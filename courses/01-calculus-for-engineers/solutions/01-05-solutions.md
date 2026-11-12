# Solutions 01-05 · Integrals: Accumulating Charge and Energy

Problems: [01-05 problems](../problems/01-05-problems.md) · Chapter: [01-05](../chapters/01-05-integrals.md)

Every numerical answer below is listed in the answer key at the end and is recomputed independently by [verify_01_05.py](../verify/verify_01_05.py).

---

## Solutions

### Solution 01-05.1

$\Delta x = 0.25$; the grid is 0, 0.25, 0.5, 0.75, 1.

| Rule | Value | Error (value − exact) |
|---|---|---|
| Left | **1.5124** | −0.2059 |
| Right | **1.9420** | +0.2237 |
| Midpoint (at 0.125, 0.375, 0.625, 0.875) | **1.7138** | −0.0045 |
| Trapezoid | **1.7272** | +0.0089 |
| Exact, $e - 1$ | **1.7183** | — |

The signs follow from the shape of $e^x$:

- it is increasing, so left sums underestimate and right sums overestimate;
- it is concave up (curving like ∪), so chords lie above the curve and the trapezoid overestimates, while the midpoint's tangent-like flat tops underestimate.

The midpoint error is about half the trapezoid error, with the opposite sign, as §3.1 predicts.

### Solution 01-05.2

(a) $\big[\tfrac{2}{3}x^{3/2}\big]_1^4 = \tfrac{2}{3}(8 - 1) = $ **4.667**.
(b) $\big[-\cos x\big]_0^\pi = 1 + 1 = $ **2**.
(c) $\big[\ln x\big]_1^e = 1 - 0 = $ **1**.
(d) $\big[x^3 - x^2 + x\big]_0^2 = 8 - 4 + 2 = $ **6**.
(e) $\big[\tfrac{1}{2}e^{2x}\big]_0^{\ln 2} = \tfrac{1}{2}(4 - 1) = $ **1.5**, using $e^{2\ln 2} = 4$.
(f) $\big[\tan x\big]_0^{\pi/4} = $ **1**.

### Solution 01-05.3

(a) By FTC part 1 directly: $\cos(x^2)$. (Its antiderivative has no elementary formula, but the derivative is immediate.)

(b) Let $G(u) = \int_1^u\ln t\,dt$, so $G'(u) = \ln u$. The integral is $G(x^2)$, and by the chain rule its derivative is $\ln(x^2)\cdot2x = 4x\ln x$. At $x = 2$: $8\ln 2 = $ **5.545**.

(c) Reverse the limits: $\int_x^5 = -\int_5^x$, so the derivative is $-e^{-x}$.

### Solution 01-05.4

(a) $x^3$ is odd and $\cos x$ is even, so the product is odd. Over a symmetric interval the negative half cancels the positive half exactly.

(b) $x^2$ is even, so the integral is $2\int_0^2x^2\,dx = 2\times8/3 = $ **5.333**.

(c) On $[0, 1]$, $e^{-x^2}$ decreases from 1 to $e^{-1}$. So $e^{-1}\times1 \le I \le 1\times1$, i.e. **0.3679** ≤ I ≤ **1**. The true 0.7468 lies inside. These bounds take no calculus beyond the comparison property, and they are often enough for a sanity check.

### Solution 01-05.5

(a) $v(t) = v(0) + \dfrac{1}{C}\displaystyle\int_0^t i\,d\lambda$.

- At 1 ms: $1 + (10\times10^{-3})(10^{-3})/(2\times10^{-6}) = 1 + 5 = $ **6 V**.
- At 3 ms: $6 + (-5\times10^{-3})(2\times10^{-3})/(2\times10^{-6}) = 6 - 5 = $ **1 V**.

(b) Net charge $= 10\text{ mA}\times1\text{ ms} - 5\text{ mA}\times2\text{ ms} = 10 - 10 = $ **0 µC**. The voltage change is net charge over $C$, so with zero net charge the capacitor returns to 1 V. The *path* went up to 6 V and back, but only the net integral matters for the end point.

(c) A linear rise from 1 V to 6 V over the first millisecond, a linear fall back to 1 V by 3 ms, then flat (chapter Figure 3).

### Solution 01-05.6

(a) $i(t) = i(0) + \dfrac{1}{L}\displaystyle\int v\,dt$.

- At 2 µs: $0.5 + 5\times2\times10^{-6}/10^{-5} = 0.5 + 1.0 = $ **1.5 A**.
- At 4 µs: $1.5 - 1.0 = $ **0.5 A**, back to the start: periodic steady state.

(b) The current is a symmetric triangle between 0.5 and 1.5 A, so the average is **1.0 A**.

(c) $\tfrac{1}{2}Li_{peak}^2 = \tfrac{1}{2}\times10^{-5}\times1.5^2 = $ **11.25 µJ**.

### Solution 01-05.7

(a) Stored: $\tfrac{1}{2}CV^2 = \tfrac{1}{2}\times10^{-5}\times144 = $ **0.72 mJ**. Supplied: the source pushes charge $CV$ at constant voltage $V$, so $CV^2 = $ **1.44 mJ**.

(b) With $i = (V/R)e^{-t/\tau}$ and $\tau = RC$:

$$
\int_0^\infty i^2R\,dt = \frac{V^2}{R}\int_0^\infty e^{-2t/\tau}\,dt = \frac{V^2}{R}\cdot\frac{\tau}{2} = \frac{V^2}{R}\cdot\frac{RC}{2} = \frac{1}{2}CV^2 .
$$

$R$ cancels.

(c) Charge in steps: raise the source voltage in $N$ equal steps, letting the capacitor settle after each. Each step loses $\tfrac{1}{2}C(V/N)^2$, so the total loss is $\tfrac{1}{2}CV^2/N$. A slow ramp (adiabatic charging) or an inductor-based converter does better still. This is the principle of adiabatic logic and of resonant and soft-charging converters.

### Solution 01-05.8

(a) $\sin^2 = \tfrac{1}{2}(1 - \cos2\omega t)$; the cosine averages to zero over a period, leaving **0.5**.

(b) The average of a linear ramp from 0 to 3 V is the midpoint, **1.5 V**: area $\tfrac{1}{2}\times3\times T$ divided by $T$.

(c) $3.3\times0.30 = $ **0.99 V**. This is why filtered PWM works as a cheap digital-to-analog converter.

(d) $V_m/\pi = 10/\pi = $ **3.183 V**.

### Solution 01-05.9

(a) Charge per hour: $15\times3 + 1.2\times57 = 45 + 68.4 = 113.4$ mA·min. The average is $113.4/60 = $ **1.890 mA**. Life $= 300/1.89 = $ **158.7 h** $= $ **6.61 days**.

(b) $50\text{ µA}\times24\text{ h} = $ **1.2 mAh** per day, or **0.4%** of capacity per day. Without recalibration, the error accumulates linearly, by 8.4 mAh over a week.

(c) Halving the GPS current gives an average of $(22.5 + 68.4)/60 = 1.515$ mA, a life of **198.0 h**. Cutting the idle current by 20% gives $(45 + 54.72)/60 = 1.662$ mA, a life of **180.5 h**. **Halving the GPS current wins**: the bursts are 40% of the charge budget ($45/113.4$) although they run only 5% of the time.

### Solution 01-05.10

(a) Trapezoid with $n = 4$ ($h = \pi/4$): $\dfrac{h}{2}\big[0 + 2(0.7071 + 1 + 0.7071) + 0\big] = $ **1.8961**, an error of **0.1039**. With $n = 8$: **1.9742**, an error of **0.02577**. The ratio of errors is **4.03**: halving $h$ quarters the error, so the rule is second order.

(b) Midpoint with $n = 4$, at $\pi/8$, $3\pi/8$, $5\pi/8$, $7\pi/8$: **2.0523**, an error of **−0.0523**. That is about half the trapezoid error in magnitude, with the opposite sign.

(c) $(2M + T)/3 = (4.1047 + 1.8961)/3 = $ **2.00027**, an error of only $2.7\times10^{-4}$, nearly 400 times smaller than the trapezoid's at the same $n$. The leading errors of the two rules cancel.

### Solution 01-05.11

(a) $RC = 10^4\times10^{-7} = 1$ ms. For a constant input the integral is $0.5t$, so $v_{out} = -0.5t/RC$. At 2 ms: **−1.0 V**. The slope is $-0.5/10^{-3} = $ **−500 V/s**.

(b) $-500t = -12$ gives $t = $ **24 ms**.

(c) Each half period (0.5 ms) at ±1 V changes the output by $1\times0.5\times10^{-3}/10^{-3} = 0.5$ V, alternately down and up. The output is a triangle of **0.5 V** peak-to-peak. (It starts at 0 and swings between 0 and −0.5 V, since the first half-cycle is positive. Any input offset would make it drift, hence the parallel resistor in practice.)

### Solution 01-05.12

(a) During $T_1$ the integrator output reaches $-V_xT_1/(RC)$. During $T_2$ the reference ramps it back: $V_{ref}T_2/(RC)$. Returning to zero requires $V_xT_1 = V_{ref}T_2$, so $V_x = V_{ref}T_2/T_1$. $RC$ cancels, so its tolerance and drift do not matter. Only the clock (which times both intervals) and $V_{ref}$ do.

(b) $T_2 = 0.35\times20 = $ **7 ms**, and the count is $7\times10^{-3}\times10^6 = $ **7000**.

(c) $\int_0^{T_1}A\sin(2\pi\cdot50t + \phi)\,dt = -\dfrac{A}{2\pi\cdot50}\big[\cos(2\pi\cdot50t + \phi)\big]_0^{0.02} = 0$, because $2\pi\cdot50\times0.02 = 2\pi$, one full cycle, so the cosine returns to its starting value. In a 60 Hz country, 20 ms is 1.2 cycles and the hum would *not* cancel. Use $T_1 = 16.67$ ms there, or 100 ms, which is a whole number of cycles at both frequencies.

### Solution 01-05.13

(a) By FTC part 1, $A'(x) = x^2 - 4$. It is negative on $[0, 2)$ (decreasing) and positive for $x > 2$ (increasing). So the minimum is at **x = 2**.

(b) $A(x) = x^3/3 - 4x$. The minimum value is $A(2) = 8/3 - 8 = $ **−5.333**. $A(x) = 0$ with $x > 0$ gives $x^2 = 12$, so $x = \sqrt{12} = $ **3.464**.

(c) At $x = 3.464$, the positive area accumulated beyond $x = 2$ exactly cancels the negative area from 0 to 2: net signed area zero.

### Solution 01-05.14

(a) $q = \displaystyle\int_0^5C_0(1 + av)\,dv = C_0\big[v + \tfrac{a}{2}v^2\big]_0^5 = C_0(5 - 1.25) = $ **3.75 µC**, against the nominal $C_0V = 5$ µC: 25% less charge.

(b) $w = \displaystyle\int_0^5vC_0(1 + av)\,dv = C_0\big[\tfrac{v^2}{2} + \tfrac{a}{3}v^3\big]_0^5 = C_0(12.5 - 4.167) = $ **8.333 µJ**, against $\tfrac{1}{2}C_0V^2 = 12.5$ µJ: 33% less energy.

(c) $q/V = 3.75/5 = $ **0.75 µF**. A part sold as "1 µF" behaves like 0.75 µF (or less, for real X5R parts at high bias) in this circuit. Decoupling networks, hold-up capacitors and filters designed with the nominal value can then fail their specifications. Engineers read the manufacturer's DC-bias derating curves, not just the nominal capacitance.

### Solution 01-05.15

(a) $v\cdot i = 3250\sin(\omega t)\sin(\omega t - 30^\circ)$. Using $\sin A\sin B = \tfrac{1}{2}\big[\cos(A - B) - \cos(A + B)\big]$, the product is $1625\big[\cos30^\circ - \cos(2\omega t - 30^\circ)\big]$. The second term averages to zero over a cycle, so $P = 1625\cos30^\circ = $ **1407 W**.

(b) $N = 80$: $P_{80} = $ **1407 W**. $N = 3$: $P_3 = $ **1407 W**, exact as well.

(c) $N = 2$, starting at 1 ms: $P_2 = $ **−208.8 W**, completely wrong (even negative). The product contains DC and a component at twice the line frequency. Averaging $N$ equally spaced samples cancels a sinusoid of $m$ cycles per period unless $m$ is a multiple of $N$. With $N = 2$, the $2\times$ component ($m = 2$) is sampled at the same phase every time, so it does not cancel. It *aliases* to DC ([11-10](../../11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md)). Any $N \ge 3$ cancels it exactly. Real meters sample much faster than this minimum to handle harmonics.

(d) $1.407\text{ kW}\times1\text{ h} = $ **1.407 kWh**.

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 01-05.1a | left sum | 1.5124 | — |
| 01-05.1b | right sum | 1.9420 | — |
| 01-05.1c | midpoint sum | 1.7138 | — |
| 01-05.1d | trapezoid sum | 1.7272 | — |
| 01-05.1e | exact | 1.7183 | — |
| 01-05.2a | (a) | 4.667 | — |
| 01-05.2b | (b) | 2 | — |
| 01-05.2c | (c) | 1 | — |
| 01-05.2d | (d) | 6 | — |
| 01-05.2e | (e) | 1.5 | — |
| 01-05.2f | (f) | 1 | — |
| 01-05.3a | (b) at x = 2 | 5.545 | — |
| 01-05.4a | ∫ x² over [−2, 2] | 5.333 | — |
| 01-05.4b | lower bound | 0.3679 | — |
| 01-05.4c | upper bound | 1 | — |
| 01-05.5a | v(1 ms) | 6 | V |
| 01-05.5b | v(3 ms) | 1 | V |
| 01-05.5c | net charge | 0 | µC |
| 01-05.6a | i(2 µs) | 1.5 | A |
| 01-05.6b | i(4 µs) | 0.5 | A |
| 01-05.6c | average current | 1.0 | A |
| 01-05.6d | peak energy | 11.25 | µJ |
| 01-05.7a | stored energy | 0.72 | mJ |
| 01-05.7b | energy supplied | 1.44 | mJ |
| 01-05.8a | (a) | 0.5 | — |
| 01-05.8b | (b) | 1.5 | V |
| 01-05.8c | (c) | 0.99 | V |
| 01-05.8d | (d) | 3.183 | V |
| 01-05.9a | average current | 1.890 | mA |
| 01-05.9b | life | 158.7 | h |
| 01-05.9c | life | 6.61 | days |
| 01-05.9d | offset charge per day | 1.2 | mAh |
| 01-05.9e | offset per day as % of capacity | 0.4 | % |
| 01-05.9h | offset charge per week | 8.4 | mAh |
| 01-05.9f | life with GPS halved | 198.0 | h |
| 01-05.9g | life with idle cut 20 % | 180.5 | h |
| 01-05.10a | trapezoid n = 4 | 1.8961 | — |
| 01-05.10b | error n = 4 | 0.1039 | — |
| 01-05.10c | trapezoid n = 8 | 1.9742 | — |
| 01-05.10d | error n = 8 | 0.02577 | — |
| 01-05.10e | error ratio | 4.03 | — |
| 01-05.10f | midpoint n = 4 | 2.0523 | — |
| 01-05.10g | Simpson combination | 2.00027 | — |
| 01-05.11a | v_out at 2 ms | −1.0 | V |
| 01-05.11b | output slope | −500 | V/s |
| 01-05.11c | time to saturate | 24 | ms |
| 01-05.11d | triangle peak-to-peak | 0.5 | V |
| 01-05.12a | T2 | 7 | ms |
| 01-05.12b | clock count | 7000 | — |
| 01-05.13a | minimum location | 2 | — |
| 01-05.13b | minimum value | −5.333 | — |
| 01-05.13c | zero crossing | 3.464 | — |
| 01-05.14a | stored charge | 3.75 | µC |
| 01-05.14b | stored energy | 8.333 | µJ |
| 01-05.14c | effective capacitance | 0.75 | µF |
| 01-05.15a | exact average power | 1407 | W |
| 01-05.15b | P with N = 80 | 1407 | W |
| 01-05.15c | P with N = 3 | 1407 | W |
| 01-05.15d | P with N = 2 from 1 ms | −208.8 | W |
| 01-05.15e | energy in one hour | 1.407 | kWh |
