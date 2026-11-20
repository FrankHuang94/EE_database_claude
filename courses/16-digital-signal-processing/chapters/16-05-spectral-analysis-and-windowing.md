<!-- status: reviewed -->
# 16-05 · Spectral Analysis and Windowing

| | |
|---|---|
| **Course** | [16 · Digital Signal Processing](../README.md) |
| **University equivalent** | The spectral-analysis chapter of a senior DSP course: leakage and windows, resolution, the periodogram and its averaging, and the FFT-based dynamic testing of ADCs (Oppenheim & Schafer, *Discrete-Time Signal Processing*, ch. 10; Lyons, *Understanding Digital Signal Processing*, ch. 3 and 11; Harris, "On the use of windows" [1]) |
| **Prerequisites** | [16-04 The FFT Algorithm](16-04-the-fft.md), [16-03 The DFT and Its Properties](16-03-the-dft.md), [03-06 Random Processes Preview: Noise](../../03-probability-statistics-and-random-variables/chapters/03-06-random-processes-preview.md) |
| **Estimated study hours** | 7 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Explain leakage as convolution with the window's spectrum, and read a window's main-lobe width, sidelobe level and falloff from its DTFT.
2. Compute and use a window's figures of merit (coherent gain, equivalent noise bandwidth, scalloping loss, highest sidelobe) to correct amplitude and noise readings.
3. Choose a window and record length for a measurement, trading resolution against dynamic range and amplitude accuracy.
4. Relate a spectrum's noise floor to the signal's SNR through processing gain, and avoid reading the floor as the noise level.
5. Estimate a noise spectrum with the periodogram and with Welch averaging, and predict the estimate's variance.
6. Test an ADC with an FFT: choose a coherent input frequency, compute SNR, SINAD, THD, SFDR and ENOB, and check them against a time-domain sine fit.

---

## 1. Big picture

16-03 showed that a tone landing between DFT bins leaks into all of them. In practice almost every tone does: real signals are not synchronized to the analyzer's record. **Windowing** shapes the record so leakage falls off fast, at the price of wider peaks and some noise. Choosing a window, a record length and an averaging strategy is the craft of **spectral analysis**: seeing a weak tone beside a strong one, measuring an amplitude to a tenth of a decibel, or estimating a noise floor without fooling yourself. The same craft underlies the most common measurement in mixed-signal chip development, the FFT test of an ADC, whose results (SNR, SFDR, ENOB) fill the first page of every converter data sheet and many acquisition memos.

- **Instruments.** Spectrum and signal analyzers, FFT oscilloscopes and audio analyzers all window and average.
- **Converter test.** ADC and DAC characterization labs and production testers run coherent FFT tests on every part family.
- **Radar and communications.** Range–Doppler maps use windows to keep strong targets from masking weak ones; receivers estimate noise and interference spectra.
- **Condition monitoring and sensing.** Vibration analysis in factories and vehicles, and spectral features in wearables, start with windowed, averaged FFTs.

## 2. Intuition first

**Cutting a record cleanly.** A finite record is the true signal multiplied by a rectangular "gate" that is 1 inside the record and 0 outside. The abrupt edges are the problem: an abrupt edge has energy at all frequencies, so the gate smears every tone's spectrum into a long skirt of sidelobes. A window tapers the record smoothly to zero at both ends, like fading audio in and out instead of cutting it. The skirt drops away, but the taper also throws away some of the record's effective length, so peaks get wider and a little noisier.

**Analogy: a moving average of returns.** An analyst who estimates volatility from a hard 60-day window sees the estimate jump when a big day enters or leaves the window; an exponentially weighted window changes smoothly. Tapering trades responsiveness (resolution) for smoothness (low leakage). **Where it breaks:** a financial window weights the recent past more, which is one-sided; spectral windows are symmetric, because a spectrum has no "recent" end.

**The noise floor is not the noise.** An FFT spreads white noise over $N/2$ bins, so each bin holds only a small fraction of it, while a tone stays concentrated in one bin. The floor on the screen is therefore far below the total noise. A 12-bit ADC whose noise is 74 dB below its full-scale tone shows a floor about 110 dB down in an 8192-point FFT. Mistaking one for the other is the most common error in reading converter spectra (Example 16-05.4).

## 3. Theory

### 3.1 Leakage is convolution with the window

Let $x[n]$ be the signal and $w[n]$, $n = 0, \dots, N - 1$, the window. The analyzer transforms $x[n]w[n]$. Multiplication in time is (periodic) convolution in frequency (11-07), so

$$
\text{DTFT}\{xw\}(e^{j\omega}) = \frac1{2\pi}\int_{-\pi}^{\pi}X(e^{j\theta})\,W(e^{j(\omega - \theta)})\,d\theta .
$$

A tone $Ae^{j\omega_0n}$ has $X$ concentrated at $\omega_0$, so the windowed spectrum is $A\,W(e^{j(\omega - \omega_0)})$: a copy of the window's spectrum centred on the tone. Every property of the measurement is a property of $W$. For the rectangular window, $W(e^{j\omega})$ is the moving-average response of 16-01 §3.6 scaled by $N$: a main lobe of null-to-null width $4\pi/N$ (two bins) and sidelobes that start at −13.3 dB and fall only 6 dB per octave. The DFT samples this pattern at the bins (16-03 §3.2). If the tone sits exactly on a bin, all the other samples land on nulls and no leakage appears; otherwise the sidelobes appear in every bin.

### 3.2 Windows and their figures of merit

Practical windows are sums of cosines, $w[n] = \sum_k(-1)^ka_k\cos(2\pi kn/N)$, which taper to near zero at the ends: Hann ($a = 0.5, 0.5$), Hamming ($0.54, 0.46$), Blackman ($0.42, 0.5, 0.08$), the 4-term Blackman–Harris ($0.35875, 0.48829, 0.14128, 0.01168$) and the flat-top ($0.21557895, 0.41663158, 0.277263158, 0.083578947, 0.006947368$, SciPy's coefficients, from D'Antona and Ferrero), the 4-term Blackman–Harris and flat-top windows. For spectral analysis they are used in the periodic ("DFT-even") form, which is a symmetric window of length $N + 1$ with its last sample dropped [1]. Four numbers describe each window:

- **Coherent gain** $\text{CG} = \frac1N\sum w[n]$. A tone of amplitude $A$ exactly on a bin gives $\lvert X\rvert = AN\cdot\text{CG}/2$, so amplitude readings are divided by $N\cdot\text{CG}/2$.
- **Equivalent noise bandwidth** $\text{ENBW} = N\sum w^2/(\sum w)^2$ bins. White noise of variance $\sigma^2$ gives $E\lvert X[k]\rvert^2 = \sigma^2\sum w^2$ in every bin (because the noise samples are independent, the variances add, 03-04), while a tone's peak power scales as $(\sum w)^2$. Relative to the tone, each bin collects the noise in a bandwidth of ENBW bins, which is ENBW times the bin spacing in hertz. The rectangular window has the minimum, 1 bin; tapering raises it.
- **Scalloping loss** is the drop in the peak bin when the tone falls halfway between bins: $\lvert W(e^{j\pi/N})\rvert/\lvert W(1)\rvert$.
- **Highest sidelobe** and its **falloff rate** set how far below a strong tone a weak one can be seen.

Computed from these definitions for $N = 4096$ (the verify script recomputes them; Harris's paper [1] tabulates the same figures of merit for most of these and many other windows, though not for this flat-top variant):

| Window | CG | ENBW (bins) | Scalloping loss (dB) | Highest sidelobe (dB) |
|---|---|---|---|---|
| Rectangular | 1 | 1.000 | −3.92 | −13.3 |
| Hann | 0.5 | 1.500 | −1.42 | −31.5 |
| Hamming | 0.54 | 1.363 | −1.75 | −42.7 |
| Blackman | 0.42 | 1.727 | −1.10 | −58.1 |
| Blackman–Harris (4-term) | 0.3588 | 2.004 | −0.83 | −92.0 |
| Flat-top | 0.2156 | 3.770 | −0.01 | −93.0 |

![Window spectra in dB from 0 to 16 bins from the tone for four windows. The rectangular window has the narrowest main lobe, with its first null at 1 bin, and sidelobes starting near -13 dB and falling slowly to about -33 dB at 16 bins. Hann's first null is at 2 bins, its first sidelobe near -31 dB, and its sidelobes fall steeply to about -82 dB at 16 bins. Blackman's first null is at 3 bins and its sidelobes start near -58 dB. The 4-term Blackman-Harris window's first null is at 4 bins and its sidelobes stay below -92 dB.](../../../assets/figures/16-05/windows.svg)

*Figure 1. Window spectra: each step down in sidelobe level widens the main lobe by about one bin.*

The pattern is the tradeoff: lower sidelobes and flatter peaks cost wider main lobes (worse resolution) and larger ENBW (more noise per bin). Hamming cancels its first sidelobe but its sidelobes then fall slowly; Hann's fall at 18 dB per octave because the window and its derivative both reach zero at the ends.

### 3.3 Resolution and dynamic range

Two tones of equal size are resolved when their main lobes do not merge: roughly when they are separated by more than the window's −6 dB main-lobe width: **1.21** bins for the rectangular window and **2.00** for Hann. **Resolution is set by the record length $N$ and the window, not by zero padding** (16-03 §3.6): frequency resolution in hertz is a small multiple of $f_s/N$, the reciprocal of the record duration.

A weak tone beside a strong one is a different problem, one of **dynamic range**: the weak tone is visible only if it rises above the strong tone's sidelobes at its location. The rectangular window's −13 dB sidelobes falling at 6 dB per octave bury anything more than about 30 dB down a few bins away; Blackman–Harris pushes the skirt below −90 dB (Example 16-05.3). Spectrum analysis is the choice of where to sit on this curve for the signal at hand.

### 3.4 Noise in spectra: processing gain and the periodogram

**Processing gain.** For a real tone of power $A^2/2$ in white noise of total power $\sigma^2$ (an SNR of $A^2/2\sigma^2$), the tone's peak bin holds $(A\sum w/2)^2$ and each noise bin $\sigma^2\sum w^2$ on average. Their ratio is

$$
\frac{(A\sum w)^2/4}{\sigma^2\sum w^2} = \frac{A^2}{2\sigma^2}\cdot\frac{N}{2\,\text{ENBW}} ,
$$

so in decibels the floor sits $\text{SNR} + 10\log_{10}\bigl(N/(2\,\text{ENBW})\bigr)$ below the tone. The term $10\log_{10}(N/2)$ is the FFT's **processing gain**: longer records push the floor down without changing the SNR at all.

**The periodogram.** The estimate $\hat P[k] = \lvert X[k]\rvert^2/\sum w^2$ of the noise power per bin is unbiased (for white noise) but noisy: each bin is the squared magnitude of a complex Gaussian, an exponential random variable whose standard deviation equals its mean, **however long the record is**. A longer record gives more bins, not steadier ones. **Welch's method** cuts the record into $K$ segments (often overlapping by half), windows each, and averages their periodograms. For independent segments the standard deviation of each bin falls as $1/\sqrt K$ (03-05), at the price of $K$ times coarser resolution. Averaging is how analyzers show smooth noise floors.

> **Going deeper — the periodogram's bias and distribution, and the spectrogram.** For a WSS process with PSD $S(\omega)$, the expected windowed periodogram is not $S$ itself but $S$ smoothed by the window's spectral shape: $\mathbb{E}\hat P(\omega) = \frac{1}{2\pi\sum w^2}\int S(\theta)\lvert W(e^{j(\omega - \theta)})\rvert^2d\theta$ (the derivation is the Wiener–Khinchin argument of 17-01 §3.4 with a window). For white noise the smoothing changes nothing, hence the unbiased floor above; for a PSD with steep slopes, sidelobes leak power from strong regions into weak ones, which is the same leakage as for tones. Each bin of one Gaussian record is $\frac12S\chi^2_2$, an exponential variable, except at DC and $N/2$, where $X[k]$ is real for real data and the bin is $S\chi^2_1$, with a standard deviation $\sqrt2$ times its mean. Sliding a window along a long record and taking a DFT at each position gives the **short-time Fourier transform**; its magnitude squared plotted against time and frequency is the **spectrogram**, the standard display of chirps, hopping radios and speech. Its window length trades time resolution against frequency resolution exactly as §3.3 trades resolution against record length.

### 3.5 Testing an ADC with an FFT

An ADC is driven with a pure, nearly full-scale sine wave, a record of $N$ output codes is captured, and its spectrum is decomposed into the fundamental, its harmonics, and everything else.

**Coherent sampling.** Choose the input frequency so the record holds an integer number $M$ of cycles: $f_{in} = Mf_s/N$. The tone then falls exactly on bin $M$, all the other bins of its leakage pattern land on nulls, and the rectangular window (ENBW 1, no lost energy) can be used. $M$ is chosen odd and relatively prime to $N$ (for $N$ a power of 2, any odd $M$), so that the $N$ samples land at $N$ distinct phases of the sine and exercise many different codes, instead of repeating a short pattern. The harmonics of an on-bin tone are also on bins (aliased into $0..N/2$ if needed), which makes their powers easy to collect.

**The figures of merit**, all in dB relative to the fundamental's power:

- **SNR**: fundamental over noise, excluding DC and the first several harmonics.
- **THD** (total harmonic distortion): harmonics (usually the 2nd to the 5th or more) over fundamental.
- **SINAD**: fundamental over noise *and* distortion: everything except DC and the fundamental.
- **SFDR** (spurious-free dynamic range): fundamental over the largest other spectral component, harmonic or not.
- **ENOB** (effective number of bits): the resolution of an ideal converter with the same SINAD.

**Where 6.02B + 1.76 comes from.** An ideal $B$-bit quantizer with step $q$ adds error that is close to uniform on $\pm q/2$, with variance $q^2/12$ (03-03). A full-scale sine spans $2^Bq$ peak to peak, so its amplitude is $2^{B-1}q$ and its power $2^{2B}q^2/8$. Their ratio is

$$
\text{SNR}_{ideal} = 10\log_{10}\frac{2^{2B}q^2/8}{q^2/12} = 10\log_{10}\left(1.5\cdot2^{2B}\right) = 6.02B + 1.76\ \text{dB} ,
$$

and inverting it defines $\text{ENOB} = (\text{SINAD} - 1.76)/6.02$. Two caveats follow from the derivation. The formula assumes a *full-scale* input: a test at −1 dBFS gives an ENOB about 1/6 bit lower unless the SINAD is referred to full scale (dBFS). The IEEE 1241 definition corrects for the test amplitude, and converter data sheets quote SINAD in dBFS and compute ENOB from it (R-237). And 16-10 revisits the uniform-noise assumption.

## 4. Worked examples

### Example 16-05.1 · What does one bin hold? (tier A)

**Setup.** A 4096-point FFT at $f_s$ = 1 MHz with a Hann window. Find the bin spacing, the equivalent noise bandwidth in hertz, and how much more white noise each bin collects than with a rectangular window.

**Solution.** Bin spacing $f_s/N = 10^6/4096$ = **244.1** Hz. ENBW = 1.5 bins, so each bin measures noise in **366.2** Hz. Relative to the tone, in an amplitude-calibrated spectrum, the per-bin noise rises by $10\log_{10}1.5$ = **1.76** dB compared with the rectangular window (ENBW 1 bin).

**Units check.** Bins × Hz per bin = Hz.

**Sanity check.** The Hann window's coherent gain of 0.5 lowers the tone's peak by **6.02** dB and its $\sum w^2/N$ = **0.375** lowers the noise per bin by **4.26** dB; the difference is the 1.76 dB loss in tone-to-noise ratio.

### Example 16-05.2 · Reading an amplitude off a spectrum (tier B)

**Setup.** A 1024-point FFT of a unit-amplitude cosine. (a) With a Hann window and the tone exactly on a bin, what is the peak $\lvert X\rvert$, and how is it converted back to amplitude? (b) With the tone halfway between bins, what amplitude error do the rectangular, Hann, Blackman–Harris and flat-top windows make?

**Solution.** (a) $\lvert X\rvert = AN\cdot\text{CG}/2 = 1 \times 1024 \times 0.5/2$ = **256**, so amplitude = $\lvert X\rvert/(N\cdot\text{CG}/2) = \lvert X\rvert/256$.

(b) The scalloping losses: rectangular **−3.92** dB (an amplitude reading **36**% low), Hann **−1.42** dB, Blackman–Harris −0.83 dB, flat-top **−0.01** dB. That is why spectrum analyzers offer a flat-top window for amplitude accuracy, and why their peaks look broad in that mode (ENBW 3.77 bins).

**Units check.** $\lvert X\rvert$ in the units of $x$ times samples.

**Sanity check.** $20\log_{10}(1 - 0.36) = -3.9$ dB.

### Example 16-05.3 · A weak tone beside a strong one (tier B)

**Setup.** A 1024-point record holds a unit tone at bin 100.5 and a tone 60 dB weaker (amplitude $10^{-3}$) exactly on bin 110. For rectangular, Hann and 4-term Blackman–Harris windows, compare the strong tone's leakage at bin 110 with the weak tone's peak there (both relative to the strong tone's peak bin). Which windows reveal the weak tone?

**Solution.** Computing the windowed DFTs:

| Window | Strong tone's leakage at bin 110 | Weak tone's peak | Margin |
|---|---|---|---|
| Rectangular | **−25.3** dB | −56.1 dB | buried by 31 dB |
| Hann | **−67.1** dB | −58.6 dB | visible, 8.5 dB above |
| Blackman–Harris | **−96.2** dB | −59.2 dB | visible, 37 dB above |

The rectangular window's sidelobes, falling only as $1/(\pi\cdot\text{bins})$, bury a −60 dB tone 9.5 bins away; Hann's fast falloff just reveals it; Blackman–Harris leaves a wide margin. (The weak tone's own level differs slightly between windows because the strong tone's peak, the reference, scallops differently.)

**Units check.** dB relative to the strong tone's peak bin.

**Sanity check.** The rectangular sidelobe estimate $1/(\pi \times 9.5)$ is **−29.5** dB; the exact value differs because both the strong tone's peak and its leakage are sampled off-centre.

### Example 16-05.4 · The noise floor is not the SNR (tier B)

**Setup.** An ideal 12-bit ADC digitizes a full-scale sine coherently, and the analyst takes an 8192-point FFT. (a) What is the ideal SNR? (b) How far below the tone does the average noise floor sit with a rectangular window, and with Hann? (c) Compare with a simulation.

**Solution.** (a) $6.02 \times 12 + 1.76$ = **74.0** dB.

(b) Rectangular: $74.0 + 10\log_{10}(8192/2)$ = **110.1** dB below the tone. Hann: $74.0 + 10\log_{10}(8192/(2 \times 1.5))$ = **108.4** dB. A reader who takes the floor (about −110 dBFS) as the noise level overstates the SNR by **36.1** dB.

(c) Quantizing a full-scale sine at bin 999 of 8192 to 12 bits and computing the spectrum gives SNR **73.9** dB and an average floor **110.0** dB below the tone, as predicted.

**Units check.** All in dB relative to the tone.

**Sanity check.** Each doubling of $N$ lowers the floor by 3 dB and leaves the SNR unchanged.

### Example 16-05.5 · A coherent ADC test (tier C)

**Setup.** A 12-bit ADC sampling at 100 MS/s is tested with $N$ = 16,384 samples near 10 MHz at −1 dBFS. (a) Choose a coherent input frequency. (b) Its output is simulated as the 12-bit quantized value of the input after a small 2nd- and 3rd-order nonlinearity (designed for −90 and −80 dBc) and Gaussian thermal noise of standard deviation $2 \times 10^{-4}$ (full scale is ±1, so this is **0.41** LSB). From the FFT compute SNR, SINAD, THD, SFDR and ENOB. (c) Check SINAD with a time-domain sine fit, and give ENOB referred to full scale.

**Solution.** (a) $10\text{ MHz} \times 16{,}384/100\text{ MHz} = 1638.4$ cycles; the nearest odd integer is 1639 ($= 11 \times 149$, relatively prime to 16,384 like every odd number), but we take the nearest prime, $M$ = **1637**, the stricter choice some test notes recommend (R-237); either is coherent, so $f_{in} = 1637 \times 100\text{ MHz}/16{,}384$ = **9.99146** MHz.

(b) From the rectangular-window FFT, with harmonics 2 to 5 collected at their (aliased) bins 3274, 4911, 6548 and 8185:

| Metric | Value |
|---|---|
| SNR | **68.15** dB |
| SINAD | **67.85** dB |
| THD | **−79.60** dB |
| SFDR | **79.97** dB |
| ENOB | **10.98** bits |

The SNR matches the expected $20\log_{10}\bigl[(A/\sqrt2)/\sqrt{\sigma_t^2 + q^2/12}\bigr]$ = **68.22** dB for thermal noise $\sigma_t$ and quantization step $q$; the THD is set by the 3rd harmonic near −80 dBc.

(c) A least-squares fit of $a\cos + b\sin + c$ at the known frequency leaves a residual whose rms, compared with the fitted amplitude's rms, gives SINAD = **67.85** dB, the same as the FFT: everything that is not the fitted sine is noise and distortion, counted in the time domain. Referred to full scale, $\text{ENOB}_{FS} = (67.854 + 1 - 1.76)/6.02$ = **11.15** bits; the **0.17**-bit difference is purely the −1 dBFS test level. A data sheet would report the full-scale-referred 11.15 bits, the convention of IEEE 1241 and of manufacturers' tables (R-237).

![Spectrum of the simulated ADC test in dBFS from 0 to 50 MHz: a fundamental at about -1 dBFS near 10 MHz, a second harmonic near -91 dBFS at 20 MHz, a third harmonic near -81 dBFS at 30 MHz, the 4th and 5th harmonics lost in the noise near 40 and 50 MHz, a small DC component near -84 dBFS from the second-order nonlinearity, and a noise floor between about -100 and -130 dBFS.](../../../assets/figures/16-05/adc-spectrum.svg)

*Figure 2. The coherent ADC test of Example 16-05.5. The floor sits about 107 dB below the fundamental, yet the SNR is 68 dB: processing gain, not converter quality.*

**Units check.** dB and bits.

**Sanity check.** SINAD can never exceed SNR or −THD; here it is within **0.30** dB of the SNR because noise dominates the distortion by **11.4** dB.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Txt 16-05.a | rectangular ENBW | 1.000 | bins |
| Txt 16-05.b | Hann ENBW | 1.500 | bins |
| Txt 16-05.c | Hamming ENBW | 1.363 | bins |
| Txt 16-05.d | Blackman ENBW | 1.727 | bins |
| Txt 16-05.e | Blackman–Harris ENBW | 2.004 | bins |
| Txt 16-05.f | flat-top ENBW | 3.770 | bins |
| Txt 16-05.g | rectangular scalloping | −3.92 | dB |
| Txt 16-05.h | Hann scalloping | −1.42 | dB |
| Txt 16-05.i | Hamming scalloping | −1.75 | dB |
| Txt 16-05.j | Blackman scalloping | −1.10 | dB |
| Txt 16-05.k | Blackman–Harris scalloping | −0.83 | dB |
| Txt 16-05.l | flat-top scalloping | −0.01 | dB |
| Txt 16-05.m | rectangular sidelobe | −13.3 | dB |
| Txt 16-05.n | Hann sidelobe | −31.5 | dB |
| Txt 16-05.o | Hamming sidelobe | −42.7 | dB |
| Txt 16-05.p | Blackman sidelobe | −58.1 | dB |
| Txt 16-05.q | Blackman–Harris sidelobe | −92.0 | dB |
| Txt 16-05.r | flat-top sidelobe | −93.0 | dB |
| Txt 16-05.s | Blackman–Harris coherent gain | 0.3588 | — |
| Txt 16-05.t | flat-top coherent gain | 0.2156 | — |
| Ex 16-05.1a | bin spacing | 244.1 | Hz |
| Ex 16-05.1b | Hann noise bandwidth | 366.2 | Hz |
| Ex 16-05.1c | extra noise per bin | 1.76 | dB |
| Ex 16-05.2a | Hann on-bin peak | 256 | — |
| Ex 16-05.2b | rectangular half-bin loss | −3.92 | dB |
| Ex 16-05.2c | Hann half-bin loss | −1.42 | dB |
| Ex 16-05.2d | flat-top half-bin loss | −0.01 | dB |
| Ex 16-05.3a | rectangular leakage at bin 110 | −25.3 | dB |
| Ex 16-05.3b | Hann leakage at bin 110 | −67.1 | dB |
| Ex 16-05.3c | Blackman–Harris leakage at bin 110 | −96.2 | dB |
| Ex 16-05.3d | weak tone, rectangular | −56.1 | dB |
| Ex 16-05.3e | weak tone, Hann | −58.6 | dB |
| Ex 16-05.3f | weak tone, Blackman–Harris | −59.2 | dB |
| Ex 16-05.4a | ideal 12-bit SNR | 74.0 | dB |
| Ex 16-05.4b | floor below tone, rectangular | 110.1 | dB |
| Ex 16-05.4c | floor below tone, Hann | 108.4 | dB |
| Ex 16-05.4d | simulated SNR | 73.9 | dB |
| Ex 16-05.4e | simulated floor below tone | 110.0 | dB |
| Ex 16-05.5a | coherent cycles M | 1637 | — |
| Ex 16-05.5b | input frequency | 9.99146 | MHz |
| Ex 16-05.5c | SNR | 68.15 | dB |
| Ex 16-05.5d | SINAD | 67.85 | dB |
| Ex 16-05.5e | THD | −79.60 | dB |
| Ex 16-05.5f | SFDR | 79.97 | dB |
| Ex 16-05.5g | ENOB | 10.98 | bits |
| Ex 16-05.5h | expected SNR | 68.22 | dB |
| Ex 16-05.5i | sine-fit SINAD | 67.85 | dB |
| Ex 16-05.5j | full-scale-referred ENOB | 11.15 | bits |
| Ex 16-05.5k | thermal noise in LSB | 0.41 | LSB |
| Ex 16-05.5l | ENOB difference from the test level | 0.17 | bits |
| Ex 16-05.5m | SNR minus SINAD | 0.30 | dB |
| Ex 16-05.5n | noise above distortion | 11.4 | dB |
| Ex 16-05.1d | Hann tone-peak drop | 6.02 | dB |
| Ex 16-05.1e | Hann mean square of the window | 0.375 | — |
| Ex 16-05.1f | Hann noise-per-bin drop | 4.26 | dB |
| Ex 16-05.2e | rectangular half-bin amplitude shortfall | 36 | % |
| Ex 16-05.3g | rectangular sidelobe estimate | −29.5 | dB |
| Ex 16-05.4f | SNR overstatement | 36.1 | dB |
| Txt 16-05.u | rectangular −6 dB main-lobe width | 1.21 | bins |
| Txt 16-05.v | Hann −6 dB main-lobe width | 2.00 | bins |
| Txt 16-05.w | Q2 amplitude | 1 | — |
| Txt 16-05.x | Q4 ideal 16-bit SNR | 98.1 | dB |
| Txt 16-05.y | Q4 processing gain | 45.2 | dB |
| Txt 16-05.z | Q4 floor depth | 143.2 | dB |
| Txt 16-05.aa | Q6 coherent bin | 409 | — |
| Txt 16-05.ab | Q6 input frequency | 99.854 | kHz |
| Txt 16-05.ac | ENOB from the ADC12DJ5200RF's SINAD | 8.76 | bits |

## 5. Simulate it

The lab, [labs/16-05-lab](../labs/16-05-lab/README.md), provides `spectral.py`: the six windows of §3.2 with their figures of merit computed from the definitions, the periodogram, Welch averaging, a coherent-frequency chooser, ADC metrics from a coherent FFT, and a three-parameter sine fit. You:

1. **Compare windows**: plot each window's spectrum in dB and reproduce the table of §3.2.
2. **Hunt a weak tone** (Example 16-05.3) and find the weakest tone each window reveals 10 bins from a strong one.
3. **Watch processing gain**: quantize a sine to 12 bits and plot the spectrum for $N$ = 1024 to 65,536; the floor drops 3 dB per doubling while the SNR stays at 74 dB.
4. **Average a noise spectrum**: compare a single periodogram with Welch averages of 4, 16 and 64 segments, and measure the standard deviation of the estimate.
5. **Test an ADC** (Example 16-05.5): choose $M$, simulate the converter, compute the metrics from the FFT and SINAD from the sine fit, then break coherence (use $M + 0.3$ cycles) and see the metrics collapse with a rectangular window and recover with Blackman–Harris.

**Guided exercise (predict, then run).** **Before Part 4,** predict the ratio of standard deviation to mean of a single periodogram bin for white noise, and after averaging 16 segments. (1 for a single periodogram; about $1/\sqrt{16} = 0.25$ after averaging, a little more with 50% overlap because neighbouring segments are correlated.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Record length $N$ | Resolution ($\approx f_s/N$); lower floor (processing gain) | Capture time, memory, latency | Test or algorithm engineer |
| Window with lower sidelobes | Dynamic range near strong tones | Wider main lobe (resolution); higher ENBW (noise per bin) | Measurement engineer |
| Flat-top window | Amplitude accuracy (< 0.01 dB scalloping) | Very wide peaks (ENBW 3.8 bins) | Instrument user |
| Averaging ($K$ segments) | Variance of noise estimates falls as $1/K$ | $K$ times coarser resolution, or $K$ times longer capture | Test engineer |
| Coherent sampling | No leakage with the rectangular window; exact bins for harmonics | Requires a synthesizer locked to the ADC clock | Converter test engineer |
| Number of harmonics in THD | More complete distortion figure | Risk of counting noise bins as harmonics | Test engineer, data-sheet author |

## 7. Numbers to know

| Quantity | Value | Source |
|---|---|---|
| Rectangular window | ENBW 1 bin, −13.3 dB sidelobes, −3.92 dB worst scalloping | §3.2 |
| Hann window | CG 0.5, ENBW 1.5 bins, −31.5 dB sidelobes, −1.42 dB scalloping | §3.2 [1] |
| 4-term Blackman–Harris | ENBW 2.0 bins, −92 dB sidelobes | §3.2 [1] |
| Ideal ADC SNR | $6.02B + 1.76$ dB (74.0 dB at 12 bits, 98.1 dB at 16 bits) | §3.5 |
| FFT processing gain | $10\log_{10}(N/2)$ dB (rectangular) | §3.4 |
| Periodogram bin | standard deviation equal to the mean; $1/\sqrt K$ with $K$ averages | §3.4 |
| ENOB | $(\text{SINAD} - 1.76)/6.02$ for a full-scale test | §3.5 |

## 8. Common mistakes

- **Reading the FFT noise floor as the noise level.** Add the processing gain back: SNR = floor depth − $10\log_{10}(N/(2\,\text{ENBW}))$.
- **Reading amplitudes without correcting for coherent gain** (or reading off-bin tones without accounting for scalloping).
- **Using a rectangular window on a non-coherent record** and mistaking leakage for noise or spurs.
- **Expecting zero padding or a longer FFT of the same data to resolve close tones.**
- **Comparing noise spectra from different windows** without normalizing by ENBW.
- **Trusting a single periodogram's fine structure.** Its bins scatter by 100%; average first.
- **Quoting ENOB from a −1 dBFS test as if it were full-scale,** or quoting SNR that silently excludes harmonics that were counted elsewhere.
- **Choosing $M$ with a common factor with $N$**, so the record repeats a short code pattern and the noise appears as spurs.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Converter data sheets are FFT measurements.** Every ADC data sheet's dynamic table (SNR, SFDR, SINAD, ENOB, often at several input frequencies and levels) comes from coherent FFT tests of the kind in Example 16-05.5, under the terminology and test methods of IEEE Std 1241 (current edition 1241-2023, published October 2023) **[Established]**. Manufacturers' notes prescribe exactly this chapter's recipe: bin-centred (coherent) inputs with a prime or odd number of cycles, no window for coherent captures and Blackman–Harris for non-coherent ones (TI SLVAG04, 2025; Renesas AN9675) (R-237) **[Established]**.
- **What a data sheet line means.** TI's ADC12DJ5200RF (12-bit, 5.2 GS/s per channel) lists, at a 347 MHz input of −1 dBFS sampled at 5.12 GS/s, SNR 55.6 dBFS, SINAD 54.5 dBFS, ENOB 8.8 bits and SFDR 65 dBFS, with SNR "excluding DC, HD2 to HD9, fS / 2, fS / 2 – fIN" (R-237) **[Established]**. The ENOB follows from the full-scale-referred SINAD, $(54.5 - 1.76)/6.02$ = **8.76** bits, and the 12-bit converter delivers under 9 effective bits. Neither jitter nor distortion explains that at 347 MHz: the data sheet's SINAD at −12 dBFS is the same 56.1 dBFS at 347, 997 and 2397 MHz, its aperture jitter (50 to 60 fs rms) would limit the SNR only near 78 dB at 347 MHz, and SNR and SINAD differ by only 1.1 dB. The limit is the converter's own input-independent noise (front-end, sampler and comparator noise; its noise spectral density is −152.0 dBFS/Hz in the 1.0 Vpp full-scale setting), not the 12-bit quantizer. Jitter and distortion take over only at multi-gigahertz inputs: SINAD at −1 dBFS falls to 46.2 dBFS at 8 GHz (R-237) **[Established]**.
- **Spectrum analyzers expose the window as "RBW".** Swept and FFT-based analyzers specify a resolution bandwidth and, for noise, normalize to 1 Hz using the filter's or window's noise bandwidth: the ENBW of §3.2 under another name **[Established; textbook]**.
- **Radar and sonar use windows on every axis.** Range, Doppler and angle FFTs are windowed (Taylor and Chebyshev windows are common, designed for a target sidelobe level) so that strong reflectors do not mask weak ones **[Established; textbook]**.

### Why it matters commercially

Converter performance is sold in decibels and bits, and those numbers are only as good as the test that produced them. A start-up's "14-bit ENOB" might be measured at a low input frequency, at a level chosen to flatter, with a window and harmonic count that make SNR look better, or as a full-scale-referred value. Knowing how the FFT test works lets a diligence team, or a customer's engineers, ask for the conditions and convert claims to a common basis. The same literacy applies to sensor front ends, RF receivers and audio codecs, whose noise and spur specifications all come from windowed, averaged FFTs.

### Marketing vs Reality

- **"−150 dB noise floor."** A floor depth depends on $N$ and the window; without them it says nothing about SNR. Ask for SNR over a stated bandwidth.
- **"ENOB of 12 bits"** measured at low frequency and quoted next to a high sample rate: ENOB falls with input frequency (clock jitter and front-end distortion). Ask for ENOB at the frequencies the application uses.
- **Front page versus table.** Even one data sheet can disagree with itself: the ADC12DJ5200RF's front page states 8.6 bits of ENOB at 2.4 GHz, while its table gives a typical of 8.7 at 2397 MHz (R-237). Read the table and its conditions, not the summary.
- **"SFDR of 90 dB"** that excludes some spurs (interleaving spurs or the second harmonic) "by definition". Ask which components were excluded.
- **"Full-scale-referred"** figures (dBFS) read as if they were carrier-referred (dBc), or the reverse; 1 dB of test level is 0.17 bit of ENOB.

### Questions for engineering leaders

1. **"At what input frequency, level, record length and window was this ENOB measured?"** *Strong:* gives all four and shows a curve versus frequency. *Evasive:* gives a single number.
2. **"Are your SNR and THD carrier-referred or full-scale-referred, and how many harmonics are in THD?"** *Strong:* states the convention and the harmonic count. *Evasive:* "industry standard".
3. **"How do you know the test is coherent and the source is cleaner than the converter?"** *Strong:* describes the locked synthesizer, the filtering of the test tone, and a check with a sine fit. *Evasive:* relies on the window to hide leakage.
4. **"What does the spectrum look like averaged, and how many averages?"** *Strong:* shows averaged spectra and knows the residual scatter. *Evasive:* single captures only.
5. **"How does the noise floor in your plots translate to SNR?"** *Strong:* subtracts the processing gain and the window's ENBW explicitly. *Evasive:* quotes the floor.

## 10. Concept check

**Q1.** Why does a tone exactly on a bin show no leakage with a rectangular window?

<details><summary>Answer</summary>

The window's spectrum is centred on the tone, and the DFT samples it at the bins; when the tone is on a bin, all the other bins fall on nulls of the rectangular window's spectrum (the moving-average nulls of 16-01).

</details>

**Q2.** A Hann-windowed 2048-point FFT shows a peak of 512 for a cosine on a bin. What is the cosine's amplitude?

<details><summary>Answer</summary>

$A = \lvert X\rvert/(N\cdot\text{CG}/2) = 512/(2048 \times 0.5/2)$ = 1.

</details>

**Q3.** Why does tapering a window raise its equivalent noise bandwidth?

<details><summary>Answer</summary>

ENBW = $N\sum w^2/(\sum w)^2$, which is 1 only when all weights are equal (by the Cauchy–Schwarz inequality, $(\sum w)^2 \le N\sum w^2$). Tapering makes the weights unequal, so the tone (which adds coherently, as $(\sum w)^2$) loses more than the noise (which adds in power, as $\sum w^2$).

</details>

**Q4.** An ideal 16-bit ADC is measured with a 65,536-point FFT and a rectangular window. How far below the full-scale tone is the average noise floor?

<details><summary>Answer</summary>

$6.02 \times 16 + 1.76 = 98.09$ dB SNR plus $10\log_{10}(32{,}768) = 45.15$ dB processing gain: 143.2 dB.

</details>

**Q5.** A single periodogram of white noise has bins that scatter as much as their mean. Will a 16 times longer record fix that?

<details><summary>Answer</summary>

No: it gives 16 times more bins, each as scattered as before. Averaging 16 periodograms of shorter segments (Welch) reduces the scatter to about a quarter, at the cost of resolution.

</details>

**Q6.** For $N$ = 4096 and $f_s$ = 1 MS/s, which coherent bin is nearest a 100 kHz input, and what is the exact input frequency?

<details><summary>Answer</summary>

$100 \times 4096/1000 = 409.6$; the nearest odd bin is $M$ = 409, so $f_{in} = 409 \times 10^6/4096$ = 99.854 kHz.

</details>

Practice: [Problems 16-05](../problems/16-05-problems.md) · [Solutions](../solutions/16-05-solutions.md)

## 11. Key terms

[Window function](../../../reference/glossary.md#window-function) · [Spectral leakage](../../../reference/glossary.md#spectral-leakage) · [Coherent gain](../../../reference/glossary.md#coherent-gain) · [Equivalent noise bandwidth (ENBW)](../../../reference/glossary.md#equivalent-noise-bandwidth-enbw) · [Scalloping loss](../../../reference/glossary.md#scalloping-loss) · [Processing gain](../../../reference/glossary.md#processing-gain) · [Periodogram](../../../reference/glossary.md#periodogram) · [Welch's method](../../../reference/glossary.md#welchs-method) · [Coherent sampling](../../../reference/glossary.md#coherent-sampling) · [SINAD](../../../reference/glossary.md#sinad) · [Spurious-free dynamic range (SFDR)](../../../reference/glossary.md#spurious-free-dynamic-range-sfdr) · [Effective number of bits (ENOB)](../../../reference/glossary.md#effective-number-of-bits-enob)

## 12. Connections

- **Builds on:** [16-03](16-03-the-dft.md) (bins, leakage, zero padding), [16-04](16-04-the-fft.md), [03-04](../../03-probability-statistics-and-random-variables/chapters/03-04-joint-distributions-and-clt.md) and [03-06](../../03-probability-statistics-and-random-variables/chapters/03-06-random-processes-preview.md) (variances add; white noise).
- **Next:** [16-06 FIR Filter Design](16-06-fir-filter-design.md) uses the same windows to design filters.
- **Used later:** quantization noise and $6.02N + 1.76$ in [16-10](16-10-quantization-and-fixed-point.md); converter testing in the data-converter chapters; radar and receiver measurements in Course 17.

## 13. Further study

- F. J. Harris, "On the use of windows for harmonic analysis with the discrete Fourier transform" [1], the standard reference on windows and their figures of merit.
- Oppenheim & Schafer, *Discrete-Time Signal Processing*, 3rd ed., ch. 10 (Fourier analysis of signals using the DFT, periodogram, averaging).
- Lyons, *Understanding Digital Signal Processing*, 3rd ed., ch. 3 (leakage, windows) and ch. 11 (signal averaging).

## 14. Sources

1. F. J. Harris, "On the use of windows for harmonic analysis with the discrete Fourier transform", *Proceedings of the IEEE* 66(1), 51–83, January 1978.
2. A. V. Oppenheim and R. W. Schafer, *Discrete-Time Signal Processing*, 3rd ed., Pearson, 2010, ch. 10.
3. R. G. Lyons, *Understanding Digital Signal Processing*, 3rd ed., Prentice Hall, 2011.
4. IEEE Std 1241-2023, *Standard for Terminology and Test Methods for Analog-to-Digital Converters* (status from the IEEE SA page); TI SLYW038D (*Analog Engineer's Pocket Reference*), SLVAG04 (coherent sampling, 2025) and the ADC12DJ5200RF data sheet SLVSEN9H; Renesas AN9675; Rohde & Schwarz 1ER03_1e (ENOB per IEEE 1241-2010, second-hand). Research log [R-237].
