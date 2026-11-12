# Problems 01-06 · Techniques of Integration

Chapter: [01-06](../chapters/01-06-techniques-of-integration.md) · Worked solutions: [01-06 solutions](../solutions/01-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** angles in radians; $\ln$ is the natural log; $k = 1.380649\times10^{-23}$ J/K and $T = 300$ K where needed; answers to 4 significant figures unless stated. Name the technique you use, and check indefinite integrals by differentiating.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 01-06.1 [A]

Evaluate by substitution.

(a) $\displaystyle\int_0^{\pi/6}\cos 3x\,dx$  (b) $\displaystyle\int_0^2x\sqrt{x^2 + 5}\,dx$  (c) $\displaystyle\int_1^e\frac{\ln x}{x}\,dx$  (d) $\displaystyle\int_0^{\pi/4}\tan x\,dx$

### Problem 01-06.2 [A]

Evaluate by integration by parts.

(a) $\displaystyle\int_0^\pi x\sin x\,dx$  (b) $\displaystyle\int_1^e\ln x\,dx$  (c) $\displaystyle\int_0^1x^2e^x\,dx$ (tabular)  (d) $\displaystyle\int_0^1\arctan x\,dx$

### Problem 01-06.3 [A]

Evaluate using trigonometric identities or orthogonality.

(a) $\displaystyle\int_0^\pi\sin^2x\,dx$  (b) $\displaystyle\int_0^{2\pi}\sin 3x\sin 5x\,dx$  (c) $\displaystyle\int_0^{2\pi}\cos^24x\,dx$  (d) $\displaystyle\int_0^{\pi/2}\sin^3x\,dx$

### Problem 01-06.4 [A]

Use partial fractions.

(a) $\displaystyle\int_2^3\frac{dx}{x^2 - 1}$  (b) $\displaystyle\int_0^1\frac{3x + 5}{(x + 1)(x + 3)}\,dx$  (c) $\displaystyle\int_1^2\frac{dx}{x(x + 1)^2}$ (repeated factor)

### Problem 01-06.5 [B]

Decide whether each improper integral converges, and evaluate those that do.

(a) $\displaystyle\int_1^\infty\frac{dx}{x^2}$  (b) $\displaystyle\int_1^\infty\frac{dx}{\sqrt{x}}$  (c) $\displaystyle\int_0^1\frac{dx}{\sqrt{x}}$  (d) $\displaystyle\int_0^\infty e^{-2t}\,dt$  (e) $\displaystyle\int_0^\infty t^2e^{-t}\,dt$

### Problem 01-06.6 [B]

**Delay estimates.** An on-chip wire segment behaves as one RC stage with $\tau = 50$ ps.

(a) Find its Elmore delay and its 50% step-response delay.
(b) Two such stages, buffered so they do not interact, give the impulse response $h(t) = \dfrac{t}{\tau^2}e^{-t/\tau}$ (01-04). Show that $\int_0^\infty h\,dt = 1$, and find the centroid (Elmore delay) of $h$.
(c) Explain why first-moment delays add along a buffered chain.

### Problem 01-06.7 [B]

A ringing voltage $v(t) = e^{-100t}\sin(1000t)$ V appears across a 1 Ω resistor for $t \ge 0$.

(a) Using $\sin^2\theta = \tfrac{1}{2}(1 - \cos2\theta)$ and the loop formula of §3.2, show that the dissipated energy is

$$
W = \int_0^\infty e^{-2at}\sin^2bt\,dt = \frac{b^2}{4a(a^2 + b^2)},
$$

with $a = 100$ s⁻¹ and $b = 1000$ rad/s.

(b) Evaluate $W$. Compare with $1/(4a)$, the value if $\sin^2$ were replaced by its average ½. Explain the agreement.

### Problem 01-06.8 [B]

A triangle wave of peak 1 has Fourier coefficients $b_n = \dfrac{8}{\pi^2n^2}(-1)^{(n-1)/2}$ for odd $n$ (and 0 otherwise). Its mean square is 1/3.

(a) Find the fundamental's amplitude.
(b) What fraction of the power is in the fundamental? Compare with the square wave (81.06%).
(c) Why do the triangle's harmonics fall as $1/n^2$, while the square wave's fall as $1/n$? (Hint: what is discontinuous in each wave?)

### Problem 01-06.9 [B]

A circuit has $H(s) = \dfrac{10}{(s + 2)(s + 5)}$.

(a) Decompose it by cover-up.
(b) Each term $A/(s + a)$ corresponds to the time function $Ae^{-at}$. Write the impulse response $h(t)$.
(c) Find when $h(t)$ peaks, and the peak value.

### Problem 01-06.10 [B]

**kT/C noise.**

(a) Find the noise bandwidth of a one-pole RC filter with $f_c = 1$ kHz.
(b) A 1 kΩ resistor has noise density $\sqrt{4kTR}$. Find it, and the RMS noise behind a filter with $f_c = 1$ kHz.
(c) For a general RC filter, $f_c = 1/(2\pi RC)$. Show that $4kTR\times\text{ENBW} = kT/C$, independent of $R$.
(d) Find the RMS kT/C noise on a 1 pF sampling capacitor.

### Problem 01-06.11 [B]

**Numerical integration.**

(a) Apply Simpson's rule with $n = 4$ to $\int_0^1e^{-x^2}\,dx$ (true value 0.746824). Find the error.
(b) Apply Simpson's rule with $n = 8$ to the sine integral $\mathrm{Si}(\pi) = \int_0^\pi\frac{\sin x}{x}\,dx$, using the limit value 1 at $x = 0$.
(c) The Gibbs overshoot: the partial Fourier sums of a ±1 square wave peak near $\frac{2}{\pi}\mathrm{Si}(\pi)$. Evaluate it, and express the overshoot above 1 as a percentage of the jump (2).

### Problem 01-06.12 [C]

**Harmonic power and THD.**

(a) Using orthogonality, show that the mean square of $A_1\sin\omega t + A_3\sin3\omega t$ is $(A_1^2 + A_3^2)/2$.
(b) Total harmonic distortion is $\text{THD} = \sqrt{\sum_{n\ge2}A_n^2}\big/A_1$. For the ±1 square wave, use Parseval and $\sum_{n\text{ odd}}1/n^2 = \pi^2/8$ to find its THD exactly.
(c) An audio amplifier is specified at THD = 0.01%. If the distortion is a single 3rd harmonic, what is its amplitude relative to the fundamental, in dB?

### Problem 01-06.13 [C]

**Flicker noise and a divergent integral.** A MOSFET amplifier's input noise has a 1/f component $S(f) = K/f$ with $K = 10^{-12}$ V².

(a) Find the noise power and RMS voltage from 1 Hz to 1 MHz.
(b) Repeat from 0.01 Hz to 1 MHz. By how much did the RMS grow for 2 more decades?
(c) Show that every decade carries the same power, and evaluate it.
(d) The integral from 0 diverges. Why is that not a practical catastrophe? What sets the lower limit in a real measurement?

### Problem 01-06.14 [C]

**Charge on a varactor (substitution with a power).** A reverse-biased pn junction has capacitance $C(v) = \dfrac{C_0}{\sqrt{1 - v/\phi}}$ for $v < 0$, with $C_0 = 10$ pF and built-in potential $\phi = 0.7$ V.

(a) Using $u = 1 - v/\phi$, find the charge $q = \int_0^{V}C(v)\,dv$ stored when the junction is taken from 0 to $V = -5$ V.
(b) Find the effective capacitance $\lvert q/V\rvert$, and compare it with the small-signal capacitance $C(-5\text{ V})$.
(c) Varactors tune RF oscillators. Which capacitance, the effective or the small-signal one, sets the oscillation frequency for a small RF swing about a −5 V bias? Explain.

### Problem 01-06.15 [C]

**Previewing the Laplace transform.** For $s > 0$, evaluate the improper integrals

(a) $\displaystyle\int_0^\infty e^{-at}e^{-st}\,dt$ with $a > 0$  (b) $\displaystyle\int_0^\infty te^{-st}\,dt$  (c) $\displaystyle\int_0^\infty\sin(\omega t)\,e^{-st}\,dt$

in general, then numerically for $s = 2$, $a = 1$, $\omega = 3$. For which $s$ does (a) converge if $a$ is negative (a growing exponential)?

---

## Objective coverage

| Learning objective (chapter 01-06) | Problems |
|---|---|
| 1. Substitution, with limits; physical changes of variable | 1, 14 |
| 2. Integration by parts; moments | 2, 5(e), 6, 7, 15 |
| 3. Partial fractions; modes | 4, 9 |
| 4. Trig integrals; orthogonality; Fourier coefficients and harmonic power | 3, 7, 8, 12 |
| 5. Improper integrals; noise bandwidth; numerical integration | 5, 10, 11, 13, 15 |
