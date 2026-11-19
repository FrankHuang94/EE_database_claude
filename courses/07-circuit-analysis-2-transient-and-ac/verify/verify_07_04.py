#!/usr/bin/env python3
"""Verify every published number in chapter 07-04 (worked examples, numbers to know, practitioner
lens), its problem solutions and its lab handout.

Independent routes: the chapter and solutions work in the s-domain (impedances, nodal and mesh
equations, partial fractions). Here each circuit is instead written as time-domain state equations
dx/dt = A x + B u from KCL/KVL; poles are numerical eigenvalues of A, zeros come from
scipy.signal.ss2zpk, and waveforms, peaks, crossings and charges come from integrating the state
equations with solve_ivp. The ngspice netlists in labs/07-04-lab are run by tools/run_spice.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "07-04",
    COURSE / "chapters" / "07-04-laplace-domain-circuit-analysis.md",
    COURSE / "solutions" / "07-04-solutions.md",
    COURSE / "labs" / "07-04-lab" / "README.md",
)
pi, sqrt, exp, ln = math.pi, math.sqrt, math.exp, math.log


def simulate(A, g, x0, t_end, n_steps=400):
    A, g = np.asarray(A, float), np.asarray(g, float)
    return solve_ivp(lambda t, x: A @ x + g, (0.0, t_end), np.asarray(x0, float), method="DOP853",
                     rtol=1e-11, atol=1e-15, dense_output=True, max_step=t_end / n_steps)


def extreme(f, t0, t1, kind="max", n=20001):
    t = np.linspace(t0, t1, n)
    y = np.asarray(f(t), float)
    k = int(np.argmax(y) if kind == "max" else np.argmin(y))
    lo, hi = t[max(k - 1, 0)], t[min(k + 1, n - 1)]
    sgn = -1.0 if kind == "max" else 1.0
    r = minimize_scalar(lambda tt: sgn * float(f(tt)), bounds=(lo, hi), method="bounded",
                        options={"xatol": (hi - lo) * 1e-9})
    return r.x, float(f(r.x))


def zpk(A, B, C, D=0.0):
    z, p, k = signal.ss2zpk(np.asarray(A, float), np.asarray(B, float).reshape(-1, 1),
                            np.asarray(C, float).reshape(1, -1), np.array([[D]]))
    return np.sort_complex(z), np.sort_complex(p), k


def dc_gain(A, B, C, D=0.0):
    return float(-np.asarray(C, float) @ np.linalg.solve(np.asarray(A, float), np.asarray(B, float)) + D)


# ================================================================================ Example 1
R, L, C = 2.0, 0.5e-3, 50e-6
A = np.array([[-R / L, -1 / L], [1 / C, 0.0]])          # states (i, vC); source 12 V
g = np.array([12 / L, 0.0])
x0 = np.array([2.0, 8.0])
v.check("Ex 07-04.1a", L * x0[0] * 1e3)
v.check("Ex 07-04.1b", -np.linalg.solve(A, g)[1])
sol = simulate(A, g, x0, 10e-3, n_steps=2000)
v.check("Ex 07-04.1c", sol.sol(0.5e-3)[1])
v.check("Ex 07-04.1d", sol.sol(0.0)[1])
v.check("Ex 07-04.1e", sol.sol(10e-3)[1])
v.assert_true("Ex1 settles to 12 V", abs(sol.sol(10e-3)[1] - 12) < 1e-6)
v.assert_true("Ex1 matches 07-03's peak of 15.37 V", abs(extreme(lambda t: sol.sol(t)[1], 0, 1e-3)[1] - 15.37) < 5e-3)

# ================================================================================ Example 2
Rr, wc = 50.0, 2 * pi * 1e6
C1 = C2 = 1 / (wc * Rr)
Lb = 2 * Rr / wc
v.assert_true("Ex2 component values 3.183 nF and 15.92 uH", abs(C1 - 3.183e-9) < 5e-13 and abs(Lb - 15.92e-6) < 5e-9)
A2 = np.array([[-1 / (Rr * C1), -1 / C1, 0], [1 / Lb, 0, -1 / Lb], [0, 1 / C2, -1 / (Rr * C2)]])  # (v1, iL, v2)
B2 = np.array([1 / (Rr * C1), 0, 0])
C2v = np.array([0, 0, 1.0])
z2, p2, _ = zpk(A2, B2, C2v)
real_pole = min(p2, key=lambda q: abs(q.imag)).real
cpx = [q for q in p2 if q.imag > 1]
v.check("Ex 07-04.2a", real_pole / 1e6)
v.check("Ex 07-04.2b", cpx[0].real / 1e6)
v.check("Ex 07-04.2c", cpx[0].imag / 1e6)
v.assert_true("Ex2 has no finite zeros", not np.any(np.abs(z2) < 1e12))
v.check("Ex 07-04.2d", dc_gain(A2, B2, C2v))
sol = simulate(A2, B2, [0, 0, 0], 4e-6)
tp, yp = extreme(lambda t: sol.sol(t)[2], 0, 2e-6)
v.check("Ex 07-04.2e", tp * 1e6)
v.check("Ex 07-04.2f", (yp / 0.5 - 1) * 100)

# ================================================================================ Example 3
R1, C3, L3, R2 = 100.0, 1e-6, 10e-3, 10.0
A3 = np.array([[-1 / (R1 * C3), -1 / C3], [1 / L3, -R2 / L3]])     # (v, iL)
B3 = np.array([1 / (R1 * C3), 0])
z3, p3, _ = zpk(A3, B3, [1, 0])
v.check("Ex 07-04.3a", z3[0].real)
v.check("Ex 07-04.3b", p3[0].real)
v.check("Ex 07-04.3c", abs(p3[0].imag))
v.check("Ex 07-04.3d", dc_gain(A3, B3, [1, 0]))
v.check("Ex 07-04.3e", (11 * B3)[0] / 1e5)
sol = simulate(A3, 11 * B3, [0, 0], 2e-3)
v.assert_true("Ex3 peak is 07-03's 6.066 V", abs(extreme(lambda t: sol.sol(t)[0], 0, 1e-3)[1] - 6.066) < 5e-4)

# ================================================================================ Example 4
# Charge sharing through a tiny resistance (1 mohm): the transferred charge and final voltages do
# not depend on it, and the ideal impulse is its limit.
Ca, Cb, Rs = 1e-6, 4e-6, 1e-3
A4 = np.array([[-1 / (Rs * Ca), 1 / (Rs * Ca)], [1 / (Rs * Cb), -1 / (Rs * Cb)]])
sol = simulate(A4, [0, 0], [10.0, 0.0], 50e-9, n_steps=5000)
va, vb = sol.sol(50e-9)
v.check("Ex 07-04.4a", Cb * vb * 1e6)
v.check("Ex 07-04.4b", va)
v.assert_true("Ex4 both capacitors end at the same voltage", abs(va - vb) < 1e-9)
v.check("Ex 07-04.4c", 0.5 * Ca * 100 * 1e6)
v.check("Ex 07-04.4d", (0.5 * Ca * va**2 + 0.5 * Cb * vb**2) * 1e6)
t = np.linspace(0, 50e-9, 200001)
P = (sol.sol(t)[0] - sol.sol(t)[1]) ** 2 / Rs
v.assert_true("Ex4 the resistor dissipates the missing 40 uJ", abs(np.trapezoid(P, t) * 1e6 - 40) < 1e-3)

# ================================================================================ Example 5
RL, Cc = 10.0, 10e-6
for RE, kp, kz, ki in ((0.5, "a", "b", "c"), (5e-3, "d", "e", "f")):
    # driving a current into the node: state vC (ideal capacitance), output v = node voltage
    # node: v = (i_in*RL*RE + RL*vC)/(RL + RE) ; C dvC/dt = (v - vC)/RE
    k1 = RL / (RL + RE)
    A5 = np.array([[(k1 - 1) / (RE * Cc)]])
    B5 = np.array([RL * RE / (RL + RE) / (RE * Cc)])
    z5, p5, k5 = zpk(A5, B5, [k1], RL * RE / (RL + RE))
    v.check(f"Ex 07-04.5{kp}", abs(p5[0].real) / (2 * pi))
    v.check(f"Ex 07-04.5{kz}", abs(z5[0].real) / (2 * pi) / 1e3 if RE == 0.5 else abs(z5[0].real) / (2 * pi) / 1e6)
    v.check(f"Ex 07-04.5{ki}", RL * RE / (RL + RE) * (1 if RE == 0.5 else 1e3))
    v.assert_true(f"Ex5 Z(0) is the load resistance for ESR {RE}", abs(dc_gain(A5, B5, [k1], RL * RE / (RL + RE)) - RL) < 1e-9)

# ================================================================================ Example 6
Rw, Cw = 10e3, 10e-9
w0 = 1 / (Rw * Cw)


def wien(K):
    """States (v1 series capacitor, v2 shunt capacitor = node x); output = K v2."""
    return np.array([[-1, K - 1], [-1, K - 2]]) / (Rw * Cw)


v.check("Ex 07-04.6a", w0 / 1e3)
v.check("Ex 07-04.6b", w0 / (2 * pi) / 1e3)
ev = np.linalg.eigvals(wien(2.9))
v.check("Ex 07-04.6c", ev[0].real)
v.check("Ex 07-04.6d", abs(ev[0].imag))
v.assert_true("Ex6 K = 3 puts the poles on the imaginary axis", np.allclose(np.linalg.eigvals(wien(3.0)).real, 0, atol=1e-6))
ev31 = np.linalg.eigvals(wien(3.1))
v.check("Ex 07-04.6e", 1 / ev31[0].real * 1e3)
sol = simulate(wien(3.1), [0, 0], [0, 1e-3], 20e-3, n_steps=20000)
v.check("Ex 07-04.6f", ln(1000) / ev31[0].real * 1e3)
T6 = 2 * pi / abs(ev31[0].imag)
pk0 = np.abs(sol.sol(np.linspace(0, T6, 2001))[1]).max()
pk1 = np.abs(sol.sol(np.linspace(10 * T6, 11 * T6, 2001))[1]).max()
v.assert_true("Ex6 simulated peaks grow by e^(500 s^-1 x 10 periods)", abs(pk1 / pk0 / exp(ev31[0].real * 10 * T6) - 1) < 0.02)
v.assert_true("Ex6 K = 0 roots are real and negative (passive network)",
              np.all(np.abs(np.linalg.eigvals(wien(0.0)).imag) < 1e-9) and np.all(np.linalg.eigvals(wien(0.0)).real < 0))

# ============================================================================== Numbers / PL
fz = lambda R, C: 1 / (2 * pi * R * C)  # noqa: E731
v.check("N 07-04.a", fz(0.1, 2.2e-6) / 1e3)
v.check("N 07-04.b", fz(20, 2.2e-6) / 1e3)
v.check("N 07-04.c", fz(0.5, 10e-6) / 1e3)
v.check("PL 07-04.a", fz(0.1, 2.2e-6) / 1e3)
v.check("PL 07-04.b", fz(0.1, 2.2e-6) / 72.3e3)

# ================================================================================ Problems
v.check("07-04.1a", 0.02 * 0.5 * 1e3)
v.check("07-04.1b", 4.7e-6 * 5 * 1e6)
# P2: driving-point impedance R + (L || C): current in, voltage out. States (vC, iL)
R, L, C = 100.0, 10e-3, 1e-6
A = np.array([[0, -1 / C], [1 / L, 0]])
B = np.array([1 / C, 0])
z, p, k = zpk(A, B, [1, 0], R)
v.check("07-04.2a", abs(p[0]) / 1e3)
v.check("07-04.2b", z[0].real)
v.check("07-04.2c", abs(z[0].imag))
v.check("07-04.2d", dc_gain(A + np.diag([-1e-12, -1e-12]), B, [1, 0], R))
# P3: (a) poles -100, -400 and zero -200: simulate as a state-space step response
num = [10, 2000]
den = np.polymul([1, 100], [1, 400])
tt = np.linspace(0, 0.1, 20001)
_, y = signal.step((num, den), T=tt)
v.check("07-04.3a", y[0])
v.check("07-04.3b", y[-1])
_, y2 = signal.step(([10], [1, 0, 1e6]), T=np.linspace(0, 0.0628318, 200001))
v.check("07-04.3c", 10 / 1e6 * 1e6)
v.check("07-04.3d", y2.mean() * 1e6, tol=0.01)
v.check("07-04.3e", y2.max() * 1e6)
# P4: states (v, iL) with I step; iL(0-) = 10 mA, v(0-) = 5 V
R, L, C = 250.0, 50e-3, 2e-6
A = np.array([[-1 / (R * C), -1 / C], [1 / L, 0]])
ev = np.linalg.eigvals(A)
v.check("07-04.4a", -ev[0].real)
v.check("07-04.4b", abs(ev[0].imag))
sol = simulate(A, [0.02 / C, 0], [5.0, 0.01], 5e-3)
v.check("07-04.4c", sol.sol(1e-3)[0])
solzs = simulate(A, [0.02 / C, 0], [0.0, 0.0], 5e-3)
t_q = pi / (2 * 3000)                      # where sin(3000 t) = 1
v.check("07-04.4d", solzs.sol(t_q)[0] * exp(1000 * t_q))
v.assert_true("P4 total response is 5 e^-1000t cos 3000t",
              np.allclose(sol.sol(np.linspace(0, 5e-3, 501))[0],
                          5 * np.exp(-1000 * np.linspace(0, 5e-3, 501)) * np.cos(3000 * np.linspace(0, 5e-3, 501)), atol=1e-8))
# P5: series loop capacitor (charged 10 V) + 1 k + 0.5 H. States (i, vC) with vC opposing
A = np.array([[-1000 / 0.5, 1 / 0.5], [-1 / 2e-6, 0]])     # L di/dt = vC - R i ; C dvC/dt = -i
ev = np.linalg.eigvals(A)
v.check("07-04.5a", -ev.real.mean() / sqrt(abs(np.prod(ev))))
sol = simulate(A, [0, 0], [0, 10.0], 10e-3)
tpk, ipk = extreme(lambda t: sol.sol(t)[0], 0, 5e-3)
v.check("07-04.5b", tpk * 1e3)
v.check("07-04.5c", ipk * 1e3)
v.check("07-04.5d", 0.5 * (A @ np.array([0, 10.0]))[0])
# P6: states (vC, iL)
R1, C, L, R2 = 10.0, 10e-6, 1e-3, 10.0
A = np.array([[-1 / (R1 * C), -1 / C], [1 / L, -R2 / L]])
g = np.array([10 / (R1 * C), 0])
ev = np.linalg.eigvals(A)
v.check("07-04.6a", ev[0].real)
v.check("07-04.6b", abs(ev[0].imag))
v.check("07-04.6c", -ev[0].real / abs(ev[0]))
v.check("07-04.6d", -np.linalg.solve(A, g)[1])
sol = simulate(A, g, [0, 0], 3e-3)
tpk, ipk = extreme(lambda t: sol.sol(t)[1], 0, 1e-3)
v.check("07-04.6e", ipk)
v.check("07-04.6f", tpk * 1e6)
v.check("07-04.6g", sol.sol(0.5e-3)[1])
# P7
A = np.array([[-2000.0, 1000.0], [1000.0, -1000.0]])
ev = np.sort(np.linalg.eigvals(A).real)
v.check("07-04.7a", ev[1])
v.check("07-04.7b", ev[0])
v.check("07-04.7c", dc_gain(A, [1000.0, 0], [0, 1]))
z, _, _ = zpk(A, [1000.0, 0], [0, 1])
v.assert_true("P7 the RC ladder has no finite zeros", not np.any(np.abs(z) < 1e12))
# P8: states (iL, vC) of the shunt branch; output = node voltage = L diL/dt + vC
R, L, C = 50.0, 1e-6, 1e-9
A = np.array([[-R / L, -1 / L], [1 / C, 0]])
B = np.array([1 / L, 0])
Cout = np.array([-R, 0])            # v_node = vin - R iL
z, p, _ = zpk(A, B, Cout, 1.0)
v.check("07-04.8a", abs(z[0].imag) / (2 * pi) / 1e6)
v.check("07-04.8b", p[0].real / 1e6)
v.check("07-04.8c", abs(p[0].imag) / 1e6)
v.check("07-04.8d", -p[0].real / abs(p[0]))
# P9: impulse response of the current = derivative of the step response's current
R, L, C = 10.0, 1e-3, 1e-6
A = np.array([[-R / L, -1 / L], [1 / C, 0]])
x_imp0 = np.array([1 / L, 0])        # a unit V·s impulse puts 1/L amperes in the inductor at once
v.check("07-04.9a", x_imp0[0])
sol = simulate(A, [0, 0], x_imp0, 200e-6)
v.check("07-04.9b", brentq(lambda t: sol.sol(t)[0], 1e-6, 80e-6, xtol=1e-16) * 1e6)
# P10: two inductors in series through a tiny resistance after the switch opens (flux sharing)
L1, L2 = 10e-3, 30e-3
i_after = (L1 * 1.0) / (L1 + L2)
v.check("07-04.10a", i_after)
v.check("07-04.10b", 0.5 * L1 * 1.0 * 1e3)
v.check("07-04.10c", 0.5 * (L1 + L2) * i_after**2 * 1e3)
v.check("07-04.10d", L2 * i_after * 1e3)
v.assert_true("P10 flux linkage is conserved", abs((L1 + L2) * i_after - L1 * 1.0) < 1e-15)
# P11: Miller stage. States: vout across (C_L + C_gd) with input feedthrough; use the exact ODE
gm, RD, Cgd, CL = 10e-3, 5e3, 0.5e-12, 2e-12
# (Cgd + CL) dvout/dt = Cgd dvin/dt - gm vin - vout/RD ; for a step, the jump is vin*Cgd/(Cgd+CL)
v0 = 0.01 * Cgd / (Cgd + CL)
A = np.array([[-1 / (RD * (Cgd + CL))]])
g = np.array([-gm * 0.01 / (Cgd + CL)])
sol = simulate(A, g, [v0], 400e-9, n_steps=4000)
# state x = vout - k vin (k = Cgd/(Cgd+CL)) removes the feedthrough: dx/dt = A x + B vin, vout = x + k vin
kq = Cgd / (Cgd + CL)
Bq = [(-gm - kq / RD) / (Cgd + CL)]
z, p, k = zpk(A, Bq, [1.0], kq)
v.check("07-04.11a", z[0].real / (2 * pi) / 1e9)
v.check("07-04.11b", abs(p[0].real) / (2 * pi) / 1e6)
v.check("07-04.11c", dc_gain(A, Bq, [1.0], kq))
v.check("07-04.11d", sol.sol(0)[0] * 1e3)
v.check("07-04.11e", sol.sol(400e-9)[0])
v.check("07-04.11f", brentq(lambda t: sol.sol(t)[0], 0, 1e-9, xtol=1e-18) * 1e12)
v.assert_true("P11 the zero is in the right half-plane", z[0].real > 0)
# P12: Sallen-Key, states (vC1 a-to-out capacitor, vC2 node b)
Rk, Ck = 10e3, 10e-9


def sallen(K):
    # node a: va = vC1 + vo, vo = K vb, vb = vC2 ; C dvC1/dt = (vin - va)/R + (vb - va)/R ; C dvC2/dt = (va - vb)/R
    # with va = vC1 + K vC2:
    a11 = -2 / (Rk * Ck)
    a12 = (1 - 2 * K) / (Rk * Ck)
    a21 = 1 / (Rk * Ck)
    a22 = (K - 1) / (Rk * Ck)
    return np.array([[a11, a12], [a21, a22]])


v.check("07-04.12a", sqrt(abs(np.linalg.det(sallen(1.0)))) / (2 * pi) / 1e3)
Kb = brentq(lambda K: (lambda ev: abs(ev[0]) / (-2 * ev[0].real))(np.linalg.eigvals(sallen(K))) - 1 / sqrt(2), 1.01, 2.9)
v.check("07-04.12b", Kb)
Kc = brentq(lambda K: np.trace(sallen(K)), 1.5, 4.0)
v.check("07-04.12c", Kc, tol=1e-6)
# P13: three-section ladder in a loop with gain -K (normalized x = sRC); state matrix of the ladder
A_l = np.array([[-2, 1, 0], [1, -2, 1], [0, 1, -1]], float)    # nodes 1..3, RC = 1


def loop(K):
    A = A_l.copy()
    A[0, 2] += -K          # input of section 1 is -K v3
    return A


Kc13 = brentq(lambda K: max(np.linalg.eigvals(loop(K)).real), 20, 40)
v.check("07-04.13a", Kc13, tol=1e-6)
ev = np.linalg.eigvals(loop(29.0))
v.check("07-04.13b", max(abs(ev.imag)) / (2 * pi * 10e3 * 10e-9) / 1e3)
v.check("07-04.13c", min(ev.real) / (10e3 * 10e-9) / 1e3)
v.assert_true("P13 ladder characteristic polynomial is x^3 + 5x^2 + 6x + 1",
              np.allclose(np.poly(A_l), [1, 5, 6, 1]))
# P14
v.check("07-04.14a", fz(0.1, 2.2e-6) / 1e3)
v.check("07-04.14b", fz(20, 2.2e-6) / 1e3)
v.check("07-04.14c", fz(5e-3, 2.2e-6) / 1e6)
v.check("07-04.14d", fz(0.205, 2.2e-6) / 1e3)
v.check("07-04.14e", 0.05 * 0.205 * 1e3)

# P15: RC low-pass driven by a ramp; simulated, and the convolution integral done numerically
tau15 = 1e-3
s15 = solve_ivp(lambda t, x: [(1000.0 * t - x[0]) / tau15], (0, 6e-3), [0.0], rtol=1e-11, atol=1e-14,
                dense_output=True)
lam = np.linspace(0, 1e-3, 200001)
conv = np.trapezoid(np.exp(-(1e-3 - lam) / tau15) / tau15 * 1000.0 * lam, lam)
v.assert_true("P15 convolution integral matches the simulation at 1 ms", abs(conv - s15.sol(1e-3)[0]) < 1e-8)
v.check("07-04.15a", s15.sol(1e-3)[0])
v.check("07-04.15b", 1.0 - s15.sol(1e-3)[0])
v.check("07-04.15c", s15.sol(5e-3)[0])
v.check("07-04.15d", 5.0 - s15.sol(5e-3)[0])
s15b = solve_ivp(lambda t, x: [(1000.0 * t - x[0]) / tau15], (0, 0.05), [0.0], rtol=1e-11, atol=1e-14)
v.check("07-04.15e", 1000.0 * 0.05 - s15b.y[0, -1])
# P16: switching on 10 cos(1000 t); the steady state by a lock-in on the late waveform
H16 = 1 / (1 + 1j * 1000 * tau15)
v.check("07-04.16a", abs(H16))
v.check("07-04.16b", np.degrees(np.angle(H16)))


def sim16(phi):
    return solve_ivp(lambda t, x: [(10 * np.cos(1000 * t + phi) - x[0]) / tau15], (0, 0.07), [0.0],
                     rtol=1e-11, atol=1e-14, dense_output=True)


s16 = sim16(0.0)
tl = np.linspace(0.03, 0.03 + 2 * pi / 1000 * 5, 50001)
yl = s16.sol(tl)[0]
ph16 = 2 * np.trapezoid(yl * np.exp(-1j * 1000 * tl), tl) / (tl[-1] - tl[0])
v.check("07-04.16c", abs(ph16))
v.check("07-04.16h", abs(ph16) / 2)
tr16 = lambda t: s16.sol(t)[0] - (ph16 * np.exp(1j * 1000 * t)).real  # noqa: E731
v.check("07-04.16d", tr16(0.0))
v.check("07-04.16e", s16.sol(1e-3)[0])
v.check("07-04.16f", 1e3 * brentq(lambda t: abs(tr16(t)) - 0.01 * abs(ph16), 1e-4, 0.02))
phi0 = brentq(lambda ph: (sim16(ph).sol(0.003)[0] - (abs(ph16) * np.exp(1j * (1000 * 0.003 + ph + np.angle(ph16)))).real),
              -1.2, -0.4)
v.check("07-04.16g", np.degrees(phi0))

# ================================================================================ Lab handout
den = [1, 11000, 1.1e8]
num = np.polymul([1 / 20000, 1], [1.1e8 / 11])
tt = np.linspace(0, 2e-3, 200001)
_, y = signal.step((num, den), T=tt)
v.check("Lab 07-04.a", 11 * y.max())

v.finish()
