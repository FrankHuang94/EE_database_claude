#!/usr/bin/env python3
"""Verify every number in the Course 25 final-exam solutions.

Second routes for about half of the values (listed in the solutions' preamble):
- Q1(a, b): oxide growth by integrating dx/dt = B/(A + 2x) as an initial-value problem with a stop event;
- Q3(a, c): projected range and annealed junction by root-finding on the Gaussian profile;
- Q4(b): clustered yields by integrating Poisson yield over gamma and triangular defect densities;
- Q5(a): restoring supply by root-finding; Q5(c): burn-in times from the weak population's survival;
- Q7(b): bond yield from the normal CDF; Q7(c): escape rate by Monte Carlo;
- Q8(c): fin efficiency from the fin ODE as a boundary-value problem;
- Q9(b): E-model and power-law fits by least squares;
- Q11(a): time offset by integrating from the initial oxide; Q11(b): package scale and corner fraction by
  integrating survival and hazard; Q11(c): mean exposure by simulating arrivals; Q11(d): gamma integration;
- Q12(a): defect density by root-finding on the cost model; Q12(d): Wilson bound from the score inequality.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("25-exam", ROOT / "exam" / "solutions.md")
K = 8.617333262e-5
H, C0 = 6.626e-34, 2.998e8
RNG = np.random.default_rng(25)

# ---------------------------------------------------------------- Q1
A, B = 0.165, 0.0117


def grow_time(x_target, x0=0.0):
    """Integrate the Deal-Grove rate from x0 until the oxide reaches x_target (hours)."""
    ev = lambda t, x: x[0] - x_target  # noqa: E731
    ev.terminal = True
    sol = integrate.solve_ivp(lambda t, x: [B / (A + 2 * x[0])], (0, 1e3), [x0], events=ev,
                              rtol=1e-11, atol=1e-13)
    return sol.t_events[0][0]


def closed_time(x):
    return x * x / B + x / (B / A)


t01, t05 = grow_time(0.10), grow_time(0.50)
v.assert_true("Q1 ODE agrees with closed form", abs(t01 - closed_time(0.10)) < 1e-6 and abs(t05 - closed_time(0.50)) < 1e-6)
v.check("X25.1a", t01)
v.check("X25.1a0", B / A)
v.check("X25.1a1", t05)
v.check("X25.1a2", t05 / t01)
x_sac = 0.050 / 0.44
v.check("X25.1b", x_sac * 1e3)
v.check("X25.1b0", x_sac)
v.check("X25.1b1", grow_time(x_sac))
lam = 60000 / 30
v.check("X25.1c", 1.5e5 / lam)
v.check("X25.1c1", lam * 20)
v.check("X25.1d", 0.3787 * 24e3 * 0.4e-12 * 1e12)
v.check("X25.1d1", 0.3787 * 12e3 * 0.2e-12 * 1e12)

# ---------------------------------------------------------------- Q2
for key, lam_n, na in (("2a", 193, 1.35), ("2a1", 13.5, 0.33), ("2a2", 13.5, 0.55)):
    v.check(f"X25.{key}", lam_n / (2 * na))
v.check("X25.2b", 13.5 / 0.33**2)
v.check("X25.2b1", 13.5 / 0.55**2)
v.check("X25.2b2", (13.5 / 0.55**2) / (13.5 / 0.33**2))
e_ph = H * C0 / 13.5e-9
e_del = 300 * (20e-9) ** 2
n_ph = e_del / e_ph
v.check("X25.2c", e_ph)
v.check("X25.2c0", e_del)
v.check("X25.2c1", n_ph)
v.check("X25.2c2", 100 / math.sqrt(n_ph))
v.check("X25.2d", 3600 / 22)
v.check("X25.2d1", 3600 / 34)

# ---------------------------------------------------------------- Q3
Q, DRP, NB = 1e15, 20e-7, 1e17
NP = Q / (math.sqrt(2 * math.pi) * DRP)
v.check("X25.3a", NP)
v.check("X25.3a0", NP / NB)
# R_p by root-finding: the Gaussian must fall to NB at 150 nm
rp = optimize.brentq(lambda r: NP * math.exp(-((150e-7 - r) ** 2) / (2 * DRP**2)) - NB, 0, 150e-7)
v.check("X25.3a1", (150e-7 - rp) * 1e7)
v.check("X25.3a2", rp * 1e7)
drp2 = math.sqrt(DRP**2 + 2 * 2e-12)
np2 = Q / (math.sqrt(2 * math.pi) * drp2)
# dose conservation, checked by quadrature of the annealed profile (no surface)
dose2 = integrate.quad(lambda x: np2 * math.exp(-((x - rp) ** 2) / (2 * drp2**2)), rp - 20 * drp2, rp + 20 * drp2)[0]
v.assert_true("Q3 anneal conserves dose", abs(dose2 / Q - 1) < 1e-9)
v.check("X25.3b", drp2 * 1e7)
v.check("X25.3b0", drp2 * 1e7)
v.check("X25.3b1", np2)
v.check("X25.3b2", np2 / NB)
xj2 = optimize.brentq(lambda x: np2 * math.exp(-((x - rp) ** 2) / (2 * drp2**2)) - NB, rp, rp + 20 * drp2)
v.check("X25.3c0", (xj2 - rp) * 1e7)
v.check("X25.3c", xj2 * 1e7)
v.check("X25.3c1", (xj2 - 150e-7) * 1e7)
v.check("X25.3d", 1 / (1 / 1 + 1 / 5))
# current density: charge per area for 1.0 um of copper, divided by the time
mol_per_cm2 = 1e-4 * 8.96 / 63.55
v.check("X25.3d1", mol_per_cm2 * 2 * 96485 / 120 * 1e3)

# ---------------------------------------------------------------- Q4
dpw_raw = math.pi * 300**2 / (4 * 150) - math.pi * 300 / math.sqrt(300)
dpw = round(dpw_raw)
v.check("X25.4a0", dpw_raw)
v.check("X25.4a", dpw)
d0 = 0.15
v.check("X25.4b0", 1.5 * d0)
y_p = math.exp(-1.5 * d0)
tri = lambda d: (d / d0**2) if d <= d0 else ((2 * d0 - d) / d0**2)  # noqa: E731
y_m = integrate.quad(lambda d: math.exp(-1.5 * d) * tri(d), 0, 2 * d0, points=[d0])[0]
y_nb = integrate.quad(lambda d: math.exp(-1.5 * d) * stats.gamma.pdf(d, 2, scale=d0 / 2), 0, np.inf)[0]
v.check("X25.4b", y_p)
v.check("X25.4b3", y_p)
v.check("X25.4b1", y_m)
v.check("X25.4b2", y_nb)
v.check("X25.4c", 18000 / (dpw * y_p))
v.check("X25.4d", 18000 / (dpw * y_nb))

# ---------------------------------------------------------------- Q5
f5 = lambda vv, vth: vv / (vv - vth) ** 1.3  # noqa: E731
v.check("X25.5a", f5(0.75, 0.34) / f5(0.75, 0.30))
target = f5(0.75, 0.30)
v.check("X25.5a0", target)
v.check("X25.5a1", f5(0.80, 0.34))
v.check("X25.5a2", f5(0.85, 0.34))
v_rest = optimize.brentq(lambda vv: f5(vv, 0.34) - target, 0.76, 1.2)
v.check("X25.5a3", v_rest)
v.check("X25.5a4", (v_rest - 0.75) * 1e3)
cox, csi = 3.9 / 1.0, 11.7 / 6
c_ser = 0.075 * cox
v.check("X25.5b0", c_ser)
t_box = optimize.brentq(lambda t: (1 / (1 / csi + t / 3.9)) / cox - 0.075, 1, 100)
v.check("X25.5b1", t_box / 3.9)
v.check("X25.5b", t_box)
v.check("X25.5b2", 0.040 / 0.075)
pw, q_t, eta_w, af_b = 0.01, 50e-6, 200.0, 40.0
v.check("X25.5c0", math.log(pw / q_t))
burn = {}
for beta, k_use, k_tb in ((0.5, "X25.5c1", "X25.5c"), (1.0, "X25.5c3", "X25.5c2")):
    te = optimize.brentq(lambda t: pw * math.exp(-((t / eta_w) ** beta)) - q_t, 1, 1e6)
    burn[beta] = te / af_b
    v.check(k_use, te)
    v.check(k_tb, te / af_b)
v.check("X25.5c4", burn[0.5] / burn[1.0])

# ---------------------------------------------------------------- Q6
v.check("X25.6a", 4 * 0.11**2 / 0.045)
n_tr = 0
while (n_tr + 1) * 10 + (n_tr + 2) * 10 <= 130 - 75:
    n_tr += 1
v.check("X25.6b", n_tr)
v.check("X25.6b1", math.ceil(18 / (n_tr + 1)))
g = 13.4e-6 * 120 * 12 / 0.08
g0 = 13.4e-6 * 100 * 10 / 0.07
v.check("X25.6c", g)
v.check("X25.6c0", g0)
v.check("X25.6c1", (g0 / g) ** 2)
v.check("X25.6d", 500 ** (-1 / 5))

# ---------------------------------------------------------------- Q7
v.check("X25.7a", (1000 / 5) ** 2)
v.check("X25.7a1", 5 / 4)
p_axis = stats.norm.cdf(1.25, 0, 0.35) - stats.norm.cdf(-1.25, 0, 0.35)
v.check("X25.7b", 100 * p_axis**2)
esc = 0.15 * 0.02 / (0.85 + 0.15 * 0.02)
n_mc = 4_000_000
bad = RNG.random(n_mc) < 0.15
caught = RNG.random(n_mc) < 0.98
passed = ~(bad & caught)
esc_mc = (bad & passed).sum() / passed.sum()
v.assert_true("Q7 escape rate: Monte Carlo within 3% of closed form", abs(esc_mc / esc - 1) < 0.03,
              f"MC {100 * esc_mc:.4f}% vs {100 * esc:.4f}%")
v.check("X25.7c", 100 * esc)
v.check("X25.7c1", 0.998**7 * (1 - esc) * (1 - 0.004) ** 6)


def pkg(areas, pkg_cost, d0_):
    s = sum((0.30 * a + 3) / math.exp(-a / 100 * d0_) for a in areas)
    return (s + pkg_cost) / 0.99 ** len(areas)


mono, chip = pkg([600], 50, 0.12), pkg([220] * 3, 90, 0.12)
v.check("X25.7d3", math.exp(-6 * 0.12))
v.check("X25.7d", mono)
v.check("X25.7d4", math.exp(-2.2 * 0.12))
v.check("X25.7d1", chip)
v.check("X25.7d2", chip / mono)

# ---------------------------------------------------------------- Q8
v.check("X25.8a", 30e-6 / (4 * 600e-6))
v.check("X25.8a1", 1000 * 30e-6 / (4 * 600e-6))
a8 = 0.4e-3
q8 = 3 / (math.pi * a8**2)
v.check("X25.8b", integrate.quad(lambda rr: q8 / 150, 0, a8)[0])
v.check("X25.8b1", 8 / (3 * math.pi**2 * 150 * a8))
m2 = 2 * 60 / (200 * 0.8e-3)
x = np.linspace(0, 0.030, 101)
sol = integrate.solve_bvp(lambda s, y: np.vstack([y[1], m2 * y[0]]), lambda ya, yb: np.array([ya[0] - 1, yb[1]]),
                          x, np.vstack([np.ones_like(x), np.zeros_like(x)]), tol=1e-8)
xs = np.linspace(0, 0.030, 4001)
v.check("X25.8c0", math.sqrt(m2))
v.check("X25.8c", math.sqrt(m2) * 0.030)
v.check("X25.8c1", integrate.trapezoid(sol.sol(xs)[0], xs) / 0.030)
rise = 1200 / (1000 * 4180 * 1.5 / 6e4)
v.check("X25.8d", rise)
v.check("X25.8d0", rise / 2)
v.check("X25.8d1", 40 + rise / 2 + 1200 * 0.030)

# ---------------------------------------------------------------- Q9
aft = math.exp(0.85 / K * (1 / 383.15 - 1 / 553.15))
v.check("X25.9a", aft)
v.check("X25.9a1", aft * 4**1.5)
e = np.array([10.0, 9.5])
lt = np.log([30.0, 300.0])
cE = np.polyfit(e, lt, 1)
cP = np.polyfit(np.log(e), lt, 1)
tE, tP = math.exp(np.polyval(cE, 6.0)), math.exp(np.polyval(cP, math.log(6.0)))
v.check("X25.9b", -cE[0])
v.check("X25.9b1", tE)
v.check("X25.9b2", -cP[0])
v.check("X25.9b3", tP)
v.check("X25.9b4", tP / tE)
v.check("X25.9c", stats.chi2.ppf(0.6, 2) / (2 * 2000 * 1000 * 50) * 1e9)
v.check("X25.9c1", stats.chi2.ppf(0.6, 4) / (2 * 2000 * 1000 * 50) * 1e9)

# ---------------------------------------------------------------- Q10
n_field = 15 * 365.25 * 3
v.check("X25.10a0", n_field)
v.check("X25.10a4", n_field)
for n_cm, k_af, k_n in ((2.0, "X25.10a", "X25.10a1"), (2.5, "X25.10a2", "X25.10a3")):
    af = (205 / 50) ** n_cm
    v.check(k_af, af)
    v.check(k_n, n_field / af)
tot, dang, cov, mech, rev = 150 + 15, 150 - 50, 0.98, 15, 0.80
rf, lat = dang * (1 - cov), mech * (1 - rev)
v.check("X25.10b2", tot)
v.check("X25.10b3", rf)
v.check("X25.10b4", lat)
v.check("X25.10b5", tot - rf)
v.check("X25.10b", 100 * (1 - rf / tot))
v.check("X25.10b1", 100 * (1 - lat / (tot - rf)))
v.check("X25.10c", 100 * optimize.brentq(lambda dc: 1 - (1 - dc) * dang / tot - 0.99, 0.5, 1))
v.check("X25.10d", 100 * stats.binom.sf(0, 12000, 0.5e-6))

# ---------------------------------------------------------------- Q11
xi = 0.025
tau = grow_time(xi)  # time from bare silicon to x_i is the offset
v.assert_true("Q11a offset equals (xi^2 + A xi)/B", abs(tau - (xi**2 + A * xi) / B) < 1e-6)
t_from_xi = grow_time(0.30, x0=xi)
v.check("X25.11a", tau)
v.check("X25.11a0", grow_time(0.30))
v.check("X25.11a1", t_from_xi)
beta = 4.5
s_other = 20000 * 3.0**-beta
s_tot = 400 + s_other
v.check("X25.11b0", s_other)
v.check("X25.11b1", s_tot)
surv = lambda t: math.exp(-(400 + s_other) * t**beta)  # noqa: E731
eta_num = integrate.quad(surv, 0, 1, limit=200)[0] / math.gamma(1 + 1 / beta)
v.check("X25.11b", eta_num)
h_c = lambda t: 400 * beta * t ** (beta - 1)  # noqa: E731
frac_num = integrate.quad(lambda t: h_c(t) * surv(t), 0, 1, limit=200)[0]
v.check("X25.11b2", 100 * frac_num)
# mean exposure T/2 by simulating Poisson arrivals over many test intervals
T = 2000.0
arr = np.cumsum(RNG.exponential(1 / 3e-3, 200_000))
expo = np.ceil(arr / T) * T - arr
v.assert_true("Q11c mean exposure of a latent fault is T/2", abs(expo.mean() / (T / 2) - 1) < 0.01,
              f"{expo.mean():.1f} h")
v.check("X25.11c", 3e-9 * 1e-7 * (T / 2) * 1e9)
v.check("X25.11c1", optimize.brentq(lambda tt: 3e-9 * 1e-7 * tt / 2 * 1e9 - 0.01, 1, 1e7))
ad = 6 * 0.1
for alpha, key in ((1, "X25.11d"), (3, "X25.11d1")):
    yv = integrate.quad(lambda d: math.exp(-6 * d) * stats.gamma.pdf(d, alpha, scale=0.1 / alpha), 0, np.inf)[0]
    v.check(key, yv)
v.assert_true("Q11d large-alpha limit is Poisson", abs((1 + ad / 1e6) ** -1e6 - math.exp(-ad)) < 1e-6)
v.check("X25.11d2", math.exp(-ad))

# ---------------------------------------------------------------- Q12
m12, c12 = pkg([800], 50, 0.1), pkg([220] * 4, 110, 0.1)
v.check("X25.12a11", math.exp(-0.8))
v.check("X25.12a12", math.exp(-0.22))
v.check("X25.12a1", m12)
v.check("X25.12a2", c12)
v.check("X25.12a", 100 * (1 - c12 / m12))
d30 = optimize.brentq(lambda d: pkg([220] * 4, 110, d) / pkg([800], 50, d) - 0.70, 0.05, 0.5)
v.check("X25.12a3", d30)
v.check("X25.12a4", 100 * (d30 / 0.1 - 1))
v.check("X25.12a5", 8 * d30)
v.check("X25.12a6", 2.2 * d30)
v.check("X25.12a7", math.exp(-8 * d30))
v.check("X25.12a8", math.exp(-2.2 * d30))
v.check("X25.12a9", pkg([800], 50, d30))
v.check("X25.12a10", pkg([220] * 4, 110, d30))
v.check("X25.12b0", 1500 * 0.015)
v.check("X25.12b2", 95 - 35 - 1500 * 0.015)
need = (95 - 35 - 1500 * 0.015) / 1500
v.check("X25.12b", need)
v.check("X25.12b1", 0.0627 / need)
eco_fixed, respin = 3 + 12 * 4, 30 + 24 * 4
v.check("X25.12c4", eco_fixed)
v.check("X25.12c0", respin)
cost_fix = eco_fixed + 0.3 * respin
delay_fix = 12 + 0.3 * 24
v.check("X25.12c", cost_fix)
v.check("X25.12c1", delay_fix)
v.check("X25.12c2", 0.95 * cost_fix)
v.check("X25.12c3", 0.95 * delay_fix)
z = 1.96
lo = optimize.brentq(lambda p: (1 - p) ** 2 - z * z * p * (1 - p) / 4, 0.01, 0.999)
v.assert_true("Q12d Wilson lower end equals n/(n + z^2)", abs(lo - 4 / (4 + z * z)) < 1e-9)
v.check("X25.12d", 100 * lo)
v.check("X25.12d1", 100 * lo / 5)

sys.exit(v.finish())
