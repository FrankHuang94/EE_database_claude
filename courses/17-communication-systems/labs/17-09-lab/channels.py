"""Wireless channel toolkit for the 17-09 lab.

- free-space loss (Friis and the ITU-R P.525 form), the two-ray ground-reflection model, log-distance loss;
- 3GPP TR 38.901 UMi-Street Canyon path loss (LOS/NLOS) and shadow-fading margins;
- power-delay-profile statistics, frequency correlation and coherence bandwidth;
- Doppler, the Clarke/Jakes autocorrelation, coherence time, level-crossing rate and fade duration;
- Rayleigh and Rician fading generators (sum of sinusoids) and outage probabilities;
- average BPSK error rates in Rayleigh fading, with L-branch maximal-ratio combining.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import optimize, special
from scipy.stats import ncx2, norm

C = 299_792_458.0  # m/s
C_3GPP = 3.0e8  # TR 38.901 uses c = 3.0e8 m/s in its breakpoint formula


# ------------------------------------------------------------------ path loss
def fspl_db(f_hz, d_m):
    """Free-space path loss 20 log10(4 pi d / lambda) between isotropic antennas."""
    return 20 * math.log10(4 * math.pi * d_m * f_hz / C)


def fspl_p525_db(f_mhz, d_km):
    """ITU-R P.525-5 eq. (6): 32.4 + 20 log10 f(MHz) + 20 log10 d(km)."""
    return 32.4 + 20 * math.log10(f_mhz) + 20 * math.log10(d_km)


def friis_pr_dbm(pt_dbm, gt_dbi, gr_dbi, f_hz, d_m):
    return pt_dbm + gt_dbi + gr_dbi - fspl_db(f_hz, d_m)


def two_ray_loss_db(d, ht, hr, f_hz, gamma=-1.0):
    """Direct plus ground-reflected ray (reflection coefficient gamma), isotropic antennas."""
    lam = C / f_hz
    d1 = math.hypot(d, ht - hr)
    d2 = math.hypot(d, ht + hr)
    k = 2 * math.pi / lam
    field = np.exp(-1j * k * d1) / d1 + gamma * np.exp(-1j * k * d2) / d2
    return -20 * math.log10(abs(field) * lam / (4 * math.pi))


def two_ray_breakpoint(ht, hr, f_hz):
    """Distance beyond which the two-ray loss grows as d^4: 4 ht hr / lambda."""
    return 4 * ht * hr * f_hz / C


def log_distance_db(d, d0, pl0_db, n):
    return pl0_db + 10 * n * math.log10(d / d0)


def umi_breakpoint(h_bs=10.0, h_ut=1.5, fc_ghz=3.5, h_e=1.0):
    """TR 38.901 note 1: d'BP = 4 h'BS h'UT fc / c with h' = h - hE (hE = 1 m for UMi)."""
    return 4 * (h_bs - h_e) * (h_ut - h_e) * fc_ghz * 1e9 / C_3GPP


def umi_los_db(d2d, fc_ghz, h_bs=10.0, h_ut=1.5):
    """TR 38.901 Table 7.4.1-1, UMi-Street Canyon LOS (fc in GHz, distances in m)."""
    d3d = math.hypot(d2d, h_bs - h_ut)
    dbp = umi_breakpoint(h_bs, h_ut, fc_ghz)
    if d2d <= dbp:
        return 32.4 + 21 * math.log10(d3d) + 20 * math.log10(fc_ghz)
    return 32.4 + 40 * math.log10(d3d) + 20 * math.log10(fc_ghz) - 9.5 * math.log10(dbp**2 + (h_bs - h_ut) ** 2)


def umi_nlos_db(d2d, fc_ghz, h_bs=10.0, h_ut=1.5):
    """UMi-Street Canyon NLOS: max(LOS, 35.3 log10 d3D + 22.4 + 21.3 log10 fc - 0.3 (hUT - 1.5))."""
    d3d = math.hypot(d2d, h_bs - h_ut)
    nlos = 35.3 * math.log10(d3d) + 22.4 + 21.3 * math.log10(fc_ghz) - 0.3 * (h_ut - 1.5)
    return max(umi_los_db(d2d, fc_ghz, h_bs, h_ut), nlos)


def shadow_margin_db(sigma_db, coverage):
    """Margin so that a lognormal shadowed link meets its budget with the given probability."""
    return sigma_db * norm.isf(1 - coverage)


# ------------------------------------------------------------------ delay spread
def pdp_stats(delays, powers_db):
    """Mean excess delay and rms delay spread of a discrete power-delay profile."""
    t = np.asarray(delays, float)
    p = 10 ** (np.asarray(powers_db, float) / 10)
    mean = np.sum(p * t) / np.sum(p)
    rms = math.sqrt(np.sum(p * t**2) / np.sum(p) - mean**2)
    return mean, rms


def freq_correlation(delays, powers_db, df):
    """|R(df)| / R(0): magnitude of the frequency correlation of the channel response."""
    t = np.asarray(delays, float)
    p = 10 ** (np.asarray(powers_db, float) / 10)
    return abs(np.sum(p * np.exp(-2j * np.pi * df * t))) / np.sum(p)


def coherence_bandwidth(delays, powers_db, level=0.5):
    """Smallest frequency separation at which the correlation falls to `level`."""
    _, rms = pdp_stats(delays, powers_db)
    grid = np.linspace(1e-6, 5, 50001) / rms
    vals = np.array([freq_correlation(delays, powers_db, f) for f in grid])
    i = int(np.argmax(vals <= level))
    return optimize.brentq(lambda f: freq_correlation(delays, powers_db, f) - level, grid[i - 1], grid[i])


def exp_pdp_coherence_bw(tau_rms, level=0.5):
    """Exponential PDP: |R| = 1/sqrt(1 + (2 pi df tau)^2) gives df = sqrt(1/level^2 - 1)/(2 pi tau)."""
    return math.sqrt(1 / level**2 - 1) / (2 * math.pi * tau_rms)


def lognormal_ds_median(mu_lg):
    """TR 38.901 gives lgDS = log10(DS / 1 s); the median of DS is 10**mu."""
    return 10**mu_lg


# ------------------------------------------------------------------ Doppler and time variation
def doppler_hz(v_mps, f_hz):
    return v_mps * f_hz / C


def jakes_corr(tau, fd):
    """Clarke/Jakes autocorrelation of the complex gain: J0(2 pi fd tau)."""
    return special.j0(2 * np.pi * fd * np.asarray(tau, float))


def coherence_time(fd, level=0.5):
    x = optimize.brentq(lambda x: special.j0(x) - level, 0.1, 2.4)
    return x / (2 * math.pi * fd)


def lcr(rho, fd):
    """Level-crossing rate (crossings per second, one direction) at rho = threshold / rms envelope."""
    return math.sqrt(2 * math.pi) * fd * rho * math.exp(-rho * rho)


def afd(rho, fd):
    """Average fade duration below rho: P(r < rho) / lcr."""
    return (math.exp(rho * rho) - 1) / (math.sqrt(2 * math.pi) * fd * rho)


def rayleigh_sos(n, fd, fs, rng, m=64, k_factor=0.0):
    """Unit-power complex fading by a sum of m sinusoids with random angles and phases (Clarke model).

    k_factor > 0 adds a fixed line-of-sight component (Rician); total mean power stays 1.
    """
    t = np.arange(n) / fs
    alpha = rng.uniform(0, 2 * np.pi, m)
    phi = rng.uniform(0, 2 * np.pi, m)
    h = np.exp(1j * (2 * np.pi * fd * np.cos(alpha)[:, None] * t[None, :] + phi[:, None])).sum(axis=0) / math.sqrt(m)
    if k_factor > 0:
        h = math.sqrt(k_factor / (k_factor + 1)) + math.sqrt(1 / (k_factor + 1)) * h
    return h


# ------------------------------------------------------------------ outage and error rates
def rayleigh_outage(margin_db):
    """P(instantaneous power < mean - margin) for Rayleigh fading: 1 - exp(-10^(-margin/10))."""
    return -math.expm1(-(10 ** (-margin_db / 10)))


def rician_outage(margin_db, k_factor):
    """Same with a Rician K-factor: noncentral chi-square with 2 degrees of freedom."""
    x = 10 ** (-margin_db / 10)
    # power = |LOS + scatter|^2 with scatter variance 1/(K+1) split over two dimensions
    scale = 1 / (2 * (k_factor + 1))
    return float(ncx2.cdf(x / scale, 2, k_factor / (k_factor + 1) / scale))


def ber_bpsk_rayleigh(gbar):
    """Average BPSK error rate over Rayleigh fading with mean Eb/N0 gbar (linear)."""
    mu = math.sqrt(gbar / (1 + gbar))
    return 0.5 * (1 - mu)


def ber_bpsk_mrc(gbar, L):
    """L-branch maximal-ratio combining, i.i.d. Rayleigh branches, mean Eb/N0 gbar per branch."""
    mu = math.sqrt(gbar / (1 + gbar))
    return ((1 - mu) / 2) ** L * sum(math.comb(L - 1 + k, k) * ((1 + mu) / 2) ** k for k in range(L))


def required_db(fn, target, lo=-10.0, hi=80.0):
    return optimize.brentq(lambda x: fn(10 ** (x / 10)) - target, lo, hi, xtol=1e-12)
