# Lab 23-09 · An Analog Matrix-Vector Multiply

Chapter: [23-09 · Compute-in-Memory and Near-Memory Computing](../../chapters/23-09-compute-in-memory.md)

## Objective

Build a small resistive crossbar in ngspice, confirm that it computes a signed matrix-vector product with Ohm's and Kirchhoff's laws, and see what happens when the columns are not held at a virtual ground. Then use the chapter's models to measure compute SNR under device variation and to map the ADC-limited efficiency ceiling.

## Background

§3.2 showed that a crossbar with row voltages $V_i$ and virtual-ground columns computes $I_j = \sum_i V_iG_{ij}$, and that signed weights use conductance pairs whose difference carries the sign. §3.3 derived the compute SNR $1/\sigma^2$ for zero-mean products with independent relative errors. §3.4 gave the ADC energy per MAC.

## Files

- `crossbar.cir`: Example 23-09.2's 4 × 4 array (two signed outputs as two conductance pairs). Part A reads the columns through 0 V sources (ideal transimpedance amplifiers); Part B reads each column through a 10 kΩ resistor.
- `cim.py`: the chapter's models.
- `23-09-cim-lab.ipynb`: the notebook for Parts 2 and 3.

## Procedure

**Part 1 · ngspice.**

1. Predict the four column currents and the two differential outputs (Example 23-09.2).
2. Run `ngspice -b crossbar.cir` and compare Part A (`i1p`, `i1n`, `i2p`, `i2n`, `y1`, `y2`).
3. *Predict first:* will Part B's outputs (`y1b`, `y2b`) be larger or smaller than Part A's? Then compare.

**Part 2 · Compute SNR** (notebook). Draw a 256 × 64 array of random signed weights and random inputs, apply 5% independent conductance variation, and compare the measured output SNR with $1/\sigma^2$.

**Part 3 · The ADC ceiling** (notebook). Plot the ADC-limited TOPS/W against precision for 256-row arrays at three figures of merit (chapter Figure 3).

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 23-09.a | column 1, positive half (Part A) | 11.6 | µA |
| Lab 23-09.b | column 2, negative half (Part A) | 4.60 | µA |
| Lab 23-09.c | output 1 (Part A) | 11.0 | µA |
| Lab 23-09.d | output 2 (Part A) | -1.00 | µA |
| Lab 23-09.e | output 1 with 10 kΩ sensing (Part B) | 6.55 | µA |
| Lab 23-09.f | output 2 with 10 kΩ sensing (Part B) | -1.02 | µA |
| Lab 23-09.g | column 1 positive-half voltage (Part B) | 70.7 | mV |
| Lab 23-09.h | output 1 drop in Part B | 40 | % |
| Lab 23-09.i | SNR for 5% variation | 26 | dB |
| Lab 23-09.j | effective bits for 5% variation | 4 | bits |

- Part 1: Part A matches Example 23-09.2 to the printed digits. In Part B, output 1 falls by about 40%, while output 2 barely changes. The error depends on each column's total conductance, so it is data-dependent, not a simple gain error.
- Part 2: the measured SNR lands within a few tenths of a decibel of the model's 26 dB (about 4 effective bits).
- Part 3: the ceiling falls as the square of the bit width; at 8 bits it sits in single digits of TOPS/W for a 5 fJ per step ADC.

## Discussion

1. Why does Part B shrink output 1 so much more than output 2?

   <details><summary>Answer</summary>

   Each column's voltage rises to $I R_s$, cutting every cell's voltage by that amount. Column 1's positive half would carry 11.6 µA ideally; with 10 kΩ sensing its voltage rises to 70.7 mV, and it loses a large share of its current. Output 2's halves carry only a few microamps each, so both lose little, and their losses nearly cancel in the difference.

   </details>

2. Why don't more rows raise the SNR in Part 2?

   <details><summary>Answer</summary>

   With random signed weights, the signal power and the error power both grow in proportion to the number of rows, so their ratio stays $1/\sigma^2$ (§3.3).

   </details>

3. What does the netlist leave out?

   <details><summary>Answer</summary>

   Wire resistance along rows and columns (IR drop), device nonlinearity (conductance changing with voltage), the input DACs and output ADCs, noise, and drift of the stored conductances (23-08). Each adds error that calibration and training must absorb.

   </details>

## Optional hardware

A breadboard version uses resistors as weights, a few precision voltage sources or a resistive divider as inputs, and an op-amp transimpedance amplifier per column (06-10). Measure the column voltages with and without the op-amps to reproduce Part B.
