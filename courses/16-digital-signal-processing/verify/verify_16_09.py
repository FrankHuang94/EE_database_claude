#!/usr/bin/env python3
"""Verify chapter 16-09 (multirate DSP): examples, text, problems and lab answers.

Routes:
- aliases and images from FFTs of simulated tones (not from the folding formula used in the text);
- polyphase decimation, interpolation and rational resampling against direct filtering (scipy.signal.upfirdn as an
  independent reference);
- equiripple and half-band designs with scipy.signal.remez, minimum lengths by search, responses by freqz;
- CIC responses against the frequency response of a cascade of moving sums (scipy.signal.freqz), the bit-true model
  against an exact integer convolution, and the committed Verilog vectors regenerated and compared.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "16-09-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import multirate as mr  # noqa: E402
import make_vectors as mv  # noqa: E402

CH = ROOT / "chapters" / "16-09-multirate-dsp.md"
v = Verifier.from_files("16-09", CH, ROOT / "solutions" / "16-09-solutions.md", LAB / "README.md")
PI = math.pi


def peaks_khz(y, fs, k):
    Y = np.abs(np.fft.rfft(y * np.hanning(len(y))))
    f = np.fft.rfftfreq(len(y), 1 / fs)
    out = []
    for _ in range(k):
        i = int(np.argmax(Y))
        out.append(f[i] / 1000)
        Y[max(0, i - 8): i + 9] = 0
    return sorted(out)


def maxdev(h, fs, fp, fst):
    _, Hp = signal.freqz(h, worN=np.linspace(0, 2 * PI * fp / fs, 4000))
    _, Hs = signal.freqz(h, worN=np.linspace(2 * PI * fst / fs, PI, 4000))
    return float(np.max(np.abs(np.abs(Hp) - 1))), float(np.max(np.abs(Hs)))


def shortest(fs, fp, fst, dp, ds, start, halfband=False):
    rng_ = (4 * K + 3 for K in range(60)) if halfband else range(start, start + 300)
    for n in rng_:
        w = None if halfband else [1, dp / ds]
        h = signal.remez(n, [0, fp, fst, fs / 2], [1, 0], weight=w, fs=fs, grid_density=64 if halfband else 32)
        a, b = maxdev(h, fs, fp, fst)
        if a <= dp and b <= ds:
            return n, h
    raise RuntimeError("no design found")


# ---------------------------------------------------------------------------------------- Example 1, Problem 1
n = np.arange(48000)
x = sum(np.cos(2 * PI * f * n / 48000) for f in (1000, 10000, 17000))
pk = peaks_khz(mr.downsample(x, 4), 12000, 3)
v.check("Ex 16-09.1a", pk[1])
v.check("Ex 16-09.1b", pk[2])
v.check("Ex 16-09.1c", 12 - 3)
v.check("Ex 16-09.1d", 12 / 2)
x3 = sum(np.cos(2 * PI * f * n / 48000) for f in (7000, 13000))
pk3 = peaks_khz(mr.downsample(x3, 3), 16000, 2)
v.check("16-09.1c", pk3[0])
v.check("16-09.1a", pk3[1])
pk9 = peaks_khz(mr.downsample(np.cos(2 * PI * 9000 * n / 48000), 3), 16000, 1)
v.check("16-09.1b", pk9[0])

# ---------------------------------------------------------------------------------------- Example 2, Problem 2
x16 = np.cos(2 * PI * 5000 * np.arange(16000) / 16000)
pku = peaks_khz(mr.upsample(x16, 3), 48000, 3)
v.check("Ex 16-09.2a", pku[1])
v.check("Ex 16-09.2b", pku[2])
xu = mr.upsample(x16, 3)
Xu = np.abs(np.fft.rfft(xu)) / len(xu) * 2
v.assert_true("each component has a third of the tone's amplitude", abs(Xu.max() - 1 / 3) < 1e-3)
v.check("Ex 16-09.2c", round(1 / Xu.max()))
x8 = np.cos(2 * PI * 1000 * np.arange(8000) / 8000)
pk4 = peaks_khz(mr.upsample(x8, 4), 32000, 4)
v.check("16-09.2a", pk4[1])
v.check("16-09.2b", pk4[2])
v.check("16-09.2c", pk4[3])

# ---------------------------------------------------------------------------------------- Example 3, polyphase
rng = np.random.default_rng(9)
xr = rng.standard_normal(2000)
hr = rng.standard_normal(96)
ref = signal.upfirdn(hr, xr, up=1, down=8)[: -(-2000 // 8)]
v.assert_true("polyphase decimator equals upfirdn", np.allclose(mr.decimate_polyphase(xr, hr, 8), ref))
v.assert_true("polyphase interpolator equals upfirdn",
              np.allclose(mr.interpolate_polyphase(xr[:300], hr, 4), signal.upfirdn(hr, xr[:300], up=4)[:1200]))
v.assert_true("polyphase rational resampler equals upfirdn",
              np.allclose(mr.resample_polyphase(xr[:300], hr, 5, 4), signal.upfirdn(hr, xr[:300], up=5, down=4)[:375]))
v.check("Ex 16-09.3a", 96 * 48000 / 1e6)
v.check("Ex 16-09.3b", mr.polyphase(hr, 8).shape[1])
v.check("Ex 16-09.3c", 96 * 6000)
v.check("Ex 16-09.3d", (96 * 48000) / (96 * 6000))

# ---------------------------------------------------------------------------------------- Example 4
dp, ds = 1e-3, 1e-4
est = (-10 * math.log10(dp * ds) - 13) / (2.324 * 2 * PI * 8e3 / 384e3)
v.check("Ex 16-09.4a", est)
n1, h1 = shortest(384e3, 20e3, 28e3, dp, ds, int(est) - 10)
v.check("Ex 16-09.4b", n1)
v.assert_true("one tap fewer fails", maxdev(signal.remez(n1 - 1, [0, 20e3, 28e3, 192e3], [1, 0], weight=[1, 10], fs=384e3,
                                                          grid_density=32), 384e3, 20e3, 28e3)[1] > ds
              or maxdev(signal.remez(n1 - 1, [0, 20e3, 28e3, 192e3], [1, 0], weight=[1, 10], fs=384e3, grid_density=32),
                        384e3, 20e3, 28e3)[0] > dp)
single_rate = math.ceil(n1 / 2) * 48e3
v.check("Ex 16-09.4c", single_rate / 1e6)
stages, rate = [], 0.0
for F, key in ((384e3, "Ex 16-09.4d"), (192e3, "Ex 16-09.4e"), (96e3, "Ex 16-09.4f")):
    nh, hh = shortest(F, 20e3, F / 2 - 20e3, ds, ds, 0, halfband=True)
    c = (nh - 1) // 2
    v.assert_true(f"stage {F / 1e3:.0f} kHz: middle tap 1/2, even offsets ~0",
                  abs(hh[c] - 0.5) < 1e-4 and max(abs(hh[c + 2 * j]) for j in range(1, c // 2 + 1)) < 1e-5)
    v.check(key, nh)
    stages.append(hh)
    rate += ((c + 1) // 2) * F / 2
    _kf = {384e3: ("Ex 16-09.4k", "Ex 16-09.4n"), 192e3: ("Ex 16-09.4l", "Ex 16-09.4o"), 96e3: ("Ex 16-09.4m", "Ex 16-09.4p")}[F]
    v.check(_kf[0], (c + 1) // 2)
    v.check(_kf[1], ((c + 1) // 2) * F / 2)
v.check("Ex 16-09.4g", rate / 1e6)
v.check("Ex 16-09.4h", single_rate / rate)
v.check("Ex 16-09.4i", 1e6 * (n1 - 1) / 2 / 384e3)
v.check("Ex 16-09.4j", 1e6 * sum((len(s) - 1) / 2 / F for s, F in zip(stages, (384e3, 192e3, 96e3))))
v.check("Ex 16-09.4q", math.ceil(n1 / 2))
v.check("Ex 16-09.4r", 100 * (sum((len(s) - 1) / 2 / F for s, F in zip(stages, (384e3, 192e3, 96e3))) / ((n1 - 1) / 2 / 384e3) - 1))
f = np.linspace(0, 192e3, 200001)
w = 2 * PI * f / 384e3
H = np.ones_like(w, dtype=complex)
for s, sc in zip(stages, (1, 2, 4)):
    H = H * signal.freqz(s, worN=sc * w)[1]
H = np.abs(H)
alias = np.zeros_like(f, bool)
for k in range(1, 5):
    alias |= np.abs(f - k * 48e3) <= 20e3
v.check("Lab 16-09.b", -20 * math.log10(H[alias].max()))
v.assert_true("cascade passband within ±0.0011 dB", np.max(np.abs(20 * np.log10(H[f <= 20e3]))) < 0.0011)

# ---------------------------------------------------------------------------------------- Example 5 and Problem 11


def cic_ref(fv, R, N, fs):
    """|H| from freqz of the moving-sum cascade, normalized by R^N."""
    b = np.ones(R)
    for _ in range(N - 1):
        b = np.convolve(b, np.ones(R))
    _, Hc = signal.freqz(b, worN=2 * PI * np.atleast_1d(fv) / fs)
    return np.abs(Hc) / R ** N


fm = 12.8e6
v.assert_true("lab CIC response equals the moving-sum cascade",
              np.allclose(mr.cic_response([20e3, 91e3, 309e3, 380e3], 32, 4, fm), cic_ref([20e3, 91e3, 309e3, 380e3], 32, 4, fm)))
f3 = brentq(lambda fv: 20 * math.log10(cic_ref(fv, 32, 4, fm)[0]) + 10 * math.log10(2), 1e3, 2e5, xtol=1e-6)
v.check("Ex 16-09.5a", f3 / 1e3)
v.check("Ex 16-09.5i", f3 / 400e3)
v.check("Ex 16-09.5b", 20 * math.log10(cic_ref(20e3, 32, 4, fm)[0]))
v.check("Ex 16-09.5c", -20 * math.log10(cic_ref(380e3, 32, 4, fm)[0]))
v.check("Ex 16-09.5d", -20 * math.log10(cic_ref(309e3, 32, 4, fm)[0]))
v.check("Ex 16-09.5e", 4 * math.log2(32))
v.check("Ex 16-09.5f", 1e6 * 4 * 32 / fm)
v.check("Ex 16-09.5g", 10.63 - 1e6 * 4 * 32 / fm)       # R-243: data-sheet latency 10.63 µs at OSR 32
v.assert_true("the 0.63 µs overhead is the same at OSR 64 and 128 (R-243: 20.63, 40.63 µs)",
              abs(20.63 - 1e6 * 4 * 64 / fm - 0.63) < 1e-9 and abs(40.63 - 1e6 * 4 * 128 / fm - 0.63) < 1e-9)
v.check("Ex 16-09.5h", 1e6 * 68 / 400e3 / 10.63)          # R-238: settling 68/fDATA; R-243: sinc4 latency 10.63 µs
v.check("Ex 16-09.5j", 1e6 * 4 * (32 - 1) / 2 / fm)
v.check("Ex 16-09.5k", len(np.convolve(np.convolve(np.ones(32), np.ones(32)), np.convolve(np.ones(32), np.ones(32)))))
f64 = brentq(lambda fv: 20 * math.log10(cic_ref(fv, 64, 4, fm)[0]) + 10 * math.log10(2), 1e3, 1e5, xtol=1e-6)
v.check("16-09.11a", f64 / 1e3)
v.check("16-09.11b", 1e6 * 4 * 64 / fm)

# ---------------------------------------------------------------------------------------- text
v.check("Txt 16-09.a", 44.1 * 160 / 1000)
v.check("Txt 16-09.b", math.gcd(44100, 48000))
v.check("Txt 16-09.d", 0.4535 * 44.1)                      # R-247: SRC4392 passband 0.4535 fSIN
v.check("Txt 16-09.e", 1e3 * 102.53125 / 48000)            # R-247: 102.53125/fSIN
v.check("Txt 16-09.f", 1e3 * 46.53125 / 48000)             # R-247: 46.53125/fSIN


def wraps_counted(x, N, W, stage):
    """Count actual wrap events of a W-bit two's-complement register: compare the exact sum with the wrapped one."""
    exact = [0] * N
    wrapped = [0] * N
    count = 0
    for xn in x:
        val, valw = xn, xn
        for i in range(N):
            exact[i] += val
            raw = wrapped[i] + valw
            wrapped[i] = ((raw + 2 ** (W - 1)) % 2**W) - 2 ** (W - 1)
            if i == stage and wrapped[i] != raw:
                count += 1
            val, valw = exact[i], wrapped[i]
    return count, max(abs(e) for e in exact)


c4, vmax = wraps_counted(mv.tests[0], mv.N, mv.W, mv.N - 1)
v.check("Txt 16-09.c", c4)
v.check("Txt 16-09.i", vmax / 2**mv.W)
v.assert_true("lab helper reports the same wrap count", mv.integrator_wraps(mv.tests[0]) == c4)
v.check("Txt 16-09.g", wraps_counted(mv.tests[0], mv.N, mv.W, mv.N - 2)[0])
v.check("Txt 16-09.h", 1e3 * 36.46875 / 48000)            # R-247: decimation filter 36.46875/fSOUT

# ---------------------------------------------------------------------------------------- Problems 3-10, 12
xa = np.array([1, 2, 3, 4, 5, 6], float)
pa = signal.lfilter([1, 0, 1], [1], xa)[::2]
pb = signal.lfilter([1, 1], [1], xa[::2])
v.assert_true("noble identity holds on the example", np.allclose(pa, pb))
v.check("16-09.3a", pa[1])
v.check("16-09.3b", pa[2])
E = mr.polyphase(np.arange(1, 8), 3)
v.assert_true("polyphase components (1,4,7), (2,5,0), (3,6,0)", np.allclose(E, [[1, 4, 7], [2, 5, 0], [3, 6, 0]]))
v.check("16-09.4a", 7 * 10000)
v.check("16-09.4b", 7 * 30000)
g = math.gcd(44100, 48000)
v.check("16-09.5a", 48000 // g)
v.check("16-09.5b", 44100 // g)
v.check("16-09.5c", 44100 * 160 / 1e6)
v.check("16-09.5d", 3200 * 44100 * 160 / 1e9)
v.check("16-09.5e", 3200 / 160)
v.check("16-09.5f", 20 * 48000)
nh59, h59 = shortest(96e3, 20e3, 28e3, 1e-4, 1e-4, 0, halfband=True)
E59 = mr.polyphase(h59, 2)
v.assert_true("59-tap half-band: E1 is 0.5 z^-14", nh59 == 59 and abs(E59[1][14] - 0.5) < 1e-4
              and np.max(np.abs(np.delete(E59[1], 14))) < 1e-5)
v.check("16-09.6a", int(np.sum(np.abs(h59) > 1e-5)))
v.check("16-09.6b", (int(np.sum(np.abs(E59[0]) > 1e-5))) // 2)
v.check("16-09.6c", (int(np.sum(np.abs(E59[0]) > 1e-5))) // 2 * 48000)
v.check("16-09.7a", 16 ** 3)
v.check("16-09.7b", 3 * math.log2(16))
v.check("16-09.7c", 20 * math.log10(cic_ref(10e3, 16, 3, 1.6e6)[0]))
v.check("16-09.7d", -20 * math.log10(cic_ref(90e3, 16, 3, 1.6e6)[0]))
v.check("16-09.8a", 16 + 5 * math.log2(64))
M9 = (-10 * math.log10(1e-7) - 13) / (2.324 * 2 * PI * 8 / 192)
v.check("16-09.9a", M9)
v.check("16-09.9b", (math.ceil(M9) + 1) * 192e3 / 1e6)
v.check("16-09.9c", (math.ceil(M9) + 1) * 48e3 / 1e6)
est10 = (-10 * math.log10(dp * ds) - 13) / (2.324 * 2 * PI * 8e3 / 192e3)
n10, _ = shortest(192e3, 20e3, 28e3, dp, ds, int(est10) - 10)
v.check("16-09.10a", n10)
r10 = math.ceil(n10 / 2) * 48e3
v.check("16-09.10b", r10 / 1e6)
nA, _ = shortest(192e3, 20e3, 76e3, ds, ds, 0, halfband=True)
nB, _ = shortest(96e3, 20e3, 28e3, ds, ds, 0, halfband=True)
v.check("16-09.10c", nA)
v.check("16-09.10d", nB)
r2 = ((nA - 1) // 2 + 1) // 2 * 96e3 + ((nB - 1) // 2 + 1) // 2 * 48e3
v.check("16-09.10e", r2 / 1e6)
v.check("16-09.10f", r10 / r2)
y12 = mr.interpolate_polyphase([2, 4, 6], [0.5, 1, 0.5], 2)
v.assert_true("polyphase interpolation of (2,4,6) is (1,2,3,4,5,6)", np.allclose(y12, [1, 2, 3, 4, 5, 6]))
v.check("16-09.12a", y12[0])
v.check("16-09.12b", y12[1])
v.check("16-09.12c", y12[5])

# ---------------------------------------------------------------------------------------- CIC model and HDL vectors
def exact_cic(xs, R, N):
    """Exact integer CIC output: N moving sums of length R (no wrap-around), every R-th sample."""
    seq = [int(t) for t in xs]
    for _ in range(N):
        seq = [sum(seq[max(0, k - R + 1): k + 1]) for k in range(len(seq))]
    return seq[R - 1::R]


v.assert_true("bit-true CIC (with wrap-around) equals the exact moving-sum cascade on every test",
              all(mr.cic_decimate_int(xs, mv.R, mv.N, mv.W) == exact_cic(xs, mv.R, mv.N) for xs in mv.tests))
v.assert_true("vectors.hex is the current model output", (LAB / "vectors.hex").read_text().split() == mv.build())

# ---------------------------------------------------------------------------------------- Lab: 44.1 -> 48 kHz
L, M = 160, 147
hp = signal.firwin(3201, 20000, window=("kaiser", 9.0), fs=44100 * L) * L
xs = np.sin(2 * PI * 1000 * np.arange(4410) / 44100)
ys = signal.upfirdn(hp, xs, up=L, down=M)
m_ = np.arange(len(ys))
refs = np.sin(2 * PI * 1000 * (m_ - 1600 / M) / 48000)
v.check("Lab 16-09.a", 20 * math.log10(np.max(np.abs(ys[500: 4800 - 100] - refs[500: 4800 - 100]))))

sys.exit(v.finish())
