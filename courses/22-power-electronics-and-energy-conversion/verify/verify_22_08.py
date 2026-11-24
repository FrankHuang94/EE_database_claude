#!/usr/bin/env python3
"""Verify every number in chapter 22-08 (PMICs and power management for SoCs), its problems and its lab.

Independent routes (the lab module pmic.py uses the closed-form expressions):
- efficiencies are computed by explicit power flow (input and output power of each stage);
- PFM/PWM crossovers by root finding on the difference of the two loss models;
- battery budgets by integrating a second-by-second power timeline over a day;
- DVS ramps, PFM down-ramps, soft start and power-gating recharge by integrating the capacitor ODEs
  (scipy solve_ivp) and the dissipated or delivered power along the trajectory;
- the DVS ramp lead by simulating the averaged buck with the type-III network and an ideal op-amp as a set of
  state equations (inductor, output and three compensation capacitors), and also by the final-value theorem
  on the closed-loop transfer function built from the network's impedances;
- sequencing by an event schedule; gating break-even by root finding on cumulative leakage energy.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "22-08-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import pmic  # noqa: E402

v = Verifier.from_files("22-08", ROOT / "chapters" / "22-08-pmics.md",
                        ROOT / "solutions" / "22-08-solutions.md", LAB / "README.md")


# ---------------------------------------------------------------- helpers
def chain_power_flow(p_out, v_out, stages, v_in):
    """stages: list of ('ldo', None) or ('buck', eta), applied from the load back to the source. Returns η."""
    i_out, v_node, p = p_out / v_out, v_out, p_out
    for kind, eta, v_up in stages:
        if kind == "ldo":            # same current, higher voltage
            p = v_up * i_out
        else:                        # buck: power divided by efficiency, current changes
            p = p / eta
        i_out, v_node = p / v_up, v_up
    return p_out / p


def crossover(p_f, r, v_in, i_q, alpha, r_p):
    diff = lambda i: (p_f + r * i * i) - (v_in * i_q + alpha * i + r_p * i * i)
    return optimize.brentq(diff, 1e-9, 10.0, xtol=1e-14)


def timeline_energy(states, v_bat, i_q, dt=1.0):
    """Build a day of 1 s samples: each state (P, seconds, η) occupies consecutive samples."""
    p_in = np.concatenate([np.full(int(round(t / dt)), p / eta) for p, t, eta in states])
    assert abs(len(p_in) * dt - 86400) < 1e-6
    return np.sum(p_in) * dt + v_bat * i_q * len(p_in) * dt


def ramp_sim(c, v1, v2, slew):
    """Capacitor driven up a ramp of slew S; returns (time to reach v2, charging current C dv/dt, ∫ v i dt)."""
    def f(t, y):                     # y = [v, energy delivered to the capacitor]
        return [slew, y[0] * c * slew]
    ev = lambda t, y: y[0] - v2
    ev.terminal = True
    sol = integrate.solve_ivp(f, (0, 10 * abs(v2 - v1) / slew), [v1, 0.0], events=ev, rtol=1e-12, atol=1e-16)
    i_c = c * np.gradient(sol.y[0], sol.t).mean()
    return sol.t_events[0][0], i_c, sol.y_events[0][0][1]


def discharge_time(c, v_hi, v_lo, i_load):
    ev = lambda t, y: y[0] - v_lo
    ev.terminal = True
    sol = integrate.solve_ivp(lambda t, y: [-i_load / c], (0, 1.0), [v_hi], events=ev, rtol=1e-12, atol=1e-15)
    return sol.t_events[0][0]


def switch_charge(c, v, r_on, i_lim=None, t_end=None):
    """Charge c from a v source through a resistive (optionally current-limited) switch.
    Returns (switch energy, supply energy, peak current, time to 0.99 v)."""
    def cur(vc):
        i = (v - vc) / r_on
        return min(i, i_lim) if i_lim is not None else i

    def f(t, y):
        i = cur(y[0])
        return [i / c, (v - y[0]) * i, v * i]
    t_end = t_end or 20 * c * (r_on + (v / i_lim if i_lim else 0))
    ev = lambda t, y: y[0] - 0.99 * v
    sol = integrate.solve_ivp(f, (0, t_end), [0.0, 0.0, 0.0], method="LSODA", rtol=1e-10, atol=1e-14,
                              events=ev, max_step=t_end / 2000)
    return sol.y[1, -1], sol.y[2, -1], cur(0.0), sol.t_events[0][0]


# ---------------------------------------------------------------- Example 22-08.1
p_out = 1.2 * 0.1
eta_a = chain_power_flow(p_out, 1.2, [("ldo", None, 3.8)], 3.8)
eta_b = chain_power_flow(p_out, 1.2, [("ldo", None, 1.8), ("buck", 0.90, 3.8)], 3.8)
eta_d = chain_power_flow(p_out, 1.2, [("ldo", None, 1.5), ("buck", 0.90, 3.8)], 3.8)
v.check("Ex 22-08.1a", 100 * eta_a)
v.check("Ex 22-08.1b", 100 * eta_b)
v.check("Ex 22-08.1c", 88.0)
v.check("Ex 22-08.1d", 100 * (eta_d - eta_b))
v.assert_true("Ex 22-08.1 lab helper agrees", abs(pmic.chain_efficiency(0.9, 1.2, 1.8) - eta_b) < 1e-12)

# ---------------------------------------------------------------- Example 22-08.2
i_x = crossover(20e-3, 0.2, 3.6, 1e-6, 0.12, 0.6)
v.check("Ex 22-08.2a", i_x * 1e3)
for key, i, mode in (("b", 1e-3, "pwm"), ("c", 1e-3, "pfm"), ("d", 0.3, "pwm"), ("e", 0.3, "pfm")):
    po = 1.8 * i
    loss = 20e-3 + 0.2 * i * i if mode == "pwm" else 3.6 * 1e-6 + 0.12 * i + 0.6 * i * i
    v.check(f"Ex 22-08.2{key}", 100 * po / (po + loss))
v.assert_true("Ex 22-08.2 lab crossover agrees",
              abs(pmic.pfm_pwm_crossover(20e-3, 0.2, 3.6, 1e-6, 0.12, 0.6) - i_x) < 1e-9)

# ---------------------------------------------------------------- Example 22-08.3
band = [(50e-6, 82800, 0.80), (15e-3, 3300, 0.88), (150e-3, 300, 0.90)]
e_states = [integrate.quad(lambda t, p=p, eta=eta: p / eta, 0, tt)[0] for p, tt, eta in band]
e_q = integrate.quad(lambda t: 3.85 * 1e-6, 0, 86400)[0]
e_tot = timeline_energy(band, 3.85, 1e-6)
e_bat = 300e-3 * 3600 * 3.85
for key, e in zip("abc", e_states):
    v.check(f"Ex 22-08.3{key}", e)
v.check("Ex 22-08.3d", e_q)
v.check("Ex 22-08.3e", e_tot)
v.check("Ex 22-08.3f", e_bat / e_tot)
v.check("Ex 22-08.3g", e_bat)
v.assert_true("Ex 22-08.3 sum of states equals the timeline", abs(sum(e_states) + e_q - e_tot) < 1e-6)

# ---------------------------------------------------------------- Example 22-08.4
t_up, i_c, e_c = ramp_sim(200e-6, 0.6, 0.9, 10e3)
v.check("Ex 22-08.4a", t_up * 1e6)
v.check("Ex 22-08.4b", i_c)
v.check("Ex 22-08.4c", e_c * 1e6)
v.check("Ex 22-08.4d", 1 / 200e-6 / 1e3)        # (A/F) in V/s → mV/µs
v.check("Ex 22-08.4e", discharge_time(200e-6, 0.9, 0.6, 1.0) * 1e6)

# ---------------------------------------------------------------- Example 22-08.5
# Dynamic energy per cycle of a switched capacitance C at V is C V²; the ratio does not depend on C.
cyc = lambda vv: integrate.quad(lambda x: 1e-9 * vv, 0, vv)[0] * 2
v.check("Ex 22-08.5a", 0.75 + 0.020)
v.check("Ex 22-08.5b", cyc(0.77) / cyc(0.81))
v.check("Ex 22-08.5c", 100 * (1 - cyc(0.77) / cyc(0.81)))

# ---------------------------------------------------------------- Example 22-08.6
c6, v6 = 100e-6, 1.0
for key, t_r in (("a", 1e-3), ("b", 10e-6)):
    _, i_r, _ = ramp_sim(c6, 0.0, v6, v6 / t_r)
    v.check(f"Ex 22-08.6{key}", i_r)
e_hard, sup_hard, ipk_hard, _ = switch_charge(c6, v6, 0.1)
e_soft, sup_soft, ipk_soft, t99 = switch_charge(c6, v6, 0.1, i_lim=0.1, t_end=3e-3)
v.check("Ex 22-08.6c", e_hard * 1e6)
v.assert_true("Ex 22-08.6c soft start dissipates the same energy", abs(e_soft - e_hard) < 1e-3 * e_hard)
v.assert_true("Ex 22-08.6 supply delivers C V² (half stored, half dissipated)",
              abs(sup_hard - c6 * v6 ** 2) < 1e-3 * c6 and abs(sup_soft - c6 * v6 ** 2) < 1e-3 * c6)
v.check("Ex 22-08.6d", ipk_hard)

# ---------------------------------------------------------------- Example 22-08.7
_, sup7, _, _ = switch_charge(20e-9, 0.8, 1.0, t_end=1e-6)
v.check("Ex 22-08.7a", sup7 * 1e9)


def breakeven(e_wake, p_leak):
    return optimize.brentq(lambda t: integrate.quad(lambda x: p_leak, 0, t)[0] - e_wake, 0, 1.0, xtol=1e-15)


v.check("Ex 22-08.7b", breakeven(sup7, 5e-3) * 1e6)
v.check("Ex 22-08.7c", breakeven(sup7 + 1e-6, 5e-3) * 1e6)


# ---------------------------------------------------------------- DVS ramp lead: state-space simulation
VG, VM, LB, CB, RL = 12.0, 1.0, 0.6e-6, 62.5e-6, 0.12
R1, R2, C1, C2, R3, C3 = 10e3, 992.3005, 11.236714e-9, 0.6740832e-9, 599.89353, 1.0519160e-9


def dvs_lead(slew, t_ramp_meas):
    """Averaged buck + type-III network around an ideal op-amp (inverting node held at v_ref).
    States: iL, vout, vC3 (across C3), vC1 (across C1), vC2 (= v_ref − v_c). Reference ramps from t = 0."""
    vref = lambda t: 1.0 + slew * t

    def f(t, y):
        il, vo, v3, v1, v2 = y
        vr = vref(t)
        i_r3 = (vo - vr - v3) / R3
        i_in = (vo - vr) / R1 + i_r3
        i_r2 = (v2 - v1) / R2
        vc = vr - v2
        return [(VG * vc / VM - vo) / LB, (il - vo / RL) / CB, i_r3 / C3, i_r2 / C1, (i_in - i_r2) / C2]
    y0 = [1.0 / RL, 1.0, 0.0, 1.0 - VM / VG, 1.0 - VM / VG]
    sol = integrate.solve_ivp(f, (0, t_ramp_meas), y0, method="Radau", rtol=1e-10, atol=1e-13)
    return sol.y[1, -1] - vref(t_ramp_meas)


lead_02 = dvs_lead(200.0, 0.5e-3)
lead_10 = dvs_lead(1000.0, 0.5e-3)


# Final-value route: e = S lim_{s→0} (H(s) − 1)/s with H = G(1 + K)/(1 + G K)
def h_minus_1_over_s(s):
    g = (VG / VM) / (1 + s * LB / RL + s * s * LB * CB)
    zf = 1 / (1 / (R2 + 1 / (s * C1)) + s * C2)
    zi = 1 / (1 / R1 + 1 / (R3 + 1 / (s * C3)))
    k = zf / zi
    return (g * (1 + k) / (1 + g * k) - 1) / s


fv = np.real(h_minus_1_over_s(1e-3 * 1j) + h_minus_1_over_s(-1e-3 * 1j)) / 2
w_i = 1 / (R1 * (C1 + C2))
v.assert_true("DVS lead: simulation matches the final-value theorem", abs(lead_02 - 200 * fv) < 1e-3 * lead_02)
v.assert_true("DVS lead: closed form S(1 − V_M/V_g)/ω_I matches", abs(lead_02 - 200 / w_i * (1 - VM / VG)) < 2e-3 * lead_02)
v.assert_true("DVS lead: ω_I of the network is 8396 rad/s", round(w_i) == 8396)
v.check("Lab 22-08.a", lead_02 * 1e3)

# ---------------------------------------------------------------- Lab soft start and battery budget
v.check("Lab 22-08.b", t99 * 1e3)
v.check("Lab 22-08.c", 100 * (e_states[1] + e_states[2]) / e_tot)
half_sleep = [(25e-6, 82800, 0.80)] + band[1:]
v.check("Lab 22-08.d", e_bat / timeline_energy(half_sleep, 3.85, 1e-6))
v.check("Lab 22-08.e", e_bat / timeline_energy(band, 3.85, 0.5e-6))
half_loss = [band[0]] + [(p, t, 1 / (1 + (1 / eta - 1) / 2)) for p, t, eta in band[1:]]
v.check("Lab 22-08.f", e_bat / timeline_energy(half_loss, 3.85, 1e-6))

# ---------------------------------------------------------------- Problems
v.check("22-08.1", 100 * chain_power_flow(1.0, 1.0, [("ldo", None, 1.15), ("buck", 0.92, 3.8)], 3.8))

i_bat = 10e-6 + 0.5e-6
v.check("22-08.2a", i_bat * 1e6)
v.check("22-08.2b", 100 * (0.9 * 10e-6) / (3.8 * i_bat))
v.check("22-08.2c", 3.8 * i_bat * 1e6)

v.check("22-08.3", crossover(12e-3, 0.15, 3.8, 0.5e-6, 0.10, 0.45) * 1e3)

node = [(2e-6, 0.999 * 86400, 0.70), (30e-3, 0.001 * 86400, 0.85)]
e_node_bat = 0.220 * 3600 * 3.0
p_avg = timeline_energy([(p, t, eta) for p, t, eta in node], 3.0, 300e-9, dt=0.1) / 86400
v.check("22-08.4a", e_node_bat)
v.check("22-08.4b", p_avg * 1e6)
v.check("22-08.4c", e_node_bat / p_avg / 86400)
v.check("22-08.4d", 100 * (0.999 * 2e-6 / 0.70) / p_avg)
v.check("22-08.4e", 100 * (3.0 * 300e-9) / p_avg)

t5, i5, e5 = ramp_sim(470e-6, 0.5, 0.8, 5e3)
v.check("22-08.5a", t5 * 1e6)
v.check("22-08.5b", i5)
v.check("22-08.5c", e5 * 1e6)
v.check("22-08.6", discharge_time(470e-6, 0.8, 0.5, 0.5) * 1e6)

r7 = cyc(0.925) / cyc(0.975)
v.check("22-08.7a", r7)
v.check("22-08.7b", 100 * (1 - r7))

v.check("22-08.8a", lead_02 * 1e3)
v.check("22-08.8b", lead_10 * 1e3)

e9, _, _, _ = switch_charge(47e-6, 1.8, 1e-3, i_lim=0.5, t_end=1e-3)
_, i9, _ = ramp_sim(47e-6, 0.0, 1.8, 0.5 / 47e-6)
t9 = optimize.brentq(lambda t: 0.5 * t / 47e-6 - 1.8, 0, 1)      # current-limited charge reaches 1.8 V
v.check("22-08.9a", t9 * 1e6)
v.check("22-08.9b", e9 * 1e6)
v.assert_true("22-08.9 the limited ramp draws exactly 0.5 A", abs(i9 - 0.5) < 1e-12)


def schedule(n, groups, t_ss=400e-6, t_pg=100e-6):
    """Event schedule: rails in each group start together; the next group starts at the previous power-good."""
    per = math.ceil(n / groups)
    t, done = 0.0, 0
    while done < n:
        starts = [t] * min(per, n - done)
        t = max(s + t_ss + t_pg for s in starts)
        done += len(starts)
    return t


v.check("22-08.10a", schedule(5, 5) * 1e3)
v.check("22-08.10b", schedule(5, 2) * 1e3)

_, sup11, _, _ = switch_charge(50e-9, 0.75, 1.0, t_end=2e-6)
p85 = 2e-3 * math.exp(math.log(2) * (85 - 25) / 25)
v.check("22-08.11a", sup11 * 1e9)
v.check("22-08.11b", breakeven(sup11 + 0.5e-6, 2e-3) * 1e6)
v.check("22-08.11c", p85 * 1e3)
v.check("22-08.11d", breakeven(sup11 + 0.5e-6, p85) * 1e6)

p_ldo = 3.8 * 0.2 - 1.8 * 0.2
p_buck = 1.8 * 0.2 / 0.9 - 1.8 * 0.2
v.check("22-08.12a", p_ldo)
v.check("22-08.12b", p_buck)
v.check("22-08.12c", p_ldo - p_buck)
v.check("22-08.12d", integrate.quad(lambda t: p_ldo - p_buck, 0, 7200)[0])
v.check("22-08.12e", 100 * (p_ldo - p_buck) * 7200 / e_bat)

# ---------------------------------------------------------------- text values derived from data-sheet figures
v.check("Txt 22-08.a", schedule(16, 16, t_ss=10e-3, t_pg=0.0) * 1e3)
v.check("Txt 22-08.b", 4.0e-3 / 800e-9)
t_up_219, _, _ = ramp_sim(1e-6, 0.6, 1.4, 3.2e3)
t_dn_219 = optimize.brentq(lambda t: 1.4 - 0.53e3 * t - 0.6, 0, 1)
v.check("Txt 22-08.c", t_up_219 * 1e6)
v.check("Txt 22-08.d", t_dn_219 * 1e3)
v.check("Txt 22-08.e", t_dn_219 / t_up_219)
_, i_fast, _ = ramp_sim(200e-6, 0.6, 0.9, 33.3e3)
v.check("Txt 22-08.f", i_fast)
v.check("Txt 22-08.g", cyc(0.605) / cyc(0.898))
v.check("Txt 22-08.h", 100 * e_q / e_tot)

# ---------------------------------------------------------------- lab helpers agree with the independent routes
v.assert_true("pmic.ramp_lead agrees with the simulation", abs(pmic.ramp_lead(200, w_i, VM, VG) - lead_02) < 2e-3 * lead_02)
v.assert_true("pmic.soft_start agrees", abs(pmic.soft_start(c6, v6, 0.1)[1] - e_soft) < 1e-3 * e_soft)
v.assert_true("pmic.gating_breakeven agrees",
              abs(pmic.gating_breakeven(50e-9, 0.75, 0.5e-6, pmic.leakage_at(2e-3, 85)) - breakeven(sup11 + 0.5e-6, p85)) < 1e-9)
v.assert_true("pmic.daily_energy agrees", abs(pmic.daily_energy(band, 3.85, 1e-6)[2] - e_tot) < 1e-6)

v.finish()
