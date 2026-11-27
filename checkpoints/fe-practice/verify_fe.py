#!/usr/bin/env python3
"""Verify the full-length FE practice exam: recompute every answer and check every multiple-choice letter.

Each value is recomputed by a route other than the hand formula where one exists:
- mathematics: a central finite difference, Simpson quadrature, numpy's linear solver and eigenvalues, an RK4
  integration of the ODE, an inverse Laplace transform by sympy, the exact square root against the Taylor sum;
- probability: scipy's normal, binomial and t distributions, and Bayes' rule by counting a population;
- economics: explicit sums of discounted cash flows and a month-free compounding loop;
- circuits: a nodal matrix solved by numpy, an RK4 transient for the RC and RL steps, complex impedances;
- systems and signals: numpy convolution, frequency response evaluated directly, an aliasing search over k,
  impulse response by running the difference equation, a simulated quantizer for the ADC SNR;
- electronics and power: complex per-phase power for the three-phase load, the loss summed phase by phase;
- control: a simulated step response for overshoot, peak time and final value; the Routh array swept over K;
- digital, computer systems and software: bit arithmetic, truth-table enumeration, counter simulation, a
  pipeline schedule, a binary search counted on a list, and the Python range itself.
Multiple-choice options are parsed from README.md; for numeric options the script checks that the letter in
solutions.md is the only option closest to the computed value, within its printed precision. Conceptual
questions are checked against the letters recorded below.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy import integrate, signal, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from eeverify import Verifier, parse_value  # noqa: E402

README, SOL = HERE / "README.md", HERE / "solutions.md"
v = Verifier.from_files("fe-practice", SOL)
ans: dict[int, float] = {}
CONCEPT = {18: "B", 19: "D", 20: "A", 46: "D", 90: "C", 94: "D", 100: "B", 108: "B", 110: "D"}


def rk4(f, y0, t_end, n=20000):
    h, t, y = t_end / n, 0.0, np.array(y0, dtype=float)
    for _ in range(n):
        k1 = f(t, y)
        k2 = f(t + h / 2, y + h / 2 * k1)
        k3 = f(t + h / 2, y + h / 2 * k2)
        k4 = f(t + h, y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t += h
    return y


def pv(flows, i):
    return sum(cf / (1 + i) ** (t + 1) for t, cf in enumerate(flows))


# ================================================================= mathematics
f = lambda x: x ** 3 * math.exp(-x)  # noqa: E731
h = 1e-5
ans[1] = (f(1 + h) - f(1 - h)) / (2 * h)
ans[2] = integrate.simpson(np.sin(np.linspace(0, math.pi, 2001)) ** 2, x=np.linspace(0, math.pi, 2001))
sol = np.linalg.solve(np.array([[1, 1, 1], [2, -1, 1], [1, 2, -1]], float), np.array([6, 3, 2], float))
ans[3] = sol[2]
v.assert_true("Q3: the solution satisfies all three equations",
              np.allclose([sol.sum(), 2 * sol[0] - sol[1] + sol[2], sol[0] + 2 * sol[1] - sol[2]], [6, 3, 2]))
ans[4] = max(np.linalg.eigvals(np.array([[4, 1], [2, 3]], float)).real)
ans[5] = abs((3 + 4j) / (1 - 1j))
ans[6] = math.degrees(np.angle(-1 + 1j * math.sqrt(3)))
ans[7] = rk4(lambda t, y: np.array([8 - 4 * y[0]]), [0.0], 0.25)[0]
roots = np.roots([1, 4, 13])
ans[8] = abs(roots[0].imag)
s, t = sp.symbols("s t", positive=True)
ans[9] = float(sp.inverse_laplace_transform(6 / (s * (s + 3)), s, t).subs(t, sp.Rational(1, 2)))
taylor = sum(sp.binomial(sp.Rational(1, 2), k) * sp.Rational(1, 10) ** k for k in range(3))
ans[10] = float(taylor)
v.assert_true("Q10: the Taylor value is within 1e-4 of the exact root", abs(ans[10] - math.sqrt(1.1)) < 1e-4)
x_, y_ = sp.symbols("x y")
F = x_ ** 2 * y_ + 3 * y_ ** 2
grad = [float(sp.diff(F, var).subs({x_: 1, y_: 2})) for var in (x_, y_)]
ans[11] = math.hypot(*grad)
ans[12] = 1 - (1 ** 2 - 2) / (2 * 1)
a_, b_ = np.array([1, 2, 2.0]), np.array([2, -1, 2.0])
ans[13] = math.degrees(math.acos(a_ @ b_ / (np.linalg.norm(a_) * np.linalg.norm(b_))))

# ================================================================= probability and statistics
ans[14] = stats.norm(1000, 10).cdf(1020) - stats.norm(1000, 10).cdf(980)
ans[15] = stats.binom(50, 0.02).pmf(0)
population = 1_000_000                               # count a population for Bayes
defective = population * 0.02
flagged_bad, flagged_good = defective * 0.95, (population - defective) * 0.05
ans[16] = flagged_bad / (flagged_bad + flagged_good)
ans[17] = stats.t.ppf(0.975, 24) * 0.05 / math.sqrt(25) * 1e3

# ================================================================= ethics (numeric)
ans[21] = 2021 + 20

# ================================================================= engineering economics
ans[22] = 10_000 / 1.08 ** 5
v.assert_true("Q22: discounting a year at a time gives the same value",
              abs(ans[22] - 10_000 * np.prod([1 / 1.08] * 5)) < 1e-9)
pa = pv([1.0] * 6, 0.07)                              # (P/A, 7%, 6) by explicit sum
ap = 1 / pa
af = ap - 0.07
ans[23] = (50_000 * ap - 5_000 * af) / 1e3
ans[24] = 200_000 / (50 - 30)
book = 120.0
for _ in range(3):
    book -= (120 - 20) / 5
ans[25] = book
bal = 1.0
for _ in range(4):
    bal *= 1 + 0.06 / 4
ans[26] = (bal - 1) * 100

# ================================================================= properties of electrical materials
ans[27] = 1.72e-8 * 100 / (math.pi * (1.0e-3 / 2) ** 2)
ans[28] = 10 * (1 + 0.00393 * (75 - 20))
ans[29] = (1e10) ** 2 / 1e16
ans[30] = 4 * 8.854e-12 * 1e-4 / 10e-6 * 1e12

# ================================================================= circuit analysis
ans[31] = 12 * (1 / (1 / 10e3 + 1 / 10e3)) / (10e3 + 1 / (1 / 10e3 + 1 / 10e3))
ans[32] = 1 / (1 / 6 + 1 / 3) + 2
G = np.array([[1 / 4 + 1 / 2, -1 / 2], [-1 / 2, 1 / 2 + 1 / 6]])
V = np.linalg.solve(G, np.array([2.0, 0.0]))
ans[33] = V[1]
rl = np.linspace(1, 500, 49_901)
ans[34] = max(10 ** 2 * rl / (50 + rl) ** 2)          # sweep the load
ans[35] = rk4(lambda t, y: np.array([(5 - y[0]) / (10e3 * 100e-9)]), [0.0], 2e-3)[0]
tau = 10e-3 / 100
i_t = rk4(lambda t, y: np.array([(10 - 100 * y[0]) / 10e-3]), [0.0], tau)[0]
v.assert_true("Q36: after one L/R the current is 63.2% of 0.1 A", abs(i_t / 0.1 - (1 - math.exp(-1))) < 1e-6)
ans[36] = tau * 1e3
Z = 30 + 1j * 2 * math.pi * 60 * 0.1
ans[37] = abs(Z)
ans[38] = math.degrees(np.angle(1 / Z))
ans[39] = 1 / (2 * math.pi * math.sqrt(2e-3 * 50e-9)) / 1e3
w0 = 2 * math.pi * ans[39] * 1e3
ans[40] = w0 * 2e-3 / 10
S_load = 230 * 10 * complex(0.8, 0.6)                 # lagging: positive reactive power
ans[41] = S_load.imag / 1e3
ans[42] = S_load.imag / (2 * math.pi * 50 * 230 ** 2) * 1e6
ans[43] = -(47e3 / 4.7e3) * 0.2
ans[44] = 1 + 9e3 / 1e3

# ================================================================= linear systems
ans[45] = abs(10 / (5j + 5))
pole_real = np.roots([1, 2, -3]).real
v.assert_true("Q46: a right-half-plane pole exists (unstable)", max(pole_real) > 0)
ans[47] = np.convolve([1, 2, 3], [1, 1])[2]
tt, yy = signal.step(signal.lti([1], [0.2, 1]), T=np.linspace(0, 2, 200_001))
ans[48] = tt[np.where(np.abs(yy - 1) > 0.02)[0][-1] + 1]
ans[49] = 20 * math.log10(abs(1000 / (100j + 10)))

# ================================================================= signal processing
ans[50] = 2 * 4
ans[51] = min(abs(7 - k * 10) for k in range(-3, 4))
ans[52] = 48_000 / 1024
hh, prev = [], 0.0
for n in range(4):                                    # run y[n] = x[n] + 0.5 y[n-1] with an impulse
    prev = (1.0 if n == 0 else 0.0) + 0.5 * prev
    hh.append(prev)
ans[53] = hh[3]
nb, N = 12, 1 << 16
x = (2 ** (nb - 1) - 1) * np.sin(2 * math.pi * 1031 * np.arange(N) / N)
q_err = np.round(x) - x
ideal = 6.02 * nb + 1.76
measured = 10 * math.log10(np.mean(x ** 2) / np.mean(q_err ** 2))
v.assert_true("Q54: a simulated 12-bit quantizer is within 0.2 dB of 6.02N + 1.76", abs(measured - ideal) < 0.2)
ans[54] = ideal

# ================================================================= electronics
ans[55] = (5 - 0.7) / 1e3 * 1e3
ans[56] = ((12 - 5.1) / 470 - 5.1 / 1e3) * 1e3
ib = (5 - 0.7) / 100e3
ans[57] = 10 - 100 * ib * 1e3
v.assert_true("Q57: the transistor is active (V_CE > 0.2 V)", ans[57] > 0.2)
kp, vov = 2e-3, 1.5 - 0.5
ans[58] = 0.5 * kp * vov ** 2 * 1e3
gm = (0.5 * kp * (vov + 1e-6) ** 2 - 0.5 * kp * (vov - 1e-6) ** 2) / 2e-6   # dI_D/dV_GS numerically
ans[59] = -gm * 5e3
ans[60] = 0.1 / (2 * 60 * 1000e-6)
ans[61] = 10e6 / 20 / 1e3
ans[62] = 20 * math.log10(1000 / 0.1)

# ================================================================= power systems
vph = 480 / math.sqrt(3)
ans[63] = 3 * abs(vph) ** 2 / 10 / 1e3
ans[64] = vph / 10
ans[65] = 50e3 / 240
ans[66] = 138e3 ** 2 / 100e6
ns = 120 * 60 / 4
ans[67] = (ns - 1746) / ns * 100
ans[68] = 120 * 50 / 6
ans[69] = 40 / 50
i_line = 10e6 / (math.sqrt(3) * 33e3 * 0.9)
ans[70] = sum(i_line ** 2 * 2 for _ in range(3)) / 1e3
ans[71] = 240 - 50 * 0.2

# ================================================================= electromagnetics
ans[72] = 8.988e9 * (1e-6) ** 2 / 0.1 ** 2
ans[73] = 4 * math.pi * 1e-7 * 10 / (2 * math.pi * 0.05) * 1e6
ans[74] = 3.00e8 / (1e9 * math.sqrt(2.25))
gam = (75 - 50) / (75 + 50)
ans[75] = (1 + gam) / (1 - gam)

# ================================================================= control systems
ss = sp.symbols("ss")
ans[76] = float(1 / sp.limit(ss * 20 / (ss * (ss + 4)), ss, 0))
wn, zeta = 1.0, 0.5
tt, yy = signal.step(signal.lti([wn ** 2], [1, 2 * zeta * wn, wn ** 2]), T=np.linspace(0, 20, 200_001))
ans[77] = (yy.max() - 1) * 100


def routh_stable(K):
    a3, a2, a1, a0 = 1, 2, 3, K
    b1 = (a2 * a1 - a3 * a0) / a2
    return a2 > 0 and b1 > 0 and a0 > 0


ks = np.linspace(0.001, 20, 200_000)
ans[78] = max(k for k in ks if routh_stable(k))
v.assert_true("Q78: roots for K just below and above 6 change half-plane",
              max(np.roots([1, 2, 3, 5.99]).real) < 0 < max(np.roots([1, 2, 3, 6.01]).real))
tt, yy = signal.step(signal.lti([25], [1, 4, 25]), T=np.linspace(0, 3, 300_001))
ans[79] = tt[np.argmax(yy)]
ans[80] = 180 + (-135)
ans[81] = 9 * 1 / (1 + 9 * 1)
tt, yy = signal.step(signal.lti([5], [1, 3, 10]), T=np.linspace(0, 30, 30_001))
ans[82] = yy[-1]

# ================================================================= communications
ans[83] = 1e6 * math.log2(1 + 15) / 1e6
ans[84] = 2 * 5
ans[85] = 2 * (75 + 15)
k_b = 1.380649e-23
ans[86] = round(10 * math.log10(k_b * 290 * 1e6 / 1e-3))
v.assert_true("Q86: kTB at 290 K and 1 MHz is -114 dBm to within 0.05 dB",
              abs(10 * math.log10(k_b * 290 * 1e6 / 1e-3) + 114) < 0.05)
ans[87] = 20 + 10 + 3 - 110

# ================================================================= computer networks
ans[88] = 2 ** (32 - 26) - 2
ans[89] = 1500 * 8 / 100e6 * 1e6
ans[91] = 2000e3 / 2e8 * 1e3

# ================================================================= digital systems
raw = 0b11110110
ans[92] = raw - 256 if raw & 0x80 else raw
minterms = [m for m in range(8) if ((not (m >> 2) & 1) and (m >> 1) & 1) or ((m >> 2) & 1 and m & 1)]
ans[93] = len(minterms)
nand = lambda a, b: 1 - (a & b)  # noqa: E731
v.assert_true("Q94: NAND builds NOT, AND and OR for every input",
              all(nand(a, a) == 1 - a and nand(nand(a, b), nand(a, b)) == (a & b) and nand(nand(a, a), nand(b, b)) == (a | b)
                  for a in (0, 1) for b in (0, 1)))
msb = [(c >> 3) & 1 for c in range(64)]               # 64 clocks of a 4-bit counter
transitions = sum(1 for i in range(1, 64) if msb[i] == 1 and msb[i - 1] == 0)
ans[95] = 1e6 * transitions / 64 / 1e3
ans[96] = int("3F", 16)
ans[97] = 2 - 0.2 - 1.4 - 0.15
ans[98] = 1 / ((0.1 + 3.2 + 0.2) * 1e-9) / 1e6
ans[99] = (1 << 12) * 8
v.assert_true("Q100: F is exactly the C = 0 rows", all(((m in (0, 2, 4, 6)) == (m & 1 == 0)) for m in range(8)))
b = 0b1011
ans[101] = b ^ (b >> 1)

# ================================================================= computer systems
ans[102] = 1 + 0.05 * 60
ans[103] = 1 / ((1 - 0.8) + 0.8 / 8)
ans[104] = 2e9 * 1.5 / 3e9
lines = 32 * 1024 // 64
ans[105] = 32 - int(math.log2(lines)) - int(math.log2(64))
finish = [5 + i for i in range(100)]                  # instruction i leaves the pipeline at cycle 5 + i
ans[106] = (5 * 100) / finish[-1]

# ================================================================= software engineering
items = list(range(1_000_000))


def comparisons(target):
    lo, hi, c = 0, len(items) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        c += 1
        if items[mid] == target:
            return c
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return c


ans[107] = max(comparisons(x_) for x_ in (0, 999_999, -1, 1_000_000, 524_287, 1))
ans[109] = sum(1 for _ in range(3, 30, 4))

# ================================================================= answer key
for qn, value in sorted(ans.items()):
    v.check(f"FE.{qn:03d}", value)

# ================================================================= multiple-choice letters
readme = README.read_text(encoding="utf-8")
sol_text = SOL.read_text(encoding="utf-8")
letters = {int(n_): l_ for n_, l_ in re.findall(r"^\*\*(\d+)\. Answer: \(([A-D])\)", sol_text, re.M)}
options = {}
for block in re.split(r"^\*\*(?=\d+\.\*\*)", readme, flags=re.M)[1:]:
    qnum = int(block.split(".", 1)[0])
    opt_line = next((ln for ln in block.splitlines() if ln.startswith("(A)")), None)
    if opt_line:
        options[qnum] = dict(re.findall(r"\(([A-D])\)\s*([^·]+?)\s*(?:·|$)", opt_line))


def option_value(text):
    try:
        pub = parse_value(text.split()[0].rstrip(";,°%"))
    except Exception:  # noqa: BLE001 - non-numeric option text
        return None
    part = pub.parts[0]
    return part.value, part.halfulp


for qn in sorted(options):
    if qn in CONCEPT:
        v.assert_true(f"Q{qn}: conceptual answer letter is {CONCEPT[qn]}",
                      letters.get(qn) == CONCEPT[qn] and len(options[qn]) == 4)
        continue
    target = ans[qn]
    scored = sorted((abs(pv_[0] - target), letter, pv_[1]) for letter, text in options[qn].items()
                    if (pv_ := option_value(text)) is not None)
    (best_err, best_l, tol), second_err = scored[0], scored[1][0]
    v.assert_true(f"Q{qn}: answer letter {letters.get(qn)} is the option closest to the computed value, within its precision",
                  len(scored) == 4 and best_l == letters.get(qn) and best_err <= tol * (1 + 1e-9) and second_err > best_err,
                  f"closest {best_l} (error {best_err:.3g}), options {options[qn]}")

numbers = sorted(int(n_) for n_ in re.findall(r"^\*\*(\d+)\.\*\*", readme, re.M))
v.assert_true("110 questions, numbered 1 to 110", numbers == list(range(1, 111)))
v.assert_true("every even-numbered question is multiple choice", set(range(2, 111, 2)) <= set(options))
v.assert_true("every multiple-choice question has an answer letter", set(options) <= set(letters))
numeric = set(range(1, 111)) - set(options)
v.assert_true("every numeric-entry question has a computed answer", numeric <= set(ans))
answered = {int(n_) for n_ in re.findall(r"^\*\*(\d+)\. Answer:", sol_text, re.M)}
v.assert_true("every question has a solution", answered == set(range(1, 111)))
v.assert_true("letters are spread across A-D", min(sum(1 for l_ in letters.values() if l_ == x) for x in "ABCD") >= 12)
counts = {"Mathematics": (1, 13), "Probability": (14, 17), "Ethics": (18, 21), "Economics": (22, 26),
          "Materials": (27, 30), "Circuits": (31, 44), "Linear systems": (45, 49), "Signal processing": (50, 54),
          "Electronics": (55, 62), "Power": (63, 71), "Electromagnetics": (72, 75), "Control": (76, 82),
          "Communications": (83, 87), "Networks": (88, 91), "Digital": (92, 101), "Computer systems": (102, 106),
          "Software": (107, 110)}
spec = {"Mathematics": (11, 17), "Probability": (4, 6), "Ethics": (4, 6), "Economics": (5, 8), "Materials": (4, 6),
        "Circuits": (11, 17), "Linear systems": (5, 8), "Signal processing": (5, 8), "Electronics": (7, 11),
        "Power": (8, 12), "Electromagnetics": (4, 6), "Control": (6, 9), "Communications": (5, 8),
        "Networks": (4, 6), "Digital": (8, 12), "Computer systems": (5, 8), "Software": (4, 6)}
v.assert_true("every area's question count is inside the NCEES range (tools/data/fe_spec.yml)",
              all(spec[k][0] <= b - a + 1 <= spec[k][1] for k, (a, b) in counts.items()))

sys.exit(v.finish())
