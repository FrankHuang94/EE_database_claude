#!/usr/bin/env python3
"""Verify every number in chapter 09-14 (optoelectronic devices), its solutions and lab.

Independent routes:
- photon energies and cutoffs from CODATA h, c and e;
- absorption thicknesses by root finding on the absorbed fraction;
- shot noise by the formula, cross-checked by a seeded Poisson simulation of photoelectron counts;
- the detection probability from the Poisson survival function;
- the escape cone by integrating the solid angle numerically;
- the laser threshold by root finding on the round-trip gain;
- solar-cell maximum-power points by root finding on dP/dV = 0 (the chapter maximized P directly), with
  series resistance handled by solving the implicit diode equation;
- the SPAD dead-time loss by a seeded event simulation, compared with the non-paralyzable formula.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants as C
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import poisson

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("09-14", COURSE / "chapters" / "09-14-optoelectronic-devices.md",
                        COURSE / "solutions" / "09-14-solutions.md",
                        COURSE / "labs" / "09-14-lab" / "README.md")

Q = C.e
VT = C.k * 300 / C.e
HC = C.h * C.c / C.e * 1e6          # eV um
E_of = lambda lam_um: HC / lam_um
rng = np.random.default_rng(20261119)

# ------------------------------------------------------------------ Example 1
for k_, Eg in (("a", 1.12), ("b", 1.424), ("c", 3.435)):
    v.check(f"Ex 09-14.1{k_}", brentq(lambda lam: E_of(lam) - Eg, 0.1, 10))
v.check("Ex 09-14.1d", E_of(1.55))
v.check("Ex 09-14.1e", E_of(0.94))
v.check("Ex 09-14.1f", E_of(0.45))

# ------------------------------------------------------------------ Example 2
for k_, a in (("a", 1e4), ("b", 1e3)):
    v.check(f"Ex 09-14.2{k_}", brentq(lambda d: 1 - math.exp(-a * d) - 0.95, 0, 1) * 1e4)
resp = lambda eta, lam: eta * Q / (E_of(lam) * Q)        # A/W
v.check("Ex 09-14.2c", resp(0.8, 0.85))
v.check("Ex 09-14.2d", resp(1.0, 1.55))

# ------------------------------------------------------------------ Example 3: shot noise
Iph, Id, B = 1e-9, 10e-12, 1e6
i_n = math.sqrt(2 * Q * (Iph + Id) * B)
v.check("Ex 09-14.3a", i_n)
v.check("Ex 09-14.3b", Iph / i_n)
v.check("Ex 09-14.3c", 20 * math.log10(Iph / i_n))
# simulation: count electrons in windows of T = 1/(2B) (the bandwidth convention), estimate the current noise
T = 1 / (2 * B)
counts = rng.poisson((Iph + Id) / Q * T, 200000)
i_sim = counts.std() * Q / T
v.assert_true("Poisson simulation reproduces sqrt(2qIB) within 1%", abs(i_sim / i_n - 1) < 0.01,
              f"{i_sim:.3e} vs {i_n:.3e}")

# ------------------------------------------------------------------ Example 4: ToF
v.check("Ex 09-14.4a", 2 * 5.0 / C.c * 1e9)
v.check("Ex 09-14.4b", C.c * 100e-12 / 2 * 100)
v.check("Ex 09-14.4c", poisson.sf(0, 0.28 * 2))

# ------------------------------------------------------------------ Example 5: pixel
cg = Q / 1.6e-15
v.check("Ex 09-14.5a", cg * 1e6)
v.check("Ex 09-14.5b", 6000 * cg)
v.check("Ex 09-14.5c", math.sqrt(6000))
v.check("Ex 09-14.5d", 20 * math.log10(math.sqrt(6000)))
v.check("Ex 09-14.5e", 20 * math.log10(6000 / 2))

# ------------------------------------------------------------------ Example 6: LED
n = math.sqrt(10.89)
thc = math.asin(1 / n)
cone = quad(lambda th: math.sin(th), 0, thc)[0] / 2          # fraction of the full sphere (4 pi)
Tn = 1 - ((n - 1) / (n + 1)) ** 2
v.check("Ex 09-14.6a", n)
v.check("Ex 09-14.6b", math.degrees(thc))
v.check("Ex 09-14.6c", cone)
v.check("Ex 09-14.6d", Tn)
v.check("Ex 09-14.6e", cone * Tn)
v.check("Ex 09-14.6f", 0.9 * 0.8 * E_of(0.45) / 3.0)
v.check("Ex 09-14.6g", E_of(0.555) / E_of(0.45))

# ------------------------------------------------------------------ Example 7: laser
R = ((n - 1) / (n + 1)) ** 2
v.check("Ex 09-14.7a", R)
gth = lambda R1, R2, L, ai: brentq(lambda g: R1 * R2 * math.exp(2 * (g - ai) * L) - 1, ai, 1e4)
v.check("Ex 09-14.7b", gth(R, R, 0.03, 10))
v.check("Ex 09-14.7c", gth(R, 0.95, 0.03, 10))


# ------------------------------------------------------------------ Example 8: solar cell
def mpp(jsc, j0=1e-13, rs=0.0):
    """Maximum-power point by root finding on dP/dV = 0, with P = V J(V) and J from the implicit equation."""
    def J(V):
        return brentq(lambda j: jsc - j0 * (math.exp((V + j * rs) / VT) - 1) - j, -1e6, jsc * 1.01, xtol=1e-16)

    voc = brentq(lambda V: J(V), 0.1, 1.0, xtol=1e-14)
    h = 1e-7
    dP = lambda V: ((V + h) * J(V + h) - (V - h) * J(V - h)) / (2 * h)
    vmp = brentq(dP, 0.3 * voc, voc - 1e-6, xtol=1e-12)
    return voc, vmp, J(vmp)


voc, vmp, jmp = mpp(40e-3)
v.check("Ex 09-14.8a", voc)
v.check("Ex 09-14.8b", vmp)
v.check("Ex 09-14.8c", jmp * 1e3)
v.check("Ex 09-14.8d", vmp * jmp * 1e3)
v.check("Ex 09-14.8e", vmp * jmp / (voc * 40e-3))
v.check("Ex 09-14.8f", vmp * jmp / 0.1 * 100)
v.check("Ex 09-14.8g", (voc - vmp) * 1e3)
v.check("T 09-14.a", 683)   # Hu Table 4-3
v.check("T 09-14.b", 0.75)  # Hu Sec. 4.12.4
v.check("T 09-14.c", brentq(lambda x: abs(math.sin(math.pi * x) / (math.pi * x)) - 1 / math.sqrt(2), 0.1, 0.9))
Mm, kk = 10, 0.1
v.check("T 09-14.d", kk * Mm + (1 - kk) * (2 - 1 / Mm))

# practitioner facts (quoted; see R-175)
for k_, val in (("P 09-14.a", 28), ("P 09-14.b", 520), ("P 09-14.c", 20), ("P 09-14.d", 5), ("P 09-14.e", 2029),
                ("P 09-14.f", 28.1), ("P 09-14.g", 35.2), ("P 09-14.h", 26.9), ("P 09-14.i", 23.4),
                ("P 09-14.j", 21.0), ("P 09-14.k", 47.6), ("P 09-14.l", 26.0), ("P 09-14.m", 28.29),
                ("P 09-14.n", 414), ("P 09-14.o", 250), ("P 09-14.p", 185), ("P 09-14.q", 240), ("P 09-14.r", 465),
                ("P 09-14.s", 282), ("P 09-14.t", 23000), ("P 09-14.u", 85),
                ("P 09-14.v", 37), ("P 09-14.w", 940)):
    v.check(k_, val)

# ------------------------------------------------------------------ solutions
v.check("09-14.1a", brentq(lambda lam: E_of(lam) - 0.661, 0.1, 10))
v.check("09-14.1b", resp(0.7, 1.31))
Eph = E_of(1.55) * Q
v.check("09-14.2a", 10e-6 / Eph)
v.check("09-14.2b", 0.8 * Q * 10e-6 / Eph * 1e6)
v.check("09-14.2c", Eph)
v.check("09-14.2d", 0.8 * Q * 10e-6 / Eph / 10e-6)
absf = 1 - math.exp(-1e3 * 10e-4)
v.check("09-14.3a", absf)
v.check("09-14.3b", 0.70 * absf)
v.check("09-14.3c", 0.98 * absf)
A4 = math.pi * (25e-4) ** 2
C4 = 11.7 * C.epsilon_0 / 100 * A4 / 2e-4
v.check("09-14.4a", A4)
v.check("09-14.4b", C4 * 1e12)
v.check("09-14.4c", 1 / (2 * math.pi * 50 * C4) / 1e9)
inz = 1e-12 * math.sqrt(1e9)
v.check("09-14.5a", inz * 1e9)
v.check("09-14.5b", 5e-9 / inz)
v.check("09-14.5c", 20 * 5e-9 / inz)
tau = 10e-9
v.check("09-14.6a", 1 / tau)
v.check("09-14.6b", 5e7 / (1 + 5e7 * tau))
v.check("09-14.6c", 1e6 * 1e-9)
# event simulation of a non-paralyzable detector
arr = np.cumsum(rng.exponential(1 / 5e7, 400000))
rec, last = 0, -1.0
for t in arr:
    if t - last >= tau:
        rec += 1
        last = t
v.assert_true("event simulation matches the non-paralyzable formula within 1%",
              abs(rec / arr[-1] / (5e7 / (1 + 5e7 * tau)) - 1) < 0.01)
v.check("09-14.7a", C.c / (2 * 1e6))
v.check("09-14.7b", C.c / (2 * 1e7))
fw = 6000 * (0.8 / 1.4) ** 2
v.check("09-14.8a", fw)
v.check("09-14.8b", math.sqrt(fw))
v.check("09-14.8c", 20 * math.log10(math.sqrt(fw)))
v.check("09-14.8d", 20 * math.log10(fw / 1.5))
snr9 = 80 / math.sqrt(80 + 2 ** 2)
v.check("09-14.9a", snr9)
v.check("09-14.9b", 20 * math.log10(snr9))
E10 = E_of(0.63)
v.check("09-14.10a", E10)
v.check("09-14.10b", E10 / 2.1)
v.check("09-14.10c", 0.85 * 0.7 * E10 / 2.1)
v.check("09-14.11a", brentq(lambda L: 0.3 * 0.3 * math.exp(2 * (40 - 10) * L) - 1, 1e-4, 1) * 1e4)
v.check("09-14.11b", brentq(lambda p: 2 * 3.2 * p - 850, 1, 1000))
voc_r, vmp_r, jmp_r = mpp(40e-3, rs=1.0)
v.check("09-14.12a", vmp_r)
v.check("09-14.12b", jmp_r * 1e3)
v.check("09-14.12c", vmp_r * jmp_r * 1e3)
v.check("09-14.12d", vmp_r * jmp_r / (voc_r * 40e-3))
v.check("09-14.12e", vmp_r * jmp_r / 0.1 * 100)
voc_c, vmp_c, jmp_c = mpp(4.0)
v.check("09-14.12f", voc_c)
v.check("09-14.12g", voc_c - voc)
v.check("09-14.12h", vmp_c * jmp_c / (voc_c * 4.0))
v.check("09-14.12i", vmp_c * jmp_c / 10 * 100)

# ------------------------------------------------------------------ lab
voc2, vmp2, jmp2 = mpp(80e-3)
v.check("Lab 09-14.a", (voc2 - voc) * 1e3)
v.check("Lab 09-14.b", vmp2 * jmp2 / 0.2 * 100)
v.check("Lab 09-14.c", vmp / jmp)

v.finish()
