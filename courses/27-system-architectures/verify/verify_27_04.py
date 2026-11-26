#!/usr/bin/env python3
"""Verify every number in chapter 27-04 (earbuds, smart glasses and XR), its problems and its lab.

Independent routes (the lab module uses closed forms):
- speaker power from pressure ratios (p/p0) and a reference pressure at 1 mW;
- ANC residuals by simulating the tone and its delayed, scaled copy in the time domain and
  taking the RMS ratio, and delay budgets by root finding on that simulation;
- LE packet sizes by building the octets and current by summing charge over a simulated second;
- battery lives by integrating the drain with an event; case recharges by stepping charge transfers;
- the thermal burst by integrating the first-order ODE C dT/dt = P - hA T;
- foveated work by counting pixels on a grid, and latency by summing stage lists.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "27-04-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import headworn as hw  # noqa: E402

v = Verifier.from_files("27-04", ROOT / "chapters" / "27-04-wearables-earbuds-and-glasses.md",
                        ROOT / "solutions" / "27-04-solutions.md", LAB / "README.md")

# ---------------------------------------------------------------------------
# Helpers (independent routes)
# ---------------------------------------------------------------------------
P0 = 20e-6  # Pa


def speaker_mw(spl, sens):
    """Power from pressure ratios: p/p_ref = 10**((SPL - S)/20), P scales with p^2."""
    p = P0 * 10 ** (spl / 20)
    p_ref = P0 * 10 ** (sens / 20)  # pressure at 1 mW
    return (p / p_ref) ** 2


def anc_resid_sim(f, tau, g=1.0):
    """RMS(residual)/RMS(noise) by sampling one second of the tone and its delayed copy."""
    fs = max(200 * f, 2e5)
    t = np.arange(0, 1.0, 1 / fs)
    n = np.cos(2 * np.pi * f * t)
    anti = -g * np.cos(2 * np.pi * f * (t - tau))
    r = n + anti
    return math.sqrt(np.mean(r ** 2) / np.mean(n ** 2))


def att_sim(f, tau, g=1.0):
    return -20 * math.log10(anc_resid_sim(f, tau, g))


def octets(payload, phy=2, enc=True):
    pkt = bytearray(b"\xaa" * (1 if phy == 1 else 2)) + bytes(4) + bytes(2) + bytes(payload)
    if enc and payload > 0:
        pkt += bytes(4)
    pkt += bytes(3)
    return len(pkt)


def airtime(payload, phy=2, enc=True):
    return 8 * octets(payload, phy, enc) / phy


def stream_sim(bitrate_kbps, frame_ms, i_rx=3.6, i_tx=4.1, i_pre=1.2, t_pre=200, t_ifs=150):
    """Average current (uA) summed frame by frame over one second."""
    n = round(bitrate_kbps * frame_ms / 8)
    t_rx = airtime(n)
    t_ack = airtime(0)
    frames = round(1000 / frame_ms)
    q_nc = 0.0
    for _ in range(frames):
        q_nc += i_pre * t_pre + i_rx * (t_rx + t_ifs) + i_tx * t_ack
    return q_nc / (frames * frame_ms * 1e3) * 1e3


def life_ode(e_mwh, p_mw, eta=1.0):
    ev = lambda t, y: y[0]  # noqa: E731
    ev.terminal = True
    sol = integrate.solve_ivp(lambda t, y: [-p_mw / eta], [0, 1e5], [e_mwh], events=ev,
                              rtol=1e-12, atol=1e-9, max_step=1.0)
    return sol.t_events[0][0]


def burst_ode(p_burst, p_idle, h, area, dt_max, tau):
    """Time (s) for the rise to reach dt_max from the idle equilibrium, by integrating
    C dT/dt = P - hA T with C = tau * hA."""
    g = h * area
    c = tau * g
    ev = lambda t, y: y[0] - dt_max  # noqa: E731
    ev.terminal = True
    sol = integrate.solve_ivp(lambda t, y: [(p_burst - g * y[0]) / c], [0, 1e5], [p_idle / g],
                              events=ev, rtol=1e-10, atol=1e-12, max_step=1.0)
    return sol.t_events[0][0]


def foveated_grid(fovea, fov, scale, n=2000):
    """Shading work by counting grid cells: full-res cells inside the fovea, scale^2 outside."""
    x = (np.arange(n) + 0.5) / n * fov - fov / 2
    xx, yy = np.meshgrid(x, x)
    inside = (np.abs(xx) <= fovea / 2) & (np.abs(yy) <= fovea / 2)
    return (inside.sum() + (~inside).sum() * scale ** 2) / inside.size


# ---------------------------------------------------------------------------
# Example 27-04.2
# ---------------------------------------------------------------------------
for k, spl in [("a", 85), ("b", 100), ("c", 110)]:
    p = speaker_mw(spl, 105)
    v.check(f"Ex 27-04.2{k}", p)
    v.check(f"Ex 27-04.2{k}1", 100 * p / (p / 0.9 + 1.0))

# ---------------------------------------------------------------------------
# Example 27-04.3
# ---------------------------------------------------------------------------
TAU = 50e-6
v.check("Ex 27-04.3a0", anc_resid_sim(100, TAU))
for k, f in [("a", 100), ("a1", 500), ("a2", 1000), ("a3", 3000)]:
    v.check(f"Ex 27-04.3{k}", att_sim(f, TAU))
tmax = optimize.brentq(lambda t: att_sim(500, t) - 20, 1e-6, 2e-4, xtol=1e-12)
v.check("Ex 27-04.3b", 1e6 * tmax)
v.check("Ex 27-04.3c0", anc_resid_sim(100, 1e-3))
v.check("Ex 27-04.3c", att_sim(100, 1e-3))
v.check("Ex 27-04.3c1", att_sim(500, 1e-3))
fcross = optimize.brentq(lambda f: anc_resid_sim(f, 1e-3) - 1.0, 100, 400, xtol=1e-6)
v.check("Ex 27-04.3c2", fcross)
v.check("Ex 27-04.3d0", anc_resid_sim(100, TAU, 1.05))
v.check("Ex 27-04.3d", att_sim(100, TAU, 1.05))
v.check("Txt 27-04.1", 1e6 * tmax)
v.check("Txt 27-04.2", fcross)
v.check("Txt 27-04.3", -20 * math.log10(0.05))
v.assert_true("lab ANC formula agrees with simulation",
              abs(hw.anc_attenuation_db(500, TAU) - att_sim(500, TAU)) < 1e-3)

# ---------------------------------------------------------------------------
# Example 27-04.4
# ---------------------------------------------------------------------------
n96 = round(96 * 10 / 8)
v.check("Ex 27-04.4a", n96)
v.check("Ex 27-04.4a1", octets(n96))
v.check("Ex 27-04.4a2", airtime(n96))
v.check("Ex 27-04.4a3", airtime(0))
on = airtime(n96) + 150 + airtime(0)
v.check("Ex 27-04.4b0", on)
v.check("Ex 27-04.4b", 100 * on / 10_000)
q = 1.2 * 200 + 3.6 * (airtime(n96) + 150) + 4.1 * airtime(0)
v.check("Ex 27-04.4c0", q)
i10 = stream_sim(96, 10)
v.check("Ex 27-04.4c", i10)
v.check("Ex 27-04.4c1", 3.0 * i10 / 1000)
n75 = round(96 * 7.5 / 8)
v.check("Ex 27-04.4d", n75)
v.check("Ex 27-04.4d1", octets(n75))
v.check("Ex 27-04.4d2", airtime(n75))
v.check("Ex 27-04.4d3", 1.2 * 200 + 3.6 * (airtime(n75) + 150) + 4.1 * airtime(0))
i75 = stream_sim(96, 7.5)
v.check("Ex 27-04.4d4", i75)
v.check("Ex 27-04.4d5", 100 * (i75 / i10 - 1))
v.assert_true("lab stream current agrees",
              abs(hw.stream_current_ua(airtime(n96), airtime(0), 150, 200, 3.6, 4.1, 1.2, 10) - i10)
              < 1e-6)

# ---------------------------------------------------------------------------
# Example 27-04.5
# ---------------------------------------------------------------------------
P5 = 8 * 0.0060 * 8
v.check("Ex 27-04.5a", P5)
v.check("Ex 27-04.5b0", 1000 / 300)
v.check("Ex 27-04.5b1", 1000 / 300 * 0.05)
sparse = 1e3 * 1000 / 300 * 0.05 / 10
white = 1e3 * 1000 / 300 / 10
v.check("Ex 27-04.5b", sparse)
v.check("Ex 27-04.5b2", white)
v.check("Ex 27-04.5b3", 100 * white / 1e3 / P5)
v.check("Ex 27-04.5c0", 0.60 / (8 * 0.006))
v.check("Ex 27-04.5c1", 0.10 / (8 * 0.006))
v.check("Ex 27-04.5c2", 0.60 / (8 * 0.006) - 0.10 / (8 * 0.006))
v.check("Ex 27-04.5c3", 0.60 / (8 * 0.006) - 8)
v.check("Ex 27-04.5c", burst_ode(0.60, 0.10, 8, 0.006, 8, 300))

# ---------------------------------------------------------------------------
# Example 27-04.6
# ---------------------------------------------------------------------------
v.check("Ex 27-04.6a", 2 * 3660 * 3200 * 90 / 1e9)
v.check("Ex 27-04.6b", foveated_grid(20, 100, 0.25))
frame = 1000 / 90
local = [2.0, frame, frame / 2, 1.0]
split = local + [3.0, 10.0, 3.0]
reproj = [2.0, 2.0, frame / 2, 1.0]
v.check("Ex 27-04.6c0", frame)
v.check("Ex 27-04.6c1", frame / 2)
for key, stages in [("c", local), ("d", split), ("e", reproj)]:
    lat = math.fsum(stages)
    err = 200 * lat / 1000
    v.check(f"Ex 27-04.6{key}", lat)
    v.check(f"Ex 27-04.6{key}2", err)
    v.check(f"Ex 27-04.6{key}3", 30 * err)
v.check("Ex 27-04.6d1", 16.0)
p_stream = 100e6 * 10e-9 + 0.5
v.check("Ex 27-04.6f", p_stream)
v.check("Ex 27-04.6f1", 8.0 - p_stream)
v.check("Txt 27-04.4", 200 * 0.020)
v.check("Txt 27-04.5", 100 * foveated_grid(20, 100, 0.25))
v.assert_true("lab foveated_fraction agrees", abs(hw.foveated_fraction(20, 100, 0.25)
                                                   - foveated_grid(20, 100, 0.25)) < 1e-6)

# ---------------------------------------------------------------------------
# Solutions
# ---------------------------------------------------------------------------
v.check("27-04.2a", speaker_mw(90, 98))
v.check("27-04.2b", speaker_mw(115, 98))
v.check("27-04.2c", speaker_mw(104, 98) / speaker_mw(98, 98))

n3 = round(160 * 7.5 / 8)
v.check("27-04.3a", n3)
v.check("27-04.3b", octets(n3, 2))
v.check("27-04.3c", airtime(n3, 2))
v.check("27-04.3d", octets(n3, 1))
v.check("27-04.3e", airtime(n3, 1))

r15 = 10 ** (-15 / 20)
v.check("27-04.4a", r15)
v.check("27-04.4a1", r15 / 2)
t4 = optimize.brentq(lambda t: att_sim(300, t) - 15, 1e-6, 5e-4, xtol=1e-12)
v.check("27-04.4a2", 1e6 * t4)
v.check("27-04.4b", anc_resid_sim(1000, t4))
v.check("27-04.4b1", att_sim(1000, t4))
f4 = optimize.brentq(lambda f: anc_resid_sim(f, t4) - 1.0, 500, 3000, xtol=1e-6)
v.check("27-04.4c", f4 / 1000)

v.check("27-04.5a1", 10 ** (-1.5))
v.check("27-04.5a", 100 * 10 ** (-1.5))
phi = 2 * math.pi * 200 * 20e-6
v.check("27-04.5b", phi)
v.check("27-04.5b1", anc_resid_sim(200, 20e-6))
v.check("27-04.5b2", att_sim(200, 20e-6))
v.check("27-04.5b3", anc_resid_sim(200, 20e-6, 1.02))
v.check("27-04.5b4", att_sim(200, 20e-6, 1.02))

eb6 = 45 * 3.85
v.check("27-04.6a", eb6)
l_on = life_ode(eb6 * 0.85, 22.0)
v.check("27-04.6b", l_on)
v.check("27-04.6b1", life_ode(eb6 * 0.85, 15.0))
ec = 480 * 3.85
v.check("27-04.6c", ec)
v.check("27-04.6c1", 0.65 * ec)
v.check("27-04.6c2", 2 * eb6)
# step the case: transfer whole pair recharges, then the fraction left
avail, full = 0.65 * ec, 0
while avail >= 2 * eb6:
    avail -= 2 * eb6
    full += 1
nrech = full + avail / (2 * eb6)
v.check("27-04.6c3", nrech)
v.check("27-04.6d", (1 + nrech) * l_on)

po = speaker_mw(85, 105)
v.check("27-04.7a", po)
pin = po / 0.9 + 1.0
v.check("27-04.7b", pin)
s1 = pin - (po / 0.9 + 0.5)
s2 = pin - (po / 0.95 + 1.0)
v.check("27-04.7c", s1)
v.check("27-04.7d", s2)
v.check("27-04.7e", s1 / s2)

p8 = 6 * 0.0045 * 6
v.check("27-04.8a", p8)
v.check("27-04.8b", 0.080 + 0.250)
v.check("27-04.8b1", 0.330 / p8)
v.check("27-04.8c", 0.330 / (6 * 0.0045))
v.check("27-04.8c1", 0.080 / (6 * 0.0045))
v.check("27-04.8c2", burst_ode(0.330, 0.080, 6, 0.0045, 6, 240))

lmax = optimize.brentq(lambda L: hw.waveguide_display_mw(L, 500, 0.10, 15) - 50, 1, 1e5)
v.check("27-04.9a", lmax)
v.check("27-04.9b", lmax * 0.10)

e_tx = 200e3 * 8 * 20e-9
v.check("27-04.10a", e_tx)
v.check("27-04.10b", 2.0 / e_tx)

def work_closed(th, fov_deg=100, scale=1 / 3):
    a = (th / fov_deg) ** 2
    return a + (1 - a) * scale ** 2


fov = optimize.brentq(lambda th: work_closed(th) - 0.15, 5, 60, xtol=1e-10)
v.assert_true("grid count agrees at the solved fovea", abs(foveated_grid(fov, 100, 1 / 3) - 0.15) < 2e-3)
v.check("27-04.11b", fov)
v.check("27-04.11a", (fov / 100) ** 2)

v.check("27-04.12a", 1000 / 300)
lat12 = 2 + 2 + 1.1 + 1
v.check("27-04.12b", lat12)
v.check("27-04.12c", 300 * lat12 / 1000)

v.check("27-04.13a", life_ode(35.0, 12.0))
v.check("27-04.13b", life_ode(35.0, 5.5))
v.check("27-04.13c", 3.0 + 10.0 + 3.0)

# ---------------------------------------------------------------------------
# Lab
# ---------------------------------------------------------------------------
f10 = optimize.brentq(lambda f: att_sim(f, 50e-6) - 10, 200, 3000, xtol=1e-6)
v.check("Lab 27-04.a", f10 / 1000)
v.check("Lab 27-04.b", round(192 * 10 / 8))
v.check("Lab 27-04.b1", stream_sim(192, 10))
v.check("Lab 27-04.c", 1e4 * 0.5 / (8 * 8))
v.check("Lab 27-04.d", foveated_grid(30, 100, 0.25))

# ---------------------------------------------------------------------------
# Example 27-04.1 (earbud budget): filled in below
# ---------------------------------------------------------------------------
eb1 = 50 * 3.85
v.check("Ex 27-04.1a", eb1)
rails = {"radio": 1.0, "dsp": 10.0, "anc": 8.0, "amp": 1.0, "sensors": 1.0, "pmic": 0.5}
on = math.fsum(rails.values())
off = on - rails["anc"]
v.check("Ex 27-04.1b", on)
v.check("Ex 27-04.1b1", on / 0.85)
v.check("Ex 27-04.1b2", off)
v.check("Ex 27-04.1b3", off / 0.85)
life_on = life_ode(eb1 * 0.85, on)
v.check("Ex 27-04.1c", life_on)
v.check("Ex 27-04.1c1", life_ode(eb1 * 0.85, off))
v.check("Ex 27-04.1d", 100 * rails["dsp"] / on)
v.check("Ex 27-04.1d1", 100 * rails["anc"] / on)
v.check("Ex 27-04.1d2", 100 * rails["radio"] / on)
v.check("Ex 27-04.1d3", 100 * rails["pmic"] / on)
v.check("Ex 27-04.1g", 100 * (rails["dsp"] + rails["anc"]) / on)
ec1 = 500 * 3.85
v.check("Ex 27-04.1e0", ec1)
v.check("Ex 27-04.1e", 0.70 * ec1)
v.check("Ex 27-04.1e1", 2 * eb1)
avail, full = 0.70 * ec1, 0
while avail >= 2 * eb1:
    avail -= 2 * eb1
    full += 1
n1 = full + avail / (2 * eb1)
v.check("Ex 27-04.1e2", n1)
v.check("Ex 27-04.1e3", (1 + n1) * life_on)
v.check("Ex 27-04.1f0", on - 5.0)
v.check("Ex 27-04.1f", life_ode(eb1 * 0.85, on - 5.0))

v.check("Txt 27-04.6", 100 * (7 / 6 - 1))
v.check("Txt 27-04.7", 100 * (12 / 8 - 1))
v.check("Txt 27-04.8", 100 * (1 - (210 / 160) / 2))
v.check("Txt 27-04.9", 2 * 3552 * 3840 / 1e6)
v.check("Txt 27-04.10", 4 * 0.9 * 5.670374e-8 * 303.15 ** 3)
v.check("Txt 27-04.11", 5 / (6 * 1e-3))
v.check("Txt 27-04.12", 1 + 0.7 * 500 * 3.85 / (2 * 50 * 3.85))

# Problem 27-04.14: complex residual evaluated directly
v.check("27-04.14a", 20 * math.log10(0.9))
v.check("27-04.14b", 20 * math.log10(1.1))
ph14 = 2 * math.pi * 500 * 20e-6
v.check("27-04.14c", ph14)
ra = math.hypot(0.05, ph14)
re_ = abs(1 - 1.05 * np.exp(-1j * ph14))
v.check("27-04.14d", ra)
v.check("27-04.14e", -20 * math.log10(ra))
v.check("27-04.14f", re_)
v.check("27-04.14g", -20 * math.log10(re_))
v.assert_true("|R| = 2|sin(pi f tau)| at unit gain",
              abs(abs(1 - np.exp(-1j * ph14)) - 2 * abs(math.sin(ph14 / 2))) < 1e-14)

# Problem 27-04.15: count the bits on air for each packet and integrate current over an event
oct15 = 32000 * 0.0075 / 8
bits_on_air = 8 * (2 + 4 + 2 + oct15 + 4 + 3)
t15 = bits_on_air / 2e6 * 1e6
on15 = t15 + 150 + t15
q15 = 1.2 * 200 + 3.6 * (t15 + 150) + 4.1 * t15
i15 = q15 / 7.5
p15 = 3.0 * i15 / 1e3
v.check("27-04.15a", oct15)
v.check("27-04.15b", t15)
v.check("27-04.15c", on15)
v.check("27-04.15d", 100 * on15 / 7500)
v.check("27-04.15e", q15)
v.check("27-04.15f", i15)
v.check("27-04.15g", p15)
v.check("27-04.15h", 55 * 3.85)
v.check("27-04.15i", 9.0 + p15)
v.check("27-04.15j", 55 * 3.85 / (9.0 + p15))

sys.exit(v.finish())
