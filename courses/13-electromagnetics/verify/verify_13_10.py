#!/usr/bin/env python3
"""Verify every number in chapter 13-10 (waveguides and resonators), its solutions and lab.

Independent routes (not the chapter's closed forms):
- waveguide cutoffs from a finite-difference eigen-solve of the 2D Helmholtz equation with Neumann walls (TE),
  Richardson-extrapolated over two grids;
- conductor attenuation and cavity Q by numerically integrating wall losses, power flow and stored energy from the
  mode fields (not Pozar's closed-form expressions);
- below-cutoff attenuation and group delay from the numerically found cutoff;
- the fibre's LP01 mode both from the Bessel matching condition and from a finite-difference eigen-solve of the
  radial scalar wave equation; the mode field diameter from a numerical Gaussian overlap;
- the cavity's equivalent RLC resonance and Q from its impedance (for the ngspice comparison).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
from scipy.integrate import dblquad, quad
from scipy.optimize import brentq, minimize_scalar
from scipy.special import jv, kv

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "13-10-waveguides-and-resonators.md",
         COURSE / "solutions" / "13-10-solutions.md"]
lab = COURSE / "labs" / "13-10-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("13-10", *files)
mu0 = 1.25663706212e-6
e0 = 8.8541878128e-12
c0 = 1 / math.sqrt(mu0 * e0)
eta0 = math.sqrt(mu0 / e0)
NP_DB = 20 * math.log10(math.e)
SIG = 5.8e7
A, B = 0.02286, 0.01016


# ---------------------------------------------------------------- waveguide eigen-solve
def neumann_1d(n, h):
    main = np.full(n, 2.0)
    main[0] = main[-1] = 1.0  # cell-centred Neumann ends
    return sps.diags([-np.ones(n - 1), main, -np.ones(n - 1)], [-1, 0, 1]) / h**2


def te_cutoffs(a, b, cells_a, nmodes=5):
    """Smallest nonzero kc^2 of -laplacian H = kc^2 H with Neumann walls on an a x b box, cell-centred grid."""
    na = cells_a
    nb = max(2, int(round(cells_a * b / a)))
    ha, hb = a / na, b / nb
    Lx, Ly = neumann_1d(na, ha), neumann_1d(nb, hb)
    L = sps.kronsum(Lx, Ly, format="csc")
    vals = spla.eigsh(L, k=nmodes + 1, sigma=-1.0, which="LM", return_eigenvectors=False)
    return np.sort(vals)[1:]  # drop the constant (kc = 0)


def cutoffs_extrapolated(a, b, n=200, nmodes=4):
    k1 = te_cutoffs(a, b, n, nmodes)
    k2 = te_cutoffs(a, b, 2 * n, nmodes)
    kc2 = (4 * k2 - k1) / 3
    return np.sqrt(kc2) * c0 / (2 * math.pi)


fcs = cutoffs_extrapolated(A, B)
fc10 = fcs[0]


def te10_alpha(f, a=A, b=B, sigma=SIG):
    """Conductor attenuation of TE10 by integrating wall losses and power flow from the fields (H0 = 1)."""
    w = 2 * math.pi * f
    k = w / c0
    kc = 2 * math.pi * fc10 / c0 if a == A else math.pi / a
    beta = math.sqrt(k * k - kc * kc)
    Rs = math.sqrt(math.pi * f * mu0 / sigma)
    Hz = lambda x: math.cos(math.pi * x / a)  # noqa: E731
    Hx = lambda x: beta * a / math.pi * math.sin(math.pi * x / a)  # noqa: E731  (magnitude)
    Ey = lambda x: w * mu0 * a / math.pi * math.sin(math.pi * x / a)  # noqa: E731
    # power: 1/2 Re(Ey Hx*) over the cross-section
    P = 0.5 * quad(lambda x: Ey(x) * Hx(x), 0, a)[0] * b
    # losses per metre: side walls (x = 0, a) see Hz; top and bottom see Hx and Hz
    side = 2 * (0.5 * Rs * Hz(0.0) ** 2 * b)
    topbot = 2 * 0.5 * Rs * quad(lambda x: Hx(x) ** 2 + Hz(x) ** 2, 0, a)[0]
    return (side + topbot) / (2 * P), beta, Rs


# ---------------------------------------------------------------- theory
v.check("T 13-10.a", fc10 / 1e9)
k1g = 2 * math.pi * 1e9 / c0
v.check("T 13-10.b", math.sqrt((math.pi / A) ** 2 - k1g**2) * A * NP_DB)

# ---------------------------------------------------------------- Example 1
v.check("Ex 13-10.1a", fcs[0] / 1e9)
v.check("Ex 13-10.1b", fcs[1] / 1e9)
v.check("Ex 13-10.1c", fcs[2] / 1e9)
v.check("Ex 13-10.1d", fcs[3] / 1e9)

# ---------------------------------------------------------------- Example 2
f2 = 1e10
k2 = 2 * math.pi * f2 / c0
kc = 2 * math.pi * fc10 / c0
beta2 = math.sqrt(k2**2 - kc**2)
v.check("Ex 13-10.2a", beta2)
v.check("Ex 13-10.2b", 2 * math.pi / beta2 * 100)
vp = 2 * math.pi * f2 / beta2
dw = 1e3
vg = (2 * math.pi * dw) / (math.sqrt((2 * math.pi * (f2 + dw) / c0) ** 2 - kc**2)
                           - math.sqrt((2 * math.pi * (f2 - dw) / c0) ** 2 - kc**2)) * 2
v.check("Ex 13-10.2c", vp)
v.check("Ex 13-10.2d", vg)
v.check("Ex 13-10.2e", 2 * math.pi * f2 * mu0 / beta2)  # Z_TE = omega mu / beta

# ---------------------------------------------------------------- Example 3
alpha3, _, Rs3 = te10_alpha(1e10)
v.check("Ex 13-10.3a", Rs3 * 1e3)
v.check("Ex 13-10.3b", alpha3)
v.check("Ex 13-10.3c", alpha3 * NP_DB)

# ---------------------------------------------------------------- Example 4
fc_vent = cutoffs_extrapolated(0.005, 0.005, n=100, nmodes=1)[0]
k4 = 2 * math.pi * 2.4e9 / c0
a4 = math.sqrt((2 * math.pi * fc_vent / c0) ** 2 - k4**2)
v.check("Ex 13-10.4a", a4)
v.check("Ex 13-10.4b", a4 * NP_DB)
v.check("Ex 13-10.4c", a4 * 0.015 * NP_DB)


# ---------------------------------------------------------------- Example 5 (cavity by field integration)
def cavity_te101(a, b, d, sigma=SIG):
    f0 = c0 / 2 * math.sqrt((1 / a) ** 2 + (1 / d) ** 2)
    w = 2 * math.pi * f0
    k = w / c0
    beta = math.pi / d
    Zte = k * eta0 / beta
    Rs = math.sqrt(math.pi * f0 * mu0 / sigma)
    E0 = 1.0
    Ey = lambda x, z: E0 * math.sin(math.pi * x / a) * math.sin(math.pi * z / d)  # noqa: E731
    Hx = lambda x, z: E0 / Zte * math.sin(math.pi * x / a) * math.cos(math.pi * z / d)  # noqa: E731
    Hz = lambda x, z: math.pi * E0 / (k * eta0 * a) * math.cos(math.pi * x / a) * math.sin(math.pi * z / d)  # noqa
    We = e0 / 4 * dblquad(lambda z, x: Ey(x, z) ** 2, 0, a, 0, d)[0] * b
    # wall losses: z = 0, d walls (Hx); x = 0, a walls (Hz); y = 0, b walls (Hx and Hz)
    Pz = 2 * Rs / 2 * quad(lambda x: Hx(x, 0.0) ** 2, 0, a)[0] * b
    Px = 2 * Rs / 2 * quad(lambda z: Hz(0.0, z) ** 2, 0, d)[0] * b
    Py = 2 * Rs / 2 * dblquad(lambda z, x: Hx(x, z) ** 2 + Hz(x, z) ** 2, 0, a, 0, d)[0]
    Q = w * 2 * We / (Pz + Px + Py)
    return f0, Q, Rs


f5, Q5, Rs5 = cavity_te101(A, B, A)
v.check("Ex 13-10.5a", f5 / 1e9)
v.check("Ex 13-10.5b", Rs5 * 1e3)
v.check("Ex 13-10.5c", Q5)
v.check("Ex 13-10.5d", f5 / Q5 / 1e6)


# ---------------------------------------------------------------- Example 6 (fibre)
def lp01(n1, n2, a, lam):
    NA = math.sqrt(n1**2 - n2**2)
    V = 2 * math.pi * a / lam * NA
    g = lambda u: u * jv(1, u) / jv(0, u) - math.sqrt(V * V - u * u) * kv(1, math.sqrt(V * V - u * u)) \
        / kv(0, math.sqrt(V * V - u * u))  # noqa: E731
    u = brentq(g, 1e-6, min(V, 2.4048) - 1e-9, xtol=1e-14)
    return NA, V, u, math.sqrt(V * V - u * u)


def lp01_fd(n1, n2, a, lam, N=3600, R=12.0):  # a falls on a cell boundary (h = a/300)
    """Finite-difference eigen-solve of (1/r)(r E')' + k^2 n(r)^2 E = beta^2 E on 0 < r < R a (E(R a) = 0)."""
    k0 = 2 * math.pi / lam
    h = R * a / N
    r = (np.arange(N) + 0.5) * h
    rp, rm = r + h / 2, r - h / 2
    main = -(rp + rm) / (r * h * h) + (k0 * np.where(r < a, n1, n2)) ** 2
    main[0] = -(rp[0]) / (r[0] * h * h) + (k0 * n1) ** 2  # symmetric condition at r = 0
    off_up = rp[:-1] / (r[:-1] * h * h)
    off_dn = rm[1:] / (r[1:] * h * h)
    M = sps.diags([off_dn, main, off_up], [-1, 0, 1], format="csc")
    val = spla.eigs(M, k=1, sigma=(k0 * n1) ** 2, which="LM", return_eigenvectors=False)[0].real
    return math.sqrt(val) / k0


def mfd_gauss(a, u, w):
    E = lambda r: jv(0, u * r / a) / jv(0, u) if r < a else kv(0, w * r / a) / kv(0, w)  # noqa: E731
    nE = quad(lambda r: E(r) ** 2 * r, 0, a)[0] + quad(lambda r: E(r) ** 2 * r, a, 40 * a, limit=200)[0]

    def neg(w0):
        ov = quad(lambda r: E(r) * math.exp(-r * r / w0**2) * r, 0, a)[0] + \
            quad(lambda r: E(r) * math.exp(-r * r / w0**2) * r, a, 40 * a, limit=200)[0]
        return -ov**2 / (nE * w0**2 / 4)
    return 2 * minimize_scalar(neg, bounds=(0.5 * a, 5 * a), method="bounded", options={"xatol": 1e-13}).x


n1, n2, af = 1.4504, 1.4457, 4.1e-6
NA, V13, u13, w13 = lp01(n1, n2, af, 1.31e-6)
v.check("Ex 13-10.6a", NA)
v.check("Ex 13-10.6b", (n1 - n2) / n1 * 100)
v.check("Ex 13-10.6c", brentq(lambda lam: 2 * math.pi * af / lam * NA - 2.404825557695773, 0.5e-6, 3e-6) * 1e6)
v.check("Ex 13-10.6d", V13)
v.check("Ex 13-10.6e", u13)
b13 = 1 - u13**2 / V13**2
v.check("Ex 13-10.6f", b13)
neff_fd = lp01_fd(n1, n2, af, 1.31e-6)
v.assert_true("FD radial solve agrees with the Bessel condition", abs(neff_fd - math.sqrt(n2**2 + b13 * NA**2)) < 2e-6,
              f"{neff_fd} vs {math.sqrt(n2**2 + b13 * NA**2)}")
v.check("Ex 13-10.6g", neff_fd)
v.check("Ex 13-10.6h", mfd_gauss(af, u13, w13) * 1e6)
v.check("Ex 13-10.6i", 2 * af * (0.65 + 1.619 / V13**1.5 + 2.879 / V13**6) * 1e6)
_, V15, u15, w15 = lp01(n1, n2, af, 1.55e-6)
v.check("Ex 13-10.6j", V15)
v.check("Ex 13-10.6k", mfd_gauss(af, u15, w15) * 1e6)

# ---------------------------------------------------------------- practitioner and simulation
v.check("Prac 13-10.a", 8.20e9 / fcs[0])
v.check("Prac 13-10.b", 12.40e9 / fcs[1])
# equivalent parallel RLC: R = 1 kohm, C = Q/(w0 R), L = 1/(w0^2 C); find the peak and the 3 dB points
Rr = 1000.0
Cr = Q5 / (2 * math.pi * f5 * Rr)
Lr = 1 / ((2 * math.pi * f5) ** 2 * Cr)
Zr = lambda f: 1 / (1 / Rr + 1j * 2 * math.pi * f * Cr + 1 / (1j * 2 * math.pi * f * Lr))  # noqa: E731
fpk = minimize_scalar(lambda f: -abs(Zr(f)), bounds=(0.999 * f5, 1.001 * f5), method="bounded",
                      options={"xatol": 1e-3}).x
lo = brentq(lambda f: abs(Zr(f)) - Rr / math.sqrt(2), 0.99 * f5, fpk)
hi = brentq(lambda f: abs(Zr(f)) - Rr / math.sqrt(2), fpk, 1.01 * f5)
v.check("Sim 13-10.a", fpk / 1e9)
v.check("Sim 13-10.b", fpk / (hi - lo))

# ---------------------------------------------------------------- Problems
v.check("13-10.1a", cutoffs_extrapolated(0.072136, 0.034036, n=200, nmodes=1)[0] / 1e9)
f = 12e9
beta = math.sqrt((2 * math.pi * f / c0) ** 2 - kc**2)
v.check("13-10.2a", 2 * math.pi / beta * 100)
v.check("13-10.2b", 2 * math.pi * f * mu0 / beta)
v.check("13-10.3a", fc10 / math.sqrt(2.25) / 1e9)
for ff, key in ((9e9, "a"), (11e9, "b")):
    dw_ = 1e3
    tau = (math.sqrt((2 * math.pi * (ff + dw_) / c0) ** 2 - kc**2)
           - math.sqrt((2 * math.pi * (ff - dw_) / c0) ** 2 - kc**2)) / (2 * 2 * math.pi * dw_)  # d beta/d omega
    v.check(f"13-10.4{key}", tau * 1e9)
t9 = 1 / (c0 * math.sqrt(1 - (fc10 / 9e9) ** 2))
t11 = 1 / (c0 * math.sqrt(1 - (fc10 / 11e9) ** 2))
v.check("13-10.4c", (t9 - t11) * 1e9)
fc3 = cutoffs_extrapolated(0.003, 0.003, n=100, nmodes=1)[0]
a5 = math.sqrt((2 * math.pi * fc3 / c0) ** 2 - (2 * math.pi * 2.45e9 / c0) ** 2)
v.check("13-10.5a", a5)
v.check("13-10.5b", a5 * 1e-3 * NP_DB)
f6, Q6, Rs6 = cavity_te101(0.05, 0.05, 0.05)
v.check("13-10.6a", f6 / 1e9)
v.check("13-10.7a", Rs6 * 1e3)
v.check("13-10.7b", Q6)
fmin = minimize_scalar(lambda f: te10_alpha(f)[0], bounds=(7e9, 30e9), method="bounded", options={"xatol": 1e3}).x
v.check("13-10.8a", fmin / 1e9)
v.check("13-10.8b", te10_alpha(fmin)[0] * NP_DB)
V9 = 2 * math.pi * 25e-6 / 850e-9 * 0.2
v.check("13-10.9a", V9)
v.check("13-10.9b", V9**2 / 2)
v.check("13-10.10a", brentq(lambda a: 2 * math.pi * a / 1.26e-6 * 0.12 - 2.404825557695773, 1e-7, 1e-5) * 1e6)
Zte10 = 2 * math.pi * 1e10 * mu0 / beta2
P11 = 0.5 * quad(lambda x: (3e6 * math.sin(math.pi * x / A)) ** 2 / Zte10, 0, A)[0] * B
v.check("13-10.11a", P11 / 1e6)
b7 = math.sqrt((2 * math.pi * 7e9 / c0) ** 2 - kc**2)
v.check("13-10.12a", 2 * math.pi * 7e9 * mu0 / b7)
v.check("13-10.13a", f5 / (1 / (1 / Q5 + 1 / Q5)) / 1e6)
E = lambda r: jv(0, u13 * r / af) / jv(0, u13) if r < af else kv(0, w13 * r / af) / kv(0, w13)  # noqa: E731
pc = quad(lambda r: E(r) ** 2 * r, 0, af)[0]
pt = pc + quad(lambda r: E(r) ** 2 * r, af, 50 * af, limit=200)[0]
v.check("13-10.14a", pc / pt * 100)

# ---------------------------------------------------------------- Lab
if lab.exists():
    # group delay difference across the recommended band and the fibre's V at 1260 nm
    t_lo = 1 / (c0 * math.sqrt(1 - (fc10 / 8.2e9) ** 2))
    t_hi = 1 / (c0 * math.sqrt(1 - (fc10 / 12.4e9) ** 2))
    v.check("Lab 13-10.a", (t_lo - t_hi) * 1e9)
    v.check("Lab 13-10.b", 2 * math.pi * af / 1.26e-6 * NA)

sys.exit(v.finish())
