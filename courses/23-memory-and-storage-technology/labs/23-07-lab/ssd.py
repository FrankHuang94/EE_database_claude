"""Models for chapter 23-07: SSD controllers and storage systems.

Closed forms for the chapter's examples: host-interface and NAND-channel bandwidth, the flash translation layer's
mapping-table size, write amplification of FIFO (LRU) garbage collection under uniform random writes, drive
endurance, the binomial failure probability of a t-error-correcting code, the binary symmetric channel's capacity,
Little's law for queue depth, and power-loss-protection capacitance; plus a small page-mapped FTL simulator with
FIFO or greedy garbage collection. The verify script recomputes the published numbers by other routes. SI units
unless a name says otherwise.
"""
from __future__ import annotations

import math
import random

from scipy import special, stats


# ---------------------------------------------------------------- interfaces
def pcie_bandwidth(gt_per_s: float, lanes: int, encoding: float = 128 / 130) -> float:
    """Bytes per second in one direction: transfers/s x lanes x encoding efficiency / 8."""
    return gt_per_s * lanes * encoding / 8


def channel_bandwidth(channels: int, mt_per_s: float, width_bits: int = 8) -> float:
    return channels * mt_per_s * width_bits / 8


# ---------------------------------------------------------------- FTL
def map_table_bytes(capacity: float, iu: float = 4096, entry_bytes: int = 4) -> float:
    """Mapping-table size for a page-mapped FTL: one entry per indirection unit."""
    return capacity / iu * entry_bytes


def max_capacity(entry_bits: int, iu: float = 4096) -> float:
    """Largest capacity an entry of entry_bits can address at indirection unit iu (bytes)."""
    return 2 ** entry_bits * iu


# ---------------------------------------------------------------- write amplification
def wa_fifo(alpha: float) -> float:
    """Write amplification of FIFO (LRU) cleaning under uniform random writes, alpha = physical/user capacity.

    The victim block's surviving fraction u solves u = exp(-alpha (1 - u)); A = 1/(1 - u)
    = alpha / (alpha + W(-alpha e^-alpha)) (Desnoyers 2012).
    """
    w = special.lambertw(-alpha * math.exp(-alpha), 0).real
    return alpha / (alpha + w)


def alpha_from_op(op: float) -> float:
    """Physical/user ratio for over-provisioning defined relative to user capacity."""
    return 1 + op


def alpha_from_spare_factor(sf: float) -> float:
    """Physical/user ratio for a spare factor defined relative to physical capacity, Sf = (T - U)/T."""
    return 1 / (1 - sf)


# ---------------------------------------------------------------- endurance
def host_writes_tb(user_tb: float, raw_tb: float, pe: float, waf: float) -> float:
    """Host terabytes a drive absorbs: NAND writes (raw capacity x cycles) divided by write amplification."""
    return raw_tb * pe / waf


# ---------------------------------------------------------------- ECC
def codeword_failure(n_bits: int, t: int, rber: float) -> float:
    """Probability that a codeword of n_bits sees more than t bit errors (binomial tail)."""
    return float(stats.binom.sf(t, n_bits, rber))


def bch_parity_bits(t: int, m: int) -> int:
    """Parity bits of a binary BCH code over GF(2^m) correcting t errors (at most m t)."""
    return m * t


def bsc_capacity(p: float) -> float:
    """Capacity of a binary symmetric channel, 1 - H(p) bits per bit."""
    return 1 + p * math.log2(p) + (1 - p) * math.log2(1 - p)


# ---------------------------------------------------------------- queues and power
def queue_depth(iops: float, latency: float) -> float:
    """Little's law: outstanding commands = throughput x latency."""
    return iops * latency


def plp_capacitance(power: float, hold_time: float, v_high: float, v_low: float, eff: float = 1.0) -> float:
    """Capacitance that supplies power for hold_time while discharging from v_high to v_low through a converter."""
    return 2 * power * hold_time / eff / (v_high ** 2 - v_low ** 2)


# ---------------------------------------------------------------- a small FTL simulator
def simulate_ftl(user_pages: int, op: float, pages_per_block: int = 64, policy: str = "greedy",
                 writes_per_page: float = 10.0, hot_fraction: float | None = None, hot_traffic: float = 0.9,
                 separate_streams: bool = False, seed: int = 1) -> float:
    """Write amplification of a page-mapped FTL under random writes, measured after a warm-up pass.

    policy: "greedy" (fewest valid pages) or "fifo" (oldest block). With hot_fraction set, hot_traffic of the
    writes go to that fraction of the logical space; separate_streams writes hot and cold data to different
    open blocks, as a host using Flexible Data Placement could.
    """
    rng = random.Random(seed)
    nb = math.ceil(user_pages * (1 + op) / pages_per_block)
    owner = [[-1] * pages_per_block for _ in range(nb)]  # logical page in each slot, -1 if invalid
    valid = [0] * nb
    where = [-1] * user_pages  # physical slot index (block * Np + page) of each logical page
    free = list(range(nb))
    order: list[int] = []  # full blocks in fill order (for FIFO)
    streams = 2 if separate_streams else 1
    open_blk = [free.pop() for _ in range(streams)]
    fill = [0] * streams
    hot_pages = int(user_pages * hot_fraction) if hot_fraction else 0
    counters = {"host": 0, "nand": 0}

    def place(lpn: int, s: int) -> None:
        b = open_blk[s]
        owner[b][fill[s]] = lpn
        where[lpn] = b * pages_per_block + fill[s]
        valid[b] += 1
        fill[s] += 1
        counters["nand"] += 1
        if fill[s] == pages_per_block:
            order.append(b)
            open_blk[s] = None  # type: ignore[call-overload]
            fill[s] = 0

    def collect() -> None:
        if policy == "fifo":
            victim = order.pop(0)
        else:
            victim = min(order, key=valid.__getitem__)
            order.remove(victim)
        moved = [lpn for lpn in owner[victim] if lpn >= 0]
        owner[victim] = [-1] * pages_per_block
        valid[victim] = 0
        free.append(victim)
        for lpn in moved:
            s = 1 if (separate_streams and lpn >= hot_pages) else 0
            ensure_open(s)
            place(lpn, s)

    def ensure_open(s: int) -> None:
        while open_blk[s] is None:
            if not free:
                collect()
                continue
            open_blk[s] = free.pop(0)

    def host_write(lpn: int) -> None:
        old = where[lpn]
        if old >= 0:
            b, p = divmod(old, pages_per_block)
            owner[b][p] = -1
            valid[b] -= 1
        s = 1 if (separate_streams and lpn >= hot_pages) else 0
        ensure_open(s)
        place(lpn, s)
        counters["host"] += 1

    def pick() -> int:
        if hot_fraction:
            if rng.random() < hot_traffic:
                return rng.randrange(hot_pages)
            return rng.randrange(hot_pages, user_pages)
        return rng.randrange(user_pages)

    for lpn in range(user_pages):  # fill the drive once, sequentially
        host_write(lpn)
    for _ in range(int(2 * user_pages)):  # warm up to steady state
        host_write(pick())
    counters["host"] = counters["nand"] = 0
    for _ in range(int(writes_per_page * user_pages)):
        host_write(pick())
    return counters["nand"] / counters["host"]
