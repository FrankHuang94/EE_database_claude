#!/usr/bin/env python3
"""Verify every number in chapter 18-10 (sensors), its problems and its lab.

Independent routes:
- spring-mass mechanics by solving the static equilibrium and the resonance directly;
- the thermomechanical floor by integrating the displacement noise of a damped oscillator driven by the
  fluctuation-dissipation force (equipartition check: <x^2> = kB T / k) as well as by the closed form;
- the complementary filter's noise reduction by summing its impulse response squared, and its bias error by
  iterating the recursion to steady state;
- PPG SNR from the shot-noise formula and from a simulated photocurrent; heart rate from a synthetic signal;
- decibels, and the barometric gradient by differentiating the standard-atmosphere formula numerically.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "18-10-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import sensors as sn  # noqa: E402

v = Verifier.from_files("18-10", ROOT / "chapters" / "18-10-sensors.md",
                        ROOT / "solutions" / "18-10-solutions.md", LAB / "README.md")

KB, G, QE, T = 1.380649e-23, 9.80665, 1.602176634e-19, 300.0


def floor(m, f0, q):
    return math.sqrt(4 * KB * T * 2 * math.pi * f0 / (m * q))


def alpha_noise_factor(alpha, n=20000):
    """Std of the output of y_n = alpha y_{n-1} + (1 - alpha) x_n for unit white x, from the impulse response."""
    h = (1 - alpha) * alpha ** np.arange(n)
    return math.sqrt(float(np.sum(h ** 2)))


def bias_error(alpha, dt, b, n=200000):
    th = 0.0
    for _ in range(n):
        th_new = alpha * (th + b * dt)
        if abs(th_new - th) < 1e-15:
            break
        th = th_new
    return th


# ---------------------------------------------------------------- Example 1
m1, f1 = 2e-9, 4e3
k1 = m1 * (2 * math.pi * f1) ** 2
v.check("Ex 18-10.1a", k1)
x1 = m1 * G / k1
v.check("Ex 18-10.1b", 1e9 * x1)
c_plus, c_minus = 100e-15 * 1.5e-6 / (1.5e-6 - x1), 100e-15 * 1.5e-6 / (1.5e-6 + x1)
v.check("Ex 18-10.1c", 100 * (c_plus - c_minus) / 100e-15)
v.check("Ex 18-10.1d", 1e15 * (c_plus - c_minus))
an = floor(m1, f1, 2.0)
v.check("Ex 18-10.1e", an / G * 1e6)
# equipartition: integrate the displacement PSD of the force noise through the oscillator; <x^2> must be kB T / k
w0, qf = 2 * math.pi * f1, 2.0
b_damp = m1 * w0 / qf
sf = 4 * KB * T * b_damp                       # one-sided force PSD, N^2/Hz


def x_psd(f):
    w = 2 * math.pi * f
    return sf / ((k1 - m1 * w * w) ** 2 + (b_damp * w) ** 2)


edges = np.concatenate(([0.0], np.logspace(-4, 4, 161) * f1))
x2 = sum(quad(x_psd, lo, hi, epsrel=1e-12, epsabs=0)[0] for lo, hi in zip(edges[:-1], edges[1:]))
x2 += quad(x_psd, edges[-1], np.inf, epsrel=1e-10)[0]
v.assert_true("equipartition <x^2> = kB T / k for the fluctuation-dissipation force", abs(x2 / (KB * T / k1) - 1) < 1e-3, str(x2 / (KB * T / k1)))
v.assert_true("sanity: gravity on 2 ug is about 20 nN", abs(m1 * G - 19.6e-9) < 0.1e-9)

# ---------------------------------------------------------------- Example 2
r2 = 120e-6 * math.sqrt(50)
v.check("Ex 18-10.2a", 1e3 * r2)
v.check("Ex 18-10.2b", math.degrees(math.atan(r2)))
v.check("Ex 18-10.2c", math.degrees(math.atan(r2)) / 10)

# ---------------------------------------------------------------- Example 3
vel = 2 * math.pi * 20e3 * 5e-6
v.check("Ex 18-10.3a", vel)
v.check("Ex 18-10.3b", 2 * math.radians(100) * vel)
v.check("Ex 18-10.3c", 0.007 * math.sqrt(3600))
rng = np.random.default_rng(18103)
walks = np.cumsum(rng.normal(0, 0.007 * math.sqrt(100), size=(2000, 6000)) * 0.01, axis=1)[:, -1]
v.assert_true("simulated angle random walk after 60 s matches N sqrt(t) within 5%", abs(np.std(walks) / (0.007 * math.sqrt(60)) - 1) < 0.05)
v.check("Ex 18-10.3d", 0.007 * math.sqrt(60))
v.check("Ex 18-10.3e", 0.5 * 60)

# ---------------------------------------------------------------- Example 4
tau4 = 0.98 * 0.01 / 0.02
v.check("Ex 18-10.4a", tau4)
v.check("Ex 18-10.4b", bias_error(0.98, 0.01, 0.5))
v.assert_true("bias error equals b tau", abs(bias_error(0.98, 0.01, 0.5) - 0.5 * tau4) < 1e-9)
v.check("Ex 18-10.4c", math.degrees(math.atan(0.02)))
v.check("Ex 18-10.4d", alpha_noise_factor(0.98))
v.assert_true("closed form sqrt((1 - a)/(1 + a))", abs(alpha_noise_factor(0.98) - math.sqrt(0.02 / 1.98)) < 1e-9)
acc, gyro, fused = sn.simulate_fusion(0.98)
v.check("Ex 18-10.4e", acc)
v.check("Ex 18-10.4f", gyro)
v.check("Ex 18-10.4g", fused)
v.assert_true("fused error is near the root-sum of bias error and filtered noise",
              0.25 < fused < 0.32 and math.hypot(0.245, 1.146 * 0.1005) < fused)

# ---------------------------------------------------------------- Example 5
snr = 10 * math.log10(0.01 ** 2 * 1e-6 / (4 * QE * 10))
v.check("Ex 18-10.5a", snr)
fs_sim, n_sim = 2000.0, 400000
rng5 = np.random.default_rng(18105)
t5 = np.arange(n_sim) / fs_sim
i5 = 1e-6 * (1 + 0.01 * np.sin(2 * np.pi * 1.2 * t5)) + rng5.normal(0, math.sqrt(2 * QE * 1e-6 * fs_sim / 2), n_sim)
spec = np.abs(np.fft.rfft(i5 - i5.mean())) ** 2
f5 = np.fft.rfftfreq(n_sim, 1 / fs_sim)
sig = spec[np.argmin(abs(f5 - 1.2))]
noise_per_bin = np.mean(spec[(f5 > 5) & (f5 < 900)])          # mean, not median: |X|^2 of noise is exponential
bin_w = fs_sim / n_sim
snr_sim = 10 * math.log10(sig / (noise_per_bin * 10 / bin_w))
v.assert_true("simulated photocurrent gives the shot-noise SNR within 1 dB", abs(snr_sim - snr) < 1.0, f"{snr_sim:.2f}")
v.check("Ex 18-10.5b", 1e6 * 20e-3 * 100e-6 * 100)
v.check("Ex 18-10.5c", 1e6 * 20e-3 * 50e-6 * 25)

# ---------------------------------------------------------------- Example 6
v.check("Ex 18-10.6a", 94 + 26)
v.check("Ex 18-10.6b", 94 - 65)
v.check("Ex 18-10.6c", (94 + 26) - (94 - 65))
v.check("Ex 18-10.6d", 20 * math.log10(1 / 20e-6))
h = 1e-3
grad = -(sn.altitude_m(101325.0 + h) - sn.altitude_m(101325.0 - h)) / (2 * h)
dpdh = 1 / grad if grad != 0 else float("nan")
v.check("Ex 18-10.6e", -abs(dpdh))
v.assert_true("formula -rho g agrees with the derivative", abs(sn.pressure_gradient_pa_per_m() - (-abs(dpdh))) < 1e-3)
v.check("Ex 18-10.6f", 100 / abs(dpdh))
v.check("Ex 18-10.6g", 3 * abs(dpdh))

# ---------------------------------------------------------------- Problems
f_p1 = math.sqrt(2 / 5e-9) / (2 * math.pi)
v.check("18-10.1a", f_p1)
x_p1 = 5e-9 * 2 * G / 2
v.check("18-10.1b", 1e9 * x_p1)
v.check("18-10.1c", 100 * 2 * x_p1 / 2e-6)
r_p2 = 150e-6 * math.sqrt(1.57 * 80)
v.check("18-10.2a", 1e3 * r_p2)
v.check("18-10.2b", math.degrees(r_p2))
v.check("18-10.3a", 1e3 * 10 ** (-38 / 20))
v.check("18-10.3b", 10 ** (-38 / 20) * 10 ** (26 / 20))
v.check("18-10.3c", 94 - 64)
an4 = 20e-6 * G
m4 = 4 * KB * T * 2 * math.pi * 3e3 / (1.0 * an4 ** 2)
v.check("18-10.4a", 1e9 * m4)
v.assert_true("mass gives exactly 20 ug/rtHz", abs(floor(m4, 3e3, 1.0) / G * 1e6 - 20) < 1e-9)
n5 = 0.3 / 60
v.check("18-10.5a", n5 * math.sqrt(600))
v.check("18-10.5b", 2 / 3600 * 600)
tau6 = 0.1 / 0.2
v.check("18-10.6a", tau6)
a6 = tau6 / (tau6 + 1 / 200)
v.check("18-10.6b", a6)
v.check("18-10.6c", alpha_noise_factor(a6))
v.check("18-10.7a", 20 * math.log10(1 / 0.3))
v.check("18-10.7b", sn.shot_noise_snr_db(1e-6, 10, 0.003))
v.check("18-10.7c", 10 ** (6.02 / 10))
v.check("18-10.7d", sn.shot_noise_snr_db(4e-6, 10, 0.003))
v.check("18-10.8a", 60 / 8)
v.check("18-10.8b", 60 / 16)
v.check("18-10.9a", 1.5 / math.sqrt(25))
v.check("18-10.9b", 100 * (1.5 / math.sqrt(25)) / 12.01)
v.check("18-10.9c", 100 * 30 / (3 * 3600))
v.check("18-10.10a", 32 / 25)
wake = 2e-3 * 3e-3 / (32 / 25)
v.check("18-10.10b", 1e6 * wake)
tot = 8e-6 + 0.05 * 900e-6 + 25e-6 + 30e-6 + wake + 2e-6
v.check("18-10.10c", 1e6 * tot)
v.check("18-10.10d", 0.200 / tot / 24)
v.assert_true("gyroscope 39% and PPG 48% of the total", round(100 * 45e-6 / tot) == 39 and round(100 * 55e-6 / tot) == 48)

# ---------------------------------------------------------------- lab
v.check("Lab 18-10.a", floor(4e-9, 4e3, 2.0) / G * 1e6)
v.check("Lab 18-10.b", floor(2e-9, 4e3, 200.0) / G * 1e6)
fs, tt = 50, np.arange(0, 8, 1 / 50)
rng10 = np.random.default_rng(1810)


def ppg(art):
    i0 = 1e-6
    return (i0 * (1 + 0.01 * np.sin(2 * np.pi * 1.2 * tt)) + art * 0.01 * i0 * np.sin(2 * np.pi * 1.5 * tt)
            + rng10.normal(0, math.sqrt(2 * QE * i0 * 25), len(tt)))


v.check("Lab 18-10.c", sn.heart_rate_from_signal(ppg(0.5), fs))
v.check("Lab 18-10.d", sn.heart_rate_from_signal(ppg(2.0), fs))
fus = {a: sn.simulate_fusion(a)[2] for a in (0.9, 0.98, 0.998)}
v.assert_true("fusion errors about 0.26, 0.29 and 2.5 deg", abs(fus[0.9] - 0.26) < 0.01 and abs(fus[0.98] - 0.29) < 0.01
              and abs(fus[0.998] - 2.5) < 0.05, str(fus))
grid = np.linspace(0.90, 0.995, 40)
errs = [sn.simulate_fusion(a)[2] for a in grid]
v.assert_true("best alpha near 0.96 with about 0.21 deg", abs(grid[int(np.argmin(errs))] - 0.96) < 0.01 and abs(min(errs) - 0.21) < 0.01)
v.assert_true("alpha 0.998: tau about 5 s and bias error about 2.5 deg",
              abs(sn.complementary_time_constant(0.998, 0.01) - 4.99) < 0.01 and abs(0.5 * 4.99 - 2.5) < 0.01)

sys.exit(v.finish())
