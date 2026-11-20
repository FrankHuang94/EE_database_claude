# Problems 15-12 · Applications: PLLs, Voltage Regulators and Thermal Management

Chapter: [15-12](../chapters/15-12-control-applications-pll-regulators-thermal.md) · Worked solutions: [15-12 solutions](../solutions/15-12-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** PLLs use the phase-domain model of §3.1 with $L = K(1 + s\tau_z)/[s^2(1 + s\tau_p)]$ and the maximum-margin design of §3.2. LDOs use the loop of §3.3 with Example 15-12.6's values unless stated. Thermal problems use Example 15-12.7's two-node model. All component values are illustrative.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 15-12.1 [A]

**Loop gain of a PLL.** A PLL has $I_{cp}$ = 50 µA, $K_v$ = 2π × 500 MHz/V, $N$ = 64 and $C + C_2$ = 500 pF. Find $K$. What is its steady phase error after a step in reference frequency, and why?

### Problem 15-12.2 [A]

**Margin, capacitor ratio and damping.** For maximum-margin designs with PM = 45°, 50° and 65°, find $\sqrt b$, $b$, the capacitor ratio $C/C_2$ and the damping $\zeta$ of the closed-loop pair. Which designs have all-real closed-loop poles?

### Problem 15-12.3 [A]

**Two rules of thumb.** (a) A PLL has a 25 MHz reference. What is the largest crossover the $f_{ref}/10$ rule allows, and about how much phase does PFD sampling cost at a 1 MHz crossover? (b) Twenty identical clock-recovery stages are cascaded, each with 0.1 dB of jitter-transfer peaking at the same frequency. What is the worst-case peaking of the chain, in dB and as an amplitude ratio?

### Problem 15-12.4 [B]

**A 2.4 GHz synthesizer.** Design the loop filter of a PLL with a 50 MHz reference, $N$ = 48, $I_{cp}$ = 200 µA and $K_v$ = 2π × 1 GHz/V for a 1 MHz crossover and 55° of phase margin. Give $\sqrt b$, $b$, $\tau_z$, $\tau_p$, $K$, $C + C_2$, $C_2$, $C$ and $R$, and check the sampling rule.

### Problem 15-12.5 [B]

**What margin buys.** Using the factorization of §3.2, give the closed-loop poles of a 45° maximum-margin design in units of $\omega_c$. Then compute its frequency-step overshoot and jitter-transfer peak (in dB, and the frequency of the peak relative to $\omega_c$), and compare them with the 60° design of Example 15-12.3.

### Problem 15-12.6 [B]

**Integrating phase noise.** A clock's phase noise is a flat −100 dBc/Hz from 10 kHz to 1 MHz offset and negligible elsewhere. Find the rms phase and, for a 1 GHz clock, the rms jitter.

### Problem 15-12.7 [C]

**The LDO at light load.** For Example 15-12.6's LDO with $R_{ESR}$ = 0.3 Ω: (a) find the crossover and phase margin at $R_L$ = 1 kΩ with $g_m$ unchanged, and explain why they barely move; (b) at that light load the pass device's current is 100 times smaller and, in strong inversion, $g_m \propto \sqrt{I_D}$, so $g_m$ = 0.05 A/V: find the crossover, the phase margin and the new ESR window for 45°; (c) is a 0.15 Ω capacitor acceptable at both loads?

### Problem 15-12.8 [B]

**Sizing output capacitance.** An accelerator's 0.8 V rail sees 100 A load steps and may move by 40 mV. Its regulator's proportional path has $g/C = 2\pi \times 100$ kHz (the crossover of a load-line design). Using the transconductance model, how much output capacitance does a load-line design need? A critically damped PI design with the same $g/C$, and where does that PI loop actually cross over?

### Problem 15-12.9 [A]

**A DVFS downshift.** The core of Example 15-12.1 moves from 2.0 GHz at 1.00 V to 1.0 GHz at 0.75 V. Give the order of operations, the time during which the core is stalled, the time for the voltage to fall at 10 mV/µs, and the ratios of dynamic power and of energy per cycle.

### Problem 15-12.10 [C]

**A better heat sink.** Example 15-12.7's processor gets a heat sink with $R_{CA}$ = 0.25 K/W (same $C_H$). Find the sustained power, the one-pole estimate and the exact time at 200 W before throttling, and the decay time constant of the permitted power.

### Problem 15-12.11 [C]

**Leakage inside the thermal loop.** Leakage adds $dP_L/dT$ = 0.6 W/K of power per kelvin of junction temperature to Example 15-12.7's processor. Find the plant's gain $\lvert\theta_J/P\rvert$ at DC and at 2 rad/s, without and with leakage, and explain what this means for the throttling loop and for the sustained useful power.

### Problem 15-12.12 [C]

**A different noise balance.** A 1 GHz PLL's reference path contributes a flat −100 dBc/Hz at the output and its VCO −115 dBc/Hz at 1 MHz, falling 20 dB/decade. With a 60° maximum-margin loop, estimate the jitter-optimal crossover, then find the optimum numerically and the rms phase and jitter there (10 kHz to 100 MHz).

---

## Objective coverage

| Learning objective (chapter 15-12) | Problems |
|---|---|
| 1. PLL phase-domain model and loop-filter design | 1, 2, 4 |
| 2. PLL closed loop, peaking, bandwidth and jitter | 3, 5, 6, 12 |
| 3. LDO loop and ESR | 7 |
| 4. Load-step droop, bandwidth and capacitance | 8 |
| 5. DVFS sequencing and thermal throttling | 9, 10, 11 |
