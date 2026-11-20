#!/usr/bin/env python3
"""Verify every number in chapter 11-10 (sampling, aliasing and reconstruction), its solutions and lab.

Independent routes:
- aliases by sampling tones and locating the FFT peak; phases by least-squares fits of the samples;
- noise folding by simulating band-limited white noise and sampling it, with and without a brick-wall filter;
- filter orders by evaluating scipy.signal Butterworth designs, not the closed-form bound alone;
- the zero-order hold by building a staircase on a fine grid and reading its spectrum;
- band-pass windows by checking replica overlap on a fine grid of sample rates;
- jitter by Monte Carlo sampling with Gaussian timing errors; quantization SNR by quantizing a sine;
- the ADS1292R chain by simulating an RC filter, a 128 kHz sampler and a sinc^3 decimator by 256 (R-190).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("11-10", COURSE / "chapters" / "11-10-sampling-aliasing-reconstruction.md",
                        COURSE / "solutions" / "11-10-solutions.md",
                        COURSE / "labs" / "11-10-lab" / "README.md")
db = lambda r: 20 * math.log10(abs(r))
rng = np.random.default_rng(2026)


def apparent(f0, fs, N=None):
    """Sample cos(2 pi f0 t) at fs and return the FFT peak frequency (1 Hz resolution or better)."""
    N = N or int(fs)
    n = np.arange(N)
    X = np.abs(np.fft.rfft(np.cos(2 * np.pi * f0 * n / fs)))
    return np.argmax(X) * fs / N


def fit_phase(x, f, fs):
    n = np.arange(len(x))
    A = np.column_stack([np.cos(2 * np.pi * f * n / fs), -np.sin(2 * np.pi * f * n / fs)])
    c, *_ = np.linalg.lstsq(A, x, rcond=None)
    return math.degrees(math.atan2(c[1], c[0]))


def butter_order(A_min, f_alias, fc):
    for n in range(1, 60):
        z, p, k = signal.butter(n, 2 * math.pi * fc, analog=True, output="zpk")
        _, h = signal.freqs_zpk(z, p, k, worN=[2 * math.pi * f_alias])
        if -db(h[0]) >= A_min:
            return n
    return None


def zoh_levels(f0, fs, freqs, over=1024, periods=20):
    """Staircase of cos(2 pi f0 n/fs) on a grid 'over' times finer; amplitudes at freqs, relative to 1."""
    # choose a record holding an integer number of cycles of both f0 and fs
    g = math.gcd(int(f0), int(fs))
    Ns = int(fs // g) * periods
    xs = np.cos(2 * np.pi * f0 * np.arange(Ns) / fs)
    st = np.repeat(xs, over)
    X = np.fft.rfft(st) / (len(st) / 2)
    df = fs * over / len(st)
    return [abs(X[int(round(f / df))]) for f in freqs], X, df


def sinc3(f, fDR=500.0, fMOD=128e3, N=256):
    return abs(np.sin(np.pi * f / fDR) / (N * np.sin(np.pi * f / fMOD))) ** 3


# ============================================================ theory
v.check("T 11-10.a", db(np.sinc(0.5)))
sig_t = 100e-15
v.check("T 11-10.b", -db(2 * math.pi * 70e6 * sig_t))
v.check("T 11-10.c", 20 * math.log10(2))
v.check("T 11-10.d", 10 * math.log10(1.5))
v.check("T 11-10.e", 512e3 / 4 / 1e3)
v.check("T 11-10.f", (512e3 / 4) / 500)
v.check("T 11-10.g", np.sinc(0.25))
v.check("T 11-10.h", db(np.sinc(0.25)))
v.check("T 11-10.i", apparent(7e3, 10e3) / 1e3)
v.check("T 11-10.k", 53.125 / 2)
# quantizer simulation for 6.02N + 1.76 at N = 12
N12 = 12
tq = np.arange(2 ** 20)
golden = (math.sqrt(5) - 1) / 2
xq = 0.5 * np.sin(2 * np.pi * 0.1 * golden * tq + 0.3) * (1 - 2 ** -N12)   # irrational frequency, inside full scale
q = 2.0 ** -N12
err = np.round(xq / q) * q - xq
snr_q = 10 * math.log10(np.mean(xq ** 2) / np.mean(err ** 2))
v.assert_true("simulated 12-bit SNR within 0.2 dB of 6.02N + 1.76", abs(snr_q - (6.0206 * 12 + 1.7609)) < 0.2)

# ============================================================ Example 1
v.check("Ex 11-10.1a", apparent(30e3, 48e3) / 1e3)
v.check("Ex 11-10.1b", apparent(50e3, 48e3) / 1e3)
v.check("Ex 11-10.1c", apparent(96.5e3, 48e3, N=96000) / 1e3)
n = np.arange(480)
v.check("Ex 11-10.1d", fit_phase(np.cos(2 * np.pi * 30e3 * n / 48e3 + math.radians(60)), 18e3, 48e3))

# ============================================================ Example 2: noise folding
def folded_ratio(B, fs, grid=200000):
    """Integrate a flat PSD on [0, B] folded into [0, fs/2], relative to the PSD's own share of [0, fs/2]."""
    f = (np.arange(grid) + 0.5) * (B / grid)
    fa = np.abs(((f + fs / 2) % fs) - fs / 2)
    return np.sum(fa <= fs / 2) * (B / grid) / (fs / 2)


ratio = folded_ratio(1e6, 48e3)
v.check("Ex 11-10.2a", ratio)
v.check("Ex 11-10.2b", 10 * math.log10(ratio))
v.check("Ex 11-10.2c", 20e-9 * math.sqrt(24e3) * 1e6)
v.check("Ex 11-10.2d", 20e-9 * math.sqrt(1e6) * 1e6)

# ============================================================ Example 3
v.check("Ex 11-10.3a", math.log(1e9 - 1) / (2 * math.log(28 / 20)))
v.check("Ex 11-10.3b", butter_order(90, 28e3, 20e3))
fmod = 128 * 48e3
v.check("Ex 11-10.3c", fmod / 1e6)
v.check("Ex 11-10.3d", math.log(1e9 - 1) / (2 * math.log((fmod - 20e3) / 20e3)))
v.assert_true("second order suffices when oversampled", butter_order(90, fmod - 20e3, 20e3) == 2)
for nn, key in ((1, "3e"), (2, "3f")):
    z, p, k = signal.butter(nn, 2 * math.pi * 20e3, analog=True, output="zpk")
    _, h = signal.freqs_zpk(z, p, k, worN=[2 * math.pi * (fmod - 20e3)])
    v.check(f"Ex 11-10.{key}", -db(h[0]))
v.check("Ex 11-10.3g", 20 * math.log10(1.4))
v.check("Ex 11-10.3h", math.log(1e9 - 1))
v.check("Ex 11-10.3i", 2 * math.log(1.4))
v.check("Ex 11-10.3j", (fmod - 20e3) / 20e3)

# ============================================================ Example 4: zero-order hold
(a20, a28, a68), _, _ = zoh_levels(20e3, 48e3, [20e3, 28e3, 68e3])
v.check("Ex 11-10.4a", a20)
v.check("Ex 11-10.4b", db(a20))
v.check("Ex 11-10.4c", a28)
v.check("Ex 11-10.4d", db(a28))
v.check("Ex 11-10.4e", db(a20) - db(a28))
v.check("Ex 11-10.4f", a68)
v.check("Ex 11-10.4g", db(a68))
_, Xz, dfz = zoh_levels(20e3, 48e3, [20e3])
ph = np.angle(Xz[int(round(20e3 / dfz))])
# the fine grid holds each value from the start of its fine step, so its centre lags by half a fine step less
v.check("Ex 11-10.4h", (-ph / (2 * math.pi * 20e3) + 0.5 / (48e3 * 1024)) * 1e6)

# ============================================================ Example 5
h5 = np.ones(5) / 5
H5 = lambda f: abs(np.sum(h5 * np.exp(-2j * np.pi * f / 500 * np.arange(5))))
v.check("Ex 11-10.5a", apparent(450, 500, N=5000))
xs = np.cos(2 * np.pi * 450 * np.arange(4000) / 500)
y = signal.lfilter(h5, [1.0], xs)[100:]
v.check("Ex 11-10.5b", np.sqrt(2 * np.mean(y ** 2)))          # amplitude of the steady-state sinusoid
v.check("Ex 11-10.5c", apparent(600, 500, N=5000))
v.assert_true("600 Hz input is removed", np.max(np.abs(signal.lfilter(h5, [1.0], np.cos(2 * np.pi * 600 *
                                                                                      np.arange(400) / 500))[10:])) < 1e-9)

# ============================================================ Example 6: band-pass sampling
fL, fH = 60e6, 80e6


def overlaps(fs, fL=fL, fH=fH, K=12):
    bands = []
    for k in range(-K, K + 1):
        bands.append((fL + k * fs, fH + k * fs))
        bands.append((-fH + k * fs, -fL + k * fs))
    a = [b for b in bands if b[1] > 0 and b[0] < fs / 2]
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if min(a[i][1], a[j][1]) - max(a[i][0], a[j][0]) > 1e-6:
                return True
    return False


def window(lo_guess, hi_guess):
    lo = brentq(lambda fs: 0.5 - overlaps(fs), lo_guess - 3e6, lo_guess + 1e5, xtol=1)
    hi = brentq(lambda fs: 0.5 - overlaps(fs), hi_guess - 1e5, hi_guess + 3e6, xtol=1)
    return lo, hi


lo3, hi3 = window(53.3e6, 60e6)
v.check("Ex 11-10.6a", lo3 / 1e6)
v.check("Ex 11-10.6b", hi3 / 1e6)
v.assert_true("40 MHz is allowed and 39.9 / 40.1 MHz are not",
              not overlaps(40e6) and overlaps(39.9e6) and overlaps(40.1e6))
v.check("Ex 11-10.6c", 40)
img = sorted([((f % 56e6) if (f % 56e6) <= 28e6 else 56e6 - (f % 56e6)) for f in (fL, fH)])
v.check("Ex 11-10.6d", img[0] / 1e6)
v.check("Ex 11-10.6e", img[1] / 1e6)
v.assert_true("upright: 60 MHz lands below 80 MHz's image", (fL % 56e6) < (fH % 56e6) <= 28e6)


def jitter_snr(f0, sig, N=2_000_000):
    tt = np.arange(N) / 997e6
    e = np.sin(2 * np.pi * f0 * (tt + rng.normal(0, sig, N))) - np.sin(2 * np.pi * f0 * tt)
    return 10 * math.log10(0.5 / np.mean(e ** 2))


v.check("Ex 11-10.6f", jitter_snr(70e6, sig_t), rtol=1e-3)
v.check("Ex 11-10.6g", jitter_snr(80e6, sig_t), rtol=1e-3)
v.check("Ex 11-10.6h", 56 / 20)

# ============================================================ Example 7: ADS1292R chain
v.check("Ex 11-10.7a", 1 / (2 * math.pi * 4e3 * 4.7e-9) / 1e3)
v.check("Ex 11-10.7b", sinc3(450) / 1e-3)
v.check("Ex 11-10.7c", -db(sinc3(450)))
v.check("Ex 11-10.7d", -db(sinc3(128e3 - 50)))
rc = lambda f: 1 / abs(1 + 1j * f / 8.4e3)
v.check("Ex 11-10.7e", -db(rc(127.95e3)))
v.check("Ex 11-10.7f", -db(rc(127.95e3)) - db(sinc3(128e3 - 50)))


def chain(f_in, seconds=4.0, with_rc=True):
    fM, N = 128e3, 256
    n = np.arange(int(fM * seconds))
    amp = rc(f_in) if with_rc else 1.0
    x = amp * np.cos(2 * np.pi * f_in * n / fM)
    box = np.ones(N) / N
    y = signal.lfilter(box, [1.0], signal.lfilter(box, [1.0], signal.lfilter(box, [1.0], x)))[::N]
    yy = y[20:]
    m = np.arange(len(yy))
    A = np.column_stack([np.cos(2 * np.pi * 50 * m / 500), np.sin(2 * np.pi * 50 * m / 500)])
    c, *_ = np.linalg.lstsq(A, yy, rcond=None)
    return db(np.hypot(*c))


v.check("T 11-10.j", chain(127.95e3) - chain(450))

# ============================================================ solutions
v.check("11-10.1a", 2 * 4)
v.check("11-10.1b", 10 / 2)
v.check("11-10.1c", (10 - 4) - 4)
for f, key in ((600, "2a"), (1100, "2b"), (1900, "2c"), (2450, "2d")):
    v.check(f"11-10.{key}", apparent(f, 1000, N=10000))
v.check("11-10.3a", apparent(700, 1000, N=10000))
n3 = np.arange(200)
x3 = np.cos(2 * np.pi * 700 * n3 / 1000 + math.radians(30))
v.check("11-10.3b", fit_phase(x3, 300, 1000))
v.check("11-10.3c", x3[1])
(g4,), _, _ = zoh_levels(12e3, 48e3, [12e3])
v.check("11-10.4a", g4)
v.check("11-10.4b", db(g4))
v.check("11-10.4c", np.sinc(0.5))
v.check("11-10.4d", db(np.sinc(0.5)))
v.check("11-10.5a", apparent(7e3, 8e3) / 1e3)
v.check("11-10.5b", apparent(7e3, 12e3) / 1e3)
v.assert_true("7 kHz is misreported at 13.9 kHz and correct at 14.1 kHz",
              apparent(7e3, 13.9e3, N=139000) != 7e3 and apparent(7e3, 14.1e3, N=141000) == 7e3)
v.check("11-10.5c", 2 * 7)
v.check("11-10.5d", apparent(3e3, 8e3) / 1e3)
v.check("11-10.6a", math.log(1e4 - 1) / (2 * math.log(350 / 150)))
v.check("11-10.6b", butter_order(40, 350, 150))
v.check("11-10.6c", math.log(1e4 - 1) / (2 * math.log(3850 / 150)))
v.check("11-10.6d", butter_order(40, 3850, 150))
v.check("11-10.6e", math.log(1e4 - 1))
v.check("11-10.6f", 2 * math.log(350 / 150))
v.check("11-10.6g", 3850 / 150)
v.check("11-10.7a", 20e-9 * math.sqrt(1e6) * 1e6)
v.check("11-10.7b", 20e-9 * math.sqrt(5e4) * 1e6)
v.check("11-10.7c", 10 * math.log10(folded_ratio(1e6, 100e3)))
(g20, g241), _, _ = zoh_levels(20e3, 44.1e3, [20e3, 24.1e3], over=256, periods=2)
v.check("11-10.8a", g20)
v.check("11-10.8b", db(g20))
v.check("11-10.8c", 44.1 - 20)
v.check("11-10.8d", g241)
v.check("11-10.8e", db(g241))
v.check("11-10.8f", db(g20) - db(g241))
h9 = np.ones(3) / 3
H9 = lambda f: abs(np.sum(h9 * np.exp(-2j * np.pi * f / 1000 * np.arange(3))))
v.check("11-10.9a", H9(100))
v.check("11-10.9b", apparent(900, 1000, N=10000))
# zero of the centred (real) response (1 + 2 cos w)/3
v.check("11-10.9c", brentq(lambda f: np.real(np.sum(h9 * np.exp(-2j * np.pi * f / 1000 * (np.arange(3) - 1)))),
                           250, 450))
tq = np.array([0.5e-3, 1.5e-3])
nn = np.arange(-2000, 2001)
xr = [np.sum((nn == 0) * np.sinc((t - nn * 1e-3) / 1e-3)) for t in tq]
v.check("11-10.10a", xr[0])
v.check("11-10.10b", xr[1])
fL2, fH2 = 10.6e6, 10.8e6
v.assert_true("n = 54 allows only 0.4 MHz", not overlaps(0.4e6, fL2, fH2, K=80) and overlaps(0.4001e6, fL2, fH2, K=80))
v.check("11-10.11a", 0.4)


def window2(lo_g, hi_g):
    lo = brentq(lambda fs: 0.5 - overlaps(fs, fL2, fH2, K=80), lo_g - 2e3, lo_g + 2e2, xtol=0.01)
    hi = brentq(lambda fs: 0.5 - overlaps(fs, fL2, fH2, K=80), hi_g - 2e2, hi_g + 2e3, xtol=0.01)
    return lo, hi


l50, h50 = window2(432e3, 432.65e3)
l40, h40 = window2(540e3, 543.59e3)
v.check("11-10.11b", l50 / 1e6)
v.check("11-10.11c", h50 / 1e6)
v.check("11-10.11d", (h50 - l50) / 1e3)
v.check("11-10.11e", l40 / 1e6)
v.check("11-10.11f", h40 / 1e6)
v.check("11-10.11g", (h40 - l40) / 1e3)
# solve in femtoseconds: brentq's absolute xtol (2e-12) would swamp a root of order 1e-13 s
v.check("11-10.12a", brentq(lambda s_fs: -db(2 * math.pi * 100e6 * s_fs * 1e-15) - 70, 1, 1e5))
v.check("11-10.12b", brentq(lambda s_fs: -db(2 * math.pi * 1e9 * s_fs * 1e-15) - 70, 1, 1e5))
v.check("11-10.13a", 6.02 * 12 + 1.76)
v.check("11-10.13b", 10 * math.log10(64))
v.check("11-10.13c", 6.02 * 12 + 1.76 + 10 * math.log10(64))
v.check("11-10.13d", (6.02 * 12 + 10 * math.log10(64)) / 6.02)
fc14 = brentq(lambda fc: 10 * math.log10(1 + (127.95e3 / fc) ** 2) - 40, 100, 1e5)
v.check("11-10.14a", fc14 / 1e3)
v.check("11-10.14b", 1 / (2 * math.pi * 4e3 * fc14) * 1e9)

# ============================================================ lab
v.check("Lab 11-10.a", apparent(30e3, 48e3) / 1e3)
v.check("Lab 11-10.b", db(a20))
v.check("Lab 11-10.c", db(a28))
# time-domain noise folding: band-limit white noise to 1 MHz at 48 kHz x 42, then keep every 42nd sample
M = 42
fsim = 48e3 * M
Nn = 2 ** 21
w = rng.normal(size=Nn)
W = np.fft.rfft(w)
fr = np.fft.rfftfreq(Nn, 1 / fsim)
wb = np.fft.irfft(W * (fr <= 1e6), Nn)
wf = np.fft.irfft(W * (fr <= 24e3), Nn)
v.check("Lab 11-10.d", 10 * math.log10(np.var(wb[::M]) / np.var(wf[::M])), rtol=5e-3)
v.check("Lab 11-10.e", chain(450))
v.check("Lab 11-10.f", chain(127.95e3))

sys.exit(v.finish())
