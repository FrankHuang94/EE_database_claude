#!/usr/bin/env python3
"""Verify every number in chapter 23-07 (SSD controllers and storage systems), its problems and its lab.

Independent routes (the lab module ssd.py uses closed forms and scipy's Lambert W):
- link bandwidths by counting payload bits per encoded block;
- write amplification by solving the fixed point u = exp(-alpha (1 - u)) with a root finder, and by an
  independent FIFO log simulation that must agree within 2%;
- codeword failure probabilities by summing binomial terms in logarithms;
- channel capacity from the entropy written out term by term;
- power-loss-protection capacitance by integrating the bank's discharge C dV/dt = -P/(eta V) and bisecting
  for the capacitance that lasts the hold-up time.
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, special

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "23-07-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("23-07", ROOT / "chapters" / "23-07-ssd-controllers.md",
                        ROOT / "solutions" / "23-07-solutions.md", LAB / "README.md")


# ---------------------------------------------------------------- independent helpers
def link_bytes_per_s(gt, lanes, payload_bits=128, block_bits=130):
    """Bytes per second: symbols per second per lane x payload fraction x lanes / 8."""
    blocks_per_s = gt * lanes / block_bits
    return blocks_per_s * payload_bits / 8


def u_fixed_point(alpha):
    """Valid fraction of FIFO victims: the nontrivial root of u = exp(-alpha (1 - u))."""
    return optimize.brentq(lambda u: u - math.exp(-alpha * (1 - u)), 1e-12, 1 - 1e-9)


def wa(alpha):
    return 1 / (1 - u_fixed_point(alpha))


def fifo_log_sim(user, alpha, steps, seed=7):
    """FIFO cleaning with one-page blocks as a circular log.

    The slot at the head is the oldest. If it still holds a valid page, cleaning copies that page to the write
    frontier, which in a circular log of fixed size means it stays in its slot and counts as a NAND write.
    """
    rng = random.Random(seed)
    phys = int(round(user * alpha))
    owner = [-1] * phys
    loc = list(range(user))
    for lba in range(user):
        owner[lba] = lba
    head = user % phys
    nand = host = 0
    for i in range(steps):
        if i == steps // 3:
            nand = host = 0
        lba = rng.randrange(user)
        owner[loc[lba]] = -1
        while owner[head] >= 0:
            nand += 1
            head = (head + 1) % phys
        owner[head] = lba
        loc[lba] = head
        head = (head + 1) % phys
        nand += 1
        host += 1
    return nand / host


def log_binom_sf(t, n, p):
    """log P(X > t) for X ~ Binomial(n, p), summing terms in logarithms."""
    k = np.arange(t + 1, n + 1)
    logs = (special.gammaln(n + 1) - special.gammaln(k + 1) - special.gammaln(n - k + 1)
            + k * math.log(p) + (n - k) * math.log1p(-p))
    m = logs.max()
    return m + math.log(np.exp(logs - m).sum())


def capacity(p):
    h = -(p * math.log(p) + (1 - p) * math.log(1 - p)) / math.log(2)
    return 1 - h


def hold_time(c, power, v1, v2, eff):
    """Seconds a capacitor c lasts from v1 to v2 feeding power through a converter of efficiency eff."""
    sol = integrate.solve_ivp(lambda t, y: [-power / eff / (c * y[0])], (0, 10), [v1],
                              events=lambda t, y: y[0] - v2, rtol=1e-10, atol=1e-12)
    return sol.t_events[0][0]


def plp_c(power, th, v1, v2, eff):
    return optimize.brentq(lambda c: hold_time(c, power, v1, v2, eff) - th, 1e-5, 1e-1, xtol=1e-12)


# ---------------------------------------------------------------- Example 23-07.1
b5 = link_bytes_per_s(32e9, 4)
v.check("Ex 23-07.1a", b5 / 1e9)
b6 = link_bytes_per_s(64e9, 4, 1, 1)
v.check("Ex 23-07.1b", b6 / 1e9)
v.check("Ex 23-07.1c", 28e9 / b6 * 100)
pay6 = b6 * 236 / 256
v.check("Ex 23-07.1d", pay6 / 1e9)
v.check("Ex 23-07.1e", 28e9 / pay6 * 100)
v.check("Ex 23-07.1g", pay6 * 512 / 528 / 1e9)
v.check("Ex 23-07.1h", 28e9 / (pay6 * 512 / 528) * 100)
v.check("Ex 23-07.1g1", pay6 * 256 / 272 / 1e9)
v.check("Ex 23-07.1f", 16 * 2400e6 * 8 / 8 / 1e9)

# ---------------------------------------------------------------- Example 23-07.2
units = 30_720_000_000_000 // 4096
v.check("Ex 23-07.2a", units)
v.check("Ex 23-07.2b", units * 4 / 1e9)
v.check("Txt 23-07.a", 1e12 // 4096 * 4 / 1e9)
v.check("Ex 23-07.2c", (1 << 32) * 4096 / 1e12)
v.check("Ex 23-07.2d0", math.log2(units))
v.check("Ex 23-07.2d", units.bit_length())
units16 = 61_440_000_000_000 // 16384
v.check("Ex 23-07.2e", units16)
v.check("Ex 23-07.2f", units16 * 4 / 1e9)
v.assert_true("61.44 TB at 16 KiB fits 32-bit entries", units16 < (1 << 32))
v.check("Ex 23-07.2g", (1 << 32) * 16384 / 1e12)
v.check("Ex 23-07.2h", 16384 // 4096)
v.check("Txt 23-07.i", 61.44 * 1.07)
v.check("Txt 23-07.j", 61.44 * 1.28)
v.assert_true("65.7 TB raw fits 32-bit reach at 16 KiB; 78.6 TB does not", 61.44e12 * 1.07 < (1 << 32) * 16384 < 61.44e12 * 1.28)
v.check("Txt 23-07.k", units * 5 / 1e9)
v.check("Txt 23-07.l", next(m for m in range(2, 30) if 8192 + m * 40 <= 2 ** m - 1))
v.check("Txt 23-07.m", next(m for m in range(2, 30) if 16384 + m * 40 <= 2 ** m - 1))

# ---------------------------------------------------------------- Example 23-07.3
for ident, op in (("a", 0.07), ("b", 0.28)):
    a = 1 + op
    v.check(f"Ex 23-07.3{ident}0", a)
    v.check(f"Ex 23-07.3{ident}1", u_fixed_point(a))
    v.check(f"Ex 23-07.3{ident}", wa(a))
v.check("Txt 23-07.b", wa(1.07))
v.check("Txt 23-07.c", wa(1.07) / wa(1.28))
asf = 1 / (1 - 0.07)
v.check("Ex 23-07.3c0", asf)
v.check("Ex 23-07.3c", wa(asf))
v.check("Ex 23-07.3c1", (wa(asf) - 6.62) / wa(asf) * 100)
for alpha in (1.07, 1.28):
    sim = fifo_log_sim(20000, alpha, 300000)
    v.assert_true(f"FIFO log simulation agrees with the fixed point at alpha {alpha} (sim {sim:.3f})",
                  abs(sim / wa(alpha) - 1) < 0.02)

# ---------------------------------------------------------------- Example 23-07.4
raw = 8.8
res = {}
for ident, user in (("a", 7.68), ("b", 6.4)):
    a = raw / user
    A = wa(a)
    tbw = raw * 3000 / A
    dw = tbw / (user * 5 * 365)
    res[ident] = dw
    v.check(f"Ex 23-07.4{ident}0", (a - 1) * 100)
    v.check(f"Ex 23-07.4{ident}1", A)
    v.check(f"Ex 23-07.4{ident}2", tbw)
    v.check(f"Ex 23-07.4{ident}", dw)
    v.check(f"Ex 23-07.4{ident}3", dw)
v.check("Ex 23-07.4a1x", wa(raw / 7.68))
v.check("Ex 23-07.4c", res["b"] / res["a"])
v.check("Ex 23-07.4c1", (1 - 6.4 / 7.68) * 100)
v.check("Txt 23-07.d", 3 / 1)

# ---------------------------------------------------------------- Example 23-07.5
n5 = 8192 + 14 * 40
v.check("Ex 23-07.5a", 14 * 40)
v.check("Ex 23-07.5a1", 14 * 40 / 8)
v.check("Ex 23-07.5b", n5)
for ident, p in (("c", 1e-3), ("d", 3e-3), ("e", 4e-3)):
    v.check(f"Ex 23-07.5{ident}0", n5 * p)
    v.check(f"Ex 23-07.5{ident}", math.exp(log_binom_sf(40, n5, p)))
v.check("Ex 23-07.5f", 1 / math.exp(log_binom_sf(40, n5, 3e-3)))
pf5 = math.exp(log_binom_sf(40, n5, 1e-3))
v.check("Txt 23-07.p", 40 + 1)
v.check("Txt 23-07.n", 41 * pf5 / 8192)
v.check("Txt 23-07.o", pf5 / (41 * pf5 / 8192))
v.assert_true("UBER at 1e-3 meets the 1e-16 enterprise target", 41 * pf5 / 8192 < 1e-16)
v.check("Txt 23-07.f", math.log10(1e-3 / 1e-15))

# ---------------------------------------------------------------- Example 23-07.6
rate = 16 / 18
v.check("Ex 23-07.6a", rate)
v.check("Ex 23-07.6b", capacity(0.01))
v.check("Ex 23-07.6c", capacity(0.02))
v.check("Ex 23-07.6d", optimize.brentq(lambda p: capacity(p) - rate, 1e-4, 0.1) * 100)

# ---------------------------------------------------------------- Example 23-07.7
v.check("Ex 23-07.7a", 5.4e6 * 100e-6)
v.check("Ex 23-07.7b", 5.4e6 * 4096 / 1e9)
per_die = 4 / 50e-6
v.check("Ex 23-07.7c", per_die)
v.check("Ex 23-07.7d0", 5.4e6 / per_die)
v.check("Ex 23-07.7d", math.ceil(5.4e6 / per_die))
v.check("Ex 23-07.7e", 1 / 100e-6)
v.check("Txt 23-07.h", 15000)
v.check("Txt 23-07.g", 1 / 15000 * 1e6)

# ---------------------------------------------------------------- Example 23-07.8
e8 = 20 * 0.025 / 0.9
v.check("Ex 23-07.8a", e8)
v.check("Ex 23-07.8a1", e8)
v.check("Ex 23-07.8a2", 2 * e8)
v.check("Ex 23-07.8b0", 35 ** 2 - 12 ** 2)
c35 = plp_c(20, 0.025, 35, 12, 0.9)
v.check("Ex 23-07.8b", c35 * 1e3)
v.check("Ex 23-07.8c0", 12.5 ** 2 - 5 ** 2)
c12 = plp_c(20, 0.025, 12.5, 5, 0.9)
v.check("Ex 23-07.8c", c12 * 1e3)
v.check("Ex 23-07.8d", c12 / c35)

# ---------------------------------------------------------------- problems
v.check("23-07.1a", link_bytes_per_s(16e9, 4) / 1e9)
v.check("23-07.1b", link_bytes_per_s(32e9, 2) / 1e9)
v.check("23-07.1c", link_bytes_per_s(64e9, 8, 1, 1) / 1e9)

v.check("23-07.2a", 3_840_000_000_000 // 4096 * 4 / 1e9)
e2 = 122_880_000_000_000 // 16384
v.check("23-07.2b", e2)
v.check("23-07.2c0", math.log2(e2))
v.check("23-07.2c", e2.bit_length())
v.check("23-07.2d", e2 * 5 / 1e9)

for ident, op in (("a", 0.10), ("b", 0.20)):
    v.check(f"23-07.3{ident}0", u_fixed_point(1 + op))
    v.check(f"23-07.3{ident}", wa(1 + op))
v.check("23-07.3c", 0.1 / 1.1 * 100)
v.check("23-07.3d", 0.2 / 1.2 * 100)
v.check("23-07.3e", wa(1.1) - 1)
v.check("23-07.3f", wa(1.2) - 1)

u4 = u_fixed_point(1.5)
v.check("23-07.4c0", u4)
v.check("23-07.4c", 1 / (1 - u4))
v.check("23-07.4c1", 1 - u4)
v.check("23-07.4c2", 1.5 * (1 - u4))
v.check("23-07.4c3", math.exp(-1.5 * (1 - u4)))

ae = 1.07 / 0.8
v.check("23-07.5a", ae)
v.check("23-07.5b", wa(ae))
v.check("23-07.5c", wa(1.07))
v.check("23-07.5d", wa(1.07) / wa(ae))

a6 = 33.0 / 30.72
A6 = wa(a6)
v.check("23-07.6a", (a6 - 1) * 100)
v.check("23-07.6b", A6)
v.check("23-07.6b1", A6)
t6 = 33.0 * 1000 / A6
v.check("23-07.6c", t6)
v.check("23-07.6d", t6 / (30.72 * 1825))
v.check("23-07.6e", t6 / 4 / (30.72 * 1825))

n7 = 16384 + 15 * 60
v.check("23-07.7a", 15 * 60)
v.check("23-07.7b", n7)
v.check("23-07.7c", n7 * 2e-3)
v.check("23-07.7d", math.exp(log_binom_sf(60, n7, 2e-3)))
p7 = optimize.brentq(lambda p: log_binom_sf(60, n7, p) - math.log(1e-15), 1e-4, 3e-3, xtol=1e-14)
v.check("23-07.7e", p7)
v.check("23-07.7f", n7 * p7)

r8 = 16 / 17
v.check("23-07.8a", r8)
lim8 = optimize.brentq(lambda p: capacity(p) - r8, 1e-5, 0.1)
v.check("23-07.8b", lim8 * 100)
v.check("23-07.8e", lim8 * 100)
v.check("23-07.8c", capacity(0.005))
v.check("23-07.8d", optimize.brentq(lambda p: capacity(p) - 16 / 18, 1e-4, 0.1) * 100)

v.check("23-07.9a", 32 / 80e-6)
v.check("23-07.9b", 1 / 80e-6)
v.check("23-07.9c", 2e6 * 120e-6)

v.check("23-07.10a", 4096 / 2.4e9 * 1e6)
v.check("23-07.10b", 2.4e9 / 4096)
v.check("23-07.10c", 8 * 2.4e9 / 4096)
v.check("23-07.10d", 8 * 4 * 4 / 60e-6)
v.assert_true("dies, not channels, limit Problem 23-07.10", 8 * 4 * 4 / 60e-6 < 8 * 2.4e9 / 4096)

e11 = 15 * 0.040 / 0.88
v.check("23-07.11a", e11)
v.check("23-07.11a1", e11)
v.check("23-07.11a2", 2 * e11)
v.check("23-07.11b0", 28 ** 2 - 10 ** 2)
c11 = plp_c(15, 0.040, 28, 10, 0.88)
v.check("23-07.11b", c11 * 1e3)
v.check("23-07.11b1", c11 * 1e3)
v.check("23-07.11c", 0.5 * c11 * 10 ** 2)
v.check("23-07.11d", 10 ** 2 / 28 ** 2 * 100)
v.check("23-07.11e", 20 ** 2 / 28 ** 2)

v.check("23-07.12a", 200 / 6)
v.check("23-07.12b", 100 / 1.5)
v.check("23-07.12c0", 200 / 6 + 100 / 1.5)
v.check("23-07.12c", 300 / (200 / 6 + 100 / 1.5))
v.check("23-07.12d", 200 * 3)

a13 = optimize.brentq(lambda a: a * 3000 / (wa(a) * 1825) - 3, 1.01, 5, xtol=1e-12)
v.check("23-07.13b", a13)
v.check("23-07.13b1", a13)
v.check("23-07.13c", wa(a13))
v.check("23-07.13d", (a13 - 1) * 100)
v.check("23-07.13e", 8.8 / a13)

host14 = 0.5e9 * 5 * 365 * 86400
v.check("23-07.14a", host14 / 1e15)
v.check("23-07.14b", 2 * host14 / 1e15)
v.check("23-07.14b1", 2 * host14 / 1e15)
v.check("23-07.14c", 2 * host14 / 130e12)
v.check("23-07.14d", 2 * host14 / 130e12)
v.assert_true("five years flat out stays within 1,500 cycles", 2 * host14 / 130e12 < 1500)

# ---------------------------------------------------------------- lab
v.check("Lab 23-07.a", wa(1.07))
v.check("Lab 23-07.b", wa(1.14))
v.check("Lab 23-07.c", wa(1.28))
lims = {}
for ident, t in (("d", 20), ("e", 40), ("f", 60)):
    n = 8192 + 14 * t
    lims[t] = optimize.brentq(lambda p, n=n, t=t: log_binom_sf(t, n, p) - math.log(1e-15), 1e-6, 5e-3, xtol=1e-15)
    v.check(f"Lab 23-07.{ident}", lims[t])
v.check("Lab 23-07.g", lims[60] / lims[20])
v.check("Lab 23-07.h", (14 * 60) / (14 * 20))

sys.exit(v.finish())
