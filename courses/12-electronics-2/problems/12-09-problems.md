# Problems 12-09 · Oscillators

Chapter: [12-09](../chapters/12-09-oscillators.md) · Worked solutions: [12-09 solutions](../solutions/12-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** oscillator loop gain $L = A\beta$ for positive feedback, sustained oscillation at $L(j\omega_0) = 1$; crystal parameters are illustrative orders of magnitude, not a specific product.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 12-09.1 [A]

**Will it start?** An amplifier with gain 10 drives a feedback network whose response at its zero-phase frequency is 0.12. Find the loop gain there. Will the circuit start, and what effective amplifier gain will it settle at?

### Problem 12-09.2 [A]

**A Wien bridge.** Find the oscillation frequency of a Wien bridge with $R$ = 4.7 kΩ and $C$ = 22 nF in both arms, and the ratio $R_2/R_1$ of its non-inverting amplifier.

### Problem 12-09.3 [A]

**A ring oscillator.** Find the frequency of a seven-stage ring whose stages each delay 15 ps.

### Problem 12-09.4 [B]

**An unbalanced Wien bridge.** The series arm has $R_1$ = 10 kΩ and $C_1$ = 10 nF; the parallel arm has $R_2$ = 10 kΩ and $C_2$ = 20 nF. Show that the zero-phase frequency is $1/(2\pi\sqrt{R_1R_2C_1C_2})$ and the feedback fraction there is $1/(1 + R_1/R_2 + C_2/C_1)$, and evaluate both and the required gain.

### Problem 12-09.5 [B]

**Designing a phase-shift oscillator.** Choose $R$ for a 10 kHz three-section phase-shift oscillator with $C$ = 10 nF, assuming the ladder drives a buffer. What inverting gain is needed?

### Problem 12-09.6 [B]

**A Colpitts design.** A Colpitts oscillator has $L$ = 10 µH, $C_1$ = 2 nF and $C_2$ = 8 nF, with a 2 kΩ drain load. Find the frequency and the minimum $g_m$.

### Problem 12-09.7 [B]

**A VCO's startup.** A cross-coupled VCO's tank has $L$ = 1 nH, $C$ = 1 pF and $Q$ = 15. Find the frequency, the parallel loss resistance and the minimum $g_m$.

### Problem 12-09.8 [B]

**Series to parallel loss.** A 2 nH on-chip inductor has a series resistance of 1 Ω at 5 GHz. Find its $Q$ and the equivalent parallel resistance (exact and high-$Q$ approximation).

### Problem 12-09.9 [B]

**A watch crystal.** Model a 32.768 kHz tuning-fork crystal with $C_m$ = 2 fF and $R_m$ = 40 kΩ (illustrative). Find its motional inductance and $Q$.

### Problem 12-09.10 [B]

**Pulling.** For Example 12-09.5's crystal ($f_s$ = 10 MHz, $C_m$ = 25 fF, $C_0$ = 5 pF), find how far the frequency moves when the load capacitance changes from 10 to 12 pF, in hertz and ppm.

### Problem 12-09.11 [C]

**A five-stage ring, linear model.** For a ring of five single-pole inverting stages with τ = 10 ps, find the minimum stage gain and the oscillation frequency. Compare the gain requirement with three stages.

### Problem 12-09.12 [C]

**A comparator-limited Wien oscillator.** A Wien bridge (β = 1/3 at $f_0$) is driven by a high-gain amplifier that saturates hard at ±1 V, so its output is nearly a square wave. Using the describing function of an ideal limiter, $N(a) = 4V_s/(\pi a)$, find the amplitude of the output's fundamental and the amplitude at the bridge's output node.

### Problem 12-09.13 [B]

**A Pierce crystal oscillator.** A 25 MHz crystal has $C_m$ = 4 fF, $C_0$ = 1.5 pF and $R_m$ = 30 Ω (illustrative). (a) Find $f_p - f_s$ in ppm. (b) The Pierce circuit has $C_1 = C_2$ = 18 pF and 3 pF of stray capacitance. Find the load capacitance and how far above $f_s$ the circuit oscillates, in ppm. (c) Its inverter has $g_m$ = 5 mA/V. Find the negative resistance it presents at 25 MHz and the ratio to $R_m$ (the gain margin).

### Problem 12-09.14 [C]

**A loaded phase-shift ladder.** In a three-section phase-shift oscillator, the inverting amplifier's input resistance equals $R$ and loads the third node. Derive the ladder's transfer function by back-substitution, and find the oscillation frequency (as a multiple of $1/RC$) and the inverting gain needed. Compare with the buffered ladder of §3.2.

### Problem 12-09.15 [A]

**Relaxation timers.** (a) An op-amp astable has $\beta$ = 1/3, $R$ = 47 kΩ and $C$ = 1 nF. Find its period and frequency. (b) A 555 astable has $R_A$ = 4.7 kΩ, $R_B$ = 47 kΩ and $C$ = 1 nF. Find its frequency and duty cycle, and explain why the duty cycle cannot reach 50% in this connection.

---

## Objective coverage

| Learning objective (chapter 12-09) | Problems |
|---|---|
| 1. The Barkhausen criterion and amplitude limiting | 1, 12 |
| 2. RC oscillators | 2, 4, 5, 14 |
| 3. LC oscillators | 6, 7, 8 |
| 4. Crystals | 9, 10, 13 |
| 5. Ring oscillators | 3, 11 |
| 6. Relaxation oscillators | 15 |
