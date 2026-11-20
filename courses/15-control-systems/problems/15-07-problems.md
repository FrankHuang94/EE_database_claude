# Problems 15-07 · Frequency-Domain Design: Bode, Nyquist and Margins

Chapter: [15-07](../chapters/15-07-frequency-domain-design.md) · Worked solutions: [15-07 solutions](../solutions/15-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Negative unity feedback around the loop gain $L(s)$ unless stated. Phase margin (PM) in degrees, gain margin (GM) as a ratio and in dB.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 15-07.1 [A]

**Margins of a three-pole loop.** For $L = 40/[s(s + 2)(s + 10)]$, find the phase crossover frequency and the gain margin by hand, then the gain crossover and phase margin numerically. Check the gain margin with Routh.

### Problem 15-07.2 [A]

**Reading a measured Bode plot.** A regulator's measured loop gain crosses 0 dB at 1 kHz with a phase of −125°. Find the phase margin, the damping ratio and overshoot it suggests (using the standard-loop relation), and the delay margin.

### Problem 15-07.3 [A]

**Two zeros, one difference.** Compare the magnitude (in dB) and phase of $(1 + s/z)$ and $(1 - s/z)$ at $\omega = z$. Why does a right-half-plane zero limit a loop's crossover frequency?

### Problem 15-07.4 [B]

**Nyquist for three equal poles.** For $L = K/(s + 1)^3$: (a) where does the Nyquist plot cross the negative real axis? (b) For $K$ = 4, find the gain margin and the phase margin. (c) Relate to Example 15-05.3.

### Problem 15-07.5 [B]

**Choosing a gain with a delay.** $L = Ke^{-sT}/s$ with $T$ = 2 ms. Find $K$ for a 60° phase margin, and the resulting gain margin.

### Problem 15-07.6 [B]

**Designing for phase margin.** Choose $K$ in $L = K/[s(s + 5)]$ for a 60° phase margin, using the standard-loop relation. Confirm the crossover and the margin.

### Problem 15-07.7 [B]

**Phase margin against closed-loop gain.** An op-amp has $A_0 = 10^5$, a dominant pole at 10 Hz (1 MHz gain-bandwidth) and a second pole at 1 MHz. Find the crossover and phase margin as a unity-gain buffer and at a closed-loop gain of 10.

### Problem 15-07.8 [B]

**A capacitive load.** Example 15-07.6's op-amp (buffer, 65.5° phase margin) has a 50 Ω output resistance and drives a 1 nF load, which adds a pole at $1/(R_oC_L)$. Find that pole's frequency and the new crossover, phase margin and gain margin.

### Problem 15-07.9 [C]

**What a sensitivity peak guarantees.** A loop has $M_s$ = 1.5. Find the minimum gain margin (ratio and dB) and minimum phase margin this guarantees, and derive both bounds.

### Problem 15-07.10 [C]

**The waterbed.** For $L = 4/[(s + 1)(s + 2)]$: (a) find $\lvert S\rvert$ at DC; (b) find the frequency above which $\lvert S\rvert > 1$; (c) find $M_s$ and its frequency; (d) evaluate $\int_0^\infty\ln\lvert S\rvert\,d\omega$ numerically and explain the result.

### Problem 15-07.11 [C]

**A PLL's phase margin.** For the third-order PLL ($\tau_z$ = 5 µs, $\tau_p = \tau_z/11$, $K = 9.09 \times 10^{10}$ s⁻²): (a) find the crossover and phase margin; (b) find the frequency of maximum phase margin and the margin there; (c) find the gain $K$ that places crossover there, and its ratio to the design gain.

### Problem 15-07.12 [C]

**Stabilizing a levitation plant.** The linearized magnetic-levitation plant of 15-01 behaves like $P = 1/(s^2 - 100)$ (poles at ±10). A PD controller $C = K(s + 5)$ closes the loop. (a) Find the range of $K$ for stability with Routh. (b) At $K$ = 40, count Nyquist encirclements and confirm stability. (c) Find the phase margin at $K$ = 40. (d) What does the Nyquist criterion say at $K$ = 15?

### Problem 15-07.13 [B]

**Adding a sampling delay.** Example 15-07.1's servo ($L = 100/[s(s + 10)]$) is moved to a digital controller that adds 50 ms of delay. Find the original delay margin, the new phase margin and the new gain margin.

### Problem 15-07.14 [A]

**Reading margins.** A loop has a 45° phase margin and a 3 dB gain margin. By what factor can its gain rise before it oscillates? Is it robust? What would you ask next?

---

## Objective coverage

| Learning objective (chapter 15-07) | Problems |
|---|---|
| 1. Bode plots and margins | 1, 2, 3, 7, 8, 14 |
| 2. The Nyquist criterion | 4, 12 |
| 3. Phase margin, damping and bandwidth | 2, 6 |
| 4. Time delay and delay margin | 2, 5, 13 |
| 5. Sensitivity peak, Bode's integral and chip loops | 8, 9, 10, 11 |
