# Problems 15-04 · Feedback Properties and Steady-State Error

Chapter: [15-04](../chapters/15-04-feedback-and-steady-state-error.md) · Worked solutions: [15-04 solutions](../solutions/15-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Unity feedback unless stated. "Unit ramp" means $r = t$ and "unit parabola" means $r = t^2/2$. Check closed-loop stability before applying the final-value theorem. Values marked illustrative are chosen for the exercise.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 15-04.1 [A]

**Sensitivity of an amplifier.** A forward gain $G$ = 2000 has feedback $H$ = 0.05. Find the closed-loop gain and $S_G^T$. If $G$ halves, find the exact fractional change of the closed-loop gain.

### Problem 15-04.2 [A]

**Type and error constants.** For each unity-feedback loop, confirm stability, give the type, the error constants and the steady-state errors to a unit step, ramp and parabola: (a) $L = 50/[(s + 2)(s + 5)]$; (b) $L = 10/[s(s + 4)]$; (c) $L = 4(s + 1)/[s^2(s + 5)]$.

### Problem 15-04.3 [A]

**Which signals does feedback reject?** A type-0 loop has $L(0)$ = 99. Find the fraction of (a) a constant output disturbance and (b) a constant sensor offset that remains in the output in steady state. Explain the difference.

### Problem 15-04.4 [B]

**Accuracy against damping.** A plant $P = 1/[(s + 1)(s + 3)]$ is under proportional control $C = K$. (a) Find the smallest $K$ for a step error of at most 2%. (b) Find $\zeta$ and the overshoot at that $K$. (c) What does this suggest about using proportional gain alone for accuracy?

### Problem 15-04.5 [B]

**Ramp tracking.** A positioning loop has $L = K/[s(s + 10)]$. Find $K$ for a unit-ramp error of 0.05, and the resulting damping ratio and overshoot.

### Problem 15-04.6 [B]

**Holding temperature under a workload step.** An illustrative thermal plant has $P(s) = 0.5/(10s + 1)$ K/W, from heat removed or added by an actuator (a thermoelectric cooler) to die temperature. A workload step of 20 W enters at the plant input. (a) Find the open-loop temperature rise. (b) With proportional control $C$ = 20 W/K, find the steady rise. (c) What controller makes it zero?

### Problem 15-04.7 [B]

**A sensor with gain.** A plant $G = 10/(s + 1)$ is measured by a sensor of gain $H$ = 0.5 V per unit, and the reference $r$ is a voltage. The desired output is $r/H$. For a 1 V reference step, find the closed-loop transfer function, the steady output, the desired output and the steady-state error.

### Problem 15-04.8 [B]

**Tracking a satellite.** An antenna positioner is a type-1 loop with $K_v$ = 20 s⁻¹. It tracks a satellite that moves across the sky at 0.5°/s. Find the steady pointing lag. What would a type-2 loop give?

### Problem 15-04.9 [B]

**Gain accuracy at 100 kHz.** An op-amp with $A_0 = 10^5$ and a 100 Hz open-loop pole (a 10 MHz gain-bandwidth product) is used at a closed-loop gain of 2 ($\beta$ = 0.5). At 100 kHz, find $\lvert L\rvert$, $\lvert S\rvert$, the magnitude error and the phase of the closed-loop gain.

### Problem 15-04.10 [C]

**Rejecting mains hum.** A 60 Hz sinusoidal disturbance of unit amplitude appears at the output of a loop with $P = 1/(s + 10)$. (a) With $C$ = 100, find the steady amplitude of the disturbance at the output. (b) Add a resonant term, $C = 100 + K_rs/(s^2 + \omega_0^2)$ with $\omega_0 = 2\pi \cdot 60$ rad/s and $K_r = 3 \times 10^4$ s⁻¹. Show the closed loop is stable, give its slow poles, and find the largest output amplitude during the cycle that starts at 0.5 s. (c) Explain with the internal model principle.

### Problem 15-04.11 [C]

**A PLL's frequency step.** For Example 15-04.5's PLL, the reference frequency steps by 100 kHz. Find the steady phase error, and simulate the peak phase error and its time. Why can the peak error matter even when the steady error is zero?

### Problem 15-04.12 [C]

**Faster recovery from a load step.** In Example 15-04.3's PI speed loop, keep $K_P$ = 0.2 V·s/rad and choose $K_I$ so that the slow closed-loop pole is at −50 s⁻¹. Find $K_I$, the other pole, the new $K_v$, and the peak speed dip under a 0.01 N·m load step and its time.

### Problem 15-04.13 [B]

**A regulator that runs hot.** Problem 15-02.12's LDO has DC loop gain $L_0 = A_0g_mR_L\beta$ with $g_m$ = 0.5 A/V, $R_L$ = 10 Ω and $\beta$ = 0.5. Its error amplifier's DC gain falls from 1000 at room temperature to 300 when hot. Find the closed-loop output resistance and the output change for a 100 mA load step in each case.

### Problem 15-04.14 [B]

**A miscalibrated sensor.** A unity-feedback loop's sensor actually has gain $H$ = 0.98. (a) With integral control, find the steady output for a unit reference. (b) With a proportional forward gain of 100 instead, find the steady output. (c) Why does more loop gain not remove the sensor error?

---

## Objective coverage

| Learning objective (chapter 15-04) | Problems |
|---|---|
| 1. Sensitivity to the plant and to the sensor | 1, 13, 14 |
| 2. Disturbances and noise, at DC and across frequency | 3, 6, 9, 10 |
| 3. Type, error constants and steady-state errors | 2, 4, 5, 7, 8 |
| 4. Integrator location and integral action | 6, 10, 12 |
| 5. Op-amps, motors and PLLs | 9, 11, 12 |
