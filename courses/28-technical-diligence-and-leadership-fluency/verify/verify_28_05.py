#!/usr/bin/env python3
"""Verify every number in chapter 28-05 (domain question banks II), its problems and its
lab.

Independent routes (the lab module uses closed forms):
- the Schreier ceiling by evaluating the figure at the 8kT*SNR power for several speeds
  and resolutions, and the floor from scipy's Boltzmann constant;
- jitter-limited SNR by Monte Carlo sampling of a jittered sine;
- class-B and Doherty efficiency by numerical integration of half-sine drain currents
  (Fourier fundamental and DC components) for the carrier and peaking devices;
- converter chains by explicit power flow from the load back to the source;
- yields and densities from first principles; battery charge counted event by event over
  a common period;
- the normal tail by numerical integration of the density, and the chi-square bound by
  root-finding on the distribution function.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants, integrate, optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "28-05-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import bankcheck as bc  # noqa: E402

v = Verifier.from_files(
    "28-05",
    ROOT / "chapters" / "28-05-question-banks-analog-rf-power-packaging-embedded.md",
    ROOT / "solutions" / "28-05-solutions.md",
    LAB / "README.md",
)
KB = constants.k
H_YR = 365.25 * 24


def schreier(sndr, bw, p):
    return sndr + 10 * np.log10(bw / p)


def floor_w(snr_db, fs, t=300.0):
    return 8 * KB * t * 10 ** (snr_db / 10) * fs


def jitter_snr_mc(f_in, sigma, n=400_000, seed=1):
    """SNR of a unit sine sampled with Gaussian timing error (Monte Carlo)."""
    rng = np.random.default_rng(seed)
    t = rng.uniform(0, 1 / f_in, n)
    err = np.sin(2 * np.pi * f_in * (t + rng.normal(0, sigma, n))) - np.sin(2 * np.pi * f_in * t)
    return 10 * np.log10(0.5 / np.mean(err ** 2))


def halfsine_dc_fund(peak):
    """DC and fundamental (cosine) amplitude of a half-sine current pulse train."""
    dc = integrate.quad(lambda th: max(peak * math.cos(th), 0.0), -math.pi, math.pi)[0] / (2 * math.pi)
    f1 = integrate.quad(lambda th: max(peak * math.cos(th), 0.0) * math.cos(th), -math.pi, math.pi)[0] / math.pi
    return dc, f1


def eff_b_numeric(a):
    """Class B at relative amplitude a: drain current peak a*Im, swing a*VDD (VDD = Im = 1)."""
    dc, f1 = halfsine_dc_fund(a)
    return 0.5 * a * f1 / dc


def eff_doherty_numeric(a):
    """Ideal symmetric Doherty with carrier and class-B-like peaking currents."""
    if a <= 0.5:
        dc_c, f1_c = halfsine_dc_fund(a)       # carrier current grows with a, sees 2x load
        p_out = 0.5 * (2 * a) * f1_c           # voltage reaches VDD at a = 1/2
        return p_out / dc_c
    dc_c, _ = halfsine_dc_fund(a)
    dc_p, _ = halfsine_dc_fund(2 * a - 1)      # peaking device turns on at a = 1/2
    p_out = 0.5 * a * a                         # full power: two devices at 1/4 each
    return p_out / (dc_c + dc_p)


def chain_flow(p_load, etas):
    p, losses = p_load, []
    for eta in reversed(etas):
        p_in = p / eta
        losses.insert(0, p_in - p)
        p = p_in
    return p, losses


def node_charge_uc(window, cpu_period, ua_per_mhz=101, sleep=2.21):
    """Charge in µC over a window (s), counted event by event."""
    q = sleep * window
    q += sum(ua_per_mhz * 32 * 0.002 for _ in range(int(round(window / cpu_period))))
    q += sum(5100 * 0.001 + 5300 * 0.001 for _ in range(int(round(window / 10))))
    return q


def ppm_tail(cpk):
    return integrate.quad(lambda z: math.exp(-z * z / 2) / math.sqrt(2 * math.pi), 3 * cpk, np.inf)[0] * 1e6


# --- Theory text ------------------------------------------------------------------------
v.check("Txt 28-05.1", 16 * KB * 300)
ceil = 10 * math.log10(1 / (16 * KB * 300))
v.check("Txt 28-05.2", ceil)
v.check("Txt 28-05.2b", 10 * math.log10(1 / (8 * 1.380649e-23 * 300)))
for snr, fs in ((60, 1e6), (90, 1e3), (40, 1e10)):
    v.assert_true(f"ceiling independent of SNR {snr} dB and fs {fs:g}",
                  abs(schreier(snr, fs / 2, floor_w(snr, fs)) - ceil) < 1e-9)
v.check("Txt 28-05.3", 100 * eff_b_numeric(1.0))
v.check("Txt 28-05.4", ppm_tail(1))
v.check("Txt 28-05.5", ppm_tail(2))
v.check("Txt 28-05.6", math.sqrt(29 / stats.chi2.ppf(0.05, 29)))
v.check("Txt 28-05.7", 100 * (1 - (1 / 0.91 - 1) / (1 / 0.90 - 1)))
v.check("Txt 28-05.8", 100 * (1 / 0.975 - 1))
v.check("Txt 28-05.9", 100 * (1 / 0.98 - 1))
v.check("Txt 28-05.10", 10 ** 0.3)
v.check("Txt 28-05.11", 10 ** 0.15)

# --- Example 28-05.1 -------------------------------------------------------------------
en = (66 - 1.76) / 6.02
v.check("Ex 28-05.1a", en)
v.check("Ex 28-05.1b", 0.020 / (1e9 * 2 ** en) * 1e15)
fom1 = schreier(66, 5e8, 0.020)
v.check("Ex 28-05.1c", fom1)
v.check("Ex 28-05.1c1", 173.3 - fom1)
fl = floor_w(66, 1e9)
v.check("Ex 28-05.1d", fl * 1e3)
v.check("Ex 28-05.1d1", 0.020 / fl)
v.check("Ex 28-05.1d2", ceil - fom1)
v.assert_true("Ex 1: gap to ceiling equals 10 log10 of the power ratio",
              abs((ceil - fom1) - 10 * math.log10(0.020 / fl)) < 1e-9)
v.check("Ex 28-05.1e", schreier(66, 5e8, 0.002))
v.assert_true("Ex 1: published 1 GS/s point recomputes to 173.3 dB",
              abs(schreier(68.2, 5e8, 0.0153) - 173.3) < 0.05)

# --- Example 28-05.2 -------------------------------------------------------------------
v.check("Ex 28-05.2a", 1e-3 / (2 * math.pi * 2e9) * 1e15)
sj = -20 * math.log10(2 * math.pi * 2e9 * 100e-15)
v.check("Ex 28-05.2b", sj)
v.assert_true("Ex 2: Monte Carlo jitter SNR within 0.1 dB", abs(jitter_snr_mc(2e9, 100e-15) - sj) < 0.1)
v.check("Ex 28-05.2c", -10 * math.log10(10 ** (-sj / 10) + 10 ** (-6.2)))
need = optimize.brentq(lambda s: -10 * math.log10(10 ** (-s / 10) + 10 ** (-6.2)) - 60, 60.01, 100)
v.check("Ex 28-05.2d", need)
v.check("Ex 28-05.2d1", 10 ** (-need / 20) / (2 * math.pi * 2e9) * 1e15)

# --- Example 28-05.3 -------------------------------------------------------------------
a8 = 10 ** (-8 / 20)
v.check("Ex 28-05.3a", 100 * eff_b_numeric(a8))
v.check("Ex 28-05.3b", 100 * eff_doherty_numeric(a8))
v.check("Ex 28-05.3c", 8 / 0.55)
v.check("Ex 28-05.3c1", 8 / 0.55 - 8)
v.check("Ex 28-05.3c2", 8 / 0.51)
v.check("Ex 28-05.3c3", 8 / 0.51 - 8)
v.assert_true("Ex 3: lab Doherty agrees", abs(bc.eff_doherty(8) - eff_doherty_numeric(a8)) < 1e-6)

# --- Example 28-05.4 -------------------------------------------------------------------
l975, l98 = 8000 / 0.975 - 8000, 8000 / 0.98 - 8000
v.check("Ex 28-05.4a", l975)
v.check("Ex 28-05.4a1", l98)
v.check("Ex 28-05.4a2", l975 - l98)
v.check("Ex 28-05.4a3", 100 * (l975 - l98) / l975)
IN3_L = (0.0254 ** 3) * 1000
v.check("Ex 28-05.4b", 8000 / 100)
v.check("Ex 28-05.4b1", 8000 / 100 * IN3_L)
v.check("Ex 28-05.4b2", 8000 / 32)
v.check("Ex 28-05.4b3", 8000 / 32 * IN3_L)
pin4, losses4 = chain_flow(1000, [0.975, 0.975, 0.90])
v.check("Ex 28-05.4c", 100 * 1000 / pin4)
v.check("Ex 28-05.4c1", pin4)
v.check("Ex 28-05.4c2", losses4[2])
v.check("Ex 28-05.4c3", losses4[1])
v.check("Ex 28-05.4c4", losses4[0])
v.assert_true("Ex 4: losses sum to input minus load", abs(sum(losses4) - (pin4 - 1000)) < 1e-9)

# --- Example 28-05.5 -------------------------------------------------------------------
dens = {p: (1000 / p) ** 2 for p in (130, 50, 9)}  # connections per mm^2: (1 mm / pitch)^2
v.check("Ex 28-05.5a", dens[130])
v.check("Ex 28-05.5a1", dens[50])
v.check("Ex 28-05.5a2", dens[9])
v.check("Ex 28-05.5a3", dens[9] / dens[130])
v.check("Ex 28-05.5b", (45 / 35) ** 2)
y5 = 0.99 * np.prod([0.995] * 8) * 0.98
v.check("Ex 28-05.5c", 100 * y5)
v.check("Ex 28-05.5c1", 100 * y5 / 0.98)
v.check("Ex 28-05.5d", 100 * 0.98 / (y5 / 0.98))
v.assert_true("Ex 5: required assembly yield exceeds 100%", 0.98 / (y5 / 0.98) > 1)

# --- Example 28-05.6 -------------------------------------------------------------------
q25 = node_charge_uc(10, 1)          # µC over 10 s
i25 = q25 / 10
v.check("Ex 28-05.6a", i25)
v.check("Ex 28-05.6a1", 225e3 / i25)  # mAh / µA = 1e3 h
v.check("Ex 28-05.6a2", 225e3 / i25 / H_YR)
i85 = node_charge_uc(10, 1, sleep=4.71) / 10
v.check("Ex 28-05.6b", i85)
v.check("Ex 28-05.6b1", 225e3 / i85 / H_YR)
iw = node_charge_uc(10, 1, ua_per_mhz=55) / 10
v.check("Ex 28-05.6c", iw)
v.check("Ex 28-05.6c1", 225e3 / iw / H_YR)
v.check("Ex 28-05.6c2", i25 / iw)
v.assert_true("Ex 6: lab model agrees",
              abs(bc.avg_current_ua(2.21, [(3232, 0.002, 1), (5100, 0.001, 10), (5300, 0.001, 10)]) - i25) < 1e-9)

# --- Problem 28-05.2 -------------------------------------------------------------------
en2 = (70 - 1.76) / 6.02
v.check("28-05.2a", en2)
v.check("28-05.2b", 0.15 / (250e6 * 2 ** en2) * 1e15)
f2 = schreier(70, 125e6, 0.15)
v.check("28-05.2c", f2)
v.check("28-05.2d", 181.5 - f2)
fl2 = floor_w(70, 250e6)
v.check("28-05.2e", fl2 * 1e3)
v.check("28-05.2f", 0.15 / fl2)

# --- Problem 28-05.3 -------------------------------------------------------------------
v.check("28-05.3a", 10 ** (-3.5) / (2 * math.pi * 4e8) * 1e15)
s1 = -20 * math.log10(2 * math.pi * 1e9 * 50e-15)
s3 = -20 * math.log10(2 * math.pi * 3e9 * 50e-15)
v.check("28-05.3b", s1)
v.check("28-05.3c", s3)
v.check("28-05.3d", s1 - s3)
v.assert_true("P3: Monte Carlo at 1 GHz, 50 fs within 0.1 dB", abs(jitter_snr_mc(1e9, 50e-15, seed=2) - s1) < 0.1)

# --- Problem 28-05.4 -------------------------------------------------------------------
c300 = schreier(60, 5e5, floor_w(60, 1e6, 300))
c358 = schreier(60, 5e5, floor_w(60, 1e6, 358.15))
v.check("28-05.4a", c300)
v.check("28-05.4b", c358)
v.check("28-05.4c", 193 - c300)
# 28-05.4d transcribes R-336's logged pair (202.96 dB on DR, 164.86 dB on SNDR); the paper's SNDR is not logged,
# so the difference (= DR - SNDR at equal power and bandwidth) cannot be recomputed from primary inputs here.
v.check("28-05.4d", 202.96 - 164.86)
v.check("28-05.4e", 10 * math.log10(1 / (8 * 1.380649e-23 * 300)) - 193)

# --- Problem 28-05.5 -------------------------------------------------------------------
v.check("28-05.5a", 100 * eff_b_numeric(0.5))
v.check("28-05.5b", 100 * eff_b_numeric(10 ** -0.5))
v.check("28-05.5c", 100 * eff_doherty_numeric(0.5))
v.check("28-05.5d", 100 * eff_doherty_numeric(10 ** -0.5))
v.check("28-05.5e", 5 / 0.45)
v.check("28-05.5f", 5 / 0.45 - 5)

# --- Problems 28-05.6 to 28-05.8 -----------------------------------------------------
v.check("28-05.6a", 10 * math.log10(0.035 ** 2))
v.check("28-05.6b", 10 * math.log10(0.025 ** 2))
v.check("28-05.6c", 100 * math.sqrt(10 ** (-38 / 10)))
v.check("28-05.7a", 3000 / 32)
v.check("28-05.7b", 8000 / 100)
v.check("28-05.7c", 3000 / 0.96 - 3000)
v.check("28-05.7d", 3000 / 0.975 - 3000)
pin8, losses8 = chain_flow(1200, [0.975, 0.97, 0.91])
v.check("28-05.8a", 100 * 1200 / pin8)
v.check("28-05.8b", pin8)
v.check("28-05.8c", pin8 - 1200)
v.check("28-05.8d", losses8[2])
v.check("28-05.8e", losses8[1])
v.check("28-05.8f", losses8[0])
v.assert_true("P8: lab chain agrees", abs(bc.chain(1200, [0.975, 0.97, 0.91])[1] - pin8) < 1e-9)

# --- Problems 28-05.9 to 28-05.11 ----------------------------------------------------
v.check("28-05.9a", (1000 / 6) ** 2 / (1000 / 9) ** 2)
v.check("28-05.9b", (1000 / 4.5) ** 2 / (1000 / 9) ** 2)
v.check("28-05.9c", 14000 / 1500)
v.check("28-05.9d", 100 * 0.99 * 0.995 ** 12 * 0.98)
ystack = optimize.brentq(lambda y: 0.99 * y ** 12 * 0.98 - 0.95, 0.9, 1.0)
v.check("28-05.9e", 100 * ystack)
v.check("28-05.10a", 35 + 1200 * 0.05)
v.check("28-05.10b", optimize.brentq(lambda p: 35 + p * 0.05 - 105, 0, 1e5))
i11 = node_charge_uc(10, 5) / 10
v.check("28-05.11a", i11)
v.check("28-05.11b", 225e3 / i11 / H_YR)
i11h = node_charge_uc(10, 5, sleep=4.71) / 10
v.check("28-05.11c", i11h)
v.check("28-05.11d", 225e3 / i11h / H_YR)

# --- Problem 28-05.12 -------------------------------------------------------------------
cpk_a = (4 - 1.5) / (3 * 0.4)
v.check("28-05.12a", cpk_a)
v.check("28-05.12b", ppm_tail(cpk_a))
cpk_b = (4 - 1.5) / (3 * 0.8)
v.check("28-05.12c", cpk_b)
v.check("28-05.12d", ppm_tail(cpk_b))
q = optimize.brentq(lambda x: stats.chi2.cdf(x, 29) - 0.05, 1, 60)
v.check("28-05.12e", q)
su = 0.4 * math.sqrt(29 / q)
v.check("28-05.12f", su)
v.check("28-05.12g", 2.5 / (3 * su))
v.assert_true("P12: lab bound agrees", abs(bc.sigma_upper(0.4, 30) - su) < 1e-9)
v.assert_true("P12: lab ppm agrees", abs(bc.ppm_beyond(cpk_b) - ppm_tail(cpk_b)) < 1e-6)

# --- Problem 28-05.13 identities ----------------------------------------------------
for a in (0.2, 0.5, 0.8, 1.0):
    v.assert_true(f"P13b: class B (pi/4)a at a={a}", abs(eff_b_numeric(a) - math.pi / 4 * a) < 1e-9)
for a in (0.1, 0.3, 0.45):
    v.assert_true(f"P13b: Doherty (pi/2)a below half amplitude, a={a}",
                  abs(eff_doherty_numeric(a) - math.pi / 2 * a) < 1e-9)
v.assert_true("P13c: chi-square interval covers sigma about 95% of the time",
              abs(np.mean([bc.sigma_upper(np.std(np.random.default_rng(k).normal(0, 1, 30), ddof=1), 30) >= 1
                           for k in range(4000)]) - 0.95) < 0.015)

# --- Lab ----------------------------------------------------------------------------------
v.check("Lab 28-05.a", schreier(66, 5e8, 0.005))
v.check("Lab 28-05.a1", schreier(68.2, 5e8, 0.0153))
v.check("Lab 28-05.b", optimize.brentq(lambda f: -20 * math.log10(2 * math.pi * f * 50e-15) - 60, 1e8, 1e11) / 1e9)
v.check("Lab 28-05.b1", -20 * math.log10(2 * math.pi * 2e9 * 50e-15))
a9 = 10 ** (-9 / 20)
v.check("Lab 28-05.c", 100 * eff_doherty_numeric(a9))
v.check("Lab 28-05.c1", 100 * eff_b_numeric(a9))
dip = optimize.minimize_scalar(lambda a: eff_doherty_numeric(a), bounds=(0.5, 1.0), method="bounded")
v.check("Lab 28-05.c2", 100 * dip.fun)
v.assert_true("Lab: the dip is at two-thirds amplitude", abs(dip.x - 2 / 3) < 1e-3)
i10 = node_charge_uc(10, 10) / 10
v.check("Lab 28-05.d", i10)
v.check("Lab 28-05.d1", 225e3 / i10 / H_YR)

sys.exit(v.finish())
