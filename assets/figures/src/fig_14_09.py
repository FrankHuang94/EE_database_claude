#!/usr/bin/env python3
"""Figures for chapter 14-09 (memory hierarchy and caches).

Run from anywhere:  python assets/figures/src/fig_14_09.py   (needs LLVM for the course simulator's builds)
Outputs SVGs to assets/figures/14-09/:
- caches.svg: left, misses of three 32 x 32 matrix-multiply versions (ijk, ikj, ikj tiled 8 x 8) against cache
  size for 4-way caches with 32-byte blocks; right, the three-Cs breakdown of the column traversal of a 64 x 64
  matrix for direct-mapped caches of 1 to 16 KB. All from labs/14-09-lab/cache.py on simulator traces.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
C14 = ROOT / "courses" / "14-computer-organization-and-architecture"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(C14 / "labs" / "14-09-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import cache  # noqa: E402

OUT = "assets/figures/14-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
SIZES = [1024, 2048, 4096, 8192, 16384]


def fig_caches():
    mm = {"ijk": cache.matmul("ijk")[0], "ikj": cache.matmul("ikj")[0], "ikj, tiled 8 × 8": cache.matmul("tiled", t=8)[0]}
    miss = {k: [cache.Cache(s, 32, 4).run(tr).misses for s in SIZES] for k, tr in mm.items()}
    assert [m[1] for m in miss.values()] == [34952, 4480, 1284]
    cols, _ = cache.traverse("cols")
    tc = [cache.three_c(cols, s, 32, 1) for s in SIZES]
    assert [t["conflict"] for t in tc] == [0, 3584, 3584, 3584, 0] and tc[0]["capacity"] == 3584

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(9.0, 3.5))
    for (k, m), c, mk in zip(miss.items(), (PALETTE[1], PALETTE[0], PALETTE[2]), "osD"):
        ax.plot([s // 1024 for s in SIZES], m, color=c, marker=mk, ms=4, label=k)
    ax.axhline(384, color="0.5", ls=":", lw=0.9, label="compulsory (384)")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xticks([s // 1024 for s in SIZES], [str(s // 1024) for s in SIZES])
    ax.set_xlabel("cache size (KB), 4-way, 32-byte blocks")
    ax.set_ylabel("misses")
    ax.set_title("32 × 32 matrix multiply", fontsize=9)
    ax.legend(fontsize=7)

    x = range(len(SIZES))
    bottom = [0] * len(SIZES)
    for key, c in (("compulsory", PALETTE[7]), ("capacity", PALETTE[4]), ("conflict", PALETTE[1])):
        vals = [t[key] for t in tc]
        bx.bar(x, vals, bottom=bottom, color=c, alpha=0.8, label=key)
        bottom = [b + v for b, v in zip(bottom, vals)]
    bx.set_xticks(list(x), [f"{s // 1024} KB" for s in SIZES])
    bx.set_ylabel("misses")
    bx.set_title("Column traversal, direct-mapped (4096 loads)", fontsize=9)
    bx.legend(fontsize=7, loc="upper right")
    bx.set_ylim(0, 4800)
    save(fig, f"{OUT}/caches.svg")
    return miss, tc


if __name__ == "__main__":
    m, t = fig_caches()
    print(m)
    print(t)
