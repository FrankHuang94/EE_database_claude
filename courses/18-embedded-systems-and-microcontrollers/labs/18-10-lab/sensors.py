"""Lab 18-10: physics and signal arithmetic of MEMS inertial sensors, optical heart-rate sensing, MEMS microphones
and barometers.

- MEMS accelerometer: resonance, static deflection, capacitive readout, thermomechanical (Brownian) noise floor;
- noise density to rms noise over a bandwidth;
- gyroscope: Coriolis acceleration, angle random walk, integrated-angle drift from a bias;
- tilt from an accelerometer and a complementary filter fusing it with a gyroscope (simulated);
- PPG: Beer-Lambert attenuation, perfusion index, shot-noise-limited SNR, heart rate from a spectrum;
- microphones: SPL and dBFS arithmetic, noise floor from SNR;
- barometer: altitude from pressure.
"""
from __future__ import annotations

import math

import numpy as np

KB = 1.380649e-23        # J/K
G0 = 9.80665             # m/s^2, standard gravity
Q_E = 1.602176634e-19    # C
P_REF = 20e-6            # Pa, 0 dB SPL


# ------------------------------------------------------------------ MEMS accelerometer
def resonance_hz(k: float, m: float) -> float:
    return math.sqrt(k / m) / (2 * math.pi)


def static_deflection(a: float, f0: float) -> float:
    """x = a / omega0^2 for a spring-mass system below resonance."""
    return a / (2 * math.pi * f0) ** 2


def capacitance_change(x: float, gap: float) -> float:
    """Differential parallel-plate pair: (C1 - C2)/C0 = 2x/gap for small x."""
    return 2 * x / gap


def brownian_noise_density(m: float, f0: float, q: float, t: float = 300.0) -> float:
    """Thermomechanical acceleration noise density sqrt(4 kB T omega0 / (m Q)) in (m/s^2)/sqrt(Hz)."""
    return math.sqrt(4 * KB * t * 2 * math.pi * f0 / (m * q))


def rms_noise(density: float, bandwidth: float, nbw_factor: float = 1.0) -> float:
    """rms noise of a white density over a bandwidth (nbw_factor 1.57 for a first-order low-pass's noise bandwidth)."""
    return density * math.sqrt(bandwidth * nbw_factor)


# ------------------------------------------------------------------ gyroscope
def coriolis_acceleration(omega: float, v: float) -> float:
    return 2 * omega * v


def angle_random_walk_deg_per_rt_hour(density_dps_per_rt_hz: float) -> float:
    """ARW in deg/sqrt(h) from a one-sided rate noise density in (deg/s)/sqrt(Hz): 60 / sqrt(2) times it
    (sqrt(3600 s/h), and the one-sided density's two-sided level is N^2 / 2)."""
    return density_dps_per_rt_hz * 60.0 / math.sqrt(2.0)


def angle_drift_from_bias(bias_dps: float, t: float) -> float:
    return bias_dps * t


def angle_noise_after(density_dps_per_rt_hz: float, t: float) -> float:
    """Standard deviation of the integrated angle (deg) after t seconds of white rate noise of one-sided density N:
    N sqrt(t / 2)."""
    return density_dps_per_rt_hz * math.sqrt(t / 2.0)


# ------------------------------------------------------------------ tilt and fusion
def tilt_deg(ax: float, az: float) -> float:
    return math.degrees(math.atan2(ax, az))


def complementary_time_constant(alpha: float, dt: float) -> float:
    return alpha * dt / (1 - alpha)


def simulate_fusion(alpha: float, dt: float = 0.01, seconds: float = 60.0, accel_noise_g: float = 0.02,
                    gyro_bias_dps: float = 0.5, gyro_noise_dps: float = 0.05, seed: int = 1810):
    """Tilt held at 0 deg: estimate it from a noisy accelerometer (per-sample noise in g) and a biased, noisy gyro,
    fused by theta = alpha (theta + omega dt) + (1 - alpha) theta_accel. Returns (rms error of the accelerometer
    alone, final drift of the gyro alone, rms error of the fused estimate over the last half) in degrees."""
    rng = np.random.default_rng(seed)
    n = int(seconds / dt)
    acc = np.degrees(np.arctan2(rng.normal(0, accel_noise_g, n), 1.0))
    gyro = gyro_bias_dps + rng.normal(0, gyro_noise_dps, n)
    theta_g = np.cumsum(gyro * dt)
    fused = np.empty(n)
    th = 0.0
    for k in range(n):
        th = alpha * (th + gyro[k] * dt) + (1 - alpha) * acc[k]
        fused[k] = th
    half = n // 2
    return float(np.sqrt(np.mean(acc ** 2))), float(theta_g[-1]), float(np.sqrt(np.mean(fused[half:] ** 2)))


# ------------------------------------------------------------------ PPG
def beer_lambert(i0: float, eps_c: float, length: float) -> float:
    return i0 * math.exp(-eps_c * length)


def perfusion_index(ac: float, dc: float) -> float:
    return ac / dc


def shot_noise_snr_db(i_photo: float, bandwidth: float, modulation: float) -> float:
    """SNR of the pulsatile (AC) part, of relative size `modulation`, against the shot noise of the whole photocurrent:
    (m I)^2 / (2 q I B)."""
    signal = (modulation * i_photo) ** 2 / 2          # sine of peak m I: power (m I)^2 / 2
    noise = 2 * Q_E * i_photo * bandwidth
    return 10 * math.log10(signal / noise)


def heart_rate_from_signal(x: np.ndarray, fs: float, fmin: float = 0.5, fmax: float = 4.0) -> float:
    """Beats per minute from the largest spectral peak between fmin and fmax (Hann window, zero-padded FFT)."""
    n = len(x)
    nfft = 1 << (int(math.ceil(math.log2(n))) + 3)
    spec = np.abs(np.fft.rfft((x - x.mean()) * np.hanning(n), nfft))
    f = np.fft.rfftfreq(nfft, 1 / fs)
    band = (f >= fmin) & (f <= fmax)
    return float(60 * f[band][np.argmax(spec[band])])


# ------------------------------------------------------------------ microphones
def spl_db(p_rms: float) -> float:
    return 20 * math.log10(p_rms / P_REF)


def pressure_from_spl(spl: float) -> float:
    return P_REF * 10 ** (spl / 20)


def full_scale_spl(sensitivity_dbfs: float, ref_spl: float = 94.0) -> float:
    """A digital microphone giving sensitivity_dbfs at ref_spl reaches 0 dBFS at ref_spl - sensitivity_dbfs."""
    return ref_spl - sensitivity_dbfs


def noise_floor_spl(snr_db: float, ref_spl: float = 94.0) -> float:
    return ref_spl - snr_db


# ------------------------------------------------------------------ barometer
def altitude_m(p: float, p0: float = 101325.0, t0: float = 288.15, lapse: float = 0.0065) -> float:
    """International standard atmosphere, troposphere: h = (T0/L) (1 - (p/p0)^(R L / (g M)))."""
    r, m = 8.314462618, 0.0289644
    return t0 / lapse * (1 - (p / p0) ** (r * lapse / (G0 * m)))


def pressure_gradient_pa_per_m(p: float = 101325.0, t: float = 288.15) -> float:
    """dp/dh = -rho g with rho = p M / (R T)."""
    r, m = 8.314462618, 0.0289644
    return -p * m / (r * t) * G0
