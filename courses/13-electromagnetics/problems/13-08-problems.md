# Problems 13-08 · Transmission Lines: Sinusoidal Steady State

Chapter: [13-08](../chapters/13-08-transmission-lines-sinusoidal-steady-state.md) · Worked solutions: [13-08 solutions](../solutions/13-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $c$ = 2.998 × 10⁸ m/s; phasors are peak amplitudes; distance $d$ is measured from the load; lines are lossless unless stated; return loss is positive in dB.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 13-08.1 [A]

**Line constants.** A lossless 75 Ω line has a phase velocity of 2 × 10⁸ m/s. Find $L'$, $C'$ and β at 100 MHz.

### Problem 13-08.2 [A]

**Invert it.** Find the input impedance of a lossless 50 Ω quarter-wave line terminated in 25 + j25 Ω.

### Problem 13-08.3 [A]

**From Γ to everything.** For $\lvert\Gamma\rvert$ = 0.1 and 0.3, find the return loss, VSWR and mismatch loss.

### Problem 13-08.4 [B]

**Through 0.3λ.** Find the input impedance of a lossless 50 Ω line 0.3λ long terminated in 30 − j40 Ω.

### Problem 13-08.5 [B]

**A 10 nH stub.** Find the shortest shorted 50 Ω air-line stub that acts as a 10 nH inductor at 1 GHz, in wavelengths and centimetres.

### Problem 13-08.6 [B]

**A 2 pF stub.** Find the shortest open 50 Ω air-line stub that acts as a 2 pF capacitor at 1 GHz.

### Problem 13-08.7 [B]

**Find the load from a slotted line.** On a 50 Ω line, the VSWR is 2 and the first voltage minimum is 0.1λ from the load. Find $\Gamma_L$ (magnitude and angle) and $Z_L$.

### Problem 13-08.8 [B]

**Power to a mismatched load.** A generator with 10 V peak open-circuit voltage and 50 Ω internal resistance drives a lossless 50 Ω line of any length terminated in 100 Ω. Find the power delivered to the load, and compare with a matched load.

### Problem 13-08.9 [B]

**A worse antenna through the same cable.** Repeat the practitioner calculation of §9 for an antenna with VSWR 3 at the end of 10 m of RG-58 at 1 GHz (7.054 dB). What return loss does the radio see?

### Problem 13-08.10 [C]

**Transformer bandwidth.** (a) For the 100 Ω to 50 Ω quarter-wave transformer of Example 13-08.5, find the fractional bandwidth for $\lvert\Gamma\rvert$ < 0.05. (b) Find the fractional bandwidth for $\lvert\Gamma\rvert$ < 0.1 when matching 10 Ω to 50 Ω with a single quarter-wave section.

### Problem 13-08.11 [C]

**Low-frequency Z₀.** A line has $R'$ = 0.5 Ω/m, $L'$ = 250 nH/m, $G'$ = 0 and $C'$ = 100 pF/m. Find γ and $Z_0$ at 1 MHz and at 100 MHz, with α in dB/m. Why is $Z_0$ complex at the lower frequency?

### Problem 13-08.12 [C]

**Make it distortionless.** For the line of Problem 13-08.11, what shunt conductance satisfies Heaviside's condition? Find the resulting α, $Z_0$ and velocity.

### Problem 13-08.13 [B]

**Half and quarter waves.** A 50 Ω line is terminated in 20 + j30 Ω. Find the input impedance when the line is λ/2 long and when it is λ/4 long.

### Problem 13-08.14 [B]

**Standing waves on a 25 Ω load.** A 1 GHz wave of 1 V peak travels on a 50 Ω air line toward a 25 Ω load. Find where the voltage minimum and the nearest maximum are, their values, and the peak current at the load.

### Problem 13-08.15 [C]

**A lossy open stub.** A 2.5 m length of 50 Ω cable (phase velocity 2 × 10⁸ m/s) with 0.5 dB/m of loss at 100 MHz is left open at the far end. (a) Find $\gamma\ell$, and the input impedance from $Z_{in} = Z_0\coth(\gamma\ell)$. (b) Find $\lvert\Gamma\rvert$ at the input and show that it equals $e^{-2\alpha\ell}$. (c) What return loss would an instrument measure, and what would a lossless line of the same length show? (Treat $Z_0$ as real.)

---

## Objective coverage

| Learning objective (chapter 13-08) | Problems |
|---|---|
| 1. γ and Z₀, exact and low-loss | 1, 11 |
| 2. Γ along the line and input impedance | 2, 4, 7, 13, 15 |
| 3. Standing waves, VSWR, return and mismatch loss, power | 3, 7, 8, 14 |
| 4. Stubs and quarter-wave transformers | 5, 6, 10 |
| 5. Loss masking and the distortionless line | 9, 12, 15 |
