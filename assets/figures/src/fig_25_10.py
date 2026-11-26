#!/usr/bin/env python3
"""Figures for chapter 25-10 (qualification and functional safety).

Run from anywhere:  python assets/figures/src/fig_25_10.py
Outputs
  assets/figures/25-10/fmeda-metrics.svg  SPFM against lockstep diagnostic coverage and LFM against self-test
                                          coverage for Example 25-10.4's element, with ASIL B/C/D thresholds
  assets/figures/25-10/htol-coverage.svg  stress hours at 125 and 150 C needed to cover the AM625 automotive
                                          mission profile (R-604) against activation energy, with a 1,000 h line
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "25-fabrication-packaging-test-and-reliability" / "labs" / "25-10-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import qual as q  # noqa: E402

OUT = "assets/figures/25-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def metrics() -> None:
    dc = np.linspace(0.90, 0.999, 100)
    cov = np.linspace(0.0, 0.99, 100)
    fig, ax = plt.subplots(1, 2, figsize=(8.0, 3.4))
    ax[0].plot(100 * dc, [100 * q.fmeda(200, 80, d, 20, 0.9)["spfm"] for d in dc], color=PALETTE[0])
    for thr, lab in ((97, "C"), (99, "D")):
        ax[0].axhline(thr, color="0.6", ls=":", lw=1)
        ax[0].text(90.2, thr + 0.1, f"ASIL {lab}", fontsize=7)
    ax[0].set_xlabel("lockstep diagnostic coverage (%)")
    ax[0].set_ylabel("SPFM (%)")
    ax[0].set_ylim(94, 100)
    ax[1].plot(100 * cov, [100 * q.fmeda(200, 80, 0.99, 20, c)["lfm"] for c in cov], color=PALETTE[1])
    for thr, lab in ((80, "C"), (90, "D")):
        ax[1].axhline(thr, color="0.6", ls=":", lw=1)
        ax[1].text(1, thr + 0.2, f"ASIL {lab}", fontsize=7)
    ax[1].set_xlabel("self-test coverage of the checker (%)")
    ax[1].set_ylabel("LFM (%)")
    for a in ax:
        a.grid(True, alpha=0.3)
    save(fig, f"{OUT}/fmeda-metrics.svg")


def htol() -> None:
    prof = [(-40, 0.05), (70, 0.65), (110, 0.20), (125, 0.10)]
    ea = np.linspace(0.4, 1.0, 60)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    for ts, col in ((125, PALETTE[0]), (150, PALETTE[1])):
        ax.semilogy(ea, [q.profile_stress_hours(prof, 20000, e, ts) for e in ea], color=col, label=f"stress at {ts} °C")
    ax.axhline(1000, color="k", ls=":", lw=1)
    ax.text(0.41, 1100, "1,000 h HTOL", fontsize=8)
    ax.set_xlabel("activation energy (eV)")
    ax.set_ylabel("stress hours to cover the profile")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    save(fig, f"{OUT}/htol-coverage.svg")


if __name__ == "__main__":
    metrics()
    htol()
