#!/usr/bin/env python3
"""Verify every number in chapter 22-09 (batteries, charging and fuel gauging), its problems and its lab.

Independent routes (the lab module battery.py uses closed forms or a fixed-step loop):
- Gibbs energies and theoretical capacities from scipy.constants (Avogadro × elementary charge) and atomic masses;
- pulse responses, discharges to a cutoff and CC/CV charges by integrating the equivalent-circuit state equations
  with scipy solve_ivp and terminal events (the SOC, the RC-branch voltage and the delivered energy are states);
- charger losses by explicit input/output power balance; gauge errors by simulating the counter and by enumerating
  the corners of the OCV-reading errors; aging by evaluating the √t law and the Arrhenius factor from constants.
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants as sc
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "22-09-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import battery as bt  # noqa: E402

v = Verifier.from_files("22-09", ROOT / "chapters" / "22-09-batteries-charging-fuel-gauging.md",
                        ROOT / "solutions" / "22-09-solutions.md", LAB / "README.md")

FARADAY = sc.N_A * sc.e
ATOM = {"Li": 6.941, "C": 12.011, "Co": 58.933, "O": 15.999, "Fe": 55.845, "P": 30.974}
Q = 1080.0                                  # teaching cell, coulombs
OCV = lambda z: 3.30 + 0.90 * z


# ---------------------------------------------------------------- models integrated with solve_ivp
def run_cell(i_fn, t_end, z0, q=Q, ocv=OCV, r0=0.20, r1=0.10, c1=200.0, events=None, t_eval=None):
    """States: z, v1, delivered energy (∫ v i dt). Discharge current i_fn(t) > 0."""
    def f(t, y):
        i = i_fn(t)
        vt = ocv(y[0]) - i * r0 - y[1]
        return [-i / q, i / c1 - y[1] / (r1 * c1), vt * i]
    return integrate.solve_ivp(f, (0, t_end), [z0, 0.0, 0.0], method="LSODA", rtol=1e-11, atol=1e-13,
                               events=events, t_eval=t_eval, max_step=t_end / 4000)


def terminal(sol_y, i, ocv=OCV, r0=0.20):
    return ocv(sol_y[0]) - i * r0 - sol_y[1]


def discharge_to_cutoff(i, r, v_cut, ocv=OCV):
    """Resistive quasi-static cell (r0 = r, no RC branch) discharged at i to v_cut. Returns (usable fraction, Wh)."""
    ev = lambda t, y: ocv(y[0]) - i * r - v_cut
    ev.terminal = True
    sol = run_cell(lambda t: i, 1e6, 1.0, ocv=ocv, r0=r, r1=1e-9, c1=1.0, events=ev)
    return 1 - sol.y_events[0][0][0], sol.y_events[0][0][2] / 3600


def cccv_ivp(i_cc, i_term, r0, r1=None, c1=None, ocv=OCV, v_max=4.20, z0=0.0):
    """CC/CV charge by integration. With r1, c1 the RC branch is included and the charger holds the terminal at
    v_max: i = min(I_cc, (v_max − OCV − v1)/r0). Returns (t_cc, t_term, z_term)."""
    def cur(y):
        v1 = y[1] if r1 else 0.0
        return min(i_cc, (v_max - ocv(y[0]) - v1) / r0)

    def f(t, y):
        i = cur(y)
        dv1 = (i / c1 - y[1] / (r1 * c1)) if r1 else 0.0
        return [i / Q, dv1]
    ev_cc = lambda t, y: (v_max - ocv(y[0]) - (y[1] if r1 else 0.0)) / r0 - i_cc
    ev_cc.direction = -1
    ev_end = lambda t, y: cur(y) - i_term
    ev_end.terminal = True
    ev_end.direction = -1
    sol = integrate.solve_ivp(f, (0, 3e4), [z0, 0.0], method="LSODA", rtol=1e-11, atol=1e-13,
                              events=[ev_cc, ev_end], max_step=2.0)
    return sol.t_events[0][0], sol.t_events[1][0], sol.y_events[1][0][0]


# ---------------------------------------------------------------- §3.1 text values
v.check("Txt 22-09.a", 3.7 * FARADAY / 1e3)
cap = lambda m: FARADAY / m / 3.6
m_c6 = 6 * ATOM["C"]
m_lco = ATOM["Li"] + ATOM["Co"] + 2 * ATOM["O"]
v.check("Txt 22-09.b", cap(m_c6))
v.check("Txt 22-09.c", cap(m_lco))
v.assert_true("molar masses quoted in §3.1", round(m_c6, 2) == 72.07 and round(m_lco, 2) == 97.87)

# ---------------------------------------------------------------- Example 22-09.1
e_wh = integrate.quad(lambda t: 3.85 * 0.300, 0, 1.0)[0]          # 0.3 A for 1 h at 3.85 V
v.check("Ex 22-09.1a", e_wh)
v.check("Ex 22-09.1b", e_wh * 3600)
v.check("Ex 22-09.1c", 300.0 / 1.0)
v.check("Ex 22-09.1d", 60 * 0.300 / (2 * 0.300))
v.check("Ex 22-09.1e", e_wh / 6.5e-3)
v.check("Ex 22-09.1f", 300.0 / cap(m_c6))

# ---------------------------------------------------------------- Example 22-09.2 (pulse)
z_38 = optimize.brentq(lambda z: OCV(z) - 3.80, 0, 1)
big = run_cell(lambda t: 0.5, 20.0, z_38, q=1e12, t_eval=[1e-9, 20.0])
small = run_cell(lambda t: 0.5, 20.0, z_38, t_eval=[20.0])
v.check("Ex 22-09.2a", terminal(big.y[:, 0], 0.5))
v.check("Ex 22-09.2b", terminal(big.y[:, 1], 0.5))
v.check("Ex 22-09.2c", (3.80 - OCV(small.y[0, -1])) * 1e3)
v.check("Ex 22-09.2d", terminal(small.y[:, -1], 0.5))
i_short = optimize.brentq(lambda i: terminal(run_cell(lambda t: i, 1e-6, z_38, q=1e12).y[:, -1], i) - 3.40, 0.1, 10)
i_long = optimize.brentq(lambda i: terminal(run_cell(lambda t: i, 2000.0, z_38, q=1e12).y[:, -1], i) - 3.40, 0.1, 10)
v.check("Ex 22-09.2e", i_short)
v.check("Txt 22-09.d", i_long)

# ---------------------------------------------------------------- Example 22-09.3 (cold)
u25, e25 = discharge_to_cutoff(0.3, 0.30, 3.30)
um10, em10 = discharge_to_cutoff(0.3, 1.20, 3.30)
v.check("Ex 22-09.3a", 100 * u25)
v.check("Ex 22-09.3b", 100 * um10)
v.check("Ex 22-09.3c", e25)
v.check("Ex 22-09.3d", em10)
v.check("Ex 22-09.3e", 100 * em10 / e25)

# ---------------------------------------------------------------- Example 22-09.4 (CC/CV)
tcc1, tend1, zend1 = cccv_ivp(0.3, 0.03, 0.30)
tcc2, tend2, zend2 = cccv_ivp(0.6, 0.03, 0.30)
v.check("Ex 22-09.4a", 0.3 * tcc1 / Q)                     # SOC = charge delivered in CC / Q
v.check("Ex 22-09.4b", tcc1 / 60)
# CV time constant: fit the exponential decay of the CV current from two samples
def cv_current_at(t_after, i_cc=0.3):
    z_cv = 0.3 * tcc1 / Q
    sol = integrate.solve_ivp(lambda t, y: [(4.20 - OCV(y[0])) / 0.30 / Q], (0, t_after), [z_cv],
                              rtol=1e-12, atol=1e-14)
    return (4.20 - OCV(sol.y[0, -1])) / 0.30


tau_fit = 100.0 / math.log(cv_current_at(0.0 + 1e-9) / cv_current_at(100.0))
v.check("Ex 22-09.4c", tau_fit)
v.check("Ex 22-09.4d", (tend1 - tcc1) / 60)
v.check("Ex 22-09.4e", zend1)
v.check("Ex 22-09.4f", tend1 / 60)
v.check("Ex 22-09.4g", 0.6 * tcc2 / Q)
v.check("Ex 22-09.4h", (tend2 - tcc2) / 60)
v.check("Ex 22-09.4i", tend2 / 60)
lab_cf = bt.cccv_linear(Q, 0.3, 0.03, 0.30)
v.assert_true("battery.cccv_linear agrees with the integration", abs(lab_cf[1] + lab_cf[3] - tend1) < 0.5)

# ---------------------------------------------------------------- Example 22-09.5 (chargers)
def charger_balance(v_in, v_bat, i, eta=None):
    p_out = v_bat * i
    p_in = v_in * i if eta is None else p_out / eta          # linear: input current equals charge current
    return p_in - p_out, p_out / p_in


d37, eff37 = charger_balance(5.0, 3.7, 1.0)
d30, _ = charger_balance(5.0, 3.0, 1.0)
dbuck, _ = charger_balance(5.0, 3.7, 1.0, eta=0.92)
v.check("Ex 22-09.5a", d37)
v.check("Ex 22-09.5b", 100 * eff37)
v.check("Ex 22-09.5c", d37 * 40)
v.check("Ex 22-09.5d", d30)
v.check("Ex 22-09.5e", d30 * 40)
v.check("Ex 22-09.5f", dbuck)
v.check("Ex 22-09.5g", dbuck * 40)
v.check("Ex 22-09.5h", optimize.brentq(lambda i: charger_balance(5.0, 3.0, i)[0] * 40 - 40, 1e-3, 5))

# ---------------------------------------------------------------- Example 22-09.6 (gauging)
t_week = np.linspace(0, 7 * 86400, 7 * 24 * 60 + 1)
err_c = integrate.trapezoid(np.full_like(t_week, 10e-6), t_week) / 3.6      # mAh
v.check("Ex 22-09.6a", err_c)
v.check("Ex 22-09.6b", 100 * err_c / 300)
v.check("Ex 22-09.6c", 0.01 * 270)
v.check("Ex 22-09.6d", 100 * 0.01 * 270 / 300)
qmax = 160 / (0.90 - 0.35)
v.check("Ex 22-09.6e", qmax)
v.check("Ex 22-09.6f", 100 * qmax / 300)
corners = [160 / ((0.90 + a) - (0.35 + b)) for a, b in itertools.product((-0.01, 0.01), repeat=2)]
v.check("Ex 22-09.6g", 100 * (max(corners) - qmax) / qmax)
v.check("Txt 22-09.l", 1e3 * 20 / (7 * 24))

# ---------------------------------------------------------------- Example 22-09.7 (ring)
i_ring = 22.5 / (7 * 24)                   # mA
v.check("Ex 22-09.7a", i_ring * 1e3)
v.check("Ex 22-09.7b", 100 * 11e-3 / i_ring)
v.check("Ex 22-09.7c", optimize.brentq(lambda h: i_ring * h - 22.5 * 0.8 * 0.9, 1, 1e4) / 24)

# ---------------------------------------------------------------- Lab
pulse = run_cell(lambda t: 0.5 if 1.0 <= t < 41.0 else 0.0, 81.0, z_38, t_eval=[81.0])
v_rest = terminal(pulse.y[:, -1], 0.0)
v.check("Lab 22-09.a", v_rest)
v.check("Lab 22-09.b", 100 * (OCV(pulse.y[0, -1]) - v_rest) / 0.90)
_, t_rc, _ = cccv_ivp(0.3, 0.03, 0.20, r1=0.10, c1=200.0)
v.check("Lab 22-09.c", t_rc / 60)
ocv_c = lambda z: 3.0 + 0.6 * z + 0.35 * (1 - math.exp(-12 * z)) + 0.25 * z ** 6
_, t_curv, z_curv = cccv_ivp(0.3, 0.03, 0.30, ocv=ocv_c)
v.check("Lab 22-09.d", t_curv / 60)
v.check("Lab 22-09.e", z_curv)
v.check("Lab 22-09.f", 100 * discharge_to_cutoff(0.3, 0.30, 3.00, ocv=ocv_c)[0])
v.check("Lab 22-09.g", 100 * discharge_to_cutoff(0.3, 1.20, 3.00, ocv=ocv_c)[0])
v.assert_true("the curved OCV runs 3.00 V to 4.20 V", abs(ocv_c(0) - 3.0) < 1e-12 and abs(ocv_c(1) - 4.2) < 1e-4)
v.assert_true("battery.ocv_curved matches", abs(float(bt.ocv_curved(0.37)) - ocv_c(0.37)) < 1e-12)

# ---------------------------------------------------------------- Problems
v.check("22-09.1a", 4.5 * 3.87)
v.check("22-09.1b", 4.5 * 3.87 / 0.070)
v.check("22-09.1c", 0.7 * 4.5)
v.check("22-09.2a", 3.3 * FARADAY / 1e3)
m_lfp = ATOM["Li"] + ATOM["Fe"] + ATOM["P"] + 4 * ATOM["O"]
v.assert_true("LiFePO4 molar mass 157.76", round(m_lfp, 2) == 157.76)
v.check("22-09.2b", cap(m_lfp))

p3 = run_cell(lambda t: 2.0 if t < 10.0 else 0.0, 20.0, 0.5, q=1e12, ocv=lambda z: 3.75, r0=0.08, r1=0.05,
              c1=400.0, t_eval=[1e-9, 10.0 - 1e-9, 20.0])
v.check("22-09.3a", terminal(p3.y[:, 0], 2.0, ocv=lambda z: 3.75, r0=0.08))
v.check("22-09.3b", terminal(p3.y[:, 1], 2.0, ocv=lambda z: 3.75, r0=0.08))
v.check("22-09.3c", terminal(p3.y[:, 1], 0.0, ocv=lambda z: 3.75, r0=0.08))
v.check("22-09.3d", terminal(p3.y[:, 2], 0.0, ocv=lambda z: 3.75, r0=0.08))
v.check("22-09.3e", 1e3 * p3.y[1, 1])  # RC-branch state just before removal
v.check("22-09.3f", 1e3 * p3.y[1, 2])
v.check("22-09.3g", 1e3 * 0.9 * 2.0 * 10.0 / (4.5 * 3600))

v.check("22-09.4a", 100 * discharge_to_cutoff(0.6, 0.30, 3.30)[0])
v.check("22-09.4b", 100 * discharge_to_cutoff(0.6, 1.20, 3.30)[0])
v.check("22-09.4c", 1e3 * optimize.brentq(lambda i: discharge_to_cutoff(i, 1.20, 3.30)[0] - 0.90, 0.01, 0.2))

tcc5, tend5, zend5 = cccv_ivp(0.15, 0.015, 0.30)
v.check("22-09.5a", 0.15 * tcc5 / Q)
v.check("22-09.5b", tcc5 / 60)
v.check("22-09.5c", (tend5 - tcc5) / 60)
v.check("22-09.5d", tend5 / 60)
v.check("22-09.5e", zend5)

tcc6, tend6, zend6 = cccv_ivp(0.3, 0.03, 0.60)
v.check("22-09.6a", 0.3 * tcc6 / Q)
v.check("22-09.6b", tcc6 / 60)
v.check("22-09.6c", (tend6 - tcc6) / math.log(10))
v.check("22-09.6d", (tend6 - tcc6) / 60)
v.check("22-09.6e", tend6 / 60)
v.check("22-09.6f", zend6)

d7, e7 = charger_balance(5.0, 4.0, 0.060)
v.check("22-09.7a", d7)
v.check("22-09.7b", 100 * e7)

p8 = 3.8 * 6
v.check("22-09.8a", p8)
v.check("22-09.8b", p8 / 0.97)
v.check("22-09.8c", charger_balance(7.6, 3.8, 6, eta=0.97)[0])
v.check("22-09.8d", charger_balance(5.0, 3.8, 6, eta=0.92)[0])


def gauge_soc(v_meas, slope, v0=3.30):
    return optimize.brentq(lambda z: v0 + slope * z - v_meas, -5, 5)


z_true = 0.5
for key, slope in (("a", 0.90), ("b", 0.15)):
    v_load = 3.30 + slope * z_true - 0.09
    v.check(f"22-09.9{key}", z_true - gauge_soc(v_load, slope))
for key, slope in (("c", 0.90), ("d", 0.15)):
    v_corr = 3.30 + slope * z_true - 0.09 + 0.3 * 0.30 * 0.8    # correction with R 20% low
    v.check(f"22-09.9{key}", z_true - gauge_soc(v_corr, slope))

i_os = 1e-6 / 10e-3
v.check("22-09.10a", i_os * 1e6)
v.check("22-09.10b", integrate.quad(lambda t: i_os, 0, 86400)[0] / 3.6)
v.check("22-09.10c", 100 * integrate.quad(lambda t: i_os, 0, 86400)[0] / Q)
r_s = optimize.brentq(lambda r: 1e-6 / r - 10e-6, 1e-3, 10)
v.check("22-09.10d", r_s * 1e3)
v.check("22-09.10e", 0.3 ** 2 * r_s * 1e3)
v.check("22-09.10f", 0.3 * r_s * 1e3)

k_sqrt = 4.0 / math.sqrt(0.5)
v.check("22-09.11a", k_sqrt * math.sqrt(2))
v.check("22-09.11b", k_sqrt * math.sqrt(5))
arr = math.exp(0.5 * sc.e / sc.k * (1 / 298.15 - 1 / 308.15))
v.check("22-09.11c", arr)
v.check("22-09.11d", k_sqrt * math.sqrt(2 * arr))
v.assert_true("battery.arrhenius_factor agrees", abs(bt.arrhenius_factor(0.5, 25, 35) - arr) < 1e-6)

fade = lambda n: 1 - 0.2 * n / 1000
v.check("22-09.12a", 100 * fade(2 * 365))
v.check("22-09.12b", 100 * fade(2 * 365 / 5))
v.check("22-09.12c", 2 * 365 / 5)

i_allow = 22.5 * 0.8 * 0.9 / 168
v.check("22-09.13a", i_allow * 1e3)
v.check("22-09.13b", i_allow * 1e3 - 85)

# ---------------------------------------------------------------- text values derived from data-sheet figures
v.check("Txt 22-09.e", 50.0 / 4200.0)                          # P42A: 50 mA cut-off, 4200 mAh
v.check("Txt 22-09.f", 18000.0 / 3600.0)                       # BQ2407x tMAXCHG typ 18 000 s
v.check("Txt 22-09.g", 8.0 / 2.0)                              # 2:1 divider: input current half the output
v.check("Txt 22-09.h", 16e-3 * 4.2)                            # P42A DC 16 mOhm x 4.2 Ah
v.check("Txt 22-09.i", (0.20 + 0.10) * 0.300)                  # teaching cell
v.check("Txt 22-09.j", 0.5 * 0.050)                            # VARTA CP 1254: <0.5 ohm at 1 kHz, 50 mAh
v.check("Txt 22-09.k", 100 * (1 - 6.1 / 6.8))                  # Saft MP 176065

qm14 = 1.32 / (0.80 - 0.25)
v.check("22-09.14a", qm14)
v.check("22-09.14b", 100 * qm14 / 2.6)
c14 = [1.32 / ((0.80 + a) - (0.25 + b)) for a, b in itertools.product((-0.005, 0.005), repeat=2)]
v.check("22-09.14c", 100 * (max(c14) - qm14) / qm14)
v.check("22-09.14d", 100 * (min(c14) - qm14) / qm14)
v.check("22-09.14e", optimize.brentq(lambda dz: dz / (dz - 0.01) - 1.02, 0.02, 5))

v.finish()
