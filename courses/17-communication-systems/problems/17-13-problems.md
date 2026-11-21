# Problems 17-13 · Computer Networks Fundamentals

Chapter: [17-13](../chapters/17-13-computer-networks-fundamentals.md) · Worked solutions: [17-13 solutions](../solutions/17-13-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Ethernet on the wire: 8 bytes preamble/SFD + 14 header + payload (46–1500) + 4 FCS + 12 inter-frame gap. Headers: IPv4 20, IPv6 40, TCP 20, UDP 8 bytes. IPv4 subnets reserve the all-zeros and all-ones host addresses. TCP formulas follow RFC 5681, 6298 and 7323. Problems marked *(lab)* can be checked with the lab's `netlab.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 17-13.1 [A]

**A small query.** A 40-byte DNS query is sent over UDP/IPv4/Ethernet. How many bytes does it occupy on the wire, and what fraction is the query itself?

### Problem 17-13.2 [A]

**Topologies.** How many links does a full mesh of 20 routers need? How many does a star of 20 hosts around one switch need?

### Problem 17-13.3 [A]

**Reading an address.** For the host 172.16.45.130/27, find the network address, the broadcast address and the number of usable host addresses.

### Problem 17-13.4 [B]

**Variable-length subnets.** *(lab)* From 10.0.0.0/24, allocate subnets for departments of 100, 50 and 20 hosts, largest first and as small as possible. Give each prefix length, and the number of addresses left unallocated.

### Problem 17-13.5 [B]

**Longest-prefix match.** A router has routes 0.0.0.0/0 → R0, 10.0.0.0/8 → R1, 10.1.0.0/16 → R2 and 10.1.2.0/24 → R3. Which next hop serves 10.1.2.9, 10.1.3.1, 10.2.0.1 and 8.8.8.8?

### Problem 17-13.6 [B]

**Dijkstra.** *(lab)* Links: S–A 4, S–B 1, A–B 2, A–C 5, B–D 8, C–D 3, C–T 2, D–T 6. Find the shortest distances from S to every node and the path to T.

### Problem 17-13.7 [B]

**Counting to infinity.** A–B–C is a chain with unit costs, and RIP's infinity is 16. The A–B link fails. Before B can advertise the loss, it hears C's distance to A (2) and adopts 3 via C; thereafter B and C alternate updates, each adding 1 to the other's latest distance. How many updates (counting B's first) until both reach 16?

### Problem 17-13.8 [B]

**A transoceanic 10 Gb/s path.** RTT 100 ms. Find the bandwidth-delay product, the throughput of an unscaled 65 535-byte window, and the smallest window-scale shift that covers the BDP.

### Problem 17-13.9 [B]

**Slow start with small segments.** What initial window does RFC 5681 allow for a 536-byte SMSS, and how many round trips of doubling bring cwnd to 64 segments?

### Problem 17-13.10 [C]

**Loss budget for one fast flow.** Using the square-root formula, what random loss rate would let a single TCP flow with a 1460-byte MSS sustain 10 Gb/s over a 100 ms RTT?

### Problem 17-13.11 [B]

**Brute force.** At $10^{12}$ guesses per second, how long does an exhaustive search take on average for 56-, 80- and 128-bit keys?

### Problem 17-13.12 [B]

**Birthday bounds.** How many random 64-bit hashes give a 50% chance of a collision? What is the base-2 logarithm of the corresponding number for a 256-bit hash?

### Problem 17-13.13 [B]

**A busy link.** A 1 Gb/s link carries 1500-byte packets. Model it as M/M/1 and find the mean time in the system at 70% and at 90% load, and the mean number of packets in the system at 90% (Little's law).

### Problem 17-13.14 [C]

**A firewall policy.** *(lab)* Rules, checked in order: (1) allow TCP to port 443 from anywhere; (2) allow TCP to port 22 from source 10.0.0.5; (3) deny TCP to port 22 from anywhere; (4) allow UDP to port 53 from anywhere; then deny all. Decide: (a) TCP 443 from 203.0.113.7; (b) TCP 22 from 10.0.0.5; (c) TCP 22 from 10.0.0.6; (d) UDP 53 from 198.51.100.2; (e) TCP 80 from 10.0.0.5. How many are allowed? What happens to (b) if rules 2 and 3 are swapped?

---

## Objective coverage

| Learning objective (chapter 17-13) | Problems |
|---|---|
| 1. Layers, overhead, topologies | 1, 2 |
| 2. Ethernet and switching | 1 |
| 3. Addressing and forwarding | 3, 4, 5 |
| 4. Routing algorithms | 6, 7 |
| 5. TCP and queues | 8, 9, 10, 13 |
| 6. Security | 11, 12, 14 |
