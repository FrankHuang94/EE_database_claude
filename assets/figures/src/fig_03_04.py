#!/usr/bin/env python3
"""Figures for chapter 03-04 (joint distributions, correlation and the CLT).

Run:  python assets/figures/src/fig_03_04.py  -> assets/figures/03-04/*.svg
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom, norm, poisson

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

use_style()
OUT = "assets/figures/03-04"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def irwin_hall_pdf(x, n):
    """Density of the sum of n independent U(0, 1)."""
    x = np.asarray(x, float)
    out = np.zeros_like(x)
    for k in range(n + 1):
        out += (-1) ** k * math.comb(n, k) * np.where(x > k, (x - k) ** (n - 1), 0.0)
    return np.where((x >= 0) & (x <= n), out / math.factorial(n - 1), 0.0)


def irwin_hall_sf(x, n):
    """P(S > x), computed from the upper end (few terms, no cancellation in the tail)."""
    y = n - np.asarray(x, float)               # P(S > x) = P(S < n - x) by symmetry
    out = np.zeros_like(y)
    for k in range(n + 1):
        out += (-1) ** k * math.comb(n, k) * np.where(y > k, (y - k) ** n, 0.0)
    return np.clip(out / math.factorial(n), 0, 1)


def fig_clt():
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.0))
    z = np.linspace(-4, 4, 800)
    axes[0].plot(z, norm.pdf(z), color="k", lw=2.2, label="N(0, 1)")
    for n, c in ((1, P), (2, G), (3, O), (12, B)):
        s = math.sqrt(n / 12)                  # standard deviation of the sum
        x = n / 2 + s * z
        axes[0].plot(z, irwin_hall_pdf(x, n) * s, color=c, lw=1.4, ls="--" if n == 12 else "-", label=f"sum of {n} uniforms")
    axes[0].set_xlabel("standardized sum (S − nμ)/(σ√n)")
    axes[0].set_ylabel("density")
    axes[0].set_title("Convolution smooths: sums of uniforms approach a Gaussian", fontsize=10)
    axes[0].legend(fontsize=7)
    zz = np.linspace(0, 6.5, 600)
    axes[1].semilogy(zz, norm.sf(zz), color="k", lw=2.2, label="Q(z)")
    for n, c in ((3, O), (12, B)):
        s = math.sqrt(n / 12)
        tail = irwin_hall_sf(n / 2 + s * zz, n)
        axes[1].semilogy(zz, np.maximum(tail, 1e-30), color=c, lw=1.4, label=f"sum of {n} uniforms")
    axes[1].set_ylim(1e-12, 1)
    axes[1].set_xlabel("z (standard deviations)")
    axes[1].set_ylabel("P(standardized sum > z)")
    axes[1].set_title("…but not in the far tail: a bounded sum stops at √(3n)", fontsize=10)
    axes[1].legend(fontsize=7, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/clt-uniform.svg")


def fig_bivariate():
    rng = np.random.default_rng(7)
    fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.8), sharex=True, sharey=True)
    for ax, rho in zip(axes, (0.0, 0.8, -0.5)):
        x = rng.standard_normal(1500)
        y = rho * x + math.sqrt(1 - rho**2) * rng.standard_normal(1500)
        ax.plot(x, y, ".", color=B, ms=2, alpha=0.5)
        xx = np.linspace(-3.5, 3.5, 2)
        ax.plot(xx, rho * xx, color=O, lw=2, label="E[Y | X = x] = ρx")
        t = np.linspace(0, 2 * np.pi, 300)
        for r in (1, 2):                       # contours of equal density
            u, w = r * np.cos(t), r * np.sin(t)
            ax.plot(u, rho * u + math.sqrt(1 - rho**2) * w, color="0.3", lw=0.8)
        ax.set_title(f"ρ = {rho:g}", fontsize=10)
        ax.set_xlim(-3.5, 3.5)
        ax.set_ylim(-3.5, 3.5)
        ax.set_aspect("equal")
        ax.set_xlabel("x")
    axes[0].set_ylabel("y")
    axes[1].legend(fontsize=7, loc="upper left")
    fig.suptitle("Jointly Gaussian pairs with unit variances: correlation tilts and squeezes the cloud", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/bivariate-gaussian.svg")


def fig_fec():
    n, t, m = 544, 15, 10
    ber = np.logspace(-5, math.log10(3e-3), 300)
    ser = -np.expm1(m * np.log1p(-ber))
    lam = n * ser
    exact = binom.sf(t, n, ser)
    pois = poisson.sf(t, lam)
    gauss = norm.sf((t + 0.5 - lam) / np.sqrt(n * ser * (1 - ser)))
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    ax.loglog(ber, exact, color=B, lw=2.2, label="exact binomial")
    ax.loglog(ber, pois, color=G, lw=1.4, ls="--", label="Poisson approximation")
    ax.loglog(ber, np.maximum(gauss, 1e-60), color=O, lw=1.4, label="Gaussian (CLT) approximation")
    for b in (2.4e-4, 3.8e-4):
        s = -math.expm1(m * math.log1p(-b))
        ax.plot([b], [binom.sf(t, n, s)], "o", color="k", ms=4)
    ax.annotate("2.4×10⁻⁴: 8.2×10⁻¹³", (2.4e-4, binom.sf(t, n, -math.expm1(m * math.log1p(-2.4e-4)))),
                xytext=(-120, -10), textcoords="offset points", fontsize=8)
    ax.set_ylim(1e-40, 1)
    ax.set_xlabel("pre-FEC bit error ratio (random errors)")
    ax.set_ylabel("uncorrectable codeword ratio")
    ax.set_title("RS(544,514), t = 15: the CLT badly underestimates the far tail", fontsize=10)
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/fec-tail.svg")


if __name__ == "__main__":
    fig_clt()
    fig_bivariate()
    fig_fec()
