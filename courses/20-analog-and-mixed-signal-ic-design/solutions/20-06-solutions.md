# Solutions 20-06 · Data Converter Fundamentals

Problems: [20-06 problem set](../problems/20-06-problems.md) · Chapter: [20-06](../chapters/20-06-data-converter-fundamentals.md). Every number below is recomputed by [verify_20_06.py](../verify/verify_20_06.py).

---

## Solutions

### Solution 20-06.1

$6.02N + 1.76$: **49.9** dB (8 bits), **62.0** dB (10), **86.0** dB (14) and **98.1** dB (16). At −6 dBFS the signal power falls 6 dB and the quantization noise does not: **92.1** dB.

### Solution 20-06.2

As measured, (70.2 − 1.76)/6.02 = **11.37** bits. Normalized to full scale the SINAD is 71.2 dB and the ENOB **11.53** bits. Data sheets usually quote the normalized value; check the footnote.

### Solution 20-06.3

- Offset error: (48 − 50)/100 = **−0.02** LSB.
- Gain error: [(655 − 48) − 600]/100 = **+0.07** LSB.
- $\Delta_{avg}$ = 607/6 = **101.17** mV.

| Code | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| DNL (LSB) | **+0.008** | **+0.107** | **+0.265** | **−1** | **+0.562** | **+0.058** |

Endpoint INL at transitions 1 to 7: 0, **+0.008**, **+0.115**, **+0.381**, **−0.619**, **−0.058**, 0 LSB. **Code 4 is missing**: $T_4 = T_5$, so it has zero width.

**Check.** The INL jumps by −1 across the missing code, as a running sum of DNL must.

### Solution 20-06.4

INL is the running sum of DNL, starting from zero at the first transition: 0, **+0.2**, **−0.2**, **+0.3**, **+0.2**, **+0.5**, 0 LSB. The DNL sums to zero (as endpoint DNL must), so the last INL returns to zero. The worst case is **0.5** LSB, at transition 6.

### Solution 20-06.5

$\text{DNL}_{mid} = 2^{N-1}\varepsilon$, so $\varepsilon = 0.5/2^{N-1}$: **0.0977**% at 10 bits, **0.0244**% at 12 bits and **0.0061**% at 14 bits. Each two bits demand four times better matching of the MSB.

### Solution 20-06.6

(a) $\sigma_u$ = 1%/√4 = **0.5**%.

(b) $\sigma_u = 0.1/\sqrt{1023}$ = **0.313**%. The area must be (1%/0.313%)² = **10.2** µm², a unit capacitance of **10.2** fF, and the DAC's 1024 units total **10.5** pF.

(c) kT/C needs only 104 fF per side at 10 bits. Matching demands a hundred times more: in this process, **matching, not noise, sets the capacitor** of an uncalibrated 10-bit SAR. Calibration breaks this link: with the mismatch measured and corrected digitally, the capacitor can shrink toward the kT/C limit, saving area and switching energy.

### Solution 20-06.7

(a) $\Delta$ = 0.977 mV and $A$ = 0.505 V. A mid-scale code catches $\Delta/(\pi A)$ of the samples, so 1000 counts need $1000\pi A/\Delta$ = **1.62 × 10⁶** samples.

(b) At 95% of the full-scale amplitude, $v/A$ = 0.95/1.01, and the count is $1000/\sqrt{1 - (v/A)^2}$ = **2945**.

### Solution 20-06.8

The fraction below mid-scale has standard deviation $\tfrac12/\sqrt{10^6}$, and the slope of $T = V_0 - A\cos(\pi C)$ there is $\pi A$, so

$$
\sigma(T_{mid}) = \frac{\pi A}{2\sqrt{N_s}} = \frac{\pi \times 0.505}{2000}\ \text{V} = \textbf{0.812}\ \text{LSB} .
$$

The INL would be uncertain by most of an LSB however good the converter. The tester should sample coherently: choose the sine frequency so the record contains an odd number of cycles co-prime with the record length, which spreads the phases uniformly and deterministically, so the cumulative counts carry no binomial error.

### Solution 20-06.9

- SNR: the noise is −72.5 dBFS and the signal −1.0 dBFS, so SNR = **71.5** dBc, **72.5** dBFS.
- THD: $10\log_{10}(10^{-8.0} + 10^{-7.6})$ = **−74.5** dBc.
- SINAD: $-10\log_{10}(10^{-7.15} + 10^{-7.454})$ = **69.75** dB.
- SFDR: the largest spur is HD3 at −76 dBc (the other spur is −88 dBFS, −87 dBc), so SFDR = **76** dBc.
- ENOB: **11.29** bits as measured, **11.46** bits normalized to full scale.

### Solution 20-06.10

$M = \text{round}(70\text{ MHz} \times 8192/250\text{ MS/s})$ = 2294, which is even, so $M$ = **2295** and $f_{in} = 2295 \times 250\text{ MS/s}/8192$ = **70.0378** MHz. Since 2295 is odd and 8192 = 2¹³, their greatest common divisor is **1**.

### Solution 20-06.11

NSD = −65 − 10 log₁₀(500 MHz) = **−152.0** dBFS/Hz. In 20 MHz the SNR is 65 + 10 log₁₀(500/20) = **79.0** dB, a gain of 14.0 dB or **2.32** bits.

### Solution 20-06.12

(a) The endpoints are $\pm A$, where $v' = \pm(A - a_3A^3)$, so the endpoint line is $v'_{line} = (1 - a_3A^2)v$. The deviation is

$$
(v - a_3v^3) - (1 - a_3A^2)v = a_3v(A^2 - v^2) ,
$$

which peaks where $A^2 - 3v^2 = 0$, at $v = A/\sqrt3$, with value $2a_3A^3/(3\sqrt3)$ = **0.385** $a_3A^3$.

(b) HD3 = $a_3A^2/4$, so $a_3 = 4 \times 10^{-70/20}/A^2$ = **1.98 × 10⁻³** V⁻². The peak INL is 0.385 × 1.98 × 10⁻³ × 0.512 V = **0.389** mV, or **1.00** LSB.

(c) Inverting: an S-shaped INL of exactly 1 LSB gives HD3 = **−70.0** dBc.

**Check.** A useful rule for 12-bit converters: a 1 LSB cubic bow costs 70 dBc of HD3, well below the 74 dB SNR. Static INL predicts low-frequency distortion; at high input frequency, dynamic errors (20-05's switch) usually dominate.

### Solution 20-06.13

| | ENOB | $\text{FoM}_W$ | $\text{FoM}_S$ |
|---|---|---|---|
| C1 | **8.01** | **38.7** fJ/step | **157.0** dB |
| C2 | **11.34** | **3.87** fJ/step | **177.0** dB |
| C3 | **16.32** | **30.6** fJ/step | **183.0** dB |

By Walden: C2, then C3, then C1. By Schreier: C3, then C2, then C1. C3's high resolution costs four times the power per bit if thermal noise limits it, which Schreier allows for and Walden penalizes as if a doubling should suffice. C1 is last by both, but very high-speed designs pay for bandwidth that neither figure rewards.

### Solution 20-06.14

(a) With the exact ideal SNRs (98.09 and 74.01 dB), 16 bits at 1 MS/s: $8kT \times 10^{9.809} \times 10^6$ = **213** µW. 12 bits at 1 GS/s: $8kT \times 10^{7.401} \times 10^9$ = **0.834** mW. The bound is tiny for low-speed precision converters and significant for fast ones.

(b) A class-A driver draws its peak current $CA\omega$ all the time, with $\omega = \pi f_s$ at Nyquist, from a supply of $2A$:

$$
P = 2A \cdot CA\pi f_s = 2\pi A^2Cf_s = 4\pi kT\cdot\text{SNR}\cdot f_s ,
$$

using $A^2C = 2kT\cdot\text{SNR}$. That is **π/2 = 1.571** times the class-B bound, so the $\text{FoM}_S$ limit falls by 1.96 dB to **189.8** dB.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 20-06.1a | SQNR, 8 bits | 49.9 | dB |
| 20-06.1b | SQNR, 10 bits | 62.0 | dB |
| 20-06.1c | SQNR, 14 bits | 86.0 | dB |
| 20-06.1d | SQNR, 16 bits | 98.1 | dB |
| 20-06.1e | 16 bits at −6 dBFS | 92.1 | dB |
| 20-06.2a | ENOB as measured | 11.37 | bits |
| 20-06.2b | ENOB normalized | 11.53 | bits |
| 20-06.3a | offset error | −0.02 | LSB |
| 20-06.3b | gain error | 0.07 | LSB |
| 20-06.3c | average step | 101.17 | mV |
| 20-06.3d | DNL code 1 | 0.008 | LSB |
| 20-06.3e | DNL code 2 | 0.107 | LSB |
| 20-06.3f | DNL code 3 | 0.265 | LSB |
| 20-06.3g | DNL code 4 | −1 | LSB |
| 20-06.3h | DNL code 5 | 0.562 | LSB |
| 20-06.3i | DNL code 6 | 0.058 | LSB |
| 20-06.3j | INL at T2 | 0.008 | LSB |
| 20-06.3k | INL at T3 | 0.115 | LSB |
| 20-06.3l | INL at T4 | 0.381 | LSB |
| 20-06.3m | INL at T5 | −0.619 | LSB |
| 20-06.3n | INL at T6 | −0.058 | LSB |
| 20-06.4a | INL at T2 | 0.2 | LSB |
| 20-06.4b | INL at T3 | −0.2 | LSB |
| 20-06.4c | INL at T4 | 0.3 | LSB |
| 20-06.4d | INL at T5 | 0.2 | LSB |
| 20-06.4e | INL at T6 | 0.5 | LSB |
| 20-06.4f | worst case | 0.5 | LSB |
| 20-06.5a | MSB error, 10 bits | 0.0977 | % |
| 20-06.5b | MSB error, 12 bits | 0.0244 | % |
| 20-06.5c | MSB error, 14 bits | 0.0061 | % |
| 20-06.6a | mismatch of a 4 um^2 unit | 0.5 | % |
| 20-06.6b | required unit mismatch | 0.313 | % |
| 20-06.6c | unit area | 10.2 | µm² |
| 20-06.6d | unit capacitance | 10.2 | fF |
| 20-06.6e | total DAC capacitance | 10.5 | pF |
| 20-06.7a | samples | 1.62e6 | — |
| 20-06.7b | counts at 95% | 2945 | — |
| 20-06.8a | sigma of T mid | 0.812 | LSB |
| 20-06.9a | SNR dBc | 71.5 | dBc |
| 20-06.9b | SNR dBFS | 72.5 | dBFS |
| 20-06.9c | THD | −74.5 | dBc |
| 20-06.9d | SINAD | 69.75 | dB |
| 20-06.9e | SFDR | 76 | dBc |
| 20-06.9f | ENOB measured | 11.29 | bits |
| 20-06.9g | ENOB normalized | 11.46 | bits |
| 20-06.9h | non-harmonic spur in dBc | −87 | dBc |
| 20-06.10a | M | 2295 | — |
| 20-06.10b | coherent frequency | 70.0378 | MHz |
| 20-06.10c | gcd | 1 | — |
| 20-06.11a | NSD | −152.0 | dBFS/Hz |
| 20-06.11b | SNR in 20 MHz | 79.0 | dB |
| 20-06.11c | bits gained | 2.32 | bits |
| 20-06.11d | dB gained | 14.0 | dB |
| 20-06.12a | peak coefficient | 0.385 | — |
| 20-06.12b | a_3 | 1.98e-3 | 1/V² |
| 20-06.12c | peak INL | 0.389 | mV |
| 20-06.12d | peak INL in LSB | 1.00 | LSB |
| 20-06.12e | HD3 for 1 LSB | −70.0 | dBc |
| 20-06.13a | ENOB C1 | 8.01 | bits |
| 20-06.13b | FoM_W C1 | 38.7 | fJ |
| 20-06.13c | FoM_S C1 | 157.0 | dB |
| 20-06.13d | ENOB C2 | 11.34 | bits |
| 20-06.13e | FoM_W C2 | 3.87 | fJ |
| 20-06.13f | FoM_S C2 | 177.0 | dB |
| 20-06.13g | ENOB C3 | 16.32 | bits |
| 20-06.13h | FoM_W C3 | 30.6 | fJ |
| 20-06.13i | FoM_S C3 | 183.0 | dB |
| 20-06.14a | 16-bit minimum power | 213 | µW |
| 20-06.14b | 12-bit minimum power | 0.834 | mW |
| 20-06.14c | class-A factor | 1.571 | — |
| 20-06.14d | class-A FoM_S limit | 189.8 | dB |
| 20-06.14e | class-A penalty | 1.96 | dB |
