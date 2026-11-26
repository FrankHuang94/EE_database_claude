# Solutions 28-03 · Maturity Scales for Silicon

Problems: [28-03 problems](../problems/28-03-problems.md) · Chapter: [28-03](../chapters/28-03-silicon-maturity-scales.md). Every number is recomputed by [verify_28_03.py](../verify/verify_28_03.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 28-03.1

- (a) **L1**, architecture and RTL. Confirm with the verification plan, the coverage database and the bug-discovery trend; coverage alone does not show the plan is complete.
- (b) **L3**, first silicon in bring-up. Ask which parts of the plan passed, why only at nominal voltage, and what the corner results are.
- (c) **L5** for that stepping, if the report is to a named revision of AEC-Q100 and the tests ran on B1 silicon.
- (d) **L6 moving to L7**, production release with volume; confirm with shipment and yield data and the qualification of both assembly sites.

### Solution 28-03.2

A breadboard tested in a realistic simulated environment is **TRL 5**; in the silicon scale, closest to a tape-out (L2), with verified RTL on emulation (L1) a step below at TRL 4. A fully functional prototype is **TRL 6**; closest to first silicon once bring-up has shown it works (late L3, the table's 5–6). "Flight qualified", ready for implementation, is **TRL 8**; closest to a completed qualification and release (L5–L6) [R-701]. The mapping is an analogy: silicon has no single "space environment" test, and a chip's TRL 7 is closest to engineering samples running in customers' systems.

### Solution 28-03.3

$P = 0.80 \times 0.85 \times 0.95$ = **0.646**; $T = 6 + 5 + 2$ = **13.0** months; multiplier $0.646/1.15^{13/12}$ = **0.555**.

### Solution 28-03.4

Discount factor $1.15^{2/12}$ = **1.024**; multiplier $0.95/1.024$ = **0.928**. Against the tape-out multiplier of 0.501 (Example 28-03.2), the ratio is **1.85**: a buyer could pay up to 1.85 times as much for the qualified program, other things equal.

### Solution 28-03.5

With $T_{\text{use}} = 343.15$ K and $T_{\text{stress}} = 398.15$ K: at 0.7 eV, $\text{AF} = \exp[8123 \times (1/343.15 - 1/398.15)]$ = **26.3**; at 0.9 eV, **67.0**. A smaller stress-to-use temperature gap gives much less acceleration than Example 28-03.3's 77.6, even at 0.9 eV.

### Solution 28-03.6

$\lambda_{60} = 1.833/(2 \times 462 \times 1000 \times 26.3) \times 10^9$ = **75.4** FIT. Doubling the sample halves the bound, but the higher use temperature (70 °C instead of 55 °C) cuts the acceleration factor by about three times, so the bound is still higher than Example 28-03.3's.

### Solution 28-03.7

With one failure, $\chi^2_{0.6;4} = 4.045$, so $\lambda_{60} = 4.045/(2 \times 462 \times 1000 \times 26.3) \times 10^9$ = **166** FIT.

### Solution 28-03.8

$\text{AF} = 77.65$ (carried unrounded) and $\chi^2_{0.9;2} = 4.605$, so $n \ge 4.605 \times 10^9/(2 \times 5 \times 1000 \times 77.65) = 5931.0$, that is **5932** devices. A 5 FIT claim at 90% confidence from a single product's qualification is a large program; such claims usually pool data across products on the same process.

### Solution 28-03.9

$e^{-8b} = 256/160 - 1 = 0.6$, so $b = -\ln 0.6/8$ = **0.0639** per week and $a = 160/0.4$ = **400**. At week 16: remaining $400 \times 0.36$ = **144**; rate $400 \times 0.0639 \times 0.36$ = **9.19** per week.

### Solution 28-03.10

$t^* = \ln(400 \times 0.0639/2)/0.0639$ = **39.9** weeks, **23.9** weeks after week 16; remaining then $2/0.0639$ = **31.3** defects.

### Solution 28-03.11

(a) **Grade 1**. (b) **Grade 0**. (c) Test A4 for Grade 1: −55 °C to +150 °C for **1000** cycles (or equivalent; −65 °C to 150 °C for 500 cycles is also allowed for legacy use) [R-612].

### Solution 28-03.12

(a) With a constant rate, failures in $T_{\text{eq}}$ are Poisson with mean $\lambda T_{\text{eq}}$, so $P(0) = e^{-\lambda T_{\text{eq}}}$, which falls as $\lambda$ rises. The upper bound at confidence $C$ is the $\lambda$ at which observing zero failures would have probability $1 - C$: $e^{-\lambda_C T_{\text{eq}}} = 1 - C$, so $\lambda_C = -\ln(1 - C)/T_{\text{eq}}$. The chi-square distribution with 2 degrees of freedom has $F(x) = 1 - e^{-x/2}$; its $C$ quantile solves $1 - e^{-x/2} = C$, giving $\chi^2_{C;2} = -2\ln(1 - C)$. Hence $\lambda_C = \chi^2_{C;2}/(2T_{\text{eq}})$.

(b) $m(t_1) = a(1 - x)$ and $m(2t_1) = a(1 - x^2) = a(1 - x)(1 + x)$ with $x = e^{-bt_1}$. Their ratio is $1 + x$, so $x = m_2/m_1 - 1$, $b = -\ln x/t_1$ and $a = m_1/(1 - x)$. The discovery rate is $\lambda(t) = ab\,e^{-bt}$ and the remaining count is $a\,e^{-bt}$; dividing, remaining $= \lambda(t)/b$ at every $t$, so at the rate $\lambda^*$ it is $\lambda^*/b$.

### Solution 28-03.13

With $x = e^{-8b}$, $m(16)/m(8) = (1 - x^2)/(1 - x) = 1 + x = 300/200$, so $x = 0.5$ and $b = \ln 2/8$ = **0.0866** per week; $a = 200/(1 - 0.5)$ = **400** defects. At week 16: remaining $400 \times 0.25$ = **100** defects; discovery rate $ab\,e^{-16b} = 400 \times 0.0866 \times 0.25$ = **8.66** per week. The rate reaches 2 a week when $e^{-bt} = 2/(ab)$, at $t = \ln(ab/2)/b$ = **32.9** weeks: **16.9** more weeks, **3.89** months. Silicon and qualification are ready now, so the least mature dimension, software, binds: the deployment date is about four months out however good the silicon is, and the diligence question is the compiler team's plan to shorten it.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 28-03.3a | probability from L3 | 0.646 | — |
| 28-03.3b | time from L3 | 13.0 | months |
| 28-03.3c | value multiplier at L3 | 0.555 | — |
| 28-03.4a | discount factor after qualification | 1.024 | — |
| 28-03.4b | value multiplier after qualification | 0.928 | — |
| 28-03.4c | ratio to tape-out | 1.85 | — |
| 28-03.5a | acceleration factor, 0.7 eV | 26.3 | — |
| 28-03.5b | acceleration factor, 0.9 eV | 67.0 | — |
| 28-03.6 | FIT bound, zero failures | 75.4 | FIT |
| 28-03.7 | FIT bound, one failure | 166 | FIT |
| 28-03.8a | devices needed, unrounded | 5931.0 | devices |
| 28-03.8b | devices needed | 5932 | devices |
| 28-03.9a | discovery rate constant | 0.0639 | 1/week |
| 28-03.9b | total findable defects | 400 | defects |
| 28-03.9c | remaining at week 16 | 144 | defects |
| 28-03.9d | rate at week 16 | 9.19 | per week |
| 28-03.10a | week of two per week | 39.9 | weeks |
| 28-03.10b | weeks still to go | 23.9 | weeks |
| 28-03.10c | remaining then | 31.3 | defects |
| 28-03.11 | Grade 1 temperature cycles | 1000 | cycles |
| 28-03.13a | discovery constant | 0.0866 | per week |
| 28-03.13b | total defects | 400 | defects |
| 28-03.13c | remaining at week 16 | 100 | defects |
| 28-03.13d | discovery rate at week 16 | 8.66 | per week |
| 28-03.13e | week the rate reaches 2 | 32.9 | weeks |
| 28-03.13f | weeks still needed | 16.9 | weeks |
| 28-03.13g | months still needed | 3.89 | months |
