"""Lab 22-05 helpers: magnetic circuits, gapped-core energy, core loss, winding loss and design equations.

SI units throughout (m, m², m³, T, A, H, Ω·m, W). Fringing is neglected unless a function says otherwise.
"""
from __future__ import annotations

import math

MU0 = 4e-7 * math.pi          # H/m; the pre-2019 exact value, within 1e-9 of the measured one
RHO_CU_20 = 1.0 / 58e6        # Ω·m, annealed copper at 20 °C (IEC 60028: 1/58 Ω·mm²/m)
ALPHA_CU = 0.00393            # 1/K, its temperature coefficient near 20 °C


# ---------------------------------------------------------------- magnetic circuit
def reluctance(length, area, mu_r=1.0):
    return length / (mu_r * MU0 * area)


def gapped_inductance(n, area, l_core, mu_r, gap, gap_area=None):
    """N²/(R_core + R_gap). gap_area defaults to the core area (no fringing)."""
    r = reluctance(l_core, area, mu_r) + reluctance(gap, gap_area or area)
    return n * n / r


def effective_permeability(mu_r, l_core, gap):
    return mu_r / (1 + mu_r * gap / l_core)


def gap_for_inductance(l_target, n, area, l_core, mu_r):
    """Gap length that gives l_target with n turns (no fringing)."""
    return MU0 * area * (n * n / l_target - l_core / (mu_r * MU0 * area))


def fringed_gap_area(a, b, gap):
    """First-order fringing: each side of a rectangular a×b centre leg grows by the gap length."""
    return (a + gap) * (b + gap)


# ---------------------------------------------------------------- energy and saturation
def peak_flux_density(l_ind, i_pk, n, area):
    """B = λ/(N A) = L I/(N A)."""
    return l_ind * i_pk / (n * area)


def gap_energy_fraction(mu_r, l_core, gap):
    return 1 / (1 + l_core / (mu_r * gap))


def max_energy(b_max, area, l_core, mu_r, gap):
    """Energy at B = b_max: B² A (g + l_c/µr)/(2 µ0)."""
    return b_max ** 2 * area * (gap + l_core / mu_r) / (2 * MU0)


def turns_for(l_ind, i_pk, b_max, area):
    return l_ind * i_pk / (b_max * area)


# ---------------------------------------------------------------- core loss
def steinmetz(k, alpha, beta, f, b_pk):
    """Sinusoidal-excitation loss density k f^α B_pk^β (units follow k)."""
    return k * f ** alpha * b_pk ** beta


def igse_ki(k, alpha, beta, n=20000):
    """k_i of the improved generalized Steinmetz equation (Venkatachalam et al. 2002)."""
    h = 2 * math.pi / n
    integral = sum(abs(math.cos((j + 0.5) * h)) ** alpha for j in range(n)) * h
    return k / ((2 * math.pi) ** (alpha - 1) * integral * 2 ** (beta - alpha))


def igse_triangle(k, alpha, beta, f, delta_b, d):
    """iGSE loss density for a triangular flux of peak-to-peak delta_b, rising for a fraction d of the period."""
    ki = igse_ki(k, alpha, beta)
    return ki * delta_b ** beta * f ** alpha * (d ** (1 - alpha) + (1 - d) ** (1 - alpha))


def eddy_loss_lamination(f, b_pk, thickness, rho):
    """Classical eddy-current loss density of a thin lamination under sinusoidal B: π² f² B² t²/(6ρ)."""
    return math.pi ** 2 * f ** 2 * b_pk ** 2 * thickness ** 2 / (6 * rho)


# ---------------------------------------------------------------- winding loss
def rho_cu(temp_c):
    return RHO_CU_20 * (1 + ALPHA_CU * (temp_c - 20))


def skin_depth(f, rho, mu_r=1.0):
    return math.sqrt(rho / (math.pi * f * mu_r * MU0))


def winding_resistance(n, mlt, wire_area, rho):
    return rho * n * mlt / wire_area


def dowell_fr(delta, layers):
    """Dowell's AC-to-DC resistance ratio for `layers` layers of foil (or equivalent) of thickness delta·δ."""
    d = delta
    xi1 = (math.sinh(2 * d) + math.sin(2 * d)) / (math.cosh(2 * d) - math.cos(2 * d))
    xi2 = (math.sinh(d) - math.sin(d)) / (math.cosh(d) + math.cos(d))
    return d * (xi1 + 2 * (layers ** 2 - 1) / 3 * xi2)


def dowell_fr_low(delta, layers):
    """Small-Δ expansion: 1 + (5M² − 1)Δ⁴/45."""
    return 1 + (5 * layers ** 2 - 1) * delta ** 4 / 45


# ---------------------------------------------------------------- design methods
def area_product(l_ind, i_pk, i_rms, ku, j, b_max):
    """A_e·A_w ≥ L I_pk I_rms/(K_u J B_max), m⁴."""
    return l_ind * i_pk * i_rms / (ku * j * b_max)


def kg_required(rho, l_ind, i_pk, i_rms, b_max, p_cu, ku):
    """Erickson's core geometrical constant K_g = A_e² W_A/MLT ≥ ρ L² I_pk² I_rms²/(B_max² P_cu K_u), m⁵."""
    return rho * l_ind ** 2 * i_pk ** 2 * i_rms ** 2 / (b_max ** 2 * p_cu * ku)


def kg_of_core(area, window, mlt):
    return area ** 2 * window / mlt


def optimum_flux_swing(core_coeff, beta, cu_coeff):
    """Minimize a·B^β + b/B²: B_opt = (2b/(β a))^(1/(β+2)); at the optimum P_core/P_cu = 2/β."""
    return (2 * cu_coeff / (beta * core_coeff)) ** (1 / (beta + 2))


def leakage_inductance(n, mlt, breadth, h_p, h_s, d):
    """Two-layer-section winding: µ0 N² MLT (h_p/3 + d + h_s/3)/b_w."""
    return MU0 * n * n * mlt * (h_p / 3 + d + h_s / 3) / breadth


def leakage_interleaved(n, mlt, breadth, h_p, h_s, d):
    """P/2–S–P/2 interleaving: µ0 N² MLT (h_p/12 + d/2 + h_s/12)/b_w."""
    return MU0 * n * n * mlt * (h_p / 12 + d / 2 + h_s / 12) / breadth
