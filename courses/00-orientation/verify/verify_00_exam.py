#!/usr/bin/env python3
"""Verify every number in the Course 00 final-exam solutions."""
from __future__ import annotations

import math
import sys
from pathlib import Path

from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("00-exam", HERE.parent / "exam" / "solutions.md")
v.check("X00.1a", 5.0 * 3.87)
v.check("X00.1b", 5.0 * 3.87 / 30)
v.check("X00.2a", 224e9 * 4e-12)
v.check("X00.2b", 32 * 224e9 * 4e-12)
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
v.check("X00.7", 3.3 * 20 / 30)
x = 1e16
v.assert_true("naive sqrt difference is 0 at 1e16", math.sqrt(x + 1) - math.sqrt(x) == 0.0)
v.check("X00.8", 1 / (math.sqrt(x + 1) + math.sqrt(x)))
v.check("X00.10", 30e9 * 0.02 * 2.5e9 * 0.4e-15)
v.check("X00.11", 100 * 0.995**40)
v.check("X00.12a", 10 + 14)
v.check("X00.12b", (8 + 10 + 15) / 3 + (12 + 14 + 22) / 3)
v.check("X00.13", 40e6 * math.log2(1 + 10**1.5) / 1e6)
v.finish()
