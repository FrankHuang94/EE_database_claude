# Problems 10-06 · MOS Single-Stage Amplifiers

Chapter: [10-06](../chapters/10-06-mos-single-stage-amplifiers.md) · Worked solutions: [10-06 solutions](../solutions/10-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** square-law NMOS, $g_m = \sqrt{2k_nI_D} = 2I_D/V_{ov}$, $r_o = 1/(\lambda I_D)$, $g_{mb} = \chi g_m$ with the body at ground unless stated; capacitors are short circuits at signal frequencies; $r_o$ is ignored unless a value of $r_o$ or λ is given.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 10-06.1 [A]

**Name the stage.** For each, state the configuration and whether it inverts: (a) input at the gate, output at the source, drain at $V_{DD}$; (b) input at the source, output at the drain, gate at a DC bias; (c) input at the gate, output at the drain, source through a bypassed resistor to ground; (d) the same as (c) with the bypass capacitor removed.

### Problem 10-06.2 [A]

**A CS stage.** $k_n$ = 2 mA/V², $I_D$ = 0.2 mA, λ = 0.1 V⁻¹, $R_D$ = 10 kΩ, source grounded. Find $V_{ov}$, $g_m$, $r_o$ and the gain. Confirm that $g_mR_D = 2V_{RD}/V_{ov}$.

### Problem 10-06.3 [A]

**A follower.** A source follower biased by an ideal current source has $g_m$ = 3 mS, χ = 0.15 and $r_o$ = 30 kΩ. Find its unloaded gain and its output resistance.

### Problem 10-06.4 [B]

**Designing with degeneration.** A CS stage with $R_D$ = 8 kΩ and $g_m$ = 2 mS needs a gain of −4. (a) Find $R_S$. (b) A process shift lowers $g_m$ by 20%. Find the new gain and its percentage change. (c) Compare with an undegenerated stage of gain $-g_mR_D$ under the same shift.

### Problem 10-06.5 [B]

**Output resistance with the body effect.** A degenerated stage has $g_m$ = 1 mS, $g_{mb}$ = 0.2 mS, $r_o$ = 100 kΩ and $R_S$ = 2 kΩ. Using a test source, find the output resistance looking into the drain, with and without the body effect.

### Problem 10-06.6 [B]

**A common-gate current buffer.** A sensor behaves as a signal current source in parallel with 1 MΩ. It feeds the source of a CG stage with $g_m$ = 1 mS, χ = 0.2 and $R_D$ = 20 kΩ. (a) Find the CG input resistance. (b) What fraction of the sensor current enters the stage? (c) Find the output voltage per microampere of sensor current. (d) Compare with connecting the sensor directly across a 20 kΩ resistor.

### Problem 10-06.7 [B]

**Active load against resistor load.** A CS transistor with $g_m$ = 1 mS and $r_{on}$ = 50 kΩ at 100 µA is loaded either by a PMOS current source with $r_{op}$ = 40 kΩ or by a 10 kΩ resistor. Find both gains, and the DC voltage each load consumes if the PMOS needs only 0.2 V across it to stay saturated.

### Problem 10-06.8 [B]

**CG input resistance depends on the load.** For $g_m$ = 2 mS, $g_{mb}$ = 0.4 mS and $r_o$ = 40 kΩ, find the CG input resistance for drain loads of 0, 40 kΩ and 400 kΩ. What happens with an ideal current-source load?

### Problem 10-06.9 [C]

**Degeneration and distortion.** (a) For a square-law CS stage with source degeneration, write $v_{gs}$ and $i_d$ to second order in the input and show that $\text{HD}_2 = \hat v/[4V_{ov}(1 + g_mR_S)^2]$ for an input amplitude $\hat v$. (b) For $V_{ov}$ = 0.5 V and $\hat v$ = 50 mV, evaluate $\text{HD}_2$ with $g_mR_S$ = 0 and 1. (c) With $g_mR_S$ = 1, the input is doubled to restore the output amplitude. Find $\text{HD}_2$. (d) The exact values, from solving the large-signal equation over a cycle, are 0.626% and 1.255% for (b) and (c). Why are they slightly above the formula?

### Problem 10-06.10 [C]

**A cascode with the body effect.** Two transistors, each with $g_m$ = 2 mS and $r_o$ = 40 kΩ, form a cascode; the upper one has $g_{mb}$ = 0.4 mS. (a) Find the output resistance. (b) Find the gain with an ideal current-source load. Compare with Example 10-06.7.

### Problem 10-06.11 [B]

**Gain at 0.9 V.** A CS stage on a 0.9 V supply biases its output at 0.45 V with $V_{ov}$ = 0.15 V. (a) Find the resistor-load gain. (b) What overdrive would give a gain of 10? (c) Is the square-law estimate trustworthy there?

### Problem 10-06.12 [C]

**Driving a 50 Ω cable.** A CS stage ($A_{vo}$ = −10, $R_{out}$ = 2.5 kΩ) must drive a 50 Ω cable termination through a source follower with $g_m$ = 20 mS and χ = 0.2, biased by an ideal current source ($r_o$ ignored). (a) Find the follower's $R_{eq}$, gain into 50 Ω and output resistance. (b) Find the overall gain. (c) What CS gain magnitude would give an overall gain of −10?

---

## Objective coverage

| Learning objective (chapter 10-06) | Problems |
|---|---|
| 1. Identify configurations and their roles | 1, 6, 12 |
| 2. Gain, $R_{in}$, $R_{out}$ with $r_o$ and body effect | 2, 3, 5, 6, 8 |
| 3. Degeneration: $G_m$, $R_{out}$ and linearity | 4, 5, 9, 10 |
| 4. Gain, headroom and intrinsic limits | 2, 7, 11 |
| 5. Combining stages | 6, 12 |
