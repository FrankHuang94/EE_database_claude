# Course 20 · Final Exam Solutions (Analog and Mixed-Signal IC Design)

Exam: [README.md](README.md). Every bold number below is recomputed by [verify_20_exam.py](../verify/verify_20_exam.py). Answers with a non-trivial route are recomputed independently, as listed here; closed-form arithmetic is re-evaluated directly:

- $g_m/I_D$ by numerically differentiating the charge-based drain current ($f_T$ is re-evaluated from its closed form);
- the op-amp's poles and zero from the roots of its exact transfer-function polynomials, and the phase margin from the exact phase at the computed unity-gain frequency;
- the bandgap from Tsividis's $V_{BE}(T)$ evaluated directly, with the flat-point gain by root finding;
- the LDO loop gain with its output capacitor's ESR, and the PLL loop gain, evaluated numerically (crossovers by root finding);
- settling, regeneration and jitter limits from their defining equations by root finding;
- SAR switching energy by explicit charge bookkeeping over all codes;
- sigma-delta noise by numerical integration of $\lvert\text{NTF}\rvert^2$, including the leaky first-order NTF whose +3 dB point checks the leakage criterion;
- the DAC INL-yield constant from the Kolmogorov series and a two-sided Monte Carlo of the Brownian bridge; harmonics from the compression law by FFT;
- the noise budget term by term, and the op-amp design by solving its pole equation;
- confidence intervals from the inverse incomplete gamma function; run counts by direct search;
- the kT/C and noise-transfer integrals by quadrature, the PLL phase maximum by numerical optimization.

---

## Solutions

### Solution 1

(a) $g_m/I_D = \dfrac{1}{nV_T}\cdot\dfrac{2}{1 + \sqrt{1 + 4IC}}$ with $nV_T$ = 33.61 mV: IC = 0.1 gives **27.26** V⁻¹, IC = 1 gives **18.39** V⁻¹, IC = 10 gives **8.04** V⁻¹.

(b) $I_{spec,\square} = 2 \times 1.3 \times 0.035\ \text{m}^2/\text{V·s} \times 8.6 \times 10^{-3}\ \text{F/m}^2 \times (0.02585)^2$ = **0.523** µA. W/L = 100 µA/(0.523 µA × 1) = **191**. $g_m$ = 18.39 × 100 µA = **1.84** mS.

(c) $A_i = (g_m/I_D)V_A'L$ = 18.39 × 8 × 0.5 = **73.6**.

(d) $q^2 + q = 1$ gives $q = (\sqrt5 - 1)/2$ = 0.618. $f_T = \dfrac{3 \times 0.035 \times 0.02585}{2\pi(0.5 \times 10^{-6})^2} \times 0.618$ = **1.07** GHz.

### Solution 2

(a) $A_0 = g_{m1}R_1g_{m6}R_2$ = 200 × 250 = **50000**, **94.0** dB. $p_1 = 1/(g_{m6}R_1R_2C_c)$ = 2 × 10⁴ rad/s, **3.18** kHz. Gain–bandwidth $g_{m1}/C_c$ = 10⁹ rad/s, **159** MHz.

(b) $p_2 = g_{m6}C_c/[C_1C_L + C_c(C_1 + C_L)] = 5 \times 10^{-15}/(2.6 \times 10^{-24})$ = 1.92 × 10⁹ rad/s, **306** MHz. $z = g_{m6}/C_c$ = 5 × 10⁹ rad/s, **796** MHz. The RHP zero adds lag like a pole: PM ≈ 90° − arctan(159/306) − arctan(159/796) = 90° − 27.5° − 11.3° = **51.2**°. This estimate is conservative: $p_2$ pulls the true unity-gain frequency down to **145** MHz, where the exact transfer function gives **54.4**°.

(c) $R_z = 1/g_{m6}$ = **200** Ω cancels the zero. The zero sits at $-1/[C_c(R_z - 1/g_{m6})]$; placing it on $p_2$ needs $R_z = 1/g_{m6} + 1/(p_2C_c)$ = 200 + 520 = **720** Ω. (The chapter's shortcut $(1 + C_L/C_c)/g_{m6}$ = 600 Ω assumes $p_2 \approx g_{m6}/C_L$; here $C_1$ is not negligible, so the full $p_2$ is more accurate. Both earn credit with the reasoning stated.)

(d) SR = $I_{SS}/C_c$ = 50 µA/1 pF = **50** V/µs. The second stage must sink the compensation current plus the load's: $I_6 \ge I_{SS}(1 + C_L/C_c)$ = **150** µA.

### Solution 3

(a) From $V_{BE}(T) = V_{g0} - (V_{g0} - V_{BE0})T/T_0 - (\eta - m)V_T\ln(T/T_0)$: $dV_{BE}/dT = -(1.2 - 0.65)/300 - 3 \times 86.17\ \mu\text{V/K}$ = **−2.092** mV/K.

(b) $\Delta V_{BE} = V_T\ln 8$ = **53.76** mV, with coefficient $(k/q)\ln 8$ = **0.1792** mV/K.

(c) $K = 2.092/0.1792$ = **11.67**. $V_{REF}$ = 0.65 + 11.67 × 0.05376 = **1.2776** V, which equals the magic voltage $V_{g0} + (\eta - 1)V_T$.

(d) At 250 K, $V_T$ = 21.54 mV and $1 - \ln(250/300)$ = 1.1823: $V_{REF}$ = **1.2764** V. At 350 K, $V_T$ = 30.16 mV and $1 - \ln(350/300)$ = 0.8459: **1.2765** V. Box TC = (1.27756 − 1.27641)/(1.2776 × 100 K) = **8.94** ppm/K.

### Solution 4

(a) $\eta = V_{out}I_L/[V_{in}(I_L + I_Q)]$ = 0.12/(1.8 × 0.10005) = **66.6**%.

(b) $R_{out}$ = 12 Ω ∥ 50 Ω = **9.68** Ω. $L_0 = A_{EA}\beta g_{mp}R_{out}$ = 50 × 0.5 × 1 × 9.68 = **242**, **47.7** dB.

(c) $\omega_c \approx A_{EA}\beta g_{mp}/C_L$ = (25 S)/(10 µF) = 2.5 × 10⁶ rad/s: **398** kHz. The ESR adds a zero at $1/(2\pi R_{ESR}C_L)$ = **1.59** MHz, only four times higher; with $Z_{out} = R_{out} \parallel (R_{ESR} + 1/sC_L)$ the crossover is **410** kHz.

(d) Small-signal estimate: $\Delta V \approx \Delta I/(\omega_cC_L) + \Delta I\,R_{ESR}$ = 0.1/25 + 0.1 × 0.01 = 4 + 1 = **5.00** mV. A step from a light load can be larger, because the loop slews (20-04).

### Solution 5

(a) Δ = 1 V/4096 = 244.1 µV, so $\Delta^2/12$ = 4.967 × 10⁻⁹ V². For one capacitor, $C = kT/(\Delta^2/12)$ = **0.834** pF. (A differential sampler would need $24kT/\Delta^2$ = **1.67** pF per side, 20-05.)

(b) $\sigma_t = 10^{-74/20}/(2\pi \times 200\ \text{MHz})$ = **159** fs.

(c) $\tau \le T_{tr}/[(N + 1)\ln 2]$ = 2 ns/(13 × 0.693) = **0.222** ns; $R_{on} \le \tau/C$ = **266** Ω.

(d) τ = C/g_m = **20** ps. $t = \tau\ln(0.5\ \text{V}/1\ \mu\text{V})$ = 20 ps × 13.12 = **262** ps. In 300 ps the gain is $e^{15}$, so the smallest input is $0.5\ \text{V}\cdot e^{-15}$ = **0.153** µV.

### Solution 6

(a) Δ = 244.1 µV. Quantization $\Delta^2/12$ = **4967** µV²; kT/C (differential) $2kT/C$ = **8284** µV²; jitter $\tfrac12A^2(2\pi f\sigma_t)^2 = 0.125 \times (2\pi \times 10^8 \times 2 \times 10^{-13})^2$ = **1974** µV²; comparator $(50\ \mu\text{V})^2$ = **2500** µV².

(b) Total 17 725 µV² against a signal of $A^2/2$ = 0.125 V²: SNR = **68.48** dB, ENOB = (68.48 − 1.76)/6.02 = **11.08**. The kT/C term dominates (alone it would allow **71.8** dB).

(c) $2kT/C = \Delta^2/12$ gives $C = 24kT/\Delta^2$ = **1.67** pF per side.

(d) Thermal noise falls to 4967 µV² and jitter to 493 µV²: SNR = **69.85** dB, ENOB = **11.31**. Quantization and thermal noise are now equal and largest, the comparator next; further gains need a lower-noise comparator and larger capacitors together, at the cost of power (the 8kT·SNR law of 20-06).

### Solution 7

(a) $2^6 - 1$ = **63** comparators; **10** comparison cycles.

(b) For the differential pair of arrays, $E = \sum_{i=1}^{8}2^{9-2i}(2^i - 1)C_uV_{REF}^2$ = **339.3** $C_uV_{REF}^2$ = **339** fJ (half of it per array).

(c) β = 1/(1 + 1 + 0.2) = **0.455**. Gain error 1/(1 + Aβ) = 1/91.9 = **1.09**%.

(d) Skew: $20\log_{10}(\pi \times 1\ \text{GHz} \times 0.5\ \text{ps})$ = **−56.1** dBc. Gain: $20\log_{10}(0.002/2)$ = **−60.0** dBc. Offset: $10\log_{10}[(1\ \text{mV})^2/(2 \times 0.25)]$ = **−57.0** dBc. The skew image dominates and will grow with input frequency.

### Solution 8

(a) The three terms: $10\log_{10}[(0.5^2/2)/(2^2/12)]$ = −4.26 dB; $-10\log_{10}(\pi^4/5)$ = −12.90 dB; $50\log_{10}64$ = 90.31 dB. SQNR = **73.2** dB.

(b) $(20L + 10)\log_{10}2$ = 50 × 0.301 = **15.1** dB.

(c) $p = (1 + 1/A)/[1 + (1 + C_s/C_i)/A]$ = 1.01/1.015 = **0.99507**; ε = **0.00493**. The leaky NTF gives $\lvert 1 - pe^{-j\omega}\rvert^2 = \varepsilon^2 + 2p(1 - \cos\omega) \approx \varepsilon^2 + p\omega^2$, so the in-band noise changes by the factor $p + 3\varepsilon^2\text{OSR}^2/\pi^2$ = 0.99507 + 0.03021 = 1.0253: a penalty of **0.11** dB. The equation sheet's approximation $\sigma_e^2[\varepsilon^2/\text{OSR} + \pi^2/(3\,\text{OSR}^3)]$, which sets $p = 1$ in the shaped term, gives **0.13** dB; both earn full credit, and either way the leak is negligible at this gain.

(d) First-order single loop (for $C_s = C_i$, ε ≈ 1/A): $A < \sqrt3\,\text{OSR}/\pi$ = **70.6** (numerically, the in-band noise doubles at A = **68.1**). MASH: $A < \sqrt5\,\text{OSR}^2/\pi^2$ = **3712** (**71.4** dB). The MASH needs fifty times more gain, because its leak lets unshaped first-stage error through.

### Solution 9

(a) Segmented: 0.5% × √(2⁷ − 1) = **0.0563** LSB. Binary: 0.5% × √4095 = **0.320** LSB, almost six times worse.

(b) At 99.73% yield the Kolmogorov constant is 1.818: $\sigma_u \le 0.5/(1.818\sqrt{1023})$ = **0.860**%.

(c) $x = R_L/r_{unit}$ = 2.5 × 10⁻⁵ and $xN_t$ = 0.02558. HD2 ≈ $xN_t/4$: **−43.9** dBc; HD3 ≈ $(xN_t)^2/16$: **−87.8** dBc; INL ≈ $xN_t^2/4$ = **6.54** LSB (first-order estimates, within 0.2 dB and 0.1 LSB of the exact compression law). For HD2 = −70 dBc, $xN_t/4 = 3.16 \times 10^{-4}$, so $r_{unit}$ = **20.2** MΩ: cascoded cells or a differential output.

(d) NRZ: $20\log_{10}[\sin(0.3\pi)/(0.3\pi)]$ = **−1.33** dB. RZ: $20\log_{10}[\tfrac12\sin(0.15\pi)/(0.15\pi)]$ = **−6.34** dB.

### Solution 10

(a) PM = arctan(8/6) = **53.1**°. $f_z = f_c/\sqrt b$ = **333** kHz; $f_p = f_c\sqrt b$ = **3.00** MHz.

(b) $K = I_{cp}K_{VCO}/(2\pi N)$ = 4000 A/(V·s). $|G(j\omega_c)| = 1$ gives $C_1 + C_2 = K\sqrt b/\omega_c^2$ = **304** pF; $C_1 = (C_1 + C_2)(b - 1)/b$ = **270** pF; $C_2$ = **33.8** pF; $R = 1/(\omega_zC_1)$ = **1.77** kΩ.

(c) −150 + 20 log₁₀ 50 = **−116.0** dBc/Hz.

(d) $\sigma_\phi = \sqrt{2 \times 10^{-11.602} \times 0.99\ \text{MHz}}$ = **2.22** mrad; $\sigma_t = \sigma_\phi/(2\pi \times 2.5\ \text{GHz})$ = **142** fs. FoM = 20 log₁₀(σ_t/1 s) + 10 log₁₀(P/1 mW) = **−247.0** dB.

### Solution 11

(a) σ(ΔV_TH) = $4/\sqrt{16}$ = **1.00** mV; $(4/0.25)^2$ = **256** µm².

(b) $\sqrt{(6 \times 0.001)^2 + 0.004^2}$ = **0.721**%.

(c) AB: 0.05 × 4 = **0.200** mV. ABBA: the linear term cancels and $2g_2p^2$ = 2 × 5 × 10⁻⁴ × 16 = **0.0160** mV remains.

(d) The multipliers are $\sqrt{199/239.96}$ = 0.911 and $\sqrt{199/161.83}$ = 1.109: σ between **1.09** and **1.33** mV. Runs: $(1 - 6.334 \times 10^{-5})^n \le 0.05$ gives n ≈ **47.3** thousand runs (≈ 3/p = 47 360; the exact count is sensitive to the last digits of p).

### Solution 12

(a) $g_{m1} = 2\pi \times 100\ \text{MHz} \times 0.5\ \text{pF}$ = **0.314** mS; at 15 V⁻¹ each input device needs 20.9 µA, a tail of **41.9** µA, and SR = $I_{SS}/C_c$ = **83.8** V/µs: short of 100.

(b) $I_{SS} \ge 100\ \text{V/µs} \times 0.5\ \text{pF}$ = **50.0** µA, 25 µA per side; keeping $g_{m1}$ = 0.314 mS needs $g_m/I_D$ = **12.6** V⁻¹ (slightly stronger inversion; or accept a higher gain–bandwidth).

(c) $p_2 = g_{m6}C_c/[C_1C_L + C_c(C_1 + C_L)]$ = 2.2 × 2π × 100 MHz gives $g_{m6}$ = **4.15** mS, which at 10 V⁻¹ needs **415** µA. Slew needs $I_6 \ge 50(1 + 2/0.5)$ = **250** µA, so the pole sets the current: total **465** µA, **418** µW from 0.9 V.

(d) $V_{DS,sat} \approx 2/10$ = **0.200** V per output device, leaving 0.9 − 0.4 = **0.500** V of swing. A telescopic first stage would stack five devices at about 2/12.6 = 0.16 V each, **0.80** V of the 0.9 V supply, leaving almost no input common-mode or output range: at this supply a simple or folded first stage feeding the swing-friendly second stage is the practical choice (20-12).

### Solution 13

(a) The resistor's noise $4kTR$ (V²/Hz) passes through $1/(1 + j2\pi fRC)$:

$$
\overline{v_n^2} = \int_0^\infty\frac{4kTR\,df}{1 + (2\pi fRC)^2} = \frac{4kTR}{2\pi RC}\int_0^\infty\frac{du}{1 + u^2} = \frac{4kTR}{2\pi RC}\cdot\frac\pi2 = \frac{kT}{C} .
$$

R cancels: more resistance means more noise density but proportionally less bandwidth. For 2 pF, $\sqrt{kT/C}$ = **45.5** µV. *Rubric (3):* integral set up (1), substitution and result (1), value (1).

(b) $\lvert\text{NTF}(e^{j\omega})\rvert^2 = \lvert 1 - e^{-j\omega}\rvert^2 = 2 - 2\cos\omega = 4\sin^2(\omega/2) \approx \omega^2$ for small ω. White error of variance $\sigma_e^2$ spreads uniformly over $(-\pi, \pi)$; the in-band power over $\lvert\omega\rvert < \omega_B = \pi/\text{OSR}$ is

$$
P_q = \frac{\sigma_e^2}{2\pi}\int_{-\omega_B}^{\omega_B}\omega^2\,d\omega = \frac{\sigma_e^2\,\omega_B^3}{3\pi} = \frac{\sigma_e^2\pi^2}{3\,\text{OSR}^3} .
$$

At OSR = 32 that is 1.00 × 10⁻⁴ $\sigma_e^2$, **−40.0** dB. *Rubric:* NTF magnitude (1), integral (1), value (1).

(c) The filter's phase lead is $\phi(\omega) = \arctan(\omega/\omega_z) - \arctan(\omega/\omega_p)$. Setting $d\phi/d\omega = 0$: $\omega_z/(\omega_z^2 + \omega^2) = \omega_p/(\omega_p^2 + \omega^2)$, so $\omega^2(\omega_p - \omega_z) = \omega_z\omega_p(\omega_p - \omega_z)$ and $\omega = \sqrt{\omega_z\omega_p}$. There $\tan A = \sqrt b$ and $\tan B = 1/\sqrt b$, so $\tan(A - B) = (\sqrt b - 1/\sqrt b)/2 = (b - 1)/(2\sqrt b)$. The type-II loop has −180° from its two integrators, so this lead is the phase margin when crossover is placed there. For b = 16: arctan(15/8) = **61.9**°. *Rubric:* derivative (1), tangent identity (1), value (1).

(d) Divide the gate into $n \propto WL$ independent patches with threshold contributions of variance $s^2$. The device threshold is their mean, with variance $s^2/n \propto 1/(WL)$; the difference of two devices doubles the variance, so $\sigma(\Delta V_{TH}) = A_{VT}/\sqrt{WL}$, and likewise for β. For a mirror at fixed $V_{GS}$, $\ln I = \ln\beta + \ln f(V_{GS} - V_{TH})$, so $dI/I = d\beta/\beta - (g_m/I_D)\,dV_{TH}$ (since $g_m/I_D = d\ln I/dV_{GS}$). With independent terms the variances add: $\sigma(\Delta I/I)^2 = (g_m/I_D)^2\sigma(\Delta V_{TH})^2 + \sigma(\Delta\beta/\beta)^2$. *Rubric:* averaging argument (1), pair doubling (1), linearization (1).

### Solution 14

(a) SNDR = 6.02 × 10.5 + 1.76 = 64.97 dB. Walden: 10 mW/(2^10.5 × 1 GS/s) = **6.91** fJ/step. Schreier: 64.97 + 10 log₁₀(500 MHz/10 mW) = **172.0** dB. Thermal limit: $8kT\cdot 10^{6.497} \times 10^9$ = **0.104** mW, so the claim is **96.1** times (**19.8** dB above) the limit: physics allows it. But the right yardstick is the speed-dependent frontier, not the 189 dB record, which belongs to a converter with a 1 kHz bandwidth. At 1 GS/s the best published Schreier figure is about 173.3 dB (a single-channel pipeline, 20-06 §7, 20-07 §9), so the claim puts an 8-way interleaved SAR, sold as IP with its reference and clock power presumably included, within about 1.3 dB of the best converter published at this speed. Verdict: extraordinary; credible only with measured silicon at Nyquist across PVT and a power breakdown. *Rubric (3):* both figures (1), thermal comparison (1), judgment on the speed-dependent frontier (1); "plausible because below 189 dB" earns no judgment point.

(b) If jitter were the only noise, $\sigma_t \le 10^{-65/20}/(2\pi \times 500\ \text{MHz})$ = **179** fs total, including the ADC's own aperture jitter. Quantization and thermal noise share the same 65 dB budget; if jitter may take half of it, $\sigma_t \le$ **127** fs. The clock must be a clean, low-jitter PLL or an external jitter cleaner; at 1 GHz this is within reach of good LC PLLs (20-10), but the IP's numbers depend on it. Ask what clock was used for the ENOB measurement and over what band its jitter was integrated. *Rubric:* value (1), clock implication (1), question (1).

(c) $\sigma_{skew} \le 10^{-70/20}/(2\pi \times 500\ \text{MHz})$ = **0.101** ps rms per channel (equivalently 0.20 ps between two channels in the two-channel formula of 20-07): far below raw layout matching, so background skew calibration is required; ask how it converges, its tracking over temperature, and the spur level before and after calibration. *Rubric:* value (1), calibration conclusion (1), question (1).

(d) Factor = 0.3 × (0.75/0.7) + 0.7 × 0.7 × (0.7/0.75)² = **0.748**: about 25% saving, not 50%. The thermal-noise-limited analog does not shrink; only the digital part benefits. Questions: what fraction of today's power is analog, reference buffer and clocking? Does the 2 nm estimate assume a lower SNR, or more calibration that lets the analog run nearer the kT/C limit? *Rubric:* factor (1), reasoning (1), questions (1).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| X20.1a | gm/ID at IC 0.1 | 27.26 | V⁻¹ |
| X20.1b | gm/ID at IC 1 | 18.39 | V⁻¹ |
| X20.1c | gm/ID at IC 10 | 8.04 | V⁻¹ |
| X20.1d | specific current per square | 0.523 | µA |
| X20.1e | W/L | 191 | — |
| X20.1f | gm | 1.84 | mS |
| X20.1g | intrinsic gain | 73.6 | — |
| X20.1h | f_T | 1.07 | GHz |
| X20.2a | DC gain | 50000 | — |
| X20.2b | DC gain | 94.0 | dB |
| X20.2c | dominant pole | 3.18 | kHz |
| X20.2d | gain–bandwidth | 159 | MHz |
| X20.2e | non-dominant pole | 306 | MHz |
| X20.2f | RHP zero | 796 | MHz |
| X20.2g | phase margin | 51.2 | ° |
| X20.2h | Rz to cancel the zero | 200 | Ω |
| X20.2i | Rz to cancel p2 | 720 | Ω |
| X20.2j | slew rate | 50 | V/µs |
| X20.2k | minimum I6 | 150 | µA |
| X20.2l | exact unity-gain frequency | 145 | MHz |
| X20.2m | exact phase margin | 54.4 | ° |
| X20.3a | dVBE/dT | −2.092 | mV/K |
| X20.3b | ΔVBE | 53.76 | mV |
| X20.3c | ΔVBE coefficient | 0.1792 | mV/K |
| X20.3d | gain K | 11.67 | — |
| X20.3e | VREF at 300 K | 1.2776 | V |
| X20.3f | VREF at 250 K | 1.2764 | V |
| X20.3g | VREF at 350 K | 1.2765 | V |
| X20.3h | box TC | 8.94 | ppm/K |
| X20.4a | efficiency | 66.6 | % |
| X20.4b | output resistance | 9.68 | Ω |
| X20.4c | loop gain | 242 | — |
| X20.4d | loop gain | 47.7 | dB |
| X20.4e | crossover | 398 | kHz |
| X20.4f | droop | 5.00 | mV |
| X20.4g | ESR zero | 1.59 | MHz |
| X20.4h | crossover with ESR | 410 | kHz |
| X20.5a | sampling capacitance | 0.834 | pF |
| X20.5b | jitter | 159 | fs |
| X20.5c | time constant | 0.222 | ns |
| X20.5d | switch resistance | 266 | Ω |
| X20.5e | latch time constant | 20 | ps |
| X20.5f | resolve time | 262 | ps |
| X20.5g | smallest input | 0.153 | µV |
| X20.5h | differential capacitance per side | 1.67 | pF |
| X20.6a | quantization noise | 4967 | µV² |
| X20.6b | kT/C noise | 8284 | µV² |
| X20.6c | jitter noise | 1974 | µV² |
| X20.6d | comparator noise | 2500 | µV² |
| X20.6e | SNR | 68.48 | dB |
| X20.6f | ENOB | 11.08 | bits |
| X20.6g | SNR from kT/C alone | 71.8 | dB |
| X20.6h | capacitance per side | 1.67 | pF |
| X20.6i | new SNR | 69.85 | dB |
| X20.6j | new ENOB | 11.31 | bits |
| X20.7a | flash comparators | 63 | — |
| X20.7b | SAR cycles | 10 | — |
| X20.7c | energy coefficient | 339.3 | CuVREF² |
| X20.7d | energy | 339 | fJ |
| X20.7e | β | 0.455 | — |
| X20.7f | gain error | 1.09 | % |
| X20.7g | skew image | −56.1 | dBc |
| X20.7h | gain image | −60.0 | dBc |
| X20.7i | offset spur | −57.0 | dBc |
| X20.8a | SQNR | 73.2 | dB |
| X20.8b | improvement | 15.1 | dB |
| X20.8c | integrator pole | 0.99507 | — |
| X20.8d | leak | 0.00493 | — |
| X20.8e | noise penalty, exact | 0.11 | dB |
| X20.8i | noise penalty, chapter approximation | 0.13 | dB |
| X20.8f | single-loop gain bound | 70.6 | — |
| X20.8g | MASH gain bound | 3712 | — |
| X20.8h | MASH gain bound | 71.4 | dB |
| X20.8j | gain where noise doubles | 68.1 | — |
| X20.9a | σ(DNL) segmented | 0.0563 | LSB |
| X20.9b | σ(DNL) binary | 0.320 | LSB |
| X20.9c | unit σ for yield | 0.860 | % |
| X20.9d | HD2 | −43.9 | dBc |
| X20.9e | HD3 | −87.8 | dBc |
| X20.9f | INL | 6.54 | LSB |
| X20.9g | unit resistance for −70 dBc | 20.2 | MΩ |
| X20.9h | NRZ at 0.3 fs | −1.33 | dB |
| X20.9i | RZ at 0.3 fs | −6.34 | dB |
| X20.10a | phase margin | 53.1 | ° |
| X20.10b | zero frequency | 333 | kHz |
| X20.10c | pole frequency | 3.00 | MHz |
| X20.10d | C1 + C2 | 304 | pF |
| X20.10e | C1 | 270 | pF |
| X20.10f | C2 | 33.8 | pF |
| X20.10g | R | 1.77 | kΩ |
| X20.10h | output in-band noise | −116.0 | dBc/Hz |
| X20.10i | rms phase | 2.22 | mrad |
| X20.10j | rms jitter | 142 | fs |
| X20.10k | jitter-power FoM | −247.0 | dB |
| X20.11a | σ(ΔV_TH) | 1.00 | mV |
| X20.11b | area for 0.25 mV | 256 | µm² |
| X20.11c | mirror mismatch | 0.721 | % |
| X20.11d | AB offset | 0.200 | mV |
| X20.11e | ABBA residual | 0.0160 | mV |
| X20.11f | σ low | 1.09 | mV |
| X20.11g | σ high | 1.33 | mV |
| X20.11h | failure-free runs | 47.3 | thousand |
| X20.12a | gm1 | 0.314 | mS |
| X20.12b | tail current | 41.9 | µA |
| X20.12c | slew rate | 83.8 | V/µs |
| X20.12d | tail for slew | 50.0 | µA |
| X20.12e | gm/ID of the pair | 12.6 | V⁻¹ |
| X20.12f | gm6 | 4.15 | mS |
| X20.12g | I6 for the pole | 415 | µA |
| X20.12h | I6 for slew | 250 | µA |
| X20.12i | total current | 465 | µA |
| X20.12j | power | 418 | µW |
| X20.12k | VDS,sat | 0.200 | V |
| X20.12l | output swing | 0.500 | V |
| X20.12m | telescopic headroom | 0.80 | V |
| X20.13a | kT/C noise on 2 pF | 45.5 | µV |
| X20.13b | first-order noise at OSR 32 | −40.0 | dB |
| X20.13c | phase margin, b = 16 | 61.9 | ° |
| X20.14a | Walden FoM | 6.91 | fJ/step |
| X20.14b | Schreier FoM | 172.0 | dB |
| X20.14c | thermal-limit power | 0.104 | mW |
| X20.14d | ratio to the limit | 96.1 | — |
| X20.14h | ratio to the limit | 19.8 | dB |
| X20.14e | jitter budget | 179 | fs |
| X20.14i | half-budget jitter | 127 | fs |
| X20.14f | per-channel skew | 0.101 | ps |
| X20.14g | power factor | 0.748 | — |
