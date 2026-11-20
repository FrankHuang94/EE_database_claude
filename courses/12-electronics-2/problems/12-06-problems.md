# Problems 12-06 · Stability and Frequency Compensation

Chapter: [12-06](../chapters/12-06-stability-and-compensation.md) · Worked solutions: [12-06 solutions](../solutions/12-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $T(s)$ is the loop gain, positive at DC for negative feedback; phases are unwrapped from 0° at DC; PM $= 180^\circ + \angle T(j\omega_c)$ at the crossover $\lvert T \rvert$ = 1; GM $= -20\log\lvert T(j\omega_{180})\rvert$. "Pole at $f$" means a factor $1/(1 + jf'/f)$. Two-stage amplifiers follow the model of chapter §3.5 and are used at unity gain (β = 1) unless stated.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 12-06.1 [A]

**Reading the margins.** A loop gain's magnitude crosses unity at 5 MHz, where its phase is −125°; its phase reaches −180° at 20 MHz, where its magnitude is 0.2. Find the phase margin and the gain margin.

### Problem 12-06.2 [A]

**The single-pole loop.** A loop gain has $T_0$ = 10⁴ and one pole at 100 Hz. Find the crossover frequency, the phase margin and the closed-loop pole frequency.

### Problem 12-06.3 [A]

**Second pole at $f_u$.** A two-pole loop (dominant pole far below crossover) has its second pole exactly at $f_u = T_0f_1$. Find its phase margin, closed-loop $Q$ and step overshoot.

### Problem 12-06.4 [B]

**What 45° means.** For a two-pole loop, find the ratio $f_2/f_u$ that gives a 45° phase margin, and the resulting $Q$, damping ratio and step overshoot.

### Problem 12-06.5 [B]

**The minimum stable gain.** For Example 12-06.3's uncompensated amplifier ($A_0$ = 10⁴, poles at 1, 10 and 100 MHz), find the largest feedback factor β for which the loop is stable, and the corresponding minimum closed-loop gain in V/V and decibels.

### Problem 12-06.6 [B]

**Dominant-pole compensation.** An amplifier has $A_0$ = 10⁵ and poles at 2 MHz and 20 MHz. A dominant pole is added for unity-gain use. (a) A designer places it so that $A_0f_d$ equals 2 MHz: find $f_d$ and the resulting phase margin. (b) Find the $f_d$ that gives exactly 45°, and the crossover.

### Problem 12-06.7 [B]

**Miller design rules.** A two-stage amplifier has $g_{m1}$ = 0.5 mA/V, $g_{m2}$ = 5 mA/V and $C_L$ = 2 pF. Apply the rules of §3.5: find $C_c$, the GBW, $p_2$, the right-half-plane zero and the estimated phase margin.

### Problem 12-06.8 [B]

**When $g_{m2}$ is too small.** In Problem 12-06.7, suppose the second stage is starved so that $g_{m2} = g_{m1}$, while $p_2$ is still placed at 2.2 times $\omega_u$ (by a smaller load). Estimate the phase margin, and say which term caused the loss.

### Problem 12-06.9 [B]

**Nulling resistors.** For Problem 12-06.7's amplifier with $C_c$ = 0.44 pF and $C_1$ = 0.1 pF, find the nulling resistor that removes the zero, the one that cancels $p_2$, and the third pole the latter creates.

### Problem 12-06.10 [B]

**A heavier load.** Example 12-06.5's amplifier ($C_c$ = 1.1 pF) now drives 10 pF instead of 5 pF. Estimate the phase margin with §3.5's formula, and compare with the exact value from the full circuit (Example 12-06.5's $A(s)$ with the new $C_L$), 45.91°, at a crossover of 110.8 MHz.

### Problem 12-06.11 [C]

**A better $C_c$ estimate.** For Example 12-06.5's amplifier, use the improved $p_2 = g_{m2}C_c/[C_1C_L + C_c(C_1 + C_L)]$, with the crossover taken as $g_{m1}/C_c$ and the zero as $g_{m2}/C_c$, to solve for the $C_c$ that gives an estimated 60°. The exact solution of the circuit (Example 12-06.5's $A(s)$) at that $C_c$ gives a phase margin of 62.20°; the exact $C_c$ for 60° is 1.180 pF. Explain the difference.

### Problem 12-06.12 [C]

**Phase margin from a scope.** A unity-gain buffer shows 20% overshoot on a small step. Assuming a two-pole loop, estimate its damping ratio, $Q$, the ratio $f_2/f_u$ and its phase margin.

### Problem 12-06.13 [B]

**Move the pole instead.** For Problem 12-06.6's amplifier ($A_0$ = 10⁵, poles at 2 MHz and 20 MHz), lower the 2 MHz pole to a new frequency $f_1'$ instead of adding a pole. Find the $f_1'$ that gives a 45° phase margin at unity gain and the resulting crossover, and compare the crossover with Problem 12-06.6(b)'s. Explain the ratio.

---

## Objective coverage

| Learning objective (chapter 12-06) | Problems |
|---|---|
| 1. Stability, phase margin and gain margin | 1, 2, 5 |
| 2. Phase margin and the closed-loop response | 3, 4, 12 |
| 3. Dominant-pole compensation, and moving an existing pole | 5, 6, 13 |
| 4. Miller compensation of a two-stage amplifier | 7, 8, 10, 11 |
| 5. The right-half-plane zero and the nulling resistor | 8, 9 |
