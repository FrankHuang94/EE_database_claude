#!/usr/bin/env python3
"""Verify every number in chapter 20-08 (oversampling and sigma-delta converters), its problems and its lab.

Independent routes:
- in-band noise by numerical quadrature of |NTF|^2 (the chapter uses the small-angle closed form);
- first-order traces in exact rational (Fraction) or scaled-integer arithmetic;
- modulators re-implemented here: the second-order loop in error-feedback form (STF 1, input delayed two samples),
  which the lab realizes as two integrators; the MASH and the Lee-rule loops with a different summation order;
- spectra by a two-sided FFT periodogram and, for single tones, explicit DFT sums;
- optimal NTF zeros by numerical minimization; Lee-rule NTFs by bisection on a dense-grid peak gain;
- MASH cancellation and excess-loop-delay algebra in sympy; anti-aliasing by quadrature of the integrate-and-dump.
ngspice confirms the first-order traces (run_spice). The lab module (dsm.py) is asserted to agree.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
import sympy as sp
from scipy import integrate, optimize, signal

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "20-08-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import dsm as lab  # noqa: E402

v = Verifier.from_files("20-08", ROOT / "chapters" / "20-08-sigma-delta-converters.md",
                        ROOT / "solutions" / "20-08-solutions.md", LAB / "README.md")
KT = 1.380649e-23 * 300.0
lg = math.log10
N = 2 ** 16


def inband_noise(order, osr, var=1 / 3):
    """Exact in-band noise of NTF (1 - z^-1)^L by quadrature, white error of variance var."""
    wb = math.pi / osr
    val, _ = integrate.quad(lambda w: (2 * math.sin(w / 2)) ** (2 * order), 0, wb)
    return var / math.pi * val


def model_sqnr(order, osr, amp, step=2.0):
    return 10 * lg((amp ** 2 / 2) / (step ** 2 / 12 * math.pi ** (2 * order) / ((2 * order + 1) * osr ** (2 * order + 1))))


def periodogram_sqnr(y, m, osr):
    """Two-sided periodogram with a Hann window; signal = bins m-2..m+2, noise = bins 3..N/(2 OSR)."""
    n = y.size
    w = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(n) / (n - 1))       # numpy's symmetric Hann
    p = np.abs(np.fft.fft(y * w)) ** 2
    p = p[:n // 2 + 1] + np.concatenate([[0], p[:n // 2:-1], [0]])[:n // 2 + 1]  # fold negative frequencies
    sig = p[m - 2:m + 3].sum()
    return 10 * lg(sig / (p[3:n // (2 * osr) + 1].sum() - sig))


def ef_loop(x, b, a=(1.0,), levels=2):
    """Error-feedback modulator, summation written out term by term (lab: vector dot products)."""
    b = list(b) + [0.0] * (max(len(a), len(b)) - len(b))
    a = list(a) + [0.0] * (len(b) - len(a))
    order = len(b) - 1
    e = [0.0] * order
    g = [0.0] * order
    y = np.empty(len(x))
    for n in range(len(x)):
        acc = 0.0
        for k in range(order - 1, -1, -1):
            acc += (b[k + 1] - a[k + 1]) * e[k] - a[k + 1] * g[k]
        w = x[n] + acc
        if not math.isfinite(w) or abs(w) > 1e9:
            return None
        if levels == 2:
            q = 1.0 if w >= 0 else -1.0
        else:
            d = 2.0 / (levels - 1)
            q = float(np.clip(np.round((w + 1) / d) * d - 1, -1, 1))
        y[n] = q
        e = [q - w] + e[:-1]
        g = [acc] + g[:-1]
    return y


def first_order(x):
    u, y = 0.0, np.empty(len(x))
    for n in range(len(x)):
        y[n] = 1.0 if u >= 0 else -1.0
        u += x[n] - y[n]
    return y


def sine(m, amp=0.5, phase=0.0):
    return amp * np.sin(2 * np.pi * m * np.arange(N) / N + phase)


def tone_bin(osr):
    return int(N / (2 * osr) / 3) | 1


# ------------------------------------------------------------------ Example 20-08.1
print("Example 20-08.1")
nyq12 = 20 * lg(2 ** 12) + 10 * lg(1.5)
v.check("Ex 20-08.1a", nyq12)
osr16 = 10 ** (4 * 20 * lg(2) / 10)
v.check("Ex 20-08.1b", osr16)
v.check("Ex 20-08.1c", nyq12 + 10 * lg(osr16))
v.check("Ex 20-08.1d", 2 * 20e3 * osr16 / 1e6)
v.check("Txt 20-08.e", 4 ** 12)

# ------------------------------------------------------------------ Example 20-08.2 (exact arithmetic)
print("Example 20-08.2")
u, x0, us, ys = Fr(1, 10), Fr(1, 5), [], []
for _ in range(40):
    y = 1 if u >= 0 else -1
    ys.append(y)
    u = u + x0 - y
    us.append(u)
for key, val in zip("abcde", us[:5]):
    v.check(f"Ex 20-08.2{key}", float(val))
period = next(p for p in range(1, 40) if us[p - 1] == Fr(1, 10))
v.check("Ex 20-08.2g", period)
v.check("Ex 20-08.2f", float(Fr(sum(ys[:period]), period)))
v.assert_true("lab mod1 reproduces the trace", np.allclose(lab.mod1(np.full(6, 0.2), u0=0.1)[1][1:], [float(q) for q in us[:5]]))
# idle tone for x = 0.002: integer arithmetic in units of 1/1000
xi, ui, nn = 2, 100, 8000
yi = np.empty(nn)
for n in range(nn):
    yi[n] = 1 if ui >= 0 else -1
    ui += xi - int(yi[n]) * 1000
k = round(0.002 * nn)
amp = 2 * abs(np.sum(yi * np.exp(-2j * np.pi * k * np.arange(nn) / nn))) / nn
v.check("Ex 20-08.2h", 0.002 * 5.12e6 / 1e3)
v.check("Ex 20-08.2i", 20 * lg(amp))
v.assert_true("idle-tone amplitude equals 2x", abs(amp - 0.004) < 1e-9)
v.check("Ex 20-08.2j", 1 / (2 * 128))

# ------------------------------------------------------------------ Example 20-08.3
print("Example 20-08.3")
q1 = 10 * lg(0.5 / (1 / 3))
v.check("Ex 20-08.3a", 10 * lg(0.5 / inband_noise(1, 64)))
v.check("Ex 20-08.3b", 10 * lg(0.5 / inband_noise(2, 64)))
v.assert_true("closed form matches quadrature within 0.02 dB",
              abs(model_sqnr(2, 64, 1) - 10 * lg(0.5 / inband_noise(2, 64))) < 0.02)
v.check("Ex 20-08.3c", 30 * lg(2))
v.check("Ex 20-08.3d", 50 * lg(2))
v.check("Txt 20-08.a", 70 * lg(2))
v.check("Txt 20-08.b", 90 * lg(2))
v.check("Txt 20-08.c", 10 * lg(math.pi ** 2 / 3))
v.check("Txt 20-08.d", 10 * lg(math.pi ** 4 / 5))
wb = math.pi / 16
v.check("Txt 20-08.f", ((wb ** 3 / 3) / (2 * (wb - math.sin(wb))) - 1) * 100)
v.check("Ex 20-08.3e", model_sqnr(1, 64, 0.5))
v.check("Ex 20-08.3f", model_sqnr(2, 64, 0.5))
sims = {}
for osr in (32, 64, 128):
    m = tone_bin(osr)
    x = sine(m)
    y2 = ef_loop(np.concatenate([[0.0, 0.0], x[:-2]]), [1, -2, 1])
    sims[osr] = periodogram_sqnr(y2, m, osr)
    if osr == 64:
        y1 = first_order(x)
        v.check("Ex 20-08.3g", periodogram_sqnr(y1, m, 64))
        v.assert_true("lab mod2 bitstream equals the error-feedback loop", np.array_equal(lab.mod2(x)[0], y2))
        v.assert_true("lab SQNR routine agrees", abs(lab.inband_sqnr(y2, m, 64) - sims[64]) < 1e-9)
        y16 = ef_loop(np.concatenate([[0.0, 0.0], x[:-2]]), [1, -2, 1], levels=16)
        v.check("Ex 20-08.3k", periodogram_sqnr(y16, m, 64))
        dy2 = {"1": np.mean(np.diff(y2) ** 2), "16": np.mean(np.diff(y16) ** 2)}
v.check("Ex 20-08.3h", sims[64])
v.check("Ex 20-08.3i", sims[32])
v.check("Ex 20-08.3j", sims[128])
v.check("Ex 20-08.3m", (sims[128] - sims[32]) / 2)
v.check("Ex 20-08.3l", 20 * lg(15))

# ------------------------------------------------------------------ Example 20-08.4
print("Example 20-08.4")


def osr_needed(target, order, step, amp=0.5):
    return optimize.brentq(lambda r: model_sqnr(order, r, amp, step) - target, 1.0, 1e6)


v.check("Ex 20-08.4a", osr_needed(100, 2, 2.0))
v.check("Ex 20-08.4b", 2 * 20e3 * 256 / 1e6)
v.check("Ex 20-08.4c", osr_needed(100, 2, 2 / 15))
v.check("Ex 20-08.4e", KT / (0.125e-10 * 128) * 1e12)
v.check("Ex 20-08.4f", KT / 0.125e-10 * 1e12)

# ------------------------------------------------------------------ Example 20-08.5
print("Example 20-08.5")
f2 = lambda a: integrate.quad(lambda t: (t * t - a * a) ** 2, 0, 1)[0]  # noqa: E731
f3 = lambda a: integrate.quad(lambda t: t * t * (t * t - a * a) ** 2, 0, 1)[0]  # noqa: E731
r2 = optimize.minimize_scalar(f2, bounds=(0, 1), method="bounded", options={"xatol": 1e-10})
r3 = optimize.minimize_scalar(f3, bounds=(0, 1), method="bounded", options={"xatol": 1e-10})
v.check("Ex 20-08.5a", 10 * lg(f2(0) / r2.fun))
v.check("Ex 20-08.5b", 10 * lg(f3(0) / r3.fun))
v.check("Ex 20-08.5c", r2.x * 20)
v.assert_true("optimal L = 3 zeros at sqrt(3/5)", abs(r3.x ** 2 - 0.6) < 1e-6)
grid = np.linspace(0, np.pi, 20001)
peak = lambda b, a: np.abs(np.polyval(b[::-1], np.exp(-1j * grid)) / np.polyval(a[::-1], np.exp(-1j * grid))).max()  # noqa: E731
v.check("Ex 20-08.5d", peak(np.poly([1, 1])[::-1], np.array([1.0])))
v.check("Ex 20-08.5e", peak(np.poly([1] * 4)[::-1], np.array([1.0])))
lee = {}
for order, (ka, kp) in ((3, ("5h", "5f")), (4, ("5i", "5g"))):
    bb = np.poly([1] * order)

    def gap(wc, order=order, bb=bb):
        _, aa = signal.butter(order, wc, "high")
        return peak(bb[::-1], (aa / aa[0])[::-1]) - 1.5
    wc = optimize.brentq(gap, 0.01, 0.9, xtol=1e-14)
    _, aa = signal.butter(order, wc, "high")
    aa = aa / aa[0]
    lee[order] = (bb, aa)
    v.check(f"Ex 20-08.{ka}", abs(aa.sum()))
    v.check(f"Ex 20-08.{kp}", 20 * lg(1 / abs(aa.sum())))
    lb, la = lab.lee_ntf(order)
    v.assert_true(f"lab Lee NTF (order {order}) matches", np.allclose(la, aa, rtol=1e-6))
    v.assert_true(f"pure order-{order} 1-bit loop diverges", ef_loop(sine(171), bb) is None)
    vals = [periodogram_sqnr(ef_loop(sine(171, phase=k * np.pi / 8), bb, aa), 171, 64) for k in range(8)]
    v.check("Lab 20-08.d" if order == 3 else "Lab 20-08.e", np.mean(vals))

# ------------------------------------------------------------------ Example 20-08.6
print("Example 20-08.6")
v.check("Ex 20-08.6a", math.sqrt(3) * 64 / math.pi)
amash = math.sqrt(5) * 64 ** 2 / math.pi ** 2
v.check("Ex 20-08.6b", amash)
v.check("Ex 20-08.6c", 20 * lg(amash))
ideal = inband_noise(2, 64)
for key, a in (("6d", 100), ("6e", 1000)):
    v.check(f"Ex 20-08.{key}", 10 * lg(0.125 / (ideal + (1 / 3) / (a * a * 64))))
v.check("Ex 20-08.6f", 10 * lg(0.125 / ideal))
z, e1, e2, xx = sp.symbols("z E1 E2 X")
y1 = xx / z + (1 - 1 / z) * e1
y2 = -e1 / z + (1 - 1 / z) * e2
v.assert_true("1-1 MASH cancels E1", sp.simplify(y1 / z + (1 - 1 / z) * y2 - (xx / z ** 2 + (1 - 1 / z) ** 2 * e2)) == 0)
cs, ci, aa_ = sp.symbols("C_s C_i A", positive=True)
pole = (1 + 1 / aa_) / (1 + (1 + cs / ci) / aa_)
v.assert_true("integrator leak is (Cs/Ci)/A to first order",
              sp.simplify(sp.series(pole.subs(aa_, 1 / sp.Symbol("t")), sp.Symbol("t"), 0, 2).removeO() - (1 - cs / ci * sp.Symbol("t"))) == 0)


def mash(x, eps):
    s1 = s2 = 0.0
    out = np.empty(len(x))
    py1 = py2 = 0.0
    for n in range(len(x)):
        a = 1.0 if s1 >= 0 else -1.0
        b = 1.0 if s2 >= 0 else -1.0
        out[n] = py1 + b - py2
        e = a - s1
        s1 = (1 - eps) * s1 + x[n] - a
        s2 = s2 - e - b
        py1, py2 = a, b
    return out


xm = sine(171)
for key, eps in (("Lab 20-08.a", 0.0), ("Lab 20-08.b", 1e-3), ("Lab 20-08.c", 1e-2)):
    ym = mash(xm, eps)
    v.check(key, periodogram_sqnr(ym, 171, 64))
    v.assert_true(f"lab MASH output matches (eps = {eps})", np.array_equal(ym, lab.mash11(xm, eps)))

# ------------------------------------------------------------------ Example 20-08.7
print("Example 20-08.7")
h = lambda f: abs(integrate.quad(lambda t: math.cos(2 * math.pi * f * t), 0, 1)[0]  # noqa: E731
                  - 1j * integrate.quad(lambda t: math.sin(2 * math.pi * f * t), 0, 1)[0])
v.check("Ex 20-08.7a", 20 * lg(h(1 - 1 / 128)))
u, yp, us = Fr(1, 10), 1, []
for _ in range(5):
    y = 1 if u >= 0 else -1
    u = u + Fr(1, 5) - Fr(1, 2) * y - Fr(1, 2) * yp
    yp = y
    us.append(u)
for key, val in zip("bcdef", us):
    v.check(f"Ex 20-08.7{key}", float(val))
v.assert_true("lab ct1 reproduces the delayed trace", np.allclose(lab.ct1(np.full(6, 0.2), 0.5, 0.1, 1.0)[1][1:], [float(q) for q in us]))
v.check("Ex 20-08.7g", abs(np.roots([1, -0.5, 0.5])).max())
v.check("Ex 20-08.7h", dy2["1"])
v.check("Ex 20-08.7i", dy2["16"])
jit = {k: 10 * lg(0.125 / (val * (1e-12 * 1.28e9) ** 2 / 32)) for k, val in dy2.items()}
v.check("Ex 20-08.7j", jit["1"])
v.check("Ex 20-08.7k", jit["16"])
nyq_j = -20 * lg(2 * math.pi * 20e6 * 1e-12)
v.check("Ex 20-08.7l", nyq_j)
v.check("Ex 20-08.7m", nyq_j - jit["1"])

# ------------------------------------------------------------------ practitioner numbers (sec. 3.3, 7, 9)
print("Practitioner numbers")
v.check("Txt 20-08.g", (111.5 - 1.76) / 6.02)              # ADS127L21 dynamic range -> effective bits
v.check("Txt 20-08.h", 2.4e6 / (2 * 20e3))                 # T5838 high-quality mode
v.check("Txt 20-08.i", 20 * lg(58 / 9.7))                  # ADS1298 noise, 32 kSPS -> 16 kSPS
v.check("Txt 20-08.j", 128e3 / 500)                        # ADS1292 modulator clock / data rate
v.check("Txt 20-08.k", 10 * lg(0.5 / inband_noise(1, 128)))
v.check("Txt 20-08.l", 10 * lg(0.75 ** 2 / 2 / inband_noise(2, 128)))
v.check("Txt 20-08.m", 20 * lg(2))

# ------------------------------------------------------------------ problems
print("Problems")
s1 = 20 * lg(2 ** 10) + 10 * lg(1.5) + 10 * lg(16)
v.check("20-08.1a", s1)
v.check("20-08.1b", (s1 - 10 * lg(1.5)) / (20 * lg(2)))
u, us, ys = Fr(3, 10), [], []
for _ in range(30):
    y = 1 if u >= 0 else -1
    ys.append(y)
    u = u + Fr(-2, 5) - y
    us.append(u)
for key, val in zip("abcd", us):
    v.check(f"20-08.2{key}", float(val))
per = next(p for p in range(1, 30) if us[p - 1] == Fr(3, 10))
v.check("20-08.2f", per)
v.check("20-08.2e", ys[:per].count(1) / per)
v.check("20-08.3a", 0.004 * 2.56e6 / 1e3)
v.check("20-08.3b", 20 * lg(0.008))
v.check("20-08.3c", 2.56e6 / 128 / 1e3)
v.check("20-08.3d", 1 / 128)
v.check("20-08.4a", model_sqnr(3, 32, 0.5))
v.check("20-08.4b", model_sqnr(3, 32, 0.5, 2 / 15))
o1, o2 = osr_needed(90, 1, 2.0), osr_needed(90, 2, 2.0)
v.check("20-08.5a", o1)
v.check("20-08.5b", o2)
v.check("20-08.5c", o1 / o2)
v.check("20-08.6a", 24 / math.sqrt(3))
v.check("20-08.6b", 10 * lg(f2(0) / f2(math.sqrt(1 / 3))))
ntf2 = lambda w: abs(1 - np.exp(-1j * w)) ** 2  # noqa: E731
v.check("20-08.7a", ntf2(np.pi / 2) ** 2)          # |NTF|^2 = (|1 - z^-1|^2)^2
v.check("20-08.7b", ntf2(np.pi))
v.check("20-08.7c", 10 * lg(ntf2(np.pi / 64) ** 2))
Y = (xx / z ** 2 + (1 - 1 / z) ** 2 * e1) / z + (1 - 1 / z) ** 2 * y2
v.assert_true("2-1 MASH gives z^-3 X + (1 - z^-1)^3 E2", sp.simplify(Y - (xx / z ** 3 + (1 - 1 / z) ** 3 * e2)) == 0)
v.check("20-08.8a", sp.degree(sp.expand((z - 1) ** 3), z))
v.check("20-08.8b", model_sqnr(3, 64, 0.5))
v.check("20-08.9a", KT / (3.125e-12 * 256) * 1e12)
v.check("20-08.9b", KT / (3.125e-12 * 64) * 1e12)
v.check("20-08.10a", 0.5 * math.sqrt(3) * 128 / math.pi)
a10 = math.sqrt(5) * 128 ** 2 / math.pi ** 2
v.check("20-08.10b", a10)
v.check("20-08.10c", 20 * lg(a10))
v.check("20-08.11a", abs(np.roots([1, -0.25, 0.25])).max())
v.check("20-08.11b", abs(2 / (1 + 0.25 + 0.25)))
for key, e in (("12a", 2.36), ("12b", 0.0298)):
    v.check(f"20-08.{key}", math.sqrt(0.125e-7 * 16 / e) / 640e6 * 1e12)
v.check("20-08.12c", math.sqrt(2.36 / 0.0298))
v.check("20-08.13a", 20 * lg(h(1 - 1 / 64)))
v.check("20-08.14a", 3 + 1)
zz = np.exp(2j * np.pi / 256)
cic = abs(np.sum(zz ** -np.arange(32)) / 32) ** 4
v.check("20-08.14b", 20 * lg(cic))
v.assert_true("lab CIC gain agrees", abs(lab.cic_gain(1 / 256, 32, 4) - cic) < 1e-12)
v.check("20-08.14c", 4 * math.log2(32))
oa, ob = osr_needed(70, 2, 2.0), osr_needed(70, 3, 2 / 15)
v.check("20-08.15a", oa)
v.check("20-08.15b", 2 * 20e6 * oa / 1e9)
v.check("20-08.15c", ob)
v.check("20-08.15d", 2 * 20e6 * ob / 1e9)
v.check("20-08.15e", oa / ob)

sys.exit(v.finish())
