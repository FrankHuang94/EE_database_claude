#!/usr/bin/env python3
"""Verify every number in chapter 09-11 (CMOS and scaling), its solutions and lab.

Independent routes:
- the inverter transfer curve by solving NMOS/PMOS current balance at each input, V_M by root finding on
  V_out(V_in) - V_in, and the noise-margin points by root finding on a numerical derivative of the curve;
- delays by integrating C dV/dt = -I_on to the half-supply crossing, and the ring period by an
  event-by-event simulation of transitions around the ring;
- switching energy by integrating the supply power and the resistor power over an RC charge;
- growth rates and doubling times by root finding;
- scaling factors from a device model (velocity-saturated current, gate capacitance, CV/I delay) evaluated
  before and after scaling, not from the exponent table;
- depletion widths from phi_B found by root finding on the carrier statistics;
- the minimum-energy supply by numerical minimization;
- lab statistics from the data files with a hand-written median.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants as C
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
LAB = COURSE / "labs" / "09-11-lab"
v = Verifier.from_files("09-11", COURSE / "chapters" / "09-11-cmos-and-scaling.md",
                        COURSE / "solutions" / "09-11-solutions.md", LAB / "README.md")

Q = C.e
VT = C.k * 300 / C.e
NI = 1.0e10
EPS = 11.7 * C.epsilon_0 / 100
EOX = 3.9 * C.epsilon_0 / 100


# ------------------------------------------------------------------ inverter
def i_sq(vgs, vds, k, vt):
    vov = vgs - vt
    if vov <= 0:
        return 0.0
    return k * (vov * vds - vds ** 2 / 2) if vds < vov else k * vov ** 2 / 2


def vout(vin, r, vdd=1.0, vtn=0.3, vtp=0.3):
    if vin <= vtn:
        return vdd
    if vin >= vdd - vtp:
        return 0.0
    return brentq(lambda vo: r * i_sq(vin, vo, 1, vtn) - i_sq(vdd - vin, vdd - vo, 1, vtp), 0, vdd, xtol=1e-15)


def vm(r, vdd=1.0, vtn=0.3, vtp=0.3):
    return brentq(lambda x: vout(x, r, vdd, vtn, vtp) - x, vtn + 1e-9, vdd - vtp - 1e-9, xtol=1e-15)


v.check("Ex 09-11.1a", vm(2.0))
v.check("Ex 09-11.1b", brentq(lambda wr: vm(2.0 / wr) - 0.5, 0.5, 8))  # k_n/k_p = (mu ratio)/(W_p/W_n)
v.check("Lab 09-11.a", vm(1.0))
h = 1e-6
slope = lambda x: (vout(x + h, 1.0) - vout(x - h, 1.0)) / (2 * h)
vil = brentq(lambda x: slope(x) + 1, 0.31, 0.49, xtol=1e-12)
vih = brentq(lambda x: slope(x) + 1, 0.51, 0.69, xtol=1e-12)
v.check("Ex 09-11.1c", vil)
v.check("Ex 09-11.1d", vih)
v.check("Ex 09-11.1e", vil - 0.0)
v.check("Ex 09-11.1f", 1.0 - vih)


# ------------------------------------------------------------------ delay
def t_half(Cl, V, I):
    """Integrate C dV/dt = -I (constant-current discharge) from V to V/2."""
    ev = lambda t, y: y[0] - V / 2
    ev.terminal = True
    sol = solve_ivp(lambda t, y: [-I / Cl], (0, 1), [V], events=ev, rtol=1e-12, atol=1e-15, max_step=1e-12)
    return sol.t_events[0][0]


tHL = t_half(1e-15, 0.75, 100e-6)
tLH = t_half(1e-15, 0.75, 80e-6)
v.check("Ex 09-11.2a", tHL * 1e12)
v.check("Ex 09-11.2b", tLH * 1e12)
v.check("Ex 09-11.2c", (tHL + tLH) / 2 * 1e12)


def ring_period(N, tf, tr):
    """Follow one transition around an odd ring; node 0 completes a cycle every two passes."""
    t, falling, back = 0.0, True, []
    for k in range(6 * N):
        t += tf if falling else tr
        falling = not falling
        if (k + 1) % N == 0:
            back.append(t)
    return back[2] - back[0]


T101 = ring_period(101, tHL, tLH)
v.check("Ex 09-11.2d", T101 * 1e12)
v.check("Ex 09-11.2e", 1 / T101 / 1e9)

# ------------------------------------------------------------------ energy (RC charge from a supply)
R, Cl, V = 1e3, 1e-15, 0.75
tau = R * Cl
i_t = lambda t: V / R * math.exp(-t / tau)
E_supply = quad(lambda t: V * i_t(t), 0, 60 * tau, epsabs=0, epsrel=1e-12)[0]
E_res = quad(lambda t: i_t(t) ** 2 * R, 0, 60 * tau, epsabs=0, epsrel=1e-12)[0]
v.check("Ex 09-11.3a", E_supply * 1e15)
v.assert_true("half the supply energy is dissipated in the resistor while charging", abs(E_res / E_supply - 0.5) < 1e-9)
Pdyn = 0.1 * 1e8 * E_supply * 3e9
Pst = 4e8 * 10e-9 * 0.75
v.check("Ex 09-11.3b", Pdyn)
v.check("Ex 09-11.3c", Pst)
v.check("Ex 09-11.3d", Pdyn + Pst)
v.check("Ex 09-11.3e", 100 * Pst / (Pdyn + Pst))

# ------------------------------------------------------------------ Moore
n65 = brentq(lambda n: 2 ** n - 65000, 1, 30)
v.assert_true("65,000 is about 16 doublings", round(n65) == 16)
v.check("Ex 09-11.4a", 2 ** round(n65))
for T2, k_ in ((1.0, "b"), (1.5, "c"), (2.0, "d")):
    v.check(f"Ex 09-11.4{k_}", 100 * brentq(lambda g: (1 + g) ** T2 - 2, 0, 2))
v.check("Ex 09-11.4e", 2 ** (50 / 2))
v.check("Ex 09-11.4f", 640 / 32)
v.check("Ex 09-11.4h", 640 * 100)
v.check("Ex 09-11.4i", math.log2(640 / 32))
v.check("Ex 09-11.4j", math.log2(100))
v.check("Ex 09-11.4k", math.log2(32) + math.log2(20) + math.log2(100))
v.check("Ex 09-11.4g", 0.7 * 0.7)


# ------------------------------------------------------------------ scaling from a device model
def device(L, W, tox, V, vt, mu=200.0, vsat=8e6, m=1.2):
    """Velocity-saturated device (09-10): returns current, gate capacitance, delay, area."""
    cox = EOX / tox
    es = 2 * vsat / mu
    vov = V - vt
    vd = 1 / (m / vov + 1 / (es * L))
    I = W * cox * vsat * (vov - m * vd)
    Cg = cox * W * L
    return I, Cg, Cg * V / I, W * L


def metrics(L, W, tox, V, vt, freq_from_delay=True, f0=None):
    I, Cg, d, A = device(L, W, tox, V, vt)
    f = 1 / d if freq_from_delay else f0
    P = Cg * V ** 2 * f
    return dict(delay=d, density=1 / A, P=P, Pd=P / A, E=Cg * V ** 2)


k = 1 / 0.7
base = (100e-7, 200e-7, 2e-7, 1.0, 0.3)
b = metrics(*base)
cf = metrics(base[0] / k, base[1] / k, base[2] / k, base[3] / k, base[4] / k)
v.check("Ex 09-11.5a", cf["delay"] / b["delay"])
v.check("Ex 09-11.5b", cf["density"] / b["density"])
v.check("Ex 09-11.5c", cf["P"] / b["P"])
v.check("Ex 09-11.5d", cf["Pd"] / b["Pd"])
v.check("Ex 09-11.5e", cf["E"] / b["E"])
# constant voltage: the velocity-saturated current is not exactly scale-invariant (V_Dsat term), so evaluate
# the fully saturated limit, in which current depends on W C_ox V only
Ivs = lambda L, W, tox, V: W * (EOX / tox) * 8e6 * V
def cv_metrics(L, W, tox, V, f=None):
    I = Ivs(L, W, tox, V)
    Cg = EOX / tox * W * L
    d = Cg * V / I
    fr = 1 / d if f is None else f
    return Cg * V ** 2 * fr / (W * L)
p0 = cv_metrics(100e-7, 200e-7, 2e-7, 1.0)
p1 = cv_metrics(100e-7 / k, 200e-7 / k, 2e-7 / k, 1.0)
v.check("Ex 09-11.5f", p1 / p0)
p4 = cv_metrics(100e-7 / k ** 4, 200e-7 / k ** 4, 2e-7 / k ** 4, 1.0)
v.check("Ex 09-11.5g", p4 / p0)
v.check("Ex 09-11.5i", 25 * p4 / p0)
f0 = 1e9
v.check("Ex 09-11.5h", cv_metrics(100e-7 / k, 200e-7 / k, 2e-7 / k, 1.0, f0) / cv_metrics(100e-7, 200e-7, 2e-7, 1.0, f0))

vt6 = 0.45 * 0.7 ** 3
v.check("Ex 09-11.6a", vt6)
ioff = lambda vt, S: 10 ** (-vt / S)
v.check("Ex 09-11.6b", ioff(vt6, 0.085) / ioff(0.45, 0.085))

v.check("Ex 09-11.7a", 48 * 160)
v.check("Ex 09-11.7b", 48 * 120)
v.check("Ex 09-11.7c", 50 * 160)
v.check("Ex 09-11.7d", 50 * 180)
v.check("Ex 09-11.7e", (48 * 160) / (48 * 120))
v.check("Ex 09-11.7f", (3 / 2) ** 2)

# practitioner and textbook facts (quoted; see R-172)
for k_, val in (("P 09-11.a", 65000), ("P 09-11.b", 2004), ("P 09-11.c", 115), ("P 09-11.d", 100), ("P 09-11.e", 5),
                ("P 09-11.f", 50), ("P 09-11.g", 15), ("P 09-11.h", 30), ("P 09-11.i", 37), ("P 09-11.j", 13),
                ("P 09-11.k", 1.2), ("P 09-11.l", 0.9), ("P 09-11.m", 30), ("P 09-11.n", 32), ("P 09-11.o", 640),
                ("P 09-11.p", 100), ("P 09-11.q", 2.5), ("P 09-11.r", 1.8), ("P 09-11.s", 1.3), ("P 09-11.t", 0.9),
                ("P 09-11.u", 0.45)):
    v.check(k_, val)

# ------------------------------------------------------------------ solutions
v.check("09-11.1a", vm(4.0))
r45 = brentq(lambda r: vm(r) - 0.45, 1.01, 10)
v.check("09-11.1b", r45)
v.check("09-11.1c", (0.5 - vm(4.0)) * 1e3)

v.check("09-11.2a", (0.7 * 0.75 / 0.95) / (1.0 * 0.80 / 1.0))

td3 = brentq(lambda td: 1 / ring_period(51, td, td) - 2.5e9, 1e-13, 1e-10, xtol=1e-20)
v.check("09-11.3a", td3 * 1e12)
v.check("09-11.3b", brentq(lambda I: t_half(0.8e-15, 0.7, I) - td3, 1e-6, 1e-3, xtol=1e-12) * 1e6)

fmax = lambda Vd, vt=0.3: (Vd - vt) / Vd           # I_on/(C V_DD) up to a constant
f08 = 3e9 * fmax(0.8) / fmax(1.0)
v.check("09-11.4a", f08 / 1e9)
v.check("09-11.4b", 10 * (0.8 / 1.0) ** 2 * f08 / 3e9)
v.check("09-11.4c", (0.8 / 1.0) ** 2)

fV = lambda Vd: 2e9 * fmax(Vd) / fmax(1.0)
E = lambda Vd: 100e-12 * Vd ** 2 + Vd * 0.1 / fV(Vd)
v.check("09-11.5a", E(1.0))
opt = minimize_scalar(E, bounds=(0.32, 1.2), method="bounded", options={"xatol": 1e-12})
v.assert_true("energy optimum is interior and a true minimum", 0.33 < opt.x < 1.1 and E(opt.x - 1e-3) > opt.fun < E(opt.x + 1e-3))
v.check("09-11.5b", opt.x)
v.check("09-11.5c", opt.fun)
v.check("09-11.5d", fV(opt.x) / 1e9)
v.check("09-11.5e", E(1.0) / opt.fun)

T2 = brentq(lambda T: 1e8 * 2 ** (20 / T) - 5e10, 0.5, 10)
v.check("09-11.6a", T2)
v.check("09-11.6b", 100 * (2 ** (1 / T2) - 1))
v.check("09-11.6c", 2 ** (10 / 2))


def wdmax(N):
    pB = brentq(lambda p: NI * math.exp(p / VT) - N, 0, 1.2)
    return pB, math.sqrt(2 * EPS * 2 * pB / (Q * N))


pa, wa = wdmax(1e16)
pb, wb = wdmax(5e16)
v.check("09-11.7a", pa)
v.check("09-11.7b", wa * 1e4)
v.check("09-11.7c", pb)
v.check("09-11.7d", wb * 1e4)
v.check("09-11.7e", wb / wa)
N7 = brentq(lambda N: wdmax(N)[1] - wa / 5, 1e16, 1e19, rtol=1e-12)
v.check("09-11.7f", N7)
v.check("09-11.7g", N7 / 1e16)

# generalized scaling from the device model: dimensions / kappa, voltage / u, frequency = 1/delay
def gen_pd(kappa, u, n):
    return cv_metrics(100e-7 / kappa ** n, 200e-7 / kappa ** n, 2e-7 / kappa ** n, 1.0 / u ** n) / p0


v.check("09-11.8a", gen_pd(k, 1 / 0.9, 1))
v.check("09-11.8b", gen_pd(k, 1 / 0.9, 3))
v.check("09-11.8c", gen_pd(k, 1.0, 3))

P9 = lambda V, f: 1e9 * 0.15 * 0.5e-15 * V ** 2 * f
v.check("09-11.9a", P9(0.7, 3e9))
v.check("09-11.9b", 60 / P9(0.7, 3e9))
v.check("09-11.9c", P9(0.6, 2.4e9))
v.check("09-11.9d", 60 / P9(0.6, 2.4e9))

ch10 = 120 * 20 / 22
v.check("09-11.10a", ch10)
v.check("09-11.10b", 46 * ch10)
v.check("09-11.10c", 48 * 120 / (46 * ch10))
v.check("09-11.10d", 48 * 160 / (46 * ch10))

v.check("09-11.11a", ioff(0.30 - 0.03, 0.080) / ioff(0.30, 0.080))
v.check("09-11.11b", 2 * ioff(0.27, 0.080) / ioff(0.30, 0.080) * 0.95)

COX2 = EOX / 2e-7


def shoot_isat(vov, mu, vsat, L=50e-7, m=1.2, W=1e-4):
    """Saturation current by shooting along the channel to the E_sat point (as in verify_09_10)."""
    es = 2 * vsat / mu
    kk = W * COX2 * mu

    def length(I):
        vs = (vov - 2 * I / (kk * es)) / m
        return quad(lambda V: (kk * (vov - m * V) - I / es) / I, 0, vs, epsabs=0, epsrel=1e-12)[0]

    imax = kk * es * vov / 2
    return brentq(lambda I: length(I) - L, imax * 1e-9, imax * (1 - 1e-12), xtol=1e-18, rtol=1e-14)


In12, Ip12 = shoot_isat(0.55, 183, 8e6), shoot_isat(0.55, 61, 6e6)
v.check("09-11.12a", In12 * 1e3)
v.check("09-11.12b", Ip12 * 1e3)
v.check("09-11.12c", In12 / Ip12)
In12m, Ip12m = shoot_isat(0.15, 183, 8e6), shoot_isat(0.15, 61, 6e6)
v.check("09-11.12d", In12m * 1e6)
v.check("09-11.12e", Ip12m * 1e6)
v.check("09-11.12f", In12m / Ip12m)

# ------------------------------------------------------------------ lab
v.check("Lab 09-11.b", gen_pd(k, 1.0, 5))
f = np.loadtxt(LAB / "data" / "rupp_frequency_mhz.dat", comments="#")
w = np.loadtxt(LAB / "data" / "rupp_power_w.dat", comments="#")


def median(a, lo, hi):
    s = sorted(a[(a[:, 0] >= lo) & (a[:, 0] < hi), 1])
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


v.check("Lab 09-11.c", median(f, 2000, 2005))
v.check("Lab 09-11.d", median(f, 2005, 2010))
v.check("Lab 09-11.e", median(f, 2010, 2015))
v.check("Lab 09-11.f", max(f[:, 1]))
v.check("Lab 09-11.g", median(w, 2000, 2005))
v.check("Lab 09-11.h", median(w, 2015, 2022))

v.finish()
