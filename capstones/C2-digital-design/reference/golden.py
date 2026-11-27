#!/usr/bin/env python3
"""Bit-exact golden model of the C2 FIR filter, and the test vectors the self-checking testbench reads.

y[n] = sat16((sum_k h_k x[n-k] + 2^14) >> 15), arithmetic shift, h = [-169, -750, 3170, 14133, 14133, 3170, -750, -169]
(Q1.15; they sum to 32768, so the DC gain is exactly 1). The stimulus has four phases: an impulse, a step, a
worst-case pattern that drives the output into both saturation limits, and seeded random samples, with in_valid
held low on a random quarter of the cycles throughout (the delay line must advance only on valid samples).

Usage: python golden.py   (rewrites stim.hex and expected.hex; the testbench and verify_c2.py read them)
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

H = [-169, -750, 3170, 14133, 14133, 3170, -750, -169]
HERE = Path(__file__).resolve().parent


def sat16(v):
    return max(-32768, min(32767, v))


def fir(samples):
    """Reference filter on the sequence of valid samples (Python integers, so no overflow anywhere)."""
    line = [0] * 8
    out = []
    for x in samples:
        line = [x] + line[:7]
        acc = sum(h * s for h, s in zip(H, line)) + (1 << 14)
        out.append(sat16(acc >> 15))            # Python's >> on negative integers is an arithmetic shift
    return out


def stimulus(seed=2026):
    rng = np.random.default_rng(seed)
    impulse = [32767] + [0] * 11
    step = [16384] * 16
    worst = []                                  # x aligned with sign(h) gives sum |h| * 32767 > 2^30: saturates high
    for hi, lo in ((32767, -32768), (-32768, 32767)):   # aligned with sign(h), then against it
        worst += [hi if h > 0 else lo for h in reversed(H)] * 3
    rand = [int(v) for v in rng.integers(-32768, 32768, 400)]
    samples = impulse + step + worst + rand
    cycles = []                                 # (valid, data) per clock; invalid cycles carry junk data
    for x in samples:
        while rng.random() < 0.25:
            cycles.append((0, int(rng.integers(-32768, 32768))))
        cycles.append((1, x))
    return samples, cycles


def main():
    samples, cycles = stimulus()
    expected = fir(samples)
    (HERE / "stim.hex").write_text("".join(f"{v:01x}{d & 0xffff:04x}\n" for v, d in cycles), encoding="utf-8")
    (HERE / "expected.hex").write_text("".join(f"{y & 0xffff:04x}\n" for y in expected), encoding="utf-8")
    print(f"{len(cycles)} cycles, {len(samples)} samples; outputs at +32767: {expected.count(32767)}, "
          f"at -32768: {expected.count(-32768)}")


if __name__ == "__main__":
    main()
