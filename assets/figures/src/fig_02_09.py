#!/usr/bin/env python3
"""Figures for chapter 02-09 (systems of linear ODEs and the matrix exponential).

Run:  python assets/figures/src/fig_02_09.py  -> assets/figures/02-09/*.svg
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

use_style()
OUT = "assets/figures/02-09"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def trajectory(A, x0, t_end, n=600):
    ts = np.linspace(0, t_end, n)
    return np.array([expm(A * t) @ x0 for t in ts])


def fig_state_flow():
    A = np.array([[-2.0, 1.0], [1.0, -2.0]])
    fig, ax = plt.subplots(figsize=(5.6, 5.2))
    g = np.linspace(-1.1, 1.1, 15)
    X, Y = np.meshgrid(g, g)
    U = A[0, 0] * X + A[0, 1] * Y
    V = A[1, 0] * X + A[1, 1] * Y
    ax.quiver(X, Y, U, V, color="0.7", angles="xy", scale=40, width=0.003)
    for d, col, lab in ((np.array([1, 1]), B, "slow mode (1, 1): λ = −1/τ"), (np.array([1, -1]), O, "fast mode (1, −1): λ = −3/τ")):
        ax.plot([-1.2 * d[0], 1.2 * d[0]], [-1.2 * d[1], 1.2 * d[1]], color=col, lw=1.2, ls="--", label=lab)
    for x0 in ([1, 0], [0, 1], [-1, 0.2], [0.3, -1], [-0.8, -0.9], [0.9, 0.95]):
        tr = trajectory(A, np.array(x0, float), 4.0)
        ax.plot(tr[:, 0], tr[:, 1], color="k" if x0 == [1, 0] else "0.4", lw=2.0 if x0 == [1, 0] else 1.0)
        ax.plot(*x0, "o", color="k", ms=3)
    ax.annotate("start (1, 0)", (1, 0), xytext=(0.62, -0.32), fontsize=8)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect("equal")
    ax.set_xlabel("v1 (V)")
    ax.set_ylabel("v2 (V)")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Flow of x' = Ax for the coupled capacitors (t in units of τ)", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/state-flow.svg")


def fig_phase_portraits():
    mats = [("stable node", np.array([[-2.0, 1.0], [1.0, -2.0]]), 4.0),
            ("saddle", np.array([[1.0, 2.0], [2.0, 1.0]]), 1.2),
            ("stable spiral", np.array([[-1.0, -4.0], [1.0, -1.0]]), 6.0),
            ("center", np.array([[0.0, 1.0], [-4.0, 0.0]]), 3.3)]
    fig, axes = plt.subplots(1, 4, figsize=(13.0, 3.6))
    starts = [np.array([math.cos(a), math.sin(a)]) for a in np.linspace(0, 2 * np.pi, 9)[:-1]]
    for ax, (name, A, tend) in zip(axes, mats):
        g = np.linspace(-1.2, 1.2, 13)
        X, Y = np.meshgrid(g, g)
        ax.quiver(X, Y, A[0, 0] * X + A[0, 1] * Y, A[1, 0] * X + A[1, 1] * Y, color="0.8", angles="xy",
                  scale=None, width=0.004)
        if name == "saddle":                      # start near the stable line so trajectories come in, then leave
            sd = np.array([1.0, -1.0]) / math.sqrt(2); un = np.array([1.0, 1.0]) / math.sqrt(2)
            these = [s * 1.6 * sd + e * un for s in (1, -1) for e in (-0.3, -0.1, -0.02, 0.02, 0.1, 0.3)]
        else:
            these = [x0 * (0.5 if name == "center" else 1.0) for x0 in starts]
        for x0 in these:
            tr = trajectory(A, x0, tend if name != "saddle" else 2.5, 800)
            tr = tr[np.all(np.abs(tr) < 1.25, axis=1)]
            ax.plot(tr[:, 0], tr[:, 1], color=B, lw=1.0)
        if name in ("stable node", "saddle"):
            w, V = np.linalg.eig(A)
            for k, col in ((0, O), (1, G)):
                d = np.real(V[:, k])
                ax.plot([-1.3 * d[0], 1.3 * d[0]], [-1.3 * d[1], 1.3 * d[1]], color=col, ls="--", lw=1.0)
        T, D = np.trace(A), np.linalg.det(A)
        ax.set_title(f"{name}\nT = {T:g}, Δ = {D:g}", fontsize=9)
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    save(fig, f"{OUT}/phase-portraits.svg")


def fig_thermal_modes():
    Rdh, Rha, Cd, Ch, Pw = 0.5, 1.5, 2.0, 50.0, 10.0
    A = np.array([[-1 / (Rdh * Cd), 1 / (Rdh * Cd)], [1 / (Rdh * Ch), -(1 / Rdh + 1 / Rha) / Ch]])
    Bv = np.array([1 / Cd, 0.0])
    xss = -np.linalg.solve(A, Bv * Pw)
    w, V = np.linalg.eig(A)
    w, V = np.real(w), np.real(V)
    c = np.linalg.solve(V, -xss)
    Ri = -(c * V[0]) / Pw
    taus = -1 / w
    t = np.linspace(0, 400, 2000)
    Td = xss[0] + (c * V[0]) @ np.exp(np.outer(w, t))
    Th = xss[1] + (c * V[1]) @ np.exp(np.outer(w, t))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 3.9))
    a1.plot(t, Td, color=O, label="die")
    a1.plot(t, Th, color=B, label="heat sink")
    a1.axhline(20, color=O, lw=0.6, ls=":")
    a1.axhline(15, color=B, lw=0.6, ls=":")
    a1.set_xlabel("t (s)")
    a1.set_ylabel("temperature rise (K)")
    a1.legend(fontsize=8, loc="lower right")
    a1.set_title("10 W step: fast rise, slow approach", fontsize=10)
    tl = np.logspace(-3, 3, 400)
    Z = sum(r * (1 - np.exp(-tl / tc)) for r, tc in zip(Ri, taus))
    a2.semilogx(tl, Z, color="k", lw=2, label="Zth = sum of Foster terms")
    for r, tc, col in zip(Ri, taus, (G, P)):
        a2.semilogx(tl, r * (1 - np.exp(-tl / tc)), color=col, ls="--", label=f"R = {r:.4f} K/W, τ = {tc:.4g} s")
    a2.set_xlabel("pulse duration t (s)")
    a2.set_ylabel("Zth (K/W)")
    a2.legend(fontsize=8, loc="upper left")
    a2.set_title("Die thermal impedance (datasheet view)", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/thermal-modes.svg")


def fig_sampling():
    tau = 1.0
    A = np.array([[-2.0, 1.0], [1.0, -2.0]]) / tau
    x0 = np.array([1.0, 0.0])
    t = np.linspace(0, 5, 500)
    exact = np.array([expm(A * tt) @ x0 for tt in t])
    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    ax.plot(t, exact[:, 1], color="k", lw=2, label="exact v2(t)")
    for T, col, mk in ((0.5, B, "o"), (1.0, O, "s")):
        Ad = expm(A * T)
        Ae = np.eye(2) + A * T
        xe, xz = x0.copy(), x0.copy()
        ks, ve, vz = [0.0], [0.0], [0.0]
        for k in range(1, int(5 / T) + 1):
            xe = Ae @ xe
            xz = Ad @ xz
            ks.append(k * T)
            ve.append(xe[1])
            vz.append(xz[1])
        ax.plot(ks, ve, mk + "--", color=col, ms=5, lw=1, label=f"forward Euler, T = {T:g} ms")
        if T == 0.5:
            ax.plot(ks, vz, "x", color=G, ms=8, mew=2, label="exact ZOH samples, T = 0.5 ms")
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel("t (ms)")
    ax.set_ylabel("v2 (V)")
    ax.legend(fontsize=8, loc="lower left")
    ax.set_title("Exact sampling vs forward Euler for the coupled capacitors (τ = 1 ms)", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/sampling.svg")


if __name__ == "__main__":
    fig_state_flow()
    fig_phase_portraits()
    fig_thermal_modes()
    fig_sampling()
