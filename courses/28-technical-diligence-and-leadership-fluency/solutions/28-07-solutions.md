# Solutions 28-07 · Evaluating Engineering Teams

Problems: [28-07 problems](../problems/28-07-problems.md) · Chapter: [28-07](../chapters/28-07-evaluating-engineering-teams.md). Every number is recomputed by [verify_28_07.py](../verify/verify_28_07.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 28-07.1

- (a) **Strong:** a specific escape, the process gap that let it through, the change and evidence that it worked. Confirm with the waiver-review records and the C0 bug tracker.
- (b) **Evasive:** universal ownership is ownership by no one. Ask for named owners and seconds of each critical block (T2).
- (c) **Partial, leaning evasive:** an admission with an external excuse. Ask for the plan-to-actual ratio and how the foundry delay was handled in the plan.
- (d) **Strong:** a measured split plus dedicated engineers, consistent with industry practice [R-651]. Confirm with the time-tracking summary.

### Solution 28-07.2

1 of 3: $\hat\theta = (1.4 + 1)/(10 + 3)$ = **18.5**%; weight $3/13$ = **0.231**. 6 of 8: $(1.4 + 6)/18$ = **41.1**%; weight $8/18$ = **0.444**.

### Solution 28-07.3

2.5th percentile **14.7**%, 97.5th **60.9**%. The 95% interval just excludes the 2024 base rate of 14% (the posterior probability that $\theta$ exceeds 14% is about **98**%), but its lower end is close to it, so the evidence is strong yet sensitive to how much weight the prior carries: with a heavier prior the interval would include the base rate.

### Solution 28-07.4

$\mu = \tfrac13(\ln 1.15 + \ln 1.35 + \ln 1.50)$; $e^{\mu}$ = **1.325**; median $24 \times 1.325$ = **31.8** months; $s_{\ln}$ = **0.134**; plug-in $P = \Phi(-\mu/s_{\ln})$ = **1.76**%. Predictive: scale $0.1338\sqrt{1 + 1/3} = 0.1545$; $P = F_{t,2}(-0.2818/0.1545)$ = **10.5**%; $T_{90} = 24\exp(0.2818 + 1.886 \times 0.1545)$ = **42.6** months. With three projects and two degrees of freedom, the $t$ distribution's heavy tails admit both an on-time finish and a very late one far more readily than a normal with the sample spread treated as exact; the honest summary is "about 32 months, with wide uncertainty", which is a reason to check the outside view (28-07 §3.2).

### Solution 28-07.5

One year: **15**%, **2.25**%, **0.338**%. Three years ($q = 1 - 0.85^3 = 0.386$): **38.6**%, **14.9**%, **5.75**%.

### Solution 28-07.6

$q = 1 - 0.88^2 = 0.2256$; $1 - (1 - 0.2256)^4$ = **64.0**%.

### Solution 28-07.7

Weighted $0.3 \times 5 + 0.25 \times 4 + 0.25 \times 1 + 0.2 \times 4$ = **3.55**; geometric $5^{0.3}4^{0.25}1^{0.25}4^{0.2}$ = **3.02**. The gate **fails** (a score of 1). The weighted score looks healthy, the geometric score less so, and the gate catches the weakness both averages hide.

### Solution 28-07.8

Without: $40 \times 1.2 \times 0.65$ = **31.2** \$M; with: **38.4** \$M; gain **7.2** \$M. Break-even: $1/(40 \times 1.2)$ = **2.08** points of retention per \$1M.

### Solution 28-07.9

$3 \times 10^6 \times 0.25/(1000 \times 0.75)$ = 1000 h = **41.7** days.

### Solution 28-07.10

Verification $15 + 0.49 \times 40$ = **34.6** FTE; design $0.51 \times 40$ = **20.4** FTE; ratio **1.70**. The head-count ratio, 15/40 = 0.375, understates this team's verification effort ratio by a factor of **4.52**. Compare effort with effort: a team at the survey's one-to-one head count, with the same 49% split, would have an effort ratio of $(1 + 0.49)/0.51$ = **2.92**, so this team's 1.70 is still well below it.

### Solution 28-07.11

$20 \times 19/2$ = **190**; $30 \times 29/2$ = **435**; ratio **2.29**: 50% more people, more than twice the channels.

### Solution 28-07.12

(a) The posterior is proportional to the likelihood times the prior: $\theta^s(1 - \theta)^{n - s} \times \theta^{\alpha_0 - 1}(1 - \theta)^{\beta_0 - 1} = \theta^{\alpha_0 + s - 1}(1 - \theta)^{\beta_0 + n - s - 1}$, the kernel of $\text{Beta}(\alpha_0 + s, \beta_0 + n - s)$. Its mean is $(\alpha_0 + s)/(\alpha_0 + \beta_0 + n)$. With $n_0 = \alpha_0 + \beta_0$ and $\theta_0 = \alpha_0/n_0$, this is $[n_0\theta_0 + n(s/n)]/(n_0 + n)$, a weighted average with weights $n_0/(n_0 + n)$ and $n/(n_0 + n)$.

(b) $\ln x \sim N(\mu, \sigma^2)$, so $P(x \le 1) = P(\ln x \le 0) = \Phi[(0 - \mu)/\sigma] = \Phi(-\mu/\sigma)$. The 90th percentile of $\ln x$ is $\mu + z_{0.9}\sigma$, so $T_{90} = T_{\text{plan}}e^{\mu + z_{0.9}\sigma}$.

(c) The capability is lost if the group event happens (probability $c$), or if it does not and all $k$ leave independently: $P = c + (1 - c)q'^k$. For $c = 0.05$, $q' = 0.2$: $k = 1$, **24.0**%; $k = 2$, **8.80**%; $k = 3$, **5.76**%, against 20%, 4% and 0.8% without the group event. However many owners there are, the risk never falls below $c$: redundancy inside one team does not protect against the team leaving together, which is why retention plans target groups as well as individuals.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 28-07.2a | posterior mean, 1 of 3 | 18.5 | % |
| 28-07.2b | weight, 1 of 3 | 0.231 | — |
| 28-07.2c | posterior mean, 6 of 8 | 41.1 | % |
| 28-07.2d | weight, 6 of 8 | 0.444 | — |
| 28-07.3a | 2.5th percentile | 14.7 | % |
| 28-07.3b | 97.5th percentile | 60.9 | % |
| 28-07.3c | posterior probability above 14% | 98 | % |
| 28-07.4a | geometric mean overrun | 1.325 | — |
| 28-07.4b | median duration | 31.8 | months |
| 28-07.4c | standard deviation of log-ratios | 0.134 | — |
| 28-07.4d | probability of meeting plan, plug-in | 1.76 | % |
| 28-07.4e | probability of meeting plan, t predictive | 10.5 | % |
| 28-07.4f | P90 duration, t predictive | 42.6 | months |
| 28-07.5a | one year, one owner | 15 | % |
| 28-07.5b | one year, two owners | 2.25 | % |
| 28-07.5c | one year, three owners | 0.338 | % |
| 28-07.5d | three years, one owner | 38.6 | % |
| 28-07.5e | three years, two owners | 14.9 | % |
| 28-07.5f | three years, three owners | 5.75 | % |
| 28-07.6 | four single-owner capabilities, two years | 64.0 | % |
| 28-07.7a | weighted score | 3.55 | — |
| 28-07.7b | geometric score | 3.02 | — |
| 28-07.8a | retained value, no package | 31.2 | $M |
| 28-07.8b | retained value, package | 38.4 | $M |
| 28-07.8c | gain | 7.2 | $M |
| 28-07.8d | break-even retention gain per $1M | 2.08 | points |
| 28-07.9 | regression time | 41.7 | days |
| 28-07.10a | verification effort | 34.6 | FTE |
| 28-07.10b | design effort | 20.4 | FTE |
| 28-07.10c | ratio | 1.70 | — |
| 28-07.10d | effort ratio over head-count ratio | 4.52 | — |
| 28-07.10e | effort ratio at one-to-one heads | 2.92 | — |
| 28-07.11a | channels, 20 people | 190 | — |
| 28-07.11b | channels, 30 people | 435 | — |
| 28-07.11c | ratio | 2.29 | — |
| 28-07.12a | group-event model, one owner | 24.0 | % |
| 28-07.12b | group-event model, two owners | 8.80 | % |
| 28-07.12c | group-event model, three owners | 5.76 | % |
