#!/usr/bin/env python3
"""Verify chapter 15-08 (PID control): examples, problems and lab answers.

Routes:
- linear loops by exact step responses (labs/15-03-lab/specs.py) and scipy impulse/step responses;
- saturating loops, filtered derivatives and setpoint weights by the fixed-step RK4 simulator
  labs/15-08-lab/pid.py, with step-halving convergence checks and a cross-check against scipy for linear cases;
- margins by root finding (labs/15-07-lab/freqdomain.py); pole placements by polynomial coefficient matching.
Example 15-08.4 is confirmed in ngspice (labs/15-08-lab/windup.cir).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
for lab in ("15-08-lab", "15-07-lab", "15-03-lab"):
    sys.path.insert(0, str(ROOT / "labs" / lab))
from eeverify import Verifier  # noqa: E402
import pid  # noqa: E402
from freqdomain import margins  # noqa: E402
from specs import step_specs  # noqa: E402

CH = ROOT / "chapters" / "15-08-pid-control.md"
v = Verifier.from_files("15-08", CH, ROOT / "solutions" / "15-08-solutions.md", ROOT / "labs" / "15-08-lab" / "README.md")


def peak_exact(num, den, t_end):
    """Peak of the step response of num/den and its time, refined on the impulse response."""
    sysd = signal.TransferFunction(num, den)
    t = np.linspace(0, t_end, 200001)
    _, y = signal.step(sysd, T=t)
    k = int(np.argmax(y))
    h = lambda tt: signal.impulse(sysd, T=[0, tt])[1][-1]  # noqa: E731
    tp = brentq(h, t[k - 1], t[k + 1], xtol=1e-14)
    return signal.step(sysd, T=[0, tp])[1][-1], tp


def settle(t, y, ref, band=0.02):
    out = np.flatnonzero(np.abs(y - ref) > band * ref)
    return t[out[-1] + 1]


# ---------------------------------------------------------------------------------------- Example 1
K, tau = 0.5, 10.0
wn, z = 0.5, 0.8
Kp1 = (2 * z * wn * tau - 1) / K
Ki1 = wn**2 * tau / K
v.check("Ex 15-08.1a", Kp1)
v.check("Ex 15-08.1b", Ki1)
v.check("Ex 15-08.1c", -Ki1 / Kp1)
den1 = [tau, 1 + K * Kp1, K * Ki1]
v.assert_true("Ex 1: poles have wn 0.5 and zeta 0.8", np.allclose(np.roots(den1), np.roots([1, 2 * z * wn, wn**2])))
v.check("Ex 15-08.1d", 100 * step_specs([K * Kp1, K * Ki1], den1, 40)["overshoot"])
v.check("Ex 15-08.1e", 100 * math.exp(-math.pi * z / math.sqrt(1 - z * z)))
v.check("Ex 15-08.1f", margins([K * Kp1, K * Ki1], [tau, 1, 0])["pm"])
pk, tp = peak_exact([K, 0], den1, 40)
v.check("Ex 15-08.1g", 20 * pk)
v.check("Ex 15-08.1h", tp)
# the RK4 simulator agrees with scipy on this linear loop
t, y, _, _ = pid.simulate(([K], [tau, 1]), Kp1, Ki1, r=lambda t: 0.0, d=lambda t: 20.0, t_end=20, dt=2e-3)
v.assert_true("Ex 1: RK4 simulator matches the exact disturbance peak", abs(y.max() - 20 * pk) < 1e-5)

# ---------------------------------------------------------------------------------------- Example 2
Kc = 5.0
v.check("Ex 15-08.2a", 1 / Kc)
denD = np.polymul(np.polymul([1, 1], [0.2, 1]), [1, Kc])
pk, tp = peak_exact([1, 0], denD, 10)
v.check("Ex 15-08.2b", pk)
v.check("Ex 15-08.2c", tp)
v.check("Ex 15-08.2d", signal.step(([1, 0], denD), T=[0, 3.0])[1][-1])

# ---------------------------------------------------------------------------------------- Example 3
P3 = ([1], [1, 3, 3, 1])
Pu = 2 * math.pi / math.sqrt(3)
v.check("Ex 15-08.3a", Pu)
zn = pid.zn_ultimate(8, Pu)
tl = pid.tyreus_luyben(8, Pu)
for (kp_, ti_, td_), keys in ((zn, "bcd"), (tl, "efg")):
    v.check(f"Ex 15-08.3{keys[0]}", kp_)
    v.check(f"Ex 15-08.3{keys[1]}", ti_)
    v.check(f"Ex 15-08.3{keys[2]}", td_)
for (kp_, ti_, td_), keys in ((zn, "hjlnp"), (tl, "ikmoq")):
    n, d = pid.pid_tf(kp_, ti_, td_, 10)
    v.check(f"Ex 15-08.3{keys[0]}", margins(n, np.polymul(d, P3[1]))["pm"])
    t, y, _, _ = pid.simulate(P3, kp_, kp_ / ti_, kp_ * td_, N=10, t_end=60, dt=1e-3)
    v.check(f"Ex 15-08.3{keys[1]}", 100 * (y.max() - 1))
    v.check(f"Ex 15-08.3{keys[2]}", settle(t, y, 1.0))
    t, y, _, _ = pid.simulate(P3, kp_, kp_ / ti_, kp_ * td_, N=10, r=lambda t: 0.0, d=lambda t: 1.0, t_end=60, dt=1e-3)
    v.check(f"Ex 15-08.3{keys[3]}", y.max())
    v.check(f"Ex 15-08.3{keys[4]}", np.trapezoid(np.abs(y), t))
    # cross-check the filtered-PID loop against scipy's step response of the same transfer function
    Ln, Ld = n, np.polymul(d, P3[1])
    _, ys = signal.step((Ln, np.polyadd(Ld, Ln)), T=np.linspace(0, 60, 60001))
    v.assert_true(f"Ex 3: RK4 matches scipy (Kp = {kp_:.3g})", abs(ys.max() - 1 - (step_specs(Ln, np.polyadd(Ld, Ln), 60)["peak"] - 1)) < 1e-6)

# ---------------------------------------------------------------------------------------- Example 4
P1 = ([K], [tau, 1])
runs = {}
for mode in ("none", "back", "clamp"):
    res = []
    for dt in (2e-3, 1e-3):
        t, y, u, _ = pid.simulate(P1, Kp1, Ki1, umin=-10, umax=10, aw=mode, r=lambda t: 4.0, t_end=80, dt=dt)
        k = int(np.argmax(y))
        res.append((y[k], t[k], settle(t, y, 4.0)))
    # clamping switches the integrator off and on, so its error is first order in dt (about 3e-6 K here), still
    # far below the published precision; the smooth modes converge at fourth order
    tol = 1e-4 if mode == "clamp" else 1e-6
    v.assert_true(f"Ex 4 ({mode}): step halving changes the peak by < {tol:g}", abs(res[0][0] - res[1][0]) < tol)
    runs[mode] = res[1]
v.check("Ex 15-08.4a", runs["none"][0])
v.check("Ex 15-08.4b", 100 * (runs["none"][0] / 4 - 1))
v.check("Ex 15-08.4c", runs["none"][1])
v.check("Ex 15-08.4d", runs["none"][2])
v.check("Ex 15-08.4e", runs["back"][0])
v.check("Ex 15-08.4f", 100 * (runs["back"][0] / 4 - 1))
v.check("Ex 15-08.4g", runs["back"][2])
v.check("Ex 15-08.4k", runs["back"][1])
v.check("Ex 15-08.4h", 100 * (runs["clamp"][0] / 4 - 1))
v.check("Ex 15-08.4i", runs["clamp"][2])
v.check("Ex 15-08.4l", runs["clamp"][0])
v.check("Ex 15-08.4m", runs["clamp"][1])
s1 = step_specs([K * Kp1, K * Ki1], den1, 40)
v.check("Ex 15-08.4j", 100 * s1["overshoot"])
v.check("Ex 15-08.4n", 4 * s1["peak"])
v.check("Ex 15-08.4o", s1["tpeak"])
v.check("Ex 15-08.4p", s1["settle"])

# ---------------------------------------------------------------------------------------- Example 5
kp_, ti_, td_ = zn
cases = {}
for b, c in ((1, 1), (1, 0), (0.5, 0)):
    t, y, u, _ = pid.simulate(P3, kp_, kp_ / ti_, kp_ * td_, N=10, b=b, c=c, t_end=30, dt=1e-3)
    cases[(b, c)] = (u[0], u.max(), 100 * (y.max() - 1))
v.check("Ex 15-08.5a", cases[(1, 1)][0])
v.assert_true("Ex 5: kick equals Kp(1 + N)", abs(cases[(1, 1)][0] - kp_ * 11) < 1e-9)
v.check("Ex 15-08.5b", cases[(1, 1)][2])
v.check("Ex 15-08.5c", cases[(1, 0)][0])
v.check("Ex 15-08.5d", cases[(1, 0)][2])
v.check("Ex 15-08.5h", cases[(1, 0)][1])
v.check("Ex 15-08.5e", cases[(0.5, 0)][0])
v.check("Ex 15-08.5f", cases[(0.5, 0)][2])
dpk = []
for b, c in ((1, 1), (1, 0), (0.5, 0)):
    t, y, _, _ = pid.simulate(P3, kp_, kp_ / ti_, kp_ * td_, N=10, b=b, c=c, r=lambda t: 0.0, d=lambda t: 1.0, t_end=30, dt=1e-3)
    dpk.append(y.max())
v.check("Ex 15-08.5g", dpk[0])
v.assert_true("Ex 5: disturbance response identical for all weights", max(dpk) - min(dpk) < 1e-12)

# ---------------------------------------------------------------------------------------- Example 6
Kt, taut, T = 0.5, 2.0, 0.1
wc6 = (math.pi / 6) / T
Kp6 = wc6 * taut / Kt
Ki6 = Kp6 / taut
m = margins(np.polymul([Kp6, Ki6], [Kt]), np.polymul([1, 0], [taut, 1]), T=T)
v.check("Ex 15-08.6a", m["wc"])
v.check("Ex 15-08.6b", Kp6)
v.check("Ex 15-08.6c", Ki6)
v.check("Ex 15-08.6d", m["gm"])
v.check("Ex 15-08.6e", m["gm_db"])
v.check("Ex 15-08.6f", m["delay_margin"])
v.check("Ex 15-08.6g", m["w180"])
v.assert_true("Ex 6: phase margin is 60 deg", abs(m["pm"] - 60) < 1e-9)

# ---------------------------------------------------------------------------------------- Problem 1
v.check("15-08.1a", 2 / 0.5)
v.check("15-08.1b", 2 * 0.1)
zz = np.sort(np.roots([0.5 * 0.1, 0.5, 1]).real)
v.check("15-08.1c", zz[1])
v.check("15-08.1d", zz[0])

# ---------------------------------------------------------------------------------------- Problem 2
v.check("15-08.2a", 1 - step_specs([K * 14], [tau, 1 + K * 14], 10)["final"])

# ---------------------------------------------------------------------------------------- Problem 3
for f, key in ((3, "a"), (5, "b"), (10, "c")):
    v.check(f"15-08.3{key}", math.degrees(math.atan(1 / f)))

# ---------------------------------------------------------------------------------------- Problem 4
Kp4 = (2 * 0.7 * 100 * 0.025 - 1) / 50
Ki4 = 100**2 * 0.025 / 50
v.check("15-08.4a", Kp4)
v.check("15-08.4b", Ki4)
v.check("15-08.4c", -Ki4 / Kp4)
s4 = step_specs([50 * Kp4, 50 * Ki4], [0.025, 1 + 50 * Kp4, 50 * Ki4], 0.3)
v.check("15-08.4d", 100 * s4["overshoot"])
v.check("15-08.4e", 1e3 * s4["settle"])
v.check("15-08.4f", 100 * math.exp(-math.pi * 0.7 / math.sqrt(1 - 0.49)))

# ---------------------------------------------------------------------------------------- Problem 5
Kp5, Ti5 = pid.simc_pi(2, 10, 1)
v.check("15-08.5a", Kp5)
v.check("15-08.5b", Ti5)
m = margins(np.polymul([Kp5 * Ti5, Kp5], [2]), np.polymul([Ti5, 0], [10, 1]), T=1.0)
v.check("15-08.5c", m["pm"])
v.check("15-08.5d", m["gm"])
v.check("15-08.5e", m["gm_db"])
v.check("15-08.5f", m["delay_margin"])
v.check("15-08.5g", m["wc"])

# ---------------------------------------------------------------------------------------- Problem 6
Ku6 = brentq(lambda k: np.max(np.roots([1, 3, 2, k]).real), 1, 20, xtol=1e-12)
v.check("15-08.6a", Ku6)
r6 = np.roots([1, 3, 2, Ku6])
Pu6 = 2 * math.pi / float(np.max(r6.imag))
v.check("15-08.6b", Pu6)
k6 = pid.zn_ultimate(Ku6, Pu6)
v.check("15-08.6c", k6[0])
v.check("15-08.6d", k6[1])
v.check("15-08.6e", k6[2])
n, d = pid.pid_tf(*k6, 10)
v.check("15-08.6f", margins(n, np.polymul(d, [1, 3, 2, 0]))["pm"])
t, y, _, _ = pid.simulate(([1], [1, 3, 2, 0]), k6[0], k6[0] / k6[1], k6[0] * k6[2], N=10, t_end=40, dt=1e-3)
v.check("15-08.6g", 100 * (y.max() - 1))

# ---------------------------------------------------------------------------------------- Problem 7
v.check("15-08.7a", zn[0] * 11)
v.check("15-08.7b", 20 * math.log10(zn[0] * 11))
v.check("15-08.7c", zn[0] * 6)
n10, d10 = pid.pid_tf(*zn, 10)
v.assert_true("P7: the filtered PID's gain tends to Kp(1 + N)", abs(abs(np.polyval(n10, 1e9j) / np.polyval(d10, 1e9j)) - zn[0] * 11) < 1e-4)

# ---------------------------------------------------------------------------------------- Problem 8
for Tt, (ko, ks) in ((1.4, "ab"), (5.6, "cd")):
    t, y, _, _ = pid.simulate(P1, Kp1, Ki1, umin=-10, umax=10, aw="back", Tt=Tt, r=lambda t: 4.0, t_end=80, dt=1e-3)
    v.check(f"15-08.8{ko}", 100 * (y.max() / 4 - 1))
    v.check(f"15-08.8{ks}", settle(t, y, 4.0))

# ---------------------------------------------------------------------------------------- Problem 9
Kd9, Kp9, Ki9 = (15 - 6) / 5, (75 - 5) / 5, 125 / 5
v.check("15-08.9a", Kd9)
v.check("15-08.9b", Kp9)
v.check("15-08.9c", Ki9)
char9 = np.polyadd(np.polymul(np.polymul([1, 1], [0.2, 1]), [1, 0]), [0, Kd9, Kp9, Ki9])
v.assert_true("P9: all poles at -5", np.allclose(np.poly(np.roots(char9)), np.poly([-5, -5, -5]), atol=1e-6))
pk, tp = peak_exact([1, 0], char9, 10)
v.check("15-08.9d", pk)
v.check("15-08.9g", tp)
v.assert_true("P9: disturbance below 1e-5 at 3 s", abs(signal.step(([1, 0], char9), T=[0, 3.0])[1][-1]) < 1e-5)
v.check("15-08.9e", signal.step(([1, 0], denD), T=[0, 3.0])[1][-1])
v.check("15-08.9f", 100 * step_specs([Kd9, Kp9, Ki9], char9, 10)["overshoot"])

# ---------------------------------------------------------------------------------------- Problem 10
f10 = lambda b: 100 * (pid.simulate(P3, kp_, kp_ / ti_, kp_ * td_, N=10, b=b, c=0, t_end=30, dt=2e-3)[1].max() - 1) - 10  # noqa: E731
b10 = brentq(f10, 0.2, 0.5, xtol=1e-7)
v.check("15-08.10a", b10)

# ---------------------------------------------------------------------------------------- Problem 11
wc11 = (math.pi / 6) / 0.3
v.check("15-08.11a", wc11)
v.check("15-08.11b", wc11 * taut / Kt)
v.check("15-08.11c", wc11 / Kt)
m = margins(np.polymul([wc11 * taut / Kt, wc11 / Kt], [Kt]), np.polymul([1, 0], [taut, 1]), T=0.3)
v.assert_true("P11: 60 deg margin with the 0.3 s delay", abs(m["pm"] - 60) < 1e-9)

# ---------------------------------------------------------------------------------------- Problem 12
v.check("15-08.12a", 4 / (math.pi * 0.159))
v.check("15-08.12b", brentq(lambda k: np.max(np.roots([1, 3, 3, 1 + k]).real), 1, 20, xtol=1e-12))

# ---------------------------------------------------------------------------------------- Lab
sat = {}
for mode in ("none", "back", "clamp"):
    t, y, u, _ = pid.simulate(P1, Kp1, Ki1, umin=-10, umax=10, aw=mode, r=lambda t: 4.0, t_end=80, dt=1e-3)
    sat[mode] = t[np.flatnonzero(u >= 10 - 1e-12)[-1]]
v.check("Lab 15-08.a", sat["none"])
v.check("Lab 15-08.b", sat["back"])
v.check("Lab 15-08.c", sat["clamp"])
t, y, _, _ = pid.simulate(P1, Kp1, Ki1, b=0.0, t_end=40, dt=1e-3)
v.check("Lab 15-08.d", 100 * (y.max() - 1))

sys.exit(v.finish())
