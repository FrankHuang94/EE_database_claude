"""Roofline and benchmark arithmetic for Lab 14-15.

- `attainable(peak, bandwidth, intensity)`: the roofline, min(peak, bandwidth x intensity), in FLOP/s.
- `KERNELS`: the FLOP and bytes moved per element (or per output) of the course's kernels, giving their
  arithmetic intensity; `gemm_intensity(n, bytes_per_value)` for an n x n x n product moving each matrix once.
- `MACHINES`: peak FLOP/s and memory bandwidth of the accelerators logged in the research log (R-220, R-222).
- Means: `amean`, `gmean`, `hmean`, and `spec_ratio` (reference time / measured time, times copies).
"""
from __future__ import annotations

import math

MACHINES = {
    "H100 SXM, FP32": (67e12, 3.35e12),                  # R-220
    "H100 SXM, BF16 dense": (1979e12 / 2, 3.35e12),      # R-220 (dense = half the sparse figure)
    "TPU v4, BF16": (275e12, 1.2e12),                     # R-222
    "TPU7x, BF16": (2307e12, 7380e9),                     # R-222
}

# (FLOP, bytes) per element, FP32 unless stated; 'stencil' assumes each input is read once (perfect caching)
KERNELS = {
    "vector add z = x + y": (1, 12),
    "SAXPY y = a x + y": (2, 12),
    "7-point stencil": (8, 8),
    "LLM decode, BF16 weights": (2, 2),
}


def intensity(flop: float, nbytes: float) -> float:
    return flop / nbytes


def gemm_intensity(n: int, bytes_per_value: float = 4) -> float:
    return 2 * n**3 / (3 * n * n * bytes_per_value)


def attainable(peak: float, bandwidth: float, ai: float) -> float:
    return min(peak, bandwidth * ai)


def ridge(peak: float, bandwidth: float) -> float:
    return peak / bandwidth


def amean(xs):
    return sum(xs) / len(xs)


def gmean(xs):
    return math.exp(sum(math.log(x) for x in xs) / len(xs))


def hmean(xs):
    return len(xs) / sum(1 / x for x in xs)


def spec_ratio(ref_time: float, time: float, copies: int = 1) -> float:
    return copies * ref_time / time
