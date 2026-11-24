#!/usr/bin/env python3
"""Verify every number in chapter 21-09 (the RF front end), its problems and its lab.

Independent routes (the lab module frontend.py uses closed forms and ABCD matrices):
- the anti-resonance is found as the root of the resonator's admittance polynomial (numpy.roots), not from
  sqrt(1 + Cm/C0); the coupling k2_eff is inverted with a Newton iteration instead of Brent's method;
- ladder filters are solved by nodal analysis (an admittance matrix with every motional R, L, C and static C0
  written out), not by ABCD cascading; band edges are bracketed on a dense grid and bisected;
- temperature drift of a filter is modelled by scaling every element value, not by re-evaluating at f/(1+alpha);
- switch on/off responses use the same nodal solver with a resistor or capacitor between the ports;
- mismatch loss is computed through return loss, peak voltage through the forward-wave amplitude;
- the intermodulation product of Problem 21-09.13 is measured by an FFT of two tones through a cubic
  nonlinearity whose coefficient is set by the IIP3;
- ngspice confirms the ladder and the switch separately (ladder.cir, switch.cir via run_spice.py).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "21-09-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("21-09", ROOT / "chapters" / "21-09-rf-front-end.md",
                        ROOT / "solutions" / "21-09-solutions.md", LAB / "README.md")
lg = math.log10
db10 = lambda x: 10 * lg(x)  # noqa: E731
db20 = lambda x: 20 * lg(x)  # noqa: E731
TWO_PI = 2 * math.pi
Z0 = 50.0


# ---------------------------------------------------------------- resonator, independent forms
def k2eff(ratio_fs_fp):
    x = math.pi / 2 * ratio_fs_fp
    return x * math.cos(x) / math.sin(x)


def invert_k2(k2):
    """Newton iteration on u = fs/fp for k2eff(u) = k2; returns fp/fs."""
    u = 0.97
    for _ in range(60):
        h = 1e-9
        g = k2eff(u) - k2
        dg = (k2eff(u + h) - k2eff(u - h)) / (2 * h)
        u -= g / dg
    return 1 / u


def motional(fs, c0, ratio, q):
    cm = c0 / ratio
    lm = 1 / ((TWO_PI * fs) ** 2 * cm)
    return lm, cm, TWO_PI * fs * lm / q


def antiresonance(lm, cm, c0):
    """Lossless resonator admittance Y = jw C0 + 1/(jw Lm + 1/(jw Cm)) vanishes where
    w^2 Lm Cm C0 - (C0 + Cm) = 0: take the positive root of that polynomial in w."""
    roots = np.roots([lm * cm * c0, 0, -(c0 + cm)])
    return max(r.real for r in roots) / TWO_PI


def resonator_y(f, c0, lm, cm, rm):
    w = TWO_PI * f
    return 1j * w * c0 + 1 / (rm + 1j * w * lm + 1 / (1j * w * cm))


# ---------------------------------------------------------------- nodal ladder solver
def nodal_s21(f, sections, scale=1.0):
    """sections: list of (series (c0, lm, cm, rm), shunt (c0, lm, cm, rm)). Each section adds a node; the source
    (50 ohm) drives node 0, the load (50 ohm) sits at the last node. scale divides every L and C (moves all
    resonances up by that factor)."""
    n = len(sections) + 1
    Y = np.zeros((n, n), complex)
    I = np.zeros(n, complex)
    Y[0, 0] += 1 / Z0
    I[0] = 1 / Z0                     # 1 V source through 50 ohm (Norton equivalent)
    for k, (ser, sh) in enumerate(sections):
        c0, lm, cm, rm = ser
        ys = resonator_y(f, c0 / scale, lm / scale, cm / scale, rm)
        Y[k, k] += ys
        Y[k + 1, k + 1] += ys
        Y[k, k + 1] -= ys
        Y[k + 1, k] -= ys
        c0, lm, cm, rm = sh
        Y[k + 1, k + 1] += resonator_y(f, c0 / scale, lm / scale, cm / scale, rm)
    Y[n - 1, n - 1] += 1 / Z0
    V = np.linalg.solve(Y, I)
    return 2 * V[-1]                  # S21 = 2 V_out / V_source


def build_ladder(fs, c0s, c0p, ratio, q, n):
    fp = antiresonance(*motional(fs, c0s, ratio, q)[:2], c0s)
    fsh = fs * fs / fp                # shunt fp = fs means shunt fs = fs / (fp/fs)
    ser = (c0s,) + motional(fs, c0s, ratio, q)
    sh = (c0p,) + motional(fsh, c0p, ratio, q)
    return [(ser, sh)] * n, fsh


def loss(f, sections, scale=1.0):
    return -db20(abs(nodal_s21(f, sections, scale)))


def edges(sections, fc, span, drop=3.0):
    ref = loss(fc, sections)
    out = []
    for a, b in ((fc * (1 - span), fc), (fc, fc * (1 + span))):
        grid = np.linspace(a, b, 4001)
        val = np.array([loss(x, sections) - ref - drop for x in grid])
        idx = np.where(np.sign(val[:-1]) != np.sign(val[1:]))[0]
        i = idx[-1] if a < fc else idx[0]           # crossing nearest the centre
        lo, hi = grid[i], grid[i + 1]
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if np.sign(loss(mid, sections) - ref - drop) == np.sign(loss(lo, sections) - ref - drop):
                lo = mid
            else:
                hi = mid
        out.append(0.5 * (lo + hi))
    return out


# ---------------------------------------------------------------- two-port switch, mismatch, voltage
def series_element_s21(z):
    """A series impedance between two Z0 ports, by the same nodal idea (two nodes)."""
    Y = np.array([[1 / Z0 + 1 / z, -1 / z], [-1 / z, 1 / Z0 + 1 / z]], complex)
    V = np.linalg.solve(Y, np.array([1 / Z0, 0], complex))
    return 2 * V[1]


def mismatch_db(vswr):
    gamma = (vswr - 1) / (vswr + 1)
    rl = -db20(gamma)                               # return loss
    return -db10(1 - 10 ** (-rl / 10))


def v_peak(p_dbm, vswr=1.0):
    vplus = math.sqrt(2 * Z0 * 1e-3 * 10 ** (p_dbm / 10))
    return vplus * (1 + (vswr - 1) / (vswr + 1))


# ================================================================ chapter
print("Text")
v.check("Txt 21-09.a", 4000 / 2e9 * 1e6)
v.check("Txt 21-09.b", 11000 / 2e9 * 1e6)
v.check("Txt 21-09.c", 299792458 / 2e9 * 100)
v.check("Txt 21-09.t", v_peak(33))

print("Example 21-09.1")
FS, C0, Q = 2e9, 1e-12, 2000
FPFS = invert_k2(0.066)
RATIO = 1 / (FPFS ** 2 - 1)
LM, CM, RM = motional(FS, C0, RATIO, Q)
FP = antiresonance(LM, CM, C0)
v.assert_true("polynomial anti-resonance matches the Newton inverse", abs(FP / FS - FPFS) < 1e-12)
v.check("Ex 21-09.1a", FP / 1e9)
v.check("Ex 21-09.1b", (FP / FS - 1) * 100)
v.check("Ex 21-09.1c", C0 / CM)
v.check("Ex 21-09.1d", CM * 1e15)
v.check("Ex 21-09.1e", LM * 1e9)
v.check("Ex 21-09.1f", RM)
v.check("Ex 21-09.1g", (math.pi ** 2 / 4) * (FP - FS) / FP * 100)
v.check("Ex 21-09.1h", k2eff(1 / 1.11) * 100)
v.check("Ex 21-09.1i", (math.pi ** 2 / 4) * 0.11 / 1.11 * 100)

print("Example 21-09.2")
LAD, FSH = build_ladder(FS, 1e-12, 2e-12, RATIO, 2000, 3)
v.check("Ex 21-09.2a", loss(FS, LAD))
lo, hi = edges(LAD, FS, 0.04)
v.check("Ex 21-09.2b", lo / 1e6)
v.check("Ex 21-09.2c", hi / 1e6)
v.check("Ex 21-09.2h", (hi - lo) / 1e6)
v.check("Ex 21-09.2d", loss(1.88e9, LAD))
v.check("Ex 21-09.2e", loss(2.12e9, LAD))
v.check("Ex 21-09.2f", loss(FS, build_ladder(FS, 1e-12, 2e-12, RATIO, 500, 3)[0]))
v.check("Ex 21-09.2g", FSH / 1e9)
v.check("Txt 21-09.d", (FS - FSH) / FS * 100)
v.check("Txt 21-09.e", (FP - FS) / FS * 100)
v.check("Txt 21-09.f", ((hi - lo) / FS) / ((FP - FS) / FS))
v.assert_true("ripple inside the 3 dB band is about 1.5 dB",
              1.3 < max(loss(x, LAD) for x in np.linspace(lo + 5e6, hi - 5e6, 301)) - loss(FS, LAD) < 1.6)

print("Example 21-09.3")
for (a, b), tcf in ((("a", "b"), -40), (("c", "d"), -8), (("e", "f"), 27)):
    d = 1.915e9 * abs(tcf) * 1e-6 * (85 - (-20))
    v.check(f"Ex 21-09.3{a}", d / 1e6)
    v.check(f"Ex 21-09.3{b}", d / 15e6 * 100)

print("Example 21-09.4")
v.check("Ex 21-09.4a", 23 + 2.0)
v.check("Ex 21-09.4b", 25 - 55)
pdc = lambda dbm: 10 ** (dbm / 10) / 0.40  # noqa: E731
v.check("Ex 21-09.4c", pdc(25))
v.check("Ex 21-09.4d", pdc(26.5))
v.check("Ex 21-09.4e", pdc(26.5) - pdc(25))
v.check("Ex 21-09.4f", -135 - (-174 + 3 - 10))

print("Example 21-09.5")
RON, COFF = 2.0, 189e-15
v.check("Ex 21-09.5a", RON * COFF * 1e15)
v.check("Ex 21-09.5b", 1 / (TWO_PI * RON * COFF) / 1e9)
v.check("Ex 21-09.5c", -db20(abs(series_element_s21(RON))))
v.check("Ex 21-09.5d", -db20(abs(series_element_s21(1 / (1j * TWO_PI * 2e9 * COFF)))))
v.check("Ex 21-09.5e", -db20(abs(series_element_s21(1 / (1j * TWO_PI * 0.7e9 * COFF)))))
vp = v_peak(33, 3)
v.check("Ex 21-09.5f", vp)
v.check("Ex 21-09.5g", math.ceil(vp / 2.5))

print("Example 21-09.6")
v.check("Ex 21-09.6a", mismatch_db(3))
v.check("Ex 21-09.6b", mismatch_db(6))
v.check("Ex 21-09.6c", mismatch_db(1.5))
v.check("Ex 21-09.6d", mismatch_db(6) - 0.5 - mismatch_db(1.5))

print("Example 21-09.7")
v.check("Ex 21-09.7a", 3 * 704)
v.check("Ex 21-09.7b", 23 - 45)
floor = -174 + db10(10e6) + 3
v.check("Ex 21-09.7c", floor)
v.check("Ex 21-09.7d", 23 - (floor - 10))

print("Example 21-09.8")
sk, qo = 0.61 * 3959.6, 0.50 * 3678.5
v.check("Ex 21-09.8a", sk)
v.check("Ex 21-09.8b", qo)
v.check("Ex 21-09.8c", sk + qo)
v.check("Ex 21-09.8d", (sk + qo) / (3959.6 + 3678.5) * 100)

print("Practitioner lens")
v.check("Txt 21-09.g", 4.32 * 4.4)
v.check("Txt 21-09.h", 600 / 4700 * 100)
nr = ["n1", "n2", "n3", "n5", "n7", "n8", "n12", "n14", "n20", "n25", "n26", "n28", "n29", "n30", "n66", "n70", "n71",
      "n75", "n38", "n40", "n41", "n48", "n53", "n77", "n78", "n79", "n258", "n260", "n261"]
lte = [1, 2, 3, 4, 5, 7, 8, 12, 13, 14, 17, 18, 19, 20, 25, 26, 28, 29, 30, 32, 66, 71, 106, 34, 38, 39, 40, 41, 42,
       48, 53]
v.assert_true("band lists have no duplicates", len(set(nr)) == len(nr) and len(set(lte)) == len(lte))
v.check("Txt 21-09.i", len(nr))
v.check("Txt 21-09.j", len(lte))
v.check("Txt 21-09.k", 24 + 8)
v.check("Txt 21-09.l", 1 / (TWO_PI * 120e-15) / 1e12)
v.check("Txt 21-09.m", 1 / (TWO_PI * 11.6e-15) / 1e12)
v.check("Txt 21-09.n", 15 / ((1915 + 1930) / 2) * 100)
v.check("Txt 21-09.o", 37 - 31)
v.check("Txt 21-09.p", 3.2 - 2.0)
v.check("Txt 21-09.q", 21 + 18)
v.check("Txt 21-09.r", 0.39 * 15.4)
v.check("Txt 21-09.s", (3959.6 / 4086.9 - 1) * 100)

# ================================================================ problems
print("Problems")
lm, cm, rm = motional(1.8e9, 1.5e-12, 15, 1500)
v.check("21-09.1a", antiresonance(lm, cm, 1.5e-12) / 1e9)
v.check("21-09.1b", cm * 1e15)
v.check("21-09.1c", lm * 1e9)
v.check("21-09.1d", rm)

v.check("21-09.2a", k2eff(3.5 / 3.6) * 100)
v.check("21-09.2b", (math.pi ** 2 / 4) * 0.1 / 3.6 * 100)
v.check("21-09.2c", 1 / ((3.6 / 3.5) ** 2 - 1))

sp = invert_k2(0.075) - 1
v.check("21-09.3a", sp * 100)
v.check("21-09.3b", 2 * sp * 2593)
v.assert_true("Problem 21-09.3c: the bound is below 194 MHz", 2 * sp * 2593 < 194)
sp_need = 194 / (2 * 2593)
v.check("21-09.3d", k2eff(1 / (1 + sp_need)) * 100)

lad4, fsh4 = build_ladder(2.45e9, 0.8e-12, 1.6e-12, 20, 1500, 2)
v.check("21-09.4a", fsh4 / 1e9)
v.check("21-09.4b", loss(2.45e9, lad4))
v.check("21-09.4c", loss(2.30e9, lad4))
v.check("21-09.4d", loss(2.60e9, lad4))

d5 = 1.9e9 * -15e-6 * 115
v.check("21-09.5a", d5 / 1e6)
v.check("21-09.5b", abs(d5) / 20e6 * 100)
v.check("21-09.5c", 0.25 * 20e6 / (1.9e9 * 115) * 1e6)

v.check("21-09.6a", 26 + 2.5)
v.check("21-09.6b", 28.5 - 52)
v.check("21-09.6c", -20 - (28.5 - 52))
v.check("21-09.6d", -138 - (-174 + 2.5 - 6))

p3, p2 = 10 ** 2.6, 10 ** 2.5
v.check("21-09.7a", 23 + 3)
v.check("21-09.7b", 23 + 2)
v.check("21-09.7c", p3 / 0.35)
v.check("21-09.7d", p2 / 0.35)
v.check("21-09.7e", (p3 - p2) / 0.35)
v.check("21-09.7f", 0.3 * (p3 - p2) / 0.35)
v.check("21-09.7g", 0.3 * (p3 - p2) / 0.35 / 3.85)

v.check("21-09.8a", 1.5 * 80)
v.check("21-09.8b", 1 / (TWO_PI * 1.5 * 80e-15) / 1e12)
v.check("21-09.8c", -db20(abs(series_element_s21(1.5))))
v.check("21-09.8d", -db20(abs(series_element_s21(1 / (1j * TWO_PI * 3.5e9 * 80e-15)))))

v.check("21-09.9a", v_peak(26))
v.check("21-09.9b", v_peak(26, 4))
n9 = math.ceil(v_peak(26, 4) / 2.4)
v.check("21-09.9c", n9)
v.check("21-09.9d", n9 ** 2)

ron = 2 * Z0 * (10 ** (0.2 / 20) - 1)
v.check("21-09.10a", ron)
v.check("21-09.10b", 150e-15 / ron * 1e15)
v.check("21-09.10c", -db20(abs(series_element_s21(1 / (1j * TWO_PI * 2.7e9 * 150e-15 / ron)))))
v.check("21-09.10d", -db20(abs(series_element_s21(1 / (1j * TWO_PI * 2.7e9 * 100e-15 / ron)))))

v.check("21-09.11a", mismatch_db(4))
v.check("21-09.11b", mismatch_db(2))
g1 = math.sqrt(1 - 10 ** (-0.1))
v.check("21-09.11c", g1)
v.check("21-09.11d", (1 + g1) / (1 - g1))

v.check("21-09.12a", mismatch_db(5))
v.check("21-09.12b", mismatch_db(2))
v.check("21-09.12c", mismatch_db(5) - mismatch_db(2))
v.check("21-09.12d", mismatch_db(5) - mismatch_db(2) - 0.6)

v.check("21-09.13a", 2 * 1745 - 1950)
v.check("21-09.13b", 2 * 1950 - 1745)
# Two equal tones through y = x + a3 x^3 with a3 = -4/(3 A_iip3^2) (amplitudes in volts on 50 ohm); measure the
# product at 2 f2 - f1 by FFT, using integer bins that keep the same arithmetic pattern.
amp = lambda dbm: math.sqrt(2 * Z0 * 1e-3 * 10 ** (dbm / 10))  # noqa: E731
N = 1 << 14
k1, k2 = 1745, 1950                     # bins standing in for MHz
t = np.arange(N)
x = amp(20) * (np.cos(TWO_PI * k1 * t / N) + np.cos(TWO_PI * k2 * t / N))
a3 = -4 / (3 * amp(65) ** 2)
y = x + a3 * x ** 3
Y = np.fft.rfft(y) / (N / 2)
p_im3 = 10 * lg(abs(Y[2 * k2 - k1]) ** 2 / (2 * Z0) / 1e-3)
v.check("21-09.13c", p_im3)
v.check("21-09.13d", -174 + db10(10e6) + 4)
v.check("21-09.13e", (3 * 20 - (-174 + db10(10e6) + 4 - 6)) / 2)

a25, a26 = 0.67 * 4086.9, 0.61 * 3959.6
v.check("21-09.14a", a25)
v.check("21-09.14b", a26)
v.check("21-09.14c", a26 - a25)
v.check("21-09.14d", (a26 / a25 - 1) * 100)
v.check("21-09.14e", 4086.9 - a25)
v.check("21-09.14f", 3959.6 - a26)
v.check("21-09.14g", ((3959.6 - a26) / (4086.9 - a25) - 1) * 100)
v.check("21-09.14h", 0.005 * 4086.9)
v.check("21-09.14i", 0.005 * 3959.6)

lam_aln = 11000 / (2 * 3.5e9)
lam_line = 299792458 / (4 * 3.5e9 * math.sqrt(6))
v.check("21-09.15a", lam_aln * 1e6)
v.check("21-09.15b", lam_line * 1e3, rtol=2e-3)       # published with c = 3e8
v.check("21-09.15c", lam_line / lam_aln, rtol=2e-3)

# ================================================================ lab
print("Lab")
v.check("Lab 21-09.a", antiresonance(LM, CM, 2e-12) / 1e9)
v.check("Lab 21-09.b", abs(1 / resonator_y(FS, C0, LM, CM, RM)))
lad_wide, _ = build_ladder(FS, 1e-12, 2e-12, RATIO / 2, 2000, 3)
lo2, hi2 = edges(lad_wide, FS, 0.06)
v.check("Lab 21-09.c", (hi2 - lo2) / 1e6)
v.check("Lab 21-09.d", loss(FS, build_ladder(FS, 1e-12, 2e-12, RATIO, 1000, 3)[0]))
v.check("Lab 21-09.e", 1.9e9 * -20e-6 * 115 / 1e6)
for key, temp in (("f", -30), ("g", 25), ("h", 85)):
    v.check(f"Lab 21-09.{key}", loss(2.07e9, LAD, scale=1 + (-20e-6) * (temp - 25)))
v.check("Lab 21-09.i", -db20(abs(series_element_s21(1 / (1j * TWO_PI * 6e9 * COFF)))))
for key, vswr in (("j", 1), ("k", 2), ("l", 4)):
    v.check(f"Lab 21-09.{key}", math.ceil(v_peak(33, vswr) / 2.5))
v.check("Lab 21-09.m", (1 + g1) / (1 - g1))
v.check("Lab 21-09.n", mismatch_db(6) - mismatch_db(1.5))

v.finish()
