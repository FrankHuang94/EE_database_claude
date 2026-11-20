#!/usr/bin/env python3
"""Verify chapter 16-03 (the DFT and its properties): examples, concept checks, problems and lab answers.

Routes:
- DFTs from the definition (labs/16-03-lab/dft.py, an explicit matrix) against numpy.fft;
- the DFT-samples-the-DTFT identity checked against a direct DTFT sum;
- circular convolution computed directly from its definition and by DFT products;
- overlap-add and overlap-save against numpy.convolve on random data;
- time aliasing by inverse-transforming samples of the closed-form DTFT;
- the FFT-convolution cost model searched exhaustively over powers of 2;
- the cyclic prefix by simulating an OFDM link (QPSK on 64 subcarriers) through a multipath channel.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(ROOT / "labs" / "16-03-lab"))
from eeverify import Verifier  # noqa: E402
import dft  # noqa: E402

CH = ROOT / "chapters" / "16-03-the-dft.md"
v = Verifier.from_files("16-03", CH, ROOT / "solutions" / "16-03-solutions.md", ROOT / "labs" / "16-03-lab" / "README.md")
rng = np.random.default_rng(163)

# helper self-tests
for N in (4, 8, 13):
    F = dft.dft_matrix(N)
    v.assert_true(f"orthogonality: F^H F = N I for N = {N}", np.allclose(F.conj().T @ F, N * np.eye(N)))
    x = rng.normal(size=N) + 1j * rng.normal(size=N)
    v.assert_true(f"dft matches numpy.fft for N = {N}", np.allclose(dft.dft(x), np.fft.fft(x)))
    v.assert_true(f"idft inverts dft for N = {N}", np.allclose(dft.idft(dft.dft(x)), x))
    v.assert_true(f"DFT samples the DTFT for N = {N}", np.allclose(dft.dft(x), dft.dtft(x, 2 * np.pi * np.arange(N) / N)))
    v.assert_true(f"Parseval for N = {N}", abs(np.sum(abs(x) ** 2) - np.sum(abs(dft.dft(x)) ** 2) / N) < 1e-9)
    h = rng.normal(size=N)
    v.assert_true(f"circular convolution theorem for N = {N}",
                  np.allclose(dft.circ_conv(x, h, N), dft.idft(dft.dft(x) * dft.dft(h))))

# ---------------------------------------------------------------------------------------- Example 1
X1 = dft.dft([1, 2, 3, 4])
v.check("Ex 16-03.1a", X1[0].real)
v.check("Ex 16-03.1b", X1[1])
v.check("Ex 16-03.1c", X1[2].real)
v.check("Ex 16-03.1d", X1[3])
v.check("Ex 16-03.1e", float(np.sum(np.abs(X1) ** 2) / 4))
v.assert_true("Ex 1: conjugate symmetry X[3] = X*[1]", abs(X1[3] - np.conj(X1[1])) < 1e-12)

# ---------------------------------------------------------------------------------------- Example 2
fs, N = 48_000.0, 1024
n = np.arange(N)
v.check("Ex 16-03.2a", fs / N)
X3k = np.fft.fft(np.cos(2 * math.pi * 3000 * n / fs))
k3 = int(np.argmax(np.abs(X3k[:N // 2])))
v.check("Ex 16-03.2b", k3)
v.check("Ex 16-03.2c", abs(X3k[k3]))
v.assert_true("Ex 2: on-bin tone leaves every other bin at zero", np.max(np.abs(np.delete(X3k, [k3, N - k3]))) < 1e-9)
v.check("Ex 16-03.2d", 1000 / (fs / N))
X1k = np.fft.fft(np.cos(2 * math.pi * 1000 * n / fs))
big = float(np.max(np.abs(X1k[:N // 2])))
v.check("Ex 16-03.2h", big)
v.check("Ex 16-03.2e", big / (N / 2))
v.check("Ex 16-03.2f", 20 * math.log10(big / (N / 2)))
v.check("Ex 16-03.2g", abs(X1k[22]) / (N / 2))
v.check("Ex 16-03.2i", N / fs * 1e3)
v.assert_true("Ex 2: Parseval for the on-bin tone", abs(np.sum(np.cos(2 * math.pi * 3000 * n / fs) ** 2) - np.sum(np.abs(X3k) ** 2) / N) < 1e-6)

# ---------------------------------------------------------------------------------------- Example 3
lin = np.convolve([1, 2, 3], [1, 1])
c3 = dft.circ_conv([1, 2, 3], [1, 1], 3)
v.assert_true("Ex 3: 3-point circular is (4, 3, 5)", np.allclose(c3, [4, 3, 5]))
Nmin = next(N for N in range(3, 10) if N >= len(lin) and np.allclose(dft.circ_conv([1, 2, 3], [1, 1], N)[:4], lin))
v.check("Ex 16-03.3a", Nmin)
v.assert_true("Ex 3: wrapping preserves the sum", abs(np.sum(c3) - np.sum(lin)) < 1e-12)

# ---------------------------------------------------------------------------------------- Example 4
Xs = 1 / (1 - 0.5 * np.exp(-2j * np.pi * np.arange(4) / 4))
xt = np.real(dft.idft(Xs))
v.check("Ex 16-03.4a", xt[0])
v.assert_true("Ex 4: aliased samples equal 0.5^n / (1 - 0.5^4)", np.allclose(xt, 0.5 ** np.arange(4) / (1 - 0.5**4)))
v.check("Ex 16-03.4c", 100 * (xt[0] - 1))
Xs16 = 1 / (1 - 0.5 * np.exp(-2j * np.pi * np.arange(16) / 16))
v.check("Ex 16-03.4b", np.real(dft.idft(Xs16))[0] - 1)

# ---------------------------------------------------------------------------------------- Example 5
for N5, key in ((128, "a"), (256, "b"), (512, "c"), (1024, "d"), (2048, "e"), (4096, "f")):
    v.check(f"Ex 16-03.5{key}", dft.fft_conv_cost(101, N5))
best = min((dft.fft_conv_cost(101, 2**p), 2**p) for p in range(7, 16))
v.assert_true("Ex 5: best FFT size is 1024", best[1] == 1024)
v.check("Ex 16-03.5g", 101 / best[0])
v.check("Ex 16-03.5h", (best[1] - 100) / 48_000 * 1e3)
cross = next(M for M in range(2, 200) if min(dft.fft_conv_cost(M, 2**p) for p in range(int(math.ceil(math.log2(M))), 18)) < M)
v.check("Ex 16-03.5i", cross)
v.check("Ex 16-03.5j", min(dft.fft_conv_cost(cross, 2**p) for p in range(int(math.ceil(math.log2(cross))), 18)))
# block convolution correctness
xb = rng.normal(size=5000)
hb = rng.normal(size=101)
v.assert_true("Ex 5: overlap-add equals numpy.convolve", np.allclose(dft.overlap_add(xb, hb, 1024), np.convolve(xb, hb)))
v.assert_true("Ex 5: overlap-save equals numpy.convolve", np.allclose(dft.overlap_save(xb, hb, 1024), np.convolve(xb, hb)))

# ---------------------------------------------------------------------------------------- text and concept checks
v.check("Txt 16-03.a", 20 * math.log10(2 / math.pi))
Nl = 1 << 16
v.assert_true("Txt a: half-bin complex tone tends to 2/pi", abs(abs(np.sin(math.pi / 2) / (Nl * np.sin(math.pi / (2 * Nl)))) - 2 / math.pi) < 1e-8)
v.assert_true("Q1: unit sample has a flat DFT", np.allclose(dft.dft(np.r_[1.0, np.zeros(7)]), 1))
v.check("Txt 16-03.b", dft.dft(np.ones(8))[0].real)
v.check("Txt 16-03.c", float(dft.bin_freq(480, 500, 10_000)))
v.check("Txt 16-03.d", 64 - 1)
v.check("Txt 16-03.e", 256 - 64 + 1)
v.check("Txt 16-03.f", 5 - 1)

# ---------------------------------------------------------------------------------------- Problem 1
P1 = dft.dft([1, 0, -1, 0])
v.check("16-03.1a", P1[1].real)
v.check("16-03.1b", P1[3].real)
v.assert_true("P1: bins 0 and 2 are zero", abs(P1[0]) < 1e-12 and abs(P1[2]) < 1e-12)
v.assert_true("P1: the sequence is cos(pi n/2)", np.allclose([1, 0, -1, 0], np.cos(np.pi * np.arange(4) / 2), atol=1e-12))
v.check("16-03.1c", 1 / 4)

# ---------------------------------------------------------------------------------------- Problem 2
v.check("16-03.2a", 1e6 / 4096)
v.check("16-03.2b", 100e3 / (1e6 / 4096))
v.check("16-03.2c", float(dft.bin_freq(4000, 4096, 1e6)) / 1e3)

# ---------------------------------------------------------------------------------------- Problem 3
sh = X1 * np.exp(-2j * np.pi * np.arange(4) / 4)
v.assert_true("P3a: shift property equals a direct DFT", np.allclose(sh, dft.dft([4, 1, 2, 3])))
v.check("16-03.3a", sh[1])
v.check("16-03.3b", sh[2].real)
v.check("16-03.3c", sh[3])
md = np.roll(X1, 2)
v.assert_true("P3b: modulation property equals a direct DFT", np.allclose(md, dft.dft(np.array([1, 2, 3, 4]) * np.array([1, -1, 1, -1]))))
v.check("16-03.3d", md[1])
v.check("16-03.3e", md[2].real)

# ---------------------------------------------------------------------------------------- Problem 4
y4 = dft.circ_conv([1, 2, 0, 1], [1, -1, 0, 0], 4)
v.assert_true("P4: DFT product agrees", np.allclose(y4, dft.idft(dft.dft([1, 2, 0, 1]) * dft.dft([1, -1, 0, 0]))))
for k, key in enumerate("abcd"):
    v.check(f"16-03.4{key}", float(np.real(y4[k])))

# ---------------------------------------------------------------------------------------- Problem 5
x5, h5 = rng.normal(size=200), rng.normal(size=57)


def circ_equals_lin(N):
    return N >= 256 and np.allclose(np.fft.ifft(np.fft.fft(x5, N) * np.fft.fft(h5, N)).real[:256], np.convolve(x5, h5))


Nreq = next(N for N in range(200, 300) if circ_equals_lin(N))
v.check("16-03.5a", Nreq)
v.check("16-03.5b", 1 << (Nreq - 1).bit_length())
v.assert_true("P5: 255 points wrap the last output onto the first",
              not np.allclose(np.fft.ifft(np.fft.fft(x5, 255) * np.fft.fft(h5, 255)).real, np.convolve(x5, h5)[:255]))

# ---------------------------------------------------------------------------------------- Problem 6


def alias_err(N):
    Xs = 1 / (1 - 0.9 * np.exp(-2j * np.pi * np.arange(N) / N))
    return np.real(np.fft.ifft(Xs))[0] - 1


N6 = next(N for N in range(2, 200) if alias_err(N) < 0.01)
v.check("16-03.6a", N6)
v.check("16-03.6b", 100 * alias_err(N6))
v.assert_true("P6: error formula 0.9^N / (1 - 0.9^N)", abs(alias_err(N6) - 0.9**N6 / (1 - 0.9**N6)) < 1e-12)

# ---------------------------------------------------------------------------------------- Problem 7
n7 = np.arange(2048)
x7 = 2 * np.cos(2 * math.pi * 100 * n7 / 2048)
X7 = np.fft.fft(x7)
v.check("16-03.7a", abs(X7[100]))
v.assert_true("P7: mirror bin equal", abs(abs(X7[1948]) - abs(X7[100])) < 1e-6)
v.check("16-03.7b", float(np.mean(x7**2)))
v.assert_true("P7: Parseval", abs(np.sum(x7**2) - np.sum(np.abs(X7) ** 2) / 2048) < 1e-6)

# ---------------------------------------------------------------------------------------- Problem 8
n8 = np.arange(1000)
r50 = np.max(np.abs(np.fft.fft(np.cos(2 * math.pi * 50 * n8 / 1000)))) / 500
r505 = np.max(np.abs(np.fft.fft(np.cos(2 * math.pi * 50.5 * n8 / 1000)))) / 500
v.check("16-03.8a", r50)
v.check("16-03.8b", r505)
v.check("16-03.8c", 20 * math.log10(r505))

# ---------------------------------------------------------------------------------------- Problem 9
L9 = 128 - 33 + 1
v.check("16-03.9a", L9)
v.check("16-03.9b", math.ceil(10_000 / L9))
v.check("16-03.9c", 33 - 1)
y9 = dft.overlap_add(rng.normal(size=10_000), rng.normal(size=33), 128)
v.check("16-03.9d", len(y9))

# ---------------------------------------------------------------------------------------- Problem 10
for N10, key in ((512, "a"), (1024, "b"), (4096, "d")):
    v.check(f"16-03.10{key}", dft.fft_conv_cost(255, N10))
best10 = min((dft.fft_conv_cost(255, 2**p), 2**p) for p in range(8, 18))
v.check("16-03.10c", best10[0])
v.check("16-03.10e", best10[1])
v.check("16-03.10f", best10[1] - 255 + 1)
v.check("16-03.10g", 255 / best10[0])

# ---------------------------------------------------------------------------------------- Problem 11
n11 = np.arange(16)
X11 = dft.dft(np.cos(2 * math.pi * 3 * n11 / 16) + 0.5 * np.sin(2 * math.pi * 5 * n11 / 16))
v.check("16-03.11a", X11[3].real)
v.assert_true("P11: bin 13 equals bin 3", abs(X11[13] - X11[3]) < 1e-9)
v.check("16-03.11b", X11[5])
v.check("16-03.11c", abs(X11[11]))
v.assert_true("P11: all other bins zero", np.max(np.abs(np.delete(X11, [3, 5, 11, 13]))) < 1e-9)

# ---------------------------------------------------------------------------------------- Problem 12 and the cyclic prefix


def ofdm(Nsc, G, chan, nsym=200, seed=5):
    """QPSK on Nsc subcarriers, cyclic prefix G, linear channel, one-tap equalizer per subcarrier; no noise.
    Returns (rms error vector in percent of the symbol magnitude, number of wrong QPSK decisions)."""
    r = np.random.default_rng(seed)
    bits = r.integers(0, 2, (nsym, Nsc, 2))
    sym = ((2 * bits[..., 0] - 1) + 1j * (2 * bits[..., 1] - 1)) / math.sqrt(2)
    tx = []
    for s_ in sym:
        t = np.fft.ifft(s_)
        tx.append(np.concatenate([t[Nsc - G:], t]) if G else t)
    rx = np.convolve(np.concatenate(tx), chan)
    C = np.fft.fft(chan, Nsc)
    e2, errs = 0.0, 0
    for i in range(nsym):
        blk = rx[i * (Nsc + G) + G: i * (Nsc + G) + G + Nsc]
        est = np.fft.fft(blk) / C
        e2 += float(np.sum(np.abs(est - sym[i]) ** 2))
        errs += int(np.sum((np.sign(est.real) != np.sign(sym[i].real)) | (np.sign(est.imag) != np.sign(sym[i].imag))))
    return 100 * math.sqrt(e2 / (nsym * Nsc)), errs


chan17 = np.r_[1.0, 0.4 * np.exp(-np.arange(1, 17) / 5.0) * np.cos(np.arange(1, 17))]
v.assert_true("P12: the 17-tap test channel has no spectral null", np.min(np.abs(np.fft.fft(chan17, 64))) > 0.1)
v.check("16-03.12a", len(chan17) - 1)
v.assert_true("P12: a 16-sample prefix makes one-tap equalization exact on a 17-tap channel", ofdm(64, 16, chan17)[0] < 1e-9)
v.assert_true("P12: a 15-sample prefix leaves interference", ofdm(64, 15, chan17)[0] > 1e-6)
v.check("16-03.12b", 16 / 20e6 * 1e6)
v.check("16-03.12c", 100 * 16 / (64 + 16))
v.check("16-03.12d", 100 * 8 / (64 + 8))
v.check("16-03.12e", 100 * 8 / (256 + 8))

# ---------------------------------------------------------------------------------------- Lab
chan5 = np.array([1.0, 0.5, -0.3, 0.2, 0.1])
v.assert_true("Lab: the 5-tap channel has no spectral null (min |C| = 0.1)", abs(np.min(np.abs(np.fft.fft(chan5, 64))) - 0.1) < 1e-9)
res = {G: ofdm(64, G, chan5) for G in range(0, 7)}
v.check("Lab 16-03.a", min(G for G in res if res[G][0] < 1e-9))
v.check("Lab 16-03.b", 100 * 4 / (64 + 4))
v.check("Lab 16-03.c", res[0][0])
v.check("Lab 16-03.d", res[3][0])
v.check("Lab 16-03.e", res[0][1])
v.check("Lab 16-03.f", res[1][1])
v.assert_true("Lab: no wrong QPSK decisions from a 2-sample prefix on", all(res[G][1] == 0 for G in range(2, 7)))
v.check("Txt 16-03.g", min(G for G in res if res[G][0] < 1e-9))
# OFDM numerology arithmetic (R-236): 802.11a 16/80; LTE (160 + 6*144)/15360 Ts per slot; NR 144 kappa 2^-mu Tc at mu = 4
v.check("Txt 16-03.h", 100 * 16 / 80)
Ts = 1 / (15000 * 2048)
v.assert_true("R-236: an LTE slot is 15360 Ts = 0.5 ms", abs(15360 * Ts - 0.5e-3) < 1e-15 and 160 + 2048 + 6 * (144 + 2048) == 15360)
v.check("Txt 16-03.i", 100 * (160 + 6 * 144) / 15360)
Tc, kappa = 1 / (480e3 * 4096), 64
v.assert_true("R-236: kappa = Ts/Tc = 64", abs(Ts / Tc - kappa) < 1e-9)
v.check("Txt 16-03.j", 144 * kappa * 2**-4 * Tc * 1e6)
v.assert_true("R-236: 802.11a 0.8 us guard interval is 16 samples at 20 MHz and 312.5 kHz spacing is 20 MHz/64",
              abs(0.8e-6 * 20e6 - 16) < 1e-9 and abs(20e6 / 64 - 312.5e3) < 1e-9)

v.check("Txt 16-03.k", 2048 / 30.72e6 * 1e6)
v.check("Txt 16-03.l", 160 / 30.72e6 * 1e6)
v.check("Txt 16-03.m", 144 / 30.72e6 * 1e6)
v.assert_true("LTE prefix is 5.9-6.5x Wi-Fi's 0.8 us", 5.8 < 144 / 30.72e6 / 0.8e-6 < 6.0 and 6.4 < 160 / 30.72e6 / 0.8e-6 < 6.6)

# Problems 13 and 14
_n = np.arange(16)
_x13 = np.cos(2 * np.pi * 4 * _n / 16) + np.cos(2 * np.pi * 5 * _n / 16)
_X13 = np.abs(np.fft.fft(_x13))
v.check("16-03.13a", _X13[4])
v.assert_true("P13: other bins zero", np.max(np.delete(_X13, [4, 5, 11, 12])) < 1e-9)
for P_, key in ((64, "16-03.13b"), (256, "16-03.13c")):
    v.check(key, 5 * P_ // 16 - 4 * P_ // 16 - 1)
_Xp = np.abs(np.fft.fft(_x13, 256))
_dip = _Xp[64:81].min()
v.check("16-03.13d", _dip)
v.check("16-03.13e", 20 * math.log10(_dip / _X13[4]))
_x2 = np.cos(2 * np.pi * 4 * _n / 16) + np.cos(2 * np.pi * 4.5 * _n / 16)
_Xq = np.abs(np.fft.fft(_x2, 1 << 14))
_kk = np.arange(1 << 14) * 16 / (1 << 14)
_sel = (_kk > 3) & (_kk < 6)
v.check("16-03.13f", _kk[_sel][np.argmax(_Xq[_sel])])
_xx, _hh, _N, _L = [1, 2, 3, 4, 5, 6], [1, 1], 4, 3
v.check("16-03.14a", _N - len(_hh) + 1)
_buf = [0] + _xx + [0] * 4
_out = []
for _st in range(0, len(_xx) + 1, _L):
    _blk = _buf[_st:_st + _N]
    _yc = np.real(np.fft.ifft(np.fft.fft(_blk) * np.fft.fft(_hh, _N)))
    _out += list(np.round(_yc[1:], 9))
v.assert_true("P14: overlap-save equals direct convolution", np.allclose(_out[:7], np.convolve(_xx, _hh)))

sys.exit(v.finish())
