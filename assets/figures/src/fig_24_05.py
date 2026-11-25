#!/usr/bin/env python3
"""Figures for chapter 24-05 (PCIe, CXL and Ethernet).

Run from anywhere:  python assets/figures/src/fig_24_05.py
Outputs
  assets/figures/24-05/credits.svg           simulated throughput of a 128 GB/s credit-flow-controlled link against
                                             receive buffer, for credit round trips of 250, 500 and 1000 ns
  assets/figures/24-05/pcie-generations.svg  PCIe per-lane bandwidth per direction, raw and after encoding, 1.0-7.0
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "24-high-speed-io-signal-integrity-and-photonics" / "labs" / "24-05-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import links  # noqa: E402

OUT = "assets/figures/24-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def credits() -> None:
    bufs = np.arange(4_000, 160_001, 4_000)
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    for i, rtt in enumerate((250, 500, 1000)):
        thr = [links.simulate_credits(128, int(b), rtt) for b in bufs]
        ax.plot(bufs / 1e3, thr, "o-", ms=2.5, color=PALETTE[i], label=f"RTT {rtt} ns")
        bdp = links.bdp_bytes(128, rtt) / 1e3
        ax.axvline(bdp, color=PALETTE[i], ls=":", lw=1)
        ax.text(bdp + 1.5, 12 + 14 * i, f"{bdp:.0f} KB", fontsize=7, color=PALETTE[i])
    ax.set_xlabel("receive buffer (KB)")
    ax.set_ylabel("throughput (GB/s)")
    ax.set_ylim(0, 140)
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(True, alpha=0.3)
    save(fig, f"{OUT}/credits.svg")


def generations() -> None:
    gens = list(links.PCIE)
    raw = [links.PCIE[g][0] / 8 for g in gens]
    eff = [links.pcie_bw(g) for g in gens]
    x = np.arange(len(gens))
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.semilogy(x, raw, "s--", color=PALETTE[1], label="raw (GT/s ÷ 8)")
    ax.semilogy(x, eff, "o-", color=PALETTE[0], label="after encoding")
    for xi, e, g in zip(x, eff, gens):
        ax.annotate(f"{e:.3g}", (xi, e), textcoords="offset points", xytext=(4, -12), fontsize=7)
    ax.set_xticks(x)
    ax.set_xticklabels([f"PCIe {g}" for g in gens], fontsize=8)
    ax.set_ylabel("GB/s per lane, each direction")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(True, which="both", alpha=0.3)
    save(fig, f"{OUT}/pcie-generations.svg")


if __name__ == "__main__":
    credits()
    generations()
