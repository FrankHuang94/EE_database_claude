# Problems 10-04 · Small-Signal Models

Chapter: [10-04](../chapters/10-04-small-signal-models.md) · Worked solutions: [10-04 solutions](../solutions/10-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $V_T$ = 25.852 mV; square-law MOSFET with $g_m = \sqrt{2k_nI_D}$ and $r_o = 1/(\lambda I_D)$; BJT with $g_m = I_C/V_T$, $r_\pi = \beta/g_m$, $r_e = \alpha/g_m$, $r_o = V_A/I_C$. Coupling and bypass capacitors are short circuits at signal frequencies. $r_o$ is ignored unless a value of $V_A$ or λ is given.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 10-04.1 [A]

**BJT parameters.** A BJT has $I_C$ = 0.2 mA, β = 150 and $V_A$ = 75 V. Find $g_m$, $r_\pi$, $r_e$, $r_o$ and the intrinsic gain.

### Problem 10-04.2 [A]

**MOSFET parameters and how they scale.** A MOSFET has $k_n$ = 2 mA/V² and λ = 0.1 V⁻¹ and carries $I_D$ = 0.25 mA. (a) Find $V_{ov}$, $g_m$, $r_o$ and $g_mr_o$. (b) The current is doubled at the same size: find $V_{ov}$, $g_m$, $r_o$ and $g_mr_o$. (c) The current is doubled by doubling $W$ at the original overdrive: find $g_m$, $r_o$ and $g_mr_o$. Which knob raises $g_m$ more efficiently?

### Problem 10-04.3 [A]

**Building the small-signal circuit.** A common-source amplifier has $V_{DD}$, a gate divider $R_1$–$R_2$, a source resistor $R_S$ bypassed by $C_S$, a drain resistor $R_D$, an input coupling capacitor $C_1$ from the source $v_{sig}$ (with resistance $R_{sig}$) to the gate, and an output coupling capacitor $C_2$ to a load $R_L$. Describe what happens to each element in the small-signal circuit, and write the voltage gain $v_o/v_{sig}$ in terms of $g_m$ and the resistors (ignore $r_o$).

### Problem 10-04.4 [B]

**Hybrid-π equals T.** For a BJT with β = 80 at $I_C$ = 0.5 mA: (a) find $g_m$, $r_\pi$ and $r_e$; (b) show algebraically that $r_\pi = (\beta + 1)r_e$ and confirm it numerically.

### Problem 10-04.5 [B]

**A loaded common-emitter stage.** A BJT with β = 120 and $V_A$ = 60 V is biased at $I_C$ = 2 mA, with a base bias network whose Thévenin resistance is $R_B$ = 20 kΩ, $R_C$ = 3 kΩ, the emitter bypassed, and a load $R_L$ = 6 kΩ coupled to the collector. The source has $R_{sig}$ = 1 kΩ. Find (a) $g_m$, $r_\pi$ and the input resistance $R_{in} = R_B \parallel r_\pi$; (b) the fraction of $v_{sig}$ that reaches the base; (c) $r_o$ and the total load at the collector; (d) the gain from base to output and the overall gain $v_o/v_{sig}$.

### Problem 10-04.6 [B]

**Degenerated common source.** A MOSFET with $k_n$ = 5 mA/V² carries $I_D$ = 0.4 mA with $R_D$ = 5 kΩ. Find $g_m$ and $V_{ov}$, the gain with the source grounded for signals, and the gain with an unbypassed $R_S$ = 500 Ω.

### Problem 10-04.7 [B]

**Distortion budget.** (a) A BJT common-emitter stage with a gain of 100 must keep second-harmonic distortion at or below 2%. Find the largest input amplitude and the corresponding output amplitude. (b) Repeat for a MOSFET stage at $V_{ov}$ = 0.15 V with a gain of 20.

### Problem 10-04.8 [B]

**The body effect in a follower.** A MOSFET with $g_m$ = 1.5 mS has γ = 0.5 V$^{1/2}$, $2\phi_F$ = 0.8 V and $V_{SB}$ = 0.5 V. (a) Find χ and $g_{mb}$. (b) It drives $R_S$ = 10 kΩ from its source, with the drain at a fixed supply and the input at the gate. Using the small-signal circuit with $v_{bs} = -v_s$ (the body is grounded), show that $v_s/v_g = g_mR_S/[1 + (g_m + g_{mb})R_S]$, and evaluate it with and without the body effect.

### Problem 10-04.9 [B]

**Paying for transconductance.** A design needs $g_m$ = 2 mS. Find the bias current for (a) a BJT; (b) a MOSFET at $V_{ov}$ = 0.25 V, and the $k_n$ it needs; (c) a MOSFET in weak inversion with $n$ = 1.4.

### Problem 10-04.10 [C]

**Third-harmonic distortion.** (a) From the cubic term of the exponential series, show that a BJT's third-harmonic distortion is $\text{HD}_3 = (\hat v/V_T)^2/24$ to first order. (b) Evaluate $\text{HD}_2$ and $\text{HD}_3$ for $\hat v$ = 5 mV. (c) Why does a square-law MOSFET have no third harmonic at all, and why does a real one have some?

### Problem 10-04.11 [B]

**Diode-connected transistors.** (a) A MOSFET with its gate tied to its drain has $g_m$ = 1 mS and $r_o$ = 40 kΩ. Find the small-signal resistance between drain and source. (b) A BJT with its base tied to its collector carries 1 mA with β = 100 ($r_o$ ignored). Find its small-signal resistance, and show it equals $r_e$.

### Problem 10-04.12 [C]

**Where small-signal fails.** The common-emitter stage of Example 10-04.1 ($I_C$ = 1 mA, $R_C$ = 5 kΩ, $r_o$ ignored) receives a slow +5 mV step at the base, and separately a −5 mV step. (a) Using the exact exponential, find the change in collector voltage for each. (b) Compare with the small-signal prediction, and give the error of each as a percentage of the prediction. (c) Which way does a large sine output distort?

### Problem 10-04.13 [C]

**Choosing the overdrive.** A MOSFET common-source stage runs at $I_D$ = 100 µA with λ = 0.1 V⁻¹. It needs (i) intrinsic gain of at least 50, (ii) $\text{HD}_2$ at most 1% for a 2 mV input, and (iii) $g_m$ of at least 1 mS. (a) Turn each requirement into a bound on $V_{ov}$. (b) Choose the most linear overdrive that meets all three, then find $k_n$, the intrinsic gain and $\text{HD}_2$, and the margin on each requirement. (c) Why should the lowest bound found in (a) be treated with suspicion?

---

## Objective coverage

| Learning objective (chapter 10-04) | Problems |
|---|---|
| 1. Linearization and parameters as derivatives | 3, 10, 12 |
| 2. Device parameters, $g_m/I$ and intrinsic gain | 1, 2, 4, 9 |
| 3. Hybrid-π and T models | 4, 8, 11 |
| 4. Amplitude limits and distortion | 7, 10, 12, 13 |
| 5. Small-signal analysis procedure | 3, 5, 6, 8 |
| 6. $g_m/I_D$ and weak inversion | 9, 13 |
