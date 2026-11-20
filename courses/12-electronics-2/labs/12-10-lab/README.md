# Lab 12-10 · Noise in Circuits

Chapter: [12-10 Noise in Circuits](../../chapters/12-10-noise-in-circuits.md)

## Objective

Generate thermal noise with the right spectral density and check it; show by simulation that an RC circuit's capacitor noise is kT/C whatever the resistance; synthesize 1/f noise and watch its integrated value grow with the logarithm of bandwidth; and find an amplifier's optimum source resistance. Confirm kT/C with ngspice's noise analysis.

## Background

Spectral density and integration (§3.1), thermal noise (§3.2), kT/C (§3.3), flicker noise (§3.5) and noise figure (§3.8).

## Files

- [12-10-noise.ipynb](12-10-noise.ipynb): the notebook (Parts 1–4).
- [rc_noise.cir](rc_noise.cir): ngspice noise analysis of an RC low-pass, reporting the low-frequency noise density and the total integrated output noise. Run with `ngspice -b rc_noise.cir`, or `python tools/run_spice.py 12-10` from the repository root.

## Procedure

1. **Thermal noise (Part 1).** Generate samples with a 1 kΩ resistor's PSD, estimate the spectrum with Welch's method, and compare with $4kTR$.
2. **kT/C (Part 2, the chapter's guided exercise).** *Predict first:* does raising $R$ from 1 kΩ to 100 kΩ raise the capacitor's noise? Then simulate the RC circuit, driven only by the resistor's noise current, for three resistances (an Euler–Maruyama integration of 20 000 independent capacitors; expect agreement with $\sqrt{kT/C}$ to within about 1%, the step size's bias).
3. **1/f noise (Part 3).** Synthesize 1/f noise and plot its integrated RMS against the lower frequency limit.
4. **Noise figure (Part 4).** Plot NF against source resistance for $e_n$ = 1 nV/√Hz and $i_n$ = 1 pA/√Hz.
5. **ngspice.** Run `rc_noise.cir`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | PSD estimate | Scatters around 1.657 × 10⁻¹⁷ V²/Hz |
| 2 | Capacitor RMS | 64.36 µV for every R (300 K) |
| 3 | Integrated 1/f noise | Grows as $\sqrt{\ln(f_2/f_1)}$ |
| 4 | Noise figure | Minimum 0.495 dB at 1 kΩ |
| ngspice | RC noise | The values in the key below, at 27 °C |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 12-10.a | kT/C at 1 pF and 27 °C | 64.37 | µV |
| Lab 12-10.b | 10 kΩ noise density at 27 °C | 12.87 | nV/√Hz |

*These are recomputed by [verify_12_10.py](../../verify/verify_12_10.py) by integrating the filtered thermal spectrum at 300.15 K, ngspice's default temperature.*

## Discussion questions

1. Why does the kT/C result not depend on the resistor?
2. In Part 3, why does starting the integral at 0.01 Hz instead of 0.1 Hz add as much noise as extending it from 1 kHz to 10 kHz?
3. In Part 4, why is the noise figure high at both very low and very high source resistances?

### Answers

1. The resistor's noise density scales as $\sqrt R$ while the RC bandwidth scales as $1/R$; their product in power, $4kTR \times 1/(4RC)$, is $kT/C$.
2. A 1/f spectrum has equal power in every decade, so any added decade contributes the same.
3. At low $R_s$ the source's own noise $4kTR_s$ is tiny and the amplifier's voltage noise dominates; at high $R_s$ the current noise term $i_n^2R_s^2$ grows faster than $4kTR_s$. The optimum balances them.

## Optional hardware extension

With a low-noise amplifier (gain 1000) and a spectrum analyzer or a sound card, measure the noise of resistors from 100 Ω to 100 kΩ shorted at the input of the amplifier; plot density against $\sqrt R$ and find the amplifier's own floor where the line flattens.
