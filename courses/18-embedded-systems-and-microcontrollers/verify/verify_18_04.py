#!/usr/bin/env python3
"""Verify every number in chapter 18-04 (DMA and data movement), its problems and its lab.

Independent routes:
- buffer bounds from the inequality written out here, and checked against the lab's event simulator: overruns
  just below the bound (with the worst latency present) and none at the chosen power of two;
- contention from p * rho and from the lab's cycle-level model of a shared port (fixed seeds, own generators);
- ring and cache arithmetic by modular and integer arithmetic;
- the lock-free ring buffer by building the lab firmware with clang 18 and running it on QEMU's Cortex-M4 at -O2 and -O0;
- loads, times and energies by direct arithmetic.
"""
from __future__ import annotations

import math
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "18-04-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import dmasim as dm  # noqa: E402
import fwrun  # noqa: E402

v = Verifier.from_files("18-04", ROOT / "chapters" / "18-04-dma-and-data-movement.md",
                        ROOT / "solutions" / "18-04-solutions.md", LAB / "README.md")


def nmin(fs, a, b, lat=0.0, k=2):
    return (a + lat) * fs / ((k - 1) - b * fs)


def pow2(x):
    return 2 ** math.ceil(math.log2(x))


# ---------------------------------------------------------------- firmware on QEMU
for opt in ("-O2", "-O0"):
    try:
        code, out, _ = fwrun.build_and_run(Path(tempfile.mkdtemp(prefix="v1804_")), opt)
    except FileNotFoundError as exc:
        sys.exit(f"verify_18_04: {exc}")
    v.assert_true(f"ring-buffer firmware passes on QEMU at {opt}", code == 0 and "TEST PASSED" in out, out)

# ---------------------------------------------------------------- Example 1
v.check("Ex 18-04.1a", 100 * 96000 * 60 / 64e6)
v.check("Ex 18-04.1b", 96000 / 512)
v.check("Ex 18-04.1c", 100 * (96000 / 512) * 200 / 64e6)
v.check("Ex 18-04.1d", 512 / 96000 * 1e3)

# ---------------------------------------------------------------- Example 2 (bound and simulation)
fs, a, b = 1e6, 20e-6, 0.6e-6
v.check("Ex 18-04.2a", nmin(fs, a, b))
n25 = nmin(fs, a, b, 25e-6)
v.check("Ex 18-04.2b", n25)
v.check("Ex 18-04.2c", pow2(n25))
v.check("Ex 18-04.2d", 2 * pow2(n25) * 2)
v.check("Ex 18-04.2e", (pow2(n25) / fs + 25e-6 + a + b * pow2(n25)) * 1e6)
n3 = nmin(fs, a, b, 25e-6, 3)
v.check("Ex 18-04.2f", n3)
v.check("Ex 18-04.2g", 3 * pow2(n3) * 2)
v.check("Ex 18-04.2h", (pow2(n3) / fs + 25e-6 + a + b * pow2(n3)) * 1e6)
floor3 = a * fs / (1 - b * fs)
v.assert_true("Example 2: lab bound agrees; with three buffers the throughput floor (50) binds, not 32.1",
              abs(dm.pingpong_min_block(fs, a, b, 25e-6) - n25) < 1e-9 and floor3 > n3
              and abs(dm.pingpong_min_block(fs, a, b, 25e-6, 3) - floor3) < 1e-9 and pow2(max(n3, floor3)) == 64)
ov48_3, _ = dm.simulate_pingpong(fs, 48, a, b, n_blocks=20000, n_buffers=3, service_latency=5e-6, jitter=20e-6, seed=1)
v.assert_true("simulation: three buffers of 48 (above 32.1, below the floor of 50) overrun almost every block",
              ov48_3 > 19000, str(ov48_3))
v.assert_true("Example 2: a block of 32 takes 39.2 us to process", abs((a + b * 32) * 1e6 - 39.2) < 1e-9)
ov112, _ = dm.simulate_pingpong(fs, 112, a, b, n_blocks=20000, service_latency=5e-6, jitter=20e-6, seed=1)
ov128, w128 = dm.simulate_pingpong(fs, 128, a, b, n_blocks=20000, service_latency=25e-6)
ov64_3, _ = dm.simulate_pingpong(fs, 64, a, b, n_blocks=20000, n_buffers=3, service_latency=5e-6, jitter=20e-6, seed=1)
v.check("Lab 18-04.a", ov112)
v.check("Lab 18-04.b", ov128)
v.assert_true("simulation: overruns below the bound, none at 128 (two buffers, worst latency) or 64 (three)", ov112 > 0 and ov128 == 0 and ov64_3 == 0)
v.assert_true("simulation: worst latency at 128 equals the formula (249.8 µs)", abs(w128 * 1e6 - 249.8) < 1e-6)
v.assert_true("Lab discussion: N = 112 fails only for latency above 24.8 µs", abs(112 * (1 - b * fs) - 20 - 24.8) < 1e-9)

# ---------------------------------------------------------------- Example 3 and lab contention
v.check("Ex 18-04.3a", dm.stall_estimate(0.3, 0.25))
sim3 = dm.bus_sim(1_000_000, 0.3, 4)["stall_fraction"]
v.check("Ex 18-04.3b", 100 * sim3)
for per, key in ((25, "Lab 18-04.c"), (10, "Lab 18-04.d")):
    s = dm.bus_sim(1_000_000, 0.3, per)["stall_fraction"]
    v.check(key, 100 * s)
    v.assert_true(f"bus model within 1% (relative) of p*rho at period {per}", abs(s / dm.stall_estimate(0.3, 1 / per) - 1) < 0.01)
v.assert_true("Example 3: 100 MB/s of words at rho = 0.25 on a 100 MHz bus", 0.25 * 100e6 * 4 == 100e6)

# ---------------------------------------------------------------- Example 4
v.check("Ex 18-04.4a", dm.transfers(65536, 1))
v.check("Ex 18-04.4b", 65536 * 2 / 100e6 * 1e3)
v.check("Ex 18-04.4c", dm.transfers(65536, 4))
v.check("Ex 18-04.4d", 16384 * 2 / 100e6 * 1e3)

# ---------------------------------------------------------------- Example 5
v.check("Ex 18-04.5a", dm.cache_lines(0x20000008, 1000))
v.check("Ex 18-04.5b", dm.cache_lines(0x20000000, 1024))
v.assert_true("Example 5: the buffer ends at 0x200003EF; lines 0 and 31 shared", 0x20000008 + 999 == 0x200003EF and (0x200003EF + 1) % 32 != 0 and 0x20000008 % 32 != 0)

# ---------------------------------------------------------------- Example 6
rate = 921600 / 10
v.check("Ex 18-04.6a", rate)
v.check("Ex 18-04.6b", rate * 5e-3)
v.check("Ex 18-04.6c", pow2(rate * 5e-3))
v.check("Ex 18-04.6d", dm.ring_head(512, 312))
v.check("Ex 18-04.6e", dm.ring_unread(200, 150, 512))
v.check("Ex 18-04.6f", 512 / rate * 1e3)

# ---------------------------------------------------------------- problems
v.check("18-04.1a", 100 * dm.irq_load(10e6 / 8, 60, 168e6))
v.check("18-04.1b", 100 * dm.irq_load(10e6 / 8 / 64, 200, 168e6))
v.check("18-04.2a", dm.transfers(1500, 4))
v.check("18-04.2b", dm.transfers(1500, 2))
v.check("18-04.3a", dm.ring_head(256, 37))
v.check("18-04.3b", dm.ring_unread(219, 200, 256))
v.check("18-04.3c", dm.ring_unread(219, 230, 256))
v.check("18-04.4a", nmin(48e3, 200e-6, 5e-6))
n4 = nmin(48e3, 200e-6, 5e-6, 100e-6)
v.check("18-04.4b", n4)
v.check("18-04.4c", pow2(n4))
v.check("18-04.4d", (pow2(n4) / 48e3 + 100e-6 + 200e-6 + 5e-6 * pow2(n4)) * 1e6)
n5 = nmin(48e3, 200e-6, 5e-6, 100e-6, 3)
v.check("18-04.5a", n5)
v.check("18-04.5f", 200e-6 * 48e3 / (1 - 5e-6 * 48e3))
v.assert_true("Problem 5: the throughput floor binds and 16 satisfies both", 200e-6 * 48e3 / 0.76 > n5 and pow2(200e-6 * 48e3 / 0.76) == 16)
v.check("18-04.5b", pow2(n5))
v.check("18-04.5c", 3 * pow2(n5) * 2)
v.check("18-04.5d", 2 * pow2(n4) * 2)
v.check("18-04.5e", (pow2(n5) / 48e3 + 100e-6 + 200e-6 + 5e-6 * pow2(n5)) * 1e6)
for N, k in ((pow2(n4), 2), (pow2(n5), 3)):
    v.assert_true(f"Problems 4-5: no overruns at N = {N} with {k} buffers at the worst latency",
                  dm.simulate_pingpong(48e3, N, 200e-6, 5e-6, n_blocks=5000, n_buffers=k, service_latency=100e-6)[0] == 0)
rho6 = (2e6 + 6.25e6) / 100e6
v.check("18-04.6a", rho6)
v.check("18-04.6b", 0.35 * rho6)
c_plain, c_burst = 4096 * 3, 4096 * 2 + 4096 // 4
v.check("18-04.7a", c_plain)
v.check("18-04.7b", c_burst)
v.check("18-04.7c", 100 * (1 - c_burst / c_plain))
v.check("18-04.8a", dm.cache_lines(0x20010014, 600))
v.check("18-04.8b", -(-600 // 32) * 32)
v.check("18-04.9a", 3e6 / 10 * 2e-3)
v.check("18-04.9b", pow2(1.5 * 600))
t_cpu = 4 * 1e6 / 48e6
t_dma = 1e6 / 4 * 2 / 48e6
e_cpu, e_dma = 3.3 * 5e-3 * t_cpu, 3.3 * 1.5e-3 * t_dma
v.check("18-04.10a", t_cpu * 1e3)
v.check("18-04.10b", t_dma * 1e3)
v.check("18-04.10c", e_cpu * 1e3)
v.check("18-04.10d", e_dma * 1e6)
v.check("18-04.10e", e_cpu / e_dma)
v.assert_true("Problem 10: time ratio 8 times current ratio 3.33", abs((t_cpu / t_dma) - 8) < 1e-9 and abs(e_cpu / e_dma - 8 * 5 / 1.5) < 1e-9)
n11 = nmin(200e3, 15e-6, 2e-6, 40e-6)
v.check("18-04.11a", n11)
v.check("18-04.11b", pow2(n11))
v.check("18-04.11c", 2 * pow2(n11) * 2)
v.check("18-04.11d", 100 * 0.4 * 200e3 / 64e6)
v.assert_true("Problem 11(d): a 1024-point block fits its block time (2063 < 5120 µs)", 15 + 2 * 1024 == 2063 and 1024 / 200e3 * 1e6 == 5120)

# lab Part 2 expected results
def p2(x): return 2 ** math.ceil(math.log2(x))
lat3 = [(p2(dm.pingpong_min_block(fs, a, b, L * 1e-6, 3)) / fs + L * 1e-6 + a + b * p2(dm.pingpong_min_block(fs, a, b, L * 1e-6, 3))) * 1e6 for L in (0, 60)]
lat2_60 = (p2(dm.pingpong_min_block(fs, a, b, 60e-6, 2)) / fs + 60e-6 + a + b * p2(dm.pingpong_min_block(fs, a, b, 60e-6, 2))) * 1e6
v.assert_true("lab Part 2: three buffers stay at 64, latency 122 -> 182 us; two buffers reach 490 us",
              all(p2(dm.pingpong_min_block(fs, a, b, L * 1e-6, 3)) == 64 for L in range(0, 61))
              and round(lat3[0]) == 122 and round(lat3[1]) == 182 and round(lat2_60) == 490)
v.assert_true("lab Part 2: two-buffer steps above 5.6 and 31.2 us", abs((64 * 0.4 - 20) - 5.6) < 1e-9 and abs((128 * 0.4 - 20) - 31.2) < 1e-9)
lines12 = dm.cache_lines(0x20000410, 200)
v.check("18-04.12a", lines12)
v.check("18-04.12b", 32 * lines12)
v.assert_true("Problem 12: the first line also holds rx_count at 0x20000408", 0x20000408 // 32 == 0x20000410 // 32)
v.assert_true("Problem 12: 200 bytes round up to 224, seven whole lines", math.ceil(200 / 32) * 32 == 224)
sys.exit(v.finish())
