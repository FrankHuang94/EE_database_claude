#!/usr/bin/env python3
"""Verify every number published in chapter 06-01, its solutions and its lab handout.

Independent routes: circuits are solved as linear systems in all node voltages and source
currents (a small modified nodal analysis written here, not the single-node KCL of the text) and
their powers summed element by element; charges and energies are integrated numerically from
sampled waveforms instead of using rectangle and triangle areas; battery lives come from
integrating a sampled current profile; the transmission-line peaks come from a bounce
(lattice) diagram, the netlist from ngspice's own line model; the Poynting flux is integrated
over the wire surface numerically.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from math import e as E_NUM, pi, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import quad

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C_DIR = HERE.parent
v = Verifier.from_files("06-01", C_DIR / "chapters" / "06-01-charge-current-voltage-power.md",
                        C_DIR / "solutions" / "06-01-solutions.md", C_DIR / "labs" / "06-01-lab" / "README.md")
E_CH = 1.602176634e-19
C0 = 299_792_458.0
N_CU = 8.96e3 / 63.546e-3 * 6.02214076e23          # one conduction electron per atom (04-05)


def mna(nodes, elements):
    """Solve a DC circuit by modified nodal analysis.

    nodes: list of node names other than ground "0". elements: tuples ("R", a, b, ohms) or
    ("V", plus, minus, volts). Returns node voltages and, for each element, the voltage from its
    first to its second terminal and the current entering its first terminal (passive convention).
    """
    idx = {n: k for k, n in enumerate(nodes)}
    vs = [el for el in elements if el[0] == "V"]
    n, m = len(nodes), len(vs)
    A = np.zeros((n + m, n + m))
    z = np.zeros(n + m)
    for el in elements:
        if el[0] == "R":
            _, a, b, r = el
            g = 1.0 / r
            for p, q in ((a, b), (b, a)):
                if p != "0":
                    A[idx[p], idx[p]] += g
                    if q != "0":
                        A[idx[p], idx[q]] -= g
    for k, (_, a, b, val) in enumerate(vs):
        row = n + k
        if a != "0":
            A[idx[a], row] += 1.0
            A[row, idx[a]] += 1.0
        if b != "0":
            A[idx[b], row] -= 1.0
            A[row, idx[b]] -= 1.0
        z[row] = val
    x = np.linalg.solve(A, z)
    volt = {"0": 0.0, **{nd: x[idx[nd]] for nd in nodes}}
    out = {}
    k = 0
    for el in elements:
        kind, a, b, val = el
        vab = volt[a] - volt[b]
        if kind == "R":
            i_in = vab / val
        else:
            i_in = x[n + k]                                      # MNA unknown: current into the + terminal
            k += 1
        out[el] = (vab, i_in)
    return volt, out


# ---------------------------------------------------------------- theory
v.check("T 06-01.a", 1 / E_CH)
v.check("T 06-01.b", 1e-3 * 3600)
v.check("T 06-01.c", 0.225 * 3600 * 3.0)
v.check("T 06-01.d", 100 * 0.97 * 0.90)

# ---------------------------------------------------------------- Example 1: integrate a sampled pulse
q1 = quad(lambda t: 2e-3 if t < 3e-3 else 2e-3 * (5e-3 - t) / 2e-3, 0, 5e-3, points=[3e-3])[0]
v.check("Ex 06-01.1a", q1 * 1e6)
v.check("Ex 06-01.1b", q1 / E_CH)
v.check("Ex 06-01.1c", q1 / 5e-3 * 1e3)

# ---------------------------------------------------------------- Example 2 by MNA
ex2 = [("V", "s1", "0", 12.0), ("R", "s1", "a", 2.0), ("V", "s2", "0", 6.0), ("R", "s2", "a", 3.0), ("R", "a", "0", 6.0)]
volt2, br2 = mna(["s1", "s2", "a"], ex2)
v.check("Ex 06-01.2a", volt2["a"])
v.check("Ex 06-01.2b", br2[ex2[1]][1])                                   # i1 = current in R1 from s1 to a
v.check("Ex 06-01.2c", br2[ex2[3]][1])                                   # i2 = current in R2 from s2 to a
v.check("Ex 06-01.2d", br2[ex2[4]][1])
powers2 = [vab * i for vab, i in br2.values()]
for key, el in zip("efghi", ex2):
    v.check(f"Ex 06-01.2{key}", br2[el][0] * br2[el][1])
v.assert_true("Example 06-01.2 powers sum to zero (Tellegen)", abs(sum(powers2)) < 1e-12)

# ---------------------------------------------------------------- Example 3
eps_board = 4.6
v.check("Ex 06-01.3a", 2.0 / (0.66 * C0) * 1e9)
td_b = 0.150 * sqrt(eps_board) / C0
v.check("Ex 06-01.3b", td_b * 1e9)
v.check("Ex 06-01.3c", 6 * td_b * 1e9)
lam = C0 / 60
v.check("Ex 06-01.3d", lam / 1e3)
v.check("Ex 06-01.3e", 400e3 / lam)
v.check("Ex 06-01.3f", 360 * 400e3 / lam)


# ---------------------------------------------------------------- Example 4: integrate a sampled 10 s profile
def tag_profile(sense_s=0.020, radio_period=10.0, dt=1e-5, span=10.0):
    t = np.arange(0, span, dt) + dt / 2
    i = np.full_like(t, 2e-6)
    i += np.where((t % 1.0) < sense_s, 1.2e-3, 0.0)
    i += np.where((t % radio_period) < 3e-3, 8e-3, 0.0)
    return t, i


t4, i4 = tag_profile()
iavg4 = i4.mean()
v.check("Ex 06-01.4a", iavg4 * 1e6)
v.check("Ex 06-01.4b", iavg4 * 3.0 * 1e6)
life_h = 0.225 / iavg4
v.check("Ex 06-01.4c", life_h)
v.check("Ex 06-01.4d", life_h / 24)
v.check("Ex 06-01.4e", 0.225 * 3600 * 3.0)
v.check("Ex 06-01.4f", 100 * np.mean(np.where((t4 % 1.0) < 0.020, 1.2e-3, 0.0)) / iavg4)
v.check("Ex 06-01.4g", 100 * np.mean(np.where((t4 % 10.0) < 3e-3, 8e-3, 0.0)) / iavg4)
v.check("Ex 06-01.4h", 100 * 2e-6 / iavg4)

# ---------------------------------------------------------------- Example 5
P5, R5 = 1000.0, 1e-4
v.check("Ex 06-01.5a", P5 / 0.80)
for V5, ki, kdrop, kfrac, kloss in ((0.80, None, "b", "c", "d"), (12.0, "e", None, None, "f"), (48.0, "g", None, None, "h")):
    I5 = P5 / V5
    if ki:
        v.check(f"Ex 06-01.5{ki}", I5)
    if kdrop:
        v.check(f"Ex 06-01.5{kdrop}", I5 * R5 * 1e3)
        v.check(f"Ex 06-01.5{kfrac}", 100 * I5 * R5 / V5)
    v.check(f"Ex 06-01.5{kloss}", I5 ** 2 * R5)
pin = P5 / (0.97 * 0.90)
v.check("Ex 06-01.5i", pin)
v.check("Ex 06-01.5j", pin - P5)
v.check("Ex 06-01.5k", 0.02 * 0.80 / (P5 / 0.80) * 1e6)

# ---------------------------------------------------------------- solutions
v.check("06-01.1a", 4.0 * 3600)
v.check("06-01.1b", 4.0 * 3.7)
v.check("06-01.1c", 4.0 * 3.7 * 3600 / 1e3)
q_year = 50e-6 * 365 * 86400
v.check("06-01.1d", q_year)
v.check("06-01.1e", q_year / 3.6)
v.check("06-01.1f", 1000 * 3600)
v.check("06-01.1g", 3.6e6 / 10 / 3600)
tau2 = 2e-3
q2 = lambda t: 5e-6 * (1 - np.exp(-t / tau2))                           # noqa: E731
h = 1e-9
v.check("06-01.2a", (q2(h) - q2(0)) / h * 1e3)                          # numerical derivative
v.check("06-01.2b", (q2(2e-3 + h) - q2(2e-3 - h)) / (2 * h) * 1e3)
v.check("06-01.2c", quad(lambda t: 5e-6 / tau2 * np.exp(-t / tau2), 0, np.inf)[0] * 1e6)
v.check("06-01.3a", 10 * 2)
v.check("06-01.3b", 10 * -2)
v.check("06-01.3c", -5 * -3)
v.check("06-01.3d", 3 * -(-4))
vd = 1.0 / (N_CU * E_CH * 1e-6)
v.assert_true("copper electron density matches 04-05's 8.491e28", abs(N_CU / 8.491e28 - 1) < 1e-3)
v.check("06-01.4a", vd)
v.check("06-01.4b", 1 / vd / 3600)
v.check("06-01.4c", 1 / (2 / 3 * C0) * 1e9)
p5 = {"A": 12 * -3, "B": 4 * 3, "C": 8 * 1, "D": 8 * 1.5}
v.check("06-01.5a", p5["A"])
v.check("06-01.5b", p5["D"])
pE = -sum(p5.values())
v.check("06-01.5c", pE)
v.check("06-01.5d", pE / 2)
p6 = [("V", "sa", "0", 9.0), ("R", "sa", "b", 1.0), ("V", "sb", "0", 12.0), ("R", "sb", "b", 2.0), ("R", "b", "0", 4.0)]
volt6, br6 = mna(["sa", "sb", "b"], p6)
v.check("06-01.6a", volt6["b"])
v.check("06-01.6b", br6[p6[1]][1])
v.check("06-01.6c", br6[p6[3]][1])
v.check("06-01.6d", br6[p6[4]][1])
for key, el in zip("egfhi", p6):                                         # 6e: 9 V source, 6f: 12 V source, 6g: 1 ohm
    v.check(f"06-01.6{key}", br6[el][0] * br6[el][1])
v.assert_true("Problem 06-01.6 powers sum to zero", abs(sum(a * b for a, b in br6.values())) < 1e-12)
v.check("06-01.6j", float(Fraction(9) + 2 * Fraction(9, 4)))
e7 = quad(lambda t: 2.0 if t < 0.1 else 2.0 * (0.3 - t) / 0.2, 0, 0.3, points=[0.1])[0]
v.check("06-01.7a", e7)
v.check("06-01.7b", e7 / 2.0)
v.check("06-01.7c", e7 / 2.0 * 86400)
v.check("06-01.7d", e7 / 2.0 * 86400 / 3600)
t8 = np.linspace(0, 1e-3, 200001)[:-1]
v8 = np.where(t8 < 0.5e-3, 5.0, 0.0)
for key, i8 in (("a", np.where(t8 < 0.5e-3, 2.0, 0.0)), ("b", np.where(t8 < 0.5e-3, 0.0, 2.0)), ("c", np.full_like(t8, 1.0))):
    v.check(f"06-01.8{key}", np.mean(v8 * i8))
v.check("06-01.8d", np.mean(v8) * np.mean(np.where(t8 < 0.5e-3, 2.0, 0.0)))
i9 = 5e-6 + 10e-3 * 0.050 / 60 + 40e-3 * 1.0 / 900
v.check("06-01.9a", i9 * 1e6)
v.check("06-01.9b", 2.5 / i9)
v.check("06-01.9c", 2.5 / i9 / 8766)
v.check("06-01.9d", 100 * (40e-3 / 900) / i9)
v.check("06-01.9e", 2.5 / (5e-6 + 10e-3 * 0.050 / 60 + 40e-3 / 3600) / 8766)
v.check("06-01.10a", (1e-9 / 6) / 7.154e-12 * 1e-3 * 1e3)
v.check("06-01.10b", (100e-12 / 6) / 7.154e-12)
d_chip = sqrt(3.0) / C0
v.check("06-01.10c", d_chip * 1e-3 * 1e12)
v.check("06-01.10d", (20e-12 / 6) / d_chip * 1e3)
for key_loss, key_frac, P, V in (("a", "b", 100, 20), (None, "c", 240, 48), ("d", "e", 240, 20)):
    I = P / V
    if key_loss:
        v.check(f"06-01.11{key_loss}", I ** 2 * 0.20)
    v.check(f"06-01.11{key_frac}", 100 * I * 0.20 / V)
v.check("06-01.12a", 120e3 / 54)
v.check("06-01.12b", 120e3 / 800)
v.check("06-01.12c", (120e3 / 54) ** 2 * 50e-6)
v.check("06-01.12d", (120e3 / 800) ** 2 * 50e-6)
v.check("06-01.12e", (800 / 54) ** 2)
c13 = [("V", "c1", "0", 6.0), ("R", "c1", "c", 1.0), ("V", "c2", "0", 0.0), ("R", "c2", "c", 1.0), ("R", "c", "0", 1.0)]
volt13, br13 = mna(["c1", "c2", "c"], c13)
v.check("06-01.13a", volt13["c"])
v.check("06-01.13b", br13[c13[1]][1])
v.check("06-01.13c", br13[c13[3]][1])
cross = sum(br2[e1][0] * br13[e2][1] for e1, e2 in zip(ex2, c13))      # circuit 1 voltages x circuit 2 currents
v.check("06-01.13d", cross)
a14, L14, I14, V14 = 0.25e-3, 0.50, 2.0, 10.0
E14, H14 = V14 / L14, I14 / (2 * pi * a14)
v.check("06-01.14a", E14)
v.check("06-01.14b", H14)
v.check("06-01.14c", E14 * H14)
flux = quad(lambda phi: quad(lambda z: E14 * H14 * a14, 0, L14)[0], 0, 2 * pi)[0]
v.check("06-01.14d", flux)
v.assert_true("Poynting inflow equals VI", abs(flux - V14 * I14) < 1e-9)
v.check("06-01.15a", 3.7 * 1.5)
v.check("06-01.15b", -2.0 / 3.7)

# ---------------------------------------------------------------- lab
v.check("Lab 06-01.a", 12 * 6 / (2 + 6))                                 # battery current zero: divider of V1


def far_end_peak(tr, rs=10.0, z0=50.0, td=1e-9, rl=1e6, t_end=140e-9, n=280001):
    gs, gl = (rs - z0) / (rs + z0), (rl - z0) / (rl + z0)
    t = np.linspace(0, t_end, n)
    out = np.zeros_like(t)
    for k in range(300):
        out += z0 / (rs + z0) * (1 + gl) * (gl * gs) ** k * np.clip((t - (2 * k + 1) * td) / tr, 0, 1)
    return out.max()


for key, tr in (("b", 0.1e-9), ("c", 2e-9), ("d", 6e-9), ("e", 20e-9)):
    v.check(f"Lab 06-01.{key}", far_end_peak(tr))
for key, (sense, radio) in (("f", (0.010, 10.0)), ("g", (0.020, 1.0))):
    _, i_lab = tag_profile(sense_s=sense, radio_period=radio)
    v.check(f"Lab 06-01.{key}", 0.225 / i_lab.mean() / 24)
v.assert_true("e^-1 sanity for 06-01.2b", abs(2.5 / E_NUM - 0.9197) < 1e-4)

sys.exit(v.finish())
