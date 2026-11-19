# Lab 10-04 · Small-Signal Models

Chapter: [10-04 Small-Signal Models](../../chapters/10-04-small-signal-models.md)

## Objective

Measure, by simulation, how far a transistor's small-signal model can be trusted: the harmonics a BJT and a MOSFET generate as the input grows, what a common-emitter output looks like when the signal is no longer small, and how the MOSFET's transconductance efficiency moves from its weak-inversion limit to the square law.

## Background

Linearization and the parameters (§3.1–3.3), the two models (§3.4), the distortion formulas and the exact Bessel-function harmonics (§3.6) and $g_m/I_D$ (§3.7). Part 3 uses the EKV interpolation [1], $I_D \propto \ln^2\!\left(1 + e^{V_{ov}/2nV_T}\right)$, which reduces to the square law for $V_{ov} \gg 2nV_T$ and to the exponential $e^{V_{ov}/nV_T}$ for $V_{ov} \ll -2nV_T$, with a smooth moderate-inversion region between.

## Files

- [10-04-small-signal.ipynb](10-04-small-signal.ipynb): the notebook (Parts 1–4).
- [ce_cs_ac.cir](ce_cs_ac.cir): ngspice AC analysis of the stages of Examples 10-04.1 and 10-04.6.

## Procedure

1. **Harmonics against amplitude (Part 1).** *Predict first:* at 20 mV, is a BJT's exact second-harmonic distortion above or below $\hat v/4V_T$? Then sample $e^{x\cos\theta}$ and the square law over a cycle, take an FFT, and plot $\text{HD}_2$ and $\text{HD}_3$ from 0.1 to 30 mV against the formulas.
2. **The common-emitter output (Part 2, the chapter's guided exercise).** *Predict first:* for Example 10-04.1's stage driven with 10 mV peak, how far does the output fall and how far does it rise? Then plot the exact output over a cycle against the small-signal sine.
3. **$g_m/I_D$ across inversion (Part 3).** *Predict first:* what is $g_m/I_D$ exactly at threshold ($V_{ov}$ = 0)? Then differentiate the EKV current numerically from $V_{ov}$ = −0.3 V to +0.6 V and overlay the two asymptotes of the chapter's Figure 2.
4. **Two models, one circuit (Part 4).** Solve 200 random degenerated common-emitter stages with the hybrid-π and the T model and confirm they agree to rounding.
5. **ngspice.** Run `python tools/run_spice.py 10-04`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | BJT $\text{HD}_2$ | slightly below $\hat v/4V_T$, by about $x^2/24$ of itself; the MOSFET's equals $\hat v/4V_{ov}$ exactly, with no third harmonic |
| 2 | CE output | the negative swing stretched, the positive compressed, and the average shifted down |
| 3 | $g_m/I_D$ | about 72% of the weak-inversion limit at threshold, and below the square law at 0.2 V of overdrive |
| 4 | Models | identical gains |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 10-04.a | BJT HD2 at 20 mV, exact | 18.88 | % |
| Lab 10-04.b | BJT HD2 at 20 mV, formula | 19.34 | % |
| Lab 10-04.c | BJT HD3 at 10 mV, exact | 0.618 | % |
| Lab 10-04.d | rise of average I_C at 10 mV | 3.78 | % |
| Lab 10-04.e | CE output, negative peak | -2.361 | V |
| Lab 10-04.f | CE output, positive peak | 1.604 | V |
| Lab 10-04.g | small-signal output amplitude | 1.934 | V |
| Lab 10-04.h | shift of average output | -0.189 | V |
| Lab 10-04.i | g_m/I_D at threshold, n = 1.3 | 21.46 | 1/V |
| Lab 10-04.j | g_m/I_D at V_ov = 0.2 V | 9.36 | 1/V |
| Lab 10-04.k | g_m/I_D at V_ov = −0.2 V | 29.03 | 1/V |

## Discussion questions

1. Why is the BJT's exact $\text{HD}_2$ *below* the first-order formula, when the higher-order terms of the exponential are all positive?
2. In Part 2, the average output falls by 0.19 V although the input averages zero. Where does the DC shift come from, and why does it matter for a multistage amplifier?
3. At $V_{ov}$ = 0.2 V the EKV $g_m/I_D$ (9.36 V⁻¹) is already below the square law's 10 V⁻¹, and near threshold the gap is far larger. Explain from the curve of Part 3 why the square law overestimates $g_m/I_D$ everywhere.

### Answers

1. Higher-order terms feed both harmonics. The cubic term adds to the fundamental ($x^3/8$) and the quartic to the second harmonic ($x^4/48$); relative to their leading terms these are $x^2/8$ and $x^2/12$, so the fundamental grows faster than the second harmonic, and their ratio falls below $x/4$ by about $x^2/24$.
2. The even-order terms of the expansion have nonzero averages: $\cos^2\theta$ averages ½, so the collector current's average rises by $I_C[I_0(x) - 1]$, 3.78% at 10 mV, and the collector's average voltage falls by $R_C$ times that. In a DC-coupled chain this shift moves the next stage's operating point, so large signals change the bias of the whole amplifier.
3. The EKV curve approaches the square law's $2/V_{ov}$ from below as $V_{ov}$ grows, so at 0.2 V it still lies under it. As $V_{ov}$ falls the square law climbs without limit, while the real curve flattens toward $1/nV_T$: the square law always overestimates $g_m/I_D$, slightly at large overdrive and grossly near threshold.

## Optional hardware extension

Bias a 2N3904 at 1 mA with $R_C$ = 5 kΩ from 10 V (a four-resistor bias as in 10-03, emitter bypassed), drive it with a 1 kHz sine through an attenuator, and look at the collector with an oscilloscope's FFT. Raise the input from 1 mV to 10 mV and compare the second harmonic with Part 1.

## Sources

1. C. C. Enz, F. Krummenacher and E. A. Vittoz, "An analytical MOS transistor model valid in all regions of operation and dedicated to low-voltage and low-current applications," *Analog Integrated Circuits and Signal Processing*, vol. 8, pp. 83–114, 1995.
