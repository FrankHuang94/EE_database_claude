# Problems 07-07 · Frequency Response and Bode Plots

Chapter: [07-07](../chapters/07-07-frequency-response-and-bode-plots.md) · Worked solutions: [07-07 solutions](../solutions/07-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $\lg = \log_{10}$; angles in degrees; ω in rad/s and $f$ in Hz, as labeled. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 07-07.1 [A]

**Decibel conversions.** (a) Express the power ratios 2, 0.5 and 1000 in dB. (b) Express the voltage ratios 2, 0.1 and √2 in dB. (c) Express 1 W and 1 µW in dBm, and 1 mV (RMS) in dBV. (d) What voltage ratio is −6 dB, and what power ratio is 13 dB?

### Problem 07-07.2 [A]

**Nepers and Bode's slopes.** (a) Express 1 Np in dB and 20 dB in Np. (b) Bode's 1940 paper discusses a loop gain falling at 10 dB per octave. Express that slope in dB per decade, and as $k$, the slope in units of 6.02 dB per octave (20 dB per decade). (c) For a minimum-phase function with that constant slope, what phase does the gain–phase relation give, and what phase margin does that leave?

### Problem 07-07.3 [A]

**One pole, exactly.** For $H = 1/(1 + j\omega/\omega_p)$, find the magnitude in dB and the phase at $\omega/\omega_p$ = 0.1, 0.5, 1, 2 and 10. Find the error of the straight-line magnitude asymptotes and of the straight-line phase approximation (0° to $\omega_p/10$, −45° per decade, −90° from $10\omega_p$) at each point.

### Problem 07-07.4 [B]

**A pole–zero–pole sketch.** $H(s) = \dfrac{1000(s + 10)}{(s + 100)(s + 10^4)}$. (a) Write it in Bode form and find the low-frequency gain in dB. (b) Sketch the asymptotic magnitude and give its value at ω = 1, 50, 1000 and $10^5$ rad/s. (c) Find the exact magnitude and phase at the same frequencies. (d) Where between the zero and the first pole is the phase lead largest, and how large is it? Compare with the formula for an isolated zero–pole pair, $\phi_{max} = \arcsin\big((\alpha - 1)/(\alpha + 1)\big)$ at $\sqrt{\omega_z\omega_p}$, where $\alpha = \omega_p/\omega_z$.

### Problem 07-07.5 [B]

**A lead network.** A resistor $R_1$ = 9 kΩ in parallel with $C$ = 10 nF is in series from input to output, and $R_2$ = 1 kΩ connects the output to ground. (a) Derive $H(j\omega)$ and write it in Bode form. (b) Find the zero and pole frequencies in Hz and the gain at low and high frequency in dB. (c) Find the maximum phase lead, the frequency where it occurs and the gain there. (d) Why is such a network useful in a feedback loop?

### Problem 07-07.6 [B]

**Complex poles at three dampings.** $H = 1/\big(1 + 2\zeta(jf/f_0) + (jf/f_0)^2\big)$ with $f_0$ = 1 kHz. For ζ = 0.1, 0.5 and 0.707: (a) find the magnitude at $f_0$ in dB and compare with the asymptotes; (b) find the phase at 500 Hz and 2 kHz. (c) For ζ = 0.1, find the peak and its frequency.

### Problem 07-07.7 [B]

**Reading a measured Bode plot.** A measured magnitude is flat at 32 dB at low frequency, bends down to −20 dB/decade around 2 kHz and to −40 dB/decade around 50 kHz; the phase passes about −45° near 2 kHz and about −135° near 50 kHz. (a) Write a transfer function consistent with these data. (b) Find the asymptotic and exact gain and the phase at 10 kHz. (c) Find where the asymptotes reach 0 dB, then the exact 0 dB frequency and the phase there. (d) If this were a loop gain, what would its phase margin be?

### Problem 07-07.8 [B]

**Op-amp bandwidth.** An op-amp has a gain–bandwidth product of 1 MHz and a DC open-loop gain of 100 dB, with a single dominant pole. (a) Find the closed-loop bandwidth of a non-inverting amplifier of gain +10 and of an inverting amplifier of gain −10. (b) Find the small-signal 10–90% rise time of the +10 amplifier. (c) What is the largest noise gain that still gives at least 20 kHz of bandwidth?

### Problem 07-07.9 [B]

**Bandwidth shrinkage.** (a) Find the bandwidth of 2, 3 and 4 identical buffered single-pole stages, as a fraction of one stage's corner frequency. (b) A three-stage amplifier must have an overall bandwidth of at least 1 MHz. What corner frequency must each stage have?

### Problem 07-07.10 [A]

**Delay and group delay.** (a) Find the phase shift of a pure 2 ns delay at 10 MHz, 100 MHz and 500 MHz. (b) Find the group delay of a single pole with a 1 kHz corner, at DC and at the corner.

### Problem 07-07.11 [B]

**Oscilloscope plus probe.** An oscilloscope (350 MHz) and a probe (500 MHz) are each modeled as a single pole, and they are cascaded without interaction. (a) Find the exact system bandwidth and the estimate $1/\text{BW}^2 = 1/\text{BW}_1^2 + 1/\text{BW}_2^2$. (b) Find the exact system rise time and the root-sum-square estimate of the two rise times. (c) Which estimate is optimistic, and why?

### Problem 07-07.12 [C]

**A fractional slope in a battery.** Electrochemical impedance spectroscopy (07-05 §9) often finds a diffusion region where a cell's impedance is approximately $Z = \sigma(j\omega)^{-1/2}$, called a Warburg element. Take $\sigma$ = 1 mΩ·s$^{-1/2}$. (a) Find $\lvert Z\rvert$ at 1 Hz and 100 Hz. (b) Find the slope of $\lvert Z\rvert$ in dB per decade and the phase of $Z$. (c) Show that these agree with Bode's constant-slope relation, and explain why a Nyquist plot of such a region is a straight line at 45°.

### Problem 07-07.13 [C]

**Phase margin and peaking.** A loop gain is $T(s) = \omega_t/\big(s(1 + s/\omega_2)\big)$ in a unity-feedback loop. (a) For $\omega_2 = \omega_t$, find the crossover frequency (as a multiple of $\omega_t$), the phase margin, the closed-loop ζ, the closed-loop peak in dB and the frequency of the peak relative to the closed-loop $\omega_0$. (b) Repeat for $\omega_2 = 2\omega_t$. (c) A datasheet quotes a phase margin of 55° at unity gain. Between which of these two cases does that fall, and what does it imply for a unity-gain buffer's step response?

### Problem 07-07.14 [C]

**Damping the supply filter.** Example 07-07.3's filter ($L$ = 4.7 µH, $R_s$ = 30 mΩ, $C$ = 22 µF, $R_L$ = 10 Ω) amplifies by 19 dB near 15.7 kHz. Add a damping branch across $C$: $R_d = \sqrt{L/C}$ in series with $C_d = 4C$. (a) Find $R_d$ and explain why $C_d$ is needed in series with it. (b) Find the gain at the original $f_0$ = 15.68 kHz with and without the damper. (c) Find the new peak gain and its frequency. (d) Find the gain at 500 kHz with the damper, and explain why the damper costs almost no attenuation there.

---

## Objective coverage

| Learning objective (chapter 07-07) | Problems |
|---|---|
| 1. Decibels, nepers, reference levels | 1, 2 |
| 2. $H(j\omega)$ from a circuit or $H(s)$; Bode form | 4, 5, 14 |
| 3. Asymptotic Bode plots and corrections | 3, 4, 5, 6 |
| 4. Reading Bode plots; minimum phase; delay | 2, 7, 10, 12 |
| 5. Bandwidth, rise time, cascades, gain–bandwidth | 8, 9, 11 |
| 6. Datasheet specifications and practice | 8, 11, 13, 14 |
