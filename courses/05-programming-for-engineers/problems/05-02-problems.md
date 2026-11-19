# Problems 05-02 · NumPy, Vectorization and Numerical Computing

Chapter: [05-02](../chapters/05-02-numpy-and-vectorization.md) · Worked solutions: [05-02 solutions](../solutions/05-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** NumPy 2.0 or later, imported as `np`. Use vectorized operations, not Python loops, unless a problem asks for a loop. Random numbers come from `np.random.default_rng(seed)` with the seed given, so results are reproducible.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 05-02.1 [A]

**Making arrays.** Find (a) the spacing of `np.linspace(0, 1, 11)`, (b) the number of elements of `np.arange(0, 1, 0.1)`, and (c) the number of elements of `np.zeros((3, 4))`. Why does `linspace` suit floating-point ranges better than `arange`?

### Problem 05-02.2 [A]

**Broadcasting shapes.** Predict the shape of each result, or say that it is an error: (a) `(4, 1)` with `(3,)`; (b) `(2, 3)` with `(2,)`; (c) `(2, 3)` with `(2, 1)`; (d) `(5,)` with `(1, 5)`. How many elements does (a) have?

### Problem 05-02.3 [A]

**Wrap-around.** Predict `np.uint8(250) + np.uint8(10)` and `np.int8(127) + np.int8(1)`, and explain each in terms of the type's range.

### Problem 05-02.4 [B]

**RMS and crest factor.** Sample one period of a triangle wave swinging between −1 and +1 at 10,000 points with `np.linspace(0, 1, 10_000, endpoint=False)`. Find its RMS value and its crest factor (peak divided by RMS), and compare with the exact $1/\sqrt3$ and $\sqrt3$.

### Problem 05-02.5 [B]

**Leakage screen.** A transistor's off-current is modeled as normal with mean 10 µA and standard deviation 2 µA. Simulate 5,000 devices with `default_rng(7)` and count those above 14 µA. Compare with the expected count from $Q(2)$.

### Problem 05-02.6 [B]

**A view in place.** After `x = np.arange(6.0)` and `x[1:4] *= 2`, what is `x`, and what is its sum? Would `x[[1, 2, 3]] *= 2` behave the same way?

### Problem 05-02.7 [B]

**Summing in float32.** A float32 array holds one million copies of 0.1. Sum it (a) with a Python loop into a `np.float32` accumulator, (b) with `np.sum`, and (c) with `math.fsum` after converting to float64. Explain the three results.

### Problem 05-02.8 [B]

**Missing data.** A log reads `[1, 2, nan, 4]`. Find `np.mean`, `np.nanmean` and the number of valid entries. Why is NumPy's default behavior (returning NaN) the safe one?

### Problem 05-02.9 [B]

**A low-pass filter over frequency.** An RC low-pass filter's response is $H = 1/(1 + jf/f_c)$. Using a complex array of normalized frequencies $f/f_c = 1$ and 10, find $|H|$ and its phase in degrees at each.

### Problem 05-02.10 [C]

**A negative variance.** Four readings of a large DC level are $10^9 + 4$, $10^9 + 7$, $10^9 + 13$ and $10^9 + 16$. Compute the population variance with the one-pass formula $\overline{x^2} - \bar x^2$ and with the two-pass formula $\overline{(x - \bar x)^2}$. Explain the difference.

### Problem 05-02.11 [C]

**A quadratic with a tiny root.** For $x^2 - 10^8x + 1 = 0$, compute the smaller root with the textbook formula $(-b - \sqrt{b^2 - 4ac})/2a$ and with the stable form $c/(a\,x_{\text{large}})$, where $x_{\text{large}}$ is the larger root. Which is right, and why?

### Problem 05-02.12 [B]

**Fitting a decay.** A capacitor voltage sampled at $t$ = 0, 1, …, 5 ms follows $v = 5e^{-t/\tau}$ with τ = 2 ms. Recover τ and the initial voltage with a straight-line fit to $\ln v$ against $t$.

### Problem 05-02.13 [C]

**A filter design table.** For an RC low-pass filter, $f_c = 1/(2\pi RC)$. Using the E6 series (1.0, 1.5, 2.2, 3.3, 4.7, 6.8) for $R$ in the 1 kΩ decade and $C$ in the 10 nF decade, compute all 36 corner frequencies by broadcasting, and list the pairs within 5% of 1 kHz.

---

## Objective coverage

| Learning objective (chapter 05-02) | Problems |
|---|---|
| 1. Creating arrays; why arrays are fast | 1, 4, 7 |
| 2. Elementwise operations, aggregations, broadcasting | 2, 4, 9, 13 |
| 3. Views, copies and masks | 5, 6, 8 |
| 4. dtypes, overflow, rounding, NaN, promotion | 3, 7, 8 |
| 5. Cancellation, complex arrays, least squares | 9, 10, 11, 12 |
