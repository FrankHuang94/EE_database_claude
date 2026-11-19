# Term 1 Checkpoint · Solutions

Questions: [README.md](README.md). Every numerical answer, and the letter of every numerical multiple-choice answer, is checked by [verify_term1.py](verify_term1.py). Each explanation names the chapter to revisit.

**Scoring by block:** Mathematics 18, Probability and statistics 10, Physics and materials 12, Software engineering 10. Aim for at least 70% in each (13, 7, 9 and 7 correct).

---

## Block 1 · Mathematics

**1. Answer: (B) 0.368.** Product rule: $f' = 2xe^{-x} - x^2e^{-x} = (2x - x^2)e^{-x}$; at $x = 1$, $f' = e^{-1} = 0.368$. (C) forgets the second term; (D) gets its sign wrong. *([01-03](../../courses/01-calculus-for-engineers/chapters/01-03-derivatives.md))*

**2. Answer: 1.57.** $\sin^2 t = \tfrac12(1 - \cos 2t)$, so the integral is $\tfrac12[t - \tfrac12\sin 2t]_0^\pi = \pi/2 = 1.571$. *([01-06](../../courses/01-calculus-for-engineers/chapters/01-06-techniques-of-integration.md))*

**3. Answer: (B) 0.5.** Both numerator and denominator → 0; L'Hôpital twice gives $\cos x/2 \to 1/2$, or use $1 - \cos x \approx x^2/2$. *([01-02](../../courses/01-calculus-for-engineers/chapters/01-02-limits-and-continuity.md), [01-08](../../courses/01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md))*

**4. Answer: (C) 1.7×10⁻⁴.** The first omitted Taylor term is $x^3/6 = 0.001/6 = 1.67\times10^{-4}$, and the exact error, $e^{0.1} - 1.105 = 1.71\times10^{-4}$, agrees. *([01-08](../../courses/01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md))*

**5. Answer: 0.500 W.** $P = V^2R_L/(R_s + R_L)^2$ is largest at $R_L = R_s$ (set $dP/dR_L = 0$), giving $P_{\max} = V^2/(4R_s) = 100/200 = 0.500$ W. *([01-04](../../courses/01-calculus-for-engineers/chapters/01-04-applications-of-derivatives.md))*

**6. Answer: (B) 5.66.** $\nabla f = (2xy,\ x^2 + 3) = (4, 4)$ at $(1, 2)$; $|\nabla f| = 4\sqrt2 = 5.66$. *([01-09](../../courses/01-calculus-for-engineers/chapters/01-09-multivariable-calculus-1.md))*

**7. Answer: 0.906 V.** $\tau = RC = 10^4 \times 10^{-5} = 0.1$ s; $v = 5(1 - e^{-0.02/0.1}) = 5(1 - e^{-0.2}) = 0.906$ V. *([02-02](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-02-first-order-linear-odes.md))*

**8. Answer: (B) 0.55.** Compare with $y'' + 2\zeta\omega_ny' + \omega_n^2y = 0$: $\omega_n = \sqrt{13} = 3.606$ rad/s and $\zeta = 4/(2\times3.606) = 0.555$. (The roots are $-2 \pm j3$: underdamped.) *([02-03](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-03-second-order-linear-odes.md))*

**9. Answer: (B) 2.5.** All poles of $sF(s) = 5/(s + 2)$ are in the left half-plane, so the final-value theorem applies: $\lim_{s\to0} sF(s) = 5/2$. *([02-05](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-05-laplace-transform-for-odes.md))*

**10. Answer: 2.59.** Steady state $y_p = 3$; homogeneous $Ce^{-2t}$; $y(0) = 0$ gives $y = 3(1 - e^{-2t})$, so $y(1) = 3(1 - e^{-2}) = 2.594$. *([02-02](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-02-first-order-linear-odes.md))*

**11. Answer: 8.** Expanding along the first row: $2(3\cdot2 - 1\cdot1) - 1(1\cdot2 - 1\cdot0) + 0 = 10 - 2 = 8$. *([02-07](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-07-determinants-inverses-and-vector-spaces.md))*

**12. Answer: (B) 2.** Adding the equations: $3x = 6$, so $x = 2$ (and $y = 1$). *([02-06](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-06-vectors-matrices-and-linear-systems.md))*

**13. Answer: (B) 2 and 5.** $\det(A - \lambda I) = (4 - \lambda)(3 - \lambda) - 2 = \lambda^2 - 7\lambda + 10 = (\lambda - 2)(\lambda - 5)$. Check: the sum equals the trace 7 and the product equals the determinant 10. *([02-08](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-08-eigenvalues-and-eigenvectors.md))*

**14. Answer: 3.** For a 2×2 matrix, $A^{-1} = \frac{1}{ad - bc}\begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$; here $\det A = 3 - 2 = 1$, and the (2, 2) entry is $a/1 = 3$. *([02-07](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-07-determinants-inverses-and-vector-spaces.md))*

**15. Answer: (B) 11.18.** Magnitudes multiply: $|3 + j4|\,|1 - j2| = 5\sqrt5 = 11.18$ (directly: $(3 + j4)(1 - j2) = 11 - j2$). *([02-01](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md))*

**16. Answer: (B) 17.32∠0°.** The imaginary parts cancel and the real parts add: $2 \times 10\cos30^\circ = 17.32$. *([02-01](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md))*

**17. Answer: 2.50 V.** The phasor is $5\angle60^\circ = 5\cos60^\circ + j5\sin60^\circ = 2.5 + j4.33$ V. *([02-01](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md))*

**18. Answer: 3.46.** The roots are $2\angle0^\circ$, $2\angle120^\circ$ and $2\angle240^\circ$, equally spaced on a circle of radius 2. The chord between neighbors is $2r\sin(60^\circ) = 2\sqrt3 = 3.464$. *([02-01](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md))*

## Block 2 · Probability and statistics

**19. Answer: (C) 0.599.** Binomial with $k = 0$: $0.95^{10} = 0.599$. *([03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md))*

**20. Answer: 0.865.** $P(N \ge 1) = 1 - P(N = 0) = 1 - e^{-2} = 0.865$. *([03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md))*

**21. Answer: (C) 0.954.** ±20 Ω is ±2σ; $P(|Z| < 2) = 0.9545$. *([03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md))*

**22. Answer: 0.819.** $R(t) = e^{-t/\text{MTTF}} = e^{-0.2} = 0.819$. *([03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md))*

**23. Answer: (B) 0.33.** Bayes: $P(D\,|\,+) = \dfrac{0.99 \times 0.01}{0.99 \times 0.01 + 0.02 \times 0.99} = \dfrac{0.0099}{0.0297} = 0.333$. Even a good test produces mostly false alarms when the defect is rare. *([03-01](../../courses/03-probability-statistics-and-random-variables/chapters/03-01-probability-in-ee-language.md))*

**24. Answer: 14.1 Ω.** Variances of independent quantities add: $\sigma = \sqrt{10^2 + 10^2} = 14.1$ Ω. *([03-03](../../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md))*

**25. Answer: (C) 1.57.** With σ known, the half-width is $z_{0.975}\,\sigma/\sqrt n = 1.96 \times 4/5 = 1.57$ mV. *([03-05](../../courses/03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md))*

**26. Answer: 0.289 mV.** A uniform error on $[-\Delta/2, \Delta/2]$ has standard deviation $\Delta/\sqrt{12} = 1/3.464 = 0.289$ mV. *([03-03](../../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md))*

**27. Answer: (B) 0.61.** $E[X] = 0.3 + 0.4 = 0.7$; $E[X^2] = 0.3 + 0.8 = 1.1$; $\text{Var}(X) = 1.1 - 0.49 = 0.61$. *([03-03](../../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md))*

**28. Answer: 0.0027.** $P(|Z| > 3) = 2[1 - \Phi(3)] = 0.0027$: about 1 point in 370. *([03-05](../../courses/03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md))*

## Block 3 · Physics and electrical materials

**29. Answer: (B) 0.899 N.** $F = k_eq^2/r^2 = 8.988\times10^9 \times 10^{-12}/0.01 = 0.899$ N (repulsive). *([04-02](../../courses/04-physics-for-ee/chapters/04-02-charge-coulomb-and-electric-fields.md))*

**30. Answer: 354 pF.** $C = \varepsilon_r\varepsilon_0A/d = 4 \times 8.854\times10^{-12} \times 10^{-4}/10^{-5} = 3.54\times10^{-10}$ F. *([04-04](../../courses/04-physics-for-ee/chapters/04-04-potential-capacitance-and-dielectrics.md))*

**31. Answer: (C) 125 µJ.** $W = \tfrac12CV^2 = 0.5 \times 10^{-5} \times 25 = 1.25\times10^{-4}$ J. *([04-04](../../courses/04-physics-for-ee/chapters/04-04-potential-capacitance-and-dielectrics.md))*

**32. Answer: 0.219 Ω.** $A = \pi(0.5\times10^{-3})^2 = 7.854\times10^{-7}$ m²; $R = \rho L/A = 1.72\times10^{-8} \times 10/7.854\times10^{-7} = 0.219$ Ω. *([04-05](../../courses/04-physics-for-ee/chapters/04-05-current-resistance-and-conduction.md))*

**33. Answer: 119.65 Ω.** $R = R_{20}[1 + \alpha(T - 20)] = 100(1 + 0.00393 \times 50) = 119.65$ Ω. *([04-05](../../courses/04-physics-for-ee/chapters/04-05-current-resistance-and-conduction.md))*

**34. Answer: (B) 200 µT.** $B = \mu_0I/(2\pi r) = 4\pi\times10^{-7} \times 10/(2\pi \times 0.01) = 2\times10^{-4}$ T. *([04-06](../../courses/04-physics-for-ee/chapters/04-06-magnetic-fields-and-forces.md))*

**35. Answer: 314 µH.** $L = \mu_0N^2A/\ell = 4\pi\times10^{-7} \times 500^2 \times 10^{-4}/0.1 = 3.14\times10^{-4}$ H. The coil is about nine times as long as it is wide, so the long-solenoid formula is a fair approximation (it overestimates short coils). *([04-07](../../courses/04-physics-for-ee/chapters/04-07-faraday-lenz-and-inductance.md))*

**36. Answer: (C) 25 V.** $|\mathcal E| = N\,\Delta\Phi/\Delta t = 50 \times 0.5\times10^{-3}/10^{-3} = 25$ V. *([04-07](../../courses/04-physics-for-ee/chapters/04-07-faraday-lenz-and-inductance.md))*

**37. Answer: 0.800 eV.** $E = hc/\lambda = 1239.84/1550 = 0.800$ eV. *([04-10](../../courses/04-physics-for-ee/chapters/04-10-intro-quantum-mechanics.md))*

**38. Answer: (C) Ge.** A photon is absorbed band-to-band only if its energy exceeds the band gap. At 0.80 eV, only germanium ($E_g$ = 0.66 eV) qualifies; silicon is transparent at 1550 nm, which is why telecom receivers use Ge or InGaAs. *([04-11](../../courses/04-physics-for-ee/chapters/04-11-intro-solid-state-physics.md))*

**39. Answer: 0.462 Ω·cm.** $\sigma = qN_D\mu_n = 1.602\times10^{-19} \times 10^{16} \times 1350 = 2.16$ S/cm; $\rho = 1/\sigma = 0.462$ Ω·cm. *([04-05](../../courses/04-physics-for-ee/chapters/04-05-current-resistance-and-conduction.md), [04-11](../../courses/04-physics-for-ee/chapters/04-11-intro-solid-state-physics.md))*

**40. Answer: (B) 66 µm.** $\delta = \sqrt{\rho/(\pi f\mu)} = \sqrt{1.72\times10^{-8}/(\pi \times 10^6 \times 4\pi\times10^{-7})} = 66.0$ µm. *([04-07](../../courses/04-physics-for-ee/chapters/04-07-faraday-lenz-and-inductance.md))*

## Block 4 · Software engineering and computing

**41. Answer: (D) 0xD3.** $45 = 0010\,1101$; invert to $1101\,0010$; add 1: $1101\,0011$ = 0xD3 = 211 ($= 256 - 45$). (C) is the inverted pattern without the +1. *([05-07](../../courses/05-programming-for-engineers/chapters/05-07-bit-manipulation.md))*

**42. Answer: 1023.** $0x3FF = 3 \times 256 + 15 \times 16 + 15 = 1023 = 2^{10} - 1$. *([05-07](../../courses/05-programming-for-engineers/chapters/05-07-bit-manipulation.md))*

**43. Answer: (C) O(n²).** The inner loop runs $0 + 1 + \cdots + (n - 1) = n(n-1)/2$ times. *([05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md))*

**44. Answer: 20.** $\lfloor\log_2 10^6\rfloor + 1 = 19 + 1 = 20$. *([05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md))*

**45. Answer: (B).** First-in, first-out order with constant-time operations and no allocation is a queue, and a ring buffer is the standard way to pass data from an interrupt to the main loop. *([05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md))*

**46. Answer: 3.** Python's `//` floors: $-17 // 5 = -4$, and `%` satisfies $a = (a // b)\,b + a \% b$, so $-17 - (-20) = 3$. (C would give −2.) *([05-01](../../courses/05-programming-for-engineers/chapters/05-01-python-fundamentals.md), [05-05](../../courses/05-programming-for-engineers/chapters/05-05-c-fundamentals.md))*

**47. Answer: (A) 6.0.** Left to right: `7 / 2` is integer division, 3; then `3 * 2.0` = 6.0. *([05-05](../../courses/05-programming-for-engineers/chapters/05-05-c-fundamentals.md))*

**48. Answer: 30.** $f(5) = 2(1 + 2 + 3 + 4 + 5) = 30$. *([05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md))*

**49. Answer: (C) merge sort.** Quicksort is $O(n^2)$ in the worst case; heapsort and selection sort are not stable. *([05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md))*

**50. Answer: 5.** Decision points: the first `if`, the `while`, the second `if` and its `and`: 4, so $M = 4 + 1 = 5$. *([05-09](../../courses/05-programming-for-engineers/chapters/05-09-software-engineering-practices.md))*

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T1.01 | derivative at x = 1 | 0.368 | — |
| T1.02 | integral of sin² over [0, π] | 1.57 | — |
| T1.03 | limit | 0.5 | — |
| T1.04 | Taylor error | 1.7×10^-4 | — |
| T1.05 | maximum load power | 0.500 | W |
| T1.06 | gradient magnitude | 5.66 | — |
| T1.07 | capacitor voltage at 20 ms | 0.906 | V |
| T1.08 | damping ratio | 0.55 | — |
| T1.09 | final value | 2.5 | — |
| T1.10 | y(1) | 2.59 | — |
| T1.11 | determinant | 8 | — |
| T1.12 | x | 2 | — |
| T1.13 | larger eigenvalue | 5 | — |
| T1.14 | inverse (2, 2) entry | 3 | — |
| T1.15 | magnitude of the product | 11.18 | — |
| T1.16 | magnitude of the sum | 17.32 | — |
| T1.17 | real part of the phasor | 2.50 | V |
| T1.18 | distance between neighboring roots | 3.46 | — |
| T1.19 | P(no defectives) | 0.599 | — |
| T1.20 | P(at least one failure) | 0.865 | — |
| T1.21 | P(within ±2σ) | 0.954 | — |
| T1.22 | reliability at 2000 h | 0.819 | — |
| T1.23 | P(defective given flagged) | 0.33 | — |
| T1.24 | σ of the series pair | 14.1 | Ω |
| T1.25 | confidence-interval half-width | 1.57 | mV |
| T1.26 | RMS quantization error | 0.289 | mV |
| T1.27 | variance | 0.61 | — |
| T1.28 | P(outside 3σ) | 0.0027 | — |
| T1.29 | force | 0.899 | N |
| T1.30 | capacitance | 354 | pF |
| T1.31 | stored energy | 125 | µJ |
| T1.32 | wire resistance | 0.219 | Ω |
| T1.33 | resistance at 70 °C | 119.65 | Ω |
| T1.34 | flux density | 200 | µT |
| T1.35 | solenoid inductance | 314 | µH |
| T1.36 | induced emf | 25 | V |
| T1.37 | photon energy | 0.800 | eV |
| T1.39 | resistivity | 0.462 | Ω·cm |
| T1.40 | skin depth | 66 | µm |
| T1.41 | −45 as an unsigned byte | 211 | — |
| T1.42 | 0x3FF | 1023 | — |
| T1.44 | binary-search comparisons | 20 | — |
| T1.46 | -17 % 5 in Python | 3 | — |
| T1.47 | 7 / 2 * 2.0 in C | 6.0 | — |
| T1.48 | f(5) | 30 | — |
| T1.50 | cyclomatic complexity | 5 | — |
