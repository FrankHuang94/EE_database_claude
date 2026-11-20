#!/usr/bin/env python3
"""Figure for chapter 14-15 (roofline and benchmarks).

Run from anywhere:  python assets/figures/src/fig_14_15.py
Outputs assets/figures/14-15/roofline.svg: the H100 SXM roofline (FP32 and dense BF16 roofs over a 3.35 TB/s
bandwidth slope, R-220) with the course's kernels placed at their arithmetic intensities, from
labs/14-15-lab/roofline.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "14-computer-organization-and-architecture" / "labs" / "14-15-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import roofline as rf  # noqa: E402

OUT = "assets/figures/14-15"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_roofline():
    fp32, bw = rf.MACHINES["H100 SXM, FP32"]
    bf16, _ = rf.MACHINES["H100 SXM, BF16 dense"]
    xs = [10 ** (k / 20) for k in range(-40, 81)]          # 0.01 to 10,000 FLOP/byte
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    ax.plot(xs, [rf.attainable(bf16, bw, x) / 1e12 for x in xs], color=PALETTE[1], label="dense BF16 tensor roof (989.5 TFLOPS)")
    ax.plot(xs, [rf.attainable(fp32, bw, x) / 1e12 for x in xs], color=PALETTE[0], label="FP32 roof (67 TFLOPS)")
    pts = [(name, f / b) for name, (f, b) in rf.KERNELS.items() if "LLM" not in name]
    pts.append(("matrix product, n = 4096", rf.gemm_intensity(4096)))
    for (name, ai), mk in zip(pts, "osD^"):
        y = rf.attainable(fp32, bw, ai) / 1e12
        ax.plot(ai, y, marker=mk, color=PALETTE[2], ms=6, ls="none")
        ax.annotate(name, (ai, y), textcoords="offset points", xytext=(6, -12 if ai < 1 else 6), fontsize=7)
    for r, lab in ((rf.ridge(fp32, bw), "20"), (rf.ridge(bf16, bw), "295")):
        ax.axvline(r, color="0.7", lw=0.8, ls=":")
        ax.text(r, 0.012, f" ridge {lab}", fontsize=7, color="0.4")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.01, 10000)
    ax.set_ylim(0.01, 2000)
    ax.set_xlabel("arithmetic intensity (FLOP per byte of memory traffic)")
    ax.set_ylabel("attainable TFLOPS")
    ax.set_title("H100 SXM roofline (3.35 TB/s)", fontsize=9)
    ax.legend(fontsize=7, loc="upper left")
    save(fig, f"{OUT}/roofline.svg")
    assert round(rf.attainable(fp32, bw, 1 / 12) / 1e12, 3) == 0.279 and round(rf.ridge(bf16, bw), 1) == 295.4


if __name__ == "__main__":
    fig_roofline()
