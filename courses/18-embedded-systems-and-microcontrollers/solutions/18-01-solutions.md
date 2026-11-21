# Solutions 18-01 · Microcontroller Architecture

Problems: [18-01 problems](../problems/18-01-problems.md) · Chapter: [18-01](../chapters/18-01-microcontroller-architecture.md). Every number below is recomputed by [verify_18_01.py](../verify/verify_18_01.py).

---

## Solutions

### Solution 18-01.1

- (a) 0x0800 1234 is in the **Code** region (0x0000 0000–0x1FFF FFFF): on many parts the internal flash lives at 0x0800 0000 and is also mapped at address 0 after reset.
- (b) 0x2000 8000 is in **SRAM**, 32 KiB above its base: on-chip data memory.
- (c) 0x4001 3800 is in the **Peripheral** region: the register block of some peripheral (which one is in the vendor's memory map).
- (d) 0xE000 E100 is on the **private peripheral bus**, inside the system control space at 0xE000 E000; this address is the NVIC's first interrupt set-enable register (18-03). It is the same on every Cortex-M3/M4 part.
- (e) 0x6000 0000 is the first address of the **External RAM** region: memory behind an external memory controller, if the part has one.

### Solution 18-01.2

(a) SRAM1: $0x2001\,BFFF - 0x2000\,0000 + 1 = 0x1\,C000 = 114\,688$ bytes = **112** KiB. SRAM2: $0x2001\,FFFF - 0x2001\,C000 + 1 = 0x4000$ = **16** KiB. Together they are a contiguous 128 KiB.

(b) $0x0800\,0000 + 0x10\,0000 - 1$ = **0x080FFFFF**.

(c) Little-endian words: bytes `00 80 01 20` form **0x20018000**, the initial main stack pointer; bytes `C1 01 00 08` form 0x0800 01C1, the reset handler's address with the Thumb bit set. The handler's first instruction is at **0x080001C0**. The stack is full-descending: the first push writes just below 0x2001 8000, so the stack starts at the top of the lowest $0x1\,8000$ bytes = **96** KiB of SRAM.

### Solution 18-01.3

(a) SR **0x40004400**, DR **0x40004404**, BRR **0x40004408**, CR1 **0x4000440C**.

(b) CR1's byte offset from the peripheral bit-band base is 0x440C. Bit 13 of the word is bit 5 of byte 0x440D. The alias is $0x4200\,0000 + 32 \times 0x440D + 4 \times 5 = 0x4200\,0000 + 0x8\,81A0 + 0x14$ = **0x420881B4**. Treating the word as a whole gives the same: $32 \times 0x440C + 4 \times 13 = 0x8\,8180 + 0x34 = 0x8\,81B4$.

### Solution 18-01.4

(a) 0x2201 0A84 is inside the SRAM bit-band **alias** region, 0x2200 0000–0x23FF FFFF.

(b) Its offset from 0x2200 0000 is 0x1 0A84 = 68 228. Dividing by 32 gives byte offset 2132 = 0x854, remainder 4; dividing the remainder by 4 gives bit **1**. The target is bit 1 of the byte at **0x20000854**.

(c) 0x854 = 2132 is divisible by 4, so **yes**: the write sets or clears bit 1 of the 32-bit word at 0x2000 0854.

### Solution 18-01.5

(a) $f\,t_{acc}$ = 1.28, 2.56 and 4.00 at 32, 64 and 100 MHz, so WS = **1**, **2** and **3**. At 100 MHz four 10 ns cycles exactly equal the 40 ns access; a real table adds margin, so expect 4 there in practice.

(b) Zero wait states need $f\,t_{acc} \le 1$: $f \le 1/40\ \text{ns}$ = **25** MHz.

### Solution 18-01.6

(a) A 16-byte line holds $16/2.5$ = **6.4** instructions on average, at least $\text{WS} + 1 = 5$, so straight-line code is never starved; equivalently $(\text{WS} + 1)s/L = 0.78 < 1$.

(b) $\text{CPI} = 1 + 0.15 \times 4$ = **1.60**; $150/1.6$ = **93.75** MIPS.

(c) $\text{CPI} = 1 + 0.15 \times 0.10 \times 4$ = **1.06**; $150/1.06$ = **141.5** MIPS.

### Solution 18-01.7

(a) 90 MHz: WS 2, CPI 1.24, **72.6** MIPS. 120 MHz: WS 3, CPI 1.36, **88.2** MIPS. 150 MHz: WS 4, CPI 1.48, **101.4** MIPS.

(b) The wait states satisfy $\text{WS} \ge f\,t_{acc} - 1$, and the model's CPI is at least $1 + b\,\text{WS}$ (the sequential term can only add to it). So the time per instruction obeys

$$
\frac{\text{CPI}}{f} \ge \frac{1 + b(f\,t_{acc} - 1)}{f} = \frac{1 - b}{f} + b\,t_{acc} > b\,t_{acc} ,
$$

and the rate is below $1/(b\,t_{acc}) = 1/(0.12 \times 33.3\ \text{ns})$ = **250** MIPS at every clock. Each taken branch costs about one flash access time in seconds, whatever the clock, so without a cache a faster clock buys less and less: the flash, not the core, sets the ceiling. (The real limit is lower still: above 240 MHz a 16-byte line holds fewer than WS + 1 instructions, and even straight-line code starves.)

### Solution 18-01.8

(a) $f_{SYS} = f_{VCO}/P$ with $f_{VCO} \le 432$ MHz allows only $P$ = 2 ($f_{VCO}$ = 200 MHz) or $P$ = 4 (400 MHz). An exact 48 MHz needs $f_{VCO} = 48Q$, but $200/48 = 4.17$ and $400/48 = 8.33$ are not integers. **Impossible**.

(b) 96 MHz: $f_{VCO}$ = 192 MHz ($P$ = 2, $Q$ = 4) or 384 MHz ($P$ = 4, $Q$ = 8). The phase-detector range 1–2 MHz needs $13 \le M \le 25$, and $N = f_{VCO}M/25$ must be an integer, which requires $M$ = 25 (a 1 MHz phase detector). The configurations are $(M, N, P, Q)$ = (25, 192, 2, 4) and (25, 384, 4, 8): **2** in all. The lab's search confirms both and finds 26 configurations for 100 MHz alone, none with an exact 48 MHz.

### Solution 18-01.9

(a) $20 \times 10^{-6} \times 86\,400$ = **1.728** s per day; $\times 365.25$ = **631** s per year, about 10.5 minutes. Watches and meters calibrate the crystal (or adjust in software against temperature) for this reason.

(b) ±1% = ±**10 000** ppm, **4** times the ±2500 ppm USB full-speed allows. The RC oscillator alone is not enough; the design needs a crystal or clock recovery from the host's start-of-frame packets.

### Solution 18-01.10

$3 \times 2 \times 10^6 = 6 \times 10^6$ transfers per second against $80 \times 10^6$ bus cycles per second: **7.5**% of the SRAM port's cycles, more with arbitration and the peripheral-side reads. Each DMA write that collides with a core access to the same SRAM port delays one of them. With the SRAM split into banks on separate matrix ports, the DMA buffers go in one bank and the core's stack and data in another, and the two never contend.

### Solution 18-01.11

$E(f) = V(I_0 + kf)\,t_{act} + VI_s(T - t_{act})$ with $t_{act} = N(1 + 0.12\,\text{WS})/f$:

| Clock | WS | Cycles | Energy per period |
|---|---|---|---|
| 30 MHz | 0 | 500 000 | **95.2** µJ |
| 60 MHz | 1 | 560 000 | **78.6** µJ |
| 90 MHz | 2 | 620 000 | **76.7** µJ |
| 120 MHz | 3 | 680 000 | **78.5** µJ |

The best is **90** MHz, the top of the two-wait-state band. The larger fixed current (1.0 mA against Example 18-01.5's 0.6 mA) pushes the optimum to a faster clock: finishing sooner saves more.

### Solution 18-01.12

(a) Write the energy per period as

$$
E = V\big[(I_0 - I_s)\,t_{act} + kf\,t_{act}\big] + VI_sT, \qquad t_{act} = \frac{N\,\text{CPI}}{f} ,
$$

so $E = VN\,\text{CPI}\,[(I_0 - I_s)/f + k] + VI_sT$. Within a band CPI is constant and $E$ falls with $f$ (if $I_0 > I_s$), so the best point of band $w$ is its top, $f = (w + 1)/t_{acc}$, where $\text{CPI} = 1 + bw$. With $A = (I_0 - I_s)t_{acc}$,

$$
E_w - VI_sT = VN(1 + bw)\Big[\frac{A}{w + 1} + k\Big] .
$$

Band $w + 1$ is better when $(1 + b(w + 1))\big[A/(w + 2) + k\big] < (1 + bw)\big[A/(w + 1) + k\big]$, that is

$$
A\Big[\frac{1 + bw}{w + 1} - \frac{1 + b(w + 1)}{w + 2}\Big] > kb .
$$

The bracket is $\dfrac{(1 + bw)(w + 2) - (1 + bw + b)(w + 1)}{(w + 1)(w + 2)} = \dfrac{1 - b}{(w + 1)(w + 2)}$, so the condition is $A > (w + 1)(w + 2)kb/(1 - b)$, and dividing by $t_{acc}$ gives the result. ∎

(b) $kb/((1 - b)t_{acc}) = (4 \times 10^{-11} \times 0.12)/(0.88 \times 3.333 \times 10^{-8}) = 0.1636$ mA. The thresholds are 2, 6 and 12 times that: **0.327**, **0.982** and **1.964** mA for $w$ = 0, 1, 2. Because the thresholds rise with $w$, the energies at the band tops fall and then rise, and the best band is the first $w$ whose threshold exceeds $I_0 - I_s$. In Example 18-01.5, $I_0 - I_s$ = 0.597 mA exceeds 0.327 (so 60 MHz beats 30) but not 0.982 (so 90 MHz does not beat 60): the optimum is 60 MHz, as the sweep found.

### Solution 18-01.13

(a) X saves \$0.25 per unit against \$120 000 of extra engineering: break-even at $120\,000/0.25$ = **480 000** units. Above that, X is cheaper.

(b) Any two of: the schedule delay of six engineer-months (lost revenue or a missed design window), the risk of new bugs in ported code, maintaining two code bases if other products stay on Y, re-qualification or certification of the new platform, tool or RTOS licences, and supply-chain risk or second-sourcing.

### Solution 18-01.14

(a) Data: $32 \times 8/4 = 64$ clocks; total $20 + 64 = 84$ flash clocks, $84/133\ \text{MHz}$ = 631.6 ns = **303.2** core cycles at 480 MHz. $\text{CPI} = 1 + 0.005 \times 303.2$ = **2.52**, and the delivered rate is $480/2.516$ = **190.8** MIPS, 40% of the headline.

(b) Octal: 32 data clocks, 52 in all, 391 ns = **187.7** core cycles; $\text{CPI}$ = **1.94**, **247.6** MIPS.

(c) Where does the benchmark's code run (TCM, internal flash, external flash), with what cache size and hit rate, on what workload? Is the external interface octal and double-data-rate? Can time-critical code and data be placed in TCM? Ask for delivered performance on the customer's code size and memory configuration.

### Solution 18-01.15

- (a) **Cortex-M0+** (Armv6-M): the logger does a few thousand instructions a minute; the smallest core minimizes leakage, area and price, and occasional arithmetic needs no FPU.
- (b) **Cortex-M4F** (Armv7E-M): field-oriented control needs Clarke and Park transforms, PI loops and space-vector PWM every 50 µs. Single-cycle multiply-accumulate, saturating arithmetic and a single-precision FPU make this a few thousand cycles per period, easily inside a 100 MHz budget of 5000 cycles.
- (c) **Cortex-M33** (Armv8-M Mainline): TrustZone isolates credentials and the firmware-update verifier in the Secure world from the application and its network stack, so a bug in the application cannot read keys or install unsigned firmware (18-08, 18-11).

### Solution 18-01.16

(a) Cortex-M4: **12** cycles, and the handler can be an ordinary C function because the hardware has already saved what the calling convention requires. RV32I: $4 + 16$ = **20** cycles.

(b) RV32E: $4 + 10$ = **14** cycles.

(c) $4 + 4$ = **8** cycles, faster than the Cortex-M4, because only the registers the handler uses are saved.

(d) Entry fraction = rate × cycles / clock: Cortex-M4 $2 \times 10^5 \times 12/(48 \times 10^6)$ = **5.0** %; RV32I **8.33** %; RV32E **5.83** %; RV32I with the attribute **3.33** %.

(e) On Cortex-M the entry cost is fixed by the hardware; on RISC-V it depends on the ISA variant, the interrupt controller (the CLIC's hardware vectoring and register-saving options) and the compiler's conventions, so a quoted latency is meaningless without them. Ask which handler type was measured, and whether the figure includes the register saves.

### Solution 18-01.17

(a) **2.1** V: it is above the ADC's 2.0 V and the flash's 1.71 V minimum, so the part never runs out of specification, and below the 2.2 V sag, with a margin of **0.1** V. 1.7 V would let the ADC run below its rating; 2.5 V would reset the device on every burst.

(b) The sag is deeper than the 2.2 V assumed: a cold or ageing cell has a higher internal resistance (18-09), or the burst is longer. Fixes: add or enlarge a reservoir capacitor at the load so that it supplies the burst (18-09 §3.6); reduce or spread the peak current (a lower transmit power, staggering the radio and the sensor); or, if the ADC is not used during bursts, accept the 1.7 V threshold while bursts last.

(c) The flags are sticky: they accumulate until cleared, so without clearing them the next startup cannot tell which event caused it. Reading them tells the firmware (and a field log) whether a reset came from the pin, the power-on circuit, a brown-out, the watchdog, a software request or a lockup, which is the first clue in diagnosing field failures.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 18-01.2a | SRAM1 size | 112 | KiB |
| 18-01.2b | SRAM2 size | 16 | KiB |
| 18-01.2c | last flash address | 0x080FFFFF | — |
| 18-01.2d | initial MSP | 0x20018000 | — |
| 18-01.2e | first instruction of the reset handler | 0x080001C0 | — |
| 18-01.2f | SRAM below the initial stack pointer | 96 | KiB |
| 18-01.3a | SR address | 0x40004400 | — |
| 18-01.3b | DR address | 0x40004404 | — |
| 18-01.3c | BRR address | 0x40004408 | — |
| 18-01.3d | CR1 address | 0x4000440C | — |
| 18-01.3e | alias for CR1 bit 13 | 0x420881B4 | — |
| 18-01.4a | target byte | 0x20000854 | — |
| 18-01.4b | target bit | 1 | — |
| 18-01.5a | wait states at 32 MHz | 1 | — |
| 18-01.5b | wait states at 64 MHz | 2 | — |
| 18-01.5c | wait states at 100 MHz | 3 | — |
| 18-01.5d | highest zero-wait clock | 25 | MHz |
| 18-01.6a | instructions per line | 6.4 | — |
| 18-01.6b | CPI, prefetch only | 1.60 | — |
| 18-01.6c | MIPS, prefetch only | 93.75 | MIPS |
| 18-01.6d | CPI with cache | 1.06 | — |
| 18-01.6e | MIPS with cache | 141.5 | MIPS |
| 18-01.7a | MIPS at 90 MHz | 72.6 | MIPS |
| 18-01.7b | MIPS at 120 MHz | 88.2 | MIPS |
| 18-01.7c | MIPS at 150 MHz | 101.4 | MIPS |
| 18-01.7d | asymptotic rate | 250 | MIPS |
| 18-01.8a | configurations for 96 MHz | 2 | — |
| 18-01.8b | configurations for 100 MHz alone | 26 | — |
| 18-01.9a | RTC gain per day | 1.728 | s |
| 18-01.9b | RTC gain per year | 631 | s |
| 18-01.9c | RC tolerance | 10000 | ppm |
| 18-01.9d | ratio to the USB tolerance | 4 | — |
| 18-01.10 | SRAM port use | 7.5 | % |
| 18-01.11a | energy at 30 MHz | 95.2 | µJ |
| 18-01.11b | energy at 60 MHz | 78.6 | µJ |
| 18-01.11c | energy at 90 MHz | 76.7 | µJ |
| 18-01.11d | energy at 120 MHz | 78.5 | µJ |
| 18-01.11e | best clock | 90 | MHz |
| 18-01.12a | threshold, band 0 to 1 | 0.327 | mA |
| 18-01.12b | threshold, band 1 to 2 | 0.982 | mA |
| 18-01.12c | threshold, band 2 to 3 | 1.964 | mA |
| 18-01.13 | break-even volume | 480000 | units |
| 18-01.14a | quad-SPI miss penalty | 303.2 | cycles |
| 18-01.14b | quad-SPI CPI | 2.52 | — |
| 18-01.14c | quad-SPI delivered rate | 190.8 | MIPS |
| 18-01.14d | octal miss penalty | 187.7 | cycles |
| 18-01.14e | octal CPI | 1.94 | — |
| 18-01.14f | octal delivered rate | 247.6 | MIPS |
| 18-01.16a | Cortex-M4 entry | 12 | cycles |
| 18-01.16b | RV32I entry | 20 | cycles |
| 18-01.16c | RV32E entry | 14 | cycles |
| 18-01.16d | RV32I entry with the interrupt attribute | 8 | cycles |
| 18-01.16e | CPU fraction, Cortex-M4 | 5.0 | % |
| 18-01.16f | CPU fraction, RV32I | 8.33 | % |
| 18-01.16g | CPU fraction, RV32E | 5.83 | % |
| 18-01.16h | CPU fraction, attribute | 3.33 | % |
| 18-01.17a | brown-out threshold | 2.1 | V |
| 18-01.17b | margin to the sag | 0.1 | V |
