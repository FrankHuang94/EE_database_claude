# Solutions 28-09 · The Business ↔ Engineering Translation Table

Problems: [28-09 problems](../problems/28-09-problems.md) · Chapter: [28-09](../chapters/28-09-business-engineering-translation.md). Every number is recomputed by [verify_28_09.py](../verify/verify_28_09.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 28-09.1

- (a) **Unit cost and gross margin:** ask for die area, node and wafer price, expected yield, package and test cost, and the selling price.
- (b) **Customer TCO:** ask for power at the customer's workload, the PUE and electricity price assumed, the fleet size and the performance basis of the comparison.
- (c) **Time to revenue:** ask for the maturity level (28-03), the remaining milestones with dates, and what a respin would do to them.
- (d) **Warranty and field cost:** ask for the qualification grade, the FIT bound with its confidence and conditions, and field-return data.

### Solution 28-09.2

100 mm²: $30000/(640 \times 0.9048)$ = **51.80** $; 120 mm²: **64.06** $; increase **23.7**% (the same as on N3, because the wafer price scales both).

### Solution 28-09.3

$1 + 600 \times 0.001$ = **1.6**. Dies per wafer **90** and **81**. Cost increase **18.0**%, average elasticity **1.80**: larger than $1 + AD_0$ because the edge loss and the rounding to whole dies weigh more for large dies.

### Solution 28-09.4

Unit cost $45 \times 0.45$ = **20.25** $; die cost **14.25** $; area **48.5** mm².

### Solution 28-09.5

Lost revenue $120 \times 5/12$ = **50** $M; lost gross profit **25** $M; total with masks **40** $M.

### Solution 28-09.6

$0.7 \times 1.2 \times 43830 \times 0.12$ = **4418** \$; 600 W: **3787** \$; saving **631** \$. Capacity: $0.7/0.6 - 1$ = **16.7**% more devices.

### Solution 28-09.7

$20 \times 10^{-9} \times 5 \times 10^6 \times 500$ = **50** failures a year, costing **0.1** $M.

### Solution 28-09.8

At $0.08: **3647** $, **14.6**% of the price. At $0.15: **6837** $, **27.3**%.

### Solution 28-09.9

$190/30$ = **6.33** million units.

### Solution 28-09.10

(a) Without the edge term, $\text{DPW} = \pi d^2/(4A)$, so $C_{\text{die}} = W/(\text{DPW}\,e^{-AD_0}) = (4W/\pi d^2)\,A\,e^{AD_0}$. Then $\ln C = \text{const} + \ln A + AD_0$ and $d\ln C/d\ln A = A\,d\ln C/dA = A(1/A + D_0) = 1 + AD_0$.

(b) $\text{GM} = 1 - C/\text{ASP}$, so $C/\text{ASP} = 1 - \text{GM}$. After a 10% price rise, $\text{GM}' = 1 - C/(1.1\,\text{ASP})$, and $\text{GM}' - \text{GM} = (C/\text{ASP})(1 - 1/1.1) = (1 - \text{GM})(1 - 1/1.1)$. With GM = 0.556: $0.444 \times 0.0909$ = **4.0** points, as in Example 28-09.6.

(c) A budget $B$ holds $B/P$ devices of power $P$ and $B/[(1 - s)P]$ at power $(1 - s)P$; the ratio is $1/(1 - s)$, so the gain is $1/(1 - s) - 1$. For $s = 0.1$, **11.1**%.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 28-09.2a | cost per good die, 100 mm², N2 | 51.80 | $ |
| 28-09.2b | cost per good die, 120 mm², N2 | 64.06 | $ |
| 28-09.2c | increase | 23.7 | % |
| 28-09.3a | 1 + AD0 | 1.6 | — |
| 28-09.3b | dies per wafer, 600 mm² | 90 | dies |
| 28-09.3c | dies per wafer, 660 mm² | 81 | dies |
| 28-09.3d | cost increase | 18.0 | % |
| 28-09.3e | average elasticity | 1.80 | — |
| 28-09.4a | maximum unit cost | 20.25 | $ |
| 28-09.4b | maximum die cost | 14.25 | $ |
| 28-09.4c | maximum die area | 48.5 | mm² |
| 28-09.5a | lost revenue | 50 | $M |
| 28-09.5b | lost gross profit | 25 | $M |
| 28-09.5c | total profit impact | 40 | $M |
| 28-09.6a | energy cost, 700 W | 4418 | $ |
| 28-09.6b | energy cost, 600 W | 3787 | $ |
| 28-09.6c | saving | 631 | $ |
| 28-09.6d | more devices | 16.7 | % |
| 28-09.7a | failures a year | 50 | failures |
| 28-09.7b | cost | 0.1 | $M |
| 28-09.8a | energy cost at $0.08 | 3647 | $ |
| 28-09.8b | share of price at $0.08 | 14.6 | % |
| 28-09.8c | energy cost at $0.15 | 6837 | $ |
| 28-09.8d | share of price at $0.15 | 27.3 | % |
| 28-09.9 | break-even volume | 6.33 | million units |
| 28-09.10a | ASP sensitivity | 4.0 | points |
| 28-09.10b | capacity gain at s = 0.1 | 11.1 | % |
