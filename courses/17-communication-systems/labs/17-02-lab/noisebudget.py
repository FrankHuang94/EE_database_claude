"""Noise budgets and calibrated AWGN: helpers for the 17-02 lab.

- decibel conversions, kTB, noise figure <-> noise temperature, Planck's correction;
- lossy passive components and Friis cascades (with each stage's contribution);
- receiver sensitivity and the SNR / Es/N0 / Eb/N0 / C/N0 conversions;
- a calibrated AWGN generator that sets the noise variance per sample from Eb/N0, the samples per bit
  and whether the signal is real or complex, and simulations that use it (BPSK error rate, spreading gain,
  a time-domain noisy cascade).

Conventions: N0 is the one-sided noise density (W/Hz); powers in dBm are relative to 1 mW; T0 = 290 K.
"""
from __future__ import annotations

import math

import numpy as np

K_B = 1.380649e-23  # J/K, exact (SI 2019)
H_PLANCK = 6.62607015e-34  # J s, exact
T0 = 290.0  # K, IEEE/ITU-R reference temperature


# ------------------------------------------------------------------ decibels
def db(x):
    """Power ratio to dB."""
    return 10 * np.log10(x)


def undb(d):
    """dB to power ratio."""
    return 10 ** (np.asarray(d, dtype=float) / 10)


def dbm(p_watts):
    """Power in W to dBm."""
    return 10 * np.log10(np.asarray(p_watts, dtype=float) / 1e-3)


def watts(p_dbm):
    """Power in dBm to W."""
    return 1e-3 * 10 ** (np.asarray(p_dbm, dtype=float) / 10)


def add_dbm(*levels):
    """Sum of independent powers given in dBm (convert, add, convert back)."""
    return float(dbm(sum(watts(x) for x in levels)))


# ------------------------------------------------------------------ thermal noise
def ktb_dbm(bandwidth_hz, temp_k=T0):
    """Available thermal noise power kTB in dBm."""
    return float(dbm(K_B * temp_k * bandwidth_hz))


def vn_rms(r_ohm, bandwidth_hz, temp_k=T0):
    """Open-circuit rms thermal noise voltage sqrt(4 k T R B)."""
    return math.sqrt(4 * K_B * temp_k * r_ohm * bandwidth_hz)


def planck_factor(f_hz, temp_k):
    """Planck's available noise power per hertz divided by kT: x / (e^x - 1), x = h f / k T."""
    x = H_PLANCK * f_hz / (K_B * temp_k)
    return x / math.expm1(x)


# ------------------------------------------------------------------ noise figure and temperature
def te_from_nf(nf_db):
    """Equivalent noise temperature (K) from a noise figure (dB): (F - 1) T0."""
    return (10 ** (nf_db / 10) - 1) * T0


def nf_from_te(te_k):
    """Noise figure (dB) from an equivalent noise temperature (K): 10 log10(1 + Te/T0)."""
    return 10 * math.log10(1 + te_k / T0)


def lossy(loss_db, temp_k=T0):
    """Matched passive loss L at physical temperature T: returns (noise factor, Te, available gain)."""
    L = 10 ** (loss_db / 10)
    te = (L - 1) * temp_k
    return 1 + te / T0, te, 1 / L


def friis(stages):
    """Cascade of stages given as (noise factor F, available gain G) in linear units.

    Returns (F_total, contributions) where contributions[i] is stage i's term in the Friis sum
    (F_1 for the first stage, (F_i - 1)/(G_1...G_{i-1}) for the others).
    """
    contrib, g = [], 1.0
    for i, (f, gain) in enumerate(stages):
        contrib.append(f if i == 0 else (f - 1) / g)
        g *= gain
    return sum(contrib), contrib


def friis_db(stages_db):
    """Friis cascade from (NF dB, gain dB) pairs; returns (NF_total dB, Te_total K, contributions)."""
    f, c = friis([(10 ** (nf / 10), 10 ** (g / 10)) for nf, g in stages_db])
    return 10 * math.log10(f), (f - 1) * T0, c


def cascade_te(temps, gains):
    """Cascade noise temperature by the stage-by-stage recursion T = T1 + T2/G1 + ... (temps in K, gains linear)."""
    total, g = 0.0, 1.0
    for t, gain in zip(temps, gains):
        total += t / g
        g *= gain
    return total


def noise_measure(nf_db, gain_db):
    """Noise measure M = (F - 1)/(1 - 1/G): the stage with the smaller M should come first."""
    f, g = 10 ** (nf_db / 10), 10 ** (gain_db / 10)
    return (f - 1) / (1 - 1 / g)


# ------------------------------------------------------------------ link figures of merit
def sensitivity_dbm(bw_hz, nf_db, snr_db, im_db=0.0, diversity_db=0.0, kt_dbm_hz=-174.0):
    """P = kT + 10 log10(BW) + NF + SNR + IM - diversity gain (dBm); 3GPP uses kT = -174 dBm/Hz."""
    return kt_dbm_hz + 10 * math.log10(bw_hz) + nf_db + snr_db + im_db - diversity_db


def ebn0_from_snr(snr_db, noise_bw_hz, bit_rate):
    """Eb/N0 (dB) from an SNR measured in noise bandwidth B_N: SNR + 10 log10(B_N / R_b)."""
    return snr_db + 10 * math.log10(noise_bw_hz / bit_rate)


def cn0_dbhz(p_dbm, t_sys_k):
    """Carrier-to-noise-density ratio (dB-Hz) for received power p_dbm and system temperature t_sys_k."""
    return p_dbm - float(dbm(K_B * t_sys_k))


def shannon_ebn0_db(eta):
    """Minimum Eb/N0 (dB) for reliable communication at spectral efficiency eta (b/s/Hz): (2^eta - 1)/eta."""
    return 10 * math.log10((2 ** eta - 1) / eta)


# ------------------------------------------------------------------ calibrated AWGN
def noise_sigma(ebn0_db, energy_per_bit, complex_signal=False):
    """Noise standard deviation per sample (per real component) for a given Eb/N0.

    energy_per_bit is the sum of |sample|^2 over one bit (unit sample spacing). With unit sample
    spacing, white noise of one-sided density N0 has variance N0/2 per real sample, and N0/2 in each
    of I and Q for complex samples (total N0 per complex sample): the energy-preserving complex
    normalization of 17-01 §3.9, in which signal energy is the sum of |sample|^2. The result is the same
    for real and complex signals; `complex_signal` is accepted only so callers can say which they mean.
    """
    n0 = energy_per_bit / 10 ** (ebn0_db / 10)
    return math.sqrt(n0 / 2)


def awgn(shape, ebn0_db, energy_per_bit, rng, complex_signal=False):
    """Gaussian noise samples calibrated to Eb/N0 (real or circularly symmetric complex)."""
    s = noise_sigma(ebn0_db, energy_per_bit, complex_signal)
    if complex_signal:
        return s * (rng.standard_normal(shape) + 1j * rng.standard_normal(shape))
    return s * rng.standard_normal(shape)


def bpsk_ber_sim(ebn0_db, sps, nbits, rng, per_sample_snr_mistake=False):
    """BPSK with rectangular +-1 pulses, sps samples per bit, sample-sum detector.

    With per_sample_snr_mistake=True the noise is (wrongly) set so the per-sample SNR equals Eb/N0.
    Returns the measured bit-error rate.
    """
    bits = rng.integers(0, 2, nbits)
    x = np.repeat(2.0 * bits - 1.0, sps)
    if per_sample_snr_mistake:
        sigma = math.sqrt(1 / 10 ** (ebn0_db / 10))
    else:
        sigma = noise_sigma(ebn0_db, float(sps))
    r = x + sigma * rng.standard_normal(x.size)
    decided = r.reshape(nbits, sps).sum(axis=1) > 0
    return float(np.mean(decided != bits.astype(bool)))


def despread_snr(snr_chip_db, nchips, nsym, rng):
    """Spread +-1 symbols with a random +-1 code of nchips chips, add noise at the per-chip SNR,
    correlate, and return (measured per-chip SNR dB, measured post-correlation SNR dB)."""
    code = rng.choice([-1.0, 1.0], nchips)
    sym = rng.choice([-1.0, 1.0], nsym)
    tx = np.outer(sym, code)
    sigma = math.sqrt(10 ** (-snr_chip_db / 10))
    noise = sigma * rng.standard_normal(tx.shape)
    rx = tx + noise
    y = rx @ code  # correlate each symbol period with the code
    sig = nchips * sym
    snr_out = np.mean(sig ** 2) / np.var(y - sig)
    snr_in = np.mean(tx ** 2) / np.var(noise)
    return 10 * math.log10(snr_in), 10 * math.log10(snr_out)


def cascade_sim(stages, n, rng, t_source=T0, signal_rms=1e-3):
    """Time-domain model of a noisy cascade: each stage (Te in K, available power gain G) adds independent
    white noise of variance k Te (per unit bandwidth, unit sample spacing) at its input, then amplifies.

    A sine of known rms rides on source noise of variance k t_source. Returns the measured noise factor
    (input SNR over output SNR) using the known signal and the separately tracked noise.
    """
    sig = signal_rms * math.sqrt(2) * np.sin(2 * math.pi * 0.01 * np.arange(n))
    noise = math.sqrt(K_B * t_source) * rng.standard_normal(n)
    snr_in = np.mean(sig ** 2) / np.mean(noise ** 2)
    for te, g in stages:
        noise = noise + math.sqrt(K_B * te) * rng.standard_normal(n)
        sig, noise = sig * math.sqrt(g), noise * math.sqrt(g)
    snr_out = np.mean(sig ** 2) / np.mean(noise ** 2)
    return snr_in / snr_out
