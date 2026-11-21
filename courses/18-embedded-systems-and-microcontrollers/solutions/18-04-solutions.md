# Solutions 18-04 · DMA and Data Movement

Problems: [18-04 problem set](../problems/18-04-problems.md) · Chapter: [18-04](../chapters/18-04-dma-and-data-movement.md). Every number below is recomputed by [verify_18_04.py](../verify/verify_18_04.py).

---

## Solutions

### Solution 18-04.1

(a) $10 \times 10^6/8 = 1.25 \times 10^6$ bytes/s: $1.25 \times 10^6 \times 60/(168 \times 10^6)$ = **44.6** %.

(b) $1.25 \times 10^6/64 = 19\,531$ blocks/s: $19\,531 \times 200/(168 \times 10^6)$ = **2.33** %, nineteen times less.

### Solution 18-04.2

$1500/4$ = **375** transfers with 32-bit words; $1500/2$ = **750** with 16-bit half-words.

### Solution 18-04.3

(a) Head $= 256 - 37$ = **219**.

(b) $(219 - 200) \bmod 256$ = **19** bytes.

(c) $(219 - 230) \bmod 256$ = **245** bytes: the head has wrapped past the end of the buffer and is "behind" the tail numerically, but ahead of it around the ring.

### Solution 18-04.4

$bf_s = 5 \times 10^{-6} \times 48\,000 = 0.24$.

(a) $N \ge 200 \times 10^{-6} \times 48\,000/0.76$ = **12.6**, so 13 samples.

(b) $N \ge 300 \times 10^{-6} \times 48\,000/0.76$ = **18.9**, so 19 samples.

(c) **32** samples (0.667 ms). Worst latency: $666.7 + 100 + 200 + 5 \times 32$ = **1127** µs.

### Solution 18-04.5

With three buffers the deadline condition gives $N \ge 300 \times 10^{-6} \times 48\,000/(2 - 0.24)$ = **8.2**, but the CPU must also keep up on average: the throughput floor $af_s/(1 - bf_s)$ is the **12.6** of Solution 18-04.4(a), and it binds. So $N \ge 12.6$, and **16** as a power of two. Memory: $3 \times 16 \times 2$ = **96** bytes against $2 \times 32 \times 2$ = **128** for two buffers of 32. Worst latency: $333.3 + 100 + 200 + 80$ = **713** µs against 1127 µs. The third buffer wins on both counts here, because it lets the blocks halve; it could not take them below 13 samples, however long the service latency allowed.

### Solution 18-04.6

(a) $(2 + 6.25) \times 10^6/(100 \times 10^6)$ = **0.0825**.

(b) $0.35 \times 0.0825$ = **0.0289**: about 2.9% of the CPU's cycles.

### Solution 18-04.7

(a) Without bursts: $4096 \times 3$ = **12 288** cycles. With bursts of four: $4096 \times 2 + 4096/4$ = **9216** cycles.

(b) $1 - 9216/12\,288$ = **25** % saved: the arbitration cycles fall from one per word to one per four words.

### Solution 18-04.8

(a) The buffer starts at offset 0x14 = 20 in its line and ends at byte offset $20 + 599 = 619$ from that line's start, in the line $\lfloor 619/32\rfloor = 19$ after it: **20** lines, of which the first and last are shared with other data.

(b) Align to 32 bytes and round 600 up to a multiple of 32: **608** bytes (19 lines).

### Solution 18-04.9

(a) $3 \times 10^6/10 = 300\,000$ bytes/s; in 2 ms, **600** bytes.

(b) With 50% margin, more than 900 bytes: **1024** bytes.

### Solution 18-04.10

(a) CPU: $4 \times 10^6/(48 \times 10^6)$ = **83.3** ms. DMA: $10^6/4 = 250\,000$ words × 2 cycles $= 500\,000$ cycles, **10.42** ms.

(b) CPU: $3.3 \times 5 \times 10^{-3} \times 0.0833$ = **1.375** mJ. DMA: $3.3 \times 1.5 \times 10^{-3} \times 0.01042$ = **51.6** µJ.

(c) A factor of **26.7**. Most of it comes from the shorter time (word transfers, 8 times fewer cycles); the lower current while the CPU sleeps contributes the remaining factor of 3.3. The assumption that matters most is the current during DMA: if the MCU cannot enter a low-power state while its DMA runs (some cannot, or must keep a fast clock and the bus matrix on), the saving shrinks to the time ratio alone.

### Solution 18-04.11

(a) $bf_s = 2 \times 10^{-6} \times 200\,000 = 0.4 < 1$: yes.

(b) $N \ge (15 + 40) \times 10^{-6} \times 200\,000/0.6$ = **18.3**, so **32** samples (0.16 ms per block), $2 \times 32 \times 2$ = **128** bytes.

(c) $\rho = 200\,000/(64 \times 10^6) = 0.003125$; stall $\approx 0.4 \times 0.003125$ = **0.125** %: negligible.

(d) The timing bound is not the binding constraint here; the FFT's frequency resolution, $f_s/N$, is. With $N$ = 32 the bins are 6.25 kHz wide, too coarse for most vibration analysis. Choose $N$ from the resolution needed (for example 1024 samples for 195 Hz bins, 4 KiB for two buffers) and confirm that processing still fits: $15 + 2 \times 1024 = 2063$ µs against a block time of 5120 µs. Contention can be ignored; a separate bank would only matter at much higher rates.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 18-04.1a | per-byte interrupt load | 44.6 | % |
| 18-04.1b | DMA block load | 2.33 | % |
| 18-04.2a | 32-bit transfers | 375 | — |
| 18-04.2b | 16-bit transfers | 750 | — |
| 18-04.3a | head | 219 | — |
| 18-04.3b | unread with tail 200 | 19 | bytes |
| 18-04.3c | unread with tail 230 | 245 | bytes |
| 18-04.4a | smallest block, no latency | 12.6 | samples |
| 18-04.4b | smallest block with 100 µs | 18.9 | samples |
| 18-04.4c | chosen block | 32 | samples |
| 18-04.4d | worst latency, two buffers | 1127 | µs |
| 18-04.5a | deadline bound, three buffers | 8.2 | samples |
| 18-04.5f | throughput floor, three buffers | 12.6 | samples |
| 18-04.5b | chosen block, three buffers | 16 | samples |
| 18-04.5c | memory, three buffers | 96 | bytes |
| 18-04.5d | memory, two buffers | 128 | bytes |
| 18-04.5e | worst latency, three buffers | 713 | µs |
| 18-04.6a | DMA port occupancy | 0.0825 | — |
| 18-04.6b | CPU stall fraction | 0.0289 | — |
| 18-04.7a | cycles without bursts | 12288 | cycles |
| 18-04.7b | cycles with bursts | 9216 | cycles |
| 18-04.7c | saving | 25 | % |
| 18-04.8a | cache lines touched | 20 | — |
| 18-04.8b | aligned, padded size | 608 | bytes |
| 18-04.9a | bytes between services | 600 | bytes |
| 18-04.9b | ring size | 1024 | bytes |
| 18-04.10a | CPU copy time | 83.3 | ms |
| 18-04.10b | DMA copy time | 10.42 | ms |
| 18-04.10c | CPU copy energy | 1.375 | mJ |
| 18-04.10d | DMA copy energy | 51.6 | µJ |
| 18-04.10e | energy ratio | 26.7 | — |
| 18-04.11a | smallest block | 18.3 | samples |
| 18-04.11b | chosen block | 32 | samples |
| 18-04.11c | SRAM for two buffers | 128 | bytes |
| 18-04.11d | contention stall | 0.125 | % |
