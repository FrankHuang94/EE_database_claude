# Problems 11-06 · The Continuous-Time Fourier Transform

Chapter: [11-06](../chapters/11-06-continuous-time-fourier-transform.md) · Worked solutions: [11-06 solutions](../solutions/11-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $X(j\omega) = \int x(t)e^{-j\omega t}dt$; $X(f) = X(j2\pi f)$; $\operatorname{sinc}(u) = \sin(\pi u)/(\pi u)$; energies are normalized to 1 Ω.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 11-06.1 [A]

**Transforms from pairs and properties.** Find $X(j\omega)$, and the value asked for: (a) $e^{-3t}u(t - 2)$, and $\lvert X(0)\rvert$; (b) $e^{-2\lvert t\rvert}$, and $X(0)$; (c) $\cos(2\pi \cdot 1000t)\operatorname{rect}(t/0.01)$, and the peak of $\lvert X(f)\rvert$.

### Problem 11-06.2 [A]

**Inverse transforms.** Find $x(t)$: (a) $X = 1/(2 + j\omega)^2$, and the value and time of its peak; (b) $X = 2\pi\delta(\omega - 3) + 2\pi\delta(\omega + 3)$; (c) $X = \operatorname{rect}(\omega/2W)$.

### Problem 11-06.3 [A]

**Energy of a sinc.** Use Parseval to find the energy of $x(t) = \sin(Wt)/(\pi t)$ without integrating in time, and evaluate it for $W = 2\pi \times 1000$ rad/s.

### Problem 11-06.4 [B]

**Shorter pulses.** Compare a 1 V pulse of 10 ns with one of 1 ns: first nulls, energies, and the spectral magnitude at DC.

### Problem 11-06.5 [B]

**A triangle by convolution.** Two unit pulses of width $T$ convolve to a triangle. (a) Find the triangle's transform from the convolution theorem. (b) For $T$ = 1, give its value at $f = 0$ and $f = 0.5$. (c) How fast do its sidelobes decay, and why?

### Problem 11-06.6 [B]

**The energy of an impulse response.** Find the energy of the RC impulse response $h = \frac1\tau e^{-t/\tau}u(t)$ with τ = 1 ms, in the time domain and by Parseval.

### Problem 11-06.7 [B]

**An all-pass filter.** $H(j\omega) = (1 - j\omega\tau)/(1 + j\omega\tau)$ with τ = 1 µs. (a) Show that $\lvert H\rvert = 1$. (b) Find the phase and the group delay as functions of ω. (c) Evaluate the group delay at $\omega = 0$ and $\omega = 1/\tau$. (d) Does this filter distort pulses?

### Problem 11-06.8 [B]

**An ideal low-pass filter.** A filter passes $\lvert f\rvert < 1$ kHz exactly. (a) Find the peak of its impulse response and its first zero crossing. (b) Find the peak of its step response and when it occurs.

### Problem 11-06.9 [B]

**How wide is a pulse's spectrum?** For a 1 µs rectangular pulse, find the bandwidth containing 90% and 99% of the energy, and compare with the first-null bandwidth.

### Problem 11-06.10 [B]

**Choosing an oscilloscope.** (a) Estimate the rise time of a 2 GHz oscilloscope. (b) What does it display for a signal with a 300 ps rise time, and what is the error?

### Problem 11-06.11 [C]

**Time–bandwidth products.** (a) For $x = e^{-a\lvert t\rvert}$, find $\sigma_t$, $\sigma_\omega$ and their product, and compare with the Gaussian's $\tfrac12$. (b) Explain why the RMS bandwidth of a rectangular pulse, or of $e^{-at}u(t)$, is infinite.

### Problem 11-06.12 [C]

**Modulation.** A message band-limited to 5 kHz multiplies a 1 MHz carrier. (a) Sketch the spectrum and give the occupied band. (b) What bandwidth does the modulated signal need, and why is it double the message's?

### Problem 11-06.13 [C]

**A link budget at Nyquist.** A PCIe 6.0 channel may lose 32 dB at 16 GHz; a work-group presentation allocated 15.5 dB of it to the system board and quoted about 1 dB per inch of PCB at 16 GHz [R-141]. (a) Find the amplitude left at Nyquist for 32 dB. (b) About how long a board trace fits in 15.5 dB? (c) If the same bit rate were sent as NRZ, the Nyquist frequency would double. Assuming, for this estimate only, that board loss per inch is proportional to frequency, how long a trace would fit?

### Problem 11-06.14 [C]

**An ADC at another data rate.** The ADS1292R's sinc³ filter at 2 kSPS: (a) find its −3 dB bandwidth; (b) find its attenuation at 60 Hz; (c) a sinc filter notches every multiple of its output rate. What output rate would notch both 50 Hz and 60 Hz, and their harmonics?

---

## Objective coverage

| Learning objective (chapter 11-06) | Problems |
|---|---|
| 1. Transform as the limit of the series; existence; impulses in frequency | 2 |
| 2. Standard pairs | 1, 2, 3, 5 |
| 3. Properties | 1, 4, 5, 12 |
| 4. Frequency response, ideal filters, group delay | 7, 8 |
| 5. Energy, bandwidth definitions, rise time | 3, 6, 9, 10, 11 |
| 6. Frequency-domain specifications | 13, 14 |
