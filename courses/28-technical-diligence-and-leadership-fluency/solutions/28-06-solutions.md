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

Factor $\tfrac13(1.1^{-1} + 1.1^{-2} + 1.1^{-3})$ = **0.829**; risk-adjusted revenue $60 \times 0.35 \times 2$ = **42** \$M; present value **34.8** \$M; ratio $120/34.8$ = **3.45**.

### Solution 28-06.8

Independent: odds $(0.4/0.6) \times 4 \times 2 \times 0.5$ = **2.67**, probability **72.7**%. Shared cause (count the 4 once): odds **1.33**, probability **57.1**%.

### Solution 28-06.9

$0.14^3$ = **0.274**%; $0.30^3$ = **2.7**%; $0.05^3$ = **0.0125**%. In 2024, **30**% of projects needed four or more spins (16% + 10% + 4% of the chart readings [R-645]; **30.9**% after renormalizing their 97% total). These are likelihoods of the record under each rate, not the probability that the team is unusual: with 28-07's Beta prior ($\theta_0 = 0.14$, $n_0 = 10$), three of three gives a posterior mean of $(1.4 + 3)/13$ = **33.8**%, better than average but far from proven exceptional. Independence across one team's projects is also doubtful (shared IP, methods and people), which makes a run of successes less surprising. So either the team is good, or "first silicon" means something weaker (booted, rather than shipped A0), or the projects were less complex. Ask for the stepping of each shipped product and the definition.

### Solution 28-06.10

$15/40$ = **0.375**; reaching one-to-one needs **25** more verification engineers, costing $25 \times 0.25$ = **6.25** \$M a year. The gap is a question, not a verdict. The benchmark is a mean *peak per-project* head count, while 40 and 15 are company totals; designers also spend about half their time verifying, so effort ratios (Problem 28-07.10: 1.70 for this team, against about 2.9 for a team at one-to-one heads) are the better comparison. And a team reusing mature IP needs less verification than one building new blocks.

### Solution 28-06.11

Mean overrun $(25 + 40 + 30)/3$ = **31.7**%; implied duration $18 \times 1.317$ = **23.7** months. The arithmetic mean estimates the *mean* duration; 28-07 §3.2 works with logarithms to model the whole distribution, whose median is slightly shorter, and warns that three projects say little about the spread.

### Solution 28-06.12

(a) $P(T \mid F) = P(F \mid T)P(T)/P(F)$ and $P(\bar T \mid F) = P(F \mid \bar T)P(\bar T)/P(F)$; dividing cancels $P(F)$, giving posterior odds $= [\pi/(1 - \pi)] \times s/f$. For an absent flag, replace $P(F \mid \cdot)$ by $P(\bar F \mid \cdot)$: odds $= [\pi/(1 - \pi)] \times (1 - s)/(1 - f)$.

(b) The probability that none of $n$ independent flags appears is $(1 - f)^n$, so at least one appears with probability $1 - (1 - f)^n$. Since $\ln(1 - f) = -f - f^2/2 - \dots \approx -f$ for small $f$, $(1 - f)^n = e^{n\ln(1 - f)} \approx e^{-nf}$.

(c) Equal shares $1/N$ give $\text{HHI} = N \times (1/N)^2 = 1/N$. For any shares, by the Cauchy–Schwarz inequality, $(\sum x_i)^2 \le N\sum x_i^2$, so $1 \le N \cdot \text{HHI}$, that is $\text{HHI} \ge 1/N$, with equality only for equal shares.

(d) The event "$K \ge k$" is a test whose sensitivity is $P(K \ge k \mid T)$ and false-positive rate $P(K \ge k \mid \bar T)$; its ratio follows as for any flag. When $s > f$, the binomial likelihood ratio for exactly $j$ flags, $(s/f)^j[(1 - s)/(1 - f)]^{n - j}$, rises with $j$, so the upper tail is weighted ever more toward the troubled distribution as $k$ rises, and the ratio of tail probabilities rises too.

(e) $P(K = k \mid T)/P(K = k \mid \bar T) = \binom{n}{k}s^k(1 - s)^{n - k}/[\binom{n}{k}f^k(1 - f)^{n - k}]$; the binomial coefficients cancel, leaving $(s/f)^k[(1 - s)/(1 - f)]^{n - k} = (\text{LR}^+)^k(\text{LR}^-)^{n - k}$, the product of the single-flag ratios for the $k$ present and $n - k$ absent flags. At $k = 2$: $7.5^2 \times 0.729^{23}$ = **0.0394**. It is below 1 because 23 absent flags, each with $\text{LR}^- = 0.729$, outweigh two present ones: two flags are typical of a healthy company and very unusual for a troubled one, which would show about 7.5.

### Solution 28-06.13

(a) $\text{LR}(F_1) = 0.6/0.2$ = **3**. Marginally, $P(F_2 \mid T) = 0.9 \times 0.6 + 0.2 \times 0.4 = 0.62$ and $P(F_2 \mid \bar T) = 0.6 \times 0.2 + 0.05 \times 0.8 = 0.16$, so $\text{LR}(F_2)$ = **3.875**. Given $F_1$, $\text{LR}(F_2 \mid F_1) = 0.9/0.6 = 1.5$, and the joint ratio is $3 \times 1.5$ = **4.5**.

(b) Prior odds $1/3$. Correct: odds 1.5, posterior **60.0**%. Wrongly multiplied: $3 \times 3.875$ = **11.6**, odds 3.875, posterior **79.5**%. Stronger flag only: odds $3.875/3$, posterior **56.4**%. Counting the stronger flag once is much closer here, because $F_2$ is largely an echo of $F_1$: most of its marginal power comes from the fact that troubled targets show $F_1$ more often, which $F_1$ has already counted. The correct answer lies between the two shortcuts, as the chain rule says it must for partially dependent flags.

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
| 28-06.9e | four or more spins, renormalized | 30.9 | % |
| 28-06.9f | posterior mean after three of three | 33.8 | % |
| 28-06.10a | verification-to-design ratio | 0.375 | — |
| 28-06.10b | hires to reach 1:1 | 25 | engineers |
| 28-06.10c | annual cost | 6.25 | $M |
| 28-06.11a | mean overrun | 31.7 | % |
| 28-06.11b | implied duration | 23.7 | months |
| 28-06.12e | likelihood ratio, exactly two flags | 0.0394 | — |
| 28-06.13a | LR of the first flag | 3 | — |
| 28-06.13b | marginal LR of the second flag | 3.875 | — |
| 28-06.13c | joint LR, chain rule | 4.5 | — |
| 28-06.13d | product, wrongly assuming independence | 11.6 | — |
| 28-06.13e | posterior, correct | 60.0 | % |
| 28-06.13f | posterior, wrongly multiplied | 79.5 | % |
| 28-06.13g | posterior, stronger flag only | 56.4 | % |
