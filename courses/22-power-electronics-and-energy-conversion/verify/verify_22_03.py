#!/usr/bin/env python3
"""Verify every number in chapter 22-03 (boost, buck-boost and other topologies), its problems and its lab.

Independent routes (the lab module topologies.py uses closed forms and a linear solve):
- boost ripples, currents and efficiency come from the periodic steady state of the switched ODEs, found by
  Newton iteration (fsolve) on the one-period map integrated with solve_ivp, with energy integrals for losses;
- the gain peak is found by numerical maximization of the resistive boost's steady state;
- boost DCM operating points come from simulating one period piecewise with an event at zero current and
  root-finding the repeating output voltage;
- the SEPIC's averaged model is checked against its own switched four-state periodic steady state.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "22-03-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("22-03", ROOT / "chapters" / "22-03-boost-buck-boost-topologies.md",
                        ROOT / "solutions" / "22-03-solutions.md", LAB / "README.md")
TOL = dict(rtol=1e-11, atol=1e-13)


def boost_pss(v_in, d, fs, ind, cap, r, r_l=0.0, r_ls=0.0, r_hs=0.0, pts=4000):
    """Synchronous boost PSS by Newton on the one-period map; returns waveforms and energy-based powers."""
    t_s = 1 / fs
    on = lambda t, y: [(v_in - y[0] * (r_l + r_ls)) / ind, -y[1] / (r * cap), v_in * y[0]]  # noqa: E731
    off = lambda t, y: [(v_in - y[0] * (r_l + r_hs) - y[1]) / ind, (y[0] - y[1] / r) / cap, v_in * y[0]]  # noqa: E731

    def period(x):
        a = integrate.solve_ivp(on, (0, d * t_s), [x[0], x[1], 0.0], **TOL)
        b = integrate.solve_ivp(off, (0, (1 - d) * t_s), a.y[:, -1], **TOL)
        return b.y[:, -1]

    x0 = optimize.fsolve(lambda x: period(x)[:2] - x, [v_in / (1 - d) / ((1 - d) * r), v_in / (1 - d)], xtol=1e-13)
    t1 = np.linspace(0, d * t_s, pts)
    t2 = np.linspace(0, (1 - d) * t_s, pts)
    a = integrate.solve_ivp(on, (0, d * t_s), [x0[0], x0[1], 0.0], t_eval=t1, **TOL)
    b = integrate.solve_ivp(off, (0, (1 - d) * t_s), a.y[:, -1], t_eval=t2, **TOL)
    il = np.concatenate([a.y[0], b.y[0]])
    vo = np.concatenate([a.y[1], b.y[1]])
    tt = np.concatenate([t1, d * t_s + t2])
    p_in = b.y[2, -1] / t_s
    p_out = np.trapezoid(vo * vo / r, tt) / t_s
    return {"di": il.max() - il.min(), "dv": vo.max() - vo.min(), "il": np.trapezoid(il, tt) / t_s,
            "vo": np.trapezoid(vo, tt) / t_s, "p_in": p_in, "p_out": p_out}


def boost_dcm_v(v_in, d, fs, ind, r, cap=0.1):
    """Diode boost in DCM, small-ripple limit (large C): root-find the repeating output voltage."""
    t_s = 1 / fs

    def period(vo):
        ipk = v_in * d * t_s / ind
        vc = vo * math.exp(-d * t_s / (r * cap))
        ev = lambda t, y: y[0]  # noqa: E731
        ev.terminal = True
        ev.direction = -1
        s = integrate.solve_ivp(lambda t, y: [(v_in - y[1]) / ind, (y[0] - y[1] / r) / cap], (0, (1 - d) * t_s),
                                [ipk, vc], events=ev, **TOL)
        t2 = s.t[-1]
        return s.y[1, -1] * math.exp(-((1 - d) * t_s - t2) / (r * cap))

    return optimize.brentq(lambda x: period(x) - x, v_in * 1.0001, v_in * 50, xtol=1e-12)


def sepic_pss(v_in, d, fs, l1, l2, c1, cout, r, r1, r2):
    t_s = 1 / fs
    on = lambda t, y: [(v_in - y[0] * r1) / l1, (y[2] - y[1] * r2) / l2, -y[1] / c1, -y[3] / (r * cout)]  # noqa: E731
    off = lambda t, y: [(v_in - y[0] * r1 - y[3] - y[2]) / l1, (-y[3] - y[1] * r2) / l2, y[0] / c1,  # noqa: E731
                        (y[0] + y[1] - y[3] / r) / cout]

    def period(x):
        a = integrate.solve_ivp(on, (0, d * t_s), x, **TOL)
        b = integrate.solve_ivp(off, (0, (1 - d) * t_s), a.y[:, -1], **TOL)
        return b.y[:, -1]

    x0 = optimize.fsolve(lambda x: period(x) - x, [2.0, 2.0, v_in, v_in * d / (1 - d)], xtol=1e-13)
    t1 = np.linspace(0, d * t_s, 2000)
    t2 = np.linspace(0, (1 - d) * t_s, 2000)
    a = integrate.solve_ivp(on, (0, d * t_s), x0, t_eval=t1, **TOL)
    b = integrate.solve_ivp(off, (0, (1 - d) * t_s), a.y[:, -1], t_eval=t2, **TOL)
    tt = np.concatenate([t1, d * t_s + t2])
    vo = np.concatenate([a.y[3], b.y[3]])
    vc = np.concatenate([a.y[2], b.y[2]])
    return np.trapezoid(vo, tt) / t_s, np.trapezoid(vc, tt) / t_s


def m_rl(dd, r_l, r):
    """Boost gain with winding resistance from its steady state (solve the DC equations numerically)."""
    dp = 1 - dd
    # unknowns V, I_L: Vin - I_L r_l = D' V ; I_L = V/(D' R)  (Vin = 1)
    a = np.array([[dp, r_l], [-1 / (dp * r), 1.0]])
    return np.linalg.solve(a, [1.0, 0.0])[0]


# ---------------------------------------------------------------- Example 22-03.1
print("Example 22-03.1")
VIN, V, I, FS, L, C = 3.6, 5.0, 1.5, 1e6, 1e-6, 22e-6
D = optimize.brentq(lambda dd: VIN / (1 - dd) - V, 0, 0.99)
s1 = boost_pss(VIN, D, FS, L, C, V / I)
v.check("Ex 22-03.1a", D)
v.check("Ex 22-03.1b", s1["il"])
v.check("Ex 22-03.1c", s1["di"])
v.check("Ex 22-03.1d", s1["il"] + s1["di"] / 2)
v.check("Ex 22-03.1e", s1["il"] - s1["di"] / 2)
v.check("Ex 22-03.1f", s1["dv"] * 1e3)
# capacitor RMS: on-time -I, off-time I_L - I (small ripple), integrated
v.check("Ex 22-03.1g", math.sqrt(D * I * I + (1 - D) * (I / (1 - D) - I) ** 2))
fz = (1 - D) ** 2 * (V / I) / L / (2 * math.pi)
v.check("Ex 22-03.1h", fz / 1e3)
v.check("Ex 22-03.1i", fz / 5 / 1e3)

# ---------------------------------------------------------------- Example 22-03.2
print("Example 22-03.2")
d2 = optimize.brentq(lambda dd: boost_pss(VIN, dd, FS, L, 1e-3, V / I, 0.030, 0.047, 0.068)["vo"] - V, 0.28, 0.4,
                     xtol=1e-9)
s2 = boost_pss(VIN, d2, FS, L, 1e-3, V / I, 0.030, 0.047, 0.068)
v.check("Ex 22-03.2a", d2)
# the example's small-ripple DC model, solved as a linear system in (V, I_L) at each trial duty cycle
def dc_boost(dd, rl=0.030, rls=0.047, rhs=0.068):
    dp = 1 - dd
    req = rl + dd * rls + dp * rhs
    return np.linalg.solve(np.array([[dp, req], [-1 / (dp * (V / I)), 1.0]]), [VIN, 0.0])


d2dc = optimize.brentq(lambda dd: dc_boost(dd)[0] - V, 0.28, 0.4, xtol=1e-13)
il2 = dc_boost(d2dc)[1]
v.assert_true("DC-model and exact duty cycles agree to 1e-4", abs(d2dc - d2) < 1e-4)
v.check("Ex 22-03.2b", il2)
v.check("Ex 22-03.2c", VIN * il2 - V * I)
v.check("Ex 22-03.2d", V * I / (VIN * il2) * 100)
v.check("Ex 22-03.2e", s2["p_out"] / s2["p_in"] * 100)

# ---------------------------------------------------------------- Example 22-03.3
print("Example 22-03.3")
res = optimize.minimize_scalar(lambda dd: -m_rl(dd, 0.1, 25.0), bounds=(0.5, 0.999), method="bounded",
                               options={"xatol": 1e-12})
v.check("Ex 22-03.3a", res.x)
v.check("Ex 22-03.3b", -res.fun)
v.check("Ex 22-03.3c", -res.fun * (1 - res.x) * 100)   # eta = D' V / Vin
for key_m, key_e, dd in (("d", "e", 0.8), ("f", "g", 0.9)):
    m = m_rl(dd, 0.1, 25.0)
    v.check(f"Ex 22-03.3{key_m}", m)
    v.check(f"Ex 22-03.3{key_e}", m * (1 - dd) * 100)
v.check("Ex 22-03.3h", 100 - m_rl(0.9, 0.1, 25.0) * 0.1 * 100)

# ---------------------------------------------------------------- Example 22-03.4
print("Example 22-03.4")
d4 = optimize.brentq(lambda dd: dd / (1 - dd) * 12 - 5, 0, 0.99)
v.check("Ex 22-03.4a", d4)
v.check("Ex 22-03.4b", 12 + 5)
v.check("Ex 22-03.4c", 1 / (1 - d4))
for key_d, key_v, vin in (("d", "f", 9.0), ("e", "g", 16.0)):
    dd = optimize.brentq(lambda x, vin=vin: x / (1 - x) * vin - 12, 0, 0.99)
    v.check(f"Ex 22-03.4{key_d}", dd)
    v.check(f"Ex 22-03.4{key_v}", vin + 12)

# ---------------------------------------------------------------- Example 22-03.5
print("Example 22-03.5")
K5 = 2 * L * FS / 100
v.check("Ex 22-03.5a", K5)
v.check("Ex 22-03.5b", D * (1 - D) ** 2)
v.check("Ex 22-03.5c", boost_dcm_v(VIN, D, FS, L, 100))
v.check("Ex 22-03.5d", optimize.brentq(lambda dd: boost_dcm_v(VIN, dd, FS, L, 100) - 5.0, 0.02, 0.2, xtol=1e-12))

# ---------------------------------------------------------------- Example 22-03.6
print("Example 22-03.6")
v.check("Ex 22-03.6a", 24 * 1 / 12)
v.check("Ex 22-03.6b", 12 * (1 / 0.5) / 12)
v.check("Ex 22-03.6c", 24 * (1 / 0.5) / 12)

# ---------------------------------------------------------------- Example 22-03.7
print("Example 22-03.7")
v.check("Ex 22-03.7a", 1 - 230 * math.sqrt(2) / 400)
v.check("Ex 22-03.7b", 1 - 277 * math.sqrt(2) / 400)
v.check("Ex 22-03.7c", 1 - 1e-9 / 400)

# ---------------------------------------------------------------- problems
print("Problems")
d = optimize.brentq(lambda x: 5 / (1 - x) - 12, 0, 0.99)
v.check("22-03.1a", d)
v.check("22-03.1b", 0.5 / (1 - d))
v.check("22-03.1c", 12)
d = optimize.brentq(lambda x: x / (1 - x) * 5 - 15, 0, 0.99)
v.check("22-03.2a", d)
v.check("22-03.2b", 20)
v.check("22-03.2c", 0.1 / (1 - d))
d = optimize.brentq(lambda x: x / (1 - x) * 24 - 12, 0, 0.99)
v.check("22-03.3a", d)
v.check("22-03.3b", 36)
s4 = boost_pss(12.0, 0.75, 250e3, 33e-6, 47e-6, 24.0)
v.check("22-03.4a", 0.75)
v.check("22-03.4b", s4["il"])
v.check("22-03.4c", s4["di"])
v.check("22-03.4d", s4["dv"])
v.check("22-03.4e", 2 * math.sqrt(0.75 / 0.25))
d5 = optimize.brentq(lambda x: m_rl(x, 0.02, 24.0) * 12 - 48, 0.5, 0.9)
v.check("22-03.5a", 1 - d5)
v.check("22-03.5b", d5)
v.check("22-03.5c", 48 * (1 - d5) / 12 * 100)
v.check("22-03.5d", 2 / (1 - d5))
v.check("22-03.5e", -optimize.minimize_scalar(lambda x: -m_rl(x, 0.02, 24.0), bounds=(0.5, 0.9999),
                                              method="bounded", options={"xatol": 1e-12}).fun)
r6 = optimize.minimize_scalar(lambda x: -m_rl(x, 0.05, 20.0), bounds=(0.5, 0.9999), method="bounded",
                              options={"xatol": 1e-12})
v.check("22-03.6a", 1 - r6.x)
v.check("22-03.6b", -r6.fun)
d6 = optimize.brentq(lambda x: m_rl(x, 0.05, 20.0) - 5, 0.5, r6.x)
v.check("22-03.6c", 1 - d6)
v.check("22-03.6d", d6)
v.check("22-03.6e", 5 * (1 - d6) * 100)
v.check("22-03.7a", 0.5 * 0.25)
v.check("22-03.7b", optimize.brentq(lambda ll: 2 * ll * 200e3 / 240 - 0.125, 1e-7, 1e-2) * 1e6)
v.check("22-03.8a", boost_dcm_v(1.0, 0.3, 1.0, 0.01, 1.0, cap=1e5))   # K = 2 L f / R = 0.02
v.check("22-03.9a", 3.3 / 4.2)
v.check("22-03.9b", 1 - 3.0 / 3.3)
v.check("22-03.9c", 3.3)
v.check("22-03.10a", 12 / 5)
d10 = optimize.brentq(lambda x: x / (1 - x) * 5 - 12, 0, 0.99)
v.check("22-03.10b", 17 / (12 * (1 - d10)))
v.check("22-03.10c", d10)
for key_f, key_c, r in (("a", "c", 12.0), ("b", "d", 8.0)):
    f = 0.25 * r / (2 * math.pi * 22e-6)
    v.check(f"22-03.11{key_f}", f / 1e3)
    v.check(f"22-03.11{key_c}", f / 5 / 1e3)
vp = 90 * math.sqrt(2)
v.check("22-03.12a", vp)
v.check("22-03.12b", 1 - vp / 400)
v.check("22-03.12c", math.sqrt(2) * 500 / 90)
ic = lambda dd: math.sqrt(dd * 1.0 + (1 - dd) * (1 / (1 - dd) - 1) ** 2)  # noqa: E731
v.check("22-03.13a", ic(0.75))

# ---------------------------------------------------------------- lab
print("Lab")
sys.path.insert(0, str(LAB))
import topologies as tp  # noqa: E402

vo_pss, vc_pss = sepic_pss(12.0, 0.5, 300e3, 47e-6, 47e-6, 10e-6, 47e-6, 6.0, 0.05, 0.05)
v.check("Lab 22-03.a", vo_pss)
v.check("Lab 22-03.b", vc_pss)
sol = tp.sepic_dc(12.0, 0.5, 6.0, 0.05, 0.05)
v.assert_true("averaged SEPIC model matches its switched steady state", abs(sol[0] - vo_pss) < 5e-3)
v.assert_true("lab boost max gain equals the numerical maximum", abs(tp.boost_max_gain(0.1, 25)[0] + res.fun) < 1e-8)

# ---------------------------------------------------------------- Problem 22-03.14 (buck-boost DCM)
k14 = 2 * 10e-6 * 200e3 / 48
v.check("22-03.14a", k14)


def bb_dcm_iout(d, vin=12.0, vo=12.0, ind=10e-6, fs=200e3):
    """Average diode current of one DCM buck-boost cycle with the output held at -vo."""
    ipk = vin * d / fs / ind
    t_off = ipk * ind / vo
    v.assert_true("buck-boost cycle is discontinuous", d / fs + t_off < 1 / fs) if d > 0.28 and d < 0.3 else None
    return 0.5 * ipk * t_off * fs


v.check("22-03.14b", optimize.brentq(lambda d: bb_dcm_iout(d) - 12 / 48, 0.05, 0.6))

# ---------------------------------------------------------------- Problem 22-03.15 (SEPIC waveforms, ideal parts)
def sepic_wave(v_in, d, fs, l1, l2, c1, cout, r, n=4000):
    t_s = 1 / fs
    on = lambda t, y: [v_in / l1, y[2] / l2, -y[1] / c1, -y[3] / (r * cout)]  # noqa: E731
    off = lambda t, y: [(v_in - y[3] - y[2]) / l1, -y[3] / l2, y[0] / c1, (y[0] + y[1] - y[3] / r) / cout]  # noqa: E731

    def period(x):
        a1 = integrate.solve_ivp(on, (0, d * t_s), x, **TOL)
        b1 = integrate.solve_ivp(off, (0, (1 - d) * t_s), a1.y[:, -1], **TOL)
        return b1.y[:, -1]

    x0 = optimize.fsolve(lambda x: period(x) - x, [2.7, 2.0, v_in, 12.0], xtol=1e-13)
    t1 = np.linspace(0, d * t_s, n)
    t2 = np.linspace(0, (1 - d) * t_s, n)
    a1 = integrate.solve_ivp(on, (0, d * t_s), x0, t_eval=t1, **TOL)
    b1 = integrate.solve_ivp(off, (0, (1 - d) * t_s), a1.y[:, -1], t_eval=t2, **TOL)
    return a1, b1, np.concatenate([t1, d * t_s + t2])


d15 = optimize.brentq(lambda d: d / (1 - d) * 9 - 12, 0.1, 0.9)
v.check("22-03.15a", d15)
on15, off15, tt15 = sepic_wave(9.0, d15, 300e3, 20e-6, 20e-6, 10e-6, 10e-3, 6.0)
il1 = np.concatenate([on15.y[0], off15.y[0]])
il2 = np.concatenate([on15.y[1], off15.y[1]])
vc1 = np.concatenate([on15.y[2], off15.y[2]])
vo15 = np.concatenate([on15.y[3], off15.y[3]])
t_s15 = 1 / 300e3
v.assert_true("22-03.15: output settles at 12 V", abs(np.trapezoid(vo15, tt15) / t_s15 - 12) < 0.02)
v.check("22-03.15b", np.trapezoid(vc1, tt15) / t_s15)
v.check("22-03.15c", np.trapezoid(il2, tt15) / t_s15)
v.check("22-03.15d", np.trapezoid(il1, tt15) / t_s15)
v.check("22-03.15e", np.ptp(vc1))
v.check("22-03.15f", np.ptp(il1))
v.assert_true("22-03.15: both inductors ripple equally", abs(np.ptp(il1) - np.ptp(il2)) < 5e-3)
v.check("22-03.15g", np.max(on15.y[0] + on15.y[1]))
v.check("22-03.15h", np.max(off15.y[2] + off15.y[3]))  # switch node off: V_C1 + V

sys.exit(v.finish())
