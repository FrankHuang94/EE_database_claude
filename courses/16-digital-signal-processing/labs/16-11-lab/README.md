# Lab 16-11 · From Algorithms to Datapaths

Chapter: [16-11 DSP Hardware Architectures](../../chapters/16-11-dsp-hardware-architectures.md)

## Objective

Budget hardware for filters, verify that look-ahead preserves a recursion while relaxing its timing, replace constant multipliers with shift-and-add networks, and build a CORDIC in Python and Verilog that agree bit for bit.

## Background

Read §3 of the chapter. `hwarch.py` computes MAC widths and hardware budgets, iteration bounds, the original and look-ahead first-order recursions, canonical signed-digit decompositions, and floating- and fixed-point CORDIC. `cordic.v` is a 14-stage unrolled rotation-mode CORDIC: 16-bit binary angle in, Q2.14 cosine and sine out; `make_vectors.py` writes its test vectors from `cordic_fixed`.

## Files

- [hwarch.py](hwarch.py): `mac_widths`, `units_needed`, `iteration_bound`, `iir1`, `iir1_lookahead2`, `csd`, `csd_adders`, `cordic_gain`, `cordic_rotate`, `cordic_vector`, `cordic_fixed`.
- [cordic.v](cordic.v), [cordic_tb.v](cordic_tb.v), [make_vectors.py](make_vectors.py), [vectors.hex](vectors.hex): the CORDIC, its self-checking testbench and its 64 test angles.
- [16-11-hardware-lab.ipynb](16-11-hardware-lab.ipynb): the notebook (Parts 1–5).

## Procedure

1. **Budgets (Part 1).** Tabulate DSP blocks for 32- to 256-tap symmetric filters at 25 to 200 MS/s on 400 and 600 MHz blocks.
2. **Look-ahead (Part 2).** Run the first-order recursion and its look-ahead-by-2 and by-4 forms on random inputs and compare.
3. **CSD (Part 3).** Decompose a set of 8-bit coefficients, most with runs of ones, into CSD and count adders against plain binary.
4. **CORDIC convergence (Part 4).** Plot the worst cos/sin error over many angles against the iteration count, in floating and fixed point. *Predict first:* the iterations needed for $10^{-4}$.
5. **Hardware (Part 5).** Check `vectors.hex` against the model, run the testbench, and measure the fixed-point worst error.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Budgets | e.g. 64 taps at 50 MS/s on 400 MHz blocks: 4 folded |
| 2 | Look-ahead | identical outputs to about 1e-12 |
| 3 | CSD | fewer adders than binary for coefficients with runs of ones |
| 4 | Convergence | floating-point worst error falls by about half per iteration, below 1e-4 at 15 iterations |
| 5 | Hardware | TEST PASSED; worst fixed-point error 10.54 LSB over the test angles, which include the worst of all 65,536 codes |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 16-11.a | iterations for worst error below 1e-4 | 15 | — |

## Discussion

1. Why does look-ahead not change the filter's output, yet change its timing?
2. Why do CSD savings appear only for some coefficients?
3. Why is the fixed-point CORDIC's error larger than the residual angle predicts?

### Answers

1. It is an exact algebraic rewrite of the same recursion: each output is still a weighted sum of all past inputs with weights $a^k$. What changes is the dependency structure: each output now depends on the output $M$ samples earlier, so the loop has $M$ registers and $M$ sample periods to complete.
2. CSD reduces nonzero digits only where binary has runs of consecutive ones ($0.111_2 = 1 - 0.001_2$); coefficients whose binary digits already alternate gain nothing.
3. Each of the 13 nonzero arithmetic right shifts per coordinate floors its result, adding a biased error of up to one LSB that accumulates; and the 16-bit angle path (one angle LSB is 1.57 output LSB, with rounded $\arctan$ entries) steers to a slightly wrong angle. Guard bits are needed in both the $x$/$y$ datapath and the angle path (Solution 16-11.12).

## Optional hardware

Synthesize `cordic.v` for an FPGA and compare its resources (adders only) with a sine/cosine lookup table of the same accuracy; then pipeline it by adding a register after every stage and observe the clock rate and the 14-cycle latency.
