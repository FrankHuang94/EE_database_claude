# Course 26 · Final Exam Solutions

Exam: [README.md](README.md). Every number below is recomputed by [verify_26_exam.py](../verify/verify_26_exam.py). About half of the values are recomputed by a second route, listed below; the rest re-evaluate the published formula independently of the text:

- Question 1(a): battery life from a simulated day of mode switching; 1(d): the out-of-spec fraction by numerical integration of the normal density;
- Question 2(a): the expected cost by following each defect's journey as a Markov chain;
- Question 3(b): the optimal reviewer count by trying every team size;
- Question 4: the cost stack by lot accounting (money spent over good units out);
- Question 5: interest factors by explicit summation and the IRR by Brent's method;
- Question 6: present values by stepping a balance backward year by year;
- Question 7: the shrunk die area by adding shrunk block areas;
- Question 8: energy by integrating power over the service life in joules;
- Question 9(b): the 90% date by root-finding; 9(c): the tape-out distribution;
- Question 10: mitigation sets by enumeration, and the optimal tape-out time by direct minimization of the expected cost;
- Question 11: the best team size by brute force, the Brooks break-even by a time-stepped work burn-down, the newsvendor base by trying every base;
- Question 12: fleet failures by unit conversion, the beta-factor model by event enumeration, the zero-failure bound from the gamma distribution, and TPP through MacTOPS.

---

## Question 1 (26-01)

**(a)** $\bar I = 0.02 \times 12 + 0.05 \times 4 + 0.93 \times 0.015 = 0.240 + 0.200 + 0.014$ = **0.454** mA. Usable charge $0.8 \times 200 = 160$ mAh, so the life is $160/0.454$ = **352** h = **14.7** days. The sleep current is only 3% of the average: the active and radio modes set the battery life.

**(b)** Worst case: $3(0.5 + 0.3 + 0.4)$ = **3.6**%. RSS: $3\sqrt{0.25 + 0.09 + 0.16} = 3 \times 0.7071$ = **2.12**%.

**(c)** $\sigma_E = \sqrt{0.50 + 2 \times 0.6 \times 0.5 \times 0.3} = \sqrt{0.68}$ = **0.825**%, so 3σ = **2.47**%: positive correlation pushes the RSS toward the worst case.

**(d)** $\sigma_E$ = 0.7071%, so $z = 2/0.7071$ = **2.83** and the fraction outside ±2% is $2\Phi(-2.828) = 2 \times 0.002342$ = **4.68e3** ppm.

## Question 2 (26-01)

**(a)** A missed defect costs, on average, $0.5 \times 10 + 0.5 \times 0.6 \times 100 + 0.5 \times 0.4 \times 1000 = 5 + 30 + 200$ = **235** \$k. Total: $C = 50[0.4 \times 1 + 0.6 \times 235]$ = **7070** \$k, about \$7.1 M; the field term alone is 85% of the downstream cost.

**(b)** $\partial C/\partial p_1 = -N(\bar c_{down} - c_1) = -50 \times 234$ = **−11700** \$k per unit of probability, so +0.01 saves **117** \$k.

**(c)** $w^* = (R_a - R_b)/[(R_a - R_b) - (s_{ac} - s_{bc})] = -1.5/(-1.5 - 4)$ = **0.273**: above about 27% weight on criterion $c$, option $a$ wins.

**(d)** $200 \times 0.08$ = **16** untraced requirements; expected cost $16 \times 0.25 \times 150$ = **600** \$k.

## Question 3 (26-02)

**(a)** $1 - 0.6^3$ = **0.784**.

**(b)** $k \le 1 + \ln[6000/(20000 \times 25 \times 0.4)]/\ln 0.6 = 1 + \ln 0.03/\ln 0.6$ = **7.86**, so **7** reviewers. Check: $C(6)$ = **\$59,328**, $C(7)$ = **\$55,997**, $C(8)$ = **\$56,398**.

**(c)** Lincoln–Petersen $18 \times 15/10$ = **27.0**; Chapman $19 \times 16/11 - 1$ = **26.6**. Found $18 + 15 - 10$ = **23**, so about **4.0** remain.

**(d)** Return $140/180$ = **77.8**% (≥ 75% ✓); approval $98/120$ = **81.7**% (≥ 75% ✓, abstentions excluded); abstention $20/140$ = **14.3**% (< 30% ✓). It passes.

## Question 4 (26-03)

**(a)** DPW $= \pi \times 300^2/480 - \pi \times 300/\sqrt{240}$ = **528.2**, so **528**; $Y = e^{-1.2 \times 0.12}$ = **0.8659**; $C_{die} = 15{,}000/(528 \times 0.8659)$ = **\$32.81**.

**(b)** After assembly $(32.809 + 5.00)/0.985$ = **\$38.38** (carry the unrounded die cost; \$32.81 would give \$38.39); after test $(38.385 + 1.50)/0.97$ = **\$41.12**.

**(c)** GM $= (75 - 41.12)/75$ = **45.2**%; markup $33.88/41.12$ = **82.4**%.

**(d)** $90 \times 10^6/(75 - 41.12)$ = **2.66** million units.

## Question 5 (26-03)

**(a)** $(P/A, 8\%, 6) = (1 - 1.08^{-6})/0.08$ = **4.6229**; $(A/P, 8\%, 6)$ = **0.21632**; payment $250{,}000 \times 0.216315$ = **\$54,079** a year.

**(b)** NPV $= -40 - 40/1.12 + 35[(P/A, 12\%, 5) - (P/A, 12\%, 1)]$ = **$19.2 M**. IRR: NPV(21%) = +$0.426 M and NPV(22%) = −\$1.248 M bracket the root; linear interpolation gives $21 + 0.426/(0.426 + 1.248)$ = 21.25%, and NPV(21.25%) = +\$0.001 M confirms it: IRR = **21.25**%.

**(c)** Cumulative cash: −40, −80, −45, −10 after year 3, then +25 after year 4, so payback = $3 + 10/35$ = **3.29** years.

**(d)** Sales now arrive in years 3–5 only: NPV $= -40 - 40/1.12 + 35(1.12^{-3} + 1.12^{-4} + 1.12^{-5})$ = **−$8.70 M**, a loss of **$27.9 M**. A one-year slip turns a good program into a bad one.

## Question 6 (26-04)

**(a)** $U = 4/1.1 + 6/1.1^2 + 6/1.1^3 + 4/1.1^4$ = **15.835** million units (carried to 5 figures because the PVs below sit near a rounding boundary).

**(b)** Licence $8 + 1.00 \times 15.835$ = **\$23.835 M**; build $30 + 0.2 \times 20$ = **$34.0 M**. License, saving **$10.165 M**.

**(c)** $U^* = (34 - 8)/1.00$ = **26.0** million, **1.64** times the plan.

**(d)** Royalties $1.000, 0.900, 0.810, 0.729$ a unit; PV $= 4.000/1.1 + 5.400/1.1^2 + 4.860/1.1^3 + 2.916/1.1^4$ = **$13.74 M**, equivalent to **$0.868** a unit, so the percentage form is cheaper for the licensee by $15.835 - 13.74$ = **\$2.09 M** in royalties.

## Question 7 (26-04)

**(a)** $s_{eff} = 1/(0.60/1.6 + 0.25/1.15 + 0.15/1.05)$ = **1.360**; new area $150/1.360$ = **110.3** mm².

**(b)** Old: DPW $\pi \times 300^2/600 - \pi \times 300/\sqrt{300}$ = 416.8, so **416**, $Y = e^{-0.15}$ = **0.8607**, cost **\$41.89**. New: DPW $\pi \times 300^2/(4 \times 110.3) - \pi \times 300/\sqrt{2 \times 110.3}$ = 577.5, so **577**, $Y = e^{-1.103 \times 0.12}$ = **0.8760**, cost **$37.59**. Saving **$4.30** (\$4.3046 unrounded).

**(c)** $40/4.3046$ = **9.29** million units.

**(d)** $(19{,}000/15{,}000)/1.360$ = **0.931**: about 7% cheaper per function. It is not $1/1.6$ because only the logic gains 1.6×; SRAM and analog shrink little (the harmonic mean), and the wafer costs 27% more.

## Question 8 (26-04)

**(a)** Energy: merchant $0.9 \times 1.25 \times 8760 \times 4 \times 0.07$ = **\$2,759**; custom $0.6 \times 1.25 \times 8760 \times 4 \times 0.07$ = **\$1,840**. TCO: merchant $25{,}000 + 10{,}000 + 2{,}759$ = **\$37,759**; custom $8{,}000 + 10{,}000 + 1{,}840$ = **\$19,840**.

**(b)** Merchant **\$37,759** per equivalent; custom $19{,}840/0.75$ = **$26,453**; saving **$11,307**.

**(c)** $500 \times 10^6/11{,}307$ = **4.42e4** merchant-equivalents, **5.90e4** custom chips.

**(d)** 150,000 chips are 112,500 equivalents: $P_m^* = 26{,}453 + 500 \times 10^6/112{,}500 - 10{,}000 - 2{,}759$ = **\$18,138**.

## Question 9 (26-05)

**(a)** Path A: means 8.67 and 3.17, $\mu_A$ = **11.83** weeks; $\sigma_A = \sqrt{1.333^2 + 0.5^2}$ = **1.424** weeks. Path B: means 7.33 and 4.33, $\mu_B$ = **11.67**; $\sigma_B = \sqrt{1^2 + 0.667^2}$ = **1.202** weeks.

**(b)** $P(A \le 14) = \Phi(1.522)$ = **0.936**; $P(B \le 14) = \Phi(1.941)$ = **0.974**; both $0.9359 \times 0.9739$ = **0.912** (interpolating the FE Handbook table gives 0.911; accept 0.911–0.912). The 90% date, iterating on $T$ until the product is 0.90: $T$ = 13.8 gives 0.882, 13.9 gives 0.897 and 14.0 gives 0.912, so the date is **13.9** weeks (13.92 by finer iteration).

**(c)** $E[N] = 1 + 0.7 + 0.7 \times 0.2$ = **1.84**; $P(N = 1, 2, 3)$ = **0.30**, **0.56**, **0.14**; expected delay $0.84 \times 16$ = **13.4** weeks.

**(d)** Full: $85 \times 1.3$ = **110.5** days = **15.8** weeks. Metal ECO from wafers held at contact, so only the 28 metal and via layers remain: $28 \times 1.3$ = **36.4** days = **5.20** weeks.

## Question 10 (26-05)

**(a)** EMV $= 5.0 + 3.0 + 4.0$ = **\$12.0 M**. Net benefits: R1 $0.15 \times 25 - 2.0$ = **\$1.75 M**; R2 $0.15 \times 10 - 1.0$ = **\$0.50 M**; R3 $0.07 \times 40 - 1.5$ = **\$1.30 M**. With $3 M, R1 and R3 ($3.5 M) do not fit, so R1 and R2 ($3.0 M, net **$2.25 M**) beat R2 and R3 (\$2.5 M, net \$1.80 M).

**(b)** $k = 1.2 \times 3/30$ = **0.12**; iterating $\lambda = ke^{\lambda}$ from $\lambda$ = $k$: 0.12 → 0.1353 → 0.1374 → 0.1377 → 0.1377, so $\lambda^*$ = **0.138**; $t^* = 3\ln(0.3 \times 30/0.138)$ = **12.5** weeks; $P_r = 1 - e^{-0.138}$ = **0.129**.

**(c)** $f(t^*) = 1.2 \times 12.5 + 30 \times 0.129$ = **\$18.9 M**; at $t$ = 0, $\lambda$ = 9 and **\$30.0 M**.

**(d)** With $\tau$ = 2: $k$ = 0.08, and the same iteration (0.08 → 0.0867 → 0.0872 → 0.0873) gives $\lambda^*$ = 0.0873, so $t^* = 2\ln(9/0.0873)$ = **9.27** weeks, $P_r$ = **0.0836**, $f = 2 + 1.2 \times 9.27 + 30 \times 0.0836$ = **$15.6 M**. Buy it: it saves **$3.27 M** and 3.3 weeks.

## Question 11 (26-06)

**(a)** $O(n) = (1 + c)n - cn^2$, so $O'(n) = 1 + c - 2cn = 0$ gives $n^* = (1 + 1/c)/2$, and $O''(n) = -2c < 0$ makes it a maximum. With $c$ = 0.035, $n^*$ = **14.8**; $O(14)$ = **7.63** and $O(15)$ = **7.65**, so **15** people give **7.65** FTE.

**(b)** Members are productive $1 - 0.035 \times 6$ = **0.79**; a team delivers $7 \times 0.79$ = **5.53**; the cross-team factor is $1 - 0.02 \times 7$ = **0.86**; total $8 \times 5.53 \times 0.86$ = **38.0** FTE, **0.594** per head.

**(c)** Without hires the team delivers $12 \times 0.78$ = 9.36 FTE. With hires, $e$ = 0.66: **5.94** FTE during the ramp (9 engineers working) and **11.88** after. Setting the finishing times equal: $W/9.36 = 2.5 + (W - 14.85)/11.88$ gives $W$ = **55.2** person-months, **5.89** months at the current rate. With less work left, the hires lengthen the project.

**(d)** $C_e/C_c$ = **0.667**. The load exceeds 12 in 6 of 8 quarters (0.75 > 0.667) but exceeds 18 in only 4 (0.50), so the base is **18**: cost $18 \times 8 \times 80{,}000 + 78 \times 120{,}000$ = **$20.9 M**. A base of 12 costs **$21.4 M** and a base of 30 **\$22.8 M**.

## Question 12 (26-07)

**(a)** $1.5 \times 365 \times 15$ = **8.21e3** hours per vehicle; fleet failures $100 \times 10^{-9} \times 5 \times 10^6 \times 8212.5$ = **4.11e3**; per vehicle $1 - e^{-8.21 \times 10^{-4}}$ = **8.21e-4**.

**(b)** $0.03 \times 5 \times 10^{-4} + (0.97 \times 5 \times 10^{-4})^2$ = **1.52e-5**, **60.9** times the independent $2.5 \times 10^{-7}$. Diversity lowers $\beta$: channels that work by different means (different designs, physics or software), not two copies of one design.

**(c)** $2.996/(2 \times 10^8)$ per hour = **15.0** FIT. Showing 10 FIT needs $2.996/10^{-8}$ = **3.00e8** failure-free hours in total, **1.50** times the data so far. A clean field record is weak evidence: zero failures only bound the rate at about $3/T$, so a low rate can be claimed only with very many device-hours (or accelerated testing), and silence may also mean failures went unreported.

**(d)** 220 TFLOPS dense is 110 dense MacTOPS, so TPP $= 2 \times 110 \times 16 = 220 \times 16$ = **3520**; density $3520/520$ = **6.77** per mm². TPP < 4800 rules out 3A090.a.1; TPP ≥ 1600 and density ≥ 5.92 meet **3A090.a.2**. The description "below US export thresholds" would be false: canons 3 (truthful public statements) and 5 (avoid deceptive acts) apply, and canon 6 (lawfully). The engineer should state the calculation in writing to the marketing owner and the trade-compliance team, decline to endorse the claim, and escalate if it is used anyway [R-654, R-659].

---

## Rubric for Question 12

| Part | Points | Award for |
|---|---|---|
| (a) | 3 | 1 each: hours, fleet failures, per-vehicle probability. |
| (b) | 3 | 2: the beta-factor probability. 1: the ratio and the design choice (diversity, not duplication, lowers $\beta$). |
| (c) | 3 | 2: the bound. 1: the total hours as a multiple of the data so far, and why a clean field record is weak evidence. |
| (d) | 1 + 1 + 1 | 1: TPP and density. 1: the criterion met. 1: canons 3 and 5 named, with the action (written statement to the owner and compliance; refuse to endorse). |

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| X26.1a | average current | 0.454 | mA |
| X26.1a1 | life | 352 | h |
| X26.1a2 | life | 14.7 | days |
| X26.1a3 | sleep share of average | 3 | % |
| X26.1b | worst case | 3.6 | % |
| X26.1b1 | RSS 3 sigma | 2.12 | % |
| X26.1c | correlated sigma | 0.825 | % |
| X26.1c1 | correlated 3 sigma | 2.47 | % |
| X26.1d | z | 2.83 | |
| X26.1d1 | out of spec | 4.68e3 | ppm |
| X26.2a | downstream cost | 235 | $k |
| X26.2a1 | total | 7070 | $k |
| X26.2a2 | field share of downstream | 85 | % |
| X26.2b | derivative | -11700 | $k |
| X26.2b1 | saving per 0.01 | 117 | $k |
| X26.2c | tie weight | 0.273 | |
| X26.2d | untraced | 16 | |
| X26.2d1 | expected cost | 600 | $k |
| X26.3a | fraction found | 0.784 | |
| X26.3b | bound | 7.86 | |
| X26.3b1 | optimal | 7 | |
| X26.3b2 | cost, 6 | 59328 | $ |
| X26.3b3 | cost, 7 | 55997 | $ |
| X26.3b4 | cost, 8 | 56398 | $ |
| X26.3c | Lincoln-Petersen | 27.0 | |
| X26.3c1 | Chapman | 26.6 | |
| X26.3c2 | found | 23 | |
| X26.3c3 | remaining | 4.0 | |
| X26.3d | return | 77.8 | % |
| X26.3d1 | approval | 81.7 | % |
| X26.3d2 | abstention | 14.3 | % |
| X26.4a | DPW formula | 528.2 | |
| X26.4a1 | DPW | 528 | |
| X26.4a2 | yield | 0.8659 | |
| X26.4a3 | cost per good die | 32.81 | $ |
| X26.4b | after assembly | 38.38 | $ |
| X26.4b1 | after test | 41.12 | $ |
| X26.4c | gross margin | 45.2 | % |
| X26.4c1 | markup | 82.4 | % |
| X26.4c2 | gross profit per unit | 33.88 | $ |
| X26.4d | break-even | 2.66 | million |
| X26.5a | P/A | 4.6229 | |
| X26.5a1 | A/P | 0.21632 | |
| X26.5a2 | payment | 54079 | $ |
| X26.5b | NPV | 19.2 | $M |
| X26.5b1 | IRR | 21.25 | % |
| X26.5c | payback | 3.29 | years |
| X26.5d | NPV after slip | -8.70 | $M |
| X26.5d1 | value lost | 27.9 | $M |
| X26.6a | discounted units | 15.835 | million |
| X26.6b | licence PV | 23.835 | $M |
| X26.6b1 | build PV | 34.0 | $M |
| X26.6b2 | saving | 10.165 | $M |
| X26.6c | break-even | 26.0 | million |
| X26.6c1 | multiple | 1.64 | |
| X26.6d | royalty year 2 | 0.900 | $ |
| X26.6d1 | royalty year 3 | 0.810 | $ |
| X26.6d2 | royalty year 4 | 0.729 | $ |
| X26.6d3 | percentage PV | 13.74 | $M |
| X26.6d4 | equivalent per unit | 0.868 | $ |
| X26.6d5 | royalty saving | 2.09 | $M |
| X26.7a | effective gain | 1.360 | |
| X26.7a1 | new area | 110.3 | mm² |
| X26.7b | old DPW | 416 | |
| X26.7b1 | old yield | 0.8607 | |
| X26.7b2 | old cost | 41.89 | $ |
| X26.7b3 | new DPW | 577 | |
| X26.7b4 | new yield | 0.8760 | |
| X26.7b5 | new cost | 37.59 | $ |
| X26.7b6 | saving | 4.30 | $ |
| X26.7c | break-even | 9.29 | million |
| X26.7d | cost-per-function ratio | 0.931 | |
| X26.7d1 | wafer premium | 27 | % |
| X26.7d2 | cost-per-function saving | 7 | % |
| X26.8a | merchant energy | 2759 | $ |
| X26.8a1 | custom energy | 1840 | $ |
| X26.8a2 | merchant TCO | 37759 | $ |
| X26.8a3 | custom TCO | 19840 | $ |
| X26.8b | custom per equivalent | 26453 | $ |
| X26.8b1 | saving | 11307 | $ |
| X26.8c | break-even, equivalents | 4.42e4 | |
| X26.8c1 | break-even, chips | 5.90e4 | |
| X26.8d | price ceiling | 18138 | $ |
| X26.8d1 | equivalents | 112500 | |
| X26.9a | path A mean | 11.83 | weeks |
| X26.9a1 | path A sd | 1.424 | weeks |
| X26.9a2 | path B mean | 11.67 | weeks |
| X26.9a3 | path B sd | 1.202 | weeks |
| X26.9a4 | verification mean | 8.67 | weeks |
| X26.9a5 | regression mean | 3.17 | weeks |
| X26.9a6 | place-and-route mean | 7.33 | weeks |
| X26.9a7 | signoff mean | 4.33 | weeks |
| X26.9b | P(A by 14) | 0.936 | |
| X26.9b1 | P(B by 14) | 0.974 | |
| X26.9b2 | P(both) | 0.912 | |
| X26.9b3 | 90% date | 13.9 | weeks |
| X26.9b4 | z for A | 1.522 | |
| X26.9b5 | z for B | 1.941 | |
| X26.9c | expected tape-outs | 1.84 | |
| X26.9c1 | P(1) | 0.30 | |
| X26.9c2 | P(2) | 0.56 | |
| X26.9c3 | P(3) | 0.14 | |
| X26.9c4 | expected delay | 13.4 | weeks |
| X26.9d | full days | 110.5 | days |
| X26.9d1 | full weeks | 15.8 | weeks |
| X26.9d2 | ECO days | 36.4 | days |
| X26.9d3 | ECO weeks | 5.20 | weeks |
| X26.10a | EMV | 12.0 | $M |
| X26.10a1 | R1 net | 1.75 | $M |
| X26.10a2 | R2 net | 0.50 | $M |
| X26.10a3 | R3 net | 1.30 | $M |
| X26.10a4 | best net | 2.25 | $M |
| X26.10a5 | alternative net | 1.80 | $M |
| X26.10b | k | 0.12 | |
| X26.10b1 | lambda | 0.138 | |
| X26.10b2 | optimal time | 12.5 | weeks |
| X26.10b3 | respin probability | 0.129 | |
| X26.10c | cost at optimum | 18.9 | $M |
| X26.10c1 | cost at once | 30.0 | $M |
| X26.10d | new time | 9.27 | weeks |
| X26.10d1 | new probability | 0.0836 | |
| X26.10d2 | new cost | 15.6 | $M |
| X26.10d3 | saving | 3.27 | $M |
| X26.10d4 | weeks earlier | 3.3 | weeks |
| X26.10d5 | new k | 0.08 | |
| X26.11a | optimum | 14.8 | |
| X26.11a1 | output, 14 | 7.63 | FTE |
| X26.11a2 | output, 15 | 7.65 | FTE |
| X26.11b | member efficiency | 0.79 | |
| X26.11b1 | team output | 5.53 | FTE |
| X26.11b2 | cross factor | 0.86 | |
| X26.11b3 | total | 38.0 | FTE |
| X26.11b4 | per head | 0.594 | |
| X26.11c | output without | 9.36 | FTE |
| X26.11c1 | output during ramp | 5.94 | FTE |
| X26.11c2 | output after | 11.88 | FTE |
| X26.11c3 | break-even work | 55.2 | person-months |
| X26.11c4 | months | 5.89 | months |
| X26.11c5 | work during ramp | 14.85 | person-months |
| X26.11d | critical ratio | 0.667 | |
| X26.11d1 | base | 18 | |
| X26.11d2 | cost | 20.9 | $M |
| X26.11d3 | cost, base 12 | 21.4 | $M |
| X26.11d4 | cost, base 30 | 22.8 | $M |
| X26.11d5 | contracted | 78 | engineer-quarters |
| X26.12a | hours | 8.21e3 | h |
| X26.12a1 | fleet failures | 4.11e3 | |
| X26.12a2 | per vehicle | 8.21e-4 | |
| X26.12b | both fail | 1.52e-5 | |
| X26.12b1 | ratio | 60.9 | |
| X26.12c | bound | 15.0 | FIT |
| X26.12c1 | multiple of data | 1.50 | |
| X26.12c2 | hours for 10 FIT | 3.00e8 | h |
| X26.12d | TPP | 3520 | |
| X26.12d1 | density | 6.77 | |
| X26.4i1 | unrounded die cost | 32.809 | $ |
| X26.4i2 | after assembly from the rounded die cost | 38.39 | $ |
| X26.4i3 | after assembly, unrounded | 38.385 | $ |
| X26.5i1 | (A/P, 8%, 6) to six figures | 0.216315 | |
| X26.5i2 | NPV at 21% | 0.426 | $M |
| X26.5i3 | NPV at 22% | -1.248 | $M |
| X26.5i4 | NPV at 21.25% | 0.001 | $M |
| X26.7i1 | old DPW before rounding | 416.8 | |
| X26.7i2 | new DPW before rounding | 577.5 | |
| X26.7i3 | unrounded saving | 4.3046 | $ |
| X26.9i1 | P(A by 14 weeks) | 0.9359 | |
| X26.9i2 | P(B by 14 weeks) | 0.9739 | |
| X26.9i3 | P(both) at 13.8 weeks | 0.882 | |
| X26.9i4 | P(both) at 13.9 weeks | 0.897 | |
| X26.9i5 | P(both) at 14.0 weeks | 0.912 | |
| X26.9i6 | 90% date, finer | 13.92 | weeks |
| X26.9i7 | P(both) by table interpolation | 0.911 | |
| X26.10i1 | iterate 1 | 0.1353 | |
| X26.10i2 | iterate 2 | 0.1374 | |
| X26.10i3 | iterate 3 | 0.1377 | |
| X26.10i4 | iterate 1, tau = 2 | 0.0867 | |
| X26.10i5 | iterate 2, tau = 2 | 0.0872 | |
| X26.10i6 | lambda*, tau = 2 | 0.0873 | |
| X26.12i1 | dense MacTOPS | 110 | |
| X26.5i5 | interpolated IRR | 21.25 | % |
