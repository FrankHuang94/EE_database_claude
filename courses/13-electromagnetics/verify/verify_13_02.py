#!/usr/bin/env python3
"""Verify every number in chapter 13-02 (electrostatics boundary-value problems), its solutions and lab.

Independent routes (not the chapter's closed forms):
- interface fields by solving the two boundary-condition equations as a linear system;
- one-dimensional potentials by symbolic solution of Laplace's and Poisson's equations (sympy dsolve), with
  charge from Gauss's law at a conductor;
- troughs by a sparse finite-difference solution of Laplace's equation, cross-checked against the series;
- image problems by numerical integration of the surface charge implied by the image field;
- wires over a plane and two-wire lines by a two-dimensional method of moments (charged surface patches);
- the strip-over-ground capacitance by finite differences and the stored energy.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "13-02-electrostatics-boundary-value-problems.md",
         COURSE / "solutions" / "13-02-solutions.md"]
lab = COURSE / "labs" / "13-02-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("13-02", *files)
e0 = 8.8541878128e-12
q = 1.602176634e-19
TP = 2 * math.pi
k = 1 / (4 * math.pi * e0)


# ============================================================ helpers
def interface(E1, er1, er2, rho_s=0.0):
    """Fields below a z = 0 interface from those above: E_t continuous, eps2 E2z = eps1 E1z - rho_s."""
    A = np.array([[1.0, 0.0], [0.0, er2 * e0]])
    b = np.array([E1[0], er1 * e0 * E1[1] - rho_s])
    return np.linalg.solve(A, b)


def laplace_fd(nx, ny, top=1.0, hx=1.0, hy=1.0):
    """Sparse finite-difference Laplace on an (nx x ny) interior grid with the top edge at `top`, others 0."""
    N = nx * ny
    idx = lambda i, j: j * nx + i  # noqa: E731
    rows, cols, vals = [], [], []
    rhs = np.zeros(N)
    cx, cy = 1 / hx ** 2, 1 / hy ** 2
    for j in range(ny):
        for i in range(nx):
            p = idx(i, j)
            rows.append(p); cols.append(p); vals.append(-2 * cx - 2 * cy)
            for di, dj, c in ((1, 0, cx), (-1, 0, cx), (0, 1, cy), (0, -1, cy)):
                ii, jj = i + di, j + dj
                if 0 <= ii < nx and 0 <= jj < ny:
                    rows.append(p); cols.append(idx(ii, jj)); vals.append(c)
                elif jj == ny:                     # top boundary
                    rhs[p] -= c * top
    A = sps.csr_matrix((vals, (rows, cols)), shape=(N, N))
    return spla.spsolve(A, rhs).reshape(ny, nx)


def trough_series(x, y, a, b, V0, nterms):
    s, n, used = 0.0, 1, 0
    while used < nterms:
        ky, kb = n * math.pi * y / a, n * math.pi * b / a     # sinh(ky)/sinh(kb) without overflow
        ratio = math.exp(ky - kb) * (1 - math.exp(-2 * ky)) / (1 - math.exp(-2 * kb))
        s += 4 * V0 / (n * math.pi) * ratio * math.sin(n * math.pi * x / a)
        n += 2
        used += 1
    return s


def mom_wire_over_plane_n(a, h, N, eps=e0):
    """C' of a round wire (radius a, axis at height h) over a grounded plane: uniform-charge surface patches on
    the wire, their images below the plane, potential 1 V matched at patch centres."""
    th = 2 * math.pi * (np.arange(N) + 0.5) / N
    w = 2 * math.pi * a / N
    x, z = a * np.cos(th), h + a * np.sin(th)
    dx = x[:, None] - x[None, :]
    d_real = np.hypot(dx, z[:, None] - z[None, :])
    np.fill_diagonal(d_real, 1.0)
    d_img = np.hypot(dx, z[:, None] + z[None, :])
    G = (-np.log(d_real) + np.log(d_img)) / (2 * math.pi * eps)
    G[np.arange(N), np.arange(N)] = (-(math.log(w / 2) - 1) + np.log(d_img[np.arange(N), np.arange(N)])) / (
        2 * math.pi * eps)
    qs = np.linalg.solve(G, np.ones(N))
    return qs.sum()


def mom_two_wire_n(a, D, N, eps=e0):
    """C' between two parallel round wires (radius a, centre spacing D) at +1/2 and -1/2 V."""
    th = 2 * math.pi * (np.arange(N) + 0.5) / N
    w = 2 * math.pi * a / N
    xs = np.concatenate([a * np.cos(th) - D / 2, a * np.cos(th) + D / 2])
    ys = np.concatenate([a * np.sin(th), a * np.sin(th)])
    d = np.hypot(xs[:, None] - xs[None, :], ys[:, None] - ys[None, :])
    np.fill_diagonal(d, 1.0)
    G = -np.log(d) / (2 * math.pi * eps)
    np.fill_diagonal(G, -(math.log(w / 2) - 1) / (2 * math.pi * eps))
    Vt = np.concatenate([np.full(N, 0.5), np.full(N, -0.5)])
    qs = np.linalg.solve(G, Vt)
    v.assert_true("two-wire MoM: net charge zero", abs(qs.sum()) < 1e-12 * abs(qs[:N].sum()))
    return qs[:N].sum() / 1.0


def mom_wire_over_plane(a, h):
    """Richardson extrapolation of the patch solution (its error falls as 1/N)."""
    return 2 * mom_wire_over_plane_n(a, h, 1600) - mom_wire_over_plane_n(a, h, 800)


def mom_two_wire(a, D):
    return 2 * mom_two_wire_n(a, D, 1200) - mom_two_wire_n(a, D, 600)


# ============================================================ theory
v.check("T 13-02.a", e0 * 3e6 * 1e6)

# ============================================================ Example 1: dielectric interface
E1 = np.array([3e3, 4e3])
E2 = interface(E1, 1.0, 4.0)
v.check("Ex 13-02.1a", np.hypot(*E2) / 1e3)
v.check("Ex 13-02.1b", math.degrees(math.atan2(E1[0], E1[1])))
v.check("Ex 13-02.1c", math.degrees(math.atan2(E2[0], E2[1])))
v.check("Ex 13-02.1d", e0 * E1[1] * 1e9)
v.check("Ex 13-02.1e", 4 * e0 * np.hypot(*E2) * 1e9)
v.assert_true("refraction law tan1/tan2 = eps1/eps2", abs((E1[0] / E1[1]) / (E2[0] / E2[1]) - 1 / 4) < 1e-12)

# ============================================================ Example 2: coaxial capacitor from Laplace's equation
rho, V0s, A_, B_ = sp.symbols("rho V0 A B", positive=True)
Vf = sp.Function("V")
sol = sp.dsolve(sp.Eq(sp.diff(rho * sp.diff(Vf(rho), rho), rho) / rho, 0), Vf(rho)).rhs
a2, b2, er2 = sp.Rational(5, 10000), sp.Rational(175, 100000), sp.Rational(225, 100)
consts = sp.solve([sol.subs(rho, a2) - 100, sol.subs(rho, b2)], sp.symbols("C1 C2"))
Vcoax = sol.subs(consts)
Er = -sp.diff(Vcoax, rho)
Qp = float(2 * sp.pi * a2 * er2 * e0 * Er.subs(rho, a2))        # Gauss at the inner conductor, per metre
v.check("Ex 13-02.2a", Qp / 100 * 1e12)
v.check("Ex 13-02.2b", Qp * 1e9)
v.check("Ex 13-02.2c", float(Er.subs(rho, a2)) / 1e3)
v.check("Ex 13-02.2d", float(Er.subs(rho, b2)) / 1e3)

# ============================================================ Example 3: Poisson in a slab
x = sp.symbols("x", real=True)
rv, d3 = sp.Rational(1, 1000), sp.Rational(1, 1000)
eps_s = sp.symbols("epsilon", positive=True)
gen = sp.dsolve(sp.Eq(sp.diff(Vf(x), x, 2), -rv / eps_s), Vf(x)).rhs
c3 = sp.solve([gen.subs(x, 0), gen.subs(x, d3)], sp.symbols("C1 C2"))
V3 = gen.subs(c3).subs(eps_s, sp.Float(e0, 30))
xm = sp.solve(sp.diff(V3, x), x)[0]
v.check("Ex 13-02.3a", float(V3.subs(x, xm)))
E3 = -sp.diff(V3, x)
v.check("Ex 13-02.3b", abs(float(E3.subs(x, 0))) / 1e3)
rs0 = e0 * float(E3.subs(x, 0))          # plate at x = 0: rho_s = D_n with n pointing into the gap (+x)
v.check("Ex 13-02.3c", rs0 * 1e6)
v.assert_true("plates carry minus the slab charge", abs(2 * rs0 + float(rv * d3)) < 1e-15)

# ============================================================ Example 4: square trough
n_fd = 199                                       # interior nodes per side, h = a/200
Vg = laplace_fd(n_fd, n_fd)
hc = 1 / (n_fd + 1)
xs = (np.arange(n_fd) + 1) * hc


def fd_at(Vgrid, xq, yq, h=hc):
    i, j = int(round(xq / h)) - 1, int(round(yq / h)) - 1
    return Vgrid[j, i]


for key, nt in (("4a", 1), ("4b", 2), ("4c", 3)):
    v.check(f"Ex 13-02.{key}", trough_series(0.5, 0.5, 1, 1, 1, nt))
v.check("Ex 13-02.4d", trough_series(0.5, 0.75, 1, 1, 1, 200))
v.check("Ex 13-02.4e", trough_series(0.5, 0.25, 1, 1, 1, 200))
v.check("Ex 13-02.4f", fd_at(Vg, 0.5, 0.5))
v.assert_true("FD centre exactly 0.25 (rotational symmetry of the discrete problem)", abs(fd_at(Vg, 0.5, 0.5) - 0.25) < 1e-10)
v.assert_true("FD agrees with the series at (a/2, 3a/4) and (a/2, a/4) within 1e-4",
              abs(fd_at(Vg, 0.5, 0.75) - trough_series(0.5, 0.75, 1, 1, 1, 200)) < 1e-4
              and abs(fd_at(Vg, 0.5, 0.25) - trough_series(0.5, 0.25, 1, 1, 1, 200)) < 1e-4)

# ============================================================ Example 5: point charge above a plane
Q, h = 1e-9, 1e-2
Fz = k * Q * (-Q) / (2 * h) ** 2
v.check("Ex 13-02.5a", abs(Fz) * 1e6)


def rho_s_point(r):
    """Surface charge from the normal field of Q at +h and -Q at -h, evaluated on the plane."""
    Ez = 0.0
    for qq, zz in ((Q, h), (-Q, -h)):
        dist = math.hypot(r, zz)
        Ez += k * qq * (0 - zz) / dist ** 3
    return e0 * Ez


v.check("Ex 13-02.5b", rho_s_point(0.0) * 1e6)
inner = quad(lambda r: rho_s_point(r) * 2 * math.pi * r, 0, h)[0]
# whole plane: substitute r = h tan(phi) so the slowly decaying tail maps onto a finite interval
total = quad(lambda ph: rho_s_point(h * math.tan(ph)) * 2 * math.pi * h * math.tan(ph) * h / math.cos(ph) ** 2,
             0, math.pi / 2)[0]
v.check("Ex 13-02.5c", 100 * inner / total)
v.assert_true("total induced charge is -Q", abs(total / -Q - 1) < 1e-6)

# ============================================================ Example 6 and Problem 14: wire over a plane
C6 = mom_wire_over_plane(0.5e-3, 5e-3)
v.check("Ex 13-02.6a", C6 * 1e12)
v.assert_true("MoM agrees with 2 pi eps / acosh(h/a) to 1e-5", abs(C6 / (2 * math.pi * e0 / math.acosh(10)) - 1) < 1e-5)
thin = lambda r: 2 * math.pi * e0 / math.log(2 * r)  # noqa: E731
v.check("Ex 13-02.6b", thin(10) * 1e12)
v.check("Ex 13-02.6c", 100 * (1 - thin(10) / C6))
C6b = mom_wire_over_plane(0.5e-3, 1e-3)
v.check("Ex 13-02.6d", C6b * 1e12)
v.check("Ex 13-02.6e", thin(2) * 1e12)
v.check("Ex 13-02.6f", 100 * (1 - thin(2) / C6b))
exact_ratio = lambda r: 1 - math.acosh(r) / math.log(2 * r)  # noqa: E731
for r_, key in ((2, "14a"), (5, "14b"), (10, "14c"), (20, "14d")):
    v.check(f"13-02.{key}", 100 * exact_ratio(r_))
v.check("13-02.14e", brentq(lambda r: exact_ratio(r) - 0.01, 1.2, 50, xtol=1e-12))
v.assert_true("MoM error at h/a = 2 matches the exact-formula error",
              abs(100 * (1 - thin(2) / C6b) - 100 * exact_ratio(2)) < 0.05)

# ============================================================ practitioner and simulation
v.check("Prac 13-02.a", 1 / 0.66 ** 2)
v.check("Prac 13-02.b", 100 * (3.66 / 3.48 - 1))
v.check("Prac 13-02.c", 100 * (1 - 3.48 / 3.66))


def grid(n=5, top=1.0):
    """The resistor-grid analogue: n x n interior nodes, each the average of its neighbours (equal resistors)."""
    return laplace_fd(n, n, top)


G5 = grid()
v.check("Sim 13-02.a", G5[2, 2])

# ============================================================ solutions
v.check("13-02.1a", e0 * 2e6 * 1e6)
v.check("13-02.1b", e0 * 3e6 * 1e6)
E2b = interface(np.array([2e3, 6e3]), 1.0, 6.0)
v.check("13-02.2a", np.hypot(*E2b) / 1e3)
v.check("13-02.2b", math.degrees(math.atan2(2e3, 6e3)))
v.check("13-02.2c", math.degrees(math.atan2(E2b[0], E2b[1])))
# 3: series layers from D continuity: V = D (d1/eps1 + d2/eps2), C/A = D/V
D3 = 1.0
Vtot = D3 * (1e-9 / (3.9 * e0) + 3e-9 / (20 * e0))
CA = D3 / Vtot
v.check("13-02.3a", 3.9 * e0 / CA * 1e9)
v.check("13-02.3b", CA * 1e15 / 1e12)
# 4: spherical Laplace symbolically
r = sp.symbols("r", positive=True)
gs = sp.dsolve(sp.Eq(sp.diff(r ** 2 * sp.diff(Vf(r), r), r) / r ** 2, 0), Vf(r)).rhs
c4 = sp.solve([gs.subs(r, sp.Rational(1, 100)) - 1, gs.subs(r, sp.Rational(2, 100))], sp.symbols("C1 C2"))
Vs4 = gs.subs(c4)
Q4 = 4 * math.pi * 0.01 ** 2 * e0 * float(-sp.diff(Vs4, r).subs(r, sp.Rational(1, 100)))
v.check("13-02.4a", Q4 * 1e12)
bb = sp.symbols("b", positive=True)
c4b = sp.solve([gs.subs(r, sp.Rational(1, 100)) - 1, gs.subs(r, bb)], sp.symbols("C1 C2"))
Q4b = sp.limit(4 * sp.pi * sp.Rational(1, 100) ** 2 * (-sp.diff(gs.subs(c4b), r).subs(r, sp.Rational(1, 100))),
               bb, sp.oo)
v.check("13-02.4b", float(Q4b) * e0 * 1e12)                 # the b -> infinity limit of the same solution
# 5: maximize E_bd a ln(b/a)
o5 = minimize_scalar(lambda a: -3e6 * a * math.log(5e-3 / a), bounds=(1e-5, 4.99e-3), method="bounded",
                     options={"xatol": 1e-12})
v.check("13-02.5a", o5.x * 1e3)
v.check("13-02.5b", -o5.fun / 1e3)
# 6: Poisson in the depletion region, integrated numerically
eps_si, NA, W = 11.7 * e0, 1e22, 0.3e-6
# integrate Poisson's equation from the field-free edge x = W back to the junction: state (V, E),
# dV/dx = -E, dE/dx = rho/eps = -qN/eps, with V(W) = E(W) = 0
pois = solve_ivp(lambda xx, st: [-st[1], -q * NA / eps_si], (W, 0.0), [0.0, 0.0], rtol=1e-12, atol=1e-18)
E0_6, V0_6 = pois.y[1, -1], pois.y[0, -1]
v.assert_true("13-02.6 field at the junction is positive (n to p)", E0_6 > 0)
v.check("13-02.6a", E0_6 / 1e6)
v.check("13-02.6b", V0_6)
# 7: 2:1 trough (a = 2, b = 1), FD with a grid of spacing 1/200
V7 = 10 * laplace_fd(399, 199)
v.check("13-02.7a", trough_series(1, 0.5, 2, 1, 10, 1))
v.check("13-02.7b", trough_series(1, 0.5, 2, 1, 10, 3))
v.check("13-02.7c", V7[99, 199])
v.assert_true("2:1 trough FD centre matches the converged series", abs(V7[99, 199] - trough_series(1, 0.5, 2, 1, 10, 400)) < 1e-3)
# 8: line charge above a plane
lam, h8 = 1e-9, 1e-2
rs8 = lambda xx: e0 * (-lam * h8 / (math.pi * e0 * (xx ** 2 + h8 ** 2)))  # noqa: E731  normal field of line + image
v.assert_true("problem 8 surface charge from the image pair's field",
              abs(rs8(0.003) - e0 * sum(lam / (2 * math.pi * e0) * (0 - zz) / (0.003 ** 2 + zz ** 2) * s
                                        for zz, s in ((h8, 1), (-h8, -1)))) < 1e-18)
v.check("13-02.8a", rs8(0.0) * 1e9)
v.check("13-02.8b", quad(rs8, -np.inf, np.inf)[0] * 1e9)
v.check("13-02.8c", lam ** 2 / (2 * math.pi * e0 * 2 * h8) * 1e6)
# 9: two-wire line by method of moments
C9 = mom_two_wire(0.5e-3, 6e-3)
v.check("13-02.9a", C9 * 1e12)
v.check("13-02.9b", math.pi * e0 / math.log(6e-3 / 0.5e-3) * 1e12)
v.check("13-02.9c", 100 * (1 - math.pi * e0 / math.log(6e-3 / 0.5e-3) / C9))
# 10: corner images; check the planes are equipotentials, then sum the forces
d10, Q10 = 1e-2, 1e-9
charges = [(-Q10, np.array([-d10, d10])), (-Q10, np.array([d10, -d10])), (Q10, np.array([-d10, -d10]))]
allq = charges + [(Q10, np.array([d10, d10]))]
pot = lambda P: sum(k * qq / np.linalg.norm(P - pos) for qq, pos in allq)  # noqa: E731
v.assert_true("both half-planes are at zero potential",
              max(abs(pot(np.array([0.0, t]))) + abs(pot(np.array([t, 0.0]))) for t in (0.003, 0.02, 0.1)) < 1e-6)
F10 = sum(k * Q10 * qq * (np.array([d10, d10]) - pos) / np.linalg.norm(np.array([d10, d10]) - pos) ** 3
          for qq, pos in charges)
v.check("13-02.10a", F10[0] * 1e6)
v.check("13-02.10b", np.linalg.norm(F10) * 1e6)
# 12: 2 x 2 interior nodes, solved generally
G12 = laplace_fd(2, 2)
v.check("13-02.12a", G12[1, 0])
v.check("13-02.12b", G12[0, 0])
v.check("13-02.12c", trough_series(1 / 3, 2 / 3, 1, 1, 1, 400))
v.check("13-02.12d", trough_series(1 / 3, 1 / 3, 1, 1, 1, 400))
# 13: energy integral
eps13 = 2.25 * e0
W13 = quad(lambda rr: 0.5 * eps13 * (100 / (rr * math.log(3.5))) ** 2 * 2 * math.pi * rr, 0.5e-3, 1.75e-3)[0]
v.check("13-02.13a", W13 * 1e6)
v.check("13-02.13b", 2 * W13 / 100 ** 2 * 1e12)

# ============================================================ lab README
if lab.exists():
    v.check("Lab 13-02.a", G5[3, 2])                               # node (3, 4) counted from the bottom-left
    v.check("Lab 13-02.b", trough_series(0.5, 4 / 6, 1, 1, 1, 400))

    def strip_cap(w_over_h, cells_per_h=30, box_w=20, box_h=10):
        """C' (F/m) of a zero-thickness strip of width w at height h over ground, inside a grounded box,
        by finite differences and the stored energy."""
        n = cells_per_h
        nx, ny = box_w * n - 1, box_h * n - 1
        N = nx * ny
        idx = lambda i, j: j * nx + i  # noqa: E731
        js = n - 1                                   # strip row (height h)
        half = int(round(w_over_h * n / 2))
        ic = nx // 2
        strip = set(range(ic - half, ic + half + 1))
        rows, cols, vals = [], [], []
        rhs = np.zeros(N)
        for j in range(ny):
            for i in range(nx):
                p = idx(i, j)
                if j == js and i in strip:
                    rows.append(p); cols.append(p); vals.append(1.0); rhs[p] = 1.0
                    continue
                rows.append(p); cols.append(p); vals.append(-4.0)
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ii, jj = i + di, j + dj
                    if 0 <= ii < nx and 0 <= jj < ny:
                        rows.append(p); cols.append(idx(ii, jj)); vals.append(1.0)
        Vs = spla.spsolve(sps.csr_matrix((vals, (rows, cols)), shape=(N, N)), rhs).reshape(ny, nx)
        Vfull = np.zeros((ny + 2, nx + 2))
        Vfull[1:-1, 1:-1] = Vs
        gx = np.diff(Vfull, axis=1)
        gy = np.diff(Vfull, axis=0)
        W_ = 0.5 * e0 * (np.sum(gx ** 2) + np.sum(gy ** 2))   # (h * dV/h)^2 summed over cell edges, per metre
        return 2 * W_ / 1.0

    c1 = strip_cap(1.0)
    v.check("Lab 13-02.c", c1 / (e0 * 1.0))
    v.assert_true("strip capacitance changes under 1% when the grid is refined to h/40",
                  abs(strip_cap(1.0, cells_per_h=40) / c1 - 1) < 0.01)
    v.assert_true("fringing factor falls toward 1 as the strip widens",
                  strip_cap(0.5) / (e0 * 0.5) > c1 / e0 > strip_cap(5.0) / (e0 * 5.0) > 1)

# 15: sphere in a uniform field. Check Laplace's equation and the boundary conditions symbolically (uniqueness
# then makes it the answer), and get the charge and dipole moment by numerical surface integrals.
rs_, ts_ = sp.symbols("r_s t_s", positive=True)
E15, a15 = sp.Integer(10**6), sp.Rational(1, 1000)
V15 = -E15 * sp.cos(ts_) * (rs_ - a15**3 / rs_**2)
lap15 = sp.diff(rs_**2 * sp.diff(V15, rs_), rs_) / rs_**2 + sp.diff(sp.sin(ts_) * sp.diff(V15, ts_), ts_) / (rs_**2 * sp.sin(ts_))
v.assert_true("13-02.15 potential satisfies Laplace", sp.simplify(lap15) == 0)
v.assert_true("13-02.15 sphere is at zero volts", sp.simplify(V15.subs(rs_, a15)) == 0)
v.assert_true("13-02.15 uniform field far away",
              abs(float((V15 / (-E15 * rs_ * sp.cos(ts_))).subs({rs_: 1e3, ts_: 0.3})) - 1) < 1e-12)
sig15 = sp.lambdify(ts_, -e0 * sp.diff(V15, rs_).subs(rs_, a15), "numpy")   # rho_s = eps0 E_r = -eps0 dV/dr
th_grid = np.linspace(0, math.pi, 20001)
v.check("13-02.15a", float(np.max(sig15(th_grid))) * 1e6)
v.check("13-02.15b", float(np.max(sig15(th_grid))) / e0 / 1e6)
a15f = float(a15)
Qtot = quad(lambda t: sig15(t) * TP * a15f**2 * math.sin(t), 0, math.pi)[0]
v.assert_true("13-02.15 net induced charge is zero", abs(Qtot) < 1e-25)
v.check("13-02.15c", quad(lambda t: sig15(t) * a15f * math.cos(t) * TP * a15f**2 * math.sin(t), 0, math.pi)[0])
# 16: graded coax by a finite-volume solve of d/drho(eps rho dV/drho) = 0 with the interface on a node
a16, c16, b16 = 0.5e-3, 1e-3, 2e-3
M16 = 30000
rg = np.linspace(a16, b16, M16 + 1)
hg = rg[1] - rg[0]
rmid = 0.5 * (rg[:-1] + rg[1:])
epm = np.where(rmid < c16, 4.0, 2.0) * e0
gcond = epm * rmid / hg                                   # "conductance" of each radial cell, per radian
Ms16 = sps.diags([np.r_[1.0, -(gcond[:-1] + gcond[1:]), 1.0], np.r_[gcond[:-1], 0.0], np.r_[0.0, gcond[1:]]],
                 [0, -1, 1], format="csc")
rhs16 = np.zeros(M16 + 1)
rhs16[0] = 1000.0
V16 = spla.spsolve(Ms16, rhs16)
Ecell = -np.diff(V16) / hg
Qp16 = TP * epm[0] * rmid[0] * Ecell[0]                 # flux of D per metre through the first cell face
v.check("13-02.16a", Qp16 / 1000.0 * 1e12)
Efield = lambda rr, er_: Qp16 / (TP * er_ * e0 * rr) / 1e6  # noqa: E731  Gauss's law with the solved charge
v.check("13-02.16b", Efield(a16, 4.0))
v.check("13-02.16c", Efield(c16, 4.0))
v.check("13-02.16d", Efield(c16, 2.0))
v.check("13-02.16e", Efield(b16, 2.0))
v.assert_true("13-02.16 solved cell fields match Gauss at the interface",
              abs(Ecell[M16 // 3 - 1] / 1e6 / Efield(rmid[M16 // 3 - 1], 4.0) - 1) < 1e-6)
v.check("13-02.16f", 1000.0 / (a16 * math.log(b16 / a16)) / 1e6)

sys.exit(v.finish())
