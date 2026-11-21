#!/usr/bin/env python3
"""Figures for chapter 18-01 (microcontroller architecture).

Run from anywhere:  python assets/figures/src/fig_18_01.py
Outputs
  assets/figures/18-01/memory-map.svg      the Armv7-M/Armv8-M default 4 GiB memory map, one row per region (not to scale),
                                           with typical contents of each region
  assets/figures/18-01/flash-wait-states.svg  left: flash wait states against clock for a 33.3 ns flash; right: effective
                                           instruction rate f/CPI with no cache and with a 95% hit-rate cache
                                           (0.12 taken branches per instruction), with the zero-wait-state ideal
Uses labs/18-01-lab/mcuarch.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "18-embedded-systems-and-microcontrollers" / "labs" / "18-01-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import mcuarch as ma  # noqa: E402

OUT = "assets/figures/18-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- memory map
contents = {
    "Code": "flash, boot ROM; vector table at 0x0000 0000",
    "SRAM": "on-chip SRAM",
    "Peripheral": "AHB/APB peripheral registers",
    "External RAM": "external memory controller",
    "External device": "external devices",
    "Private peripheral bus": "NVIC, SysTick, SCB, MPU, debug",
    "Vendor system": "vendor-specific",
}
fig, ax = plt.subplots(figsize=(8.6, 4.6))
y = 0.0
for i, (lo, hi, name) in enumerate(ma.REGIONS):
    h = 1.0
    ax.add_patch(plt.Rectangle((0, y), 1.6, h, facecolor=PALETTE[i % len(PALETTE)], alpha=0.35, edgecolor="black"))
    size = hi - lo + 1
    size_txt = f"{size / 2**30:.0f} GiB" if size >= 2**30 else f"{size / 2**20:.0f} MiB"
    ax.text(0.8, y + 0.5, f"{name} ({size_txt})", ha="center", va="center", fontsize=8)
    ax.text(-0.05, y, f"0x{lo:08X}", ha="right", va="center", fontsize=7, family="monospace")
    ax.text(1.7, y + 0.5, contents[name], ha="left", va="center", fontsize=7.5)
    y += h
ax.text(-0.05, y, "0xFFFFFFFF", ha="right", va="center", fontsize=7, family="monospace")
ax.set_xlim(-1.0, 4.6)
ax.set_ylim(-0.3, y + 0.3)
ax.axis("off")
ax.set_title("Cortex-M default memory map (one region per row, not to scale)")
fig.tight_layout()
save(fig, f"{OUT}/memory-map.svg")

# ---------------------------------------------------------------- wait states and throughput
t_acc = 1 / 30e6
f = np.linspace(1e6, 180e6, 1000)
ws = np.array([ma.wait_states(x, t_acc) for x in f])
cpi0 = np.array([ma.cpi_analytic(w, 16, 2, 0.12) for w in ws])
cpi_c = np.array([ma.cpi_analytic(w, 16, 2, 0.12, 0.05) for w in ws])
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.0, 3.6))
a1.step(f / 1e6, ws, where="post", color=PALETTE[0])
a1.set_xlabel("core clock (MHz)")
a1.set_ylabel("flash wait states")
a1.set_title("WS = ⌈f · t_acc⌉ − 1, t_acc = 33.3 ns")
a2.plot(f / 1e6, f / 1e6, "--", color="gray", label="zero wait states")
a2.plot(f / 1e6, f / cpi_c / 1e6, color=PALETTE[2], label="cache, 95% hits")
a2.plot(f / 1e6, f / cpi0 / 1e6, color=PALETTE[1], label="no cache (prefetch only)")
a2.set_xlabel("core clock (MHz)")
a2.set_ylabel("instructions per µs")
a2.set_title("Wait states tax every taken branch")
a2.legend(fontsize=7)
fig.tight_layout()
save(fig, f"{OUT}/flash-wait-states.svg")
