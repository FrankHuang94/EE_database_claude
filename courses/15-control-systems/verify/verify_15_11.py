#!/usr/bin/env python3
"""Verify chapter 15-11 (digital control): examples, problems and lab answers.

Routes:
- z-plane maps, ZOH equivalents and Tustin coefficients from closed forms, cross-checked with an
  independent matrix-exponential discretization written here and with labs/15-11-lab/digital.py;
- sampled-loop step responses by an exact simulation written here (the plant state advanced with the
  matrix exponential, the intersample peak refined by bounded minimization), cross-checked against
  digital.sampled_loop;
- discrete margins by root finding on the unit circle (linear frequency grid, written here), compared
  with digital.dmargins;
- stability limits from the Jury closed form and, independently, by bisection on the largest root magnitude;
- the ngspice sampler (labs/15-11-lab/sample_hold.cir) is modelled here as a track-and-hold to confirm the
  chapter's statement about its measured overshoot; run_spice confirms the netlist itself.
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
sys.path.insert(0, str(ROOT / "labs" / "15-11-lab"))
from eeverify import Verifier  # noqa: E402
import digital as dg  # noqa: E402

CH = ROOT / "chapters" / "15-11-digital-control.md"
v = Verifier.from_files("15-11", CH, ROOT / "solutions" / "15-11-solutions.md", ROOT / "labs" / "15-11-lab" / "README.md")


# ---------------------------------------------------------------- independent helpers
def zoh_phi_gamma(A, B, T):
    """Exact ZOH discretization from one matrix exponential of the augmented matrix [[A, B], [0, 0]]."""
    A = np.atleast_2d(np.asarray(A, float))
    n = len(A)
    M = np.zeros((n + 1, n + 1))
    M[:n, :n] = A
    M[:n, n] = np.asarray(B, float).ravel()
    E = expm(M * T)
    return E[:n, :n], E[:n, n]


def zoh_tf(A, B, C, T):
    """ZOH-equivalent G(z) = C (zI - Phi)^-1 Gamma as (num, den) in powers of z."""
    Phi, Gam = zoh_phi_gamma(A, B, T)
    num, den = signal.ss2tf(Phi, Gam.reshape(-1, 1), np.atleast_2d(C), np.zeros((1, 1)))
    return np.trim_zeros(np.where(abs(num[0]) < 1e-15, 0, num[0]), "f"), den


def L_at(numz, denz, w, T):
    z = cmath.exp(1j * w * T)
    return np.polyval(numz, z) / np.polyval(denz, z)


def margins_unit_circle(numz, denz, T, n=400001):
    """PM (deg), crossover (rad/s), GM and its frequency on a linear grid up to the Nyquist frequency."""
    wN = math.pi / T
    w = np.linspace(wN * 1e-6, wN * (1 - 1e-9), n)
    z = np.exp(1j * w * T)
    L = np.polyval(numz, z) / np.polyval(denz, z)
    mag, ph = np.abs(L), np.unwrap(np.angle(L))
    out = {}
    i = np.flatnonzero(np.diff(np.sign(mag - 1)) != 0)
    if i.size:
        k = i[0]
        wc = brentq(lambda x: abs(L_at(numz, denz, x, T)) - 1, w[k], w[k + 1], xtol=1e-13, rtol=1e-14)
        phc = ph[k] + cmath.phase(L_at(numz, denz, wc, T) / L[k])
        out["wc"], out["pm"] = wc, 180 + math.degrees(phc)
    j = np.flatnonzero(np.diff(np.sign(ph + math.pi)) != 0)
    if j.size:
        k = j[0]
        f = lambda x: ph[k] + cmath.phase(L_at(numz, denz, x, T) / L[k]) + math.pi  # noqa: E731
        w180 = brentq(f, w[k], w[k + 1], xtol=1e-13, rtol=1e-14)
        out["w180"], out["gm"] = w180, 1 / abs(L_at(numz, denz, w180, T))
    return out


def sim_sampled(A, B, C, T, ctrl, t_end, r=1.0, fine=200, track=0.0):
    """Exact step response of a continuous plant under a discrete controller with a hold.

    ctrl(e, state) -> (u, state) is called with e = r - y(kT). With track > 0 the sampler is a
    track-and-hold: for the first `track` seconds of each period u = ctrl applied continuously to the live
    error (proportional control only), then held at its value at kT + track, like sample_hold.cir.
    Returns (peak value, time of peak, list of sample values y(kT)).
    """
    A = np.atleast_2d(np.asarray(A, float))
    B = np.asarray(B, float).ravel()
    C = np.asarray(C, float).ravel()
    n = len(A)
    M = np.zeros((n + 1, n + 1))
    M[:n, :n] = A
    M[:n, n] = B
    taus = np.linspace(0, T, fine + 1)
    Es = [expm(M * t) for t in taus]
    x = np.zeros(n)
    state = None
    best, tbest = -math.inf, 0.0
    samples = []
    steps = int(round(t_end / T))
    if track:
        K = ctrl(1.0, None)[0]                       # proportional gain
        Acl = A - K * np.outer(B, C)                 # live tracking: u = K (r - y)
        Mt = np.zeros((n + 1, n + 1))
        Mt[:n, :n] = Acl
        Mt[:n, n] = K * B * r                        # constant input r through the gain
        Et = expm(Mt * track)
    for k in range(steps):
        samples.append(float(C @ x))
        if track:
            x = (Et @ np.append(x, 1.0))[:n]         # transparent phase (the peak never falls in this 1 ms)
            u, state = ctrl(r - float(C @ x), state)
            seg = T - track
            Eseg = [expm(M * t) for t in np.linspace(0, seg, fine + 1)]
            z = np.append(x, u)
            ys = [float(C @ (E @ z)[:n]) for E in Eseg]
            i = int(np.argmax(ys))
            if ys[i] > best:
                lo, hi = seg * max(i - 1, 0) / fine, seg * min(i + 1, fine) / fine
                res = minimize_scalar(lambda t: -float(C @ (expm(M * t) @ z)[:n]), bounds=(lo, hi),
                                      method="bounded", options={"xatol": 1e-11})
                best, tbest = -res.fun, k * T + track + res.x
            x = (Eseg[-1] @ z)[:n]
            continue
        u, state = ctrl(r - float(C @ x), state)
        z = np.append(x, u)
        ys = [float(C @ (E @ z)[:n]) for E in Es]
        i = int(np.argmax(ys))
        if ys[i] > best:
            lo, hi = taus[max(i - 1, 0)], taus[min(i + 1, fine)]
            res = minimize_scalar(lambda t: -float(C @ (expm(M * t) @ z)[:n]), bounds=(lo, hi),
                                  method="bounded", options={"xatol": 1e-11})
            best, tbest = -res.fun, k * T + res.x
        x = (Es[-1] @ z)[:n]
    return best, tbest, samples


def pi_ctrl(b0, b1):
    def f(e, st):
        up, ep = st if st is not None else (0.0, 0.0)
        u = up + b0 * e + b1 * ep
        return u, (u, e)
    return f


def p_ctrl(K):
    return lambda e, st: (K * e, st)


def cont_margins(Ls, w_lo=1e-4, w_hi=1e4):
    """Crossover and PM of a continuous loop with phase unwrapped on a log grid."""
    w = np.logspace(math.log10(w_lo), math.log10(w_hi), 200001)
    L = Ls(1j * w)
    ph = np.unwrap(np.angle(L))
    k = np.flatnonzero(np.diff(np.sign(np.abs(L) - 1)) != 0)[0]
    wc = brentq(lambda x: abs(Ls(1j * x)) - 1, w[k], w[k + 1], xtol=1e-13, rtol=1e-14)
    return wc, 180 + math.degrees(ph[k] + cmath.phase(Ls(1j * wc) / L[k]))


SERVO = ([[0, 1], [0, -1]], [0, 1], [1, 0])           # 1/[s(s + 1)], states y and dy/dt
THERMAL = ([[-0.1]], [0.05], [1.0])                    # 0.5/(10s + 1) K/W


# ---------------------------------------------------------------- Example 15-11.1
T = 0.1
s1 = complex(-2, 2 * math.sqrt(3))
z1 = cmath.exp(s1 * T)
v.check("Ex 15-11.1a", abs(z1))
v.check("Ex 15-11.1b", math.degrees(cmath.phase(z1)))
v.assert_true("Ex1: poles have zeta 0.5 and wn 4", abs(abs(s1) - 4) < 1e-12 and abs(-s1.real / abs(s1) - 0.5) < 1e-12)
v.assert_true("Ex1: about 18 samples per damped period", round(360 / math.degrees(cmath.phase(z1))) == 18)

# ---------------------------------------------------------------- Example 15-11.2
T = 0.1
p = math.exp(-T)
numa, dena = zoh_tf([[-1]], [1], [1], T)
v.check("Ex 15-11.2a", 1 - p)
v.check("Ex 15-11.2b", p)
v.assert_true("Ex2a: matrix exponential matches closed form", abs(numa[-1] - (1 - p)) < 1e-14 and abs(dena[-1] + p) < 1e-14)
n1, n0 = T - 1 + p, 1 - p - T * p
numb, denb = zoh_tf(*SERVO, T)
v.check("Ex 15-11.2c", n1)
v.check("Ex 15-11.2d", n0)
v.check("Ex 15-11.2e", -n0 / n1)
v.assert_true("Ex2b: matrix exponential matches closed form",
              np.allclose(numb, [n1, n0], atol=1e-14) and np.allclose(denb, [1, -(1 + p), p], atol=1e-14))
v.assert_true("Ex2b: denominator z^2 - 1.905z + 0.905", round(1 + p, 3) == 1.905 and round(p, 3) == 0.905)
nl, dl = dg.zoh([1], [1, 1, 0], T)
v.assert_true("Ex2b: lab zoh() agrees", np.allclose(nl, [n1, n0], atol=1e-12) and np.allclose(dl, [1, -(1 + p), p], atol=1e-12))
v.assert_true("Ex2a: DC gain 1", abs((1 - p) / (1 - p) - 1) < 1e-15)

# ---------------------------------------------------------------- Example 15-11.3
Kp, Ki = 14.0, 5.0
cont = lambda s: 0.5 * (Kp * s + Ki) / (s * (10 * s + 1))  # noqa: E731
wc_c, pm_c = cont_margins(cont)
v.assert_true("Ex3: continuous crossover 0.766 rad/s, PM 72.4 deg", round(wc_c, 3) == 0.766 and round(pm_c, 1) == 72.4)
# continuous overshoot (12.6%): closed loop 0.5(14s + 5)/(10s^2 + 8s + 2.5)
tc = np.linspace(0, 60, 600001)
_, yc = signal.step(([7.0, 2.5], [10.0, 8.0, 2.5]), T=tc)
v.assert_true("Ex3: continuous overshoot 12.6%", round(100 * (yc.max() - 1), 1) == 12.6)

res3 = {}
for T in (0.5, 2.0):
    b0, b1 = Kp + Ki * T / 2, -Kp + Ki * T / 2
    lb0, lb1 = dg.pi_tustin(Kp, Ki, T)
    v.assert_true(f"Ex3 T={T}: lab pi_tustin agrees", abs(lb0 - b0) < 1e-14 and abs(lb1 - b1) < 1e-14)
    # C(z) = Kp + Ki (T/2)(z + 1)/(z - 1) expanded by hand, compared with the lab's general tustin()
    tn, td = dg.tustin([Kp, Ki], [1, 0], T)
    v.assert_true(f"Ex3 T={T}: tustin() of Kp + Ki/s gives (b0 z + b1)/(z - 1)",
                  np.allclose(np.asarray(tn) / td[0], [b0, b1], atol=1e-12) and np.allclose(np.asarray(td) / td[0], [1, -1], atol=1e-12))
    pk, tpk, _ = sim_sampled(*THERMAL, T, pi_ctrl(b0, b1), 300.0)
    os_ = 100 * (pk - 1)
    _, yl, _ = dg.sampled_loop(([0.5], [10, 1]), lambda e, st: pi_ctrl(b0, b1)(e, st), T, 300.0, n_sub=400)
    v.assert_true(f"Ex3 T={T}: lab sampled_loop overshoot agrees", abs(100 * (yl.max() - 1) - os_) < 2e-3)
    q = math.exp(-T / 10)
    G = ([0.5 * (1 - q)], [1, -q])
    numL = np.polymul([b0, b1], G[0])
    denL = np.polymul([1, -1], G[1])
    m = margins_unit_circle(numL, denL, T)
    ml = dg.dmargins(numL, denL, T)
    v.assert_true(f"Ex3 T={T}: lab dmargins agrees", abs(ml["pm"] - m["pm"]) < 1e-6)
    poles = np.roots(np.polyadd(denL, numL))
    v.assert_true(f"Ex3 T={T}: closed-loop poles inside the unit circle", np.all(np.abs(poles) < 1))
    res3[T] = (b0, b1, os_, m["pm"])
v.check("Ex 15-11.3a", res3[0.5][0])
v.check("Ex 15-11.3b", res3[0.5][1])
v.check("Ex 15-11.3c", res3[0.5][2])
v.check("Ex 15-11.3d", res3[0.5][3])
v.check("Ex 15-11.3e", res3[2.0][2])
v.check("Ex 15-11.3f", res3[2.0][3])
v.assert_true("Ex3 T=2: difference equation 19 e_k - 9 e_k-1", res3[2.0][0] == 19 and res3[2.0][1] == -9)
v.check("Ex 15-11.3g", math.degrees(wc_c * 0.5 / 2))
v.check("Ex 15-11.3h", pm_c - res3[0.5][3])
v.assert_true("Ex3: about 20 samples per plant time constant at T = 0.5 s", 10 / 0.5 == 20)

# ---------------------------------------------------------------- Example 15-11.4
T = 0.05
wc4 = math.sqrt((-100 + math.sqrt(100**2 + 4 * 100**2)) / 2)
pm4c = 90 - math.degrees(math.atan(wc4 / 10))
v.assert_true("Ex4: continuous crossover 7.86 rad/s, PM 51.8 deg", round(wc4, 2) == 7.86 and round(pm4c, 1) == 51.8)
loss4 = math.degrees(wc4 * T / 2)
v.assert_true("Ex4: displayed 11.26 deg and 51.83 deg", round(loss4, 2) == 11.26 and round(pm4c, 2) == 51.83)
v.check("Ex 15-11.4a", pm4c - loss4)
num4, den4 = zoh_tf([[0, 1], [0, -10]], [0, 100], [1, 0], T)
m4 = margins_unit_circle(num4, den4, T)
v.check("Ex 15-11.4b", m4["pm"])
v.check("Ex 15-11.4c", m4["gm"])
v.assert_true("Ex4: discrete crossover 7.82 rad/s", round(m4["wc"], 2) == 7.82)
v.assert_true("Ex4: wc T = 0.39 rad", round(wc4 * T, 2) == 0.39)
m4l = dg.dmargins(num4, den4, T)
v.assert_true("Ex4: lab dmargins agrees", abs(m4l["pm"] - m4["pm"]) < 1e-6 and abs(m4l["gm"] - m4["gm"]) < 1e-6)


# ---------------------------------------------------------------- Example 15-11.5 and Problem 15-11.7
def kmax_closed(T):
    q = math.exp(-T)
    return (1 - q) / (1 - q - T * q)


def char_servo(K, T):
    q = math.exp(-T)
    return [1, -(1 + q) + K * (T - 1 + q), q + K * (1 - q - T * q)]


def kmax_bisect(T):
    lo, hi = 1e-6, 1e4
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if np.max(np.abs(np.roots(char_servo(mid, T)))) < 1:
            lo = mid
        else:
            hi = mid
    return lo


for T, key in ((0.1, "Ex 15-11.5a"), (1.0, "Ex 15-11.5b"), (0.5, "15-11.7a")):
    k_c, k_b = kmax_closed(T), kmax_bisect(T)
    v.assert_true(f"Kmax at T={T}: Jury closed form equals root-magnitude bisection", abs(k_c - k_b) < 1e-9 * k_c)
    a1, a0 = char_servo(k_c * 0.999, T)[1:]
    v.assert_true(f"Kmax at T={T}: the other Jury conditions hold at the limit", dg.jury2(a1, a0) and 1 + a1 + a0 > 0 and 1 - a1 + a0 > 0)
    v.check(key, k_c)
v.assert_true("Ex5: Kmax ~ 2/T for small T", abs(kmax_closed(1e-3) * 1e-3 / 2 - 1) < 1e-2)
q = math.exp(-0.5)
v.assert_true("P7: displayed 0.3935/0.0902", round(1 - q, 4) == 0.3935 and round(1 - q - 0.5 * q, 4) == 0.0902)
v.assert_true("P7: Kmax(0.5) equals Ex 15-11.4's gain margin (time scaling)", abs(kmax_closed(0.5) - m4["gm"]) < 1e-6)

T = 0.5
poles5 = np.roots(char_servo(1.0, T))
v.assert_true("Ex5: poles 0.75 +- j0.366", np.allclose(sorted(np.round(poles5.imag, 3)), [-0.366, 0.366]) and np.allclose(np.round(poles5.real, 2), 0.75))
v.check("Ex 15-11.5c", abs(poles5[0]))
pk5, tpk5, _ = sim_sampled(*SERVO, T, p_ctrl(1.0), 30.0)
v.check("Ex 15-11.5e", 100 * (pk5 - 1))
v.check("Ex 15-11.5f", tpk5)
pk5f, tpk5f, _ = sim_sampled(*SERVO, T, p_ctrl(1.0), 30.0, fine=800)
v.assert_true("Ex5: peak converged in the intersample grid", abs(pk5f - pk5) < 1e-9 and abs(tpk5f - tpk5) < 1e-7)
tl, yl, _ = dg.sampled_loop(([1], [1, 1, 0]), lambda e, st: (e, st), T, 30.0, n_sub=500)
v.assert_true("Ex5: lab sampled_loop agrees", abs(yl.max() - pk5) < 1e-5 and abs(tl[np.argmax(yl)] - tpk5) < 2e-3)
# The ngspice sampler tracks for 1 ms then holds: model it and confirm the chapter's "28.6% at 3.45 s"
pk_th, tpk_th, _ = sim_sampled(*SERVO, T, p_ctrl(1.0), 30.0, track=1e-3)
v.assert_true("Ex5: track-and-hold sampler gives 28.6% at 3.45 s", round(100 * (pk_th - 1), 1) == 28.6 and round(tpk_th, 2) == 3.45)
v.assert_true("Lab discussion 1: the 1 ms tracking lowers overshoot by about 0.2% of its value",
              pk_th < pk5 and 0.1 < 100 * (pk5 - pk_th) / (pk5 - 1) < 0.3)

# ---------------------------------------------------------------- Example 15-11.6
for fs, key in ((1e6, "Ex 15-11.6a"), (2e6, "Ex 15-11.6b")):
    v.check(key, 360 * 60e3 * 1.5 / fs)

# ---------------------------------------------------------------- Section 3.5 and lab guided exercise
v.assert_true("3.5: 10x to 30x sampling costs about 18 to 6 degrees (wc ~ bandwidth)",
              round(math.degrees(math.pi / 10)) == 18 and round(math.degrees(math.pi / 30)) == 6)
wc_servo = math.sqrt((math.sqrt(5) - 1) / 2)
v.assert_true("Guided exercise: crossover 0.79 rad/s, hold cost ~11 deg",
              round(wc_servo, 2) == 0.79 and round(math.degrees(wc_servo * 0.25)) == 11)
v.assert_true("Guided exercise: sampled overshoot in the predicted 25-30% band", 25 < 100 * (pk5 - 1) < 30)

# ---------------------------------------------------------------- Lab answers
zeta = 0.5
os_cont = 100 * math.exp(-math.pi * zeta / math.sqrt(1 - zeta**2))
ts = np.linspace(0, 20, 200001)
_, ys = signal.step(([1], [1, 1, 1]), T=ts)
v.assert_true("Lab a: closed form matches simulated step", abs(100 * (ys.max() - 1) - os_cont) < 1e-4)
v.check("Lab 15-11.a", os_cont)
numl, denl = zoh_tf(*SERVO, 0.5)
ml = margins_unit_circle(numl, denl, 0.5)
v.check("Lab 15-11.b", ml["pm"])
v.assert_true("Lab b equals Ex 15-11.4b by time scaling (s' = s/10, T' = 10 T)", abs(ml["pm"] - m4["pm"]) < 1e-6)

# ---------------------------------------------------------------- Problems
T = 0.05
v.check("15-11.1a", math.exp(-1 * T))
v.check("15-11.1b", math.exp(-10 * T))
v.check("15-11.1c", math.degrees(10 * T))

v.check("15-11.2a", math.degrees(2 * math.pi * 1000 / 20000 / 2))
v.assert_true("P2: 0.157 rad", round(2 * math.pi * 1000 / 40000, 3) == 0.157)

T = 0.25
num3, den3 = zoh_tf([[-2]], [2], [1], T)
v.check("15-11.3a", num3[-1])
v.check("15-11.3b", -den3[-1])
v.check("15-11.3c", num3[-1] / (1 - (-den3[-1])))
v.assert_true("P3: closed form 1 - e^-0.5", abs(num3[-1] - (1 - math.exp(-0.5))) < 1e-14)

# Problem 4: lead (1 + aT s)/(1 + T s) with the stated aT = 0.45364 s and T = 0.112591 s, Tustin at 0.2 s
aTl, Tl, T = 0.45364, 0.112591, 0.2
wm = 1 / math.sqrt(aTl * Tl)
alpha_lead = aTl / Tl
v.assert_true("P4: stated lead peaks at 37.0 deg at 4.42 rad/s",
              round(math.degrees(math.asin((alpha_lead - 1) / (alpha_lead + 1))), 1) == 37.0 and round(wm, 4) == 4.4248)
v.assert_true("P4: stated values round to 15-09's 0.454 s and 0.1126 s", round(aTl, 3) == 0.454 and round(Tl, 4) == 0.1126)


def tustin_lead(al):
    """s <- (1/al)(z - 1)/(z + 1); returns (b0, b1, pole) of (b0 z + b1)/(z - pole)."""
    d = al + Tl
    return (al + aTl) / d, (al - aTl) / d, (Tl - al) / d


def phase_peak(b0, b1, pz):
    f = lambda w: -cmath.phase((b0 * cmath.exp(1j * w * T) + b1) / (cmath.exp(1j * w * T) - pz))  # noqa: E731
    r = minimize_scalar(f, bounds=(0.5, math.pi / T * 0.99), method="bounded", options={"xatol": 1e-10})
    return r.x, -math.degrees(r.fun)


wp = wm
for al, keys, label in ((T / 2, ("15-11.4c", "15-11.4d", "15-11.4e", "15-11.4a"), "plain"),
                        (math.tan(wp * T / 2) / wp, ("15-11.4f", "15-11.4g", "15-11.4h", "15-11.4b"), "prewarped")):
    b0, b1, pz = tustin_lead(al)
    tn, td = dg.tustin([aTl, 1], [Tl, 1], T, None if label == "plain" else wp)
    v.assert_true(f"P4 {label}: lab tustin agrees", np.allclose(np.asarray(tn) / td[0], [b0, b1], atol=1e-12)
                  and np.allclose(np.asarray(td) / td[0], [1, -pz], atol=1e-12))
    wpk, phpk = phase_peak(b0, b1, pz)
    v.assert_true(f"P4 {label}: peak phase preserved at 37.0 deg", round(phpk, 1) == 37.0)
    v.check(keys[0], b0)
    v.check(keys[1], b1)
    v.check(keys[2], pz)
    v.check(keys[3], wpk)
    if label == "plain":
        v.assert_true("P4: plain peak equals the warping formula (2/T) arctan(wm T/2)", abs(wpk - 2 / T * math.atan(wm * T / 2)) < 1e-6)
        v.assert_true("P4: about 6% below the design frequency", round(100 * (1 - wpk / wm)) == 6)
v.assert_true("P4: w T = 0.88 rad", round(4.42 * T, 2) == 0.88)

r5a = np.roots([1, -1.2, 0.5])
r5b = np.roots([1, 0.5, -0.6])
v.assert_true("P5a: stable by Jury and by roots", dg.jury2(-1.2, 0.5) and np.all(np.abs(r5a) < 1))
v.assert_true("P5a: roots 0.6 +- j0.374", np.allclose(np.round(r5a.real, 1), 0.6) and np.allclose(sorted(np.round(r5a.imag, 3)), [-0.374, 0.374]))
v.check("15-11.5b", abs(r5a[0]))
v.assert_true("P5b: unstable by Jury and by roots", (not dg.jury2(0.5, -0.6)) and np.any(np.abs(r5b) > 1))
v.assert_true("P5b: 1 - a1 + a0 = -0.1", abs(1 - 0.5 - 0.6 + 0.1) < 1e-12)
v.check("15-11.5a", min(r5b))
v.check("15-11.5c", max(r5b))

sT = -100 * 0.025
v.check("15-11.6a", 1 + sT)
v.check("15-11.6b", 1 / (1 - sT))
v.check("15-11.6c", (1 + sT / 2) / (1 - sT / 2))
v.check("15-11.6d", math.exp(sT))

wc8, T8 = 5.24, 0.1
v.assert_true("P8: 15-08's thermal loop crossover (pi/6)/0.1 = 5.24 rad/s", round((math.pi / 6) / 0.1, 2) == wc8)
loss8 = math.degrees(wc8 * T8 / 2)
v.check("15-11.8a", loss8)
v.check("15-11.8b", 60 - loss8)
v.check("15-11.8c", (math.pi / 6) / 0.15)

v.check("15-11.9a", 150 / 2**12)
v.check("15-11.9b", 150 / 2**16)

# Problem 10: build the notch, discretize by hand (bilinear substitution), and read the null's angle
fs, f0 = 4000.0, 1000.0
T = 1 / fs
w0 = 2 * math.pi * f0


def notch_null(al):
    """Numerator s^2 + w0^2 with s <- (1/al)(z - 1)/(z + 1): (z - 1)^2 + (w0 al)^2 (z + 1)^2."""
    num = np.polyadd(np.polymul([1, -1], [1, -1]), (w0 * al) ** 2 * np.polymul([1, 1], [1, 1]))
    r = np.roots(num)
    v.assert_true("P10: notch zeros on the unit circle", np.allclose(np.abs(r), 1, atol=1e-12))
    return abs(cmath.phase(r[0])) / (2 * math.pi * T)


f_plain = notch_null(T / 2)
f_pw = notch_null(math.tan(w0 * T / 2) / w0)
v.assert_true("P10: plain null matches (fs/pi) arctan(pi f/fs)", abs(f_plain - fs / math.pi * math.atan(math.pi * f0 / fs)) < 1e-9)
Q = 5
tn, td = dg.tustin([1, 0, w0**2], [1, w0 / Q, w0**2], T)
v.assert_true("P10: lab tustin places the same null", abs(abs(cmath.phase(np.roots(tn)[0])) / (2 * math.pi * T) - f_plain) < 1e-6)
v.check("15-11.10a", f_plain)
v.check("15-11.10b", f_pw)
v.assert_true("P10: about 15% low", round(100 * (1 - f_plain / f0)) == 15)

sys.exit(v.finish())
