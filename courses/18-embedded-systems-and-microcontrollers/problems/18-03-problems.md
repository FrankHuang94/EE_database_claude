# Problems 18-03 · Interrupts, Exceptions and Timers

Chapter: [18-03](../chapters/18-03-interrupts-exceptions-timers.md) · Worked solutions: [18-03 solutions](../solutions/18-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Cortex-M (Armv7-M) unless stated: a smaller priority value is more urgent; entry and return each take 12 cycles and tail-chaining 6 at zero wait states. Response times use the recurrence of §3.4 with all times in µs. Timers count up from 0 to ARR unless stated. Problems marked *(lab)* can be checked with `labs/18-03-lab/irqtime.py` or the lab firmware.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 18-03.1 [A]

**Vectors.** (a) What is the exception number of external interrupt 45, and at what byte offset in the vector table is its handler's address? (b) At what offset is SysTick's? (c) Why can no configurable priority make an interrupt preempt the HardFault handler?

### Problem 18-03.2 [A]

**I²C load.** An I²C bus at 400 kHz transfers bytes back to back, 9 clock cycles per byte (8 data bits and an acknowledge), with one interrupt per byte costing 80 cycles in total on a 16 MHz Cortex-M0+. (a) How many interrupts per second, and what CPU load? (b) What would you change if the load were too high?

### Problem 18-03.3 [A]

**SysTick.** (a) What reload value gives a 10 ms tick at 48 MHz? (b) What is the longest SysTick period at 48 MHz? (c) What reload gives 1 ms at 72 MHz?

### Problem 18-03.4 [B]

**Three priority bits.** A part implements 3 priority bits (bits 7:5) and PRIGROUP splits them into 2 group bits and 1 subpriority bit. (a) How many preemption levels and subpriorities? (b) Give the byte for group 1, subpriority 1. (c) Software writes 0x47 to an interrupt's priority register. What does it read back, and which priority does the interrupt get?

### Problem 18-03.5 [B]

**Who runs when?** IRQ5 (priority 0x80) is running. In the same cycle IRQ7 and IRQ3 (both 0x40) become pending; shortly after, while IRQ3 runs, IRQ2 (0x80) becomes pending. List the order in which the handlers run and finish, saying where preemption and tail-chaining occur.

### Problem 18-03.6 [B]

**Four interrupts.** *(lab)* A has $C$ = 2, $T$ = 20; B has $C$ = 4, $T$ = 40; C has $C$ = 10, $T$ = 100; D has $C$ = 15, $T$ = 250 (µs, most urgent first, deadlines equal to periods). Main code disables interrupts for at most 3 µs. (a) What is the utilization? (b) Find every worst-case response time. (c) Are all deadlines met?

### Problem 18-03.7 [B]

**A handler grows.** *(lab)* In Example 18-03.3 (8 µs blocking), interrupt B's handler grows from 10 to 25 µs. What is C's new worst-case response time, and why did it grow by more than B's 15 µs?

### Problem 18-03.8 [B]

**A one-second timer.** A 16-bit timer with a 16-bit prescaler runs from 72 MHz. (a) Find the smallest prescaler that gives an exact 1 s update period, and the matching auto-reload. (b) Why can no prescaler of 0 work?

### Problem 18-03.9 [B]

**PWM frequency against resolution.** (a) What is the highest edge-aligned PWM frequency with 10-bit resolution from an 84 MHz timer clock? (b) An LED dimmer on a 16 MHz MCU wants 8-bit resolution. What PWM frequency results, and is it fast enough to avoid visible flicker?

### Problem 18-03.10 [B]

**A tachometer.** A fan's tachometer gives 2 pulses per revolution. A 32-bit timer counts at 1 MHz and captures rising edges. Two consecutive captures are 0xFFFF F000 and 0x0000 2710. (a) How many ticks between them? (b) What is the fan speed in revolutions per minute?

### Problem 18-03.11 [C]

**Designing a watchdog.** An independent watchdog's oscillator may run from 24 to 40 kHz. The prescaler can be 4, 8, 16, …, 256 and the reload 1 to 4095. The main loop's worst-case kick interval is 0.5 s, and the design rule is a shortest timeout of at least twice that. (a) What prescaler × reload product is needed? (b) Choose the smallest prescaler that works and its reload. (c) What is the longest time a hang can go undetected after the last kick?

### Problem 18-03.12 [C]

**Reading a fault.** A product returns from the field with a saved fault record: CFSR = 0x0000 8200, HFSR = 0x4000 0000, BFAR = 0x2003 0004 and stacked PC = 0x0800 4A1E. The MCU has 192 KiB of SRAM at 0x2000 0000. (a) Decode CFSR and HFSR. (b) Where is BFAR relative to the SRAM? (c) What are the likely causes, and what would you look at next?

### Problem 18-03.13 [C]

**Write a capture handler that measures long periods.** *(code)* A 16-bit timer counts at 1 MHz and captures rising edges; signals of 3 Hz to 50 Hz (periods up to 333 000 ticks) must be measured, so the count is extended with a software overflow counter. The timer's interrupt can be pending for both an overflow (update) and a capture at once; the handler runs within 20 ms of the earliest pending event, and edges are at least 20 ms apart. (a) Write `int capx_isr(capx_t *s, int update, int capture, uint16_t ccr, uint32_t *period)`, which keeps the state in `s` and returns 1 with the period when one is available. (b) When both flags are pending, how does the handler decide whether the edge came before or after the overflow, and why does that need the handler to run within half a counter period? (c) Why is the period computed with unsigned 32-bit subtraction? Check your code with `labs/18-03-lab/host/capx_test.c`, which simulates 200 000 edges with random latencies.

---

## Objective coverage

| Learning objective (chapter 18-03) | Problems |
|---|---|
| 1. Polling, interrupts and CPU load | 2 |
| 2. The exception model | 1, 5, 12 |
| 3. Priorities, groups and masking | 1, 4, 5 |
| 4. Worst-case response times | 6, 7 |
| 5. Handler design and faults | 2, 12, 13 |
| 6. Timers, PWM and watchdogs | 3, 8, 9, 10, 11, 13 |
