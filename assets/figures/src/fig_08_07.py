#!/usr/bin/env python3
"""Figures for chapter 08-07 (registers, counters and shift registers).

Run from anywhere:  python assets/figures/src/fig_08_07.py
Outputs SVGs to assets/figures/08-07/: a 4-bit Fibonacci LFSR (x^4 + x^3 + 1) with its 15-state
sequence (computed by stepping the register), and the waveforms of a 4-bit ripple counter going
from 6 to 7 to 8 with 2 ns per stage (computed by an event simulation), showing its transient states.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/08-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def lfsr_step(state, n, k):
    """Bit i-1 of state holds Q_i; Q1 <- Q_n xor Q_k, the others shift toward Q_n."""
    fb = ((state >> (n - 1)) ^ (state >> (k - 1))) & 1
    return ((state << 1) | fb) & ((1 << n) - 1)


def arrow(ax, p, q, color="black"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12, lw=1.4, color=color,
                                 shrinkA=0, shrinkB=0))


def fig_lfsr():
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.set_xlim(-0.6, 11.4)
    ax.set_ylim(-2.9, 3.3)
    ax.set_aspect("equal")
    ax.axis("off")
    xs = [1.0, 3.2, 5.4, 7.6]                      # left edges of the four flip-flops
    w, h, y0 = 1.3, 1.3, 0.0
    for i, x in enumerate(xs):
        ax.add_patch(Rectangle((x, y0), w, h, fill=False, lw=1.6))
        ax.text(x + w / 2, y0 + h / 2, f"$Q_{i + 1}$", ha="center", va="center", fontsize=12)
        ax.plot([x, x + 0.18, x], [y0 + 0.05, y0 + 0.17, y0 + 0.29], color="black", lw=0.9)
    ym = y0 + h / 2
    for a, b in zip(xs[:-1], xs[1:]):              # Q_i drives D of Q_(i+1)
        arrow(ax, (a + w, ym), (b, ym))
    arrow(ax, (xs[3] + w, ym), (xs[3] + w + 1.3, ym))
    ax.text(xs[3] + w + 1.4, ym, "output\n(PRBS)", va="center", fontsize=9)
    # feedback: taps at Q3 and Q4 into an XOR, back to D of Q1
    xor_c = (6.0, 2.45)
    ax.add_patch(Circle(xor_c, 0.32, fill=False, lw=1.6, color=PALETTE[1]))
    ax.plot([xor_c[0] - 0.32, xor_c[0] + 0.32], [xor_c[1]] * 2, color=PALETTE[1], lw=1.4)
    ax.plot([xor_c[0]] * 2, [xor_c[1] - 0.32, xor_c[1] + 0.32], color=PALETTE[1], lw=1.4)
    tap4 = xs[3] + w + 0.5
    tap3 = xs[2] + w + 0.4
    ax.plot([tap4, tap4, xor_c[0] + 0.32], [ym, xor_c[1], xor_c[1]], color=PALETTE[1], lw=1.4)
    ax.plot([tap3, tap3], [ym, xor_c[1] - 0.9], color=PALETTE[1], lw=1.4)
    ax.plot([tap3, xor_c[0]], [xor_c[1] - 0.9, xor_c[1] - 0.9], color=PALETTE[1], lw=1.4)
    arrow(ax, (xor_c[0], xor_c[1] - 0.9), (xor_c[0], xor_c[1] - 0.32), PALETTE[1])
    for xt in (tap3, tap4):
        ax.plot(xt, ym, "o", color=PALETTE[1], ms=4)
    ax.plot([xor_c[0] - 0.32, 0.3, 0.3], [xor_c[1], xor_c[1], ym], color=PALETTE[1], lw=1.4)
    arrow(ax, (0.3, ym), (xs[0], ym), PALETTE[1])
    ax.text(xor_c[0], xor_c[1] + 0.5, r"$Q_1^{\mathrm{next}} = Q_4 \oplus Q_3$", ha="center", fontsize=10,
            color=PALETTE[1])
    # common clock
    ax.plot([0.3, xs[3] + 0.3], [-0.6, -0.6], color="0.4", lw=1.0)
    for x in xs:
        ax.plot([x + 0.3, x + 0.3], [-0.6, y0], color="0.4", lw=1.0)
    ax.text(0.2, -0.6, "clk", ha="right", va="center", fontsize=9, color="0.4")
    # the state sequence, computed
    s, states = 1, []
    for _ in range(15):
        states.append(s)
        s = lfsr_step(s, 4, 3)
    assert s == 1 and len(set(states)) == 15
    words = ["".join(str((st >> i) & 1) for i in range(4)) for st in states]
    ax.text(5.4, -1.5, r"states $Q_1Q_2Q_3Q_4$ from 1000 (period $2^4 - 1 = 15$):", ha="center", fontsize=9)
    ax.text(5.4, -2.15, "  ".join(words[:8]), ha="center", fontsize=8.5, family="monospace")
    ax.text(5.4, -2.6, "  ".join(words[8:]) + "  -> 1000", ha="center", fontsize=8.5, family="monospace")
    ax.set_title(r"A 4-bit Fibonacci LFSR, $x^4 + x^3 + 1$", fontsize=11)
    save(fig, f"{OUT}/lfsr.svg")


def ripple_trace(start, n, tcq, t0):
    """Event simulation: stage 0 toggles at t0 + tcq; each stage falling 1 -> 0 toggles the next tcq later."""
    q, t, out, stage = start, t0, [], 0
    while stage < n:
        t += tcq
        old = (q >> stage) & 1
        q ^= 1 << stage
        out.append((t, q))
        if old == 0:
            break
        stage += 1
    return out


def fig_ripple():
    tcq, period = 2.0, 20.0
    events = [(-6.0, 6)] + ripple_trace(6, 4, tcq, 0.0) + ripple_trace(7, 4, tcq, period)
    assert [s for _, s in events] == [6, 7, 6, 4, 0, 8]
    t_end = 36.0
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    rows = ["clk", "$Q_0$", "$Q_1$", "$Q_2$", "$Q_3$"]
    for r, name in enumerate(rows):
        base = (len(rows) - 1 - r) * 1.5
        if r == 0:
            ts = [-6, 0, 0, 10, 10, 20, 20, 30, 30, t_end]
            ys = [0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
        else:
            ts, ys = [], []
            for i, (t, s) in enumerate(events):
                bit = (s >> (r - 1)) & 1
                if i:
                    ts.append(t)
                    ys.append(ys[-1])
                ts.append(t)
                ys.append(bit)
            ts.append(t_end)
            ys.append(ys[-1])
        ax.plot(ts, [base + 0.9 * y for y in ys], color=PALETTE[0] if r else "black", lw=1.6)
        ax.text(-7.0, base + 0.45, name, ha="right", va="center", fontsize=10)
    ax.axvspan(period + tcq, period + 4 * tcq, color=PALETTE[1], alpha=0.12, lw=0)
    for (t, s), (t2, _) in zip(events, events[1:] + [(t_end, None)]):
        ax.text((t + t2) / 2, 7.55, str(s), ha="center", fontsize=9,
                color=PALETTE[1] if period < t < period + 4 * tcq else "black")
    ax.text(-7.0, 7.55, "count", ha="right", fontsize=9)
    ax.set_xlim(-6, t_end)
    ax.set_ylim(-0.4, 8.2)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.grid(False)
    ax.set_xlabel("time (ns)")
    ax.set_title("A 4-bit ripple counter, 2 ns per stage: counting 6, 7, 8\n(shaded: transient states 6, 4, 0 between 7 and 8)", fontsize=11)
    save(fig, f"{OUT}/ripple-transients.svg")


if __name__ == "__main__":
    fig_lfsr()
    fig_ripple()
    print("figures written to", OUT)
