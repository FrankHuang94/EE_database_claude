# Solutions 26-02 · Design Reviews, Documentation and Standards Bodies

Problems: [26-02 problems](../problems/26-02-problems.md) · Chapter: [26-02](../chapters/26-02-design-reviews-and-standards.md). Every number is recomputed by [verify_26_02.py](../verify/verify_26_02.py).

---

## Solutions

### Solution 26-02.1

(a) **Peer review**: independent experts examine a work product to find defects before it reaches a gate; it decides nothing about the program, only which issues must be fixed.

(b) **Milestone review** (the tape-out gate): a decision authority decides whether to spend the mask set.

(c) **Peer review**, with an outside expert, which adds the independent viewpoint §3.2 values.

(d) **Milestone review** (the architecture review, NASA's PDR analogue): it decides whether to proceed to detailed design [R-630].

### Solution 26-02.2

A model answer:

- *Entry criteria:* (1) every feature in the baselined specification is coded, shown by the traceability matrix from requirements to RTL (26-01); (2) the verification plan is reviewed and its coverage model defined, shown by the coverage database (19-13); (3) synthesis and preliminary timing show the design can close at the target frequency, shown by the timing report with its worst negative slack and path count (19-10).
- *Exit criteria:* (1) change control is in force, so only bug fixes enter and each needs an approved change request; (2) every open issue from the review has an owner and a closing date; (3) the coverage-closure schedule to tape-out is agreed, with the remaining coverage holes listed.

### Solution 26-02.3

(a) The ratio is $C_r/(C_eNp) = 8{,}000/(5{,}000 \times 30 \times 0.50)$ = **0.1067**, so $k \le 1 + \ln 0.1067/\ln 0.5$ = **4.23**: the optimum is **4** reviewers.

(b) $1 - 0.5^4$ = **93.75**% found, **1.875** expected escapes, and a total of $4 \times 8{,}000 + 5{,}000 \times 1.875$ = **$41,375**.

(c) $C(k)$ for $k$ = 1 to 6: **$83,000**, **$53,500**, **$42,750**, **$41,375**, **$44,688** and **$50,344**. Three, four or five reviewers are all within **8.0**% of the optimum, so the choice among them can rest on who is available and how independent they are.

### Solution 26-02.4

With $P(k) = 0.60[1 - 0.4^k] + 0.25[1 - 0.8^k] + 0.15 \times 0$:

(a) One reviewer: $0.60 \times 0.6 + 0.25 \times 0.2$ = **0.410**.

(b) Three: **0.684**.

(c) Five: **0.762**; ten: **0.823**.

(d) As $k \to \infty$, $P \to 0.60 + 0.25$ = **0.85**: the invisible 15% is never found by reading.

(e) Four reviewers give **0.732** and five give 0.762, so **5** reach 75%. Three independent reviewers with the same single-reviewer rate of 0.41 would find $1 - 0.59^3$ = **0.795**, more than the 0.684 of (b): heterogeneity costs **0.111** of the defects at three reviewers.

### Solution 26-02.5

(a) Reviewer 1 found 15 of reviewer 2's 22: $\hat p_1$ = **0.682**; reviewer 2 found 15 of reviewer 1's 30: $\hat p_2$ = **0.500**.

(b) $\hat N = 30 \times 22/15$ = **44.0**; Chapman $31 \times 23/16 - 1$ = **43.6**.

(c) Found $30 + 22 - 15$ = **37**, so about **7.0** remain (**6.6** by Chapman), and more if the issues differ in difficulty.

### Solution 26-02.6

(a) Assume (1) $N$ defects, each found by reviewer $i$ with the same probability $p_i$; (2) the two reviewers search independently; (3) the document does not change between reviews. Then $n_1 \sim \text{Bin}(N, p_1)$, $n_2 \sim \text{Bin}(N, p_2)$ and, by independence, each defect is found by both with probability $p_1p_2$, so $E[m] = Np_1p_2$. Setting the counts equal to their expectations and solving the three equations for $N$, $p_1$ and $p_2$: $\hat p_2 = m/n_1$, $\hat p_1 = m/n_2$, and $\hat N = n_1/\hat p_1 = n_1n_2/m$.

(b) Chapman's $\hat N_C = (n_1 + 1)(n_2 + 1)/(m + 1) - 1$ has denominator at least 1, so it is finite for $m$ = 0, where Lincoln–Petersen divides by zero.

(c) $E[n_1] = E[n_2] = 20 \times 0.8 + 20 \times 0.2$ = **20**; $E[m] = 20 \times 0.8^2 + 20 \times 0.2^2$ = **13.6**; so $\hat N = 20 \times 20/13.6$ = **29.4**, **26.5**% below the true 40.

(d) Both reviewers find the easy defects, so the overlap is larger than independence at the *average* rate predicts ($40 \times 0.5^2$ = **10** for $p$ = 0.5 everywhere); a larger $m$ in the denominator makes $\hat N$ too small. Heterogeneous difficulty acts like positive correlation between the reviewers.

### Solution 26-02.7

(a) Return: $160/220$ = **72.7**%, below 75%, so the ballot cannot close yet; under the rules a first ballot may be extended until a 75% return is received, and fails only if that cannot be obtained [R-632]. Approval: $105/145$ = **72.4**%, also below 75%. Abstention: $15/160$ = **9.4**%, valid.

(b) Return $165/220$ = **75.0**%, which meets the rule; approval $110/150$ = **73.3**%, still short. It does not pass.

(c) It needs at least $0.75 \times 150$ = **112.5**, so **113** Approve votes: **3** Do Not Approve voters must change (resolving their comments is how that happens).

### Solution 26-02.8

(a) Return $170/200$ = **85.0**% ✓; approval $90/115$ = **78.3**% ✓; abstention $55/170$ = **32.4**% ≥ 30%, so the ballot is invalid despite its approval rate.

(b) Abstentions must stay below $0.30 \times 170$ = **51**, so at most **50**.

(c) Five abstainers become Do Not Approve: approval $90/120$ = **75.0**%, exactly the threshold, so the ballot passes, with no margin at all.

### Solution 26-02.9

(a) $40 \times 0.0025 \times 1{,}000$ = **$100** per laptop, **16.7** times the chip's price.

(b) $0.10 \times 6$ = **$0.60** per chip.

(c) $0.03 \times 1{,}000 \times 0.05$ = **$1.50** per laptop, out of an aggregate of **$30**.

### Solution 26-02.10

(a) A device-level royalty $r_dP_d$ is a fraction $r_dP_d/P_c$ of the chip's price, which is the equivalent chip-level rate $r_c$. It equals the whole chip price when $r_dP_d = P_c$, that is $r_d^* = P_c/P_d$.

(b) $r_d^* = 20/500$ = **4.0**%, and a 1% device royalty equals $r_c = 0.01 \times 500/20$ = **25**% of the chip's price.

(c) The royalty is a cost of 25% of the chip's price, so the gross margin falls from 55% to **30**% (before any price increase the supplier could pass on).

(d) If royalties are assessed on the smallest saleable compliant implementation (often the chip), the base is the component's own price, so the royalty scales with the value the supplier captures; if they are assessed on the end device, a component supplier can face royalties larger than its revenue. The IEEE policy names the smallest saleable compliant implementation as one optional consideration for a reasonable rate, alongside "another appropriate value level" [R-631]; how the base is chosen in practice is contested.

### Solution 26-02.11

(a) Gain $4 \times 3$ = **$12 M**; expected penalty $0.3 \times (2 + 1 \times 3)$ = **$1.5 M**; net **$10.5 M**.

(b) Expected penalty $0.3 \times (20 + 5 \times 3)$ = **$10.5 M**; net **$1.5 M**, barely positive.

(c) Break-even at $p = 12/(20 + 15)$ = **0.343**: with a respin as the fallback, a 30% chance of a late change nearly cancels the four months gained.

### Solution 26-02.12

(a) **Datasheet** (an absolute maximum rating, guaranteed). (b) **Application note** (guidance, not a guarantee). (c) **Errata**, listing the affected stepping and the workaround. (d) **Internal specification only** (implementation detail; publish it only if customers need it). (e) **Datasheet**, as a typical value with its workload and conditions, clearly separated from guaranteed limits.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 26-02.3a | ratio | 0.1067 | |
| 26-02.3a1 | marginal bound | 4.23 | |
| 26-02.3a2 | optimal reviewers | 4 | |
| 26-02.3b | fraction found | 93.75 | % |
| 26-02.3b1 | expected escapes | 1.875 | |
| 26-02.3b2 | total cost | 41375 | $ |
| 26-02.3c1 | cost, 1 | 83000 | $ |
| 26-02.3c2 | cost, 2 | 53500 | $ |
| 26-02.3c3 | cost, 3 | 42750 | $ |
| 26-02.3c4 | cost, 4 | 41375 | $ |
| 26-02.3c5 | cost, 5 | 44688 | $ |
| 26-02.3c6 | cost, 6 | 50344 | $ |
| 26-02.3c7 | worst excess, 3 to 5 | 8.0 | % |
| 26-02.4a | one reviewer | 0.410 | |
| 26-02.4b | three reviewers | 0.684 | |
| 26-02.4c | five reviewers | 0.762 | |
| 26-02.4c1 | ten reviewers | 0.823 | |
| 26-02.4d | limit | 0.85 | |
| 26-02.4e0 | four reviewers | 0.732 | |
| 26-02.4e | reviewers for 75% | 5 | |
| 26-02.4e1 | independent, three | 0.795 | |
| 26-02.4e2 | heterogeneity cost | 0.111 | |
| 26-02.5a | p1 | 0.682 | |
| 26-02.5a1 | p2 | 0.500 | |
| 26-02.5b | Lincoln-Petersen | 44.0 | |
| 26-02.5b1 | Chapman | 43.6 | |
| 26-02.5c | found | 37 | |
| 26-02.5c1 | remaining | 7.0 | |
| 26-02.5c2 | remaining, Chapman | 6.6 | |
| 26-02.6c | expected n1 | 20 | |
| 26-02.6c1 | expected m | 13.6 | |
| 26-02.6c2 | estimate | 29.4 | |
| 26-02.6c3 | relative error | 26.5 | % |
| 26-02.6d | overlap at uniform p | 10 | |
| 26-02.7a | return | 72.7 | % |
| 26-02.7a1 | approval | 72.4 | % |
| 26-02.7a2 | abstention | 9.4 | % |
| 26-02.7b | return | 75.0 | % |
| 26-02.7b1 | approval | 73.3 | % |
| 26-02.7c0 | 75% of votes cast | 112.5 | |
| 26-02.7c | approvals needed | 113 | |
| 26-02.7c1 | switches | 3 | |
| 26-02.8a | return | 85.0 | % |
| 26-02.8a1 | approval | 78.3 | % |
| 26-02.8a2 | abstention | 32.4 | % |
| 26-02.8b0 | 30% of returns | 51 | |
| 26-02.8b | maximum abstentions | 50 | |
| 26-02.8c | approval | 75.0 | % |
| 26-02.9a | stacked royalty | 100 | $ |
| 26-02.9a1 | multiple of chip price | 16.7 | |
| 26-02.9b | on chip | 0.60 | $ |
| 26-02.9c | holder's share | 1.50 | $ |
| 26-02.9c1 | aggregate | 30 | $ |
| 26-02.10b | break-even device rate | 4.0 | % |
| 26-02.10b1 | chip-level equivalent | 25 | % |
| 26-02.10c | gross margin after royalty | 30 | % |
| 26-02.11a | gain | 12 | $M |
| 26-02.11a1 | penalty, ECO | 1.5 | $M |
| 26-02.11a2 | net, ECO | 10.5 | $M |
| 26-02.11b | penalty, respin | 10.5 | $M |
| 26-02.11b1 | net, respin | 1.5 | $M |
| 26-02.11c | break-even probability | 0.343 | |
