# Problems 12-03 · Frequency Response: Device Capacitances, Miller Effect, Poles and Zeros

Chapter: [12-03](../chapters/12-03-frequency-response-miller-poles-zeros.md) · Worked solutions: [12-03 solutions](../solutions/12-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** small-signal models with linear capacitances; $V_T$ = 25.852 mV; frequencies in hertz unless stated; "pole at $f$" means a factor $1/(1 + jf'/f)$. $R_L$ is the total resistance at the output node and $C_L$ its total capacitance to ground excluding $C_{gd}$.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 12-03.1 [A]

**Transition frequency.** A MOSFET has $g_m$ = 2 mA/V, $C_{gs}$ = 50 fF and $C_{gd}$ = 10 fF. Find $f_T$.

### Problem 12-03.2 [A]

**Miller capacitances.** A 5 fF capacitor bridges the input and output of an inverting amplifier with gain −40. Find the equivalent capacitances to ground at the input and at the output.

### Problem 12-03.3 [A]

**Bipolar capacitances from $f_T$.** A bipolar transistor at $I_C$ = 1 mA has $f_T$ = 500 MHz and $C_\mu$ = 0.5 pF. Find $g_m$, $C_\pi + C_\mu$ and $C_\pi$, and the forward transit time if $C_{je}$ = 2 pF.

### Problem 12-03.4 [B]

**How good is the dominant-pole estimate?** A transfer function has real poles at 10 MHz and 100 MHz and no zeros. Find $1/(2\pi b_1)$ and the exact −3 dB frequency.

### Problem 12-03.5 [B]

**A common-source stage.** $g_m$ = 2 mA/V, $C_{gs}$ = 50 fF, $C_{gd}$ = 10 fF, $C_L$ = 50 fF, $R_S$ = 5 kΩ and $R_L$ = 10 kΩ. Find the gain, $b_1$, the dominant-pole estimate, $b_2$, the exact poles, the zero and the exact −3 dB frequency.

### Problem 12-03.6 [B]

**A Miller resistance.** A 1 MΩ feedback resistor bridges an inverting amplifier with gain −99. Find its equivalent resistances at the input and at the output, and explain why shunt feedback lowers input resistance.

### Problem 12-03.7 [B]

**A common-gate stage.** $g_m$ = 5 mA/V, $C_{gs}$ = 100 fF, source resistance 200 Ω, $R_L$ = 2 kΩ, and $C_L + C_{gd}$ = 200 fF. Find the gain from the source, and the input and output poles.

### Problem 12-03.8 [B]

**A source follower.** Driven from an ideal source, a follower with $g_m$ = 1 mA/V and $C_{gs}$ = 72.67 fF drives $C_L$ = 100 fF (current-source bias, $r_o$ neglected). Find its pole and zero.

### Problem 12-03.9 [B]

**The cascode's Miller factor.** A common-source device with $g_{m1}$ = 2 mA/V, $C_{gs}$ = 50 fF and $C_{gd}$ = 10 fF is cascoded by a device with $g_{m2}$ = 1 mA/V, whose own load resistance is small compared with its $r_o$. Find the gain from M1's gate to its drain and the input capacitance. Without the cascode, the stage's gain would be −30: find the input capacitance then.

### Problem 12-03.10 [B]

**Gain–bandwidth.** A stage with $g_m$ = 4 mA/V drives a total of 1 pF at its output, which dominates its bandwidth. Find the gain–bandwidth product, and the load resistance and bandwidth for a gain of 10.

### Problem 12-03.11 [C]

**The right-half-plane zero's phase.** For Example 12-03.2's stage (zero at $g_m/(2\pi C_{gd})$ with $g_m$ = 1 mA/V, $C_{gd}$ = 6 fF), find the zero's frequency and the phase lag it adds at 1 GHz and at the zero. Compare with a left-half-plane zero at the same frequency.

### Problem 12-03.12 [C]

**Which node dominates?** For Example 12-03.2's stage, find the source resistance at which the Miller input time constant equals the output time constant $R_L(C_L + C_{gd})$. At that $R_S$, find $1/(2\pi b_1)$ and the exact −3 dB frequency.

---

## Objective coverage

| Learning objective (chapter 12-03) | Problems |
|---|---|
| 1. Device capacitances and $f_T$ | 1, 3 |
| 2. The Miller theorem | 2, 6, 9 |
| 3. The common-source stage's poles and zero | 4, 5, 11, 12 |
| 4. CG, CD and cascode | 7, 8, 9 |
| 5. Gain–bandwidth | 10, 12 |
