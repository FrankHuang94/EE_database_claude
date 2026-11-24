#!/usr/bin/env python3
"""Verify every number in chapter 20-09 (DACs), its problems and its lab.

Independent routes:
- the R-2R ladder by an explicit Thevenin recursion (ideal) and by a modified-nodal solve written here with a
  different node ordering (with switch resistance); the lab uses its own nodal solver;
- DNL spreads from variance sums, checked against a seeded Monte Carlo of the cell structure;
- the Kolmogorov quantile by root finding on the series and an independent Monte Carlo of max |INL|;
- output-impedance harmonics by explicit Fourier projection over one period (the lab uses an FFT);
- sinc responses from numerical integrals of the pulse shapes;
- DWA with an explicit pointer simulation.
ngspice confirms the ladder output, the switch-resistance DNL and the output-impedance compression (run_spice).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "20-09-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import dac as lab  # noqa: E402

v = Verifier.from_files("20-09", ROOT / "chapters" / "20-09-dacs.md", ROOT / "solutions" / "20-09-solutions.md",
                        LAB / "README.md")
lg = math.log10


def ladder_thevenin(code, nbits, vref):
    vk = 0.0
    for k in range(nbits):
        vk = (((code >> k) & 1) * vref + vk) / 2
    return vk


def ladder_mna(code, nbits, vref, rsw, leg_adj=0.0, term_adj=0.0):
    """Nodes ordered MSB first; R = 1. Every 2R leg has a switch resistance rsw (legs 2R + rsw + leg_adj); the
    termination is 2R + term_adj."""
    n = nbits
    g = np.zeros((n, n))
    rhs = np.zeros(n)
    idx = lambda k: n - 1 - k  # noqa: E731
    for k in range(n):
        i = idx(k)
        gl = 1 / (2 + rsw + leg_adj)
        g[i, i] += gl
        rhs[i] += gl * vref * ((code >> k) & 1)
        if k > 0:
            j = idx(k - 1)
            g[i, i] += 1
            g[j, j] += 1
            g[i, j] -= 1
            g[j, i] -= 1
    g[idx(0), idx(0)] += 1 / (2 + term_adj)
    return np.linalg.solve(g, rhs)[idx(n - 1)]


def kolmogorov_lambda(y):
    cdf = lambda lam: 1 - 2 * sum((-1) ** (k - 1) * math.exp(-2 * k * k * lam * lam) for k in range(1, 80))  # noqa: E731
    return optimize.brentq(lambda lam: cdf(lam) - y, 0.3, 4)


def harmonic(fun, k, npts=8192):
    """Amplitude of harmonic k of fun(sin t) over one period by direct projection."""
    t = 2 * np.pi * np.arange(npts) / npts
    y = fun(np.sin(t))
    a = 2 / npts * np.sum(y * np.cos(k * t))
    b = 2 / npts * np.sum(y * np.sin(k * t))
    return math.hypot(a, b)


def hd(fun, k):
    return 20 * lg(harmonic(fun, k) / harmonic(fun, 1))


def pulse_gain(f, shape):
    """|H(f)| of a pulse p(t) on [0, 1) (time in sample periods), normalized to the NRZ DC gain."""
    re = integrate.quad(lambda t: shape(t) * math.cos(2 * math.pi * f * t), 0, 1, points=[0.5], limit=200)[0]
    im = integrate.quad(lambda t: shape(t) * math.sin(2 * math.pi * f * t), 0, 1, points=[0.5], limit=200)[0]
    return math.hypot(re, im)


NRZ = lambda t: 1.0  # noqa: E731
RZ = lambda t: 1.0 if t < 0.5 else 0.0  # noqa: E731
MIX = lambda t: 1.0 if t < 0.5 else -1.0  # noqa: E731
db = lambda f, s: 20 * lg(pulse_gain(f, s))  # noqa: E731

# ------------------------------------------------------------------ Example 20-09.1
print("Example 20-09.1")
v.check("Ex 20-09.1a", 1.2 / 1024 * 1e3)
v.check("Ex 20-09.1b", ladder_thevenin(683, 10, 1.2))
v.assert_true("lab ladder solver agrees (ideal)", abs(lab.r2r_output(683, 10, 1.2) - ladder_thevenin(683, 10, 1.2)) < 1e-12)
v.check("Ex 20-09.1c", 2 ** 10)
v.check("Ex 20-09.1d", 2 ** 11 - 2)
vs = np.array([ladder_mna(c, 10, 1.2, 0.01) for c in range(1024)])
lsb = (vs[-1] - vs[0]) / 1023
dnl = np.diff(vs) / lsb - 1
inl = (vs - vs[0]) / lsb - np.arange(1024)
v.check("Ex 20-09.1e", dnl[np.argmax(np.abs(dnl))])          # signed: negative means a falling step
v.check("Ex 20-09.1g", -(vs[512] - vs[511]) * 1e3)
v.assert_true("non-monotonic: code 512 below code 511", vs[512] < vs[511])


def worst_dnl(**kw):
    vv = np.array([ladder_mna(c, 10, 1.2, 0.01, **kw) for c in range(1024)])
    dd = np.diff(vv) / ((vv[-1] - vv[0]) / 1023) - 1
    return dd[np.argmax(np.abs(dd))]


v.assert_true("padding only the termination does not fix it", worst_dnl(term_adj=0.01) < -1.6)
v.assert_true("legs made 2R - r_sw restore binary weighting", abs(worst_dnl(leg_adj=-0.01)) < 1e-9)
v.check("Ex 20-09.1f", np.abs(inl).max())
v.assert_true("worst DNL at the 511 -> 512 transition", int(np.argmax(np.abs(dnl))) == 511)
v.assert_true("lab ladder solver agrees (switch resistance)",
              abs(lab.r2r_output(512, 10, 1.2, r_sw=0.01) - vs[512]) < 1e-12)

# ------------------------------------------------------------------ Example 20-09.2
print("Example 20-09.2")
su = 0.005
v.check("Ex 20-09.2a", 14)
v.check("Ex 20-09.2b", su * math.sqrt(2 ** 13 + 2 ** 13 - 1))
v.check("Ex 20-09.2c", 14)
v.check("Ex 20-09.2d", 2 ** 14 - 1)
v.check("Ex 20-09.2e", su)
v.check("Ex 20-09.2f", (2 ** 6 - 1) + 8)
v.check("Ex 20-09.2g", su * math.sqrt(2 ** 8 + 2 ** 8 - 1))
v.check("Ex 20-09.2h", 8 + 1)
v.check("Ex 20-09.2i", 1 / (su * math.sqrt(2 ** 14 - 1)))
rng = np.random.default_rng(209)
steps = []
for _ in range(400):
    lv = lab.cs_levels(14, 6, su, rng)
    steps.append(lv[2 ** 8] - lv[2 ** 8 - 1] - (lv[-1] - lv[0]) / (2 ** 14 - 1))
v.assert_true("Monte Carlo segmented DNL spread within 15% of 0.113", abs(np.std(steps) / 0.11303 - 1) < 0.15)

# ------------------------------------------------------------------ Example 20-09.3
print("Example 20-09.3")
lam = kolmogorov_lambda(0.9973)
C = stats.norm.ppf(0.5 + 0.9973 / 2)
v.check("Ex 20-09.3a", 1 / (C * 64) * 100)
v.check("Ex 20-09.3b", lam)
s_exact = 0.5 / (lam * 64)
v.check("Ex 20-09.3c", s_exact * 100)
wl = (math.sqrt(2) * 3.5e-3 / (0.4 * s_exact)) ** 2
v.check("Ex 20-09.3d", wl)
v.check("Ex 20-09.3e", wl * 4095 / 1e6)
v.check("Txt 20-09.a", (1 - (C / 2) / lam) * 100)
rng = np.random.default_rng(2009)


def mc_yield(sig, trials=3000, nt=4095):
    e = rng.normal(0, sig, (trials, nt))
    c = np.concatenate([np.zeros((trials, 1)), np.cumsum(1 + e, axis=1)], axis=1)
    inl_ = c / (c[:, -1:] / nt) - np.arange(nt + 1)
    return np.mean(np.abs(inl_).max(axis=1) <= 0.5)


y_mid, y_exact = mc_yield(1 / (C * 64)), mc_yield(s_exact)
v.assert_true(f"Monte Carlo: mid-scale estimate misses the target (yield {y_mid:.4f})", y_mid < 0.99)
v.assert_true(f"Monte Carlo: exact rule meets the target within sampling error (yield {y_exact:.4f})", y_exact > 0.993)

# ------------------------------------------------------------------ Example 20-09.4
print("Example 20-09.4")
x4 = 50 / 50e3
lv = np.array([n * 1e-3 * 50 / (1 + n * x4) for n in range(16)])
v.check("Ex 20-09.4a", lv[-1])
l4 = lv[-1] / 15
v.check("Ex 20-09.4b", np.max(np.abs(lv / l4 - np.arange(16))))
v.check("Ex 20-09.4c", 25 * 4095 ** 2 / 2 / 1e6)
z100 = 1 / (2 * math.pi * 1e8 * 1e-15)
v.check("Ex 20-09.4d", z100 / 1e6)
N = 4095


def se_fun(x):
    return lambda s: (N * (1 + s) / 2) / (1 + N * (1 + s) / 2 * x)


def df_fun(x):
    return lambda s: se_fun(x)(s) - (N * (1 - s) / 2) / (1 + N * (1 - s) / 2 * x)


x12 = 25 / z100
h2 = hd(se_fun(x12), 2)
h3 = hd(df_fun(x12), 3)
v.check("Ex 20-09.4e", h2)
v.check("Ex 20-09.4f", h3)
v.assert_true("differential HD2 cancels", hd(df_fun(x12), 2) < -250)
v.check("Ex 20-09.4g", h2 - h3)
v.check("Ex 20-09.4h", hd(df_fun(10 * x12), 3))
v.assert_true("lab harmonic routine agrees", abs(lab.harmonics(df_fun(x12))[3] - h3) < 0.01)
# capacitive quasi-static model: x = j omega C R_L, harmonics from the complex Fourier coefficients


def hd_complex(fun, k, m=4096):
    tt = np.arange(m)
    c = np.fft.fft(fun(np.sin(2 * math.pi * tt / m))) / m
    return 20 * lg(abs(c[k]) / abs(c[1]))


v.check("Ex 20-09.4i", hd_complex(se_fun(1j * x12), 2))
v.check("Ex 20-09.4j", hd_complex(df_fun(1j * x12), 3))
v.check("Ex 20-09.4k", hd_complex(df_fun(10j * x12), 3))
v.assert_true("complex FFT route reproduces the real-x harmonics", abs(hd_complex(se_fun(x12), 2) - h2) < 0.01)

# ------------------------------------------------------------------ Example 20-09.5
print("Example 20-09.5")
v.check("Ex 20-09.5a", db(0.4, NRZ))
v.check("Ex 20-09.5b", db(0.6, NRZ))
v.check("Ex 20-09.5c", db(0.4, NRZ) - db(0.6, NRZ))
v.check("Ex 20-09.5d", db(0.4, RZ))
v.check("Ex 20-09.5e", db(0.6, MIX))
v.check("Ex 20-09.5f", db(0.6, MIX) - db(0.6, NRZ))
v.check("Ex 20-09.5g", db(0.5, NRZ))
v.check("Ex 20-09.5h", db(0.5, RZ))
v.check("Ex 20-09.5i", db(0.5, NRZ) - db(0.5, RZ))
v.check("Txt 20-09.b", db(0, RZ) - db(0.5, RZ))
for f in (0.4, 0.5, 0.6, 0.7):
    for mode, s in (("nrz", NRZ), ("rz", RZ), ("mix", MIX)):
        v.assert_true(f"lab zoh_gain {mode} at {f}", abs(20 * lg(lab.zoh_gain(f, mode)) - db(f, s)) < 1e-6)

# ------------------------------------------------------------------ Example 20-09.6 and 20-09.7
print("Examples 20-09.6, 20-09.7")
bin_err = (2 ** 11 + 2 ** 11 - 1) - 2 ** 11
v.check("Ex 20-09.6d", bin_err)
gb = bin_err / 4096 * 50
gs = (2 ** 6 - 1) / 4096 * 50
v.check("Ex 20-09.6a", gb)
v.check("Ex 20-09.6b", gs)
v.check("Ex 20-09.6c", gb / gs)
n_tau = 17 * math.log(2)
v.check("Ex 20-09.7a", n_tau)
v.check("Ex 20-09.7b", 1e3 / n_tau)
v.check("Ex 20-09.7c", n_tau / (2 * math.pi * 1e-6) / 1e6)
v.check("Ex 20-09.7d", 17 / 5)

# ------------------------------------------------------------------ practitioner and text numbers
print("Practitioner numbers")
v.check("Txt 20-09.c", 1 / (2 * C * 64) * 100)
v.check("Txt 20-09.d", s_exact / (1 / (2 * C * 64)))
v.check("Txt 20-09.k", (s_exact / (1 / (2 * C * 64))) ** 2)
pk = optimize.minimize_scalar(lambda f: -pulse_gain(f, MIX), bounds=(0.5, 1.0), method="bounded", options={"xatol": 1e-9})
v.check("Txt 20-09.e", pk.x)
v.check("Txt 20-09.f", 20 * lg(-pk.fun))
v.check("Txt 20-09.g", 2263 * 1.0 / 3747 * 100)        # DAC39RF10 Mode 1: 1.0 V rail current x voltage / total
v.check("Txt 20-09.h", 155 - 10 * lg(1e9))
v.check("Txt 20-09.i", math.log2(1000))
v.check("Txt 20-09.j", 4 / 0.1)

# ------------------------------------------------------------------ problems
print("Problems")
v.check("20-09.1a", 2.5 / 4096 * 1e3)
v.check("20-09.1b", 3000 * 2.5 / 4096)
v.check("20-09.1c", 4096)
v.check("20-09.2a", ladder_thevenin(0b1011, 4, 1.0))
v.check("20-09.2b", 1.0)
v.check("20-09.3a", 2 ** 5 - 1)
v.check("20-09.3b", 2 ** 11)
v.check("20-09.3c", 11)
v.check("20-09.4a", 0.001 * math.sqrt(2 ** 16 - 1))
v.check("20-09.4b", 0.001 * math.sqrt(2 ** 12 + 2 ** 12 - 1))
lam14 = kolmogorov_lambda(0.9973)
v.check("20-09.5a", 1 / (C * 128) * 100)
s14 = 0.5 / (lam14 * 128)
v.check("20-09.5b", s14 * 100)
wl14 = (math.sqrt(2) * 3.5e-3 / (0.5 * s14)) ** 2
v.check("20-09.6a", wl14)
v.check("20-09.6b", wl14 * 16383 / 1e6)
v.check("20-09.6c", (wl14 * 16383) / (wl * 4095))
z10 = 50 * 1023 ** 2 / 2
v.check("20-09.7a", z10 / 1e6)
v.check("20-09.7b", 20 * lg((50 / z10) * 1023 / 4))
N = 1023
x10 = 0.01 / N
v.check("20-09.8a", 20 * lg(0.01 / 4))
v.check("20-09.8b", 20 * lg(0.01 ** 2 / 16))
v.check("20-09.8c", hd(se_fun(x10), 2))
v.check("20-09.8d", hd(df_fun(x10), 3))
v.check("20-09.9a", db(0.4, NRZ))
v.check("20-09.9b", db(0.6, NRZ))
v.check("20-09.9c", db(0.4, NRZ) - db(0.6, NRZ))
v.check("20-09.10a", -db(0.5, NRZ))
v.check("20-09.10b", db(0, RZ) - db(0.5, RZ))
v.check("20-09.11a", db(0.7, MIX))
v.check("20-09.11b", db(0.7, NRZ))
v.check("20-09.11c", db(0.7, MIX) - db(0.7, NRZ))
v.check("20-09.12a", 511 / 1024 * 100)
v.check("20-09.12b", 63 / 1024 * 100)
nt19 = 19 * math.log(2)
v.check("20-09.13a", 2 / nt19)
v.check("20-09.13b", nt19 / (2 * math.pi * 2e-6) / 1e6)
ptr, used, ptrs = 0, np.zeros(8, int), []
for c in (3, 5, 2):
    for _ in range(c):
        used[ptr] += 1
        ptr = (ptr + 1) % 8
    ptrs.append(ptr)
    if len(ptrs) == 2:
        v.assert_true("after codes 3 and 5 every element is used once", np.all(used == 1))
for key, p_ in zip("abc", ptrs):
    v.check(f"20-09.14{key}", p_)
v.check("20-09.14d", int(np.sum(used == 2)))
v.assert_true("lab DWA agrees", np.array_equal(lab.dwa_select([3, 5, 2], 8).sum(axis=0), used))

# Problem 15: ladder fixed point by iterating the recursion, weights by solving the node equation numerically
eps15 = 0.01
rk = 2.0                                       # start anywhere; the recursion converges
for _ in range(200):
    rk = (rk + 1) * (2 + eps15) / (rk + 3 + eps15)
v.check("20-09.15a", rk)
v.assert_true("closed-form fixed point", abs(rk - (-1 + math.sqrt(9 + 4 * eps15)) / 2) < 1e-12)
v.check("20-09.15b", (2 + eps15) / (rk + 3 + eps15))
v.check("20-09.15c", (rk + 1) / (rk + 3 + eps15))
v.assert_true("first-order a and c", abs((2 + eps15) / (rk + 3 + eps15) - 0.5 * (1 + eps15 / 6)) < 1e-4)
for nb, ke, kn in ((10, "d", "e"), (8, "f", "g")):
    v.check(f"20-09.15{ke}", -(eps15 / 3) * 2 ** (nb - 1))
    vv = np.array([ladder_mna(c, nb, 1.0, eps15) for c in range(2 ** nb)])
    dd = np.diff(vv) / ((vv[-1] - vv[0]) / (2 ** nb - 1)) - 1
    v.check(f"20-09.15{kn}", dd[np.argmax(np.abs(dd))])

# Problem 16: segmentation search, area, and the cell-capacitance bound with the full harmonic analysis
nt16 = 2 ** 14 - 1
su16 = 0.5 / (kolmogorov_lambda(0.9973) * math.sqrt(nt16))
v.assert_true("lambda(99.73%) rounds to 1.818", abs(kolmogorov_lambda(0.9973) - 1.818) < 5e-4)
su16 = 0.5 / (1.818 * math.sqrt(nt16))
v.check("20-09.16a", su16 * 100)
ok_m = [m for m in range(1, 15) if su16 * math.sqrt(2 ** (14 - m + 1) - 1) <= 0.1 and 2 ** m - 1 <= 63]
v.check("20-09.16b", min(ok_m))
v.check("20-09.16c", max(ok_m))
wl16 = (math.sqrt(2) * 3e-3 / (0.4 * su16)) ** 2
v.check("20-09.16d", wl16)
v.check("20-09.16e", wl16 * nt16 / 1e6)
xn16 = 4 * 10 ** (-70 / 40)
v.check("20-09.16f", xn16)
zu16 = 25 / (xn16 / nt16)
v.check("20-09.16g", zu16 / 1e6)
cu16 = 1 / (2 * math.pi * 5e8 * zu16)
v.check("20-09.16h", cu16 * 1e18)
ccell = 256 * cu16
v.check("20-09.16i", ccell * 1e15)


def cell_dac_diff(xc, m_cells=63, units=256):
    """Unary-cell model: m of 63 cells on, each 256 units with impedance R_L/xc (complex for a capacitor)."""
    def f(sv):
        mm_ = m_cells * (1 + sv) / 2
        mc_ = m_cells * (1 - sv) / 2
        return mm_ * units / (1 + mm_ * xc) - mc_ * units / (1 + mc_ * xc)
    return f


xc16 = 1j * 2 * math.pi * 5e8 * ccell * 25
v.assert_true("full capacitive-cell harmonic analysis within 0.3 dB of -70 dBc",
              abs(hd_complex(cell_dac_diff(xc16), 3) + 70) < 0.3)

# ------------------------------------------------------------------ lab Part 5: DWA shaping (deterministic)
print("Lab")
M = 16
elem = 1 + 0.02 * (np.arange(M) / (M - 1) - 0.5)
nn, mm = 4096, 41
codes = np.round(8 + 7.5 * np.sin(2 * np.pi * mm * np.arange(nn) / nn)).astype(int)
fixed = np.array([elem[:c].sum() for c in codes])
p, rot = 0, []
for c in codes:
    rot.append(sum(elem[(p + i) % M] for i in range(c)))
    p = (p + c) % M
rot = np.array(rot)
ref = codes * elem.mean()
k = np.arange(1, nn // 32 + 1)
basis = np.exp(-2j * np.pi * np.outer(k, np.arange(nn)) / nn)
sig_p = abs(np.sum((codes - codes.mean()) * np.exp(-2j * np.pi * mm * np.arange(nn) / nn))) ** 2
for key, y in (("Lab 20-09.a", fixed), ("Lab 20-09.b", rot)):
    v.check(key, 10 * lg(np.sum(np.abs(basis @ (y - ref)) ** 2) / sig_p))

sys.exit(v.finish())
