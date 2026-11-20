# Lab 14-06 · Pipelining and Hazards

Chapter: [14-06 Pipelining and Hazards](../../chapters/14-06-pipelining-and-hazards.md)

## Objective

Run a five-stage pipelined RV32I core with forwarding, load-use stalls and branch flushing. Confirm that it executes exactly the same register writes as the single-cycle core and the reference simulator. Then check that its cycle count obeys the model $N + 4 + S + 2T$, and use micro-programs to see each hazard appear and disappear.

## Background

The five-stage pipeline (§3.2), data hazards and forwarding (§3.3), control hazards (§3.4) and the performance model (§3.5).

## Tools

Icarus Verilog, as in [Lab 14-05](../14-05-lab/README.md#tools). The notebook's micro-programs also need the LLVM tools of [Lab 14-03](../14-03-lab/README.md#tools).

## Files

| File | Contents |
|---|---|
| [rv32_pipe.v](rv32_pipe.v) | The pipelined core: pipeline registers, forwarding unit, hazard unit, branch resolution in EX |
| [rv32_decoder.v](rv32_decoder.v) | Lab 14-05's decoder plus `uses_rs1` and `uses_rs2` for the hazard logic |
| [rv32_regfile.v](rv32_regfile.v) | Register file with write-before-read (a WB write is visible to ID in the same cycle) |
| [rv32_immgen.v](rv32_immgen.v), [rv32_alu.v](rv32_alu.v) | Unchanged from Lab 14-05 |
| [rv32_pipe_tb.v](rv32_pipe_tb.v) | Self-checking testbench: results, register writes, cycles, stalls and flushes |
| [program.s](program.s), [make_program.py](make_program.py) | Lab 14-05's program, and the generator that also computes the cycle model from the simulator's trace |
| [14-06-pipeline-lab.ipynb](14-06-pipeline-lab.ipynb) | Notebook: micro-programs and a pipeline diagram |

## Procedure

1. **Run the core.** From this directory:

   ```bash
   iverilog -g2012 -I . -o sim.vvp rv32_pipe_tb.v rv32_pipe.v rv32_decoder.v rv32_immgen.v rv32_alu.v rv32_regfile.v
   ```

   ```bash
   vvp -n sim.vvp +trace
   ```

   *Predict first:* with $N$ = 1924, $S$ = 10 and $T$ = 456, how many cycles?
2. **Compare with the single-cycle core.** The register-write trace (`trace.txt`) must be identical to Lab 14-05's: pipelining changes timing, never results.
3. **Micro-programs (notebook).** Run the sequences of Examples 14-06.3 to 14-06.5 and Problems 14-06.2, 14-06.5 and 14-06.6, and read the stall and flush counts.
4. **Break it.** In `rv32_pipe.v`, make the forwarding unit prefer MEM/WB over EX/MEM, or remove the load-use stall. Rerun the testbench and the micro-programs: which check fails first, and which instruction is the first to produce a wrong value?

## Expected results

| Step | Quantity | Expected |
|---|---|---|
| 1 | Testbench | `sum = 115, fib(10) = 55, 2850 cycles for 1924 instructions (CPI = 1.481), 10 load-use stalls, 456 flushes`, then `TEST PASSED` |
| 2 | Trace | 1281 register writes, identical to Lab 14-05's |
| 3 | Micro-programs | 0 stalls with forwarding only; 1 per adjacent load-use; 0 after scheduling; 2 flush cycles per taken branch or jump |
| 4 | Broken forwarding | Problem 14-06.5's `add` writes 6 instead of 20; the full program fails its result checks |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 14-06.a | cycles | 2850 | — |
| Lab 14-06.b | load-use stalls | 10 | — |
| Lab 14-06.c | flushes (taken branches and jumps) | 456 | — |
| Lab 14-06.d | run time at 285 ps | 0.812 | µs |

*These are recomputed by [verify_14_06.py](../../verify/verify_14_06.py), which rebuilds the program, runs this core in Icarus Verilog, and compares its counts with the model and its trace with the Python simulator.*

## Discussion questions

1. The testbench checks the number of stalls and flushes as well as the cycle count. Why is the cycle count alone not enough?
2. All 10 load-use stalls come from the sum loop. Why does the recursive `fib` never stall on a load, even though it loads three registers before every return?
3. Why can the pipeline flush the two instructions after a taken branch without undoing anything?

### Answers

1. Different combinations can give the same total. One stall too many and one flush too few, for example, cancel out. Checking each count separately pins down which mechanism misbehaves.
2. The three loads (`lw ra`, `lw s0`, `lw s1`) are followed by `addi sp, sp, 16` and `ret`. Neither of those reads a register loaded by the instruction just before it: `ret` reads ra, which was loaded three instructions earlier, and `addi` reads sp. The compiler-style ordering of an epilogue naturally hides load latency.
3. No instruction writes a register or memory before MEM (stores) or WB (registers), and the two wrong-path instructions are only in IF and ID when the branch resolves in EX. Turning them into bubbles discards work that has no visible effect yet.

## Optional hardware extension

Synthesize both cores (Lab 14-05 and this one) for the same FPGA and compare the maximum clock frequencies the timing reports give. Is the ratio close to the 2.56 the chapter's model predicts? The FPGA's memories and multiplexers have very different relative delays from the chapter's illustrative numbers, and the comparison shows how much the stage balance depends on the technology.
