#!/usr/bin/env python3
"""Verify every number in chapter 11-02 (systems and their properties), its solutions and lab.

Independent routes:
- each system is coded as a function of a whole input (a sampled waveform or a sequence) and the properties
  are tested by running it: inputs are combined, scaled and shifted, and the two paths are compared;
- recursions are iterated sample by sample (never summed in closed form), and first-crossing times are found by
  iterating until the condition holds;
- distortion and intermodulation products are read from an FFT of the amplifier's output over a whole number
  of cycles, not from the trigonometric expansion in the text;
- the RC response with an initial condition is integrated numerically (scipy solve_ivp); the LC resonance by
  integrating the ODE and reading the envelope;
- the bipolar transistor's exact harmonic ratio comes from an FFT of exp(x cos theta), checked against the
  modified-Bessel-function identity;
- the noncausal inverse is found by solving its defining recursion backward in time, then summed;
- data-sheet conversions (R-179, R-182, R-185) are arithmetic on the quoted values.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import iv

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("11-02", COURSE / "chapters" / "11-02-system-properties.md",
                        COURSE / "solutions" / "11-02-solutions.md",
                        COURSE / "labs" / "11-02-lab" / "README.md")
rng = np.random.default_rng(20261120)


def db(r):
    return 20 * math.log10(r)


def recursion(a, x, y_init=0.0):
    """y[n] = a y[n-1] + x[n], iterated sample by sample from y[-1] = y_init."""
    y, prev = np.zeros(len(x)), y_init
    for i, xi in enumerate(x):
        prev = a * prev + xi
        y[i] = prev
    return y


def delay(x, k):
    return np.concatenate([np.zeros(k), x[:len(x) - k]]) if k > 0 else x.copy()


# ============================================================ data-sheet conversions (T 11-02)
v.check("T 11-02.a", db(0.000015 / 100))                       # OPA1611 THD+N 0.000015 % [R-182]
v.check("T 11-02.b", 100 * 10 ** (-85 / 20))                    # TLV320AIC3204 ADC THD+N, typ [R-185]
v.check("T 11-02.c", 100 * 10 ** (-70 / 20))                    # max
v.check("T 11-02.d", db(10 / 100))                              # TPA3116D2 rating at 10 % THD+N [R-179]
v.check("T 11-02.e", db(0.1 / 100))                             # 0.1 % at 25 W
v.check("T 11-02.f", 1 / 8e-6 / 1e3)                            # OPA333 zero-corrected every 8 us [R-185]
v.check("T 11-02.g", 0.262 * 500)                               # ADS1292R -3 dB bandwidth 0.262 f_DR [R-185]
v.check("T 11-02.h", db(0.01))

# ============================================================ section 3 claims checked by running the systems
# decimator on the pulse 1, 2, 3, 2, 1 (Figure 1)
pulse = np.array([1, 2, 3, 2, 1, 0, 0, 0, 0, 0], dtype=float)
dec = pulse[::2]
dec_shift = delay(pulse, 1)[::2]
v.assert_true("decimated pulse is 1, 3, 1", list(dec[:3]) == [1, 3, 1] and not dec[3:].any())
v.assert_true("decimating the delayed pulse gives 2, 2 at n = 1, 2",
              list(dec_shift[:4]) == [0, 2, 2, 0] and not dec_shift[4:].any())
v.assert_true("a two-sample delay commutes with a one-sample output delay",
              np.array_equal(delay(pulse, 2)[::2], delay(dec, 1)))
# moving average annihilates a period-5 zero-sum input (section 3.8)
per5 = np.tile([1.0, -1.0, 0.0, 0.0, 0.0], 8)
ma = np.array([per5[n - 2:n + 3].sum() / 5 for n in range(2, len(per5) - 2)])
v.assert_true("the centered moving average maps 1, -1, 0, 0, 0 repeated to zero", np.allclose(ma, 0))

# ============================================================ Example 1: amplifier with offset
T1 = lambda x: 10 * x + 0.05
v.check("Ex 11-02.1a", T1(0.1))
v.check("Ex 11-02.1b", T1(0.2))
v.check("Ex 11-02.1c", T1(0.1) + T1(0.2))
v.check("Ex 11-02.1d", T1(0.3))
v.check("Ex 11-02.1e", T1(0.1) + T1(0.2) - T1(0.3))
v.check("Ex 11-02.1f", 3 * T1(0.1))
v.check("Ex 11-02.1g", 3 * T1(0.1) - T1(0.3))
v.check("Ex 11-02.1h", T1(0.2) - T1(0.1))
xs = np.linspace(-0.3, 0.3, 6001)
v.check("Ex 11-02.1i", np.max(np.abs(T1(xs))))
v.check("Ex 11-02.1j", xs[np.argmin(np.abs(T1(xs) - 2.55))])

# ============================================================ Example 2: time-invariance tests
n = np.arange(-5, 20)
imp = lambda k: (n == k).astype(float)
T2a = lambda x: n * x
out = T2a(imp(3))
v.check("Ex 11-02.2a", out[n == 3][0])
v.check("Ex 11-02.2b", T2a(imp(1))[n == 1][0])                 # delayed output keeps the weight it had at n = 1


def decimate(x_fn, idx):
    return x_fn(2 * idx)


m = np.arange(-5, 10)
d1 = decimate(lambda k: (k == 1).astype(float), m)
v.check("Ex 11-02.2c", float(np.sum(d1 ** 2)))
d2 = decimate(lambda k: (k == 2).astype(float), m)
v.check("Ex 11-02.2d", float(m[np.argmax(d2)]))
fc = 1000.0
mod = lambda x_fn, t: x_fn(t) * math.cos(2 * math.pi * fc * t)
u = lambda t: 1.0 if t >= 0 else 0.0
t0 = 0.25e-3
v.check("Ex 11-02.2e", mod(lambda t: u(t - t0), 1e-3))
v.check("Ex 11-02.2f", mod(u, 1e-3 - t0))

# ============================================================ Example 3: moving average and latency
nn = np.arange(-10, 10)
step = (nn >= 0).astype(float)
ma5 = {int(k): sum(step[(nn == k + j)].sum() for j in range(-2, 3)) / 5 for k in nn[2:-2]}
v.check("Ex 11-02.3a", ma5[-2])
v.check("Ex 11-02.3b", ma5[-1])
v.check("Ex 11-02.3c", ma5[0])
v.assert_true("the centered average responds two samples before the step", ma5[-3] == 0 and ma5[-2] > 0)
lookahead = 2
v.check("Ex 11-02.3d", lookahead)
v.check("Ex 11-02.3e", lookahead / 500 * 1e3)
taps = 101
h_fir = np.hanning(taps + 2)[1:-1]                               # any symmetric filter
centroid = np.sum(np.arange(taps) * h_fir) / np.sum(h_fir)       # symmetric => delay at the middle tap
v.check("Ex 11-02.3f", centroid)
v.check("Ex 11-02.3g", centroid / 48e3 * 1e3)
v.check("Ex 11-02.3h", 3 * (1 / 500) * 1e3)                      # three data periods at 500 SPS [R-185]

# ============================================================ Example 4: recursion stability
v.check("Ex 11-02.4a", 1 / (1 - 0.9))
y9 = recursion(0.9, np.ones(20))
v.check("Ex 11-02.4b", y9[19])
ym9 = recursion(-0.9, np.ones(4000))
v.check("Ex 11-02.4c", ym9[-1])
yalt = recursion(-0.9, (-1.0) ** np.arange(20))
v.check("Ex 11-02.4d", abs(yalt[19]))
v.check("Ex 11-02.4e", abs(recursion(-0.9, (-1.0) ** np.arange(4000))[-1]))
v.check("Ex 11-02.4f", recursion(1.0, np.ones(1000))[999])
sol = solve_ivp(lambda t, y: [1.0 / 1e-3], (0, 1.0), [0.0], rtol=1e-10, atol=1e-10)
v.check("Ex 11-02.4g", sol.y[0, -1])
# worst input found by search for a = -0.9, N = 20: try all sign patterns of the last 12 inputs
best = 0.0
for bits in range(1 << 12):
    x = (-1.0) ** np.arange(20)
    tail = np.array([1.0 if (bits >> i) & 1 else -1.0 for i in range(12)])
    x[8:] = tail
    best = max(best, abs(recursion(-0.9, x)[19]))
v.assert_true("no sign pattern beats the alternating input", best <= abs(yalt[19]) + 1e-12)
v.check("T 11-02.i", abs(recursion(-0.9, (-1.0) ** np.arange(4000))[-1]) / ym9[-1])


# ============================================================ Example 5: distortion by FFT
def amp(x):
    return 10 * x + 0.5 * x ** 2 - 0.2 * x ** 3


def spectrum(x, M):
    Y = np.fft.rfft(x) / M * 2
    Y[0] /= 2
    return np.abs(Y)


M = 4096
tt = np.arange(M) / M
S = spectrum(amp(0.1 * np.cos(2 * np.pi * 8 * tt)), M)
v.check("Ex 11-02.5a", S[0] * 1e3)
v.check("Ex 11-02.5b", S[8])
v.check("Ex 11-02.5c", S[16] * 1e3)
v.check("Ex 11-02.5d", S[24] * 1e3)
v.check("Ex 11-02.5e", db(S[16] / S[8]))
v.check("Ex 11-02.5f", db(S[24] / S[8]))
v.check("Ex 11-02.5g", 100 * math.hypot(S[16], S[24]) / S[8])
M2 = 4000                                                       # bins of 100 Hz: tones at bins 10 and 11
t2 = np.arange(M2) / M2
S2 = spectrum(amp(0.1 * np.cos(2 * np.pi * 10 * t2) + 0.1 * np.cos(2 * np.pi * 11 * t2)), M2)
v.check("Ex 11-02.5h", S2[1] * 1e3)
v.assert_true("IM2 equal at f2 - f1 and f1 + f2", abs(S2[1] - S2[21]) < 1e-12)
v.check("Ex 11-02.5i", 1 * 100.0)
v.check("Ex 11-02.5j", 21 * 0.1)
v.check("Ex 11-02.5k", db(S2[1] / 1.0))
v.check("Ex 11-02.5l", S2[9] * 1e3)
v.assert_true("IM3 equal at 2f1 - f2 and 2f2 - f1", abs(S2[9] - S2[12]) < 1e-12)
v.check("Ex 11-02.5m", 9 * 0.1)
v.check("Ex 11-02.5n", 12 * 0.1)
v.check("Ex 11-02.5o", db(S2[1] / S2[9]))
v.assert_true("no output at frequencies the polynomial cannot create (e.g. 0.5 kHz)", S2[5] < 1e-12)
# guided exercise: 0.3 V
S3 = spectrum(amp(0.3 * np.cos(2 * np.pi * 8 * tt)), M)
hd2_03, hd3_03 = db(S3[16] / S3[8]), db(S3[24] / S3[8])
v.check("T 11-02.j", db(3))                                   # HD2 proportional to A: 20 log10 3
v.assert_true("measured HD2 rise within 0.02 dB of 20 log10 3", abs(hd2_03 - db(S[16] / S[8]) - db(3)) < 0.02)
v.check("T 11-02.k", hd2_03)
v.check("T 11-02.l", hd3_03 - db(S[24] / S[8]))
v.check("T 11-02.m", hd3_03)

# ============================================================ Example 6: RC with initial charge
tau = 1e-3


def rc(vs, y0=1.0, t_end=1e-3):
    s = solve_ivp(lambda t, y: [(vs - y[0]) / tau], (0, t_end), [y0], rtol=1e-11, atol=1e-13)
    return s.y[0, -1]


y2, y4 = rc(2.0), rc(4.0)
v.check("Ex 11-02.6a", y2)
v.check("Ex 11-02.6b", y4)
v.check("Ex 11-02.6c", 2 * y2)
v.check("Ex 11-02.6d", y4 - y2)
v.check("Ex 11-02.6e", rc(0.0))
v.check("Ex 11-02.6f", rc(4.0, y0=0.0))
v.assert_true("zero-state parts are proportional", abs(rc(4.0, y0=0.0) - 2 * rc(2.0, y0=0.0)) < 1e-9)

# ============================================================ Example 7: inverses
h_inv = recursion(-0.5, np.r_[1.0, np.zeros(200)])
v.check("Ex 11-02.7a", np.sum(np.abs(h_inv)))
x_rec = recursion(-0.5, np.r_[1.0, 0.5, np.zeros(20)])
v.assert_true("the b = 0.5 inverse recovers a unit sample exactly", np.allclose(x_rec, np.r_[1.0, np.zeros(21)]))
err = lambda b, k: abs(recursion(-b, np.r_[1e-3, np.zeros(k)])[k])
v.check("Ex 11-02.7b", err(0.5, 10) * 1e6)
v.check("Ex 11-02.7c", err(2.0, 10))
v.check("Ex 11-02.7d", err(2.0, 20))
# noncausal inverse: g[n] + 2 g[n-1] = delta[n], g = 0 for n >= 0, solved backward: g[n-1] = (delta[n] - g[n]) / 2
K = 60
g = {0: 0.0}
for nb_ in range(0, -K, -1):
    g[nb_ - 1] = ((1.0 if nb_ == 0 else 0.0) - g[nb_]) / 2
v.check("Ex 11-02.7e", g[-1])
v.check("Ex 11-02.7f", g[-2])
v.check("Ex 11-02.7g", sum(abs(g[k]) for k in range(-1, -K - 1, -1)))
gseq = np.array([g[k] for k in range(-K, 1)])                   # g[-K] .. g[0]
conv = np.convolve(gseq, [1.0, 2.0])
v.assert_true("g convolved with the channel is a unit sample (up to truncation)",
              abs(conv[K] - 1) < 1e-12 and np.max(np.abs(np.delete(conv, [0, K]))) < 1e-12)

# ============================================================ solutions
v.check("11-02.2a", (1 + 2) ** 2)
v.check("11-02.2b", 1 ** 2 + 2 ** 2)
v.check("11-02.2c", abs(1 + (-1)))
v.check("11-02.2d", abs(1) + abs(-1))
qround = lambda x: math.floor(x + 0.5)
v.check("11-02.2e", qround(0.4) + qround(0.4))
v.check("11-02.2f", qround(0.8))
# 3(b): time reversal of p(t - 2) and the delayed output, supports read from a grid
tg = np.linspace(-5, 5, 100001)
p = lambda t: ((t > 0) & (t < 1)).astype(float)
s1 = tg[p(-tg - 2) > 0]
s2 = tg[p(-(tg - 2)) > 0]
v.check("11-02.3a", s1.min())
v.check("11-02.3b", s1.max())
v.check("11-02.3c", s2.min())
v.check("11-02.3d", s2.max())
ug = lambda t: (t >= 0).astype(float)
v.check("11-02.3e", tg[(ug(tg - 2 + 1) * ug(tg - 2)) > 0].min())
v.check("11-02.3f", tg[(ug(tg - 1) * ug(tg)) > 0].min())
nd = np.arange(-3, 6)
alt = lambda x: ((-1.0) ** nd) * x
v.check("11-02.3g", alt((nd == 0).astype(float))[nd == 0][0])
v.check("11-02.3h", alt((nd == 1).astype(float))[nd == 1][0])
xb = np.linspace(-3, 3, 60001)
v.check("11-02.4a", np.max(xb ** 2))
v.check("11-02.4b", np.max(np.exp(xb)))
v.check("11-02.4c", np.max(np.abs(np.convolve(3 * np.ones(30), np.ones(5)))))
tq = np.linspace(-50, 50, 200001)
v.check("11-02.4d", np.max(np.abs(3 / (1 + tq ** 2))))
v.check("11-02.5a", np.sum(np.abs(recursion(0.5, np.r_[1.0, np.zeros(200)]))))
w5 = recursion(-1.0, (-1.0) ** np.arange(10))
v.check("11-02.5b", abs(w5[9]))
v.assert_true("w[0..2] = 1, -2, 3", list(w5[:3]) == [1.0, -2.0, 3.0])
# 6: bipolar distortion; exact ratio from an FFT of exp(x cos theta)
VT = 0.025852
th = 2 * np.pi * np.arange(4096) / 4096


def hd_exact(A):
    E = np.abs(np.fft.rfft(np.exp(A / VT * np.cos(th))))
    return E[2] / E[1], E[3] / E[1]


hd2_1, hd3_1 = hd_exact(1e-3)
hd2_5, hd3_5 = hd_exact(5e-3)
v.check("11-02.6a", 100 * 1e-3 / (4 * VT))
v.check("11-02.6b", 100 * (1e-3 / VT) ** 2 / 24)
v.check("11-02.6c", 100 * 5e-3 / (4 * VT))
v.check("11-02.6d", 100 * (5e-3 / VT) ** 2 / 24)
v.assert_true("Taylor HD3 within 0.3 % of exact at 5 mV", abs((5e-3 / VT) ** 2 / 24 / hd3_5 - 1) < 3e-3)
from scipy.optimize import brentq  # noqa: E402
v.check("11-02.6e", brentq(lambda A: A / (4 * VT) - 0.01, 1e-5, 1e-2) * 1e3)
v.check("11-02.6f", 100 * hd2_5)
v.assert_true("FFT ratio matches I2/I1", abs(hd2_5 - iv(2, 5e-3 / VT) / iv(1, 5e-3 / VT)) < 1e-12)
v.check("11-02.6g", 5e-3 / VT)
v.check("11-02.6h", 100 * ((5e-3 / (4 * VT)) / hd2_5 - 1))
v.check("11-02.8a", 2 * 3 ** 2)
v.check("11-02.8b", (2 * 3) ** 2)
xr = np.arange(0, 30, dtype=float)
dec_then_delay = lambda k: xr[2 * (k - 1)]
delay_then_dec = lambda k: delay(xr, 1)[2 * k]
v.check("11-02.8c", dec_then_delay(3))
v.check("11-02.8d", delay_then_dec(3))
xr2 = rng.normal(size=40)
v.assert_true("gain and delay commute", np.allclose(3 * delay(xr2, 2), delay(3 * xr2, 2)))
y_a = recursion(1.0, np.ones(4), y_init=5.0)
y_b = recursion(1.0, 2 * np.ones(4), y_init=5.0)
v.check("11-02.9a", y_a[3])
v.check("11-02.9b", y_b[3])
v.check("11-02.9c", 2 * y_a[3])
v.check("11-02.9d", recursion(1.0, np.zeros(4), y_init=5.0)[3])
# 10: LC resonance by ODE
L_, C_ = 1e-3, 1e-6
w0 = 1 / math.sqrt(L_ * C_)
v.check("11-02.10a", w0 / 1e3)
v.check("11-02.10b", w0 / (2 * math.pi) / 1e3)


def lc_env(t_end, R=0.0):
    rhs = lambda t, y: [y[1], (math.cos(w0 * t) - y[0] - R * C_ * y[1]) / (L_ * C_)]
    s = solve_ivp(rhs, (0, t_end), [0.0, 0.0], max_step=2 * math.pi / w0 / 60, rtol=1e-10, atol=1e-12,
                  dense_output=True)
    tt_ = np.linspace(t_end - 2 * math.pi / w0, t_end, 4001)
    return s, np.max(np.abs(s.sol(tt_)[0]))


s_lc, env1 = lc_env(1e-3)
v.assert_true("the ODE solution matches w0 t sin(w0 t)/2 throughout",
              all(abs(s_lc.sol(t)[0] - 0.5 * w0 * t * math.sin(w0 * t)) < 1e-4 for t in np.linspace(0, 1e-3, 201)))
v.check("11-02.10c", s_lc.sol(1e-3)[0] / math.sin(w0 * 1e-3))  # amplitude coefficient at 1 ms from the ODE
v.check("11-02.10d", 0.5 * w0 * 1e-2)
v.assert_true("ODE envelope at 10 ms", abs(lc_env(1e-2)[1] - 0.5 * w0 * 1e-2) < 0.5)
Q = math.sqrt(L_ / C_) / 1.0
v.check("11-02.10e", Q)
_, env_r = lc_env(60e-3, R=1.0)                                  # many time constants 2L/R = 2 ms
v.check("11-02.10f", env_r)
period = 8e-6
s_ch = lambda t: 1.0 if (t % period) < period / 2 else -1.0
v.check("11-02.11a", u(5e-6 - 4e-6) * s_ch(5e-6 - 4e-6))
v.check("11-02.11b", u(5e-6 - 4e-6) * s_ch(5e-6))
v.check("11-02.11c", 1 / period / 1e3)
v.assert_true("chopping twice restores the input",
              all(abs(s_ch(t) * s_ch(t) - 1) < 1e-15 for t in np.linspace(0, 3e-5, 301)))
v.check("11-02.12a", 1 / (1 - 0.99))
y99 = recursion(0.99, np.ones(2000))
first = int(np.argmax(y99 >= 99))
v.check("11-02.12b", first)
v.check("11-02.12c", first / 1e3)
v.check("11-02.12d", math.log(0.01) / math.log(0.99))
v.check("11-02.12e", y99[457])
v.check("11-02.12f", y99[458])
budget = 2e-3 * 48e3
v.check("11-02.13a", budget)
ntaps = max(N for N in range(1, 400, 2) if (N - 1) / 2 <= budget - 40)
v.check("11-02.13b", ntaps)
v.check("11-02.13c", 10e-3 * 48e3)
v.check("11-02.14a", 0.5 / 0.010)
v.check("11-02.14b", 0.5 / 0.020)

# ============================================================ lab
lib = {
    "S1": lambda x: 10 * x + 0.05,
    "S2": lambda x: delay(x, 2),
    "S4": lambda x: np.cumsum(x),
    "S5": lambda x: np.array([x[max(0, k - 2):k + 3].sum() / 5 for k in range(len(x))]),
    "S6": lambda x: x ** 2,
    "S7": lambda x: x * np.cos(0.3 * np.pi * np.arange(len(x))),
    "S8": lambda x: np.concatenate([x[::2], np.zeros(len(x) - len(x[::2]))]),
    "S10": lambda x: recursion(0.8, x),
}
NL = 64


def lin_ok(T):
    for _ in range(10):
        x1, x2 = rng.normal(size=NL), rng.normal(size=NL)
        a, b = rng.normal(size=2)
        if not np.allclose(T(a * x1 + b * x2), a * T(x1) + b * T(x2)):
            return False
    return True


def ti_ok(T):
    for _ in range(10):
        x = np.r_[rng.normal(size=NL // 2), np.zeros(NL // 2)]
        k = int(rng.integers(1, 6))
        if not np.allclose(T(delay(x, k))[k:], T(x)[:NL - k]):
            return False
    return True


def causal_ok(T):
    for _ in range(10):
        x = rng.normal(size=NL)
        n1 = int(rng.integers(5, NL - 5))
        x2 = x.copy()
        x2[n1:] += 1.0
        if not np.allclose(T(x)[:n1], T(x2)[:n1]):
            return False
    return True


v.check("Lab 11-02.a", sum(not lin_ok(T) for T in lib.values()))
v.check("Lab 11-02.b", sum(not ti_ok(T) for T in lib.values()))
v.check("Lab 11-02.c", sum(not causal_ok(T) for T in lib.values()))
worst = np.array([np.sign((-0.8) ** (29 - mm)) for mm in range(30)])
v.check("Lab 11-02.d", abs(recursion(-0.8, worst)[-1]))
v.check("Lab 11-02.e", recursion(-0.8, np.ones(3000))[-1])
v.check("Lab 11-02.f", hd2_03)
v.check("Lab 11-02.g", hd3_03)
S01 = spectrum(amp(0.01 * np.cos(2 * np.pi * 8 * tt)), M)
v.check("Lab 11-02.h", db(S[16] / S[8]) - db(S01[16] / S01[8]))
v.check("Lab 11-02.i", db(S[24] / S[8]) - db(S01[24] / S01[8]))
v.check("Lab 11-02.j", next(k for k in range(100) if err(2.0, k) > 1.0))
Kt = 8
gt = np.array([g[-k] for k in range(Kt, 0, -1)])
casc = np.convolve(gt, [1.0, 2.0])
v.check("Lab 11-02.k", np.max(np.abs(np.delete(casc, np.argmax(np.abs(casc))))))
v.check("Lab 11-02.l", abs(recursion(-0.8, worst)[-1]) / recursion(-0.8, np.ones(3000))[-1])

sys.exit(v.finish())
