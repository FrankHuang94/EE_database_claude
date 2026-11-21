# Lab 18-03 · Interrupts on a Real (Emulated) NVIC, and Timing by Analysis

Chapter: [18-03 · Interrupts, Exceptions and Timers](../../chapters/18-03-interrupts-exceptions-timers.md)

## Objective

- Run interrupt handlers on QEMU's emulated Cortex-M4 and observe the NVIC's behaviour: implemented priority bits, preemption, tail-chaining, BASEPRI and PRIMASK masking, deferral to PendSV, the stacked frame and EXC_RETURN, SysTick, and a recovered bus fault.
- Compute worst-case response times with the fixed-priority recurrence and check them against a discrete-event simulation.
- Size timers, PWM and watchdogs.

## Background

A pending exception preempts only if its priority value is strictly smaller than the running one; equal priorities wait and then tail-chain (§3.3). BASEPRI masks priority values greater than or equal to its own; PRIMASK masks all configurable exceptions. On entry the core stacks eight registers and puts EXC_RETURN in LR (§3.2). An unmapped data access raises a precise BusFault, which escalates to HardFault when BusFault is not enabled (§3.5). Worst-case response times follow $R_i = C_i + B_i + \sum_{j \in hp(i)}\lceil R_i/T_j\rceil C_j$ (§3.4).

The firmware is built with Lab 18-02's toolchain wrapper (clang 18, ld.lld) and run on QEMU's `mps2-an386` board. QEMU models the NVIC's logic faithfully but not the timing of a real chip: it implements all 8 priority bits (real parts commonly implement 3 or 4, some more) and is not cycle-accurate, so latency must come from Arm's documents, not from the emulator.

## Files

- `fw/startup.c` (vector table with 32 external interrupts), `fw/main.c` (the self-checking tests), `fw/nvic.h` (NVIC, SCB and SysTick registers, masking intrinsics), plus `link.ld`, `semihost.h` and `regbits.h` from Lab 18-02.
- `fwrun.py`: `build_and_run` (build `fw/` and run it on QEMU) and `priority_bits`.
- `irqtime.py`: `response_time`, `utilization`, `simulate` (discrete-event, with an optional blocking section and an execution trace), `cpu_load`, `timer_period`, `find_psc_arr`, `pwm_resolution_bits`, `capture_delta`, `systick_reload`, `watchdog_timeout`.
- `18-03-interrupts-lab.ipynb`: the guided notebook.

## Procedure

1. **Priority bits.** Predict what the priority byte reads back after writing 0xFF on a part with 4 implemented bits. Run the firmware and read QEMU's answer.
2. **Order.** IRQ0 (0xC0) pends IRQ1 (0x40) and IRQ2 (0xC0) from inside its handler. Predict the event log (1 = IRQ0 enters, 2 = IRQ0 leaves, 3 = IRQ1, 4 = IRQ2); run.
3. **Masking and deferral.** Predict which pended interrupts run under BASEPRI = 0x80 and under PRIMASK, and when PendSV (lowest priority) runs after being pended from a priority-0x20 handler. The firmware's checks pass only if the predictions of §3.3 hold.
4. **The fault.** Predict CFSR, HFSR and BFAR after a read of 0x5000 0000, which is unmapped on this board; run.
5. **Response times.** Compute the worst-case response times of Example 18-03.3, then simulate them at the critical instant. Predict $R_C$ when B's handler grows from 10 to 25 µs; compute and simulate.
6. **Timers.** Tabulate edge-aligned PWM frequency against resolution for an 84 MHz clock; find PSC and ARR for a 1 s period from 72 MHz.

## Expected results

- Part 1: QEMU reads back 0xFF: all **8** priority bits are implemented in the emulator. A part with 4 bits would read 0xF0.
- Part 2: the event log 1, 3, 2, 4: IRQ1 preempts IRQ0 in the middle, IRQ2 waits and tail-chains after IRQ0 returns.
- Part 3: BASEPRI 0x80 holds IRQ2 (0xC0) and passes IRQ1 (0x40); the held interrupt runs as soon as BASEPRI is cleared; PRIMASK holds everything; PendSV runs only after the pending handler returns. EXC_RETURN is 0xFFFF FFF9, and SysTick delivers its interrupts.
- Part 4: CFSR = 0x0000 8200 (PRECISERR and BFARVALID), HFSR = 0x4000 0000 (FORCED), BFAR = 0x5000 0000; the handler skips the instruction and the program continues.
- Part 5: 13, 23 and 43 µs, reproduced by the simulator; with B at 25 µs, $R_C$ = 63 µs.
- Part 6: 10-bit PWM up to 82 kHz; PSC = 1124 and ARR = 63 999 for 1 s.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 18-03.a | priority bits implemented by QEMU's NVIC | 8 | — |
| Lab 18-03.b | event log, packed one byte per event | 0x01030204 | — |
| Lab 18-03.c | CFSR after the unmapped read | 0x00008200 | — |
| Lab 18-03.d | BFAR after the unmapped read | 0x50000000 | — |
| Lab 18-03.e | R_C with B's handler at 25 µs | 63 | µs |

## Discussion

1. Why must priority values be written left-justified in the byte, and what goes wrong if code written for an 8-bit emulator uses values like 0x05 on a 4-bit chip?
2. Why does the simulator need the blocking section to start at the same instant as all the requests to reproduce the recurrence's worst case?
3. The fault handler advances the stacked PC to skip the faulting instruction. Why is that acceptable in this lab and dangerous in a product?

## Answers

1. Unimplemented bits are the *low* bits and read as zero. On a 4-bit part, 0x05 becomes 0x00, the most urgent priority, and 0x0F becomes 0x00 too: priorities that were distinct on the emulator collapse into one, and the most urgent level at that. Writing values like 0x50 and 0xF0 (or using CMSIS's `NVIC_SetPriority`, which shifts by the implemented width) keeps them distinct on every part.
2. The recurrence bounds the worst case over all arrival patterns; that worst case (the critical instant) is when the interrupt is requested just as the longest blocking starts and every more urgent one is requested together. Any other alignment gives a response time no longer than that, so a simulation with arbitrary offsets can only under-estimate it.
3. The lab caused the fault deliberately and knows the instruction has no side effect worth repeating. In a product, the fault means the program's state is already wrong (a bad pointer, a corrupted stack); skipping the instruction continues with garbage. A product's fault handler records the cause and resets, or enters a safe state.

## Optional hardware

On a Cortex-M development board, toggle a GPIO at the start and end of each handler and watch them on a logic analyzer: measure entry latency (request pin to first toggle), preemption and tail-chaining, and compare with Arm's 12-cycle figure at your clock and wait states. Read the NVIC priority register after writing 0xFF to find your part's implemented bits.
