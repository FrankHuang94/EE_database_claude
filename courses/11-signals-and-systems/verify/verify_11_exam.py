#!/usr/bin/env python3
"""Verify every number in the Course 11 final-exam solutions.

Independent routes (not the hand formulas of the solutions):
- the period by searching for the smallest shift that repeats the sampled signal; power by numerical averaging;
- convolution by numerical integration and numpy.convolve; impulse responses by iterating the recursions;
- the square wave's harmonics and THD by FFT of a sampled square wave;
- spectra and energy fractions by numerical integration; DTFT values by direct summation;
- residues as numerical limits; poles with numpy.roots; overshoot by simulating the step response;
- transforms by numerical Fourier integrals; a two-sided inverse z-transform checked on the unit circle;
- the sample-filter-hold chain by simulation and FFT; AM efficiency by FFT power.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("11-exam", HERE.parent / "exam" / "solutions.md")
db = lambda r: 20 * math.log10(abs(r))
rng = np.random.default_rng(1101)


def apparent(f0, fs, N):
    n = np.arange(N)
    X = np.abs(np.fft.rfft(np.cos(2 * np.pi * f0 * n / fs)))
    return np.argmax(X) * fs / N


# 1
fsx = 120000.0
t = np.arange(int(fsx * 0.1)) / fsx
x1 = 3 * np.cos(200 * np.pi * t) + 2 * np.sin(300 * np.pi * t)
period = next(k for k in range(1, len(t) // 2) if np.max(np.abs(x1[k:k + 2000] - x1[:2000])) < 1e-9)
v.check("X11.1a", period / fsx * 1e3)
v.check("X11.1b", np.mean(x1[: int(fsx * 0.02) * 5] ** 2))

# 2(iii)
h = 0.5 ** np.arange(200)
v.check("X11.2a", np.sum(np.abs(h)))
v.assert_true("constant input B reaches the bound", abs(np.convolve(np.ones(400), h)[399] - 2) < 1e-12)

# 3
y = lambda tt: quad(lambda tau: math.exp(-(tt - tau)) if 0 <= tau <= 2 and tau <= tt else 0.0, 0, min(tt, 2))[0]
v.check("X11.3a", y(1.0))
v.check("X11.3b", y(3.0))
v.check("X11.3c", np.convolve([1, 2, 3], [1, -1])[3])

# 4
v.check("X11.4a", np.roots([1, -1.2, 0.36]).real.mean())
imp = np.zeros(400)
imp[0] = 1
h4 = signal.lfilter([1.0], [1, -1.2, 0.36], imp)
v.check("X11.4b", h4[3])
v.check("X11.4c", h4[4])
v.check("X11.4d", h4.sum())

# 5
N5 = 2 ** 16
sq = np.where(np.arange(N5) < N5 // 2, 1.0, -1.0)
S = np.fft.rfft(sq) / (N5 / 2)
v.check("X11.5a", abs(S[3]))
v.check("X11.5b", abs(S[1]) ** 2 / 2 / np.mean(sq ** 2))
harm = sum(abs(S[k]) ** 2 / 2 for k in range(2, N5 // 2))
v.check("X11.5c", 100 * math.sqrt(harm / (abs(S[1]) ** 2 / 2)), rtol=2e-4)

# 6: transforms by numerical integration, not by the properties used in the solution
def ft_num(fn, w, t_end=60.0):
    re = quad(lambda tt: fn(tt) * math.cos(w * tt), 0, t_end, limit=800)[0]
    im = quad(lambda tt: -fn(tt) * math.sin(w * tt), 0, t_end, limit=800)[0]
    return complex(re, im)


y6 = lambda tt: math.exp(-2 * (tt - 1)) if tt >= 1 else 0.0
Y2 = quad(lambda tt: y6(tt) * math.cos(2 * tt), 1, 40, limit=800)[0] - 1j * quad(
    lambda tt: y6(tt) * math.sin(2 * tt), 1, 40, limit=800)[0]
v.check("X11.6a", abs(Y2))
v.assert_true("Y(j2) matches e^{-j2}/(2 + j2)", abs(Y2 - np.exp(-2j) / (2 + 2j)) < 1e-7)
z6 = lambda tt: tt * math.exp(-tt)
v.assert_true("Z(jw) matches 1/(1 + jw)^2 at three frequencies",
              all(abs(ft_num(z6, w) - 1 / (1 + 1j * w) ** 2) < 1e-7 for w in (0.3, 1.0, 2.5)))
v.check("X11.6b", quad(lambda tt: z6(tt) ** 2, 0, 80)[0])
Iw = quad(lambda w: 1 / (1 + w * w) ** 2, -np.inf, np.inf)[0]
v.check("X11.6c", Iw)
v.check("X11.6d", Iw / (2 * math.pi))

# 7
h7 = np.ones(4) / 4
H7 = lambda w: abs(np.sum(h7 * np.exp(-1j * w * np.arange(4))))
v.check("X11.7a", H7(math.pi / 4))
w1 = minimize_scalar(H7, bounds=(1.2, 1.9), method="bounded", options={"xatol": 1e-12}).x
v.check("X11.7b", w1 / math.pi)
v.assert_true("second null at pi", H7(math.pi) < 1e-12)
wq = np.linspace(0.05, 1.4, 50)
v.check("X11.7c", -np.polyfit(wq, np.unwrap([np.angle(np.sum(h7 * np.exp(-1j * w * np.arange(4)))) for w in wq]), 1)[0])

# 8
X8 = lambda s: (s + 3) / ((s + 1) * (s + 2))
eps = 1e-7
v.check("X11.8a", (eps * X8(-1 + eps)).real)
v.check("X11.8b", (eps * X8(-2 + eps)).real)
v.check("X11.8c", signal.impulse(([1, 3], [1, 3, 2]), T=np.linspace(0, 1, 1001))[1][-1])

# 9
p9 = np.roots([1, 4, 13])
v.check("X11.9a", abs(p9[0]))
v.check("X11.9b", -p9[0].real / abs(p9[0]))
_, ys = signal.step(([13], [1, 4, 13]), T=np.linspace(0, 6, 60001))
v.check("X11.9c", 100 * (ys.max() - 1))
v.check("X11.9d", brentq(lambda K: -np.roots([1, 4, K])[0].real / abs(np.roots([1, 4, K])[0]) - 1 / math.sqrt(2),
                         4.5, 30))

# 10: residues as numerical limits; the two-sided inverse checked by summing its z-transform on the unit circle
X10 = lambda zinv: 1 / ((1 - 0.8 * zinv) * (1 + 1.25 * zinv))
eps = 1e-8
A10 = ((1 - 0.8 * (1 / 0.8 + eps)) * X10(1 / 0.8 + eps))
B10 = ((1 + 1.25 * (-1 / 1.25 + eps)) * X10(-1 / 1.25 + eps))
v.check("X11.10a", A10)
v.check("X11.10b", B10)
nn10 = np.arange(-200, 201)
x10 = np.where(nn10 >= 0, A10 * 0.8 ** np.clip(nn10, 0, None), -B10 * (-1.25) ** np.clip(nn10, None, -1).astype(float))
v.assert_true("two-sided sequence is absolutely summable", np.sum(np.abs(x10)) < 10)
v.assert_true("its z-transform on the unit circle equals X",
              all(abs(np.sum(x10 * np.exp(-1j * w * nn10)) - X10(np.exp(-1j * w))) < 1e-6 for w in (0.2, 1.3, 2.9)))
v.check("X11.10c", x10[nn10 == 0][0])
v.check("X11.10d", x10[nn10 == 2][0])
v.check("X11.10e", x10[nn10 == -1][0])

# 11: simulate the chain: sample, filter, zero-order hold on a fine grid, and measure tones by FFT
fs11, up = 8000, 1024
n11 = np.arange(800)                                    # 0.1 s of samples: 10 Hz FFT bins, tone in bin 100
x11 = np.cos(2 * np.pi * 1000 * n11 / fs11)
y11 = 0.5 * (x11 + np.roll(x11, 1))      # 100 whole cycles: a circular shift is the steady state
v.check("X11.11a", np.abs(np.fft.rfft(y11))[100] / (len(n11) / 2))
v.check("X11.11b", np.sinc(1000 / fs11))
hold = np.repeat(y11, up)          # ZOH output on a fine grid (1024 steps per sample, so the staircase's
Sh = np.abs(np.fft.rfft(hold)) / (len(hold) / 2)        # Dirichlet weighting matches the sinc to 1e-7)
v.check("X11.11c", Sh[100])
img = 101 + np.argmax(Sh[101:2000])
v.check("X11.11d", img * 10 / 1e3)
v.check("X11.11e", db(Sh[img] / Sh[100]))
x9 = np.cos(2 * np.pi * 9000 * n11 / fs11)
v.assert_true("9 kHz and 1 kHz give identical samples", np.allclose(x9, x11))
v.check("X11.11f", np.argmax(np.abs(np.fft.rfft(x9))) * fs11 / len(n11) / 1e3)

# 12
fs12 = 2e6
t12 = np.arange(int(fs12 * 0.01)) / fs12
s12 = (1 + 0.6 * np.cos(2 * np.pi * 3e3 * t12)) * np.cos(2 * np.pi * 300e3 * t12)
P = np.abs(np.fft.rfft(s12)) ** 2
f12 = np.fft.rfftfreq(len(t12), 1 / fs12)
v.check("X11.12a", 100 * P[(np.abs(f12 - 300e3) > 1e3) & (np.abs(f12 - 300e3) < 1e4)].sum() / P.sum())
m = 0.6
tt12 = np.arange(int(4e7 * 3 / 3e3)) / 4e7
env = 1 + m * np.cos(2 * np.pi * 3e3 * tt12)


def worst(RC):
    k = math.exp(-1 / (4e7 * RC))
    vv = np.empty_like(env)
    vv[0] = env[0]
    for i in range(1, len(env)):
        vv[i] = max(env[i], vv[i - 1] * k)
    return np.max(vv - env)


lo, hi = 1e-6, 1e-3
for _ in range(40):
    mid = math.sqrt(lo * hi)
    lo, hi = (mid, hi) if worst(mid) < 1e-7 else (lo, mid)
v.check("X11.12b", lo * 1e6)
v.check("X11.12c", 100 + 2 * 10.7)

# 14
r14 = 1 - (2 * math.pi * 0.1 / 250) / 2
v.check("X11.14a", r14)
v.check("X11.14b", -1 / math.log(r14), rtol=1e-3)
v.check("X11.14c", -1 / math.log(r14) / 250)
v.check("X11.14d", apparent(180, 250, 2500))
v.check("X11.14e", apparent(300, 250, 2500))

sys.exit(v.finish())
