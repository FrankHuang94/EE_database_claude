#!/usr/bin/env python3
"""Verify every number in chapter 21-06 (oscillators and VCOs), its problems and its lab.

Independent routes (the lab module vco.py uses the closed forms and scipy.quad for the describing function):
- the tank is built from complex component impedances (inductor with series loss, capacitor with parallel loss);
  R_p is read from the admittance at resonance and Q from the numerically found 3 dB bandwidth;
- the describing function is evaluated by an FFT of the sampled tanh current, and the amplitude is cross-checked by
  integrating the oscillator's differential equation to steady state;
- the start-up rate is the real part of the linearized system's eigenvalues;
- the ISF is extracted from the differential equation by charge kicks (assert, a few per cent from -sin theta);
- tuning-line spurs use the exact Bessel sideband J1(beta); integrated phase uses scipy.quad and the Gaussian EVM;
- the divide-by-2 phase error is measured by simulating two toggle flip-flops clocked by a sampled clock;
- the RC-CR network is solved by nodal analysis; injection locking and the Adler beat are confirmed by simulation;
- ngspice confirms the amplitude, the Groszkowski frequency, injection locking and the RC-CR network.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, special

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "21-06-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import vco as lab  # noqa: E402

_files = [ROOT / "chapters" / "21-06-oscillators-and-vcos.md", ROOT / "solutions" / "21-06-solutions.md",
          LAB / "README.md"]
v = Verifier.from_files("21-06", *[p for p in _files if p.exists()])
lg = math.log10
db10 = lambda x: 10 * lg(x)  # noqa: E731
db20 = lambda x: 20 * lg(x)  # noqa: E731
K_B = 1.380649e-23
Q_E = 1.602176634e-19
T = 300.0
kT = K_B * T
VT = kT / Q_E


# ---------------------------------------------------------------- helpers (independent of vco.py)
def tank_numeric(f0, L, QL, QC):
    """Component-level tank: L with series r_s = w0 L / QL, C with parallel R = QC / (w0 C), C = 1/(w0^2 L).
    Returns C, R_p (1/Re Y at the admittance's zero-susceptance frequency) and Q = w0 C R_p."""
    w0 = 2 * math.pi * f0
    C = 1 / (w0 * w0 * L)
    rs = w0 * L / QL
    Rc = QC / (w0 * C)
    Y = lambda w: 1 / (rs + 1j * w * L) + 1j * w * C + 1 / Rc  # noqa: E731
    wr = optimize.brentq(lambda w: Y(w).imag, 0.9 * w0, 1.1 * w0, xtol=1e-6)
    Rp = 1 / Y(wr).real
    # Q from its energy definition at w0: w0 (peak stored energy C V^2/2) / (power V^2 / 2 R_p)
    return C, Rp, w0 * C * Rp, wr


def df_fft(V, I0, V0, n=1 << 14):
    """Describing function of i = I0 tanh(v/V0) from an FFT of one sampled period."""
    x = 2 * np.pi * np.arange(n) / n
    i = I0 * np.tanh(V * np.cos(x) / V0)
    return 2 * abs(np.fft.rfft(i)[1]) / n / V


def amp_fft(Rp, I0, V0):
    return optimize.brentq(lambda V: df_fft(V, I0, V0) - 1 / Rp, 1e-3 * V0, 10 * I0 * Rp, xtol=1e-14)


def ode_fundamental(Q, I0n, V0n, cycles=300):
    """Normalized oscillator (L = C = 1, R = Q); fundamental amplitude of v over the last period."""
    f = lambda t, y: [-y[0] / Q - y[1] + I0n * math.tanh(y[0] / V0n), y[0]]  # noqa: E731
    t_end = 2 * math.pi * cycles
    ts = np.linspace(t_end - 2 * math.pi, t_end, 4097)[:-1]
    sol = integrate.solve_ivp(f, (0, t_end), [1e-3, 0], method="DOP853", rtol=1e-11, atol=1e-13, t_eval=ts)
    return 2 * abs(np.fft.rfft(sol.y[0])[1]) / len(ts)


# ================================================================ Example 21-06.1
F0, L0 = 5e9, 1e-9
W0 = 2 * math.pi * F0
C1, RP1, Q1, WR1 = tank_numeric(F0, L0, 15, 50)
v.check("Ex 21-06.1a", C1 * 1e12)
v.check("Ex 21-06.1b", Q1)
v.check("Ex 21-06.1c", RP1)
v.check("Ex 21-06.1d", 2 / RP1 * 1e3)
gm1 = 1e-3 / VT
v.check("Ex 21-06.1e", gm1 * RP1 / 2)
I0, V0 = 1e-3, 2 * VT
VH = 4 * I0 * RP1 / math.pi
v.check("Ex 21-06.1f", VH)
VDF = amp_fft(RP1, I0, V0)
v.check("Ex 21-06.1g", VDF)
v.assert_true("DF amplitude agrees with vco.amplitude_df",
              abs(lab.amplitude_df(RP1, I0, V0) / VDF - 1) < 1e-9)
# time-domain cross-check in normalized units: a = 1 V, b = w0 C amperes
b = W0 * C1
v.assert_true("ODE fundamental matches the describing function to 0.05%",
              abs(ode_fundamental(Q1, I0 / b, V0) / VDF - 1) < 5e-4)
v.check("Ex 21-06.1h", VH * (1 - math.pi ** 2 / 24 * (V0 / VH) ** 2))
A = np.array([[(gm1 / 2 - 1 / RP1) / C1, -1 / C1], [1 / L0, 0.0]])
sigma = max(np.linalg.eigvals(A).real)
v.check("Ex 21-06.1i", 1 / sigma * 1e9)
PS1 = VDF ** 2 / (2 * RP1)
v.check("Ex 21-06.1j", PS1 * 1e3)
ETA1 = PS1 / (2e-3 * 1.2)
v.check("Ex 21-06.1k", ETA1 * 100)

# ================================================================ Example 21-06.2
QMAX = C1 * VDF
v.check("Ex 21-06.2a", QMAX * 1e12)
SI = 4 * kT / RP1
v.check("Ex 21-06.2b", SI)
th = np.linspace(0, 2 * np.pi, 4096, endpoint=False)
G2 = float(np.mean(np.sin(th) ** 2))
dw = 2 * math.pi * 1e6
L_isf = G2 * SI / (2 * QMAX ** 2 * dw ** 2)
v.check("Ex 21-06.2c", db10(L_isf))
L_lee = (2 * kT / PS1) * (1 + (F0 / (2 * Q1 * 1e6)) ** 2)
v.check("Ex 21-06.2d", db10(L_lee))
v.assert_true("ISF and Leeson agree in the 1/f^2 region", abs(db10(L_isf) - db10(L_lee)) < 1e-3)
LF2 = db10(2 * L_isf)
v.check("Ex 21-06.2e", LF2)
FOM2 = -LF2 + db20(F0 / 1e6) - db10(2.4e-3 / 1e-3)
v.check("Ex 21-06.2f", FOM2)
BOUND = db10(2 * Q1 ** 2 * 1e-3 / kT)
v.check("Ex 21-06.2g", BOUND)
v.assert_true("FoM = bound - 10log F + 10log eta", abs(BOUND - db10(2) + db10(ETA1) - FOM2) < 1e-9)
FC = 1e6 * 0.15 ** 2
v.check("Ex 21-06.2h", FC / 1e3)
v.check("Ex 21-06.2i", db10(2 * G2 * SI / (2 * QMAX ** 2 * (2 * math.pi * 1e4) ** 2) * (1 + FC / 1e4)))


# ================================================================ Example 21-06.3
def f_of(C, L=L0):
    # oscillation frequency as the root of L C s^2 + 1 = 0
    return abs(np.roots([L * C, 0, 1])[0].imag) / (2 * math.pi)


CF = 0.70e-12
bands = {}
for code in (0, 7):
    cmin = CF + code * 60e-15 + 0.15e-12
    bands[code] = (f_of(cmin + 0.15e-12), f_of(cmin))
lo0, hi0 = bands[0]
lo7, hi7 = bands[7]
v.check("Ex 21-06.3a", lo0 / 1e9)
v.check("Ex 21-06.3b", hi0 / 1e9)
v.check("Ex 21-06.3c", (hi0 - lo0) / ((hi0 + lo0) / 2) * 100)
v.check("Ex 21-06.3d", (hi0 - lo0) / 1e6)
v.check("Ex 21-06.3e", lo7 / 1e9)
v.check("Ex 21-06.3f", hi7 / 1e9)
v.check("Ex 21-06.3g", (hi7 - lo7) / 1e6)
v.check("Ex 21-06.3h", (hi0 - lo7) / ((hi0 + lo7) / 2) * 100)
v.check("Ex 21-06.3i", (hi0 - lo0) / (hi7 - lo7))
v.check("Ex 21-06.3j", (1.345 / 0.925) ** 1.5)

# ================================================================ Example 21-06.4
SV = 4 * kT * 1e3
v.check("Ex 21-06.4a", math.sqrt(SV) * 1e9)
for key, K in (("b", 400e6), ("c", 50e6)):
    # the noise in a 1 Hz band as a sinusoid of peak sqrt(2 S_v): each sideband (beta/2)^2
    beta = K * math.sqrt(2 * SV) / 1e6
    v.check(f"Ex 21-06.4{key}", db10((beta / 2) ** 2))
for key, K in (("d", 400e6), ("e", 50e6)):
    beta = K * 10e-6 / 1e6
    v.check(f"Ex 21-06.4{key}", db20(special.jv(1, beta) / special.jv(0, beta)))

# ================================================================ Example 21-06.5
v.check("Ex 21-06.5a", -131.9 + db20(1 / 4))
v.check("Ex 21-06.5b", db20(77 / 2.4))
v.check("Ex 21-06.5c", -96 - db20(77 / 2.4))
var = 2 * 1e-10 * 3e5 * integrate.quad(lambda x: 1 / (1 + x * x), 0, np.inf)[0]  # f = x f_c
phi = math.sqrt(var)
v.check("Ex 21-06.5d", phi * 1e3)
v.check("Ex 21-06.5e", math.degrees(phi))
evm = math.sqrt(2 * (1 - math.exp(-var / 2)))  # Gaussian phase: E|exp(j phi) - 1|^2 = 2 - 2 exp(-var/2)
v.check("Ex 21-06.5f", evm * 100)
v.check("Ex 21-06.5g", db20(evm))
v.check("Ex 21-06.5h", evm ** 2 / 10 ** (-3.8) * 100)


# ================================================================ Example 21-06.6
def div2_phase(duty, n=50000, cycles=64):
    """Two toggle flip-flops, one on the clock's rising edges and one on its falling edges; phase difference of
    their fundamentals in degrees."""
    k = np.arange(n * cycles)                           # n samples per clock period (duty * n is an integer)
    clk = (k % n) < round(duty * n)
    rise = np.flatnonzero(clk[1:] & ~clk[:-1]) + 1
    fall = np.flatnonzero(~clk[1:] & clk[:-1]) + 1
    qi = np.zeros(k.size)
    qq = np.zeros(k.size)
    for k, idx in enumerate(rise):
        qi[idx:] = k % 2 == 0
    for k, idx in enumerate(fall):
        qq[idx:] = k % 2 == 0
    sl = slice(n * 8, n * 8 + n * 48)                   # 24 output periods after start-up
    m = 24
    pi_ = np.angle(np.fft.rfft(qi[sl] - qi[sl].mean())[m])
    pq = np.angle(np.fft.rfft(qq[sl] - qq[sl].mean())[m])
    return (math.degrees(pi_ - pq) + 180) % 360 - 180


def irr_phasor(eps, theta_rad):
    g = (1 + eps) * cmath.exp(1j * theta_rad)
    return db10(abs(1 + g) ** 2 / abs(1 - g) ** 2)


TH6 = abs(abs(div2_phase(0.51)) - 90)
v.check("Ex 21-06.6a", TH6)
v.check("Ex 21-06.6b", irr_phasor(0, math.radians(TH6)))


def rc_cr_nodal(f, R=1e3, C=1 / (2 * math.pi * 2.45e9 * 1e3)):
    """Nodal solution of the two-node RC-CR network driven by 1 V."""
    s = 2j * math.pi * f
    Yg = np.array([[1 / R + s * C, 0], [0, s * C + 1 / R]])
    Iin = np.array([1 / R, s * C])
    vi, vq = np.linalg.solve(Yg, Iin)
    return vi, vq


vi, vq = rc_cr_nodal(2.40e9)
v.check("Ex 21-06.6c", db20(abs(vq / vi)))
v.check("Ex 21-06.6d", math.degrees(cmath.phase(vq / vi)))
v.check("Ex 21-06.6e", irr_phasor(abs(vq / vi) - 1, 0))
vi, vq = rc_cr_nodal(2.50e9)
v.check("Ex 21-06.6f", irr_phasor(abs(vq / vi) - 1, 0))
vi, vq = rc_cr_nodal(2.45e9, C=1.1 / (2 * math.pi * 2.45e9 * 1e3))
v.check("Ex 21-06.6g", irr_phasor(abs(vq / vi) - 1, 0))

# ================================================================ Example 21-06.7
half_bw = F0 / (2 * Q1)


def lock_geom(r):
    # largest rotation of I_osc + I_inj (tangent from the origin to the circle of radius r) -> tan(alpha_max)
    a = max(math.atan2(r * math.sin(p), 1 + r * math.cos(p)) for p in np.linspace(0, math.pi, 200001))
    return half_bw * math.tan(a)


FL1 = lock_geom(0.01)
v.check("Ex 21-06.7a", FL1 / 1e6)
v.check("Ex 21-06.7b", lock_geom(0.10) / 1e6)
TB = integrate.quad(lambda p: 1 / (10e6 - FL1 * math.sin(p)), 0, 2 * math.pi)[0]  # seconds per cycle of slip x 2 pi
beat = 2 * math.pi / TB
v.check("Ex 21-06.7c", beat / 1e6)
v.check("Ex 21-06.7d", (10e6 - beat) / 1e6)
v.check("Ex 21-06.7e", 5.010)
v.check("Ex 21-06.7f", FL1 ** 2 / (2 * 10e6) / 1e6)
v.check("Ex 21-06.7g", (5.010e9 - 4.9968e9) / 1e6)

# ================================================================ Example 21-06.8
fom = lambda Ldb, f0, df, P: -Ldb + db20(f0 / df) - db10(P / 1e-3)  # noqa: E731
v.check("Ex 21-06.8a", fom(-152, 4e9, 20e6, 5.5e-3 * 1.2))
v.check("Ex 21-06.8b", fom(-106.5, 29.1e9, 1e6, 0.88e-3))
v.check("Ex 21-06.8c", fom(-106.5, 24.5e9, 1e6, 0.88e-3))
La = -152 + db20(20e6 / 1e6) + db20(28 / 4)
Lb = -106.5 - db20(29.1 / 28)
v.check("Ex 21-06.8d", La)
v.check("Ex 21-06.8e", Lb)
v.check("Ex 21-06.8f", Lb - La)
v.check("Ex 21-06.8g", next(n for n in range(1, 10) if db10(n) >= Lb - La))

# ================================================================ text values
v.check("Txt 21-06.a", math.sqrt(G2))
gros = -sum(1 / (2 * (n * n - 1) * Q1 ** 2) for n in range(3, 200001, 2))
v.check("Txt 21-06.b", gros * 100)
# Groszkowski with FFT harmonics of the tanh current at the describing-function amplitude
x = 2 * np.pi * np.arange(1 << 14) / (1 << 14)
Ih = 2 * np.abs(np.fft.rfft(I0 * np.tanh(VDF * np.cos(x) / V0))) / x.size
s = sum((n * n - 1) * (Ih[n] / abs(1 / RP1 + 1j * W0 * C1 * (n - 1 / n)) / VDF) ** 2 for n in range(3, 60, 2))
FGROS = F0 * (1 - s / 2)
v.check("Txt 21-06.c", FGROS / 1e9)
v.assert_true("ODE free-running shift within 5% of the Groszkowski prediction",
              abs(lab.free_running_shift(Q1, I0 / b, V0) / (-s / 2) - 1) < 0.05)
v.check("Txt 21-06.d", db20(2))
v.check("Txt 21-06.e", 2 * RP1 * C1 * 1e9)
v.check("Txt 21-06.f", fom(-153, 1.1e9, 3e6, 3.7e-3 * 2.5))

# ================================================================ lab
L_tank_dev = 2 * L_isf                                     # Example 21-06.2e, linear
L_line = (400e6 * math.sqrt(2 * SV) / 1e6 / 2) ** 2       # Example 21-06.4b, linear
v.check("Lab 21-06.a", db10(L_tank_dev + L_line))
v.check("Lab 21-06.b", db10((L_tank_dev + L_line) * 100))
worst = min(irr_phasor(abs(q_ / i_) - 1, 0)
            for rc in (0.9, 1.1) for f in np.linspace(2.40e9, 2.50e9, 101)
            for i_, q_ in [rc_cr_nodal(f, C=rc / (2 * math.pi * 2.45e9 * 1e3))])
v.check("Lab 21-06.c", worst)
vi, vq = rc_cr_nodal(2.50e9, C=1.1 / (2 * math.pi * 2.45e9 * 1e3))
v.check("Lab 21-06.d", irr_phasor(abs(vq / vi) - 1, 0))
wL_n = (1 / (2 * 10.0)) * math.tan(math.asin(0.05))       # geometric lock range, normalized w0 = 1
v.check("Lab 21-06.e", wL_n)
v.check("Lab 21-06.f", math.sqrt((2 * wL_n) ** 2 - wL_n ** 2))

# ---------------------------------------------------------------- ISF and injection locking by simulation
Q_N, I0_N, V0_N = Q1, 1.0, Q1 / 7.01          # Example 21-06.1 in normalized units (loop gain 7)
g = lab.isf(Q_N, I0_N, V0_N, np.linspace(0, 2 * np.pi, 8, endpoint=False))
v.assert_true("simulated ISF rms within 3% of 1/sqrt(2)", abs(math.sqrt(np.mean(g ** 2)) * math.sqrt(2) - 1) < 0.03)
v.assert_true("simulated ISF at the zero crossing within 5% of -1", abs(g[2] + 1) < 0.05)
v.assert_true("simulated ISF average below 0.01", abs(np.mean(g)) < 0.01)
gq = lab.isf(50.0, 1.0, 50.0 / 7.01, [math.pi / 2])
v.assert_true("at Q = 50 the zero-crossing ISF is -1 within 0.5%", abs(gq[0] + 1) < 5e-3)
# Adler: soft nonlinearity (loop gain 3), Q = 10, 5% injection, detuning measured from the free-running frequency
Qa, Va = 10.0, 10.0 / 3
w_free = lab.free_running_shift(Qa, 1.0, Va)
amp = math.hypot(*lab.settle(Qa, 1.0, Va))
r = 0.05
wL = lab.lock_range(1 / (2 * math.pi), Qa, r) * 2 * math.pi
rate_in, _, _ = lab.injection_beat(Qa, 1.0, Va, r * amp / Qa, w_free + 0.9 * wL, cycles=1500, skip=300)
v.assert_true("injection at 0.9 lock range locks (slip rate < 2% of the lock range)", abs(rate_in) < 0.02 * wL)
rate_out, _, _ = lab.injection_beat(Qa, 1.0, Va, r * amp / Qa, w_free + 2 * wL, cycles=1500, skip=300)
v.assert_true("beat at 2 lock ranges within 4% of sqrt(3) w_L", abs(-rate_out / (math.sqrt(3) * wL) - 1) < 0.04)

# ================================================================ problems
C_1, RP_1, Q_1, _ = tank_numeric(6e9, 0.8e-9, 12, 40)
W6 = 2 * math.pi * 6e9
v.check("21-06.1a", C_1 * 1e12)
v.check("21-06.1b", Q_1)
v.check("21-06.1c", RP_1)
v.check("21-06.1d", 2 / RP_1 * 1e3)
IC = optimize.brentq(lambda ic: (ic / VT) * RP_1 / 2 - 3, 1e-6, 1e-2)
v.check("21-06.1e", IC * 1e3)
v.check("21-06.1f", 2 * IC * 1e3)
V2 = 4 * 1.5e-3 * RP_1 / math.pi
v.check("21-06.2a", V2)
v.check("21-06.2b", V2 / 2)
I2 = optimize.brentq(lambda i: 4 * (i / 2) * RP_1 / math.pi - 0.8, 1e-4, 1e-1)
v.check("21-06.2c", I2 * 1e3)
PS2 = 0.8 ** 2 / (2 * RP_1)
v.check("21-06.2d", PS2 / (I2 * 1.0) * 100)
v.check("21-06.2e", PS2 * 1e3)
gm3 = 1e-3 / VT
v.check("21-06.3a", gm3 * RP_1 / 2)
VH3 = 4 * 1e-3 * RP_1 / math.pi
v.check("21-06.3b", VH3)
v.check("21-06.3c", VH3 * (1 - math.pi ** 2 / 24 * (2 * VT / VH3) ** 2))
V3 = amp_fft(RP_1, 1e-3, 2 * VT)
v.check("21-06.3d", V3)
A3 = np.array([[(gm3 / 2 - 1 / RP_1) / C_1, -1 / C_1], [1 / 0.8e-9, 0.0]])
v.check("21-06.3e", 1 / max(np.linalg.eigvals(A3).real) * 1e9)
v.check("21-06.3f", 2 * RP_1 * C_1 * 1e9)
dq = 1e-15
G = lambda th: -math.sin(th)  # noqa: E731
v.check("21-06.4a", abs(G(math.pi / 2)) * dq / QMAX * 1e3)
v.check("21-06.4b", math.degrees(dq / QMAX))
v.check("21-06.4c", dq / QMAX / W0 * 1e15)
v.check("21-06.4d", dq / QMAX * 100)
v.check("21-06.4e", 2 * RP1 * C1 * 1e9)
v.check("21-06.4f", abs(G(math.pi / 4)) * dq / QMAX * 1e3)
PS5 = V3 ** 2 / (2 * RP_1)
v.check("21-06.5a", PS5 * 1e3)
v.check("21-06.5b", PS5 / 2e-3 * 100)
for key, dfo in (("c", 1e6), ("d", 10e6)):
    # ISF route with F folded into the noise current, plus Leeson's white floor 2FkT/Ps
    Sx = 2.5 * 4 * kT / RP_1
    Lx = 0.5 * Sx / (2 * (C_1 * V3) ** 2 * (2 * math.pi * dfo) ** 2) + 2 * 2.5 * kT / PS5
    v.check(f"21-06.5{key}", db10(Lx))
L5 = db10(0.5 * 2.5 * 4 * kT / RP_1 / (2 * (C_1 * V3) ** 2 * (2 * math.pi * 1e6) ** 2) + 2 * 2.5 * kT / PS5)
v.check("21-06.5e", fom(L5, 6e9, 1e6, 2e-3))
v.check("21-06.5f", db10(2 * Q_1 ** 2 * 1e-3 / (2.5 * kT)))
fa, fb = 2e6 * (0.02 / 0.6) ** 2, 2e6 * (0.1 / 0.6) ** 2
v.check("21-06.6a", fa / 1e3)
v.check("21-06.6b", fb / 1e3)
v.check("21-06.6c", db10(1 + fa / 1e4))
v.check("21-06.6d", db10(1 + fb / 1e4))
v.check("21-06.6e", db10(1 + fb / 1e4) - db10(1 + fa / 1e4))
c55 = optimize.brentq(lambda c: f_of(c) - 5.5e9, 0.1e-12, 5e-12, xtol=1e-20)
c45 = optimize.brentq(lambda c: f_of(c) - 4.5e9, 0.1e-12, 5e-12, xtol=1e-20)
v.check("21-06.7a", c45 / c55)
v.check("21-06.7b", c55 * 1e12)
v.check("21-06.7c", c45 * 1e12)
v.check("21-06.7d", (c55 - 0.6e-12) * 1e12)
v.check("21-06.7e", (c45 - 0.6e-12) * 1e12)
v.check("21-06.7f", (c45 - 0.6e-12) / (c55 - 0.6e-12))
bank = lambda code: sum((80e-15 if (code >> bit) & 1 else 20e-15) * (1 << bit) for bit in range(4))  # noqa: E731
v.check("21-06.8a", bank(0) * 1e12)
v.check("21-06.8b", bank(15) * 1e12)
f8 = lambda C: f_of(C, 1.2e-9)  # noqa: E731
v.check("21-06.8c", f8(0.5e-12 + bank(0) + 0.2e-12) / 1e9)
v.check("21-06.8d", f8(0.5e-12 + bank(0) + 0.1e-12) / 1e9)
v.check("21-06.8e", f8(0.5e-12 + bank(15) + 0.2e-12) / 1e9)
v.check("21-06.8f", f8(0.5e-12 + bank(15) + 0.1e-12) / 1e9)
top, bot = f8(0.5e-12 + bank(0) + 0.1e-12), f8(0.5e-12 + bank(15) + 0.2e-12)
v.check("21-06.8g", (top - bot) / ((top + bot) / 2) * 100)
v.check("21-06.8h", f8(0.6e-12) / 1e9)
SV9 = 4 * kT * 2e3
v.check("21-06.9a", math.sqrt(SV9) * 1e9)
K9 = optimize.brentq(lambda K: db10((K * math.sqrt(2 * SV9) / 1e6 / 2) ** 2) + 130, 1e6, 1e9)
v.check("21-06.9b", K9 / 1e6)
beta9 = K9 * 50e-6 / 10e6
v.check("21-06.9c", db20(special.jv(1, beta9) / special.jv(0, beta9)))
v.check("21-06.10a", -128 + db20(3))
v.check("21-06.10b", -128 - db20(8))
v.check("21-06.10c", -148 - db20(8))
v.check("21-06.10d", db10(10 ** ((-148 - db20(8)) / 10) + 10 ** (-155 / 10)))
var11 = 2 * 10 ** -9.5 * 5e5 * integrate.quad(lambda x: 1 / (1 + x * x), 0, np.inf)[0]
evm11 = math.sqrt(2 * (1 - math.exp(-var11 / 2)))
v.check("21-06.11a", math.sqrt(var11) * 1e3)
v.check("21-06.11b", math.degrees(math.sqrt(var11)))
v.check("21-06.11c", evm11 * 100)
v.check("21-06.11d", (evm11 / 0.035) ** 2 * 100)
v.check("21-06.11e", (evm11 / 0.025) ** 2 * 100)
L11 = optimize.brentq(lambda Ldb: math.sqrt(2 * (1 - math.exp(-math.pi * 10 ** (Ldb / 10) * 5e5 / 2))) - 0.01,
                      -130, -80)
v.check("21-06.11f", L11)
th12 = optimize.brentq(lambda t: irr_phasor(0, math.radians(t)) - 40, 0.01, 10)
v.check("21-06.12a", th12)
v.check("21-06.12b", th12 / 180 * 100)
th12c = optimize.brentq(lambda t: irr_phasor(0.01, math.radians(t)) - 40, 0.01, 10)
v.check("21-06.12c", th12c)
v.check("21-06.12d", th12c / 180 * 100)
v.check("21-06.12e", math.degrees(math.sqrt(4e-4 - 1e-4)))


def rc_cr_mismatch(f, RI, RQ, C):
    s_ = 2j * math.pi * f
    vi_ = (1 / RI) / (1 / RI + s_ * C)
    vq_ = (s_ * C) / (s_ * C + 1 / RQ)
    return vq_ / vi_


r13 = rc_cr_mismatch(2.45e9, 1.01e3, 1.00e3, 1 / (2 * math.pi * 2.45e9 * 1e3))
ph13 = math.degrees(cmath.phase(r13))
v.check("21-06.13a", ph13)
v.check("21-06.13b", ph13 - 90)
v.check("21-06.13c", (abs(r13) - 1) * 100)
v.check("21-06.13d", irr_phasor(abs(r13) - 1, math.radians(ph13 - 90)))
v.check("21-06.13e", db10(4 / ((abs(r13) - 1) ** 2 + math.radians(ph13 - 90) ** 2)))
fl14 = optimize.brentq(lambda fl: fl * fl / (2 * 20e6) - 1e4, 1e3, 1e7)
v.check("21-06.14a", fl14 / 1e3)
r14 = fl14 / (5e9 / 20)
v.check("21-06.14b", r14)
v.check("21-06.14c", db20(r14))
v.check("21-06.14d", (20e6 - 2 * math.pi / integrate.quad(lambda p: 1 / (20e6 - fl14 * math.sin(p)), 0,
                                                            2 * math.pi)[0]) / 1e3)
v.check("21-06.15a", fom(-120, 10e9, 1e6, 10e-3))
v.check("21-06.15b", -120 - db10(4))
v.check("21-06.15c", fom(-120 - db10(4), 10e9, 1e6, 40e-3))
v.check("21-06.15d", optimize.brentq(lambda n: db10(n) - 5, 1, 10))
v.check("21-06.15e", math.ceil(10 ** 0.5))
v.check("21-06.15f", db10(2 * (2 * Q_1) ** 2 * 1e-3 / kT) - db10(2 * Q_1 ** 2 * 1e-3 / kT))

sys.exit(v.finish())
