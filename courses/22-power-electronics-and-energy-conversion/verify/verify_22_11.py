#!/usr/bin/env python3
"""Verify every number in chapter 22-11 (electric machines and drives), its problems and its lab.

Independent routes (the lab module machines.py uses the closed forms):
- DC motor operating points by solving the circuit and torque balance with a root finder, and the start-up
  transient by integrating the electrical and mechanical ODEs;
- synchronous speed by tracking the peak of the summed winding fields over time;
- the induction machine by solving the full per-phase circuit as a complex nodal system (no Thevenin reduction),
  with the Thevenin parameters found from open-circuit voltage and short-circuit current, and the maximum torque
  by numerical maximization over slip;
- synchronous-machine power from the phasor current, P = 3 Re(V I*);
- inverter voltage limits by synthesizing sine-triangle PWM leg waveforms and taking the Fourier fundamental of
  the line voltage, and the space-vector limit by min–max common-mode injection;
- rotating-field amplitudes by sampling the field over angle.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "22-11-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import machines as mc  # noqa: E402

v = Verifier.from_files("22-11", ROOT / "chapters" / "22-11-electric-machines.md",
                        ROOT / "solutions" / "22-11-solutions.md", LAB / "README.md")
RPM = 2 * math.pi / 60


# ---------------------------------------------------------------- helpers
def dc_point(v_s, r_a, k, t_load):
    """Solve V = I R + k w and k I = T for (I, w) with a root finder."""
    i = optimize.brentq(lambda ii: k * ii - t_load, -1e4, 1e4)
    w = optimize.brentq(lambda ww: v_s - i * r_a - k * ww, -1e6, 1e6)
    return i, w


def field_speed(poles, f, phases=3):
    """Track the angle of the field maximum of 'phases' windings over a short time; return mechanical rad/s."""
    pp = poles / 2
    th = np.linspace(0, 2 * math.pi / pp, 20001)                      # one electrical cycle of space
    def peak(t):
        if phases == 3:
            b = sum(math.cos(2 * math.pi * f * t - k * 2 * math.pi / 3) * np.cos(pp * th - k * 2 * math.pi / 3)
                    for k in range(3))
        else:
            b = math.cos(2 * math.pi * f * t) * np.cos(pp * th) + math.sin(2 * math.pi * f * t) * np.sin(pp * th)
        return th[np.argmax(b)], b.max()
    dt = 1e-4 / f
    (a0, _), (a1, _) = peak(0.0), peak(dt)
    return (a1 - a0) / dt


def solve_induction(vph, r1, x1, xm, r2, x2, s):
    """Nodal solution: node A between R1+jX1 and the magnetizing branch. Returns (I1, I2) phasors."""
    z1, zm, z2 = r1 + 1j * x1, 1j * xm, r2 / s + 1j * x2
    # (VA - Vph)/z1 + VA/zm + VA/z2 = 0
    va = (vph / z1) / (1 / z1 + 1 / zm + 1 / z2)
    return (vph - va) / z1, va / z2


def torque_full(vph, r1, x1, xm, r2, x2, s, ws):
    _, i2 = solve_induction(vph, r1, x1, xm, r2, x2, s)
    return 3 * abs(i2) ** 2 * (r2 / s) / ws


def thevenin_oc_sc(vph, r1, x1, xm):
    z1, zm = r1 + 1j * x1, 1j * xm
    v_oc = vph * zm / (z1 + zm)
    i_sc = vph / z1
    return v_oc, v_oc / i_sc


def pwm_line_rms(v_dc, m, inject=False, switched=False, n=400000, carrier=99):
    """Build three leg voltages, either switched (0 or V_dc, by comparing the modulating waves with a triangle) or
    averaged over each carrier period (V_dc(1 + ref)/2), and return the rms of the line-to-line fundamental from its
    Fourier coefficient."""
    t = np.linspace(0, 1, n, endpoint=False)
    ref = [m * np.cos(2 * math.pi * t - k * 2 * math.pi / 3) for k in range(3)]
    if inject:
        cm = (np.maximum.reduce(ref) + np.minimum.reduce(ref)) / 2
        ref = [r - cm for r in ref]
    tri = 2 * np.abs(2 * ((t * carrier) % 1) - 1) - 1
    legs = [np.where(r > tri, v_dc, 0.0) if switched else v_dc * (1 + r) / 2 for r in ref]
    vab = legs[0] - legs[1]
    a1 = 2 * np.mean(vab * np.cos(2 * math.pi * t))
    b1 = 2 * np.mean(vab * np.sin(2 * math.pi * t))
    return math.hypot(a1, b1) / math.sqrt(2)


# ---------------------------------------------------------------- Example 22-11.1
w0 = optimize.brentq(lambda w: 24 - 0.05 * w, 0, 1e4)
v.check("Ex 22-11.1a", w0)
v.check("Ex 22-11.1b", w0 / RPM)
i_st = optimize.brentq(lambda i: 24 - 0.5 * i, 0, 1e3)
v.check("Ex 22-11.1c", i_st)
v.check("Ex 22-11.1d", 0.05 * i_st)
i1, w1 = dc_point(24, 0.5, 0.05, 0.5)
v.check("Ex 22-11.1e", i1)
v.check("Ex 22-11.1f", 0.05 * w1)
v.check("Ex 22-11.1g", w1 / RPM)
v.check("Ex 22-11.1h", 100 * 0.5 * w1 / (24 * i1))

# ---------------------------------------------------------------- Example 22-11.2
v.check("Ex 22-11.2a", field_speed(4, 50) / RPM)
v.check("Ex 22-11.2b", field_speed(4, 60) / RPM)
v.check("Ex 22-11.2c", field_speed(2, 60) / RPM)
s2 = (field_speed(4, 50) / RPM - 1460) / (field_speed(4, 50) / RPM)
v.check("Ex 22-11.2d", 100 * s2)
v.check("Ex 22-11.2e", s2 * 50)

# ---------------------------------------------------------------- Example 22-11.3
p_ag = 12500 - 400 - 300
w_s = field_speed(4, 50)
v.check("Ex 22-11.3a", p_ag)
v.check("Ex 22-11.3b", 0.03 * p_ag)
p_mech = p_ag * (1 - 0.03)
v.check("Ex 22-11.3c", p_mech)
v.check("Ex 22-11.3d", p_mech - 150)
v.check("Ex 22-11.3e", 100 * (p_mech - 150) / 12500)
v.check("Ex 22-11.3f", p_mech / ((1 - 0.03) * w_s))           # induced torque = P_mech / w_m
v.check("Ex 22-11.3g", (p_mech - 150) / ((1 - 0.03) * w_s))

# ---------------------------------------------------------------- Example 22-11.4
VPH = 400 / math.sqrt(3)
P4 = dict(r1=0.5, x1=1.0, xm=30.0, r2=0.4, x2=1.0)
v_oc, z_th = thevenin_oc_sc(VPH, 0.5, 1.0, 30.0)
v.check("Ex 22-11.4a", abs(v_oc))
v.check("Ex 22-11.4b", z_th.real)
v.check("Ex 22-11.4c", z_th.imag)
tq = lambda s: torque_full(VPH, 0.5, 1.0, 30.0, 0.4, 1.0, s, w_s)
v.check("Ex 22-11.4d", tq(1.0))
best = optimize.minimize_scalar(lambda s: -tq(s), bounds=(1e-3, 1.0), method="bounded", options={"xatol": 1e-10})
v.check("Ex 22-11.4e", best.x)
v.check("Ex 22-11.4f", -best.fun)
v.check("Ex 22-11.4g", tq(0.03))
v.check("Ex 22-11.4h", abs(solve_induction(VPH, 0.5, 1.0, 30.0, 0.4, 1.0, 1.0)[0]))
v.check("Ex 22-11.4i", abs(solve_induction(VPH, 0.5, 1.0, 30.0, 0.4, 1.0, 0.03)[0]))
mot = mc.Induction(VPH, 50, 4, **P4)
v.assert_true("machines.Induction agrees with the nodal solution",
              abs(mot.torque(0.03) - tq(0.03)) < 1e-9 and abs(mot.t_max() + best.fun) < 1e-6)

# ---------------------------------------------------------------- Example 22-11.5
def sync_phasor_power(vph, ef, xs, delta_deg):
    e = ef * np.exp(-1j * math.radians(delta_deg))
    i = (vph - e) / (1j * xs)
    return 3 * (vph * np.conj(i)).real


v.check("Ex 22-11.5a", VPH)
p5 = sync_phasor_power(VPH, 260, 2, 20)
v.check("Ex 22-11.5b", p5 / 1e3)
v.check("Ex 22-11.5c", p5 / w_s)
pmax = -optimize.minimize_scalar(lambda d: -sync_phasor_power(VPH, 260, 2, d), bounds=(0, 180), method="bounded").fun
v.check("Ex 22-11.5d", pmax / 1e3)

# ---------------------------------------------------------------- Example 22-11.6
v.check("Ex 22-11.6a", optimize.brentq(lambda vv: vv / 30 - 400 / 50, 0, 1000))
v.check("Ex 22-11.6b", field_speed(4, 30) / RPM)
v.check("Ex 22-11.6c", field_speed(4, 30) / RPM - 40)
v.check("Ex 22-11.6d", 0.6 ** 3)

# ---------------------------------------------------------------- Example 22-11.7 (synthesized PWM)
v_spwm = pwm_line_rms(800, 1.0)
v_svm = pwm_line_rms(800, 2 / math.sqrt(3), inject=True)
v.check("Ex 22-11.7a", v_spwm)
v.check("Ex 22-11.7b", v_svm)
v.check("Ex 22-11.7c", v_svm / v_spwm)
v.check("Txt 22-11.a", 100 * (v_svm / v_spwm - 1))
xs = np.linspace(0, 2 * math.pi, 100001)
refs = [np.cos(xs - k * 2 * math.pi / 3) for k in range(3)]
cm = (np.maximum.reduce(refs) + np.minimum.reduce(refs)) / 2
v.assert_true("min–max injection keeps the references within the carrier at m = 2/sqrt(3)",
              float(np.abs((refs[0] - cm) * 2 / math.sqrt(3)).max()) <= 1 + 1e-9)

# ---------------------------------------------------------------- Example 22-11.8
p_base = 400 * 5000 * RPM
v.check("Ex 22-11.8a", p_base / 1e3)
v.check("Ex 22-11.8b", optimize.brentq(lambda tt: tt * 15000 * RPM - p_base, 1, 1000))
n_wheel = 15000 / 9
v.check("Ex 22-11.8c", n_wheel)
v.check("Ex 22-11.8d", n_wheel * RPM * 0.35)
v.check("Ex 22-11.8e", n_wheel * RPM * 0.35 * 3.6)

# ---------------------------------------------------------------- Lab
def dc_start(t_end=0.2):
    v_s, r_a, l_a, k, j, tl = 24, 0.5, 1e-3, 0.05, 1e-4, 0.5
    def f(t, y):
        i, w = y
        return [(v_s - r_a * i - k * w) / l_a, (k * i - tl * min(1.0, max(0.0, w))) / j]
    return integrate.solve_ivp(f, (0, t_end), [0.0, 0.0], method="LSODA", rtol=1e-9, atol=1e-11, max_step=1e-5,
                               dense_output=True)


sol = dc_start()
tt = np.linspace(0, 0.2, 200001)
ii, ww = sol.sol(tt)
v.check("Lab 22-11.a", ii.max())
v.check("Lab 22-11.b", optimize.brentq(lambda t: sol.sol(t)[1] - 0.63 * 380, 1e-3, 0.1) * 1e3)
v.assert_true("DC start settles at 380 rad/s and 10 A", abs(ww[-1] - 380) < 0.1 and abs(ii[-1] - 10) < 0.01)
f20 = 20
t20 = lambda s: torque_full(VPH * f20 / 50, 0.5, 1.0 * f20 / 50, 30 * f20 / 50, 0.4, 1.0 * f20 / 50, s,
                             field_speed(4, f20))
v.check("Lab 22-11.c", -optimize.minimize_scalar(lambda s: -t20(s), bounds=(1e-3, 1), method="bounded").fun)

# ---------------------------------------------------------------- Problems
w01 = optimize.brentq(lambda w: 48 - 0.1 * w, 0, 1e4)
v.check("22-11.1a", w01 / RPM)
v.check("22-11.1b", 48 / 0.2)
v.check("22-11.1c", 0.1 * 48 / 0.2)
_, wp1 = dc_point(48, 0.2, 0.1, 2.0)
v.check("22-11.1d", wp1 / RPM)
v.check("22-11.2", (2 * 2) / (1 * 1))                        # T ∝ Φ I ∝ I²
ns3 = field_speed(6, 60) / RPM
v.check("22-11.3a", ns3)
v.check("22-11.3b", 100 * (ns3 - 1164) / ns3)
v.check("22-11.3c", (ns3 - 1164) / ns3 * 60)
pag4 = 50 - 1.5 - 1.0
v.check("22-11.4a", pag4)
v.check("22-11.4b", 0.025 * pag4)
v.check("22-11.4c", pag4 * 0.975)
v.check("22-11.4d", pag4 * 0.975 - 0.6)
v.check("22-11.4e", 100 * (pag4 * 0.975 - 0.6) / 50)
v.check("22-11.4f", (pag4 * 0.975 - 0.6) * 1e3 / (0.975 * field_speed(4, 60)))
ratio5 = tq(0.03) and torque_full(0.9 * VPH, 0.5, 1.0, 30.0, 0.4, 1.0, 0.03, w_s) / tq(0.03)
v.check("22-11.5a", ratio5)
v.check("22-11.5b", 100 * 0.03 / 0.81)
r2n = abs(complex(z_th.real, z_th.imag + 1.0))
v.check("22-11.6a", r2n)
tq6 = lambda s: torque_full(VPH, 0.5, 1.0, 30.0, r2n, 1.0, s, w_s)
v.check("22-11.6b", tq6(1.0))
v.check("22-11.6c", tq6(0.03))
v.check("22-11.6d", 100 * optimize.brentq(lambda s: tq6(s) - tq(0.03), 1e-4, 0.5))
vp7 = 480 / math.sqrt(3)
v.check("22-11.7a", vp7)
v.check("22-11.7b", optimize.brentq(lambda d: sync_phasor_power(vp7, 300, 1.5, d) - 60e3, 0, 90))
v.check("22-11.7c", sync_phasor_power(vp7, 300, 1.5, 90) / 1e3)
v.check("22-11.8a", 460 * 45 / 60)
v.check("22-11.8b", field_speed(4, 45) / RPM)
v.check("22-11.9a", 0.8)
v.check("22-11.9b", 0.8 ** 2)
v.check("22-11.9c", 0.8 ** 3)
v.check("22-11.9d", 30 * (1 - 0.8 ** 3) * 6000)
v.check("22-11.10a", pwm_line_rms(400, 1.0))
v.check("22-11.10b", pwm_line_rms(400, 2 / math.sqrt(3), inject=True))
f11 = 400 * 9 / 0.35
v.check("22-11.11a", f11)
v.check("22-11.11b", f11 / 2000)
vb = 5000 / 9 * RPM * 0.35
v.check("22-11.11c", vb)
v.check("22-11.11d", vb * 3.6)
v.check("22-11.11e", optimize.brentq(lambda t: integrate.quad(lambda x: f11 / 2000, 0, t)[0] - vb, 0.1, 100))
l91, l93 = 11 / 0.91 - 11, 11 / 0.93 - 11
v.check("22-11.12a", l91)
v.check("22-11.12b", l93)
v.check("22-11.12c", (l91 - l93) * 5000)
th = np.linspace(0, 2 * math.pi, 3601)
amp2 = max(float((math.cos(w) * np.cos(th) + math.sin(w) * np.sin(th)).max()) for w in np.linspace(0, 6.28, 50))
amp3 = max(float(sum(math.cos(w - k * 2 * math.pi / 3) * np.cos(th - k * 2 * math.pi / 3) for k in range(3)).max())
           for w in np.linspace(0, 6.28, 50))
v.check("22-11.13a", amp2)
v.check("22-11.13b", amp3)
v.check("22-11.13c", amp2 / amp3)
v.assert_true("switched PWM synthesis agrees with the averaged legs within 0.1%",
              abs(pwm_line_rms(800, 1.0, switched=True) / v_spwm - 1) < 1e-3
              and abs(pwm_line_rms(800, 2 / math.sqrt(3), inject=True, switched=True) / v_svm - 1) < 1e-3)
v.assert_true("machines.inverter_vll_rms agrees with the synthesized PWM",
              abs(mc.inverter_vll_rms(800) - v_spwm) < 1.0 and abs(mc.inverter_vll_rms(800, svpwm=True) - v_svm) < 1.0)

# ---------------------------------------------------------------- text values derived from sourced data
loss = lambda eta: 11000 / eta - 11000
v.check("Txt 22-11.b", loss(0.876))
v.check("Txt 22-11.c", loss(0.898))
v.check("Txt 22-11.d", loss(0.914))
v.check("Txt 22-11.e", loss(0.933))
v.check("Txt 22-11.f", 100 * (loss(0.914) - loss(0.933)) / loss(0.914))
ns4 = field_speed(4, 50) / RPM
v.check("Txt 22-11.g", 100 * (ns4 - 1477) / ns4)
v.check("Txt 22-11.h", 11000 / (1477 * RPM))
v.check("Txt 22-11.i", 11000 / (math.sqrt(3) * 400 * 0.933 * 0.79))
v.check("Txt 22-11.j", 100 * (ns4 - 1466) / ns4)
n_base = optimize.brentq(lambda n: 280 * n * RPM - 80e3, 100, 20000)
v.check("Txt 22-11.k", n_base)
v.check("Txt 22-11.l", 10390 / n_base)
M_ND, M_FE, M_B = 144.242, 55.845, 10.811
v.check("Txt 22-11.m", 100 * 2 * M_ND / (2 * M_ND + 14 * M_FE + M_B))

v.finish()
