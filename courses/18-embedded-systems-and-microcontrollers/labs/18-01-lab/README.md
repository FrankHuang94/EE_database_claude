# Lab 18-01 · Memory Maps, Wait States and Clock Trees

Chapter: [18-01 · Microcontroller Architecture](../../chapters/18-01-microcontroller-architecture.md)

## Objective

Work through a microcontroller's architecture numerically:

- decode the Cortex-M memory map, peripheral register addresses and bit-band aliases;
- compute flash wait states and measure their cost with a cycle-level fetch simulator, with and without a cache;
- configure a PLL by exhaustive search under its constraints;
- find the clock that minimizes energy per task for a duty-cycled workload;
- score candidate parts and test how robust the choice is.

## Background

The Cortex-M address space is a fixed 4 GiB map (§3.3); a register's address is its peripheral's base plus its offset, and on Armv7-M each bit of the first megabyte of SRAM and peripherals has an alias word. A flash with access time $t_{acc}$ needs $\lceil f\,t_{acc}\rceil - 1$ wait states (§3.5); prefetch hides them for sequential code, and each taken branch that misses pays them. The PLL multiplies its reference by $N/M$ and divides by $P$ and $Q$ (§3.6). Energy per task trades fixed current against the CPI that wait states add (Example 18-01.5).

## Files

- `mcuarch.py`: `region`, `region_size`, `reg_addr`, `bitband_alias`, `wait_states`, `max_freq`, `make_program`, `simulate_fetch`, `cpi_analytic`, `pll_search`, `task_energy`, `duty_cycle_energy`, `weighted_scores`, `gate`.
- `18-01-mcu-architecture-lab.ipynb`: the guided notebook.

## Procedure

1. **Addresses.** Predict the bit-band alias of bit 13 of the word at 0x4001 1008; compute it and decode it back to (address, bit).
2. **Wait states.** For a 33.3 ns flash, predict the instruction rate at 30 and 31 MHz with prefetch only; sweep 1–180 MHz and plot the sawtooth.
3. **The fetch simulator.** Simulate 16-bit code with line-aligned branch targets, then mixed 16/32-bit code with unaligned targets, at 0–7 wait states, and compare with `cpi_analytic`.
4. **Caches.** Run a loop-heavy program (code in 512 bytes) and a random-branch program (64 KiB) with 0, 16 and 64 cache lines.
5. **PLL.** Find every configuration from an 8 MHz crystal for 168, 120 and 180 MHz, with and without an exact 48 MHz output.
6. **Energy.** Repeat Example 18-01.5 with a fixed current of 0.2 mA and of 2 mA, and find the best clock each time.

## Expected results

- Part 1: 0x4222 0134, decoding back to 0x4001 1008 bit 13 (byte 0x4001 1009, bit 5).
- Part 2: 30.0 instructions per µs at 30 MHz but 27.7 at 31 MHz: one more megahertz costs a wait state.
- Part 3: the simulator matches the formula exactly for aligned 16-bit code; at 5 wait states, unaligned branch targets raise the CPI by about 13% (about 1.81 against 1.60), 30% 32-bit instructions with aligned targets cost almost nothing (about 1.62), and both together raise it by about 20% (about 1.92).
- Part 4: a 64-line cache holds the loop program entirely and removes the branch stalls; it barely helps the random-branch program.
- Part 5: five configurations for 168 MHz with 48 MHz, five for 120 MHz with 48 MHz, none for 180 MHz with 48 MHz.
- Part 6: 30 MHz is best at 0.2 mA and 120 MHz at 2 mA: the larger the fixed current, the more it pays to race to idle.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 18-01.a | alias of bit 13 of 0x4001 1008 | 0x42220134 | — |
| Lab 18-01.b | instruction rate at 31 MHz | 27.7 | per µs |
| Lab 18-01.c | configurations for 120 MHz + 48 MHz | 5 | — |
| Lab 18-01.d | best clock at 0.2 mA fixed current | 30 | MHz |
| Lab 18-01.e | best clock at 2 mA fixed current | 120 | MHz |

## Discussion

1. Why do vendors publish wait-state tables per voltage range rather than a single access time?
2. Why does a cache help a loop far more than random branching, and what does that imply for interrupt handlers that run rarely?
3. Why is the most energy-efficient clock always at the top of a wait-state band in the model, and what real effects could move it?

## Answers

1. The flash access time grows as the supply falls (weaker sense currents, slower word-line drive), so each voltage range has its own bands; a single number would be either unsafe at low voltage or wasteful at high voltage.
2. A loop re-executes the same few lines, which stay in the cache after the first pass; random branches keep touching new lines. Rarely run code, such as an interrupt handler, is usually not in the cache when it runs, so its first instructions pay the full flash latency: time-critical handlers are placed in SRAM or TCM.
3. Within a band the CPI is fixed, so energy falls as the task finishes sooner. Real effects that move it: dynamic current that is not exactly linear in frequency, voltage scaling (a higher clock may require a higher core voltage), regulator efficiency that varies with load, and peripherals or memories whose current depends on time awake rather than on cycles.

## Optional hardware

Any Cortex-M development board with a debugger shows the real thing: read the reset-cause register, toggle a pin through the bit-band alias and through a read-modify-write, change the flash latency setting and time a loop with the cycle counter (DWT_CYCCNT on Cortex-M3 and above) at several clocks, with the cache or accelerator on and off.
