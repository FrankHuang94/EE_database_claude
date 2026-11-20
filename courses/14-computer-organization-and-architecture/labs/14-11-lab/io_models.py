"""Small analytic models for Lab 14-11: polling and interrupt overheads, DMA, bus and link bandwidth, and the
average hop count of a mesh network-on-chip (computed by enumerating every source-destination pair)."""
from __future__ import annotations

import itertools


def uart_time(nbytes: int, baud: float, bits_per_char: int = 10) -> float:
    """Seconds to send nbytes over a UART (8N1 framing: start + 8 data + stop = 10 bits per character)."""
    return nbytes * bits_per_char / baud


def overhead_fraction(events_per_s: float, cycles_per_event: float, clock_hz: float) -> float:
    """Fraction of a core's cycles spent handling events (polls or interrupts)."""
    return events_per_s * cycles_per_event / clock_hz


def mesh_hops(k: int) -> tuple[float, int]:
    """Average Manhattan distance between uniformly random (source, destination) pairs in a k x k mesh, counting
    pairs with source = destination, and the bisection width in links (one direction)."""
    nodes = list(itertools.product(range(k), repeat=2))
    total = sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a in nodes for b in nodes)
    return total / len(nodes) ** 2, k


def link_bandwidth(gt_per_s: float, lanes: int, efficiency: float = 1.0) -> float:
    """Bytes per second in one direction of a serial link: GT/s x lanes x encoding efficiency / 8."""
    return gt_per_s * 1e9 * lanes * efficiency / 8


def outstanding_needed(bandwidth: float, latency_s: float, bytes_per_txn: int) -> float:
    """Little's law: transactions in flight needed to sustain `bandwidth` bytes/s at a given latency."""
    return bandwidth * latency_s / bytes_per_txn
