#!/usr/bin/env python3
"""Verify every published number in chapter 07-05 (worked examples, numbers to know, practitioner
lens), its problem solutions and its lab handout.

Independent routes: the chapter solves circuits with phasors and nodal or mesh equations. Here the
circuits are written as time-domain state equations dx/dt = A x + B u; steady-state phasors come
from the state-space frequency response C (jwI - A)^-1 B + D, and the key results are confirmed by
integrating the state equations into steady state and extracting amplitude and phase with a
lock-in (correlation over whole periods). Mesh problems are re-solved by nodal analysis and vice
versa. The ngspice AC netlists in labs/07-05-lab are run by tools/run_spice.py.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "07-05",
    COURSE / "chapters" / "07-05-sinusoidal-steady-state-and-impedance.md",
    COURSE / "solutions" / "07-05-solutions.md",
    COURSE / "labs" / "07-05-lab" / "README.md",
)
pi = math.pi
deg = lambda z: math.degrees(cmath.phase(z))  # noqa: E731


def freq_resp(A, B, C, D, w):
    """Steady-state output phasor per unit input phasor(s) of dx/dt = Ax + Bu, y = Cx + Du."""
    A, B, C = np.atleast_2d(A).astype(complex), np.atleast_2d(B).astype(complex), np.atleast_2d(C).astype(complex)
    X = np.linalg.solve(1j * w * np.eye(A.shape[0]) - A, B)
    return C @ X + np.atleast_2d(D)


def lockin(A, B, C, D, u_of_t, w, n_settle, n_meas=20):
    """Integrate into steady state, then return the output phasor at w by correlation over n_meas periods."""
    T = 2 * pi / w
    A, B = np.atleast_2d(A).astype(float), np.atleast_2d(B).astype(float)
    C, D = np.atleast_2d(C).astype(float), np.atleast_2d(D).astype(float)
    f = lambda t, x: A @ x + B @ u_of_t(t)  # noqa: E731
    t_end = (n_settle + n_meas) * T
    sol = solve_ivp(f, (0, t_end), np.zeros(A.shape[0]), method="DOP853", rtol=1e-10, atol=1e-13,
                    dense_output=True, max_step=T / 200)
    t = np.linspace(n_settle * T, t_end, n_meas * 2000, endpoint=False)
    y = (C @ sol.sol(t) + D @ np.array([u_of_t(tt) for tt in t]).T)[0]
    return 2 * np.mean(y * np.exp(-1j * w * t))


# ================================================================================ Example 1
Cc, Rc, Lc = 10e-6, 0.1, 2e-9
for f, kZ, kA, kD, kCs, kCp, kRp in ((1e3, "a", "b", "e", "g", "i", "j"), (100e3, "c", "d", "f", "h", "k", "l")):
    w = 2 * pi * f
    Z = Rc + 1j * w * Lc + 1 / (1j * w * Cc)
    Y = 1 / Z
    v.check(f"Ex 07-05.1{kZ}", abs(Z))
    v.check(f"Ex 07-05.1{kA}", deg(Z))
    v.check(f"Ex 07-05.1{kD}", Z.real / abs(Z.imag))
    v.check(f"Ex 07-05.1{kCs}", -1 / (w * Z.imag) * 1e6)
    v.check(f"Ex 07-05.1{kCp}", Y.imag / w * 1e6)
    v.check(f"Ex 07-05.1{kRp}", 1 / Y.real)
    v.assert_true(f"Ex1 Cp = Cs/(1 + D^2) at {f:g} Hz",
                  abs(Y.imag / w - (-1 / (w * Z.imag)) / (1 + (Z.real / Z.imag) ** 2)) < 1e-15)

# ================================================================================ Example 2
w = 2 * pi * 1e3
R1, C1, L1, R2 = 1e3, 100e-9, 100e-3, 2e3
# states (v1, iL); node 2 is algebraic: v2 = R2 (iL + is). Inputs u = (vs, is).
A = np.array([[-1 / (R1 * C1), -1 / C1], [1 / L1, -R2 / L1]])
B = np.array([[1 / (R1 * C1), 0], [0, -R2 / L1]])
Cv = np.array([[1, 0], [0, R2]])
Dv = np.array([[0, 0], [0, R2]])
U = np.array([10.0, 0.01 * cmath.exp(-1j * pi / 2)])
Vn = freq_resp(A, B, Cv, Dv, w) @ U
v.check("Ex 07-05.2a", abs(Vn[0]))
v.check("Ex 07-05.2b", deg(Vn[0]))
v.check("Ex 07-05.2c", abs(Vn[1]))
v.check("Ex 07-05.2d", deg(Vn[1]))
v.check("Ex 07-05.2e", 1 / (2 * pi * math.sqrt(L1 * C1)) / 1e3)
Vs_only = freq_resp(A, B, Cv, Dv, w) @ np.array([10.0, 0.0])
Is_only = freq_resp(A, B, Cv, Dv, w) @ np.array([0.0, 0.01 * cmath.exp(-1j * pi / 2)])
v.check("Ex 07-05.2f", abs(Vs_only[1]))
v.check("Ex 07-05.2g", deg(Vs_only[1]))
v.check("Ex 07-05.2h", abs(Is_only[1]))
v.check("Ex 07-05.2i", deg(Is_only[1]))
u2 = lambda t: np.array([10 * math.cos(w * t), 0.01 * math.cos(w * t - pi / 2)])  # noqa: E731
V2_lock = lockin(A, B, Cv[1:], Dv[1:], u2, w, n_settle=40)
v.assert_true("Ex2 time-domain lock-in agrees with the phasor V2", abs(V2_lock - Vn[1]) < 1e-4)

# ================================================================================ Example 3
w = 2 * pi * 10e3
R1, C, R2, RL = 1e3, 10e-9, 500.0, 1e3
ZC = 1 / (1j * w * C)
Vth = 10 * ZC / (R1 + ZC)
Zth = R2 + R1 * ZC / (R1 + ZC)
v.check("Ex 07-05.3a", abs(Vth))
v.check("Ex 07-05.3b", deg(Vth))
v.check("Ex 07-05.3c", Zth.real)
v.check("Ex 07-05.3d", Zth.imag)
# independent: state vC at node a; output vL = vC RL/(R2 + RL)
k = RL / (R2 + RL)
A = np.array([[-1 / (R1 * C) - (1 - k) / (R2 * C)]])
B = np.array([[1 / (R1 * C)]])
VL = freq_resp(A, B, [[k]], [[0]], w)[0, 0] * 10
v.check("Ex 07-05.3e", abs(VL))
v.check("Ex 07-05.3f", deg(VL))
v.assert_true("Ex3 Thevenin divider agrees with the direct solution", abs(Vth * RL / (Zth + RL) - VL) < 1e-12)

# ================================================================================ Example 4
ZLd, Zln = 18.4 + 13.8j, 0.5 + 0.3j
I = 23 / ZLd
Vs = 23 + I * Zln
v.check("Ex 07-05.4a", abs(I))
v.check("Ex 07-05.4b", deg(I))
v.check("Ex 07-05.4c", abs(Vs))
v.check("Ex 07-05.4d", (abs(Vs) - 23) / 23 * 100)
th = -cmath.phase(I)
v.check("Ex 07-05.4e", abs(I) * (Zln.real * math.cos(th) + Zln.imag * math.sin(th)))
v.assert_true("Ex4 the approximation is within 0.1 mV of the exact drop",
              abs(abs(Vs) - 23 - abs(I) * (0.5 * math.cos(th) + 0.3 * math.sin(th))) < 1e-4)

# ================================================================================ Example 5
Lx, Rx, R2b, R3b = 50e-3, 20.0, 1e3, 1e3
C4 = Lx / (R2b * R3b)
R4 = R2b * R3b / Rx
v.check("Ex 07-05.5a", C4 * 1e9)
v.check("Ex 07-05.5b", R4 / 1e3)
for f in (50.0, 1e3, 1e5):                      # detector null at every frequency
    w = 2 * pi * f
    Z1, Z2, Z3 = Rx + 1j * w * Lx, R2b, R3b
    Z4 = 1 / (1 / R4 + 1j * w * C4)
    vdet = Z1 / (Z1 + Z3) - Z2 / (Z2 + Z4)       # unit source across the bridge
    v.assert_true(f"Ex5 bridge balanced at {f:g} Hz", abs(vdet) < 1e-12)
v.check("Ex 07-05.5c", 2 * pi * 1e3 * Lx / Rx)

# ================================================================================ Example 6
R = 10e3
C = brentq(lambda c: (lambda H: deg(H) + 90)((1 - 1j * 2 * pi * 1e3 * R * c) / (1 + 1j * 2 * pi * 1e3 * R * c)), 1e-9, 1e-7)
v.check("Ex 07-05.6a", C * 1e9)
# all-pass as state equations: dvC/dt = (vin - vC)/(RC); vout = 2 vC - vin
A6, B6, C6, D6 = [[-1 / (R * C)]], [[1 / (R * C)]], [[2.0]], [[-1.0]]
for f, key in ((3e3, "b"), (100.0, "c"), (10e3, "d")):
    H = freq_resp(A6, B6, C6, D6, 2 * pi * f)[0, 0]
    v.check(f"Ex 07-05.6{key}", deg(H))
    v.assert_true(f"Ex6 all-pass magnitude 1 at {f:g} Hz", abs(abs(H) - 1) < 1e-12)
w1 = 2 * pi * 1e3
sol = solve_ivp(lambda t, x: np.array([(math.cos(w1 * t) + math.cos(3 * w1 * t) / 3 - x[0]) / (R * C)]),
                (0, 20e-3), [0.0], method="DOP853", rtol=1e-11, atol=1e-13, dense_output=True, max_step=2e-6)
tt = np.linspace(19e-3, 20e-3, 200000, endpoint=False)
vin = np.cos(w1 * tt) + np.cos(3 * w1 * tt) / 3
vout = 2 * sol.sol(tt)[0] - vin
v.check("Ex 07-05.6e", vin.max())
v.check("Ex 07-05.6f", vout.max())
H1 = freq_resp(A6, B6, C6, D6, w1)[0, 0]
H3 = freq_resp(A6, B6, C6, D6, 3 * w1)[0, 0]
v.check("Ex 07-05.6g", -cmath.phase(H1) / w1 * 1e3)
v.check("Ex 07-05.6h", -cmath.phase(H3) / (3 * w1) * 1e6)
v.check("Ex 07-05.6i", math.sqrt(np.mean(vout**2)))
v.assert_true("Ex6 RMS unchanged by the all-pass", abs(math.sqrt(np.mean(vin**2)) - math.sqrt(np.mean(vout**2))) < 1e-6)

# ================================================================================ Example 7 (VCCS, test source)
w7 = 1e4


def ex7(vs, it):
    """Nodes x, o; KCL with currents leaving: VCCS draws gm*Vx out of node o. Returns (Vx, Vo)."""
    G1, Gc, Gf, G2, gm = 1e-3, 1j * w7 * 100e-9, 1e-4, 5e-4, 10e-3
    Y = np.array([[G1 + Gc + Gf, -Gf], [-Gf + gm, Gf + G2]])
    return np.linalg.solve(Y, np.array([vs * G1, it]))


vx7, vo7 = ex7(1.0, 0.0)
v.check("Ex 07-05.7a", abs(vx7))
v.check("Ex 07-05.7b", deg(vx7))
v.check("Ex 07-05.7c", abs(vo7))
v.check("Ex 07-05.7d", deg(vo7))
zth7 = ex7(0.0, 1.0)[1]
v.check("Ex 07-05.7e", zth7.real)
v.check("Ex 07-05.7f", zth7.imag)
v.check("Ex 07-05.7g", 1 / (1e-4 + 5e-4))
v.check("Ex 07-05.7i", abs(zth7))
# short-circuit current: replace node o by ground and sum the currents into the short
vx_sc = 1e-3 / (1e-3 + 1j * w7 * 100e-9 + 1e-4)
v.check("Ex 07-05.7h", 1e3 * abs(vx_sc * 1e-4 - 10e-3 * vx_sc))
v.assert_true("Ex7 Isc equals VTh/ZTh", abs(abs(vo7 / zth7) - abs(vx_sc * 1e-4 - 10e-3 * vx_sc)) < 1e-12)

# ================================================================================ Problems
Y = 1 / (60 + 80j)
v.check("07-05.1a", Y.real * 1e3)
v.check("07-05.1b", Y.imag * 1e3)
Z = 1 / (2e-3 - 3e-3j)
v.check("07-05.1c", Z.real)
v.check("07-05.1d", Z.imag)
R, L, C = 50.0, 10e-3, 1e-6
Zs = lambda f: R + 1j * 2 * pi * f * L + 1 / (1j * 2 * pi * f * C)  # noqa: E731
v.check("07-05.2a", abs(Zs(1e3)))
v.check("07-05.2b", deg(Zs(1e3)))
v.check("07-05.2c", brentq(lambda f: Zs(f).imag, 100, 1e4) / 1e3)
v.check("07-05.2d", abs(Zs(5e3)))
v.check("07-05.2e", deg(Zs(5e3)))
w = 2 * pi * 1e6
Zi = 0.5 + 1j * w * 100e-6
Yi = 1 / Zi
v.check("07-05.3a", Zi.imag)
v.check("07-05.3b", Zi.imag / Zi.real)
v.check("07-05.3c", 1 / Yi.real / 1e3)
v.check("07-05.3d", -1 / (w * Yi.imag) * 1e6)
w = 2 * pi * 1e3
esr = 0.001 / (w * 1e-6)
Yc = 1 / (esr + 1 / (1j * w * 1e-6))
v.check("07-05.4a", esr)
v.check("07-05.4b", 1 / Yc.real / 1e3)
v.check("07-05.4c", Yc.imag / w * 1e6)
# P5: re-solve by nodal analysis at the capacitor node x
w = 2 * pi * 50
V1, V2 = 100.0, 50 * cmath.exp(1j * math.radians(30))
Zb1 = 10 + 1j * w * 0.1
Vx = (V1 / Zb1 + V2 / 20) / (1 / Zb1 + 1j * w * 100e-6 + 1 / 20)
I1, I2 = (V1 - Vx) / Zb1, (Vx - V2) / 20
v.check("07-05.5a", abs(I1))
v.check("07-05.5b", deg(I1))
v.check("07-05.5c", abs(I2))
v.check("07-05.5d", deg(I2))
v.check("07-05.5e", abs(I1 - I2))
v.check("07-05.5f", deg(I1 - I2))
v.check("07-05.5g", 2 * pi * 50 * 0.1)
v.check("07-05.5h", 1 / (2 * pi * 50 * 100e-6))
# P6: time-domain simulation with DC + AC, then lock-in and mean
R1, R2, C = 1e3, 1e3, 100e-9
A, B = [[-(1 / R1 + 1 / R2) / C]], [[1 / (R1 * C)]]
w = 2 * pi * 1e3
Vac = lockin(A, B, [[1.0]], [[0.0]], lambda t: np.array([2 * math.cos(w * t)]), w, n_settle=20)
v.check("07-05.6a", 5 * R2 / (R1 + R2))
v.check("07-05.6b", abs(Vac))
v.check("07-05.6c", deg(Vac))
# P7
w = 2 * pi * 1e6
ZL7 = 1j * w * 10e-6
Voc = 1 * 100 / (ZL7 + 100)
Isc = 1 / ZL7
v.check("07-05.7a", abs(Isc) * 1e3)
ZN = Voc / Isc
v.check("07-05.7b", ZN.real)
v.check("07-05.7c", ZN.imag)
v.check("07-05.7d", abs(ZN))
v.check("07-05.7e", deg(ZN))
# P8
R, L, C = 10.0, 10e-3, 1e-6
w0 = 1 / math.sqrt(L * C)
v.check("07-05.8a", w0 / (2 * pi) / 1e3)
I8 = 1 / (R + 1j * w0 * L + 1 / (1j * w0 * C))
v.check("07-05.8b", abs(I8))
v.check("07-05.8c", abs(1j * w0 * L * I8))
v.check("07-05.8d", w0 * L / R)
# P9
I9 = 10 * cmath.exp(-1j * pi / 6)
Vs9 = 100 + I9 * (1 + 2j)
v.check("07-05.9a", abs(Vs9))
v.check("07-05.9b", abs(Vs9) - 100)
v.check("07-05.9c", 10 * (math.cos(pi / 6) + 2 * math.sin(pi / 6)))
v.check("07-05.9d", I9.real)
v.check("07-05.9e", abs(100 + I9.real * (1 + 2j)) - 100)
v.check("07-05.9f", deg(Vs9))
v.check("07-05.9g", (abs(Vs9) - 100) - 10 * (math.cos(pi / 6) + 2 * math.sin(pi / 6)))
v.check("07-05.9h", Vs9.imag)
v.check("07-05.9i", abs(100 + I9.real * (1 + 2j)))
# P10
R, C = 1e4, 1e-8
ratio = lambda w: (R + 1 / (1j * w * C)) * (1 / R + 1j * w * C)  # noqa: E731
wb = brentq(lambda w: ratio(w).imag, 1e3, 1e5)
v.check("07-05.10a", wb / (2 * pi) / 1e3)
v.check("07-05.10b", ratio(wb).real)
# P11: solve the complex balance equation for the unknown's two parameters
w = 2 * pi * 1e3
Z2 = 4.4 + 1 / (1j * w * 100e-9)
Z1 = Z2 * 1e3 / 2.2e3                         # Z1 Z4 = Z2 Z3
Rx11, Cx11 = Z1.real, -1 / (w * Z1.imag)
v.check("07-05.11a", Rx11)
v.check("07-05.11b", Cx11 * 1e9)
v.check("07-05.11c", w * Cx11 * Rx11)
# P12
H12 = lambda f: -10e3 / (1e3 + 1 / (1j * 2 * pi * f * 100e-9))  # noqa: E731
v.check("07-05.12a", abs(H12(100)))
v.check("07-05.12b", abs(H12(1 / (2 * pi * 1e3 * 100e-9))))
v.check("07-05.12c", abs(H12(100e3)))
v.check("07-05.12d", 2 * pi * 100e3 * 10e3 * 100e-9)
v.check("07-05.12e", deg(H12(100)))
v.check("07-05.12f", deg(H12(1 / (2 * pi * 1e3 * 100e-9))))
v.check("07-05.12g", deg(H12(100e3)))
v.check("07-05.12h", 2 * pi * 100 * 10e3 * 100e-9)
v.check("07-05.12i", 1 / (1e3 * 100e-9) * 10e3 * 100e-9)
# P13
Re, Ri, Cm = 500.0, 300.0, 5e-9
Zt = lambda f: Re * (Ri + 1 / (1j * 2 * pi * f * Cm)) / (Re + Ri + 1 / (1j * 2 * pi * f * Cm))  # noqa: E731
v.check("07-05.13a", abs(Zt(5e3)))
v.check("07-05.13b", abs(Zt(50e3)))
v.check("07-05.13c", deg(Zt(50e3)))
v.check("07-05.13d", abs(Zt(1e6)))
v.check("07-05.13e", abs(Zt(1e-3)), tol=0.5)
v.check("07-05.13f", abs(Zt(1e12)))
v.check("07-05.13g", 1 / (2 * pi * (Re + Ri) * Cm) / 1e3)
v.check("07-05.13h", 1 / (2 * pi * Ri * Cm) / 1e3)
fmin = minimize_scalar(lambda lf: deg(Zt(10**lf)), bounds=(3, 7), method="bounded", options={"xatol": 1e-10}).x
v.check("07-05.13i", 10**fmin / 1e3)
v.check("07-05.13j", deg(Zt(5e3)))
v.check("07-05.13k", deg(Zt(1e6)))

# ================================================================================ Lab handout
w = 2 * pi * 100e3
Z = 0.1 + 1j * w * 20e-9 + 1 / (1j * w * 10e-6)
v.check("Lab 07-05.a", -1 / (w * Z.imag) * 1e6)
v.check("Lab 07-05.b", 1 / (2 * pi * math.sqrt(20e-9 * 10e-6)) / 1e3)
v.check("Lab 07-05.c", 1 / (2 * pi * 10e3 * 15e-9) / 1e3)
v.check("Lab 07-05.d", brentq(lambda f: math.degrees(cmath.phase((1 - 2j * pi * f * 10e3 * 16e-9) / (1 + 2j * pi * f * 10e3 * 16e-9))) + 90, 100, 1e4) / 1e3)

# ================================================================================ Numbers to know (section 7)
v.check("N 07-05.a", 1 / (2 * pi * 50 * 1e-6) / 1e3)
v.check("N 07-05.b", 1 / (2 * pi * 1e3 * 1e-6))
v.check("N 07-05.c", 1 / (2 * pi * 1e6 * 1e-6))
v.check("N 07-05.d", 2 * pi * 1e6 * 1e-6)
v.check("N 07-05.e", 2 * pi * 100e6 * 1e-6)

# ================================================================================ Practitioner lens (section 9)
# Small complex error delta: worst-case angle change is |delta| rad. Check by brute force over directions.
for eps, ident in [(0.0005, "PL 07-05.a"), (0.0008, "PL 07-05.b")]:
    ang = np.linspace(0, 2 * pi, 20001)
    worst = np.max(np.abs(np.angle(1 + eps * np.exp(1j * ang)))) * 180 / pi
    v.check(ident, worst, tol=0.0005)
    v.assert_true(f"{ident}: small-angle rule (180/pi)*eps", abs(worst - eps * 180 / pi) < 1e-4)
Zo_hf, Zs_hf, Zo_lf, Zs_lf = 1e6, 30e-3, 2e9, 1e-3
v.check("PL 07-05.c", 100 * 10e3 / Zo_hf)
v.check("PL 07-05.d", 100 * Zs_hf / 0.1)
v.check("PL 07-05.e", 100 * Zs_lf / 0.1)
resid = lambda Z, Zo, Zs: 100 * (Z / Zo + Zs / Z)  # noqa: E731
opt_hf = minimize_scalar(lambda lz: resid(10**lz, Zo_hf, Zs_hf), bounds=(-3, 9), method="bounded", options={"xatol": 1e-12})
opt_lf = minimize_scalar(lambda lz: resid(10**lz, Zo_lf, Zs_lf), bounds=(-3, 9), method="bounded", options={"xatol": 1e-12})
v.check("PL 07-05.f", 10**opt_hf.x)
v.check("PL 07-05.g", 10**opt_lf.x / 1e3)
v.check("PL 07-05.h", opt_hf.fun)
v.check("PL 07-05.i", opt_lf.fun)
v.assert_true("optimum is sqrt(Zo*Zs)", abs(10**opt_hf.x - math.sqrt(Zo_hf * Zs_hf)) < 1e-3)
v.check("PL 07-05.j", 1.0 * 200e-6 * 1e6)
v.check("PL 07-05.k", 1 / (360 * 3.5e3) * 1e6)
v.check("PL 07-05.l", 1 / (360 * 5e-6))
# phase error from a 5 us skew, by lock-in on sampled sines
f, dt = 3.5e3, 5e-6
t = np.arange(200000) / (200000 * f) * 50  # 50 periods
i_s = np.cos(2 * pi * f * t)
v_s = np.cos(2 * pi * f * (t - dt))
ph = lambda x: np.angle(np.sum(x * np.exp(-1j * 2 * pi * f * t)))  # noqa: E731
v.check("PL 07-05.m", abs(ph(v_s) - ph(i_s)) * 180 / pi)

# P14: the original Delta network solved by nodal analysis (no Delta-Y conversion); 1 A test current a -> d
Yab, Ybc, Yca, Ybd, Ycd = 1 / 10, 1 / 10j, 1 / -10j, 1 / 10, 1 / 5
# nodes a, b, c (d is ground)
Y14 = np.array([[Yab + Yca, -Yab, -Yca],
                [-Yab, Yab + Ybc + Ybd, -Ybc],
                [-Yca, -Ybc, Ybc + Yca + Ycd]])
Zad = np.linalg.solve(Y14, np.array([1.0, 0, 0]))[0]
# Y arms: from the Y equivalent's open-circuit two-terminal impedances (Z_ab = Za + Zb etc. with the third open)


def delta_z(p_, q_):
    """Impedance between two nodes of the Delta alone (third node floating), by nodal analysis."""
    ys = {("a", "b"): Yab, ("b", "c"): Ybc, ("c", "a"): Yca}
    nodes = [n for n in "abc" if n != q_]
    M = np.zeros((2, 2), complex)
    for (m, n), y in ys.items():
        for i, x in enumerate(nodes):
            if x in (m, n):
                M[i, i] += y
                other = n if x == m else m
                if other in nodes:
                    M[i, nodes.index(other)] -= y
    rhs = np.array([1.0 if x == p_ else 0.0 for x in nodes])
    return np.linalg.solve(M, rhs)[nodes.index(p_)]


Zab_oc, Zbc_oc, Zca_oc = delta_z("a", "b"), delta_z("b", "c"), delta_z("c", "a")
Za14 = (Zab_oc + Zca_oc - Zbc_oc) / 2
Zb14 = (Zab_oc + Zbc_oc - Zca_oc) / 2
Zc14 = (Zbc_oc + Zca_oc - Zab_oc) / 2
v.check("07-05.14a", Za14.imag)
v.check("07-05.14b", Zb14.imag)
v.check("07-05.14c", Zc14.real)
v.check("07-05.14d", Zad.real)
v.check("07-05.14e", Zad.imag)
v.check("07-05.14f", abs(Zad))
v.check("07-05.14g", deg(Zad))
I14 = 10 / Zad
v.check("07-05.14h", abs(I14))
v.check("07-05.14i", deg(I14))
v.check("07-05.14j", 0.5 * (10 * np.conj(I14)).real)
# P15: nodal with the VCVS's internal node e = -50 Vx (unknowns Vx, Vo, Ie through the source)
w15 = 2 * pi * 1e4


def p15(drive_vs, it=0.0):
    Gs = 1e-3 if drive_vs else 0.0
    yc = 1j * w15 * 1e-9
    M = np.array([[Gs + 1e-4 + yc, -yc], [-yc + 50 / 100, yc + 1 / 100 + 1e-4]])
    return np.linalg.solve(M, np.array([0.1 * Gs + it, 0.0]))


vx15, vo15 = p15(True)
K15 = vo15 / vx15
v.check("07-05.15a", abs(K15))
v.check("07-05.15b", deg(K15))
v.check("07-05.15c", abs(vx15))
v.check("07-05.15d", deg(vx15))
v.check("07-05.15e", abs(vo15))
v.check("07-05.15f", deg(vo15))
v.check("07-05.15g", abs(vo15 / 0.1))
zin15 = p15(False, 1.0)[0]
v.check("07-05.15h", zin15.real)
v.check("07-05.15i", zin15.imag)
zm = 1 / (1e-4 + 1j * w15 * 1e-9 * 51)
v.check("07-05.15j", zm.real)
v.check("07-05.15k", zm.imag)
v.check("07-05.15l", 1e9 * (1 / zin15 - 1e-4).imag / w15)

v.finish()
