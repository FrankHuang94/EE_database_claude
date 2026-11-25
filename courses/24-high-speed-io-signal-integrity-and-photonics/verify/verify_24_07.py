#!/usr/bin/env python3
"""Verify every number in chapter 24-07 (photonics fundamentals), its problems and lab.

Independent routes (the lab module optics.py uses closed forms and an FFT):
- photon physics from the CODATA constants written out here, in eV and SI;
- dispersion broadening by direct numerical quadrature of the Fourier integral of a Gaussian pulse, checked
  against the closed form sqrt(1 + (L/L_D)^2);
- the TIA by solving its nodal equation at each frequency and root-finding the -3 dB point;
- receiver sensitivities by root-finding BER(P) built on scipy.stats.norm, not on erfc;
- modulator levels, link budgets and WDM spacings by direct arithmetic.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "24-07-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("24-07", ROOT / "chapters" / "24-07-photonics-fundamentals.md",
                        ROOT / "solutions" / "24-07-solutions.md", LAB / "README.md")

h, q, c, k = 6.62607015e-34, 1.602176634e-19, 299792458.0, 1.380649e-23
NG = 1.468


def resp(lam_nm, eta=1.0):
    e_ph = h * c / (lam_nm * 1e-9)  # J per photon
    return eta * q / e_ph  # A/W: one electron per photon


def dbm(p_w):
    return 10 * math.log10(p_w / 1e-3)


def mw(p_dbm):
    return 10 ** (p_dbm / 10)


def dlam_nm(lam_nm, df_hz):
    return (lam_nm * 1e-9) ** 2 * df_hz / c * 1e9


def sens_w(ber, r, sigma):  # OOK: BER = Q(R P / sigma)
    return norm.isf(ber) * sigma / r


def er_pen(er):
    return 10 * math.log10((er + 1) / (er - 1))


# ---------------------------------------------------------------- Example 24-07.1
for i, lam in enumerate((850, 1310, 1550)):
    v.check(f"Ex 24-07.1a{'' if i == 0 else i}", resp(lam))
    v.check(f"Ex 24-07.1a{i + 3}", h * c / (lam * 1e-9) / q)
i_ph = 0.9 * mw(-10) * 1e-3
v.check("Ex 24-07.1b", i_ph * 1e6)
v.check("Ex 24-07.1b1", mw(-10) * 1e-3 / (h * c / 1310e-9))
v.check("Ex 24-07.1c", resp(1550) / resp(850))
v.assert_true("responsivity ratio equals wavelength ratio", abs(resp(1550) / resp(850) - 1550 / 850) < 1e-12)

# ---------------------------------------------------------------- Example 24-07.2
tau_per_m = NG / c
v.check("Ex 24-07.2a", tau_per_m * 1e3 * 1e6)
v.check("Ex 24-07.2a1", tau_per_m * 1e9)
v.check("Ex 24-07.2b", tau_per_m * 500 * 1e6)
v.check("Ex 24-07.2c", 100 * (1 - 1 / NG))
v.check("Ex 24-07.2d", 2 * 0.36)
v.check("Ex 24-07.2d1", 10 * 0.22)

# ---------------------------------------------------------------- Example 24-07.3 and text roundings
ui53 = 1e12 / 53.125e9
dl1550, dl1310 = dlam_nm(1550, 53.125e9), dlam_nm(1310, 53.125e9)
sp1550, sp1310 = 18 * 2 * dl1550, 3.5 * 2 * dl1310
v.check("Ex 24-07.3a", dl1550)
v.check("Ex 24-07.3a1", sp1550)
v.check("Ex 24-07.3a2", sp1550 / ui53)
v.check("Ex 24-07.3b", dl1310)
v.check("Ex 24-07.3b1", sp1310)
v.check("Ex 24-07.3b2", sp1310 / ui53)
v.check("Txt 24-07.d", sp1550)
v.check("Txt 24-07.e", sp1550 / ui53)
v.check("Txt 24-07.f", sp1310)

# ---------------------------------------------------------------- Example 24-07.4
v.check("Ex 24-07.4a", 4700e6 / 0.1 / 1e9)
v.check("Ex 24-07.4b", 2000e6 / 0.1 / 1e9)
v.check("Ex 24-07.4c", 0.1 * 3.0)


# ---------------------------------------------------------------- Example 24-07.5 (MZM as two interfering arms)
def mzm_field(dphi):
    """Output power fraction of a balanced MZM: two half-power arms recombined with phase difference dphi."""
    e = 0.5 * (np.exp(1j * dphi / 2) + np.exp(-1j * dphi / 2))
    return float(abs(e) ** 2)


v.check("Ex 24-07.5a", 2 / 4)
v.check("Ex 24-07.5a1", 2 / 2)
hi, lo = mzm_field(math.pi / 2 - math.pi / 4), mzm_field(math.pi / 2 + math.pi / 4)
v.check("Ex 24-07.5b", hi)
v.check("Ex 24-07.5b1", lo)
v.check("Ex 24-07.5b2", 10 * math.log10(hi / lo))
v.check("Ex 24-07.5b3", hi - lo)
v.check("Lab 24-07.g", 10 * math.log10(hi / lo))
v.check("Ex 24-07.5c", 1.4 * 2.0)
v.check("Ex 24-07.5c1", 2.3 * 1.0)
v.check("Ex 24-07.5c2", 4.4 * 0.5)

# ---------------------------------------------------------------- Example 24-07.6
shift = 1310 * 1.8e-4 / 4.2
lw = 1310 / 1e4
v.check("Ex 24-07.6a", shift)
v.check("Ex 24-07.6b", lw)
v.check("Ex 24-07.6c", lw / shift)
v.check("Ex 24-07.6d", 20e-15 * 1.0 ** 2 / 4 * 1e15)
v.check("Txt 24-07.c", 20e-15 * 1.0 ** 2 / 4 * 1e15)
v.check("Lab 24-07.h", shift * 2.3)

# ---------------------------------------------------------------- Example 24-07.7
sig7 = 20e-12 * math.sqrt(30e9)
p12 = sens_w(1e-12, 0.9, sig7)
pk4 = sens_w(2.4e-4, 0.9, sig7)
v.check("Ex 24-07.7a", sig7 * 1e6)
v.check("Ex 24-07.7b", p12 * 1e6)
v.check("Ex 24-07.7b1", dbm(p12))
v.check("Ex 24-07.7c0", norm.isf(2.4e-4))
v.check("Ex 24-07.7c", pk4 * 1e6)
v.check("Ex 24-07.7c1", dbm(pk4))
v.check("Ex 24-07.7d", 10 * math.log10(3))
v.check("Ex 24-07.7e", er_pen(10 ** 0.5))
v.check("Ex 24-07.7f", dbm(p12) - dbm(pk4))
v.check("Txt 24-07.a", 20 * math.log10(3))
v.check("Txt 24-07.g", p12 * 1e6)
v.check("Txt 24-07.h", er_pen(10 ** 0.5))

# ---------------------------------------------------------------- Example 24-07.8
rx8 = 0 - 2 * 0.36 - 2 * 0.5 - 2 * 1.5
req8 = dbm(pk4) + 10 * math.log10(3) + er_pen(10 ** 0.5)
v.check("Ex 24-07.8a", rx8)
v.check("Ex 24-07.8b", req8)
v.check("Ex 24-07.8c", rx8 - req8)
v.check("Ex 24-07.8d", (2 * 0.5 + 2 * 1.5) / (2 * 0.36))
v.check("Txt 24-07.k", rx8 - req8)


# ---------------------------------------------------------------- Example 24-07.9 and lab Part 1 (nodal TIA)
def tia_z(f, rf, a, cin):
    """Input node: I = V_in (j w C_in) + (V_in - V_out)/R_F with V_out = -A V_in. Returns |V_out / I|."""
    y = np.array([[1j * 2 * math.pi * f * cin + 1 / rf, -1 / rf], [a, 1.0]])
    vin, vout = np.linalg.solve(y, np.array([1.0, 0.0]))
    return abs(vout)


def tia_bw(rf, a, cin):
    z0 = tia_z(1.0, rf, a, cin)
    return optimize.brentq(lambda f: tia_z(f, rf, a, cin) - z0 / math.sqrt(2), 1e6, 1e12, xtol=1e-3), z0


bw9, z9 = tia_bw(1e3, 10, 100e-15)
v.check("Ex 24-07.9a", z9)
v.check("Ex 24-07.9b", bw9 / 1e9)
v.check("Ex 24-07.9b1", 1 / (2 * math.pi * 1e3 * 100e-15) / 1e9)
n9 = math.sqrt(4 * k * 300 / 1e3)
v.check("Ex 24-07.9c", n9 * 1e12)
v.check("Ex 24-07.9c1", n9 / 20e-12)
v.check("Txt 24-07.i", n9 * 1e12)
v.check("Ex 24-07.9d", c * 20e-9 / 1310e-9 ** 2 / 1e12)
v.check("Ex 24-07.9d1", dlam_nm(1550, 100e9))
v.check("Txt 24-07.j", c * 20e-9 / 1310e-9 ** 2 / 1e12)
v.check("Lab 24-07.a", z9)
v.check("Lab 24-07.b", bw9 / 1e9)
v.check("Lab 24-07.c", tia_bw(2e3, 10, 100e-15)[0] / 1e9)


# ---------------------------------------------------------------- Lab Part 2: dispersion by quadrature
def broadening(t0_ps, d, lam_nm, l_km):
    beta2 = -d * lam_nm ** 2 / (2 * math.pi * c * 1e-3)  # ps^2/km with c in nm/ps
    phi = beta2 * l_km / 2
    wmax = 12 / t0_ps

    def field(t):
        # E(t) = (1/2pi) int E~(w) exp(j phi w^2 - j w t) dw, with E~(w) = sqrt(2 pi) T0 exp(-T0^2 w^2 / 2)
        re = integrate.quad(lambda w: math.exp(-t0_ps ** 2 * w ** 2 / 2) * math.cos(phi * w ** 2 - w * t),
                            -wmax, wmax, limit=400)[0]
        im = integrate.quad(lambda w: math.exp(-t0_ps ** 2 * w ** 2 / 2) * math.sin(phi * w ** 2 - w * t),
                            -wmax, wmax, limit=400)[0]
        return (re ** 2 + im ** 2) * (t0_ps / math.sqrt(2 * math.pi)) ** 2

    def rms(l_scale):
        tt = np.linspace(-12 * t0_ps * l_scale, 12 * t0_ps * l_scale, 1201)
        p = np.array([field(t) for t in tt])
        return math.sqrt(integrate.trapezoid(tt ** 2 * p, tt) / integrate.trapezoid(p, tt)), p

    ld = t0_ps ** 2 / abs(beta2)
    closed = math.sqrt(1 + (l_km / ld) ** 2)
    w_out, _ = rms(closed)
    return w_out / (t0_ps / math.sqrt(2)), closed, ld


b1550, c1550, ld1550 = broadening(5.0, 18, 1550, 2.0)
b1310, c1310, _ = broadening(5.0, 3.5, 1310, 2.0)
v.assert_true("quadrature broadening at 1550 nm matches closed form", abs(b1550 / c1550 - 1) < 1e-4)
v.assert_true("quadrature broadening at 1310 nm matches closed form", abs(b1310 / c1310 - 1) < 1e-4)
v.check("Lab 24-07.d", b1550)
v.check("Lab 24-07.e", b1310)
v.check("Lab 24-07.f", ld1550)


# ---------------------------------------------------------------- Lab Part 4: sensitivity curves by root-finding
def log_ber_ook(p):
    return norm.logsf(0.9 * p / sig7)


def log_ber_pam4(p):
    return math.log(0.75) + norm.logsf(0.9 * p / 3 / sig7)  # Gray-coded: SER = 1.5 Q, BER = SER / 2


def p_for(log_fn, target):
    return optimize.brentq(lambda x: log_fn(mw(x) * 1e-3) - math.log(target), -30, 0, xtol=1e-9)


pi_ook, pi_pam = p_for(log_ber_ook, 1e-12), p_for(log_ber_pam4, 1e-12)
v.check("Lab 24-07.i", pi_ook)
v.check("Lab 24-07.j", pi_pam)
v.check("Lab 24-07.k", pi_pam - pi_ook)
v.assert_true("PAM4 sits slightly less than 4.77 dB right of OOK", 0 < 10 * math.log10(3) - (pi_pam - pi_ook) < 0.05)

# ---------------------------------------------------------------- Solutions
r1 = resp(1310, 0.8)
v.check("24-07.1a", r1)
v.check("24-07.1b0", mw(-6) * 1e3)
v.check("24-07.1b", r1 * mw(-6) * 1e3)
v.check("24-07.2a", mw(-20) * 1e3)
v.check("24-07.2b0", mw(-2))
v.check("24-07.2b", 4 * mw(-2))
v.check("24-07.2b1", dbm(4 * mw(-2) * 1e-3))
v.check("24-07.2b2", dbm(4 * mw(-2) * 1e-3) - (-2))
v.check("24-07.3a", 100 * NG / c * 1e6)
v.check("24-07.3b", 200 * NG / c * 1e6)
dl4 = dlam_nm(1310, 113.4375e9)
ui4 = 1e12 / 113.4375e9
v.check("24-07.4a", dl4)
v.check("24-07.4b", 3.5 * 2 * dl4)
v.check("24-07.4c0", ui4)
v.check("24-07.4c", 3.5 * 2 * dl4 / ui4)
v.check("24-07.4d", (3.5 * 2 * dl4 / ui4) / (sp1310 / ui53))
v.check("24-07.4d1", 113.4375 / 53.125)
v.assert_true("fractional spread grows as the square of the rate", abs((3.5 * 2 * dl4 / ui4) / (sp1310 / ui53)
                                                                        - (113.4375 / 53.125) ** 2) < 1e-9)
dl5, ui5 = dlam_nm(1550, 26.5625e9), 1e12 / 26.5625e9
v.check("24-07.5a", dl5)
v.check("24-07.5a1", ui5)
v.check("24-07.5", optimize.brentq(lambda L: 17 * L * dl5 - 0.25 * ui5, 0.01, 100))
v.check("24-07.6a", 2.3 / 1.0)
hi6, lo6 = mzm_field(math.pi / 2 - 0.4 * math.pi), mzm_field(math.pi / 2 + 0.4 * math.pi)
v.check("24-07.6b", hi6)
v.check("24-07.6b1", lo6)
v.check("24-07.6b2", hi6 / lo6)
v.check("24-07.6b3", 10 * math.log10(hi6 / lo6))
v.check("24-07.6b4", hi6 - lo6)
tune = 40 * shift
v.check("24-07.7a", tune)
v.check("24-07.7b", tune / 0.25)
v.check("24-07.7c", tune / 0.25 * 1e-3 / 100e9 * 1e15)
v.check("24-07.7c1", (tune / 0.25 * 1e-3 / 100e9 * 1e15) / 5)
sig8 = 15e-12 * math.sqrt(60e9)
p8 = sens_w(2.4e-4, 0.85, sig8)
v.check("24-07.8a", sig8 * 1e6)
v.check("24-07.8b0", norm.isf(2.4e-4))
v.check("24-07.8b", p8 * 1e6)
v.check("24-07.8b1", dbm(p8))
v.check("24-07.8c0", er_pen(10 ** 0.4))
v.check("24-07.8c", dbm(p8) + 10 * math.log10(3) + er_pen(10 ** 0.4))
v.check("24-07.9a", 1 - 0.5 * 0.36 - 2 * 0.75)
v.check("24-07.9b", (1 - 0.5 * 0.36 - 2 * 0.75) - (-8))
rf10 = optimize.brentq(lambda rf: tia_bw(rf, 8, 80e-15)[0] - 30e9, 100, 5000, xtol=1e-6)
v.check("24-07.10a", rf10)
v.check("24-07.10b", math.sqrt(4 * k * 300 / rf10) * 1e12)
v.check("24-07.10c", math.sqrt(4 * k * 300 / rf10) * math.sqrt(30e9) * 1e6)
v.check("24-07.11a", dlam_nm(1310, 100e9))
v.check("24-07.11b", 15 * dlam_nm(1310, 100e9))
v.check("24-07.12a", 10 ** (3 / 10))  # 3 dB optical is a factor of 2.0 in power and so in current
v.check("24-07.12b", 20 * math.log10(10 ** (3 / 10)))
q12 = norm.isf(1e-12) / 10 ** (3 / 10)
v.check("24-07.12c0", q12)
v.check("24-07.12c", norm.sf(q12))
er13 = optimize.brentq(lambda er: er_pen(er) - 1.0, 1.01, 1000)
v.check("24-07.13a", er13)
v.check("24-07.13b", 10 * math.log10(er13))

sys.exit(v.finish())
