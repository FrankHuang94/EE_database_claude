# Full-Length FE Practice Exam · Solutions

Questions: [README.md](README.md). [verify_fe.py](verify_fe.py) recomputes every numerical answer by a second route where one exists (numerical differentiation, integration and ODE solution, matrix solvers, sampled and exact probabilities, explicit cash-flow sums, simulated circuits and sequences) and checks the letter of every numeric multiple-choice answer. Conceptual answers are checked against the letters recorded in the script. Each explanation names the chapter to revisit.

**Scoring by area.** Count your correct answers in each area and divide by the area's size. Aim for at least 70% in every area, then in total. Areas below 70% point to the chapters named in their explanations.

| Area | Questions | Count |
|---|---|---|
| Mathematics | 1–13 | 13 |
| Probability and statistics | 14–17 | 4 |
| Ethics and professional practice | 18–21 | 4 |
| Engineering economics | 22–26 | 5 |
| Properties of electrical materials | 27–30 | 4 |
| Circuit analysis | 31–44 | 14 |
| Linear systems | 45–49 | 5 |
| Signal processing | 50–54 | 5 |
| Electronics | 55–62 | 8 |
| Power systems | 63–71 | 9 |
| Electromagnetics | 72–75 | 4 |
| Control systems | 76–82 | 7 |
| Communications | 83–87 | 5 |
| Computer networks | 88–91 | 4 |
| Digital systems | 92–101 | 10 |
| Computer systems | 102–106 | 5 |
| Software engineering | 107–110 | 4 |

---

## Mathematics

**1. Answer: 0.736.** Product rule: $f'(x) = 3x^2e^{-x} - x^3e^{-x} = x^2(3 - x)e^{-x}$, so $f'(1) = 2e^{-1} = 0.7358$. *([01-03](../../courses/01-calculus-for-engineers/chapters/01-03-derivatives.md))*

**2. Answer: (B) 1.571.** $\sin^2x = \tfrac12(1 - \cos 2x)$, so the integral is $\tfrac12[x - \tfrac12\sin 2x]_0^{\pi} = \pi/2 = 1.571$. (A) forgets the factor of one half; (C) is $\pi/4$; (D) is $\int_0^\pi \sin x\,dx$. *([01-06](../../courses/01-calculus-for-engineers/chapters/01-06-techniques-of-integration.md))*

**3. Answer: 3.** Subtract the first equation from the second: $x - 2y = -3$. Add the first and third: $2x + 3y = 8$. Then $x = 2y - 3$ gives $7y = 14$, so $y = 2$, $x = 1$ and $z = 6 - 1 - 2 = 3$. Check: $1 + 4 - 3 = 2$. *([02-06](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-06-vectors-matrices-and-linear-systems.md))*

**4. Answer: (D) 5.** The characteristic equation is $\lambda^2 - 7\lambda + 10 = 0$ (trace 7, determinant $12 - 2 = 10$), so $\lambda = 5$ and $2$. (A) is the trace and (B) the determinant. *([02-08](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-08-eigenvalues-and-eigenvectors.md))*

**5. Answer: 3.54.** Magnitudes divide: $\lvert 3 + j4\rvert/\lvert 1 - j\rvert = 5/\sqrt2 = 3.536$. *([02-01](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md))*

**6. Answer: (C) 120.** The point is in the second quadrant: $\operatorname{atan2}(\sqrt3, -1) = 180° - 60° = 120°$. (B) is what a calculator's $\tan^{-1}(\sqrt3/-1)$ returns without the quadrant correction. *([02-01](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md))*

**7. Answer: 1.26.** The solution is $y = 2(1 - e^{-4t})$: final value $8/4 = 2$, time constant 0.25. At $t = 0.25$, $y = 2(1 - e^{-1}) = 1.264$. *([02-02](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-02-first-order-linear-odes.md))*

**8. Answer: (A) 3.** The roots of $r^2 + 4r + 13 = 0$ are $-2 \pm j3$, so the solution is $e^{-2t}(c_1\cos 3t + c_2\sin 3t)$: it oscillates at 3 rad/s. (C) is the undamped natural frequency $\sqrt{13}$. *([02-03](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-03-second-order-linear-odes.md))*

**9. Answer: 1.55.** Partial fractions: $6/[s(s + 3)] = 2/s - 2/(s + 3)$, so $f(t) = 2(1 - e^{-3t})$ and $f(0.5) = 2(1 - e^{-1.5}) = 1.554$. *([02-05](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-05-laplace-transform-for-odes.md))*

**10. Answer: (D) 1.049.** $\sqrt{1 + x} \approx 1 + x/2 - x^2/8$, so $1 + 0.05 - 0.00125 = 1.04875$. The exact value is 1.04881. (A) stops at first order. *([01-08](../../courses/01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md))*

**11. Answer: 13.6.** $\partial f/\partial x = 2xy = 4$ and $\partial f/\partial y = x^2 + 6y = 13$ at $(1, 2)$, so $\lvert\nabla f\rvert = \sqrt{16 + 169} = \sqrt{185} = 13.60$. *([01-09](../../courses/01-calculus-for-engineers/chapters/01-09-multivariable-calculus-1.md))*

**12. Answer: (B) 1.5.** $x_1 = x_0 - f(x_0)/f'(x_0) = 1 - (-1)/2 = 1.5$. (C) is the root itself, reached only after more steps. *([02-10](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-10-numerical-methods.md))*

**13. Answer: 63.6.** $\mathbf a\cdot\mathbf b = 2 - 2 + 4 = 4$ and both vectors have length 3, so $\cos\theta = 4/9$ and $\theta = 63.6°$. *([02-06](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-06-vectors-matrices-and-linear-systems.md))*

## Probability and statistics

**14. Answer: (C) 0.9545.** ±20 Ω is ±2σ, and $\Phi(2) - \Phi(-2) = 0.9545$. (A) is ±1σ and (B) ±3σ. *([03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md))*

**15. Answer: 0.364.** $P(0) = 0.98^{50} = 0.3642$. (The Poisson approximation $e^{-1} = 0.368$ is close.) *([03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md))*

**16. Answer: (A) 0.279.** Bayes: $P(D\mid +) = 0.95 \times 0.02/(0.95 \times 0.02 + 0.05 \times 0.98) = 0.019/0.068 = 0.279$. (B) confuses $P(+\mid D)$ with $P(D\mid +)$; (C) is the joint probability. *([03-01](../../courses/03-probability-statistics-and-random-variables/chapters/03-01-probability-in-ee-language.md))*

**17. Answer: 20.6.** With 24 degrees of freedom, $t_{0.025} = 2.064$. The half-width is $t\,s/\sqrt n = 2.064 \times 0.05/5 = 0.02064$ V. *([03-05](../../courses/03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md))*

## Ethics and professional practice

**18. Answer: (B).** The Model Rules put the public's safety, health and welfare first; the engineer should notify the employer and, if the danger remains, the appropriate authority. *([26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md))*

**19. Answer: (D).** Engineers may not solicit or accept gifts or other valuable consideration from parties dealing with their employer or client in connection with the work. Disclosure after the fact does not cure it, and the part's merits are irrelevant. *([26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md))*

**20. Answer: (A).** A licensee may seal only work prepared under their responsible charge. A quick review does not create responsible charge, and the preparer's licence elsewhere does not transfer. *([26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md))*

**21. Answer: 2041.** A US utility patent's term runs 20 years from the earliest non-provisional filing date, not from the grant: 2021 + 20 = 2041. *([26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md))*

## Engineering economics

**22. Answer: (A) 6806.** $P = F/(1 + i)^n = 10{,}000/1.08^5 = 6805.8$ dollars. (D) compounds instead of discounting; (C) subtracts simple interest. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

**23. Answer: 9.79.** $(A/P, 7\%, 6) = 0.07 \times 1.07^6/(1.07^6 - 1) = 0.20980$ and $(A/F) = 0.13980$. EAC $= 50{,}000 \times 0.20980 - 5{,}000 \times 0.13980 = 10{,}490 - 699 = 9{,}791$ dollars. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

**24. Answer: (D) 10000.** Break-even $= F/(p - v) = 200{,}000/(50 - 30) = 10{,}000$ units. (A) divides by the price and (B) by the variable cost. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

**25. Answer: 60.0.** Depreciation is $(120 - 20)/5 = 20$ k a year, so the book value after 3 years is $120 - 60 = 60$ k. *([26-04](../../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md))*

**26. Answer: (C) 6.14.** $(1 + 0.06/4)^4 - 1 = 1.015^4 - 1 = 6.136\%$. (B) is continuous compounding, $e^{0.06} - 1 = 6.18\%$, rounded down; (D) is the quarterly rate. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

## Properties of electrical materials

**27. Answer: 2.19.** $A = \pi(0.5 \times 10^{-3})^2 = 7.854 \times 10^{-7}$ m², so $R = \rho L/A = 1.72 \times 10^{-8} \times 100/7.854 \times 10^{-7} = 2.190$ Ω. *([04-05](../../courses/04-physics-for-ee/chapters/04-05-current-resistance-and-conduction.md))*

**28. Answer: (B) 12.2.** $R = R_0[1 + \alpha(T - T_0)] = 10[1 + 0.00393 \times 55] = 12.16$ Ω. (A) uses 5 °C of rise; (C) uses 75 °C. *([04-05](../../courses/04-physics-for-ee/chapters/04-05-current-resistance-and-conduction.md))*

**29. Answer: 1.00 × 10⁴.** Mass action: $p = n_i^2/N_D = 10^{20}/10^{16} = 10^4$ cm⁻³, since $n \approx N_D$. *([09-02](../../courses/09-semiconductor-devices/chapters/09-02-carriers-doping-fermi-level.md))*

**30. Answer: (D) 354.** $C = \varepsilon_r\varepsilon_0A/d = 4 \times 8.854 \times 10^{-12} \times 10^{-4}/10^{-5} = 3.54 \times 10^{-10}$ F. (A) drops $\varepsilon_r$. *([04-04](../../courses/04-physics-for-ee/chapters/04-04-potential-capacitance-and-dielectrics.md))*

## Circuit analysis

**31. Answer: 4.00.** The lower resistor in parallel with the load is 5 kΩ, so the output is $12 \times 5/(10 + 5) = 4.00$ V (not 6 V, the unloaded value). *([06-03](../../courses/06-circuit-analysis-1-dc/chapters/06-03-kirchhoffs-laws.md))*

**32. Answer: (A) 4.** $6 \parallel 3 = 18/9 = 2$ Ω, plus 2 Ω in series gives 4 Ω. (B) adds all three. *([06-08](../../courses/06-circuit-analysis-1-dc/chapters/06-08-thevenin-and-norton.md))*

**33. Answer: 4.00.** Node 2: $(V_2 - V_1)/2 + V_2/6 = 0$, so $V_1 = \tfrac43V_2$. Node 1: $V_1/4 + (V_1 - V_2)/2 = 2$, which gives $V_2/3 + V_2/6 = 2$ and $V_2 = 4.00$ V ($V_1$ = 5.33 V). *([06-04](../../courses/06-circuit-analysis-1-dc/chapters/06-04-nodal-analysis.md))*

**34. Answer: (C) 0.5.** With $R_L = R_{Th}$, $P_{max} = V_{Th}^2/(4R_{Th}) = 100/200 = 0.5$ W. (A) omits the factor of 4 and uses $V^2/2R$. *([06-09](../../courses/06-circuit-analysis-1-dc/chapters/06-09-maximum-power-transfer.md))*

**35. Answer: 4.32.** $\tau = RC = 1$ ms, so $v = 5(1 - e^{-2}) = 4.323$ V. *([07-02](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md))*

**36. Answer: (B) 0.1.** 63% is one time constant, $\tau = L/R = 0.01/100 = 0.1$ ms. *([07-02](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md))*

**37. Answer: 48.2.** $X_L = 2\pi \times 60 \times 0.1 = 37.70$ Ω, so $\lvert Z\rvert = \sqrt{30^2 + 37.70^2} = 48.18$ Ω. *([07-05](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-05-sinusoidal-steady-state-and-impedance.md))*

**38. Answer: (D) −51.5.** $\angle Z = \tan^{-1}(37.70/30) = 51.5°$, and the current lags the voltage by that angle: −51.5°. (A) has the sign of the impedance; (B) is the complement. *([07-05](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-05-sinusoidal-steady-state-and-impedance.md))*

**39. Answer: 15.9.** $f_0 = 1/(2\pi\sqrt{LC}) = 1/(2\pi\sqrt{10^{-10}}) = 15{,}915$ Hz. *([07-08](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md))*

**40. Answer: (A) 20.** $Q = (1/R)\sqrt{L/C} = 0.1 \times \sqrt{40{,}000} = 20$. (C) omits the $1/R$. *([07-08](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md))*

**41. Answer: 1.38.** $Q = VI\sin\phi = 230 \times 10 \times 0.6 = 1380$ var, since $\sin\phi = \sqrt{1 - 0.8^2} = 0.6$. *([07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md))*

**42. Answer: (C) 83.0.** The capacitor must supply 1380 var: $C = Q/(\omega V^2) = 1380/(2\pi \times 50 \times 230^2) = 83.0$ µF. (A) uses 60 Hz and the real power; (D) doubles it. *([07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md))*

**43. Answer: −2.00.** $v_o = -(R_f/R_{in})v_i = -10 \times 0.2 = -2.00$ V. *([06-10](../../courses/06-circuit-analysis-1-dc/chapters/06-10-ideal-op-amp.md))*

**44. Answer: (B) 10.** $1 + R_f/R_g = 1 + 9 = 10$. (A) is the inverting magnitude. *([06-10](../../courses/06-circuit-analysis-1-dc/chapters/06-10-ideal-op-amp.md))*

## Linear systems

**45. Answer: 1.41.** $\lvert H(j5)\rvert = 10/\lvert 5 + j5\rvert = 10/7.071 = 1.414$: 3 dB below the DC gain of 2, as expected at the pole frequency. *([11-08](../../courses/11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md))*

**46. Answer: (D) unstable.** The denominator factors as $(s + 3)(s - 1)$, so there is a pole at $s = +1$ in the right half-plane. *([11-08](../../courses/11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md); [15-05](../../courses/15-control-systems/chapters/15-05-stability-routh-hurwitz.md))*

**47. Answer: 5.** $y[2] = x[2]h[0] + x[1]h[1] = 3 + 2 = 5$; the whole output is $\{1, 3, 5, 3\}$. *([11-03](../../courses/11-signals-and-systems/chapters/11-03-convolution.md))*

**48. Answer: (A) 0.782.** $e^{-t/\tau} = 0.02$ gives $t = \tau\ln 50 = 3.912 \times 0.2 = 0.782$ s, the exact form of the "$4\tau$" rule. (C) is the 90% time, $\tau\ln 10$. *([15-03](../../courses/15-control-systems/chapters/15-03-time-response.md))*

**49. Answer: 20.0.** $\lvert H\rvert = 1000/\lvert 10 + j100\rvert = 1000/100.50 = 9.950$, and $20\log_{10} 9.950 = 19.96$ dB. *([07-07](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-07-frequency-response-and-bode-plots.md))*

## Signal processing

**50. Answer: (C) 8.** Nyquist: $f_s > 2f_{max} = 8$ kHz. *([11-10](../../courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md))*

**51. Answer: 3.00.** A tone at $f$ sampled at $f_s$ appears at $\lvert f - kf_s\rvert$ folded into $[0, f_s/2]$: $\lvert 7 - 10\rvert = 3$ kHz. *([11-10](../../courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md))*

**52. Answer: (B) 46.9.** $f_s/N = 48{,}000/1024 = 46.875$ Hz. (A) uses $2N$; (C) uses $N/2$. *([16-03](../../courses/16-digital-signal-processing/chapters/16-03-the-dft.md))*

**53. Answer: 0.125.** $h[n] = 0.5^n u[n]$, so $h[3] = 0.125$. *([11-09](../../courses/11-signals-and-systems/chapters/11-09-z-transform.md))*

**54. Answer: (D) 74.0.** $6.02N + 1.76 = 72.24 + 1.76 = 74.0$ dB. (A) omits the 1.76 dB. *([20-06](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-06-data-converter-fundamentals.md))*

## Electronics

**55. Answer: 4.30.** $I = (5 - 0.7)/1000 = 4.30$ mA. *([10-01](../../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md))*

**56. Answer: (A) 9.58.** The resistor carries $(12 - 5.1)/470 = 14.68$ mA and the load takes $5.1/1000 = 5.10$ mA, so the Zener takes 9.58 mA. (B) forgets the load. *([10-01](../../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md))*

**57. Answer: 5.70.** $I_B = (5 - 0.7)/100\text{ k} = 43$ µA, $I_C = \beta I_B = 4.3$ mA, and $V_{CE} = 10 - 4.3 = 5.70$ V. It is above saturation, so the transistor is in the active region and the assumption holds. *([10-03](../../courses/10-electronics-1/chapters/10-03-bjt-dc-operation-and-biasing.md))*

**58. Answer: (C) 1.00.** $I_D = \tfrac12 \times 2 \times (1.5 - 0.5)^2 = 1.00$ mA. (A) omits the one half. *([10-02](../../courses/10-electronics-1/chapters/10-02-mosfet-dc-operation-and-biasing.md))*

**59. Answer: −10.0.** $g_m = k'(W/L)(V_{GS} - V_{TH}) = 2$ mA/V, so $A_v = -g_mR_D = -2 \times 5 = -10.0$. *([10-04](../../courses/10-electronics-1/chapters/10-04-small-signal-models.md); [10-06](../../courses/10-electronics-1/chapters/10-06-mos-single-stage-amplifiers.md))*

**60. Answer: (B) 0.833.** The capacitor discharges for about half a cycle at 60 Hz: $\Delta V \approx I/(2fC) = 0.1/(120 \times 10^{-3}) = 0.833$ V. (A) is the half-wave value. *([10-01](../../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md))*

**61. Answer: 500.** Bandwidth = GBW ÷ noise gain = 10 MHz ÷ 20 = 500 kHz. *([10-09](../../courses/10-electronics-1/chapters/10-09-real-op-amps-nonidealities.md))*

**62. Answer: (D) 80.** $20\log_{10}(1000/0.1) = 20\log_{10}10^4 = 80$ dB. *([12-01](../../courses/12-electronics-2/chapters/12-01-differential-pairs.md))*

## Power systems

**63. Answer: 23.0.** Phase voltage $480/\sqrt3 = 277.1$ V, so each phase takes $277.1^2/10 = 7680$ W and the total is 23.0 kW (equivalently $V_L^2/R$). *([07-11](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-11-three-phase-circuits.md))*

**64. Answer: (A) 27.7.** $I_L = I_\phi = 277.1/10 = 27.7$ A. (B) uses the line voltage across 10 Ω. *([07-11](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-11-three-phase-circuits.md))*

**65. Answer: 208.** $I_2 = S/V_2 = 50{,}000/240 = 208.3$ A. *([07-09](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-09-mutual-inductance-and-transformers.md))*

**66. Answer: (C) 190.** $Z_{base} = V_{base}^2/S_{base} = 138^2/100 = 190.4$ Ω. *([22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md))*

**67. Answer: 3.00.** $n_s = 120f/p = 1800$ rpm, so $s = (1800 - 1746)/1800 = 3.00\%$. *([22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md))*

**68. Answer: (B) 1000.** $n_s = 120 \times 50/6 = 1000$ rpm. (A) is a 4-pole machine. *([22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md))*

**69. Answer: 0.800.** pf $= P/S = 40/50 = 0.800$. *([07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md))*

**70. Answer: (D) 227.** $I = P/(\sqrt3 V_L \text{pf}) = 10^7/(\sqrt3 \times 33{,}000 \times 0.9) = 194.4$ A, and the loss is $3I^2R = 3 \times 194.4^2 \times 2 = 227$ kW. (A) counts one phase. *([22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md))*

**71. Answer: 230.** $E = V - I_aR_a = 240 - 50 \times 0.2 = 230$ V. *([22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md))*

## Electromagnetics

**72. Answer: (A) 0.899.** $F = kq_1q_2/r^2 = 8.988 \times 10^9 \times 10^{-12}/0.01 = 0.899$ N. (C) uses $r$ instead of $r^2$. *([04-02](../../courses/04-physics-for-ee/chapters/04-02-charge-coulomb-and-electric-fields.md))*

**73. Answer: 40.0.** $B = \mu_0I/(2\pi r) = 4\pi \times 10^{-7} \times 10/(2\pi \times 0.05) = 4.00 \times 10^{-5}$ T. *([04-06](../../courses/04-physics-for-ee/chapters/04-06-magnetic-fields-and-forces.md))*

**74. Answer: (C) 0.200.** $\lambda = c/(f\sqrt{\varepsilon_r}) = 0.3/1.5 = 0.200$ m. (A) is the free-space wavelength; (B) divides by $\varepsilon_r$, not its square root. *([13-07](../../courses/13-electromagnetics/chapters/13-07-transmission-lines-time-domain.md))*

**75. Answer: 1.50.** $\Gamma = (75 - 50)/(75 + 50) = 0.2$, so VSWR $= (1 + 0.2)/(1 - 0.2) = 1.50$ (for real loads, simply 75/50). *([13-08](../../courses/13-electromagnetics/chapters/13-08-transmission-lines-sinusoidal-steady-state.md))*

## Control systems

**76. Answer: (B) 0.2.** Type 1: $K_v = \lim_{s\to0} sG(s) = 20/4 = 5$, so $e_{ss} = 1/K_v = 0.2$. A type-1 loop follows a step with zero error, not a ramp. *([15-04](../../courses/15-control-systems/chapters/15-04-feedback-and-steady-state-error.md))*

**77. Answer: 16.3.** $M_p = e^{-\pi\zeta/\sqrt{1 - \zeta^2}} = e^{-1.814} = 0.163$. *([15-03](../../courses/15-control-systems/chapters/15-03-time-response.md))*

**78. Answer: (D) 6.** Routh array: $s^3$: 1, 3; $s^2$: 2, $K$; $s^1$: $(6 - K)/2$; $s^0$: $K$. Every first-column entry is positive for $0 < K < 6$. *([15-05](../../courses/15-control-systems/chapters/15-05-stability-routh-hurwitz.md))*

**79. Answer: 0.686.** $\omega_n = 5$ and $\zeta = 4/(2 \times 5) = 0.4$, so $t_p = \pi/(\omega_n\sqrt{1 - \zeta^2}) = \pi/(5 \times 0.9165) = 0.686$ s. *([15-03](../../courses/15-control-systems/chapters/15-03-time-response.md))*

**80. Answer: (A) 45.** PM $= 180° + \angle L(j\omega_c) = 180 - 135 = 45°$. *([15-07](../../courses/15-control-systems/chapters/15-07-frequency-domain-design.md))*

**81. Answer: 0.900.** $T(0) = K_pG(0)/(1 + K_pG(0)) = 9/10 = 0.900$; a type-0 loop leaves a 10% step error. *([15-04](../../courses/15-control-systems/chapters/15-04-feedback-and-steady-state-error.md))*

**82. Answer: (C) 0.5.** The poles have negative real parts, so the final-value theorem applies: $\lim_{s\to0} sG(s)/s = G(0) = 5/10 = 0.5$. *([15-03](../../courses/15-control-systems/chapters/15-03-time-response.md))*

## Communications

**83. Answer: 4.00.** $C = B\log_2(1 + \text{SNR}) = 10^6 \times \log_2 16 = 4.00$ Mb/s. *([17-07](../../courses/17-communication-systems/chapters/17-07-information-theory-and-shannon.md))*

**84. Answer: (B) 10.** DSB AM occupies twice the message bandwidth: 10 kHz. *([17-03](../../courses/17-communication-systems/chapters/17-03-analog-modulation.md))*

**85. Answer: 180.** $B \approx 2(\Delta f + f_m) = 2(75 + 15) = 180$ kHz. *([17-03](../../courses/17-communication-systems/chapters/17-03-analog-modulation.md))*

**86. Answer: (D) −114.** $-174 + 10\log_{10}10^6 = -174 + 60 = -114$ dBm. *([17-02](../../courses/17-communication-systems/chapters/17-02-noise-and-snr.md))*

**87. Answer: −77.0.** $P_r = P_t + G_t + G_r - L = 20 + 10 + 3 - 110 = -77.0$ dBm. *([21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md))*

## Computer networks

**88. Answer: (A) 62.** A /26 leaves 6 host bits: $2^6 - 2 = 62$ usable (the network and broadcast addresses are reserved). *([17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md))*

**89. Answer: 120.** $1500 \times 8/10^8 = 1.2 \times 10^{-4}$ s. *([17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md))*

**90. Answer: (C) TCP.** TCP provides acknowledged, ordered, retransmitted delivery; UDP and IP are best-effort; Ethernet is a link layer. *([17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md))*

**91. Answer: 10.0.** $2 \times 10^6/(2 \times 10^8) = 0.01$ s. *([17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md))*

## Digital systems

**92. Answer: (B) −10.** The sign bit is set, so the value is $246 - 256 = -10$ (invert to 00001001 and add 1: 00001010). (A) reads it as unsigned. *([08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md))*

**93. Answer: 4.** $\bar AB$ covers 010 and 011; $AC$ covers 101 and 111; they do not overlap, so there are 4 minterms (2, 3, 5, 7). *([08-02](../../courses/08-digital-logic-design/chapters/08-02-boolean-algebra-and-gates.md))*

**94. Answer: (D) NAND.** NAND alone makes NOT (tie inputs), AND and OR, so it is functionally complete; so is NOR. *([08-02](../../courses/08-digital-logic-design/chapters/08-02-boolean-algebra-and-gates.md))*

**95. Answer: 62.5.** Each stage divides by 2, so the MSB of a 4-bit counter toggles at $1/16$ of the clock: 62.5 kHz. *([08-07](../../courses/08-digital-logic-design/chapters/08-07-registers-counters-shift-registers.md))*

**96. Answer: (A) 63.** $3 \times 16 + 15 = 63$. *([08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md))*

**97. Answer: 0.250.** Slack $= T - t_{cq} - t_{logic} - t_{setup} = 2 - 0.2 - 1.4 - 0.15 = 0.250$ ns. *([08-10](../../courses/08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md))*

**98. Answer: (C) 286.** $f_{max} = 1/(0.1 + 3.2 + 0.2 \text{ ns}) = 1/3.5 \text{ ns} = 286$ MHz. (A) ignores clock-to-Q and setup. *([08-10](../../courses/08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md))*

**99. Answer: 32768.** $2^{12} \times 8 = 4096 \times 8 = 32{,}768$ bits (4 KB). *([08-11](../../courses/08-digital-logic-design/chapters/08-11-memories-and-programmable-logic.md))*

**100. Answer: (B) $\bar C$.** Minterms 0, 2, 4 and 6 are exactly the inputs with $C = 0$. *([08-03](../../courses/08-digital-logic-design/chapters/08-03-logic-minimization.md))*

**101. Answer: 14.** Gray code: $g_3 = b_3$, $g_i = b_{i+1} \oplus b_i$, so 1011 becomes 1110, which is 14. *([08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md))*

## Computer systems

**102. Answer: (D) 4.00.** AMAT $= 1 + 0.05 \times 60 = 4.00$ ns. *([14-09](../../courses/14-computer-organization-and-architecture/chapters/14-09-memory-hierarchy-and-caches.md))*

**103. Answer: 3.33.** Amdahl: $1/(0.2 + 0.8/8) = 1/0.3 = 3.33$. *([14-01](../../courses/14-computer-organization-and-architecture/chapters/14-01-performance-power-iron-law.md))*

**104. Answer: (A) 1.00.** $t = N \times \text{CPI}/f = 2 \times 10^9 \times 1.5/3 \times 10^9 = 1.00$ s. *([14-01](../../courses/14-computer-organization-and-architecture/chapters/14-01-performance-power-iron-law.md))*

**105. Answer: 17.** $32\text{ KB}/64\text{ B} = 512$ lines, so 9 index bits; 6 offset bits; the tag is $32 - 9 - 6 = 17$ bits. *([14-09](../../courses/14-computer-organization-and-architecture/chapters/14-09-memory-hierarchy-and-caches.md))*

**106. Answer: (C) 4.81.** Unpipelined: $5 \times 100 = 500$ cycles. Pipelined: $5 + 99 = 104$ cycles. The speedup is $500/104 = 4.81$, approaching 5 only for long runs. *([14-06](../../courses/14-computer-organization-and-architecture/chapters/14-06-pipelining-and-hazards.md))*

## Software engineering

**107. Answer: 20.** Each comparison halves the range: $\lceil\log_2(10^6 + 1)\rceil = 20$. *([05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md))*

**108. Answer: (B) hash table.** A hash table gives $O(1)$ average lookup; a search tree $O(\log n)$; a list $O(n)$. *([05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md))*

**109. Answer: 7.** $i$ takes 3, 7, 11, 15, 19, 23, 27: 7 iterations. *([05-01](../../courses/05-programming-for-engineers/chapters/05-01-python-fundamentals.md))*

**110. Answer: (D) integration testing.** Integration testing exercises the interfaces between modules; unit tests check modules alone; acceptance tests check requirements. *([05-09](../../courses/05-programming-for-engineers/chapters/05-09-software-engineering-practices.md))*

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| FE.001 | derivative at 1 | 0.736 | — |
| FE.002 | integral | 1.571 | — |
| FE.003 | z | 3 | — |
| FE.004 | larger eigenvalue | 5 | — |
| FE.005 | magnitude | 3.54 | — |
| FE.006 | angle | 120 | ° |
| FE.007 | y(0.25) | 1.26 | — |
| FE.008 | damped frequency | 3 | rad/s |
| FE.009 | f(0.5) | 1.55 | — |
| FE.010 | Taylor value | 1.049 | — |
| FE.011 | gradient magnitude | 13.6 | — |
| FE.012 | Newton step | 1.5 | — |
| FE.013 | angle between vectors | 63.6 | ° |
| FE.014 | fraction within two sigma | 0.9545 | — |
| FE.015 | probability of no defect | 0.364 | — |
| FE.016 | posterior probability | 0.279 | — |
| FE.017 | half-width | 20.6 | mV |
| FE.021 | expiry year | 2041 | — |
| FE.022 | present worth | 6806 | dollars |
| FE.023 | equivalent annual cost | 9.79 | k dollars |
| FE.024 | break-even volume | 10000 | units |
| FE.025 | book value | 60.0 | k dollars |
| FE.026 | effective rate | 6.14 | % |
| FE.027 | resistance | 2.19 | Ω |
| FE.028 | hot resistance | 12.2 | Ω |
| FE.029 | hole concentration | 1.00e4 | cm⁻³ |
| FE.030 | capacitance | 354 | pF |
| FE.031 | loaded divider output | 4.00 | V |
| FE.032 | Thévenin resistance | 4 | Ω |
| FE.033 | node-2 voltage | 4.00 | V |
| FE.034 | maximum power | 0.5 | W |
| FE.035 | capacitor voltage | 4.32 | V |
| FE.036 | time constant | 0.1 | ms |
| FE.037 | impedance magnitude | 48.2 | Ω |
| FE.038 | current phase | -51.5 | ° |
| FE.039 | resonant frequency | 15.9 | kHz |
| FE.040 | quality factor | 20 | — |
| FE.041 | reactive power | 1.38 | kvar |
| FE.042 | correction capacitance | 83.0 | µF |
| FE.043 | inverting output | -2.00 | V |
| FE.044 | non-inverting gain | 10 | — |
| FE.045 | magnitude | 1.41 | — |
| FE.047 | convolution sample | 5 | — |
| FE.048 | settling time | 0.782 | s |
| FE.049 | magnitude | 20.0 | dB |
| FE.050 | Nyquist rate | 8 | kHz |
| FE.051 | alias frequency | 3.00 | kHz |
| FE.052 | bin spacing | 46.9 | Hz |
| FE.053 | impulse-response sample | 0.125 | — |
| FE.054 | ideal SNR | 74.0 | dB |
| FE.055 | diode current | 4.30 | mA |
| FE.056 | Zener current | 9.58 | mA |
| FE.057 | collector-emitter voltage | 5.70 | V |
| FE.058 | drain current | 1.00 | mA |
| FE.059 | voltage gain | -10.0 | — |
| FE.060 | ripple | 0.833 | V |
| FE.061 | closed-loop bandwidth | 500 | kHz |
| FE.062 | CMRR | 80 | dB |
| FE.063 | total power | 23.0 | kW |
| FE.064 | line current | 27.7 | A |
| FE.065 | secondary current | 208 | A |
| FE.066 | base impedance | 190 | Ω |
| FE.067 | slip | 3.00 | % |
| FE.068 | synchronous speed | 1000 | rpm |
| FE.069 | power factor | 0.800 | — |
| FE.070 | line loss | 227 | kW |
| FE.071 | back EMF | 230 | V |
| FE.072 | Coulomb force | 0.899 | N |
| FE.073 | flux density | 40.0 | µT |
| FE.074 | wavelength | 0.200 | m |
| FE.075 | VSWR | 1.50 | — |
| FE.076 | ramp error | 0.2 | — |
| FE.077 | percent overshoot | 16.3 | % |
| FE.078 | maximum gain | 6 | — |
| FE.079 | peak time | 0.686 | s |
| FE.080 | phase margin | 45 | ° |
| FE.081 | closed-loop DC gain | 0.900 | — |
| FE.082 | final value | 0.5 | — |
| FE.083 | capacity | 4.00 | Mb/s |
| FE.084 | AM bandwidth | 10 | kHz |
| FE.085 | Carson bandwidth | 180 | kHz |
| FE.086 | noise power | -114 | dBm |
| FE.087 | received power | -77.0 | dBm |
| FE.088 | usable hosts | 62 | — |
| FE.089 | transmission time | 120 | µs |
| FE.091 | propagation delay | 10.0 | ms |
| FE.092 | two's-complement value | -10 | — |
| FE.093 | minterm count | 4 | — |
| FE.095 | MSB frequency | 62.5 | kHz |
| FE.096 | decimal value | 63 | — |
| FE.097 | setup slack | 0.250 | ns |
| FE.098 | maximum clock | 286 | MHz |
| FE.099 | ROM capacity | 32768 | bits |
| FE.101 | Gray-code value | 14 | — |
| FE.102 | average access time | 4.00 | ns |
| FE.103 | speedup | 3.33 | — |
| FE.104 | execution time | 1.00 | s |
| FE.105 | tag bits | 17 | — |
| FE.106 | pipeline speedup | 4.81 | — |
| FE.107 | comparisons | 20 | — |
| FE.109 | iterations | 7 | — |
