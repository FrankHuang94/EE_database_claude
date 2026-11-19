# Lab 09-10 · Short-Channel Effects and Leakage

**Chapter:** [09-10](../../chapters/09-10-short-channel-effects-and-leakage.md) · **Notebook:** [09-10-short-channel.ipynb](09-10-short-channel.ipynb) · **Time:** about 2 hours

## Objective

1. Integrate the channel with Hu's piecewise velocity model, locate saturation where the drain-end field reaches $\mathcal E_{sat}$, and follow $I_{Dsat}$ from 2 µm down to 20 nm against the long-channel and source-injection limits.
2. Add source resistance self-consistently and see how much drive current it costs.
3. Plot threshold roll-off and DIBL against length, and the subthreshold curves of a short device at low and high drain bias.
4. Explore the I_on–I_off window against supply, swing and temperature.
5. Place dopants at random in thousands of virtual transistors and compare the threshold spread with the depth-weighted formula.

## Background

Chapter sections 3.1–3.7 and Examples 09-10.1 to 09-10.6. The transistor of Parts 1–2: 2 nm EOT ($C_{ox}$ = 1.727 µF/cm²), $m$ = 1.2, $V_t$ = 0.35 V, $\mu_{ns}$ = 183 cm²/V·s, $v_{sat}$ = 8 × 10⁶ cm/s, $V_{GS}$ = 1.0 V, $W$ = 1 µm. Below saturation the channel obeys $I_D(1 + \mathcal E/\mathcal E_{sat}) = W C_{ox}\mu_{ns}(V_{ov} - mV_c)\mathcal E$ with $\mathcal E = dV_c/dx$; integrating over the channel gives Hu's Eq. (6.9.3). Part 3 uses Hu's roll-off model with $l_d$ = 10 nm, Part 4 the swing $S = mV_T\ln 10$ scaled with temperature, and Part 5 the Poisson statistics of 09-02 and 03-02. You need Python with NumPy, SciPy and Matplotlib (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [09-10-short-channel.ipynb](09-10-short-channel.ipynb) | The guided notebook (Parts 1 to 5) | Its own `assert`s, which compare with the chapter's examples and the answer key below |

There is no ngspice file for this lab: SPICE's simple MOSFET levels do not model DIBL and roll-off in Hu's form, and the BSIM models that do need foundry parameters.

## Procedure

1. **$I_{Dsat}$ against length (Part 1, the chapter's guided exercise).** *Predict first:* as $L$ shrinks from 2 µm to 20 nm at 0.65 V overdrive, by what factor does the velocity-saturated $I_{Dsat}$ rise, against the 100-fold rise of the long-channel law? Then compute it, and find the length at which velocity saturation halves the long-channel current.
2. **Series resistance (Part 2).** *Predict first:* will 100 Ω·µm cost more or less than 10% of the current? Then solve self-consistently and compare with Example 09-10.2.
3. **Roll-off and DIBL (Part 3).** *Predict first:* at $L = 3l_d$ with $S$ = 80 mV/decade, by what factor does raising $V_{DS}$ from 0.05 V to 1.0 V raise the off-current? Then plot the subthreshold curves.
4. **The I_on–I_off window (Part 4).** *Predict first:* at $V_{DD}$ = 0.6 V, keeping 0.3 V of overdrive, how many decades of on/off ratio can a 70 mV/decade device have below threshold? Then sweep swing and temperature.
5. **Dopant fluctuation (Part 5).** *Predict first:* will the Monte Carlo spread match the first estimate (75.8 mV) or the depth-weighted value (43.7 mV) of Example 09-10.6? Then run it.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | $I_{Dsat}$ at 50 nm from the integrated channel | 0.497 mA/µm (Example 09-10.1) |
| 1 | $I_{Dsat}$ at 2 µm and 20 nm, the rise, the half-current length | see the answer key |
| 2 | Self-consistent $I_{Dsat}$ with 100 Ω·µm | 0.448 mA/µm (Example 09-10.2) |
| 3 | Off-current factor from DIBL at $L$ = 30 nm | see the answer key |
| 4 | Decades of on/off ratio below threshold | see the answer key |
| 5 | Monte Carlo $\sigma_{V_t}$ | within 2% of 43.7 mV (Example 09-10.6) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 09-10.a | I_Dsat at L = 2 µm | 0.0270 | mA/µm |
| Lab 09-10.b | I_Dsat at L = 20 nm | 0.679 | mA/µm |
| Lab 09-10.c | rise from 2 µm to 20 nm | 25.2 | — |
| Lab 09-10.d | length where velocity saturation halves the current | 62.0 | nm |
| Lab 09-10.e | DIBL off-current factor at 30 nm | 3.90 | — |
| Lab 09-10.f | decades of on/off ratio | 4.29 | — |
| Lab 09-10.g | threshold shift from DIBL at 30 nm | 47.3 | mV |

## Discussion questions

1. Why does $I_{Dsat}$ rise only about 25-fold, not 100-fold, as $L$ shrinks 100-fold?
2. Why does the self-consistent series-resistance loss exceed Hu's closed-form estimate for this device?
3. Why does the off-current respond to drain bias at 30 nm but hardly at 100 nm?
4. Why did the Monte Carlo spread land on the depth-weighted value, and what in the simulation encodes the depth weighting?

<details><summary>Answers to the discussion questions</summary>

1. At long lengths the current follows the $1/L$ law, but below about 100 nm the carriers at the drain end reach $v_{sat}$ and the current becomes $WC_{ox}v_{sat}(V_{ov} - mV_{Dsat})$, which depends on $L$ only through the small $V_{Dsat}$ term. From 2 µm to 20 nm the rise is **25.2**-fold, and the velocity-saturated current is half the long-channel value already at **62.0** nm.
2. Hu's closed form assumes $I_D \propto V_{ov}$ (full velocity saturation). This device is only partly saturated, so its current falls faster than linearly as the IR drop eats into the overdrive.
3. The drain's coupling to the source barrier decays as $e^{-L/l_d}$. At $3l_d$ (30 nm) raising $V_{DS}$ by 0.95 V lowers the threshold by **47.3** mV and raises the off-current **3.90**-fold at 80 mV/decade; at $10l_d$ the shift is under 0.1 mV.
4. Each simulated dopant shifts the threshold by $q(1 - x/W_{dep})/(C_{ox}WL)$ according to its depth $x$, so deep dopants count less. Averaging the square of that weight over a uniform depth gives the factor 1/3 in the variance, or $1/\sqrt3$ in σ.

</details>

## Optional extension

Replace the uniform doping of Part 5 with a retrograde profile: undoped for the top 10 nm and 5 × 10¹⁸ cm⁻³ below. Keep the depletion depth at 20 nm and recompute the spread. Why does moving the dopants away from the surface help, and what does it suggest about thin undoped bodies (09-12)?
