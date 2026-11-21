#!/usr/bin/env python3
"""Verify every number in chapter 18-06 (ADC, DAC and PWM), its problems and its lab.

Independent routes:
- quantization noise by numerical integration of the uniform error, SQNR and ENOB by direct arithmetic;
- settling by solving the RC charging equation for the half-LSB crossing (root finding, not the closed form);
- the multiplexed input with an external capacitor by iterating a period-by-period charge model to convergence
  (not the lab's closed-form fixed point), and by the average-current model;
- averaging by the normal distribution (exact rounding probabilities) and a Monte Carlo through the quantizer with
  its own generator and honest tolerances;
- PWM ripple by simulating the RC filter period by period to steady state, against the exact formula;
- ZOH droop and images from sin(x)/x; the lab's C arithmetic by compiling and running its host test.
"""
from __future__ import annotations

import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "18-06-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import mcuanalog as ma  # noqa: E402

v = Verifier.from_files("18-06", ROOT / "chapters" / "18-06-adc-dac-pwm.md",
                        ROOT / "solutions" / "18-06-solutions.md", LAB / "README.md")


def settle(r_total, c, bits, frac=0.5, v_step=1.0):
    """Time at which a full-scale step on an RC is within frac LSB, by root finding on the response."""
    tau = r_total * c
    target = v_step * frac / 2 ** bits
    return brentq(lambda t: v_step * math.exp(-t / tau) - target, 0, 100 * tau, xtol=1e-18)


def mux_iterate(v_in, r_s, c_ext, c_sh, f, v_other=0.0, n=200000, tol=1e-15):
    """Iterate: share charge with C_sh (at v_other), then recover through r_s for 1/f. Returns the sampled value."""
    x = v_in
    e = math.exp(-1 / (f * r_s * c_ext))
    for _ in range(n):
        s = (c_ext * x + c_sh * v_other) / (c_ext + c_sh)
        x_new = v_in + (s - v_in) * e
        if abs(x_new - x) < tol:
            x = x_new
            break
        x = x_new
    return (c_ext * x + c_sh * v_other) / (c_ext + c_sh)


def avg_current(v_in, r_s, c_sh, f, v_other=0.0):
    g = r_s * f * c_sh
    return (v_in - v_other) * g / (1 + g)


def pwm_steady_ripple(vh, d, period, tau, n=20000):
    """Simulate phase by phase until the period-to-period change vanishes; return max - min."""
    a, b = math.exp(-d * period / tau), math.exp(-(1 - d) * period / tau)
    lo = 0.0
    for _ in range(n):
        hi = vh + (lo - vh) * a
        lo_new = hi * b
        if abs(lo_new - lo) < 1e-16:
            break
        lo = lo_new
    return hi - lo


def sinc(x):
    return 1.0 if x == 0 else math.sin(math.pi * x) / (math.pi * x)


def db(x):
    return 20 * math.log10(x)


L12 = 3.3 / 4096

# ---------------------------------------------------------------- text
v.check("Txt 18-06.a", math.log(2 ** 13))
v.check("Txt 18-06.b", 1e9 * 3.3e-12 * (2 ** 13 - 1))
v.check("Txt 18-06.c", 1e-6 / (100e3 * 3.3e-12))
v.check("Txt 18-06.d", 0.01 * 4096)
v.check("Txt 18-06.e", sinc(0.25))
v.check("Txt 18-06.f", db(sinc(0.25)))
v.check("Txt 18-06.g", sinc(0.5))
v.check("Txt 18-06.h", db(sinc(0.5)))
v.check("Txt 18-06.i", 64e6 / 2 ** 16)
v.assert_true("6.02 dB per bit and 1.76 dB", abs(20 * math.log10(2) - 6.0206) < 1e-4
              and abs(10 * math.log10(1.5) - 1.7609) < 1e-4)
msq = quad(lambda e: e * e, -0.5, 0.5)[0]
v.assert_true("uniform rounding error has mean square q^2/12", abs(msq - 1 / 12) < 1e-12)
v.assert_true("PWM ripple formula matches simulation and its approximation for T << tau",
              abs(pwm_steady_ripple(1, 0.3, 1e-3, 1) - ma.pwm_ripple_exact(1, 0.3, 1e-3, 1)) < 1e-12
              and abs(ma.pwm_ripple_exact(1, 0.3, 1e-3, 1) / (0.3 * 0.7 * 1e-3) - 1) < 1e-3)
v.assert_true("10-bit PWM at 64 MHz: f_c bound 2 f_clk / (pi 4^N) = 38.9 Hz",
              abs(2 * 64e6 / (math.pi * 4 ** 10) - 38.86) < 0.01)
v.assert_true("ZOH image ratio sinc(1 - x)/sinc(x) = x/(1 - x)", abs(sinc(0.95) / sinc(0.05) - 0.05 / 0.95) < 1e-12)

# ---------------------------------------------------------------- Example 1
v.check("Ex 18-06.1a", 1e3 * L12)
v.check("Ex 18-06.1b", int(ma.adc_code(1.0, 3.3, 12)))
v.assert_true("1.000 V is 1241.2 LSB", abs(1.0 / L12 - 1241.2) < 0.05)
v.check("Ex 18-06.1c", 1e3 * L12 * math.sqrt(msq))
sqnr12 = 10 * math.log10((2 ** 12 * L12 / 2) ** 2 / 2 / (L12 ** 2 * msq))
v.check("Ex 18-06.1d", sqnr12)
v.assert_true("serialbus-free: lab sqnr_db agrees", abs(ma.sqnr_db(12) - sqnr12) < 1e-9)
v.check("Ex 18-06.1e", 6.0206 * 11.1 + 1.7609)

# ---------------------------------------------------------------- Example 2
v.check("Ex 18-06.2a", 1e9 * 550 * 3.3e-12)
v.check("Ex 18-06.2b", 1e9 * settle(550, 3.3e-12, 12))
rsm = brentq(lambda r: settle(r + 500, 3.3e-12, 12) - 62.5e-9, 0, 1e6, xtol=1e-9)
v.check("Ex 18-06.2c", rsm)
v.assert_true("lab rs_max agrees", abs(ma.rs_max(62.5e-9, 3.3e-12, 500, 12) - rsm) < 1e-6)
v.check("Ex 18-06.2d", 1e9 * settle(10500, 3.3e-12, 12))
v.assert_true("e^9 is about 2^13", abs(math.exp(9) / 2 ** 13 - 1) < 0.02)

# ---------------------------------------------------------------- Example 3
step = 3.3 * 3.3e-12 / (100e-9 + 3.3e-12)
v.check("Ex 18-06.3a", 1e3 * step)
v.assert_true("sharing step is about a quarter of half an LSB", 0.2 < step / (L12 / 2) < 0.3)
v.check("Ex 18-06.3b", 1e9 * 3.3e-12 * (2 ** 13 - 1))
v.check("Ex 18-06.3c", 1e-6 / (100e3 * 3.3e-12))
v.check("Ex 18-06.3d", 1e3 * avg_current(3.3, 10e3, 3.3e-12, 100e3))
s100 = mux_iterate(3.3, 10e3, 100e-9, 3.3e-12, 100e3)
v.check("Ex 18-06.3e", 1e3 * (3.3 - s100))
v.assert_true("lab closed form agrees with iteration", abs(ma.mux_equilibrium(3.3, 10e3, 100e-9, 3.3e-12, 100e3)[1] - s100) < 1e-9)
v.check("Ex 18-06.3f", (3.3 - s100) / L12)
s1k = mux_iterate(3.3, 10e3, 100e-9, 3.3e-12, 1e3)
v.check("Ex 18-06.3g", 1e3 * (3.3 - s1k))
v.assert_true("sanity: 3.3 pF x 3.3 V x 100 kHz x 10 kOhm is about 11 mV", abs(3.3e-12 * 3.3 * 1e5 * 1e4 - 10.89e-3) < 1e-5)
v.assert_true("average-current model within 1% at 100 kHz", abs(avg_current(3.3, 10e3, 3.3e-12, 100e3) / (3.3 - s100) - 1) < 0.01)

# ---------------------------------------------------------------- Example 4
v.check("Ex 18-06.4a", round(4096 * 10 / 20))
c33, c30 = round(4096 * 1.65 / 2.5), round(4096 * 1.5 / 2.5)
v.check("Ex 18-06.4b", c33)
v.check("Ex 18-06.4c", c30)
v.check("Ex 18-06.4d", c33 - c30)
v.assert_true("B = 3950 K gives -4.44 %/K at 25 C", abs(3950 / 298.15 ** 2 - 0.0444) < 5e-5)
sens = 4096 * 10e3 * 10e3 / (20e3) ** 2 * 0.0444
v.check("Ex 18-06.4e", sens)
v.check("Ex 18-06.4f", (c33 - c30) / sens)
vdd = 4096 * 1.20 / 1489
v.check("Ex 18-06.4g", vdd)
v.check("Ex 18-06.4h", 1e3 * vdd / 1489)
v.check("Ex 18-06.4i", 1e3 * 0.01 * vdd)
v.assert_true("9% supply change of 2703 codes is about 245", abs(0.0909 * 2703 - 245) < 1)

# ---------------------------------------------------------------- Example 5
v.check("Ex 18-06.5a", 0.8 / math.sqrt(16))
v.check("Ex 18-06.5b", 10 * math.log10(16) / 6.0206)
v.check("Ex 18-06.5c", 4e6 / 16 / 1e3)
v.check("Ex 18-06.5d", 4 ** 4)
v.check("Ex 18-06.5e", 4e6 / 256 / 1e3)
p_up = norm.sf(0.2 / 0.1)
v.check("Ex 18-06.5f", p_up)


def expected_code_offset(offset, sigma, kmax=8):
    """E[rounded(offset + noise)] for a code-centred input, noise N(0, sigma^2), in LSB."""
    return sum(k * (norm.cdf((k + 0.5 - offset) / sigma) - norm.cdf((k - 0.5 - offset) / sigma))
               for k in range(-kmax, kmax + 1))


bias01 = expected_code_offset(0.3, 0.1) - 0.3
v.check("Ex 18-06.5g", -bias01)
v.check("Ex 18-06.5h", 12.5 - 11.1)
rng = np.random.default_rng(180605)
codes = np.floor(1000.3 + rng.normal(0, 0.1, size=(2000, 64)) + 0.5).mean(axis=1)
v.assert_true("Monte Carlo: 0.1 LSB noise leaves the 0.277 LSB bias at M = 64",
              abs((1000.3 - codes.mean()) - (-bias01)) < 0.01, f"{1000.3 - codes.mean():.4f}")

# ---------------------------------------------------------------- Example 6
T10 = 1024 / 64e6
v.check("Ex 18-06.6a", 1e-3 / T10)
tau10 = 1024 * T10 / 4
v.check("Ex 18-06.6b", 1e3 * tau10)
v.check("Ex 18-06.6c", 1 / (2 * math.pi * tau10))
v.check("Ex 18-06.6d", 1e3 * settle(tau10, 1.0, 10))
v.check("Ex 18-06.6e", 1e3 * pwm_steady_ripple(3.3, 0.5, T10, tau10))
v.check("Ex 18-06.6f", 1e3 * 3.3 / 1024)
v.assert_true("R = 4.096 kOhm with 1 uF is the time constant", abs(4096 * 1e-6 - tau10) < 1e-15)
T8 = 256 / 64e6
tau8 = 256 * T8 / 4
v.assert_true("8-bit PWM is 250 kHz", abs(1 / T8 - 250e3) < 1e-6)
v.check("Ex 18-06.6g", 1e6 * tau8)
v.check("Ex 18-06.6h", 1 / (2 * math.pi * tau8))
v.check("Ex 18-06.6i", 1e3 * settle(tau8, 1.0, 8))
v.assert_true("two bits fewer, 16 times the bandwidth", abs(tau10 / tau8 - 16) < 1e-12)

# ---------------------------------------------------------------- Problem 1
L10 = 2.5 / 1024
v.check("18-06.1a", 1e3 * L10)
v.check("18-06.1b", int(ma.adc_code(1.8, 2.5, 10)))
v.check("18-06.1c", 512 * L10)
v.check("18-06.1d", 1e3 * L10 / 2)
v.check("18-06.1e", 10 * math.log10(1.5 * 4 ** 10))

# ---------------------------------------------------------------- Problem 2
v.check("18-06.2a", (54.0 - 1.7609) / 6.0206)
v.assert_true("8.68 rounds to the data sheet's 8.7", round((54.0 - 1.7609) / 6.0206, 1) == 8.7)
v.check("18-06.2b", (61.5 - 1.7609) / 6.0206)

# ---------------------------------------------------------------- Problem 3
ref = 0.005 * 4096
v.check("18-06.3a", ref)
v.check("18-06.3b", 2 + 3 + 2 + ref)
v.check("18-06.3c", 1e3 * (2 + 3 + 2 + ref) * L12)
rss = math.sqrt(2 ** 2 + 3 ** 2 + 2 ** 2 + ref ** 2)
v.check("18-06.3d", rss)
v.check("18-06.3e", 1e3 * rss * L12)
v.assert_true("converter errors add under half an LSB in quadrature", rss - ref < 0.5)

# ---------------------------------------------------------------- Problem 4
tc = 14 / 40e6
v.check("18-06.4a", 1e9 * tc)
v.check("18-06.4b", 1e-6 / (62.5e-9 + tc))
t10k = settle(10500, 3.3e-12, 12)
v.check("18-06.4c", 1e-6 / (t10k + tc))
v.assert_true("costs 38% of throughput", abs(1 - (62.5e-9 + tc) / (t10k + tc) - 0.38) < 0.005)

# ---------------------------------------------------------------- Problem 5
v.check("18-06.5a", 1e6 * 4.2 / 2e6)
v.check("18-06.5b", 1e6 * settle(500.5e3, 3.3e-12, 12))
leak = 50e-9 * 500e3
v.check("18-06.5c", 1e3 * leak)
v.check("18-06.5d", leak / L12)
v.check("18-06.5e", 100 * leak / 2.1)
v.check("18-06.5f", 1e3 * 500e3 * 100e-9)
v.check("18-06.5g", 1e6 * avg_current(2.1, 500e3, 3.3e-12, 10))
s5 = mux_iterate(2.1, 500e3, 100e-9, 3.3e-12, 10)
v.check("18-06.5h", 1e6 * (2.1 - s5))
v.assert_true("sharing step is 69 uV and the exact error about 0.1 LSB",
              abs(2.1 * 3.3e-12 / 100e-9 - 69.3e-6) < 0.1e-6 and abs((2.1 - s5) / L12 - 0.1) < 0.01)
v.assert_true("100k/100k divider cuts the leakage error tenfold", abs(50e-9 * 50e3 / leak - 0.1) < 1e-12)

# ---------------------------------------------------------------- Problem 6
v.check("18-06.6a", 1e3 * 2.8 * 3.3e-12 / (47e-9 + 3.3e-12))
v.assert_true("g = 0.003102", abs(4.7e3 * 200e3 * 3.3e-12 - 0.003102) < 1e-9)
v.check("18-06.6b", 1e3 * -avg_current(0.5, 4.7e3, 3.3e-12, 200e3, 3.3))
s6 = mux_iterate(0.5, 4.7e3, 47e-9, 3.3e-12, 200e3, 3.3)
v.check("18-06.6c", 1e3 * (s6 - 0.5))
v.assert_true("reading is high", s6 > 0.5)
v.check("18-06.6d", (s6 - 0.5) / L12)
v.check("18-06.6e", 1e3 * (mux_iterate(0.5, 4.7e3, 47e-9, 3.3e-12, 50e3, 3.3) - 0.5))


def mux_two_conversions(v_in, r_s, c_ext, c_sh, f_scan, v_other):
    """Two back-to-back conversions per scan (second discarded is the first here: we keep the second)."""
    x = v_in
    e = math.exp(-1 / (f_scan * r_s * c_ext))
    for _ in range(200000):
        s1 = (c_ext * x + c_sh * v_other) / (c_ext + c_sh)
        s2 = (c_ext * s1 + c_sh * s1) / (c_ext + c_sh)      # C_sh arrives at s1: no change
        x_new = v_in + (s2 - v_in) * e
        if abs(x_new - x) < 1e-15:
            break
        x = x_new
    return s2


v.assert_true("converting twice does not change the DC error with the capacitor",
              abs(mux_two_conversions(0.5, 4.7e3, 47e-9, 3.3e-12, 200e3, 3.3) - s6) < 1e-9)

# ---------------------------------------------------------------- Problem 7
vbg = 3.000 * 1652 / 4096
v.check("18-06.7a", vbg)
vdd7 = 4096 * vbg / 1502
v.check("18-06.7b", vdd7)
v.check("18-06.7c", vdd7 * 2000 / 4096)
v.check("18-06.7d", 1e3 * vdd7 / 1502)

# ---------------------------------------------------------------- Problem 8
v.check("18-06.8a", 4 ** 2)
v.check("18-06.8b", 1e6 / 16 / 1e3)
v.check("18-06.8c", 16 * 4095)
v.check("18-06.8d", math.ceil(math.log2(16 * 4095 + 1)))
v.check("18-06.8e", 256 * 4095)
v.check("18-06.8f", math.ceil(math.log2(256 * 4095 + 1)))
v.check("18-06.8g", math.sqrt(0.5 ** 2 - 0.1 ** 2))

# ---------------------------------------------------------------- Problem 9
v.check("18-06.9a", sinc(0.05))
v.check("18-06.9b", db(sinc(0.05)))
v.check("18-06.9c", 1e3 - 50)
img = sinc(0.95) / sinc(0.05)
v.check("18-06.9d", img)
v.check("18-06.9e", db(img))
need = (6.0206 * 12 + 1.7609) + db(img)
v.check("18-06.9f", need)
v.check("18-06.9g", 40 * math.log10(9.5))
v.check("18-06.9h", 60 * math.log10(9.5))
v.assert_true("second order fails, third order passes", 40 * math.log10(9.5) < need < 60 * math.log10(9.5))
t = np.linspace(0, 20e-6, 200001)
slope = np.max(np.abs(np.gradient(1.65 * np.sin(2 * np.pi * 50e3 * t), t)))
v.check("18-06.9i", slope / 1e6)
v.check("18-06.9j", 1e6 * 2)

# ---------------------------------------------------------------- Problem 10
T12 = 4096 / 80e6
v.check("18-06.10a", 1e-3 / T12)
v.check("18-06.10b", 1e6 * T12)
tau12 = 4096 * T12 / 4
v.check("18-06.10c", 1e3 * tau12)
v.check("18-06.10d", 1 / (2 * math.pi * tau12))
v.check("18-06.10e", 1e3 * settle(tau12, 1.0, 12))
v.check("18-06.10f", 4 / (2 * math.pi * tau12))
v.assert_true("ripple at tau12 is one LSB", abs(pwm_steady_ripple(3.3, 0.5, T12, tau12) / (3.3 / 4096) - 1) < 1e-3)

# ---------------------------------------------------------------- Problem 11
v.check("18-06.11a", 1e6 * 3.3 / 20e3)
rth = 10050 * 10000 / 20050
tau11 = rth * 100e-9
v.check("18-06.11b", 1e3 * tau11)
ts11 = settle(tau11, 1.0, 12)
v.check("18-06.11c", 1e3 * ts11)
vf = 3.3 * 10000 / 20050
q_est = 3.3 / 20050 * ts11 + 100e-9 * vf
v.check("18-06.11d", 1e6 * q_est)
# exact: integrate the GPIO current (V - v(t)) / (R_f + R_o) numerically
q_ex = quad(lambda tt: (3.3 - vf * (1 - math.exp(-tt / tau11))) / 10050, 0, ts11, epsabs=1e-16)[0]
v.check("18-06.11e", 1e6 * q_ex)
v.check("18-06.11f", 1e6 * q_ex / 1.0)
v.assert_true("about 200 times less than the permanent divider", abs((3.3 / 20e3) / q_ex - 200) < 1)
code11 = 4096 * 10000 / 20050
v.check("18-06.11g", 2048 - code11)
v.check("18-06.11h", (2048 - code11) / 45.5)
v.assert_true("thermistor current is the steady 164.6 uA", abs(3.3 / 20050 - 164.6e-6) < 0.05e-6)

# ---------------------------------------------------------------- Problem 12
ts12 = [max(62.5e-9, settle(r + 500, 3.3e-12, 12)) for r in (50, 5e3, 20e3, 100e3)]
for ident, t_s in zip(("18-06.12a", "18-06.12b", "18-06.12c", "18-06.12d"), ts12):
    v.check(ident, 1e9 * t_s)
scan = sum(ts12) + 4 * 350e-9
v.check("18-06.12e", 1e-3 / scan)
v.check("18-06.12f", 1e-3 / (4 * max(ts12) + 4 * 350e-9))
scan3 = sum(ts12[:3]) + 62.5e-9 + 4 * 350e-9
v.check("18-06.12g", 1e-3 / scan3)
s12 = mux_iterate(2.0, 100e3, 100e-9, 3.3e-12, 1 / scan3, 1.0)
v.check("18-06.12h", 1e3 * (2.0 - s12))
v.check("18-06.12i", (2.0 - s12) / L12)
v.assert_true("average-current estimate agrees", abs(avg_current(2.0, 100e3, 3.3e-12, 1 / scan3, 1.0) / (2.0 - s12) - 1) < 0.01)
v.assert_true("slow scan at 1 kHz: about 0.35 mV", abs(1e3 * (2.0 - mux_iterate(2.0, 100e3, 100e-9, 3.3e-12, 1e3, 1.0)) - 0.35) < 0.005)

# ---------------------------------------------------------------- lab
tau_l = 10500 * 3.3e-12
v.check("Lab 18-06.a", 4096 * math.exp(-62.5e-9 / tau_l))
v.check("Lab 18-06.b", 4096 * math.exp(-312e-9 / tau_l))
v.check("Lab 18-06.c", 1e3 * (3.3 - mux_iterate(3.3, 10e3, 100e-9, 3.3e-12, 10e3)))
v.check("Lab 18-06.d", -(expected_code_offset(0.3, 0.3) - 0.3))
rng2 = np.random.default_rng(180606)
c3 = np.floor(1000.3 + rng2.normal(0, 0.3, size=(4000, 256)) + 0.5).mean(axis=1)
v.assert_true("Monte Carlo bias with 0.3 LSB at M = 256 within 0.005 of theory",
              abs((1000.3 - c3.mean()) + (expected_code_offset(0.3, 0.3) - 0.3)) < 0.005)
c8 = np.floor(1000.3 + rng2.normal(0, 0.8, size=(4000, 16)) + 0.5).mean(axis=1)
v.assert_true("Monte Carlo: 0.8 LSB follows sigma_q/sqrt(M) within 5% at M = 16",
              abs(np.sqrt(np.mean((c8 - 1000.3) ** 2)) / (math.sqrt(0.64 + 1 / 12) / 4) - 1) < 0.05)
v.check("Lab 18-06.e", 1e3 * pwm_steady_ripple(3.3, 0.1, T10, tau10))
v.assert_true("2 pi f tau is 1608", abs(2 * math.pi / T10 * tau10 - 1608) < 1)


def two_stage_ripple(vh, period, tau, d=0.5, n_fine=4000):
    """Periodic steady state of two cascaded (buffered) RC stages, by matrix exponentials over each phase."""
    from scipy.linalg import expm
    A = np.array([[-1 / tau, 0.0], [1 / tau, -1 / tau]])
    B = np.array([1 / tau, 0.0])
    Ainv = np.linalg.inv(A)

    def step(x, u, dt):
        E = expm(A * dt)
        return E @ x + (E - np.eye(2)) @ Ainv @ B * u
    # x(T) = M x(0) + c  -> fixed point
    M = expm(A * (1 - d) * period) @ expm(A * d * period)
    c = step(step(np.zeros(2), vh, d * period), 0.0, (1 - d) * period)
    x = np.linalg.solve(np.eye(2) - M, c)
    ys = []
    for u, dur in ((vh, d * period), (0.0, (1 - d) * period)):
        for k in range(n_fine):
            ys.append(step(x, u, dur * k / n_fine)[1])
        x = step(x, u, dur)
    return max(ys) - min(ys)


r2 = two_stage_ripple(3.3, T10, tau10)
v.check("Lab 18-06.j", 1e6 * r2)
v.assert_true("two stages cut the ripple about 2000 times", abs(pwm_steady_ripple(3.3, 0.5, T10, tau10) / r2 / 2000 - 1) < 0.05)
v.assert_true("start-up from 0 V needs about 13.2 tau, 54 ms",
              abs(math.log(1.65 / 3e-6) - 13.2) < 0.05 and abs(math.log(1.65 / 3e-6) * tau10 - 54e-3) < 0.5e-3)
v.assert_true("4095 x 3300 x 1000 exceeds 2^32", 4095 * 3300 * 1000 > 2 ** 32)

cc = shutil.which("cc") or shutil.which("clang") or shutil.which("gcc")
if not cc:
    sys.exit("verify_18_06: a C compiler is required (see SETUP.md)")
with tempfile.TemporaryDirectory(prefix="v1806_") as td:
    subprocess.run([cc, "-std=c17", "-O1", "-o", f"{td}/t", str(LAB / "c" / "adcmath_test.c"), "-lm"],
                   check=True, capture_output=True, text=True)
    out = subprocess.run([f"{td}/t"], capture_output=True, text=True).stdout
v.assert_true("host C test passes", "TEST PASSED" in out, out)
vals = [int(x) for x in re.findall(r": (?:VDD |14-bit )?(\d+)", out)]
v.assert_true("C test printed four values", len(vals) == 4, out)
v.check("Lab 18-06.f", vals[0])
v.check("Lab 18-06.g", vals[1])
v.check("Lab 18-06.h", vals[2])
v.check("Lab 18-06.i", vals[3])
v.assert_true("C results match exact rounding", vals == [round(1241 * 3300e3 / 4096), round(4096 * 1200 / 1489),
                                                          math.floor((8 * 2047 + 8 * 2048) / 4 + 0.5),
                                                          math.floor((6 * 2047 + 10 * 2048) / 4 + 0.5)])

sys.exit(v.finish())
