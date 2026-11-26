#!/usr/bin/env python3
"""Verify the Term 7 checkpoint: recompute every answer and check every multiple-choice letter.

Each value is recomputed by a route other than the hand formula where one exists:
- economics: explicit sums of discounted cash flows for every interest factor; brentq for the IRR; an amortization
  schedule that pays the test cell off exactly; monthly compounding stepped month by month;
- schedule and teams: Monte Carlo sampling of PERT (scaled beta) durations against the normal approximation; a
  simulated tape-out sequence for the respin delay; a search over integer team sizes; binomial review escapes;
- ethics: the exact fleet probability against the exponential approximation; scipy's chi-square bound for zero failures;
- systems: CAN bit counting by frame field; a step-by-step ring all-reduce simulation; summed MAC counts for the
  separable convolution;
- diligence: Bayes' rule by enumerating hypotheses; the Beta posterior from scipy; a finite-difference elasticity.
Multiple-choice options are parsed from README.md; for numeric options the script checks that the letter in
solutions.md is the only option matching the computed value to its printed precision. The two conceptual questions
are checked against the letters recorded below.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy import optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from eeverify import Verifier, parse_value  # noqa: E402

README, SOL = HERE / "README.md", HERE / "solutions.md"
v = Verifier.from_files("term-7", SOL)
ans: dict[int, float] = {}
RNG = np.random.default_rng(2607)
HOURS_YEAR = 8760.0
CONCEPT = {22: "B", 24: "A"}


def pv(flows, i):
    """Present value of end-of-period cash flows flows[0] at t = 1, flows[1] at t = 2, ..."""
    return sum(cf / (1 + i) ** (t + 1) for t, cf in enumerate(flows))


# ================================================================= block 1 · engineering economics
f1 = 10_000.0
for _ in range(8):
    f1 *= 1.06
ans[1] = f1 / 1e3
v.check("T7.01a", f1)

pa_8_10 = pv([1.0] * 10, 0.08)
v.check("T7.02a", pa_8_10)
v.check("T7.02b", 50_000 * pa_8_10)
ans[2] = 50_000 * pa_8_10 / 1e3

ap = 0.1 * 1.1 ** 5 / (1.1 ** 5 - 1)
af = ap - 0.1
cr = 2000 * ap - 200 * af
bal = 2000.0                                   # amortize: the cell, less salvage, is paid off by the CR payments
for _ in range(5):
    bal = bal * 1.1 - cr
v.assert_true("Q3: after five CR payments the balance left equals the salvage value", abs(bal - 200) < 1e-9, f"{bal:.6f}")
v.check("T7.03a", ap)
v.check("T7.03b", af)
v.check("T7.03c", 2000 * ap)
v.check("T7.03d", 200 * af)
ans[3] = cr

growth = 1.0
for _ in range(12):
    growth *= 1 + 0.12 / 12
ans[4] = 100 * (growth - 1)

pa_12_5 = pv([1.0] * 5, 0.12)
v.check("T7.05a", pa_12_5)
v.check("T7.05b", 15 * pa_12_5)
ans[5] = -40 + pv([15.0] * 5, 0.12)

irr = optimize.brentq(lambda r: -100 + pv([60, 60], r), 0.0, 1.0, xtol=1e-14)
v.check("T7.06a", 1 / (1 + irr))
v.check("T7.06b", 100 * irr)
v.assert_true("Q6: closed-form root agrees", abs((-60 + math.sqrt(60 ** 2 + 4 * 60 * 100)) / 120 - 1 / (1 + irr)) < 1e-10)
ans[6] = 100 * irr

ans[7] = 60e6 / (25 - 10) / 1e6
ans[8] = 0.25 * (5e6 - 1e6) / 8 / 1e3

after_asm = (20 + 5) / 0.98
c_good = (after_asm + 2) / 0.95
# second route: simulate 1e6 dies through assembly and test with expected losses
n0 = 1e6
spent = n0 * (20 + 5)
n_asm = n0 * 0.98
spent += n_asm * 2
n_good = n_asm * 0.95
v.assert_true("Q9: cost per good part from the flow equals the cascaded formula", abs(spent / n_good - c_good) < 1e-9)
v.check("T7.09a", c_good)
v.check("T7.09b", after_asm)
ans[9] = 100 * (1 - c_good / 60)

pv_build = 8 + 0.2 * 5
v.check("T7.10a", pv_build)
ans[10] = optimize.brentq(lambda u: (3 + 0.5 * u) - pv_build, 0, 100)

v.check("T7.11a", pv([0.4] * 3000, 0.08), tol=0.5)        # a long finite sum converges to A/i = 5
ans[11] = 3 + 0.4 / 0.08
v.assert_true("Q11: 3000-year sum is within 1e-9 of the perpetuity", abs(pv([0.4] * 3000, 0.08) - 5) < 1e-9)

ans[12] = 1.0 * 1.25 * 4 * HOURS_YEAR * 0.10 / 1e3

# ================================================================= block 2 · requirements, reviews, schedule, teams
i_avg = 0.99 * 5 + 0.01 * 2000                 # µA
life_h = 0.8 * 220 / (i_avg / 1000)
v.check("T7.13a", i_avg)
v.check("T7.13b", life_h)
v.check("T7.13c", 100 * 0.01 * 2000 / i_avg)
ans[13] = life_h / 24

samples = RNG.normal(0, 3, 400_000) + RNG.normal(0, 4, 400_000) + RNG.normal(0, 12, 400_000)
v.assert_true("Q14: sampled SD of the sum is 13 mV", abs(samples.std() - 13) < 0.1, f"{samples.std():.3f}")
ans[14] = math.sqrt(3 ** 2 + 4 ** 2 + 12 ** 2)

# Q15: expected escapes by enumerating how many reviewers catch each defect (binomial)
p_escape = stats.binom.pmf(0, 4, 0.4)
ans[15] = 50 * p_escape

a, m, b = 4.0, 6.0, 14.0
mu, sd = (a + 4 * m + b) / 6, (b - a) / 6
path_sd = sd * math.sqrt(3)
z16 = (24 - 3 * mu) / path_sd
v.check("T7.16a", path_sd)
v.check("T7.16b", z16)
v.check("T7.16c", sd)
ans[16] = 100 * stats.norm.cdf(z16)
# PERT-beta Monte Carlo: alpha = 1 + 4(m-a)/(b-a), beta = 1 + 4(b-m)/(b-a) has mean (a+4m+b)/6
al, be = 1 + 4 * (m - a) / (b - a), 1 + 4 * (b - m) / (b - a)
paths = sum(a + (b - a) * RNG.beta(al, be, 400_000) for _ in range(3))
mc16 = 100 * float(np.mean(paths <= 24))
v.assert_true("Q16: PERT-beta Monte Carlo within 3 points of the normal approximation", abs(mc16 - ans[16]) < 3,
              f"MC {mc16:.1f}% vs {ans[16]:.1f}%")

e_n = 1 + 0.7 / 0.8
v.check("T7.17a", e_n)
v.check("T7.17b", e_n - 1)
ans[17] = (e_n - 1) * 4
tries = np.ones(200_000)
ok = RNG.random(200_000) < 0.3
while not ok.all():
    idx = ~ok
    tries[idx] += 1
    ok[idx] = RNG.random(int(idx.sum())) < 0.8
v.assert_true("Q17: simulated respin delay within 0.05 months", abs((tries.mean() - 1) * 4 - ans[17]) < 0.05,
              f"{(tries.mean() - 1) * 4:.3f}")

ans[18] = sum(1 for i in range(20) for j in range(i + 1, 20))

c = 0.04
outputs = {n: n * (1 - c * (n - 1)) for n in range(1, 40)}
n_best = max(outputs, key=outputs.get)
v.assert_true("Q19: the integer search finds n* = (1 + 1/c)/2 = 13", n_best == 13 and abs((1 + 1 / c) / 2 - 13) < 1e-12)
v.check("T7.19a", n_best)
v.check("T7.19b", 1 + 1 / c)
v.check("T7.19c", 1 - c * (n_best - 1))
ans[19] = outputs[n_best]

v.check("T7.20a", (0.30 - 0.15) * 10)
ans[20] = (0.30 - 0.15) * 10 - 1.2

# ================================================================= block 3 · ethics, safety and IP
p_unit, n_units = 2e-7, 5e6
exact21 = -math.expm1(n_units * math.log1p(-p_unit))
v.assert_true("Q21: exponential approximation within 1e-6", abs(exact21 - (1 - math.exp(-p_unit * n_units))) < 1e-6)
ans[21] = 100 * exact21

v.check("T7.23a", -math.log(0.05))
# chi-square route: zero failures, bound = chi2(C, 2)/(2T)
ans[23] = stats.chi2.ppf(0.95, 2) / (2 * 3e8) * 1e9
v.assert_true("Q23: chi-square(0.95, 2)/2 equals -ln 0.05", abs(stats.chi2.ppf(0.95, 2) / 2 + math.log(0.05)) < 1e-9)

start_year = min(2021, 2022)                    # earlier of first commercial exploitation and registration
v.assert_true("Q25: registration within two years of first exploitation", (2022 + 1 / 12) - (2021 + 2.5 / 12) < 2)
ans[25] = start_year + 10

mactops = 1000 / 2
ans[26] = 2 * mactops * 8
v.assert_true("Q26: TPP 8000 is above the 3A090.a.1 threshold of 4800", ans[26] >= 4800)

# ================================================================= block 4 · system architectures
rails = [(1.2, 0.9), (0.5, 0.85), (0.3, 1.2 / 1.8)]
from_batt = [pw / eta for pw, eta in rails]
v.check("T7.27a", from_batt[0])
v.check("T7.27b", from_batt[1])
v.check("T7.27c", from_batt[2])
ans[27] = sum(from_batt)

ans[28] = (43 - 25) / 6
ans[29] = 8533e6 * 64 / 8 / 1e9
weight_bytes = 8e9 * 4 / 8
v.check("T7.30a", weight_bytes / 1e9)
ans[30] = 68.3e9 / weight_bytes

e_b = 0.3 * 3.85
e_day = 0.020 * 2 + 0.002 * 24 + 0.005 * 1 + 0.0006 * 24
v.check("T7.31a", e_day)
v.check("T7.31b", e_b)
ans[31] = 0.9 * 0.85 * e_b / e_day

res32 = abs(1 - np.exp(-2j * np.pi * 500 * 50e-6))   # |1 - g e^{-j phi}| with g = 1
v.assert_true("Q32: complex residual equals 2|sin(pi f tau)|", abs(res32 - 2 * math.sin(math.pi * 500 * 50e-6)) < 1e-12)
v.check("T7.32a", 1 / (6 * 50e-6) / 1e3)
v.check("T7.32b", res32)
ans[32] = -20 * math.log10(res32)

# Q33: count fields of a classic CAN data frame (11-bit id), then worst-case stuff bits on the stuffed region
sof, ident, rtr, ide, r0, dlc, crc = 1, 11, 1, 1, 1, 4, 15
stuffed_region = sof + ident + rtr + ide + r0 + dlc + 8 * 8 + crc         # 34 + 8n bits are subject to stuffing
tail = 1 + 1 + 1 + 7 + 3                       # CRC delimiter, ACK slot, ACK delimiter, EOF, interframe space
stuff = (stuffed_region - 1) // 4
v.assert_true("Q33: field count matches 34 + 8n and 13", stuffed_region == 34 + 64 and tail == 13)
v.check("T7.33a", stuffed_region + tail + stuff)
v.check("T7.33b", stuff)
ans[33] = (stuffed_region + tail + stuff) / 500e3 * 1e6

ans[34] = 30 * 0.1 + 30 ** 2 / (2 * 7)
v.check("T7.34a", 30 * 0.010)

load = 8 * (8 * 1.0 + 2) + 6
v.check("T7.35b", load)
v.check("T7.35a", load / 0.95)
ans[35] = load / 0.95 * 1.2

flops = 6 * 70e9 * 2e12
rate = 4096 * 1e15 * 0.4
v.check("T7.36a", flops)
v.check("T7.36b", flops / rate)
v.check("T7.36c", rate)
ans[36] = flops / rate / 86400


def ring_allreduce_time(p, size, bw):
    """Simulate reduce-scatter then all-gather: 2(p - 1) steps, each moving one chunk of size/p per link."""
    chunk = size / p
    t = 0.0
    for _ in range(2 * (p - 1)):
        t += chunk / bw
    return t


ans[37] = ring_allreduce_time(8, 12e9, 400e9) * 1e3
v.assert_true("Q37: simulation equals 2(p-1)/p S/B", abs(ans[37] - 2 * 7 / 8 * 12 / 400 * 1e3) < 1e-9)

H = W = 32
cin = cout = 64
k = 3
std_macs = H * W * cout * k * k * cin
ds_macs = H * W * cin * k * k + H * W * cin * cout
ans[38] = 100 * ds_macs / std_macs
v.assert_true("Q38: summed MACs equal 1/C_out + 1/k^2", abs(ds_macs / std_macs - (1 / cout + 1 / k ** 2)) < 1e-12)

# ================================================================= block 5 · technical diligence
odds39 = 0.3 / 0.7 * 3 * 0.4 * 2
v.check("T7.39a", odds39)
ans[39] = 100 * odds39 / (1 + odds39)

# Q40 by enumeration over a population of 1,000 troubled and 1,000 healthy targets
troubled_absent, healthy_absent = 1000 * (1 - 0.6), 1000 * (1 - 0.1)
ans[40] = (troubled_absent / 1000) / (healthy_absent / 1000)

post = stats.beta(1.4 + 4, (10 - 1.4) + (5 - 4))
ans[41] = 100 * post.mean()

ridge = 2e15 / 4e12
intensity = 2 * 16 / 1
attain = min(2e15, intensity * 4e12)
v.check("T7.42a", ridge)
v.check("T7.42b", intensity)
v.check("T7.42c", attain / 1e12)
ans[42] = 100 * attain / 2e15

fr = 1.25 / 1.1
v.check("T7.43a", fr ** 3)
v.check("T7.43b", 100 * (1 - 1 / 1.25))
v.check("T7.43c", fr)
ans[43] = 100 * (1 - 1 / fr ** 3)


def die_cost(area, d0=0.001):
    return area * math.exp(area * d0)          # proportional to cost, ignoring the edge term


h = 1e-6
ans[44] = (math.log(die_cost(400 * (1 + h))) - math.log(die_cost(400 * (1 - h)))) / (math.log(1 + h) - math.log(1 - h))
v.assert_true("Q44: finite difference equals 1 + AD0", abs(ans[44] - 1.4) < 1e-6)

v.check("T7.45a", 200 * 3 / 12)
v.check("T7.45b", 0.5 * 200 * 3 / 12)
ans[45] = 0.5 * 200 * 3 / 12 + 15

ans[46] = 50e-9 * 2e6 * HOURS_YEAR
ans[47] = (0.900 - 0.750) * 1.3 * 5 * HOURS_YEAR * 0.09

shares = [0.40, 0.25, 0.15, 0.10, 0.10]
hhi = sum(s * s for s in shares)
v.assert_true("Q48: shares sum to 1", abs(sum(shares) - 1) < 1e-12)
v.check("T7.48a", hhi)
ans[48] = 1 / hhi

planned = pv([40.0] * 5, 0.10)
late = pv([0.0] + [0.8 * 40.0] * 5, 0.10)       # same flows, one year later, 80% realized
v.check("T7.49a", planned)
v.check("T7.49b", 100 * (1 - late / planned))
v.check("T7.49c", pv([1.0] * 5, 0.10))
ans[49] = late
v.assert_true("Q49: shifted sum equals 0.8 x planned / 1.1", abs(late - 0.8 * planned / 1.1) < 1e-9)

ans[50] = float(np.mean([(0.9 - o) ** 2 for o in (1, 1, 1, 1, 0)]))

for qn, value in sorted(ans.items()):
    v.check(f"T7.{qn:02d}", value)

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


for qn in range(2, 51, 2):
    if qn in CONCEPT:
        v.assert_true(f"Q{qn}: conceptual answer letter is {CONCEPT[qn]}",
                      letters.get(qn) == CONCEPT[qn] and len(options.get(qn, {})) == 4)
        continue
    target = ans[qn]
    scored = sorted((abs(pv_[0] - target), letter, pv_[1]) for letter, text in options[qn].items()
                    if (pv_ := option_value(text)) is not None)
    (best_err, best_l, tol), second_err = scored[0], scored[1][0]
    v.assert_true(f"Q{qn}: answer letter {letters.get(qn)} is the option closest to the computed value, within its precision",
                  len(scored) == 4 and best_l == letters.get(qn) and best_err <= tol * (1 + 1e-9) and second_err > best_err,
                  f"closest {best_l} (error {best_err:.3g}), options {options[qn]}")
v.assert_true("every multiple-choice question has an answer letter", set(options) <= set(letters))
v.assert_true("50 questions, numbered 1 to 50",
              sorted(int(n_) for n_ in re.findall(r"^\*\*(\d+)\.\*\*", readme, re.M)) == list(range(1, 51)))
v.assert_true("even-numbered questions are multiple choice, odd ones numeric entry",
              set(options) == set(range(2, 51, 2)))
answered = {int(n_) for n_ in re.findall(r"^\*\*(\d+)\. Answer:", sol_text, re.M)}
v.assert_true("every question has a solution", answered == set(range(1, 51)))
v.assert_true("letters are spread across A-D", min(sum(1 for l_ in letters.values() if l_ == x) for x in "ABCD") >= 4)

sys.exit(v.finish())
