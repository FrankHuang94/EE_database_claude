#!/usr/bin/env python3
"""Verify every number in the Course 16 final-exam solutions.

Independent routes:
- aliasing by sampling tones and locating the FFT peak; moving-average gains by direct summation of e^{-jwn};
- the notch from its pole/zero definition, its exact -3 dB width by root finding on |H|, its DC gain by evaluation;
- DFT values with numpy.fft; FFT operation counts by enumerating every stage's twiddles;
- the coherent-bin choice by searching odd bins; ENOB and processing gain from their definitions, the floor offset
  checked against a simulated Hann-windowed periodogram;
- Kaiser and equiripple estimates from their formulas; the IIR order bounds re-derived here (elliptic with
  scipy.special.ellipk), the order-3 elliptic limit by solving the degree equation and confirmed by an actual design;
- reflection coefficients by the step-down recursion, checked against the pole radius; the DF II state gain on a
  dense grid;
- polyphase and direct decimation simulated and compared; CIC gain by summing the cascaded boxcar;
- the dead band by running the rounded recursion; the CORDIC residual by iterating the angle over a dense grid;
- Q12 designs with scipy.signal.ellip and scipy.signal.remez, measured on dense grids; group delay with
  scipy.signal.group_delay; the derivations' identities checked numerically.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.optimize import brentq
from scipy.special import ellipk

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("16-exam", ROOT / "exam" / "solutions.md")
PI = math.pi


def peak_freq(f0, fs, n=4800):
    t = np.arange(n) / fs
    X = np.abs(np.fft.rfft(np.cos(2 * PI * f0 * t)))
    return np.argmax(X) * fs / n


def freq_resp(b, a, w):
    e = np.exp(-1j * np.asarray(w, dtype=float))
    num = sum(bk * e**k for k, bk in enumerate(b))
    den = sum(ak * e**k for k, ak in enumerate(a))
    return num / den


# ------------------------------------------------------------------------------------------------- 1 basics
v.check("X16.1a", peak_freq(9000, 8000) / 1000)
v.check("X16.1b", 2 * PI * 1000 / 8000)
ma = lambda w: abs(sum(np.exp(-1j * w * n) for n in range(4)) / 4)  # noqa: E731
v.check("X16.1c", ma(0.0))
v.check("X16.1d", ma(PI / 4))
v.check("X16.1e", ma(PI / 2), tol=1e-9)
h = 0.5 ** np.arange(10)
n_e = 1 / math.log(2)
v.check("X16.1f", n_e)
v.assert_true("Q1 1/e point", abs(0.5**n_e - math.exp(-1)) < 1e-12)

# ------------------------------------------------------------------------------------------------- 2 notch
th = 2 * PI * 60 / 1000
r = 0.99
zeros = [np.exp(1j * th), np.exp(-1j * th)]
poles = [r * np.exp(1j * th), r * np.exp(-1j * th)]
b = np.real(np.poly(zeros))
a = np.real(np.poly(poles))
v.check("X16.2a", -b[1])
v.check("X16.2b", -a[1])
v.check("X16.2c", a[2])
v.check("X16.2d", (1 - r) * 1000 / PI)
g0 = abs(freq_resp(b, a, [0.0])[0])
gn = lambda w: abs(freq_resp(b, a, [w])[0]) / g0 - 1 / math.sqrt(2)  # noqa: E731
lo = brentq(gn, th - 0.05, th - 1e-6, xtol=1e-14)
hi = brentq(gn, th + 1e-6, th + 0.05, xtol=1e-14)
v.check("X16.2e", (hi - lo) * 1000 / (2 * PI))
v.check("X16.2f", -1 / math.log(r))
v.check("X16.2g", -1 / math.log(r) / 1000)
v.check("X16.2h", g0)
v.check("X16.2i", 1 / g0)

# ------------------------------------------------------------------------------------------------- 3 DFT
x = np.zeros(8)
x[:2] = 1
X = np.fft.fft(x)
v.check("X16.3a", X[0].real)
v.assert_true("Q3 X[2] = 1 - j", abs(X[2] - (1 - 1j)) < 1e-12)
v.check("X16.3b", abs(X[4]), tol=1e-9)
v.check("X16.3c", abs(X[1]))
v.check("X16.3d", 48000 / 1024)
v.check("X16.3e", 1024 - 129 + 1)
# overlap-save: confirm 896 valid outputs per block by direct comparison
rng = np.random.default_rng(16)
hf = rng.standard_normal(129)
xb = rng.standard_normal(1024)
circ = np.real(np.fft.ifft(np.fft.fft(xb) * np.fft.fft(hf, 1024)))
lin = np.convolve(xb, hf)[:1024]
valid = int(np.sum(np.abs(circ - lin) < 1e-9))
v.assert_true("Q3 overlap-save valid outputs", valid == 896, f"{valid}")
cost = 4 * (1024 * math.log2(1024) + 1024) / 896
v.check("X16.3f", cost)
v.check("X16.3g", 129 / cost)

# ------------------------------------------------------------------------------------------------- 4 FFT
N = 4096
m = int(math.log2(N))
v.check("X16.4a", m)
v.check("X16.4b", N // 2 * m)
nontriv = 0
for s in range(1, m + 1):
    size = 2**s
    for j in range(size // 2):
        wv = np.exp(-2j * PI * j / size)
        if not (abs(wv - 1) < 1e-12 or abs(wv + 1j) < 1e-12):
            nontriv += N // size
v.check("X16.4c", nontriv)
v.check("X16.4d", N * N / (N // 2 * m))
G = np.fft.fft([1, 0])
H = np.fft.fft([2, -1])
X4 = [G[0] + H[0], G[1] - 1j * H[1], G[0] - H[0], G[1] + 1j * H[1]]
v.assert_true("Q4c butterflies equal the DFT", np.allclose(X4, np.fft.fft([1, 2, 0, -1])))

# ------------------------------------------------------------------------------------------------- 5 ADC test
fs, N = 100e6, 8192
target = 10e6 / (fs / N)
odd = [k for k in range(1, N // 2) if math.gcd(k, N) == 1]
k = min(odd, key=lambda kk: abs(kk - target))
v.check("X16.5a", k)
v.check("X16.5b", k * fs / N / 1e6)
v.check("X16.5c", (70.0 - 1.76) / 6.02)
v.check("X16.5d", (71.0 - 1.76) / 6.02)
v.check("X16.5e", 10 * math.log10(N / 2))
hann = np.hanning(N + 1)[:N]  # periodic Hann
enbw = N * np.sum(hann**2) / np.sum(hann) ** 2
v.assert_true("Q5 Hann ENBW is 1.5 bins", abs(enbw - 1.5) < 1e-9)
pg = 10 * math.log10(N / (2 * enbw))
v.check("X16.5f", pg)
v.check("X16.5g", 72 + pg)
# simulate: a tone at SNR 72 dB, Hann-windowed; the mean noise bin sits ~106.4 dB below the tone bin
nn = np.arange(N)
A = 1.0
sigma = math.sqrt(A**2 / 2 / 10 ** (72 / 10))
floors = []
for seed in range(8):
    noise = np.random.default_rng(seed).standard_normal(N) * sigma
    S = np.abs(np.fft.rfft(hann * (A * np.cos(2 * PI * k * nn / N) + noise))) ** 2
    mask = np.ones_like(S, bool)
    mask[[0, k - 1, k, k + 1]] = False
    floors.append(10 * math.log10(S[k] / np.mean(S[mask])))
v.assert_true("Q5 simulated floor offset", abs(np.mean(floors) - (72 + pg)) < 0.2, f"{np.mean(floors):.2f}")

# ------------------------------------------------------------------------------------------------- 6 FIR design
dp = (10**0.005 - 1) / (10**0.005 + 1)
ds = 10 ** (-50 / 20)
v.check("X16.6a", dp)
v.check("X16.6b", ds)
v.assert_true("Q6 stopband governs", ds < dp)
Aatt = -20 * math.log10(min(dp, ds))
beta = 0.5842 * (Aatt - 21) ** 0.4 + 0.07886 * (Aatt - 21)
v.check("X16.6c", beta)
dw = 2 * PI * 1000 / 48000
M = (Aatt - 8) / (2.285 * dw)
v.check("X16.6d", M)
v.check("X16.6e", (-10 * math.log10(dp * ds) - 13) / (2.324 * dw))
Mk = math.ceil(M)
v.check("X16.6f", Mk / 2)
v.check("X16.6g", Mk / 2 / 48000 * 1e3)
v.check("X16.6h", (Mk + 1) // 2 + (Mk + 1) % 2)

# ------------------------------------------------------------------------------------------------- 7 IIR design
fs7 = 8000.0
Wp, Ws = math.tan(PI * 1000 / fs7), math.tan(PI * 2000 / fs7)
D = (10 ** (40 / 10) - 1) / (10 ** (1 / 10) - 1)
v.check("X16.7a", Wp)
v.check("X16.7b", Ws / Wp)
v.check("X16.7c", 2 * fs7 * Wp)
v.check("X16.7d", D)
v.check("X16.7e", math.log(D) / (2 * math.log(Ws / Wp)))
v.check("X16.7f", math.acosh(math.sqrt(D)) / math.acosh(Ws / Wp))


def ellip_order(kk, k1):
    return ellipk(kk**2) * ellipk(1 - k1**2) / (ellipk(k1**2) * ellipk(1 - kk**2))


kk = Wp / Ws
bound = ellip_order(kk, 1 / math.sqrt(D))
v.assert_true("Q7c elliptic bound 3.0012", abs(bound - 3.0012) < 5e-5, f"{bound:.5f}")
k1_3 = brentq(lambda k1: ellip_order(kk, k1) - 3, 1e-6, 0.5, xtol=1e-15)
As3 = 10 * math.log10(1 + (10**0.1 - 1) / k1_3**2)
v.check("X16.7g", As3)
# confirm with a real order-3 design at that attenuation: its stopband edge lands at the 2.414 ratio
b3, a3 = signal.ellip(3, 1, As3, 1.0, analog=True)
edge = brentq(lambda W: -20 * math.log10(abs(signal.freqs(b3, a3, [W])[1][0])) - As3 + 1e-9, 1.01, Ws / Wp * 1.001)
v.assert_true("Q7c order-3 design edge ratio", abs(edge - Ws / Wp) < 1e-3, f"{edge:.5f}")
unwarp = lambda f: 2 * math.atan(2 * PI * f / (2 * fs7)) * fs7 / (2 * PI)  # noqa: E731
v.check("X16.7h", unwarp(1000))
v.check("X16.7i", unwarp(2000))

# ------------------------------------------------------------------------------------------------- 8 structures
a8 = [1, -1.2, 0.81]
p8 = np.roots(a8)
v.check("X16.8a", abs(p8[0]))
v.check("X16.8b", abs(np.angle(p8[0])))
v.check("X16.8c", math.degrees(abs(np.angle(p8[0]))))
k2 = a8[2]
k1 = a8[1] / (1 + k2)
v.check("X16.8d", k2)
v.check("X16.8e", k1)
v.assert_true("Q8 |k| < 1 iff poles inside", (abs(k1) < 1 and abs(k2) < 1) and np.all(np.abs(p8) < 1))
th8 = abs(np.angle(p8[0]))
gp = 1 / abs(freq_resp(a8, [1], [th8])[0])
v.check("X16.8f", gp)
ww = np.linspace(0, PI, 400001)
v.check("X16.8g", np.max(1 / np.abs(freq_resp(a8, [1], ww))))
v.check("X16.8h", 20 * math.log10(gp))

# ------------------------------------------------------------------------------------------------- 9 multirate
for f0, key in ((30000, "X16.9a"), (50000, "X16.9b")):
    t = np.arange(4800) * 4 / 192000
    xs = np.cos(2 * PI * f0 * t)
    Xs = np.abs(np.fft.rfft(xs))
    v.check(key, np.argmax(Xs) * 48000 / 4800 / 1000)
v.check("X16.9c", 64 * 192000 / 1e6)
v.check("X16.9d", 64 * 48000 / 1e6)
# polyphase equals filter-then-downsample, using 64/4 = 16 taps per output phase
hd = rng.standard_normal(64)
xd = rng.standard_normal(400)
direct = np.convolve(xd, hd)[: len(xd)][::4]
poly = np.zeros(len(direct))
for p in range(4):
    ep = hd[p::4]
    xp = np.concatenate([np.zeros(p), xd])[: len(xd)][::4]
    poly += np.convolve(xp, ep)[: len(direct)]
v.assert_true("Q9 polyphase = direct", np.allclose(direct, poly))
box = np.ones(8)
cic = np.array([1.0])
for _ in range(3):
    cic = np.convolve(cic, box)
v.check("X16.9e", cic.sum())
v.check("X16.9f", math.log2(cic.sum()))

# ------------------------------------------------------------------------------------------------- 10 quantization
Kq = math.tan(PI / 8)
v.check("X16.10a", Kq)
bq, aq = signal.butter(2, 1000, fs=8000)
v.check("X16.10b", bq[0])
v.assert_true("Q10 b2 = b0", abs(bq[2] - bq[0]) < 1e-15)
v.check("X16.10c", bq[1])
v.check("X16.10d", aq[1])
v.check("X16.10f", aq[2])
dq = 1 + math.sqrt(2) * Kq + Kq * Kq
v.assert_true("Q10 closed-form coefficients match scipy", abs(Kq * Kq / dq - bq[0]) < 1e-12 and abs(2 * (Kq * Kq - 1) / dq - aq[1]) < 1e-12)
gq = signal.lfilter([1.0], aq, np.r_[1.0, np.zeros(4000)])
ngq = float(np.sum(gq**2))
v.assert_true("Q10 noise-gain formula", abs(ngq - (1 + aq[2]) / ((1 - aq[2]) * ((1 + aq[2]) ** 2 - aq[1] ** 2))) < 1e-9)
v.check("X16.10g", ngq)
v.check("X16.10h", 10 * math.log10(ngq))
v.check("X16.10i", math.sqrt(ngq / 12))
y = 20
for _ in range(200):
    y = math.floor(0.9 * y + 0.5)
v.check("X16.10e", y)
v.assert_true("Q10 dead band bound", abs(y - 1 / (2 * (1 - 0.9))) < 1e-9)

# ------------------------------------------------------------------------------------------------- 11 hardware
v.check("X16.11a", 18 + 18)
v.check("X16.11b", 18 + 18 + math.log2(512))
v.check("X16.11c", math.ceil(128 * 200e6 / 600e6))
v.check("X16.11d", (1.5 + 0.5) / 1)
v.check("X16.11e", (1.5 + 0.5) / 2)
# look-ahead form equals the original recursion
aa = 0.9
xl = rng.standard_normal(200)
y1 = signal.lfilter([1], [1, -aa], xl)
y2 = signal.lfilter([1, aa], [1, 0, -aa * aa], xl)
v.assert_true("Q11 look-ahead by 2 matches", np.allclose(y1, y2))


def cordic_residual(theta, n):
    z = theta
    for i in range(n):
        z -= math.copysign(math.atan(2.0**-i), z if z != 0 else 1)
    return abs(z)


grid = np.linspace(-PI / 2, PI / 2, 20001)
worst = {n: max(cordic_residual(t, n) for t in grid) for n in (10, 11)}
need = next(n for n in range(1, 20) if math.atan(2.0 ** -(n - 1)) < 2.0**-10)
v.check("X16.11f", need)
v.assert_true("Q11 11 iterations suffice, 10 do not", worst[11] < 2.0**-10 < worst[10],
              f"{worst[10]:.3e} {worst[11]:.3e}")

# ------------------------------------------------------------------------------------------------- 12 FIR vs IIR
sos = signal.ellip(4, 1, 40, 1000 / 4000, output="sos")
free = lambda c: abs(c) < 1e-12 or abs(abs(c) - 1) < 1e-9  # noqa: E731
mults = sum(0 if free(c) else 1 for sec in sos for c in list(sec[:3]) + list(sec[4:]))
v.check("X16.12a", mults)
dp12 = (10**0.05 - 1) / (10**0.05 + 1)
ds12 = 0.01
wp, ws = PI / 4, PI / 2
wpb = np.linspace(0, wp, 40001)
wsb = np.linspace(ws, PI, 40001)


def fir_meas(n):
    hh = signal.remez(n, [0, wp / (2 * PI), ws / (2 * PI), 0.5], [1, 0], weight=[1, dp12 / ds12],
                      fs=1.0, grid_density=64)
    ap = np.abs(np.polyval(hh[::-1], np.exp(-1j * wpb)))
    asb = np.abs(np.polyval(hh[::-1], np.exp(-1j * wsb)))
    return hh, 20 * math.log10(ap.max() / ap.min()), -20 * math.log10(asb.max())


h15, rip15, att15 = fir_meas(15)
_, rip14, att14 = fir_meas(14)
v.assert_true("Q12 15 taps meets the mask", rip15 <= 1 and att15 >= 40)
v.assert_true("Q12 14 taps fails", not (rip14 <= 1 and att14 >= 40))
v.assert_true("Q12 15-tap filter is symmetric", np.allclose(h15, h15[::-1]))
v.check("X16.12b", (15 - 1) // 2 + 1)
v.check("X16.12c", (15 - 1) / 2)
v.check("X16.12d", (-10 * math.log10(dp * 0.001) - 13) / (2.324 * 2 * PI / 48))
v.check("X16.12e", (-10 * math.log10(dp12 * ds12) - 13) / (2.324 * (ws - wp)))
bz, az = signal.sos2tf(sos)
v.check("X16.12f", -20 * math.log10(abs(freq_resp(bz, az, [ws])[0])))
v.check("X16.12g", rip15)
v.check("X16.12h", att15)
v.check("X16.12i", rip14)
gd = signal.group_delay((bz, az), w=np.linspace(1e-9, wp, 40001))[1]
v.assert_true("Q12 group delay 2.69 at DC", abs(gd[0] - 2.69) < 0.005, f"{gd[0]:.4f}")
v.assert_true("Q12 group delay peak 14.96", abs(gd.max() - 14.96) < 0.005, f"{gd.max():.4f}")
v.check("X16.12j", gd.max() - gd[0])
mag = np.abs(freq_resp(bz, az, np.linspace(ws, PI, 40001)))
v.assert_true("Q12 elliptic meets 40 dB", -20 * math.log10(mag.max()) >= 40 - 1e-6)
v.assert_true("Q12 the 4.9 of 16-07", abs(69 / 14 - 4.9) < 0.05)

# ------------------------------------------------------------------------------------------------- 13 derivations
e = np.linspace(-0.5, 0.5, 200001)
v.assert_true("Q13a uniform variance is 1/12", abs(np.trapezoid(e**2, e) - 1 / 12) < 1e-9)
v.assert_true("Q13a constants", abs(10 * math.log10(1.5) - 1.761) < 5e-4 and abs(20 * math.log10(2) - 6.0206) < 5e-5)
ht = rng.standard_normal(8)
ht = np.concatenate([ht, ht[::-1]])  # length 16, type II
v.assert_true("Q13b type II zero at pi", abs(np.polyval(ht[::-1], -1.0)) < 1e-12)
hn = rng.standard_normal(5)
xn = rng.standard_normal(300)
Mn = 3
up = np.zeros(len(hn) * Mn - (Mn - 1))
up[::Mn] = hn
left = np.convolve(xn, up)[: len(xn)][::Mn]
right = np.convolve(xn[::Mn], hn)[: len(left)]
v.assert_true("Q13c noble identity", np.allclose(left, right))

# ------------------------------------------------------------------------------------------------- 14 diligence
rate = 128 * 48000
v.check("X16.14a", rate / 1e6)
epm = 4e-6 / rate
v.check("X16.14b", epm * 1e12)
v.check("X16.14c", 3.2e-12 / epm)
v.check("X16.14d", (120 - 1.76) / 6.02)
v.check("X16.14e", 127 / 2)
v.check("X16.14f", 127 / 2 / 48000 * 1e3)
v.check("X16.14g", (127 / 2 / 48000) / 1e-4)
v.check("X16.14h", 4e-6 / (64 * 48000) * 1e12)
v.check("X16.14i", 10e-12 / epm)
v.check("X16.14j", 1e-4 * 48000)

sys.exit(v.finish())
