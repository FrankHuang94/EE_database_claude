# Lab 05-03 · SciPy, SymPy and Matplotlib

**Chapter:** [05-03](../../chapters/05-03-scipy-sympy-matplotlib.md) · **Notebook:** [05-03-scipy.ipynb](05-03-scipy.ipynb) · **Time:** about 75 minutes

## Objective

1. Compare bisection, Brent's method and Newton's (secant) method for speed and robustness.
2. Detect an inadequate model from its residuals, and fix it.
3. See how numerical integration accuracy depends on the method and the function.
4. Use SymPy to check a hand-derived condition.
5. Produce and save a two-panel engineering figure.

## Background

Chapter sections 3.1 to 3.6 and Examples 05-03.1, 05-03.2 and 05-03.6; Problems 05-03.10 and 05-03.12. All random data use fixed seeds.

## Procedure

1. Run **Restart & Run All** once, then work cell by cell, writing each prediction first.
2. **Part 1:** predict which root-finder needs fewest function evaluations and which can fail.
3. **Part 2:** predict whether a wrong one-exponential model will look wrong when plotted over the data.
4. **Part 3:** predict how many rectangles match `quad`.
5. **Part 4:** state the Wheatstone bridge's balance condition, then check it.
6. **Part 5:** save the figure and open the SVG to inspect it.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | evaluations to reach 10⁻¹² | bisection 41, `brentq` 14, `newton` from 0.7 V 7; `newton` from 0 or 0.5 V returns a point that is not a root (residual about 5 mA); from 1.5 V it runs out of its 50 iterations |
| 2 | RMS residuals | one exponential 49.7 mV (systematic pattern); two exponentials 8.5 mV, time constants 1.009 and 5.334 ms |
| 3 | integration errors for sin²(πt) on [0, 1] | zero to rounding for every method (a special case); `quad`'s own estimate 5.6×10⁻¹⁵ |
| 4 | bridge | difference $V(R_2R_3 - R_1R_4)/[(R_1 + R_2)(R_3 + R_4)]$, which is 0 when $R_1/R_2 = R_3/R_4$ (SymPy prints an equal, unexpanded form) |
| 5 | figure | SVG saved; the response is −3.01 dB at $f_c$ |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 05-03.a | bisection evaluations | 41 | — |
| Lab 05-03.b | brentq evaluations | 14 | — |
| Lab 05-03.c | Newton (secant) evaluations from 0.7 V | 7 | — |
| Lab 05-03.d | RMS residual, two-exponential fit | 8.5 | mV |
| Lab 05-03.e | fitted slow time constant | 5.334 | ms |

## Discussion questions

1. Newton's method returned 0.5 V, which is not a root, without raising an error. Why did it stop there, and what single habit would have caught the mistake?
2. In Part 2 the one-exponential fit "looks" good on the data plot. Why do residual plots reveal what the data plot hides?
3. The rectangle sum was exact for $\sin^2(\pi t)$. Why is that a special case, and what happens for $\sqrt t$ on $[0, 1]$?
4. Why save engineering figures as SVG or PDF rather than PNG?

<details><summary>Answers to the discussion questions</summary>

1. Without a derivative, SciPy's `newton` uses the secant method, and it stops when two successive estimates agree to within `tol`; it never checks that the function itself is near zero. From 0.5 V the function is dominated by the resistor term and has a gentle slope, so the first secant step jumps to about 4.6 V, where the diode's exponential makes the function about −10⁶³ A. A secant line through such a gigantic value is nearly vertical, so the next estimate lands back on 0.5 V to within about 10⁻⁶⁰ V; two successive estimates now agree, and the step-size test declares convergence at a point that is not a root. (From 1.5 V the opposite happens: the exponential dominates, each step moves only about 18 mV, less than one thermal voltage, and the method creeps toward the root until its 50 iterations run out.) Substituting the answer back (`mismatch(root)` is 4.5 mA, not zero) catches the false root immediately. Always check the residual.
2. The model's errors (tens of millivolts) are small compared with the signal's range (5 V), so the curves overlap on a full-scale plot. Residuals remove the signal and magnify what is left; a systematic pattern (long runs of one sign, a curve) means the model is missing physics, while random scatter at the noise level means it is adequate.
3. With equally spaced points covering whole half-periods, sums of $\sin^2$ average to exactly ½, because $\sin^2 = \tfrac12(1 - \cos2\pi t)$ and the cosine terms cancel over the points. For $\sqrt t$, whose slope is infinite at 0, the rectangle and trapezoid errors shrink slowly (roughly as $n^{-1}$ and $n^{-1.5}$), while `quad`, which places points adaptively, still reaches near machine precision.
4. Vector formats store lines and text as shapes, so they stay sharp at any zoom or print size and are small for line plots; text in them remains searchable and editable. PNG is a fixed grid of pixels that blurs when enlarged (though it is better for images with millions of points, such as dense scatter plots).

</details>

## Optional hardware version

If you have a multimeter and a resistor–capacitor pair (say 10 kΩ and 100 µF, τ = 1 s), log the capacitor voltage by hand every second while it charges from a battery, fit $V_s(1 - e^{-t/\tau})$ with `curve_fit`, and compare the fitted τ with $RC$ from the component values (and their tolerances).
