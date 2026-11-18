# Problems 05-03 · SciPy, SymPy and Matplotlib

Chapter: [05-03](../chapters/05-03-scipy-sympy-matplotlib.md) · Worked solutions: [05-03 solutions](../solutions/05-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** SciPy, SymPy and Matplotlib as in the chapter. Random data use `np.random.default_rng(seed)` with the seed given. For every numerical answer, state how you checked it (substitution, a known case or a physical argument).

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 05-03.1 [A]

**A fixed point.** Solve $\cos x = x$ with `brentq` on $[0, 1]$. Why is this bracket valid?

### Problem 05-03.2 [A]

**A minimum you can check by hand.** Use `minimize_scalar` to find the minimum of $x^2 - 4x + 7$ on $[-10, 10]$, and confirm it by completing the square.

### Problem 05-03.3 [B]

**An LED-style operating point.** Repeat Example 05-03.1 with a 3.3 V source and a 330 Ω resistor. Find the diode voltage and current.

### Problem 05-03.4 [B]

**Fitting a discharge.** A capacitor discharges as $v = V_0e^{-t/\tau}$ with $V_0$ = 5 V and τ = 2 ms. Simulate 21 samples from 0 to 10 ms with 50 mV of noise using `default_rng(11)`, fit $V_0$ and τ with `curve_fit`, and report both with standard errors.

### Problem 05-03.5 [B]

**Charge as an area.** A current decays as $i(t) = 2e^{-t/1\,\text{ms}}$ mA. Use `quad` to find the total charge it delivers (from 0 to ∞) and the charge delivered in the first millisecond.

### Problem 05-03.6 [B]

**An inductor's current.** In a series RL circuit the current changes at the rate $di/dt = (V - Ri)/L$ with $V$ = 12 V, $R$ = 6 Ω and $L$ = 3 mH, starting from zero. Use `solve_ivp` to find the current at 0.5 ms, and compare with the exact $\frac VR(1 - e^{-tR/L})$.

### Problem 05-03.7 [B]

**Making a resistance with a parallel pair.** With SymPy, find the resistor $R_2$ that, in parallel with 10 kΩ, gives 4.7 kΩ. Give the exact rational answer and its decimal value.

### Problem 05-03.8 [B]

**Checking an identity.** Use SymPy to simplify $\dfrac{R_1R_2}{R_1 + R_2}\left(\dfrac1{R_1} + \dfrac1{R_2}\right)$. Explain the result physically.

### Problem 05-03.9 [B]

**Reading a datasheet curve.** A ceramic capacitor's datasheet gives its capacitance against DC bias as 10, 9.6, 8.7, 7.5, 6.3 and 5.2 µF at 0, 1, 2, 3, 4 and 5 V (illustrative values). Estimate the capacitance at 2.5 V by linear interpolation and with a cubic spline.

### Problem 05-03.10 [C]

**When the model is wrong.** Simulate 51 samples from 0 to 25 ms of $v = 5(1 - e^{-t/1\,\text{ms}}) + 0.5(1 - e^{-t/5\,\text{ms}})$ with 10 mV of noise (`default_rng(5)`). Fit a single exponential $V_s(1 - e^{-t/\tau})$. Report the fitted values and the RMS residual, and explain how the residuals reveal that the model is inadequate.

### Problem 05-03.11 [C]

**Reading a value off a plotted curve.** For an RC low-pass filter with $f_c$ = 1 kHz, compute $|H|$ in dB on a fine logarithmic frequency grid (as you would to plot it) and use interpolation to find the frequency where the response crosses −20 dB. Compare with the exact value.

### Problem 05-03.12 [C]

**Several roots.** The polynomial $x^3 - 6x^2 + 11x - 6$ has three real roots. Find them exactly with SymPy and numerically with `brentq`, choosing three brackets. What would happen with the bracket $[0, 4]$?

---

## Objective coverage

| Learning objective (chapter 05-03) | Problems |
|---|---|
| 1. Root-finding and optimization | 1, 2, 3, 12 |
| 2. Fitting with uncertainties | 4, 10 |
| 3. Areas and initial-value problems | 5, 6 |
| 4. Symbolic algebra | 7, 8, 12 |
| 5. Plotting and reading curves | 9, 11 |
