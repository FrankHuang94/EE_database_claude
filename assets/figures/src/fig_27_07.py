#!/usr/bin/env python3
"""Figures for chapter 27-07 (the AI datacenter server and rack).

Run from anywhere:  python assets/figures/src/fig_27_07.py
Outputs
  assets/figures/27-07/inference-goodput.svg  left: per-user decode speed against rack throughput as
                                              the batch grows from 1 to the HBM capacity limit, for
                                              Example 27-07.6's model and rack (assumed parameters),
                                              a straight line in this memory-bound model, with
                                              B = 256, B = 6575 and the limit marked and the
                                              KV-cache throughput ceiling dashed; right: effective
                                              training time against checkpoint interval for 10 s and
                                              60 s saves at Example 27-07.5's interruption rate with a
                                              10-minute restart, with Young's optimum marked
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "27-system-architectures" / "labs" / "27-07-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import rackmodel as rm  # noqa: E402

OUT = "assets/figures/27-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

W, K, BW, ETA, NACT, F4 = 0.5e12, 0.8e9, 576e12, 0.5, 4e10, 720e15
bmax = rm.max_batch(13.4e12, W, K)
batches = np.unique(np.round(np.logspace(0, np.log10(bmax), 300)).astype(int))
thr, user = [], []
for b in batches:
    s = rm.decode_step_s(b, W, K, BW, ETA, NACT, F4)[0]
    thr.append(b / s)
    user.append(1 / s)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
ax1.plot(np.array(thr) / 1e3, user, color=PALETTE[0])
for b, lab, off in ((256, "B = 256", (8, 6)), (6575, "B = 6575 (50 tokens/s)", (-150, 22)),
                    (bmax, f"B = {bmax} (HBM full)", (-120, 8))):
    s = rm.decode_step_s(b, W, K, BW, ETA, NACT, F4)[0]
    ax1.plot([b / s / 1e3], [1 / s], "o", color=PALETTE[1])
    ax1.annotate(lab, (b / s / 1e3, 1 / s), textcoords="offset points", xytext=off, fontsize=8)
ax1.axvline(ETA * BW / K / 1e3, color=PALETTE[3], ls="--", lw=1)
ax1.text(ETA * BW / K / 1e3 - 4, 250, "KV-cache ceiling", rotation=90, ha="right", fontsize=8)
ax1.set_ylim(0, 620)
ax1.set_xlabel("rack throughput (thousand tokens/s)")
ax1.set_ylabel("per-user speed (tokens/s)")
ax1.set_title("Batching trades interactivity for throughput", fontsize=10)
ax1.grid(True, alpha=0.3)

M = 54 * 86400 / 419
tau = np.linspace(60, 7200, 400)
for k, d in enumerate((10, 60)):
    eff = [100 * (1 - rm.lost_fraction(t, d, M, 600)) for t in tau]
    ax2.plot(tau / 60, eff, color=PALETTE[k + 2], label=f"save time {d} s")
    ts = rm.young_interval_s(d, M)
    ax2.plot([ts / 60], [100 * (1 - rm.lost_fraction(ts, d, M, 600))], "o", color=PALETTE[k + 2])
ax2.axhline(90, color="0.5", ls=":", lw=1)
ax2.text(118, 90.4, "90%", ha="right", fontsize=8, color="0.4")
ax2.set_xlabel("checkpoint interval (min)")
ax2.set_ylabel("effective training time (%)")
ax2.set_title("Young's optimum, one interruption per 3.09 h", fontsize=10)
ax2.set_ylim(70, 95)
ax2.legend(fontsize=8, loc="lower right")
ax2.grid(True, alpha=0.3)
fig.tight_layout()
save(fig, f"{OUT}/inference-goodput.svg")
