# Problems 12-04 · High-Frequency Analysis Methods

Chapter: [12-04](../chapters/12-04-high-frequency-analysis-methods.md) · Worked solutions: [12-04 solutions](../solutions/12-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** independent sources are zeroed when finding the resistance a capacitor sees; controlled sources stay. "OCTC" and "SCTC" are open- and short-circuit time constants; transistor models are 12-03's.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 12-04.1 [A]

**A two-section RC ladder.** A source drives 1 kΩ into node A (1 nF to ground), then 1 kΩ into node B (1 nF to ground); the output is node B. Find each capacitor's open-circuit resistance, the OCTC bandwidth estimate, the exact poles and the exact −3 dB frequency.

### Problem 12-04.2 [A]

**The bridging resistance.** A common-source stage has $R_S$ = 2 kΩ, $R_L$ = 10 kΩ and $g_m$ = 5 mA/V. Find the resistance seen by $C_{gd}$.

### Problem 12-04.3 [B]

**OCTC of a common-source stage.** $g_m$ = 2 mA/V, $C_{gs}$ = 50 fF, $C_{gd}$ = 10 fF, $C_L$ = 50 fF, $R_S$ = 5 kΩ, $R_L$ = 10 kΩ. Find the three time constants, their sum, the bandwidth estimate, and the largest contributor's share.

### Problem 12-04.4 [B]

**Its second-order coefficient.** For the stage of Problem 12-04.3, find $R_{gd}^{gs}$, $R_L^{gs}$ and $R_L^{gd}$, and $b_2$.

### Problem 12-04.5 [B]

**Two coupling capacitors.** An amplifier has a 600 Ω source, a 1 µF input coupling capacitor into a 10 kΩ input resistance, and a 10 µF output coupling capacitor between a 2 kΩ output resistance and an 8 kΩ load. Estimate its low-frequency corner by SCTC.

### Problem 12-04.6 [B]

**Sizing a bypass capacitor.** A 1 kΩ source resistor is bypassed in a stage with $g_m$ = 10 mA/V. What capacitance puts this capacitor's short-circuit corner at 20 Hz?

### Problem 12-04.7 [B]

**Pole splitting.** A two-stage amplifier has $R_1$ = 100 kΩ, $C_1$ = 0.1 pF, $g_{m2}$ = 2 mA/V, $R_2$ = 50 kΩ, $C_2$ = 2 pF and $C_c$ = 2 pF. Find $b_1$, $b_2$, the exact poles, the simple estimates of both, and the right-half-plane zero. What is worrying about the zero here?

### Problem 12-04.8 [B]

**A follower with a large load.** A follower with $g_m$ = 2 mA/V, $C_{gs}$ = 100 fF and $C_{gd}$ = 10 fF drives 2 pF from 20 kΩ. Find $\Sigma$, $Q$ and $f_0$. Will it peak?

### Problem 12-04.9 [C]

**A symmetry of zero-value time constants.** For the common-source stage, show that $R_{gd0}R_L^{gd} = R_{L0}R_{gd}^L$, and evaluate both sides for Example 12-04.1's values.

### Problem 12-04.10 [C]

**OCTC of a common-gate stage.** Apply OCTC to Example 12-03.4's common-gate stage with the 10 kΩ source ($g_m$ = 1 mA/V, $C_{gs}$ = 72.67 fF, $R_L$ = 20 kΩ, $C_L + C_{gd}$ = 106 fF), and compare with the exact 75.00 MHz.

### Problem 12-04.11 [C]

**Deriving the follower's response and its inductive output.** (a) For the source follower of §3.5 (source resistance $R_S$, $C_{gs}$ from gate to output, $C_{gd}$ from gate to ground, load $C_L$), write KCL at the gate and at the output and derive $V_o/V_s$, showing every cancellation. (b) Neglect $C_{gd}$, zero $V_s$, and find the impedance $Z_{out}$ seen by the load. Show that it equals $1/g_m$ in series with an inductance $L = (C_{gs}/g_m)(R_S - 1/g_m)$ shunted by a resistance $R_S - 1/g_m$. (c) Evaluate $L$ for Example 12-04.5's follower at $R_S$ = 30 kΩ and compare $1/(2\pi\sqrt{LC_L})$ with the follower's natural frequency with $C_{gd}$ neglected. (d) What happens at $R_S = 1/g_m$, and what does it say about peaking?

---

## Objective coverage

| Learning objective (chapter 12-04) | Problems |
|---|---|
| 1. Open-circuit time constants | 1, 2, 3, 10 |
| 2. Zero-value time constants and the second pole | 4, 9 |
| 3. Short-circuit time constants | 5, 6 |
| 4. Pole splitting | 7 |
| 5. Follower response and peaking | 8, 11 |
