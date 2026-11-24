# Lab 21-09 · The RF Front End: Acoustic Resonators, Ladder Filters, Switches and Mismatch

Chapter: [21-09 · The RF Front End](../../chapters/21-09-rf-front-end.md)

## Objective

- Build an acoustic resonator from the Butterworth-Van Dyke model and see its series and parallel resonances.
- Assemble a three-section ladder filter, measure its loss, bandwidth and rejection, and confirm them in ngspice.
- Watch temperature drift move a filter skirt across a fixed frequency.
- Evaluate an RF switch's on-state loss and off-state isolation (confirmed in ngspice) and size a transistor stack.
- Quantify antenna mismatch loss and decide when a tuner pays.

## Background

`frontend.py` holds the resonator model (`bvd`, `z_bvd`, `fp_over_fs`, `k2_eff`, `k2_approx`, `fp_for_k2`), the ladder (`ladder`, `ladder_s21`, `insertion_loss_db`, `band_edges`, `loss_at_temperature`), drift (`tcf_drift`), switches (`series_switch_on_db`, `series_switch_off_db`, `fom_fs`, `cutoff_hz`, `peak_voltage`, `stack_count`) and `mismatch_loss_db`. The ladder is computed by cascading ABCD matrices between 50 Ω terminations.

`ladder.cir` is the three-section ladder of Example 21-09.2 (series resonators at 2.000 GHz with $C_0$ = 1 pF, shunt resonators with $C_0$ = 2 pF tuned so that their anti-resonance is at 2.000 GHz, Q = 2000), measuring the loss at 2.00 GHz and the rejection at 1.88 and 2.12 GHz. `switch.cir` is a series switch between 50 Ω ports, once on (2 Ω) and once off (189 fF), at 2 GHz.

## Procedure

1. **The resonator.** *Predict* the anti-resonance of the 2 GHz resonator of Example 21-09.1 (capacitance ratio 17.44), and where it moves if $C_0$ is doubled with the motional branch unchanged. Plot $\lvert Z\rvert$ and read the impedance at $f_s$ (Part 1).
2. **The ladder.** *Predict* the 3 dB bandwidth if the coupling doubles (the capacitance ratio halves), and the centre loss at Q = 1000. Run the sweeps and `ngspice -b ladder.cir` (Part 2).
3. **Temperature.** *Predict* the edge drift of a −20 ppm/°C filter at 1.9 GHz from −30 to +85 °C. Then hold a frequency fixed at 2.07 GHz, just above the ladder's upper notch, and compute the ladder's rejection there at −30, +25 and +85 °C with the same TCF (Part 3).
4. **The switch.** *Predict* the isolation of the 2 Ω, 189 fF switch at 0.7, 2 and 6 GHz; run `ngspice -b switch.cir`; then size a stack of 2.5 V transistors for 33 dBm at VSWR 1, 2 and 4 (Part 4).
5. **Mismatch and tuning.** *Predict* the VSWR at which mismatch costs 1 dB, then find it; compute the largest tuner loss worth paying to go from VSWR 6 to 1.5 (Part 5).

## Expected results

- **Part 1.** The anti-resonance is 2.0565 GHz; with $C_0$ doubled it falls to **2.0285** GHz, because the spacing is proportional to $C_m/C_0$. At $f_s$ the impedance is **0.694** Ω, essentially $R_m$.
- **Part 2.** The bandwidth is 72.2 MHz; doubling the coupling nearly doubles it, to **142.0** MHz. At Q = 1000 the centre loss is **0.655** dB, twice the Q = 2000 value. ngspice reproduces the loss at 2.00 GHz (0.328 dB) and the rejections at 1.88 and 2.12 GHz (32.15 and 33.20 dB).
- **Part 3.** The edge drifts **−4.37** MHz. At 2.07 GHz the rejection is **52.98** dB at −30 °C, **49.94** dB at +25 °C and **47.35** dB at +85 °C: with a negative TCF the filter moves down in frequency as it warms, and the upper skirt slides toward the fixed frequency.
- **Part 4.** Isolation 21.64, 12.72 and **4.73** dB at 0.7, 2 and 6 GHz; ngspice gives 0.172 dB on and 12.72 dB off at 2 GHz. The stack needs **6**, **8** and **10** transistors at VSWR 1, 2 and 4.
- **Part 5.** Mismatch costs 1 dB at VSWR **2.66**; going from VSWR 6 to 1.5 is worth up to **2.92** dB of tuner loss.

## Discussion

1. **Why does doubling $C_0$ move the anti-resonance but not the series resonance?** The series resonance depends only on $L_m$ and $C_m$; the anti-resonance is where the inductive motional branch resonates with $C_0$, so a larger $C_0$ pulls it toward $f_s$. Filter designers use this: an added parallel capacitor narrows a resonator's effective coupling.
2. **Why does a filter's rejection at a fixed frequency change with temperature even though its shape does not?** The whole response slides by TCF × ΔT; near a steep skirt a slide of a few MHz changes the attenuation by several dB. Guaranteed isolation must be read at the worst temperature.
3. **Why does switch isolation fall at high frequency?** The off-state capacitance's impedance $1/\omega C_{off}$ falls with frequency, so isolation drops 6 dB per octave; a 6 GHz Wi-Fi switch needs a much smaller $C_{off}$ (and thus a better figure of merit) than a 700 MHz one.

## Optional hardware

A vector network analyser (or a low-cost one-port VNA) and any SAW filter evaluation board show the ideas directly: measure $\lvert S_{21}\rvert$, find the notches beside the pass band, and warm the board with a hair dryer while watching the skirt move. Measuring a crystal's impedance with the same instrument shows the series and parallel resonances of §3.1 at megahertz.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 21-09.a | anti-resonance with C0 doubled | 2.0285 | GHz |
| Lab 21-09.b | impedance at the series resonance | 0.694 | Ω |
| Lab 21-09.c | 3 dB bandwidth with doubled coupling | 142.0 | MHz |
| Lab 21-09.d | centre loss at Q = 1000 | 0.655 | dB |
| Lab 21-09.e | edge drift, −20 ppm/°C, 115 °C | −4.37 | MHz |
| Lab 21-09.f | rejection at 2.07 GHz, −30 °C | 52.98 | dB |
| Lab 21-09.g | rejection at 2.07 GHz, 25 °C | 49.94 | dB |
| Lab 21-09.h | rejection at 2.07 GHz, 85 °C | 47.35 | dB |
| Lab 21-09.i | switch isolation at 6 GHz | 4.73 | dB |
| Lab 21-09.j | stack at VSWR 1 | 6 | |
| Lab 21-09.k | stack at VSWR 2 | 8 | |
| Lab 21-09.l | stack at VSWR 4 | 10 | |
| Lab 21-09.m | VSWR for 1 dB mismatch loss | 2.66 | |
| Lab 21-09.n | tuner break-even loss, VSWR 6 to 1.5 | 2.92 | dB |
