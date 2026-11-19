# Problems 07-04 · Laplace-Domain Circuit Analysis

Chapter: [07-04](../chapters/07-04-laplace-domain-circuit-analysis.md) · Worked solutions: [07-04 solutions](../solutions/07-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** passive sign convention throughout; transforms use $0^-$ initial values. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 07-04.1 [A]

**Element models.** A 20 mH inductor carries 0.5 A and a 4.7 µF capacitor holds 5 V at $t = 0^-$. (a) Draw both s-domain models of each element and give the value and units of each initial-condition source. (b) Show with the series model that a shorted inductor keeps its current, and with the parallel model that an open capacitor keeps its voltage.

### Problem 07-04.2 [A]

**An impedance with poles and zeros.** Find $Z(s)$ for a 100 Ω resistor in series with the parallel combination of 10 mH and 1 µF. Give its poles and zeros, its values at $s = 0$ and $s \to \infty$, and explain physically why it has poles on the imaginary axis.

### Problem 07-04.3 [A]

**The limit theorems, and when one lies.** (a) For $V(s) = \dfrac{10(s + 200)}{s(s + 100)(s + 400)}$, find $v(0^+)$ and $v(\infty)$, checking that the final-value theorem applies. (b) For $V(s) = \dfrac{10}{s(s^2 + 10^6)}$, what does $\lim_{s\to0}sV(s)$ give, and what does $v(t)$ actually do? Find its average and its maximum.

### Problem 07-04.4 [B]

**A complete response.** A parallel combination of $R$ = 250 Ω, $L$ = 50 mH and $C$ = 2 µF has, at $t = 0^-$, an inductor current of 10 mA (flowing down through the inductor) and a capacitor voltage of 5 V. At $t = 0$ a current source of 20 mA is switched into the top node. (a) Draw the s-domain circuit with parallel initial-condition sources and find $V(s)$. (b) Find $v(t)$ and $v(1\text{ ms})$. (c) Separate the zero-state and zero-input parts and give the zero-state part's amplitude.

### Problem 07-04.5 [B]

**A Thévenin source with stored charge.** A 2 µF capacitor charged to 10 V in series with 1 kΩ is connected at $t = 0$ across a 0.5 H inductor that carries no current. (a) Write the source's s-domain Thévenin equivalent and find $I(s)$. (b) Classify the response and find $i(t)$. (c) Find the peak current and when it occurs. (d) Use the initial-value theorem to find the inductor voltage at $0^+$.

### Problem 07-04.6 [B]

**Mesh analysis in s.** A 10 V step drives mesh 1: $R_1$ = 10 Ω in series with $C$ = 10 µF to ground. The capacitor is shared with mesh 2, which continues through $L$ = 1 mH and $R_2$ = 10 Ω back to ground. Everything starts at rest. (a) Write the two mesh equations and find the inductor current $I_2(s)$. (b) Give the poles and ζ. (c) Find the final inductor current, its peak and the time of the peak, and $i_2(0.5\text{ ms})$.

### Problem 07-04.7 [B]

**The RC ladder in s.** For the ladder of Example 07-03.6 ($R_1 = R_2$ = 1 kΩ, $C_1 = C_2$ = 1 µF), find $H(s) = V_2/V_{in}$ by nodal analysis in the s-domain. Give its poles, and check them against the state-matrix eigenvalues of 07-03. Why are there no finite zeros?

### Problem 07-04.8 [B]

**An RF trap.** A 50 Ω source drives a node from which a series LC ($L$ = 1 µH, $C$ = 1 nF) goes to ground; the output is the node voltage. (a) Find $H(s)$. (b) Locate its zeros and the frequency they remove. (c) Find the poles and ζ. (d) What are $H(0)$ and $H(\infty)$, and why?

### Problem 07-04.9 [B]

**An impulse response from an admittance.** For the series RLC of Problem 07-03.14 ($R$ = 10 Ω, $L$ = 1 mH, $C$ = 1 µF), the input admittance is $Y(s) = I(s)/V(s)$. (a) Find $Y(s)$. (b) Find the current's impulse response $i_\delta(t)$ (the current for $v = \delta(t)$ V·s) and its value at $0^+$. (c) Find the first time $i_\delta$ crosses zero, and explain why it equals the time of the step-response current's peak.

### Problem 07-04.10 [B]

**Inductors forced into series.** A 10 mH inductor carries 1 A, its current circulating through a closed switch; a 30 mH inductor carries nothing. At $t = 0$ the switch opens, leaving the two inductors in series. (a) Use the s-domain (or flux conservation) to find the common current just after the switch opens. (b) Find the energy before and after. (c) What flux linkage did the switching transfer to the 30 mH inductor, and what does the s-domain predict for the switch voltage? (d) Compare with Example 07-04.4.

### Problem 07-04.11 [C]

**A right-half-plane zero.** A transistor amplifier is modeled as a transconductance $g_m$ = 10 mS from gate to drain node, a load $R_D$ = 5 kΩ and $C_L$ = 2 pF from drain to ground, and $C_{gd}$ = 0.5 pF from gate to drain. The gate is driven directly by an ideal 10 mV step. (a) Find $H(s) = V_{out}/V_{in}$ by nodal analysis at the drain. (b) Locate its pole and zero, and give the DC gain. (c) Use the initial- and final-value theorems to find $v_{out}(0^+)$ and $v_{out}(\infty)$. (d) Find $v_{out}(t)$ and when it crosses zero. (e) Explain the wrong-way start physically.

### Problem 07-04.12 [B]

**A Sallen–Key low-pass.** The input feeds $R$ to node a, then $R$ to node b; a capacitor $C$ goes from node b to ground, and another $C$ from node a to the amplifier output; a non-inverting amplifier of gain $K$ drives the output from node b. With $R$ = 10 kΩ and $C$ = 10 nF: (a) find $H(s)$ by nodal analysis; (b) find $f_0$, and the gain $K$ that gives $Q = 1/\sqrt2$ (a Butterworth response); (c) at what $K$ does the circuit become unstable, and what happens there?

### Problem 07-04.13 [C]

**The cubic test: an RC phase-shift oscillator.** Three identical RC low-pass sections ($R$ = 10 kΩ in series, $C$ = 10 nF to ground), not buffered from each other, are connected in a loop with an inverting amplifier of gain $-K$. (a) Show that the ladder's transfer function is $1/(x^3 + 5x^2 + 6x + 1)$ with $x = sRC$. (b) Write the loop's characteristic equation and use the cubic condition of chapter §3.8 to find the gain at which oscillation starts. (c) Find the oscillation frequency, and confirm it by factoring the characteristic polynomial at that gain.

### Problem 07-04.14 [B]

**An ESR window in numbers.** A legacy LDO needs at least 2.2 µF of output capacitance with an ESR between 0.1 Ω and 20 Ω (chapter §9). (a) Find the range of ESR-zero frequencies this allows with 2.2 µF. (b) A designer substitutes a 2.2 µF ceramic capacitor with 5 mΩ of ESR. Where is its zero? (c) The designer adds a 0.2 Ω resistor in series with the ceramic. Where is the zero now, and what voltage step does a 50 mA load step produce across the added resistance and the ESR? (d) An application note prints the zero for 0.1 Ω and 2.2 µF as 72.3 kHz. Is it right?

### Problem 07-04.15 [B]

**Convolution and the ramp.** An RC low-pass ($R$ = 1 kΩ, $C$ = 1 µF) starts uncharged and is driven from $t = 0$ by the ramp $v_{in} = kt$, with $k$ = 1 V/ms. (a) Find the impulse response $h(t)$. (b) Find $v_{out}(t)$ by evaluating the convolution integral $h * v_{in}$. (c) Find it again from $H(s)V_{in}(s)$ by partial fractions, and compare with 07-02's ramp response. (d) Find $v_{out}$ and the lag $v_{in} - v_{out}$ at 1 ms and at 5 ms, and the lag the output settles to.

### Problem 07-04.16 [B]

**Switching on a sinusoid.** The same uncharged RC low-pass is connected at $t = 0$ to $v_{in} = 10\cos(1000t)$ V. (a) Find $V_{out}(s)$ and, by partial fractions, the complete response. (b) Identify the steady-state part, and confirm that it equals $\lvert H(j\omega)\rvert\cos(\omega t + \angle H(j\omega))$ times the input amplitude. (c) Find the transient's initial value, $v_{out}$ at 1 ms, and the time after which the transient stays below 1% of the steady-state amplitude. (d) With $v_{in} = 10\cos(1000t + \phi)$, which switch-on phase φ between −90° and +90° makes the transient vanish, and why?

---

## Objective coverage

| Learning objective (chapter 07-04) | Problems |
|---|---|
| 1. s-domain element models with initial conditions | 1, 4, 5, 10 |
| 2. Impedances, dividers, nodal/mesh, Thévenin in s; characteristic polynomial | 2, 5, 6, 7, 8, 12 |
| 3. Transfer functions; poles and zeros from circuit structure | 2, 7, 8, 11, 14, 16 |
| 4. Impulse, step, convolution and complete responses; sinusoidal steady state from $H(j\omega)$; IVT/FVT; impulsive switching | 3, 4, 5, 9, 10, 11, 15, 16 |
| 5. Stability; passive versus active; onset of oscillation | 12, 13 |
| 6. Pole–zero reasoning in practice | 11, 14 |
