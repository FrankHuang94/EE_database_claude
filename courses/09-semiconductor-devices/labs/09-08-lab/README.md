# Lab 09-08 · The MOS Capacitor

**Chapter:** [09-08](../../chapters/09-08-mos-capacitor.md) · **Notebook:** [09-08-mos.ipynb](09-08-mos.ipynb) · **Time:** about 2 hours

## Objective

1. Solve Poisson's equation in the silicon numerically and check the closed-form surface charge $Q_s(\phi_s)$.
2. Compute the surface potential and the depletion and inversion charges against gate voltage, and compare threshold definitions.
3. Compute quasi-static, high-frequency and deep-depletion C–V curves, and extract oxide thickness, doping and flat-band voltage from a synthetic noisy measurement.
4. Add interface charge and poly-gate depletion and see how each distorts the C–V curve.

## Background

Chapter sections 3.1–3.9 and Examples 09-08.1 to 09-08.6. The capacitor is the chapter's: p-type silicon with $N_A$ = 10¹⁷ cm⁻³, a 10 nm SiO₂ dielectric and an n⁺ polysilicon gate ($V_{fb}$ = −0.9858 V, $V_t$ = 0.3293 V). The notebook integrates Poisson's equation as an initial-value problem from the surface into the bulk (shooting on the surface field) to get $\phi(x)$, $n(x)$ and $p(x)$. It uses the first integral of §3.6 for the gate-voltage sweeps. High-frequency inversion is modeled by freezing the inversion charge at its DC value and letting the depletion edge respond, which reduces to $C_{\min}$ in the depletion approximation. You need Python with NumPy, SciPy and Matplotlib (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [09-08-mos.ipynb](09-08-mos.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s, which compare with Examples 09-08.1 to 09-08.5 and the answer key below |

## Procedure

1. **Poisson in the silicon (Part 1).** *Predict first:* at threshold, is the electron sheet density larger or smaller than $N_A$ times the Debye length? Then solve for $\phi(x)$ at $\phi_s = 2\phi_B$ and plot the carrier densities.
2. **Charges against gate voltage (Part 2, the chapter's guided exercise).** *Predict first:* how far above $2\phi_B$ is the surface potential when the inversion charge equals the depletion charge, and is the gate voltage there larger or smaller than $V_t + |Q_{dep}|/C_{ox}$? Then compute. Also find the gate voltage at which the inversion layer holds 10¹¹ electrons/cm², a current-like threshold.
3. **C–V and extraction (Part 3).** *Predict first:* which part of the C–V curve is most sensitive to doping? Then compute the three C–V curves and extract parameters from a noisy synthetic curve.
4. **Non-idealities (Part 4).** *Predict first:* does a positive interface charge of 10¹¹ cm⁻² shift the curve left or right, and by how much? Then add it, and add poly depletion with $N_{poly}$ = 10²⁰ cm⁻³ to a 2 nm oxide.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Exact charge at $2\phi_B$ | 1.663 × 10⁻⁷ C/cm², equal to the depletion approximation (Example 09-08.3) |
| 2 | $\phi_s$ at $V_g$ = 2 V | 0.9947 V (Example 09-08.3) |
| 2 | Inversion charge equal to depletion charge | see the answer key |
| 3 | $C_{FB}/C_{ox}$, $C_{\min}/C_{ox}$ | 0.6988 and 0.2242 (Example 09-08.4) |
| 4 | Flat-band shift from 10¹¹ cm⁻² | see the answer key |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 09-08.a | φ_s above 2φ_B when inversion charge equals depletion charge | 121.0 | mV |
| Lab 09-08.b | gate voltage there (exact) | 0.9854 | V |
| Lab 09-08.c | V_t + Q_dep/C_ox (sheet model) | 0.8109 | V |
| Lab 09-08.d | V_g for 1e11 electrons/cm² | 0.431 | V |
| Lab 09-08.e | flat-band shift from 1e11 cm⁻² | -46.4 | mV |

## Discussion questions

1. Why does the exact model need a higher gate voltage than the sheet model to make the inversion charge equal the depletion charge?
2. Part 2 gives two "thresholds": 0.3293 V ($\phi_s = 2\phi_B$) and the voltage for 10¹¹ electrons/cm². Which would a circuit designer use, and why do foundries define threshold by a current?
3. In Part 3, why is the minimum high-frequency capacitance the most doping-sensitive feature, and the accumulation capacitance the most oxide-sensitive?
4. In Part 4, how would you distinguish fixed oxide charge from interface traps on a measured C–V curve?

<details><summary>Answers to the discussion questions</summary>

1. In the exact model the surface potential keeps rising above $2\phi_B$: here by **121.0** mV when the two charges are equal. That deepens the depletion layer and absorbs some of the gate charge as extra acceptor charge rather than electrons. The sheet model pins $\phi_s$ at $2\phi_B$, so it predicts equality already at $V_t + Q_{dep}/C_{ox}$ = **0.8109** V, while the exact answer is **0.9854** V.
2. Circuits care about current. At $\phi_s = 2\phi_B$ the inversion charge is still small, and the current-defined threshold (here a charge of 10¹¹ cm⁻² at **0.431** V) better marks where a transistor turns on usefully. Foundries define threshold by a drain current per unit width because it is directly measurable on transistors and relevant to circuits; the $2\phi_B$ definition is a convenient physical approximation for derivations.
3. In accumulation the capacitance is $C_{ox}$ alone, so it measures the dielectric. In strong high-frequency inversion it is $C_{ox}$ in series with $\varepsilon_s/W_{d\max}$, and $W_{d\max}$ depends on doping (roughly as $1/\sqrt{N_A}$), so $C_{\min}$ encodes the doping.
4. Fixed charge shifts the whole curve rigidly along the voltage axis (here by **−46.4** mV for 10¹¹ cm⁻² through 10 nm). Interface traps change charge as the surface potential sweeps, so they stretch the curve, more in some regions than others, and they show frequency dispersion; comparing high- and low-frequency curves, or using conductance or charge-pumping methods, separates them.

</details>

## Optional extension

Model interface traps with a uniform density of 10¹¹ cm⁻²eV⁻¹ across the gap, neutral at mid-gap. Add their charge $-qD_{it}(\phi_s - \phi_B)$ to the voltage balance and plot the stretched quasi-static C–V curve.
