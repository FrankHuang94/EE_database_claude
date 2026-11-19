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
4. **Part 3:** predict how fast the rectangle and trapezoid errors shrink for $e^t$, and how many rectangles would match `quad`.
5. **Part 4:** state the Wheatstone bridge's balance condition, then check it.
6. **Part 5:** save the figure and open the SVG to inspect it.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | evaluations to reach 10⁻¹² | bisection 41, `brentq` 14, `newton` from 0.7 V 7; `newton` from 0 or 0.5 V returns a point that is not a root (residual about 5 mA); from 1.5 V it is still creeping toward the root when its 50 iterations run out (it would converge after 52) |
| 2 | RMS residuals | one exponential 49.7 mV (systematic pattern); two exponentials 8.5 mV, time constants 1.009 and 5.334 ms |
| 3 | integration errors for $e^t$ on [0, 1] at n = 256 | left rectangles 3.35×10⁻³, trapezoid 2.18×10⁻⁶ (each fourfold increase in n divides them by 4 and 16); `quad` 2.2×10⁻¹⁶, with its own estimate 1.9×10⁻¹⁴ |
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
| Lab 05-03.f | left-rectangle error for $e^t$, n = 256 | 3.35×10^-3 | — |
| Lab 05-03.g | trapezoid error for $e^t$, n = 256 | 2.18×10^-6 | — |

## Discussion questions

1. Newton's method returned 0.5 V, which is not a root, without raising an error. Why did it stop there, and what single habit would have caught the mistake?
2. In Part 2 the one-exponential fit "looks" good on the data plot. Why do residual plots reveal what the data plot hides?
3. Why does the trapezoid error for $e^t$ shrink as $1/n^2$ while the rectangle error shrinks only as $1/n$?
4. Why save engineering figures as SVG or PDF rather than PNG?

<details><summary>Answers to the discussion questions</summary>

1. Without a derivative, SciPy's `newton` uses the secant method, and it stops when two successive estimates agree to within `tol`; it never checks that the function itself is near zero. From 0.5 V the function is dominated by the resistor term and has a gentle slope, so the first secant step jumps to 4.6 V (from 0 V, to 5.0 V), where the diode's exponential makes the function about −10⁶³ A. A secant line through such a gigantic value is nearly vertical, so the next estimate lands back on 0.5 V to within about 10⁻⁶⁰ V; two successive estimates now agree, and the step-size test declares convergence at a point that is not a root. (From 1.5 V the opposite happens: the exponential dominates, each step moves only about 18 mV, less than one thermal voltage, and the method creeps toward the root; it needs 52 iterations and is stopped at 50. Slow and divergent look the same from outside, which is another reason to check.) Substituting the answer back (`mismatch(root)` is 4.5 mA, not zero) catches the false root immediately. Always check the residual.
2. The model's errors (tens of millivolts) are small compared with the signal's range (5 V), so the curves overlap on a full-scale plot. Residuals remove the signal and magnify what is left; a systematic pattern (long runs of one sign, a curve) means the model is missing physics, while random scatter at the noise level means it is adequate.
3. A left-rectangle sum treats the function as constant across each interval of width $h = 1/n$, so on each interval it misses a triangle of area about $\tfrac12 g'h^2$; summed over $n$ intervals, the error is about $\tfrac12 h\,[g(1) - g(0)]$, proportional to $h$ (here $0.86/n$). The trapezoid rule joins the endpoints with a straight line, which captures the slope exactly; what remains is the curvature, an error of about $g''h^3/12$ per interval, so the total is proportional to $h^2$ (here $0.14/n^2$). Each extra power of $h$ is a factor of 4 for a fourfold increase in $n$. The notebook's "Your turn" shows two exceptions: $\sqrt t$, whose infinite slope at 0 spoils the trapezoid rule's $h^2$ rate, and $\sin^2$ over whole periods, where both sums are exact.
4. Vector formats store lines and text as shapes, so they stay sharp at any zoom or print size and are small for line plots; text in them remains searchable and editable. PNG is a fixed grid of pixels that blurs when enlarged (though it is better for images with millions of points, such as dense scatter plots).

</details>

## Optional hardware version

If you have a multimeter and a resistor–capacitor pair (say 10 kΩ and 100 µF, τ = 1 s), log the capacitor voltage by hand every second while it charges from a battery, fit $V_s(1 - e^{-t/\tau})$ with `curve_fit`, and compare the fitted τ with $RC$ from the component values (and their tolerances).
