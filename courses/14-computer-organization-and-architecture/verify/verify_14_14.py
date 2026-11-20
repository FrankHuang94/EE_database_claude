#!/usr/bin/env python3
"""Verify every number in chapter 14-14, its problem set and its lab.

Independent routes:
- the systolic-array cycle counts are produced by the cycle-accurate Python simulator (labs/14-14-lab/systolic.py),
  checked here against the closed form K + M + N - 2 on random shapes and against the product computed directly;
  the Verilog 4 x 4 array's self-checking testbench is run under Icarus when available and must report the same
  cycle counts (10 and 22);
- quantization results are recomputed here with NumPy-free arithmetic and the SQNR formula 6.02 b + 1.76 dB;
- energies, intensities, ridge points and timings are evaluated from the logged figures (R-208, R-220, R-222).
"""
from __future__ import annotations

import math
import random
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "14-14-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import systolic  # noqa: E402

v = Verifier.from_files("14-14", ROOT / "chapters" / "14-14-ai-accelerators.md",
                        ROOT / "solutions" / "14-14-solutions.md", LAB / "README.md")
V4, V4BW, V5P, V5PBW, IW, IWBW = 275e12, 1.2e12, 459e12, 2765e9, 2307e12, 7380e9
H100D, H100BW = 1979e12 / 2, 3.35e12
E_MAC, E_SRAM_B, E_DRAM_B = 0.2 + 0.03, 20 / 8, 1300 / 8


def sim(M, K, N, P, seed=1):
    rng = random.Random(seed)
    A = [[rng.randrange(-9, 10) for _ in range(K)] for _ in range(M)]
    B = [[rng.randrange(-9, 10) for _ in range(N)] for _ in range(K)]
    C, cyc, macs = systolic.run(A, B, P)
    assert C == [[sum(A[i][k] * B[k][j] for k in range(K)) for j in range(N)] for i in range(M)]
    return cyc, macs


rng = random.Random(9)
shapes = [(rng.randint(1, 6), rng.randint(1, 20), rng.randint(1, 6)) for _ in range(25)]
v.assert_true("simulator: correct products and cycles = K + M + N - 2 on 25 random shapes",
              all(sim(M, K, N, 6)[0] == K + M + N - 2 and sim(M, K, N, 6)[1] == M * K * N for M, K, N in shapes))

# Verilog
if shutil.which("iverilog") and shutil.which("vvp"):
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "tb"
        subprocess.run(["iverilog", "-g2012", "-o", str(out), str(LAB / "systolic4_tb.v"), str(LAB / "systolic4.v")], check=True)
        log = subprocess.run(["vvp", str(out)], capture_output=True, text=True, check=True).stdout
    m = re.search(r"CYCLES K4=(\d+) K16=(\d+)", log)
    v.assert_true("Verilog array: TEST PASSED with 10 and 22 cycles", "TEST PASSED" in log and m and m.groups() == ("10", "22"))
else:
    print("note: iverilog not found; tools/run_hdl.py checks the Verilog array in CI")

# Example 1 and Problem 1
macs = 2 * 4 * 128 * 128
v.check("Ex 14-14.1a", macs)
v.check("Ex 14-14.1b", macs * 2 * 1.05e9 / 1e12)
v.check("Ex 14-14.1c", H100D / (macs * 2 * 1.05e9))
v.check("14-14.1a", 256 * 256)
v.check("14-14.1b", 256 * 256 * 2 * 0.94e9 / 1e12)

# Example 2 and Problems 2, 10
for idc, K in (("a", 4), ("c", 16)):
    cyc, mc = sim(4, K, 4, 4)
    v.check(f"Ex 14-14.2{idc}", cyc)
    v.check(f"Ex 14-14.2{chr(ord(idc) + 1)}", 100 * systolic.utilization(4, K, 4, 4, cyc))
v.check("Ex 14-14.2e", 100 * 1000 / (1000 + 254))
cyc2, _ = sim(8, 32, 8, 8)
v.check("14-14.2a", cyc2)
v.check("14-14.2b", 100 * systolic.utilization(8, 32, 8, 8, cyc2))
c100, _ = sim(4, 100, 4, 4)
v.check("14-14.10a", c100)
v.check("14-14.10b", 100 * 100 / c100)
k90 = next(K for K in range(1, 1000) if K / (K + 6) >= 0.9)
v.check("14-14.10c", k90)

# Example 3 and Problem 4
v.check("Ex 14-14.3a", systolic.tiled_cycles(1024, 1024, 1024, 128))
v.check("Ex 14-14.3b", 1024**3 // 128**2)
v.check("Ex 14-14.3c", 100 * 1024**3 / 128**2 / systolic.tiled_cycles(1024, 1024, 1024, 128))
t4 = systolic.tiled_cycles(2048, 512, 2048, 128)
ideal4 = 2048 * 512 * 2048 // 128**2
v.check("14-14.4a", t4)
v.check("14-14.4b", 100 * ideal4 / t4)
ov = 16 * 16 * 512 + 2 * 127
v.check("14-14.4c", ov)
v.check("14-14.4d", 100 * ideal4 / ov)

# Example 4 and Problem 5
v.check("Ex 14-14.4a", 2 * E_SRAM_B)
v.check("Ex 14-14.4b", math.ceil(2 * E_SRAM_B / E_MAC))
v.check("Ex 14-14.4c", 2 * E_DRAM_B)
v.check("Ex 14-14.4d", math.ceil(2 * E_DRAM_B / E_MAC))
for idc, B in (("a", 1), ("b", 16), ("c", 256)):
    v.check(f"14-14.5{idc}", E_DRAM_B / B + E_SRAM_B / 128)
v.assert_true("solution 5: 707x the MAC at B = 1, 2.8x at B = 256", round((E_DRAM_B + E_SRAM_B / 128) / E_MAC) == 707
              and round((E_DRAM_B / 256 + E_SRAM_B / 128) / E_MAC, 1) == 2.8)

# Example 5 and Problems 6, 7
xs = [math.sin(2 * math.pi * k / 64) for k in range(64)]


def sqnr(x, bits):
    q, s, dq = systolic.quantize(x, bits)
    err = [a - b for a, b in zip(x, dq)]
    return s, max(abs(e) for e in err), 10 * math.log10(sum(a * a for a in x) / sum(e * e for e in err))


s8, e8, n8 = sqnr(xs, 8)
s4, e4, n4 = sqnr(xs, 4)
v.assert_true("errors within half a step", e8 <= s8 / 2 and e4 <= s4 / 2)
v.check("Ex 14-14.5a", s8)
v.check("Ex 14-14.5b", e8)
v.check("Ex 14-14.5c", n8)
v.check("Ex 14-14.5d", 6.02 * 8 + 1.76)
v.check("Ex 14-14.5e", s4)
v.check("Ex 14-14.5f", e4)
v.check("Ex 14-14.5g", n4)
v.assert_true("4-bit formula 25.8 dB", round(6.02 * 4 + 1.76, 1) == 25.8)
x6 = [0.5, -1.2, 0.031, 2.54, -2.54, 1.0]
q6, s6, d6 = systolic.quantize(x6)
v.assert_true("Problem 6 integers", q6 == [25, -60, 2, 127, -127, 50])
v.check("14-14.6a", s6)
v.check("14-14.6b", max(abs(a - b) for a, b in zip(x6, d6)))
v.check("14-14.7a", 6.02 * 6 + 1.76)
for idc, bytes_per in (("b", 2), ("c", 1), ("d", 0.5)):
    v.check(f"14-14.7{idc}", 7e9 * bytes_per / 1e9)

# Example 6 and Problems 3, 8, 11, 12
v.check("Ex 14-14.6a", 2 / 2)
v.check("Ex 14-14.6b", V4 / V4BW)
v.check("Ex 14-14.6c", IW / IWBW)
v.check("Ex 14-14.6d", V4BW / 14e9)
v.check("Ex 14-14.6e", 100 * V4BW * 1.0 / V4)
v.check("Ex 14-14.6f", IWBW / 14e9)
v.check("Ex 14-14.6g", math.ceil(V4 / V4BW))
v.assert_true("HBM bandwidth grew about sixfold from v4 to TPU7x", round(IWBW / V4BW) == 6)
v.check("14-14.3a", 512 / 3)
v.check("14-14.3b", math.ceil(3 * V4 / V4BW))
v.check("14-14.8a", V5PBW / 14e9)
v.check("14-14.8b", V5PBW / 7e9)
v.check("14-14.8c", V5P / V5PBW)
v.check("14-14.9a", 2000 / 2)
v.check("14-14.9b", 1 / (0.2 + 0.8 / 2))
t11 = 1e25 / (9216 * IW * 0.4)
v.check("14-14.11a", t11 / 86400)
ridges = {"TPU v5p": V5P / V5PBW, "TPU v4": V4 / V4BW, "H100": H100D / H100BW, "TPU7x": IW / IWBW}
v.assert_true("ranking by ridge: v5p < v4 < H100 < TPU7x", sorted(ridges, key=ridges.get) == ["TPU v5p", "TPU v4", "H100", "TPU7x"])
v.check("14-14.12a", ridges["TPU v5p"])
v.check("14-14.12b", ridges["H100"])
v.check("14-14.12c", IWBW / 1e9)

# Lab
v.check("Lab 14-14.a", sim(3, 5, 2, 4)[0])
v.check("Lab 14-14.b", sim(8, 100, 8, 8)[0])
v.check("Lab 14-14.c", sqnr(xs, 6)[2])

sys.exit(v.finish())
