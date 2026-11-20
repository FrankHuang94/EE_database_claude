# Lab 14-05 · Single-Cycle Datapath and Control

Chapter: [14-05 Single-Cycle Datapath and Control](../../chapters/14-05-single-cycle-datapath.md)

## Objective

Run, read and extend a complete single-cycle RV32I processor written in Verilog. Check it against the course's instruction-set simulator by comparing every register write, and explore with a timing model which instruction class sets the clock.

## Background

The datapath elements (§3.1), the datapath built class by class (§3.2), the control unit (§3.3) and the timing of one long cycle (§3.4).

## Tools

[Icarus Verilog](https://steveicarus.github.io/iverilog/) (`iverilog`, `vvp`) for simulation, as in Course 08. Regenerating the test program also needs the LLVM tools of [Lab 14-03](../14-03-lab/README.md#tools), but the generated files are committed, so the testbench runs without them.

## Files

| File | Contents |
|---|---|
| [rv32_single.v](rv32_single.v) | The core: PC, next-PC logic, multiplexers and branch comparator; instantiates the modules below |
| [rv32_decoder.v](rv32_decoder.v) | Main decoder and ALU decoder (the table of §3.3) |
| [rv32_immgen.v](rv32_immgen.v) | Immediate generator |
| [rv32_alu.v](rv32_alu.v) | ALU |
| [rv32_regfile.v](rv32_regfile.v) | Register file: 32 × 32 bits, two read ports, one write port, x0 = 0 |
| [rv32_single_tb.v](rv32_single_tb.v) | Self-checking testbench with instruction and data memories |
| [program.s](program.s) | The test program: an array sum and a recursive `fib(10)` |
| [make_program.py](make_program.py) | Builds `program.hex`, `data.hex` and `expected.vh` with LLVM and the Python simulator |
| [14-05-datapath-lab.ipynb](14-05-datapath-lab.ipynb) | Notebook: timing explorer, control-table check, and the trace comparison |

The core implements RV32I except byte and halfword loads and stores, FENCE and the CSR instructions; ECALL, EBREAK and any unsupported opcode halt it.

## Procedure

1. **Run the core.** From this directory:

   ```bash
   iverilog -g2012 -o sim.vvp rv32_single_tb.v rv32_single.v rv32_decoder.v rv32_immgen.v rv32_alu.v rv32_regfile.v
   ```

   ```bash
   vvp -n sim.vvp +trace
   ```

   *Predict first:* how many cycles will the program take? (Use the counts from 14-03.)
2. **Compare traces (notebook, Part 3).** `+trace` writes every register write to `trace.txt`. Compare it with the Python simulator's list of writes.
3. **Timing explorer (notebook, Part 1).** Change the component delays and see which class sets the clock.
4. **Control table (notebook, Part 2).** Print the decoder's outputs for every opcode and compare with §3.3.
5. **Extend the core.** Add `lwr rd, rs1, rs2` (Problem 14-05.11): one decoder row, using an unused opcode such as 0001011 (custom-0). Write a test program that uses it with `.insn r 0x0b, 2, 0, rd, rs1, rs2` in the assembly, and check it in the testbench.

## Expected results

| Step | Quantity | Expected |
|---|---|---|
| 1 | Testbench | `sum = 115, fib(10) = 55, 1923 cycles (CPI = 1), 1281 register writes`, then `TEST PASSED` |
| 2 | Trace | All 1281 register writes match the Python simulator in order, address and value |
| 3 | Timing | The load sets the clock at 730 ps with §3.4's delays; with a 120 ps data memory, still the load at 650 ps |
| 4 | Control | The decoder's outputs match the table of §3.3 for all nine instruction classes |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 14-05.a | cycles for the test program | 1923 | — |
| Lab 14-05.b | register writes | 1281 | — |
| Lab 14-05.c | stored array sum | 115 | — |
| Lab 14-05.d | run time at 730 ps | 1.404 | µs |

*These are recomputed by [verify_14_05.py](../../verify/verify_14_05.py), which rebuilds the program, runs the Python simulator, runs this core in Icarus Verilog, and compares the two register-write traces entry by entry.*

## Discussion questions

1. The testbench counts cycles and register writes, not just the final results. What kind of bug would the counts catch that the results might miss?
2. Why does the core stop when it sees an unsupported opcode instead of ignoring it?
3. The data memory is read on every cycle, even for `add`. What would you change to save that energy, and what would it cost?

### Answers

1. A bug that changes the path but not the answer. For example, if a taken branch were mispredicted as not taken and then recovered by an extra jump, or if a loop ran one extra iteration that happened not to change the sum. Counting instructions and writes, and better still comparing the full trace, catches divergence anywhere, not only in the final state.
2. Silently executing an unknown instruction as something else would let the run continue with wrong state, the hardest kind of bug to find. A real processor raises an illegal-instruction exception (14-10); halting is this core's equivalent, and the testbench reports it as a failure.
3. Add a read-enable signal from the decoder (1 only for loads) and gate the memory's clock or enable with it, as in Problem 14-05.12. The cost is one more control signal and a gate. In a real design the memory's read must also not start speculatively, which a pipelined design (where the enable arrives later) handles naturally.

## Optional hardware extension

Synthesize the core for an FPGA (08-12's flow), replacing the testbench memories with block RAM initialized from `program.hex` and `data.hex`. Read the timing report: which path does the tool find critical, and how does it compare with §3.4's model? Block RAMs usually have a synchronous read, which forces a design change. Why, and where does the extra cycle go?
