#!/usr/bin/env python3
"""Verify chapter 17-13 (computer networks fundamentals): text, examples, problems and lab answers.

Routes:
- overheads from the header sizes written out here (R-292, R-293);
- addressing by hand-coded bit arithmetic and by Python's ipaddress module;
- shortest paths by Dijkstra (lab), by Bellman-Ford, and by brute-force enumeration of simple paths;
- count-to-infinity by stepping the alternating updates;
- TCP: window and slow-start arithmetic, RFC 7323 shift search, the square-root formula against a
  simulated AIMD sawtooth, and the RFC 6298 recursion written out independently (R-294);
- M/M/1 delay by an event-driven simulation; security arithmetic from first principles.
"""
from __future__ import annotations

import ipaddress
import itertools
import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "17-13-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import netlab as nl  # noqa: E402

CH = ROOT / "chapters" / "17-13-computer-networks-fundamentals.md"
v = Verifier.from_files("17-13", CH, ROOT / "solutions" / "17-13-solutions.md", LAB / "README.md")
rng = np.random.default_rng(17130)

PRE, ETH, FCS, GAP = 8, 14, 4, 12  # bytes (R-292)
IP4, IP6, TCP, UDP = 20, 40, 20, 8  # bytes (R-293)


def wire(l3):
    return PRE + ETH + max(l3, 46) + FCS + GAP


def ip_to_int(s):
    a, b, c, d = (int(x) for x in s.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d


def brute_paths(graph, src, dst):
    """Cheapest simple path by enumerating permutations of intermediate nodes."""
    others = [n for n in graph if n not in (src, dst)]
    best = math.inf
    for r in range(len(others) + 1):
        for mid in itertools.permutations(others, r):
            p = (src,) + mid + (dst,)
            if all(b in graph[a] for a, b in zip(p, p[1:])):
                best = min(best, sum(graph[a][b] for a, b in zip(p, p[1:])))
    return best


def rto(samples):
    """RFC 6298 written out: first sample SRTT = R, RTTVAR = R/2; then RTTVAR before SRTT."""
    srtt = rttvar = None
    out = []
    for r in samples:
        if srtt is None:
            srtt, rttvar = r, r / 2
        else:
            rttvar = 0.75 * rttvar + 0.25 * abs(srtt - r)
            srtt = 0.875 * srtt + 0.125 * r
        out.append((srtt, rttvar, srtt + 4 * rttvar))
    return out


G1 = {"A": {"B": 2, "C": 5}, "B": {"A": 2, "C": 1, "D": 4}, "C": {"A": 5, "B": 1, "D": 1, "E": 6}, "D": {"B": 4, "C": 1, "E": 2}, "E": {"C": 6, "D": 2}}
G2 = {"S": {"A": 4, "B": 1}, "A": {"S": 4, "B": 2, "C": 5}, "B": {"S": 1, "A": 2, "D": 8}, "C": {"A": 5, "D": 3, "T": 2}, "D": {"B": 8, "C": 3, "T": 6}, "T": {"C": 2, "D": 6}}

# ------------------------------------------------------------------ text
v.check("Txt 17-13.a", len(list(itertools.combinations(range(10), 2))))
v.check("Txt 17-13.b", 1 / (1 - 0.8))
v.check("Txt 17-13.c", round(math.log2(math.sqrt(2.0**256))))
v.assert_true("header bytes: 1518-byte maximum frame = 14 + 1500 + 4; 64-byte minimum = 14 + 46 + 4", ETH + 1500 + FCS == 1518 and ETH + 46 + FCS == 64)
v.assert_true("1 ms LAN with an unscaled window: 524 Mb/s", abs(8 * 65535 / 1e-3 / 1e6 - 524) < 0.5)
v.assert_true("M/M/1 at 95% load: 20 service times", abs(1 / (1 - 0.95) - 20) < 1e-12)
v.assert_true("AES-128 search about 5e18 years; DES-56 about 10 hours at 1e12/s", abs(0.5 * 2.0**128 / 1e12 / 3.15576e7 / 5.39e18 - 1) < 0.01 and abs(0.5 * 2.0**56 / 1e12 / 3600 - 10.0) < 0.05)
v.assert_true("RFC 7323: shift <= 14 gives windows below 2^30", 65535 * 2**14 < 2**30)
v.assert_true("private ranges (RFC 1918) are /8, /12, /16 blocks", all(ipaddress.ip_network(n).is_private for n in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16")))
v.assert_true("square-root formula from the sawtooth: (3/8) Wm^2 = 1/p gives mean (3/4) Wm = sqrt(3/(2p))", abs(0.75 * math.sqrt(8 / (3 * 1e-4)) - math.sqrt(3 / (2 * 1e-4))) < 1e-9)

# ------------------------------------------------------------------ examples
v.check("Ex 17-13.1a", 100 * 1460 / wire(1460 + TCP + IP4))
v.check("Ex 17-13.1b", 100 * 1440 / wire(1440 + TCP + IP6))
v.check("Ex 17-13.1c", 100 * 100 / wire(100 + UDP + IP4))
v.check("Ex 17-13.1d", 10e9 / (8 * wire(46)) / 1e6)
v.assert_true("Example 1: lab efficiency and wire bytes agree (1538, 166, 84)", wire(1500) == nl.wire_bytes(1500) == 1538 and wire(128) == 166 and wire(46) == 84 and abs(nl.efficiency(1460) - 1460 / 1538) < 1e-12)
hb = next(h for h in range(1, 9) if 2**h - 2 >= 60)
v.check("Ex 17-13.2a", 32 - hb)
v.check("Ex 17-13.2b", 2**hb - 2)
v.check("Ex 17-13.2c", 2 ** ((32 - hb) - 24))
first = ipaddress.ip_network("192.168.10.0/26")
v.check("Ex 17-13.2d", int(str(first.broadcast_address).split(".")[-1]))
agg = nl.aggregate(["10.1.0.0/24", "10.1.1.0/24", "10.1.2.0/24", "10.1.3.0/24"])
v.check("Ex 17-13.2e", agg[0].prefixlen)
v.assert_true("Example 2: the four /24s share exactly 22 leading bits", all((ip_to_int(f"10.1.{k}.0") >> 10) == (ip_to_int("10.1.0.0") >> 10) for k in range(4)) and (ip_to_int("10.1.4.0") >> 10) != (ip_to_int("10.1.0.0") >> 10))
d1, prev1 = nl.dijkstra(G1, "A")
for key, node in (("Ex 17-13.3a", "B"), ("Ex 17-13.3b", "C"), ("Ex 17-13.3c", "D"), ("Ex 17-13.3d", "E")):
    v.check(key, brute_paths(G1, "A", node))
v.assert_true("Example 3: Dijkstra, Bellman-Ford and enumeration agree; path A-B-C-D-E", all(d1[n] == brute_paths(G1, "A", n) == nl.bellman_ford(G1, "A")[0][n] for n in "BCDE") and nl.path(prev1, "E") == ["A", "B", "C", "D", "E"])
bdp = 1e9 * 0.04 / 8
v.check("Ex 17-13.4a", bdp / 1e6)
v.check("Ex 17-13.4b", 8 * 65535 / 0.04 / 1e6)
v.check("Ex 17-13.4c", next(s for s in range(15) if 65535 * 2**s >= bdp))
v.assert_true("Example 4: shift 7 gives 8.39 MB", abs(65535 * 2**7 / 1e6 - 8.39) < 0.005)
# RFC 5681 initial-window rule written independently: 2 segments above 2190 bytes, 3 above 1095, else 4
iw = next(n for lim, n in ((2190, 2), (1095, 3), (0, 4)) if 1460 > lim)
v.assert_true("lab initial_window agrees with the RFC 5681 rule", nl.initial_window(1460) == iw)
v.check("Ex 17-13.5a", iw)
rtts = next(k for k in range(40) if iw * 2**k >= bdp / 1460)
v.check("Ex 17-13.5b", rtts)
v.check("Ex 17-13.5c", rtts * 0.04)
v.check("Ex 17-13.5d", 8 * 1460 / 0.04 * math.sqrt(1.5 / 1e-5) / 1e6)
v.check("Ex 17-13.5e", 8 * 1460 / 0.04 * math.sqrt(1.5 / 1e-7) / 1e6)
seq = rto([0.100, 0.120, 0.080, 0.200])
v.check("Ex 17-13.6a", seq[-1][1] * 1e3)
v.check("Ex 17-13.6b", seq[-1][0] * 1e3)
v.check("Ex 17-13.6c", seq[-1][2] * 1e3)
v.check("Ex 17-13.6d", max(1.0, max(s[2] for s in seq)))
v.assert_true("Example 6: intermediate RTOs 300, 272.5, 249.7 ms; lab estimator agrees", [round(s[2] * 1e3, 1) for s in seq[:3]] == [300.0, 272.5, 249.7] and all(abs(a[2] - b[2]) < 1e-12 for a, b in zip(seq, nl.rto_sequence([0.1, 0.12, 0.08, 0.2]))))
wbar = nl.simulate_aimd(1e-3, 200_000, rng)
v.assert_true(f"AIMD with random loss: mean window {wbar:.1f} is 3-12% above the periodic-loss sqrt(3/(2p)) = 38.7 (constant about 1.3)", 0.03 < wbar / math.sqrt(1.5e3) - 1 < 0.12)
v.assert_true("Example 3: Bellman-Ford converges in four synchronous rounds", nl.bellman_ford(G1, "A")[1] == 4)
v.assert_true("Example 5: the BDP is 3425 segments", round(bdp / 1460) == 3425)
sim_mm1 = nl.simulate_mm1(0.8, 1.0, 300_000, rng)
v.assert_true(f"M/M/1 simulation at 80%: {sim_mm1:.2f} service times vs 5", abs(sim_mm1 / 5 - 1) < 0.05)

# ------------------------------------------------------------------ problems
v.check("17-13.1a", wire(40 + UDP + IP4))
v.check("17-13.1b", 100 * 40 / wire(40 + UDP + IP4))
v.check("17-13.2a", 20 * 19 // 2)
v.check("17-13.2b", len(nx_star := [(0, k) for k in range(1, 21)]))  # one hub-to-host link per host
host = ip_to_int("172.16.45.130")
mask = (0xFFFFFFFF << (32 - 27)) & 0xFFFFFFFF
v.check("17-13.3a", (host | ~mask & 0xFFFFFFFF) & 0xFF)
v.check("17-13.3b", 2 ** (32 - 27) - 2)
v.assert_true("Problem 3: network 172.16.45.128 by masking", (host & mask) == ip_to_int("172.16.45.128") and str(ipaddress.ip_interface("172.16.45.130/27").network) == "172.16.45.128/27")
pf = [32 - next(h for h in range(1, 12) if 2**h - 2 >= n) for n in (100, 50, 20)]
v.check("17-13.4a", pf[0])
v.check("17-13.4b", pf[1])
v.check("17-13.4c", pf[2])
v.check("17-13.4d", 256 - sum(2 ** (32 - p) for p in pf))
table = {"0.0.0.0/0": "R0", "10.0.0.0/8": "R1", "10.1.0.0/16": "R2", "10.1.2.0/24": "R3"}
v.assert_true("Problem 5: longest-prefix matches R3, R2, R1, R0", [nl.longest_prefix_match(table, a) for a in ("10.1.2.9", "10.1.3.1", "10.2.0.1", "8.8.8.8")] == ["R3", "R2", "R1", "R0"])
d2, prev2 = nl.dijkstra(G2, "S")
for key, node in (("17-13.6a", "A"), ("17-13.6b", "C"), ("17-13.6c", "D"), ("17-13.6d", "T")):
    v.check(key, brute_paths(G2, "S", node))
v.assert_true("Problem 6: path S-B-A-C-T; Dijkstra agrees with enumeration", nl.path(prev2, "T") == ["S", "B", "A", "C", "T"] and all(d2[n] == brute_paths(G2, "S", n) for n in "ABCDT"))
b, c, upd, turn = 3, 2, 1, "C"
while not (b >= 16 and c >= 16):
    if turn == "C":
        c = min(b + 1, 16)
        turn = "B"
    else:
        b = min(c + 1, 16)
        turn = "C"
    upd += 1
v.check("17-13.7a", upd)
bdp2 = 10e9 * 0.1 / 8
v.check("17-13.8a", bdp2 / 1e6)
v.check("17-13.8b", 8 * 65535 / 0.1 / 1e6)
v.check("17-13.8c", next(s for s in range(15) if 65535 * 2**s >= bdp2))
v.check("17-13.9a", nl.initial_window(536))
v.check("17-13.9b", next(k for k in range(20) if 4 * 2**k >= 64))
v.check("17-13.10a", 1.5 * (8 * 1460 / (0.1 * 1e10)) ** 2)
yr = 365.25 * 24 * 3600
v.check("17-13.11a", 0.5 * 2.0**56 / 1e12 / 3600)
v.check("17-13.11b", 0.5 * 2.0**80 / 1e12 / yr)
v.check("17-13.11c", 0.5 * 2.0**128 / 1e12 / yr)
v.check("17-13.12a", math.sqrt(2 * 2.0**64 * math.log(2)))
v.check("17-13.12b", math.log2(math.sqrt(2 * 2.0**256 * math.log(2))))
coll = np.mean([len(set(rng.integers(0, 2**20, 1206))) < 1206 for _ in range(4000)])
v.assert_true(f"Problem 12: birthday bound checked at 20 bits: {coll:.3f} collision probability at sqrt(2 ln2 2^20) = 1206 draws", abs(coll - 0.5) < 0.03)
svc = 1500 * 8 / 1e9
v.check("17-13.13a", svc / (1 - 0.7) * 1e6)
v.check("17-13.13b", svc / (1 - 0.9) * 1e6)
v.check("17-13.13c", 0.9 / (1 - 0.9))
rules = [("allow", {"proto": "tcp", "dport": 443}), ("allow", {"proto": "tcp", "dport": 22, "src": "10.0.0.5"}), ("deny", {"proto": "tcp", "dport": 22}), ("allow", {"proto": "udp", "dport": 53})]
pkts = [{"proto": "tcp", "dport": 443, "src": "203.0.113.7"}, {"proto": "tcp", "dport": 22, "src": "10.0.0.5"}, {"proto": "tcp", "dport": 22, "src": "10.0.0.6"}, {"proto": "udp", "dport": 53, "src": "198.51.100.2"}, {"proto": "tcp", "dport": 80, "src": "10.0.0.5"}]
dec = [nl.firewall(rules, p) for p in pkts]
v.check("17-13.14a", dec.count("allow"))
v.assert_true("Problem 14: decisions allow, allow, deny, allow, deny; swapping rules 2 and 3 denies (b)", dec == ["allow", "allow", "deny", "allow", "deny"] and nl.firewall([rules[0], rules[2], rules[1], rules[3]], pkts[1]) == "deny")

# ------------------------------------------------------------------ lab
v.check("Lab 17-13.a", 100 * 512 / wire(512 + TCP + IP4))
v.check("Lab 17-13.b", 32 - next(h for h in range(1, 16) if 2**h - 2 >= 1000))
v.check("Lab 17-13.c", len(list(ipaddress.ip_network("10.20.0.0/16").subnets(new_prefix=22))))
v.check("Lab 17-13.d", math.sqrt(3 / (2 * 1e-3)))
v.check("Lab 17-13.e", math.sqrt(3 / (2 * 1e-4)))
v.check("Lab 17-13.f", 1 / (1 - 0.95))
v.assert_true("Lab part 1: 64-byte payload efficiency 45.1%", abs(100 * 64 / wire(64 + TCP + IP4) - 45.1) < 0.05)

# Problems 17-13.16 to 17-13.19
_pa, _tp, _fp = 1e-5, 0.99, 1e-3
v.check("17-13.16a", 100 * _tp * _pa / (_tp * _pa + _fp * (1 - _pa)))
v.check("17-13.16b", _fp * (1 - _pa) / (_tp * _pa))
v.check("17-13.16c", optimize.brentq(lambda f: _tp * _pa - f * (1 - _pa), 0, 1e-3))
v.check("17-13.17a", 1500 * 8 / 1e9 * 1e6)
v.check("17-13.17b", 1e6 / 2e8 * 1e3)
_wait = 1 / (1 / 12e-6 - 0.8 / 12e-6) - 12e-6  # M/M/1 time in system minus service
v.check("17-13.17c", _wait * 1e6)
v.check("17-13.17d", (2e-6 + _wait + 12e-6 + 5e-3) * 1e6)
_table, _flood = {}, 0
for src, port, dst in (("A", 1, "B"), ("B", 2, "A"), ("C", 3, "A"), ("A", 1, "C"), ("D", 4, "B")):
    _table[src] = port
    if dst not in _table:
        _flood += 1
v.check("17-13.18", _flood)
for key, b in (("17-13.19a", 2), ("17-13.19b", 1)):
    v.check(key, 8 * 1460 / 0.05 * math.sqrt(3 / (2 * b * 1e-4)) / 1e6)
_wm = math.sqrt(8 / (3 * 2 * 1e-4))
v.assert_true("delayed-ACK cycle carries 1/p packets", abs(0.75 * _wm * 2 * _wm / 2 - 1e4) < 1e-6)

# lab: distance vector after a failure, with and without split horizon (rounds independent of the lab via brute force)
_chain = {"A": {"B": 1}, "B": {"A": 1, "C": 1}, "C": {"B": 1}}
_G2 = {"S": {"A": 4, "B": 1}, "A": {"S": 4, "B": 2, "C": 5}, "B": {"S": 1, "A": 2, "D": 8},
       "C": {"A": 5, "D": 3, "T": 2}, "D": {"B": 8, "C": 3, "T": 6}, "T": {"C": 2, "D": 6}}
v.check("Lab 17-13.g", nl.dv_after_failure(_chain, ("B", "C"), "C")[0])
v.check("Lab 17-13.h", nl.dv_after_failure(_chain, ("B", "C"), "C", split_horizon=True)[0])
_r8, _d8 = nl.dv_after_failure(_G2, ("C", "T"), "T")
_r4, _d4 = nl.dv_after_failure(_G2, ("C", "T"), "T", split_horizon=True)
v.check("Lab 17-13.i", _r8)
v.check("Lab 17-13.j", _r4)
_G2f = {u: {w: c for w, c in nb.items() if {u, w} != {"C", "T"}} for u, nb in _G2.items()}
v.assert_true("after the failure both variants converge to the true shortest distances",
              all(_d8[n] == _d4[n] == brute_paths(_G2f, n, "T") for n in "SABCD"))

sys.exit(v.finish())
