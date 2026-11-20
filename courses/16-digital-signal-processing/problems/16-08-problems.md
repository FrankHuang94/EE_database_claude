# Problems 16-08 · Filter Structures and Implementation

Chapter: [16-08](../chapters/16-08-filter-structures.md) · Worked solutions: [16-08 solutions](../solutions/16-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $H(z) = B(z)/A(z)$ with $A(z) = 1 + a_1z^{-1} + \cdots$; costs are counted as multipliers, two-input adders and delay registers per output sample. "Fractional bits" means coefficients rounded to the nearest multiple of $2^{-B}$. Problems marked *(lab)* need the lab's `structures.py` or an equivalent tool.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 16-08.1 [A]

**Counting.** An order-6 IIR filter has 7 numerator and 6 denominator coefficients. Count multipliers, adders and delays for Direct Form I, Direct Form II and a cascade of three biquads (each in Direct Form II).

### Problem 16-08.2 [A]

**Transposition by hand.** For the FIR filter $h = (1, -1, 0.5)$, draw the transposed structure and compute its first five outputs for the input $x = (1, 2, 3, 0, 0)$, tracking the two registers. Check against direct convolution.

### Problem 16-08.3 [A]

**Direct Form II by hand.** For $H(z) = (1 + z^{-1})/(1 - 0.5z^{-1})$, write the DF II recursions for $w[n]$ and $y[n]$ and compute the first four outputs of the impulse response.

### Problem 16-08.4 [B]

**Clock rates.** A multiplier takes 1.5 ns and an adder 0.4 ns. For a 32-tap FIR filter, find the critical path and maximum clock for (a) the direct form with an adder chain, (b) the direct form with a balanced adder tree, (c) the transposed form.

### Problem 16-08.5 [B]

**Headroom for DF II.** A biquad has poles at $0.95e^{\pm j\pi/3}$, so $A(z) = 1 - 0.95z^{-1} + 0.9025z^{-2}$. *(lab)* Find the peak of $\lvert 1/A(e^{j\omega})\rvert$ and the frequency where it occurs, and the number of extra bits a DF II implementation needs at its internal node for sinusoidal inputs.

### Problem 16-08.6 [B]

**Angle sensitivity.** For a direct-form biquad with poles $\rho e^{\pm j\theta}$, show that $\partial\theta/\partial a_1 = 1/(2\rho\sin\theta)$ when $a_2$ is held fixed. Evaluate it for $\rho = 0.99$ at $\theta = \pi/2$ and at $\theta = 0.01$ rad.

### Problem 16-08.7 [B]

**Lattice stability test.** Find the reflection coefficients of (a) $A(z) = 1 + 0.5z^{-1} + 0.9z^{-2}$ and (b) $A(z) = 1 - 1.8z^{-1} + 1.2z^{-2}$, and decide stability. Confirm (b) by computing its root magnitude.

### Problem 16-08.8 [B]

**A fixed-point Butterworth biquad.** *(lab)* Quantize the coefficients of Example 16-07.3 ($b = (0.09763, 0.19526, 0.09763)$, $a = (1, -0.94281, 0.33333)$) to Q2.14 integers. (a) Give the five integers and the quantized DC gain. (b) A step of 32,000 is applied. Does the 16-bit output saturate, and what is the final output value?

### Problem 16-08.9 [C]

**Coupled form for a 50 Hz resonator.** *(lab)* A resonator at 50 Hz with pole radius 0.9995 runs at $f_s$ = 48 kHz with 14 fractional bits. Find the realized pole frequency in direct form and in coupled form, and the multiplications per sample of each recursion.

### Problem 16-08.10 [C]

**Ordering sections.** *(lab)* The order-8 elliptic filter of 16-07 has four biquads. Compute the peak gain from the input to each section's output for SciPy's ordering and for the reverse ordering. How many extra bits of headroom does the reverse ordering need at its worst intermediate node?

### Problem 16-08.11 [C]

**Lattice of a fourth-order polynomial.** *(lab)* Multiply the denominators of the last two sections of the 16-07 elliptic filter into one fourth-order $A(z)$ and find its reflection coefficients. Is it stable, and which coefficient warns that a root is close to the circle?

### Problem 16-08.12 [C]

**Round-off noise gain.** In a DF I biquad that rounds once, at the output of its accumulator, the rounding error $e[n]$ enters the feedback loop and reaches the output filtered by $1/A(z)$. *(lab)* For the sharpest elliptic section ($a = (1, -1.6973, 0.9702)$), compute the noise power gain $\sum_n g[n]^2$ of $1/A$ and express it in dB. What does it mean for the output noise?

---

## Objective coverage

| Learning objective (chapter 16-08) | Problems |
|---|---|
| 1. Structures, counts and transposition | 1, 2, 3 |
| 2. Critical paths | 4 |
| 3. Internal gain, pairing, ordering, scaling | 5, 10, 12 |
| 4. Coefficient sensitivity and the coupled form | 6, 9 |
| 5. Lattice structures | 7, 11 |
| 6. Fixed-point biquads | 8, 12 |
