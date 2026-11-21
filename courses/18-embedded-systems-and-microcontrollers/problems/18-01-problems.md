# Problems 18-01 · Microcontroller Architecture

Chapter: [18-01](../chapters/18-01-microcontroller-architecture.md) · Worked solutions: [18-01 solutions](../solutions/18-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Addresses are byte addresses in hexadecimal, written with or without a space between 16-bit halves. The memory map is the Cortex-M default of §3.3; bit-band aliases follow §3.3 (Armv7-M). Wait states follow $\text{WS} = \lceil f\,t_{acc}\rceil - 1$, and the effective CPI is the first-order model of §3.5 relative to the zero-wait-state core. "MIPS" means millions of instructions per second. Problems marked *(lab)* can be checked with the lab's `mcuarch.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 18-01.1 [A]

**Which region?** In which region of the Cortex-M default memory map does each address lie, and what would you expect to find there: (a) 0x0800 1234, (b) 0x2000 8000, (c) 0x4001 3800, (d) 0xE000 E100, (e) 0x6000 0000?

### Problem 18-01.2 [A]

**Sizes and the reset vector.** (a) An MCU has SRAM1 at 0x2000 0000–0x2001 BFFF and SRAM2 at 0x2001 C000–0x2001 FFFF. Give their sizes in KiB. (b) Its 1 MiB flash starts at 0x0800 0000. What is its last address? (c) The first eight bytes of its vector table are, in address order, `00 80 01 20 C1 01 00 08`. The core is little-endian. Give the initial main stack pointer and the reset handler's address, and say where the handler's first instruction is. How large is the SRAM below the initial stack pointer?

### Problem 18-01.3 [A]

**Register addresses.** A USART has base address 0x4000 4400 and registers SR, DR, BRR and CR1 at offsets 0x00, 0x04, 0x08 and 0x0C. (a) Give each register's address. (b) Bit 13 of CR1 enables the USART. Give the bit-band alias that sets it.

### Problem 18-01.4 [B]

**Decoding an alias.** A debugger shows a write to address 0x2201 0A84. (a) Which region is this? (b) Which SRAM byte and bit does it change? (c) Is the target byte the start of a word?

### Problem 18-01.5 [A]

**Wait states at low voltage.** At 1.8 V an MCU's flash has an access time of 40 ns. (a) How many wait states are needed at 32, 64 and 100 MHz? (b) What is the highest clock with zero wait states?

### Problem 18-01.6 [B]

**What the cache buys.** Code with an average instruction size of 2.5 bytes runs from a flash with 128-bit lines and 4 wait states at 150 MHz, with 0.15 taken branches per instruction and line-aligned targets. (a) Check that a line feeds sequential code at full speed. (b) Find the effective CPI and MIPS with a prefetch buffer only. (c) Repeat with a cache that holds 90% of branch targets.

### Problem 18-01.7 [B]

**Diminishing returns.** For the flash of Example 18-01.2 ($t_{acc}$ = 33.3 ns, prefetch only, 0.12 taken branches per instruction, 16-bit code): (a) find the MIPS at 90, 120 and 150 MHz; (b) show that, at any clock, the delivered rate can never exceed $1/(b\,t_{acc})$, and evaluate the bound. What does this say about raising the clock without a cache?

### Problem 18-01.8 [B]

**A PLL from a 25 MHz crystal.** *(lab)* Many boards with Ethernet use a 25 MHz crystal. The PLL has the constraints of Example 18-01.3 (phase-detector frequency 1–2 MHz, VCO 100–432 MHz, $50 \le N \le 432$, $P \in \{2, 4, 6, 8\}$, $2 \le Q \le 15$). (a) Show that 100 MHz with an exact 48 MHz output is impossible. (b) Find every configuration for 96 MHz with exact 48 MHz.

### Problem 18-01.9 [B]

**Clock accuracy.** (a) A real-time clock runs from a 32.768 kHz crystal that is 20 ppm fast. How many seconds does it gain per day and per year? (b) A 48 MHz internal RC oscillator is trimmed to ±1%. Express that in ppm and compare it with the USB full-speed tolerance.

### Problem 18-01.10 [B]

**Bus bandwidth.** A DMA engine moves three ADC channels, each sampled at 2 MS/s with 16-bit results, into SRAM over a 32-bit AHB at 80 MHz, one transfer per sample. What fraction of the SRAM port's cycles does it use, and why does a split SRAM help the core?

### Problem 18-01.11 [B]

**Energy at the top of each band.** *(lab)* A task of $5 \times 10^5$ instructions (16-bit code, 0.12 taken branches per instruction, the 33.3 ns flash, prefetch only) runs every 50 ms. Running, the MCU draws $1.0\ \text{mA} + 30\ \mu\text{A/MHz} \times f$ at 3.0 V; asleep, 2 µA. Find the energy per period at 30, 60, 90 and 120 MHz, and the best clock.

### Problem 18-01.12 [C]

**When does the next band pay?** For the energy model of Example 18-01.5 with taken-branch rate $b$, access time $t_{acc}$, dynamic coefficient $k$ (A/Hz), fixed current $I_0$ and sleep current $I_s$, compare running at the top of band $w$ ($f = (w + 1)/t_{acc}$) with the top of band $w + 1$. (a) Show that band $w + 1$ uses less energy per period if and only if

$$
I_0 - I_s > \frac{(w + 1)(w + 2)\,k\,b}{(1 - b)\,t_{acc}} .
$$

(b) Evaluate the threshold for $w$ = 0, 1 and 2 with $k$ = 40 µA/MHz, $b$ = 0.12 and $t_{acc}$ = 33.3 ns, and check Example 18-01.5's result.

### Problem 18-01.13 [C]

**Price against porting cost.** MCU X costs \$1.20 at volume but needs six engineer-months more firmware work (porting drivers and RTOS support) than MCU Y at \$1.45, which runs the team's existing code. An engineer-month costs \$20 000 fully loaded. (a) Above what lifetime volume is X cheaper? (b) Name two costs this calculation leaves out.

### Problem 18-01.14 [C]

**Headline against delivered.** A 480 MHz Cortex-M7 part runs a large application by execute-in-place from external quad-SPI flash through its instruction cache. A cache miss fills a 32-byte line: 20 clocks of command, address and dummy cycles, then the data four bits per clock, at a 133 MHz flash clock. The application misses 5 times per 1000 instructions; take the core's CPI as 1 otherwise. (a) Find the miss penalty in core cycles, the effective CPI and the delivered MIPS. (b) Repeat with an octal (8-bit) flash at the same clock and overhead. (c) What would you ask a vendor who quotes "480 MHz"?

### Problem 18-01.15 [B]

**Choosing an architecture.** For each application, choose among Armv6-M (Cortex-M0+), Armv7E-M with FPU (Cortex-M4F) and Armv8-M Mainline with TrustZone (Cortex-M33), and justify in two sentences: (a) a disposable temperature logger that wakes once a minute; (b) a motor controller running field-oriented control at 20 kHz with floating-point PI loops; (c) a smart lock that stores credentials and accepts firmware updates over the air.

---

## Objective coverage

| Learning objective (chapter 18-01) | Problems |
|---|---|
| 1. MCU blocks against an application processor | 1, 10 |
| 2. Cortex-M and RISC-V cores | 14, 15 |
| 3. Memory map, registers, bit-banding | 1, 2, 3, 4 |
| 4. Wait states and effective instruction rate | 5, 6, 7, 11, 12, 14 |
| 5. PLLs, clock sources and resets | 2, 8, 9 |
| 6. Part selection | 11, 13, 15 |
