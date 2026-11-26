# Solutions 28-01 · A Framework for Evaluating a Chip Company's Technology

Problems: [28-01 problems](../problems/28-01-problems.md) · Chapter: [28-01](../chapters/28-01-technology-evaluation-framework.md). Every number is recomputed by [verify_28_01.py](../verify/verify_28_01.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 28-01.1

- (a) **IP position, strong.** Counsel's freedom-to-operate opinion is an examined artefact, with professional liability behind it.
- (b) **Architecture, weak.** A peak-efficiency comparison chosen by the target; a failing team can produce the same slide (28-02 shows how to check it).
- (c) **Manufacturing and supply, strong.** A written allocation from the supplier is the evidence a ramp depends on.
- (d) **Ecosystem and software, strong.** Release cadence and the issue list show what customers actually experience.
- (e) **Implementation (and manufacturing), strong.** Lot-level yield on a named stepping is measured on silicon.
- (f) **Team, weak.** A résumé describes one person's past; the team's tape-out record and depth are the evidence (28-07).

### Solution 28-01.2

Arithmetic: X $= 0.3 \times 5 + 0.3 \times 5 + 0.2 \times 1 + 0.2 \times 4$ = **4.0**; Y $= 1.2 + 1.2 + 0.6 + 0.7$ = **3.7**. Geometric: $G_X = 5^{0.6} \times 1^{0.2} \times 4^{0.2}$ = **3.47**; $G_Y = 4^{0.6} \times 3^{0.2} \times 3.5^{0.2}$ = **3.68**.

X leads on the arithmetic score and Y on the geometric one. X's single score of 1 is fully offset by its two 5s in the sum, but in the product $1^{0.2}$ contributes nothing, so the geometric score treats the weakness as unrecoverable.

### Solution 28-01.3

(a) **No.** A score of 1 is below the gate of 2, so X is not investable as it stands, whatever its weighted totals. The scores of Problem 28-01.2 describe a company the buyer cannot own on these terms.

(b) With an IP score of 3: arithmetic $0.3 \times 5 + 0.3 \times 5 + 0.2 \times 3 + 0.2 \times 4$ = **4.4**; geometric $5^{0.6} \times 3^{0.2} \times 4^{0.2}$ = **4.32**. The closing condition turns X from uninvestable into the clear leader under either form, which is why gates are better handled by structure than by scores.

### Solution 28-01.4

(a) $\operatorname{Var}(S_X) = 0.3^2 \times 1.0^2 + 0.3^2 \times 0.5^2 + 0.2^2 \times 0.5^2 + 0.2^2 \times 0.3^2 = 0.0900 + 0.0225 + 0.0100 + 0.0036$ = **0.126**, so the standard deviation is **0.355**. The first dimension contributes $0.09/0.1261$ = **71.4**% of the variance.

(b) With $\sigma_1 = 0.4$ the first term becomes $0.09 \times 0.16 = 0.0144$: variance **0.0505**, standard deviation **0.225**. One deep-dive removes more than half the variance.

### Solution 28-01.5

(a) $\operatorname{Var}(S_Y) = 0.4^2 \times (0.09 + 0.09 + 0.04 + 0.04)$ = **0.0416**. $\sigma_D = \sqrt{0.1261 + 0.0416}$ = **0.410**, and $P(D < 0) = \Phi(-0.3/0.410)$ = **23.2**%.

(b) The correlated terms add $2\rho\sum_{i<j}w_iw_j\sigma_i\sigma_j$. With $w_i\sigma_i = 0.30, 0.15, 0.10, 0.06$, the pairwise products sum to $0.045 + 0.030 + 0.018 + 0.015 + 0.009 + 0.006 = 0.123$, so $\operatorname{Var}(S_X) = 0.1261 + 1.2 \times 0.123$ = **0.274**. Then $\sigma_D$ = **0.562** and the probability that Y is ahead rises to **29.7**%. A halo makes X's lead look safer than it is.

### Solution 28-01.6

Prior odds $0.3/0.7$ = **0.429**. Posterior odds $0.429 \times 2 \times 5 \times 0.5$ = **2.14**, probability $2.14/3.14$ = **68.2**%. The sandbox test, run by the buyer on the buyer's models, carries most of the weight; the customer's hand-written kernels pull the other way and deserve a follow-up question (why do they still need them?).

### Solution 28-01.7

Counted as independent, the odds become $2.14 \times 5$ = **10.7** and the probability **91.5**%. With the conditional likelihood ratio of 1.2, the odds are $2.14 \times 1.2$ = **2.57** and the probability **72.0**%. Repeating a test on the same inputs mostly re-observes the first result; it guards against a mistake in running the test, not against the claim being false.

### Solution 28-01.8

From 10% to 50%: $(0.5/0.5)/(0.1/0.9)$ = **9**. From 10% to 90%: $(0.9/0.1)/(0.1/0.9)$ = **81**. Signals with a ratio of 3 reach 81 after $\ln 81/\ln 3$ = **4** of them, if they are truly independent. A claim with a low prior needs either several independent pieces of evidence or one very strong one.

### Solution 28-01.9

The plan holds with probability $(14 + 25 + 28)/97$ = **69.1**%. Expected spins beyond plan: $(1 \times 16 + 2 \times 10 + 3 \times 4)/97 = 48/97$ = **0.495**. Expected delay $0.495 \times 5$ = **2.47** months and extra cost $0.495 \times 30$ = **14.8** million dollars. Budgeting the median number of spins (three) rather than two cuts the expected spins beyond plan by more than half compared with Example 28-01.4.

### Solution 28-01.10

$P = 0.8 \times 0.5 \times 0.9 \times 0.6$ = **0.216**. Expected value $0.216 \times 1.2 + 0.784 \times 0.1$ = **0.338** billion dollars. The chain fails at the silicon stage with probability $0.8 \times (1 - 0.5)$ = **0.40**, the largest single failure mode, so the silicon evidence of 28-02 and 28-03 deserves the most diligence.

### Solution 28-01.11

(a) $1.12^3$ = **1.405**. Seller: $0.7 \times 400/1.405$ = **199.3**, total **799.3** million dollars. Buyer: $0.3 \times 400/1.405$ = **85.4**, total **685.4** million dollars.

(b) The seller values the earn-out deal at \$799.3 million against \$700 million in cash and prefers the earn-out; the buyer values it at \$685.4 million against \$700 million and also prefers the earn-out. Both sides prefer the same structure.

(c) The gap, $199.3 - 85.4$ = **113.9** million dollars, is value created by disagreement about the probability: each side prices the contingent payment at its own belief. It is real only if both cannot be right; whoever is wrong about the technology bears the cost, which is why the milestone definitions (what counts as revenue, by when, under whose control) are negotiated as hard as the price.

### Solution 28-01.12

**Prior 0.9.** Buying now is worth $0.9 \times 500 - 0.1 \times 200$ = **430** million dollars; EVPI $= 0.9 \times 500 - 430$ = **20** million dollars. $P(\text{pass}) = 0.72 + 0.01$ = **0.73**. After a fail, $P(\text{works} \mid \text{fail}) = 0.18/0.27$ = **0.667** and buying is still worth $0.667 \times 500 - 0.333 \times 200$ = **266.7** million dollars, so the buyer buys whatever the result: EVSI = **0**.

**Prior 0.2.** Buying now is worth $0.2 \times 500 - 0.8 \times 200$ = **−60** million dollars, so pass; EVPI $= 0.2 \times 500 - 0$ = **100** million dollars. $P(\text{pass}) = 0.16 + 0.08$ = **0.24**, $P(\text{works} \mid \text{pass}) = 0.16/0.24$ = **0.667**, and buying after a pass is worth **266.7** million dollars. EVSI $= 0.24 \times 266.7$ = **64.0** million dollars.

A test is valuable only when one of its results would change the decision. At a prior of 0.9 no result does; at 0.2 a pass turns "pass" into "buy", so the test is worth almost two-thirds of perfect information.

### Solution 28-01.13

(a) $150/3.0$ = **50** months.

(b) $24 \times 3.0 + 2 \times 45$ = **162** million dollars, a shortfall of **12** million dollars.

(c) With a \$20 million respin: \$182 million, a shortfall of **32** million dollars.

(d) After both NREs, $150 - 90 = 60$ million dollars lasts **20** months, less than the 24-month plan.

The plan is not fundable from current cash even if everything works the first time. The question to ask is where the rest comes from (a committed next round, a customer's NRE payment, a design-services partner), and whether the second chip reuses enough of the first to cost far less than \$45 million.

### Solution 28-01.14

(a) Bayes' rule gives $P(T \mid E) = P(E \mid T)P(T)/P(E)$ and $P(\bar T \mid E) = P(E \mid \bar T)P(\bar T)/P(E)$. Dividing, $P(E)$ cancels:

$$
\frac{P(T \mid E)}{P(\bar T \mid E)} = \frac{P(E \mid T)}{P(E \mid \bar T)}\cdot\frac{P(T)}{P(\bar T)}, \qquad O(T \mid E) = \Lambda\,O(T).
$$

For $E_1, \dots, E_m$ conditionally independent given $T$ and given $\bar T$, $P(E_1, \dots, E_m \mid T) = \prod_k P(E_k \mid T)$ and likewise for $\bar T$, so the joint likelihood ratio is $\prod_k \Lambda_k$. Taking logarithms, $\ln O(T \mid E_1, \dots, E_m) = \ln O(T) + \sum_k \ln \Lambda_k$: the weights of evidence add.

(b) With $w_i = 1/n$, the variance formula of §3.2 gives

$$
\operatorname{Var}(S) = \sum_i \frac{\sigma^2}{n^2} + 2\sum_{i<j}\frac{\rho\sigma^2}{n^2} = \frac{\sigma^2}{n^2}\left[n + n(n - 1)\rho\right] = \frac{\sigma^2}{n}\left[1 + (n - 1)\rho\right],
$$

because there are $n(n - 1)/2$ pairs. As $n \to \infty$ it tends to $\rho\sigma^2$, not to zero. For $n = 7$ and $\sigma = 0.5$: at $\rho = 0$ the variance is **0.0357** and the standard deviation **0.189**; at $\rho = 0.5$ the variance is **0.143** and the standard deviation **0.378**; the limit is $\rho\sigma^2$ = **0.125**, a standard deviation of **0.354**. Adding dimensions averages away independent errors but not a shared one: a halo can only be removed by independent evidence (different people, different artefacts), not by a longer scorecard.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 28-01.2a | X arithmetic score | 4.0 | — |
| 28-01.2b | Y arithmetic score | 3.7 | — |
| 28-01.2c | X geometric score | 3.47 | — |
| 28-01.2d | Y geometric score | 3.68 | — |
| 28-01.3a | X arithmetic score with IP 3 | 4.4 | — |
| 28-01.3b | X geometric score with IP 3 | 4.32 | — |
| 28-01.4a | variance of X's score | 0.126 | — |
| 28-01.4b | standard deviation of X's score | 0.355 | — |
| 28-01.4c | first dimension's share | 71.4 | % |
| 28-01.4d | variance after the deep-dive | 0.0505 | — |
| 28-01.4e | standard deviation after the deep-dive | 0.225 | — |
| 28-01.5a | variance of Y's score | 0.0416 | — |
| 28-01.5b | standard deviation of the difference | 0.410 | — |
| 28-01.5c | probability Y is ahead | 23.2 | % |
| 28-01.5d | sum of pairwise products | 0.123 | — |
| 28-01.5e | variance of X's score with halo | 0.274 | — |
| 28-01.5f | standard deviation with halo | 0.562 | — |
| 28-01.5g | probability Y is ahead with halo | 29.7 | % |
| 28-01.6a | prior odds | 0.429 | — |
| 28-01.6b | posterior odds | 2.14 | — |
| 28-01.6c | posterior probability | 68.2 | % |
| 28-01.7a | odds, double-counted | 10.7 | — |
| 28-01.7b | probability, double-counted | 91.5 | % |
| 28-01.7c | odds, conditional ratio 1.2 | 2.57 | — |
| 28-01.7d | probability, conditional ratio 1.2 | 72.0 | % |
| 28-01.8a | ratio from 10% to 50% | 9 | — |
| 28-01.8b | ratio from 10% to 90% | 81 | — |
| 28-01.8c | signals of ratio 3 | 4 | — |
| 28-01.9a | probability the plan holds | 69.1 | % |
| 28-01.9b | expected spins beyond plan | 0.495 | spins |
| 28-01.9c | expected delay | 2.47 | months |
| 28-01.9d | expected extra cost | 14.8 | million $ |
| 28-01.10a | chain probability | 0.216 | — |
| 28-01.10b | expected value | 0.338 | billion $ |
| 28-01.10c | failure at the silicon stage | 0.40 | — |
| 28-01.11a | discount factor | 1.405 | — |
| 28-01.11b | seller's earn-out value | 199.3 | million $ |
| 28-01.11c | seller's total | 799.3 | million $ |
| 28-01.11d | buyer's earn-out value | 85.4 | million $ |
| 28-01.11e | buyer's total | 685.4 | million $ |
| 28-01.11f | valuation gap | 113.9 | million $ |
| 28-01.12a | value now, prior 0.9 | 430 | million $ |
| 28-01.12b | EVPI, prior 0.9 | 20 | million $ |
| 28-01.12c | P(pass), prior 0.9 | 0.73 | — |
| 28-01.12d | P(works given fail), prior 0.9 | 0.667 | — |
| 28-01.12e | value after a fail, prior 0.9 | 266.7 | million $ |
| 28-01.12f | EVSI, prior 0.9 | 0 | million $ |
| 28-01.12g | value now, prior 0.2 | -60 | million $ |
| 28-01.12h | EVPI, prior 0.2 | 100 | million $ |
| 28-01.12i | P(pass), prior 0.2 | 0.24 | — |
| 28-01.12j | P(works given pass), prior 0.2 | 0.667 | — |
| 28-01.12k | value after a pass, prior 0.2 | 266.7 | million $ |
| 28-01.12l | EVSI, prior 0.2 | 64.0 | million $ |
| 28-01.13a | runway without NRE | 50 | months |
| 28-01.13b | cash needed | 162 | million $ |
| 28-01.13c | shortfall | 12 | million $ |
| 28-01.13d | shortfall with a respin | 32 | million $ |
| 28-01.13e | runway after both NREs | 20 | months |
| 28-01.14a | variance, uncorrelated | 0.0357 | — |
| 28-01.14b | standard deviation, uncorrelated | 0.189 | — |
| 28-01.14c | variance, correlated | 0.143 | — |
| 28-01.14d | standard deviation, correlated | 0.378 | — |
| 28-01.14e | limiting variance | 0.125 | — |
| 28-01.14f | limiting standard deviation | 0.354 | — |
