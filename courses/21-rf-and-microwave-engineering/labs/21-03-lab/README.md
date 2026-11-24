# Lab 21-03 · Noise Figure, Noise Parameters and Intermodulation

Chapter: [21-03 · Noise Figure and Linearity](../../chapters/21-03-noise-figure-and-linearity.md)

## Objective

- Map a transistor's noise figure over the source-reflection plane and see why a noise match is not a power match.
- Simulate Y-factor measurements with random noise and see how averaging limits their precision.
- Measure intercept points the way a bench does, with two-tone FFTs, and see where the slope-3 rule fails.
- Confirm a bipolar transistor's and a differential pair's distortion in ngspice.
- Explore the noise–linearity tradeoff of a receiver line-up as the LNA gain changes.

## Background

`rfnl.py` holds the chapter's formulas: `friis`, `noise_factor_gamma`, `noise_circle`, `noise_params_from_en_in`, `y_factor_nf`, `second_stage_correct`, `sensitivity_dbm`, `a_1db`, `a_iip3`, `a_iip2`, `cascade_iip3`, `sfdr_db`, a two-tone FFT helper `tones`, `bjt_harmonics` (Bessel functions) and `tanh_fundamental`/`tanh_x1db` for the differential pair. `bjt_im.cir` drives an ideal bipolar transistor and an emitter-coupled pair with one and two tones, resamples the collector currents on a uniform grid and correlates them with cosines, which is a discrete Fourier transform at chosen frequencies.

## Procedure

1. **Noise over the source plane.** Map the noise figure of Example 21-03.3's device for every passive $\Gamma_s$; overlay the 1.0 and 1.5 dB circles and mark $\Gamma_{opt}$, 50 Ω and the power-match point (Part 1).
2. **Y-factor statistics.** Simulate 2000 Y-factor measurements of Example 21-03.2's system, each averaging $10^4$ Gaussian noise samples per state, and compare the scatter of the noise figure with the prediction (Part 2).
3. **Two-tone sweep.** Sweep Example 21-03.1's amplifier (a cubic with 18 dB gain and IIP3 = 0 dBm) from −60 to 0 dBm per tone; measure the IM3 slope between −50 and −40 dBm and watch it change near compression (Part 3).
4. **Transistors in ngspice.** Compute the harmonic and IM3 levels of Example 21-03.4 exactly, then run `ngspice -b bjt_im.cir` and compare (Part 4).
5. **The line-up.** Sweep the LNA gain of Example 21-03.5 from 5 to 30 dB and plot the cascade noise figure and IIP3 (Part 5).

## Expected results

- **Part 1.** The map's minimum, 0.80 dB, sits at $\Gamma_{opt}$; 50 Ω gives 1.07 dB and the power match 2.04 dB.
- **Part 2.** The noise figures scatter with a standard deviation close to the prediction $10\log_{10}e \times \tfrac{Y}{Y - 1} \times 2/\sqrt{n}$ = **0.091** dB for $n = 10^4$: a single quick measurement cannot resolve a 0.1 dB difference.
- **Part 3.** The measured slope is **3.00**; the IIP3 extrapolated at −30 dBm is 0 dBm. Above about −15 dBm per tone the products no longer follow slope 3, and an intercept extrapolated there is wrong.
- **Part 4.** HD2 4.828%, HD3 0.1555%, IM3 −46.66 dBc for the transistor and −40.87 dBc for the pair, in both Python and ngspice; the pair's IM2 residue is about $10^{-8}$ of the fundamental.
- **Part 5.** At 10 dB of LNA gain the cascade noise figure is **6.32** dB and IIP3 **−8.6** dBm; at 25 dB they are **3.34** dB and **−20.3** dBm. No single gain is best for both, which is why receivers switch LNA gain with signal level.

## Discussion

1. **Why does the noise map have a single minimum, with circles around it?** The noise factor is a quadratic in the source admittance divided by its real part; in the reflection plane its level sets are circles, nested around $\Gamma_{opt}$ (§3.2).
2. **Why does more averaging help a Y-factor measurement only as $1/\sqrt n$?** Each noise power is estimated from $n$ samples of a random signal; the estimate's relative standard deviation falls as $\sqrt{2/n}$, and the ratio of two such estimates inherits both.
3. **Why does the IM3 slope change near compression?** Terms beyond the cubic (fifth and higher order) grow faster with amplitude and, in most amplifiers, oppose the cubic term; the polynomial's small-signal predictions no longer hold.
4. **Why is the differential pair's IM2 zero?** Its transfer characteristic is odd (tanh), so all even-order terms cancel; in a real pair, mismatch between the two halves leaves a residue that sets its IIP2.

## Optional hardware

With a signal generator that can sum two tones (or two generators and a resistive combiner), a small RF amplifier module and a spectrum analyzer, measure output IM3 at three input levels 5 dB apart: check the slope of 3 and compute IIP3. With a noise source and a spectrum analyzer that offers a noise-figure mode, repeat Part 2's measurement and note how the reading scatters with the analyzer's averaging setting.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 21-03.a | Y-factor noise-figure scatter, n = 10^4 | 0.091 | dB |
| Lab 21-03.b | measured IM3 slope, −50 to −40 dBm | 3.00 | dB/dB |
| Lab 21-03.c | cascade NF at 10 dB LNA gain | 6.32 | dB |
| Lab 21-03.d | cascade IIP3 at 10 dB LNA gain | −8.6 | dBm |
| Lab 21-03.e | cascade NF at 25 dB LNA gain | 3.34 | dB |
| Lab 21-03.f | cascade IIP3 at 25 dB LNA gain | −20.3 | dBm |
