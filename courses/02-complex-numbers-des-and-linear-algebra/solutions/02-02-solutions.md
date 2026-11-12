# Solutions 02-02 · First-Order Linear ODEs

Problems: [02-02 problems](../problems/02-02-problems.md) · Chapter: [02-02](../chapters/02-02-first-order-linear-odes.md)

Every numerical answer below is listed in the answer key at the end and is recomputed independently by [verify_02_02.py](../verify/verify_02_02.py).

---

## Solutions

### Solution 02-02.1

(a)

| Equation | Order | Linear? | Homogeneous? | Autonomous? |
|---|---|---|---|---|
| (i) $y' + 4y = 0$ | 1 | yes | yes | yes |
| (ii) $y' = y\sin t$ | 1 | yes ($y' - (\sin t)y = 0$) | yes | no |
| (iii) $L\,di/dt + Ri = V_0\cos\omega t$ | 1 | yes | no | no |
| (iv) $y' = 1 - y^3$ | 1 | no ($y^3$) | — | yes |

(b) $y' = 3e^{-3t}$, and $6 - 3y = 6 - 6 + 3e^{-3t} = 3e^{-3t}$ ✓. Also $y(0) = 2 - 1 = 1$ ✓.

(c) $y' = -1/(1 + t)^2 = -y^2$ ✓, and $y(0) = $ **1**.

### Solution 02-02.2

(a) Separate: $dy/y = -2t\,dt$, so $\ln\lvert y\rvert = -t^2 + C$ and $y = 5e^{-t^2}$. Then $y(1) = 5/e = $ **1.839**. (The equilibrium $y = 0$ is the case $y_0 = 0$.)

(b) Separate: $dy/(1 + y^2) = dt$, so $\arctan y = t + C$, and $y(0) = 0$ gives $C = 0$: $y = \tan t$. It blows up at $t = \pi/2 = $ **1.571**, although $1 + y^2$ is perfectly smooth. The growth rate rises faster than $y$ itself, as in the chapter's $y' = y^2$.

### Solution 02-02.3

(a) $f(y) = y^2 - y - 2 = (y - 2)(y + 1)$, so the equilibria are $-1$ and $2$. With $f'(y) = 2y - 1$: $f'(-1) = -3 < 0$, so $-1$ is **stable**; $f'(2) = 3 > 0$, so $2$ is **unstable**.

(b) The local time constant at $-1$ is $-1/f'(-1) = 1/3 = $ **0.3333** (in the time units of the equation).

(c) $f$ is positive below $-1$, negative between $-1$ and 2, and positive above 2. From $y(0) = 1$, $f(1) = -2 < 0$, so $y$ falls toward $-1$ and settles there. From $y(0) = 3$, $f(3) = 4 > 0$, so $y$ rises away from 2. Because the growth is quadratic, it blows up in finite time.

### Solution 02-02.4

$\mu = e^{3t}$, so $(e^{3t}y)' = 6e^{3t}$ and $e^{3t}y = 2e^{3t} + C$. With $y(0) = 0$, $C = -2$:

$$
y = 2\left(1 - e^{-3t}\right).
$$

The time constant is $1/3$ and the steady state is 2. $y = 1.9$ when $e^{-3t} = 0.05$, so $t = \ln 20/3 = $ **0.9986**.

### Solution 02-02.5

Standard form: $y' - y/t = t^2$, so $p = -1/t$ and $\mu = e^{-\ln t} = 1/t$ (for $t > 0$). Then $(y/t)' = t$, so $y/t = t^2/2 + C$ and $y = t^3/2 + Ct$. From $y(1) = 2$, $C = 3/2$. So $y = t^3/2 + 3t/2$ and $y(2) = 4 + 3 = $ **7**.

**Check:** $y' = 3t^2/2 + 3/2$, so $ty' - y = 3t^3/2 + 3t/2 - t^3/2 - 3t/2 = t^3$ ✓, and $y(1) = 1/2 + 3/2 = 2$ ✓.

### Solution 02-02.6

(a) Separable: $B = B_0e^{\int_0^t r\,ds}$. Here $\int_0^{10}(0.02 + 0.004s)\,ds = 0.2 + 0.2 = 0.4$, so $B(10) = 100\,000\,e^{0.4} = $ **\$149,182**.

(b) $D(t) = e^{-\int_0^t r\,ds} = e^{-(0.02t + 0.002t^2)}$, and $D(10) = e^{-0.4} = $ **0.6703**. It is the present value of \$1 due at year 10 under this rate path. Multiplying the ODE $B' - rB = 0$ by $D$ gives $(DB)' = 0$: the present value of the balance stays constant, which is just another way to say $B(10) = B_0/D(10)$.

(c) $\mu = e^{-0.05t}$, so $(e^{-0.05t}B)' = 10\,000\,e^{-0.05t}$. Integrating from 0 to $t$:

$$
B(t) = B_0e^{0.05t} + \frac{10\,000}{0.05}\left(e^{0.05t} - 1\right).
$$

At $t = 10$: $50\,000\,e^{0.5} = $ **\$82,436** from the initial balance, plus $200\,000(e^{0.5} - 1) = $ **\$129,744** from the deposits, total **\$212,180**. The second term is the continuous-time future value of an annuity.

### Solution 02-02.7

Let the error be $e = T_{oven} - T_p$. Since $T_{oven} = 25 + 2t$ has derivative 2, substituting $T_p = T_{oven} - e$ into $\tau T_p' + T_p = T_{oven}$ gives $\tau(2 - e') + T_{oven} - e = T_{oven}$, that is

$$
\tau e' + e = 2\tau = 8\ ^\circ\text{C}, \qquad e(0) = 0 .
$$

So $e = 8(1 - e^{-t/4})$ °C.

(a) The steady lag is $\tau = $ **4 s** in time, and $S\tau = 2 \times 4 = $ **8 °C** in temperature.

(b) Within 1% of the final error when $e^{-t/4} \le 0.01$: $t = 4\ln100 = $ **18.42 s**.

(c) At $t = 10$ s, $e = 8(1 - e^{-2.5}) = $ **7.343 °C**. The oven is at 45 °C, so the probe reads **37.66 °C**.

### Solution 02-02.8

(a) The equation is $\tau v' + v = 5e^{-\alpha t}$ with $\alpha = 1/\tau_2 = 2000$ s⁻¹, so $\alpha\tau = 2$. By §3.6, $v_p = 5e^{-\alpha t}/(1 - \alpha\tau) = -5e^{-2t/\tau}$. Adding $Ce^{-t/\tau}$ and imposing $v(0) = 0$ gives $C = 5$:

$$
v(t) = 5\left(e^{-t/\tau} - e^{-2t/\tau}\right)\text{ V}.
$$

Setting $v' = 0$: $e^{-t/\tau} = 2e^{-2t/\tau}$, so $e^{-t/\tau} = 1/2$ and $t = \tau\ln2 = $ **0.6931 ms**. The peak is $5(1/2 - 1/4) = $ **1.25 V**.

(b) Now $\alpha\tau = 1$ and the guess must be $ate^{-t/\tau}$, which gives $a = 5/\tau$ (chapter §3.6). The homogeneous part must vanish to keep $v(0) = 0$, so

$$
v(t) = 5\,\frac{t}{\tau}\,e^{-t/\tau}\text{ V}.
$$

$v' = \frac{5}{\tau}e^{-t/\tau}(1 - t/\tau) = 0$ at $t = \tau = $ **1 ms**, where $v = 5/e = $ **1.839 V**.

(c) In (b) the input $e^{-t/\tau}$ already solves the homogeneous equation, so substituting $ae^{-t/\tau}$ gives $0 = 5e^{-t/\tau}$: no constant $a$ works. The formula $1/(1 - \alpha\tau)$ blows up for the same reason. Multiplying the guess by $t$ fixes it. This is the first-order version of resonance.

### Solution 02-02.9

(a) $\tau = L/R = 10^{-3}/10 = $ **0.1 ms**, and $\omega\tau = 2\pi\times5000\times10^{-4} = \pi = $ **3.142**.

(b) In standard form, $\tau i' + i = (V_0/R)\cos\omega t$ with $V_0/R = 1$ A. The phasor answer is $\mathbf{I} = (1\text{ A})/(1 + j\pi)$: amplitude $1/\sqrt{1 + \pi^2} = $ **0.3033 A**, lagging the source by $\arctan\pi = $ **72.34°**.

(c) Undetermined coefficients give $i_p = a\cos\omega t + b\sin\omega t$ with $a = 1/(1 + \pi^2) = 0.09200$ A and $b = \pi/(1 + \pi^2) = 0.2890$ A. The transient must cancel $i_p(0) = a$, so

$$
i(t) = 0.3033\cos(\omega t - 72.34^\circ) - 0.09200\,e^{-t/(0.1\text{ ms})}\text{ A}.
$$

### Solution 02-02.10

Use $N(t) = K\big/\big(1 + \frac{K - N_0}{N_0}e^{-rt}\big)$ with $(K - N_0)/N_0 = 99$.

(a) $N = K/2$ when $99e^{-0.8t} = 1$: $t = \ln99/0.8 = $ **5.744 years**.

(b) $2\ln9/r = 4.394/0.8 = $ **5.493 years**.

(c) $N(3) = 200/(1 + 99e^{-2.4}) = $ **20.04 million**.

(d) Pure exponential growth from 2 million at the same early rate predicts $2e^{0.8\times6} = $ **243.0 million** at year 6, more than the entire capacity of 200 million. The logistic model gives $200/(1 + 99e^{-4.8}) = $ **110.2 million**. In the early phase the two curves are indistinguishable, so early data pin down $r$ but say almost nothing about $K$. Market sizing that extrapolates early growth overstates the market; the capacity must come from independent evidence (addressable users, replacement cycles).

### Solution 02-02.11

(a) $y = 0$: both sides are 0 ✓. $y = t^3$: $y' = 3t^2$ and $3y^{2/3} = 3t^2$ ✓. Both satisfy $y(0) = 0$. The function $f(y) = 3y^{2/3}$ is continuous, but $\partial f/\partial y = 2y^{-1/3}$ is unbounded at $y = 0$, so the uniqueness hypothesis fails exactly there.

(b) $p(t) = \tan t$ is continuous on $(-\pi/2, \pi/2)$, which contains $t_0 = 0$, so a unique solution exists on all of that interval. $\mu = e^{\int\tan t\,dt} = e^{-\ln\cos t} = \sec t$. Then $(y\sec t)' = \cos t\sec t = 1$, so $y\sec t = t + C$, and $y(0) = 1$ gives $C = 1$: $y = (t + 1)\cos t$. **Check:** $y' + y\tan t = \cos t - (t + 1)\sin t + (t + 1)\sin t = \cos t$ ✓.

(c) Separate: $-1/y = t + C$, and $y(0) = 2$ gives $C = -1/2$. So $y = 2/(1 - 2t)$, which blows up at $t = $ **0.5**.

### Solution 02-02.12

(a) Forward Euler multiplies by $1 - h/\tau$ each step, so it is stable for $h < 2\tau = $ **2 µs**.

(b) Four steps of 0.5 µs reach 2 µs:

| Method | Factor per step | $y(2\text{ µs})$ | Error vs exact |
|---|---|---|---|
| Exact | $e^{-0.5}$ | **0.1353** | — |
| Forward Euler | $1 - 0.5 = 0.5$ | **0.0625** | **−53.8%** |
| Backward Euler | $1/1.5$ | **0.1975** | **+46.0%** |
| Trapezoidal | $0.75/1.25 = 0.6$ | **0.1296** | **−4.24%** |

(c) For a stiff circuit, an implicit method: backward Euler and the trapezoidal rule both stay stable for any step (their factors are below 1 in magnitude for every $h > 0$), so the step can be chosen for accuracy on the slow parts of the circuit instead of being forced tiny by the fastest time constant. The trapezoidal rule is also far more accurate here, which is why SPICE uses it by default. Its factor tends to −1 for very large steps, however, which can cause a slowly decaying numerical ringing; that is why simulators fall back to backward Euler or Gear's method in some situations.

### Solution 02-02.13

With $v = 1/y$, $v' = -y'/y^2$. From $y' = y^2 - y$:

$$
v' = -\frac{y^2 - y}{y^2} = -1 + \frac{1}{y} = v - 1 .
$$

This is linear: $v' - v = -1$, with $v = 1 + Ce^t$. From $v(0) = 1/0.5 = 2$, $C = 1$, so

$$
y(t) = \frac{1}{1 + e^t}, \qquad y(1) = \frac{1}{1 + e} = 0.2689 .
$$

The equation is $y' = -y(1 - y)$: a logistic equation running backward in time. Its equilibria are $y = 0$ (stable, $f'(0) = -1$) and $y = 1$ (unstable, $f'(1) = +1$). Starting at 0.5, the solution slides down an S-curve toward 0. Run backward in time, it rises toward 1.

### Solution 02-02.14

The model is $C_{th}T' = P - (T - 25)/R_{th}$, with $\tau = R_{th}C_{th} = 300$ s.

(a) The steady temperature is $25 + 10P$. Setting it to 43 °C gives $P = $ **1.8 W**.

(b) $25 + 10\times1.0 = $ **35 °C**.

(c) At 5 W the target is $25 + 50 = 75$ °C, so $T(t) = 75 - 40e^{-t/300}$. $T = 43$ when $e^{-t/300} = 32/40$: $t = 300\ln1.25 = $ **66.94 s**. At 3 W the target is 55 °C, $T = 55 - 20e^{-t/300}$, and $t = 300\ln(20/12) = $ **153.2 s**.

(d) At 1.8 W the equilibrium is exactly 43 °C. The temperature is already there, so it stays at 43 °C: the governor has found the sustainable operating point.

(e) The 5 W burst lasts $66.94/300 = $ **0.2231** of a time constant. A benchmark that runs for a minute measures the phone before its thermal capacitance has charged, so it reports burst performance (5 W). After a few minutes the phone can deliver only 1.8 W, about a third of that. Looping stress tests, or measurements after 20 minutes, reveal the sustained figure.

### Solution 02-02.15

(a) KCL at the capacitor: $Cv' = -v/R(t)$, so

$$
v' = -\frac{e^{-t/T}}{R_0C}\,v .
$$

Separate: $\ln(v/v_0) = -\frac{1}{R_0C}\int_0^te^{-s/T}ds = -\frac{T}{R_0C}\left(1 - e^{-t/T}\right)$. With $R_0C = 100\times10^{-11} = 1$ ns and $T/(R_0C) = 2$:

$$
v(t) = v_0\exp\!\left[-2\left(1 - e^{-t/T}\right)\right].
$$

(b) At $t = 2$ ns: $\exp[-2(1 - e^{-1})] = $ **0.2825**. As $t \to \infty$: $e^{-2} = $ **0.1353**. The capacitor *never* discharges below 13.5%.

(c) With a constant $R_0$, $v = v_0e^{-t/(1\text{ ns})}$: 0.1353 at 2 ns and zero eventually. The slowly opening switch delivers a total "discharge budget" of only $T/(R_0C) = 2$ time constants, however long you wait. So a reset or sampling switch must stay fully on for many $R_0C$ before it starts to turn off; how long it takes to turn off sets what fraction of the old charge is left behind. (Course 20 treats the related charge-injection and signal-dependent turn-off errors.)

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 02-02.1a | initial condition for 1/(1 + t) | 1 | — |
| 02-02.2a | y(1) for y' = −2ty | 1.839 | — |
| 02-02.2b | blow-up time of tan t | 1.571 | — |
| 02-02.3a | stable equilibrium | −1 | — |
| 02-02.3b | unstable equilibrium | 2 | — |
| 02-02.3c | local time constant at −1 | 0.3333 | — |
| 02-02.4a | time constant | 0.3333 | — |
| 02-02.4b | steady state | 2 | — |
| 02-02.4c | time to reach 1.9 | 0.9986 | — |
| 02-02.5a | y(2) | 7 | — |
| 02-02.6a | balance at year 10, varying rate | 149182 | US$ |
| 02-02.6b | discount factor D(10) | 0.6703 | — |
| 02-02.6c | grown initial balance | 82436 | US$ |
| 02-02.6d | future value of deposits | 129744 | US$ |
| 02-02.6e | balance at year 10, 5% with deposits | 212180 | US$ |
| 02-02.7a | lag in time | 4 | s |
| 02-02.7b | lag in temperature | 8 | °C |
| 02-02.7c | time to within 1 % | 18.42 | s |
| 02-02.7d | error at 10 s | 7.343 | °C |
| 02-02.7e | reading at 10 s | 37.66 | °C |
| 02-02.8a | peak time, τ2 = 0.5 ms | 0.6931 | ms |
| 02-02.8b | peak value, τ2 = 0.5 ms | 1.25 | V |
| 02-02.8c | peak time, matched case | 1 | ms |
| 02-02.8d | peak value, matched case | 1.839 | V |
| 02-02.9a | time constant | 0.1 | ms |
| 02-02.9b | ωτ | 3.142 | — |
| 02-02.9c | steady-state amplitude | 0.3033 | A |
| 02-02.9d | phase lag | 72.34 | ° |
| 02-02.9e | cosine coefficient a | 0.09200 | A |
| 02-02.9f | sine coefficient b | 0.2890 | A |
| 02-02.10a | time to half capacity | 5.744 | yr |
| 02-02.10b | 10 % to 90 % time | 5.493 | yr |
| 02-02.10c | installed base at 3 years | 20.04 | million |
| 02-02.10d | exponential extrapolation to year 6 | 243.0 | million |
| 02-02.10e | logistic value at year 6 | 110.2 | million |
| 02-02.11a | blow-up time of y' = y², y(0) = 2 | 0.5 | — |
| 02-02.12a | largest stable forward-Euler step | 2 | µs |
| 02-02.12b | exact y(2 µs) | 0.1353 | — |
| 02-02.12c | forward Euler | 0.0625 | — |
| 02-02.12d | backward Euler | 0.1975 | — |
| 02-02.12e | trapezoidal | 0.1296 | — |
| 02-02.12f | forward-Euler error | −53.8 | % |
| 02-02.12g | backward-Euler error | 46.0 | % |
| 02-02.12h | trapezoidal error | −4.24 | % |
| 02-02.13a | y(1) | 0.2689 | — |
| 02-02.14a | sustainable power | 1.8 | W |
| 02-02.14b | idle temperature | 35 | °C |
| 02-02.14c | time to limit at 5 W | 66.94 | s |
| 02-02.14d | time to limit at 3 W | 153.2 | s |
| 02-02.14e | burst as a fraction of τ | 0.2231 | — |
| 02-02.14f | thermal time constant | 300 | s |
| 02-02.15a | R0C | 1 | ns |
| 02-02.15b | fraction left at 2 ns | 0.2825 | — |
| 02-02.15c | final fraction left | 0.1353 | — |
