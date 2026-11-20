#!/usr/bin/env python3
"""Figures for chapter 13-06 (reflection and transmission of waves).

Run from anywhere:  python assets/figures/src/fig_13_06.py
Outputs SVGs to assets/figures/13-06/:
- fresnel.svg: TE and TM power reflectance against angle of incidence, from air into glass (n = 1.5) and from
  glass into air, with the Brewster and critical angles marked.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/13-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def reflectances(n1, n2, th):
    s = n1 * np.sin(th) / n2
    ct = np.sqrt((1 - s**2).astype(complex))
    ci = np.cos(th)
    rte = (n1 * ci - n2 * ct) / (n1 * ci + n2 * ct)
    rtm = (n1 * ct - n2 * ci) / (n1 * ct + n2 * ci)
    return np.abs(rte) ** 2, np.abs(rtm) ** 2


def fig_fresnel():
    th = np.radians(np.linspace(0, 89.9, 1000))
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.3), sharey=True)
    for ax, (n1, n2, title) in zip(axes, ((1.0, 1.5, "air → glass"), (1.5, 1.0, "glass → air"))):
        rte, rtm = reflectances(n1, n2, th)
        ax.plot(np.degrees(th), rte, color=PALETTE[0], lw=1.7, label="TE (s)")
        ax.plot(np.degrees(th), rtm, color=PALETTE[1], lw=1.7, label="TM (p)")
        tb = math.degrees(math.atan(n2 / n1))
        ax.axvline(tb, color="0.5", lw=0.8, ls=":")
        ax.text(tb + 1 if n1 < n2 else tb - 14, 0.55 if n1 < n2 else 0.35, f"Brewster\n{tb:.1f}°", fontsize=7)
        if n1 > n2:
            tc = math.degrees(math.asin(n2 / n1))
            ax.axvline(tc, color="0.3", lw=0.8, ls="--")
            ax.text(tc + 1, 0.8, f"critical\n{tc:.1f}°", fontsize=7)
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("angle of incidence (°)")
        ax.set_xlim(0, 90)
        ax.legend(fontsize=7, loc="upper left")
    axes[0].set_ylabel("reflected power fraction")
    fig.tight_layout()
    save(fig, f"{OUT}/fresnel.svg")


if __name__ == "__main__":
    fig_fresnel()
