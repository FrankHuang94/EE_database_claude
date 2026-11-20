#!/usr/bin/env python3
"""Verify every number in chapter 12-07 (output stages and power amplifiers), its solutions and lab.

Independent routes (not the closed forms of the chapter):
- efficiencies and dissipations by averaging the devices' instantaneous currents and powers over a sampled
  cycle; worst-case dissipation by bounded optimization over amplitude;
- crossover distortion by FFT of the dead-band waveform, with the feedback loop solved sample by sample;
- class AB currents by solving the two exponential device equations at the output node;
- thermal runaway loop gain by numerically differentiating the solved bias current with temperature;
- the class B stage with Ebers-Moll transistors (the ngspice model's defaults) solved sample by sample;
- the LC filter's attenuation from its transfer function.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "12-07-output-stages.md", COURSE / "solutions" / "12-07-solutions.md"]
lab = COURSE / "labs" / "12-07-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("12-07", *files)
VT = 0.025852
N = 65536
PH = 2 * math.pi * (np.arange(N) + 0.5) / N
SIN = np.sin(PH)


# ============================================================ cycle-averaged stages
def class_a(Vcc, RL, IQ, Vop):
    vo = Vop * SIN
    i_e = IQ + vo / RL                      # follower's emitter current (must stay positive)
    assert np.all(i_e >= -1e-12)
    PL = float(np.mean(vo ** 2 / RL))
    PS = float(Vcc * np.mean(i_e) + Vcc * IQ)   # follower from +Vcc, current source from -Vcc
    return PL, PS


def class_b(Vcc, RL, Vop):
    vo = Vop * SIN
    i_n, i_p = np.maximum(vo, 0) / RL, np.maximum(-vo, 0) / RL
    PL = float(np.mean(vo ** 2 / RL))
    PS = float(Vcc * np.mean(i_n) + Vcc * np.mean(i_p))
    return PL, PS


def worst_b(Vcc, RL):
    res = minimize_scalar(lambda x: -(lambda r: r[1] - r[0])(class_b(Vcc, RL, x)), bounds=(0.01, Vcc),
                          method="bounded", options={"xatol": 1e-10})
    return res.x, -res.fun


v.check("T 12-07.a", 100 * (lambda r: r[0] / r[1])(class_a(10, 100, 0.1, 10)))
v.check("T 12-07.b", 100 * (lambda r: r[0] / r[1])(class_b(15, 8, 15)))
xw, _ = worst_b(15, 8)
v.check("T 12-07.c", 100 * xw / 15)
v.check("T 12-07.d", 100 * (lambda r: r[0] / r[1])(class_b(15, 8, xw)))

# ============================================================ Example 1: class A
PL1, PS1 = class_a(10, 100, 0.1, 10)
v.check("Ex 12-07.1a", PL1)
v.check("Ex 12-07.1b", PS1)
v.check("Ex 12-07.1c", 100 * PL1 / PS1)
v.check("Ex 12-07.1d", float(np.mean((10 - 0 * SIN) * (0.1 + 0 * SIN))))   # idle: mean of V_CE * i_C with no signal
PLh, PSh = class_a(10, 100, 0.1, 5)
v.check("Ex 12-07.1e", 100 * PLh / PSh)
v.check("Ex 12-07.1f", PLh)

# ============================================================ Example 2: class B
PL2, PS2 = class_b(15, 8, 15)
v.check("Ex 12-07.2a", PL2)
v.check("Ex 12-07.2b", PS2)
v.check("Ex 12-07.2c", 100 * PL2 / PS2)
xw, pdw = worst_b(15, 8)
v.check("Ex 12-07.2d", xw)
v.check("Ex 12-07.2e", pdw)
v.check("Ex 12-07.2f", pdw / 2)
v.check("Ex 12-07.2g", 100 * (lambda r: r[0] / r[1])(class_b(15, 8, xw)))
v.check("Ex 12-07.2h", PS2 - PL2)


# ============================================================ Example 3: crossover distortion
def dead(x, d=0.6):
    return np.where(x > d, x - d, np.where(x < -d, x + d, 0.0))


def thd(y):
    F = np.abs(np.fft.rfft(y)) / N * 2
    return math.sqrt(float(np.sum(F[2:] ** 2))) / F[1]


def in_loop(vin, A=1e4, d=0.6):
    """Solve vo = dead(A (vin - vo)) sample by sample (a monotone scalar equation)."""
    out = np.empty_like(vin)
    for k, x in enumerate(vin):
        if abs(A * x) <= d:
            out[k] = 0.0
        else:
            out[k] = brentq(lambda y: float(dead(np.array([A * (x - y)]), d)[0]) - y, -abs(x) - 1, abs(x) + 1,
                            xtol=1e-15)
    return out


t_open1, t_open10 = thd(dead(1.0 * SIN)), thd(dead(10.0 * SIN))
v.check("Ex 12-07.3a", 100 * t_open1)
v.check("Ex 12-07.3b", 100 * t_open10)
v.check("Ex 12-07.3c", 0.6 / 1e4 * 1e6)
SUB = 8192                                   # the loop solve is per sample; use a coarser grid for it
ph_s = 2 * math.pi * (np.arange(SUB) + 0.5) / SUB


def thd_sub(y):
    F = np.abs(np.fft.rfft(y)) / SUB * 2
    return math.sqrt(float(np.sum(F[2:] ** 2))) / F[1]


t_cl1 = thd_sub(in_loop(1.0 * np.sin(ph_s)))
t_cl10 = thd_sub(in_loop(10.0 * np.sin(ph_s)))
v.check("Ex 12-07.3d", 100 * t_cl1)
v.check("Ex 12-07.3e", 100 * t_cl10)
v.check("Ex 12-07.3f", t_open1 / t_cl1)
# square-wave estimate of crossover THD: harmonic content of a unit square wave (by FFT, not the series sum)
sq = np.sign(SIN)
Fsq = np.abs(np.fft.rfft(sq)) / N * 2
coef = math.sqrt(float(np.sum(Fsq[2:] ** 2)))      # RMS-ratio coefficient: harmonics of a unit square wave
v.check("T 12-07.e", coef)
v.assert_true("square-wave coefficient equals (4/pi) sqrt(pi^2/8 - 1)",
              abs(coef - 4 / math.pi * math.sqrt(math.pi ** 2 / 8 - 1)) < 1e-3)
v.check("T 12-07.f", 100 * coef * 0.6 / 10)
v.check("T 12-07.g", 100 * t_open10)
v.check("T 12-07.l", 100 * coef * 0.6 / 1)
for Vp, ke, kx in ((5.0, "a", "c"), (20.0, "b", "d")):
    v.check(f"12-07.15{ke}", 100 * coef * 0.65 / Vp)
    v.check(f"12-07.15{kx}", 100 * thd(dead(Vp * SIN, 0.65)))
v.check("12-07.15e", 100 * (1 - coef * 0.65 / 5 / thd(dead(5 * SIN, 0.65))))
v.check("12-07.15f", 100 * (1 - coef * 0.65 / 20 / thd(dead(20 * SIN, 0.65))))
v.check("12-07.15g", 0.65 / 5)
v.check("12-07.15h", 0.65 / 20)

# ============================================================ Example 4: class AB bias
IS, IQ = 1e-13, 20e-3
VBB = brentq(lambda vb: IS * math.exp(vb / 2 / VT) - IQ, 0.5, 2.0, xtol=1e-15)


def ab_currents(iL, Vbb=VBB, Is=IS):
    """NPN and PNP currents with v_BEN + v_EBP = Vbb and i_N - i_P = iL."""
    vn = brentq(lambda x: Is * math.exp(x / VT) - Is * math.exp((Vbb - x) / VT) - iL, 0.0, Vbb, xtol=1e-16)
    return Is * math.exp(vn / VT), Is * math.exp((Vbb - vn) / VT)


v.check("Ex 12-07.4a", VBB)
v.check("Ex 12-07.4b", VBB / 0.65 - 1)
iN, iP = ab_currents(0.1)
v.check("Ex 12-07.4c", iN * 1e3)
v.check("Ex 12-07.4d", iP * 1e3)
h = 1e-7                                     # output resistance at idle: dv_out / di_L, numerically
vo = lambda iL: -brentq(lambda x: IS * math.exp(x / VT) - IS * math.exp((VBB - x) / VT) - iL,  # noqa: E731
                        0.0, VBB, xtol=1e-17)
v.check("Ex 12-07.4e", abs((vo(h) - vo(-h)) / (2 * h)))
v.assert_true("translinear product i_N i_P = I_Q^2", abs(iN * iP / IQ ** 2 - 1) < 1e-9)


# ============================================================ Example 5: thermal
def junction_temp(P, thetas, Ta):
    """Steady state of the thermal ladder by nodal analysis: heat P injected at the junction node."""
    n = len(thetas)
    G = np.zeros((n, n))
    for k, th in enumerate(thetas):        # node k to node k+1 (node n is ambient)
        g = 1 / th
        G[k, k] += g
        if k + 1 < n:
            G[k + 1, k + 1] += g
            G[k, k + 1] -= g
            G[k + 1, k] -= g
    b = np.zeros(n)
    b[0] = P
    return Ta + np.linalg.solve(G, b)[0]


Pd = pdw / 2
v.check("Ex 12-07.5a", junction_temp(Pd, [1.5, 0.5, 10.0], 40))
v.check("Ex 12-07.5b", brentq(lambda th: junction_temp(Pd, [th], 40) - 125, 0.1, 100, xtol=1e-12))
tsa = brentq(lambda th: junction_temp(Pd, [1.5, 0.5, th], 40) - 125, 0.1, 100, xtol=1e-12)
v.check("Ex 12-07.5c", tsa)


def thermal_loop(I0, Vce, theta, RE):
    """Loop gain dP/dT * theta, with the bias current solved from a fixed base voltage at each temperature."""
    VB = VT * math.log(I0 / 1e-14) + I0 * RE   # V_BE(I0, T0) + I0 R_E with any I_S

    def current(dT):
        return brentq(lambda i: VT * math.log(i / 1e-14) - 0.002 * dT + i * RE - VB, 1e-6, 100, xtol=1e-15)
    dIdT = (current(1e-3) - current(-1e-3)) / 2e-3
    return dIdT * Vce * theta


v.check("Ex 12-07.5d", (lambda vb: (IS * math.exp((vb + 1e-6) / VT) - IS * math.exp((vb - 1e-6) / VT)) / 2e-6)(
    VT * math.log(0.1 / IS)))                 # g_m as the slope of the exponential at 100 mA
v.check("Ex 12-07.5e", thermal_loop(0.1, 15, 12, 0.0))
v.check("Ex 12-07.5f", thermal_loop(0.1, 15, 12, 0.0) / thermal_loop(0.1, 15, 12, 0.47))
v.check("Ex 12-07.5g", thermal_loop(0.1, 15, 12, 0.47))


def shared_sink(P_each, n, th_jc, th_cs, th_sa, Ta):
    """n devices, each with its own junction-case-sink path, on one heat sink: nodal solution."""
    m = 2 * n + 1                              # junctions, cases, then the sink node
    G = np.zeros((m, m))

    def link(a, b, th):
        G[a, a] += 1 / th
        if b is not None:
            G[b, b] += 1 / th
            G[a, b] -= 1 / th
            G[b, a] -= 1 / th
    for k in range(n):
        link(k, n + k, th_jc)
        link(n + k, 2 * n, th_cs)
    link(2 * n, None, th_sa)
    rhs = np.zeros(m)
    rhs[:n] = P_each
    return Ta + np.linalg.solve(G, rhs)[0]


v.check("Ex 12-07.5h", shared_sink(Pd, 2, 1.5, 0.5, 10.0, 40))
v.check("Ex 12-07.5i", brentq(lambda th: shared_sink(Pd, 2, 1.5, 0.5, th, 40) - 125, 0.1, 100, xtol=1e-12))
v.assert_true("one device on its own sink reproduces Example 5(a)",
              abs(shared_sink(Pd, 1, 1.5, 0.5, 10.0, 40) - junction_temp(Pd, [1.5, 0.5, 10.0], 40)) < 1e-9)

# ============================================================ Example 6: class D against class B
Rdson, Pfix = 0.085, 2.5
Ipk = math.sqrt(2 * 100 / 4)
i_load = Ipk * SIN
Pcond = float(np.mean(i_load ** 2)) * 2 * Rdson
v.check("Ex 12-07.6a", math.sqrt(float(np.mean(i_load ** 2))))
v.check("Ex 12-07.6b", Pcond)
v.check("Ex 12-07.6c", 100 * 100 / (100 + Pcond + Pfix))
Vop6 = brentq(lambda x: class_b(51, 4, x)[0] - 100, 1, 51, xtol=1e-12)
PL6, PS6 = class_b(51, 4, Vop6)
v.check("Ex 12-07.6d", Vop6)
v.check("Ex 12-07.6e", 100 * PL6 / PS6)
v.check("Ex 12-07.6f", PS6 - PL6)
Lf, Cf = 10e-6, 1e-6
f0 = brentq(lambda f: (2 * math.pi * f) ** 2 * Lf * Cf - 1, 1e3, 1e6, xtol=1e-9)   # where |1 - w^2 LC| = 0
v.check("Ex 12-07.6g", f0 / 1e3)
v.check("Ex 12-07.6h", 40 * math.log10(450e3 / f0))
H450 = abs(1 / (1 - (2 * math.pi * 450e3) ** 2 * Lf * Cf))
v.assert_true("unloaded LC attenuation at 450 kHz within 0.2 dB of the 40 dB/decade estimate",
              abs(-20 * math.log10(H450) - 40 * math.log10(450e3 / f0)) < 0.2)

# ============================================================ simulation: Ebers-Moll class B stage (ngspice defaults)
k_B, q_e = 1.380649e-23, 1.602176634e-19
VT27 = k_B * 300.15 / q_e                    # ngspice's default temperature, 27 C
ISB, BF, RLs, VCCs = 1e-13, 100.0, 8.0, 15.0


def em_out(vin):
    f = lambda vo: (ISB * math.expm1((vin - vo) / VT27) - ISB * math.expm1((vo - vin) / VT27)) * (1 + 1 / BF) - vo / RLs  # noqa: E731,E501
    return brentq(f, vin - 1.5, vin + 1.5, xtol=1e-14)


M = 20000
vin_s = 10 * np.sin(2 * math.pi * (np.arange(M) + 0.5) / M)
vo_s = np.array([em_out(x) for x in vin_s])
icn = ISB * np.expm1((vin_s - vo_s) / VT27)
icp = ISB * np.expm1((vo_s - vin_s) / VT27)
PLs = float(np.mean(vo_s ** 2 / RLs))
PSs = float(VCCs * np.mean(icn) + VCCs * np.mean(icp))
PLi, PSi = class_b(15, 8, 10)
v.check("Sim 12-07.a", PLi)
v.check("Sim 12-07.b", 100 * PLi / PSi)
v.check("Sim 12-07.c", PLs)
v.check("Sim 12-07.d", 100 * PLs / PSs)
kpk = int(np.argmax(vo_s))
v.check("Sim 12-07.e", vin_s[kpk] - vo_s[kpk])
v.check("Sim 12-07.f", vo_s[kpk] / RLs)
v.check("Sim 12-07.g", vo_s[kpk])
PLr, PSr = class_b(15, 8, vo_s[kpk])               # ideal class B at the simulated peak
v.check("Sim 12-07.h", 100 * PLr / PSr)


def em_eta(beta_f):
    """The same Ebers-Moll stage with a different forward beta: efficiency in percent."""
    def out(vin):
        f = lambda vo: (ISB * math.expm1((vin - vo) / VT27) - ISB * math.expm1((vo - vin) / VT27)) * (  # noqa: E731
            1 + 1 / beta_f) - vo / RLs
        return brentq(f, vin - 1.5, vin + 1.5, xtol=1e-14)
    vo_b = np.array([out(x) for x in vin_s])
    icn_b = ISB * np.expm1((vin_s - vo_b) / VT27)
    icp_b = ISB * np.expm1((vo_b - vin_s) / VT27)
    return 100 * float(np.mean(vo_b ** 2 / RLs)) / float(VCCs * (np.mean(icn_b) + np.mean(icp_b)))


eta_inf = em_eta(1e12)
v.check("Sim 12-07.i", eta_inf)
v.assert_true("simulated efficiency exceeds the reduced-swing ideal, and beta accounts for most of it",
              100 * PLs / PSs > eta_inf > 100 * PLr / PSr)

# ============================================================ drive and protection (section 3.5)
Ipk2 = 15.0 / 8.0
v.check("T 12-07.h", Ipk2 / 100 * 1e3)
v.check("T 12-07.i", Ipk2 / (100 * 100) * 1e3)
Ilim = brentq(lambda i: i * 0.33 - 0.6, 0.0, 10.0, xtol=1e-15)       # Q_L turns on at 0.6 V across R_E
v.check("T 12-07.j", Ilim)
v.check("T 12-07.k", 15.0 * Ilim)
# problems 13-14
Vp13 = brentq(lambda x: class_b(1, 4, x)[0] - 20, 1, 30, xtol=1e-13)  # sine power into 4 ohm
v.check("12-07.13a", Vp13)
v.check("12-07.13b", Vp13 / 4)
v.check("12-07.13c", Vp13 / 4 / 50 * 1e3)
v.check("12-07.13d", Vp13 / 4 / (50 * 50) * 1e3)
Il14 = brentq(lambda i: i * 0.25 - 0.65, 0.0, 10.0, xtol=1e-15)
v.check("12-07.14a", Il14)
v.check("12-07.14b", 24 * Il14)

# ============================================================ practitioner arithmetic (TPA3255, R-191)
v.check("Prac 12-07.a", class_b(1, 4, 51 * 4 / (4 + 2 * 0.085))[0])   # BTL: the load sees a ±V_DD swing
v.check("Prac 12-07.b", class_b(1, 4, 51)[0])
v.assert_true("BTL sine power is (V_DD)^2/(2 R_L) per the sampled average",
              abs(class_b(1, 4, 51)[0] - 51 ** 2 / 8) < 1e-9)

# ============================================================ solutions
PLa, PSa = class_a(10, 100, 0.1, 5)
v.check("12-07.1a", 100 * PLa / PSa)
PL, PS = class_b(12, 4, 12)
v.check("12-07.2a", PL)
v.check("12-07.2b", PS)
v.check("12-07.2c", 100 * PL / PS)
xw3, pd3 = worst_b(20, 8)
v.check("12-07.3a", xw3)
v.check("12-07.3b", pd3)
v.check("12-07.3c", pd3 / 2)
IQ4 = brentq(lambda i: np.min(i + (-5 * SIN) / 50) - 0, 1e-4, 1, xtol=1e-14)   # emitter current must not go negative
PL4, PS4 = class_a(5, 50, IQ4, 5)
v.check("12-07.4a", IQ4 * 1e3)
v.check("12-07.4b", PS4)
v.check("12-07.4c", PL4)
Pm = class_b(15, 8, 15)[0]
V5 = brentq(lambda x: class_b(15, 8, x)[0] - Pm / 3, 1, 15, xtol=1e-12)
v.check("12-07.5a", 100 * (lambda r: r[0] / r[1])(class_b(15, 8, V5)))
v.check("12-07.6a", 0.7 / 1e5 * 1e6)
iN7, iP7 = ab_currents(0.2, Vbb=2 * VT * math.log(10e-3 / IS))
v.check("12-07.7a", iN7 * 1e3)
v.check("12-07.7b", iP7 * 1e3)
v.check("12-07.7c", VT / (2 * 10e-3))
v.assert_true("problem 7 idle resistance equals the numerical slope",
              abs(abs((lambda f: (f(1e-7) - f(-1e-7)) / 2e-7)(
                  lambda iL: brentq(lambda x: IS * math.exp(x / VT) - IS * math.exp((2 * VT * math.log(10e-3 / IS) - x) / VT) - iL,  # noqa: E501
                                    0.0, 2.0, xtol=1e-17))) / (VT / 2e-2) - 1) < 1e-4)
R2 = 0.6 / 1e-3
R1 = brentq(lambda r: 0.6 * (1 + r / R2) - 1.25, 1, 1e4, xtol=1e-12)
v.check("12-07.8a", R2)
v.check("12-07.8b", R1)
v.check("12-07.8c", -2 * (1 + R1 / R2))
v.check("12-07.8d", R1 / R2)
th9 = brentq(lambda th: junction_temp(20, [1.0, 0.3, th], 50) - 150, 0.01, 100, xtol=1e-12)
v.check("12-07.9a", th9)
v.check("12-07.10a", 0.2 / VT)
v.check("12-07.10b", thermal_loop(0.2, 20, 8, 0.0))
v.check("12-07.10c", brentq(lambda r: thermal_loop(0.2, 20, 8, r) - 0.5, 0.01, 10, xtol=1e-12))
for P, ids in ((50.0, ("12-07.11a", "12-07.11b", "12-07.11c")), (1.0, (None, "12-07.11d", "12-07.11e"))):
    il = math.sqrt(2 * P / 8) * SIN
    pc = float(np.mean(il ** 2)) * 0.2
    if ids[0]:
        v.check(ids[0], math.sqrt(float(np.mean(il ** 2))))
    v.check(ids[1], pc)
    v.check(ids[2], 100 * P / (P + pc + 1.5 + 1.0))
Pm12 = class_b(15, 8, 15)[0]
V12 = brentq(lambda x: 10 * math.log10(Pm12 / class_b(15, 8, x)[0]) - 10, 0.5, 15, xtol=1e-12)
PL12, PS12 = class_b(15, 8, V12)
v.check("12-07.12a", Pm12)
v.check("12-07.12b", PL12)
v.check("12-07.12c", 100 * PL12 / PS12)
v.check("12-07.12d", PS12 - PL12)

# ============================================================ lab README (the ngspice stage)
if lab.exists():
    v.check("Lab 12-07.a", PLs)
    v.check("Lab 12-07.b", PSs)
    v.check("Lab 12-07.c", 100 * PLs / PSs)
    v.check("Lab 12-07.d", 100 * PLr / PSr)
    v.check("Lab 12-07.e", eta_inf)

sys.exit(v.finish())
