# Solutions 21-03 · Noise Figure and Linearity

Problems: [21-03 problem set](../problems/21-03-problems.md) · Chapter: [21-03](../chapters/21-03-noise-figure-and-linearity.md). Every number below is recomputed by [verify_21_03.py](../verify/verify_21_03.py).

---

## Solutions

### Solution 21-03.1

Gain = −5 − (−25) = **20** dB. $\text{IIP3} = -25 + (-5 + 63)/2$ = **4** dBm, and $\text{OIP3} = 4 + 20$ = **24** dBm. At −35 dBm per tone, IM3 = $-2(4 + 35)$ = **−78** dBc; the output tones are −15 dBm, so the output IM3 is **−93** dBm.

*Check:* from −25 to −35 dBm the output IM3 fell from −63 to −93 dBm, 30 dB for 10 dB: slope 3.

### Solution 21-03.2

$\text{IIP2} = P_{in} + (P_{fund} - P_{IM2}) = -30 + 42$ = **12** dBm. IM2 grows with slope 2, so relative to the tones it is $-(\text{IIP2} - P_{in})$ dBc: at −40 dBm, **−52** dBc. The output tones are −20 dBm, so the output IM2 is **−72** dBm (20 dB below its −52 dBm at −30 dBm input: slope 2).

### Solution 21-03.3

ENR = $10^{0.6}$ = 3.981 and $Y = 10^{0.32}$ = 2.089, so $F = 3.981/1.089$ = 3.655: NF = **5.63** dB, and $T_e = (3.655 - 1) \times 290$ = **770** K. A 15 dB source would give $Y = 31.62/3.655 + 1$ = 9.652, or **9.85** dB.

*Comment:* both are usable: the noise figure is well within 10 dB of either ENR. The larger Y of the 15 dB source makes the ratio easier to read accurately; the 6 dB source changes its own output match less between on and off, which matters for devices whose noise depends strongly on source impedance.

### Solution 21-03.4

$\lvert a_1/a_3\rvert$ = 5 V². $A_{1dB} = \sqrt{0.145 \times 5}$ = **0.851** V and $A_{IIP3} = \sqrt{(4/3) \times 5}$ = **2.582** V; their ratio is $20\log_{10}(2.582/0.851)$ = **9.64** dB, as for any cubic. $\text{HD}_3 = \tfrac14\lvert a_3/a_1\rvert A^2 = 0.25 \times 0.2 \times 0.01$ = **0.05**%.

### Solution 21-03.5

$r_n = 20/50$ = 0.4, $F_{min} = 10^{0.12}$ = 1.318, $\Gamma_{opt} = -0.25 + j0.433$ and $\lvert 1 + \Gamma_{opt}\rvert^2 = 0.75^2 + 0.433^2$ = 0.75.

- 50 Ω: $F = 1.318 + 4(0.4)(0.25)/0.75$ = 1.852, NF = **2.68** dB.
- $\Gamma_s = j0.5$: $\lvert\Gamma_s - \Gamma_{opt}\rvert^2 = 0.25^2 + 0.067^2$ = 0.0670 and $1 - \lvert\Gamma_s\rvert^2$ = 0.75, so $F = 1.318 + 1.6 \times 0.0670/(0.75 \times 0.75)$ = 1.509, NF = **1.79** dB.
- 2.0 dB circle: $N = (1.585 - 1.318)(0.75)/1.6$ = 0.125; centre $0.5/1.125$ = **0.444**∠120°, radius $\sqrt{0.125(1.125 - 0.25)}/1.125$ = **0.294**.
- $Z_{opt} = 50(1 + \Gamma_{opt})/(1 - \Gamma_{opt})$ = **21.4** + j**24.7** Ω.

*Interpretation:* with $R_n$ = 20 Ω this device is sensitive: a 50 Ω source costs 1.48 dB, while a source only 30° away from $\Gamma_{opt}$ at the same magnitude costs 0.59 dB.

### Solution 21-03.6

- $R_n = e_n^2/(4kT_0) = (0.5 \times 10^{-9})^2/(1.6016 \times 10^{-20})$ = **15.6** Ω; $G_u = i_u^2/(4kT_0)$ = **0.250** mS.
- $G_{opt} = \sqrt{G_u/R_n + G_{cor}^2} = \sqrt{1.60 \times 10^{-5} + 4 \times 10^{-6}}$ = **4.47** mS, $B_{opt} = -B_{cor}$ = **−10** mS, so $Y_{opt}$ = (4.47 − j10) mS and $Z_{opt} = 1/Y_{opt}$ = **37.3** + j**83.3** Ω.
- $F_{min} = 1 + 2R_n(G_{opt} + G_{cor}) = 1 + 2(15.6)(0.00647)$ = 1.202: $\text{NF}_{min}$ = **0.80** dB.
- With 50 Ω ($G_s$ = 20 mS, $B_s$ = 0): $F = 1 + [G_u + R_n((G_s + G_{cor})^2 + B_{cor}^2)]/G_s = 1 + [0.00025 + 15.6(0.000484 + 0.0001)]/0.02$ = 1.468: NF = **1.67** dB.

*Check:* $F = F_{min} + (R_n/G_s)\lvert Y_s - Y_{opt}\rvert^2 = 1.202 + (15.6/0.02) \times \left[(0.02 - 0.00447)^2 + 0.01^2\right]$ = 1.468, the same.

### Solution 21-03.7

Filter first: $F = 1.778 + (1.259 - 1)/0.562 + (7.943 - 1)/(0.562 \times 63.1) + (15.85 - 1)/(0.562 \times 63.1 \times 10)$ = 2.476, NF = **3.94** dB. In mW, $1/\text{IIP3} = 0.562/0.1 + 0.562 \times 63.1/6.31 + 0.562 \times 631/100$ = 5.62 + 5.62 + 3.55, IIP3 = **−11.7** dBm.

Filter after the LNA: $F = 1.259 + (1.778 - 1)/63.1 + (7.943 - 1)/(63.1 \times 0.562) + (15.85 - 1)/(63.1 \times 0.562 \times 10)$ = 1.509, NF = **1.79** dB; $1/\text{IIP3} = 10 + 0.002 + 5.62 + 3.55$, IIP3 = **−12.8** dBm.

Moving the filter gains 2.15 dB of noise figure and loses 1.1 dB of in-band IIP3. The larger cost is not in these numbers: the LNA now sees every out-of-band signal at the antenna unattenuated, so strong out-of-band blockers can compress it or intermodulate in it. That is why handsets keep a filter or duplexer ahead of the LNA and buy back noise figure with a lower-loss filter.

### Solution 21-03.8

$\text{NF} = -96.5 - (-173.98 + 60 + 10)$ = **7.48** dB. With NF = 6 dB the sensitivity would be $-173.98 + 60 + 6 + 10$ = **−97.98** dBm. Against a −70 dBm requirement, −96.5 dBm has **26.5** dB of margin.

*Comment:* the 10 dB SNR and 1 MHz bandwidth are assumptions of this problem, not a standard's numbers. The large margin is typical of Bluetooth LE chips, which is why vendors compete on sensitivity well beyond the requirement (§9).

### Solution 21-03.9

$A_B^2/A_{IIP3}^2 = 10^{(-20 + 5)/10}$ = 0.0316, so the gain changes by $20\log_{10}(1 - 2 \times 0.0316)$ = **−0.567** dB. For a 1 dB reduction, $1 - 2r = 10^{-1/20}$ gives $r$ = 0.0544, a blocker of $-5 + 10\log_{10}0.0544$ = **−17.65** dBm. The cubic model's own compression point is $-5 - 9.64$ = **−14.64** dBm: the blocker desensitizes at a power **3.01** dB lower, because its cross term carries twice the coefficient of self-compression.

### Solution 21-03.10

Thermal floor: $-173.98 + 10\log_{10}(18 \times 10^6) + 6$ = **−95.42** dBm. A 1 dB rise allows reciprocal-mixing noise of $(10^{0.1} - 1)$ = 0.259 of it: **−101.29** dBm. Then $\mathcal{L} \le -101.29 + 40 - 72.55$ = **−133.8** dBc/Hz at the blocker's offset.

### Solution 21-03.11

$V_T = kT/q$: 20.09 mV at 233.15 K and 34.31 mV at 398.15 K. $A_{IIP3} = \sqrt8\,V_T$ = **56.83** mV (**−14.91** dBm) at −40 °C and **97.04** mV (**−10.26** dBm) at 125 °C. A hot transistor is more linear for a given input voltage, because its exponential is gentler. At 300 K a 2 mV tone has $x$ = 0.07736: $\text{HD}_2 = x/4$ = **1.9341**% from the series and $I_2(x)/I_1(x)$ = **1.9336**% exactly.

### Solution 21-03.12

(a) Solving $\overline{\tanh}(u)/u = 10^{-1/20}$, where $\overline{\tanh}(u)$ is the fundamental of $\tanh(u\cos\theta)$, gives $u$ = 0.7127, so $A_{1dB} = 2V_Tu$ = **1.4254** $V_T$, against **1.3191** $V_T$ from the cubic model: 0.67 dB more.

(b) At 20 mV per tone ($A/V_T$ = 0.7736), the series gives $(A/V_T)^2/16$, **−28.54** dBc; the exact two-tone FFT gives **−29.64** dBc.

The tanh series is $u - u^3/3 + 2u^5/15 - \cdots$. The fifth-order term opposes the cubic one and grows two powers of the amplitude faster, so at 20 mV it corrects the cubic estimate by more than 1 dB, while at 10 mV (Example 21-03.4) it corrected it by only 0.29 dB.

### Solution 21-03.13

The thermal floor is $-173.98 + 66.53 + 9$ = **−98.44** dBm, so the IM2 product must stay below −108.44 dBm. The leakage at the receiver input is $23 - 50$ = −27 dBm. With slope 2, the input-referred IM2 is $2P_{leak} - \text{IIP2}$, so

$$
\text{IIP2} \ge 2(-27) + 108.44 = \mathbf{54.4}\ \text{dBm} .
$$

With 55 dB of isolation the leakage is −32 dBm and IIP2 ≥ **44.4** dBm: 5 dB of isolation relaxes IIP2 by 10 dB.

*What the simplification misses:* a modulated leak's second-order product is its squared envelope, a DC term plus a spectrum about twice the transmit bandwidth wide. Only part falls in the receive channel after DC removal, which makes the two-tone estimate pessimistic; the envelope's peak-to-average ratio makes it optimistic. Designs check the real waveform. The transmitter's own noise in the receive band is a separate FDD problem that IIP2 does not address.

### Solution 21-03.14

(a) $A_{IIP3,1} = \sqrt{(4/3)(5/0.5)}$ = **3.651** V and $A_{IIP3,2} = \sqrt{(4/3)(4/0.2)}$ = **5.164** V. The formula gives $1/A^2 = 1/3.651^2 + 5^2/5.164^2$ = 0.075 + 0.9375, so $A_{IIP3}$ = **0.9938** V. The second stage dominates: it sees five times the voltage.

(b) Substituting, the cascade's coefficients are $c_1 = a_1b_1$ = 20 and $c_3 = a_3b_1 + b_3a_1^3 = -2 - 25$ = **−27**, so $A_{IIP3} = \sqrt{(4/3)(20/27)}$ = **0.9938** V: the terms have the same sign and the formula is exact.

(c) With $b_3$ = +0.2, $c_3 = -2 + 25$ = **23** and $A_{IIP3}$ = **1.077** V. The formula assumes the stages' cubic terms add in phase. When they have opposite signs, or in RF circuits arrive with different phases, they partly cancel and the formula is pessimistic. The lab's two-tone FFT of the composite polynomial confirms both values at small amplitude.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 21-03.1a | gain | 20 | dB |
| 21-03.1b | IIP3 | 4 | dBm |
| 21-03.1c | OIP3 | 24 | dBm |
| 21-03.1d | IM3 at −35 dBm | −78 | dBc |
| 21-03.1e | output IM3 at −35 dBm | −93 | dBm |
| 21-03.2a | IIP2 | 12 | dBm |
| 21-03.2b | IM2 at −40 dBm | −52 | dBc |
| 21-03.2c | output IM2 at −40 dBm | −72 | dBm |
| 21-03.3a | noise figure | 5.63 | dB |
| 21-03.3b | noise temperature | 770 | K |
| 21-03.3c | Y with a 15 dB source | 9.85 | dB |
| 21-03.4a | 1 dB amplitude | 0.851 | V |
| 21-03.4b | IIP3 amplitude | 2.582 | V |
| 21-03.4c | ratio | 9.64 | dB |
| 21-03.4d | HD3 at 0.1 V | 0.05 | % |
| 21-03.5a | NF with 50 ohm | 2.68 | dB |
| 21-03.5b | NF at 0.5 at 90 degrees | 1.79 | dB |
| 21-03.5c | 2.0 dB circle centre magnitude | 0.444 | — |
| 21-03.5d | 2.0 dB circle radius | 0.294 | — |
| 21-03.5e | Re Zopt | 21.4 | Ω |
| 21-03.5f | Im Zopt | 24.7 | Ω |
| 21-03.5g | cost of 50 ohm over the minimum | 1.48 | dB |
| 21-03.5h | cost at 0.5 at 90 degrees | 0.59 | dB |
| 21-03.6a | Rn | 15.6 | Ω |
| 21-03.6b | Gu | 0.250 | mS |
| 21-03.6c | Gopt | 4.47 | mS |
| 21-03.6d | Bopt | −10 | mS |
| 21-03.6e | Re Zopt | 37.3 | Ω |
| 21-03.6f | Im Zopt | 83.3 | Ω |
| 21-03.6g | NFmin | 0.80 | dB |
| 21-03.6h | NF with 50 ohm | 1.67 | dB |
| 21-03.7a | NF, filter first | 3.94 | dB |
| 21-03.7b | IIP3, filter first | −11.7 | dBm |
| 21-03.7c | NF, filter after LNA | 1.79 | dB |
| 21-03.7d | IIP3, filter after LNA | −12.8 | dBm |
| 21-03.7e | NF gained | 2.15 | dB |
| 21-03.7f | IIP3 lost | 1.1 | dB |
| 21-03.8a | NF for −96.5 dBm | 7.48 | dB |
| 21-03.8b | sensitivity with NF 6 dB | −97.98 | dBm |
| 21-03.8c | margin over −70 dBm | 26.5 | dB |
| 21-03.9a | gain change | −0.567 | dB |
| 21-03.9b | blocker for 1 dB | −17.65 | dBm |
| 21-03.9c | cubic P1dB | −14.64 | dBm |
| 21-03.9d | difference | 3.01 | dB |
| 21-03.10a | thermal floor | −95.42 | dBm |
| 21-03.10b | allowed reciprocal-mixing noise | −101.29 | dBm |
| 21-03.10c | phase noise | −133.8 | dBc/Hz |
| 21-03.11a | IIP3 amplitude at −40 C | 56.83 | mV |
| 21-03.11b | IIP3 at −40 C | −14.91 | dBm |
| 21-03.11c | IIP3 amplitude at 125 C | 97.04 | mV |
| 21-03.11d | IIP3 at 125 C | −10.26 | dBm |
| 21-03.11e | HD2 series, 2 mV | 1.9341 | % |
| 21-03.11f | HD2 exact, 2 mV | 1.9336 | % |
| 21-03.12a | exact 1 dB amplitude | 1.4254 | V_T |
| 21-03.12b | cubic 1 dB amplitude | 1.3191 | V_T |
| 21-03.12c | IM3 at 20 mV, series | −28.54 | dBc |
| 21-03.12d | IM3 at 20 mV, exact | −29.64 | dBc |
| 21-03.12e | series correction at 10 mV | 0.29 | dB |
| 21-03.13a | thermal floor | −98.44 | dBm |
| 21-03.13b | IIP2 required | 54.4 | dBm |
| 21-03.13c | IIP2 with 55 dB isolation | 44.4 | dBm |
| 21-03.14a | stage 1 IIP3 amplitude | 3.651 | V |
| 21-03.14b | stage 2 IIP3 amplitude | 5.164 | V |
| 21-03.14c | cascade IIP3 amplitude | 0.9938 | V |
| 21-03.14d | cascade c3 | −27 | — |
| 21-03.14e | cascade c3 with b3 positive | 23 | — |
| 21-03.14f | cascade IIP3 amplitude with b3 positive | 1.077 | V |
