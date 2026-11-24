#!/usr/bin/env python3
"""Verify every number in chapter 20-12 (why analog does not scale like digital), its problems and its lab.

Independent routes:
- kT/C noise by numerical integration of the RC network's thermal-noise spectrum 4kTR/(1 + (2 pi f R C)^2)
  (the lab uses the closed form), and the stage power from the closed-loop pole of a gm-C model;
- closed-loop gain errors by solving the op-amp feedback equation directly;
- the two-step converter re-implemented with integer codes, its SNDR from an FFT (signal bin against all other
  non-DC bins) rather than the lab's least-squares fit;
- the level-1 cascode solved as a two-unknown nonlinear system with scipy.optimize.fsolve and differentiated by a
  central difference (the lab uses a one-dimensional root search); ngspice confirms it (run_spice).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "20-12-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import scaling as lab  # noqa: E402

v = Verifier.from_files("20-12", ROOT / "chapters" / "20-12-why-analog-does-not-scale.md",
                        ROOT / "solutions" / "20-12-solutions.md", LAB / "README.md")
KT = 1.380649e-23 * 300
lg = math.log10


def noise_var(c, r=1e3):
    """Integrated output noise variance of an RC low-pass (V^2), by quadrature in the variable u = 2 pi f R C."""
    val, _ = integrate.quad(lambda u: 1 / (1 + u * u), 0, np.inf)
    return 4 * KT * r * val / (2 * math.pi * r * c)


v.assert_true("kT/C independent of R (1 k vs 100 k)", abs(noise_var(1e-12, 1e3) / noise_var(1e-12, 1e5) - 1) < 1e-9)


def cap_for_snr(snr_db, amp):
    # SNR = (A^2/2)/noise_var(C), and noise_var is proportional to 1/C
    return (10 ** (snr_db / 10)) * noise_var(1.0) / (amp ** 2 / 2)


def stage_power(c, f, vdd, gmid, beta=1.0):
    # single-pole closed loop: pole at beta gm / C (rad/s) = 2 pi f
    gm = optimize.brentq(lambda g: beta * g / c - 2 * math.pi * f, 1e-9, 10.0)
    i = gm / gmid
    return gm, i, vdd * i


# ---- Example 20-12.1
s = 1.4
v.check("Ex 20-12.1a", 1 / s)
v.check("Ex 20-12.1b", 1 / s ** 3)
v.check("Ex 20-12.1c", 1 / s ** 2)
v.check("Ex 20-12.1d", s ** 2)
v.check("Ex 20-12.1e", s)
v.assert_true("lab constant_field agrees", abs(lab.constant_field(1.4)["energy"] - 1 / 1.4 ** 3) < 1e-12)

# ---- Example 20-12.2
res = {}
for vdd, keys in ((1.8, "abcd"), (0.8, "efgh")):
    amp = 0.8 * vdd / 2
    c = cap_for_snr(74, amp)
    gm, i, p = stage_power(c, 1e8, vdd, 15)
    res[vdd] = p
    v.check(f"Ex 20-12.2{keys[0]}", c * 1e12)
    v.check(f"Ex 20-12.2{keys[1]}", math.sqrt(noise_var(c)) * 1e6)
    v.check(f"Ex 20-12.2{keys[2]}", i * 1e6)
    v.check(f"Ex 20-12.2{keys[3]}", p * 1e6)
    v.assert_true(f"lab thermal_power agrees at {vdd} V", abs(lab.thermal_power(74, 1e8, vdd)[3] / p - 1) < 1e-6)
v.check("Ex 20-12.2i", res[0.8] / res[1.8])
v.check("Ex 20-12.2j", (0.8 / 1.8) ** 2)
v.assert_true("power ratio equals the supply ratio", abs(res[0.8] / res[1.8] - 1.8 / 0.8) < 1e-9)

# ---- Example 20-12.3
ai = 12 * 2.5
v.check("Ex 20-12.3a", ai)
v.check("Ex 20-12.3b", 20 * lg(ai))
v.check("Ex 20-12.3c", ai ** 2 / 2)
v.check("Ex 20-12.3d", 20 * lg(ai ** 2 / 2))
v.check("Ex 20-12.3e", 1.8 - 5 * 0.15)
v.check("Ex 20-12.3f", 0.8 - 5 * 0.15)
v.check("Ex 20-12.3g", (ai / 2) ** 2)
v.check("Ex 20-12.3h", 20 * lg((ai / 2) ** 2))
v.check("Ex 20-12.3i", 0.8 - 2 * 0.15)

# ---- Example 20-12.4 and the text
cox, avt, sig = 10e-15, 3.5e-3, 0.5e-3   # F/um^2, V um, V
v.check("Ex 20-12.4a", cox * avt ** 2 / sig ** 2 * 1e15)
v.check("Ex 20-12.4b", noise_var(1.0) / sig ** 2 * 1e15)
ratio = cox * avt ** 2 / noise_var(1.0)
v.check("Ex 20-12.4c", ratio)
v.check("Txt 20-12.b", ratio)
v.check("Ex 20-12.4d", 2 * cox * (avt / 2) ** 2 / sig ** 2 * 1e15)
v.check("Ex 20-12.4e", 2 * cox * (avt / 2) ** 2 / noise_var(1.0))


# ---- Example 20-12.5: closed-loop gain of a non-inverting x2 stage from the op-amp equation
def closed_loop_error(a0, beta):
    # vout = a0 (vin - beta vout)  ->  vout / vin = a0 / (1 + a0 beta); ideal 1/beta
    g = optimize.brentq(lambda x: x - a0 * (1 - beta * x), 0, 1 / beta)
    return 1 - g * beta


eps = closed_loop_error(30, 0.5)
v.check("Ex 20-12.5a", eps * 100)
a_need = optimize.brentq(lambda a: closed_loop_error(a, 0.5) - 1 / 4096, 10, 1e6)
v.check("Ex 20-12.5b", math.ceil(a_need))
v.check("Ex 20-12.5c", 20 * lg(a_need))
v.check("Ex 20-12.5d", (1 / 4096) / eps * 100)


def adc_int(x, e, e_hat):
    """Integer-code two-step ADC: 4-bit coarse, 8-bit fine on a residue scaled by (1 - e); output in fine LSBs."""
    d1 = (16 * x).astype(np.int64)
    r = (16 * x - d1) * (1 - e)
    d2 = np.minimum((r * 256).astype(np.int64), 255)
    return d1 * 256 + (d2 + 0.5) / (1 - e_hat)


def sndr_fft(y, k):
    spec = np.abs(np.fft.rfft(y - y.mean())) ** 2
    sig_p = spec[k]
    noise_p = spec[1:].sum() - sig_p
    return 10 * lg(sig_p / noise_p)


n, k = 8192, 1021
xin = 0.5 + 0.49 * np.sin(2 * np.pi * k * np.arange(n) / n)
v.check("Lab 20-12.d", sndr_fft(adc_int(xin, 0, 0), k))
v.check("Ex 20-12.5e", sndr_fft(adc_int(xin, 0.0625, 0), k))
v.check("Ex 20-12.5f", sndr_fft(adc_int(xin, 0.0625, 0.0625), k))
v.check("Lab 20-12.e", sndr_fft(adc_int(xin, 0.0625, 0.0625 * (1 - 0.0039)), k))
v.check("Ex 20-12.5g", sndr_fft(adc_int(xin, 0.0625, 0.0625 * 1.02), k))
v.assert_true("lab two_step_adc SNDR agrees with the FFT route within 0.05 dB",
              abs(lab.sndr(lab.two_step_adc(xin, 0.0625, 0.0625), xin) - sndr_fft(adc_int(xin, 0.0625, 0.0625), k)) < 0.05)

# ---- Lab: level-1 single and cascode sinks
KP, WL, VT0, LAM = 300e-6, 20.0, 0.4, 0.2


def ids(vgs, vds):
    vov = vgs - VT0
    if vov <= 0:
        return 0.0
    if vds >= vov:
        return KP * WL / 2 * vov ** 2 * (1 + LAM * vds)
    return KP * WL * (vov * vds - vds ** 2 / 2) * (1 + LAM * vds)


def casc_i(vout):
    def f(z):
        x, i_ua = z   # node voltage (V) and current (uA), scaled so both unknowns are of order 0.1-100
        return [ids(0.55, x) * 1e6 - i_ua, ids(0.75 - x, vout - x) * 1e6 - i_ua]
    sol = optimize.root(f, [0.2, 70.0], method="lm", tol=1e-15)
    return sol.x[1] * 1e-6


h = 1e-5
r_single = 2 * h / (ids(0.55, 0.6 + h) - ids(0.55, 0.6 - h))
r_c06 = 2 * h / (casc_i(0.6 + h) - casc_i(0.6 - h))
r_c03 = 2 * h / (casc_i(0.3 + h) - casc_i(0.3 - h))
v.check("Lab 20-12.a", r_single / 1e3)
v.check("Lab 20-12.b", r_c06 / 1e6)
v.check("Lab 20-12.c", r_c03 / 1e3)
v.check("Txt 20-12.a", r_c06 / r_single)
v.assert_true("lab cascode_current agrees with fsolve", abs(lab.cascode_current(0.6)[0] / casc_i(0.6) - 1) < 1e-8)
v.check("Lab 20-12.f", (1 / 1.4 ** 3) ** 3 * 100)
v.check("Lab 20-12.g", 1.4 ** 3)

# ---- Problems
v.check("20-12.1a", 1 / 2)
v.check("20-12.1b", 1 / 8)
v.check("20-12.1c", 1 / 4)
v.check("20-12.1d", 4)
v.check("20-12.1e", 2)
v.check("20-12.2a", math.sqrt(noise_var(0.5e-12)) * 1e6)
v.check("20-12.2b", math.sqrt(noise_var(2e-12)) * 1e6)
c3 = cap_for_snr(80, 0.4)
v.check("20-12.3a", c3 * 1e12)
v.check("20-12.4a", stage_power(c3, 5e7, 1.0, 15, beta=0.5)[2] * 1e6)
v.check("20-12.5a", ((1.2 - 0.3) / (0.7 - 0.3)) ** 2)
v.check("20-12.5b", (1.2 / 0.7) ** 2)
for key, length in (("a", 0.1), ("c", 0.4)):
    g = lab.intrinsic_gain(10, 5 * length)
    v.check(f"20-12.6{key}", g)
    v.check(f"20-12.6{chr(ord(key) + 1)}", 20 * lg(g))
v.check("20-12.7a", 0.9 - 5 * 0.12)
v.check("20-12.7b", 0.9 - 4 * 0.12)
v.check("20-12.8a", 25e-15 * (1.5e-3) ** 2 / noise_var(1.0))
v.check("20-12.8b", 25 * (1.5 / 0.2) ** 2)
v.check("20-12.8c", noise_var(1.0) / (0.2e-3) ** 2 * 1e15)
a14 = optimize.brentq(lambda a: closed_loop_error(a, 0.5) - 2 ** -14, 10, 1e7)
v.check("20-12.9a", round(a14))
v.check("20-12.9b", 20 * lg(a14))
v.check("20-12.9c", 2 ** -14 / 0.02 * 100)
e_hot = closed_loop_error(24, 0.5)
resid = (e_hot - eps) / (1 - eps)
v.check("20-12.10a", e_hot * 100)
v.check("20-12.10b", resid * 100)
v.check("20-12.10c", resid * 4096)
# residual by direct simulation of the corrected gain: (1 - e_hot) / (1 - eps)
v.assert_true("residual equals 1 - (1 - e_hot)/(1 - eps)", abs(resid - (1 - (1 - e_hot) / (1 - eps))) < 1e-12)
v.check("20-12.11a", (0.7 / 1.2) * ((1.2 - 0.3) / (0.7 - 0.3)) ** 2)
v.check("20-12.12a", 0.9 / 0.75)
v.check("20-12.12b", 0.4 * 0.9 / 0.75 + 0.6 * 0.5 * (0.75 / 0.9) ** 2)

# ---- Text: practitioner arithmetic (sources in section 14)
v.check("Txt 20-12.c", 0.70 / 0.2884)          # IRDS 2024: V_dd 0.70 V, V_t,sat (HD) 288.4 mV
wafer = 16988 / 9346                             # CSET 2020 estimates, 5 nm over 7 nm
v.check("Txt 20-12.f", wafer)
v.check("Txt 20-12.d", wafer / 1.2)
v.check("Txt 20-12.e", wafer / 1.1)
v.check("Txt 20-12.g", -10 * lg(16 * KT) - 189.17)

sys.exit(v.finish())
