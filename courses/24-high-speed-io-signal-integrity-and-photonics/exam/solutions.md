# Course 24 · Final Exam Solutions

Exam: [README.md](README.md). Every number below is recomputed by [verify_24_exam.py](../verify/verify_24_exam.py). About half the values are recomputed by a second route, listed below; the rest are closed-form re-evaluations of the same formulas:

- Question 1(d): the return loss from $S_{11}$ of the impedance step;
- Question 2(c) and 9(d): BERs by numerical integration of the noise density (and, for linear chains, of the convolved densities);
- Question 3(c): the CTLE's gains and frequencies from its transfer function evaluated numerically;
- Question 4(d): the net coding gain with $Q^{-1}$ by root finding;
- Question 8(b): the TIA by nodal analysis at each frequency;
- Question 9(c): the driver–bond–modulator response from complex impedances;
- Questions 10(c), 11(d) and 12(c): failure-rate bounds by root-finding the Poisson probability;
- Question 11(c): the coupling by numerical quadrature of the overlap integral.

---

## Solutions

### Solution 1

(a) PAM4 carries 2 bits per symbol: **106.25** GBd; UI = **9.41** ps; $f_N$ = **53.125** GHz.

(b) $\alpha_d = \pi \times 53.125 \times 10^9 \times \sqrt{3.4} \times 0.002/c$ = 2.05 Np/m; × 8.686 × 0.0254 = **0.453** dB/in. $\alpha_c = 36\sqrt{53.125}/(4 \times 50)$ = **1.31** dB/in. Total **1.76** dB/in; 8 inches lose **14.1** dB.

(c) $f = c/(4\ell\sqrt{\varepsilon_r})$: **135** GHz for 0.3 mm and **40.6** GHz for 1.0 mm, inside the band. For $f \ge 106.25$ GHz, $\ell \le c/(4 \times 106.25\ \text{GHz} \times \sqrt{3.4})$ = **0.383** mm: back-drill the longer stub.

(d) $\Gamma = (92 - 100)/(92 + 100)$ = **−0.0417**; RL = $-20\log_{10}0.0417$ = **27.6** dB.

### Solution 2

(a) ISI sum $0.04 + 0.18 + 0.06 + 0.02$ = 0.30 V. NRZ: $0.60 - 0.30$ = **0.30** V. PAM4: $0.60/3 - 0.30$ = **−0.10** V: closed.

(b) Only $h_{-1}$ remains: NRZ **0.56** V; PAM4 $0.20 - 0.04$ = **0.16** V.

(c) $0.16/(2 \times 0.012)$ = **6.67**; BER = $\tfrac34Q(6.67)$ = **9.8** × 10⁻¹².

(d) TJ = $14.07 \times 0.15 + 1.2$ = **3.31** ps. The UI is 9.41 ps, so the eye is **6.10** ps = **0.648** UI. At 10⁻⁶, $2 \times 4.75 \times 0.15 + 1.2$ = **2.63** ps.

### Solution 3

(a) $106.25/8$ = **13.3** GHz; $360°/8$ = **45**°, one UI.

(b) $I = 1.0\ \text{V}/50\ \Omega$ = **20** mA; $P_{CML} = 0.9 \times 20$ mA = **18** mW. $P_{SST} = 1.0^2/200$ = **5.0** mW. Ratio **3.6**.

(c) $1 + g_mR_S/2$ = 5.0, **14.0** dB. $f_z = 1/(2\pi R_SC_S)$ = **1.99** GHz; $f_{p1} = 5f_z$ = **9.95** GHz. DC gain $g_mR_D/5$ = **1.0**; high-frequency gain $g_mR_D$ = **5.0**.

(d) $\Delta f_{baud}/(2\pi f_c) = 2 \times 10^{-4} \times 106.25 \times 10^9/(2\pi \times 2 \times 10^7)$ = **0.169** UI.

### Solution 4

(a) $-20\log_{10}(2\pi \times 53.125\ \text{GHz} \times 50\ \text{fs})$ = **35.6** dB; ENOB = **5.61** bits.

(b) $212.5/128$ = **1.66** GS/s.

(c) $10\log_{10}(1 + 0.7^2)$ = **1.73** dB.

(d) $20\log_{10}(7.94/3.49) + 10\log_{10}(514/544)$ = **6.89** dB. A codeword is 544 ten-bit symbols: $5440/212.5\ \text{Gb/s}$ = **25.6** ns.

### Solution 5

(a) $16 \times 32 \times 10^9 \times (128/130)/8$ = **63.0** GB/s.

(b) $128/152$ = **84.2**%; **53.1** GB/s.

(c) $63.0\ \text{GB/s} \times 500$ ns = **31.5** kB.

(d) $200 \times (257/256) \times (544/514)$ = **212.5** Gb/s. $k^2/2$: **2,048** hosts at radix 64 and **131,072** at radix 512.

### Solution 6

(a) $CV^2/4 = 150\ \text{fF} \times 0.16/4$ = **6.0** fJ; at 32 Gb/s, **0.192** mW.

(b) $V^2/(4Rf_b) = 0.16/(4 \times 50 \times 32 \times 10^9)$ = **25** fJ.

(c) $0.5 \times 32/(8 \times 0.036^2)$ = **1,543** GB/s/mm², about 1.5 TB/s/mm².

(d) $2 \times 10^{12} \times 8 \times 0.3$ pJ = **4.8** W; at 5 pJ/bit, **80** W.

### Solution 7

(a) $0.85q\lambda/hc$ = **0.898** A/W; −8 dBm = **158** µW; $I$ = **142** µA.

(b) $(1.31\ \mu\text{m})^2 \times 106.25\ \text{GHz}/c$ = **0.608** nm; $3.5 \times 2 \times 0.608$ = **4.26** ps = **0.45** UI.

(c) $\cos^2(\pi/4 \mp 0.15\pi)$: **0.905** and **0.0955**; ER = **9.47** = **9.76** dB; OMA = **0.809** $P_{in}$.

(d) σ = $18 \times 10^{-12}\sqrt{55 \times 10^9}$ = **4.22** µA. $P = 3.49 \times 4.22/0.85$ = **17.3** µW = **−17.6** dBm. ER = $10^{0.4}$ = 2.51: penalty **3.66** dB. PAM4: $-17.6 + 4.77 + 3.66$ = **−9.2** dBm.

### Solution 8

(a) $3 - 0.72 - 1.0 - 3.6$ = **−2.32** dBm; margin $-2.32 - (-9.2)$ = **6.9** dB.

(b) $Z_T = R_FA/(1 + A)$ = **554** Ω; $f_{3dB} = (1 + A)/(2\pi R_FC_{in})$ = **38.3** GHz; $\sqrt{4kT/R_F}$ = **5.26** pA/√Hz; over 38.3 GHz, **1.03** µA.

(c) $\lambda^2\Delta f/c$ = **4.58** nm; $c\Delta\lambda/\lambda^2$ = **786** GHz.

(d) $1310 \times 1.8 \times 10^{-4}/3.9$ = **0.0605** nm/K; $1310/7500$ = **0.175** nm; **2.89** K.

### Solution 9

(a) $(2 \times 4.6 \times 2.5/(4.6^2 + 2.5^2))^2$ = **0.704**, **−1.52** dB; offset $\exp(-2 \times 0.8^2/27.41)$ = **0.954**, **−0.20** dB; total **−1.73** dB.

(b) $1310/(2.75 - \sin 12°)$ = **515** nm; $1/(\Lambda\cos 12°)$ = **0.114**°/nm; **2.27**° over 20 nm.

(c) $f_0 = 1/(2\pi\sqrt{LC})$ = **65.0** GHz; ζ = $25\sqrt{30\ \text{fF}/0.2\ \text{nH}}$ = **0.306**; peak $1/(2\zeta\sqrt{1 - \zeta^2})$ = **1.72** = **4.69** dB at $f_0\sqrt{1 - 2\zeta^2}$ = **58.6** GHz; $f_{3dB}$ = **94.2** GHz.

(d) $1/\sqrt{2/64 + 1/49}$ = **4.40**; BER **5.4** × 10⁻⁶. Retimed: $2Q(8) + Q(7)$ = **1.3** × 10⁻¹².

### Solution 10

(a) $4/800$ Gb/s = **5.0** pJ/bit; $14/800$ Gb/s = **17.5** pJ/bit; saving $1 - 4/14$ = **71**%.

(b) $17 - 2 - 1 - 2$ = **12.0** dB, a factor of **15.8**: **8** lanes.

(c) $3.00/(3 \times 10^6)$ h = **1.0e3** FIT; with one failure $4.744/(3 \times 10^6)$ h = **1.58e3** FIT.

(d) $(300 \times 16 \times 8/16)/(150 \times 0.5)$ = **32**.

### Solution 11

(a) For a TEM line in a dielectric, $Z_0 = \sqrt{L'/C'}$ and $\sqrt{L'C'} = \sqrt{\varepsilon_r}/c$. Then

$$
\alpha_d = \frac{G'Z_0}{2} = \frac{\omega C'\tan\delta}{2}\sqrt{\frac{L'}{C'}} = \frac{\omega\tan\delta}{2}\sqrt{L'C'} = \frac{2\pi f\tan\delta}{2}\cdot\frac{\sqrt{\varepsilon_r}}{c} = \frac{\pi f\sqrt{\varepsilon_r}\tan\delta}{c}.
$$

At 26.5625 GHz, $\varepsilon_r$ = 3.0, $\tan\delta$ = 0.0015: 0.723 Np/m × 8.686 × 0.0254 = **0.160** dB/in.

(b) The half circuit's source impedance is $Z_S = (R_S/2) \parallel (1/2sC_S) = (R_S/2)/(1 + sR_SC_S)$. With degeneration, the drain current is $g_mv_{in}/(1 + g_mZ_S)$, so

$$
H(s) = -\frac{g_mR_D}{1 + g_mZ_S} = -\frac{g_mR_D(1 + sR_SC_S)}{1 + g_mR_S/2 + sR_SC_S}.
$$

At $s = 0$, $H(0) = g_mR_D/(1 + g_mR_S/2)$; as $s \to \infty$, $Z_S \to 0$ and $H(\infty) = g_mR_D$. Their ratio is $1 + g_mR_S/2$. With 30 mS and 300 Ω: **5.5**, **14.8** dB.

(c) With $E_i = e^{-r^2/w_i^2}$, $\iint E_1E_2\,dA = \pi/(1/w_1^2 + 1/w_2^2) = \pi w_1^2w_2^2/(w_1^2 + w_2^2)$ and $\iint E_i^2\,dA = \pi w_i^2/2$. So

$$
\eta = \frac{(\pi w_1^2w_2^2/(w_1^2 + w_2^2))^2}{(\pi w_1^2/2)(\pi w_2^2/2)} = \left(\frac{2w_1w_2}{w_1^2 + w_2^2}\right)^2.
$$

For 4.6 and 3.0 µm: **0.837**, **−0.77** dB.

(d) Each segment adds independent zero-mean Gaussian noise $\sigma_i$ to a common half-eye $a$, with $Q_i = a/\sigma_i$. The sum of independent Gaussians is Gaussian with variance $\sum\sigma_i^2$, so $Q = a/\sqrt{\sum\sigma_i^2}$ and $1/Q^2 = \sum\sigma_i^2/a^2 = \sum 1/Q_i^2$. For 9, 7, 9: $Q$ = **4.71**, BER = **1.2** × 10⁻⁶.

With exponential lifetimes, failures in $T$ device-hours are Poisson with mean $\lambda T$, so $P(0) = e^{-\lambda T}$. The 95% upper bound is the rate at which seeing none has probability 0.05: $\lambda_U = -\ln(0.05)/T$. For $5 \times 10^6$ h: **599** FIT.

### Solution 12

(a) $8/1.6$ Tb/s = **5.0** pJ/bit; $25/1.6$ Tb/s = **15.6** pJ/bit. $4 \times 10^5$ modules: **10** MW with DSP modules and **3.2** MW with LPO; saving **6.8** MW.

(b) $1/Q^2 = 2/121 + 1/42.25$: $Q$ = **4.99**, BER = **3.1** × 10⁻⁷, margin $20\log_{10}(4.99/3.49)$ = **3.1** dB. 10⁻¹² needs $Q$ = **7.03**. The claim is inconsistent with the stated segment $Q$s: the optical segment alone ($Q$ = 6.5) is worse than 10⁻¹². The link can work with FEC, not pre-FEC at 10⁻¹².

(c) $3.00/(2 \times 10^6)$ h = **1.5e3** FIT, from **228** device-years. "Below 100 FIT" needs about $3.00/(100 \times 10^{-9})$ = **30** million failure-free device-hours.

(d) Rubric (3 points for four good questions with strong answers):

1. *"What is the BER before FEC, measured end to end with which host SerDes, across temperature and over how many host–module pairings?"* Strong: measured pre-FEC BER distributions, named hosts, worst case across corners.
2. *"Is 8 W typical or maximum, and what does the host SerDes spend on the extra equalization?"* Strong: both figures, and the host's incremental power, so the system saving is net.
3. *"What reliability exposure and failure data do you have, in the field and in the lab?"* Strong: device-hours, failures, confidence bounds, failure mechanisms.
4. *"How do you qualify interoperability with other hosts and modules, and what does the LPO MSA specify for 200 Gb/s lanes?"* Strong: compliance tests, multi-vendor results, a roadmap for 200 Gb/s specifications.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| X24.1a | symbol rate | 106.25 | GBd |
| X24.1a1 | unit interval | 9.41 | ps |
| X24.1a2 | Nyquist frequency | 53.125 | GHz |
| X24.1b0 | dielectric loss | 2.05 | Np/m |
| X24.1b | dielectric loss | 0.453 | dB/in |
| X24.1b1 | conductor loss | 1.31 | dB/in |
| X24.1b2 | total | 1.76 | dB/in |
| X24.1b3 | 8 inches | 14.1 | dB |
| X24.1c | notch, 0.3 mm | 135 | GHz |
| X24.1c1 | notch, 1.0 mm | 40.6 | GHz |
| X24.1c2 | longest stub | 0.383 | mm |
| X24.1d | reflection coefficient | -0.0417 | |
| X24.1d1 | return loss | 27.6 | dB |
| X24.2a0 | ISI sum | 0.30 | V |
| X24.2a | NRZ eye | 0.30 | V |
| X24.2a1 | PAM4 eye | -0.10 | V |
| X24.2b | NRZ eye after DFE | 0.56 | V |
| X24.2b1 | PAM4 eye after DFE | 0.16 | V |
| X24.2c | V_eye/2 sigma | 6.67 | |
| X24.2c1 | BER | 9.8e-12 | |
| X24.2d | TJ at 1e-12 | 3.31 | ps |
| X24.2d1 | eye width | 6.10 | ps |
| X24.2d2 | eye width | 0.648 | UI |
| X24.2d3 | TJ at 1e-6 | 2.63 | ps |
| X24.3a | clock | 13.3 | GHz |
| X24.3a1 | phase spacing | 45 | ° |
| X24.3b | CML current | 20 | mA |
| X24.3b1 | CML power | 18 | mW |
| X24.3b2 | SST power | 5.0 | mW |
| X24.3b3 | ratio | 3.6 | |
| X24.3c0 | peaking ratio | 5.0 | |
| X24.3c | peaking | 14.0 | dB |
| X24.3c1 | zero | 1.99 | GHz |
| X24.3c2 | first pole | 9.95 | GHz |
| X24.3c3 | DC gain | 1.0 | |
| X24.3c4 | HF gain | 5.0 | |
| X24.3d | phase error | 0.169 | UI |
| X24.4a | SNR | 35.6 | dB |
| X24.4a1 | ENOB | 5.61 | bits |
| X24.4b | slice rate | 1.66 | GS/s |
| X24.4c | MLSD gain | 1.73 | dB |
| X24.4d | NCG | 6.89 | dB |
| X24.4d1 | codeword time | 25.6 | ns |
| X24.5a | PCIe 5.0 x16 | 63.0 | GB/s |
| X24.5b | TLP efficiency | 84.2 | % |
| X24.5b1 | effective bandwidth | 53.1 | GB/s |
| X24.5c | credit buffer | 31.5 | kB |
| X24.5d | lane rate | 212.5 | Gb/s |
| X24.5d1 | hosts at radix 64 | 2048 | |
| X24.5d2 | hosts at radix 512 | 131072 | |
| X24.6a | unterminated energy | 6.0 | fJ |
| X24.6a1 | power at 32 Gb/s | 0.192 | mW |
| X24.6b | terminated energy | 25 | fJ |
| X24.6c | areal density | 1543 | GB/s/mm² |
| X24.6c1 | areal density | 1.5 | TB/s/mm² |
| X24.6d | die-to-die power | 4.8 | W |
| X24.6d1 | SerDes power | 80 | W |
| X24.7a | responsivity | 0.898 | A/W |
| X24.7a1 | power | 158 | µW |
| X24.7a2 | photocurrent | 142 | µA |
| X24.7b | spectral width | 0.608 | nm |
| X24.7b1 | spread | 4.26 | ps |
| X24.7b2 | spread in UI | 0.45 | UI |
| X24.7c | high level | 0.905 | |
| X24.7c1 | low level | 0.0955 | |
| X24.7c2 | extinction ratio | 9.47 | |
| X24.7c3 | extinction ratio in dB | 9.76 | dB |
| X24.7c4 | OMA | 0.809 | |
| X24.7d | sigma | 4.22 | µA |
| X24.7d1 | OOK sensitivity | 17.3 | µW |
| X24.7d2 | OOK sensitivity | -17.6 | dBm |
| X24.7d3 | ER penalty | 3.66 | dB |
| X24.7d4 | PAM4 sensitivity | -9.2 | dBm |
| X24.8a | received power | -2.32 | dBm |
| X24.8a1 | margin | 6.9 | dB |
| X24.8b | transimpedance | 554 | Ω |
| X24.8b1 | bandwidth | 38.3 | GHz |
| X24.8b2 | RF noise density | 5.26 | pA/√Hz |
| X24.8b3 | RF noise current | 1.03 | µA |
| X24.8c | 800 GHz spacing | 4.58 | nm |
| X24.8c1 | 4.5 nm spacing | 786 | GHz |
| X24.8d | shift per kelvin | 0.0605 | nm/K |
| X24.8d1 | linewidth | 0.175 | nm |
| X24.8d2 | kelvin per linewidth | 2.89 | K |
| X24.9a | coupling | 0.704 | |
| X24.9a1 | coupling loss | -1.52 | dB |
| X24.9a2 | offset factor | 0.954 | |
| X24.9a3 | offset loss | -0.20 | dB |
| X24.9a4 | total | -1.73 | dB |
| X24.9b | period | 515 | nm |
| X24.9b1 | angular dispersion | 0.114 | °/nm |
| X24.9b2 | steer over 20 nm | 2.27 | ° |
| X24.9c | natural frequency | 65.0 | GHz |
| X24.9c1 | damping ratio | 0.306 | |
| X24.9c2 | peak gain | 1.72 | |
| X24.9c3 | peaking | 4.69 | dB |
| X24.9c4 | peak frequency | 58.6 | GHz |
| X24.9c5 | bandwidth | 94.2 | GHz |
| X24.9d | linear Q | 4.40 | |
| X24.9d1 | linear BER | 5.4e-6 | |
| X24.9d2 | retimed BER | 1.3e-12 | |
| X24.10a | CPO energy per bit | 5.0 | pJ/bit |
| X24.10a1 | pluggable energy per bit | 17.5 | pJ/bit |
| X24.10a2 | saving | 71 | % |
| X24.10b | available for splitting | 12.0 | dB |
| X24.10b1 | split factor | 15.8 | |
| X24.10b2 | lanes | 8 | |
| X24.10c | bound, no failures | 1.0e3 | FIT |
| X24.10c1 | bound, one failure | 1.58e3 | FIT |
| X24.10d | port-hours ratio | 32 | |
| X24.11a0 | dielectric loss | 0.723 | Np/m |
| X24.11a | dielectric loss | 0.160 | dB/in |
| X24.11b | peaking ratio | 5.5 | |
| X24.11b1 | peaking | 14.8 | dB |
| X24.11c | coupling | 0.837 | |
| X24.11c1 | coupling loss | -0.77 | dB |
| X24.11d | linear Q | 4.71 | |
| X24.11d1 | linear BER | 1.2e-6 | |
| X24.11d2 | bound for 5 M h | 599 | FIT |
| X24.12a | LPO energy per bit | 5.0 | pJ/bit |
| X24.12a1 | DSP energy per bit | 15.6 | pJ/bit |
| X24.12a2 | DSP modules total | 10 | MW |
| X24.12a3 | LPO modules total | 3.2 | MW |
| X24.12a4 | saving | 6.8 | MW |
| X24.12b | linear Q | 4.99 | |
| X24.12b1 | linear BER | 3.1e-7 | |
| X24.12b2 | margin | 3.1 | dB |
| X24.12b3 | Q for 1e-12 | 7.03 | |
| X24.12c | bound | 1.5e3 | FIT |
| X24.12c1 | device-years | 228 | |
| X24.12c2 | hours for 100 FIT | 30 | million h |
