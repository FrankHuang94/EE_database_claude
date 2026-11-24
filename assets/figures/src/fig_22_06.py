#!/usr/bin/env python3
"""Figures for chapter 22-06 (converter losses and wide-bandgap switches).

Run from anywhere:  python assets/figures/src/fig_22_06.py
Outputs
  assets/figures/22-06/switching-waveforms.svg  clamped-inductive hard switching of 10 A at 400 V: drain voltage,
                                                drain current and instantaneous power over a turn-on (current rises,
                                                then voltage falls) and a turn-off (voltage rises, then current falls),
                                                each 20 ns long, with the overlap energies shaded
  assets/figures/22-06/loss-vs-frequency.svg    Example 22-06.6's switch-loss budget (48 V to 12 V, 20 A) against
                                                switching frequency for 100 V silicon and GaN, stacked by mechanism,
                                                with the 2%-of-240 W line
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "22-power-electronics-and-energy-conversion" / "labs" / "22-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import losses as ls  # noqa: E402

OUT = "assets/figures/22-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_waveforms():
    V, I, t1 = 400.0, 10.0, 10e-9            # each sub-ramp 10 ns, so t_on = t_off = 20 ns
    t = np.linspace(0, 140e-9, 2801)
    v = np.full_like(t, V)
    i = np.zeros_like(t)
    on0, off0 = 10e-9, 90e-9
    for k, tt in enumerate(t):
        if on0 <= tt < on0 + t1:                      # current rises at full voltage
            i[k], v[k] = I * (tt - on0) / t1, V
        elif on0 + t1 <= tt < on0 + 2 * t1:           # voltage falls at full current
            i[k], v[k] = I, V * (1 - (tt - on0 - t1) / t1)
        elif on0 + 2 * t1 <= tt < off0:
            i[k], v[k] = I, 0.0
        elif off0 <= tt < off0 + t1:                  # voltage rises at full current
            i[k], v[k] = I, V * (tt - off0) / t1
        elif off0 + t1 <= tt < off0 + 2 * t1:         # current falls at full voltage
            i[k], v[k] = I * (1 - (tt - off0 - t1) / t1), V
        elif tt >= off0 + 2 * t1:
            i[k], v[k] = 0.0, V
    p = v * i
    tn = t * 1e9
    fig, ax = plt.subplots(3, 1, figsize=(5.8, 5.2), sharex=True)
    ax[0].plot(tn, v, color=PALETTE[0], lw=1.5)
    ax[0].set_ylabel("v_DS (V)")
    ax[1].plot(tn, i, color=PALETTE[1], lw=1.5)
    ax[1].set_ylabel("i_D (A)")
    ax[2].plot(tn, p / 1e3, color=PALETTE[3], lw=1.5)
    ax[2].fill_between(tn, 0, p / 1e3, color=PALETTE[3], alpha=0.25)
    ax[2].set_ylabel("p = v·i (kW)")
    ax[2].set_xlabel("time (ns)")
    ax[2].text(14, 3.3, "turn-on: ½VI·t_on", fontsize=8)
    ax[2].text(92, 3.3, "turn-off: ½VI·t_off", fontsize=8)
    ax[0].set_title("Hard switching of 10 A at 400 V (t_on = t_off = 20 ns)", fontsize=10)
    save(fig, f"{OUT}/switching-waveforms.svg")


def fig_losses():
    f = np.linspace(50e3, 2e6, 400)
    vin, io = 48.0, 20.0
    ihs2, ils2 = io ** 2 * 0.25, io ** 2 * 0.75
    fig, ax = plt.subplots(1, 2, figsize=(8.0, 3.4), sharey=True)
    for a, (name, r, qg, vd, qoss, qrr, t, vsd) in zip(ax, (("100 V silicon", 1.8e-3, 73e-9, 10, 135e-9, 70e-9, 8e-9, 0.8),
                                                             ("100 V GaN", 2.4e-3, 11e-9, 5, 43e-9, 0.0, 3e-9, 2.5))):
        parts = [np.full_like(f, (ihs2 + ils2) * r), ls.gate_drive(2 * qg, vd, f), ls.coss_hard_turn_on(qoss, vin, f),
                 ls.recovery(qrr, vin, f), ls.overlap(vin, io, t, t, f), ls.dead_time(vsd, io, 20e-9, f)]
        labels = ["conduction", "gate", "Q_oss·V", "Q_rr·V", "overlap", "dead time"]
        a.stackplot(f / 1e6, *parts, labels=labels, colors=PALETTE[:6], alpha=0.8)
        a.axhline(4.8, color="0.2", ls="--", lw=1)
        a.text(0.06, 5.2, "2% of 240 W", fontsize=8)
        a.set_title(name, fontsize=10)
        a.set_xlabel("switching frequency (MHz)")
    ax[0].set_ylabel("switch loss (W)")
    ax[0].set_ylim(0, 25)
    ax[1].legend(fontsize=7, loc="upper left")
    save(fig, f"{OUT}/loss-vs-frequency.svg")


if __name__ == "__main__":
    fig_waveforms()
    fig_losses()
