#!/usr/bin/env python3
"""Verify every number in the Course 07 final-exam solutions.

Each value is recomputed independently of the hand method in the solutions:
- Transients are integrated numerically (solve_ivp) from initial states found by DC circuit solves. Peaks,
  crossings and settling times are located on the simulated waveforms. Rates, damping and poles come from
  the eigenvalues of the state matrices.
- AC answers come from a complex modified-nodal-analysis solver that handles coupled inductors and
  controlled sources. Thevenin equivalents use open-circuit and test-source solves; the maximum-power load
  is found by numerical optimization.
- Power and harmonic answers are averaged over sampled waveforms, and the Fourier coefficient is taken by FFT.
- Filter designs are found by solving the circuit's response for the component values, and the
  Butterworth order comes from scipy's buttord.
- S-parameters come from a 50-ohm-terminated simulation, and the L-section by root-finding on Z_in = 50.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, fsolve, minimize, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("07-exam", HERE.parent / "exam" / "solutions.md")
TAU = 2 * math.pi
DEG = 180 / math.pi
RT = dict(rtol=1e-10, atol=1e-13, dense_output=True, method="LSODA")


def mna(elements, w):
    """Complex MNA at angular frequency w (w = 0 for DC: C open, L short). Elements (name, kind, a, b, val):
    R, C, L (val = ohm, F, H); V, I (complex value; I flows a -> b through the source, i.e. into b);
    E: v_a - v_b = mu (v_c - v_d) with val = (c, d, mu); K: coupling with val = (L1name, L2name, M).
    Inductors and voltage sources carry branch currents (a -> b through the element)."""
    nodes = sorted({n for e in elements if e[1] != "K" for n in (e[2], e[3]) if n != "0"})
    idx = {n: k for k, n in enumerate(nodes)}
    br = [e for e in elements if e[1] in "VLE"]
    bidx = {e[0]: len(nodes) + k for k, e in enumerate(br)}
    n = len(nodes) + len(br)
    M, z = np.zeros((n, n), complex), np.zeros(n, complex)

    def stamp_y(a, b, y):
        for p, q, s in ((a, a, 1), (b, b, 1), (a, b, -1), (b, a, -1)):
            if p != "0" and q != "0":
                M[idx[p], idx[q]] += s * y

    for name, kind, a, b, val in elements:
        if kind == "R":
            stamp_y(a, b, 1 / val)
        elif kind == "C":
            if w != 0:
                stamp_y(a, b, 1j * w * val)
        elif kind == "I":
            if a != "0":
                z[idx[a]] -= val
            if b != "0":
                z[idx[b]] += val
        elif kind in "VLE":
            k = bidx[name]
            for node, s in ((a, 1), (b, -1)):
                if node != "0":
                    M[idx[node], k] += s
                    M[k, idx[node]] += s
            if kind == "V":
                z[k] = val
            elif kind == "L":
                M[k, k] -= 1j * w * val
            else:
                c, d, mu = val
                for node, s in ((c, -mu), (d, mu)):
                    if node != "0":
                        M[k, idx[node]] += s
    for name, kind, a, b, val in elements:
        if kind == "K":
            l1, l2, mutual = val
            M[bidx[l1], bidx[l2]] -= 1j * w * mutual
            M[bidx[l2], bidx[l1]] -= 1j * w * mutual
    x = np.linalg.solve(M, z)
    volt = {"0": 0.0, **{nd: x[idx[nd]] for nd in nodes}}
    cur = {e[0]: x[bidx[e[0]]] for e in br}
    return volt, cur


def crossing(sol, f, lo, hi, n=4000):
    """First root of f(sol(t)) in [lo, hi], bracketed on a grid then refined."""
    ts = np.linspace(lo, hi, n)
    vals = np.array([f(sol(t)) for t in ts])
    k = int(np.nonzero(np.sign(vals[:-1]) != np.sign(vals[1:]))[0][0])
    return brentq(lambda t: f(sol(t)), ts[k], ts[k + 1], xtol=1e-15)


def extremum(sol, f, lo, hi, n=4000, sign=1):
    """Location and value of the largest sign*f(sol(t)) on [lo, hi], refined by bounded minimization."""
    ts = np.linspace(lo, hi, n)
    k = int(np.argmax([sign * f(sol(t)) for t in ts]))
    r = minimize_scalar(lambda t: -sign * f(sol(t)), bounds=(ts[max(k - 1, 0)], ts[min(k + 1, n - 1)]),
                        method="bounded", options={"xatol": 1e-15})
    return r.x, f(sol(r.x))


# ---- Q1 (07-01)
t = np.linspace(0, 2e-3, 2001)
v.check("X07.1a", 1e3 * np.mean(10e-6 * np.gradient(5 * t / 2e-3, t)))
t = np.linspace(0, 10e-6, 2001)
i_l = 3 * t / 10e-6
vl = 100e-6 * np.gradient(i_l, t)
v.check("X07.1b", np.mean(vl))
v.check("X07.1c", 1e6 * np.trapezoid(vl * i_l, t))
s1 = solve_ivp(lambda t, q: [(12 - q[0] / 4.7e-6 - q[0] / 2.2e-6) / 1.0], (0, 2e-4), [0.0], **RT)
qf = s1.y[0, -1]
v.check("X07.1d", 1e6 * qf / 12)
v.check("X07.1e", qf / 4.7e-6)
v.check("X07.1f", qf / 2.2e-6)


def droop(c):
    s = solve_ivp(lambda t, x: [-2.0 / c], (0, 1e-6), [1.0], **RT)
    return 1.0 - s.y[0, -1]


v.check("X07.1g", 1e6 * brentq(lambda c: droop(c) - 0.05, 1e-6, 1e-3))

# ---- Q2 (07-02)
R2_, C2_, V2_ = 10e3, 100e-9, 3.3
s2 = solve_ivp(lambda t, x: [(V2_ - x[0]) / (R2_ * C2_)], (0, 0.03), [0.0], **RT)
A2 = np.array([[-1 / (R2_ * C2_)]])
tau2 = -1 / np.linalg.eigvals(A2)[0].real
v.check("X07.2a", 1e3 * tau2)
v.check("X07.2b", s2.sol(2e-3)[0])
t10 = crossing(s2.sol, lambda x: x[0] - 0.1 * V2_, 0, 0.01)
t90 = crossing(s2.sol, lambda x: x[0] - 0.9 * V2_, 0, 0.01)
v.check("X07.2c", 1e3 * (t90 - t10))
f3 = brentq(lambda f: abs(1 / (1 + 1j * TAU * f * R2_ * C2_)) - 1 / math.sqrt(2), 1, 1e5)
v.check("X07.2d", f3)
v.check("X07.2e", (t90 - t10) * f3)
v.check("X07.2f", 1e3 * crossing(s2.sol, lambda x: (V2_ - x[0]) - V2_ / 2 ** 13, 1e-4, 0.03, n=20000))
tt = np.linspace(0, 0.03, 300001)
v.check("X07.2g", 1e9 * np.trapezoid((V2_ - s2.sol(tt)[0]) ** 2 / R2_, tt))

# ---- Q3 (07-02): DC states from MNA, then two simulated intervals
base3 = [("V1", "V", "1", "0", 12.0), ("R1", "R", "1", "a", 4e3), ("R2", "R", "a", "0", 12e3)]
vc0 = mna(base3, 0)[0]["a"].real
v.check("X07.3a", vc0)
v.check("X07.3b", mna(base3 + [("R3", "R", "a", "0", 6e3)], 0)[0]["a"].real)


def rhs3(closed):
    g = 1 / 4e3 + 1 / 12e3 + (1 / 6e3 if closed else 0.0)
    return lambda t, x: [(12 / 4e3 - g * x[0]) / 10e-6]


v.check("X07.3c", 1e3 / (1 / 10e-6 * (1 / 4e3 + 1 / 12e3 + 1 / 6e3)))
sa = solve_ivp(rhs3(True), (0, 0.04), [vc0], **RT)
v.check("X07.3d", 1e3 * sa.sol(0)[0] / 6e3)
v.check("X07.3e", 1e3 * 10e-6 * rhs3(True)(0, [vc0])[0])
v.check("X07.3f", 1e3 * crossing(sa.sol, lambda x: x[0] - 7, 0, 0.04))
v40 = sa.sol(0.04)[0]
v.check("X07.3g", v40)
v.check("X07.3h", 1e3 * 10e-6 / (1 / 4e3 + 1 / 12e3))
sb = solve_ivp(rhs3(False), (0.04, 0.1), [v40], **RT)
v.check("X07.3i", sb.sol(0.1)[0])

# ---- Q4 (07-03): series RLC, state (v_C, i)


def rlc4(R, L=1e-3, C=1e-6):
    return np.array([[0, 1 / C], [-1 / L, -R / L]])


ev = np.linalg.eigvals(rlc4(20.0))
w0 = abs(ev[0])
v.check("X07.4a", w0)
v.check("X07.4b", w0 / TAU)
v.check("X07.4c", -ev[0].real)
v.check("X07.4d", -ev[0].real / w0)
v.check("X07.4e", w0 / (2 * -ev[0].real))
v.check("X07.4f", abs(ev[0].imag))
v.check("X07.4g", abs(ev[0].imag) / TAU)


def sim4(R):
    A = rlc4(R)
    return solve_ivp(lambda t, x: A @ x + np.array([0, 10 / 1e-3]), (0, 1e-3), [0.0, 0.0], **RT)


s4 = sim4(20.0)
tp, vp = extremum(s4.sol, lambda x: x[0], 0, 3e-4)
v.check("X07.4h", 100 * (vp - 10) / 10)
v.check("X07.4i", vp)
v.check("X07.4j", 1e6 * tp)
v.check("X07.4m", brentq(lambda R: np.trace(rlc4(R)) ** 2 - 4 * np.linalg.det(rlc4(R)), 1, 200))


def overshoot(R):
    s = sim4(R)
    return (extremum(s.sol, lambda x: x[0], 0, 1e-3)[1] - 10) / 10


R5 = brentq(lambda R: overshoot(R) - 0.05, 30, 60, xtol=1e-9)
v.check("X07.4o", R5)
ev5 = np.linalg.eigvals(rlc4(R5))
v.check("X07.4n", -ev5[0].real / abs(ev5[0]))

# ---- Q5 (07-04): two-section RC ladder, state (v_C1, v_C2)
G, C5 = 1e-3, 1e-6
A5 = np.array([[-2 * G / C5, G / C5], [G / C5, -G / C5]])
B5 = np.array([G / C5, 0.0])
ladder = [("Vi", "V", "1", "0", 2.0), ("R1", "R", "1", "2", 1e3), ("R2", "R", "2", "3", 1e3),
          ("Rl", "R", "3", "0", 1e15)]
dc5 = mna(ladder, 0)[0]
x0 = np.array([dc5["2"].real, dc5["3"].real])
v.check("X07.5a", x0[1])
assert abs(x0[0] - x0[1]) < 1e-9
poles = np.sort(np.linalg.eigvals(A5).real)
poly = np.poly(A5)  # s^2 + 2 zeta w0 s + w0^2
v.check("X07.5b", poly[1] / (2 * math.sqrt(poly[2])))
v.check("X07.5c", poles[1])
v.check("X07.5d", poles[0])
xinf = -np.linalg.solve(A5, B5 * 5.0)
lam, V = np.linalg.eig(A5)
cvec = np.linalg.solve(V, x0 - xinf)
coef = {round(l.real): V[1, k] * cvec[k] for k, l in enumerate(lam)}
v.check("X07.5e", coef[round(poles[1])].real)
v.check("X07.5f", coef[round(poles[0])].real)
s5 = solve_ivp(lambda t, x: A5 @ x + B5 * 5.0, (0, 0.01), x0, **RT)
v.check("X07.5g", s5.sol(1e-3)[1])
v.check("X07.5h", s5.sol(2e-3)[1])
v.check("X07.5i", s5.sol(0)[1])
v.check("X07.5j", (A5 @ x0 + B5 * 5.0)[1])
v.check("X07.5k", xinf[1])

# ---- Q6 (07-05, 07-06): phasor MNA at 1e4 rad/s
w6 = 1e4
c6 = [("Vs", "V", "1", "0", 10.0), ("R1", "R", "1", "2", 20.0), ("L", "L", "2", "0", 10e-3),
      ("C", "C", "2", "3", 10e-6), ("R2", "R", "3", "0", 10.0)]
e6, i6 = mna(c6, w6)
v.check("X07.6a", (1j * w6 * 10e-3).imag)
v.check("X07.6b", (1 / (1j * w6 * 10e-6)).imag)
Is = -i6["Vs"]
Zin = 10.0 / Is
v.check("X07.6c", Zin.real)
v.check("X07.6d", Zin.imag)
Zp = e6["2"] / Is
v.check("X07.6p", Zp.real)
v.check("X07.6q", Zp.imag)
v.check("X07.6e", abs(e6["2"]))
v.check("X07.6f", np.angle(e6["2"]) * DEG)
IR2 = e6["3"] / 10.0
v.check("X07.6g", abs(IR2))
v.check("X07.6h", np.angle(IR2) * DEG)
v.check("X07.6i", 0.5 * abs(IR2) ** 2 * 10)
v.check("X07.6j", 0.5 * (10.0 * np.conj(Is)).real)
v.check("X07.6r", abs(Is))
v.check("X07.6s", np.angle(Is) * DEG)
v.check("X07.6t", 0.5 * abs(Is) ** 2 * 20)
open6 = c6[:4] + [("Rinf", "R", "3", "0", 1e15)]
Vth = mna(open6, w6)[0]["3"]
v.check("X07.6k", abs(Vth))
v.check("X07.6l", np.angle(Vth) * DEG)
test6 = [("Vs", "V", "1", "0", 0.0)] + c6[1:4] + [("It", "I", "0", "3", 1.0)]
Zth = mna(test6, w6)[0]["3"]
v.check("X07.6m", Zth.real)
v.check("X07.6n", Zth.imag)


def p_load(rx):
    zl = complex(*rx)
    ii = Vth / (Zth + zl)
    return -0.5 * abs(ii) ** 2 * zl.real


opt = minimize(p_load, [10.0, 0.0], method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-14})
v.check("X07.6o", -opt.fun)
assert abs(opt.x[0] - Zth.real) < 1e-4 and abs(opt.x[1] + Zth.imag) < 1e-4

# ---- Q7 (07-06): sampled 50 Hz waveforms
w7 = TAU * 50
t7 = np.linspace(0, 0.02, 20000, endpoint=False)
vt = 230 * math.sqrt(2) * np.cos(w7 * t7)


def rms(x):
    return math.sqrt(np.mean(x ** 2))


Iload = 10e3 / (230 * 0.75)
it = Iload * math.sqrt(2) * np.cos(w7 * t7 - math.acos(0.75))
P7 = np.mean(vt * it)
S7 = rms(vt) * rms(it)
v.check("X07.7a", S7 / 1e3)
v.check("X07.7b", math.sqrt(S7 ** 2 - P7 ** 2) / 1e3)
v.check("X07.7c", rms(it))


def pf_with(C):
    ic = C * np.gradient(vt, t7)
    tot = it + ic
    return np.mean(vt * tot) / (rms(vt) * rms(tot)), tot


C7 = brentq(lambda C: pf_with(C)[0] - 0.95, 1e-6, 600e-6, xtol=1e-14)
v.check("X07.7f", 1e6 * C7)
ic7 = C7 * np.gradient(vt, t7)
v.check("X07.7e", rms(vt) * rms(ic7) / 1e3)
tot7 = pf_with(C7)[1]
St = rms(vt) * rms(tot7)
v.check("X07.7d", math.sqrt(St ** 2 - np.mean(vt * tot7) ** 2) / 1e3)
v.check("X07.7g", rms(tot7))
v.check("X07.7l", (rms(tot7) / rms(it)) ** 2)
v.check("X07.7h", 100 * (1 - (rms(tot7) / rms(it)) ** 2))
ih = math.sqrt(2) * (10 * np.cos(w7 * t7) + 3 * np.cos(3 * w7 * t7) + 1.5 * np.cos(5 * w7 * t7))
v.check("X07.7i", rms(ih))
spec = np.abs(np.fft.rfft(ih)) / len(t7) * 2
v.check("X07.7j", 100 * math.sqrt(np.sum(spec[2:] ** 2)) / spec[1])
v.check("X07.7k", np.mean(vt * ih) / (rms(vt) * rms(ih)))

# ---- Q8 (07-07)
lead = signal.lti([1e-3, 1], [1e-4, 1])
_, Hl = signal.freqresp(lead, [1e3, 1e4])
v.check("X07.8a", 20 * np.log10(abs(Hl[0])))
v.check("X07.8b", 20 * np.log10(abs(Hl[1])))
ph = minimize_scalar(lambda lw: -np.angle(signal.freqresp(lead, [10 ** lw])[1][0]), bounds=(2, 5),
                     method="bounded", options={"xatol": 1e-12})
wm = 10 ** ph.x
v.check("X07.8c", wm)
v.check("X07.8d", -ph.fun * DEG)
v.check("X07.8e", 20 * np.log10(abs(signal.freqresp(lead, [wm])[1][0])))
A0, f1, f2 = 1e5, 10.0, 2e6
v.check("X07.8f", brentq(lambda f: abs(A0 / (1 + 1j * f / f1)) - 1, 1, 1e8) / 1e6)  # single-pole unity-gain f


def loop(f, beta):
    return beta * A0 / ((1 + 1j * f / f1) * (1 + 1j * f / f2))


for beta, kf, kp in ((1.0, "X07.8g", "X07.8h"), (0.1, "X07.8i", "X07.8j")):
    fc = brentq(lambda f: abs(loop(f, beta)) - 1, 1e3, 1e8, xtol=1e-9)
    v.check(kf, fc / 1e3)
    v.check(kp, 180 + np.angle(loop(fc, beta)) * DEG)

# ---- Q9 (07-08)
L9, C9, R9 = 10e-6, 1e-9, 5.0


def h9(f):
    e, _ = mna([("V", "V", "1", "0", 1.0), ("L", "L", "1", "2", L9), ("C", "C", "2", "3", C9),
                ("R", "R", "3", "0", R9)], TAU * f)
    return e["3"], e["2"] - e["3"]


f0_9 = brentq(lambda f: np.angle(h9(f)[0]), 1e6, 2.5e6, xtol=1e-6)
v.check("X07.9a", f0_9 / 1e6)
lo = brentq(lambda f: abs(h9(f)[0]) - 1 / math.sqrt(2), 1e6, f0_9)
hi = brentq(lambda f: abs(h9(f)[0]) - 1 / math.sqrt(2), f0_9, 3e6)
v.check("X07.9c", (hi - lo) / 1e3)
v.check("X07.9b", f0_9 / (hi - lo))
v.check("X07.9d", abs(h9(f0_9)[1]))
for f, kg, kp in ((1.5e6, "X07.9e", "X07.9f"), (1.7e6, "X07.9g", "X07.9h")):
    v.check(kg, 20 * np.log10(abs(h9(f)[0])))
    v.check(kp, np.angle(h9(f)[0]) * DEG)


def sk(f, c1, c2):
    els = [("Vi", "V", "in", "0", 1.0), ("R1", "R", "in", "A", 10e3), ("R2", "R", "A", "B", 10e3),
           ("C2", "C", "B", "0", c2), ("C1", "C", "A", "out", c1), ("E", "E", "out", "0", ("B", "out", 1e9))]
    return mna(els, TAU * f)[0]["out"]


def bw_err(cs):
    c1, c2 = cs[0] * 1e-9, cs[1] * 1e-9
    return [abs(sk(f, c1, c2)) ** 2 - 1 / (1 + (f / 1e3) ** 4) for f in (1e3, 2e3)]


c1n, c2n = fsolve(bw_err, [20.0, 10.0], xtol=1e-13)
v.check("X07.9i", c2n)
v.check("X07.9j", c1n)
v.check("X07.9k", 20 * np.log10(abs(sk(1e3, c1n * 1e-9, c2n * 1e-9))))
b2, a2 = signal.butter(2, TAU * 1e3, analog=True)
v.check("X07.9l", -20 * np.log10(abs(signal.freqs(b2, a2, [TAU * 3e3])[1][0])))
v.check("X07.9m", brentq(lambda n: 10 * np.log10(1 + 3 ** (2 * n)) - 40, 1, 10))
nmin, _ = signal.buttord(TAU * 1e3, TAU * 3e3, 3.0103, 40, analog=True)
v.check("X07.9n", nmin)
b5, a5 = signal.butter(5, TAU * 1e3, analog=True)
v.check("X07.9o", -20 * np.log10(abs(signal.freqs(b5, a5, [TAU * 3e3])[1][0])))

# ---- Q10 (07-09)
L1, L2, M10 = 4e-3, 1e-3, 1.8e-3
v.check("X07.10a", M10 / math.sqrt(L1 * L2))
wt = 1e3


def series(sign):
    els = [("V", "V", "1", "0", 1.0), ("La", "L", "1", "2", L1), ("Lb", "L", "2", "0", L2),
           ("K", "K", "x", "x", ("La", "Lb", sign * M10))]
    _, cur = mna(els, wt)
    return (1.0 / cur["V"] * -1).imag / wt


v.check("X07.10b", 1e3 * series(1))
v.check("X07.10c", 1e3 * series(-1))
w10 = TAU * 1e4
c10 = [("V", "V", "1", "0", 1.0), ("La", "L", "1", "0", L1), ("Lb", "L", "2", "0", L2),
       ("RL", "R", "2", "0", 50.0), ("K", "K", "x", "x", ("La", "Lb", M10))]
e10, i10 = mna(c10, w10)
Zin10 = 1.0 / i10["La"]
Zr = Zin10 - 1j * w10 * L1
v.check("X07.10d", Zr.real)
v.check("X07.10e", Zr.imag)
v.check("X07.10f", Zin10.imag)
assert abs(Zin10.real - Zr.real) < 1e-9
v.check("X07.10g", abs(i10["Lb"] / i10["La"]))


def ideal_zin(nratio):
    # ideal transformer: primary voltage = n * secondary voltage (E source); primary current = I2/n
    # (secondary current sensed by a zero-volt source and mirrored by a current source of gain 1/n)
    sec = mna([("Vs", "V", "s", "0", 1.0 / nratio), ("Vm", "V", "s", "x", 0.0), ("RL", "R", "x", "0", 8.0)], 0)
    i2 = sec[1]["Vm"]
    return 1.0 / (i2 / nratio)


v.check("X07.10h", brentq(lambda nr: ideal_zin(nr).real - 800, 1, 100))


def eff(x, pf=0.8):
    return x * 10e3 * pf / (x * 10e3 * pf + 80 + 200 * x ** 2)


v.check("X07.10i", 100 * eff(1.0))
xm = minimize_scalar(lambda x: -eff(x), bounds=(0.05, 2), method="bounded", options={"xatol": 1e-12})
v.check("X07.10j", xm.x)
v.check("X07.10k", -100 * xm.fun)

# ---- Q11 (07-10): T network by port tests
T = [("Ra", "R", "p1", "m", 10.0), ("Rb", "R", "m", "p2", 20.0), ("Rc", "R", "m", "0", 100.0)]
e = mna(T + [("I1", "I", "0", "p1", 1.0)], 0)[0]
v.check("X07.11a", e["p1"].real)
v.check("X07.11b", e["p2"].real)
z12 = mna(T + [("I2", "I", "0", "p2", 1.0)], 0)[0]
v.check("X07.11c", z12["p2"].real)
assert abs(z12["p1"] - e["p2"]) < 1e-12
# ABCD from tests: A = V1/V2 (I2 = 0), C = I1/V2 (I2 = 0), B = V1/(-I2) (V2 = 0), D = I1/(-I2) (V2 = 0)
o = mna(T + [("V1", "V", "p1", "0", 1.0), ("Ro", "R", "p2", "0", 1e15)], 0)
Aa, Ca = 1 / o[0]["p2"].real, -o[1]["V1"].real / o[0]["p2"].real
sh = mna(T + [("V1", "V", "p1", "0", 1.0), ("V2", "V", "p2", "0", 0.0)], 0)
Bb, Dd = 1 / sh[1]["V2"].real, -sh[1]["V1"].real / sh[1]["V2"].real
for k, val in (("X07.11d", Aa), ("X07.11e", Bb), ("X07.11f", Ca), ("X07.11g", Dd), ("X07.11h", Aa * Dd - Bb * Ca)):
    v.check(k, val)
ld = mna(T + [("V1", "V", "p1", "0", 1.0), ("RL", "R", "p2", "0", 50.0)], 0)
v.check("X07.11i", (1 / -ld[1]["V1"]).real)
v.check("X07.11j", ld[0]["p2"].real)
fw = mna(T + [("Vg", "V", "g", "0", 2.0), ("Rg", "R", "g", "p1", 50.0), ("RL", "R", "p2", "0", 50.0)], 0)
S11, S21 = fw[0]["p1"].real - 1, fw[0]["p2"].real
rv = mna(T + [("Vg", "V", "g", "0", 2.0), ("Rg", "R", "g", "p2", 50.0), ("RL", "R", "p1", "0", 50.0)], 0)
S22 = rv[0]["p2"].real - 1
v.check("X07.11k", S11)
v.check("X07.11l", S21)
v.check("X07.11m", S22)
v.check("X07.11n", -20 * np.log10(abs(S21)))
v.check("X07.11o", -20 * np.log10(abs(S11)))
v.check("X07.11q", (1 / -mna(T + [("V2", "V", "p2", "0", 1.0), ("R1", "R", "p1", "0", 50.0)], 0)[1]["V2"]).real)

# ---- Q12 (07-11): full three-phase circuit, RMS phasors, delta load
w12 = TAU * 50
Vp = 400 / math.sqrt(3)
src = [("Va", "V", "a", "0", Vp), ("Vb", "V", "b", "0", Vp * np.exp(-2j * math.pi / 3)),
       ("Vc", "V", "c", "0", Vp * np.exp(2j * math.pi / 3))]
dl = []
for p, q in (("a", "b"), ("b", "c"), ("c", "a")):
    dl += [("R" + p + q, "R", p, p + q, 30.0), ("L" + p + q, "L", p + q, q, 40 / w12)]
e12, i12 = mna(src + dl, w12)
Ia, Ic = -i12["Va"], -i12["Vc"]
v.check("X07.12a", abs(i12["Lab"]))
v.check("X07.12b", abs(Ia))
S12 = sum(e12[n] * np.conj(-i12[s]) for n, s in (("a", "Va"), ("b", "Vb"), ("c", "Vc")))
v.check("X07.12c", S12.real)
v.check("X07.12d", S12.imag)
v.check("X07.12e", S12.real / abs(S12))
v.check("X07.12f", ((e12["a"] - e12["b"]) * np.conj(Ia)).real)
v.check("X07.12g", ((e12["c"] - e12["b"]) * np.conj(Ic)).real)


def q_with(C, delta):
    caps = ([("C" + p + q, "C", p, q, C) for p, q in (("a", "b"), ("b", "c"), ("c", "a"))] if delta
            else [("C" + p, "C", p, "n", C) for p in "abc"])
    e, i = mna(src + dl + caps, w12)
    return sum(e[n] * np.conj(-i[s]) for n, s in (("a", "Va"), ("b", "Vb"), ("c", "Vc"))), -i["Va"]


Cy = brentq(lambda C: q_with(C, False)[0].imag, 1e-6, 1e-3, xtol=1e-15)
v.check("X07.12h", 1e6 * Cy)
v.check("X07.12i", abs(q_with(Cy, False)[1]))
v.check("X07.12j", 1e6 * brentq(lambda C: q_with(C, True)[0].imag, 1e-6, 1e-3, xtol=1e-15))

# ---- Q13 (07-03, 07-07, 07-08): buck output filter
L13, C13, ESR = 2.2e-6, 47e-6, 0.01


def h13(f, R=1.0, esr=0.0):
    els = [("V", "V", "sw", "0", 1.0), ("L", "L", "sw", "o", L13), ("RL", "R", "o", "0", R)]
    els += [("Re", "R", "o", "m", esr), ("C", "C", "m", "0", C13)] if esr else [("C", "C", "o", "0", C13)]
    return mna(els, TAU * f)[0]["o"]


f0_13 = brentq(lambda f: np.angle(h13(f)) + math.pi / 2, 1e3, 1e5)
v.check("X07.13a", f0_13 / 1e3)
v.check("X07.13b", math.sqrt(L13 / C13))
v.check("X07.13c", abs(h13(f0_13)))
v.check("X07.13d", 20 * np.log10(abs(h13(f0_13))))
N = 1 << 16
tsw = np.arange(N) / N / 5e5
sw = np.where((tsw * 5e5) % 1 < 0.25, 12.0, 0.0)
fft = np.fft.rfft(sw) / N
v.check("X07.13e", fft[0].real)
v.check("X07.13f", 2 * abs(fft[1]))
v.check("X07.13g", 1e3 * 2 * abs(fft[1]) * abs(h13(5e5, esr=ESR)))
v.check("X07.13h", 1e3 * 2 * abs(fft[1]) * abs(h13(5e5)))
v.check("X07.13i", brentq(lambda f: ESR - 1 / (TAU * f * C13), 1e4, 1e7) / 1e3)


def a13(R):
    return np.array([[-1 / (R * C13), 1 / C13], [-1 / L13, 0.0]])  # state (v_out deviation, i_L deviation)


ev13 = np.linalg.eigvals(a13(1.0))
v.check("X07.13r", -ev13[0].real)
v.check("X07.13s", abs(ev13[0].imag))
v.check("X07.13t", -ev13[0].real / abs(ev13[0]))
s13 = solve_ivp(lambda t, x: a13(1.0) @ x + np.array([-2.0 / C13, 0.0]), (0, 1e-4), [0.0, 0.0], **RT)
tdr, vdr = extremum(s13.sol, lambda x: x[0], 0, 5e-5, sign=-1)
v.check("X07.13j", 1e6 * tdr)
v.check("X07.13k", -vdr)
v.check("X07.13l", 2.0 * math.sqrt(L13 / C13))
v.check("X07.13m", abs(h13(f0_13, R=10.0)))
v.check("X07.13n", 20 * np.log10(abs(h13(f0_13, R=10.0))))
ev10 = np.linalg.eigvals(a13(10.0))
v.check("X07.13o", -ev10[0].real)
v.check("X07.13p", 1e3 / -ev10[0].real)
v.check("X07.13q", 1e6 * TAU / abs(ev10[0].imag))

# ---- Q14 (07-10, 07-08): L-section by root-finding on Z_in = 50
f14, RL14 = 2.4e9, 12.5


def zin14(f, L, C):
    w = TAU * f
    abcd = np.array([[1, 0], [1j * w * C, 1]]) @ np.array([[1, 1j * w * L], [0, 1]])
    return (abcd[0, 0] * RL14 + abcd[0, 1]) / (abcd[1, 0] * RL14 + abcd[1, 1])


def match_err(x):
    z = zin14(f14, x[0] * 1e-9, x[1] * 1e-12)
    return [z.real - 50, z.imag]


Ln, Cp = fsolve(match_err, [1.0, 2.0], xtol=1e-14)
g0 = (RL14 - 50) / (RL14 + 50)
v.check("X07.14a", g0)
v.check("X07.14b", -20 * np.log10(abs(g0)))
v.check("X07.14c", -10 * np.log10(1 - g0 ** 2))
v.check("X07.14d", TAU * f14 * Ln * 1e-9 / RL14)
v.check("X07.14e", Ln)
v.check("X07.14f", Cp)
v.check("X07.14g", zin14(f14, Ln * 1e-9, Cp * 1e-12).real)
for f, kg, kr, kre, kim in ((2.2e9, "X07.14h", "X07.14i", "X07.14n", "X07.14o"),
                            (2.6e9, "X07.14j", "X07.14k", "X07.14p", "X07.14q")):
    z = zin14(f, Ln * 1e-9, Cp * 1e-12)
    g = abs((z - 50) / (z + 50))
    v.check(kg, g)
    v.check(kr, -20 * np.log10(g))
    v.check(kre, z.real)
    v.check(kim, z.imag)

# ---- Q15: three-phase apparent power by summing the three phases' VA; -3 dB amplitude from a first-order H
Sph = sum(abs((415 / math.sqrt(3)) * 30) for _ in range(3))
v.check("X07.15a", Sph / 1e3)
v.check("X07.15b", 0.8 * Sph / 1e3)
v.check("X07.15c", 100 * (1 - abs(1 / (1 + 1j))))

v.finish()
