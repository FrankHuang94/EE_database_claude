#!/usr/bin/env python3
"""Verify every published number in chapter 07-07 (worked examples, numbers to know, practitioner
lens), its problem solutions and its lab handout.

Independent routes: the chapter works in Bode form, with asymptotes and closed-form corrections.
Here transfer functions are evaluated from expanded polynomials (numpy polyval) or from time-domain
state equations (C (jwI - A)^-1 B + D); corner, peak and crossover frequencies come from numerical
root-finding and optimization; rise times come from integrating step responses; the gain-phase
integral is evaluated by quadrature; and one steady-state gain is confirmed by integrating the
circuit into steady state and extracting the phasor with a lock-in. ngspice netlists in
labs/07-07-lab are run separately by tools/run_spice.py.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar
from scipy.special import erfinv, sici

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "07-07",
    COURSE / "chapters" / "07-07-frequency-response-and-bode-plots.md",
    COURSE / "solutions" / "07-07-solutions.md",
    COURSE / "labs" / "07-07-lab" / "README.md",
)
pi = math.pi
LN10 = math.log(10)
dB = lambda z: 20 * math.log(abs(z)) / LN10  # noqa: E731  (natural log route, not log10)
dBp = lambda r: 10 * math.log(r) / LN10  # noqa: E731
deg = lambda z: math.degrees(cmath.phase(z))  # noqa: E731


def tf(num, den):
    """Return H(s) from polynomial coefficient lists (highest power first)."""
    return lambda s: np.polyval(num, s) / np.polyval(den, s)


def freq_resp(A, B, C, D, w):
    A = np.atleast_2d(A).astype(complex)
    X = np.linalg.solve(1j * w * np.eye(A.shape[0]) - A, np.atleast_2d(B).astype(complex))
    return complex((np.atleast_2d(C) @ X + np.atleast_2d(D))[0, 0])


def rise_time(A, B, C, t_end, n=200001):
    """10-90% rise time of the unit-step response of dx/dt = Ax + Bu, y = Cx (DC gain normalized)."""
    A, B, C = np.atleast_2d(A).astype(float), np.atleast_2d(B).astype(float).ravel(), np.atleast_2d(C).astype(float)
    sol = solve_ivp(lambda t, x: A @ x + B, (0, t_end), np.zeros(A.shape[0]), method="DOP853",
                    rtol=1e-11, atol=1e-14, dense_output=True, max_step=t_end / 2000)
    t = np.linspace(0, t_end, n)
    y = (C @ sol.sol(t))[0]
    y = y / y[-1]
    return np.interp(0.9, y, t) - np.interp(0.1, y, t)


def unwrap_deg(z_list):
    return np.degrees(np.unwrap(np.angle(np.array(z_list))))


# ================================================================================ Example 1
v.check("Ex 07-07.1a", dB(1.0 / 0.05))
Pin, Pout = 0.05**2 / 10e3, 1.0**2 / 100
v.check("Ex 07-07.1b", dBp(Pout / Pin))
v.check("Ex 07-07.1c", dBp(Pout / Pin) - dB(1.0 / 0.05))
v.check("Ex 07-07.1d", dB(1.0), tol=0.005)
v.check("Ex 07-07.1e", dBp(Pout / 1e-3))
v.check("Ex 07-07.1f", dB(0.05))
v.check("Ex 07-07.1g", dBp(Pin / 1e-3))
v.check("Ex 07-07.1h", math.log(20))
v.assert_true("Np from dB", abs(26.0206 * LN10 / 20 - math.log(20)) < 1e-4)

# ================================================================================ Example 2
R1, C1, G, R2, C2 = 100e3, 100e-9, 100.0, 1e3, 10e-9
# state equations: x1 = v(C1), x2 = v(C2); u = vin.  i(C1) = (vin - x1)/R1 -> node n1 = vin - x1
# C1 dx1/dt = (vin - x1)/R1 ; out-stage: C2 dx2/dt = (G*(vin - x1) - x2)/R2
A2 = [[-1 / (R1 * C1), 0], [-G / (R2 * C2), -1 / (R2 * C2)]]
B2 = [[1 / (R1 * C1)], [G / (R2 * C2)]]
C2m = [[0, 1]]
H2 = lambda f: freq_resp(A2, B2, C2m, [[0]], 2 * pi * f)  # noqa: E731
fL = 1 / (2 * pi * R1 * C1)
fH = 1 / (2 * pi * R2 * C2)
v.check("Ex 07-07.2a", fL)
v.check("Ex 07-07.2b", fH / 1e3)
fmid = math.sqrt(fL * fH)
v.check("Ex 07-07.2n", fmid)
mid = abs(H2(fmid))
v.check("Ex 07-07.2c", dB(G), tol=0.005)
v.assert_true("midband within 0.01 dB of 40 dB", abs(dB(mid) - 40) < 0.01)
v.check("Ex 07-07.2d", dB(H2(fL / 10)))
v.check("Ex 07-07.2e", deg(H2(fL / 10)))
v.check("Ex 07-07.2f", dB(H2(fL)))
v.check("Ex 07-07.2g", deg(H2(fL)))
v.check("Ex 07-07.2h", dB(H2(1e3)))
v.check("Ex 07-07.2i", deg(H2(1e3)))
v.check("Ex 07-07.2j", deg(H2(fH)))
v.check("Ex 07-07.2k", 40 - 20 * math.log10(100e3 / fH))
v.check("Ex 07-07.2l", dB(H2(100e3)))
v.check("Ex 07-07.2m", deg(H2(100e3)))
v.assert_true("phase zero at geometric center", abs(deg(H2(fmid))) < 1e-9)
g3 = lambda f: abs(H2(f)) - G / math.sqrt(2)  # noqa: E731
f1, f2 = brentq(g3, 1, fmid), brentq(g3, fmid, 1e7)
v.check("Ex 07-07.2o", f1)
v.check("Ex 07-07.2p", f2 / 1e3)
v.check("Ex 07-07.2q", (f2 - f1) / 1e3)

# ================================================================================ Example 3 (state equations of 07-03)
L, Rs, C = 4.7e-6, 30e-3, 22e-6


def lc(RL, damp=None):
    """States (iL, v[, vCd]); input vin; output v."""
    if damp is None:
        A = [[-Rs / L, -1 / L], [1 / C, -1 / (RL * C)]]
        return A, [[1 / L], [0]], [[0, 1]], [[0]]
    Rd, Cd = damp
    A = [[-Rs / L, -1 / L, 0],
         [1 / C, -1 / (RL * C) - 1 / (Rd * C), 1 / (Rd * C)],
         [0, 1 / (Rd * Cd), -1 / (Rd * Cd)]]
    return A, [[1 / L], [0], [0]], [[0, 1, 0]], [[0]]


def lc_H(RL, f, damp=None):
    return freq_resp(*lc(RL, damp), 2 * pi * f)


A3 = np.array(lc(10)[0])
eig = np.linalg.eigvals(A3)
w0 = math.sqrt(np.prod(eig).real)
zeta = -eig.real.mean() / w0
v.check("Ex 07-07.3a", dB(lc_H(10, 1e-3)))
v.check("Ex 07-07.3b", w0 / 2 / pi / 1e3)
v.check("Ex 07-07.3c", zeta)
v.check("Ex 07-07.3d", 1 / (2 * zeta))
f0 = w0 / 2 / pi
v.check("Ex 07-07.3e", dB(lc_H(10, f0)))
v.check("Ex 07-07.3f", 20 * math.log10(1 / (2 * zeta)))
pk = minimize_scalar(lambda lf: -abs(lc_H(10, 10**lf)), bounds=(3.5, 5), method="bounded", options={"xatol": 1e-13})
v.check("Ex 07-07.3g", dB(lc_H(10, 10**pk.x)))
v.check("Ex 07-07.3h", 10**pk.x / 1e3)
v.check("Ex 07-07.3i", deg(lc_H(10, f0)))
K3 = 10 / 10.03
v.check("Ex 07-07.3j", dB(K3) - 40 * math.log10(500e3 / f0))
v.check("Ex 07-07.3k", dB(lc_H(10, 500e3)))
v.check("Ex 07-07.3l", dB(lc_H(10, 100e3)))
pk100 = minimize_scalar(lambda lf: -abs(lc_H(100, 10**lf)), bounds=(3.5, 5), method="bounded", options={"xatol": 1e-13})
v.check("Ex 07-07.3m", dB(lc_H(100, 10**pk100.x)))
v.check("Ex 07-07.3n", 10**pk100.x / 1e3)
v.check("Ex 07-07.3o", 10 * abs(lc_H(10, 10**pk.x)))
v.check("Ex 07-07.3p", abs(lc_H(10, 10**pk.x)))
eig100 = np.linalg.eigvals(np.array(lc(100)[0]))
zeta100 = -eig100.real.mean() / math.sqrt(np.prod(eig100).real)
v.check("Ex 07-07.3q", zeta100)
v.check("Ex 07-07.3r", 1 / (2 * zeta100))
# lock-in confirmation of the peak gain by integrating the state equations into steady state
fpk = 10**pk.x
wpk = 2 * pi * fpk
A, B, Cm, _ = (np.array(m, dtype=float) for m in lc(10))
sol = solve_ivp(lambda t, x: A @ x + B[:, 0] * math.cos(wpk * t), (0, 120 / fpk), [0.0, 0.0], method="DOP853",
                rtol=1e-10, atol=1e-13, dense_output=True, max_step=1 / (fpk * 200))
tt = np.linspace(100 / fpk, 120 / fpk, 40000, endpoint=False)
ph = 2 * np.mean(sol.sol(tt)[1] * np.exp(-1j * wpk * tt))
v.assert_true("lock-in peak gain matches frequency response", abs(abs(ph) - abs(lc_H(10, fpk))) < 2e-3)
# 07-03's turn-on peak, by integrating the step response
st = solve_ivp(lambda t, x: A @ x + B[:, 0] * 5.0, (0, 2e-4), [0.0, 0.0], method="DOP853", rtol=1e-11, atol=1e-13,
               max_step=1e-7)
v.check("N 07-07.ab", st.y[1].max())

# ================================================================================ Example 4
fp, fz = 1e6, 10e6
HA = tf(np.array([1 / (2 * pi * fz), 1]), np.array([1 / (2 * pi * fp), 1]))
HB = tf(np.array([-1 / (2 * pi * fz), 1]), np.array([1 / (2 * pi * fp), 1]))
for f, im, ia, ib in [(1e6, "a", "d", "e"), (10e6, "b", "f", "g"), (100e6, "c", "h", "i")]:
    s = 2j * pi * f
    v.check(f"Ex 07-07.4{im}", dB(HA(s)))
    v.assert_true(f"equal magnitudes at {f:g} Hz", abs(abs(HA(s)) - abs(HB(s))) < 1e-12)
    v.check(f"Ex 07-07.4{ia}", deg(HA(s)))
    v.check(f"Ex 07-07.4{ib}", deg(HB(s)))
v.check("Ex 07-07.4j", deg(cmath.exp(-2j * pi * 100e6 * 1e-9)), tol=0.005)


def bode_phase(H, w0):
    """Gain-phase integral: phase (rad) at w0 from ln|H| alone (minimum-phase assumption)."""
    def dAdu(u):
        h = 1e-5
        return (math.log(abs(H(1j * w0 * math.exp(u + h)))) - math.log(abs(H(1j * w0 * math.exp(u - h))))) / (2 * h)

    def integrand(u):
        return dAdu(u) * math.log(1 / math.tanh(abs(u) / 2)) if u != 0 else 0.0

    val = quad(integrand, -40, 0, limit=400, points=[0])[0] + quad(integrand, 0, 40, limit=400)[0]
    return val / pi


HAw = lambda s: (1 + s / (2 * pi * fz)) / (1 + s / (2 * pi * fp))  # noqa: E731
HBw = lambda s: (1 - s / (2 * pi * fz)) / (1 + s / (2 * pi * fp))  # noqa: E731
for f in (1e6, 10e6, 100e6):
    w = 2 * pi * f
    pr = math.degrees(bode_phase(HAw, w))
    v.assert_true(f"Bode integral recovers min-phase phase at {f:g} Hz", abs(pr - deg(HAw(1j * w))) < 0.05)
    v.assert_true(f"Bode integral cannot recover RHP-zero phase at {f:g} Hz", abs(pr - deg(HBw(1j * w))) > 10)
area = quad(lambda u: math.log(1 / math.tanh(u / 2)), 0, 50, limit=200)[0] * 2
v.assert_true("weight area = pi^2/2", abs(area - pi**2 / 2) < 1e-8)

# ================================================================================ Example 5 (op-amp state model)


def opamp_cl(A0, fa, beta, inverting=False):
    """State x = op-amp internal pole node; vout = x. dx/dt = wa (A0 (v+ - v-) - x)."""
    wa = 2 * pi * fa
    if not inverting:
        # v+ = vin, v- = beta vout
        A = [[-wa * (1 + A0 * beta)]]
        B = [[wa * A0]]
    else:
        # v+ = 0, v- = (1-beta) vin + beta vout  (Rf/(Rf+Rg) * vin + Rg/(Rf+Rg) * vout)
        A = [[-wa * (1 + A0 * beta)]]
        B = [[-wa * A0 * (1 - beta)]]
    return A, B, [[1]], [[0]]


def bw3(sys_, f_lo=1, f_hi=1e9):
    g0 = abs(freq_resp(*sys_, 2 * pi * f_lo))
    return brentq(lambda f: abs(freq_resp(*sys_, 2 * pi * f)) - g0 / math.sqrt(2), f_lo, f_hi), g0


GBW = 10e6
A0t, A0m = 10 ** (130 / 20), 10 ** (104 / 20)
v.check("Ex 07-07.5a", GBW / A0t)
v.check("Ex 07-07.5b", GBW / A0m)
bwt, gt = bw3(opamp_cl(A0t, GBW / A0t, 0.01))
bwm, gm = bw3(opamp_cl(A0m, GBW / A0m, 0.01))
v.check("Ex 07-07.5c", bwt / 1e3)
v.check("Ex 07-07.5d", 100 - gt)
v.check("Ex 07-07.5e", bwm / 1e3)
v.check("Ex 07-07.5f", 100 - gm)
bwi, gi = bw3(opamp_cl(A0t, GBW / A0t, 1 / 101, inverting=True))
v.check("Ex 07-07.5g", bwi / 1e3)
v.assert_true("inverting gain near -100", abs(gi - 100) < 0.01)
bw10, _ = bw3(opamp_cl(A0t, GBW / A0t, 0.1))
v.check("Ex 07-07.5h", bw10 / 1e6)
# two cascaded +10 stages: product of responses
H10 = lambda f: freq_resp(*opamp_cl(A0t, GBW / A0t, 0.1), 2 * pi * f)  # noqa: E731
g00 = abs(H10(1)) ** 2
fc2 = brentq(lambda f: abs(H10(f)) ** 2 - g00 / math.sqrt(2), 1e3, 1e8)
v.check("Ex 07-07.5i", fc2 / 1e3)

# ================================================================================ Example 6
tau1 = 1e-9 / math.log(9)
tau2 = 1 / (2 * pi * 200e6)
tr1 = rise_time([[-1 / tau2]], [[1 / tau2]], [[1]], 20 * tau2)
v.check("Ex 07-07.6a", tr1 * 200e6)
v.check("Ex 07-07.6b", tr1 * 1e9)
A6 = [[-1 / tau1, 0], [1 / tau2, -1 / tau2]]
tr2 = rise_time(A6, [[1 / tau1], [0]], [[0, 1]], 20 * (tau1 + tau2))
v.check("Ex 07-07.6c", tr2 * 1e9)
rss = math.hypot(1e-9, tr1)
v.check("Ex 07-07.6d", rss * 1e9)
v.check("Ex 07-07.6e", (tr2 - rss) / tr2 * 100)
v.check("Ex 07-07.6f", (1 - abs(1 / (1 + 0.2j))) * 100)
v.check("Ex 07-07.6g", (1 - abs(1 / (1 + 1j))) * 100)

# ================================================================================ Numbers to know (section 7)
v.check("N 07-07.a", dBp((1.0**2 / 50) / 1e-3))
v.check("N 07-07.b", math.sqrt(1e-3 * 600) * 10 ** (4 / 20))
v.check("N 07-07.c", math.sqrt(1e-3 * 600))
v.check("N 07-07.d", dB(math.e))
v.check("N 07-07.e", math.log(10 ** (1 / 20)))
v.check("N 07-07.f", dB(1 / (1 + 2j)) + 20 * math.log10(2))
v.check("N 07-07.g", dB(1 / (1 + 10j)) + 20)
v.check("N 07-07.h", math.degrees(math.atan(0.1)))
dphi = lambda H, w: (deg(H(w * 10**1e-6)) - deg(H(w * 10**-1e-6))) / 2e-6  # noqa: E731  degrees per decade
v.check("N 07-07.i", -dphi(lambda w: 1 / (1 + 1j * w), 1.0))
v.check("N 07-07.j", -dphi(lambda w: 1 / (1 + 2j * w - w**2), 1.0))
v.check("N 07-07.k", dB(1 / (1 + 2j * 0.1 - 1)))
v.check("N 07-07.l", -360 * 10e6 * 1e-9)
for n, ident in ((2, "m"), (3, "n"), (4, "o")):
    v.check(f"N 07-07.{ident}", brentq(lambda x: (1 + x * x) ** (-n / 2) - 1 / math.sqrt(2), 0.01, 1))
# Gaussian: step = Phi(t/sigma); 10-90 = 2*Phi^-1(0.9) sigma ; |H(f)| = exp(-2 pi^2 sigma^2 f^2)
z90 = math.sqrt(2) * erfinv(0.8)
f3g = brentq(lambda f: math.exp(-2 * pi**2 * f**2) - 1 / math.sqrt(2), 0.01, 1)
v.check("N 07-07.p", 2 * z90 * f3g)
v.check("N 07-07.r", 2 * z90)
step_bw = lambda x: 0.5 + sici(x)[0] / pi  # noqa: E731  ideal low-pass step vs x = 2 pi fc t
x10 = brentq(lambda x: step_bw(x) - 0.1, -5, 0)
x90 = brentq(lambda x: step_bw(x) - 0.9, 0, 5)
v.check("N 07-07.q", (x90 - x10) / (2 * pi))
worst = 0.0
for q in (1.0001, 1.1, 1.3):
    trq = rise_time([[-1.0, 0], [1 / q, -1 / q]], [[1.0], [0]], [[0, 1]], 30 * (1 + q))
    worst = max(worst, (trq - math.log(9) * math.hypot(1, q)) / trq * 100)
v.check("N 07-07.s", worst)
v.check("N 07-07.t", math.log(9) / (2 * pi) / 1e-9 / 1e6, tol=1)


def two_pole_loop(r):
    """Loop T = wt/(s(1+s/w2)) with wt = 1, w2 = r. Returns crossover, PM, closed-loop zeta, peak dB."""
    T = lambda w: 1 / (1j * w * (1 + 1j * w / r))  # noqa: E731
    wc = brentq(lambda w: abs(T(w)) - 1, 1e-3, 1e3)
    pm = 180 + deg(T(wc))
    Hcl = lambda w: T(w) / (1 + T(w))  # noqa: E731
    res = minimize_scalar(lambda lw: -abs(Hcl(10**lw)), bounds=(-3, 2), method="bounded", options={"xatol": 1e-12})
    peak = max(abs(Hcl(10**res.x)), abs(Hcl(1e-6)))
    poles = np.roots([1 / r, 1, 1])  # s^2/r + s + 1 = 0 -> closed loop char. poly
    w0 = math.sqrt(abs(np.prod(poles)))
    zeta = -poles.real.mean() / w0
    return wc, pm, zeta, dB(peak) - dB(Hcl(1e-6)), 10**res.x / w0


wc1, pm1, z1, pk1, fr1 = two_pole_loop(1.0)
v.check("N 07-07.u", wc1)
v.check("N 07-07.v", pm1)
v.check("N 07-07.w", pk1)
v.check("N 07-07.x", 100 * math.exp(-pi * z1 / math.sqrt(1 - z1 * z1)), tol=0.5)
wc2, pm2, z2, pk2, _ = two_pole_loop(2.0)
v.check("N 07-07.y", pm2)
r30 = brentq(lambda r: two_pole_loop(r)[1] - 30, 0.05, 1)
_, _, z30, pk30, _ = two_pole_loop(r30)
v.check("N 07-07.z", z30)
v.check("N 07-07.aa", pk30)

# ================================================================================ Practitioner lens (section 9)
v.check("PL 07-07.a", 2 ** (30 // 10 + 1))
v.check("PL 07-07.b", 2 ** (60 // 10 + 1))
v.assert_true("128 is 'more than a hundred'", 2 ** 7 > 100)
v.check("PL 07-07.c", 200e6 * 2.3e-9)
v.check("PL 07-07.d", 1e9 * 450e-12)
v.check("PL 07-07.e", 1.5e9 * 333e-12)

# ================================================================================ Problems
v.check("07-07.1a", dBp(2))
v.check("07-07.1b", dBp(0.5))
v.check("07-07.1c", dBp(1000))
v.check("07-07.1d", dB(2))
v.check("07-07.1e", dB(0.1))
v.check("07-07.1f", dB(math.sqrt(2)))
v.check("07-07.1g", dBp(1 / 1e-3))
v.check("07-07.1h", dBp(1e-6 / 1e-3))
v.check("07-07.1i", dB(1e-3))
v.check("07-07.1j", math.exp(-6 / 20 * LN10))
v.check("07-07.1k", math.exp(13 / 10 * LN10))
v.check("07-07.2a", dB(math.e))
v.check("07-07.2b", math.log(10 ** (20 / 20)))
v.check("07-07.2c", 10 * math.log(10) / math.log(2))
k2 = 10 / dB(2)
v.check("07-07.2d", k2)
v.check("07-07.2e", k2 * 90)
v.check("07-07.2f", 180 - k2 * 90)
# P3: straight-line phase
P = lambda x: 1 / (1 + 1j * x)  # noqa: E731
line = lambda x: 0.0 if x <= 0.1 else (-90.0 if x >= 10 else -45 * (1 + math.log10(x)))  # noqa: E731
for x, im, ip in [(0.1, "a", "g"), (0.5, "b", "h"), (1, "c", "i"), (2, "d", "j"), (10, "e", "k")]:
    v.check(f"07-07.3{im}", dB(P(x)))
    v.check(f"07-07.3{ip}", deg(P(x)))
v.check("07-07.3f", dB(P(2)) + 20 * math.log10(2))
v.check("07-07.3l", deg(P(0.1)) - line(0.1))
v.check("07-07.3m", deg(P(0.5)) - line(0.5))
# P4
num4 = 1000 * np.array([1, 10])
den4 = np.polymul([1, 100], [1, 1e4])
H4 = tf(num4, den4)
v.check("07-07.4a", dB(H4(1e-6)))


def asym4(w):
    corners = [(10, +1), (100, -1), (1e4, -1)]
    a = dB(H4(1e-9))
    for c, sgn in corners:
        if w > c:
            a += sgn * 20 * math.log10(w / c)
    return a


for w, ia, ie, ip in [(1, None, "e", "i"), (50, "b", "f", "j"), (1000, "c", "g", "k"), (1e5, "d", "h", "l")]:
    if ia:
        v.check(f"07-07.4{ia}", asym4(w))
    v.check(f"07-07.4{ie}", dB(H4(1j * w)))
    v.check(f"07-07.4{ip}", deg(H4(1j * w)))
lead = minimize_scalar(lambda lw: -deg(H4(1j * 10**lw)), bounds=(0, 3), method="bounded", options={"xatol": 1e-12})
v.check("07-07.4m", deg(H4(1j * 10**lead.x)))
v.check("07-07.4n", 10**lead.x)
v.check("07-07.4o", math.degrees(math.asin(9 / 11)))
v.check("07-07.4p", asym4(50) - dB(H4(50j)))
v.check("07-07.4q", math.degrees(math.asin(9 / 11)) - deg(H4(1j * 10**lead.x)))
# P5: nodal solve of the lead network
R1, R2, C5 = 9e3, 1e3, 10e-9


def H5(f):
    s = 2j * pi * f
    Y1 = 1 / R1 + s * C5
    return Y1 / (Y1 + 1 / R2)


v.check("07-07.5a", 1 / (2 * pi * R1 * C5) / 1e3)
v.check("07-07.5b", 1 / (2 * pi * (R1 * R2 / (R1 + R2)) * C5) / 1e3)
v.check("07-07.5c", dB(H5(1e-3)))
v.check("07-07.5d", dB(H5(1e12)), tol=0.005)
lead5 = minimize_scalar(lambda lf: -deg(H5(10**lf)), bounds=(2, 6), method="bounded", options={"xatol": 1e-12})
v.check("07-07.5e", deg(H5(10**lead5.x)))
v.check("07-07.5f", 10**lead5.x / 1e3)
v.check("07-07.5g", dB(H5(10**lead5.x)))
# P6: second-order low-pass via state space (x1 = y, x2 = y'), w0 = 2 pi 1 kHz
w06 = 2 * pi * 1e3


def H6(z, f):
    A = [[0, 1], [-(w06**2), -2 * z * w06]]
    return freq_resp(A, [[0], [w06**2]], [[1, 0]], [[0]], 2 * pi * f)


for z, ia in ((0.1, "a"), (0.5, "b"), (1 / math.sqrt(2), "c")):
    v.check(f"07-07.6{ia}", dB(H6(z, 1e3)), tol=0.005)
for z, i5, i2 in ((0.1, "d", "e"), (0.5, "f", "g"), (1 / math.sqrt(2), "h", "i")):
    v.check(f"07-07.6{i5}", deg(H6(z, 500)))
    ph2 = deg(H6(z, 2e3))
    v.check(f"07-07.6{i2}", ph2 if ph2 < 0 else ph2 - 360)
pk6 = minimize_scalar(lambda lf: -abs(H6(0.1, 10**lf)), bounds=(2.5, 3.5), method="bounded", options={"xatol": 1e-13})
v.check("07-07.6j", dB(H6(0.1, 10**pk6.x)))
v.check("07-07.6k", 10**pk6.x)
v.check("07-07.6l", abs(H6(0.1, 10**pk6.x)))
# P7
K7 = 10 ** (32 / 20)
H7 = tf([K7], np.polymul([1 / 2e3, 1], [1 / 50e3, 1]))  # in units of f (Hz), s -> j f
v.check("07-07.7a", K7)
v.check("07-07.7b", 32 - 20 * math.log10(10 / 2))
v.check("07-07.7c", dB(H7(1j * 10e3)))
v.check("07-07.7d", deg(H7(1j * 10e3)))
a50 = 32 - 20 * math.log10(25)
fa7 = 50e3 * 10 ** (a50 / 40)
v.check("07-07.7e", fa7 / 1e3)
fc7 = brentq(lambda f: abs(H7(1j * f)) - 1, 1e3, 1e7)
v.check("07-07.7f", fc7 / 1e3)
ph7 = unwrap_deg([H7(1j * f) for f in np.linspace(0, fc7, 2000)])[-1]
v.check("07-07.7g", ph7)
v.check("07-07.7h", 180 + ph7)
v.check("07-07.7i", (fa7 - fc7) / fc7 * 100)
# P8
A08, fa8 = 1e5, 1e6 / 1e5
bw8, _ = bw3(opamp_cl(A08, fa8, 0.1))
v.check("07-07.8a", bw8 / 1e3)
bw8i, _ = bw3(opamp_cl(A08, fa8, 1 / 11, inverting=True))
v.check("07-07.8b", bw8i / 1e3)
tau8 = 1 / (2 * pi * fa8 * (1 + A08 * 0.1))
v.check("07-07.8c", rise_time([[-1 / tau8]], [[1 / tau8]], [[1]], 20 * tau8) * 1e6)
v.check("07-07.8d", math.floor(1e6 / 20e3))
# P9
for n, ident in ((2, "a"), (3, "b"), (4, "c")):
    v.check(f"07-07.9{ident}", brentq(lambda x: (1 + x * x) ** (-n / 2) - 1 / math.sqrt(2), 0.01, 1))
v.check("07-07.9d", 1e6 / brentq(lambda x: (1 + x * x) ** (-1.5) - 1 / math.sqrt(2), 0.01, 1) / 1e6)
# P10
for f, ident in ((10e6, "a"), (100e6, "b"), (500e6, "c")):
    v.check(f"07-07.10{ident}", -360 * f * 2e-9)
wp10 = 2 * pi * 1e3
gd = lambda w: -(cmath.phase(1 / (1 + 1j * (w + 1e-3) / wp10)) - cmath.phase(1 / (1 + 1j * (w - 1e-3) / wp10))) / 2e-3  # noqa: E731
v.check("07-07.10d", gd(1e-2) * 1e6)
v.check("07-07.10e", gd(wp10) * 1e6)
# P11
B1, B2 = 350e6, 500e6
H11 = lambda f: 1 / ((1 + 1j * f / B1) * (1 + 1j * f / B2))  # noqa: E731
f11 = brentq(lambda f: abs(H11(f)) - 1 / math.sqrt(2), 1e6, 1e9)
v.check("07-07.11a", f11 / 1e6)
est = 1 / math.sqrt(1 / B1**2 + 1 / B2**2)
v.check("07-07.11b", est / 1e6)
t1, t2 = 1 / (2 * pi * B1), 1 / (2 * pi * B2)
tr11 = rise_time([[-1 / t1, 0], [1 / t2, -1 / t2]], [[1 / t1], [0]], [[0, 1]], 20 * (t1 + t2))
v.check("07-07.11c", tr11 * 1e9)
rs1, rs2 = math.log(9) * t1, math.log(9) * t2
v.check("07-07.11d", math.hypot(rs1, rs2) * 1e9)
v.check("07-07.11e", (est - f11) / est * 100)
v.check("07-07.11f", (tr11 - math.hypot(rs1, rs2)) / math.hypot(rs1, rs2) * 100)
v.check("07-07.11g", rs1 * 1e9)
v.check("07-07.11h", rs2 * 1e9)
# P12
sig = 1e-3
Zw = lambda f: sig * (2j * pi * f) ** -0.5  # noqa: E731
v.check("07-07.12a", abs(Zw(1)) * 1e3)
v.check("07-07.12b", abs(Zw(100)) * 1e3)
v.check("07-07.12c", dB(Zw(10)) - dB(Zw(1)), tol=0.005)
v.check("07-07.12d", deg(Zw(3.7)), tol=0.005)
v.assert_true("Warburg: Re Z = -Im Z", abs(Zw(5).real + Zw(5).imag) < 1e-15)
v.assert_true("Bode integral gives -45 deg for k = -1/2",
              abs(math.degrees(bode_phase(lambda s: s**-0.5, 1.0)) + 45) < 0.01)
# P13
v.check("07-07.13a", wc1)
v.check("07-07.13b", pm1)
v.check("07-07.13c", z1)
v.check("07-07.13d", pk1)
v.check("07-07.13e", fr1)
v.check("07-07.13k", 10 ** (pk1 / 20))
v.check("07-07.13f", pm2)
v.check("07-07.13g", z2)
v.assert_true("no peak for r = 2", pk2 < 1e-6)
r55 = brentq(lambda r: two_pole_loop(r)[1] - 55, 0.2, 3)
_, _, z55, pk55, _ = two_pole_loop(r55)
v.check("07-07.13h", z55)
v.check("07-07.13i", pk55)
v.check("07-07.13j", 100 * math.exp(-pi * z55 / math.sqrt(1 - z55**2)))
# P14
Rd = math.sqrt(L / C)
v.check("07-07.14a", Rd)
damp = (Rd, 4 * C)
v.check("07-07.14b", dB(lc_H(10, f0)))
v.check("07-07.14c", dB(lc_H(10, f0, damp)))
pk14 = minimize_scalar(lambda lf: -abs(lc_H(10, 10**lf, damp)), bounds=(3, 5), method="bounded", options={"xatol": 1e-13})
v.check("07-07.14d", dB(lc_H(10, 10**pk14.x, damp)))
v.check("07-07.14e", 10**pk14.x / 1e3)
v.check("07-07.14f", dB(lc_H(10, 500e3, damp)))
v.check("07-07.14g", 5**2 / Rd, tol=0.5)
v.check("07-07.14h", dB(lc_H(10, 10**pk.x)) - dB(lc_H(10, 10**pk14.x, damp)))
v.check("07-07.14i", 1 / (2 * pi * 500e3 * C))

# ================================================================================ Lab handout
lab = two_pole_loop(1.0)
v.check("Lab 07-07.a", lab[1])
v.check("Lab 07-07.b", lab[3])
v.check("Lab 07-07.c", lab[4] * 10.0)  # w0 = wt = 10 MHz in the lab
v.check("Lab 07-07.d", 2 * z90 * f3g)
v.check("Lab 07-07.e", math.log(9) / (2 * pi))
v.check("Lab 07-07.f", (x90 - x10) / (2 * pi))
# P15: minimum- versus non-minimum-phase zero (unwrapped phase along a dense sweep; simulated step)
den15 = np.polymul([1e-3, 1], [1e-5, 1])
H15 = {1: signal.lti(10 * np.array([1e-4, 1]), den15), 2: signal.lti(10 * np.array([-1e-4, 1]), den15)}
wgrid = np.logspace(0, 8, 80001)
ph15 = {k: np.degrees(np.unwrap(np.angle(signal.freqresp(h, wgrid)[1]))) for k, h in H15.items()}
for wv, (ka, kb) in ((1e3, ("07-07.15a", "07-07.15b")), (1e4, ("07-07.15c", "07-07.15d")), (1e5, ("07-07.15e", "07-07.15f"))):
    i = int(np.argmin(abs(wgrid - wv)))
    v.check(ka, ph15[1][i])
    v.check(kb, ph15[2][i])
v.check("07-07.15g", round(ph15[2][-1] / 90) * 90)
assert np.allclose(abs(signal.freqresp(H15[1], wgrid)[1]), abs(signal.freqresp(H15[2], wgrid)[1]))
ts15 = np.linspace(0, 0.02, 400001)
_, y15 = signal.step(H15[2], T=ts15)
v.check("07-07.15h", y15[0])
v.check("07-07.15i", (y15[1] - y15[0]) / (ts15[1] - ts15[0]), tol=500)
v.check("07-07.15j", y15[-1])
v.assert_true("P15 H2 step response dips below zero first", y15[:2000].min() < -0.1)

v.finish()
