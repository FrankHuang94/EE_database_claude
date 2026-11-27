# Solutions 26-01 · Requirements, Specifications and the Design Process

Problems: [26-01 problems](../problems/26-01-problems.md) · Chapter: [26-01](../chapters/26-01-requirements-and-specifications.md). Every number is recomputed by [verify_26_01.py](../verify/verify_26_01.py).

---

## Solutions

### Solution 26-01.1

Model answers; the numbers are assumptions the writer must state and then agree with the customer.

(a) "The PMIC's 1.8 V buck converter shall convert with an efficiency of at least 90% from 10 mA to 500 mA load, at an input of 3.0 to 4.4 V and 25 °C; verified by test on characterization units, with analysis (loss model, 22-06) before silicon." Assumed: which rail, the load range and the input range. "Efficient" had no number and no operating point; light-load efficiency, the hard part for wearables, would otherwise be left out.

(b) "The 112 Gb/s SerDes shall achieve a pre-FEC bit-error ratio of at most 10⁻⁶ (and at most 10⁻¹⁵ after the specified FEC) over any channel whose insertion loss at the Nyquist frequency is at most 30 dB and whose crosstalk and return loss meet the channel template of Appendix B; verified by test on the evaluation board with a set of reference channels, and by analysis (channel simulation) for the template's corners." Assumed: the data rate, the loss limit and the template. "All customer channels" is unbounded; the requirement must define the channel class, and the customer's own channels then become a validation activity.

(c) "The NPU shall serve the reference model of Appendix C (a stated number of parameters, precision and sequence length) at a latency of at most 50 ms per token and a throughput of at least 2,000 tokens/s per chip, at the specified power limit; verified by analysis (performance model) before tape-out and by test on silicon." Assumed: the model, the precision, the batch and the power limit. "Large models fast" says neither which model nor which metric.

### Solution 26-01.2

(a) **Inspection**: the marking is a visible physical feature (or a record of it).

(b) **Analysis** supported by accelerated **test**: 15 years cannot be tested directly, so test structures are stressed at high temperature and current and the result is extrapolated with Black's equation (25-09).

(c) **Demonstration** (or test): link training with a reference host is a pass/fail showing of capability; detailed eye and jitter measurements would make it a test.

(d) **Test**: characterization at the corner yields measured data (a shmoo, 25-12), with static timing analysis before silicon.

(e) **Inspection** of records: the bill of materials and supplier declarations are checked, with laboratory analysis of samples where the risk warrants it.

### Solution 26-01.3

(a) The usable charge is $0.80 \times 22$ = **17.6** mAh, so $\bar I_{max} = 17.6/120$ = **0.147** mA.

(b) $\bar I = 0.90 \times 0.010 + 0.085 \times 0.40 + 0.015 \times 3.0 = 0.009 + 0.034 + 0.045$ = **0.088** mA, so the life is $17.6/0.088$ = **200** h (**8.33** days). The design meets the requirement with room to spare.

(c) With radio duty $d$ and sleep duty **0.915** − $d$, $\bar I = 0.010(0.915 - d) + 0.034 + 3.0d$ = **0.04315** + **2.99**$d$. Setting it equal to **0.1467** mA gives $d$ = **3.46**%.

(d) Now $\bar I_{max} = 0.70 \times 22/120$ = **0.1283** mA, and $d = (0.1283 - 0.04315)/2.99$ = **2.85**%. The end-of-life battery, not the new one, sets the radio's duty-cycle budget, which is why the requirement must state the battery age.

### Solution 26-01.4

(a) The unit interval is $1/(32 \times 10^9)$ = **31.25** ps, so the limit is 0.50 UI = **15.625** ps. $DJ = 4 + 3 + 2$ = **9** ps; $\sigma_{RJ} = \sqrt{0.30^2 + 0.25^2 + 0.22^2} = \sqrt{0.2009}$ = **0.448** ps; $2Q\sigma_{RJ} = 2 \times 7.03 \times 0.448 = 14.06 \times 0.448$ = **6.30** ps; $TJ$ = **15.30** ps (**0.490** UI), a margin of **0.32** ps.

(b) $\sqrt{4^2 + 3^2 + 2^2}$ = **5.39** ps, so $TJ$ = **11.69** ps: an apparent margin of **3.9** ps that does not exist.

(c) $14.06 \times (0.30 + 0.25 + 0.22) = 14.06 \times 0.77$ = **10.83** ps, so $TJ$ = **19.83** ps, failing by **4.20** ps.

(d) Error (b) is the dangerous one: it hides a real risk. Deterministic jitter (from reflections, crosstalk and duty-cycle distortion) is bounded and can align in the worst case, so it must add linearly. Error (c) is merely wasteful: it rejects a design that works, but it never ships a failure. The dual-Dirac model already separates the two kinds (24-02); budgets must keep them separate too.

### Solution 26-01.5

(a) The upper tail starts $(3.0 - 0.50)/0.90$ = **2.78**σ above the mean and the lower tail $(3.0 + 0.50)/0.90$ = **3.89**σ below it. So $P_{upper} = 1 - \Phi(2.78)$ = **2.74e-3**, $P_{lower} = \Phi(-3.89)$ = **5.04e-5**, and the total is **2.79e-3**.

(b) With no offset, $2[1 - \Phi(3.33)]$ = **8.58e-4**. The 0.50% offset multiplies the reject rate by **3.25**, almost all of it on one side.

(c) A spread requirement alone ("σ ≤ 0.9%") is met here, yet the product fails more often than planned, because the systematic offset was not budgeted. Mean errors (calibration, design offsets, a biased reference) add linearly to the limit, so the specification should state an allowance for the mean and verify it separately.

### Solution 26-01.6

(a) By induction on the two-variable identity, or directly from $\operatorname{Var}(\sum e_i) = E[(\sum_i(e_i - \mu_i))^2] = \sum_i\sum_jE[(e_i - \mu_i)(e_j - \mu_j)]$:

$$
\sigma_E^2 = \sum_i\sum_j\rho_{ij}\sigma_i\sigma_j = \sum_i\sigma_i^2 + 2\sum_{i<j}\rho_{ij}\sigma_i\sigma_j,
$$

with $\rho_{ii}$ = 1.

(b) With every $\rho_{ij}$ = 1, $\sigma_E^2 = \sum_i\sum_j\sigma_i\sigma_j = (\sum_i\sigma_i)^2$, so $\sigma_E = \sum_i\sigma_i$: the RSS of perfectly correlated terms is their linear sum, the worst case.

(c) With equal σ and common ρ, the double sum has $n$ diagonal terms σ² and $n(n - 1)$ off-diagonal terms ρσ², so $\sigma_E^2 = \sigma^2[n + n(n - 1)\rho]$.

(d) $\sqrt{6 + 30 \times 0.2} = \sqrt{12}$ = **3.46**σ, against $\sqrt 6$ = **2.45**σ for independence and 6σ for worst case. A modest common correlation of 0.2 moves the total **29**% of the way from RSS toward worst case. Shared causes (one supply, one temperature, one process corner) rarely give exactly zero correlation, which is why budgets often add a margin on top of the RSS.

### Solution 26-01.7

(a) Worst case gives each block $1.0/n$: **0.250**% for $n$ = 4 and **0.111**% for $n$ = 9. RSS requires $\sqrt{n}\,b = 1.0$, so each block gets $1.0/\sqrt n$: **0.500**% and **0.333**%.

(b) The ratio is $\sqrt n$: **2** and **3**. The larger the system, the more RSS helps, provided the blocks really are independent.

(c) RSS: the remaining variance is $1.0^2 - 0.50^2 = 0.75$, shared by three blocks, so each gets $\sqrt{0.25}$ = **0.500**%. Worst case: $(1.0 - 0.50)/3$ = **0.167**%.

### Solution 26-01.8

(a) $231/250$ = **92.4**%.

(b) $4 \times 0.25 + 15 \times 0.04$ = **1.6** expected escapes, costing $1.6 \times 1.5$ = **\$2.40 M**.

(c) $19 \times 0.015$ = **\$0.285 M**, so the expected loss is **8.4** times the cost of closing the gaps.

(d) Write the four high-risk tests first (they carry **1.0** of the 1.6 expected escapes), then two low-risk ones. That leaves 13 low-risk gaps: $13 \times 0.04 \times 1.5$ = **\$0.78 M** expected. Ranking by risk, not by order in the document, is what makes a limited budget go furthest.

### Solution 26-01.9

(a) An error that passes the review is caught in design with probability 0.5, in build with $0.5 \times 0.2$, in test with $0.5 \times 0.8 \times 0.7$, and escapes with $0.5 \times 0.8 \times 0.3$:

$$
\bar c_{down} = 0.5 \times 4 + 0.5 \times 0.2 \times 12 + 0.5 \times 0.8 \times 0.7 \times 40 + 0.5 \times 0.8 \times 0.3 \times 200,
$$

whose terms are **2.0**, **1.2**, **11.2** and **24.0**, so $\bar c_{down}$ = **38.4**.

(b) At 30%: found **18**, **21**, **4.2**, **11.76** and **5.04** (review, design, build, test, field); cost $60[0.3 + 0.7 \times 38.4]$ = **1630.8** units. At 50%: found **30**, **15**, **3.0**, **8.40** and **3.60**; cost $60[0.5 + 0.5 \times 38.4]$ = **1182** units.

(c) The saving is **448.8** units, or **$3.59 M**.

### Solution 26-01.10

(a) Let $\bar c_k$ be the expected cost of an error that has reached phase $k$. It is caught there with probability $p_k$ at cost $c_k$, or passes on with probability $1 - p_k$ and then costs $\bar c_{k+1}$; hence $\bar c_k = p_kc_k + (1 - p_k)\bar c_{k+1}$, with $\bar c$ = 200 in the field (everything left is caught there). For Problem 26-01.9: test, $0.7 \times 40 + 0.3 \times 200$ = **88**; build, $0.2 \times 12 + 0.8 \times 88$ = **72.8**; design, $0.5 \times 4 + 0.5 \times 72.8$ = **38.4**, which confirms (a).

(b) $\partial C/\partial p_1 = -N(\bar c_{down} - c_1) = -60 \times$ **37.4** = **−2244** units per unit of $p_1$, so one percentage point is worth **22.44** units, or **\$1.80e5** at \$8,000 per unit.

(c) $250{,}000/(2244 \times 8000)$ = **0.0139**, so the review pays for itself if it raises the catch rate by **1.39** percentage points.

(d) The model treats errors as independent and equally costly, assumes the review does not delay the program, and takes the escalation factors as known. In practice the errors a review catches are often the easy ones, while the expensive escapes are subtle; reviews also have diminishing returns. The lab samples the factors over their ranges; the conclusion that a review is worth a few percent of catch rate survives, but the dollar figure is uncertain.

### Solution 26-01.11

(a) $S_I = 0.35 \times 5 + 0.30 \times 4 + 0.20 \times 2 + 0.15 \times 2$ = **3.65**; $S_E = 0.35 \times 2 + 0.30 \times 3 + 0.20 \times 5 + 0.15 \times 5$ = **3.35**. The integrated radio ranks first.

(b) The other weights total **0.80**. $R_I = (0.35 \times 5 + 0.30 \times 4 + 0.15 \times 2)/0.80$ = **4.0625** and $R_E = (0.35 \times 2 + 0.30 \times 3 + 0.15 \times 5)/0.80$ = **2.9375**. With the time-to-market scores 2 and 5,

$$
w^* = \frac{4.0625 - 2.9375}{(4.0625 - 2.9375) - (2 - 5)} = \frac{1.125}{4.125} = \mathbf{0.273} .
$$

(c) No: the time-to-market weight needs to rise only **36**%, from 0.20 to 0.273, to flip the choice, against **69**% in Example 26-01.6. A team that is even moderately worried about schedule would choose the external radio. The review should debate the market window, because that weight, not the scores, decides.

### Solution 26-01.12

(a) Adding a constant $a$ to criterion $c$'s scores adds $w_ca$ to every option's total, which shifts all totals equally and leaves the ranking unchanged. Multiplying its scores by $m$ changes each total to $\sum_{j \ne c}w_js_j + (mw_c)s_c$, which is the weighted sum with $w_c$ replaced by $mw_c$; dividing every weight by $1 + (m - 1)w_c$ to restore $\sum w = 1$ does not change the ranking. So a criterion scored on a wider scale silently carries more weight.

(b) $S_I = 0.35 \times 5 + 0.30 \times 4 + 0.20 \times 4 + 0.15 \times 2$ = **4.05** and $S_E = 0.35 \times 2 + 0.30 \times 3 + 0.20 \times 10 + 0.15 \times 5$ = **4.35**: the external radio now wins.

(c) The scale change doubles the effective weight: $2 \times 0.20$ = **0.40** out of a weight total of **1.20**, or **0.333**, above the tie weight 0.273, which is why the ranking flipped. A decision matrix must use one scale for every criterion, or normalize each criterion explicitly.

### Solution 26-01.13

(a) **Agile** (iterative releases): firmware can be updated in the field at low cost, so short cycles with working increments and continuous regression fit, within the hardware program's gates.

(b) **Phase-gate / V-model** with iteration inside the phases: tape-out is irreversible, so it is a hard gate preceded by specification and RTL freezes, with verification planned against each specification level.

(c) **Spiral**: the largest risk is technical (will the block meet its specification at all?), so cycles of modelling, a test chip and measurement retire it before the block is committed to a product.

(d) **V-model** with formal traceability: functional-safety processes require every safety requirement to be implemented and verified at the matching level, and the V makes that pairing explicit (25-10).

### Solution 26-01.14

(a) $40 \times 2.5$ = **100** engineer-weeks, costing $100 \times 5{,}000$ = **\$0.50 M**.

(b) $40 \times 0.15 \times 1.0$ = **6.0** weeks of expected slip, costing $6.0 \times 2.0$ = **\$12.0 M**.

(c) Delay dominates, by a factor of **24**. Changes after freeze should therefore be approved against their schedule impact, by someone who owns the schedule, using the traceability links to find what each change touches; the engineering hours are the small part.

### Solution 26-01.15

(a) Life is $uQ/\bar I$, so $\ln t = \ln u + \ln Q - \ln\bar I$; for independent terms the log-variances add: $\sigma_{\ln t} = \sqrt{0.03^2 + 0.05^2}$ = **0.0583**.

(b) $z = \ln(168/175)/0.0583$ = **−0.700**, so $\Phi(-0.700)$ = **24.2**% of units fall short, although the mean exceeds the requirement.

(c) The median must satisfy $\ln(168/t_{50}) = -2.326 \times 0.0583$, so $t_{50} = 168\,e^{2.326 \times 0.0583}$ = **192.4** h.

(d) For example: "At least 99% of units shall operate for at least 168 h under profile UP-1 at 25 °C at 80% battery capacity, demonstrated by test on a sample sized for that confidence." "Every unit" cannot be verified by test, and the mean is not what a customer experiences; a percentile with a confidence statement is both meaningful and verifiable.

### Solution 26-01.16

(a) An X marks a trace (T = test, D = design element):

| | T1 | T2 | T3 | T4 | T5 | T6 | D1 | D2 | D3 | D4 | D5 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R1 (M1) | X | | | | | | X | | | X | |
| R2 (M1) | | X | | | | | X | | | | |
| R3 (M2) | | | X | | | | | X | | | |
| R4 (M2) | | | | X | | | | X | | | |
| R5 (M3) | | | | | | | | | X | | |
| R6 (M5) | | | | | | X | | | | X | |
| R7 (M4) | | | | | | | | | | | |
| R8 (M3) | | | | | | | | | X | | |

(b) Five of the eight requirements (R1, R2, R3, R4, R6) have a verifying test: coverage = 5/8 = **62.5**%. The **3** unverified requirements are R5, R8 and R7.

(c) Only R7 has no design element: **1** childless requirement. Nothing in the architecture was chosen to meet the temperature range, so it is met, if at all, by luck.

(d) **1** orphan test, T5, and **1** orphan design element, D5. The drop test suggests a missing requirement: "rugged outdoor use" (M4) clearly implies drop survival, but no PRD requirement states it, so the test has no pass criterion. The NFC module traces to no need at all: either the MRD is missing a need (contactless payment) or the module is cost (M5) with no value, and it should be challenged.

(e) M3 (R5 and R8 have no test) and M4 (R7 has no test and no design element, and its drop-survival requirement is missing). M1, M2 and M5 are fully verified at this level. The matrix turns these gaps into a short list of actions: add tests for R5, R7 and R8, add a drop requirement under M4, assign a design owner for R7, and justify or remove D5.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 26-01.3a0 | usable charge | 17.6 | mAh |
| 26-01.3a | allowed average current | 0.147 | mA |
| 26-01.3a1 | allowed average current, unrounded | 0.1467 | mA |
| 26-01.3b0 | sleep contribution | 0.009 | mA |
| 26-01.3b1 | sensing contribution | 0.034 | mA |
| 26-01.3b2 | radio contribution | 0.045 | mA |
| 26-01.3b | profile average | 0.088 | mA |
| 26-01.3b3 | life | 200 | h |
| 26-01.3b4 | life | 8.33 | days |
| 26-01.3c0 | constant term | 0.04315 | mA |
| 26-01.3c1 | sleep plus radio share | 0.915 | |
| 26-01.3c2 | radio slope | 2.99 | mA |
| 26-01.3c | radio duty allowed | 3.46 | % |
| 26-01.3d0 | allowed current, aged | 0.1283 | mA |
| 26-01.3d | radio duty allowed, aged | 2.85 | % |
| 26-01.4a | unit interval | 31.25 | ps |
| 26-01.4a7 | TJ limit | 15.625 | ps |
| 26-01.4a1 | DJ | 9 | ps |
| 26-01.4a2 | sigma RJ | 0.448 | ps |
| 26-01.4a0 | RJ variance | 0.2009 | ps² |
| 26-01.4a3 | 2Q sigma | 6.30 | ps |
| 26-01.4a4 | TJ | 15.30 | ps |
| 26-01.4a5 | TJ in UI | 0.490 | UI |
| 26-01.4a6 | margin | 0.32 | ps |
| 26-01.4b | RSS of DJ | 5.39 | ps |
| 26-01.4b1 | TJ with RSS DJ | 11.69 | ps |
| 26-01.4b2 | apparent margin | 3.9 | ps |
| 26-01.4a8 | 2Q | 14.06 | |
| 26-01.4c2 | sum of rms RJ | 0.77 | ps |
| 26-01.4c0 | linear RJ term | 10.83 | ps |
| 26-01.4c | TJ with linear RJ | 19.83 | ps |
| 26-01.4c1 | shortfall | 4.20 | ps |
| 26-01.5a | upper z | 2.78 | |
| 26-01.5a0 | lower z | 3.89 | |
| 26-01.5a1 | upper tail | 2.74e-3 | |
| 26-01.5a2 | lower tail | 5.04e-5 | |
| 26-01.5a3 | total outside | 2.79e-3 | |
| 26-01.5b | no offset | 8.58e-4 | |
| 26-01.5b1 | ratio | 3.25 | |
| 26-01.6d | correlated total | 3.46 | sigma |
| 26-01.6d1 | independent total | 2.45 | sigma |
| 26-01.6d2 | fraction of the way to worst case | 29 | % |
| 26-01.7a | worst case, n = 4 | 0.250 | % |
| 26-01.7a1 | worst case, n = 9 | 0.111 | % |
| 26-01.7a2 | RSS, n = 4 | 0.500 | % |
| 26-01.7a3 | RSS, n = 9 | 0.333 | % |
| 26-01.7b | ratio, n = 4 | 2 | |
| 26-01.7b1 | ratio, n = 9 | 3 | |
| 26-01.7c2 | remaining variance | 0.75 | %² |
| 26-01.7c3 | variance per block | 0.25 | %² |
| 26-01.7c | RSS, others | 0.500 | % |
| 26-01.7c1 | worst case, others | 0.167 | % |
| 26-01.8a | coverage | 92.4 | % |
| 26-01.8b | expected escapes | 1.6 | |
| 26-01.8b1 | expected cost | 2.40 | $M |
| 26-01.8c | cost to close | 0.285 | $M |
| 26-01.8c1 | ratio | 8.4 | |
| 26-01.8d | remaining expected cost | 0.78 | $M |
| 26-01.8d0 | high-risk expected escapes | 1.0 | |
| 26-01.9a1 | design term | 2.0 | units |
| 26-01.9a2 | build term | 1.2 | units |
| 26-01.9a3 | test term | 11.2 | units |
| 26-01.9a4 | field term | 24.0 | units |
| 26-01.9a | downstream average | 38.4 | units |
| 26-01.9b1 | 30%: review | 18 | |
| 26-01.9b2 | 30%: design | 21 | |
| 26-01.9b3 | 30%: build | 4.2 | |
| 26-01.9b4 | 30%: test | 11.76 | |
| 26-01.9b5 | 30%: field | 5.04 | |
| 26-01.9b | cost at 30% | 1630.8 | units |
| 26-01.9c1 | 50%: review | 30 | |
| 26-01.9c2 | 50%: design | 15 | |
| 26-01.9c3 | 50%: build | 3.0 | |
| 26-01.9c4 | 50%: test | 8.40 | |
| 26-01.9c5 | 50%: field | 3.60 | |
| 26-01.9c | cost at 50% | 1182 | units |
| 26-01.9d | saving | 448.8 | units |
| 26-01.9d1 | saving | 3.59 | $M |
| 26-01.10a | test-phase average | 88 | units |
| 26-01.10a1 | build-phase average | 72.8 | units |
| 26-01.10b | slope | -2244 | units |
| 26-01.10b0 | downstream minus review cost | 37.4 | units |
| 26-01.10b2 | value per point | 22.44 | units |
| 26-01.10b1 | value per point | 1.80e5 | $ |
| 26-01.10c | break-even increase | 1.39 | points |
| 26-01.10c0 | break-even increase | 0.0139 | |
| 26-01.11a | score I | 3.65 | |
| 26-01.11a1 | score E | 3.35 | |
| 26-01.11b0 | other weights | 0.80 | |
| 26-01.11b1 | R_I | 4.0625 | |
| 26-01.11b2 | R_E | 2.9375 | |
| 26-01.11b | tie weight | 0.273 | |
| 26-01.11c | rise needed | 36 | % |
| 26-01.11c1 | rise in Example 26-01.6 | 69 | % |
| 26-01.12b | score I, 1-10 scale | 4.05 | |
| 26-01.12b1 | score E, 1-10 scale | 4.35 | |
| 26-01.12c | effective weight | 0.333 | |
| 26-01.12c0 | doubled weight | 0.40 | |
| 26-01.12c1 | weight total | 1.20 | |
| 26-01.14a | rework | 100 | engineer-weeks |
| 26-01.14a1 | rework cost | 0.50 | $M |
| 26-01.14b | expected slip | 6.0 | weeks |
| 26-01.14b1 | delay cost | 12.0 | $M |
| 26-01.14c | ratio | 24 | |
| 26-01.15a | log-sigma of life | 0.0583 | |
| 26-01.15b | z | -0.700 | |
| 26-01.15b1 | fraction short | 24.2 | % |
| 26-01.15c | median needed | 192.4 | h |
| 26-01.16b | test coverage | 62.5 | % |
| 26-01.16b1 | unverified requirements | 3 | |
| 26-01.16c | childless requirements | 1 | |
| 26-01.16d | orphan tests | 1 | |
| 26-01.16d1 | orphan design elements | 1 | |
