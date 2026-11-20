# Problems 17-01 · Random Processes and Power Spectral Density

Chapter: [17-01](../chapters/17-01-random-processes-and-psd.md) · Worked solutions: [17-01 solutions](../solutions/17-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $S(f)$ is a two-sided PSD and $G(f) = 2S(f)$ a one-sided one; powers are into 1 Ω (V²). $k = 1.380649 \times 10^{-23}$ J/K and $T_0$ = 290 K. $\operatorname{sinc}x = \sin(\pi x)/(\pi x)$. Problems marked *(lab)* need the lab's `randproc.py` or an equivalent tool.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 17-01.1 [A]

**A tone in noise.** $X(t) = \cos(2\pi f_0t + \Theta) + W(t)$, where Θ is uniform on $[0, 2\pi)$, $f_0$ = 1 kHz, and $W$ is zero-mean WSS noise, independent of Θ, with $R_W(\tau) = 0.01e^{-\lvert\tau\rvert/10\,\mu\text{s}}$ V². Find $R_X(\tau)$, the total power, the fraction of it in the tone, and describe $S_X(f)$.

### Problem 17-01.2 [A]

**One-sided and two-sided.** An op-amp's input voltage noise is 4 nV/√Hz, white. Give its one-sided and two-sided densities in V²/Hz and the rms noise in a band from 10 kHz to 1 MHz.

### Problem 17-01.3 [A]

**Is it WSS?** (a) $X(t) = A\cos(2\pi f_0t)$ with $A$ a zero-mean random variable of variance $\sigma^2$. (b) $X(t) = A\cos(2\pi f_0t) + B\sin(2\pi f_0t)$ with $A$, $B$ uncorrelated, zero mean, each of variance $\sigma^2$. Compute the mean and autocorrelation of each and decide.

### Problem 17-01.4 [B]

**Valid autocorrelations.** (a) Find the PSD of $R(\tau) = e^{-a\lvert\tau\rvert}\cos(2\pi f_0\tau)$ and show it is valid. (b) Show that $R(\tau) = 1 - \tau^2$ for $\lvert\tau\rvert \le 1$ (0 otherwise) is not a valid autocorrelation, and find the first frequency where its transform is negative.

### Problem 17-01.5 [B]

**RC-filtered noise.** White noise of one-sided density $10^{-14}$ V²/Hz drives an RC low-pass filter with $R$ = 1 kΩ and $C$ = 1 nF. Give the correlation time, the noise bandwidth, the output rms and the minimum sampling interval for which successive samples have correlation below 0.01.

### Problem 17-01.6 [B]

**Noise bandwidth of a two-pole filter.** *(lab)* Find the equivalent noise bandwidth of a second-order Butterworth low-pass filter, $\lvert H\rvert^2 = 1/(1 + (f/f_c)^4)$, as a multiple of $f_c$, and compare it with a one-pole filter of the same $f_c$.

### Problem 17-01.7 [B]

**Identifying a system with noise.** White noise of two-sided density $10^{-6}$ V²/Hz drives a system $H(f) = 1/(1 + jf/f_c)$, $f_c$ = 1 kHz. The measured output also contains independent sensor noise. Show that the cross-spectrum $S_{YX}$ is unaffected by the sensor noise, and give its magnitude and phase at 1 kHz.

### Problem 17-01.8 [B]

**An AR(1) sequence.** $X[n] = -0.8X[n - 1] + W[n]$ with white $W$ of variance 1. Give $R_X[0]$, $R_X[1]$, and the PSD at $\omega = 0$ and $\omega = \pi$. Which frequencies does it emphasize?

### Problem 17-01.9 [B]

**25 Gb/s NRZ.** A 25 Gb/s polar NRZ lane uses ±0.3 V. Give the first spectral null, the one-sided density near DC, and the power below 12.5 GHz. For unipolar 0/0.6 V signalling, what fraction of the power is in spectral lines?

### Problem 17-01.10 [B]

**Independent samples of band-limited noise.** Gaussian noise has a two-sided PSD of $2 \times 10^{-17}$ V²/Hz for $\lvert f\rvert < 5$ MHz and zero elsewhere. At what spacing are its samples independent, what is each sample's variance, and what is the probability that a sample exceeds 3σ in magnitude?

### Problem 17-01.11 [C]

**Noise folding at an ADC.** An amplifier with 5 nV/√Hz of white noise and a 50 MHz single-pole bandwidth drives an ADC sampling at 10 MS/s with no anti-alias filter. By what factor (and how many dB) does the in-band noise density exceed that with an ideal 5 MHz anti-alias filter? Give the rms noise in the samples in both cases.

### Problem 17-01.12 [C]

**A half-sine pulse.** *(lab)* Polar symbols ±1 at rate $1/T$ use the pulse $p(t) = \sin(\pi t/T)$ on $[0, T)$. Find $\lvert P(f)\rvert$, the first spectral null and the fraction of the power below $\lvert f\rvert = 1/T$, and compare with NRZ of the same symbol energy.

### Problem 17-01.13 [C]

**Asymmetric bandpass noise.** *(lab)* Noise has a two-sided PSD $N_0/2$ over $f_c < \lvert f\rvert < f_c + B$ only (one side of the carrier). After down-conversion at $f_c$, find $S_{n_I}$, the power of $n_I$, and the cross-correlation $R_{n_In_Q}(\tau)$. What is the largest magnitude of the correlation coefficient between $n_I(t + \tau)$ and $n_Q(t)$, at which lags does it occur, and what is its sign for $\tau > 0$?

### Problem 17-01.14 [C]

**The AMI line code.** *(lab)* Alternate mark inversion sends a 0 bit as 0 and each 1 bit as alternately +1 and −1, with NRZ pulses. For independent equiprobable bits, find $R_a[0]$ and $R_a[\pm1]$, the PSD, its value at DC, and the frequency of its peak.

---

## Objective coverage

| Learning objective (chapter 17-01) | Problems |
|---|---|
| 1. Stationarity, means and correlations | 1, 3 |
| 2. Wiener–Khinchin, valid autocorrelations, band power | 1, 2, 4 |
| 3. LTI systems, cross-spectra, noise bandwidth | 5, 6, 7 |
| 4. Gaussian processes, sampling and noise folding | 8, 10, 11 |
| 5. PSD of PAM signals | 9, 12, 14 |
| 6. Bandpass noise and I/Q components | 13 |
