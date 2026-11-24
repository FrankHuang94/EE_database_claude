# Problems 21-03 · Noise Figure and Linearity

Chapter: [21-03](../chapters/21-03-noise-figure-and-linearity.md) · Worked solutions: [21-03 solutions](../solutions/21-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Powers are in dBm referred to 50 Ω; a peak voltage amplitude $A$ across 50 Ω carries $A^2/100$ W. $T_0$ = 290 K and $kT_0$ = −173.98 dBm/Hz unless a problem says −174. Problems marked *(lab)* can be checked with `labs/21-03-lab/rfnl.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 21-03.1 [A]

**Two-tone arithmetic.** Two tones of −25 dBm each produce output tones of −5 dBm and output IM3 products of −63 dBm. Find the gain, IIP3 and OIP3. What are the IM3 level in dBc and the output IM3 power in dBm at −35 dBm per tone?

### Problem 21-03.2 [A]

**Second order.** Two tones of −30 dBm each give output tones of −10 dBm and an output IM2 product of −52 dBm at the difference frequency. Find IIP2. At −40 dBm per tone, what are the IM2 level in dBc and its output power?

### Problem 21-03.3 [A]

**A low-ENR measurement.** A 6.0 dB ENR noise source gives a Y-factor of 3.2 dB on an amplifier (cold temperature 290 K, analyzer noise negligible). Find the noise figure and noise temperature. What Y-factor would a 15 dB ENR source give on the same amplifier?

### Problem 21-03.4 [A]

**From coefficients to intercepts.** An amplifier has $a_1$ = 10 and $a_3$ = −2 V⁻² (voltage in, voltage out). Find the input 1 dB compression amplitude and the IIP3 amplitude, and the ratio between them in dB. What is $\text{HD}_3$ for a 0.1 V input?

### Problem 21-03.5 [B]

**Noise circles.** A device has $\text{NF}_{min}$ = 1.2 dB, $R_n$ = 20 Ω and $\Gamma_{opt} = 0.5\angle 120°$ (50 Ω system). Find its noise figure with a 50 Ω source and with $\Gamma_s = 0.5\angle 90°$, and the centre and radius of its 2.0 dB noise circle. What impedance is $Z_{opt}$?

### Problem 21-03.6 [B]

**Noise parameters from $e_n$ and $i_n$.** A two-port has $e_n$ = 0.5 nV/√Hz, an uncorrelated input noise current $i_u$ = 2 pA/√Hz and a correlation admittance $Y_{cor} = (2 + j10)$ mS, all at 290 K. Find $R_n$, $G_u$, $Y_{opt}$, $Z_{opt}$ and $\text{NF}_{min}$, and the noise figure with a 50 Ω source.

### Problem 21-03.7 [B]

**Filter before or after the LNA?** A receiver has a filter (2.5 dB loss), an LNA (18 dB gain, NF 1.0 dB, IIP3 −10 dBm), a mixer (10 dB gain, NF 9 dB, IIP3 +8 dBm) and an ADC driver (15 dB gain, NF 12 dB, IIP3 +20 dBm). Find the cascade NF and IIP3 with the filter first (treat it as perfectly linear), and with the filter after the LNA (filter IIP3 +45 dBm). What does the noise figure gain cost, beyond the IIP3 change?

### Problem 21-03.8 [B]

**A Bluetooth-class sensitivity.** Assume a 1 MHz noise bandwidth and a required SNR of 10 dB. What noise figure gives a sensitivity of −96.5 dBm? What sensitivity would a 6 dB noise figure give, and how much margin does −96.5 dBm have over a −70 dBm requirement?

### Problem 21-03.9 [B]

**Desensitization by compression.** An LNA has IIP3 = −5 dBm. How much does a −20 dBm blocker reduce the gain of a weak signal? At what blocker power is the reduction 1 dB, and how does that compare with the LNA's own input 1 dB compression point from the cubic model?

### Problem 21-03.10 [B]

**A Wi-Fi phase-noise requirement.** A receiver with a 6 dB noise figure and an 18 MHz noise bandwidth faces a −40 dBm blocker. What LO phase noise at the blocker's offset keeps the reciprocal-mixing desensitization to 1 dB?

### Problem 21-03.11 [B] *(lab)*

**A transistor's intercept and temperature.** Find a bare bipolar transistor's IIP3 amplitude, and its power across 50 Ω, at −40 °C and 125 °C. What is $\text{HD}_2$ for a 2 mV tone at 300 K, from the series and exactly?

### Problem 21-03.12 [B] *(lab)*

**When the cubic model fails.** For an emitter-coupled pair: (a) find the exact input 1 dB compression amplitude in units of $V_T$ and compare it with the cubic model; (b) find the IM3 level for two differential tones of 20 mV each (300 K), from the series and exactly. Why do the two diverge more at 20 mV than at 10 mV?

### Problem 21-03.13 [C]

**A zero-IF receiver's IIP2.** A handset transmits +23 dBm at its antenna port in an FDD band; the duplexer gives 50 dB of transmit-to-receive isolation. The receiver has a 9 dB noise figure in a 4.5 MHz channel and converts to zero IF. Treating the leakage as a two-tone-equivalent aggressor, what IIP2 keeps its second-order product 10 dB below the thermal noise floor? How much does 5 dB more isolation relax it? What does the simplification overstate or understate?

### Problem 21-03.14 [C] *(lab)*

**Cascaded intercepts, derived and tested.** Stage 1 has $a_1$ = 5, $a_3$ = −0.5 and stage 2 has $b_1$ = 4, $b_3$ = −0.2 (all in V and V⁻²). (a) Find each stage's IIP3 amplitude and the cascade's from the formula of §3.6. (b) Compute the cascade's exact third-order coefficient and its IIP3 amplitude. (c) Repeat (b) if $b_3$ = +0.2. When is the cascade formula pessimistic?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Noise parameters and noise circles | 5, 6 |
| 2. Y-factor measurement | 3 |
| 3. Polynomial nonlinearity, IIP2 and IIP3 | 1, 2, 4, 11, 12, 13 |
| 4. Cascaded noise figure and IIP3 | 7, 14 |
| 5. Desensitization: compression and reciprocal mixing | 9, 10, 13 |
| 6. Sensitivity and dynamic range | 8 |
