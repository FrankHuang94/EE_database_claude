# Lab 07-07 · Frequency Response and Bode Plots

**Chapter:** [07-07](../../chapters/07-07-frequency-response-and-bode-plots.md) · **Notebook:** [07-07-bode.ipynb](07-07-bode.ipynb) · **Time:** about 2.5 hours

## Objective

1. Draw Bode plots with their asymptotes and see where the straight lines fail.
2. Watch a resonant filter amplify near its corner, and damp it.
3. Test Bode's gain–phase relation numerically, and see it fail for a right-half-plane zero.
4. Measure how gain trades against bandwidth in an op-amp circuit, and how phase margin shows up as peaking.
5. Relate rise time to bandwidth for different response shapes.

## Background

Chapter sections 3.1 to 3.9 and Examples 07-07.2 to 07-07.6. You need Python with NumPy, SciPy and Matplotlib, and ngspice for the simulator checks (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [07-07-bode.ipynb](07-07-bode.ipynb) | The guided notebook (Parts 1 to 5) | Its own `assert`s |
| [ex2_ac_amp.cir](ex2_ac_amp.cir) | AC sweep of Example 07-07.2: gain and phase at three frequencies, both −3 dB points | Chapter answer key |
| [ex3_lc_filter.cir](ex3_lc_filter.cir) | Example 07-07.3's filter at two loads, and Problem 07-07.14's damped version: peaks and attenuation | Chapter and solutions answer keys |
| [ex5_opamp.cir](ex5_opamp.cir) | Op-amp macromodels in feedback (Example 07-07.5) and the guided exercise's two-pole buffer | Chapter answer key and this handout |
| [ex6_rise.cir](ex6_rise.cir) | Transient rise times of one pole and of two cascaded poles (Example 07-07.6) | Chapter answer key |

Run the netlists from the repository root:

```bash
python tools/run_spice.py 07-07
```

## Procedure

1. **Asymptotes (Part 1).** *Predict first:* for Example 07-07.2, the gain at 1.592 Hz and at 159.2 kHz. Then plot the exact curve over the asymptotes and read the errors.
2. **A filter that amplifies (Part 2).** *Predict first:* the peak gain of Example 07-07.3's filter with no load at all (only the 30 mΩ series resistance damps it). Then add the damper of Problem 07-07.14 and watch the peak collapse.
3. **Gain and phase are linked (Part 3).** *Predict first:* the phase of a response whose magnitude falls at a steady −30 dB/decade. Then evaluate Bode's integral for Example 07-07.4's two stages.
4. **Gain versus bandwidth (Part 4).** Run [ex5_opamp.cir](ex5_opamp.cir). *Predict first* (the chapter's guided exercise): with a second pole at the 10 MHz unity-gain frequency, a unity-gain buffer has a phase margin of about 52°. How much does it peak, and at what frequency?
5. **Rise time and bandwidth (Part 5).** *Predict first:* which rises faster for the same −3 dB bandwidth, a single pole or a brick-wall response?

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | errors | 3.01 dB at each corner; under 0.05 dB a decade away |
| 2 | unloaded peak | higher than the 23.16 dB of the 100 Ω case (the notebook computes it) |
| 2 | damped peak | 2.27 dB at 8.67 kHz |
| 3 | −30 dB/decade | phase −135° (Bode's $k = -1.5$) |
| 4 | two-pole buffer | see the key below |
| 5 | rise time × bandwidth | 0.340 (Gaussian), 0.350 (single pole), 0.446 (brick-wall): for the same bandwidth the Gaussian rises fastest and the brick wall slowest (and it rings) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 07-07.a | phase margin of the two-pole buffer's loop | 51.83 | ° |
| Lab 07-07.b | closed-loop peak | 1.249 | dB |
| Lab 07-07.c | frequency of the peak | 7.071 | MHz |
| Lab 07-07.d | rise time × bandwidth, Gaussian | 0.340 | — |
| Lab 07-07.e | rise time × bandwidth, single pole | 0.350 | — |
| Lab 07-07.f | rise time × bandwidth, brick wall | 0.446 | — |

## Discussion questions

1. Why does the asymptotic Bode plot give no warning of Example 07-07.3's 19 dB peak?
2. In Part 4, why does the inverting amplifier of gain −100 have slightly less bandwidth than the non-inverting amplifier of gain +100?
3. In Part 3, why can the gain–phase integral recover stage A's phase but not stage B's?
4. Why do oscilloscope makers disagree about the rise-time constant (0.35 or 0.45)?

<details><summary>Answers to the discussion questions</summary>

1. The asymptotes of a complex pole pair ignore damping: they meet at the corner at 0 dB whatever ζ is. The true response there is $20\lg Q$ above them, 19.1 dB for this filter. Every complex pair needs that correction.
2. The bandwidth is GBW divided by the noise gain, $1/\beta$. Both circuits feed back through the same kind of divider, but the inverting one needs $R_f/R_g = 100$ for a signal gain of −100, which is a noise gain of 101. The non-inverting one reaches +100 with a noise gain of 100.
3. Bode's relation assumes no zeros in the right half-plane. Stage B's zero at $+\omega_z$ adds phase lag that leaves no trace on the magnitude, so no formula that sees only the magnitude can recover it.
4. The constant depends on the shape of the response near and beyond the cutoff. A single pole gives 0.35; instruments corrected to be flat almost to the bandwidth and then fall sharply behave more like a brick wall, about 0.45. Each maker states the constant that matches its own response.

</details>

## Optional hardware

With a function generator and a two-channel oscilloscope (or a USB audio interface and free audio-analysis software), build Example 07-07.2's input high-pass section and an RC low-pass with a corner near 1 kHz. Sweep the frequency, record the output-to-input amplitude ratio and the time shift between the channels, convert them to decibels and degrees, and plot them over the theory. Then build a non-inverting op-amp amplifier of gain 100 with any general-purpose op-amp and find its −3 dB frequency; compare it with the datasheet's gain–bandwidth product divided by 100. Keep the input small enough that the output never slews (a few tens of millivolts at the output is enough), or slew-rate limiting will look like a bandwidth limit.
