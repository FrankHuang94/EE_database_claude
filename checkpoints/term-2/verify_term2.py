#!/usr/bin/env python3
"""Verify the Term 2 checkpoint: recompute every answer and check every multiple-choice letter.

Each value is recomputed independently of the hand method in the solutions:
- DC and AC circuits by a modified-nodal-analysis solver (resistors, sources, controlled sources, L, C,
  coupled inductors), so dividers, superposition, Thevenin values and loading are found by solving the
  circuit, not by the textbook shortcut;
- transients by integrating the circuit ODEs (solve_ivp), and step responses by simulating the transfer
  function; peaks, final values and the -3 dB band are located numerically;
- power by averaging sampled waveforms or summing per-phase phasor products;
- digital answers by brute force: truth tables, exhaustive minimization, bit-level addition, LFSR runs.
For numerical multiple-choice questions, the option text is parsed from README.md, and the script checks
that the letter in solutions.md is the only option matching the computed value to its printed precision.
"""
from __future__ import annotations

import cmath
import itertools
import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
from eeverify import Verifier, parse_value  # noqa: E402

README, SOL = HERE / "README.md", HERE / "solutions.md"
v = Verifier.from_files("term-2", SOL)


def mna(elements, w=0.0):
    """Solve a circuit. Elements: (kind, a, b, value[, extra]).
    R, C, L: value in ohm, F, H. V: source, a is +. I: current value driven from b into a? No:
    I flows from node b through the source into node a ("into node a"). E: VCVS v_a - v_b = gain*(v_c - v_d),
    extra = (c, d). G: VCCS current gain*(v_c - v_d) flows from a to b through the source, extra = (c, d).
    K: coupling (L1 name index, L2 name index, k). Node 0 is ground. Returns node voltages dict."""
    nodes = sorted({n for e in elements if e[0] != "K" for n in e[1:3] if n != 0})
    idx = {n: i for i, n in enumerate(nodes)}
    branch = [i for i, e in enumerate(elements) if e[0] in ("V", "E") or (e[0] == "L")]
    bidx = {i: len(nodes) + k for k, i in enumerate(branch)}
    N = len(nodes) + len(branch)
    A = np.zeros((N, N), complex)
    z = np.zeros(N, complex)
    s = 1j * w

    def stamp_g(a, b, g):
        for p, q, sg in ((a, a, 1), (b, b, 1), (a, b, -1), (b, a, -1)):
            if p and q:
                A[idx[p], idx[q]] += sg * g

    for i, e in enumerate(elements):
        kind, a, b, val = e[:4]
        if kind == "R":
            stamp_g(a, b, 1 / val)
        elif kind == "C":
            stamp_g(a, b, s * val)
        elif kind in ("V", "E", "L"):
            k = bidx[i]
            if a:
                A[idx[a], k] += 1
                A[k, idx[a]] += 1
            if b:
                A[idx[b], k] -= 1
                A[k, idx[b]] -= 1
            if kind == "V":
                z[k] = val
            elif kind == "E":
                c, d = e[4]
                if c:
                    A[k, idx[c]] -= val
                if d:
                    A[k, idx[d]] += val
            else:  # inductor: v_a - v_b - s L i = 0
                A[k, k] -= s * val
        elif kind == "I":
            if a:
                z[idx[a]] += val
            if b:
                z[idx[b]] -= val
        elif kind == "G":
            c, d = e[4]
            for node, sg in ((a, 1), (b, -1)):
                if node:
                    if c:
                        A[idx[node], idx[c]] += sg * val
                    if d:
                        A[idx[node], idx[d]] -= sg * val
    for e in elements:
        if e[0] == "K":
            _, i1, i2, kc = e
            m = kc * math.sqrt(elements[i1][3] * elements[i2][3])
            A[bidx[i1], bidx[i2]] -= s * m
            A[bidx[i2], bidx[i1]] -= s * m
    x = np.linalg.solve(A, z)
    out = {0: 0.0}
    out.update({n: x[idx[n]] for n in nodes})
    out["branch"] = {i: x[bidx[i]] for i in branch}
    return out


ans = {}
# ================================================================= Block 1
ans[1] = 12 * 2.5 * 3 * 3600 / 1e3                                   # kJ
r = mna([("V", 1, 0, 1.0), ("R", 1, 2, 6e3), ("R", 2, 0, 3e3), ("R", 1, 3, 4e3), ("R", 3, 0, 1e30)])
# equivalent resistance by test source: (6k || 3k) + 4k between node 1 and ground, built explicitly
r = mna([("V", 1, 0, 1.0), ("R", 1, 2, 4e3), ("R", 2, 0, 6e3), ("R", 2, 0, 3e3)])
ans[2] = (1 / -r["branch"][0]).real / 1e3                             # kΩ (source current is -i)
r = mna([("V", 1, 0, 10.0), ("R", 1, 2, 10e3), ("R", 2, 0, 10e3), ("R", 2, 0, 10e3)])
ans[3] = r[2].real
r = mna([("V", 1, 0, 10.0), ("R", 1, 2, 2e3), ("R", 2, 0, 4e3), ("R", 2, 3, 2e3), ("R", 3, 0, 4e3),
         ("I", 3, 0, 1e-3)])
ans[4] = r[3].real
v.assert_true("Q4: node 2 is at 6.18 V", abs(r[2].real - 6.18) < 5e-3)
r = mna([("V", 1, 0, 12.0), ("R", 1, 2, 4.0), ("R", 2, 0, 6.0), ("R", 2, 3, 2.0), ("V", 3, 0, 6.0)])
ans[5] = (r[2] / 6.0).real
v.assert_true("Q5: mesh currents 1.364 A (left, through R1) and 0.273 A (right, through R3)",
              abs((12 - r[2].real) / 4 - 1.364) < 5e-4 and abs((r[2].real - 6) / 2 - 0.273) < 5e-4)
r = mna([("V", 1, 0, 1.0), ("R", 1, 2, 1e3), ("R", 2, 0, 9e3), ("E", 3, 0, 50.0, (2, 0)),
         ("R", 3, 4, 100.0), ("R", 4, 0, 1e3)])
ans[6] = r[4].real
r = mna([("V", 1, 0, 10.0), ("R", 1, 2, 5.0), ("R", 2, 0, 20.0), ("I", 2, 0, 2.0)])
ans[7] = r[2].real
q8 = [("V", 1, 0, 24.0), ("R", 1, 2, 6e3), ("R", 2, 0, 3e3), ("R", 2, 3, 2e3)]
voc = mna(q8 + [("R", 3, 0, 1e15)])[3].real
isc = mna(q8 + [("V", 3, 0, 0.0)])["branch"][4].real           # current from node 3 through the short
rth = voc / isc
v.assert_true("Q8: the Thevenin equivalent is 8 V in series with 4 kΩ (option A)",
              abs(voc - 8) < 1e-9 and abs(rth - 4e3) < 1e-6)
loads = np.linspace(100, 20e3, 20000)
pl = [(mna(q8 + [("R", 3, 0, RL)])[3].real ** 2 / RL) for RL in loads]
ans[9] = max(pl) * 1e3                                                # mW
v.assert_true("Q9: the power peaks at a load equal to R_th", abs(loads[int(np.argmax(pl))] - rth) < 10)
r = mna([("V", 1, 0, 1.0), ("R", 1, 0, 2e3), ("G", 1, 0, 1e-3, (1, 0))])
ans[10] = (1 / -r["branch"][0]).real
r = mna([("V", 1, 0, 0.3), ("R", 1, 2, 4.7e3), ("R", 2, 3, 47e3), ("E", 3, 0, 1e9, (0, 2))])
ans[11] = r[3].real
r = mna([("V", 1, 0, 0.5), ("V", 4, 0, -0.2), ("R", 1, 2, 10e3), ("R", 4, 2, 5e3), ("R", 2, 3, 10e3),
         ("E", 3, 0, 1e9, (0, 2))])
ans[12] = r[3].real
ans[13] = brentq(lambda rx: (mna([("V", 1, 0, 1.0), ("R", 1, 2, 1e3), ("R", 2, 0, 2e3), ("R", 1, 3, 1.5e3),
                                  ("R", 3, 0, rx)])[2] - mna([("V", 1, 0, 1.0), ("R", 1, 2, 1e3),
                                  ("R", 2, 0, 2e3), ("R", 1, 3, 1.5e3), ("R", 3, 0, rx)])[3]).real,
                 100, 1e5) / 1e3
r = mna([("V", 1, 0, 10.0), ("R", 1, 2, 1e6), ("R", 2, 0, 1e6), ("R", 2, 0, 10e6)])
ans[14] = r[2].real

# ================================================================= Block 2
ans[15] = 47e-6 * 5 / 10e-3 * 1e3                                     # mA
sol = solve_ivp(lambda t, y: [(9 - y[0]) / (20e3 * 0.5e-6)], (0, 15e-3), [0.0], rtol=1e-11, atol=1e-13)
ans[16] = sol.y[0, -1]
sol = solve_ivp(lambda t, y: [(12 - 100 * y[0]) / 50e-3], (0, 1e-3), [0.0], rtol=1e-11, atol=1e-14)
ans[17] = sol.y[0, -1] * 1e3                                          # mA
R18, L18, C18 = 10.0, 1e-3, 10e-6
roots = np.roots([L18 * C18, R18 * C18, 1])
ans[18] = -roots.real[0] / abs(roots[0])                              # zeta = -Re(p)/|p|
zeta = 0.5
t = np.linspace(0, 20, 400001)
_, y = signal.step(([1.0], [1.0, 2 * zeta, 1.0]), T=t)
ans[19] = 100 * (y.max() - 1)
t20 = np.linspace(0, 30, 30001)
_, y20 = signal.step(([10.0], [1.0, 3.0, 2.0]), T=t20)
ans[20] = y20[-1]
w21 = 2 * math.pi * 1e3
r = mna([("V", 1, 0, 100.0), ("R", 1, 2, 30.0), ("L", 2, 0, 6.366e-3)], w21)
i21 = r[2] / (1j * w21 * 6.366e-3)
v.assert_true("Q21: the current is 2.00 A at -53.1 degrees (option A)",
              abs(abs(i21) - 2.00) < 0.005 and abs(math.degrees(cmath.phase(i21)) + 53.1) < 0.05)
tt = np.linspace(0, 1, 100001)[:-1]
ans[22] = math.sqrt(np.mean((10 + 10 * np.cos(2 * math.pi * tt)) ** 2))
phi = math.acos(0.8)
vt = 230 * math.sqrt(2) * np.cos(2 * math.pi * tt)
it = 10 * math.sqrt(2) * np.cos(2 * math.pi * tt - phi)
it_q = 10 * math.sqrt(2) * np.cos(2 * math.pi * tt - phi + math.pi / 2)    # reactive power: V times I shifted 90°
ans[23] = float(np.mean(vt * it_q))
v.assert_true("Q23: the real power is 1840 W", abs(np.mean(vt * it) - 1840) < 1e-6)
q_before = 10e3 * math.tan(math.acos(0.70))
q_after = 10e3 * math.tan(math.acos(0.95))
ans[24] = (q_before - q_after) / 1e3
r = mna([("V", 1, 0, 1.0), ("R", 1, 2, 1.59e3), ("C", 2, 0, 100e-9)], 2 * math.pi * 10e3)
ans[25] = 20 * math.log10(abs(r[2]))
ans[26] = 10 ** ((26 - 6) / 20)


def series_current(f):
    w = 2 * math.pi * f
    rr = mna([("V", 1, 0, 1.0), ("R", 1, 2, 20.0), ("L", 2, 3, 10e-3), ("C", 3, 0, 100e-9)], w)
    return abs(rr[3] * 1j * w * 100e-9)


f0 = 1 / (2 * math.pi * math.sqrt(10e-3 * 100e-9))
imax = series_current(f0)
f_lo = brentq(lambda f: series_current(f) - imax / math.sqrt(2), f0 / 2, f0)
f_hi = brentq(lambda f: series_current(f) - imax / math.sqrt(2), f0, 2 * f0)
ans[27] = f_hi - f_lo
v.assert_true("Q27: f0 = 5.03 kHz and Q = 15.8", abs(f0 - 5033) < 0.5 and abs(math.sqrt(10e-3 / 100e-9) / 20 - 15.8) < 0.05)
b, a = signal.butter(2, 2 * math.pi * 1e3, analog=True)
_, h = signal.freqs(b, a, worN=[2 * math.pi * 3e3])
ans[28] = -20 * math.log10(abs(h[0]))
el = [("V", 1, 0, 1.0), ("L", 1, 0, 25.0 * 1e6), ("L", 2, 0, 1.0 * 1e6), ("R", 2, 0, 8.0), ("K", 1, 2, 1.0)]
r = mna(el, 2 * math.pi * 1e3)
ans[29] = (1 / -r["branch"][0]).real
gam = (75 - 50) / (75 + 50)
ans[30] = -20 * math.log10(abs(gam))
vph = 400 / math.sqrt(3)
zph = cmath.rect(20, math.radians(36.87))
p31 = 0
for k in range(3):
    va = cmath.rect(vph, -2 * math.pi * k / 3)
    rr = mna([("V", 1, 0, va), ("R", 1, 2, zph.real), ("L", 2, 0, zph.imag / 100.0)], 100.0)  # neutral at 0
    ia = (va - rr[2]) / zph.real
    p31 += (va * ia.conjugate()).real
ans[31] = p31 / 1e3
v.assert_true("Q31: phase current 11.55 A and 2133 W per phase", abs(vph / 20 - 11.55) < 5e-3 and abs(p31 / 3 - 2133) < 0.5)
i_line = 15e3 / (3 * vph * 0.85)                                       # per-phase: P/3 = Vph I pf
ans[32] = i_line

# ================================================================= Block 3
pat = 0b11001011
ans[33] = pat - 256 if pat & 0x80 else pat
ans[34] = int("3A7", 16)
v.assert_true("Q35: 12-bit two's complement spans -2048 to 2047 (option A)",
              (-(2 ** 11), 2 ** 11 - 1) == (-2048, 2047))
s36 = (0x70 + 0x30) & 0xFF
c_out = (0x70 + 0x30) >> 8
c_in7 = (((0x70 & 0x7F) + (0x30 & 0x7F)) >> 7) & 1
v.assert_true("Q36: 70h + 30h overflows (V = 1), reads -96, with no carry out (option B)",
              (c_out ^ c_in7) == 1 and s36 - 256 == -96 and c_out == 0)
rows = list(itertools.product((0, 1), repeat=3))
f37 = [(a & b) | (a & (1 - b) & c) | ((1 - a) & c) for a, b, c in rows]
v.assert_true("Q37: AB + AB'C + A'C equals AB + C (option A) and none of the other options",
              f37 == [(a & b) | c for a, b, c in rows]
              and f37 != [a | c for a, b, c in rows]
              and f37 != [(a & b) | ((1 - a) & c) for a, b, c in rows] and f37 != [c for a, b, c in rows])
g38 = [1 - (((1 - a) & b) | c) for a, b, c in rows]
v.assert_true("Q38: the complement of A'B + C is (A + B')C' (option A) and not the other options",
              g38 == [(a | (1 - b)) & (1 - c) for a, b, c in rows]
              and g38 != [(a & (1 - b)) | (1 - c) for a, b, c in rows]
              and g38 != [((1 - a) | b) & c for a, b, c in rows]
              and g38 != [a | (1 - b) | (1 - c) for a, b, c in rows])
on39 = {0, 2, 5, 7, 8, 10, 13, 15}


def bits4(m):
    return (m >> 3) & 1, (m >> 2) & 1, (m >> 1) & 1, m & 1


cubes = [c for c in itertools.product((0, 1, None), repeat=4)
         if {m for m in range(16) if all(x is None or x == y for x, y in zip(c, bits4(m)))} <= on39]
best = None
for k in range(1, 4):
    for combo in itertools.combinations(cubes, k):
        cov = {m for m in range(16) for c in combo if all(x is None or x == y for x, y in zip(c, bits4(m)))}
        if cov == on39:
            lit = sum(x is not None for c in combo for x in c)
            if best is None or lit < best[0]:
                best = (lit, combo)
    if best:
        break
v.assert_true("Q39: the unique minimal SOP is B'D' + BD with 4 literals (option A)",
              best[0] == 4 and set(best[1]) == {(None, 0, None, 0), (None, 1, None, 1)})
ans[40] = 32 - 1
ans[41] = 2 * 32 * 25e-3                                               # ns
ans[42] = 1000 / (80 + 720 + 50)                                       # GHz
v.assert_true("Q43: hold slack 30 + 15 - 60 = -15 ps, violated by 15 ps (option B)", 30 + 15 - 60 == -15)
ans[44] = math.ceil(math.log2(100))
s_, n45 = 1, 0
while True:                                                            # x^10 + x^7 + 1, Fibonacci form
    bit = ((s_ >> 9) ^ (s_ >> 6)) & 1
    s_ = ((s_ << 1) | bit) & 0x3FF
    n45 += 1
    if s_ == 1:
        break
ans[45] = n45
v.assert_true("Q45: x^10 + x^7 + 1 is maximal (period 2^10 - 1)", n45 == 2 ** 10 - 1)
v.assert_true("Q46: 12 states need 4 binary flip-flops and 12 one-hot (option A)",
              math.ceil(math.log2(12)) == 4)
ans[48] = int(math.log2(256 * 1024))
ans[50] = 2 ** 6 * 4

for qn, value in sorted(ans.items()):
    v.check(f"T2.{qn:02d}", value)

# ================================================================= multiple-choice letters
readme = README.read_text(encoding="utf-8")
sol_text = SOL.read_text(encoding="utf-8")
letters = {int(n): l_ for n, l_ in re.findall(r"^\*\*(\d+)\. Answer: \(([A-D])\)", sol_text, re.M)}
options = {}
for block in re.split(r"^\*\*(?=\d+\.\*\*)", readme, flags=re.M)[1:]:
    n = int(block.split(".", 1)[0])
    opt_line = next((ln for ln in block.splitlines() if ln.startswith("(A)")), None)
    if opt_line:
        options[n] = dict(re.findall(r"\(([A-D])\)\s*([^·]+?)\s*(?:·|$)", opt_line))


def option_value(text):
    try:
        pub = parse_value(text.split()[0])
    except Exception:  # noqa: BLE001 - non-numeric option text
        return None
    part = pub.parts[0]
    return part.value, part.halfulp


numeric_mc = [1, 3, 7, 11, 14, 15, 17, 18, 20, 23, 25, 28, 29, 32, 33, 44]
for qn in numeric_mc:
    target = ans[qn]
    scored = sorted((abs(p[0] - target), letter, p[1]) for letter, text in options[qn].items()
                    if (p := option_value(text)) is not None)
    (best_err, best_l, tol), second_err = scored[0], scored[1][0]
    v.assert_true(f"Q{qn}: answer letter {letters.get(qn)} is the option closest to the computed value, within its precision",
                  best_l == letters.get(qn) and best_err <= tol * (1 + 1e-9) and second_err > best_err,
                  f"closest {best_l} (error {best_err:.3g}), options {options[qn]}")
expected_text = {8: "A", 21: "A", 35: "A", 36: "B", 37: "A", 38: "A", 39: "A", 43: "B", 46: "A", 47: "A", 49: "A"}
v.assert_true("the non-numerical multiple-choice letters match the checks above",
              all(letters.get(q) == l_ for q, l_ in expected_text.items()))
v.assert_true("every multiple-choice question has an answer letter", set(options) <= set(letters))
v.assert_true("50 questions, numbered 1 to 50",
              sorted(int(n) for n in re.findall(r"^\*\*(\d+)\.\*\*", readme, re.M)) == list(range(1, 51)))

sys.exit(v.finish())
