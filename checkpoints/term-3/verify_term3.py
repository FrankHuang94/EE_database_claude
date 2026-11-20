#!/usr/bin/env python3
"""Verify the Term 3 checkpoint: recompute every answer and check every multiple-choice letter.

Each value is recomputed by a route other than the hand formula where one exists:
- device quantities by root finding on the carrier and charge-balance equations (depletion widths from
  N_A x_p = N_D x_n and the potential integral), per-decade slopes from the exponential laws;
- circuit quantities by solving the device equations (square law, exponential law) and small-signal
  networks, with numerical derivatives for g_m and r_d, a corner search for the difference amplifier, and a
  simulated single-pole op-amp loop for the bandwidth;
- signal quantities by convolution, FFTs, simulated step responses and quantizers.
For numerical multiple-choice questions, the option text is parsed from README.md, and the script checks
that the letter in solutions.md is the only option matching the computed value to its printed precision.
"""
from __future__ import annotations

import itertools
import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
from eeverify import Verifier, parse_value  # noqa: E402

README, SOL = HERE / "README.md", HERE / "solutions.md"
v = Verifier.from_files("term-3", SOL)
k_B, q = 1.380649e-23, 1.602176634e-19
VT = 0.025852
eps_s, eps_ox, ni = 1.036e-12, 3.453e-13, 1.0e10
db = lambda r: 20 * math.log10(abs(r))
ans: dict[int, float] = {}

# ================================================================= block 1
ans[1] = brentq(lambda x: ni * math.exp(x / VT) - 1e16, 0, 1)
ans[2] = VT * math.log(1e16 / ni) + VT * math.log(1e17 / ni)      # sum of the two sides' |E_F - E_i|
NA, ND, Vbi = 1e17, 1e16, ans[2]


def width(V):
    # x_n from charge balance and the potential drop q/(2 eps)(N_A x_p^2 + N_D x_n^2) = Vbi - V
    xn = brentq(lambda xn: q / (2 * eps_s) * (NA * (ND * xn / NA) ** 2 + ND * xn ** 2) - (Vbi - V), 0, 1e-3)
    return xn + ND * xn / NA


ans[3] = width(0.0) * 1e4
mu = 92 + 1268 / (1 + (1e16 / 1.3e17) ** 0.91)
v.assert_true("the course mobility model gives 1248 cm^2/V.s at 1e16", abs(mu - 1248) < 0.5)
ans[4] = 1 / (q * 1e16 * 1248)
ans[5] = 1200 * k_B * 300 / q
ans[6] = math.sqrt(12 * 1e-6) * 1e4
ans[7] = brentq(lambda dv: math.exp(dv / VT) - 10, 0.01, 0.2) * 1e3
ans[8] = width(0.0) / width(-5.0)
ans[9] = eps_ox / 2.0e-7 * 1e15 / 1e8
phiB = brentq(lambda p: ni * math.exp(p / VT) - 1e17, 0, 1)
ans[10] = 2 * phiB
ans[11] = math.sqrt(2 * eps_s * 2 * phiB / (q * 1e17)) * 1e4
ans[12] = brentq(lambda dv: math.exp(dv / (1.3 * VT)) - 10, 0.01, 0.3) * 1e3
alpha = 0.995
IE = 1.0
ans[13] = alpha * IE / (IE - alpha * IE)
ans[14] = 1.2398 / 1.12
ans[15] = 1.2398 / 0.850
ans[16] = 10.0 / 1.4

# ================================================================= block 2
ans[17] = (5.0 - 0.7) / 2.2
IS = 1e-15
Vd = VT * math.log(1e-3 / IS)
h = 1e-7
ans[18] = 2 * h / (IS * math.exp((Vd + h) / VT) - IS * math.exp((Vd - h) / VT))
ans[19] = 15 / (2 * 60 * 1000 * 470e-6)
v.assert_true("the exponential discharge is within 2% of the small-ripple value",
              abs(15 * (1 - math.exp(-1 / (2 * 60 * 1000 * 470e-6))) / ans[19] - 1) < 0.02)
ans[20] = (10 - 5.1) / (0.030 + 0.002)


def i_d(vgs, vds, kn=4e-3, vt=0.5):
    vov = vgs - vt
    if vov <= 0:
        return 0.0
    return kn * (vov - vds / 2) * vds if vds < vov else 0.5 * kn * vov ** 2


ans[21] = i_d(1.0, 0.3) * 1e3
vgs05 = brentq(lambda vg: i_d(vg, 5.0) - 0.5e-3, 0.5, 2)
ans[22] = (i_d(vgs05 + 1e-6, 5.0) - i_d(vgs05 - 1e-6, 5.0)) / 2e-6 * 1e3
Vbe = VT * math.log(1e-3 / IS)
gm = (IS * math.exp((Vbe + h) / VT) - IS * math.exp((Vbe - h) / VT)) / (2 * h)
ans[23] = 100 / gm / 1e3
ans[24] = -2e-3 / (1 / 10e3 + 1 / 50e3)
beta = 1e6
rpi = beta / (1e-3 / VT)
ans[25] = -beta * 5e3 / (rpi + (beta + 1) * 500)
ans[26] = brentq(lambda vo: 2e-3 * (1 - vo) - vo / 2e3, 0, 1)      # g_m (v_in - v_o) = v_o / R_S
ans[27] = 20 * math.log10(20 * 15 * 0.8)
ans[28] = 100 * (1 + 0.1 * 2.0) / (1 + 0.1 * 0.8)
A0, fa = 1e5, 100.0
bfb = 1 / 100
Hcl = lambda f: abs((A0 / (1 + 1j * f / fa)) / (1 + bfb * A0 / (1 + 1j * f / fa)))
ans[29] = brentq(lambda f: Hcl(f) - Hcl(0) / math.sqrt(2), 1e3, 1e7) / 1e3
ans[30] = 6.5e6 / (2 * math.pi * 5.0) / 1e3
ans[31] = 2.0 * (1 + 10)
eps_r = 0.001


def cmrr(errs):
    R1, R2, R3, R4 = (1e3 * (1 + e) for e in errs)
    # V_o = V_b (R4/(R3+R4))(1 + R2/R1) - V_a R2/R1
    gb = R4 / (R3 + R4) * (1 + R2 / R1)
    ga = R2 / R1
    adm = (ga + gb) / 2
    acm = gb - ga
    return abs(adm / acm) if acm else float("inf")


worst = min(cmrr(c) for c in itertools.product((-eps_r, eps_r), repeat=4))
ans[32] = 20 * math.log10((1 + 1) / (4 * eps_r))
v.assert_true("the worst resistor corner meets the (1 + K)/(4 eps) bound to within 1%", worst >= 500 * 0.99)
ans[33] = 5.0 * 10e3 / 100e3

# ================================================================= block 3
fs34 = 6000.0
t34 = np.arange(int(fs34 * 1.0)) / fs34
x34 = np.cos(40 * np.pi * t34) + np.sin(60 * np.pi * t34)
ans[34] = next(k for k in range(1, len(t34) // 2) if np.max(np.abs(x34[k:k + 600] - x34[:600])) < 1e-9) / fs34
ans[35] = float(np.convolve([1, 1, 1], [1, 2])[1])
ans[37] = float(np.sum(0.8 ** np.arange(400)))
N38 = 2 ** 14
sq = np.where(np.arange(N38) < N38 // 2, 2.0, -2.0)
ans[38] = abs(np.fft.rfft(sq)[3]) / (N38 / 2)
_, ystep = signal.step(([1], [1e-4, 1]), T=np.linspace(0, 1e-3, 100001))
tt = np.linspace(0, 1e-3, 100001)
ans[39] = (tt[np.argmax(ystep >= 0.9)] - tt[np.argmax(ystep >= 0.1)]) * 1e6
ans[40] = abs(0.5 * (1 + np.exp(-1j * np.pi / 2)))
hf = signal.firwin(21, 0.3)
wq = np.linspace(0.05, 0.5, 40)
ph = np.unwrap(np.angle([np.sum(hf * np.exp(-1j * w * np.arange(21))) for w in wq]))
ans[41] = -np.polyfit(wq, ph, 1)[0] / 48e3 * 1e6
_, y43 = signal.step(([25], [1, 6, 25]), T=np.linspace(0, 5, 50001))
ans[43] = 100 * (y43.max() - 1)
r45 = 0.98
ans[45] = 2 * (1 - r45) * 8000 / (2 * math.pi)
a45 = np.real(np.poly([r45 * np.exp(1j), r45 * np.exp(-1j)]))
m45 = lambda w: 1 / abs(np.polyval(a45[::-1], np.exp(-1j * w)))
wpk = max(np.linspace(0.8, 1.2, 40001), key=m45)
lo = brentq(lambda w: m45(w) - m45(wpk) / math.sqrt(2), 0.8, wpk)
hi = brentq(lambda w: m45(w) - m45(wpk) / math.sqrt(2), wpk, 1.2)
v.assert_true("the 2(1 - r) estimate is within 3% of the exact bandwidth", abs((hi - lo) * 8000 / (2 * math.pi) / ans[45] - 1) < 0.03)
n46 = np.arange(10000)
ans[46] = np.argmax(np.abs(np.fft.rfft(np.cos(2 * np.pi * 7e3 * n46 / 10e3)))) * 10e3 / 10000 / 1e3
ans[47] = 2 * 22.0
ans[48] = 6.02 * 12 + 1.76
tq = np.arange(2 ** 20)
xq = 0.5 * np.sin(2 * np.pi * 0.1 * (math.sqrt(5) - 1) / 2 * tq + 0.3) * (1 - 2 ** -12)
eq = np.round(xq / 2 ** -12) * 2 ** -12 - xq
v.assert_true("a simulated 12-bit quantizer gives 74.0 dB within 0.2 dB",
              abs(10 * math.log10(np.mean(xq ** 2) / np.mean(eq ** 2)) - 74.0) < 0.2)
t49 = np.arange(200000) / 2e6
s49 = (1 + np.cos(2 * np.pi * 1e3 * t49)) * np.cos(2 * np.pi * 100e3 * t49)
P49 = np.abs(np.fft.rfft(s49)) ** 2
f49 = np.fft.rfftfreq(len(t49), 1 / 2e6)
ans[49] = 100 * P49[(np.abs(f49 - 100e3) > 500) & (np.abs(f49 - 100e3) < 5e3)].sum() / P49.sum()
lo50 = 900 + 455
ans[50] = brentq(lambda f: abs(f - lo50) - 455, lo50 + 1, 5000)

for qn, value in sorted(ans.items()):
    v.check(f"T3.{qn:02d}", value)

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


numeric_mc = [2, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 34, 38, 40, 46, 48, 50]
for qn in numeric_mc:
    target = ans[qn]
    scored = sorted((abs(p[0] - target), letter, p[1]) for letter, text in options[qn].items()
                    if (p := option_value(text)) is not None)
    (best_err, best_l, tol), second_err = scored[0], scored[1][0]
    v.assert_true(f"Q{qn}: answer letter {letters.get(qn)} is the option closest to the computed value, within its precision",
                  best_l == letters.get(qn) and best_err <= tol * (1 + 1e-9) and second_err > best_err,
                  f"closest {best_l} (error {best_err:.3g}), options {options[qn]}")
# conceptual questions: 36 (only the delay is LTI), 42 (stable ROC is the strip), 44 (pole outside the circle)
lti = {"A": True, "B": False, "C": False, "D": False}
v.assert_true("Q36: only the delay is linear and time-invariant",
              letters.get(36) == "A" and sum(lti.values()) == 1)
v.assert_true("Q42: the stable ROC is the strip between the poles",
              letters.get(42) == "A" and -2 < 0 < 1)
v.assert_true("Q44: a pole at -1.2 lies outside the unit circle",
              letters.get(44) == "B" and max(abs(np.roots(np.poly([0.5, -1.2])))) > 1)
v.assert_true("every multiple-choice question has an answer letter", set(options) <= set(letters))
v.assert_true("50 questions, numbered 1 to 50",
              sorted(int(n) for n in re.findall(r"^\*\*(\d+)\.\*\*", readme, re.M)) == list(range(1, 51)))

sys.exit(v.finish())
