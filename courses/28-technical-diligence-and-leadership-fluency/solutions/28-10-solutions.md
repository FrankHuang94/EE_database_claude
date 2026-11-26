# Solutions 28-10 · Conversation Scenarios

Problems: [28-10 problems](../problems/28-10-problems.md) · Chapter: [28-10](../chapters/28-10-conversation-scenarios.md). Every number is recomputed by [verify_28_10.py](../verify/verify_28_10.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 28-10.1

- (a) "What is the efficiency at 10%, 50% and 100% load, at what input voltage and temperature, with fans included?"
- (b) "What pin rate is qualified at each customer, and what bandwidth and energy per bit does that give per stack?"
- (c) "What FIT bound do you claim, at what confidence, junction temperature and activation energy, and what do field returns show?"

### Solution 28-10.2

Ridge $3 \times 10^{15}/6 \times 10^{12}$ = **500** FLOP/byte; intensity $2 \times 32$ = **64**; attainable $64 \times 6$ TB/s = **384** TFLOP/s, **12.8**% of peak; batch at the ridge **250**. Next question: "what latency per token do you see at batch 32, and how much KV cache does batch 250 need?"

### Solution 28-10.3

Frequency $1.15/1.05$ = **1.095**; power factor $1.05 \times 1.095^3$ = **1.379**; reduction **27.5**%. Next question: "how much comes from the node, and how much from design?"

### Solution 28-10.4

$25.6 \times 10^{12} \times 3.5 \times 10^{-12}$ = **89.6** W.

### Solution 28-10.5

$-\ln 0.05/(5 \times 10^5)$ = **6.0** per million link-hours (5.99 unrounded); cluster $4000 \times 24 \times 5.99 \times 10^{-6}$ = **0.575** flaps per day. Half the exposure doubles the bound; ask for field hours.

### Solution 28-10.6

$2 + 5000 \times 0.010/5 + 8000 \times 0.003/60$ = **12.4** µA; life $1000/0.0124/8766$ = **9.20** years. Next question: "at what temperature, and with what self-discharge?"

### Solution 28-10.7

$(1.4 + 5)/(10 + 6)$ = **40.0**%; weight $6/16$ = **0.375**.

### Solution 28-10.8

Odds $(0.3/0.7) \times 3 \times 0.4 \times 2 \times 1 \times 0.5$ = **0.514**, probability **34.0**%. Counted once: odds **1.03**, probability **50.7**%. Double-counting the shared weakness moved the posterior by almost 17 points.

### Solution 28-10.9

Factor $\tfrac13(1.1^{-1} + 1.1^{-2} + 1.1^{-3})$ = **0.829**; value $50 \times 0.3 \times 2 \times 0.829$ = **24.9** \$M; ratio **4.02**.

### Solution 28-10.10

First forecaster: $[5 \times 0.2^2 + 5 \times 0.6^2]/10$ = **0.20**. Always 0.5: **0.25**. Overconfident: $[6 \times 0.05^2 + 4 \times 0.95^2]/10$ = **0.3625**, worse than saying 0.5 every time.

### Solution 28-10.11

Unit cost $25 \times 0.5$ = **12.5** \$; die cost **9.5** \$; area **33.2** mm².

### Solution 28-10.12

(a) The posterior odds are the prior odds times the product of the likelihood ratios; multiplication is commutative, so any order gives the same product.

(b) With outcome $o \sim \text{Bernoulli}(q)$: $E[(p - o)^2] = q(p - 1)^2 + (1 - q)p^2 = p^2 - 2pq + q = (p - q)^2 + q - q^2$. The first term is zero only at $p = q$, so honest reporting minimizes the expected score. For $q = 0.7$: **0.21** at $p = 0.7$ and **0.25** at $p = 0.9$.

### Solution 28-10.13

A model answer follows. Other priors and ratios are acceptable if they are stated and justified.

(a) **Prior 0.5.** Battery-life figures are usually measured on some real profile, so the number is rarely invented. But "14 days" claims are typically quoted for a light profile (heart rate sampled rather than continuous, display mostly off, infrequent sync), so whether it holds for *always-on* heart rate is a coin toss before the meeting.

(b) **Identity:** life = capacity / average current (28-05 §3.5). The claim allows $300/(14 \times 24)$ = **893** µA on average before derating, or **714** µA with 20% held back. That figure is the budget to split between sleep, the heart-rate sensor and its processing, the radio and the display. An always-on optical heart-rate sensor typically draws a meaningful share of it, so the breakdown is the test.

(c) **Questions.**

1. "What is the average current split into sleep, heart-rate sensing, radio and display, and at what sampling rate, display on-time and sync interval?"
2. "What battery life do your beta units show in the field, at what temperature and usage profile, and how many units is that?"
3. "Where does 14 days stop holding: with GPS on, with an always-on display, at 0 °C?"

(d) **Expected answers.**

| Question | Strong (LR 3) | Partial (LR 1) | Evasive (LR 0.4) |
|---|---|---|---|
| 1 | A budget that sums to under about 700 µA, with the heart-rate duty cycle and the measurement setup | A total without the split, or a split without the profile | "Our power team optimized everything" |
| 2 | Field data from a stated number of units and profiles, close to the lab figure | Lab data only, offered as an artifact | "Customers love the battery life" |
| 3 | Named limits with numbers ("about 9 days with always-on display") | Limits without numbers | "It holds in all normal use" |

### Solution 28-10.14

(a) **Scores.**

- Energy per bit: **strong**. Conditions are given and a limitation is volunteered; the excluded PLL is the kind of detail an honest engineer offers.
- Customers: **partial**. The answer is plausible and an artifact (reference calls) is offered, but nothing can be checked yet.
- BER margin: **evasive**. "Very robust" replaces a number, and "no field issues" answers a different question.
- Field records: **evasive**, on the same fact.

(b) **Grouping.** The last two answers concern one fact, the worst-case margin. Count them once, at 0.4.

(c) **Posterior.** Odds $(0.4/0.6) \times 3 \times 1 \times 0.4$ = **0.80**, probability **44.4**%.

(d) **Careless debrief.** Counting both evasive answers gives odds $0.80 \times 0.4$ = **0.32**, probability **24.2**%. The 20-point gap is pure double counting.

(e) **All-in figures.** All-in $4 + 0.3$ = **4.3** pJ/bit; per lane $4.3 \times 10^{-12} \times 112 \times 10^9$ = **0.482** W. Compare the all-in figure, not the 4, with competitors' all-in figures (28-04 §3.4).

(f) **Follow-ups.**

- Reference calls with two of the three customers under NDA. Owner: the deal lead. Date: within two weeks.
- BER bathtub curves at the worst-case channel and 85 °C, from the evaluation board and from one customer's system. Owner: the target's SerDes lead. Date: within one week.
- The PLL and DSP power breakdown on the customer configuration. Owner: the target's SerDes lead. Date: with the BER data.

The margin question is where the probability can move most: strong data there would lift the posterior to $(0.4/0.6) \times 3 \times 1 \times 3 = 6$ in odds (86%).

### Solution 28-10.15

- (a) **Leading question.** Better: "What is the sort yield on the last five lots, at what die size?"
- (b) **Anchoring the speaker with your number first.** Better: "What utilization do you see, on which model and batch?" Then reconcile with your 25%.
- (c) **Arguing.** Better: "I get about 3% from the roofline. Help me square that with your figure."
- (d) **Bluffing.** Better: ask. "Which part of that sets your power, and what would a simpler equalizer cost you in reach?" Look up the terms afterward (24-03, 24-04).
- (e) **Counting repeats.** Both statements rest on one fact. Count it once, and ask for the stepping history as an artifact.
- (f) **Mistaking fluency for truth.** Confidence has a likelihood ratio near 1. Raise the probability only for answers whose content was checked or can be.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 28-10.2a | ridge | 500 | FLOP/byte |
| 28-10.2b | decode intensity | 64 | FLOP/byte |
| 28-10.2c | attainable | 384 | TFLOP/s |
| 28-10.2d | share of peak | 12.8 | % |
| 28-10.2e | batch at the ridge | 250 | sequences |
| 28-10.3a | frequency ratio | 1.095 | — |
| 28-10.3b | power factor | 1.379 | — |
| 28-10.3c | required reduction | 27.5 | % |
| 28-10.4 | SerDes power | 89.6 | W |
| 28-10.5a | 95% bound | 6.0 | per 10⁶ link-hours |
| 28-10.5b | cluster flaps per day | 0.575 | flaps |
| 28-10.6a | average current | 12.4 | µA |
| 28-10.6b | battery life | 9.20 | years |
| 28-10.7a | posterior mean | 40.0 | % |
| 28-10.7b | weight on the record | 0.375 | — |
| 28-10.8a | posterior odds | 0.514 | — |
| 28-10.8b | posterior probability | 34.0 | % |
| 28-10.8c | odds, counted once | 1.03 | — |
| 28-10.8d | probability, counted once | 50.7 | % |
| 28-10.9a | average discount factor | 0.829 | — |
| 28-10.9b | risk-adjusted value | 24.9 | $M |
| 28-10.9c | claim over value | 4.02 | — |
| 28-10.10a | Brier score, first forecaster | 0.20 | — |
| 28-10.10b | Brier score, always 0.5 | 0.25 | — |
| 28-10.10c | Brier score, overconfident | 0.3625 | — |
| 28-10.11a | unit-cost budget | 12.5 | $ |
| 28-10.11b | die-cost budget | 9.5 | $ |
| 28-10.11c | area budget | 33.2 | mm² |
| 28-10.12a | expected Brier, honest | 0.21 | — |
| 28-10.12b | expected Brier, overstated | 0.25 | — |
| 28-10.13a | average current allowed | 893 | µA |
| 28-10.13b | average current allowed, derated | 714 | µA |
| 28-10.14a | posterior odds | 0.80 | — |
| 28-10.14b | posterior probability | 44.4 | % |
| 28-10.14c | odds, careless debrief | 0.32 | — |
| 28-10.14d | probability, careless debrief | 24.2 | % |
| 28-10.14e | all-in energy per bit | 4.3 | pJ/bit |
| 28-10.14f | power per lane | 0.482 | W |
| 28-10.14g | probability with strong margin data | 86 | % |
