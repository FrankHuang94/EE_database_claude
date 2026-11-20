#!/usr/bin/env python3
"""Verify chapter 17-05 (matched filters and optimal detection): text, examples, problems and lab answers.

Routes:
- matched-filter SNR and its timing loss by Monte Carlo on sampled white noise, against 2E/N0;
- the one-pole optimum by numerical optimization, cross-checked by simulating the filter;
- Gram-Schmidt numerically on sampled waveforms;
- error probabilities in closed form, by inverse-Q root finding, and by Monte Carlo detection in signal space;
- the MAP threshold by scanning the error probability, and MAP/ML by simulation;
- coloured-noise and brick-wall filter ratios by numerical integration;
- pulse compression by filtering a simulated chirp.
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
LAB = ROOT / "labs" / "17-05-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import detection as dt_  # noqa: E402

CH = ROOT / "chapters" / "17-05-matched-filters-and-detection.md"
v = Verifier.from_files("17-05", CH, ROOT / "solutions" / "17-05-solutions.md", LAB / "README.md")
rng = np.random.default_rng(1705)
Q, Qi = norm.sf, norm.isf


def db(x):
    return 10 * math.log10(x)


def un(d):
    return 10 ** (d / 10)


def ebn0_for(ber):
    return db(Qi(ber) ** 2 / 2)


# ------------------------------------------------------------------ text
v.check("Txt 17-05.a", ebn0_for(1e-5))
v.check("Txt 17-05.b", ebn0_for(1e-6))
x4 = optimize.brentq(lambda x: 0.75 * Q(math.sqrt(0.8 * un(x))) - 1e-6, 5, 25, xtol=1e-12)
v.check("Txt 17-05.c", x4 - ebn0_for(1e-6))
v.check("Txt 17-05.d", db(5 / 2))
opt = optimize.minimize_scalar(lambda x: -dt_.one_pole_ratio(x), bounds=(0.1, 5), method="bounded", options={"xatol": 1e-12})
v.check("Txt 17-05.e", dt_.one_pole_ratio(opt.x))
v.check("Txt 17-05.f", db(dt_.one_pole_ratio(opt.x)))
v.check("Txt 17-05.g", -db(0.9 ** 2))
for tag, p in zip("hijk", (1e-5, 1e-6, 1e-12, 1e-13)):
    v.check(f"Txt 17-05.{tag}", Qi(p))
v.check("Txt 17-05.l", ebn0_for(1e-13))
v.check("Txt 17-05.m", db(2 * un(46.87) * 1e-3))
v.check("Txt 17-05.n", 1e15 / 100e9 / 3600)
v.check("Txt 17-05.o", db(4096))
v.check("Txt 17-05.p", -174 + db(125e3) - 20)
v.check("Txt 17-05.q", -136 - (-174 + db(125e3) - 20))
v.check("Txt 17-05.r", -20 + db(125e3 / 293))

# ------------------------------------------------------------------ Example 1 (Monte Carlo on a grid)
T, dt = 1e-6, 1e-8
s = np.ones(int(T / dt))
n0 = 2e-8
snr_mc, snr_th = dt_.mf_peak_snr_mc(s, n0, dt, 20000, rng)
v.check("Ex 17-05.1a", snr_th)
v.check("Ex 17-05.1b", db(snr_th))
v.assert_true("Monte Carlo matched-filter SNR within 3% of 2E/N0", abs(snr_mc / snr_th - 1) < 0.03, f"{snr_mc:.1f}")
v.check("Ex 17-05.1c", math.sqrt(n0 / 2 * dt_.energy(s, dt)))
y = dt_.matched_filter_output(s, s, dt)
k_peak = int(np.argmax(y))
v.assert_true("matched-filter output is a triangle peaking at E", abs(y[k_peak] - dt_.energy(s, dt)) < 1e-12)
late = y[k_peak + int(0.1 * T / dt)]
v.check("Ex 17-05.1d", db((late / y[k_peak]) ** 2))
# shape-independence: a half-sine and a chirp of equal energy give the same 2E/N0 by Monte Carlo
tt = np.arange(len(s)) * dt
hs = np.sin(np.pi * tt / T)
hs *= math.sqrt(dt_.energy(s, dt) / dt_.energy(hs, dt))
snr_hs, _ = dt_.mf_peak_snr_mc(hs, n0, dt, 20000, rng)
v.assert_true("half-sine of equal energy: same SNR (within 3%)", abs(snr_hs / snr_th - 1) < 0.03, f"{snr_hs:.1f}")

# ------------------------------------------------------------------ Example 2
v.check("Ex 17-05.2a", opt.x)
v.check("Ex 17-05.2b", dt_.one_pole_ratio(opt.x))
v.check("Ex 17-05.2c", db(dt_.one_pole_ratio(opt.x)))
v.check("Ex 17-05.2d", opt.x / (2 * math.pi))
v.check("Ex 17-05.2e", dt_.one_pole_ratio(1.0))
v.check("Ex 17-05.2f", db(dt_.one_pole_ratio(1.0)))
# simulate the one-pole filter at x = 1: noise variance N0/(4 tau) and signal 1 - e^-1
tau = T
a = math.exp(-dt / tau)
sig_out = 0.0
for _ in range(len(s)):
    sig_out = a * sig_out + (1 - a) * 1.0
h = (1 - a) * a ** np.arange(int(20 * tau / dt))
noise_var = n0 / (2 * dt) * np.sum(h ** 2)
v.assert_true("one-pole simulation ratio matches closed form (x = 1)",
              abs(sig_out ** 2 / noise_var / (2 * dt_.energy(s, dt) / n0) - dt_.one_pole_ratio(1.0)) < 0.01)

# ------------------------------------------------------------------ Example 3
n = 1000
ddt = 1 / n
s1 = np.ones(n)
s2 = np.concatenate([np.ones(n // 2), -np.ones(n // 2)])
s3 = np.concatenate([np.ones(n // 2), np.zeros(n // 2)])
B = dt_.gram_schmidt([s1, s2, s3], ddt)
C = dt_.coordinates([s1, s2, s3], B, ddt)
v.check("Ex 17-05.3a", len(B))
v.check("Ex 17-05.3b", dt_.energy(s3, ddt))
v.check("Ex 17-05.3c", float(np.linalg.norm(C[0] - C[1])))
v.check("Ex 17-05.3d", float(np.linalg.norm(C[0] - C[2])))
v.assert_true("d13 from waveforms equals d13 from vectors", abs(math.sqrt(dt_.energy(s1 - s3, ddt)) - np.linalg.norm(C[0] - C[2])) < 1e-12)

# ------------------------------------------------------------------ Example 4
e8 = un(8)
v.check("Ex 17-05.4a", dt_.ber_bpsk(e8))
v.check("Ex 17-05.4b", dt_.ber_orthogonal(e8))
v.check("Ex 17-05.4c", ebn0_for(1e-6))
v.check("Ex 17-05.4d", db(Qi(1e-6) ** 2))
eb = 1.0
n0_8 = eb / e8
ant = np.array([[math.sqrt(eb)], [-math.sqrt(eb)]])
orth = np.array([[math.sqrt(eb), 0], [0, math.sqrt(eb)]])
onoff = np.array([[0.0], [math.sqrt(2 * eb)]])
for name, pts, th in (("antipodal", ant, dt_.ber_bpsk(e8)), ("orthogonal", orth, dt_.ber_orthogonal(e8)), ("on-off", onoff, dt_.ber_orthogonal(e8))):
    sim = dt_.simulate_ser(pts, n0_8, 2_000_000, rng)
    v.assert_true(f"Monte Carlo {name} BER at 8 dB within 8%", abs(sim / th - 1) < 0.08, f"{sim:.3e} vs {th:.3e}")

# ------------------------------------------------------------------ Example 5
p1, n05 = 0.8, 0.5
sg = math.sqrt(n05 / 2)
t5 = (n05 / 4) * math.log((1 - p1) / p1)
v.check("Ex 17-05.5a", t5)
v.check("Ex 17-05.5b", Q((1 - t5) / sg))
v.check("Ex 17-05.5c", Q((1 + t5) / sg))
pmap = p1 * Q((1 - t5) / sg) + (1 - p1) * Q((1 + t5) / sg)
v.check("Ex 17-05.5d", pmap)
v.check("Ex 17-05.5e", Q(1 / sg))
ts = np.linspace(-1, 1, 200001)
pe = p1 * Q((1 - ts) / sg) + (1 - p1) * Q((1 + ts) / sg)
v.assert_true("scanning the threshold finds the MAP value", abs(ts[np.argmin(pe)] - t5) < 2e-5)
sim_map = dt_.simulate_ser(ant, n05, 1_000_000, rng, priors=[p1, 1 - p1], rule="map")
v.assert_true("Monte Carlo MAP error within 3%", abs(sim_map / pmap - 1) < 0.03, f"{sim_map:.4f}")

# ------------------------------------------------------------------ Example 6
es = 2 * un(10)
v.check("Ex 17-05.6a", dt_.ser_pam(4, es))
v.check("Ex 17-05.6b", dt_.ser_pam(4, es) / 2)
v.check("Ex 17-05.6c", dt_.ber_bpsk(un(10)))
v.check("Ex 17-05.6d", x4)
v.check("Ex 17-05.6e", x4 - ebn0_for(1e-6))
orth4 = math.sqrt(es) * np.eye(4)
v.check("Ex 17-05.6f", dt_.union_bound(orth4, 1.0))
pam4 = np.array([[-3.0], [-1.0], [1.0], [3.0]])
n0p = np.mean(pam4 ** 2) / un(9)
sim4 = dt_.simulate_ser(pam4, n0p, 2_000_000, rng)
v.assert_true("Monte Carlo PAM4 SER at Es/N0 = 9 dB within 5%", abs(sim4 / dt_.ser_pam(4, un(9)) - 1) < 0.05)

# ------------------------------------------------------------------ problems
v.check("17-05.1a", 2 ** 2 * 3e-6 / 3)
v.check("17-05.1b", 2 * (2 ** 2 * 3e-6 / 3) / 1e-7)
v.check("17-05.1c", db(2 * (2 ** 2 * 3e-6 / 3) / 1e-7))
ramp = 2 * np.arange(3000) / 3000
v.assert_true("ramp energy by integration", abs(dt_.energy(ramp, 1e-9) - 4e-6) < 1e-8)
for tag, x in zip("abcd", (0, 4, 7, 9.6)):
    v.check(f"17-05.2{tag}", dt_.ber_bpsk(un(x)))
for tag, p in zip("abc", (1e-3, 1e-9, 1e-12)):
    v.check(f"17-05.3{tag}", ebn0_for(p))
v.check("17-05.4a", db(0.75 ** 2))
v.check("17-05.4b", 0.75 - 0.25)
s4a = np.concatenate([np.ones(n // 2), np.zeros(n // 2)])
s4b = np.concatenate([np.zeros(n // 2), np.ones(n // 2)])
sigs = [s1, s4a, s4b, s4a - s4b]
B5 = dt_.gram_schmidt(sigs, ddt)
C5 = dt_.coordinates(sigs, B5, ddt)
v.check("17-05.5a", len(B5))
v.check("17-05.5b", float(np.linalg.norm(C5[1] - C5[2])))
v.check("17-05.5c", float(np.linalg.norm(C5[0] - C5[3])))
q = Q(math.sqrt(10))
v.check("17-05.6a", 2 * q - q * q)
qpsk = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]], dtype=float)
n06 = 2.0 / 10  # Es = 2 a^2 = 2 with a = 1, Es/N0 = 10
v.check("17-05.6b", dt_.union_bound(qpsk, n06))
v.check("17-05.6c", dt_.nearest_neighbour(qpsk, n06))
sim6 = dt_.simulate_ser(qpsk, n06, 4_000_000, rng)
v.assert_true("Monte Carlo four-point SER within 6%", abs(sim6 / (2 * q - q * q) - 1) < 0.06, f"{sim6:.3e}")
t7 = 0.25 * math.log(0.4 / 0.6)
s7 = math.sqrt(0.5)
v.check("17-05.7a", t7)
v.check("17-05.7b", 0.6 * Q((1 - t7) / s7) + 0.4 * Q((1 + t7) / s7))
v.check("17-05.7c", Q(1 / s7))
for tag, m in zip("abc", (2, 4, 8)):
    v.check(f"17-05.8{tag}", optimize.brentq(lambda x: dt_.ser_pam(m, un(x)) - 1e-5, 0, 40, xtol=1e-12))
v.check("17-05.9a", dt_.one_pole_ratio(2.0))
v.check("17-05.9b", db(dt_.one_pole_ratio(2.0)))
g = lambda x: 1 + 9 / (1 + x * x)  # noqa: E731
# write g = 1 + 9/(1 + x^2) and 1/g = 1 - 9/(10 + x^2) so that only fast-decaying integrands remain
# (the sinc^2 tails alone converge too slowly for a truncated quadrature: int sinc^2 = 1 exactly)
xi_w, _ = integrate.quad(lambda x: np.sinc(x) ** 2 * 9 / (1 + x * x), -2000, 2000, limit=20000, points=[0])
xi_o, _ = integrate.quad(lambda x: np.sinc(x) ** 2 * 9 / (10 + x * x), -2000, 2000, limit=20000, points=[0])
wh, op = 1 + xi_w, 1 - xi_o
v.assert_true("decomposition of 1/g", abs(1 / g(0.7) - (1 - 9 / (10 + 0.49))) < 1e-12)
v.check("17-05.10a", 1 / wh)
v.check("17-05.10b", db(1 / wh))
v.check("17-05.10c", op)
v.check("17-05.10d", db(op))
v.check("17-05.10e", db(op * wh))
al = 0.35


def hrc(f):
    f = abs(f)
    lo, hi = (1 - al) / 2, (1 + al) / 2
    if f <= lo:
        return 1.0
    if f <= hi:
        return 0.5 * (1 + math.cos(math.pi / al * (f - lo)))
    return 0.0


num, _ = integrate.quad(lambda f: math.sqrt(hrc(f)), -(1 + al) / 2, (1 + al) / 2, points=[-(1 - al) / 2, (1 - al) / 2], limit=200)
den, _ = integrate.quad(hrc, -(1 + al) / 2, (1 + al) / 2, points=[-(1 - al) / 2, (1 - al) / 2], limit=200)
v.check("17-05.11a", num ** 2 / (den * (1 + al)))
v.check("17-05.11b", db(num ** 2 / (den * (1 + al))))
eb6 = un(6)
for tag, m in zip("abc", (2, 16, 64)):
    v.check(f"17-05.12{tag}", (m - 1) * Q(math.sqrt(math.log2(m) * eb6)))
v.check("17-05.12d", 64 / 6)
v.check("17-05.13a", 20e-6 * 50e6)
v.check("17-05.13b", db(20e-6 * 50e6))
v.check("17-05.13c", 299_792_458 / (2 * 50e6))
v.check("17-05.13d", 1 / 50e6 * 1e9)
# simulated pulse compression: the -4 dB (amplitude 0.637) main-lobe width is about 1/B
fs = 400e6
ref = dt_.chirp(20e-6, 50e6, fs)
comp = dt_.compress(ref, ref)
w = dt_.mainlobe_width(comp, fs, level=2 / math.pi)
v.assert_true("compressed main lobe about 1/B wide (within 15%)", abs(w * 50e6 - 1) < 0.15, f"{w * 1e9:.1f} ns")
v.assert_true("compressed peak equals the chirp's energy (gain TB in power over one sample)",
              abs(np.abs(comp).max() / len(ref) - 1) < 1e-9)
snr14 = 2 * un(16.87)
v.check("17-05.14a", db(snr14))
v.check("17-05.14b", Q(math.sqrt(snr14) / 2))
v.check("17-05.14c", Q(math.sqrt(snr14) / 2))
v.check("17-05.14d", 1023 * 2 * 20)
v.check("17-05.14e", 1023 * 2 * 20 * Q(math.sqrt(snr14) / 2))

# ------------------------------------------------------------------ lab
v.check("Lab 17-05.a", 2 * dt_.energy(s, dt) / n0)
v.check("Lab 17-05.b", opt.x)
v.check("Lab 17-05.c", 10e-6 * 10e6)

# ------------------------------------------------------------------ concept checks
v.assert_true("CC3 orthogonal needs 3.01 dB more", abs(db(Qi(1e-6) ** 2) - ebn0_for(1e-6) - db(2)) < 1e-12)

sys.exit(v.finish())
