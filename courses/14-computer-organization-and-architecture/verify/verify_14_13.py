#!/usr/bin/env python3
"""Verify every number in chapter 14-13, its problem set and its lab.

Independent routes:
- SIMD efficiencies come from the lab's masked warp executor (labs/14-13-lab/simt.py) and are re-derived here
  from lane counts per path (sum of path lengths for divergent branches; maximum trip count for loops);
- sector counts from simt.sectors are checked against the closed form min(32, 4 * stride) for strides of 4-byte
  elements in a 32-thread warp (with 32-byte sectors), and bank conflicts against gcd(stride, 32);
- occupancy is recomputed here directly from the resource limits;
- peak, ridge-point and timing figures are evaluated from the vendor numbers logged in R-220 and R-221.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(ROOT / "labs" / "14-13-lab"))
from eeverify import Verifier  # noqa: E402
import simt  # noqa: E402

v = Verifier.from_files("14-13", ROOT / "chapters" / "14-13-gpus-and-simt.md",
                        ROOT / "solutions" / "14-13-solutions.md", ROOT / "labs" / "14-13-lab" / "README.md")
FP32, BF16_SPARSE, BW = 67e12, 1979e12, 3.35e12
SMS, LANES = 132, 128


def branch(pred, a, b):
    return [("if", pred, [("op", a)], [("op", b)])]


def eff_closed(groups):
    """groups: list of (lanes, path length) for paths a warp executes one after the other."""
    slots = sum(n for _, n in groups)
    return sum(k * n for k, n in groups) / (32 * slots), slots


# Example 1 and Problem 2
v.check("Ex 14-13.1a", SMS * LANES)
v.check("Ex 14-13.1b", FP32 / (SMS * LANES * 2) / 1e9)
v.check("Ex 14-13.1c", BF16_SPARSE / 2 / 1e12)
v.check("Ex 14-13.1d", BF16_SPARSE / 2 / FP32)
v.check("14-13.2a", 100 * 128 * 2 * 1.8e9 / 1e12)

# Example 2 and Problems 3, 4
for idc, pred, groups in (("b", lambda i: i % 4 == 0, [(8, 20), (24, 10)]), ("c", lambda i: i < 16, [(16, 20), (16, 10)])):
    e, slots = eff_closed(groups)
    v.assert_true(f"Example 2{idc}: executor equals closed form", abs(simt.efficiency(branch(pred, 20, 10)) - e) < 1e-12
                  and simt.run_warp(branch(pred, 20, 10))[0] == slots == 30)
    v.check(f"Ex 14-13.2{idc}", 100 * e)
v.check("Ex 14-13.2a", simt.run_warp(branch(lambda i: i % 4 == 0, 20, 10))[0])
loop = [("loop", lambda i: i, [("op", 1)])]
v.check("Ex 14-13.2d", simt.run_warp(loop)[0])
v.check("Ex 14-13.2e", 100 * simt.efficiency(loop))
v.assert_true("loop closed form: 496 / (31 x 32)", simt.efficiency(loop) == sum(range(32)) / (31 * 32))
v.assert_true("uniform branch: 100%", simt.efficiency(branch(lambda i: True, 20, 10)) == 1.0)
nested = [("if", lambda i: i < 16, [("if", lambda i: i < 8, [("op", 10)], [("op", 10)])], [("op", 10)])]
s3, _ = simt.run_warp(nested)
e3, slots3 = eff_closed([(8, 10), (8, 10), (16, 10)])
v.assert_true("Problem 3: executor equals closed form", s3 == slots3 and abs(simt.efficiency(nested) - e3) < 1e-12)
v.check("14-13.3a", s3)
v.check("14-13.3b", 100 * simt.efficiency(nested))
loop4 = [("loop", lambda i: i % 8 + 1, [("op", 1)])]
v.check("14-13.4a", simt.run_warp(loop4)[0])
v.check("14-13.4b", 100 * simt.efficiency(loop4))
v.assert_true("Problem 4 closed form: mean 4.5 / max 8", simt.efficiency(loop4) == 4.5 / 8)
v.check("14-13.1a", math.ceil(200 / 32))
v.check("14-13.1b", 200 - 6 * 32)
v.check("14-13.1c", 100 * 200 / (7 * 32))

# Example 3 and Problems 5, 6
for idc, stride in (("a", 1), ("c", 2), ("e", 32)):
    n = simt.sectors([0x10000 + 4 * stride * t for t in range(32)])
    v.assert_true(f"stride {stride}: sectors = min(32, 4 x stride)", n == min(32, 4 * stride))
    v.check(f"Ex 14-13.3{idc}", n)
    v.check(f"Ex 14-13.3{chr(ord(idc) + 1)}", 100 * 128 / (32 * n))
aos = simt.sectors([0x10000 + 16 * t for t in range(32)])
soa = simt.sectors([0x10000 + 4 * t for t in range(32)])
v.check("14-13.5a", aos)
v.check("14-13.5b", 100 * 128 / (32 * aos))
v.check("14-13.5c", soa)
v.check("14-13.6a", simt.sectors([0x10000 + 128 * t for t in range(32)]))
v.check("14-13.6b", simt.sectors([0x10000 + 4 * t for t in range(32)]))
v.check("14-13.6c", simt.bank_conflict([32 * t for t in range(32)]))
v.check("14-13.6d", simt.bank_conflict([33 * t for t in range(32)]))

# Example 4 and Problem 7
for idc, s in (("a", 1), ("b", 2), ("c", 32), ("d", 33)):
    d = simt.bank_conflict([s * t for t in range(32)])
    v.assert_true(f"stride {s}: conflict degree = gcd(s, 32)", d == math.gcd(s, 32))
    v.check(f"Ex 14-13.4{idc}", d)
v.assert_true("strides 1..64 all match gcd", all(simt.bank_conflict([s * t for t in range(32)]) == math.gcd(s, 32) for s in range(1, 65)))
for idc, s in (("a", 3), ("b", 6), ("c", 64)):
    v.check(f"14-13.7{idc}", simt.bank_conflict([s * t for t in range(32)]))


# Example 5 and Problem 8: occupancy, recomputed directly
def occ(regs, threads, smem):
    wpb = threads // 32
    blocks = min(65536 // (regs * threads), (196608 // smem) if smem else 32, 64 // wpb, 32)
    return blocks * wpb


for idc, regs in (("a", 64), ("c", 32)):
    w = occ(regs, 256, 32768)
    v.assert_true(f"occupancy {regs} registers: lab model agrees", simt.occupancy(regs, 256, 32768)[0] == w)
    v.check(f"Ex 14-13.5{idc}", w)
    v.check(f"Ex 14-13.5{chr(ord(idc) + 1)}", 100 * w / 64)
v.assert_true("limits: registers at 64, shared memory at 32", simt.occupancy(64, 256, 32768)[1] == "registers"
              and simt.occupancy(32, 256, 32768)[1] == "shared memory")
for idc, regs in (("a", 128), ("c", 40)):
    w = occ(regs, 128, 0)
    v.assert_true(f"Problem 8, {regs} registers: lab model agrees", simt.occupancy(regs, 128, 0)[0] == w)
    v.check(f"14-13.8{idc}", w)
    v.check(f"14-13.8{chr(ord(idc) + 1)}", 100 * w / 64)

# Example 6 and Problems 9-12
v.check("Ex 14-13.6a", simt.warps_to_hide(500, 10))
v.check("Ex 14-13.6b", simt.warps_to_hide(500, 40))
v.check("Ex 14-13.6c", FP32 / BW)
v.check("Ex 14-13.6d", BW / 12 / 1e12)
v.check("Ex 14-13.6e", 100 * (BW / 12) / FP32)
v.check("Ex 14-13.6f", BF16_SPARSE / 2 / BW)
v.check("14-13.9a", simt.warps_to_hide(400, 20))
v.check("14-13.9b", simt.warps_to_hide(400, 40))
v.check("14-13.10a", BW * 2 / 12 / 1e12)
n = 4096
v.check("14-13.10b", 2 * n**3 / (3 * n * n * 4))
v.assert_true("GEMM intensity above the 20 FLOP/B ridge", 2 * n**3 / (3 * n * n * 4) > FP32 / BW)
rate = 0.4 * BF16_SPARSE / 2
t1 = 1e21 / rate
v.check("14-13.11a", rate / 1e12)
v.check("14-13.11b", t1 / 86400)
v.check("14-13.11c", t1 / 1024 / 60)
v.check("14-13.11d", 2)
v.check("14-13.12a", 13.4e3 / 72)
v.check("14-13.12b", 576 / 72)
v.check("14-13.12c", 1440 / 8)
v.check("14-13.12d", 64 / 8)
v.check("14-13.12e", 8 / 3.35)

# Lab
v.check("Lab 14-13.a", simt.bank_conflict([16 * t for t in range(32)]))
v.check("Lab 14-13.b", simt.bank_conflict([48 * t for t in range(32)]))
v.check("Lab 14-13.c", 100 * simt.efficiency(branch(lambda i: i % 2 == 0, 10, 10)))
v.assert_true("lab Part 4: 256-thread blocks, no shared memory: registers limit exactly above 32 per thread",
              all((simt.occupancy(r, 256, 0)[1] == "registers") == (65536 // (r * 256) < 8) for r in range(16, 256))
              and simt.occupancy(33, 256, 0)[0] < 64 <= simt.occupancy(32, 256, 0)[0])
v.check("Lab 14-13.d", simt.sectors([0x10000 + 4 * 3 * t for t in range(32)]))

sys.exit(v.finish())
