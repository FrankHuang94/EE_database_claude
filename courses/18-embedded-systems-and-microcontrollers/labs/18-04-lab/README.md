# Lab 18-04 · Buffers, Bus Contention and a Lock-Free Ring

Chapter: [18-04 · DMA and Data Movement](../../chapters/18-04-dma-and-data-movement.md)

## Objective

- Size ping-pong and multi-buffer schemes from processing time and service latency, and watch overruns appear exactly below the bound in a simulation.
- Measure, in a cycle-level model, how much a DMA master slows a CPU on a shared memory port, and compare with the estimate $p\rho$.
- Run a lock-free single-producer, single-consumer ring buffer between an interrupt handler and `main` on QEMU's emulated Cortex-M4, through the 32-bit index wrap, and with a deliberately full buffer.

## Background

A block of $N$ samples is safe with $k$ buffers when $L + a + bN \le (k - 1)N/f_s$ (§3.3). A DMA master occupying a port for a fraction $\rho$ of cycles stalls a CPU that uses that port in a fraction $p$ of its cycles by about $p\rho$ (§3.4). A ring buffer with one writer per index needs no critical section, only a barrier between writing data and publishing the index (§3.3).

QEMU's `mps2-an386` board has no general-purpose DMA controller for the firmware to drive, so the DMA side is modelled in Python; the firmware plays the DMA completion interrupt's role with SysTick.

## Files

- `dmasim.py`: `pingpong_min_block`, `simulate_pingpong`, `bus_sim`, `stall_estimate`, `irq_load`, `transfers`, `ring_head`, `ring_unread`, `cache_lines`.
- `fw/ring.h`: the lock-free ring buffer (power-of-two size, free-running 32-bit indices, `dmb` barriers); `fw/main.c`: the test; `fw/startup.c`, `fw/nvic.h`, `fw/link.ld`, `fw/semihost.h` from Labs 18-02 and 18-03.
- `fwrun.py`: builds `fw/` with Lab 18-02's wrapper and runs it on QEMU.
- `18-04-dma-lab.ipynb`: the guided notebook.

## Procedure

1. **Block size.** For Example 18-04.2 (1 MS/s, $a$ = 20 µs, $b$ = 0.6 µs, $L$ up to 25 µs), predict the smallest safe block for two and three buffers. Simulate 20 000 blocks with service latencies uniform from 5 to 25 µs at 64, 112 and 128 samples (two buffers) and 64 samples (three buffers).
2. **Latency against memory.** For $L$ from 0 to 60 µs, plot the power-of-two block, memory and worst latency for two and three buffers.
3. **Contention.** For $p$ = 0.3 and DMA periods of 25, 10 and 4 cycles, predict the CPU's stall fraction; run `bus_sim` for $10^6$ cycles with both policies.
4. **The ring on the core.** Predict what happens when the consumer stops while the producer continues. Run the firmware at `-O2` and `-O0`.
5. **Cache lines.** Predict the lines touched by 1000 bytes at 0x2000 0008 and by 600 bytes at 0x2001 0014; check.

## Expected results

- Part 1: bounds of 112.5 (two buffers) and 32.1 (three). Overruns at 64 and 112 with two buffers (about 191 of 20 000 at 112), none at 128, none at 64 with three buffers.
- Part 2: the third buffer halves the block and roughly halves the latency for the same safety.
- Part 3: stall fractions of about 1.2%, 3.0% and 7.5%, within 1% of $p\rho$; the two policies agree here because the DMA never has more than one request waiting.
- Part 4: `TEST PASSED` at both levels: 5000 items in order through the index wrap, then exactly 64 items accepted by the full ring, later drops counted, and the ring drains intact.
- Part 5: 32 and 20 lines.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 18-04.a | overruns at N = 112, two buffers, 20 000 blocks | 191 | — |
| Lab 18-04.b | overruns at N = 128, two buffers | 0 | — |
| Lab 18-04.c | simulated stall with a 25-cycle DMA period | 1.21 | % |
| Lab 18-04.d | simulated stall with a 10-cycle DMA period | 3.02 | % |

## Discussion

1. Why do overruns at $N$ = 112 appear only occasionally rather than on every block?
2. Why does the ring buffer use free-running 32-bit indices instead of indices reduced modulo the size?
3. What would break in the ring buffer if the `dmb` in `ring_put` were removed on a core with a write buffer, and why does the test not catch it on QEMU?

## Answers

1. The bound uses the worst service latency, 25 µs. The simulator draws latencies uniformly from 5 to 25 µs, and $N$ = 112 fails only when the latency exceeds $112(1 - 0.6) - 20 = 24.8$ µs, which happens in about 1% of blocks. A design sized for typical latency fails rarely, which is the worst kind of failure to debug.
2. With free-running indices, $\text{head} - \text{tail}$ is the number of items stored, from 0 to the size, so full and empty are distinguishable without wasting a slot or keeping a shared count; unsigned arithmetic makes the wrap at $2^{32}$ harmless. Only the array access reduces the index modulo the (power-of-two) size.
3. The consumer could see the new head before the data write reached memory and read a stale item. QEMU executes memory accesses in program order and has no write buffer to reorder them, so the test passes with or without the barrier; the barrier is required by the architecture's memory model, not by this emulator. This is a case where only reasoning, not testing, shows correctness.

## Optional hardware

On a board with DMA, stream an ADC (or a UART at high baud rate) into ping-pong buffers, toggle a GPIO while each block is processed, and add a deliberate busy loop in a higher-priority interrupt to push the service latency past the bound: count overruns by checking the DMA's current-buffer flag at the end of processing.
