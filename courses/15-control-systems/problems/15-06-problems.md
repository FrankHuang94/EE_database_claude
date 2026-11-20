# Problems 15-06 · Root Locus

Chapter: [15-06](../chapters/15-06-root-locus.md) · Worked solutions: [15-06 solutions](../solutions/15-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Loops are $1 + KG(s) = 0$ with $K \ge 0$ unless stated. Angles are in degrees, measured counterclockwise from the positive real axis.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 15-06.1 [A]

**Segments and asymptotes.** For $G(s) = (s + 3)/[s(s + 1)(s + 5)(s + 6)]$, find the real-axis segments of the locus, the asymptote angles and the centroid.

### Problem 15-06.2 [A]

**On the locus or not?** For $G(s) = 1/[s(s + 4)(s + 6)]$: (a) is $s = -2 + j2$ on the locus? (b) Find the imaginary-axis crossing and its gain.

### Problem 15-06.3 [A]

**A breakaway point.** Find the breakaway point and its gain for $G = 1/[(s + 1)(s + 3)]$, and describe the locus.

### Problem 15-06.4 [B]

**A full sketch.** Sketch the locus of $G = 1/[s(s + 1)(s + 5)]$: real-axis segments, asymptotes, breakaway point and its gain, and the imaginary-axis crossing and its gain.

### Problem 15-06.5 [B]

**A departure angle.** For $G = (s + 2)/[(s + 3)(s^2 + 2s + 2)]$, find the angle at which the locus leaves the pole $-1 + j1$.

### Problem 15-06.6 [B]

**Gain for a damping ratio.** For $G = 1/[s(s + 2)(s + 10)]$, find the point on the locus with $\zeta$ = 0.6, its gain and the third closed-loop pole. Is the dominant-pair approximation reasonable?

### Problem 15-06.7 [B]

**What an extra pole does.** $G_1 = 1/[s(s + 4)]$ is stable for every $K$. Add a pole at −10: $G_2 = 1/[s(s + 4)(s + 10)]$. Find the largest stable $K$ and the crossing frequency, and explain the change with the asymptotes.

### Problem 15-06.8 [B]

**The constant-sum rule.** For $G = 1/[s(s + 2)(s + 4)]$, find the gain at which the complex closed-loop poles have real part −0.5, and the third pole there. Compare with Example 15-05.6.

### Problem 15-06.9 [C]

**The circle.** For $G = (s + 6)/[s(s + 2)]$: (a) show that every point $s = -6 + \rho e^{j\phi}$ with $\rho = \sqrt{24}$ satisfies the angle condition; (b) find the smallest damping ratio of the complex closed-loop poles and the gain that gives it.

### Problem 15-06.10 [C]

**Positive feedback.** For $G = 1/[(s + 1)(s + 2)]$ with negative $K$ (positive feedback), state the angle condition, find the real-axis segments, and find the value of $\lvert K\rvert$ at which the loop becomes unstable.

### Problem 15-06.11 [C]

**A decompensated amplifier.** An op-amp has $A(s) = 10^4/[(1 + s/10^4)(1 + s/10^6)(1 + s/10^7)]$ (poles in rad/s). With a resistive feedback factor $\beta$, the loop gain is $A\beta$. Find the largest $\beta$ for stability, the corresponding smallest stable closed-loop gain $1/\beta$, and the oscillation frequency at the boundary. Relate the result to amplifiers specified as "stable in gains of 5 or more".

### Problem 15-06.12 [C]

**A locus in a time constant.** Example 15-05.5's PLL has characteristic polynomial $\tau_ps^3 + s^2 + K\tau_zs + K$ with $K = 9.09 \times 10^{10}$ s⁻² and $\tau_p$ = 0.455 µs. Treat $\tau_z$ as the parameter: write the polynomial as $D(s) + \tau_zN(s)$, and find the value of $\tau_z$ at which the loop becomes unstable, and the crossing frequency there.

### Problem 15-06.13 [B]

**An arrival angle.** $G = (s^2 + 2s + 5)/[s(s + 4)]$ has complex zeros at $-1 \pm j2$. At what angle does the locus arrive at $-1 + j2$?

### Problem 15-06.14 [B]

**Damping against accuracy.** For $G = 1/[(s + 1)(s + 3)]$ with proportional gain $K$, find the gain for $\zeta$ = 0.5 and the resulting steady-state error to a unit step.

---

## Objective coverage

| Learning objective (chapter 15-06) | Problems |
|---|---|
| 1. Angle and magnitude conditions | 2, 6, 9 |
| 2. The sketching rules | 1, 3, 4, 5, 13 |
| 3. Gain from a damping requirement | 6, 8, 14 |
| 4. Effects of added poles and zeros | 7, 9 |
| 5. PLLs, amplifiers and other parameters | 10, 11, 12 |
