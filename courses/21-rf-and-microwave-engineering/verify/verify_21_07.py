#!/usr/bin/env python3
"""Verify every number in chapter 21-07 (power amplifiers), its problems and its lab.

Independent routes (the lab module pa.py uses the closed forms):
- conduction-angle currents are Fourier integrals of the truncated cosine evaluated with scipy.quad;
- class E is solved from its four defining conditions (zero voltage and zero slope at turn-on, average voltage
  equal to V_DD, lossless power balance) with scipy.optimize.fsolve, and the reactance from a numerical projection;
- class F3 finds the largest fundamental for which the sampled waveform stays non-negative;
- average efficiencies integrate over the Rayleigh envelope density instead of the exponential power density;
- the Doherty is solved as a phasor circuit (two current sources, a quarter-wave line as an ABCD matrix, a load);
- ACLR of the cubic model is checked against a simulated OFDM signal (assert), and the seeded DPD results are
  recomputed with the lab's routines (they are simulation outputs, published to 0.1 dB);
- ngspice confirms class E and the Doherty (classe.cir, doherty.cir).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "21-07-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import pa as lab  # noqa: E402

_files = [ROOT / "chapters" / "21-07-power-amplifiers.md", ROOT / "solutions" / "21-07-solutions.md",
          LAB / "README.md"]
v = Verifier.from_files("21-07", *[p for p in _files if p.exists()])
lg = math.log10
db10 = lambda x: 10 * lg(x)  # noqa: E731
db20 = lambda x: 20 * lg(x)  # noqa: E731


# ---------------------------------------------------------------- helpers
def fourier_trunc(alpha_deg):
    """DC and fundamental of the truncated cosine (peak 1) by numerical integration."""
    a = math.radians(alpha_deg)
    c = math.cos(a / 2)
    i = lambda th: max(0.0, (math.cos(th) - c) / (1 - c)) if abs(th) <= a / 2 else 0.0  # noqa: E731
    idc = integrate.quad(i, -math.pi, math.pi, points=[-a / 2, a / 2], limit=200)[0] / (2 * math.pi)
    i1 = integrate.quad(lambda th: i(th) * math.cos(th), -math.pi, math.pi, points=[-a / 2, a / 2],
                        limit=200)[0] / math.pi
    return idc, i1


def class_e_solve():
    """Unknowns I_DC, I_m, phi, wC for V_DD = 1, R = 1."""
    def eqs(p):
        idc, im, phi, wc = p
        v2pi = (idc * math.pi + im * (math.cos(2 * math.pi + phi) - math.cos(math.pi + phi))) / wc
        dv2pi = (idc - im * math.sin(2 * math.pi + phi)) / wc
        mean_v = integrate.quad(lambda th: (idc * (th - math.pi) + im * (math.cos(th + phi) - math.cos(math.pi + phi))) / wc,
                                math.pi, 2 * math.pi)[0] / (2 * math.pi)
        return [v2pi, dv2pi, mean_v - 1.0, im * im / 2 - idc]
    idc, im, phi, wc = optimize.fsolve(eqs, [0.6, 1.1, 2.5, 0.2], xtol=1e-13)
    th = np.linspace(math.pi, 2 * math.pi, 200001)
    vv = (idc * (th - math.pi) + im * (np.cos(th + phi) - np.cos(math.pi + phi))) / wc
    # quadrature projection over the full cycle (v = 0 while the switch is closed)
    q = integrate.quad(lambda t: (idc * (t - math.pi) + im * (math.cos(t + phi) - math.cos(math.pi + phi))) / wc
                       * math.cos(t + phi), math.pi, 2 * math.pi)[0] / math.pi
    return {"P": idc, "wCR": wc, "X_R": q / im, "Im": im / idc, "vpk": vv.max(), "ipk": (idc + im) / idc}


def rayleigh_avg(eta_fun, papr_db):
    """Average efficiency with a Rayleigh envelope r (E r^2 = 1) normalized to x = r / r_peak, clipped at 1."""
    rpk = math.sqrt(10 ** (papr_db / 10))
    pdf = lambda r: 2 * r * math.exp(-r * r)  # noqa: E731
    xo = lambda r: min(1.0, r / rpk)  # noqa: E731
    num = integrate.quad(lambda r: xo(r) ** 2 * pdf(r), 0, 12, points=[rpk], limit=300)[0]
    den = integrate.quad(lambda r: xo(r) ** 2 / eta_fun(xo(r)) * pdf(r) if r > 0 else 0.0, 0, 12, points=[rpk],
                         limit=300)[0]
    return num / den


def doherty_phasor(x, vdd=28.0, ropt=25.0, gamma=1.0):
    """Phasor solution: main current I_m = x I_max into a quarter-wave line (Z0 = R_opt), auxiliary current
    gamma (x(1+gamma) - 1)/gamma ... scaled to reach gamma I_max at x = 1 and starting at x = 1/(1+gamma),
    lagging 90 degrees, into the load R_opt/(1+gamma). Returns (|V_main|, P_out, P_DC, eta)."""
    imax = vdd / ropt
    rl = ropt / (1 + gamma)
    x0 = 1 / (1 + gamma)
    im = x * imax
    ia = max(0.0, (x - x0) / (1 - x0)) * gamma * imax
    z0 = ropt
    # line ABCD (lossless quarter wave): V1 = j Z0 I2, I1 = j V2 / Z0; load node: V2 = rl (I2 + I_aux)
    # unknowns V1, I1 (= im), V2, I2: from I1 = j V2 / Z0 -> V2 = -j Z0 im
    v2 = -1j * z0 * im
    i_aux = -1j * ia                                   # 90 degrees behind the main
    i2 = v2 / rl - i_aux
    v1 = 1j * z0 * i2
    pout = abs(v2) ** 2 / (2 * rl)
    pdc = vdd * (2 / math.pi) * (im + ia)
    return abs(v1), pout, pdc, pout / pdc


# ================================================================ Example 21-07.1
R1 = (3.4 - 0.4) ** 2 / (2 * 1.0)
v.check("Ex 21-07.1a", R1)
v.check("Ex 21-07.1b", 50 / R1)
v.check("Ex 21-07.1c", math.sqrt(50 / R1 - 1))
I1 = 3.0 / R1
idc_b, i1_b = fourier_trunc(180)
IDC = I1 * idc_b / i1_b
v.check("Ex 21-07.1d", I1)
v.check("Ex 21-07.1e", IDC)
PDC = 3.4 * IDC
v.check("Ex 21-07.1f", PDC)
v.check("Ex 21-07.1g", 1 / PDC * 100)
PIN = 10 ** ((30 - 15) / 10) * 1e-3
v.check("Ex 21-07.1h", PIN * 1e3)
v.check("Ex 21-07.1i", (1 - PIN) / PDC * 100)
v.check("Ex 21-07.1j", PDC + PIN - 1)
v.check("Ex 21-07.1k", (48 - 5) ** 2 / (2 * 40))

# ================================================================ Example 21-07.2
ref = fourier_trunc(360)[1]
for key, a in zip("abcd", (360, 240, 180, 120)):
    idc, i1 = fourier_trunc(a)
    v.check(f"Ex 21-07.2{key}", 0.5 * i1 / idc * 100)
for key, a in zip("efgh", (360, 240, 180, 120)):
    v.check(f"Ex 21-07.2{key}", db20(fourier_trunc(a)[1] / ref))
v.check("Ex 21-07.2i", 1 / fourier_trunc(240)[1])
v.check("Ex 21-07.2j", 1 / fourier_trunc(120)[1])

# ================================================================ Example 21-07.3
CE = class_e_solve()
v.assert_true("class-E solve agrees with pa.class_e", abs(CE["P"] - lab.class_e()["PR_V2"]) < 1e-9)
W = 2 * math.pi * 2e9
R3 = CE["P"] * 3.3 ** 2 / 1.0
v.check("Ex 21-07.3a", R3)
v.check("Ex 21-07.3b", CE["wCR"] / (W * R3) * 1e12)
v.check("Ex 21-07.3c", CE["X_R"] * R3)
v.check("Ex 21-07.3d", CE["X_R"] * R3 / W * 1e9)
v.check("Ex 21-07.3e", 1.0 / 3.3)
v.check("Ex 21-07.3f", CE["vpk"] * 3.3)
v.check("Ex 21-07.3g", CE["ipk"] / 3.3)
v.check("Ex 21-07.3h", 100)
v.check("Ex 21-07.3i", CE["P"] * 3.3 ** 2 / R3)


# ================================================================ Example 21-07.4
def f3_max_v1():
    th = np.linspace(0, 2 * np.pi, 20001)
    return optimize.brentq(lambda v1: (1 - v1 * np.cos(th) + v1 / 9 * np.cos(3 * th)).min(), 0.5, 1.5, xtol=1e-14)


V1 = f3_max_v1()
v.check("Ex 21-07.4a", V1)
v.check("Ex 21-07.4b", V1 / 9)
idc_h, i1_h = fourier_trunc(180)
v.check("Ex 21-07.4c", 0.5 * V1 * i1_h / idc_h * 100)
v.check("Ex 21-07.4d", db20(V1))

# ================================================================ Example 21-07.5
etaA = lambda x: 0.5 * x * x  # noqa: E731
etaB = lambda x: math.pi / 4 * x  # noqa: E731
v.check("Ex 21-07.5a", etaA(0.5) * 100)
v.check("Ex 21-07.5b", etaB(0.5) * 100)
xb = 10 ** (-9.64 / 20)
v.check("Ex 21-07.5c", etaA(xb) * 100)
v.check("Ex 21-07.5d", etaB(xb) * 100)
PAPR = db10(math.log(1e4))
v.check("Ex 21-07.5e", rayleigh_avg(etaA, PAPR) * 100)
v.check("Ex 21-07.5f", rayleigh_avg(etaB, PAPR) * 100)
etaD = lambda x: doherty_phasor(x)[3] if x > 0 else math.pi / 2 * 1e-12  # noqa: E731
DAVG = rayleigh_avg(lambda x: doherty_phasor(max(x, 1e-9))[3], PAPR)
v.check("Ex 21-07.5g", DAVG * 100)

# ================================================================ Example 21-07.6
v.check("Ex 21-07.6a", 25 / 2)
v.check("Ex 21-07.6b", 25)
vm1, p1, _, e1 = doherty_phasor(1.0)
v.check("Ex 21-07.6c", p1)
v.check("Ex 21-07.6d", db10(p1 / 1e-3))
vmh, ph, _, eh = doherty_phasor(0.5)
v.check("Ex 21-07.6e", ph)
v.check("Ex 21-07.6f", eh * 100)
v.check("Ex 21-07.6g", vmh)
v.assert_true("main amplitude at peak is also 28 V", abs(vm1 - 28) < 1e-9)
v.assert_true("efficiency at peak is pi/4", abs(e1 - math.pi / 4) < 1e-12)
_, p23, _, e23 = doherty_phasor(2 / 3)
v.check("Ex 21-07.6h", p23)
v.check("Ex 21-07.6i", e23 * 100)
xs = np.linspace(0.5, 1, 2001)
v.assert_true("the dip is at x = 2/3", abs(xs[np.argmin([doherty_phasor(x)[3] for x in xs])] - 2 / 3) < 1e-3)
v.check("Ex 21-07.6j", DAVG * 100)
v.check("Ex 21-07.6k", math.sqrt(12.5 * 50))

# ================================================================ Example 21-07.7
v.check("Ex 21-07.7a", rayleigh_avg(lambda x: math.pi / 4, PAPR) * 100)
v.check("Ex 21-07.7b", rayleigh_avg(lambda x: math.pi / 4, PAPR) * 85)
ET20 = rayleigh_avg(lambda x: math.pi / 4 * x / max(x, 0.2), PAPR)
v.check("Ex 21-07.7c", ET20 * 100)
v.check("Ex 21-07.7d", ET20 * 85)
rpk = math.sqrt(10 ** (PAPR / 10))
rf = 0.2 * rpk
v.check("Ex 21-07.7e", integrate.quad(lambda r: 2 * r * math.exp(-r * r), 0, rf)[0] * 100)
v.check("Ex 21-07.7f", integrate.quad(lambda r: r * r * 2 * r * math.exp(-r * r), 0, rf)[0] * 100)

# ================================================================ Example 21-07.8
v.check("Ex 21-07.8a", 2 * (-20) + db10(1 / 3))
v.check("Ex 21-07.8b", optimize.brentq(lambda d: 2 * d + db10(1 / 3) + 45, -60, 0))
X = lab.ofdm()
asat = 10 ** (10 / 20)
PAm = lambda s: lab.rapp(s, 1.0, asat, 2.0)  # noqa: E731
v.check("Ex 21-07.8c", lab.aclr_db(PAm(X)))
U = lab.dpd_loop(X, PAm, iterations=4, orders=(1, 3, 5))
v.check("Ex 21-07.8d", lab.aclr_db(PAm(U)))
a = np.minimum(np.abs(X), 0.98 * asat)
UI = a / (1 - (a / asat) ** 4) ** 0.25 * np.exp(1j * np.angle(X))
v.check("Ex 21-07.8e", lab.aclr_db(PAm(UI)))
v.check("Ex 21-07.8f", db10(np.quantile(np.abs(X) ** 2, 1 - 1e-4)))
# cubic theory against simulation: ACLR = |a3|^2 P^2 / (3 |a1|^2)
P = 0.01
sim = lab.aclr_db(lab.cubic(math.sqrt(P) * X, 1.0, -0.05))
v.assert_true("cubic ACLR formula within 0.5 dB of the OFDM simulation", abs(sim - db10(0.05 ** 2 * P ** 2 / 3)) < 0.5)

# ================================================================ lab
v.check("Lab 21-07.a", db10(0.05 ** 2 * 0.01 ** 2 / 3))
v.check("Lab 21-07.b", sim)
asat12 = 10 ** (12 / 20)
PA12 = lambda s_: lab.rapp(s_, 1.0, asat12, 2.0)  # noqa: E731
Y12 = PA12(X)
U12 = lab.dpd_loop(X, PA12, iterations=4, orders=(1, 3, 5))
v.check("Lab 21-07.c", lab.aclr_db(Y12))
v.check("Lab 21-07.d", lab.aclr_db(PA12(U12)))
v.check("Lab 21-07.e", lab.evm_pct(Y12, X))
v.check("Lab 21-07.f", lab.evm_pct(PA12(U12), X))

# ================================================================ text values
v.check("Txt 21-07.a", 0.5 * i1_h / idc_h * 100)
v.check("Txt 21-07.b", 0.5 * V1 * i1_h / idc_h * 100)
v.check("Txt 21-07.c", CE["P"])
v.check("Txt 21-07.d", CE["wCR"])
v.check("Txt 21-07.e", CE["X_R"])
v.check("Txt 21-07.f", CE["vpk"])
v.check("Txt 21-07.g", CE["ipk"])
v.check("Txt 21-07.h", CE["Im"])
x_first = optimize.brentq(lambda x: doherty_phasor(x)[0] - 28 + 1e-9, 0.1, 0.9)
v.check("Txt 21-07.i", -db20(x_first))
v.check("Txt 21-07.j", min(doherty_phasor(x)[3] for x in xs) * 100)
xg = optimize.brentq(lambda x: doherty_phasor(x, gamma=2.0)[0] - 28 + 1e-9, 0.05, 0.9)
_, pg, _, _ = doherty_phasor(xg, gamma=2.0)
_, pgmax, _, _ = doherty_phasor(1.0, gamma=2.0)
v.check("Txt 21-07.k", -db10(pg / pgmax))
v.check("Txt 21-07.l", db10(1 / 3))
v.check("Txt 21-07.m", ET20 * 85)
v.check("Txt 21-07.n", 30.15 - 9)
v.check("Txt 21-07.o", 10 ** ((30.15 - 9) / 10) / 830 * 100)

# ================================================================ problems
v.check("21-07.1a", 0.1 / 0.25 * 100)
pin1 = 10 ** ((20 - 8) / 10) * 1e-3
v.check("21-07.1b", pin1 * 1e3)
v.check("21-07.1c", (0.1 - pin1) / 0.25 * 100)
v.check("21-07.1d", optimize.brentq(lambda g: (0.1 / 10 ** (g / 10)) / 0.25 - 0.01, 0, 40))
r2 = (5 - 0.5) ** 2 / (2 * 2)
v.check("21-07.2a", r2)
v.check("21-07.2b", 50 / r2)
v.check("21-07.2c", math.sqrt(50 / r2 - 1))
r40 = (3.4 - 0.4) ** 2 / (2 * 40)
v.check("21-07.2d", r40)
v.check("21-07.2e", 50 / r40)
idcA, i1A = fourier_trunc(360)
v.check("21-07.3a", 0.5 * i1A / idcA * 0.9 * 100)
v.check("21-07.3b", 0.5 * i1_h / idc_h * 0.9 * 100)
for (ke, kp, kr), a in ((("a", "c", "e"), 300), (("b", "d", "f"), 150)):
    idc, i1 = fourier_trunc(a)
    v.check(f"21-07.4{ke}", 0.5 * i1 / idc * 100)
    v.check(f"21-07.4{kp}", db20(i1 / ref))
    v.check(f"21-07.4{kr}", 1 / i1)
w5 = 2 * math.pi * 0.9e9
r5 = CE["P"] * 25 / 2
v.check("21-07.5a", r5)
v.check("21-07.5b", CE["wCR"] / (w5 * r5) * 1e12)
v.check("21-07.5c", CE["X_R"] * r5)
v.check("21-07.5d", CE["X_R"] * r5 / w5 * 1e9)
v.check("21-07.5e", CE["vpk"] * 5)
v.check("21-07.5f", 2 / 5)
v.check("21-07.5g", CE["ipk"] * 0.4)
vmax = 12 / CE["vpk"]
v.check("21-07.5h", vmax)
v.check("21-07.5i", CE["P"] * vmax ** 2 / r5)
th = np.linspace(0, 2 * np.pi, 20001)
v16 = optimize.brentq(lambda v1: (1 - v1 * np.cos(th) + v1 / 18 * np.cos(3 * th)).min(), 0.5, 1.5, xtol=1e-14)
v.check("21-07.6a", v16)
v.check("21-07.6b", 0.5 * v16 * i1_h / idc_h * 100)
for keys, bo in ((("a", "b", "c"), 3), (("d", "e", "f"), 6), (("g", "h", "i"), 10)):
    x = 10 ** (-bo / 20)
    v.check(f"21-07.7{keys[0]}", etaA(x) * 100)
    v.check(f"21-07.7{keys[1]}", etaB(x) * 100)
    v.check(f"21-07.7{keys[2]}", doherty_phasor(x)[3] * 100)
b8 = rayleigh_avg(etaB, 8.0)
d8 = rayleigh_avg(lambda x: doherty_phasor(max(x, 1e-9))[3], 8.0)
v.check("21-07.8a", b8 * 100)
v.check("21-07.8b", d8 * 100)
v.check("21-07.8c", 10 / b8)
v.check("21-07.8d", 10 / d8)
v.check("21-07.8e", 10 / b8 - 10 / d8)
v.check("21-07.9a", 25 / 3)
v.check("21-07.9b", 25)
_, pg1, _, _ = doherty_phasor(1.0, gamma=2.0)
v.check("21-07.9c", pg1)
v.check("21-07.9d", -db10(pg / pg1))
v.check("21-07.9e", pg)
xs9 = np.linspace(1 / 3, 1, 60001)
e9 = np.array([doherty_phasor(x, gamma=2.0)[3] for x in xs9])
v.check("21-07.9g", xs9[np.argmin(e9)])
v.check("21-07.9h", e9.min() * 100)
v.check("21-07.9i", rayleigh_avg(lambda x: doherty_phasor(max(x, 1e-9), gamma=2.0)[3], PAPR) * 100)
v.check("21-07.10a", DAVG / ET20 * 100)
v.check("21-07.10b", DAVG / (math.pi / 4) * 100)
v.check("21-07.11a", 5 + optimize.brentq(lambda d: 2 * d + db10(1 / 3) + 38, -60, 0))
v.check("21-07.11b", 3 * 100)
v.check("21-07.11c", 5 * 100)
# 12: expand the predistorted cubic numerically and read the x|x|^4 coefficient
a1, a3 = 10.0, -2.0
b3 = -a3 / a1
v.check("21-07.12a", b3)
amps = np.array([1e-3, 2e-3])
yv = [a1 * (r + b3 * r ** 3) + a3 * (r + b3 * r ** 3) ** 3 - a1 * r for r in amps]
v.check("21-07.12b", yv[0] / amps[0] ** 5)
v.check("21-07.12c", abs(a3) * 0.5 ** 3)
v.check("21-07.12d", abs(3 * a3 * b3) * 0.5 ** 5)
v.check("21-07.12e", db20(abs(a3) * 0.5 ** 3 / (abs(3 * a3 * b3) * 0.5 ** 5)))
v.check("21-07.13a", integrate.quad(lambda u: math.exp(-u), 10 ** 0.8, np.inf)[0])
v.check("21-07.13b", 10 ** (-39.25 / 20) * 100)
v.check("21-07.13c", (d8 - DAVG) * 100)
po14 = 10 ** (26 / 10) * 1e-3
pi14 = 10 ** (-2 / 10) * 1e-3
v.check("21-07.14a", po14 * 1e3)
v.check("21-07.14b", pi14 * 1e3)
v.check("21-07.14c", (po14 - pi14) / 0.4 / 3.8 * 1e3)
v.check("21-07.14d", (po14 - pi14) / 0.5 / 3.8 * 1e3)
v.check("21-07.14e", (po14 - pi14) / 3.8 * (1 / 0.4 - 1 / 0.5) * 1e3)

sys.exit(v.finish())
