# Term 7 Checkpoint · Solutions

Questions: [README.md](README.md). [verify_term7.py](verify_term7.py) checks every numerical answer and the letter of every numeric multiple-choice answer. Where a second route exists it recomputes the value that way:

- explicit cash-flow sums for every interest factor, root-finding for the IRR, and an amortization schedule for the capital-recovery cost;
- Monte Carlo sampling of PERT (beta) task durations as a check on the normal approximation, and a simulated tape-out sequence for the respin delay;
- sampled error sums for the RSS budget, binomial probabilities for review escapes, and the exact fleet probability against its exponential approximation;
- an exact search over team sizes for the flat-team optimum;
- bit counting for the CAN frame and a step-by-step ring simulation for the all-reduce;
- a counted population of targets for the flag's likelihood ratio, scipy's Beta distribution for the track record, and a finite-difference elasticity.

The two conceptual questions (22 and 24) are checked against the answer letters recorded in the script. Each explanation names the chapter to revisit.

**Scoring by block:** engineering economics 12, requirements, reviews, schedule and teams 8, ethics 6, system architectures 12, technical diligence 12. Aim for at least 70% in each: 9 of 12, 6 of 8 and 5 of 6.

---

## Block 1 · Engineering economics

**1. Answer: 15.9.** $F = P(1 + i)^n = 10{,}000 \times 1.06^8 = 15{,}938$ dollars. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

**2. Answer: (C) 336.** $(P/A, 8\%, 10) = [1 - 1.08^{-10}]/0.08 = 6.710$, so $P = 50{,}000 \times 6.710 = 335{,}504$ dollars. (A) discounts the whole \$500k from year 10; (B) ignores discounting; (D) treats the payments as arriving at the start of each year. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

**3. Answer: 495.** $(A/P, 10\%, 5) = 0.1 \times 1.1^5/(1.1^5 - 1) = 0.26380$ and $(A/F) = (A/P) - i = 0.16380$. CR $= 2000 \times 0.26380 - 200 \times 0.16380 = 527.6 - 32.8$, in \$k. The salvage value returns at the end, so it reduces the annual cost by its sinking-fund equivalent, not by $200/5$. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

**4. Answer: (D) 12.7%.** $i_{eff} = (1 + 0.12/12)^{12} - 1 = 1.01^{12} - 1 = 12.68\%$. (A) is the nominal rate; (B) compounds quarterly; (C) is the monthly rate. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

**5. Answer: 14.1.** $(P/A, 12\%, 5) = 3.6048$, so NPV $= -40 + 15 \times 3.6048 = -40 + 54.07$, in \$M. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

**6. Answer: (A) 13.1%.** Set NPV to zero: $100 = 60x + 60x^2$ with $x = 1/(1 + r)$. The positive root is $x = [-60 + \sqrt{60^2 + 4 \times 60 \times 100}]/120 = 0.8844$, so $r = 1/x - 1 = 13.07\%$. (B) is the undiscounted gain over the investment, $120/100 - 1$; (C) and (D) are not roots. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

**7. Answer: 4.00.** $V^* = \text{NRE}/(\text{ASP} - \text{COGS}) = 60/(25 - 10)$, in millions of units. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

**8. Answer: (D) 125.** $D = (P - S)/n = (5 - 1)/8 = \$0.5\text{M}$ a year, and the tax shield is $tD = 0.25 \times 0.5$. (A) ignores the salvage value; (B) is the depreciation itself; (C) is $D(1 - t)$. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

**9. Answer: 51.7.** $C_{good} = [(20 + 5)/0.98 + 2]/0.95 = (25.51 + 2)/0.95 = 28.96$ dollars, so GM $= 1 - 28.96/60$. Yields divide everything spent before the step that loses parts: a part failing final test wastes its die, package, assembly and test. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

**10. Answer: (D) 12.0.** $\text{PV}_L = F + rU$ and $\text{PV}_B = N_B + p_sC_s = 8 + 0.2 \times 5 = 9$, in \$M. Equal when $U^* = (9 - 3)/0.5$ million discounted units. (A) ignores the respin risk; (B) ignores the license fee; (C) ignores both. *([26-04](../../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md))*

**11. Answer: 8.00.** A perpetuity $A$ is worth $A/i$ today: $0.4/0.08 = 5$, plus the \$3M first cost, in \$M. *([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md))*

**12. Answer: (B) 4.38.** $E = P\,\text{PUE}\,h\,c_e = 1\ \text{kW} \times 1.25 \times (4 \times 8760\ \text{h}) \times \$0.10/\text{kWh} = \$4{,}380$. (A) leaves out the PUE; (C) is one year; (D) applies the PUE twice. *([26-04](../../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md))*

## Block 2 · Requirements, reviews, schedule and teams

**13. Answer: 294.** $\bar I = 0.99 \times 5 + 0.01 \times 2000 = 24.95$ µA; $t = uQ/\bar I = 0.8 \times 220\ \text{mAh}/0.02495\ \text{mA} = 7054$ h, divided by 24 h. The 1% awake time draws 80% of the charge, so the wake budget, not the sleep current, sets the life. *([26-01](../../courses/26-engineering-design-and-professional-practice/chapters/26-01-requirements-and-specifications.md))*

**14. Answer: (B) 13.0 mV.** Independent errors add in variance: $\sqrt{3^2 + 4^2 + 12^2} = \sqrt{169}$. (A) is the worst-case sum; (C) is that sum divided by $\sqrt3$; (D) is the variance, in mV². *([26-01](../../courses/26-engineering-design-and-professional-practice/chapters/26-01-requirements-and-specifications.md))*

**15. Answer: 6.48.** $N(1 - p)^k = 50 \times 0.6^4$. Each extra reviewer removes 40% of what is left, so returns diminish, and correlated reviewers (the same blind spots) do worse than this. *([26-02](../../courses/26-engineering-design-and-professional-practice/chapters/26-02-design-reviews-and-standards.md))*

**16. Answer: (D) 85.1%.** Each task has mean $(4 + 24 + 14)/6 = 7$ weeks and standard deviation $10/6 = 1.667$; the path has mean 21 and standard deviation $1.667\sqrt3 = 2.887$. $P = \Phi(3/2.887) = \Phi(1.039)$. (A) adds standard deviations instead of variances; (B) uses one task's standard deviation; (C) plans from the most likely durations (18 weeks). *([26-05](../../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md))*

**17. Answer: 3.50.** $E[N] = 1 + (1 - q_1)\,\big[1 + (1 - q_2) + (1 - q_2)^2 + \cdots\big] = 1 + 0.7/0.8 = 1.875$ tape-outs, and the delay is $(E[N] - 1)t_r = 0.875 \times 4$ months. *([26-05](../../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md))*

**18. Answer: (A) 190.** $n(n - 1)/2 = 20 \times 19/2$. (B) counts each pair twice; (C) counts people; (D) is $n(n + 1)/2$. *([26-06](../../courses/26-engineering-design-and-professional-practice/chapters/26-06-team-structures-and-sizing.md))*

**19. Answer: 6.76.** $O(n) = n[1 - c(n - 1)]$ peaks at $n^* = (1 + 1/c)/2 = 13$, where $O = 13 \times (1 - 0.04 \times 12) = 13 \times 0.52$. Past 13 people a flat team produces less; past 26 it produces nothing. *([26-06](../../courses/26-engineering-design-and-professional-practice/chapters/26-06-team-structures-and-sizing.md))*

**20. Answer: (C) 0.30.** The expected loss falls by $(0.30 - 0.15) \times 10 = 1.5$, against a cost of 1.2. (A) assumes the risk disappears; (B) is the cost; (D) is the gross saving. *([26-05](../../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md))*

## Block 3 · Ethics, safety and intellectual property

**21. Answer: 63.2.** $1 - (1 - 2 \times 10^{-7})^{5 \times 10^6} \approx 1 - e^{-1}$. A risk that is negligible per unit is likely across a fleet; canon 1 is about the public, which is the fleet. *([26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md))*

**22. Answer: (B).** NSPE canon 1, "Hold paramount the safety, health, and welfare of the public", ranks above canon 4 (faithful agent), and the rules of practice require an engineer overruled where life or property is endangered to notify the employer "and such other authority as may be appropriate". (A) puts canon 4 above canon 1; (C) leaves the hazard in place; (D) skips the employer and the proper authority and may breach confidentiality. *([26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md))*

**23. Answer: 9.99.** $\lambda_U = -\ln 0.05/(3 \times 10^8\ \text{h}) = 2.996/(3 \times 10^8)$ per hour, times $10^9$. The "rule of three": zero failures in $T$ bound the rate below about $3/T$ at 95%. *([26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md))*

**24. Answer: (A).** Confidential information with economic value from not being generally known, which its owner takes reasonable measures to keep secret, is a trade secret. Taking it breaches canon 4 and may be unlawful. Copyright protects expression such as code; patents protect published inventions; mask works protect chip layouts. *([26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md))*

**25. Answer: 2031.** Protection starts at the earlier of registration and first commercial exploitation (2021), lasts ten years, and runs to the end of the calendar year: 31 December 2031. Registration in 2022 is within the two-year window, so protection does not lapse. *([26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md))*

**26. Answer: (C) 8000.** Dense TOPS already counts a multiply-accumulate as two operations ($2 \times$ MacTOPS), so TPP $= 1000 \times 8$. That is above 4800, the 3A090.a.1 threshold in the 2023 rule text. (A) halves it; (B) doubles it again; (D) forgets the bit length. *([26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md))*

## Block 4 · System architectures

**27. Answer: 2.37.** $P_{batt} = \sum_k P_k/\eta_k = 1.2/0.9 + 0.5/0.85 + 0.3/(1.2/1.8) = 1.333 + 0.588 + 0.450$, in W. An LDO's efficiency is at most $V_{out}/V_{in}$. *([27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md))*

**28. Answer: (B) 3.00 W.** $P_{sus} = (T_{s,max} - T_a)/\theta_{sa} = 18/6$. (A) and (C) divide a temperature, not a rise; (D) multiplies. *([27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md))*

**29. Answer: 68.3.** $\beta = Rw/8 = 8533 \times 10^6 \times 64/8$ bytes per second. *([27-02](../../courses/27-system-architectures/chapters/27-02-smartphone-soc.md))*

**30. Answer: (D) 17.1.** The weights are $8 \times 10^9 \times 0.5$ bytes = 4 GB, so the rate is $68.3/4$ tokens/s. (A) uses one byte per parameter; (B) a quarter byte; (C) bits instead of bytes. *([27-05](../../courses/27-system-architectures/chapters/27-05-pc-soc.md))*

**31. Answer: 8.23.** $E_b = 0.3 \times 3.85 = 1.155$ Wh; $E_{day} = 0.040 + 0.048 + 0.005 + 0.0144 = 0.1074$ Wh; life $= u\eta E_b/E_{day} = 0.9 \times 0.85 \times 1.155/0.1074$ days. The always-on sensors use more than the display. *([27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md))*

**32. Answer: (C) 16.1 dB.** $\lvert R\rvert = 2\sin(\pi \times 500 \times 50 \times 10^{-6}) = 0.157$, and $-20\log_{10}0.157$. (A) uses $10\log_{10}$; (B) drops the factor 2; (D) is a guess. The same delay gives no attenuation at $1/(6\tau)$ = 3.3 kHz, which is why ANC works only at low frequencies. *([27-04](../../courses/27-system-architectures/chapters/27-04-wearables-earbuds-and-glasses.md))*

**33. Answer: 270.** $34 + 64 + 13 + \lfloor 97/4\rfloor = 111 + 24 = 135$ bits at 2 µs each. *([27-06](../../courses/27-system-architectures/chapters/27-06-automotive-ee-architecture.md))*

**34. Answer: (B) 67.3 m.** $d = vt + v^2/(2a) = 30 \times 0.1 + 900/14 = 3 + 64.3$. (A) ignores the latency; (C) drops the 2; (D) doubles the latency. Every 10 ms of compute latency costs 0.3 m at this speed. *([27-06](../../courses/27-system-architectures/chapters/27-06-automotive-ee-architecture.md))*

**35. Answer: 109.** $P_{in} = (8 \times (8 \times 1.0 + 2) + 6)/0.95 = 86/0.95 = 90.5$ kW at the rack, times the PUE of 1.2 at the facility. *([27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md))*

**36. Answer: (D) 5.93 days.** $6ND = 6 \times 7 \times 10^{10} \times 2 \times 10^{12} = 8.4 \times 10^{23}$ FLOPs, divided by $4096 \times 10^{15} \times 0.4 = 1.64 \times 10^{18}$ FLOP/s, gives $5.13 \times 10^5$ s. (A) multiplies by the utilization instead of dividing; (B) uses $2ND$; (C) divides by the utilization twice. *([27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md))*

**37. Answer: 52.5.** $2 \times \tfrac78 \times 12\ \text{GB}/400\ \text{GB/s} = 1.75 \times 0.03$ s. A ring sends each byte across nearly two link traversals, whatever the number of accelerators. *([27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md))*

**38. Answer: (B) 12.7%.** The ratio is $1/C_{out} + 1/k^2 = 1/64 + 1/9$. (A) keeps only the depthwise term and (C) only the pointwise term; (D) is the saving, not the fraction. *([27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md))*

## Block 5 · Technical diligence

**39. Answer: 50.7.** Odds $(0.3/0.7) \times 3 \times 0.4 \times 2 = 1.029$, so $p = 1.029/2.029$. *([28-01](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md))*

**40. Answer: (A) 0.444.** $\text{LR}^- = (1 - s)/(1 - f) = 0.4/0.9$. (B) is $\text{LR}^+ = 0.6/0.1$; (C) is $1 - s$ alone; (D) is $f/(1 - f)$. A flag's absence is weak evidence of health: 40% of troubled targets lack it too. *([28-06](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-06-red-and-green-flags.md))*

**41. Answer: 36.0.** $(\alpha_0 + s)/(n_0 + n) = (1.4 + 4)/(10 + 5)$. Five projects carry only a third of the weight, so an 80% record shrinks most of the way to the base rate. *([28-07](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-07-evaluating-engineering-teams.md))*

**42. Answer: (B) 6.40%.** The ridge is $2 \times 10^{15}/4 \times 10^{12} = 500$ FLOP/byte; decode intensity is $2 \times 16 = 32$; attainable $32 \times 4$ TB/s = 128 TFLOP/s, against 2,000. (A) is batch 8; (C) batch 32; (D) batch 4. *([28-04](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-04-question-banks-digital-ai-memory-interconnect.md))*

**43. Answer: 31.9.** Frequency rises by $1.25/1.1 = 1.136$, which costs $1.136^3 = 1.467$ times the power, so energy per operation at the new point must fall by $1 - 1/1.467$. Against the old product it falls by $1 - 1/1.25 = 20\%$ (same power, 25% more work); the larger figure is the design improvement needed beyond the voltage–frequency line. *([28-04](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-04-question-banks-digital-ai-memory-interconnect.md))*

**44. Answer: (C) 1.40.** $C_{die} \propto Ae^{AD_0}$, so $d\ln C/d\ln A = 1 + AD_0 = 1 + 0.4$. A 10% larger die costs about 14% more, and more once the wafer-edge term is included. *([28-09](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md))*

**45. Answer: 40.0.** Lost gross profit $mRd_m/12 = 0.5 \times 200 \times 3/12 = 25$, plus \$15M of masks, in \$M. Lost *revenue* (\$50M) overstates it: the unsold parts would have cost money to build. *([28-09](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md))*

**46. Answer: (D) 876.** $\lambda Nt = 50 \times 10^{-9} \times 2 \times 10^6 \times 8760$. (A) is the rate per hour; (B) and (C) are off by factors of ten. *([28-09](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md))*

**47. Answer: 769.** $0.15\ \text{kW} \times 1.3 \times 43{,}800\ \text{h} \times \$0.09/\text{kWh}$. *([28-09](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md))*

**48. Answer: (C) 3.77.** $\text{HHI} = 0.16 + 0.0625 + 0.0225 + 0.01 + 0.01 = 0.265$, and $1/0.265$. (A) counts customers; (B) is one over the largest share; (D) is the HHI itself. *([28-06](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-06-red-and-green-flags.md))*

**49. Answer: 110.** Planned $40 \times [1 - 1.1^{-5}]/0.1 = 40 \times 3.791 = 151.6$; late and partial, $\times\,0.8/1.1$, in \$M. A one-year slip and 80% realization together cost 27% of the plan's value. *([28-08](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-08-integration-risk.md))*

**50. Answer: (C) 0.170.** $[4 \times (0.9 - 1)^2 + (0.9 - 0)^2]/5 = (0.04 + 0.81)/5$. (A) is the score for always saying 0.5; (B) the score if all five had come true; (D) the single false claim's term alone. *([28-10](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-10-conversation-scenarios.md))*

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| T7.01 | future value | 15.9 | $k |
| T7.02 | present worth of the annuity | 336 | $k |
| T7.03 | capital-recovery cost | 495 | $k |
| T7.04 | effective annual rate | 12.7 | % |
| T7.05 | net present value | 14.1 | $M |
| T7.06 | internal rate of return | 13.1 | % |
| T7.07 | break-even volume | 4.00 | million units |
| T7.08 | annual tax shield | 125 | $k |
| T7.09 | gross margin | 51.7 | % |
| T7.10 | break-even discounted volume | 12.0 | million units |
| T7.11 | capitalized cost | 8.00 | $M |
| T7.12 | lifetime electricity cost | 4.38 | $k |
| T7.13 | battery life | 294 | days |
| T7.14 | standard deviation of the sum | 13.0 | mV |
| T7.15 | expected escapes | 6.48 | defects |
| T7.16 | on-time probability | 85.1 | % |
| T7.17 | expected respin delay | 3.50 | months |
| T7.18 | communication channels | 190 | — |
| T7.19 | maximum team output | 6.76 | engineer-equivalents |
| T7.20 | net expected saving | 0.30 | $M |
| T7.21 | fleet probability of at least one failure | 63.2 | % |
| T7.23 | 95% upper bound | 9.99 | FIT |
| T7.25 | year protection ends | 2031 | — |
| T7.26 | total processing performance | 8000 | — |
| T7.27 | battery power | 2.37 | W |
| T7.28 | sustained power | 3.00 | W |
| T7.29 | peak bandwidth | 68.3 | GB/s |
| T7.30 | decode rate | 17.1 | tokens/s |
| T7.31 | battery life | 8.23 | days |
| T7.32 | ANC attenuation | 16.1 | dB |
| T7.33 | CAN frame time | 270 | µs |
| T7.34 | stopping distance | 67.3 | m |
| T7.35 | facility power | 109 | kW |
| T7.36 | training time | 5.93 | days |
| T7.37 | all-reduce time | 52.5 | ms |
| T7.38 | separable fraction | 12.7 | % |
| T7.39 | posterior probability | 50.7 | % |
| T7.40 | likelihood ratio, flag absent | 0.444 | — |
| T7.41 | posterior mean | 36.0 | % |
| T7.42 | share of peak | 6.40 | % |
| T7.43 | required reduction | 31.9 | % |
| T7.44 | cost elasticity | 1.40 | — |
| T7.45 | profit impact | 40.0 | $M |
| T7.46 | field failures per year | 876 | failures |
| T7.47 | electricity saving | 769 | $ |
| T7.48 | effective customers | 3.77 | — |
| T7.49 | present value, late and partial | 110 | $M |
| T7.50 | Brier score | 0.170 | — |
| T7.02a | (P/A, 8%, 10) | 6.710 | — |
| T7.03a | (A/P, 10%, 5) | 0.26380 | — |
| T7.03b | (A/F, 10%, 5) | 0.16380 | — |
| T7.05a | (P/A, 12%, 5) | 3.6048 | — |
| T7.06a | root x = 1/(1 + r) | 0.8844 | — |
| T7.09a | cost per good part | 28.96 | $ |
| T7.13a | average current | 24.95 | µA |
| T7.13b | battery life in hours | 7054 | h |
| T7.16a | path standard deviation | 2.887 | weeks |
| T7.16b | z-score | 1.039 | — |
| T7.17a | expected tape-outs | 1.875 | — |
| T7.19a | optimal team size | 13 | engineers |
| T7.31a | daily rail energy | 0.1074 | Wh |
| T7.33a | frame length | 135 | bits |
| T7.35a | rack input power | 90.5 | kW |
| T7.36a | training compute | 8.4e23 | FLOP |
| T7.36b | training time in seconds | 5.13e5 | s |
| T7.39a | posterior odds | 1.029 | — |
| T7.43a | power factor | 1.467 | — |
| T7.48a | HHI | 0.265 | — |
| T7.49a | planned present value | 151.6 | $M |
| T7.49b | value lost to the slip and realization | 27 | % |
| T7.49c | (P/A, 10%, 5) | 3.791 | — |
| T7.01a | future value in dollars | 15938 | $ |
| T7.02b | present worth in dollars | 335504 | $ |
| T7.03c | capital term | 527.6 | $k |
| T7.03d | salvage term | 32.8 | $k |
| T7.05b | present value of the returns | 54.07 | $M |
| T7.06b | internal rate of return, unrounded | 13.07 | % |
| T7.09b | die and package after assembly yield | 25.51 | $ |
| T7.10a | present cost of building | 9 | $M |
| T7.11a | present value of maintenance | 5 | $M |
| T7.13c | share of charge drawn while awake | 80 | % |
| T7.16c | task standard deviation | 1.667 | weeks |
| T7.17b | expected extra tape-outs | 0.875 | — |
| T7.19b | team size with zero output | 26 | engineers |
| T7.19c | effective fraction per engineer at the optimum | 0.52 | — |
| T7.20a | gross expected saving | 1.5 | $M |
| T7.23a | −ln 0.05 | 2.996 | — |
| T7.27a | first rail from the battery | 1.333 | W |
| T7.27b | second rail from the battery | 0.588 | W |
| T7.27c | LDO rail from the battery | 0.450 | W |
| T7.30a | weight bytes | 4 | GB |
| T7.31b | battery energy | 1.155 | Wh |
| T7.32a | frequency of zero attenuation | 3.3 | kHz |
| T7.32b | residual fraction | 0.157 | — |
| T7.33b | stuff bits | 24 | bits |
| T7.34a | distance per 10 ms of latency | 0.3 | m |
| T7.35b | rack load before conversion | 86 | kW |
| T7.36c | cluster throughput | 1.64e18 | FLOP/s |
| T7.42a | ridge | 500 | FLOP/byte |
| T7.42b | decode intensity | 32 | FLOP/byte |
| T7.42c | attainable throughput | 128 | TFLOP/s |
| T7.43b | energy reduction against the old product | 20 | % |
| T7.43c | frequency ratio | 1.136 | — |
| T7.45a | lost revenue | 50 | $M |
| T7.45b | lost gross profit | 25 | $M |
