#!/usr/bin/env python3
"""Verify every number in chapter 22-02 (buck converter steady state), its problems and its lab.

Independent routes (the lab module buck.py uses closed forms and matrix exponentials):
- CCM ripples, RMS currents and conduction-loss efficiency come from brute-force time stepping of the switched
  ODEs until periodic steady state, with RMS values integrated from the simulated waveforms;
- DCM operating points come from simulating one period piecewise (on, freewheel until the current reaches zero,
  idle) and solving for the capacitor voltage that repeats, by root finding, then measuring D2, D3 and the peak;
- PFM pulses come from integrating one pulse with an event at zero current;
- duty cycles with resistances are found by root finding on the DC model;
- the ripple-ratio optimum of Problem 22-02.15 is found numerically.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "22-02-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("22-02", ROOT / "chapters" / "22-02-buck-converter-steady-state.md",
                        ROOT / "solutions" / "22-02-solutions.md", LAB / "README.md")


def ccm_sim(v_in, d, fs, ind, cap, r, r_hs=0.0, r_ls=0.0, r_l=0.0, periods=400, pts=3000):
    """Brute-force switched ODE to steady state; returns dict of ripple, RMS currents, powers, average."""
    t_s = 1 / fs

    def rhs(vs, rs):
        return lambda t, y: [(vs - y[0] * (rs + r_l) - y[1]) / ind, y[0] / cap - y[1] / (r * cap)]

    on, off = rhs(v_in, r_hs), rhs(0.0, r_ls)
    x = np.array([v_in * d / r, v_in * d])
    for _ in range(periods):
        s1 = integrate.solve_ivp(on, (0, d * t_s), x, rtol=1e-10, atol=1e-13)
        s2 = integrate.solve_ivp(off, (0, (1 - d) * t_s), s1.y[:, -1], rtol=1e-10, atol=1e-13)
        x = s2.y[:, -1]
    t1 = np.linspace(0, d * t_s, pts)
    t2 = np.linspace(0, (1 - d) * t_s, pts)
    s1 = integrate.solve_ivp(on, (0, d * t_s), x, t_eval=t1, rtol=1e-11, atol=1e-14)
    s2 = integrate.solve_ivp(off, (0, (1 - d) * t_s), s1.y[:, -1], t_eval=t2, rtol=1e-11, atol=1e-14)
    il1, il2 = s1.y[0], s2.y[0]
    vo = np.concatenate([s1.y[1], s2.y[1]])
    il = np.concatenate([il1, il2])
    tt = np.concatenate([t1, d * t_s + t2])
    ms = lambda y, tv: np.trapezoid(y * y, tv) / t_s  # noqa: E731
    i_load = vo / r
    i_cout = il - i_load
    i_avg_in = np.trapezoid(il1, t1) / t_s
    return {
        "di": il.max() - il.min(),
        "dv": vo.max() - vo.min(),
        "vavg": np.trapezoid(vo, tt) / t_s,
        "il_rms": math.sqrt(ms(il, tt)),
        "hs_rms": math.sqrt(ms(il1, t1)),
        "ls_rms": math.sqrt(ms(il2, t2)),
        "cin_rms": math.sqrt((np.trapezoid((il1 - i_avg_in) ** 2, t1) + i_avg_in ** 2 * (1 - d) * t_s) / t_s),
        "cout_rms": math.sqrt(ms(i_cout, tt)),
        "p_in": v_in * i_avg_in,
        "p_out": np.trapezoid(vo * vo / r, tt) / t_s,
    }


def ccm_fourier(v_in, d, fs, ind, cap, r, nh=6000, npts=24000):
    """Ideal-switch CCM steady state by Fourier synthesis through the loaded LC (independent of time stepping)."""
    t_s = 1 / fs
    t = np.linspace(0, t_s, npts, endpoint=False)
    w = 2 * math.pi * fs
    il = np.full_like(t, d * v_in / r)
    vo = np.full_like(t, d * v_in)
    for n in range(1, nh + 1):
        cn = v_in / (1j * 2 * math.pi * n) * (1 - np.exp(-1j * 2 * math.pi * n * d))
        wn = n * w
        zp = 1 / (1 / r + 1j * wn * cap)
        iln = cn / (1j * wn * ind + zp)
        ph = np.exp(1j * wn * t)
        il += 2 * np.real(iln * ph)
        vo += 2 * np.real(iln * zp * ph)
    on = t < d * t_s
    dt = t_s / npts
    ms = lambda y: float(np.sum(y * y) * dt / t_s)  # noqa: E731
    i_in_avg = float(np.sum(np.where(on, il, 0.0)) * dt / t_s)
    i_cin = np.where(on, il, 0.0) - i_in_avg
    return {
        "di": il.max() - il.min(), "dv": vo.max() - vo.min(), "vavg": float(np.mean(vo)),
        "il_rms": math.sqrt(ms(il)), "hs_rms": math.sqrt(ms(np.where(on, il, 0.0))),
        "ls_rms": math.sqrt(ms(np.where(on, 0.0, il))), "cin_rms": math.sqrt(ms(i_cin)),
        "cout_rms": math.sqrt(ms(il - vo / r)),
    }


def dcm_period(v_in, d1, fs, ind, cap, r, v0):
    """Simulate one DCM period from i_L = 0, v_C = v0; returns (v_end, t_freewheel, i_peak)."""
    t_s = 1 / fs
    on = lambda t, y: [(v_in - y[1]) / ind, y[0] / cap - y[1] / (r * cap)]  # noqa: E731
    s1 = integrate.solve_ivp(on, (0, d1 * t_s), [0.0, v0], rtol=1e-11, atol=1e-14)
    ipk = s1.y[0, -1]
    ev = lambda t, y: y[0]  # noqa: E731
    ev.terminal = True
    ev.direction = -1
    off = lambda t, y: [(-y[1]) / ind, y[0] / cap - y[1] / (r * cap)]  # noqa: E731
    s2 = integrate.solve_ivp(off, (0, (1 - d1) * t_s), s1.y[:, -1], events=ev, rtol=1e-11, atol=1e-14)
    t2 = s2.t[-1]
    vc = s2.y[1, -1]
    t3 = (1 - d1) * t_s - t2
    return vc * math.exp(-t3 / (r * cap)), t2, ipk


def dcm_steady(v_in, d1, fs, ind, cap, r):
    v0 = optimize.brentq(lambda x: dcm_period(v_in, d1, fs, ind, cap, r, x)[0] - x, 1e-3, v_in, xtol=1e-12)
    _, t2, ipk = dcm_period(v_in, d1, fs, ind, cap, r, v0)
    return v0, t2 * fs, ipk


def pfm_charge(v_in, v_out, t_on, ind):
    """Integrate one fixed-on-time pulse into a constant output voltage; returns (ipk, t_off, charge)."""
    s1 = integrate.solve_ivp(lambda t, y: [(v_in - v_out) / ind, y[0]], (0, t_on), [0.0, 0.0], rtol=1e-12,
                             atol=1e-20)
    ev = lambda t, y: y[0]  # noqa: E731
    ev.terminal = True
    s2 = integrate.solve_ivp(lambda t, y: [-v_out / ind, y[0]], (0, 10 * t_on), s1.y[:, -1], events=ev,
                             rtol=1e-12, atol=1e-20)
    return s1.y[0, -1], s2.t[-1], s2.y[1, -1]


def duty_dc(v_in, v_out, i_out, r_hs, r_ls, r_l, v_f=None):
    if v_f is None:
        f = lambda dd: dd * v_in - i_out * (dd * r_hs + (1 - dd) * r_ls + r_l) - v_out  # noqa: E731
    else:
        f = lambda dd: dd * v_in - (1 - dd) * v_f - i_out * (dd * r_hs + r_l) - v_out  # noqa: E731
    return optimize.brentq(f, 1e-6, 1 - 1e-6, xtol=1e-14)


# ---------------------------------------------------------------- Example 22-02.1
print("Example 22-02.1")
VIN, V, I, FS = 12.0, 1.2, 10.0, 600e3
D = V / VIN
L = V * (1 - D) / (FS * 0.3 * I)
v.check("Ex 22-02.1a", D)
v.check("Ex 22-02.1b", D / FS * 1e9)
v.check("Ex 22-02.1d", L * 1e6)
sim = ccm_fourier(VIN, D, FS, L, 62.5e-6, V / I)
v.check("Ex 22-02.1c", sim["di"])
v.check("Ex 22-02.1e", I + sim["di"] / 2)
v.check("Ex 22-02.1f", I - sim["di"] / 2)

# ---------------------------------------------------------------- Example 22-02.2
print("Example 22-02.2")
C = optimize.brentq(lambda c: 3.0 / (8 * FS * c) - 0.010, 1e-7, 1e-2)
v.check("Ex 22-02.2a", C * 1e6)
v.check("Ex 22-02.2b", 0.005 / 3.0 * 1e3)
v.check("Ex 22-02.2c", C / 0.5 * 1e6)
v.check("Ex 22-02.2d", math.ceil(C / 0.5 / 22e-6))
v.check("Ex 22-02.2e", sim["dv"] * 1e3)

# ---------------------------------------------------------------- Example 22-02.3
print("Example 22-02.3")
v.check("Ex 22-02.3a", sim["il_rms"])
v.check("Ex 22-02.3b", sim["hs_rms"])
v.check("Ex 22-02.3c", sim["ls_rms"])
v.check("Ex 22-02.3d", sim["cin_rms"])
v.check("Ex 22-02.3e", sim["cout_rms"])
v.check("Ex 22-02.3f", sim["cin_rms"] / sim["cout_rms"])
v.assert_true("switch RMS currents add in quadrature to the inductor's",
              abs(sim["hs_rms"] ** 2 + sim["ls_rms"] ** 2 - sim["il_rms"] ** 2) < 1e-6)

# ---------------------------------------------------------------- Example 22-02.4
print("Example 22-02.4")
d4 = duty_dc(VIN, V, I, 8e-3, 3e-3, 1e-3)
req = d4 * 8e-3 + (1 - d4) * 3e-3 + 1e-3
v.check("Ex 22-02.4a", d4)
v.check("Ex 22-02.4b", req * 1e3)
v.check("Ex 22-02.4c", I * I * req)
v.check("Ex 22-02.4d", V * I / (V * I + I * I * req) * 100)
d4d = duty_dc(VIN, V, I, 8e-3, 0, 1e-3, v_f=0.5)
pd = (1 - d4d) * 0.5 * I
v.check("Ex 22-02.4e", d4d)
v.check("Ex 22-02.4f", pd)
v.check("Ex 22-02.4g", V * I / (V * I + pd + I * I * (d4d * 8e-3 + 1e-3)) * 100)
v.check("Ex 22-02.4h", pd / (V * I) * 100)
v.check("Ex 22-02.4i", 0.5 * 0.75 / 12 * 100)
simB = ccm_sim(VIN, d4, FS, L, 62.5e-6, V / I, 8e-3, 3e-3, 1e-3)
v.check("Lab 22-02.a", simB["p_out"] / simB["p_in"] * 100)

# ---------------------------------------------------------------- Example 22-02.5
print("Example 22-02.5")
v.check("Ex 22-02.5a", sim["di"] / 2)
K = 2 * L * FS / 4.0
v.check("Ex 22-02.5b", K)
v.check("Ex 22-02.5c", 1 - D)
# a 100 mF capacitor makes the ripple negligible: the small-ripple limit the example assumes
CBIG = 100e-3
d1 = optimize.brentq(lambda x: dcm_steady(VIN, x, FS, L, CBIG, 4.0)[0] - 1.2, 0.01, 0.099, xtol=1e-12)
vss, d2, ipk = dcm_steady(VIN, d1, FS, L, CBIG, 4.0)
v.check("Ex 22-02.5d", d1)
v.check("Ex 22-02.5e", d1 / FS * 1e9)
v.check("Ex 22-02.5f", d2)
v.check("Ex 22-02.5g", 1 - d1 - d2)
v.check("Ex 22-02.5h", ipk)

# ---------------------------------------------------------------- Example 22-02.6
print("Example 22-02.6")
TON = 1.8 / 3.6 * 556e-9
ipk6, toff6, q6 = pfm_charge(3.6, 1.8, TON, 2.2e-6)
v.check("Ex 22-02.6a", TON * 1e9)
v.check("Ex 22-02.6b", ipk6)
v.check("Ex 22-02.6c", q6 * 1e9)
v.check("Ex 22-02.6d", 1e-3 / q6 / 1e3)
v.check("Ex 22-02.6e", 1e-6 / q6)
v.check("Ex 22-02.6f", q6 / 556e-9)
v.assert_true("PFM boundary load equals ipk/2", abs(q6 / 556e-9 - ipk6 / 2) < 1e-9)
v.check("Ex 22-02.6g", q6 / 10e-6 * 1e3)

# ---------------------------------------------------------------- Example 22-02.7
print("Example 22-02.7")
v.check("Ex 22-02.7a", (1 / 48) / 68e-9 / 1e3)
v.check("Ex 22-02.7b", (1 / 12) / 68e-9 / 1e6)
v.check("Ex 22-02.7c", 1.8 + 0.5 * 0.5)

# ---------------------------------------------------------------- text
print("Text")
v.check("Txt 22-02.a", 0.4785 / (8 * 500e3 * 1e-6) * 1e3)
v.check("Txt 22-02.b", (math.sqrt(1 + 0.09 / 12) - 1) * 100)

# ---------------------------------------------------------------- problems
print("Problems")
v.check("22-02.1a", optimize.brentq(lambda x: (24 - x) * 0.25 - x * 0.75, 0, 24))
v.check("22-02.1b", 0.25 * 3)

s2 = ccm_fourier(5.0, 0.36, 2e6, 1e-6, 22e-6, 0.9)
v.check("22-02.2a", 1.8 / 5)
v.check("22-02.2b", s2["di"])
v.check("22-02.2c", s2["di"] / 2)
v.check("22-02.2d", 2 + s2["di"] / 2)
v.check("22-02.2e", s2["dv"] * 1e3)
v.check("22-02.3a", s2["il_rms"])
v.check("22-02.3b", s2["hs_rms"])
v.check("22-02.3c", s2["ls_rms"])
v.check("22-02.3d", s2["cin_rms"])
v.check("22-02.3e", s2["cout_rms"])

dvc = 2 / (8 * 100e3 * 220e-6)
v.check("22-02.4a", dvc * 1e3)
v.check("22-02.4b", 0.030 * 2 * 1e3)
v.check("22-02.4c", (dvc + 0.06) * 1e3)
v.check("22-02.4d", (0.020 - dvc) / 2 * 1e3)

d5 = duty_dc(5.0, 1.0, 6.0, 0.020, 0.010, 0.005)
r5 = d5 * 0.020 + (1 - d5) * 0.010 + 0.005
v.check("22-02.5a", d5)
v.check("22-02.5b", r5 * 1e3)
v.check("22-02.5c", 36 * r5)
v.check("22-02.5d", 6 / (6 + 36 * r5) * 100)

d6 = duty_dc(12.0, 5.0, 3.0, 0, 0, 0, v_f=0.45)
pd6 = (1 - d6) * 0.45 * 3
ps6 = (1 - 5 / 12) * 9 * 0.015
v.check("22-02.6a", d6)
v.check("22-02.6b", pd6)
v.check("22-02.6c", ps6)
v.check("22-02.6d", pd6 / ps6)
v.check("22-02.6e", pd6 / 15 * 100)
v.check("22-02.6f", ps6 / 15 * 100)

D7 = 5 / 24
di7 = 5 * (1 - D7) / (300e3 * 22e-6)
K7 = 2 * 22e-6 * 300e3 / 50
v.check("22-02.7a", di7)
v.check("22-02.7b", di7 / 2)
v.check("22-02.7c", K7)
v.check("22-02.7d", 1 - D7)
# open-loop DCM from the simulation, in the small-ripple limit
v8, _, _ = dcm_steady(24.0, D7, 300e3, 22e-6, CBIG, 50.0)
v.check("22-02.8a", v8 / 24)
v.check("22-02.8b", v8)
d18 = optimize.brentq(lambda x: dcm_steady(24.0, x, 300e3, 22e-6, CBIG, 50.0)[0] - 5.0, 0.05, D7, xtol=1e-12)
v.check("22-02.8c", d18)

ipk9, toff9, q9 = pfm_charge(4.0, 1.2, 200e-9, 1e-6)
v.check("22-02.9a", ipk9)
v.check("22-02.9b", toff9 * 1e9)
v.check("22-02.9c", q9 * 1e9)
v.check("22-02.9d", 10e-3 / q9 / 1e3)
v.check("22-02.9e", 1 / (200e-9 + toff9) / 1e6)
v.check("22-02.9f", q9 / (200e-9 + toff9))

rb = 5 / (di7 / 2)
v.check("22-02.10a", rb)
v.check("22-02.10b", 2 * 22e-6 * 300e3 / rb)

v.check("22-02.11a", (0.9 / 20) / 50e-9 / 1e3)
v.check("22-02.11b", (0.9 / 20) / 60e-9 / 1e3)

dmin = 3.3 / 13.2
l12 = 3.3 * (1 - dmin) / (1e6 * 1.5)
v.check("22-02.12a", dmin)
v.check("22-02.12b", l12 * 1e6)
v.check("22-02.12c", 5 + 0.75)
c12 = 1.5 / (8 * 1e6 * 0.015)
v.check("22-02.12d", c12 * 1e6)
v.check("22-02.12e", c12 / 0.6 * 1e6)
v.check("22-02.12f", 0.005 / 1.5 * 1e3)
worst = max(5 * math.sqrt(dd * (1 - dd)) for dd in np.linspace(3.3 / 13.2, 3.3 / 10.8, 1001))
v.check("22-02.12g", worst)
v.check("22-02.12h", dmin / 1e6 * 1e9)

v.check("22-02.13a", 3.3 / 4.2)
v.check("22-02.13b", 3.3 + 0.3 * 0.3)
v.check("22-02.13c", 0.3 * 0.3)

s14 = ccm_fourier(12.0, 0.5, 500e3, 1e-3, 100e-6, 0.6)   # large L: the small-ripple limit the problem assumes
v.check("22-02.14a", s14["cin_rms"])
v.check("22-02.14b", s14["cin_rms"] / 4)
v.check("22-02.14c", (s14["cin_rms"] / 4) ** 2 * 0.005 * 4 * 1e3)
v.check("22-02.14d", (s14["cin_rms"] / 4) ** 2 * 0.005 * 1e3)

g = lambda r: (1 + r / 2) ** 2 / r  # noqa: E731
ropt = optimize.minimize_scalar(g, bounds=(0.05, 10), method="bounded").x
v.assert_true("stored energy is minimized at r = 2", abs(ropt - 2) < 1e-4)
v.check("22-02.15a", g(0.3))
v.check("22-02.15b", g(2))
v.check("22-02.15c", g(0.3) / g(2))

# ---------------------------------------------------------------- lab
print("Lab")
sys.path.insert(0, str(LAB))
import buck as bk  # noqa: E402

_, il, vo, pin, pout = bk.pss(VIN, d4, FS, L, 62.5e-6, V / I, 8e-3, 3e-3, 1e-3)
v.assert_true("lab PSS efficiency equals brute-force efficiency", abs(pout / pin - simB["p_out"] / simB["p_in"]) < 1e-6)
v.assert_true("lab DCM duty equals simulated duty", abs(bk.dcm_duty_for_ratio(0.1, K) - d1) < 1e-6)

sys.exit(v.finish())
