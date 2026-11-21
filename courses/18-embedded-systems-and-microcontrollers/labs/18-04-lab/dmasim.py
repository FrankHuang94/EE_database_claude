"""Lab 18-04: models of DMA streaming, buffering and bus contention.

- `pingpong_min_block`: smallest block that a CPU can keep up with, from t_proc(N) = a + bN and fill time N/fs;
- `simulate_pingpong`: event simulation of DMA filling two (or more) buffers while the CPU processes completed
  ones with a random service latency; counts overruns (DMA reusing a buffer the CPU has not finished);
- `bus_sim`: cycle-level model of one SRAM port shared by the CPU and a DMA master, with DMA priority or
  round-robin arbitration; returns the CPU's stall fraction, to compare with the estimate p_cpu * rho_dma;
- small helpers: interrupt rates and loads, transfer counts, ring-buffer head from a remaining-count register,
  cache lines touched by a buffer.
"""
from __future__ import annotations

import math

import numpy as np


# ------------------------------------------------------------------ buffering
def pingpong_min_block(fs: float, a: float, b: float, latency: float = 0.0, n_buffers: int = 2) -> float:
    """Smallest N (samples) for which a block can always be processed before its buffer is refilled.

    With n_buffers buffers the CPU has (n_buffers - 1) N / fs after a block completes; it needs the worst service
    latency L plus a + bN. So L + a + bN <= (n_buffers - 1) N / fs, i.e. N >= (a + L) fs / (n_buffers - 1 - b fs).
    """
    room = n_buffers - 1 - b * fs
    if room <= 0:
        return math.inf
    return (a + latency) * fs / room


def simulate_pingpong(fs, n_block, a, b, n_blocks=2000, n_buffers=2, service_latency=0.0, jitter=0.0, seed=0):
    """Return (overruns, worst latency from a sample's arrival to the end of its block's processing).

    Block k is filled during [k N/fs, (k+1) N/fs). Its processing may start at the later of its completion plus a
    service latency (uniform in [service_latency, service_latency + jitter]) and the end of the previous block's
    processing, and takes a + bN. With n_buffers buffers, the DMA reuses block k's buffer at (k + n_buffers) N/fs;
    finishing after that is an overrun.
    """
    rng = np.random.default_rng(seed)
    t_fill = n_block / fs
    t_proc = a + b * n_block
    busy_until = 0.0
    overruns = 0
    worst = 0.0
    for k in range(n_blocks):
        done_fill = (k + 1) * t_fill
        start = max(done_fill + service_latency + jitter * rng.random(), busy_until)
        finish = start + t_proc
        busy_until = finish
        if finish > (k + n_buffers) * t_fill + 1e-15:
            overruns += 1
        worst = max(worst, finish - k * t_fill)
    return overruns, worst


# ------------------------------------------------------------------ bus contention
def bus_sim(n_cycles: int, p_cpu: float, dma_period: float, policy: str = "dma_first", seed: int = 0) -> dict:
    """One shared SRAM port, one access per cycle.

    The CPU wants the port in a cycle with probability p_cpu (an instruction's load or store); if it loses
    arbitration it stalls and retries next cycle. The DMA wants it once every `dma_period` cycles (on average:
    requests are spread evenly) and holds a request until served. `policy`: "dma_first" (DMA wins conflicts) or
    "round_robin" (alternate winners on conflicts). Returns stall fraction of CPU cycles and DMA service stats.
    """
    rng = np.random.default_rng(seed)
    cpu_pending = False
    dma_pending = 0
    next_dma = dma_period
    stalls = 0
    cpu_useful = 0
    dma_served = 0
    dma_wait = 0
    last_winner = "cpu"
    for c in range(n_cycles):
        if c >= next_dma:
            dma_pending += 1
            next_dma += dma_period
        if not cpu_pending:
            cpu_pending = rng.random() < p_cpu
            if not cpu_pending:
                cpu_useful += 1          # a cycle without a memory access always makes progress
                if dma_pending:
                    dma_pending -= 1
                    dma_served += 1
                continue
        # the CPU wants the port this cycle
        if dma_pending and (policy == "dma_first" or last_winner == "cpu"):
            dma_pending -= 1
            dma_served += 1
            stalls += 1
            last_winner = "dma"
        else:
            cpu_pending = False
            cpu_useful += 1
            last_winner = "cpu"
            dma_wait += dma_pending
    return {"stall_fraction": stalls / n_cycles, "dma_served": dma_served, "dma_backlog": dma_pending,
            "cpu_progress": cpu_useful / n_cycles}


def stall_estimate(p_cpu: float, rho_dma: float) -> float:
    """First-order estimate: a CPU access collides with a DMA access with probability rho_dma."""
    return p_cpu * rho_dma


# ------------------------------------------------------------------ helpers
def irq_load(rate_hz: float, cycles: float, f_cpu: float) -> float:
    return rate_hz * cycles / f_cpu


def transfers(n_bytes: int, width_bytes: int) -> int:
    return -(-n_bytes // width_bytes)


def ring_head(size: int, remaining: int) -> int:
    """Write index of a circular DMA whose count register counts down from size to 1 and reloads."""
    return (size - remaining) % size


def ring_unread(head: int, tail: int, size: int) -> int:
    return (head - tail) % size


def cache_lines(addr: int, length: int, line: int = 32) -> int:
    """Number of cache lines a buffer [addr, addr + length) touches."""
    return (addr + length - 1) // line - addr // line + 1
