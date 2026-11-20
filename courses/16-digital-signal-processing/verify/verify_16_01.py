#!/usr/bin/env python3
"""Verify chapter 16-01 (discrete-time signals and systems review): examples, concept checks and problems.

Routes:
- aliasing by sampling both tones and comparing the sample arrays, not by the folding formula alone;
- periods by brute-force search for the smallest N with x[n + N] = x[n];
- convolution with numpy.convolve against the lab's MAC-counting loop;
- impulse and step responses with scipy.signal.lfilter against the lab's direct-form-I loop and the closed forms;
- moving-average gains from the direct DTFT sum against the closed form;
- EMA settling and noise gain by simulation and by summing h^2 numerically;
- wraparound arithmetic with numpy int8/int4 emulation and the lab's running_sum;
- stability by pole radii and by partial sums of |h|.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(ROOT / "labs" / "16-01-lab"))
from eeverify import Verifier  # noqa: E402
import dtsys as ds  # noqa: E402

CH = ROOT / "chapters" / "16-01-discrete-time-systems-review.md"
v = Verifier.from_files("16-01", CH, ROOT / "solutions" / "16-01-solutions.md", ROOT / "labs" / "16-01-lab" / "README.md")


def brute_period(x_of_n, nmax=1000):
    """Smallest N <= nmax with x[n + N] == x[n] for n in 0..3*nmax (to 1e-9), else None."""
    n = np.arange(3 * nmax + nmax + 1)
    x = x_of_n(n)
    for N in range(1, nmax + 1):
        if np.allclose(x[N:N + 3 * nmax], x[:3 * nmax], atol=1e-9):
            return N
    return None


def dtft(h, w):
    k = np.arange(len(h))
    return np.sum(np.asarray(h)[:, None] * np.exp(-1j * np.outer(k, np.atleast_1d(w))), axis=0)


def ma_gain_direct(N, f, fs):
    return float(np.abs(dtft(np.full(N, 1 / N), 2 * math.pi * f / fs))[0])


# ---------------------------------------------------------------------------------------- Example 1
v.check("Ex 16-01.1a", ds.digital_freq(1e3, 48e3))
v.check("Ex 16-01.1b", brute_period(lambda n: np.cos(2 * math.pi * n / 48)))
v.check("Ex 16-01.1c", ds.digital_freq(7e3, 8e3))
n = np.arange(64)
v.assert_true("Ex 1: 7 kHz and 1 kHz tones give identical samples at 8 kHz",
              np.allclose(np.cos(2 * math.pi * 7e3 * n / 8e3), np.cos(2 * math.pi * 1e3 * n / 8e3)))
v.check("Ex 16-01.1d", ds.apparent_freq(7e3, 8e3) / 1e3)
v.check("Ex 16-01.1e", brute_period(lambda n: np.cos(3 * math.pi * n / 8)))
v.assert_true("Ex 1: cos(0.3n) has no period up to 1000 samples", brute_period(lambda n: np.cos(0.3 * n)) is None)

# ---------------------------------------------------------------------------------------- Example 2
fs2, N2 = 1000.0, 20
v.check("Ex 16-01.2a", fs2 / N2)
v.assert_true("Ex 2: nulls at 50, 100, ..., 450 Hz", all(ma_gain_direct(N2, 50 * m, fs2) < 1e-12 for m in range(1, 10)))
g10, g25, g60 = (ma_gain_direct(N2, f, fs2) for f in (10, 25, 60))
v.assert_true("Ex 2: closed form equals the direct DTFT sum",
              all(abs(ds.ma_gain(N2, 2 * math.pi * f / fs2) - ma_gain_direct(N2, f, fs2)) < 1e-12 for f in (10, 25, 60)))
v.check("Ex 16-01.2b", g10)
v.check("Ex 16-01.2c", 20 * math.log10(g10))
v.check("Ex 16-01.2d", g25)
v.check("Ex 16-01.2m", 20 * math.log10(g25))
v.check("Ex 16-01.2e", g60)
v.check("Ex 16-01.2f", 20 * math.log10(g60))
# delay: the phase of H is -w (N-1)/2 where the real factor is positive (check at 10 Hz)
w10 = 2 * math.pi * 10 / fs2
ph = float(np.angle(dtft(np.full(N2, 1 / N2), w10))[0])
v.check("Ex 16-01.2g", -ph / w10)
v.check("Ex 16-01.2h", -ph / w10 / fs2 * 1e3)
# recursive sum: two additions per sample; outputs equal the direct average
x = np.random.default_rng(1).integers(-100, 100, 200)
s_rec, _ = ds.running_sum(list(x), N2)
v.assert_true("Ex 2: recursive sum equals the direct 20-point sum",
              np.array_equal(s_rec, np.convolve(x, np.ones(N2, int))[:len(x)]))
# count the additions the recursive structure performs per sample once the window is full
ops = {"add": 0}


def counted_running_sum(xs, N):
    s_prev, out = 0, []
    for k, xk in enumerate(xs):
        s_new = s_prev + xk
        ops["add"] += 1
        if k >= N:
            s_new = s_new - xs[k - N]
            ops["add"] += 1
        out.append(s_new)
        s_prev = s_new
    return out


counted_running_sum(list(range(N2 + 100)), N2)
before = ops["add"]
ops["add"] = 0
counted_running_sum(list(range(N2 + 101)), N2)
v.check("Ex 16-01.2i", ops["add"] - before)   # one more steady-state sample costs this many additions
N100 = int(fs2 / math.gcd(50, 60))   # nulls at multiples of gcd(50, 60) = 10 Hz
v.check("Ex 16-01.2j", N100)
v.assert_true("Ex 2: N = 100 nulls 50 and 60 Hz", ma_gain_direct(N100, 50, fs2) < 1e-12 and ma_gain_direct(N100, 60, fs2) < 1e-12)
v.check("Ex 16-01.2k", (N100 - 1) / 2 / fs2 * 1e3)
v.check("Ex 16-01.2l", ma_gain_direct(N100, 5, fs2))

# ---------------------------------------------------------------------------------------- Example 3
a3 = 1 / 16
tau = -1 / math.log(1 - a3)
v.check("Ex 16-01.3a", tau)
v.check("Ex 16-01.3b", tau * 1.0)  # 1 ms per sample
v.assert_true("Ex 3: approximation 1/alpha - 1/2 within 0.01 sample", abs(tau - (1 / a3 - 0.5)) < 0.01)
y3 = ds.ema(a3, np.ones(200))
v.assert_true("Ex 3: EMA step response matches 1 - (1-a)^(n+1)",
              np.allclose(y3, 1 - (1 - a3) ** (np.arange(200) + 1), atol=1e-14))
y3s = signal.lfilter([a3], [1, -(1 - a3)], np.ones(200))
v.assert_true("Ex 3: scipy lfilter agrees", np.allclose(y3, y3s, atol=1e-14))
n1 = int(np.argmax(np.abs(1 - y3) <= 0.01))
v.check("Ex 16-01.3c", n1)
h3 = ds.impulse([a3], [1, -(1 - a3)], 2000)
v.check("Ex 16-01.3d", float(np.sum(h3**2)))
v.check("Ex 16-01.3e", 1 / float(np.sum(h3**2)))
ma31 = ds.step(np.full(31, 1 / 31), [1], 60)
v.check("Ex 16-01.3f", int(np.argmax(np.abs(ma31 - 1) < 1e-12)))
v.assert_true("Ex 3: the 31-point average is not yet settled at n = 29", abs(ma31[29] - 1) > 0.01)
v.check("Ex 16-01.3g", n1 / tau)
v.check("Ex 16-01.3h", math.log(0.01) / math.log(15 / 16))
v.assert_true("Ex 3: e^-3 is about 5% and e^-5 about 0.7%",
              abs(math.exp(-3) - 0.05) < 0.0003 and abs(math.exp(-5) - 0.007) < 0.0005)

# ---------------------------------------------------------------------------------------- Example 4
x4 = [25, 30, 32, 33, 30]
s_wrap, mid_wrap = ds.running_sum(x4, 4, bits=8)
v.check("Ex 16-01.4a", int(mid_wrap[4]))
v.check("Ex 16-01.4b", int(s_wrap[4]))
v.assert_true("Ex 4: wrapped result equals the true sum", int(s_wrap[4]) == sum(x4[1:5]))
# independent route: numpy int8 arithmetic wraps natively
with np.errstate(over="ignore"):
    acc = np.int8(0)
    hist = []
    for k, xn in enumerate(x4):
        mid = np.int8(acc + np.int8(xn))
        acc = np.int8(mid - np.int8(x4[k - 4] if k >= 4 else 0))
        hist.append((int(mid), int(acc)))
v.assert_true("Ex 4: numpy int8 reproduces the trace", hist[4] == (int(mid_wrap[4]), int(s_wrap[4])))
v.assert_true("Ex 4: the accumulator holds 25, 55, 87, 120 before n = 4", [h[1] for h in hist[:4]] == [25, 55, 87, 120])


def run4(x, mode, upset_at=None):
    """Recursive 4-sample moving sum on an 8-bit accumulator, simulated step by step (wrap or saturate)."""
    fix = (lambda v_: ((v_ + 128) % 256) - 128) if mode == "wrap" else (lambda v_: max(-128, min(127, v_)))
    acc, out = 0, []
    for k, xn in enumerate(x):
        acc = fix(fix(acc + xn) - (x[k - 4] if k >= 4 else 0))
        if k == upset_at:
            acc = fix(acc + 1)
        out.append(acc)
    return out


sat = run4(x4, "sat")[4]
v.check("Ex 16-01.4c", sat)
v.check("Ex 16-01.4e", run4(x4, "wrap", upset_at=2)[4])
v.check("Ex 16-01.4f", run4(x4, "sat", upset_at=2)[4])
v.assert_true("Ex 4: the saturating upset is absorbed at n = 4", run4(x4, "sat", 2)[4] == run4(x4, "sat")[4])
v.check("Ex 16-01.4d", sum(x4[1:5]) - sat)

# ---------------------------------------------------------------------------------------- Example 5
mac_ch = 256 + 10 * 5
rate = 2 * 48_000 * mac_ch
v.check("Ex 16-01.5a", rate / 1e6)
v.check("Ex 16-01.5b", 100 * rate / (200e6 * 2))
v.check("Ex 16-01.5c", 200e6 / (2 * 48_000))
v.check("Ex 16-01.5d", mac_ch / 2)
v.assert_true("Ex 5: load x available cycles = needed cycles",
              abs((rate / 400e6) * 200e6 / (2 * 48_000) - mac_ch / 2) < 1e-9)
# FIR group delay from the phase of a symmetric 256-tap filter (any symmetric taps): -dphase/dw = 127.5
hs = np.hanning(258)[1:-1]
ws = np.array([0.01, 0.02])
phs = np.unwrap(np.angle(dtft(hs, ws)))
gd = -(phs[1] - phs[0]) / (ws[1] - ws[0])
v.assert_true("Ex 5: a symmetric 256-tap FIR has group delay 127.5 samples", abs(gd - 127.5) < 1e-6)
v.check("Ex 16-01.5e", gd / 48_000 * 1e3)
v.check("Ex 16-01.5f", 2 * 64 / 48_000 * 1e3)
v.check("Ex 16-01.5g", (gd + 128) / 48_000 * 1e3)
E_mul32, E_add32, E_sram8k, E_instr = 3.1e-12, 0.1e-12, 10e-12, 70e-12   # Horowitz ISSCC 2014 (R-208)
v.check("Ex 16-01.5h", rate * (E_mul32 + E_add32) * 1e6)
v.check("Ex 16-01.5i", rate * 2 * E_sram8k * 1e6)
v.check("Ex 16-01.5j", rate / 2 * E_instr * 1e3)
v.assert_true("Ex 5: SRAM energy is more than six times the arithmetic", 2 * E_sram8k / (E_mul32 + E_add32) > 6)

# ---------------------------------------------------------------------------------------- Concept checks
v.check("Txt 16-01.a", ds.apparent_freq(900, 1000))
v.check("Txt 16-01.b", brute_period(lambda n: np.cos(math.pi * n / 5)))
v.check("Txt 16-01.c", 1 / (1 / 8) - 0.5)
v.check("Txt 16-01.d", -1 / math.log(7 / 8))
v.check("Txt 16-01.e", (2 - 1 / 8) / (1 / 8))
v.check("Txt 16-01.f", (101 - 1) / 2)
v.check("Txt 16-01.g", (101 - 1) / 2 / 16_000 * 1e3)
v.check("Txt 16-01.h", 101 * 16_000 / 1e6)

# 30-tap FFE at 106.25 GBd (R-234 symbol rate, R-235 tap count), one sample per symbol
v.check("Txt 16-01.i", 30 * 106.25e9 / 1e12)

# ---------------------------------------------------------------------------------------- Problem 1
v.check("16-01.1a", ds.digital_freq(441, 44_100))
v.check("16-01.1b", ds.digital_freq(11_025, 44_100))
v.check("16-01.1c", brute_period(lambda n: np.cos(2 * math.pi * 441 * n / 44_100), nmax=200))
v.check("16-01.1d", brute_period(lambda n: np.cos(2 * math.pi * 11_025 * n / 44_100)))
v.check("16-01.1e", 11_025 / 44_100)

# ---------------------------------------------------------------------------------------- Problem 2
n = np.arange(100)
ref = np.cos(2 * math.pi * 300 * n / 1000)
for f, key in ((700, "a"), (1300, "b"), (1700, "c"), (2200, "d")):
    fa = ds.apparent_freq(f, 1000)
    v.check(f"16-01.2{key}", fa)
    same = np.allclose(np.cos(2 * math.pi * f * n / 1000), ref)
    v.assert_true(f"P2: {f} Hz {'matches' if fa == 300 else 'differs from'} the 300 Hz samples", same == (fa == 300))
v.assert_true("P2: mirrored sines flip sign", np.allclose(np.sin(2 * math.pi * 700 * n / 1000), -np.sin(2 * math.pi * 300 * n / 1000)))

# ---------------------------------------------------------------------------------------- Problem 3
v.check("16-01.3a", brute_period(lambda n: np.cos(math.pi * n / 6)))
v.assert_true("P3: cos(n/6) not periodic", brute_period(lambda n: np.cos(n / 6)) is None)
v.check("16-01.3b", brute_period(lambda n: np.sin(0.7 * math.pi * n)))
v.check("16-01.3c", brute_period(lambda n: np.cos(0.8 * math.pi * n) + np.cos(0.5 * math.pi * n)))
v.check("16-01.3d", brute_period(lambda n: np.exp(1j * 5 * math.pi * n / 3)))
v.check("16-01.3e", brute_period(lambda n: np.cos(0.5 * math.pi * n)))
v.assert_true("P3: dt_period agrees for 7/20 and 5/6", ds.dt_period(7, 20) == 20 and ds.dt_period(5, 6) == 6)

# ---------------------------------------------------------------------------------------- Problem 4 (spot checks)
med = lambda a: float(np.median(a))  # noqa: E731
v.assert_true("P4e: the median is not additive", med([1, 0, 0]) + med([0, 1, 0]) != med([1, 1, 0]))

# ---------------------------------------------------------------------------------------- Problem 5
y5, macs5 = ds.conv_mac([1, 2, 3], [2, -1, 1])
v.assert_true("P5: MAC loop equals numpy.convolve", np.allclose(y5, np.convolve([1, 2, 3], [2, -1, 1])))
for k, key in enumerate("abcde"):
    v.check(f"16-01.5{key}", y5[k])
v.check("16-01.5f", macs5)
v.check("16-01.5g", sum([1, 2, 3]) * sum([2, -1, 1]))
v.assert_true("P5: sum identity", abs(y5.sum() - 12) < 1e-12)

# ---------------------------------------------------------------------------------------- Problem 6
h6 = ds.impulse([1, 1], [1, -0.5], 40)
v.assert_true("P6: lfilter agrees", np.allclose(h6, signal.lfilter([1, 1], [1, -0.5], np.r_[1.0, np.zeros(39)])))
nn = np.arange(40)
v.assert_true("P6: closed form h", np.allclose(h6, np.where(nn == 0, 1.0, 1.5 * 0.5 ** (nn - 1.0))))
v.check("16-01.6a", h6[3])
s6 = ds.step([1, 1], [1, -0.5], 40)
v.assert_true("P6: closed form s = 4 - 3 (0.5)^n", np.allclose(s6, 4 - 3 * 0.5**nn))
v.check("16-01.6b", s6[0])
v.check("16-01.6c", s6[3])
v.check("16-01.6d", (1 + 1) / (1 - 0.5))
v.assert_true("P6: the sum of h is the DC gain", abs(ds.impulse([1, 1], [1, -0.5], 200).sum() - 4) < 1e-12)

# ---------------------------------------------------------------------------------------- Problem 7
v.check("16-01.7a", float(np.sum(0.9 ** np.arange(2000))))
v.assert_true("P7b: (-1.1)^n grows", abs((-1.1) ** 200) > 1e8)
v.assert_true("P7c: the harmonic partial sums keep growing (> 9 at 10^4 terms)", np.sum(1 / np.arange(1, 10**4 + 1)) > 9)
v.check("16-01.7b", math.pi**2 / 6)
v.assert_true("P7d: partial sum of 1/(n+1)^2 approaches pi^2/6", abs(np.sum(1 / np.arange(1, 10**6 + 1) ** 2) - math.pi**2 / 6) < 2e-6)
h7 = ds.impulse([1], [1, -1.6, 0.64], 400)
v.assert_true("P7e: h = (n+1) 0.8^n", np.allclose(h7, (np.arange(400) + 1) * 0.8 ** np.arange(400)))
v.assert_true("P7e: double pole at 0.8, stable", ds.is_stable([1, -1.6, 0.64]) and np.allclose(np.abs(ds.poles([1, -1.6, 0.64])), 0.8, atol=1e-6))
v.check("16-01.7c", float(np.sum(np.abs(h7))))
v.assert_true("P7f: poles at +/-1, not stable", not ds.is_stable([1, 0, -1]))

# ---------------------------------------------------------------------------------------- Problem 8
for k in range(1, 12):
    if -1 / math.log(1 - 2.0**-k) >= 50:
        break
a8 = 2.0**-k
v.check("16-01.8a", 1 / a8)
v.assert_true("P8: 1/32 is too fast", -1 / math.log(1 - 1 / 32) < 50)
v.check("16-01.8b", -1 / math.log(1 - a8))
v.check("16-01.8c", -1 / math.log(1 - a8))
v.check("16-01.8d", (2 - a8) / a8)
y8 = ds.ema(a8, np.ones(400))
v.check("16-01.8e", int(np.argmax(np.abs(1 - y8) <= 0.01)))

# ---------------------------------------------------------------------------------------- Problem 9
v.check("16-01.9a", 960 // 60)
g = ma_gain_direct(16, 10, 960)
v.check("16-01.9b", g)
v.check("16-01.9c", 20 * math.log10(g))
v.check("16-01.9d", ma_gain_direct(16, 50, 960))
v.assert_true("P9: nulls at 60, 120, 180 Hz", all(ma_gain_direct(16, f, 960) < 1e-12 for f in (60, 120, 180)))
w9 = 2 * math.pi * 10 / 960
d9 = -float(np.angle(dtft(np.full(16, 1 / 16), w9))[0]) / w9
v.check("16-01.9e", d9)
v.check("16-01.9f", d9 / 960 * 1e3)

# ---------------------------------------------------------------------------------------- Problem 10
b10, a10 = [1, 0.5], [1, -0.9, 0.5]
v.check("16-01.10a", (len(b10) - 1) + (len(a10) - 1))
v.check("16-01.10b", max(len(b10), len(a10)) - 1)
v.check("16-01.10c", sum(1 for c in (b10[1], a10[1], a10[2]) if c not in (0, 1, -1)))
v.check("16-01.10d", 4 - 1)  # four terms combined by two-input adders
p10 = ds.poles(a10)
v.check("16-01.10e", float(abs(p10[0])))
v.check("16-01.10f", math.degrees(abs(float(np.angle(p10[0])))))
v.assert_true("P10: stable", ds.is_stable(a10))
h10 = ds.impulse(b10, a10, 4)
v.assert_true("P10: lfilter agrees", np.allclose(h10, signal.lfilter(b10, a10, [1, 0, 0, 0])))
v.check("16-01.10g", h10[1])
v.check("16-01.10h", h10[2])
v.check("16-01.10i", h10[3])

# ---------------------------------------------------------------------------------------- Problem 11
h11 = [0.25, 0.5, 0.25]
for w, key in ((0.0, None), (math.pi / 2, "b"), (math.pi / 3, "c"), (math.pi, "d")):
    H = dtft(h11, w)[0]
    v.assert_true(f"P11: H = e^-jw (0.5 + 0.5 cos w) at w = {w:.4f}",
                  abs(H - np.exp(-1j * w) * (0.5 + 0.5 * math.cos(w))) < 1e-12)
    if key:
        v.check(f"16-01.11{key}", abs(H))
nn = np.arange(40)
y11 = signal.lfilter(h11, [1], 2 * np.ones(40))
v.check("16-01.11a", y11[-1])
y11b = signal.lfilter(h11, [1], np.cos(math.pi * nn / 2))
v.assert_true("P11b: steady state 0.5 cos(pi n/2 - pi/2) from n = 2",
              np.allclose(y11b[2:], 0.5 * np.cos(math.pi * nn[2:] / 2 - math.pi / 2), atol=1e-12))
y11c = signal.lfilter(h11, [1], np.cos(math.pi * nn / 3))
v.assert_true("P11c: steady state 0.75 cos(pi n/3 - pi/3) from n = 2",
              np.allclose(y11c[2:], 0.75 * np.cos(math.pi * nn[2:] / 3 - math.pi / 3), atol=1e-12))

# ---------------------------------------------------------------------------------------- Problem 12
# exact width: largest |product| of 12-bit and 16-bit signed values times 64, as a signed width
maxprod = (2**11) * (2**15)            # (-2048) * (-32768)
need = 64 * maxprod
width = next(b for b in range(8, 80) if -(2 ** (b - 1)) <= -need and need <= 2 ** (b - 1) - 1)
v.check("16-01.12a", width)
v.check("16-01.12b", 48 - (12 + 16))
v.check("16-01.12f", 48 - width)
need_sum = 64 * 2**11                   # 64 x (-2048) is the most negative sum
width_sum = next(b for b in range(4, 40) if -(2 ** (b - 1)) <= -need_sum and 64 * (2**11 - 1) <= 2 ** (b - 1) - 1)
v.check("16-01.12c", width_sum)
s12, mid12 = ds.running_sum([3, 4, 2], 2, bits=4)
v.check("16-01.12d", int(mid12[2]))
v.check("16-01.12e", int(s12[2]))
v.assert_true("P12: wrapped result is the true sum", int(s12[2]) == 4 + 2)
rng = np.random.default_rng(7)
xr = list(rng.integers(-2048, 2048, 3000))
sw, _ = ds.running_sum(xr, 64, bits=width_sum)
v.assert_true("P12: an 18-bit wraparound running sum of 64 12-bit samples is exact",
              np.array_equal(sw, np.convolve(xr, np.ones(64, int))[:3000]))

# ---------------------------------------------------------------------------------------- Problem 13
r13 = 2 * 16_000 * (128 + 4 * 5)
v.check("16-01.13a", r13 / 1e6)
v.check("16-01.13b", 100 * r13 * 1.5 / 48e6)
fir13 = (128 - 1) / 2 / 16_000 * 1e3
v.check("16-01.13c", fir13)
v.check("16-01.13d", 2 * 32 / 16_000 * 1e3)
v.check("16-01.13e", fir13 + 2 * 32 / 16_000 * 1e3)
v.check("16-01.13f", 2 * 64 / 16_000 * 1e3)
v.check("16-01.13g", fir13 + 2 * 64 / 16_000 * 1e3)
v.check("16-01.13h", r13 * 1.5 * 70e-12 * 1e3)
v.check("16-01.13i", r13 * 3.2e-12 * 1e6)
v.check("16-01.13j", (r13 * 1.5 * 70e-12) / (r13 * 3.2e-12))
v.assert_true("P13: 32-sample blocks meet 10 ms, 64-sample blocks do not",
              fir13 + 4.0 < 10 < fir13 + 8.0)

# ---------------------------------------------------------------------------------------- Problem 14
b14, a14 = [1, -2, 1], [1, -2, 1]
h14 = ds.impulse(b14, a14, 50)
v.assert_true("P14: h = delta", np.allclose(h14, np.r_[1.0, np.zeros(49)]))
# inject an error into the stored y at n0 and run the recursion by hand
x14 = np.random.default_rng(3).normal(size=1200)
n0, eps = 100, 1e-3
y_ok = np.zeros(1200)
y_bad = np.zeros(1200)
for yy, inject in ((y_ok, False), (y_bad, True)):
    for k in range(1200):
        acc = x14[k]
        acc += -2 * x14[k - 1] if k >= 1 else 0
        acc += x14[k - 2] if k >= 2 else 0
        acc += 2 * yy[k - 1] if k >= 1 else 0
        acc += -yy[k - 2] if k >= 2 else 0
        yy[k] = acc + (eps if (inject and k == n0) else 0.0)
err = y_bad - y_ok
v.assert_true("P14: error grows as (n - n0 + 1) eps", np.allclose(err[n0:], (np.arange(1200 - n0) + 1) * eps, rtol=1e-6, atol=1e-9))
v.check("16-01.14a", err[n0 + 1000] / eps)

# ---------------------------------------------------------------------------------------- Lab
xl = np.random.default_rng(16).normal(size=1000)
hl = np.random.default_rng(17).normal(size=64)
yl, macs_l = ds.conv_mac(xl, hl)
v.assert_true("Lab: conv_mac equals numpy.convolve", np.allclose(yl, np.convolve(xl, hl)))
v.check("Lab 16-01.a", macs_l)
# a 10 Hz sinusoid through the 20-point average: steady-state amplitude by least squares on the output
nl = np.arange(4000)
yl10 = signal.lfilter(np.full(20, 1 / 20), [1], np.cos(2 * math.pi * 10 * nl / 1000))[100:]
A = np.c_[np.cos(2 * math.pi * 10 * nl[100:] / 1000), np.sin(2 * math.pi * 10 * nl[100:] / 1000)]
coef = np.linalg.lstsq(A, yl10, rcond=None)[0]
v.check("Lab 16-01.b", float(np.hypot(*coef)))
v.check("Lab 16-01.c", math.sqrt(1 / 31))
noise = np.random.default_rng(5).normal(size=400_000)
r_ema = ds.ema(1 / 16, noise)[1000:].std()
r_ma = signal.lfilter(np.full(31, 1 / 31), [1], noise)[1000:].std()
v.assert_true("Lab: simulated residual noise of both filters within 1% of 1/sqrt(31)",
              abs(r_ema / math.sqrt(1 / 31) - 1) < 0.01 and abs(r_ma / math.sqrt(1 / 31) - 1) < 0.01)
v.check("Lab 16-01.d", ds.apparent_freq(1200, 1000))

sys.exit(v.finish())
