#!/usr/bin/env python3
"""Verify chapter 16-10 (quantization and fixed point): examples, text, problems and lab answers.

Routes:
- formats, bounds and SQNR formulas recomputed from their definitions;
- SQNR, dither and harmonic results by independent simulation written here (numpy rounding, FFTs);
- clipping noise by numerical integration of the Gaussian tail (scipy.integrate.quad), not the closed form;
- noise gains and norms from impulse responses computed with scipy.signal.lfilter;
- coefficient quantization by rounding with numpy and measuring with scipy.signal.freqz;
- limit cycles by an integer recursion written here;
- floating-point rounding with numpy.float16 for binary16 and an independent bit-level encoder for E4M3, E5M2 and
  bfloat16 (constructed from the bit fields, then searched for the nearest representable value).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, signal
from scipy.optimize import minimize_scalar
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "16-10-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
sys.path.insert(0, str(ROOT / "labs" / "16-06-lab"))
from eeverify import Verifier  # noqa: E402
import quant as q  # noqa: E402
import firdesign as fd  # noqa: E402

CH = ROOT / "chapters" / "16-10-quantization-and-fixed-point.md"
v = Verifier.from_files("16-10", CH, ROOT / "solutions" / "16-10-solutions.md", LAB / "README.md")


def rnd(x, F):
    return np.floor(np.asarray(x) * 2.0**F + 0.5) / 2.0**F


# ---------------------------------------------------------------------------------------- Example 1
D15 = 2.0**-15
v.check("Ex 16-10.1d", D15)
v.check("Ex 16-10.1a", float(rnd(-0.3, 15)) + 0.3)
v.check("Ex 16-10.1b", math.floor(-0.3 / D15) * D15 + 0.3)
v.check("Ex 16-10.1c", -D15 / 2)
v.assert_true("lab quantizer agrees", abs(q.quantize(-0.3, 15) - rnd(-0.3, 15)) < 1e-15
              and abs(q.quantize(-0.3, 15, "floor") - math.floor(-0.3 / D15) * D15) < 1e-15)

# ---------------------------------------------------------------------------------------- Example 2 and text
v.check("Txt 16-10.a", 20 * math.log10(2))
v.check("Ex 16-10.2a", 10 * math.log10(1.5 * 2**24))
v.check("Txt 16-10.b", 10 * math.log10(1.5 * 2**32))


def sim_sine(B, N=65536, cycles=4093):
    n = np.arange(N)
    amp = (2 ** (B - 1) - 1) / 2 ** (B - 1)
    x = amp * np.sin(2 * np.pi * cycles * n / N + 0.1)
    xq = np.clip(rnd(x, B - 1), -1, 1 - 2.0 ** (1 - B))
    return 10 * math.log10(np.mean(x**2) / np.mean((x - xq) ** 2))


v.check("Ex 16-10.2b", sim_sine(12))
v.check("Ex 16-10.2c", 10 * math.log10(3 * 4**12 / 16))


def clip_noise(L):
    s = 1 / L
    val, _ = integrate.quad(lambda x: (x - 1) ** 2 * norm.pdf(x, scale=s), 1, np.inf)
    return 2 * val


def sqnr_tot(L, B):
    s = 1 / L
    D = 2.0 ** (1 - B)
    return 10 * math.log10(s * s / (D * D / 12 + clip_noise(L)))


v.check("Ex 16-10.2j", clip_noise(4))
v.check("Ex 16-10.2k", (2.0**-11) ** 2 / 12)
v.check("Ex 16-10.2d", sqnr_tot(4, 12))
rng = np.random.default_rng(10)
g = rng.standard_normal(1_000_000) / 4
gq = np.clip(rnd(g, 11), -1, 1 - 2.0**-11)
v.check("Ex 16-10.2e", 10 * math.log10(np.mean(g**2) / np.mean((g - gq) ** 2)))
v.check("Lab 16-10.c", q.gaussian_sqnr(12, 4.0))
for B, kl, ks in ((12, "Ex 16-10.2f", "Ex 16-10.2g"), (16, "Ex 16-10.2h", "Ex 16-10.2i")):
    r = minimize_scalar(lambda L: -sqnr_tot(L, B), bounds=(3, 8), method="bounded", options={"xatol": 1e-6})
    v.check(kl, r.x)
    v.check(ks, -r.fun)
v.check("16-10.5a", 10 * math.log10(3 * 4**16 / 16))
v.check("16-10.5b", sqnr_tot(4, 16))
from scipy.stats import norm as _norm  # noqa: E402
v.check("16-10.5c", 2 * ((1 + 16) * _norm.sf(4) - 4 * _norm.pdf(4)))

# ---------------------------------------------------------------------------------------- Example 3
N, k0 = 4096, 67
x = 1.5 * np.sin(2 * np.pi * k0 * np.arange(N) / N + 0.3)
xq = np.floor(x + 0.5)
X = np.abs(np.fft.rfft(xq))
for h, key in ((3, "Ex 16-10.3a"), (5, "Ex 16-10.3b"), (7, "Ex 16-10.3c")):
    v.check(key, 20 * math.log10(X[h * k0] / X[k0]))
v.check("Ex 16-10.3d", float(np.var(xq - x)))
rng = np.random.default_rng(5)
d = rng.uniform(-0.5, 0.5, N) + rng.uniform(-0.5, 0.5, N)
xd = np.floor(x + d + 0.5)
v.check("Ex 16-10.3e", float(np.var(xd - x)))
Xd = np.abs(np.fft.rfft(xd))
v.assert_true("dithered harmonic bins all below -30 dBc", max(Xd[h * k0] / Xd[k0] for h in range(2, 8)) < 10 ** (-30 / 20))
_floor = 10 * math.log10(np.mean(np.delete(Xd[1:], [k0 - 1]) ** 2) / Xd[k0] ** 2)
v.assert_true("dithered floor is about -40 dBc per bin on average", -42 < _floor < -38, f"{_floor:.2f}")
v.check("Txt 16-10.d", 10 * math.log10(3))

# ---------------------------------------------------------------------------------------- noise gains (text, Problems 6, 7, 10)


def impulse(b, a, n=200000):
    return signal.lfilter(b, a, np.r_[1.0, np.zeros(n - 1)])


sos = signal.ellip(8, 0.1, 60, 4000, fs=48000, output="sos")
ng = float(np.sum(impulse([1], sos[3][3:]) ** 2))
v.check("Txt 16-10.c", ng)
v.check("Txt 16-10.e", 0.5 * math.log2(ng))
for a_, kg, kd in ((0.9, "16-10.6a", "16-10.6b"), (0.99, "16-10.6c", "16-10.6d")):
    gg = float(np.sum(impulse([1], [1, -a_]) ** 2))
    v.check(kg, gg)
    v.check(kd, 10 * math.log10(gg))
v.assert_true("noise gain equals 1/(1 - a^2)", abs(float(np.sum(impulse([1], [1, -0.99]) ** 2)) - 1 / (1 - 0.99**2)) < 1e-6)
v.check("16-10.6e", 0.5 * math.log2(1 / (1 - 0.99**2)))
v.check("16-10.6f", math.ceil(0.5 * math.log2(1 / (1 - 0.99**2))))
v.check("16-10.7a", 10 * math.log10(64))
hr = impulse([1], [1, -0.95, 0.9025])
_, Hr = signal.freqz([1], [1, -0.95, 0.9025], worN=400001)
L1, Linf, L2 = float(np.sum(np.abs(hr))), float(np.max(np.abs(Hr))), float(math.sqrt(np.sum(hr**2)))
v.check("16-10.10a", L1)
v.check("16-10.10b", Linf)
v.check("16-10.10c", L2)
v.check("16-10.10d", math.ceil(math.log2(L1)))
v.check("16-10.10f", math.ceil(math.log2(Linf)))
v.check("16-10.10e", math.ceil(math.log2(L2)))

# ---------------------------------------------------------------------------------------- Example 4 and Problem 8
fs = 48000
wp, ws = 2 * np.pi * 4000 / fs, 2 * np.pi * 5000 / fs
dp, ds = fd.deltas(0.1, 60)
h = fd.remez_lowpass(137, wp, ws, dp, ds)
v.check("Ex 16-10.4a", float(np.max(np.abs(h))))


def atten(hh):
    _, Hs = signal.freqz(hh, worN=np.linspace(ws, np.pi, 20000))
    return -20 * math.log10(np.max(np.abs(Hs)))


def meets(hh):
    _, Hp = signal.freqz(hh, worN=np.linspace(0, wp, 20000))
    _, Hs = signal.freqz(hh, worN=np.linspace(ws, np.pi, 20000))
    return np.max(np.abs(np.abs(Hp) - 1)) <= dp and np.max(np.abs(Hs)) <= ds


for F, key in ((12, "Ex 16-10.4b"), (14, "Ex 16-10.4c"), (16, "Ex 16-10.4d"), (17, "Ex 16-10.4e"), (18, "Ex 16-10.4f")):
    v.check(key, atten(rnd(h, F)))
v.check("Ex 16-10.4g", min(F for F in range(10, 24) if meets(rnd(h, F))))
v.check("Ex 16-10.4h", 20 * math.log10(math.sqrt(137) * 2.0**-14 / math.sqrt(12)))
dpp, dss = fd.deltas(0.08, 66)
nm, hm = fd.min_taps(lambda n_: fd.remez_lowpass(n_, wp, ws, dpp, dss), wp, ws, dpp, dss, 140, 170)
v.check("Ex 16-10.4i", nm)
v.check("Ex 16-10.4j", min(F for F in range(10, 24) if meets(rnd(hm, F))))
v.check("Ex 16-10.4k", atten(rnd(hm, 14)))
v.check("16-10.8a", 20 * math.log10(math.sqrt(101) * 2.0**-12 / math.sqrt(12)))
v.check("16-10.8b", 20 * math.log10(101 * 2.0**-13))
v.check("16-10.8c", math.sqrt(101) * 2.0**-12 / math.sqrt(12))
v.check("16-10.8d", 101 * 2.0**-13)

# ---------------------------------------------------------------------------------------- Example 5 and Problem 9


def first_order(a, y, mode, n=3000):
    for _ in range(n):
        val = a * y
        y = math.floor(val + 0.5) if mode == "round" else int(val)
    return y


v.check("Ex 16-10.5a", first_order(0.9, 20, "round"))
v.check("Ex 16-10.5b", abs(first_order(-0.9, 20, "round")))
v.assert_true("magnitude truncation decays to zero", first_order(0.9, 20, "zero") == 0 and first_order(-0.9, 20, "zero") == 0)
v.check("16-10.9a", first_order(0.95, 200, "round"))
v.check("16-10.9b", first_order(0.99, 200, "round"))


def so(a1, a2, y1, y2, mode, n):
    Q = 2**15
    Y1, Y2 = round(y1 * Q), round(y2 * Q)
    A1, A2 = round(a1 * 2**14), round(a2 * 2**14)
    out = []
    for _ in range(n):
        y = math.floor((-A1 * Y1 - A2 * Y2) / 2**14 + 0.5)
        y = (y + Q) % (2 * Q) - Q if mode == "wrap" else max(-Q, min(Q - 1, y))
        Y2, Y1 = Y1, y
        out.append(y)
    return out


v.check("Ex 16-10.5c", max(map(abs, so(-1.6, 0.9, 0.9, -0.9, "wrap", 1000)[-50:])))
v.check("Ex 16-10.5d", max(map(abs, so(-1.6, 0.9, 0.9, -0.9, "sat", 1000)[-50:])))
v.check("Ex 16-10.5e", max(map(abs, so(-1.6, 0.9, 0.9, -0.9, "sat", 200)[-50:])))
v.assert_true("lab second-order simulator agrees", q.second_order_zero_input(-1.6, 0.9, 0.9, -0.9, "wrap", 1000)
              == so(-1.6, 0.9, 0.9, -0.9, "wrap", 1000))

# ---------------------------------------------------------------------------------------- Problems 1-4, 11
v.check("16-10.1a", 2.0**-12)
v.check("16-10.1b", 2.0**-31)
v.check("16-10.1c", next(I for I in range(1, 20) if 2 ** (I - 1) > 20))
v.check("16-10.1d", next(F for F in range(1, 30) if 2.0**-F <= 0.001))
v.check("16-10.1e", 6 + 10)
v.check("16-10.2a", 10 * math.log10(1.5 * 4**10))
v.check("16-10.2b", 10 * math.log10(1.5 * 4**14))
v.check("16-10.2c", (100 - 1.76) / 6.02)
v.check("16-10.2d", math.ceil((100 - 1.76) / 6.02))
rng = np.random.default_rng(3)
vals = rng.uniform(-0.9, 0.9, (2000, 1000))
errs = (np.floor(vals / D15) * D15 - vals).sum(axis=1)
v.assert_true("simulated truncation bias matches -500 LSB", abs(errs.mean() / (-1000 * D15 / 2) - 1) < 0.01)
v.check("16-10.3a", -1000 * D15 / 2)
v.check("16-10.4a", D15**2 / 12)
rng = np.random.default_rng(11)
xs = rng.uniform(-100, 100, 400000)
e_r = np.floor(rng.uniform(-0.5, 0.5, 400000) + xs + 0.5) - xs
e_t = np.floor(xs + rng.uniform(-0.5, 0.5, 400000) + rng.uniform(-0.5, 0.5, 400000) + 0.5) - xs
e_0 = np.floor(xs + 0.5) - xs
v.check("16-10.11a", 10 * math.log10(np.var(e_r) / np.var(e_0)), tol=0.05)
v.check("16-10.11b", 10 * math.log10(np.var(e_t) / np.var(e_0)), tol=0.05)
v.check("16-10.11a", 10 * math.log10((1 / 6) / (1 / 12)))
v.check("16-10.11b", 10 * math.log10((1 / 4) / (1 / 12)))

# ---------------------------------------------------------------------------------------- floating point (Problem 12, §9)


def fp_values(ebits, mbits, bias, finite_max=None, ieee_special=True):
    """All non-negative finite values of a binary format, built from its bit fields."""
    out = []
    for e in range(2**ebits):
        for m in range(2**mbits):
            if ieee_special and e == 2**ebits - 1:
                continue  # Inf/NaN
            val = (m / 2**mbits) * 2.0 ** (1 - bias) if e == 0 else (1 + m / 2**mbits) * 2.0 ** (e - bias)
            out.append(val)
    out = sorted(set(out))
    if finite_max is not None:
        out = [x_ for x_ in out if x_ <= finite_max]
    return np.array(out)


E4M3 = fp_values(4, 3, 7, ieee_special=False)
E4M3 = E4M3[E4M3 <= 448]          # S.1111.111 is NaN, so the largest finite value is S.1111.110
E5M2 = fp_values(5, 2, 15)
BF16 = fp_values(8, 7, 127)


def nearest(vals, x):
    i = int(np.argmin(np.abs(vals - x)))
    return float(vals[i])


v.check("Txt 16-10.f", float(E4M3.max()))
v.check("Txt 16-10.g", float(E5M2.max()))
v.check("Txt 16-10.l", float(np.finfo(np.float16).max))
v.check("Txt 16-10.h", 100 * 2.0**-4)
v.check("Txt 16-10.i", 100 * 2.0**-3)
v.check("Txt 16-10.j", 100 * 2.0**-8)
v.check("Txt 16-10.k", 100 * 2.0**-11)
_rr = np.random.default_rng(16)
for _vals, _p, _lo, _name in ((E4M3, 4, 2.0**-6, "E4M3"), (E5M2, 3, 2.0**-14, "E5M2"), (BF16, 8, 2.0**-126, "bfloat16")):
    _x = np.exp(_rr.uniform(math.log(_lo), math.log(_vals.max() * 0.99), 3000))
    _err = max(abs(nearest(_vals, xx) - xx) / xx for xx in _x)
    v.assert_true(f"{_name}: relative rounding error <= 2^-p over the normal range", _err <= 2.0**-_p * (1 + 1e-12), f"{_err:.4g}")
_x16 = np.exp(_rr.uniform(math.log(2.0**-14), math.log(60000.0), 3000))
v.assert_true("binary16: relative rounding error <= 2^-11 over the normal range",
              np.max(np.abs(_x16.astype(np.float16).astype(float) - _x16) / _x16) <= 2.0**-11 * (1 + 1e-12))
v.check("Txt 16-10.m", (8 + 32 * 4) / 32)
v.check("16-10.12a", 100 * (nearest(E4M3, 0.3) - 0.3) / 0.3)
v.check("16-10.12b", 100 * (nearest(BF16, 0.3) - 0.3) / 0.3)
v.check("16-10.12c", 100 * (float(np.float16(0.3)) - 0.3) / 0.3)
v.check("16-10.12d", min(nearest(E4M3, 1000), 448))
v.check("16-10.12e", nearest(E5M2, 1000))
v.check("16-10.12f", nearest(E4M3, 0.3))
v.assert_true("E5M2 rounds 0.3 to the same 0.3125", nearest(E5M2, 0.3) == nearest(E4M3, 0.3))
v.check("16-10.12g", nearest(BF16, 0.3))
v.check("16-10.12h", float(np.float16(0.3)))
v.check("16-10.12i", 100 * (nearest(E5M2, 1000) - 1000) / 1000)
v.assert_true("E5M2 rounds 0.3 like E4M3, to 0.3125", nearest(E5M2, 0.3) == 0.3125 == nearest(E4M3, 0.3))

# ---------------------------------------------------------------------------------------- Lab: 6 dB per bit
Ns = np.arange(8, 21)
sims = np.array([sim_sine(int(B)) for B in Ns])
slope, icpt = np.polyfit(Ns, sims, 1)
v.check("Lab 16-10.a", slope)
v.check("Lab 16-10.b", icpt)
v.assert_true("every point within 0.05 dB of 6.02N + 1.76", np.max(np.abs(sims - (6.02 * Ns + 1.76))) < 0.05)

from scipy import signal as _sg  # noqa: E402
_sos = _sg.ellip(8, 0.1, 60, 4000, fs=48000, output="sos")
_sharp = max(_sos, key=lambda sec: max(abs(np.roots(sec[3:]))))
_g = _sg.lfilter([1.0], _sharp[3:], np.r_[1.0, np.zeros(20000)])
_ng = float(np.sum(_g**2))
v.assert_true("sharpest elliptic section noise gain is 66.05", abs(_ng - 66.05) < 0.005, f"{_ng:.3f}")
v.check("Txt 16-10.n", 10 * math.log10(_ng))
v.check("Txt 16-10.o", 10 * math.log10(_ng) - 3 * 20 * math.log10(2))
v.check("Txt 16-10.p", 10 * math.log10(1.5 * 4**24))

sys.exit(v.finish())
