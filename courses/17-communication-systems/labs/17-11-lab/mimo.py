"""MIMO and beamforming toolkit for the 17-11 lab.

- receive diversity: maximal-ratio, equal-gain and selection combining (SNR statistics and BER simulation);
- Alamouti space-time block coding (encoder and linear decoder);
- uniform linear arrays: steering vectors, array factor, half-power beamwidth, first nulls, grating lobes;
- MIMO capacity: equal-power (log det) and water-filling over singular values, ergodic capacity by Monte Carlo
  and, for 2 x 2 i.i.d. Rayleigh, by integrating the Wishart eigenvalue density;
- linear MIMO detectors (zero-forcing and MMSE) with their post-detection SINRs, and BER simulation;
- the 3GPP TS 38.306 approximate maximum data-rate formula.

Channels are complex Gaussian with unit average gain per entry unless stated; rho is the total transmit SNR.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import integrate, optimize, special
from scipy.stats import norm

Q = norm.sf


def crandn(rng, *shape):
    return (rng.standard_normal(shape) + 1j * rng.standard_normal(shape)) / math.sqrt(2)


# ------------------------------------------------------------------ receive diversity
def combine_snr(h, kind):
    """Post-combining SNR gain (multiply by the per-branch SNR) for channel vectors along axis 0."""
    g = np.abs(h) ** 2
    if kind == "mrc":
        return g.sum(axis=0)
    if kind == "sc":
        return g.max(axis=0)
    if kind == "egc":
        return np.abs(h).sum(axis=0) ** 2 / h.shape[0]
    raise ValueError(kind)


def sc_mean_gain(n):
    """Mean SNR of selection combining over n i.i.d. unit-mean exponential branches: sum 1/k."""
    return sum(1 / k for k in range(1, n + 1))


def mrc_outage(x, n):
    """P(sum of n unit exponentials < x) = 1 - e^-x sum_{k<n} x^k/k! (Erlang CDF)."""
    return 1 - math.exp(-x) * sum(x**k / math.factorial(k) for k in range(n))


def sc_outage(x, n):
    return (1 - math.exp(-x)) ** n


def ber_bpsk_mrc(gbar, n):
    mu = math.sqrt(gbar / (1 + gbar))
    return ((1 - mu) / 2) ** n * sum(math.comb(n - 1 + k, k) * ((1 + mu) / 2) ** k for k in range(n))


def simulate_combining(n, gbar_db, kind, nbits, rng):
    """BPSK over n i.i.d. Rayleigh branches with the chosen combiner; returns BER."""
    gbar = 10 ** (gbar_db / 10)
    b = rng.integers(0, 2, nbits)
    h = crandn(rng, n, nbits)
    y = h * (1 - 2 * b) + crandn(rng, n, nbits) / math.sqrt(gbar)
    if kind == "mrc":
        z = np.sum(np.conj(h) * y, axis=0)
    elif kind == "egc":
        z = np.sum(np.exp(-1j * np.angle(h)) * y, axis=0)
    else:
        idx = np.argmax(np.abs(h), axis=0)
        z = np.conj(h[idx, np.arange(nbits)]) * y[idx, np.arange(nbits)]
    return float(np.mean((z.real < 0) != b))


# ------------------------------------------------------------------ Alamouti
def alamouti_encode(s):
    """Pairs (s1, s2) -> two time slots x two antennas: slot 1 sends (s1, s2), slot 2 sends (-s2*, s1*).

    Each antenna transmits at half power so the total stays that of one antenna.
    """
    s = np.asarray(s).reshape(-1, 2)
    x = np.empty((s.shape[0], 2, 2), complex)  # [pair, slot, antenna]
    x[:, 0, 0], x[:, 0, 1] = s[:, 0], s[:, 1]
    x[:, 1, 0], x[:, 1, 1] = -np.conj(s[:, 1]), np.conj(s[:, 0])
    return x / math.sqrt(2)


def alamouti_decode(r1, r2, h1, h2):
    """Linear combining for one receive antenna; returns estimates scaled to (|h1|^2 + |h2|^2)/sqrt(2) s."""
    s1 = np.conj(h1) * r1 + h2 * np.conj(r2)
    s2 = np.conj(h2) * r1 - h1 * np.conj(r2)
    return s1, s2


def simulate_alamouti(gbar_db, npairs, rng):
    """BPSK Alamouti 2 x 1 over i.i.d. Rayleigh (constant over a pair); returns BER."""
    gbar = 10 ** (gbar_db / 10)
    b = rng.integers(0, 2, (npairs, 2))
    s = (1 - 2 * b).astype(complex)
    x = alamouti_encode(s.ravel())
    h = crandn(rng, npairs, 2)
    noise = crandn(rng, npairs, 2) / math.sqrt(gbar)
    r = np.einsum("psa,pa->ps", x, h) + noise
    e1, e2 = alamouti_decode(r[:, 0], r[:, 1], h[:, 0], h[:, 1])
    dec = np.stack([e1.real < 0, e2.real < 0], axis=1)
    return float(np.mean(dec != b))


# ------------------------------------------------------------------ uniform linear arrays
def steering(n, d_over_lambda, theta_deg):
    k = np.arange(n)
    return np.exp(-2j * np.pi * d_over_lambda * k * math.sin(math.radians(theta_deg)))


def array_factor(n, d_over_lambda, theta_deg, steer_deg=0.0):
    """Normalized |AF| (1 at the steering direction) of an n-element ULA with uniform weights."""
    th = np.radians(np.atleast_1d(theta_deg))
    psi = 2 * np.pi * d_over_lambda * (np.sin(th) - math.sin(math.radians(steer_deg)))
    num = np.sin(n * psi / 2)
    den = n * np.sin(psi / 2)
    out = np.ones_like(psi)
    nz = np.abs(den) > 1e-12
    out[nz] = np.abs(num[nz] / den[nz])
    return out


def hpbw_deg(n, d_over_lambda, steer_deg=0.0):
    """Half-power beamwidth found numerically from the array factor."""
    f = lambda t: array_factor(n, d_over_lambda, steer_deg + t, steer_deg)[0] ** 2 - 0.5  # noqa: E731
    hi = optimize.brentq(f, 1e-6, 89.0 - steer_deg if steer_deg >= 0 else 89.0)
    lo = optimize.brentq(lambda t: array_factor(n, d_over_lambda, steer_deg - t, steer_deg)[0] ** 2 - 0.5, 1e-6, 89.0)
    return hi + lo


def first_null_deg(n, d_over_lambda, steer_deg=0.0):
    """Angle of the first null above the beam: sin(theta) = sin(theta0) + 1/(n d/lambda)."""
    return math.degrees(math.asin(math.sin(math.radians(steer_deg)) + 1 / (n * d_over_lambda)))


def grating_free_spacing(scan_deg):
    """Largest element spacing (in wavelengths) with no grating lobe when scanning to scan_deg."""
    return 1 / (1 + math.sin(math.radians(scan_deg)))


# ------------------------------------------------------------------ MIMO capacity
def capacity_equal_power(H, rho):
    """log2 det(I + rho/Nt H H^H) in b/s/Hz (no CSI at the transmitter)."""
    H = np.asarray(H, complex)
    nr, nt = H.shape
    sign, logdet = np.linalg.slogdet(np.eye(nr) + (rho / nt) * H @ H.conj().T)
    return float(logdet / math.log(2))


def capacity_svd(H, rho):
    s = np.linalg.svd(np.asarray(H, complex), compute_uv=False)
    return float(np.sum(np.log2(1 + rho / H.shape[1] * s**2)))


def waterfill(gains, total):
    g = np.asarray(gains, float)
    g = g[g > 1e-15]
    floors = 1 / g
    order = np.argsort(floors)
    for k in range(len(g), 0, -1):
        used = order[:k]
        mu = (total + floors[used].sum()) / k
        if mu > floors[used].max():
            p = np.zeros_like(g)
            p[used] = mu - floors[used]
            return p, float(np.sum(np.log2(1 + g * p)))
    raise ValueError("no allocation")


def capacity_waterfill(H, rho):
    """Capacity with transmitter CSI: water-filling total power rho over the squared singular values."""
    s = np.linalg.svd(np.asarray(H, complex), compute_uv=False)
    return waterfill(s**2, rho)[1]


def ergodic_capacity_mc(nr, nt, rho, trials, rng):
    H = crandn(rng, trials, nr, nt)
    G = np.eye(nr) + (rho / nt) * H @ np.conj(np.transpose(H, (0, 2, 1)))
    return float(np.mean(np.linalg.slogdet(G)[1]) / math.log(2))


def ergodic_siso(rho):
    """E[log2(1 + rho |h|^2)] for Rayleigh fading: log2(e) e^(1/rho) E1(1/rho)."""
    return math.log2(math.e) * math.exp(1 / rho) * special.exp1(1 / rho)


def ergodic_2x2(rho):
    """2 x 2 i.i.d. Rayleigh: 2 * int log2(1 + rho lam / 2) p(lam) d lam with the Wishart marginal
    p(lam) = 0.5 (1 + (1 - lam)^2) e^-lam."""
    f = lambda lam: math.log2(1 + rho * lam / 2) * 0.5 * (1 + (1 - lam) ** 2) * math.exp(-lam)  # noqa: E731
    val, _ = integrate.quad(f, 0, np.inf, limit=200)
    return 2 * val


# ------------------------------------------------------------------ linear detectors
def zf_sinr(H, rho):
    """Per-stream post-detection SNR of zero-forcing with equal power rho/Nt per stream."""
    H = np.asarray(H, complex)
    nt = H.shape[1]
    inv = np.linalg.inv(H.conj().T @ H)
    return (rho / nt) / np.real(np.diag(inv))


def mmse_sinr(H, rho):
    """Per-stream SINR of the linear MMSE detector: 1/[(I + rho/Nt H^H H)^-1]_kk - 1."""
    H = np.asarray(H, complex)
    nt = H.shape[1]
    A = np.linalg.inv(np.eye(nt) + (rho / nt) * H.conj().T @ H)
    return 1 / np.real(np.diag(A)) - 1


def simulate_spatial_mux(nr, nt, rho_db, nvec, rng, detector="zf"):
    """QPSK spatial multiplexing over i.i.d. Rayleigh with a ZF or MMSE detector; returns BER."""
    rho = 10 ** (rho_db / 10)
    bits = rng.integers(0, 2, (nvec, nt, 2))
    s = ((1 - 2 * bits[..., 0]) + 1j * (1 - 2 * bits[..., 1])) / math.sqrt(2)
    H = crandn(rng, nvec, nr, nt)
    y = np.einsum("vrt,vt->vr", H, s) * math.sqrt(rho / nt) + crandn(rng, nvec, nr)
    Hh = np.conj(np.transpose(H, (0, 2, 1)))
    if detector == "zf":
        W = np.linalg.inv(Hh @ H) @ Hh
    else:
        W = np.linalg.inv(Hh @ H + (nt / rho) * np.eye(nt)) @ Hh
    est = np.einsum("vtr,vr->vt", W, y)
    dec = np.stack([est.real < 0, est.imag < 0], axis=-1)
    return float(np.mean(dec != bits))


# ------------------------------------------------------------------ NR maximum data rate (TS 38.306 4.1.2)
def nr_max_rate_mbps(layers, qm, nrb, mu, oh, f=1.0, rmax=948 / 1024):
    """1e-6 * v * Qm * f * Rmax * (NRB * 12 / Ts) * (1 - OH), Ts = 1e-3 / (14 * 2^mu)."""
    ts = 1e-3 / (14 * 2**mu)
    return 1e-6 * layers * qm * f * rmax * (nrb * 12 / ts) * (1 - oh)
