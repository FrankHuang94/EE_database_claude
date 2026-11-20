#!/usr/bin/env python3
"""Verify every number in chapter 11-11 (modulation and filtering applications), its solutions and lab.

Independent routes:
- spectra by FFTs of simulated modulated signals; band edges from the measured spectral support;
- coherent demodulation by simulating multiplication and low-pass filtering with phase and frequency errors;
- envelope detection by simulating an ideal-diode RC detector and finding where diagonal clipping begins;
- images by simulating a mixer and locating output tones;
- filter orders by searching scipy.signal designs that meet the specification; group delays by differentiating
  computed phase; step overshoots by simulation;
- capacities from the Shannon formula; sourced facts (R-134, R-188) quoted.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("11-11", COURSE / "chapters" / "11-11-modulation-and-filtering-applications.md",
                        COURSE / "solutions" / "11-11-solutions.md",
                        COURSE / "labs" / "11-11-lab" / "README.md")
db = lambda r: 20 * math.log10(abs(r))


def band_edges(msg_lo, msg_hi, fc, fs=4e6, T=0.05):
    """DSB-SC of a dense multitone message spanning [msg_lo, msg_hi]; return the measured occupied edges."""
    t = np.arange(int(fs * T)) / fs
    tones = np.linspace(msg_lo, msg_hi, 40)
    x = sum(np.cos(2 * np.pi * f * t + k) for k, f in enumerate(tones))
    S = np.abs(np.fft.rfft(x * np.cos(2 * np.pi * fc * t)))
    f = np.fft.rfftfreq(len(t), 1 / fs)
    occ = f[S > 0.1 * S.max()]
    return occ.min(), occ.max()


def demod_amplitude(phi_deg, f_msg=1e3, fc=100e3, fs=2e6, T=0.02):
    t = np.arange(int(fs * T)) / fs
    s = np.cos(2 * np.pi * f_msg * t) * np.cos(2 * np.pi * fc * t)
    r = s * np.cos(2 * np.pi * fc * t + math.radians(phi_deg))
    b, a = signal.butter(6, 20e3, fs=fs)
    y = signal.filtfilt(b, a, r)[len(t) // 4: -len(t) // 4]
    return 2 * np.sqrt(2 * np.mean(y ** 2))          # x2 undoes the 1/2 of the product


def envelope_detect(m, fm, fc, RC, fs=None, cycles=6):
    """Ideal diode + RC: output follows the input when the input exceeds it, otherwise decays."""
    fs = fs or 200 * fc
    T = cycles / fm
    t = np.arange(int(fs * T)) / fs
    s = (1 + m * np.cos(2 * np.pi * fm * t)) * np.cos(2 * np.pi * fc * t)
    y = np.empty_like(s)
    y[0] = s[0]
    k = math.exp(-1 / (fs * RC))
    for i in range(1, len(s)):
        y[i] = max(s[i], y[i - 1] * k)
    return t, y, 1 + m * np.cos(2 * np.pi * fm * t)


def clipping_onset(m, fm, fs=4e7, cycles=3):
    """Largest RC for which a diode-RC detector driven by the envelope itself (the f_c -> infinity limit that
    the derivation assumes) never sits above the envelope: bisection on a simulated discharge."""
    t = np.arange(int(fs * cycles / fm)) / fs
    env = 1 + m * np.cos(2 * np.pi * fm * t)

    def worst(RC):
        k = math.exp(-1 / (fs * RC))
        vv = np.empty_like(env)
        vv[0] = env[0]
        for i in range(1, len(env)):
            vv[i] = max(env[i], vv[i - 1] * k)
        return np.max(vv - env)
    lo, hi = 1e-6, 1e-3
    for _ in range(40):
        mid = math.sqrt(lo * hi)
        if worst(mid) < 1e-7:
            lo = mid
        else:
            hi = mid
    return lo


def order(kind, fp, fstop, rp, rs):
    wp, ws = 2 * math.pi * fp, 2 * math.pi * fstop
    for n in range(1, 40):
        if kind == "butter":
            z, p, k = signal.butter(n, wp * (10 ** (rp / 10) - 1) ** (-1 / (2 * n)), analog=True, output="zpk")
        elif kind == "cheby1":
            z, p, k = signal.cheby1(n, rp, wp, analog=True, output="zpk")
        else:
            z, p, k = signal.ellip(n, rp, rs, wp, analog=True, output="zpk")
        _, h = signal.freqs_zpk(z, p, k, worN=np.linspace(ws, 20 * ws, 4000))
        _, hp = signal.freqs_zpk(z, p, k, worN=np.linspace(1, wp, 2000))
        if -db(np.max(np.abs(h))) >= rs - 1e-9 and -db(np.min(np.abs(hp))) <= rp + 1e-9:
            return n, (z, p, k)
    return None, None


def delay_spread(zpk, f1=1e3):
    w = np.linspace(2 * math.pi * 1, 2 * math.pi * f1, 8000)
    _, h = signal.freqs_zpk(*zpk, worN=w)
    gd = -np.gradient(np.unwrap(np.angle(h)), w)
    return (gd.max() - gd.min()) * 1e3


def capacity(B, snr_db):
    return B * math.log2(1 + 10 ** (snr_db / 10))


# ============================================================ theory / practitioner
v.check("T 11-11.a", (0.5) / (1 + 0.5))
v.check("T 11-11.b", 24 + 8)
v.check("T 11-11.c", (7.125 - 5.925) * 1e3)
v.check("T 11-11.d", 1e6 / 20 / 1e3)
v.check("T 11-11.e", 2 * 2)
v.check("T 11-11.f", 100 * (math.log2(1 + 2 * 1000) / math.log2(1 + 1000) - 1), rtol=0.05)

# ============================================================ Example 1
lo, hi = band_edges(300, 3400, 100e3)
v.check("Ex 11-11.1a", lo / 1e3, rtol=2e-4)
v.check("Ex 11-11.1b", hi / 1e3, rtol=2e-4)
v.check("Ex 11-11.1c", 2 * hi / 1e3 - 2 * 100)            # two sidebands of the measured upper extent
v.check("Ex 11-11.1d", demod_amplitude(30))
v.check("Ex 11-11.1e", db(demod_amplitude(30)))
v.assert_true("90 degrees loses the message", demod_amplitude(90) < 1e-3)

# ============================================================ Example 2
eta = lambda m: (m * m * 0.5) / (1 + m * m * 0.5)
fs = 4e6
t = np.arange(int(fs * 0.01)) / fs
s = (1 + 0.5 * np.cos(2 * np.pi * 5e3 * t)) * np.cos(2 * np.pi * 1e6 * t)
S = np.abs(np.fft.rfft(s)) ** 2
f = np.fft.rfftfreq(len(t), 1 / fs)
side = S[(np.abs(f - 1e6) > 1e3) & (np.abs(f - 1e6) < 1e4)].sum()
v.check("Ex 11-11.2a", 100 * side / S.sum())
v.check("Ex 11-11.2b", 100 * eta(1.0))
rcmax = clipping_onset(0.5, 5e3)
v.check("Ex 11-11.2c", rcmax * 1e6)
# with the 1 MHz carrier present, a detector at 0.8x the limit tracks the envelope to within its ripple,
# while one at 3x the limit lags it badly (diagonal clipping)
def lag(RC):
    t_, y_, env_ = envelope_detect(0.5, 5e3, 1e6, RC, cycles=3)
    sl = t_ > 1 / 5e3
    return np.max(y_[sl] - env_[sl])
v.assert_true("carrier simulation: small lag below the limit, large lag above it",
              lag(0.8 * rcmax) < 0.05 and lag(3 * rcmax) > 0.2)
v.check("Ex 11-11.2d", 1 / 1e6 * 1e6)

# ============================================================ Example 3
f0, IF = 1000e3, 455e3
LO = f0 + IF
img = brentq(lambda fr: abs(fr - LO) - IF, LO + 1, 5e6)
v.check("Ex 11-11.3a", LO / 1e3)
v.check("Ex 11-11.3b", img / 1e3)
Q = 20
v.check("Ex 11-11.3c", Q * (img / f0 - f0 / img))
v.check("Ex 11-11.3d", -db(1 / abs(1 + 1j * Q * (img / f0 - f0 / img))))
v.check("Ex 11-11.3e", (540e3 + 2 * IF) / 1e3)
v.assert_true("1910 kHz is above the 1700 kHz top of the table's band", img > 1700e3)

# ============================================================ Example 4
nb, zb = order("butter", 1e3, 1.5e3, 0.5, 50)
nc, zc = order("cheby1", 1e3, 1.5e3, 0.5, 50)
ne, ze = order("ellip", 1e3, 1.5e3, 0.5, 50)
v.check("Ex 11-11.4a", nb)
v.check("Ex 11-11.4b", nc)
v.check("Ex 11-11.4c", ne)
v.assert_true("orders agree with scipy's order formulas",
              (nb, nc, ne) == (signal.buttord(2e3 * math.pi, 3e3 * math.pi, 0.5, 50, analog=True)[0],
                               signal.cheb1ord(2e3 * math.pi, 3e3 * math.pi, 0.5, 50, analog=True)[0],
                               signal.ellipord(2e3 * math.pi, 3e3 * math.pi, 0.5, 50, analog=True)[0]))
n_b, wn_b = signal.buttord(2e3 * math.pi, 3e3 * math.pi, 0.5, 50, analog=True)
v.check("Ex 11-11.4d", delay_spread(signal.butter(n_b, wn_b, analog=True, output="zpk")))
v.check("Ex 11-11.4e", delay_spread(signal.cheby1(nc, 0.5, 2e3 * math.pi, analog=True, output="zpk")))
n_e, wn_e = signal.ellipord(2e3 * math.pi, 3e3 * math.pi, 0.5, 50, analog=True)
v.check("Ex 11-11.4f", delay_spread(signal.ellip(n_e, 0.5, 50, wn_e, analog=True, output="zpk")))
v.check("Ex 11-11.4g", 20 * math.log10(1.5))
v.check("Ex 11-11.4h", 50 / (20 * math.log10(1.5)))

# ============================================================ Example 5
for snr, key in ((30, "5a"), (25, "5b"), (10, "5c"), (0, "5d")):
    v.check(f"Ex 11-11.{key}", capacity(20e6, snr) / 1e6)
v.check("Ex 11-11.5e", (capacity(20e6, 30) - capacity(20e6, 25)) / 20e6)
v.check("Ex 11-11.5f", (capacity(20e6, 30) - capacity(20e6, 25)) / 1e6)

# ============================================================ solutions
lo1, hi1 = band_edges(50, 10e3, 1e6, fs=8e6, T=0.02)
v.check("11-11.1a", lo1 / 1e6, rtol=2e-4)
v.check("11-11.1b", hi1 / 1e6, rtol=2e-4)
v.check("11-11.1c", (hi1 - lo1) / 1e3, rtol=0.01)
v.check("11-11.2a", demod_amplitude(60))
v.check("11-11.2b", db(demod_amplitude(60)))
tt = np.linspace(0, 1e-3, 20001)
envx = 1 + 0.5 * np.cos(2 * np.pi * 1e3 * tt)
emax, emin = envx.max(), envx.min()
v.check("11-11.3a", (emax + emin) / 2)
v.check("11-11.3b", (emax - emin) / (emax + emin))
v.check("11-11.4a", 98.1 + 10.7)
v.check("11-11.4b", 98.1 + 2 * 10.7)
v.check("11-11.4c", 2 * 10.7)
v.check("11-11.5a", 10 * 0.64 / 2)
v.check("11-11.5b", 10 * (1 + 0.64 / 2))
v.check("11-11.5c", 100 * eta(0.8))
rc6 = math.sqrt(1 - 0.64) / (0.8 * 2 * math.pi * 1e4)
v.check("11-11.6a", rc6 * 1e6)
v.check("11-11.6b", 1 / 455e3 * 1e6)
v.check("11-11.6c", rc6 * 455e3)
tz = np.linspace(0.01, 2.6, 260000)
gz = np.cos(2 * np.pi * 0.5 * tz)
zeros = tz[np.where(np.diff(np.sign(gz)) != 0)[0]]
v.check("11-11.7a", np.mean(np.diff(zeros)))
fsm = 20e9
tm = np.arange(200000) / fsm
mix = np.cos(2 * np.pi * 900e6 * tm) * np.cos(2 * np.pi * 1000e6 * tm)
M = np.abs(np.fft.rfft(mix))
fm_ = np.fft.rfftfreq(len(tm), 1 / fsm)
pk = np.sort(fm_[np.argsort(M)[-2:]])
v.check("11-11.8a", pk[0] / 1e6)
v.check("11-11.8b", pk[1] / 1e6)
v.check("11-11.8c", (1000e6 + (1000e6 - 900e6)) / 1e6)
v.check("11-11.9a", 3.1 + 0.9)
v.check("11-11.9b", 12 * (3.1 + 0.9))
for kind, key in (("butter", "10a"), ("cheby1", "10b"), ("ellip", "10c")):
    v.check(f"11-11.{key}", order(kind, 10e3, 20e3, 1, 60)[0])
v.check("11-11.11a", brentq(lambda s: 80e6 * math.log2(1 + s) - 1e9, 1, 1e6))
v.check("11-11.11b", 10 * math.log10(2 ** 12.5 - 1))
fi = brentq(lambda fr: 10 * math.log10(1 + (30 * (fr / 600e3 - 600e3 / fr)) ** 2) - 40, 601e3, 1.2e7)
v.check("11-11.12a", fi / 1e3)
v.check("11-11.12b", (fi - 600e3) / 2 / 1e3)

# ============================================================ lab
v.check("Lab 11-11.a", demod_amplitude(30))
fsl = 20e6
tl = np.arange(400000) / fsl
outs = []
for frf in (1000e3, 1910e3):
    y = np.cos(2 * np.pi * frf * tl) * np.cos(2 * np.pi * 1455e3 * tl)
    Y = np.abs(np.fft.rfft(y))
    fy = np.fft.rfftfreq(len(tl), 1 / fsl)
    outs.append(fy[np.argmax(Y * (fy < 1e6))])
v.assert_true("station and image land on the same IF", abs(outs[0] - outs[1]) < 1)
v.check("Lab 11-11.b", outs[1] / 1e3)
ts = np.linspace(0, 0.02, 200001)
_, ye = signal.step(signal.ellip(n_e, 0.5, 50, wn_e, analog=True), T=ts)
v.check("Lab 11-11.c", 100 * (ye.max() / ye[-1] - 1))
_, yb = signal.step(signal.bessel(5, 2 * math.pi * 1e3, analog=True, norm="mag"), T=ts)
v.check("Lab 11-11.d", 100 * (yb.max() / yb[-1] - 1))

sys.exit(v.finish())
