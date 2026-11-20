# Problems 15-11 · Digital Control

Chapter: [15-11](../chapters/15-11-digital-control.md) · Worked solutions: [15-11 solutions](../solutions/15-11-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $T$ is the sample period; ZOH means zero-order hold; discrete transfer functions are in powers of $z$.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 15-11.1 [A]

**Mapping poles.** With $T$ = 0.05 s, where do the continuous poles −1, −10 and $-1 \pm j10$ map in the z-plane? Give magnitudes and angles.

### Problem 15-11.2 [A]

**The hold's phase cost.** A loop crosses over at 1 kHz and is sampled at 20 kHz. Estimate the phase lost to the zero-order hold.

### Problem 15-11.3 [B]

**A ZOH equivalent.** Find the ZOH equivalent of $2/(s + 2)$ for $T$ = 0.25 s, and check its DC gain.

### Problem 15-11.4 [B]

**Tustin and frequency warping.** Discretize Example 15-09.2's lead, $(1 + 0.45364s)/(1 + 0.112591s)$ (that example's design before rounding to 0.454 s and 0.1126 s; peak phase 37.0° at $\omega_m$ = 4.4248 rad/s), with Tustin at $T$ = 0.2 s, without and with prewarping at $\omega_m$. Give the coefficients and the frequency of peak phase in each case.

### Problem 15-11.5 [B]

**Jury.** Which of these are stable: (a) $z^2 - 1.2z + 0.5$; (b) $z^2 + 0.5z - 0.6$? Give the roots.

### Problem 15-11.6 [B]

**When Euler fails.** Map the stable pole $s = -100$ s⁻¹ with $T$ = 25 ms by forward Euler, backward Euler, Tustin and the exact map $e^{sT}$, and comment.

### Problem 15-11.7 [C]

**The stable-gain limit.** For proportional control of $1/[s(s + 1)]$ through a ZOH with $T$ = 0.5 s, find the largest stable gain.

### Problem 15-11.8 [C]

**Sampling a thermal limiter.** Example 15-08.6's thermal PI loop was designed for 60° of phase margin at $\omega_c$ = 5.24 rad/s, with a 0.1 s delay already included. Suppose that 0.1 s covers only the sensor and the computation, and the firmware's zero-order hold at $T$ = 0.1 s is an additional effect not yet counted. Estimate the extra phase lost and the remaining margin.

### Problem 15-11.9 [A]

**ADC resolution.** A die-temperature sensor spans 0 to 150 °C. What temperature step does a 12-bit ADC resolve? A 16-bit ADC?

### Problem 15-11.10 [C]

**A notch in the wrong place.** A notch filter designed in continuous time at 1 kHz is discretized with Tustin at a 4 kHz sample rate, without prewarping. At what frequency does the discrete notch fall? What does prewarping give?

### Problem 15-11.11 [B]

**A digital derivative that rings.** A PID's derivative term has $K_d$ = 0.1 s and filter time constant $T_f$ = 5 ms, and runs at $T$ = 20 ms. Find the backward-Euler difference equation's pole and gain, then the Tustin version's pole and gain, and the first two outputs of each for a unit step in the error at $k = 0$ (with $d_{-1} = 0$).

### Problem 15-11.12 [B]

**Type and ramp error in z.** For Example 15-11.5's loop (proportional gain $K$ = 1, ZOH, $T$ = 0.5 s), find the system type and the velocity constant from $L(z)$, and the steady error at the sample instants to a unit ramp. Compare with the continuous loop.

---

## Objective coverage

| Learning objective (chapter 15-11) | Problems |
|---|---|
| 1. ZOH equivalents and the z-plane | 1, 3 |
| 2. Discretizing controllers | 4, 6, 10 |
| 3. Discrete stability and steady-state error | 5, 7, 12 |
| 4. Phase cost and sample-rate choice | 2, 8 |
| 5. Implementation | 9, 11 |
