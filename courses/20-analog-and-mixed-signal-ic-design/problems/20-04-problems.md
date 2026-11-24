# Problems 20-04 · Low-Dropout Regulators

Chapter: [20-04](../chapters/20-04-ldo-regulators.md) · Worked solutions: [20-04 solutions](../solutions/20-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Unless stated, "the design" is the chapter's running design: T130 PMOS pass device (μ = 100 cm²/V·s, $C_{ox}$ = 8.6 fF/µm², $n$ = 1.3, $\lvert V_{TH}\rvert$ = 0.45 V, $v_{sat}$ = 6 × 10⁶ cm/s, $V_A'$ = 8 V/µm, $L_{ch}$ = 0.15 µm, $W$ = 1.877 mm), $V_{out}$ = 1.2 V, $V_{REF}$ = 0.6 V (β = 0.5), $R_{div}$ = 1.2 MΩ, error amplifier $g_{ma}$ = 1 mS, $R_a$ = 100 kΩ, $C_a$ = 0.2 pF, gate buffer $g_{mb}$ = 2 mS, $C_L$ = 1 µF with 5 mΩ ESR, $V_{in}$ = 1.8 V, $I_Q$ = 120 µA, load from 100 µA to 100 mA. Phase margins come from the full loop gain of §3.4. Problems marked *(lab)* need `labs/20-04-lab/ldo.py` or an equivalent numerical tool.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 20-04.1 [A]

**Where the power goes.** An LDO delivers 1.0 V at 50 mA with a quiescent current of 30 µA. (a) Find its efficiency and the power dissipated in the pass device from a 1.2 V input and from a 3.3 V input. (b) A buck converter with 90% efficiency could make the same output from 3.3 V. How much input power would it draw, against the LDO's?

### Problem 20-04.2 [A]

**PMOS or NMOS?** An NMOS source-follower pass device needs $V_{GS}$ = 0.75 V at 100 mA. Its gate driver is powered from $V_{in}$ and needs 0.15 V of headroom. (a) For a 1.2 V output, what is the minimum input voltage, and the best-case efficiency there? (b) Compare with the design's PMOS (150 mV dropout). (c) Name two advantages that keep NMOS pass devices in use anyway.

### Problem 20-04.3 [B] *(lab)*

**Lower dropout.** Resize the pass device for 100 mV of dropout at 100 mA with $V_{in}$ = 1.3 V. Find the long-channel width, the velocity-saturation factor, the width, its ratio to the design's width, and the gate capacitance $\tfrac23WLC_{ox}$. What happens to the gate pole $g_{mb}/C_g$?

### Problem 20-04.4 [B] *(lab)*

**The middle of the load range.** At 10 mA, find the pass device's $V_{SG}$, $g_m/I_D$, $g_{mp}$, $r_{ds}$, $R_{out}$, the DC loop gain (also in dB), the closed-loop output impedance and the line regulation (gate tracking the supply). Check that they fall between Example 20-04.3's light- and full-load values.

### Problem 20-04.5 [C] *(lab)*

**Buying regulation.** The design must hold its output within 5 mV from 100 µA to 100 mA. (a) Using $\Delta V_{out} \approx \Delta V_{SG}/(A_{EA}\beta)$, find the required error-amplifier gain (and in dB). (b) The gain is raised by increasing $g_{ma}$ with $R_a$ and $C_a$ unchanged. Find the new crossover and phase margin at 100 µA and at 100 mA, and explain the change.

### Problem 20-04.6 [B] *(lab)*

**The minimum output capacitor.** Find the smallest $C_L$ (5 mΩ ESR) that gives 60° of phase margin at 100 mA, and the crossover there. Compare the crossover with the estimate $A_{EA}\beta g_{mp}/(2\pi C_L)$ and explain the difference.

### Problem 20-04.7 [C] *(lab)*

**The ESR window.** (a) With 1 µF and an ESR of 0.5 Ω, find the ESR zero, the crossover and the phase margin at 100 mA. Why did the crossover move so far? (b) The error amplifier has a parasitic pole at 30 MHz that the model of §3.4 omitted. Repeat at 100 mA with the pole included, for 5 mΩ and for 0.5 Ω. What does this say about the upper edge of 15-12's ESR window?

### Problem 20-04.8 [B] *(lab)*

**After a buck converter.** The LDO's input carries 20 mV of ripple at 2 MHz from a buck converter. At 100 mA, find the PSRR at 2 MHz and the output ripple for $k$ = 1 and $k$ = 0.

### Problem 20-04.9 [A]

**An accuracy budget.** The design's reference is accurate to ±0.5%, the divider ratio to ±0.2%, and the error amplifier's offset is at most ±2 mV. Add the load-regulation error of 13.41 mV (100 µA to 100 mA). (a) Find each contribution at the output and the worst-case total in mV and in %. (b) Combine the three random terms in root-sum-square, add the systematic load-regulation term, and compare.

### Problem 20-04.10 [B] *(lab)*

**A small load step.** At the 100 mA operating point, the load steps up by 10 mA. (a) Estimate the dip from §3.6 and the final deviation from the closed-loop output impedance. (b) Simulate the linear step response and find the peak deviation and its time. Why is there essentially no overshoot?

### Problem 20-04.11 [C]

**A capacitor-less LDO.** The design's pass device is used on chip with $C_o$ = 200 pF and Miller compensation. (a) At a 1 mA minimum load, find $g_{mp}$, the second pole $g_{mp}/(2\pi C_o)$ and the largest unity-gain frequency that keeps 60° of phase margin (two-pole model). (b) A 20 mA load step must dip by no more than 60 mV. Find the required response time and the equivalent bandwidth $1/(2\pi t_{resp})$. (c) What do you conclude, and what do designers do about it?

### Problem 20-04.12 [B]

**A digital LDO.** A digital LDO has unit switches of 0.5 mA each, a 100 MHz clock and 100 nF of output capacitance. (a) Estimate the limit-cycle ripple. (b) How many switches are needed for 100 mA? (c) With one switch added per clock, how long does it take to follow a 10 mA load step, and roughly how far does the output dip meanwhile?

### Problem 20-04.13 [B]

**A wearable's always-on domain.** A microcontroller domain at 0.9 V draws 5 µA asleep and 3 mA active, active 1% of the time, from a 1.8 V rail. Option 1 is an LDO with $I_Q$ = 1 µA. Option 2 is a buck converter with 85% efficiency when active and 60% asleep. (a) Find each option's input power asleep, active and on average. (b) By what factor does the LDO raise the average power, and what is its efficiency when active and asleep?

### Problem 20-04.14 [C] *(lab)*

**A slower error amplifier.** To save current, the error amplifier's output capacitance grows to 2 pF (so $p_a$ falls tenfold). (a) Find the crossover and phase margin at 100 µA and 100 mA. (b) Find the PSRR at 100 mA ($k$ = 1) at 100 kHz and 1 MHz, and compare with the original design. (c) Explain both results with §3.4 and §3.5.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Architecture, pass devices, efficiency and headroom | 1, 2, 13 |
| 2. Size a PMOS pass device for dropout | 3 |
| 3. Load and line regulation, DC accuracy | 4, 5, 9 |
| 4. Stability across load and output capacitor | 5, 6, 7, 14 |
| 5. Supply rejection against frequency | 8, 14 |
| 6. Load transients, capacitor-less and digital LDOs | 10, 11, 12 |
