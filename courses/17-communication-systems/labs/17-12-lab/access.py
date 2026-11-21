"""Multiple-access and system-level toolkit for the 17-12 lab.

- channel counts for FDMA/TDMA and the single-cell CDMA capacity estimate;
- hexagonal frequency-reuse geometry and first-tier signal-to-interference ratio;
- ALOHA and slotted-ALOHA throughput, analytic and simulated;
- a slotted random-access model of CSMA/CA (per-slot attempt probability), with simulation;
- Erlang B blocking and the channels needed for a target grade of service;
- schedulers (round robin, max-SNR, proportional fair) over Rayleigh-fading users, with Jain's fairness index;
- HARQ throughput with independent retransmissions.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import integrate, optimize


# ------------------------------------------------------------------ FDMA / TDMA / CDMA
def fdma_tdma_users(bandwidth_hz, channel_hz, slots):
    return int(bandwidth_hz // channel_hz) * slots


def cdma_processing_gain(chip_or_bw_hz, bit_rate):
    return chip_or_bw_hz / bit_rate


def cdma_users(gain, ebi0_db, activity=1.0, other_cell=0.0):
    """Single-cell uplink with perfect power control: N = 1 + G / (Eb/I0) / (activity (1 + other_cell))."""
    return 1 + gain / (10 ** (ebi0_db / 10)) / (activity * (1 + other_cell))


# ------------------------------------------------------------------ cellular reuse
def reuse_distance_ratio(n_cluster):
    """D/R = sqrt(3N) for hexagonal cells with cluster size N."""
    return math.sqrt(3 * n_cluster)


def sir_first_tier(n_cluster, path_exp, interferers=6):
    """Worst-case-free estimate SIR = (D/R)^n / i0 (all first-tier interferers at distance D)."""
    return reuse_distance_ratio(n_cluster) ** path_exp / interferers


def valid_cluster_sizes(limit=30):
    """N = i^2 + i j + j^2 for non-negative integers i, j."""
    out = set()
    for i in range(0, 8):
        for j in range(0, 8):
            n = i * i + i * j + j * j
            if 0 < n <= limit:
                out.add(n)
    return sorted(out)


# ------------------------------------------------------------------ random access
def aloha(G):
    return G * math.exp(-2 * G)


def slotted_aloha(G):
    return G * math.exp(-G)


def simulate_slotted_aloha(G, nslots, rng):
    """Poisson arrivals of mean G per slot; a slot succeeds if exactly one packet is sent."""
    k = rng.poisson(G, nslots)
    return float(np.mean(k == 1))


def simulate_pure_aloha(G, npkts, rng):
    """Poisson packet starts at rate G per packet time; success if no other start within +-1 packet time."""
    t = np.sort(rng.uniform(0, npkts / G, npkts))
    gaps = np.diff(t)
    ok = np.ones(npkts, bool)
    ok[1:] &= gaps >= 1
    ok[:-1] &= gaps >= 1
    return float(np.sum(ok) / (npkts / G))


def slot_outcomes(n, tau):
    """Per slot with n stations each transmitting with probability tau: (idle, success, collision)."""
    idle = (1 - tau) ** n
    succ = n * tau * (1 - tau) ** (n - 1)
    return idle, succ, 1 - idle - succ


def tau_from_window(w):
    """Attempt probability per slot for a uniform backoff in [0, w - 1] with no collisions: 2/(w + 1)."""
    return 2 / (w + 1)


def simulate_slots(n, tau, nslots, rng):
    k = rng.binomial(n, tau, nslots)
    return float(np.mean(k == 0)), float(np.mean(k == 1)), float(np.mean(k >= 2))


# ------------------------------------------------------------------ Erlang B
def erlang_b(c, a):
    """Blocking probability for c channels and offered traffic a (Erlangs), by the stable recursion."""
    b = 1.0
    for k in range(1, c + 1):
        b = a * b / (k + a * b)
    return b


def channels_for(a, target):
    c = 1
    while erlang_b(c, a) > target:
        c += 1
    return c


# ------------------------------------------------------------------ scheduling
def ergodic_rayleigh(snr):
    """E[log2(1 + snr X)] for X ~ Exp(1)."""
    from scipy import special

    return math.log2(math.e) * math.exp(1 / snr) * special.exp1(1 / snr)


def max_snr_capacity(snr, k):
    """E[log2(1 + snr * max of k unit exponentials)], by integrating against the max's density."""
    f = lambda x: math.log2(1 + snr * x) * k * math.exp(-x) * (1 - math.exp(-x)) ** (k - 1)  # noqa: E731
    val, _ = integrate.quad(f, 0, np.inf, limit=200)
    return val


def simulate_schedulers(mean_snr_db, nslots, rng, tc=100.0):
    """Users with possibly different mean SNRs (dB list) and i.i.d. Rayleigh per slot.

    Returns {scheduler: per-user average throughput (b/s/Hz)} for round robin, max-SNR and
    proportional fair (time constant tc slots).
    """
    snr = 10 ** (np.asarray(mean_snr_db) / 10)
    k = len(snr)
    g = rng.exponential(1.0, (nslots, k)) * snr
    r = np.log2(1 + g)
    out = {}
    rr = np.zeros(k)
    for t in range(nslots):
        rr[t % k] += r[t, t % k]
    out["rr"] = rr / nslots
    mx = np.zeros(k)
    win = np.argmax(r, axis=1)
    np.add.at(mx, win, r[np.arange(nslots), win])
    out["max"] = mx / nslots
    pf = np.zeros(k)
    avg = np.full(k, 1e-3)
    for t in range(nslots):
        u = int(np.argmax(r[t] / avg))
        pf[u] += r[t, u]
        served = np.zeros(k)
        served[u] = r[t, u]
        avg = (1 - 1 / tc) * avg + (1 / tc) * served
    out["pf"] = pf / nslots
    return out


def jain(x):
    x = np.asarray(x, float)
    return float(x.sum() ** 2 / (len(x) * np.sum(x**2)))


# ------------------------------------------------------------------ HARQ
def harq_throughput(p_err, max_tx):
    """Normalized throughput and residual error for independent retransmissions (no combining gain)."""
    expected_tx = sum(p_err**k for k in range(max_tx))
    residual = p_err**max_tx
    return (1 - residual) / expected_tx, residual


def harq_rtt_slots_needed(rtt_slots):
    """Stop-and-wait HARQ processes needed to keep the link busy: one per slot of round-trip time."""
    return rtt_slots
