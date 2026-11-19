#!/usr/bin/env python3
"""Verify every number in chapter 09-12 (advanced transistors), its solutions and lab.

Independent routes:
- scale lengths re-derived symbolically (SymPy) from the parabolic potential, the oxide boundary condition and
  Laplace's equation, for the double-gate and the single-gate (insulating back) bodies;
- threshold shifts and DIBL by solving u'' = u / lambda^2 along the channel by finite differences (sparse
  solve) and locating the barrier minimum numerically, not from the 2 sqrt(PQ) formula;
- body thicknesses and minimum lengths by root finding on that finite-difference DIBL;
- IR drops by solving a resistor ladder with distributed load currents;
- confinement energies by a finite-difference Schrodinger eigenvalue problem in a box.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy import constants as C
from scipy.linalg import eigh_tridiagonal, solve_banded
from scipy.optimize import brentq
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("09-12", COURSE / "chapters" / "09-12-finfet-gaa-cfet-backside-power.md",
                        COURSE / "solutions" / "09-12-solutions.md",
                        COURSE / "labs" / "09-12-lab" / "README.md")

# ------------------------------------------------------------------ scale lengths derived symbolically
t, tox, es, eox, c0, c2, c1, V = sp.symbols("t t_ox e_s e_ox c0 c2 c1 V", positive=True)
Cox = eox / tox
# double gate: phi = c0 + c2 y^2 on [-t/2, t/2]; e_s dphi/dy (t/2) = Cox (V - phi_s); Laplace at y = 0
c2_dg = sp.solve(sp.Eq(es * 2 * c2 * t / 2, Cox * (V - (c0 + c2 * t ** 2 / 4))), c2)[0]
lam2_dg = sp.simplify((c0 - V) / (-2 * c2_dg))        # c0'' = -2 c2 = (c0 - V)/lambda^2
# single gate: phi = c0 + c1 y + c2 y^2 on [0, t]; e_s c1 = Cox (c0 - V); c1 + 2 c2 t = 0; Laplace at y = t
c1_sg = Cox * (c0 - V) / es
c2_sg = -c1_sg / (2 * t)
phib = c0 + c1_sg * t + c2_sg * t ** 2
lam2_sg = sp.simplify((phib - V) / (-2 * c2_sg))
lam_dg = sp.lambdify((t, tox), sp.sqrt(lam2_dg.subs({es: 3, eox: 1})))
lam_sg = sp.lambdify((t, tox), sp.sqrt(lam2_sg.subs({es: 3, eox: 1})))
v.assert_true("symbolic DG scale length equals (e_s/2e_ox) t t_ox + t^2/8",
              sp.simplify(lam2_dg - (es / (2 * eox) * t * tox + t ** 2 / 8)) == 0)
v.assert_true("symbolic SG scale length equals (e_s/e_ox) t t_ox + t^2/2",
              sp.simplify(lam2_sg - (es / eox * t * tox + t ** 2 / 2)) == 0)

v.check("Ex 09-12.1a", lam_dg(7, 1))
v.check("Ex 09-12.1b", lam_dg(5, 1))
v.check("Ex 09-12.1c", lam_sg(7, 1))


# ------------------------------------------------------------------ barrier by finite differences
def barrier(L, lam, vds, a=0.2, n=4001):
    """Solve u'' = u/lam^2 on [0, L] with u(0) = a, u(L) = a + vds; return the interior minimum of u
    (refined by a parabola through the three lowest grid points)."""
    x = np.linspace(0, L, n)
    h = x[1] - x[0]
    m = n - 2
    main = np.full(m, -2.0 / h ** 2 - 1.0 / lam ** 2)
    off = np.full(m - 1, 1.0 / h ** 2)
    A = diags([off, main, off], [-1, 0, 1], format="csc")
    rhs = np.zeros(m)
    rhs[0] -= a / h ** 2
    rhs[-1] -= (a + vds) / h ** 2
    u = np.concatenate(([a], spsolve(A, rhs), [a + vds]))
    i = int(np.argmin(u))
    if i == 0:
        return a
    y0, y1, y2 = u[i - 1], u[i], u[i + 1]
    return y1 - (y2 - y0) ** 2 / (8 * (y2 - 2 * y1 + y0))


def dibl(L, lam, vdd=0.7):
    return (barrier(L, lam, vdd) - barrier(L, lam, 0.05)) / (vdd - 0.05)


rows = (("Ex 09-12.2", "abcd", lam_dg(7, 1)), ("Ex 09-12.2", "efgh", lam_dg(5, 1)), ("Ex 09-12.2", "ijkl", lam_sg(7, 1)))
for pre, ids, lam in rows:
    v.check(f"{pre}{ids[0]}", 20 / lam)
    v.check(f"{pre}{ids[1]}", barrier(20, lam, 0.05) * 1e3)
    v.check(f"{pre}{ids[2]}", barrier(20, lam, 0.7) * 1e3)
    v.check(f"{pre}{ids[3]}", dibl(20, lam) * 1e3)
v.check("Ex 09-12.2m", 2 * math.sqrt(0.2 * 0.25) * math.exp(-20 / (2 * lam_dg(7, 1))) * 1e3)

# ------------------------------------------------------------------ widths
fin = lambda h, w: 2 * h + w
sheets = lambda n, w, th: n * 2 * (w + th)
v.check("Ex 09-12.3a", fin(50, 6))
v.check("Ex 09-12.3b", (1000 / 30) * fin(50, 6) / 1000)
v.check("Ex 09-12.3c", sheets(3, 30, 6))
v.check("Ex 09-12.3d", sheets(3, 30, 6) / fin(50, 6))

# ------------------------------------------------------------------ swing
VT = C.k * 300 / C.e
S1 = brentq(lambda s: 10 ** (s / VT / math.log(10) / 1.0) - 10, 0.01, 0.2)   # gate swing for x10 at m = 1
S13 = 1.3 * S1
v.check("Ex 09-12.4a", S1 * 1e3)
v.check("Ex 09-12.4b", S13 * 1e3)
v.check("Ex 09-12.4c", 10 ** (-0.25 / S13) / 10 ** (-0.25 / S1))
vt_eq = brentq(lambda x: 10 ** (-x / S1) - 10 ** (-0.25 / S13), 0, 1)
v.check("Ex 09-12.4d", vt_eq)
v.check("Ex 09-12.4e", (0.25 - vt_eq) * 1e3)
v.check("Ex 09-12.4f", 0.7 - vt_eq)
v.check("Ex 09-12.4g", 100 * ((0.7 - vt_eq) / 0.45 - 1))

# ------------------------------------------------------------------ body thickness
t12 = brentq(lambda x: lam_dg(x, 0.9) - 12 / 6, 0.1, 20)
t16 = brentq(lambda x: lam_dg(x, 0.9) - 16 / 6, 0.1, 20)
v.check("Ex 09-12.5a", t12)
v.check("Ex 09-12.5b", t16)
v.check("Ex 09-12.5c", dibl(6.0, 1.0) * 1e3)
v.check("Ex 09-12.5d", lam_dg(6, 0.9))
v.check("Ex 09-12.5e", lam_dg(8, 0.9))
v.check("Ex 09-12.5f", 12 / lam_dg(6, 0.9))
v.check("Ex 09-12.5g", 16 / lam_dg(8, 0.9))
v.check("Ex 09-12.5h", dibl(12, lam_dg(6, 0.9)) * 1e3)
v.check("Ex 09-12.5i", dibl(16, lam_dg(8, 0.9)) * 1e3)
v.check("Ex 09-12.5j", t12 / 0.543)


# ------------------------------------------------------------------ IR drop by a resistor ladder
def ladder_drop(R, I, n=20000, both=True):
    """Rail split into n equal segments with I/(n-1) drawn at each internal node; supply at node 0 (and at
    node n when fed from both ends). Solve the tridiagonal nodal equations for the drop below the supply."""
    g = n / R
    m = n - 1 if both else n                    # unknown nodes: 1..n-1 (both ends) or 1..n (one end)
    main = np.full(m, 2 * g)
    if not both:
        main[-1] = g                            # the far end has only one segment
    ab = np.zeros((3, m))
    ab[0, 1:] = -g
    ab[1] = main
    ab[2, :-1] = -g
    load = np.full(m, I / (n - 1))
    if not both:
        load[-1] = 0.0                          # keep the same n-1 loaded nodes
    return solve_banded((1, 1), ab, load).max()


rho_f, rho_b = 5e-6, 3e-6
Rf = rho_f * 10e-4 / (20e-7 * 40e-7)
Rb = rho_b * 10e-4 / (200e-7 * 200e-7)
v.check("Ex 09-12.6a", Rf)
v.check("Ex 09-12.6b", ladder_drop(Rf, 0.2e-3) * 1e3)
v.check("Ex 09-12.6c", ladder_drop(Rf, 0.2e-3, both=False) * 1e3)
v.check("Ex 09-12.6d", Rb)
v.check("Ex 09-12.6e", ladder_drop(Rb, 0.2e-3) * 1e3)
dv6 = ladder_drop(Rf, 0.2e-3)
delay = lambda vdd: vdd / (vdd - 0.3)
v.check("Ex 09-12.6f", delay(0.7 - dv6) / delay(0.7))

# practitioner facts (quoted; see R-173)
for k_, val in (("P 09-12.a", 1999), ("P 09-12.b", 1996), ("P 09-12.c", 2011), ("P 09-12.d", 2022), ("P 09-12.e", 45),
                ("P 09-12.f", 23), ("P 09-12.g", 16), ("P 09-12.h", 9), ("P 09-12.i", 18), ("P 09-12.j", 45),
                ("P 09-12.k", 2031), ("P 09-12.l", 25), ("P 09-12.m", 25), ("P 09-12.n", 11),
                ("P 09-12.o", 10), ("P 09-12.p", 6), ("P 09-12.q", 15)):
    v.check(k_, val)

# ------------------------------------------------------------------ solutions
v.check("09-12.1a", fin(45, 7))
nf = next(k for k in range(1, 20) if k * fin(45, 7) >= 400)
v.check("09-12.1b", nf)
v.check("09-12.1c", nf * fin(45, 7))
v.check("09-12.1d", 100 * (nf * fin(45, 7) / 400 - 1))
v.check("09-12.2a", lam_dg(6, 0.8))
v.check("09-12.3a", lam_sg(7, 1))
v.check("09-12.3b", lam_sg(4, 1))
v.check("09-12.3c", lam_dg(4, 1))
v.check("09-12.3d", lam_sg(4, 1) / lam_dg(4, 1))
L4 = brentq(lambda L: dibl(L, lam_dg(6, 0.8)) - 0.030, 12, 60, xtol=1e-6)
v.check("09-12.4a", L4)
v.check("09-12.4b", L4 / lam_dg(6, 0.8))
v.check("09-12.5a", lam_dg(10, 1.0))
v.check("09-12.5b", 20 / lam_dg(10, 1.0))
v.check("09-12.5c", dibl(20, lam_dg(10, 1.0)) * 1e3)
t5 = brentq(lambda x: dibl(20, lam_dg(x, 1.0)) - 0.050, 2, 10, xtol=1e-6)
v.check("09-12.5d", t5)
v.check("09-12.5e", lam_dg(t5, 1.0))
v.check("09-12.6a", sheets(4, 25, 5))
v.check("09-12.6b", sheets(3, 35, 5))
v.check("09-12.6c", 240 / fin(50, 6))
v.check("09-12.6d", 2 * fin(50, 6))
v.check("09-12.6e", 3 * fin(50, 6))
v.check("09-12.6f", 100 * (1 - 2 * fin(50, 6) / 240))
v.check("09-12.6g", 100 * (3 * fin(50, 6) / 240 - 1))
S7 = 1.05 * S1
S7h = S7 * 358.15 / 300
v.check("09-12.7a", S7 * 1e3)
v.check("09-12.7b", S7h * 1e3)
v.check("09-12.7c", 10 ** (-0.25 / S7h) / 10 ** (-0.25 / S7))
v.check("09-12.8a", ladder_drop(400, 0.3e-3, both=False) * 1e3)
v.check("09-12.8b", ladder_drop(400, 0.3e-3) * 1e3)
v.check("09-12.9a", 6 * 24)
v.check("09-12.9b", 5 * 24)
v.check("09-12.9c", (6 * 24) / (5 * 24))
for g, ids in ((0.20, "ab"), (0.25, "cd")):
    area = (1 - g) ** 6
    v.check(f"09-12.10{ids[0]}", area)
    v.check(f"09-12.10{ids[1]}", 1 / area)
v.check("09-12.10e", 0.5 ** 6)
v.check("09-12.10f", 2 ** 6)


def box_E1(t_nm, m_rel, n=3000):
    """Lowest level of a particle in an infinite well by finite differences (eV)."""
    L = t_nm * 1e-9
    h = L / (n + 1)
    k = C.hbar ** 2 / (2 * m_rel * C.m_e * h ** 2)
    w = eigh_tridiagonal(np.full(n, 2 * k), np.full(n - 1, -k), select="i", select_range=(0, 0))[0]
    return w[0] / C.e


E5, E4, E3 = box_E1(5, 0.98), box_E1(4, 0.98), box_E1(3, 0.98)
v.check("09-12.11a", E5 * 1e3)
v.check("09-12.11b", E4 * 1e3)
v.check("09-12.11c", E3 * 1e3)
v.check("09-12.11d", (E4 - E5) * 1e3)
dEdt = lambda tn: (box_E1(tn - 0.01, 0.98) - box_E1(tn + 0.01, 0.98)) / 0.02
v.check("09-12.11e", dEdt(5) * 1e3)
v.check("09-12.11f", dEdt(3) * 1e3)
v.check("09-12.11g", dEdt(3) * 0.3 * 1e3)
v.check("09-12.12a", 18 + 30 + 40 + 30 + 18)
v.check("09-12.12b", 18 + 30 + 18)
v.check("09-12.12c", 4 * 18)
v.check("09-12.12d", 136 / max(66, 72))
v.check("09-12.12e", 136 / 66)

# ------------------------------------------------------------------ lab
LAB_L = brentq(lambda L: dibl(L, lam_dg(7, 1)) - 0.050, 12, 60, xtol=1e-6)
v.check("Lab 09-12.a", LAB_L)
v.check("Lab 09-12.b", dibl(20, lam_dg(7, 1)) / dibl(20, lam_dg(5, 1)))
v.check("Lab 09-12.c", math.exp(20 / (2 * lam_dg(5, 1)) - 20 / (2 * lam_dg(7, 1))))

v.finish()
