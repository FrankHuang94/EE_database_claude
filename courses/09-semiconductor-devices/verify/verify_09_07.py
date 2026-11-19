#!/usr/bin/env python3
"""Verify every number in chapter 09-07 (the bipolar junction transistor), its solutions and lab.

Independent routes:
- collector and base currents by solving the minority-carrier diffusion problem in the base and emitter
  with finite differences (including recombination), not from the closed short-base forms;
- band-gap-narrowing and SiGe factors as ratios of n_i^2 computed from shifted band gaps;
- depletion edges by root finding on the junction potential; the Early voltage by numerically
  differentiating I_C as the base-side depletion edge moves with V_CB;
- saturation points by solving the two Ebers-Moll equations with a root finder;
- base transit times by integrating the numerically solved drift-diffusion electron profile;
- f_T from the hybrid-pi current gain beta(f) evaluated until |beta| = 1;
- charge-control switching by integrating the charge-control ODE with an event.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants as C
from scipy.integrate import solve_ivp, trapezoid
from scipy.linalg import solve_banded
from scipy.optimize import brentq, fsolve

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("09-07", COURSE / "chapters" / "09-07-bipolar-junction-transistor.md",
                        COURSE / "solutions" / "09-07-solutions.md",
                        COURSE / "labs" / "09-07-lab" / "README.md")

Q = C.e
KB = C.k / C.e
VT = KB * 300
NI = 1.0e10
EPS = 11.7 * C.epsilon_0 / 100


def mun(N):
    return 92 + 1268 / (1 + (N / 1.3e17) ** 0.91)


def mup(N):
    return 48 + 402 / (1 + (N / 6.3e16) ** 0.76)


def ni2_shift(dEg):
    """n_i^2 for a band gap reduced by dEg (eV), from n_i^2 = N_C N_V exp(-E_g/kT) with fixed N_C N_V."""
    Eg = 1.12
    NCNV = NI ** 2 / math.exp(-Eg / VT)
    return NCNV * math.exp(-(Eg - dEg) / VT)


def short_flux(D, W, tau=None, n=4001):
    """-D dp/dx at x = 0 for p(0) = 1, p(W) = 0, solving D p'' = p/tau (or p'' = 0) numerically."""
    x = np.linspace(0, W, n)
    h = x[1] - x[0]
    k2 = 0.0 if tau is None else 1 / (D * tau)
    m = n - 2
    ab = np.zeros((3, m))
    ab[0, 1:] = 1 / h ** 2
    ab[1, :] = -2 / h ** 2 - k2
    ab[2, :-1] = 1 / h ** 2
    rhs = np.zeros(m)
    rhs[0] = -1 / h ** 2
    p = np.concatenate([[1.0], solve_banded((1, 1), ab, rhs), [0.0]])
    flux_in = -D * (-3 * p[0] + 4 * p[1] - p[2]) / (2 * h)
    flux_out = -D * (3 * p[-1] - 4 * p[-2] + p[-3]) / (2 * h)
    return flux_in, flux_out


def vbe_for(I, Is):
    return brentq(lambda V: Is * (math.exp(V / VT) - 1) - I, 0, 2, xtol=1e-14)


def junction_edges(NA, ND, VA):
    """Depletion edges (x_p, x_n) of a step junction by root finding on the potential."""
    Vbi = VT * math.log(NA * ND / NI ** 2)
    f = lambda W: Q * (ND * (W * NA / (NA + ND)) ** 2 + NA * (W * ND / (NA + ND)) ** 2) / (2 * EPS) - (Vbi - VA)
    W = brentq(f, 1e-9, 1e-1, xtol=1e-16)
    return W * ND / (NA + ND), W * NA / (NA + ND), W, Vbi


# ------------------------------------------------------------------ Example 1
AE, WB, NB, NE, WE, NC = 1e-7, 1e-5, 1e18, 1e20, 2e-5, 1e17
v.check("Ex 09-07.1a", mun(NB))
DB = VT * mun(NB)
v.check("Ex 09-07.1b", DB)
nB0 = NI ** 2 / NB
fl, _ = short_flux(DB, WB)
IS = Q * AE * nB0 * fl
v.check("Ex 09-07.1c", IS)
v.check("Ex 09-07.1d", vbe_for(1e-6, IS))
V1m = vbe_for(1e-3, IS)
v.check("Ex 09-07.1e", V1m)
v.check("Ex 09-07.1f", trapezoid(np.full(101, NB / DB), np.linspace(0, WB, 101)))
v.check("Ex 09-07.1g", NB * WB)
v.check("Ex 09-07.1j", NB * WB * 1e-8)
n0 = nB0 * (math.exp(V1m / VT) - 1)
v.check("Ex 09-07.1h", n0)
v.check("Ex 09-07.1i", 100 * n0 / NB)

# ------------------------------------------------------------------ Example 2
v.check("Ex 09-07.2a", mup(NE))
DE = VT * mup(NE)
v.check("Ex 09-07.2b", DE)


def beta_numeric(DB_, WB_, NB_, DE_, WE_, NE_, dEgE=0.0, dEgB=0.0, tauB=None):
    """Collector current over base current from numerical electron and hole diffusion solutions."""
    fin_b, fout_b = short_flux(DB_, WB_, tauB)
    fin_e, _ = short_flux(DE_, WE_)
    nB0_ = ni2_shift(dEgB) / NB_
    pE0 = ni2_shift(dEgE) / NE_
    Ic = Q * nB0_ * fout_b
    Ib = Q * pE0 * fin_e + Q * nB0_ * (fin_b - fout_b)
    return Ic / Ib


b0 = beta_numeric(DB, WB, NB, DE, WE, NE)
v.check("Ex 09-07.2c", b0)
fHu = ni2_shift(0.095) / ni2_shift(0.0)
v.check("Ex 09-07.2d", fHu)
bHu = beta_numeric(DB, WB, NB, DE, WE, NE, dEgE=0.095)
v.check("Ex 09-07.2e", bHu)
dHB = 3.5e-8 * NE ** (1 / 3)
v.check("Ex 09-07.2f", dHB)
v.check("Ex 09-07.2g", ni2_shift(dHB) / ni2_shift(0.0))
v.check("Ex 09-07.2h", beta_numeric(DB, WB, NB, DE, WE, NE, dEgE=dHB))
v.check("Ex 09-07.2q", bHu / beta_numeric(DB, WB, NB, DE, WE, NE, dEgE=dHB))
v.check("Ex 09-07.2i", ni2_shift(0.1) / ni2_shift(0.0))
v.check("T 09-07.a", ni2_shift(0.1) / ni2_shift(0.0))
v.check("Ex 09-07.2j", beta_numeric(DB, WB, NB, DE, WE, NE, dEgE=0.095, dEgB=0.1))
DB19 = VT * mun(1e19)
v.check("Ex 09-07.2k", DB19)
v.check("Ex 09-07.2l", beta_numeric(DB19, WB, 1e19, DE, WE, NE, dEgE=0.095, dEgB=0.1))
v.check("Ex 09-07.2m", 1 / (Q * mup(1e18) * 1e18 * WB))
v.check("Ex 09-07.2n", 1 / (Q * mup(1e19) * 1e19 * WB))
fin, fout = short_flux(VT * mun(1e16), 2e-4, 1e-6, n=20001)
v.check("Ex 09-07.2o", (fin - fout) / fout)
v.check("Ex 09-07.2p", fout / (fin - fout))
v.check("T 09-07.b", 3.5e-8 * 1e19 ** (1 / 3) * 1e3)
v.check("T 09-07.c", 3.5e-8 * 1e20 ** (1 / 3) * 1e3)
v.check("T 09-07.d", ni2_shift(0.067) / ni2_shift(0.0))


# ------------------------------------------------------------------ Example 3 (Early voltage)
def ic_vs_vcb(VCB, NB_=NB, NC_=NC, WB_at=WB, Vref=2.0):
    """I_C (arbitrary scale) with the neutral base width set by the base-side depletion edge."""
    xp_ref = junction_edges(NB_, NC_, -Vref)[0]
    xp = junction_edges(NB_, NC_, -VCB)[0]
    return 1 / (WB_at + xp_ref - xp)


xp3, xn3, W3, Vbi3 = junction_edges(NB, NC, -2.0)
v.check("Ex 09-07.3a", Vbi3)
v.check("Ex 09-07.3b", W3 * 1e4)
v.check("Ex 09-07.3c", xp3 * 1e7)
v.check("Ex 09-07.3d", xn3 * 1e4)
v.check("Ex 09-07.3j", 100 * xn3 / W3)
h = 1e-4
Cj3 = Q * NB * (junction_edges(NB, NC, -2 - h)[0] - junction_edges(NB, NC, -2 + h)[0]) / (2 * h)
v.check("Ex 09-07.3e", Cj3)
v.check("Ex 09-07.3f", Cj3 * 1e7)
VA3 = ic_vs_vcb(2.0) / ((ic_vs_vcb(2 + h) - ic_vs_vcb(2 - h)) / (2 * h))
v.check("Ex 09-07.3g", VA3)
v.check("Ex 09-07.3h", VA3 / 1e-3 / 1e3)
v.check("Ex 09-07.3i", VA3 / VT)
v.check("T 09-07.e", 50 / VT)

# ------------------------------------------------------------------ Example 4 (Ebers-Moll)
def em(vbe, vbc, Is, bF, bR):
    x, y = math.exp(vbe / VT), math.exp(vbc / VT)
    Ic = Is * (x - 1) - Is * (1 + 1 / bR) * (y - 1)
    Ib = Is / bF * (x - 1) + Is / bR * (y - 1)
    return Ic, Ib


def em_solve(Ic, Ib, Is, bF, bR, guess=(0.9, 0.85)):
    sol = fsolve(lambda z: [em(z[0], z[1], Is, bF, bR)[0] / Ic - 1, em(z[0], z[1], Is, bF, bR)[1] / Ib - 1],
                 guess, xtol=1e-13)
    return sol


v.check("Ex 09-07.4a", 100 / 101)
v.check("Ex 09-07.4b", 2 / 3)
vbe4, vbc4 = em_solve(1e-3, 1e-4, IS, 100, 2)
v.check("Ex 09-07.4c", (vbe4 - vbc4) * 1e3)
v.check("Ex 09-07.4d", vbe4)
v.check("Ex 09-07.4e", vbc4)
v.check("Ex 09-07.4f", math.exp((vbe4 - vbc4) / VT))


# ------------------------------------------------------------------ Example 5 (transit times)
def transit_numeric(W, D, dEg=0.0, n=20001):
    """Integrate the electron profile backward from n(W) = 0 for a unit particle flux with drift
    velocity mu|E| = D eta/W; return the stored charge per unit flux, the transit time."""
    eta = dEg / VT
    x = np.linspace(W, 0, n)
    def rhs(xx, y):
        return [(D * eta / W * y[0] - 1.0) / D]      # flux = mu|E| n - D dn/dx = 1 (normalized)
    sol = solve_ivp(rhs, [W, 0], [0.0], t_eval=x, rtol=1e-11, atol=1e-30)
    nn = sol.y[0][::-1]
    return trapezoid(nn, x[::-1])                     # charge per unit (J/q) = transit time


tB = transit_numeric(WB, DB)
v.check("Ex 09-07.5a", tB * 1e12)
v.check("Ex 09-07.5b", 0.1 / VT)
tBd = transit_numeric(WB, DB, 0.1)
v.check("Ex 09-07.5c", tBd / (WB ** 2 / DB))
v.check("Ex 09-07.5d", tBd * 1e12)
v.check("Ex 09-07.5e", tB / tBd)
v.check("Ex 09-07.5f", 0.1 / WB)
vsat = 1.53e9 * 300 ** -0.87
v.check("Ex 09-07.5g", vsat)
tC = xn3 / (2 * vsat)
v.check("Ex 09-07.5h", tC * 1e12)
CjC = Cj3 * 2 * AE
v.check("Ex 09-07.5i", CjC * 1e15)
CjE = 20e-15
tch = (CjE + CjC) * VT / 1e-3
v.check("Ex 09-07.5j", tch * 1e12)


def ft_numeric(gm, rpi, tauF, Cje, Cjc):
    """Frequency at which |i_c/i_b| = 1 for the hybrid-pi model with C_pi = tauF gm + Cje, C_mu = Cjc
    (output shorted, C_mu's feedforward current neglected)."""
    Cin = tauF * gm + Cje + Cjc
    beta = lambda f: abs(gm / (1 / rpi + 2j * math.pi * f * Cin))
    return brentq(lambda f: beta(f) - 1, 1e6, 1e13, xtol=1e-3)


gm = 1e-3 / VT
tF = tB + tC
v.check("Ex 09-07.5p", tF * 1e12)
v.check("Ex 09-07.5q", (tF + tch) * 1e12)
v.check("Ex 09-07.5r", (tBd + tC + tch) * 1e12)
v.check("Ex 09-07.5k", ft_numeric(gm, 1e9, tF, CjE, CjC) / 1e9)
v.check("Ex 09-07.5l", ft_numeric(gm, 1e9, tBd + tC, CjE, CjC) / 1e9)
JK = Q * NC * vsat
v.check("Ex 09-07.5m", JK)
v.check("Ex 09-07.5n", JK / 1e8 * 1e3)
v.check("Ex 09-07.5o", JK * AE * 1e3)

# ------------------------------------------------------------------ Example 6
gm_num = (IS * math.exp((V1m + 1e-7) / VT) - IS * math.exp((V1m - 1e-7) / VT)) / 2e-7
v.check("Ex 09-07.6a", gm_num * 1e3)
v.check("T 09-07.g", gm_num * 1e3)
v.check("Ex 09-07.6b", 100 / gm_num)
v.check("Ex 09-07.6c", 8.21e-12 * gm_num * 1e15)
v.check("Ex 09-07.6d", (8.21e-12 * gm_num + CjE) * 1e15)
fT6 = ft_numeric(gm, 1e9, tF, CjE, CjC)
v.check("Ex 09-07.6e", math.sqrt(fT6 / (8 * math.pi * 100 * CjC)) / 1e9)
v.check("T 09-07.f", (7e-6) ** 2 / (2 * 10) * 1e12)


# ------------------------------------------------------------------ Example 7 (charge control)
def t_to(Ib, tauF, bF, Ic_target):
    ev = lambda t, q: q[0] / tauF - Ic_target
    ev.terminal = True
    sol = solve_ivp(lambda t, q: [Ib - q[0] / (tauF * bF)], [0, 50 * tauF * bF], [0.0], events=ev,
                    rtol=1e-11, atol=1e-30)
    return sol.t_events[0][0]


v.check("Ex 09-07.7a", 8.21e-12 * 100 * 1e9)
v.check("Ex 09-07.7b", t_to(20e-6, 8.21e-12, 100, 1e-3) * 1e9)
v.check("Ex 09-07.7c", 1e-3 * 8.21e-12 * 1e15)
v.check("Ex 09-07.7d", 20e-6 * 8.21e-12 * 100 * 1e15)

# practitioner (quoted figures)
for k_, val in (("P 09-07.a", 505), ("P 09-07.b", 720), ("P 09-07.c", 300), ("P 09-07.d", 500),
                ("P 09-07.e", 470), ("P 09-07.f", 650)):
    v.check(k_, val)

# ------------------------------------------------------------------ Solutions
for k_, val in (("09-07.1a", 0.75 + 2), ("09-07.1b", 0.75 - 0.6), ("09-07.1c", -0.5 + 3), ("09-07.1d", -1 - 0.7)):
    v.check(k_, val)
D2 = VT * mun(5e18)
v.check("09-07.2a", mun(5e18))
v.check("09-07.2b", D2)
IS2 = Q * 4e-8 * (NI ** 2 / 5e18) * short_flux(D2, 5e-6)[0]
v.check("09-07.2c", IS2)
v.check("09-07.2d", vbe_for(1e-4, IS2))
v.check("09-07.2e", 5e18 * 5e-6 / D2)
v.check("09-07.2f", 5e18 * 5e-6)
v.check("09-07.3a", 150 / 151)
v.check("09-07.3b", 0.995 / 0.005)
v.check("09-07.3c", 2e-3 / 151 * 1e6)
v.check("09-07.3d", 2e-3 * 150 / 151 * 1e3)
# 4
DB4, DE4 = VT * mun(1e17), VT * mup(1e19)
v.check("09-07.4a", DB4)
v.check("09-07.4b", DE4)
v.check("09-07.4c", ni2_shift(0.05) / ni2_shift(0.0))
bE = beta_numeric(DB4, 0.5e-4, 1e17, DE4, 0.3e-4, 1e19, dEgE=0.05)
v.check("09-07.4d", bE)
v.check("09-07.4e", math.sqrt(DB4 * 1e-7) * 1e4)
fin4, fout4 = short_flux(DB4, 0.5e-4, 1e-7, n=20001)
bT = fout4 / (fin4 - fout4)
v.check("09-07.4f", bT)
b4 = beta_numeric(DB4, 0.5e-4, 1e17, DE4, 0.3e-4, 1e19, dEgE=0.05, tauB=1e-7)
v.check("09-07.4g", b4)
v.check("09-07.4h", 1 / (1 + 1 / bE))
v.check("09-07.4i", fout4 / fin4)
v.check("09-07.4j", b4 / (1 + b4))
# 5
b19 = beta_numeric(DB, WB, 1e18, VT * mup(1e19), WB, 1e19, dEgE=0.05)
b20 = beta_numeric(DB, WB, 1e18, VT * mup(1e20), WB, 1e20, dEgE=0.095)
v.check("09-07.5a", b19)
v.check("09-07.5b", b20)
v.check("09-07.5c", b20 / b19)
v.check("09-07.5d", ni2_shift(0.095) / ni2_shift(0.05))
# 6
b6 = 27.0 * (DB19 / DB) * (1e18 / 1e19)
v.check("09-07.6a", b6)
v.check("09-07.6b", brentq(lambda d: b6 * ni2_shift(d) / ni2_shift(0) - 100, 0, 0.5))
# 7
for NCx, kv, kw, kx, kc, ka in ((3e16, "09-07.7a", "09-07.7b", "09-07.7c", "09-07.7d", "09-07.7e"),
                                (1e18, "09-07.7f", "09-07.7g", "09-07.7h", "09-07.7i", "09-07.7j")):
    xp, xn, W, Vbi = junction_edges(NB, NCx, -2.0)
    Cj = Q * NB * (junction_edges(NB, NCx, -2 - h)[0] - junction_edges(NB, NCx, -2 + h)[0]) / (2 * h)
    v.check(kv, Vbi)
    v.check(kw, W * 1e4)
    v.check(kx, xp * 1e7)
    v.check(kc, Cj * 1e7)
    v.check(ka, ic_vs_vcb(2.0, NC_=NCx) / ((ic_vs_vcb(2 + h, NC_=NCx) - ic_vs_vcb(2 - h, NC_=NCx)) / (2 * h)))
x0 = junction_edges(NB, NC, 0.0)[0]
x5 = junction_edges(NB, NC, -5.0)[0]
v.check("09-07.7k", x0 * 1e7)
v.check("09-07.7l", x5 * 1e7)
v.check("09-07.7m", (x5 - x0) * 1e7)
v.check("09-07.7n", ic_vs_vcb(5.0) / ic_vs_vcb(0.0))
v.check("09-07.7o", 1 + 5 / 31.4)
# 8
xpE8, _, _, VbiE8 = junction_edges(2e17, 1e20, 0.7)
v.check("09-07.8a", VbiE8)
v.check("09-07.8b", xpE8 * 1e7)
xpC0, _, _, VbiC8 = junction_edges(2e17, 1e16, 0.0)
v.check("09-07.8c", VbiC8)
v.check("09-07.8d", xpC0 * 1e7)
v.check("09-07.8e", (0.15e-4 - xpE8 - xpC0) * 1e7)
v.check("09-07.8f", brentq(lambda V: xpE8 + junction_edges(2e17, 1e16, -V)[0] - 0.15e-4, 0, 1e4, xtol=1e-9))
v.check("09-07.8g", 54.7)
# 9
for bf, k_ in ((5, "09-07.9a"), (20, "09-07.9b"), (50, "09-07.9c")):
    vb, vc = em_solve(1e-3, 1e-3 / bf, 1e-16, 80, 1, guess=(0.75, 0.7))
    v.check(k_, (vb - vc) * 1e3)
Ic9, Ib9 = em(0.7, 0.6, 1e-16, 80, 1)
Ia9 = 1e-16 * (math.exp(0.7 / VT) - 1)
v.check("09-07.9d", Ic9 * 1e6)
v.check("09-07.9e", Ib9 * 1e6)
v.check("09-07.9f", Ic9 / Ib9)
v.check("09-07.9g", Ia9 * 1e6)
v.check("09-07.9h", 100 * (1 - Ic9 / Ia9))
# 10
Vk = brentq(lambda V: nB0 * math.exp(V / VT) - NB, 0.5, 1.2, xtol=1e-14)
v.check("09-07.10a", Vk)
v.check("09-07.10b", Q * AE * DB * NB / WB * 1e3)
n10 = brentq(lambda n_: n_ * (NB + n_) - NI ** 2 * math.exp(1.0 / VT), 0, 1e21, xtol=1e3)
v.check("09-07.10c", n10)
v.check("09-07.10d", Q * AE * DB * n10 / WB * 1e3)
v.check("09-07.10e", IS * math.exp(1.0 / VT) * 1e3)
# 11
t11 = transit_numeric(30e-7, DB19)
v.check("09-07.11a", t11 * 1e12)
v.check("09-07.11b", 0.15 / VT)
t11d = transit_numeric(30e-7, DB19, 0.15)
v.check("09-07.11c", t11d / ((30e-7) ** 2 / DB19))
v.check("09-07.11d", t11d * 1e12)
v.check("09-07.11e", 0.15 / 30e-7)
tc11 = 0.15e-4 / (2 * vsat)
v.check("09-07.11f", tc11 * 1e12)
v.check("09-07.11g", ft_numeric(1.0, 1e12, t11 + tc11, 0, 0) / 1e9)
v.check("09-07.11h", ft_numeric(1.0, 1e12, t11d + tc11, 0, 0) / 1e9)
# 12
gm12 = 0.2e-3 / VT
v.check("09-07.12a", gm12 * 1e3)
v.check("09-07.12b", 120 / gm12 / 1e3)
v.check("09-07.12c", 40 / 0.2e-3 / 1e3)
v.check("09-07.12d", (2e-12 * gm12 + 5e-15) * 1e15)
v.check("09-07.12e", 40 / VT)
v.check("09-07.12f", ft_numeric(gm12, 1e12, 2e-12, 5e-15, 3e-15) / 1e9)
v.check("09-07.12g", 1 / (2 * math.pi * 2e-12) / 1e9)
v.check("09-07.12h", brentq(lambda I: 8e-15 * VT / I - 2e-12, 1e-6, 1) * 1e3)
# 13
v.check("09-07.13a", brentq(lambda rb: math.sqrt(300e9 / (8 * math.pi * rb * 2e-15)) - 500e9, 1, 1000))
v.check("09-07.13b", math.sqrt(300e9 / (8 * math.pi * 50 * 2e-15)) / 1e9)
v.check("09-07.13c", math.sqrt(300e9 / (8 * math.pi * 25 * 2e-15)) / math.sqrt(300e9 / (8 * math.pi * 100 * 2e-15)))
# 14
NC14 = brentq(lambda N: Q * N * vsat - 3e5, 1e15, 1e19)
v.check("09-07.14a", NC14)
res14 = []
for NCx, kc, ka in ((1e17, "09-07.14b", "09-07.14c"), (NC14, "09-07.14d", "09-07.14e")):
    Cj = Q * NB * (junction_edges(NB, NCx, -1 - h)[0] - junction_edges(NB, NCx, -1 + h)[0]) / (2 * h)
    VA = Q * NB * WB / Cj
    v.check(kc, Cj * 1e7)
    v.check(ka, VA)
    res14.append((Cj, VA))
v.check("09-07.14f", 100 * (NC14 / 1e17 - 1))
v.check("09-07.14g", 100 * (res14[1][0] / res14[0][0] - 1))
v.check("09-07.14h", 100 * (1 - res14[1][1] / res14[0][1]))
# 15
v.check("09-07.15a", 20e-12 * 50 * 1e9)
v.check("09-07.15b", 2e-3 / 50 * 1e6)
IB15 = brentq(lambda Ib: t_to(Ib, 20e-12, 50, 2e-3) - 0.5e-9, 41e-6, 1e-3, xtol=1e-12)
v.check("09-07.15c", 50 * IB15 * 1e3)
v.check("09-07.15d", IB15 * 1e6)
v.check("09-07.15e", 2e-3 * 20e-12 * 1e15)
v.check("09-07.15f", IB15 * 20e-12 * 50 * 1e15)
v.check("09-07.15g", (IB15 * 1e-9 - 2e-3 * 20e-12) * 1e15)
v.check("09-07.15h", IB15 / 40e-6)

# ------------------------------------------------------------------ Lab
TAU0, WEB = 1e-7, 3e-6
IR0 = Q * NI * WEB * AE / (2 * TAU0)


def ic_hi(V):
    n_ = (-NB + math.sqrt(NB ** 2 + 4 * NI ** 2 * math.exp(V / VT))) / 2
    return Q * AE * DB * n_ / WB


def beta_of(V):
    return ic_hi(V) / (IS / bHu * math.exp(V / VT) + IR0 * (math.exp(V / (2 * VT)) - 1))


from scipy.optimize import minimize_scalar  # noqa: E402
pk = minimize_scalar(lambda V: -beta_of(V), bounds=(0.5, 1.0), method="bounded", options={"xatol": 1e-10})
bpk = -pk.fun
v.check("Lab 09-07.a", bpk)
Vhi = brentq(lambda V: beta_of(V) - bpk / 2, pk.x, 1.3, xtol=1e-12)
Vlo = brentq(lambda V: beta_of(V) - bpk / 2, 0.2, pk.x, xtol=1e-12)
v.check("Lab 09-07.b", ic_hi(Vhi) * 1e3)
v.check("Lab 09-07.c", ic_hi(Vlo) * 1e9)
# Early voltage by extrapolating the physical I_C(V_CE) over 1-3 V (V_BE held, I_C at V_CB = 2 V is 1 mA)
vce = np.linspace(1.0, 3.0, 201)
icp = np.array([ic_vs_vcb(vc - V1m) for vc in vce])
icp = icp / ic_vs_vcb(2.0) * 1e-3
slope, icpt = np.polyfit(vce, icp, 1)
v.check("Lab 09-07.d", icpt / slope)
# f_T peak with the illustrative Kirk model (uniform base)
def ft_kirk(I):
    J = I / AE
    push = xn3 * (1 - JK / J) if J > JK else 0.0
    return 1 / (2 * math.pi * ((WB + push) ** 2 / (2 * DB) + (xn3 - push) / (2 * vsat) + (CjE + CjC) * VT / I))


Is_grid = np.sort(np.append(np.geomspace(1e-5, 1e-1, 20001), JK * AE))   # include the Kirk current
fts = np.array([ft_kirk(I) for I in Is_grid])
v.check("Lab 09-07.e", fts.max() / 1e9)
v.check("Lab 09-07.f", Is_grid[int(np.argmax(fts))] * 1e3)

v.finish()
