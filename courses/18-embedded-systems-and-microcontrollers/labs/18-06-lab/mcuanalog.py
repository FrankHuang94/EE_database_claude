"""Lab 18-06: models of an MCU's analog interfaces.

- ADC: ideal rounding quantizer, LSB, quantization noise, SQNR and ENOB;
- sampling: settling of the sample-and-hold capacitor, the largest source resistance for a sampling time, the
  charge-sharing step with an external capacitor, and a period-by-period model of a multiplexed input whose
  sample-and-hold capacitor arrives at another channel's voltage (the equilibrium sampling error);
- oversampling: averaging M samples of a noisy input through the quantizer (Monte Carlo, own generator);
- DAC: zero-order-hold droop and image amplitudes;
- PWM as a DAC: the exact steady-state ripple of a square wave through a first-order RC filter, its small-T/tau
  approximation, the filter needed for a ripple target, settling time, and a step-by-step exact simulation.
"""
from __future__ import annotations

import math

import numpy as np


# ------------------------------------------------------------------ ADC transfer function
def lsb(v_ref: float, bits: int) -> float:
    return v_ref / 2 ** bits


def adc_code(v_in, v_ref: float, bits: int):
    """Ideal converter: rounds to the nearest code (transitions at (k - 1/2) LSB), clipped to 0 .. 2^N - 1."""
    code = np.floor(np.asarray(v_in, dtype=float) / lsb(v_ref, bits) + 0.5)
    return np.clip(code, 0, 2 ** bits - 1).astype(int)


def quantization_noise_rms(v_ref: float, bits: int) -> float:
    return lsb(v_ref, bits) / math.sqrt(12)


def sqnr_db(bits: int) -> float:
    """Full-scale sine against uniform quantization noise: 6.02 N + 1.76 dB."""
    return 20 * math.log10(2 ** bits * math.sqrt(1.5))


def enob(sinad_db: float) -> float:
    return (sinad_db - 10 * math.log10(1.5)) / (20 * math.log10(2))


def sinad_from_enob(n_eff: float) -> float:
    return 20 * math.log10(2 ** n_eff * math.sqrt(1.5))


# ------------------------------------------------------------------ sampling
def settle_time(r_total: float, c_sh: float, bits: int, frac_lsb: float = 0.5) -> float:
    """Time for a full-scale step on C_sh to settle within frac_lsb of an LSB: tau * ln(2^N / frac_lsb)."""
    return r_total * c_sh * math.log(2 ** bits / frac_lsb)


def rs_max(t_sample: float, c_sh: float, r_switch: float, bits: int, frac_lsb: float = 0.5) -> float:
    return t_sample / (c_sh * math.log(2 ** bits / frac_lsb)) - r_switch


def charge_share_step(v_step: float, c_sh: float, c_ext: float) -> float:
    """Drop of an external capacitor at v when an empty-of-signal C_sh (at v - v_step) is connected."""
    return v_step * c_sh / (c_sh + c_ext)


def c_ext_min(c_sh: float, bits: int, frac_lsb: float = 0.5) -> float:
    """External capacitor for a full-scale charge-sharing step below frac_lsb of an LSB."""
    return c_sh * (2 ** bits / frac_lsb - 1)


def mux_equilibrium(v_in: float, r_s: float, c_ext: float, c_sh: float, f_sample: float, v_other: float = 0.0):
    """Steady state of a source (v_in, r_s) with an external capacitor, sampled at f_sample by a C_sh that arrives
    each time at v_other. Charge sharing is instantaneous (the acquisition is much shorter than r_s c_ext); between
    samples c_ext recovers towards v_in with tau = r_s c_ext. Returns (voltage on c_ext before a sample, sampled
    voltage)."""
    a = c_ext / (c_ext + c_sh)
    b = c_sh / (c_ext + c_sh)
    e = math.exp(-1 / (f_sample * r_s * c_ext))
    # x' = v_in + (a x + b v_other - v_in) e, fixed point:
    x = (v_in * (1 - e) + b * v_other * e) / (1 - a * e)
    return x, a * x + b * v_other


def mux_error_approx(v_in: float, r_s: float, c_sh: float, f_sample: float, v_other: float = 0.0) -> float:
    """Average-current model: C_sh acts as a resistor 1/(f C_sh) to v_other."""
    g = r_s * f_sample * c_sh
    return (v_in - v_other) * g / (1 + g)


# ------------------------------------------------------------------ oversampling
def averaged_code(v_in: float, sigma_lsb: float, m: int, v_ref: float = 1.0, bits: int = 12, trials: int = 2000,
                  seed: int = 1806):
    """Monte Carlo: average m quantized samples of v_in plus Gaussian noise (sigma in LSB). Returns the estimates
    (in LSB) for each trial."""
    rng = np.random.default_rng(seed)
    q = lsb(v_ref, bits)
    noise = rng.normal(0.0, sigma_lsb * q, size=(trials, m))
    codes = adc_code(v_in + noise, v_ref, bits)
    return codes.mean(axis=1)


def extra_bits(m: int) -> float:
    """Resolution gained by averaging m samples of white noise: (1/2) log2 m."""
    return 0.5 * math.log2(m)


# ------------------------------------------------------------------ DAC
def zoh_gain(f: float, f_s: float) -> float:
    """|sinc(f / f_s)| of a zero-order hold, sinc(x) = sin(pi x)/(pi x)."""
    x = f / f_s
    return 1.0 if x == 0 else abs(math.sin(math.pi * x) / (math.pi * x))


# ------------------------------------------------------------------ PWM as a DAC
def pwm_ripple_exact(v_high: float, duty: float, period: float, tau: float) -> float:
    """Steady-state peak-to-peak ripple of a 0 / v_high square wave through R-C (tau = RC)."""
    a, b, c = math.exp(-duty * period / tau), math.exp(-(1 - duty) * period / tau), math.exp(-period / tau)
    return v_high * (1 - a) * (1 - b) / (1 - c)


def pwm_ripple_approx(v_high: float, duty: float, period: float, tau: float) -> float:
    return v_high * duty * (1 - duty) * period / tau


def pwm_tau_for_ripple(v_high: float, period: float, ripple: float) -> float:
    """Smallest tau for worst-case (D = 1/2) approximate ripple at most `ripple`."""
    return v_high * period / (4 * ripple)


def pwm_simulate(v_high: float, duty: float, period: float, tau: float, n_periods: int, v0: float = 0.0,
                 points_per_phase: int = 50):
    """Exact piecewise-exponential response of the RC filter, sampled within each phase. Returns (t, v)."""
    ts, vs = [], []
    v, t = v0, 0.0
    for _ in range(n_periods):
        for level, dur in ((v_high, duty * period), (0.0, (1 - duty) * period)):
            if dur <= 0:
                continue
            tt = np.linspace(0, dur, points_per_phase, endpoint=False)
            ts.append(t + tt)
            vs.append(level + (v - level) * np.exp(-tt / tau))
            v = level + (v - level) * math.exp(-dur / tau)
            t += dur
    return np.concatenate(ts), np.concatenate(vs)
