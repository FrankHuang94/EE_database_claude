# Problems 01-04 · Applications of Derivatives

Chapter: [01-04](../chapters/01-04-applications-of-derivatives.md) · Worked solutions: [01-04 solutions](../solutions/01-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** angles in radians; $\ln$ is the natural log; answers to 4 significant figures unless stated. Use a calculator or Python freely, but show the method. In optimization problems, always classify the critical point and check the endpoints.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 01-04.1 [A]

Let $f(x) = x^3 - 3x$ on $[-2, 3]$.

(a) Find the critical points and classify them with the second derivative test.
(b) Find the global maximum and minimum on the interval, and where they occur.

### Problem 01-04.2 [A]

Let $f(x) = xe^{-x}$ for $x \ge 0$. (Its shape, a rise then a slow decay, is the response of the two equal RC stages in chapter Example 01-04.5.)

(a) Find the maximum and its value.
(b) Find the inflection point and the value of $f$ there.
(c) Find $\lim_{x\to\infty}f(x)$.

### Problem 01-04.3 [A]

Evaluate with L'Hôpital's rule, checking the indeterminate form at each step.

(a) $\lim_{x\to0}\dfrac{e^x - 1 - x}{x^2}$  (b) $\lim_{x\to0^+}x\ln x$  (c) $\lim_{x\to1}\dfrac{\ln x}{x - 1}$  (d) $\lim_{x\to0}\dfrac{1 - \cos 3x}{x^2}$  (e) $\lim_{x\to\infty}x^{1/x}$ (hint: take the logarithm)

### Problem 01-04.4 [A]

Use linearization at a convenient point to estimate each value. Compare with the exact value, and with the error estimate $\tfrac{1}{2}f''(a)(x - a)^2$ for part (a).

(a) $\sqrt{4.1}$  (b) $e^{0.05}$  (c) $\sin 0.2$  (d) $1.02^{10}$

### Problem 01-04.5 [B]

A piezoelectric sensor behaves as a 1 V source (open circuit) with 2 kΩ internal resistance.

(a) What load resistance extracts the most power, and how much is it?
(b) How much power does a 1 kΩ load receive, as a fraction of the maximum?
(c) If instead the load is fixed at 2 kΩ and you could redesign the sensor's internal resistance, what value of $R_s$ would maximize the load power? Explain why this does not contradict (a).

### Problem 01-04.6 [B]

**Repeater insertion.** A long on-chip wire has an intrinsic RC delay of 800 ps, which grows as the square of its length. Splitting it into $n$ equal segments, each driven by its own buffer (the source driver counts as the first), gives total delay

$$
T(n) = 20n + \frac{800}{n}\ \text{ps},
$$

where 20 ps is the delay each buffer adds.

(a) Treating $n$ as continuous, find the optimal $n$ and the minimum delay.
(b) $n$ must be an integer. Which integer is best, and what is its delay?
(c) Compare with a single segment driven only by the source driver ($n = 1$).
(d) Explain why the delay of each segment falls as $1/n^2$ while the total wire delay falls as $1/n$.

### Problem 01-04.7 [B]

**Division by multiplication.** Newton's method on $f(x) = 1/x - a$ computes $1/a$.

(a) Show that the Newton update is $x_{k+1} = x_k(2 - ax_k)$, which needs no division.
(b) For $a = 3$ and $x_0 = 0.3$, compute three iterations.
(c) Define the relative error $\varepsilon_k = 1 - ax_k$. Show that $\varepsilon_{k+1} = \varepsilon_k^2$, and list $\varepsilon_1$, $\varepsilon_2$, $\varepsilon_3$.
(d) A lookup table gives a seed with $\lvert\varepsilon_0\rvert \le 2^{-8}$. How many iterations reach double precision ($2^{-53}$)?

### Problem 01-04.8 [B]

**When Newton fails.** Solve $\arctan x = 0$ (root $x = 0$) by Newton's method.

(a) Show that the update is $x_{k+1} = x_k - (1 + x_k^2)\arctan x_k$.
(b) Iterate four times from $x_0 = 1.0$ and from $x_0 = 1.5$. Describe what happens.
(c) There is a critical starting value $x_c$ for which the iterates bounce between $x_c$ and $-x_c$ forever. It satisfies $x_{k+1} = -x_k$. Find $x_c$ numerically.
(d) What safeguard would you add to a production solver?

### Problem 01-04.9 [B]

**A MEMS microphone (constant-voltage teaching model, chapter §3.7).** A condenser microphone is a parallel-plate capacitor with $C = \varepsilon_0A/d$, plate area $A = 1$ mm² and rest gap $d = 2$ µm, biased at a constant 5 V ($\varepsilon_0 = 8.854\times10^{-12}$ F/m).

(a) Find the rest capacitance.
(b) Sound moves the diaphragm away from the backplate at 1 mm/s (the gap is increasing). Find $dC/dt$ and the current $i = V\,dC/dt$ at the rest gap.
(c) By what factor would the current grow if the gap were halved, at the same diaphragm velocity?

### Problem 01-04.10 [B]

Power is computed as $P = V^2/R$ from $V = 5.00$ V ± 1% and $R = 100\ \Omega$ ± 2%.

(a) Find the nominal power.
(b) Find the relative and absolute uncertainty of $P$ by the worst-case linear method.
(c) Repeat with RSS, assuming the errors are independent.
(d) Why does the voltage's 1% contribute twice as much as one might expect?

### Problem 01-04.11 [B]

The mean value theorem in practice.

(a) An op-amp slews at most 1 V/µs. What is the largest possible output change in 2 µs?
(b) A temperature sensor reports that a battery's temperature never changes faster than 0.5 K/s. Bound the change over 10 s.
(c) Prove that $\lvert\sin a - \sin b\rvert \le \lvert a - b\rvert$ for all $a, b$.
(d) A 1 µF capacitor is driven by a current that never exceeds 10 mA in magnitude. Bound the change of its voltage over 50 µs.

### Problem 01-04.12 [B]

Repeat chapter Example 01-04.2 for $E(V) = AV^2 + B/V$ with $A = 0.8$ pJ/V² and $B = 0.1$ pJ·V.

(a) Find $V^\ast$ and $E(V^\ast)$.
(b) Compare with operating at 0.9 V.
(c) Show that, for any $A$ and $B$, leakage energy is twice switching energy at the optimum.
(d) The stylized model ignores that real circuits slow down exponentially below threshold. Would including that effect move $V^\ast$ up or down? Explain.

### Problem 01-04.13 [C]

**Optimal pipeline depth (a stylized model).** A processor's logic takes 600 ps in total. Splitting it into $n$ pipeline stages gives a clock period of $600/n + 40$ ps, where 40 ps is the latch and skew overhead per stage. Deeper pipelines lose more cycles to hazards: the cycles per instruction are $1 + 0.04n$. The time per instruction is

$$
T(n) = \left(\frac{600}{n} + 40\right)(1 + 0.04n)\ \text{ps}.
$$

(a) Show that $T(n) = 600\cdot0.04 + 40 + \dfrac{600}{n} + 1.6n$, and find the optimal $n$ and the minimum $T$.
(b) Evaluate $T$ at $n = 1$, $n = 5$, and at the best integer depth. What speedup does pipelining give over $n = 1$?
(c) How flat is the optimum? Evaluate $T$ at half and at double the optimal depth.
(d) If a better branch predictor halved the hazard coefficient to 0.02, how would the optimal depth change?

### Problem 01-04.14 [C]

**Measuring quadratic convergence.** For Newton's method on $f(x) = x^2 - 2$ from $x_0 = 1$ (chapter Example 01-04.4):

(a) Compute $e_k = x_k - \sqrt{2}$ for $k = 1$ to 4, and the ratios $e_{k+1}/e_k^2$.
(b) Show that the ratios approach $f''(r)/\big(2f'(r)\big) = 1/(2\sqrt{2})$, and evaluate it.
(c) Explain why the first ratio differs from the limit.

### Problem 01-04.15 [C]

**How long can turbo last?** A processor's die temperature follows $T(t) = T_a + PR_{th}\left(1 - e^{-t/\tau}\right)$ after its power steps to $P$ at $t = 0$, with ambient $T_a = 40$ °C, thermal resistance $R_{th} = 0.5$ K/W and thermal time constant $\tau = 2$ s. The limit is 85 °C.

(a) At $P = 100$ W, find the initial heating rate $dT/dt$ at $t = 0$, the steady-state temperature, and the time to reach 85 °C.
(b) At a "turbo" level of 150 W, find the time to reach 85 °C exactly, and estimate it from the initial rate alone (linearization). Which estimate is safer for a control algorithm, and why?
(c) What is the highest power that can be sustained forever?

---

## Objective coverage

| Learning objective (chapter 01-04) | Problems |
|---|---|
| 1. Critical points and classification; engineering optimization | 1, 2, 5, 6, 12, 13 |
| 2. Linearization, differentials, tolerances, small-signal idea | 4, 10, 15(b) |
| 3. Newton's method: derivation, convergence, failure | 7, 8, 14 |
| 4. Related rates | 9, 15 |
| 5. L'Hôpital's rule; the mean value theorem | 2(c), 3, 11 |
