# Problems 14-11 · I/O, Buses and Interconnect

Chapter: [14-11](../chapters/14-11-io-buses-and-interconnect.md) · Worked solutions: [14-11 solutions](../solutions/14-11-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** UARTs use 8N1 framing (10 bits per byte). KB = 1000 bytes and GB = 10⁹ bytes for bandwidths; KiB = 1024 bytes for buffer sizes. Link bandwidths are per direction unless stated.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 14-11.1 [A]

**A register map.** A device's registers start at 0x4000_2000: CTRL at offset 0x00, STATUS at 0x04, TXDATA at 0x08 and RXDATA at 0x0C. (a) At what address is RXDATA? (b) Why must software read it through a `volatile` pointer, and why must the page be uncacheable?

### Problem 14-11.2 [A]

**A slow UART.** At 9600 baud, how long does one byte take, and what is the maximum throughput in bytes per second?

### Problem 14-11.3 [B]

**How often to poll?** A UART receiving at 115,200 baud has a 16-byte receive FIFO. (a) How often must a polling loop empty it to avoid losing data? (b) At 200 cycles per poll on a 48 MHz microcontroller, what fraction of the CPU does that polling use?

### Problem 14-11.4 [B]

**The crossover.** A driver can poll a device every 10 µs at 100 cycles per poll, or take an interrupt costing 1500 cycles per event. Above what event rate does polling use fewer cycles than interrupts?

### Problem 14-11.5 [B]

**DMA for a large buffer.** A driver must move 64 KiB from a device. Programmed I/O moves 4 bytes per 40 cycles. DMA costs 500 cycles to set up and 1500 for the completion interrupt. (a) Compare the CPU cycles. (b) How many 64-byte cache lines must a driver invalidate if the DMA is not coherent?

### Problem 14-11.6 [B]

**Stalled responses.** The lab's AXI4-Lite subordinate takes $2 + k$ cycles per write when the manager accepts each response $k$ cycles late. (a) How long do 100 writes take at 200 MHz with $k$ = 1, and what is the write throughput? (b) A redesigned subordinate accepts a new write in the same cycle as it completes the previous response, sustaining one write per cycle with $k$ = 0. What throughput does it reach?

### Problem 14-11.7 [B]

**Bus efficiency.** A 128-bit bus runs at 1 GHz. Each 16-beat burst needs 4 extra cycles of address, arbitration and turnaround. Find the peak bandwidth, the efficiency and the delivered bandwidth.

### Problem 14-11.8 [B]

**Scaling a mesh.** Find the average hop count of 4 × 4 and 16 × 16 meshes under uniform traffic, and the average zero-load latency of the 16 × 16 mesh at 4 cycles per hop. By what factor does the bisection bandwidth grow from 4 × 4 to 16 × 16, compared with the number of nodes?

### Problem 14-11.9 [B]

**SSD and GPU links.** Find the per-direction bandwidth of (a) a PCIe 4.0 x4 link, (b) a PCIe 5.0 x4 link, both with 128b/130b encoding, and (c) the raw per-direction bandwidth of a PCIe 7.0 x16 link.

### Problem 14-11.10 [C]

**Keeping a link busy.** An accelerator reads host memory over a link at 64 GB/s with 256-byte requests and 1 µs of round-trip latency. How many requests must be in flight? If the DMA engine supports 64 outstanding requests, what bandwidth does it reach?

### Problem 14-11.11 [C]

**Coalescing with a timeout.** The network port of Example 14-11.2 (83,333 packets per second, 2000 cycles per interrupt, 3 GHz core) coalesces up to 32 packets but fires after at most 50 µs. (a) Which limit triggers the interrupts, and how many interrupts per second result? (b) What fraction of the core do they use? (c) What is the worst-case added latency?

---

## Objective coverage

| Learning objective (chapter 14-11) | Problems |
|---|---|
| 1. Memory-mapped device registers | 1, 2 |
| 2. Polling, interrupts, coalescing and DMA | 3, 4, 5, 11 |
| 3. Valid/ready buses and Little's law | 6, 7, 10 |
| 4. Mesh networks-on-chip | 8 |
| 5. Serial-link bandwidth | 9, 10 |
