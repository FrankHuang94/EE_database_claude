# Problems 15-08 · PID Control

Chapter: [15-08](../chapters/15-08-pid-control.md) · Worked solutions: [15-08 solutions](../solutions/15-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Standard form $K_p(1 + 1/(T_is) + T_ds)$ unless stated; a derivative filter $N$ = 10 where a derivative is simulated. Unity feedback. Values marked illustrative are chosen for the exercise.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 15-08.1 [A]

**Forms and zeros.** A PID has $K_p$ = 2, $T_i$ = 0.5 s and $T_d$ = 0.1 s. Find $K_i$, $K_d$ and the controller's zeros.

### Problem 15-08.2 [A]

**Why add integral action?** Example 15-08.1's thermal plant ($K$ = 0.5 K/W) is controlled by $K_p$ = 14 W/K alone. Find the steady-state error to a setpoint step, as a fraction of the step.

### Problem 15-08.3 [A]

**The price of a PI zero.** A PI zero placed a factor $f$ below the crossover frequency subtracts $\arctan(1/f)$ of phase at crossover. Evaluate it for $f$ = 3, 5 and 10.

### Problem 15-08.4 [B]

**A PI speed loop by pole placement.** For the motor $P = 50/(0.025s + 1)$ rad/s per V, design a PI controller for $\omega_n$ = 100 rad/s and $\zeta$ = 0.7. Find $K_p$, $K_i$, the closed-loop zero, the overshoot and the 2% settling time.

### Problem 15-08.5 [B]

**SIMC tuning.** A process is modelled as $2e^{-s}/(10s + 1)$ (time in seconds). Apply the SIMC PI rule with $\tau_c = \theta$, and find the phase margin, gain margin and delay margin of the resulting loop.

### Problem 15-08.6 [B]

**Ziegler–Nichols on an integrating plant.** For $P = 1/[s(s + 1)(s + 2)]$: find $K_u$ and $P_u$ with Routh, the Ziegler–Nichols PID settings, the phase margin and the setpoint overshoot.

### Problem 15-08.7 [A]

**Noise gain.** For Example 15-08.3's Ziegler–Nichols PID ($K_p$ = 4.8), find the controller's high-frequency gain (ratio and dB) with $N$ = 10, and with $N$ = 5.

### Problem 15-08.8 [C]

**Choosing the tracking time.** Repeat Example 15-08.4's back-calculation run with $T_t$ = 1.4 s and with $T_t$ = 5.6 s. Report the overshoot and settling time, and explain the trend.

### Problem 15-08.9 [C]

**Fixing the slow disturbance response.** For Example 15-08.2's plant $1/[(s + 1)(0.2s + 1)]$, choose a parallel-form PID ($K_p$, $K_i$, $K_d$, ideal derivative) that places all three closed-loop poles at −5. Compare the peak and the value at 3 s of the response to a unit input disturbance with the cancelling design, and give the setpoint overshoot.

### Problem 15-08.10 [B]

**How much setpoint weighting?** For Example 15-08.5's Ziegler–Nichols loop with the derivative on the measurement ($c = 0$), find the proportional weight $b$ that gives exactly 10% setpoint overshoot.

### Problem 15-08.11 [B]

**A slower firmware loop.** Repeat Example 15-08.6 with a 0.3 s delay. Find $\omega_c$, $K_p$ and $K_i$ for a 60° phase margin, and compare the speed with the 0.1 s design.

### Problem 15-08.12 [A]

**Relay auto-tuning.** A relay of amplitude $d$ = 1 in place of the controller makes $1/(s + 1)^3$ settle into a limit cycle; a simulation (or a measurement) shows output amplitude $a$ = 0.163 and period 3.68 s. Using the describing-function estimate $K_u \approx 4d/(\pi a)$ (§3.6), estimate $K_u$ and $P_u$, and compare with the exact values from Routh.

---

## Objective coverage

| Learning objective (chapter 15-08) | Problems |
|---|---|
| 1. The three actions and the controller forms | 1, 2, 3 |
| 2. Pole placement and loop shaping | 4, 9, 11 |
| 3. Tuning rules and their trades | 5, 6, 12 |
| 4. Windup and anti-windup | 8 |
| 5. Derivative filtering and setpoint weighting | 7, 10 |
