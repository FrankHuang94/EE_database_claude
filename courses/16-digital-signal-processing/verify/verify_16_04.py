#!/usr/bin/env python3
"""Verify chapter 16-04 (the FFT algorithm): examples, concept checks, problems and lab answers.

Routes:
- the lab's recursive, in-place DIT and DIF FFTs against numpy.fft for many sizes;
- operation counts by instrumenting the in-place FFT, against the closed forms of sections 3.2 and 3.5;
- bit-reversed orders by enumeration;
- the Q1.15 butterfly arithmetic of Example 16-04.5 with Python integers, and the fixed-point 8-point FFT model
  against the exact DFT/8; the committed Verilog test vectors are regenerated and compared;
- hardware counts (R2SDF delays, twiddle triviality per stage) by enumerating the stages.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "16-04-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import fft  # noqa: E402

CH = ROOT / "chapters" / "16-04-the-fft.md"
v = Verifier.from_files("16-04", CH, ROOT / "solutions" / "16-04-solutions.md", LAB / "README.md")
rng = np.random.default_rng(164)

for N in (2, 4, 8, 16, 32, 256, 1024, 4096):
    x = rng.normal(size=N) + 1j * rng.normal(size=N)
    ref = np.fft.fft(x)
    v.assert_true(f"in-place DIT matches numpy for N = {N}", np.allclose(fft.fft_dit(x), ref))
    v.assert_true(f"DIF matches numpy for N = {N}", np.allclose(fft.fft_dif(x), ref))
    if N <= 1024:
        v.assert_true(f"recursive matches numpy for N = {N}", np.allclose(fft.fft_recursive(x), ref))
    v.assert_true(f"inverse via forward for N = {N}", np.allclose(fft.ifft_via_fft(ref), x))
    b, c, nt = fft.twiddle_counts(N)
    m = int(math.log2(N))
    v.assert_true(f"butterflies = (N/2) log2 N for N = {N}", b == N // 2 * m and c == b)
    if N >= 4:
        v.assert_true(f"non-trivial = (N/2) log2 N - 3N/2 + 2 for N = {N}", nt == N // 2 * m - 3 * N // 2 + 2)

# ---------------------------------------------------------------------------------------- Example 1
for N, keys in ((256, ("a", "g", "h")), (1024, ("b", "e", "f")), (4096, ("c", "i", "j"))):
    direct, ffts = N * N, fft.twiddle_counts(N)[1]
    v.check(f"Ex 16-04.1{keys[0]}", direct / ffts)
    v.check(f"Ex 16-04.1{keys[1]}", direct)
    v.check(f"Ex 16-04.1{keys[2]}", ffts)
v.check("Ex 16-04.1d", fft.twiddle_counts(1024)[2])
v.assert_true("Ex 1: N = 2 needs no non-trivial multiplication", fft.twiddle_counts(2)[2] == 0)

# ---------------------------------------------------------------------------------------- Example 2
X2 = fft.fft_dit([1, 2, 3, 4])
v.check("Ex 16-04.2a", X2[0].real)
v.check("Ex 16-04.2b", X2[2].real)
v.assert_true("Ex 2: equals the DFT of 16-03.1", np.allclose(X2, [10, -2 + 2j, -2, -2 - 2j]))
c4 = {}
fft.fft_dit(np.zeros(4), count=c4)
v.assert_true("Ex 2: 4 butterflies, no non-trivial multiplication", c4["butterflies"] == 4 and c4.get("cmul_nontrivial", 0) == 0)

# ---------------------------------------------------------------------------------------- Example 3
v.assert_true("Ex 3: 16-point bit-reversed order",
              [fft.bit_reverse(i, 4) for i in range(16)] == [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15])


def nontrivial_per_stage(N):
    out = []
    size = 2
    while size <= N:
        cnt = 0
        for _start in range(0, N, size):
            for j in range(size // 2):
                k = j * (N // size)
                if not fft._is_trivial(k, N):
                    cnt += 1
        out.append(cnt)
        size *= 2
    return out


st16 = nontrivial_per_stage(16)
v.assert_true("Ex 3: stages 1 and 2 have no non-trivial twiddles", st16[:2] == [0, 0])
v.check("Ex 16-04.3a", st16[2])
v.check("Ex 16-04.3b", st16[3])
v.check("Ex 16-04.3c", sum(st16))

# ---------------------------------------------------------------------------------------- Example 4
period = 1024 / 100e6
v.check("Ex 16-04.4a", period * 1e6)
rate = fft.twiddle_counts(1024)[0] / period
v.check("Ex 16-04.4b", rate / 1e6)
v.check("Ex 16-04.4c", math.ceil(rate / 500e6 * 1.0000001))   # exactly 1.0 at 500 MHz: no margin, so 2 units
v.check("Ex 16-04.4d", 2 * 1024)
v.check("Ex 16-04.4e", int(math.log2(1024)))
# general multipliers between R2SDF stages: stages whose twiddle set contains a non-trivial value (DIF: stage of size s
# uses W_s^j); the last two stages (sizes 4 and 2) use only 1 and -j
sizes = [1024 >> i for i in range(10)]
general = sum(1 for s in sizes if any(not fft._is_trivial(j * (1024 // s), 1024) for j in range(s // 2)))
v.check("Ex 16-04.4f", general)
v.check("Ex 16-04.4g", sum(1024 >> i for i in range(1, 11)))
v.check("Ex 16-04.4h", 500 / 100)

# ---------------------------------------------------------------------------------------- Example 5
wr, wi = fft.TW8[1]
br, bi = 32767, 32767
pr_raw = br * wr - bi * wi
v.check("Ex 16-04.5e", pr_raw)
tr, ti = fft._cmul_q15(br, bi, wr, wi)
v.assert_true("Ex 5: the rotated b is real", ti == 0)
v.check("Ex 16-04.5a", tr)
v.check("Ex 16-04.5b", (32767 + tr) >> 1)
v.check("Ex 16-04.5c", (32767 - tr) >> 1)
v.assert_true("Ex 5: the model saturates the sum to 32767", fft._bfly(32767, 0, br, bi, 1)[0] == 32767)
v.check("Ex 16-04.5d", 1 + math.sqrt(2))
v.check("Ex 16-04.5f", 32767 * math.sqrt(2))

# ---------------------------------------------------------------------------------------- text and concept checks
v.check("Txt 16-04.a", 8 * 8)
v.check("Txt 16-04.b", fft.twiddle_counts(8)[0])
cr = (1024 // 4) * math.log2(512) + 512
v.check("Txt 16-04.c", 100 * cr / 5120)
v.check("Txt 16-04.d", 100 * (3 * 1024 / 8 * 10) / 5120)
v.check("Txt 16-04.e", int(math.log2(32)))
v.check("Txt 16-04.f", fft.twiddle_counts(32)[0])
v.check("Txt 16-04.g", fft.bit_reverse(3, 5))
v.check("Txt 16-04.h", 12 + int(math.log2(4096)))
a_, b_ = rng.normal(size=64), rng.normal(size=64)
A_, B_ = fft.two_real_ffts(a_, b_)
v.assert_true("3.6: two real FFTs from one complex FFT", np.allclose(A_, np.fft.fft(a_)) and np.allclose(B_, np.fft.fft(b_)))

# ---------------------------------------------------------------------------------------- Problems
b256, c256, nt256 = fft.twiddle_counts(256)
v.check("16-04.1a", int(math.log2(256)))
v.check("16-04.1b", b256)
v.check("16-04.1c", nt256)
v.check("16-04.1d", 256 * 256 / c256)
v.check("16-04.2a", fft.bit_reverse(3, 4))
v.check("16-04.2b", fft.bit_reverse(6, 4))
v.check("16-04.2c", fft.bit_reverse(11, 4))
v.check("16-04.2d", sum(1 for i in range(16) if fft.bit_reverse(i, 4) == i))
v.check("16-04.3a", 2 ** (6 - 1))
X4 = fft.fft_dit([0, 1, 0, -1])
v.check("16-04.4a", X4[1])
v.check("16-04.4b", X4[3])
X5 = np.fft.fft([1, 1, 1, 1, 0, 0, 0, 0])
W8 = np.exp(-2j * np.pi / 8)
odd = np.fft.fft(np.array([1, 1, 1, 1]) * W8 ** np.arange(4))
even = np.fft.fft(np.array([1, 1, 1, 1]))
v.assert_true("P5: DIF halves reproduce the 8-point DFT", np.allclose(even, X5[0::2]) and np.allclose(odd, X5[1::2]))
v.check("16-04.5a", X5[0].real)
v.check("16-04.5b", abs(X5[2]))
v.check("16-04.5c", X5[1])
v.check("16-04.5d", X5[3])
v.check("16-04.6a", 4 * nt256)
v.check("16-04.6b", 3 * nt256)
v.check("16-04.7a", 3 * 1024 // 8 * 10)
v.check("16-04.7b", 3 * 4096 // 8 * 12)
v.check("16-04.7c", 100 * (3 / 8) / (1 / 2))
v.check("16-04.8a", cr)
v.check("16-04.8b", 100 * cr / 5120)
v.assert_true("P9: inverse via forward", np.allclose(fft.ifft_via_fft([10, -2 + 2j, -2, -2 - 2j]), [1, 2, 3, 4]))
bf4096 = fft.twiddle_counts(4096)[0]
v.check("16-04.10a", bf4096)
t10 = 4096 / 250e6
v.check("16-04.10b", t10 * 1e6)
v.check("16-04.10c", bf4096 / (t10 * 1e9))
v.check("16-04.10d", math.ceil(bf4096 / (t10 * 1e9)))
v.check("16-04.11a", 10)
v.check("16-04.11b", general)
v.check("16-04.11c", sum(1024 >> i for i in range(1, 11)))
v.check("16-04.11d", sum(1024 >> i for i in range(1, 11)) * 32 / 8)
v.check("16-04.11e", 50)
# a DC full-scale input attains the bound N * max|x|
v.check("16-04.12a", 12 + int(round(math.log2(abs(np.fft.fft(np.full(4096, -2048.0))[0]) / 2048))))
n12 = np.arange(4096)
Xs = np.abs(np.fft.fft(2047 * np.cos(2 * np.pi * 100 * n12 / 4096))) / 4096
v.check("16-04.12b", Xs[100])
v.check("16-04.12c", math.ceil(math.log2(Xs[100])) + 1)   # magnitude bits plus the sign bit

# ---------------------------------------------------------------------------------------- Lab: fixed-point FFT and vectors
errs = []
rng_lab = np.random.default_rng(1640)
for _ in range(2000):
    xr = list(map(int, rng_lab.integers(-16000, 16001, 8)))
    xi = list(map(int, rng_lab.integers(-16000, 16001, 8)))
    Xr, Xi = fft.fft8_fixed(xr, xi)
    errs.append(np.max(np.abs(np.array(Xr) + 1j * np.array(Xi) - np.fft.fft(np.array(xr) + 1j * np.array(xi)) / 8)))
v.check("Lab 16-04.a", float(np.max(errs)))
v.assert_true("Lab: fixed-point error below 3 LSB for half-scale inputs", np.max(errs) < 3)
# rebuild the Verilog test vectors in memory and compare with the committed file, word for word
sys.path.insert(0, str(LAB))
import make_vectors  # noqa: E402

committed = (LAB / "vectors.hex").read_text().split()
v.assert_true("Lab: committed vectors.hex equals a fresh build from the bit-exact model", committed == make_vectors.build())
v.check("Lab 16-04.b", len(committed) // 32)


def s16(h):
    x = int(h, 16)
    return x - 65536 if x >= 32768 else x


sat_cases = 0
for t in range(len(committed) // 32):
    w = [s16(h) for h in committed[32 * t:32 * t + 32]]
    before = fft.SAT_EVENTS[0]
    fft.fft8_fixed(w[:8], w[8:16])
    sat_cases += fft.SAT_EVENTS[0] > before
v.assert_true("Lab: the saturating vector's output differs from DFT/8 by far more than rounding",
              any(np.max(np.abs(np.array([s16(h) for h in committed[32 * t + 16:32 * t + 24]])
                                + 1j * np.array([s16(h) for h in committed[32 * t + 24:32 * t + 32]])
                                - np.fft.fft(np.array([s16(h) for h in committed[32 * t:32 * t + 8]])
                                             + 1j * np.array([s16(h) for h in committed[32 * t + 8:32 * t + 16]])) / 8)) > 100
                  for t in range(len(committed) // 32)))
v.check("Lab 16-04.c", sat_cases)

sys.exit(v.finish())
