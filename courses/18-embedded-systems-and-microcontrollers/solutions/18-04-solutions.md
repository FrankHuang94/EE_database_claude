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

With three buffers the deadline condition gives $N \ge 300 \times 10^{-6} \times 48\,000/(2 - 0.24)$ = **8.2**, but the CPU must also keep up on average: the throughput floor $af_s/(1 - bf_s)$ is the **12.6** of Solution 18-04.4(a), and it binds. So $N \ge 12.6$, and **16** as a power of two. Memory: $3 \times 16 \times 2$ = **96** bytes against $2 \times 32 \times 2$ = **128** for two buffers of 32. Worst latency: $333.3 + 100 + 200 + 80$ = **713** µs against 1127 µs. The third buffer wins on both counts here, because it lets the blocks halve; it could not take them below 13 samples, however short the service latency.

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

### Solution 18-04.12

(a) TX: the CPU writes the buffer; **clean** the buffer's lines (write the dirty data to memory); `DSB`; start the DMA. RX: **clean and invalidate** (or just invalidate, if no line is shared) the buffer's lines before starting, so that no dirty line can later be evicted over the DMA's data; start the DMA; when it completes, `DSB`, **invalidate** the lines again (the CPU may have speculatively refetched them meanwhile), then read.

(b) The buffer runs from 0x2000 0410 to $0x2000\,0410 + 199 = 0x2000\,04D7$. Lines are 0x20 bytes: from the line at 0x2000 0400 to the one at 0x2000 04C0, $\lfloor 0x4D7/32\rfloor - \lfloor 0x410/32\rfloor + 1 = 38 - 32 + 1$ = **7** lines. The first, 0x2000 0400–0x2000 041F, also holds `rx_count`.

(c) Two failures. If the handler has incremented `rx_count`, its line is dirty in the cache; invalidating the buffer's lines after the transfer throws the new count away. If instead the driver *cleans* that line while the DMA is running (or the cache evicts it), the cache writes its stale copy of bytes 0x410–0x41F over the data the DMA has just written. Either corrupts data only when the timing is unlucky.

(d) `__attribute__((aligned(32))) uint8_t rx[224];`: 200 bytes rounded up to whole lines, $7 \times 32$ = **224** bytes, that no other variable shares. Alternatively, place DMA buffers in a non-cacheable region set up with the MPU, or in the M7's DTCM, which the cache does not cover.

### Solution 18-04.13

(a) `count++` in the handler and `count--` in `main` are both read-modify-writes of the same variable. If the receive interrupt arrives between `main`'s load of `count` and its store, `main` writes back the old value minus one and the handler's increment is lost: `count` now under-reports the data in the buffer, and bytes sit unread until another byte arrives. The handler cannot be interrupted by `main`, so the error only ever goes one way: each lost increment leaves the count one lower for good, until the writer starts overwriting data the count says is free. It is the race of 18-02 §3.6 in a different place.

(b) `volatile` makes each access happen, but `count--` is still a load, a subtract and a store, and an interrupt can fall between them.

(c) Drop the shared count and use free-running head and tail indices, each written by only one side (the lab's `ring.h`): the handler writes `head` only, `main` writes `tail` only, and the number of bytes is `head - tail`, computed by whichever side needs it.

```c
#define N 64u                                   /* power of two */
volatile uint8_t buf[N]; volatile uint32_t head, tail, overruns;
void UART_IRQHandler(void)                      /* producer: writes head only */
{
    uint8_t c = UART->DR;
    if (head - tail != N) { buf[head % N] = c; __asm__ volatile("" ::: "memory"); head++; }
    else overruns++;                            /* full: count the loss */
}
int get(uint8_t *c)                             /* consumer: writes tail only */
{
    if (head == tail) return 0;
    *c = buf[tail % N]; __asm__ volatile("" ::: "memory"); tail++;
    return 1;
}
```

On one core the compiler barriers are enough (§3.3).

### Solution 18-04.14

(a) `put`: write the data, then a `DMB` (a release), then store the new head; without it the M7 may see the new head before the data and read a stale record. `get`: load the head, then a `DMB` (an acquire), then read the slot; without it the M7 may read the slot before it has seen the head that made it valid. Then a second `DMB` before storing the new tail; without it the M4 may see the slot freed and overwrite it before the M7's read of it has completed.

(b) On one core the core observes its own accesses in order and an interrupt falls between instructions, so the slot's read always completes before the tail store. Between two cores, each core's accesses can become visible to the other in a different order than they were issued, so the order must be enforced on both sides.

(c) The M7 must clean its cache lines for anything it writes (the tail) before publishing, and invalidate the lines of the head and the slots before reading them, because the M4 writes memory directly and the M7's cache would otherwise serve stale copies; the line rules of Problem 12 apply, and head, tail and data should sit in separate lines. The simpler alternative is to place the ring in a region the MPU marks non-cacheable (or shareable, where the cache supports it), at the cost of slower access.

(d) Reason from the memory model, then test on the real part under stress: run both cores at full rate for hours with sequence numbers in the records and a checker on the consumer, vary the timing (other bus traffic, interrupts, cache pressure), and confirm that removing a barrier makes the checker fail, so the test is known to be able to detect the bug.

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
| 18-04.12a | cache lines touched by the RX buffer | 7 | — |
| 18-04.12b | padded buffer size | 224 | bytes |
