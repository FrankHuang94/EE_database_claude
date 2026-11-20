#!/usr/bin/env python3
"""Verify every number in the Course 13 final-exam solutions.

Independent routes (not the hand formulas of the solutions):
- vector calculus by sympy differentiation and numerical surface, volume and line integrals;
- electrostatics by finite-difference Laplace solutions (layered plates, radial coax with energy
  integration) and by integrating the induced surface-charge pressure on the grounded plane;
- the gapped core by root finding on Ampere's law and integrating field energy; the loop by
  summing Biot-Savart segments;
- Maxwell's equations by sympy: H from Faraday's law, permittivity from Ampere's law, power by
  time-averaging E x H; relaxation by integrating the continuity equation;
- lossy media from the exact complex propagation constant and intrinsic impedance, with a
  Bessel-function check on the round wire;
- optics by Snell/Fresnel with complex cosines, a thin-film characteristic matrix, and root
  finding for the Brewster and critical angles;
- the line transient by a discrete-time forward/backward-wave simulation, and the capacitive load
  by integrating its differential equation;
- line sections by cascading 2000-section LC ladders and exact ABCD matrices, matching networks by
  solving for components, standing waves by sampling |V(z)|;
- the waveguide by finite-difference eigenvalues and a numerical derivative of the dispersion;
- the link by Friis in linear units and power density; the dipole by integrating its far-field
  Poynting flux; the array by summing element phasors.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import dblquad, quad, solve_ivp
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq, fsolve, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("13-exam", HERE.parent / "exam" / "solutions.md")
c = 2.998e8
e0 = 8.854e-12
mu0 = 4e-7 * math.pi
eta0 = 376.7
TP = 2 * math.pi
DB = 20 * math.log10(math.e)

# ---------------------------------------------------------------- Q1 vector calculus
x, y, z = sp.symbols("x y z", real=True)
A = sp.Matrix([x * y, y * z, z * x])
pt = {x: 1, y: 2, z: 3}
div = sum(sp.diff(A[i], s) for i, s in enumerate((x, y, z)))
curl = sp.Matrix([sp.diff(A[2], y) - sp.diff(A[1], z), sp.diff(A[0], z) - sp.diff(A[2], x),
                  sp.diff(A[1], x) - sp.diff(A[0], y)]).subs(pt)
v.check("X13.1a", float(div.subs(pt)))
v.check("X13.1b", float(curl[0]))
v.check("X13.1c", float(curl[1]))
v.check("X13.1d", float(curl[2]))
V = x**2 * y * z
grad = [float(sp.diff(V, s).subs(pt)) for s in (x, y, z)]
v.check("X13.1e", grad[0])
v.check("X13.1f", grad[1])
v.check("X13.1g", grad[2])
v.check("X13.1h", float(np.linalg.norm(grad)))
r = sp.symbols("r", positive=True)
rho_v = sp.diff(r**2 * 2 * r**2, r) / r**2           # spherical divergence of D_r = 2 r^2
v.check("X13.1i", float(rho_v.subs(r, 1)))
q_vol = quad(lambda rr: float(rho_v.subs(r, rr)) * 4 * math.pi * rr**2, 0, 2)[0]
q_flux = dblquad(lambda th, ph: 2 * 2.0**2 * 2.0**2 * math.sin(th), 0, TP, 0, math.pi)[0]
v.assert_true("X13.1 volume and flux agree", abs(q_vol - q_flux) < 1e-9 * q_flux)
v.check("X13.1j", q_flux)
circ = quad(lambda ph: (-2 * math.sin(ph)) * (-2 * math.sin(ph)) + (2 * math.cos(ph)) * (2 * math.cos(ph)),
            0, TP)[0]
v.check("X13.1k", circ)

# ---------------------------------------------------------------- Q2 electrostatics
# (a) layered plates: finite-difference d/dx(eps dV/dx) = 0 on 2000 cells
N = 2000
dx = 2e-3 / N
eps = np.where(np.arange(N) < N // 2, 2.0, 6.0) * e0     # cell permittivities
G = eps / dx                                              # "conductance" per area of each cell
n = N + 1
Mat = np.zeros((n, n))
b = np.zeros(n)
for i in range(N):
    Mat[i, i] += G[i]
    Mat[i + 1, i + 1] += G[i]
    Mat[i, i + 1] -= G[i]
    Mat[i + 1, i] -= G[i]
for node, val in ((0, 100.0), (n - 1, 0.0)):
    Mat[node, :] = 0
    Mat[node, node] = 1
    b[node] = val
Vx = np.linalg.solve(Mat, b)
E_cells = -np.diff(Vx) / dx
Dfield = eps[0] * E_cells[0]
v.check("X13.2b", Dfield * 1e6)
v.check("X13.2a", Dfield * 1e-3 / 100 * 1e12)
v.check("X13.2c", E_cells[10] / 1e3)
v.check("X13.2d", E_cells[-10] / 1e3)
# (b) coax: FD of d/drho(rho dV/drho) = 0, then C' = 2W'/V^2 and E(a) from Gauss on the solved charge
a_in, b_out, er = 0.45e-3, 1.5e-3, 2.25
M = 20000
rho = np.linspace(a_in, b_out, M + 1)
h = rho[1] - rho[0]
rm = 0.5 * (rho[:-1] + rho[1:])                          # midpoints carry rho in the flux
main = np.zeros(M + 1)
off = rm / h**2
main[1:-1] = -(off[:-1] + off[1:])
from scipy.sparse import diags  # noqa: E402
from scipy.sparse.linalg import spsolve  # noqa: E402
lower = off.copy()
upper = off.copy()
lower[-1] = 0.0
upper[0] = 0.0
Ms = diags([np.r_[1.0, main[1:-1], 1.0], lower, upper], [0, -1, 1], format="csc")
rhs = np.zeros(M + 1)
rhs[0] = 1000.0
Vr = spsolve(Ms, rhs)
Er = -np.diff(Vr) / h
W = 0.5 * er * e0 * np.sum(Er**2 * TP * rm * h)
Cp = 2 * W / 1000.0**2
v.check("X13.2e", Cp * 1e12)
v.check("X13.2f", Cp * 1000.0 / (TP * er * e0 * a_in) / 1e6)
# (c) image problem: force = integral of sigma^2/(2 eps0) over the plane
q, d = 1e-9, 0.01
sig = lambda s: -q * d / (TP * (s**2 + d**2) ** 1.5)
F = quad(lambda s: sig(s) ** 2 / (2 * e0) * TP * s, 0, np.inf)[0]
v.check("X13.2g", F * 1e6)

# ---------------------------------------------------------------- Q3 gapped core
Ncoil, Ac, lc, mur, gap, I = 250, 1e-5, 0.1, 1200, 1e-3, 2.0
Bsol = brentq(lambda B: B / (mur * mu0) * lc + B / mu0 * gap - Ncoil * I, 1e-6, 5.0, xtol=1e-14)
Wc = Bsol**2 / (2 * mur * mu0) * Ac * lc
Wg = Bsol**2 / (2 * mu0) * Ac * gap
v.check("X13.3a", 100 * (Bsol / mu0 * gap) / (Ncoil * I))
v.check("X13.3b", 2 * (Wc + Wg) / I**2 * 1e6)
v.check("X13.3c", Bsol)
v.check("X13.3d", (Wc + Wg) * 1e3)
v.check("X13.3e", 100 * Wg / (Wc + Wg))
K = 20000
ph = np.linspace(0, TP, K, endpoint=False) + math.pi / K
dl = np.stack([-np.sin(ph), np.cos(ph), 0 * ph], 1) * 0.01 * TP / K
Rv = -np.stack([0.01 * np.cos(ph), 0.01 * np.sin(ph), 0 * ph], 1)   # from segment to centre
Bz = mu0 * 1.0 / (4 * math.pi) * np.sum(np.cross(dl, Rv)[:, 2] / 0.01**3)
v.check("X13.3f", Bz * 1e6)

# ---------------------------------------------------------------- Q4 Maxwell's equations
t, epsr = sp.symbols("t epsr", positive=True)
w = TP * 1e9
Ex = 100 * sp.cos(w * t - 30 * z)
Hy = sp.integrate(-sp.diff(Ex, z) / mu0, t)              # Faraday: dHy/dt = -(1/mu) dEx/dz
amp_res = sp.simplify(-sp.diff(Hy, z) - epsr * e0 * sp.diff(Ex, t))   # Ampere x-component
er_sol = float(sp.solve(sp.expand_trig(amp_res).subs({t: 0.1e-9, z: 0.0}), epsr)[0])
v.check("X13.4a", er_sol)
fHt = sp.lambdify(t, Hy.subs(z, 0), "numpy")
Hamp = minimize_scalar(lambda tt: -abs(fHt(tt)), bounds=(0.2e-9, 0.8e-9), method="bounded",
                       options={"xatol": 1e-20}).fun * -1
v.check("X13.4c", Hamp)
v.check("X13.4b", 100 / Hamp)
ts = np.linspace(0, 1e-9, 4001)[:-1]
fE = sp.lambdify(t, Ex.subs(z, 0), "numpy")
fH = sp.lambdify(t, Hy.subs(z, 0), "numpy")
v.check("X13.4d", float(np.mean(fE(ts) * fH(ts))))
v.check("X13.4e", 100 * minimize_scalar(lambda zz: -math.cos(30 * zz), bounds=(0.1, 0.3), method="bounded",
                                       options={"xatol": 1e-12}).x)   # spatial period of E at t = 0
sig_s, er_s = 2e-3, 4.0
for key, f in (("X13.4f", 1e6), ("X13.4g", 1e9)):
    Ephasor = 1.0
    Jc = sig_s * Ephasor
    Jd = 1j * TP * f * er_s * e0 * Ephasor
    v.check(key, abs(Jc) / abs(Jd))
sol = solve_ivp(lambda tt, rr: -sig_s / (er_s * e0) * rr, (0, 1e-7), [1.0], dense_output=True,
                rtol=1e-12, atol=1e-15)
v.check("X13.4h", brentq(lambda tt: sol.sol(tt)[0] - math.exp(-1), 1e-9, 1e-7, xtol=1e-16) * 1e9)


# ---------------------------------------------------------------- Q5 lossy media
def gamma_eta(f, sigma, er_):
    jw = 1j * TP * f
    return np.sqrt(jw * mu0 * (sigma + jw * er_ * e0)), np.sqrt(jw * mu0 / (sigma + jw * er_ * e0))


g, etac = gamma_eta(3e8, 3.5e7, 1.0)
delta = 1 / g.real
Rs = etac.real
v.check("X13.5a", delta * 1e6)
v.check("X13.5b", Rs * 1e3)
Rac = Rs / (math.pi * 1e-3)
Rdc = 1 / (3.5e7 * math.pi * 0.5e-3**2)
v.check("X13.5c", Rac)
v.check("X13.5d", Rdc * 1e3)
v.check("X13.5e", Rac / Rdc)
# exact round-wire internal impedance (Bessel functions of complex argument)
from scipy.special import jv  # noqa: E402
kw = (1 - 1j) / delta
Zw = kw * jv(0, kw * 0.5e-3) / (TP * 0.5e-3 * 3.5e7 * jv(1, kw * 0.5e-3))
v.check("X13.5k", 100 * (Zw.real / Rac - 1))
gs, _ = gamma_eta(4e4, 4.0, 81.0)
v.check("X13.5f", 4.0 / (TP * 4e4 * 81 * e0))
v.check("X13.5g", 1 / gs.real)
v.check("X13.5h", DB * gs.real)
v.check("X13.5i", TP / gs.imag)
v.check("X13.5j", 80 / (DB * gs.real))


# ---------------------------------------------------------------- Q6 optics
def fresnel(n1, n2, th):
    kx = n1 * np.sin(th)
    c1 = np.sqrt(n1**2 - kx**2 + 0j) / n1
    c2 = np.sqrt(n2**2 - kx**2 + 0j) / n2
    te = (n1 * c1 - n2 * c2) / (n1 * c1 + n2 * c2)
    tm = (n1 * c2 - n2 * c1) / (n1 * c2 + n2 * c1)   # Ulaby's Gamma_par = (eta2 cos t - eta1 cos i)/(...)
    return te, tm


te0, _ = fresnel(1.0, 3.0, 0.0)
v.check("X13.6a", te0.real)
tau = 1 + te0.real
v.check("X13.6b", tau)
v.check("X13.6c", 100 * abs(te0) ** 2)
v.check("X13.6d", 100 * tau**2 * 3.0)                  # |tau|^2 eta1/eta2 with eta1/eta2 = n2/n1


def coat_R(n1, t_nm, lam_nm=550.0, ns=1.8):
    dlt = TP * n1 * t_nm / lam_nm
    Mx = np.array([[np.cos(dlt), 1j * np.sin(dlt) / n1], [1j * n1 * np.sin(dlt), np.cos(dlt)]])
    B, C = Mx @ np.array([1.0, ns])
    rr = (B - C) / (B + C)
    return abs(rr) ** 2


best = minimize_scalar(lambda n1: coat_R(n1, 550 / (4 * n1)), bounds=(1.1, 1.6), method="bounded",
                       options={"xatol": 1e-10})
v.check("X13.6e", best.x)
tbest = minimize_scalar(lambda tt: coat_R(best.x, tt), bounds=(80, 140), method="bounded",
                        options={"xatol": 1e-9}).x
v.check("X13.6f", tbest)
v.check("X13.6g", 100 * coat_R(1.38, 550 / (4 * 1.38)))
v.check("X13.6h", 100 * coat_R(1.8, 0.0))
v.check("X13.6i", math.degrees(brentq(lambda th: fresnel(1.0, 1.45, th)[1].real, 0.5, 1.2, xtol=1e-14)))
v.check("X13.6j", math.degrees(brentq(lambda th: 1.0 - (1.45 * math.sin(th)) ** 2, 0.3, 1.2, xtol=1e-14)))
v.assert_true("X13.6 total reflection beyond critical",
              abs(abs(fresnel(1.45, 1.0, math.radians(50))[0]) - 1) < 1e-12)
v.assert_true("X13.6 Ulaby sign: Gamma_par = Gamma_perp at normal incidence",
              abs(fresnel(1.0, 1.45, 0.0)[0] - fresnel(1.0, 1.45, 0.0)[1]) < 1e-15)

# ---------------------------------------------------------------- Q7 line transient
Z0, Rsrc, RL, Vs = 50.0, 25.0, 200.0, 2.0
steps = 20                                       # samples per one-way delay
fwd = np.zeros(steps)                            # forward wave, index 0 at the source
bwd = np.zeros(steps)                            # backward wave, index 0 at the load
vload = []
launched = None
for k in range(40 * steps):
    # source end: V = Vs - Rsrc*I with V = a + bsrc, I = (a - bsrc)/Z0, bsrc arriving
    bsrc = bwd[-1]
    a = (Vs * Z0 + bsrc * (Rsrc - Z0)) / (Rsrc + Z0)
    launched = a if launched is None else launched
    # load end: incident a_L = fwd[-1]; reflected r with (a_L + r) = RL (a_L - r)/Z0
    aL = fwd[-1]
    rL = aL * (RL - Z0) / (RL + Z0)
    vload.append(aL + rL)
    fwd = np.r_[a, fwd[:-1]]
    bwd = np.r_[rL, bwd[:-1]]
vload = np.array(vload)
v.check("X13.7a", launched)
v.check("X13.7b", (Rsrc - Z0) / (Rsrc + Z0))
v.check("X13.7c", (RL - Z0) / (RL + Z0))
v.check("X13.7d", vload[steps + 1])
v.check("X13.7e", vload[3 * steps + 1])
v.check("X13.7f", vload[5 * steps + 1])
v.check("X13.7g", vload[-1])
Cl, vp = 2e-12, 1.0
cap = solve_ivp(lambda tt, vv: (2 * vp - vv) / (Z0 * Cl), (0, 2e-9), [0.0], dense_output=True,
                rtol=1e-12, atol=1e-15)
t63 = brentq(lambda tt: cap.sol(tt)[0] - 2 * vp * (1 - math.exp(-1)), 1e-13, 1e-9, xtol=1e-18)
t10 = brentq(lambda tt: cap.sol(tt)[0] - 0.2 * vp, 1e-14, 1e-9, xtol=1e-18)
t90 = brentq(lambda tt: cap.sol(tt)[0] - 1.8 * vp, 1e-14, 2e-9, xtol=1e-18)
v.check("X13.7h", t63 * 1e12)
v.check("X13.7i", (t90 - t10) * 1e12)


# ---------------------------------------------------------------- Q8 line parameters
def ladder_abcd(Lp, Cp_, length, f, nsec=2000):
    w_ = TP * f
    hh = length / nsec
    Zs = 1j * w_ * Lp * hh / 2
    Yp = 1j * w_ * Cp_ * hh
    sec = np.array([[1, Zs], [0, 1]]) @ np.array([[1, 0], [Yp, 1]]) @ np.array([[1, Zs], [0, 1]])
    return np.linalg.matrix_power(sec, nsec)


Lp, Cpp = 300e-9, 120e-12
T = ladder_abcd(Lp, Cpp, 0.01, 1e9)
Zoc = T[0, 0] / T[1, 0]
Zsc = T[0, 1] / T[1, 1]
Z0n = np.sqrt(Zoc * Zsc).real
v.check("X13.8a", Z0n)
betal = math.acos(T[0, 0].real)
vph = TP * 1e9 * 0.01 / betal
v.check("X13.8b", vph)
v.check("X13.8c", (c / vph) ** 2)
v.check("X13.8d", Zoc.imag)
Ceq = -1 / (TP * 1e9 * Zoc.imag)
v.check("X13.8e", Ceq * 1e12)
v.check("X13.8f", Cpp * 0.01 * 1e12)
v.check("X13.8g", 100 * (Ceq / (Cpp * 0.01) - 1))


def line_zin(ZL, Z0_, beta, ell):
    M_ = np.array([[np.cos(beta * ell), 1j * Z0_ * np.sin(beta * ell)],
                   [1j * np.sin(beta * ell) / Z0_, np.cos(beta * ell)]])
    return (M_[0, 0] * ZL + M_[0, 1]) / (M_[1, 0] * ZL + M_[1, 1])


bq = TP * 2.5e9 / vph
sol8 = fsolve(lambda p: [line_zin(100.0, p[0], bq, p[1] / 100).real - 50,
                         line_zin(100.0, p[0], bq, p[1] / 100).imag], [60.0, 1.5], xtol=1e-13)
v.check("X13.8h", sol8[0])
v.check("X13.8i", sol8[1])

# ---------------------------------------------------------------- Q9 standing waves
ZL9 = 20 - 10j
zq = line_zin(ZL9, 50.0, TP, 0.25)                 # beta = 2 pi per wavelength, ell = lambda/4
v.check("X13.9a", zq.real)
v.check("X13.9b", zq.imag)
GL = (ZL9 - 50) / (ZL9 + 50)
dd = np.linspace(0, 0.5, 200001)
Vmag = np.abs(np.exp(1j * TP * dd) + GL * np.exp(-1j * TP * dd))   # |V| at distance d from load
vswr = Vmag.max() / Vmag.min()
gmag = (vswr - 1) / (vswr + 1)
v.check("X13.9c", gmag)
v.check("X13.9d", vswr)
v.check("X13.9e", -20 * math.log10(gmag))
Zin9 = line_zin(ZL9, 50.0, TP, 0.137)              # any length: lossless line
Pdel = abs(2.0 / (50 + Zin9)) ** 2 * Zin9.real / 2
Pav = 2.0**2 / (8 * 50)
v.check("X13.9f", -10 * math.log10(Pdel / Pav))
vabs = lambda dl_: abs(np.exp(1j * TP * dl_) + GL * np.exp(-1j * TP * dl_))
dmin = minimize_scalar(vabs, bounds=(0.0, 0.2), method="bounded", options={"xatol": 1e-12}).x
dmax = minimize_scalar(lambda q_: -vabs(q_), bounds=(0.15, 0.4), method="bounded",
                       options={"xatol": 1e-12}).x
v.check("X13.9g", dmin)
v.check("X13.9h", dmax)
# (d) single-stub match: find where the line admittance has conductance 1/Z0, then the shorted-stub length
Yd = lambda d_: 1 / line_zin(ZL9, 50.0, TP, d_)  # noqa: E731
roots = [brentq(lambda d_: Yd(d_).real - 1 / 50, lo_, hi_, xtol=1e-14) for lo_, hi_ in ((0.05, 0.2), (0.35, 0.49))]
for (kd, kl), d_ in zip((("X13.9i", "X13.9j"), ("X13.9k", "X13.9l")), roots):
    b_need = -Yd(d_).imag * 50                        # normalized susceptance the stub must add
    l_ = brentq(lambda l: (1 / line_zin(1e-12, 50.0, TP, l)).imag * 50 - b_need, 0.01, 0.49, xtol=1e-14)
    v.check(kd, d_)
    v.check(kl, l_)


# ---------------------------------------------------------------- Q10 L-network
def lnet_z(Lh, Cf, f):
    w_ = TP * f
    return 1 / (1j * w_ * Cf + 1 / (12.5 + 1j * w_ * Lh))


s10 = fsolve(lambda p: [lnet_z(p[0] * 1e-9, p[1] * 1e-12, 9e8).real - 50,
                        lnet_z(p[0] * 1e-9, p[1] * 1e-12, 9e8).imag], [4.0, 6.0], xtol=1e-14)
Lh, Cf = s10[0] * 1e-9, s10[1] * 1e-12
v.check("X13.10a", TP * 9e8 * Lh / 12.5)
v.check("X13.10b", Lh * 1e9)
v.check("X13.10c", Cf * 1e12)
z8 = lnet_z(Lh, Cf, 8e8)
Y8s = 1 / (12.5 + 1j * TP * 8e8 * Lh)
v.check("X13.10i", Y8s.real * 1e3)
v.check("X13.10j", Y8s.imag * 1e3)
v.check("X13.10k", TP * 8e8 * Cf * 1e3)
v.check("X13.10l", (1 / z8).imag * 1e3)
g8 = abs((z8 - 50) / (z8 + 50))
v.check("X13.10d", z8.real)
v.check("X13.10e", z8.imag)
v.check("X13.10f", g8)
v.check("X13.10g", -10 * math.log10(1 - g8**2))


# ---------------------------------------------------------------- Q11 waveguide
def fd_k(length, mode, npts):
    hh = length / (npts + 1)
    ev = eigh_tridiagonal(np.full(npts, 2 / hh**2), np.full(npts - 1, -1 / hh**2),
                          select="i", select_range=(mode - 1, mode - 1))[0][0]
    return math.sqrt(ev)


def k_extrap(length, mode):
    k1, k2 = fd_k(length, mode, 4000), fd_k(length, mode, 8000)
    return math.sqrt((4 * k2**2 - k1**2) / 3)        # Richardson on the O(h^2) eigenvalue error


aw, bw = 19.05e-3, 9.525e-3
kc10 = k_extrap(aw, 1)
kc20 = k_extrap(aw, 2)
kc01 = k_extrap(bw, 1)
for key, kc in (("X13.11a", kc10), ("X13.11b", kc20), ("X13.11c", kc01)):
    v.check(key, kc * c / TP / 1e9)
beta_of = lambda f: math.sqrt((TP * f / c) ** 2 - kc10**2)
b13 = beta_of(13e9)
v.check("X13.11d", b13)
v.check("X13.11e", TP / b13 * 100)
v.check("X13.11f", TP * 13e9 * mu0 / b13)
df = 1e3
vg = TP * 2 * df / (beta_of(13e9 + df) - beta_of(13e9 - df))
v.check("X13.11g", vg / c)
v.check("X13.11h", 1 / vg * 1e9)
v.check("X13.11i", math.hypot(kc10, k_extrap(0.02, 1)) * c / TP / 1e9)

# ---------------------------------------------------------------- Q12 link
lam = c / 5.8e9
Pt = 10 ** (20 / 10) * 1e-3
Gt = Gr = 10 ** (9 / 10)
Pr_lin = lambda R: Pt * Gt * Gr * (lam / (4 * math.pi * R)) ** 2
v.check("X13.12a", 10 * math.log10(Pt * Gt / 1e-3))
v.check("X13.12b", 10 * math.log10(Pt * Gt * Gr / Pr_lin(2000.0)))
Prd = 10 * math.log10(Pr_lin(2000.0) / 1e-3)
v.check("X13.12c", Prd)
Sden = Pt * Gt / (4 * math.pi * 2000.0**2)
v.check("X13.12d", Pr_lin(2000.0) / Sden * 1e4)
v.check("X13.12e", Prd + 90)
v.check("X13.12f", brentq(lambda R: 10 * math.log10(Pr_lin(R) / 1e-3) + 90, 1e3, 1e5, xtol=1e-9) / 1e3)

# ---------------------------------------------------------------- Q13 short dipole
kk, Ip, ell, rr0 = TP, 1.0, 1 / 25, 100.0          # lambda = 1 m
Sfar = lambda th: (eta0 * kk * Ip * ell * math.sin(th) / (4 * math.pi * rr0)) ** 2 / (2 * eta0)
Prad = dblquad(lambda th, ph_: Sfar(th) * rr0**2 * math.sin(th), 0, TP, 0, math.pi)[0]
Rrad = 2 * Prad / Ip**2
v.check("X13.13a", Rrad)
v.check("X13.13b", 100 * Rrad / (Rrad + 1.0))

# ---------------------------------------------------------------- Q14 array diligence
Nel = 16
Pel = 1e-2
Gel = 10 ** 0.5


def eirp_dbm(theta, f=28e9, dsp=5e-3, R=1e3):
    """EIRP toward theta: sum each element's field at a distant point using exact path lengths (not the
    plane-wave phase), with steering phases for theta and a cos(theta) power pattern per element."""
    k_ = TP * f / c
    xn = (np.arange(Nel) - (Nel - 1) / 2) * dsp
    obs = np.array([R * math.sin(theta), R * math.cos(theta)])
    dist = np.hypot(obs[0] - xn, obs[1])
    steer = np.exp(-1j * k_ * xn * math.sin(theta))       # phase that makes the paths add in phase at theta
    amp = np.sqrt(Pel * Gel * math.cos(theta) * eta0 / (2 * math.pi)) / dist   # |E| of one element, peak
    field = np.sum(amp * steer * np.exp(-1j * k_ * dist))
    S = abs(field) ** 2 / (2 * eta0)
    return 10 * math.log10(S * 4 * math.pi * R**2 / 1e-3)


v.check("X13.14a", eirp_dbm(0.0))
v.check("X13.14b", eirp_dbm(math.radians(60)))
v.check("X13.14c", Nel * Pel / 0.15)


def edge_level(f, dsp):
    """|AF|/N at the edge of visible space (u = -1) for a beam steered to +60 degrees."""
    k_ = TP * f / c
    nn = np.arange(Nel)
    u0 = math.sin(math.radians(60))
    return abs(np.sum(np.exp(1j * k_ * dsp * nn * (-1 - u0)))) / Nel


fmax = minimize_scalar(lambda f: -edge_level(f * 1e9, 5e-3), bounds=(30, 34), method="bounded",
                       options={"xatol": 1e-9}).x
v.assert_true("X13.14 grating lobe reaches full height at the edge", abs(edge_level(fmax * 1e9, 5e-3) - 1) < 1e-9)
v.check("X13.14d", fmax)
dlim = minimize_scalar(lambda dd_: -edge_level(40e9, dd_ * 1e-3), bounds=(3.5, 4.5), method="bounded",
                       options={"xatol": 1e-10}).x
v.check("X13.14e", dlim * 1e-3 / (c / 40e9))
v.check("X13.14f", dlim)
v.check("X13.14g", 100 * (40 - 24) / ((40 + 24) / 2))
def edge_level_scan(theta_max, f=40e9, dsp=5e-3):
    k_ = TP * f / c
    nn = np.arange(Nel)
    return abs(np.sum(np.exp(1j * k_ * dsp * nn * (-1 - math.sin(theta_max))))) / Nel
v.check("X13.14h", math.degrees(minimize_scalar(lambda t: -edge_level_scan(t), bounds=(0.3, 0.7), method="bounded",
                                                options={"xatol": 1e-12}).x))
for key, f in (("X13.14i", 24e9), ("X13.14j", 28e9)):
    v.check(key, 10 * math.log10(4 * math.pi * 25e-6 / (c / f) ** 2))

sys.exit(v.finish())
