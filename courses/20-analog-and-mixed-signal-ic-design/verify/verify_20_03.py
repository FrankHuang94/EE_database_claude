#!/usr/bin/env python3
"""Verify every number in chapter 20-03 (bandgap and voltage references), its problems and its lab.

Independent routes:
- junction voltages by root-finding the exponential law I = I_S(T) e^{V/V_T} rather than taking a logarithm;
- every circuit (op-amp bandgap with offset, current-mode reference, beta multiplier) solved as a full set of node
  equations with scipy.optimize.fsolve, from scratch, rather than by the lab's one-variable reductions;
- the centered design is found by matching the exact circuit's outputs at -40 and 125 C, not from the closed form,
  and peak temperatures by numerical maximization;
- the closed forms (Tsividis' V_BE(T), the first-order output V_g0 + (eta - m) V_T [1 - ln(T/T_c)], the
  T ln T difference) are checked symbolically with sympy;
- the lab module (bandgap.py) is asserted to agree; ngspice confirms the netlists (run_spice).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import brentq, fsolve, minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "20-03-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import bandgap as lab  # noqa: E402

v = Verifier.from_files("20-03", ROOT / "chapters" / "20-03-bandgap-references.md",
                        ROOT / "solutions" / "20-03-solutions.md", LAB / "README.md")

KB, QE = 1.380649e-23, 1.602176634e-19
T0 = 300.0
IS0, VG0, ETA = 2e-17, 1.2009, 3.0
U = 1e-6
TA, TB = 233.15, 398.15


def vt(t):
    return KB * t / QE


def i_s(t, area=1.0, is0=IS0, eta=ETA):
    return area * is0 * (t / T0) ** eta * math.exp(QE * VG0 / KB * (1 / T0 - 1 / t))


def vbe(i, t, area=1.0, is0=IS0, eta=ETA):
    """Junction voltage by root-finding the chapter's exponential law I = I_S e^{V/V_T} (no logarithm). SPICE's
    diode-connected BJT obeys I_S (e^{V/V_T} - 1); the -1 term (35 pA in the 8x device at 125 C) moves the output
    by under 2 uV and is not part of the chapter's model."""
    isat = i_s(t, area, is0, eta)
    return brentq(lambda x: isat * math.exp(x / vt(t)) - i, 0.0, 2.0, xtol=1e-15, rtol=1e-15)


def bandgap_fs(t, r1, r2, n=8.0, vos=0.0, is0=IS0, eta=ETA):
    """Op-amp bandgap: unknowns (V_out, V_A, V_C); V_B = V_A - V_os; equal-R2 feeds; solved with fsolve."""
    def eqs(x):
        vo, va, vc = x
        vb = va - vos
        i1 = (vo - va) / r2
        i2 = (vo - vb) / r2
        isa, isb = i_s(t, 1.0, is0, eta), i_s(t, n, is0, eta)
        return [(isa * math.exp(va / vt(t)) - i1) / U,     # Q1 carries i1 (residuals in uA)
                ((vb - vc) / r1 - i2) / U,                   # R1 carries i2
                (isb * math.exp(vc / vt(t)) - i2) / U]     # Q2 carries i2
    # start near the working state (a guess at 0.68 V at -40 C slides into the zero-current state, section 3.7)
    va0 = vt(t) * math.log(5e-6 * t / T0 / i_s(t, 1.0, is0, eta))
    x0 = [1.25, va0, va0 - vt(t) * math.log(n) - vos]
    sol, info, _, _ = fsolve(eqs, x0, full_output=True, xtol=1e-15)
    assert np.max(np.abs(info["fvec"])) < 1e-9, info["fvec"]
    assert (sol[0] - sol[1]) / r2 > 1e-7, "converged to the zero-current state"
    return sol[0]


def current_mode_fs(t, r1, r2, r3, n=8.0):
    """Current-mode reference: unknowns (I, V_A, V_C) with V_B = V_A; output I R3."""
    def eqs(x):
        i, va, vc = x
        return [(i_s(t) * math.exp(va / vt(t)) + va / r2 - i) / U,
                ((va - vc) / r1 + va / r2 - i) / U,
                (i_s(t, n) * math.exp(vc / vt(t)) - (va - vc) / r1) / U]
    va0 = vt(t) * math.log(5e-6 * t / T0 / i_s(t))
    sol, info, _, _ = fsolve(eqs, [5e-6 * t / T0 + va0 / r2, va0, va0 - vt(t) * math.log(n)], full_output=True,
                             xtol=1e-15)
    assert np.max(np.abs(info["fvec"])) < 1e-9, info["fvec"]
    return sol[0] * r3, sol


def box(values, vnom, ta=TA, tb=TB):
    values = np.asarray(values)
    return (values.max() - values.min()) / (vnom * (tb - ta)) * 1e6


TS = np.arange(-40, 125.0001, 0.05) + 273.15
TS_COARSE = np.arange(-40, 125.0001, 0.5) + 273.15

# ================================================================ symbolic checks of section 3
T, Tz, Tc, Vg, Vb0, eta, m, k_, q_, Kx, Nx = sp.symbols("T T_0 T_c V_g0 V_BE0 eta m k q K N", positive=True)
Vt = k_ * T / q_
c_ = sp.symbols("c")
vbe_t = Vg + Vt * (c_ + (m - eta) * sp.log(T / Tz)) - 0 * T
# choose c so that V_BE(T0) = V_BE0, then compare with Tsividis' form
c_sol = sp.solve(sp.Eq(vbe_t.subs(T, Tz) - Vg, Vb0 - Vg), c_)[0]
tsiv = Vg - (Vg - Vb0) * T / Tz - (eta - m) * Vt * sp.log(T / Tz)
v.assert_true("Tsividis V_BE(T) from I_S ~ T^eta exp(-qV_g0/kT) and I ~ T^m",
              sp.simplify(sp.expand_log(vbe_t.subs(c_, c_sol) - tsiv, force=True)) == 0, "")
vref = tsiv + Kx * Vt * sp.log(Nx)
k_sol = sp.solve(sp.Eq(sp.diff(vref, T).subs(T, Tc), 0), Kx)[0]
closed = Vg + (eta - m) * Vt * (1 - sp.log(T / Tc))
v.assert_true("first-order bandgap closed form V_g0 + (eta - m) V_T [1 - ln(T/T_c)]",
              sp.simplify(sp.expand_log(vref.subs(Kx, k_sol) - closed, force=True)) == 0, "")
diff10 = tsiv.subs(m, 1) - tsiv.subs(m, 0)
v.assert_true("V_BE(m=1) - V_BE(m=0) = V_T ln(T/T0)", sp.simplify(diff10 - Vt * sp.log(T / Tz)) == 0, "")

# ================================================================ sections 3.2-3.3 and Example 20-03.1
VT0 = vt(T0)
v.check("Txt 20-03.a", VT0 * 1e3)
v.check("Ex 20-03.4a", VT0 * math.log(8) / (VT0 * math.log(8) / 5e-6) / U)
I0 = 5e-6
vbe0 = vbe(I0, T0)
v.check("Ex 20-03.1a", vbe0)
dT = 1e-3


def slope_m(m_, i0=I0):
    f = lambda t: vbe(i0 * (t / T0) ** m_, t)  # noqa: E731
    return (f(T0 + dT) - f(T0 - dT)) / (2 * dT)


s0, s1 = slope_m(0), slope_m(1)
v.check("Ex 20-03.1b", s0 * 1e3)
v.check("Ex 20-03.1c", s1 * 1e3)
ptat8 = KB / QE * math.log(8)
v.check("Ex 20-03.1d", ptat8 * 1e6)
v.check("Txt 20-03.b", ptat8 * 1e6)
K300 = -s1 / ptat8
v.check("Ex 20-03.1e", K300)
magic = VG0 + 2 * VT0
v.check("Ex 20-03.1f", magic)
v.check("Txt 20-03.c", magic)
# the flat sum at 300 K with K300 really is flat and equals the magic voltage
fs = lambda t: vbe(I0 * t / T0, t) + K300 * vt(t) * math.log(8)  # noqa: E731
v.assert_true("V_BE + K V_T ln N has zero slope at 300 K", abs((fs(T0 + dT) - fs(T0 - dT)) / (2 * dT)) < 1e-9, "")
v.assert_true("and equals V_g0 + 2 V_T", abs(fs(T0) - magic) < 1e-9, "")

# ================================================================ Example 20-03.2: centered design from the exact circuit
R1 = VT0 * math.log(8) / I0


def ends_mismatch(k):
    return bandgap_fs(TA, R1, k * R1) - bandgap_fs(TB, R1, k * R1)


KC = brentq(ends_mismatch, 10.0, 11.5, xtol=1e-13)
R2 = KC * R1
pk = minimize_scalar(lambda t: -bandgap_fs(t, R1, R2), bounds=(290, 340), method="bounded", options={"xatol": 1e-9})
v.check("Ex 20-03.2a", pk.x)
v.check("Txt 20-03.d", pk.x)
v.check("Ex 20-03.2b", pk.x - 273.15)
v.check("Ex 20-03.2g", pk.x - 273.15)
v.check("Ex 20-03.2c", KC)
v.check("Ex 20-03.2h", R1 / 1e3)
v.check("Ex 20-03.2i", R2 / 1e3)
vs = np.array([bandgap_fs(t, R1, R2) for t in TS])
VN = bandgap_fs(T0, R1, R2)
OFFSET_GAIN = abs(bandgap_fs(T0, R1, R2, vos=1e-5) - bandgap_fs(T0, R1, R2, vos=-1e-5)) / 2e-5   # exact circuit
_re = VT0 / I0
v.assert_true("offset gain matches the linearized formula", abs(OFFSET_GAIN - ((R2 / R1) * (1 + _re / R2) ** 2 + 1 + _re / R2))
              < 1e-3)
v.check("Txt 20-03.aa", OFFSET_GAIN)
v.check("Ex 20-03.2d", VN)
v.check("Ex 20-03.2e", vs.max())
v.check("Ex 20-03.2f", vs.min())
v.assert_true("minimum at -40 C", abs(TS[int(np.argmin(vs))] - TA) < 1e-6, "")
v.check("Ex 20-03.2j", (vs.max() - vs.min()) * 1e3)
v.check("Txt 20-03.f", (vs.max() - vs.min()) * 1e3)
BOX = box(vs, VN)
v.check("Ex 20-03.2k", BOX)
v.check("Txt 20-03.e", BOX)
v.check("Ex 20-03.4f", BOX)
v.check("Ex 20-03.5a", BOX)
v.assert_true("peak value equals V_g0 + 2 V_T(T_c)", abs(-pk.fun - (VG0 + 2 * vt(pk.x))) < 1e-8,
              f"{-pk.fun - (VG0 + 2 * vt(pk.x))}")
# 0 to 70 C: center by matching the exact circuit's ends at 0 and 70 C
t1, t2 = 273.15, 343.15
k07 = brentq(lambda k: bandgap_fs(t1, R1, k * R1) - bandgap_fs(t2, R1, k * R1), 10.0, 11.5, xtol=1e-13)
pk07 = minimize_scalar(lambda t: -bandgap_fs(t, R1, k07 * R1), bounds=(290, 330), method="bounded",
                       options={"xatol": 1e-9})
ts07 = np.arange(0, 70.0001, 0.05) + 273.15
v07 = np.array([bandgap_fs(t, R1, k07 * R1) for t in ts07])
v.check("Ex 20-03.2l", pk07.x - 273.15)
v.check("Ex 20-03.2m", (v07.max() - v07.min()) * 1e6)
box07 = box(v07, bandgap_fs(T0, R1, k07 * R1), t1, t2)
v.check("Ex 20-03.2n", box07)
v.check("Txt 20-03.g", box07)
v.check("Ex 20-03.2o", (vs.max() - vs.min()) / (v07.max() - v07.min()))
v.check("Ex 20-03.2p", 165 / 70)

# ================================================================ Example 20-03.3: errors and trims
fa = lambda t, r2=R2: bandgap_fs(t, R1, r2, is0=1.3 * IS0)  # noqa: E731
v.check("Ex 20-03.3a", (fa(T0) - VN) * 1e3)
v.check("Ex 20-03.3b", (fa(T0) - VN) / T0 * 1e6)
v.check("Ex 20-03.3c", box([fa(t) for t in TS], VN))
r2t = brentq(lambda r: fa(T0, r) - VN, 0.9 * R2, 1.1 * R2, xtol=1e-9)
v.check("Ex 20-03.3d", (r2t / R2 - 1) * 100)
dev = max(abs(fa(t, r2t) - bandgap_fs(t, R1, R2)) for t in TS_COARSE)
v.assert_true("I_S error trimmed out at every temperature", dev < 1e-8, f"{dev}")
fo = lambda t, r2=R2: bandgap_fs(t, R1, r2, vos=1e-3)  # noqa: E731
v.check("Ex 20-03.3e", fo(T0))
v.check("Ex 20-03.3f", (fo(T0) - VN) * 1e3)
v.check("Ex 20-03.3g", 1 + R2 / R1)
v.check("Txt 20-03.m", 1 + R2 / R1)
v.check("Ex 20-03.3h", box([fo(t) for t in TS], VN))
r2o = brentq(lambda r: fo(T0, r) - VN, 0.9 * R2, 1.2 * R2, xtol=1e-9)
v.check("Ex 20-03.3i", r2o / 1e3)
v.check("Ex 20-03.3j", (fo(TB, r2o) - bandgap_fs(TB, R1, R2)) * 1e3)
v.check("Ex 20-03.3k", (fo(TA, r2o) - bandgap_fs(TA, R1, R2)) * 1e3)
v.check("Ex 20-03.3l", box([fo(t, r2o) for t in TS], VN))

# ================================================================ Example 20-03.4: current mode
_, sol300 = current_mode_fs(T0, R1, R2, 1.0)
i_tot, va300, _ = sol300
iq = (va300 - sol300[2]) / R1
R3 = 0.6 / i_tot
v.check("Ex 20-03.4b", va300)
v.check("Ex 20-03.4c", i_tot / U)
v.check("Ex 20-03.4d", R3 / 1e3)
v.check("Ex 20-03.4e", R3 / R2)
v.assert_true("junction current is V_T ln N / R1", abs(iq - VT0 * math.log(8) / R1) < 1e-15, "")
vcm = np.array([current_mode_fs(t, R1, R2, R3)[0] for t in TS])
v.check("Ex 20-03.4g", (vcm.max() - vcm.min()) * 1e3)
v.check("Ex 20-03.4h", 3 * i_tot / U)
v.assert_true("current-mode TC equals the voltage-mode TC", abs(box(vcm, 0.6) - BOX) < 1e-6, "")
# netlist values (rounded resistors, as in banba.cir)
vnl = np.array([current_mode_fs(t, 10.7515e3, 115.2307e3, 55.1065e3)[0] for t in TS])
v.check("Ex 20-03.4i", current_mode_fs(T0, 10.7515e3, 115.2307e3, 55.1065e3)[0])
v.check("Ex 20-03.4j", vnl.max())
v.check("Ex 20-03.4k", vnl.min())
v.check("Txt 20-03.n", vbe(I0 * TA / T0, TA))
v.check("Txt 20-03.o", vbe(I0 * TA / T0, TA) + 0.15)

# ================================================================ Example 20-03.5 and section 3.8: curvature


def curv_box(cc, ta=TA, tb=TB):
    """Box TC of V_g0 + c V_T(T)[1 - ln(T/T_c)] with T_c centred numerically (ends equal)."""
    f = lambda t, tc: VG0 + cc * vt(t) * (1 - math.log(t / tc))  # noqa: E731
    tc = brentq(lambda x: f(ta, x) - f(tb, x), 200, 420, xtol=1e-12)
    ts = np.arange(ta, tb + 1e-9, 0.05)
    vals = np.array([f(t, tc) for t in ts])
    return box(vals, f(T0, tc), ta, tb), vals.max() - vals.min()


b30, _ = curv_box(2.0)
b32, _ = curv_box(2.2)
b32c, pp02 = curv_box(0.2)
v.check("Ex 20-03.5b", b32)
v.check("Txt 20-03.i", b32)
v.check("Ex 20-03.5c", b32c)
v.check("Txt 20-03.h", b32c)
v.check("Ex 20-03.5d", b32 / b32c)
v.check("Txt 20-03.j", b32 / b32c)
v.check("Ex 20-03.5e", pp02 / 0.2 * 1e3)
v.assert_true("closed-form box for c = 2 matches the circuit", abs(b30 - BOX) < 1e-6, f"{b30} vs {BOX}")

# ================================================================ Example 20-03.6: beta multiplier (fsolve, from scratch)
MU, COX, NN, VTHN = 350e-4, 8.6e-3, 1.3, 0.45


def id_ekv(vg, vs, wl, t):
    vp = (vg - VTHN) / NN
    qq = brentq(lambda q: 2 * q + math.log(q) - (vp - vs) / vt(t), 1e-40, 1e6, xtol=1e-40, rtol=1e-15)
    return 2 * NN * MU * COX * wl * vt(t) ** 2 * (qq * qq + qq)


def beta_mult(r, k, wl, t, delta=0.0):
    """Unknowns (V_G, V_S): M1 carries I_P + delta, M2 (k wl, source V_S) carries I_P = V_S / R."""
    def eqs(x):
        vg, vsrc = x
        ip = vsrc / r
        return [id_ekv(vg, 0.0, wl, t) / 1e-7 - (ip + delta) / 1e-7, id_ekv(vg, vsrc, k * wl, t) / 1e-7 - ip / 1e-7]
    sol, info, _, _ = fsolve(eqs, [0.36, 0.037], full_output=True, xtol=1e-15)
    assert np.max(np.abs(info["fvec"])) < 1e-9, info["fvec"]
    return sol[1] / r, sol[0]


ib, vgb = beta_mult(100e3, 4, 10, T0)
v.check("Ex 20-03.6a", vt(T0) * math.log(4) / 100e3 / U)
v.check("Ex 20-03.6b", ib / U)
v.check("Ex 20-03.6c", (ib / (vt(T0) * math.log(4) / 100e3) - 1) * 100)
v.check("Ex 20-03.6d", ib / (2 * NN * MU * COX * 10 * vt(T0) ** 2))
ih, _ = beta_mult(100e3, 4, 10, TB)
ic_, _ = beta_mult(100e3, 4, 10, TA)
v.check("Ex 20-03.6e", ih / U)
v.check("Ex 20-03.6f", ic_ / U)
v.check("Ex 20-03.6g", ih / ib)
v.check("Ex 20-03.6h", TB / T0)

# ================================================================ section 1 and sourced values (R-326)
fits = [2.330, 2.303, 2.286, 2.316, 2.405]          # Tsividis (1980), five processes
v.check("Txt 20-03.p", min(fits))
v.check("Txt 20-03.q", max(fits))
v.check("Txt 20-03.r", 1.20595)                     # Tsividis' extrapolated V_G0 (T_r >= 300 K)
v.check("Txt 20-03.s", 3.429)                       # "fictitious" eta of the linear form (process V)
v.check("Txt 20-03.t", 1.1761)                      # and its V_G0
v.check("Txt 20-03.u", 1.20595 + (min(fits) - 1) * VT0)
v.check("Txt 20-03.v", 1.20595 + (max(fits) - 1) * VT0)
v.check("Txt 20-03.w", 518)                         # Banba et al. (1999), measured output in mV
v.check("Txt 20-03.x", 3 * 165)
v.check("Txt 20-03.k", 1e6 / 4096)
v.check("Txt 20-03.l", BOX * 165)

# ================================================================ problems
# 20-03.1
for i, (a, b) in ((1e-6, ("a", "b")), (20e-6, ("c", "d"))):
    v.check(f"20-03.1{a}", vbe(i, T0))
    v.check(f"20-03.1{b}", slope_m(1, i) * 1e3)
# 20-03.2
p24 = KB / QE * math.log(24)
v.check("20-03.2a", ptat8 * 1e6)
v.check("20-03.2b", p24 * 1e6)
v.check("20-03.2c", -s1 / ptat8)
v.check("20-03.2d", -s1 / p24)
# 20-03.3: constant-current bias, zero slope at 300 K, from the junction law directly
k_m0 = -s0 / ptat8
v.check("20-03.3a", vbe(I0, T0) + k_m0 * VT0 * math.log(8))
v.check("20-03.3b", magic)
v.check("20-03.3c", (curv_box(3.0)[0] / curv_box(2.0)[0] - 1) * 100)
# 20-03.4
for (ta, tb), (a, b, c3) in (((218.15, 398.15), ("a", "b", "c")), ((233.15, 358.15), ("d", "e", "f"))):
    f = lambda t, tc: VG0 + 2 * vt(t) * (1 - math.log(t / tc))  # noqa: E731
    tc = brentq(lambda x: f(ta, x) - f(tb, x), 200, 420, xtol=1e-12)
    bx, pp = curv_box(2.0, ta, tb)
    v.check(f"20-03.4{a}", tc - 273.15)
    v.check(f"20-03.4{b}", pp * 1e3)
    v.check(f"20-03.4{c3}", bx)
# 20-03.5: 2 uA, N = 24, zero TC centred (ends of the exact circuit equal)
r1_5 = VT0 * math.log(24) / 2e-6
k5 = brentq(lambda k: bandgap_fs(TA, r1_5, k * r1_5, n=24) - bandgap_fs(TB, r1_5, k * r1_5, n=24), 6.0, 8.5,
            xtol=1e-13)
v.check("20-03.5a", vbe(2e-6, T0))
v.check("20-03.5b", r1_5 / 1e3)
v.check("20-03.5c", k5)
v.check("20-03.5d", k5 * r1_5 / 1e3)
v.check("20-03.5e", bandgap_fs(T0, r1_5, k5 * r1_5, n=24))
# 20-03.6
f8 = lambda t, r2=R2: bandgap_fs(t, R1, r2, is0=0.8 * IS0)  # noqa: E731
v.check("20-03.6a", (f8(T0) - VN) * 1e3)
v.check("20-03.6b", (f8(T0) - VN) / T0 * 1e6)
r2_6 = brentq(lambda r: f8(T0, r) - VN, 0.9 * R2, 1.1 * R2, xtol=1e-9)
v.check("20-03.6c", (r2_6 / R2 - 1) * 100)
v.assert_true("trim matches ln(0.8)/(K ln 8)", abs((r2_6 / R2 - 1) - math.log(0.8) / (KC * math.log(8))) < 1e-6, "")
# 20-03.7
f7 = lambda t, r2=R2: bandgap_fs(t, R1, r2, vos=0.2e-3)  # noqa: E731
v.check("20-03.7a", (f7(T0) - VN) * 1e3)
r2_7 = brentq(lambda r: f7(T0, r) - VN, 0.9 * R2, 1.1 * R2, xtol=1e-9)
v.check("20-03.7b", box([f7(t, r2_7) for t in TS], VN))
v.check("20-03.7c", (f7(TB, r2_7) - bandgap_fs(TB, R1, R2)) * 1e3)
# 20-03.8
v.check("20-03.8a", (bandgap_fs(T0, R1, 1.005 * R2) - VN) * 1e3)
v.check("20-03.8b", 400 / 300)
v.check("20-03.8c", 1 + 2000e-6 * 100)
v.check("20-03.8d", (400 / 300) / 1.2)
v.check("20-03.8e", KC * VT0 * math.log(8))


def vref_rtc(t, tc):
    f = 1 + tc * (t - T0)
    return bandgap_fs(t, R1 * f, R2 * f)


shift400 = (vref_rtc(400.0, 2000e-6) - vref_rtc(400.0, 0.0)) * 1e3
v.check("20-03.8f", shift400)
v.check("Txt 20-03.y", shift400)
v.check("20-03.8g", box([vref_rtc(t, 0.0) for t in TS_COARSE], VN))
box_tc = box([vref_rtc(t, 2000e-6) for t in TS_COARSE], VN)
v.check("20-03.8h", box_tc)
v.check("Txt 20-03.z", box_tc)
v.assert_true("absolute +20% resistor error equals -V_T ln 1.2 (PTAT)",
              abs((bandgap_fs(T0, 1.2 * R1, 1.2 * R2) - VN) + VT0 * math.log(1.2)) < 1e-9)
# 20-03.9
v.check("20-03.9a", 0.5 / i_tot / 1e3)
v.check("20-03.9b", vbe(I0 * TA / T0, TA))
v.check("20-03.9c", vbe(I0 * TA / T0, TA) + 0.15)
# 20-03.10
b35, _ = curv_box(2.5)
b35c, _ = curv_box(0.5)
v.check("20-03.10a", b35)
v.check("20-03.10b", b35c)
v.check("20-03.10c", b35 / b35c)
v.check("20-03.10d", (1 - 0.5 / 2.5) * 100)
# 20-03.11
v.check("20-03.11a", vt(T0) * math.log(8) / 1e-6 / 1e3)
v.check("20-03.11b", NN * vt(T0) * math.log(8) / 1e-6 / 1e3)
# 20-03.12
v.check("20-03.12a", vgb)
v.check("20-03.12b", ib / U)
v.check("20-03.12c", 1e-9 / math.log(4) * 1e9)
ibd, _ = beta_mult(100e3, 4, 10, T0, delta=1e-9)
v.check("20-03.12d", (ibd - ib) * 1e9)
v.check("20-03.12e", (ibd - ib) / ib * 100)
v.check("20-03.12f", 1e-9 / math.log(4) / ib * 100)
# 20-03.13
gain = OFFSET_GAIN
v.check("20-03.13a", gain)
v.check("20-03.13i", 1 + KC)
v.check("20-03.13b", 30 * gain)
rms = 30e-9 * gain * 100
v.check("20-03.13c", rms / U)
v.check("20-03.13d", rms / VN * 1e6)
k24 = brentq(lambda k: bandgap_fs(TA, R1 * math.log(24) / math.log(8), k * R1 * math.log(24) / math.log(8), n=24)
             - bandgap_fs(TB, R1 * math.log(24) / math.log(8), k * R1 * math.log(24) / math.log(8), n=24), 6.0, 8.5,
             xtol=1e-13)
r1_24 = R1 * math.log(24) / math.log(8)
g24 = abs(bandgap_fs(T0, r1_24, k24 * r1_24, n=24, vos=1e-5) - bandgap_fs(T0, r1_24, k24 * r1_24, n=24, vos=-1e-5)) / 2e-5
v.check("20-03.13e", k24)
v.check("20-03.13f", g24)
v.check("20-03.13g", 30e-9 * g24 * 100 / U)
v.check("20-03.13h", (1 - g24 / gain) * 100)
# 20-03.14
v.check("20-03.14a", 500 + 3 * 165)
v.check("20-03.14b", (500 + 3 * 165) * 1e-6 * 2.5 * 1e3)
v.check("20-03.14c", 1e6 / 4096)
v.check("20-03.14d", 1e6 / 65536)
v.check("20-03.14e", 3 * 165)

# ================================================================ lab README
for m_, t_, key in ((0, TA, "a"), (0, TB, "b"), (1, TA, "c"), (1, TB, "d")):
    v.check(f"Lab 20-03.{key}", vbe(I0 * (t_ / T0) ** m_, t_))
# the seeded Monte Carlo, re-solved with this script's own nodal solver
rng = np.random.default_rng(2003)
zz = rng.standard_normal((400, 2))
grid5 = np.arange(-40, 125.0001, 5.0) + 273.15
v300, bun, btr = [], [], []
for z1, z2 in zz:
    isx, vosx = IS0 * math.exp(0.1 * z1), 0.5e-3 * z2
    fmc = lambda t, r2=R2: bandgap_fs(t, R1, r2, vos=vosx, is0=isx)  # noqa: E731
    v300.append(fmc(T0))
    bun.append(box([fmc(t) for t in grid5], VN))
    r2x = brentq(lambda r: fmc(T0, r) - VN, 0.8 * R2, 1.25 * R2, xtol=1e-9)
    btr.append(box([fmc(t, r2x) for t in grid5], VN))
v300, bun, btr = np.array(v300), np.array(bun), np.array(btr)
v.check("Lab 20-03.e", v300.std(ddof=1) * 1e3)
v.check("Lab 20-03.f", np.median(bun))
v.check("Lab 20-03.g", np.percentile(bun, 95))
v.check("Lab 20-03.h", np.median(btr))
v.check("Lab 20-03.i", np.percentile(btr, 95))
v.check("Lab 20-03.j", np.mean(btr < 15) * 100)
v.check("Lab 20-03.k", OFFSET_GAIN)
v.check("Lab 20-03.l", VT0 * 0.1 * 1e3)
# offset-free parts return to the nominal curve after the trim
z1 = zz[0, 0]
f0 = lambda t, r2=R2: bandgap_fs(t, R1, r2, is0=IS0 * math.exp(0.1 * z1))  # noqa: E731
r2z = brentq(lambda r: f0(T0, r) - VN, 0.8 * R2, 1.25 * R2, xtol=1e-9)
v.assert_true("an offset-free part trims back to the nominal TC", abs(box([f0(t, r2z) for t in grid5], VN) -
                                                                  box([bandgap_fs(t, R1, R2) for t in grid5], VN))
              < 1e-6, "")

# ================================================================ the lab module agrees
p = lab.PNP()
v.assert_true("bandgap.py V_BE matches", abs(p.vbe(I0, T0) - vbe0) < 1e-12, "")
v.assert_true("bandgap.py op-amp bandgap matches", abs(lab.opamp_bandgap(312.0, R1, R2)["vref"] -
                                                         bandgap_fs(312.0, R1, R2)) < 1e-10, "")
v.assert_true("bandgap.py offset case matches", abs(lab.opamp_bandgap(TB, R1, R2, vos=1e-3)["vref"] - fo(TB)) < 1e-10,
              "")
v.assert_true("bandgap.py current mode matches", abs(lab.current_mode_bandgap(TA, R1, R2, R3)["vref"] -
                                                     current_mode_fs(TA, R1, R2, R3)[0]) < 1e-10, "")
v.assert_true("bandgap.py beta multiplier matches", abs(lab.beta_multiplier(100e3, 4, 10) / ib - 1) < 1e-8, "")
v.assert_true("bandgap.py closed form matches", abs(lab.vref_closed_form(350.0, VG0, ETA, 1.0, pk.x) -
                                                    bandgap_fs(350.0, R1, R2)) < 1e-8, "")

sys.exit(v.finish())
