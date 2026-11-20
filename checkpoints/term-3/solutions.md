# Term 3 Checkpoint · Solutions

Questions: [README.md](README.md). Every numerical answer, and the letter of every multiple-choice answer, is checked by [verify_term3.py](verify_term3.py), which recomputes each value by its own route (root finding, numerical integration, simulation, FFTs). Each explanation names the chapter to revisit.

**Scoring by block:** semiconductor devices 16, Electronics I 17, signals and systems 17. Aim for at least 70% in each (12, 12 and 12 correct).

---

## Block 1 · Semiconductor devices

**1. Answer: 0.357 eV.** $E_F - E_i = kT\ln(n/n_i) = 0.025852\ln(10^6)$ = 0.357 eV. *([09-02](../../courses/09-semiconductor-devices/chapters/09-02-carriers-doping-fermi-level.md))*

**2. Answer: (C) 0.774 V.** $V_{bi} = V_T\ln(N_AN_D/n_i^2) = 0.025852\ln(10^{13})$ = 0.774 V. (A) uses the older $n_i$ = 1.5 × 10¹⁰ cm⁻³; (B) doubles the n side's $E_F - E_i$; (D) is $2\phi_B$ of the p side alone. *([09-05](../../courses/09-semiconductor-devices/chapters/09-05-pn-junction-electrostatics.md))*

**3. Answer: 0.332 µm.** $W = \sqrt{(2\varepsilon_sV_{bi}/q)(1/N_A + 1/N_D)} = \sqrt{2 \times 1.036 \times 10^{-12} \times 0.774/(1.602 \times 10^{-19}) \times 1.1 \times 10^{-16}}$ = 3.32 × 10⁻⁵ cm. Most of it lies on the lightly doped side. *([09-05](../../courses/09-semiconductor-devices/chapters/09-05-pn-junction-electrostatics.md))*

**4. Answer: 0.500 Ω·cm.** $\rho = 1/(qn\mu_n) = 1/(1.602 \times 10^{-19} \times 10^{16} \times 1248)$. *([09-03](../../courses/09-semiconductor-devices/chapters/09-03-drift-and-diffusion.md))*

**5. Answer: (A) 31.0 cm²/s.** Einstein relation $D = \mu V_T = 1200 \times 0.025852$. (B) slips a decimal; (C) uses $kT/q$ at 450 K; (D) forgets $V_T$. *([09-03](../../courses/09-semiconductor-devices/chapters/09-03-drift-and-diffusion.md))*

**6. Answer: 34.6 µm.** $L_p = \sqrt{D_p\tau_p} = \sqrt{12 \times 10^{-6}}$ cm = 3.46 × 10⁻³ cm. *([09-04](../../courses/09-semiconductor-devices/chapters/09-04-generation-recombination-continuity.md))*

**7. Answer: (B) 59.5 mV.** $\Delta V = nV_T\ln 10$ = 59.5 mV. (A) is $V_T$ itself (a factor of e, not 10); (C) is $n$ = 2. *([09-06](../../courses/09-semiconductor-devices/chapters/09-06-pn-junction-iv-and-capacitance.md))*

**8. Answer: 0.366.** $C_j \propto 1/W \propto (V_{bi} - V)^{-1/2}$, so the ratio is $\sqrt{0.774/5.774}$ = 0.366. *([09-06](../../courses/09-semiconductor-devices/chapters/09-06-pn-junction-iv-and-capacitance.md))*

**9. Answer: (B) 17.3 fF/µm².** $C_{ox} = \varepsilon_{ox}/T_{ox} = 3.453 \times 10^{-13}/(2 \times 10^{-7})$ = 1.73 × 10⁻⁶ F/cm² = 17.3 fF/µm² (1 F/cm² = 10⁷ fF/µm²). (A) uses 20 nm; (C) uses silicon's permittivity; (D) both. *([09-08](../../courses/09-semiconductor-devices/chapters/09-08-mos-capacitor.md))*

**10. Answer: 0.833 V.** $\phi_B = V_T\ln(N_A/n_i) = 0.025852\ln(10^7)$ = 0.417 V; $2\phi_B$ = 0.833 V. *([09-08](../../courses/09-semiconductor-devices/chapters/09-08-mos-capacitor.md))*

**11. Answer: (A) 0.104 µm.** $W_{d\max} = \sqrt{2\varepsilon_s(2\phi_B)/(qN_A)}$ = 1.04 × 10⁻⁵ cm. (B) uses $\phi_B$, (C) $4\phi_B$, (D) slips a factor of ten. *([09-08](../../courses/09-semiconductor-devices/chapters/09-08-mos-capacitor.md))*

**12. Answer: 77.4 mV/decade.** $S = mV_T\ln10 = 1.3 \times 59.5$ mV. *([09-09](../../courses/09-semiconductor-devices/chapters/09-09-long-channel-mosfet.md))*

**13. Answer: (B) 199.** $\beta = \alpha/(1 - \alpha) = 0.995/0.005$. (C) uses $1/(1 - \alpha)$. *([09-07](../../courses/09-semiconductor-devices/chapters/09-07-bipolar-junction-transistor.md))*

**14. Answer: 1.11 µm.** $\lambda_c = hc/E_g = 1.2398/1.12$ µm. *([09-14](../../courses/09-semiconductor-devices/chapters/09-14-optoelectronic-devices.md))*

**15. Answer: (A) 1.46 eV.** $E = hc/\lambda = 1.2398/0.850$. (C) inverts the ratio. *([09-14](../../courses/09-semiconductor-devices/chapters/09-14-optoelectronic-devices.md))*

**16. Answer: 7.14 ps.** Constant-field scaling divides delay by κ: 10.0/1.4. *([09-11](../../courses/09-semiconductor-devices/chapters/09-11-cmos-and-scaling.md))*

## Block 2 · Electronics I

**17. Answer: (B) 1.95 mA.** $(5.0 - 0.7)/2.2$ kΩ. (A) ignores the drop; (C) subtracts two drops. *([10-01](../../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md))*

**18. Answer: 25.9 Ω.** $r_d = V_T/I_D$ = 25.852 mV/1 mA. *([10-01](../../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md))*

**19. Answer: (B) 0.266 V.** Full-wave: $V_r = V_p/(2fRC) = 15/(2 \times 60 \times 1000 \times 470\ \mu\text{F})$. (A) is the half-wave formula. *([10-01](../../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md))*

**20. Answer: 153 Ω.** At the lowest input and full load the resistor must carry 32 mA: $(10 - 5.1)/0.032$ = 153 Ω. *([10-01](../../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md))*

**21. Answer: (B) 0.420 mA.** $V_{ov}$ = 0.5 V > $V_{DS}$ = 0.3 V, so the transistor is in triode: $k_n(V_{ov} - V_{DS}/2)V_{DS} = 4(0.5 - 0.15)(0.3)$. (A) assumes saturation without checking the region. *([10-02](../../courses/10-electronics-1/chapters/10-02-mosfet-dc-operation-and-biasing.md))*

**22. Answer: 2.00 mA/V.** $g_m = \sqrt{2k_nI_D} = \sqrt{2 \times 4 \times 0.5}$. *([10-04](../../courses/10-electronics-1/chapters/10-04-small-signal-models.md))*

**23. Answer: (A) 2.59 kΩ.** $g_m = I_C/V_T$ = 38.7 mA/V; $r_\pi = \beta/g_m$ = 2.59 kΩ. (D) divides β by $V_T$ expressed in millivolts. *([10-04](../../courses/10-electronics-1/chapters/10-04-small-signal-models.md))*

**24. Answer: −16.7.** $-g_m(R_D \parallel r_o) = -2\ \text{mS} \times 8.33\ \text{k}\Omega$. *([10-06](../../courses/10-electronics-1/chapters/10-06-mos-single-stage-amplifiers.md))*

**25. Answer: (B) −9.51.** $-R_C/(r_e + R_E)$ with $r_e \approx V_T/I_C$ = 25.9 Ω: $-5000/525.9$. (A) ignores $r_e$; (C) ignores $R_E$. *([10-07](../../courses/10-electronics-1/chapters/10-07-bjt-single-stage-amplifiers.md))*

**26. Answer: 0.800.** $g_mR_S/(1 + g_mR_S) = 4/5$. *([10-06](../../courses/10-electronics-1/chapters/10-06-mos-single-stage-amplifiers.md))*

**27. Answer: (B) 47.6 dB.** $20\log_{10}(20 \times 15 \times 0.8) = 20\log_{10}240$. (A) ignores the loading; (C) uses $10\log_{10}$. *([10-05](../../courses/10-electronics-1/chapters/10-05-amplifier-fundamentals.md))*

**28. Answer: 111 µA.** $I_{out} = I_{ref}(1 + \lambda V_{DS2})/(1 + \lambda V_{GS}) = 100 \times 1.2/1.08$. *([10-08](../../courses/10-electronics-1/chapters/10-08-current-sources-and-mirrors.md))*

**29. Answer: (A) 100 kHz.** Noise gain $1 + R_f/R_g$ = 100; bandwidth $10\ \text{MHz}/100$. (D) divides by 99. *([10-09](../../courses/10-electronics-1/chapters/10-09-real-op-amps-nonidealities.md))*

**30. Answer: 207 kHz.** $\text{SR}/(2\pi V_p) = 6.5 \times 10^6/(2\pi \times 5)$. *([10-09](../../courses/10-electronics-1/chapters/10-09-real-op-amps-nonidealities.md))*

**31. Answer: (C) 22.0 mV.** Offset is amplified by the noise gain $1 + R_2/R_1$ = 11, not the signal gain 10 (B). *([10-09](../../courses/10-electronics-1/chapters/10-09-real-op-amps-nonidealities.md))*

**32. Answer: 54.0 dB.** $(1 + 1)/(4 \times 0.001) = 500$, and $20\log_{10}500$ = 54.0 dB. *([10-10](../../courses/10-electronics-1/chapters/10-10-op-amp-application-circuits.md))*

**33. Answer: (A) 0.500 V.** Hysteresis $V_{DD}R_1/R_2 = 5 \times 10/100$. (B) uses $R_1/(R_1 + R_2)$. *([10-10](../../courses/10-electronics-1/chapters/10-10-op-amp-application-circuits.md))*

## Block 3 · Signals and systems

**34. Answer: (A) 0.100 s.** The components are at 20 Hz and 30 Hz; their greatest common divisor is 10 Hz. (B) and (C) are the components' own periods. *([11-01](../../courses/11-signals-and-systems/chapters/11-01-signals-classification-and-operations.md))*

**35. Answer: 3.** $y = \{1, 3, 3, 2\}$; $y[1] = x[0]h[1] + x[1]h[0] = 2 + 1$. *([11-03](../../courses/11-signals-and-systems/chapters/11-03-convolution.md))*

**36. Answer: (A).** A delay is linear and time-invariant. (B) is time-varying (time scaling), (C) is time-varying, (D) is not linear (zero in gives 1 out). *([11-02](../../courses/11-signals-and-systems/chapters/11-02-system-properties.md))*

**37. Answer: 5.00.** $\sum\lvert h\rvert = 1/(1 - 0.8)$, reached by a constant input of 1. *([11-02](../../courses/11-signals-and-systems/chapters/11-02-system-properties.md))*

**38. Answer: (A) 0.849 V.** Odd harmonics of a ±$A$ square wave have amplitude $4A/(\pi k)$: $8/(3\pi)$. (B) uses ±1 V; (C) is the fundamental; (D) assumes $1/k^2$ decay. *([11-05](../../courses/11-signals-and-systems/chapters/11-05-fourier-series.md))*

**39. Answer: 220 µs.** $t_r = RC\ln 9 = 0.1\ \text{ms} \times 2.197$ (equivalently $0.35/f_{3dB}$ with $f_{3dB}$ = 1.59 kHz). *([11-06](../../courses/11-signals-and-systems/chapters/11-06-continuous-time-fourier-transform.md))*

**40. Answer: (A) 0.707.** $\lvert H\rvert = \lvert\cos(\omega/2)\rvert$ = cos(π/4). *([11-07](../../courses/11-signals-and-systems/chapters/11-07-discrete-time-fourier-transform.md))*

**41. Answer: 208 µs.** $(N - 1)/2$ = 10 samples at 48 kHz. *([11-07](../../courses/11-signals-and-systems/chapters/11-07-discrete-time-fourier-transform.md))*

**42. Answer: (A).** Stability needs the ROC to contain the $j\omega$ axis: −2 < σ < 1, a strip, so the system is two-sided and noncausal. *([11-08](../../courses/11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md))*

**43. Answer: 9.48%.** ζ = 3/5 = 0.6; overshoot $e^{-\pi\zeta/\sqrt{1 - \zeta^2}} = e^{-3\pi/4}$. *([11-08](../../courses/11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md))*

**44. Answer: (B).** A causal filter needs every pole inside the unit circle; the pole at −1.2 contributes $(-1.2)^n$. *([11-09](../../courses/11-signals-and-systems/chapters/11-09-z-transform.md))*

**45. Answer: 50.9 Hz.** Bandwidth ≈ $2(1 - r)$ = 0.04 rad/sample, times $f_s/2\pi$. *([11-09](../../courses/11-signals-and-systems/chapters/11-09-z-transform.md))*

**46. Answer: (A) 3 kHz.** $\lvert 7 - 10\rvert$ kHz. *([11-10](../../courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md))*

**47. Answer: 44.0 kHz.** Twice the highest frequency; a practical rate must exceed it. *([11-10](../../courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md))*

**48. Answer: (B) 74.0 dB.** $6.02 \times 12 + 1.76$. (A) omits the 1.76 dB; (C) is 16 bits; (D) is 11 bits. *([11-10](../../courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md))*

**49. Answer: 33.3%.** $m^2P_x/(1 + m^2P_x)$ with $P_x = 1/2$ and $m = 1$. *([11-11](../../courses/11-signals-and-systems/chapters/11-11-modulation-and-filtering-applications.md))*

**50. Answer: (A) 1810 kHz.** $f_{RF} + 2f_{IF} = 900 + 910$. (B) is the LO frequency. *([11-11](../../courses/11-signals-and-systems/chapters/11-11-modulation-and-filtering-applications.md))*

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T3.01 | E_F − E_i | 0.357 | eV |
| T3.02 | built-in potential | 0.774 | V |
| T3.03 | depletion width | 0.332 | µm |
| T3.04 | resistivity | 0.500 | Ω·cm |
| T3.05 | diffusion coefficient | 31.0 | cm²/s |
| T3.06 | diffusion length | 34.6 | µm |
| T3.07 | voltage per decade | 59.5 | mV |
| T3.08 | capacitance ratio | 0.366 | — |
| T3.09 | oxide capacitance | 17.3 | fF/µm² |
| T3.10 | 2φ_B | 0.833 | V |
| T3.11 | maximum depletion width | 0.104 | µm |
| T3.12 | subthreshold swing | 77.4 | mV/decade |
| T3.13 | β | 199 | — |
| T3.14 | cutoff wavelength | 1.11 | µm |
| T3.15 | photon energy | 1.46 | eV |
| T3.16 | scaled delay | 7.14 | ps |
| T3.17 | diode current | 1.95 | mA |
| T3.18 | small-signal resistance | 25.9 | Ω |
| T3.19 | ripple | 0.266 | V |
| T3.20 | series resistor | 153 | Ω |
| T3.21 | drain current | 0.420 | mA |
| T3.22 | transconductance | 2.00 | mA/V |
| T3.23 | r_π | 2.59 | kΩ |
| T3.24 | common-source gain | −16.7 | — |
| T3.25 | degenerated CE gain | −9.51 | — |
| T3.26 | follower gain | 0.800 | — |
| T3.27 | cascade gain | 47.6 | dB |
| T3.28 | mirror output | 111 | µA |
| T3.29 | closed-loop bandwidth | 100 | kHz |
| T3.30 | full-power bandwidth | 207 | kHz |
| T3.31 | output offset | 22.0 | mV |
| T3.32 | CMRR bound | 54.0 | dB |
| T3.33 | hysteresis | 0.500 | V |
| T3.34 | fundamental period | 0.100 | s |
| T3.35 | y[1] | 3 | — |
| T3.37 | BIBO bound | 5.00 | — |
| T3.38 | third-harmonic amplitude | 0.849 | V |
| T3.39 | rise time | 220 | µs |
| T3.40 | gain at π/2 | 0.707 | — |
| T3.41 | group delay | 208 | µs |
| T3.43 | overshoot | 9.48 | % |
| T3.45 | resonator bandwidth | 50.9 | Hz |
| T3.46 | alias | 3 | kHz |
| T3.47 | Nyquist rate | 44.0 | kHz |
| T3.48 | ideal SNR | 74.0 | dB |
| T3.49 | sideband power fraction | 33.3 | % |
| T3.50 | image frequency | 1810 | kHz |
