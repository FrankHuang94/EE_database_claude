"""Foundry and PDK models for lab 25-05.

Corner delays with the alpha-power law and a Monte Carlo of global and local threshold variation;
FD-SOI back-gate coupling from the series-capacitor formula and from a numerical 1-D Laplace solve
through the gate-oxide / silicon / BOX stack; shuttle against dedicated cost; die-area migration.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.stats import norm

EPS_OX, EPS_SI = 3.9, 11.7


def delay(v: float, vt: float, alpha: float = 1.3) -> float:
    return v / (v - vt) ** alpha


def corner_ratio(v_nom: float, vt_nom: float, dv_frac: float, dvt: float, alpha: float = 1.3) -> tuple[float, float]:
    """(slow, fast) delay relative to typical."""
    tt = delay(v_nom, vt_nom, alpha)
    ss = delay(v_nom * (1 - dv_frac), vt_nom + dvt, alpha)
    ff = delay(v_nom * (1 + dv_frac), vt_nom - dvt, alpha)
    return ss / tt, ff / tt


def simulate_vt(sigma_global: float, sigma_local: float, n: int = 100_000, seed: int = 1) -> np.ndarray:
    """Threshold shifts (V) of n critical paths: one global draw per die plus a local draw per path."""
    rng = np.random.default_rng(seed)
    return rng.normal(0, sigma_global, n) + rng.normal(0, sigma_local, n)


def fraction_beyond(threshold: float, sigma_global: float, sigma_local: float) -> float:
    return float(norm.sf(threshold / math.hypot(sigma_global, sigma_local)))


def coupling_formula(t_ox: float, t_si: float, t_box: float) -> float:
    c_ox, c_si, c_box = EPS_OX / t_ox, EPS_SI / t_si, EPS_OX / t_box
    return c_si * c_box / (c_ox * (c_si + c_box))


def coupling_numerical(t_ox: float, t_si: float, t_box: float, n_per_nm: int = 20) -> float:
    """Solve d/dx(eps dphi/dx) = 0 on a grid (front gate | oxide | silicon | BOX | back gate) for the
    front-surface potential with (V_G, V_BG) = (1, 0) and (0, 1); the coupling is the ratio of the two
    sensitivities (keep the front surface fixed: dV_G/dV_BG)."""
    layers = [(t_ox, EPS_OX), (t_si, EPS_SI), (t_box, EPS_OX)]
    eps = np.concatenate([np.full(max(2, int(round(t * n_per_nm))), e) for t, e in layers])
    n = len(eps) + 1
    edges = np.concatenate([[0.0], np.cumsum([t / max(2, int(round(t * n_per_nm))) for t, _ in layers
                                             for _ in range(max(2, int(round(t * n_per_nm))))])])
    surface = max(2, int(round(t_ox * n_per_nm)))     # node index of the oxide/silicon interface

    def solve(vg: float, vbg: float) -> float:
        a = np.zeros((n, n))
        b = np.zeros(n)
        a[0, 0] = 1.0
        b[0] = vg
        a[-1, -1] = 1.0
        b[-1] = vbg
        for i in range(1, n - 1):
            gl = eps[i - 1] / (edges[i] - edges[i - 1])
            gr = eps[i] / (edges[i + 1] - edges[i])
            a[i, i - 1], a[i, i], a[i, i + 1] = gl, -(gl + gr), gr
        return float(np.linalg.solve(a, b)[surface])

    s_g = solve(1.0, 0.0)
    s_bg = solve(0.0, 1.0)
    return s_bg / s_g


def mpw_cost(area_mm2: float, price_per_mm2: float, min_area: float) -> float:
    return max(area_mm2, min_area) * price_per_mm2


def break_even_area(mask_cost: float, price_per_mm2: float) -> float:
    return mask_cost / price_per_mm2


def migrated_area(digital: float, nvm: float, analog: float, k_dig: float = 3.0, k_nvm: float = 2.5,
                  k_ana: float = 1.2) -> float:
    return digital / k_dig + nvm / k_nvm + analog / k_ana
