"""Microcontroller-architecture toolkit for the 18-01 lab.

- the Armv7-M / Armv8-M fixed memory map: region lookup, peripheral register addresses, bit-band aliases;
- flash wait states from the access time, and the frequency bands they imply;
- an instruction-fetch simulator: a flash of a given line width and wait states feeding a core that
  executes one instruction per cycle, with a one-line prefetch buffer and an optional instruction cache;
- the analytic effective-CPI model the simulator checks;
- PLL configuration search under input, VCO and divider constraints;
- energy per task and the best clock for a duty-cycled workload;
- weighted-score MCU selection.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

# ------------------------------------------------------------------ memory map (Armv7-M / Armv8-M architecture)
REGIONS = [
    (0x0000_0000, 0x1FFF_FFFF, "Code"),
    (0x2000_0000, 0x3FFF_FFFF, "SRAM"),
    (0x4000_0000, 0x5FFF_FFFF, "Peripheral"),
    (0x6000_0000, 0x9FFF_FFFF, "External RAM"),
    (0xA000_0000, 0xDFFF_FFFF, "External device"),
    (0xE000_0000, 0xE00F_FFFF, "Private peripheral bus"),
    (0xE010_0000, 0xFFFF_FFFF, "Vendor system"),
]
BITBAND = {"SRAM": (0x2000_0000, 0x2200_0000), "Peripheral": (0x4000_0000, 0x4200_0000)}  # (region base, alias base)
BITBAND_SIZE = 0x10_0000  # 1 MB bit-band region in each


def region(addr: int) -> str:
    for lo, hi, name in REGIONS:
        if lo <= addr <= hi:
            return name
    raise ValueError(f"address {addr:#x} outside 32-bit space")


def region_size(name: str) -> int:
    for lo, hi, n in REGIONS:
        if n == name:
            return hi - lo + 1
    raise KeyError(name)


def reg_addr(base: int, offset: int) -> int:
    return base + offset


def bitband_alias(addr: int, bit: int) -> int:
    """Armv7-M bit-band alias word for bit `bit` of the byte at `addr` (word-aligned addresses use bit 0..31)."""
    for name, (base, alias) in BITBAND.items():
        if base <= addr < base + BITBAND_SIZE:
            byte_offset = (addr - base) + bit // 8
            return alias + byte_offset * 32 + (bit % 8) * 4
    raise ValueError("address outside the bit-band regions")


# ------------------------------------------------------------------ flash wait states
def wait_states(f_hz: float, t_access_s: float) -> int:
    """Smallest WS with (WS + 1) / f >= t_access: the read must complete within WS + 1 clock cycles."""
    return max(0, math.ceil(f_hz * t_access_s - 1e-9) - 1)


def max_freq(ws: int, t_access_s: float) -> float:
    return (ws + 1) / t_access_s


# ------------------------------------------------------------------ fetch simulation
@dataclass
class FetchResult:
    cycles: int
    instructions: int
    line_fetches: int
    cpi: float


def make_program(n_instr, branch_every, taken_frac, size_mix, rng, aligned=True, code_bytes=64 * 1024, line_bytes=16):
    """Synthetic instruction stream: list of (pc, size, taken).

    Every `branch_every`-th instruction is a branch, taken with probability `taken_frac`, to a random address
    in `code_bytes`: line-aligned if `aligned` (as compilers align loop heads), else any 2-byte boundary.
    `size_mix` is the probability that an instruction is 32-bit (Thumb-2 mixes 16- and 32-bit encodings).
    """
    prog = []
    pc = 0
    for i in range(n_instr):
        size = 4 if rng.random() < size_mix else 2
        taken = (i + 1) % branch_every == 0 and rng.random() < taken_frac
        prog.append((pc, size, taken))
        if taken:
            unit = line_bytes if aligned else 2
            pc = int(rng.integers(0, code_bytes // unit)) * unit
        else:
            pc += size
    return prog


def simulate_fetch(prog, ws, line_bytes=16, cache_lines=0, prefetch=True):
    """Cycle count for a core that issues one instruction per cycle when its bytes are in the line buffer.

    Timing is relative to a zero-wait-state memory, whose one-cycle access the pipeline already hides: a line
    read that starts at cycle b can feed the core from cycle b + ws, and it occupies the flash until
    b + ws + 1. With `prefetch`, the next sequential line is read as soon as the flash is free; a
    non-sequential (branch) request aborts that prefetch. An optional fully associative LRU instruction cache
    of `cache_lines` lines serves hits with no stall.
    """
    t = 0
    flash_free = 0
    pending = None  # (line, available_time) of the speculative prefetch
    buffer_line = None
    cache = []
    fetches = 0

    def start_read(line, when):
        nonlocal flash_free, fetches
        b = max(when, flash_free)
        flash_free = b + ws + 1
        fetches += 1
        return b + ws

    for pc, size, _taken in prog:
        lines = sorted({pc // line_bytes, (pc + size - 1) // line_bytes})
        for line in lines:
            if line == buffer_line:
                continue
            if cache_lines and line in cache:
                cache.remove(line)
                cache.append(line)
                buffer_line = line
            else:
                if pending is not None and pending[0] == line:
                    avail = pending[1]
                else:
                    flash_free = min(flash_free, t)  # abort a useless prefetch
                    avail = start_read(line, t)
                pending = None
                t = max(t, avail)
                buffer_line = line
                if cache_lines:
                    cache.append(line)
                    if len(cache) > cache_lines:
                        cache.pop(0)
            if prefetch and (pending is None or pending[0] != line + 1):
                nxt = line + 1
                if not (cache_lines and nxt in cache):
                    pending = (nxt, start_read(nxt, t))
        t += 1
    return FetchResult(t, len(prog), fetches, t / len(prog))


def cpi_analytic(ws, line_bytes, avg_instr_bytes, taken_per_instr, miss_rate=1.0):
    """Effective CPI: sequential supply limit plus a refill penalty of WS cycles per taken branch that misses.

    Sequential code runs at max(1, (ws + 1) * s / L) cycles per instruction (one line every ws + 1 cycles,
    L / s instructions per line); each taken branch whose target is not buffered or cached waits ws extra cycles.
    """
    seq = max(1.0, (ws + 1) * avg_instr_bytes / line_bytes)
    return seq + taken_per_instr * miss_rate * ws


# ------------------------------------------------------------------ PLL
def pll_search(f_in, f_target, m_range=range(2, 64), n_range=range(50, 433), p_set=(2, 4, 6, 8),
               pfd=(1e6, 2e6), vco=(100e6, 432e6), f_aux=None, q_range=range(2, 16)):
    """All (M, N, P, Q, f_out, f_aux_out) meeting f_out = f_in N / (M P) exactly, within the PFD and VCO ranges,
    and, if f_aux is given, VCO / Q = f_aux exactly."""
    out = []
    for m in m_range:
        fp = f_in / m
        if not pfd[0] <= fp <= pfd[1]:
            continue
        for n in n_range:
            fv = fp * n
            if not vco[0] <= fv <= vco[1]:
                continue
            for p in p_set:
                if abs(fv / p - f_target) > 1e-3:
                    continue
                if f_aux is None:
                    out.append((m, n, p, None, fv / p, None))
                else:
                    for q in q_range:
                        if abs(fv / q - f_aux) < 1e-3:
                            out.append((m, n, p, q, fv / p, fv / q))
    return out


# ------------------------------------------------------------------ energy
def task_energy(f_hz, cycles_at_f, v, i_static_a, i_per_hz_a):
    """Energy (J) and time (s) to run a task of `cycles_at_f` cycles at clock f: I = I_static + k f."""
    t = cycles_at_f / f_hz
    return v * (i_static_a + i_per_hz_a * f_hz) * t, t


def duty_cycle_energy(f_hz, cycles_at_f, period_s, v, i_static_a, i_per_hz_a, i_sleep_a):
    e_act, t_act = task_energy(f_hz, cycles_at_f, v, i_static_a, i_per_hz_a)
    if t_act > period_s:
        return math.inf
    return e_act + v * i_sleep_a * (period_s - t_act)


# ------------------------------------------------------------------ selection
def weighted_scores(weights: dict, scores: dict) -> dict:
    """scores: {candidate: {criterion: score}}; weights: {criterion: weight}. Returns normalized weighted sums."""
    wsum = sum(weights.values())
    return {c: sum(weights[k] * s[k] for k in weights) / wsum for c, s in scores.items()}


def gate(requirements: dict, specs: dict) -> list:
    """Candidates meeting every hard requirement {spec: minimum}."""
    return [c for c, s in specs.items() if all(s[k] >= v for k, v in requirements.items())]


if __name__ == "__main__":
    rng = np.random.default_rng(1)
    for aligned, mix in ((True, 0.0), (True, 0.3), (False, 0.3)):
        prog = make_program(200_000, 5, 0.6, mix, rng, aligned=aligned)
        s = 2 + 2 * mix
        for ws in (0, 1, 2, 5, 7):
            r = simulate_fetch(prog, ws)
            print(aligned, mix, ws, round(r.cpi, 4), round(cpi_analytic(ws, 16, s, 0.12), 4))
