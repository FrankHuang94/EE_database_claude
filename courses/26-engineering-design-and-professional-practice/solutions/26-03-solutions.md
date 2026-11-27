# Solutions 26-03 · Engineering Economics I: NRE, Die Cost, ASP and Gross Margin

Problems: [26-03 problems](../problems/26-03-problems.md) · Chapter: [26-03](../chapters/26-03-engineering-economics-1.md). Every number is recomputed by [verify_26_03.py](../verify/verify_26_03.py). Intermediate values are shown rounded but carried at full precision, so recomputing from the displayed figures can differ in the last digit.

---

## Solutions

### Solution 26-03.1

(a) $F = 10{,}000 \times 1.06^8$ = **\$15,938.48**.

(b) $P = 50{,}000 \times 1.07^{-5}$ = **\$35,649.31**.

### Solution 26-03.2

(a) $(1 + 0.12/12)^{12} - 1$ = **12.683**%.

(b) $e^{0.12} - 1$ = **12.750**%. Continuous compounding adds only 0.07 point over monthly; the big step is from annual to any intra-year compounding.

### Solution 26-03.3

(a) The payment at the end of period $t$ grows for $n - t$ periods, so $F = A\sum_{t=1}^n(1 + i)^{n-t} = A[1 + (1 + i) + \dots + (1 + i)^{n-1}] = A[(1 + i)^n - 1]/i$, a geometric series with ratio $1 + i$. Hence $(F/A, i, n) = [(1 + i)^n - 1]/i$.

(b) $(1.05^{10} - 1)/0.05$ = **12.5779**.

(c) $A = 1{,}000{,}000/12.5779$ = **\$79,505** a year.

### Solution 26-03.4

$(A/P, 9\%, 3) = 0.09 \times 1.09^3/(1.09^3 - 1)$ = **0.39505**, so the annual payment is $12 \times 0.39505$ = **\$4.7407 M**.

### Solution 26-03.5

(a) NPV $= -10 + 4(P/A, 10\%, 3) + 2(P/F, 10\%, 4) = -10 + 4 \times 2.4869 + 2 \times 0.6830$ = **\$1.313 M**.

(b) Solving NPV($r$) = 0 by bisection gives IRR = **16.5**%, above the 10% MARR, consistent with a positive NPV.

(c) Cumulative cash is −6 after year 1 and −2 after year 2, and year 3 brings 4, so payback is $2 + 2/4$ = **2.5** years.

### Solution 26-03.6

(a) DPW $= \pi \times 300^2/800 - \pi \times 300/\sqrt{400}$ = **306.3**, so **306**; $Y = e^{-0.3}$ = **0.7408**; $C_{die} = 12{,}000/(306 \times 0.7408)$ = **\$52.94**.

(b) After assembly $(52.94 + 6.00)/0.985$ = **\$59.83**; after test $(59.83 + 2.50)/0.96$ = **\$64.93**.

(c) COGS $= 64.93 + 0.50$ = **\$65.43**.

(d) GM $= (95 - 65.43)/95$ = **31.1**%; markup **45.2**%. The large die on a modest-yield process makes this a thin-margin product unless the price rises or the die shrinks.

### Solution 26-03.7

(a) With 97% assembly yield, COGS = **$37.51**, up **$0.71**.

(b) With 96% final-test yield, COGS = **$37.55**, up **$0.74**.

(c) The same two-point loss costs more at final test, because a unit failing there has already absorbed the package, assembly and its share of the test cost; the difference grows with the cost added between the two steps.

### Solution 26-03.8

(a) $25 \times 10^6/8$ = **3.125 million** units.

(b) A \$2 price cut lowers the contribution to \$6, so $V^* = 25 \times 10^6/6$ = **4.17 million** units, **33**% more. A 10% price cut raised break-even volume by a third, because it took a quarter of the contribution.

(c) COGS is $20 - 8$ = \$12. NRE per unit $25 \times 10^6/(5 \times 10^6)$ = **\$5.00**; fully loaded cost $12 + 5$ = **\$17.00**; fully loaded margin $(20 - 17)/20$ = **15.0**%.

### Solution 26-03.9

Gross margin is $(\text{ASP} - 30 - 0.03\,\text{ASP})/\text{ASP} = 0.55$, so $\text{ASP}(1 - 0.03 - 0.55) = 30$ and ASP $= 30/0.42$ = **\$71.43**. A royalty proportional to price acts like a reduction of the margin available, not a fixed cost.

### Solution 26-03.10

(a) ASPs **$40.00**, **$36.00**, **$32.40** and **$29.16**; contributions **$18.00**, **$14.00**, **$10.40** and **$7.16**; cash flows (\$M) −40, −40, **36.0**, **70.0**, **62.4** and **28.6**.

(b) NPV at 12% = **$58.7 M**.

(c) Solving NPV = 0 for the erosion rate gives **19.8**% a year. Erosion this fast is not unusual in competitive consumer markets, which is why such products need short development times and successors already in design.

### Solution 26-03.11

(a) Adding back the discounted NRE, the sales cash flows are worth $96.52 + 30 + 30/1.12$ = **\$153.31 M** at year 0.

(b) $153.31/1.12^{0.5} - 30 - 26.79$ = **$88.07 M**, a loss of **$8.45 M**.

(c) $153.31/1.12 - 56.79$ = **$80.09 M**, a loss of **$16.43 M**.

(d) Of the \$39.93 M loss, discounting accounts for $16.43 M and the closing window for **$23.50 M**, or **59**%. Losing the end of the market window costs more than waiting for the money.

### Solution 26-03.12

$(A/P, 10\%, 4)$ = **0.31547** and $(A/P, 10\%, 6)$ = **0.22961**. EUAC(A) $= 2.0 \times 0.31547 + 0.3$ = **\$0.9309 M**; EUAC(B) $= 3.0 \times 0.22961 + 0.2$ = **$0.8888 M**. B is cheaper by **$42,119** a year, assuming each can be replaced in kind at the end of its life.

### Solution 26-03.13

(a) $D = (5.0 - 0.5)/5$ = **\$0.90 M** a year; book value after 2 years $5.0 - 2 \times 0.9$ = **\$3.20 M**.

(b) Tax saving $0.21 \times 0.90$ = **\$0.189 M** a year, worth $0.189 \times (P/A, 10\%, 5) = 0.189 \times 3.7908$ = **\$0.7165 M** today. Depreciation is not a cash flow, but its tax shield is.

### Solution 26-03.14

With 6.61 million discounted units:

(a) ASP ±10% is ±$6.00 a unit, less the ±$0.12 change in the 2% royalty: ±$5.88 a unit, ±**$38.9 M**.

(b) Volume ±10% scales the contribution stream: $0.1 \times 23.19 \times 6.61$ = ±**\$15.3 M**.

(c) Manufacturing cost ±10% is ∓$3.56 a unit: ∓**$23.5 M**.

(d) NRE ±10%: ∓**$5.68 M**.

The ranking is ASP, manufacturing cost, volume, NRE. Cost outranks volume because a 10% change in manufacturing cost ($3.56) is larger than 10% of the contribution ($2.32): at a 39% margin, costs are a larger lever than units.

### Solution 26-03.15

(a) **Variable**, in COGS (the die cost). (b) **Fixed** (NRE), not in COGS. (c) **Variable**, in COGS (test cost per unit). (d) **Fixed** (R&D), not in COGS. (e) **Variable**, in COGS (per-unit royalty). (f) **Fixed** (NRE), not in COGS.

### Solution 26-03.16

(a) With $1.08^5$ = 1.469328: $(P/G, 8\%, 5) = (1.469328 - 1 - 5 \times 0.08)/(0.08^2 \times 1.469328) = 0.069328/0.0094037$ = **7.372**; $(A/G, 8\%, 5) = 1/0.08 - 5/0.469328 = 12.5 - 10.6535$ = **1.8465**. (The derivation is in §3.3: stack the gradient as uniform series starting in years 2, 3, 4 and 5.)

(b) The costs are a uniform \$50,000 plus a gradient of \$10,000: $50{,}000 \times (P/A, 8\%, 5) + 10{,}000 \times (P/G, 8\%, 5) = 50{,}000 \times 3.99271 + 10{,}000 \times 7.3724$ = **\$273,360**.

(c) EUAC $= 50{,}000 + 10{,}000 \times 1.8465$ = **\$68,465** a year. Check: $273{,}360 \times (A/P, 8\%, 5) = 273{,}360 \times 0.250456$ = \$68,465. ✓

### Solution 26-03.17

(a) $P = A/i = 300{,}000/0.06$ = **\$5.00 M**.

(b) $(P/A, 10\%, 4)$ = 3.16987. Base: PV of costs $4.0 + 1.0 \times 3.16987$ = \$7.170 M; PV of benefits $3.0 \times 3.16987$ = $9.510 M; B/C = **1.33**; NPV = **$2.34 M**. Expanded: costs $6.0 + 1.2 \times 3.16987$ = \$9.804 M; benefits $3.8 \times 3.16987$ = $12.045 M; B/C = **1.23**; NPV = **$2.24 M**.

(c) The increment costs $9.804 - 7.170$ = \$2.634 M and brings $12.045 - 9.510$ = \$2.536 M: $\Delta B/\Delta C$ = **0.963** < 1, so the extra spending does not pay; choose the base version. Both versions pass B/C > 1 on their own, which is why ranking by each one's own ratio, or by B/C rather than the increment, can mislead; the incremental test agrees with NPV (2.34 against 2.24).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 26-03.1a | future value | 15938.48 | $ |
| 26-03.1b | present value | 35649.31 | $ |
| 26-03.2a | effective rate, monthly | 12.683 | % |
| 26-03.2b | effective rate, continuous | 12.750 | % |
| 26-03.2c | difference | 0.07 | points |
| 26-03.3b | F/A 5% 10 | 12.5779 | |
| 26-03.3c | annual deposit | 79505 | $ |
| 26-03.4 | A/P 9% 3 | 0.39505 | |
| 26-03.4a | annual payment | 4.7407 | $M |
| 26-03.5a0 | P/A 10% 3 | 2.4869 | |
| 26-03.5a1 | P/F 10% 4 | 0.6830 | |
| 26-03.5a | NPV | 1.313 | $M |
| 26-03.5b | IRR | 16.5 | % |
| 26-03.5c | payback | 2.5 | years |
| 26-03.6a0 | dies per wafer, formula | 306.3 | |
| 26-03.6a | dies per wafer | 306 | |
| 26-03.6a1 | die yield | 0.7408 | |
| 26-03.6a2 | cost per good die | 52.94 | $ |
| 26-03.6b | after assembly | 59.83 | $ |
| 26-03.6b1 | after test | 64.93 | $ |
| 26-03.6c | COGS | 65.43 | $ |
| 26-03.6d | gross margin | 31.1 | % |
| 26-03.6d1 | markup | 45.2 | % |
| 26-03.7a | COGS, assembly 97% | 37.51 | $ |
| 26-03.7a1 | increase | 0.71 | $ |
| 26-03.7b | COGS, test 96% | 37.55 | $ |
| 26-03.7b1 | increase | 0.74 | $ |
| 26-03.8a | break-even | 3.125 | million |
| 26-03.8b | break-even after price cut | 4.17 | million |
| 26-03.8b1 | increase | 33 | % |
| 26-03.8c | NRE per unit | 5.00 | $ |
| 26-03.8c1 | fully loaded cost | 17.00 | $ |
| 26-03.8c2 | fully loaded margin | 15.0 | % |
| 26-03.9 | ASP | 71.43 | $ |
| 26-03.10a | ASP year 2 | 40.00 | $ |
| 26-03.10a1 | ASP year 3 | 36.00 | $ |
| 26-03.10a2 | ASP year 4 | 32.40 | $ |
| 26-03.10a3 | ASP year 5 | 29.16 | $ |
| 26-03.10a4 | contribution year 2 | 18.00 | $ |
| 26-03.10a5 | contribution year 3 | 14.00 | $ |
| 26-03.10a6 | contribution year 4 | 10.40 | $ |
| 26-03.10a7 | contribution year 5 | 7.16 | $ |
| 26-03.10a8 | cash flow year 2 | 36.0 | $M |
| 26-03.10a9 | cash flow year 3 | 70.0 | $M |
| 26-03.10a10 | cash flow year 4 | 62.4 | $M |
| 26-03.10a11 | cash flow year 5 | 28.6 | $M |
| 26-03.10b | NPV | 58.7 | $M |
| 26-03.10c | break-even erosion | 19.8 | % |
| 26-03.11a | PV of sales | 153.31 | $M |
| 26-03.11b | NPV, half-year delay | 88.07 | $M |
| 26-03.11b1 | loss | 8.45 | $M |
| 26-03.11c | NPV, one-year delay | 80.09 | $M |
| 26-03.11c1 | loss | 16.43 | $M |
| 26-03.11d | window share of loss | 23.50 | $M |
| 26-03.11d1 | window share | 59 | % |
| 26-03.12a | A/P 10% 4 | 0.31547 | |
| 26-03.12a1 | A/P 10% 6 | 0.22961 | |
| 26-03.12b | EUAC A | 0.9309 | $M |
| 26-03.12b1 | EUAC B | 0.8888 | $M |
| 26-03.12c | difference | 42119 | $ |
| 26-03.13a | depreciation | 0.90 | $M |
| 26-03.13a1 | book value after 2 years | 3.20 | $M |
| 26-03.13b | annual tax saving | 0.189 | $M |
| 26-03.13b1 | present value | 0.7165 | $M |
| 26-03.14a | ASP swing | 38.9 | $M |
| 26-03.14b | volume swing | 15.3 | $M |
| 26-03.14c | manufacturing-cost swing | 23.5 | $M |
| 26-03.14d | NRE swing | 5.68 | $M |
| 26-03.14e | 10% of manufacturing cost | 3.56 | $ |
| 26-03.14e1 | 10% of contribution | 2.32 | $ |
| 26-03.16a | P/G at 8%, 5 years | 7.372 | |
| 26-03.16a1 | A/G at 8%, 5 years | 1.8465 | |
| 26-03.16b | present worth | 273360 | $ |
| 26-03.16c | EUAC | 68465 | $ |
| 26-03.17a | capitalized cost | 5.00 | $M |
| 26-03.17b | base B/C | 1.33 | |
| 26-03.17b1 | base NPV | 2.34 | $M |
| 26-03.17b2 | expanded B/C | 1.23 | |
| 26-03.17b3 | expanded NPV | 2.24 | $M |
| 26-03.17c | incremental B/C | 0.963 | |
