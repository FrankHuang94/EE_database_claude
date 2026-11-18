# Lab 05-02 · NumPy, Vectorization and Numerical Computing

**Chapter:** [05-02](../../chapters/05-02-numpy-and-vectorization.md) · **Notebook:** [05-02-numpy.ipynb](05-02-numpy.ipynb) · **Time:** about 75 minutes

## Objective

1. Measure the speedup of a vectorized NumPy computation over a Python loop.
2. Use broadcasting to explore a whole component design space in one expression.
3. Compare the range and precision of float16, float32 and float64, and of the integer types.
4. See NaN propagate, and compare summation methods on float32 data.
5. Make a random simulation reproducible with a seeded generator.

## Background

Chapter sections 3.1 to 3.6 and Examples 05-02.2 to 05-02.4; Problems 05-02.7 and 05-02.13. Part 1's timings depend on your computer; every other result is deterministic.

## Procedure

1. Open the notebook and run **Restart & Run All** once; then work through it cell by cell.
2. **Part 1:** predict the speedup of NumPy over a loop for a million-sample RMS.
3. **Part 2:** predict how many E12 resistor–capacitor pairs give a 1 ms time constant within 2%.
4. **Part 3:** predict float16's precision and largest value.
5. **Part 4:** predict the mean of an array containing NaN, and the most accurate summation method.
6. **Part 5:** predict whether seeded and unseeded generators repeat their numbers.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | RMS of a million standard-normal samples | 1.000125 by both methods; NumPy roughly 10–100× faster (machine-dependent) |
| 2 | pairs within 2% of 1 ms | 6: 1.2 kΩ/820 nF and 8.2 kΩ/120 nF (0.984 ms), 1.5 kΩ/680 nF and 6.8 kΩ/150 nF (1.020 ms), 1.8 kΩ/560 nF and 5.6 kΩ/180 nF (1.008 ms) |
| 3 | float16 / float32 / float64 | ε = 9.766×10⁻⁴ / 1.192×10⁻⁷ / 2.220×10⁻¹⁶; max 65504 / 3.403×10³⁸ / 1.798×10³⁰⁸ |
| 4 | mean with a NaN; float32 sums of a million 0.1s | NaN (nanmean 1.5); loop 100958.34, `np.sum` 100000.01, float64 accumulation 100000.00149 |
| 5 | seeded generator, seed 42 | 0.304717, −1.039984, 0.750451 every time; unseeded generators differ |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 05-02.a | RMS of the samples | 1.000125 | — |
| Lab 05-02.b | pairs within 2% of 1 ms | 6 | — |
| Lab 05-02.c | float16 machine epsilon | 9.766×10^-4 | — |
| Lab 05-02.d | float16 largest value | 65504 | — |
| Lab 05-02.e | float32 loop sum | 100958.34 | — |
| Lab 05-02.f | first seeded normal sample | 0.304717 | — |

## Discussion questions

1. Part 1's speedup is smaller than the hundreds-fold you may have heard quoted. Why might squaring and averaging be near the low end for NumPy, and what kinds of operations gain the most?
2. In Part 2 the six pairs come in mirror-image couples. Why must they, and when would you still prefer one member of a couple over the other?
3. float16 cannot represent 1.0004 distinctly from 1.0. What does that imply for accumulating gradients in AI training at 16 bits, and how do training systems cope?
4. Why is seeding a simulation essential for testing, yet dangerous if the seed is never changed?

<details><summary>Answers to the discussion questions</summary>

1. NumPy's `samples ** 2` creates a temporary million-element array and `np.mean` reads it back, so the work is limited by memory traffic rather than arithmetic; the loop, by contrast, pays interpreter overhead per element. Operations that do much arithmetic per element loaded (polynomials, transcendental functions, matrix products) or that call optimized libraries (`@`, `np.linalg`) gain the most, sometimes thousands of times.
2. The time constant depends only on the product $RC$, so swapping which E12 multiplier goes to $R$ and which to $C$ gives the same product. Practical factors pick one: a larger $R$ draws less current from the source and allows a smaller, cheaper capacitor, but makes the node more sensitive to leakage and noise and to the load it drives.
3. A small gradient update added to a weight near 1.0 is lost if it is smaller than half the gap above 1.0 (about 0.0005 in float16), so training would stall. Systems keep a float32 "master copy" of the weights and accumulate updates in 32 bits, scale the loss so small gradients stay representable, or use bfloat16, whose larger exponent range avoids underflow (though its precision is even lower).
4. A fixed seed makes results repeatable, so a test can check exact values and a bug can be reproduced. But a conclusion drawn from one seed may be a fluke of that particular random sample; rerunning with several seeds (or many trials) shows whether the result is robust.

</details>

## Optional hardware version

None is needed. If you have an oscilloscope or a sound card that can save a captured waveform as CSV, load it with `np.loadtxt` and compute its RMS, peak and crest factor with the array methods of this lab.
