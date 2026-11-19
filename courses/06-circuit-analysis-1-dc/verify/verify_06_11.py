#!/usr/bin/env python3
"""Verify every number published in chapter 06-11, its solutions and its lab handout.

Independent routes. The text uses closed forms: the loading ratio R_th/(R_th + R_in), the burden
ratio, the four-wire formula, R = rho L/A with the AWG diameter formula, and worst-case products of
tolerances. This script instead solves every circuit with a sparse-tableau solver (meters as the
resistors they are, a remote-sense supply as an error amplifier), finds unknowns by root-finding on
those solves (the source resistance for a given error, the Thevenin pair from two readings, the
longest cable), evaluates temperature drift by re-solving with temperature-dependent resistors,
searches all tolerance corners for worst cases, and obtains the Monte Carlo statistics of the bus
monitor from the exact (linearized) distribution by numerical convolution.
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, fsolve

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C_DIR = HERE.parent
v = Verifier.from_files("06-11", C_DIR / "chapters" / "06-11-practical-dc-circuits-and-measurement.md",
                        C_DIR / "solutions" / "06-11-solutions.md", C_DIR / "labs" / "06-11-lab" / "README.md")

RHO_CU, ALPHA_CU = 1.7241e-8, 0.00393   # IACS copper at 20 °C (Ω·m, 1/°C)


def tableau(elements):
    """Sparse tableau with dependent sources. Each element is (name, kind, a, b, value) where
    branch current flows a -> b through the element and branch voltage is v_a - v_b:
      R: v = value * i;  I: i = value;  V: v = value;
      G: i = g * (v_c - v_d) with value = (c, d, g);   E: v = mu * (v_c - v_d) with value = (c, d, mu);
      F: i = beta * i_ctrl with value = (ctrl, beta);  H: v = r * i_ctrl with value = (ctrl, r)."""
    nodes = sorted({n for _, _, a, b, _ in elements for n in (a, b) if n != "0"})
    nn, nb = len(nodes), len(elements)
    idx = {n: k for k, n in enumerate(nodes)}
    bidx = {el[0]: k for k, el in enumerate(elements)}
    A = np.zeros((nn, nb))
    for k, (_, _, a, b, _) in enumerate(elements):
        if a != "0":
            A[idx[a], k] += 1.0
        if b != "0":
            A[idx[b], k] -= 1.0
    size = nn + 2 * nb
    M, z = np.zeros((size, size)), np.zeros(size)
    M[:nn, nn:nn + nb] = A
    M[nn:nn + nb, :nn] = -A.T
    M[nn:nn + nb, nn + nb:] = np.eye(nb)

    def node_col(n):
        return None if n == "0" else idx[n]

    for k, (_, kind, _, _, val) in enumerate(elements):
        r = nn + nb + k
        ci, cv = nn + k, nn + nb + k
        if kind == "R":
            M[r, cv], M[r, ci] = 1.0, -val
        elif kind == "I":
            M[r, ci], z[r] = 1.0, val
        elif kind == "V":
            M[r, cv], z[r] = 1.0, val
        elif kind in "GE":
            c, d, gain = val
            M[r, ci if kind == "G" else cv] = 1.0
            for node, sgn in ((c, -1.0), (d, 1.0)):
                if node_col(node) is not None:
                    M[r, node_col(node)] += sgn * gain
        elif kind in "FH":
            ctrl, gain = val
            M[r, ci if kind == "F" else cv] = 1.0
            M[r, nn + bidx[ctrl]] -= gain
        else:
            raise ValueError(kind)
    x = np.linalg.solve(M, z)
    e = {"0": 0.0, **{n: x[idx[n]] for n in nodes}}
    cur = {el[0]: x[nn + k] for k, el in enumerate(elements)}
    vol = {el[0]: x[nn + nb + k] for k, el in enumerate(elements)}
    return e, cur, vol


# Units: ohms, volts, amps unless a name says otherwise.

def voltmeter(Vth, Rth, Rin):
    """Reading of a voltmeter (input resistance Rin) on a Thevenin source, by tableau solve."""
    e, _, _ = tableau([("V", "V", "a", "0", Vth), ("Rth", "R", "a", "m", Rth), ("Rin", "R", "m", "0", Rin)])
    return e["m"]


def ammeter(Vs, RA, RL):
    """Current through a load with an ammeter (internal resistance RA) in series."""
    _, c, _ = tableau([("V", "V", "a", "0", Vs), ("RA", "R", "a", "b", RA), ("RL", "R", "b", "0", RL)])
    return c["RL"]


# ================================================================ examples
# ---- Example 06-11.1: 10 V into 1M/1M
e0, _, _ = tableau([("V", "V", "a", "0", 10.0), ("R1", "R", "a", "m", 1e6), ("R2", "R", "m", "0", 1e6)])
Vth1 = e0["m"]
Rth1 = Vth1 / tableau([("V", "V", "a", "0", 10.0), ("R1", "R", "a", "m", 1e6), ("R2", "R", "m", "0", 1e6),
                       ("Rs", "R", "m", "0", 1e-9)])[1]["Rs"]           # V_oc / I_sc
v.check("Ex 06-11.1a", Rth1 / 1e3)


def divider_read(Rin):
    return tableau([("V", "V", "a", "0", 10.0), ("R1", "R", "a", "m", 1e6), ("R2", "R", "m", "0", 1e6),
                    ("Rin", "R", "m", "0", Rin)])[0]["m"]


r10M, r10G = divider_read(10e6), divider_read(10e9)
v.check("Ex 06-11.1b", r10M)
v.check("Ex 06-11.1c", 100 * (r10M / Vth1 - 1))
v.check("Ex 06-11.1d", r10G)
v.check("Ex 06-11.1e", 1e6 * (r10G / Vth1 - 1))
v.check("Ex 06-11.1f", r10M * (1 + Rth1 / 10e6))

# ---- Example 06-11.2
i0 = ammeter(3.3, 0.0, 33.0)
im = ammeter(3.3, 1.8, 33.0)
ia = ammeter(3.3, 0.05, 33.0)
v.check("Ex 06-11.2a", 1e3 * i0)
v.check("Ex 06-11.2b", 1e3 * im)
v.check("Ex 06-11.2c", 100 * (im / i0 - 1))
v.check("Ex 06-11.2d", 1e3 * im * 1.8)
v.check("Ex 06-11.2e", 1e3 * ia)
v.check("Ex 06-11.2f", 1e3 * ia * 0.05)
v.check("Ex 06-11.2g", 1e3 * im * (1 + 1.8 / 33.0))


# ---- Example 06-11.3: ±(0.05% + 1 count)
def unc(reading, count):
    return 0.0005 * abs(reading) + count


v.check("Ex 06-11.3a", 1e3 * unc(3.300, 1e-3))
v.check("Ex 06-11.3b", 100 * unc(3.300, 1e-3) / 3.300)
v.check("Ex 06-11.3c", 1e3 * unc(0.300, 1e-3))
v.check("Ex 06-11.3d", 100 * unc(0.300, 1e-3) / 0.300)
v.check("Ex 06-11.3e", 1e3 * unc(0.3000, 1e-4))
v.check("Ex 06-11.3f", 100 * unc(0.3000, 1e-4) / 0.3000)
eV, eI = unc(3.300, 1e-3) / 3.300, 0.005
# worst case by evaluating the product at the error corners (exact, not the first-order sum)
worstP = max(abs((1 + a * eV) * (1 + b * eI) - 1) for a in (-1, 1) for b in (-1, 1))
v.check("Ex 06-11.3g", 100 * worstP)
v.check("Ex 06-11.3h", 100 * math.hypot(eV, eI))


# ---- Example 06-11.4: two-wire and four-wire
def two_wire(R, lead, I=10e-3):
    e, _, _ = tableau([("I", "I", "0", "t", I), ("L1", "R", "t", "x", lead), ("R", "R", "x", "y", R),
                       ("L2", "R", "y", "0", lead)])
    return e["t"] / I


def four_wire(R, lead, Rin, I=10e-3):
    e, _, _ = tableau([("I", "I", "0", "f", I), ("F1", "R", "f", "x", lead), ("R", "R", "x", "y", R),
                       ("F2", "R", "y", "0", lead), ("S1", "R", "x", "s1", lead), ("S2", "R", "y", "s2", lead),
                       ("Rin", "R", "s1", "s2", Rin)])
    return (e["s1"] - e["s2"]) / I, e["s1"] - e["s2"]


v.check("Ex 06-11.4a", two_wire(1.0, 0.08))
v.check("Ex 06-11.4b", 100 * (two_wire(1.0, 0.08) - 1.0))
r4w, vs4 = four_wire(1.0, 0.08, 10e6)
v.check("Ex 06-11.4c", r4w)
v.check("Ex 06-11.4d", 1e3 * vs4)
v.check("Ex 06-11.4e", 1e6 * (r4w - 1.0))
v.assert_true("Ex 4: four-wire independent of force-lead resistance",
              abs(four_wire(1.0, 5.0, 10e6)[0] - four_wire(1.0, 0.08, 10e6)[0]) < 1e-6)


# ---- Example 06-11.5: shunt with copper, solved at two temperatures
def shunt(T, I=20.0):
    """Returns (Kelvin reading, misplaced-tap reading) in ohms at board temperature T (°C), calibrated at 25 °C."""
    rcu = 0.05e-3 * (1 + ALPHA_CU * (T - 25))
    rsh = 1e-3 * (1 + 250e-6 * (T - 25))                 # worst-case (positive) TCR
    e, _, _ = tableau([("I", "I", "0", "x", I), ("C1", "R", "x", "k1", rcu), ("S", "R", "k1", "k2", rsh),
                       ("C2", "R", "k2", "0", rcu)])
    return (e["k1"] - e["k2"]) / I, e["x"] / I


k25, m25 = shunt(25.0)
k75, m75 = shunt(75.0)
v.check("Ex 06-11.5a", 1e3 * 20 * k25)
v.check("Ex 06-11.5b", 20 ** 2 * k25)
v.check("Ex 06-11.5c", 1e3 * m25)
v.check("Ex 06-11.5d", 100 * (m25 / 1e-3 - 1))
v.check("Ex 06-11.5e", 100 * (k75 / k25 - 1))
v.check("Ex 06-11.5f", 100 * (m75 / m25 - 1))
v.check("Ex 06-11.5g", 1e6 * (m75 / m25 - 1) / 50)


# ---- Example 06-11.6: AWG wire and remote sensing
def awg_diameter_mm(n):
    """AWG: 36 gauge is 0.005 in and 0000 (n = -3) is 0.46 in, in geometric steps (ASTM B258)."""
    d36, d0000 = 0.005, 0.46
    return 25.4 * d36 * (d0000 / d36) ** ((36 - n) / 39)


d16 = awg_diameter_mm(16)
r16 = RHO_CU / (math.pi * (d16 * 1e-3) ** 2 / 4)       # Ω/m
v.check("Ex 06-11.6a", d16)
v.check("Ex 06-11.6b", 1e3 * r16)
Rloop = 2 * 1.5 * r16
v.check("Ex 06-11.6c", 1e3 * Rloop)
e6, c6, vb6 = tableau([("V", "V", "s", "0", 12.0), ("Wp", "R", "s", "lp", 1.5 * r16), ("Ld", "I", "lp", "ln", 10.0),
                       ("Wn", "R", "ln", "0", 1.5 * r16)])
v.check("Ex 06-11.6d", e6["lp"] - e6["ln"])
v.check("Ex 06-11.6e", 10.0 ** 2 * Rloop)
# remote sense: an error amplifier of gain 1e9 regulates (sense+ - sense-) to 12 V; sense wires 0.5 Ω into 1 GΩ
e6s, _, _ = tableau([("Vr", "V", "r", "0", 12.0), ("Ed", "E", "d", "0", ("sp", "sn", 1.0)),
                     ("Ea", "E", "s", "0", ("r", "d", 1e9)), ("Wp", "R", "s", "lp", 1.5 * r16),
                     ("Ld", "I", "lp", "ln", 10.0), ("Wn", "R", "ln", "0", 1.5 * r16),
                     ("Sp", "R", "lp", "sp", 0.5), ("Sn", "R", "ln", "sn", 0.5), ("Rs", "R", "sp", "sn", 1e9)])
v.check("Ex 06-11.6f", e6s["s"])
v.assert_true("Ex 6: load regulated to 12 V", abs(e6s["lp"] - e6s["ln"] - 12.0) < 1e-6)

# ================================================================ solutions
v.check("06-11.1a", voltmeter(10.0, 100e3, 10e6))
v.check("06-11.1b", 100 * (voltmeter(10.0, 100e3, 10e6) / 10 - 1))
v.check("06-11.1c", voltmeter(10.0, 100e3, 10e9))
v.check("06-11.1d", 1e6 * (voltmeter(10.0, 100e3, 10e9) / 10 - 1))

i2 = ammeter(1.5, 2.0, 15.0)
v.check("06-11.2a", 1e3 * i2)
v.check("06-11.2b", 100 * (i2 / ammeter(1.5, 0.0, 15.0) - 1))
v.check("06-11.2c", 1e3 * i2 * 2.0)
v.check("06-11.2d", 1e3 * i2 * (1 + 2.0 / 15.0))

v.check("06-11.3a", 1e3 * unc(12.47, 0.01))
v.check("06-11.3b", 100 * unc(12.47, 0.01) / 12.47)

# Problem 4: find (Vth, Rth) so that tableau solves reproduce the two readings
sol4 = fsolve(lambda p: [voltmeter(p[0], p[1] * 1e6, 10e6) - 4.5, voltmeter(p[0], p[1] * 1e6, 5e6) - 4.0], [5.0, 1.0],
              xtol=1e-13)
v.check("06-11.4a", sol4[1])
v.check("06-11.4b", sol4[0])

v.check("06-11.5a", 1e3 * 50e-3 / 5.0)
v.check("06-11.5b", 5.0 ** 2 * 10e-3)
v.check("06-11.5c", 1e3 * 5.0 * 1e-3)
v.check("06-11.5d", 1e3 * 5.0 ** 2 * 1e-3)
v.check("06-11.5e", 100 * 50e-6 / (5.0 * 10e-3))
v.check("06-11.5f", 100 * 50e-6 / (5.0 * 1e-3))

t1oz = 35e-6
Rsq = RHO_CU / t1oz
v.check("06-11.6a", 1e3 * Rsq)
v.check("06-11.6b", 40.0 / 0.5)
R6 = RHO_CU * 40e-3 / (0.5e-3 * t1oz)                  # from the volume formula, not squares
v.check("06-11.6c", 1e3 * R6)
v.check("06-11.6d", 1e3 * 2 * R6)
v.check("06-11.6e", 1e3 * 2 ** 2 * R6)
v.check("06-11.6f", 1e3 * R6 * (1 + ALPHA_CU * (85 - 20)))

v.check("06-11.7a", 1e3 * 3 * 0.02)
v.check("06-11.7b", 100 * 3 * 0.02 / 1.0)

v.check("06-11.8a", 1e3 * two_wire(10e-3, 0.05, I=1.0))
v.check("06-11.8b", two_wire(10e-3, 0.05, I=1.0) / 10e-3)
v.check("06-11.8c", 1e3 * four_wire(10e-3, 0.05, 10e6, I=1.0)[1])


# Problem 9: 48 V monitor
def monitor(R1, R2, Rin=None, V=48.0):
    els = [("V", "V", "a", "0", V), ("R1", "R", "a", "m", R1), ("R2", "R", "m", "0", R2)]
    if Rin is not None:
        els.append(("Rin", "R", "m", "0", Rin))
    return tableau(els)[0]["m"]


nom = monitor(140e3, 10e3)
v.check("06-11.9a", nom)
loaded = monitor(140e3, 10e3, 1e6)
v.check("06-11.9b", 100 * (loaded / nom - 1))
v.check("06-11.9c", loaded)


def ratio_corners(t):
    return [monitor(140e3 * (1 + a * t), 10e3 * (1 + b * t)) / nom - 1 for a in (-1, 1) for b in (-1, 1)]


c1 = ratio_corners(0.01)
v.check("06-11.9d", 100 * max(c1))
v.check("06-11.9e", 100 * min(c1))
tot1 = [(1 + c) * (1 + s * 0.005) - 1 for c in c1 for s in (-1, 1)]
v.check("06-11.9f", 100 * max(tot1))
v.check("06-11.9g", 100 * min(tot1))
c01 = ratio_corners(0.001)
v.check("06-11.9h", 100 * max(abs(c) for c in c01))
tot01 = [(1 + c) * (1 + s * 0.005) - 1 for c in c01 for s in (-1, 1)]
v.check("06-11.9i", 100 * max(tot01))
v.check("06-11.9j", 100 * min(tot01))

v.check("06-11.10a", 1e3 * 0.5 / 10.0)
len16 = brentq(lambda L: 10.0 * 2 * L * r16 - 0.5, 0.01, 100.0, xtol=1e-12)
v.check("06-11.10b", len16)
d14 = awg_diameter_mm(14)
r14 = RHO_CU / (math.pi * (d14 * 1e-3) ** 2 / 4)
v.check("06-11.10c", d14)
v.check("06-11.10d", 1e3 * r14)
v.check("06-11.10e", brentq(lambda L: 10.0 * 2 * L * r14 - 0.5, 0.01, 100.0, xtol=1e-12))

THETA = 50.0     # °C/W on this board
v.check("06-11.11a", 15 ** 2 * 2e-3)
v.check("06-11.11b", THETA * 15 ** 2 * 2e-3)
v.check("06-11.11c", 100 * 250e-6 * THETA * 15 ** 2 * 2e-3)
v.check("06-11.11d", 15 ** 2 * 5e-3)
v.assert_true("11: 5 mΩ exceeds the 1.0 W rating", 15 ** 2 * 5e-3 > 1.0)
v.check("06-11.11e", THETA * 15 ** 2 * 3e-3)
v.check("06-11.11f", 100 * 75e-6 * THETA * 15 ** 2 * 3e-3)
v.check("06-11.11g", 1e3 * 15 * 3e-3)
v.check("06-11.11h", 1e3 * 15 * 2e-3)

# Problem 12: three 1 MΩ across 9 V
chain = [("V", "V", "a", "0", 9.0), ("R1", "R", "a", "b", 1e6), ("R2", "R", "b", "c", 1e6), ("R3", "R", "c", "0", 1e6)]
voc = tableau(chain)[0]
isc = tableau(chain + [("S", "R", "b", "c", 1e-9)])[1]["S"]
v.check("06-11.12a", (voc["b"] - voc["c"]) / isc / 1e3)
reads = []
for (p, q) in (("a", "b"), ("b", "c"), ("c", "0")):
    e = tableau(chain + [("M", "R", p, q, 10e6)])[0]
    reads.append(e[p] - e.get(q, 0.0))
v.check("06-11.12b", reads[1])
v.assert_true("12: the three loaded readings are equal", max(reads) - min(reads) < 1e-9)
v.check("06-11.12c", sum(reads))
e = tableau(chain + [("M", "R", "b", "c", 10e9)])[0]
v.check("06-11.12d", e["b"] - e["c"])
e_all = tableau(chain + [("M1", "R", "a", "b", 10e6), ("M2", "R", "b", "c", 10e6), ("M3", "R", "c", "0", 10e6)])[0]
v.assert_true("12: three meters at once read 3 V each", abs(e_all["b"] - e_all["c"] - 3.0) < 1e-9)

# ---- Problem 06-11.13: re-solve the shunt circuit at two temperatures (Ω, A)
def shunt13(T, I=10.0):
    rcu = 0.02e-3 * (1 + ALPHA_CU * (T - 25))
    rsh = 2e-3 * (1 + 250e-6 * (T - 25))
    e, _, _ = tableau([("I", "I", "0", "x", I), ("C1", "R", "x", "k1", rcu), ("S", "R", "k1", "k2", rsh),
                       ("C2", "R", "k2", "0", rcu)])
    return (e["k1"] - e["k2"]) / I, e["x"] / I


k0, m0 = shunt13(25.0)
k40, m40 = shunt13(65.0)
v.check("06-11.13a", 1e3 * m0)
v.check("06-11.13b", 100 * (m0 / 2e-3 - 1))
v.check("06-11.13c", 1e6 * (m40 / m0 - 1) / 40)
v.check("06-11.13d", 100 * (m40 / m0 - 1))
v.check("06-11.13e", 100 * (k40 / k0 - 1))
terms = np.array([0.5, 1.0, 0.3, 0.2])
v.check("06-11.13f", max(abs(np.dot(terms, s)) for s in itertools.product((-1, 1), repeat=4)))
v.check("06-11.13g", math.sqrt(np.sum(terms ** 2)))

# ================================================================ lab
v.check("Lab 06-11.a", brentq(lambda R: voltmeter(1.0, R, 10e6) - 0.99, 1.0, 1e7, xtol=1e-9) / 1e3)
v.check("Lab 06-11.b", brentq(lambda R: voltmeter(1.0, R, 10e9) - 0.99, 1.0, 1e10, xtol=1e-6) / 1e6)
v.check("Lab 06-11.c", 100 * unc(0.6, 1e-3) / 0.6)
v.check("Lab 06-11.d", 100 * unc(6.0, 1e-3) / 6.0)
dT5 = brentq(lambda T: shunt(25 + T)[1] / m25 - 1.05, 1.0, 500.0, xtol=1e-10)
v.check("Lab 06-11.e", dT5)
v.check("Lab 06-11.f", 100 * (shunt(25 + dT5)[0] / k25 - 1))

# Monitor error to first order: (14/15)(e2 - e1) + e3, e1, e2 ~ U(-1%, 1%), e3 ~ U(-0.5%, 0.5%).
x = np.linspace(-0.05, 0.05, 200_001)
dx = x[1] - x[0]
a = (14 / 15) * 0.01
tri = np.clip((2 * a - np.abs(x)) / (4 * a * a), 0, None)       # density of a (u2 - u1), u ~ U(-1, 1)
box = np.where(np.abs(x) <= 0.005, 1 / 0.01, 0.0)
dens = np.convolve(tri, box, mode="same") * dx
v.assert_true("Lab: density integrates to 1", abs(dens.sum() * dx - 1) < 1e-6)
v.check("Lab 06-11.g", 100 * dens[np.abs(x) > 0.015].sum() * dx)
v.check("Lab 06-11.h", 100 * math.sqrt(2 * a ** 2 / 3 + 0.005 ** 2 / 3))
v.check("Lab 06-11.i", brentq(lambda R: ammeter(1.0, 1.8, R) / ammeter(1.0, 0.0, R) - 0.99, 1.0, 1e5, xtol=1e-10))
v.check("Lab 06-11.j", 1e6 * ((5e-3 * 35e-6 + 0.1e-3 * ALPHA_CU) / 5.1e-3))
v.assert_true("Lab: 0.1% resistors cannot exceed 1.5%", max(abs(t) for t in tot01) < 0.015)
v.check("Lab 06-11.k", 0.0)

v.finish()
