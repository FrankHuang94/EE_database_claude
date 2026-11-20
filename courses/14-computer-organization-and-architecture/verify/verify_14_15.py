#!/usr/bin/env python3
"""Verify every number in chapter 14-15, its problem set and its lab.

Independent routes:
- roofline quantities use the vendor figures logged in R-220 and R-222 through labs/14-15-lab/roofline.py, and
  are recomputed here directly from min(peak, bandwidth x intensity);
- SPEC ratios reproduce SPEC's own worked examples (R-223) to the digits SPEC prints (5.009458 exactly; the
  SPECrate example to 6 significant figures), and the geometric-mean property gmean(x/y) = gmean(x)/gmean(y) is
  checked on the examples;
- every mean and throughput is evaluated from its definition.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(ROOT / "labs" / "14-15-lab"))
from eeverify import Verifier  # noqa: E402
import roofline as rf  # noqa: E402

v = Verifier.from_files("14-15", ROOT / "chapters" / "14-15-roofline-and-benchmarks.md",
                        ROOT / "solutions" / "14-15-solutions.md", ROOT / "labs" / "14-15-lab" / "README.md")
FP32, BF16, BW = 67e12, 989.5e12, 3.35e12
V4, V4BW = 275e12, 1.2e12
roof = lambda p, b, i: min(p, b * i)  # noqa: E731
v.assert_true("lab machine table matches the logged figures",
              rf.MACHINES["H100 SXM, FP32"] == (FP32, BW) and rf.MACHINES["H100 SXM, BF16 dense"] == (BF16, BW)
              and rf.MACHINES["TPU v4, BF16"] == (V4, V4BW))

# Example 1
v.check("Ex 14-15.1a", FP32 / BW)
v.check("Ex 14-15.1b", BF16 / BW)
v.check("Ex 14-15.1c", roof(FP32, BW, 4) / 1e12)
# Example 2
for idc, (f, b) in (("a", (1, 12)), ("b", (2, 12)), ("c", (8, 8))):
    v.check(f"Ex 14-15.2{idc}", roof(FP32, BW, f / b) / 1e12)
    v.assert_true(f"lab attainable agrees ({idc})", rf.attainable(FP32, BW, f / b) == roof(FP32, BW, f / b))
gi = rf.gemm_intensity(4096)
v.assert_true("GEMM intensity n/6 = 682.7", round(gi, 1) == 682.7 == round(4096 / 6, 1))
v.check("Ex 14-15.2d", roof(FP32, BW, gi) / 1e12)
v.check("Ex 14-15.2e", 100 * roof(FP32, BW, 1 / 12) / FP32)
v.assert_true("§3.2 table intensities 0.083, 0.167, 1, 1", [round(f / b, 3) for f, b in rf.KERNELS.values()] == [0.083, 0.167, 1.0, 1.0])
# with write-allocate each store also reads its line: vector add 4 + 4 + (4 + 4) bytes, stencil 4 + (4 + 4)
v.check("Txt 14-15.a", rf.intensity(1, 4 + 4 + 2 * 4))
v.check("Txt 14-15.b", rf.intensity(8, 4 + 2 * 4))
# Example 3
r1, r2 = rf.spec_ratio(1775, 354.329738), rf.spec_ratio(1592, 541.52471, 8)
v.assert_true("SPEC's worked examples: 5.009458 and 23.5188 (SPEC prints 23.518776)",
              round(r1, 6) == 5.009458 and round(r2, 4) == 23.5188)
v.check("Ex 14-15.3a", r1)
v.check("Ex 14-15.3b", r2)
v.check("Ex 14-15.3c", rf.gmean([4, 9, 16]))
v.check("Ex 14-15.3d", rf.amean([4, 9, 16]))
# Example 4
a, b = [10, 40], [20, 20]
v.check("Ex 14-15.4a", rf.amean([y / x for x, y in zip(a, b)]))
v.check("Ex 14-15.4b", rf.amean([x / y for x, y in zip(a, b)]))
v.check("Ex 14-15.4c", rf.gmean([y / x for x, y in zip(a, b)]))
v.assert_true("gmean of ratios = ratio of gmeans; totals 50 and 40 s",
              abs(rf.gmean([y / x for x, y in zip(a, b)]) - rf.gmean(b) / rf.gmean(a)) < 1e-12 and (sum(a), sum(b)) == (50, 40))
# Example 5
gi_int, gi_fp = rf.gmean([2000, 3000, 2500]), rf.gmean([4000, 1000])
v.check("Ex 14-15.5a", gi_int)
v.check("Ex 14-15.5b", gi_fp)
v.check("Ex 14-15.5c", 0.65 * gi_int + 0.35 * gi_fp)
# Example 6
v.check("Ex 14-15.6a", 1 / 0.020)
v.check("Ex 14-15.6b", 32 / 0.080)
v.check("Ex 14-15.6c", (32 / 0.080) / (1 / 0.020))
v.check("Ex 14-15.6d", 80 / 20)

# Problems
v.check("14-15.1a", V4 / V4BW)
v.check("14-15.1b", roof(V4, V4BW, 50) / 1e12)
v.check("14-15.2a", 2 / 4)
v.check("14-15.2b", roof(FP32, BW, 0.5) / 1e12)
v.check("14-15.3a", 2 / (12 + 8))
v.check("14-15.3b", 2 / 12)
v.check("14-15.3c", 20 / 12)
v.check("14-15.4a", 2 / 6)
v.check("14-15.4b", BW * 2 / 6 / 1e12)
v.check("14-15.4c", (2 / 6) / (2 / 12))
ratios = [1000 / 250, 2000 / 400, 3000 / 1000]
v.assert_true("ratios 4, 5, 3", ratios == [4, 5, 3])
v.check("14-15.5a", rf.gmean(ratios))
v.check("14-15.5b", rf.spec_ratio(1000, 400, 16))
v.check("14-15.6a", rf.hmean([100, 400]))
v.check("14-15.6b", rf.amean([100, 400]))
a7, b7 = [2, 8, 4], [4, 4, 4]
v.check("14-15.7a", rf.amean([y / x for x, y in zip(a7, b7)]))
v.check("14-15.7b", rf.amean([x / y for x, y in zip(a7, b7)]))
v.check("14-15.7c", rf.gmean([y / x for x, y in zip(a7, b7)]))
bmax = max(b for b in range(1, 1000) if 10 + 2 * b <= 50)
v.check("14-15.8a", bmax / ((10 + 2 * bmax) / 1000))
v.check("14-15.8b", 128 / ((10 + 2 * 128) / 1000))
x_eq = 4000 / 2 / 2 / 2
v.check("14-15.9a", x_eq)
v.check("14-15.9b", 4000 / 989.5)
v.check("14-15.9c", x_eq / 989.5)
v.check("14-15.10a", 500 / 700)
v.check("14-15.10b", 300 / 300)
v.check("14-15.10c", 700 / 300)
v.check("14-15.10d", 700 / 300 * 300)

# Lab
v.check("Lab 14-15.a", roof(*rf.MACHINES["TPU7x, BF16"], 1) / 1e12)
v.check("Lab 14-15.b", rf.ridge(*rf.MACHINES["TPU7x, BF16"]))
v.check("Lab 14-15.c", roof(V4, V4BW, 1) / 1e12)

# Problem 11: Geekbench 6 composite (weighted arithmetic mean, R-225) and subsection geometric means
gb = lambda i, f: 0.65 * i + 0.35 * f  # noqa: E731
v.check("14-15.11a", 250)
v.check("14-15.11b", gb(3000, 2000))
v.check("14-15.11c", 100 * (gb(3000, 2400) / gb(3000, 2000) - 1))
w4 = [1000.0, 1500.0, 2200.0, 3100.0]
v.check("14-15.11d", 100 * (rf.gmean([2 * w4[0]] + w4[1:]) / rf.gmean(w4) - 1))

sys.exit(v.finish())
