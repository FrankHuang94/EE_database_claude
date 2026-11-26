# Solutions 25-11 · Test: ATE, Wafer Sort, Burn-In and Binning

Problems: [25-11 problems](../problems/25-11-problems.md) · Chapter: [25-11](../chapters/25-11-test-ate-sort-burn-in.md)

Every number is recomputed by [verify_25_11.py](../verify/verify_25_11.py).

---

## Solutions

### Solution 25-11.1

$\eta = 1 - (2.4 - 1.5)/(7 \times 1.5)$ = **0.914**; gain $8 \times 1.5/2.4$ = **5.0**.

### Solution 25-11.2

$(300/3600) \times (2.4 + 0.5)/8$ = **$0.0302** per die.

### Solution 25-11.3

$0.02/(250/3600)$ = **0.288** s.

### Solution 25-11.4

(a) $\exp[(0.7/k)(1/328.15 - 1/398.15)]$ = **77.6**. (b) $77.6 \times e^{1}$ = **211**. (c) $1200/211$ = **5.69** h: voltage acceleration shortens burn-in a lot, but too much voltage can create failures that would never occur in use.

### Solution 25-11.5

(a) $1 - \exp[-(12)^{0.3}]$ = **0.878**. (b) $10^6 \times 0.01 \times 0.122$ = **1.22e3** ppm. (c) $100 \times (\ln 100)^{1/0.3}$ = 1.62 × 10⁴ use hours, **325** h at AF = 50, nearly two weeks. A shallow weak population is better fixed at its source than burned out.

### Solution 25-11.6

$0.01 \times 0.969$ = **0.969**% of production.

### Solution 25-11.7

Fractions **0.0228**, **0.477**, **0.477**; revenue **$345**, up from $332. The top bin shrinks, but the scrap bin shrinks just as much (from 9.1% to 2.3%), and more parts land in the paid middle bins.

### Solution 25-11.8

A guard band of **50.4** MHz gives 100 ppm escapes, with **13.1**% overkill.

### Solution 25-11.9

(a) $1128.6/779.7 - 1$ = **44.7**%. (b) $499.1/1128.6$ = **44.2**%. (c) $1863.0/1128.6 - 1$ = **65.1**%.

### Solution 25-11.10

$1306/769 - 1$ = **69.8**% growth; $1072/1306$ = **82.1**% from semiconductor test.

### Solution 25-11.11

$9.0/1.5$ = **$6.0 B**.

### Solution 25-11.12

Without sort, 140 bad dies are packaged: **$420** wasted. With sort: $1000 \times 0.05 = 50$ plus $140 \times 0.05 \times 3 = 21$ of wasted packaging, **$71**. Saving **$349** per wafer; for chiplets, where a bad die scraps a whole module, the case is far stronger (25-07).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 25-11.1a | multisite efficiency | 0.914 | |
| 25-11.1b | throughput gain | 5.0 | |
| 25-11.2a | cost per die | 0.0302 | $ |
| 25-11.3a | test-time budget | 0.288 | s |
| 25-11.4a | thermal factor | 77.6 | |
| 25-11.4b | total factor | 211 | |
| 25-11.4c | burn-in hours | 5.69 | h |
| 25-11.5a | fraction removed | 0.878 | |
| 25-11.5b | weak shipped | 1.22e3 | ppm |
| 25-11.5c0 | use hours for 100 ppm | 1.62e4 | h |
| 25-11.5c | burn-in hours | 325 | h |
| 25-11.6a | production removed | 0.969 | % |
| 25-11.7a | top-bin fraction | 0.0228 | |
| 25-11.7a1 | middle-bin fraction | 0.477 | |
| 25-11.7b | revenue | 345 | $ |
| 25-11.8a | guard band | 50.4 | MHz |
| 25-11.8b | overkill | 13.1 | % |
| 25-11.9a | FY2025 growth | 44.7 | % |
| 25-11.9b | operating margin | 44.2 | % |
| 25-11.9c | FY2026 forecast growth | 65.1 | % |
| 25-11.10a | growth | 69.8 | % |
| 25-11.10b | semiconductor-test share | 82.1 | % |
| 25-11.11a | CY2024 ATE market | 6.0 | $B |
| 25-11.12a | wasted without sort | 420 | $ |
| 25-11.12b | cost with sort | 71 | $ |
| 25-11.12c | saving | 349 | $ |
