# Solutions 03-06 · Random Processes Preview: Noise

Problems: [03-06 problems](../problems/03-06-problems.md) · Chapter: [03-06](../chapters/03-06-random-processes-preview.md)

Every numerical answer below is listed in the answer key at the end and is recomputed by [verify_03_06.py](../verify/verify_03_06.py).

---

## Solutions

### Solution 03-06.1

(a) $\mu_X(t) = \frac{1}{\pi}\int_0^\pi A\cos(\omega t + \theta)\,d\theta = \frac{A}{\pi}\big[\sin(\omega t + \pi) - \sin\omega t\big] = -\frac{2A}{\pi}\sin\omega t$.

(b) No: the mean varies with time. Restricting the phase to half a cycle makes some parts of the waveform systematically more likely.

(c) At $\omega t = \pi/2$: $-2/\pi = $ **−0.6366 V**.

### Solution 03-06.2

(a) $R_X(0) = 4 + 1 = $ **5 V²**.

(b) As τ → ∞ the correlated part dies away and $R_X \to \mu^2 = 1$ V²: DC power **1 V²**, so the mean is +1 V or −1 V (the autocorrelation cannot tell the sign).

(c) AC power $5 - 1 = $ **4 V²**.

(d) The autocovariance is $4e^{-|\tau|/\tau_c}$, so the correlation coefficient at τ_c is $e^{-1} = $ **0.3679**.

### Solution 03-06.3

(a) To that sensor's own offset (plus a negligible residual from the white noise): the process is not ergodic across units.

(b) $1.96/\sqrt{2(n - 1)} \le 0.1$ gives $n - 1 \ge 192.07$, so **194** sensors.

(c) 100 sensors for one hour: they sample the population's offsets. One sensor for 100 hours only measures its own offset ever more precisely.

### Solution 03-06.4

(a) $\sqrt{4kTR} = \sqrt{4\times1.380649\times10^{-23}\times290\times50} = $ **0.8949 nV/√Hz**.

(b) $0.8949\text{ nV}\times\sqrt{10^6} = $ **0.8949 µV** and $\times\sqrt{10^9} = $ **28.30 µV**.

(c) $kT_0B$: $4.004\times10^{-15}$ W in 1 MHz, or **−113.98 dBm**, and **−83.98 dBm** in 1 GHz.

### Solution 03-06.5

(a) $-173.98 + 10\log_{10}(2\times10^6) + 2 = -173.98 + 63.01 + 2 = $ **−108.96 dBm**.

(b) $-108.96 + 6 = $ **−102.96 dBm**.

(c) Time or bandwidth. Correlating against a known code or averaging over many symbols collects signal energy coherently while noise adds incoherently, a "processing gain" (Course 17). The cost is a lower data rate for the same bandwidth, or a longer acquisition.

### Solution 03-06.6

(a) $\Delta = 1/4096$ V, so $\Delta/\sqrt{12} = $ **70.48 µV**, and $kT/C \le (70.48\text{ µV})^2$ gives $C \ge 4.142\times10^{-21}/4.967\times10^{-9} = $ **0.8339 pF**.

(b) $\Delta = 1/65{,}536$ V, so **4.405 µV**, and $C \ge $ **213.5 pF**.

Each extra bit halves Δ and so quadruples the required capacitance: four bits cost 256 times the capacitance, with the area and drive power that go with it. That is why high-resolution converters are large and power-hungry.

### Solution 03-06.7

$B_N = (\pi/2)\times10$ kHz $= $ **15.71 kHz**, and the output noise is $10\text{ nV}\times\sqrt{15{,}708} = $ **1.253 µV** rms.

### Solution 03-06.8

$\sqrt{2qIB} = \sqrt{2\times1.602\times10^{-19}\times10^{-5}\times10^8} = $ **17.90 nA** rms. The ratio $10\ \mu\text{A}/17.90\text{ nA} = 558.6$, or **54.94 dB**. A hundredfold smaller current than Example 03-06.5 loses 10 dB of ratio in a tenfold smaller bandwidth: the ratio scales as $\sqrt{I/B}$.

### Solution 03-06.9

(a) The source contributes $(0.8949\text{ nV})^2$, the voltage noise $(1\text{ nV})^2$, and the current noise flowing in the source resistance $(2\text{ pA}\times50\ \Omega)^2 = (0.1\text{ nV})^2$, all per hertz. Total: $\sqrt{0.8009 + 1 + 0.01}$ nV/√Hz $= $ **1.346 nV/√Hz**.

(b) $F = 1.8109/0.8009 = $ **2.261**, so NF = **3.544 dB**. The amplifier's own voltage noise, larger than the source's, dominates; with a 50 Ω source, low voltage noise matters far more than low current noise.

### Solution 03-06.10

(a) $\sigma_{\text{avg}} \approx 2\text{ mV}\times\sqrt{2\times0.01/10} = $ **89.44 µV**.

(b) $N_{\text{eff}} = 10/(2\times0.01) = $ **500**.

(c) $2\text{ mV}/\sqrt{10^4} = $ **20 µV**, 4.5 times too optimistic.

### Solution 03-06.11

(a) $f_c = 1/(2\pi\times10^{-3}) = $ **159.2 Hz**.

(b) $G(0) = 4\sigma^2\tau_c = 4\times10^{-6}\times10^{-3} = 4\times10^{-9}$ V²/Hz, or **63.25 µV/√Hz**.

(c) $\int_0^{f_c}G\,df = \sigma^2\cdot\frac{2}{\pi}\arctan(2\pi f_c\tau_c) = \sigma^2\cdot\frac2\pi\cdot\frac\pi4$: **0.5**. Half the power lies below the corner; the $1/f^2$ tail holds the other half.

### Solution 03-06.12

(a) $e^2 = (5\text{ nV})^2[10\ln100 + 9.9] = 25\times10^{-18}\times55.95$ V², so **37.40 nV** rms.

(b) $5.2\sqrt{9.9} = $ **16.36 nV** rms: less than half the noise at DC despite a slightly higher white floor.

(c) At 1 kHz, a hundred times above the 10 Hz corner, both are essentially white, so the 5 nV part is marginally quieter and avoids chopping artifacts in the audio band. A weigh-scale bridge measures near DC, where the zero-drift part's lack of 1/f noise (and offset drift) wins.

### Solution 03-06.13

For a random walk the rms error grows as $\sqrt t$. After 100 µs: $1\text{ ps}\times\sqrt{100} = $ **10 ps**; after 1 ms: $\sqrt{1000} = $ **31.62 ps**. Without correction the error grows without bound; a clock-and-data-recovery loop measures the phase of the incoming data and continuously corrects the sampling clock, turning the unbounded walk into a bounded tracking error ([24](../../24-high-speed-io-signal-integrity-and-photonics/README.md)).

### Solution 03-06.14

(a) Integrating $\operatorname{sinc}^2$ numerically, **0.7737** of the power lies below $R_b/2$ and **0.9028** below $R_b$.

(b) At $R_b = $ **10 GHz**.

(c) Three-quarters of the signal's power, and the fundamental of the fastest pattern (1010…), sit below $R_b/2$, so the channel's loss there largely sets how open the eye is. Equalizers are specified against the loss at that frequency.

### Solution 03-06.15

(a) With $2K = 32$ degrees of freedom, the quantiles are $\chi^2_{0.025} = 18.29$ and $\chi^2_{0.975} = 49.48$. The true PSD lies between $32/49.48 = $ **0.6467** and $32/18.29 = $ **1.750** times the measured value: **−1.893 dB** to **+2.429 dB**.

(b) Searching $K$, the upper limit first falls within 1 dB at $K = $ **82** (lower limit −0.8911 dB).

(c) It is the same chi-square interval: each PSD bin is a variance estimate with $2K$ degrees of freedom, so pinning a spectrum to ±1 dB needs about 160 degrees of freedom, just as 03-05's 50-sample noise-power estimate was uncertain by ±1.7 dB.

### Solution 03-06.16

(a) The sensor's density is 4.070 nV/√Hz. Over 0.1–100 Hz:

- Option A: $(4.070\text{ nV})^2\times99.9 + (5\text{ nV})^2[10\ln1000 + 99.9]$, giving **76.68 nV** rms.
- Option B: $[(4.070)^2 + 8^2]\text{ nV}^2\times99.9$, giving **89.71 nV** rms.

(b) For 40 dB SNR the signal must be 100 times the rms noise: **7.668 µV** (A) or **8.971 µV** (B).

(c) Most of this band lies above Option A's 10 Hz corner, where its white floor (5 nV/√Hz) beats the zero-drift part's 8 nV/√Hz; three decades of 1/f noise below 10 Hz cost A less than B's higher floor over 100 Hz. In a 0.01–1 Hz band the result reverses: A gives **34.53 nV** and B **8.931 nV**, because now the whole band sits deep in A's 1/f region. The right amplifier depends on the band, which is why noise must be compared as a spectrum, not a single number.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 03-06.1a | mean at ωt = π/2 | −0.6366 | V |
| 03-06.2a | total power | 5 | V² |
| 03-06.2b | DC power | 1 | V² |
| 03-06.2c | AC power | 4 | V² |
| 03-06.2d | correlation at τc | 0.3679 | — |
| 03-06.3a | sensors required | 194 | — |
| 03-06.4a | 50 Ω noise density at 290 K | 0.8949 | nV/√Hz |
| 03-06.4b | rms noise in 1 MHz | 0.8949 | µV |
| 03-06.4c | rms noise in 1 GHz | 28.30 | µV |
| 03-06.4d | available power in 1 MHz | −113.98 | dBm |
| 03-06.4e | available power in 1 GHz | −83.98 | dBm |
| 03-06.5a | noise floor | −108.96 | dBm |
| 03-06.5b | input for 6 dB SNR | −102.96 | dBm |
| 03-06.5c | 10 log10 of 2 MHz | 63.01 | dB |
| 03-06.6a | quantization noise, 12 bits | 70.48 | µV |
| 03-06.6b | minimum capacitance, 12 bits | 0.8339 | pF |
| 03-06.6c | quantization noise, 16 bits | 4.405 | µV |
| 03-06.6d | minimum capacitance, 16 bits | 213.5 | pF |
| 03-06.7a | noise bandwidth | 15.71 | kHz |
| 03-06.7b | output rms noise | 1.253 | µV |
| 03-06.8a | shot noise in 100 MHz | 17.90 | nA |
| 03-06.8b | signal-to-noise current ratio | 558.6 | — |
| 03-06.8c | signal-to-noise current ratio | 54.94 | dB |
| 03-06.9a | total input noise density | 1.346 | nV/√Hz |
| 03-06.9b | noise factor | 2.261 | — |
| 03-06.9c | noise figure | 3.544 | dB |
| 03-06.10a | σ of the 10 s average | 89.44 | µV |
| 03-06.10b | effective independent samples | 500 | — |
| 03-06.10c | naive σ/√n | 20 | µV |
| 03-06.11a | corner frequency | 159.2 | Hz |
| 03-06.11b | flat-region density | 63.25 | µV/√Hz |
| 03-06.11c | fraction of power below the corner | 0.5 | — |
| 03-06.12a | 0.1–10 Hz noise, option with 1/f | 37.40 | nV |
| 03-06.12b | 0.1–10 Hz noise, zero-drift | 16.36 | nV |
| 03-06.13a | timing error after 100 µs | 10 | ps |
| 03-06.13b | timing error after 1 ms | 31.62 | ps |
| 03-06.14a | NRZ power below Rb/2 | 0.7737 | — |
| 03-06.14b | NRZ power below Rb | 0.9028 | — |
| 03-06.14c | first null at 10 Gb/s | 10 | GHz |
| 03-06.15a | chi-square 2.5% quantile, 32 df | 18.29 | — |
| 03-06.15b | chi-square 97.5% quantile, 32 df | 49.48 | — |
| 03-06.15c | lower ratio | 0.6467 | — |
| 03-06.15d | upper ratio | 1.750 | — |
| 03-06.15e | lower limit | −1.893 | dB |
| 03-06.15f | upper limit | 2.429 | dB |
| 03-06.15g | averages for a 1 dB upper limit | 82 | — |
| 03-06.15h | lower limit at that K | −0.8911 | dB |
| 03-06.16a | sensor noise density | 4.070 | nV/√Hz |
| 03-06.16b | total noise, option A | 76.68 | nV |
| 03-06.16c | total noise, option B | 89.71 | nV |
| 03-06.16d | signal for 40 dB SNR, A | 7.668 | µV |
| 03-06.16e | signal for 40 dB SNR, B | 8.971 | µV |
| 03-06.16f | option A, 0.01–1 Hz | 34.53 | nV |
| 03-06.16g | option B, 0.01–1 Hz | 8.931 | nV |
