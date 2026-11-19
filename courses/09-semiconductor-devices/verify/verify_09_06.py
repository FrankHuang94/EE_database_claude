#!/usr/bin/env python3
"""Verify every number in chapter 09-06 (PN junction I-V, capacitance and breakdown), its solutions and lab.

Independent routes:
- minority-carrier currents by solving the steady diffusion boundary-value problem with finite differences
  (not the closed-form exponential or coth solutions); forward voltages by root finding on I(V);
- the temperature coefficient by numerical differentiation of V(T) with the full n_i(T) model;
- diffusion capacitance and admittance by solving the small-signal (complex) diffusion equation numerically;
- storage times by integrating the time-dependent diffusion equation (Crank-Nicolson) until the edge density
  reaches zero, and charge control by integrating the charge-control ODE with an event;
- avalanche multiplication by integrating the current-continuity ODE dJn/dx = an Jn + ap Jp through the
  depletion region (not the closed-form ionization integral), with breakdown by root finding;
- the Richardson constant by quadrature over a Maxwell-Boltzmann velocity distribution;
- design optima by numerical minimization.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants as C
from scipy.integrate import quad, solve_ivp
from scipy.linalg import solve_banded
from scipy.optimize import brentq, minimize_scalar
from scipy.special import erf

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("09-06", COURSE / "chapters" / "09-06-pn-junction-iv-and-capacitance.md",
                        COURSE / "solutions" / "09-06-solutions.md",
                        COURSE / "labs" / "09-06-lab" / "README.md")

Q = C.e
KB = C.k / C.e                       # eV/K
VT = KB * 300
NI = 1.0e10
EPS = 11.7 * C.epsilon_0 / 100       # F/cm
NC = 3.2e19
CN, CP = 1.1e-30, 0.3e-30


def mun(N):
    return 92 + 1268 / (1 + (N / 1.3e17) ** 0.91)


def mup(N):
    return 48 + 402 / (1 + (N / 6.3e16) ** 0.76)


def Eg(T):
    return 1.17 - 4.73e-4 * T ** 2 / (T + 636)


def niT(T):
    return NI * (T / 300) ** 1.5 * math.exp(Eg(300) / (2 * KB * 300) - Eg(T) / (2 * KB * T))


# ------------------------------------------------------------------ numerical minority-carrier solver
def diffusion_flux(D, tau, length, n=4001, omega=0.0):
    """Solve D p'' - (1 + j w tau) p / tau = 0 on [0, length], p(0) = 1, p(length) = 0, by finite
    differences; return -D p'(0) (carrier flux per unit edge excess, cm/s) from a 2nd-order one-sided
    difference. Complex when omega > 0."""
    x = np.linspace(0.0, length, n)
    h = x[1] - x[0]
    k2 = (1 + 1j * omega * tau) / (D * tau)
    m = n - 2
    ab = np.zeros((3, m), dtype=complex)
    ab[0, 1:] = 1 / h ** 2
    ab[1, :] = -2 / h ** 2 - k2
    ab[2, :-1] = 1 / h ** 2
    rhs = np.zeros(m, dtype=complex)
    rhs[0] = -1 / h ** 2
    inner = solve_banded((1, 1), ab, rhs)
    p = np.concatenate([[1.0], inner, [0.0]])
    dp0 = (-3 * p[0] + 4 * p[1] - p[2]) / (2 * h)
    out = -D * dp0
    return out if omega else out.real


def long_flux(D, tau):
    L = math.sqrt(D * tau)
    return diffusion_flux(D, tau, 25 * L, n=20001)


# ------------------------------------------------------------------ Example 09-06.1
NA, ND, TP, AREA = 1e19, 1e16, 1e-6, 1e-4
v.check("Ex 09-06.1a", mup(ND))
Dp = VT * mup(ND)
v.check("Ex 09-06.1b", Dp)
Lp = math.sqrt(Dp * TP)
v.check("Ex 09-06.1c", Lp * 1e4)
pn0 = NI ** 2 / ND
Jp0 = Q * pn0 * long_flux(Dp, TP)
v.check("Ex 09-06.1d", Jp0)
taun = 1 / (CP * NA ** 2)
v.check("Ex 09-06.1e", taun * 1e9)
v.check("Ex 09-06.1f", mun(NA))
Dn = VT * mun(NA)
v.check("Ex 09-06.1g", Dn)
v.check("Ex 09-06.1h", math.sqrt(Dn * taun) * 1e4)
Jn0 = Q * (NI ** 2 / NA) * long_flux(Dn, taun)
v.check("Ex 09-06.1i", Jn0)
v.check("Ex 09-06.1j", 100 * Jp0 / (Jp0 + Jn0))
Is = AREA * (Jp0 + Jn0)
v.check("Ex 09-06.1k", Is)


def vfwd(I, Is_, T=300.0, eta=1.0):
    return brentq(lambda V: Is_ * (math.exp(V / (eta * KB * T)) - 1) - I, -1, 2, xtol=1e-14)


V10 = vfwd(1e-5, Is)
v.check("Ex 09-06.1l", V10)
v.check("Ex 09-06.1m", vfwd(1e-4, Is))
v.check("Ex 09-06.1n", (vfwd(1e-4, Is) - V10) * 1e3)
Vhi = brentq(lambda V: pn0 * (math.exp(V / VT) - 1) - ND, 0, 1.5, xtol=1e-14)
v.check("Ex 09-06.1o", Vhi)
v.check("T 09-06.b", Vhi)
v.check("Ex 09-06.1p", Is * (math.exp(Vhi / VT) - 1) * 1e3)
dp10 = pn0 * (math.exp(V10 / VT) - 1)
v.check("Ex 09-06.1q", dp10)
v.check("Ex 09-06.1r", 100 * dp10 / ND)

# ------------------------------------------------------------------ Example 09-06.2 (short diode)
WN = 2e-4
Jp_short = Q * pn0 * diffusion_flux(Dp, TP, WN, n=20001)
v.check("Ex 09-06.2a", Jp_short / Jp0)
v.check("Ex 09-06.2b", Jp_short)
Jp_lin = Q * pn0 * Dp / WN
v.check("Ex 09-06.2c", Jp_lin)
Is_short = AREA * (Jp_short + Jn0)
v.check("Ex 09-06.2d", Is_short)
V10s = vfwd(1e-5, Is_short)
v.check("Ex 09-06.2e", V10s)
v.check("Ex 09-06.2f", (V10 - V10s) * 1e3)
# fraction recombining: compare flux into the contact with flux injected (numerical profile)
x = np.linspace(0, WN, 20001)
h = x[1] - x[0]
k2 = 1 / (Dp * TP)
ab = np.zeros((3, len(x) - 2))
ab[0, 1:] = 1 / h ** 2
ab[1, :] = -2 / h ** 2 - k2
ab[2, :-1] = 1 / h ** 2
rhs = np.zeros(len(x) - 2)
rhs[0] = -1 / h ** 2
prof = np.concatenate([[1.0], solve_banded((1, 1), ab, rhs), [0.0]])
flux_in = -(-3 * prof[0] + 4 * prof[1] - prof[2]) / (2 * h)
flux_out = -(3 * prof[-1] - 4 * prof[-2] + prof[-3]) / (2 * h)
v.check("Ex 09-06.2g", 100 * (1 - flux_out / flux_in))
v.check("Ex 09-06.2h", WN ** 2 / (2 * Dp) * 1e9)
v.check("Ex 09-06.2i", 100 * (Jp_short - Jp_lin) / Jp_short)
v.check("Ex 09-06.2j", WN / Lp)


# ------------------------------------------------------------------ junction helpers
def vbi(NA_, ND_):
    return VT * math.log(ND_ / NI) + VT * math.log(NA_ / NI)


def wdep(NA_, ND_, VA):
    """Depletion width by root finding on the potential of the uniform depletion charges."""
    Vb = vbi(NA_, ND_)
    def pot(W):
        xn, xp = W * NA_ / (NA_ + ND_), W * ND_ / (NA_ + ND_)
        return Q * (ND_ * xn ** 2 + NA_ * xp ** 2) / (2 * EPS)
    return brentq(lambda W: pot(W) - (Vb - VA), 1e-9, 1e-1, xtol=1e-16)


# ------------------------------------------------------------------ Example 09-06.3
v.check("Ex 09-06.3a", vbi(NA, ND))
W04 = wdep(NA, ND, 0.4)
v.check("Ex 09-06.3b", W04 * 1e4)
# recombination prefactor: integrate the maximum SRH rate over the width (rate at n = p with tau0)
tau0 = 1e-6
Js = Jp0 + Jn0
Jr0 = Q * W04 * NI / (2 * tau0)
v.check("Ex 09-06.3c", Jr0)
Vx = brentq(lambda V: Js * math.exp(V / VT) - Jr0 * math.exp(V / (2 * VT)), 0.1, 0.8, xtol=1e-14)
v.check("Ex 09-06.3d", Vx)
v.check("Ex 09-06.3e", Jr0 * math.exp(0.2 / (2 * VT)) / (Js * math.exp(0.2 / VT)))
v.check("Ex 09-06.3f", Jr0 * math.exp(0.6 / (2 * VT)) / (Js * math.exp(0.6 / VT)))
hV = 1e-6
lnI = lambda V: math.log(Js * math.exp(V / VT) + Jr0 * math.exp(V / (2 * VT)))
v.check("Ex 09-06.3g", 1 / (VT * (lnI(Vx + hV) - lnI(Vx - hV)) / (2 * hV)))
W5 = wdep(NA, ND, -5)
v.check("Ex 09-06.3h", W5 * 1e4)
# generation: SRH rate with n, p << ni, mid-gap traps
U_gen = NI ** 2 / (tau0 * (2 * NI))
Jgen = Q * U_gen * W5
v.check("Ex 09-06.3i", Jgen)
v.check("Ex 09-06.3j", Jgen * AREA * 1e12)
v.check("Ex 09-06.3k", Jgen * AREA / Is)

# ------------------------------------------------------------------ Example 09-06.4 (temperature)
def Is_T(T, Is300):
    return Is300 * (niT(T) / NI) ** 2


r350 = Is_T(350, 1.0)
v.check("Ex 09-06.4a", r350)
v.check("Ex 09-06.4g", Is_T(350, Is))
V350 = vfwd(1e-5, Is_T(350, Is), T=350)
v.check("Ex 09-06.4b", V350)
v.check("Ex 09-06.4h", (V10 - V350) * 1e3)
v.check("Ex 09-06.4c", (V350 - V10) / 50 * 1e3)
dT = 1e-3
dVdT = (vfwd(1e-5, Is_T(300 + dT, Is), T=300 + dT) - vfwd(1e-5, Is_T(300 - dT, Is), T=300 - dT)) / (2 * dT)
v.check("Ex 09-06.4d", dVdT * 1e3)
v.check("Ex 09-06.4e", (vfwd(1e-4, Is) - V10) * 1e3)
v.check("Ex 09-06.4f", (vfwd(1e-4, Is_T(300 + dT, Is), T=300 + dT) - vfwd(1e-5, Is_T(300 + dT, Is), T=300 + dT)
                        - (vfwd(1e-4, Is_T(300 - dT, Is), T=300 - dT) - vfwd(1e-5, Is_T(300 - dT, Is), T=300 - dT)))
        / (2 * dT) * 1e6)
v.check("T 09-06.c", Eg(300))
v.check("T 09-06.d", (Eg(300 + dT) - Eg(300 - dT)) / (2 * dT) * 1e3)
Vg0 = Eg(300) - 300 * (Eg(300 + dT) - Eg(300 - dT)) / (2 * dT)
v.check("T 09-06.e", Vg0)
# dV/dT at 0.6 V: pick the current that gives 0.6 V and differentiate numerically
I06 = Is * (math.exp(0.6 / VT) - 1)
d06 = (vfwd(I06, Is_T(300 + dT, Is), T=300 + dT) - vfwd(I06, Is_T(300 - dT, Is), T=300 - dT)) / (2 * dT)
v.check("T 09-06.t", d06 * 1e3)
v.check("T 09-06.a", 2 * VT * math.log(10) * 1e3)
v.check("T 09-06.u", 1 / (1e-3 / VT))
v.check("P 09-06.d", niT(350) / NI)

# ------------------------------------------------------------------ Example 09-06.5 (small signal)
I_D = 1e-5
g = I_D / VT  # check against numerical derivative of the diode equation
g_num = (Is * (math.exp((V10 + 1e-7) / VT) - 1) - Is * (math.exp((V10 - 1e-7) / VT) - 1)) / 2e-7
v.check("Ex 09-06.5a", g_num * 1e3)
v.check("Ex 09-06.5b", 1 / g_num)
v.check("Ex 09-06.5c", I_D * TP * 1e12)
# quasi-static dQ/dV with Q = tau_p I(V) (one-sided: all current treated as hole current)
Qs = lambda V: TP * Is * (math.exp(V / VT) - 1)
v.check("Ex 09-06.5d", (Qs(V10 + 1e-7) - Qs(V10 - 1e-7)) / 2e-7 * 1e12)
# exact small-signal: numerical complex diffusion problem at small omega
w = 1e-3 / TP
flux_w = diffusion_flux(Dp, TP, 25 * Lp, n=20001, omega=w)
Cd = g_num * (flux_w.imag / long_flux(Dp, TP)) / w
v.check("Ex 09-06.5e", Cd * 1e12)
Cj0 = EPS * AREA / wdep(NA, ND, 0.0)
v.check("Ex 09-06.5f", Cj0 * 1e12)
v.check("Ex 09-06.5g", wdep(NA, ND, 0.0) * 1e4)
Cj06 = EPS * AREA / wdep(NA, ND, 0.6)
v.check("Ex 09-06.5h", Cj06 * 1e12)
v.check("Ex 09-06.5k", Cd / Cj0)
v.check("Ex 09-06.5l", Cd / Cj06)
# corner: frequency where g_d = w C_d
v.check("Ex 09-06.5i", g_num / (2 * math.pi * Cd) / 1e3)
tau5 = 1e-6
v.check("Ex 09-06.5n", 1 / (2 * math.pi * tau5) / 1e3)
x1 = brentq(lambda x: np.sqrt(1 + 1j * x).real - 1.01, 1e-3, 2)
v.check("Ex 09-06.5o", x1 / (2 * math.pi * tau5) / 1e3)
Y2 = np.sqrt(1 + 2j)
v.check("Ex 09-06.5p", (Y2.real - 1) * 100)
v.check("Ex 09-06.5q", (1 - Y2.imag / 1.0) * 100)   # model C term is x/2 = 1 at x = 2
flux_ws = diffusion_flux(Dp, TP, WN, n=20001, omega=w)
Cds = g_num * (flux_ws.imag / diffusion_flux(Dp, TP, WN, n=20001)) / w
v.check("Ex 09-06.5m", Cds * 1e12)
v.check("Ex 09-06.5j", g_num * WN ** 2 / (3 * Dp) * 1e12)   # leading-order (W << L) formula


# ------------------------------------------------------------------ storage time (PDE)
def storage_pde(ratio_R_over_F, L=12.0, n=2401, dt=1e-5):
    """Dimensionless long diode: u_t = u_xx - u, u(x,0) = exp(-x), flux at x = 0 reversed to
    ratio * I_F; return t_s/tau when u(0) = 0 (Crank-Nicolson)."""
    x = np.linspace(0, L, n)
    h = x[1] - x[0]
    N = n - 1
    main = np.full(N, -2.0 / h ** 2 - 1.0)
    up = np.full(N - 1, 1.0 / h ** 2)
    up[0] = 2.0 / h ** 2
    lo = np.full(N - 1, 1.0 / h ** 2)
    b = np.zeros(N)
    b[0] = -2 * ratio_R_over_F / h
    A1 = np.zeros((3, N))
    A1[0, 1:] = -0.5 * dt * up
    A1[1, :] = 1 - 0.5 * dt * main
    A1[2, :-1] = -0.5 * dt * lo
    u = np.exp(-x[:N])
    t = 0.0
    while True:
        rhs = u + 0.5 * dt * (main * u + np.concatenate([up * u[1:], [0]]) + np.concatenate([[0], lo * u[:-1]])) + dt * b
        new = solve_banded((1, 1), A1, rhs)
        t += dt
        if new[0] <= 0:
            return t - dt + dt * u[0] / (u[0] - new[0])
        u = new


def storage_cc(IF, IR, tau):
    ev = lambda t, q: q[0]
    ev.terminal = True
    sol = solve_ivp(lambda t, q: [-IR - q[0] / tau], [0, 50 * tau], [IF * tau], events=ev, rtol=1e-11, atol=1e-30)
    return sol.t_events[0][0]


ts1 = storage_pde(1.0)
v.check("Ex 09-06.6a", 20e-6 * TP * 1e12)
v.check("Ex 09-06.6b", storage_cc(20e-6, 20e-6, TP) * 1e6)
v.check("Ex 09-06.6c", ts1 * TP * 1e6)
v.check("Ex 09-06.6d", storage_cc(20e-6, 200e-6, TP) * 1e6)
ts10 = storage_pde(10.0, dt=2e-6)
v.check("Ex 09-06.6e", ts10 * TP * 1e9)
v.check("Ex 09-06.6f", ts1 * 6.73)
v.check("Ex 09-06.6g", brentq(lambda z: erf(z) - 0.5, 0, 2))
v.check("T 09-06.v", storage_cc(1, 1, 1) / ts1)
# Kingston formula cross-check against the PDE
v.assert_true("Kingston erf formula matches the PDE (ratio 1)",
              abs(brentq(lambda s: erf(math.sqrt(s)) - 0.5, 1e-9, 5) - ts1) < 2e-4)
v.assert_true("Kingston erf formula matches the PDE (ratio 10)",
              abs(brentq(lambda s: erf(math.sqrt(s)) - 1 / 11, 1e-9, 5) - ts10) < 5e-5)

# ------------------------------------------------------------------ avalanche (continuity ODE)
def an(F):
    return 3.318e5 * np.exp(-1.174e6 / F)


def ap(F):
    return np.where(F < 5.3e5, 2e6 * np.exp(-1.97e6 / F), 5.6e5 * np.exp(-1.32e6 / F))


def jn0_needed(field, W):
    """Integrate dJn/dx = an Jn + ap (J - Jn) backward from Jn(W) = J = 1; return Jn(0) = 1/M_n."""
    def rhs(x, y):
        F = max(field(x), 1e3)
        return [float(an(F)) * y[0] + float(ap(F)) * (1 - y[0])]
    sol = solve_ivp(rhs, [W, 0], [1.0], rtol=1e-10, atol=1e-13, max_step=W / 400)
    return sol.y[0, -1]


def jp_hole_needed(field, W):
    """Hole-initiated form: integrate dJp/dx = -(an (J - Jp) + ap Jp) forward from Jp(0) = J = 1;
    return Jp(W) = 1/M_p."""
    def rhs(x, y):
        F = max(field(x), 1e3)
        return [-(float(an(F)) * (1 - y[0]) + float(ap(F)) * y[0])]
    sol = solve_ivp(rhs, [0, W], [1.0], rtol=1e-10, atol=1e-13, max_step=W / 400)
    return sol.y[0, -1]


def one_sided(Em, N):
    W = EPS * Em / (Q * N)
    return (lambda x: Em * (1 - x / W)), W


def breakdown(N, hole=False):
    f = jp_hole_needed if hole else jn0_needed
    Em = brentq(lambda E: f(*one_sided(E, N)), 1.5e5, 9e5, xtol=1.0)
    W = EPS * Em / (Q * N)
    return Em, Em * W / 2 - vbi(1e19, N), W


Em16, VB16, W16 = breakdown(1e16)
v.check("Ex 09-06.7a", Em16)
v.check("Ex 09-06.7b", W16 * 1e4)
v.check("Ex 09-06.7c", VB16)


def mult(VR, N):
    Vt = vbi(1e19, N) + VR
    W = math.sqrt(2 * EPS * Vt / (Q * N))
    Em = 2 * Vt / W
    return 1 / jn0_needed(lambda x: Em * (1 - x / W), W), Em


M40, E40 = mult(40, 1e16)
v.check("Ex 09-06.7d", 1 - 1 / M40)
v.check("Ex 09-06.7e", M40)
v.check("Ex 09-06.7i", E40)
M50, _ = mult(50, 1e16)
v.check("Ex 09-06.7f", M50)
v.check("Ex 09-06.7j", 1 - 1 / M50)
v.check("Ex 09-06.7g", EPS * 3e5 ** 2 / (2 * Q * 1e16) - vbi(1e19, 1e16))
hu = lambda N: 15 * (1e17 / N) ** 0.6
v.check("Ex 09-06.7h", hu(1e16))
v.check("Ex 09-06.7k", 100 * (hu(1e16) / VB16 - 1))
for N, kE, kV, kW, kH in ((1e15, "T 09-06.j", "T 09-06.k", "T 09-06.l", "T 09-06.p"),
                          (1e17, "T 09-06.m", "T 09-06.n", "T 09-06.o", "T 09-06.q")):
    Em, VB, W = breakdown(N)
    v.check(kE, Em)
    v.check(kV, VB)
    v.check(kW, W * 1e4)
    v.check(kH, hu(N))
v.check("T 09-06.z", math.log(breakdown(1e17)[1] / breakdown(1e15)[1]) / math.log(100))
v.check("T 09-06.f", float(an(3e5)))
v.check("T 09-06.g", float(ap(3e5)))
v.check("T 09-06.h", float(an(3e5) / ap(3e5)))
v.check("T 09-06.s", 1 / float(an(3e5)) * 1e4)
v.check("T 09-06.i", brentq(lambda F: float(an(F) - ap(F)), 3e5, 5.29e5))

# ------------------------------------------------------------------ Schottky and contacts
def richardson(m):
    """K = q * N_C(m) * <v_x, v_x > 0> * (1/2) / T^2, by quadrature over the 1D Maxwell-Boltzmann
    distribution (per T^2, in A/(cm^2 K^2)) at T = 300 K."""
    T = 300.0
    kT = C.k * T
    vth = math.sqrt(kT / m)                                          # velocity scale, m/s
    g = lambda u: u * math.exp(-u * u / 2) / math.sqrt(2 * math.pi)  # v f(v) in units of vth
    mean_pos = vth * quad(g, 0, np.inf, epsabs=0)[0]                 # integral of v f over v > 0
    Nc = 2 * (2 * math.pi * m * kT / C.h ** 2) ** 1.5             # m^-3
    return Q * Nc * mean_pos / T ** 2 / 1e4


v.check("T 09-06.r", richardson(C.m_e))
K = 100.0
J0 = K * 300 ** 2 * math.exp(-0.67 / VT)
v.check("Ex 09-06.8a", J0)
v.check("Ex 09-06.8b", J0 * AREA * 1e9)
v.check("Ex 09-06.8c", J0 * AREA / Is)
VS = vfwd(1e-5, J0 * AREA)
v.check("Ex 09-06.8d", VS)
v.check("Ex 09-06.8e", V10 - VS)
v.check("Ex 09-06.8q", VT * math.log(NC / 1e16))
VbiS = 0.67 - VT * math.log(NC / 1e16)
v.check("Ex 09-06.8f", VbiS)
v.check("Ex 09-06.8g", math.sqrt(2 * EPS * VbiS / (Q * 1e16)) * 1e4)
v.check("Ex 09-06.8h", 4.6 - 4.05)
v.check("Ex 09-06.8i", 0.7 + 0.2 * (4.6 - 4.75))
v.check("T 09-06.w", VT * math.log(1e3))
v.check("T 09-06.x", VT * math.log(1e8))
v.check("T 09-06.y", Eg(300) / 1e6 * 1e7)
MSTAR = 0.26 * C.m_e
EPS_SI = EPS * 100


def wkb_exponent(phi, N_cm3):
    """2 * integral of kappa over a rectangular barrier of height q*phi and thickness W/2."""
    W = math.sqrt(2 * EPS * phi / (Q * N_cm3)) / 100        # m
    kappa = math.sqrt(2 * MSTAR * Q * phi) / C.hbar
    return 2 * quad(lambda x: kappa, 0, W / 2)[0]


for N, kW, kE in ((1e18, "Ex 09-06.8j", "Ex 09-06.8m"), (1e19, "Ex 09-06.8k", "Ex 09-06.8n"),
                  (1e20, "Ex 09-06.8l", "Ex 09-06.8o")):
    v.check(kW, math.sqrt(2 * EPS * 0.6 / (Q * N)) * 1e7)
    v.check(kE, wkb_exponent(0.6, N))
v.check("Ex 09-06.8p", math.exp(wkb_exponent(0.6, 1e19) - wkb_exponent(0.6, 1e20)))
v.assert_true("closed-form exponent (4 pi phi/h) sqrt(eps m/N) equals the WKB integral",
              abs((4 * math.pi * 0.6 / C.h) * math.sqrt(EPS_SI * MSTAR / 1e26) - wkb_exponent(0.6, 1e20)) < 1e-9)

# practitioner
v.check("P 09-06.a", 1e-9 / (20e-7) ** 2)
v.check("P 09-06.b", 140 * math.pi * (0.15e-4) ** 2)
v.check("P 09-06.c", 50 * 0.8)

# ------------------------------------------------------------------ Solutions
# 1
pn05 = NI ** 2 / 5e15
v.check("09-06.1a", pn05)
v.check("09-06.1b", pn05 * math.exp(0.5 / VT))
v.check("09-06.1c", pn05 * math.exp(0.5 / VT) / 5e15)
v.check("09-06.1d", pn05 * math.exp(0.65 / VT))
v.check("09-06.1e", 100 * pn05 * math.exp(0.65 / VT) / 5e15)
v.check("09-06.1f", brentq(lambda V: pn05 * (math.exp(V / VT) - 1) - 5e14, 0, 1, xtol=1e-14))
v.check("09-06.1g", math.exp(-0.2 / VT))
# 2
Dn2 = VT * mun(1e16)
v.check("09-06.2a", mun(1e16))
v.check("09-06.2b", Dn2)
v.check("09-06.2c", math.sqrt(Dn2 * 2e-6) * 1e4)
Js2 = Q * (NI ** 2 / 1e16) * long_flux(Dn2, 2e-6)
v.check("09-06.2d", Js2)
Is2 = Js2 * 2.5e-5
v.check("09-06.2e", Is2)
v.check("09-06.2f", vfwd(1e-6, Is2))
v.check("09-06.2g", Is2 * (math.exp(0.55 / VT) - 1) * 1e6)
# 3: fit the exponential through each pair (least squares on ln I)
for (pts, ke, k0) in ((((0.20, 1.00e-9), (0.32, 10.2e-9)), "09-06.3a", "09-06.3c"),
                      (((0.50, 0.200e-6), (0.56, 2.00e-6)), "09-06.3b", "09-06.3d")):
    Vs = np.array([p[0] for p in pts])
    lnI_ = np.log([p[1] for p in pts])
    slope, icpt = np.polyfit(Vs, lnI_, 1)
    v.check(ke, 1 / (slope * VT))
    v.check(k0, math.exp(icpt))
# 4
Dp4 = VT * mup(1e15)
Lp4 = math.sqrt(Dp4 * 1e-5)
W4 = 20e-4
v.check("09-06.4a", mup(1e15))
v.check("09-06.4b", Dp4)
v.check("09-06.4c", Lp4 * 1e4)
v.check("09-06.4d", W4 / Lp4)
ratio4 = diffusion_flux(Dp4, 1e-5, W4, n=20001) / long_flux(Dp4, 1e-5)
v.check("09-06.4e", ratio4)
v.check("09-06.4f", Lp4 / W4)
v.check("09-06.4k", 100 * (1 - (Lp4 / W4) / ratio4))
v.check("09-06.4g", 100 * (1 - 1 / math.cosh(W4 / Lp4)))
v.check("09-06.4h", 100 * W4 ** 2 / (2 * Lp4 ** 2))
tt4 = W4 ** 2 / (2 * Dp4)
v.check("09-06.4i", tt4 * 1e9)
v.check("09-06.4j", 1e-5 / tt4)
# 5
tp5 = 1 / (CN * 1e38)
Dp5 = VT * mup(1e19)
Lp5 = math.sqrt(Dp5 * tp5)
v.check("09-06.5a", tp5 * 1e9)
v.check("09-06.5b", mup(1e19))
v.check("09-06.5c", Dp5)
v.check("09-06.5d", Lp5 * 1e4)
Dn5 = VT * mun(1e16)
v.check("09-06.5e", math.sqrt(Dn5 * 1e-6) * 1e4)
Jp5 = Q * (NI ** 2 / 1e19) * long_flux(Dp5, tp5)
Jn5 = Q * (NI ** 2 / 1e16) * long_flux(Dn5, 1e-6)
v.check("09-06.5f", Jp5)
v.check("09-06.5g", Jn5)
v.check("09-06.5h", 100 * Jn5 / (Jn5 + Jp5))
v.check("09-06.5i", 0.3e-4 / Lp5)
Jp5s = Q * (NI ** 2 / 1e19) * diffusion_flux(Dp5, tp5, 0.3e-4, n=20001)
v.check("09-06.5j", Jp5s / Jp5)
v.check("09-06.5k", Jp5s)
v.check("09-06.5l", Q * (NI ** 2 / 1e19) * Dp5 / 0.3e-4)
v.check("09-06.5m", 100 * Jn5 / (Jn5 + Jp5s))
v.check("09-06.5n", Jp5s / Jp5)
# 6
I6 = lambda V: 1e-15 * math.exp(V / VT) + 1e-10 * math.exp(V / (2 * VT))
eta6 = lambda V: 1 / (VT * (math.log(I6(V + 1e-6)) - math.log(I6(V - 1e-6))) / 2e-6)
v.check("09-06.6a", brentq(lambda V: 1e-15 * math.exp(V / VT) - 1e-10 * math.exp(V / (2 * VT)), 0.1, 1))
v.check("09-06.6b", I6(0.3))
v.check("09-06.6c", eta6(0.3))
v.check("09-06.6d", I6(0.6))
v.check("09-06.6e", eta6(0.6))
v.check("09-06.6f", brentq(lambda V: eta6(V) - 1.1, 0.5, 1.0, xtol=1e-12))
# 7
r7 = 7.00e-12 / 4.973e-16
v.check("09-06.7a", r7)
T7 = brentq(lambda T: 4.973e-16 * (niT(T) / NI) ** 2 - 7.00e-12 * (niT(T) / NI), 301, 800, xtol=1e-10)
v.check("09-06.7b", T7)
v.check("09-06.7c", T7 - 273.15)
Ea = lambda f: -(math.log(f(300 + dT)) - math.log(f(300 - dT))) / (1 / (KB * (300 + dT)) - 1 / (KB * (300 - dT)))
v.check("09-06.7d", Ea(niT))
v.check("09-06.7e", Ea(lambda T: niT(T) ** 2))
# 8
V8 = vfwd(1e-6, 2e-15)
v.check("09-06.8a", V8)
d8 = (vfwd(1e-6, Is_T(300 + dT, 2e-15), T=300 + dT) - vfwd(1e-6, Is_T(300 - dT, 2e-15), T=300 - dT)) / (2 * dT)
v.check("09-06.8b", d8 * 1e3)
v.check("09-06.8c", V8 + 75 * d8)
v.check("09-06.8d", Is_T(375, 2e-15))
V375 = vfwd(1e-6, Is_T(375, 2e-15), T=375)
v.check("09-06.8e", V375)
v.check("09-06.8f", (V8 + 75 * d8 - V375) * 1e3)
v.check("09-06.8g", (vfwd(8e-6, 2e-15) - V8) * 1e3)
v.check("09-06.8h", (vfwd(8e-6, Is_T(375, 2e-15), T=375) - V375) * 1e3)
# 9: numerical complex diffusion problem for the exact admittance
tau9 = 0.5e-6
g9 = 50e-6 / VT
v.check("09-06.9a", g9 * 1e3)
v.check("09-06.9b", 1 / g9)
D9 = Dp
L9 = math.sqrt(D9 * tau9)
fl0 = long_flux(D9, tau9)
wlow = 1e-3 / tau9
Cd9 = g9 * (diffusion_flux(D9, tau9, 25 * L9, n=20001, omega=wlow).imag / fl0) / wlow
v.check("09-06.9c", Cd9 * 1e12)
w9 = 2 * math.pi * 1e6
v.check("09-06.9d", w9 * tau9)
Y9 = g9 * diffusion_flux(D9, tau9, 25 * L9, n=40001, omega=w9) / fl0 + 1j * w9 * 2e-12
v.check("09-06.9e", Y9.real * 1e3)
v.check("09-06.9f", Y9.imag * 1e3)
v.check("09-06.9g", abs(Y9) * 1e3)
Ym = g9 + 1j * w9 * (Cd9 + 2e-12)
v.check("09-06.9h", Ym.imag * 1e3)
v.check("09-06.9i", abs(Ym) * 1e3)
v.check("09-06.9j", 100 * (abs(Ym) / abs(Y9) - 1))
v.check("09-06.9k", Y9.imag / w9 * 1e12)
v.check("09-06.9l", (Cd9 + 2e-12) * 1e12)
# 10
tau10 = 200e-9
v.check("09-06.10a", 5e-3 * tau10 * 1e9)
v.check("09-06.10b", storage_cc(5e-3, 2.5e-3, tau10) * 1e9)
ts05 = storage_pde(0.5)
v.check("09-06.10c", math.sqrt(ts05))
v.check("09-06.10d", ts05 * tau10 * 1e9)
v.check("09-06.10e", erf(math.sqrt(0.1)))
IR10 = brentq(lambda IR: storage_pde(IR / 5e-3, dt=1e-5) - 0.1, 5e-3, 15e-3, xtol=1e-7)
v.check("09-06.10f", IR10 * 1e3)
v.check("09-06.10g", storage_cc(5e-3, IR10, tau10) * 1e9)
# 11
Em11, VB11, W11 = breakdown(2e15)
v.check("09-06.11a", Em11)
v.check("09-06.11b", W11 * 1e4)
v.check("09-06.11c", vbi(1e19, 2e15))
v.check("09-06.11d", VB11)
v.check("09-06.11e", EPS * 9e10 / (2 * Q * 2e15) - vbi(1e19, 2e15))
v.check("09-06.11f", hu(2e15))
N100 = brentq(lambda N: breakdown(N)[1] - 100, 2e15, 1e16, xtol=1e10)
v.check("09-06.11g", N100)
NHu = brentq(lambda N: hu(N) - 100, 1e15, 1e16)
v.check("09-06.11h", NHu)
v.check("09-06.11i", 100 * (NHu / N100 - 1))
# 12
N12 = 1e18
Neff = N12 * N12 / (2 * N12)
Vb12 = vbi(N12, N12)
v.check("09-06.12a", Vb12)
v.check("09-06.12b", wdep(N12, N12, 0.0) * 1e7)
Vt12 = brentq(lambda Vt: math.sqrt(2 * Q * Neff * Vt / EPS) - 1e6, 0.1, 100, xtol=1e-12)
v.check("09-06.12c", Vt12)
v.check("09-06.12d", Vt12 - Vb12)
W12 = wdep(N12, N12, -(Vt12 - Vb12))
v.check("09-06.12e", W12 * 1e7)
v.check("09-06.12j", Eg(300) / 1e6 * 1e7)
v.check("09-06.12f", float(an(1e6)))
v.check("09-06.12g", float(ap(1e6)))
field12 = lambda x: 1e6 * (1 - abs(x - W12 / 2) / (W12 / 2))
jn12 = jn0_needed(field12, W12)
v.check("09-06.12h", 1 - jn12)
v.check("09-06.12i", 1 / jn12)
# 13
for phi, kI, kV, kH, kF in ((0.5, "09-06.13a", "09-06.13c", "09-06.13e", "09-06.13f"),
                            (0.9, "09-06.13b", "09-06.13d", "09-06.13g", "09-06.13h")):
    I0 = 0.01 * K * 300 ** 2 * math.exp(-phi / VT)
    I0h = 0.01 * K * 400 ** 2 * math.exp(-phi / (KB * 400))
    v.check(kI, I0)
    v.check(kV, vfwd(0.1, I0))
    v.check(kH, I0h * (1e3 if phi == 0.5 else 1e6))
    v.check(kF, I0h / I0)
# 14
T14 = 373.15
VT14 = KB * T14
v.check("09-06.14a", VT14 * 1e3)
I0S = 0.05 * K * T14 ** 2 * math.exp(-0.6 / VT14)
v.check("09-06.14b", I0S * 1e3)
r14 = (niT(T14) / NI) ** 2
v.check("09-06.14c", r14)
I0P = 0.05 * 1e-12 * r14
v.check("09-06.14d", I0P)
VFS = vfwd(5, I0S, T=T14)
VFP = vfwd(5, I0P, T=T14)
v.check("09-06.14e", VFS)
v.check("09-06.14f", VFP)
v.check("09-06.14g", 0.5 * 5 * VFS)
v.check("09-06.14h", 0.5 * 20 * I0S)
PS = 0.5 * 5 * VFS + 0.5 * 20 * I0S
v.check("09-06.14i", PS)
v.check("09-06.14j", 0.5 * 5 * VFP)
PP = 0.5 * 5 * VFP + 0.5 * 20 * I0P
v.check("09-06.14k", PP)
v.check("09-06.14r", PS / PP)


def loss(phi):
    """Loss with the forward drop V_T ln(I_F/I_0) (the +1 dropped, as in the solution)."""
    I0 = 0.05 * K * T14 ** 2 * math.exp(-phi / VT14)
    return 0.5 * 5 * VT14 * math.log(5 / I0) + 0.5 * 20 * I0


opt = minimize_scalar(loss, bounds=(0.4, 0.8), method="bounded", options={"xatol": 1e-9})
v.check("09-06.14m", opt.x)
v.check("09-06.14l", 0.05 * K * T14 ** 2 * math.exp(-opt.x / VT14) * 1e3)
v.check("09-06.14n", opt.fun)
v.check("09-06.14o", 100 * (loss(0.6) / opt.fun - 1))
v.check("09-06.14p", 100 * (loss(opt.x - 0.02) / opt.fun - 1))
v.check("09-06.14q", 100 * (loss(opt.x + 0.02) / opt.fun - 1))
# 15
e20 = wkb_exponent(0.6, 1e20)
v.check("09-06.15a", e20)
v.check("09-06.15b", brentq(lambda N: wkb_exponent(0.6, N) - 3, 1e20, 1e21))
e3 = wkb_exponent(0.6, 3e20)
v.check("09-06.15c", e3)
v.check("09-06.15d", math.exp(e20 - e3))
v.check("09-06.15e", 1e-7 / math.exp(e20 - e3))
e04 = wkb_exponent(0.4, 1e20)
v.check("09-06.15f", e04)
v.check("09-06.15g", math.exp(e20 - e04))
v.check("09-06.15h", 1e-9 / (20e-7 * 30e-7))

# ------------------------------------------------------------------ Lab
tsl2 = storage_pde(2.0, dt=4e-6)
v.check("Lab 09-06.a", tsl2)
v.check("Lab 09-06.b", storage_cc(1, 2, 1))
v.check("Lab 09-06.c", ts1 / tsl2)
v.check("Lab 09-06.d", storage_cc(1, 1, 1) / storage_cc(1, 2, 1))
v.check("Lab 09-06.e", breakdown(1e16, hole=True)[1])
v.check("Lab 09-06.f", VT / 50 * 1e3)
v.assert_true("electron- and hole-initiated breakdown agree at 1e16",
              abs(breakdown(1e16, hole=True)[1] - VB16) < 0.05)

v.finish()
