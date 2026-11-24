# Lab 20-03 · Bandgap References over Temperature, Process and Trim

Chapter: [20-03 · Bandgap and Voltage References](../../chapters/20-03-bandgap-references.md)

## Objective

- See the CTAT junction voltage, the PTAT difference voltage and their flat sum, and how the bias current's temperature dependence changes the junction's slope.
- Confirm the op-amp bandgap and the 0.6 V current-mode reference in ngspice, whose PNP model follows the chapter's temperature law exactly.
- Run a seeded Monte Carlo of saturation-current spread and op-amp offset, and see what a one-temperature trim fixes and what it breaks.
- Compare first-order and curvature-compensated references as the device exponent η changes.
- Find both operating points of a β-multiplier, including the zero-current one.

## Background

The T130 substrate PNP has $I_S(T) = I_{S0}(T/T_0)^\eta\exp[(qV_{g0}/k)(1/T_0 - 1/T)]$ with $I_{S0}$ = 2 × 10⁻¹⁷ A, $V_{g0}$ = 1.2009 V and η = 3. This is SPICE's Gummel–Poon law with `EG` = 1.2009 and `XTI` = 3, and `.options tnom=26.85` puts SPICE's reference temperature at 300 K. Example 20-03.2's design (8:1 area ratio, 5 µA per branch, $R_1$ = 10.75 kΩ, $R_2$ = 115.2 kΩ) has zero TC at 312.0 K and 1.25463 V at 300 K.

Files:

- `bandgap.py`: the PNP model (`PNP`), Tsividis's closed form (`vbe_closed_form`), the zero-TC gain (`k_zero_tc`), the first-order output (`vref_closed_form`), exact solvers for the op-amp bandgap (`opamp_bandgap`, with offset) and the current-mode reference (`current_mode_bandgap`), `box_tc`, and a charge-based β-multiplier (`NMOS`, `beta_multiplier`).
- `bandgap.cir`: Example 20-03.2 with and without a 1 mV op-amp offset, swept from −40 to 125 °C.
- `banba.cir`: the 0.6 V current-mode reference of Example 20-03.4, swept over temperature.
- `20-03-bandgap-lab.ipynb`: the procedure below.

## Procedure

1. **The two slopes.** Predict $V_{BE}$ at −40 °C and 125 °C for 5 µA with constant and with PTAT bias. Plot $V_{BE}$, $\Delta V_{BE}$ and their weighted sum from −40 to 125 °C (Part 1).
2. **The bandgap in ngspice.** Predict the output at 300 K, the peak temperature and the box TC of Example 20-03.2; run `ngspice -b bandgap.cir`. Plot the output for zero-TC temperatures of 27, 39 and 60 °C (Part 2).
3. **Trim Monte Carlo.** Draw 400 parts with a seeded generator (`numpy.random.default_rng(2003)`, one standard-normal pair per part): $I_S$ multiplied by $e^{0.1z_1}$ (a 10% log-normal spread) and an op-amp offset of 0.5 mV × $z_2$. For each part compute the 300 K output, the untrimmed box TC, and the box TC after trimming $R_2$ to restore 1.25463 V at 300 K (box TCs on a 5 K grid from −40 to 125 °C, normalized to 1.25463 V). Predict whether the trim improves the median TC (Part 3).
4. **Sub-1 V.** Predict the 0.6 V reference's output at −40 °C and 125 °C; run `ngspice -b banba.cir` (Part 4).
5. **Curvature compensation.** Plot the box TC against the true η from 2.6 to 3.4 for a first-order design and for one compensated with α = 2 (Part 5).
6. **Two operating points.** For Example 20-03.6's β-multiplier, plot M1's current and the M2 + $R$ branch's current against the gate voltage on a log scale, and mark the intersection (Part 6).

## Expected results

- **Part 1.** At 5 µA: **0.8101** V at −40 °C and **0.4784** V at 125 °C with a constant current; **0.8050** V and **0.4881** V with a PTAT current. The PTAT current flattens the junction slightly.
- **Part 2.** ngspice gives 1.25463 V at 300 K, a peak of 1.25467 V near 39 °C and 1.25279 V at −40 °C (Example 20-03.2); with a 1 mV offset, 1.24187 V at 300 K.
- **Part 3.** The untrimmed 300 K outputs spread with a standard deviation of **7.06** mV, dominated by the offset (about 11.7 × 0.5 mV) and by $V_T\ln$ of the $I_S$ spread. The untrimmed box TC has a median of **11.37** ppm/K and a 95th percentile of **18.14** ppm/K. After trimming, every part sits at 1.25463 V at 300 K, but the median box TC rises to **15.39** ppm/K and the 95th percentile to **35.15** ppm/K; only **47.75**% of trimmed parts are within 15 ppm/K. Repeat with the offset set to zero: every trimmed part returns exactly to the nominal 9.10 ppm/K.
- **Part 4.** ngspice gives 0.6000 V at 300 K, 0.60002 V at the peak and 0.59912 V at −40 °C (Example 20-03.4).
- **Part 5.** The first-order TC grows in proportion to η − 1; the compensated TC is proportional to |η − 3| and vanishes at η = 3.
- **Part 6.** The curves cross at 0.363 V and 0.372 µA; below it the M2 branch carries more current than M1 for the same gate voltage, so the only other consistent state is zero current.

## Discussion

1. **Why did trimming make the median TC worse?** The trim adjusts the PTAT term. It exactly cancels the $I_S$ error, which is PTAT, but converts the offset's nearly constant error into a slope (chapter §3.5). With a 0.5 mV offset σ, the offset dominates. A real product would remove the offset first (chopping, as in Ge et al.) and then trim.
2. **Is a 10% $I_S$ spread realistic?** It is an illustrative figure: a **2.6** mV shift in $V_{BE}$ per σ ($V_T \times 0.1$). The lab's point does not depend on its exact value: whatever the $I_S$ spread, a one-temperature trim removes it completely.
3. **Why use `.options tnom=26.85`?** SPICE's default nominal temperature is 27 °C (300.15 K). Setting it to 300 K makes the model's $I_{S0}$ refer to the chapter's $T_0$, so ngspice and the Python model agree to about a microvolt.

## Optional hardware

Two diode-connected transistors from a matched array (for example a CA3096-style or SSM2212-style pair, or simply two 2N3904 transistors on the same heat-spreading clip) at a 1:8 current ratio, with an op-amp and two resistors, make a working bandgap on a breadboard. Measure its output with a 6½-digit meter while heating the transistors with a hair dryer: you will see the arch of §3.3, and how much a thermal gradient between the two transistors matters.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 20-03.a | V_BE at −40 C, constant current | 0.8101 | V |
| Lab 20-03.b | V_BE at 125 C, constant current | 0.4784 | V |
| Lab 20-03.c | V_BE at −40 C, PTAT current | 0.8050 | V |
| Lab 20-03.d | V_BE at 125 C, PTAT current | 0.4881 | V |
| Lab 20-03.e | sigma of the untrimmed 300 K output | 7.06 | mV |
| Lab 20-03.f | median untrimmed box TC | 11.37 | ppm/K |
| Lab 20-03.g | 95th-percentile untrimmed box TC | 18.14 | ppm/K |
| Lab 20-03.h | median trimmed box TC | 15.39 | ppm/K |
| Lab 20-03.i | 95th-percentile trimmed box TC | 35.15 | ppm/K |
| Lab 20-03.j | trimmed parts within 15 ppm/K | 47.75 | % |
| Lab 20-03.k | offset gain | 11.7 | — |
| Lab 20-03.l | V_BE shift per sigma of I_S | 2.6 | mV |
