#!/usr/bin/env python3
"""Verify chapter 17-03 (analog modulation): text, examples, problems and lab answers.

Routes:
- Bessel coefficients from SciPy and, independently, by numerically integrating their defining integral;
  carrier nulls by root finding; Carson fractions by summation;
- SSB spectra, carrier-error effects and sideband suppression by simulating phasing modulators and
  coherent detectors and reading FFT lines;
- output-SNR formulas in closed form and by Monte Carlo simulation of each receiver (coherent DSB and SSB,
  envelope-detected AM, quadrature FM discriminator), using the lab's analogmod.py;
- the pre-emphasis gain by numerically integrating the de-emphasized parabolic noise spectrum;
- the radar beat by simulating a dechirped echo.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize
from scipy.special import jv

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "17-03-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import analogmod as am  # noqa: E402

CH = ROOT / "chapters" / "17-03-analog-modulation.md"
v = Verifier.from_files("17-03", CH, ROOT / "solutions" / "17-03-solutions.md", LAB / "README.md")
rng = np.random.default_rng(1703)
C = 299_792_458.0


def db(x):
    return 10 * math.log10(x)


def jn_int(n, beta):
    """J_n(beta) from its defining integral (1/2pi) int exp(j(beta sin t - n t)) dt (real part)."""
    val, _ = integrate.quad(lambda t: math.cos(beta * math.sin(t) - n * t), -math.pi, math.pi, limit=200)
    return val / (2 * math.pi)


def line_amp(x, fs, f):
    """Amplitude of a sinusoid at frequency f in x (record holds an integer number of cycles)."""
    X = np.fft.rfft(x) / len(x) * 2
    k = int(round(f * len(x) / fs))
    return abs(X[k])


for n, b in ((0, 5), (1, 1), (2, 0.2), (6, 5)):
    v.assert_true(f"Bessel J{n}({b}) by integral", abs(jn_int(n, b) - jv(n, b)) < 1e-10)

# ------------------------------------------------------------------ text
z1 = optimize.brentq(lambda b: jv(0, b), 2, 3, xtol=1e-14)
z2 = optimize.brentq(lambda b: jv(0, b), 5, 6, xtol=1e-14)
v.check("Txt 17-03.a", z1)
v.check("Txt 17-03.b", z2)
frac6 = am.power_fraction(5, 6)
v.check("Txt 17-03.c", 100 * frac6)
v.check("Txt 17-03.d", am.carson(75, 15))
v.check("Txt 17-03.e", db(0.5 / 1.5))
v.check("Txt 17-03.f", db(1.5 * 25))
W = 15e3


def deemph_gain(tau, w=W):
    f1 = 1 / (2 * math.pi * tau)
    num, _ = integrate.quad(lambda f: f * f, 0, w)
    den, _ = integrate.quad(lambda f: f * f / (1 + (f / f1) ** 2), 0, w)
    return num / den, f1


I75, f75 = deemph_gain(75e-6)
v.check("Txt 17-03.g", db(I75))
v.check("Txt 17-03.h", 20 * math.log10(math.hypot(1, 2 * math.pi * 15e3 * 75e-6)))
v.check("Txt 17-03.i", db(8))
v.check("Txt 17-03.j", db((53 / 5) ** 2))
v.check("Txt 17-03.k", 20 * math.log10(2.2))
v.check("Txt 17-03.l", 10 * math.log10((2.2e-6) ** 2 / (4 * 50) / 1e-3))
v.check("Txt 17-03.m", db(1 / math.tan(math.radians(0.5)) ** 2))
v.check("Txt 17-03.n", 9 / 2)
v.assert_true("sum of J_n^2 is 1 (beta = 5)", abs(am.power_fraction(5, 60) - 1) < 1e-12)

# ------------------------------------------------------------------ Example 1 (simulated)
fs, n = 1.0e6, 1_000_000
t = np.arange(n) / fs
m = np.cos(2 * np.pi * 1000 * t)
s = am.ssb(m, 100e3, fs, upper=True, amp=2.0)
X = np.abs(np.fft.rfft(s))
f = np.fft.rfftfreq(n, 1 / fs)
v.check("Ex 17-03.1a", f[np.argmax(X)] / 1e3)
y = 2 * s * np.cos(2 * np.pi * 100_050 * t)
Y = np.abs(np.fft.rfft(y))
low = f < 20e3
v.check("Ex 17-03.1b", f[low][np.argmax(Y[low])])
d = am.dsb_sc(m, 100e3, fs)
yd = 2 * d * np.cos(2 * np.pi * 100e3 * t + math.radians(60))
amp = line_amp(yd, fs, 1000)
v.check("Ex 17-03.1c", amp)
v.check("Ex 17-03.1d", 20 * math.log10(amp))
ys = 2 * s * np.cos(2 * np.pi * 100e3 * t + math.radians(60))
v.assert_true("SSB with 60 deg phase error keeps full amplitude", abs(line_amp(ys, fs, 1000) - 1) < 1e-3)

# ------------------------------------------------------------------ Example 2
v.check("Ex 17-03.2a", 75 / 15)
v.check("Ex 17-03.2b", am.carson(75, 15))
v.check("Ex 17-03.2c", 100 * frac6)
v.check("Ex 17-03.2d", 100 * jv(0, 5) ** 2)
v.check("Ex 17-03.2e", jn_int(0, 5))
v.check("Ex 17-03.2f", 100 * am.power_fraction(5, 5))
v.check("Ex 17-03.2g", 100 * (am.power_fraction(5, 7) - frac6))
# FFT of simulated tone FM (complex baseband) against the Bessel lines
fs2, n2 = 1.536e6, 1 << 16
fm_tone = fs2 / n2 * 640  # 15 kHz exactly on a bin
tt = np.arange(n2) / fs2
zz = np.exp(1j * 5 * np.sin(2 * np.pi * fm_tone * tt))
Z = np.fft.fft(zz) / n2
lines = [abs(Z[(640 * k) % n2]) for k in range(-6, 7)]
v.assert_true("FFT lines of tone FM equal |J_n(5)|", max(abs(a - abs(jv(k, 5))) for a, k in zip(lines, range(-6, 7))) < 1e-9)

# ------------------------------------------------------------------ Example 3
v.check("Ex 17-03.3a", z1)
v.check("Ex 17-03.3b", z2)
v.check("Ex 17-03.3c", 5 / z1)
v.check("Ex 17-03.3d", 20 * math.log10(jv(1, 0.2) / jv(0, 0.2)))
v.check("Ex 17-03.3e", jv(2, 0.2))
v.check("Ex 17-03.3f", -20 * math.log10(jv(2, 0.2) / jv(0, 0.2)))

# ------------------------------------------------------------------ Examples 4 and 5
N0 = -174 + 6
gamma = -95 - (N0 + 10 * math.log10(W))
v.check("Ex 17-03.4a", gamma)
v.check("Ex 17-03.4b", am.snr_theory_db("am", gamma, pm=0.5, ka=1.0))
v.check("Ex 17-03.4c", am.snr_theory_db("fm", gamma, pm=0.5, d=5))
v.check("Ex 17-03.4d", gamma - db(180e3 / W))
pth = N0 + 10 * math.log10(180e3) + 10
gth = pth - (N0 + 10 * math.log10(W))
v.check("Ex 17-03.5a", pth)
v.check("Ex 17-03.5b", gth)
v.check("Ex 17-03.5c", am.snr_theory_db("fm", gth, pm=0.5, d=5))
v.check("Ex 17-03.5d", am.snr_theory_db("am", gth, pm=0.5, ka=1.0))

# Monte Carlo of the receivers
for sch in ("dsb", "ssb", "am"):
    snr, pm = am.simulate_linear_snr(sch, 30.0, rng=rng)
    th = am.snr_theory_db(sch, 30.0, pm=pm, ka=0.9)
    v.assert_true(f"Monte Carlo {sch} at gamma 30 dB within 0.3 dB", abs(snr - th) < 0.3, f"{snr:.2f} vs {th:.2f}")
fm_sim = am.simulate_fm_snr(30.0, rng=rng, if_factor=1.5)
fm_th = am.snr_theory_db("fm", 30.0)
v.assert_true("Monte Carlo FM at gamma 30 dB within 0.3 dB", abs(fm_sim - fm_th) < 0.3, f"{fm_sim:.2f} vs {fm_th:.2f}")
fm_low = am.simulate_fm_snr(14.0, rng=rng)
v.assert_true("FM collapses below threshold (gamma 14 dB, >5 dB under formula)",
              fm_low < am.snr_theory_db("fm", 14.0) - 5, f"{fm_low:.2f}")

# ------------------------------------------------------------------ Example 6
v.check("Ex 17-03.6a", f75)
v.check("Ex 17-03.6b", I75)
v.check("Ex 17-03.6c", db(I75))
I50, f50 = deemph_gain(50e-6)
v.check("Ex 17-03.6d", f50)
v.check("Ex 17-03.6e", I50)
v.check("Ex 17-03.6f", db(I50))
x = W / f75
v.assert_true("closed form x^3/(3(x - atan x))", abs(I75 - x ** 3 / (3 * (x - math.atan(x)))) < 1e-9)

# ------------------------------------------------------------------ Problem 1 (simulated)
fs, n = 100e3, 100_000
t = np.arange(n) / fs
m1 = np.cos(2 * np.pi * 300 * t) + 0.5 * np.sin(2 * np.pi * 2000 * t)
u = am.ssb(m1, 10e3, fs, upper=True)
U = np.abs(np.fft.rfft(u)) / n * 2
lines_u = np.fft.rfftfreq(n, 1 / fs)[U > 0.1]
v.assert_true("P1 exactly two spectral lines", len(lines_u) == 2, str(lines_u))
v.check("17-03.1a", lines_u[0] / 1e3)
v.check("17-03.1b", line_amp(u, fs, lines_u[0]))
v.check("17-03.1c", lines_u[1] / 1e3)
v.check("17-03.1d", line_amp(u, fs, lines_u[1]))
v.assert_true("P1 nothing below the carrier", max(line_amp(u, fs, 9.7e3), line_amp(u, fs, 8e3)) < 1e-9)
v.assert_true("P1 Hilbert of the message", np.max(np.abs(am.hilbert(m1) - (np.sin(2 * np.pi * 300 * t) - 0.5 * np.cos(2 * np.pi * 2000 * t)))) < 1e-9)

# ------------------------------------------------------------------ Problems 2-10
v.check("17-03.2a", 2 * 5)
v.check("17-03.2b", 5)
v.check("17-03.2c", 0.64 / 2.64)
v.assert_true("P2 fraction from the waveform", abs(np.mean((0.8 * np.cos(2 * np.pi * 1000 * t)) ** 2) / np.mean((1 + 0.8 * np.cos(2 * np.pi * 1000 * t)) ** 2) - 0.64 / 2.64) < 1e-9)
fi = 1e6 + 3000 * np.cos(2 * np.pi * 1000 * np.linspace(0, 1e-3, 10001))
v.check("17-03.3a", fi.min() / 1e3)
v.check("17-03.3b", fi.max() / 1e3)
v.check("17-03.3c", 3000 / 1000)
v.check("17-03.3d", am.carson(3, 1))
v.check("17-03.4a", jv(0, 1) ** 2)
v.check("17-03.4b", 2 * jv(1, 1) ** 2)
v.check("17-03.4c", am.power_fraction(1, 2))
tt = np.linspace(0, 1, 100001)
env = np.sqrt(1 + (0.2 * np.sin(2 * np.pi * tt)) ** 2)
v.check("17-03.5a", env.max())
v.check("17-03.6a", 75e3 / 25)
v.check("17-03.6b", 200e3 * 3000 / 1e6)
v.check("17-03.6c", (200e3 * (75e3 / 25) - 100e6) / 1e6)
v.check("17-03.7a", db(4))
v.check("17-03.7b", am.carson(150, 15))
v.check("17-03.7c", db(330 / 180))
# P8 by direct power accounting on waveforms
th = np.linspace(0, 2 * np.pi, 200001)[:-1]
am_env = 1 + np.cos(th)
pep_am = am_env.max() ** 2 / 2
pav_am = np.mean(am_env ** 2) / 2
snr_am = (1 / 3) * pav_am
snr_ssb = pep_am  # SSB tone: average power equals peak envelope power
v.check("17-03.8a", db(snr_ssb / snr_am))
H = math.hypot(1, 2 * math.pi * 15e3 * 75e-6)
v.check("17-03.9a", H)
v.check("17-03.9b", 20 * math.log10(H))
v.check("17-03.10a", 2 * 75)
# discriminator check: at fs just above 150 kHz the 75 kHz peak is recovered; below it wraps
zf = am.fm_baseband(np.cos(2 * np.pi * 1e3 * np.arange(20000) / 160e3), 160e3, 75e3)
v.assert_true("P10 discriminator recovers 75 kHz at 160 kS/s", abs(am.fm_discriminator(zf, 160e3).max() - 75e3) < 200)
zf2 = am.fm_baseband(np.cos(2 * np.pi * 1e3 * np.arange(20000) / 140e3), 140e3, 75e3)
v.assert_true("P10 discriminator wraps at 140 kS/s", am.fm_discriminator(zf2, 140e3).max() < 70e3)

# ------------------------------------------------------------------ Problem 11
v.check("17-03.11a", db(1 ** 2 * 0.5))
v.check("17-03.11b", db((math.pi / 2) ** 2 * 0.5))

# ------------------------------------------------------------------ Problem 12
for tag, g in (("a", 25), ("c", 15)):
    gl = 10 ** (g / 10)
    dmax = gl / 20 - 1
    v.check(f"17-03.12{tag}", dmax)
    v.check(f"17-03.12{chr(ord(tag) + 1)}", db(1.5 * dmax ** 2 * gl))
    v.assert_true(f"P12 CNR at D_max is 10 dB (gamma {g})", abs(db(gl / (2 * (dmax + 1))) - 10) < 1e-9)


# ------------------------------------------------------------------ Problem 13 (simulated phasing modulator)
def suppression_sim(eps_deg, g):
    fs, n = 1e6, 100_000
    t = np.arange(n) / fs
    mm = np.cos(2 * np.pi * 1e3 * t)
    mh = am.hilbert(mm)
    out = mm * np.cos(2 * np.pi * 100e3 * t) - g * mh * np.sin(2 * np.pi * 100e3 * t + math.radians(eps_deg))
    return 20 * math.log10(line_amp(out, fs, 101e3) / line_amp(out, fs, 99e3))


def suppression(eps_deg, g):
    e = math.radians(eps_deg)
    return db((1 + 2 * g * math.cos(e) + g * g) / (1 - 2 * g * math.cos(e) + g * g))


for tag, (e, g) in zip("abc", ((1, 1.0), (0, 1.01), (1, 1.01))):
    v.check(f"17-03.13{tag}", suppression_sim(e, g))
    v.assert_true(f"P13 formula agrees ({tag})", abs(suppression_sim(e, g) - suppression(e, g)) < 1e-6)

# ------------------------------------------------------------------ Problem 14 (simulated dechirp)
B, Tc = 4e9, 40e-6
S = B / Tc
fsr = 200e6
tr = np.arange(int(Tc * fsr)) / fsr
tau = 2 * 30 / C
tx = np.exp(1j * np.pi * S * tr ** 2)
rx = np.exp(1j * np.pi * S * (tr - tau) ** 2)
beat = tx * np.conj(rx)
nfft = 1 << 20
Bt = np.abs(np.fft.fft(beat, nfft))
fb = np.fft.fftfreq(nfft, 1 / fsr)[np.argmax(Bt)]
v.check("17-03.14a", fb / 1e6)
v.assert_true("P14 beat equals S tau", abs(fb - S * tau) < fsr / nfft)
v.check("17-03.14b", 10e6 * C / (2 * S))
v.check("17-03.14c", C / (2 * B) * 100)
v.check("17-03.14d", tau * 1e9)

# ------------------------------------------------------------------ Problem 12(e): threshold-limited break-even
def fm_minus_ssb(gl):
    dmax = gl / 20 - 1
    return 1.5 * dmax ** 2 * gl - gl


g_even = optimize.brentq(fm_minus_ssb, 21, 1000, xtol=1e-12)
v.check("17-03.12e", db(g_even))
v.assert_true("P12e D = sqrt(2/3) at break-even", abs((g_even / 20 - 1) - math.sqrt(2 / 3)) < 1e-9)

# ------------------------------------------------------------------ Problem 15: Costas loop detector (simulated)
fs15, n15 = 200e3, 200_000
t15 = np.arange(n15) / fs15
m15 = np.cos(2 * np.pi * 300 * t15)  # zero mean, P_m = 0.5
s15 = am.dsb_sc(m15, 20e3, fs15, amp=2.0)
trim = slice(5000, n15 - 5000)


def costas_out(phi):
    i_arm = am.lowpass(s15 * np.cos(2 * np.pi * 20e3 * t15 + phi), 3e3, fs15)
    q_arm = am.lowpass(s15 * np.sin(2 * np.pi * 20e3 * t15 + phi), 3e3, fs15)
    return np.mean((i_arm * q_arm)[trim])


dphi = 1e-3
kd = abs(costas_out(dphi) - costas_out(-dphi)) / (2 * dphi)
v.check("17-03.15", kd)
v.assert_true("P15 detector is (1/8)A^2 Pm sin(2 phi)", all(abs(costas_out(p) - 0.125 * 4 * 0.5 * math.sin(2 * p)) < 1e-3 for p in (0.3, 1.0, 2.0)))
v.assert_true("P15 null at pi as well as 0", abs(costas_out(math.pi)) < 1e-6 and abs(costas_out(0.0)) < 1e-6)

# ------------------------------------------------------------------ Problem 16: carrier errors (simulated)
fs16, n16, fc16 = 100e3, 100_000, 10e3
t16 = np.arange(n16) / fs16
m16 = np.cos(2 * np.pi * 300 * t16) + 0.5 * np.cos(2 * np.pi * 1200 * t16)
dsb16 = am.dsb_sc(m16, fc16, fs16)
usb16 = am.ssb(m16, fc16, fs16, upper=True)


def out_lines(sig, phase=0.0, df=0.0, scale=1.0):
    y = am.coherent_demod(sig, fc16, fs16, 4e3, phase=phase, freq_offset=df)[trim.start // 2:n16 - trim.start // 2]
    y = y[: (len(y) // int(fs16)) * int(fs16)] if len(y) >= fs16 else y
    Y = np.abs(np.fft.rfft(y)) / len(y) * 2 / scale
    f = np.fft.rfftfreq(len(y), 1 / fs16)
    keep = Y > 0.05
    return f[keep], Y[keep]


f_ref, a_ref = out_lines(dsb16)
v.assert_true("P16 reference DSB output is the message", np.allclose(f_ref, [300, 1200]) and np.allclose(a_ref, [1, 0.5], atol=5e-3))
f_a, a_a = out_lines(dsb16, phase=math.radians(30))
v.check("17-03.16a", a_a[0] / a_ref[0])
v.assert_true("P16 DSB phase error scales both tones alike", abs(a_a[1] / a_ref[1] - a_a[0] / a_ref[0]) < 1e-3)
f_b, a_b = out_lines(dsb16, df=20.0)
v.assert_true("P16 DSB 20 Hz error gives four lines", len(f_b) == 4, str(f_b))
v.check("17-03.16b", f_b[0])
v.check("17-03.16c", f_b[1])
v.assert_true("P16 DSB beat amplitudes 0.5, 0.5, 0.25, 0.25", np.allclose(a_b, [0.5, 0.5, 0.25, 0.25], atol=1e-2), str(a_b))
f_c, a_c = out_lines(usb16, phase=math.radians(30))
f_c0, a_c0 = out_lines(usb16)
v.assert_true("P16 SSB phase error leaves amplitudes unchanged", np.allclose(f_c, [300, 1200]) and np.allclose(a_c, a_c0, rtol=1e-3))
f_d, a_d = out_lines(usb16, df=20.0)
v.assert_true("P16 SSB 20 Hz error gives two shifted lines", len(f_d) == 2 and np.allclose(a_d / a_c0, 1, atol=1e-2), f"{f_d} {a_d}")
v.check("17-03.16d", f_d[1])

# ------------------------------------------------------------------ lab
v.check("Lab 17-03.a", am.snr_theory_db("fm", 30.0))
v.check("Lab 17-03.b", am.snr_theory_db("dsb", 30.0))
v.check("Lab 17-03.c", 10 + db(2 * (5 + 1)))

sys.exit(v.finish())
