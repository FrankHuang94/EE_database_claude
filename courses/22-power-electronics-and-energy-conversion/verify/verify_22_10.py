#!/usr/bin/env python3
"""Verify every number in chapter 22-10 (datacenter power delivery), its problems and its lab.

Independent routes (the lab module pdn.py uses the closed forms):
- busbar losses by discretizing the bar into many segments with taps and summing I²R segment by segment;
- AC/DC conductor capacity by averaging the instantaneous power of sampled three-phase waveforms;
- conversion chains by sequential power flow; PUE by definition;
- multiphase ripple by building each phase's piecewise-linear inductor current in time, summing and taking the
  peak-to-peak value;
- the package resonance from the eigenvalues of the L–C state matrix, impedance peaks by a frequency sweep, first
  droops by integrating the circuit ODE (solve_ivp), and the optimum ESR by numerical minimization;
- plane resistance as parallel strips; capacitor storage by integrating C v dv.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "22-10-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import pdn  # noqa: E402

v = Verifier.from_files("22-10", ROOT / "chapters" / "22-10-datacenter-power-delivery.md",
                        ROOT / "solutions" / "22-10-solutions.md", LAB / "README.md")
RHO = 1.72e-8


# ---------------------------------------------------------------- helpers
def bar_loss_discrete(i_total, r_loop, profile, n=20000):
    """Split the loop into n segments; profile(u) gives the fraction of the current still flowing at position u."""
    u = (np.arange(n) + 0.5) / n
    return float(np.sum((i_total * profile(u)) ** 2 * r_loop / n))


def per_conductor_sampled(v_dc, v_ll, n_ac, pf, i_rms=1.0, n=20000):
    """Average three-phase power per conductor from sampled waveforms, against DC power per conductor."""
    th = np.linspace(0, 2 * math.pi, n, endpoint=False)
    vph = v_ll / math.sqrt(3) * math.sqrt(2)
    phi = math.acos(pf)
    p = sum(vph * np.cos(th - k * 2 * math.pi / 3) * i_rms * math.sqrt(2) * np.cos(th - k * 2 * math.pi / 3 - phi)
            for k in range(3)).mean()
    return (v_dc * i_rms / 2) / (p / n_ac)


def chain_input(p_chip, etas):
    p = p_chip
    for eta in reversed(etas):        # VRM first, then upstream stages
        p = p / eta
    return p


def summed_ripple_time(n, v_in, v_out, l, fs, samples=120000):
    """Build each phase's inductor current over one period, shift by T/n, sum, take p-p. The sample count is a
    multiple of 4, 6, 12, 15 and 20, so every switching instant used here falls on a sample."""
    t_per = 1 / fs
    d = v_out / v_in
    t = np.linspace(0, t_per, samples, endpoint=False)

    def phase(tt):
        tt = np.mod(tt, t_per)
        up = (v_in - v_out) / l
        dn = v_out / l
        return np.where(tt < d * t_per, up * tt, up * d * t_per - dn * (tt - d * t_per))
    tot = sum(phase(t - k * t_per / n) for k in range(n))
    return float(tot.max() - tot.min()), float(phase(t).max() - phase(t).min())


def lc_resonance(l, c):
    a = np.array([[0.0, -1 / l], [1 / c, 0.0]])            # states: iL, vC
    w = abs(np.linalg.eigvals(a)[0].imag)
    return w / (2 * math.pi)


def droop(l, c, di, r_esr, t_end=None):
    """Die-node deviation for a load step di at t = 0, stiff source behind l, capacitor c with series r_esr."""
    f0 = lc_resonance(l, c)
    t_end = t_end or 4 / f0
    def f(t, y):
        il, vc = y
        ic = il - di
        vn = vc + r_esr * ic
        return [-vn / l, ic / c]
    sol = integrate.solve_ivp(f, (0, t_end), [0.0, 0.0], max_step=1 / f0 / 4000, rtol=1e-10, atol=1e-15)
    il, vc = sol.y
    vn = vc + r_esr * (il - di)
    k = int(np.argmin(vn[: np.searchsorted(sol.t, 0.6 / f0)])) if r_esr == 0 else int(np.argmin(vn))
    return -float(vn[k]), float(sol.t[k])


def z_die(f, l, c, r_esr):
    s = 2j * math.pi * f
    zl = s * l
    zc = r_esr + 1 / (s * c)
    return zl * zc / (zl + zc)


# ---------------------------------------------------------------- Example 22-10.1
r_any = 1e-4
v.check("Ex 22-10.1a", optimize.brentq(lambda i: 50 * i - 120e3, 1, 1e6))
v.check("Ex 22-10.1b", optimize.brentq(lambda i: 800 * i - 120e3, 1, 1e6))
v.check("Ex 22-10.1c", ((120e3 / 50) ** 2 * r_any) / ((120e3 / 800) ** 2 * r_any))

# ---------------------------------------------------------------- Example 22-10.2
a_bar = 10e-3 * 60e-3
r_one = integrate.quad(lambda x: RHO / a_bar, 0, 1.5)[0]
r_loop = 2 * r_one
v.check("Ex 22-10.2a", r_one * 1e6)
v.check("Ex 22-10.2b", r_loop * 1e6)
v.check("Ex 22-10.2c", bar_loss_discrete(2400, r_loop, lambda u: np.ones_like(u)))
v.check("Ex 22-10.2d", bar_loss_discrete(2400, r_loop, lambda u: 1 - u))
v.check("Ex 22-10.2e", 2 * a_bar * 1.5 * 8960)
v.check("Ex 22-10.2f", bar_loss_discrete(150, r_loop, lambda u: 1 - u))
v.check("Txt 22-10.e", 2 * a_bar * 1.5 * 8960 * (1e6 / 120e3))
v.check("Txt 22-10.n", 100 * bar_loss_discrete(2400, r_loop, lambda u: 1 - u) / 120e3)

# ---------------------------------------------------------------- AC vs DC (text)
r3 = per_conductor_sampled(800, 415, 3, 1.0)
r4 = per_conductor_sampled(800, 415, 4, 1.0)
v.check("Txt 22-10.a", r3)
v.check("Txt 22-10.b", r4)
v.check("Txt 22-10.c", 100 * (r3 - 1))
v.check("Txt 22-10.d", 100 * (r4 - 1))
v.assert_true("pdn.per_conductor_ratio agrees", abs(pdn.per_conductor_ratio(800, 415, 3) - r3) < 1e-6)

# ---------------------------------------------------------------- Example 22-10.3
etas = [0.97, 0.975, 0.98, 0.90]
p_in = chain_input(1.0, etas)
v.check("Ex 22-10.3a", 100 / p_in)
v.check("Ex 22-10.3b", p_in)
v.check("Ex 22-10.3c", p_in - 1.0)
p_it = chain_input(1.0, etas[1:])  # PUE meters IT power at the UPS output, the rack-PSU input
v.check("Ex 22-10.3f", p_it)
v.check("Ex 22-10.3d", 1.09 * p_it)
v.check("Ex 22-10.3e", 1.54 * p_it)
vrm_loss = 1 / 0.90 - 1
v.assert_true("Ex 22-10.3: the VRM is more than half the loss", vrm_loss / (p_in - 1) > 0.5)

# ---------------------------------------------------------------- Example 22-10.4
sum20, one = summed_ripple_time(20, 12, 0.8, 100e-9, 1e6)
sum4, _ = summed_ripple_time(4, 12, 0.8, 100e-9, 1e6)
sum15, _ = summed_ripple_time(15, 12, 0.8, 100e-9, 1e6)
v.check("Ex 22-10.4a", 1000 / 20)
v.check("Ex 22-10.4b", 0.8 / 12)
v.check("Ex 22-10.4c", one)
v.check("Ex 22-10.4d", sum20)
v.check("Ex 22-10.4e", 20 * 1.0)
v.check("Ex 22-10.4f", sum4)
v.check("Ex 22-10.4g", round(sum15, 6))
v.check("Ex 22-10.4h", 20 * (12 - 0.8) / 100e-9 / 1e6)
v.assert_true("pdn.summed_ripple agrees with the time-domain sum",
              abs(pdn.summed_ripple(20, 12, 0.8 / 12, 100e-9, 1e6) - sum20) < 1e-6)

# ---------------------------------------------------------------- Example 22-10.5
i_pts = np.array([0.0, 1000.0])
v_pts = np.array([0.85, 0.75])
slope, icpt = np.polyfit(i_pts, v_pts, 1)
v.check("Ex 22-10.5a", 0.05 / 1000 * 1e6)
v.check("Ex 22-10.5b", -slope * 1e3)
v.check("Ex 22-10.5c", icpt + slope * 500)
v.check("Ex 22-10.5d", (0.85 - 0.75) / 1000 * 1e6)
v.check("Ex 22-10.5e", (0.80 - (icpt + slope * 1000)) * 1000)
v.check("Ex 22-10.5f", 100 * (0.80 - (icpt + slope * 1000)) / 0.80)

# ---------------------------------------------------------------- Example 22-10.6 and the lab
L6, C6 = 2e-12, 20e-6
f6 = lc_resonance(L6, C6)
z0 = math.sqrt(L6 / C6)
d0, t0 = droop(L6, C6, 100, 0.0)
d1, t1 = droop(L6, C6, 100, 0.1e-3)
v.check("Ex 22-10.6a", f6 / 1e6)
v.check("Ex 22-10.6b", z0 * 1e6)
v.check("Ex 22-10.6c", d0 * 1e3)
v.check("Ex 22-10.6d", t0 * 1e9)
v.check("Ex 22-10.6e", 0.025 / 100 * 1e6)
v.check("Ex 22-10.6f", optimize.brentq(lambda cu: math.sqrt(L6 / (cu * 1e-6)) - 250e-6, 0.1, 1000))
v.check("Ex 22-10.6g", d1 * 1e3)
v.assert_true("Ex 22-10.6g: the damped droop occurs about 7 ns after the step", 6.5e-9 < t1 < 7.5e-9)
fs = np.logspace(6, 9, 20001)
zs = np.abs(z_die(fs, L6, C6, 0.1e-3))
v.check("Lab 22-10.a", zs.max() * 1e3)
v.check("Lab 22-10.b", z0 ** 2 / 0.1e-3 * 1e3)
opt = optimize.minimize_scalar(lambda r: droop(L6, C6, 100, r)[0], bounds=(1e-6, 0.6e-3), method="bounded",
                               options={"xatol": 1e-9})
v.check("Lab 22-10.c", opt.fun * 1e3)
v.check("Lab 22-10.d", opt.x * 1e3)
v.assert_true("too much ESR: 0.5 mohm gives at least the 50 mV resistive step", droop(L6, C6, 100, 0.5e-3)[0] >= 0.05 - 1e-9)

# ---------------------------------------------------------------- Example 22-10.7
def plane_loop(length, width, t, n):
    r_plane = RHO * length / (width * t)
    return 2 / sum(1 / r_plane for _ in range(n))


v.check("Ex 22-10.7a", RHO / 70e-6 * 1e3)
v.check("Ex 22-10.7b", RHO * 20e-3 / (50e-3 * 70e-6) * 1e6)
rl7 = plane_loop(20e-3, 50e-3, 70e-6, 8)
v.check("Ex 22-10.7c", rl7 * 1e6)
v.check("Ex 22-10.7d", 1000 ** 2 * rl7)
v.check("Ex 22-10.7e", 100 * 1000 * rl7 / 0.8)

# ---------------------------------------------------------------- Example 22-10.8
v.check("Ex 22-10.8a", 65 / (0.70 * 1400) * 1e3)
v.check("Ex 22-10.8b", 72 * 65 / 1e3)
v.check("Ex 22-10.8c", optimize.brentq(lambda c: integrate.quad(lambda x: c * x, 45, 50)[0] - 65, 1e-4, 10))

# ---------------------------------------------------------------- Problems
v.check("22-10.1a", 1e6 / 54)
v.check("22-10.1b", 1e6 / 800)
v.check("22-10.1c", (800 / 54) ** 2)
v.check("22-10.2a", bar_loss_discrete(1000, 100e-6, lambda u: np.ones_like(u)))
v.check("22-10.2b", bar_loss_discrete(1000, 100e-6, lambda u: 1 - u))
v.check("22-10.2c", bar_loss_discrete(1000, 100e-6, lambda u: (u < 0.5).astype(float)))
v.check("22-10.3a", per_conductor_sampled(800, 480, 3, 0.95))
v.check("22-10.3b", per_conductor_sampled(800, 480, 4, 0.95))
e48 = 1 / chain_input(1.0, [0.975, 0.98, 0.90])
e800 = 1 / chain_input(1.0, [0.985, 0.975, 0.90])
v.check("22-10.4a", 100 * e48)
v.check("22-10.4b", 100 * e800)
v.check("22-10.4c", 1 / e48)
v.check("22-10.4d", 1 / e800)
v.check("22-10.4e", (1 / e48 - 1 / e800) * 1e3)
s6, one5 = summed_ripple_time(6, 12, 1.0, 150e-9, 800e3)
s12, _ = summed_ripple_time(12, 12, 1.0, 150e-9, 800e3)
v.check("22-10.5a", 1.0 / 12)
v.check("22-10.5b", one5)
v.check("22-10.5c", s6)
v.check("22-10.5d", round(s12, 6))
n6 = next(n for n in range(1, 100) if n * 0.8 * 70 >= 1200)
v.check("22-10.6a", n6)
v.check("22-10.6b", 1200 / n6)
rll7 = 0.08 / 600
v.check("22-10.7a", rll7 * 1e3)
v.check("22-10.7b", 1.04 - rll7 * 300)
v.check("22-10.7c", (1.00 - (1.04 - rll7 * 600)) * 600)
L8, C8 = 3e-12, 30e-6
v.check("22-10.8a", lc_resonance(L8, C8) / 1e6)
v.check("22-10.8b", math.sqrt(L8 / C8) * 1e6)
v.check("22-10.8c", droop(L8, C8, 150, 0.0)[0] * 1e3)
# solve in picohenries: brentq's default absolute xtol (2e-12) would swamp an answer in henries
v.check("22-10.8d", optimize.brentq(lambda lp: droop(lp * 1e-12, C8, 150, 0.0)[0] - 0.030, 0.2, 3.0))
v.check("22-10.9a", 0.5 * L6 * 100 ** 2 * 1e9)
v.check("22-10.9b", 0.5 * C6 * d0 ** 2 * 1e9)
rl10 = plane_loop(30e-3, 40e-3, 35e-6, 6)
v.check("22-10.10a", RHO / 35e-6 * 1e3)
v.check("22-10.10b", RHO * 30e-3 / (40e-3 * 35e-6) * 1e3)
v.check("22-10.10c", rl10 * 1e3)
v.check("22-10.10d", 800 ** 2 * rl10)
v.check("22-10.10e", 800 ** 2 * rl10 / 10)
v.check("22-10.11a", 50 / 40)
v.check("22-10.11b", (50 - 40) / 40)
v.check("22-10.11c", 50 / 40 - 1.09)
v.check("22-10.11d", (50 / 40 - 1.09) * 40)
e12 = integrate.quad(lambda t: 0.60 * 1200, 0, 0.020)[0]
v.check("22-10.12a", e12)
v.check("22-10.12b", optimize.brentq(lambda c: integrate.quad(lambda x: c * x, 48, 54)[0] - e12, 1e-5, 10))
zt13 = 0.03 * 0.75 / 400
v.check("22-10.13a", zt13 * 1e6)
v.check("22-10.13b", next(n for n in range(1, 1000) if 2e-3 / n <= zt13))

# ---------------------------------------------------------------- text values derived from sourced figures
v.check("Txt 22-10.f", 100 * 1089 / 1252)                      # Intel model, 1 kW GPU: MBVR out / in
v.check("Txt 22-10.g", 1.1e-3 * 280)                           # 12th-gen desktop: 1.1 mohm at 280 A
v.check("Txt 22-10.h", 1e-9 * 20e9)                            # 1 nH x 20 A/ns
v.check("Txt 22-10.i", 2400 / 600)                             # A per mm^2
v.check("Txt 22-10.j", 1342 / (0.25 * 4 * 25.4 ** 2))          # CDA 1/4 x 4 in bar
v.check("Txt 22-10.k", 100 * 826 / 1252)                       # Intel model, useful / MBVR input, 1 kW
v.check("Txt 22-10.l", 100 * 3472 / 8301)                      # Intel model, 5 kW
v.check("Txt 22-10.m", 280 / (10 * 9))                         # Infineon TDM2454xx: 280 A over 10 x 9 mm

# ---------------------------------------------------------------- Problem 22-10.14
def pickup(nph, l=120e-9, step=600.0):
    """Integrate the phase currents (all on) against a stepped load; return slew, pick-up time and deficit charge."""
    slew = nph * (12 - 0.75) / l
    tt = np.linspace(0, 2e-6, 200001)
    i_reg = np.minimum(slew * tt, step)
    t_up = tt[np.argmax(i_reg >= step)]
    deficit = integrate.trapezoid(step - i_reg, tt)
    return slew, t_up, deficit


s16, t16, q16 = pickup(16)
v.check("22-10.14a", s16 / 1e6)
v.check("22-10.14b", t16 * 1e6)
v.check("22-10.14c", q16 * 1e6)
v.check("22-10.14d", q16 / 0.03 * 1e3)
_, t8, q8 = pickup(8)
v.check("22-10.14e", t8 * 1e6)
v.check("22-10.14f", q8 / 0.03 * 1e3)

v.finish()
