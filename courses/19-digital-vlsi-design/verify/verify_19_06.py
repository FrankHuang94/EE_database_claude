#!/usr/bin/env python3
"""Verify every number in chapter 19-06 (power and low-power design), its problems and its lab.

Independent routes:
- switching energy by integrating V_DD i(t) for an inverter charging a capacitor (square-law ODE);
- short-circuit charge by solving the unloaded inverter's static transfer curve at each input voltage and integrating
  the resulting supply current (not the closed form);
- the stack effect by solving current continuity in log form with a different root finder;
- supply scaling, the minimum-energy point and the parallelism break-even by direct numerical minimization or root
  finding on the defining quantities;
- the lab's module is checked against these results; ngspice confirms the switching and short-circuit charges.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp, trapezoid
from scipy.optimize import brentq, minimize_scalar, root_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "19-06-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import power as pw  # noqa: E402

v = Verifier.from_files("19-06", ROOT / "chapters" / "19-06-power-and-low-power-design.md",
                        ROOT / "solutions" / "19-06-solutions.md", LAB / "README.md")
VTH = 1.380649e-23 * 300 / 1.602176634e-19


def ids(k, vgs, vds, vt):
    ov = vgs - vt
    if ov <= 0 or vds <= 0:
        return 0.0
    return k * (ov * vds - vds * vds / 2) if vds < ov else k * ov * ov / 2


# ---------------------------------------------------------------- switching energy by ODE
def charge_energy(c, k, vdd, vt):
    sol = solve_ivp(lambda _t, y: [ids(k, vdd, vdd - y[0], vt) / c], (0, 2e-9), [0.0], method="LSODA", rtol=1e-11,
                    atol=1e-16, dense_output=True, max_step=1e-12)
    t = np.linspace(0, 2e-9, 200001)
    vo = sol.sol(t)[0]
    i = np.array([ids(k, vdd, vdd - x, vt) for x in vo])
    return trapezoid(vdd * i, t), trapezoid(i, t), 0.5 * c * vo[-1] ** 2


e_sup, q_sup, e_cap = charge_energy(10e-15, 200e-6, 1.2, 0.35)
v.check("Lab 19-06.a", q_sup * 1e15)
v.check("Lab 19-06.c", e_sup * 1e15)
v.check("Lab 19-06.d", e_cap * 1e15)


# ---------------------------------------------------------------- short-circuit charge from the static curve
def static_current(vin, k, vdd, vt):
    """Supply current of an unloaded symmetric inverter at a static input, from the VTC."""
    if vin <= vt or vin >= vdd - vt:
        return 0.0
    vo = brentq(lambda x: ids(k, vdd - vin, vdd - x, vt) - ids(k, vin, x, vt), 0.0, vdd, xtol=1e-15) \
        if abs(vin - vdd / 2) > 1e-12 else vdd / 2
    return ids(k, vin, vo, vt)


def sc_charge(k, vdd, vt, tau):
    vins = np.linspace(0, vdd, 40001)
    i = np.array([static_current(x, k, vdd, vt) for x in vins])
    return trapezoid(i, vins) * tau / vdd


q50 = sc_charge(200e-6, 1.2, 0.35, 50e-12)
v.check("Ex 19-06.2b", q50 * 1e15)
v.check("Ex 19-06.2a", 2 * q50 * 1.2 / 1e-9 * 1e6)
pdyn = 0.5 * 10e-15 * 1.2 ** 2 * 1e9
v.check("Ex 19-06.2c", pdyn * 1e6)
v.check("Ex 19-06.2d", 100 * 2 * q50 * 1.2 / 1e-9 / pdyn)
v.check("Lab 19-06.b", 2 * q50 * 1e15)
v.check("Lab 19-06.e", 2 * sc_charge(200e-6, 1.2, 0.35, 200e-12) * 1e15)
v.assert_true("lab Veendrick matches the static-curve integral",
              abs(pw.short_circuit_power_veendrick(200e-6, 1.2, 0.35, 50e-12, 1e-9) - 2 * q50 * 1.2 / 1e-9) < 1e-12, "")
q200 = sc_charge(200e-6, 1.2, 0.35, 200e-12)
v.check("19-06.4a", 2 * q200 * 1.2 / 1e-9 * 1e6)
v.check("19-06.4b", 100 * 2 * q200 * 1.2 / 1e-9 / pdyn)
v.check("19-06.4c", 2 * sc_charge(200e-6, 0.8, 0.35, 200e-12) * 0.8 / 1e-9 * 1e6)
v.check("19-06.10a", sc_charge(100e-6, 1.0, 0.3, 100e-12) * 1e15)

# ---------------------------------------------------------------- Example 1 and Problems 1-2
v.check("Ex 19-06.1a", 0.1 * 1e-9 * 0.8 ** 2 * 2e9)
v.check("Ex 19-06.1b", 1e-9 * 0.64 * 1e9)
v.check("Ex 19-06.1c", 0.5 * 1e-9 * 0.64 * 1e9)
v.check("Ex 19-06.1d", 100 * (1 - 0.7 ** 2 / 0.8 ** 2))
v.check("19-06.1a", 5e-15 * 0.81 * 1e15)
v.check("19-06.1b", 0.5 * 5e-15 * 0.81 * 1e15)
v.check("19-06.1c", 0.15 * 5e-15 * 0.81 * 1.5e9 * 1e6)
v.check("19-06.2a", 200e-12 * 0.81 * 2e9)
v.check("19-06.2b", 0.4 * 200e-12 * 0.81 * 2e9)

# ---------------------------------------------------------------- leakage
v.check("Ex 19-06.3a", 10 ** (100 / 90))
v.check("Ex 19-06.3b", 1e9 * 0.5 * 10e-9)
v.check("Ex 19-06.3c", 1e9 * 0.5 * 10e-9 * 0.8)
v.check("Ex 19-06.3d", 1e9 * 0.5 * 10e-9 * 0.8 * 10 ** (100 / 90))
v.check("19-06.3a", 1.4 * VTH * math.log(10) * 1e3)
v.check("19-06.3b", 1.4 * VTH * 380 / 300 * math.log(10) * 1e3)
vth380 = VTH * 380 / 300
v.check("19-06.5a", math.exp(-(0.35 - 0.8e-3 * 80) / (1.3 * vth380)) / math.exp(-0.35 / (1.3 * VTH)))


def stack(eta, n=1.3, vdd=1.0, vt=0.35):
    """Solve ln I_top = ln I_bottom for the middle node; return (vx, I_single/I_bottom)."""
    def lnI(vgs, vds):
        return (vgs - vt + eta * vds) / (n * VTH) + math.log1p(-math.exp(-vds / VTH))
    sol = root_scalar(lambda x: lnI(-x, vdd - x) - lnI(0.0, x), bracket=[1e-6, 0.5], method="bisect", xtol=1e-15)
    vx = sol.root
    return vx, math.exp(lnI(0.0, vdd) - lnI(0.0, vx))


for eta, kx, kr in ((0.1, "Ex 19-06.4a", "Ex 19-06.4b"), (0.0, "Ex 19-06.4c", "Ex 19-06.4d"),
                    (0.05, "19-06.6a", "19-06.6b"), (0.2, "19-06.6c", "19-06.6d")):
    vx, ratio = stack(eta)
    v.check(kx, vx * 1e3)
    v.check(kr, ratio)
v.check("Ex 19-06.4e", math.exp(0.1 * 1.0 / (1.3 * VTH)))
v.assert_true("lab stack_leakage_ratio matches", abs(pw.stack_leakage_ratio(1.0, 0.35, 1.3, 0.1)[1] - stack(0.1)[1]) < 1e-6, "")


# ---------------------------------------------------------------- voltage scaling
def vfor(factor, v0=1.0, vt=0.35, a=1.3):
    d = lambda x: x / (x - vt) ** a  # noqa: E731
    return root_scalar(lambda x: d(x) - factor * d(v0), bracket=[vt + 1e-9, v0], method="brentq", xtol=1e-15).root


v2, v3, v4 = vfor(2), vfor(3), vfor(4)
v.check("Ex 19-06.5a", v2)
v.check("Ex 19-06.5b", v2 ** 2 / 2)
v.check("Ex 19-06.5c", 2 / v2 ** 2)
v.check("Ex 19-06.5d", v2 ** 2)
v.check("Ex 19-06.5e", 2 * 1.15 * v2 ** 2 / 2)
v.check("19-06.7a", v3)
v.check("19-06.7b", v3 ** 2 / 3)
v.check("19-06.7c", v3 ** 2)
v.check("19-06.12a", brentq(lambda o: (1 + o) * v2 ** 2 - 1, 0, 5, xtol=1e-14))
v.check("19-06.12b", v4)
v.check("19-06.12c", v4 ** 2)
v.check("19-06.12d", 1.3 * v4 ** 2)


# ---------------------------------------------------------------- minimum energy by direct minimization
def e_op(vv, a, d, n=1.3):
    return vv * vv * (a + d * math.exp(-vv / (n * VTH)))


def vmin(a, d):
    return minimize_scalar(lambda x: e_op(x, a, d), bounds=(0.1, 0.6), method="bounded", options={"xatol": 1e-12}).x


vm = vmin(0.1, 20)
v.check("Ex 19-06.6a", vm / (1.3 * VTH))
v.check("Ex 19-06.6b", vm * 1e3)
leak = 20 * math.exp(-vm / (1.3 * VTH))
v.check("Ex 19-06.6c", 100 * leak / (0.1 + leak))
v.check("Ex 19-06.6d", e_op(0.3, 0.1, 20) / e_op(vm, 0.1, 20))
v.check("Ex 19-06.6e", e_op(0.4, 0.1, 20) / e_op(vm, 0.1, 20))
v.check("Ex 19-06.6f", vmin(0.05, 20) * 1e3)
v.check("Ex 19-06.6g", vmin(0.1, 50) * 1e3)
v.check("Ex 19-06.6h", (0.4 / vm) ** 2)
vm11 = vmin(0.02, 10)
v.check("19-06.11a", vm11 / (1.3 * VTH))
v.check("19-06.11b", vm11 * 1e3)
v.assert_true("V_min depends only on L_d/alpha", abs(vm11 - vmin(0.1, 50)) < 1e-9, "")
v.assert_true("leakage share equals 2/x", abs(leak / (0.1 + leak) - 2 / (vm / (1.3 * VTH))) < 1e-6, "")
lmax = minimize_scalar(lambda x: -e_op(x, 0.1, 20), bounds=(0.03, 0.15), method="bounded", options={"xatol": 1e-12}).x
v.check("Lab 19-06.f", lmax * 1e3)
v.assert_true("lab minimum_energy_supply matches", abs(pw.minimum_energy_supply(0.1, 20, 1.3) - vm) < 1e-6, "")

# ---------------------------------------------------------------- gating and multi-VT
v.check("19-06.8a", (500e-12 * 0.8 ** 2 + 0.08e-9) * 1e9)
v.check("19-06.8b", (500e-12 * 0.64 + 0.08e-9) / 2e-3 * 1e9)
v.check("19-06.8c", (500e-12 * 0.64 + 0.08e-9) / (0.99 * 2e-3) * 1e9)
f_lvt = 10 ** (100 / 90)
v.check("19-06.9a", 0.9 + 0.1 * f_lvt)
v.check("19-06.9b", 0.7 + 0.3 * f_lvt)

# practitioner lens: SKY130 hd and hdll leakage per kGate [R-314]
v.check("Txt 19-06.a", 0.86 / 0.08)
v.check("Txt 19-06.b", 50 * 0.35 / 1.2)
v.check("Txt 19-06.c", static_current(0.6, 200e-6, 1.2, 0.35) * 1e6)
v.check("Txt 19-06.d", 50 * (1.2 - 0.35) / 1.2)
v.check("Txt 19-06.e", (1.000 / 0.675) ** 2)
v.check("Txt 19-06.f", (1.000 / 0.675) ** 2 * 2)

sys.exit(v.finish())
