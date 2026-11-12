#!/usr/bin/env python3
"""Verify every number in the Course 00 final-exam solutions."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("00-exam", HERE.parent / "exam" / "solutions.md")
v.check("X00.1a", 5.0 * 3.87)
v.check("X00.1b", 5.0 * 3.87 / 30)
v.check("X00.3a", 0.30 / (1.5e8 / 1e9))
v.check("X00.3b", 0.30 / (1.5e8 / 10e6))
v.check("X00.4a", 0.45 - 0.15)
v.check("X00.4b", 1.05 - 0.75)
p = norm.sf(0.45 / 0.1)
v.check("X00.5a", p)
v.check("X00.5b", 100 * (1 - (1 - p) ** 1000))
gs, vi = (30 - 50) / 80, 50 / 80
v.check("X00.6a", gs)
v.check("X00.6b", vi)
v.check("X00.6c", 2 * vi)
v.check("X00.6d", 2 * vi + 2 * vi * gs)
v.check("X00.7a", 10e-3 * 1e3)  # SPICE "M" = milli
v.check("X00.7b", 3.3 * 20 / 30)
b = 1e8
naive = (b - math.sqrt(b * b - 4)) / 2
stable = 2 / (b + math.sqrt(b * b - 4))
v.check("X00.8a", naive)
v.check("X00.8b", stable)
v.check("X00.8c", 100 * (naive - stable) / stable)
v.assert_true("adjacent doubles near 1e8 are 1.49e-8 apart", round(float(np.spacing(1e8)), 10) == 1.49e-8)
v.assert_true("roots multiply to 1: stable root x large root ≈ 1",
              math.isclose(stable * (b + math.sqrt(b * b - 4)) / 2, 1.0, rel_tol=1e-12))
v.check("X00.10", 30e9 * 0.02 * 2.5e9 * 0.4e-15)
v.check("X00.11", 100 * 0.995**40)
v.check("X00.12a", 10 + 14)
v.check("X00.12b", (8 + 10 + 15) / 3 + (12 + 14 + 22) / 3)
s13 = 10**1.5
v.check("X00.13a", 40e6 * math.log2(1 + s13) / 1e6)
v.check("X00.13b", 80e6 * math.log2(1 + s13) / 1e6)
v.check("X00.13c", 40e6 * math.log2(1 + 2 * s13) / 1e6)
v.check("X00.13d", 40e6 * (math.log2(1 + 2 * s13) - math.log2(1 + s13)) / 1e6)
v.check("X00.15a", 1511 / 1000)  # R-016: WSTS Spring 2026 forecast, US$ 1,511 B
v.check("X00.15b", 795.6)  # R-016: WSTS 2025 actual
v.assert_true("R-016: 1511/795.6 = +89.9 %", round(100 * (1511 / 795.6 - 1), 1) == 89.9)
v.finish()
