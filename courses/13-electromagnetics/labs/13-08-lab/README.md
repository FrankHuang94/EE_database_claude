# Lab 13-08 · Transmission Lines: Sinusoidal Steady State

Chapter: [13-08 Transmission Lines: Sinusoidal Steady State](../../chapters/13-08-transmission-lines-sinusoidal-steady-state.md)

## Objective

See standing waves form for different loads, watch Γ and $Z_{in}$ trace circles and spirals as a line lengthens, measure how a quarter-wave transformer's bandwidth shrinks with the impedance ratio, and see how loss hides a mismatch and how Heaviside's condition removes distortion. Then simulate the input impedance of line sections in ngspice.

## Background

γ and $Z_0$ (§3.1), Γ along the line and input impedance (§3.2), standing waves and power (§3.4), the quarter-wave transformer (§3.5) and lossy lines (§3.6).

## Files

- [13-08-lines-steady-state.ipynb](13-08-lines-steady-state.ipynb): the notebook (Parts 1–4).
- [line_impedance.cir](line_impedance.cir): a λ/8 50 Ω line with a 100 Ω load, and a 70.71 Ω quarter-wave transformer with a 100 Ω load, driven by 1 A at 1 GHz. Run with `ngspice -b line_impedance.cir`, or `python tools/run_spice.py 13-08` from the repository root.
- [problems.cir](problems.cir): input impedances of Problems 13-08.2, 13-08.4 and 13-08.13 and the stubs of Example 13-08.3.

## Procedure

1. **Standing waves (Part 1).** Plot |V| over one wavelength for a short, an open, a match, 100 Ω, 25 Ω and 50 + j50 Ω. *Predict first:* where are the minima?
2. **Γ and Z_in (Part 2).** Plot Γ(d) and $Z_{in}$ in the complex plane for a 100 − j50 Ω load, lossless and lossy.
3. **Transformer bandwidth (Part 3).** Plot |Γ| against $f/f_0$ for 2:1, 4:1 and 10:1 steps; find the bandwidth for |Γ| < 0.1.
4. **Loss and distortion (Part 4).** Plot the apparent return loss of a short through RG-58 against length; propagate a pulse on an ordinary and a distortionless line.
5. **ngspice (the chapter's guided exercise).** Predict both input impedances, then run `line_impedance.cir`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Minima | At the load for the short and 25 Ω; λ/4 away for the open and 100 Ω; at 0.3381λ for 50 + j50 Ω |
| 2 | Γ(d) | A circle repeating every λ/2 when lossless; an inward spiral with loss |
| 3 | Bandwidth | 36.70% (2:1), 17.11% (4:1), 9.00% (10:1) |
| 4 | Loss | Apparent return loss rising 1.41 dB per metre; the distortionless line's pulse keeps its shape |
| ngspice | Input impedance | 40 − j30 Ω and 50 Ω |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 13-08.a | single-section bandwidth for a 4:1 step, Γ below 0.1 | 17.11 | % |
| Lab 13-08.b | apparent return loss of a short through 5 m of RG-58 at 1 GHz | 7.054 | dB |

*These are recomputed by [verify_13_08.py](../../verify/verify_13_08.py), which marches the phasor telegrapher's equations numerically instead of using the closed forms.*

## Discussion questions

1. Why does Γ(d) rotate clockwise as you move toward the generator?
2. Why does the quarter-wave transformer's bandwidth shrink as the impedance ratio grows?
3. Why does the distortionless line need more loss (a nonzero $G'$) to give a better pulse?

### Answers

1. $\Gamma(d) = \Gamma_Le^{-j2\beta d}$: increasing $d$ subtracts phase, a clockwise rotation in the complex plane. Physically, moving toward the source delays the reflected wave relative to the forward one by the extra round-trip distance $2d$.
2. Off the design frequency the section's input impedance deviates from 50 Ω by an amount that scales with how different $Z_1$ is from $Z_0$ and $R_L$; with a bigger step, the same fractional frequency error produces a larger reflection, so the |Γ| limit is reached sooner.
3. Distortion comes from the frequency dependence of α and of the phase velocity, not from the size of α. Adding $G'$ in proportion ($G'/C' = R'/L'$) makes the series and shunt losses scale identically, so γ becomes a constant plus jω times a constant: every frequency is attenuated and delayed equally. The pulse arrives smaller but with its shape intact, which equalizers otherwise have to restore.

## Optional hardware extension

With a NanoVNA-class instrument (or any VNA), measure the input impedance of a coaxial cable a few metres long terminated in an open, a short and a 50 Ω load, against frequency. Watch the impedance trace circle the Smith chart as frequency changes, and estimate the cable's loss from how the circles shrink at high frequency.
