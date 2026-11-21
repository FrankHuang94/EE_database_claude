# Lab 17-13 · Packets, Routes, Windows and Firewalls

Chapter: [17-13 · Computer Networks Fundamentals](../../chapters/17-13-computer-networks-fundamentals.md)

## Objective

Work through the networking stack numerically:

- protocol overhead and wire efficiency against payload size;
- IPv4 subnetting, aggregation and longest-prefix forwarding;
- Dijkstra and Bellman–Ford routing, including count-to-infinity after a failure;
- TCP's window and loss limits, with a simulated AIMD sawtooth;
- queueing delay in an M/M/1 link;
- a first-match firewall and the arithmetic of key search.

## Background

Each layer adds a header; Ethernet adds a preamble and an inter-frame gap on the wire (§3.2). A /p IPv4 subnet holds $2^{32-p} - 2$ hosts, and routers forward by the longest matching prefix (§3.3). Link-state routing runs Dijkstra; distance-vector routing iterates Bellman–Ford (§3.4). TCP sends at most a window per RTT, and with random loss $p$ its AIMD sawtooth averages $\sqrt{3/(2p)}$ segments per RTT (§3.5). An M/M/1 queue's delay is $1/(\mu - \lambda)$ (§3.6).

## Files

- `netlab.py`: `wire_bytes`, `efficiency`, `max_frame_rate`, `full_mesh_links`, `subnet`, `usable_hosts`, `prefix_for_hosts`, `aggregate`, `longest_prefix_match`, `dijkstra`, `path`, `bellman_ford`, `dv_after_failure`, `window_throughput`, `bdp_bytes`, `window_shift_needed`, `initial_window`, `slow_start_rtts`, `mathis_throughput`, `simulate_aimd`, `rto_sequence`, `mm1_delay`, `simulate_mm1`, `brute_force_years`, `birthday_trials`, `firewall`, and header-size constants.
- `17-13-networks-lab.ipynb`: the guided notebook.

## Procedure

1. **Overhead.** Predict the TCP/IPv4 wire efficiency for 64-, 512- and 1460-byte payloads; plot efficiency from 1 to 1460 bytes and mark where padding stops mattering.
2. **Addressing.** Split 10.20.0.0/16 into subnets of at least 1000 hosts; build a forwarding table with overlapping prefixes and test longest-prefix matches.
3. **Routing.** Run Dijkstra on the six-router network of Problem 17-13.6; then fail a link (B–C in a three-router chain, C–T in the six-router network) and run `dv_after_failure` with and without split horizon.
4. **TCP.** Simulate the AIMD sawtooth for loss rates from $10^{-2}$ to $10^{-5}$; compare the mean window with $\sqrt{3/(2p)}$. Then compute window-limited and loss-limited throughput for a 1 Gb/s, 40 ms path.
5. **Queues.** Simulate an M/M/1 queue from 10% to 95% load and compare with $1/(\mu - \lambda)$.
6. **Security.** Implement the firewall policy of Problem 17-13.14 and test it; tabulate brute-force times for 56-, 80- and 128-bit keys.

## Expected results

- Part 1: 45.1%, 86.8% and 94.9%; below 6 bytes of TCP payload the 46-byte padding floor sets the frame size (mark it on the plot).
- Part 2: /22 subnets (1022 hosts), 64 of them in the /16.
- Part 3: distances 3, 1, 8, 9, 10 to A, B, C, D, T. After B–C fails, the chain counts to infinity (16) in 15 rounds without split horizon and 2 with it; after C–T fails in the six-router network, the routers settle on the route via D in 8 rounds without split horizon and 4 with it.
- Part 4: the simulated mean window is within about 10% of $\sqrt{3/(2p)}$ (38.7 segments at $10^{-3}$, 122.5 at $10^{-4}$), slightly above it because the model's loss process differs from the ideal sawtooth.
- Part 5: simulation within a few percent of the formula (convergence is slow as ρ → 1); 20 service times in the system at 95% load.
- Part 6: decisions allow, allow, deny, allow, deny; times of 10 hours, about 19 000 years and $5 \times 10^{18}$ years.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 17-13.a | efficiency, 512-byte TCP payload | 86.8 | % |
| Lab 17-13.b | prefix for 1000 hosts | 22 | — |
| Lab 17-13.c | subnets of that size in a /16 | 64 | — |
| Lab 17-13.d | AIMD mean window at 1e-3 (formula) | 38.7 | segments |
| Lab 17-13.e | AIMD mean window at 1e-4 (formula) | 122.5 | segments |
| Lab 17-13.f | M/M/1 delay at 95% load | 20 | service times |
| Lab 17-13.g | chain count-to-infinity rounds, no split horizon | 15 | — |
| Lab 17-13.h | chain rounds with split horizon | 2 | — |
| Lab 17-13.i | six-router rounds after C–T fails, no split horizon | 8 | — |
| Lab 17-13.j | six-router rounds with split horizon | 4 | — |

## Discussion

1. Why do switch vendors quote packet rates at 64-byte frames?
2. Why does Bellman–Ford count to infinity after a failure while Dijkstra does not?
3. Why does halving the RTT double TCP's loss-limited throughput?

## Answers

1. Fixed per-frame work (lookup, buffering, scheduling) and fixed per-frame wire overhead make minimum-size frames the hardest case: 14.88 million per second at 10 Gb/s.
2. Distance-vector routers know only neighbours' distances, not paths, so a router can adopt a route that passes back through itself; each exchange raises the stale cost by the link cost (one, with unit costs). Link-state routers have the whole topology and recompute shortest paths directly after the failure is flooded.
3. AIMD adds one segment per RTT, so the sawtooth's window size is set by the loss rate alone; throughput is that window divided by the RTT.

## Optional hardware

On any computer, `ping` and `traceroute` show RTTs and hop counts to distant servers, and a file transfer with a tool such as `iperf3` (with one and with several parallel streams) shows window- and loss-limited throughput on a real path. Only test networks you own or are authorized to measure.
