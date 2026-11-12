# Solutions 00-04 · Toolchain Setup Walkthrough

Problems: [00-04 problems](../problems/00-04-problems.md) · Chapter: [00-04](../chapters/00-04-toolchain-walkthrough.md)

All numbers are in the answer key and recomputed by [verify_00_04.py](../verify/verify_00_04.py).

---

## Solutions

### Solution 00-04.1

(a) 4700 Ω. (b) $1.0\times10^{-5}$ F (10 µF). (c) $2.2\times10^{-9}$ F (2.2 nF). (d) $1.0\times10^{6}$ Ω. (e) $3.0\times10^{-3}$ A. (f) **$1.0\times10^{-3}$ Ω**. `M` is milli, not mega.

### Solution 00-04.2

$I = 12/(10 + 5)\text{ kΩ} = 0.800$ mA, so $V_{out} = IR_2 = 0.8\text{ mA} \times 5\text{ kΩ} = 4.000$ V and $P = 12 \times 0.8\times10^{-3} = 9.600$ mW. SPICE reports the source current as **−0.8 mA**, because it measures current flowing into the + terminal and a delivering source has current flowing out of it.

### Solution 00-04.3

(a) **False**: `0.1 + 0.2` is 0.30000000000000004.
(b) $5.55\times10^{-17}/0.3 = 1.85\times10^{-16}$, about one machine epsilon. A relative tolerance of $10^{-9}$ treats the two as equal.
(c) **True.** The next representable number above 1.0 is $1 + \varepsilon$. Adding $\varepsilon/4$ falls below half that gap, so the result rounds back to exactly 1.0.

### Solution 00-04.4

The netlist:

```text
* Problem 00-04.4
V1 n1 0 DC 10
R1 n1 a 1k
R2 a  0 2k
R3 a  b 1k
R4 b  0 1k
.op
.end
```

$R_3 + R_4 = 2$ kΩ in parallel with $R_2 = 2$ kΩ gives 1 kΩ from `a` to ground. That forms a 1 kΩ : 1 kΩ divider from 10 V, so $V_a = 5.000$ V and $I = 10/(1 + 1)\text{ kΩ} = 5.000$ mA. $R_3$ and $R_4$ divide $V_a$ equally: $V_b = 2.500$ V.

### Solution 00-04.5

(a) $f_c = 1/(2\pi \cdot 10^4 \cdot 10^{-8}) = 1/(6.283\times10^{-4}) = 1.592$ kHz.
(b) At 10 kHz: $\lvert H\rvert = 1/\sqrt{1 + (10/1.592)^2} = 1/\sqrt{1 + 39.48} = 0.1572$, which is $20\log_{10}0.1572 = -16.07$ dB.

### Solution 00-04.6

(a) $x^2 + 1 = 10^{16} + 1$. The spacing between doubles near $10^{16}$ is 2, so adding 1 rounds back to $10^{16}$. The square root gives exactly $10^8$, and the subtraction gives 0. This is catastrophic cancellation.

(b) Multiply and divide by the conjugate:

$$
\sqrt{x^2 + 1} - x = \frac{(\sqrt{x^2 + 1} - x)(\sqrt{x^2 + 1} + x)}{\sqrt{x^2 + 1} + x} = \frac{1}{\sqrt{x^2 + 1} + x} \approx \frac{1}{2x} = 5.00\times10^{-9}.
$$

The rewritten form has no subtraction of near-equal numbers.

### Solution 00-04.7

(a) Two 8-bit inputs give 16 input bits: $2^{16} = 65\,536$ vectors, taking 65.5 µs.
(b) 32 input bits: $2^{32} = 4.29\times10^9$ vectors, taking 4.29 s.
(c) 64 input bits: $2^{64}/10^9 = 1.84\times10^{10}$ s, about **585 years**.

Exhaustive simulation is impossible for datapaths of realistic width. Processors are verified with structured directed tests, constrained-random stimulus measured by coverage, and formal methods. Arithmetic units in particular are often proven correct formally.

### Solution 00-04.8

(a) $10^{-3}/10^{-9} = 10^6$ steps.
(b) $10^6 \times 10\ \mu\text{s} = 10$ s.
(c) $10^9$ steps × 10 µs $= 10^4$ s $= 2.78$ hours.

And this is for a *small* circuit. Per-step cost grows with circuit size, roughly linearly or worse with sparse solvers, so transistor-level simulation of a whole chip over realistic times is impractical. Digital chips are therefore simulated at higher abstraction levels: event-driven RTL and gate-level simulation, plus static timing analysis. SPICE is reserved for cells, analog blocks and critical paths. That is the abstraction stack ([00-02](../chapters/00-02-the-abstraction-stack.md)) in action.

### Solution 00-04.9

(a) $g'(V) = -\frac{1}{1000} - \frac{I_s}{V_T}e^{V/V_T}$, so

$$
V_{k+1} = V_k - \frac{\frac{5 - V_k}{1000} - I_s\big(e^{V_k/V_T} - 1\big)}{-\frac{1}{1000} - \frac{I_s}{V_T}e^{V_k/V_T}} .
$$

(b) From $V_0 = 0.70$ V: $V_1 = 0.69352$ V, $V_2 = 0.692562$ V, $V_3 = 0.6925436$ V. It has converged to $V_D = 0.6925$ V. The diode current is $(5 - 0.6925)/1000 = 4.307$ mA.

(c) At 0.60 V the diode current is tiny, so $g$ is dominated by the resistor and the slope is shallow. The tangent line overshoots to $V_1 = 1.358$ V, where $e^{V/V_T}$ is astronomically large (about $10^{22}$). From there each Newton step reduces $V$ by only about $V_T \approx 26$ mV, because the exponential term dominates. It takes about 25 more steps to crawl back. SPICE prevents this with **junction-voltage limiting**: it caps how much a diode or transistor junction voltage may change in one iteration, using a logarithmic update when the step is large. That keeps the exponential in range. Further convergence aids are source stepping (ramping sources up from zero) and gmin stepping.

### Solution 00-04.10

(a) The allowed difference is $0.5 \times 0.01 = 0.005$. The actual difference is $\lvert 2.21 - 2.2046\rvert = 0.0054 > 0.005$, so the check **fails**.
(b) Correctly rounded to the same three significant figures, 2.2046 is **2.20**.
(c) "2.2" has a tolerance of 0.05, and $\lvert 2.2 - 2.2046\rvert = 0.0046$, so it passes. The trade-off: fewer digits pass more easily but tell the reader less, and a learner checking an answer to three figures cannot use a two-figure key. Publish as many digits as the inputs justify, typically 3–4, and round them correctly.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 00-04.1a | `4.7k` | 4700 | Ω |
| 00-04.1b | `10u` | 1.0×10^-5 | F |
| 00-04.1c | `2.2n` | 2.2×10^-9 | F |
| 00-04.1d | `1meg` | 1.0×10^6 | Ω |
| 00-04.1e | `3m` | 3.0×10^-3 | A |
| 00-04.1f | `1M` | 1.0×10^-3 | Ω |
| 00-04.2a | output voltage | 4.000 | V |
| 00-04.2b | current | 0.800 | mA |
| 00-04.2c | total power | 9.600 | mW |
| 00-04.3a | relative difference | 1.85×10^-16 | — |
| 00-04.4a | $V_a$ | 5.000 | V |
| 00-04.4b | $V_b$ | 2.500 | V |
| 00-04.4c | source current | 5.000 | mA |
| 00-04.5a | −3 dB frequency | 1.592 | kHz |
| 00-04.5b | gain at 10 kHz | −16.07 | dB |
| 00-04.6 | stable value of $\sqrt{x^2+1} - x$ | 5.00×10^-9 | — |
| 00-04.7a | 8-bit adder test time | 65.5 | µs |
| 00-04.7b | 16-bit multiplier test time | 4.29 | s |
| 00-04.7c | 32-bit adder test time | 585 | years |
| 00-04.8a | time steps | 1.0×10^6 | — |
| 00-04.8b | run time at 1 ns step | 10 | s |
| 00-04.8c | run time at 1 ps step | 2.78 | h |
| 00-04.9a | $V_1$ from 0.70 V | 0.69352 | V |
| 00-04.9b | $V_2$ | 0.692562 | V |
| 00-04.9c | $V_3$ | 0.6925436 | V |
| 00-04.9d | diode current | 4.307 | mA |
| 00-04.9e | first iterate from 0.60 V | 1.358 | V |
| 00-04.10a | difference 2.21 vs 2.2046 | 0.0054 | — |
