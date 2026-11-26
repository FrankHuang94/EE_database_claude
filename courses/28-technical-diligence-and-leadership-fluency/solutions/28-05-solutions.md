# Solutions 28-05 · Domain Question Banks II: Analog/Mixed-Signal, RF, Power, Packaging, Embedded

Problems: [28-05 problems](../problems/28-05-problems.md) · Chapter: [28-05](../chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md). Every number is recomputed by [verify_28_05.py](../verify/verify_28_05.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 28-05.1

- (a) **Evasive (a pivot):** SNR, not SNDR, and no frequency. To be strong: SNDR against input frequency, including near Nyquist, at a stated amplitude and clock.
- (b) **Strong:** average efficiency with the signal, its PAPR and bandwidth, the ACLR, the DPD with its power counted, and a limit over temperature.
- (c) **Evasive:** an adjective in place of a definition. To be strong: the volume definition (cased or open-frame, with or without hold-up and connectors) and the dimensions.
- (d) **Partial:** an honest follow-up plus a number at the wrong condition. It becomes strong when the 85 °C typical and maximum arrive, with what is retained in standby.

### Solution 28-05.2

ENOB $= (70 - 1.76)/6.02$ = **11.34** bits. $\text{FoM}_W = 0.15/(2.5 \times 10^8 \times 2^{11.34})$ = **232** fJ per step. $\text{FoM}_S = 70 + 10\log_{10}(1.25 \times 10^8/0.15)$ = **159.2** dB, **22.3** dB below the 181.5 dB published result. Floor: $8k_BT \times 10^7 \times 2.5 \times 10^8$ = **0.0828** mW; the part uses **1811** times that. The large gap is consistent with a product whose power includes a buffer and references and whose design favors robustness; it is not a red flag by itself, but it shows how much of a data-sheet power figure is outside the converter core (AM2).

### Solution 28-05.3

(a) $\sigma_t = 10^{-70/20}/(2\pi \times 4 \times 10^8)$ = **126** fs. (b) $-20\log_{10}(2\pi \times 10^9 \times 50 \times 10^{-15})$ = **70.1** dB. (c) At 3 GHz, **60.5** dB: tripling the input frequency costs $20\log_{10}3 = 9.5$ dB.

### Solution 28-05.4

At 300 K: $10\log_{10}[1/(16 \times 1.380649 \times 10^{-23} \times 300)]$ = **191.8** dB. At 358.15 K: **191.0** dB. A 193 dB claim exceeds the 300 K ceiling by **1.2** dB. The ceiling applies to rail-to-rail class-B circuits [R-336], so a result above it is possible only if the power is not all counted, the noise is not thermal-limited in the way assumed, or the figure uses dynamic range rather than SNDR (the survey records one DR-based figure 38 dB above its SNDR-based one [R-336]). Ask which SNDR or DR, which bandwidth, and what the power includes.

### Solution 28-05.5

Class B: at half amplitude $\pi/8$ = **39.3**%; at 10 dB $(\pi/4) \times 10^{-0.5}$ = **24.8**%. Doherty: at half amplitude **78.5**%; at 10 dB $(\pi/2) \times 10^{-0.5}$ = **49.7**%. The PA draws $5/0.45$ = **11.1** W and dissipates **6.11** W.

### Solution 28-05.6

$20\log_{10}0.035$ = **−29.1** dB; $20\log_{10}0.025$ = **−32.0** dB; $10^{-38/20}$ = **1.26**%. With $\text{EVM}^2 \approx 1/\text{SNR}$, the SNRs are 29.1, 32.0 and 38 dB.

### Solution 28-05.7

$3000/32$ = **93.75** in³ and $8000/100$ = **80** in³: the 8 kW unit is smaller than the 3 kW one. Loss at 96%: $3000/0.96 - 3000$ = **125** W; at 97.5%, **76.9** W.

### Solution 28-05.8

$0.975 \times 0.97 \times 0.91$ = **86.1**%; input $1200/0.8606$ = **1394** W; loss **194** W. Core regulators $1200/0.91 - 1200$ = **118.7** W; intermediate converter **40.8** W; supply **34.9** W.

### Solution 28-05.9

(a) $(9/6)^2$ = **2.25** and $(9/4.5)^2$ = **4**. (b) $14000/1500$ = **9.33**. (c) $0.99 \times 0.995^{12} \times 0.98$ = **91.4**%. (d) $y^{12} = 0.95/(0.99 \times 0.98)$, so $y$ = **99.82**% per stack.

### Solution 28-05.10

$T_j = 35 + 1200 \times 0.05$ = **95** °C; $P_{max} = (105 - 35)/0.05$ = **1400** W.

### Solution 28-05.11

At 25 °C: $2.21 + 6.464/5 + 1.04$ = **4.54** µA, life $225/0.0045428/8766$ = **5.65** years. At 85 °C: $4.71 + 1.293 + 1.04$ = **7.04** µA, **3.64** years. With less frequent CPU wake-ups, sleep current becomes a larger share, so temperature matters more.

### Solution 28-05.12

(a) $C_{pk} = (4 - 1.5)/(3 \times 0.4)$ = **2.08**; $\Phi(-6.25) \times 10^6$ = **0.000205** ppm.

(b) $C_{pk} = 2.5/2.4$ = **1.04**; $\Phi(-3.125) \times 10^6$ = **889** ppm.

(c) $\chi^2_{0.05;\,29}$ = **17.71**; $\sigma_U = 0.4\sqrt{29/17.71}$ = **0.512** µA; $C_{pk} \ge 2.5/(3 \times 0.512)$ = **1.63**. Thirty parts cannot prove the 2.08 of (a), only about 1.63 with 95% confidence.

### Solution 28-05.13

(a) $\text{FoM}_S = 10\log_{10}\text{SNR} + 10\log_{10}[f_s/(2P)]$. With $P = 8k_BT \cdot \text{SNR} \cdot f_s$, the second term is $10\log_{10}[1/(16k_BT \cdot \text{SNR})]$, so the sum is $10\log_{10}[1/(16k_BT)]$: $f_s$ cancels inside the fraction and SNR cancels between the terms.

(b) A half-sine of peak $I_p$ has mean $I_p/\pi$ and fundamental amplitude $I_p/2$. DC power is $V_{DD}I_p/\pi$ and output power $\tfrac12 V_o (I_p/2)$, so $\eta = (\pi/4)(V_o/V_{DD})$. A carrier amplifier presented with twice the load reaches $V_o = V_{DD}$ when the output amplitude is half its peak; below that its voltage swing relative to $V_{DD}$ is twice what a class-B stage sized for full power would have at the same output, so its efficiency is $(\pi/4) \times 2a = (\pi/2)a$, twice class B, where $a$ is the output amplitude relative to the peak.

(c) If $X \sim N(\mu, \sigma^2)$, $P(X > \text{USL}) = P[Z > (\text{USL} - \mu)/\sigma] = P(Z > 3C_{pk}) = \Phi(-3C_{pk})$. For the bound, $(n-1)s^2/\sigma^2 \sim \chi^2_{n-1}$, so $P[(n-1)s^2/\sigma^2 \ge \chi^2_{1-C;\,n-1}] = C$; rearranging the inequality gives $\sigma \le s\sqrt{(n-1)/\chi^2_{1-C;\,n-1}}$ with probability $C$.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 28-05.2a | ENOB | 11.34 | bits |
| 28-05.2b | Walden figure | 232 | fJ/conv-step |
| 28-05.2c | Schreier figure | 159.2 | dB |
| 28-05.2d | gap to 181.5 dB | 22.3 | dB |
| 28-05.2e | 8kT·SNR power floor | 0.0828 | mW |
| 28-05.2f | ratio to floor | 1811 | — |
| 28-05.3a | jitter for 70 dB at 400 MHz | 126 | fs |
| 28-05.3b | SNR at 1 GHz, 50 fs | 70.1 | dB |
| 28-05.3c | SNR at 3 GHz, 50 fs | 60.5 | dB |
| 28-05.3d | cost of tripling frequency | 9.5 | dB |
| 28-05.4a | ceiling at 300 K | 191.8 | dB |
| 28-05.4b | ceiling at 358.15 K | 191.0 | dB |
| 28-05.4c | claim above the ceiling | 1.2 | dB |
| 28-05.4d | DR-based over SNDR-based figure | 38 | dB |
| 28-05.5a | class B, half amplitude | 39.3 | % |
| 28-05.5b | class B, 10 dB | 24.8 | % |
| 28-05.5c | Doherty, half amplitude | 78.5 | % |
| 28-05.5d | Doherty, 10 dB | 49.7 | % |
| 28-05.5e | DC power | 11.1 | W |
| 28-05.5f | dissipation | 6.11 | W |
| 28-05.6a | 3.5% EVM | −29.1 | dB |
| 28-05.6b | 2.5% EVM | −32.0 | dB |
| 28-05.6c | −38 dB EVM | 1.26 | % |
| 28-05.7a | volume, 3 kW | 93.75 | in³ |
| 28-05.7b | volume, 8 kW | 80 | in³ |
| 28-05.7c | loss at 96% | 125 | W |
| 28-05.7d | loss at 97.5% | 76.9 | W |
| 28-05.8a | chain efficiency | 86.1 | % |
| 28-05.8b | input power | 1394 | W |
| 28-05.8c | total loss | 194 | W |
| 28-05.8d | core-regulator loss | 118.7 | W |
| 28-05.8e | intermediate-converter loss | 40.8 | W |
| 28-05.8f | supply loss | 34.9 | W |
| 28-05.9a | density gain, 9 to 6 µm | 2.25 | — |
| 28-05.9b | density gain, 9 to 4.5 µm | 4 | — |
| 28-05.9c | face-to-face to face-to-back | 9.33 | — |
| 28-05.9d | package yield, twelve stacks | 91.4 | % |
| 28-05.9e | stack survival needed | 99.82 | % |
| 28-05.10a | junction temperature | 95 | °C |
| 28-05.10b | maximum power | 1400 | W |
| 28-05.11a | average current, 25 °C | 4.54 | µA |
| 28-05.11b | battery life, 25 °C | 5.65 | years |
| 28-05.11c | average current, 85 °C | 7.04 | µA |
| 28-05.11d | battery life, 85 °C | 3.64 | years |
| 28-05.12a | Cpk | 2.08 | — |
| 28-05.12b | ppm above limit | 0.000205 | ppm |
| 28-05.12c | Cpk if σ = 0.8 µA | 1.04 | — |
| 28-05.12d | ppm if σ = 0.8 µA | 889 | ppm |
| 28-05.12e | chi-square quantile | 17.71 | — |
| 28-05.12f | upper bound on σ | 0.512 | µA |
| 28-05.12g | Cpk at that bound | 1.63 | — |
