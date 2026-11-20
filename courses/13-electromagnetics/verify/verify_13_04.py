#!/usr/bin/env python3
"""Verify every number in chapter 13-04 (Maxwell's equations and time-varying fields), its solutions and lab.

Independent routes (not the chapter's closed forms):
- Faraday EMFs by integrating an explicit induced E field around the loop (its curl checked against -dB/dt);
- displacement currents as numerical time derivatives of the Gauss's-law flux of D;
- phasor and time-domain field relations by symbolic curls and divergences in sympy, with the Ampere-Maxwell
  residual simplified to zero;
- Poynting fluxes and averages by numerical surface integration and numerical time averaging;
- crossover frequencies and cutoffs by root finding;
- the lab's FDTD phase velocity by running a 1D Yee grid and fitting the phase of the steady-state wave.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "13-04-maxwells-equations.md",
         COURSE / "solutions" / "13-04-solutions.md"]
lab = COURSE / "labs" / "13-04-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("13-04", *files)
mu0 = 1.25663706212e-6
e0 = 8.8541878128e-12
c0 = 1 / math.sqrt(mu0 * e0)
eta0 = math.sqrt(mu0 / e0)
sig_cu = 5.8e7

# ---------------------------------------------------------------- helpers
t, x, y, z, w, b = sp.symbols("t x y z omega beta", real=True)


def curl(F):
    Fx, Fy, Fz = F
    return (sp.diff(Fz, y) - sp.diff(Fy, z), sp.diff(Fx, z) - sp.diff(Fz, x), sp.diff(Fy, x) - sp.diff(Fx, y))


def emf_uniform_B(B_peak, omega, A_w, A_h):
    """Peak EMF around a w x h rectangle in a uniform B_z = B cos(wt): integrate the induced field
    E = -(1/2) dB/dt (-y, x, 0) (whose curl is -dB/dt z) around the loop at the instant of peak dB/dt."""
    Bz = B_peak * sp.cos(w * t)
    E = (-sp.Rational(1, 2) * sp.diff(Bz, t) * (-y), -sp.Rational(1, 2) * sp.diff(Bz, t) * x, 0)
    assert sp.simplify(curl(E)[2] + sp.diff(Bz, t)) == 0
    tt = math.pi / (2 * omega)  # sin(wt) = 1
    Ex = sp.lambdify((x, y), E[0].subs({w: omega, t: tt}))
    Ey = sp.lambdify((x, y), E[1].subs({w: omega, t: tt}))
    hw, hh = A_w / 2, A_h / 2
    emf = (quad(lambda s: Ex(s, -hh), -hw, hw)[0] + quad(lambda s: Ey(hw, s), -hh, hh)[0]
           - quad(lambda s: Ex(s, hh), -hw, hw)[0] - quad(lambda s: Ey(-hw, s), -hh, hh)[0])
    return abs(emf)


def displacement_current(eps, area, gap, V, omega):
    """Peak of d/dt of the D-flux through the gap, by central differences over one period."""
    tt = np.linspace(0, 2 * math.pi / omega, 4001)
    psi = eps * V * np.cos(omega * tt) / gap * area
    return np.max(np.abs(np.gradient(psi, tt)))


def time_avg(f, omega, n=20000):
    tt = np.linspace(0, 2 * math.pi / omega, n, endpoint=False)
    return np.mean(f(tt))


# ---------------------------------------------------------------- theory
v.check("T 13-04.a", e0 / sig_cu)
lam_1g = c0 / (2 * 1e9)
v.check("T 13-04.b", lam_1g * 100)
v.check("T 13-04.c", lam_1g / 10 * 100)
v.check("T 13-04.d", c0 / (2 * 1e10) / 10 * 1e3)
# speed of light from the symbolic wave equation: E = cos(w t - b z) satisfies d2E/dz2 = mu eps d2E/dt2 iff b = w sqrt(mu eps)
Ewave = sp.cos(w * t - b * z)
res = sp.simplify(sp.diff(Ewave, z, 2) - mu0 * e0 * sp.diff(Ewave, t, 2))
bsol = sp.solve(sp.simplify(res / Ewave), b)
speed = float(1 / (max(bsol, key=lambda s: float(s.subs(w, 1))) / w).subs(w, 1))
v.check("T 13-04.e", speed)

# ---------------------------------------------------------------- Example 1
v.check("Ex 13-04.1a", emf_uniform_B(1e-5, 2 * math.pi * 1e6, 0.02, 0.01) * 1e3)
v.check("Ex 13-04.1b", emf_uniform_B(1e-5, 2 * math.pi * 1e8, 0.02, 0.01))

# ---------------------------------------------------------------- Example 2
eps2 = 4 * e0
Q_per_V = eps2 * (1.0 / 1e-4) * 1e-4  # Gauss: Q = D A with D = eps V/d
v.check("Ex 13-04.2a", Q_per_V * 1e12)
Id = displacement_current(eps2, 1e-4, 1e-4, 1.0, 2 * math.pi * 1e9)
v.check("Ex 13-04.2b", Id / 1e-4)
v.check("Ex 13-04.2c", Id)
v.check("Ex 13-04.2d", abs(1j * 2 * math.pi * 1e9 * Q_per_V * 1.0))

# ---------------------------------------------------------------- Example 3
ratio = lambda sig, er, f: sig / (2 * math.pi * f * er * e0)  # noqa: E731
v.check("Ex 13-04.3a", ratio(sig_cu, 1, 1e9))
v.check("Ex 13-04.3b", ratio(4, 81, 1e6))
v.check("Ex 13-04.3c", ratio(4, 81, 1e10))
fx = brentq(lambda f: ratio(4, 81, f) - 1, 1e6, 1e11, xtol=1e-3)
v.check("Ex 13-04.3d", fx / 1e6)
# relaxation: integrate d rho/dt = -(sigma/eps) rho numerically and read the 1/e time
for sig, er, key, scale in ((sig_cu, 1, "e", 1.0), (4.0, 81, "f", 1e9)):
    k = sig / (er * e0)
    tt = np.linspace(0, 3 / k, 300001)
    rho = np.exp(-k * tt)  # exact solution of the linear ODE; check the ODE residual numerically
    v.assert_true(f"relaxation ODE residual ({key})", np.max(np.abs(np.gradient(rho, tt) + k * rho)) < 1e-4 * k)
    v.check(f"Ex 13-04.3{key}", tt[np.argmin(np.abs(rho - math.exp(-1)))] * scale)
v.assert_true("crossover = 1/(2 pi tau)", abs(fx * 2 * math.pi * 81 * e0 / 4 - 1) < 1e-9)

# ---------------------------------------------------------------- Example 4 (sympy)
w4 = 2 * math.pi * 1e8
E4 = (10 * sp.cos(w * t - b * z), 0, 0)
# Faraday: dB/dt = -curl E  -> integrate in time (no static part)
dBdt = [-c for c in curl(E4)]
B4 = [sp.integrate(c, t, conds="none") for c in dBdt]
H4 = [c / mu0 for c in B4]
# Ampere-Maxwell residual must vanish for the right beta
resid = sp.simplify((curl(H4)[0] - e0 * sp.diff(E4[0], t)) / sp.sin(w * t - b * z))
v.assert_true("Ampere-Maxwell residual is a pure sinusoid", resid.free_symbols <= {w, b}, str(resid))
bsol4 = [r for r in sp.solve(resid, b) if float(r.subs(w, w4)) > 0][0]
beta4 = float(bsol4.subs(w, w4))
v.check("Ex 13-04.4a", beta4)
v.check("Ex 13-04.4b", 2 * math.pi / beta4)
Hy = sp.lambdify(t, H4[1].subs({w: w4, b: beta4, z: 0}))
Ex4 = sp.lambdify(t, E4[0].subs({w: w4, b: beta4, z: 0}))
tt = np.linspace(0, 2 * math.pi / w4, 2001)
v.check("Ex 13-04.4c", np.max(np.abs(Hy(tt))) * 1e3)
v.check("Ex 13-04.4d", time_avg(lambda s: Ex4(s) * Hy(s), w4))

# ---------------------------------------------------------------- Example 5
a5, I5, L5 = 1e-3, 10.0, 1.0
R5 = L5 / quad(lambda r: sig_cu * 2 * math.pi * r, 0, a5)[0]  # conductance of the cross-section
v.check("Ex 13-04.5a", R5 * 1e3)
v.check("Ex 13-04.5b", I5**2 * R5)
E5 = I5 * R5 / L5
H5 = I5 / (2 * math.pi * a5)  # Ampere: enclosed current over the circumference
v.check("Ex 13-04.5c", E5 * 1e3)
v.check("Ex 13-04.5d", H5)
S5 = np.linalg.norm(np.cross([0, 0, E5], [0, H5, 0]))  # E along z, H along phi (at the +x point)
v.check("Ex 13-04.5e", S5)
P5 = quad(lambda phi: S5 * a5 * L5, 0, 2 * math.pi)[0]
v.check("Ex 13-04.5f", P5)

# ---------------------------------------------------------------- Example 6
a6, b6, V6, I6 = 0.5e-3, 1.75e-3, 10.0, 0.2
lnab = quad(lambda r: 1 / r, a6, b6)[0]
E6 = lambda r: V6 / (r * lnab)  # noqa: E731
H6 = lambda r: I6 / (2 * math.pi * r)  # noqa: E731
v.check("Ex 13-04.6a", E6(a6) / 1e3)
v.check("Ex 13-04.6b", H6(a6))
v.check("Ex 13-04.6c", E6(a6) * H6(a6) / 1e6)
P6 = quad(lambda r: E6(r) * H6(r) * 2 * math.pi * r, a6, b6)[0]
v.check("Ex 13-04.6d", P6)
rhalf = brentq(lambda r: quad(lambda s: E6(s) * H6(s) * 2 * math.pi * s, a6, r)[0] - P6 / 2, a6, b6, xtol=1e-12)
v.check("Ex 13-04.6e", rhalf * 1e3)

# ---------------------------------------------------------------- practitioner and simulation
v.check("Prac 13-04.a", math.sqrt(10 * eta0))
v.check("Prac 13-04.b", 27.5 / 0.073)
v.check("Prac 13-04.c", brentq(lambda r: 1 / (4 * math.pi * r * r) - 10, 1e-3, 10) * 100)
v.check("Sim 13-04.a", Id)

# ---------------------------------------------------------------- Problems
v.check("13-04.1a", emf_uniform_B(2e-4, 2 * math.pi * 60, 0.1, 0.1) * 1e3)
v.check("13-04.2a", displacement_current(e0, 1.0, 1.0, 1e3, 2 * math.pi * 1e9))  # 1 m2 area, E = 1 kV/m
for rho_ohm_cm, k1, k2, fs in ((0.5, "a", "b", 1e9), (2.3e5, "c", "d", 1e3)):
    tau = 11.7 * e0 * rho_ohm_cm * 1e-2
    v.check(f"13-04.3{k1}", tau)
    fco = brentq(lambda f: (1 / (rho_ohm_cm * 1e-2)) / (2 * math.pi * f * 11.7 * e0) - 1, 1, 1e14, xtol=1e-6)
    v.check(f"13-04.3{k2}", fco / fs)

# 4: sympy curl of the given H phasor
Hph = (0, 0.1 * sp.exp(-2j * z), 0)
omega4 = 2 * c0
Eph = [sp.simplify(cc / (sp.I * omega4 * e0)) for cc in curl(Hph)]
Ex_amp = complex(Eph[0].subs(z, 0))
v.check("13-04.4a", omega4)
v.check("13-04.4b", omega4 / (2 * math.pi) / 1e6)
v.check("13-04.4c", abs(Ex_amp))
v.assert_true("E in phase with H", abs(np.angle(Ex_amp)) < 1e-12)
v.check("13-04.4d", 0.5 * (Ex_amp * np.conj(0.1)).real)
v.check("13-04.5a", float(-sp.diff(1.0 * x / 0.01, x)))
sig6 = 2 * math.pi * 1e9 * 4.3 * e0 * 0.02
v.check("13-04.6a", sig6 * 1e3)
v.check("13-04.6b", time_avg(lambda s: sig6 * (100 * np.cos(2 * math.pi * 1e9 * s)) ** 2, 2 * math.pi * 1e9))

# 7: Ampere-Maxwell around the rim, Poynting flux through the rim surface
r7, d7 = 0.01, 1e-3
C7 = e0 * quad(lambda r: 2 * math.pi * r, 0, r7)[0] / d7
Id7 = C7 * 1e9
H7 = Id7 / (2 * math.pi * r7)
S7 = 100 / d7 * H7
P7 = quad(lambda zz_: S7 * 2 * math.pi * r7, 0, d7)[0]
v.check("13-04.7a", C7 * 1e12)
v.check("13-04.7b", Id7 * 1e3)
v.check("13-04.7c", H7 * 1e3)
v.check("13-04.7d", S7)
v.check("13-04.7e", P7)
hstep = 1e-12
W = lambda tt_: 0.5 * C7 * (100 + 1e9 * tt_) ** 2  # noqa: E731
v.check("13-04.7f", (W(hstep) - W(-hstep)) / (2 * hstep))

r8 = brentq(lambda r: 1000 / (4 * math.pi * r * r) - 10, 0.01, 100)
v.check("13-04.8a", r8)
v.check("13-04.8b", math.sqrt(10 * eta0))
lam9 = c0 / math.sqrt(4) / 1e9
v.check("13-04.9a", lam9 * 100)
v.check("13-04.9b", lam9 / 10 * 100)
v.check("13-04.9c", lam9 / 100 * 1e3)
E10, H10 = 1.0 / 1e-4, 10 / 0.02
v.check("13-04.10a", E10 / 1e3)
v.check("13-04.10b", H10)
v.check("13-04.10c", E10 * H10)
v.check("13-04.10d", quad(lambda s: E10 * H10 * 0.02, 0, 1e-4)[0])

sig11 = 2 * math.pi * 1e8 * 4.3 * e0 * 0.02
v.check("13-04.11a", sig11 * 1e3)
v.check("13-04.11b", time_avg(lambda s: sig11 * (1e4 * np.cos(2 * math.pi * 1e8 * s)) ** 2, 2 * math.pi * 1e8) * 1e-7 * 1e3)
C11 = 4.3 * e0 * 1e-4 / 1e-3
Y11 = 2 * math.pi * 1e8 * C11 * (0.02 + 1j)  # G + j omega C with G = omega C tan delta
v.check("13-04.11c", C11 * 1e12)
v.check("13-04.11d", Y11.real * 1e6)
v.check("13-04.11e", 0.5 * (10 * np.conj(Y11 * 10)).real * 1e3)

# 12: numerical derivative of the flux linkage
wg = 2 * math.pi * 60
lam12 = lambda tt_: 100 * 0.5 * 0.01 * np.cos(wg * tt_)  # noqa: E731
tt = np.linspace(0, 1 / 60, 200001)
emf12 = -np.gradient(lam12(tt), tt)
v.check("13-04.12a", np.max(np.abs(emf12)))
v.check("13-04.12b", math.sqrt(np.mean(emf12[:-1] ** 2)))

# 13: symbolic Helmholtz check and root finding for the cutoff
a13 = 0.02286
E0 = sp.symbols("E0")
Ey = E0 * sp.sin(sp.pi * x / a13) * sp.exp(-sp.I * b * z)
helm = sp.simplify((sp.diff(Ey, x, 2) + sp.diff(Ey, z, 2) + w**2 * mu0 * e0 * Ey) / Ey)
v.assert_true("waveguide field vanishes on the walls", Ey.subs(x, 0) == 0 and abs(complex(Ey.subs({x: a13, E0: 1, z: 0}))) < 1e-15)
fc = brentq(lambda f: float((2 * math.pi * f) ** 2 * mu0 * e0 - (math.pi / a13) ** 2), 1e9, 2e10, xtol=1e-3)
v.check("13-04.13a", fc / 1e9)
b13 = float(max(sp.solve(helm.subs(w, 2 * math.pi * 1e10), b), key=lambda s: float(s)))
v.check("13-04.13b", b13)
v.check("13-04.13c", 2 * math.pi / b13 * 100)
v.check("13-04.14a", speed)
v.check("13-04.14b", math.sqrt(mu0 / e0))


# ---------------------------------------------------------------- Lab: 1D FDTD phase velocity
def fdtd_phase_velocity(cells_per_wavelength, courant, ncell=1500, nsteps=None):
    """Run a 1D Yee grid in normalized units (dz = 1, c = 1) with a soft sinusoidal source, then fit the phase
    of the steady-state wave across many cells to get the numerical phase velocity / c."""
    dt = courant  # c dt / dz with c = 1 and dz = 1
    omega = 2 * math.pi / cells_per_wavelength  # free-space wavelength = cpw cells
    nsteps = nsteps or int(1100 / courant)  # stop before the far-end reflection returns to the probe cells
    ez = np.zeros(ncell)
    hy = np.zeros(ncell - 1)
    src = 37  # the echo off the fixed left end returns after 74 cells, which never cancels the wave for these cpw
    rec = []
    t_rec = []
    probe = np.arange(200, 700)
    for n in range(nsteps):
        hy += courant * (ez[1:] - ez[:-1])
        ez[1:-1] += courant * (hy[1:] - hy[:-1])
        ez[src] += math.sin(omega * n * dt) * min(1.0, n * dt / 60)
        if n > nsteps - int(4 * cells_per_wavelength / courant):
            rec.append(ez[probe].copy())
            t_rec.append(n * dt)
    rec = np.array(rec)
    t_rec = np.array(t_rec)
    # complex amplitude at each probe cell by projecting on exp(-j omega t)
    ph = (rec * np.exp(-1j * omega * t_rec)[:, None]).sum(axis=0)
    phase = np.unwrap(np.angle(ph))
    k_num = -np.polyfit(probe, phase, 1)[0]
    return omega / k_num


def dispersion_phase_velocity(cpw, courant):
    kdz = 2 * math.pi / cpw
    return 2 * math.asin(courant * math.sin(kdz / 2)) / (courant * kdz)


if lab.exists():
    for cpw, key in ((20, "a"), (10, "b")):
        vp_formula = dispersion_phase_velocity(cpw, 0.5)
        vp_fdtd = fdtd_phase_velocity(cpw, 0.5)
        v.assert_true(f"FDTD measured phase velocity matches dispersion relation ({cpw} cells)",
                      abs(vp_fdtd - vp_formula) < 1e-3, f"{vp_fdtd} vs {vp_formula}")
        v.check(f"Lab 13-04.{key}", vp_formula)
    v.check("Lab 13-04.c", dispersion_phase_velocity(20, 1.0))
    v.assert_true("magic time step is exact in FDTD", abs(fdtd_phase_velocity(20, 1.0) - 1) < 2e-4)

sys.exit(v.finish())
