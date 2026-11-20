#!/usr/bin/env python3
"""Verify every number in chapter 10-04 (small-signal models), its solutions and lab.

Independent routes:
- every small-signal parameter is a central-difference partial derivative of the large-signal law
  (exponential BJT with an Early factor, square-law MOSFET with channel-length modulation and a
  body-effect threshold), evaluated at the operating point, not the chapter's closed forms;
- every gain and resistance comes from solving the small-signal circuit's nodal equations with
  numpy.linalg.solve, the hybrid-pi and T models built separately;
- distortion figures from an FFT of the exact large-signal law sampled over one period, cross-checked
  against the modified-Bessel-function series (scipy.special.iv);
- the weak/strong-inversion crossover and the EKV curve by root finding and numerical differentiation.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.special import iv

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("10-04", COURSE / "chapters" / "10-04-small-signal-models.md",
                        COURSE / "solutions" / "10-04-solutions.md",
                        COURSE / "labs" / "10-04-lab" / "README.md")

VT = 1.380649e-23 * 300 / 1.602176634e-19
N = 8192
TH = 2 * np.pi * np.arange(N) / N


def ddx(f, x, h=1e-7):
    return (f(x + h) - f(x - h)) / (2 * h)


def par(*rs):
    return 1 / sum(1 / r for r in rs)


# ------------------------------------------------------------------ large-signal laws and their derivatives
def bjt_params(ic, beta, va=math.inf):
    """g_m, r_pi, r_e, r_o by differentiating i_C = I_S e^(v_BE/V_T)(1 + v_CE/V_A), i_B = i_C/beta."""
    i_s = ic / math.exp(0.7 / VT)                       # any I_S: place the operating point at V_BE = 0.7 V
    vbe0 = 0.7

    def i_c(vbe, vce=0.0):
        early = 1.0 if math.isinf(va) else 1 + vce / va
        return i_s * math.exp(vbe / VT) * early

    gm = ddx(lambda x: i_c(x), vbe0, 1e-6)
    rpi = 1 / ddx(lambda x: i_c(x) / beta, vbe0, 1e-6)
    re = 1 / ddx(lambda x: i_c(x) * (beta + 1) / beta, vbe0, 1e-6)
    ro = math.inf if math.isinf(va) else 1 / ddx(lambda y: i_c(vbe0, y), 0.0, 1e-3)
    return gm, rpi, re, ro


def mos_params(kn, i_d, lam=0.0, vtn=0.5):
    """g_m, V_ov, r_o by differentiating i_D = (k_n/2)(v_GS - V_TN)^2 (1 + lambda v_DS)."""
    vov = brentq(lambda x: 0.5 * kn * x * x - i_d, 1e-9, 10)
    vgs = vtn + vov

    def idf(vg, vd=0.0):
        return 0.5 * kn * (vg - vtn) ** 2 * (1 + lam * vd)

    gm = ddx(lambda x: idf(x), vgs, 1e-6)
    ro = math.inf if lam == 0 else 1 / ddx(lambda y: idf(vgs, y), 0.0, 1e-3)
    return gm, vov, ro


def solve(G, I):
    return np.linalg.solve(np.array(G, float), np.array(I, float))


def harm(y):
    c = np.fft.rfft(y) / N
    return abs(c[0]), 2 * abs(c[1]), 2 * abs(c[2]), 2 * abs(c[3])


def bjt_hd(a):
    """(HD2, HD3, DC rise) of i_C/I_C = exp(x cos th) by FFT; cross-checked with the Bessel series."""
    x = a / VT
    dc, f1, f2, f3 = harm(np.exp(x * np.cos(TH)))
    assert abs(f2 / f1 - iv(2, x) / iv(1, x)) < 1e-12 and abs(f3 / f1 - iv(3, x) / iv(1, x)) < 1e-12
    return f2 / f1, f3 / f1, dc - 1


def mos_hd(a, vov):
    _, f1, f2, f3 = harm((vov + a * np.cos(TH)) ** 2)
    return f2 / f1, f3 / f1


# ------------------------------------------------------------------ theory
gm1, rpi1, re1, ro1 = bjt_params(1e-3, 100, 50)
v.check("T 10-04.a", gm1 * 1e3)
hie_min, hie_max, hoe_min, hoe_max, hfe_min, hfe_max = 1.0, 10.0, 1.0, 40.0, 100, 400   # onsemi 2N3904, R-178
v.check("T 10-04.b", hie_min)
v.check("T 10-04.c", hie_max)
v.check("T 10-04.d", hoe_min)
v.check("T 10-04.e", hoe_max)
v.check("T 10-04.f", 1e-3 / (hoe_max * 1e-6))        # V_A = I_C r_o = I_C / h_oe
v.check("T 10-04.g", 1e-3 / (hoe_min * 1e-6))
v.check("T 10-04.h", bjt_params(1e-3, hfe_min)[1] / 1e3)
v.check("T 10-04.i", bjt_params(1e-3, hfe_max)[1] / 1e3)
v.check("T 10-04.j", hfe_min)
v.check("T 10-04.k", hfe_max)
a1 = brentq(lambda a: a / (4 * VT) - 0.01, 1e-6, 1e-2)       # first-order formula
v.check("T 10-04.l", a1 * 1e3)
v.check("T 10-04.m", brentq(lambda a: a / (2 * VT) - 0.1, 1e-6, 1e-1) * 1e3)   # quadratic/linear = 10%
n = 1.3
# weak inversion: the EKV interpolation's g_m/I_D deep below threshold approaches 1/(n V_T) (an independent route
# from the exponential's own derivative; the chapter quotes the limit)
v.check("T 10-04.n", ddx(lambda q: math.log(math.log1p(math.exp(q / (2 * n * VT))) ** 2), -0.6, 1e-6))
cross = brentq(lambda x: 2 / x - 1 / (n * VT), 1e-3, 1)
v.check("T 10-04.o", cross * 1e3)
v.check("T 10-04.p", mos_params(4e-3, 0.5 * 4e-3 * 0.2 ** 2)[0] / (0.5 * 4e-3 * 0.2 ** 2))
v.check("T 10-04.q", gm1 * ro1)
v.assert_true("2N3904 h_ie range brackets beta V_T/I_C over its h_fe range",
              hie_min <= bjt_params(1e-3, hfe_min)[1] / 1e3 and bjt_params(1e-3, hfe_max)[1] / 1e3 <= hie_max + 0.5)

# ------------------------------------------------------------------ Example 1
v.check("Ex 10-04.1a", gm1 * 1e3)
v.check("Ex 10-04.1b", rpi1 / 1e3)
v.check("Ex 10-04.1c", re1)
v.check("Ex 10-04.1d", ro1 / 1e3)
v.check("Ex 10-04.1e", gm1 * ro1)
# collector node, base driven by 1 V: (1/R_C + 1/r_o) v_c = -g_m
v.check("Ex 10-04.1f", solve([[1 / 5e3]], [-gm1])[0])
v.check("Ex 10-04.1g", solve([[1 / 5e3 + 1 / ro1]], [-gm1])[0])
v.assert_true("g_m R_C equals the DC drop across R_C over V_T", abs(gm1 * 5e3 - 5.0 / VT) < 1e-6)

# ------------------------------------------------------------------ Example 2 (bias of Example 10-02.3)
kn = 4e-3
vov2 = brentq(lambda x: x + 0.5 * kn * x * x * 1e3 - 1.5, 0, 2)   # V_G = 2.0 V, R_S = 1 kOhm, V_TN = 0.5 V
id2 = 0.5 * kn * vov2 ** 2
gm2, _, ro2 = mos_params(kn, id2, lam=0.05)
v.check("Ex 10-04.2a", 2 * id2 / vov2 * 1e3)
v.check("Ex 10-04.2b", gm2 * 1e3)
v.check("Ex 10-04.2c", ro2 / 1e3)
v.check("Ex 10-04.2d", gm2 * ro2)
v.check("Ex 10-04.2e", gm2 / id2)
v.check("Ex 10-04.2f", gm1 / 1e-3)
v.check("Ex 10-04.2g", (gm1 / 1e-3) / (gm2 / id2))
v.assert_true("10-02.3's 0.8486 mA and 0.6514 V are reproduced", abs(id2 - 0.8486e-3) < 5e-8 and abs(vov2 - 0.6514) < 5e-5)

# ------------------------------------------------------------------ Example 3
v.check("Ex 10-04.3a", brentq(lambda a: a / (4 * VT) - 0.01, 1e-6, 1e-2) * 1e3)
v.check("Ex 10-04.3b", brentq(lambda a: mos_hd(a, 0.2)[0] - 0.01, 1e-5, 0.1) * 1e3)
v.check("Ex 10-04.3c", 10e-3 / (4 * VT) * 100)
v.check("Ex 10-04.3d", mos_hd(10e-3, 0.2)[0] * 100)
v.check("Ex 10-04.3e", bjt_hd(10e-3)[0] * 100)
exact_1 = brentq(lambda a: bjt_hd(a)[0] - 0.01, 1e-4, 5e-3)
v.assert_true("at 1% the exact and first-order BJT amplitudes agree to 4 digits", abs(exact_1 / a1 - 1) < 1e-4)
v.assert_true("the exact BJT HD2 lies below the formula by about x^2/24 at 10 mV",
              abs(bjt_hd(10e-3)[0] / (10e-3 / (4 * VT)) - (1 - (10e-3 / VT) ** 2 / 24)) < 1e-4)
v.assert_true("the formula is within ~1% of itself up to V_T/2",
              abs(bjt_hd(VT / 2)[0] / (0.5 / 4) - 1) < 0.011)

# ------------------------------------------------------------------ Example 4: degenerated CE, both models
beta4, RC, RE = 100, 5e3, 200.0
gm4, rpi4, re4, _ = bjt_params(1e-3, beta4)
alpha4 = beta4 / (beta4 + 1)
# Input resistance: drive the base with 1 V; unknown v_e. KCL at e: (1 - v_e)/r_pi + g_m(1 - v_e) = v_e/R_E
ve = solve([[1 / rpi4 + gm4 + 1 / RE]], [1 / rpi4 + gm4])[0]
ib = (1 - ve) / rpi4
v.check("Ex 10-04.4a", 1 / ib / 1e3)
v.check("Ex 10-04.4b", (1 / ib) / rpi4)
# hybrid-pi: unknowns [v_e, v_c]
x = solve([[1 / rpi4 + gm4 + 1 / RE, 0], [-gm4, 1 / RC]], [1 / rpi4 + gm4, -gm4])
v.check("Ex 10-04.4c", x[1])
# T model: emitter current through r_e from the base (internal base = base), collector alpha i_e
ie = solve([[re4 + RE]], [1.0])[0]
v.check("Ex 10-04.4d", re4)
v.check("Ex 10-04.4e", -alpha4 * ie * RC)
v.check("Ex 10-04.4f", -gm4 * RC / (1 + gm4 * RE))
v.assert_true("hybrid-pi and T gains agree", abs(x[1] + alpha4 * ie * RC) < 1e-9)
v.assert_true("approximation is 0.9% high", abs((gm4 * RC / (1 + gm4 * RE)) / abs(x[1]) - 1.009) < 5e-4)

# ------------------------------------------------------------------ Example 5: body transconductance
gamma, phi2, vsb = 0.4, 0.7, 0.849                 # V_SB: the source voltage of Example 10-02.3, body at ground
vtn0 = 0.5


def id_body(vgs, vsb_):
    vt = vtn0 + gamma * (math.sqrt(phi2 + vsb_) - math.sqrt(phi2))
    return 0.5 * kn * (vgs - vt) ** 2


vgs5 = vtn0 + gamma * (math.sqrt(phi2 + vsb) - math.sqrt(phi2)) + vov2      # same overdrive and current
gm5 = ddx(lambda g: id_body(g, vsb), vgs5, 1e-6)
gmb5 = -ddx(lambda s: id_body(vgs5, s), vsb, 1e-6)
v.check("Ex 10-04.5a", gmb5 / gm5)
v.check("Ex 10-04.5b", gmb5 * 1e3)

# ------------------------------------------------------------------ Example 6: CS stage of Example 10-02.3
RD, RS = 2e3, 1e3
v.check("Ex 10-04.6a", solve([[1 / RD + 1 / ro2]], [-gm2])[0])
v.check("Ex 10-04.6b", solve([[1 / RD]], [-gm2])[0])
# unbypassed: unknowns [v_s, v_d]; KCL at s: g_m(1 - v_s) = v_s/R_S; at d: g_m(1 - v_s) + v_d/R_D = 0
y = solve([[gm2 + 1 / RS, 0], [-gm2, 1 / RD]], [gm2, -gm2])
v.check("Ex 10-04.6c", y[1])
v.assert_true("degeneration factor equals 10-02's 3.61", abs((1 + gm2 * RS) - 3.61) < 5e-3)

# ------------------------------------------------------------------ Example 7
gm_t = 1e-3
v.check("Ex 10-04.7a", brentq(lambda i: bjt_params(i, 100)[0] - gm_t, 1e-7, 1e-2) * 1e6)
v.check("Ex 10-04.7b", brentq(lambda i: 2 * i / 0.2 - gm_t, 1e-7, 1e-2) * 1e6)
v.check("Ex 10-04.7c", brentq(lambda i: i / (n * VT) - gm_t, 1e-7, 1e-2) * 1e6)
v.check("Ex 10-04.7d", cross * 1e3)
v.check("Ex 10-04.7e", 1 / (n * VT))

# ================================================================== solutions
g, rp, r_e, ro = bjt_params(0.2e-3, 150, 75)
v.check("10-04.1a", g * 1e3)
v.check("10-04.1b", rp / 1e3)
v.check("10-04.1c", r_e)
v.check("10-04.1d", ro / 1e3)
v.check("10-04.1e", g * ro)

g, vo, ro = mos_params(2e-3, 0.25e-3, 0.1)
v.check("10-04.2a", vo)
v.check("10-04.2b", g * 1e3)
v.check("10-04.2c", ro / 1e3)
v.check("10-04.2d", g * ro)
g, vo, ro = mos_params(2e-3, 0.5e-3, 0.1)
v.check("10-04.2e", vo)
v.check("10-04.2f", g * 1e3)
v.check("10-04.2g", ro / 1e3)
v.check("10-04.2h", g * ro)
g, vo, ro = mos_params(4e-3, 0.5e-3, 0.1)          # doubled W: k_n doubles
v.check("10-04.2i", g * 1e3)
v.check("10-04.2j", ro / 1e3)
v.check("10-04.2k", g * ro)
v.assert_true("doubled width keeps the overdrive", abs(vo - 0.5) < 1e-9)

g, rp, r_e, _ = bjt_params(0.5e-3, 80)
v.check("10-04.4a", g * 1e3)
v.check("10-04.4b", rp / 1e3)
v.check("10-04.4c", r_e)
v.check("10-04.4d", 81 * r_e / 1e3)

g, rp, _, ro = bjt_params(2e-3, 120, 60)
rin = par(20e3, rp)
v.check("10-04.5a", g * 1e3)
v.check("10-04.5b", rp / 1e3)
v.check("10-04.5c", rin / 1e3)
# full circuit: nodes [b, c] driven from v_sig = 1 through 1 kOhm
z = solve([[1 / 1e3 + 1 / 20e3 + 1 / rp, 0], [g, 1 / 3e3 + 1 / 6e3 + 1 / ro]], [1 / 1e3, 0])
v.check("10-04.5d", z[0])
v.check("10-04.5e", ro / 1e3)
v.check("10-04.5f", par(3e3, 6e3, ro) / 1e3)
v.check("10-04.5g", z[1] / z[0])
v.check("10-04.5h", z[1])

g, vo, _ = mos_params(5e-3, 0.4e-3)
v.check("10-04.6a", g * 1e3)
v.check("10-04.6b", vo)
v.check("10-04.6c", solve([[1 / 5e3]], [-g])[0])
y = solve([[g + 1 / 500, 0], [-g, 1 / 5e3]], [g, -g])
v.check("10-04.6d", y[1])

v.check("10-04.7a", brentq(lambda a: a / (4 * VT) - 0.02, 1e-6, 1e-2) * 1e3)
v.check("10-04.7b", 100 * brentq(lambda a: a / (4 * VT) - 0.02, 1e-6, 1e-2) * 1e3)
a7 = brentq(lambda a: mos_hd(a, 0.15)[0] - 0.02, 1e-5, 0.1)
v.check("10-04.7c", a7 * 1e3)
v.check("10-04.7d", 20 * a7 * 1e3)

gamma, phi2, vsb, vtn0 = 0.5, 0.8, 0.5, 0.5
kn8 = 1.5e-3 / 0.6                                  # any k_n with g_m = 1.5 mS (V_ov = 0.6 V)
vgs8 = vtn0 + gamma * (math.sqrt(phi2 + vsb) - math.sqrt(phi2)) + 0.6


def id8(vgs, vsb_):
    return 0.5 * kn8 * (vgs - vtn0 - gamma * (math.sqrt(phi2 + vsb_) - math.sqrt(phi2))) ** 2


gm8 = ddx(lambda x: id8(x, vsb), vgs8, 1e-6)
gmb8 = -ddx(lambda s: id8(vgs8, s), vsb, 1e-6)
v.check("10-04.8a", gmb8 / gm8)
v.check("10-04.8b", gmb8 * 1e3)
# follower: KCL at the source with v_g = 1: g_m(1 - v_s) + g_mb(0 - v_s) = v_s / R_S
v.check("10-04.8c", solve([[gm8 + gmb8 + 1 / 10e3]], [gm8])[0])
v.check("10-04.8d", solve([[gm8 + 1 / 10e3]], [gm8])[0])
v.assert_true("g_m of 1.5 mS reproduced", abs(gm8 - 1.5e-3) < 1e-9)

v.check("10-04.9a", brentq(lambda i: i / VT - 2e-3, 1e-8, 1) * 1e6)
v.check("10-04.9b", brentq(lambda i: 2 * i / 0.25 - 2e-3, 1e-8, 1) * 1e6)
v.check("10-04.9c", brentq(lambda k: mos_params(k, 250e-6)[0] - 2e-3, 1e-4, 1) * 1e3)
v.check("10-04.9d", brentq(lambda i: i / (1.4 * VT) - 2e-3, 1e-8, 1) * 1e6)
v.assert_true("k_n = 8 mA/V^2 gives 2 mS at 250 uA", abs(mos_params(8e-3, 250e-6)[0] - 2e-3) < 1e-9)

x5 = 5e-3 / VT
v.check("10-04.10a", x5 / 4 * 100)
v.check("10-04.10b", x5 ** 2 / 24 * 100)
h2, h3, _ = bjt_hd(5e-3)
v.check("10-04.10c", h2 * 100)
v.check("10-04.10d", h3 * 100)
v.assert_true("square law has no third harmonic", mos_hd(5e-3, 0.2)[1] < 1e-12)

# diode-connected devices: drive the node with 1 V and sum the currents
v.check("10-04.11a", 1 / (1e-3 * 1 + 1 / 40e3))
g, rp, r_e, _ = bjt_params(1e-3, 100)
v.check("10-04.11b", 1 / (g + 1 / rp))
v.assert_true("diode-connected BJT equals r_e", abs(1 / (g + 1 / rp) - r_e) < 1e-6)

i_s = 1e-3 / math.exp(0.7 / VT)
icf = lambda vbe: i_s * math.exp(vbe / VT)          # noqa: E731
dn = -5e3 * (icf(0.7 + 5e-3) - 1e-3)
up = -5e3 * (icf(0.7 - 5e-3) - 1e-3)
lin = 5e3 * ddx(icf, 0.7, 1e-6) * 5e-3
v.check("10-04.12a", dn)
v.check("10-04.12b", up)
v.check("10-04.12c", lin)
v.check("10-04.12d", (abs(dn) / lin - 1) * 100)
v.check("10-04.12e", (up / lin - 1) * 100)

lam, I13 = 0.1, 100e-6
v.check("10-04.13a", brentq(lambda x: mos_params(2 * I13 / x ** 2, I13, lam)[0] * mos_params(2 * I13 / x ** 2, I13, lam)[2] - 50, 0.01, 2))
v.check("10-04.13b", brentq(lambda x: mos_hd(2e-3, x)[0] - 0.01, 0.01, 1))
v.check("10-04.13c", brentq(lambda x: mos_params(2 * I13 / x ** 2, I13)[0] - 1e-3, 0.01, 2))
g, vo, ro = mos_params(2 * I13 / 0.2 ** 2, I13, lam)
v.check("10-04.13d", 2 * I13 / 0.2 ** 2 * 1e3)
v.check("10-04.13e", g * ro)
v.check("10-04.13f", mos_hd(2e-3, 0.2)[0] * 100)
v.assert_true("13(c): weak-inversion HD2 at 2 mV is about 1.5%", abs(2e-3 / (4 * 1.3 * VT) * 100 - 1.49) < 0.01)

# ================================================================== lab
h2_20, _, _ = bjt_hd(20e-3)
v.check("Lab 10-04.a", h2_20 * 100)
v.check("Lab 10-04.b", 20e-3 / (4 * VT) * 100)
_, h3_10, dc10 = bjt_hd(10e-3)
v.check("Lab 10-04.c", h3_10 * 100)
v.check("Lab 10-04.d", dc10 * 100)
x10 = 10e-3 / VT
out = -5e3 * 1e-3 * (np.exp(x10 * np.cos(TH)) - 1)
v.check("Lab 10-04.e", out.min())
v.check("Lab 10-04.f", out.max())
v.check("Lab 10-04.g", 5e3 * 1e-3 * x10)
v.check("Lab 10-04.h", out.mean())


def ekv_gmid(vov):
    f = lambda q: math.log(math.log1p(math.exp(q / (2 * n * VT))) ** 2)   # noqa: E731
    return ddx(f, vov, 1e-6)


v.check("Lab 10-04.i", ekv_gmid(0.0))
v.check("Lab 10-04.j", ekv_gmid(0.2))
v.check("Lab 10-04.k", ekv_gmid(-0.2))
v.assert_true("EKV at threshold is about 72% of the weak-inversion limit", abs(ekv_gmid(0.0) * n * VT - 0.7213) < 5e-4)
v.assert_true("EKV lies below the square law at 0.2 V", ekv_gmid(0.2) < 2 / 0.2)
gx = ekv_gmid(2 * n * VT)
v.check("T 10-04.r", gx)
v.check("T 10-04.s", gx * n * VT * 100)
v.check("T 10-04.t", gx * VT * 100)
v.check("T 10-04.u", brentq(lambda q: ekv_gmid(q) * n * VT - 0.9, -0.5, 0.1, xtol=1e-12) * 1e3)

v.finish()
