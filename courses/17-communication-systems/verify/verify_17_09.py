#!/usr/bin/env python3
"""Verify chapter 17-09 (wireless channels): text, examples, problems and lab answers.

Routes:
- free-space loss from Friis with exact c and from the P.525 form (R-282); the two-ray model from an exact
  field sum of direct and reflected rays, against the d^4 approximation;
- TR 38.901 UMi path loss and breakpoint from the published formulas (R-283), delay-spread medians (R-284);
- PDP moments directly; coherence bandwidth by root finding on the frequency correlation, and by Monte Carlo
  over random exponential-PDP channels;
- the Jakes autocorrelation by averaging over arrival angles, and by a simulated sum-of-sinusoids channel;
  level-crossing rate and fade duration by counting crossings in simulated fading;
- Rayleigh/Rician outage in closed form and by Monte Carlo; BER in fading by numerical integration of
  Q(sqrt(2 gamma)) against the exponential density, by simulation, and against the closed forms;
- NR slot timing from TS 38.211 (R-285).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, special
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "17-09-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import channels as ch  # noqa: E402

CH = ROOT / "chapters" / "17-09-wireless-channels.md"
v = Verifier.from_files("17-09", CH, ROOT / "solutions" / "17-09-solutions.md", LAB / "README.md")
rng = np.random.default_rng(1709)
c = 299_792_458.0
Q, Qi = norm.sf, norm.isf


def db(x):
    return 10 * math.log10(x)


def un(d):
    return 10 ** (d / 10)


def fs(f, d):
    return 20 * math.log10(4 * math.pi * d * f / c)


def umi(d2d, fc, nlos, hbs=10.0, hut=1.5):
    """Written out from TR 38.901 Table 7.4.1-1 (independent of the lab)."""
    d3 = math.sqrt(d2d**2 + (hbs - hut) ** 2)
    dbp = 4 * (hbs - 1) * (hut - 1) * fc * 1e9 / 3.0e8
    los = 32.4 + 21 * math.log10(d3) + 20 * math.log10(fc) if d2d <= dbp else 32.4 + 40 * math.log10(d3) + 20 * math.log10(fc) - 9.5 * math.log10(dbp**2 + (hbs - hut) ** 2)
    if not nlos:
        return los
    return max(los, 35.3 * math.log10(d3) + 22.4 + 21.3 * math.log10(fc) - 0.3 * (hut - 1.5))


def avg_ber(cond, gbar):
    """Average a conditional error rate over an exponential SNR distribution by quadrature."""
    # the conditional error rate is negligible beyond g = 100 (Q(sqrt(200)) ~ 1e-45), so integrate there only
    val, _ = integrate.quad(lambda g: cond(g) * math.exp(-g / gbar) / gbar, 0, 100, limit=400, epsabs=0, epsrel=1e-10)
    return val


def bpsk_awgn(g):
    return Q(math.sqrt(2 * g))


# ------------------------------------------------------------------ text
v.check("Txt 17-09.a", 20 * math.log10(4 * math.pi * 1e6 * 1e3 / c))
v.check("Txt 17-09.b", math.sqrt(3) / (2 * math.pi))
x05 = optimize.brentq(lambda x: special.j0(x) - 0.5, 0.5, 2.4, xtol=1e-14)
v.check("Txt 17-09.c", x05)
mu_umi = -0.18 * math.log10(1 + 3.5) - 7.28  # R-284
mu_uma = -6.47 - 0.134 * math.log10(6)  # R-284, fc floored at 6 GHz (note 6)
v.check("Txt 17-09.d", 10**mu_umi * 1e9)
v.check("Txt 17-09.e", 10**mu_uma * 1e9)
v.assert_true("delay-spread exponents -7.40 (UMi LOS, 3.5 GHz) and -6.57 (UMa NLOS)", abs(mu_umi + 7.40) < 0.005 and abs(mu_uma + 6.57) < 0.005)
fd389 = (120 / 3.6) * 3.5e9 / c
rho = 10 ** (-10 / 20)
v.check("Txt 17-09.f", math.sqrt(2 * math.pi) * fd389 * rho * math.exp(-rho**2))
v.check("Txt 17-09.g", 1e3 * (math.exp(rho**2) - 1) / (math.sqrt(2 * math.pi) * fd389 * rho))

# Friis aperture identity and the f^2 effect with fixed apertures
lam = c / 3.5e9
v.assert_true("Friis: Pt Gt/(4 pi d^2) x Gr lambda^2/(4 pi) = Pt Gt Gr (lambda/4 pi d)^2", abs((1 / (4 * math.pi * 100**2)) * lam**2 / (4 * math.pi) - (lam / (4 * math.pi * 100)) ** 2) < 1e-18)
v.assert_true("P.525 constant 32.4 is 32.45 rounded", abs(20 * math.log10(4 * math.pi * 1e9 / c) - 32.45) < 0.005)

# two-ray: exact field sum vs approximation; breakpoint; frequency independence beyond it
def two_ray_exact(d, ht, hr, f):
    k = 2 * math.pi * f / c
    d1, d2 = math.hypot(d, ht - hr), math.hypot(d, ht + hr)
    e = np.exp(-1j * k * d1) / d1 - np.exp(-1j * k * d2) / d2
    return -20 * math.log10(abs(e) * (c / f) / (4 * math.pi))


approx = lambda d, ht, hr: 40 * math.log10(d) - 20 * math.log10(ht) - 20 * math.log10(hr)  # noqa: E731
v.assert_true("two-ray: exact sum approaches 40 log d - 20 log(ht hr) far beyond the breakpoint (10 km, 3.5 GHz)", abs(two_ray_exact(1e4, 10, 1.5, 3.5e9) - approx(1e4, 10, 1.5)) < 0.1)
v.assert_true("two-ray: beyond the breakpoint the loss barely depends on frequency (2 vs 4 GHz at 20 km)", abs(two_ray_exact(2e4, 10, 1.5, 2e9) - two_ray_exact(2e4, 10, 1.5, 4e9)) < 0.2)
v.assert_true("two-ray: lab model equals the exact sum", abs(ch.two_ray_loss_db(3000, 10, 1.5, 3.5e9) - two_ray_exact(3000, 10, 1.5, 3.5e9)) < 1e-9)
v.assert_true("two-ray: path difference ~ 2 ht hr / d (d = 1 km)", abs((math.hypot(1000, 11.5) - math.hypot(1000, 8.5)) - 2 * 10 * 1.5 / 1000) < 1e-4)

# shadowing margin
v.assert_true("90% coverage margin is 1.28 sigma; 95% is 1.64 sigma", abs(Qi(0.1) - 1.28) < 0.005 and abs(Qi(0.05) - 1.64) < 0.005)
sh = rng.normal(0, 7.82, 200_000)
v.assert_true("Monte Carlo: 90% of shadowed users lie within the 10.02 dB margin", abs(np.mean(sh < 1.2816 * 7.82) - 0.9) < 0.003)

# exponential PDP: rms = mean = tau; correlation formula by integration
tau = 1e-6
mean_e, _ = integrate.quad(lambda t: t * math.exp(-t / tau) / tau, 0, 60 * tau)
m2_e, _ = integrate.quad(lambda t: t * t * math.exp(-t / tau) / tau, 0, 60 * tau)
v.assert_true("exponential PDP: mean and rms both equal tau", abs(mean_e - tau) < 1e-12 and abs(math.sqrt(m2_e - mean_e**2) - tau) < 1e-12)
dfx = 0.2 / tau
re_, _ = integrate.quad(lambda t: math.exp(-t / tau) / tau * math.cos(2 * math.pi * dfx * t), 0, 60 * tau, limit=200)
im_, _ = integrate.quad(lambda t: math.exp(-t / tau) / tau * math.sin(2 * math.pi * dfx * t), 0, 60 * tau, limit=200)
v.assert_true("exponential PDP: |R(df)| = 1/sqrt(1 + (2 pi df tau)^2) by integration", abs(math.hypot(re_, im_) - 1 / math.sqrt(1 + (2 * math.pi * dfx * tau) ** 2)) < 1e-9)

# Jakes: average over angles; Doppler spectrum is the density of fd cos(alpha)
a = np.linspace(0, 2 * np.pi, 200001)[:-1]
for dt in (0.3e-3, 1e-3):
    assert abs(np.mean(np.exp(1j * 2 * np.pi * 100 * dt * np.cos(a))).real - special.j0(2 * np.pi * 100 * dt)) < 1e-9
v.assert_true("Jakes: the angle average of exp(j 2 pi fd dt cos a) is J0(2 pi fd dt)", True)
v.assert_true("Doppler spectrum integrates to 1 over (-fd, fd)", abs(integrate.quad(lambda f: 1 / (math.pi * 100 * math.sqrt(1 - (f / 100) ** 2)), -100, 100, limit=200)[0] - 1) < 1e-6)
v.assert_true("coherence time 0.242/fd (J0 = 0.5)", abs(x05 / (2 * math.pi) - 0.242) < 0.0005)

# simulated Rayleigh fading: autocorrelation, level crossings, Rayleigh/Rician statistics
fs_rate, fd = 20_000.0, 100.0
h = np.concatenate([ch.rayleigh_sos(20_000, fd, fs_rate, rng, m=64) for _ in range(30)])
lag = int(round(0.002 * fs_rate))
acs = []
for k in range(30):
    seg = h[k * 20_000 : (k + 1) * 20_000]
    acs.append(np.mean(seg[:-lag] * np.conj(seg[lag:])).real / np.mean(np.abs(seg) ** 2))
v.assert_true("simulated fading: correlation at 2 ms within 0.05 of J0(2 pi fd 2 ms)", abs(np.mean(acs) - special.j0(2 * np.pi * fd * 0.002)) < 0.05)
env = np.abs(h) / math.sqrt(np.mean(np.abs(h) ** 2))
below = env < rho
crossings = np.sum(below[1:] & ~below[:-1]) / (len(h) / fs_rate)
v.assert_true(f"simulated fading: {crossings:.1f} fades/s below -10 dB vs formula {ch.lcr(rho, fd):.1f}", abs(crossings / ch.lcr(rho, fd) - 1) < 0.12)
v.assert_true("simulated fading: fraction of time below -10 dB = lcr x afd = 1 - e^-0.1", abs(np.mean(below) - (1 - math.exp(-0.1))) < 0.012 and abs(ch.lcr(rho, fd) * ch.afd(rho, fd) - (1 - math.exp(-0.1))) < 1e-12)
g = (rng.standard_normal(400_000) + 1j * rng.standard_normal(400_000)) / math.sqrt(2)
v.assert_true("Rayleigh: Monte Carlo outage at 10 dB margin matches 1 - e^-0.1", abs(np.mean(np.abs(g) ** 2 < 0.1) - (1 - math.exp(-0.1))) < 0.002)
K = 10.0
gr = math.sqrt(K / (K + 1)) + g / math.sqrt(K + 1)
v.assert_true("Rician K = 10: Monte Carlo outage at 10 dB margin matches the noncentral chi-square", abs(np.mean(np.abs(gr) ** 2 < 0.1) / ch.rician_outage(10, K) - 1) < 0.15)
v.assert_true("Rician: at tiny thresholds outage/Rayleigh -> (K + 1) e^-K", abs(ch.rician_outage(40, 4.0) / ch.rayleigh_outage(40) / (5 * math.exp(-4)) - 1) < 0.01)

# BER in fading by quadrature vs closed form; 1/(4 gbar); MRC asymptote
v.assert_true("Rayleigh BPSK: quadrature of Q(sqrt(2g)) e^(-g/gbar)/gbar equals 1/2 (1 - sqrt(gbar/(1+gbar))) at 0, 10, 30 dB", all(abs(avg_ber(bpsk_awgn, un(x)) / ch.ber_bpsk_rayleigh(un(x)) - 1) < 1e-6 for x in (0, 10, 30)))
v.assert_true("Rayleigh BPSK -> 1/(4 gbar) at 40 dB", abs(ch.ber_bpsk_rayleigh(un(40)) * 4 * un(40) - 1) < 1e-3)
v.assert_true("MRC: L = 2 tends to 3/(16 gbar^2) and L = 4 to 35/(4 gbar)^4", abs(ch.ber_bpsk_mrc(un(40), 2) / (3 / (16 * un(40) ** 2)) - 1) < 0.01 and abs(ch.ber_bpsk_mrc(un(40), 4) / (35 / (4 * un(40)) ** 4) - 1) < 0.02)
nb = 400_000
bits = rng.integers(0, 2, nb)
gains = (rng.standard_normal((2, nb)) + 1j * rng.standard_normal((2, nb))) / math.sqrt(2)
gbar = un(10)
noise = (rng.standard_normal((2, nb)) + 1j * rng.standard_normal((2, nb))) * math.sqrt(1 / (2 * gbar))
y = gains * (1 - 2 * bits) + noise
dec1 = np.real(np.conj(gains[0]) * y[0]) < 0
dec2 = np.real(np.sum(np.conj(gains) * y, axis=0)) < 0
v.assert_true("Monte Carlo at 10 dB: one branch and 2-branch MRC match the closed forms within 5%", abs(np.mean(dec1 != bits) / ch.ber_bpsk_rayleigh(gbar) - 1) < 0.05 and abs(np.mean(dec2 != bits) / ch.ber_bpsk_mrc(gbar, 2) - 1) < 0.08)

# ------------------------------------------------------------------ examples
v.check("Ex 17-09.1a", fs(2.4e9, 100))
v.check("Ex 17-09.1b", 32.4 + 20 * math.log10(2400) + 20 * math.log10(0.1))
v.check("Ex 17-09.1c", 20 - fs(2.4e9, 100))
v.check("Ex 17-09.1d", fs(12e9, 36e6))
v.assert_true("Example 1: lambda = 0.1249 m; lab Friis and P.525 agree", abs(c / 2.4e9 - 0.1249) < 5e-5 and abs(ch.fspl_db(2.4e9, 100) - fs(2.4e9, 100)) < 1e-12 and abs(ch.fspl_p525_db(2400, 0.1) - 80.00) < 0.005)
v.check("Ex 17-09.2a", 4 * 9 * 0.5 * 3.5e9 / 3.0e8)
v.check("Ex 17-09.2b", umi(100, 3.5, False))
v.check("Ex 17-09.2c", umi(100, 3.5, True))
v.check("Ex 17-09.2d", fs(3.5e9, math.hypot(100, 8.5)))
v.check("Ex 17-09.2e", Qi(0.1) * 4)
v.check("Ex 17-09.2f", Qi(0.1) * 7.82)
v.assert_true("Example 2: lab UMi functions agree; d3D = 100.36 m; NLOS - LOS = 19.3 dB", abs(ch.umi_los_db(100, 3.5) - umi(100, 3.5, False)) < 1e-12 and abs(ch.umi_nlos_db(100, 3.5) - umi(100, 3.5, True)) < 1e-12 and abs(math.hypot(100, 8.5) - 100.36) < 0.005 and abs(umi(100, 3.5, True) - umi(100, 3.5, False) - 19.3) < 0.05)
dl, pw = [0, 1e-6, 2e-6, 5e-6], [0, -3, -6, -10]
p = 10 ** (np.array(pw) / 10)
m1 = np.sum(p * dl) / p.sum()
m2 = np.sum(p * np.square(dl)) / p.sum()
v.check("Ex 17-09.3a", m1 * 1e6)
v.check("Ex 17-09.3b", math.sqrt(m2 - m1**2) * 1e6)
corr = lambda f: abs(np.sum(p * np.exp(2j * np.pi * f * np.array(dl)))) / p.sum()  # noqa: E731
grid = np.linspace(1, 600e3, 60000)
first = grid[np.argmax([corr(f) <= 0.5 for f in grid])]
bc = optimize.brentq(lambda f: corr(f) - 0.5, first - 20, first, xtol=1e-6)
v.check("Ex 17-09.3c", bc / 1e3)
v.check("Ex 17-09.3d", 1 / (5 * math.sqrt(m2 - m1**2)) / 1e3)
v.assert_true("Example 3: linear powers sum 1.852, mean square 2.163 us^2; lab agrees; 1 MHz is about 4 Bc", abs(p.sum() - 1.852) < 5e-4 and abs(m2 * 1e12 - 2.163) < 5e-4 and abs(ch.coherence_bandwidth(dl, pw) - bc) < 1 and round(1e6 / bc) == 4)
for key, (vkmh, f) in (("Ex 17-09.4a", (120, 3.5e9)), ("Ex 17-09.4d", (120, 28e9))):
    v.check(key, (vkmh / 3.6) * f / c)
v.check("Ex 17-09.4b", x05 / (2 * math.pi * fd389) * 1e3)
v.check("Ex 17-09.4c", x05 / (2 * math.pi * (3 / 3.6) * 3.5e9 / c) * 1e3)
v.check("Ex 17-09.4e", x05 / (2 * math.pi * (120 / 3.6) * 28e9 / c) * 1e6)
slot = lambda mu: 1e-3 / 2**mu  # noqa: E731  R-285: 2^mu slots per 1 ms subframe
v.assert_true("Example 4: NR slots of 0.5 ms (30 kHz) and 0.125 ms (120 kHz) bracket the coherence times; pedestrian Doppler 9.73 Hz", slot(1) == 0.5e-3 and slot(3) == 0.125e-3 and x05 / (2 * math.pi * fd389) > slot(1) and x05 / (2 * math.pi * (120 / 3.6) * 28e9 / c) < slot(3) and abs((3 / 3.6) * 3.5e9 / c - 9.73) < 0.005)
v.check("Ex 17-09.5a", 100 * (1 - math.exp(-0.1)))
v.check("Ex 17-09.5b", 100 * (1 - math.exp(-0.01)))
v.check("Ex 17-09.5c", 100 * (1 - math.exp(-0.001)))
v.check("Ex 17-09.5d", db(1 / -math.log(0.99)))
v.check("Ex 17-09.5e", ch.rician_outage(10, 10.0))
v.assert_true("Example 5: Rician outage more than 100x below Rayleigh", ch.rayleigh_outage(10) / ch.rician_outage(10, 10.0) > 100)
v.check("Ex 17-09.6a", avg_ber(bpsk_awgn, 100.0))
x6 = optimize.brentq(lambda x: avg_ber(bpsk_awgn, un(x)) - 1e-5, 30, 60, xtol=1e-10)
v.check("Ex 17-09.6b", x6)
v.check("Ex 17-09.6c", x6 - db(Qi(1e-5) ** 2 / 2))
v.check("Ex 17-09.6d", ch.required_db(lambda gg: ch.ber_bpsk_mrc(gg, 2), 1e-5))
v.check("Ex 17-09.6e", ch.required_db(lambda gg: ch.ber_bpsk_mrc(gg, 4), 1e-5))
v.assert_true("Example 6: savings 22.6 and 34.0 dB; L = 2 approximation 21.37 dB", abs(x6 - ch.required_db(lambda gg: ch.ber_bpsk_mrc(gg, 2), 1e-5) - 22.6) < 0.05 and abs(x6 - ch.required_db(lambda gg: ch.ber_bpsk_mrc(gg, 4), 1e-5) - 34.0) < 0.05 and abs(db(math.sqrt(3 / 16 / 1e-5)) - 21.37) < 0.005)

# MRC formula against numerical integration over the chi-square (Erlang) density for L = 2
erl = lambda gg, L, gb: gg ** (L - 1) * math.exp(-gg / gb) / (math.factorial(L - 1) * gb**L)  # noqa: E731
mrc2_num, _ = integrate.quad(lambda gg: bpsk_awgn(gg) * erl(gg, 2, un(15)), 0, 2000, limit=400, points=[un(15)])
v.assert_true("MRC L = 2 closed form equals integration over the Erlang density (15 dB)", abs(mrc2_num / ch.ber_bpsk_mrc(un(15), 2) - 1) < 1e-6)

# practitioner: radius and site count vs margin
v.assert_true("n = 3.5: 10 dB margin costs 1.9x radius, about 3.7x sites", abs(10 ** (10 / 35) - 1.93) < 0.005 and abs(10 ** (20 / 35) - 3.73) < 0.005)
v.assert_true("Q3 (concept check): 0.276/300 ns = 0.92 MHz", abs(math.sqrt(3) / (2 * math.pi * 300e-9) / 1e6 - 0.92) < 0.005)

# ------------------------------------------------------------------ problems
v.check("17-09.1a", fs(5.8e9, 1000))
v.check("17-09.1b", fs(60e9, 100))
v.check("17-09.2a", 23 + 25 + 15 - fs(28e9, 200))
v.assert_true("Problem 2: free-space loss 107.41 dB", abs(fs(28e9, 200) - 107.41) < 0.005)
A = 0.1
prf = lambda f: A * A / ((c / f) ** 2 * 1e4**2)  # noqa: E731
v.check("17-09.3a", db(prf(30e9) / prf(3e9)))
v.check("17-09.3b", db(4 * math.pi * A / (c / 30e9) ** 2))
v.assert_true("Problem 3: 4 pi A / lambda^2 = 12 584 at 30 GHz; 21.0 dBi at 3 GHz", abs(4 * math.pi * A / (c / 30e9) ** 2 - 12584) < 0.5 and abs(db(4 * math.pi * A / (c / 3e9) ** 2) - 21.0) < 0.05)
v.check("17-09.4a", 4 * 30 * 1.5 * 900e6 / c)
v.check("17-09.4b", approx(5000, 30, 1.5))
v.check("17-09.4c", fs(900e6, 5000))
v.assert_true("Problem 4: exact two-ray at 5 km is 114.94 dB; ground costs 9.4 dB", abs(two_ray_exact(5000, 30, 1.5, 900e6) - 114.94) < 0.005 and abs(approx(5000, 30, 1.5) - fs(900e6, 5000) - 9.4) < 0.05)
v.check("17-09.5a", 80 + 35 * math.log10(10))
v.check("17-09.5b", 100 * 10 ** ((125 - 80) / 35))
v.check("17-09.5c", 100 * 10 ** ((125 - 80 - 8 * Qi(0.1)) / 35))
v.check("17-09.6a", 4 * 9 * 0.5 * 28e9 / 3.0e8)
v.check("17-09.6b", umi(50, 28, False))
v.check("17-09.6c", umi(50, 28, True))
v.check("17-09.7a", ch.pdp_stats([0, 1e-6], [0, 0])[1] * 1e6)
v.check("17-09.7b", 1 / 1e-6 / 1e6)
v.check("17-09.7c", optimize.brentq(lambda f: abs(math.cos(math.pi * f * 1e-6)) - 0.5, 1e3, 4.9e5) / 1e3)
v.check("17-09.8a", math.sqrt(3) / (2 * math.pi * 50e-9) / 1e6)
v.check("17-09.8b", math.sqrt(1 / 0.81 - 1) / (2 * math.pi * 50e-9) / 1e6)
fd_ped = (5 / 3.6) * 5.8e9 / c
fd_train = (300 / 3.6) * 2.6e9 / c
v.check("17-09.9a", fd_ped)
v.check("17-09.9b", x05 / (2 * math.pi * fd_ped) * 1e3)
v.check("17-09.9c", fd_train)
v.check("17-09.9d", x05 / (2 * math.pi * fd_train) * 1e3)
v.check("17-09.10a", 100 * (1 - math.exp(-0.01)))
v.check("17-09.10b", math.sqrt(2 * math.pi) * 50 * 0.1 * math.exp(-0.01))
v.check("17-09.10c", 1e3 * (math.exp(0.01) - 1) / (math.sqrt(2 * math.pi) * 50 * 0.1))
sig = 1.0
mean_r, _ = integrate.quad(lambda r: r * r / sig**2 * math.exp(-r * r / (2 * sig**2)), 0, 40)
ms_r, _ = integrate.quad(lambda r: r**3 / sig**2 * math.exp(-r * r / (2 * sig**2)), 0, 40)
v.check("17-09.11a", mean_r / math.sqrt(ms_r))
v.check("17-09.11b", db(math.log(2)))
v.assert_true("Problem 11: mean sigma sqrt(pi/2), mean square 2 sigma^2", abs(mean_r - math.sqrt(math.pi / 2)) < 1e-9 and abs(ms_r - 2) < 1e-9)
v.check("17-09.12a", avg_ber(lambda gg: 0.5 * math.exp(-gg), 1000.0))
v.check("17-09.12b", avg_ber(bpsk_awgn, 1000.0))
v.assert_true("Problem 12: DPSK in Rayleigh is 1/(2(1 + gbar))", abs(avg_ber(lambda gg: 0.5 * math.exp(-gg), 1000.0) - 1 / (2 * 1001)) < 1e-12)
v.check("17-09.13a", 1 - math.exp(-0.1))
e2 = rng.exponential(1.0, (2, 400_000))
v.check("17-09.13b", (1 - math.exp(-0.1)) ** 2)
v.check("17-09.13c", 1 - math.exp(-0.1) * 1.1)
v.assert_true("Problem 13: Monte Carlo selection and MRC outages match", abs(np.mean(e2.max(axis=0) < 0.1) / (1 - math.exp(-0.1)) ** 2 - 1) < 0.05 and abs(np.mean(e2.sum(axis=0) < 0.1) / (1 - 1.1 * math.exp(-0.1)) - 1) < 0.07)
fd_hst = (500 / 3.6) * 3.5e9 / c
v.check("17-09.14a", fd_hst)
v.check("17-09.14b", 1e3 / (2 * fd_hst))
v.check("17-09.14c", math.floor((1 / (2 * fd_hst)) / (0.5e-3 / 14)))

# ------------------------------------------------------------------ lab
v.check("Lab 17-09.a", 4 * 10 * 1.5 * 3.5e9 / c)
v.check("Lab 17-09.b", norm.cdf(10 / 7.82))
v.check("Lab 17-09.c", math.sqrt(3) / (2 * math.pi * 100e-9) / 1e6)
# Monte Carlo check of part 3: random exponential-PDP channels
nch, npaths, tr = 2000, 200, 100e-9
taus = rng.exponential(tr, (nch, npaths))
gains3 = (rng.standard_normal((nch, npaths)) + 1j * rng.standard_normal((nch, npaths))) / math.sqrt(2 * npaths)
H0 = gains3.sum(axis=1)
Hd = (gains3 * np.exp(-2j * np.pi * 2.76e6 * taus)).sum(axis=1)
v.assert_true("Lab part 3: simulated channels decorrelate to 0.5 at 2.76 MHz (within 0.05)", abs(abs(np.mean(H0 * np.conj(Hd))) / np.mean(np.abs(H0) ** 2) - 0.5) < 0.05)
v.check("Lab 17-09.d", math.sqrt(2 * math.pi) * 100 * rho * math.exp(-rho**2))
v.check("Lab 17-09.e", 1e3 * (math.exp(rho**2) - 1) / (math.sqrt(2 * math.pi) * 100 * rho))
v.check("Lab 17-09.f", 100 * ch.rician_outage(10, 10**0.6))
v.check("Lab 17-09.g", ch.ber_bpsk_mrc(un(15), 2))
v.assert_true("Lab part 6: at 15 dB one branch gives 7.7e-3 and four about 1e-7", abs(ch.ber_bpsk_rayleigh(un(15)) - 7.7e-3) < 5e-5 and 0.5e-7 < ch.ber_bpsk_mrc(un(15), 4) < 2e-7)

sys.exit(v.finish())
