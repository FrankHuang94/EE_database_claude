#!/usr/bin/env python3
"""Verify every published number in chapter 00-02, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "00-02",
    COURSE / "chapters" / "00-02-the-abstraction-stack.md",
    COURSE / "solutions" / "00-02-solutions.md",
    COURSE / "labs" / "00-02-lab" / "README.md",
)
c = 299_792_458.0
Q = norm.sf


def far_end_arrivals(rs, z0=50.0, v_step=1.0, n=3):
    """Far-end voltage after each arrival at an open end (lattice diagram, Gamma_L = +1)."""
    gs, launched = (rs - z0) / (rs + z0), v_step * z0 / (rs + z0)
    far, fwd, out = 0.0, launched, []
    for _ in range(n):
        far += 2 * fwd
        out.append(far)
        fwd *= gs
    return gs, launched, out


def far_end_waveform(t, rs, td=1e-9, t_rise=10e-12, z0=50.0, n=400):
    gs, tau_s = (rs - z0) / (rs + z0), z0 / (rs + z0)
    x = np.clip(t[None, :] - (2 * np.arange(n)[:, None] + 1) * td, 0, None) / t_rise
    return (2 * tau_s * gs ** np.arange(n)[:, None] * np.clip(x, 0, 1)).sum(axis=0)


# ------------------------------------------------------------------ chapter examples
lam60 = c / 60
v.check("Ex 00-02.1a", lam60 / 1e3)
v.check("Ex 00-02.1b", 100e3 / lam60)
lam_pcb = 1.5e8 / 2.5e9
v.check("Ex 00-02.1c", lam_pcb * 100)
v.check("Ex 00-02.1d", 0.15 / lam_pcb)
v_ox = c / math.sqrt(3.9)
v.check("Ex 00-02.1e", v_ox)
v.check("Ex 00-02.1f", v_ox / 3e9 * 100)
v.check("Ex 00-02.1g", 2e-3 / (v_ox / 3e9))

A = dict(VOL=0.4, VOH=2.4, VIL=0.8, VIH=2.0)
B = dict(VOL=0.2, VOH=1.6, VIL=0.6, VIH=1.2)
v.assert_true("Ex2 within-family margins are 0.4 V",
              all(math.isclose(x, 0.4) for x in [A["VIL"] - A["VOL"], A["VOH"] - A["VIH"],
                                                   B["VIL"] - B["VOL"], B["VOH"] - B["VIH"]]))
v.check("Ex 00-02.2a", B["VIL"] - A["VOL"])
v.check("Ex 00-02.2b", A["VOH"] - B["VIH"])
v.check("Ex 00-02.2c", A["VIL"] - B["VOL"])
v.check("Ex 00-02.2d", B["VOH"] - A["VIH"])

v.check("Ex 00-02.3a", 0.05 * math.sqrt(100))
v.check("Ex 00-02.3b", Q(10))
p150 = Q(0.5 / 0.15)
v.check("Ex 00-02.3c", p150)
v.check("Ex 00-02.3d", 100 * (1 - (1 - p150) ** 100))
rng = np.random.default_rng(0)
sims = (rng.normal(0, 0.15, (200_000, 100)) > 0.5).any(axis=1).mean()
v.assert_true("Ex3 Monte Carlo matches 4.20 % within sampling error", abs(sims - 0.0420) < 0.0015, f"{sims:.4f}")

v.check("Ex 00-02.4a", 0.020 / 1.5e8 * 1e12)
C0 = 2.998e8
v.assert_true("SiO2 (er 3.9) gives ~1.5e8 m/s", round(C0 / math.sqrt(3.9) / 1e8, 1) == 1.5)
v.assert_true("low-k (er 2.5-3) gives 1.7-1.9e8 m/s",
              round(C0 / math.sqrt(3.0) / 1e8, 1) == 1.7 and round(C0 / math.sqrt(2.5) / 1e8, 1) == 1.9)
v.assert_true("Q(10/3) = 4.29e-4 but Q(3.33) = 4.34e-4 and Q(3.3) = 4.8e-4",
              round(norm.sf(10 / 3), 6) == 4.29e-4 and round(norm.sf(3.33), 6) == 4.34e-4
              and round(norm.sf(3.3), 5) == 4.8e-4)
v.assert_true("atoms (0.25 nm) to datacenter (~300 m) is ~12 orders of magnitude",
              round(math.log10(300 / 0.25e-9)) == 12)
v.assert_true("lambda/10 with f = 0.35/tr allows tr/3.5; lambda/20 allows tr/7",
              math.isclose(0.1 / 0.35, 1 / 3.5) and math.isclose(0.05 / 0.35, 1 / 7))
v.check("Ex 00-02.4b", 100 * (0.020 / 1.5e8) / (1 / 3e9))

gs, launched, arr = far_end_arrivals(10.0)
v.check("Ex 00-02.5a", launched)
v.check("Ex 00-02.5b", arr[0])
v.check("Ex 00-02.5c", arr[1])
v.check("Ex 00-02.5d", arr[2])
v.check("Ex 00-02.5f", gs)
t = np.linspace(0, 150e-9, 150_001)
v.check("Ex 00-02.5e", far_end_waveform(t, 10.0, t_rise=50e-9).max())
v.assert_true("Ex5 final value is 1 V", abs(far_end_waveform(np.array([140e-9]), 10.0)[0] - 1.0) < 1e-9)

v.check("N 00-02.a", c / 1e9 * 100)
v.check("N 00-02.b", 26 * 33)
v.check("N 00-02.c", 26 * 16.5)
v.check("N 00-02.d", Q(3))
v.check("N 00-02.e", Q(6))

# ------------------------------------------------------------------ problems
v.check("00-02.2a", c / 50 / 1e3)
v.check("00-02.2b", c / 2.4e9 * 100)
v.check("00-02.2c", c / 77e9 * 1e3)
v.check("00-02.2d", c / 500e-9 / 1e12)
v.check("00-02.3a", 0.35 - 0.1)
v.check("00-02.3b", 0.9 - 0.65)
v.check("00-02.4a", 1 / (2e8 / 20e3))
v.check("00-02.4b", 0.30 / (1.5e8 / 16e9))
v.check("00-02.4c", 5e-3 / (1.5e8 / 1e9))
v.check("00-02.5a", 1.5e8 * 100e-12 / 6 * 1e3)
v.check("00-02.5b", 1.5e8 * 100e-12 / 10 * 1e3)
C_ = dict(VOL=0.3, VOH=3.0, VIL=1.0, VIH=2.3)
v.check("00-02.6a", B["VIL"] - C_["VOL"])
v.check("00-02.6b", C_["VOH"] - B["VIH"])
v.check("00-02.6c", C_["VIL"] - B["VOL"])
v.check("00-02.6d", B["VOH"] - C_["VIH"])
p_req = 1e-12 / 1e9
x = norm.isf(p_req)
v.check("00-02.7a", p_req)
v.check("00-02.7b", x)
v.check("00-02.7c", 0.5 / x * 1e3)
v.check("00-02.8a", 10 * math.log10(100))
v.check("00-02.8b", 10 ** (10 / 10))
v.check("00-02.9", 0.5 / 5e9 * 1.5e8 * 1e3)
gs25, l25, arr25 = far_end_arrivals(25.0)
v.check("00-02.10a", gs25)
v.check("00-02.10b", arr25[0])
v.check("00-02.10c", arr25[1])
v.check("00-02.10d", arr25[2])
v.check("00-02.10e", l25)
dE = 32 * 10e-15 * 0.8**2
v.check("00-02.11a", dE * 1e12)
v.check("00-02.11b", dE * 1e8 * 1e6)
v.check("00-02.12a", math.floor((1e12 / 3e9 - 60) / 15))
v.check("00-02.12b", math.floor((1e12 / 4e9 - 60) / 15))
v.check("00-02.12c", 5e-3 / 1.5e8 * 1e12)
v.check("00-02.12d", (5e-3 / 1.5e8 * 1e12) / 15)

# ------------------------------------------------------------------ lab predictions
p02 = Q(0.5 / 0.2)
v.check("Lab 00-02.1", p02)
v.check("Lab 00-02.2", 100 * (1 - (1 - p02) ** 10))

v.finish()
