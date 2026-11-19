# Lab 09-09 · The Long-Channel MOSFET

**Chapter:** [09-09](../../chapters/09-09-long-channel-mosfet.md) · **Notebook:** [09-09-mosfet.ipynb](09-09-mosfet.ipynb) · **Netlist:** [nmos.cir](nmos.cir) · **Time:** about 2 hours

## Objective

1. Solve the channel numerically: potential and charge along the channel and output characteristics, for the bulk-charge ($m$) model and the exact bulk-charge model.
2. Add Hu's universal mobility and compare the transfer curve with the constant-mobility square law.
3. Follow $g_m/I_D$ from weak to strong inversion, and find where it falls to half its weak-inversion value.
4. Confirm in ngspice that a level-1 (square-law) model reproduces the chapter's $m$ = 1 saturation currents with and without body bias.

## Background

Chapter sections 3.1–3.7 and Examples 09-09.1 to 09-09.7. The transistor: $W$ = 10 µm, $L$ = 1 µm, $T_{ox}$ = 4 nm, $N_A$ = 5 × 10¹⁷ cm⁻³, $V_{TH}$ = 0.4 V. The channel profile comes from current continuity: $I_D\,dx = W\mu C_{ox}q(V_c)\,dV_c$, integrated numerically. Part 3 uses an interpolation (the form used in the EKV compact model), $I_D = 2mK V_T^2\ln^2(1 + e^{V_{ov}/2mV_T})$ with $K = \mu C_{ox}W/L$. It reduces to the square law in strong inversion and to an exponential with swing $mV_T\ln10$ in weak inversion. SPICE's level-1 model is the square law with $m$ = 1, the body effect of §3.1 (parameters `GAMMA` and `PHI` = $2\phi_B$), and $\lambda$ for channel-length modulation. You need Python with NumPy, SciPy and Matplotlib, and optionally ngspice (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [09-09-mosfet.ipynb](09-09-mosfet.ipynb) | The guided notebook (Parts 1 to 3) | Its own `assert`s, which compare with the chapter's examples and the answer key below |
| [nmos.cir](nmos.cir) | ngspice level-1 NMOS: saturation current at $V_{SB}$ = 0 and 1 V | `* EXPECT` lines tied to the chapter's answer key (run by `tools/run_spice.py`) |

## Procedure

1. **The channel (Part 1).** *Predict first:* at $V_{DS} = V_{Dsat}$, what fraction of the channel length has an inversion charge below half its source value? Then plot $V_c(x)$ and $Q_{inv}(x)$, and the output characteristics for both models.
2. **Mobility (Part 2).** *Predict first:* will mobility degradation make $\sqrt{I_{Dsat}}$ against $V_{GS}$ bend up or down? Then compute both curves.
3. **$g_m/I_D$ (Part 3, the chapter's guided exercise).** *Predict first:* at what overdrive does $g_m/I_D$ fall to half of $1/(mV_T)$? Then compute it.
4. **ngspice (optional).** Run `ngspice -b nmos.cir` and compare with Examples 09-09.2 and 09-09.3.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | $I_{Dsat}$, $m$-model and exact | 0.698 and 0.7118 mA (Examples 09-09.2, 09-09.4) |
| 3 | Overdrive for half the weak-inversion $g_m/I_D$; $g_m/I_D$ at $V_{ov}$ = 0 | see the answer key |
| 4 | ngspice level-1 currents | 0.870 mA ($V_{SB}$ = 0) and 0.487 mA ($V_{SB}$ = 1 V) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 09-09.a | overdrive where g_m/I_D halves | 88.1 | mV |
| Lab 09-09.b | g_m/I_D at V_ov = 0 (interpolation) | 22.39 | V⁻¹ |

## Discussion questions

1. Why does the inversion charge fall slowly over most of the channel and then collapse near the drain at saturation?
2. Why does mobility degradation make the transfer curve look more linear than the square law?
3. What does it mean physically that $g_m/I_D$ at the conventional threshold ($V_{ov}$ = 0) is already well below its weak-inversion maximum?
4. SPICE's level-1 model gives 25% more current than the $m$-model for this device. Why do circuit designers still use more elaborate models, and what would they get wrong with level 1?

<details><summary>Answers to the discussion questions</summary>

1. Current continuity requires $q(V_c)\,dV_c/dx$ to be constant. Where the charge is large, a small field suffices, and the potential rises slowly. Near pinch-off the charge vanishes, so the field, and hence the potential, must rise steeply over a short distance: the charge collapses there.
2. Higher gate voltage raises the effective field and lowers the mobility (Hu's fit), so the current grows more slowly than $V_{ov}^2$. The square root of the current then bends down rather than rising as a straight line.
3. At the conventional threshold the inversion layer is in moderate inversion: part weak (diffusion, exponential) and part strong (drift, square law). The interpolation gives **22.39** V⁻¹ there, against the weak-inversion maximum of about 31 V⁻¹. $g_m/I_D$ halves at an overdrive of only **88.1** mV. The "threshold" is a convention, not a sharp edge, and analog designers bias in this moderate region for its balance of efficiency and speed.
4. Level 1 omits the bulk-charge factor, mobility degradation, velocity saturation, subthreshold conduction and accurate capacitances. It overestimates current and transconductance, cannot model leakage or moderate inversion, and fails badly for short channels. Production design uses physics-based compact models (BSIM and others) fitted to measured devices.

</details>

## Optional extension

Add a series source resistance $R_S$ to the $m$-model and solve for the drain current self-consistently ($V_{GS,\text{internal}} = V_{GS} - I_DR_S$). Find the $R_S$ at which the saturation current falls by 10%, and compare with the on-resistance of Example 09-09.1.
