#!/usr/bin/env python3
"""Verify chapter 16-08 (filter structures and implementation): examples, text, problems and lab answers.

Routes:
- every structure in labs/16-08-lab/structures.py against scipy.signal.lfilter / numpy.convolve;
- peak gains with freqz on a fine grid, L1 and L2 norms from impulse responses computed by lfilter;
- pole positions after rounding by numpy.roots, coupled-form poles from the quantized (c, s) pair;
- reflection coefficients by an independent Schur-Cohn step-down written here, checked by root magnitudes;
- the fixed-point biquad: an independent integer re-implementation here, the committed vectors.hex regenerated and
  compared, and saturation of both signs confirmed.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "16-08-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import structures as st  # noqa: E402
import make_vectors as mv  # noqa: E402

CH = ROOT / "chapters" / "16-08-filter-structures.md"
v = Verifier.from_files("16-08", CH, ROOT / "solutions" / "16-08-solutions.md", LAB / "README.md")
PI = math.pi
W = np.linspace(0, PI, 400001)

# ---------------------------------------------------------------------------------------- structures agree
rng = np.random.default_rng(16)
x = rng.standard_normal(1500)
b, a = signal.ellip(4, 0.5, 40, 0.3)
ref = signal.lfilter(b, a, x)
v.assert_true("DF I, DF II, DF2T and cascade equal lfilter",
              all(np.max(np.abs(y - ref)) < 1e-10 for y in (st.df1(b, a, x), st.df2(b, a, x)[0], st.df2t(b, a, x)[0],
                                                             st.sos_filter(signal.tf2sos(b, a), x))))
h = rng.standard_normal(12)
v.assert_true("direct and transposed FIR equal convolution",
              np.allclose(st.fir_direct(h, x[:200]), np.convolve(h, x[:200])[:200])
              and np.allclose(st.fir_transposed(h, x[:200]), np.convolve(h, x[:200])[:200]))

# ---------------------------------------------------------------------------------------- Example 1 and Problem 1


def cost(structure, N):
    if structure == "df1":
        return 2 * N + 1, 2 * N, 2 * N
    if structure == "df2":
        return 2 * N + 1, 2 * N, N
    return 5 * (N // 2), 4 * (N // 2), 2 * (N // 2)


v.check("Ex 16-08.1a", cost("df1", 4)[0])
v.check("Ex 16-08.1b", cost("df1", 4)[1])
v.check("Ex 16-08.1c", cost("df1", 4)[2])
v.check("Ex 16-08.1d", cost("df2", 4)[2])
v.check("Ex 16-08.1e", cost("cascade", 4)[0])
v.assert_true("lab counts agree", st.counts("df1", 4) == cost("df1", 4) and st.counts("cascade", 6) == cost("cascade", 6))
v.check("16-08.1a", cost("df1", 6)[0])
v.check("16-08.1b", cost("df1", 6)[2])
v.check("16-08.1c", cost("df2", 6)[2])
v.check("16-08.1d", cost("cascade", 6)[0])
v.check("16-08.1e", cost("df2", 6)[1])

# ---------------------------------------------------------------------------------------- Example 2 and Problem 4
for taps, kp, kf in ((8, "Ex 16-08.2a", "Ex 16-08.2b"), (64, "Ex 16-08.2c", "Ex 16-08.2d")):
    T = 2.0 + (taps - 1) * 0.5
    v.check(kp, T)
    v.check(kf, 1000 / T)
v.check("Ex 16-08.2e", 2.0 + math.log2(64) * 0.5)
v.check("Ex 16-08.2f", 1000 / (2.0 + math.log2(64) * 0.5))
v.check("Ex 16-08.2g", 2.0 + 0.5)
v.check("Ex 16-08.2i", 2.0 + math.log2(8) * 0.5)
v.check("Ex 16-08.2j", 1000 / (2.0 + math.log2(8) * 0.5))
v.check("Ex 16-08.2h", 1000 / 2.5)
v.check("16-08.4a", 1.5 + 31 * 0.4)
v.check("16-08.4b", 1000 / (1.5 + 31 * 0.4))
v.check("16-08.4c", 1.5 + math.log2(32) * 0.4)
v.check("16-08.4d", 1000 / (1.5 + math.log2(32) * 0.4))
v.check("16-08.4e", 1.5 + 0.4)
v.check("16-08.4f", 1000 / (1.5 + 0.4))

# ---------------------------------------------------------------------------------------- Example 3, Problems 10-12
sos = signal.ellip(8, 0.1, 60, 4000, fs=48000, output="sos")
sec = sos[3]
_, HA = signal.freqz([1], sec[3:], worN=W)
_, HS = signal.freqz(sec[:3], sec[3:], worN=W)
g = signal.lfilter([1], sec[3:], np.r_[1.0, np.zeros(40000)])
v.check("Ex 16-08.3a", np.abs(HA).max())
v.check("Ex 16-08.3b", math.log2(np.abs(HA).max()))
v.check("Ex 16-08.3e", 20 * math.log10(np.abs(HA).max()))
v.check("Ex 16-08.3c", float(np.sum(np.abs(g))))
v.check("Ex 16-08.3d", np.abs(HS).max())
v.check("16-08.12a", float(np.sum(g * g)))
v.check("16-08.12b", 10 * math.log10(float(np.sum(g * g))))
ipk = int(np.argmax(np.abs(HA)))
v.check("Lab 16-08.b", np.abs(HA)[ipk])
v.check("Lab 16-08.c", np.abs(HS)[ipk])


def cum_peaks(S):
    out, H = [], np.ones_like(W, dtype=complex)
    for s_ in S:
        _, Hs = signal.freqz(s_[:3], s_[3:], worN=W)
        H = H * Hs
        out.append(float(np.abs(H).max()))
    return out


pf, pr = cum_peaks(sos), cum_peaks(sos[::-1])
for key, val in zip(("16-08.10a", "16-08.10b", "16-08.10c"), pf[:3]):
    v.check(key, val)
for key, val in zip(("16-08.10d", "16-08.10e", "16-08.10f"), pr[:3]):
    v.check(key, val)
v.check("16-08.10g", math.ceil(math.log2(max(pr))))
for key, val in zip(("Txt 16-08.a", "Txt 16-08.b", "Txt 16-08.c"), pr[:3]):
    v.check(key, 20 * math.log10(val))
v.assert_true("SciPy ordering never exceeds unity at an intermediate node", max(pf) <= 1 + 1e-9)
v.check("Txt 16-08.d", 32 + math.ceil(math.log2(5)))

# ---------------------------------------------------------------------------------------- Example 4 and Problem 9
fs = 48000


def q(val, B):
    return np.round(val * 2.0 ** B) / 2.0 ** B


def realized(f0, r, B):
    th = 2 * PI * f0 / fs
    p = np.roots([1, q(-2 * r * math.cos(th), B), q(r * r, B)])
    fdir = abs(np.angle(p[0])) * fs / (2 * PI)
    fcou = math.atan2(q(r * math.sin(th), B), q(r * math.cos(th), B)) * fs / (2 * PI)
    return fdir, fcou


th = 2 * PI * 100 / fs
v.check("Ex 16-08.4f", th)
v.check("Ex 16-08.4g", -2 * 0.999 * math.cos(th))
v.check("Ex 16-08.4h", 0.999 * math.sin(th))
d12, c12 = realized(100, 0.999, 12)
d16, c16 = realized(100, 0.999, 16)
v.check("Ex 16-08.4a", d12)
v.check("Ex 16-08.4b", c12)
v.check("Ex 16-08.4c", d16)
v.check("Ex 16-08.4d", c16)
v.check("Ex 16-08.4i", 100 * (d12 / 100 - 1))
v.check("Ex 16-08.4l", 100 * (1 - d16 / 100))
v.check("Ex 16-08.4e", 1 / (2 * 0.999 * math.sin(th)))
v.check("Ex 16-08.4j", 2.0 ** -12 / (2 * 0.999 * math.sin(th)) * fs / (2 * PI))
v.check("Ex 16-08.4k", 2.0 ** -13 * math.cos(th) / 0.999 * fs / (2 * PI))
d14, c14 = realized(50, 0.9995, 14)
v.check("16-08.9a", d14)
v.check("16-08.9b", c14)

# ---------------------------------------------------------------------------------------- lattices


def step_down(acoef):
    """Schur-Cohn step-down, written independently: returns k_1..k_N."""
    cur = list(map(float, acoef))
    ks = []
    while len(cur) > 1:
        km = cur[-1]
        ks.append(km)
        rev = cur[::-1]
        cur = [(c - km * rv) / (1 - km * km) for c, rv in zip(cur, rev)][:-1]
    return ks[::-1]


k3 = step_down([1, -0.9, 0.64, -0.576])
v.check("Ex 16-08.5a", k3[2])
v.check("Ex 16-08.5b", k3[1])
v.check("Ex 16-08.5c", k3[0])
v.check("Ex 16-08.5d", (-0.9 - k3[2] * 0.64) / (1 - k3[2] ** 2))
v.assert_true("lab lattice conversion agrees and round-trips",
              np.allclose(st.poly_to_lattice([1, -0.9, 0.64, -0.576]), k3)
              and np.allclose(st.lattice_to_poly(k3), [1, -0.9, 0.64, -0.576]))
v.assert_true("stable: roots 0.9 and ±0.8j", np.allclose(np.sort(np.abs(np.roots([1, -0.9, 0.64, -0.576]))), [0.8, 0.8, 0.9]))
b2, a2 = signal.butter(2, 1000, fs=8000)
kb = step_down(a2)
v.check("Ex 16-08.5e", kb[0])
v.check("Ex 16-08.5f", kb[1])
v.check("16-08.7a", step_down([1, 0.5, 0.9])[0])
v.assert_true("(b) has k2 = 1.2 > 1", abs(step_down([1, -1.8, 1.2])[1] - 1.2) < 1e-12)
v.check("16-08.7b", float(np.max(np.abs(np.roots([1, -1.8, 1.2])))))
A4 = np.polymul(sos[2][3:], sos[3][3:])
k4 = step_down(A4)
for key, val in zip(("16-08.11d", "16-08.11c", "16-08.11b", "16-08.11a"), k4):
    v.check(key, val)
v.assert_true("all |k| < 1 and roots inside", max(abs(kk) for kk in k4) < 1 and np.max(np.abs(np.roots(A4))) < 1)

# ---------------------------------------------------------------------------------------- Problems 2, 3, 5, 6
y2 = st.fir_transposed([1, -1, 0.5], [1, 2, 3, 0, 0])
v.assert_true("transposed outputs equal convolution", np.allclose(y2, np.convolve([1, -1, 0.5], [1, 2, 3])))
for key, i in (("16-08.2a", 1), ("16-08.2b", 2), ("16-08.2c", 3), ("16-08.2d", 4)):
    v.check(key, y2[i])
h3 = signal.lfilter([1, 1], [1, -0.5], [1, 0, 0, 0])
v.assert_true("lab DF II gives the same impulse response", np.allclose(st.df2([1, 1], [1, -0.5], [1, 0, 0, 0])[0], h3))
for key, i in (("16-08.3a", 1), ("16-08.3b", 2), ("16-08.3c", 3)):
    v.check(key, h3[i])
_, H5 = signal.freqz([1], [1, -0.95, 0.9025], worN=W)
m5 = float(np.abs(H5).max())
v.check("16-08.5a", m5)
v.check("16-08.5b", W[np.argmax(np.abs(H5))] / PI)
v.check("16-08.5c", math.log2(m5))
v.check("16-08.5d", math.ceil(math.log2(m5)))
v.check("16-08.6a", 1 / (2 * 0.99 * math.sin(PI / 2)))
v.check("16-08.6b", 1 / (2 * 0.99 * math.sin(0.01)))

# ---------------------------------------------------------------------------------------- fixed point


def biquad_int(xs, coef):
    """Independent integer model: exact sum, round half up, saturate, feed back the saturated value."""
    b0, b1, b2_, a1, a2_ = coef
    xh, yh, out, nsat = [0, 0], [0, 0], [], [0, 0]
    for xn in xs:
        acc = b0 * xn + b1 * xh[0] + b2_ * xh[1] - a1 * yh[0] - a2_ * yh[1]
        yn = math.floor((acc + 8192) / 16384)
        if yn > 32767:
            yn, nsat[0] = 32767, nsat[0] + 1
        elif yn < -32768:
            yn, nsat[1] = -32768, nsat[1] + 1
        xh, yh = [xn, xh[0]], [yn, yh[0]]
        out.append(yn)
    return out, nsat


coef = tuple(int(round(c * 16384)) for c in (b2[0], b2[1], b2[2], a2[1], a2[2]))
v.assert_true("Q2.14 coefficients are (1600, 3199, 1600, -15447, 5461)", coef == (1600, 3199, 1600, -15447, 5461) == mv.COEF)
v.check("16-08.8a", sum(coef[:3]) / (16384 + coef[3] + coef[4]))
v.check("16-08.8b", float(np.max(signal.lfilter(b2, a2, [32000.0] * 200))))
ys, ns = biquad_int([32000] * 200, coef)
v.check("16-08.8c", ns[0])
v.check("16-08.8d", ys[-1])
lines, sat = mv.build()
v.assert_true("vectors.hex is the current model output", (LAB / "vectors.hex").read_text().split() == lines)
tot = [0, 0]
match = True
for xs in mv.tests:
    yi, nsi = biquad_int(xs, coef)
    match &= yi == st.biquad_df1_fixed(xs, coef)[0]
    tot = [tot[0] + nsi[0], tot[1] + nsi[1]]
v.assert_true("independent integer model equals the lab's bit-exact model", match)
v.assert_true("vectors saturate in both directions", tot[0] >= 1 and tot[1] >= 1)
v.check("Lab 16-08.a", tot[0] + tot[1])


def trunc_model(xs, c):
    b0, b1, b2_, a1, a2_ = c
    xh, yh, out = [0, 0], [0, 0], []
    for xn in xs:
        acc = b0 * xn + b1 * xh[0] + b2_ * xh[1] - a1 * yh[0] - a2_ * yh[1]
        yn = max(-32768, min(32767, math.floor(acc / 16384)))
        xh, yh = [xn, xh[0]], [yn, yh[0]]
        out.append(yn)
    return out


v.check("Lab 16-08.d", sum(sum(u != w_ for u, w_ in zip(biquad_int(xs, coef)[0], trunc_model(xs, coef))) for xs in mv.tests))

# lattice stage equations (§3.5) and DF2T (§3.2), checked against direct filtering
_rng = np.random.default_rng(1608)
_kk = [0.5, -0.3, 0.2, 0.6]
_A = st.lattice_to_poly(_kk)
_x = _rng.standard_normal(300)


def _fir_lattice(k, x):
    g_prev = np.zeros(len(k))
    y = np.zeros(len(x))
    for n, xn in enumerate(x):
        f, g = xn, xn
        gs = [g]
        for m, km in enumerate(k):
            f, g = f + km * g_prev[m], km * f + g_prev[m]
            gs.append(g)
        g_prev = np.array(gs[:-1])
        y[n] = f
    return y


def _allpole_lattice(k, x):
    N = len(k)
    g_prev = np.zeros(N)  # g_{m-1}[n-1], m = 1..N
    y = np.zeros(len(x))
    for n, xn in enumerate(x):
        f = xn
        fs_ = [0.0] * (N + 1)
        fs_[N] = f
        for m in range(N, 0, -1):
            fs_[m - 1] = fs_[m] - k[m - 1] * g_prev[m - 1]
        g = [fs_[0]] + [0.0] * N
        for m in range(1, N + 1):
            g[m] = k[m - 1] * fs_[m - 1] + g_prev[m - 1]
        g_prev = np.array(g[:N])
        y[n] = fs_[0]
    return y


v.assert_true("FIR lattice stage equations realize A_N(z)", np.allclose(_fir_lattice(_kk, _x), signal.lfilter(_A, [1.0], _x)))
v.assert_true("all-pole lattice realizes 1/A_N(z)", np.allclose(_allpole_lattice(_kk, _x), signal.lfilter([1.0], _A, _x)))
_b, _a = [0.2, 0.3, 0.1], [1.0, -0.5, 0.3]
s1 = s2 = 0.0
_y = []
for xn in _x:
    yn = _b[0] * xn + s1
    s1, s2 = _b[1] * xn - _a[1] * yn + s2, _b[2] * xn - _a[2] * yn
    _y.append(yn)
v.assert_true("DF2T equations realize B/A", np.allclose(_y, signal.lfilter(_b, _a, _x)))

sys.exit(v.finish())
