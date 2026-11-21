#!/usr/bin/env python3
"""Verify chapter 17-10 (OFDM): text, examples, problems and lab answers.

Routes:
- orthogonality by numerical integration of products of subcarriers;
- NR timing from the TS 38.211 definitions written out here (Tc, kappa, N_u, N_CP), summed over whole
  subframes, and guard bands against TS 38.101-1 Table 5.3.3-1 values (R-286, R-287);
- one-tap equalization by running the lab's modulator/demodulator through a multipath channel and
  checking Y_k = H_k X_k exactly when the prefix is long enough;
- CFO ICI from the exact Dirichlet-kernel expression, the small-offset form, and simulation;
- Doppler ICI by simulating a time-varying Jakes channel inside one OFDM symbol;
- PAPR by Monte Carlo against the Nyquist-sample approximation, and DFT-spread OFDM's identity at full band.
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
LAB = ROOT / "labs" / "17-10-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import ofdm as of  # noqa: E402

CH = ROOT / "chapters" / "17-10-ofdm.md"
v = Verifier.from_files("17-10", CH, ROOT / "solutions" / "17-10-solutions.md", LAB / "README.md")
rng = np.random.default_rng(1710)
c = 299_792_458.0
Q = norm.sf
Ts = 1 / (15e3 * 2048)  # kappa * Tc


def db(x):
    return 10 * math.log10(x)


def corr_window(dk, frac):
    """|int_0^{frac T} e^{j 2 pi dk t/T} dt| / (frac T) by quadrature (T = 1)."""
    re, _ = integrate.quad(lambda t: math.cos(2 * math.pi * dk * t), 0, frac, limit=200)
    im, _ = integrate.quad(lambda t: math.sin(2 * math.pi * dk * t), 0, frac, limit=200)
    return math.hypot(re, im) / frac


def ici_exact(eps, n):
    return 1 - (math.sin(math.pi * eps) / (n * math.sin(math.pi * eps / n))) ** 2


def papr_level(p, n):
    return db(-math.log(1 - (1 - p) ** (1 / n)))


# ------------------------------------------------------------------ text
v.check("Txt 17-10.a", db((math.pi * 0.01) ** 2 / 3))
v.check("Txt 17-10.b", 144 * Ts * 1e6)
v.check("Txt 17-10.c", 144 * Ts / 8 * 1e6)
v.assert_true("orthogonality: subcarriers 1..3 apart integrate to zero over T", all(corr_window(dk, 1.0) < 1e-12 for dk in (1, 2, 3)))
v.assert_true("each subcarrier's sinc spectrum is zero at every other subcarrier", all(abs(np.sinc(k)) < 1e-15 for k in (1, 2, 3, 7)))
v.assert_true("NR CP ratio 144/2048 is 6.57% of the symbol at every mu", all(abs(of.nr_symbol(mu)[1] / sum(of.nr_symbol(mu)) - 144 / 2192) < 1e-12 for mu in range(7)))
v.assert_true("CP energy penalty 10 log10(2192/2048) = 0.30 dB", abs(db(2192 / 2048) - 0.30) < 0.005)
v.assert_true("ICI at 10% offset -14.8 dB; SIR at 5% offset about 20.8 dB", abs(db((math.pi * 0.1) ** 2 / 3) + 14.8) < 0.05 and abs(db(3 / (math.pi * 0.05) ** 2) - 20.8) < 0.05)
v.assert_true("ICI for 120 vs 15 kHz spacing differs by 64x (square of 8)", abs(of.ici_doppler(1000, 15e3) / of.ici_doppler(1000, 120e3) - 64) < 1e-9)
v.assert_true("unitary DFT keeps noise variance per subcarrier", abs(np.var(np.fft.fft(rng.standard_normal((400, 1024)) + 1j * rng.standard_normal((400, 1024)), axis=1) / math.sqrt(1024)) - 2) < 0.02)

# one-tap equalization: exact Y = H X with a sufficient prefix, noise-free
n, ncp = 64, 8
h = np.array([0.8, 0.4 - 0.3j, 0.2, 0.1j, -0.05, 0.02])
X = of.qam(16)[rng.integers(0, 16, (20, n))]
y = np.convolve(of.ofdm_mod(X, ncp), h)[: 20 * (n + ncp)]
Y = of.ofdm_demod(y, n, ncp, 20)
v.assert_true("with CP >= channel memory, every subcarrier obeys Y_k = H_k X_k exactly", np.allclose(Y, of.channel_response(h, n) * X, atol=1e-12))
mm = of.equalize(Y, of.channel_response(h, n), 20.0)
v.assert_true("MMSE output is a positive real multiple of the ZF output on every subcarrier", np.allclose(np.angle(mm / (Y / of.channel_response(h, n))), 0, atol=1e-12))

# ------------------------------------------------------------------ examples
v.check("Ex 17-10.1a", 2048 * Ts / 2 * 1e6)
v.check("Ex 17-10.1b", 144 * Ts / 2 * 1e6)
v.check("Ex 17-10.1c", 2192 * Ts / 2 * 1e6)
v.check("Ex 17-10.1d", 100 * 144 / 2192)
sub = sum((2048 + 144) * Ts / 2 + (16 * Ts if l in (0, 14) else 0) for l in range(28))
v.check("Ex 17-10.1e", sub / 2 * 1e6)
v.check("Ex 17-10.1f", c * 144 * Ts / 2)
v.assert_true("Example 1: a 1 ms subframe holds exactly 2 slots at mu = 1 (and 2^mu at every mu); lab agrees", abs(sub - 1e-3) < 1e-15 and all(abs(of.nr_slot_duration(mu) * 2**mu - 1e-3) < 1e-15 for mu in range(7)) and abs(16 * Ts * 1e6 - 0.521) < 0.0005)
v.check("Ex 17-10.2a", 273 * 12)
v.check("Ex 17-10.2b", 273 * 12 * 30e3 / 1e6)
v.check("Ex 17-10.2c", (100e3 - 273 * 12 * 30) / 2 - 15)
v.check("Ex 17-10.2d", 4096 * 30e3 / 1e6)
v.check("Ex 17-10.2e", 4096 / 3276)
v.check("Ex 17-10.2f", 100 * 106 * 12 * 15 / 20e3)
v.check("Ex 17-10.2g", (20e3 - 106 * 12 * 15) / 2 - 7.5)
v.assert_true("Example 2: guard bands match TS 38.101-1 Table 5.3.3-1 (845, 452.5; also 50 MHz at 15 kHz: 692.5)", of.nr_guardband_khz(100, 273, 30) == 845 and of.nr_guardband_khz(20, 106, 15) == 452.5 and of.nr_guardband_khz(50, 270, 15) == 692.5)
H8 = np.array([1 + 0.5 * np.exp(-2j * np.pi * k / 8) for k in range(8)])
v.check("Ex 17-10.3a", abs(H8[0]))
v.check("Ex 17-10.3b", abs(H8[2]))
v.check("Ex 17-10.3c", abs(H8[4]))
v.check("Ex 17-10.3d", 20 * math.log10(abs(H8[4])))
v.assert_true("Example 3: |H| = 1.399 and 0.737 at k = 1, 3; 1/H_2 = 0.8 + 0.4j; mean |H|^2 = 1.25 (Parseval); lab FFT agrees", abs(abs(H8[1]) - 1.399) < 5e-4 and abs(abs(H8[3]) - 0.737) < 5e-4 and abs(1 / H8[2] - (0.8 + 0.4j)) < 1e-12 and abs(np.mean(abs(H8) ** 2) - 1.25) < 1e-12 and np.allclose(of.channel_response([1, 0.5], 8), H8))
eps01, eps1 = 350 / 30e3, 3500 / 30e3
v.check("Ex 17-10.4a", db((math.pi * eps01) ** 2 / 3))
v.check("Ex 17-10.4b", db((math.pi * eps1) ** 2 / 3))
fd35 = (120 / 3.6) * 3.5e9 / c
fd28 = (120 / 3.6) * 28e9 / c
v.check("Ex 17-10.4c", db((math.pi * fd35 / 30e3) ** 2 / 6))
v.check("Ex 17-10.4d", db((math.pi * fd28 / 120e3) ** 2 / 6))
v.assert_true("Example 4: exact ICI at 1 ppm (N = 4096) is -13.6 dB", abs(db(ici_exact(eps1, 4096)) + 13.6) < 0.05)
sim_ici = of.measure_ici(0.05, 256, 400, rng)
v.assert_true(f"CFO ICI simulated {sim_ici:.5f} vs exact {ici_exact(0.05, 256):.5f}", abs(sim_ici / ici_exact(0.05, 256) - 1) < 0.03)


def doppler_ici_sim(fdT, n=128, trials=400, paths=64):
    """Time-varying Rayleigh channel inside one symbol (Clarke angles); ICI relative to total received power."""
    tot_ici, tot_sig = 0.0, 0.0
    t = np.arange(n) / n
    for _ in range(trials):
        a = rng.uniform(0, 2 * np.pi, paths)
        ph = rng.uniform(0, 2 * np.pi, paths)
        g = np.exp(1j * (2 * np.pi * fdT * np.cos(a)[:, None] * t[None, :] + ph[:, None])).sum(axis=0) / math.sqrt(paths)
        Xd = of.qam(4)[rng.integers(0, 4, n)]
        Yd = np.fft.fft(np.fft.ifft(Xd) * g)
        gm = np.mean(g)  # the common (wanted) gain is the time average of g over the symbol
        tot_ici += np.sum(np.abs(Yd - gm * Xd) ** 2)
        tot_sig += np.sum(np.abs(gm * Xd) ** 2) + np.sum(np.abs(Yd - gm * Xd) ** 2)
    return tot_ici / tot_sig


dsim = doppler_ici_sim(0.05)
v.assert_true(f"Doppler ICI simulated {dsim:.2e} vs (pi fd T)^2/6 = {(math.pi * 0.05) ** 2 / 6:.2e}", abs(dsim / ((math.pi * 0.05) ** 2 / 6) - 1) < 0.1)
v.check("Ex 17-10.5a", papr_level(1e-3, 64))
v.check("Ex 17-10.5b", papr_level(1e-3, 1024))
v.check("Ex 17-10.5c", papr_level(1e-3, 3276))
v.check("Ex 17-10.5d", papr_level(1e-3, 3276) - 10 * math.log10(18 / 10))
p300 = of.ofdm_papr(300, 4000, rng, nfft=1200)
d300 = of.dfts_papr(300, 4000, rng)
q_ofdm, q_dfts = np.quantile(p300, 0.999), np.quantile(d300, 0.999)
v.assert_true(f"PAPR Monte Carlo (300 sc, 4x oversampled): OFDM {q_ofdm:.2f} dB at 1e-3, within 0.5 dB above the approximation; DFT-spread {q_dfts:.2f} dB, at least 2 dB lower", 0 <= q_ofdm - papr_level(1e-3, 300) < 0.5 and q_ofdm - q_dfts > 2)
v.assert_true("16-QAM PAPR (17-06) is 18/10 = 2.55 dB", abs(db(18 / 10) - 2.55) < 0.005)
re_s = 3276 * 14 / 0.5e-3
v.check("Ex 17-10.6a", re_s * 8 * 0.9 * 0.86 / 1e6)
v.check("Ex 17-10.6b", re_s * 8 * 0.9 * 0.86 / 100e6)
v.check("Ex 17-10.6c", db(2 ** 7.2 - 1))
v.assert_true("Example 6: four layers give about 2.3 Gb/s", abs(4 * re_s * 8 * 0.9 * 0.86 / 1e9 - 2.3) < 0.05)
v.assert_true("concept check Q4: SIR 3/(pi 0.05)^2 = 122", round(3 / (math.pi * 0.05) ** 2) == 122)

# ------------------------------------------------------------------ problems
v.check("17-10.1a", corr_window(1, 0.9))
v.check("17-10.1b", 20 * math.log10(corr_window(1, 0.9)))
v.check("17-10.1c", corr_window(1, 1.0))
v.check("17-10.2a", 20e6 / 64 / 1e3)
v.check("17-10.2b", 64 / 20e6 * 1e6)
v.check("17-10.2c", 100 * 0.8 / (3.2 + 0.8))
v.check("17-10.3a", 144 * Ts / 4 * 1e6)
v.check("17-10.3b", c * 144 * Ts / 8)
v.check("17-10.4a", db(1 + 144 / 2048))
v.check("17-10.4b", db(1 + 0.8 / 3.2))
eps_max = optimize.brentq(lambda e: (math.pi * e) ** 2 / 3 - 10 ** -3.5, 1e-6, 0.2)
v.check("17-10.5a", eps_max)
v.check("17-10.5b", eps_max * 30e3)
v.check("17-10.5c", eps_max * 30e3 / 3.5e9 * 1e6)
fdmax = optimize.brentq(lambda f: (math.pi * f / 120e3) ** 2 / 6 - 1e-3, 1, 1e5)
v.check("17-10.6a", fdmax)
v.check("17-10.6b", fdmax * c / 28e9 * 3.6)
v.check("17-10.7a", papr_level(1e-4, 256))
v.check("17-10.7b", papr_level(1e-2, 256))
v.check("17-10.8a", 4096 / 2 * math.log2(4096))
v.check("17-10.8b", 4096 / 2 * math.log2(4096) * 28000)
v.check("17-10.9a", db(0.1**2 * 100))
v.check("17-10.9b", 1 - (1 - Q(math.sqrt(0.1**2 * 100))) ** 2)
v.assert_true("Problem 9: MMSE factor relative to ZF is 0.5 here", abs((0.1 / (0.01 + 0.01)) / (1 / 0.1) - 0.5) < 1e-12)
v.check("17-10.10a", 106 * 12 * 14 / 1e-3 * 6 * 0.75 * 0.86 / 1e6)
v.check("17-10.10b", 106 * 12 * 14 / 1e-3 * 6 * 0.75 * 0.86 / 20e6)
mu_ds = -6.47 - 0.134 * math.log10(6)  # R-284
v.check("17-10.11a", 100 * norm.cdf((math.log10(144 * Ts / 2 / 3) - mu_ds) / 0.39))
v.check("17-10.11b", 100 * norm.cdf((math.log10(144 * Ts / 3) - mu_ds) / 0.39))
v.check("17-10.11c", 10 ** (mu_ds + norm.isf(0.01) * 0.39) * 1e6)
v.check("17-10.12a", 4096 * 144 / 2048)
v.check("17-10.12b", 0.5)
v.check("17-10.13a", ici_exact(0.2, 64))
v.check("17-10.13b", (math.pi * 0.2) ** 2 / 3)
s = of.qam(4)[rng.integers(0, 4, 256)]
x_full = np.fft.ifft(np.fft.fft(s))
v.check("17-10.14a", of.papr_db(x_full))
v.assert_true("Problem 14: full-band DFT-spread returns the QPSK symbols exactly", np.allclose(x_full, s))

# ------------------------------------------------------------------ lab
v.check("Lab 17-10.a", corr_window(2, 0.9))
h6 = np.array([0.7, 0.5, 0.3, 0.3, 0.2, 0.15])
sers = {cp: of.simulate_link(64, cp, h6 / np.linalg.norm(h6), 16, 30.0, 300, rng) for cp in (0, 3, 5, 8)}
v.check("Lab 17-10.b", min(cp for cp, ser in sers.items() if ser == 0))
v.assert_true(f"Lab part 2: SER {sers} (0 and 3 leave an error floor)", sers[0] > 1e-3 and sers[3] > 1e-4 and sers[5] == 0 and sers[8] == 0)
v.check("Lab 17-10.c", db(ici_exact(0.05, 256)))
v.check("Lab 17-10.d", papr_level(1e-3, 300))
v.check("Lab 17-10.e", of.nr_slot_duration(4) * 1e6)
v.assert_true("Lab part 4: -28.8 and -14.9 dB at eps 0.02 and 0.1", abs(db(ici_exact(0.02, 256)) + 28.8) < 0.05 and abs(db(ici_exact(0.1, 256)) + 14.9) < 0.05)

sys.exit(v.finish())
