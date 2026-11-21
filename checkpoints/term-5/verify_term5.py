#!/usr/bin/env python3
"""Verify the Term 5 checkpoint: recompute every answer and check every multiple-choice letter.

Each value is recomputed by a route other than the hand formula where one exists:
- control by simulating step responses (scipy.signal), root finding on loop gains, numerical Routh checks through
  polynomial roots, state-space DC gains by solving A x = -B u, and exact zero-order-hold discretization;
- DSP by FFTs of synthetic tones (aliases, bins, window main lobes), counting the radix-2 butterflies, filter
  group delay measured from the impulse response, polynomial roots for stability, Q15 integer arithmetic, and the
  bilinear map checked by evaluating the analog and digital responses;
- communications by stage-by-stage noise accounting, Monte Carlo BPSK, an exact free-space link from the Friis
  transmission equation, the Hamming code by exhaustive syndrome decoding, ipaddress for subnets, and ALOHA by
  maximizing its throughput curve;
- embedded systems by the Course 18 lab models (wait states, rise time by root finding, the RTOS scheduler and the
  ping-pong simulator) and binary search by counting comparisons.
For numerical multiple-choice questions the option text is parsed from README.md, and the script checks that the
letter in solutions.md is the only option matching the computed value to its printed precision; for the four
non-numerical ones it checks the keyed option against the computed facts.
"""
from __future__ import annotations

import importlib.util
import ipaddress
import itertools
import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from eeverify import Verifier, parse_value  # noqa: E402

LABS18 = ROOT / "courses" / "18-embedded-systems-and-microcontrollers" / "labs"


def lab(name, sub):
    spec = importlib.util.spec_from_file_location(name, LABS18 / sub / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


ma, dm, rs = lab("mcuarch", "18-01-lab"), lab("dmasim", "18-04-lab"), lab("rtsched", "18-07-lab")

README, SOL = HERE / "README.md", HERE / "solutions.md"
v = Verifier.from_files("term-5", SOL)
ans: dict[int, float] = {}
facts: dict[int, object] = {}

# ================================================================= block 1 · control systems
wn, zeta = 10.0, 0.4
t = np.linspace(0, 6, 60001)
_, y = signal.step(signal.TransferFunction([wn ** 2], [1, 2 * zeta * wn, wn ** 2]), T=t)
ans[1] = 100 * (y.max() - 1)
v.assert_true("Q1: simulated overshoot equals exp(-zeta pi / sqrt(1 - zeta^2))",
              abs(ans[1] - 100 * math.exp(-zeta * math.pi / math.sqrt(1 - zeta ** 2))) < 1e-3)
ans[2] = 4 / (zeta * wn)
outside = np.where(np.abs(y - 1) > 0.02)[0]
v.assert_true("Q2: the exact 2% settling time is within 20% of the 4/(zeta wn) estimate",
              abs(t[outside[-1]] / ans[2] - 1) < 0.2, f"{t[outside[-1]]:.3f}")
_, y3 = signal.step(signal.TransferFunction([20], np.polyadd(np.polymul([1, 1], [1, 4]), [20])), T=np.linspace(0, 20, 20001))
ans[3] = 1 - y3[-1]
_, yr, _ = signal.lsim(signal.TransferFunction([50], [1, 5, 50]), U=np.linspace(0, 30, 30001), T=np.linspace(0, 30, 30001))
ans[4] = 30 - yr[-1]
den = lambda K: [1, 6, 11, K]  # noqa: E731
k_max = brentq(lambda K: max(np.roots(den(K)).real), 1, 200)
ans[5] = k_max
ans[6] = abs(np.roots(den(k_max)).imag).max()
L7 = lambda w: 10 / (1j * w * (1j * w + 1))  # noqa: E731
wc = brentq(lambda w: abs(L7(w)) - 1, 0.1, 100)
ans[7] = 180 + math.degrees(np.angle(L7(wc)))
_, y7 = signal.step(signal.TransferFunction([10], [1, 1, 10]), T=np.linspace(0, 30, 30001))
v.assert_true("Q7: the closed loop overshoots about 60%", abs(100 * (y7.max() - 1) - 60.5) < 0.5, f"{100 * (y7.max() - 1):.1f}")
v.assert_true("Q2 distractors: 4/wn = 0.4 s, peak time 0.343 s, 4/(zeta^2 wn) = 2.5 s",
              abs(4 / wn - 0.4) < 1e-12 and round(math.pi / (wn * math.sqrt(1 - zeta ** 2)), 3) == 0.343 and abs(4 / (zeta ** 2 * wn) - 2.5) < 1e-12)
L8 = lambda w: 10 / ((1j * w + 1) * (1j * w + 2) * (1j * w + 3))  # noqa: E731
w180 = brentq(lambda w: L8(w).imag, 1, 10)
ans[8] = -20 * math.log10(abs(L8(w180)))
ans[9] = math.degrees(math.asin(9 / 11))
phase10 = lambda w: math.atan(w / 2) - math.atan(w / 20)  # noqa: E731
ans[10] = minimize_scalar(lambda w: -phase10(w), bounds=(0.1, 100), method="bounded").x
v.assert_true("Q9: the lead's phase peak equals arcsin(9/11)", abs(math.degrees(phase10(ans[10])) - ans[9]) < 1e-4)
A = np.array([[0.0, 1.0], [-6.0, -5.0]]); B = np.array([0.0, 1.0]); C = np.array([1.0, 0.0])
ans[11] = float(C @ np.linalg.solve(A, -B))
facts[12] = sorted(np.linalg.eigvals(A).real)
sysd = signal.cont2discrete(([1], [1, 2]), 0.1, method="zoh")
ans[13] = float(np.roots(np.atleast_1d(np.squeeze(sysd[1])))[0])

# ================================================================= block 2 · DSP
fs = 10e3
n = np.arange(10000)
spec = np.abs(np.fft.rfft(np.cos(2 * np.pi * 7e3 * n / fs)))
ans[14] = np.argmax(spec) * fs / len(n) / 1e3
ans[15] = 44.1e3 / 1024


def butterflies(N):
    return 0 if N == 1 else 2 * butterflies(N // 2) + N // 2


ans[16] = butterflies(1024)
w_h = np.hanning(1024 + 1)[:-1]                      # periodic Hann
W = np.abs(np.fft.fft(w_h, 1024 * 64))
first_null = np.argmax(np.diff(W[: 64 * 4]) > 0)     # first minimum, in units of 1/64 bin
ans[17] = 2 * (first_null / 64) * 44.1e3 / 1024
h18 = signal.firwin(41, 0.25)
gd = signal.group_delay((h18, [1]), w=[0.1])[1][0]
ans[18] = gd / 8e3 * 1e3
fa = 2 * 8e3 * math.tan(math.pi * 1e3 / 8e3) / (2 * math.pi)
ans[19] = fa / 1e3
b_a, a_a = signal.butter(1, 2 * math.pi * fa, analog=True)
b_d, a_d = signal.bilinear(b_a, a_a, fs=8e3)
_, h_d = signal.freqz(b_d, a_d, worN=[2 * math.pi * 1e3 / 8e3])
v.assert_true("Q19: a prewarped analog cutoff lands the digital -3 dB point exactly at 1 kHz",
              abs(abs(h_d[0]) - 1 / math.sqrt(2)) < 1e-9)
facts[20] = np.abs(np.roots([1, -1.2, 0.5]))
ans[21] = 6.02 * 16 + 1.76
w23 = math.pi / 2
ans[23] = abs(sum(np.exp(-1j * w23 * k) for k in range(3))) / 3
q15 = lambda x: int(round(x * 32768))  # noqa: E731
ans[24] = (q15(0.75) * q15(-0.5)) >> 15
ans[22] = 48 / 4 / 2
_, yz = signal.dstep(([0.5], [1, -0.6], 1), n=200)
ans[25] = float(np.squeeze(yz)[-1])
x256 = np.cos(2 * np.pi * 0.1 * np.arange(256))
facts[26] = (len(np.fft.rfft(x256, 1024)) - 1) / (len(np.fft.rfft(x256)) - 1)

# ================================================================= block 3 · communications and networks
kT0 = 1.380649e-23 * 290
ans[27] = 10 * math.log10(kT0 * 1e6 / 1e-3)
# cascade by noise powers referred to the input: each stage adds (F - 1) k T0 B at its own input
g1, f1, f2 = 100.0, 10 ** 0.2, 10.0
n_out = kT0 * g1 * 1.0 + (f1 - 1) * kT0 * g1 + (f2 - 1) * kT0     # per hertz, after stage 2 (gain 1)
ans[28] = 10 * math.log10(n_out / (kT0 * g1))
ans[29] = 2 * (75 + 15)
ans[30] = (1 + 0.25) * 10 / 2
ebn0 = 10 ** 0.8
ans[31] = norm.sf(math.sqrt(2 * ebn0))
rng = np.random.default_rng(1705)
bits = rng.integers(0, 2, 4_000_000)
rx = (2 * bits - 1) + rng.normal(0, math.sqrt(1 / (2 * ebn0)), bits.size)
ber_mc = np.mean((rx > 0) != bits)
v.assert_true("Q31: Monte Carlo BPSK at 8 dB matches Q(sqrt(2 Eb/N0)) within 10%", abs(ber_mc / ans[31] - 1) < 0.1, f"{ber_mc:.3e}")
ans[32] = 1e6 * math.log2(1 + 15) / 1e6
lam = 2.998e8 / 2.4e9
ans[33] = -10 * math.log10((lam / (4 * math.pi * 100)) ** 2)    # Friis with unity-gain antennas
H = np.array([[1, 1, 0, 1, 1, 0, 0], [1, 0, 1, 1, 0, 1, 0], [0, 1, 1, 1, 0, 0, 1]])
syn = {tuple(H[:, i]) for i in range(7)}
two_bit = {tuple((H[:, i] + H[:, j]) % 2) for i, j in itertools.combinations(range(7), 2)}
facts[34] = (len(syn) == 7 and (0, 0, 0) not in syn, two_bit <= syn)
ans[35] = 20e6 / 64 / 1e3
ans[36] = 65536 * 8 / 0.05 / 1e6
ans[37] = ipaddress.ip_network("192.168.10.64/26").num_addresses - 2
G = np.linspace(0.01, 3, 30000)
ans[38] = float(np.max(G * np.exp(-G)))
ans[39] = 100 * 1500 / (8 + 14 + 1500 + 4 + 12)

# ================================================================= block 4 · embedded systems and software
ans[40] = ma.wait_states(100e6, 25e-9)
ans[41] = 9600 / 10
tau42 = 2200 * 100e-12
ans[42] = (brentq(lambda tt: 1 - math.exp(-tt / tau42) - 0.7, 0, 1e-5) - brentq(lambda tt: 1 - math.exp(-tt / tau42) - 0.3, 0, 1e-5)) * 1e9
ans[43] = 3.3 / 4096 * 1e3
ans[44] = rs.ll_bound(2)
tasks = rs.rm_priorities([rs.Task("A", 5, [(2, None)]), rs.Task("B", 10, [(2, None)]), rs.Task("C", 20, [(3, None)])])
res = rs.simulate(tasks, 200, policy="fp")
ans[45] = res.worst("C")
v.assert_true("Q45: simulation and recurrence agree", rs.response_time(tasks, [t_.name for t_ in tasks].index("C")) == ans[45])
ans[46] = 230e-3 / 20e-6 / 24
ans[47] = dm.pingpong_min_block(100e3, 50e-6, 2e-6, 30e-6)
v.assert_true("Q47: 10-sample blocks never overrun at the worst latency; 9 do",
              dm.simulate_pingpong(100e3, 10, 50e-6, 2e-6, n_blocks=2000, service_latency=30e-6)[0] == 0
              and dm.simulate_pingpong(100e3, 9, 50e-6, 2e-6, n_blocks=2000, service_latency=30e-6)[0] > 0)


def bsearch_worst(nitems):
    """Comparisons a binary search makes when it always continues into the larger half (the worst case)."""
    lo, hi, c = 0, nitems - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        c += 1
        if mid - lo > hi - mid:
            hi = mid - 1
        else:
            lo = mid + 1
    return c


ans[48] = bsearch_worst(1_000_000)
v.assert_true("Q48: 20 comparisons = ceil(log2(N + 1))", ans[48] == math.ceil(math.log2(1_000_001)))
ans[49] = (10 ** 4 + 1) / 2 * 3 / 3600
ans[50] = int.from_bytes(bytes.fromhex("FF38"), "big", signed=True)

for qn, value in sorted(ans.items()):
    v.check(f"T5.{qn:02d}", value)

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


non_numeric = {12, 20, 26, 34}
numeric_mc = [q for q in range(2, 51, 2) if q not in non_numeric]
for qn in numeric_mc:
    target = ans[qn]
    scored = sorted((abs(p[0] - target), letter, p[1]) for letter, text in options[qn].items()
                    if (p := option_value(text)) is not None)
    (best_err, best_l, tol), second_err = scored[0], scored[1][0]
    v.assert_true(f"Q{qn}: answer letter {letters.get(qn)} is the option closest to the computed value, within its precision",
                  best_l == letters.get(qn) and best_err <= tol * (1 + 1e-9) and second_err > best_err,
                  f"closest {best_l} (error {best_err:.3g}), options {options[qn]}")
# non-numerical options: the keyed option must state the computed facts
v.assert_true("Q12: eigenvalues are -3 and -2, option (A)", np.allclose(facts[12], [-3, -2]) and letters.get(12) == "A"
              and "−2 and −3" in options[12]["A"])
v.assert_true("Q20: both poles inside the unit circle at radius 0.707, option (A)",
              np.allclose(facts[20], math.sqrt(0.5)) and letters.get(20) == "A" and "0.707" in options[20]["A"])
v.assert_true("Q26: zero padding 256 -> 1024 gives four times as many bins, option (B)",
              facts[26] == 4.0 and letters.get(26) == "B" and "bin spacing" in options[26]["B"])
v.assert_true("Q34: single errors have distinct nonzero syndromes and double errors alias them, option (C)",
              facts[34] == (True, True) and letters.get(34) == "C")
v.assert_true("every multiple-choice question has an answer letter", set(options) <= set(letters))
v.assert_true("50 questions, numbered 1 to 50",
              sorted(int(n_) for n_ in re.findall(r"^\*\*(\d+)\.\*\*", readme, re.M)) == list(range(1, 51)))
v.assert_true("even-numbered questions are multiple choice, odd ones numeric entry",
              set(options) == set(range(2, 51, 2)))

sys.exit(v.finish())
