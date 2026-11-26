#!/usr/bin/env python3
"""Verify every number in chapter 25-08 (thermal engineering), its problems and lab.

Independent routes (the lab module thermal.py uses closed forms and a finite-volume solver):
- hotspot centre rise by numerically superposing point sources; average rise from the Bessel integral
  int J1(x)^2/x^2 dx evaluated by quadrature;
- spreading through a lid by the exact Fourier-Bessel series (isothermal base, adiabatic sides);
- fin efficiency by shooting on the fin ODE with solve_ivp;
- power limits and inlet temperatures by root-finding; Arrhenius-equivalent temperature by bisection on
  the damage balance.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, special

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "25-08-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("25-08", ROOT / "chapters" / "25-08-thermal-engineering.md",
                        ROOT / "solutions" / "25-08-solutions.md", LAB / "README.md")

KB = 8.617333262e-5
RHO_CP_AIR = 1.2 * 1005
RHO_CP_W = 1000 * 4180
CFM = 4.719474e-4


def centre_rise(q_total, a, k):
    q = q_total / (math.pi * a * a)
    # ring at radius r contributes q 2 pi r dr / (2 pi k r)
    return integrate.quad(lambda r: q * 2 * math.pi * r / (2 * math.pi * k * r), 0, a)[0]


J12 = integrate.quad(lambda x: special.j1(x) ** 2 / x**2, 0, 200, limit=2000)[0] + \
    integrate.quad(lambda x: special.j1(x) ** 2 / x**2, 200, np.inf, limit=2000)[0]


def r_avg(a, k):
    return 2 * J12 / (math.pi * k * a)  # Delta T_avg = (2 q a / k) J12 with q = 1/(pi a^2)


def series_r(a, b, t, k, n=3000):
    q = 1 / (math.pi * a * a)
    total = q * a * a / (b * b) / k * t
    for lam in special.jn_zeros(1, n) / b:
        coeff = (q * a * special.j1(lam * a) / lam) / (b * b * special.j0(lam * b) ** 2 / 2) / (k * lam)
        total += coeff * math.tanh(lam * t) * 2 * special.j1(lam * a) / (lam * a)
    return total


def fin_eta(h, k, tf, length):
    m2 = 2 * h / (k * tf)

    def tip_slope(s0):
        sol = integrate.solve_ivp(lambda x, y: [y[1], m2 * y[0]], (0, length), [1.0, s0], rtol=1e-11, atol=1e-13)
        return sol.y[1, -1]

    s0 = optimize.brentq(tip_slope, -1e4, 0)
    return -k * tf * s0 / (2 * h * length)  # base heat over ideal, per unit theta_b and depth


def tj(p, t_in, lpm, r):
    return t_in + p / (RHO_CP_W * lpm / 6e4) / 2 + p * r


def t_eq(temps, w, ea):
    tk = np.array(temps) + 273.15
    dmg = float(np.sum(np.array(w) * np.exp(-ea / (KB * tk))))
    return optimize.bisect(lambda tc: math.exp(-ea / (KB * (tc + 273.15))) - dmg, -40, 125, xtol=1e-10)


# ---------------------------------------------------------------- Example 1
A = 800e-6
r_si, r_tim, r_lid = 0.775e-3 / (150 * A), 25e-6 / (5 * A), 2e-3 / (400 * A)
v.check("Ex 25-08.1a", r_si)
v.check("Ex 25-08.1a1", r_tim)
v.check("Ex 25-08.1a2", r_lid)
v.check("Ex 25-08.1b", r_si + r_tim + r_lid)
v.check("Ex 25-08.1c", 1000 * (r_si + r_tim + r_lid))
v.check("Ex 25-08.1d", 0.775e-3 / 25e-6)
v.check("Ex 25-08.1d1", 150 / 5)

# ---------------------------------------------------------------- Example 2
v.assert_true("Bessel integral equals 4/(3 pi)", abs(J12 - 4 / (3 * math.pi)) < 1e-6)
v.check("Ex 25-08.2a", 2 / (math.pi * 0.5**2))
v.check("Ex 25-08.2a0", 1000 / 800)
v.check("Ex 25-08.2a2", 2 / (math.pi * 0.25) + 1.25)
v.check("Ex 25-08.2a1", (2 / (math.pi * 0.25) + 1.25) / 1.25)
v.check("Ex 25-08.2b", centre_rise(2, 0.5e-3, 150))
v.check("Ex 25-08.2c", r_avg(0.5e-3, 150))
v.check("Ex 25-08.2d", 2 * r_avg(0.5e-3, 150))

# ---------------------------------------------------------------- Example 3
a3, b3, t3, k3 = 16e-3, 35e-3, 3e-3, 400
r_fp, r_full = t3 / (k3 * math.pi * a3**2), t3 / (k3 * math.pi * b3**2)
r45 = integrate.quad(lambda z: 1 / (k3 * math.pi * (a3 + z) ** 2), 0, t3)[0]
r_ex = series_r(a3, b3, t3, k3)
v.check("Ex 25-08.3a", 1e3 * r_fp)
v.check("Ex 25-08.3b", 1e3 * r_full)
v.check("Ex 25-08.3c", 1e3 * r45)
v.check("Ex 25-08.3d", 1e3 * r_ex)
v.check("Ex 25-08.3e", 100 * (r45 - r_ex) / r_ex)
v.check("Ex 25-08.3f", 100 * (r_fp - r_ex) / r_ex)
v.check("Ex 25-08.3g", 100 * (r_full - r_ex) / r_ex)
v.check("Ex 25-08.3h", 1000 * r_ex)

# ---------------------------------------------------------------- Example 4
m = math.sqrt(2 * 50 / (200 * 1e-3))
eta = fin_eta(50, 200, 1e-3, 0.040)
v.check("Ex 25-08.4a", m)
v.check("Ex 25-08.4b", m * 0.040)
v.check("Ex 25-08.4c", eta)
v.check("Ex 25-08.4d0", 50 * 2 * 0.040 * 0.100)
r_sink = 1 / (50 * eta * 0.40)
v.check("Ex 25-08.4d", r_sink)
v.check("Ex 25-08.4e", 35 + 1000 * (r_si + r_tim + r_lid) + 1000 * r_sink)
v.check("Ex 25-08.4f", (95 - 35 - 1000 * (r_si + r_tim + r_lid)) / 1000)

# ---------------------------------------------------------------- Example 5
v.check("Ex 25-08.5a", RHO_CP_W / RHO_CP_AIR)
v.check("Ex 25-08.5b", 1000 / (RHO_CP_AIR * 15))
v.check("Ex 25-08.5b1", 1000 / (RHO_CP_AIR * 15) / CFM)
v.check("Ex 25-08.5c0", 1000 / (RHO_CP_W * 10))
v.check("Ex 25-08.5c", 1000 / (RHO_CP_W * 10) * 6e4)
v.check("Ex 25-08.5d0", 120e3 / (RHO_CP_AIR * 15))
v.check("Ex 25-08.5d", 120e3 / (RHO_CP_AIR * 15) / CFM)

# ---------------------------------------------------------------- Example 6
g2 = RHO_CP_W * 2 / 6e4
v.check("Ex 25-08.6a0", g2)
v.check("Ex 25-08.6a", 1400 / g2)
v.check("Ex 25-08.6b", tj(1400, 45, 2, 0.035))
v.check("Ex 25-08.6c", 2300 / g2)
v.check("Ex 25-08.6c0", 2300 / g2 / 2)
v.check("Ex 25-08.6d", tj(2300, 45, 2, 0.035))
v.check("Ex 25-08.6e", optimize.brentq(lambda r: tj(2300, 45, 2, r) - 105, 1e-4, 1))

# ---------------------------------------------------------------- Example 7
v.check("Ex 25-08.7a", 0.9 * 135)
v.check("Ex 25-08.7b", 0.1 * 135)
v.check("Ex 25-08.7c", 121.5e3 / (RHO_CP_W * 10) * 6e4)
v.check("Ex 25-08.7d0", 13.5e3 / (RHO_CP_AIR * 15))
v.check("Ex 25-08.7d", 13.5e3 / (RHO_CP_AIR * 15) / CFM)

# ---------------------------------------------------------------- Example 8
prof_t, prof_w = [-40, 70, 110, 125], [0.05, 0.65, 0.20, 0.10]
mean = float(np.dot(prof_t, prof_w))
teq = t_eq(prof_t, prof_w, 0.7)
d = np.array(prof_w) * np.exp(-0.7 / (KB * (np.array(prof_t) + 273.15)))
v.check("Ex 25-08.8a", mean)
v.check("Ex 25-08.8b", teq)
v.check("Ex 25-08.8c", 100 * d[3] / d.sum())
v.check("Ex 25-08.8d", 100 * (d[2] + d[3]) / d.sum())
v.check("Ex 25-08.8e", 100_000 / 20_000)
v.check("Ex 25-08.8f", teq - mean)
v.check("Txt 25-08.b", 10e6 / 9216 / 1e3)

# ---------------------------------------------------------------- Problems
v.check("25-08.1a", 100e-6 / (80 * A))
v.check("25-08.1b", r_tim / (100e-6 / (80 * A)))
v.check("25-08.2a", 2 / math.pi)
v.check("25-08.2a1", centre_rise(2, 1e-3, 150))
v.check("25-08.2a2", r_avg(1e-3, 150))
p_b = 2 / (math.pi * 0.25) * math.pi * 1.0
v.check("25-08.2b", p_b)
v.check("25-08.2b1", centre_rise(p_b, 1e-3, 150))
r_fp5 = 3e-3 / (400 * math.pi * 0.005**2)
r45_5 = integrate.quad(lambda z: 1 / (400 * math.pi * (0.005 + z) ** 2), 0, 3e-3)[0]
r_ex5 = series_r(0.005, 0.035, 3e-3, 400)
v.check("25-08.3a", 1e3 * r_fp5)
v.check("25-08.3b", 1e3 * r45_5)
v.check("25-08.3c", 1e3 * r_ex5)
v.check("25-08.3d", 100 * (r45_5 - r_ex5) / r_ex5)
mc = math.sqrt(2 * 50 / (400 * 1e-3))
eta_cu = fin_eta(50, 400, 1e-3, 0.040)
eta_80 = fin_eta(50, 200, 1e-3, 0.080)
v.check("25-08.4b0", mc)
v.check("25-08.4b1", mc * 0.040)
v.check("25-08.4b", eta_cu)
v.check("25-08.4c0", m * 0.080)
v.check("25-08.4c", eta_80)
v.check("25-08.4c1", 2 * eta_80 / eta)
v.check("25-08.5a", 2400 / (RHO_CP_AIR * 20))
v.check("25-08.5b", 2400 / (RHO_CP_AIR * 20) / CFM)
p2 = optimize.brentq(lambda p: tj(p, 45, 2, 0.035) - 105, 1, 1e5)
p4 = optimize.brentq(lambda p: tj(p, 45, 4, 0.035) - 105, 1, 1e5)
v.check("25-08.6a", p2)
v.check("25-08.6a0", RHO_CP_W * 4 / 6e4)
v.check("25-08.6b", p4)
v.check("25-08.6c", 100 * (p4 / p2 - 1))
v.check("25-08.7a", tj(2300, 30, 2, 0.035))
v.check("25-08.7b", optimize.brentq(lambda ti: tj(2300, ti, 2, 0.035) - 105, -50, 100))
v.check("25-08.8a", 72 * 2.5)
v.check("25-08.8b", 180e3 / (RHO_CP_W * 10) * 6e4)
v.check("25-08.9a", 10e6 / 9216 / 1e3)
v.check("25-08.9b", 192 * 9216 / 1e6)
v.check("25-08.9c", 4614 * 9216 / 1e6)
v.check("25-08.10a", 100 * (125 / 90 - 1))
v.check("25-08.10a1", 100 * (136 / 101 - 1))
v.check("25-08.10b", 10_000 // 136)
v.check("25-08.10b1", 10_000 // 101)
v.check("25-08.11a", t_eq(prof_t, prof_w, 1.0))
v.check("25-08.11b", t_eq(prof_t, prof_w, 0.4))
v.check("25-08.12a", 100 * (1.10 / 1.20 - 1))
v.check("25-08.13a", 100 / 2.26e6)
v.check("25-08.13a1", 100 / 2.26e6 * 1e6)
v.check("25-08.13b", 2.26e6 / (4180 * 10))

# ---------------------------------------------------------------- Lab
for key, t in (("a", 1e-3), ("a1", 10e-3)):
    ex = series_r(a3, b3, t, k3)
    v.check(f"Lab 25-08.{key}", 100 * (t / (k3 * math.pi * a3 * (a3 + t)) - ex) / ex)
v.check("Lab 25-08.b", eta_cu)
v.check("Lab 25-08.c", p2)
v.check("Lab 25-08.d", t_eq(prof_t, prof_w, 1.0))

# ---------------------------------------------------------------- lab solvers asserted (finite volume, fin ODE)
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("thermal", LAB / "thermal.py")
thermal = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(thermal)
r_fd = thermal.spreader_fd(0.016, 0.035, 3e-3, 400)
r_fd2 = thermal.spreader_fd(0.016, 0.035, 3e-3, 400, nr=320, nz=96)
v.assert_true("Ex 25-08.3d: finite-volume spreading resistance agrees with the series within 0.5%", abs(r_fd / r_ex - 1) < 5e-3,
              f"{r_fd * 1e3:.4f} vs {r_ex * 1e3:.4f} mK/W")
v.assert_true("finite-volume result changes by under 0.2% when the grid is doubled", abs(r_fd2 / r_fd - 1) < 2e-3)
for h_, kf, tf, Lf in ((60, 200, 0.8e-3, 0.030), (5265, 400, 3e-4, 2e-3)):
    v.assert_true(f"fin ODE matches tanh(mL)/mL within 0.1% (h={h_})",
                  abs(thermal.fin_efficiency_ode(h_, kf, tf, Lf) / fin_eta(h_, kf, tf, Lf) - 1) < 1e-3)

# ---------------------------------------------------------------- Example 9 and Problem 14: microchannels
rho_w, mu_w, kf_w, cp_w = 1000.0, 0.65e-3, 0.63, 4180.0


def channels(n, w, d=2e-3, length=0.040, flow=2.0 / 60_000):
    ac, pw = w * d, 2 * (w + d)
    dh = 4 * ac / pw
    vel = flow / n / ac
    re = rho_w * vel * dh / mu_w
    h_ = 4.36 * kf_w / dh
    area = n * pw * length
    dp = 32 * mu_w * length * vel / dh**2          # Hagen-Poiseuille form of f = 64/Re
    return dh, vel, re, h_, area, 1 / (h_ * area), dp, dp * flow


dh9, v9, re9, h9, a9, r9, dp9, pp9 = channels(100, 0.3e-3)
v.check("Ex 25-08.9a", dh9 * 1e3)
v.check("Ex 25-08.9b", v9)
v.check("Ex 25-08.9b1", re9)
v.check("Ex 25-08.9c", h9)
v.check("Ex 25-08.9d", a9)
v.check("Ex 25-08.9d1", r9)
v.check("Ex 25-08.9e", dp9 / 1e3)
v.check("Ex 25-08.9e1", pp9)
v.assert_true("Hagen-Poiseuille drop equals f(L/D)(rho v^2/2) with f = 64/Re",
              abs(dp9 / ((64 / re9) * (0.040 / dh9) * rho_w * v9**2 / 2) - 1) < 1e-12)
eta9 = thermal.fin_efficiency_ode(h9, 400, 3e-4, 2e-3)
v.check("Ex 25-08.9f", math.sqrt(2 * h9 / (400 * 3e-4)) * 2e-3)
v.check("Ex 25-08.9f1", eta9)
v.check("Ex 25-08.9f2", 1 / (h9 * 100 * 0.040 * (2 * 0.3e-3 + 2 * 2e-3 * eta9)))
pr9 = mu_w * cp_w / kf_w
v.check("Ex 25-08.9g", pr9)
v.check("Ex 25-08.9g1", 0.05 * re9 * pr9 * dh9 * 100)
d14 = channels(200, 0.15e-3)
for key, val in zip(("a", "b", "b1", "c", "d", "d1", "e", "e1"),
                    (d14[0] * 1e3, d14[1], d14[2], d14[3], d14[4], d14[5], d14[6] / 1e3, d14[7])):
    v.check(f"25-08.14{key}", val)
v.check("25-08.14f", d14[3] / h9)
v.check("25-08.14f1", r9 / d14[5])
v.check("25-08.14f2", d14[6] / dp9)

sys.exit(v.finish())
