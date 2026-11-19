#!/usr/bin/env python3
"""Verify every published number in chapter 07-11 (worked examples, practitioner lens), its problem
solutions and its lab handout.

Independent routes: the chapter uses the per-phase equivalent, the sqrt(3) relations and the power
formulas. Here every three-phase circuit is built from its three sources and solved whole by
modified nodal analysis (MNA), without assuming balance or using the per-phase shortcut; total
power is the sum of the three phases' complex powers, the instantaneous power is sampled over a
cycle, harmonic neutral currents are summed from sampled waveforms, and wattmeter readings come from
the solved voltages and currents. ngspice netlists in labs/07-11-lab are run separately.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, fsolve

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "07-11",
    COURSE / "chapters" / "07-11-three-phase-circuits.md",
    COURSE / "solutions" / "07-11-solutions.md",
    COURSE / "labs" / "07-11-lab" / "README.md",
)
pi = math.pi
deg = lambda z: math.degrees(cmath.phase(z))  # noqa: E731
R3 = math.sqrt(3)


def mna(elements):
    """Elements: ("Z", a, b, impedance) or ("V", a, b, phasor). Returns node voltages and V-source
    currents (flowing from a through the source to b)."""
    nodes = sorted({n for e in elements for n in e[1:3] if n != "0"})
    idx = {n: i for i, n in enumerate(nodes)}
    vs = [e for e in elements if e[0] == "V"]
    N, M = len(nodes), len(vs)
    A = np.zeros((N + M, N + M), complex)
    b = np.zeros(N + M, complex)
    for e in elements:
        if e[0] == "Z":
            y = 1 / e[3]
            for p, sp in ((e[1], 1), (e[2], -1)):
                if p == "0":
                    continue
                for q, sq in ((e[1], 1), (e[2], -1)):
                    if q != "0":
                        A[idx[p], idx[q]] += sp * sq * y
    for j, e in enumerate(vs):
        r = N + j
        for p, sp in ((e[1], 1), (e[2], -1)):
            if p != "0":
                A[idx[p], r] += sp
                A[r, idx[p]] += sp
        b[r] = e[3]
    x = np.linalg.solve(A, b)
    V = {n: x[idx[n]] for n in nodes}
    V["0"] = 0.0
    return V, [x[N + j] for j in range(M)]


def y_source(Vp, extra, neutral_name="0"):
    """A Y source with its neutral at ground: line nodes A, B, C."""
    return [("V", "A", neutral_name, Vp), ("V", "B", neutral_name, Vp * cmath.exp(-2j * pi / 3)),
            ("V", "C", neutral_name, Vp * cmath.exp(2j * pi / 3))] + extra


def three_phase_power(V, I_lines, phase_nodes, ref="0"):
    """Total complex power into a load from line currents and line-to-reference voltages (RMS phasors)."""
    return sum((V[n] - V[ref]) * i.conjugate() for n, i in zip(phase_nodes, I_lines))


# ================================================================================ Example 1 (Y-Y, no neutral wire)
Z1 = 8 + 6j
Vp400 = 400 / R3
net1 = y_source(Vp400, [("Z", "A", "N", Z1), ("Z", "B", "N", Z1), ("Z", "C", "N", Z1)])
V1, I1s = mna(net1)
Il1 = [-i for i in I1s]  # current each source delivers into its line
Ia = Il1[0]
v.check("Ex 07-11.1a", abs(V1["A"] - V1["N"]))
v.check("Ex 07-11.1b", abs(Ia))
v.check("Ex 07-11.1c", deg(Ia))
v.check("Ex 07-11.1d", abs(V1["A"] - V1["B"]))
v.check("Ex 07-11.1e", deg(V1["A"] - V1["B"]))
S1 = three_phase_power(V1, Il1, ["A", "B", "C"], ref="N")
v.check("Ex 07-11.1f", abs(S1) / 1e3)
v.check("Ex 07-11.1g", S1.real / 1e3)
v.check("Ex 07-11.1h", S1.imag / 1e3)
v.check("Ex 07-11.1i", S1.real / abs(S1))
v.assert_true("floating star point stays at ground potential", abs(V1["N"]) < 1e-9)
# instantaneous power by sampling (peak values)
t = np.linspace(0, 0.02, 4001)
p = np.zeros_like(t)
for k, n in enumerate(("A", "B", "C")):
    Vk, Ik = (V1[n] - V1["N"]) * math.sqrt(2), Il1[k] * math.sqrt(2)
    p += np.abs(Vk) * np.cos(2 * pi * 50 * t + cmath.phase(Vk)) * np.abs(Ik) * np.cos(2 * pi * 50 * t + cmath.phase(Ik))
v.assert_true("balanced instantaneous power is constant", np.ptp(p) < 1e-6 * p.mean())

# ================================================================================ Example 2 (Delta load)
net2 = y_source(Vp400, [("Z", "A", "B", Z1), ("Z", "B", "C", Z1), ("Z", "C", "A", Z1)])
V2, I2s = mna(net2)
Iab = (V2["A"] - V2["B"]) / Z1
Ia2 = -I2s[0]  # current delivered by source A into line A
v.check("Ex 07-11.2a", abs(Iab))
v.check("Ex 07-11.2b", abs(Ia2))
v.check("Ex 07-11.2c", deg(Ia2) - deg(V2["A"] - V2["B"]))
S2 = sum((V2[x] - V2[y]) * ((V2[x] - V2[y]) / Z1).conjugate() for x, y in (("A", "B"), ("B", "C"), ("C", "A")))
v.check("Ex 07-11.2d", S2.real / 1e3)
v.assert_true("Delta line current in phase with the Y case", abs(deg(Ia2) - deg(Ia)) < 1e-9)

# ================================================================================ Example 3 (line impedance)
Zl = 0.1 + 0.2j
net3 = y_source(Vp400, [("Z", "A", "a", Zl), ("Z", "B", "b", Zl), ("Z", "C", "c", Zl),
                        ("Z", "a", "N", Z1), ("Z", "b", "N", Z1), ("Z", "c", "N", Z1)])
V3, _ = mna(net3)
Ia3 = (V3["A"] - V3["a"]) / Zl
v.check("Ex 07-11.3a", abs(Ia3))
v.check("Ex 07-11.3b", deg(Ia3))
VL3 = abs(V3["a"] - V3["b"])
v.check("Ex 07-11.3c", VL3)
v.check("Ex 07-11.3d", (400 - VL3) / 400 * 100)
v.check("Ex 07-11.3e", 3 * abs(Ia3) ** 2 * Zl.real)
v.check("Ex 07-11.3f", 3 * abs(Ia3) ** 2 * Z1.real / 1e3)

# ================================================================================ Example 4 (unbalanced 4-wire; harmonics by sampling)
net4 = y_source(230.0, [("Z", "A", "0", 10.0), ("Z", "B", "0", 20.0), ("Z", "C", "0", 40.0)])
V4, I4s = mna(net4)
In4 = sum(-i for i in I4s)  # source currents return through the grounded neutral
v.check("Ex 07-11.4a", abs(In4))
v.check("Ex 07-11.4b", deg(In4))
ts = np.linspace(0, 0.02, 20000, endpoint=False)
w = 2 * pi * 50
i_n_fund = sum(23 * math.sqrt(2) * np.cos(w * ts - k * 2 * pi / 3) for k in range(3))
i_n_3 = sum(10 * math.sqrt(2) * np.cos(3 * (w * ts - k * 2 * pi / 3)) for k in range(3))
v.check("Ex 07-11.4c", np.sqrt(np.mean(i_n_fund**2)), tol=1e-9)
v.check("Ex 07-11.4d", np.sqrt(np.mean(i_n_3**2)))

# ================================================================================ Example 5 (rack power)
for VLx, i_full, i_cont in ((208, "a", "b"), (415, "c", "d")):
    v.check(f"Ex 07-11.5{i_full}", R3 * VLx * 30 / 1e3)
    v.check(f"Ex 07-11.5{i_cont}", 0.8 * R3 * VLx * 30 / 1e3)
v.check("Ex 07-11.5e", 415 / R3)
v.check("Ex 07-11.5f", 17300 / (R3 * 415))
v.check("Ex 07-11.5g", 17300 / (R3 * 208))
v.check("Ex 07-11.5h", (415 / 208) ** 2)

# ================================================================================ Example 6 (two wattmeters from the solved circuit)
Ic1 = Il1[2]
W1 = ((V1["A"] - V1["B"]) * Il1[0].conjugate()).real
W2 = ((V1["C"] - V1["B"]) * Ic1.conjugate()).real
v.check("Ex 07-11.6a", W1)
v.check("Ex 07-11.6b", W2)
v.assert_true("W1 + W2 = P", abs(W1 + W2 - S1.real) < 1e-6)
v.assert_true("sqrt3 (W2 - W1) = Q", abs(R3 * (W2 - W1) - S1.imag) < 1e-6)
Qc = S1.real * (math.tan(math.acos(0.8)) - math.tan(math.acos(0.95)))
v.check("Ex 07-11.6c", Qc)
wq = 2 * pi * 50
Cd = Qc / 3 / (wq * 400**2)
Cy = Qc / 3 / (wq * Vp400**2)
v.check("Ex 07-11.6d", Cd * 1e6)
v.check("Ex 07-11.6e", Cy * 1e6)
# confirm by adding the Delta bank to the circuit and solving whole
Zc = 1 / (1j * wq * Cd)
V6, I6s = mna(net1 + [("Z", "A", "B", Zc), ("Z", "B", "C", Zc), ("Z", "C", "A", Zc)])
Ia6 = -I6s[0]
v.check("Ex 07-11.6f", abs(Ia6))

# ================================================================================ Numbers to know
# copper for equal loss and equal line-to-line voltage: single phase 2 wires at P/V, three phase 3 wires at P/(sqrt3 V)
R1 = 1.0
loss1 = 2 * (1 / 1) ** 2 * R1
R3w = loss1 / (3 * (1 / R3) ** 2)  # resistance per three-phase conductor giving the same loss
v.check("N 07-11.a", 3 * (R1 / R3w) / 2 * 100)  # copper volume ~ number of wires / resistance
v.check("N 07-11.b", R3 * 230)

# ================================================================================ Practitioner lens
v.check("PL 07-11.a", 400 / R3)
v.check("PL 07-11.b", 690 / R3)
v.check("PL 07-11.c", 480 / R3)
v.check("PL 07-11.d", 0.8 * R3 * 208 * 30 / 1e3)
v.check("PL 07-11.e", R3 * 208 * 60 / 1e3)
v.check("PL 07-11.f", R3 * 415 * 30 / 1e3)
v.check("PL 07-11.g", 208 * 30 / 1e3)

# ================================================================================ Problems
v.check("07-11.1a", R3 * 120)
v.check("07-11.1b", R3 * 277)
v.check("07-11.1c", 400 / R3)
v.check("07-11.1d", R3 * 10)
Va, Vb, Vc = 277, 277 * cmath.exp(-2j * pi / 3), 277 * cmath.exp(2j * pi / 3)
v.check("07-11.2a", abs(Vb - Vc))
v.check("07-11.2b", deg(Vb - Vc), tol=1e-6)
v.check("07-11.2c", abs(Vc - Va))
v.check("07-11.2d", deg(Vc - Va), tol=1e-6)
# P3: Delta-Y by driving both from the same source and comparing line currents
Zd3 = 30 + 15j
Vd, Id = mna(y_source(100.0, [("Z", "A", "B", Zd3), ("Z", "B", "C", Zd3), ("Z", "C", "A", Zd3)]))
Zy3 = (Vd["A"] - 0) / (-Id[0])
v.check("07-11.3a", Zy3.real)
v.check("07-11.3b", Zy3.imag)
Vp208 = 208 / R3
V4p, I4p = mna(y_source(Vp208, [("Z", "A", "N", 12 + 9j), ("Z", "B", "N", 12 + 9j), ("Z", "C", "N", 12 + 9j)]))
Ia4 = -I4p[0]
v.check("07-11.4a", Vp208)
v.check("07-11.4b", abs(Ia4))
v.check("07-11.4c", deg(Ia4))
S4 = sum((V4p[n] - V4p["N"]) * (-i).conjugate() for n, i in zip("ABC", I4p))
v.check("07-11.4d", S4.real)
v.check("07-11.4e", S4.imag)
v.check("07-11.4f", S4.real / abs(S4))
# P5: build a Delta impedance that draws 40 kW at 0.85 lagging at 480 V, solve whole
Sph = 40e3 / 3 * (1 + 1j * math.tan(math.acos(0.85)))
Zm = 480**2 / Sph.conjugate()
V5, I5 = mna(y_source(480 / R3, [("Z", "A", "B", Zm), ("Z", "B", "C", Zm), ("Z", "C", "A", Zm)]))
v.check("07-11.5a", abs(I5[0]))
v.check("07-11.5b", abs((V5["A"] - V5["B"]) / Zm))
v.check("07-11.5c", 3 * ((V5["A"] - V5["B"]) * ((V5["A"] - V5["B"]) / Zm).conjugate()).imag / 1e3)
# P6
Zd6, Zl6 = 24 + 18j, 0.5 + 1j
V6p, _ = mna(y_source(400 / R3, [("Z", "A", "a", Zl6), ("Z", "B", "b", Zl6), ("Z", "C", "c", Zl6),
                                ("Z", "a", "b", Zd6), ("Z", "b", "c", Zd6), ("Z", "c", "a", Zd6)]))
Ia6p = (V6p["A"] - V6p["a"]) / Zl6
v.check("07-11.6a", abs(Ia6p))
v.check("07-11.6b", deg(Ia6p))
v.check("07-11.6c", abs(V6p["a"] - V6p["b"]))
v.check("07-11.6d", abs((V6p["a"] - V6p["b"]) / Zd6))
v.check("07-11.6e", 3 * abs((V6p["a"] - V6p["b"]) / Zd6) ** 2 * Zd6.real / 1e3)
# P7
V7, I7 = mna(y_source(120.0, [("Z", "A", "0", 12.0), ("Z", "B", "0", 12.0), ("Z", "C", "0", 12j)]))
Ic7 = -I7[2]
v.check("07-11.7a", abs(Ic7))
v.check("07-11.7b", deg(Ic7))
In7 = sum(-i for i in I7)
v.check("07-11.7c", abs(In7))
v.check("07-11.7d", deg(In7))
# P8 by sampling
iph = [10 * math.sqrt(2) * np.cos(w * ts - k * 2 * pi / 3) + 4 * math.sqrt(2) * np.cos(3 * (w * ts - k * 2 * pi / 3))
       + 2 * math.sqrt(2) * np.cos(5 * (w * ts - k * 2 * pi / 3)) for k in range(3)]
v.check("07-11.8a", np.sqrt(np.mean(iph[0] ** 2)))
v.check("07-11.8b", np.sqrt(np.mean(sum(iph) ** 2)))
i5 = sum(2 * math.sqrt(2) * np.cos(5 * (w * ts - k * 2 * pi / 3)) for k in range(3))
v.check("07-11.8c", np.sqrt(np.mean(i5**2)), tol=1e-9)
# P9: find the balanced load whose two meters read -2 kW and 10 kW, then read P, Q and PF from the circuit


def meters(Zmag, th, seq=1):
    Z = Zmag * cmath.exp(1j * th)
    Vp = 400 / R3
    els = [("V", "A", "0", Vp), ("V", "B", "0", Vp * cmath.exp(-seq * 2j * pi / 3)),
           ("V", "C", "0", Vp * cmath.exp(seq * 2j * pi / 3)), ("Z", "A", "N", Z), ("Z", "B", "N", Z),
           ("Z", "C", "N", Z)]
    V, I = mna(els)
    Ia, Ic = -I[0], -I[2]
    W1 = ((V["A"] - V["B"]) * Ia.conjugate()).real
    W2 = ((V["C"] - V["B"]) * Ic.conjugate()).real
    S = sum((V[n] - V["N"]) * (-I[k]).conjugate() for k, n in enumerate("ABC"))
    return W1, W2, S


zm9, th9 = fsolve(lambda x: [meters(x[0], x[1])[0] + 2e3, meters(x[0], x[1])[1] - 10e3], [10.0, 1.0], xtol=1e-12)
_, _, S9 = meters(zm9, th9)
v.check("07-11.9a", S9.real / 1e3)
v.check("07-11.9b", S9.imag / 1e3)
v.check("07-11.9c", S9.real / abs(S9))
v.check("07-11.9d", math.degrees(th9))
v.check("07-11.9e", math.cos(brentq(lambda th: meters(10.0, th)[0], 0.5, 1.5)))

# P10: a balanced Y load drawing 300 kW at PF 0.75 from 480 V, 60 Hz; Delta capacitors sized by root-finding


def plant(Cd):
    Vp = 480 / R3
    Zl = (3 * Vp ** 2 / 300e3) * 0.75 * cmath.exp(1j * math.acos(0.75))    # |Z| = 3 Vp^2 PF / P
    Zc = 1 / (1j * 2 * pi * 60 * Cd) if Cd else 1e15
    els = y_source(Vp, [("Z", "A", "N", Zl), ("Z", "B", "N", Zl), ("Z", "C", "N", Zl),
                        ("Z", "A", "B", Zc), ("Z", "B", "C", Zc), ("Z", "C", "A", Zc)])
    V, I = mna(els)
    S = sum(V[n] * (-I[k]).conjugate() for k, n in enumerate("ABC"))
    return S, abs(I[0])


S0, I0 = plant(0.0)
assert abs(S0.real - 300e3) < 1e-6 and abs(S0.real / abs(S0) - 0.75) < 1e-12
Cd10 = brentq(lambda C: plant(C)[0].real / abs(plant(C)[0]) - 0.95, 1e-6, 1e-3, xtol=1e-15)
S1, I1 = plant(Cd10)
v.check("07-11.10a", (S0.imag - S1.imag) / 1e3)
v.check("07-11.10b", Cd10 * 1e6)
v.check("07-11.10c", I0)
v.check("07-11.10d", I1)
# P11: single-phase swing by sampling; three-phase constant shown above
S11 = 12.8e3 / 0.8
th = math.acos(0.8)
p1 = np.sqrt(2) * 1 * np.cos(w * ts) * np.sqrt(2) * S11 * np.cos(w * ts - th)
v.check("07-11.11a", p1.min() / 1e3)
v.check("07-11.11b", p1.max() / 1e3)
v.check("07-11.11c", p.mean() / 1e3)
# P12
for VLx, ident in ((415, "a"), (208, "b")):
    Ix = 17300 / (R3 * VLx)
    v.check(f"07-11.12{ident}", 3 * Ix**2 * 0.06)
v.check("07-11.12c", 0.8 * R3 * 208 * 30 / 1e3)
v.check("07-11.12d", R3 * 208 * 60 / 1e3)
v.check("07-11.12e", R3 * 415 * 30 / 1e3)
v.check("07-11.12f", 208 * 30 / 1e3)

# ================================================================================ Lab handout (open neutral)
V7o, _ = mna(y_source(230.0, [("Z", "A", "N", 10.0), ("Z", "B", "N", 20.0), ("Z", "C", "N", 40.0)]))
for n, ident in (("A", "a"), ("B", "b"), ("C", "c")):
    v.check(f"Lab 07-11.{ident}", abs(V7o[n] - V7o["N"]))
v.check("Lab 07-11.d", abs(V7o["N"]))

# ---- Example 7 (audit addition): broken neutral, star point floating
V7, I7 = mna(y_source(230.0, [("Z", "A", "N", 10.0), ("Z", "B", "N", 20.0), ("Z", "C", "N", 40.0)]))
v.check("Ex 07-11.7a", abs(V7["N"]))
v.check("Ex 07-11.7b", math.degrees(cmath.phase(V7["N"])))
for k, (n, z) in enumerate((("A", 10.0), ("B", 20.0), ("C", 40.0))):
    v.check(f"Ex 07-11.7{'cde'[k]}", abs(V7[n] - V7["N"]))
    v.check(f"Ex 07-11.7{'fgh'[k]}", abs((V7[n] - V7["N"]) / z))
# ---- P13 (audit addition): negative sequence
Vp13 = 400 / R3
V13, I13 = mna([("V", "A", "0", Vp13), ("V", "B", "0", Vp13 * cmath.exp(2j * pi / 3)),
                ("V", "C", "0", Vp13 * cmath.exp(-2j * pi / 3)), ("Z", "A", "N", 8 + 6j), ("Z", "B", "N", 8 + 6j),
                ("Z", "C", "N", 8 + 6j)])
Vab13 = V13["A"] - V13["B"]
v.check("07-11.13a", abs(Vab13))
v.check("07-11.13b", math.degrees(cmath.phase(Vab13)))
Ia13, Ic13 = -I13[0], -I13[2]
v.check("07-11.13c", abs(Ia13))
v.check("07-11.13d", math.degrees(cmath.phase(Ia13)))
W1n = (Vab13 * Ia13.conjugate()).real
W2n = ((V13["C"] - V13["B"]) * Ic13.conjugate()).real
v.check("07-11.13e", W1n)
v.check("07-11.13f", W2n)
v.check("07-11.13g", (W1n + W2n) / 1e3)
v.check("07-11.13h", R3 * (W2n - W1n))
v.check("07-11.13i", sum(((V13[n] - V13["N"]) * (-I13[k]).conjugate()).imag for k, n in enumerate("ABC")))
# ---- P14 (audit addition): unbalanced Delta load from a Delta source (two winding sources suffice;
# node B is the reference), line currents from the load branches
V14, _ = mna([("V", "A", "0", 400.0), ("V", "0", "C", 400 * cmath.exp(-2j * pi / 3)),
              ("Z", "A", "0", 100.0), ("Z", "0", "C", 100j), ("Z", "C", "A", -100j)])
Vb14 = 0.0
Iab, Ibc, Ica = (V14["A"] - Vb14) / 100, (Vb14 - V14["C"]) / 100j, (V14["C"] - V14["A"]) / -100j
d14 = lambda z: math.degrees(cmath.phase(z))  # noqa: E731
v.check("07-11.14a", abs(Iab))
v.check("07-11.14b", d14(Ibc))
v.check("07-11.14c", d14(Ica))
Ia14, Ib14, Ic14 = Iab - Ica, Ibc - Iab, Ica - Ibc
v.check("07-11.14d", abs(Ia14))
v.check("07-11.14e", d14(Ia14))
v.check("07-11.14f", d14(Ib14))
v.check("07-11.14g", abs(Ic14))
v.check("07-11.14h", d14(Ic14))
S14 = Iab * Iab.conjugate() * 100 + Ibc * Ibc.conjugate() * 100j + Ica * Ica.conjugate() * -100j
v.check("07-11.14i", S14.real)
v.check("07-11.14j", S14.imag, tol=0.5)
cent = (V14["A"] + Vb14 + V14["C"]) / 3   # neutral of the equivalent balanced Y = centroid
v.check("07-11.14k", abs(V14["A"] - cent))
v.check("07-11.14l", d14(V14["A"] - cent))

v.finish()
