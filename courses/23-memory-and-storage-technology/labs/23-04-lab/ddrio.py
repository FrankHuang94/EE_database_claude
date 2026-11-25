"""Models for chapter 23-04: DRAM interfaces (DDR, LPDDR and GDDR).

Closed forms for the chapter's examples: prefetch and access granularity, bandwidth, pseudo-open-drain and
low-voltage-swing termination power, data bus inversion, transmission-line reflections, fly-by skew, the pulse
response of a first-order channel with and without decision-feedback equalization, and multilevel (PAM) signaling.
The verify script recomputes the published numbers by other routes. SI units unless a name says otherwise.
"""
from __future__ import annotations

import math
from itertools import product

C0 = 299_792_458.0  # speed of light (m/s)


# ---------------------------------------------------------------- prefetch, granularity, bandwidth
def core_column_rate(data_rate: float, prefetch: int) -> float:
    """Column accesses per second the DRAM core must sustain for one pin at data_rate (transfers/s)."""
    return data_rate / prefetch


def access_bytes(width_bits: int, burst_length: int) -> float:
    """Bytes moved by one burst on a channel of width_bits."""
    return width_bits * burst_length / 8


def bandwidth(data_rate: float, width_bits: int) -> float:
    """Peak bytes per second of a bus: transfers/s × bits per transfer / 8."""
    return data_rate * width_bits / 8


def unit_interval(data_rate: float) -> float:
    return 1.0 / data_rate


# ---------------------------------------------------------------- termination power
def pod_low(vddq: float, r_on: float, r_tt: float) -> tuple[float, float, float]:
    """Pseudo-open-drain driver pulling low against termination to VDDQ: (low voltage, current, power)."""
    i = vddq / (r_on + r_tt)
    return vddq - i * r_tt, i, vddq * i


def lvstl_high(vddq: float, r_on: float, r_tt: float) -> tuple[float, float, float]:
    """Low-voltage-swing driver pulling high against termination to ground: (high voltage, current, power)."""
    i = vddq / (r_on + r_tt)
    return i * r_tt, i, vddq * i


def energy_per_bit(p_active: float, data_rate: float, active_fraction: float) -> float:
    """Average termination energy per bit when the static current flows for active_fraction of the bits."""
    return p_active / data_rate * active_fraction


def dbi_zeros_per_byte() -> float:
    """Expected low wires per byte (8 data + DBI) for random data with DDR4-style DBI (invert if more than four 0s)."""
    total = 0
    for bits in product((0, 1), repeat=8):
        zeros = bits.count(0)
        total += zeros if zeros <= 4 else (8 - zeros) + 1  # inverted data plus a low DBI_n
    return total / 256


# ---------------------------------------------------------------- transmission lines and skew
def launched_wave(v_s: float, r_s: float, z0: float) -> float:
    return v_s * z0 / (r_s + z0)


def gamma(r: float, z0: float) -> float:
    """Reflection coefficient of a resistive termination (r = inf for an open end)."""
    if math.isinf(r):
        return 1.0
    return (r - z0) / (r + z0)


def far_end_arrivals(v_s: float, r_s: float, z0: float, r_l: float, n: int = 3) -> list[float]:
    """Far-end voltage after each of the first n arrivals of a step (lattice diagram)."""
    vp = launched_wave(v_s, r_s, z0)
    gl, gs = gamma(r_l, z0), gamma(r_s, z0)
    out, v, wave = [], 0.0, vp
    for _ in range(n):
        v += wave * (1 + gl)
        out.append(v)
        wave *= gl * gs
    return out


def delay_per_mm(eps_eff: float) -> float:
    """Propagation delay per millimetre (s/mm) for an effective relative permittivity."""
    return math.sqrt(eps_eff) / C0 * 1e-3


# ---------------------------------------------------------------- channel, ISI and DFE
def rc_cursors(ui: float, tau: float, n: int = 6) -> list[float]:
    """Samples, one UI apart, of a first-order channel's response to a one-UI pulse of unit height.

    h0 = 1 - a and h_k = (1 - a) a^k, with a = exp(-UI/tau); the post-cursors sum to a.
    """
    a = math.exp(-ui / tau)
    return [(1 - a)] + [(1 - a) * a ** k for k in range(1, n)]


def worst_eye(h0: float, post: float, levels: int = 2) -> float:
    """Worst-case vertical opening of each eye, as a fraction of the full swing, for PAM-M with ISI sum `post`."""
    return h0 / (levels - 1) - post


def pam_symbol_rate(bit_rate: float, bits_per_symbol: float) -> float:
    return bit_rate / bits_per_symbol


def pam_penalty_db(levels: int) -> float:
    """Eye-height penalty of PAM-M against NRZ at the same swing (dB)."""
    return 20 * math.log10(levels - 1)


def loss_amplitude(loss_db: float) -> float:
    return 10 ** (-loss_db / 20)
