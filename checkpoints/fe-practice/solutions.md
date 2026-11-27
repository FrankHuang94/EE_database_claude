# Full-Length FE Practice Exam · Solutions

Questions: [README.md](README.md). Each explanation names the chapter to revisit, and every multiple-choice explanation names the mistake behind each wrong option.

**How the answers are checked.** [verify_fe.py](verify_fe.py) recomputes every numerical answer by a second route where one exists (numerical differentiation, quadrature and ODE integration, matrix solvers, scipy distributions, explicit cash-flow sums, simulated step and ramp responses, a simulated quantizer and rectifier, a Biot–Savart sum, a standing-wave sweep, cache, pipeline and finite-state-machine models). It recomputes every wrong option from the mistake named here, and checks that the lettered answer is the option equal to the correct value. Conceptual answers are checked by their text, and the Boolean ones by truth tables. The circuit answers are also simulated in ngspice ([fe_circuits.cir](fe_circuits.cir)).

**Scoring by area.** Count your correct answers in each area and divide by the area's size. Aim for at least 70% in every area, then in total. Areas below 70% point to the chapters named in their explanations.

| Area | Questions | Count |
|---|---|---|
| Mathematics | 1–12 | 12 |
| Probability and statistics | 13–17 | 5 |
| Ethics and professional practice | 18–21 | 4 |
| Engineering economics | 22–26 | 5 |
| Properties of electrical materials | 27–30 | 4 |
| Circuit analysis | 31–41 | 11 |
| Linear systems | 42–48 | 7 |
| Signal processing | 49–55 | 7 |
| Electronics | 56–64 | 9 |
| Power systems | 65–73 | 9 |
| Electromagnetics | 74–77 | 4 |
| Control systems | 78–84 | 7 |
| Communications | 85–89 | 5 |
| Computer networks | 90–93 | 4 |
| Digital systems | 94–101 | 8 |
| Computer systems | 102–106 | 5 |
| Software engineering | 107–110 | 4 |

---

## Mathematics

**1. Answer: (D) 3.** The roots of $r^2 + 4r + 13 = 0$ are $-2 \pm j3$, so the solution is $e^{-2t}(c_1\cos 3t + c_2\sin 3t)$: it oscillates at 3 rad/s. **Wrong options:** (A) 3.61 is the undamped natural frequency $\sqrt{13}$; (B) 13 is $\omega_n^2$; (C) 2 is the decay rate, the real part of the roots. *([02-03](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-03-second-order-linear-odes.md))*

**2. Answer: 63.6°.** $\mathbf a\cdot\mathbf b = 2 - 2 + 4 = 4$ and both vectors have length 3, so $\cos\theta = 4/9$ and $\theta = 63.6°$. *([02-06](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-06-vectors-matrices-and-linear-systems.md))*

**3. Answer: (C) 0.736.** Product rule: $f'(x) = 3x^2e^{-x} - x^3e^{-x} = x^2(3 - x)e^{-x}$, so $f'(1) = 2e^{-1} = 0.7358$. **Wrong options:** (A) 1.10 differentiates only the $x^3$ factor ($3x^2e^{-x}$); (B) −0.368 differentiates only the exponential ($-x^3e^{-x}$); (D) 0.368 is $f(1)$, not $f'(1)$. *([01-03](../../courses/01-calculus-for-engineers/chapters/01-03-derivatives.md))*

**4. Answer: (C) 1.180.** $f(0) = 1$, $f'(0) = \tfrac12$, $f''(0) = -\tfrac14$, so $\sqrt{1 + x} \approx 1 + x/2 - x^2/8$. At $x = 0.4$: $1 + 0.2 - 0.02 = 1.180$. The exact value is 1.1832; the error is about the size of the next term, $x^3/16 = 0.004$. **Wrong options:** (A) 1.160 uses $f''(0)\,x^2$ without dividing by $2!$; (B) 1.183 is the exact value $\sqrt{1.4}$, not the approximation; (D) 1.200 stops at first order. *([01-08](../../courses/01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md))*

**5. Answer: (C) 120.** The point is in the second quadrant: $\operatorname{atan2}(\sqrt3, -1) = 180° - 60° = 120°$. **Wrong options:** (A) 240 is the angle of the conjugate, $-1 - j\sqrt3$; (B) 60 drops the sign of the real part; (D) −60 is what $\tan^{-1}(\sqrt3/(-1))$ returns without the quadrant correction. *([02-01](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md))*

**6. Answer: 1.26.** The solution is $y = 2(1 - e^{-4t})$: final value $8/4 = 2$, time constant 0.25. At $t = 0.25$, $y = 2(1 - e^{-1}) = 1.264$. *([02-02](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-02-first-order-linear-odes.md))*

**7. Answer: (D) 5.** The characteristic equation is $\lambda^2 - 7\lambda + 10 = 0$ (trace 7, determinant $12 - 2 = 10$), so $\lambda = 5$ and $2$. **Wrong options:** (A) 7 is the trace, the sum of the eigenvalues; (B) 10 is the determinant, their product; (C) 2 is the smaller eigenvalue. *([02-08](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-08-eigenvalues-and-eigenvectors.md))*

**8. Answer: (A) 1.500.** $x_1 = x_0 - f(x_0)/f'(x_0) = 1 - (-1)/2 = 1.5$. **Wrong options:** (B) 0.500 adds $f/f'$ instead of subtracting it; (C) 1.414 is the root itself, reached only after more steps; (D) 2.000 takes $f'(x_0) = 1$ instead of $2x_0 = 2$. *([02-10](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-10-numerical-methods.md))*

**9. Answer: 3.54.** Magnitudes divide: $\lvert 3 + j4\rvert/\lvert 1 - j\rvert = 5/\sqrt2 = 3.536$. *([02-01](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md))*

**10. Answer: (B) 1.571.** $\sin^2x = \tfrac12(1 - \cos 2x)$, so the integral is $\tfrac12[x - \tfrac12\sin 2x]_0^{\pi} = \pi/2 = 1.571$. **Wrong options:** (A) 2.000 is $\int_0^\pi \sin x\,dx$; (C) 0.785 is $\pi/4$, a slip in the limits; (D) 3.142 forgets the factor of one half in $\sin^2x = \tfrac12(1 - \cos 2x)$. *([01-06](../../courses/01-calculus-for-engineers/chapters/01-06-techniques-of-integration.md))*

**11. Answer: 13.6.** $\partial f/\partial x = 2xy = 4$ and $\partial f/\partial y = x^2 + 6y = 13$ at $(1, 2)$, so $\lvert\nabla f\rvert = \sqrt{16 + 169} = \sqrt{185} = 13.60$. *([01-09](../../courses/01-calculus-for-engineers/chapters/01-09-multivariable-calculus-1.md))*

**12. Answer: 3.** Subtract the first equation from the second: $x - 2y = -3$. Add the first and third: $2x + 3y = 8$. Then $x = 2y - 3$ gives $7y = 14$, so $y = 2$, $x = 1$ and $z = 6 - 1 - 2 = 3$. Check: $1 + 4 - 3 = 2$. *([02-06](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-06-vectors-matrices-and-linear-systems.md))*

## Probability and statistics

**13. Answer: 30.0 FIT.** With zero failures, the bound $\lambda_U$ is the rate at which seeing none has probability 5%: $e^{-\lambda_U T} = 0.05$, so $\lambda_U = \ln 20/T = 2.996/10^8$ per hour $= 29.96$ FIT, the \"rule of three\". Zero observed failures do not mean a zero rate. *([26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md); [25-09](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md))*

**14. Answer: (D) 0.279.** Bayes: $P(D\mid +) = 0.95 \times 0.02/(0.95 \times 0.02 + 0.05 \times 0.98) = 0.019/0.068 = 0.279$. **Wrong options:** (A) 0.019 is the joint probability $P(D \cap +)$; (B) 0.950 confuses $P(+\mid D)$ with $P(D\mid +)$; (C) 0.068 is the probability that a unit is flagged, $P(+)$. *([03-01](../../courses/03-probability-statistics-and-random-variables/chapters/03-01-probability-in-ee-language.md))*

**15. Answer: (C) 0.736.** Binomial: $P(0) = 0.98^{50} = 0.3642$ and $P(1) = 50 \times 0.02 \times 0.98^{49} = 0.3716$, so $P(X \le 1) = 0.7358$. The Poisson approximation with mean $np = 1$ gives $2e^{-1} = 0.7358$ too. **Wrong options:** (A) 0.364 is the probability of no defective part only; (B) 0.264 is the probability of two or more; (D) 0.372 is the probability of exactly one. *([03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md))*

**16. Answer: (A) 0.9545.** ±20 Ω is ±2σ, and $\Phi(2) - \Phi(-2) = 0.9545$. **Wrong options:** (B) 0.4772 counts one side only, $\Phi(2) - 0.5$; (C) 0.6827 is the fraction within ±1σ; (D) 0.9973 is the fraction within ±3σ. *([03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md))*

**17. Answer: 20.6 mV.** With 24 degrees of freedom, $t_{0.025} = 2.064$. The half-width is $t\,s/\sqrt n = 2.064 \times 0.05/5 = 0.02064$ V. (The normal value 1.96 would give 19.6 mV; with $s$ estimated from 25 samples the $t$ value is the right one.) *([03-05](../../courses/03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md))*

## Ethics and professional practice

**18. Answer: 2041.** A US utility patent's term runs 20 years from the earliest non-provisional filing date, not from the grant: 2021 + 20 = 2041. *([26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md))*

**19. Answer: (C) decline it.** Rule II.4.c: engineers shall not solicit or accept financial or other valuable consideration from outside agents in connection with the work for which they are responsible; rule III.5.a adds the case of suppliers whose product is being specified. **Wrong options:** (A) accept it if the vendor's part is the best choice makes the part's merits relevant; they are not; (B) accept it and disclose it after the award treats disclosure as a cure, but the rule forbids acceptance; (D) accept it if it is worth less than \$100 invents a threshold the rule does not have. *([26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md))*

**20. Answer: (B) refuse to seal them.** Rule II.2.b: engineers shall not affix their signatures to any plan or document not prepared under their direction and control. **Wrong options:** (A) seal them after a brief review assumes a quick review puts the work under the engineer's direction and control; it does not; (C) seal them if the preparer is licensed in another state assumes the preparer's licence transfers; it does not; (D) seal them if the client agrees in writing assumes the client can waive the rule; it cannot. *([26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md))*

**21. Answer: (D) the public's safety, health and welfare.** Canon 1: engineers shall hold paramount the safety, health and welfare of the public. If overruled where life or property is endangered, the engineer notifies the employer or client and such other authority as may be appropriate (rule II.1.a). **Wrong options:** (A) the client is the same faithful-agent duty; (B) the employer is the faithful-agent duty, which ranks below the public (canon 4); (C) the reputation of the profession is not the paramount duty. *([26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md))*

## Engineering economics

**22. Answer: 60.0.** Depreciation is $(120 - 20)/5 = 20$ k a year, so the book value after 3 years is $120 - 60 = 60$ k. *([26-04](../../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md))*

**23. Answer: (C) 6806.** $P = F/(1 + i)^n = 10{,}000/1.08^5 = 6805.8$ dollars. **Wrong options:** (A) 7143 discounts at simple interest, $10{,}000/1.40$; (B) 6000 subtracts five years of simple interest; (D) 14693 compounds instead of discounting. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

**24. Answer: (C) 6.14.** $(1 + 0.06/4)^4 - 1 = 1.015^4 - 1 = 6.136\%$. **Wrong options:** (A) 6.00 is the nominal rate itself; (B) 6.18 is continuous compounding, $e^{0.06} - 1$; (D) 1.50 is the quarterly rate. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

**25. Answer: 10.1.** $(A/P, 8\%, 6) = 0.08 \times 1.08^6/(1.08^6 - 1) = 0.21632$ and $(A/F, 8\%, 6) = 0.21632 - 0.08 = 0.13632$. EAC $= 50{,}000 \times 0.21632 - 5{,}000 \times 0.13632 = 10{,}816 - 682 = 10{,}134$ dollars. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

**26. Answer: (B) 10000.** Break-even $= F/(p - v) = 200{,}000/(50 - 30) = 10{,}000$ units. **Wrong options:** (A) 4000 divides by the price, not the contribution margin; (C) 6667 divides by the variable cost; (D) 2500 adds the price and the variable cost. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

## Properties of electrical materials

**27. Answer: (A) 12.2.** $R = R_0[1 + \alpha(T - T_0)] = 10[1 + 0.00393 \times 55] = 12.16$ Ω. **Wrong options:** (B) 2.16 is only the change in resistance; (C) 8.22 divides by $1 + \alpha\Delta T$ instead of multiplying; (D) 12.9 uses 75 °C as the temperature rise instead of 55 °C. *([04-05](../../courses/04-physics-for-ee/chapters/04-05-current-resistance-and-conduction.md))*

**28. Answer: (B) 354.** $C = \varepsilon_r\varepsilon_0A/d = 4 \times 8.854 \times 10^{-12} \times 10^{-4}/10^{-5} = 3.54 \times 10^{-10}$ F. **Wrong options:** (A) 22.1 divides by $\varepsilon_r$ instead of multiplying; (C) 35.4 reads 10 µm as $10^{-4}$ m; (D) 88.5 drops $\varepsilon_r$. *([04-04](../../courses/04-physics-for-ee/chapters/04-04-potential-capacitance-and-dielectrics.md))*

**29. Answer: 2.19 Ω.** $A = \pi(0.5 \times 10^{-3})^2 = 7.854 \times 10^{-7}$ m², so $R = \rho L/A = 1.72 \times 10^{-8} \times 100/7.854 \times 10^{-7} = 2.190$ Ω. (Using the diameter as the radius would give a quarter of this.) *([04-05](../../courses/04-physics-for-ee/chapters/04-05-current-resistance-and-conduction.md))*

**30. Answer: 1.00e4 cm⁻³.** Mass action: $p = n_i^2/N_D = 10^{20}/10^{16} = 1.00 \times 10^4$ cm⁻³, since $n \approx N_D$. *([09-02](../../courses/09-semiconductor-devices/chapters/09-02-carriers-doping-fermi-level.md))*

## Circuit analysis

**31. Answer: 48.2 Ω.** $X_L = 2\pi \times 60 \times 0.1 = 37.70$ Ω, so $\lvert Z\rvert = \sqrt{30^2 + 37.70^2} = 48.18$ Ω. *([07-05](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-05-sinusoidal-steady-state-and-impedance.md))*

**32. Answer: (C) 5.29.** The mean square is $0.25 \times 10^2 + 0.75 \times (-2)^2 = 25 + 3 = 28$ V², so $V_{rms} = \sqrt{28} = 5.29$ V. Squaring makes both levels add, whatever their sign; the average, $2.5 - 1.5 = 1.00$ V, is a different quantity. **Wrong options:** (A) 5.00 ignores the −2 V part; (B) 1.00 is the average value; (D) 4.69 subtracts the −2 V part's mean square instead of adding it. *([07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md); [01-07](../../courses/01-calculus-for-engineers/chapters/01-07-applications-of-integration.md))*

**33. Answer: 4.00 V.** Node 2: $(V_2 - V_1)/2 + V_2/6 = 0$, so $V_1 = \tfrac43V_2$. Node 1: $V_1/4 + (V_1 - V_2)/2 = 2$, which gives $V_2/3 + V_2/6 = 2$ and $V_2 = 4.00$ V ($V_1$ = 5.33 V). *([06-04](../../courses/06-circuit-analysis-1-dc/chapters/06-04-nodal-analysis.md))*

**34. Answer: 1.38 kvar.** $Q = VI\sin\phi = 230 \times 10 \times 0.6 = 1380$ var, since $\sin\phi = \sqrt{1 - 0.8^2} = 0.6$. *([07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md))*

**35. Answer: (A) 0.500.** With $R_L = R_{Th}$ the load sees $V_{Th}/2 = 5$ V, so $P_{max} = V_{Th}^2/(4R_{Th}) = 100/200 = 0.500$ W. **Wrong options:** (B) 0.250 applies the sinusoidal $V_p^2/(2R)$ formula to the 5 V DC load voltage; (C) 2.00 is $V_{Th}^2/R_{Th}$, which ignores the load's share of the voltage; (D) 1.00 is the power the source delivers to $R_{Th}$ and the load together. *([06-09](../../courses/06-circuit-analysis-1-dc/chapters/06-09-maximum-power-transfer.md))*

**36. Answer: (A) 4.** $6 \parallel 3 = 18/9 = 2$ Ω, plus 2 Ω in series gives 4 Ω. **Wrong options:** (B) 2 keeps only the parallel pair; (C) 11 adds all three resistors; (D) 2.73 groups the circuit as 6 Ω in parallel with (3 + 2) Ω. *([06-08](../../courses/06-circuit-analysis-1-dc/chapters/06-08-thevenin-and-norton.md))*

**37. Answer: (B) 6.00.** KCL at node a: $(12 - v_a)/2 = v_a/4 + 0.25v_a$, so $6 = v_a(0.5 + 0.25 + 0.25)$ and $v_a = 6.00$ V. A source drawing $0.25v_a$ behaves like a 4 Ω resistor (1/0.25), so node a sees 4 Ω ∥ 4 Ω = 2 Ω and the divider gives $12 \times 2/(2 + 2) = 6$ V. **Wrong options:** (A) 1.26 treats the 0.25 A/V gain as a 0.25 Ω resistor; (C) 12.0 reverses the dependent source's direction, so it feeds node a; (D) 8.00 leaves out the dependent source. *([06-06](../../courses/06-circuit-analysis-1-dc/chapters/06-06-dependent-sources.md))*

**38. Answer: 1.77 A.** Impedances: $j\omega L = j4$ Ω and $1/(j\omega C) = -j2$ Ω. Mesh 1 (source, 4 Ω, inductor) and mesh 2 (inductor, 2 Ω, capacitor) give $(4 + j4)\mathbf I_1 - j4\mathbf I_2 = 10$ and $-j4\mathbf I_1 + (2 + j2)\mathbf I_2 = 0$. The second gives $\mathbf I_1 = \mathbf I_2(2 + j2)/(j4) = \mathbf I_2(0.5 - j0.5)$; substituting, $\mathbf I_2[(4 + j4)(0.5 - j0.5) - j4] = \mathbf I_2(4 - j4) = 10$, so $\mathbf I_2 = 1.25 + j1.25$ A and $\lvert\mathbf I_2\rvert = 1.77$ A. Check: the two branches in parallel are $j4(2 - j2)/(2 + j2) = 4$ Ω, so $\mathbf I_1 = 10/8 = 1.25$ A. *([07-05](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-05-sinusoidal-steady-state-and-impedance.md); [06-05](../../courses/06-circuit-analysis-1-dc/chapters/06-05-mesh-analysis.md))*

**39. Answer: (C) 83.0.** The capacitor must supply the load's $Q = 230 \times 10 \times 0.6 = 1380$ var: $C = Q/(\omega V^2) = 1380/(2\pi \times 50 \times 230^2) = 83.0$ µF. **Wrong options:** (A) 166 uses $\omega = \pi f$; (B) 69.2 uses 60 Hz; (D) 111 uses the real power, 1840 W, instead of the reactive power. *([07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md))*

**40. Answer: (D) −51.5.** $X_L = 37.70$ Ω and $\angle Z = \tan^{-1}(37.70/30) = 51.5°$. The current is $\mathbf V/Z$, so it lags the voltage by that angle: −51.5°. **Wrong options:** (A) 51.5 is the angle of the impedance, not of the current; (B) −38.5 takes $\tan^{-1}(R/X)$, the complement; (C) −0.899 is the right angle in radians. *([07-05](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-05-sinusoidal-steady-state-and-impedance.md))*

**41. Answer: 4.00 V.** The lower resistor in parallel with the load is 5 kΩ, so the output is $12 \times 5/(10 + 5) = 4.00$ V, not the unloaded 6 V. *([06-03](../../courses/06-circuit-analysis-1-dc/chapters/06-03-kirchhoffs-laws.md))*

## Linear systems

**42. Answer: (D) 0.782.** $e^{-t/\tau} = 0.02$ gives $t = \tau\ln 50 = 3.912 \times 0.2 = 0.782$ s, the exact form of the \"$4\tau$\" rule. **Wrong options:** (A) 1.00 is $5\tau$, the time to settle within 0.7%; (B) 0.200 is the time constant; (C) 0.461 is the 90% time, $\tau\ln 10$. *([15-03](../../courses/15-control-systems/chapters/15-03-time-response.md))*

**43. Answer: 1.55.** Partial fractions: $6/[s(s + 3)] = 2/s - 2/(s + 3)$, so $f(t) = 2(1 - e^{-3t})$ and $f(0.5) = 2(1 - e^{-1.5}) = 1.554$. *([02-05](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-05-laplace-transform-for-odes.md); [11-08](../../courses/11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md))*

**44. Answer: 4.32 V.** $\tau = RC = 1$ ms, so $v = 5(1 - e^{-2}) = 4.323$ V. *([07-02](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md))*

**45. Answer: (D) unstable.** The denominator factors as $(s + 3)(s - 1)$, so there is a pole at $s = +1$ in the right half-plane. A negative coefficient in the denominator is already enough to rule out stability. **Wrong options:** (A) impossible to classify from $H(s)$ is wrong: the poles settle it; (B) stable reads the stability from the positive $s$ coefficient alone; (C) marginally stable would need poles on the imaginary axis; there are none. *([11-08](../../courses/11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md); [15-05](../../courses/15-control-systems/chapters/15-05-stability-routh-hurwitz.md))*

**46. Answer: (B) 86.5.** $\tau = L/R = 0.1$ ms and the final current is $10/100 = 100$ mA, so $i = 100(1 - e^{-0.2/0.1}) = 86.5$ mA. **Wrong options:** (A) 13.5 is the part still to come, $100e^{-2}$; (C) 100 is the final value, reached only after several time constants; (D) 63.2 is the value after one time constant. *([07-02](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md))*

**47. Answer: 20.0 dB.** $\lvert H\rvert = 1000/\lvert 10 + j100\rvert = 1000/100.50 = 9.950$, and $20\log_{10} 9.950 = 19.96$ dB. The Bode asymptote gives the same: 40 dB at DC (gain 100), falling 20 dB/decade from the 10 rad/s corner. *([07-07](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-07-frequency-response-and-bode-plots.md))*

**48. Answer: (D) 20.0.** $Q = \omega_0L/R = (1/R)\sqrt{L/C} = 0.1 \times \sqrt{40{,}000} = 20.0$, with $f_0 = 1/(2\pi\sqrt{LC}) = 15.9$ kHz. The half-power bandwidth is $f_0/Q = 796$ Hz. **Wrong options:** (A) 0.0500 is the reciprocal, $R\sqrt{C/L}$; (B) 3.18 uses $f_0$ in place of $\omega_0$ in $\omega_0L/R$; (C) 200 is $\sqrt{L/C}$, without the $1/R$. *([07-08](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md))*

## Signal processing

**49. Answer: (A) 74.0.** $6.02N + 1.76 = 72.24 + 1.76 = 74.0$ dB. **Wrong options:** (B) 70.5 subtracts the 1.76 dB instead of adding it; (C) 72.2 omits the 1.76 dB sine term ($20\log_{10}2^{12}$); (D) 36.1 uses $10\log_{10}$ on an amplitude ratio. *([20-06](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-06-data-converter-fundamentals.md); [16-10](../../courses/16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md))*

**50. Answer: (D) 1.27.** For an odd square wave, $b_k = \tfrac{2}{T}\int_0^T x(t)\sin(k\omega_0t)\,dt = 4/(k\pi)$ for odd $k$, so $b_1 = 4/\pi = 1.27$ V: the fundamental is larger than the wave itself. **Wrong options:** (A) 1.00 is the square wave's own peak; (B) 0.900 is the fundamental's rms value, $4/(\pi\sqrt2)$; (C) 0.637 is $2/\pi$, the fundamental of a 0-to-1 V square wave. *([11-05](../../courses/11-signals-and-systems/chapters/11-05-fourier-series.md))*

**51. Answer: (C) 8.** The Nyquist rate is $2f_{max} = 8$ kHz. Sampling must be faster than this (and in practice comfortably faster, to leave room for the anti-aliasing filter's transition band). **Wrong options:** (A) 4 is the bandwidth itself; (B) 2 halves the bandwidth instead of doubling it; (D) 50.3 is $2f_{max}$ converted to krad/s. *([11-10](../../courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md))*

**52. Answer: (C) 43.1.** $f_s/N = 44{,}100/1024 = 43.07$ Hz. **Wrong options:** (A) 86.1 divides by $N/2$; (B) 44.1 divides by 1000 instead of 1024; (D) 21.5 divides by $2N$. *([16-03](../../courses/16-digital-signal-processing/chapters/16-03-the-dft.md))*

**53. Answer: 0.125.** $h[n] = 0.5^n u[n]$, so $h[3] = 0.125$. Equivalently, run $y[n] = x[n] + 0.5y[n-1]$ with an impulse: 1, 0.5, 0.25, 0.125. *([11-09](../../courses/11-signals-and-systems/chapters/11-09-z-transform.md))*

**54. Answer: 3.00 kHz.** A tone at $f$ sampled at $f_s$ appears at $\lvert f - kf_s\rvert$ folded into $[0, f_s/2]$: $\lvert 7 - 10\rvert = 3$ kHz. *([11-10](../../courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md))*

**55. Answer: 3.** $y[2] = x[0]h[2] + x[1]h[1] + x[2]h[0] = 2 - 2 + 3 = 3$; the whole output is $\{1, 1, 3, 1, 6\}$. Forgetting to reverse $h$ gives $1 - 2 + 6 = 5$. *([11-03](../../courses/11-signals-and-systems/chapters/11-03-convolution.md))*

## Electronics

**56. Answer: (B) 0.640.** $I_D = \tfrac12 \times 2 \times (1.3 - 0.5)^2 = 0.640$ mA. **Wrong options:** (A) 0.800 does not square the overdrive; (C) 1.69 uses $V_{GS}$ in place of the overdrive; (D) 1.28 omits the one half. *([10-02](../../courses/10-electronics-1/chapters/10-02-mosfet-dc-operation-and-biasing.md))*

**57. Answer: −8.00.** $I_D = 0.640$ mA, so $V_{DS} = 5 - 0.640 \times 5 = 1.80$ V, above $V_{ov} = 0.8$ V: the transistor is in saturation. $g_m = k'(W/L)V_{ov} = 1.6$ mA/V, and $A_v = -g_mR_D = -1.6 \times 5 = -8.00$. *([10-04](../../courses/10-electronics-1/chapters/10-04-small-signal-models.md); [10-06](../../courses/10-electronics-1/chapters/10-06-mos-single-stage-amplifiers.md))*

**58. Answer: (C) 80.** $20\log_{10}(1000/0.1) = 20\log_{10}10^4 = 80$ dB. **Wrong options:** (A) 60 is the differential gain alone in dB; (B) 40 uses $10\log_{10}$ on a voltage-gain ratio; (D) −80 inverts the ratio. *([12-01](../../courses/12-electronics-2/chapters/12-01-differential-pairs.md))*

**59. Answer: (A) 0.833.** The capacitor discharges for nearly half a cycle at 60 Hz: $\Delta V \approx I/(2fC) = 0.1/(120 \times 10^{-3}) = 0.833$ V, the standard estimate. It is about 12% high here: with 12 V peaks and 0.8 V of droop, the diodes start conducting about 20° before each peak, so the capacitor discharges for less than a full half-cycle, and a simulation gives 0.74 V. **Wrong options:** (B) 0.133 uses $\omega$ in place of $f$; (C) 1.67 uses the half-wave formula, $I/(fC)$; (D) 0.241 is the rms value of the sawtooth ripple. *([10-01](../../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md))*

**60. Answer: 4.30 mA.** $I = (5 - 0.7)/1000 = 4.30$ mA. *([10-01](../../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md))*

**61. Answer: 5.70 V.** $I_B = (5 - 0.7)/100\text{ k} = 43$ µA, $I_C = \beta I_B = 4.3$ mA, and $V_{CE} = 10 - 4.3 = 5.70$ V. It is above saturation, so the transistor is in the active region and the assumption holds. *([10-03](../../courses/10-electronics-1/chapters/10-03-bjt-dc-operation-and-biasing.md))*

**62. Answer: 500 kHz.** Bandwidth = GBW ÷ noise gain = 10 MHz ÷ 20 = 500 kHz. *([10-09](../../courses/10-electronics-1/chapters/10-09-real-op-amps-nonidealities.md))*

**63. Answer: (D) 1.25.** $\Delta R = GF \cdot \varepsilon \cdot R = 2.0 \times 500 \times 10^{-6} \times 120 = 0.12$ Ω. The output is the difference of the two dividers: $5(120.12/240.12 - 120/240) = 1.249$ mV, close to the linearized $V\,GF\,\varepsilon/4 = 1.25$ mV. **Wrong options:** (A) 5.00 is the output of a full bridge, with four active arms; (B) 2.50 is the output of a half bridge, with two active arms; (C) 0.625 omits the gauge factor. *([06-03](../../courses/06-circuit-analysis-1-dc/chapters/06-03-kirchhoffs-laws.md))*

**64. Answer: (A) 9.58.** The resistor carries $(12 - 5.1)/470 = 14.68$ mA and the load takes $5.1/1000 = 5.10$ mA, so the Zener takes 9.58 mA. **Wrong options:** (B) 19.8 adds the load current instead of subtracting it; (C) 5.10 is the load current; (D) 14.7 forgets the load. *([10-01](../../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md))*

## Power systems

**65. Answer: 23.0 kW.** Phase voltage $480/\sqrt3 = 277.1$ V, so each phase takes $277.1^2/10 = 7680$ W and the total is 23.0 kW (equivalently $V_L^2/R$). *([07-11](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-11-three-phase-circuits.md))*

**66. Answer: (D) 190.** $Z_{base} = V_{base,LL}^2/S_{base,3\phi} = 138^2/100 = 190.4$ Ω. **Wrong options:** (A) 63.5 uses the line-to-neutral voltage with the three-phase base; (B) 0.00525 inverts the formula; (C) 1.38 divides the voltage by the power. *([22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md))*

**67. Answer: (B) 227.** $I = P/(\sqrt3 V_L \text{pf}) = 10^7/(\sqrt3 \times 33{,}000 \times 0.9) = 194.4$ A, and the loss is $3I^2R = 3 \times 194.4^2 \times 2 = 227$ kW. **Wrong options:** (A) 680 omits the $\sqrt3$ in the line current; (C) 75.6 counts one phase; (D) 184 ignores the power factor. *([22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md))*

**68. Answer: 208 A.** $I_2 = S/V_2 = 50{,}000/240 = 208.3$ A (the primary carries $50{,}000/7200 = 6.94$ A). *([07-09](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-09-mutual-inductance-and-transformers.md))*

**69. Answer: (D) 27.7.** $I_L = I_\phi = (480/\sqrt3)/10 = 27.7$ A. **Wrong options:** (A) 16.0 divides by $\sqrt3$ twice; (B) 48.0 puts the line voltage across a phase; (C) 83.1 is the line current of a delta connection, $\sqrt3 \times 48.0$. *([07-11](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-11-three-phase-circuits.md))*

**70. Answer: (B) 1000.** $n_s = 120f/P = 120 \times 50/6 = 1000$ rpm ($P$ is the number of poles). **Wrong options:** (A) 960 is a typical full-load speed of such a motor, with 4% slip; (C) 500 uses $60f/P$ with $P$ counted in poles; (D) 2000 uses $120f/P$ with $P$ counted in pole pairs. *([22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md))*

**71. Answer: 3.00%.** $n_s = 120f/P = 1800$ rpm, so $s = (1800 - 1746)/1800 = 3.00\%$. *([22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md))*

**72. Answer: (D) 0.958.** The load's reactive power is $40\tan(\cos^{-1}0.8) = 30$ kvar. With 18 kvar supplied locally, 12 kvar remains: $S = \sqrt{40^2 + 12^2} = 41.8$ kVA and pf $= 40/41.8 = 0.958$. **Wrong options:** (A) 0.912 takes the capacitors' 18 kvar as the remaining reactive power; (B) 0.640 adds the capacitors' kvar instead of subtracting it; (C) 0.800 is the original power factor, as if the capacitors changed nothing. *([07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md))*

**73. Answer: (D) 0.275.** Volt-second balance on the inductor: $(V_{in} - V_{out})DT = V_{out}(1 - D)T$, so $D = V_{out}/V_{in} = 3.3/12 = 0.275$. **Wrong options:** (A) 3.64 is $V_{in}/V_{out}$; (B) 0.216 uses the buck-boost relation $V_{out}/V_{in} = D/(1 - D)$; (C) 0.725 is $1 - D$, the off-time fraction. *([22-02](../../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md))*

## Electromagnetics

**74. Answer: (B) 0.200.** The wave travels at $c/\sqrt{\varepsilon_r} = 2 \times 10^8$ m/s, so $\lambda = c/(f\sqrt{\varepsilon_r}) = 0.3/1.5 = 0.200$ m. **Wrong options:** (A) 0.133 divides by $\varepsilon_r$, not its square root; (C) 0.450 multiplies by $\sqrt{\varepsilon_r}$; (D) 0.300 is the free-space wavelength. *([13-05](../../courses/13-electromagnetics/chapters/13-05-plane-waves.md); [13-08](../../courses/13-electromagnetics/chapters/13-08-transmission-lines-sinusoidal-steady-state.md))*

**75. Answer: 40.0 µT.** $B = \mu_0I/(2\pi r) = 4\pi \times 10^{-7} \times 10/(2\pi \times 0.05) = 4.00 \times 10^{-5}$ T. *([04-06](../../courses/04-physics-for-ee/chapters/04-06-magnetic-fields-and-forces.md))*

**76. Answer: 2.00.** $\Gamma = (25 - 50)/(25 + 50) = -1/3$, so VSWR $= (1 + \lvert\Gamma\rvert)/(1 - \lvert\Gamma\rvert) = 2.00$. For a real load, VSWR is the larger of $Z_L/Z_0$ and $Z_0/Z_L$, never below 1; $Z_L/Z_0 = 0.5$ is not a VSWR. *([13-08](../../courses/13-electromagnetics/chapters/13-08-transmission-lines-sinusoidal-steady-state.md))*

**77. Answer: (A) 25.0.** A quarter-wave line inverts the load: $Z_{in} = Z_0^2/Z_L = 2500/100 = 25.0$ Ω. **Wrong options:** (B) 100 is the load itself, which a half-wave section would show; (C) 50.0 is the characteristic impedance, as for a matched line; (D) 200 is $Z_L^2/Z_0$. *([13-08](../../courses/13-electromagnetics/chapters/13-08-transmission-lines-sinusoidal-steady-state.md); [13-09](../../courses/13-electromagnetics/chapters/13-09-smith-chart-and-matching.md))*

## Control systems

**78. Answer: (B) 0.500.** The poles have negative real parts, so the final-value theorem applies: $\lim_{s\to0} s\,G(s)/s = G(0) = 5/10 = 0.500$. **Wrong options:** (A) 1.67 divides by the $s$ coefficient instead of the constant term; (C) 0.00 applies the final-value theorem to $G(s)$ instead of $G(s)/s$; (D) 5.00 takes the numerator alone. *([15-03](../../courses/15-control-systems/chapters/15-03-time-response.md))*

**79. Answer: (A) 0.200.** Type 1: $K_v = \lim_{s\to0} sG(s) = 20/4 = 5$, so $e_{ss} = 1/K_v = 0.200$. **Wrong options:** (B) 5.00 is the velocity constant $K_v$ itself; (C) 0.00 is the error to a step, not a ramp; (D) 0.0500 uses the numerator 20 as $K_v$, forgetting the pole at $-4$. *([15-04](../../courses/15-control-systems/chapters/15-04-feedback-and-steady-state-error.md))*

**80. Answer: 6.** Routh array: $s^3$: 1, 3; $s^2$: 2, $K$; $s^1$: $(6 - K)/2$; $s^0$: $K$. Every first-column entry is positive for $0 < K < 6$. At $K = 6$ the auxiliary polynomial $2s^2 + 6$ gives roots at $\pm j\sqrt3$. *([15-05](../../courses/15-control-systems/chapters/15-05-stability-routh-hurwitz.md))*

**81. Answer: (C) 45.** PM $= 180° + \angle L(j\omega_c) = 180 - 135 = 45°$. **Wrong options:** (A) 225 adds 360° to the phase; (B) 135 reports the size of the phase itself; (D) −45 computes $-180° - \angle L$. *([15-07](../../courses/15-control-systems/chapters/15-07-frequency-domain-design.md))*

**82. Answer: (D) 0.625.** $T(s) = G/(1 + GH)$ with $G(s) = 5/(s + 2)$ and $H = 1.2$. At DC, $G(0) = 2.5$ and $T(0) = 2.5/(1 + 3) = 0.625$. **Wrong options:** (A) 0.750 puts the loop gain $GH$ in the numerator; (B) 0.714 ignores the sensor gain (unity feedback); (C) 2.50 is the open-loop forward DC gain. *([15-02](../../courses/15-control-systems/chapters/15-02-transfer-functions-and-block-diagrams.md))*

**83. Answer: 16.3%.** $M_p = e^{-\pi\zeta/\sqrt{1 - \zeta^2}} = e^{-1.814} = 0.163$. *([15-03](../../courses/15-control-systems/chapters/15-03-time-response.md))*

**84. Answer: 0.686 s.** $\omega_n = 5$ and $\zeta = 4/(2 \times 5) = 0.4$, so $t_p = \pi/(\omega_n\sqrt{1 - \zeta^2}) = \pi/(5 \times 0.9165) = 0.686$ s. *([15-03](../../courses/15-control-systems/chapters/15-03-time-response.md))*

## Communications

**85. Answer: −77.0 dBm.** $P_r = P_t + G_t + G_r - L = 20 + 10 + 3 - 110 = -77.0$ dBm. *([21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md))*

**86. Answer: 180 kHz.** $B \approx 2(\Delta f + f_m) = 2(75 + 15) = 180$ kHz. *([17-03](../../courses/17-communication-systems/chapters/17-03-analog-modulation.md))*

**87. Answer: 4.00 Mb/s.** $C = B\log_2(1 + \text{SNR}) = 10^6 \times \log_2 16 = 4.00$ Mb/s. *([17-07](../../courses/17-communication-systems/chapters/17-07-information-theory-and-shannon.md))*

**88. Answer: (A) 40.** 16-QAM carries $\log_2 16 = 4$ bits a symbol, so $R_b = 4 \times 10 = 40$ Mb/s. **Wrong options:** (B) 20 uses $\log_2\sqrt{16} = 2$ bits a symbol, the QPSK figure; (C) 2.5 divides by the bits per symbol; (D) 160 multiplies by $M = 16$ instead of $\log_2 M$. *([17-06](../../courses/17-communication-systems/chapters/17-06-bandpass-digital-modulation.md))*

**89. Answer: (C) −114.** $-174 + 10\log_{10}10^6 = -174 + 60 = -114$ dBm (from $kTB = 4.00 \times 10^{-15}$ W). **Wrong options:** (A) −234 subtracts $10\log_{10}B$ instead of adding it; (B) −144 takes the bandwidth in kHz; (D) −174 is the density per hertz, without the bandwidth. *([17-02](../../courses/17-communication-systems/chapters/17-02-noise-and-snr.md))*

## Computer networks

**90. Answer: (C) TCP.** TCP provides acknowledged, ordered, retransmitted delivery. **Wrong options:** (A) UDP is best-effort datagrams; (B) IP is best-effort packet delivery; (D) Ethernet is a link layer. *([17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md))*

**91. Answer: 120 µs.** $1500 \times 8/10^8 = 1.2 \times 10^{-4}$ s. *([17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md))*

**92. Answer: (A) integrity and authenticity of the data.** Recomputing the MAC with the shared key detects any change to the packet (integrity) and shows it came from a key holder (authenticity). HMAC is the common construction. **Wrong options:** (B) non-repudiation would need a digital signature: either key holder could have computed the MAC; (C) protection against denial of service is availability, which a MAC does not provide; (D) confidentiality of the data would need encryption; a MAC leaves the data readable. *([17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md))*

**93. Answer: (A) 62.** A /26 leaves 6 host bits: $2^6 - 2 = 62$ usable (the network and broadcast addresses are reserved). **Wrong options:** (B) 30 is a /27; (C) 126 is a /25; (D) 64 forgets the network and broadcast addresses. *([17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md))*

## Digital systems

**94. Answer: 62.5 kHz.** Each stage divides by 2, so the MSB of a 4-bit counter completes one cycle every 16 clocks: 62.5 kHz. *([08-07](../../courses/08-digital-logic-design/chapters/08-07-registers-counters-shift-registers.md))*

**95. Answer: (B) NAND.** NAND alone makes NOT (tie the inputs), AND and OR, so it is functionally complete; so is NOR. **Wrong options:** (A) OR cannot make NOT; (C) XOR cannot make AND or OR alone; (D) AND cannot make NOT. *([08-02](../../courses/08-digital-logic-design/chapters/08-02-boolean-algebra-and-gates.md))*

**96. Answer: (D) 294.** $f_{max} = 1/(0.12 + 3.1 + 0.18 \text{ ns}) = 1/3.4 \text{ ns} = 294$ MHz. **Wrong options:** (A) 305 omits the clock-to-Q delay; (B) 329 subtracts the setup time instead of adding it; (C) 323 uses the logic delay alone. *([08-10](../../courses/08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md))*

**97. Answer: 14.** Gray code: $g_3 = b_3$, $g_i = b_{i+1} \oplus b_i$, so 1011 becomes 1110, which is 14. *([08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md))*

**98. Answer: (B) −10.** The sign bit is set, so the value is $246 - 256 = -10$ (invert to 00001001 and add 1: 00001010). **Wrong options:** (A) 246 reads it as unsigned; (C) −9 reads it as ones' complement; (D) −118 reads it as sign-magnitude. *([08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md))*

**99. Answer: (A) 4.** States: S0 (no progress), S1 (seen 1), S2 (seen 10), S3 (seen 101, output 1). From S3, a 0 leads to S2 (the last \"10\") and a 1 to S1, which is how overlaps are kept. No two states are equivalent, so four is minimal. **Wrong options:** (B) 3 is the Mealy count; a Moore output needs its own state; (C) 8 keeps one state per 3-bit history, which is not minimal; (D) 2 is the number of flip-flops for 4 states, not the number of states. *([08-08](../../courses/08-digital-logic-design/chapters/08-08-finite-state-machines.md))*

**100. Answer: 0.250 ns.** Slack $= T - t_{cq} - t_{logic} - t_{setup} = 2 - 0.2 - 1.4 - 0.15 = 0.250$ ns. *([08-10](../../courses/08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md))*

**101. Answer: (B) $D$.** The 1s are the odd minterms other than 13 and 15, which are don't-cares. Taking both don't-cares as 1 makes $F$ true for every odd minterm, which is the single literal $D$ (an eight-cell group on the K-map). **Wrong options:** (A) $\bar AD$ misses minterms 9 and 11; (C) $\bar BD$ misses minterms 5 and 7; (D) $\bar AD + \bar BD$ covers every 1 but ignores the don't-cares, so it is not minimal. *([08-03](../../courses/08-digital-logic-design/chapters/08-03-logic-minimization.md))*

## Computer systems

**102. Answer: 3.33.** Amdahl: $1/(0.2 + 0.8/8) = 1/0.3 = 3.33$. *([14-01](../../courses/14-computer-organization-and-architecture/chapters/14-01-performance-power-iron-law.md))*

**103. Answer: (B) 4.00.** AMAT $= t_{hit} + m \times t_{penalty} = 1 + 0.05 \times 60 = 4.00$ ns. **Wrong options:** (A) 3.00 omits the hit time; (C) 61.0 adds the full penalty to every access; (D) 1.05 adds the miss rate but not the penalty. *([14-09](../../courses/14-computer-organization-and-architecture/chapters/14-09-memory-hierarchy-and-caches.md))*

**104. Answer: (C) 1.00.** $t = N \times \text{CPI}/f = 2 \times 10^9 \times 1.5/(3 \times 10^9) = 1.00$ s. **Wrong options:** (A) 0.444 divides by the CPI instead of multiplying; (B) 2.25 inverts the iron law; (D) 0.667 ignores the CPI. *([14-01](../../courses/14-computer-organization-and-architecture/chapters/14-01-performance-power-iron-law.md))*

**105. Answer: 17.** $32\text{ KB}/64\text{ B} = 512$ lines, so 9 index bits; 6 offset bits; the tag is $32 - 9 - 6 = 17$ bits. *([14-09](../../courses/14-computer-organization-and-architecture/chapters/14-09-memory-hierarchy-and-caches.md))*

**106. Answer: (A) 4.81.** Unpipelined: $5 \times 100 = 500$ cycles. Pipelined: the first instruction finishes after 5 cycles and one more finishes each cycle after that, so $5 + 99 = 104$ cycles. The speedup is $500/104 = 4.81$, approaching 5 only for long runs. **Wrong options:** (B) 4.76 counts the fill as 5 extra cycles instead of 4; (C) 5.00 ignores the fill time; (D) 1.04 is the pipelined cycles per instruction, 104/100. *([14-06](../../courses/14-computer-organization-and-architecture/chapters/14-06-pipelining-and-hazards.md))*

## Software engineering

**107. Answer: (D) integration testing.** Integration testing exercises the interfaces between modules. **Wrong options:** (A) unit testing checks modules alone; (B) acceptance testing checks the requirements with the customer; (C) regression testing re-runs existing tests after a change. *([05-09](../../courses/05-programming-for-engineers/chapters/05-09-software-engineering-practices.md))*

**108. Answer: 20.** Each comparison halves the range: $\lceil\log_2(10^6 + 1)\rceil = 20$. *([05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md))*

**109. Answer: 7.** $i$ takes 3, 7, 11, 15, 19, 23, 27; the next value, 31, fails the test: 7 iterations. *([05-01](../../courses/05-programming-for-engineers/chapters/05-01-python-fundamentals.md))*

**110. Answer: (A) hash table.** A hash table computes the key's slot directly, so lookups take $O(1)$ on average. **Wrong options:** (B) sorted array needs $O(\log n)$ with binary search; (C) binary search tree needs $O(\log n)$ when balanced; (D) linked list needs $O(n)$. *([05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md))*

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| FE.001 | damped frequency | 3 | rad/s |
| FE.002 | angle between vectors | 63.6 | ° |
| FE.003 | derivative at 1 | 0.736 | — |
| FE.004 | Taylor value | 1.180 | — |
| FE.005 | angle | 120 | ° |
| FE.006 | y(0.25) | 1.26 | — |
| FE.007 | larger eigenvalue | 5 | — |
| FE.008 | Newton step | 1.500 | — |
| FE.009 | magnitude | 3.54 | — |
| FE.010 | integral | 1.571 | — |
| FE.011 | gradient magnitude | 13.6 | — |
| FE.012 | z | 3 | — |
| FE.013 | upper bound | 30.0 | FIT |
| FE.014 | posterior probability | 0.279 | — |
| FE.015 | probability of at most one defect | 0.736 | — |
| FE.015.P0 | probability of none | 0.3642 | — |
| FE.015.P1 | probability of exactly one | 0.3716 | — |
| FE.016 | fraction within two sigma | 0.9545 | — |
| FE.017 | half-width | 20.6 | mV |
| FE.017.t | t critical value | 2.064 | — |
| FE.018 | expiry year | 2041 | — |
| FE.022 | book value | 60.0 | k dollars |
| FE.023 | present worth | 6806 | dollars |
| FE.024 | effective rate | 6.14 | % |
| FE.025 | equivalent annual cost | 10.1 | k dollars |
| FE.025.AP | capital-recovery factor | 0.21632 | — |
| FE.025.AF | sinking-fund factor | 0.13632 | — |
| FE.026 | break-even volume | 10000 | units |
| FE.027 | hot resistance | 12.2 | Ω |
| FE.028 | capacitance | 354 | pF |
| FE.029 | resistance | 2.19 | Ω |
| FE.030 | hole concentration | 1.00e4 | cm⁻³ |
| FE.031 | impedance magnitude | 48.2 | Ω |
| FE.031.XL | inductive reactance | 37.70 | Ω |
| FE.032 | rms value | 5.29 | V |
| FE.033 | node-2 voltage | 4.00 | V |
| FE.033.V1 | node-1 voltage | 5.33 | V |
| FE.034 | reactive power | 1.38 | kvar |
| FE.035 | maximum power | 0.500 | W |
| FE.036 | Thévenin resistance | 4 | Ω |
| FE.037 | node-a voltage | 6.00 | V |
| FE.038 | branch current amplitude | 1.77 | A |
| FE.038.I1 | source current amplitude | 1.25 | A |
| FE.039 | correction capacitance | 83.0 | µF |
| FE.040 | current phase | -51.5 | ° |
| FE.041 | loaded divider output | 4.00 | V |
| FE.042 | settling time | 0.782 | s |
| FE.043 | f(0.5) | 1.55 | — |
| FE.044 | capacitor voltage | 4.32 | V |
| FE.046 | inductor current | 86.5 | mA |
| FE.047 | magnitude | 20.0 | dB |
| FE.048 | quality factor | 20.0 | — |
| FE.048.f0 | resonant frequency | 15.9 | kHz |
| FE.048.BW | half-power bandwidth | 796 | Hz |
| FE.049 | ideal SNR | 74.0 | dB |
| FE.050 | fundamental amplitude | 1.27 | V |
| FE.051 | Nyquist rate | 8 | kHz |
| FE.052 | bin spacing | 43.1 | Hz |
| FE.053 | impulse-response sample | 0.125 | — |
| FE.054 | alias frequency | 3.00 | kHz |
| FE.055 | convolution sample | 3 | — |
| FE.056 | drain current | 0.640 | mA |
| FE.057 | voltage gain | -8.00 | — |
| FE.057.VDS | drain-source voltage | 1.80 | V |
| FE.057.gm | transconductance | 1.6 | mA/V |
| FE.058 | CMRR | 80 | dB |
| FE.059 | ripple | 0.833 | V |
| FE.059.sim | simulated ripple | 0.74 | V |
| FE.060 | diode current | 4.30 | mA |
| FE.061 | collector-emitter voltage | 5.70 | V |
| FE.062 | closed-loop bandwidth | 500 | kHz |
| FE.063 | bridge output | 1.25 | mV |
| FE.063.dR | gauge resistance change | 0.12 | Ω |
| FE.064 | Zener current | 9.58 | mA |
| FE.065 | total power | 23.0 | kW |
| FE.065.Vph | phase voltage | 277.1 | V |
| FE.066 | base impedance | 190 | Ω |
| FE.067 | line loss | 227 | kW |
| FE.067.I | line current | 194.4 | A |
| FE.068 | secondary current | 208 | A |
| FE.069 | line current | 27.7 | A |
| FE.070 | synchronous speed | 1000 | rpm |
| FE.071 | slip | 3.00 | % |
| FE.072 | power factor | 0.958 | — |
| FE.072.Q | load reactive power | 30 | kvar |
| FE.073 | duty cycle | 0.275 | — |
| FE.074 | wavelength | 0.200 | m |
| FE.075 | flux density | 40.0 | µT |
| FE.076 | VSWR | 2.00 | — |
| FE.076.G | reflection-coefficient magnitude | 0.333 | — |
| FE.077 | input impedance | 25.0 | Ω |
| FE.078 | final value | 0.500 | — |
| FE.079 | ramp error | 0.200 | — |
| FE.080 | maximum gain | 6 | — |
| FE.081 | phase margin | 45 | ° |
| FE.082 | closed-loop DC gain | 0.625 | — |
| FE.083 | percent overshoot | 16.3 | % |
| FE.084 | peak time | 0.686 | s |
| FE.085 | received power | -77.0 | dBm |
| FE.086 | Carson bandwidth | 180 | kHz |
| FE.087 | capacity | 4.00 | Mb/s |
| FE.088 | bit rate | 40 | Mb/s |
| FE.089 | noise power | -114 | dBm |
| FE.091 | transmission time | 120 | µs |
| FE.093 | usable hosts | 62 | — |
| FE.094 | MSB frequency | 62.5 | kHz |
| FE.096 | maximum clock | 294 | MHz |
| FE.097 | Gray-code value | 14 | — |
| FE.098 | two's-complement value | -10 | — |
| FE.099 | state count | 4 | — |
| FE.100 | setup slack | 0.250 | ns |
| FE.102 | speedup | 3.33 | — |
| FE.103 | average access time | 4.00 | ns |
| FE.104 | execution time | 1.00 | s |
| FE.105 | tag bits | 17 | — |
| FE.106 | pipeline speedup | 4.81 | — |
| FE.108 | comparisons | 20 | — |
| FE.109 | iterations | 7 | — |
