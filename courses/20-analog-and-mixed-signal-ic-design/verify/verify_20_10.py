#!/usr/bin/env python3
"""Verify every number in chapter 20-10 (PLLs and jitter), its problems and its lab.

Independent routes:
- the loop filter solved by root finding on the three design conditions (zero, pole, unity gain at crossover) with an
  open-loop gain coded here from polynomials (the lab uses closed-form design equations);
- closed-loop bandwidth, peaking and settling from numpy polynomials and scipy.signal.lsim (the lab uses step());
- jitter by adaptive quadrature of the phase-noise profile (the lab uses log-spaced trapezoids) and in closed form;
- the MASH divider re-implemented as a cascade of first-order error-feedback stages with exact Fractions, checked
  bit-for-bit against the lab's integer accumulators, with its period found by search;
- figures of merit and the TDC floor from their definitions.
ngspice confirms the open-loop crossover and phase margin (run_spice).
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, signal

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "20-10-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import pll as lab  # noqa: E402

v = Verifier.from_files("20-10", ROOT / "chapters" / "20-10-plls-and-jitter.md", ROOT / "solutions" / "20-10-solutions.md",
                        LAB / "README.md")
lg = math.log10
TWO_PI = 2 * math.pi


def g_poly(icp, kv, n, r, c1, c2):
    """Open-loop G(s) = num/den as numpy polynomials (highest power first)."""
    k = icp * kv / (TWO_PI * n)
    tau2 = r * c1 * c2 / (c1 + c2)
    return np.array([k * r * c1, k]), np.array([(c1 + c2) * tau2, c1 + c2, 0.0, 0.0])


def g_eval(f, *args):
    num, den = g_poly(*args)
    s = 1j * TWO_PI * np.asarray(f, float)
    return np.polyval(num, s) / np.polyval(den, s)


def design(fc, b, icp, kv, n):
    """Solve for (R, C1, C2): zero at fc/sqrt b, pole at fc sqrt b, |G(j 2 pi fc)| = 1."""
    def resid(ctot):
        c2 = ctot / b
        c1 = ctot - c2
        r = math.sqrt(b) / (TWO_PI * fc * c1)
        return abs(g_eval(fc, icp, kv, n, r, c1, c2)) - 1
    ctot = optimize.brentq(resid, 1e-15, 1e-6, xtol=1e-25)
    c2 = ctot / b
    c1 = ctot - c2
    return math.sqrt(b) / (TWO_PI * fc * c1), c1, c2


ICP, KV, N = 500e-6, TWO_PI * 500e6, 100

# ------------------------------------------------------------------ Example 20-10.1
print("Example 20-10.1")
v.check("Ex 20-10.1a", N * 50e6 / 1e9)
v.check("Ex 20-10.1b", ICP / TWO_PI * 1e6)
v.check("Ex 20-10.1c", (5e9 - 4.5e9) / 500e6)
v.check("Ex 20-10.1d", N * 51e6 / 1e9)
v.check("Ex 20-10.1e", (5.1e9 - 4.5e9) / 500e6)

# ------------------------------------------------------------------ Example 20-10.2
print("Example 20-10.2")
args = None
R, C1, C2 = design(2e6, 10, ICP, KV, N)
args = (ICP, KV, N, R, C1, C2)
fx = optimize.brentq(lambda f: abs(g_eval(f, *args)) - 1, 1e4, 1e8)
pm = 180 + math.degrees(np.angle(g_eval(fx, *args)))
v.check("Ex 20-10.2a", pm)
v.check("Ex 20-10.2b", 1 / (TWO_PI * R * C1) / 1e3)
v.check("Ex 20-10.2c", (C1 + C2) / (TWO_PI * R * C1 * C2) / 1e6)
v.check("Ex 20-10.2d", (C1 + C2) * 1e12)
v.check("Ex 20-10.2e", C1 * 1e12)
v.check("Ex 20-10.2f", C2 * 1e12)
v.check("Ex 20-10.2g", R / 1e3)
v.check("Ex 20-10.2h", fx / 1e6)
v.check("Ex 20-10.2i", pm)
lr, lc1, lc2 = lab.design_third_order(2e6, 10, ICP, KV, N)
v.assert_true("lab design equations agree", abs(lr / R - 1) < 1e-9 and abs(lc1 / C1 - 1) < 1e-9 and abs(lc2 / C2 - 1) < 1e-9)
v.assert_true("closed-form PM agrees", abs(pm - math.degrees(math.atan(9 / (2 * math.sqrt(10))))) < 1e-9)

# ------------------------------------------------------------------ Example 20-10.3
print("Example 20-10.3")
num, den = g_poly(*args)
cl_num, cl_den = np.polymul(num, [1.0]), np.polyadd(den, num)          # G/(1+G) = (theta_out/N)/theta_ref
hcl = lambda f: abs(np.polyval(cl_num, 1j * TWO_PI * f) / np.polyval(cl_den, 1j * TWO_PI * f))  # noqa: E731
f3 = optimize.brentq(lambda f: hcl(f) - 1 / math.sqrt(2), 2e6, 2e7)
grid = np.logspace(4, 8, 40001)
v.check("Ex 20-10.3a", f3 / 1e6)
v.check("Ex 20-10.3b", 20 * lg(max(hcl(f) for f in grid)))
t = np.linspace(0, 4e-6, 400001)
_, y, _ = signal.lsim((cl_num, cl_den), np.ones_like(t), t)
outside = np.nonzero(np.abs(y - 1) > 1e-3)[0]
v.check("Ex 20-10.3c", t[outside[-1] + 1] * 1e6)
k = ICP * KV / (TWO_PI * N)
wn = math.sqrt(k / C1)
zeta = R / 2 * math.sqrt(k * C1)
v.check("Ex 20-10.3d", wn / TWO_PI / 1e6)
v.check("Ex 20-10.3e", zeta)
v.check("Ex 20-10.3f", zeta * wn / TWO_PI / 1e6)
v.check("Ex 20-10.3g", math.log(1000) / (zeta * wn) * 1e6)

# ------------------------------------------------------------------ Example 20-10.4
print("Example 20-10.4")
g1 = g_eval(1e6, *args)
ref_db = 20 * lg(abs(g1 / (1 + g1)))
vco_db = 20 * lg(abs(1 / (1 + g1)))
v.check("Ex 20-10.4a", ref_db)
v.check("Ex 20-10.4b", -150 + 20 * lg(N) + ref_db)
v.check("Ex 20-10.4c", vco_db)
v.check("Ex 20-10.4d", -120 + vco_db)
v.check("Ex 20-10.4e", (-150 + 20 * lg(N) + ref_db) - (-120 + vco_db))

# ------------------------------------------------------------------ Example 20-10.5 and lab Part 4
print("Example 20-10.5")


def jitter_quad(l0, fc, f1, f2, f0):
    prof = lambda f: l0 if f <= fc else l0 * (fc / f) ** 2  # noqa: E731
    a, _ = integrate.quad(prof, f1, fc, limit=200)
    b, _ = integrate.quad(prof, fc, f2, limit=400)
    return math.sqrt(2 * (a + b)), math.sqrt(2 * (a + b)) / (TWO_PI * f0)


phi, sj = jitter_quad(1e-10, 2e6, 1e4, 1e9, 5e9)
v.check("Ex 20-10.5a", sj * 1e15)
v.check("Ex 20-10.5d", phi * 1e3)
v.check("Ex 20-10.5b", -20 * lg(TWO_PI * 1e9 * sj))
v.check("Ex 20-10.5c", -20 * lg(TWO_PI * 1e8 * sj))
v.assert_true("lab jitter integrator agrees",
              abs(lab.integrate_jitter([1e3, 2e6, 2e9], [-100, -100, -160], 1e4, 1e9, 5e9) / sj - 1) < 1e-4)
v.check("Lab 20-10.a", jitter_quad(1e-10, 2e6, 12e3, 20e6, 5e9)[1] * 1e15)
v.check("Lab 20-10.b", jitter_quad(1e-10, 2e6, 10e3, 100e6, 5e9)[1] * 1e15)
# Part 3: closed-loop noise transfer with this script's own loop design, integrated 1 kHz to 1 GHz
f3 = np.logspace(3, 9, 20001)
l_ref3 = 10 ** (-150 / 10) * N ** 2
l_vco3 = 10 ** (-120 / 10) * (1e6 / f3) ** 2
for key, fc3 in zip("cdefg", (0.1e6, 0.3e6, 1e6, 2e6, 5e6)):
    g3 = g_eval(f3, ICP, KV, N, *design(fc3, 10, ICP, KV, N))
    tot3 = l_ref3 * np.abs(g3 / (1 + g3)) ** 2 + l_vco3 * np.abs(1 / (1 + g3)) ** 2
    v.check(f"Lab 20-10.{key}", math.sqrt(2 * integrate.trapezoid(tot3, f3)) / (TWO_PI * 5e9) * 1e15)
v.check("Lab 20-10.h", optimize.brentq(lambda f_mhz: -120 + 20 * lg(1 / f_mhz) - (-150 + 20 * lg(N)), 0.01, 10))
v.check("Lab 20-10.i", -150 + 20 * lg(N))

# ------------------------------------------------------------------ Example 20-10.6
print("Example 20-10.6")
v.check("Ex 20-10.6a", 5.0123e9 / 50e6)
mash = lambda f, fr: (TWO_PI) ** 2 / (12 * fr) * (2 * math.sin(math.pi * f / fr)) ** 4  # noqa: E731
v.check("Ex 20-10.6b", 10 * lg(mash(1e6, 50e6)))
v.check("Ex 20-10.6c", 10 * lg(mash(10e6, 50e6)))
g10 = g_eval(10e6, *args)
v.check("Ex 20-10.6d", 10 * lg(mash(1e6, 50e6) * abs(g1 / (1 + g1)) ** 2))
v.check("Ex 20-10.6e", 10 * lg(mash(10e6, 50e6) * abs(g10 / (1 + g10)) ** 2))


def mash_frac(frac, n):
    """MASH 1-1-1 as three error-feedback quantizers on exact fractions: stage j quantizes (input + error) with floor."""
    e = [Fr(0)] * 3
    y = []
    hist = [[0, 0], [0, 0]]
    for _ in range(n):
        x = frac
        q = []
        for j in range(3):
            s = x + e[j]
            qj = 1 if s >= 1 else 0
            e[j] = s - qj
            x = e[j]
            q.append(qj)
        out = q[0] + (q[1] - hist[0][0]) + (q[2] - 2 * hist[1][0] + hist[1][1])
        hist[0] = [q[1], hist[0][0]]
        hist[1] = [q[2], hist[1][0]]
        y.append(out)
    return np.array(y, float)


seq = mash_frac(Fr(123, 500), 6000)
v.assert_true("lab integer MASH matches the exact-fraction MASH", np.array_equal(seq, lab.mash_sequence(123, 500, 6000)))
period = next(p for p in range(1, 3000) if np.array_equal(seq[2000:4000], seq[2000 + p:4000 + p]))
v.check("Ex 20-10.6f", period)
v.check("Ex 20-10.6g", 50e6 / period / 1e3)

# ------------------------------------------------------------------ Example 20-10.7
print("Example 20-10.7")
v.check("Ex 20-10.7a", 10 * lg((100e-15) ** 2 * (10e-3 / 1e-3)))
v.check("Ex 20-10.7b", 120 + 20 * lg(5e9 / 1e6) - 10 * lg(5))
tdc = 10 * lg(TWO_PI ** 2 / 12 * (10e-12 * 5e9) ** 2 / 50e6)
v.check("Ex 20-10.7c", tdc)
v.check("Ex 20-10.7d", tdc - (-100))

# ------------------------------------------------------------------ problems
print("Problems")
v.check("20-10.1a", 96 * 25e6 / 1e9)
v.check("20-10.1b", 200e-6 / TWO_PI * 1e6)
v.check("20-10.2a", 1e9 * 10e-3 / 1e6)
v.check("20-10.2b", TWO_PI * 10e6 * 1e-6)
icp3, kv3, n3, c3, r3 = 100e-6, TWO_PI * 200e6, 40, 100e-12, 10e3
k3 = icp3 * kv3 / (TWO_PI * n3)
v.check("20-10.3a", math.sqrt(k3 / c3) / TWO_PI / 1e3)
v.check("20-10.3b", r3 / 2 * math.sqrt(k3 * c3))
for key, b in (("4a", 4), ("4b", 10), ("4c", 20)):
    rr, cc1, cc2 = design(2e6, b, ICP, KV, N)
    ff = optimize.brentq(lambda f: abs(g_eval(f, ICP, KV, N, rr, cc1, cc2)) - 1, 1e4, 1e8)
    v.check(f"20-10.{key}", 180 + math.degrees(np.angle(g_eval(ff, ICP, KV, N, rr, cc1, cc2))))
r5, c15, c25 = design(500e3, 10, icp3, kv3, n3)
v.check("20-10.5a", (c15 + c25) * 1e12)
v.check("20-10.5b", c15 * 1e12)
v.check("20-10.5c", c25 * 1e12)
v.check("20-10.5d", r5 / 1e3)
v.check("20-10.6a", 25e6 / 10 / 1e6)
v.check("20-10.7a", -155 + 20 * lg(96))
phi8, sj8 = jitter_quad(10 ** -10.5, 1e6, 1e3, 1e8, 2.4e9)
v.check("20-10.8a", phi8 * 1e3)
v.check("20-10.8b", sj8 * 1e15)
v.check("20-10.9a", 10 ** (-70 / 20) / (TWO_PI * 500e6) * 1e15)
lin = 10 * lg((10e-12 / (200e-6 / TWO_PI)) ** 2 / 2)
v.check("20-10.10a", lin)
v.check("20-10.10b", lin + 20 * lg(96))
v.check("20-10.11a", 2.41e9 / 25e6)
v.check("20-10.11b", 10 * lg(mash(1e6, 25e6)))
v.check("20-10.12a", 25e6 / 5 / 1e6)
v.check("20-10.13a", 10 * lg((200e-15) ** 2 * 4))
v.check("20-10.13b", 125 + 20 * lg(2.4e9 / 1e6) - 10 * lg(2))
v.check("20-10.14a", math.sqrt(12 * 25e6 * 1e-11) / (TWO_PI * 2.4e9) * 1e12)

# --- Text: practitioner numbers (sources in §14; arithmetic recomputed here) ---
from scipy import special  # noqa: E402

# Gardner's bound w_c < w_ref / (pi (1 + pi w_z / w_ref)) in the limit w_z -> 0, as a fraction of f_ref.
v.check("Txt 20-10.a", 1 / (math.pi * (1 + math.pi * 1e-9)))
# Gaussian peak-to-peak band holding all but one of N edges on average: 2 Q^-1(1/(2N)) = 2 sqrt2 erfcinv(1/N).
for key, n_edges in (("b", 1e3), ("c", 1e9), ("d", 1e12)):
    v.check(f"Txt 20-10.{key}", 2 * math.sqrt(2) * special.erfcinv(1 / n_edges))
phi_evm = 0.035  # rad, EVM ~ rms phase error for small errors
v.check("Txt 20-10.e", math.degrees(phi_evm))
v.check("Txt 20-10.f", phi_evm / (TWO_PI * 28e9) * 1e15)


def fom_j(sigma_t, p_mw):
    return 10 * lg(sigma_t ** 2 * p_mw)


v.check("Txt 20-10.g", fom_j(0.15e-12, 4.2 * 1.8))
v.check("Txt 20-10.h", fom_j(20.3e-15, 12))
v.check("Txt 20-10.i", fom_j(21.6e-15, 18.1))
v.check("Txt 20-10.j", fom_j(143e-15, 40))
# LMX2594 model: flat = FOM + 20 log(fvco/fpd) + 10 log(fpd/1 Hz).
v.check("Txt 20-10.k", 10 * lg(10 ** (-236 / 10) * (12e9 / 100e6) ** 2 * 100e6))
# ideal oscillator FoM from Leeson's model evaluated at an arbitrary 1/f^2-region point (F = 1, P_s = P)
kt10 = 1.380649e-23 * 300
f0_, df_, q_, p_ = 5e9, 1e6, 10, 1e-3
l_leeson = 2 * kt10 / p_ * (1 + (f0_ / (2 * q_ * df_)) ** 2)
v.check("Txt 20-10.l", -10 * lg(l_leeson) + 20 * lg(f0_ / df_) - 10 * lg(p_ / 1e-3))
v.assert_true("closed form 2Q^2 mW/(FkT) agrees", abs(10 * lg(2 * q_ ** 2 * 1e-3 / kt10) - 196.8) < 0.05)

# ------------------------------------------------------------------ Problems 15 and 16 (own design, own transfer functions)
print("Problems 15-16")


def loop_parts(fc, b, icp, kv, n):
    rr, cc1, cc2 = design(fc, b, icp, kv, n)
    return rr, cc1, cc2


def settle(fc, n, tol=10e3 / 50e6, b=10):
    rr, cc1, cc2 = design(fc, b, ICP, KV, n)
    nm, dn = g_poly(ICP, KV, n, rr, cc1, cc2)
    tt = np.linspace(0, 40e-6, 400001)
    _, yy, _ = signal.lsim((nm, np.polyadd(dn, nm)), np.ones_like(tt), tt)
    return tt[np.nonzero(np.abs(yy - 1) > tol)[0][-1] + 1]


r15, c1_15, c2_15 = design(0.3e6, 10, ICP, KV, N)
k15 = ICP * KV / (TWO_PI * N)
v.check("20-10.15a", (c1_15 + c2_15) * 1e9)
v.assert_true("C1 + C2 = K sqrt(b)/wc^2 exactly", abs((c1_15 + c2_15) - k15 * math.sqrt(10) / (TWO_PI * 0.3e6) ** 2) < 1e-15)
v.check("20-10.15b", c2_15 * 1e12)
v.check("20-10.15c", c1_15 * 1e9)
v.check("20-10.15d", r15)
wn15 = math.sqrt(k15 / c1_15)
z15 = r15 / 2 * math.sqrt(k15 * c1_15)
v.check("20-10.15e", wn15 / TWO_PI / 1e3)
v.check("20-10.15f", z15)
v.check("20-10.15g", math.log(5000) / (z15 * wn15) * 1e6)
v.check("20-10.15h", settle(0.15e6, N) * 1e6)
v.assert_true("exact settling at 0.3 MHz is 8.17 us", abs(settle(0.3e6, N) * 1e6 - 8.17) < 0.005)

mash3 = lambda f, fr: TWO_PI ** 2 / (12 * fr) * (2 * np.sin(np.pi * f / fr)) ** 4  # noqa: E731
v.check("20-10.16a", optimize.brentq(lambda fm: -120 + 20 * lg(1 / fm) + 110, 0.01, 10))
v.check("20-10.16b", optimize.brentq(lambda f: 10 * lg(mash3(f, 50e6)) + 110, 1e5, 5e6) / 1e6)
f16 = np.logspace(4, math.log10(20e6), 40001)


def jitter16(fc, fref, with_mash=True, only_mash=False):
    nn = 5.0123e9 / fref
    gg = g_eval(f16, ICP, KV, nn, *design(fc, 10, ICP, KV, nn))
    hh = np.abs(gg / (1 + gg)) ** 2
    ref = 1e-15 * nn ** 2 * hh
    vco = 1e-12 * (1e6 / f16) ** 2 * np.abs(1 / (1 + gg)) ** 2
    msh = mash3(f16, fref) * hh
    tot = msh if only_mash else ref + vco + (msh if with_mash else 0)
    return math.sqrt(2 * integrate.trapezoid(tot, f16)) / (TWO_PI * 5.0123e9) * 1e15


for kj, ks, fc in (("c", "d", 0.2e6), ("e", "f", 0.3e6), ("g", "h", 0.5e6)):
    v.check(f"20-10.16{kj}", jitter16(fc, 50e6))
    v.check(f"20-10.16{ks}", settle(fc, 5.0123e9 / 50e6) * 1e6)
v.check("20-10.16r", jitter16(0.3e6, 50e6, with_mash=False))
v.check("20-10.16q", jitter16(0.3e6, 50e6, only_mash=True))
v.check("20-10.16i", 10 * lg(mash3(1e5, 50e6) / mash3(1e5, 100e6)))
v.check("20-10.16j", 20 * lg(2))
v.check("20-10.16k", jitter16(0.3e6, 100e6))
v.assert_true("100 MHz reference: settling unchanged", abs(settle(0.3e6, 5.0123e9 / 100e6) - settle(0.3e6, 5.0123e9 / 50e6)) < 2e-9)
r16, c1_16, c2_16 = design(0.3e6, 10, ICP, KV, 5.0123e9 / 100e6)
v.check("20-10.16l", (c1_16 + c2_16) * 1e9)
v.check("20-10.16m", c1_16 * 1e9)
v.check("20-10.16n", c2_16 * 1e12)
v.check("20-10.16o", r16)
v.check("20-10.16p", (c1_16 + c2_16) / 0.5e-9)

sys.exit(v.finish())
