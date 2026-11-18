# Problems 03-06 · Random Processes Preview: Noise

Chapter: [03-06](../chapters/03-06-random-processes-preview.md) · Worked solutions: [03-06 solutions](../solutions/03-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $k = 1.380649\times10^{-23}$ J/K, $q = 1.602177\times10^{-19}$ C. Noise densities are one-sided unless stated. $T = 300$ K unless stated; $T_0 = 290$ K for $kT_0$. Answers to 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 03-06.1 [A]

$X(t) = A\cos(\omega t + \Theta)$ with Θ uniform on $[0, \pi]$ (not $[0, 2\pi)$). (a) Find the mean function. (b) Is the process wide-sense stationary? (c) Evaluate the mean at $\omega t = \pi/2$ for $A = 1$ V.

### Problem 03-06.2 [A]

A WSS voltage has autocorrelation $R_X(\tau) = 4e^{-|\tau|/\tau_c} + 1$ V². Find (a) the total average power, (b) the DC power and the possible mean values, (c) the AC power, and (d) the correlation coefficient between samples τ_c apart.

### Problem 03-06.3 [B]

**Offsets are not ergodic.** Temperature sensors have offsets that are Gaussian across units with σ = 0.5 °C, plus white measurement noise of 0.05 °C rms. (a) A one-hour time average on one sensor converges to what? (b) To estimate the population's offset σ within ±10% at 95% confidence (using $\text{SE}(s)/\sigma \approx 1/\sqrt{2(n - 1)}$), how many sensors must be measured? (c) Which plan reveals the population spread: one sensor for 100 hours, or 100 sensors for one hour each?

### Problem 03-06.4 [A]

For a 50 Ω resistor at 290 K, find (a) the open-circuit noise density, (b) the rms noise in 1 MHz and in 1 GHz, and (c) the available noise power in each bandwidth, in dBm.

### Problem 03-06.5 [B]

A receiver has a 2 MHz bandwidth and a 2 dB noise figure. (a) Find its noise floor. (b) What input power gives an SNR of 6 dB? (c) Some systems recover signals well below the noise floor. What must they trade to do so?

### Problem 03-06.6 [B]

**Sizing a sampling capacitor.** An ADC with a 1 V full-scale range samples onto a capacitor at 300 K. Require the kT/C noise to be no larger than the quantization noise $\Delta/\sqrt{12}$. Find the quantization noise and the minimum capacitance for (a) 12 bits and (b) 16 bits. Comment on the trend.

### Problem 03-06.7 [B]

White noise of 10 nV/√Hz passes through a first-order low-pass filter with a 10 kHz corner. Find the noise bandwidth and the output rms noise.

### Problem 03-06.8 [A]

A photodiode carries 10 µA of signal current. Find its shot noise in a 100 MHz bandwidth and the ratio of signal current to noise, in dB.

### Problem 03-06.9 [B]

**Adding noise at an amplifier input.** A 50 Ω source at 290 K drives an amplifier with input voltage noise 1 nV/√Hz and input current noise 2 pA/√Hz. (a) Find the total input-referred noise density. (b) The noise factor $F$ is the total noise power divided by the source's own thermal noise power. Find $F$ and the noise figure $10\log_{10}F$.

### Problem 03-06.10 [B]

A sensor's noise has σ = 2 mV and an exponential autocorrelation with a 10 ms correlation time. A 10 s measurement is sampled at 1 kHz. Find (a) the standard deviation of the 10 s average (approximate formula), (b) the effective number of independent samples, and (c) what a naive $\sigma/\sqrt n$ would claim.

### Problem 03-06.11 [B]

Noise with σ = 1 mV and an exponential autocorrelation of correlation time 1 ms has a Lorentzian one-sided PSD. Find (a) its corner frequency, (b) its flat-region density in µV/√Hz, and (c) the fraction of its power below the corner.

### Problem 03-06.12 [B]

An amplifier has a white noise of 5 nV/√Hz with a 1/f corner at 10 Hz. (a) Find its rms noise from 0.1 to 10 Hz. (b) Compare with a zero-drift amplifier of 5.2 nV/√Hz flat. (c) Which would you choose for a 1 kHz audio preamplifier, and which for a weigh-scale bridge?

### Problem 03-06.13 [B]

A free-running oscillator accumulates timing error as a random walk, reaching 1 ps rms after 1 µs. Find the rms timing error after 100 µs and after 1 ms. Why does a receiver lock its sampling clock to the incoming data?

### Problem 03-06.14 [B]

Random NRZ data at bit rate $R_b$ has a one-sided PSD proportional to $\operatorname{sinc}^2(f/R_b)$, with nulls at multiples of $R_b$. (a) What fraction of the power lies below $R_b/2$, and below $R_b$? (b) Where is the first null for 10 Gb/s data? (c) Why do link designers often quote channel loss at $R_b/2$ (the Nyquist frequency)?

### Problem 03-06.15 [C]

**How noisy is a measured spectrum?** A spectrum analyzer averages $K$ independent periodograms, so each PSD bin is $\chi^2_{2K}/(2K)$ times the true value. (a) For $K = 16$, find the 95% confidence interval for the true PSD relative to the measured one, in dB. (b) Find the smallest $K$ for which the upper limit is within 1 dB. (c) Relate this to 03-05's chi-square interval for noise power.

### Problem 03-06.16 [C]

**A sensor front-end noise budget.** A 1 kΩ bridge sensor at 300 K feeds an amplifier; the measurement band is 0.1–100 Hz. Option A: an amplifier with 5 nV/√Hz white noise and a 10 Hz 1/f corner. Option B: a zero-drift amplifier with 8 nV/√Hz flat. (a) Find the total input-referred rms noise for each, including the sensor's thermal noise. (b) What signal gives a 40 dB SNR in each case? (c) Explain why the zero-drift part loses here, and how the answer changes if the band is 0.01–1 Hz.

---

## Objective coverage

| Learning objective (chapter 03-06) | Problems |
|---|---|
| 1. Mean and autocorrelation; wide-sense stationarity | 1, 2 |
| 2. Ergodicity; averaging correlated noise | 3, 10 |
| 3. PSD, noise bandwidth, filtering | 7, 11, 14, 15 |
| 4. Thermal, kT/C and shot noise; adding sources | 4, 5, 6, 8, 9, 16 |
| 5. Flicker noise and random walks | 12, 13, 16 |
