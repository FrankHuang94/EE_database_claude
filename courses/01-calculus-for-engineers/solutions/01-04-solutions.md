# Solutions 01-04 · Applications of Derivatives

Problems: [01-04 problems](../problems/01-04-problems.md) · Chapter: [01-04](../chapters/01-04-applications-of-derivatives.md)

Every numerical answer below is listed in the answer key at the end and is recomputed independently by [verify_01_04.py](../verify/verify_01_04.py).

---

## Solutions

### Solution 01-04.1

(a) $f'(x) = 3x^2 - 3 = 0$ at $x = \pm1$. Then $f''(x) = 6x$:

- $f''(-1) = -6 < 0$, a local maximum, $f(-1) = $ **2**;
- $f''(1) = 6 > 0$, a local minimum, $f(1) = $ **−2**.

(b) Compare the critical values with the endpoint values $f(-2) = -8 + 6 = -2$ and $f(3) = 27 - 9 = 18$.

- **Global maximum: 18**, at the endpoint $x = 3$. The interior local maximum (2) is not the global one.
- **Global minimum: −2**, attained twice, at $x = -2$ and $x = 1$.

### Solution 01-04.2

(a) $f'(x) = e^{-x} - xe^{-x} = (1 - x)e^{-x}$, zero at $x = 1$. It changes from + to −, so this is a maximum, $f(1) = e^{-1} = $ **0.3679**.

(b) $f''(x) = -e^{-x} - (1 - x)e^{-x} = (x - 2)e^{-x}$, zero at $x = 2$, where the sign changes (concave down before, concave up after). The inflection point is at $x = 2$, $f(2) = 2e^{-2} = $ **0.2707**.

(c) $x/e^x$ is an ∞/∞ form. L'Hôpital gives $1/e^x \to$ **0**.

### Solution 01-04.3

(a) Both numerator and denominator → 0. The first application gives $\dfrac{e^x - 1}{2x}$, still 0/0. The second gives $\dfrac{e^x}{2} \to$ **0.5**.

(b) Write $x\ln x = \dfrac{\ln x}{1/x}$, a $-\infty/\infty$ form. L'Hôpital gives $\dfrac{1/x}{-1/x^2} = -x \to$ **0**.

(c) 0/0 at $x = 1$. L'Hôpital gives $\dfrac{1/x}{1} \to$ **1**.

(d) 0/0. The first application gives $\dfrac{3\sin 3x}{2x}$, still 0/0. The second gives $\dfrac{9\cos 3x}{2} \to$ **4.5**. (Alternatively, $1 - \cos u \approx u^2/2$ with $u = 3x$ gives $9x^2/2 \div x^2$.)

(e) Let $y = x^{1/x}$, so $\ln y = \dfrac{\ln x}{x}$, an ∞/∞ form → $\dfrac{1/x}{1} \to 0$. So $y \to e^0 = $ **1**.

### Solution 01-04.4

(a) $f(x) = \sqrt{x}$ at $a = 4$: $f' = 1/(2\sqrt{x}) = 1/4$, so $L(4.1) = 2 + 0.1/4 = $ **2.025**. Exact: **2.0248**. Since $f''(x) = -\tfrac{1}{4}x^{-3/2}$, $f''(4) = -1/32$, and the predicted error is $\tfrac{1}{2}(-1/32)(0.1)^2 = $ **−1.56×10^−4**. The actual error, exact minus linear, is $-1.54\times10^{-4}$ ✓.

(b) $e^x$ at 0: $L = 1 + x$, so $e^{0.05} \approx$ **1.05**. Exact: **1.051**. The linearization underestimates, because $e^x$ curves up.

(c) $\sin x$ at 0: $L = x$, so $\sin 0.2 \approx$ **0.2**. Exact: **0.1987**.

(d) $(1 + x)^{10}$ at 0: $L = 1 + 10x$, so $1.02^{10} \approx$ **1.2**. Exact: **1.219**. Compounding (the curvature) adds 0.019, which is the "convexity" a finance reader will recognize.

### Solution 01-04.5

(a) $R_L = R_s = $ **2 kΩ**, and $P_{max} = V_s^2/(4R_s) = 1/8000$ W $= $ **125 µW**.

(b) $P = 1^2\times1000/3000^2 = $ **111.1 µW**, or **88.9%** of the maximum.

(c) With $R_L$ fixed, $P = V_s^2R_L/(R_s + R_L)^2$ *decreases* as $R_s$ grows, so the best choice is $R_s = $ **0**. There is no contradiction. Part (a) optimized the load for a given source; this part optimizes the source for a given load. The variable you optimize over changes the answer. Low source resistance is always better for delivering power; matching is the right answer only when the source is fixed.

### Solution 01-04.6

(a) $T'(n) = 20 - 800/n^2 = 0$ gives $n^\ast = \sqrt{40} = $ **6.325**, and $T_{min} = 2\sqrt{20\times800} = $ **253.0 ps** (the balance principle, §3.4). $T''(n) = 1600/n^3 > 0$, so it is a minimum.

(b) $T(6) = 120 + 133.3 = $ **253.3 ps** and $T(7) = 140 + 114.3 = 254.3$ ps. The best integer is **6**.

(c) $T(1) = 20 + 800 = $ **820 ps** (the driver plus the whole wire). Repeaters make the wire $820/253.3 = $ **3.2 times** faster.

(d) A wire's RC delay is proportional to $R\times C$, and both grow with length, so the delay grows as length squared. Each of the $n$ segments has length $L/n$, so its delay is $(1/n)^2$ of the whole. Summing $n$ segments gives $n\times(1/n^2) = 1/n$ of the unrepeated delay.

### Solution 01-04.7

(a) $f(x) = x^{-1} - a$ and $f'(x) = -x^{-2}$. So

$$
x_{k+1} = x_k - \frac{x_k^{-1} - a}{-x_k^{-2}} = x_k + x_k - ax_k^2 = x_k(2 - ax_k).
$$

Only multiplication and subtraction are needed.

(b) $x_1 = 0.3(2 - 0.9) = $ **0.33**; $x_2 = 0.33(2 - 0.99) = $ **0.3333**; $x_3 = 0.3333(2 - 0.9999) = $ **0.33333333**.

(c) $1 - ax_{k+1} = 1 - ax_k(2 - ax_k) = 1 - 2ax_k + a^2x_k^2 = (1 - ax_k)^2$, so $\varepsilon_{k+1} = \varepsilon_k^2$ exactly. With $\varepsilon_0 = 1 - 0.9 = 0.1$: $\varepsilon_1 = $ **0.01**, $\varepsilon_2 = $ **10^−4**, $\varepsilon_3 = $ **10^−8**.

(d) The exponent doubles each iteration: $2^{-8} \to 2^{-16} \to 2^{-32} \to 2^{-64}$. **3 iterations** pass $2^{-53}$.

### Solution 01-04.8

(a) $f = \arctan x$ and $f' = 1/(1 + x^2)$, so $x_{k+1} = x_k - \arctan(x_k)(1 + x_k^2)$.

(b) The iterates are:

| $k$ | from $x_0 = 1.0$ | from $x_0 = 1.5$ |
|---|---|---|
| 1 | **−0.5708** | **−1.694** |
| 2 | 0.1169 | 2.321 |
| 3 | −0.001061 | −5.114 |
| 4 | $8\times10^{-10}$ | 32.30 |

From 1.0, the iterates alternate in sign and converge quickly, in fact *cubically* at the end: $\lvert e_4\rvert/\lvert e_3\rvert^3 = 0.667$. The reason is that $f''(0) = 0$ for arctan (it is odd), so the quadratic error term of the chapter's formula vanishes. Expanding, $x - \arctan x\,(1 + x^2) = -\tfrac23x^3 + \cdots$, so $e_{k+1} \approx -\tfrac23e_k^3$. From 1.5, they alternate in sign with *growing* magnitude: divergence. The tangent of the flattening arctan curve, far from the root, is nearly horizontal, and it throws the next guess far past the root.

(c) Setting $x_{k+1} = -x_k$ gives $2x = (1 + x^2)\arctan x$. Solving numerically (bisection on $[1, 2]$) gives $x_c = $ **1.392**. Starting below it converges; starting above it diverges.

(d) Add a bracket and a bisection fallback (a hybrid method), or damp each step: halve it while $\lvert f\rvert$ does not decrease. SPICE limits the per-iteration voltage change for the same reason.

### Solution 01-04.9

(a) $C = \varepsilon_0A/d = 8.854\times10^{-12}\times10^{-6}/(2\times10^{-6}) = $ **4.427 pF**.

(b) $\dfrac{dC}{dt} = -\dfrac{\varepsilon_0A}{d^2}\dfrac{dd}{dt} = -\dfrac{8.854\times10^{-18}}{4\times10^{-12}}\times10^{-3} = -2.214\times10^{-9}$ F/s. Then $i = V\,dC/dt = 5\times(-2.214\times10^{-9}) = $ **−11.07 nA**. The negative sign means charge flows *out* of the capacitor as it loses capacitance.

(c) $dC/dt \propto 1/d^2$, so halving the gap multiplies the current by **4**. This is why MEMS microphones and accelerometers use micrometer gaps, and also why they are fragile: the electrostatic force grows as $1/d^2$ too ("pull-in").

### Solution 01-04.10

(a) $P = 25/100 = $ **0.25 W**.

(b) The elasticities are $S_V = 2$ and $S_R = -1$. Worst case: $2(1\%) + 1(2\%) = $ **4%**, i.e. ±**0.01 W**.

(c) RSS: $\sqrt{(2\times1)^2 + (1\times2)^2}\% = \sqrt{8}\% = $ **2.828%**, i.e. ±**0.00707 W**.

(d) $P \propto V^2$, so a 1% error in $V$ becomes a 2% error in $P$: the exponent is the elasticity. Squared quantities double relative errors, a useful rule for any power or energy measurement.

### Solution 01-04.11

(a) By the MVT, $\lvert\Delta v\rvert \le 1\text{ V/µs}\times2\text{ µs} = $ **2 V**.

(b) $\lvert\Delta T\rvert \le 0.5\times10 = $ **5 K**.

(c) By the MVT, $\sin a - \sin b = \cos(c)(a - b)$ for some $c$ between $a$ and $b$. Since $\lvert\cos c\rvert \le 1$, $\lvert\sin a - \sin b\rvert \le \lvert a - b\rvert$. $\blacksquare$

(d) $\lvert dv/dt\rvert = \lvert i\rvert/C \le 0.01/10^{-6} = 10^4$ V/s, so $\lvert\Delta v\rvert \le 10^4\times50\times10^{-6} = $ **0.5 V**.

### Solution 01-04.12

(a) $V^\ast = (B/2A)^{1/3} = (0.1/1.6)^{1/3} = 0.0625^{1/3} = $ **0.3969 V**, and $E(V^\ast) = 0.8(0.1575) + 0.1/0.3969 = 0.1260 + 0.2520 = $ **0.3780 pJ**.

(b) $E(0.9) = 0.8(0.81) + 0.1/0.9 = 0.648 + 0.111 = $ **0.7591 pJ**, so the optimum saves a factor of **2.008**.

(c) At the optimum, $2AV^\ast = B/V^{\ast2}$. Multiply by $V^\ast/2$: $AV^{\ast2} = \tfrac{1}{2}B/V^\ast$. Switching energy is half of leakage energy, for any $A$, $B$. $\blacksquare$

(d) **Up.** If delay grows exponentially below threshold, leakage energy (leakage power times delay) rises much faster as $V$ falls than $B/V$ suggests. The balance point moves to a higher voltage. This is why measured minimum-energy points sit near or slightly below threshold rather than far below it.

### Solution 01-04.13

(a) Expand: $T = \dfrac{600}{n} + 600\times0.04 + 40 + 40\times0.04\,n = 64 + \dfrac{600}{n} + 1.6n$. This is the balance form $an + b/n$ plus a constant, with $a = 1.6$ and $b = 600$. So $n^\ast = \sqrt{600/1.6} = $ **19.36**, and $T_{min} = 64 + 2\sqrt{960} = $ **125.97 ps**.

(b) $T(1) = $ **665.6 ps**; $T(5) = $ **192.0 ps**; $T(19) = $ **125.98 ps** (the best integer; $T(20) = 126.0$ ps). The speedup over $n = 1$ is $665.6/125.98 = $ **5.28×**.

(c) At half the optimal depth (9.68) and at double (38.7), $T = $ **141.46 ps**, only **12.3%** slower. The optimum is broad. That is why real designs can sit some distance from the "optimal" depth for power or design-effort reasons.

(d) $T = 52 + 600/n + 0.8n$, so $n^\ast = \sqrt{600/0.8} = $ **27.39**, with $T_{min} = $ **95.82 ps**. Better branch prediction justifies deeper pipelines. This is the historical logic of the deep-pipeline era (Hartstein and Puzak, ISCA 2002, analyzed it in this spirit), and also part of why power limits later pulled depths back down.

### Solution 01-04.14

(a) The errors $e_k = x_k - \sqrt{2}$ are $8.579\times10^{-2}$, $2.453\times10^{-3}$, $2.124\times10^{-6}$ and $1.595\times10^{-12}$. The ratios $e_{k+1}/e_k^2$ are **0.3333**, **0.3529** and **0.3535**.

(b) $f'(r) = 2\sqrt{2}$ and $f'' = 2$, so $f''/(2f') = 2/(4\sqrt{2}) = 1/(2\sqrt{2}) = $ **0.3536**. The ratios approach it ✓.

(c) For $f = x^2 - 2$, $f'' = 2$ is constant and $f'(x_k) = 2x_k$, so the chapter's formula is *exact*: $e_{k+1} = e_k^2/(2x_k)$. The ratios are therefore $1/(2x_k)$ at the current iterate: $1/(2\times1.5) = 0.3333$ at $x_1 = 1.5$, then $1/(2\times1.41667) = 0.3529$, then $1/(2\times1.414216) = 0.3535$. As $x_k \to \sqrt2$ they converge to the limiting constant $1/(2\sqrt2)$.

### Solution 01-04.15

(a) $dT/dt = \dfrac{PR_{th}}{\tau}e^{-t/\tau}$, which is $50/2 = $ **25 K/s** at $t = 0$. The steady state is $40 + 50 = $ **90 °C**. Solve $40 + 50(1 - e^{-t/2}) = 85$: $e^{-t/2} = 0.1$, so $t = 2\ln 10 = $ **4.605 s**.

(b) At 150 W the steady state would be 115 °C. Solve $45 = 75(1 - e^{-t/2})$: $e^{-t/2} = 0.4$, so $t = -2\ln 0.4 = $ **1.833 s**. The linear estimate uses the initial rate $75/2 = 37.5$ K/s: $45/37.5 = $ **1.2 s**. The linear estimate is **safer**. The heating rate only *decreases* over time, so the true temperature always lies below the tangent line, and the tangent reaches 85 °C first. A controller using the linear estimate throttles early and never overshoots the limit, at the cost of 0.6 s of lost turbo.

(c) Sustainable forever: $40 + 0.5P \le 85$, so $P \le $ **90 W**.

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 01-04.1a | local maximum value | 2 | — |
| 01-04.1b | local minimum value | −2 | — |
| 01-04.1c | global maximum | 18 | — |
| 01-04.1d | global minimum | −2 | — |
| 01-04.2a | maximum value | 0.3679 | — |
| 01-04.2b | value at inflection | 0.2707 | — |
| 01-04.2c | limit at infinity | 0 | — |
| 01-04.3a | (a) | 0.5 | — |
| 01-04.3b | (b) | 0 | — |
| 01-04.3c | (c) | 1 | — |
| 01-04.3d | (d) | 4.5 | — |
| 01-04.3e | (e) | 1 | — |
| 01-04.4a | linear estimate √4.1 | 2.025 | — |
| 01-04.4b | exact √4.1 | 2.0248 | — |
| 01-04.4c | predicted error | −1.56×10^-4 | — |
| 01-04.4d | linear e^0.05 | 1.05 | — |
| 01-04.4e | exact e^0.05 | 1.051 | — |
| 01-04.4f | linear sin 0.2 | 0.2 | — |
| 01-04.4g | exact sin 0.2 | 0.1987 | — |
| 01-04.4h | linear 1.02^10 | 1.2 | — |
| 01-04.4i | exact 1.02^10 | 1.219 | — |
| 01-04.5a | optimal load | 2 | kΩ |
| 01-04.5b | maximum power | 125 | µW |
| 01-04.5c | power into 1 kΩ | 111.1 | µW |
| 01-04.5d | fraction of maximum | 88.9 | % |
| 01-04.5e | best R_s for fixed load | 0 | Ω |
| 01-04.6a | continuous optimum n | 6.325 | — |
| 01-04.6b | continuous minimum delay | 253.0 | ps |
| 01-04.6c | best integer n | 6 | — |
| 01-04.6d | delay with 6 repeaters | 253.3 | ps |
| 01-04.6e | single-segment delay including driver | 820 | ps |
| 01-04.6f | speed-up from repeaters | 3.2 | — |
| 01-04.7a | x1 | 0.33 | — |
| 01-04.7b | x2 | 0.3333 | — |
| 01-04.7c | x3 | 0.33333333 | — |
| 01-04.7d | ε1 | 0.01 | — |
| 01-04.7e | ε2 | 1×10^-4 | — |
| 01-04.7f | ε3 | 1×10^-8 | — |
| 01-04.7g | iterations to double precision | 3 | — |
| 01-04.8a | first iterate from 1.0 | −0.5708 | — |
| 01-04.8b | first iterate from 1.5 | −1.694 | — |
| 01-04.8c | critical starting value | 1.392 | — |
| 01-04.8d | second iterate from 1.0 | 0.1169 | — |
| 01-04.8e | third iterate from 1.0 | −0.001061 | — |
| 01-04.8f | fourth iterate from 1.0 | 8×10^-10 | — |
| 01-04.8g | cubic error ratio | 0.667 | — |
| 01-04.8h | second iterate from 1.5 | 2.321 | — |
| 01-04.8i | third iterate from 1.5 | −5.114 | — |
| 01-04.8j | fourth iterate from 1.5 | 32.30 | — |
| 01-04.9a | rest capacitance | 4.427 | pF |
| 01-04.9b | current | −11.07 | nA |
| 01-04.9c | factor for half the gap | 4 | — |
| 01-04.10a | nominal power | 0.25 | W |
| 01-04.10b | worst-case relative | 4 | % |
| 01-04.10c | worst-case absolute | 0.01 | W |
| 01-04.10d | RSS relative | 2.828 | % |
| 01-04.10e | RSS absolute | 0.00707 | W |
| 01-04.11a | max output change | 2 | V |
| 01-04.11b | max temperature change | 5 | K |
| 01-04.11c | max capacitor voltage change | 0.5 | V |
| 01-04.12a | V* | 0.3969 | V |
| 01-04.12b | E(V*) | 0.3780 | pJ |
| 01-04.12c | E(0.9 V) | 0.7591 | pJ |
| 01-04.12d | saving factor | 2.008 | — |
| 01-04.13a | optimal depth | 19.36 | — |
| 01-04.13b | minimum time per instruction | 125.97 | ps |
| 01-04.13c | T(1) | 665.6 | ps |
| 01-04.13d | T(5) | 192.0 | ps |
| 01-04.13e | T(19) | 125.98 | ps |
| 01-04.13f | speedup over n = 1 | 5.28 | — |
| 01-04.13g | T at half or double depth | 141.46 | ps |
| 01-04.13h | optimal depth, hazard 0.02 | 27.39 | — |
| 01-04.13i | minimum T, hazard 0.02 | 95.82 | ps |
| 01-04.13j | slowdown at half or double depth | 12.3 | % |
| 01-04.14a | ratio e2/e1² | 0.3333 | — |
| 01-04.14b | ratio e3/e2² | 0.3529 | — |
| 01-04.14c | ratio e4/e3² | 0.3535 | — |
| 01-04.14e | x2 | 1.41667 | — |
| 01-04.14f | x3 | 1.414216 | — |
| 01-04.14d | limit 1/(2√2) | 0.3536 | — |
| 01-04.15a | initial heating rate | 25 | K/s |
| 01-04.15b | steady state at 100 W | 90 | °C |
| 01-04.15c | time to 85 °C at 100 W | 4.605 | s |
| 01-04.15d | time to 85 °C at 150 W | 1.833 | s |
| 01-04.15e | linear estimate at 150 W | 1.2 | s |
| 01-04.15f | maximum sustained power | 90 | W |
