#!/usr/bin/env python3
"""Verify every number in chapter 18-01 (microcontroller architecture), its problems and its lab.

Independent routes:
- addresses by explicit bit arithmetic, decoded back to (byte, bit) to check the round trip; region membership against
  a separately written region table; the vector-table words unpacked with struct;
- wait states by searching for the smallest whole number of clock cycles that covers the access time;
- effective CPI from the first-order formula and, separately, from the lab's cycle-level fetch simulator on
  synthetic programs whose taken-branch rate is counted exactly;
- PLL configurations by a brute-force loop over every divider written here;
- energies by a dense frequency sweep and the wait-state band thresholds by root finding;
- the selection break-even weight by root finding on the two weighted scores.
"""
from __future__ import annotations

import math
import struct
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(ROOT / "labs" / "18-01-lab"))
from eeverify import Verifier  # noqa: E402
import mcuarch as ma  # noqa: E402

v = Verifier.from_files(
    "18-01",
    ROOT / "chapters" / "18-01-microcontroller-architecture.md",
    ROOT / "solutions" / "18-01-solutions.md",
    ROOT / "labs" / "18-01-lab" / "README.md",
)

# ---------------------------------------------------------------- memory map
REG = {"Code": (0x0, 0x1FFFFFFF), "SRAM": (0x20000000, 0x3FFFFFFF), "Peripheral": (0x40000000, 0x5FFFFFFF),
       "External RAM": (0x60000000, 0x9FFFFFFF), "External device": (0xA0000000, 0xDFFFFFFF),
       "Private peripheral bus": (0xE0000000, 0xE00FFFFF), "Vendor system": (0xE0100000, 0xFFFFFFFF)}
total = sum(hi - lo + 1 for lo, hi in REG.values())
v.check("Txt 18-01.a", total / 2**30)
v.assert_true("regions tile the 4 GiB space", total == 2**32)
for name, (lo, hi) in REG.items():
    v.assert_true(f"lab region table: {name}", ma.region(lo) == name and ma.region(hi) == name)


def alias(addr, bit, base, abase):
    byte_off = (addr - base) + (bit >> 3)
    return abase + (byte_off << 5) + ((bit & 7) << 2)


def decode(a, base, abase):
    off = a - abase
    return base + (off >> 5), (off & 31) >> 2


v.check("Txt 18-01.b", 8 * 4)
v.check("Txt 18-01.c", 4 * 168e6 / 1e6)
v.check("Txt 18-01.d", 0.0025 * 1e6)
v.check("Txt 18-01.e", 2**15)

P, PA, S, SA = 0x40000000, 0x42000000, 0x20000000, 0x22000000
odr = 0x40020000 + 0x14
v.check("Ex 18-01.1a", odr)
a1 = alias(odr, 5, P, PA)
v.check("Ex 18-01.1b", a1)
v.assert_true("decode(alias) round trip", decode(a1, P, PA) == (odr, 5))
v.assert_true("lab bit-band agrees", ma.bitband_alias(odr, 5) == a1)
v.check("Ex 18-01.1c", (0x2001FFFF - 0x20000000 + 1) / 1024)
v.check("Ex 18-01.1d", alias(0x20000100, 3, S, SA))
v.check("Ex 18-01.1e", alias(P + 2**20 - 1, 7, P, PA))
v.assert_true("last alias word is the last word of the 32 MiB alias region", alias(P + 2**20 - 1, 7, P, PA) == PA + 2**25 - 4)

# ---------------------------------------------------------------- wait states


def ws_search(f, t):
    n = 1
    while n / f < t * (1 - 1e-12):
        n += 1
    return n - 1


t30 = 1 / 30e6
for key, f in (("Ex 18-01.2a", 24e6), ("Ex 18-01.2b", 84e6), ("Ex 18-01.2c", 168e6)):
    v.check(key, ws_search(f, t30))
    v.assert_true(f"lab wait_states at {f/1e6:.0f} MHz", ma.wait_states(f, t30) == ws_search(f, t30))


def cpi(ws, b=0.12, m=1.0, s=2.0, L=16):
    return max(1.0, (ws + 1) * s / L) + b * m * ws


v.check("Ex 18-01.2d", 24e6 / cpi(0) / 1e6)
v.check("Ex 18-01.2e", 84e6 / cpi(2) / 1e6)
v.check("Ex 18-01.2f", cpi(5))
v.check("Ex 18-01.2g", 168e6 / cpi(5) / 1e6)
v.check("Ex 18-01.2h", cpi(5, m=0.05))
v.check("Ex 18-01.2i", 168e6 / cpi(5, m=0.05) / 1e6)
v.check("Txt 18-01.f", (1 - 1 / cpi(5)) * 100)
v.check("Txt 18-01.g", (1 - 1 / cpi(5, m=0.05)) * 100)

# the cycle simulator reproduces the formula for line-aligned targets and 16-bit code
rng = np.random.default_rng(1801)
prog = ma.make_program(150_000, 5, 0.6, 0.0, rng, aligned=True)
b_meas = sum(1 for _, _, tk in prog if tk) / len(prog)
for ws in (0, 2, 5):
    sim = ma.simulate_fetch(prog, ws).cpi
    v.assert_true(f"simulator = formula at WS {ws}", abs(sim - cpi(ws, b=b_meas)) < 2e-3, f"{sim} vs {cpi(ws, b=b_meas)}")
progu = ma.make_program(150_000, 5, 0.6, 0.3, rng, aligned=False)
bu = sum(1 for _, _, tk in progu if tk) / len(progu)
extra = ma.simulate_fetch(progu, 5).cpi / cpi(5, b=bu, s=2.6) - 1
v.assert_true("unaligned targets stall 10-25% more than the formula at WS 5", 0.10 < extra < 0.25, f"{extra:.3f}")
cached = ma.simulate_fetch(ma.make_program(60_000, 5, 0.6, 0.0, rng, aligned=True, code_bytes=512), 5, cache_lines=64).cpi
v.assert_true("a cache holding the whole loop removes the branch stalls", cached < 1.01, f"{cached}")

# ---------------------------------------------------------------- PLL


def pll(f_in, f_sys, f_aux=None):
    sols = []
    for m in range(2, 64):
        if not 1e6 <= f_in / m <= 2e6:
            continue
        for n in range(50, 433):
            fv = f_in / m * n
            if not 100e6 <= fv <= 432e6:
                continue
            for p in (2, 4, 6, 8):
                if abs(fv / p - f_sys) > 1:
                    continue
                if f_aux is None:
                    sols.append((m, n, p))
                    continue
                sols += [(m, n, p, q) for q in range(2, 16) if abs(fv / q - f_aux) < 1]
    return sols


s168 = pll(8e6, 168e6, 48e6)
v.check("Ex 18-01.3a", s168[0][3])
v.check("Ex 18-01.3b", len(s168))
v.assert_true("no exact 180 MHz + 48 MHz configuration", pll(8e6, 180e6, 48e6) == [])
v.assert_true("lab PLL search agrees", len(ma.pll_search(8e6, 168e6, f_aux=48e6)) == len(s168))

# ---------------------------------------------------------------- Example 4: cores for 300 CoreMark (R-297, R-300)
cm = {"M0+": 2.46, "M4": 3.54, "M33": 4.10}
need = 300.0
clk = {k: need / c for k, c in cm.items()}
v.check("Ex 18-01.4a", clk["M0+"])
v.check("Ex 18-01.4b", clk["M4"])
v.check("Ex 18-01.4c", clk["M33"])
clk97 = {k: brentq(lambda f, c=c: 0.97 * c * f - need, 30, 1000) for k, c in cm.items()}
v.check("Ex 18-01.4d", clk97["M0+"])
v.check("Ex 18-01.4e", clk97["M4"])
v.check("Ex 18-01.4f", clk97["M33"])
v.assert_true("Example 4: every clock is above the 30 MHz zero-wait band, so the 3% loss applies", min(clk.values()) > 30)
v.check("Ex 18-01.4g", 100 * (1 - clk["M33"] / clk["M4"]))
v.check("Ex 18-01.4h", 403 / 120)
v.check("Ex 18-01.4i", 100 * (403 / 120) / cm["M4"])
v.assert_true("Example 4: clock ratio M0+/M33 = 1.67 = 4.10/2.46", round(clk["M0+"] / clk["M33"], 2) == 1.67 and abs(clk["M0+"] / clk["M33"] - 4.10 / 2.46) < 1e-12)
v.assert_true("Example 4: M4F and M33 clocks fit SAM D5x (120 MHz) and RA6M5 (200 MHz)", clk97["M4"] < 120 and clk97["M33"] < 200)

# ---------------------------------------------------------------- section 9 and Example 2 sanity: real wait-state tables (R-300)
samd = [24, 51, 77, 101, 119]  # MHz for 0..4 wait states, VDD > 2.7 V
implied = [(w + 1) / (f * 1e6) * 1e9 for w, f in enumerate(samd)]
v.assert_true(f"SAM D5x table implies t_acc of 39-42 ns ({min(implied):.1f} to {max(implied):.1f})", 38.5 < min(implied) and max(implied) < 42.5)
v.assert_true("SAM D5x bands about 25 MHz wide (24, 27, 26, 24 MHz for 0-3 wait states)", [b - a for a, b in zip([0] + samd[:3], samd[:4])] == [24, 27, 26, 24])
samd_lv = [22, 44, 67, 89, 111]
v.assert_true("SAM D5x: lower voltage, every band edge lower (slower flash)", all(lo < hi for lo, hi in zip(samd_lv, samd)))
ra6 = {50e6: 0, 50.1e6: 1, 100e6: 1, 100.1e6: 2, 150e6: 2, 150.1e6: 3, 200e6: 3}
v.assert_true("RA6M5 FLWT table equals the band model with t_acc = 20 ns", all(ma.wait_states(f, 20e-9) == w for f, w in ra6.items()))

# ---------------------------------------------------------------- lab Part 3 expected results (own generator)
rng_l3 = np.random.default_rng(18013)
cpi_l3 = {name: ma.simulate_fetch(ma.make_program(100_000, 5, 0.6, mix, rng_l3, aligned=al), 5).cpi
          for name, mix, al in (("aligned16", 0.0, True), ("unaligned16", 0.0, False), ("mixed_aligned", 0.3, True), ("mixed_unaligned", 0.3, False))}
v.assert_true(f"Lab 3 / Example 2: at 5 WS, aligned 1.60, unaligned about 1.81, mixed aligned about 1.62, both about 1.92 ({cpi_l3})",
              abs(cpi_l3["aligned16"] - 1.6) < 0.01 and 1.77 < cpi_l3["unaligned16"] < 1.85 and cpi_l3["mixed_aligned"] < 1.65 and 1.88 < cpi_l3["mixed_unaligned"] < 1.96)

# ---------------------------------------------------------------- energy


def energy(f, n_instr, period, vdd, i0, k, isl, b=0.12):
    cyc = n_instr * cpi(ws_search(f, t30), b=b)
    ta = cyc / f
    return vdd * (i0 + k * f) * ta + vdd * isl * (period - ta)


E5 = {f: energy(f * 1e6, 1.2e6, 0.1, 1.8, 0.6e-3, 40e-12, 3e-6) for f in (30, 60, 168)}
v.check("Ex 18-01.5a", E5[30] * 1e6)
v.check("Ex 18-01.5b", E5[60] * 1e6)
v.check("Ex 18-01.5c", E5[168] * 1e6)
fs = np.arange(1e6, 168e6 + 1, 0.05e6)
Es = np.array([energy(f, 1.2e6, 0.1, 1.8, 0.6e-3, 40e-12, 3e-6) for f in fs])
v.check("Ex 18-01.5d", fs[np.argmin(Es)] / 1e6)
v.check("Ex 18-01.5e", Es.min() / 0.1 * 1e3)
v.assert_true("savings 6.6% and 20%", round((1 - E5[60] / E5[30]) * 100, 1) == 6.6 and round((1 - E5[60] / E5[168]) * 100) == 20)

# ---------------------------------------------------------------- selection
wts = {"power": 0.35, "cost": 0.25, "compute": 0.15, "memory": 0.10, "security": 0.10, "eco": 0.05}
sc = {"C": dict(zip(wts, (5, 2, 5, 5, 5, 4))), "D": dict(zip(wts, (4, 4, 3, 3, 2, 4)))}
scores = ma.weighted_scores(wts, sc)
v.check("Ex 18-01.6a", sum(wts[k] * sc["C"][k] for k in wts))
v.check("Ex 18-01.6b", sum(wts[k] * sc["D"][k] for k in wts))
v.assert_true("lab weighted_scores agrees", abs(scores["C"] - 4.2) < 1e-12 and abs(scores["D"] - 3.55) < 1e-12)


def score(c, w):
    rest = {k: x * (1 - w) / 0.75 for k, x in wts.items() if k != "cost"}
    return w * sc[c]["cost"] + sum(rest[k] * sc[c][k] for k in rest)


v.check("Ex 18-01.6c", brentq(lambda w: score("C", w) - score("D", w), 0.01, 0.99))
v.check("Ex 18-01.6d", (2.40 - 1.80) * 1e6)
specs = {"A": {"flash": 256, "sram": 32, "fpu": 0, "ua": -30}, "B": {"flash": 512, "sram": 128, "fpu": 1, "ua": -45},
         "C": {"flash": 1024, "sram": 256, "fpu": 1, "ua": -25}, "D": {"flash": 512, "sram": 160, "fpu": 1, "ua": -35}}
v.assert_true("gate passes C and D only", ma.gate({"flash": 256, "sram": 64, "fpu": 1, "ua": -40}, specs) == ["C", "D"])

# ---------------------------------------------------------------- problems
msp, rv = struct.unpack("<II", bytes.fromhex("00800120C1010008"))
v.check("18-01.2a", (0x2001BFFF - 0x20000000 + 1) / 1024)
v.check("18-01.2b", (0x2001FFFF - 0x2001C000 + 1) / 1024)
v.check("18-01.2c", 0x08000000 + 2**20 - 1)
v.check("18-01.2d", msp)
v.check("18-01.2e", rv & ~1)
v.assert_true("reset vector has the Thumb bit", rv & 1 == 1)
v.check("18-01.2f", (msp - 0x20000000) / 1024)
for key, off in (("18-01.3a", 0), ("18-01.3b", 4), ("18-01.3c", 8), ("18-01.3d", 0xC)):
    v.check(key, 0x40004400 + off)
v.check("18-01.3e", alias(0x4000440C, 13, P, PA))
byte, bit = decode(0x22010A84, S, SA)
v.check("18-01.4a", byte)
v.check("18-01.4b", bit)
v.assert_true("target is word-aligned", byte % 4 == 0)
t40 = 40e-9
v.check("18-01.5a", ws_search(32e6, t40))
v.check("18-01.5b", ws_search(64e6, t40))
v.check("18-01.5c", ws_search(100e6, t40))
v.check("18-01.5d", 1 / t40 / 1e6)
v.check("18-01.6a", 16 / 2.5)
v.check("18-01.6b", cpi(4, b=0.15, s=2.5))
v.check("18-01.6c", 150 / cpi(4, b=0.15, s=2.5))
v.check("18-01.6d", cpi(4, b=0.15, m=0.1, s=2.5))
v.check("18-01.6e", 150 / cpi(4, b=0.15, m=0.1, s=2.5))
for key, f in (("18-01.7a", 90e6), ("18-01.7b", 120e6), ("18-01.7c", 150e6)):
    v.check(key, f / cpi(ws_search(f, t30)) / 1e6)
v.check("18-01.7d", 1 / (0.12 * t30) / 1e6)
rates = [f / cpi(ws_search(f, t30)) / 1e6 for f in np.linspace(1e6, 5e9, 4000)]
v.assert_true("delivered rate stays below 1/(b t_acc) at every clock", max(rates) < 250)
v.assert_true("bound approached when sequential supply is ignored", abs(1e12 / (1 + 0.12 * ws_search(1e12, t30)) / 1e6 - 250) < 0.5)
v.assert_true("sequential starvation begins above 240 MHz", ws_search(240e6, t30) + 1 <= 8 < ws_search(241e6, t30) + 1)
v.check("18-01.8a", len(pll(25e6, 96e6, 48e6)))
v.check("18-01.8b", len(pll(25e6, 100e6)))
v.assert_true("no 100 MHz + 48 MHz", pll(25e6, 100e6, 48e6) == [])
v.check("18-01.9a", 20e-6 * 86400)
v.check("18-01.9b", 20e-6 * 86400 * 365.25)
v.check("18-01.9c", 0.01 * 1e6)
v.check("18-01.9d", 0.01 / 0.0025)
v.check("18-01.10", 3 * 2e6 / 80e6 * 100)
E11 = {f: energy(f * 1e6, 5e5, 0.05, 3.0, 1.0e-3, 30e-12, 2e-6) for f in (30, 60, 90, 120)}
for key, f in (("18-01.11a", 30), ("18-01.11b", 60), ("18-01.11c", 90), ("18-01.11d", 120)):
    v.check(key, E11[f] * 1e6)
Es11 = np.array([energy(f, 5e5, 0.05, 3.0, 1.0e-3, 30e-12, 2e-6) for f in fs])
v.check("18-01.11e", fs[np.argmin(Es11)] / 1e6)


def band_top_energy(w, i0, isl=0.0, k=40e-12, b=0.12):
    f = (w + 1) / t30
    return (1 + b * w) * ((i0 - isl) / f + k)


for key, w in (("18-01.12a", 0), ("18-01.12b", 1), ("18-01.12c", 2)):
    thr = brentq(lambda i0: band_top_energy(w + 1, i0) - band_top_energy(w, i0), 1e-6, 0.1)
    v.check(key, thr * 1e3)
    v.assert_true(f"closed form threshold w={w}", abs(thr - (w + 1) * (w + 2) * 40e-12 * 0.12 / (0.88 * t30)) < 1e-12)
v.check("18-01.13", 6 * 20000 / (1.45 - 1.20))
for pre, lanes in (("a", 4), ("d", 8)):
    pen = (20 + 32 * 8 / lanes) / 133e6 * 480e6
    v.check(f"18-01.14{pre}", pen)
    c = 1 + 0.005 * pen
    v.check(f"18-01.14{chr(ord(pre) + 1)}", c)
    v.check(f"18-01.14{chr(ord(pre) + 2)}", 480 / c)

# ---------------------------------------------------------------- lab
v.check("Lab 18-01.a", alias(0x40011008, 13, P, PA))
v.assert_true("lab alias decodes to byte 0x40011009 bit 5", decode(alias(0x40011008, 13, P, PA), P, PA) == (0x40011009, 5))
v.check("Lab 18-01.b", 31e6 / cpi(ws_search(31e6, t30)) / 1e6)
v.check("Lab 18-01.c", len(pll(8e6, 120e6, 48e6)))
for key, i0 in (("Lab 18-01.d", 0.2e-3), ("Lab 18-01.e", 2e-3)):
    Ei = np.array([energy(f, 1.2e6, 0.1, 1.8, i0, 40e-12, 3e-6) for f in fs])
    v.check(key, fs[np.argmin(Ei)] / 1e6)

sys.exit(v.finish())
