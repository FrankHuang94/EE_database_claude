# Problems 18-04 · DMA and Data Movement

Chapter: [18-04](../chapters/18-04-dma-and-data-movement.md) · Worked solutions: [18-04 solutions](../solutions/18-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Processing a block of $N$ samples takes $a + bN$; $L$ is the worst service latency before processing starts. A UART byte with 8N1 framing is 10 bits. Bus transfers take one cycle per access unless stated. Problems marked *(lab)* can be checked with `labs/18-04-lab/dmasim.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 18-04.1 [A]

**SPI receive.** An SPI link receives at 10 Mbit/s on a 168 MHz MCU. (a) With one interrupt per byte at 60 cycles, what is the CPU load? (b) With DMA blocks of 64 bytes and a 200-cycle handler per block?

### Problem 18-04.2 [A]

**Transfer counts.** How many DMA transfers move a 1500-byte Ethernet frame with 32-bit transfers, and with 16-bit transfers?

### Problem 18-04.3 [A]

**Reading a circular DMA.** A 256-byte circular receive buffer's DMA remaining-count register reads 37. (a) Where is the write position? (b) How many bytes are unread if the consumer's tail is 200? (c) If the tail is 230?

### Problem 18-04.4 [B]

**Audio blocks.** *(lab)* Audio arrives at 48 kHz. Processing a block takes $200\ \mu\text{s} + 5\ \mu\text{s} \times N$. (a) What is the smallest safe ping-pong block with no service latency? (b) With $L$ = 100 µs? (c) Choose a power of two for (b) and give its worst latency.

### Problem 18-04.5 [B]

**When is the third buffer worth it?** *(lab)* For Problem 18-04.4(b), find the smallest power-of-two block with three buffers, and compare memory (16-bit samples) and worst latency with the two-buffer design.

### Problem 18-04.6 [B]

**Two streams on one port.** An ADC (2 M items/s) and an SPI flash read (6.25 M items/s) are written by DMA into the same SRAM bank on a 100 MHz bus, one cycle per item. The CPU accesses that bank in 35% of its cycles. (a) What fraction of the port's cycles does the DMA use? (b) Estimate the CPU's stall fraction.

### Problem 18-04.7 [B]

**Bursts.** Moving 4096 words costs, per transfer, one arbitration cycle, one read and one write. A burst of four words needs only one arbitration. (a) How many cycles without and with bursts? (b) What fraction is saved?

### Problem 18-04.8 [B]

**Cache lines.** A Cortex-M7 (32-byte lines) DMA buffer of 600 bytes starts at 0x2001 0014. (a) How many lines does it touch? (b) What aligned, padded size should it be declared with?

### Problem 18-04.9 [B]

**A fast UART.** A UART at 3 Mbaud (8N1) feeds a circular DMA; the consumer is serviced at least every 2 ms. (a) How many bytes can arrive between services? (b) Choose a power-of-two ring size with at least 50% margin.

### Problem 18-04.10 [C]

**Copying with the CPU or the DMA.** A 1 MB block must be copied on a 48 MHz MCU at 3.3 V. A CPU copy loop takes 4 cycles per byte with the MCU drawing 5 mA. A DMA copy with word transfers takes 2 bus cycles per word, during which the CPU sleeps and the MCU draws 1.5 mA. (a) How long does each take? (b) How much energy does each use? (c) By what factor does DMA save energy, and what assumption matters most?

### Problem 18-04.11 [C]

**Designing a sensor stream.** A vibration sensor delivers 200 kS/s of 16-bit samples to an MCU at 64 MHz. Each block runs an FFT costing $15\ \mu\text{s} + 2\ \mu\text{s} \times N$. Other interrupts can delay processing by up to 40 µs. The stream's DMA writes one sample per bus cycle into SRAM, and the CPU spends 40% of its cycles on memory accesses. (a) Is a ping-pong design possible? (b) Find the smallest power-of-two block for two buffers, and its SRAM. (c) Estimate the CPU slowdown from contention if the buffers share the CPU's SRAM bank (bus at 64 MHz). (d) What would you change?

---

## Objective coverage

| Learning objective (chapter 18-04) | Problems |
|---|---|
| 1. When DMA pays | 1, 10 |
| 2. DMA controller anatomy | 2, 3, 7 |
| 3. Buffer sizing | 4, 5, 9, 11 |
| 4. Bus contention | 6, 11 |
| 5. Caches and ordering | 8 |
| 6. Lock-free hand-over | 3, 9 |
