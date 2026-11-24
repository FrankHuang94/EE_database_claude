# Course 20 · Final Exam (Analog and Mixed-Signal IC Design)

**Time limit:** 240 minutes.
**Allowed:** a scientific calculator and the [Course 20 equation sheet](../../../reference/equation-sheets/20-analog-and-mixed-signal-ic-design.md) printed without its chapter links. No notes, no Python and no simulator.

**Instructions.**

- Answer all 14 questions and show every step.
- Question 1 [A] is worth 8 points (2 per part), each [B] 8 (2 per part), and Questions 13 and 14 [C] 12 each (3 per part): 120 points in total. 84 or more (70%) is a strong pass.
- Give numerical answers to 3–4 significant figures, with units.
- Question 12 is a short design; Question 13 asks for derivations, and in it results quoted from the equation sheet earn no credit unless derived; Question 14 is a diligence question, partly graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These follow the chapters.

- T = 300 K, so $kT$ = 4.142 × 10⁻²¹ J and $V_T = kT/q$ = 25.85 mV; $k/q$ = 86.17 µV/K.
- $g_m/I_D$ is in V⁻¹; the slope factor is $n$ = 1.3 unless given. In Question 1, $q$ is the normalized inversion charge, not the electron charge.
- Thresholds are $V_{TH}$; a pair's threshold mismatch is $\Delta V_{TH}$, with Pelgrom coefficient $A_{VT}$.
- A sine of peak amplitude $A$ has power $A^2/2$; phase noise $\mathcal L(f)$ is single-sideband, so $\sigma_\phi^2 = 2\int\mathcal L\,df$.
- Mismatch coefficients $A_{VT}$ and $A_\beta$ refer to the difference of a pair.
- Spurs and images are quoted in dBc, relative to the signal.
- In Question 8, a 1-bit quantizer has levels ±1 (Δ = 2).

---

**1 [A] · The transistor in all regions.** (20-01)
A process has μ = 350 cm²/V·s, $C_{ox}$ = 8.6 fF/µm², $n$ = 1.3 and $V_A'$ = 8 V/µm. Neglect velocity saturation.
(a) Find $g_m/I_D$ at IC = 0.1, 1 and 10.
(b) Find the specific current per square $I_{spec,\square} = 2n\mu C_{ox}V_T^2$, the W/L that carries 100 µA at IC = 1, and the resulting $g_m$.
(c) Find the intrinsic gain at IC = 1 and L = 0.5 µm.
(d) Find $f_T = (3\mu V_T/2\pi L^2)\,q$ at IC = 1 and L = 0.5 µm, where $q^2 + q = IC$.

**2 [B] · A two-stage op-amp.** (20-02)
A Miller-compensated two-stage op-amp has $g_{m1}$ = 1 mS, $g_{m6}$ = 5 mS, $R_1$ = 200 kΩ, $R_2$ = 50 kΩ, $C_1$ = 0.2 pF, $C_L$ = 2 pF and $C_c$ = 1 pF.
(a) Find the DC gain (ratio and dB), the dominant pole frequency and the gain–bandwidth product $g_{m1}/(2\pi C_c)$ (both in Hz).
(b) Find the non-dominant pole and the right-half-plane zero (in Hz), and estimate the phase margin from them.
(c) What nulling resistor cancels the zero, and what value moves it onto the non-dominant pole?
(d) With a 50 µA tail current, find the slew rate and the minimum second-stage current that does not limit it.

**3 [B] · A bandgap reference.** (20-03)
A PNP has $V_{BE}$ = 0.65 V at 300 K under a PTAT bias ($m$ = 1); $V_{g0}$ = 1.2 V and η = 4. The PTAT term uses an area ratio N = 8.
(a) Find $dV_{BE}/dT$ at 300 K.
(b) Find $\Delta V_{BE}$ at 300 K and its temperature coefficient.
(c) Find the gain $K$ that makes $V_{REF} = V_{BE} + K\Delta V_{BE}$ flat at 300 K, and $V_{REF}$ there.
(d) Using $V_{REF}(T) = V_{g0} + (\eta - 1)V_T(T)\,[1 - \ln(T/300\text{ K})]$, find $V_{REF}$ at 250 K and 350 K and the box temperature coefficient over 250–350 K.

**4 [B] · An LDO.** (20-04)
An LDO delivers 1.2 V at 100 mA from 1.8 V with 50 µA of quiescent current. Its error amplifier has gain 50, the feedback divider β = 0.5, the pass device $g_{mp}$ = 1 S and $r_{ds}$ = 50 Ω, and the output capacitor is 10 µF with 10 mΩ ESR.
(a) Find the efficiency.
(b) Find the output resistance at full load and the DC loop gain (ratio and dB).
(c) Find the crossover frequency, first ignoring the ESR and then including it.
(d) Estimate the small-signal output droop for a 100 mA load step from a light load.

**5 [B] · Sampling and comparing.** (20-05)
A 12-bit converter with a single-ended sampler (one capacitor) has a 1 V peak-to-peak full scale.
(a) What sampling capacitance makes kT/C noise equal to the quantization noise?
(b) What rms clock jitter limits the SNR of a full-scale 200 MHz input to 74 dB?
(c) The track phase lasts 2 ns. What time constant settles to ½ LSB at 12 bits, and what switch on-resistance does that allow with the capacitor of (a)?
(d) A latch has $C$ = 20 fF and $g_m$ = 1 mS. How long does it take to grow 1 µV to 0.5 V, and what is the smallest input it resolves to 0.5 V in 300 ps?

**6 [B] · A noise budget.** (20-05, 20-06)
A 12-bit converter digitizes a full-scale sine of 0.5 V amplitude (1 V peak-to-peak) at 100 MHz. Its differential sampler has 1 pF per side (noise $2kT/C$), its clock has 200 fs rms jitter, and its comparator adds 50 µV rms of input-referred noise.
(a) Find each noise power (in µV²): quantization, kT/C, jitter and comparator.
(b) Find the total SNR and the ENOB. Which term dominates?
(c) What capacitance per side would make the kT/C noise equal to the quantization noise?
(d) With that capacitance and the jitter halved to 100 fs, find the new SNR and ENOB. What now limits the converter?

**7 [B] · Nyquist ADCs.** (20-07)
(a) How many comparators does a 6-bit flash ADC need, and how many comparison cycles does a 10-bit SAR take?
(b) Find the average conventional switching energy of an 8-bit differential SAR (two arrays) with $C_u$ = 1 fF and $V_{REF}$ = 1 V.
(c) A flip-around 1.5-bit MDAC has $C_s = C_f$ = 1 pF, $C_p$ = 0.2 pF and an op-amp gain of 200. Find β and the gain error.
(d) A two-channel interleaved ADC digitizes a 1 GHz sine of 0.5 V amplitude. Find the image from 0.5 ps of skew, the image from 0.2% gain mismatch, and the spur from 1 mV of offset mismatch, all in dBc.

**8 [B] · Sigma-delta.** (20-08)
(a) A second-order 1-bit modulator at OSR = 64 has an input of 0.5 amplitude (−6 dBFS). Find its SQNR.
(b) How much does the SQNR improve if OSR doubles to 128?
(c) A first-order switched-capacitor modulator has $C_s/C_i$ = 0.5 and op-amp gain 100. Using $p = (1 + 1/A)/[1 + (1 + C_s/C_i)/A]$, find the integrator pole $p$, the leak ε = 1 − p, and the in-band noise penalty at OSR = 64.
(d) At OSR = 128 with $C_s = C_i$, below what op-amp gain does leakage matter in a first-order single-loop modulator, and in a MASH 1-1?

**9 [B] · DACs.** (20-09)
(a) A 12-bit current-steering DAC is segmented into 6 unary MSBs and 6 binary LSBs, with unit-current σ = 0.5%. Find σ of the DNL at its worst transition, and compare a fully binary design.
(b) What unit-current σ gives 99.73% (3σ) yield of |INL| ≤ ½ LSB in a 10-bit fully unary DAC?
(c) A 10-bit single-ended DAC drives 25 Ω, and each unit cell has 1 MΩ output resistance. Estimate HD2, HD3 and the peak INL from the first-order formulas; then the unit resistance that makes HD2 = −70 dBc.
(d) Find the NRZ and RZ amplitude responses at $0.3f_s$, in dB.

**10 [B] · A PLL.** (20-10)
A charge-pump PLL has $I_{cp}$ = 200 µA, $K_{VCO}$ = 2π × 1 GHz/V and N = 50 (50 MHz reference, 2.5 GHz output). Its third-order loop filter is designed for a 1 MHz crossover with spread b = 9.
(a) Find the phase margin and the zero and pole frequencies.
(b) Find $C_1 + C_2$, $C_1$, $C_2$ and $R$.
(c) The reference path contributes −150 dBc/Hz (referred to the input) in band. What is it at the output?
(d) If the output noise were that in-band level from 10 kHz to 1 MHz and negligible elsewhere, find the rms phase and jitter, and the jitter-power FoM at 10 mW.

**11 [B] · Matching.** (20-11)
A process has $A_{VT}$ = 4 mV·µm.
(a) Find σ(ΔV_TH) for an 8 µm × 2 µm pair, and the area that brings it to 0.25 mV.
(b) Find a mirror's σ(ΔI/I) at $g_m/I_D$ = 6 V⁻¹ with σ(ΔV_TH) = 1 mV and σ(Δβ/β) = 0.4%.
(c) A threshold gradient of 0.05 mV/µm and a quadratic term of 5 × 10⁻⁴ mV/µm² act on unit cells 4 µm apart. Find the AB offset (linear only) and the ABBA residual.
(d) A 200-run Monte Carlo estimates σ = 1.2 mV. Give the 95% interval for σ, using $\chi^2_{0.025,199}$ = 161.83 and $\chi^2_{0.975,199}$ = 239.96. How many failure-free runs would demonstrate a two-sided 4σ failure rate, $2Q(4) = 6.334 \times 10^{-5}$?

**12 [B] · Design an op-amp for a low supply.** (20-01, 20-02, 20-12)
Design a Miller two-stage op-amp on a 0.9 V supply for a 100 MHz gain–bandwidth product, a 2 pF load and at least 100 V/µs slew rate. Use $C_c$ = 0.5 pF, a first-stage parasitic $C_1$ = 0.2 pF and a nulling resistor that removes the zero. The input pair runs at $g_m/I_D$ = 15 V⁻¹ and the second stage at 10 V⁻¹.
(a) Find $g_{m1}$, the tail current and the slew rate this gives. Does it meet the slew specification?
(b) Raise the tail current to meet slew. What tail current is needed, and what $g_m/I_D$ keeps the gain–bandwidth at 100 MHz?
(c) Size the second stage so that $p_2 = 2.2\,\omega_u$ (about 65° of phase margin). Find $g_{m6}$, the current it needs, the current the slew condition $I_6 \ge I_{SS}(1 + C_L/C_c)$ needs, and the total power.
(d) With $V_{DS,sat} \approx 2/(g_m/I_D)$ for the output devices, what output swing remains? Why would a telescopic first stage be a poor choice on this supply?

**13 [C] · Derivations.** (20-05, 20-08, 20-10, 20-11)
(a) Derive the kT/C result from the noise spectrum of a resistor R charging a capacitor C, and evaluate it for 2 pF.
(b) Starting from NTF $= 1 - z^{-1}$, derive the in-band quantization noise of a first-order modulator for large OSR, and evaluate it relative to $\sigma_e^2$ at OSR = 32.
(c) A loop filter has a zero at $\omega_z$ and a pole at $\omega_p = b\,\omega_z$ in a type-II loop. Show that the phase lead peaks at $\sqrt{\omega_z\omega_p}$ and derive $\text{PM}_{max} = \arctan[(b - 1)/(2\sqrt b)]$. Evaluate it for b = 16.
(d) Derive Pelgrom's area law from independent patches, and from it the mirror mismatch formula $\sigma(\Delta I/I)^2 = (g_m/I_D)^2\sigma(\Delta V_{TH})^2 + \sigma(\Delta\beta/\beta)^2$.

**14 [C] · Diligence: an ADC IP claim.** (20-06, 20-07, 20-10, 20-12)
A start-up offers a "12-bit, 1 GS/s ADC IP at 10 mW in 3 nm, ENOB 10.5 at Nyquist", and says it "will halve its power at 2 nm".
(a) Find the Walden and Schreier figures for the claim, and compare its power with the thermal limit $P = 8kT\cdot\text{SNR}\cdot f_s$. Is the claim plausible?
(b) What total rms jitter would a 65 dB SNR at a 500 MHz input allow if jitter were the only noise, and what if it may take half the noise budget? What does that imply for the clock source?
(c) The design is an 8-way interleaved SAR. What rms per-channel timing skew keeps the total skew-spur power below −70 dBc for a near-Nyquist (500 MHz) input, using total skew-spur power ≈ $(2\pi f_{in}\sigma_{skew})^2$? What does that imply?
(d) Suppose 30% of the power is thermal-noise-limited analog (power ∝ $1/V_{DD}$ at fixed SNR) and 70% digital ($CV_{DD}^2f$, with $C$ falling to 0.7×), with $V_{DD}$ moving from 0.75 V to 0.7 V. Find the power factor. Is "half the power" credible? List two questions you would ask.
