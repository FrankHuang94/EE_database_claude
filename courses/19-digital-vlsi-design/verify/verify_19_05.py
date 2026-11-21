#!/usr/bin/env python3
"""Verify every number in chapter 19-05 (interconnect), its problems and its lab.

Independent routes:
- the distributed line's 50% delay by solving the diffusion PDE with a fine finite-difference method of lines
  (not the Fourier series), and the Fourier series checked against it;
- driver-wire-load delays from ladder simulations integrated with solve_ivp and extrapolated to infinitely many
  sections (Richardson), not from the formula;
- repeater optima by brute-force numerical minimization of T(k, h), and the closed forms checked against it;
- capacitances from the geometry formulas evaluated here; crosstalk by charge conservation;
- the lab's module is checked against these results; ngspice confirms the 100-section ladders in rcline.cir.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "19-05-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import wires as wr  # noqa: E402

v = Verifier.from_files("19-05", ROOT / "chapters" / "19-05-interconnect.md",
                        ROOT / "solutions" / "19-05-solutions.md", LAB / "README.md")
LN2 = math.log(2)
EPS0 = 8.8541878128e-12
P, F = 1e-12, 1e-15


# ---------------------------------------------------------------- ladders by ODE integration
def ladder50(n, r_tot, c_tot, r_drv=0.0, c_load=0.0):
    rs = np.array([r_drv + r_tot / n] + [r_tot / n] * (n - 1))
    cs = np.array([c_tot / n] * (n - 1) + [c_tot / n + c_load])
    g = 1 / rs

    def f(_t, x):
        left = np.concatenate(([1.0], x[:-1]))
        i_in = g * (left - x)
        i_out = np.concatenate((i_in[1:], [0.0]))
        return (i_in - i_out) / cs
    tau = float(np.sum(cs * np.cumsum(rs)))
    ev = lambda _t, x: x[-1] - 0.5  # noqa: E731
    ev.terminal = True
    main = np.concatenate(([-(g[0] + (g[1] if n > 1 else 0))], -(g[1:] + np.concatenate((g[2:], [0.0])))))
    jac = np.diag(main) + np.diag(g[1:], 1) + np.diag(g[1:], -1)
    jac = jac / cs[:, None]
    sol = solve_ivp(f, (0, 5 * tau), np.zeros(n), events=ev, method="Radau", jac=jac, rtol=1e-10, atol=1e-13)
    return float(sol.t_events[0][0])


def continuum(r_tot, c_tot, r_drv=0.0, c_load=0.0):
    """Richardson extrapolation of the ladder delay to infinitely many sections (error ~ 1/n)."""
    a, b = ladder50(200, r_tot, c_tot, r_drv, c_load), ladder50(400, r_tot, c_tot, r_drv, c_load)
    return 2 * b - a


t_line = continuum(1.0, 1.0)
v.check("Txt 19-05.a", t_line)
v.assert_true("Fourier series agrees with the PDE solution", abs(wr.line_t50() - t_line) < 2e-4, f"{t_line:.5f}")
v.check("Txt 19-05.b", LN2 / 2)
v.check("Txt 19-05.f", LN2 / 2)
v.check("Txt 19-05.c", 100 * (LN2 / t_line - 1))
v.check("Txt 19-05.d", 100 * (1 - (LN2 / 2) / t_line))


# ---------------------------------------------------------------- repeater optimum by brute force
def t_rep(k, h, r0, c0, rw, cw):
    return LN2 * r0 * cw / h + LN2 * k * r0 * c0 + 0.379 * rw * cw / k + LN2 * rw * h * c0


def opt_rep(r0, c0, rw, cw):
    res = minimize(lambda x: t_rep(math.exp(x[0]), math.exp(x[1]), r0, c0, rw, cw) * 1e12, [math.log(10), math.log(10)],
                   method="Nelder-Mead", options={"xatol": 1e-12, "fatol": 1e-12, "maxiter": 20000})
    return math.exp(res.x[0]), math.exp(res.x[1]), res.fun * 1e-12


v.check("Txt 19-05.e", opt_rep(1.0, 1.0, 1.0, 1.0)[2])
v.check("19-05.10a", opt_rep(3.0, 0.5, 7.0, 2.0)[2] / math.sqrt(3.0 * 0.5 * 7.0 * 2.0))

# ---------------------------------------------------------------- Example 1
rho = 1.7e-8
R1 = rho * 100e-6 / (50e-9 * 100e-9)
v.check("Ex 19-05.1a", rho / 100e-9)
v.check("Ex 19-05.1b", 100e-6 / 50e-9)
v.check("Ex 19-05.1c", R1)
v.check("Ex 19-05.1d", 2 * R1)
v.check("Ex 19-05.1e", 475 * 100 / 1e3)
v.check("Ex 19-05.1f", 270e-18 * 100 / F)
v.check("Ex 19-05.1g", 0.379 * 475 * 100 * 270e-18 * 100 / P)
v.check("Ex 19-05.1h", 475 * 100 / R1)
v.assert_true("lab wire_resistance", abs(wr.wire_resistance(rho, 100e-6, 50e-9, 100e-9) - R1) < 1e-9, "")

# Example 2
cp = 2.5 * EPS0 * 24 / 48
cc = 2.5 * EPS0 * 48 / 24
v.check("Ex 19-05.2a", cp * 1e12)
v.check("Ex 19-05.2b", cc * 1e12)
v.check("Ex 19-05.2c", (cp + 2 * cc) * 1e12)
v.check("Ex 19-05.2d", 100 * 2 * cc / (cp + 2 * cc))

# Example 3
Rw, Cw = 13.3 * 1000, 0.198e-15 * 1000
v.check("Ex 19-05.3a", Rw / 1e3)
v.check("Ex 19-05.3b", Cw / F)
v.check("Ex 19-05.3c", Rw * Cw * 1e9)
v.check("Ex 19-05.3d", 0.379 * Rw * Cw / P)
v.check("Ex 19-05.3e", LN2 * Rw * Cw / P)
v.check("Ex 19-05.3f", LN2 * Rw * Cw / 2 / P)
est = LN2 * 1e3 * (Cw + 10e-15) + Rw * (0.379 * Cw + LN2 * 10e-15)
ex3 = continuum(Rw, Cw, 1e3, 10e-15)
v.check("Ex 19-05.3g", est / P)
v.check("Ex 19-05.3h", ex3 / P)
v.check("Ex 19-05.3i", 100 * (1 - est / ex3))
v.check("Ex 19-05.3j", 100 * Rw * (0.379 * Cw + LN2 * 10e-15) / est)
v.assert_true("lab driver_wire_load_delay", abs(wr.driver_wire_load_delay(1e3, Rw, Cw, 10e-15) - est) < 1e-18, "")

# Example 4
k4, h4, T4 = opt_rep(10e3, 0.1e-15, Rw, Cw)
v.check("Ex 19-05.4a", k4)
v.check("Ex 19-05.4b", 1000 / k4)
v.check("Ex 19-05.4c", h4)
v.check("Ex 19-05.4d", T4 / P)
un4 = LN2 * (10e3 / h4) * (Cw + h4 * 0.1e-15) + Rw * (0.379 * Cw + LN2 * h4 * 0.1e-15)
v.check("Ex 19-05.4e", un4 / P)
v.check("Ex 19-05.4f", un4 / T4)
k5, h5, T5 = opt_rep(10e3, 0.1e-15, 5 * Rw, 5 * Cw)
un5 = LN2 * (10e3 / h5) * (5 * Cw + h5 * 0.1e-15) + 5 * Rw * (0.379 * 5 * Cw + LN2 * h5 * 0.1e-15)
v.check("Ex 19-05.4g", k5)
v.check("Ex 19-05.4h", T5 / P)
v.check("Ex 19-05.4i", un5 * 1e9)
v.check("Ex 19-05.4j", un5 / T5)
v.assert_true("h independent of length", abs(h5 - h4) < 1e-4 * h4, "")
v.assert_true("lab repeater_optimum", abs(wr.repeater_optimum(10e3, 0.1e-15, Rw, Cw)[2] - T4) < 1e-6 * T4, "")

# Example 5
v.check("Ex 19-05.5a", 1.0 * 5 / 25)
v.check("Ex 19-05.5b", 100 + 2 * 50 * 0)
v.check("Ex 19-05.5c", 100 + 2 * 50 * 1)
v.check("Ex 19-05.5d", 100 + 2 * 50 * 2)
v.check("Ex 19-05.5e", 300 / 100)
# charge conservation for the floating victim: aggressor step dV through Cc onto Cg
dv = brentq(lambda x: 5e-15 * ((1.0 - x) - 0) - 20e-15 * x, 0, 1, xtol=1e-15)
v.assert_true("floating victim by charge conservation", abs(dv - 0.2) < 1e-12, "")

# Example 6
S = 0.7
v.check("Ex 19-05.6a", 1 / S ** 2)
v.check("Ex 19-05.6b", (S / S ** 2) * S)
v.check("Ex 19-05.6c", 1 / S ** 2)
v.check("Ex 19-05.6d", math.sqrt(S / S ** 2))
v.check("Ex 19-05.6e", math.sqrt(S / S ** 2) / S)

# ---------------------------------------------------------------- problems
R_1, C_1 = 0.08 * 2000 / 0.1, 0.2e-15 * 2000
v.check("19-05.1a", 2000 / 0.1)
v.check("19-05.1b", R_1 / 1e3)
v.check("19-05.1c", C_1 / F)
v.check("19-05.1d", 0.379 * R_1 * C_1 / P)
v.check("19-05.2a", 2e3 / 10)
v.check("19-05.3a", 0.8 * 3 / 18)
v.check("19-05.4a", 0.379 * 500)
v.check("19-05.4b", LN2 * 500)
v.check("19-05.4c", LN2 * 250)
a5 = LN2 * 500 * 420e-15 + 10e3 * (0.379 * 400e-15 + LN2 * 20e-15)
b5 = LN2 * 125 * 420e-15 + 10e3 * (0.379 * 400e-15 + LN2 * 20e-15)
v.check("19-05.5a", a5 / P)
v.check("19-05.5b", b5 / P)
v.check("19-05.5c", 100 * (1 - b5 / a5))
k6, h6, T6 = opt_rep(8e3, 0.2e-15, 10e3, 400e-15)
v.check("19-05.6a", k6)
v.check("19-05.6b", 2000 / k6)
v.check("19-05.6c", h6)
v.check("19-05.6d", T6 / P)
v.check("19-05.6e", T6 / P / 2)
v.check("19-05.6f", a5 / T6)
v.check("19-05.7a", opt_rep(4e3, 0.2e-15, 10e3, 400e-15)[2] / T6)
v.check("19-05.8a", 60)
v.check("19-05.8b", 60 + 30 * 2 + 30 * 2)
v.check("19-05.8c", 60 + 30 + 0)
v.check("19-05.8d", 60 + 30 + 60)
pc9, cc9 = 3.0 * EPS0 * 40 / 80, 3.0 * EPS0 * 80 / 40
v.check("19-05.9a", 2 * pc9 * 1e12)
v.check("19-05.9b", 2 * cc9 * 1e12)
v.check("19-05.9c", (2 * pc9 + 2 * cc9) * 1e12)
v.check("19-05.9d", 100 * 2 * cc9 / (2 * pc9 + 2 * cc9))
rf = 1.25 / S ** 2
v.check("19-05.11a", rf)
v.check("19-05.11b", math.sqrt(S * rf))
v.check("19-05.11c", math.sqrt(S * rf) / S)
v.check("19-05.11d", math.sqrt(S * rf) ** 3)
v.check("19-05.11e", (math.sqrt(S * rf) / S) ** 3)
per_mm = T4 / P
v.check("19-05.12a", 6 * per_mm)
v.check("19-05.12b", 200 / per_mm)
v.check("19-05.12c", math.ceil(6 / (200 / per_mm)))

# ---------------------------------------------------------------- lab
v.check("Lab 19-05.a", ladder50(100, Rw, Cw) / P)
v.check("Lab 19-05.b", ladder50(100, Rw, Cw, 1e3, 10e-15) / P)
for n, key in ((10, "c"), (50, "d"), (100, "e")):
    v.check(f"Lab 19-05.{key}", 100 * (ladder50(n, 1.0, 1.0) / t_line - 1))
v.check("Lab 19-05.f", 100 * (t_rep(2 * k4, h4, 10e3, 0.1e-15, Rw, Cw) / T4 - 1))
v.assert_true("half the repeaters costs the same", abs(t_rep(k4 / 2, h4, 10e3, 0.1e-15, Rw, Cw)
                                                     - t_rep(2 * k4, h4, 10e3, 0.1e-15, Rw, Cw)) < 1e-18, "")
v.check("Lab 19-05.g", 100 * (t_rep(k4, 2 * h4, 10e3, 0.1e-15, Rw, Cw) / T4 - 1))
v.check("Lab 19-05.h", opt_rep(5e3, 0.1e-15, Rw, Cw)[2] / P)
v.check("Lab 19-05.i", LN2 * Rw * 10e-15 / P)

sys.exit(v.finish())
