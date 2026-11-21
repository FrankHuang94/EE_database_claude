#!/usr/bin/env python3
"""Verify chapter 17-06 (bandpass digital modulation and BER): text, examples, problems and lab answers.

Routes:
- constellation energies, minimum distances and peak-to-average ratios by enumerating the points;
- PSK error rates by Craig's integral and by Monte Carlo; QAM in closed form and by Monte Carlo;
- DPSK and binary FSK by simulating their receivers;
- EVM by simulating impaired transmitters (phase noise, I/Q imbalance);
- Gray-coding benefit by simulation with both labellings;
- DVB-S2 comparisons from the logged table (R-276) against the Shannon bound;
- the 2-D signal-space claim by integrating the carrier basis functions.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "17-06-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import modulation as md  # noqa: E402

CH = ROOT / "chapters" / "17-06-bandpass-digital-modulation.md"
v = Verifier.from_files("17-06", CH, ROOT / "solutions" / "17-06-solutions.md", LAB / "README.md")
rng = np.random.default_rng(1706)
Q, Qi = norm.sf, norm.isf


def db(x):
    return 10 * math.log10(x)


def un(d):
    return 10 ** (d / 10)


def fom(pts):
    """d_min^2 / (4 Eb) from the points themselves."""
    k = math.log2(len(pts))
    return md.dmin(pts) ** 2 / (4 * md.es(pts) / k)


# 2-D signal space of one symbol: phi1, phi2 orthonormal for fc*T large
T, fc = 1.0, 50.0
t = np.linspace(0, T, 200001)
p1 = math.sqrt(2 / T) * np.cos(2 * np.pi * fc * t)
p2 = -math.sqrt(2 / T) * np.sin(2 * np.pi * fc * t)
v.assert_true("carrier basis functions are orthonormal", abs(integrate.trapezoid(p1 * p1, t) - 1) < 1e-6 and abs(integrate.trapezoid(p1 * p2, t)) < 1e-6)

# ------------------------------------------------------------------ text
v.check("Txt 17-06.a", db(fom(md.psk(8)[0])))
v.check("Txt 17-06.b", db(fom(md.psk(16)[0])))
for tag, m in zip("cdef", (16, 64, 256, 1024)):
    v.check(f"Txt 17-06.{tag}", db(fom(md.qam(m)[0])))
    v.assert_true(f"QAM{m} figure of merit formula", abs(fom(md.qam(m)[0]) - 3 * math.log2(m) / (2 * (m - 1))) < 1e-12)
v.check("Txt 17-06.g", db(fom(md.qam(16)[0]) / fom(md.psk(16)[0])))
v.check("Txt 17-06.h", md.papr_db(md.qam(16)[0]))
v.check("Txt 17-06.i", md.papr_db(md.qam(64)[0]))
v.check("Txt 17-06.j", db(math.log(1 / 2e-5)) - db(Qi(1e-5) ** 2 / 2))
v.check("Txt 17-06.k", 6 / 1.22)
v.check("Txt 17-06.l", db(1 / 0.035 ** 2))
v.check("Txt 17-06.m", db(1 / 0.025 ** 2))
v.check("Txt 17-06.n", db(2 * math.log(1 / 2e-5)) - db(Qi(1e-5) ** 2))
v.check("Txt 17-06.o", db(2 * math.log(1 / 2e-5)) - db(Qi(1e-5) ** 2 / 2))
v.check("Txt 17-06.p", 6 / 255)
v.check("Txt 17-06.q", 6 / 1023)
v.check("Txt 17-06.r", db(1 / 0.025 ** 2) - db(1 / 0.035 ** 2))

# ------------------------------------------------------------------ Example 1
v.check("Ex 17-06.1a", 2 * 20)
v.check("Ex 17-06.1b", 1.25 * 20)
v.check("Ex 17-06.1c", 40 / 25)
q8 = Q(math.sqrt(2 * un(8)))
v.check("Ex 17-06.1d", q8)
v.check("Ex 17-06.1e", 2 * q8 - q8 * q8)
qp, ql = md.psk(4)
ser, ber = md.simulate(qp, ql, db(2 * un(8)), 2_000_000, rng)
v.assert_true("Monte Carlo QPSK BER and SER at 8 dB within 8%", abs(ber / q8 - 1) < 0.08 and abs(ser / (2 * q8 - q8 * q8) - 1) < 0.08, f"{ber:.3e} {ser:.3e}")

# ------------------------------------------------------------------ Example 2
e15 = un(15)
v.check("Ex 17-06.2a", md.ser_psk_craig(4, e15))
v.check("Ex 17-06.2b", md.ser_psk_craig(8, e15))
v.assert_true("8-PSK nearest-neighbour equals Craig to 3 digits", abs(md.ser_psk_nn(8, e15) / md.ser_psk_craig(8, e15) - 1) < 1e-3)
v.check("Ex 17-06.2c", db(fom(md.psk(8)[0])))
p8, l8 = md.psk(8)
ser8, _ = md.simulate(p8, l8, 15.0, 2_000_000, rng)
v.assert_true("Monte Carlo 8-PSK SER within 8%", abs(ser8 / md.ser_psk_craig(8, e15) - 1) < 0.08, f"{ser8:.3e}")

# ------------------------------------------------------------------ Example 3
es12 = 4 * un(12)
v.check("Ex 17-06.3a", md.ser_qam(16, es12))
v.check("Ex 17-06.3b", md.ser_psk_craig(16, es12))
v.check("Ex 17-06.3c", db(fom(md.qam(16)[0]) / fom(md.psk(16)[0])))
p16, l16 = md.qam(16)
s16, _ = md.simulate(p16, l16, db(es12), 2_000_000, rng)
v.assert_true("Monte Carlo 16-QAM SER within 8%", abs(s16 / md.ser_qam(16, es12) - 1) < 0.08, f"{s16:.3e}")

# ------------------------------------------------------------------ Example 4
v.check("Ex 17-06.4a", db(1 / 0.035 ** 2))
v.check("Ex 17-06.4b", db(1 / 0.025 ** 2))
v.check("Ex 17-06.4c", md.ser_qam(256, 1 / 0.035 ** 2))
v.check("Ex 17-06.4d", md.ser_qam(1024, 1 / 0.025 ** 2))
v.check("Ex 17-06.4e", 100 * 10 ** (-35 / 20))

# ------------------------------------------------------------------ Example 5 (DVB-S2 table values, R-276)
for tag_e, tag_s, tag_g, eta, esn0 in (("a", "c", "d", 0.988858, 1.00), ("b", "e", "f", 4.453027, 16.05)):
    v.check(f"Ex 17-06.5{tag_e}", esn0 - db(eta))
    v.check(f"Ex 17-06.5{tag_s}", db(2 ** eta - 1))
    v.check(f"Ex 17-06.5{tag_g}", esn0 - db(2 ** eta - 1))

# ------------------------------------------------------------------ Example 6
e10 = un(10)
v.check("Ex 17-06.6a", Q(math.sqrt(2 * e10)))
v.check("Ex 17-06.6b", md.ber_dpsk(e10))
v.check("Ex 17-06.6c", md.ber_fsk_coherent(e10))
v.check("Ex 17-06.6d", md.ber_fsk_noncoherent(e10))
v.check("Ex 17-06.6e", db(Qi(1e-5) ** 2 / 2))
v.check("Ex 17-06.6f", db(math.log(1 / 2e-5)))
v.check("Ex 17-06.6g", db(2 * math.log(1 / 2e-5)))
sim_d = md.simulate_dpsk(8.0, 2_000_000, rng)
sim_nc = md.simulate_bfsk(10.0, 2_000_000, rng, coherent=False)
sim_c = md.simulate_bfsk(10.0, 2_000_000, rng, coherent=True)
v.assert_true("Monte Carlo DPSK at 8 dB within 6%", abs(sim_d / md.ber_dpsk(un(8)) - 1) < 0.06, f"{sim_d:.3e}")
v.assert_true("Monte Carlo noncoherent BFSK within 5%", abs(sim_nc / md.ber_fsk_noncoherent(e10) - 1) < 0.05, f"{sim_nc:.3e}")
v.assert_true("Monte Carlo coherent BFSK within 6%", abs(sim_c / md.ber_fsk_coherent(e10) - 1) < 0.06, f"{sim_c:.3e}")

# ------------------------------------------------------------------ problems
z = 3 - 4j
v.check("17-06.1a", z.real)
v.check("17-06.1b", z.imag)
v.check("17-06.1c", abs(z))
v.check("17-06.1d", math.degrees(math.atan2(z.imag, z.real)))
tt = np.linspace(0, 1, 100001)
sig = 3 * np.cos(2 * np.pi * 20 * tt) + 4 * np.sin(2 * np.pi * 20 * tt)
I = 2 * integrate.trapezoid(sig * np.cos(2 * np.pi * 20 * tt), tt)
Qc = -2 * integrate.trapezoid(sig * np.sin(2 * np.pi * 20 * tt), tt)
v.assert_true("P1 demodulated I and Q", abs(I - 3) < 1e-6 and abs(Qc + 4) < 1e-6)
v.check("17-06.2a", md.dmin(math.sqrt(2) * md.psk(4)[0] * np.exp(1j * math.pi / 4)))
v.check("17-06.3a", 10 / 1.05)
v.check("17-06.3b", 4 / 1.35)
v.check("17-06.4a", md.ser_psk_nn(8, un(18)))
v.assert_true("P4 Craig agrees", abs(md.ser_psk_craig(8, un(18)) / md.ser_psk_nn(8, un(18)) - 1) < 1e-3)
v.check("17-06.4b", 18 - db(3))
p64 = md.qam(64)[0]
v.check("17-06.5a", md.es(p64))
v.check("17-06.5b", md.papr_db(p64))
v.check("17-06.5c", md.ser_qam(64, un(25)))
# P6: bits per nearest-neighbour error with natural labels (4-PAM)
nat = [0b00, 0b01, 0b10, 0b11]
gry = [0b00, 0b01, 0b11, 0b10]
flips = lambda lab: np.mean([bin(lab[i] ^ lab[i + 1]).count("1") for i in range(3)])  # noqa: E731
v.check("17-06.6a", flips(nat) / flips(gry))
pg, lg = md.qam(16)
pn, ln = md.natural_qam(16)
_, bg = md.simulate(pg, lg, db(4 * un(12)), 2_000_000, rng)
_, bn = md.simulate(pn, ln, db(4 * un(12)), 2_000_000, rng)
v.assert_true("16-QAM natural labels give about 1.33x the Gray BER (simulated, 1.2-1.45)", 1.2 < bn / bg < 1.45, f"{bn / bg:.3f}")
v.check("17-06.7a", 100 * 10 ** (-25 / 20))
v.check("17-06.7b", -20 * math.log10(0.08))
v.check("17-06.7c", db(1 / (0.03 ** 2 + 1e-3)))
sg = math.radians(2)
v.check("17-06.8a", 100 * math.sqrt(2 - 2 * math.exp(-sg * sg / 2)))
v.check("17-06.8b", db(1 / (2 - 2 * math.exp(-sg * sg / 2))))
ref = md.qam(64)[0][rng.integers(0, 64, 400_000)]
ev = md.evm(md.phase_noise(ref, 2.0, rng), ref)
v.assert_true("simulated phase-noise EVM on 64-QAM matches (within 2%)", abs(ev / math.sqrt(2 - 2 * math.exp(-sg * sg / 2)) - 1) < 0.02, f"{100 * ev:.3f}%")
v.check("17-06.9a", db(math.log(1 / 2e-6)))
v.check("17-06.9b", db(math.log(1 / 2e-6)) - db(Qi(1e-6) ** 2 / 2))
v.check("17-06.10a", 0.5 * 1e6 / 1e3)
v.check("17-06.10b", 0.5 * 1e6 / 2 / 1e3)
v.check("17-06.11a", fom(md.qam(4)[0]))
e15_ = un(15)
d = lambda k: 2 * math.sin(k * math.pi / 8)  # noqa: E731
n0 = 1 / e15_
ub = sum(2 * Q(d(k) / math.sqrt(2 * n0)) for k in (1, 2, 3)) + Q(d(4) / math.sqrt(2 * n0))
v.check("17-06.12a", ub)
v.check("17-06.12b", md.ser_psk_nn(8, e15_))
v.check("17-06.12c", md.ser_psk_craig(8, e15_))
g, e = 1.01, math.radians(1)
img = (1 - 2 * g * math.cos(e) + g * g) / (1 + 2 * g * math.cos(e) + g * g)
v.check("17-06.13a", db(img))
v.check("17-06.13b", 100 * math.sqrt(img))
ref16 = md.qam(16)[0]  # every point once: E[z^2] = 0 exactly, so the image coefficient is unbiased
# simulate a quadrature modulator with the imbalance: decompose its output into wanted + image
I_, Q_ = ref16.real, ref16.imag
out = I_ + 1j * g * (Q_ * np.cos(e) + I_ * np.sin(e))  # s = I + j g (Q cos e + I sin e)
a_w = np.mean(out * np.conj(ref16)) / np.mean(np.abs(ref16) ** 2)
a_i = np.mean(out * ref16) / np.mean(np.abs(ref16) ** 2)
v.assert_true("simulated I/Q imbalance image ratio matches the formula (within 0.2 dB)", abs(db(abs(a_i) ** 2 / abs(a_w) ** 2) - db(img)) < 0.2)
thr = {}
thr[4] = optimize.brentq(lambda x: 2 * Q(math.sqrt(un(x))) - Q(math.sqrt(un(x))) ** 2 - 1e-3, 0, 45, xtol=1e-12)
for m in (16, 64, 256):
    thr[m] = optimize.brentq(lambda x, m=m: md.ser_qam(m, un(x)) - 1e-3, 0, 45, xtol=1e-12)
for tag, m in zip("abcd", (4, 16, 64, 256)):
    v.check(f"17-06.14{tag}", thr[m])
chosen = max(m for m in (4, 16, 64, 256) if thr[m] <= 18)
v.check("17-06.14e", math.log2(chosen) * 20 / 1.25)

# ------------------------------------------------------------------ lab
v.check("Lab 17-06.a", md.es(md.qam(64)[0]))
v.check("Lab 17-06.b", 100 * math.sqrt(2 - 2 * math.exp(-sg * sg / 2)))
v.check("Lab 17-06.c", db(math.log(1 / 2e-5)) - db(Qi(1e-5) ** 2 / 2))

# Problem 17-06.14 note, 15 (DVB-S2 against Shannon) and 16 (phase error)
v.check("17-06.14f", 18 + db(1.25))
for tag, esn0, eta in (("a", 6.62, 1.980636), ("d", 10.21, 2.966728)):
    shannon = db(2**eta - 1)
    v.check(f"17-06.15{tag}", esn0 - db(eta))
    v.check(f"17-06.15{chr(ord(tag) + 1)}", shannon)
    v.check(f"17-06.15{chr(ord(tag) + 2)}", esn0 - shannon)
from scipy.stats import norm as _norm  # noqa: E402
for tag, deg in (("a", 0), ("b", 10), ("c", 20)):
    v.check(f"17-06.16{tag}", _norm.sf(math.sqrt(20) * math.cos(math.radians(deg))))
_rng = np.random.default_rng(1706)
_n = 2_000_000
_g = 10 ** 0.3
_bits = _rng.integers(0, 2, _n)
_sym = (1 - 2 * _bits) * np.exp(1j * math.radians(30))
_r = _sym + (_rng.normal(size=_n) + 1j * _rng.normal(size=_n)) * math.sqrt(1 / (2 * _g))  # N0/2 per component, Eb = 1
_ber = np.mean((np.real(_r) < 0) != (_bits == 1))
_th = _norm.sf(math.sqrt(2 * _g) * math.cos(math.radians(30)))
v.assert_true("phase-error BPSK simulation matches Q(sqrt(2Eb/N0) cos theta) at 3 dB, 30 deg", abs(_ber / _th - 1) < 0.03, f"{_ber} vs {_th}")
_p = (3 + 3j) * np.exp(1j * math.radians(5))
v.check("17-06.16d", _p.real - 2)
v.check("17-06.16e", _p.imag - 2)
v.check("17-06.16f", -20 * math.log10(_p.real - 2))

sys.exit(v.finish())
