#!/usr/bin/env python3
"""Figures for chapter 02-08 (eigenvalues, eigenvectors and the SVD).

Run:  python assets/figures/src/fig_02_08.py  -> assets/figures/02-08/*.svg
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

use_style()
OUT = "assets/figures/02-08"
B, O, G, P, Y = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3], PALETTE[4]


def arrow(ax, start, end, color, lw=1.6, alpha=1.0):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, alpha=alpha, shrinkA=0, shrinkB=0,
                                mutation_scale=11))


def fig_eigen_directions():
    A = np.array([[4.0, 1.0], [2.0, 3.0]])
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.8))
    th = np.linspace(0, 2 * np.pi, 25)[:-1]
    eig_dirs = [np.array([1, 1]) / math.sqrt(2), np.array([1, -2]) / math.sqrt(5)]
    for ax, title in ((axes[0], "inputs x on the unit circle"), (axes[1], "outputs Ax")):
        ax.set_aspect("equal")
        ax.set_title(title, fontsize=10)
    for t in th:
        x = np.array([math.cos(t), math.sin(t)])
        arrow(axes[0], (0, 0), tuple(x), "0.7", lw=1)
        arrow(axes[1], (0, 0), tuple(A @ x), "0.7", lw=1)
    circ = np.linspace(0, 2 * np.pi, 200)
    axes[0].plot(np.cos(circ), np.sin(circ), color="0.85", lw=1)
    ell = A @ np.vstack([np.cos(circ), np.sin(circ)])
    axes[1].plot(ell[0], ell[1], color="0.85", lw=1)
    for d, lam, col in ((eig_dirs[0], 5, B), (eig_dirs[1], 2, O)):
        for s in (1, -1):
            arrow(axes[0], (0, 0), tuple(s * d), col, lw=2.4)
            arrow(axes[1], (0, 0), tuple(s * lam * d), col, lw=2.4)
        line = np.vstack([-6 * d, 6 * d])
        for ax in axes:
            ax.plot(line[:, 0], line[:, 1], color=col, lw=0.8, ls=":")
    axes[1].text(3.7, 3.0, "λ = 5 along (1, 1)", color=B, fontsize=9)
    axes[1].text(1.1, -2.2, "λ = 2 along (1, −2)", color=O, fontsize=9)
    axes[0].set_xlim(-1.5, 1.5)
    axes[0].set_ylim(-1.5, 1.5)
    axes[1].set_xlim(-5.2, 5.2)
    axes[1].set_ylim(-5.2, 5.2)
    fig.suptitle("A = [4 1; 2 3]: grey arrows turn; coloured eigenvector arrows stay on their lines", fontsize=11)
    fig.tight_layout()
    save(fig, f"{OUT}/eigen-directions.svg")


def fig_ladder_modes():
    n = 20
    K = 2 * np.eye(n) - np.eye(n, k=1) - np.eye(n, k=-1)
    w, V = np.linalg.eigh(K)
    nodes = np.arange(1, n + 1)
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    for idx, col in ((0, B), (1, O), (2, G), (n - 1, P)):
        vec = V[:, idx] * np.sign(V[np.argmax(np.abs(V[:, idx])), idx])
        ax.plot(nodes, vec, "o-", color=col, ms=3.5, lw=1.4, label=f"mode {idx + 1}: λ = {w[idx]:.4f} S")
    ax.axhline(0, color="0.6", lw=0.8)
    ax.set_xlabel("node number")
    ax.set_ylabel("eigenvector entry")
    ax.set_xticks([1, 5, 10, 15, 20])
    ax.legend(fontsize=8, loc="lower left")
    ax.set_title("Eigenvectors of a 20-node 1 Ω ladder: sampled standing waves", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/ladder-modes.svg")


def fig_mode_splitting():
    L, C = 1e-6, 1e-9
    cc = np.linspace(0, 0.3e-9, 200)
    f1 = np.full_like(cc, 1 / (2 * math.pi * math.sqrt(L * C)))
    f2 = 1 / (2 * math.pi * np.sqrt(L * (C + 2 * cc)))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 3.9))
    a1.plot(cc * 1e9, f1 / 1e6, color=B, label="in-phase mode (1, 1)")
    a1.plot(cc * 1e9, f2 / 1e6, color=O, label="out-of-phase mode (1, −1)")
    a1.axvline(0.1, color="0.6", lw=0.8, ls="--")
    a1.text(0.105, 4.25, "Example 02-08.5\n(Cc = 0.1 nF)", fontsize=8, color="0.35")
    a1.set_xlabel("coupling capacitance Cc (nF)")
    a1.set_ylabel("mode frequency (MHz)")
    a1.legend(fontsize=8, loc="lower left")
    a1.set_title("Coupling splits one resonance into two", fontsize=10)
    w1 = 2 * math.pi / math.sqrt(L * C)
    w2 = 2 * math.pi / math.sqrt(L * 1.2e-9)
    w1, w2 = 1 / math.sqrt(L * C), 1 / math.sqrt(L * 1.2e-9)
    t = np.linspace(0, 3e-6, 6000)
    v1 = 0.5 * (np.cos(w1 * t) + np.cos(w2 * t))
    v2 = 0.5 * (np.cos(w1 * t) - np.cos(w2 * t))
    a2.plot(t * 1e6, v1, color=B, lw=0.6, label="resonator 1")
    a2.plot(t * 1e6, v2 - 2.4, color=O, lw=0.6, label="resonator 2 (offset)")
    a2.axvline(1.140, color="0.5", lw=0.8, ls="--")
    a2.text(1.18, 0.75, "complete transfer\nat 1.140 µs", fontsize=8, color="0.35")
    a2.set_xlabel("t (µs)")
    a2.set_yticks([])
    a2.legend(fontsize=8, loc="upper right")
    a2.set_title("Only resonator 1 excited: energy beats between them", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/mode-splitting.svg")


def fig_svd_geometry():
    H = np.array([[2.0, 2.0], [-1.0, 1.0]])
    U, s, Vt = np.linalg.svd(H)
    V = Vt.T.copy()
    for i in range(2):                 # singular-vector signs are arbitrary; match the chapter (v_i first entry > 0)
        if V[0, i] < 0:
            V[:, i] *= -1
            U[:, i] *= -1
    circ = np.linspace(0, 2 * np.pi, 300)
    pts = np.vstack([np.cos(circ), np.sin(circ)])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 4.2))
    a1.plot(pts[0], pts[1], color="0.6")
    img = H @ pts
    a2.plot(img[0], img[1], color="0.6")
    for i, col in ((0, B), (1, O)):
        arrow(a1, (0, 0), tuple(V[:, i]), col, lw=2.4)
        a1.text(*(V[:, i] * 1.18), f"v{i + 1}", color=col, fontsize=10, ha="center")
        arrow(a2, (0, 0), tuple(s[i] * U[:, i]), col, lw=2.4)
        a2.text(*(s[i] * U[:, i] * 1.12 + np.array([0.0, 0.18])), f"σ{i + 1}u{i + 1}, σ{i + 1} = {s[i]:.3f}",
                color=col, fontsize=9, ha="center")
    for ax, title, lim in ((a1, "unit circle (inputs)", 1.6), (a2, "image under H = [2 2; −1 1]", 3.4)):
        ax.set_aspect("equal")
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_title(title, fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/svd-geometry.svg")


if __name__ == "__main__":
    fig_eigen_directions()
    fig_ladder_modes()
    fig_mode_splitting()
    fig_svd_geometry()
