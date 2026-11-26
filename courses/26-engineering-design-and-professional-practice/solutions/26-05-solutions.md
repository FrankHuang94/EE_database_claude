# Solutions 26-05 · Schedule and Risk: Why Respins Happen

Problems: [26-05 problems](../problems/26-05-problems.md) · Chapter: [26-05](../chapters/26-05-schedule-and-respin-risk.md). Every number is recomputed by [verify_26_05.py](../verify/verify_26_05.py).

---

## Solutions

### Solution 26-05.1

$\mu = (6 + 32 + 16)/6$ = **9.0** weeks; $\sigma = 10/6$ = **1.67** weeks; $P(D \le 10) = \Phi(1.0/1.67) = \Phi(0.60)$ = **0.726**.

### Solution 26-05.2

(a) **Workaround**: firmware or the boot code writes the correct value after reset.

(b) **Metal-only ECO**: rewire nearby spare cells to add the missing logic.

(c) **Full respin**: transistor sizes are set by the base layers, which no metal change can alter (raising the minimum supply voltage, at a power cost, might serve as a stopgap).

(d) **Trim**: set the bandwidth trim bits at test or in firmware.

(e) **Workaround** (microcode or software mitigation), as with Zenbleed [R-321]; the next stepping fixes it in hardware.

### Solution 26-05.3

(a) Means **4.33**, **8.50** and **3.33** weeks; standard deviations **0.667**, **1.17** and **0.667** weeks.

(b) $\mu$ = **16.17** weeks; $\sigma = \sqrt{0.667^2 + 1.17^2 + 0.667^2}$ = **1.50** weeks.

(c) $\Phi((17 - 16.17)/1.50)$ = **0.711**.

(d) $16.17 + 1.645 \times 1.50$ = **18.6** weeks.

### Solution 26-05.4

(a) $0.9^4$ = **0.656**.

(b) $0.9^{1/4}$ = **0.974**.

(c) That needs $z = \Phi^{-1}(0.974)$ = **1.94** instead of $\Phi^{-1}(0.90)$ = **1.28**, so each path's date must move **0.66** of its standard deviation later, or each path must be made that much more predictable.

### Solution 26-05.5

(a) $E[N] = 1 + 0.6 + 0.6 \times 0.2$ = **1.72**.

(b) $0.6 \times 0.2$ = **0.120**.

(c) Delay $0.72 \times 16$ = **11.5** weeks; cost $0.72 \times 15$ = **$10.8 M**.

### Solution 26-05.6

$E[N] = 1 + (1 - q_1) + (1 - q_1)(0.4)$:

(a) **2.20**; (b) **2.33**; (c) **1.98**.

(d) A sixfold change in first-spin success (0.05 to 0.30) moves the expected number of tape-outs only from 2.33 to 1.98, because the later spins are good. What matters for planning is the second spin, and that depends on how quickly bring-up finds the problems and on the fixes the design allows (spare cells, configuration bits).

### Solution 26-05.7

(a) Full: $90 \times 1.4$ = **126** days = **18.0** weeks. ECO: $30 \times 1.4$ = **42** days = **6.0** weeks.

(b) Full respin: $18 + 5$ = **23.0** weeks, $25 + 4 + 23 \times 2$ = **$75.0 M**. ECO: $6 + 3$ = **9.0** weeks, $6 + 1.5 + 9 \times 2$ = **$25.5 M**.

(c) **$49.5 M** and **14.0** weeks.

### Solution 26-05.8

(a) $0.3 \times 12 + 0.1 \times 50 + 0.4 \times 4 = 3.6 + 5.0 + 1.6$ = **$10.2 M**.

(b) R1: $0.2 \times 12 - 1.5$ = **$0.90 M**; R2: $0.06 \times 50 - 2.5$ = **$0.50 M**; R3: $0.2 \times 4 - 0.5$ = **$0.30 M**.

(c) With $3 M: R1 and R3 ($2.0 M, net **$1.20 M**); R1 and R2 ($4.0 M) do not fit. With $4.5 M: all three fit ($4.5 M, net **$1.70 M**).

### Solution 26-05.9

(a) $2 \times 0.2 \times 10$ = **$4.0 M** in both cases.

(b) Independent: $P(\text{lose } 20) = 0.2^2$ = **0.04**; variance $2 \times 10^2 \times 0.2 \times 0.8 = 32$, standard deviation **$5.66 M**.

(c) Always together: $P(\text{lose } 20)$ = **0.20**; the loss is 20 with probability 0.2, variance $20^2 \times 0.2 \times 0.8 = 64$, standard deviation **$8.0 M**.

(d) EMV is the same, but the chance of the worst case is five times higher and the spread larger. Correlated risks (a common cause such as an understaffed team or an immature node) need to be identified and managed as one exposure.

### Solution 26-05.10

(a) $P_{miss} = \Phi(-\Delta/4)$ and $f(\Delta) = 0.5\Delta + 40P_{miss}$:

| $\Delta$ | $P_{miss}$ | $f$ ($ M) |
|---|---|---|
| 0 | **0.500** | **20.0** |
| 4% | **0.159** | **8.35** |
| 8% | **0.0228** | **4.91** |

(b) $f'(\Delta) = 0.5 - (40/4)\varphi(\Delta/4) = 0$, where $\varphi$ is the standard normal density, so $\varphi(z) = 0.05$ with $z = \Delta/4$. Then $z = \sqrt{-2\ln(0.05\sqrt{2\pi})}$ = **2.04**, $\Delta^*$ = **8.15**%, $P_{miss}$ = **0.0208** and $f$ = **$4.91 M** (to three figures the same as at 8%: the optimum is flat). $f''$ is positive there, so it is a minimum.

### Solution 26-05.11

(a) $k = 1 \times 5/30$ = **0.167**; $\lambda^*$ = **0.204**.

(b) $t^* = 5\ln(0.2 \times 60/0.204)$ = **20.4** weeks.

(c) $P_r$ = **0.185**; $f = 20.4 + 30 \times 0.185$ = **$25.9 M**.

(d) With $\lambda$ = 12 a respin is all but certain: **$30.0 M**. Verifying to the optimum saves **$4.1 M**; the slower discovery ($\tau$ = 5) makes the optimum later than in Example 26-05.5.

### Solution 26-05.12

(a) $\lambda^*$ is unchanged (0.179, since $k$ is unchanged), so $t^* = 4\ln(5/0.179)$ = **13.3** weeks and $P_r$ = **0.164**.

(b) $f = 2 + 1.5 \times 13.3 + 40 \times 0.164$ = **$28.5 M**, against $30.7 M without it: worth doing.

(c) The optimum is set by $\lambda e^{-\lambda} = c_w\tau/C_r$, which does not involve $N_0$: whatever the starting point, the team stops when the expected escapes reach the same $\lambda^*$. Halving the starting escapes reaches that point $\tau\ln 2$ = **2.77** weeks sooner.

### Solution 26-05.13

Any three of: (1) the survey counts spins before production, and as far as its published material shows it does not separate planned steppings and quick metal ECOs from forced fixes (our reading), so "not first-time success" often means an A1 or B0 stepping, not an unusable chip; (2) first silicon is usually good enough for bring-up, software development and customer sampling even when a respin follows; (3) the respondents are self-selected, the sponsor sells verification tools, and the recruitment method changed between studies [R-018, R-321]; (4) the figure is about projects reaching production without a respin, not about whether the program eventually succeeds.

### Solution 26-05.14

(a) Forward pass (ES–EF): A 0–4; B 4–14; C 4–10; D starts at the later of B and C, 14–22; E 14–21; F starts at the later of D and E, 22–25. The project takes **25** weeks.

(b) Backward pass from 25 (LS–LF): F 22–25; D 14–22; E 15–22; B must finish by the earlier of D's and E's latest starts, 14, so 4–14; C must finish by 14, so 8–14; A 0–4. Total float (LS − ES): A 0, B 0, C **4**, D 0, E **1**, F 0. The critical path is A–B–D–F (4 + 10 + 8 + 3 = 25 weeks); A–B–E–F is one week shorter and A–C–D–F four weeks shorter.

(c) E has 1 week of float, so a 2-week slip delays the project by **1** week, to 26: A–B–E–F becomes the critical path.

(d) Every path must fall to 23 weeks or less: A–B–D–F (25) needs 2 weeks and A–B–E–F (24) needs 1. Shortening A, B or F by 2 weeks cuts both paths at once and gives 23. Shortening only D by 2 weeks brings A–B–D–F to 23 but leaves A–B–E–F at **24** weeks: the near-critical path becomes critical. This is the network form of merge bias: compressing one path exposes the next.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 26-05.1a | mean | 9.0 | weeks |
| 26-05.1a1 | standard deviation | 1.67 | weeks |
| 26-05.1a2 | P within 10 weeks | 0.726 | |
| 26-05.1a3 | z | 0.60 | |
| 26-05.3a | floorplan mean | 4.33 | weeks |
| 26-05.3a1 | place-and-route mean | 8.50 | weeks |
| 26-05.3a2 | signoff mean | 3.33 | weeks |
| 26-05.3a3 | floorplan sd | 0.667 | weeks |
| 26-05.3a4 | place-and-route sd | 1.17 | weeks |
| 26-05.3a5 | signoff sd | 0.667 | weeks |
| 26-05.3b | path mean | 16.17 | weeks |
| 26-05.3b1 | path sd | 1.50 | weeks |
| 26-05.3c | P within 17 weeks | 0.711 | |
| 26-05.3d | 95% date | 18.6 | weeks |
| 26-05.4a | joint chance | 0.656 | |
| 26-05.4b | required per path | 0.974 | |
| 26-05.4c | z required | 1.94 | |
| 26-05.4c1 | z at 90% | 1.28 | |
| 26-05.4c2 | shift | 0.66 | sd |
| 26-05.5a | expected tape-outs | 1.72 | |
| 26-05.5b | P(three) | 0.120 | |
| 26-05.5c | expected delay | 11.5 | weeks |
| 26-05.5c1 | expected cost | 10.8 | $M |
| 26-05.6a | E[N], 0.14 | 2.20 | |
| 26-05.6b | E[N], 0.05 | 2.33 | |
| 26-05.6c | E[N], 0.30 | 1.98 | |
| 26-05.7a | full fab days | 126 | days |
| 26-05.7a1 | full fab weeks | 18.0 | weeks |
| 26-05.7a2 | ECO fab days | 42 | days |
| 26-05.7a3 | ECO fab weeks | 6.0 | weeks |
| 26-05.7b | full delay | 23.0 | weeks |
| 26-05.7b1 | full cost | 75.0 | $M |
| 26-05.7b2 | ECO delay | 9.0 | weeks |
| 26-05.7b3 | ECO cost | 25.5 | $M |
| 26-05.7c | saving | 49.5 | $M |
| 26-05.7c1 | weeks saved | 14.0 | weeks |
| 26-05.8a | EMV | 10.2 | $M |
| 26-05.8b | R1 net | 0.90 | $M |
| 26-05.8b1 | R2 net | 0.50 | $M |
| 26-05.8b2 | R3 net | 0.30 | $M |
| 26-05.8c | net, $3 M | 1.20 | $M |
| 26-05.8c1 | spend, $3 M | 2.0 | $M |
| 26-05.8c2 | net, $4.5 M | 1.70 | $M |
| 26-05.9a | EMV | 4.0 | $M |
| 26-05.9b | P(20), independent | 0.04 | |
| 26-05.9b1 | sd, independent | 5.66 | $M |
| 26-05.9c | P(20), correlated | 0.20 | |
| 26-05.9c1 | sd, correlated | 8.0 | $M |
| 26-05.10a | miss at 0 | 0.500 | |
| 26-05.10a1 | cost at 0 | 20.0 | $M |
| 26-05.10a2 | miss at 4% | 0.159 | |
| 26-05.10a3 | cost at 4% | 8.35 | $M |
| 26-05.10a4 | miss at 8% | 0.0228 | |
| 26-05.10a5 | cost at 8% | 4.91 | $M |
| 26-05.10b | z at optimum | 2.04 | |
| 26-05.10b1 | optimal margin | 8.15 | % |
| 26-05.10b2 | miss at optimum | 0.0208 | |
| 26-05.10b3 | cost at optimum | 4.91 | $M |
| 26-05.11a | k | 0.167 | |
| 26-05.11a1 | lambda at optimum | 0.204 | |
| 26-05.11b | optimal time | 20.4 | weeks |
| 26-05.11c | respin probability | 0.185 | |
| 26-05.11c1 | expected cost | 25.9 | $M |
| 26-05.11d | cost at once | 30.0 | $M |
| 26-05.11d1 | saving from verifying | 4.1 | $M |
| 26-05.12a | optimal time | 13.3 | weeks |
| 26-05.12a1 | respin probability | 0.164 | |
| 26-05.12b | expected cost | 28.5 | $M |
| 26-05.12c | time saved | 2.77 | weeks |
| 26-05.14a | project duration | 25 | weeks |
| 26-05.14b | float of C | 4 | weeks |
| 26-05.14b1 | float of E | 1 | weeks |
| 26-05.14c | project slip | 1 | weeks |
| 26-05.14d | A-B-E-F after shortening D | 24 | weeks |
