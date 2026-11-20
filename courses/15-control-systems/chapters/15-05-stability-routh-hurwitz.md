<!-- status: verified -->
# 15-05 · Stability and the Routh–Hurwitz Criterion

| | |
|---|---|
| **Course** | [15 · Control Systems](../README.md) |
| **University equivalent** | The stability material of a first course in feedback control: BIBO and internal stability, the Routh–Hurwitz criterion and its special cases, and stability ranges for a gain (Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 3; Nise, *Control Systems Engineering*, ch. 6; Ogata, *Modern Control Engineering*, ch. 5) |
| **Prerequisites** | [15-03 Time Response and Specifications](15-03-time-response.md), [15-04 Feedback Properties and Steady-State Error](15-04-feedback-and-steady-state-error.md), [02-08 Eigenvalues and Eigenvectors](../../02-complex-numbers-des-and-linear-algebra/chapters/02-08-eigenvalues-and-eigenvectors.md) |
| **Estimated study hours** | 5 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Define BIBO and internal stability, and decide either from pole locations.
2. Build a Routh array and count a polynomial's right-half-plane roots without solving it.
3. Handle the two special cases, a zero first-column entry and a row of zeros, and find imaginary-axis roots from the auxiliary polynomial.
4. Find the range of a gain (or of two parameters) for which a loop is stable, and the frequency at which it oscillates on the boundary.
5. Apply these tools to ring oscillators, regulators with an extra pole and a third-order PLL, and test relative stability by shifting the axis.

---

## 1. Big picture

Every result so far assumed the loop was stable. Feedback that is too strong, or too slow to arrive, turns a regulator into an oscillator: the correction overshoots, the next correction overshoots more, and the output swings until something saturates. Stability is therefore the first property checked in any loop design, and it is a property of the closed-loop poles: all of them must lie in the left half-plane. For a polynomial of high degree, or one with a free gain, finding the roots is not the point. The Routh–Hurwitz criterion answers the yes-or-no question, and the "for which gains?" question, from the coefficients alone, by arithmetic a person can do on paper.

- **Oscillators are loops designed to be unstable.** A ring oscillator is three or more inverting stages in a loop; Routh tells you the minimum stage gain and the oscillation frequency (12-09).
- **Regulators fail by oscillating.** An extra pole from a pass transistor's gate capacitance can turn a stable two-pole LDO into an oscillator (Problem 15-05.9).
- **Gain ranges are design limits.** The largest stable gain bounds the accuracy that proportional control can buy (15-04), and the boundary frequency predicts where an unstable loop rings.
- **Stability is checked again in the frequency domain** with margins (15-07), which also handle time delays; Routh is the algebraic counterpart.

## 2. Intuition first

**A loop that corrects too hard.** Picture a thermostat that sees a room 1 °C cold and fires the heater, but the heat takes a while to arrive. By the time the sensor reacts, the room has overshot. A gentle controller lets the oscillation die out; an aggressive one makes each overshoot larger than the last. The difference is whether the closed-loop poles have negative real parts (decaying modes) or positive ones (growing modes).

**An analogy: a price-adjustment loop.** Suppose a market maker adjusts a quoted price in proportion to the order imbalance, but sees the imbalance with a delay. Small adjustments converge on the clearing price. Large ones overshoot, the imbalance flips sign, and the price oscillates with growing swings, a cobweb. The analogy breaks down because markets are nonlinear and adaptive. A linear loop's instability is exact and predictable: once a pole crosses into the right half-plane, every disturbance grows exponentially until a nonlinearity stops it.

The s-plane sorts modes by what they do over time:

```text
              Im s
               ^
   decaying    |    growing
  oscillation  |  oscillation
       x       |       x          x  pole: mode e^{st}
               |
 --x-----------+-----------x--->  Re s
  fast decay   |   exponential growth
               |
       x       |       x
   (stable:    |  (unstable:
    left half) |   right half)
```

**Why delay and extra poles matter.** Each pole adds phase lag at high frequency. A one-pole loop can never lag more than 90°, and a two-pole loop never quite reaches 180°, so negative feedback with any positive gain stays stable. A third pole can push the lag past 180°, and then a large enough gain makes the "negative" feedback arrive in phase with the error: it reinforces instead of correcting.

## 3. Theory

### 3.1 BIBO stability and internal stability

A system is **bounded-input, bounded-output (BIBO) stable** if every bounded input produces a bounded output. For a linear time-invariant system with impulse response $h(t)$, the output is the convolution $y = h * u$ (11-03), so $\lvert y(t)\rvert \le \sup\lvert u\rvert\int_0^\infty\lvert h(\tau)\rvert d\tau$. BIBO stability holds if and only if

$$
\int_0^\infty\lvert h(t)\rvert\,dt < \infty .
$$

For a proper rational transfer function, $h(t)$ is a sum of terms $t^ke^{p_it}$, one group per pole, so the integral is finite exactly when **every pole has a negative real part**.

- A pole in the right half-plane gives a growing exponential: **unstable**.
- A simple pole on the imaginary axis gives a term that neither grows nor decays, for example $\sin\omega_0t$ for poles at $\pm j\omega_0$. The system is **marginally stable**, which is *not* BIBO stable: a bounded input at $\omega_0$ resonates and produces an output that grows as $t\sin\omega_0t$ (Problem 15-05.14).
- A repeated pole on the axis gives $t^k$ growth even without input.

A loop is **internally stable** if every transfer function inside it, from every input to every signal, is stable: $T$, $S$, $PS$ and $CS$ (15-02 §3.2, Problem 15-02.11). A pole–zero cancellation can make $T$ look stable while $PS$ is not; checking the characteristic polynomial $1 + L = 0$ formed *without* cancellation catches this.

For a state-space model, the poles are the eigenvalues of $\mathbf{A}$ (15-02), so stability means every eigenvalue of $\mathbf{A}$ has a negative real part (02-08, 02-09).

### 3.2 A quick necessary condition

Write the characteristic polynomial $a(s) = a_ns^n + a_{n-1}s^{n-1} + \cdots + a_0$ with $a_n > 0$. If every root has a negative real part, $a(s)$ factors into terms $(s + \alpha)$ with $\alpha > 0$ and $(s^2 + \beta s + \gamma)$ with $\beta, \gamma > 0$. Multiplying polynomials with positive coefficients gives positive coefficients. Hence:

> **Necessary condition.** A stable polynomial has every coefficient present and positive. A missing or negative coefficient means at least one root is on the imaginary axis or in the right half-plane.

The condition is also sufficient for degree 1 and 2, but not beyond: $s^3 + 2s^2 + 3s + 10$ has all coefficients positive and two right-half-plane roots (Example 15-05.1).

### 3.3 The Routh array

Arrange the coefficients in two rows, alternating, and compute each further row from the two above it:

$$
\begin{array}{c|cccc}
s^n & a_n & a_{n-2} & a_{n-4} & \cdots \\
s^{n-1} & a_{n-1} & a_{n-3} & a_{n-5} & \cdots \\
s^{n-2} & b_1 & b_2 & b_3 & \cdots \\
s^{n-3} & c_1 & c_2 & \cdots & \\
\vdots & & & & \\
s^0 & \ast & & &
\end{array}
\qquad
b_1 = \frac{a_{n-1}a_{n-2} - a_na_{n-3}}{a_{n-1}},\quad
b_2 = \frac{a_{n-1}a_{n-4} - a_na_{n-5}}{a_{n-1}},\quad
c_1 = \frac{b_1a_{n-3} - a_{n-1}b_2}{b_1} .
$$

Each new entry is minus the determinant of a 2 × 2 block (the first column of the two rows above and the column to the right of the entry), divided by the first entry of the row immediately above. Missing coefficients are zeros. A row may be multiplied by any positive number to simplify the arithmetic without changing the conclusion.

> **Routh–Hurwitz criterion.** The number of roots of $a(s)$ with positive real part equals the number of sign changes in the first column of the Routh array. All roots are in the open left half-plane if and only if every first-column entry is positive.

**The cubic, in closed form.** For $a_3s^3 + a_2s^2 + a_1s + a_0$ the first column is $a_3$, $a_2$, $(a_2a_1 - a_3a_0)/a_2$, $a_0$. With positive coefficients, the cubic is stable if and only if

$$
a_2a_1 > a_3a_0 .
$$

This one inequality covers most loop problems with three poles.

> **Going deeper — why counting sign changes counts roots.** The array is a sequence of polynomial divisions, each row encoding the even or odd part of a polynomial of one lower degree. Routh's theorem follows from a continuity argument: as the coefficients vary, a root can cross the imaginary axis only when some first-column entry passes through zero, and each crossing changes the sign-change count by the number of roots that cross: one for a real root passing through the origin, two for a complex pair crossing the imaginary axis (Example 15-05.1 shows one negative entry producing two sign changes). Starting from a polynomial whose roots are all in the left half-plane (no sign changes) and deforming it proves the count. A rigorous proof uses Cauchy indices or Sturm sequences (Gantmacher, *The Theory of Matrices*, vol. 2, ch. 15); it is beyond BSEE, and the lab checks the criterion against computed roots instead.

### 3.4 The two special cases

**A zero in the first column, rest of the row not all zero.** The next division would divide by zero. Replace the zero with a small positive number $\varepsilon$, continue, and count sign changes as $\varepsilon \to 0^+$. (The result is the same with a small negative $\varepsilon$.) Equivalently, multiply the polynomial by $(s + 1)$, which adds a stable root and usually removes the zero. A zero first-column entry always signals that the polynomial is not stable.

**A whole row of zeros.** This happens when the polynomial has a factor with roots symmetric about the origin: pairs $\pm j\omega$, pairs $\pm\sigma$, or quadruples $\pm\sigma \pm j\omega$. Form the **auxiliary polynomial** $A(s)$ from the row *above* the zero row, using its entries as coefficients of every other power of $s$, starting with the power that labels that row. $A(s)$ divides $a(s)$, and its roots are the symmetric roots. Replace the zero row with the coefficients of $dA/ds$ and continue. Sign changes below the auxiliary row count right-half-plane roots among the symmetric ones. Roots of $A(s)$ on the imaginary axis are where a loop at its stability boundary oscillates.

### 3.5 Stability ranges for a gain

When the characteristic polynomial contains a gain $K$, carry $K$ through the array symbolically. Each first-column entry is then a function of $K$, and requiring all to be positive gives the stable range. At a boundary value of $K$, one first-column entry is zero:

- if it is the $s^0$ entry, a root sits at the origin;
- if it is the $s^1$ entry, the row above gives an auxiliary polynomial whose roots $\pm j\omega_{osc}$ are the **oscillation frequency** at the boundary.

Just past the boundary, a loop oscillates near $\omega_{osc}$ with a slowly growing amplitude, until a nonlinearity limits it. This is how oscillators are designed: aim just past the boundary and let saturation set the amplitude (12-09, and the ring oscillator of the lab).

### 3.6 Relative stability

Routh tests the imaginary axis, but a settling-time specification needs every root left of some line $s = -\sigma_0$ (15-03). Substitute $s = z - \sigma_0$, expand, and apply Routh to the polynomial in $z$: sign changes now count roots to the right of $-\sigma_0$. Example 15-05.6 uses this to find the gains that guarantee a minimum decay rate.

### 3.7 What Routh cannot do

Routh needs a polynomial. A pure time delay $e^{-sT}$, common in digital control (15-11) and in thermal and chemical processes, makes the characteristic equation transcendental. A rational approximation such as the first-order Padé form $e^{-sT} \approx (1 - sT/2)/(1 + sT/2)$ lets Routh give an estimate, but the frequency-domain Nyquist criterion (15-07) handles delay exactly (Problem 15-05.13). Routh also says nothing about *how* stable a loop is beyond the axis shift of §3.6; margins (15-07) and root locus (15-06) give that.

## 4. Worked examples

### Example 15-05.1 · Positive coefficients are not enough (tier A)

**Setup.** Is $s^3 + 2s^2 + 3s + 10$ stable?

**Solution.** All coefficients are positive, so the necessary condition passes. The Routh array:

$$
\begin{array}{c|cc}
s^3 & 1 & 3 \\
s^2 & 2 & 10 \\
s^1 & (2 \cdot 3 - 1 \cdot 10)/2 = -2 & 0 \\
s^0 & 10 &
\end{array}
$$

The first column is 1, 2, **−2**, 10: two sign changes, so **2** roots lie in the right half-plane. The cubic test agrees: $a_2a_1 = 6 < a_3a_0 = 10$.

**Units check.** Not applicable: the coefficients are numbers.

**Sanity check.** The roots are −2.45 and **0.223** ± j2.01: one stable real root and an unstable complex pair, as counted.

### Example 15-05.2 · The largest stable gain (tier B)

**Setup.** A unity loop has $L(s) = K/[s(s + 2)(s + 4)]$. Find the range of $K$ for stability and the oscillation frequency at the boundary.

**Solution.** The characteristic polynomial is $s(s + 2)(s + 4) + K = s^3 + 6s^2 + 8s + K$. The array:

$$
\begin{array}{c|cc}
s^3 & 1 & 8 \\
s^2 & 6 & K \\
s^1 & (48 - K)/6 & \\
s^0 & K &
\end{array}
$$

Stability needs $48 - K > 0$ and $K > 0$: $0 < K <$ **48**. At $K$ = 48 the $s^1$ row vanishes, and the auxiliary polynomial from the $s^2$ row is $6s^2 + 48$, with roots $s = \pm j\sqrt 8$: the loop oscillates at **2.828** rad/s.

**Units check.** $K$ has units of 1/s³ here, matching $s^3$; $\omega$ in rad/s.

**Sanity check.** At $K$ = 48 the polynomial factors as $(s + 6)(s^2 + 8)$: one stable pole and a pair exactly on the axis.

### Example 15-05.3 · Three identical poles and the ring oscillator (tier B)

**Setup.** (a) Find the largest $K$ for which $L(s) = K/(1 + s/\omega_0)^3$ is stable in a unity negative-feedback loop, and the boundary frequency. (b) A ring oscillator is three identical inverting stages, each with small-signal gain $-A$ and a pole at $\omega_0$. Find the minimum $A$ for oscillation, and the frequency for $f_0 = \omega_0/2\pi$ = 1 GHz.

**Solution.** (a) With $x = s/\omega_0$, the characteristic polynomial is $(x + 1)^3 + K = x^3 + 3x^2 + 3x + (1 + K)$. The cubic test requires $3 \times 3 > 1 + K$, so $K <$ **8**. At $K$ = 8 the auxiliary polynomial $3x^2 + 9$ gives $x = \pm j\sqrt3$: the boundary frequency is $\sqrt3\,\omega_0$ = **1.732** $\omega_0$.

(b) Three inversions in a loop make the overall feedback negative, with loop gain $A^3/(1 + s/\omega_0)^3$. Oscillation starts when $A^3 > 8$, that is $A >$ **2**, at frequency $\sqrt3 f_0$ = **1.732** GHz. Each stage then contributes 60° of lag, and the three inversions supply the remaining 180°.

**Units check.** $x$ is dimensionless; $\omega = x\omega_0$ in rad/s.

**Sanity check.** The lab builds this ring with saturating stages of gain 2.2 in ngspice. It oscillates at 276.2 kHz for $f_0$ = 159.2 kHz, within 0.2% of $\sqrt 3 f_0$ = 275.7 kHz. Saturation lowers the effective gain until the loop sits on the boundary.

### Example 15-05.4 · The special cases (tier B)

**Setup.** Count the right-half-plane roots of (a) $s^4 + s^3 + 2s^2 + 2s + 3$ and (b) $s^4 + 2s^3 + 6s^2 + 8s + 8$.

**Solution.** (a) The $s^2$ row starts with $(1 \cdot 2 - 1 \cdot 2)/1 = 0$, but its second entry is 3, so replace the zero with $\varepsilon$:

$$
\begin{array}{c|ccc}
s^4 & 1 & 2 & 3 \\
s^3 & 1 & 2 & \\
s^2 & \varepsilon & 3 & \\
s^1 & (2\varepsilon - 3)/\varepsilon \approx -3/\varepsilon & & \\
s^0 & 3 & &
\end{array}
$$

The first column is $+, +, +, -, +$: **2** sign changes, so two roots in the right half-plane (they are $0.406 \pm j1.293$).

(b) The $s^2$ row is $(12 - 8)/2 = 2$ and 8; the $s^1$ row is $(2 \times 8 - 2 \times 8)/2 = 0$, a row of zeros. The auxiliary polynomial from the $s^2$ row is $A(s) = 2s^2 + 8$, with $dA/ds = 4s$. Replacing the zero row with 4, the first column is 1, 2, 2, 4, 8: no sign changes. So there are **0** right-half-plane roots, but the auxiliary polynomial's roots, $\pm j$**2**, lie on the imaginary axis. Dividing, $a(s) = (s^2 + 4)(s^2 + 2s + 2)$: the other roots are $-1 \pm j1$. The system is marginally stable, not BIBO stable.

**Units check.** Not applicable.

**Sanity check.** In (b), a loop with this characteristic polynomial would ring at 2 rad/s forever after any disturbance.

### Example 15-05.5 · A third-order PLL (tier C)

**Setup.** Example 15-02.6's PLL gets a small ripple capacitor $C_2$ = 100 pF across its loop filter ($R$ = 5 kΩ in series with $C$ = 1 nF). The loop gain becomes $L(s) = \dfrac{K(1 + s\tau_z)}{s^2(1 + s\tau_p)}$ with $K = \dfrac{I_{cp}K_v}{2\pi N(C + C_2)}$, $\tau_z = RC$ and $\tau_p = R\,CC_2/(C + C_2)$. For what parameters is it stable? Find $K$, $\tau_z$, $\tau_p$ and the closed-loop poles.

**Solution.** The characteristic polynomial is $s^2(1 + s\tau_p) + K(1 + s\tau_z) = \tau_ps^3 + s^2 + K\tau_zs + K$. The cubic test needs $1 \cdot K\tau_z > \tau_pK$, that is

$$
\tau_z > \tau_p ,
$$

for every $K > 0$: the loop filter's zero must come before (at a lower frequency than) its extra pole. Since $\tau_z/\tau_p = (C + C_2)/C_2 = 1 + C/C_2$, this always holds for a positive $C_2$, so the standard third-order loop is stable at any gain. Its *margin* is what $C_2$ costs (15-07).

Numbers: $K = 10^{11} \times C/(C + C_2)$ = **9.09 × 10¹⁰** s⁻², $\tau_z$ = **5** µs and $\tau_p$ = **0.455** µs, a ratio of **11**. The closed-loop poles are **−1.674 × 10⁶** s⁻¹ and $-2.630 \times 10^5 \pm j2.243 \times 10^5$ s⁻¹, all stable.

**Units check.** $K\tau_z$ has units of 1/s, matching the coefficient of $s$ against $\tau_ps^3$ (s) and $s^2$.

**Sanity check.** As $C_2 \to 0$, $\tau_p \to 0$ and the loop returns to the second-order case of 15-02.

### Example 15-05.6 · Guaranteeing a decay rate (tier C)

**Setup.** For Example 15-05.2's loop, find the gains for which every closed-loop pole lies left of $s = -0.5$ (so every mode decays at least as fast as $e^{-0.5t}$).

**Solution.** Substitute $s = z - 0.5$ into $s^3 + 6s^2 + 8s + K$ and expand:

$$
z^3 + 4.5z^2 + 2.75z + (K - 2.625) .
$$

The cubic test: $4.5 \times 2.75 > K - 2.625$, so $K <$ **15**; and the constant term $K - 2.625 > 0$, so $K >$ **2.625**. For $2.625 < K < 15$ every pole is left of −0.5. Below 2.625 the real pole near the origin is too slow; above 15 the complex pair crosses the line. At $K$ = 10, for example, the poles are −4.76 and **−0.620** ± j1.310.

**Units check.** The shift $\sigma_0$ = 0.5 s⁻¹ has the units of $s$.

**Sanity check.** The guaranteed-decay range (2.625, 15) lies inside the stability range (0, 48), as it must.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 15-05.1a | third first-column entry | −2 | — |
| Ex 15-05.1b | right-half-plane roots | 2 | — |
| Ex 15-05.1c | real part of the unstable pair | 0.223 | 1/s |
| Ex 15-05.2a | largest stable K | 48 | 1/s³ |
| Ex 15-05.2b | boundary frequency | 2.828 | rad/s |
| Ex 15-05.3a | largest stable K | 8 | — |
| Ex 15-05.3b | boundary frequency / ω0 | 1.732 | — |
| Ex 15-05.3c | minimum stage gain | 2 | — |
| Ex 15-05.3d | ring frequency for f0 = 1 GHz | 1.732 | GHz |
| Ex 15-05.4a | right-half-plane roots (a) | 2 | — |
| Ex 15-05.4b | right-half-plane roots (b) | 0 | — |
| Ex 15-05.4c | imaginary-axis root (b) | 2 | rad/s |
| Ex 15-05.5a | K | 9.09e10 | 1/s² |
| Ex 15-05.5b | τz | 5 | µs |
| Ex 15-05.5c | τp | 0.455 | µs |
| Ex 15-05.5d | τz/τp | 11 | — |
| Ex 15-05.5e | real closed-loop pole | −1.674e6 | 1/s |
| Ex 15-05.5f | complex closed-loop pole | −2.630e5 + j2.243e5 | 1/s |
| Ex 15-05.6a | largest K | 15 | 1/s³ |
| Ex 15-05.6b | smallest K | 2.625 | 1/s³ |
| Ex 15-05.6c | real part of the slow pair at K = 10 | −0.620 | 1/s |

## 5. Simulate it

The lab, [labs/15-05-lab](../labs/15-05-lab/README.md), provides `routh.py`: the Routh array with both special cases, `rhp_count`, `jw_roots` and a gain-range scanner. You:

1. **Check the criterion** against computed roots on hundreds of random polynomials, including ones built to hit each special case.
2. **Sweep a gain** for Example 15-05.2's loop and watch two roots cross the imaginary axis at $K$ = 48 and $\pm j2.83$.
3. **Run `ring3.cir`**, the three-stage ring oscillator of Example 15-05.3 built from saturating transconductors, and compare its frequency with the Routh boundary frequency and with a Python simulation of the same nonlinear circuit.
4. **Shift the axis** and map the gain range that guarantees a decay rate.

**Guided exercise (predict, then run).** **Before Part 3,** predict whether the ring oscillates at the linear model's frequency for a stage gain of 2.2 (303 kHz) or near the boundary frequency $\sqrt3 f_0$ (275.7 kHz), and why.

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Loop gain $K$ | Accuracy and disturbance rejection (15-04) | Approaches the stability boundary; ringing near it | Control designer |
| Extra filtering poles (ripple filters, anti-aliasing) | Noise and spur suppression | Phase lag; lower maximum stable gain | Analog / PLL designer |
| Zeros placed before extra poles (PLL $\tau_z > \tau_p$) | Stability for any gain | Less high-frequency filtering | PLL designer |
| Fewer, faster stages in a loop | A higher stability boundary | Power and area for the faster stages | Circuit designer |
| Ring stages and stage gain (oscillators) | Reliable start-up (gain margin above the Routh limit) | Power, phase noise, frequency set by stage count and delay | Oscillator designer |

## 7. Numbers to know

| Quantity | Value | Source |
|---|---|---|
| Stability of a cubic $a_3s^3 + a_2s^2 + a_1s + a_0$ | positive coefficients and $a_2a_1 > a_3a_0$ | §3.3 |
| Largest stable gain, three identical poles | 8 (18 dB), oscillation at $\sqrt3\,\omega_0$ | Example 15-05.3 |
| Minimum stage gain of an $n$-stage ring oscillator (identical single-pole stages) | $1/\cos(180°/n)$: 2 for three stages, 1.24 for five | Example 15-05.3, Problem 15-05.7 |
| Ring-oscillator frequency, $n$ single-pole stages | $\omega_0\tan(180°/n)$ | Problem 15-05.7 |
| Third-order PLL | stable for any $K$ if $\tau_z > \tau_p$ | Example 15-05.5 |

## 8. Common mistakes

- **Trusting positive coefficients beyond degree 2.** They are necessary, not sufficient.
- **Dividing by the wrong entry.** Each new row divides by the first entry of the row immediately above it.
- **Treating a zero first entry and a zero row the same way.** The first needs $\varepsilon$; the second needs the auxiliary polynomial.
- **Calling a marginally stable system stable.** Poles on the imaginary axis give sustained oscillation and unbounded resonant responses.
- **Forgetting that cancelled poles still count.** Use the characteristic polynomial $1 + L = 0$ formed without cancelling anything.
- **Using Routh on a loop with time delay.** It needs a polynomial; a Padé approximation gives only an estimate (Problem 15-05.13).

## 9. Practitioner lens

### State of the art (as of Nov 2026)

These are established practice; no perishable figures are quoted.

- **Stability is verified in simulation and on silicon, not by Routh alone.** Analog designers run loop-gain (stability) analyses in circuit simulators across process, voltage and temperature corners, and confirm on the bench with injection measurements (15-02, 15-07) **[Established]**.
- **Routh survives as a design tool for low-order loops**: choosing PLL filter ratios, checking regulator compensation in early architecture work, and deriving closed-form conditions such as $\tau_z > \tau_p$ that hold for every gain **[Established]**.
- **Ring oscillators are everywhere in chips**: as voltage-controlled oscillators in PLLs, as on-die process and temperature monitors, and as entropy sources. Their start-up condition is the Routh boundary of this chapter (12-09) **[Established]**.

### Why it matters commercially

- **Instability is a field-failure mode.** A regulator that oscillates only with a particular customer capacitor, or only when cold, causes returns and redesigns; stability across the specified range is part of a part's value.
- **Stability limits set performance limits.** The maximum stable loop gain bounds accuracy, bandwidth and disturbance rejection; architectures that remove a pole or add a zero raise that ceiling.
- **Oscillators are designed instabilities.** Their start-up margin is a yield item: too little gain margin and some parts fail to start at a corner.

### Marketing vs Reality

- **"Unconditionally stable."** *Reality:* stable for the stated load and component ranges. *Sanity check:* ask for the conditions (load capacitance, ESR, temperature) and the measured margins at the extremes.
- **"Stable at any gain."** *Reality:* sometimes true for an ideal third-order PLL (Example 15-05.5), but real loops have more poles and delay. *Sanity check:* ask what limits the gain in practice and what the phase margin is at the operating point.
- **"Guaranteed to start up."** *Reality:* an oscillator starts only if its loop gain exceeds the boundary at every corner. *Sanity check:* ask for the start-up margin at the slow, cold, low-supply corner.

### Questions for engineering leaders

1. **"What is the maximum stable loop gain, and how far below it do you operate?"**
   *Strong:* a number with the margin across corners and loads. *Evasive:* "it is stable in simulation".
2. **"What unmodelled poles or delays could reduce that limit?"**
   *Strong:* lists parasitic poles, sampling delay and package effects, with bench confirmation. *Evasive:* none considered.
3. **"For your oscillators, what is the start-up gain margin at the worst corner?"**
   *Strong:* a corner analysis and a production test. *Evasive:* typical-corner simulation only.
4. **"Is there any pole–zero cancellation hiding a mode?"**
   *Strong:* the characteristic polynomial checked without cancellation. *Evasive:* only the closed-loop transfer function checked.

## 10. Concept check

**Q1.** Why is a system with simple poles on the imaginary axis not BIBO stable?

<details><summary>Answer</summary>

Its impulse response does not decay, so $\int\lvert h\rvert$ diverges. A bounded input at the pole frequency resonates, and the output grows without bound, for example as $t\sin\omega_0t$.

</details>

**Q2.** Why must every coefficient of a stable polynomial be positive?

<details><summary>Answer</summary>

A stable polynomial is a product of factors $(s + \alpha)$ and $(s^2 + \beta s + \gamma)$ with positive $\alpha, \beta, \gamma$; products of polynomials with positive coefficients have positive coefficients.

</details>

**Q3.** State the cubic stability test.

<details><summary>Answer</summary>

$a_3s^3 + a_2s^2 + a_1s + a_0$ is stable if and only if all coefficients are positive and $a_2a_1 > a_3a_0$.

</details>

**Q4.** What does a row of zeros in a Routh array tell you, and how do you continue?

<details><summary>Answer</summary>

The polynomial has roots symmetric about the origin, often a pair on the imaginary axis. Form the auxiliary polynomial from the row above, replace the zero row with its derivative's coefficients, and continue. The auxiliary polynomial's roots are the symmetric roots.

</details>

**Q5.** Why can a two-pole loop with negative feedback never be made unstable by raising its gain, while a three-pole loop can?

<details><summary>Answer</summary>

$s^2 + a_1s + a_0 + K$ keeps positive coefficients for every $K > 0$, which is sufficient in degree 2. For a cubic, $K$ enters $a_0$, and the condition $a_2a_1 > a_3a_0$ fails for large $K$. Physically, two poles give less than 180° of lag at any frequency; three can give more.

</details>

**Q6.** How do you check that every pole decays faster than $e^{-\sigma_0t}$?

<details><summary>Answer</summary>

Substitute $s = z - \sigma_0$ and apply Routh to the polynomial in $z$; sign changes count roots to the right of $-\sigma_0$.

</details>

**Q7.** Why does a ring oscillator with stage gain 2.2 oscillate near $\sqrt3 f_0$ rather than at its linear model's frequency?

<details><summary>Answer</summary>

The linear model's poles are in the right half-plane, so the amplitude grows until the stages saturate. Saturation lowers the effective gain until the loop sits on its stability boundary (effective gain 2), where the oscillation frequency is $\sqrt3 f_0$.

</details>

Practice: [Problems 15-05](../problems/15-05-problems.md) · [Solutions](../solutions/15-05-solutions.md)

## 11. Key terms

[BIBO stability](../../../reference/glossary.md#bibo-stability) · [Marginal stability](../../../reference/glossary.md#marginal-stability) · [Internal stability](../../../reference/glossary.md#internal-stability) · [Characteristic polynomial](../../../reference/glossary.md#characteristic-polynomial) · [Routh array](../../../reference/glossary.md#routh-array) · [Routh–Hurwitz criterion](../../../reference/glossary.md#routh-hurwitz-criterion) · [Auxiliary polynomial](../../../reference/glossary.md#auxiliary-polynomial) · [Ring oscillator](../../../reference/glossary.md#ring-oscillator)

## 12. Connections

- **Builds on:** poles and modes ([15-02](15-02-transfer-functions-and-block-diagrams.md), [15-03](15-03-time-response.md)); the stability assumption behind steady-state errors ([15-04](15-04-feedback-and-steady-state-error.md)); eigenvalues ([02-08](../../02-complex-numbers-des-and-linear-algebra/chapters/02-08-eigenvalues-and-eigenvectors.md)); convolution ([11-03](../../11-signals-and-systems/chapters/11-03-convolution.md)).
- **Next:** [15-06 Root Locus](15-06-root-locus.md), which draws where the poles go as the gain changes, including where they cross the axis.
- **Used later:** gain and phase margins and time delay ([15-07](15-07-frequency-domain-design.md)); discrete-time stability ([15-11](15-11-digital-control.md)); oscillators ([12-09](../../12-electronics-2/chapters/12-09-oscillators.md)); PLL and regulator design ([15-12](15-12-control-applications-pll-regulators-thermal.md)).

## 13. Further study

- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 3 (stability, the Routh criterion and its special cases).
- N. S. Nise, *Control Systems Engineering*, ch. 6 (Routh–Hurwitz criterion, special cases, stability design via gain).
- K. J. Åström and R. M. Murray, *Feedback Systems*, ch. 5 (stability of linear systems; free online).
- F. R. Gantmacher, *The Theory of Matrices*, vol. 2, ch. 15 (the proof of the Routh–Hurwitz theorem; beyond BSEE).

## 14. Sources

1. Franklin, Powell and Emami-Naeini; Nise; Åström and Murray (Further study): BIBO stability and the Routh–Hurwitz criterion (textbook material).
2. Gantmacher (Further study): the proof of the criterion.

This chapter has no perishable industry figures; its practitioner statements are tagged [Established]. Every number in the examples is recomputed by the verify script from the Routh arrays and checked against numerically computed roots; the ring oscillator is simulated in Python and confirmed in ngspice.
