# Lab 19-12 · Faults, Scan Chains and Self-Test

Chapter: [19-12 · Design for Test: Scan, BIST and ATPG](../../chapters/19-12-design-for-test.md)

## Objective

- Enumerate, simulate and collapse stuck-at faults, and find small test sets by search.
- Watch random patterns stall on random-pattern-resistant faults.
- Run a Verilog scan chain through shift, capture and unload, and catch an injected fault.
- Build LFSRs and a MISR, and measure aliasing exactly.
- Compare March C− with a shorter memory test on every single fault of a small memory.

## Background

The chapter's §3.1 derives the defect level, §3.2–3.3 cover fault models and test generation, §3.4 scan, and §3.5 BIST (LFSRs, MISRs and March tests).

Files:

- `dft.py`: a `Circuit` class (gate-level evaluation with an optional stuck-at fault on a stem or a fanout branch, the fault list, exhaustive test sets), `equivalence_classes`, `greedy_test_set`, `random_coverage`, `patterns_for_detection`; `defect_level`, `coverage_for_dl`; `scan_cycles`, `test_data_bits`; `lfsr_sequence`, `misr_signature`; `MARCH_C_MINUS`, `march_ops`, `FaultyMemory` (stuck-at, transition and idempotent coupling faults) and `run_march`.
- `scan_reg.v`: an 8-bit register of mux-D scan flip-flops around an incrementer (q + 3), with a parameter that injects a stuck-at-0 on one output bit of the logic.
- `scan_reg_tb.v`: a self-checking testbench that loads four patterns through the chain, captures one cycle each, unloads each response while loading the next pattern, and checks a fault-free and a faulty copy. Run with `iverilog -g2012 -o sim scan_reg_tb.v scan_reg.v && vvp sim` (or `python tools/run_hdl.py` from the repository root).
- `19-12-dft-lab.ipynb`: the procedure below.

## Procedure

1. **Faults and tests.** For c17 and for the consensus circuit of Example 19-12.3, predict the number of faults, the undetectable ones and the minimal test-set size, then compute them (Part 1).
2. **Random patterns.** For a 10-input AND feeding an OR with an XOR of two other inputs, predict the shape of the coverage curve under random patterns; plot it for several seeds (Part 2).
3. **Scan in Verilog.** Predict the number of clock cycles for 4 patterns on the 8-bit chain, and which of the patterns 00, 5A, FF and 80 (hex) catch a stuck-at-0 on bit 2 of the incrementer's output; run the testbench (Part 3).
4. **LFSRs and MISRs.** Find the periods of the 4-bit LFSRs $x^4 + x^3 + 1$ and $x^4 + x^2 + 1$; enumerate every nonzero three-word error stream through a 4-bit MISR and count the ones that alias (Part 4).
5. **Memory test.** Inject every single stuck-at, transition and idempotent coupling fault into an 8-cell memory and run March C− and MATS+ ($\{\Updownarrow(w0); \Uparrow(r0, w1); \Downarrow(r1, w0)\}$) (Part 5).

## Expected results

- Part 1: c17 has 34 faults in 21 equivalence classes, none undetectable, and needs 4 tests; the consensus circuit has 28 faults, 3 of them undetectable (the redundant term), and 4 tests cover the rest.
- Part 2: 9 of the 30 faults are detected within a few patterns; the other 21 need the 10 AND inputs all at 1 (or all but one) with the XOR at 0, a probability of $2^{-11}$ per pattern, so their climb is centred near $1/p \approx 2000$ patterns (about 63 % of them caught by then) and finishes after several thousand.
- Part 3: 44 clock cycles, $P(L + 1) + L$ with $P = 4$, $L = 8$; only pattern 5A detects the fault (5A + 3 = 5D has bit 2 set; the other three sums do not), and the testbench prints TEST PASSED.
- Part 4: periods 15 and 6; 255 of the 4095 nonzero error streams alias, $(2^8 - 1)/(2^{12} - 1)$, close to $2^{-4}$.
- Part 5: March C− detects all 32 stuck-at and transition faults and all 224 coupling faults; MATS+ misses 8 transition faults (every falling transition, because its last write of 0 is never read) and 140 of the 224 coupling faults.

## Discussion

1. Why did pattern 00 fail to catch the stuck-at-0 on bit 2, even though it exercised the incrementer?
2. Why does a 10-input AND resist random patterns, and how would you fix it in a real design?
3. Why does MATS+ miss falling-transition faults, and which element of March C− catches them?
4. A MISR's aliasing probability is about $2^{-n}$. Why is that a weak argument for using a short MISR on a large design?

**Answers.**

1. 00 + 3 = 03, whose bit 2 is 0 anyway: the fault was not activated (the good value equalled the stuck value). A test must drive the faulty line to the opposite of its stuck value.
2. Its output and inputs are observable only when all ten inputs are 1 and the OR's other input is 0, a $2^{-11}$ chance per pattern. A test point (an extra observable flip-flop at a partial AND, or a control point) or deterministic top-up patterns fix it.
3. MATS+ ends with a descending element that writes 0 after reading 1; nothing reads that 0 back, so a cell that cannot fall from 1 to 0 is never caught. March C−'s ⇑(r1, w0) and ⇓(r1, w0) elements are followed by elements that read 0, which detect it.
4. The $2^{-n}$ figure assumes the error stream is random. Real faults produce structured error patterns, and millions of parts are tested, so even a small escape probability adds up. A 32-bit or longer MISR makes aliasing negligible for a few more flip-flops.

## Optional extensions

- Add a second scan chain to `scan_reg.v` and compare cycle counts.
- Write a March element in Verilog against a small register-file model with an injected coupling fault.

## Optional hardware

Any JTAG-equipped development board and an open-source tool such as OpenOCD can read a chip's IDCODE and run boundary-scan SAMPLE; check the board's documentation for the TAP pins.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 19-12.a | testbench clock cycles | 44 | — |
| Lab 19-12.b | patterns detecting the injected fault | 1 | — |
| Lab 19-12.c | transition faults missed by MATS+ | 8 | — |
| Lab 19-12.d | coupling faults missed by MATS+ | 140 | — |
| Lab 19-12.e | coupling faults injected | 224 | — |
| Lab 19-12.f | hard faults in the wide circuit | 21 | — |
| Lab 19-12.g | easy faults in the wide circuit | 9 | — |
| Lab 19-12.h | tests covering the consensus circuit's detectable faults | 4 | — |
| Lab 19-12.i | share of hard faults caught by 2048 patterns | 63 | % |
