# Problems 15-05 · Stability and the Routh–Hurwitz Criterion

Chapter: [15-05](../chapters/15-05-stability-routh-hurwitz.md) · Worked solutions: [15-05 solutions](../solutions/15-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Negative unity feedback unless stated. "Stable" means all closed-loop poles in the open left half-plane. Values marked illustrative are chosen for the exercise.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 15-05.1 [A]

**The quick test.** Without building a full array, decide what you can about the stability of: (a) $s^3 + 2s^2 + 5$; (b) $s^4 + 3s^3 - s^2 + 2s + 1$; (c) $s^2 + 3s + 2$; (d) $s^3 + s^2 + s + 2$.

### Problem 15-05.2 [A]

**Two cubics.** Build the Routh arrays of (a) $s^3 + 4s^2 + 5s + 2$ and (b) $s^3 + s^2 + 2s + 8$, and give the number of right-half-plane roots of each.

### Problem 15-05.3 [A]

**Which are BIBO stable?** (a) $1/(s + 1)$; (b) $1/s$; (c) $1/(s^2 + 4)$; (d) $(s - 1)/[(s + 2)(s + 3)]$; (e) $1/(s - 1)$. Explain each in one line.

### Problem 15-05.4 [B]

**Stabilizing an unstable plant.** A loop has $L(s) = \dfrac{K(s + 1)}{s(s - 1)(s + 6)}$. Find the range of $K$ for stability and the oscillation frequency at the boundary.

### Problem 15-05.5 [B]

**A row of zeros.** Use the Routh array to locate the roots of $s^5 + s^4 + 6s^3 + 6s^2 + 8s + 8$: how many are in the right half-plane, how many on the imaginary axis, and at what frequencies? Is the system BIBO stable?

### Problem 15-05.6 [B]

**A zero in the first column.** How many right-half-plane roots has $s^4 + 2s^3 + 4s^2 + 8s + 5$?

### Problem 15-05.7 [C]

**A five-stage ring oscillator.** Five identical inverting stages, each with gain $-A$ and a pole at $\omega_0$, form a loop. (a) Show that the loop gain at the oscillation boundary has phase −180° when each stage lags by 36°. (b) Find the minimum $A$ and the oscillation frequency in terms of $\omega_0$. (c) Confirm with the characteristic polynomial. (d) For $f_0$ = 1 GHz, what is the oscillation frequency?

### Problem 15-05.8 [B]

**How fast can proportional gain make it?** For $L = K/[s(s + 2)(s + 4)]$: (a) show that no $K$ puts every closed-loop pole left of $s = -1$; (b) find the largest guaranteed decay rate $\sigma$ (every pole left of $-\sigma$) and the $K$ that achieves it.

### Problem 15-05.9 [C]

**An LDO's hidden pole.** Problem 15-02.12's regulator has poles at $\omega_a$ = 2π × 10 kHz and $\omega_L$ = 10⁵ rad/s. The pass transistor's gate capacitance adds a third pole at $\omega_g$ = 2π × 1 MHz. (a) Find the largest stable DC loop gain $L_0$. (b) Find the boundary oscillation frequency. (c) The design has $L_0$ = 2500; what happens?

### Problem 15-05.10 [C]

**A fourth-order PLL.** Example 15-05.5's PLL ($\tau_z$ = 5 µs, $\tau_p$ = 0.455 µs) gets an extra RC post-filter with $\tau_3$ = 1 µs, so $L = K(1 + s\tau_z)/[s^2(1 + s\tau_p)(1 + s\tau_3)]$. (a) Find the range of $K$ for stability. (b) At $K = 9.09 \times 10^{10}$ s⁻², by what factor (and how many dB) can $K$ rise before the loop oscillates? (c) At what frequency would it oscillate?

### Problem 15-05.11 [C]

**Throttling against runaway.** A chip's linearized thermal model (15-01) is $RC\,\dot T = -(1 - G)T + RP$ with $R$ = 0.8 K/W, $C$ = 20 J/K and leakage loop gain $G$ = 1.2 (illustrative), so on its own it runs away. A throttling controller cuts power, $P = -K_cT_s$, from a sensor with lag $\tau_s\dot T_s = T - T_s$, $\tau_s$ = 0.1 s. (a) Find the characteristic polynomial. (b) Find the smallest $K_c$ that stabilizes it, and any other condition. (c) Interpret.

### Problem 15-05.12 [B]

**Two parameters.** For $s^3 + as^2 + 4s + K$, find the region of the $(a, K)$ plane where the polynomial is stable. Show that on the boundary $K = 4a$ the oscillation frequency is the same for every $a$, and find it.

### Problem 15-05.13 [B]

**Routh and time delay.** A loop has $L = Ke^{-sT}/s$ with $T$ = 1 s. (a) Replace the delay by the Padé approximation $(1 - sT/2)/(1 + sT/2)$ and find the stable range of $K$. (b) The exact limit (15-07) is $K < \pi/(2T)$. By how much does the approximation overestimate it?

### Problem 15-05.14 [A]

**Marginal stability is not stability.** The system $1/(s^2 + 4)$ is driven from rest by $u = \sin 2t$. Show that $y(t) = (\sin 2t - 2t\cos 2t)/8$, give $y$ at $t$ = 10 s and the envelope of the oscillation there.

---

## Objective coverage

| Learning objective (chapter 15-05) | Problems |
|---|---|
| 1. BIBO and internal stability from pole locations | 3, 14 |
| 2. Routh arrays and right-half-plane counts | 1, 2 |
| 3. Special cases and imaginary-axis roots | 5, 6 |
| 4. Stable ranges for gains and parameters | 4, 9, 10, 12, 13 |
| 5. Ring oscillators, regulators, PLLs, relative stability | 7, 8, 9, 10, 11 |
