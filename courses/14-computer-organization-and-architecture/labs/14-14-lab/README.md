# Lab 14-14 · AI Accelerators: Systolic Arrays, Dataflow and Low Precision

Chapter: [14-14 AI Accelerators](../../chapters/14-14-ai-accelerators.md)

## Objective

Build intuition for the matrix engines at the heart of AI accelerators. Run a 4 × 4 systolic array in Verilog and watch skewed operands meet in the right place at the right cycle. Then use a cycle-accurate Python model to measure latency and utilization across matrix shapes and tilings. Finally, quantize data to 8, 6 and 4 bits and measure what is lost.

## Background

Systolic arrays (§3.2), tiling (§3.3), dataflows and reuse (§3.4), quantization (§3.5) and the memory wall (§3.7).

## Tools

Icarus Verilog (`iverilog`, `vvp`), with GTKWave optional; Python.

## Files

- [systolic4.v](systolic4.v): a 4 × 4 output-stationary array of signed 8-bit multiply-accumulate PEs with 32-bit accumulators.
- [systolic4_tb.v](systolic4_tb.v): a self-checking testbench. It multiplies 4 × K by K × 4 matrices for K = 4 and 16, compares all accumulators with a reference after every cycle, and checks that they first all match after K + 6 cycles.
- [systolic.py](systolic.py): `run` (the cycle-accurate model), `utilization`, `tiled_cycles`, `quantize`.
- [14-14-systolic-lab.ipynb](14-14-systolic-lab.ipynb): the notebook (Parts 2–4).

## Procedure

1. **Verilog (Part 1).** Run `python tools/run_hdl.py 14-14` from the repository root, add `$dumpvars`, and follow one product's operands through the array in the waveform.
2. **Latency and utilization (Part 2).** Sweep M, N and K in `systolic.run`, confirm $T = K + M + N - 2$, and plot utilization against K for a 4 × 4 and an 8 × 8 array. *Predict first:* M = 3, K = 5, N = 2 on a 4 × 4 array.
3. **Tiling (Part 3).** Compare `tiled_cycles` with the ideal for square and for short-K products.
4. **Quantization (Part 4).** Quantize a sinusoid and a random matrix to 8, 6 and 4 bits; measure the SQNR and the error of a matrix product.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Verilog | TEST PASSED; all products correct after 10 cycles (K = 4) and 22 (K = 16) |
| 2 | Latency | $T = K + M + N - 2$ exactly: 8 cycles for (3, 5, 2); 114 for an 8 × 100 by 100 × 8 product on 8 × 8 |
| 3 | Tiling | 80.1% for 1024³ on 128 × 128; 66.8% for K = 512 |
| 4 | Quantization | about 6 dB per bit: 48.7, 39.2 and 25.2 dB at 8, 6 and 4 bits for the sinusoid, scattered about a decibel around the symmetric ideal (49.9, 37.6 and 24.7 dB) because 64 samples of one period give a fixed error pattern, not noise |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 14-14.a | cycles, (M, K, N) = (3, 5, 2) | 8 | — |
| Lab 14-14.b | cycles, 8 × 100 × 8 on 8 × 8 | 114 | — |
| Lab 14-14.c | SQNR, 6 bits | 39.2 | dB |
| Lab 14-14.d | symmetric ideal, 8 bits | 49.9 | dB |
| Lab 14-14.e | symmetric ideal, 6 bits | 37.6 | dB |
| Lab 14-14.f | symmetric ideal, 4 bits | 24.7 | dB |

*These are recomputed by [verify_14_14.py](../../verify/verify_14_14.py), which also runs the Verilog testbench when Icarus Verilog is installed.*

## Discussion questions

1. Why does the testbench, not the array, apply the skew to the inputs?
2. Why is a systolic array's wiring easier to scale than a crossbar's?
3. What happens to a product computed in INT8 if the accumulators were also 8 bits?

### Answers

1. Skewing is a matter of timing at the array's edge. In real accelerators it is done by delay registers or by the buffers that feed the array, so the PEs stay identical and simple. Putting it in the testbench keeps the PE design minimal and shows the timing explicitly.
2. Every PE talks only to its neighbours, so all wires are short and the same length whatever the array size. A crossbar connecting $N$ inputs to $N$ outputs needs $N^2$ crosspoints and long wires that slow down as $N$ grows.
3. They would overflow almost immediately. The products of two 8-bit values need 16 bits, and a sum of K of them needs about $16 + \log_2 K$ bits. That is why the PEs use 32-bit accumulators, and why accelerators quote "INT8 with 32-bit accumulation".

## Optional hardware extension

On a GPU or a TPU you can access (for example a free cloud notebook), time matrix multiplications of growing size in BF16 and in FP32, compute the achieved TFLOPS, and find the size at which each reaches its plateau. Compare the plateau with the vendor's dense peak.
