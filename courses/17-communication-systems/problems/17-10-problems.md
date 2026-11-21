# Problems 17-10 · OFDM

Chapter: [17-10](../chapters/17-10-ofdm.md) · Worked solutions: [17-10 solutions](../solutions/17-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $T$ is the useful symbol, $T_{CP}$ the cyclic prefix, $\Delta f = 1/T$, ε a frequency offset in units of $\Delta f$. NR timing follows TS 38.211 (normal CP $= 144/2048 \cdot T$). PAPR probabilities use the Nyquist-sample approximation $1 - (1 - e^{-\gamma})^N$ unless stated. Problems marked *(lab)* can be checked with the lab's `ofdm.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 17-10.1 [A]

**A misaligned window.** Two subcarriers one spacing apart are correlated over 0.9 of a symbol instead of a full symbol. Find the magnitude of their normalized correlation $\big|\int_0^{0.9T}e^{j2\pi t/T}dt\big|/(0.9T)$ and express it in dB. What is it over the full symbol?

### Problem 17-10.2 [A]

**A small OFDM system.** A 64-point FFT runs at 20 Msamples/s with a 0.8 μs guard interval. Find the subcarrier spacing, the useful symbol length and the fraction of airtime spent on the guard interval.

### Problem 17-10.3 [A]

**NR prefixes.** Find the NR normal cyclic prefix for μ = 2, and the excess path length the prefix covers for μ = 3.

### Problem 17-10.4 [B]

**The energy cost of a prefix.** Express the cyclic-prefix overhead as an $E_b/N_0$ penalty in dB for NR's normal prefix and for the 20% guard interval of Problem 17-10.2.

### Problem 17-10.5 [B]

**Oscillator accuracy.** For ICI below −35 dB with 30 kHz spacing, what is the largest residual frequency error ε, in hertz, and in parts per million of a 3.5 GHz carrier?

### Problem 17-10.6 [B]

**How fast at 28 GHz?** With 120 kHz spacing, what maximum Doppler keeps the Jakes-model ICI below −30 dB, and what speed is that at 28 GHz?

### Problem 17-10.7 [B]

**PAPR of a 256-subcarrier symbol.** Find the PAPR exceeded with probabilities $10^{-4}$ and $10^{-2}$.

### Problem 17-10.8 [B]

**FFT load.** A radix-2 FFT of size $N$ needs $(N/2)\log_2N$ complex multiplications. How many does a 4096-point FFT need per OFDM symbol, and per second per antenna at 30 kHz (28 000 symbols/s)?

### Problem 17-10.9 [B]

**A notched subcarrier.** *(lab)* At 20 dB SNR, one subcarrier has $|H_k|$ = 0.1. Find its SNR after zero-forcing and its QPSK symbol-error rate. Would MMSE equalization change the decision on this subcarrier?

### Problem 17-10.10 [B]

**A 20 MHz carrier's throughput.** A 20 MHz NR carrier at 15 kHz uses 106 resource blocks. With 64-QAM at code rate 0.75 and 14% overhead, find the information rate and spectral efficiency of one layer.

### Problem 17-10.11 [C]

**Prefix against the delay-spread distribution.** TR 38.901 models UMa NLOS delay spread as lognormal: $\log_{10}(\text{DS}/1\,\text{s})$ has mean $\mu_{lgDS} = -6.47 - 0.134\log_{10}f_c$ (with $f_c$ = 6 for carriers below 6 GHz) and standard deviation 0.39 (TR 38.901 V19.5.0, Table 7.5-6, [R-284](../../../reference/research-log.md#r-284--3gpp-tr-38901-delay-spread-parameters)). Assume the channel's maximum excess delay is about three times its rms delay spread. What fraction of links does a 30 kHz NR prefix cover? A 15 kHz prefix? What is the 99th-percentile delay spread?

### Problem 17-10.12 [B]

**The prefix as a frequency detector.** With a 4096-point FFT at 30 kHz, how many samples long is the normal cyclic prefix? A receiver correlates the prefix with the end of the symbol; the correlation's phase is $2\pi\varepsilon$. What range of ε can it measure without ambiguity?

### Problem 17-10.13 [B]

**Exact against approximate ICI.** Derive $P_{ICI} \approx (\pi\varepsilon)^2/3$ from the exact expression, then evaluate both for $N$ = 64 and ε = 0.2.

### Problem 17-10.14 [C]

**DFT-spread at full band.** Show that DFT-spread OFDM with the DFT size equal to the IFFT size transmits exactly the original single-carrier symbols at the sample instants. What is the Nyquist-sampled PAPR for QPSK?

### Problem 17-10.15 [B]

**Placing pilots.** An NR carrier at 3.5 GHz uses 30 kHz subcarriers (symbol with prefix 35.68 μs). The channel's maximum excess delay is 2 μs and users move at up to 120 km/h. (a) What is the largest pilot spacing in frequency, in hertz and in subcarriers? (b) The largest spacing in time, in seconds and in OFDM symbols? (c) A grid with a pilot every 12 subcarriers and every 7 symbols meets both. What fraction of resource elements does it use? (d) Why do real systems place pilots more densely than these limits?

---

## Objective coverage

| Learning objective (chapter 17-10) | Problems |
|---|---|
| 1. Orthogonality | 1, 14 |
| 2. Sizing: FFT, sampling, bandwidth | 2, 8, 10, 12 |
| 3. Cyclic prefix, one-tap equalization and numerology | 3, 4, 9, 11 |
| 4. Frequency offset and Doppler ICI | 5, 6, 12, 13 |
| 5. PAPR and DFT-spread OFDM | 7, 14 |
| 6. OFDMA, the resource grid and pilots | 10, 15 |
