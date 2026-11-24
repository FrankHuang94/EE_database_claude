#!/usr/bin/env python3
"""Verify every number in chapter 21-05 (mixers), its problems and its lab.

Independent routes (the lab module mixer.py uses the closed forms and an FFT of the composite LO):
- conversion gains and harmonic responses are measured by multiplying sampled tones by a sampled square wave and
  reading the IF bin of an FFT;
- image rejection is measured by simulating a quadrature (Hartley) downconverter with gain and phase error on the
  Q path and comparing the wanted and image tones after the complex combination;
- noise folding is measured by Monte Carlo: white noise (optionally brick-wall filtered) times a square wave;
- harmonic-reject responses come from the analytic sum of phase-shifted square-wave Fourier series;
- the N-path filter is simulated in the time domain with exact RC steps per sample;
- ngspice confirms the conversion gains, the 3rd-harmonic response and the 4-path centre loss (mixer.cir).
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "21-05-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import mixer as lab  # noqa: E402

v = Verifier.from_files("21-05", ROOT / "chapters" / "21-05-mixers.md", ROOT / "solutions" / "21-05-solutions.md",
                        LAB / "README.md")
lg = math.log10
db20 = lambda x: 20 * lg(x)  # noqa: E731
db10 = lambda x: 10 * lg(x)  # noqa: E731

# ---------------------------------------------------------------- sampled square-wave mixing
NS = 1 << 20                        # samples over one IF period (f_IF = 1 bin)
T = np.arange(NS) / NS              # time in units of the IF period
F_LO = 64                           # LO at 64 IF-cycles per window


def square(phase_deg=0.0, f=F_LO):
    return np.sign(np.cos(2 * np.pi * f * T - math.radians(phase_deg)))


def if_amp(x):
    return abs(np.fft.rfft(x)[1]) / NS * 2


def conv_gain(n):
    """Conversion gain for an input at n f_LO + f_IF (n = 1, 3, 5)."""
    rf = np.cos(2 * np.pi * (n * F_LO + 1) * T)
    return if_amp(rf * square())


for n, k in ((1, "Ex 21-05.1e"), (3, "Ex 21-05.1f"), (5, "Ex 21-05.1g")):
    v.check(k, db20(conv_gain(n)))
v.check("Txt 21-05.a", db20(conv_gain(1)) - db20(conv_gain(3)))
v.check("Txt 21-05.b", db20(conv_gain(1)) - db20(conv_gain(5)))
v.check("Ex 21-05.1a", 2.45 - 2.40)
v.check("Ex 21-05.1b", 2 * 2.40 - 2.45)
v.check("Ex 21-05.1c", 3 * 2.40 - 0.05)
v.check("Ex 21-05.1d", 3 * 2.40 + 0.05)
g1 = conv_gain(1)
v.check("Ex 21-05.2a", g1 * 0.02 * 500)
v.check("Ex 21-05.2b", db20(g1 * 0.02 * 500))
v.assert_true("lab conversion gains match the FFT", abs(lab.conversion_gain_db(3) - db20(conv_gain(3))) < 1e-3)


# ---------------------------------------------------------------- image rejection by simulation
def irr_sim(eps, theta_deg):
    """Hartley-style: I = x cos(wLO t), Q = (1+eps) x sin(wLO t + theta); y = I + j Q (complex IF);
    the wanted tone (above the LO) and the image (below) land at opposite IF frequencies."""
    resp = {}
    for side in (+1, -1):
        x = np.cos(2 * np.pi * (F_LO + side) * T)
        i = x * np.cos(2 * np.pi * F_LO * T)
        q = (1 + eps) * x * np.sin(2 * np.pi * F_LO * T + math.radians(theta_deg))
        spec = np.fft.fft(i + 1j * q) / NS
        resp[side] = abs(spec[-1])          # the wanted tone lands at -f_IF; the image's leakage into that bin
    return db20(resp[+1] / resp[-1])


v.check("Ex 21-05.3a", irr_sim(0.02, 2))
v.check("Ex 21-05.3b", db10(4 / (0.02 ** 2 + math.radians(2) ** 2)))
v.check("Ex 21-05.3c", optimize.brentq(lambda t: irr_sim(0.005, t) - 40, 0.1, 5, xtol=1e-9))
v.check("Txt 21-05.d", irr_sim(0.01, 1))
v.check("Txt 21-05.i", irr_sim(0.001, 0.1))
v.assert_true("lab IRR formula matches the simulation", abs(lab.irr_db(0.02, 2) - irr_sim(0.02, 2)) < 1e-6)

# ---------------------------------------------------------------- noise folding by Monte Carlo
rng = np.random.default_rng(2105)
gsig = conv_gain(1) ** 2


def folded_nf(trials=20, ns=1 << 16, f_lo=256, k_if=60):
    """SSB noise factor of a noiseless square-wave mixer, by Monte Carlo: white noise times a square wave, output
    power in IF bins 1..k_if, over the output power when only the signal band (input bins f_lo+1..f_lo+k_if)
    carries noise. Averaging over k_if bins and several trials keeps the scatter to a few percent."""
    t = np.arange(ns) / ns
    sq = np.sign(np.cos(2 * np.pi * f_lo * t))
    out = ref = 0.0
    for _ in range(trials):
        spec = np.fft.rfft(rng.normal(0, 1, ns))
        out += np.sum(abs(np.fft.rfft(np.fft.irfft(spec, ns) * sq)[1:k_if + 1]) ** 2)
        only = np.zeros_like(spec)
        only[f_lo + 1:f_lo + k_if + 1] = spec[f_lo + 1:f_lo + k_if + 1]
        ref += np.sum(abs(np.fft.rfft(np.fft.irfft(only, ns) * sq)[1:k_if + 1]) ** 2)
    return out / ref


# The ratio of two Monte Carlo powers scatters; check against the closed forms within a tolerance, and publish
# the closed forms (whose ingredients are measured above): output density = input density (s^2 = 1).
ff = folded_nf()
v.assert_true("Monte Carlo unfiltered SSB noise factor ~ pi^2/4", abs(ff / (math.pi ** 2 / 4) - 1) < 0.15, f"{ff}")
v.check("Ex 21-05.4a", db10(1 / gsig))
v.check("Ex 21-05.4b", db10(1 / (2 * gsig)))
# Parseval: the conversion powers of all bands sum to the mean of s^2 (= 1); the harmonics take the rest
harm = float(np.mean(square() ** 2)) - 2 * gsig
v.check("Ex 21-05.4c", harm)
v.check("Ex 21-05.4d", db10((gsig + harm) / gsig))
v.check("Txt 21-05.c", 2 * gsig)
v.check("Txt 21-05.f", db10(1 / gsig) - db10((gsig + harm) / gsig))
v.check("Lab 21-05.a", db10(ff))


# ---------------------------------------------------------------- cascades
def friis(stages):
    te, g = 0.0, 1.0
    for gdb, nfdb in stages:
        te += (10 ** (nfdb / 10) - 1) * 290 / g
        g *= 10 ** (gdb / 10)
    return db10(1 + te / 290)


v.check("Ex 21-05.5a", friis([(15, 1.5), (-6.9, 6.9), (20, 3)]))
v.check("Ex 21-05.5b", friis([(-6.9, 6.9), (20, 3)]))
v.check("Ex 21-05.6a", -2 * (15 + 20))
v.check("Ex 21-05.6b", -2 * (23 + 20))
v.check("Txt 21-05.g", 10 ** 1.7)


# ---------------------------------------------------------------- harmonic-reject LO, analytic Fourier sums
def hr(weights, n):
    """|n-th harmonic| / |fundamental| of sum_k w_k sign(cos(x - phi_k)); each square wave's n-th harmonic is
    (4/(n pi)) (-1)^((n-1)/2) e^{-j n phi_k}."""
    def h(m):
        return abs(sum(w * cmath.exp(-1j * m * math.radians(ph)) for ph, w in weights)) * 4 / (m * math.pi)
    return h(n) / h(1)


ideal = [(-45.0, 1.0), (0.0, math.sqrt(2)), (45.0, 1.0)]
v.check("Ex 21-05.7a", db20(hr(ideal, 7)))
werr = [(-45.0, 1.0), (0.0, math.sqrt(2) * 1.01), (45.0, 1.0)]
perr = [(-45.0, 1.0), (0.0, math.sqrt(2)), (46.0, 1.0)]
v.check("Ex 21-05.7b", db20(hr(werr, 3)))
v.check("Ex 21-05.7c", db20(hr(werr, 5)))
v.check("Ex 21-05.7d", db20(hr(perr, 3)))
v.check("Ex 21-05.7e", db20(hr(perr, 5)))
v.assert_true("ideal HR LO cancels the 3rd and 5th", hr(ideal, 3) < 1e-12 and hr(ideal, 5) < 1e-12)
v.assert_true("lab FFT of the composite LO agrees", abs(lab.composite_lo_harmonics(werr, nmax=3, npts=1 << 16)[3]
                                                         - hr(werr, 3)) < 1e-4)


# ---------------------------------------------------------------- N-path filter, time-domain simulation
def npath(n_paths, r, c, f_lo, f_in, periods, steps=200, last=2000):
    tt = 1 / f_lo
    dt = tt / steps
    t = np.arange(periods * steps) * dt
    vs = np.cos(2 * np.pi * f_in * t)
    k_of = ((np.arange(periods * steps) % steps) * n_paths // steps).astype(int)
    a = math.exp(-dt / (r * c))
    caps = np.zeros(n_paths)
    out = np.empty_like(vs)
    for i in range(len(vs)):
        k = k_of[i]
        caps[k] = vs[i] + (caps[k] - vs[i]) * a
        out[i] = caps[k]
    m = slice(len(vs) - last * steps, len(vs))
    return abs(2 * np.mean(out[m] * np.exp(-2j * np.pi * f_in * t[m])))


bw4 = 1 / (math.pi * 4 * 50 * 200e-12)
v.check("Ex 21-05.8a", bw4 / 1e6)
centre = npath(4, 50, 200e-12, 1e9, 1e9, 6000)
v.check("Ex 21-05.8b", -db20(centre))
v.check("Ex 21-05.8c", -db20(((8 / math.pi) * math.sin(math.pi / 8)) ** 2))
v.check("Txt 21-05.e", db20(((8 / math.pi) * math.sin(math.pi / 8)) ** 2))
v.check("Txt 21-05.h", 1e9 / bw4)
up = npath(4, 50, 200e-12, 1e9, 1e9 + bw4 / 2, 6000)
dn = npath(4, 50, 200e-12, 1e9, 1e9 - bw4 / 2, 6000)
v.check("Lab 21-05.b", db20(up / centre))
v.check("Lab 21-05.c", db20(dn / centre))

# ---------------------------------------------------------------- problems
v.check("21-05.1a", 5.80 + 0.10)
v.check("21-05.1b", 5.80 + 0.20)
uni = 0.5 + 0.5 * square()
g_single = if_amp(np.cos(2 * np.pi * (F_LO + 1) * T) * uni)
v.check("21-05.2a", db20(g_single))
v.check("21-05.2b", db20(g1) - db20(g_single))
v.check("21-05.3a", 10 ** (12 / 20) / (g1 * 400) * 1e3)
v.check("21-05.4a", irr_sim(0.03, 0.5))
v.check("21-05.4b", optimize.brentq(lambda e: irr_sim(e, 0.3) - 45, 1e-4, 0.05, xtol=1e-12) * 100)
v.check("21-05.5a", db10(1 / math.tan(math.radians(1)) ** 2))
v.check("21-05.5b", db10(4 / math.radians(2) ** 2))
v.check("21-05.6a", db10(2 * gsig / gsig))
v.check("21-05.6b", db10((2 * gsig + 2 * conv_gain(3) ** 2) / gsig))
v.check("21-05.7a", friis([(18, 1.2), (10, 12), (30, 20)]))
v.check("21-05.8a", -2 * (15 + 10))
v.check("21-05.8b", -10 + 70 / 2)
w2 = [(-45.0, 1.0), (0.0, math.sqrt(2) * 1.02), (45.0, 1.0)]
p2 = [(-45.0, 1.0), (0.0, math.sqrt(2)), (45.5, 1.0)]
v.check("21-05.9a", db20(hr(w2, 3)))
v.check("21-05.9b", db20(hr(w2, 5)))
v.check("21-05.9c", db20(0.02 / 6))
v.check("21-05.9d", db20(hr(p2, 3)))
v.check("21-05.9e", db20(hr(p2, 5)))
v.check("21-05.10a", 1 / (math.pi * 8 * 50 * 20e6) * 1e12)
v.check("21-05.10b", -db20(((8 / math.pi) * math.sin(math.pi / 8)) ** 2))
# 11: self-mixing DC by averaging the product of the leaked LO and the square wave (phase 0)
leak = 0.3e-3 * np.cos(2 * np.pi * F_LO * T)
dc = np.mean(leak * square())
sig_amp = math.sqrt(100 * 1e-12)
v.check("21-05.11a", dc * 1e3)
v.check("21-05.11b", sig_amp * 1e6)
v.check("21-05.11c", sig_amp * g1 * 1e6)
v.check("21-05.11d", db20(dc / (sig_amp * g1)))
v.check("21-05.11e", dc * 1e3)
v.check("21-05.12a", 800 / 3)
v.check("21-05.12b", 800 / 5)

sys.exit(v.finish())
