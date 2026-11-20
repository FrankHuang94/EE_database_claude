# Lab 16-08 · One Transfer Function, Many Structures

Chapter: [16-08 Filter Structures and Implementation](../../chapters/16-08-filter-structures.md)

## Objective

Implement one filter in several structures, show that they agree in exact arithmetic and differ in internal signal levels, coefficient sensitivity and speed, and verify a fixed-point biquad in Verilog bit for bit against a Python model, including its saturation behaviour.

## Background

Read §3 of the chapter. `structures.py` computes every structure sample by sample so that its internal state can be inspected; the verify script checks each against `scipy.signal.lfilter`. `biquad_df1_fixed` is the bit-exact model of `biquad_df1.v`: Q2.14 coefficients, products summed exactly, rounding by adding $2^{13}$ before an arithmetic shift, and saturation to 16 bits with the saturated value fed back. `make_vectors.py` writes `vectors.hex` from that model; the verify script regenerates the vectors and compares them with the committed file.

## Files

- [structures.py](structures.py): `fir_direct`, `fir_transposed`, `df1`, `df2`, `df2t`, `sos_filter`, `counts`, `critical_path`, `poly_to_lattice`, `lattice_to_poly`, `biquad_df1_fixed`.
- [biquad_df1.v](biquad_df1.v), [biquad_df1_tb.v](biquad_df1_tb.v), [make_vectors.py](make_vectors.py), [vectors.hex](vectors.hex): the fixed-point biquad, its self-checking testbench and its vectors (15 sequences of 64 samples).
- [16-08-structures-lab.ipynb](16-08-structures-lab.ipynb): the notebook (Parts 1–5).

## Procedure

1. **Equivalence (Part 1).** Filter one random input with every structure and compare with `lfilter`.
2. **Internal signals (Part 2).** Record DF II's $w[n]$ for the sharpest elliptic section of 16-07 driven by a sinusoid at its peak frequency, and compare its amplitude with the input and output amplitudes. *Predict first:* the ratio.
3. **Section ordering (Part 3).** Measure the peak gain at each section output for both orderings (Figure 3 of the chapter).
4. **Pole grids (Part 4).** Quantize the 100 Hz resonator of Example 16-08.4 in direct and coupled forms, and plot the reachable pole grids.
5. **Hardware (Part 5).** Run `python ../../../../tools/run_hdl.py 16-08` (or `iverilog`/`vvp` directly) and see `TEST PASSED`. Then change the model's rounding to truncation (remove the $2^{13}$) and count how many expected outputs change: the testbench would catch the mismatch.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Equivalence | every structure matches `lfilter` to about 1e-12 |
| 2 | DF II state | for a unit sinusoid at the peak of $1/A$ (4.07 kHz), $w$ reaches about 66 while the section's output is about 6.2, and in the full cascade the overall output never exceeds the input; DF I stores only $x$ and $y$ |
| 3 | Ordering | intermediate peaks 0.08, 0.39, 0.73 (SciPy) against 6.25, 17.2, 53.6 (reversed) |
| 4 | Pole grids | at 12 bits the direct form puts the resonator at 119.19 Hz, the coupled form at 100.81 Hz |
| 5 | Hardware | TEST PASSED on 15 sequences with 4 saturated outputs (2 positive, 2 negative); truncating instead of rounding changes 895 of the 960 outputs |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 16-08.a | saturated outputs in the vectors | 4 | — |
| Lab 16-08.b | DF II state amplitude at the peak frequency | 66.1 | — |
| Lab 16-08.c | section output amplitude at that frequency | 6.17 | — |
| Lab 16-08.d | outputs changed by truncation (of 960) | 895 | — |

## Discussion

1. In Part 2, why is the DF II state so much larger than the section's output at that frequency?
2. In Part 3, why does SciPy's ordering keep every intermediate peak at or below 1?
3. In Part 5, why must the test vectors include full-scale steps of both signs?
4. Why does the Verilog model feed back the *saturated* output, and what would change if it fed back the unsaturated sum?

### Answers

1. The state is the input through the poles alone, whose gain near their angle is about 66; the section's zeros sit on the unit circle just above the passband and cancel about 90% of that gain before the output (66 down to 6.2).
2. The sections with poles far from the circle (and their zeros) come first and attenuate out-of-band energy before the sharp, high-gain sections see it; in the reverse order the sharpest section amplifies everything near its pole frequency first.
3. Saturation logic has two branches (positive and negative limits). A design is verified only for the cases the vectors exercise; without full-scale steps, both clipping branches and the feedback of a clipped value would go untested.
4. The stored output must be a representable 16-bit value; feeding back the unsaturated sum would require wider state registers and would make the hardware's behaviour after overload differ from a saturating model. Feeding back the clipped value is the standard choice and is what the model does, so the two agree bit for bit.

## Optional hardware

Synthesize `biquad_df1.v` for any FPGA with a vendor tool and look at the resource report: the five products map onto DSP blocks, and the 40-bit accumulator onto their built-in adders. Then pipeline the multiply–add (add a register after the products) and observe that the feedback loop, not the multipliers, now limits the clock.
