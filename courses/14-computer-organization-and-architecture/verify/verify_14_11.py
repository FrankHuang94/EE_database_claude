#!/usr/bin/env python3
"""Verify every number in chapter 14-11, its problem set and its lab.

Independent routes:
- the AXI4-Lite register block's cycle counts are measured by running its self-checking testbench under Icarus
  Verilog (when installed) and parsing the CYCLES line; they must equal the closed form 2 + k cycles per write
  (k = response delay) that the chapter derives from the handshake rules;
- mesh hop counts are computed by enumerating every source-destination pair (io_models.mesh_hops) and compared
  with the closed form 2(k^2 - 1)/(3k);
- every other quantity (UART timing, overheads, DMA, bus and link bandwidth, Little's law) is evaluated from its
  formula, with link rates and encodings taken from the research log (R-216, R-217).
"""
from __future__ import annotations

import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "14-11-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import io_models as io  # noqa: E402

v = Verifier.from_files("14-11", ROOT / "chapters" / "14-11-io-buses-and-interconnect.md",
                        ROOT / "solutions" / "14-11-solutions.md", LAB / "README.md")

# ---------------------------------------------------------------------------------------------------------------
# The AXI4-Lite testbench
W_CYC, R_CYC, STALL_CYC = 16, 16, 5            # what the chapter states; checked against Icarus when available
if shutil.which("iverilog") and shutil.which("vvp"):
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "tb"
        subprocess.run(["iverilog", "-g2012", "-o", str(out), str(LAB / "axil_regs_tb.v"), str(LAB / "axil_regs.v")], check=True)
        log = subprocess.run(["vvp", str(out)], capture_output=True, text=True, check=True).stdout
    m = re.search(r"CYCLES writes=(\d+) reads=(\d+) stalled_write=(\d+)", log)
    v.assert_true("testbench passes and reports 16, 16 and 5 cycles",
                  "TEST PASSED" in log and m is not None and tuple(map(int, m.groups())) == (W_CYC, R_CYC, STALL_CYC))
else:
    print("note: iverilog not found; the Verilog measurement is checked by tools/run_hdl.py in CI")
v.assert_true("closed form 2 + k per write: 8 writes = 16 cycles, k = 3 gives 5", 8 * (2 + 0) == W_CYC and 2 + 3 == STALL_CYC)

# ---------------------------------------------------------------------------------------------------------------
# Examples
t_char = io.uart_time(1, 115200)
v.check("Ex 14-11.1a", t_char * 1e6)
v.check("Ex 14-11.1b", io.uart_time(1000, 115200) * 1e3)
v.check("Ex 14-11.1c", io.uart_time(1000, 115200) * 100e6 / 1e6)

pps = 1e9 / (1500 * 8)
v.check("Ex 14-11.2a", pps)
v.check("Ex 14-11.2b", 100 * io.overhead_fraction(pps, 2000, 3e9))
v.check("Ex 14-11.2c", 100 * io.overhead_fraction(pps / 32, 2000, 3e9))
v.check("Ex 14-11.2d", 31 * 1500 * 8 / 1e9 * 1e6)
v.assert_true("2604 interrupts per second with coalescing", round(pps / 32) == 2604)

pio = 4096 // 4 * 50
v.check("Ex 14-11.3a", pio)
v.check("Ex 14-11.3b", 300 + 2000)
v.check("Ex 14-11.3c", 100 * (1 - 2300 / pio))
v.check("Ex 14-11.3d", 4096 // 64)
v.check("Ex 14-11.3e", len({a // 64 for a in range(32, 32 + 4096)}))       # a buffer starting mid-line
v.assert_true("64-byte transfer: PIO 800 cycles < DMA 2300", 64 // 4 * 50 == 800 < 2300)

v.check("Ex 14-11.4a", W_CYC / 8)
v.check("Ex 14-11.4b", 4 / (W_CYC / 8 * 10e-9) / 1e6)
v.check("Ex 14-11.4c", STALL_CYC)
v.check("Ex 14-11.4d", io.outstanding_needed(16e9, 200e-9, 64))

h8, bis8 = io.mesh_hops(8)
v.assert_true("enumeration equals 2(k^2-1)/(3k) for k = 2..16",
              all(abs(io.mesh_hops(k)[0] - 2 * (k * k - 1) / (3 * k)) < 1e-12 for k in range(2, 17)))
v.check("Ex 14-11.5a", h8)
v.check("Ex 14-11.5b", h8 * (3 + 1))
v.check("Ex 14-11.5c", bis8 * 32 * 2e9 / 1e9)
v.check("Ex 14-11.5d", io.link_bandwidth(8, 16, 128 / 130) / 1e9)
v.check("Ex 14-11.5e", io.link_bandwidth(64, 16) / 1e9)
v.assert_true("PCI-SIG's 256 GB/s is the bidirectional total", 2 * io.link_bandwidth(64, 16) == 256e9)

# ---------------------------------------------------------------------------------------------------------------
# Problems
v.check("14-11.1a", 0x4000_2000 + 0x0C)
v.check("14-11.2a", io.uart_time(1, 9600) * 1e3)
v.check("14-11.2b", 9600 / 10)
rate = 115200 / 10
v.check("14-11.3a", 16 / rate * 1e3)
v.check("14-11.3b", 100 * io.overhead_fraction(rate / 16, 200, 48e6))
v.check("14-11.4a", (1 / 10e-6) * 100 / 1500)
v.check("14-11.5a", 65536 // 4 * 40)
v.check("14-11.5b", 500 + 1500)
v.check("14-11.5c", 65536 // 64)
t6 = 100 * (2 + 1) / 200e6
v.check("14-11.6a", t6 * 1e6)
v.check("14-11.6b", 400 / t6 / 1e6)
v.check("14-11.6c", 4 * 200e6 / 1e6)
v.check("14-11.7a", 16 * 1e9 / 1e9)
v.check("14-11.7b", 100 * 16 / 20)
v.check("14-11.7c", 16 * 16 / 20)
h4, b4 = io.mesh_hops(4)
h16, b16 = io.mesh_hops(16)
v.check("14-11.8a", h4)
v.check("14-11.8b", h16)
v.check("14-11.8c", h16 * 4)
v.check("14-11.8d", b16 / b4)
v.check("14-11.8e", 16 * 16 / (4 * 4))
v.check("14-11.9a", io.link_bandwidth(16, 4, 128 / 130) / 1e9)
v.check("14-11.9b", io.link_bandwidth(32, 4, 128 / 130) / 1e9)
v.check("14-11.9c", io.link_bandwidth(128, 16) / 1e9)
v.check("14-11.10a", io.outstanding_needed(64e9, 1e-6, 256))
v.check("14-11.10b", 64 * 256 / 1e-6 / 1e9)
fill = 32 * 1500 * 8 / 1e9
v.assert_true("32 packets take 384 µs, longer than the 50 µs timeout", round(fill * 1e6) == 384 and fill > 50e-6)
v.check("14-11.11a", 1 / 50e-6)
v.check("14-11.11b", 100 * io.overhead_fraction(1 / 50e-6, 2000, 3e9))
v.check("14-11.11c", 50)

# Lab
v.check("Lab 14-11.a", W_CYC)
v.check("Lab 14-11.b", R_CYC)
v.check("Lab 14-11.c", STALL_CYC)
v.check("Lab 14-11.d", io.mesh_hops(16)[0])
v.check("Lab 14-11.e", (1 / 10e-6) * 100 / 1500)

sys.exit(v.finish())
