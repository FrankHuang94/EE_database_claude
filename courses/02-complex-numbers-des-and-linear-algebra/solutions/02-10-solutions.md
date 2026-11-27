# Solutions 02-10 · Numerical Methods for Engineers

Problems: [02-10 problems](../problems/02-10-problems.md) · Chapter: [02-10](../chapters/02-10-numerical-methods.md)

Every numerical answer below is listed in the answer key at the end and is recomputed by [verify_02_10.py](../verify/verify_02_10.py).

---

## Solutions

### Solution 02-10.1

| Format | ε = $2^{-p}$ | Unit roundoff ε/2 | Decimal digits ($-\log_{10}$ of ε/2) |
|---|---|---|---|
| Double ($p = 52$) | **2.220×10⁻¹⁶** | $1.11\times10^{-16}$ | **15.95** |
| Single ($p = 23$) | **1.192×10⁻⁷** | $5.96\times10^{-8}$ | **7.225** |
| Half ($p = 10$) | **9.766×10⁻⁴** | $4.88\times10^{-4}$ | **3.311** |

So double carries about 16 significant digits, single about 7, and half about 3.

### Solution 02-10.2

(a) 0.5 = $2^{-1}$ and 0.375 = $2^{-2} + 2^{-3}$ are finite binary fractions, so they are exact. 0.1 = 1/10 has a factor of 5 in its denominator, so its binary expansion repeats forever, $0.000110011\ldots_2$, and must be rounded.

(b) In single precision, the ten-term sum is **1.0000001** (printed), an error of **+1.192×10⁻⁷**: exactly one unit in the last place at 1. Both formats store 0.1 slightly too large, but each of the ten additions rounds again, and the accumulated result depends on those roundings: in double it lands one unit below 1, in single one unit above.

### Solution 02-10.3

After $n$ steps the bracket length is $2^{-n}$. We need $2^{-n} \le 10^{-6}$, so $n \ge \log_210^6 = 19.93$, that is, **20** steps.

### Solution 02-10.4

With $f' = 2x$, the Newton step is $x - (x^2 - 2)/(2x) = \tfrac12(x + 2/x)$: the ancient "Babylonian" square-root method. From $x_0 = 1$:

- $x_1 = $ **1.5**;
- $x_2 = $ **1.416667**;
- $x_3 = $ **1.414216**.

The errors are 0.4142, 0.08579, $2.453\times10^{-3}$, $2.124\times10^{-6}$ and then $1.6\times10^{-12}$. Each is close to the square of the previous one, divided by $2\sqrt2$, as §3.2 predicts: $f''/(2f') = 2/(2\cdot2\sqrt2) = 1/(2\sqrt2)$.

### Solution 02-10.5

(a) Direct: $e^{10^{-10}} = 1.0000000001$, but stored to about 16 digits, so subtracting 1 keeps only about 6 correct digits. The result is $1.000000082740371\times10^{-10}$, a relative error of **8.269×10⁻⁸**. `expm1` evaluates $e^x - 1$ without ever forming $e^x$ (using a series for small $x$), and returns $1.00000000005\times10^{-10}$, correct to full precision.

(b) With values near $10^8$, the squares are near $10^{16}$, where adjacent doubles are 2 apart. So $\overline{x^2}$ and $\bar{x}^2$ agree to all stored digits, and their difference is **0**: completely wrong. The two-pass formula subtracts the mean *first*, giving deviations −1, 0 and 1, and returns exactly **0.6667**. A logger should use the two-pass formula, or Welford's one-pass update, which never subtracts large nearly equal quantities. The same trap appears when computing the RMS of a signal with a large DC offset.

### Solution 02-10.6

(a) Newton on $f(x) = x - \cos x$, with $f' = 1 + \sin x$, from 1 converges to \$x^* = \$ **0.7390851** in **5** iterations (steps below $10^{-14}$).

(b) The fixed-point iteration $x_{k+1} = \cos x_k$ converges linearly. Each step multiplies the error by about \$\lvert g'(x^*)\rvert = \sin x^* = \$ **0.6736**, the slope of $g(x) = \cos x$ at the root. Reaching $10^{-10}$ from an error of 0.26 takes about $\ln(4\times10^{-10})/\ln0.6736 \approx 55$ steps; counted directly, **55** iterations. Newton's quadratic convergence wins by an order of magnitude in steps.

### Solution 02-10.7

$$
\mathbf{F} = \begin{bmatrix} x^2 + y^2 - 4 \\ xy - 1\end{bmatrix}, \qquad \mathbf{J} = \begin{bmatrix} 2x & 2y \\ y & x\end{bmatrix} .
$$

At $(2, 0.5)$: $\mathbf{F} = (0.25, 0)$ and $\mathbf{J} = \begin{bmatrix} 4 & 1 \\ 0.5 & 2\end{bmatrix}$, with determinant 7.5. Solving $\mathbf{J}\Delta = -\mathbf{F}$ gives $\Delta = (-0.06667, 0.01667)$, so \$(x_1, y_1) = \$ (**1.9333**, **0.5167**). Further steps converge to (**1.9319**, **0.5176**).

*Exact:* substituting $y = 1/x$ gives $x^4 - 4x^2 + 1 = 0$, so $x^2 = 2 + \sqrt3$ and $x = 1.93185$, $y = 0.51764$ ✓.

### Solution 02-10.8

- Euler: $1 + 0.1(-2) = $ **0.8**.
- Heun: $k_1 = -2$ and $k_2 = -2(1 - 0.2) = -1.6$, so \$y = 1 + 0.05(-3.6) = \$ **0.82**.
- RK4: $k_1 = -2$, $k_2 = -1.8$, $k_3 = -1.82$, $k_4 = -1.636$, so \$y = 1 + \tfrac{0.1}{6}(-2 - 3.6 - 3.64 - 1.636) = \$ **0.8187333**.

The exact value is \$e^{-0.2} = \$ **0.8187308**. The one-step errors are 0.0187, 0.0013 and $2.6\times10^{-6}$. These are the Taylor series of $e^{-0.2}$ truncated after its first-, second- and fourth-order terms (2, 3 and 5 terms). For a linear problem, an order-$p$ Runge–Kutta method reproduces exactly the first $p + 1$ terms of $e^{h\lambda}$.

### Solution 02-10.9

(a) $h \le 2\tau = $ **20 µs**.

(b) With $z = h\lambda = -3$:

- forward Euler: $1 + z = $ **−2**, unstable, and oscillating in sign;
- backward Euler: $1/(1 - z) = $ **0.25**, stable and smooth;
- trapezoidal: $(1 + z/2)/(1 - z/2) = -0.5/2.5 = $ **−0.2**, stable, but it flips sign each step (a mild version of trapezoidal ringing).

The exact factor, $e^{-3} = 0.0498$, is positive.

### Solution 02-10.10

(a) Backward Euler gives $i_{n+1} = (C/h)(v_{n+1} - v_n)$: a conductance \$G = C/h = \$ **0.1 S** in parallel with a current source of value \$Gv_n = \$ **0.2 A**, injecting current into the capacitor's top node (the chapter's $-Cv_n/h$ drawn from it), which carries the memory of the previous voltage.

(b) The capacitor current flows into the resistor: $G(v_{n+1} - v_n) + v_{n+1}/R = 0$. So \$v_{n+1} = Gv_n/(G + 1/R) = 0.2/0.11 = \$ **1.818 V**. The exact value is \$2e^{-h/RC} = 2e^{-0.1} = \$ **1.810 V**. The error, about 0.5%, is backward Euler's first-order error for $h/\tau = 0.1$.

### Solution 02-10.11

\$\kappa(\mathbf{A}) = \$ **247.4** and \$\kappa(\mathbf{A}^\mathsf{T}\mathbf{A}) = \$ **6.121×10⁴** $= \kappa(\mathbf{A})^2$. The normal equations can therefore lose $\log_{10}\kappa(\mathbf{A}) \approx 2.4$ more digits than a QR or SVD solve: about 4.8 instead of 2.4. The two columns are nearly parallel because the abscissas 1, 1.01 and 1.02 are close together. Centering them ($t - 1.01$) would make the columns orthogonal and remove the problem.

### Solution 02-10.12

Near $10^8 \approx 2^{26.6}$, single precision's 23 fraction bits leave a spacing of \$2^{26 - 23} = \$ **8**. So $10^8 + 1$ rounds back to $10^8$. A single-precision counter that adds 1 each time stops increasing at $2^{24} = 16{,}777{,}216$, where the spacing first exceeds 1. This is why event counters, timestamps and accumulators belong in integers or doubles, and why FP16 and BF16 sums need wider accumulators.

### Solution 02-10.13

(a) With $f' = 2(x - 1)$, the Newton step is $x - (x - 1)^2/(2(x - 1)) = x - (x - 1)/2$, so $e_{k+1} = e_k/2$: linear convergence with ratio ½. From $e_0 = 1$, reaching $10^{-6}$ needs $2^{-n} \le 10^{-6}$, that is **20** steps.

(b) $x - 2f/f' = x - (x - 1) = 1$ in one step. At a root of multiplicity $m$, Newton's error ratio tends to $1 - 1/m$ instead of 0, because $f'$ vanishes along with $f$. Multiplying the step by $m$ restores fast convergence. In practice, slow, linear convergence of Newton is a symptom of a multiple or nearly multiple root (for example, a circuit near a bifurcation, with two operating points about to merge).

### Solution 02-10.14

(a) $h \le 2\times1\text{ ps} = 2$ ps, so \$10\text{ µs}/2\text{ ps} = \$ **5×10⁶** steps.

(b) $10\text{ µs}/10\text{ ns} = $ **1000** steps, a factor of **5000** fewer.

(c) Each implicit step must solve the circuit equations for the new time point: a Newton iteration, each iteration a sparse LU solve of the MNA matrix. An explicit step needs only function evaluations. For stiff circuits, the trade is overwhelmingly worth it, which is why SPICE is implicit.

### Solution 02-10.15

(a) Half: $10^3\times2^{-11} = $ **0.4883**. Single: $10^3\times2^{-24} = $ **5.960×10⁻⁵**.

(b) The floor is $\kappa u_{64} = 10^3\times2^{-53} = 1.1\times10^{-13}$: no number of passes goes below it, because the residual itself is only that accurate. Passes needed to reach $10^{-13}$: half, \$\ln(10^{-13}/0.4883)/\ln0.4883 \approx \$ **40.8**; single, \$\ln(10^{-13}/5.96\times10^{-5})/\ln(5.96\times10^{-5}) \approx \$ **2.077**, that is, 3 passes (after 2 the error, $(5.96\times10^{-5})^3 = 2.1\times10^{-13}$, is already within a factor of 2 of the floor). Single-precision factorization plus two or three cheap $O(n^2)$ refinement passes gives the full double-precision solve's accuracy; the lab's run stalls near $2\times10^{-14}$ after 2 passes, consistent with this floor. Half precision barely converges at this κ.

(c) The contraction factor must be below 1: $\kappa < 1/u = 2^{11} = $ **2048**. In practice, schemes that use FP16 factorization apply extra techniques, such as scaling, or GMRES-based refinement preconditioned by the low-precision factors, to handle harder matrices.

### Solution 02-10.16

(a) $e^{0.65/0.02586} = 8.24\times10^{10}$, so $i(0.65) = 8.24\times10^{-4}$ A and \$G = i/V_T \approx \$ **0.03172 S** (using $e^{v/V_T}$ exactly, without the −1). Then \$I_{eq} = i - Gv = 8.24\times10^{-4} - 0.03172\times0.65 = \$ **−0.01980 A**. Each diode becomes a 31.7 mS conductance in parallel with a current source.

(b) KCL at $a$: $(v_a - 5)/R + G(v_a - v_b) + I_{eq} = 0$. KCL at $b$: $-G(v_a - v_b) - I_{eq} + Gv_b + I_{eq} = 0$. In matrix form,

$$
\begin{bmatrix} 1/R + G & -G \\ -G & 2G\end{bmatrix}\begin{bmatrix} v_a \\ v_b\end{bmatrix} = \begin{bmatrix} 5/R - I_{eq} \\ 0\end{bmatrix}.
$$

The second row gives $v_a = 2v_b$ (equal diodes share the voltage). Substituting into the first row, $(1/R + G)(2v_b) - Gv_b = 5/R - I_{eq}$, so $v_b(2/R + G) = 5/R - I_{eq}$ and $v_b = (0.005 + 0.01980)/(0.002 + 0.03172) = 0.7354$ V. So \$v_a = \$ **1.471 V**: the step proposes **0.7354 V** across each diode, up from 0.65 V.

(c) $\lvert\Delta v_a\rvert = 0.171$ V, against $10^{-3}\times1.471 + 10^{-6} \approx 1.5$ mV. Not converged.

(d) $a = (0.7354 - 0.65)/V_T = 3.302 > 0$, so the limited voltage is \$0.65 + V_T\big(2 + \ln(3.302 - 2)\big) = 0.65 + 0.02586\times2.264 = \$ **0.7085 V**. The rule halves the proposed step, keeping the next exponential evaluation from jumping by a factor of $e^{3.3}$.

(e) The converged solution has $(5 - 2v)/R = I_S(e^{v/V_T} - 1)$, which gives **0.6884 V** per diode and **3.623 mA**. (Plain Newton from the starting guess, without limiting, takes 8 iterations to reach $10^{-12}$ V.)

### Solution 02-10.17

(a) The trapezoidal rule is $y_{n+1} = y_n + \tfrac h2\big(-y_n - y_{n+1}\big)$, so $y_{n+1}(1 + h/2) = y_n(1 - h/2)$.

(b) $h = 0.1$: \$y(1) = (0.95/1.05)^{10} = \$ **0.3676**, an error of **3.069×10⁻⁴** against $e^{-1} = 0.3679$. $h = 0.05$: $(0.975/1.025)^{20} = 0.3678$, an error of **7.666×10⁻⁵**. The ratio is \$3.069/0.7666 = \$ **4.003**: halving $h$ quarters the error, so the method is **second order**.

(c) Backward Euler at $h = 0.1$: $(1/1.1)^{10} = 0.3855$, an error of **0.01766**, about 58 times larger, as its first order predicts.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 02-10.1a | double machine epsilon | 2.220×10^-16 | — |
| 02-10.1b | single machine epsilon | 1.192×10^-7 | — |
| 02-10.1c | half machine epsilon | 9.766×10^-4 | — |
| 02-10.1d | double decimal digits | 15.95 | — |
| 02-10.1e | single decimal digits | 7.225 | — |
| 02-10.1f | half decimal digits | 3.311 | — |
| 02-10.2a | single-precision sum of ten 0.1 | 1.0000001 | — |
| 02-10.2b | its error | 1.192×10^-7 | — |
| 02-10.3a | bisection steps | 20 | — |
| 02-10.4a | x1 | 1.5 | — |
| 02-10.4b | x2 | 1.416667 | — |
| 02-10.4c | x3 | 1.414216 | — |
| 02-10.5a | relative error of direct e^x − 1 | 8.269×10^-8 | — |
| 02-10.5b | naive variance | 0 | — |
| 02-10.5c | two-pass variance | 0.6667 | — |
| 02-10.6a | root | 0.7390851 | — |
| 02-10.6b | Newton iterations | 5 | — |
| 02-10.6c | fixed-point contraction rate | 0.6736 | — |
| 02-10.6d | fixed-point iterations | 55 | — |
| 02-10.7a | x after one step | 1.9333 | — |
| 02-10.7b | y after one step | 0.5167 | — |
| 02-10.7c | converged x | 1.9319 | — |
| 02-10.7d | converged y | 0.5176 | — |
| 02-10.8a | Euler | 0.8 | — |
| 02-10.8b | Heun | 0.82 | — |
| 02-10.8c | RK4 | 0.8187333 | — |
| 02-10.8d | exact | 0.8187308 | — |
| 02-10.9a | largest stable Euler step | 20 | µs |
| 02-10.9b | Euler factor at 30 µs | −2 | — |
| 02-10.9c | backward Euler factor | 0.25 | — |
| 02-10.9d | trapezoidal factor | −0.2 | — |
| 02-10.10a | companion conductance | 0.1 | S |
| 02-10.10b | companion current source | 0.2 | A |
| 02-10.10c | backward Euler step | 1.818 | V |
| 02-10.10d | exact value | 1.810 | V |
| 02-10.11a | κ(A) | 247.4 | — |
| 02-10.11b | κ(AᵀA) | 6.121×10^4 | — |
| 02-10.12a | single spacing near 1e8 | 8 | — |
| 02-10.13a | steps at the double root | 20 | — |
| 02-10.14a | explicit steps | 5×10^6 | — |
| 02-10.14b | implicit steps | 1000 | — |
| 02-10.14c | speed-up | 5000 | — |
| 02-10.15a | half-precision contraction | 0.4883 | — |
| 02-10.15b | single-precision contraction | 5.960×10^-5 | — |
| 02-10.15c | half-precision passes | 40.8 | — |
| 02-10.15d | single-precision passes | 2.077 | — |
| 02-10.15e | half-precision κ limit | 2048 | — |
| 02-10.16a | companion conductance | 0.03172 | S |
| 02-10.16b | companion current source | −0.01980 | A |
| 02-10.16c | v_a after one step | 1.471 | V |
| 02-10.16d | proposed diode voltage | 0.7354 | V |
| 02-10.16e | limited diode voltage | 0.7085 | V |
| 02-10.16f | converged voltage per diode | 0.6884 | V |
| 02-10.16g | converged current | 3.623 | mA |
| 02-10.17a | y(1), h = 0.1 | 0.3676 | — |
| 02-10.17b | error, h = 0.1 | 3.069×10^-4 | — |
| 02-10.17c | error, h = 0.05 | 7.666×10^-5 | — |
| 02-10.17d | error ratio | 4.003 | — |
| 02-10.17e | backward-Euler error, h = 0.1 | 0.01766 | — |
