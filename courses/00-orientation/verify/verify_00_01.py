#!/usr/bin/env python3
"""Verify every published number in chapter 00-01, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "00-01",
    COURSE / "chapters" / "00-01-map-of-electrical-engineering.md",
    COURSE / "solutions" / "00-01-solutions.md",
    COURSE / "labs" / "00-01-lab" / "README.md",
)
k = 1.380649e-23
shannon = lambda B, snr_db: B * math.log2(1 + 10 ** (snr_db / 10))  # noqa: E731
# WSTS 2025, US$ millions (R-016)
SEG = {"logic": 299547, "memory": 230042, "analog": 86519, "micro": 84867, "opto": 43042, "discretes": 30728,
       "sensors": 20894}
TOTAL = 795640
v.assert_true("WSTS segments sum to the published total (within $1 M rounding)", abs(sum(SEG.values()) - TOTAL) <= 1)

E = 4.0 * 3.85
v.check("Ex 00-01.1a", E)
v.check("Ex 00-01.1b", E * 3600 / 1e3)
v.check("Ex 00-01.1c", E / 24)
v.check("Ex 00-01.2a", 5e-12 * 112e9)
v.check("Ex 00-01.2b", 64 * 5e-12 * 112e9)
L300 = k * 300 * math.log(2)
v.check("Ex 00-01.3a", L300)
v.check("Ex 00-01.3b", 1e-15 / L300)
v.check("Ex 00-01.4a", 100 * SEG["memory"] / TOTAL)
v.check("Ex 00-01.4b", 100 * (SEG["logic"] + SEG["memory"]) / TOTAL)
v.check("Ex 00-01.4c", SEG["logic"] / 1.388 / 1e3)
v.check("Ex 00-01.5a", shannon(20e6, 30) / 1e6)

Ew = 0.300 * 3.85
v.check("00-01.2a", Ew)
v.check("00-01.2b", Ew * 3600)
v.check("00-01.2c", Ew / 48 * 1e3)
v.assert_true("watch draws ~27x less than the phone (0.642 W)", round(0.642 / (Ew / 48)) == 27)
Pc = 9 * 2.22
v.check("00-01.3a", Pc)
v.check("00-01.3b", Pc * 1800 / 1e3)
v.check("00-01.3c", Pc * 0.5)
v.check("00-01.4a", 15e-12 * 400e9)
v.check("00-01.4b", 64 * 15e-12 * 400e9)
v.check("00-01.5a", k * 77 * math.log(2))
v.check("00-01.5b", 0.1e-15 / L300)
v.check("00-01.6a", shannon(80e6, 25) / 1e6)
v.check("00-01.6b", shannon(160e6, 25) / 1e6)
v.check("00-01.6c", 80e6 * math.log2(1 + 2 * 10**2.5) / 1e6)
v.check("00-01.7a", 795.6 / 1.262)
v.check("00-01.7b", 299.5 / 86.5)
v.check("00-01.8a", 18.497e9 / 42000 / 1e3)
v.check("00-01.8b", 1.77e9 / 24500 / 1e3)
v.check("00-01.9a", 0.6 / 0.75 * 60)
v.check("00-01.9b", 0.6 / 0.5 * 60)
eff = 0.98 * 0.96 * 0.94 * 0.90
v.check("00-01.10a", 100 * eff)
v.check("00-01.10b", 1 / eff)
v.check("00-01.10c", (1 / eff - 1) * 1e3)

# lab predictions
v.check("Lab 00-01.1", shannon(80e6, 20) / 1e6)
v.check("Lab 00-01.2", shannon(20e6, 40) / 1e6)

v.finish()
