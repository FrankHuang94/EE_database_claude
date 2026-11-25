#!/usr/bin/env python3
"""Verify every number in chapter 24-04 (DSP-based SerDes and FEC), its problems and its lab.

Independent routes (the lab module dsp.py uses closed forms, scipy's binomial and its own search):
- quantization noise measured on a dense ramp through an explicit quantizer, not Delta/sqrt(12);
- jitter-limited SNR from the exact expectation 1 - exp(-(w sigma)^2/2), not the small-angle formula;
- MLSD distances by an independent exhaustive search over error events;
- burst lengths by sliding every burst over every alignment and counting symbols per codeword;
- RS failure probability by an exact sum with math.comb;
- inverse Q by root-finding on the log tail.
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "24-04-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("24-04", ROOT / "chapters" / "24-04-dsp-serdes-and-fec.md",
                        ROOT / "solutions" / "24-04-solutions.md", LAB / "README.md")


def Qi(p):
    return optimize.brentq(lambda x: stats.norm.logsf(x) - math.log(p), 0, 40, xtol=1e-14)


PAM4_RMS = math.sqrt((1 + 1 / 9) / 2)


def quant_noise(bits, fs):
    """rms error of a mid-rise quantizer over a dense ramp spanning the full scale."""
    step = fs / 2 ** bits
    x = np.linspace(-fs / 2 + 1e-9, fs / 2 - 1e-9, 2_000_001)
    xq = (np.floor(x / step) + 0.5) * step
    return float(np.sqrt(np.mean((x - xq) ** 2))), step


def jitter_snr(f, sigma):
    w = 2 * math.pi * f
    return 10 * math.log10(0.5 / (1 - math.exp(-(w * sigma) ** 2 / 2)))


def sigma_for_snr(f, snr_db):
    return optimize.brentq(lambda s: jitter_snr(f, s) - snr_db, 1e-16, 1e-11, xtol=1e-22)


# ================================================================ chapter
for bits, keys in ((6, ("1a1", "1a2", "1a3")), (5, ("1a4", "1a5", "1a6")), (7, ("1a7", "1a8", "1a9"))):
    sq, step = quant_noise(bits, 3.0)
    if bits == 6:
        v.check("Ex 24-04.1a", step)
        v.check("Txt 24-04.g", 20 * math.log10(PAM4_RMS / sq))
    v.check(f"Ex 24-04.{keys[0]}", sq)
    v.check(f"Ex 24-04.{keys[1]}", (1 / 3) / sq)
    v.check(f"Ex 24-04.{keys[2]}", 20 * math.log10(PAM4_RMS / sq))
v.check("Txt 24-04.a", PAM4_RMS)
s7, _ = quant_noise(7, 3.0)
s6, _ = quant_noise(6, 3.0)
v.check("Txt 24-04.f", 20 * math.log10(s6 / s7))
j100 = jitter_snr(26.5625e9, 100e-15)
j50 = jitter_snr(26.5625e9, 50e-15)
v.check("Ex 24-04.1b", j100)
v.check("Ex 24-04.1b1", (j100 - 1.76) / 6.02)
v.check("Ex 24-04.1b2", j50)
v.check("Ex 24-04.1b3", (j50 - 1.76) / 6.02)
pam4_off = -20 * math.log10(PAM4_RMS * math.sqrt(12) / 3.0)  # SQNR = 6.02N - offset for a +-1.5 full scale
v.check("Txt 24-04.i", pam4_off)
v.check("Ex 24-04.1b4", (j100 + pam4_off) / (20 * math.log10(2)))
v.check("Ex 24-04.1b5", (j50 + pam4_off) / (20 * math.log10(2)))
v.check("Ex 24-04.1c", sigma_for_snr(53.125e9, j100) * 1e15)

v.check("Ex 24-04.2a", 106.25 / 64)
sk1 = sigma_for_snr(26.5625e9, 35.0) * 1e15
v.check("Ex 24-04.2b", sk1)
v.check("Ex 24-04.2c", sigma_for_snr(53.125e9, 35.0) * 1e15)
v.check("Ex 24-04.2d", 1e12 / (106.25e9 / 64))
v.check("Ex 24-04.2d1", 100 * sigma_for_snr(53.125e9, 35.0) * (106.25e9 / 64))

mac = 24 * 106.25e9
v.check("Ex 24-04.3a", mac)
v.check("Ex 24-04.3b", 106.25 / 128)
v.check("Ex 24-04.3b1", 24 * 128)
v.check("Ex 24-04.3c", mac * 20e-15 * 1e3)
v.check("Ex 24-04.3c1", mac * 20e-15 / 212.5e9 * 1e12)


def dmin2(h, max_len=7):
    """Independent exhaustive search: smallest squared distance over NRZ error events."""
    h = list(h)
    best = math.inf
    for n in range(1, max_len + 1):
        for e in itertools.product((-2, 0, 2), repeat=n):
            if e[0] == 0 or e[-1] == 0:
                continue
            out = [sum(e[i] * h[k - i] for i in range(n) if 0 <= k - i < len(h)) for k in range(n + len(h) - 1)]
            best = min(best, sum(x * x for x in out))
    return best


v.check("Ex 24-04.4a", (2 * 1.0) ** 2)
d05, d1 = dmin2([1, 0.5]), dmin2([1, 1])
v.check("Ex 24-04.4b", d05)
v.check("Ex 24-04.4b1", d1)
v.check("Ex 24-04.4c", sum(x * x for x in np.convolve([2, -2], [1, 1])))
v.check("Ex 24-04.4d", 10 * math.log10(d05 / 4))
v.check("Ex 24-04.4d1", 10 * math.log10(d1 / 4))
v.check("Ex 24-04.4e", 4 ** 2)
v.check("Ex 24-04.4e1", 4 ** 3)
v.check("Txt 24-04.c", 4 ** 1)
v.check("Txt 24-04.d", 4 ** 2)

cw = 544 * 10
v.check("Txt 24-04.b", cw)
v.check("Ex 24-04.5a", cw / 106.25e9 * 1e9)
v.check("Ex 24-04.5a1", cw / 212.5e9 * 1e9)
v.check("Ex 24-04.5b", cw / 106.25e9 * 1e9 + 100)
flit16 = 256 * 8 / (16 * 64e9) * 1e9
v.check("Ex 24-04.5c", flit16)
v.check("Ex 24-04.5c1", 256 * 8 / 64e9 * 1e9)
v.check("Ex 24-04.5d", (cw / 106.25e9 * 1e9 + 100) / flit16)

r_inner = 106.25 * 128 / 120
v.check("Ex 24-04.6a", r_inner)
r_pad = r_inner * (3264 * 128 + 384) / (3264 * 128)
v.check("Ex 24-04.6b", r_pad)
v.check("Ex 24-04.6c", 156.25 * 726)
v.assert_true("padded rate equals 156.25 MHz x 726", abs(r_pad * 1e3 - 156.25 * 726) < 1e-9)
v.check("Ex 24-04.6d", 100 * (128 / 120 - 1))
v.check("Ex 24-04.6d1", 100 * (128 / 120 - 1))

R1, R2 = 514 / 544, 514 / 544 * 120 / 128
qa, qb, q13, q15 = Qi(2.2e-4), Qi(4.85e-3), Qi(1e-13), Qi(1e-15)
v.check("Ex 24-04.7a0", qa)
v.check("Ex 24-04.7a00", qb)
v.check("Ex 24-04.7a02", q15)
v.check("Ex 24-04.7a03", R1)
v.check("Ex 24-04.7a04", R2)


def ncg(qin, qout, r):
    # required Eb/N0 ratio uncoded/coded in BPSK: (qout^2/2) / (qin^2/(2 r))
    return 10 * math.log10((qout ** 2 / 2) / (qin ** 2 / (2 * r)))


kp13, kp15 = ncg(qa, q13, R1), ncg(qa, q15, R1)
cc13, cc15 = ncg(qb, q13, R2), ncg(qb, q15, R2)
v.check("Txt 24-04.h", kp15)
v.check("Ex 24-04.7a1", kp15)
v.check("Ex 24-04.7b1", cc15)
v.check("Ex 24-04.7c", cc13 - kp13)
v.assert_true("inner-code gain independent of output BER", abs((cc13 - kp13) - (cc15 - kp15)) < 1e-12)

v.check("Ex 24-04.8a", 5e-6 * 100e-9 * 1e12)
v.check("Ex 24-04.8b", 100 * 5e-6 * 100)
v.check("Ex 24-04.8c", 150e-9 / (5e-6 * 100e-9))

# ================================================================ solutions
sq7, st7 = quant_noise(7, 2.5)
v.check("24-04.1a", st7)
v.check("24-04.1b", sq7)
sqnr7 = 20 * math.log10(PAM4_RMS / sq7)
v.check("24-04.1c", sqnr7)
v.check("24-04.1d", (1 / 3) / sq7)
v.check("24-04.1e", sqnr7 - 20 * math.log10(PAM4_RMS / s6))
v.check("24-04.1e1", 100 * (1 - 1.25 / 1.5))

v.check("24-04.2a", sigma_for_snr(53.125e9, 30.0) * 1e15)
v.check("24-04.2b", sigma_for_snr(26.5625e9, 38.0) * 1e15)


def comb(*snr):
    return -10 * math.log10(sum(10 ** (-x / 10) for x in snr))


v.check("24-04.3a", comb(30, 34.8, 35.6))
v.check("24-04.3b", comb(34.8, 35.6))
v.check("24-04.3b1", comb(30, 35.6))
v.check("24-04.3b2", comb(30, 34.8))

v.check("24-04.4a", 106.25 / 128)
v.check("24-04.4b", 106.25 / 128)
v.check("24-04.4c", sigma_for_snr(26.5625e9, 32.0) * 1e15)

ffe = 40 * 106.25e9 * 30e-15
mlsd = 16 * 106.25e9 * 10e-15
v.check("24-04.5a", ffe * 1e3)
v.check("24-04.5b", mlsd * 1e3)
v.check("24-04.5c", (ffe + mlsd) / 212.5e9 * 1e12)
v.check("24-04.5c1", ffe / 212.5e9 * 1e12)
v.check("24-04.5c2", mlsd / 212.5e9 * 1e12)

d6a = dmin2([1, 0.75])
d6b = dmin2([1, 0.5, 0.25])
v.assert_true("P6 single errors are closest", abs(d6a - 4 * (1 + 0.75 ** 2)) < 1e-12 and abs(d6b - 5.25) < 1e-12)
v.check("24-04.6a", d6a)
v.check("24-04.6a1", 10 * math.log10(d6a / 4))
v.check("24-04.6b", d6b)
v.check("24-04.6b1", sum(x * x for x in np.convolve([2, -2], [1, 0.5, 0.25])))
v.check("24-04.6b2", 10 * math.log10(d6b / 4))

v.check("24-04.7a", 4 ** 3)
v.check("24-04.7a1", 4 ** 4)
v.check("24-04.7b", 2 ** 3)
v.check("24-04.7b1", 2 ** 4)
v.check("24-04.7c", 16 * 106.25e9)

acc = 4 * cw / 212.5e9 * 1e9
v.check("24-04.8a", acc)
v.check("24-04.8b", acc + 100)
v.check("24-04.8c", acc + 100 + 56)

q3 = Qi(1e-3)
n9 = ncg(q3, q15, 0.9)
v.check("24-04.9a0", q3)
v.check("24-04.9a", n9)
v.check("24-04.9b", n9 - kp15)

rate10 = 200 * 257 / 256 * 544 / 514
v.check("24-04.10a", rate10)
v.check("24-04.10a1", rate10 / 2)
v.check("24-04.10b", 100 * (2 * r_pad / 200 - 1))
v.check("24-04.10c", 100 * (rate10 / 200 - 1))

flits = 16 * 64e9 / 2048
v.check("24-04.11a", flits)
v.check("24-04.11b", flits * 5e-6)
v.check("24-04.11c", 1 - (1 - 1e-6) ** 2048)


def longest_burst(interleave, t=15, m=10):
    """Largest b such that every b-bit burst, at every alignment, leaves each codeword with <= t bad symbols."""
    def ok(b):
        for start in range(m):
            first, last = start // m, (start + b - 1) // m
            syms = range(first, last + 1)
            counts = {}
            for s in syms:
                counts[s % interleave] = counts.get(s % interleave, 0) + 1
            if max(counts.values()) > t:
                return False
        return True
    b = 1
    while ok(b + 1):
        b += 1
    return b


v.check("24-04.12a", longest_burst(1))
v.check("24-04.12b", longest_burst(4))
v.check("24-04.12b1", 4 * 15)

v.check("24-04.13a", 4 * 151)
v.check("24-04.13b", 4 * flit16)

# ================================================================ lab
la, _ = quant_noise(6, 3.6)
lb, _ = quant_noise(4, 3.6)
v.check("Lab 24-04.a", 20 * math.log10(PAM4_RMS / la))
v.check("Lab 24-04.b", 20 * math.log10(PAM4_RMS / lb))
v.check("Lab 24-04.c", d05)
v.check("Lab 24-04.d", d1)
v.check("Lab 24-04.e", dmin2([1, 1.25]))
v.check("Lab 24-04.f", 10 * math.log10(d1 / 4))
v.check("Lab 24-04.g", 1 / Qi(1e-3))
ps = 1 - (1 - 2.4e-4) ** 10
ucr = sum(math.comb(544, i) * ps ** i * (1 - ps) ** (544 - i) for i in range(16, 545))
v.check("Lab 24-04.h", ucr)
v.check("Lab 24-04.i", 16 / 5440 * ucr)
v.check("Lab 24-04.j", r_pad)
v.check("Lab 24-04.k", cw / 212.5e9 * 1e9)

# ---------------------------------------------------------------- Problems 24-04.14 to 24-04.16
import itertools  # noqa: E402
from scipy import stats as _st  # noqa: E402
# 14: expectations by enumerating the three symbols involved, noise added analytically
combos = list(itertools.product([-1, 1], repeat=3))  # (a_n, a_{n-1}, a_{n-2})
Exx = np.zeros((2, 2))
Exa = np.zeros(2)
for an, a1, a2 in combos:
    xv = np.array([an + 0.5 * a1, a1 + 0.5 * a2])
    Exx += np.outer(xv, xv) / len(combos)
    Exa += xv * an / len(combos)
Exx += 0.01 * np.eye(2)
v.check("24-04.14a0", Exx[0, 0])
v.check("24-04.14a1", Exx[0, 1])
v.check("24-04.14a2", np.linalg.det(Exx))
cm = np.linalg.solve(Exx, Exa)
v.check("24-04.14a", cm[0])
v.check("24-04.14a3", cm[1])
mse = lambda c_: c_ @ Exx @ c_ - 2 * c_ @ Exa + 1.0  # noqa: E731
v.check("24-04.14b", mse(cm))
v.check("24-04.14c0", float(np.convolve([1, -0.5], [1, 0.5])[2] ** 2))
v.check("24-04.14c", mse(np.array([1.0, -0.5])))
# 15: brute force over all 16 sequences, and the running two-state metrics
y15 = [1.6, 0.4, -1.3, -0.7]
best = min(itertools.product([-1, 1], repeat=4),
           key=lambda seq: sum((y15[n] - seq[n] - 0.5 * (seq[n - 1] if n else 1)) ** 2 for n in range(4)))
v.assert_true("Viterbi sequence is (+1, -1, -1, -1)", tuple(best) == (1, -1, -1, -1))
cost = lambda seq: sum((y15[n] - seq[n] - 0.5 * (seq[n - 1] if n else 1)) ** 2 for n in range(len(seq)))  # noqa: E731
v.check("24-04.15b", cost(best))
pm_ = {}
for n in range(4):
    for s_ in (1, -1):
        pm_[(n, s_)] = min(cost(seq) for seq in itertools.product([-1, 1], repeat=n + 1) if seq[-1] == s_)
keys15 = [("24-04.15a", (0, 1)), ("24-04.15a1", (0, -1)), ("24-04.15a2", (1, 1)), ("24-04.15a3", (1, -1)),
          ("24-04.15a4", (2, 1)), ("24-04.15a5", (2, -1)), ("24-04.15a6", (3, 1))]
for kk, idx in keys15:
    v.check(kk, pm_[idx])
# 16: binomial tail summed directly in logs
ps16 = 1 - (1 - 2.4e-4) ** 10
v.check("24-04.16a", ps16)
v.check("24-04.16b", 544 * ps16)
logterms = [math.lgamma(545) - math.lgamma(k + 1) - math.lgamma(545 - k) + k * math.log(ps16)
            + (544 - k) * math.log1p(-ps16) for k in range(16, 545)]
v.check("24-04.16c", sum(math.exp(t) for t in logterms))
v.assert_true("binomial tail matches scipy", abs(sum(math.exp(t) for t in logterms) / _st.binom.sf(15, 544, ps16) - 1) < 1e-6)

sys.exit(v.finish())
