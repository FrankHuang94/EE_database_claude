#!/usr/bin/env python3
"""Figures for chapter 27-04 (earbuds, smart glasses and XR headsets).

Run from anywhere:  python assets/figures/src/fig_27_04.py
Outputs
  assets/figures/27-04/anc-latency.svg  left: ANC attenuation against frequency for perfect-gain cancellation
                                        with delays of 20 us, 50 us, 100 us and 1 ms (negative = amplification);
                                        right: motion-to-photon latency budgets of Example 27-04.6 (local,
                                        split and reprojected) with the registration error at 200 deg/s
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "27-system-architectures" / "labs" / "27-04-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import headworn as hw  # noqa: E402

OUT = "assets/figures/27-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
f = np.logspace(1, np.log10(5000), 400)
for k, (tau, lab) in enumerate([(20e-6, "20 µs"), (50e-6, "50 µs"), (100e-6, "100 µs"), (1e-3, "1 ms")]):
    att = [hw.anc_attenuation_db(fi, tau) for fi in f]
    ax1.semilogx(f, att, color=PALETTE[k], label=f"delay {lab}")
ax1.axhline(0, color="k", lw=0.8)
ax1.set_ylim(-10, 45)
ax1.set_xlabel("frequency (Hz)")
ax1.set_ylabel("cancellation (dB)")
ax1.set_title("ANC with perfect gain: delay limits bandwidth", fontsize=10)
ax1.legend(fontsize=8)
ax1.grid(True, which="both", alpha=0.3)

frame = 1000 / 90
stages = {
    "local": [("tracking", 2.0), ("render", frame), ("scan-out", frame / 2), ("response", 1.0)],
    "split": [("tracking", 2.0), ("render", frame), ("encode+net+decode", 16.0), ("scan-out", frame / 2),
              ("response", 1.0)],
    "reprojected": [("tracking", 2.0), ("reprojection", 2.0), ("scan-out", frame / 2), ("response", 1.0)],
}
colors = {"tracking": PALETTE[0], "render": PALETTE[1], "encode+net+decode": PALETTE[2],
          "scan-out": PALETTE[3], "response": PALETTE[4], "reprojection": PALETTE[5]}
seen = set()
for y, (name, parts) in enumerate(stages.items()):
    left = 0.0
    for stage, dur in parts:
        ax2.barh(y, dur, left=left, color=colors[stage], label=stage if stage not in seen else None)
        seen.add(stage)
        left += dur
    ax2.text(left + 0.5, y, f"{left:.1f} ms, {hw.angular_error_deg(200, left):.2f}°", va="center", fontsize=8)
ax2.set_yticks(range(len(stages)))
ax2.set_yticklabels(list(stages))
ax2.set_xlim(0, 50)
ax2.set_xlabel("motion-to-photon latency (ms)")
ax2.set_title("Example 27-04.6: latency and error at 200°/s", fontsize=10)
ax2.legend(fontsize=7, loc="lower right")
fig.tight_layout()
save(fig, f"{OUT}/anc-latency.svg")
