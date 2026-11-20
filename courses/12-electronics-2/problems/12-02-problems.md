# Problems 12-02 · Active Loads, Cascodes and Multistage Amplifiers

Chapter: [12-02](../chapters/12-02-active-loads-cascodes-multistage.md) · Worked solutions: [12-02 solutions](../solutions/12-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** square law with $g_m = 2I_D/V_{ov}$ and $r_o = 1/(\lambda I_D)$; $V_{TN} = \lvert V_{TP}\rvert$ = 0.5 V; body effect neglected unless stated; midband (no capacitances). "Gain" means the magnitude of the small-signal voltage gain.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 12-02.1 [A]

**Intrinsic gain.** A short-channel NMOS has λ = 0.2 V⁻¹ and runs at $V_{ov}$ = 0.15 V. Find its intrinsic gain.

### Problem 12-02.2 [A]

**An active load with unequal λ.** An NMOS common-source stage at 50 µA and $V_{ov}$ = 0.25 V has λ = 0.1 V⁻¹; its PMOS current-source load has λ = 0.15 V⁻¹. Find $g_m$, both output resistances and the gain.

### Problem 12-02.3 [A]

**Cascode output resistance.** Both devices of an NMOS cascode have $g_m$ = 2 mA/V and $r_o$ = 20 kΩ. Find the output resistance.

### Problem 12-02.4 [B]

**A five-transistor OTA.** The OTA has $I_{SS}$ = 100 µA, every device at $V_{ov}$ = 0.2 V and λ = 0.2 V⁻¹. Find $g_m$, $r_o$ and the differential gain (ratio and dB), and the short-circuit output current for $v_{id}$ = 2 mV.

### Problem 12-02.5 [B]

**The OTA's CMRR.** For the OTA of Problem 12-02.4, the tail is a single transistor with the same λ. Estimate the common-mode gain and CMRR. By how many decibels does a cascode tail that raises $R_{SS}$ twentyfold improve it?

### Problem 12-02.6 [B]

**Deriving the cascode's gain.** With an ideal current-source load, show that a cascode's gain is $g_{m1}r_{o1}(1 + g_{m2}r_{o2})$, and evaluate it for $g_m$ = 1 mA/V and $r_o$ = 50 kΩ.

### Problem 12-02.7 [B]

**Swing at 1.2 V.** A fully differential telescopic cascode and a two-stage amplifier both run from 1.2 V with every overdrive at 0.15 V. Find each one's output swing per side, and the telescopic stage's differential peak-to-peak output.

### Problem 12-02.8 [B]

**Loading between stages.** Stage 1 has $G_m$ = 1 mA/V and $R_{out}$ = 50 kΩ; it drives stage 2, whose input resistance is 50 kΩ, $G_m$ = 40 mA/V and output resistance 10 kΩ (unloaded). Find each stage's gain in the cascade, the total gain, and the total if stage 2's input resistance were infinite.

### Problem 12-02.9 [B]

**Referring offsets.** A three-stage amplifier has gains $A_1$ = 20 and $A_2$ = 50 and input offsets of 2 mV, 10 mV and 20 mV at the inputs of stages 1, 2 and 3. Find the input-referred offset if all three add, and if they are independent random variables with these standard deviations.

### Problem 12-02.10 [B]

**A level shifter.** An NMOS source follower with $k_n$ = 2 mA/V² carries 50 µA. Find its level shift, and the shift if body effect raises its threshold to 0.6 V.

### Problem 12-02.11 [C]

**Systematic offset.** A two-stage op-amp has a first stage with gain 50 and 100 µA in its mirror device M4. Its PMOS second stage M6 is four times as wide as M4 at the same length, so at equal $V_{SG}$ it carries 400 µA, but the second stage's current-source load sinks 450 µA. With $g_{m6}$ = 4 mA/V, find the shift of the first stage's output needed for balance, and the input-referred systematic offset.

### Problem 12-02.12 [C]

**Gain per volt of headroom.** Every device has $g_m$ = 1 mA/V, $r_o$ = 20 kΩ and $V_{ov}$ = 0.15 V. Find the gain of (a) a common-source stage with a simple current-source load, (b) a cascode with a simple current-source load, (c) a cascode with a cascode load (same output resistance), and the minimum headroom ($\sum V_{ov}$ between the rails) each needs. Which gives the most gain per volt?

### Problem 12-02.13 [B]

**Bipolar versions.** (a) A bipolar pair with a simple mirror load runs each side at 100 µA with β = 100. The mirror's diode side supplies both transistors' base currents. By what fraction does the copied current fall short, and what differential input does the pair need to balance the output? Compare with the estimate $2V_T/\beta$. (b) A bipolar cascode has both transistors at 100 µA, $r_o$ = 100 kΩ and β = 100. Find its output resistance, and compare with $\beta r_o$ and with the MOS-style $g_mr_o^2$.

### Problem 12-02.14 [B]

**A telescopic cascode.** Every device of a fully differential telescopic cascode has $g_m$ = 1 mA/V, $r_o$ = 50 kΩ and $V_{ov}$ = 0.15 V, from a 1.5 V supply. Find the differential gain (in V/V and dB), each output's swing range and the peak-to-peak differential swing.

### Problem 12-02.15 [B]

**An OTA's DC levels.** A five-transistor OTA (NMOS pair, PMOS mirror) runs from 1.8 V with $I_{SS}$ = 200 µA. The NMOS devices have $V_{TN}$ = 0.5 V and $V_{ov}$ = 0.2 V; the PMOS mirror has $\lvert V_{TP}\rvert$ = 0.5 V and $V_{ov}$ = 0.25 V; the tail needs 0.2 V. Find the output's DC level when the halves match, and the input common-mode range.

---

## Objective coverage

| Learning objective (chapter 12-02) | Problems |
|---|---|
| 1. Resistor and active loads | 1, 2 |
| 2. The five-transistor OTA | 4, 5, 13, 15 |
| 3. Cascode output resistance and gain | 3, 6, 12, 13 |
| 4. Telescopic gain and swing | 7, 14 |
| 5. Multistage gain, offset and DC coupling | 8, 9, 10, 11 |
