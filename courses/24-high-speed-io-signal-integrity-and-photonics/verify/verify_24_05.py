#!/usr/bin/env python3
"""Verify every number in chapter 24-05 (PCIe, CXL and Ethernet), its problems and its lab.

Independent routes (the lab module links.py uses rate x efficiency formulas and an event simulator):
- encoding efficiencies counted from block structures (data bits per coded block; flit byte map);
- credit-limited throughput from a fixed-step (1 ns) simulation, not the event queue;
- fabric sizes by constructing the leaf-spine graph and counting host ports;
- lane rates by building the bit budget of one RS codeword.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "24-05-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("24-05", ROOT / "chapters" / "24-05-pcie-cxl-ethernet.md",
                        ROOT / "solutions" / "24-05-solutions.md", LAB / "README.md")

# encoding efficiencies from block structure
eff_8b10b = 8 / 10              # 8 data bits per 10-bit symbol
eff_128b130b = 128 / (128 + 2)  # 2-bit sync header per 128-bit block
flit = {"tlp": 236, "dlp": 6, "crc": 8, "fec": 6}
v.assert_true("flit is 256 bytes", sum(flit.values()) == 256)
eff_flit = flit["tlp"] / sum(flit.values())


def bw(rate, lanes, eff):
    return rate * 1e9 * lanes * eff / 8 / 1e9  # GB/s per direction


# ================================================================ chapter
b3 = bw(8, 16, eff_128b130b)
b5 = bw(32, 16, eff_128b130b)
b6 = bw(64, 16, eff_flit)
v.check("Ex 24-05.1a", b3)
v.check("Ex 24-05.1b", b5)
v.check("Ex 24-05.1c", b6)
v.check("Ex 24-05.1d", 64 * 16 * 2 / 8)
v.check("Ex 24-05.1e", 100 * (eff_128b130b - eff_flit))
v.check("Ex 24-05.1f", b6 / b5)

for p, key in ((64, "2a"), (128, "2a1"), (256, "2a2"), (512, "2a3")):
    v.check(f"Ex 24-05.{key}", 100 * p / (p + 24))
v.check("Ex 24-05.2b", b5 * 256 / 280)


def stepped_throughput(bw_gbps, buf_bytes, rtt_ns, pkt=256, t_end=100_000):
    """Fixed 1-ns step simulation: credits return rtt_ns after a packet starts; link busy pkt/bw ns."""
    credits = buf_bytes // pkt
    pending = []  # return times
    busy_until = 0.0
    sent = 0
    t = 0
    tpkt = pkt / bw_gbps
    while t < t_end:
        while pending and pending[0] <= t:
            pending.pop(0)
            credits += 1
        while credits > 0 and busy_until <= t + 1e-9:
            start = max(busy_until, t)
            if start >= t + 1:
                break
            credits -= 1
            pending.append(start + rtt_ns)
            busy_until = start + tpkt
            if t >= t_end / 2:
                sent += 1
        t += 1
    return sent * pkt / (t_end / 2)


v.check("Ex 24-05.3a", 128e9 * 500e-9 / 1e3)
v.check("Ex 24-05.3b", 128e9 * 500e-9 / 64)
v.check("Ex 24-05.3c", 128e9 * 1e-6 / 1e3)
v.check("Txt 24-05.p", 128e9 * 250e-9 / 1e3)
thr_full = stepped_throughput(128, 64_000, 500)
v.assert_true("64 KB sustains 128 GB/s at 500 ns", abs(thr_full - 128) / 128 < 0.01)

cxl_raw = 64 * 16 / 8
cxl_eff = bw(64, 16, eff_flit)
ddr5 = 6400e6 * 8 / 1e9
v.check("Ex 24-05.4a", cxl_raw)
v.check("Ex 24-05.4a1", cxl_eff)
v.check("Ex 24-05.4b", cxl_eff / ddr5)
v.check("Txt 24-05.q", cxl_eff / ddr5)
v.check("Ex 24-05.4c", 0.8 * 100 + 0.2 * 200)
v.check("Ex 24-05.4d", 0.5 * 100 + 0.5 * 200)


def lane_rate(mac):
    # one RS codeword: 514 data symbols of 10 bits carry 5140 bits of 257-bit blocks (each 256 bits of 64b/66b data)
    data_bits = 514 * 10 * 256 / 257
    line_bits = 544 * 10
    return mac * line_bits / data_bits


lr = lane_rate(200)
v.check("Ex 24-05.5a", lr)
v.check("Ex 24-05.5b", lr / 2)
v.check("Ex 24-05.5b1", lr / 4)
v.check("Ex 24-05.5c", 8 * lr)
v.check("Ex 24-05.5d", 1600 / (8 * lr))
v.check("Ex 24-05.5e", 100 / 256)
v.check("Ex 24-05.5f", 100 * (lr / 200 - 1))


def leaf_spine_hosts(k):
    """Build a full-bisection two-tier fabric: k/2 host ports per leaf, k/2 uplinks, spines with k ports."""
    leaves = k  # each spine port connects one leaf, so at most k leaves
    uplinks = leaves * (k // 2)
    spines = uplinks // k
    v.assert_true(f"spines fully used (k={k})", spines * k == uplinks)
    return leaves * (k // 2)


for tbps, port, key in ((51.2, 0.8, "6a1"), (51.2, 1.6, "6a2")):
    v.check(f"Ex 24-05.{key}", tbps / port)
v.check("Ex 24-05.6a", 51.2e12 / 200e9)
v.check("Ex 24-05.6b", leaf_spine_hosts(64))
v.check("Ex 24-05.6b1", leaf_spine_hosts(128))
v.check("Ex 24-05.6c", 64 ** 3 / 4)

v.check("Ex 24-05.7a", 800e9 * 1e-6 / 8 / 1e3)
v.check("Ex 24-05.7b", 1.6e12 * 1e-6 / 8 / 1e3)

v.check("Ex 24-05.8a", 100 * (2 ** (1 / 3) - 1))
v.check("Ex 24-05.8b", (2025 - 2019) / math.log2(128 / 32))
v.check("Ex 24-05.8c", (2028 - 2017) / math.log2(256 / 16))

v.check("Txt 24-05.a", eff_8b10b)
v.check("Txt 24-05.b", eff_128b130b)
for gen, rate, eff, key in (("3.0", 8, eff_128b130b, "c"), ("4.0", 16, eff_128b130b, "d"),
                            ("5.0", 32, eff_128b130b, "e"), ("6.0", 64, eff_flit, "f"),
                            ("7.0", 128, eff_flit, "g"), ("1.0", 2.5, eff_8b10b, "m"), ("2.0", 5, eff_8b10b, "n")):
    v.check(f"Txt 24-05.{key}", bw(rate, 1, eff))
v.check("Txt 24-05.h", 100 * eff_flit)
v.check("Txt 24-05.i", 128 * 16 * 2 / 8)
v.check("Txt 24-05.j", 256 * 16 * 2 / 8 / 1000)
v.check("Txt 24-05.k", 100 * (1 - eff_8b10b))
v.check("Txt 24-05.l", 100 * (1 - eff_128b130b))
v.check("Txt 24-05.o", 100 * (8 / 5 - 1))

# ================================================================ solutions
b4x8 = bw(16, 8, eff_128b130b)
v.check("24-05.1a", b4x8)
v.check("24-05.1b", b4x8 * 128 / 152)
b7 = bw(128, 16, eff_flit)
v.check("24-05.2a", b7)
v.check("24-05.2b", b7 / 512)
v.check("24-05.3a", bw(8, 1, eff_128b130b))
v.check("24-05.3a1", bw(10, 1, eff_8b10b))
v.check("24-05.3b", 8 / 2)
v.check("24-05.3b1", 10 / 2)
v.check("24-05.3c", 100 * bw(8, 1, eff_128b130b) / bw(10, 1, eff_8b10b))
v.check("24-05.3c1", 100 * (1 - 4 / 5))
raw4 = 32 * 8 / 8
bdp4 = raw4 * 1e9 * 800e-9
v.check("24-05.4a", raw4)
v.check("24-05.4b", bdp4 / 1e3)
frac4 = min(1.0, 16_000 / bdp4)
v.check("24-05.4c", frac4)
v.check("24-05.4c1", frac4 * raw4)
v.check("24-05.4c2", 100 * frac4)
thr4 = stepped_throughput(32, 16_128, 800)  # 63 packets of 256 B, the nearest whole number of credits
v.assert_true("stepped simulation reproduces the credit limit", abs(thr4 - 63 * 256 / 800) / thr4 < 0.02)
v.check("24-05.5a", 2 * 2 * 10)
v.check("24-05.5", 128e9 * 40e-9 / 1e3)
c4 = bw(128, 16, eff_flit)
v.check("24-05.6a", c4)
v.check("24-05.6b", c4 / ddr5)
v.check("24-05.6c0", 2 * c4)
v.check("24-05.6c", 2 * c4 / 64)
v.check("24-05.6c1", ddr5 / 64)
v.check("24-05.6c2", (2 * c4 / 64) / (ddr5 / 64))
v.check("24-05.7", (110 - 100) / (200 - 100))
v.check("24-05.8a", 800 / 200)
v.check("24-05.8a1", 4 * lane_rate(200))
v.check("24-05.8b", 800 / 100)
v.check("24-05.8b1", 8 * lane_rate(100))
v.check("24-05.8c", lane_rate(100) / 2)
v.check("24-05.9a", 102.4 / 0.8)
v.check("24-05.9a1", leaf_spine_hosts(128))
v.check("24-05.9b", 102.4 / 1.6)
v.check("24-05.9b1", leaf_spine_hosts(64))
k10 = int(51.2 / 0.4)
v.check("24-05.10a", k10)
v.check("24-05.10b", leaf_spine_hosts(k10))
leaves = 4096 // (k10 // 2)
v.check("24-05.10c", leaves)
v.check("24-05.10d", leaves * (k10 // 2))
spines = leaves * (k10 // 2) // k10
v.check("24-05.10e", spines)
v.check("24-05.10f", leaves + spines)
v.check("24-05.11", 1.6e12 * 2e-6 / 8 / 1e3)
v.check("24-05.12a", 512 / 2)
v.check("24-05.12b", 512 / 4)
v.check("24-05.12c", 1e3 / 256)
v.check("24-05.13a", 128 / 2)
v.check("24-05.13b", 128 / 4)
v.check("24-05.13c", 1e3 / 64)

# ================================================================ lab
v.check("Lab 24-05.a", b4x8 * 128 / 152)
thr_lab = stepped_throughput(128, 32_000, 500)
v.assert_true("32 KB at 500 ns gives half rate", abs(thr_lab - 64) / 64 < 0.01)
v.check("Lab 24-05.b", 32_000 / 500)
v.check("Lab 24-05.c", 128e9 * 500e-9 / 1e3)
v.check("Lab 24-05.d", leaf_spine_hosts(128))
v.check("Lab 24-05.e", lane_rate(200))

sys.exit(v.finish())
