#!/usr/bin/env python3
"""Verify every number in the Course 20 final-exam solutions.

Answers with a non-trivial route are recomputed independently; closed-form arithmetic is re-evaluated directly:
- gm/ID by numerically differentiating the charge-based current (q from 2q + ln q = V/V_T by root finding);
- the op-amp poles and zero from the roots of its exact transfer-function polynomials, the phase margin from the
  exact phase at the numerically found unity-gain frequency;
- the bandgap from Tsividis's V_BE(T) evaluated directly, the flat-point gain by root finding on dV/dT;
- LDO and PLL crossovers by root finding on the loop-gain magnitude;
- settling, regeneration and jitter limits by root finding on their defining equations;
- SAR switching energy by explicit charge bookkeeping over all codes;
- sigma-delta noise by numerical integration of |NTF|^2; leakage bounds by root finding;
- the DAC INL-yield constant by Monte Carlo of a pinned random walk; harmonics by FFT of the compression law;
- confidence intervals from the inverse incomplete gamma function; run counts by direct search;
- the kT/C integral by quadrature and the PLL phase maximum by numerical optimization.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, signal, special

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("20-exam", ROOT / "exam" / "solutions.md")
K_B, Q_E = 1.380649e-23, 1.602176634e-19
T0 = 300.0
KT = K_B * T0
VT = KT / Q_E
lg = math.log10
TWO_PI = 2 * math.pi
rng = np.random.default_rng(20)

# ---- Q1: charge-based model
n = 1.3


def q_of_v(vp):
    """Solve 2q + ln q = vp / V_T for q."""
    return optimize.brentq(lambda q: 2 * q + math.log(q) - vp / VT, 1e-30, 1e3)


def ic_of_v(vp):
    q = q_of_v(vp)
    return q * q + q


def gm_over_id_at(ic_target):
    vp = optimize.brentq(lambda x: ic_of_v(x) - ic_target, -0.3, 1.0)
    h = 1e-6
    # V_P = (V_G - V_TH)/n, so d ln I / dV_G = (1/n) d ln IC / dV_P
    return (math.log(ic_of_v(vp + h)) - math.log(ic_of_v(vp - h))) / (2 * h) / n


for key, ic in (("a", 0.1), ("b", 1), ("c", 10)):
    v.check(f"X20.1{key}", gm_over_id_at(ic))
mu, cox = 350e-4, 8.6e-3
isq = 2 * n * mu * cox * VT ** 2
v.check("X20.1d", isq * 1e6)
v.check("X20.1e", 100e-6 / (isq * 1))
g1 = gm_over_id_at(1)
v.check("X20.1f", g1 * 100e-6 * 1e3)
v.check("X20.1g", g1 * 8 * 0.5)
q1 = optimize.brentq(lambda q: q * q + q - 1, 0, 1)
v.check("X20.1h", 3 * mu * VT / (TWO_PI * (0.5e-6) ** 2) * q1 / 1e9)

# ---- Q2: exact two-stage transfer function
gm1, gm6, R1, R2, C1, CL, Cc = 1e-3, 5e-3, 2e5, 5e4, 0.2e-12, 2e-12, 1e-12
G1, G2 = 1 / R1, 1 / R2
# Vo {[G1 + s(C1+Cc)][G2 + s(CL+Cc)] + sCc(gm6 - sCc)} = gm1 (gm6 - sCc) Vin
den = np.polyadd(np.polymul([C1 + Cc, G1], [CL + Cc, G2]), np.polymul([Cc, 0], [-Cc, gm6]))
num = np.polymul([gm1], [-Cc, gm6])
A0 = num[-1] / den[-1]
poles = np.sort(np.abs(np.roots(den)))
zero = abs(np.roots(num)[0])
# The published values use the pole-splitting approximations; the exact polynomial roots must agree with them.
p1a = 1 / (gm6 * R1 * R2 * Cc)
p2a = gm6 * Cc / (C1 * CL + Cc * (C1 + CL))
v.assert_true("exact dominant pole within 2% of the approximation", abs(poles[0] / p1a - 1) < 0.02)
v.assert_true("exact second pole within 2% of the approximation", abs(poles[1] / p2a - 1) < 0.02)
v.assert_true("RHP zero is exactly gm6/Cc", abs(zero / (gm6 / Cc) - 1) < 1e-9)
v.check("X20.2a", A0)
v.check("X20.2b", 20 * lg(A0))
v.check("X20.2c", p1a / TWO_PI / 1e3)
v.check("X20.2d", gm1 / Cc / TWO_PI / 1e6)
v.check("X20.2e", p2a / TWO_PI / 1e6)
v.check("X20.2f", zero / TWO_PI / 1e6)
wu = gm1 / Cc
pm_est = 90 - math.degrees(math.atan(wu / p2a)) - math.degrees(math.atan(wu / zero))
v.check("X20.2g", pm_est)
H = lambda w: np.polyval(num, 1j * w) / np.polyval(den, 1j * w)  # noqa: E731
wx = optimize.brentq(lambda w: abs(H(w)) - 1, 1e6, 1e11)
pm_exact = 180 - sum(math.degrees(math.atan(wx / pp)) for pp in poles) - math.degrees(math.atan(wx / zero))
v.check("X20.2l", wx / TWO_PI / 1e6)
v.check("X20.2m", pm_exact)
v.check("X20.2h", 1 / gm6)
v.check("X20.2i", 1 / gm6 + 1 / (p2a * Cc))
v.check("X20.2j", 50e-6 / Cc / 1e6)
v.check("X20.2k", 50 * (1 + CL / Cc))

# ---- Q3: bandgap from V_BE(T) directly
kq, Vg0, VBE0, eta, m, N = K_B / Q_E, 1.2, 0.65, 4, 1, 8


def vbe(t):
    return Vg0 - (Vg0 - VBE0) * t / T0 - (eta - m) * kq * t * math.log(t / T0)


h = 1e-3
dvbe = (vbe(T0 + h) - vbe(T0 - h)) / (2 * h)
v.check("X20.3a", dvbe * 1e3)
v.check("X20.3b", kq * T0 * math.log(N) * 1e3)
v.check("X20.3c", kq * math.log(N) * 1e3)


def vref(t, kk):
    return vbe(t) + kk * kq * t * math.log(N)


kflat = optimize.brentq(lambda kk: (vref(T0 + h, kk) - vref(T0 - h, kk)) / (2 * h), 1, 30)
v.check("X20.3d", kflat)
v.check("X20.3e", vref(T0, kflat))
v.check("X20.3f", vref(250, kflat))
v.check("X20.3g", vref(350, kflat))
ts = np.linspace(250, 350, 2001)
vs = np.array([vref(t, kflat) for t in ts])
v.check("X20.3h", (vs.max() - vs.min()) / (vref(T0, kflat) * 100) * 1e6)

# ---- Q4: LDO
v.check("X20.4a", 1.2 * 0.1 / (1.8 * (0.1 + 50e-6)) * 100)
rout = 1 / (1 / 12 + 1 / 50)
v.check("X20.4b", rout)
L0 = 50 * 0.5 * 1 * rout
v.check("X20.4c", L0)
v.check("X20.4d", 20 * lg(L0))
# crossover of L(s) = A beta gmp Rout / (1 + s Rout CL) (ESR zero far above), by root finding
wc = optimize.brentq(lambda w: abs(L0 / (1 + 1j * w * rout * 10e-6)) - 1, 1e3, 1e9)
v.check("X20.4e", wc / TWO_PI / 1e3)
v.check("X20.4f", (0.1 / (wc * 10e-6) + 0.1 * 0.01) * 1e3)

# ---- Q5
delta = 1 / 4096
cs = KT / (delta ** 2 / 12)
v.check("X20.5a", cs * 1e12)
sj_fs = optimize.brentq(lambda s: -20 * lg(TWO_PI * 2e8 * s * 1e-15) - 74, 1, 1e4)
v.check("X20.5b", sj_fs)
tau = optimize.brentq(lambda t: math.exp(-2e-9 / t) - 2 ** -13, 1e-12, 1e-9)
v.check("X20.5c", tau * 1e9)
v.check("X20.5d", tau / cs)
tl = 20e-15 / 1e-3
v.check("X20.5e", tl * 1e12)
v.check("X20.5f", optimize.brentq(lambda t_ps: 1e-6 * math.exp(t_ps * 1e-12 / tl) - 0.5, 0, 1e3))
v.check("X20.5g", 0.5 * math.exp(-300e-12 / tl) * 1e6)

# ---- Q6
enob = (58 - 1.76) / 6.02
v.check("X20.6a", 6.02 * 10 + 1.76)
v.check("X20.6b", enob)
v.check("X20.6c", 5e-3 / (2 ** enob * 1e8) * 1e15)
v.check("X20.6d", 58 + 10 * lg(5e7 / 5e-3))
v.check("X20.6e", -60 - 10 * lg(5e7))
v.check("X20.6f", 60 + 10 * lg(50))
sd = 0.01 * math.sqrt(1023)
v.check("X20.6g", sd)
v.check("X20.6h", 0.5 * special.erfc(1 / sd / math.sqrt(2)) * 100)

# ---- Q7: SAR energy by explicit charge bookkeeping (differential arrays, trial-and-revert, all codes)


def sar_energy_conventional(nbits):
    """Average energy (C_u V_REF^2) drawn from V_REF by a conventional SAR, by explicit loops over every code: one
    single-ended array of binary caps plus a unit dummy, top plate at -vin after sampling; each trial raises the new
    bit and, if the previous trial failed, lowers that bit in the same transition; differential = 2 x single-ended."""
    caps = [2 ** i for i in range(nbits)] + [1]
    ct = sum(caps)
    total = 0.0
    for code in range(2 ** nbits):
        vin = (code + 0.5) / 2 ** nbits
        state = [0] * (nbits + 1)
        kept = [0] * (nbits + 1)
        vx = -vin
        for b in range(nbits - 1, -1, -1):
            new = kept.copy()
            new[b] = 1
            vxn = -vin + sum(c * s_ for c, s_ in zip(caps, new)) / ct
            total += sum(c * ((1 - vxn) - (s0 - vx)) for c, s0, s1 in zip(caps, state, new) if s1 == 1)
            state, vx = new, vxn
            if vx <= 0:
                kept[b] = 1
    return 2 * total / 2 ** nbits


e8_formula = sum(2 ** (8 + 1 - 2 * i) * (2 ** i - 1) for i in range(1, 9))
e10_formula = sum(2 ** (10 + 1 - 2 * i) * (2 ** i - 1) for i in range(1, 11))
v.assert_true("10-bit formula reproduces 20-07's 1363.3", abs(e10_formula - 1363.33) < 0.01)
e8_sim = sar_energy_conventional(8)
v.assert_true(f"bookkeeping matches the formula within 1% (sim {e8_sim:.1f}, formula {e8_formula:.1f})",
              abs(e8_sim / e8_formula - 1) < 0.01)
v.check("X20.7a", 2 ** 6 - 1)
v.check("X20.7b", 10)
v.check("X20.7c", e8_formula)
v.check("X20.7d", e8_formula * 1e-15 * 1.0 ** 2 * 1e15)
beta = 1 / (1 + 1 + 0.2)
v.check("X20.7e", beta)
v.check("X20.7f", 1 / (1 + 200 * beta) * 100)
v.check("X20.7g", 20 * lg(math.pi * 1e9 * 0.5e-12))
v.check("X20.7h", 20 * lg(0.002 / 2))
v.check("X20.7i", 10 * lg((1e-3) ** 2 / (2 * 0.5 ** 2)))

# ---- Q8: sigma-delta by numerical integration of |NTF|^2


def inband(L, osr):
    wb = math.pi / osr
    val, _ = integrate.quad(lambda w: (2 - 2 * math.cos(w)) ** L, 0, wb)
    return val / math.pi   # times sigma_e^2


sig_e2 = 2 ** 2 / 12
sq = 10 * lg((0.5 ** 2 / 2) / (sig_e2 * inband(2, 64)))
v.assert_true("numerical SQNR within 0.1 dB of the formula", abs(sq - (10 * lg(0.125 / (1 / 3)) - 10 * lg(math.pi ** 4 / 5) + 50 * lg(64))) < 0.1)
v.check("X20.8a", 10 * lg(0.125 / (1 / 3)) - 10 * lg(math.pi ** 4 / 5) + 50 * lg(64))
v.check("X20.8b", 50 * lg(2))
p8 = (1 + 1 / 100) / (1 + 1.5 / 100)
eps8 = 1 - p8
v.check("X20.8c", p8)
v.check("X20.8d", eps8)
# leaky NTF 1 - p z^-1 integrated numerically against the ideal
leaky, _ = integrate.quad(lambda w: abs(1 - p8 * np.exp(-1j * w)) ** 2, 0, math.pi / 64)
ideal, _ = integrate.quad(lambda w: abs(1 - np.exp(-1j * w)) ** 2, 0, math.pi / 64)
v.check("X20.8e", 10 * lg(leaky / ideal))
v.check("X20.8i", 10 * lg(1 + 3 * eps8 ** 2 * 64 ** 2 / math.pi ** 2))
a_single = optimize.brentq(lambda a: 1 / a - math.pi / (math.sqrt(3) * 128), 1, 1e4)
a_mash = optimize.brentq(lambda a: 1 / a - math.pi ** 2 / (math.sqrt(5) * 128 ** 2), 1, 1e6)
v.check("X20.8f", a_single)
v.check("X20.8g", a_mash)
v.check("X20.8h", 20 * lg(a_mash))

# ---- Q9
v.check("X20.9a", 0.005 * math.sqrt(2 ** 7 - 1))
v.check("X20.9b", 0.005 * math.sqrt(4095))
v.check("X20.9c", 0.5 / (1.818 * math.sqrt(1023)) * 100)
# Monte Carlo check of the 1.818 constant: max |bridge| of a 1023-step pinned walk exceeds 1.818 sigma sqrt(N)/2 ~0.27%
walks = rng.normal(0, 1, (6000, 1023)).cumsum(axis=1)
idx = np.arange(1, 1024) / 1023
bridge = walks - idx * walks[:, -1:]
frac = np.mean(np.abs(bridge).max(axis=1) / math.sqrt(1023) > 1.818 / 2 * 2)
v.assert_true(f"Brownian-bridge tail at 1.818 is about 0.27% (MC {frac * 100:.2f}%)", frac < 0.008)
x = 25 / 1e6
codes = np.arange(1024)
t = np.arange(4096)
sig_codes = 511.5 + 511.5 * np.sin(TWO_PI * 7 * t / 4096)   # unquantized, so only the compression distorts
vout = sig_codes / (1 + x * sig_codes)
spec = np.abs(np.fft.rfft(vout - vout.mean()))
hd2_fft, hd3_fft = 20 * lg(spec[14] / spec[7]), 20 * lg(spec[21] / spec[7])
xn = x * 1023
v.check("X20.9d", 20 * lg(xn / 4))
v.check("X20.9e", 20 * lg(xn ** 2 / 16))
v.assert_true(f"FFT of the compression law agrees within 0.5 dB (HD2 {hd2_fft:.2f}, HD3 {hd3_fft:.2f} dBc)",
              abs(hd2_fft - 20 * lg(xn / 4)) < 0.5 and abs(hd3_fft - 20 * lg(xn ** 2 / 16)) < 0.5)
v.check("X20.9f", x * 1023 ** 2 / 4)
v.check("X20.9g", 25 / (4 * 10 ** (-70 / 20) / 1023) / 1e6)
sinc = np.sinc
v.check("X20.9h", 20 * lg(sinc(0.3)))
v.check("X20.9i", 20 * lg(0.5 * sinc(0.15)))

# ---- Q10: loop filter by root finding on |G| = 1
b, fc = 9, 1e6
wc10 = TWO_PI * fc
K10 = 200e-6 * TWO_PI * 1e9 / (TWO_PI * 50)
wz, wp = wc10 / math.sqrt(b), wc10 * math.sqrt(b)


def gmag(ctot):
    return K10 * abs(1 + 1j * wc10 / wz) / (wc10 ** 2 * ctot * abs(1 + 1j * wc10 / wp))


ct = optimize.brentq(lambda c: gmag(c) - 1, 1e-13, 1e-6)
c1 = ct * (b - 1) / b
v.check("X20.10a", math.degrees(math.atan(wc10 / wz) - math.atan(wc10 / wp)))
v.check("X20.10b", wz / TWO_PI / 1e3)
v.check("X20.10c", wp / TWO_PI / 1e6)
v.check("X20.10d", ct * 1e12)
v.check("X20.10e", c1 * 1e12)
v.check("X20.10f", (ct - c1) * 1e12)
v.check("X20.10g", 1 / (wz * c1) / 1e3)
v.check("X20.10h", -150 + 20 * lg(50))
lin10 = 10 ** ((-150 + 20 * lg(50)) / 10)
var, _ = integrate.quad(lambda f: 2 * lin10, 1e4, 1e6)
sphi = math.sqrt(var)
v.check("X20.10i", sphi * 1e3)
sj10 = sphi / (TWO_PI * 2.5e9)
v.check("X20.10j", sj10 * 1e15)
v.check("X20.10k", 10 * lg(sj10 ** 2 * 10))

# ---- Q11
v.check("X20.11a", 4 / math.sqrt(16))
v.check("X20.11b", (4 / 0.25) ** 2)
v.check("X20.11c", math.hypot(6e-3, 0.004) * 100)
v.check("X20.11d", 0.05 * 4)
xs = np.array([-1.5, -0.5, 0.5, 1.5]) * 4
prof = 0.05 * xs + 5e-4 * xs ** 2
v.check("X20.11e", abs(prof[[0, 3]].mean() - prof[[1, 2]].mean()))
dof = 199
lo = math.sqrt(dof / (2 * special.gammaincinv(dof / 2, 0.975)))
hi = math.sqrt(dof / (2 * special.gammaincinv(dof / 2, 0.025)))
v.check("X20.11f", 1.2 * lo)
v.check("X20.11g", 1.2 * hi)
pf = special.erfc(4 / math.sqrt(2))
nrun = 1
while (1 - pf) ** nrun > 0.05:
    nrun += 1
v.check("X20.11h", nrun)

# ---- Q12
c12 = 2 * KT * 1e8 / 0.25 ** 2
v.check("X20.12a", c12 * 1e12)
gm12 = TWO_PI * 2e7 * c12 / 0.5
v.check("X20.12b", gm12 / 15 * 1e6)
v.check("X20.12c", 0.9 * gm12 / 15 * 1e6)
v.check("X20.12d", 10 * 3)
v.check("X20.12e", 0.9 - 5 * 0.12)
e12 = 1 / (1 + 50 * 0.4)
v.check("X20.12f", e12 * 100)
v.check("X20.12g", 2 ** -14 / e12 * 100)

# ---- Q13
fcorner = 1 / (TWO_PI * 1e3 * 2e-12)   # R = 1 kohm; the result must not depend on it
shape, _ = integrate.quad(lambda xx: 1 / (1 + xx * xx), 0, np.inf)
noise = 4 * KT * 1e3 * fcorner * shape
v.check("X20.13a", math.sqrt(noise) * 1e6)
v.check("X20.13b", 10 * lg(inband(1, 32)))
res = optimize.minimize_scalar(lambda lw: -(math.atan(math.exp(lw)) - math.atan(math.exp(lw) / 16)),
                               bounds=(-5, 5), method="bounded")
v.assert_true("phase lead peaks at sqrt(wz wp) = 4 wz", abs(math.exp(res.x) - 4) < 1e-3)
v.check("X20.13c", math.degrees(-res.fun))

# ---- Q14
sndr = 6.02 * 10.5 + 1.76
v.check("X20.14a", 10e-3 / (2 ** 10.5 * 1e9) * 1e15)
v.check("X20.14b", sndr + 10 * lg(5e8 / 10e-3))
pmin = 8 * KT * 10 ** (sndr / 10) * 1e9
v.check("X20.14c", pmin * 1e3)
v.check("X20.14d", 10e-3 / pmin)
v.check("X20.14e", optimize.brentq(lambda s_fs: -20 * lg(TWO_PI * 5e8 * s_fs * 1e-15) - 65, 1, 1e4))
v.check("X20.14f", optimize.brentq(lambda d_ps: 20 * lg(math.pi * 5e8 * d_ps * 1e-12) + 70, 1e-4, 10))
v.check("X20.14g", 0.3 * 0.75 / 0.7 + 0.7 * 0.7 * (0.7 / 0.75) ** 2)

sys.exit(v.finish())
