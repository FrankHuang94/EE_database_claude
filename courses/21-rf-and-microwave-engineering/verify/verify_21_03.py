#!/usr/bin/env python3
"""Verify every number in chapter 21-03 (noise figure and linearity), its problems and its lab.

Independent routes (the lab module rfnl.py uses the closed forms of the chapter):
- intercepts and compression are measured by two-tone and one-tone FFTs of the polynomial or device law, not
  taken from the closed forms; cascades are built as composed polynomials and measured the same way;
- noise figures are recomputed with noise temperatures (T_e = (F - 1) T0) and, for noise parameters, from the
  admittance form F = 1 + [Gu + Rn |Ys + Ycor|^2]/Gs; noise circles are checked by sampling points on them;
- the Y-factor is recomputed from hot and cold temperatures, and simulated with random noise;
- transistor harmonics come from modified Bessel functions and from FFTs of the exponential and tanh laws;
- ngspice confirms the harmonic and intermodulation levels of Example 4 (bjt_im.cir, run by run_spice).
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from numpy.polynomial import polynomial as P_
from scipy import optimize, special

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "21-03-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import rfnl as lab  # noqa: E402

v = Verifier.from_files("21-03", ROOT / "chapters" / "21-03-noise-figure-and-linearity.md",
                        ROOT / "solutions" / "21-03-solutions.md", LAB / "README.md")

KB, QE, T0 = 1.380649e-23, 1.602176634e-19, 290.0
lg = math.log10


def dbm(p_w):
    return 10 * lg(p_w / 1e-3)


def amp(p_dbm):                    # peak volts across 50 ohm
    return math.sqrt(100 * 1e-3 * 10 ** (p_dbm / 10))


def pw(a):                         # dBm of a peak amplitude across 50 ohm
    return dbm(a * a / 100)


FS, N, F1, F2 = 64e6, 6400, 9e6, 10e6
FREQ = np.fft.rfftfreq(N, 1 / FS)
T = np.arange(N) / FS


def spectrum(func, amps, freqs):
    x = sum(a * np.cos(2 * np.pi * f * T) for a, f in zip(amps, freqs))
    return np.abs(np.fft.rfft(func(x))) / N * 2


def line(sp, f):
    return sp[np.argmin(abs(FREQ - f))]


def two_tone_iip3(func, p_in):
    """IIP3 (dBm) from a two-tone FFT at p_in dBm per tone (50 ohm in and out)."""
    a = amp(p_in)
    sp = spectrum(func, [a, a], [F1, F2])
    return p_in + (pw(line(sp, F1)) - pw(line(sp, 2 * F1 - F2))) / 2


def cubic(g_db, iip3_dbm):
    """Voltage-domain cubic with power gain g_db and the given IIP3 (a3 opposite in sign to a1)."""
    a1 = 10 ** (g_db / 20)
    a3 = -4 / 3 * a1 / amp(iip3_dbm) ** 2
    return lambda x: a1 * x + a3 * x ** 3


# ---------------------------------------------------------------- text: kT0, constants
v.check("Txt 21-03.a", dbm(KB * T0))
c1db = 1 - 10 ** (-1 / 20)
v.check("Txt 21-03.b", c1db)
v.check("Txt 21-03.f", 4 / 3 * c1db)
# IIP3 - P1dB for a cubic: find the 1 dB point by a one-tone FFT sweep of y = x - x^3 (|a1/a3| = 1)
fund = lambda a: line(spectrum(lambda x: x - x ** 3, [a], [F1]), F1) / a  # noqa: E731
a1db_num = optimize.brentq(lambda a: 20 * lg(fund(a)) + 1, 0.05, 0.6, xtol=1e-12)
v.check("Txt 21-03.c", 20 * lg(math.sqrt(4 / 3) / a1db_num))
# Two-tone fundamental: gain a1 + (9/4) a3 A^2 against a1 + (3/4) a3 A^2 for one tone, found by root finding.
a_one = optimize.brentq(lambda aa: 20 * lg(1 - 0.75 * aa**2) + 1, 1e-4, 1.0)
a_two = optimize.brentq(lambda aa: 20 * lg(1 - 2.25 * aa**2) + 1, 1e-4, 0.66)
v.check("Txt 21-03.i", 20 * lg(a_one / a_two))
v.check("Txt 21-03.j", -96.1 + 10 * lg(273 / 24))

# ---------------------------------------------------------------- Example 1: two-tone arithmetic, checked by simulation
iip3_1 = -30 + (-12 + 72) / 2
v.check("Ex 21-03.1a", -12 + 30)
v.check("Ex 21-03.1b", iip3_1)
v.check("Ex 21-03.1c", iip3_1 + 18)
v.check("Ex 21-03.1d", -30 + (-12 + 60))
amp1 = cubic(18, 0.0)
v.assert_true("a cubic with G 18 dB and IIP3 0 dBm reproduces the -72 dBm IM3 at -30 dBm",
              abs(pw(line(spectrum(amp1, [amp(-30)] * 2, [F1, F2]), 2 * F1 - F2)) + 72) < 0.01)
sp40 = spectrum(amp1, [amp(-40)] * 2, [F1, F2])
v.check("Ex 21-03.1e", pw(line(sp40, 2 * F1 - F2)) - pw(line(sp40, F1)))
v.check("Ex 21-03.1f", pw(line(sp40, 2 * F1 - F2)))
v.check("Ex 21-03.1h", pw(line(sp40, F1)))
g1 = lambda a: line(spectrum(amp1, [a], [F1]), F1) / a  # noqa: E731
v.check("Ex 21-03.1g", pw(optimize.brentq(lambda a: 20 * lg(g1(a) / 10 ** 0.9) + 1, 0.01, 0.2, xtol=1e-12)))

# ---------------------------------------------------------------- Example 2: Y-factor from temperatures
def te_from_y(enr_db, y_db, tc):
    th = T0 * (10 ** (enr_db / 10) + 1)          # hot temperature as calibrated
    y = 10 ** (y_db / 10)
    return (th - y * tc) / (y - 1)


te12 = te_from_y(15.0, 13.5, T0)
f2 = 10 ** 0.8
te1 = te12 - (f2 - 1) * T0 / 100                # Friis in temperatures: Te12 = Te1 + Te2/G1
v.check("Ex 21-03.2a", 10 * lg(1 + te12 / T0))
v.check("Ex 21-03.2b", 10 * lg(1 + te1 / T0))
v.check("Ex 21-03.2c", te1)
te12c = te_from_y(15.0, 13.5, 300.0)
v.check("Ex 21-03.2d", 10 * lg(1 + te12c / T0))
v.check("Ex 21-03.2e", 10 * lg(1 + (te12c - (f2 - 1) * T0 / 100) / T0))
v.check("Ex 21-03.2f", 10 * lg(1 + te12 / T0) - 10 * lg(1 + te1 / T0))
v.check("Ex 21-03.2g", 10 * lg(1 + te1 / T0) - 10 * lg(1 + (te12c - (f2 - 1) * T0 / 100) / T0))
# Monte Carlo Y-factor: Gaussian noise of variance proportional to temperature, long averages
rng = np.random.default_rng(2103)
nsamp = 2_000_000
t_on, t_off = T0 * (10 ** 1.5 + 1) + te12, T0 + te12
p_on = np.mean(rng.normal(0, math.sqrt(t_on), nsamp) ** 2)
p_off = np.mean(rng.normal(0, math.sqrt(t_off), nsamp) ** 2)
v.assert_true("simulated Y-factor recovers the system noise figure within 0.05 dB",
              abs(10 * lg(10 ** 1.5 / (p_on / p_off - 1)) - 10 * lg(1 + te12 / T0)) < 0.05)

# ---------------------------------------------------------------- Example 3: noise parameters in admittance form
def f_admittance(gs_refl, fmin_db, rn, gopt_refl, z0=50.0):
    ys = (1 - gs_refl) / (1 + gs_refl) / z0
    yopt = (1 - gopt_refl) / (1 + gopt_refl) / z0
    return 10 ** (fmin_db / 10) + rn / ys.real * abs(ys - yopt) ** 2


P = lambda m, d: m * cmath.exp(1j * math.radians(d))  # noqa: E731


def edge(g, u):
    """Distance along the unit vector u from g to |Gamma| = 0.999 (the passive edge)."""
    b = (g * u.conjugate()).real
    return -b + math.sqrt(b * b - abs(g) ** 2 + 0.999 ** 2)

GOPT3 = P(0.45, 60)
nf0 = 10 * lg(f_admittance(0, 0.8, 8, GOPT3))
nfc = 10 * lg(f_admittance(P(0.6, -40), 0.8, 8, GOPT3))
v.check("Ex 21-03.3a", nf0)
v.check("Ex 21-03.3b", nfc)
v.check("Txt 21-03.d", nf0 - 0.8)
v.check("Txt 21-03.e", nfc - 0.8)
for nf_i, kc, kr in ((1.0, "Ex 21-03.3c", "Ex 21-03.3d"), (1.5, "Ex 21-03.3e", "Ex 21-03.3f")):
    # find the circle by searching along rays from Gamma_opt for the target noise figure
    pts = []
    for ang in np.linspace(0, 2 * np.pi, 72, endpoint=False):
        u = cmath.exp(1j * ang)
        r = optimize.brentq(lambda s: 10 * lg(f_admittance(GOPT3 + s * u, 0.8, 8, GOPT3)) - nf_i, 1e-6, edge(GOPT3, u))
        pts.append(GOPT3 + r * u)
    pts = np.array(pts)
    a_ls = np.column_stack([2 * pts.real, 2 * pts.imag, np.ones(len(pts))])
    sol = np.linalg.lstsq(a_ls, np.abs(pts) ** 2, rcond=None)[0]
    centre = complex(sol[0], sol[1])
    v.check(kc, abs(centre))
    v.check(kr, math.sqrt(sol[2] + abs(centre) ** 2))
    v.assert_true(f"{nf_i} dB circle centre lies on the line to Gamma_opt",
                  abs(cmath.phase(centre) - math.radians(60)) < 1e-6)

# ---------------------------------------------------------------- Example 4: bipolar transistor and differential pair
VT = KB * 300 / QE
v.check("Ex 21-03.4a", math.sqrt(8) * VT * 1e3)
v.check("Ex 21-03.4b", pw(math.sqrt(8) * VT))
x5 = 0.005 / VT
v.check("Ex 21-03.4c", x5 / 4 * 100)
v.check("Ex 21-03.4d", x5 ** 2 / 24 * 100)
v.check("Ex 21-03.4e", special.iv(2, x5) / special.iv(1, x5) * 100)
v.check("Ex 21-03.4f", special.iv(3, x5) / special.iv(1, x5) * 100)
sp_bjt = spectrum(lambda u: np.exp(u / VT), [0.005, 0.005], [F1, F2])
v.check("Ex 21-03.4g", 20 * lg(line(sp_bjt, 2 * F1 - F2) / line(sp_bjt, F1)))
v.check("Ex 21-03.4h", 20 * lg(x5 ** 2 / 8))
v.check("Ex 21-03.4i", 4 * VT * 1e3)
v.check("Ex 21-03.4j", pw(4 * VT))
v.check("Ex 21-03.4k", math.sqrt(c1db * 4 / 3 * 12) * VT * 1e3)
tanh_fund = lambda a: line(spectrum(lambda u: np.tanh(u / (2 * VT)), [a], [F1]), F1)  # noqa: E731
a1db_dp = optimize.brentq(lambda a: 20 * lg(tanh_fund(a) / (a / (2 * VT))) + 1, 0.01, 0.08, xtol=1e-13)
v.check("Ex 21-03.4l", a1db_dp * 1e3)
v.check("Ex 21-03.4m", pw(4 * VT) - pw(a1db_dp))
v.check("Ex 21-03.4p", 20 * lg(a1db_dp / (math.sqrt(c1db * 16) * VT)))
v.check("Ex 21-03.4q", 4 / math.sqrt(8))
sp_dp = spectrum(lambda u: np.tanh(u / (2 * VT)), [0.01, 0.01], [F1, F2])
v.check("Ex 21-03.4n", 20 * lg(line(sp_dp, 2 * F1 - F2) / line(sp_dp, F1)))
v.check("Ex 21-03.4o", 20 * lg((0.01 / VT) ** 2 / 16))
v.assert_true("lab tanh 1 dB point agrees with the FFT route", abs(2 * VT * lab.tanh_x1db() / a1db_dp - 1) < 1e-6)


# ---------------------------------------------------------------- Example 5: line-up by noise temperatures and composed cubics
def friis_t(stages):
    """stages: (gain dB, NF dB); cascade noise temperature referred to the input."""
    te, g = 0.0, 1.0
    for gdb, nfdb in stages:
        te += (10 ** (nfdb / 10) - 1) * T0 / g
        g *= 10 ** (gdb / 10)
    return 10 * lg(1 + te / T0)


def composed(stages):
    funcs = [cubic(g, i) for g, i in stages]

    def f(x):
        for fn in funcs:
            x = fn(x)
        return x
    return f


for glna, kn, ki in ((15, "Ex 21-03.5a", "Ex 21-03.5b"), (20, "Ex 21-03.5c", "Ex 21-03.5d")):
    v.check(kn, friis_t([(-2, 2), (glna, 1.2), (8, 10), (20, 15)]))
    v.check(ki, two_tone_iip3(composed([(-2, 40), (glna, -8), (8, 5), (20, 15)]), -60))
v.check("Ex 21-03.5e", friis_t([(-2, 2), (15, 1.2), (8, 10), (20, 15)]) - friis_t([(-2, 2), (20, 1.2), (8, 10), (20, 15)]))
v.check("Ex 21-03.5f", two_tone_iip3(composed([(-2, 40), (15, -8), (8, 5), (20, 15)]), -60)
        - two_tone_iip3(composed([(-2, 40), (20, -8), (8, 5), (20, 15)]), -60))
v.assert_true("lab cascade formulas match (Example 5)",
              abs(lab.cascade_iip3([(-2, 40), (15, -8), (8, 5), (20, 15)])
                  - two_tone_iip3(composed([(-2, 40), (15, -8), (8, 5), (20, 15)]), -60)) < 0.01
              and abs(lab.friis([(-2, 2), (15, 1.2), (8, 10), (20, 15)])
                      - friis_t([(-2, 2), (15, 1.2), (8, 10), (20, 15)])) < 1e-9)

# ---------------------------------------------------------------- Example 6: 3GPP reconstruction and SFDR
def sens_3gpp(nf, nrb, scs):
    return -174 + 10 * lg(nrb * 12 * scs) + nf - 1 + 2.5 - 3


v.check("Ex 21-03.6a", sens_3gpp(9, 25, 15e3))
v.check("Ex 21-03.6b", sens_3gpp(9, 52, 15e3))
v.check("Ex 21-03.6c", sens_3gpp(10, 273, 30e3))
for val, pub in ((sens_3gpp(9, 25, 15e3), -100.0), (sens_3gpp(9, 52, 15e3), -96.8), (sens_3gpp(10, 273, 30e3), -85.6)):
    v.assert_true(f"{val:.2f} rounds down to the published {pub}", math.floor(val * 10) / 10 == pub)
nf5 = friis_t([(-2, 2), (15, 1.2), (8, 10), (20, 15)])
iip3_5 = two_tone_iip3(composed([(-2, 40), (15, -8), (8, 5), (20, 15)]), -60)
floor6 = dbm(KB * T0 * 4.5e6) + nf5
v.check("Ex 21-03.6d", floor6)
# SFDR by solving 3 P - 2 IIP3 = N for P with brentq, then P - N
p_top = optimize.brentq(lambda p: 3 * p - 2 * iip3_5 - floor6, -150, 50)
v.check("Ex 21-03.6e", p_top - floor6)

# ---------------------------------------------------------------- Example 7: blocker compression by simulation; reciprocal mixing
def blocker_gain_change(iip3, p_b, p_w=-90.0):
    f = cubic(0, iip3)
    aw, ab = amp(p_w), amp(p_b)
    sp = spectrum(f, [aw, ab], [F1, F2])
    return 20 * lg(line(sp, F1) / aw)


v.check("Ex 21-03.7a", blocker_gain_change(-8, -25))
f_ch = np.linspace(0, 4.5e6, 4501)
n_rm = dbm(np.trapezoid(np.full(f_ch.size, 10 ** ((-25 - 140) / 10) * 1e-3), f_ch))
n_th = dbm(KB * T0 * 4.5e6 * 10 ** 0.9)
v.check("Ex 21-03.7b", n_rm)
v.check("Ex 21-03.7c", n_th)
v.check("Ex 21-03.7d", 10 * lg(10 ** (n_rm / 10) + 10 ** (n_th / 10)) - n_th)
lmax = optimize.brentq(lambda L: 10 * lg(10 ** ((-25 + L + 10 * lg(4.5e6)) / 10) + 10 ** (n_th / 10)) - n_th - 0.5,
                       -200, -100)
v.check("Ex 21-03.7e", lmax)
v.check("Txt 21-03.g", -20 + 50 / 2)
v.check("Txt 21-03.h", -2 * (5 + 30))

# ---------------------------------------------------------------- Problems
# 1, 2: arithmetic, then confirmed with polynomial simulations
v.check("21-03.1a", -5 + 25)
v.check("21-03.1b", -25 + (-5 + 63) / 2)
v.check("21-03.1c", -25 + (-5 + 63) / 2 + 20)
sp1 = spectrum(cubic(20, 4), [amp(-35)] * 2, [F1, F2])
v.check("21-03.1d", pw(line(sp1, 2 * F1 - F2)) - pw(line(sp1, F1)))
v.check("21-03.1e", pw(line(sp1, 2 * F1 - F2)))
v.check("21-03.2a", -30 + (-10 + 52))
a1_2 = 10.0
a2_2 = a1_2 / amp(12)
sp2 = spectrum(lambda x: a1_2 * x + a2_2 * x ** 2, [amp(-40)] * 2, [F1, F2])
v.check("21-03.2b", pw(line(sp2, F2 - F1)) - pw(line(sp2, F1)))
v.check("21-03.2c", pw(line(sp2, F2 - F1)))
# 3: Y-factor
te3 = te_from_y(6.0, 3.2, T0)
v.check("21-03.3a", 10 * lg(1 + te3 / T0))
v.check("21-03.3b", te3)
v.check("21-03.3c", 10 * lg((T0 * (10 ** 1.5 + 1) + te3) / (T0 + te3)))
# 4: polynomial by FFT
f4 = lambda x: 10 * x - 2 * x ** 3  # noqa: E731
g4 = lambda a: line(spectrum(f4, [a], [F1]), F1) / a  # noqa: E731
a1db4 = optimize.brentq(lambda a: 20 * lg(g4(a) / 10) + 1, 0.1, 1.5, xtol=1e-12)
v.check("21-03.4a", a1db4)
a_small = 0.01
sp4 = spectrum(f4, [a_small, a_small], [F1, F2])
v.check("21-03.4b", a_small * math.sqrt(line(sp4, F1) / line(sp4, 2 * F1 - F2)))
v.check("21-03.4c", 20 * lg(a_small * math.sqrt(line(sp4, F1) / line(sp4, 2 * F1 - F2)) / a1db4))
sp4h = spectrum(f4, [0.1], [F1])
v.check("21-03.4d", line(sp4h, 3 * F1) / line(sp4h, F1) * 100)
# 5: noise circles in admittance form
GOPT5 = P(0.5, 120)
nf5a = 10 * lg(f_admittance(0, 1.2, 20, GOPT5))
nf5b = 10 * lg(f_admittance(P(0.5, 90), 1.2, 20, GOPT5))
v.check("21-03.5a", nf5a)
v.check("21-03.5b", nf5b)
v.check("21-03.5g", nf5a - 1.2)
v.check("21-03.5h", nf5b - 1.2)
pts = []
for ang in np.linspace(0, 2 * np.pi, 72, endpoint=False):
    u = cmath.exp(1j * ang)
    r = optimize.brentq(lambda s: 10 * lg(f_admittance(GOPT5 + s * u, 1.2, 20, GOPT5)) - 2.0, 1e-6, edge(GOPT5, u))
    pts.append(GOPT5 + r * u)
pts = np.array(pts)
sol = np.linalg.lstsq(np.column_stack([2 * pts.real, 2 * pts.imag, np.ones(len(pts))]), np.abs(pts) ** 2, rcond=None)[0]
v.check("21-03.5c", abs(complex(sol[0], sol[1])))
v.check("21-03.5d", math.sqrt(sol[2] + sol[0] ** 2 + sol[1] ** 2))
zopt5 = 50 * (1 + GOPT5) / (1 - GOPT5)
v.check("21-03.5e", zopt5.real)
v.check("21-03.5f", zopt5.imag)
# 6: noise parameters by numerical minimization of the admittance form
en, iu, ycor = 0.5e-9, 2e-12, complex(2e-3, 10e-3)
rn6 = en ** 2 / (4 * KB * T0)
gu6 = iu ** 2 / (4 * KB * T0)


def f6(ys):
    return 1 + (gu6 + rn6 * abs(ys + ycor) ** 2) / ys.real


# search over ln(Gs) (keeps Gs > 0) and Bs in mS
res = optimize.minimize(lambda p: f6(complex(math.exp(p[0]), p[1] * 1e-3)), [math.log(0.01), 0.0],
                        method="Nelder-Mead", options={"xatol": 1e-11, "fatol": 1e-15, "maxiter": 20000})
yopt6 = complex(math.exp(res.x[0]), res.x[1] * 1e-3)
v.check("21-03.6a", rn6)
v.check("21-03.6b", gu6 * 1e3)
v.check("21-03.6c", yopt6.real * 1e3)
v.check("21-03.6d", yopt6.imag * 1e3)
v.check("21-03.6e", (1 / yopt6).real)
v.check("21-03.6f", (1 / yopt6).imag)
v.check("21-03.6g", 10 * lg(res.fun))
v.check("21-03.6h", 10 * lg(f6(complex(0.02, 0))))
_, _, yopt_lab, fmin_lab = lab.noise_params_from_en_in(en, iu, ycor)
v.assert_true("lab noise parameters match the numerical optimum", abs(yopt_lab - yopt6) < 1e-8 and abs(fmin_lab - res.fun) < 1e-10)
# 7: filter before or after the LNA
nf7a = friis_t([(-2.5, 2.5), (18, 1.0), (10, 9), (15, 12)])
ip7a = two_tone_iip3(composed([(18, -10), (10, 8), (15, 20)]), -60) + 2.5   # a linear 2.5 dB loss in front
nf7b = friis_t([(18, 1.0), (-2.5, 2.5), (10, 9), (15, 12)])
ip7b = two_tone_iip3(composed([(18, -10), (-2.5, 45), (10, 8), (15, 20)]), -60)
v.check("21-03.7a", nf7a)
v.check("21-03.7b", ip7a)
v.check("21-03.7c", nf7b)
v.check("21-03.7d", ip7b)
v.check("21-03.7e", nf7a - nf7b)
v.check("21-03.7f", ip7a - ip7b)
# 8: sensitivity
v.check("21-03.8a", -96.5 - dbm(KB * T0 * 1e6) - 10)
v.check("21-03.8b", dbm(KB * T0 * 1e6) + 6 + 10)
v.check("21-03.8c", -70 - (-96.5))
# 9: blocker desensitization by simulation, and the cubic model's own compression point by FFT
v.check("21-03.9a", blocker_gain_change(-5, -20))
pb1 = optimize.brentq(lambda p: blocker_gain_change(-5, p) + 1, -30, -10, xtol=1e-9)
g9 = lambda a: line(spectrum(cubic(0, -5), [a], [F1]), F1) / a  # noqa: E731
p1db9 = pw(optimize.brentq(lambda a: 20 * lg(g9(a)) + 1, 0.005, 0.1, xtol=1e-12))
v.check("21-03.9b", pb1)
v.check("21-03.9c", p1db9)
v.check("21-03.9d", p1db9 - pb1)
# 10: reciprocal mixing requirement
nth10 = dbm(KB * T0 * 18e6) + 6
v.check("21-03.10a", nth10)
allow10 = optimize.brentq(lambda n: 10 * lg(10 ** (n / 10) + 10 ** (nth10 / 10)) - nth10 - 1, -150, -80)
v.check("21-03.10b", allow10)
v.check("21-03.10c", allow10 + 40 - 10 * lg(18e6))
# 11: temperature
for tc, ka, kp in ((233.15, "21-03.11a", "21-03.11b"), (398.15, "21-03.11c", "21-03.11d")):
    vt = KB * tc / QE
    sp11 = spectrum(lambda u: np.exp(u / vt), [1e-4, 1e-4], [F1, F2])
    a_ip = 1e-4 * math.sqrt(line(sp11, F1) / line(sp11, 2 * F1 - F2))   # small-signal extrapolation
    v.check(ka, a_ip * 1e3)
    v.check(kp, pw(a_ip))
x2 = 0.002 / VT
v.check("21-03.11e", x2 / 4 * 100)
sp11h = spectrum(lambda u: np.exp(u / VT), [0.002], [F1])
v.check("21-03.11f", line(sp11h, 2 * F1) / line(sp11h, F1) * 100)
# 12: differential pair beyond the cubic
v.check("21-03.12a", a1db_dp / VT)
v.check("21-03.12b", math.sqrt(c1db * 16))
v.check("21-03.12c", 20 * lg((0.02 / VT) ** 2 / 16))
sp12 = spectrum(lambda u: np.tanh(u / (2 * VT)), [0.02, 0.02], [F1, F2])
v.check("21-03.12d", 20 * lg(line(sp12, 2 * F1 - F2) / line(sp12, F1)))
v.check("21-03.12e", 20 * lg((0.01 / VT) ** 2 / 16) - 20 * lg(line(sp_dp, 2 * F1 - F2) / line(sp_dp, F1)))
# 13: IIP2 from transmitter leakage
nth13 = dbm(KB * T0 * 4.5e6) + 9
v.check("21-03.13a", nth13)
v.check("21-03.13b", 2 * (23 - 50) - (nth13 - 10))
v.check("21-03.13c", 2 * (23 - 55) - (nth13 - 10))
# 14: composed polynomials measured by FFT
s1 = lambda x: 5 * x - 0.5 * x ** 3  # noqa: E731
v.check("21-03.14a", math.sqrt(4 / 3 * 5 / 0.5))
v.check("21-03.14b", math.sqrt(4 / 3 * 4 / 0.2))
for b3, kc, ka in ((-0.2, "21-03.14d", "21-03.14c"), (0.2, "21-03.14e", "21-03.14f")):
    comp = lambda x, b3=b3: 4 * s1(x) + b3 * s1(x) ** 3  # noqa: E731
    p1 = np.array([0.0, 5.0, 0.0, -0.5])        # stage 1, ascending powers
    pc = 4 * np.pad(p1, (0, 6)) + b3 * P_.polypow(p1, 3)   # composed polynomial by polynomial algebra
    v.check(kc, pc[3])
    sp14 = spectrum(comp, [1e-3, 1e-3], [F1, F2])
    v.check(ka, 1e-3 * math.sqrt(line(sp14, F1) / line(sp14, 2 * F1 - F2)))

# ---------------------------------------------------------------- lab README
y2 = 10 ** 1.35
v.check("Lab 21-03.a", 10 / math.log(10) * y2 / (y2 - 1) * 2 / math.sqrt(1e4))
# Monte Carlo of 2000 measurements with 10^4 samples per state
rng_lab = np.random.default_rng(21031)
t_on2, t_off2 = T0 * (10 ** 1.5 + 1) + te12, T0 + te12
nfs = []
for _ in range(2000):
    pon = np.mean(rng_lab.normal(0, math.sqrt(t_on2), 10_000) ** 2)
    poff = np.mean(rng_lab.normal(0, math.sqrt(t_off2), 10_000) ** 2)
    nfs.append(10 * lg(10 ** 1.5 / (pon / poff - 1)))
v.assert_true("simulated scatter within 10% of the prediction",
              abs(np.std(nfs) / (10 / math.log(10) * y2 / (y2 - 1) * 2 / 100) - 1) < 0.1, f"{np.std(nfs)}")
im_50 = pw(line(spectrum(amp1, [amp(-50)] * 2, [F1, F2]), 2 * F1 - F2))
im_40 = pw(line(spectrum(amp1, [amp(-40)] * 2, [F1, F2]), 2 * F1 - F2))
v.check("Lab 21-03.b", (im_40 - im_50) / 10)
for glna, kn, ki in ((10, "Lab 21-03.c", "Lab 21-03.d"), (25, "Lab 21-03.e", "Lab 21-03.f")):
    v.check(kn, friis_t([(-2, 2), (glna, 1.2), (8, 10), (20, 15)]))
    v.check(ki, two_tone_iip3(composed([(-2, 40), (glna, -8), (8, 5), (20, 15)]), -60))

# Lab README Part 3: pure cubic, two-tone fundamental gain a1 + (9/4) a3 A^2 (per-tone amplitude A), IIP3 = 0 dBm.
r1 = optimize.brentq(lambda r: 20 * math.log10(1 - 3 * r) + 1, 1e-6, 0.3)  # r = A^2 / A_IIP3^2
v.assert_true("lab: two-tone fundamental is 1 dB compressed near -14.4 dBm per tone", abs(10 * math.log10(r1) + 14.4) < 0.05)
v.assert_true("lab: two-tone fundamental nulls near -4.8 dBm per tone", abs(10 * math.log10(1 / 3) + 4.8) < 0.05)
r10 = 10 ** (-10 / 10)
iip3_est = -10 + ((-10 + 20 * math.log10(1 - 3 * r10)) - (3 * -10)) / 2
v.assert_true("lab: intercept extrapolated from -10 dBm is about -1.6 dBm", abs(iip3_est + 1.55) < 0.06, f"{iip3_est:.2f}")

sys.exit(v.finish())
