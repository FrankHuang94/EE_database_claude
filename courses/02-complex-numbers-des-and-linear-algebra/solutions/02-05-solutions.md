# Solutions 02-05 · The Laplace Transform for ODEs

Problems: [02-05 problems](../problems/02-05-problems.md) · Chapter: [02-05](../chapters/02-05-laplace-transform-for-odes.md)

Every numerical answer below is listed in the answer key at the end and is recomputed independently by [verify_02_05.py](../verify/verify_02_05.py).

---

## Solutions

### Solution 02-05.1

(a) $\int_0^\infty e^{-2t}e^{-st}dt = \Big[\frac{-e^{-(s + 2)t}}{s + 2}\Big]_0^\infty = \dfrac{1}{s + 2}$, converging for $\operatorname{Re}s > -2$.

(b) By parts with $u = t$, $dv = e^{-st}dt$: $\Big[-\frac{te^{-st}}{s}\Big]_0^\infty + \frac1s\int_0^\infty e^{-st}dt = \dfrac{1}{s^2}$, for $\operatorname{Re}s > 0$.

(c) $5\int_3^\infty e^{-st}dt = \dfrac{5e^{-3s}}{s}$, for $\operatorname{Re}s > 0$.

### Solution 02-05.2

(a) By parts with $u = t^n$ and $dv = e^{-st}dt$: $\mathcal{L}\{t^n\} = \Big[-\frac{t^ne^{-st}}{s}\Big]_0^\infty + \frac{n}{s}\int_0^\infty t^{n-1}e^{-st}dt = \frac{n}{s}\mathcal{L}\{t^{n-1}\}$, since the boundary term vanishes for $n \ge 1$ and $\operatorname{Re}s > 0$. Starting from $\mathcal{L}\{1\} = 1/s$ and applying this $n$ times gives $\frac{n}{s}\cdot\frac{n - 1}{s}\cdots\frac{1}{s}\cdot\frac{1}{s} = \frac{n!}{s^{n+1}}$.

(b) $\mathcal{L}\{t^3\} = 6/s^4$. With the $s$-shift, $\mathcal{L}\{t^2e^{-t}\} = 2/(s + 1)^3$.

### Solution 02-05.3

(a) $\dfrac{2s}{s^2 + 25} - \dfrac{15}{s^2 + 25} = \dfrac{2s - 15}{s^2 + 25}$.
(b) The $s$-shift of $4/(s^2 + 16)$: $\dfrac{4}{(s + 3)^2 + 16}$.
(c) The time shift of $t \leftrightarrow 1/s^2$ by 2: $\dfrac{e^{-2s}}{s^2}$.

### Solution 02-05.4

(a) Cover-up: $\dfrac{6}{s(s + 3)} = \dfrac{2}{s} - \dfrac{2}{s + 3}$, so $f = 2(1 - e^{-3t})$ and $f(1) = $ **1.900**.
(b) $\dfrac{2s}{s^2 + 9} + \dfrac{3}{s^2 + 9}$, so $f = 2\cos3t + \sin3t$ and $f(1) = $ **−1.839**.
(c) $\mathcal{L}\{t^2e^{-2t}\} = 2/(s + 2)^3$, so $f = \tfrac12t^2e^{-2t}$ and $f(1) = $ **0.06767**.

### Solution 02-05.5

Write $\dfrac{s + 4}{s^2(s + 2)} = \dfrac{A}{s} + \dfrac{B}{s^2} + \dfrac{C}{s + 2}$.

- Cover-up for the double pole's top coefficient: $B = \big[(s + 4)/(s + 2)\big]_{s=0} = 2$.
- $A = \dfrac{d}{ds}\left[\dfrac{s + 4}{s + 2}\right]_{s=0} = \left[\dfrac{(s + 2) - (s + 4)}{(s + 2)^2}\right]_{s=0} = -\dfrac{2}{4} = -0.5$.
- Cover-up at −2: $C = \big[(s + 4)/s^2\big]_{s=-2} = 2/4 = 0.5$.

So $y = -0.5 + 2t + 0.5e^{-2t}$ and $y(1) = $ **1.568**. **Check:** $y(0) = 0$, consistent with the initial-value theorem, $\lim_{s\to\infty}sY = \lim\frac{s + 4}{s(s + 2)} = 0$ ✓.

### Solution 02-05.6

$s^2 + 4s + 13 = (s + 2)^2 + 9$ and $3s + 7 = 3(s + 2) + 1$, so

$$
Y = 3\frac{s + 2}{(s + 2)^2 + 9} + \frac13\cdot\frac{3}{(s + 2)^2 + 9}, \qquad y = e^{-2t}\left(3\cos3t + \tfrac13\sin3t\right).
$$

$y(0.5) = $ **0.2004**. Initial-value theorem: $\lim_{s\to\infty}\frac{s(3s + 7)}{s^2 + 4s + 13} = 3 = y(0^+)$ ✓.

### Solution 02-05.7

$sY - 5 + 4Y = 8/s$, so $Y = \dfrac{5}{s + 4} + \dfrac{8}{s(s + 4)} = \dfrac{5}{s + 4} + \dfrac{2}{s} - \dfrac{2}{s + 4} = \dfrac{2}{s} + \dfrac{3}{s + 4}$. Then $y = 2 + 3e^{-4t}$, and $y(0.25) = 2 + 3e^{-1} = $ **3.104**.

### Solution 02-05.8

$(s^2 + 4)Y = \dfrac{1}{s^2 + 1}$, so $Y = \dfrac{1}{(s^2 + 1)(s^2 + 4)} = \dfrac13\left(\dfrac{1}{s^2 + 1} - \dfrac{1}{s^2 + 4}\right)$ (treat $s^2$ as the variable for the split). Hence

$$
y = \tfrac13\sin t - \tfrac16\sin2t, \qquad y(\pi/2) = \tfrac13 - 0 = 0.3333 .
$$

$\tfrac13\sin t$ is the steady state at the input frequency (ERF: $1/p(j) = 1/(4 - 1)$). $-\tfrac16\sin2t$ is the natural response at $\omega_0 = 2$, which never decays because there is no damping.

### Solution 02-05.9

$V(s) = \dfrac{1}{1 + 2s}\cdot\dfrac{10e^{-s}}{s}$. The step response of $1/(1 + 2s)$ to 10 V is $10(1 - e^{-t/2})$, so by the time shift

$$
v(t) = 10\left(1 - e^{-(t - 1)/2}\right)u(t - 1)\text{ V}, \qquad v(3) = 10(1 - e^{-1}) = 6.321\text{ V}.
$$

### Solution 02-05.10

(a) $(s^2 + 2s + 5)Y = 3$, so $Y = \dfrac{3}{(s + 1)^2 + 4} = \dfrac32\cdot\dfrac{2}{(s + 1)^2 + 4}$ and $y = \tfrac32e^{-t}\sin2t$.

(b) $y(0^+) = 0$, and $y' = \tfrac32e^{-t}(2\cos2t - \sin2t)$ gives $y'(0^+) = 3$. The impulse delivers its whole area to the highest derivative: integrating $y'' = 3\delta - 2y' - 5y$ across $t = 0$ gives a jump of 3 in $y'$ and none in $y$. (Mechanically: a hammer blow changes the velocity instantly, not the position.)

(c) $y' = 0$ when $\tan2t = 2$, first at $t = \tfrac12\arctan2 = $ **0.5536**, where $y = $ **0.7713**.

### Solution 02-05.11

(a) $f(0^+) = \lim_{s\to\infty}\dfrac{2s + 3}{(s + 1)(s + 3)} = $ **0**. The poles of $sF$ are −1 and −3, so $f(\infty) = \lim_{s\to0}\dfrac{2s + 3}{(s + 1)(s + 3)} = $ **1**.

(b) $sF = 4/(s^2 - s + 2)$ has poles $s = \tfrac12 \pm j\tfrac{\sqrt7}{2}$, in the right half-plane, so $f$ grows in an oscillation and has no final value. The theorem would give the meaningless answer 2.

(c) $H(0) = 10\times2/20 = $ **1**. The poles $-1.5 \pm j4.21$ are stable, so the unit-step response settles to $H(0) = 1$.

### Solution 02-05.12

Directly: $\int_0^te^{-\lambda}e^{-2t + 2\lambda}d\lambda = e^{-2t}\int_0^te^{\lambda}d\lambda = e^{-2t}(e^t - 1) = e^{-t} - e^{-2t}$. By the convolution theorem: $\dfrac{1}{(s + 1)(s + 2)} = \dfrac{1}{s + 1} - \dfrac{1}{s + 2}$, which inverts to the same ✓. At $t = 1$: **0.2325**.

### Solution 02-05.13

(a) In the $s$-domain the series impedance is $R + sL + 1/(sC)$, so the resistor voltage is $V_R = \dfrac{R}{R + sL + 1/(sC)}V_{in}$. Multiplying top and bottom by $s/L$ gives the stated $H(s)$. With $R/L = 10^4$ s⁻¹ and $1/(LC) = 10^8$ s⁻²: poles $-5000 \pm j\sqrt{10^8 - 2.5\times10^7} = -5000 \pm j$ **8660** s⁻¹; a zero at $s = 0$; $\zeta = 5000/10^4 = $ **0.5** and $Q = $ **1**.

(b) $Y = H/s = \dfrac{10^4}{(s + 5000)^2 + 8660^2}$, so $y = \dfrac{10^4}{8660}e^{-5000t}\sin8660t = 1.155\,e^{-5000t}\sin8660t$. The peak is where $\tan(8660t) = 8660/5000 = \sqrt3$, at $t = (\pi/3)/8660 = $ **120.9 µs**, with value **0.5463**.

(c) $\lim_{s\to0}sY = H(0) = 0$: the zero at the origin blocks DC. Physically, once the capacitor has charged to the step voltage no current flows, so the resistor voltage returns to zero.

### Solution 02-05.14

Let $D(s) = LCs^2 + RCs + 1$. Split off the pole at the origin: $\dfrac{R + sL}{s\,D(s)} = \dfrac{K}{s} + \dfrac{Ps + Q'}{D(s)}$. Cover-up at $s = 0$ gives $K = R/D(0) = R$. Recombining, $R\,D(s) + s(Ps + Q') = R + sL$; matching the $s^2$ terms gives $RLC + P = 0$, so $P = -RLC$, and matching the $s$ terms gives $R^2C + Q' = L$, so $Q' = L - R^2C$. Dividing the second fraction's top and bottom by $LC$, with $D/(LC) = (s + \alpha)^2 + \omega_d^2$ and α = $R/(2L)$:

$$
\frac{Ps + Q'}{D(s)} = \frac{-Rs + \frac1C - \frac{R^2}{L}}{(s + \alpha)^2 + \omega_d^2} = \frac{-R(s + \alpha) + \left(\frac1C - R\alpha\right)}{(s + \alpha)^2 + \omega_d^2},
$$

because $R\alpha - R^2/L = -R\alpha$. Inverting with the $s$-shift rule and multiplying by $-\Delta I$:

$$
\Delta V(t) = -\Delta I\,R + e^{-\alpha t}\big(A\cos\omega_dt + B\sin\omega_dt\big), \qquad A = R\Delta I, \quad B = -\frac{\Delta I\left(\frac1C - R\alpha\right)}{\omega_d} .
$$

Numerically $A = $ **10.00 mV** and $B = -10(10^7 - 2\times10^4)/(6.321\times10^8) = $ **−157.9 mV**, exactly the constants of 02-03 Example 5. Minimizing numerically, the worst value of $\Delta V$ is **−160.3 mV** at **2.535 ns** ✓.

### Solution 02-05.15

(a) $Y = \dfrac{s + 1.1}{s(s + 1)(s + 10)}$. Cover-up: at 0, $1.1/10 = 0.11$; at −1, $\dfrac{0.1}{(-1)(9)} = -0.01111$; at −10, $\dfrac{-8.9}{(-10)(-9)} = -0.09889$. So

$$
y(t) = 0.11 - 0.01111\,e^{-t} - 0.09889\,e^{-10t}.
$$

(b) The slow term's amplitude is $0.01111/0.11 = $ **10.10%** of the final value: a 10% tolerance on the zero leaves a 10% tail with the slow pole's time constant of 1 s.

(c) The fast term is gone after about half a second, after which the slow tail sets settling: solving $\lvert y - 0.11\rvert = 0.0011$ numerically gives **2.313 s**. With perfect cancellation, $y = 0.1(1 - e^{-10t})$ settles within 1% in $\ln100/10 = $ **0.4605 s**: the imperfect cancellation makes settling five times slower, through a small, slow "doublet" tail that is easy to miss on a coarse plot.

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 02-05.2a | numerator of L{t³} | 6 | — |
| 02-05.4a | (a) at t = 1 | 1.900 | — |
| 02-05.4b | (b) at t = 1 | −1.839 | — |
| 02-05.4c | (c) at t = 1 | 0.06767 | — |
| 02-05.5a | B | 2 | — |
| 02-05.5b | A | −0.5 | — |
| 02-05.5c | C | 0.5 | — |
| 02-05.5d | y(1) | 1.568 | — |
| 02-05.6a | y(0.5) | 0.2004 | — |
| 02-05.6b | y(0+) | 3 | — |
| 02-05.7a | y(0.25) | 3.104 | — |
| 02-05.8a | y(π/2) | 0.3333 | — |
| 02-05.9a | v(3) | 6.321 | V |
| 02-05.10a | y′(0+) | 3 | — |
| 02-05.10b | time of first peak | 0.5536 | — |
| 02-05.10c | first peak | 0.7713 | — |
| 02-05.11a | f(0+) for (a) | 0 | — |
| 02-05.11b | f(∞) for (a) | 1 | — |
| 02-05.11c | meaningless FVT value for (b) | 2 | — |
| 02-05.11d | DC gain for (c) | 1 | — |
| 02-05.11e | real part of the poles in (c) | −1.5 | 1/s |
| 02-05.11f | imaginary part of the poles in (c) | 4.21 | rad/s |
| 02-05.12a | convolution at t = 1 | 0.2325 | — |
| 02-05.13a | ωd | 8660 | rad/s |
| 02-05.13b | ζ | 0.5 | — |
| 02-05.13c | Q | 1 | — |
| 02-05.13d | step-response amplitude 10⁴/ωd | 1.155 | — |
| 02-05.13e | time of peak | 120.9 | µs |
| 02-05.13f | peak value | 0.5463 | — |
| 02-05.14a | A | 10.00 | mV |
| 02-05.14b | B | −157.9 | mV |
| 02-05.14c | worst droop | 160.3 | mV |
| 02-05.14d | time of worst droop | 2.535 | ns |
| 02-05.15a | final value | 0.11 | — |
| 02-05.15b | slow-term coefficient | −0.01111 | — |
| 02-05.15c | fast-term coefficient | −0.09889 | — |
| 02-05.15d | slow tail as % of final | 10.10 | % |
| 02-05.15e | 1 % settling time | 2.313 | s |
| 02-05.15f | settling time with perfect cancellation | 0.4605 | s |
