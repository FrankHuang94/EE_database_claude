# Solutions 14-11 · I/O, Buses and Interconnect

Problems: [14-11 problems](../problems/14-11-problems.md) · Chapter: [14-11](../chapters/14-11-io-buses-and-interconnect.md). Every number below is recomputed by [verify_14_11.py](../verify/verify_14_11.py). The AXI4-Lite cycle counts are measured by running the lab's testbench under Icarus Verilog, and the mesh hop counts by enumerating every pair of nodes.

---

## Solutions

### Solution 14-11.1

(a) 0x4000_2000 + 0x0C = **0x4000_200C**.

(b) Reading RXDATA has a side effect: it removes a byte from the receive queue. Its value also changes without any store from the CPU.

- `volatile` forces the compiler to perform every read and write, in program order, rather than keeping a copy in a register or deleting reads that look redundant.
- The page must be uncacheable so that each access reaches the device. A cached copy would return the same stale byte forever, and a cached write might reach the device late or never.

### Solution 14-11.2

One byte is 10 bits: $10 / 9600$ = **1.042** ms. The maximum throughput is $9600 / 10$ = **960** bytes per second.

### Solution 14-11.3

(a) Bytes arrive at $115200 / 10 = 11{,}520$ per second, so a 16-byte FIFO fills in $16 / 11520$ = **1.389** ms. The loop must empty it at least that often, 720 times per second (in practice faster, for margin).

(b) $720 \times 200 / (48 \times 10^6)$ = **0.3**% of the CPU, cheap, but only because the FIFO absorbs 16 bytes per poll. With a single-byte buffer it would be 16 times more.

### Solution 14-11.4

Polling costs $100{,}000 \text{ polls/s} \times 100$ cycles = $10^7$ cycles per second, whatever the event rate. Interrupts cost $1500\,r$ cycles per second at $r$ events per second. They are equal at $r = 10^7 / 1500$ = **6667** events per second. Above that, polling is cheaper. Below it, interrupts are, and they also free the CPU completely when the device is idle.

### Solution 14-11.5

(a) Programmed I/O takes $65536 / 4 \times 40$ = **655,360** cycles. DMA takes $500 + 1500$ = **2000** cycles of CPU time, more than 300 times less.

(b) $65536 / 64$ = **1024** lines. Invalidation itself costs cycles, so large coherent systems prefer hardware-coherent DMA.

### Solution 14-11.6

(a) Each write takes $2 + 1 = 3$ cycles of 5 ns, so 100 writes take 300 cycles = **1.5** µs. The throughput is 400 bytes / 1.5 µs = **266.7** MB/s.

(b) One 4-byte write per 5 ns cycle gives **800** MB/s, three times better. The subordinate must be able to hold a new response while the previous one is still being accepted (a skid buffer), which costs registers.

### Solution 14-11.7

The peak is 16 bytes × 1 GHz = **16** GB/s. Each burst moves 16 beats in 20 cycles, an efficiency of **80**%, so the delivered bandwidth is **12.8** GB/s. Longer bursts amortize the overhead better.

### Solution 14-11.8

Average hops, from $2(k^2 - 1)/(3k)$ and confirmed by enumeration:

- 4 × 4: **2.5** hops;
- 16 × 16: **10.625** hops, so the average zero-load latency is $10.625 \times 4$ = **42.5** cycles.

The bisection grows from 4 to 16 links per direction, a factor of **4**, while the nodes grow from 16 to 256, a factor of **16**. Bisection bandwidth per node therefore falls as $1/k$, and many-core chips depend on keeping traffic local.

### Solution 14-11.9

(a) PCIe 4.0 x4: $16 \times 4 \times (128/130) / 8$ = **7.877** GB/s.

(b) PCIe 5.0 x4: $32 \times 4 \times (128/130) / 8$ = **15.754** GB/s.

(c) PCIe 7.0 x16, raw: $128 \times 16 / 8$ = **256** GB/s per direction, the "512 GB/s" bidirectional figure of PCI-SIG's release. Flit and FEC overhead come off this.

### Solution 14-11.10

By Little's law, $64 \times 10^9 \times 10^{-6} / 256$ = **250** requests in flight. With 64 outstanding, the bandwidth is $64 \times 256 / 10^{-6}$ = **16.384** GB/s, a quarter of the target. The engine needs deeper queues, or several engines in parallel.

### Solution 14-11.11

(a) 32 packets take $32 \times 12 = 384$ µs to arrive, much longer than the 50 µs timeout. The timeout therefore always fires first, giving $1 / 50 \text{ µs}$ = **20,000** interrupts per second, each covering about 4.2 packets.

(b) $20{,}000 \times 2000 / (3 \times 10^9)$ = **1.333**% of the core: four times less than per-packet interrupts (5.56%), though more than the 0.174% of pure 32-packet coalescing.

(c) At most **50** µs. The timeout bounds the latency cost of coalescing.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 14-11.1a | RXDATA address | 0x4000200C | — |
| 14-11.2a | time per byte | 1.042 | ms |
| 14-11.2b | throughput | 960 | B/s |
| 14-11.3a | time to fill the FIFO | 1.389 | ms |
| 14-11.3b | polling overhead | 0.3 | % |
| 14-11.4a | crossover event rate | 6667 | /s |
| 14-11.5a | CPU cycles, programmed I/O | 655360 | — |
| 14-11.5b | CPU cycles, DMA | 2000 | — |
| 14-11.5c | lines to invalidate | 1024 | — |
| 14-11.6a | time for 100 writes | 1.5 | µs |
| 14-11.6b | throughput, k = 1 | 266.7 | MB/s |
| 14-11.6c | throughput, one write per cycle | 800 | MB/s |
| 14-11.7a | peak bandwidth | 16 | GB/s |
| 14-11.7b | efficiency | 80 | % |
| 14-11.7c | delivered bandwidth | 12.8 | GB/s |
| 14-11.8a | average hops, 4 × 4 | 2.5 | — |
| 14-11.8b | average hops, 16 × 16 | 10.625 | — |
| 14-11.8c | zero-load latency, 16 × 16 | 42.5 | cycles |
| 14-11.8d | bisection growth | 4 | — |
| 14-11.8e | node growth | 16 | — |
| 14-11.9a | PCIe 4.0 x4 | 7.877 | GB/s |
| 14-11.9b | PCIe 5.0 x4 | 15.754 | GB/s |
| 14-11.9c | PCIe 7.0 x16 raw | 256 | GB/s |
| 14-11.10a | requests in flight | 250 | — |
| 14-11.10b | bandwidth with 64 outstanding | 16.384 | GB/s |
| 14-11.11a | interrupts per second | 20000 | /s |
| 14-11.11b | CPU fraction | 1.333 | % |
| 14-11.11c | worst-case added latency | 50 | µs |
