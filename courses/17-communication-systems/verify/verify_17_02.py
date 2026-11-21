#!/usr/bin/env python3
"""Verify chapter 17-02 (noise and SNR): text, examples, problems and lab answers.

Routes:
- thermal-noise values from the SI constants; Planck's factor from its definition;
- noise temperature and figure both ways; lossy components from the equilibrium argument, checked by a
  direct nodal noise analysis of a matched resistive pad (every resistor's noise through its transfer function);
- cascades by the Friis formula and, independently, by propagating noise powers stage by stage;
- noise bandwidths by numerical integration of |H|^2;
- the 3GPP and Wi-Fi budgets in decibels;
- the BPSK calibration and the correlation gain by Monte Carlo, against the closed forms;
- the Shannon bound from its definition and its limit by a series.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "17-02-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

CH = ROOT / "chapters" / "17-02-noise-and-snr.md"
v = Verifier.from_files("17-02", CH, ROOT / "solutions" / "17-02-solutions.md", LAB / "README.md")
K = 1.380649e-23
H = 6.62607015e-34
T0 = 290.0
rng = np.random.default_rng(1702)


def dbm(p):
    return 10 * math.log10(p / 1e-3)


def db(x):
    return 10 * math.log10(x)


def un(d):
    return 10 ** (d / 10)


def te(nf):
    return (un(nf) - 1) * T0


def planck(f, t):
    x = H * f / (K * t)
    return x / math.expm1(x)


def cascade_power(stages, t_src=T0):
    """Propagate available noise power density (W/Hz) through (Te, G) stages; return the noise factor
    measured as total output noise over the source's share (an independent route to Friis)."""
    total, src = K * t_src, K * t_src
    for t, g in stages:
        total = (total + K * t) * g
        src = src * g
    return total / src


def friis(stages_fg):
    f_tot, g = 0.0, 1.0
    for i, (f, gain) in enumerate(stages_fg):
        f_tot += f if i == 0 else (f - 1) / g
        g *= gain
    return f_tot


kT0 = K * T0

# ------------------------------------------------------------------ text
v.check("Txt 17-02.a", dbm(kT0))
v.check("Txt 17-02.b", dbm(kT0 * 20e6))
v.check("Txt 17-02.c", db(2))
v.check("Txt 17-02.d", dbm(1e-3 * (un(-100) + un(-110))))
v.check("Txt 17-02.e", planck(6e9, 290))
v.check("Txt 17-02.f", planck(6e9, 0.02))
v.check("Txt 17-02.g", H * 6e9 / (2 * K))
v.check("Txt 17-02.h", te(3))
v.check("Txt 17-02.i", db(math.log(2)))
# two-antenna MRC: amplitudes add (x2 -> power x4), independent noises add in power (x2)
v.check("Txt 17-02.j", db(4 / 2))
v.check("Txt 17-02.k", db(2.046e6 / 1e3))
v.check("Txt 17-02.l", db(4))
v.check("Txt 17-02.m", planck(1e12, 290))
v.check("Txt 17-02.n", dbm(kT0 * 2.046e6))
v.check("Txt 17-02.o", -128.5 - dbm(kT0 * 2.046e6))
v.check("Txt 17-02.p", dbm(2 * 1e-3 * un(-100)))
v.check("Txt 17-02.q", db(20e6 / 1e3))
bn_onepole, _ = integrate.quad(lambda f: 1 / (1 + f * f), 0, np.inf)
v.check("Txt 17-02.r", db(bn_onepole))
Lp = un(3)
v.check("Txt 17-02.s", (Lp - 1) * 77)
v.check("Txt 17-02.t", db(1 + (Lp - 1) * 77 / T0))
v.check("Txt 17-02.u", -57 - (-82))  # R-261 table entries
v.assert_true("Planck factor tends to 1 at low frequency", abs(planck(1e3, 290) - 1) < 1e-9)
v.assert_true("Planck x at 4 K, 6 GHz is 0.072", abs(H * 6e9 / (K * 4) - 0.072) < 5e-4)
v.assert_true("Planck x at 20 mK, 6 GHz is 14.4", abs(H * 6e9 / (K * 0.02) - 14.4) < 0.05)

# ------------------------------------------------------------------ Example 1
vn50 = math.sqrt(4 * kT0 * 50 * 1e6)
v.check("Ex 17-02.1a", vn50 * 1e6)
# available power: open-circuit source into a matched noiseless load gets (v/2)^2 / R
v.check("Ex 17-02.1b", dbm((vn50 / 2) ** 2 / 50))
v.check("Ex 17-02.1c", math.sqrt(4 * kT0 * 1e3 * 1e6) * 1e6)
v.check("Ex 17-02.1d", dbm(K * 77 * 1e6))
v.check("Ex 17-02.1e", db(290 / 77))
v.check("Ex 17-02.1f", planck(6e9, 4))
v.assert_true("1 kOhm available power equals 50 Ohm's", abs((math.sqrt(4 * kT0 * 1e3 * 1e6) / 2) ** 2 / 1e3 - kT0 * 1e6) < 1e-25)

# ------------------------------------------------------------------ Example 2
Te_lna = te(0.6)
v.check("Ex 17-02.2a", Te_lna)
v.check("Ex 17-02.2b", dbm(un(20.2) * K * (T0 + Te_lna) * 20e6))
v.check("Ex 17-02.2c", db((100 + Te_lna) / 100))
v.assert_true("degradation from a 290 K source equals F", abs((T0 + Te_lna) / T0 - un(0.6)) < 1e-12)

# ------------------------------------------------------------------ Example 3
L = un(1.5)
stA = [((L - 1) * T0, 1 / L), (Te_lna, un(20.2)), (te(8), 1.0)]
stB = [(Te_lna, un(20.2)), ((L - 1) * T0, 1 / L), (te(8), 1.0)]
FA, FB = cascade_power(stA), cascade_power(stB)
FA_f = friis([(L, 1 / L), (un(0.6), un(20.2)), (un(8), 1)])
FB_f = friis([(un(0.6), un(20.2)), (L, 1 / L), (un(8), 1)])
v.assert_true("Friis equals power propagation (A)", abs(FA - FA_f) < 1e-12)
v.assert_true("Friis equals power propagation (B)", abs(FB - FB_f) < 1e-12)
v.check("Ex 17-02.3a", db(FA))
v.check("Ex 17-02.3b", (FA - 1) * T0)
v.check("Ex 17-02.3c", db(FB))
v.check("Ex 17-02.3d", (FB - 1) * T0)
v.check("Ex 17-02.3e", db(FA) - db(FB))
v.assert_true("Ex 3 printed terms", abs(L - 1.4125) < 5e-5 and abs((un(0.6) - 1) * L - 0.2093) < 5e-5
              and abs((un(8) - 1) * L / un(20.2) - 0.0716) < 5e-5 and abs((L - 1) / un(20.2) - 0.0039) < 5e-5)

# ------------------------------------------------------------------ Example 4
e1 = 9 + db(12.5e6 / 10e6)
e2 = 20 + db(10e6 / 40e6)
v.check("Ex 17-02.4a", e1)
v.check("Ex 17-02.4b", e2)
v.check("Ex 17-02.4c", 10 / 12.5)
v.check("Ex 17-02.4d", 40 / 10)
v.assert_true("Ex 4 sanity identity", abs((e2 - e1) - (11 - db(4) - db(12.5 / 10))) < 1e-12)

# ------------------------------------------------------------------ Example 5
v.check("Ex 17-02.5a", -174 + db(52 * 12 * 15e3) + 10 - 1 + 2.5 - 3)
v.check("Ex 17-02.5b", -101.7 - (-174 + db(25 * 12 * 15e3) + 5 + 2))
floor_w = -174 + db(56 * 312.5e3)
v.check("Ex 17-02.5c", floor_w)
v.check("Ex 17-02.5d", -82 - floor_w)
v.check("Ex 17-02.5e", -82 - floor_w - 10 - 5)

# ------------------------------------------------------------------ Example 6
Te_fe = te(1.4)
Tsys = 100 + Te_fe
N0dbm = dbm(K * Tsys)
cn0 = -128.5 - N0dbm
v.check("Ex 17-02.6a", Te_fe)
v.check("Ex 17-02.6b", Tsys)
v.check("Ex 17-02.6c", N0dbm)
v.check("Ex 17-02.6d", cn0)
v.check("Ex 17-02.6e", cn0 - db(2.046e6))
v.check("Ex 17-02.6f", cn0 + db(1e-3))
v.check("Ex 17-02.6g", cn0 - db(50))
cn0_hot = -128.5 - dbm(kT0 * un(1.4))
v.check("Ex 17-02.6h", cn0_hot)
v.check("Ex 17-02.6i", cn0 - cn0_hot)
v.assert_true("Ex 6 signal more than 40x below noise", 10 ** (-(cn0 - db(2.046e6)) / 10) > 40)

# ------------------------------------------------------------------ Problem 1
for tag, B in zip("abcd", (1, 200e3, 20e6, 400e6)):
    v.check(f"17-02.1{tag}", dbm(kT0 * B))
v.check("17-02.1e", math.sqrt(4 * kT0 * 50 * 400e6) * 1e6)

# ------------------------------------------------------------------ Problem 2
v.check("17-02.2a", te(0.5))
v.check("17-02.2b", te(2))
v.check("17-02.2c", te(10))
v.check("17-02.2d", db(1 + 35 / T0))
v.check("17-02.2e", db(1 + 150 / T0))


# ------------------------------------------------------------------ Problem 3 and the lab pad: nodal noise analysis
def pad_noise(R1, R2, R3, Rs=50.0, RL=50.0, t_pad=T0, noisy_pad=True):
    """Noise power density delivered to a noiseless RL by a T-pad (R1 series, R2 shunt, R3 series) driven
    by Rs, by superposing each resistor's Norton noise current through the solved network."""
    # nodes: a (after Rs), b (centre), o (output). Conductance matrix:
    G = np.array([[1 / Rs + 1 / R1, -1 / R1, 0.0],
                  [-1 / R1, 1 / R1 + 1 / R2 + 1 / R3, -1 / R3],
                  [0.0, -1 / R3, 1 / R3 + 1 / RL]])
    Z = np.linalg.inv(G)
    # each resistor: Norton current density 4kT/R between its nodes (index, index or ground=None)
    elems = [(Rs, 0, None, T0, True), (R1, 0, 1, t_pad, noisy_pad), (R2, 1, None, t_pad, noisy_pad),
             (R3, 1, 2, t_pad, noisy_pad)]
    src_v2, tot_v2 = 0.0, 0.0
    for R, n1, n2, t, on in elems:
        if not on:
            continue
        zt = Z[2, n1] - (Z[2, n2] if n2 is not None else 0.0)
        contrib = 4 * K * t / R * zt * zt
        tot_v2 += contrib
        if R is Rs:
            src_v2 = contrib
    return src_v2 / RL, tot_v2 / RL  # one-sided W/Hz into RL


Kp = 10 ** (6 / 20)
R1 = 50 * (Kp - 1) / (Kp + 1)
R2 = 2 * 50 * Kp / (Kp * Kp - 1)
src, tot = pad_noise(R1, R2, R1)
direct_src = 4 * K * T0 * 50 * (50 / 100) ** 2 / 50  # no pad: source straight into the matched load
v.check("Lab 17-02.a", db(tot / src))
v.check("Lab 17-02.b", db(direct_src / src))
v.assert_true("matched pad delivers kT to the load", abs(tot / kT0 - 1) < 1e-9)
v.assert_true("netlist resistor values match the design", abs(R1 - 16.6139) < 5e-5 and abs(R2 - 66.9310) < 5e-5)
# 3 dB pad at 290 K and 77 K, via the same nodal analysis (equilibrium argument checked independently)
K3 = 10 ** (3 / 20)
r1, r2 = 50 * (K3 - 1) / (K3 + 1), 2 * 50 * K3 / (K3 * K3 - 1)
s3, t3 = pad_noise(r1, r2, r1)
v.check("17-02.3a", db(t3 / s3))
s77, t77 = pad_noise(r1, r2, r1, t_pad=77.0)
L3 = un(3)
v.check("17-02.3b", (t77 / s77 - 1) * T0)
v.check("17-02.3c", db(t77 / s77))
v.assert_true("nodal 77 K pad agrees with (L-1)Tp", abs((t77 / s77 - 1) * T0 - (L3 - 1) * 77) < 1e-6)
L05 = un(0.5)
v.check("17-02.3d", (L05 - 1) * 330)
v.check("17-02.3e", db(1 + (L05 - 1) * 330 / T0))

# ------------------------------------------------------------------ Problem 4
st4 = [(te(1.2), un(15)), (te(9), un(8)), (te(4), un(30))]
F4 = cascade_power(st4)
v.assert_true("P4 Friis equals power propagation", abs(F4 - friis([(un(1.2), un(15)), (un(9), un(8)), (un(4), un(30))])) < 1e-12)
v.check("17-02.4a", db(F4))
v.check("17-02.4b", (F4 - 1) * T0)
v.check("17-02.4c", un(1.2))
v.check("17-02.4d", (un(9) - 1) / un(15))
v.check("17-02.4e", (un(4) - 1) / (un(15) * un(8)))
G4 = ((un(9) - 1) + (un(4) - 1) / un(8)) / (un(1.5) - un(1.2))
v.check("17-02.4f", db(G4))
v.assert_true("P4 gain gives 1.5 dB", abs(db(cascade_power([(te(1.2), G4), (te(9), un(8)), (te(4), un(30))])) - 1.5) < 1e-9)

# ------------------------------------------------------------------ Problem 5
v.check("17-02.5a", bn_onepole)
v.check("17-02.5b", db(bn_onepole))
bn4, _ = integrate.quad(lambda u: 1 / (1 + u ** 8), 0, np.inf)
v.assert_true("Butterworth closed form", abs(bn4 - (math.pi / 8) / math.sin(math.pi / 8)) < 1e-9)
v.check("17-02.5c", bn4)
v.check("17-02.5d", db(bn4))

# ------------------------------------------------------------------ Problem 6
v.check("17-02.6a", 10 + db(2))
v.check("17-02.6b", 2 * 1.25)
v.check("17-02.6c", 10 + db(2) + db(2e6 / 2.5e6))
v.check("17-02.6d", 10 + db(4e6))

# ------------------------------------------------------------------ Problem 7
Lf = un(0.3)
Tf, Tl, Tr = (Lf - 1) * T0, 60 * Lf, te(10) * Lf / un(55)
Ts7 = 50 + Tf + Tl + Tr
v.check("17-02.7a", Tf)
v.check("17-02.7b", Tl)
v.check("17-02.7c", Tr)
v.check("17-02.7d", Ts7)
v.check("17-02.7h", dbm(K * Ts7))
c7 = -95 - dbm(K * Ts7)
v.check("17-02.7e", c7)
v.check("17-02.7f", c7 - db(30e6))
Ts7n = 50 + 60 + te(10) / un(55)
v.check("17-02.7i", Ts7 / Ts7n)
v.check("17-02.7g", db(Ts7 / Ts7n))
# independent route: antenna temperature + cascade_power of (feed, LNB, receiver) referred to the input
F7 = cascade_power([(Tf, 1 / Lf), (60.0, un(55)), (te(10), 1.0)], t_src=50.0)
v.assert_true("P7 system temperature by power propagation", abs(50 * F7 - Ts7) < 1e-9)

# ------------------------------------------------------------------ Problem 8
v.check("17-02.8a", -174 + 60 + 7 + 9 + 2)
v.check("17-02.8b", -174 + 60 + 7 + 9 + 2 - db(8))
v.check("17-02.8c", math.sqrt(8))

# ------------------------------------------------------------------ Problem 9
v.check("17-02.9a", -96.1 + db(273 / 24))
v.check("17-02.9b", -174 + db(273 * 12 * 30e3) + 10 - 1 + 2.5 - 3)
v.check("17-02.9c", -174 + db(24 * 12 * 30e3) + 10 - 1 + 2.5 - 3)

# ------------------------------------------------------------------ Problem 10 (with Monte Carlo)
eb = un(6)
s2 = (8 / eb) / 2
v.check("17-02.10a", s2)
v.check("17-02.10b", db(1 / s2))
wrong_s2 = 1 / eb
v.check("17-02.10c", db(8 / (2 * wrong_s2)))
ber_ok = norm.sf(math.sqrt(2 * eb))
ber_bad = norm.sf(math.sqrt(8 / wrong_s2))
v.check("17-02.10d", ber_ok)
v.check("17-02.10e", ber_bad)
nb_ = 1_000_000
bits = rng.integers(0, 2, nb_)
x = np.repeat(2.0 * bits - 1.0, 8)
r = x + math.sqrt(s2) * rng.standard_normal(x.size)
ber_mc = np.mean((r.reshape(nb_, 8).sum(axis=1) > 0) != bits.astype(bool))
v.assert_true("P10 Monte Carlo BER within 8% of Q(sqrt(2Eb/N0))", abs(ber_mc / ber_ok - 1) < 0.08, f"{ber_mc:.3e}")
for sps in (1, 16):
    xs = np.repeat(2.0 * bits[:400000] - 1.0, sps)
    rs = xs + math.sqrt((sps / eb) / 2) * rng.standard_normal(xs.size)
    b = np.mean((rs.reshape(400000, sps).sum(axis=1) > 0) != bits[:400000].astype(bool))
    v.assert_true(f"P10 BER independent of sps ({sps})", abs(b / ber_ok - 1) < 0.12, f"{b:.3e}")

# ------------------------------------------------------------------ Problem 11
c11 = -150 - N0dbm
v.check("17-02.11a", c11)
T11 = 10 ** ((15 - c11) / 10)
v.check("17-02.11b", T11 * 1e3)
v.check("17-02.11c", math.ceil(T11 / 0.02))

# ------------------------------------------------------------------ Problem 12
Ma = (un(1) - 1) / (1 - 1 / un(10))
Mb = (un(0.8) - 1) / (1 - 1 / un(6))
v.check("17-02.12a", Ma)
v.check("17-02.12b", Mb)
fba = cascade_power([(te(0.8), un(6)), (te(1), un(10))])
fab = cascade_power([(te(1), un(10)), (te(0.8), un(6))])
v.check("17-02.12c", db(fba))
v.check("17-02.12d", db(fab))
v.assert_true("P12 smaller noise measure first is better", (Mb < Ma) == (fba < fab))
# the noise measure is the excess noise factor of an infinite chain of identical stages
finf = cascade_power([(te(1), un(10))] * 200)
v.assert_true("P12 infinite chain equals 1 + M", abs(finf - (1 + Ma)) < 1e-9)
# random pairs: the ordering rule never fails
ok = True
for _ in range(2000):
    n1, n2 = rng.uniform(0.2, 6, 2)
    g1, g2 = rng.uniform(1, 25, 2)
    m1 = (un(n1) - 1) / (1 - 1 / un(g1))
    m2 = (un(n2) - 1) / (1 - 1 / un(g2))
    f12 = un(n1) + (un(n2) - 1) / un(g1)
    f21 = un(n2) + (un(n1) - 1) / un(g2)
    ok &= (m1 <= m2) == (f12 <= f21 + 1e-15)
v.assert_true("P12 noise-measure rule holds on random pairs", ok)

# ------------------------------------------------------------------ Problem 13
for tag, g in zip("abc", (10, 20, 30)):
    v.check(f"17-02.13{tag}", db(un(1) + (un(23) - 1) / un(g)))
g13 = (un(23) - 1) / (un(2) - un(1))
v.check("17-02.13d", db(g13))
v.check("17-02.13e", 0.97 - db(g13))

# ------------------------------------------------------------------ Problem 14
def bound(eta):
    return math.expm1(eta * math.log(2)) / eta


for tag, eta in zip("abcd", (0.5, 1, 4, 8)):
    v.check(f"17-02.14{tag}", db(bound(eta)))
v.check("17-02.14e", db(bound(1e-9)))
v.assert_true("P14 limit is ln 2", abs(bound(1e-9) - math.log(2)) < 1e-8)
v.check("17-02.14f", e1 - db(bound(0.8)))
v.check("17-02.14g", e2 - db(bound(4)))

# ------------------------------------------------------------------ lab: noise in 1 kHz, correlation gain
v.check("Lab 17-02.c", dbm(kT0 * 1e3))
code = rng.choice([-1.0, 1.0], 1023)
sym = rng.choice([-1.0, 1.0], 3000)
noise = math.sqrt(10 ** 2) * rng.standard_normal((3000, 1023))
y = (np.outer(sym, code) + noise) @ code
snr_out = np.mean((1023 * sym) ** 2) / np.var(y - 1023 * sym)
v.check("Lab 17-02.d", -20 + db(1023))
v.assert_true("correlation gain by Monte Carlo within 0.3 dB", abs(db(snr_out) - (-20 + db(1023))) < 0.3, f"{db(snr_out):.2f} dB")

# ------------------------------------------------------------------ concept checks
v.assert_true("CC2 NF of 75 K is 1.0 dB, 30 K source 5.4 dB", round(db(1 + 75 / T0), 1) == 1.0 and round(db(1 + 75 / 30), 1) == 5.4)
v.assert_true("CC3 pad + amplifier 4.0 dB", round(db(friis([(un(3), 1 / un(3)), (un(1), un(20))])), 1) == 4.0)
v.assert_true("CC4 Eb/N0 at 1 and 100 Mb/s", 70 - db(1e6) == 10 and abs(70 - db(1e8) + 10) < 1e-12)

# Y-factor example: derive F from the hot/cold temperatures directly, then compare with ENR/(Y - 1)
_T0 = 290.0
_Thot = _T0 * (1 + 10 ** 1.5)
_Y = 10.0
_Te = (_Thot - _Y * _T0) / (_Y - 1)
v.check("Txt 17-02.yf", db(1 + _Te / _T0))
v.assert_true("Y-factor: F = ENR/(Y - 1)", abs((1 + _Te / _T0) - 10 ** 1.5 / (_Y - 1)) < 1e-12)

sys.exit(v.finish())
