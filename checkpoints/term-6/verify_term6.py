#!/usr/bin/env python3
"""Verify the Term 6 checkpoint: recompute every answer and check every multiple-choice letter.

Each value is recomputed by a route other than the hand formula where one exists:
- digital: numerical minimization of path delay over stage sizes; an RC-ladder transient for the wire delay;
- analog: integrating the thermal-noise spectrum of an RC for kT/C; quantizing and jitter-sampling synthetic sines;
  the diode equation for the PTAT voltage;
- RF: noise temperatures for the cascade; impedance arithmetic for the L-match; intercept lines solved for IIP3;
  numerical integration of half-sine currents for class B;
- power: volt-second balance by root-finding for the boost; phasor arithmetic for power flow, per-unit and faults;
- memory: charge conservation on the bitline; root-finding on the MRAM flip budget;
- I/O: the binomial zero-error condition solved exactly; the dielectric loss from its Np/m form as a cross-check;
- fabrication: Bayes' rule by enumerating die classes for escapes; scipy's chi-square quantile for the FIT bound.
For multiple-choice questions the option text is parsed from README.md, and the script checks that the letter in
solutions.md is the only option matching the computed value to its printed precision.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from eeverify import Verifier, parse_value  # noqa: E402

README, SOL = HERE / "README.md", HERE / "solutions.md"
v = Verifier.from_files("term-6", SOL)
ans: dict[int, float] = {}
K_J, K_EV, C0 = 1.381e-23, 8.617e-5, 2.998e8
VT = 0.02585
db = lambda x: 10 ** (x / 10)  # noqa: E731

# ================================================================= block 1 · digital VLSI
# Q1: energy drawn from the supply per 0->1 transition is C V^2; alpha full cycles per clock
ans[1] = 0.15 * 2e9 * (2e-9 * 0.8 * 0.8)
# Q2: minimize d = sum(g_i h_i + p_i) over the two internal capacitances
g, p, H = [1, 4 / 3, 5 / 3], [1, 2, 2], 12.0


def path_delay(x):
    c1, c2 = np.exp(x)                    # internal loads relative to the path input capacitance (1)
    caps = [1.0, c1, c2, H]
    return sum(g[i] * caps[i + 1] / caps[i] + p[i] for i in range(3))


res = optimize.minimize(path_delay, x0=[1.0, 2.0], method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-12})
ans[2] = res.fun
v.assert_true("Q2: numerical optimum equals 3 F^(1/3) + P", abs(res.fun - (3 * (20 / 9 * 12) ** (1 / 3) + 5)) < 1e-6)
# Q3: the composite formula, and an RC-ladder transient as a sanity check
ans[3] = (0.69 * 1e3 * 210e-15 + 500 * (0.38 * 200e-15 + 0.69 * 10e-15)) * 1e12
nseg = 100
Rs, Cs = 500 / nseg, 200e-15 / nseg


def ladder(t, vv):
    i_in = (1.0 - vv[0]) / (1e3 + Rs / 2)
    dv = np.empty(nseg)
    for kk in range(nseg):
        i_out = (vv[kk] - vv[kk + 1]) / Rs if kk < nseg - 1 else 0.0
        i_prev = i_in if kk == 0 else (vv[kk - 1] - vv[kk]) / Rs
        c = Cs + (10e-15 if kk == nseg - 1 else 0.0)
        dv[kk] = (i_prev - i_out) / c
    return dv


sol = integrate.solve_ivp(lambda t, y: ladder(t, y), (0, 1.5e-9), np.zeros(nseg), method="LSODA", rtol=1e-8, atol=1e-11,
                          dense_output=True)
t50 = optimize.brentq(lambda t: sol.sol(t)[-1] - 0.5, 1e-12, 1.5e-9) * 1e12
v.assert_true("Q3: the ladder transient's 50% delay is within 10% of the composite estimate", abs(t50 / ans[3] - 1) < 0.10,
              f"{t50:.1f} ps")
ans[4] = 1 / (60 + 350 + 40 + 20) * 1e3
ans[5] = (1 - math.exp((1 - 0.98) * math.log(0.8))) * 1e6
v.assert_true("Q5: the (1 - T)(-ln Y) approximation agrees within 1%",
              abs(0.02 * -math.log(0.8) * 1e6 / ans[5] - 1) < 0.01)
# Q6: subthreshold current I0 exp((VGS - VTH)/(n VT)) with n set by S = n VT ln 10
n6 = 0.090 / (VT * math.log(10))
ans[6] = math.exp(0.060 / (n6 * VT))
ans[7] = math.exp(400 / 20) / (20e-12 * 2e9 * 1e8)

# ================================================================= block 2 · analog and mixed-signal
# Q8: EKV gm/ID = 1/(n VT (1 + q)) as q -> 0
ans[8] = 1 / (1.3 * VT * (1 + 1e-12))
# Q9: the integrator gm/(s Cc) reaches unity gain where |gm/(j w Cc)| = 1
ans[9] = optimize.brentq(lambda f: 1e-3 / (2 * math.pi * f * 2e-12) - 1, 1e6, 1e9) / 1e6
ans[10] = 100e-6 / 2e-12 / 1e6
# Q11: integrate 4kTR over the RC low-pass and take the root
R11 = 1e3
psd = lambda f: 4 * K_J * 300 * R11 / (1 + (2 * math.pi * f * R11 * 2e-12) ** 2)  # noqa: E731
fc = 1 / (2 * math.pi * R11 * 2e-12)
var = fc * integrate.quad(lambda u: psd(u * fc), 0, np.inf, limit=500)[0]   # substitute f = u fc
ans[11] = math.sqrt(var) * 1e6
v.assert_true("Q11: integrated noise equals sqrt(kT/C)", abs(ans[11] / (math.sqrt(K_J * 300 / 2e-12) * 1e6) - 1) < 1e-4)
ans[12] = 6.02 * 12 + 1.76
nq = 1 << 16
x12 = np.sin(2 * np.pi * 1001 / nq * np.arange(nq)) * (2 ** 11 - 0.5)
err = np.round(x12) - x12
v.assert_true("Q12: a quantized full-scale sine has SQNR within 0.2 dB of 74.0",
              abs(10 * math.log10(np.mean(x12 ** 2) / np.mean(err ** 2)) - 74.0) < 0.2)
ans[13] = -20 * math.log10(2 * math.pi * 1e8 * 1e-13)
rng = np.random.default_rng(6)
tt = np.arange(200000) / 1e9 + rng.normal(0, 1e-13, 200000)
e13 = np.sin(2 * np.pi * 1e8 * tt) - np.sin(2 * np.pi * 1e8 * np.arange(200000) / 1e9)
v.assert_true("Q13: jitter-sampled sine has SNR within 0.2 dB of the formula",
              abs(10 * math.log10(0.5 / np.mean(e13 ** 2)) - ans[13]) < 0.2)
# Q14: V_BE = VT ln(I / (A Is)); equal currents, areas 1 and 8
Is = 1e-16
ans[14] = (VT * math.log(1e-5 / Is) - VT * math.log(1e-5 / (8 * Is))) * 1e3

# ================================================================= block 3 · RF
T0 = 290.0
te = [(db(1.5) - 1) * T0, (db(10) - 1) * T0, (db(15) - 1) * T0]
te_tot = te[0] + te[1] / db(15) + te[2] / (db(15) * db(8))
ans[15] = 10 * math.log10(1 + te_tot / T0)
ans[16] = 10 * math.log10(K_J * T0 * 20e6 / 1e-3) + 6 + 10
v.assert_true("Q16: kT0 is -174 dBm/Hz to 0.05 dB", abs(10 * math.log10(K_J * T0 / 1e-3) + 174) < 0.05)
gam = (75 - 50) / (75 + 50)
ans[17] = -20 * math.log10(abs(gam))
vswr = (1 + gam) / (1 - gam)
w18 = 2 * math.pi * 2.4e9
L18 = optimize.brentq(lambda L: (1 / (10 + 1j * w18 * L)).real - 1 / 50, 1e-12, 1e-8, xtol=1e-22, rtol=1e-15)
Csh = -(1 / (10 + 1j * w18 * L18)).imag / w18
zin = 1 / (1j * w18 * Csh + 1 / (10 + 1j * w18 * L18))
v.assert_true("Q18: the L-match presents 50 ohms", abs(zin - 50) < 1e-6)
ans[18] = L18 * 1e9
ans[19] = -10 * math.log10((C0 / 5.8e9 / (4 * math.pi * 100)) ** 2)
ans[20] = optimize.brentq(lambda P: (-5 + (P + 20)) - (-55 + 3 * (P + 20)), -50, 50)
th = np.linspace(0, 2 * math.pi, 200001)[:-1]
i_load = 0.5 * np.cos(th)                       # half amplitude into a 1-ohm load, supplies +-1 V (VDD = 1)
p_out = np.mean(i_load ** 2)                    # average power in the load
p_dc = 1.0 * np.mean(np.abs(i_load))            # each half-sine current is drawn from its own 1 V supply
ans[21] = 100 * p_out / p_dc
v.assert_true("Q21: integrated class-B efficiency equals (pi/4) x", abs(ans[21] - 100 * math.pi / 4 * 0.5) < 1e-3)

# ================================================================= block 4 · power
D22 = 1.2 / 12
ans[22] = (12 - 1.2) * D22 / (5e5 * 1e-6)
ans[23] = optimize.brentq(lambda d: 5 * d + (5 - 12) * (1 - d), 0, 1)
ans[24] = 1000 / 0.95 - 1000
ans[25] = (10e6 / 3) / (13.8e3 / math.sqrt(3))
ib = 100e6 / (math.sqrt(3) * 138e3)
zb = (138e3 / math.sqrt(3)) / ib
ans[26] = 20 / zb
v1, v2 = 1.0, np.exp(-1j * math.radians(20))
ans[27] = (v1 * np.conj((v1 - v2) / (1j * 0.5))).real
ans[28] = 100 * (120 * 60 / 4 - 1746) / (120 * 60 / 4)
zb29 = 13.8e3 ** 2 / 100e6
i_f = (13.8e3 / math.sqrt(3)) / (0.1 * zb29)
ans[29] = i_f / 1e3

# ================================================================= block 5 · memory
q_tot = 20e-15 * 1.1 + 80e-15 * 0.55
ans[30] = (q_tot / 100e-15 - 0.55) * 1e3
ans[31] = 100 * 350 / 3900
ans[32] = 1024 * 9.6e9 / 8 / 1e12
ans[33] = 1e12 * 100e-9 / 1e3
levels = np.linspace(0, 6, 8)
ans[34] = float(np.diff(levels)[0])
tbw = 2 * 3000 / 3
ans[35] = tbw / (1.92 * 365 * 5)
yrs = 10 * 365.25 * 86400
ans[36] = optimize.brentq(lambda d: 1e8 * yrs * 1e9 * math.exp(-d) - 1, 1, 200)

# ================================================================= block 6 · high-speed I/O
ans[37] = 112e9 / 2 / 2 / 1e9
gam38 = (100 - 85) / (100 + 85)
ans[38] = gam38
ans[39] = 2 * 7.03 * 0.5 + 3
v.assert_true("Q39: Q^-1(1e-12) = 7.03", round(stats.norm.isf(1e-12), 2) == 7.03)
n40 = math.log(0.05) / math.log1p(-1e-12)
ans[40] = n40 / 100e9
ans[41] = 2.3 * 28 * 0.002 * math.sqrt(3.4)
np_m = math.pi * 28e9 * math.sqrt(3.4) * 0.002 / C0
v.assert_true("Q41: the rule matches the Np/m form within 1%", abs(np_m * 8.686 * 0.0254 / ans[41] - 1) < 0.01)
ans[42] = 16 / 800e9 * 1e12
ans[43] = 32e9 * 16 * 128 / 130 / 8 / 1e9

# ================================================================= block 7 · fabrication and reliability
ans[44] = 0.30 * 13.5 / 0.33
dpw = math.floor(math.pi * 300 ** 2 / (4 * 200) - math.pi * 300 / math.sqrt(2 * 200))
ans[45] = 17000 / (dpw * math.exp(-200 / 100 * 0.1))
ans[46] = math.exp(0.7 / K_EV * (1 / (55 + 273.15) - 1 / (125 + 273.15)))
chi = stats.chi2.ppf(0.90, 2)
v.assert_true("Q47: chi-square(0.90, 2) = 4.605", round(chi, 3) == 4.605)
ans[47] = chi / (2 * 1000 * 1000 * 50) * 1e9
ans[48] = 35 + 300 * (0.05 + 0.03 + 0.10)
classes = {("good", "pass"): 0.8 * 1.0, ("bad", "pass"): 0.2 * 0.01, ("bad", "fail"): 0.2 * 0.99}
passing = sum(pr for (q, r), pr in classes.items() if r == "pass")
ans[49] = 1e6 * classes[("bad", "pass")] / passing
lam, safe, dc = 200.0, 50.0, 0.98
ans[50] = 100 * (1 - (lam - safe) * (1 - dc) / lam)

for qn, value in sorted(ans.items()):
    v.check(f"T6.{qn:02d}", value)
v.check("T6.17a", vswr)
v.check("T6.26a", zb)
v.check("T6.33a", 1e12 * 100e-9)
v.check("T6.35a", tbw)
v.check("T6.36a", yrs)
v.check("T6.38a", -20 * math.log10(gam38))
v.check("T6.40a", n40)
v.check("T6.45a", dpw)

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
    target = ans[qn]
    scored = sorted((abs(pv[0] - target), letter, pv[1]) for letter, text in options[qn].items()
                    if (pv := option_value(text)) is not None)
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

sys.exit(v.finish())
