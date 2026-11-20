#!/usr/bin/env python3
"""Verify every number in the Course 14 final-exam solutions.

Independent routes:
- encodings are assembled from their bit fields here and, when LLVM is installed, compared with llvm-mc's own
  encoding and disassembly; floating-point encodings and rounding use Python's struct (IEEE 754 binary32);
- the 2-bit counter is simulated with the 14-07 lab's TwoBit model and by hand-coded saturation here;
- dependences use the 14-08 verify's style of counting (first later writer / most recent earlier writer);
- caches, Sv32 fields, MESI, litmus outcomes, SIMT efficiency and occupancy, and systolic latency come from the
  labs' simulators (14-09, 14-10, 14-12, 14-13, 14-14), each checked against its closed form where one exists;
- performance, Amdahl, AMAT, Little's law, PCIe and the diligence figures are evaluated from their formulas.
"""
from __future__ import annotations

import math
import random
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
for lab in ("14-07-lab", "14-09-lab", "14-10-lab", "14-12-lab", "14-13-lab", "14-14-lab"):
    sys.path.insert(0, str(ROOT / "labs" / lab))
from eeverify import Verifier  # noqa: E402
import bpred  # noqa: E402
import cache  # noqa: E402
import litmus  # noqa: E402
import mesi  # noqa: E402
import simt  # noqa: E402
import systolic  # noqa: E402
import vm  # noqa: E402

v = Verifier.from_files("14-exam", ROOT / "exam" / "solutions.md")

# 1 Performance
v.check("X14.1a", 2e9 * 1.5 / 2.5e9)
v.check("X14.1b", (2e9 * 1.5 / 2.5e9) / (2e9 * 1.1 / 2.0e9))
v.check("X14.1c", 1 / (0.2 + 0.8 / 8))
v.check("X14.1d", 1 / 0.2)
v.check("X14.1e", 100 * (1 - 0.9**2 * 0.9))

# 2 Encoding
word = ((-3) & 0xFFF) << 20 | 6 << 15 | 0 << 12 | 5 << 7 | 0x13
v.check("X14.2a", word)
x = 0x00A28233
fields = dict(op=x & 0x7F, rd=x >> 7 & 31, f3=x >> 12 & 7, rs1=x >> 15 & 31, rs2=x >> 20 & 31, f7=x >> 25)
v.assert_true("decoded word is add (opcode 0x33, funct3 0, funct7 0)", (fields["op"], fields["f3"], fields["f7"]) == (0x33, 0, 0))
v.check("X14.2b", fields["rd"])
v.check("X14.2c", fields["rs1"])
v.check("X14.2d", fields["rs2"])
v.check("X14.2e", 2**12 - 2)
v.check("X14.2f", 2)
mc = shutil.which("llvm-mc") or shutil.which("llvm-mc-18")
if mc:
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "t.s"
        src.write_text("addi x5, x6, -3\nadd x4, x5, x10\nlui x7, 0x12345\naddi x7, x7, 0x678\n")
        out = subprocess.run([mc, "-triple=riscv32", "-show-encoding", str(src)], capture_output=True, text=True, check=True).stdout
    v.assert_true("llvm-mc agrees: addi encodes as 0xFFD30293 and add as 0x00A28233",
                  "[0x93,0x02,0xd3,0xff]" in out.replace(" ", "") and "[0x33,0x82,0xa2,0x00]" in out.replace(" ", ""))
else:
    print("note: llvm-mc not found; encodings checked from bit fields only")
v.assert_true("lui 0x12345 + addi 0x678 builds 0x12345678", (0x12345 << 12) + 0x678 == 0x12345678 and 0x678 < 0x800)

# 3 Calls
v.check("X14.3a", 5 * 100 + 4)
v.check("X14.3b", math.ceil((4 * 4 + 8) / 16) * 16)

# 4 Numbers
s8 = (100 + 50) & 0xFF
v.check("X14.4a", s8 - 256 if s8 & 0x80 else s8)
v.check("X14.4b", int.from_bytes(struct.pack(">f", -6.25), "big"))
v.check("X14.4c", int.from_bytes(struct.pack(">f", -6.25), "big") >> 16)
v.assert_true("bfloat16 truncation is exact here", (int.from_bytes(struct.pack(">f", -6.25), "big") & 0xFFFF) == 0)
v.check("X14.4d", struct.unpack(">f", struct.pack(">I", 0x3F800001))[0] - 1.0)
v.check("X14.4e", struct.unpack(">f", struct.pack(">f", 1 + 2**-24))[0])
q, scale, dq = systolic.quantize([3.81, 1.0, -2.0])
v.check("X14.4f", scale)
v.check("X14.4g", q[1])
v.check("X14.4h", dq[1])

# 5 Datapath
load, rtype = 200 + 100 + 150 + 200 + 25 + 50, 200 + 100 + 150 + 25 + 50
v.check("X14.5a", load)
v.check("X14.5b", rtype)
v.check("X14.5c", 1e12 / load / 1e9)
v.check("X14.5d", 1e12 / 230 / 1e9)
v.check("X14.5e", load / 230)

# 6 Pipeline
v.check("X14.6a", 1000 + 4 + 150 + 2 * 100)
v.check("X14.6b", (1000 + 4 + 150 + 2 * 100) / 1000)

# 7 Branch prediction
outcomes = [1, 1, 0, 1, 0, 0, 1, 1]
t = bpred.TwoBit(1, init=1)
mis = 0
for o in outcomes:
    mis += t.predict(0) != bool(o)
    t.update(0, bool(o))
c, mis2 = 1, 0
for o in outcomes:
    mis2 += (c >= 2) != bool(o)
    c = min(3, c + 1) if o else max(0, c - 1)
v.assert_true("lab TwoBit and hand saturation agree", mis == mis2)
v.check("X14.7a", mis)
v.check("X14.7b", 1 + 0.2 * 0.1 * 15)

# 8 OoO
code = [("lw", "t0", ["a0"]), ("add", "t1", ["t0", "a1"]), ("sub", "t0", ["a2", "a3"]), ("mul", "t2", ["t1", "t0"])]
raw = sum(any(code[i][1] == s for i in range(j)) for j, (_, _, ss) in enumerate(code) for s in set(ss))
war = sum(any(code[k][1] == s for k in range(j + 1, len(code))) for j, (_, _, ss) in enumerate(code) for s in set(ss))
waw = sum(any(code[i][1] == d for i in range(j)) for j, (_, d, _) in enumerate(code))
v.assert_true("3 RAW, 1 WAR, 1 WAW", (raw, war, waw) == (3, 1, 1))
lat = {"lw": 3, "mul": 3}
ready, fin = {}, []
for op, d, ss in code:
    f = max([ready.get(s, 0) for s in ss], default=0) + lat.get(op, 1)
    ready[d] = f
    fin.append(f)
v.check("X14.8a", max(fin))
v.check("X14.8b", 6 * 200)
v.check("X14.8c", 512 / 200)

# 9 Caches
c9 = cache.Cache(16 * 1024, 64, 4)
tag, idx, off = c9.split(0xABCD1234)
v.check("X14.9a", c9.nsets)
v.check("X14.9b", off)
v.check("X14.9c", idx)
v.check("X14.9d", tag)
v.check("X14.9e", 1 + 0.03 * (10 + 0.25 * 120))
tr9 = [(a, False) for a in (0x00, 0x40, 0x10, 0x00, 0x50, 0x40)]
v.check("X14.9f", cache.Cache(64, 16, 1).run(tr9).misses)
v.check("X14.9g", cache.Cache(64, 16, 4).run(tr9).misses)

# 10 Virtual memory
f10 = vm.fields(0xC0FFEE00)
v.check("X14.10a", f10[0])
v.check("X14.10b", f10[1])
v.check("X14.10c", f10[2])
v.check("X14.10d", vm.TLB(128).reach // 1024)
v.check("X14.10e", 128 * vm.MEGA // (1024 * 1024))
v.check("X14.10f", vm.CAUSE["load"])
v.check("X14.10g", 8)

# 11 Coherence, consistency, PCIe
s11 = mesi.System(3).run([(0, 0x100, False), (1, 0x100, False), (0, 0x100, True), (2, 0x100, False), (1, 0x100, True)])
v.check("X14.11a", s11.bus)
v.check("X14.11b", s11.stats["invalidations"])
v.check("X14.11c", len(litmus.outcomes(litmus.SB, "SC")))
v.check("X14.11d", len(litmus.outcomes(litmus.SB, "TSO")))
v.check("X14.11e", 32e9 * 16 * 128 / 130 / 8 / 1e9)

# 12 GPUs
prog = [("if", lambda i: i % 8 == 0, [("op", 24)], [("op", 8)])]
slots, useful = simt.run_warp(prog)
v.assert_true("closed form: 4 x 24 + 28 x 8 useful lane-slots", useful == 4 * 24 + 28 * 8 and slots == 32)
v.check("X14.12a", slots)
v.check("X14.12b", 100 * simt.efficiency(prog))
sec = simt.sectors([0x10000 + 16 * i for i in range(32)])
v.check("X14.12c", sec)
v.check("X14.12d", 100 * 128 / (32 * sec))
warps, _ = simt.occupancy(96, 256, 0)
v.check("X14.12e", warps)
v.check("X14.12f", 100 * warps / 64)

# 13 Derivations
v.check("X14.13a", 100 * 0.03 * 0.25)
v.check("X14.13b", 1 + 0.03 * 10 + 0.03 * 0.25 * 120)
rng = random.Random(2)
A = [[rng.randrange(-5, 6) for _ in range(64)] for _ in range(8)]
B = [[rng.randrange(-5, 6) for _ in range(8)] for _ in range(64)]
C, cyc, macs = systolic.run(A, B, 8)
v.assert_true("systolic simulation: correct product in K + M + N - 2 cycles",
              cyc == 64 + 8 + 8 - 2 and C == [[sum(A[i][k] * B[k][j] for k in range(64)) for j in range(8)] for i in range(8)])
v.check("X14.13c", cyc)
v.check("X14.13d", 100 * systolic.utilization(8, 64, 8, 8, cyc))
v.check("X14.13e", simt.warps_to_hide(600, 15))

# 14 Diligence
dense = 4000 / 2 / 2 / 2
v.check("X14.14a", dense)
v.check("X14.14b", dense / 989.5)
v.check("X14.14c", dense * 1e12 / 2e12)
v.check("X14.14d", 2e12 / (70e9 * 2))
v.check("X14.14e", 2e12 / (70e9 * 0.5))
v.check("X14.14f", 500 / (2e12 / (70e9 * 0.5)))

sys.exit(v.finish())
