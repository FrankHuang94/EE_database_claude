# Solutions 18-03 · Interrupts, Exceptions and Timers

Problems: [18-03 problem set](../problems/18-03-problems.md) · Chapter: [18-03](../chapters/18-03-interrupts-exceptions-timers.md). Every number below is recomputed by [verify_18_03.py](../verify/verify_18_03.py).

---

## Solutions

### Solution 18-03.1

(a) External interrupts start at exception 16: $16 + 45$ = **61**, at offset $61 \times 4 = 244$ = **0xF4**.

(b) SysTick is exception 15: offset $15 \times 4$ = **0x3C**.

(c) HardFault has the fixed priority −1, more urgent than any configurable priority (0 is the most urgent configurable value). Only NMI (−2) and Reset (−3) can preempt it.

### Solution 18-03.2

(a) $400\,000/9$ = **44 444** bytes, and interrupts, per second. Load: $44\,444 \times 80/(16 \times 10^6)$ = **22.2** %.

(b) Use DMA for the transfer (18-04) with an interrupt per message; or, if the controller has a FIFO, interrupt per several bytes; or raise the clock. On a Cortex-M0+ (15-cycle entry) the fixed overhead is a large part of each interrupt.

### Solution 18-03.3

(a) $48 \times 10^6 \times 0.01 - 1$ = **479 999**.

(b) $2^{24}/(48 \times 10^6)$ = **349.5** ms.

(c) $72\,000 - 1$ = **71 999**.

### Solution 18-03.4

(a) $2^2$ = **4** preemption levels, each with $2^1$ = **2** subpriorities.

(b) Group 1 = 0b01 in bits 7:6, subpriority 1 = 1 in bit 5: 0b0110 0000 = **0x60**.

(c) Only bits 7:5 exist: 0x47 = 0b0100 0111 reads back as **0x40**, group 1, subpriority 0. The low bits were silently dropped, so priorities must be written left-justified.

### Solution 18-03.5

IRQ3 and IRQ7 have equal priority 0x40, more urgent than the running 0x80, so one of them preempts IRQ5 at once: the lower exception number, **IRQ3**. IRQ2 (0x80) pends while IRQ3 runs; it is less urgent than IRQ3 and IRQ7 and only equal to IRQ5, so it cannot preempt either. When IRQ3 returns, IRQ7 is pending at 0x40, more urgent than IRQ5: it **tail-chains**. When IRQ7 returns, the pending IRQ2 (0x80) is not more urgent than the interrupted IRQ5 (0x80), so **IRQ5 resumes** and finishes; then IRQ2 runs (tail-chained from IRQ5's return). Order of completion: IRQ3, IRQ7, IRQ5, IRQ2.

### Solution 18-03.6

(a) $2/20 + 4/40 + 10/100 + 15/250 = 0.1 + 0.1 + 0.1 + 0.06$ = **0.36**.

(b) $R_A = 2 + 3$ = **5**. $R_B$: $7 \to 7 + \lceil 7/20\rceil 2 = 9 \to 9$: **9**. $R_C$: $13 \to 13 + 2 + 4 = 19 \to 13 + \lceil 19/20\rceil 2 + \lceil 19/40\rceil 4 = 19$: **19**. $R_D$: $18 \to 18 + 2 + 4 + 10 = 34 \to 18 + \lceil 34/20\rceil 2 + \lceil 34/40\rceil 4 + \lceil 34/100\rceil 10 = 18 + 4 + 4 + 10 = 36 \to 36$: **36**.

(c) Yes: 5 ≤ 20, 9 ≤ 40, 19 ≤ 100 and 36 ≤ 250, with large margins. The lab's simulator, with all four requested at the moment a 3 µs critical section starts, reproduces the four values.

### Solution 18-03.7

$R_C$: start at $20 + 8 = 28$: $28 + \lceil 28/50\rceil 5 + \lceil 28/200\rceil 25 = 58$, then $28 + \lceil 58/50\rceil 5 + 25 = 63$, then $28 + \lceil 63/50\rceil 5 + 25 = 63$: **63** µs, 20 µs more than before. B's extra 15 µs pushed C's completion past A's second request at 50 µs, so C now also waits for a second run of A (5 µs). Interference compounds: lengthening one handler can pull in further preemptions.

### Solution 18-03.8

(a) $(PSC + 1)(ARR + 1) = 72 \times 10^6$, with each factor at most 65 536. The smallest divisor $p$ of $72 \times 10^6$ with $72 \times 10^6/p \le 65\,536$ is $p = 1125$ (1099 to 1124 do not divide it): $PSC$ = **1124**, $ARR + 1 = 64\,000$, $ARR$ = **63 999**. (The rounder choice $PSC$ = 7199, $ARR$ = 9999 also works, with 0.1 ms ticks.)

(b) $ARR + 1$ would have to be $72 \times 10^6$, far beyond a 16-bit register.

### Solution 18-03.9

(a) $84 \times 10^6/2^{10}$ = **82 031** Hz, about 82 kHz.

(b) $16 \times 10^6/2^8$ = **62 500** Hz, hundreds of times faster than the frequencies at which flicker is perceptible, and also above the audible range, which matters if the LED driver's inductor could sing.

### Solution 18-03.10

(a) Modulo $2^{32}$: $0x0000\,2710 - 0xFFFF\,F000 = 0x1000 + 0x2710 = 0x3710$ = **14 096** ticks, 14.096 ms.

(b) One revolution is 2 pulses, $2 \times 14.096 = 28.192$ ms, so the speed is $60/0.028192$ = **2128** RPM.

### Solution 18-03.11

(a) The shortest timeout, at 40 kHz, must be at least $2 \times 0.5 = 1.0$ s: prescaler × reload ≥ $1.0 \times 40\,000$ = **40 000**.

(b) With reload ≤ 4095, the prescaler must be at least $40\,000/4095 = 9.8$, so the smallest allowed is **16**, with reload $40\,000/16$ = **2500**.

(c) At the slow end, 24 kHz: $40\,000/24\,000$ = **1.67** s after the last kick.

### Solution 18-03.12

(a) CFSR = 0x0000 8200 has bit 9 (**PRECISERR**: a precise data bus error, so the stacked PC is the faulting instruction) and bit 15 (**BFARVALID**: BFAR holds the address). HFSR = 0x4000 0000 is bit 30, **FORCED**: the BusFault was not enabled, so it escalated to HardFault.

(b) The SRAM ends at $0x2000\,0000 + 192 \times 1024 = 0x2003\,0000$. BFAR is **4** bytes past the end.

(c) A read or write just beyond the end of SRAM, with a word-sized step past the last address: typically an array index or pointer that ran off the end of a buffer placed at the top of SRAM, or a stack that **underflowed** upward past its top (popping more than was pushed, possibly from a corrupted frame). Next: disassemble the instruction at 0x0800 4A1E (which register held the address), check the map file for what sits at the top of SRAM, and look at the stacked LR for the caller.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 18-03.1a | exception number of IRQ45 | 61 | — |
| 18-03.1b | its vector offset | 0xF4 | — |
| 18-03.1c | SysTick vector offset | 0x3C | — |
| 18-03.2a | I²C byte interrupts per second | 44444 | 1/s |
| 18-03.2b | CPU load | 22.2 | % |
| 18-03.3a | reload for 10 ms at 48 MHz | 479999 | — |
| 18-03.3b | longest period at 48 MHz | 349.5 | ms |
| 18-03.3c | reload for 1 ms at 72 MHz | 71999 | — |
| 18-03.4a | preemption levels | 4 | — |
| 18-03.4b | subpriorities | 2 | — |
| 18-03.4c | byte for group 1, subpriority 1 | 0x60 | — |
| 18-03.4d | read-back of 0x47 | 0x40 | — |
| 18-03.6a | utilization | 0.36 | — |
| 18-03.6b | R_A | 5 | µs |
| 18-03.6c | R_B | 9 | µs |
| 18-03.6d | R_C | 19 | µs |
| 18-03.6e | R_D | 36 | µs |
| 18-03.7a | R_C with the larger B | 63 | µs |
| 18-03.8a | smallest prescaler | 1124 | — |
| 18-03.8b | matching auto-reload | 63999 | — |
| 18-03.9a | highest 10-bit PWM frequency | 82031 | Hz |
| 18-03.9b | 8-bit PWM at 16 MHz | 62500 | Hz |
| 18-03.10a | ticks between captures | 14096 | — |
| 18-03.10b | fan speed | 2128 | RPM |
| 18-03.11a | required prescaler × reload | 40000 | — |
| 18-03.11b | prescaler | 16 | — |
| 18-03.11c | reload | 2500 | — |
| 18-03.11d | longest undetected hang | 1.67 | s |
| 18-03.12a | BFAR beyond the end of SRAM | 4 | bytes |
