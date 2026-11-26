# Solutions 28-08 · Post-Acquisition Integration Risk

Problems: [28-08 problems](../problems/28-08-problems.md) · Chapter: [28-08](../chapters/28-08-integration-risk.md). Every number is recomputed by [verify_28_08.py](../verify/verify_28_08.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 28-08.1

- (a) **Evasive:** it offers what the buyer may want to hear and ignores the current tape-out. Strong would name the tape-out date and propose a sequence.
- (b) **Strong:** a dated plan that protects the tape-out, a sequence and a mechanism for transferring methodology.
- (c) **Evasive:** an assertion. Strong would compare products socket by socket and say where they overlap.
- (d) **Partial:** honest about a gap that matters. It becomes strong with the license terms in hand; until then it is a diligence action item, not a red flag.

### Solution 28-08.2

Annuity $[1 - 1.12^{-4}]/0.12$ = **3.037**; planned $30 \times 3.037$ = **91.1** $M. One year late at 75%: $0.75 \times 91.1/1.12$ = **61.0** $M; two years: **54.5** $M. Losses $1 - 0.75/1.12$ = **33.0**% and $1 - 0.75/1.12^2$ = **40.2**%.

### Solution 28-08.3

$40 \times 6 \times 0.022$ = **5.28** $M; lost revenue $90 \times 4/12$ = **30** $M.

### Solution 28-08.4

(a) Both fail $0.3 \times 0.6$ = **0.18**; at least one **0.82**; value with both $150 \times 0.82$ = **123** $M; better alone **105** $M; gain **18** $M, below the $25M cost: cancel the second program.

(b) At least one succeeds with probability $1 - 0.25 = 0.75$; gain $150 \times 0.75 - 105$ = **7.5** $M, an even clearer case to cancel.

### Solution 28-08.5

Revenue $30 \times 10^6 \times 12$ = $360M; royalty **5.4** $M at 1.5% and **10.8** $M at 3%; the difference is **1.5** margin points.

### Solution 28-08.6

Contingent share $0.8/2.0$ = **40**%. At $p = 0.5$: contingent $0.5 \times 0.8/1.1^2$ = **0.331** $B; deal **1.53** $B. At $p = 0.7$: deal **1.66** $B.

### Solution 28-08.7

$10 + 12 + 15 + 4.5$ = **41.5** $M; largest **15** $M (the tail risk). With the review: $41.5 - 15 + 3$ = **29.5** $M; saving **12** $M.

### Solution 28-08.8

400 TOPS: TPP $400 \times 8$ = **3200**; density $3200/600$ = **5.33**: below 4800, and above 1600 but with density below 5.92, so not in 3A090.a under the 2023 text (it falls in the lower 3A090.b band if designed or marketed for datacenters [R-659]). 1,200 TOPS: **9600**, above 4800 (3A090.a.1). Edge NPU: **1200**, below 1600.

### Solution 28-08.9

$0.8 \times 189.5/1.1^2$ = **125.3** $M; loss **33.9**%.

### Solution 28-08.10

Fixed window: years 2–5 only, $50 \times [1 - 1.1^{-4}]/0.1 \times 1.1^{-1}$ = **144.1** $M, a loss of **24.0**%. Shifted window: $189.5/1.1$ = **172.3** $M, a loss of **9.09**%. Losing a year of a fixed window costs more than two and a half times as much as shifting it.

### Solution 28-08.11

No package: $0.99^{24}$ = **78.6**% stay. Lump vesting: $0.99^{23} \times 0.85$ = **67.5**%. The cliff concentrates departures and, here, loses more people over two years than steady attrition; staged vesting spreads the risk.

### Solution 28-08.12

(a) $\sum_{t=1}^{n}x^t$ with $x = 1/(1 + r)$ is $x(1 - x^n)/(1 - x)$. Since $x/(1 - x) = 1/r$, the sum is $[1 - (1 + r)^{-n}]/r$.

(b) Each cash flow $\rho S$ arrives $d$ years later than planned, at $t + d$, so its value is $\rho S(1 + r)^{-(t + d)} = \rho(1 + r)^{-d} \times S(1 + r)^{-t}$; summing over $t$ multiplies the planned value by $\rho(1 + r)^{-d}$.

(c) With both programs the socket is won unless both fail: value $W[1 - P(\text{both fail})]$. With the better alone it is $W\max(p_1, p_2)$. The difference is the gain. Positive correlation makes joint failure more likely than $(1 - p_1)(1 - p_2)$, which lowers $1 - P(\text{both fail})$ and the gain.

(d) Loss is $L = \sum_i I_i\mathbf{1}_i$, where $\mathbf{1}_i$ is 1 if risk $i$ occurs. By linearity of expectation, $E[L] = \sum_i I_iP(\mathbf{1}_i = 1) = \sum_i p_iI_i$, whatever the dependence between risks. A mitigation that changes $p_i$ or $I_i$ changes only its own term, so its value is the change in $p_iI_i$.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 28-08.2a | annuity factor | 3.037 | — |
| 28-08.2b | planned value | 91.1 | $M |
| 28-08.2c | one year late, 75% | 61.0 | $M |
| 28-08.2d | two years late, 75% | 54.5 | $M |
| 28-08.2e | loss, one year | 33.0 | % |
| 28-08.2f | loss, two years | 40.2 | % |
| 28-08.3a | migration cost | 5.28 | $M |
| 28-08.3b | lost revenue | 30 | $M |
| 28-08.4a | both fail, independent | 0.18 | — |
| 28-08.4b | at least one succeeds | 0.82 | — |
| 28-08.4c | value with both | 123 | $M |
| 28-08.4d | value with the better one | 105 | $M |
| 28-08.4e | gain, independent | 18 | $M |
| 28-08.4f | gain, correlated | 7.5 | $M |
| 28-08.5a | royalty at 1.5% | 5.4 | $M |
| 28-08.5b | royalty at 3% | 10.8 | $M |
| 28-08.5c | margin points | 1.5 | points |
| 28-08.6a | contingent share | 40 | % |
| 28-08.6b | contingent PV at 0.5 | 0.331 | $B |
| 28-08.6c | deal PV at 0.5 | 1.53 | $B |
| 28-08.6d | deal PV at 0.7 | 1.66 | $B |
| 28-08.7a | expected loss | 41.5 | $M |
| 28-08.7b | largest contributor | 15 | $M |
| 28-08.7c | expected loss after review | 29.5 | $M |
| 28-08.7d | saving | 12 | $M |
| 28-08.8a | TPP, 400 TOPS | 3200 | — |
| 28-08.8b | performance density | 5.33 | per mm² |
| 28-08.8c | TPP, 1,200 TOPS | 9600 | — |
| 28-08.8d | TPP, edge NPU | 1200 | — |
| 28-08.9a | value, two years late | 125.3 | $M |
| 28-08.9b | loss | 33.9 | % |
| 28-08.10a | value, fixed window | 144.1 | $M |
| 28-08.10b | loss, fixed window | 24.0 | % |
| 28-08.10c | value, shifted window | 172.3 | $M |
| 28-08.10d | loss, shifted window | 9.09 | % |
| 28-08.11a | retention, no package | 78.6 | % |
| 28-08.11b | retention, lump vesting | 67.5 | % |
