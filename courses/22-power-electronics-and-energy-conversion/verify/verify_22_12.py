#!/usr/bin/env python3
"""Verify every number in chapter 22-12 (power systems fundamentals), its problems and its lab.

Independent routes (the lab module grid.py uses the closed forms):
- per-unit results by converting to volts, amperes and ohms and back;
- line inductance by integrating B·dx from the conductor surface to the spacing (plus the internal term), and
  capacitance by integrating E·dx; SIL by the reactive balance I²ωL = V²ωC;
- two-bus power flow from complex phasors, S = V I*; voltage drop checked against the exact phasor solution;
- unbalanced faults by building the phase currents from sequence networks with the operator a = 1∠120°;
- RoCoF and frequency response by integrating the swing equation with solve_ivp; droop sharing by solving the
  power balance with a root finder; the Ferranti ratio from the ABCD parameters of a distributed lossless line.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "22-12-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import grid  # noqa: E402

v = Verifier.from_files("22-12", ROOT / "chapters" / "22-12-power-systems-fundamentals.md",
                        ROOT / "solutions" / "22-12-solutions.md", LAB / "README.md")
MU0, EPS0, C0 = 4e-7 * math.pi, 8.854187817e-12, 299792458.0
SQ3 = math.sqrt(3)


# ---------------------------------------------------------------- helpers
def base(s_va, v_ll):
    """Base impedance and current from one-phase quantities (V_ph, S/3) rather than the line formulas."""
    v_ph = v_ll / SQ3
    i_b = (s_va / 3) / v_ph
    return v_ph / i_b, i_b


def flux_inductance(d, gmr):
    # external flux from the GMR to the spacing: ∫ μ0 i/(2π x) dx per unit current
    return integrate.quad(lambda x: MU0 / (2 * math.pi * x), gmr, d)[0]


def field_capacitance(d, r):
    v_per_q = integrate.quad(lambda x: 1 / (2 * math.pi * EPS0 * x), r, d)[0]
    return 1 / v_per_q


def two_bus_phasor(v1, v2, x, delta_deg):
    a1 = v1 * cmath.exp(1j * math.radians(delta_deg))
    a2 = complex(v2)
    i = (a1 - a2) / (1j * x)
    s1 = a1 * i.conjugate()
    s2 = a2 * i.conjugate()
    return s1.real, s1.imag, s2.imag


def slg_from_sequences(z1, z2, z0, vf=1.0):
    i1 = vf / (z1 + z2 + z0)
    i2 = i1
    i0 = i1
    a = cmath.exp(2j * math.pi / 3)
    ia = i0 + i1 + i2
    ib = i0 + a * a * i1 + a * i2
    ic = i0 + a * i1 + a * a * i2
    assert abs(ib) < 1e-12 and abs(ic) < 1e-12
    return abs(ia)


def swing(dp, ek, s=None, r=0.05, t_gov=5.0, d_load=1000.0, f0=60.0, t_end=60.0, governor=True):
    s = s if s is not None else 50e3
    def f(t, y):
        df, pg = y
        dpg = ((-(s / (r * f0)) * df - pg) / t_gov) if governor else 0.0
        return [(pg - dp - d_load * df) * f0 / (2 * ek), dpg]
    return integrate.solve_ivp(f, (0, t_end), [0.0, 0.0], max_step=0.002, rtol=1e-10, atol=1e-12, dense_output=True)


# ---------------------------------------------------------------- Example 22-12.1 and 22-12.2
zb230, ib230 = base(100e6, 230e3)
zb138, ib138 = base(100e6, 13.8e3)
v.check("Ex 22-12.1a", zb230)
v.check("Ex 22-12.1b", zb138)
v.check("Ex 22-12.1c", ib230)
v.check("Ex 22-12.1d", ib138)
v.check("Ex 22-12.1e", 50 / zb230)
z_ohm = 0.08 * base(50e6, 230e3)[0]                      # the transformer in ohms on its own base
v.check("Ex 22-12.2", z_ohm / zb230)

# ---------------------------------------------------------------- Example 22-12.3
L3 = flux_inductance(8.0, 0.10)
C3 = field_capacitance(8.0, 0.12)
v.check("Ex 22-12.3a", L3 * 1e6)
v.check("Ex 22-12.3b", C3 * 1e12)
v.check("Ex 22-12.3c", 2 * math.pi * 60 * L3 * 1e3)
zc = optimize.brentq(lambda z: (1 / z) ** 2 * L3 - C3, 10, 1000)       # reactive balance: (V/Z)² L = V² C
v.check("Ex 22-12.3d", zc)
v.check("Ex 22-12.3e", 345e3 ** 2 / zc / 1e6)
v.check("Ex 22-12.3f", 1 / math.sqrt(L3 * C3) / C0)

# ---------------------------------------------------------------- Example 22-12.4
p4, q1, q2 = two_bus_phasor(1.0, 0.98, 0.1, 10)
v.check("Ex 22-12.4a", p4)
v.check("Ex 22-12.4b", p4 * 100)
v.check("Ex 22-12.4c", q1)
v.check("Ex 22-12.4d", q2)
v.check("Ex 22-12.4e", -optimize.minimize_scalar(lambda d: -two_bus_phasor(1.0, 0.98, 0.1, d)[0],
                                                  bounds=(0, 180), method="bounded").fun)
v.check("Ex 22-12.4f", q1 - q2)
i4 = abs((cmath.exp(1j * math.radians(10)) - 0.98) / 0.1j)
v.assert_true("Ex 22-12.4: reactive loss equals I²X", abs((q1 - q2) - i4 ** 2 * 0.1) < 1e-9)

# ---------------------------------------------------------------- Examples 22-12.5 and 22-12.6
z_th = 0.20j + 0.10j
i3 = abs(1 / z_th)
v.check("Ex 22-12.5a", i3)
v.check("Ex 22-12.5b", i3 * ib230)
v.check("Ex 22-12.5c", i3 * 100)
v.check("Ex 22-12.5d", i3 * ib138 / 1e3)
islg = slg_from_sequences(0.30j, 0.30j, 0.15j)
v.check("Ex 22-12.6a", islg)
v.check("Ex 22-12.6b", islg * ib230)

# ---------------------------------------------------------------- Example 22-12.7 (RoCoF from the swing equation)
def initial_rocof(dp, ek):
    sol = swing(dp, ek, governor=False, d_load=0.0, t_end=0.01)
    return -(sol.sol(0.01)[0] - sol.sol(0.0)[0]) / 0.01


r4, r2 = initial_rocof(1800, 4 * 50e3), initial_rocof(1800, 2 * 50e3)
v.check("Ex 22-12.7a", r4)
v.check("Ex 22-12.7b", 0.5 / r4)
v.check("Ex 22-12.7c", r2)
v.check("Ex 22-12.7d", 0.5 / r2)
v.check("Ex 22-12.7e", initial_rocof(2805, 100e3))

# ---------------------------------------------------------------- Example 22-12.8
def droop_balance(dp, units, d_load=0.0, f0=60.0):
    return optimize.brentq(lambda df: sum(-(s / (r * f0)) * df for s, r in units) - d_load * df - dp, -10, 10)


v.check("Ex 22-12.8a", droop_balance(50, [(500, 0.05)]))
v.check("Ex 22-12.8b", droop_balance(50, [(500, 0.05)] * 10))

# ---------------------------------------------------------------- Example 22-12.9 (exact phasor check of the drop)
p9, pf9 = 300e6, 0.98
i9 = p9 / (SQ3 * 230e3 * pf9)
q9 = p9 * math.tan(math.acos(pf9))
x9 = 0.489 * 20
r9 = x9 / 8.9
v.check("Ex 22-12.9a", i9)
v.check("Ex 22-12.9b", q9 / 1e6)
v.check("Ex 22-12.9c", x9)
v.check("Ex 22-12.9d", r9)
dv9 = (r9 * p9 + x9 * q9) / 230e3
v.check("Ex 22-12.9e", dv9 / 1e3)
v.check("Ex 22-12.9f", 100 * dv9 / 230e3)
v.check("Ex 22-12.9g", 3000 / 300)
# exact: receiving end at 230 kV, current at -acos(pf): sending-end magnitude minus receiving
vr = 230e3 / SQ3
ip = i9 * cmath.exp(-1j * math.acos(pf9))
vs = vr + ip * (r9 + 1j * x9)
dv_exact = (abs(vs) - vr) * SQ3
v.check("Ex 22-12.9h", dv_exact / 1e3)
v.check("Ex 22-12.9i", 100 * dv_exact / 230e3)
dq = (x9 * p9 - r9 * q9) / 230e3
v.check("Ex 22-12.9j", dq / 1e3)
v.check("Ex 22-12.9k", dq ** 2 / (2 * 230e3) / 1e3)
v.assert_true("Ex 22-12.9: first-order drop plus the quadrature correction is within 0.5% of exact",
              abs(dv9 + dq ** 2 / (2 * 230e3) - dv_exact) / dv_exact < 5e-3)
v.check("Txt 22-12.a", 10.4 + 6.8)

# ---------------------------------------------------------------- Lab (frequency response)
def nadir(ek):
    sol = swing(1800, ek)
    tt = np.linspace(0, 60, 600001)
    df = sol.sol(tt)[0]
    k = int(np.argmin(df))
    return -df[k], tt[k], df[-1]


n4, t4, ss4 = nadir(4 * 50e3)
n2, t2, _ = nadir(2 * 50e3)
v.check("Lab 22-12.a", n4)
v.check("Lab 22-12.b", t4)
v.check("Lab 22-12.c", ss4)
v.check("Lab 22-12.d", n2)
v.check("Lab 22-12.e", t2)
v.assert_true("grid.droop_df agrees with the settled simulation",
              abs(grid.droop_df(1800, [(50e3, 0.05)], d_load=1000.0) - ss4) < 1e-4)

# ---------------------------------------------------------------- Problems
zb500, ib500 = base(500e6, 500e3)
v.check("22-12.1a", zb500)
v.check("22-12.1b", ib500)
v.check("22-12.1c", 25 / zb500)
x_ohm = 0.15 * base(200e6, 20e3)[0]
v.check("22-12.2", x_ohm / base(100e6, 22e3)[0])
v.check("22-12.3", 10 * (138 / 13.8) ** 2)
v.check("22-12.4a", 500e3 ** 2 / 250 / 1e6)
v.check("22-12.4b", 1.75 * 500e3 ** 2 / 250 / 1e6)
d5 = optimize.brentq(lambda d: two_bus_phasor(1.02, 1.0, 0.25, d)[0] - 2.0, 0, 90)
v.check("22-12.5a", d5)
v.check("22-12.5b", two_bus_phasor(1.02, 1.0, 0.25, d5)[2])
v.check("22-12.5c", two_bus_phasor(1.02, 1.0, 0.25, d5)[1])
v.check("22-12.5d", two_bus_phasor(1.02, 1.0, 0.25, d5)[1] - two_bus_phasor(1.02, 1.0, 0.25, d5)[2])
dv6 = (2 * 30e6 + 8 * 10e6) / 69e3
v.check("22-12.6a", dv6)
v.check("22-12.6b", 100 * dv6 / 69e3)
zs = 100 / 5000
v.check("22-12.7a", zs)
v.check("22-12.7b", 100 / (zs + 0.10))
v.check("22-12.7c", (1 / (zs + 0.10)) * base(100e6, 13.8e3)[1] / 1e3)
v.check("22-12.8a", abs(1 / 0.12j))
v.check("22-12.8b", slg_from_sequences(0.12j, 0.12j, 0.06j))
v.check("22-12.8c", slg_from_sequences(0.12j, 0.12j, 0.06j) / abs(1 / 0.12j))
v.check("22-12.9a", initial_rocof(3000, 5 * 100e3))
v.check("22-12.9b", initial_rocof(3000, 3 * 100e3))
df10 = droop_balance(80, [(300, 0.04), (500, 0.05)])
v.check("22-12.10a", df10)
v.check("22-12.10b", -(300 / (0.04 * 60)) * df10)
v.check("22-12.10c", -(500 / (0.05 * 60)) * df10)
v.check("22-12.11a", initial_rocof(1500, 400e3))
v.check("22-12.11b", optimize.brentq(lambda df: 25e3 * df - 1500, -1, 1))
v.check("22-12.12a", 192 / 0.047)
v.check("22-12.12b", 649 / 0.118)
beta = 2 * math.pi * 60 / (0.979 * C0)          # wave speed from Example 22-12.3, rounded as published
a_param = math.cos(beta * 300e3)                 # ABCD 'A' of a lossless line: V_S = A V_R at no load
v.check("22-12.13", 1 / a_param)

# ---------------------------------------------------------------- Problem 22-12.14 (line parameters by integration)
MU0, EPS0 = 4e-7 * math.pi, 8.8541878128e-12
r14, d14 = 0.014, 7.0
lam_int = integrate.quad(lambda x: MU0 * x / (2 * math.pi * r14**2) * (x / r14) ** 2, 0, r14)[0]  # per amp
lam_ext = integrate.quad(lambda x: MU0 / (2 * math.pi * x), r14, d14)[0]
l14 = lam_int + lam_ext                        # balanced phases cancel the far-field terms
v.check("22-12.14a", 1e3 * d14 / math.exp(l14 * 2 * math.pi / MU0))
v.check("22-12.14b", 1e6 * l14)
v.check("22-12.14c", 2 * math.pi * 60 * l14 * 1e3)
c14 = 1 / integrate.quad(lambda x: 1 / (2 * math.pi * EPS0 * x), r14, d14)[0]
v.check("22-12.14d", 1e12 * c14)
v.check("22-12.14e", math.sqrt(l14 / c14))
v.check("22-12.14f", 230e3**2 / math.sqrt(l14 / c14) / 1e6)

# ---------------------------------------------------------------- Problem 22-12.15 (faults solved in the phase domain)
a_op = cmath.exp(2j * math.pi / 3)
A_mat = np.array([[1, 1, 1], [1, a_op**2, a_op], [1, a_op, a_op**2]])       # phase = A @ sequence
Zseq = np.diag([0.15j, 0.30j, 0.30j])
Zabc = A_mat @ Zseq @ np.linalg.inv(A_mat)                                   # phase-domain Thevenin impedance
Eabc = np.array([1, a_op**2, a_op])                                          # prefault 1.0 pu, positive sequence


def fault(kind):
    """Solve V = E - Z I with the fault's boundary conditions as a 6x6 linear system in (V_abc, I_abc)."""
    M = np.zeros((6, 6), complex)
    rhs = np.zeros(6, complex)
    M[:3, :3] = np.eye(3)
    M[:3, 3:] = Zabc
    rhs[:3] = Eabc
    rows = {"3ph": [("V", 0), ("V", 1), ("V", 2)], "slg": [("V", 0), ("I", 1), ("I", 2)],
            "ll": [("I", 0), ("Isum", 1), ("Vdiff", 1)], "dlg": [("I", 0), ("V", 1), ("V", 2)]}[kind]
    for k, (what, ph) in enumerate(rows):
        r = 3 + k
        if what == "V":
            M[r, ph] = 1
        elif what == "I":
            M[r, 3 + ph] = 1
        elif what == "Isum":
            M[r, 4], M[r, 5] = 1, 1
        elif what == "Vdiff":
            M[r, 1], M[r, 2] = 1, -1
    if kind == "3ph":  # a bolted 3-phase fault to a common point: V_a = V_b = V_c = 0
        pass
    x = np.linalg.solve(M, rhs)
    return x[:3], x[3:]


ib230p = 100e6 / (math.sqrt(3) * 230e3)
for key_pu, key_a, kind, sel in (("22-12.15a", "22-12.15b", "3ph", lambda I: abs(I[0])),
                                 ("22-12.15c", "22-12.15d", "slg", lambda I: abs(I[0])),
                                 ("22-12.15e", "22-12.15f", "ll", lambda I: abs(I[1])),
                                 ("22-12.15g", "22-12.15h", "dlg", lambda I: abs(I[1]))):
    _, I_f = fault(kind)
    v.check(key_pu, sel(I_f))
    v.check(key_a, sel(I_f) * ib230p)
_, I_dlg = fault("dlg")
v.assert_true("DLG: both faulted phases carry the same magnitude", abs(abs(I_dlg[1]) - abs(I_dlg[2])) < 1e-9)
v.check("22-12.15i", abs(I_dlg.sum()))
v.check("22-12.15j", abs(I_dlg.sum()) * ib230p)

v.finish()
