"""Models for chapter 23-01: the memory hierarchy and the memory wall.

Every function is a closed form from the chapter; the verify script recomputes the published numbers by other
routes (sampled waveforms, numerical integration, root finding). Units are SI unless a name says otherwise.
"""
from __future__ import annotations

from dataclasses import dataclass

# Horowitz, ISSCC 2014, Fig. 1.1.9 (45 nm, 0.9 V), as reproduced in MIT 6.5930 slides; energies in pJ.
HOROWITZ_45NM_PJ = {
    "8b add": 0.03, "16b add": 0.05, "32b add": 0.1, "16b FP add": 0.4, "32b FP add": 0.9,
    "8b mult": 0.2, "32b mult": 3.1, "16b FP mult": 1.1, "32b FP mult": 3.7,
    "32b SRAM read (8 KB)": 5.0, "32b DRAM read": 640.0,
}


def switching_energy(c: float, v: float) -> float:
    """Energy drawn from the supply when a capacitance c charges from 0 to v (J); half is stored, half dissipated."""
    return c * v * v


def wire_energy_per_bit(c_per_m: float, length: float, v: float, p01: float = 0.25) -> float:
    """Average energy per bit sent down a full-swing wire (J/bit).

    p01 is the probability that a bit makes a 0 -> 1 transition (1/4 for random data, 1/2 for alternating data);
    only those transitions draw energy from the supply.
    """
    return p01 * switching_energy(c_per_m * length, v)


def link_power(bandwidth_bytes: float, energy_per_bit: float) -> float:
    """Power (W) of moving data at bandwidth_bytes (B/s) with energy_per_bit (J/bit)."""
    return 8 * bandwidth_bytes * energy_per_bit


def max_bandwidth(power: float, energy_per_bit: float) -> float:
    """Largest bandwidth (B/s) a power budget (W) allows at energy_per_bit (J/bit)."""
    return power / energy_per_bit / 8


def all_in_energy_per_bit(power: float, bandwidth_bytes: float) -> float:
    """Measured memory power divided by delivered bits per second (J/bit)."""
    return power / (8 * bandwidth_bytes)


def interface_bandwidth(width_bits: int, rate_per_pin: float) -> float:
    """Peak bandwidth (B/s) of a parallel interface of width_bits pins at rate_per_pin (b/s)."""
    return width_bits * rate_per_pin / 8


def per_pin_rate(bandwidth_bytes: float, width_bits: int) -> float:
    """Pin rate (b/s) that a parallel interface needs for bandwidth_bytes (B/s)."""
    return 8 * bandwidth_bytes / width_bits


def bytes_in_flight(bandwidth_bytes: float, latency: float) -> float:
    """Little's law: data that must be outstanding to sustain bandwidth_bytes at a given latency (B)."""
    return bandwidth_bytes * latency


def ridge_point(peak_flops: float, bandwidth_bytes: float) -> float:
    """Arithmetic intensity (FLOP/B) at which peak compute equals bandwidth times intensity."""
    return peak_flops / bandwidth_bytes


def growth(rate_per_2yr: float, years: float) -> float:
    """Total growth after `years` at a constant factor per two years."""
    return rate_per_2yr ** (years / 2)


@dataclass
class Transformer:
    """A dense decoder-only transformer, described only by what decode traffic depends on."""
    params: float          # parameter count
    weight_bytes: float    # bytes per weight
    layers: int
    q_heads: int
    kv_heads: int
    head_dim: int
    kv_bytes: float        # bytes per stored K or V element

    @property
    def d_model(self) -> int:
        return self.q_heads * self.head_dim

    @property
    def weights(self) -> float:
        return self.params * self.weight_bytes

    def kv_per_token(self) -> float:
        """KV-cache bytes added per token of context: K and V for every layer and KV head."""
        return 2 * self.layers * self.kv_heads * self.head_dim * self.kv_bytes

    def kv_per_sequence(self, context: int) -> float:
        return self.kv_per_token() * context

    def decode_flops(self, context: int, batch: int) -> float:
        """FLOPs of one decode step: 2 per weight per sequence plus attention (QK^T and AV) over the context."""
        return batch * (2 * self.params + 4 * self.layers * self.d_model * context)

    def decode_bytes(self, context: int, batch: int) -> float:
        """Bytes read in one decode step: every weight once, plus each sequence's whole KV cache."""
        return self.weights + batch * self.kv_per_sequence(context)

    def intensity(self, context: int, batch: int) -> float:
        return self.decode_flops(context, batch) / self.decode_bytes(context, batch)

    def intensity_limit(self, context: int) -> float:
        """Intensity as batch -> infinity: the KV cache, not the weights, sets it."""
        return (2 * self.params + 4 * self.layers * self.d_model * context) / self.kv_per_sequence(context)

    def attention_intensity(self) -> float:
        """FLOP per KV byte of decode attention: 2 (q_heads/kv_heads) / kv_bytes, independent of batch and context."""
        return 4 * self.layers * self.d_model / self.kv_per_token()

    def max_batch(self, capacity: float, context: int) -> int:
        """Sequences whose KV caches fit beside the weights (ignores activations and fragmentation)."""
        return int((capacity - self.weights) // self.kv_per_sequence(context))

    def step_time(self, context: int, batch: int, bandwidth_bytes: float, peak_flops: float) -> float:
        """Roofline lower bound on one decode step (s): the slower of memory traffic and arithmetic."""
        return max(self.decode_bytes(context, batch) / bandwidth_bytes,
                   self.decode_flops(context, batch) / peak_flops)

    def tokens_per_second(self, context: int, batch: int, bandwidth_bytes: float, peak_flops: float) -> float:
        return batch / self.step_time(context, batch, bandwidth_bytes, peak_flops)

    def memory_energy_per_token(self, context: int, batch: int, energy_per_bit: float) -> float:
        """Memory-traffic energy per generated token (J)."""
        return 8 * self.decode_bytes(context, batch) * energy_per_bit / batch
