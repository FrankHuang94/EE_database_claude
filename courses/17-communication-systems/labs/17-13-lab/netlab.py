"""Computer-networks toolkit for the 17-13 lab.

- protocol overhead: header sizes and wire efficiency of Ethernet frames;
- IPv4/IPv6 addressing with the standard-library ipaddress module: subnetting, aggregation, membership;
- routing: Dijkstra (link state) and Bellman-Ford (distance vector), longest-prefix-match forwarding;
- TCP: window-limited throughput, bandwidth-delay product, window scaling, slow start, the AIMD sawtooth
  and its square-root loss formula, and the RFC 6298 retransmission-timeout estimator;
- queueing: M/M/1 delay with a discrete-event simulation;
- security arithmetic: brute-force key search time and birthday bounds; a first-match firewall.
"""
from __future__ import annotations

import heapq
import ipaddress
import math

import numpy as np

# header sizes in bytes (RFC 791, 768, 8200, 9293; Ethernet per RFC 894 and IEEE 802.3)
ETH_HEADER, ETH_FCS, PREAMBLE_SFD, IFG = 14, 4, 8, 12
IPV4, IPV6, TCP, UDP = 20, 40, 20, 8
ETH_MIN_PAYLOAD, ETH_MAX_PAYLOAD = 46, 1500


# ------------------------------------------------------------------ overhead
def wire_bytes(l3_packet):
    """Bytes on the wire for one Ethernet frame carrying an L3 packet (padding, preamble/SFD and IFG included)."""
    payload = max(l3_packet, ETH_MIN_PAYLOAD)
    return PREAMBLE_SFD + ETH_HEADER + payload + ETH_FCS + IFG


def efficiency(app_bytes, l4=TCP, l3=IPV4):
    return app_bytes / wire_bytes(app_bytes + l4 + l3)


def max_frame_rate(bit_rate, l3_packet=ETH_MIN_PAYLOAD):
    return bit_rate / (8 * wire_bytes(l3_packet))


def full_mesh_links(n):
    return n * (n - 1) // 2


# ------------------------------------------------------------------ addressing
def subnet(network, new_prefix):
    return list(ipaddress.ip_network(network).subnets(new_prefix=new_prefix))


def usable_hosts(prefix_len, bits=32):
    n = 2 ** (bits - prefix_len)
    return n - 2 if bits == 32 and prefix_len <= 30 else n


def prefix_for_hosts(hosts, bits=32):
    """Longest IPv4 prefix whose subnets hold at least `hosts` usable addresses."""
    p = bits
    while usable_hosts(p, bits) < hosts:
        p -= 1
    return p


def aggregate(networks):
    return list(ipaddress.collapse_addresses(ipaddress.ip_network(n) for n in networks))


def longest_prefix_match(table, address):
    """table: {prefix string: next hop}; returns the next hop of the most specific matching prefix."""
    addr = ipaddress.ip_address(address)
    best, hop = -1, None
    for pfx, nh in table.items():
        net = ipaddress.ip_network(pfx)
        if addr in net and net.prefixlen > best:
            best, hop = net.prefixlen, nh
    return hop


# ------------------------------------------------------------------ routing
def dijkstra(graph, src):
    """graph: {node: {neighbour: cost}} (undirected entries in both directions). Returns (dist, prev)."""
    dist = {v: math.inf for v in graph}
    prev = {v: None for v in graph}
    dist[src] = 0
    pq = [(0, src)]
    done = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        for w, c in graph[u].items():
            if d + c < dist[w]:
                dist[w] = d + c
                prev[w] = u
                heapq.heappush(pq, (dist[w], w))
    return dist, prev


def path(prev, dst):
    out = []
    while dst is not None:
        out.append(dst)
        dst = prev[dst]
    return out[::-1]


def bellman_ford(graph, src, max_rounds=None):
    """Synchronous distance-vector iterations; returns (dist, rounds until no change)."""
    dist = {v: math.inf for v in graph}
    dist[src] = 0
    rounds = 0
    for _ in range(max_rounds or len(graph)):
        new = dict(dist)
        for u in graph:
            for w, c in graph[u].items():
                if dist[w] + c < new[u]:
                    new[u] = dist[w] + c
        rounds += 1
        if new == dist:
            return dist, rounds - 1
        dist = new
    return dist, rounds


def dv_after_failure(graph, failed, dest, infinity=16, split_horizon=False, max_rounds=100):
    """Distance-vector routing to `dest` after the link `failed` = (u, w) goes down.

    Starts from the converged distances and next hops of the intact graph, removes the link, then runs synchronous
    rounds: every router recomputes d = min over neighbours (link cost + neighbour's last advertisement), capped at
    `infinity`. With `split_horizon`, a router does not advertise its route back to the neighbour it routes through.
    Returns (rounds until no change, final distances).
    """
    dist, _ = bellman_ford(graph, dest)
    g = {u: dict(nb) for u, nb in graph.items()}
    a, b = failed
    g[a].pop(b, None)
    g[b].pop(a, None)
    d = {u: min(dist[u], infinity) for u in g}
    nxt = {u: None for u in g}
    for u in g:
        if u != dest:
            nxt[u] = min(graph[u], key=lambda v: graph[u][v] + dist[v])
    for rnd in range(1, max_rounds + 1):
        new, new_nxt = dict(d), dict(nxt)
        for u in g:
            if u == dest:
                continue
            best, hop = infinity, None
            for v, c in g[u].items():
                adv = d[v]
                if split_horizon and nxt[v] == u:
                    adv = infinity
                if c + adv < best:
                    best, hop = c + adv, v
            new[u], new_nxt[u] = min(best, infinity), hop
        if new == d:
            return rnd - 1, d
        d, nxt = new, new_nxt
    return max_rounds, d


# ------------------------------------------------------------------ TCP
def window_throughput(window_bytes, rtt):
    return 8 * window_bytes / rtt


def bdp_bytes(rate_bps, rtt):
    return rate_bps * rtt / 8


def window_shift_needed(window_bytes):
    """Smallest RFC 7323 shift count s with 65535 * 2^s >= window (s <= 14)."""
    s = 0
    while 65535 * 2**s < window_bytes:
        s += 1
    return s


def initial_window(smss):
    """RFC 5681 initial window in segments."""
    if smss > 2190:
        return 2
    if smss > 1095:
        return 3
    return 4


def slow_start_rtts(target_segments, iw):
    """RTTs of doubling (cwnd = iw, 2 iw, 4 iw, ...) until cwnd >= target."""
    return max(0, math.ceil(math.log2(target_segments / iw)))


def mathis_throughput(mss_bytes, rtt, p):
    """Steady AIMD sawtooth: (MSS/RTT) sqrt(3 / (2p)) bits per second."""
    return 8 * mss_bytes / rtt * math.sqrt(3 / (2 * p))


def simulate_aimd(p, rounds, rng, w0=10.0):
    """Per-RTT AIMD: each of the floor(W) packets is lost independently with probability p; on any loss halve W,
    otherwise add 1. Returns the mean window (segments per RTT)."""
    w = w0
    total = 0.0
    for _ in range(rounds):
        n = int(w)
        total += w
        if rng.random() < 1 - (1 - p) ** n:
            w = max(1.0, w / 2)
        else:
            w += 1
    return total / rounds


def rto_sequence(samples, g=0.0, alpha=1 / 8, beta=1 / 4, k=4, min_rto=1.0):
    """RFC 6298: returns [(SRTT, RTTVAR, raw RTO, clamped RTO)] after each sample (seconds)."""
    out = []
    srtt = rttvar = None
    for r in samples:
        if srtt is None:
            srtt, rttvar = r, r / 2
        else:
            rttvar = (1 - beta) * rttvar + beta * abs(srtt - r)
            srtt = (1 - alpha) * srtt + alpha * r
        raw = srtt + max(g, k * rttvar)
        out.append((srtt, rttvar, raw, max(raw, min_rto)))
    return out


# ------------------------------------------------------------------ queueing
def mm1_delay(lam, mu):
    """Mean time in an M/M/1 system (queue + service)."""
    return 1 / (mu - lam)


def simulate_mm1(lam, mu, n, rng):
    arr = np.cumsum(rng.exponential(1 / lam, n))
    svc = rng.exponential(1 / mu, n)
    dep = np.empty(n)
    t = 0.0
    for i in range(n):
        t = max(t, arr[i]) + svc[i]
        dep[i] = t
    return float(np.mean(dep - arr))


# ------------------------------------------------------------------ security arithmetic
def brute_force_years(key_bits, rate_per_s, fraction=0.5):
    """Expected time to find a key by exhaustive search (half the space on average)."""
    return fraction * 2.0**key_bits / rate_per_s / (365.25 * 24 * 3600)


def birthday_trials(bits, prob=0.5):
    """Hashes needed for a collision with probability prob: sqrt(2 * 2^bits * ln(1/(1 - prob)))."""
    return math.sqrt(2 * 2.0**bits * math.log(1 / (1 - prob)))


def firewall(rules, packet):
    """First-match rule list: rules are (action, field dict); packet a dict. Default deny."""
    for action, cond in rules:
        if all(packet.get(k) == v or v == "*" for k, v in cond.items()):
            return action
    return "deny"
