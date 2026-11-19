# Lab 09-07 · The Bipolar Junction Transistor

**Chapter:** [09-07](../../chapters/09-07-bipolar-junction-transistor.md) · **Notebook:** [09-07-bjt.ipynb](09-07-bjt.ipynb) · **Netlist:** [bjt.cir](bjt.cir) · **Time:** about 2.5 hours

## Objective

1. Build a Gummel plot from device physics and see the current gain fall at both ends of the current range.
2. Compute output characteristics from the moving base–collector depletion edge, and compare two definitions of the Early voltage.
3. Solve the drift–diffusion transit problem for graded SiGe bases.
4. Compute the cutoff frequency against current, including a simple Kirk-effect model.
5. Confirm in ngspice that the SPICE bipolar model reproduces the chapter's saturation point and output resistance.

## Background

Chapter sections 3.2–3.10 and Examples 09-07.1 to 09-07.6. The transistor is the chapter's NPN: $A_E$ = 10 µm², $W_B$ = 0.1 µm, $N_B$ = 10¹⁸ cm⁻³, $N_E$ = 10²⁰ cm⁻³ ($W_E$ = 0.2 µm, Hu's 95 meV band-gap narrowing) and $N_C$ = 10¹⁷ cm⁻³. The Gummel model adds two effects:

- high-level injection in the base, through $n'(N_B + n') = n_i^2e^{V_{BE}/V_T}$;
- depletion-region recombination in the emitter–base junction, with an assumed 0.1 µs lifetime over a 30 nm depletion width.

The SPICE bipolar model (Gummel–Poon) reduces to the Ebers–Moll equations of §3.7 when its high-current and leakage parameters are left at their defaults, and its Early-effect parameter `VAF` multiplies the transport current by $(1 - V_{BC}/V_{AF})$. You need Python with NumPy, SciPy and Matplotlib, and optionally ngspice (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [09-07-bjt.ipynb](09-07-bjt.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s, which compare with the chapter's examples and the answer key below |
| [bjt.cir](bjt.cir) | ngspice: forced-gain saturation point and output resistance | `* EXPECT` lines tied to the chapter's answer key (run by `tools/run_spice.py`) |

## Procedure

1. **Gummel plot (Part 1).** *Predict first:* over how many decades of collector current does the gain stay within a factor of 2 of its peak? Then compute $I_C$, $I_B$ and $\beta_F$ against $V_{BE}$, and find the peak gain and the currents at which it has halved.
2. **Early effect (Part 2).** *Predict first:* will extrapolating the $I_C$–$V_{CE}$ curve between 1 and 3 V give a larger or smaller Early voltage than the local value $Q'_B/C'_{jC}$ = 31.4 V at $V_{CB}$ = 2 V? Then compute both.
3. **Graded base (Part 3).** *Predict first:* does doubling the germanium grading from 0.1 to 0.2 eV halve the transit time? Then plot $\tau_B$ against the grading.
4. **Cutoff frequency (Part 4, the chapter's guided exercise).** *Predict first:* where does $f_T$ peak as $I_C$ rises from 10 µA to 100 mA, and why? Then compute $f_T(I_C)$ and identify the three regimes.
5. **ngspice (optional).** Run `ngspice -b bjt.cir` and compare with Examples 09-07.3 and 09-07.4.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Peak gain and half-gain currents | see the answer key |
| 2 | Local Early voltage at $V_{CB}$ = 2 V | 31.4 V (Example 09-07.3) |
| 2 | Extrapolated intercept over 1–3 V | see the answer key |
| 3 | $\tau_B$ at 0.1 eV grading | 2.84 ps (Example 09-07.5) |
| 4 | Peak $f_T$ (uniform base) and its current | see the answer key |
| 5 | ngspice | $V_{CE,\text{sat}}$ = 51.1 mV, $V_{BE}$ = 0.8967 V, $r_o$ = 31.4 kΩ |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 09-07.a | peak current gain | 26.6 | — |
| Lab 09-07.b | I_C where gain halves, high side | 11.2 | mA |
| Lab 09-07.c | I_C where gain halves, low side | 3.66 | nA |
| Lab 09-07.d | Early voltage extrapolated over V_CE 1–3 V | 24.5 | V |
| Lab 09-07.e | peak f_T, uniform base | 19.3 | GHz |
| Lab 09-07.f | current at the f_T peak | 17.2 | mA |

## Discussion questions

1. Why does the gain fall at low current, and why does the fall begin at a lower current for a cleaner (longer-lifetime) emitter–base junction?
2. Part 2 finds two different Early voltages. Why, and which one does a circuit designer need?
3. In Part 3, why does doubling the grading not halve the transit time?
4. In Part 4, why does $f_T$ peak just at the Kirk-effect current in this model, and why do designers bias slightly below the peak?
5. The ngspice model's output resistance is set by one parameter, `VAF`. What physics does that single parameter hide, and when would it mislead you?

<details><summary>Answers to the discussion questions</summary>

1. At low current, the base current is dominated by recombination in the emitter–base depletion region, which grows only as $e^{V_{BE}/2V_T}$ while the collector current grows as $e^{V_{BE}/V_T}$. The gain therefore falls as the current falls, halving at **3.66** nA here from a peak of **26.6**. A longer depletion-region lifetime shrinks the recombination prefactor, moving the crossover to lower current.
2. The local value $Q'_B/C'_{jC}$ is $I_C/(\partial I_C/\partial V_{CB})$ at one bias. The extrapolated intercept is where a straight line through the curve between 1 and 3 V hits the axis; it differs because the measurement point sits at a positive $V_{CE}$ (the intercept is shifted by roughly $V_{CE}$) and because $C'_{jC}$, and with it the slope, changes with bias. The fit gives **24.5** V. A designer needs the local small-signal value, $r_o = (\partial I_C/\partial V_{CE})^{-1}$, at the operating point.
3. With strong grading, transport becomes drift-dominated and $\tau_B \to W_B/(\mu_n\mathcal E)$, which does halve with doubled field. At 0.1–0.2 eV, however, diffusion still contributes, so the improvement is less than twofold.
4. In this model, $f_T$ rises while depletion-charging delay shrinks as $1/I_C$, and the base pushes out abruptly once $J > qN_Cv_{\text{sat}}$, so the peak, **19.3** GHz, sits at the Kirk current, **17.2** mA. Real devices show a rounded peak, and gain and linearity fall near it, so circuits bias somewhat below the peak, with margin for process and temperature spread.
5. `VAF` lumps the base-width modulation into a constant, but the real Early effect depends on the base doping profile and the bias-dependent base–collector capacitance, and at high $V_{CE}$ impact ionization adds further output conductance. A constant `VAF` misleads for large voltage swings, near breakdown, and for SiGe bases where the germanium profile makes $I_C$ depend more strongly on the collector-side base doping.

</details>

## Optional extension

Replace the abrupt Kirk model with a gradual one in which the base push-out grows smoothly with current, for example $W_{dC}\,\tfrac12[1 + \tanh((J - J_K)/0.2J_K)]$, and see how the $f_T$ peak rounds off and moves below $J_K$.
