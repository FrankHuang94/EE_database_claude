# Course 28 · Final Exam Solutions

Exam: [README.md](README.md). Every number is recomputed by [verify_28_exam.py](../verify/verify_28_exam.py), mostly by second routes. Intermediate values are shown rounded but carried at full precision.

---

**1.** (a) A: weighted $0.3 \times 4 + 0.3 \times 4 + 0.2 \times 2 + 0.2 \times 5$ = **3.80**; geometric $4^{0.6} \times 2^{0.2} \times 5^{0.2}$ = **3.64**. B: weighted **3.50**; geometric $3^{0.5} \times 4^{0.5}$ = **3.46**. A leads on both, but its geometric score falls more because of its weak third dimension.
(b) Prior odds $0.35/0.65 = 0.538$; posterior odds $0.538 \times 4 \times 0.6$ = **1.29**; probability **56.4**%.
(c) Expected value $0.564 \times 300 - 0.436 \times 150$ = **103.7** \$M. With perfect information the buyer buys only when the claim holds: $0.564 \times 300 = 169.1$, so EVPI = **65.4** \$M.
(d) $0.564 \times 120/1.12^2$ = **53.9** \$M.

**2.** (a) $2 \times 16384 \times 1.5 \times 10^9$ = **49.2** TOPS dense INT8, so the brochure is **1.99** times that: 2:4 sparsity at INT8 or dense INT4 (28-02).
(b) MacTOPS $16384 \times 1.5 \times 10^9/10^{12} = 24.6$; TPP $2 \times 24.6 \times 8$ = **393**.
(c) $100 \times 51.2 \times 10^9$ = **5.12** TOPS, **10.4**% of the dense peak.
(d) $5.12/4$ = **1.28** TOPS/W delivered, against the brochure's **24.5**: a factor of about 19, from sparsity or precision (2×) and memory-bound utilization.

**3.** (a) $P = 0.85 \times 0.95$ = **0.8075**; multiplier $0.8075/1.15^{7/12}$ = **0.744**.
(b) $\exp[(0.7/8.617 \times 10^{-5})(1/333.15 - 1/398.15)]$ = **53.6**.
(c) $1.833/(2 \times 300 \times 1000 \times 53.6) \times 10^9$ = **57.0** FIT.
(d) $n \ge 4.605 \times 10^9/(2 \times 20 \times 1000 \times 53.6) = 2149.9$, so **2150** devices.

**4.** (a) Frequency $1.18/1.08$ = **1.093**; power factor $1.04 \times 1.093^3$ = **1.356**; reduction $1 - 1/1.356$ = **26.3**%.
(b) Ridge $4 \times 10^{15}/8 \times 10^{12}$ = **500** FLOP/byte; intensity $2 \times 24$ = **48**; attainable $48 \times 8$ TB/s = **384** TFLOP/s, **9.6**% of peak; batch at the ridge **250**.
(c) $2048 \times 9.6/8$ = **2457.6** GB/s per stack; six stacks **14.7** TB/s.
(d) $14.75 \times 10^{12} \times 8 \times 6.5 \times 10^{-12}$ = **767** W.

**5.** (a) $102.4 \times 10^{12} \times 4.5 \times 10^{-12}$ = **460.8** W.
(b) $3 \times 10^{12} \times 8 \times 0.25 \times 10^{-12}$ = **6** W; edge $3000/1317$ = **2.28** mm.
(c) Pluggable $25/1.6 \times 10^{12}$ = **15.625** pJ/bit; CPO **3.75** pJ/bit.
(d) $10^{23/10}$ = **200** mW; electrical $0.1995/0.2$ = **0.998** W.

**6.** (a) $58 + 10\log_{10}(10^9/0.08)$ = **159.0** dB; ENOB $(58 - 1.76)/6.02$ = **9.34** bits.
(b) $\sigma_t = 10^{-58/20}/(2\pi \times 3 \times 10^9)$ = **66.8** fs.
(c) Class B $(\pi/4)10^{-9/20}$ = **27.9**%; Doherty **55.7**%.
(d) $20\log_{10}0.02$ = **−34.0** dB.

**7.** (a) Losses $6000(1/0.97 - 1)$ = **185.6** W and $6000(1/0.98 - 1)$ = **122.4** W; difference **63.1** W.
(b) Chain $0.975 \times 0.96 \times 0.90$ = **84.24**%; input $800/0.8424$ = **949.7** W; loss **149.7** W.
(c) $0.995 \times 0.997^4 \times 0.99$ = **97.3**%.
(d) $0.9 + 2500 \times 0.006/4 + 5000 \times 0.0015/20$ = **5.025** µA; life $220/0.005025/8766$ = **4.99** years.

**8.** (a) $\text{LR}^+ = 0.7/0.15$ = **4.67**; $\text{LR}^- = 0.3/0.85$ = **0.353**.
(b) Prior odds $1/3$. Present: odds 1.556, probability **60.9**%. Absent: odds 0.118, probability **10.5**%.
(c) $1 - 0.97^{30}$ = **59.9**%; expected $30 \times 0.03$ = **0.9** flags.
(d) Sensitivity $P(K \ge 3; 30, 0.25)$ = **98.9**%; false-positive rate $P(K \ge 3; 30, 0.03)$ = **6.01**%; ratio **16.5**. That ratio weighs the *rule*. A target observed with exactly three flags carries $(0.25/0.03)^3(0.75/0.97)^{27}$ = **0.558**, mild evidence of health, because a troubled target averages 7.5 flags (28-06 §3.2); full marks need neither, but an answer that uses 16.5 to update on an observed count of three loses the interpretation mark.

**9.** (a) Posterior $\text{Beta}(3.4, 11.6)$: mean $3.4/15$ = **22.7**%; weight $5/15$ = **0.333**.
(b) 5th to 95th percentile: **7.75**% to **41.8**%.
(c) $e^{\mu}$ = **1.275**; forecast $20 \times 1.275$ = **25.5** months; $\sigma$ = **0.139**; $\Phi(-\mu/\sigma)$ = **4.03**%.
(d) $q = 1 - 0.85^2$ = **27.75**% with one owner; $q^2$ = **7.70**% with two.

**10.** (a) Annuity $[1 - 1.1^{-5}]/0.1 = 3.791$; planned $40 \times 3.791$ = **151.6** \$M; late and partial $0.75 \times 151.6/1.1$ = **103.4** \$M; loss $1 - 0.75/1.1$ = **31.8**%.
(b) Migration $30 \times 5 \times 0.025$ = **3.75** \$M; delay $120 \times 2/12$ = **20** \$M. Freeze the flow until the tape-out.
(c) $1 - 0.45 \times 0.55$ = **0.7525**; with both $180 \times 0.7525$ = **135.45** \$M; better alone $180 \times 0.55$ = **99** \$M; gain **36.45** \$M, just above the \$35M cost: keep both, narrowly, and only if the programs are truly independent.
(d) Contingent $0.45 \times 300/1.1^3$ = **101.4** \$M; deal **601.4** \$M.

**11.** (a) DPW $\lfloor \pi \cdot 300^2/600 - \pi \cdot 300/\sqrt{300} \rfloor$ = **416**; yield $e^{-0.12}$ = **88.7**%; cost $20000/(416 \times 0.8869)$ = **54.21** \$.
(b) Ignoring the edge, $\text{DPW} = \pi d^2/(4A)$, so $C = (4W/\pi d^2)\,A\,e^{AD_0}$ and $\ln C = \text{const} + \ln A + AD_0$; then $d\ln C/d\ln A = A\,(1/A + D_0) = 1 + AD_0$ = **1.12**. At 165 mm²: DPW **376**, cost increase **12.0**%, average elasticity **1.20**, above 1.12 because of the edge term and whole-die rounding.
(c) Margin $1 - (54.21 + 12)/120$ = **44.8**%. For 65%: unit cost $120 \times 0.35$ = **42** \$, die budget **30** \$, area **89.9** mm².
(d) $0.45 \times 1.3 \times 35064 \times 0.09$ = **1846** \$; 400 W **1641** \$; saving **205** \$; capacity gain $0.45/0.40 - 1$ = **12.5**%.

**12.** (a) With $o \sim \text{Bernoulli}(q)$: $E[(p - o)^2] = q(1 - p)^2 + (1 - q)p^2 = p^2 - 2pq + q = (p - q)^2 + q(1 - q)$. Only the first term depends on $p$, and it is zero at $p = q$, so honest reporting minimizes the expected score (rubric below).
(b) All counted: odds $(0.45/0.55) \times 3 \times 2 \times 0.5 \times 3 \times 0.8$ = **5.89**, probability **85.5**%. Fact A once: odds **1.96**, probability **66.3**%.
(c) $[(0.1)^2 + (0.3)^2 + (0.6)^2 + (0.3)^2 + (0.8)^2]/5$ = **0.238**, barely better than **0.25** for always saying 0.5: the forecaster's 0.8 on a false claim cost most.
(d) See the rubric below.

**Rubric for 11(b) and 12(a)** (3 points each). 11(b): 1 for $C \propto Ae^{AD_0}$ from DPW and yield, 1 for the logarithmic derivative, 1 for the numbers. 12(a): 1 for the expectation over the Bernoulli outcome, 1 for completing the square, 1 for the minimization argument.

**Rubric for 12(d)** (3 points: one per question with a strong-answer criterion; ½ point for a pertinent question without one). Credible questions include: TOPS/W at which precision, sparsity and utilization on a named model, measured on silicon (strong: dense and sparse figures, the model, batch, and the measurement boundary, 28-02); power boundary (strong: chip, module or board, with the voltage and temperature); comparison basis (strong: named competitor part, same model and accuracy, independent or customer measurement); memory-bound performance (strong: bandwidth and the intensity of the buyer's model, 28-04).

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| X28.1a | A weighted score | 3.80 | — |
| X28.1a1 | A geometric score | 3.64 | — |
| X28.1a2 | B weighted score | 3.50 | — |
| X28.1a3 | B geometric score | 3.46 | — |
| X28.1b | posterior odds | 1.29 | — |
| X28.1b1 | posterior probability | 56.4 | % |
| X28.1c | expected value of buying | 103.7 | $M |
| X28.1c1 | EVPI | 65.4 | $M |
| X28.1d | earn-out PV | 53.9 | $M |
| X28.2a | dense INT8 peak | 49.2 | TOPS |
| X28.2a1 | brochure over dense | 1.99 | — |
| X28.2b | TPP | 393 | — |
| X28.2c | attainable | 5.12 | TOPS |
| X28.2c1 | share of dense peak | 10.4 | % |
| X28.2d | delivered TOPS/W | 1.28 | TOPS/W |
| X28.2d1 | brochure TOPS/W | 24.5 | TOPS/W |
| X28.3a | probability of production | 0.8075 | — |
| X28.3a1 | value multiplier | 0.744 | — |
| X28.3b | acceleration factor | 53.6 | — |
| X28.3c | FIT bound | 57.0 | FIT |
| X28.3d | devices needed | 2150 | devices |
| X28.4a | frequency ratio | 1.093 | — |
| X28.4a1 | power factor | 1.356 | — |
| X28.4a2 | required reduction | 26.3 | % |
| X28.4b | ridge | 500 | FLOP/byte |
| X28.4b1 | decode intensity | 48 | FLOP/byte |
| X28.4b2 | attainable | 384 | TFLOP/s |
| X28.4b3 | share of peak | 9.6 | % |
| X28.4b4 | batch at the ridge | 250 | sequences |
| X28.4c | stack bandwidth | 2457.6 | GB/s |
| X28.4c1 | six stacks | 14.7 | TB/s |
| X28.4d | six stacks' power | 767 | W |
| X28.5a | switch SerDes power | 460.8 | W |
| X28.5b | D2D link power | 6 | W |
| X28.5b1 | die edge | 2.28 | mm |
| X28.5c | pluggable energy per bit | 15.625 | pJ/bit |
| X28.5c1 | CPO energy per bit | 3.75 | pJ/bit |
| X28.5d | laser optical power | 200 | mW |
| X28.5d1 | laser electrical power | 0.998 | W |
| X28.6a | Schreier figure | 159.0 | dB |
| X28.6a1 | ENOB | 9.34 | bits |
| X28.6b | jitter | 66.8 | fs |
| X28.6c | class B at 9 dB | 27.9 | % |
| X28.6c1 | Doherty at 9 dB | 55.7 | % |
| X28.6d | 2% EVM | −34.0 | dB |
| X28.7a | loss at 97% | 185.6 | W |
| X28.7a1 | loss at 98% | 122.4 | W |
| X28.7a2 | difference | 63.1 | W |
| X28.7b | chain efficiency | 84.24 | % |
| X28.7b1 | input power | 949.7 | W |
| X28.7b2 | loss | 149.7 | W |
| X28.7c | package yield | 97.3 | % |
| X28.7d | average current | 5.025 | µA |
| X28.7d1 | battery life | 4.99 | years |
| X28.8a | LR+ | 4.67 | — |
| X28.8a1 | LR− | 0.353 | — |
| X28.8b | posterior, present | 60.9 | % |
| X28.8b1 | posterior, absent | 10.5 | % |
| X28.8c | at least one false flag | 59.9 | % |
| X28.8c1 | expected false flags | 0.9 | flags |
| X28.8d | sensitivity, three or more | 98.9 | % |
| X28.8d1 | false-positive rate, three or more | 6.01 | % |
| X28.8d2 | ratio | 16.5 | — |
| X28.8d3 | likelihood ratio, exactly three | 0.558 | — |
| X28.9a | posterior mean | 22.7 | % |
| X28.9a1 | weight on the record | 0.333 | — |
| X28.9b | 5th percentile | 7.75 | % |
| X28.9b1 | 95th percentile | 41.8 | % |
| X28.9c | geometric-mean overrun | 1.275 | — |
| X28.9c1 | forecast | 25.5 | months |
| X28.9c2 | standard deviation of log-ratios | 0.139 | — |
| X28.9c3 | probability of meeting plan | 4.03 | % |
| X28.9d | one owner, two years | 27.75 | % |
| X28.9d1 | two owners, two years | 7.70 | % |
| X28.10a | planned synergy value | 151.6 | $M |
| X28.10a1 | late and partial | 103.4 | $M |
| X28.10a2 | loss | 31.8 | % |
| X28.10b | migration cost | 3.75 | $M |
| X28.10b1 | delay cost | 20 | $M |
| X28.10c | at least one succeeds | 0.7525 | — |
| X28.10c1 | value with both | 135.45 | $M |
| X28.10c2 | better alone | 99 | $M |
| X28.10c3 | gain | 36.45 | $M |
| X28.10d | contingent PV | 101.4 | $M |
| X28.10d1 | deal PV | 601.4 | $M |
| X28.11a | dies per wafer | 416 | dies |
| X28.11a1 | yield | 88.7 | % |
| X28.11a2 | cost per good die | 54.21 | $ |
| X28.11b | no-edge elasticity | 1.12 | — |
| X28.11b1 | dies per wafer at 165 mm² | 376 | dies |
| X28.11b2 | cost increase | 12.0 | % |
| X28.11b3 | average elasticity | 1.20 | — |
| X28.11c | gross margin | 44.8 | % |
| X28.11c1 | unit-cost budget | 42 | $ |
| X28.11c2 | die-cost budget | 30 | $ |
| X28.11c3 | area budget | 89.9 | mm² |
| X28.11d | energy cost, 450 W | 1846 | $ |
| X28.11d1 | energy cost, 400 W | 1641 | $ |
| X28.11d2 | saving | 205 | $ |
| X28.11d3 | capacity gain | 12.5 | % |
| X28.12b | odds, all counted | 5.89 | — |
| X28.12b1 | probability, all counted | 85.5 | % |
| X28.12b2 | odds, fact A once | 1.96 | — |
| X28.12b3 | probability, fact A once | 66.3 | % |
| X28.12c | Brier score | 0.238 | — |
| X28.12c1 | always 0.5 | 0.25 | — |
