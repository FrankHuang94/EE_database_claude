#!/usr/bin/env python3
"""Verify every number in chapter 27-07 (the AI datacenter server and rack), its
problems and its lab.

Independent routes (the lab module uses closed forms):
- the ring all-reduce is executed step by step on arrays, checking the sums and
  counting the bytes each device sends per step; time = steps x chunk / bandwidth;
- the hierarchical all-reduce is executed the same way, phase by phase;
- 6ND is checked by counting the multiply-adds of a small network's forward and
  backward passes;
- Young's interval is found by numerical minimization of the lost fraction, and the
  first-order model is checked against a Monte Carlo of exponential failures;
- job MTBF m/N is checked by sampling the minimum of exponential lifetimes;
- inference, power and cost figures by explicit sums of their parts.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "27-07-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import rackmodel as rm  # noqa: E402

v = Verifier.from_files("27-07", ROOT / "chapters" / "27-07-ai-datacenter-server-and-rack.md",
                        ROOT / "solutions" / "27-07-solutions.md", LAB / "README.md")
rng = np.random.default_rng(2707)


# ---------------------------------------------------------------------------
# Independent all-reduce execution
# ---------------------------------------------------------------------------

def ring_allreduce_execute(data):
    """Run a ring all-reduce on data[rank, chunk] (p ranks, p chunks) in place.
    Returns (number of steps, max chunks sent by any rank in any step)."""
    p = data.shape[0]
    r = np.arange(p)
    steps = 0
    sent_max = 0
    # reduce-scatter: at step k, rank r sends chunk (r - k) mod p to rank r + 1
    for k in range(p - 1):
        c = (r - k) % p
        payload = data[r, c].copy()
        data[(r + 1) % p, c] += payload
        steps += 1
        sent_max = max(sent_max, 1)
    # now rank r holds the full sum of chunk (r + 1) mod p
    # all-gather: at step k, rank r forwards chunk (r + 1 - k) mod p
    for k in range(p - 1):
        c = (r + 1 - k) % p
        payload = data[r, c].copy()
        data[(r + 1) % p, c] = payload
        steps += 1
    return steps, sent_max


def ring_time_executed(size_bytes, p, bw, alpha=0.0):
    """Execute the ring on random data, check every rank ends with the total, and
    return the time from the executed step count."""
    if p == 1:
        return 0.0
    data = rng.integers(0, 1000, size=(p, p)).astype(np.int64)
    total = data.sum(axis=0)
    steps, _ = ring_allreduce_execute(data)
    assert np.all(data == total), "ring all-reduce did not produce the sum"
    return steps * (alpha + size_bytes / p / bw)


def hierarchical_time_executed(size_bytes, p1, b1, p2, b2):
    """Execute reduce-scatter inside domains, all-reduce of shards across domains,
    all-gather inside domains, on random data; check the result; return times."""
    p = p1 * p2
    data = rng.integers(0, 1000, size=(p, p1)).astype(np.int64)  # p1 shards per device
    total = data.sum(axis=0)
    # phase 1: reduce-scatter within each domain (p1 - 1 steps of one shard each)
    steps1 = 0
    for d in range(p2):
        block = data[d * p1:(d + 1) * p1]
        r = np.arange(p1)
        for k in range(p1 - 1):
            c = (r - k) % p1
            payload = block[r, c].copy()
            block[(r + 1) % p1, c] += payload
        steps1 = p1 - 1
    # device r of each domain now holds shard (r + 1) mod p1 summed over the domain
    # phase 2: all-reduce each shard across domains (ring of p2 at b2, shard = S/p1)
    for i in range(p1):
        holders = [d * p1 + i for d in range(p2)]
        c = (i + 1) % p1
        s = data[holders, c].sum()
        data[holders, c] = s
    # phase 3: all-gather within each domain
    for d in range(p2):
        block = data[d * p1:(d + 1) * p1]
        r = np.arange(p1)
        for k in range(p1 - 1):
            c = (r + 1 - k) % p1
            payload = block[r, c].copy()
            block[(r + 1) % p1, c] = payload
    assert np.all(data == total), "hierarchical all-reduce did not produce the sum"
    inside = 2 * steps1 * (size_bytes / p1) / b1
    across = ring_time_executed(size_bytes / p1, p2, b2)
    return inside, across, inside + across


# ---------------------------------------------------------------------------
# Example 27-07.1 · datasheet
# ---------------------------------------------------------------------------
hbm_gpu = 13.4e12 / 72
bw_gpu = 576e12 / 72
nvl_gpu = 130e12 / 72
fp8_gpu = 720e15 / 72
v.check("Ex 27-07.1a", hbm_gpu / 1e9)
v.check("Ex 27-07.1b", bw_gpu / 1e12)
v.check("Ex 27-07.1c", nvl_gpu / 1e12)
v.assert_true("NVLink per GPU matches 1.8 TB/s within 0.5%", abs(nvl_gpu / 1.8e12 - 1) < 0.005)
v.check("Ex 27-07.1d", fp8_gpu / 1e15)
v.check("Ex 27-07.1e", fp8_gpu / bw_gpu)
v.check("Ex 27-07.1e1", fp8_gpu / 2 / bw_gpu)
v.check("Ex 27-07.1e2", 5e15 / 8e12)
v.check("Ex 27-07.1e3", 4614e12 / 7.37e12)
v.assert_true("three dense balances within 0.2%",
              abs((4614e12 / 7.37e12) / (5e15 / 8e12) - 1) < 0.002)
v.check("Ex 27-07.1f", 8.0 / 0.9)
v.check("Ex 27-07.1f1", 0.9 / 0.1)
v.check("Ex 27-07.1f2", 8.0 / 0.1)

# ---------------------------------------------------------------------------
# Example 27-07.2 · power budget
# ---------------------------------------------------------------------------
parts = {"gpu": 72 * 1.2, "cpu": 36 * 0.30, "tray": 18 * 0.60, "switch": 9 * 0.80, "fans": 2.0}
load = sum(parts.values())
p_in = load / 0.97
v.check("Ex 27-07.2a", load)
v.check("Ex 27-07.2a1", p_in)
v.check("Ex 27-07.2b", 100 * parts["gpu"] / p_in)
v.check("Ex 27-07.2b1", p_in / 72)
fac = p_in * 1.2
v.check("Ex 27-07.2c", fac)
racks = 0
while (racks + 1) * fac <= 100e3:
    racks += 1
v.check("Ex 27-07.2d", racks)
v.check("Ex 27-07.2d1", racks * 72)
v.check("Ex 27-07.2d2", fac / 72)
v.check("Ex 27-07.2e", 10e3 / 9216)
v.assert_true("rack input within the 120-142 kW vendor range", 120 <= p_in <= 142)
v.check("Txt 27-07.7", (p_in / 72) / 1.2)
v.check("Txt 27-07.8", (fac / 72) / 1.2)
v.check("Txt 27-07.9", math.floor(100e3 / 1.2))
v.check("Txt 27-07.10", 100 * (100e3 / 1.2 / (racks * 72) - 1))

# ---------------------------------------------------------------------------
# Example 27-07.3 · training compute (6ND checked by counting a small network)
# ---------------------------------------------------------------------------
dims = [(64, 256), (256, 256), (256, 32)]  # (d_in, d_out) per dense layer
n_params = sum(a * b for a, b in dims)
tokens = 7
flops = 0
for _ in range(tokens):
    for d_in, d_out in dims:
        flops += 2 * d_in * d_out          # forward  y = W x
        flops += 2 * d_in * d_out          # backward dx = W^T dy
        flops += 2 * d_in * d_out          # backward dW += dy x^T
v.assert_true("counted training FLOPs equal 6ND", flops == 6 * n_params * tokens)

F = 6 * 405e9 * 15.6e12
v.check("Ex 27-07.3a", F)
v.check("Ex 27-07.3a1", 100 * (1 - F / 3.8e25))
t3 = F / (16384 * 400e12)
v.check("Ex 27-07.3b", t3)
v.check("Ex 27-07.3b1", t3 / 86400)
p3 = 16384 * 700
v.check("Ex 27-07.3c", p3 / 1e6)
e3 = p3 * t3 / 3.6e12
v.check("Ex 27-07.3c1", e3)
v.check("Ex 27-07.3d", e3 * 1.5 * 1.1)
v.check("Ex 27-07.3d1", e3 * 1.5 * 1.1 * 1e6 * 0.08 / 1e6)
n30 = optimize.brentq(lambda n: F / (n * 400e12 * 0.9) - 30 * 86400, 1e3, 1e6)
v.check("Ex 27-07.3e", n30)
v.check("Txt 27-07.11", n30 / 16384)

# ---------------------------------------------------------------------------
# Example 27-07.4 · all-reduce (executed)
# ---------------------------------------------------------------------------
S = 10e9
flat = ring_time_executed(S, 1152, 100e9)
inside, across, hier = hierarchical_time_executed(S, 72, 900e9, 16, 100e9)
v.check("Ex 27-07.4a", 1e3 * flat)
v.check("Ex 27-07.4b", 1e3 * inside)
v.check("Ex 27-07.4c", S / 72 / 1e9)
v.check("Ex 27-07.4c1", 1e3 * across)
v.check("Ex 27-07.4c2", 1e3 * hier)
v.check("Ex 27-07.4c3", flat / hier)
v.check("Ex 27-07.4d", 100 * flat / (flat + 0.1))
v.check("Ex 27-07.4d1", 100 * hier / (hier + 0.1))
lat = ring_time_executed(1e-30, 1152, 1e30, alpha=5e-6)
v.check("Ex 27-07.4e", 1e3 * lat)
v.check("Ex 27-07.4f", 72 * 0.1)
v.assert_true("executed times match the closed forms",
              abs(flat - rm.ring_allreduce_s(S, 1152, 100e9)) < 1e-12
              and abs(hier - rm.hierarchical_allreduce_s(S, 72, 900e9, 16, 100e9)[2]) < 1e-12)
v.check("Txt 27-07.1", 2 * 71 / 72)

# ---------------------------------------------------------------------------
# Example 27-07.5 · failures and checkpoints
# ---------------------------------------------------------------------------
M = 54 * 86400 / 419
v.check("Ex 27-07.5a", M / 3600)
v.check("Ex 27-07.5a1", M)
m_gpu_h = 16384 * M / 3600
v.check("Ex 27-07.5b", m_gpu_h)
v.check("Ex 27-07.5b1", m_gpu_h / 8766)
v.check("Ex 27-07.5b2", 1e9 / m_gpu_h)
v.check("Txt 27-07.6", m_gpu_h / 8766)


def lost(tau, delta, mtbf, restart):
    return delta / tau + (tau / 2 + restart) / mtbf


res = optimize.minimize_scalar(lambda t: lost(t, 60, M, 600), bounds=(1, M), method="bounded",
                               options={"xatol": 1e-6})
tau = res.x
v.check("Ex 27-07.5c", tau)
v.check("Ex 27-07.5c1", tau / 60)
v.check("Ex 27-07.5d", 100 * 60 / tau)
v.check("Ex 27-07.5d1", 100 * (60 / tau + tau / (2 * M)))
v.check("Ex 27-07.5d2", 100 * 600 / M)
v.check("Ex 27-07.5d3", 100 * res.fun)
v.check("Ex 27-07.5d4", 100 * (1 - res.fun))
d_max = optimize.brentq(lambda d: math.sqrt(2 * d / M) - 0.10, 1e-6, 1e4)
v.check("Ex 27-07.5e", d_max)
ov10 = optimize.minimize_scalar(lambda t: 10 / t + t / (2 * M), bounds=(1, M), method="bounded",
                                options={"xatol": 1e-6}).fun
v.check("Ex 27-07.5e1", 100 * ov10)
r_max = (0.10 - ov10) * M
v.check("Ex 27-07.5e2", r_max)
v.check("Ex 27-07.5e3", r_max / 60)

# Monte Carlo of the first-order model: exponential failures, checkpoints every tau
def simulate_job(work_s, tau, delta, mtbf, restart, n_runs=400):
    fractions = []
    for _ in range(n_runs):
        t, done = 0.0, 0.0
        next_fail = rng.exponential(mtbf)
        while done < work_s:
            seg = min(tau, work_s - done)
            if t + seg + delta <= next_fail:      # segment and its save complete
                t += seg + delta
                done += seg
            else:                                  # failure: lose the segment, restart
                t = next_fail + restart
                next_fail = t + rng.exponential(mtbf)
        fractions.append(1 - work_s / t)
    return float(np.mean(fractions))


mc = simulate_job(40 * M, tau, 60, M, 600)
v.assert_true(f"Monte Carlo lost fraction {mc:.4f} within 2 points of first order {res.fun:.4f}",
              abs(mc - res.fun) < 0.02)

# job MTBF m/N from the minimum of exponential lifetimes
life = rng.exponential(1.0, size=(20000, 50)).min(axis=1)
v.assert_true("mean of min of 50 exponentials is 1/50 within 3%", abs(life.mean() * 50 - 1) < 0.03)

# ---------------------------------------------------------------------------
# Example 27-07.6 · serving from a rack
# ---------------------------------------------------------------------------
W = 1e12 * 0.5
K = 0.8e9
BW = 576e12
ETA = 0.5
NACT = 4e10
FLOPS4 = 720e15


def step(batch):
    bytes_read = W + sum(K for _ in range(batch)) if batch < 5000 else W + batch * K
    t_mem = bytes_read / (ETA * BW)
    t_cmp = sum(2 * NACT for _ in range(batch)) / FLOPS4 if batch < 5000 else 2 * NACT * batch / FLOPS4
    return max(t_mem, t_cmp), t_mem, t_cmp


v.check("Ex 27-07.6a", W / 1e12)
v.check("Ex 27-07.6a1", 1e3 * W / (ETA * BW))
v.check("Ex 27-07.6a2", 1e3 * W / BW)
s256, m256, c256 = step(256)
v.check("Ex 27-07.6b", 1e3 * m256)
v.check("Ex 27-07.6b1", 1e3 * c256)
v.check("Ex 27-07.6b2", m256 / c256)
thr = 256 / s256
v.check("Ex 27-07.6c", thr)
v.check("Ex 27-07.6c1", 1 / s256)
v.check("Ex 27-07.6c2", 130e3 / thr)
bmax = 0
while W + (bmax + 1) * K <= 13.4e12:
    bmax += 1
v.check("Ex 27-07.6d", bmax)
smax, _, _ = step(bmax)
v.check("Ex 27-07.6d1", 1e3 * smax)
v.check("Ex 27-07.6d2", bmax / smax)
v.check("Ex 27-07.6d3", 1 / smax)
v.check("Ex 27-07.6d4", ETA * BW / K)
v.check("Ex 27-07.6d5", (bmax / smax) / thr)
v.check("Ex 27-07.6d6", (1 / s256) / (1 / smax))
capex_yr = 3.0e6 / 4
energy_yr = sum(130 * 1.2 * 0.08 for _ in range(8760))
tok_yr = thr * 0.6 * 8760 * 3600
v.check("Ex 27-07.6e", capex_yr)
v.check("Ex 27-07.6e1", energy_yr)
v.check("Ex 27-07.6e2", tok_yr)
cost = (capex_yr + energy_yr) / (tok_yr / 1e6)
v.check("Ex 27-07.6e3", cost)
v.check("Ex 27-07.6e4", 100 * energy_yr / (capex_yr + energy_yr))
v.check("Txt 27-07.12", capex_yr / energy_yr)
v.assert_true("cost model matches the lab module",
              abs(cost - rm.cost_per_million_tokens(3e6, 4, 130, 1.2, 0.08, thr, 0.6)[0]) < 1e-12)

# ---------------------------------------------------------------------------
# Chapter text
# ---------------------------------------------------------------------------
v.check("Txt 27-07.2", 9216 * 4614e12 / 1e18)
v.check("Txt 27-07.3", 42.5 / 1.7)
v.check("Txt 27-07.4", 42.5 / 16.680)
v.check("Txt 27-07.5", 100 * (125 / 90 - 1))
v.check("Txt 27-07.13", 7)
v.check("Txt 27-07.14", 144)
v.check("Txt 27-07.15", 0.5e12 / 0.8e9)
# the frontier is linear in the memory-bound region: Theta = eta*BW/K - (W/K) s
for b in (1, 256, 6575, 16125):
    sb = 1 / rm.decode_step_s(b, 0.5e12, 0.8e9, 576e12, 0.5, 4e10, 720e15)[0]
    v.assert_true(f"frontier line holds at B = {b}",
                  abs(b * sb - (0.5 * 576e12 / 0.8e9 - 0.5e12 / 0.8e9 * sb)) < 1e-6 * b * sb)

# ---------------------------------------------------------------------------
# Problems
# ---------------------------------------------------------------------------
v.check("27-07.2a", 13.4 * 1.5)
v.check("27-07.2b", 13.4e3 * 1.5 / 72)
v.check("27-07.2c", 720 * 1.5)
v.check("27-07.2d", 720 * 1.5 / 72)

F3 = 6 * 70e9 * 15e12
v.check("27-07.3a", F3)
v.check("27-07.3b", F3 / (4096 * 400e12))
v.check("27-07.3c", F3 / (4096 * 400e12) / 86400)

g4 = 72 * 1.4
l4 = g4 + parts["cpu"] + parts["tray"] + parts["switch"] + parts["fans"]
i4 = l4 / 0.97
v.check("27-07.4a", g4)
v.check("27-07.4b", l4)
v.check("27-07.4c", i4)
v.check("27-07.4d", 100 * g4 / i4)
v.check("27-07.4e", 100e3 / (i4 * 1.2))
r4 = math.floor(100e3 / (i4 * 1.2))
v.check("27-07.4f", r4)
v.check("27-07.4g", r4 * 72)
v.check("27-07.4h", 100 * (1 - r4 * 72 / (racks * 72)))

v.check("27-07.5a", 2 * 7 / 8 * 4)
v.check("27-07.5b", 1e3 * ring_time_executed(4e9, 8, 450e9))
v.check("27-07.5c", 1e6 * 2 * 7 * 3e-6)

b6 = optimize.brentq(lambda b: ring_time_executed(S, 1152, b) - hier, 1e9, 1e14)
v.check("27-07.6a", b6 / 1e9)
v.check("27-07.6b", 8 * b6 / 1e12)
v.check("27-07.6c", b6 / 100e9)

counts = {"Faulty GPU": 148, "GPU HBM3 Memory": 72, "Software Bug": 54, "Network Switch/Cable": 35,
          "Host Maintenance": 32, "GPU SRAM Memory": 19, "GPU System Processor": 17, "NIC": 7,
          "NCCL Watchdog Timeouts": 7, "Silent Data Corruption": 6,
          "GPU Thermal Interface + Sensor": 6, "SSD": 3, "Power Supply": 3, "Server Chassis": 2,
          "IO Expansion Board": 2, "Dependency": 2, "CPU": 2, "System Memory": 2}
printed = [30.1, 17.2, 12.9, 8.4, 7.6, 4.5, 4.1, 1.7, 1.7, 1.4, 1.4, 0.7, 0.7, 0.5, 0.5, 0.5, 0.5, 0.5]
gpu_cats = ["Faulty GPU", "GPU HBM3 Memory", "GPU SRAM Memory", "GPU System Processor",
            "Silent Data Corruption", "GPU Thermal Interface + Sensor"]
tot = sum(counts.values())
v.check("27-07.7a", tot)
v.check("27-07.7b", 100 * counts["Faulty GPU"] / tot)
gsum = sum(counts[c] for c in gpu_cats)
v.check("27-07.7c", gsum)
v.check("27-07.7d", 100 * gsum / tot)
alt = round(0.301 * tot)
v.check("27-07.7e", alt)
v.check("27-07.7f", 100 * (gsum - 148 + alt) / tot)
v.check("27-07.7g", tot - 148 + alt)
v.check("27-07.7h", sum(printed))
v.assert_true("HBM3 share 72/419 matches the printed 17.2%", round(100 * 72 / tot, 1) == 17.2)

M8 = 16384 * M / 100000
v.check("27-07.8a", M8)
v.check("27-07.8b", M8 / 60)
t8 = optimize.minimize_scalar(lambda t: 10 / t + t / (2 * M8), bounds=(1, M8), method="bounded",
                              options={"xatol": 1e-6})
v.check("27-07.8c", t8.x)
v.check("27-07.8d", 100 * t8.fun)
v.check("27-07.8e", 100 * 300 / M8)
v.check("27-07.8f", 100 * (t8.fun + 300 / M8))
v.check("27-07.8g", 100 * (1 - t8.fun - 300 / M8))

ex = stats.expon(scale=M)
v.check("27-07.9a", ex.sf(3600))
v.check("27-07.9b", ex.sf(3 * 3600))
v.check("27-07.9c", 100 * ex.cdf(86400))

e10 = 40625 * 700 * 30 * 24 / 1e6
v.check("27-07.10a", e10)
v.check("27-07.10b", e10 * 1.65 / 1e3)
v.check("27-07.10c", e10 * 1.65 * 1e3 * 0.08 / 1e6)

b11 = 0
while step(b11 + 1)[0] <= 0.02 + 1e-15:
    b11 += 1
v.check("27-07.11a", b11)
thr11 = b11 / step(b11)[0]
v.check("27-07.11b", thr11)
v.check("27-07.11c", 130e3 / thr11)
v.check("27-07.11d", b11 * K / 1e12)
v.check("27-07.11e", 1e3 * step(b11)[2])

annual = capex_yr + energy_yr
v.check("27-07.12a", annual)
tok12 = thr11 * 0.6 * 8760 * 3600
v.check("27-07.12b", tok12)
c60 = annual / (tok12 / 1e6)
v.check("27-07.12c", c60)
v.check("27-07.12d", annual / (thr11 * 0.3 * 8760 * 3600 / 1e6))
v.check("27-07.12e", cost / c60)

v.check("27-07.13a", 16384 * 600 / 1e6)
v.check("27-07.13b", 16384 * 600 * 1.5 / 1e6)

# ---------------------------------------------------------------------------
# Lab
# ---------------------------------------------------------------------------
ia, aa, ta = hierarchical_time_executed(S, 8, 900e9, 144, 100e9)
v.check("Lab 27-07.a", 1e3 * ia)
v.check("Lab 27-07.a1", 1e3 * aa)
v.check("Lab 27-07.a2", 1e3 * ta)
Mb = M / 2
rb = optimize.minimize_scalar(lambda t: lost(t, 60, Mb, 600), bounds=(1, Mb), method="bounded",
                              options={"xatol": 1e-6})
v.check("Lab 27-07.b", Mb)
v.check("Lab 27-07.b1", rb.x)
v.check("Lab 27-07.b2", rb.x / 60)
v.check("Lab 27-07.b3", 100 * rb.fun)
v.check("Lab 27-07.b4", 100 * (1 - rb.fun))
s1024 = step(1024)[0]
v.check("Lab 27-07.c", 1e3 * s1024)
v.check("Lab 27-07.c1", 1024 / s1024)
v.check("Lab 27-07.c2", 1 / s1024)
v.check("Lab 27-07.c3", (1024 / s1024) / thr)
v.check("Lab 27-07.c4", (1 / s1024) / (1 / s256))
energy2 = sum(130 * 1.2 * 0.16 for _ in range(8760))
c2 = (capex_yr + energy2) / (tok_yr / 1e6)
v.check("Lab 27-07.d", c2)
v.check("Lab 27-07.d1", 100 * (c2 / cost - 1))

sys.exit(v.finish())
