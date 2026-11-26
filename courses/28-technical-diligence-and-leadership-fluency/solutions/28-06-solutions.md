# Solutions 28-06 · Red Flags and Green Flags

Problems: [28-06 problems](../problems/28-06-problems.md) · Chapter: [28-06](../chapters/28-06-red-and-green-flags.md). Every number is recomputed by [verify_28_06.py](../verify/verify_28_06.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 28-06.1

- (a) **Weak red flag.** Most chip projects run late (75% in the 2024 survey [R-621]), so one six-week slip has a likelihood ratio near 1. Settle it with the cause and whether the plan absorbed it.
- (b) **Red flag**, moderately strong: it may mean the engineering bench is thin or the story is managed. Settle it by meeting the engineers without the CEO and asking 28-04/28-05 questions.
- (c) **Strong green flag**: independent reproduction is rare for a false claim. Settle the remaining doubt by checking that the customers' setups match the buyer's use.
- (d) **Red flag**, stronger if the departures cluster in one team. Settle it with exit reasons, who replaced them and the state of their designs.
- (e) **Red flag on supply**, weak on technology: single sourcing is common at the leading edge. Settle it with contracted capacity, allocation history and a qualification plan for alternates.

### Solution 28-06.2

$\text{LR}^+ = 0.5/0.05$ = **10**; $\text{LR}^- = 0.5/0.95$ = **0.526**. Prior odds $0.3/0.7 = 0.429$. Present: odds **4.29**, probability **81.1**%. Absent: odds **0.226**, probability **18.4**%.

### Solution 28-06.3

$1 - 0.975^{40}$ = **63.7**%; expected $40 \times 0.025$ = **1**; $P(K \ge 2)$ = **26.4**%. Approximation $1 - e^{-1}$ = **63.2**%, close because $f$ is small.

### Solution 28-06.4

"Two or more": sensitivity **99.8**%, false-positive rate **26.4**%, ratio **3.78**. "Five or more": sensitivity **91.0**%, false-positive rate **0.278**%, ratio **327**. Two or more suits a trigger for deeper diligence (few misses, cheap false alarms); five or more suits a walk-away recommendation (very few healthy companies reach it), although a walk-away should also rest on the content of the flags, not only their count.

### Solution 28-06.5

One year: $1 - 0.85^3$ = **38.6**%. Three years: $1 - 0.85^9$ = **76.8**%. With retention (7.5%): $1 - 0.925^9$ = **50.4**%.

### Solution 28-06.6

$\text{HHI} = 0.09 + 0.0625 + 0.0225 + 3 \times 0.01$ = **0.205**; effective number **4.88**. Losing the two largest costs **55**% of revenue.

### Solution 28-06.7

Factor $\tfrac13(1.1^{-1} + 1.1^{-2} + 1.1^{-3})$ = **0.829**; risk-adjusted revenue $60 \times 0.35 \times 2$ = **42** $M; present value **34.8** $M; ratio $120/34.8$ = **3.45**.

### Solution 28-06.8

Independent: odds $(0.4/0.6) \times 4 \times 2 \times 0.5$ = **2.67**, probability **72.7**%. Shared cause (count the 4 once): odds **1.33**, probability **57.1**%.

### Solution 28-06.9

$0.14^3$ = **0.274**%; $0.30^3$ = **2.7**%; $0.05^3$ = **0.0125**%. In 2024, **30**% of projects needed four or more spins (16% + 10% + 4% [R-645]). The record is unlikely by chance, so either the team is unusually good, or "first silicon" means something weaker (booted, rather than shipped A0), or the projects were less complex. Ask for the stepping of each shipped product and the definition.

### Solution 28-06.10

$15/40$ = **0.375**; reaching one-to-one needs **25** more verification engineers, costing $25 \times 0.25$ = **6.25** $M a year. The gap is a question, not a verdict: a team reusing mature IP needs less verification than one building new blocks.

### Solution 28-06.11

Mean overrun $(25 + 40 + 30)/3$ = **31.7**%; implied duration $18 \times 1.317$ = **23.7** months.

### Solution 28-06.12

(a) $P(T \mid F) = P(F \mid T)P(T)/P(F)$ and $P(\bar T \mid F) = P(F \mid \bar T)P(\bar T)/P(F)$; dividing cancels $P(F)$, giving posterior odds $= [\pi/(1 - \pi)] \times s/f$. For an absent flag, replace $P(F \mid \cdot)$ by $P(\bar F \mid \cdot)$: odds $= [\pi/(1 - \pi)] \times (1 - s)/(1 - f)$.

(b) The probability that none of $n$ independent flags appears is $(1 - f)^n$, so at least one appears with probability $1 - (1 - f)^n$. Since $\ln(1 - f) = -f - f^2/2 - \dots \approx -f$ for small $f$, $(1 - f)^n = e^{n\ln(1 - f)} \approx e^{-nf}$.

(c) Equal shares $1/N$ give $\text{HHI} = N \times (1/N)^2 = 1/N$. For any shares, by the Cauchy–Schwarz inequality, $(\sum s_i)^2 \le N\sum s_i^2$, so $1 \le N \cdot \text{HHI}$, that is $\text{HHI} \ge 1/N$, with equality only for equal shares.

(d) The event "$K \ge k$" is a test whose sensitivity is $P(K \ge k \mid T)$ and false-positive rate $P(K \ge k \mid \bar T)$; its ratio follows as for any flag. When $s > f$, the binomial likelihood ratio for exactly $j$ flags, $(s/f)^j[(1 - s)/(1 - f)]^{n - j}$, rises with $j$, so the upper tail is weighted ever more toward the troubled distribution as $k$ rises, and the ratio of tail probabilities rises too.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 28-06.2a | LR+ | 10 | — |
| 28-06.2b | LR− | 0.526 | — |
| 28-06.2c | posterior odds, present | 4.29 | — |
| 28-06.2d | posterior, present | 81.1 | % |
| 28-06.2e | posterior odds, absent | 0.226 | — |
| 28-06.2f | posterior, absent | 18.4 | % |
| 28-06.3a | at least one false flag | 63.7 | % |
| 28-06.3b | expected false flags | 1 | flags |
| 28-06.3c | two or more | 26.4 | % |
| 28-06.3d | exponential approximation | 63.2 | % |
| 28-06.4a | sensitivity, two or more | 99.8 | % |
| 28-06.4b | false-positive rate, two or more | 26.4 | % |
| 28-06.4c | ratio, two or more | 3.78 | — |
| 28-06.4d | sensitivity, five or more | 91.0 | % |
| 28-06.4e | false-positive rate, five or more | 0.278 | % |
| 28-06.4f | ratio, five or more | 327 | — |
| 28-06.5a | at least one leaves, one year | 38.6 | % |
| 28-06.5b | at least one leaves, three years | 76.8 | % |
| 28-06.5c | with retention, three years | 50.4 | % |
| 28-06.6a | HHI | 0.205 | — |
| 28-06.6b | effective customers | 4.88 | — |
| 28-06.6c | revenue lost, two largest | 55 | % |
| 28-06.7a | average discount factor | 0.829 | — |
| 28-06.7b | risk-adjusted revenue | 42 | $M |
| 28-06.7c | present value | 34.8 | $M |
| 28-06.7d | claim over value | 3.45 | — |
| 28-06.8a | odds, independent | 2.67 | — |
| 28-06.8b | posterior, independent | 72.7 | % |
| 28-06.8c | odds, shared cause | 1.33 | — |
| 28-06.8d | posterior, shared cause | 57.1 | % |
| 28-06.9a | three for three at 14% | 0.274 | % |
| 28-06.9b | three for three at 30% | 2.7 | % |
| 28-06.9c | three for three at 5% | 0.0125 | % |
| 28-06.9d | four or more spins, 2024 | 30 | % |
| 28-06.10a | verification-to-design ratio | 0.375 | — |
| 28-06.10b | hires to reach 1:1 | 25 | engineers |
| 28-06.10c | annual cost | 6.25 | $M |
| 28-06.11a | mean overrun | 31.7 | % |
| 28-06.11b | implied duration | 23.7 | months |
