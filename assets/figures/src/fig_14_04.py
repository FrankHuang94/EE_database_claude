#!/usr/bin/env python3
"""Figures for chapter 14-04 (computer arithmetic and number formats).

Run from anywhere:  python assets/figures/src/fig_14_04.py
Outputs SVGs to assets/figures/14-04/:
- summation.svg: the magnitude of the relative error in summing n copies of the FP32 value nearest 0.1, in
  FP32, for sequential, pairwise (recursive halving) and Kahan summation, against n from 10 to 10^6, with the
  sequential worst-case bound (n - 1)u. Every addition is performed in FP32 (NumPy float32); the exact sum is
  computed with rational arithmetic.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from functools import lru_cache
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/14-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
f32 = np.float32
X = f32(0.1)


@lru_cache(maxsize=None)
def pairwise(n: int):
    if n == 1:
        return X
    h = n // 2
    return f32(pairwise(h) + pairwise(n - h))


def fig_summation():
    ns = sorted({int(round(10 ** e)) for e in np.linspace(1, 6, 41)})
    targets = set(ns)
    seq_at, kah_at = {}, {}
    s, k, c = f32(0), f32(0), f32(0)
    for i in range(1, ns[-1] + 1):
        s = f32(s + X)
        y = f32(X - c)
        t = f32(k + y)
        c = f32(f32(t - k) - y)
        k = t
        if i in targets:
            seq_at[i], kah_at[i] = s, k
    rel = lambda val, n: abs(float((Fr(float(val)) - Fr(float(X)) * n) / (Fr(float(X)) * n)))  # noqa: E731
    floor = 1e-10  # exact results (error 0) are drawn at this floor
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for lab, vals, col in (("sequential", seq_at, PALETTE[1]), ("pairwise", {n: pairwise(n) for n in ns}, PALETTE[0]), ("Kahan", kah_at, PALETTE[2])):
        ax.plot(ns, [max(rel(vals[n], n), floor) for n in ns], "o-", ms=3, lw=1.2, color=col, label=lab)
    ax.plot(ns, [(n - 1) * 2.0**-24 for n in ns], ":", color="0.4", lw=1, label="bound $(n-1)u$")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(floor / 2, 1)
    ax.set_xlabel("number of terms $n$")
    ax.set_ylabel("|relative error|")
    ax.set_title("Summing the FP32 value of 0.1 n times, in FP32", fontsize=9)
    ax.legend(fontsize=8, loc="upper left")
    assert abs(rel(seq_at[10**6], 10**6) - 0.009583) < 1e-6
    save(fig, f"{OUT}/summation.svg")


if __name__ == "__main__":
    fig_summation()
