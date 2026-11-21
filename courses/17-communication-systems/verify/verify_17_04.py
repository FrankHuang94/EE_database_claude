#!/usr/bin/env python3
"""Verify chapter 17-04 (baseband digital transmission): text, examples, problems and lab answers.

Routes:
- level statistics by enumerating the levels; coding overheads by arithmetic;
- line-code spectra in closed form, by numerical integration, and by Welch estimates of simulated waveforms;
- the RC channel's cursors by simulating the filter exactly (zero-order hold) and by the closed form;
  eye openings by enumerating every symbol pattern;
- the Nyquist criterion by folding spectra numerically and by sampling the pulses;
- raised-cosine ISI under timing error by summing pulse samples; the RRC cascade by numerical convolution;
- the ZF equalizer by solving the system and by least squares; DFE and FFE error rates by simulation;
- statistical-eye BERs by pattern enumeration, checked against Monte Carlo.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, signal
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "17-04-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import baseband as bb  # noqa: E402

CH = ROOT / "chapters" / "17-04-baseband-digital-transmission.md"
v = Verifier.from_files("17-04", CH, ROOT / "solutions" / "17-04-solutions.md", LAB / "README.md")
rng = np.random.default_rng(1704)


def db20(x):
    return 20 * math.log10(x)


def db10(x):
    return 10 * math.log10(x)


K = np.arange(-200, 201)
K = K[K != 0]


def isi_sum(fun, eps, k=K):
    return float(np.sum(np.abs(fun(k + eps))))


# ------------------------------------------------------------------ text
v.check("Txt 17-04.a", bb.mean_energy(4))
v.check("Txt 17-04.b", bb.mean_energy(8))
v.check("Txt 17-04.c", db20(1 / 3))
v.check("Txt 17-04.d", db20(math.sqrt(1 / bb.mean_energy(4))))
v.check("Txt 17-04.e", 100 * 8 / 10)
v.check("Txt 17-04.f", 100 * 2 / 64)
v.check("Txt 17-04.g", 100 * 2 / 128)
v.check("Txt 17-04.h", 2 * math.pi / math.log(2))
v.check("Txt 17-04.i", 2 * math.pi / math.log(4))
v.check("Txt 17-04.j", isi_sum(np.sinc, 0.1))
v.check("Txt 17-04.k", isi_sum(lambda t: bb.raised_cosine(t, 0.22), 0.1))
v.check("Txt 17-04.l", isi_sum(lambda t: bb.raised_cosine(t, 0.5), 0.1))
v.check("Txt 17-04.m", 10 * math.log10((1 + 2e6 ** 2) / (1 + 1e6 ** 2)))  # |H|^2 of a one-pole, an octave far above the corner
worst = 0.0
for xx in np.linspace(0.01, 0.49, 25):
    nrz = 1 - 2 * xx
    hk4 = bb.rc_cursors(xx * xx, 200)
    pam4 = (hk4[0] - 3 * (np.sum(hk4) - hk4[0])) / 3
    worst = max(worst, abs(pam4 - nrz * (1 + 2 * xx) / 3))
v.assert_true("one-pole: PAM4 worst eye is (1 + 2r)/3 of NRZ, never larger", worst < 1e-9, f"{worst}")
v.assert_true("sum of (2i-1)^2 identity for M = 2..16", all(abs(bb.mean_energy(m) - (m * m - 1) / 3) < 1e-12 for m in (2, 4, 8, 16)))

# ------------------------------------------------------------------ Example 1
v.check("Ex 17-04.1a", 112 / 2)
v.check("Ex 17-04.1b", 112 / 2)
v.check("Ex 17-04.1c", 56 / 2)
v.check("Ex 17-04.1d", db20(1 / 3))
v.check("Ex 17-04.1e", db10(np.mean((bb.pam_levels(4) / 3) ** 2)))
bits = rng.integers(0, 2, 4000)
lv = bb.gray_map(bits, 4)
_words = [(b1, b0) for b1 in (0, 1) for b0 in (0, 1)]
_lab = {float(bb.gray_map(np.array(w), 4)[0]): w for w in _words}
_adj = [sum(x != y for x, y in zip(_lab[lo], _lab[hi])) for lo, hi in ((-3.0, -1.0), (-1.0, 1.0), (1.0, 3.0))]
v.assert_true("Gray map: adjacent levels differ in one bit", set(np.unique(lv)) == {-3.0, -1.0, 1.0, 3.0} and _adj == [1, 1, 1], f"{_adj}")

# ------------------------------------------------------------------ Example 2 (closed form, integration, simulation)
nrz_frac, _ = integrate.quad(lambda x: np.sinc(x) ** 2, -1, 1, points=[0])
v.check("Ex 17-04.2a", 100 * nrz_frac)
v.check("Ex 17-04.2b", float(bb.manchester_psd(0.0)))
v.check("Ex 17-04.2c", optimize.minimize_scalar(lambda x: float(bb.manchester_psd(x)), bounds=(1.5, 2.5), method="bounded").x)
v.assert_true("Manchester PSD positive on (0.01, 1.99): first null at 2/T", min(float(bb.manchester_psd(x)) for x in np.linspace(0.01, 1.99, 400)) > 0)
seg = lambda a, b: integrate.quad(bb.manchester_psd, a, b, limit=400)[0]  # noqa: E731
tot = 2 * sum(seg(2 * k, 2 * k + 2) for k in range(0, 4000))
v.assert_true("Manchester total power is A^2", abs(tot - 1) < 2e-4, f"{tot}")
v.check("Ex 17-04.2d", 100 * 2 * seg(0, 1))
v.check("Ex 17-04.2e", 100 * 2 * seg(0, 2))
pk = optimize.minimize_scalar(lambda x: -bb.manchester_psd(x), bounds=(0.3, 1.5), method="bounded", options={"xatol": 1e-10})
v.check("Ex 17-04.2f", pk.x)
v.check("Ex 17-04.2g", float(bb.manchester_psd(pk.x)))
sps = 16
x = bb.waveform(rng.choice([-1.0, 1.0], 1 << 17), sps, "manchester")
f, G = signal.welch(x, fs=sps, nperseg=1024, detrend=False)
sel = (f > 0.2) & (f < 1.8)
v.assert_true("Welch estimate of Manchester matches the closed form (rms dev < 5%)",
              np.sqrt(np.mean((G[sel] / 2 / bb.manchester_psd(f[sel]) - 1) ** 2)) < 0.05)

# ------------------------------------------------------------------ Example 3 (closed form and simulated RC filter)
tau = 1 / (2 * math.pi * 5e9)
T = 1 / 25e9
r = math.exp(-T / tau)
v.check("Ex 17-04.3a", tau * 1e12)
v.check("Ex 17-04.3b", r)
ovs = 400
pulse = np.zeros(ovs * 12)
pulse[:ovs] = 1.0
resp = bb.rc_channel(pulse, tau / (T / ovs))
h_sim = resp[ovs - 1::ovs][:10]
v.check("Ex 17-04.3c", h_sim[0])
v.check("Ex 17-04.3d", h_sim[1])
v.assert_true("simulated cursors match (1-r) r^k", np.max(np.abs(h_sim - bb.rc_cursors(r, 9))) < 1e-12)
h_long = bb.rc_cursors(r, 60)
v.check("Ex 17-04.3e", bb.worst_case_eye(h_long, 0))
v.assert_true("worst-case pattern (run then flip) gives 1 - 2r",
              abs(bb.pattern_samples(h_long[:12], 0).min() - (1 - 2 * r)) < 1e-6)
v.check("Ex 17-04.3f", 1 / (tau * math.log(2)) / 1e9)
v.check("Ex 17-04.3g", 1 / (tau * math.log(4)) / 1e9)

# ------------------------------------------------------------------ Example 4
v.check("Ex 17-04.4a", 3.84 * 1.22)
v.check("Ex 17-04.4b", 3.84 * 1.22 / 2)
v.check("Ex 17-04.4c", isi_sum(np.sinc, 0.1))
v.check("Ex 17-04.4d", isi_sum(lambda t: bb.raised_cosine(t, 0.22), 0.1))
v.check("Ex 17-04.4e", isi_sum(lambda t: bb.raised_cosine(t, 0.5), 0.1))
v.check("Ex 17-04.4f", float(np.sinc(0.1)))
v.check("Ex 17-04.4g", float(bb.raised_cosine(np.array([0.1]), 0.22)[0]))
v.check("Ex 17-04.4h", float(bb.raised_cosine(np.array([0.1]), 0.5)[0]))
K2 = np.arange(-2000, 2001)
K2 = K2[K2 != 0]
v.assert_true("sinc ISI keeps growing (+-2000 > +-200 by > 0.3)", isi_sum(np.sinc, 0.1, K2) - isi_sum(np.sinc, 0.1) > 0.3)
v.assert_true("RC ISI converged (+-2000 vs +-200 < 1e-3)",
              abs(isi_sum(lambda t: bb.raised_cosine(t, 0.22), 0.1, K2) - isi_sum(lambda t: bb.raised_cosine(t, 0.22), 0.1)) < 1e-3)
for a in (0.22, 0.5):
    ff = np.linspace(-0.5, 0.5, 2001)
    v.assert_true(f"RC alpha={a} folded spectrum is flat", np.max(np.abs(bb.folded_spectrum(lambda q: bb.raised_cosine_spectrum(q, a), ff) - 1)) < 1e-12)
    v.assert_true(f"RC alpha={a} zero crossings at nonzero integers", np.max(np.abs(bb.raised_cosine(np.arange(1, 30).astype(float), a))) < 1e-12)
# RRC * RRC = RC (numerical convolution)
dt = 1 / 64
tt = np.arange(-40, 40 + dt / 2, dt)
rr = bb.root_raised_cosine(tt, 0.35)
casc = np.convolve(rr, rr) * dt
tc = np.arange(len(casc)) * dt - 80
idx = [np.argmin(np.abs(tc - k)) for k in range(-6, 7)]
v.assert_true("RRC cascade has zero ISI (within truncation)", np.max(np.abs(casc[idx] - (np.arange(-6, 7) == 0))) < 2e-3)
rr_self = bb.root_raised_cosine(np.arange(1, 6).astype(float), 0.35)
v.assert_true("RRC alone does not have zero ISI", np.max(np.abs(rr_self)) > 0.01)

# ------------------------------------------------------------------ Example 5
h5 = [0.1, 1.0, 0.4, 0.15]  # h_{-1}..h_2, main index 1
c = bb.zf_equalizer(h5, 1, 3)
v.check("Ex 17-04.5a", c[0])
v.check("Ex 17-04.5b", c[1])
v.check("Ex 17-04.5c", c[2])
q = bb.apply_ffe(h5, c)  # lags -2..3
main_q = 2
v.assert_true("ZF forces q_-1 = q_1 = 0 and q_0 = 1", abs(q[1]) < 1e-12 and abs(q[3]) < 1e-12 and abs(q[2] - 1) < 1e-12)
v.check("Ex 17-04.5d", float(np.sum(np.abs(q)) - abs(q[main_q])))
v.check("Ex 17-04.5e", bb.worst_case_eye(h5, 1))
v.check("Ex 17-04.5f", bb.worst_case_eye(q, main_q))
v.check("Ex 17-04.5g", float(np.sum(c ** 2)))
v.check("Ex 17-04.5h", db10(float(np.sum(c ** 2))))
v.assert_true("printed q values", np.allclose(q, [-0.0109, 0, 1, 0, -0.0043, -0.0627], atol=5e-5))
# least-squares cross-check: same taps from an overdetermined system restricted to the forced lags
A = np.array([[([0.0, 0.0] + h5 + [0.0, 0.0])[2 + 1 + i - j] for j in (-1, 0, 1)] for i in (-1, 0, 1)])
v.assert_true("ZF taps by an independent linear solve", np.allclose(np.linalg.lstsq(A, [0, 1, 0], rcond=None)[0], c))

# ------------------------------------------------------------------ Example 6
v.check("Ex 17-04.6a", 0.8 * 56)
v.check("Ex 17-04.6b", 0.8 * 28)
v.check("Ex 17-04.6c", 0.8 * 56 - 0.8 * 28 + db20(1 / 3))
b6 = 20 / math.sqrt(28)
v.check("Ex 17-04.6d", b6 * math.sqrt(56))
v.check("Ex 17-04.6e", b6 * (math.sqrt(56) - math.sqrt(28)))
v.check("Ex 17-04.6f", -db20(1 / 3) - b6 * (math.sqrt(56) - math.sqrt(28)))

# ------------------------------------------------------------------ Problems 1-3
v.check("17-04.1a", 400 / 4)
v.check("17-04.1b", 100 / 2)
v.check("17-04.1c", 50 / 2)
v.check("17-04.1d", 64 / 2)
v.check("17-04.1e", 32 / 2)
v.check("17-04.1f", 3 / 2)
v.check("17-04.1g", 1.5 / math.log2(3))
v.check("17-04.2a", 10.3125 * 64 / 66)
v.check("17-04.2b", 2.5 * 8 / 10)
v.check("17-04.2c", 8 * 128 / 130)
v.check("17-04.2d", 16 * 8 * 128 / 130 / 8)
for tag, m in zip("abc", (2, 4, 8)):
    v.check(f"17-04.3{tag}", bb.mean_energy(m))
v.check("17-04.3d", db20(1 / 3))
v.check("17-04.3e", db20(1 / 7))
v.check("17-04.3f", db20(math.sqrt(1 / bb.mean_energy(4))))
v.check("17-04.3g", db20(math.sqrt(1 / bb.mean_energy(8))))

# ------------------------------------------------------------------ Problem 4 (transform by numerical integration)
fq = 1.0
re, _ = integrate.quad(lambda t: (1 if t < 0.5 else -1) * math.cos(2 * math.pi * fq * t), 0, 1, points=[0.5])
im, _ = integrate.quad(lambda t: -(1 if t < 0.5 else -1) * math.sin(2 * math.pi * fq * t), 0, 1, points=[0.5])
v.check("17-04.4a", re * re + im * im)
v.assert_true("P4 equals the closed form", abs(re * re + im * im - bb.manchester_psd(1.0)) < 1e-10)

# ------------------------------------------------------------------ Problem 5 (fold numerically, sample the pulses)
specs = {
    "a": lambda q: np.clip(1 - np.abs(q), 0, None),
    "b": lambda q: (np.abs(q) < 0.6).astype(float),
    "c": lambda q: (np.abs(q) < 0.5).astype(float),
    "d": lambda q: np.clip((0.7 - np.abs(q)) / 0.4, 0, 1),
}
ff = np.linspace(-0.49, 0.49, 999)
flat = {k: np.max(np.abs(bb.folded_spectrum(fn, ff) - 1)) < 1e-9 for k, fn in specs.items()}
v.assert_true("P5 folding: a, c, d pass and b fails", flat == {"a": True, "b": False, "c": True, "d": True})
fgrid = np.linspace(-1, 1, 200001)
dfq = fgrid[1] - fgrid[0]
h_b = lambda t: np.sum(specs["b"](fgrid) * np.cos(2 * np.pi * fgrid * t)) * dfq  # noqa: E731
v.check("17-04.5a", h_b(1.0) / h_b(0.0))
h_d = lambda t: np.sum(specs["d"](fgrid) * np.cos(2 * np.pi * fgrid * t)) * dfq  # noqa: E731
v.assert_true("P5 (d) pulse samples vanish", max(abs(h_d(k) / h_d(0)) for k in (1, 2, 3)) < 1e-4)

# ------------------------------------------------------------------ Problems 6-10
v.check("17-04.6a", 6 / 1.25)
v.check("17-04.6b", 6 * 6 / 1.25)
v.check("17-04.6c", 6 / 1.1)
v.check("17-04.6d", 6 * 6 / 1.1)
v.check("17-04.7a", norm.sf(0.6 / 0.12))
v.check("17-04.7b", norm.sf(1 / 0.12))
tau8 = 1 / (2 * math.pi * 10e9)
v.check("17-04.8a", 1 / (tau8 * math.log(4)) / 1e9)
v.check("17-04.8b", bb.worst_case_eye(bb.rc_cursors(math.exp(-(1 / 56e9) / tau8), 80), 0))
h0r = float(bb.raised_cosine(np.array([0.25]), 0.35)[0])
isr = isi_sum(lambda t: bb.raised_cosine(t, 0.35), 0.25)
v.check("17-04.9a", h0r)
v.check("17-04.9b", isr)
v.check("17-04.9c", h0r - isr)
v.check("17-04.9d", float(np.sinc(0.25)))
v.check("17-04.9e", isi_sum(np.sinc, 0.25))
v.check("17-04.9f", float(np.sinc(0.25)) - isi_sum(np.sinc, 0.25))
v.check("17-04.10a", bb.worst_case_eye([0.1, 1.0, 0.0, 0.15], 1))
v.check("17-04.10b", bb.worst_case_eye([0.1, 1.0, 0.0, 0.0], 1))
# DFE/FFE by simulation at a noise level where the differences show
sig = 0.25
ber_raw = bb.simulate_binary(np.array(h5), 1, sig, 400_000, rng)
ber_dfe = bb.simulate_binary(np.array(h5), 1, sig, 2_000_000, rng, dfe=[0.4, 0.15])
ber_ffe = bb.simulate_binary(np.array(h5), 1, sig, 400_000, rng, ffe=c)
ber_dfe_th = bb.statistical_ber([0.1, 1.0], 1, sig)
v.assert_true("two-tap DFE BER near its statistical eye (error propagation adds < 60%)", 0.8 < ber_dfe / ber_dfe_th < 1.6, f"{ber_dfe:.2e} vs {ber_dfe_th:.2e}")
v.assert_true("equalizers beat no equalization", ber_dfe < ber_raw and ber_ffe < ber_raw, f"raw {ber_raw:.2e}")

# ------------------------------------------------------------------ Problem 11
v.check("17-04.11a", float(bb.raised_cosine_spectrum(0.4, 0.5)))
v.check("17-04.11b", float(bb.raised_cosine_spectrum(-0.6, 0.5)))

# ------------------------------------------------------------------ Problem 12 (duobinary)
dbn = lambda t: np.sinc(t) + np.sinc(t - 1)  # noqa: E731
v.assert_true("duobinary samples 1, 1, 0...", np.allclose(dbn(np.arange(-3, 6).astype(float)), [0, 0, 0, 1, 1, 0, 0, 0, 0], atol=1e-12))
a = rng.choice([-1.0, 1.0], 200_000)
yv = a[1:] + a[:-1]
levels, counts = np.unique(yv, return_counts=True)
v.check("17-04.12a", len(levels))
_y = [p + q for p in (-1, 1) for q in (-1, 1)]
v.check("17-04.12b", _y.count(0) / 4)
v.check("17-04.12c", _y.count(2) / 4)
v.assert_true("duobinary level frequencies 1/4, 1/2, 1/4 (simulated)", np.allclose(counts / counts.sum(), [0.25, 0.5, 0.25], atol=0.005))
v.check("17-04.12d", db20(2 / 4))
# precoding removes error propagation: each level maps to one bit
d = rng.integers(0, 2, 1000)
bpre = np.zeros(1001, dtype=int)
for i in range(1000):
    bpre[i + 1] = d[i] ^ bpre[i]
ap = 2 * bpre - 1
yp = ap[1:] + ap[:-1]
v.assert_true("precoded duobinary decodes symbol by symbol", np.all((np.abs(yp) == 0) == (d == 1)))

# ------------------------------------------------------------------ Problem 13
pen = -db20(1 / 3)
v.check("17-04.13a", pen / 28)
bth = pen / (math.sqrt(56) - math.sqrt(28))
v.check("17-04.13b", bth)
v.check("17-04.13c", bth * math.sqrt(28))

# ------------------------------------------------------------------ Problem 14 (enumeration and Monte Carlo)
h14 = [0.1, 1.0, 0.3]
vals = np.sort(bb.pattern_samples(h14, 1))
v.check("17-04.14a", vals[0])
v.assert_true("P14 sample values 0.6, 0.8, 1.2, 1.4", np.allclose(vals, [0.6, 0.8, 1.2, 1.4]))
ber14 = bb.statistical_ber(h14, 1, 0.1)
v.check("17-04.14b", ber14)
v.check("17-04.14c", norm.sf(6.0))
v.check("17-04.14d", norm.sf(10.0))
ber_mc = bb.simulate_binary(np.array([0.1, 1.0, 0.3]), 1, 0.2, 1_000_000, rng)
v.assert_true("statistical eye matches Monte Carlo at sigma = 0.2 (within 10%)",
              abs(ber_mc / bb.statistical_ber(h14, 1, 0.2) - 1) < 0.1, f"{ber_mc:.3e}")

# ------------------------------------------------------------------ lab
v.check("Lab 17-04.a", bb.worst_case_eye(bb.rc_cursors(math.exp(-(1 / 10e9) / tau), 80), 0))
v.check("Lab 17-04.b", bb.worst_case_eye(bb.rc_cursors(math.exp(-(1 / 45e9) / tau), 80), 0))
v.check("Lab 17-04.c", ber_dfe_th)

# ------------------------------------------------------------------ concept checks
v.assert_true("CC3 rates 20 and 16 Msymbol/s", 2 * 10 == 20 and abs(2 * 10 / 1.25 - 16) < 1e-12)
v.assert_true("CC5 eye 0.2", abs(bb.worst_case_eye([1.0, 0.5, 0.3], 0) - 0.2) < 1e-12)

# Problem 17-04.15: ZF design, checked against the lab's general solver and by convolution
_h = [0.15, 1.0, 0.5, 0.2]
_c = bb.zf_equalizer(_h, 1, 3)
_q = np.convolve(_h, _c)  # indices k = -2..3
v.check("17-04.15a", _c[1])
v.check("17-04.15b", _c[0])
v.check("17-04.15c", _c[2])
v.assert_true("ZF forces q(-1) = q(1) = 0 and q(0) = 1", np.allclose(_q[1:4], [0, 1, 0], atol=1e-12))
_res = np.sum(np.abs(_q)) - 1
v.check("17-04.15d", _res)
v.check("17-04.15e", _h[1] - (abs(_h[0]) + abs(_h[2]) + abs(_h[3])))
v.check("17-04.15f", 1 - _res)
v.check("17-04.15g", float(np.sum(_c ** 2)))
v.check("17-04.15h", db10(float(np.sum(_c ** 2))))

sys.exit(v.finish())
