#!/usr/bin/env python3
"""Verify chapter 15-12 (applications: PLLs, regulators, thermal management): examples, problems, lab answers.

Routes (each independent of labs/15-12-lab/loops.py, which is then cross-checked):
- PLL designs from the closed forms of section 3.2, confirmed by root finding on |L| = 1 with the phase
  written as a sum of factor angles; closed-loop poles by numpy roots and by the factorization;
- step and impulse responses in closed form from partial fractions (scipy.signal.residue), so overshoot,
  settling and peak phase error are exact up to root refinement;
- jitter by trapezoidal integration on a dense logarithmic grid (loops.jitter uses adaptive quadrature);
- LDO margins by root finding with factor-wise phase; the ESR window by bisection;
- droop in closed form, checked against a numerical impulse response;
- the two-node thermal model with the matrix exponential, and the sampled limiter re-implemented here;
- the discrete thermal loop's margins with labs/15-11-lab/digital.py and on the unit circle here.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.linalg import expm
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
for lab in ("15-12-lab", "15-11-lab"):
    sys.path.insert(0, str(ROOT / "labs" / lab))
from eeverify import Verifier  # noqa: E402
import loops as lp  # noqa: E402
import digital as dg  # noqa: E402

CH = ROOT / "chapters" / "15-12-control-applications-pll-regulators-thermal.md"
v = Verifier.from_files("15-12", CH, ROOT / "solutions" / "15-12-solutions.md", ROOT / "labs" / "15-12-lab" / "README.md")
TWO_PI = 2 * math.pi


# ---------------------------------------------------------------- independent helpers
def x_from_pm(pm_deg):
    r = math.radians(pm_deg)
    return math.tan(r) + 1 / math.cos(r)


def design(fc, pm_deg, Icp, Kv, N):
    wc = TWO_PI * fc
    x = x_from_pm(pm_deg)
    tz, tp, K = x / wc, 1 / (x * wc), wc**2 / x
    Ctot = Icp * Kv / (TWO_PI * N * K)
    C2 = Ctot / x**2
    C = Ctot - C2
    return dict(x=x, b=x * x, wc=wc, tz=tz, tp=tp, K=K, Ctot=Ctot, C2=C2, C=C, R=tz / C)


def pll_L(K, tz, tp):
    return (lambda w: K * (1 + 1j * w * tz) / ((1j * w) ** 2 * (1 + 1j * w * tp)),
            lambda w: -math.pi + math.atan(w * tz) - math.atan(w * tp))


def crossover(Lf, phf, lo, hi, n=20001):
    w = np.logspace(math.log10(lo), math.log10(hi), n)
    m = np.array([abs(Lf(x)) for x in w])
    k = int(np.flatnonzero(np.diff(np.sign(m - 1)) != 0)[0])
    wc = brentq(lambda x: abs(Lf(x)) - 1, w[k], w[k + 1], xtol=1e-14 * w[k], rtol=1e-15)
    return wc, 180 + math.degrees(phf(wc))


def from_components(Icp, Kv, N, R, C, C2):
    K = Icp * Kv / (TWO_PI * N * (C + C2))
    return K, R * C, R * C * C2 / (C + C2)


def step_closed_form(num, den):
    """Return y(t) for the unit step response of num/den (distinct poles) from partial fractions."""
    r, p, k = signal.residue(np.asarray(num, float), np.polymul(np.asarray(den, float), [1, 0]))
    def y(t):
        return float(np.real(np.sum(r * np.exp(p * t))))
    return y


def impulse_closed_form(num, den):
    r, p, k = signal.residue(np.asarray(num, float), np.asarray(den, float))
    def h(t):
        return float(np.real(np.sum(r * np.exp(p * t))))
    return h


def peak_of(f, t_lo, t_hi, n=200001, sign=1):
    t = np.linspace(t_lo, t_hi, n)
    yv = np.array([sign * f(x) for x in t])
    k = int(np.argmax(yv))
    r = minimize_scalar(lambda x: -sign * f(x), bounds=(t[max(k - 1, 0)], t[min(k + 1, n - 1)]), method="bounded",
                        options={"xatol": 1e-16})
    return sign * -r.fun, r.x


def settle_time(f, final, band, t_end, n=400001):
    t = np.linspace(0, t_end, n)
    yv = np.array([f(x) for x in t])
    out = np.flatnonzero(np.abs(yv - final) > band)
    k = int(out[-1])
    lev = final + band if yv[k] > final else final - band
    return brentq(lambda x: f(x) - lev, t[k], t[k + 1], xtol=1e-16, rtol=1e-15)


Icp, Kv, N = 100e-6, TWO_PI * 100e6, 100

# ---------------------------------------------------------------- Example 15-12.1 (DVFS)
v.check("Ex 15-12.1a", 200 / 10)
v.check("Ex 15-12.1b", 200 / 10 + 5)
v.check("Ex 15-12.1c", 200 / 10 + 5 + 20)
v.check("Ex 15-12.1d", 100 * 20e-6 / 1e-3)
v.check("Ex 15-12.1e", (1.00 / 0.80) ** 2 * 2.0 / 1.2)
v.check("Ex 15-12.1f", (1.00 / 0.80) ** 2)
v.assert_true("Ex1: 56% more energy per operation", round(100 * ((1 / 0.8) ** 2 - 1)) == 56)

# ---------------------------------------------------------------- Example 15-12.2 (PLL design)
d = design(200e3, 60, Icp, Kv, N)
v.assert_true("Ex2: x solves x^2 - 2x tan(PM) - 1 = 0", abs(d["x"] ** 2 - 2 * d["x"] * math.tan(math.radians(60)) - 1) < 1e-12)
v.assert_true("Ex2: x = 2 + sqrt(3)", abs(d["x"] - (2 + math.sqrt(3))) < 1e-12)
v.check("Ex 15-12.2a", d["x"])
v.check("Ex 15-12.2b", d["b"])
v.check("Ex 15-12.2c", d["tz"] * 1e6)
v.check("Ex 15-12.2d", d["tp"] * 1e6)
v.check("Ex 15-12.2e", d["K"])
v.check("Ex 15-12.2f", d["Ctot"] * 1e12)
v.check("Ex 15-12.2g", d["C2"] * 1e12)
v.check("Ex 15-12.2h", d["C"] * 1e12)
v.check("Ex 15-12.2i", d["R"] / 1e3)
v.check("Ex 15-12.2j", math.degrees(math.pi * 200e3 / 10e6))
Kc, tzc, tpc = from_components(Icp, Kv, N, d["R"], d["C"], d["C2"])
Lf, phf = pll_L(Kc, tzc, tpc)
wc2, pm2 = crossover(Lf, phf, 1e3, 1e9)
v.assert_true("Ex2: components give 200 kHz crossover and 60.0 deg", abs(wc2 / TWO_PI - 200e3) < 1e-3 and abs(pm2 - 60) < 1e-9)
dl = lp.pll_design(200e3, 60, Icp, Kv, N)
v.assert_true("Ex2: lab pll_design agrees", all(abs(dl[k] / d[k] - 1) < 1e-12 for k in ("x", "tz", "tp", "K", "C", "C2", "R")))
v.assert_true("Ex2: C/C2 = b - 1 = 12.9", round(d["C"] / d["C2"], 1) == 12.9 and abs(d["C"] / d["C2"] - (d["b"] - 1)) < 1e-9)
v.assert_true("Ex2: 1 nF filter is about four times the capacitance", 4 < 1e-9 / d["Ctot"] < 4.5)
v.assert_true("Ex2: wc = 1.2566e6 rad/s", round(d["wc"] / 1e6, 4) == 1.2566)

# ---------------------------------------------------------------- section 3.2 claims
v.assert_true("3.2: real pair needs PM >= atan(8/6) = 53.1 deg", round(math.degrees(math.atan(8 / 6)), 1) == 53.1
              and abs(x_from_pm(math.degrees(math.atan(8 / 6))) - 3) < 1e-12)
v.assert_true("3.2: sampling cost 18 deg at fref/10", abs(math.degrees(math.pi / 10) - 18) < 1e-12)
for pm in (45, 53.13, 60, 65):
    dd = design(1 / TWO_PI, pm, 1, 1, 1)
    char = [dd["tp"], 1, dd["K"] * dd["tz"], dd["K"]]
    v.assert_true(f"3.2: s = -wc is a closed-loop pole for PM {pm}", abs(np.polyval(char, -1.0)) < 1e-12)
    fac = np.polymul([1, 1], [1, dd["x"] - 1, 1])
    v.assert_true(f"3.2: factorization for PM {pm}", np.allclose(np.asarray(char) / char[0], fac, atol=1e-12))

# ---------------------------------------------------------------- Example 15-12.3 (closed loop, hop)
num = [Kc * tzc, Kc]
den = [tpc, 1, 0, 0]
dcl = np.polyadd(den, num)
poles = np.sort(np.roots(dcl).real)
v.assert_true("Ex3: poles are real", np.all(np.abs(np.roots(dcl).imag) < 1e-6))
v.check("Ex 15-12.3a", poles[1])
v.check("Ex 15-12.3b", poles[2])
v.check("Ex 15-12.3c", poles[0])
zeta = (d["x"] - 1) / 2
v.assert_true("Ex3: zeta 1.366 and factorization roots", round(zeta, 3) == 1.366 and
              np.allclose(sorted([d["wc"] * (-zeta - math.sqrt(zeta**2 - 1)), -d["wc"], d["wc"] * (-zeta + math.sqrt(zeta**2 - 1))]), poles, rtol=1e-9))
T = lambda w: Lf(w) / (1 + Lf(w))  # noqa: E731
pkdb, wpk = peak_of(lambda lw: 20 * math.log10(abs(T(10**lw))), 3, 8, n=20001)
v.check("Ex 15-12.3d", pkdb)
v.check("Ex 15-12.3e", 10**wpk / TWO_PI / 1e3)
wl = np.logspace(3, 8, 20001)
k3 = int(np.flatnonzero(np.array([abs(T(x)) for x in wl]) < 1 / math.sqrt(2))[0])
w3 = brentq(lambda x: abs(T(x)) - 1 / math.sqrt(2), wl[k3 - 1], wl[k3], xtol=1e-10, rtol=1e-15)
v.check("Ex 15-12.3f", w3 / TWO_PI / 1e3)
v.assert_true("Ex3: -3 dB bandwidth is 1.56 times fc", round(w3 / d["wc"], 2) == 1.56)
v.assert_true("Ex3: peak at 0.466 wc", round(10**wpk / d["wc"], 3) == 0.466)
nT, dT = lp.closed(*lp.pll_loop(Icp, Kv, N, d["R"], d["C"], d["C2"]))
v.assert_true("Ex3: lab peaking and bw3db agree", abs(lp.peaking(nT, dT)[0] - pkdb) < 1e-9 and abs(lp.bw3db(nT, dT) - w3 / TWO_PI) < 1e-3)
# hop: N = 101
K1, tz1, tp1 = from_components(Icp, Kv, 101, d["R"], d["C"], d["C2"])
num1, den1 = [K1 * tz1, K1], [tp1, 1, 0, 0]
dcl1 = np.polyadd(den1, num1)
y = step_closed_form(num1, dcl1)
ypk, tpk = peak_of(y, 0, 20e-6)
v.check("Ex 15-12.3g", 100 * (ypk - 1))
ts = settle_time(y, 1.0, 1e-4, 100e-6)
v.check("Ex 15-12.3h", ts * 1e6)
dw = TWO_PI * 10e6 * (1 - 100 / 101)
v.assert_true("Ex3: equivalent reference step 2 pi x 99.0 kHz", round(dw / TWO_PI / 1e3, 1) == 99.0)
h = impulse_closed_form([tp1, 1], dcl1)          # E(s) = dw (tp s + 1)/(den + num)
epk, tep = peak_of(lambda t: dw * h(t), 0, 20e-6)
v.check("Ex 15-12.3i", epk)
v.assert_true("Ex3: PFD error well inside 2 pi", epk < 0.1 * TWO_PI)
lpk, _ = lp.phase_error_peak(num1, den1, dw, 50e-6)
v.assert_true("Ex3: lab phase_error_peak agrees", abs(lpk - epk) < 1e-6)
v.assert_true("Ex3: gain falls by 1%", round(100 * (1 - K1 / Kc)) == 1)
v.assert_true("Ex3: 1.9 MHz above the new frequency", round((ypk - 1) * 10, 1) == 1.9)
v.assert_true("Ex3: zero at wc/x = 3.37e5", round(d["wc"] / d["x"] / 1e5, 2) == 3.37)
v.assert_true("Ex3: zero slower than every pole", d["wc"] / d["x"] < abs(poles[2]))

# ---------------------------------------------------------------- Example 15-12.4 (droop)
dI, C, dV = 20.0, 1e-3, 0.04
v.check("Ex 15-12.4a", dV / dI * 1e3)
wll = dI / (C * dV)
v.check("Ex 15-12.4b", wll)
v.check("Ex 15-12.4c", wll / TWO_PI / 1e3)
wpi = (2 / math.e) * dI / (C * dV)
v.check("Ex 15-12.4d", wpi)
v.check("Ex 15-12.4e", wpi / TWO_PI / 1e3)
vpi = lambda t: -(dI / C) * t * math.exp(-wpi * t / 2)  # noqa: E731
vpk, tvpk = peak_of(vpi, 0, 50e-6, sign=-1)
v.assert_true("Ex4: closed-form peak is -40 mV at 2/wc", abs(vpk + dV) < 1e-12 and abs(tvpk - 2 / wpi) < 1e-10)
v.check("Ex 15-12.4f", 2 / wpi * 1e6)
v.check("Ex 15-12.4g", brentq(lambda t: -vpi(t) - 0.004, 2 / wpi, 1e-3, xtol=1e-16) * 1e6)
tt = np.linspace(0, 60e-6, 61)
v.assert_true("Ex4: closed form equals the numerical impulse response", np.allclose(lp.droop(dI, C, wpi, wpi / 4, tt), [vpi(t) for t in tt], atol=1e-9))
v.assert_true("Ex4: load-line droop settles at -40 mV", abs(lp.droop(dI, C, wll, 0.0, [1e-3])[0] + dV) < 1e-9)
Lpi = lambda w: (wpi / (1j * w)) * (1 + wpi / 4 / (1j * w))  # noqa: E731
wcp, pmp = crossover(Lpi, lambda w: -math.pi / 2 - math.atan(wpi / 4 / w), 1e3, 1e8)
v.check("Ex 15-12.4h", pmp)
v.assert_true("Ex4: PI crosses slightly above wc", 1 < wcp / wpi < 1.05)
v.assert_true("Ex4: PI needs 26% less bandwidth", round(100 * (1 - wpi / wll)) == 26)

# ---------------------------------------------------------------- Example 15-12.5 (jitter)
def jitter_trap(fc, L_ref=-110.0, L_vco=-120.0, f_out=2e9, n=400001):
    dd = design(fc, 60, 1, 1, 1)
    Lj, _ = pll_L(dd["K"], dd["tz"], dd["tp"])
    lf = np.linspace(4, 8, n)
    f = 10**lf
    Lw = Lj(TWO_PI * f)
    Tm2, Sm2 = np.abs(Lw / (1 + Lw)) ** 2, np.abs(1 / (1 + Lw)) ** 2
    p = 10 ** (L_ref / 10) * Tm2 + 10 ** ((L_vco + 20 * np.log10(1e6 / f)) / 10) * Sm2
    phi = math.sqrt(2 * np.trapezoid(p * f * math.log(10), lf))
    return phi, phi / (TWO_PI * f_out)


v.check("Ex 15-12.5a", 10 ** (6 - 0.5) / 1e3)
res5 = {fc: jitter_trap(fc) for fc in (1e5, 10**5.5, 1e6)}
for fc, key in ((1e5, "Ex 15-12.5b"), (10**5.5, "Ex 15-12.5c"), (1e6, "Ex 15-12.5d")):
    v.check(key, res5[fc][1] * 1e15)
    v.assert_true(f"Ex5: lab jitter agrees at {fc:.0f} Hz", abs(lp.jitter(fc)[1] / res5[fc][1] - 1) < 1e-6)
v.check("Ex 15-12.5e", res5[10**5.5][0] * 1e3)
v.assert_true("Ex5: rms phase 6.85 mrad at 100 kHz and 1 MHz", round(res5[1e5][0] * 1e3, 2) == 6.85 and round(res5[1e6][0] * 1e3, 2) == 6.85)
opt = minimize_scalar(lambda lf: jitter_trap(10**lf, n=100001)[1], bounds=(5, 6), method="bounded", options={"xatol": 1e-7})
v.check("Ex 15-12.5f", 10**opt.x / 1e3)
v.assert_true("Ex5: optimum within 0.02% of the crossing", abs(10**opt.x / 10**5.5 - 1) < 2e-4)
v.assert_true("Ex5: a factor of ~3 off costs 32% more jitter", round(100 * (res5[1e5][1] / res5[10**5.5][1] - 1)) == 32)
v.assert_true("Ex5: crossing below fref/10 = 5 MHz", 10**5.5 < 50e6 / 10)
dd = design(1 / TWO_PI, 60, 1, 1, 1)
Lu, _ = pll_L(dd["K"], dd["tz"], dd["tp"])
v.assert_true("Ex5: |T(j wc^2/w)| = |S(j w)| for the max-margin loop",
              all(abs(abs(Lu(1 / u) / (1 + Lu(1 / u))) - abs(1 / (1 + Lu(u)))) < 1e-12 for u in (0.03, 0.3, 0.9, 2.0, 17.0)))
# Figure 1 alt-text claims
dfig = design(10**5.5, 60, 1, 1, 1)
Lfig, _ = pll_L(dfig["K"], dfig["tz"], dfig["tp"])
Sv = lambda f: -120 + 20 * math.log10(1e6 / f) + 20 * math.log10(abs(1 / (1 + Lfig(TWO_PI * f))))  # noqa: E731
Rv = lambda f: -110 + 20 * math.log10(abs(Lfig(TWO_PI * f) / (1 + Lfig(TWO_PI * f))))  # noqa: E731
tot = lambda lf: 10 * math.log10(10 ** (Rv(10**lf) / 10) + 10 ** (Sv(10**lf) / 10))  # noqa: E731
tpkv, ftp = peak_of(tot, 4, 7, n=30001)
v.assert_true("Figure 1: shaped VCO noise about -129 dBc/Hz at 10 kHz", abs(Sv(1e4) + 129) < 0.5)
v.assert_true("Figure 1: total peaks near -106 dBc/Hz around 180 kHz", abs(tpkv + 106) < 0.5 and 150e3 < 10**ftp < 220e3)

# ---------------------------------------------------------------- Example 15-12.6 (LDO ESR window)
def ldo_L(Re, A0=1000.0, wa=TWO_PI * 1e4, gm=0.5, RL=10.0, beta=0.5, wg=TWO_PI * 1e6, CL=10e-6):
    wz, wo = 1 / (Re * CL), 1 / ((RL + Re) * CL)
    L0 = A0 * beta * gm * RL
    Lf_ = lambda w: L0 * (1 + 1j * w / wz) / ((1 + 1j * w / wa) * (1 + 1j * w / wg) * (1 + 1j * w / wo))  # noqa: E731
    ph = lambda w: math.atan(w / wz) - math.atan(w / wa) - math.atan(w / wg) - math.atan(w / wo)  # noqa: E731
    return Lf_, ph


def ldo_margin(Re, **kw):
    Lf_, ph = ldo_L(Re, **kw)
    return crossover(Lf_, ph, 1.0, 1e10)


def window(pm_min=45.0, **kw):
    lr = np.linspace(-3, 1, 401)
    pms = np.array([ldo_margin(10**x, **kw)[1] for x in lr])
    k = int(np.argmax(pms))
    best = minimize_scalar(lambda x: -ldo_margin(10**x, **kw)[1], bounds=(lr[k - 1], lr[k + 1]), method="bounded",
                           options={"xatol": 1e-10})
    rb = 10**best.x
    f = lambda r: ldo_margin(r, **kw)[1] - pm_min  # noqa: E731
    return brentq(f, 1e-3, rb, xtol=1e-14), brentq(f, rb, 10, xtol=1e-14), rb, -best.fun


lo6, hi6, rb6, pmb6 = window()
v.check("Ex 15-12.6a", lo6)
v.check("Ex 15-12.6b", hi6)
v.check("Ex 15-12.6c", pmb6)
v.check("Ex 15-12.6d", rb6)
v.check("Ex 15-12.6e", ldo_margin(0.005)[1])
wc6, pm6 = ldo_margin(0.3)
v.check("Ex 15-12.6f", wc6 / TWO_PI / 1e3)
v.check("Ex 15-12.6g", pm6)
v.check("Ex 15-12.6h", 1 / (TWO_PI * 0.3 * 10e-6) / 1e3)
lw = lp.esr_window(45)
v.assert_true("Ex6: lab esr_window agrees", abs(lw[0] - lo6) < 1e-8 and abs(lw[1] - hi6) < 1e-8 and abs(lw[3] - pmb6) < 1e-6)
v.assert_true("Ex6: lab ldo_pm agrees at 0.3 ohm", abs(lp.ldo_pm(0.3) - pm6) < 1e-8)
v.assert_true("Ex6: 1 uF version has no 45 deg design (best below 45)", max(ldo_margin(10**x, CL=1e-6)[1] for x in np.linspace(-3, 1, 81)) < 45)
v.assert_true("Ex6: output pole near 1e4 1/s", abs(1 / (10 * 10e-6) - 1e4) < 1e-9)
f6 = wc6 / TWO_PI
two_poles = math.degrees(math.atan(wc6 / (TWO_PI * 1e4)) + math.atan(wc6 * 10.3e-5))
v.assert_true("Ex6 sanity: 85.1, 31.8 and -126.7 deg", round(math.degrees(math.atan(f6 / 53.05e3)), 1) == 85.1
              and round(math.degrees(math.atan(f6 / 1e6)), 1) == 31.8
              and round(-180 + round(math.degrees(math.atan(621 / 53.1)), 1) - round(math.degrees(math.atan(0.621)), 1), 1) == -126.7)
v.assert_true("Ex6 sanity: the two low poles give -178.9 deg", round(-two_poles, 1) == -178.9)
v.assert_true("Guided exercise: 5 mohm zero at 3.2 MHz", round(1 / (TWO_PI * 0.005 * 10e-6) / 1e6, 1) == 3.2)

# ---------------------------------------------------------------- Example 15-12.7 (throttle)
CJ, RJC, CH, RCA, TA, TLIM = 5.0, 0.15, 300.0, 0.35, 30.0, 95.0
A = np.array([[-1 / (CJ * RJC), 1 / (CJ * RJC)], [1 / (CH * RJC), -1 / (CH * RJC) - 1 / (CH * RCA)]])
B = np.array([1 / CJ, 0.0])
Kp, Ki, Ts = 10.0, 10.0 / 0.75, 0.1
v.check("Ex 15-12.7a", Kp)
v.check("Ex 15-12.7b", Ki)
v.check("Ex 15-12.7c", Ki * Ts)
v.assert_true("Ex7: fast time constant 0.75 s and crossover 0.2 Kp", CJ * RJC == 0.75 and abs(Kp * RJC / 0.75 - 2) < 1e-12)
num_s, den_s = signal.ss2tf(A, B.reshape(-1, 1), np.array([[1.0, 0.0]]), np.zeros((1, 1)))
num_s = np.trim_zeros(np.where(np.abs(num_s[0]) < 1e-14, 0, num_s[0]), "f")
nz, dz = dg.zoh(num_s, den_s, Ts)
numL, denL = np.polymul([Kp + Ki * Ts, -Kp], nz), np.polymul([1, -1], dz)
md = dg.dmargins(numL, denL, Ts)


def unit_circle_pm(numz, denz, T, n=200001):
    w = np.linspace(1e-4, math.pi / T * (1 - 1e-9), n)
    z = np.exp(1j * w * T)
    Lz = np.polyval(numz, z) / np.polyval(denz, z)
    k = int(np.flatnonzero(np.diff(np.sign(np.abs(Lz) - 1)) != 0)[0])
    g = lambda x: abs(np.polyval(numz, cmath.exp(1j * x * T)) / np.polyval(denz, cmath.exp(1j * x * T))) - 1  # noqa: E731
    wc = brentq(g, w[k], w[k + 1], xtol=1e-14)
    Lc = np.polyval(numz, cmath.exp(1j * wc * T)) / np.polyval(denz, cmath.exp(1j * wc * T))
    ph = np.unwrap(np.angle(Lz))[k] + cmath.phase(Lc / Lz[k])
    return wc, 180 + math.degrees(ph)


wcd, pmd = unit_circle_pm(numL, denL, Ts)
v.assert_true("Ex7: discrete margins agree with labs/15-11-lab dmargins", abs(md["pm"] - pmd) < 1e-6 and abs(md["wc"] - wcd) < 1e-6)
v.check("Ex 15-12.7d", wcd)
v.check("Ex 15-12.7e", pmd)
v.check("Ex 15-12.7f", (TLIM - TA) / (RJC + RCA))
v.check("Ex 15-12.7g", RCA * CH * math.log(2))
M = np.zeros((3, 3))
M[:2, :2] = A
M[:2, 2] = B
TJ_at = lambda t: TA + (expm(M * t) @ np.array([0.0, 0.0, 200.0]))[0]  # noqa: E731
t_lim = brentq(lambda t: TJ_at(t) - TLIM, 1, 300, xtol=1e-12)
v.check("Ex 15-12.7h", t_lim)
tau = CH * RJC * RCA / (RJC + RCA)
v.check("Ex 15-12.7i", tau)
v.check("Ex 15-12.7j", 130 + 70 * math.exp(-60 / tau))
v.assert_true("Ex7: 200 x 0.15 = 30 K, final heat-sink rise 70 K, R_CA C_H = 105 s",
              200 * RJC == 30 and 200 * RCA == 70 and RCA * CH == 105)
# with T_J held at the limit, the heat-sink node is first order with time constant tau (exact statement in 3.6)
a_c = -(1 / RJC + 1 / RCA) / CH
v.assert_true("3.6: held-junction heat-sink pole is -1/tau", abs(-1 / a_c - tau) < 1e-12)


def throttle_here(Kp, Ki, Ts=0.1, t_end=400.0, Pmax=200.0):
    E = expm(M * Ts)
    x = np.zeros(2)
    P, Tprev = Pmax, TA
    out_t, out_T, out_P, t_on = [], [], [], None
    for k in range(int(round(t_end / Ts))):
        Tn = TA + x[0]
        P = min(Pmax, max(0.0, P - (Kp * (Tn - Tprev) + Ki * Ts * (Tn - TLIM))))
        Tprev = Tn
        if t_on is None and P < Pmax - 1e-12:
            t_on = k * Ts
        out_t.append(k * Ts)
        out_T.append(Tn)
        out_P.append(P)
        x = (E @ np.append(x, P))[:2]
    return np.array(out_t), np.array(out_T), np.array(out_P), t_on


t7, T7, P7, ton = throttle_here(Kp, Ki)
v.check("Ex 15-12.7k", ton)
v.check("Ex 15-12.7l", T7.max())
k60 = int(round((ton + 60) / Ts))
v.check("Ex 15-12.7m", P7[k60])
v.assert_true("Ex7: settles at 130.0 W", round(P7[-1], 1) == 130.0)
tl, Tl, Pl, tonl = lp.throttle(Kp, Ki)
v.assert_true("Ex7: lab throttle agrees", tonl == ton and np.allclose(Pl, P7, atol=1e-9) and np.allclose(Tl, T7, atol=1e-9))
for s in (0.5, 2.0):
    _, Ts_, Ps_, ts_on = throttle_here(Kp * s, Ki * s)
    v.assert_true(f"Lab discussion 5: gains x{s} change the envelope by under 0.2 W", abs(Ps_[int(round((ts_on + 60) / Ts))] - P7[k60]) < 0.2
                  and Ts_.max() - TLIM < 0.5)

# ---------------------------------------------------------------- Lab answers
Kr, tzr, tpr = from_components(Icp, Kv, N, 13.5e3, 220e-12, 17e-12)
Lr, phr = pll_L(Kr, tzr, tpr)
wcr, pmr = crossover(Lr, phr, 1e3, 1e9)
v.check("Lab 15-12.a", pmr)
v.check("Lab 15-12.b", wcr / TWO_PI / 1e3)
v.assert_true("Lab discussion 1: crossover moves 0.2%, margin by hundredths of a degree",
              round(100 * abs(wcr / d["wc"] - 1), 1) == 0.2 and abs(pmr - 60) < 0.05)

# ---------------------------------------------------------------- Problems
v.check("15-12.1a", 50e-6 * TWO_PI * 5e8 / (TWO_PI * 64 * 500e-12))
v.check("15-12.1b", 0.0)
keys2 = {45: "abcd", 50: "efgh", 65: "ijkl"}
for pm, ks in keys2.items():
    x = x_from_pm(pm)
    v.check(f"15-12.2{ks[0]}", x)
    v.check(f"15-12.2{ks[1]}", x * x)
    v.check(f"15-12.2{ks[2]}", x * x - 1)
    v.check(f"15-12.2{ks[3]}", (x - 1) / 2)
real_pms = [pm for pm in (45, 50, 65) if x_from_pm(pm) >= 3]
v.check("15-12.2m", real_pms[0])
v.assert_true("P2: only 65 deg has real poles", real_pms == [65])
v.assert_true("P2: 45 deg gives zeta = 1/sqrt(2)", abs((x_from_pm(45) - 1) / 2 - 1 / math.sqrt(2)) < 1e-12)
v.assert_true("P2: capacitor spread four times for 20 deg", round((x_from_pm(65) ** 2 - 1) / (x_from_pm(45) ** 2 - 1)) == 4)

v.check("15-12.3a", 25 / 10)
v.check("15-12.3b", math.degrees(math.pi / 25))
v.check("15-12.3c", 20 * 0.1)
v.check("15-12.3d", 10 ** (2 / 20))

d4 = design(1e6, 55, 200e-6, TWO_PI * 1e9, 48)
for k, val in (("a", d4["x"]), ("b", d4["b"]), ("c", d4["tz"] * 1e6), ("d", d4["tp"] * 1e9), ("e", d4["K"]),
               ("f", d4["Ctot"] * 1e12), ("g", d4["C2"] * 1e12), ("h", d4["C"] * 1e12), ("i", d4["R"] / 1e3)):
    v.check(f"15-12.4{k}", val)
v.check("15-12.4j", 180 * 1e6 / 50e6)
K4, tz4, tp4 = from_components(200e-6, TWO_PI * 1e9, 48, d4["R"], d4["C"], d4["C2"])
w4, p4 = crossover(*pll_L(K4, tz4, tp4), 1e3, 1e10)
v.assert_true("P4: components give 1 MHz and 55 deg", abs(w4 / TWO_PI - 1e6) < 1e-2 and abs(p4 - 55) < 1e-9)
v.assert_true("P4: tan 55 + sec 55 = 1.428 + 1.743, zeta 1.086",
              round(math.tan(math.radians(55)), 3) == 1.428 and round(1 / math.cos(math.radians(55)), 3) == 1.743
              and round((d4["x"] - 1) / 2, 3) == 1.086)

d5 = design(1 / TWO_PI, 45, 1, 1, 1)
p5 = np.roots(np.polyadd([d5["tp"], 1, 0, 0], [d5["K"] * d5["tz"], d5["K"]]))
v.check("15-12.5a", min(p5.real, key=lambda r: abs(r + 1)))
v.check("15-12.5b", complex(p5[np.argmax(p5.imag)]))
y5 = step_closed_form([d5["K"] * d5["tz"], d5["K"]], np.polyadd([d5["tp"], 1, 0, 0], [d5["K"] * d5["tz"], d5["K"]]))
y5pk, _ = peak_of(y5, 0, 20)
v.check("15-12.5c", 100 * (y5pk - 1))
L5, _ = pll_L(d5["K"], d5["tz"], d5["tp"])
pk5, w5 = peak_of(lambda lw: 20 * math.log10(abs(L5(10**lw) / (1 + L5(10**lw)))), -2, 2, n=20001)
v.check("15-12.5d", pk5)
v.check("15-12.5e", 10**w5)
y60 = step_closed_form([dd["K"] * dd["tz"], dd["K"]], np.polyadd([dd["tp"], 1, 0, 0], [dd["K"] * dd["tz"], dd["K"]]))
os60 = 100 * (peak_of(y60, 0, 20)[0] - 1)
v.assert_true("P5: 60 deg design 18.8% (scale-free)", round(os60, 1) == 18.8)
v.assert_true("P5: 2.7 times the capacitor ratio; roughly half the overshoot and peaking",
              round((d["b"] - 1) / (d5["b"] - 1), 1) == 2.7 and 0.45 < os60 / (100 * (y5pk - 1)) < 0.6 and 0.45 < pkdb / pk5 < 0.6)

phi6 = math.sqrt(2 * 1e-10 * (1e6 - 1e4))
v.check("15-12.6a", phi6 * 1e3)
v.check("15-12.6b", phi6 / (TWO_PI * 1e9) * 1e12)
v.check("15-12.6c", 100 * (1e6 - 1e5) / (1e6 - 1e4))

wa7, pa7 = ldo_margin(0.3, RL=1000.0)
v.check("15-12.7a", wa7 / TWO_PI / 1e3)
v.check("15-12.7b", pa7)
wb7, pb7 = ldo_margin(0.3, RL=1000.0, gm=0.05)
v.check("15-12.7c", wb7 / TWO_PI / 1e3)
v.check("15-12.7d", pb7)
lo7, hi7, _, _ = window(RL=1000.0, gm=0.05)
v.check("15-12.7e", lo7)
v.check("15-12.7f", hi7)
wc7g, pm7g = ldo_margin(0.15, RL=1000.0, gm=0.05)
v.check("15-12.7g", pm7g)
v.assert_true("P7c: 0.15 ohm fine at full load (55.6 deg), 68.3 kHz at light load",
              round(ldo_margin(0.15)[1], 1) == 55.6 and round(wc7g / TWO_PI / 1e3, 1) == 68.3)
v.assert_true("P7a: RL = 10 ohm reference 621 kHz, 54.3 deg", round(wc6 / TWO_PI / 1e3) == 621 and round(pm6, 1) == 54.3)

C8 = 100 / (TWO_PI * 1e5 * 0.04)
v.check("15-12.8a", C8 * 1e3)
v.check("15-12.8b", (2 / math.e) * C8 * 1e3)

v.check("15-12.9a", 20)
v.check("15-12.9b", 250 / 10)
v.check("15-12.9c", (0.75 / 1.00) ** 2 * 1.0 / 2.0)
v.check("15-12.9d", 0.75**2)

RCA10 = 0.25
A10 = np.array([[-1 / (CJ * RJC), 1 / (CJ * RJC)], [1 / (CH * RJC), -1 / (CH * RJC) - 1 / (CH * RCA10)]])
M10 = np.zeros((3, 3))
M10[:2, :2] = A10
M10[:2, 2] = B
t10 = brentq(lambda t: TA + (expm(M10 * t) @ np.array([0.0, 0.0, 200.0]))[0] - TLIM, 1, 400, xtol=1e-12)
v.check("15-12.10a", (TLIM - TA) / (RJC + RCA10))
v.check("15-12.10b", RCA10 * CH * math.log(50 / 15))
v.check("15-12.10c", t10)
v.check("15-12.10d", CH * RJC * RCA10 / (RJC + RCA10))
v.assert_true("P10: +25% sustained, about 18 s longer", round(100 * (162.5 / 130 - 1)) == 25 and round(t10 - t_lim) == 18)

GL = 0.6
Zth = lambda s: float(np.real_if_close(np.array([1.0, 0.0]) @ np.linalg.solve(s * np.eye(2) - A, B))) if s == 0 else \
    (np.array([1.0, 0.0]) @ np.linalg.solve(s * np.eye(2) - A, B))  # noqa: E731
Z0 = abs(Zth(0))
Z2 = abs(Zth(2j))
v.assert_true("P11: DC thermal gain 0.5 K/W", abs(Z0 - 0.5) < 1e-12)
v.check("15-12.11a", Z0 / (1 - GL * Z0))
v.check("15-12.11b", Z2)
v.check("15-12.11c", abs(Zth(2j) / (1 - GL * Zth(2j))))
v.assert_true("P11: 43% at DC, under 3% at 2 rad/s", round(100 * (1 / (1 - GL * Z0) - 1)) == 43
              and abs(Zth(2j) / (1 - GL * Zth(2j))) / Z2 - 1 < 0.03)

v.check("15-12.12a", 1e6 * 10 ** (-15 / 20) / 1e3)
opt12 = minimize_scalar(lambda lf: jitter_trap(10**lf, L_ref=-100, L_vco=-115, f_out=1e9, n=100001)[1],
                        bounds=(4.8, 5.8), method="bounded", options={"xatol": 1e-7})
v.check("15-12.12b", 10**opt12.x / 1e3)
phi12, j12 = jitter_trap(10**opt12.x, L_ref=-100, L_vco=-115, f_out=1e9)
v.check("15-12.12c", phi12 * 1e3)
v.check("15-12.12d", j12 * 1e12)

sys.exit(v.finish())
