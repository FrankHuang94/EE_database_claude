#!/usr/bin/env python3
"""Figures for chapter 27-01 (system analysis method).

Run from anywhere:  python assets/figures/src/fig_27_01.py
Outputs
  assets/figures/27-01/thermal-and-roofline.svg  left: surface temperature of Example 27-01.2's device during
                                                 9 W and 12 W bursts from a 2 W steady state (theta 4.0 C/W,
                                                 60 J/C, 25 C air) with the 43 C limit; right: the roofline of
                                                 Example 27-01.3 (400 TFLOP/s, 3.2 TB/s) with decode at batch 1
                                                 and 32 and a matrix multiplication at 300 FLOP/byte
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "27-system-architectures" / "labs" / "27-01-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import sysbudget as sb  # noqa: E402

OUT = "assets/figures/27-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def main() -> None:
    fig, ax = plt.subplots(1, 2, figsize=(9.6, 3.6))
    theta, cth, ta, tmax, t0 = 4.0, 60.0, 25.0, 43.0, 33.0
    t = np.linspace(0, 300, 601)
    for k, p in enumerate((9.0, 12.0)):
        temps = [sb.rc_temperature(x, t0, ta, p, theta, cth) for x in t]
        tb = sb.time_to_limit(t0, tmax, ta, p, theta, cth)
        ax[0].plot(t, temps, color=PALETTE[k], label=f"{p:.0f} W burst")
        ax[0].plot([tb], [tmax], "o", color=PALETTE[k], ms=4)
        ax[0].annotate(f"{tb:.0f} s", (tb, tmax), textcoords="offset points", xytext=(4, -12), fontsize=8)
    ax[0].axhline(tmax, color="k", ls=":", lw=1)
    ax[0].text(305, tmax + 0.5, "43 °C limit", fontsize=8, ha="right")
    ax[0].set_xlabel("time from start of burst (s)")
    ax[0].set_ylabel("surface temperature (°C)")
    ax[0].set_title("A burst lasts until the heat capacity fills")
    ax[0].legend(loc="lower right")

    peak, bw = 400e12, 3.2e12
    intensity = np.logspace(-0.5, 3, 300)
    att = [sb.roofline(peak, bw, i) / 1e12 for i in intensity]
    ax[1].loglog(intensity, att, color=PALETTE[0])
    ax[1].axvline(peak / bw, color="k", ls=":", lw=1)
    ax[1].text(peak / bw * 1.1, 1.0, "ridge\n125 FLOP/B", fontsize=8)
    for name, i in (("decode, batch 1", 1.0), ("decode, batch 32", 32.0), ("matrix multiply", 300.0)):
        y = sb.roofline(peak, bw, i) / 1e12
        ax[1].plot([i], [y], "o", color=PALETTE[2], ms=4)
        ax[1].annotate(f"{name}\n{y:g} TFLOP/s", (i, y), textcoords="offset points", xytext=(5, -22), fontsize=8)
    ax[1].set_xlabel("arithmetic intensity (FLOP/byte)")
    ax[1].set_ylabel("attainable TFLOP/s")
    ax[1].set_title("Below the ridge, only bandwidth helps")
    ax[1].set_ylim(0.5, 1000)
    fig.tight_layout()
    save(fig, f"{OUT}/thermal-and-roofline.svg")


if __name__ == "__main__":
    main()
