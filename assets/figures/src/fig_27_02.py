#!/usr/bin/env python3
"""Figures for chapter 27-02 (the smartphone SoC).

Run from anywhere:  python assets/figures/src/fig_27_02.py
Outputs
  assets/figures/27-02/core-energy.svg  left: energy per instruction against performance for the big and little
                                        cores of Example 27-02.2 (assumed parameters), crossing at 4.0 GIPS;
                                        right: big-core energy per instruction against frequency at 0.10 W and
                                        0.6 W leakage, with the minimum-energy points of Example 27-02.3
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "27-system-architectures" / "labs" / "27-02-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import socmodel as s  # noqa: E402

OUT = "assets/figures/27-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

BIG = dict(ipc=6.0, c=1.2, v0=0.45, k=0.12, ps=0.10, f_max=4.2)
LIT = dict(ipc=2.5, c=0.22, v0=0.45, k=0.30, ps=0.02, f_max=2.4)


def main() -> None:
    fig, ax = plt.subplots(1, 2, figsize=(9.6, 3.6))
    perf = np.linspace(0.3, 6.0, 400)
    ax[0].plot(perf, [s.epi_at_perf(p, BIG) for p in perf], color=PALETTE[0], label="big core")
    ax[0].plot(perf, [s.epi_at_perf(p, LIT) for p in perf], color=PALETTE[1], label="little core")
    x = s.crossover_gips(BIG, LIT)
    y = s.epi_at_perf(x, BIG)
    ax[0].plot([x], [y], "ko", ms=4)
    ax[0].annotate(f"crossover\n{x:.2f} GIPS", (x, y), textcoords="offset points", xytext=(-70, 20), fontsize=8)
    ax[0].set_xlabel("performance (GIPS)")
    ax[0].set_ylabel("energy per instruction (nJ)")
    ax[0].set_ylim(0, 0.2)
    ax[0].set_title("Small cores win at low performance")
    ax[0].legend(loc="upper right")

    f = np.linspace(0.15, 4.2, 400)
    for k, ps in enumerate((0.10, 0.6)):
        core = dict(BIG, ps=ps)
        ax[1].plot(f, [s.epi_nj(x_, core["c"], core["v0"], core["k"], core["ipc"], ps) for x_ in f],
                   color=PALETTE[k], label=f"leakage {ps:g} W")
        fs = s.f_min_energy(core)
        es = s.epi_nj(fs, core["c"], core["v0"], core["k"], core["ipc"], ps)
        ax[1].plot([fs], [es], "o", color=PALETTE[k], ms=4)
        ax[1].annotate(f"{fs:.2f} GHz", (fs, es), textcoords="offset points", xytext=(4, -14), fontsize=8)
    ax[1].set_xlabel("frequency (GHz)")
    ax[1].set_ylabel("energy per instruction (nJ)")
    ax[1].set_ylim(0, 0.4)
    ax[1].set_title("Leakage moves the minimum-energy point up")
    ax[1].legend(loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/core-energy.svg")


if __name__ == "__main__":
    main()
