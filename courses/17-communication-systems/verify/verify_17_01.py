#!/usr/bin/env python3
"""Verify chapter 17-01 (random processes and PSD): examples, text, problems and lab answers.

Routes:
- transforms of candidate autocorrelations by numerical quadrature (not the closed forms of the text);
- noise powers by integrating |H|^2 S over frequency, checked against closed forms and, for the RLC case,
  against equipartition; correlation coefficients by simulating the exact AR(1) sampled process;
- NRZ, half-sine and AMI spectra by Welch estimates of simulated symbol streams, and power fractions by quadrature;
- noise folding by summing the Lorentzian's aliases directly, compared with the AR(1) closed form and a Welch
  estimate of simulated samples;
- I/Q components by down-converting simulated bandpass noise (powers, zero-lag and lagged correlations, sign).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, signal, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "17-01-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import randproc as rp  # noqa: E402

CH = ROOT / "chapters" / "17-01-random-processes-and-psd.md"
v = Verifier.from_files("17-01", CH, ROOT / "solutions" / "17-01-solutions.md", LAB / "README.md")
K = 1.380649e-23
PI = math.pi
rng = np.random.default_rng(1701)


def ft_even(R, f, tmax):
    """Transform of an even real function by quadrature: 2 * int_0^tmax R(t) cos(2 pi f t) dt."""
    val, _ = integrate.quad(lambda t: R(t) * math.cos(2 * PI * f * t), 0, tmax, limit=400)
    return 2 * val


# ------------------------------------------------------------------------------------- Example 1
rect = lambda t: 1.0 if abs(t) <= 1 else 0.0  # noqa: E731
res = optimize.minimize_scalar(lambda f: ft_even(rect, f, 1.0), bounds=(0.5, 1.0), method="bounded",
                               options={"xatol": 1e-9})
v.check("Ex 17-01.1a", res.fun)
v.check("Ex 17-01.1b", res.x)
tri = lambda t: max(1 - abs(t), 0.0)  # noqa: E731
v.check("Ex 17-01.1c", tri(0))
v.check("Ex 17-01.1d", ft_even(tri, 0.0, 1.0))
v.assert_true("Ex1 triangle transform is non-negative",
              min(ft_even(tri, f, 1.0) for f in np.linspace(0, 5, 501)) > -1e-9)
rc = lambda t: math.exp(-abs(t)) - 0.5 * math.exp(-2 * abs(t))  # noqa: E731
v.check("Ex 17-01.1e", rc(0))
v.check("Ex 17-01.1f", ft_even(rc, 0.0, 60))
v.assert_true("Ex1 (c) transform is positive", min(ft_even(rc, f, 60) for f in np.linspace(0, 3, 301)) > 0)
rd = lambda t: math.exp(-(abs(t) - 1) ** 2)  # noqa: E731
v.check("Ex 17-01.1g", rd(0))
v.assert_true("Ex1 (d) violates |R| <= R(0)", rd(1) > rd(0))
v.assert_true("lab Bochner test agrees", rp.is_valid_autocorrelation(lambda t: (abs(t) <= 1).astype(float), 50) < -0.2
              and rp.is_valid_autocorrelation(lambda t: np.maximum(1 - abs(t), 0), 50) > -1e-6)

# ------------------------------------------------------------------------------------- Example 2
N0 = (10e-9) ** 2  # one-sided density = N0
fc = 1e6
RC = 1 / (2 * PI * fc)
v.check("Ex 17-01.2a", RC * 1e9)
pw = N0 * fc * integrate.quad(lambda u: 1 / (1 + u * u), 0, np.inf)[0]  # f = fc u
v.check("Ex 17-01.2b", math.sqrt(pw) * 1e6)
v.assert_true("Ex2 closed form N0/(4RC)", abs(pw - N0 / (4 * RC)) / pw < 1e-9)
# correlation coefficients by simulating the exact sampled process (step 10 ns)
x = rp.ou_samples(400000, 1.0, RC, 10e-9, rng)
rho10 = np.mean(x[10:] * x[:-10]) / np.mean(x * x)
v.check("Ex 17-01.2c", math.exp(-100e-9 / RC))
v.assert_true("Ex2 simulated correlation at 100 ns", abs(rho10 - math.exp(-100e-9 / RC)) < 0.02, f"{rho10:.4f}")
v.check("Ex 17-01.2d", math.exp(-1e-6 / RC))

# ------------------------------------------------------------------------------------- Example 3
R, L, C, T = 5.0, 1e-6, 1e-9, 300.0
f0 = 1 / (2 * PI * math.sqrt(L * C))
Q = math.sqrt(L / C) / R
v.check("Ex 17-01.3a", f0 / 1e6)
v.check("Ex 17-01.3b", Q)


def dens(f):
    w = 2 * PI * f
    return 4 * K * T * R / ((1 - w * w * L * C) ** 2 + (w * R * C) ** 2)


v.check("Ex 17-01.3c", math.sqrt(dens(f0)) * 1e9)
fpk = optimize.minimize_scalar(lambda f: -dens(f), bounds=(4.5e6, 5.5e6), method="bounded", options={"xatol": 1}).x
v.check("Ex 17-01.3f", fpk / 1e6)
edges = [0, f0 * 0.5, f0 * 0.9, f0 * 0.99, f0, f0 * 1.01, f0 * 1.1, f0 * 2, f0 * 10, f0 * 1e3, f0 * 1e5]
tot = sum(integrate.quad(dens, a, b, limit=500)[0] for a, b in zip(edges[:-1], edges[1:]))
v.check("Ex 17-01.3d", math.sqrt(tot) * 1e6)
v.assert_true("Ex3 equals kT/C", abs(tot - K * T / C) / tot < 1e-6)
v.check("Ex 17-01.3e", tot / dens(f0) / 1e6)
v.assert_true("Ex3 lab density matches", abs(rp.rlc_vc_density(f0, R, L, C, T) - dens(f0)) < 1e-30)

# ------------------------------------------------------------------------------------- Example 4 and text
A, Tb = 0.4, 1e-10
v.check("Ex 17-01.4a", A * A)
v.check("Ex 17-01.4b", 1 / Tb / 1e9)
frac = lambda k: integrate.quad(lambda u: np.sinc(u) ** 2, -k, k, limit=200)[0]  # noqa: E731
v.check("Ex 17-01.4c", frac(1))
v.check("Ex 17-01.4d", frac(0.5))
v.check("Txt 17-01.a", 100 * frac(1))
v.check("Txt 17-01.b", 100 * frac(0.5))
mu, var = 0.4, 0.16
v.check("Ex 17-01.4e", mu * mu / (mu * mu + var))
# simulated polar NRZ (normalized T = 1, 16 samples/bit) against A^2 T sinc^2(fT), main lobe away from the null
sps = 16
bits = rng.choice([-A, A], 100000)
wv = rp.pam_waveform(bits, sps)
f, G = signal.welch(wv, fs=sps, nperseg=2048, detrend=False)
sel = (f > 0.02) & (f < 0.8)
theory = 2 * A * A * np.sinc(f[sel]) ** 2
dev = np.sqrt(np.mean((G[sel] / theory - 1) ** 2))
v.assert_true("Ex4 Welch matches NRZ spectrum in the main lobe (rms deviation < 4%)", dev < 0.04, f"{dev:.3f}")

# ------------------------------------------------------------------------------------- Example 5
s2, Ts = 1e-6, 1e-6
for tc, ka, kr, kd in ((1e-7, "Ex 17-01.5a", "Ex 17-01.5b", "Ex 17-01.5c"), (1e-6, "Ex 17-01.5d", "Ex 17-01.5e", "Ex 17-01.5f")):
    a = math.exp(-Ts / tc)
    v.check(ka, a)
    # direct alias sum at DC (two-sided), compared with the unaliased two-sided density 2 s2 tc
    m = np.arange(-200000, 200001)
    alias = np.sum(2 * s2 * tc / (1 + (2 * PI * m / Ts * tc) ** 2))
    ratio = alias / (2 * s2 * tc)
    closed = (1 + a) / (1 - a) * Ts / (2 * tc)
    v.assert_true(f"Ex5 alias sum equals AR(1) closed form (tc={tc})", abs(ratio - closed) / closed < 1e-4)
    v.check(kr, closed)
    v.check(kd, 10 * math.log10(closed))
xs = rp.ou_samples(2 ** 18, s2, 1e-7, Ts, rng)
fw, Gw = signal.welch(xs, fs=1 / Ts, nperseg=1024, detrend=False)
v.assert_true("Ex5 Welch of samples shows the folded density", abs(np.mean(Gw[1:50]) / 2.0e-12 - 1) < 0.05,
              f"{np.mean(Gw[1:50]):.3e}")

# ------------------------------------------------------------------------------------- Example 6
N0b = K * 290
Pn = N0b * 20e6
v.check("Ex 17-01.6a", 10 * math.log10(Pn / 1e-3))
v.check("Ex 17-01.6b", -90 - 10 * math.log10(Pn / 1e-3))
fsb, fcb, Bb = 200e6, 40e6, 20e6
xb = rp.bandpass_noise(400000, fsb, fcb, Bb, 1.0, rng)
ib, qb = rp.iq_components(xb, fsb, fcb, Bb)
px = np.mean(xb ** 2)
v.assert_true("Ex6 I and Q powers equal the bandpass power", abs(np.mean(ib ** 2) / px - 1) < 0.02
              and abs(np.mean(qb ** 2) / px - 1) < 0.02)
v.assert_true("Ex6 zero-lag I/Q correlation below 0.01", abs(np.mean(ib * qb)) / np.mean(ib ** 2) < 0.01)

# ------------------------------------------------------------------------------------- Problems
v.check("17-01.1a", 0.5 + 0.01)
v.check("17-01.1b", 0.5 / 0.51)
v.check("17-01.1c", 1 / (2 * PI * 10e-6) / 1e3)
G2 = (4e-9) ** 2
v.check("17-01.2a", G2)
v.check("17-01.2b", G2 / 2)
v.check("17-01.2c", math.sqrt(integrate.quad(lambda f: G2, 1e4, 1e6)[0]) * 1e6)
# 4
r4 = lambda t: 1 - t * t if abs(t) <= 1 else 0.0  # noqa: E731
S4 = lambda f: ft_even(r4, f, 1.0)  # noqa: E731
z1 = optimize.brentq(S4, 0.6, 0.8, xtol=1e-12)
z2 = optimize.brentq(S4, 1.1, 1.3, xtol=1e-12)
v.check("17-01.4a", z1)
v.check("17-01.4b", z2)
v.check("17-01.4c", optimize.minimize_scalar(S4, bounds=(z1, z2), method="bounded").fun)
S4a = lambda f, a=2.0, f0_=3.0: ft_even(lambda t: math.exp(-a * abs(t)) * math.cos(2 * PI * f0_ * t), f, 40)  # noqa: E731
v.assert_true("P4a transform positive and matches formula",
              all(abs(S4a(f) - (2.0 / (4 + 4 * PI ** 2 * (f - 3) ** 2) + 2.0 / (4 + 4 * PI ** 2 * (f + 3) ** 2))) < 1e-6
                  for f in (0.0, 1.0, 3.0, 5.0)))
# 5
RC5 = 1e3 * 1e-9
v.check("17-01.5a", RC5 * 1e6)
BN5 = integrate.quad(lambda u: 1 / (1 + u * u), 0, np.inf)[0] / (2 * PI * RC5)  # f = u / (2 pi RC)
v.check("17-01.5b", BN5 / 1e3)
v.check("17-01.5c", math.sqrt(1e-14 * BN5) * 1e6)
v.check("17-01.5d", optimize.brentq(lambda t: math.exp(-t / RC5) - 0.01, 0, 1e-5) * 1e6)
# 6
b2 = integrate.quad(lambda x_: 1 / (1 + x_ ** 4), 0, np.inf)[0]
b1 = integrate.quad(lambda x_: 1 / (1 + x_ ** 2), 0, np.inf)[0]
v.check("17-01.6a", b2)
v.check("17-01.6b", b1)
v.check("17-01.6c", 100 * (1 - b2 / b1))
# 7
H7 = 1 / (1 + 1j)
v.check("17-01.7a", abs(H7) * 1e-6)
v.check("17-01.7b", math.degrees(np.angle(H7)))
# 8
a8 = -0.8
v.check("17-01.8a", 1 / (1 - a8 * a8))
v.check("17-01.8b", a8 / (1 - a8 * a8))
v.check("17-01.8c", 1 / abs(1 - a8) ** 2)
v.check("17-01.8d", 1 / abs(1 + a8) ** 2)
x8 = signal.lfilter([1], [1, -a8], rng.standard_normal(400000))
v.assert_true("P8 simulated R[1]", abs(np.mean(x8[1:] * x8[:-1]) - a8 / (1 - a8 * a8)) < 0.05)
# 9
T9, A9 = 40e-12, 0.3
v.check("17-01.9a", 1 / T9 / 1e9)
v.check("17-01.9b", 2 * A9 * A9 * T9)
v.check("17-01.9c", frac(0.5) * A9 * A9)
v.check("17-01.9d", 0.3 ** 2 / (0.3 ** 2 + 0.09))
# 10
B10, S10 = 5e6, 2e-17
v.check("17-01.10a", 1 / (2 * B10) * 1e9)
v.check("17-01.10b", 2 * S10 * B10)
Rs = lambda tau: 2 * S10 * B10 * np.sinc(2 * B10 * tau)  # noqa: E731
v.assert_true("P10 sinc zeros at 1/(2B)", all(abs(Rs(k / (2 * B10))) < 1e-25 for k in (1, 2, 3)))
v.check("17-01.10c", 2 * stats.norm.sf(3))
# 11
G11 = (5e-9) ** 2
tc11 = 1 / (2 * PI * 50e6)
tot11 = G11 * 50e6 * integrate.quad(lambda u: 1 / (1 + u * u), 0, np.inf)[0]  # f = 50 MHz u
v.check("17-01.11a", math.sqrt(tot11) * 1e6)
a11 = math.exp(-1e-7 / tc11)
r11 = (1 + a11) / (1 - a11) * 1e-7 / (2 * tc11)
v.check("17-01.11b", r11)
v.check("17-01.11c", 10 * math.log10(r11))
v.check("17-01.11d", math.sqrt(G11 * 50e6 * integrate.quad(lambda u: 1 / (1 + u * u), 0, 0.1)[0]) * 1e6)
# 12: half-sine pulse spectrum by numerical transform, T = 1
P12 = lambda f: abs(integrate.quad(lambda t: math.sin(PI * t) * math.cos(2 * PI * f * t), 0, 1)[0]  # noqa: E731
                    - 1j * integrate.quad(lambda t: math.sin(PI * t) * math.sin(2 * PI * f * t), 0, 1)[0])
null = optimize.minimize_scalar(P12, bounds=(1.3, 1.7), method="bounded", options={"xatol": 1e-9}).x
v.check("17-01.12a", null)
E12 = 0.5
inb = integrate.quad(lambda f: P12(f) ** 2, -1, 1, limit=200)[0]
v.check("17-01.12b", inb / E12)
v.check("17-01.12c", frac(1))
v.check("17-01.12d", P12(0.0) ** 2)
hs = rp.pam_waveform(rng.choice([-1.0, 1.0], 100000), sps, pulse="halfsine")
f12, G12 = signal.welch(hs, fs=sps, nperseg=2048, detrend=False)
sel = (f12 > 0.02) & (f12 < 1.2)
th12 = 2 * np.array([P12(ff) ** 2 for ff in f12[sel]])
v.assert_true("P12 Welch matches half-sine spectrum (rms deviation < 4%)", np.sqrt(np.mean((G12[sel] / th12 - 1) ** 2)) < 0.04)
# 13: simulate noise only above the carrier; R_IQ(tau) negative for tau > 0, peak |rho| 0.725 at 0.371/B
x13 = rp.bandpass_noise(600000, 200e6, 40e6 + 5e6, 10e6, 1.0, rng, ntaps=1201)
i13, q13 = rp.iq_components(x13, 200e6, 40e6, 40e6, ntaps=1201)
g = lambda xx: (1 - math.cos(xx)) / xx  # noqa: E731
ext = optimize.minimize_scalar(lambda xx: -g(xx), bounds=(1, 4), method="bounded", options={"xatol": 1e-10})
v.check("17-01.13a", -ext.fun)
v.check("17-01.13b", ext.x / (2 * PI))
lag = round(ext.x / (2 * PI) / 10e6 * 200e6)  # samples at 200 MS/s for B = 10 MHz
rho13 = np.mean(i13[lag:] * q13[:-lag]) / np.mean(i13 ** 2)
v.assert_true("P13 simulated correlation is negative, about -0.72", -0.78 < rho13 < -0.66, f"{rho13:.3f}")
v.assert_true("P13 zero-lag correlation vanishes", abs(np.mean(i13 * q13)) / np.mean(i13 ** 2) < 0.02)
# 14: AMI
bits14 = rng.integers(0, 2, 200000)
sign, ami = 1, np.zeros(len(bits14))
for k_, bt in enumerate(bits14):
    if bt:
        ami[k_] = sign
        sign = -sign
v.check("17-01.14a", np.mean(ami ** 2), tol=0.005)
v.check("17-01.14b", np.mean(ami[1:] * ami[:-1]), tol=0.005)
v.assert_true("P14 R_a[2] is zero", abs(np.mean(ami[2:] * ami[:-2])) < 0.005)
h14 = lambda u: np.sinc(u) ** 2 * np.sin(PI * u) ** 2  # noqa: E731
pk = optimize.minimize_scalar(lambda u: -h14(u), bounds=(0.1, 0.9), method="bounded", options={"xatol": 1e-10})
v.check("17-01.14c", pk.x)
v.check("17-01.14d", -pk.fun)
wa = rp.pam_waveform(ami, sps)
fa, Ga = signal.welch(wa, fs=sps, nperseg=2048, detrend=False)
sel = (fa > 0.1) & (fa < 0.9)
v.assert_true("P14 Welch matches AMI spectrum (rms deviation < 4%)", np.sqrt(np.mean((Ga[sel] / (2 * h14(fa[sel])) - 1) ** 2)) < 0.04)

# ------------------------------------------------------------------------------------- §9 analyzer corrections
_rg = np.random.default_rng(170109)
_I, _Q = _rg.standard_normal(2_000_000), _rg.standard_normal(2_000_000)
_env = np.sqrt(_I**2 + _Q**2)
_c_ray = -20 * math.log10(np.mean(_env) / math.sqrt(np.mean(_env**2)))
v.check("Txt 17-01.c", -20 * math.log10(math.sqrt(math.pi / 4)))
v.assert_true("simulated Rayleigh envelope mean/rms matches 1.05 dB", abs(_c_ray - 1.049) < 0.01, f"{_c_ray:.4f}")
_pw = _env**2
_c_log = 10 * math.log10(np.mean(_pw)) - np.mean(10 * np.log10(_pw))
v.check("Txt 17-01.d", 10 * math.log10(math.e) * np.euler_gamma)
v.assert_true("simulated log-average under-response matches 2.51 dB", abs(_c_log - 2.507) < 0.01, f"{_c_log:.4f}")
v.check("Txt 17-01.e", 10 * math.log10(1.056))                 # R-257: noise BW / RBW = 1.056
v.check("Txt 17-01.f", 10 * math.log10(math.e) * np.euler_gamma - 10 * math.log10(1.056))
_pfs = (0.5 / math.sqrt(2)) ** 2 / 100                         # 1.0 Vpp differential full scale into 100 ohm
v.check("Txt 17-01.g", 10 * math.log10(_pfs / 1e-3))
_kT0 = 10 * math.log10(K * 290 / 1e-3)
v.check("Txt 17-01.i", _kT0)
v.check("Txt 17-01.h", -152.0 + 10 * math.log10(_pfs / 1e-3) - _kT0)  # R-237: NSD -152.0 dBFS/Hz

# ------------------------------------------------------------------------------------- Lab
R50 = 50.0
d50 = lambda f: 4 * K * T * R50 / ((1 - (2 * PI * f) ** 2 * L * C) ** 2 + (2 * PI * f * R50 * C) ** 2)  # noqa: E731
tot50 = sum(integrate.quad(d50, a_, b_, limit=500)[0] for a_, b_ in zip(edges[:-1], edges[1:]))
v.check("Lab 17-01.a", math.sqrt(tot50) * 1e6)
Xens = np.array([rp.ou_samples(64, 1 / (1 - 0.81), -1 / math.log(0.9), 1.0, rng) for _ in range(4000)])
r1_ens = rp.autocorr_ensemble(Xens, 30, 1)[1]
r1_time = rp.autocorr_time(rp.ou_samples(400000, 1 / (1 - 0.81), -1 / math.log(0.9), 1.0, rng), 1)[1]
v.check("Lab 17-01.b", 0.9 / (1 - 0.81))
v.assert_true("Lab AR(1) ensemble and time averages agree with theory",
              abs(r1_ens / 4.7368 - 1) < 0.06 and abs(r1_time / 4.7368 - 1) < 0.03, f"{r1_ens:.3f} {r1_time:.3f}")

sys.exit(v.finish())
