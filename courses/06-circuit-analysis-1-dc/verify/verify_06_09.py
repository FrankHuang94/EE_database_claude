#!/usr/bin/env python3
"""Verify every number published in chapter 06-09, its solutions and its lab handout.

Independent routes. The text uses the closed forms R_L = R_th, V^2/(4R), 4*eta*(1 - eta) and the
derivative conditions for the coax optima. This script instead maximizes load power numerically
(bounded scalar optimization over the load or the load voltage), finds the coax optima by numerical
minimization of the loss and power expressions written from first principles, solves operating
points of networks with a small nodal solver, and finds the solar cell's maximum-power point by
optimization of v*i(v).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C_DIR = HERE.parent
v = Verifier.from_files("06-09", C_DIR / "chapters" / "06-09-maximum-power-transfer.md",
                        C_DIR / "solutions" / "06-09-solutions.md", C_DIR / "labs" / "06-09-lab" / "README.md")


def load_power(V, R, RL):
    i = V / (R + RL)
    return i * i * RL


def best_load(V, R):
    """Numerically maximize load power over log(R_L); returns (R_L*, p_max)."""
    res = minimize_scalar(lambda u: -load_power(V, R, np.exp(u)), bounds=(np.log(R) - 10, np.log(R) + 10),
                          method="bounded", options={"xatol": 1e-12})
    return np.exp(res.x), -res.fun


def efficiency(R, RL):
    return RL / (R + RL)


# ================================================================ chapter
v.check("T 06-09.a", 100 * load_power(1, 1, 2) / best_load(1, 1)[1])
for ident, eta in (("b", 0.8), ("c", 0.9), ("d", 0.95), ("e", 0.99)):
    RL = eta / (1 - eta)                           # with R_th = 1
    v.check(f"T 06-09.{ident}", load_power(1, 1, RL) / best_load(1, 1)[1])

v.check("Ex 06-09.1a", best_load(10, 8)[1])
v.check("Ex 06-09.1b", load_power(10, 8, 4))
v.check("Ex 06-09.1c", 100 * efficiency(8, 4))
v.check("Ex 06-09.1d", load_power(10, 8, 16))
v.check("Ex 06-09.1e", 100 * efficiency(8, 16))
v.check("Ex 06-09.1f", 100 * load_power(10, 8, 16) / best_load(10, 8)[1])

RLb, pb = best_load(12, 0.1)
v.check("Ex 06-09.2a", pb)
v.check("Ex 06-09.2b", 12 / (0.1 + RLb))
RL95 = brentq(lambda r: efficiency(0.1, r) - 0.95, 0.01, 100)
v.check("Ex 06-09.2c", RL95)
v.check("Ex 06-09.2d", load_power(12, 0.1, RL95))
v.check("Ex 06-09.2e", (12 / (0.1 + RL95)) ** 2 * 0.1)
v.check("Ex 06-09.2f", 12 / (0.1 + RL95))

RL3, p3 = best_load(-4.0, 10 / 11)                 # kOhm, V -> mW
v.check("Ex 06-09.3a", 1e3 * RL3)
v.check("Ex 06-09.3b", p3)

vt = minimize_scalar(lambda x: -x * (0.5 - x) / 2.0, bounds=(0, 0.5), method="bounded", options={"xatol": 1e-12}).x
v.check("Ex 06-09.4a", 1e3 * vt * (0.5 - vt) / 2.0)
v.check("Ex 06-09.4b", vt)
v.check("Ex 06-09.4c", 1e3 * (0.5 - vt) / 2.0)
v.check("Ex 06-09.4d", 1e3 * 0.4 * 0.1 / 2.0)
v.check("Ex 06-09.4e", 1e3 * 0.1 * 0.4 / 2.0)
v.check("Ex 06-09.4f", 100 * (0.4 * 0.1 / 2.0) / (vt * (0.5 - vt) / 2.0))

# coax: fixed outer radius b = 1; inner radius a = 1/x
loss = lambda a: (1 / a + 1.0) / np.log(1.0 / a)   # skin resistance (1/a + 1/b) over ln(b/a)  # noqa: E731
cap = lambda a: (a * np.log(1.0 / a)) ** 2 / np.log(1.0 / a)  # V_max^2/Z0 with E_max = 1  # noqa: E731
a_loss = minimize_scalar(loss, bounds=(0.05, 0.9), method="bounded", options={"xatol": 1e-13}).x
a_pow = minimize_scalar(lambda a: -cap(a), bounds=(0.05, 0.95), method="bounded", options={"xatol": 1e-13}).x
Z = lambda a, er=1.0: 60.0 / np.sqrt(er) * np.log(1.0 / a)  # eta0/(2 pi) = 59.96 ohm, rounded to 60 as in the text  # noqa: E731
v.check("Ex 06-09.5a", 1 / a_loss)
v.check("Ex 06-09.5b", Z(a_loss))
v.check("Ex 06-09.5c", 1 / a_pow)
v.check("Ex 06-09.5d", Z(a_pow), tol=0.05)
a50 = np.exp(-50 / 60.0)
v.check("Ex 06-09.5e", 1 / a50)
v.check("Ex 06-09.5f", loss(a50) / loss(a_loss))
v.check("Ex 06-09.5g", cap(a50) / cap(a_pow))
v.check("Ex 06-09.5h", Z(a_loss, 2.25))
v.check("Ex 06-09.5i", np.sqrt(Z(a_loss) * Z(a_pow)), tol=0.01)
v.check("Ex 06-09.5j", np.sqrt(77 * 30))
v.check("Ex 06-09.5k", (Z(a_loss) + Z(a_pow)) / 2)
v.check("Ex 06-09.5l", (1 + 1 / a50) / np.log(1 / a50))
v.check("Ex 06-09.5m", np.log(1 / a50) * a50 ** 2)
v.check("Ex 06-09.5n", 100 * cap(np.exp(-75 / 60.0)) / cap(a_pow))
# T 06-09.j-m: extra conductor loss at a given impedance in a given dielectric (fixed outer radius):
# the inner radius follows from Z0 = (60/sqrt(er)) ln(b/a); loss per meter ∝ sqrt(er)(1/a + 1/b)/ln(b/a),
# and the sqrt(er) factor is common to the cable and its optimum, so it cancels in the ratio.
def extra_loss(Z0, er):
    a = np.exp(-Z0 * np.sqrt(er) / 60.0)
    return 100 * (loss(a) / loss(a_loss) - 1)


v.check("T 06-09.j", extra_loss(75, 1.4))
v.check("T 06-09.k", extra_loss(50, 1.4))
v.check("T 06-09.l", extra_loss(50, 2.25))
v.check("T 06-09.m", extra_loss(75, 2.25))
# T 06-09.f-i: the counterexample, solved as a circuit (10 V, 1 kΩ series, 1 kΩ shunt; kΩ, mA, mW)
def cx(RL):
    g = 1 / 1.0 + 1 / 1.0 + (1 / RL if RL else 0.0)   # series 1 kΩ, shunt 1 kΩ, load
    vout = (10 / 1.0) / g                      # nodal equation at the output node
    return vout, 10 * (10 - vout) / 1.0        # output voltage, power from the 10 V source
voc_cx = cx(None)[0]
rth_cx = voc_cx / (10 / 1.0)                   # V_oc / I_sc
vm, psrc = cx(rth_cx)
v.check("T 06-09.f", vm ** 2 / rth_cx)
v.check("T 06-09.g", psrc)
v.check("T 06-09.h", 100 * (vm ** 2 / rth_cx) / psrc)
v.check("T 06-09.i", cx(None)[1])
v.assert_true("Ex 06-09.5 optimal ratios: ln x = 1 + 1/x and x = sqrt(e)",
              abs(np.log(1 / a_loss) - 1 - a_loss) < 1e-6 and abs(1 / a_pow - np.sqrt(np.e)) < 1e-6)

# ================================================================ solutions
RL1, p1 = best_load(6, 300)
v.check("06-09.1a", 1e3 * p1)
v.check("06-09.1b", RL1)
v.check("06-09.1c", 1e3 * load_power(6, 300, 100))
v.check("06-09.1d", 1e3 * load_power(6, 300, 900))

v.check("06-09.2a", 100 * efficiency(1, 4))
v.check("06-09.2b", load_power(1, 1, 4) / best_load(1, 1)[1])

RL3s, p3s = best_load(0.010 * 2000, 2000)          # Norton -> Thevenin
v.check("06-09.3a", 1e-3 * RL3s)
v.check("06-09.3b", 0.010 * 2000 * RL3s / (2000 + RL3s))
v.check("06-09.3c", 1e3 * p3s)

v.check("06-09.4a", best_load(4, 3)[1])
RLm, pm = best_load(119.0476, 1.0238095)           # mV, kOhm -> uW (mV^2 / kOhm = nW... rescale)
v.check("06-09.4b", pm * 1e-3)
v.check("06-09.4c", RLm)

RL5, p5 = best_load(48, 0.25)
v.check("06-09.5a", p5)
v.check("06-09.5b", 48 / (0.25 + RL5))
RL595 = brentq(lambda r: efficiency(0.25, r) - 0.95, 0.01, 1000)
v.check("06-09.5c", RL595)
v.check("06-09.5d", load_power(48, 0.25, RL595))
v.check("06-09.5e", 48 / (0.25 + RL595))
v.check("06-09.5f", 48 - 30 * 0.25)
v.check("06-09.5g", 30 * (48 - 30 * 0.25))
v.check("06-09.5h", 100 * (48 - 30 * 0.25) / 48)
v.check("06-09.5i", 30 ** 2 * 0.25)

Rmax = brentq(lambda r: 5 - 2 * r - 4.75, 0, 1)
v.check("06-09.6a", Rmax)
v.check("06-09.6b", 100 * 4.75 / 5)
Rdev = 4.75 / 2.0
v.check("06-09.6c", 5 * Rdev / (Rdev + Rdev))

RL7, p7 = best_load(0.9665071770334929, 0.03349282296650718)
v.check("06-09.7a", 1e3 * RL7)
v.check("06-09.7b", p7)

for ids, RL in (("ab", 100.0), ("cd", 60.0)):
    vl = 1.0 * RL / (-50.0 + RL)
    v.check(f"06-09.8{ids[0]}", vl)
    v.check(f"06-09.8{ids[1]}", 1e3 * vl ** 2 / RL)

for ident, Voc in (("a", 0.8), ("b", 0.4)):
    v.check(f"06-09.9{ident}", 1e3 * best_load(Voc, 4.0)[1])
v.check("06-09.9c", 1e3 * 0.4 * (0.4 - 0.4) / 4.0, tol=1e-12)
v.assert_true("06-09.9 fixed 4 ohm load is optimal at both temperatures",
              all(abs(best_load(Voc, 4.0)[0] - 4.0) < 1e-6 for Voc in (0.8, 0.4)))

v.check("06-09.10a", Z(a_loss, 2.1))
v.check("06-09.10b", Z(a_pow, 2.1))
a50p = np.exp(-50 * np.sqrt(2.1) / 60.0)
v.check("06-09.10c", 1 / a50p)
v.check("06-09.10d", loss(a50p) / loss(a_loss))
v.check("06-09.10e", cap(a50p) / cap(a_pow))

v.check("06-09.11a", 100 * efficiency(0.05, 8.0))
v.check("06-09.11b", 8.0 / 0.05)

# two sources: equivalent from two loaded nodal solves
def node_v(RL):
    G = 1 / 4 + 1 / 3 + 1 / RL
    return (12 / 4 + 6 / 3) / G


v1, v2 = node_v(1.0), node_v(10.0)
i1, i2 = v1 / 1.0, v2 / 10.0
Req = -(v2 - v1) / (i2 - i1)
Veq = v1 + Req * i1
v.check("06-09.12a", Veq)
v.check("06-09.12b", Req)
RL12, p12 = best_load(Veq, Req)
v.check("06-09.12c", p12)
vm = node_v(RL12)
v.check("06-09.12d", vm)
v.check("06-09.12e", (12 - vm) / 4)
v.check("06-09.12f", (6 - vm) / 3)

# ================================================================ lab
v.check("Lab 06-09.a", 100 * load_power(10, 8, 16) / best_load(10, 8)[1])
VT = 0.025852
IL, I0, n = 50e-3, 1e-9, 1.5
i_solar = lambda x: IL - I0 * np.expm1(x / (n * VT))  # noqa: E731
voc = brentq(i_solar, 0.1, 1.0, xtol=1e-15)
v.check("Lab 06-09.b", voc)
res = minimize_scalar(lambda x: -x * i_solar(x), bounds=(0, voc), method="bounded", options={"xatol": 1e-12})
v.check("Lab 06-09.c", res.x)
v.check("Lab 06-09.d", -1e3 * res.fun)
v.check("Lab 06-09.e", 100 * res.x / voc)
v.check("Lab 06-09.f", 100 * (voc / 2) * i_solar(voc / 2) / -res.fun)
lo = brentq(lambda e: 4 * e * (1 - e) - 0.5, 0.0, 0.5)
hi = brentq(lambda e: 4 * e * (1 - e) - 0.5, 0.5, 1.0)
v.check("Lab 06-09.g", 100 * lo)
v.check("Lab 06-09.h", 100 * hi)
v.check("Lab 06-09.i", Z(a_loss, 1.4))

sys.exit(v.finish())
