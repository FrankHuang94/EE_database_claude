# Solutions 17-13 · Computer Networks Fundamentals

Problems: [17-13 problems](../problems/17-13-problems.md) · Chapter: [17-13](../chapters/17-13-computer-networks-fundamentals.md). Every number below is recomputed by [verify_17_13.py](../verify/verify_17_13.py).

---

## Solutions

### Solution 17-13.1

IP packet $40 + 8 + 20 = 68$ bytes (above the 46-byte minimum, so no padding). Wire: $8 + 14 + 68 + 4 + 12$ = **106** bytes; the query is $40/106$ = **37.7** %.

### Solution 17-13.2

Full mesh: $20 \times 19/2$ = **190** links. Star: one link per host, **20**. The mesh buys redundancy and direct paths at a cost that grows as $n^2$.

### Solution 17-13.3

A /27 has 32 addresses; 130 lies in the block 128–159. Network **172.16.45.128**, broadcast 172.16.45.**159**, usable hosts $32 - 2$ = **30**.

### Solution 17-13.4

100 hosts need 7 host bits (126): **/25** at 10.0.0.0. 50 hosts need 6 (62): **/26** at 10.0.0.128. 20 hosts need 5 (30): **/27** at 10.0.0.192. Used $128 + 64 + 32 = 224$ of 256, leaving **32** addresses (10.0.0.224/27) free. Allocating largest first keeps every subnet aligned on its own size.

### Solution 17-13.5

10.1.2.9 matches all four; the longest is /24: **R3**. 10.1.3.1 matches /0, /8, /16: **R2**. 10.2.0.1 matches /0 and /8: **R1**. 8.8.8.8 matches only the default: **R0**.

### Solution 17-13.6

Finalize S (0); B = 1, A = 4. Finalize B (1); A = min(4, 3) = 3, D = 9. Finalize A (3); C = 8. Finalize C (8); D = min(9, 11) = 9, T = 10. Finalize D (9); T = min(10, 15) = 10. Distances: A **3**, B **1**, C **8**, D **9**, T **10**, path S–B–A–C–T.

### Solution 17-13.7

B adopts 3 (update 1); C then 4 (2), B 5 (3), C 6 (4), …: update $k$ sets the updating router to $k + 2$. Update 14 brings C to 16 (infinity), and update 15 brings B to 16 (capped): **15** updates, each one exchange interval of misrouting. Split horizon with poisoned reverse (C advertising ∞ back to B for routes learned through B) removes this two-node loop.

### Solution 17-13.8

BDP $= 10^{10} \times 0.1/8$ = **125** MB. Unscaled throughput $8 \times 65\,535/0.1$ = **5.24** Mb/s. Shift: $65\,535 \times 2^{11}$ = 134.2 MB ≥ 125 MB, so **11** (10 gives 67.1 MB).

### Solution 17-13.9

SMSS ≤ 1095 bytes: IW = **4** segments. $4 \to 8 \to 16 \to 32 \to 64$: **4** round trips.

### Solution 17-13.10

Solve $\frac{8 \times 1460}{0.1}\sqrt{\frac{3}{2p}} = 10^{10}$: $p = \tfrac32\big(\frac{11\,680}{10^9}\big)^2$ = **2.05e-10**, one loss in about five billion packets, far below what real long-distance paths deliver. High-speed bulk transfers therefore use many flows or congestion controllers less sensitive to random loss.

### Solution 17-13.11

Half the key space on average: 56-bit **10.0** hours; 80-bit **1.92e4** years; 128-bit **5.39e18** years (the universe is about $1.4 \times 10^{10}$ years old).

### Solution 17-13.12

$\sqrt{2 \times 2^{64}\ln2}$ = **5.06e9** hashes, so 64-bit digests are inadequate for collision resistance. For 256 bits: $\log_2\sqrt{2 \times 2^{256}\ln2}$ = **128.2**.

### Solution 17-13.13

Service time $1500 \times 8/10^9$ = 12 μs. $T = 12/(1 - \rho)$: **40** μs at 70%, **120** μs at 90%. Little's law: $N = \lambda T = \rho/(1 - \rho)$ = **9** packets at 90%.

### Solution 17-13.14

(a) rule 1: allow. (b) rule 2: allow. (c) rule 3: deny. (d) rule 4: allow. (e) no rule matches: default deny. So (a), (b) and (d) are allowed: **3** of 5. With rules 2 and 3 swapped, (b) matches "deny TCP 22 from anywhere" first and is **denied**: rule order is policy.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 17-13.1a | wire bytes | 106 | bytes |
| 17-13.1b | query fraction | 37.7 | % |
| 17-13.2a | full-mesh links | 190 | — |
| 17-13.2b | star links | 20 | — |
| 17-13.3a | broadcast last octet | 159 | — |
| 17-13.3b | usable hosts | 30 | — |
| 17-13.4a | prefix for 100 hosts | 25 | — |
| 17-13.4b | prefix for 50 hosts | 26 | — |
| 17-13.4c | prefix for 20 hosts | 27 | — |
| 17-13.4d | addresses left | 32 | — |
| 17-13.6a | distance to A | 3 | — |
| 17-13.6b | distance to C | 8 | — |
| 17-13.6c | distance to D | 9 | — |
| 17-13.6d | distance to T | 10 | — |
| 17-13.7a | updates to infinity | 15 | — |
| 17-13.8a | bandwidth-delay product | 125 | MB |
| 17-13.8b | unscaled throughput | 5.24 | Mb/s |
| 17-13.8c | window-scale shift | 11 | — |
| 17-13.9a | initial window | 4 | segments |
| 17-13.9b | round trips to 64 segments | 4 | — |
| 17-13.10a | tolerable loss rate | 2.05e-10 | — |
| 17-13.11a | 56-bit search | 10.0 | hours |
| 17-13.11b | 80-bit search | 1.92e4 | years |
| 17-13.11c | 128-bit search | 5.39e18 | years |
| 17-13.12a | 64-bit birthday bound | 5.06e9 | — |
| 17-13.12b | 256-bit bound, log2 | 128.2 | — |
| 17-13.13a | delay at 70% | 40 | μs |
| 17-13.13b | delay at 90% | 120 | μs |
| 17-13.13c | packets in system at 90% | 9 | — |
| 17-13.14a | packets allowed | 3 | — |
