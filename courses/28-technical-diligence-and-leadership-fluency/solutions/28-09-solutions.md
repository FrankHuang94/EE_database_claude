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

100 mm²: $30000/(640 \times 0.9048)$ = **51.80** \$; 120 mm²: **64.06** \$; increase **23.7**% (the same as on N3, because the wafer price scales both).

### Solution 28-09.3

$1 + 600 \times 0.001$ = **1.6**. Dies per wafer: $\pi \cdot 300^2/2400 - \pi \cdot 300/\sqrt{1200} = 117.8 - 27.2 = 90.6$, so **90**; at 660 mm², $107.1 - 25.9 = 81.2$, so **81**. Cost increase **18.0**%, average elasticity **1.80**: larger than $1 + AD_0 = 1.6$ mainly because the wafer-edge term is large for big dies (the point elasticity including it is about **1.75** at 600 mm²) and $AD_0$ rises across the interval; rounding to whole dies here slightly *lowers* the increase (it is **18.5**% unrounded).

### Solution 28-09.4

Unit cost $45 \times 0.45$ = **20.25** \$; die cost **14.25** \$; area **48.5** mm².

### Solution 28-09.5

Lost revenue $120 \times 5/12$ = **50** \$M; lost gross profit **25** \$M; total with masks **40** \$M.

### Solution 28-09.6

$0.7 \times 1.2 \times 43830 \times 0.12$ = **4418** \$; 600 W: **3787** \$; saving **631** \$. Capacity: $0.7/0.6 - 1$ = **16.7**% more devices.

### Solution 28-09.7

$20 \times 10^{-9} \times 5 \times 10^6 \times 500$ = **50** failures a year, costing **0.1** \$M.

### Solution 28-09.8

At $0.08: **3647** $, **14.6**% of the price. At $0.15: **6837** $, **27.3**%.

### Solution 28-09.9

$190/30$ = **6.33** million units.

### Solution 28-09.10

(a) Without the edge term, $\text{DPW} = \pi d^2/(4A)$, so $C_{\text{die}} = W/(\text{DPW}\,e^{-AD_0}) = (4W/\pi d^2)\,A\,e^{AD_0}$. Then $\ln C = \text{const} + \ln A + AD_0$ and $d\ln C/d\ln A = A\,d\ln C/dA = A(1/A + D_0) = 1 + AD_0$.

(b) $\text{GM} = 1 - C/\text{ASP}$, so $C/\text{ASP} = 1 - \text{GM}$. After a 10% price rise, $\text{GM}' = 1 - C/(1.1\,\text{ASP})$, and $\text{GM}' - \text{GM} = (C/\text{ASP})(1 - 1/1.1) = (1 - \text{GM})(1 - 1/1.1)$. With GM = 0.556: $0.444 \times 0.0909$ = **4.0** points, as in Example 28-09.6.

(c) A budget $B$ holds $B/P$ devices of power $P$ and $B/[(1 - s)P]$ at power $(1 - s)P$; the ratio is $1/(1 - s)$, so the gain is $1/(1 - s) - 1$. For $s = 0.1$, **11.1**%.

### Solution 28-09.11

(a) The base margin is 55.6%. Changing one driver at a time, with whole dies (640 at 100 mm², 653 at 98 mm², 620 at 103 mm²):

| Driver | Low end | High end | Swing (points) |
|---|---|---|---|
| ASP \$80 / \$95 | **−5.5** | **+2.3** | **7.9** |
| Die area 98 / 103 mm² | **+0.8** | **−1.3** | **2.0** |
| Wafer \$17,000 / \$20,000 | **+2.9** | **−2.9** | **5.8** |
| $D_0$ 0.0008 / 0.003 per mm² | **+0.7** | **−7.9** | **8.6** |
| Package and test \$7 / \$10 | **+1.1** | **−2.2** | **3.3** |

(b) Ranked by swing: defect density, ASP, wafer price, package and test, die area. The equal-swing tornado (±10%) ranked die area and ASP first and defect density last (−0.36 points). The reversal comes from the ranges: die area after tape-out is known within a few percent, while defect density on a young node can be off by several times, and its effect is one-sided, because it enters through $e^{-AD_0}$ and the plausible range sits mostly above the base. The ASP range is also wide, but it is a commercial claim, tested with customer pricing rather than engineering.

(c) Defect density. Ask for the measured $D_0$ trend on this node by month, the wafer-sort yield of the last few lots with the die size, the yield model used in the plan, and any contractual yield commitment from the foundry. Then rerun the margin at the measured value.

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
| 28-09.3f | point elasticity with the edge term, 600 mm² | 1.75 | — |
| 28-09.3g | cost increase without rounding | 18.5 | % |
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
| 28-09.11a | margin change, ASP \$80 | -5.5 | points |
| 28-09.11b | margin change, ASP \$95 | 2.3 | points |
| 28-09.11c | swing, ASP | 7.9 | points |
| 28-09.11d | margin change, 98 mm² | 0.8 | points |
| 28-09.11e | margin change, 103 mm² | -1.3 | points |
| 28-09.11f | swing, die area | 2.0 | points |
| 28-09.11g | margin change, \$17,000 wafer | 2.9 | points |
| 28-09.11h | margin change, \$20,000 wafer | -2.9 | points |
| 28-09.11i | swing, wafer price | 5.8 | points |
| 28-09.11j | margin change, D0 = 0.0008 | 0.7 | points |
| 28-09.11k | margin change, D0 = 0.003 | -7.9 | points |
| 28-09.11l | swing, defect density | 8.6 | points |
| 28-09.11m | margin change, \$7 package and test | 1.1 | points |
| 28-09.11n | margin change, \$10 package and test | -2.2 | points |
| 28-09.11o | swing, package and test | 3.3 | points |
