#!/usr/bin/env python3
"""Verify every number in chapter 18-08 (boot, bootloaders and firmware update), its problems and its lab.

Independent routes:
- budgets, times, wear, energies and fuse lives by direct arithmetic written out here;
- outage risk from the Poisson model computed here, cross-checked against the lab's helper and a Monte Carlo of
  outage arrival times (own generator);
- operation counts derived by formula here and compared with the lab's flash model;
- power-cut outcomes by running the lab's flash and bootloader model with a cut during every operation, each image
  checked by SHA-256, and a deliberately broken bootloader to show that the campaign detects bugs;
- the vector-table arithmetic of Problem 18-08.1 by integer operations.
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "18-08-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import bootsim as bs  # noqa: E402

v = Verifier.from_files("18-08", ROOT / "chapters" / "18-08-boot-and-firmware-update.md",
                        ROOT / "solutions" / "18-08-solutions.md", LAB / "README.md")

MONTH = 30 * 86400


def p_outage(window, per_month):
    return 1 - math.exp(-per_month / MONTH * window)


def copy_time(sector_bytes, word_bytes, t_word, t_erase):
    return t_erase + sector_bytes // word_bytes * t_word


def ops_count(scheme, n):
    if scheme == "inplace":
        return 1 + 2 * n + 1
    if scheme == "overwrite":
        return 2 * n + 1 + 3 * n + 1
    if scheme == "swap":
        return 2 * n + 1 + 9 * n + 1 + 1          # download, pending, 3 x (erase, write, status) per sector, test, confirm
    raise ValueError(scheme)


# ---------------------------------------------------------------- Example 1
v.check("Ex 18-08.1a", 1024 - 64)
v.check("Ex 18-08.1b", (1024 - 64) / 2)
v.check("Ex 18-08.1c", (1024 - 64 - 32) / 2)

# ---------------------------------------------------------------- Example 2
n2 = 384 * 1024 // 4096
c2 = copy_time(4096, 8, 40e-6, 20e-3)
v.check("Ex 18-08.2a", n2)
v.check("Ex 18-08.2b", 1e3 * c2)
v.check("Ex 18-08.2c", n2 * c2)
v.check("Ex 18-08.2d", 3 * n2 * c2)
v.assert_true("lab swap_time agrees", abs(bs.swap_time(384 * 1024, 4096, 20e-3, 512 * 40e-6, 3) - 3 * n2 * c2) < 1e-12)
v.check("Ex 18-08.2e", math.floor(10000 / n2))

# ---------------------------------------------------------------- Example 3
v.check("Ex 18-08.3a", 1e3 * 384 * 1024 * 25 / 64e6)
v.check("Ex 18-08.3b", 1e3 * 4e6 / 64e6)
v.check("Ex 18-08.3c", 1e3 * (384 * 1024 * 25 + 4e6) / 64e6)
v.check("Ex 18-08.3d", 1e3 * (384 * 1024 + 4e6) / 64e6)

# ---------------------------------------------------------------- Example 4
w4 = 384 * 1024 / 50e3
v.check("Ex 18-08.4a", w4)
p4 = p_outage(w4, 2)
v.check("Ex 18-08.4b", p4)
v.check("Ex 18-08.4c", 1e6 * p4)
v.assert_true("lab outage_probability agrees", abs(bs.outage_probability(w4, 2) - p4) < 1e-15)
rng = random.Random(18084)
lam = 2 / MONTH * 1e4          # an amplified outage rate, so that the probability is measurable by sampling
p_amp = 1 - math.exp(-lam * w4)
trials = 200000
hits = sum(rng.expovariate(lam) < w4 for _ in range(trials))   # memoryless: time to the next outage
v.assert_true("Monte Carlo of outage arrivals matches 1 - exp(-rate x window) within 5 sigma",
              abs(hits / trials - p_amp) < 5 * math.sqrt(p_amp * (1 - p_amp) / trials), f"{hits / trials:.4f} vs {p_amp:.4f}")
v.check("Ex 18-08.4d", 0.01 * 1e6)
v.check("Ex 18-08.4e", 0.01 * 1e6 * 50)
camp = {s: bs.campaign(s, 6) for s in ("inplace", "overwrite", "swap")}
v.check("Ex 18-08.4f", camp["inplace"]["bricked"])
v.check("Ex 18-08.4g", camp["overwrite"]["bricked"])
v.check("Ex 18-08.4h", camp["swap"]["bricked"])
v.assert_true("in-place has 14 cut positions, overwrite 32, swap 69",
              [camp[s]["cuts"] for s in ("inplace", "overwrite", "swap")] == [14, 32, 69]
              and all(camp[s]["cuts"] == ops_count(s, 6) for s in camp))
v.assert_true("swap: only download, pending and final-confirm cuts keep the old image",
              camp["swap"]["old"] == 2 * 6 + 1 + 1)

# ---------------------------------------------------------------- Example 5
v.check("Ex 18-08.5a", 32 / 12)
v.check("Ex 18-08.5b", 32 / 4)

# ---------------------------------------------------------------- Example 6
v.check("Ex 18-08.6a", w4 * 8e-3 * 3)
v.check("Ex 18-08.6b", 0.15 * w4)

# ---------------------------------------------------------------- Problem 1
base = 0x00010000
v.check("18-08.1a", base)
v.check("18-08.1b", base + 4)
v.check("18-08.1c", 0x000102C9 & ~1)
v.assert_true("reset vector is odd (Thumb)", 0x000102C9 & 1 == 1)

# ---------------------------------------------------------------- Problem 2
v.check("18-08.2a", (512 - 32) / 2)
v.check("18-08.2b", (512 - 32 - 16) / 2)
v.check("18-08.2c", 512 - 32)
v.check("18-08.2d", (512 - 32) / 2 - 4)

# ---------------------------------------------------------------- Problem 3
v.check("18-08.3a", 2.0 ** -32)

# ---------------------------------------------------------------- Problem 4
n4 = 256 * 1024 // 2048
c4 = copy_time(2048, 4, 16e-6, 25e-3)
v.check("18-08.4a", 1e3 * c4)
v.check("18-08.4b", n4 * c4)
v.check("18-08.4c", 3 * n4 * c4)
v.check("18-08.4d", math.floor(10000 / n4))
v.check("18-08.4e", math.floor(8 * 10000 / n4))

# ---------------------------------------------------------------- Problem 5
v.check("18-08.5a", 1e3 * 512 * 1024 * 30 / 100e6)
v.check("18-08.5b", 1e3 * 3e6 / 100e6)
v.check("18-08.5c", 1e3 * (512 * 1024 * 30 + 3e6) / 100e6)

# ---------------------------------------------------------------- Problem 6
w6 = 1024 * 1024 / 20e3
p6 = p_outage(w6, 4)
v.check("18-08.6a", w6)
v.check("18-08.6b", p6)
v.check("18-08.6c", 2e5 * p6)
v.check("18-08.6d", 0.03 * 2e5)
v.check("18-08.6e", 0.03 * 2e5 * 80)

# ---------------------------------------------------------------- Problems 7 to 9
v.check("18-08.7a", 64 / 6)
v.check("18-08.8a", w6 * 10e-3 * 3.6)
v.check("18-08.8b", 0.12 * w6)
v.check("18-08.9a", (1024 - 48) / 2)
v.check("18-08.9b", math.log(((1024 - 48) / 2) / 400) / math.log(1.15))
v.check("18-08.9c", math.log((1024 - 48) / 400) / math.log(1.15))

# ---------------------------------------------------------------- Problem 10
c3o, c3i, c3s = bs.campaign("overwrite", 3), bs.campaign("inplace", 3), bs.campaign("swap", 3)
v.check("18-08.10a", ops_count("overwrite", 3))
v.assert_true("lab model counts 17 overwrite operations", c3o["cuts"] == 17)
v.check("18-08.10b", c3o["old"])
v.check("18-08.10c", c3o["new"])
v.assert_true("overwrite never bricks", c3o["bricked"] == 0)
v.check("18-08.10d", ops_count("inplace", 3))
v.check("18-08.10e", c3i["bricked"])
v.assert_true("in-place: 8 operations, first and last cuts do not brick", c3i["cuts"] == 8 and c3i["old"] == 1 and c3i["new"] == 1)
v.check("18-08.10f", c3s["cuts"])
v.assert_true("swap never bricks", c3s["bricked"] == 0)

# ---------------------------------------------------------------- lab
v.check("Lab 18-08.a", camp["inplace"]["cuts"])
v.check("Lab 18-08.b", camp["overwrite"]["cuts"])
v.check("Lab 18-08.c", camp["overwrite"]["old"])
v.check("Lab 18-08.d", camp["swap"]["cuts"])
v.check("Lab 18-08.e", camp["swap"]["new"])
v.assert_true("unconfirmed image is reverted", bs.revert_test() == 1)
rc = bs.revert_campaign()
v.check("Lab 18-08.f", rc["cuts"])
v.assert_true("every revert cut ends with the old image", rc["bricked"] == 0 and rc["new"] == 0 and rc["old"] == rc["cuts"] + 1)


class BrokenResume(bs.Device):
    """A bootloader that resumes an installation only if the secondary slot still validates."""

    def boot(self):
        st = self.f.status
        if st is not None and st[0] == "pending":
            if bs.validate(self.slot(1)) is not None:
                if self.scheme == "swap":
                    self._swap_steps(st[1], st[2], st[3])
                elif self.scheme == "overwrite":
                    self._overwrite_steps(st[1])
            return bs.validate(self.slot(0))
        return super().boot()


broken = bs.campaign("swap", 6, device_cls=BrokenResume)
v.check("Lab 18-08.g", broken["bricked"])
v.check("Lab 18-08.h", broken["bricking_cuts"][0] + 1)
v.assert_true("the first bricking cut erases the secondary slot's first sector (download 12, status 1, then 6 ops)",
              broken["bricking_cuts"][0] == 2 * 6 + 1 + 6 and broken["bricking_cuts"] == list(range(19, 63)))
v.assert_true("installation time grows linearly with size", abs(bs.swap_time(1 << 20, 4096, 20e-3, 20.48e-3, 1)
                                                                / bs.swap_time(1 << 17, 4096, 20e-3, 20.48e-3, 1) - 8) < 1e-12)

sys.exit(v.finish())
