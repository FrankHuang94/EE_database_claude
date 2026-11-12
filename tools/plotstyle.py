"""Shared Matplotlib style for every committed figure and lab plot.

Usage (figure scripts and notebooks):
    from plotstyle import use_style, save
    use_style()
    ...
    save(fig, "assets/figures/02-01/complex-plane.svg")

Figures use a white background so they read correctly in both GitHub light and
dark themes, SI units on every axis label, and a colorblind-safe palette.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]

# Okabe–Ito colorblind-safe palette
PALETTE = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#F0E442", "#000000"]


def use_style() -> None:
    mpl.rcParams.update({
        "figure.figsize": (6.4, 4.0),
        "figure.dpi": 110,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "axes.grid": True,
        "grid.alpha": 0.3,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": mpl.cycler(color=PALETTE),
        "font.size": 10,
        "axes.titlesize": 11,
        "legend.frameon": False,
        "lines.linewidth": 1.8,
        "svg.fonttype": "path",
        "svg.hashsalt": "self-taught-bsee",  # deterministic SVG output
    })


def save(fig, relpath: str) -> Path:
    """Save a figure relative to the repo root (creating folders) and close it."""
    out = ROOT / relpath
    out.parent.mkdir(parents=True, exist_ok=True)
    meta = {"Date": None} if out.suffix == ".svg" else {}
    fig.savefig(out, bbox_inches="tight", metadata=meta)
    plt.close(fig)
    return out
