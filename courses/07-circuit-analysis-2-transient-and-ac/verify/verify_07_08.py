#!/usr/bin/env python3
"""Verify every published number in chapter 07-08 (worked examples, numbers to know, practitioner
lens), its problem solutions and its lab handout.

Independent routes: the chapter uses closed-form resonance, Butterworth and Sallen-Key formulas.
Here every circuit is re-solved by a small modified-nodal-analysis (MNA) solver at each frequency,
built from the netlist of elements rather than from any transfer function; peaks, half-power and
-3 dB frequencies come from numerical search; Butterworth section Q values come from the roots of
1 + (-s^2)^n; stored and dissipated energies come from integrating sampled waveforms over a period;
and the finite-GBW filter uses an op-amp whose gain A(jw) enters the MNA matrix directly.
ngspice netlists in labs/07-08-lab are run separately by tools/run_spice.py.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.optimize import brentq, fsolve, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "07-08",
    COURSE / "chapters" / "07-08-filters-and-resonance.md",
    COURSE / "solutions" / "07-08-solutions.md",
    COURSE / "labs" / "07-08-lab" / "README.md",
)
pi = math.pi
dB = lambda z: 20 * math.log10(abs(z))  # noqa: E731
deg = lambda z: math.degrees(cmath.phase(z))  # noqa: E731


def mna(elements, f, out, inp="in"):
    """Solve a linear circuit at frequency f (Hz). Elements: (kind, n1, n2, value[, extra]).
    kinds: R, L, C (two-terminal), V (source, value = phasor, from n1(+) to n2), E (VCVS: n1, n2 out;
    extra = (nc1, nc2), value = gain, may be complex). Node '0' is ground. Returns V(out)/V(source)."""
    nodes = sorted({n for e in elements for n in e[1:3] if n != "0"}
                   | {n for e in elements if e[0] == "E" for n in e[4] if n != "0"})
    idx = {n: i for i, n in enumerate(nodes)}
    vsrc = [e for e in elements if e[0] in ("V", "E")]
    N, M = len(nodes), len(vsrc)
    A = np.zeros((N + M, N + M), dtype=complex)
    b = np.zeros(N + M, dtype=complex)
    s = 2j * pi * f

    def stamp_y(n1, n2, y):
        for a, sgn_a in ((n1, 1), (n2, -1)):
            if a == "0":
                continue
            for c, sgn_c in ((n1, 1), (n2, -1)):
                if c == "0":
                    continue
                A[idx[a], idx[c]] += sgn_a * sgn_c * y

    for e in elements:
        k, n1, n2, val = e[0], e[1], e[2], e[3]
        if k == "R":
            stamp_y(n1, n2, 1 / val)
        elif k == "L":
            stamp_y(n1, n2, 1 / (s * val))
        elif k == "C":
            stamp_y(n1, n2, s * val)
    for j, e in enumerate(vsrc):
        k, n1, n2, val = e[0], e[1], e[2], e[3]
        r = N + j
        for n, sgn in ((n1, 1), (n2, -1)):
            if n != "0":
                A[idx[n], r] += sgn
                A[r, idx[n]] += sgn
        if k == "V":
            b[r] = val
        else:
            nc1, nc2 = e[4]
            for n, sgn in ((nc1, 1), (nc2, -1)):
                if n != "0":
                    A[r, idx[n]] -= sgn * val
    x = np.linalg.solve(A, b)
    vin = 1.0
    return x[idx[out]] / vin if out != "0" else 0.0


def peak_search(fun, lo, hi):
    r = minimize_scalar(lambda lf: -abs(fun(10**lf)), bounds=(math.log10(lo), math.log10(hi)), method="bounded",
                        options={"xatol": 1e-13})
    return 10**r.x, abs(fun(10**r.x))


# ================================================================================ Example 1 (series RLC)
R1_, L1_, C1_ = 10.0, 100e-6, 100e-12
ser = lambda f: (1 - mna([("V", "in", "0", 1.0), ("R", "in", "a", R1_), ("L", "a", "b", L1_),  # noqa: E731
                          ("C", "b", "0", C1_)], f, "a")) / R1_  # current per volt, through R
fpk, ipk = peak_search(ser, 1e6, 3e6)
v.check("Ex 07-08.1a", fpk / 1e6)
v.check("Ex 07-08.1b", math.sqrt(L1_ / C1_))
half = lambda f: abs(ser(f)) - ipk / math.sqrt(2)  # noqa: E731
f1, f2 = brentq(half, 1e6, fpk), brentq(half, fpk, 3e6)
v.check("Ex 07-08.1c", fpk / (f2 - f1), tol=0.5)
v.check("Ex 07-08.1d", (f2 - f1) / 1e3)
v.check("Ex 07-08.1e", f1 / 1e6)
v.check("Ex 07-08.1f", f2 / 1e6)
v.check("Ex 07-08.1g", ipk * 10e-3 * 1e3)
VC = abs(ser(fpk)) * 10e-3 / (2 * pi * fpk * C1_)
v.check("Ex 07-08.1h", VC)
# energies by sampling the waveforms over one period at resonance
t = np.linspace(0, 1 / fpk, 20001)
Im = ipk * 10e-3
i_t = Im * np.cos(2 * pi * fpk * t)
vC_t = Im / (2 * pi * fpk * C1_) * np.sin(2 * pi * fpk * t)
w_t = 0.5 * L1_ * i_t**2 + 0.5 * C1_ * vC_t**2
v.check("Ex 07-08.1i", w_t.mean() * 1e12)
v.assert_true("stored energy constant at resonance", np.ptp(w_t) / w_t.mean() < 1e-6)
Ecyc = np.trapezoid(i_t**2 * R1_, t)
v.check("Ex 07-08.1j", Ecyc * 1e12)
v.check("Ex 07-08.1k", 2 * pi * w_t.mean() / Ecyc)

# ================================================================================ Example 2 (loaded tank)
f0e2, Lc, Qc = 10.7e6, 1e-6, 80
rc = 2 * pi * f0e2 * Lc / Qc
v.check("Ex 07-08.2a", rc)
v.check("Ex 07-08.2k", 2 * pi * 10.7e6 * 1e-6)
Zcoil = 1j * 2 * pi * 10.7e6 * 1e-6 + 2 * pi * 10.7e6 * 1e-6 / 80
v.check("Ex 07-08.2l", 1e6 * (-1 / (1 / Zcoil).imag) / (2 * pi * 10.7e6))
v.check("Ex 07-08.2b", rc * (1 + Qc**2))
# choose C so the coil (r + jwL) in parallel with C has zero susceptance at 10.7 MHz
Yc = 1 / (rc + 2j * pi * f0e2 * Lc)
Ct = -Yc.imag / (2 * pi * f0e2)
v.check("Ex 07-08.2c", Ct * 1e12)
tank = lambda f: mna([("V", "in", "0", 1.0), ("R", "in", "x", 1e12), ("R", "x", "0", 20e3), ("R", "x", "0", 10e3),  # noqa: E731
                      ("C", "x", "0", Ct), ("R", "x", "m", rc), ("L", "m", "0", Lc)], f, "x") * 1e12
Rt = abs(tank(f0e2))
v.check("Ex 07-08.2d", Rt)
pk2, zpk = peak_search(tank, 9e6, 12e6)
fa = brentq(lambda f: abs(tank(f)) - zpk / math.sqrt(2), 9e6, pk2)
fb = brentq(lambda f: abs(tank(f)) - zpk / math.sqrt(2), pk2, 12e6)
v.check("Ex 07-08.2e", pk2 / (fb - fa))
v.check("Ex 07-08.2f", (fb - fa) / 1e3)
v.check("Ex 07-08.2g", f0e2 / Qc / 1e3)
# power shares: currents into each branch at resonance with 1 A drive
Vx = tank(f0e2) * 1.0
P_coil = 0.5 * abs(Vx / (rc + 2j * pi * f0e2 * Lc)) ** 2 * rc
P_src, P_load = 0.5 * abs(Vx) ** 2 / 20e3, 0.5 * abs(Vx) ** 2 / 10e3
Ptot = P_coil + P_src + P_load
v.check("Ex 07-08.2h", P_coil / Ptot * 100)
v.check("Ex 07-08.2i", P_src / Ptot * 100)
v.check("Ex 07-08.2j", P_load / Ptot * 100)

# ================================================================================ Example 3 (Butterworth LC)
R0, fc3 = 50.0, 10e6
L3, C3 = math.sqrt(2) * R0 / (2 * pi * fc3), math.sqrt(2) / (R0 * 2 * pi * fc3)
v.check("Ex 07-08.3a", L3 * 1e6)
v.check("Ex 07-08.3b", C3 * 1e12)
lp2 = lambda f: mna([("V", "in", "0", 1.0), ("R", "in", "a", R0), ("L", "a", "o", L3), ("C", "o", "0", C3),  # noqa: E731
                     ("R", "o", "0", R0)], f, "o")
g0 = dB(lp2(1.0))
v.check("Ex 07-08.3c", g0)
for f, ia, ir, ip in ((10e6, "d", "e", "f"), (30e6, "g", "h", "i"), (100e6, "j", "k", "l")):
    v.check(f"Ex 07-08.3{ia}", dB(lp2(f)))
    v.check(f"Ex 07-08.3{ir}", dB(lp2(f)) - g0)
    v.check(f"Ex 07-08.3{ip}", deg(lp2(f)))

# ================================================================================ Example 4 (order)


def bw_q(n):
    """Q values of the Butterworth pole pairs, from the roots of 1 + (-s^2)^n (left half)."""
    coeffs = np.zeros(2 * n + 1)
    coeffs[0] = (-1) ** n
    coeffs[-1] = 1
    roots = np.roots(coeffs)
    lhp = roots[roots.real < -1e-9]
    qs = sorted({round(abs(r) / (-2 * r.real), 10) for r in lhp if abs(r.imag) > 1e-9})
    return qs, int(np.sum(np.abs(lhp.imag) < 1e-9))


nreq = math.log10(10**4 - 1) / (2 * math.log10(5))
v.check("Ex 07-08.4a", nreq)
n4 = math.ceil(nreq)
v.check("Ex 07-08.4b", n4)
qs3, nreal3 = bw_q(3)
v.check("Ex 07-08.4c", qs3[0])
v.assert_true("third order has one real pole", nreal3 == 1)
v.check("Ex 07-08.4d", -dB(1 / math.sqrt(1 + 5**6)))
v.check("Ex 07-08.4e", -dB(1 / math.sqrt(1 + 5**4)))


# ================================================================================ Example 5 (Sallen-Key by MNA)
def sk_lp(R1, R2, C1, C2, K=1.0):
    """Sallen-Key low-pass: in-R1-A-R2-B, C2 B-gnd, C1 A-out, out = K*V(B) (ideal VCVS)."""
    return lambda f: mna([("V", "in", "0", 1.0), ("R", "in", "A", R1), ("R", "A", "B", R2), ("C", "B", "0", C2),  # noqa: E731
                          ("C", "A", "out", C1), ("E", "out", "0", K, ("B", "0"))], f, "out")


def f0_q(H, lo, hi):
    """Natural frequency from the -90 deg phase crossing, Q from |H(f0)|/|H(0)|."""
    f0 = brentq(lambda f: deg(H(f) / H(1e-3)) + 90, lo, hi)
    return f0, abs(H(f0)) / abs(H(1e-3))


v.check("Ex 07-08.5a", 2 * 10e-9 * 1e9)
Rex = brentq(lambda R: f0_q(sk_lp(R, R, 20e-9, 10e-9), 10, 1e5)[0] - 1e3, 1e3, 1e5)
v.check("Ex 07-08.5b", Rex / 1e3)
H5 = sk_lp(11.3e3, 11.3e3, 20e-9, 10e-9)
f05, q5 = f0_q(H5, 10, 1e5)
v.check("Ex 07-08.5c", f05)
v.assert_true("Q is 0.7071 with equal resistors", abs(q5 - 1 / math.sqrt(2)) < 1e-6)
v.check("Ex 07-08.5d", dB(H5(1e3)))
f0lo, qlo = f0_q(sk_lp(11.3e3, 11.3e3, 18e-9, 10e-9), 10, 1e5)
f0hi, qhi = f0_q(sk_lp(11.3e3, 11.3e3, 22e-9, 10e-9), 10, 1e5)
v.check("Ex 07-08.5e", qlo)
v.check("Ex 07-08.5f", f0lo)
v.check("Ex 07-08.5g", qhi)
v.check("Ex 07-08.5h", f0hi)
Kb = brentq(lambda K: f0_q(sk_lp(10e3, 10e3, 10e-9, 10e-9, K), 10, 1e5)[1] - 1 / math.sqrt(2), 1.0, 2.9)
v.check("Ex 07-08.5i", Kb)
v.check("Ex 07-08.5j", Kb - 1)
v.check("Ex 07-08.5k", dB(Kb))


# ================================================================================ Example 6 (insertion loss by MNA)
def il(Qu, QL, R=50.0, f0=2e9):
    """One parallel resonator between equal terminations, Z0 chosen to give QL; loss at f0 in dB."""
    # QL = (Rp || R/2)/Z0 and Qu = Rp/Z0  ->  Rp from the ratio, then Z0
    Rp = (R / 2) * (Qu / QL - 1)
    Z0 = Rp / Qu
    L, C = Z0 / (2 * pi * f0), 1 / (Z0 * 2 * pi * f0)
    with_res = mna([("V", "in", "0", 1.0), ("R", "in", "x", R), ("R", "x", "0", R), ("R", "x", "0", Rp),
                    ("L", "x", "0", L), ("C", "x", "0", C)], f0, "x")
    return -dB(with_res / 0.5)


v.check("Ex 07-08.6a", 2000 / 20)
v.check("Ex 07-08.6b", il(200, 100))
v.check("Ex 07-08.6c", il(1000, 100))
v.check("Ex 07-08.6d", il(2000, 100))
v.check("Ex 07-08.6e", 4 * il(200, 100), tol=0.5)

# ================================================================================ Problems
# P1: read w0 and Q from denominators by root finding
for den, iw, iq in (([1, 1000, 1e6], "a", "b"), ([1, 200, 1e6], None, "c"), ([1, 50, 1e6], None, "d"),
                    ([1, 400, 4e6], "e", "f"), ([1, 100, 1e4], "g", "h")):
    r = np.roots(den)[0]
    w0, Q = abs(r), abs(r) / (-2 * r.real)
    if iw:
        v.check(f"07-08.1{iw}", w0)
    v.check(f"07-08.1{iq}", Q)
# P2
ser2 = lambda f: mna([("V", "in", "0", 1.0), ("R", "in", "a", 20), ("L", "a", "b", 2e-3), ("C", "b", "0", 50e-9)], f, "a")  # noqa: E731
i2 = lambda f: (1 - ser2(f)) / 20  # noqa: E731
fp2, ip2 = peak_search(i2, 5e3, 5e4)
a2 = brentq(lambda f: abs(i2(f)) - ip2 / math.sqrt(2), 5e3, fp2)
b2 = brentq(lambda f: abs(i2(f)) - ip2 / math.sqrt(2), fp2, 5e4)
v.check("07-08.2a", fp2 / 1e3)
v.check("07-08.2b", fp2 / (b2 - a2))
v.check("07-08.2c", (b2 - a2) / 1e3)
v.check("07-08.2d", a2 / 1e3)
v.check("07-08.2e", b2 / 1e3)
v.check("07-08.2f", (fp2 - a2) / 1e3)
v.check("07-08.2g", (b2 - fp2) / 1e3)
# P3: parallel RLC driven by a 1 A source (1 TOhm source resistor trick)
par3 = lambda f: mna([("V", "in", "0", 1.0), ("R", "in", "x", 1e12), ("R", "x", "0", 10e3), ("L", "x", "0", 1e-3),  # noqa: E731
                      ("C", "x", "0", 10e-9)], f, "x") * 1e12
fp3, zp3 = peak_search(par3, 1e4, 2e5)
a3 = brentq(lambda f: abs(par3(f)) - zp3 / math.sqrt(2), 1e4, fp3)
b3 = brentq(lambda f: abs(par3(f)) - zp3 / math.sqrt(2), fp3, 2e5)
v.check("07-08.3a", fp3 / 1e3)
v.check("07-08.3b", fp3 / (b3 - a3))
v.check("07-08.3c", (b3 - a3) / 1e3)
v.check("07-08.3d", zp3 / 1e3)
v.check("07-08.3e", abs(par3(a3)) / 1e3)
v.check("07-08.3f", deg(par3(a3)), tol=0.5)
v.check("07-08.3g", deg(par3(b3)), tol=0.5)
# P4: energy by sampling
L4, C4, R4, Im4 = 10e-3, 1e-6, 5.0, 0.1
f04 = 1 / (2 * pi * math.sqrt(L4 * C4))
v.check("07-08.4a", f04 / 1e3)
t4 = np.linspace(0, 1 / f04, 20001)
i4 = Im4 * np.cos(2 * pi * f04 * t4)
vc4 = Im4 / (2 * pi * f04 * C4) * np.sin(2 * pi * f04 * t4)
W4 = (0.5 * L4 * i4**2 + 0.5 * C4 * vc4**2).mean()
E4 = np.trapezoid(i4**2 * R4, t4)
v.check("07-08.4b", W4 * 1e6)
v.check("07-08.4c", E4 * 1e6)
v.check("07-08.4d", 2 * pi * W4 / E4)
# P5
ser5 = lambda f: mna([("V", "in", "0", 3.0), ("R", "in", "a", 8.0), ("L", "a", "b", 1e-3), ("C", "b", "0", 10e-9)], f, "b") * 3.0  # noqa: E731
fp5, vc5 = peak_search(lambda f: mna([("V", "in", "0", 1.0), ("R", "in", "a", 8.0), ("L", "a", "b", 1e-3),
                                       ("C", "b", "0", 10e-9)], f, "b"), 1e4, 2e5)
f05 = 1 / (2 * pi * math.sqrt(1e-3 * 10e-9))
v.check("07-08.5a", f05 / 1e3)
vcr = abs(mna([("V", "in", "0", 1.0), ("R", "in", "a", 8.0), ("L", "a", "b", 1e-3), ("C", "b", "0", 10e-9)], f05, "b"))
v.check("07-08.5b", vcr)
v.check("07-08.5c", 3 * vcr)
v.check("07-08.5d", 3 * vcr * math.sqrt(2))
Rmin = brentq(lambda R: 3 * abs(mna([("V", "in", "0", 1.0), ("R", "in", "a", R), ("L", "a", "b", 1e-3),
                                      ("C", "b", "0", 10e-9)], f05, "b")) - 40, 1, 200)
v.check("07-08.5e", Rmin)
# P6
Q6 = pi * 20
v.check("07-08.6a", Q6)
v.check("07-08.6b", 1e6 / Q6 / 1e3)
v.check("07-08.6c", 2 * Q6 / (2 * pi * 1e6) * 1e6)
# P7: third-order prototype scaled, MNA
R7, fc7 = 50.0, 100e6
L7, C7 = 1 * R7 / (2 * pi * fc7), 2 / (R7 * 2 * pi * fc7)
v.check("07-08.7a", L7 * 1e9)
v.check("07-08.7b", C7 * 1e12)
lp3 = lambda f: mna([("V", "in", "0", 1.0), ("R", "in", "a", R7), ("L", "a", "b", L7), ("C", "b", "0", C7),  # noqa: E731
                     ("L", "b", "o", L7), ("R", "o", "0", R7)], f, "o")
v.check("07-08.7c", dB(lp3(fc7)))
v.check("07-08.7d", dB(lp3(fc7)) - dB(lp3(1.0)))
v.check("07-08.7e", deg(lp3(fc7)) if deg(lp3(fc7)) < 0 else deg(lp3(fc7)) - 360)
v.check("07-08.7f", dB(lp3(3 * fc7)))
v.check("07-08.7g", dB(lp3(3 * fc7)) - dB(lp3(1.0)))
# P8
n8 = math.log10(10**5 - 1) / (2 * math.log10(5))
v.check("07-08.8a", n8)
v.check("07-08.8b", math.ceil(n8))
qs4, _ = bw_q(4)
v.check("07-08.8c", max(qs4))
v.check("07-08.8d", min(qs4))
v.check("07-08.8e", 10 * math.log10(1 + 5**8))
# P9
H9 = sk_lp(10e3, 10e3, 22e-9, 10e-9)
f09, q9 = f0_q(H9, 10, 1e5)
v.check("07-08.9a", f09 / 1e3)
v.check("07-08.9b", q9)
fp9, pk9 = peak_search(H9, 30, 3e3)
v.check("07-08.9c", dB(pk9))
v.check("07-08.9d", fp9)
v.check("07-08.9e", 1 / (2 * q9))
v.check("07-08.9f", 10 ** (dB(pk9) / 20))
# P10
f010, _ = f0_q(sk_lp(10e3, 10e3, 10e-9, 10e-9, 1.5), 10, 1e5)
v.check("07-08.10a", f010 / 1e3)
for Qt, ik, ir, idb in ((1 / math.sqrt(2), "b", "c", "d"), (1.0, "e", "f", "g")):
    K = brentq(lambda K: f0_q(sk_lp(10e3, 10e3, 10e-9, 10e-9, K), 10, 1e5)[1] - Qt, 1.0, 2.9)
    v.check(f"07-08.10{ik}", K)
    v.check(f"07-08.10{ir}", K - 1)
    v.check(f"07-08.10{idb}", dB(K))
# P11: Sallen-Key high-pass by MNA
Ch = 100e-9


def sk_hp(R1, R2):
    return lambda f: mna([("V", "in", "0", 1.0), ("C", "in", "A", Ch), ("C", "A", "B", Ch), ("R", "B", "0", R2),  # noqa: E731
                          ("R", "A", "out", R1), ("E", "out", "0", 1.0, ("B", "0"))], f, "out")


def hp_f0_q(H):
    f0 = brentq(lambda f: deg(H(f)) - 90, 1, 1e4)
    return f0, abs(H(f0))


R1h = brentq(lambda R1: hp_f0_q(sk_hp(R1, 2 * R1))[0] - 100, 1e3, 1e5)
v.check("07-08.11a", R1h / 1e3)
v.check("07-08.11b", 2 * R1h / 1e3)
v.assert_true("HP Q = 0.7071 with R2 = 2 R1", abs(hp_f0_q(sk_hp(R1h, 2 * R1h))[1] - 1 / math.sqrt(2)) < 1e-9)
Hh = sk_hp(R1h, 2 * R1h)
v.check("07-08.11c", dB(Hh(10)))
v.check("07-08.11d", dB(Hh(100)))
v.check("07-08.11e", dB(Hh(1000)), tol=0.005)
v.check("07-08.11f", dB(Hh(1000)), tol=0.00005)
# P12: notch by MNA
C12 = 1 / ((2 * pi * 1e6) ** 2 * 100e-6)
v.check("07-08.12a", C12 * 1e12)
v.check("07-08.12b", math.sqrt(100e-6 / C12))
H12 = lambda f: mna([("V", "in", "0", 1.0), ("R", "in", "o", 50), ("L", "o", "m", 100e-6), ("C", "m", "0", C12)], f, "o")  # noqa: E731
lo12 = brentq(lambda f: abs(H12(f)) - 1 / math.sqrt(2), 1e5, 0.99999e6)
hi12 = brentq(lambda f: abs(H12(f)) - 1 / math.sqrt(2), 1.00001e6, 1e7)
v.check("07-08.12c", 1e6 / (hi12 - lo12))
v.check("07-08.12d", (hi12 - lo12) / 1e3)
v.check("07-08.12e", lo12 / 1e3)
v.check("07-08.12f", hi12 / 1e3)
v.check("07-08.12g", dB(H12(990e3)))
v.assert_true("notch edges geometric about 1 MHz", abs(lo12 * hi12 / 1e12 - 1) < 1e-9)
# P13
v.check("07-08.13a", il(100, 50))
v.check("07-08.13b", il(1000, 50))
v.check("07-08.13c", brentq(lambda q: il(q, 50) - 1.0, 60, 1e4))
# P14: third-order active filter with op-amp followers in the MNA matrix
fc14 = 10e3
Rrc = 1 / (2 * pi * fc14 * 1e-9)
Rsk = 1 / (2 * pi * fc14 * math.sqrt(4e-9 * 1e-9))
v.check("07-08.14a", Rrc / 1e3)
v.check("07-08.14b", 4 * 1e-9 * 1e9)
v.check("07-08.14c", Rsk / 1e3)


def third(f, gbw=None, A0=1e5):
    if gbw is None:
        A = 1e12
    else:
        A = A0 / (1 + 2j * pi * f * A0 / (2 * pi * gbw))
    els = [("V", "in", "0", 1.0), ("R", "in", "p1", Rrc), ("C", "p1", "0", 1e-9),
           ("E", "o1", "0", A, ("p1", "o1")),
           ("R", "o1", "A", Rsk), ("R", "A", "B", Rsk), ("C", "B", "0", 1e-9), ("C", "A", "o2", 4e-9),
           ("E", "o2", "0", A, ("B", "o2"))]
    return mna(els, f, "o2")


v.check("07-08.14d", dB(third(fc14)))
v.check("07-08.14e", dB(third(20e3)))
g1, g100 = dB(third(fc14, 1e6)), dB(third(fc14, 100e3))
v.check("07-08.14f", g1)
v.check("07-08.14g", abs(g1 - dB(third(fc14))))
v.check("07-08.14h", g100)
v.check("07-08.14i", abs(g100 - dB(third(fc14))))
gbw01 = brentq(lambda g: abs(dB(third(fc14, g)) - dB(third(fc14))) - 0.01, 2e5, 1e7)
v.check("07-08.14j", gbw01 / 1e3, tol=5)
v.check("07-08.14k", gbw01 / fc14, tol=0.5)

# ================================================================================ Numbers to know (section 7)


def q_sensitivity(Qt, h=1e-6):
    """(dQ/Q)/(dK/K) of the equal-component section, by finite difference of the MNA-measured Q."""
    K = brentq(lambda K: f0_q(sk_lp(10e3, 10e3, 10e-9, 10e-9, K), 10, 1e5)[1] - Qt, 1.0, 2.99)
    q = lambda k: f0_q(sk_lp(10e3, 10e3, 10e-9, 10e-9, k), 10, 1e5)[1]  # noqa: E731
    return (q(K * (1 + h)) - q(K * (1 - h))) / (2 * h * q(K))


v.check("N 07-08.a", q_sensitivity(1 / math.sqrt(2)))
v.check("N 07-08.b", q_sensitivity(3.0), tol=0.5)
for n, idq in ((2, ("c",)), (3, ("d",)), (4, ("e", "f")), (5, ("g", "h"))):
    qs, _ = bw_q(n)
    for ident, q in zip(idq, qs):
        v.check(f"N 07-08.{ident}", q)
v.check("N 07-08.i", -dB(1 / (1 + 5j)), tol=0.5)  # one real pole, exact, at five times its corner
v.check("N 07-08.j", 20 * math.log10(2**12))
v.check("N 07-08.k", 20 * math.log10(2**13))

# ================================================================================ Practitioner lens (section 9)
Kw = 1 + 1.9 * 1.01 / 0.99
v.check("PL 07-08.a", f0_q(sk_lp(10e3, 10e3, 10e-9, 10e-9, Kw), 10, 1e5)[1])
v.check("PL 07-08.b", 1 / (2 * pi * 100 * 47e-9) / 1e3)
v.check("PL 07-08.c", 100 * 1.0 * 1.0 * 10e3 / 1e6)
v.check("PL 07-08.d", 20 * math.log10(4095 / 4096) * 1e3)
v.check("PL 07-08.e", 1 / (2 * pi * 5e6 * 1e-14) / 1e6, tol=0.05)
v.assert_true("Q*f = 16 million gives 3.2 million at 5 MHz", abs(16e6 / 5 - 3.2e6) < 1)
wl = 2 * pi * 433.92e6 * 63.8e-6
v.check("PL 07-08.f", wl / 19.4)
v.check("PL 07-08.g", wl / (19.4 + 100))
# series resonator in a 50-ohm path, by MNA at resonance
fS = 1 / (2 * pi * math.sqrt(63.8e-6 * 2.11e-15))
ser_saw = mna([("V", "in", "0", 1.0), ("R", "in", "a", 50), ("R", "a", "b", 19.4), ("L", "b", "c", 63.8e-6),
               ("C", "c", "o", 2.11e-15), ("R", "o", "0", 50)], fS, "o")
v.check("PL 07-08.h", -dB(ser_saw / 0.5))
v.check("PL 07-08.i", 5e12 / 2e9)
v.check("PL 07-08.j", 5e12 / 5e9)
v.check("PL 07-08.k", (4200 - 3300) / ((4200 + 3300) / 2) * 100, tol=0.5)
v.check("PL 07-08.l", (7.125 - 5.925) / ((7.125 + 5.925) / 2) * 100)
v.check("PL 07-08.m", -dB(lp2(fc3 / 2) / lp2(1.0)))

# ================================================================================ Lab handout


def sk_gbw(f, gbw, A0=1e5):
    A = A0 / (1 + 2j * pi * f * A0 / (2 * pi * gbw))
    return mna([("V", "in", "0", 1.0), ("R", "in", "A", 11.3e3), ("R", "A", "B", 11.3e3), ("C", "B", "0", 10e-9),
                ("C", "A", "out", 20e-9), ("E", "out", "0", A, ("B", "out"))], f, "out")


v.check("Lab 07-08.a", dB(sk_gbw(1e3, 100e3)))
v.check("Lab 07-08.b", dB(sk_gbw(1e3, 10e3)))
v.check("Lab 07-08.c", fpk / (f2 - f1) / pi, tol=0.5)
qs6, _ = bw_q(6)
v.check("Lab 07-08.d", max(qs6))
v.check("Lab 07-08.e", brentq(lambda q: il(q, 100) - 0.5, 150, 1e5))

# Example 1 (audit addition): average power and period at resonance, from the series circuit itself
L1e, C1e, R1e = 100e-6, 100e-12, 10.0
f01 = brentq(lambda f: (2j * pi * f * L1e + 1 / (2j * pi * f * C1e)).imag, 1e6, 3e6)
I1 = 10e-3 / abs(R1e + 2j * pi * f01 * L1e + 1 / (2j * pi * f01 * C1e))
v.check("Ex 07-08.1l", 1e6 * 0.5 * I1 ** 2 * R1e)
v.check("Ex 07-08.1m", 1e9 / f01)

# ---- Example 6 (audit addition): four-resonator Butterworth band-pass ladder with lossy resonators
g4 = [2 * math.sin((2 * k - 1) * pi / 8) for k in range(1, 5)]
v.check("Ex 07-08.6i", sum(g4))


def ladder_loss(Qu, f0=2e9, wfrac=0.01, R0=50.0):
    w0 = 2 * pi * f0
    els = [("V", "s", "0", 1.0), ("R", "s", "n0", R0)]
    node = "n0"
    for k, gk in enumerate(g4):
        if k % 2 == 0:   # shunt parallel resonator at the current node
            Cs, Ls = gk / (R0 * w0 * wfrac), R0 * wfrac / (w0 * gk)
            els += [("C", node, "0", Cs), ("L", node, "0", Ls), ("R", node, "0", Qu / (w0 * Cs))]
        else:            # series resonator to a new node
            Ls, Cs = gk * R0 / (w0 * wfrac), wfrac / (w0 * gk * R0)
            nxt = f"n{k}"
            els += [("R", node, f"r{k}", w0 * Ls / Qu), ("L", f"r{k}", f"m{k}", Ls), ("C", f"m{k}", nxt, Cs)]
            node = nxt
    els += [("R", node, "0", R0)]
    return -dB(2 * mna(els, f0, node, inp="s"))


v.check("Ex 07-08.6f", ladder_loss(200))
v.check("Ex 07-08.6g", ladder_loss(2000))
v.check("Ex 07-08.6h", 4.343 * 100 * sum(g4) / 200)

# ---- Example 7 (audit addition): voice-band cascade, components found by fitting the Butterworth response


def hp_sec(R1, R2, Cc=100e-9):
    return [("C", "in", "A", Cc), ("C", "A", "B", Cc), ("R", "B", "0", R2), ("R", "A", "h", R1),
            ("E", "h", "0", 1.0, ("B", "0"))]


def mfb_sec(C1, C2, R=10e3, inp="h"):
    return [("R", inp, "P", R), ("C", "P", "0", C1), ("R", "P", "out", R), ("R", "P", "N", R),
            ("C", "N", "out", C2), ("E", "out", "0", -1e8, ("N", "0"))]


def bw_fit(build, fc, node, x0, hp=False):
    def err(x):
        H = [abs(mna([("V", "in", "0", 1.0)] + build(*x), f, node)) for f in (fc, 2 * fc if not hp else fc / 2)]
        ref = [1 / math.sqrt(2), 1 / math.sqrt(1 + 2.0 ** 4)]
        return [H[0] - ref[0], H[1] - ref[1]]
    return fsolve(err, x0, xtol=1e-12)


R1h, R2h = bw_fit(lambda a, b: hp_sec(a * 1e3, b * 1e3), 300, "h", [3.0, 6.0], hp=True)
v.check("Ex 07-08.7a", R1h)
v.check("Ex 07-08.7b", R2h)
C1m, C2m = bw_fit(lambda a, b: mfb_sec(a * 1e-9, b * 1e-9, inp="in"), 3400, "out", [10.0, 2.0])
v.check("Ex 07-08.7c", C2m)
v.check("Ex 07-08.7d", C1m)
casc = [("V", "in", "0", 1.0)] + hp_sec(R1h * 1e3, R2h * 1e3) + mfb_sec(C1m * 1e-9, C2m * 1e-9)
for f, k in ((50, "Ex 07-08.7e"), (300, "Ex 07-08.7f"), (1000, "Ex 07-08.7g"), (3400, "Ex 07-08.7h"), (20e3, "Ex 07-08.7i")):
    v.check(k, dB(mna(casc, f, "out")))
v.check("Ex 07-08.7j", deg(mna(casc, 1000, "out")))

# P15-P17 (audit additions)
f15, L15 = 10e6, 1e-6
C15 = brentq(lambda C: 1 / (2 * pi * f15 * L15) - 2 * pi * f15 * C, 1e-12, 1e-9)
Rp15 = 100 * 2 * pi * f15 * L15
v.check("07-08.15a", C15 * 1e12)
v.check("07-08.15b", math.sqrt(L15 / C15))
v.check("07-08.15c", Rp15)
tank = lambda f, load=True: mna([("V", "in", "0", 1.0), ("R", "in", "x", 1e3), ("L", "x", "0", L15), ("C", "x", "0", C15),  # noqa: E731
                                 ("R", "x", "0", Rp15)] + ([("R", "x", "0", 2e3)] if load else []), f, "x")
v.check("07-08.15d", Rp15 / math.sqrt(L15 / C15))
Rt15 = 1 / (1 / Rp15 + 1e-3 + 5e-4)
v.check("07-08.15e", Rt15)
pk15 = abs(tank(f15))
lo15 = brentq(lambda f: abs(tank(f)) - pk15 / math.sqrt(2), 5e6, f15)
hi15 = brentq(lambda f: abs(tank(f)) - pk15 / math.sqrt(2), f15, 2e7)
v.check("07-08.15g", (hi15 - lo15) / 1e6)
v.check("07-08.15f", f15 / (hi15 - lo15), tol=0.01)
vx = abs(tank(f15))
pcoil, pload = vx ** 2 / Rp15, vx ** 2 / 2e3
v.check("07-08.15h", 100 * pcoil / (pcoil + pload))
v.check("07-08.15i", 100 * pload / (pcoil + pload))
direct = abs(mna([("V", "in", "0", 1.0), ("R", "in", "x", 1e3), ("R", "x", "0", 2e3)], f15, "x"))
v.check("07-08.15j", -dB(vx / direct))


def mfb16(f, C1, C2):
    return mna([("V", "in", "0", 1.0), ("R", "in", "P", 10e3), ("C", "P", "0", C1), ("R", "P", "out", 20e3),
                ("R", "P", "N", 20e3), ("C", "N", "out", C2), ("E", "out", "0", -1e8, ("N", "0"))], f, "out")


def fit16(x):
    c1, c2 = x[0] * 1e-9, x[1] * 1e-12
    return [abs(mfb16(f, c1, c2)) / 2 - 1 / math.sqrt(1 + (f / 1e4) ** 4) for f in (1e4, 2e4)]


c1n, c2n = fsolve(fit16, [2.0, 300.0], xtol=1e-12)
v.check("07-08.16b", c2n)
v.check("07-08.16c", c1n)
v.check("07-08.16a", c1n * 1e3 / c2n)
v.check("07-08.16d", dB(mfb16(1.0, c1n * 1e-9, c2n * 1e-12)))
v.check("07-08.16e", dB(mfb16(3e4, c1n * 1e-9, c2n * 1e-12)))


def hp17(f, R1, R2, Cc=47e-9):
    return mna([("V", "in", "0", 1.0), ("C", "in", "A", Cc), ("C", "A", "B", Cc), ("R", "B", "0", R2),
                ("R", "A", "out", R1), ("E", "out", "0", 1.0, ("B", "0"))], f, "out")


r1n, r2n = fsolve(lambda x: [abs(hp17(f, x[0] * 1e3, x[1] * 1e3)) - 1 / math.sqrt(1 + (200 / f) ** 4) for f in (200, 100)],
                  [10.0, 20.0], xtol=1e-12)
v.check("07-08.17a", r1n)
v.check("07-08.17b", r2n)
v.check("07-08.17c", -dB(hp17(50, r1n * 1e3, r2n * 1e3)))
v.check("07-08.17d", brentq(lambda n: 10 * math.log10(1 + 4 ** (2 * n)) - 40, 1, 10))
nmin17, _ = signal.buttord(2 * pi * 200, 2 * pi * 50, 3.0103, 40, analog=True)
v.check("07-08.17e", nmin17)
b4, a4 = signal.butter(4, 2 * pi * 200, btype="high", analog=True)
v.check("07-08.17f", -dB(signal.freqs(b4, a4, [2 * pi * 50])[1][0]))

v.finish()
