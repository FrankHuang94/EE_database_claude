"""Models for chapter 23-08: emerging memories (MRAM, PCM, ReRAM, FeRAM).

Closed forms for the chapter's examples: magnetic-tunnel-junction read margins, thermal stability and array
retention, spin-transfer-torque write energy, phase-change heating, quench and resistance drift, the conductance
quantum of a ReRAM filament, ferroelectric switched charge and bitline signal, and the FeFET memory window. The
verify script recomputes the published numbers by other routes. SI units unless a name says otherwise.
"""
from __future__ import annotations

import math

Q_E = 1.602176634e-19
H_PLANCK = 6.62607015e-34


# ---------------------------------------------------------------- MRAM
def r_antiparallel(r_p: float, tmr: float) -> float:
    """Antiparallel resistance from the parallel resistance and TMR = (R_AP - R_P)/R_P."""
    return r_p * (1 + tmr)


def read_currents(v_read: float, r_p: float, r_ap: float, r_series: float = 0.0) -> tuple[float, float]:
    return v_read / (r_p + r_series), v_read / (r_ap + r_series)


def delta_required(n_bits: float, t_s: float, f0: float = 1e9, expected_flips: float = 1.0) -> float:
    """Thermal stability factor so that n_bits held for t_s see at most expected_flips flips (Neel-Arrhenius)."""
    return math.log(n_bits * t_s * f0 / expected_flips)


def delta_at(delta_ref: float, t_ref_c: float, t_c: float) -> float:
    """Delta = E_b/(k T) rescaled to another temperature, assuming a temperature-independent barrier."""
    return delta_ref * (t_ref_c + 273.15) / (t_c + 273.15)


def retention_time(delta: float, f0: float = 1e9) -> float:
    """Mean time for one bit to flip thermally, tau = exp(Delta)/f0."""
    return math.exp(delta) / f0


def write_energy(v: float, i: float, t: float) -> float:
    return v * i * t


# ---------------------------------------------------------------- PCM
def joule_power(i: float, r: float) -> float:
    return i * i * r


def thermal_rise(power: float, r_th: float) -> float:
    return power * r_th


def cooling_time(tau: float, dt_start: float, dt_end: float) -> float:
    """Time for an exponential cool-down from a rise dt_start to dt_end."""
    return tau * math.log(dt_start / dt_end)


def drift(r0: float, t: float, t0: float = 1.0, nu: float = 0.1) -> float:
    """Amorphous-state resistance drift R(t) = R0 (t/t0)^nu."""
    return r0 * (t / t0) ** nu


# ---------------------------------------------------------------- ReRAM
def conductance_quantum() -> float:
    """G0 = 2 e^2 / h (siemens)."""
    return 2 * Q_E ** 2 / H_PLANCK


# ---------------------------------------------------------------- FeRAM and FeFET
def switched_charge(p_r: float, area: float) -> float:
    """Charge released when a ferroelectric capacitor's polarization reverses: 2 P_r A."""
    return 2 * p_r * area


def bitline_signal(charge: float, c_bitline: float) -> float:
    return charge / c_bitline


def fefet_window(e_c: float, t_fe: float) -> float:
    """First-order FeFET memory window, about 2 E_c t_FE."""
    return 2 * e_c * t_fe
