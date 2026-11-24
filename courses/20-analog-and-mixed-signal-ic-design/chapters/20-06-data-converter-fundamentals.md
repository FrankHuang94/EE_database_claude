<!-- status: verified -->
# 20-06 · Data Converter Fundamentals

| | |
|---|---|
| **Course** | [20 · Analog and Mixed-Signal IC Design](../README.md) |
| **University equivalent** | The specification and testing material of a graduate data-converter course: quantization, static (INL, DNL) and dynamic (SNR, SINAD, SFDR, THD, ENOB) metrics, histogram and FFT testing, and converter figures of merit (Pelgrom, *Analog-to-Digital Conversion*, 4th ed.; Maloberti, *Data Converters*; IEEE Std 1241) |
| **Prerequisites** | [16-10](../../16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md) (quantization noise model), [16-05](../../16-digital-signal-processing/chapters/16-05-spectral-analysis-and-windowing.md) (FFT, windowing), [18-06](../../18-embedded-systems-and-microcontrollers/chapters/18-06-adc-dac-pwm.md) (MCU converter specifications), [20-05](20-05-comparators-and-sample-and-hold.md) (kT/C, jitter, the running ADC front end) |
| **Estimated study hours** | 7 |
| **Last verified** | 2026-11-24 |

**Learning objectives.** After this chapter you can:

1. Derive the quantization-noise SNR for sine, uniform and Gaussian signals and explain when the white-noise model fails.
2. Compute offset, gain error, DNL and INL (endpoint and best-fit) from transition levels, and relate capacitor mismatch to DNL, INL and missing codes.
3. Run a sine-wave histogram test and explain why coherent sampling matters for INL.
4. Compute SNR, THD, SINAD, SFDR, ENOB and noise spectral density from a spectrum, in dBc and dBFS.
5. Compute the Walden and Schreier figures of merit, derive the thermal limit on the Schreier figure, and explain which designs each figure favors.

## 1. Big picture

A data converter's data sheet is a page of numbers whose definitions are precise and whose implications are not obvious. A "12-bit" ADC may deliver 10 effective bits at the input frequency you care about; an ADC with excellent SNR may have spurs that ruin a radio receiver; a record-setting figure of merit may come from a design that would be useless in your product. This chapter defines the metrics, derives what limits each, shows how they are measured, and ends with the figures of merit used to compare converters across architectures and decades. The running example is the 12-bit, 100 MS/s SAR front end of 20-05, now complete with its capacitor DAC's mismatch.

- **Quantization noise is the floor, not the ceiling.** An ideal $N$-bit converter has an SNR of $6.02N + 1.76$ dB for a full-scale sine; real converters lose bits to thermal noise, jitter and nonlinearity.
- **Static and dynamic metrics answer different questions.** DNL and INL describe the transfer curve at DC; SNR, SINAD and SFDR describe a spectrum. Instrumentation and control care about the first; communications care about the second.
- **Measurement is part of the specification.** Histogram and FFT tests have their own pitfalls, and a number measured badly is not a property of the converter.
- **Figures of merit encode assumptions about cost.** The Walden figure assumes power doubles per bit; the Schreier figure assumes it quadruples, as thermal noise demands. They rank designs differently, and the frontier of each tells you where the field is.

## 2. Intuition first

```text
 code
  7 │                          ┌───────
  6 │                     ┌────┘
  5 │                ┌────┘            ideal: equal steps of 1 LSB,
  4 │           ┌────┘                 first transition at ½ LSB
  3 │      ┌────┘
  2 │  ┌───┘          real: steps of unequal width (DNL),
  1 │┌─┘                    staircase bends away from the line (INL)
  0 ┼┘─────────────────────────────────── v_in
     T1  T2   T3   T4   T5   T6   T7
```

*Figure 1. An ADC's transfer function is a staircase defined by its transition levels $T_k$. Unequal step widths are differential nonlinearity; the staircase's departure from a straight line is integral nonlinearity.*

**A ruler analogy, and its limits.** An ADC is a ruler. Its resolution is the spacing of the tick marks (the LSB). **DNL** asks whether every tick spacing is the same: a spacing of zero is a missing mark, a *missing code*. **INL** asks whether the ticks drift: a ruler printed on stretched paper can have perfectly even local spacing yet read 2 mm long at 30 cm. **Noise** is a shaky hand: repeated measurements of the same object scatter. **SNR and ENOB** summarize how finely the ruler can really distinguish lengths, including the hand. The analogy breaks for moving targets: a converter measures a signal that changes during the measurement, so its timing (jitter, 20-05) and its speed (bandwidth, distortion at high frequency) matter in a way no ruler's do.

**Finance analogy for figures of merit.** A figure of merit is a valuation multiple: it normalizes performance by cost (power) so different-sized companies (converters) can be compared. Like a P/E ratio, it embeds an assumption, here about how cost should scale with resolution, and like any multiple it misleads when the assumption does not fit the business.

## 3. Theory

> **Conventions.** $N$ bits, full-scale range $V_{FS}$ (peak to peak), LSB $\Delta = V_{FS}/2^N$. Codes $k = 0 \ldots 2^N - 1$; code $k$ is output for $T_k \le v < T_{k+1}$, with transition levels $T_1 \ldots T_{2^N-1}$ measured from the bottom of the range. Ideally $T_k = (k - \tfrac12)\Delta$. A full-scale sine has amplitude $A = V_{FS}/2$. dBc is relative to the measured signal; dBFS relative to a full-scale sine.

### 3.1 Quantization noise and signal statistics

If the input is "busy" (it crosses many codes between samples, uncorrelated with the sampling), the quantization error is well modeled as uniform on $[-\Delta/2, \Delta/2]$ and white, with variance $\Delta^2/12$ (16-10). For a full-scale sine, with power $A^2/2 = V_{FS}^2/8$:

$$
\text{SQNR} = \frac{V_{FS}^2/8}{\Delta^2/12} = \frac{3}{2}\,2^{2N} \quad\Longrightarrow\quad 6.02N + 1.76\ \text{dB} .
$$

The 1.76 dB is specific to a sine. The general rule is SQNR = $6.02N + 10\log_{10}(12\,\sigma_x^2/V_{FS}^2)$ for a signal of variance $\sigma_x^2$:

- **Uniform over the full range** ($\sigma_x^2 = V_{FS}^2/12$): exactly $6.02N$ dB.
- **Gaussian**, with the full scale at ±4σ so clipping is rare ($\sigma_x = V_{FS}/8$): $6.02N - 7.27$ dB. Communication signals such as OFDM (17-10) are nearly Gaussian, so a "12-bit" converter gives them about 65 dB, not 74 dB, before any other noise. The price of headroom is the signal's **crest factor** (peak to rms): 3.0 dB for a sine, 12.0 dB at 4σ.

**When the model fails.** If the input is periodic and its period divides the record (for example a sine at exactly $f_s/64$), the quantization error repeats every period too. Its power is unchanged but concentrated in harmonics: spurs instead of a floor (lab Part 1). The cures are a sine frequency co-prime with the record (§3.5), or **dither**: a small added noise that decorrelates the error at the cost of a little SNR (16-10).

### 3.2 Static errors: offset, gain, DNL and INL

From the measured transition levels:

- **Offset error**: $T_1 - \tfrac12\Delta$ (how far the first transition is from ideal).
- **Gain error**: $(T_{2^N-1} - T_1) - (2^N - 2)\Delta$ (how much the span between first and last transition differs from ideal).
- **Average step** after removing offset and gain: $\Delta_{avg} = (T_{2^N-1} - T_1)/(2^N - 2)$.
- **Differential nonlinearity** of code $k$ (for $k = 1 \ldots 2^N - 2$):

$$
\text{DNL}_k = \frac{T_{k+1} - T_k}{\Delta_{avg}} - 1 .
$$

- **Integral nonlinearity** at transition $k$, relative to the straight line through the end points:

$$
\text{INL}_k = \frac{T_k - \left[T_1 + (k - 1)\Delta_{avg}\right]}{\Delta_{avg}} = \sum_{j=1}^{k-1}\text{DNL}_j .
$$

The second form follows by telescoping: INL is the running sum of DNL. A **best-fit** INL uses a least-squares line instead. It is usually, though not always, smaller than the endpoint worst case (a least-squares line minimizes the sum of squares, not the maximum; only a minimax line is guaranteed never to be larger), so it is usually the more flattering number, and data sheets should say which they use.

**Properties.** DNL cannot be below −1 LSB: a code of zero width is a **missing code**. "No missing codes" therefore means DNL > −1 everywhere. A converter is **monotonic** if its output never decreases as the input increases; a SAR's binary search is monotonic by construction (a larger input wins the first comparison where two inputs differ), so its DNL errors appear as wide codes or missing codes, never as reversed ones.

### 3.3 Where DNL and INL come from: capacitor mismatch in a SAR

A SAR ADC's capacitive DAC (20-07) has binary-weighted bit capacitors, each made of $2^b$ unit capacitors. The transition to code $k$ is where the DAC's value for $k$ crosses the input, so the transition levels inherit the DAC's errors.

**A deterministic MSB error.** Let the MSB capacitor be $2^{N-1}(1 + \varepsilon)$ units and all others exact. At mid-scale the code steps from $011\ldots1$ (DAC value $2^{N-1} - 1$) to $100\ldots0$ (value $2^{N-1}(1 + \varepsilon)$), a step of $1 + 2^{N-1}\varepsilon$ LSB:

$$
\text{DNL}_{mid} = 2^{N-1}\varepsilon .
$$

For $\varepsilon > 0$ the code below mid-scale is wide. For $\varepsilon < -2^{-(N-1)}$ the step would be negative. The SAR then decides the MSB as 1 for inputs whose correct code is just below mid-scale, so those codes are never produced: missing codes (Example 20-06.3). Making each bit slightly *smaller* than binary and adding redundancy, so that any decision error can be recovered by later bits, is the standard cure (20-07).

**Random mismatch.** If each unit capacitor has an independent relative error with standard deviation $\sigma_u$, a bit capacitor of $2^b$ units has a relative error $\sigma_u/\sqrt{2^b}$. The mid-scale step compares $2^{N-1}$ units with $2^{N-1} - 1$ others, so its standard deviation in LSB is

$$
\sigma(\text{DNL}_{mid}) = \sigma_u\sqrt{2^N - 1} .
$$

The INL at mid-scale, relative to the endpoint line, is $(2047e_m - 2048e_l)/4095$ for 12 bits, where $e_m$ and $e_l$ are the summed unit errors of the MSB and of all the lower bits; its standard deviation is

$$
\sigma(\text{INL}_{mid}) = \sigma_u\sqrt{\frac{2^{N-1}(2^{N-1} - 1)}{2^N - 1}} \approx \frac{\sigma_u}{2}\,2^{N/2} .
$$

Matching therefore sets resolution: for 12 bits, 0.5% unit mismatch gives a mid-scale DNL of 0.32 LSB rms. Each extra bit multiplies the required matching by $\sqrt 2$, which is why converters beyond about 12 bits are calibrated rather than matched (20-07, 20-11).

### 3.4 The histogram (code-density) test

Measuring 4095 transition levels directly would need an accurate, slow DC sweep. The **code-density test** instead applies a known input distribution and counts how often each code appears: a code's count is proportional to its width times the input's probability density there.

A sine $v = V_0 + A\sin\theta$ with phase θ uniform on $[0, 2\pi)$ has the probability density

$$
p(v) = \frac{1}{\pi\sqrt{A^2 - (v - V_0)^2}} ,
$$

denser near the peaks, where the sine lingers. Its cumulative distribution is $P(v) = 1 - \tfrac{1}{\pi}\arccos[(v - V_0)/A]$. If $C_{k-1}$ is the fraction of samples with codes below $k$, inverting gives the transition levels directly:

$$
T_k = V_0 - A\cos\left(\pi C_{k-1}\right) .
$$

The amplitude is set slightly above full scale so every code is exercised. A sine is used rather than a ramp because a pure sine is far easier to generate than a perfectly linear ramp: its distortion can be filtered away.

**How many samples?** A mid-scale code of width Δ catches a fraction $\Delta/(\pi A)$ of the samples. If the samples are effectively random, the count is Poisson-like and its relative standard deviation is $1/\sqrt{\text{count}}$, which is the DNL's statistical error in LSB. A DNL resolution of 0.05 LSB needs about 400 counts per mid-scale code, several million samples for 12 bits (Example 20-06.5).

**Coherent sampling matters even more for INL.** INL is a running sum of DNL, so random count errors accumulate like a random walk. With random phases, the fraction of samples below mid-scale itself has a binomial standard deviation $\tfrac12/\sqrt{N_s}$, which at mid-scale moves $T_k$ by $\pi A/(2\sqrt{N_s})$, more than an LSB even for millions of samples. Choosing the sine frequency so the sample phases are spread uniformly and deterministically over the record (§3.5) removes this error almost entirely (lab Part 4).

![DNL and INL of a 12-bit SAR with 0.5 percent unit-capacitor mismatch: the DNL is small everywhere except negative spikes at major carries, largest at mid-scale near minus 0.37 LSB; the true INL wanders within about plus or minus 0.3 LSB; a histogram test with coherent phases reproduces it exactly, while one with random phases wanders up to 1.4 LSB away](../../../assets/figures/20-06/dnl_inl.svg)

*Figure 2. The lab's seeded 12-bit SAR. Top: DNL, with its largest errors at the major carries. Bottom: the true INL and the INL recovered by a $2^{22}$-sample sine histogram; coherent phases reproduce it to 0.001 LSB, random phases add a random walk of more than an LSB.*

### 3.5 Dynamic metrics and the FFT test

A converter's dynamic performance is measured with a pure sine input, an FFT of $N_{FFT}$ samples, and the following quantities, all ratios of powers:

- **SNR**: signal power over the noise power, excluding the DC bin, the signal and its harmonics.
- **THD**: the sum of the harmonics' powers (usually the 2nd to 5th or to 9th) over the signal power, a negative number of dBc.
- **SINAD** (also SNDR): signal over noise plus distortion. $\text{SINAD} = -10\log_{10}(10^{-\text{SNR}/10} + 10^{\text{THD}/10})$.
- **SFDR**: signal over the largest spur anywhere in the band, harmonic or not, in dBc (or dBFS if referred to full scale).
- **ENOB**: the resolution of an ideal converter with the same SINAD, $\text{ENOB} = (\text{SINAD} - 1.76)/6.02$. If the test signal is below full scale, data sheets often correct SINAD to full scale first, adding $20\log_{10}(A_{FS}/A)$.

**Coherent sampling.** To keep all the signal's energy in one FFT bin without a window, the input frequency must be an integer number of cycles of the record: $f_{in} = (M/N_{FFT})f_s$. Choosing $M$ odd, with $N_{FFT}$ a power of two, makes them co-prime, so every sample has a different phase and the quantization error does not repeat within the record (§3.1). Without coherent sampling, a window is needed and its leakage blurs the measurement (16-05).

**Noise spectral density and bandwidth.** White noise is spread over the Nyquist band $f_s/2$. The **noise spectral density** relative to full scale is

$$
\text{NSD} = -\text{SNR}_{FS} - 10\log_{10}(f_s/2)\ \ \text{dBFS/Hz} ,
$$

and a signal occupying only a bandwidth $B$ sees an SNR better by $10\log_{10}(f_s/2B)$, the **processing gain** of oversampling (20-08). In an FFT, each bin collects $1/(N_{FFT}/2)$ of the noise, so the displayed noise floor sits $10\log_{10}(N_{FFT}/2)$ dB below the SNR: a long FFT shows a deep floor without the converter being any quieter.

**Nonlinearity and harmonics.** A smooth static nonlinearity $v' = v - a_3v^3$ applied to $A\sin\omega t$ produces a third harmonic of amplitude $a_3A^3/4$, so $\text{HD}_3 = a_3A^2/4$. A bowed INL is such a nonlinearity: the INL's shape predicts the low-order harmonics, while DNL's code-by-code errors spread into many small spurs and a raised noise floor.

![Spectrum in dBFS from 0 to 50 megahertz of a 16384-point FFT test of the lab's converter at a 49 megahertz input: the signal at 0 dBFS near 49 megahertz, the aliased third harmonic at minus 64 dBc near 47 megahertz, a few small spurs, and a noise floor near minus 108 dBFS per bin](../../../assets/figures/20-06/spectrum.svg)

*Figure 3. An FFT test of the lab's full converter model at 49 MHz. The third harmonic, at 147 MHz, aliases to 47 MHz; it sets the SFDR and most of the SINAD loss. The noise floor per bin sits 39 dB below the 68.7 dB SNR because the 16,384-point FFT spreads the noise over 8192 bins.*

### 3.6 Figures of merit

Comparing converters of different speed and resolution needs a normalization. Two are standard.

**The Walden figure of merit** treats each effective bit as doubling the work per conversion:

$$
\text{FoM}_W = \frac{P}{2^{\text{ENOB}}\,f_s}\quad\text{(J per conversion step)} ,
$$

usually quoted in fJ/conversion-step, smaller being better. (When the bandwidth differs from $f_s/2$, $f_s$ is replaced by twice the bandwidth.) It assumes power grows as $2^{\text{ENOB}}$, which fits converters limited by matching, speed and digital logic rather than by thermal noise.

**The Schreier figure of merit** treats each bit as quadrupling the work, as thermal noise does (kT/C, 20-05):

$$
\text{FoM}_S = \text{SNDR} + 10\log_{10}\frac{BW}{P}\quad\text{(dB)} ,
$$

with $BW$ the signal bandwidth ($f_s/2$ for a Nyquist converter) and larger being better. A variant uses the dynamic range (DR) instead of SNDR.

**A thermal limit on FoM_S.** Consider the simplest Nyquist sampler: a capacitor $C$ driven by an ideal class-B driver from a supply equal to the full-scale swing $2A$, tracking a full-scale sine of frequency $f$. The driver delivers current $C\,dv/dt$. In class B the supply sources only the charging half-cycles; on the discharging half the capacitor returns its charge to ground, not to the supply. Each signal period therefore draws a charge $2AC$ from the supply, and the power is

$$
P = 2A \times 2AC \times f = 4A^2Cf .
$$

kT/C noise gives $\text{SNR} = (A^2/2)/(kT/C) = A^2C/(2kT)$, so $A^2C = 2kT\cdot\text{SNR}$ and $P = 8kT\cdot\text{SNR}\cdot f$. For a sine at the Nyquist frequency, $f = f_s/2$:

$$
\frac{P}{f_s} = 4kT\cdot\text{SNR} \quad\Longrightarrow\quad \text{FoM}_S \le 10\log_{10}\frac{1}{8kT} ,
$$

**194.8** dB at 300 K. Murmann's survey draws a more conservative line, $P/f_s = 8kT\cdot\text{SNR}$, attributing it to rail-to-rail class-B circuits after Vittoz (1990) [3]; it is the same bound evaluated at $f = f_s$, 3 dB higher in power, and corresponds to

$$
\text{FoM}_S = 10\log_{10}\frac{1}{16kT} ,
$$

**191.8** dB at 300 K. This course follows the survey and calls 191.8 dB "the thermal line", while remembering that an ideal sampler at a Nyquist input could in principle do 3 dB better. Real converters need much more than one ideal driver and one capacitor, but the bound explains the shape of the survey data: at high resolution, power must grow fourfold per bit, so the Schreier figure is the fair yardstick there, while at low resolution the Walden figure is.

> **Going deeper — what the figures ignore.** Neither figure counts the power of the input driver, the reference buffer or the clock, all of which can exceed the converter core's; neither rewards input bandwidth beyond $f_s/2$, latency or area. Murmann's survey, which collects every ISSCC and VLSI Symposium converter since 1997, plots both figures against speed so readers can see the trade-offs rather than one number (§9).

## 4. Worked examples

### Example 20-06.1 · Quantization noise and signal statistics (tier A)

**Setup.** For a 12-bit converter, find the SQNR for (a) a full-scale sine, (b) a signal uniform over the full range, (c) a Gaussian signal with the full scale at ±4σ, and the probability that it clips. (d) What is the SQNR of a sine at −20 dBFS?

**Solution.**

(a) $6.02 \times 12 + 1.76$ = **74.0** dB.

(b) $10\log_{10}(2^{24})$ = **72.2** dB.

(c) $10\log_{10}(12 \times 4^{12}/64)$ = **65.0** dB, that is 7.27 dB below (b). A Gaussian exceeds ±4σ with probability **6.33 × 10⁻⁵**, about one sample in 16,000.

(d) The quantization noise does not shrink with the signal: **54.0** dB.

**Sanity check.** The crest factor of a sine is $\sqrt 2$ (**3.0** dB), and of the Gaussian at 4σ, 4 (**12.0** dB); the 9.0 dB difference is exactly the gap between (a) and (c). Headroom for peaks is paid in SNR.

### Example 20-06.2 · Static errors of a 3-bit flash ADC (tier B)

**Setup.** A 3-bit flash ADC's reference ladder runs from 0 to 0.8 V (LSB 100 mV) with resistors, bottom to top, of 51, 98, 103, 100, 97, 104, 100 and 150 Ω (nominal 50, 6 × 100 and 150 Ω). Its seven comparators have offsets of +15, −20, +35, 0, −10, +40 and −5 mV. Find (a) the ladder taps, (b) the transition levels, (c) offset and gain errors in LSB, (d) DNL and endpoint INL, (e) the best-fit INL's worst case.

**Solution.**

(a) Each tap is 0.8 V times the resistance below it over the 803 Ω total: **50.81**, **148.44**, **251.06**, **350.68**, **447.32**, **550.93** and **650.56** mV. The ideal taps are 50, 150, …, 650 mV.

(b) Adding the offsets: **65.81**, **128.44**, **286.06**, **350.68**, **437.32**, **590.93** and **645.56** mV.

(c) Offset error $(65.81 - 50)/100$ = **0.158** LSB; gain error $[(645.56 - 65.81) - 600]/100$ = **−0.202** LSB.

(d) $\Delta_{avg}$ = (645.56 − 65.81)/6 = **96.63** mV. Then:

| Code | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| DNL (LSB) | **−0.352** | **+0.631** | **−0.331** | **−0.103** | **+0.590** | **−0.435** |

The endpoint INL at transitions 2 to 6 is **−0.352**, **+0.279**, **−0.052**, **−0.155** and **+0.435** LSB (zero at the ends by construction).

(e) The least-squares line gives a worst-case best-fit INL of **0.318** LSB, smaller than the endpoint worst case of 0.435 LSB.

**Sanity check.** The resistor errors alone (2–4%) move the taps by only a few millivolts; the comparator offsets of tens of millivolts dominate. In a flash ADC, comparator offset *is* nonlinearity (20-05 §3.8), and INL is the running sum of DNL: −0.352 + 0.631 = 0.279 ✓.

### Example 20-06.3 · A wrong MSB capacitor (tier B)

**Setup.** In a 12-bit SAR, the MSB capacitor is (a) 0.05% too large, (b) 0.1% too small, all other capacitors exact. Find the DNL at mid-scale and the endpoint INL there, and identify any missing codes.

**Solution.**

(a) $\text{DNL}_{mid} \approx 2048 \times 0.0005$ = 1.024 LSB; the exact model (which renormalizes the total) gives **+1.023** LSB for code 2047, which is twice as wide as normal. The endpoint INL at mid-scale is **+0.512** LSB. No codes are missing.

(b) The step would be $1 - 2.048$ LSB, negative. The SAR decides the MSB as 1 for inputs just below mid-scale, so codes **2046** and **2047** never appear: **2** missing codes (DNL = −1), and code 2045 is narrowed (DNL **−0.048**). The endpoint INL at mid-scale is **−1.02** LSB.

**Sanity check.** A 0.1% error in one capacitor costs two codes of a 4096-code converter. Matching to 0.05%, the threshold for one LSB at mid-scale in 12 bits, is hard for small capacitors, which is why SARs above 10 bits use redundancy or calibration.

### Example 20-06.4 · Random mismatch (tier B)

**Setup.** The 12-bit SAR's unit capacitors have 0.5% relative mismatch (σ). (a) Find the standard deviations of the mid-scale DNL and INL. (b) What unit mismatch gives a mid-scale DNL of 0.1 LSB rms? (c) In the lab's seeded instance, what are the worst-case DNL and endpoint INL?

**Solution.**

(a) $\sigma(\text{DNL}_{mid}) = 0.005\sqrt{4095}$ = **0.320** LSB and $\sigma(\text{INL}_{mid}) = 0.005\sqrt{2048 \times 2047/4095}$ = **0.160** LSB.

(b) $\sigma_u = 0.1/\sqrt{4095}$ = **0.156**%.

(c) The seeded instance (lab Part 3) has a worst-case |DNL| of **0.370** LSB, at mid-scale, and a worst-case |INL| of **0.328** LSB; no codes are missing.

**Sanity check.** The largest DNL sits at the MSB transition, as the formula predicts: the major carry compares the most capacitors. The worst-case INL, 0.328 LSB, is about twice the mid-scale σ, a typical extreme over thousands of transitions.

### Example 20-06.5 · Planning a histogram test (tier B)

**Setup.** The 12-bit converter is tested with a sine 2% above full scale ($A$ = 0.816 V around 0.8 V). (a) What fraction of samples lands in a mid-scale code? (b) How many samples give 400 counts per mid-scale code? (c) What counts do codes at 0.4 V and 0.79 V from the center then receive? (d) With random phases, what is the standard deviation of a mid-scale transition level estimated from the cumulative histogram, for $2^{22}$ samples?

**Solution.**

(a) $\Delta/(\pi A)$ = 390.6 µV/(π × 0.816 V) = **1.524 × 10⁻⁴**.

(b) 400/1.524 × 10⁻⁴ = **2.63 × 10⁶** samples.

(c) The count scales as $1/\sqrt{1 - (v/A)^2}$: **459** at 0.4 V and **1597** at 0.79 V.

(d) The fraction below mid-scale has standard deviation $\tfrac12/\sqrt{2^{22}}$ = 2.44 × 10⁻⁴, and $T = V_0 - A\cos(\pi C)$ has slope $\pi A$ there, so σ(T) = π × 0.816 × 2.44 × 10⁻⁴ = **0.626** mV, **1.60** LSB.

**Sanity check.** The DNL from 400 counts per code is good to about 1/√400 = 5% of an LSB, but the INL from random phases is off by more than an LSB: the cumulative sum inherits the binomial uncertainty of all the codes below. Coherent sampling makes the phases deterministic and removes it (lab Part 4: errors of about 0.001 LSB).

### Example 20-06.6 · Dynamic metrics of the running ADC (tier B)

**Setup.** From 20-05, the running design at a 49 MHz input has SNR 68.8 dB (Problem 20-05.9's noise budget) and, from its bootstrapped switch, HD3 of −64.4 dBc with the body grounded or −83.1 dBc with the body tied to the source; HD2 cancels. Find THD, SINAD, SFDR and ENOB in each case. Then repeat the SINAD for a measurement at −1 dBFS, quoting SNR in dBFS and dBc.

**Solution.**

| | THD | SINAD | SFDR | ENOB |
|---|---|---|---|---|
| Body grounded | **−64.4** dBc | **63.05** dB | **64.4** dBc | **10.18** |
| Body tied | **−83.1** dBc | **68.61** dB | **83.1** dBc | **11.10** |

$\text{SINAD} = -10\log_{10}(10^{-6.876} + 10^{-6.441})$ for the first row. With the signal at −1 dBFS, the noise is unchanged, so the SNR is 68.8 dBFS but **67.8** dBc.

**Sanity check.** With the body grounded, distortion costs nearly a full bit (ENOB 10.18 against 11.13 from noise alone): one spur 4.4 dB above the noise power dominates. With the body tied, the ENOB is within 0.03 bit of the noise-only value.

### Example 20-06.7 · Noise density and processing gain (tier A)

**Setup.** For the running design (SNR 68.8 dBFS at $f_s$ = 100 MS/s), find the noise spectral density, the SNR in a 1 MHz band, and the processing gain. Where does the noise floor sit on a 16,384-point FFT?

**Solution.** $\text{NSD} = -68.8 - 10\log_{10}(50 \times 10^6)$ = **−145.8** dBFS/Hz. In 1 MHz, $\text{SNR} = 68.8 + 10\log_{10}(50)$ = **85.8** dB, a processing gain of **17.0** dB. The FFT floor is $68.8 + 10\log_{10}(8192)$ = **107.9** dB below full scale per bin.

**Sanity check.** A narrowband user of a wideband ADC gains about 3 dB (half a bit) per doubling of the oversampling ratio: from **11.1** effective bits of noise to **14.0** within 1 MHz. A spectrum plot's floor at −108 dBFS is not the SNR.

### Example 20-06.8 · Figures of merit (tier B)

**Setup.** (a) The running ADC draws 1.5 mW at 100 MS/s. Find its Walden and Schreier figures for both cases of Example 20-06.6. (b) Compare two hypothetical converters: A (ENOB 7.5, 1 mW, 1 GS/s) and B (ENOB 15, 10 mW, 10 MS/s), assuming SINAD = 6.02 ENOB + 1.76. (c) Find the thermal-limit energy per conversion $8kT\cdot\text{SNR}$ for the running design's SNR, and its power at 100 MS/s.

**Solution.**

(a) Body grounded: $\text{FoM}_W$ = 1.5 mW/(2^10.18 × 100 MS/s) = **12.9** fJ/step and $\text{FoM}_S$ = 63.05 + 10 log₁₀(50 MHz/1.5 mW) = **168.3** dB. Body tied: **6.82** fJ/step and **173.8** dB.

(b) A: **5.52** fJ/step and **163.9** dB. B: **30.5** fJ/step and **179.0** dB. Walden ranks A better; Schreier ranks B better.

(c) $8kT \times 10^{6.876}$ = **0.249** pJ per conversion, **24.9** µW at 100 MS/s, 60 times below the assumed 1.5 mW.

**Sanity check.** Each figure rewards the kind of design whose cost scaling it assumes. B pays 4× power per bit, which Schreier treats as fair and Walden penalizes. The running design is 23.5 dB (Schreier) from the 191.8 dB thermal limit, a typical gap: real converters spend power on references, comparators, logic and drivers that the bound does not count.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 20-06.1a | SQNR, full-scale sine | 74.0 | dB |
| Ex 20-06.1b | SQNR, uniform signal | 72.2 | dB |
| Ex 20-06.1c | SQNR, Gaussian at 4 sigma | 65.0 | dB |
| Ex 20-06.1d | Gaussian clipping probability | 6.33e-5 | — |
| Ex 20-06.1e | SQNR at −20 dBFS | 54.0 | dB |
| Ex 20-06.1f | crest factor of a sine | 3.0 | dB |
| Ex 20-06.1g | crest factor at 4 sigma | 12.0 | dB |
| Ex 20-06.1h | uniform minus Gaussian | 7.27 | dB |
| Ex 20-06.1i | one sample in | 1.6×10⁴ | — |
| Ex 20-06.1j | crest-factor difference | 9.0 | dB |
| Ex 20-06.2a | tap 1 | 50.81 | mV |
| Ex 20-06.2b | tap 2 | 148.44 | mV |
| Ex 20-06.2c | tap 3 | 251.06 | mV |
| Ex 20-06.2d | tap 4 | 350.68 | mV |
| Ex 20-06.2e | tap 5 | 447.32 | mV |
| Ex 20-06.2f | tap 6 | 550.93 | mV |
| Ex 20-06.2g | tap 7 | 650.56 | mV |
| Ex 20-06.2h | T1 | 65.81 | mV |
| Ex 20-06.2i | T2 | 128.44 | mV |
| Ex 20-06.2j | T3 | 286.06 | mV |
| Ex 20-06.2k | T4 | 350.68 | mV |
| Ex 20-06.2l | T5 | 437.32 | mV |
| Ex 20-06.2m | T6 | 590.93 | mV |
| Ex 20-06.2n | T7 | 645.56 | mV |
| Ex 20-06.2o | offset error | 0.158 | LSB |
| Ex 20-06.2p | gain error | −0.202 | LSB |
| Ex 20-06.2q | average step | 96.63 | mV |
| Ex 20-06.2r | DNL code 1 | −0.352 | LSB |
| Ex 20-06.2s | DNL code 2 | 0.631 | LSB |
| Ex 20-06.2t | DNL code 3 | −0.331 | LSB |
| Ex 20-06.2u | DNL code 4 | −0.103 | LSB |
| Ex 20-06.2v | DNL code 5 | 0.590 | LSB |
| Ex 20-06.2w | DNL code 6 | −0.435 | LSB |
| Ex 20-06.2x | INL at T2 | −0.352 | LSB |
| Ex 20-06.2y | INL at T3 | 0.279 | LSB |
| Ex 20-06.2z | INL at T4 | −0.052 | LSB |
| Ex 20-06.2aa | INL at T5 | −0.155 | LSB |
| Ex 20-06.2ab | INL at T6 | 0.435 | LSB |
| Ex 20-06.2ac | worst-case best-fit INL | 0.318 | LSB |
| Ex 20-06.3a | DNL, MSB 0.05% high, approximation | 1.024 | LSB |
| Ex 20-06.3b | DNL, MSB 0.05% high, exact | 1.023 | LSB |
| Ex 20-06.3c | INL at mid-scale, MSB high | 0.512 | LSB |
| Ex 20-06.3d | first missing code | 2046 | — |
| Ex 20-06.3e | second missing code | 2047 | — |
| Ex 20-06.3f | number of missing codes | 2 | — |
| Ex 20-06.3g | DNL of code 2045 | −0.048 | LSB |
| Ex 20-06.3h | INL at mid-scale, MSB low | −1.02 | LSB |
| Ex 20-06.3i | step for MSB 0.1% low | −1.048 | LSB |
| Ex 20-06.4a | sigma DNL mid | 0.320 | LSB |
| Ex 20-06.4b | sigma INL mid | 0.160 | LSB |
| Ex 20-06.4c | unit mismatch for 0.1 LSB | 0.156 | % |
| Ex 20-06.4d | seeded worst DNL | 0.370 | LSB |
| Ex 20-06.4e | seeded worst INL | 0.328 | LSB |
| Ex 20-06.5a | mid-code fraction | 1.524e-4 | — |
| Ex 20-06.5b | samples for 400 counts | 2.63e6 | — |
| Ex 20-06.5c | counts at 0.4 V | 459 | — |
| Ex 20-06.5d | counts at 0.79 V | 1597 | — |
| Ex 20-06.5e | sigma of the mid-scale fraction | 2.44e-4 | — |
| Ex 20-06.5f | sigma of T, random phases | 0.626 | mV |
| Ex 20-06.5g | sigma of T in LSB | 1.60 | LSB |
| Ex 20-06.5h | DNL resolution from 400 counts | 5 | % |
| Ex 20-06.6a | THD, body grounded | −64.4 | dBc |
| Ex 20-06.6b | SINAD, body grounded | 63.05 | dB |
| Ex 20-06.6c | SFDR, body grounded | 64.4 | dBc |
| Ex 20-06.6d | ENOB, body grounded | 10.18 | bits |
| Ex 20-06.6e | THD, body tied | −83.1 | dBc |
| Ex 20-06.6f | SINAD, body tied | 68.61 | dB |
| Ex 20-06.6g | SFDR, body tied | 83.1 | dBc |
| Ex 20-06.6h | ENOB, body tied | 11.10 | bits |
| Ex 20-06.6i | SNR at −1 dBFS in dBc | 67.8 | dBc |
| Ex 20-06.6j | ENOB from noise alone | 11.13 | bits |
| Ex 20-06.6k | spur above noise power | 4.4 | dB |
| Ex 20-06.6l | ENOB gap, body tied | 0.03 | bits |
| Ex 20-06.7a | NSD | −145.8 | dBFS/Hz |
| Ex 20-06.7b | SNR in 1 MHz | 85.8 | dB |
| Ex 20-06.7c | processing gain | 17.0 | dB |
| Ex 20-06.7d | FFT floor below full scale | 107.9 | dB |
| Ex 20-06.7e | effective bits, full band | 11.1 | bits |
| Ex 20-06.7f | effective bits in 1 MHz | 14.0 | bits |
| Ex 20-06.8a | FoM_W, body grounded | 12.9 | fJ |
| Ex 20-06.8b | FoM_S, body grounded | 168.3 | dB |
| Ex 20-06.8c | FoM_W, body tied | 6.82 | fJ |
| Ex 20-06.8d | FoM_S, body tied | 173.8 | dB |
| Ex 20-06.8e | FoM_W, A | 5.52 | fJ |
| Ex 20-06.8f | FoM_S, A | 163.9 | dB |
| Ex 20-06.8g | FoM_W, B | 30.5 | fJ |
| Ex 20-06.8h | FoM_S, B | 179.0 | dB |
| Ex 20-06.8i | 8kT SNR energy | 0.249 | pJ |
| Ex 20-06.8j | thermal-limit power | 24.9 | µW |
| Ex 20-06.8k | ratio to 1.5 mW | 60 | — |
| Ex 20-06.8l | gap to the thermal limit | 23.5 | dB |
| Txt 20-06.a | thermal limit on FoM_S | 191.8 | dB |
| Txt 20-06.a2 | ideal class-B limit at a Nyquist input | 194.8 | dB |
| Txt 20-06.b | mid-scale DNL for 0.5% | 0.32 | LSB |
| Txt 20-06.c | 10 log10(8192) | 39 | dB |
| Txt 20-06.d | gap from the record to the thermal line | 2.6 | dB |
| Txt 20-06.f | log2 sqrt(12) | 1.79 | bits |
| Txt 20-06.e | NSD from 55.6 dBFS at 5.12 GS/s | −149.7 | dBFS/Hz |

## 5. Simulate it

The lab ([labs/20-06-lab](../labs/20-06-lab/README.md)) implements a behavioral SAR ADC with capacitor mismatch in `adc.py`, with the histogram and FFT tests and the figures of merit, and confirms the flash ladder in ngspice.

**Predict, then run.**

1. Predict the SFDR of an ideal 12-bit quantizer with a sine at bin 64 of a 4096-point FFT, and at bin 1001. Then add 0.5 LSB of dither (Part 1).
2. Predict the ladder taps of Example 20-06.2, then run `ngspice -b ladder.cir` (Part 2).
3. Draw a seeded SAR with 0.5% unit mismatch and plot its DNL and INL (Part 3).
4. Predict the histogram test's INL error with random phases and with coherent sampling, then run both (Part 4).
5. Run a full FFT test of the converter with mismatch, thermal noise and the switch's third-order distortion; compute ENOB and both figures of merit (Part 5).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| More bits (resolution) | SQNR, dynamic range | Matching or calibration, kT/C capacitance (4× per bit), power | Converter architect |
| Larger unit capacitors | DNL/INL (matching) | Area, DAC switching energy, speed | Analog designer |
| Redundancy and calibration | Linearity beyond matching | Extra conversion cycles, digital logic, test time | Converter architect |
| Input amplitude backoff | Distortion (HD3 falls 2 dB per dB) | SNR (1 dB per dB) | System designer |
| Dither | Spurs from correlated quantization error | A little SNR | System designer |
| Longer test records | Test accuracy (histogram, FFT floor) | Test time and cost | Product and test engineering |
| Choice of figure of merit | Fair comparison for the use case | Can flatter one architecture over another | Analyst, reviewer |

## 7. Numbers to know

| Quantity | Typical value | Note |
|---|---|---|
| Ideal SQNR, full-scale sine | $6.02N + 1.76$ dB | 74.0 dB at 12 bits, 98.1 dB at 16 bits; exact |
| SQNR penalty for a Gaussian signal at ±4σ | 7.27 dB below a uniform signal, 9.0 dB below a sine | crest factor; exact |
| Processing gain | $10\log_{10}(f_s/2B)$ | 3 dB (half a bit) per doubling of oversampling |
| Thermal limit on the Schreier figure | about 192 dB at 300 K (the survey's $8kT\cdot\text{SNR}$ line); 194.8 dB for an ideal class-B sampler with a Nyquist-frequency input | $10\log_{10}(1/16kT)$ and $10\log_{10}(1/8kT)$ (§3.6) |
| Thermal noise floor of pipeline ADCs (as of 2010) | about 70–74 dB for a 14-bit pipeline, 77–80 dB for a 16-bit ADC | TI *Analog Applications Journal* SLYT379 [R-332] |
| RF-sampling ADC noise density (as of Nov 2026) | about −150 to −156 dBFS/Hz | TI ADC12DJ5200RF: −150.4 dBFS/Hz (dual channel, 0.8 Vpp); ADC32RF55: −155.6 dBFS/Hz [R-334] |
| SNR across frequency of a 12-bit RF-sampling ADC (as of Nov 2026) | 55.6 dBFS at 347 MHz falling to 49.6 dBFS at 8.0 GHz | TI ADC12DJ5200RF, dual-channel mode [R-334] |
| Low-speed state of the art (as of 2022) | at the "8kTSNR energy limit" | Murmann, ISSCC 2022 short course [R-334] |
| Best published Walden figure (as of Nov 2026) | 0.35 fJ/conversion-step | 10-bit SAR at 200 kS/s, 65 nm (Bindra et al., VLSI 2019), from the survey [R-336] |
| Best published Schreier figure (as of Nov 2026) | 189.2 dB (oversampled); 186.8 dB (Nyquist rate) | noise-shaping SAR, 1 kHz bandwidth (Zhao et al., ISSCC 2025); SAR-ISDM (Hsieh and Hsieh, ISSCC 2018) [R-336] |
| Best Schreier figure at high speed (as of Nov 2026) | 181.5 dB at 130 MS/s; 173.3 dB at 1 GS/s; 159.3 dB at 12 GS/s | Wang and Kuo (ISSCC 2022); Cao et al. (ISSCC 2025); Cao et al. (ISSCC 2024) [R-336] |

## 8. Common mistakes

- **Reading the FFT floor as the SNR.** The floor per bin sits $10\log_{10}(N_{FFT}/2)$ dB below the noise power; a 16k-point FFT shows a floor 39 dB below the SNR.
- **Comparing dBc with dBFS.** An SNR measured at −1 dBFS is 1 dB worse in dBc; data sheets usually quote dBFS.
- **Quoting ENOB without frequency and amplitude.** ENOB at 1 MHz and at Nyquist can differ by bits; ENOB at −1 dBFS may be normalized to full scale or not.
- **Best-fit INL presented as INL.** Both lines remove gain error, but the least-squares line usually lowers the worst case; check which definition is used.
- **Assuming DNL > −1 means good linearity.** A converter can have no missing codes and still have a bowed INL that produces large harmonics.
- **Non-coherent FFT tests without a window.** Leakage spreads the signal over many bins and corrupts every metric.
- **Comparing Walden figures across resolutions.** Walden flatters low-resolution designs; use Schreier for thermal-noise-limited ones, and ask what power was counted.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **The definitions are standardized [Established].** IEEE Std 1241-2023 (ADCs) and IEEE Std 1658-2023 (DACs) are the current editions of the terminology and test-method standards [1]. Their text is paywalled; the definitions in §3 follow the standard's terms as described by members of its committee and by vendors' application notes, which also state the $6.02N + 1.76$ dB and ENOB conventions and the coherent-sampling rule [R-335].
- **The field's yardstick is a public survey [Established].** Murmann's "ADC Performance Survey 1997–2026" collects every converter published at ISSCC and the VLSI Symposium since 1997; its latest revision (August 2026) includes VLSI 2026 [R-332]. From its data, as of Nov 2026: the best Walden figure is **0.35** fJ/conversion-step, a 10-bit SAR at 200 kS/s in 65 nm (Bindra et al., VLSI 2019, unchanged since); the best Schreier figure is **189.2** dB, a noise-shaping SAR with 120 dB SNDR in a 1 kHz band (Zhao et al., ISSCC 2025), and **186.8** dB at Nyquist rate (Hsieh and Hsieh, ISSCC 2018). The record sits **2.6** dB below the 191.8 dB thermal line of §3.6 [R-336].
- **The frontier falls with speed [Established].** The best Schreier figures are 181.5 dB at 130 MS/s (a pipelined-SAR, Wang and Kuo, ISSCC 2022), 173.3 dB at 1 GS/s (a 14-bit single-channel pipeline, Cao et al., ISSCC 2025) and 159.3 dB at 12 GS/s (a 4× time-interleaved pipeline, Cao et al., ISSCC 2024) [R-336]. Murmann's 2022 short course shows the envelope rolling off at about −10 dB per decade above roughly 10 MS/s and summarizes low-speed converters as at the "8kTSNR energy limit" and high-speed ones as limited by "tens of femtoseconds timing jitter" [R-334].
- **Commercial converters specify the full picture [Established].** TI's ADC12DJ5200RF (12 bits, up to 10.4 GS/s) specifies DNL of +0.14/−0.13 LSB with no missing codes but INL of +2.0/−2.4 LSB, and at 2.4 GHz SNR 54.7 dBFS, SINAD 53.9 dBFS, ENOB 8.7 and SFDR 65 dBFS. A 16-bit, 1 MS/s SAR (ADS8861) specifies ±1 LSB INL, 96.5 dB SNR and −112 dB THD at 5.5 mW; a 24-bit ΔΣ converter (ADS127L11) specifies 0.9 ppm best-fit INL and 111.5 dB dynamic range [R-336].

### Why it matters commercially

Converter specifications are where analog performance meets a customer's purchase decision, and they are where most disputes about "performance" between vendors, customers and acquirers start. A base-station or radar customer buys SFDR and NSD at its carrier frequency, not bits; an instrumentation customer buys INL, drift and no missing codes; a battery-powered sensor buys energy per conversion at modest resolution, which is what the Walden figure measures. A semiconductor company's converter portfolio, and the IP inside its SoCs, is valued on these numbers, so an engineer or investor who can read them skeptically (which frequency, which amplitude, which definition, which power was counted) can tell a genuine advance from a well-chosen test condition.

### Questions for engineering leaders

1. **"What are SNR, SFDR and ENOB at the top of our band, at our signal amplitude?"** Strong: a table across frequency and amplitude, measured coherently, with the window and record length stated. Evasive: the low-frequency, full-scale values.
2. **"Is your INL endpoint or best-fit, and over what temperature range?"** Strong: both, with the test method (histogram, record length) and the distribution across parts. Evasive: a typical best-fit value.
3. **"Which power does your figure of merit include: core only, or reference buffers, input drivers and clocking?"** Strong: a breakdown that adds up to the package-level power. Evasive: a core-only Schreier figure.
4. **"How does performance hold up over process, voltage and temperature, and how much of it depends on calibration?"** Strong: calibration method, its convergence time and what happens if it is interrupted. Evasive: "background calibration handles it."
5. **"What does the converter do with an input beyond full scale, and how fast does it recover?"** Strong: specified overload recovery and over-range flags. Evasive: no answer; overload behavior is often untested in academic designs.

### Marketing vs Reality

- **"12-bit."** Resolution is the number of output bits; ENOB at your frequency is what you get. The ADC12DJ5200RF specifies 8.7 effective bits at 2.4 GHz and 7.4 at 8.0 GHz (SINAD 46.2 dBFS) [R-336].
- **dBFS versus dBc.** The same data sheet quotes SFDR in dBFS; most older data sheets and TI's own measurement guide use dBc. At −1 dBFS the difference is 1 dB, at −10 dBFS ten [R-335], [R-336].
- **Noise density versus SNR.** NSD is usually measured with a small input (−20 dBFS for the ADC12DJ5200RF), where jitter and distortion are negligible, so it looks better than the SNR measured near full scale. From the 55.6 dBFS SNR at 347 MHz and 5.12 GS/s, §3.5's formula gives **−149.7** dBFS/Hz, against the specified −150.4 dBFS/Hz at −20 dBFS [R-334].
- **Dynamic-range figures of merit.** A Schreier figure computed from dynamic range instead of SNDR can be inflated by a noise floor that depends on the signal. Computed from the survey's data, one 2020 entry reaches about 203 dB on dynamic range against 164.9 dB on SNDR, above the thermal line; the survey ranks by SNDR and has no dynamic-range column [R-336].
- **"Effective resolution."** Some precision-converter data sheets quote an "effective resolution" of $\log_2(\text{FSR}/v_{n,rms})$, which omits the $\sqrt{12}$ of the IEEE-style ENOB and so reads **1.79** bits higher for the same noise [R-336].
- **Averaging is not free resolution.** The ADC32RF55's 2× and 4× averaging modes gain 2.5 and 4.8 dB against an ideal 3.0 and 6.0 dB, because the averaged channels' noise is partly correlated [R-334].
- **Front page versus table.** Check both: the ADC12DJ5200RF's front page gives 8.6 bits where its table gives 8.7, and the ADS8861's front page gives −115 dB THD where its table gives −112 dB [R-336].
- **Sanity check.** Convert every claim to the same footing: SNR in dBFS at a stated frequency and amplitude, ENOB from SINAD, and power at the package pins. Then compare against $-20\log_{10}(2\pi f_{in}\sigma_t)$ and the 192 dB thermal limit.

## 10. Concept check

**Q1.** Why is the SQNR of a Gaussian signal lower than that of a full-scale sine for the same converter?

<details><summary>Answer</summary>

The quantization noise is fixed at $\Delta^2/12$, but a Gaussian signal must be scaled down so its peaks rarely clip; its rms value is a smaller fraction of full scale than a sine's (crest factor 4 at ±4σ against $\sqrt 2$). The SQNR falls by the ratio of the crest factors squared, 9.0 dB.

</details>

**Q2.** Why is INL the running sum of DNL?

<details><summary>Answer</summary>

Each DNL is the excess width of one code relative to the average step. The transition level $T_k$ is the sum of all code widths below it, so its departure from the straight line is the sum of the excess widths below it.

</details>

**Q3.** A SAR ADC's MSB capacitor is slightly too small. What happens near mid-scale, and why does redundancy help?

<details><summary>Answer</summary>

The MSB decision switches to 1 before the input reaches the correct mid-scale level, so the codes just below mid-scale can never be produced: missing codes. With redundancy (bit weights below binary plus extra conversion steps), a wrong early decision can be corrected by later bits, so no codes are lost and the error can be calibrated out.

</details>

**Q4.** Why does a sine-wave histogram test need more samples near mid-scale than near the ends?

<details><summary>Answer</summary>

A sine spends the least time near its zero crossing, so mid-scale codes receive the fewest samples: a fraction $\Delta/(\pi A)$. The sample count is set by the code that receives the least.

</details>

**Q5.** Why must the input frequency in an FFT test be $f_s M/N_{FFT}$ with $M$ odd?

<details><summary>Answer</summary>

An integer $M$ puts the signal exactly in one bin, so no window is needed. An odd $M$ is co-prime with a power-of-two $N_{FFT}$, so every sample has a different phase; otherwise the quantization error repeats and appears as spurs.

</details>

**Q6.** Converter X has a Walden figure of 2 fJ/step at 6 effective bits; converter Y has 20 fJ/step at 14 effective bits. Which is better?

<details><summary>Answer</summary>

It depends on the use. By Walden, X is ten times better. By Schreier, with the same speed, Y's figure is higher: going from 6 to 14 bits multiplies $2^{\text{ENOB}}$ by 256 but SNR by 65,536, so Y spends only 10 × 256 = 2560 times X's power for 65,536 times the SNR. For thermal-noise-limited resolutions, Schreier is the fairer comparison.

</details>

**Q7.** What thermal limit does the Schreier figure have, and where does it come from?

<details><summary>Answer</summary>

About 191.8 dB at 300 K on the survey's line $P/f_s = 8kT\cdot\text{SNR}$, which combines kT/C noise with the charge a class-B driver must move. An ideal class-B sampler tracking a Nyquist-frequency sine needs only half that power, $4kT\cdot\text{SNR}$ per sample, and could reach 194.8 dB; the survey's line is the same bound evaluated at $f = f_s$.

</details>

Problems: [20-06 problem set](../problems/20-06-problems.md) · Worked solutions: [20-06 solutions](../solutions/20-06-solutions.md)

## 11. Key terms

[Differential nonlinearity (DNL)](../../../reference/glossary.md#differential-nonlinearity-dnl) · [Integral nonlinearity (INL)](../../../reference/glossary.md#integral-nonlinearity-inl) · [Missing code](../../../reference/glossary.md#missing-code) · [Code-density test](../../../reference/glossary.md#code-density-test) · [Coherent sampling](../../../reference/glossary.md#coherent-sampling) · [SINAD](../../../reference/glossary.md#sinad) · [Spurious-free dynamic range (SFDR)](../../../reference/glossary.md#spurious-free-dynamic-range-sfdr) · [Effective number of bits (ENOB)](../../../reference/glossary.md#effective-number-of-bits-enob) · [Noise spectral density](../../../reference/glossary.md#noise-spectral-density) · [Walden figure of merit](../../../reference/glossary.md#walden-figure-of-merit) · [Schreier figure of merit](../../../reference/glossary.md#schreier-figure-of-merit) · [Crest factor](../../../reference/glossary.md#crest-factor)

## 12. Connections

- **Previous:** [20-05](20-05-comparators-and-sample-and-hold.md) built the sampler and comparator whose noise, jitter and distortion this chapter turns into converter metrics.
- **Builds on:** [16-10](../../16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md) (quantization noise), [16-05](../../16-digital-signal-processing/chapters/16-05-spectral-analysis-and-windowing.md) (FFT and windows), [18-06](../../18-embedded-systems-and-microcontrollers/chapters/18-06-adc-dac-pwm.md) (data-sheet terms), [10-08](../../10-electronics-1/chapters/10-08-current-sources-and-mirrors.md) (mismatch).
- **Next:** [20-07](20-07-nyquist-adcs.md) builds flash, SAR and pipeline converters and the calibration that removes the mismatch errors of §3.3.
- **Used later:** [20-08](20-08-sigma-delta-converters.md) (processing gain and noise shaping), [20-09](20-09-dacs.md) (the same static and dynamic metrics for DACs), [20-12](20-12-why-analog-does-not-scale.md) (the thermal limit and scaling).

## 13. Further study

- M. Pelgrom, *Analog-to-Digital Conversion*, 4th ed., Springer, 2022: the chapters on converter specifications and quantization.
- F. Maloberti, *Data Converters*, Springer, 2007: specifications and testing.
- IEEE Std 1241-2023, *Terminology and Test Methods for Analog-to-Digital Converters* (cited in §14), for the formal definitions and test procedures.
- B. Murmann, "ADC Performance Survey" (github.com/bmurmann/ADC-survey): download the spreadsheet and plot the figures of merit yourself.

## 14. Sources

1. IEEE Std 1241-2023, *IEEE Standard for Terminology and Test Methods for Analog-to-Digital Converters*, DOI 10.1109/IEEESTD.2023.10269815; IEEE Std 1658-2023 (DACs), DOI 10.1109/IEEESTD.2023.10285677; P. Crovetti et al., "The IEEE Std. 1658-2023 for terminology and test methods of digital-to-analog converters," *IEEE Instrum. Meas. Mag.*, vol. 28, no. 4, pp. 7–12, June 2025 [R-335].
2. R. H. Walden, "Analog-to-digital converter survey and analysis," *IEEE J. Sel. Areas Commun.*, vol. 17, no. 4, pp. 539–550, Apr. 1999, DOI 10.1109/49.761034 [R-332].
3. B. Murmann, "ADC Performance Survey 1997–2026," github.com/bmurmann/ADC-survey (revision 2026-08-01), and "Introduction to ADCs/DACs: Metrics, Topologies, Trade Space, and Applications," ISSCC Short Course, Feb. 2022 (the 8kT·SNR line, after E. A. Vittoz, "Future of analog in the VLSI environment," *Proc. ISCAS*, 1990) [R-332], [R-334], [R-336].
4. Record designs: H. S. Bindra et al., VLSI Symposium 2019, DOI 10.23919/VLSIC.2019.8778093; H. Zhao et al., ISSCC 2025, paper 18.1, DOI 10.1109/ISSCC49661.2025.10904778; S.-E. Hsieh and C.-C. Hsieh, ISSCC 2018, DOI 10.1109/ISSCC.2018.8310273; J.-C. Wang and T.-H. Kuo, ISSCC 2022, DOI 10.1109/ISSCC42614.2022.9731546; Y. Cao et al., ISSCC 2025, paper 24.2, DOI 10.1109/ISSCC49661.2025.10904766; Y. Cao et al., ISSCC 2024, paper 22.1, DOI 10.1109/ISSCC49657.2024.10454350 [R-336].
5. TI application notes: C. Pearson, "High-speed, analog-to-digital converter basics," SLAA510, 2011; *ADCPro User's Guide* SBAU128C, 2012 (coherent sampling); R. Reeder, "Coherently sampling in high-speed data-converter testing," SLVAG04, 2025; T. Neu, "Clock jitter analyzed in the time domain, Part 1," SLYT379, 2010 [R-332], [R-335].
6. Texas Instruments data sheets ADC12DJ5200RF (SLVSEN9H), ADC32RF55 (SBAS500B), ADS8861 and ADS127L11 [R-333], [R-334], [R-336].
7. Course chapters [16-10](../../16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md) (quantization), [16-05](../../16-digital-signal-processing/chapters/16-05-spectral-analysis-and-windowing.md) (spectral analysis) and [20-05](20-05-comparators-and-sample-and-hold.md) (kT/C and jitter).
