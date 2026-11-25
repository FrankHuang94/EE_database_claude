# Solutions 24-05 · Interconnect Standards: PCIe, CXL and Ethernet

Problems: [24-05 problems](../problems/24-05-problems.md) · Chapter: [24-05](../chapters/24-05-pcie-cxl-ethernet.md)

Every number is recomputed by [verify_24_05.py](../verify/verify_24_05.py).

---

## Solutions

### Solution 24-05.1

(a) $8 \times 16 \times (128/130)/8$ = **15.75** GB/s.

(b) $15.75 \times 128/152$ = **13.27** GB/s.

### Solution 24-05.2

(a) $128 \times 16 \times (236/256)/8$ = **236** GB/s.

(b) $236/512$ = **0.461**: less than half the headline, because the headline counts both directions and the raw rate.

### Solution 24-05.3

(a) $8 \times 128/130/8$ = **0.985** GB/s against $10 \times 0.8/8$ = **1.00** GB/s.

(b) **4** GHz against **5** GHz.

(c) 8 GT/s. It gives 98.5% of the bandwidth at a 20% lower Nyquist frequency, so the channel loses less and costs less. The better encoding paid for nearly all of the rate.

### Solution 24-05.4

(a) $8 \times 32/8$ = **32** GB/s.

(b) $32 \times 10^9 \times 800 \times 10^{-9}$ = **25.6** KB.

(c) $16/25.6$ = **0.625** of the raw rate, **20** GB/s.

The link runs at 62.5% of its capability for want of buffer, a loss no SerDes improvement can recover.

### Solution 24-05.5

The round trip grows by $2 \times 2 \times 10$ = 40 ns, so the buffer grows by $128 \times 10^9 \times 40 \times 10^{-9}$ = **5.12** KB.

### Solution 24-05.6

(a) $128 \times 16 \times (236/256)/8$ = **236** GB/s.

(b) $236/51.2$ = **4.61** channels.

(c) Both directions give 472 GB/s over 64 wires, **7.375** GB/s per wire, against $51.2/64$ = **0.8** GB/s per DDR5 data pin: **9.2** times more.

This is CXL's real attraction for memory: bandwidth per pin. The comparison flatters it a little, since DDR's pins also carry strobes and commands and its data pins are shared between reads and writes, but the order of magnitude is right.

### Solution 24-05.7

The average is $100 + 100x \le 110$, so $x \le$ **0.10**: at most 10% of accesses may go to CXL memory.

### Solution 24-05.8

(a) **4** lanes, $4 \times 212.5$ = **850** Gb/s.

(b) **8** lanes at 106.25 Gb/s, also **850** Gb/s.

(c) **53.125** GBd PAM4.

### Solution 24-05.9

(a) $102.4/0.8$ = **128** ports; $128^2/2$ = **8,192** hosts.

(b) **64** ports; **2,048** hosts, each at twice the bandwidth.

### Solution 24-05.10

(a) $51.2/0.4$ = **128** ports.

(b) A two-tier fabric holds $128^2/2$ = **8,192** hosts at full bisection, more than 4,096: **yes**.

(c) Each leaf uses half its ports, 64, for hosts: $4096/64$ = **64** leaves.

(d) Each leaf has 64 uplinks: $64 \times 64$ = **4,096** uplinks.

(e) Each spine has 128 ports: $4096/128$ = **32** spines.

That is 96 switch chips and 4,096 leaf-to-spine links, most of them optical (24-08 prices the optics' power).

### Solution 24-05.11

$1.6 \times 10^{12} \times 2 \times 10^{-6}/8$ = **400** KB.

### Solution 24-05.12

(a) $512/2$ = **256** GBd. (b) **128** GHz. (c) **3.91** ps.

A 128 GHz Nyquist frequency on a printed-circuit board is far beyond the losses of 24-01's budgets, which is why each PCIe generation leans harder on retimers, better materials, cables and eventually optics.

### Solution 24-05.13

(a) $128/2$ = **64** GBd. (b) **32** GHz. (c) $1/64$ GBd = **15.625** ps.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 24-05.1a | PCIe 4.0 x8 bandwidth | 15.75 | GB/s |
| 24-05.1b | payload bandwidth, 128-byte TLPs | 13.27 | GB/s |
| 24-05.2a | PCIe 7.0 x16 flit payload | 236 | GB/s |
| 24-05.2b | fraction of headline | 0.461 | |
| 24-05.3a | 8 GT/s 128b/130b per lane | 0.985 | GB/s |
| 24-05.3a1 | 10 GT/s 8b/10b per lane | 1.00 | GB/s |
| 24-05.3b | Nyquist at 8 GT/s | 4 | GHz |
| 24-05.3b1 | Nyquist at 10 GT/s | 5 | GHz |
| 24-05.3c | bandwidth retained | 98.5 | % |
| 24-05.3c1 | lower Nyquist frequency | 20 | % |
| 24-05.4a | raw bandwidth | 32 | GB/s |
| 24-05.4b | bandwidth-delay product | 25.6 | KB |
| 24-05.4c | sustainable fraction | 0.625 | |
| 24-05.4c1 | throughput | 20 | GB/s |
| 24-05.4c2 | sustainable share | 62.5 | % |
| 24-05.5a | added round trip | 40 | ns |
| 24-05.5 | added buffer | 5.12 | KB |
| 24-05.6a | CXL 4.0 x16 payload | 236 | GB/s |
| 24-05.6b | DDR5-6400 channels | 4.61 | |
| 24-05.6c0 | both directions | 472 | GB/s |
| 24-05.6c | per CXL wire | 7.375 | GB/s |
| 24-05.6c1 | per DDR5 data pin | 0.8 | GB/s |
| 24-05.6c2 | ratio | 9.2 | |
| 24-05.7 | largest CXL share | 0.10 | |
| 24-05.8a | lanes at 200G | 4 | |
| 24-05.8a1 | line rate at 200G | 850 | Gb/s |
| 24-05.8b | lanes at 100G | 8 | |
| 24-05.8b1 | line rate at 100G | 850 | Gb/s |
| 24-05.8c | 100G lane symbol rate | 53.125 | GBd |
| 24-05.9a | radix at 800G | 128 | |
| 24-05.9a1 | two-tier hosts at 800G | 8192 | |
| 24-05.9b | radix at 1.6T | 64 | |
| 24-05.9b1 | two-tier hosts at 1.6T | 2048 | |
| 24-05.10a | radix at 400G | 128 | |
| 24-05.10b | two-tier capacity | 8192 | |
| 24-05.10c | leaves | 64 | |
| 24-05.10d | uplinks | 4096 | |
| 24-05.10e | spines | 32 | |
| 24-05.10f | switch chips | 96 | |
| 24-05.11 | replay buffer | 400 | KB |
| 24-05.12a | symbol rate | 256 | GBd |
| 24-05.12b | Nyquist frequency | 128 | GHz |
| 24-05.12c | UI | 3.91 | ps |
| 24-05.13a | symbol rate | 64 | GBd |
| 24-05.13b | Nyquist frequency | 32 | GHz |
| 24-05.13c | UI | 15.625 | ps |
