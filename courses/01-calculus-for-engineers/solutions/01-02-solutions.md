# Solutions 01-02 · Limits and Continuity

Problems: [01-02 problems](../problems/01-02-problems.md) · Chapter: [01-02](../chapters/01-02-limits-and-continuity.md)

Every numerical answer below is listed in the answer key at the end and is recomputed independently by [verify_01_02.py](../verify/verify_01_02.py).

---

## Solutions

### Solution 01-02.1

(a) $(e^{0.1} - 1)/0.1 = $ **1.0517** and $(e^{0.01} - 1)/0.01 = $ **1.0050**. From the left, $(e^{-0.1} - 1)/(-0.1) = 0.9516$ and $(e^{-0.01} - 1)/(-0.01) = 0.9950$. The values close in on 1 from both sides: **limit 1**. This is the defining property of $e$ (chapter §3.3).

(b) $\sin(0.3)/0.1 = $ **2.9552** and $\sin(0.03)/0.01 = $ **2.9996**. The function is even, so the negative side gives the same values. **Limit 3.** (Write $\sin 3x/x = 3\cdot\sin 3x/(3x)$, and the second factor tends to 1.)

(c) $(1.1^3 - 1)/0.1 = 0.331/0.1 = $ **3.3100** and $(1.01^3 - 1)/0.01 = $ **3.0301**. On the left, $x = 0.9$ gives 2.71 and $x = 0.99$ gives 2.9701. **Limit 3.** Algebraically, $x^3 - 1 = (x - 1)(x^2 + x + 1)$, so the quotient is $x^2 + x + 1 \to 3$.

### Solution 01-02.2

(a) Factor: $(x - 3)(x + 3)/(x - 3) = x + 3 \to$ **6**.

(b) Rationalize with the conjugate $\sqrt{4 + x} + 2$:

$$
\frac{\sqrt{4 + x} - 2}{x}\cdot\frac{\sqrt{4 + x} + 2}{\sqrt{4 + x} + 2} = \frac{(4 + x) - 4}{x(\sqrt{4 + x} + 2)} = \frac{1}{\sqrt{4 + x} + 2} \to \frac{1}{4} = \mathbf{0.25}.
$$

Check: at $x = 0.01$ the original expression is 0.24984 ✓.

(c) Factor: $x^2 + 3x + 2 = (x + 1)(x + 2)$, so the quotient is $x + 2 \to -1 + 2 = $ **1**.

(d) Expand: $(1 + h)^3 - 1 = 3h + 3h^2 + h^3$, so the quotient is $3 + 3h + h^2 \to$ **3**. This is the slope of $x^3$ at $x = 1$, a preview of the rule $(x^3)' = 3x^2$.

### Solution 01-02.3

(a) $\dfrac{\sin 5x}{x} = 5\cdot\dfrac{\sin 5x}{5x}$. As $x \to 0$, $\theta = 5x \to 0$, so the second factor tends to 1. **Limit 5.**

(b) $\dfrac{\tan x}{x} = \dfrac{\sin x}{x}\cdot\dfrac{1}{\cos x} \to 1 \cdot 1 = $ **1**.

(c) Multiply top and bottom by $1 + \cos x$: $\dfrac{1 - \cos^2 x}{x^2(1 + \cos x)} = \left(\dfrac{\sin x}{x}\right)^2\dfrac{1}{1 + \cos x} \to \dfrac{1}{2} = $ **0.5**.

(d) $\dfrac{x}{\sin\pi x} = \dfrac{1}{\pi}\cdot\dfrac{\pi x}{\sin\pi x} \to \dfrac{1}{\pi} = $ **0.3183**.

### Solution 01-02.4

(a) The left limit at 1 is $1^2 = 1$; the right limit (and value) is $2 + c$. Continuity requires $2 + c = 1$, so $c = $ **−1**.

(b) With $c = 0$: left limit **1**, right limit $2(1) = $ **2**. The jump is **1**.

(c) For $x < 0$, $\lvert x\rvert = -x$, so $\lvert x\rvert/x = -1$; for $x > 0$ it is $+1$. The one-sided limits are **−1** and **+1**. They differ, so no two-sided limit exists: a jump discontinuity (this is the sign function).

(d) $g(x) = (x - 3)(x + 3)/(x + 3) = x - 3$ for $x \ne -3$, so the limit is $-6$. Defining $g(-3) = $ **−6** removes the discontinuity.

### Solution 01-02.5

(a) Divide by $x^2$: $\dfrac{3 + 5/x^2}{2 - 1/x} \to \dfrac{3}{2} = $ **1.5**.

(b) Divide by $x^2$: $\dfrac{5/x + 1/x^2}{1 + 2/x^2} \to \dfrac{0}{1} = $ **0**. (The numerator's degree is lower.)

(c) This is an $\infty - \infty$ form. Multiply by the conjugate:

$$
\sqrt{x^2 + 4x} - x = \frac{(x^2 + 4x) - x^2}{\sqrt{x^2 + 4x} + x} = \frac{4x}{x\left(\sqrt{1 + 4/x} + 1\right)} = \frac{4}{\sqrt{1 + 4/x} + 1} \to \frac{4}{2} = \mathbf{2}.
$$

Check: at $x = 10^4$ the original expression is 1.9998 ✓.

(d) **0**: exponential decay beats any power (chapter §3.7).

(e) **0**: the logarithm grows more slowly than any positive power of $x$.

### Solution 01-02.6

(a) **Removable.** The quotient equals $x + 2$ away from 2, so the limit is 4. Engineering analog: sinc at 0, fixed by defining the value as 1.

(b) **Infinite.** Both one-sided limits are $+\infty$. Engineering analog: the impedance of an ideal parallel LC circuit at resonance, or a lossless resonator's response at its resonant frequency.

(c) **Jump.** Left limit 2, right limit (and value) 3. Engineering analog: an ADC's output code as the input voltage crosses a code boundary, or the current into a capacitor at a switching instant.

(d) **Oscillatory.** $\sin(1/x)$ oscillates infinitely often near 0 between −1 and 1. Engineering analog: none physical; real signals have finite bandwidth. It is a warning that "bounded" does not imply "has a limit".

(e) **Removable**, with limit 1 (chapter §3.3).

### Solution 01-02.7

(a) $\tau = L/R = 0.030/6 = 5\times10^{-3}$ s $= $ **5.000 ms**.

(b) Before the switch closes nothing flows: $i(0^-) = 0$ and $v_L(0^-) = 0$. Just after closing, $i(0^+) = 2(1 - e^{0}) = $ **0**, and $v_L(0^+) = 12e^{0} = $ **12 V**. The current is continuous; the inductor voltage jumps from 0 to 12 V. The current *must* be continuous because $v_L = L\,di/dt$: a jump in $i$ would need an infinite voltage, and equivalently the stored energy $\tfrac{1}{2}Li^2$ cannot change instantly. At $0^+$ the inductor carries no current, so no voltage drops across $R$, and the entire 12 V appears across $L$.

(c) As $t \to \infty$, $e^{-t/\tau} \to 0$, so $i \to 12/6 = $ **2 A** and $v_L \to 0$. The inductor ends up as a short circuit at DC.

(d) $t/\tau = 2$: $i = 2(1 - e^{-2}) = $ **1.729 A** and $v_L = 12e^{-2} = $ **1.624 V**. Check by KVL: $Ri + v_L = 6(1.729) + 1.624 = 12.0$ V ✓.

### Solution 01-02.8

(a)

| Compounding | $n$ | $(1 + 0.06/n)^n$ |
|---|---|---|
| Annual | 1 | **1.06000** |
| Quarterly | 4 | **1.06136** |
| Monthly | 12 | **1.06168** |
| Daily | 365 | **1.06183** |
| Continuous (limit) | ∞ | $e^{0.06} = $ **1.06184** |

The sequence increases toward its limit, with sharply diminishing gains.

(b) Let $a_n = (1 + r/n)^n$. Then $\ln a_n = n\ln(1 + r/n)$. Substitute $x = r/n$, so $n = r/x$ and $x \to 0$ as $n \to \infty$:

$$
\ln a_n = r\cdot\frac{\ln(1 + x)}{x} \;\longrightarrow\; r \cdot 1 = r .
$$

Because $\exp$ is continuous, $a_n = e^{\ln a_n} \to e^{r}$. $\blacksquare$

(c) Daily: effective rate $6.1831\%$. Continuous: $6.1837\%$. The difference is $0.00052$ percentage points, or **0.052 basis points**. Beyond daily compounding the limit is reached for all practical purposes.

### Solution 01-02.9

(a) KCL at the diode node:

$$
g(V) = \frac{3.3 - V}{10^4} - 10^{-15}\left(e^{V/V_T} - 1\right) = 0 .
$$

$g$ is continuous. $g(0) = 3.3\times10^{-4}$ A $> 0$. At $V = 1$, $10^{-15}e^{38.68} \approx 63$ A, so $g(1) < 0$. By the IVT, a root exists in $(0, 1)$, and it is unique because $g$ is decreasing.

(b) $n \ge \log_2(1/10^{-4}) = 13.3$, so **14** steps.

(c) Bisection (or any solver) gives $V = $ **0.6796 V** and $I = (3.3 - 0.6796)/10^4 = $ **0.2620 mA**.

(d) Two effects nearly cancel.

- The current falls from 4.308 mA to 0.2620 mA, a factor of 16.4, or 1.22 decades. At 59.5 mV per decade that alone would lower the voltage by about 72 mV.
- But $I_s$ is 10 times smaller here. That shifts the whole curve *up* by one decade's worth of voltage, $+59.5$ mV, because the diode needs a larger $V$ to carry the same current.

The net change is about $-72 + 59.5 \approx -13$ mV. The direct difference, from the unrounded operating points, is **0.0128 V**. Lesson: a diode's voltage is insensitive to its current (logarithmic), which is why "0.7 V" is such a durable rule of thumb.

### Solution 01-02.10

(a) Divide top and bottom by $f/f_c$: $\lvert H\rvert = 1/\sqrt{(f_c/f)^2 + 1} \to $ **1** as $f \to \infty$ (0 dB, the passband). As $f \to 0$, the numerator tends to 0 and the denominator to 1, so $\lvert H\rvert \to$ **0** (DC is blocked, as a coupling capacitor should).

(b) For $f \ll f_c$, $\sqrt{1 + (f/f_c)^2} \to 1$, so $\lvert H\rvert \sim f/f_c$. In dB that is $20\log_{10}(f/f_c)$, rising **+20 dB per decade** toward the corner.

(c)

- At $f = f_c = 100$ Hz: $\lvert H\rvert = 1/\sqrt{2}$, i.e. **−3.010 dB**. The asymptotes give 0 dB.
- At 10 Hz: $0.1/\sqrt{1.01}$, i.e. **−20.04 dB**. The asymptote gives −20 dB, an error of 0.043 dB.
- At 1 kHz: $10/\sqrt{101}$, i.e. **−0.0432 dB**. The asymptote gives 0 dB.

The high-pass is the mirror image of the low-pass in chapter Example 01-02.5.

### Solution 01-02.11

(a) Since $-1 \le \sin(1/x) \le 1$ and $x^2 \ge 0$, we have $-x^2 \le x^2\sin(1/x) \le x^2$. Both bounds tend to 0, so the squeeze gives a limit of **0**. The wild oscillation is crushed by the shrinking envelope.

(b) $-e^{-t} \le e^{-t}\cos 10t \le e^{-t}$, and $e^{-t} \to 0$, so $y \to 0$. The envelope falls below 0.01 when $e^{-t} < 0.01$, i.e. $t > \ln 100 = $ **4.605 s**. After that, $\lvert y\rvert \le e^{-t} < 0.01$ for all later times. (The bound is guaranteed; $\lvert y\rvert$ may dip below 0.01 earlier at zero crossings, but it does not *stay* there.)

(c) For $x > 0$: $-1/x \le \sin x/x \le 1/x$, and both bounds tend to 0. **Limit 0.** The sinc function's ripples die out as $1/x$.

### Solution 01-02.12

(a) The computed values are:

| $x$ | $(1 - \cos x)/x^2$ |
|---|---|
| $10^{-1}$ | **0.4996** (the true value; the limit is approached as $x^2/24$ shrinks) |
| $10^{-3}$ | 0.49999996 |
| $10^{-5}$ | 0.50000004 (now *above* 0.5: rounding error) |
| $10^{-7}$ | 0.4996 (wrong in the 4th digit) |
| $10^{-8}$ | 0 (completely wrong) |

The approach to 0.5 improves at first, then deteriorates, then collapses.

(b) $1 - \cos x \approx x^2/2$, and the stored $\cos x$ can be off by up to $\tfrac{1}{2}\times1.11\times10^{-16} = 5.55\times10^{-17}$. The relative error is therefore up to

$$
\frac{5.55\times10^{-17}}{x^2/2} = \frac{1.11\times10^{-16}}{x^2}.
$$

At $x = 10^{-5}$ that is **1.1×10^−6**; at $x = 10^{-7}$ it is $1.1\times10^{-2}$, i.e. **1.1%**. Both match the observed behavior. At $x = 10^{-8}$ the bound exceeds 100%: the difference is below the rounding granularity, and $\cos x$ rounds to exactly 1.

(c) Use $1 - \cos x = 2\sin^2(x/2)$, which involves no subtraction:

$$
\frac{1 - \cos x}{x^2} = \frac{2\sin^2(x/2)}{x^2} .
$$

At $x = 10^{-8}$ this gives **0.5000**, correct to full precision.

### Solution 01-02.13

(a)

| $h$ | $D(h)$ | Error $D - 1$ | $h/2$ |
|---|---|---|---|
| 0.1 | **1.0517** | 0.0517 | 0.05 |
| 0.01 | **1.0050** | 0.00502 | 0.005 |
| $10^{-5}$ | **1.0000050** | $5.0\times10^{-6}$ | $5\times10^{-6}$ |

The error tracks $h/2$. (It is the next term of the series $e^h = 1 + h + h^2/2 + \cdots$, divided by $h$; see [01-08](../chapters/01-08-sequences-series-and-taylor.md).)

(b) $E(h) = h/2 + \epsilon_{\text{mach}}/h$. The first term grows with $h$ and the second shrinks, so the sum is smallest where they balance: $h/2 = \epsilon_{\text{mach}}/h$, giving

$$
h^\ast = \sqrt{2\epsilon_{\text{mach}}} = \sqrt{4.44\times10^{-16}} = 2.1\times10^{-8}.
$$

The minimum error is $E(h^\ast) = h^\ast/2 + h^\ast/2 = h^\ast = $ **2.1×10^−8**. So the best a forward difference can do in double precision is about 8 correct digits, half of the 16 available.

(c) The estimate predicts a rounding error of about $2.22\times10^{-16}/10^{-12} = $ **2.2×10^−4**. Python gives $D(10^{-12}) = 1.000089$, an error of $8.9\times10^{-5}$: the same order of magnitude, as an estimate should be. Shrinking $h$ from $10^{-5}$ to $10^{-12}$ made the answer about 18 times *worse*.

(d) `expm1` evaluates $e^h - 1$ directly, for example from its series $h + h^2/2 + \cdots$, without first forming the number $e^h \approx 1$ and then subtracting 1. No nearly equal numbers are subtracted, so no catastrophic cancellation occurs. `math.expm1(1e-12)/1e-12` returns 1.0000000000005, correct to full precision.

### Solution 01-02.14

(a) Charge is conserved: $Q = C_1V_0 = 10\times10^{-6}\times5 = 50$ µC, shared over $C_1 + C_2 = 20$ µF. The final voltage is $50/20 = $ **2.5 V**.

(b) Before: $\tfrac{1}{2}C_1V_0^2 = \tfrac{1}{2}(10^{-5})(25) = $ **125 µJ**. After: $\tfrac{1}{2}(20\times10^{-6})(2.5)^2 = $ **62.5 µJ**. Lost: **62.5 µJ**, exactly half.

(c) $C_s = (10 \times 10)/(10 + 10) = 5$ µF.

- $R = 1\ \Omega$: $\tau = 5$ µs and peak current $5/1 = $ **5 A**.
- $R = 0.01\ \Omega$: $\tau = 50$ ns and peak current **500 A**.

(The full 5 V difference appears across $R$ at $t = 0^+$, because both capacitor voltages are continuous.)

(d) As $R \to 0$: $\tau = RC_s \to 0$ and the peak current $5/R \to \infty$, yet the lost energy stays exactly 62.5 µJ. The limit of the physical circuit as $R \to 0$ is a zero-time, infinite-current event that still dissipates half the energy. The ideal model with $R = 0$ cannot describe it: it demands that both capacitor voltages jump (to conserve charge) while energy vanishes with no resistor to absorb it. The contradiction says the idealization has broken down. In a real circuit, as $R$ shrinks, the loop's **inductance** takes over: the current rings instead of decaying instantly, energy is dissipated in whatever resistance remains, radiated, or lost in a spark at the switch contacts. Lesson: limits of physical models can be **singular**. The answer for "very small $R$" need not match the answer at "$R = 0$", and engineers must know which one applies. The same charge-sharing loss is a central design issue in switched-capacitor power converters ([Course 22](../../22-power-electronics-and-energy-conversion/README.md)).

### Solution 01-02.15

(a) The ratio is $N^2/(N\log_2 N) = N/\log_2 N$.

- At $N = 1024 = 2^{10}$: $1024/10 = $ **102.4**.
- At $N = 2^{20}$: $2^{20}/20 = $ **5.243×10^4**.

For the limit, $\dfrac{N\log_2 N}{N^2} = \dfrac{\log_2 N}{N} = \dfrac{1}{\ln 2}\cdot\dfrac{\ln N}{N} \to 0$, by the growth hierarchy.

(b) At $N = 10^{10}$: $\ln N = 23.03$ and $N^{0.1} = 10$, so the ratio is **2.303**. The "slower" function is still more than twice as large.

(c) Solving $\ln N = N^{0.1}$ numerically (for example with `scipy.optimize.brentq` on $\ln N - N^{0.1}$) gives **N ≈ 3.06** and **N ≈ 3.43×10^15**. Between them, $\ln N$ is the *larger* function. The asymptotic ordering only takes over beyond about $3\times10^{15}$.

(d) An asymptotic statement says nothing about *where* the crossover is. "Scales better asymptotically" is a claim about arbitrarily large sizes. A product runs at specific sizes, where constants and lower-order terms may dominate. Always ask for measurements at the sizes that matter.

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 01-02.1a | (e^x−1)/x at 0.1 | 1.0517 | — |
| 01-02.1b | (e^x−1)/x at 0.01 | 1.0050 | — |
| 01-02.1c | sin 3x / x at 0.1 | 2.9552 | — |
| 01-02.1d | sin 3x / x at 0.01 | 2.9996 | — |
| 01-02.1e | (x³−1)/(x−1) at 1.1 | 3.3100 | — |
| 01-02.1f | (x³−1)/(x−1) at 1.01 | 3.0301 | — |
| 01-02.2a | (a) | 6 | — |
| 01-02.2b | (b) | 0.25 | — |
| 01-02.2c | (c) | 1 | — |
| 01-02.2d | (d) | 3 | — |
| 01-02.3a | (a) | 5 | — |
| 01-02.3b | (b) | 1 | — |
| 01-02.3c | (c) | 0.5 | — |
| 01-02.3d | (d) | 0.3183 | — |
| 01-02.4a | c for continuity | −1 | — |
| 01-02.4b | left limit with c = 0 | 1 | — |
| 01-02.4c | right limit with c = 0 | 2 | — |
| 01-02.4d | jump | 1 | — |
| 01-02.4e | left limit of abs(x)/x | −1 | — |
| 01-02.4f | right limit of abs(x)/x | 1 | — |
| 01-02.4g | g(−3) for continuity | −6 | — |
| 01-02.5a | (a) | 1.5 | — |
| 01-02.5b | (b) | 0 | — |
| 01-02.5c | (c) | 2 | — |
| 01-02.5d | (d) | 0 | — |
| 01-02.5e | (e) | 0 | — |
| 01-02.7a | τ | 5.000 | ms |
| 01-02.7b | i(0⁺) | 0 | A |
| 01-02.7c | v_L(0⁺) | 12 | V |
| 01-02.7d | final current | 2 | A |
| 01-02.7e | i(10 ms) | 1.729 | A |
| 01-02.7f | v_L(10 ms) | 1.624 | V |
| 01-02.8a | annual | 1.06000 | — |
| 01-02.8b | quarterly | 1.06136 | — |
| 01-02.8c | monthly | 1.06168 | — |
| 01-02.8d | daily | 1.06183 | — |
| 01-02.8e | continuous | 1.06184 | — |
| 01-02.8f | daily vs continuous gap | 0.052 | bp |
| 01-02.9a | bisection steps for 0.1 mV | 14 | — |
| 01-02.9b | operating-point voltage | 0.6796 | V |
| 01-02.9c | operating-point current | 0.2620 | mA |
| 01-02.9d | voltage difference from Ex 01-02.4 | 0.0128 | V |
| 01-02.10a | magnitude at 100 Hz | −3.010 | dB |
| 01-02.10b | magnitude at 10 Hz | −20.04 | dB |
| 01-02.10c | magnitude at 1 kHz | −0.0432 | dB |
| 01-02.11a | time for envelope below 0.01 | 4.605 | s |
| 01-02.12a | (1−cos x)/x² at 0.1 | 0.4996 | — |
| 01-02.12b | rounding bound at x = 1e−5 | 1.1×10^-6 | — |
| 01-02.12c | rounding bound at x = 1e−7 | 1.1 | % |
| 01-02.12d | stable form at 1e−8 | 0.5000 | — |
| 01-02.12e | computed value at 1e−3 | 0.49999996 | — |
| 01-02.12f | computed value at 1e−5 | 0.50000004 | — |
| 01-02.12g | computed value at 1e−7 | 0.4996 | — |
| 01-02.12h | computed value at 1e−8 | 0 | — |
| 01-02.13a | D(0.1) | 1.0517 | — |
| 01-02.13b | D(0.01) | 1.0050 | — |
| 01-02.13c | D(1e−5) | 1.0000050 | — |
| 01-02.13d | optimal h | 2.1×10^-8 | — |
| 01-02.13e | minimum error estimate | 2.1×10^-8 | — |
| 01-02.13f | predicted rounding error at h = 1e−12 | 2.2×10^-4 | — |
| 01-02.14a | final voltage | 2.5 | V |
| 01-02.14b | energy before | 125 | µJ |
| 01-02.14c | energy after | 62.5 | µJ |
| 01-02.14d | energy lost | 62.5 | µJ |
| 01-02.14e | τ for R = 1 Ω | 5 | µs |
| 01-02.14f | peak current for R = 1 Ω | 5 | A |
| 01-02.14g | τ for R = 0.01 Ω | 50 | ns |
| 01-02.14h | peak current for R = 0.01 Ω | 500 | A |
| 01-02.15a | cost ratio at N = 1024 | 102.4 | — |
| 01-02.15b | cost ratio at N = 2^20 | 5.243×10^4 | — |
| 01-02.15c | ln N / N^0.1 at 1e10 | 2.303 | — |
| 01-02.15d | lower crossover | 3.06 | — |
| 01-02.15e | upper crossover | 3.43×10^15 | — |
