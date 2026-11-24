# Solutions 21-06 · Oscillators and VCOs

Problems: [21-06 problem set](../problems/21-06-problems.md) · Chapter: [21-06](../chapters/21-06-oscillators-and-vcos.md). Every number below is recomputed by [verify_21_06.py](../verify/verify_21_06.py).

---

## Solutions

### Solution 21-06.1

(a) $\omega_0 = 2\pi \times 6$ GHz = 3.770 × 10¹⁰ rad/s, so $C = 1/(\omega_0^2L) = 1/[(3.770 \times 10^{10})^2 \times 0.8\text{ nH}]$ = **0.8795** pF.

(b) $1/Q = 1/12 + 1/40 = 0.1083$, so $Q$ = **9.231**.

(c) $\omega_0L$ = 30.16 Ω, so $R_p = Q\omega_0L$ = **278.4** Ω.

(d) Start-up needs $g_mR_p/2 > 1$: $g_m > 2/R_p$ = **7.184** mS.

(e) A loop gain of 3 needs $g_m = 6/R_p$ = 21.55 mS per device, so $I_C = g_mV_T$ = 21.55 mS × 25.85 mV = **0.5572** mA and $I_{tail} = 2I_C$ = **1.114** mA.

**Check.** Units: (A/V)(V) = A. A loop gain of 3 at only 1.1 mA shows how cheap start-up is; the tail current is set by the swing and phase noise, not by start-up.

### Solution 21-06.2

(a) Hard switching: $V = (2/\pi)I_{tail}R_p = (2/\pi)(3\text{ mA})(278.4\ \Omega)$ = **0.5317** V.

(b) The two outputs move in antiphase, each by half the differential amplitude: **0.2658** V.

(c) Inverting (a): $I_{tail} = \pi V/(2R_p) = \pi \times 0.8/(2 \times 278.4)$ = **4.514** mA.

(d) $\eta = V/(\pi V_{DD}) = 0.8/\pi$ = **25.5** %.

(e) $P_s = V^2/(2R_p) = 0.64/556.8$ = **1.149** mW. Check: $P_s/(I_{tail}V_{DD})$ = 1.149/4.514 = 25.5%, the same efficiency by the direct route.

Beyond 4.5 mA the amplitude would stop growing, and extra current would add device noise without adding signal: the boundary is the efficient design point.

### Solution 21-06.3

(a) Each device carries 1 mA: $g_m = I_C/V_T$ = 38.68 mS, and the loop gain $g_mR_p/2$ = **5.38**.

(b) $I_0 = I_{tail}/2$ = 1 mA: $V_{hard} = (4/\pi)I_0R_p$ = **0.3545** V.

(c) $V_0 = 2V_T$ = 51.70 mV, so $V_0/V_{hard}$ = 0.1458 and the correction is $(\pi^2/24)(0.1458)^2$ = 0.00874: $V \approx 0.3545 \times (1 - 0.00874)$ = **0.3514** V.

(d) Solving $G(V) = 1/R_p$ numerically for $g = I_0\tanh(v/V_0)$ (`vco.amplitude_df`) gives **0.3512** V. The closed form is within 0.05%.

(e) $\sigma = (g_m/2 - 1/R_p)/(2C) = (19.34 - 3.592)\text{ mS}/(2 \times 0.8795\text{ pF})$ = 8.95 × 10⁹ s⁻¹, so $1/\sigma$ = **0.1117** ns.

(f) $2R_pC = 2 \times 278.4 \times 0.8795$ pF = **0.4897** ns, about three cycles at 6 GHz.

**Check.** Growth is fast (0.11 ns per e-fold) because the loop gain is large; recovery near steady state is slower, set by the tank alone.

### Solution 21-06.4

(a) At a zero crossing $\lvert\Gamma\rvert$ = 1, so $\lvert\Delta\phi\rvert = \Delta q/q_{max}$ = 1 fC/0.4652 pC = **2.150** mrad (a delay, since a positive kick on a falling crossing makes it late).

(b) **0.1232**°.

(c) $\Delta t = \Delta\phi/\omega_0 = 2.150 \times 10^{-3}/(3.1416 \times 10^{10})$ = **68.43** fs.

(d) At a peak, $\Gamma$ = 0: no phase change. The amplitude changes by $\Delta V/V = \Delta q/q_{max}$ = **0.215** %, and the saturating devices remove it with time constant $2R_pC$ = **0.7346** ns.

(e) $\lvert\Gamma(45°)\rvert = \sin 45°$, so $\lvert\Delta\phi\rvert$ = 0.7071 × 2.150 = **1.520** mrad; the rest of the kick goes into amplitude.

### Solution 21-06.5

(a) $P_s = V^2/(2R_p) = 0.3512^2/(2 \times 278.4)$ = **0.2216** mW.

(b) $P_{DC}$ = 2 mA × 1.0 V = 2 mW, so η = **11.08** %.

(c) Leeson: $\mathcal{L} = (2FkT/P_s) \times \left[1 + (f_0/2Q\Delta f)^2\right]$. $2FkT/P_s = 2 \times 2.5 \times 4.142 \times 10^{-21}/2.216 \times 10^{-4}$ = 9.35 × 10⁻¹⁷, and $f_0/(2Q\Delta f)$ = 6 GHz/(18.46 × 1 MHz) = 325.0, so $\mathcal{L}$ = 9.35 × 10⁻¹⁷ × (1 + 1.056 × 10⁵) = 9.87 × 10⁻¹²: **−110.06** dBc/Hz.

(d) At 10 MHz the ratio is 32.50: $\mathcal{L}$ = 9.35 × 10⁻¹⁷ × 1057 = 9.88 × 10⁻¹⁴, **−130.05** dBc/Hz: 20 dB per decade, as expected (the "1 +" floor term adds 0.004 dB).

(e) FoM = 110.06 + 20 log(6000) − 10 log 2 = 110.06 + 75.56 − 3.01 = **182.6** dB.

(f) $10\log_{10}[2Q^2(1\text{ mW})/(FkT)]$ with $Q$ = 9.231, $F$ = 2.5: **192.2** dB. The gap, 9.6 dB, is exactly $-10\log_{10}\eta$.

### Solution 21-06.6

(a) $\Delta f_{1/f^3} = f_{1/f}(\Gamma_{dc}/\Gamma_{rms})^2$ = 2 MHz × (0.02/0.6)² = **2.222** kHz.

(b) 2 MHz × (0.1/0.6)² = **55.56** kHz.

(c) Flicker multiplies the white-noise phase noise by $1 + \Delta f_{1/f^3}/\Delta f$: 1.222, or **0.872** dB.

(d) 6.556, or **8.17** dB.

(e) **7.29** dB. A fivefold rise in $\Gamma_{dc}$ moves the corner 25-fold; close-in phase noise, which dominates integrated jitter in narrow-loop PLLs, is very sensitive to symmetry.

### Solution 21-06.7

(a) $f \propto C^{-1/2}$, so $C_{max}/C_{min} = (5.5/4.5)^2$ = **1.494**.

(b) $C = 1/(\omega^2L)$ at 5.5 GHz: **0.8374** pF.

(c) At 4.5 GHz: **1.251** pF.

(d) Subtracting the fixed 0.6 pF: **0.2374** pF and (e) **0.6509** pF.

(f) **2.742**: the variable part must swing almost 2.7:1 to give a 1.49:1 total ratio. This is why the fixed capacitance (devices, wiring, buffers) is the tuning range's main enemy.

### Solution 21-06.8

(a) At code 0 every cell is off: 15 × 20 fF = **0.300** pF.

(b) At code 15 every cell is on: 15 × 80 fF = **1.200** pF.

(c, d) Code 0: $C_{tot}$ = 0.5 + 0.3 + (0.10 to 0.20) = 0.90 to 1.00 pF, so $f = 1/(2\pi\sqrt{1.2\text{ nH} \times C})$ = **4.594** to **4.843** GHz.

(e, f) Code 15: 1.80 to 1.90 pF: **3.333** to **3.424** GHz.

(g) 3.333 to 4.843 GHz: $(4.843 - 3.333)/4.088$ = **36.9** %. Each LSB step is 60 fF (80 − 20) and each band spans the varactor's 0.10 pF, so neighbouring bands overlap by 40 fF.

(h) With no off-capacitance the code-0 minimum would be 0.6 pF, giving **5.931** GHz. The switches' parasitics cost over a gigahertz at the top of the range: a bank's useful figure is its on/off capacitance ratio (here 4), traded against switch resistance, which lowers Q.

### Solution 21-06.9

(a) $\sqrt{4kTR} = \sqrt{4 \times 4.142 \times 10^{-21} \times 2000}$ = **5.756** nV/√Hz.

(b) $\mathcal{L} = K^2S_v/(2\Delta f^2) \le 10^{-13}$ gives $K \le \sqrt{2 \times 10^{12} \times 10^{-13}/3.314 \times 10^{-17}}$ = **77.7** MHz/V.

(c) $\beta = KV_m/f_m$ = 7.769 × 10⁷ × 5 × 10⁻⁵/10⁷ = 3.88 × 10⁻⁴, and each sideband is $20\log_{10}(\beta/2)$ = **−74.23** dBc.

**Check.** A 78 MHz/V VCO needs a capacitor bank to cover any useful range; the noise requirement, not the range, sets $K_{VCO}$.

### Solution 21-06.10

(a) Multiplication by 3 raises phase noise by $20\log_{10}3$ = 9.54 dB: **−118.46** dBc/Hz.

(b) Division by 8 lowers it by 18.06 dB: **−146.06** dBc/Hz.

(c) **−166.06** dBc/Hz.

(d) Independent noise powers add: $10\log_{10}(10^{-16.606} + 10^{-15.5})$ = **−154.67** dBc/Hz. Far from the carrier the divider, not the VCO, sets the output.

### Solution 21-06.11

(a) $\phi_{rms} = \sqrt{\pi\mathcal{L}_0f_c} = \sqrt{\pi \times 10^{-9.5} \times 5 \times 10^5}$ = **22.29** mrad.

(b) **1.277**°.

(c) EVM ≈ $\phi_{rms}$ = **2.229** %.

(d) Error powers add, so the share is $(2.229/3.5)^2$ = **40.5** % of the 256-QAM budget, and (e) $(2.229/2.5)^2$ = **79.5** % of the 1024-QAM budget, leaving little for the PA, the DAC and the channel.

(f) $\mathcal{L}_0 = \text{EVM}^2/(\pi f_c) = 10^{-4}/(\pi \times 5 \times 10^5)$ = 6.37 × 10⁻¹¹: **−101.96** dBc/Hz, about 7 dB better.

### Solution 21-06.12

(a) With ε = 0, IRR = $\cot^2(\theta/2) \ge 10^4$, so $\tan(\theta/2) \le 0.01$ and θ ≤ **1.146**°.

(b) θ = $(D - \tfrac12) \times 180°$, so $\lvert D - \tfrac12\rvert \le 1.146/180$ = **0.637** %: the clock's duty cycle must sit between 49.36% and 50.64%.

(c) Solving the exact formula of 21-05 for 40 dB with ε = 0.01 gives θ ≤ **0.994**° (the small-error form, $\theta = \sqrt{4 \times 10^{-4} - 10^{-4}}$ rad, gives **0.992**°).

(d) **0.552** %. Gain and phase errors share one budget: a 1% gain error takes a quarter of it.

### Solution 21-06.13

Let $x_I = \omega R_IC$ = 1.01 and $x_Q = \omega R_QC$ = 1.00. Then $V_I = 1/(1 + jx_I)$ and $V_Q = jx_Q/(1 + jx_Q)$, so

$$
\frac{V_Q}{V_I} = \frac{jx_Q(1 + jx_I)}{1 + jx_Q} .
$$

(a) Its phase is $90° + \arctan x_I - \arctan x_Q$ = 90° + 45.285° − 45° = **90.285**°.

(b) The phase error is **0.285**°.

(c) Its magnitude is $x_Q\sqrt{1 + x_I^2}/\sqrt{1 + x_Q^2} = \sqrt{2.0201/2}$ = 1.00501: a gain error of **0.501** %.

(d) The exact formula with ε = 0.00501 and θ = 0.285° gives **49.05** dB.

(e) $4/(\varepsilon^2 + \theta^2) = 4/(2.51 \times 10^{-5} + 2.48 \times 10^{-5})$: **49.04** dB.

**Check.** A 1% resistor mismatch splits roughly equally into gain and phase error; at the design frequency the network still gives almost 50 dB, but the frequency error of Example 21-06.6 usually dominates.

### Solution 21-06.14

(a) For large detuning the pull is $f_L^2/(2\Delta f) \le 10$ kHz, so $f_L \le \sqrt{2 \times 20\text{ MHz} \times 10\text{ kHz}}$ = **632.5** kHz.

(b) The lock range is $(f_0/2Q)(I_{inj}/I_{osc})$ with $f_0/2Q$ = 250 MHz: $I_{inj}/I_{osc} \le$ **2.530 × 10⁻³**.

(c) $20\log_{10}$ of that ratio: **−51.94** dB.

(d) Exactly, $\Delta f - \sqrt{\Delta f^2 - f_L^2}$ = **10.00** kHz: the approximation is excellent here.

(e) The PA's 5 GHz output is then 5 GHz from the 10 GHz VCO, thousands of times its lock range (about 4,000×), far outside the narrowband model's range, so it cannot pull it. The PA's second harmonic does land at 10 GHz, though; it is weaker, but frequency plans that avoid every harmonic coincidence (for example a VCO at 4/3 of the carrier) exist for that reason.

### Solution 21-06.15

(a) FoM = 120 + 20 log(10⁴) − 10 log 10 = 120 + 80 − 10 = **190.0** dB.

(b) Four coupled cores average independent noise: −120 − 10 log 4 = **−126.02** dBc/Hz.

(c) At 40 mW: 126.02 + 80 − 16.02 = **190.0** dB. Coupling cores does not change the FoM.

(d) $10\log_{10}N \ge 5$ dB: $N \ge 10^{0.5}$ = **3.162**.

(e) **4** cores (40 mW).

(f) The bound rises 20 dB per decade of Q, so doubling Q adds $20\log_{10}2$ = **6.02** dB: FoM 196.0 dB, the same phase noise as four cores at a quarter of the power. Q is the strongest lever, but the hardest to buy.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 21-06.1a | tank capacitance | 0.8795 | pF |
| 21-06.1b | tank Q | 9.231 | |
| 21-06.1c | R_p | 278.4 | Ω |
| 21-06.1d | minimum gm | 7.184 | mS |
| 21-06.1e | collector current for loop gain 3 | 0.5572 | mA |
| 21-06.1f | tail current for loop gain 3 | 1.114 | mA |
| 21-06.2a | differential amplitude | 0.5317 | V |
| 21-06.2b | single-ended swing | 0.2658 | V |
| 21-06.2c | tail current at the voltage limit | 4.514 | mA |
| 21-06.2d | efficiency at the limit | 25.5 | % |
| 21-06.2e | tank signal power at the limit | 1.149 | mW |
| 21-06.3a | loop gain | 5.38 | |
| 21-06.3b | hard-limit amplitude | 0.3545 | V |
| 21-06.3c | soft-switching closed form | 0.3514 | V |
| 21-06.3d | describing-function amplitude | 0.3512 | V |
| 21-06.3e | start-up e-folding time | 0.1117 | ns |
| 21-06.3f | amplitude-recovery time constant | 0.4897 | ns |
| 21-06.4a | phase shift at a zero crossing | 2.150 | mrad |
| 21-06.4b | phase shift at a zero crossing | 0.1232 | deg |
| 21-06.4c | timing shift | 68.43 | fs |
| 21-06.4d | amplitude change at a peak | 0.215 | % |
| 21-06.4e | amplitude-recovery time constant | 0.7346 | ns |
| 21-06.4f | phase shift at 45° | 1.520 | mrad |
| 21-06.5a | tank signal power | 0.2216 | mW |
| 21-06.5b | efficiency | 11.08 | % |
| 21-06.5c | phase noise at 1 MHz | −110.06 | dBc/Hz |
| 21-06.5d | phase noise at 10 MHz | −130.05 | dBc/Hz |
| 21-06.5e | FoM | 182.6 | dB |
| 21-06.5f | FoM bound | 192.2 | dB |
| 21-06.6a | 1/f³ corner, design A | 2.222 | kHz |
| 21-06.6b | 1/f³ corner, design B | 55.56 | kHz |
| 21-06.6c | flicker penalty at 10 kHz, A | 0.872 | dB |
| 21-06.6d | flicker penalty at 10 kHz, B | 8.17 | dB |
| 21-06.6e | difference | 7.29 | dB |
| 21-06.7a | total capacitance ratio | 1.494 | |
| 21-06.7b | capacitance at 5.5 GHz | 0.8374 | pF |
| 21-06.7c | capacitance at 4.5 GHz | 1.251 | pF |
| 21-06.7d | variable part, minimum | 0.2374 | pF |
| 21-06.7e | variable part, maximum | 0.6509 | pF |
| 21-06.7f | variable-part ratio | 2.742 | |
| 21-06.8a | bank at code 0 | 0.300 | pF |
| 21-06.8b | bank at code 15 | 1.200 | pF |
| 21-06.8c | code-0 band, low edge | 4.594 | GHz |
| 21-06.8d | code-0 band, high edge | 4.843 | GHz |
| 21-06.8e | code-15 band, low edge | 3.333 | GHz |
| 21-06.8f | code-15 band, high edge | 3.424 | GHz |
| 21-06.8g | total tuning range | 36.9 | % |
| 21-06.8h | code-0 top with ideal switches | 5.931 | GHz |
| 21-06.9a | 2 kΩ noise density | 5.756 | nV/√Hz |
| 21-06.9b | maximum K_VCO | 77.7 | MHz/V |
| 21-06.9c | ripple spur | −74.23 | dBc |
| 21-06.10a | after ×3 | −118.46 | dBc/Hz |
| 21-06.10b | after ÷8 at 1 MHz | −146.06 | dBc/Hz |
| 21-06.10c | after ÷8 at 10 MHz, ideal | −166.06 | dBc/Hz |
| 21-06.10d | after ÷8 at 10 MHz, with floor | −154.67 | dBc/Hz |
| 21-06.11a | rms phase error | 22.29 | mrad |
| 21-06.11b | rms phase error | 1.277 | deg |
| 21-06.11c | EVM | 2.229 | % |
| 21-06.11d | share of 256-QAM budget | 40.5 | % |
| 21-06.11e | share of 1024-QAM budget | 79.5 | % |
| 21-06.11f | in-band level for 1% EVM | −101.96 | dBc/Hz |
| 21-06.12a | phase error, no gain error | 1.146 | deg |
| 21-06.12b | duty-cycle tolerance | 0.637 | % |
| 21-06.12c | phase error with 1% gain error | 0.994 | deg |
| 21-06.12d | duty-cycle tolerance | 0.552 | % |
| 21-06.12e | small-error estimate of (c) | 0.992 | deg |
| 21-06.13a | phase difference | 90.285 | deg |
| 21-06.13b | phase error | 0.285 | deg |
| 21-06.13c | gain error | 0.501 | % |
| 21-06.13d | IRR, exact | 49.05 | dB |
| 21-06.13e | IRR, small-error | 49.04 | dB |
| 21-06.14a | tolerable lock range | 632.5 | kHz |
| 21-06.14b | current ratio | 2.530e-3 | |
| 21-06.14c | coupling | −51.94 | dB |
| 21-06.14d | exact pull | 10.00 | kHz |
| 21-06.15a | FoM, one core | 190.0 | dB |
| 21-06.15b | phase noise, four cores | −126.02 | dBc/Hz |
| 21-06.15c | FoM, four cores | 190.0 | dB |
| 21-06.15d | minimum cores, real | 3.162 | |
| 21-06.15e | cores needed | 4 | |
| 21-06.15f | FoM gain from doubling Q | 6.02 | dB |
