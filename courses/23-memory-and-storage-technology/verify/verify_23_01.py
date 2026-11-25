#!/usr/bin/env python3
"""Verify every number in chapter 23-01 (the memory hierarchy and the memory wall), its problems and its lab.

Independent routes (the lab module memwall.py uses the closed forms):
- operation energies by summing a sampled trace of reads and arithmetic; the reuse factor by root finding;
- wire energy by integrating the supply power of a 20-section RC ladder (solve_ivp), and transition
  probabilities by enumerating bit patterns;
- power budgets and pin rates by root finding on P = 8·BW·E_b and BW = N·r/8;
- Little's law by a discrete-event simulation of requests with fixed latency, averaging the number in flight;
- growth factors by repeated multiplication;
- the decode model by counting K and V bytes and attention and projection FLOPs layer by layer and head by head,
  and the largest batch by incrementing until memory overflows.
"""
from __future__ import annotations

import math
import sys
from itertools import product
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "23-01-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import memwall as mw  # noqa: E402

v = Verifier.from_files("23-01", ROOT / "chapters" / "23-01-memory-hierarchy-and-memory-wall.md",
                        ROOT / "solutions" / "23-01-solutions.md", LAB / "README.md")
E = mw.HOROWITZ_45NM_PJ


# ---------------------------------------------------------------- independent helpers
def trace_energy(ops: list[str]) -> float:
    """Total energy (pJ) of a list of operations from the 45 nm table."""
    return float(np.sum([E[o] for o in ops]))


def ladder_supply_energy(c_tot: float, r_tot: float, r_drv: float, vdd: float, nseg: int = 20) -> tuple[float, float]:
    """Charge an nseg-section RC ladder from a step; return (energy delivered by the source, energy stored)."""
    cseg, rseg = c_tot / nseg, r_tot / nseg
    tau = (r_drv + r_tot) * c_tot

    def rhs(_t, vn):
        vin = np.concatenate([[vdd], vn[:-1]])
        r_in = np.concatenate([[r_drv + rseg], np.full(nseg - 1, rseg)])
        i_in = (vin - vn) / r_in
        i_out = np.concatenate([i_in[1:], [0.0]])
        return (i_in - i_out) / cseg

    def p_src(_t, vn):
        return vdd * (vdd - vn[0]) / (r_drv + rseg)

    sol = integrate.solve_ivp(lambda t, y: np.concatenate([rhs(t, y[:-1]), [p_src(t, y[:-1])]]),
                              (0, 40 * tau), np.zeros(nseg + 1), method="LSODA", rtol=1e-10, atol=1e-22)
    vn = sol.y[:-1, -1]
    return sol.y[-1, -1], float(np.sum(0.5 * cseg * vn ** 2))


def p01_enumerated(nbits: int = 12, pattern=None) -> float:
    """Fraction of bit positions that are a 1 following a 0, over all (or one) bit pattern(s)."""
    seqs = [pattern] if pattern is not None else list(product((0, 1), repeat=nbits))
    hits = sum(sum(1 for a, b in zip(s, s[1:]) if a == 0 and b == 1) for s in seqs)
    return hits / (len(seqs) * (len(seqs[0]) - 1))


def little_sim(rate: float, latency: float, n_req: int = 200_000) -> float:
    """Average number in flight for requests arriving at `rate` and each taking `latency`, by sampling n(t)."""
    t_arr = np.arange(n_req) / rate
    t_done = t_arr + latency
    t = np.linspace(t_done[0], t_arr[-1], 50_001)  # steady-state window
    n = np.searchsorted(t_arr, t, side="right") - np.searchsorted(t_done, t, side="right")
    return float(np.mean(n))


def grow(rate: float, steps: int) -> float:
    x = 1.0
    for _ in range(steps):
        x *= rate
    return x


def layer_count(params, w_bytes, layers, q_heads, kv_heads, head_dim, kv_b, context, batch):
    """Bytes and FLOPs of one decode step, counted layer by layer and head by head."""
    kv_bytes = 0.0
    attn_flops = 0.0
    for _layer in range(layers):
        for _h in range(kv_heads):
            kv_bytes += 2 * head_dim * kv_b * context          # one K and one V vector per context token
        for _h in range(q_heads):
            attn_flops += 2 * head_dim * context                 # q·k for every context token
            attn_flops += 2 * head_dim * context                 # weighted sum of the values
    step_bytes = params * w_bytes + batch * kv_bytes
    step_flops = batch * (2 * params + attn_flops)
    return step_bytes, step_flops, kv_bytes


def max_batch_count(capacity, weights, kv_seq):
    b = 0
    while weights + (b + 1) * kv_seq <= capacity:
        b += 1
    return b


# ---------------------------------------------------------------- Example 23-01.1
print("Examples")
mac_dram = trace_energy(["32b DRAM read", "32b DRAM read", "32b FP mult", "32b FP add"])
mac_sram = trace_energy(["32b SRAM read (8 KB)", "32b SRAM read (8 KB)", "32b FP mult", "32b FP add"])
arith = trace_energy(["32b FP mult", "32b FP add"])
v.check("Ex 23-01.1a", E["32b DRAM read"] / E["32b FP mult"])
v.check("Txt 23-01.a", E["32b DRAM read"] / E["32b FP mult"])
v.check("Ex 23-01.1b", mac_dram)
v.check("Ex 23-01.1c", 100 * (mac_dram - arith) / mac_dram)
v.check("Ex 23-01.1d", mac_sram)
v.check("Ex 23-01.1e", 100 * (mac_sram - arith) / mac_sram)
v.check("Ex 23-01.1f", optimize.brentq(lambda r: 2 * E["32b DRAM read"] / r - arith, 1, 1e4))

# ---------------------------------------------------------------- Example 23-01.2
C1MM, VDD = 0.2e-15 / 1e-6 * 1e-3, 0.75
e_src, e_store = ladder_supply_energy(C1MM, 2e3, 1e3, VDD)
e_src10, _ = ladder_supply_energy(C1MM, 2e3, 10e3, VDD)
p01 = p01_enumerated()
v.assert_true("random data: a 0->1 transition at 1/4 of bit positions", abs(p01 - 0.25) < 1e-12)
v.assert_true("alternating data: a 0->1 transition at 1/2 of bit positions", p01_enumerated(pattern=(0, 1) * 500 + (0,)) == 0.5)
v.check("Ex 23-01.2a", C1MM * 1e15)
v.check("Ex 23-01.2b", e_src * 1e15)
v.assert_true("supply energy does not depend on the driver resistance", abs(e_src10 / e_src - 1) < 1e-6)
eb_mm = p01 * e_src
v.check("Ex 23-01.2c", eb_mm * 1e15)
v.check("Txt 23-01.b", eb_mm * 1e15)
v.check("Ex 23-01.2d", 20 * eb_mm * 1e12)
v.check("Ex 23-01.2e", 512 * 2e9 * 20 * eb_mm)
v.check("Ex 23-01.2f", 8 * 8e12 * 20 * eb_mm)

# ---------------------------------------------------------------- Example 23-01.3
bw_gddr = optimize.brentq(lambda bw: 8 * bw * 14.0e-12 - 60, 1e9, 1e14)
bw_hbm2 = optimize.brentq(lambda bw: 8 * bw * 3.9e-12 - 60, 1e9, 1e14)
v.check("Ex 23-01.3a", bw_gddr / 1e9)
v.check("Ex 23-01.3b", bw_hbm2 / 1e12)
v.check("Txt 23-01.c", 14.0 / 3.9)
e_all = optimize.brentq(lambda e: 8 * 4.52e12 * e - 248, 1e-13, 1e-10)
v.check("Ex 23-01.3c", e_all * 1e12)
v.check("Ex 23-01.3d", 100 * 248 / 700)
v.check("Ex 23-01.3e", 100 * 4.52 / 4.8)
p_all, p_mod = 8 * 8e12 * e_all, 8 * 8e12 * 3.9e-12
v.check("Ex 23-01.3f", p_all)
v.check("Ex 23-01.3g", p_mod)
v.check("Ex 23-01.3h", 100 * p_all / 1400)
v.check("Ex 23-01.3i", 100 * p_mod / 1400)

# ---------------------------------------------------------------- Example 23-01.4
pin = optimize.brentq(lambda r: 8192 * r / 8 - 8e12, 1e8, 1e11)
v.check("Ex 23-01.4a", pin / 1e9)
v.check("Ex 23-01.4b", 8e12 / 8 / 1e12)
v.check("Ex 23-01.4c", optimize.brentq(lambda r: 1024 * r / 8 - 1.2e12, 1e8, 1e11) / 1e9)
v.check("Ex 23-01.4d", 1024 * 9.2e9 / 8 / 1e12)
v.check("Ex 23-01.4e", optimize.brentq(lambda r: 8 * 2048 * r / 8 - 19.2e12, 1e8, 1e11) / 1e9)
ddr5 = sum(64 * 6.0e9 / 8 for _ch in range(2))
v.check("Ex 23-01.4f", ddr5 / 1e9)
v.check("Ex 23-01.4g", 8e12 / ddr5)
v.check("Txt 23-01.d", 8e12 / ddr5)
v.check("Txt 23-01.g", 8192 / 128)

# ---------------------------------------------------------------- Example 23-01.5
req_rate_gpu = 8e12 / 64
in_flight_gpu = little_sim(req_rate_gpu, 600e-9)
v.check("Ex 23-01.5b", in_flight_gpu)
v.check("Ex 23-01.5a", in_flight_gpu * 64 / 1e6)
in_flight_cpu = little_sim(96e9 / 64, 70e-9)
v.check("Ex 23-01.5d", in_flight_cpu)
v.check("Ex 23-01.5c", in_flight_cpu * 64)
v.check("Txt 23-01.l", in_flight_gpu / in_flight_cpu)

# ---------------------------------------------------------------- Example 23-01.6
v.check("Ex 23-01.6a", grow(3.0, 10))
v.check("Ex 23-01.6b", grow(1.6, 10))
v.check("Ex 23-01.6c", grow(1.4, 10))
v.check("Ex 23-01.6d", grow(3.0, 1) / grow(1.6, 1))
v.check("Txt 23-01.h", grow(3.0, 1) / grow(1.6, 1))
v.check("Ex 23-01.6e", grow(3.0, 5) / grow(1.6, 5))
v.check("Txt 23-01.i", grow(3.0, 5) / grow(1.6, 5))
ridge = {"f": (2e15, 3.35e12), "g": (5e15, 8e12), "h": (15e15, 8e12), "i": (35e15, 19.2e12), "j": (17.5e15, 19.2e12)}
for key, (fl, bw) in ridge.items():
    v.check(f"Ex 23-01.6{key}", fl / bw)
v.check("Ex 23-01.6k", 19.2 / 3.35)
v.check("Ex 23-01.6l", 17.5 / 2)
v.check("Ex 23-01.6m", (17.5 / 2) / (19.2 / 3.35))
v.check("Txt 23-01.m", (17.5e15 / 19.2e12) / (2e15 / 3.35e12))
v.check("Txt 23-01.n", 15 / 5)

# ---------------------------------------------------------------- Example 23-01.7
M = dict(params=70e9, w_bytes=1, layers=80, q_heads=64, kv_heads=8, head_dim=128, kv_b=1)
CTX = 32_768
_, _, kv_seq = layer_count(**M, context=CTX, batch=1)
v.check("Ex 23-01.7a", kv_seq / CTX)
v.check("Ex 23-01.7b", kv_seq / 1e9)
B7 = max_batch_count(288e9, 70e9, kv_seq)
v.check("Ex 23-01.7c", B7)
sb, sf, _ = layer_count(**M, context=CTX, batch=B7)
v.check("Ex 23-01.7d", sb / 1e9)
t_mem, t_cmp = sb / 8e12, sf / 5e15
v.check("Ex 23-01.7e", t_mem * 1e3)
v.check("Ex 23-01.7f", B7 / max(t_mem, t_cmp))
v.check("Ex 23-01.7g", sf / 1e12)
v.check("Ex 23-01.7h", t_cmp * 1e3)
v.check("Ex 23-01.7i", t_mem / t_cmp)
v.check("Txt 23-01.j", t_mem / t_cmp)
v.check("Ex 23-01.7j", sf / sb)
_, _, kv_tok = layer_count(**M, context=1, batch=1)
attn_flops_tok = 4 * M["layers"] * M["q_heads"] * M["head_dim"]
v.check("Ex 23-01.7k", attn_flops_tok / kv_tok)
big = 10 ** 7
sb_big, sf_big, _ = layer_count(**M, context=CTX, batch=big)
v.check("Ex 23-01.7l", sf_big / sb_big)
v.check("Txt 23-01.k", sf_big / sb_big)
v.check("Txt 23-01.f", B7 * kv_seq / 1e9)
v.check("Txt 23-01.e", 1024 / 64)

# ---------------------------------------------------------------- Example 23-01.8
e_step = 8 * sb * e_all
v.check("Ex 23-01.8a", e_step)
v.check("Ex 23-01.8b", e_step / B7)
sb1, _, _ = layer_count(**M, context=CTX, batch=1)
v.check("Ex 23-01.8c", sb1 / 1e9)
v.check("Ex 23-01.8d", 8 * sb1 * e_all)
v.check("Ex 23-01.8e", (8 * sb1 * e_all) / (e_step / B7))

# lab module agrees with the independent routes
tm = mw.Transformer(params=70e9, weight_bytes=1, layers=80, q_heads=64, kv_heads=8, head_dim=128, kv_bytes=1)
v.assert_true("memwall: KV per sequence and batch agree", tm.kv_per_sequence(CTX) == kv_seq and tm.max_batch(288e9, CTX) == B7)
v.assert_true("memwall: intensity and limit agree",
              abs(tm.intensity(CTX, B7) - sf / sb) < 1e-9 and abs(tm.intensity_limit(CTX) / (sf_big / sb_big) - 1) < 1e-5)
v.assert_true("memwall: wire energy agrees", abs(mw.wire_energy_per_bit(0.2e-15 / 1e-6, 1e-3, VDD) / eb_mm - 1) < 1e-6)

# ---------------------------------------------------------------- problems
print("Problems")
v.check("23-01.1a", E["32b DRAM read"] / E["32b SRAM read (8 KB)"])
v.check("23-01.1b", E["32b DRAM read"] / E["32b add"])
v.check("23-01.1c", trace_energy(["32b DRAM read"]) * (1e9 / 4) * 1e-12)
v.check("23-01.2a", 8 * 4e12 * 5e-12)
v.check("23-01.2b", integrate.quad(lambda t: 8 * 4e12 * 5e-12, 0, 100e9 / 4e12)[0])
v.check("23-01.2c", 100e9 / 4e12 * 1e3)
v.check("23-01.3a", 384 * 28e9 / 8 / 1e12)
v.check("23-01.3b", 1024 * 8e9 / 8 / 1e12)
v.check("23-01.3c", optimize.brentq(lambda n: n * 32e9 / 8 - 1e12, 1, 1e4))
fl4 = little_sim(1e12 / 64, 400e-9)
v.check("23-01.4b", fl4)
v.check("23-01.4a", fl4 * 64 / 1e3)
v.check("23-01.4c", optimize.brentq(lambda bw: little_sim(bw / 64, 400e-9, 50_000) - 2048, 1e10, 1e12, xtol=1e6) / 1e9)
c5 = 0.18e-15 / 1e-6 * 2e-3
e5, _ = ladder_supply_energy(c5, 4e3, 1e3, 0.8)
v.check("23-01.5a", c5 * 1e15)
v.check("23-01.5b", e5 * 1e15)
v.check("23-01.5c", p01_enumerated() * e5 * 1e15)
alt = p01_enumerated(pattern=(0, 1) * 500 + (0,))
v.check("23-01.5d", alt * e5 * 1e15)
v.check("23-01.5e", 0.2 * e5 * 1e15)
v.check("23-01.6a", 1.6e-9 / 8192 * 1e12)
v.check("23-01.6b", 1.6e-9 / 512 * 1e12)
v.check("23-01.6c", (1.6e-9 / 512) / (1.6e-9 / 8192))
v.check("23-01.6d", optimize.brentq(lambda nb: 1.6e-9 / (8 * nb) - 0.5e-12, 1, 1e5))
v.check("23-01.7a", optimize.brentq(lambda t: (3.0 / 1.6) ** (t / 2) - 2, 0.1, 10))
v.check("23-01.7b", optimize.brentq(lambda r: 3.0 / r - 1, 1, 10))
v.check("23-01.7c", 100 * grow(1.6, 5) / grow(3.0, 5))
for key, wb in (("23-01.8a", 2), ("23-01.8b", 1), ("23-01.8c", 0.5)):
    v.check(key, 3.35e12 / (7e9 * wb))
M9 = dict(params=7e9, w_bytes=2, layers=32, q_heads=32, kv_heads=8, head_dim=128, kv_b=2)
_, _, kv9 = layer_count(**M9, context=131_072, batch=1)
v.check("23-01.9a", kv9 / 131_072)
v.check("23-01.9b", kv9 / 1e9)
_, _, kv9m = layer_count(**{**M9, "kv_heads": 32}, context=131_072, batch=1)
v.check("23-01.9c", kv9m / 1e9)
_, _, kv10 = layer_count(**M9, context=32_768, batch=1)
v.check("23-01.10a", kv10 / 1e9)
b10 = max_batch_count(80e9, 14e9, kv10)
v.check("23-01.10b", b10)
sb10, _, _ = layer_count(**M9, context=32_768, batch=b10)
v.check("23-01.10c", sb10 / 1e9)
v.check("23-01.10d", sb10 / 3.35e12 * 1e3)
v.check("23-01.10e", b10 / (sb10 / 3.35e12))
# 23-01.11: half the limit, by root finding on the intensity curve
sb_1, sf_1, _ = layer_count(**M, context=CTX, batch=1)
f1 = sf_1
w_bytes = sb_1 - kv_seq
half = optimize.brentq(lambda b: b * f1 / (w_bytes + b * kv_seq) - 0.5 * f1 / kv_seq, 0.1, 1e4)
v.check("23-01.11b", half)
bs = np.linspace(0.1, 500, 2000)
v.assert_true("23-01.11: intensity rises monotonically with batch", np.all(np.diff(bs * f1 / (w_bytes + bs * kv_seq)) > 0))
e_sram = E["32b SRAM read (8 KB)"] / 32
v.check("23-01.12a", e_sram)
v.check("23-01.12b", 8 * 40e9 * e_sram * 1e-12)
v.check("23-01.12c", 8 * 40e9 * 6.86e-12)
v.check("23-01.12d", 6.86 / e_sram)
e13 = optimize.brentq(lambda e: 8 * 20e12 * e - 300, 1e-14, 1e-10)
v.check("23-01.13a", e13 * 1e12)
v.check("23-01.13b", 6.86e-12 / e13)
v.check("23-01.13c", math.ceil(optimize.brentq(lambda s: s * 2048 * 10e9 / 8 - 20e12, 0.1, 100)))
one_core = optimize.brentq(lambda bw: little_sim(bw / 64, 90e-9, 50_000) - 24, 1e9, 1e11, xtol=1e5)
bw14 = 12 * one_core
v.check("23-01.14a", bw14 / 1e9)
v.check("23-01.14b", min(bw14, 160e9) / 1e9)
v.check("23-01.14c", one_core / 1e9)

# ---------------------------------------------------------------- lab
print("Lab")
v.check("Lab 23-01.a", e_store * 1e15)
v.check("Lab 23-01.b", (e_src - e_store) * 1e15)
M4 = {**M, "kv_b": 0.5}
_, _, kv4 = layer_count(**M4, context=CTX, batch=1)
v.check("Lab 23-01.c", max_batch_count(288e9, 70e9, kv4))
sb4, sf4, _ = layer_count(**M4, context=CTX, batch=big)
v.check("Lab 23-01.d", sf4 / sb4)
v.check("Lab 23-01.e", 75_000 * 64 / 1.2e-6 / 1e12)

# ---------------------------------------------------------------- audit additions
v.check("Txt 23-01.o", 2.24 + 0.3 + 1.21)
v.check("Txt 23-01.p", 3.92)
v.check("Txt 23-01.q", 3.92 - (2.24 + 0.3 + 1.21))
v.check("Txt 23-01.r", 3 / 2)
_P, _L, _d, _k = 70e9, 80, 64 * 128, 2 * 80 * 8 * 128 * 1


def _limit(n):
    return (2 * _P + 4 * _L * _d * n) / (_k * n)


v.check("Txt 23-01.s", _limit(512))
v.check("Txt 23-01.t", _limit(1024))
v.check("Txt 23-01.u", optimize.brentq(lambda n: _limit(n) - 625, 100, 1e5))
v.check("Txt 23-01.v", 20 / 15)
v.check("Txt 23-01.w", 288 * 2 ** 30 / 1e9)
v.check("Txt 23-01.w1", 288 * 2 ** 30 / 1e9)
v.check("Txt 23-01.x", 300e9 / 2 ** 30)
v.check("Txt 23-01.y", (288 * 2 ** 30 - 300e9) / 1e9)
v.check("Txt 23-01.z", _k * 32768 / 1e9)
v.check("Txt 23-01.za", _k * 32768 / 2 ** 30)
v.check("Txt 23-01.zb", (288 * 2 ** 30 - 70e9) // (_k * 32768))
v.check("Txt 23-01.zc", (2 ** 30 / 1e9 - 1) * 100)

sys.exit(v.finish())
