#!/usr/bin/env python3
"""Figures for chapter 17-13 (computer networks fundamentals).

Run from anywhere:  python assets/figures/src/fig_17_13.py
Outputs
  assets/figures/17-13/tcp-and-queues.svg  left: mean TCP congestion window (segments per RTT) against random loss
                                           probability, simulated AIMD sawtooth vs sqrt(3/(2p)); right: M/M/1 mean time in
                                           system (service times) against utilization, formula vs event simulation
Uses labs/17-13-lab/netlab.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "17-communication-systems" / "labs" / "17-13-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import netlab as nl  # noqa: E402

OUT = "assets/figures/17-13"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(1713)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.0, 3.6))
p = np.logspace(-5, -2, 100)
a1.loglog(p, np.sqrt(1.5 / p), color=PALETTE[0], label="√(3/(2p)) (square-root formula)")
ps = np.logspace(-5, -2, 7)
a1.loglog(ps, [nl.simulate_aimd(x, 60_000 if x > 3e-5 else 150_000, rng) for x in ps], "o", color=PALETTE[1], label="simulated AIMD")
a1.set_xlabel("packet loss probability p")
a1.set_ylabel("mean window (segments per RTT)")
a1.set_title("TCP: 100× less loss buys 10× the window")
a1.legend(fontsize=7)
rho = np.linspace(0.05, 0.95, 100)
a2.plot(rho, 1 / (1 - rho), color=PALETTE[0], label="1/(1 − ρ)")
rs = np.array([0.2, 0.4, 0.6, 0.8, 0.9])
a2.plot(rs, [nl.simulate_mm1(r, 1.0, 100_000, rng) for r in rs], "s", color=PALETTE[2], label="simulated M/M/1")
a2.set_xlabel("utilization ρ")
a2.set_ylabel("mean time in system (service times)")
a2.set_title("Queues: delay explodes as ρ → 1")
a2.set_ylim(0, 22)
a2.legend(fontsize=7)
fig.tight_layout()
save(fig, f"{OUT}/tcp-and-queues.svg")
