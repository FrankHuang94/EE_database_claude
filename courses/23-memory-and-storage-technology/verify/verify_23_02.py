#!/usr/bin/env python3
"""Verify every number in chapter 23-02 (SRAM technology), its problems and its lab.

Independent routes (the lab module sramtech.py uses closed forms and brentq on the same balance equations):
- cell-node voltages by integrating the node's charging ODE, C dV/dt = I_in - I_out, to steady state with an
  independently written square-law current, and the inverter threshold by integrating its self-connected node;
- sigma by integrating the normal density numerically and root finding;
- Vmin by root finding on mean margin = k sigma;
- bitline times by integrating a constant-current discharge until it reaches the sense voltage;
- Poisson repair by summing the Poisson terms explicitly;
- the read-disturb closed form for any cell ratio against root finding on the current balance.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "23-02-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import sramtech as st  # noqa: E402

v = Verifier.from_files("23-02", ROOT / "chapters" / "23-02-sram-technology.md",
                        ROOT / "solutions" / "23-02-solutions.md", LAB / "README.md")


# ---------------------------------------------------------------- independent helpers
def i_sq(k, vg, vs, vd, vt):
    """Square-law current from drain to source of an n-type device with terminals at absolute voltages."""
    vgs, vds = vg - vs, vd - vs
    if vds < 0:  # swap roles so the formula sees a positive vds
        return -i_sq(k, vg, vd, vs, vt)
    vov = vgs - vt
    if vov <= 0:
        return 0.0
    return 0.5 * k * vov ** 2 if vds >= vov else k * (vov * vds - 0.5 * vds ** 2)


def i_sq_p(k, vg, vs, vd, vt):
    """Square-law current from source to drain of a p-type device (vt is |V_TP|)."""
    return i_sq(k, -vg, -vs, -vd, vt)


def settle(dvdt, v0, c=1e-15, t_end=5e-9):
    """Integrate C dV/dt = I(V) from v0 until it settles; return the final voltage."""
    sol = integrate.solve_ivp(lambda t, y: [dvdt(y[0]) / c], (0, t_end), [v0], rtol=1e-11, atol=1e-14,
                              method="LSODA")
    return float(sol.y[0, -1])


def vm_sim(vdd, kn, kp, vtn, vtp):
    """Self-connected inverter: the node charges until pull-up and pull-down currents balance."""
    return settle(lambda x: i_sq_p(kp, x, vdd, x, vtp) - i_sq(kn, x, 0.0, x, vtn), vdd / 2)


def write_sim(vdd, k_pg, k_pu, vt_pg, vt_pu, v_bl=0.0):
    """The written node starts at vdd; the pass gate (gate vdd) discharges it, the pull-up (gate 0) charges it."""
    return settle(lambda x: i_sq_p(k_pu, 0.0, vdd, x, vt_pu) - i_sq(k_pg, vdd, v_bl, x, vt_pg), vdd)


def write_bal(vdd, k_pg, k_pu, vt_pg, vt_pu, v_bl=0.0):
    """Faster route for root-finding loops: the same balance solved with brentq on the independent currents."""
    return optimize.brentq(lambda x: i_sq_p(k_pu, 0.0, vdd, x, vt_pu) - i_sq(k_pg, vdd, v_bl, x, vt_pg), v_bl, vdd,
                           xtol=1e-13)


def read_sim(vdd, k_pg, k_pd, vt_pg, vt_pd, v_wl):
    """The 0 node starts at 0; the pass gate from the vdd bitline charges it, the pull-down (gate vdd) holds it."""
    return settle(lambda x: i_sq(k_pg, v_wl, x, vdd, vt_pg) - i_sq(k_pd, vdd, 0.0, x, vt_pd), 0.0)


def q_tail(x):
    return integrate.quad(lambda u: math.exp(-u * u / 2) / math.sqrt(2 * math.pi), x, np.inf)[0]


def sigma_for(n_bits, y=0.99):
    target = -math.log(y) / n_bits
    return optimize.brentq(lambda k: math.log(q_tail(k)) - math.log(target), 1, 12, xtol=1e-12)


def vmin_root(k, sig_mv, slope=0.2, v0=0.25, g=0.6):
    return optimize.brentq(lambda vv: slope * (vv - v0) - k * g * sig_mv * 1e-3, v0, 3)


def discharge_time(c_tot, dv, i):
    """Time for a constant current i to move a capacitance c_tot by dv, by integrating dV/dt = i/c."""
    sol = integrate.solve_ivp(lambda t, y: [i / c_tot], (0, 1e-6), [0.0], events=lambda t, y: y[0] - dv,
                              rtol=1e-12, atol=1e-15, max_step=1e-11)
    return float(sol.t_events[0][0])


def poisson_cdf(m, lam):
    term, total = math.exp(-lam), math.exp(-lam)
    for j in range(1, m + 1):
        term *= lam / j
        total += term
    return total


# ---------------------------------------------------------------- Example 23-02.1
print("Examples")
v.check("Ex 23-02.1a", 1 / 0.021)
v.check("Ex 23-02.1b", 100 * 38.1 * 0.021)
v.check("Ex 23-02.1c", 100 * (0.021 - 0.0199) / 0.021)
v.check("Ex 23-02.1d", 1 / 0.017)
v.check("Ex 23-02.1e", 0.80 / 0.017)
v.check("Ex 23-02.1f", 512 / 38.1)
v.check("Txt 23-02.m", 100 * (2 ** 20 / 1e6 - 1))

# ---------------------------------------------------------------- Example 23-02.2
new2 = 0.40 / 1.0 + 0.60 / 1.6
v.check("Ex 23-02.2a", 100 * new2)
v.check("Ex 23-02.2b", 100 * 0.40 / new2)
v.check("Ex 23-02.2c", 1 / new2)

# ---------------------------------------------------------------- Example 23-02.3
k1, k64 = sigma_for(2 ** 23), sigma_for(2 ** 29)
v.check("Ex 23-02.3a", k1)
v.check("Ex 23-02.3b", k64)
v.check("Txt 23-02.b", k1)
v.check("Txt 23-02.c", k64)
v.check("Txt 23-02.n", k64 - k1)
s_fin, s_ns = 1.0 / math.sqrt(0.10 * 0.016), 1.0 / math.sqrt(0.15 * 0.016)
v.check("Ex 23-02.3c", s_fin)
v.check("Ex 23-02.3d", s_ns)
vm_e, vm_f, vm_g = vmin_root(k1, s_fin), vmin_root(k64, s_fin), vmin_root(k64, s_ns)
v.check("Ex 23-02.3e", vm_e)
v.check("Ex 23-02.3f", vm_f)
v.check("Ex 23-02.3g", vm_g)
v.check("Txt 23-02.d", 1e3 * (vm_f - vm_e))
v.check("Txt 23-02.e", 1e3 * (vm_f - vm_g))

# ---------------------------------------------------------------- Example 23-02.4
VDD, K, KPU = 0.7, 100e-6, 80e-6
r0, r1 = read_sim(VDD, K, K, 0.3, 0.3, 0.7), read_sim(VDD, K, K, 0.3, 0.3, 0.6)
i0, i1 = i_sq(K, 0.7, r0, VDD, 0.3), i_sq(K, 0.6, r1, VDD, 0.3)
v.check("Ex 23-02.4a", r0)
v.check("Ex 23-02.4b", r1)
v.check("Ex 23-02.4c", i0 * 1e6)
v.check("Ex 23-02.4d", i1 * 1e6)
v.check("Ex 23-02.4e", i1 / i0)
v.check("Txt 23-02.f", 100 * (1 - r1 / r0))
v.check("Txt 23-02.g", 100 * (1 - i1 / i0))
v.check("Txt 23-02.h", i0 / i1)
v.assert_true("read disturb closed form (V_DD - V_T)(1 - 1/sqrt 2)", abs(r0 - 0.4 * (1 - 1 / math.sqrt(2))) < 1e-6)

# ---------------------------------------------------------------- Example 23-02.5
vm5 = vm_sim(VDD, K, KPU, 0.3, 0.3)
w0, w1 = write_sim(VDD, K, KPU, 0.3, 0.3), write_sim(VDD, K, KPU, 0.35, 0.25)
v.check("Ex 23-02.5a", vm5)
v.check("Txt 23-02.a", math.sqrt(100 / 80))
v.check("Ex 23-02.5b", w0)
v.check("Ex 23-02.5c", w1)
v.check("Txt 23-02.i", 1e3 * (w1 - w0))
nbl5 = optimize.brentq(lambda vb: write_bal(VDD, K, KPU, 0.35, 0.25, vb) - vm5, -0.3, 0.0, xtol=1e-9)
v.assert_true("ODE and balance agree at the assist point", abs(write_sim(VDD, K, KPU, 0.35, 0.25, nbl5) - vm5) < 1e-5)
v.check("Ex 23-02.5d", 1e3 * nbl5)
v.check("Txt 23-02.k", -1e3 * nbl5)
v.assert_true("sramtech's write solver agrees with the ODE", abs(st.write_node(VDD, K, KPU, 0.35, 0.25) - w1) < 1e-6)

# ---------------------------------------------------------------- Example 23-02.6
a256, a512 = 0.021 + 1.0 / 256 + 0.0012, 0.021 + 1.0 / 512 + 0.0012
v.check("Ex 23-02.6a", a256)
v.check("Ex 23-02.6b", 1 / a256)
v.check("Ex 23-02.6c", a512)
v.check("Ex 23-02.6d", 1 / a512)
v.check("Ex 23-02.6e", 100 * (a256 / a512 - 1))
t256 = discharge_time(256 * 0.1e-15 + 5e-15, 0.1, 20e-6)
t512 = discharge_time(512 * 0.1e-15 + 5e-15, 0.1, 20e-6)
v.check("Ex 23-02.6f", t256 * 1e12)
v.check("Ex 23-02.6g", t512 * 1e12)
v.check("Ex 23-02.6h", t512 / t256)

# ---------------------------------------------------------------- Example 23-02.7
bits = 2 ** 29
i_op = bits * 5e-12
fac = math.exp(-0.25 / 0.1 * math.log(2))
v.check("Ex 23-02.7a", i_op * 1e3)
v.check("Ex 23-02.7b", i_op * 0.7 * 1e3)
v.check("Ex 23-02.7c", fac)
v.check("Ex 23-02.7d", i_op * fac * 1e3)
v.check("Ex 23-02.7e", i_op * fac * 0.45 * 1e3)
v.check("Ex 23-02.7f", (i_op * 0.7) / (i_op * fac * 0.45))
v.check("Txt 23-02.l", (i_op * 0.7) / (i_op * fac * 0.45))
v.check("Txt 23-02.j", 0.7 / 0.45)

# ---------------------------------------------------------------- problems
print("Problems")
v.check("23-02.1a", 1 / 0.0312)
v.check("23-02.1b", 1 / 0.024)
v.check("23-02.1c", 100 * (1 - 0.024 / 0.0312))
v.check("23-02.2a", 38.1 * 2 ** 20 / 1e6)
v.check("23-02.2b", 100 * 38.1 * 2 ** 20 / 1e6 * 0.021)
v.check("23-02.3", sigma_for(2 ** 21, 0.999))
new4 = 0.55 / 1.05 + 0.45 / 1.7
v.check("23-02.4a", 100 * new4)
v.check("23-02.4b", 100 * (0.55 / 1.05) / new4)
v.check("23-02.4c", 1 / new4)
r5a = read_sim(0.8, K, K, 0.32, 0.32, 0.8)
r5b = read_sim(0.8, K, 2 * K, 0.32, 0.32, 0.8)
v.check("23-02.5a", r5a)
v.check("23-02.5b", r5b)
v.check("23-02.5c", 100 * (1 - r5b / r5a))
K6, KPU6 = 120e-6, 60e-6
vm6 = vm_sim(0.75, K6, KPU6, 0.3, 0.3)
v.check("23-02.6a", vm6)
v.check("23-02.6b", write_sim(0.75, K6, KPU6, 0.3, 0.3))
v.check("23-02.6c", 1e3 * optimize.brentq(lambda d: write_bal(0.75, K6, KPU6, 0.3 + d, 0.3 - d) - vm6, 0.0, 0.2,
                                          xtol=1e-9))
v.check("23-02.6d", write_sim(0.75, K6, KPU6, 0.4, 0.2))
v.check("23-02.6e", 1e3 * optimize.brentq(lambda vb: write_bal(0.75, K6, KPU6, 0.4, 0.2, vb) - vm6, -0.3, 0.0,
                                          xtol=1e-9))
c7 = 1024 * 0.08e-15 + 4e-15
t7 = discharge_time(c7, 0.08, 25e-6)
v.check("23-02.7a", t7 * 1e12)
i7 = c7 * 0.08 / 150e-12
v.assert_true("the discharge at that current takes 150 ps", abs(discharge_time(c7, 0.08, i7) - 150e-12) < 1e-15)
v.check("23-02.7b", i7 * 1e6)
v.check("23-02.7c", i7 / 25e-6)
a128, a256b = 0.021 + 0.8 / 128 + 0.0015, 0.021 + 0.8 / 256 + 0.0015
v.check("23-02.8a", a128)
v.check("23-02.8b", 1 / a128)
v.check("23-02.8c", a256b)
v.check("23-02.8d", 1 / a256b)
v.check("23-02.8e", 100 * (a128 / a256b - 1))
k9 = sigma_for(2 ** 28)
vm9 = optimize.brentq(lambda vv: 0.25 * (vv - 0.2) - k9 * 0.5 * 0.022, 0.2, 3)
vm9e = optimize.brentq(lambda vv: 0.25 * (vv - 0.2) - 4.5 * 0.5 * 0.022, 0.2, 3)
v.check("23-02.9a", k9)
v.check("23-02.9b", vm9)
v.check("23-02.9c", vm9e)
v.check("23-02.9d", 1e3 * (vm9 - vm9e))
i10 = 2 ** 28 * 8e-12
f10 = math.exp(-0.25 / 0.09 * math.log(2))
v.check("23-02.10a", i10 * 1e3)
v.check("23-02.10b", i10 * 0.75 * 1e3)
v.check("23-02.10c", f10)
v.check("23-02.10d", i10 * f10 * 1e3)
v.check("23-02.10e", i10 * f10 * 0.5 * 1e3)
v.check("23-02.10f", 0.75 / (f10 * 0.5))
for key, beta in (("23-02.11a", 1.0), ("23-02.11b", 1.5), ("23-02.11c", 2.0)):
    root = optimize.brentq(lambda x: 0.5 * (0.4 - x) ** 2 - beta * (0.4 * x - 0.5 * x * x), 0, 0.4 * (1 - 1e-9))
    v.check(key, root)
    v.assert_true(f"closed form for beta = {beta}", abs(root - 0.4 * (1 - math.sqrt(beta / (1 + beta)))) < 1e-9)
v.check("23-02.11d", optimize.brentq(
    lambda b: optimize.brentq(lambda x: 0.5 * (0.4 - x) ** 2 - b * (0.4 * x - 0.5 * x * x), 0, 0.4 * (1 - 1e-9))
    - 0.08, 0.5, 10))
N12 = 2 ** 30
k12 = sigma_for(N12)
lam = optimize.brentq(lambda lm: poisson_cdf(100, lm) - 0.99, 1, 200)
k12r = optimize.brentq(lambda k: math.log(q_tail(k)) - math.log(lam / N12), 1, 12, xtol=1e-12)
v.check("23-02.12a", k12)
v.check("23-02.12b", vmin_root(k12, 25.0))
v.check("23-02.12c", lam)
v.check("23-02.12d", k12r)
v.check("23-02.12e", vmin_root(k12r, 25.0))
v.check("23-02.12f", 1e3 * (vmin_root(k12, 25.0) - vmin_root(k12r, 25.0)))
v.check("23-02.12g", k12 - k12r)

# ---------------------------------------------------------------- lab
print("Lab")
v.check("Lab 23-02.a", write_sim(VDD, K, KPU, 0.35, 0.25, -0.043))


def fail_mismatch(v_bl):
    return optimize.brentq(lambda d: write_bal(VDD, K, KPU, 0.3 + d, 0.3 - d, v_bl) - vm5, 0.0, 0.29, xtol=1e-10)


d0, d50 = fail_mismatch(0.0), fail_mismatch(-0.05)
v.check("Lab 23-02.b", 1e3 * d0)
v.check("Lab 23-02.c", q_tail(d0 / 0.025))
v.check("Lab 23-02.d", 1e3 * d50)
v.check("Lab 23-02.e", q_tail(d50 / 0.025))
v.check("Lab 23-02.f", 1e3 * optimize.brentq(lambda vb: write_bal(VDD, K, KPU, 0.45, 0.15, vb) - vm5, -0.6, 0.0,
                                             xtol=1e-9))

sys.exit(v.finish())
