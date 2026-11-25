#!/usr/bin/env python3
"""Verify every number in the Course 22 final-exam solutions.

About half the values are recomputed by a second route, listed below; the rest are closed-form
re-evaluations of the solution's formulas (definitions and one-line arithmetic):
- efficiency optima and crossovers by numerical minimization and root finding; the hold-up time by integrating
  the constant-power discharge C v dv/dt = -P;
- buck and boost ripples, RMS currents and capacitor ripple from waveforms sampled over one switching period;
  discontinuous-conduction duty cycles by root finding on the simulated cycle's average current;
- lossy boost duty cycles by solving the averaged equations, the gain limit by maximizing the gain numerically;
- flyback and forward duty cycles by root finding on volt-second balance; the clamp energy by integrating the
  clamp voltage times the falling leakage current;
- the inductance from the stored field energy; core loss by integrating the iGSE over sampled flux waveforms,
  with k_i from its defining integral and the sinusoid's iGSE loss checked against Steinmetz;
- switching-loss energies by integrating sampled voltage-current overlaps; the device-size optimum by
  minimization; triangular-current-mode currents from the sampled inductor waveform;
- the control loop by evaluating G_vd and the k-factor compensator numerically and locating the crossover;
  the current-mode ratio by iterating the peak-current map; the delay's phase from exp(-s t_d);
- PMIC crossovers by root finding, energies by summation;
- the cell's pulse response and the CC/CV charge by integrating the equivalent circuit in time;
- the busbar by summing 1000 discrete taps, the summed ripple by adding shifted phase currents, and the first
  droop by simulating the L-C network;
- motor quantities from their circuit equations; induction torques by sweeping slip; synchronous phasors;
- per-unit bases and power flow by complex arithmetic; fault currents through symmetrical components; the
  frequency response by integrating the swing equation with first-order governors to steady state;
- the derivations' results by integration (charging loss), numerical linearization of the averaged boost
  (right-half-plane zero) and numerical minimization (flux swing).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, signal

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("22-exam", ROOT / "exam" / "solutions.md")
PI = math.pi
MU0 = 4e-7 * PI
FARADAY = 96485.33212


def trap(y: np.ndarray, x: np.ndarray) -> float:
    return float(np.sum((y[1:] + y[:-1]) * np.diff(x)) / 2)


def rms(y: np.ndarray, x: np.ndarray) -> float:
    return math.sqrt(trap(y * y, x) / (x[-1] - x[0]))


# ---------------------------------------------------------------- Q1 efficiency, loss, hold-up
p_out = 1200.0
v.check("X22.1a", p_out / 0.965)
loss1, loss2 = p_out / 0.965 - p_out, p_out / 0.975 - p_out
v.check("X22.1b", loss1)
v.check("X22.1c", loss2)
v.check("X22.1d", loss1 - loss2)
v.check("X22.1e", 100 * (loss1 - loss2) / loss1)
i_ldo = 15e-3 + 25e-6
v.check("X22.1f", 100 * (1.2 * 15e-3) / (3.6 * i_ldo))
v.check("X22.1g", 1e3 * i_ldo)
i_buck = 1.2 * 15e-3 / (0.9 * 3.6)
v.check("X22.1h", 1e3 * i_buck)
v.check("X22.1i", i_ldo / i_buck)
P0, A_LIN, R_C, V_O = 0.3, 0.02, 0.012, 1.8


def eff(i: float, phases: int = 1) -> float:
    return V_O * i / (V_O * i + phases * P0 + A_LIN * i + R_C * i * i / phases)


best = optimize.minimize_scalar(lambda i: -eff(i), bounds=(0.1, 50), method="bounded", options={"xatol": 1e-9})
v.check("X22.1j", best.x)
v.check("X22.1k", 100 * eff(best.x))
v.check("X22.1l", 100 * eff(20))
v.check("X22.1m", 100 * eff(20, 2))
v.check("X22.1n", optimize.brentq(lambda i: eff(i, 2) - eff(i, 1), 1, 40))
c_hold = 2 * 3000 * 0.02 / (54**2 - 40**2)
# integrate C v dv/dt = -P from 54 V; the voltage must reach 40 V at 20 ms
sol = integrate.solve_ivp(lambda t, y: [-3000 / (c_hold * y[0])], (0, 0.02), [54.0], rtol=1e-11, atol=1e-12)
v.assert_true("hold-up: constant-power discharge reaches 40 V at 20 ms", abs(sol.y[0, -1] - 40) < 1e-6)
v.check("X22.1o", 1e3 * c_hold)
v.check("X22.1p", 100 * (0.5 * c_hold * (54**2 - 40**2)) / (0.5 * c_hold * 54**2))
v.check("X22.1q", 100 * integrate.quad(lambda x: c_hold * x, 0, 40)[0] / integrate.quad(lambda x: c_hold * x, 0, 54)[0])

# ---------------------------------------------------------------- Q2 buck
VIN, VOUT, IOUT, FS, L2, C2 = 5.0, 1.0, 6.0, 2e6, 220e-9, 47e-6
TS = 1 / FS
D2 = VOUT / VIN
t = np.linspace(0, TS, 400001)
ton = D2 * TS
# inductor current by integrating v_L from its valley; the valley is set so the average equals the load
v_l = np.where(t < ton, VIN - VOUT, -VOUT)
i_l = np.concatenate([[0], np.cumsum((v_l[1:] + v_l[:-1]) / 2 * np.diff(t))]) / L2
i_l += IOUT - trap(i_l, t) / TS
di = i_l.max() - i_l.min()
v.check("X22.2a", di)
v.check("X22.2b", di / IOUT)
v.check("X22.2c", i_l.max())
i_c = i_l - IOUT
q_c = np.concatenate([[0], np.cumsum((i_c[1:] + i_c[:-1]) / 2 * np.diff(t))])
v.check("X22.2d", 1e3 * np.ptp(q_c / C2))
v.check("X22.2e", 1e3 * np.ptp(2e-3 * i_c))
v.assert_true("ESR plus capacitive ripple lies between the larger term and the sum",
              max(np.ptp(q_c / C2), np.ptp(2e-3 * i_c)) < np.ptp(q_c / C2 + 2e-3 * i_c) < np.ptp(q_c / C2) + np.ptp(2e-3 * i_c))
v.check("X22.2g", rms(i_l, t))
i_hs = np.where(t < ton, i_l, 0.0)
i_ls = np.where(t < ton, 0.0, i_l)
v.check("X22.2h", rms(i_hs, t))
v.check("X22.2i", rms(i_ls, t))
v.check("X22.2j", rms(i_hs - trap(i_hs, t) / TS, t))
RHS, RLS, RLL = 12e-3, 5e-3, 3e-3
req = D2 * RHS + (1 - D2) * RLS + RLL
v.check("X22.2k", 1e3 * req)
v.check("X22.2l", IOUT**2 * req)
v.check("X22.2m", 100 * VOUT * IOUT / (VOUT * IOUT + IOUT**2 * req))
# duty that holds 1.0 V: average of the switch-node voltage minus the drops
d_real = optimize.brentq(lambda d: d * (VIN - IOUT * RHS) + (1 - d) * (-IOUT * RLS) - IOUT * RLL - VOUT, 0.1, 0.5)
v.check("X22.2n", d_real)
v.check("X22.2o", di / 2)
R_LIGHT = VOUT / 0.4
v.check("X22.2p", 2 * L2 / (R_LIGHT * TS))


def dcm_buck_avg(d1: float) -> tuple[float, float, float]:
    """Average inductor current of a DCM buck cycle at V = VOUT, by sampling one period."""
    ipk = (VIN - VOUT) * d1 * TS / L2
    d2 = ipk * L2 / (VOUT * TS)
    tt = np.linspace(0, TS, 200001)
    il = np.where(tt < d1 * TS, ipk * tt / (d1 * TS),
                  np.clip(ipk - VOUT * (tt - d1 * TS) / L2, 0, None))
    return trap(il, tt) / TS, d2, ipk


d1 = optimize.brentq(lambda d: dcm_buck_avg(d)[0] - 0.4, 0.01, 0.19, xtol=1e-12)
_, d2b, ipk = dcm_buck_avg(d1)
v.check("X22.2q", d1)
v.check("X22.2r", d2b)
v.check("X22.2s", ipk)
v.assert_true("buck at 0.4 A is discontinuous (D1 + D2 < 1)", d1 + d2b < 1)

# ---------------------------------------------------------------- Q3 boost and buck-boost
VI3, VO3, IO3, FS3, L3, C3 = 3.0, 12.0, 0.5, 1e6, 4.7e-6, 22e-6
d3 = optimize.brentq(lambda d: VI3 * d + (VI3 - VO3) * (1 - d), 0.01, 0.99)  # volt-second balance
v.check("X22.3a", d3)
v.check("X22.3b", IO3 / (1 - d3))
v.check("X22.3c", VI3 * d3 / FS3 / L3)
# output ripple: the capacitor alone feeds the load during the on-time
t3 = np.linspace(0, d3 / FS3, 10001)
v.check("X22.3d", 1e3 * trap(np.full_like(t3, IO3), t3) / C3)
RL3, R3 = 0.05, VO3 / IO3


def boost_avg(d: float) -> tuple[float, float]:
    """Averaged lossy boost: solve L-volt-second and C-charge balance for (I_L, V)."""
    # L: V_in - I_L R_L - D' V = 0;  C: D' I_L - V/R = 0 (linear in I_L and V)
    il, vo = np.linalg.solve(np.array([[RL3, 1 - d], [1 - d, -1 / R3]]), np.array([VI3, 0.0]))
    return il, vo


il_a, vo_a = boost_avg(d3)
v.check("X22.3e", 100 * vo_a**2 / R3 / (VI3 * il_a))
v.check("X22.3f", vo_a)
d12 = optimize.brentq(lambda d: boost_avg(d)[1] - 12.0, 0.7, 0.9)
il_b, vo_b = boost_avg(d12)
v.check("X22.3g", d12)
v.check("X22.3h", 100 * vo_b**2 / R3 / (VI3 * il_b))
mx = optimize.minimize_scalar(lambda d: -boost_avg(d)[1], bounds=(0.9, 0.99), method="bounded",
                              options={"xatol": 1e-10})
v.check("X22.3i", -mx.fun / VI3)
v.check("X22.3j", mx.x)
dbb = optimize.brentq(lambda d: 5 * d - 12 * (1 - d), 0.01, 0.99)  # V_in D = |V| D'
v.check("X22.3k", dbb)
v.check("X22.3l", 0.3 / (1 - dbb))
# switch voltage over one sampled period: 0 while on; while off the inductor is clamped to the output,
# so the switch node sits at V_in - v_L with v_L set by volt-second balance
tbb = np.linspace(0, 1.0, 100001)
v_l_off = -5 * dbb / (1 - dbb)
v_sw = np.where(tbb < dbb, 0.0, 5 - v_l_off)
v.assert_true("buck-boost inductor volt-second balance", abs(trap(np.where(tbb < dbb, 5.0, v_l_off), tbb)) < 1e-4)
v.check("X22.3m", v_sw.max())
i_in = np.where(tbb < dbb, 0.3 / (1 - dbb), 0.0)
v.check("X22.3n", trap(i_in, tbb))
v.assert_true("buck-boost input power equals output power", abs(5 * trap(i_in, tbb) - 12 * 0.3) < 1e-3)
R_L20 = VO3 / 0.02
k3 = 2 * L3 / (R_L20 / FS3)
v.check("X22.3o", k3)
v.check("X22.3p", d3 * (1 - d3) ** 2)
v.assert_true("boost at 20 mA is discontinuous (K < K_crit)", k3 < d3 * (1 - d3) ** 2)


def dcm_boost_iout(d: float) -> float:
    """Diode (output) current averaged over a DCM boost cycle at 12 V output."""
    ipk = VI3 * d / FS3 / L3
    t_off = ipk * L3 / (VO3 - VI3)
    return 0.5 * ipk * t_off * FS3


v.check("X22.3q", optimize.brentq(lambda d: dcm_boost_iout(d) - 0.02, 0.05, 0.7))

# ---------------------------------------------------------------- Q4 isolated converters
for key, vin in (("X22.4a", 36), ("X22.4b", 48), ("X22.4c", 72)):
    v.check(key, optimize.brentq(lambda d: vin * d - 3 * 12 * (1 - d), 0.01, 0.99))
v.check("X22.4d", 72 + 3 * 12)
LLK, IPK4, VC, VR, FS4 = 1.2e-6, 2.5, 60.0, 36.0, 150e3
tc = LLK * IPK4 / (VC - VR)
v.check("X22.4e", 1e9 * tc)
tt = np.linspace(0, tc, 100001)
e_clamp = trap(VC * (IPK4 - (VC - VR) / LLK * tt), tt)  # clamp voltage times falling leakage current
v.check("X22.4f", 1e6 * e_clamp)
v.check("X22.4g", e_clamp * FS4)
v.check("X22.4h", 72 + VC)
v.check("X22.4i", 1e6 * 0.5 * LLK * IPK4**2)
v.check("X22.4j", e_clamp / (0.5 * LLK * IPK4**2))
N3_N1 = 0.8
n_fw = 0.495 * 36 / 3.3
v.check("X22.4k", n_fw)
v.check("X22.4l", optimize.brentq(lambda d: d * 72 / n_fw - 3.3, 0.01, 0.99))
# reset: the magnetizing volt-seconds V_in D must be returned in D_r = D N3/N1, and D + D_r <= 1
d_max = optimize.brentq(lambda d: d + d * N3_N1 - 1, 0.01, 0.99)
v.check("X22.4m", d_max)
v.check("X22.4n", 72 * (1 + 1 / N3_N1))
TS4, N1, AE4 = 1 / 300e3, 15, 50e-6
db_normal = [vin * (n_fw * 3.3 / vin) * TS4 / (N1 * AE4) for vin in (36, 48, 60, 72)]
v.assert_true("forward flux swing is independent of input voltage", np.ptp(db_normal) < 1e-12)
v.check("X22.4o", db_normal[0])
db_worst = 72 * d_max * TS4 / (N1 * AE4)
v.check("X22.4p", db_worst)
v.check("X22.4r", db_worst / db_normal[0])
v.check("X22.4q", 36 * 0.495 * TS4 / 250e-6)

# ---------------------------------------------------------------- Q5 magnetics
AE, LE, MUR, NT, GAP = 80e-6, 60e-3, 2500, 30, 0.8e-3
rc, rg = LE / (MUR * MU0 * AE), GAP / (MU0 * AE)
v.check("X22.5a", rc / 1e5)
v.check("X22.5b", rg / 1e6)
L5 = NT**2 / (rc + rg)
# independent: L from the stored field energy at 1 A, W = (1/2) L I^2
phi = NT * 1.0 / (rc + rg)
b1 = phi / AE
w_field = b1**2 / (2 * MU0) * AE * GAP + b1**2 / (2 * MUR * MU0) * AE * LE
v.check("X22.5c", 1e6 * 2 * w_field)
v.assert_true("inductance from reluctance equals inductance from field energy", abs(2 * w_field - L5) < 1e-15)
v.check("X22.5d", L5 / (MU0 * NT**2 * AE / LE))
isat = 0.32 * NT * AE / L5
v.check("X22.5e", isat)
bsat = 0.32
w_gap = bsat**2 / (2 * MU0) * AE * GAP
w_core = bsat**2 / (2 * MUR * MU0) * AE * LE
v.check("X22.5f", 1e3 * (w_gap + w_core))
v.check("X22.5g", 100 * w_gap / (w_gap + w_core))
K_ST, AL, BE, F5, BPK = 3.0, 1.4, 2.5, 1e5, 0.1
ki = K_ST / ((2 * PI) ** (AL - 1) * integrate.quad(lambda th: abs(math.cos(th)) ** AL * 2 ** (BE - AL), 0, 2 * PI,
                                                    limit=200)[0])
v.assert_true("k_i given in the exam (0.1873) matches its defining integral", round(ki, 4) == 0.1873)


def igse(b: np.ndarray, tt: np.ndarray) -> float:
    """iGSE loss density of a sampled periodic flux waveform."""
    dbdt = np.gradient(b, tt)
    dpp = b.max() - b.min()
    return trap(ki * np.abs(dbdt) ** AL * dpp ** (BE - AL), tt) / (tt[-1] - tt[0])


T5 = 1 / F5
ts = np.linspace(0, T5, 400001)
p_sin = igse(BPK * np.sin(2 * PI * F5 * ts), ts)
v.assert_true("iGSE reproduces Steinmetz for a sinusoid", abs(p_sin / (K_ST * F5**AL * BPK**BE) - 1) < 1e-4)
v.check("X22.5h", p_sin / 1e3)
v.check("X22.5i", p_sin * AE * LE)


def tri(dd: float) -> np.ndarray:
    up = ts < dd * T5
    return np.where(up, -BPK + 2 * BPK * ts / (dd * T5), BPK - 2 * BPK * (ts - dd * T5) / ((1 - dd) * T5))


p_t5, p_t1 = igse(tri(0.5), ts), igse(tri(0.1), ts)
v.check("X22.5j", p_t5 / 1e3)
v.check("X22.5k", p_t5 / p_sin)
v.check("X22.5l", p_t1 / 1e3)
v.check("X22.5m", p_t1 / p_sin)
RHO100 = 22.66e-9
delta = math.sqrt(RHO100 / (PI * 2e5 * MU0))
v.check("X22.5n", 1e3 * delta)
dl = 0.12e-3 / delta
v.check("X22.5o", dl)
v.check("X22.5p", 1 + (5 * 9 - 1) / 45 * dl**4)
fr = dl * ((math.sinh(2 * dl) + math.sin(2 * dl)) / (math.cosh(2 * dl) - math.cos(2 * dl))
           + 2 * (9 - 1) / 3 * (math.sinh(dl) - math.sin(dl)) / (math.cosh(dl) + math.cos(dl)))
v.check("X22.5q", fr)

# ---------------------------------------------------------------- Q6 switching loss
V6, I6, F6 = 380.0, 12.0, 80e3


def overlap_energy(t_x: float) -> float:
    """A linear current ramp then a linear voltage ramp (or the reverse), each half of t_x."""
    tt = np.linspace(0, t_x / 2, 20001)
    return 2 * trap(V6 * I6 * tt / (t_x / 2), tt)


v.check("X22.6a", (overlap_energy(24e-9) + overlap_energy(16e-9)) * F6)
v.check("X22.6b", 8**2 * 0.04)
v.check("X22.6c", 1e6 * 70e-9 * V6)
v.check("X22.6d", 70e-9 * V6 * F6)
v.check("X22.6e", 9e-6 * F6)
v.check("X22.6f", 1e6 * 90e-9 * V6)
v.check("X22.6g", 90e-9 * V6 * F6)
v.check("X22.6h", 0.0)
RQ = 0.04 * 70e-9


def p_size(r: float, f: float = F6) -> float:
    return 8**2 * r + RQ * V6 * f / r


opt6 = optimize.minimize_scalar(p_size, bounds=(1e-3, 0.5), method="bounded", options={"xatol": 1e-12})
v.check("X22.6i", 1e3 * opt6.x)
v.check("X22.6j", opt6.fun)
v.check("X22.6k", optimize.minimize_scalar(lambda r: p_size(r, 2 * F6), bounds=(1e-3, 0.5), method="bounded",
                                           options={"xatol": 1e-12}).fun)
v.check("X22.6l", p_size(0.020))
i_neg = 2 * 8e-9 / 8e-9
v.check("X22.6m", i_neg)
d6, f6b = 12 / 48, 400e3
l6 = optimize.brentq(lambda l: 5 - (12 * (1 - d6) / (f6b * l)) / 2 + i_neg, 0.1e-6, 10e-6)  # valley = -2 A
t6 = np.linspace(0, 1 / f6b, 400001)
vl6 = np.where(t6 < d6 / f6b, 48 - 12, -12.0)
il6 = np.concatenate([[0], np.cumsum((vl6[1:] + vl6[:-1]) / 2 * np.diff(t6))]) / l6
il6 += 5 - trap(il6, t6) * f6b
v.check("X22.6n", np.ptp(il6))
v.check("X22.6o", 1e6 * l6)
v.check("X22.6p", il6.max())
v.assert_true("TCM valley reaches -2 A", abs(il6.min() + 2) < 1e-3)
v.check("X22.6q", rms(il6, t6))
v.check("X22.6r", (rms(il6, t6) / 5) ** 2)

# ---------------------------------------------------------------- Q7 control
VG7, VO7, L7, C7, R7, VM = 12.0, 1.2, 0.5e-6, 470e-6, 0.12, 1.0
gvd = signal.TransferFunction([VG7], [L7 * C7, L7 / R7, 1])
w0 = 1 / math.sqrt(L7 * C7)
v.check("X22.7a", w0 / 2 / PI / 1e3)
v.check("X22.7b", R7 * math.sqrt(C7 / L7))
v.check("X22.7c", 20 * math.log10(abs(np.polyval(gvd.num, 0) / np.polyval(gvd.den, 0))))
FC = 40e3
wc = 2 * PI * FC
g_c = np.polyval(gvd.num, 1j * wc) / np.polyval(gvd.den, 1j * wc)
v.check("X22.7d", abs(g_c))
phase_p = math.degrees(np.angle(g_c))
v.check("X22.7e", phase_p)
boost = 55 - 90 - phase_p
v.check("X22.7f", boost)
kf = math.tan(math.radians((boost / 2 + 90) / 2))
v.check("X22.7g", kf)
v.check("X22.7h", FC / kf / 1e3)
v.check("X22.7i", FC * kf / 1e3)
gc_mag = VM / abs(g_c)
v.check("X22.7j", gc_mag)
w_i = gc_mag * wc / kf**2
v.check("X22.7k", w_i / 2 / PI / 1e3)


def loop(w: float) -> complex:
    s = 1j * w
    gc = (w_i / s) * (1 + s / (wc / kf)) ** 2 / (1 + s / (wc * kf)) ** 2
    return gc / VM * VG7 / (L7 * C7 * s * s + L7 / R7 * s + 1)


w_x = optimize.brentq(lambda w: abs(loop(w)) - 1, 2 * PI * 15e3, 2 * PI * 200e3)
v.check("X22.7l", w_x / 2 / PI / 1e3)
v.check("X22.7m", 180 + math.degrees(np.angle(loop(w_x))))
ws = np.logspace(2, 6.3, 20000) * 2 * PI
v.assert_true("loop gain crosses unity once", np.sum(np.diff(np.sign(np.abs([loop(w) for w in ws]) - 1)) != 0) == 1)
m1, m2 = (12 - 7.5) / 3.3, 7.5 / 3.3  # A/us


def cm_ratio(ma: float) -> float:
    """Iterate the peak-current map: a small initial valley error, propagated through 40 cycles."""
    tsw = 1.0  # time in us
    i_peak_ref = 10.0  # control level; the map is linear, so the operating point does not matter

    def one_cycle(i_valley: float) -> float:
        # on until i_L reaches i_peak_ref - m_a t; then fall at m2 for the rest of the period
        t_on = (i_peak_ref - i_valley) / (m1 + ma)
        return i_valley + m1 * t_on - m2 * (tsw - t_on)

    # find the steady valley by fixed point, then perturb
    iv_ss = optimize.brentq(lambda x: one_cycle(x) - x, -100, 100)
    eps = 1e-6
    return (one_cycle(iv_ss + eps) - iv_ss) / eps


v.check("X22.7n", m1)
v.check("X22.7o", m2)
v.check("X22.7p", cm_ratio(0.0))
v.check("X22.7q", optimize.brentq(lambda ma: abs(cm_ratio(ma)) - 1, 0.01, 1.4))
a_comp = cm_ratio(m2 / 2)
v.check("X22.7r", a_comp)
v.check("X22.7s", abs(a_comp) ** 5)
v.check("X22.7t", 1e3 * 5 / (2 * PI * FC * C7))
delay_phase = -math.degrees(np.angle(np.exp(-1j * wc * 1e-6)))
v.check("X22.7u", delay_phase)
v.check("X22.7v", 180 + math.degrees(np.angle(loop(w_x) * np.exp(-1j * w_x * 1e-6))))
v.check("X22.7w", optimize.brentq(lambda f: 360 * f * 1e-6 - 10, 1e3, 1e5) / 1e3)

# ---------------------------------------------------------------- Q8 PMIC
eta_c = 0.9 * 0.8 / 1.0
v.check("X22.8a", 100 * eta_c)
ib_c, ib_d = 0.08 / (eta_c * 3.8), 0.08 / (0.87 * 3.8)
v.check("X22.8b", 1e3 * ib_c)
v.check("X22.8c", 1e3 * ib_d)
v.check("X22.8d", 1e3 * (ib_c - ib_d))


def p_pwm(i: float) -> float:
    return 12e-3 + 0.15 * i * i


def p_pfm(i: float) -> float:
    return 3.8 * 0.5e-6 + 0.06 * i + 0.5 * i * i


v.check("X22.8e", 1e3 * optimize.brentq(lambda i: p_pwm(i) - p_pfm(i), 1e-4, 1))
for key, i, fn in (("X22.8f", 0.5e-3, p_pwm), ("X22.8g", 0.5e-3, p_pfm), ("X22.8h", 0.2, p_pwm),
                   ("X22.8i", 0.2, p_pfm)):
    v.check(key, 100 * 1.0 * i / (1.0 * i + fn(i)))
# integrate the battery power over a sampled 24 h profile (1 s steps), term by term
tday = np.arange(0, 86400, 1.0)
mode = np.where(tday < 23.5 * 3600, 0, np.where(tday < 23.5 * 3600 + 25 * 60, 1, 2))
p_load = np.array([20e-6 / 0.8, 6e-3 / 0.9, 45e-3 / 0.88])[mode]
terms = [float(np.sum(np.where(mode == k, p_load, 0.0))) for k in range(3)] + [float(np.sum(np.full_like(tday, 3.8 * 1.5e-6)))]
v.assert_true("usage profile covers 24 h", abs(23.5 * 60 + 25 + 5 - 24 * 60) < 1e-9)
for key, e in zip(("X22.8j", "X22.8k", "X22.8l", "X22.8m"), terms):
    v.check(key, e)
e_day = sum(terms)
v.check("X22.8n", e_day)
v.check("X22.8o", 1e3 * e_day / 86400)
v.check("X22.8p", 0.150 * 3.8 * 3600 / e_day)
v.check("X22.8q", 47e-6 * (0.95 - 0.65) / 15e-6)
v.check("X22.8r", 100 * (1 - (0.88 / 0.95) ** 2))
v.check("X22.8s", 1e6 * (5e-9 * 0.88**2 + 0.3e-6) / 2e-3)

# ---------------------------------------------------------------- Q9 battery
v.check("X22.9a", FARADAY / (3.6 * 6 * 12.011))
v.check("X22.9b", 4.2 * 3.6)
v.check("X22.9c", 6 / 4.2)
VOC9, R0, R1, TAU1, I9 = 3.8, 0.040, 0.025, 50.0, 3.0
c1 = TAU1 / R1
pulse = integrate.solve_ivp(lambda t, y: [I9 / c1 - y[0] / TAU1], (0, 200), [0.0], t_eval=[0, 50, 200],
                            rtol=1e-11, atol=1e-13)
for key, v1 in zip(("X22.9d", "X22.9e", "X22.9f"), pulse.y[0]):
    v.check(key, VOC9 - I9 * R0 - v1)
v.check("X22.9g", optimize.brentq(lambda i: VOC9 - i * R0 - 3.0, 0, 100))
v.check("X22.9h", optimize.brentq(lambda i: VOC9 - i * (R0 + R1) - 3.0, 0, 100))
Q9, RC9, ICC, ITERM = 4.2 * 3600, 0.06, 0.7 * 4.2, 4.2 / 20
ceff = Q9 / 0.5
v.check("X22.9i", ceff)
v.check("X22.9j", RC9 * ceff / 60)


def ocv(z: float) -> float:
    return 3.7 + 0.5 * z


# simulate CC then CV with the linear OCV: CC until terminal reaches 4.2 V, then hold 4.2 V until C/20
def cc_phase(t, y):
    return [ICC / Q9]


def hit_vmax(t, y):
    return ocv(y[0]) + ICC * RC9 - 4.2


hit_vmax.terminal = True
cc = integrate.solve_ivp(cc_phase, (0, 1e5), [0.2], events=hit_vmax, rtol=1e-12, atol=1e-14)
t_cc, z_cv = cc.t_events[0][0], cc.y_events[0][0][0]


def cv_phase(t, y):
    return [(4.2 - ocv(y[0])) / RC9 / Q9]


def at_term(t, y):
    return (4.2 - ocv(y[0])) / RC9 - ITERM


at_term.terminal = True
cv = integrate.solve_ivp(cv_phase, (0, 1e5), [z_cv], events=at_term, rtol=1e-12, atol=1e-14)
t_cv, z_end = cv.t_events[0][0], cv.y_events[0][0][0]
v.check("X22.9k", z_cv)
v.check("X22.9l", t_cc / 60)
v.check("X22.9m", t_cv / 60)
v.check("X22.9n", (t_cc + t_cv) / 60)
v.check("X22.9o", z_end)
v.check("X22.9p", (z_end - z_cv) * Q9 / 3600)
v.check("X22.9q", 1e3 * 50e-6 * 30 * 24)
qmax = 2.1 / (0.85 - 0.30)
v.check("X22.9r", qmax)
v.check("X22.9s", 100 * qmax / 4.2)

# ---------------------------------------------------------------- Q10 datacenter
P10, RW = 132e3, 40e-6
i54, i800 = P10 / 54, P10 / 800
v.check("X22.10a", i54)
v.check("X22.10b", i800)
v.check("X22.10c", i54**2 * 2 * RW)


def tapped_loss(i_total: float, n: int = 1000) -> float:
    """n equal loads tapped at the ends of n equal segments of a 2*RW loop."""
    seg = 2 * RW / n
    currents = i_total * (1 - np.arange(n) / n)  # current in segment k carries the loads beyond it
    return float(np.sum(currents**2 * seg))


v.assert_true("discrete taps converge to one third of the lumped loss",
              abs(tapped_loss(i54, 4000) / (i54**2 * 2 * RW) - 1 / 3) < 2e-4)
v.check("X22.10d", i54**2 * 2 * RW / 3)
v.check("X22.10e", i800**2 * 2 * RW / 3)
v.check("X22.10v", (i54 / i800) ** 2)
v.check("X22.10f", (800 / 2) / (math.sqrt(3) * 480 * 0.95 / 3))
VIN10, VO10, IO10, NPH, F10, L10 = 12.0, 0.75, 600.0, 12, 800e3, 100e-9
d10 = VO10 / VIN10
v.check("X22.10g", d10)
v.check("X22.10h", IO10 / NPH)
t10 = np.linspace(0, 1 / F10, 240001)[:-1]
vl10 = np.where(t10 < d10 / F10, VIN10 - VO10, -VO10)
one = np.concatenate([[0], np.cumsum(vl10[:-1] * np.diff(t10))]) / L10
v.check("X22.10i", np.ptp(one))
shift = len(t10) // NPH
total = sum(np.roll(one, k * shift) for k in range(NPH))
v.check("X22.10j", np.ptp(total))
v.check("X22.10k", np.ptp(total) / np.ptp(one))
spec = np.abs(np.fft.rfft(total - total.mean()))
v.check("X22.10l", np.argmax(spec) * F10 / 1e6)
zt = 0.03 / 400
v.check("X22.10m", 1e6 * zt)
v.check("X22.10n", 0.80 - zt * 600)
v.check("X22.10o", 1e3 * 400 / (2 * PI * 300e3 * 0.03))
LP, CD = 0.8e-12, 80e-6


def first_droop(lp: float, cd: float, di: float, esr: float = 0.0) -> float:
    """Simulate the die node: inductor from a stiff source into C (with ESR), load steps by di at t = 0."""
    f0 = 1 / (2 * PI * math.sqrt(lp * cd))
    tend = 1.5 / f0

    def rhs(_t, y):
        il, vc = y
        return [-(vc + esr * (il - di)) / lp, (il - di) / cd]

    s = integrate.solve_ivp(rhs, (0, tend), [0.0, 0.0], max_step=tend / 3000, rtol=1e-10, atol=1e-16)
    return float(-np.min(s.y[1] + esr * (s.y[0] - di)))


v.check("X22.10p", 1 / (2 * PI * math.sqrt(LP * CD)) / 1e6)
v.check("X22.10q", 1e6 * math.sqrt(LP / CD))
v.check("X22.10r", 1e3 * first_droop(LP, CD, 300))
v.check("X22.10s", 1e3 * first_droop(LP, CD, 400))
c_need = optimize.brentq(lambda c: first_droop(LP, c, 400) - 0.03, 100e-6, 200e-6, xtol=1e-12)
v.check("X22.10t", 1e6 * c_need)
z0_sim = first_droop(LP, CD, 1.0)  # an undamped 1 A step droops by Z0
v.check("X22.10u", 1e6 * z0_sim / 2)
esr_opt = optimize.minimize_scalar(lambda e: first_droop(LP, CD, 400, e), bounds=(10e-6, 100e-6), method="bounded",
                                   options={"xatol": 1e-9}).x
v.check("X22.10x", esr_opt / math.sqrt(LP / CD))
v.check("X22.10y", 1e6 * esr_opt)
v.assert_true("the droop optimum is flat: Z0/2 is within 0.2% of the best droop",
              first_droop(LP, CD, 400, z0_sim / 2) / first_droop(LP, CD, 400, esr_opt) - 1 < 2e-3)

# ---------------------------------------------------------------- Q11 machines
KM, RA, VDC = 0.12, 0.25, 48.0
v.check("X22.11a", optimize.brentq(lambda w: VDC - KM * w, 0, 1e4))
v.check("X22.11b", VDC / KM * 60 / (2 * PI))
v.check("X22.11c", KM * VDC / RA)
i11 = 3.0 / KM
w11 = (VDC - i11 * RA) / KM
v.check("X22.11d", i11)
v.check("X22.11e", w11)
v.check("X22.11f", 100 * 3.0 * w11 / (VDC * i11))
ns11 = 120 * 50 / 8
s11 = (ns11 - 727.5) / ns11
v.check("X22.11g", s11)
v.check("X22.11h", s11 * 50)
v.check("X22.11i", s11 * 20e3)
v.check("X22.11j", (1 - s11) * 20e3 / 1e3)
v.check("X22.11k", (1 - s11) * 20e3 / (2 * PI * (1 - s11) * ns11 / 60))  # P_mech / omega_m
VTH, RTH, XTH, X2, R2 = 250.0, 0.3, 0.9, 0.9, 0.35
WS = 2 * PI * 1800 / 60


def torque(s: float) -> float:
    """Torque from the rotor current of the Thevenin circuit: P_ag = 3 I2^2 R2/s."""
    i2 = VTH / abs(complex(RTH + R2 / s, XTH + X2))
    return 3 * i2**2 * (R2 / s) / WS


res = optimize.minimize_scalar(lambda s: -torque(s), bounds=(0.01, 1), method="bounded", options={"xatol": 1e-12})
v.check("X22.11l", res.x)
v.check("X22.11m", 1800 * (1 - res.x))
v.check("X22.11n", -res.fun)
v.check("X22.11o", torque(1.0))
v.check("X22.11p", torque(0.03))
VPH = 4160 / math.sqrt(3)
EF, XS, P11 = 2800.0, 8.0, 1.5e6


def p_sync(dlt: float) -> tuple[float, complex]:
    ia = (VPH - EF * np.exp(-1j * dlt)) / (1j * XS)
    return 3 * (VPH * np.conj(ia)).real, ia


dlt = optimize.brentq(lambda d: p_sync(d)[0] - P11, 0, PI / 2)
_, ia11 = p_sync(dlt)
v.check("X22.11q", math.degrees(dlt))
v.check("X22.11r", optimize.minimize_scalar(lambda d: -p_sync(d)[0], bounds=(0, PI), method="bounded",
                                            options={"xatol": 1e-12}).fun * -1 / 1e6)
v.check("X22.11s", abs(ia11))
v.check("X22.11t", math.cos(np.angle(ia11)))
v.assert_true("motor current lags (under-excited at this load)", np.angle(ia11) < 0)
v.check("X22.11u", 3 * (VPH * np.conj(ia11)).imag / 1e6)


def q_at_ef(ef: float) -> float:
    d = math.asin(P11 * XS / (3 * VPH * ef))
    ia = (VPH - ef * np.exp(-1j * d)) / (1j * XS)
    return 3 * (VPH * np.conj(ia)).imag


v.check("X22.11v", optimize.brentq(q_at_ef, 2500, 3500))

# ---------------------------------------------------------------- Q12 power systems
SB, VB = 100e6, 345e3
ib12 = SB / (math.sqrt(3) * VB)
zb12 = VB**2 / SB
v.check("X22.12a", ib12)
v.check("X22.12b", zb12)
xt = 0.09 * (345e3**2 / 75e6) / zb12  # ohms on its own 75 MVA base, re-expressed on the 100 MVA base
v.check("X22.12c", xt)
xl = 0.38 * 150 / zb12
v.check("X22.12d", xl)
x12 = xt + xl
v.check("X22.12e", x12)
V1M, V2M, P12 = 1.02, 1.00, 2.0


def flow(d: float) -> tuple[complex, complex]:
    v1, v2 = V1M * np.exp(1j * d), V2M
    i = (v1 - v2) / (1j * x12)
    return v1 * np.conj(i), v2 * np.conj(i)


d12a = optimize.brentq(lambda d: flow(d)[0].real - P12, 0, PI / 2)
s1, s2 = flow(d12a)
v.check("X22.12f", math.degrees(d12a))
v.check("X22.12g", s1.imag)
v.check("X22.12h", s2.imag)
v.check("X22.12i", s1.imag - s2.imag)
v.assert_true("line reactive consumption equals I^2 X",
              abs((s1.imag - s2.imag) - abs((V1M * np.exp(1j * d12a) - V2M) / (1j * x12)) ** 2 * x12) < 1e-12)
v.check("X22.12j", -optimize.minimize_scalar(lambda d: -flow(d)[0].real, bounds=(0, PI), method="bounded",
                                             options={"xatol": 1e-12}).fun)
Z1 = Z2 = 0.20j
Z0 = 0.10j
v.check("X22.12k", abs(1 / Z1))
v.check("X22.12l", abs(1 / Z1) * ib12 / 1e3)
v.check("X22.12m", 100 / abs(Z1))
# SLG through symmetrical components: I0 = I1 = I2 = V/(Z1+Z2+Z0); phase currents by the A matrix
ia0 = 1 / (Z1 + Z2 + Z0)
a = np.exp(2j * PI / 3)
A = np.array([[1, 1, 1], [1, a * a, a], [1, a, a * a]])
iabc = A @ np.array([ia0, ia0, ia0])
v.assert_true("SLG: healthy phases carry no fault current", abs(iabc[1]) < 1e-12 and abs(iabc[2]) < 1e-12)
v.check("X22.12n", abs(iabc[0]))
v.check("X22.12o", abs(iabc[0]) * ib12 / 1e3)
H12, S12, F0, DP12 = 4.5, 80e3, 60.0, 1200.0
v.check("X22.12p", H12 * S12 / 1e3)
GOV, DAMP, TGOV = 30e3 / (0.05 * F0), 1500.0, 5.0


def grid(_t, y):
    df, pg = y  # frequency deviation (Hz) and governor output (MW)
    dfdt = (pg - DP12 - DAMP * df) * F0 / (2 * H12 * S12)
    return [dfdt, (-GOV * df - pg) / TGOV]


v.check("X22.12q", grid(0, [0.0, 0.0])[0])  # initial RoCoF from the swing equation itself
g = integrate.solve_ivp(grid, (0, 600), [0.0, 0.0], max_step=0.05, rtol=1e-10, atol=1e-12)
v.assert_true("RoCoF at t = 0 matches the swing equation",
              abs(grid(0, [0, 0])[0] + DP12 * F0 / (2 * H12 * S12)) < 1e-12)
v.check("X22.12r", g.y[0, -1])
v.check("X22.12s", g.y[1, -1])

# ---------------------------------------------------------------- Q13 derivations
C13, V13, R13 = 40e-9, 0.9, 1e3
tt13 = np.linspace(0, 40 * R13 * C13, 400001)
e_r = trap((V13 / R13 * np.exp(-tt13 / (R13 * C13))) ** 2 * R13, tt13)
tt50 = tt13 * 50 / R13
e_r2 = trap((V13 / 50 * np.exp(-tt50 / (50 * C13))) ** 2 * 50, tt50)
v.assert_true("charging loss independent of R", abs(e_r / e_r2 - 1) < 1e-6)
v.check("X22.13a", 1e9 * e_r)
v.check("X22.13b", 1e9 * C13 * V13**2)
v.check("X22.13c", 1e6 * e_r * 1e4)
e_steps = sum(trap(((V13 / 4) / R13 * np.exp(-tt13 / (R13 * C13))) ** 2 * R13, tt13) for _ in range(4))
v.check("X22.13d", 1e6 * e_steps * 1e4)
v.check("X22.13w", 1e9 * e_steps)
VI13, VO13, IO13, L13, C13b = 5.0, 12.0, 2.0, 3.3e-6, 47e-6
R13b = VO13 / IO13
d13 = 1 - VI13 / VO13
v.check("X22.13e", d13)


def avg_boost(x, dd):
    il, vo = x
    return np.array([(VI13 - (1 - dd) * vo) / L13, ((1 - dd) * il - vo / R13b) / C13b])


# operating point and numerical Jacobians
x0 = np.array([IO13 / (1 - d13), VO13])
h = 1e-7
Amat = np.column_stack([(avg_boost(x0 + h * e, d13) - avg_boost(x0 - h * e, d13)) / (2 * h) for e in np.eye(2)])
Bvec = (avg_boost(x0, d13 + h) - avg_boost(x0, d13 - h)) / (2 * h)
Cvec = np.array([0.0, 1.0])


def g_vd(s: complex) -> complex:
    return complex(Cvec @ np.linalg.solve(s * np.eye(2) - Amat, Bvec))


den = np.poly(Amat)  # det(sI - A)
numer0 = g_vd(0) * np.polyval(den, 0)
numer1 = g_vd(1.0) * np.polyval(den, 1.0)  # the numerator is first order: n1 s + n0
v.check("X22.13f", g_vd(0).real)
v.check("X22.13g", 20 * math.log10(g_vd(0).real))
poles = np.roots(den)
v.check("X22.13h", abs(poles[0]) / 2 / PI / 1e3)
v.check("X22.13i", abs(poles[0]) / (-2 * poles[0].real))
zero = -numer0 / (numer1 - numer0)
v.assert_true("boost zero lies in the right half plane", zero.real > 0 and abs(zero.imag) < 1e-6)
v.check("X22.13j", zero.real / 2 / PI / 1e3)
BE13 = 2.6
a13 = 3.0 / 0.2**BE13
b13 = 1.0 * 0.2**2
v.check("X22.13k", a13)
v.check("X22.13l", b13)
opt13 = optimize.minimize_scalar(lambda x: a13 * x**BE13 + b13 / x**2, bounds=(0.01, 1), method="bounded",
                                 options={"xatol": 1e-12})
v.check("X22.13m", opt13.x)
v.check("X22.13n", a13 * opt13.x**BE13)
v.check("X22.13o", b13 / opt13.x**2)
v.check("X22.13p", opt13.fun)
v.check("X22.13q", (a13 * opt13.x**BE13) / (b13 / opt13.x**2))
RR, XX, PP, QQ, VR13 = 0.02, 0.10, 0.8, 0.3, 1.0
vs = VR13 + complex(RR, XX) * np.conj(complex(PP, QQ) / VR13)
v.check("X22.13r", vs.real - VR13)
v.check("X22.13s", vs.imag)
v.check("X22.13t", vs.real)
v.check("X22.13u", abs(vs))
v.check("X22.13v", vs.real + vs.imag**2 / (2 * vs.real))

# ---------------------------------------------------------------- Q14 diligence
P14 = 0.75 * 2000
pin14 = P14 / 0.93
v.check("X22.14a", pin14)
v.check("X22.14b", pin14 - P14)
v.check("X22.14c", pin14 / 48)
v.check("X22.14d", 100 * 0.93 / 0.975)
chain = 0.975 * 0.870
v.check("X22.14e", 100 * chain)
v.check("X22.14f", P14 / chain)
v.check("X22.14g", P14 / chain - pin14)
RSQ = 17.24e-9 / 70e-6
v.check("X22.14h", 1e3 * RSQ)


def plane_loop(n_planes: int) -> float:
    """Resistance of supply plus return: each polarity n planes in parallel, 25 mm long and 50 mm wide."""
    one_way = (RSQ * 25e-3 / 50e-3) / n_planes
    return 2 * one_way


v.check("X22.14i", 1e6 * plane_loop(6))
v.check("X22.14j", 1e3 * 2000 * plane_loop(6))
v.check("X22.14k", 2000**2 * plane_loop(6))
n_ok = next(n for n in range(1, 50) if 2000**2 * plane_loop(n) < 150)
v.check("X22.14l", n_ok)
v.check("X22.14m", 2000**2 * plane_loop(n_ok))
L14, C14 = 0.4e-12, 150e-6
v.check("X22.14n", 1e6 * math.sqrt(L14 / C14))
droop14 = first_droop(L14, C14, 1000)
v.check("X22.14o", 1e3 * droop14)
v.check("X22.14p", 100 * droop14 / 0.75)
v.check("X22.14q", 1 / (2 * PI * math.sqrt(L14 * C14)) / 1e6)
v.check("X22.14r", 1e6 * 0.0375 / 1000)
v.check("X22.14s", 1e6 * optimize.brentq(lambda c: first_droop(L14, c, 1000) - 0.0375, 150e-6, 500e-6, xtol=1e-12))
# (d) on 22-10's boundary the regulator efficiency excludes the plane I^2R, so the lateral chain must supply both
lateral_in = optimize.brentq(lambda p: p * chain - (P14 + 2000**2 * plane_loop(6)), 1000, 5000)
v.check("X22.14t", lateral_in)
v.check("X22.14u", lateral_in - pin14)

v.finish()
