"""Lab 21-10 helpers: patch antennas, the Chu limit, linear and planar arrays, beam squint, phase quantization,
EIRP scaling, beamforming-architecture power and millimetre-wave links. SI units unless a name says otherwise."""
from __future__ import annotations

import math

import numpy as np

C0 = 299_792_458.0


# ---------------------------------------------------------------- patch antenna (transmission-line model)
def patch_design(f0, eps_r, h):
    """Rectangular patch on a substrate of permittivity eps_r and thickness h (Hammerstad/Balanis
    transmission-line model). Returns (W, eps_eff, dL, L) in metres."""
    w = C0 / (2 * f0) * math.sqrt(2 / (eps_r + 1))
    e_eff = (eps_r + 1) / 2 + (eps_r - 1) / 2 / math.sqrt(1 + 12 * h / w)
    dl = 0.412 * h * (e_eff + 0.3) * (w / h + 0.264) / ((e_eff - 0.258) * (w / h + 0.8))
    length = C0 / (2 * f0 * math.sqrt(e_eff)) - 2 * dl
    return w, e_eff, dl, length


# ---------------------------------------------------------------- small antennas
def chu_q(ka):
    """Lower bound on the radiation Q of a linearly polarized antenna inside a sphere of radius a (McLean form)."""
    return 1 / ka ** 3 + 1 / ka


def bandwidth_from_q(q, vswr=2.0):
    """Fractional bandwidth within which a single-resonance antenna, matched at centre, stays below vswr."""
    return (vswr - 1) / (q * math.sqrt(vswr))


# ---------------------------------------------------------------- arrays
def array_factor(theta_deg, n, d_lambda, theta0_deg, f_ratio=1.0, mode="phase"):
    """Normalized |AF| of an n-element linear array (spacing d_lambda wavelengths at the design frequency),
    steered to theta0 at the design frequency, evaluated at f = f_ratio * f0. mode 'phase': fixed phase
    shifters set at f0 (beam squints); 'ttd': true-time delay (no squint)."""
    th = np.radians(np.asarray(theta_deg, dtype=float))
    s0 = math.sin(math.radians(theta0_deg))
    k = np.arange(n)
    geo = 2 * np.pi * d_lambda * f_ratio * np.multiply.outer(np.sin(th), k)
    comp = 2 * np.pi * d_lambda * (f_ratio if mode == "ttd" else 1.0) * s0 * k
    return np.abs(np.exp(1j * (geo - comp)).sum(axis=-1)) / n


def planar_af(theta_deg, phi_deg, nx, ny, dx, dy, theta0_deg=0.0, phi0_deg=0.0):
    """|AF| of an nx-by-ny rectangular array (spacings in wavelengths), steered to (theta0, phi0)."""
    th, ph = np.radians(theta_deg), np.radians(phi_deg)
    t0, p0 = math.radians(theta0_deg), math.radians(phi0_deg)
    u = np.sin(th) * np.cos(ph) - math.sin(t0) * math.cos(p0)
    v = np.sin(th) * np.sin(ph) - math.sin(t0) * math.sin(p0)

    def one(n, d, w):
        psi = 2 * np.pi * d * w
        with np.errstate(invalid="ignore", divide="ignore"):
            r = np.sin(n * psi / 2) / (n * np.sin(psi / 2))
        return np.where(np.abs(np.sin(psi / 2)) < 1e-12, 1.0, np.abs(r))
    return one(nx, dx, u) * one(ny, dy, v)


def squint_angle_deg(f_ratio, theta0_deg):
    """Beam direction of a phase-shifter array steered to theta0 at f0, at frequency f_ratio * f0."""
    return math.degrees(math.asin(math.sin(math.radians(theta0_deg)) / f_ratio))


def squint_bandwidth(n, d_lambda, theta0_deg, exact=True):
    """Fractional bandwidth over which the gain toward theta0 stays within 3 dB of its peak (phase shifters).
    exact=False returns the large-N formula 0.886 / (n d sin theta0)."""
    if not exact:
        x = 1.39156  # sin(x)/x = 1/sqrt(2)
        return 2 * (2 * x / n) / (2 * np.pi * d_lambda * math.sin(math.radians(theta0_deg)))
    from scipy.optimize import brentq
    g = lambda fr: array_factor([theta0_deg], n, d_lambda, theta0_deg, fr)[0] - 1 / math.sqrt(2)  # noqa: E731
    return brentq(g, 1 + 1e-9, 1.5) - brentq(g, 0.5, 1 - 1e-9)


def max_scan_no_grating_deg(d_lambda):
    s = 1 / d_lambda - 1
    return 90.0 if s >= 1 else math.degrees(math.asin(s))


def hpbw_deg(n, d_lambda, theta0_deg=0.0):
    """Half-power beamwidth found numerically from the array factor."""
    th = np.linspace(theta0_deg - 60, theta0_deg + 60, 240001)
    th = th[(th > -90) & (th < 90)]
    af = array_factor(th, n, d_lambda, theta0_deg)
    above = th[af >= 1 / math.sqrt(2)]
    return above.max() - above.min()


# ---------------------------------------------------------------- phase quantization
def quantization_gain_loss_db(bits):
    """Average gain loss from uniformly distributed phase errors of +/- pi/2^bits (large array)."""
    x = math.pi / 2 ** bits
    return -20 * math.log10(math.sin(x) / x)


def quantization_rms_deg(bits):
    return 180 / 2 ** bits / math.sqrt(3)


# ---------------------------------------------------------------- EIRP and power
def eirp_dbm(n, p_elem_dbm, g_elem_dbi):
    """N elements each radiating p_elem: N times the power and N times the gain."""
    return p_elem_dbm + g_elem_dbi + 20 * math.log10(n)


def dc_power_w(n, eirp_w, g_elem, eta, p_overhead_w):
    """DC power of an n-element transmit array delivering eirp_w (linear), with PA efficiency eta and a fixed
    per-element overhead."""
    return eirp_w / (n * g_elem * eta) + n * p_overhead_w


def optimal_elements(eirp_w, g_elem, eta, p_overhead_w):
    return math.sqrt(eirp_w / (g_elem * eta * p_overhead_w))


def adc_power_w(fom_j, enob, fs):
    """Walden figure of merit: P = FoM * 2^ENOB * fs."""
    return fom_j * 2 ** enob * fs


# ---------------------------------------------------------------- links
def fspl_db(f, r):
    return 20 * math.log10(4 * math.pi * r * f / C0)


def noise_floor_dbm(bw_hz, nf_db):
    return -174 + 10 * math.log10(bw_hz) + nf_db


def quantization_monte_carlo(n, bits, theta0_deg=20.0, trials=4000, seed=1):
    """Steer an n-element lambda/2 array to theta0 with b-bit phase shifters, each element carrying a random
    calibration offset so that rounding errors are decorrelated. Returns (mean peak gain relative to ideal, mean
    power at the first null of the ideal pattern relative to the ideal peak)."""
    rng = np.random.default_rng(seed)
    k = np.arange(n)
    s0 = math.sin(math.radians(theta0_deg))
    want = -np.pi * k * s0                         # ideal steering phase for d = lambda/2
    step = 2 * np.pi / 2 ** bits
    s_null = s0 + 2.0 / n                          # first null: sin(theta) = sin(theta0) + lambda/(N d)
    peak, null = 0.0, 0.0
    for _ in range(trials):
        off = rng.uniform(0, 2 * np.pi, n)        # unknown offset each element's calibration absorbs
        applied = np.round((want + off) / step) * step - off
        peak += abs(np.exp(1j * (np.pi * k * s0 + applied)).sum()) ** 2 / n ** 2
        null += abs(np.exp(1j * (np.pi * k * s_null + applied)).sum()) ** 2 / n ** 2
    return peak / trials, null / trials
