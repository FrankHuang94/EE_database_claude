# Problems 13-07 · Transmission Lines: Time Domain

Chapter: [13-07](../chapters/13-07-transmission-lines-time-domain.md) · Worked solutions: [13-07 solutions](../solutions/13-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $c$ = 2.998 × 10⁸ m/s; lines are lossless; sources are steps at $t$ = 0 with the stated internal resistance; voltages are measured to the return conductor.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 13-07.1 [A]

**A stripline.** A stripline has $L'$ = 333.6 nH/m and $C'$ = 133.4 pF/m. Find $Z_0$, the velocity, the delay per millimetre, and the relative permittivity of its (homogeneous) dielectric.

### Problem 13-07.2 [A]

**Reflection coefficients.** Find $\Gamma_L$ on a 50 Ω line terminated in 0 Ω, an open circuit, 25 Ω, 75 Ω and 100 Ω.

### Problem 13-07.3 [A]

**Launch.** A 3.3 V driver with 25 Ω output resistance drives a 50 Ω line. Find the launched voltage step.

### Problem 13-07.4 [B]

**Both ends mismatched.** A 1 V step with 100 Ω source resistance drives a 50 Ω line ending in 25 Ω. Find $v^+$, $\Gamma_S$, $\Gamma_L$, the load voltage after the first, second and third arrivals, and the final value.

### Problem 13-07.5 [A]

**Size a series resistor.** A driver has 15 Ω output resistance and drives a 50 Ω line to a single receiver at its far end. What series resistor terminates the line? What voltages appear at the receiver and just after the resistor for a 1.8 V step, and for how long does the second one persist if the line's delay is 0.8 ns?

### Problem 13-07.6 [B]

**The price of parallel termination.** A 3.3 V output drives a 50 Ω line terminated by 50 Ω to ground. Find the DC power in the terminator when the line is high. A Thevenin termination of two 100 Ω resistors (to 3.3 V and to ground) is equivalent to 50 Ω to 1.65 V. Find its power when the line is high (driver ideal), and its standing power with the driver disconnected.

### Problem 13-07.7 [B]

**A capacitive receiver.** A matched source launches a 0.5 V step on a 50 Ω line that ends at a receiver with 5 pF input capacitance (and no other load). Find the time constant of the receiver voltage, its final value, and its 10–90% rise time.

### Problem 13-07.8 [B]

**Find the break.** A TDR on a cable with a velocity factor of 66% shows the reflection from an open circuit 4.2 ns after the launch. How far away is the break?

### Problem 13-07.9 [B]

**Critical length.** Using the guideline that a net needs transmission-line treatment when its one-way delay exceeds one sixth of the rise time, find the critical length on a stripline with $\varepsilon_r$ = 4 for rise times of 100 ps and 1 ns.

### Problem 13-07.10 [C]

**Extract L and C from TDR areas.** On a 50 Ω line, a TDR trace normalized to the incident step shows a positive bump of area 10 ps and later a negative dip of area −25 ps. Derive the area formulas for a series inductance and a shunt capacitance, and find both values.

### Problem 13-07.11 [C]

**RG-58 from its data sheet.** RG-58 is specified at 101 pF/m with a 66% velocity factor. Show that the d'Alembert waves satisfy the telegrapher's equations, and use $v = 1/\sqrt{L'C'}$ and $Z_0 = \sqrt{L'/C'}$ to find $L'$ and $Z_0$ from the data.

### Problem 13-07.12 [C]

**A 75 Ω video line.** A 1 V step with 25 Ω source resistance drives a 75 Ω line terminated in 150 Ω. Find $v^+$, $\Gamma_L$, $\Gamma_S$, the load voltage after each of the first four arrivals, and the final value.

### Problem 13-07.13 [A]

**Ringing frequency.** An open line driven by a near-zero-impedance source has a one-way delay of 1 ns. At what frequency does it ring?

### Problem 13-07.14 [B]

**Two lines in series.** A matched source launches 0.5 V onto a 50 Ω line, which joins a 75 Ω line terminated in 75 Ω. Find the transmission coefficient at the junction, the voltage reaching the load, and the reflected wave returning to the source.

### Problem 13-07.15 [C]

**Follow the current.** A 1 V step source with 10 Ω internal resistance drives a 50 Ω line of 1 ns delay terminated in 200 Ω. (a) Show that a current wave reflects with coefficient $-\Gamma$, and find the launched current. (b) Find the load current just after 1 ns and 3 ns, and the source current between 0 and 2 ns, between 2 and 4 ns, and just after 4 ns. (c) Find the final current. Why is the source current zero for a while?

---

## Objective coverage

| Learning objective (chapter 13-07) | Problems |
|---|---|
| 1. Telegrapher's equations, Z₀ and velocity | 1, 11 |
| 2. Launching and reflecting | 2, 3, 14, 15 |
| 3. Bounce diagrams | 4, 12, 13, 15 |
| 4. Reactive terminations | 7, 10 |
| 5. Terminations and critical length | 5, 6, 9 |
| 6. TDR | 8, 10 |
