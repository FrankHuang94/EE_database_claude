#!/usr/bin/env python3
"""Figures for chapter 26-04 (engineering economics II).

Run from anywhere:  python assets/figures/src/fig_26_04.py
Outputs
  assets/figures/26-04/sourcing-breakevens.svg  left: present cost of licensing ($6 M + $0.80/unit) and
                                                building ($24 M + 25% x $15 M slip) the PHY of Example 26-04.2
                                                against the discounted unit stream, with the plan and the
                                                break-even marked; right: break-even fleet of Example
                                                26-04.5's custom accelerator against the merchant price
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "26-engineering-design-and-professional-practice" / "labs" / "26-04-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import sourcing as s  # noqa: E402

OUT = "assets/figures/26-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def main() -> None:
    units = [3, 5, 5, 3]
    U = s.discounted_units(units, 0.12)
    build = s.build_pv(24.0, 0.25, 15.0)
    ustar = s.breakeven_discounted_units(build, 6.0, 0.80)
    u = np.linspace(0, 40, 201)
    fig, ax = plt.subplots(1, 2, figsize=(9.6, 3.6))
    ax[0].plot(u, 6.0 + 0.80 * u, color=PALETTE[0], label=r"license: \$6 M + \$0.80/unit")
    ax[0].plot(u, np.full_like(u, build), color=PALETTE[1], label=r"build: \$24 M + expected slip")
    ax[0].axvline(U, color="k", ls=":", lw=1)
    ax[0].annotate(f"plan\n{U:.1f} M", (U, 34), xytext=(-34, 0), textcoords="offset points", fontsize=8)
    ax[0].plot([ustar], [build], "ko", ms=4)
    ax[0].annotate(f"break-even {ustar:.1f} M", (ustar, build), xytext=(6, -14), textcoords="offset points",
                   fontsize=8)
    ax[0].set_xlabel("discounted unit stream U (million units)")
    ax[0].set_ylabel("present cost ($M)")
    ax[0].set_ylim(0, 40)
    ax[0].set_title("License below the break-even, build above it")
    ax[0].legend(fontsize=8, loc="lower right")

    custom = s.tco_per_throughput(9000, 0.7, 0.8, 4, 1.3, 0.08, 12000)
    floor = custom - 12000 - 1.0 * 1.3 * s.HOURS_PER_YEAR * 4 * 0.08
    prices = np.linspace(floor + 600, 40000, 300)
    fleet = [800e6 / (s.tco_per_throughput(p, 1.0, 1.0, 4, 1.3, 0.08, 12000) - custom) for p in prices]
    ax[1].plot(prices / 1e3, np.array(fleet) / 1e3, color=PALETTE[0])
    ax[1].axvline(floor / 1e3, color="gray", ls="--", lw=1)
    ax[1].annotate(f"no saving below\n\\${floor / 1e3:.1f}k", (floor / 1e3, 45), xytext=(6, 0),
                   textcoords="offset points", fontsize=8)
    for p in (20000, 30000):
        f = 800e6 / (s.tco_per_throughput(p, 1.0, 1.0, 4, 1.3, 0.08, 12000) - custom)
        ax[1].plot([p / 1e3], [f / 1e3], "ko", ms=4)
        ax[1].annotate(f"{f / 1e3:.0f}k at \\${p / 1e3:.0f}k", (p / 1e3, f / 1e3), xytext=(6, 4),
                       textcoords="offset points", fontsize=8)
    ax[1].set_yscale("log")
    ax[1].set_xlabel("merchant accelerator price ($ thousand)")
    ax[1].set_ylabel("break-even fleet (thousand merchant-equivalents)")
    ax[1].set_title("A merchant price cut raises the custom bar")
    fig.tight_layout()
    save(fig, f"{OUT}/sourcing-breakevens.svg")


if __name__ == "__main__":
    main()
