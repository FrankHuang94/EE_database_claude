# Lab 16-04 · The FFT in Software and Silicon

Chapter: [16-04 The FFT Algorithm](../../chapters/16-04-the-fft.md)

## Objective

Build the radix-2 FFT, count its operations exactly, exploit real inputs, and run the same algorithm as a fixed-point hardware datapath: an 8-point FFT in Verilog that must match a Python model bit for bit, including the overflow case that per-stage halving does not prevent.

## Background

Read §3 of the chapter. `fft.py` holds a recursive FFT, in-place decimation-in-time and decimation-in-frequency FFTs (the DIT one instrumented to count butterflies and twiddle multiplications), the inverse via conjugation, two real FFTs from one complex FFT, and `fft8_fixed`, a bit-exact model of the hardware. `bfly.v` is one Q1.15 butterfly (rounded twiddle product, half-scaled and saturated outputs); `fft8.v` wires twelve of them into Figure 2's flow graph. `make_vectors.py` writes `vectors.hex` from the Python model; `fft8_tb.v` applies every vector and compares all outputs exactly. The Verilog parts need Icarus Verilog; CI runs the testbench through `tools/run_hdl.py`.

## Files

- [fft.py](fft.py): `bit_reverse`, `fft_recursive`, `fft_dit`, `fft_dif`, `ifft_via_fft`, `two_real_ffts`, `twiddle_counts`, `fft8_fixed`.
- [bfly.v](bfly.v), [fft8.v](fft8.v): the fixed-point butterfly and the 8-point FFT.
- [fft8_tb.v](fft8_tb.v): self-checking testbench; [make_vectors.py](make_vectors.py) and [vectors.hex](vectors.hex): its test vectors.
- [16-04-fft-lab.ipynb](16-04-fft-lab.ipynb): the notebook (Parts 1–5).

## Procedure

1. **Check and count (Part 1).** Compare `fft_dit`, `fft_dif` and `fft_recursive` with `numpy.fft.fft` for $N$ = 2 to 4096, and tabulate butterflies and non-trivial multiplications against §3.5's formula.
2. **Time it (Part 2).** Time the direct DFT (a matrix product), the Python `fft_dit` and `numpy.fft.fft` for $N$ = 64 to 4096, and plot the times on log axes. *Predict first:* the slopes of the three curves.
3. **Real data and the inverse (Part 3).** Compute two real FFTs with one complex FFT, and an inverse FFT with the forward routine.
4. **Run the hardware (Part 4).** Simulate `fft8_tb.v` and read its report. Then find the vector that saturates, and print each stage's values from the Python model to see where it happens.
5. **Fixed-point error (Part 5).** For 2000 random half-scale inputs, compare `fft8_fixed` with the exact DFT/8 and histogram the error in LSBs.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Counts | butterflies $\frac N2\log_2N$; non-trivial multiplications $\frac N2\log_2N - \frac{3N}2 + 2$ (10 for $N$ = 16, 3,586 for $N$ = 1024) |
| 2 | Timing | direct grows about as $N^2$, both FFTs as $N\log N$; the Python FFT is much slower than `numpy.fft` at every size |
| 3 | Real and inverse | both match `numpy.fft` to rounding |
| 4 | Hardware | `TEST PASSED (67 vectors, bit-exact)`; two full-scale vectors saturate a butterfly, one negatively and one positively (Example 16-04.5) |
| 5 | Fixed-point error | at most 2.03 LSB over 2000 half-scale vectors |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 16-04.a | largest fixed-point error, half-scale inputs | 2.03 | LSB |
| Lab 16-04.b | test vectors | 67 | — |
| Lab 16-04.c | vectors that drive a saturation | 2 | — |

## Discussion

1. In Part 2, why is the Python FFT slower than the direct DFT for small $N$ even though it does far fewer multiplications?
2. In Part 4, why must the testbench compare against a bit-exact model rather than against `numpy.fft`?
3. In Part 4, why did the saturating vector have to be searched for, when Example 16-04.5 shows the overflow so simply?
4. In Part 5, where does the fixed-point error come from, and why is it a couple of LSBs rather than half an LSB?

### Answers

1. The direct DFT is a single matrix product executed in compiled, vectorized code, while the Python FFT runs one interpreted loop iteration per butterfly. Interpreter overhead, not arithmetic, dominates until $N$ is large; this is why algorithm comparisons must be made in the same implementation technology.
2. Fixed-point hardware rounds and truncates at specific points, so its outputs differ from the exact FFT by a few LSBs. A comparison against `numpy.fft` would need a tolerance, which could hide real bugs (a wrong rounding constant changes outputs by one LSB). A bit-exact model makes any difference a failure.
3. The overflow needs a particular combination at one butterfly's inputs in the last stage: a large $a$ and a $b$ whose rotation by the twiddle lines its magnitude up with $a$ (Example 16-04.5's $a = 32767$, $b = 32767 + j32767$ at $W_8^1$). Those values are produced by the earlier stages, so a designer must work backwards through the flow graph, as the constructed vector does, or search, as the seeded vector does (it saturates negatively: $a = -32767$, $b = -16383 + j32767$ at $W_8^3$). Most inputs, even full-scale ones, never produce it, and a testbench must include both signs, or a clamp error on one side goes unnoticed.
4. Each butterfly rounds the twiddle product and truncates when it halves the sum, and the twiddles themselves are rounded to 15 bits ($W^0 = 1$ becomes 32767/32768). Three stages of such errors accumulate, and the halvings truncate rather than round, which biases them; together they give errors of one to two LSBs.

## Optional hardware

Synthesize `fft8.v` for any FPGA with a free toolchain (for example Yosys with nextpnr for an iCE40 or ECP5 board) and report the number of DSP blocks or LUTs and the maximum clock frequency. Then register the outputs of each stage and see how pipelining changes the clock rate and the latency.
