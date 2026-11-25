"""Interconnect-standard arithmetic for chapter 24-05.

PCIe generations (rate, encoding efficiency), bandwidth per direction for any width, TLP efficiency;
an event-driven credit-based flow-control simulator; Ethernet lane rates; switch radix and fabric sizes;
replay-buffer sizing.
"""
from __future__ import annotations

import heapq

PCIE = {  # generation: (GT/s, encoding efficiency for TLP-carrying bits)
    "1.0": (2.5, 8 / 10), "2.0": (5.0, 8 / 10), "3.0": (8.0, 128 / 130), "4.0": (16.0, 128 / 130),
    "5.0": (32.0, 128 / 130), "6.0": (64.0, 236 / 256), "7.0": (128.0, 236 / 256),
}


def pcie_bw(gen: str, lanes: int = 1) -> float:
    """Bandwidth per direction after encoding, GB/s."""
    rate, eff = PCIE[gen]
    return lanes * rate * eff / 8


def pcie_raw_bidir(rate_gts: float, lanes: int = 16) -> float:
    """PCI-SIG-style headline: raw rate, both directions, GB/s."""
    return rate_gts * lanes * 2 / 8


def tlp_efficiency(payload: int, overhead: int = 24) -> float:
    return payload / (payload + overhead)


def simulate_credits(bw_gbps: float, buffer_bytes: int, rtt_ns: float, pkt: int = 256, t_end_ns: float = 200_000):
    """Event-driven credit flow control: a packet may start only when a credit is free and the link is idle;
    its credit returns rtt_ns after it starts. Returns delivered throughput in GB/s over the last half."""
    credits = buffer_bytes // pkt
    t_pkt = pkt / bw_gbps  # ns per packet (GB/s = bytes/ns)
    returns: list[float] = []
    t = 0.0
    sent_times = []
    while t < t_end_ns:
        while returns and returns[0] <= t:
            heapq.heappop(returns)
            credits += 1
        if credits > 0:
            credits -= 1
            sent_times.append(t)
            heapq.heappush(returns, t + rtt_ns)
            t += t_pkt
        else:
            t = returns[0]
    half = t_end_ns / 2
    n = sum(1 for s in sent_times if s >= half)
    return n * pkt / (t_end_ns - half)


def bdp_bytes(bw_gbps: float, rtt_ns: float) -> float:
    return bw_gbps * rtt_ns


def ethernet_lane_rate(mac_per_lane_gbps: float) -> float:
    """MAC rate per lane x 257/256 transcoding x 544/514 RS FEC."""
    return mac_per_lane_gbps * 257 / 256 * 544 / 514


def radix(switch_tbps: float, port_gbps: float) -> int:
    return int(round(switch_tbps * 1000 / port_gbps))


def two_tier_hosts(k: int) -> int:
    return k * k // 2


def three_tier_hosts(k: int) -> int:
    return k ** 3 // 4


def replay_buffer_bytes(rate_gbps: float, rtt_us: float) -> float:
    return rate_gbps * 1e9 * rtt_us * 1e-6 / 8
