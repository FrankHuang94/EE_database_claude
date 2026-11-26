# Solutions 26-04 · Engineering Economics II: Build, Buy or License; Node; Chiplets; ASIC vs Merchant

Problems: [26-04 problems](../problems/26-04-problems.md) · Chapter: [26-04](../chapters/26-04-engineering-economics-2.md). Every number is recomputed by [verify_26_04.py](../verify/verify_26_04.py). Intermediate values are shown rounded but carried at full precision, so recomputing from the displayed figures can differ in the last digit.

---

## Solutions

### Solution 26-04.1

(a) $0.45/18$ = **2.50**%.

(b) $0.015 \times 22$ = **$0.330** per unit.

(c) The royalty is $0.005 \times 300$ = **$1.50** per phone, which is $1.50/15$ = **10.0**% of the chip's price (26-02 §3.6).

(d) The royalty takes 10 points of price, so the margin falls from 55% to **45.0**%.

### Solution 26-04.2

(a) **License.** A USB PHY is a standard block that customers assume works; a silicon-proven licence is cheaper and faster, and it does not differentiate the camera chip.

(b) **Build.** The engine is the product's differentiator; owning it keeps control of the roadmap and the know-how, and its NRE is spread over every product it goes into.

(c) **License.** A first-time team on a nine-month schedule carries a high slip risk ($p_sC_s$ in §3.2); a proven controller removes most of it.

(d) **Build.** Link reach is what this company sells, so the SerDes is core; a licensed PHY would give competitors the same performance.

(e) **License** (usually from the foundry or a library vendor). Cells must be characterized on the foundry's process, a large effort that differentiates little; companies build their own cells only for special needs (very low voltage, very high density).

### Solution 26-04.3

(a) $(9 - 1.5)/0.25$ = **30** million units.

(b) The licence costs $1.5 + 0.25 \times 20$ = **$6.5 M** against $9 M: license, saving **$2.5 M**.

(c) The expected build cost is $9 + 0.2 \times 6$ = **$10.2 M**, so $V^* = (10.2 - 1.5)/0.25$ = **34.8** million units.

### Solution 26-04.4

(a) $U = 2/1.1^2 + 6/1.1^3 + 8/1.1^4 + 6/1.1^5 + 3/1.1^6 = 1.653 + 4.508 + 5.464 + 3.726 + 1.693$ = **17.04** million units.

(b) Build: $10 + 10/1.1$ = **$19.09 M**. Licence: $4 + 0.60 \times 17.04$ = **$14.23 M** (royalties **$10.23 M**). License, saving **$4.86 M**.

(c) $U^* = (19.09 - 4)/0.60$ = **25.2** million discounted units, **1.48** times the plan. The margin is thinner than in Example 26-04.2 because the planned royalties are a larger share of the build cost: **54**% ($10.23 M of $19.09 M) against **35**% ($9.70 M of $27.75 M).

### Solution 26-04.5

(a) The ASPs are $25.00, $20.00, $16.00 and $12.80, so the royalties are **$0.400**, **$0.320**, **$0.256** and **$0.205** per unit.

(b) $U = 10 \times (P/A, 10\%, 4) = 10 \times 3.1699$ = **31.70** million units. Per-unit form: $0.40 \times 31.70$ = **$12.68 M**. Percentage form: $10 \times (0.400/1.1 + 0.320/1.1^2 + 0.256/1.1^3 + 0.2048/1.1^4)$ = **$9.60 M**.

(c) $r_{eq} = 9.60/31.70$ = **$0.303** per unit.

(d) With ASPs falling 10% a year, the percentage form is worth **$11.04 M** (equivalent to **$0.348** per unit). The licensee, expecting 20% erosion, prefers the percentage form ($9.60 M against $12.68 M); the licensor, even with its milder forecast, prefers the per-unit form ($12.68 M against $11.04 M). Their different forecasts leave room for a deal. A percentage rate above $1.6\% \times 12.68/11.04$ = **1.84**% is worth more to the licensor than $0.40 a unit, and a rate below $1.6\% \times 12.68/9.60$ = **2.11**% costs the licensee less than $0.40 a unit, so any rate between the two is preferred by both sides to the per-unit offer.

### Solution 26-04.6

(a) $0.015 \times 30 + 0.20 + 0.05 + 0.30 + 0.25 = 0.45 + 0.80$ = **$1.25** per unit.

(b) $1.25/30$ = **4.17**% of ASP.

(c) Before royalties $(30 - 14)/30$ = **53.3**%; after, $(30 - 14 - 1.25)/30$ = **49.2**%.

(d) $1.25/16$ = **7.8**% of the gross profit, although no single royalty exceeds $0.45.

### Solution 26-04.7

(a) $1/(0.60/1.7 + 0.35/1.2 + 0.05/1.1)$ = **1.449**.

(b) $1/(0.20/1.7 + 0.50/1.2 + 0.30/1.1)$ = **1.239**.

(c) $400/1.449$ = **276.0** mm².

(d) The accelerator is mostly logic, which shrinks 1.7×; the microcontroller is mostly SRAM, flash interface and analog, which shrink 1.2× and 1.1×. Mature-node microcontrollers often stay on older processes for exactly this reason: the new node's wafer premium buys little area.

### Solution 26-04.8

(a) $1/1.3$ = **0.7692** = $0.5/s_L + 0.3/1.0 + 0.2/1.1$, so $0.5/s_L$ = **0.2874** and $s_L$ = **1.74**.

(b) $0.5/s_L = 0.7692 - 0.3/1.1 - 0.2/1.1$ = **0.3147**, so $s_L$ = **1.59**.

(c) A 10% change in the assumed SRAM gain moves the implied logic gain from 1.74× to 1.59×, and the first exceeds even the 1.7× "up to" logic figure quoted for N3. Headline figures can mix best-case logic, bitcell and macro densities, and a particular block mix; to compare claims, rebuild the chip-level gain from per-block figures defined the same way.

### Solution 26-04.9

(a) Cost per function is unchanged when $W_{N3}/W_{N5} = s_{eff}$: $17{,}000 \times 1.378$ = **$23,400**.

(b) $(30{,}000/20{,}000)/1.15$ = **1.30**: cost per function rises 30%.

(c) A gain of $30{,}000/20{,}000$ = **1.50**× would be needed. At these assumptions N2 is justified by power and performance, not cost.

### Solution 26-04.10

(a) Setting $20{,}000/(895\,e^{-0.7259D_0}) = 29.36$ gives $e^{0.7259D_0} = 29.36 \times 895/20{,}000$ = **1.314**, so $D_0$ = **0.376** cm⁻². Above that the N3 die costs more than the N5 die.

(b) With $AD_0$ = 0.1815, 0.1089 and 0.0726:

| Year | $D_0$ (cm⁻²) | Yield | N3 die cost | Saving per die | Units |
|---|---|---|---|---|---|
| 1 | 0.25 | **0.8340** | **$26.79** | **$2.56** | 1 M |
| 2 | 0.15 | **0.8968** | **$24.92** | **$4.44** | 2 M |
| 3 | 0.10 | 0.9300 | $24.03 | $5.33 | 3 M |

The total saving is $2.56 + 2 \times 4.44 + 3 \times 5.33$ = **$27.4 M**, less than the $30 M of NRE: N3 does not pay over 6 million units, although at the mature yield alone it would have saved $6 \times 5.33$ = **$32.0 M**. The yield ramp falls on the earliest units, and here it decides the case.

### Solution 26-04.11

(a) DPW = **82**, $Y = e^{-0.65}$ = **0.5220**, good die $(20{,}000/82 + 2)/0.5220$ = **$471.04**.

(b) Monolithic: $(471.04 + 15)/0.99$ = **$490.95**. Chiplets: $(4 \times 65.09 + 10.83 + 50)/0.99^5$ = **$337.76**, **$153.19** less.

(c) Monolithic: $110 + 0.5 \times 490.95$ = **$355.5 M**. Chiplets: $8 + 0.5 \times 337.76$ = **$176.9 M**. Adding XL costs **$178.6 M** less with chiplets, because no new die is designed.

(d) Monolithic $773.7 + 355.5$ = **$1,129.2 M**; chiplets $719.3 + 176.9$ = **$896.2 M**; chiplets save **$233.0 M**. Each additional product built from existing chiplets widens the gap; the largest products gain the most yield.

### Solution 26-04.12

(a) DPW = **1195**, $Y = e^{-0.055}$ = **0.9465**, good die $(20{,}000/1195 + 2)/0.9465$ = **$19.80**, **$8.96** more than on N6.

(b) $(65.09 + 19.80 + 25)/0.99^2$ = **$112.12**.

(c) **$9.14** more per S unit than with the N6 I/O die: the I/O area costs twice as much per wafer on N3 and gains nothing from the denser node.

### Solution 26-04.13

(a) Merchant $1.0 \times 1.3 \times 8760 \times 5 \times 0.12$ = **$6,833**; custom $0.7 \times$ that = **$4,783**.

(b) Merchant $30{,}000 + 12{,}000 + 6{,}833$ = **$48,833**; custom $(9{,}000 + 12{,}000 + 4{,}783)/0.8$ = **$32,229**.

(c) **$16,604** per merchant-equivalent.

(d) $800 \times 10^6/16{,}604$ = **48,200** merchant-equivalents, **60,200** custom chips.

(e) Energy is a larger part of TCO, and the custom chip uses less of it per unit of work ($0.7/0.8$ = **0.875** of the merchant's), so dearer power favours it slightly. The effect is small because the slot overhead and prices dominate.

### Solution 26-04.14

(a) $0.30 \times 30{,}000$ = **$9,000**.

(b) $N_{eq}$ = 80,000, so $P_m^* = 29{,}438.64 + 800 \times 10^6/80{,}000 - 12{,}000 - 3{,}644.16$ = **$23,794**, at which the merchant keeps $1 - 9{,}000/23{,}794$ = **62.2**%.

(c) At $9,000 the merchant's cost per equivalent would be $9{,}000 + 12{,}000 + 3{,}644$ = **$24,644**, below the custom chip's **$29,439** even with no NRE at all. Equivalently, the lowest ceiling, reached as the fleet grows without limit, is $29{,}439 - 12{,}000 - 3{,}644$ = **$13,794**, above the merchant's cost. This custom chip is less efficient per unit of work than the merchant part; its whole advantage is the merchant's margin.

### Solution 26-04.15

(a) Licensing then choosing costs $29.16 M at $p$ = 0.3; building now costs $27.75 + c_{port}$, so they tie at $c_{port}$ = **$1.41 M**.

(b) $27.75 + 1 = 15.70 + 9.80 + 12.2p$ gives $p$ = **0.266**.

(c) Build now **$30.75 M**; license then choose $15.70 + 0.6 \times 22 + 0.4 \times 9.80$ = **$32.82 M**; license both, with expected volume **17.4** million, $15.70 + 5 + 0.80 \times 17.4$ = **$34.62 M**. Building now is best. Flexibility is worth **$1.80 M** against licensing both, but committing to the build is worth more, because the high-volume outcome is now likely and the port is cheap.

### Solution 26-04.16

(a) $6{,}000/0.60$ = **$10,000**; $6{,}000/0.40$ = **$15,000**.

(b) $(15{,}000 + 12{,}000 + 2{,}551)/0.8$ = **$36,939** per merchant-equivalent; saving $45{,}644.16 - 36{,}938.64$ = **$8,706**; break-even $800 \times 10^6/8{,}706$ = **91,900** merchant-equivalents.

(c) The merchant would earn $30{,}000 - 6{,}000$ = **$24,000** per unit; the partner $10{,}000 - 6{,}000$ = **$4,000**; the buyer captures **$20,000** of the merchant's margin per chip, before the throughput shortfall, the extra slots and the NRE take their share.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 26-04.1a | royalty percentage | 2.50 | % |
| 26-04.1b | royalty per unit | 0.330 | $ |
| 26-04.1c | device royalty | 1.50 | $ |
| 26-04.1c1 | chip-level rate | 10.0 | % |
| 26-04.1d | margin after royalty | 45.0 | % |
| 26-04.3a | break-even | 30 | million |
| 26-04.3b | licence cost | 6.5 | $M |
| 26-04.3b1 | saving | 2.5 | $M |
| 26-04.3c | expected build cost | 10.2 | $M |
| 26-04.3c1 | break-even with risk | 34.8 | million |
| 26-04.4a | discounted units | 17.04 | million |
| 26-04.4a1 | year 2 term | 1.653 | million |
| 26-04.4a2 | year 3 term | 4.508 | million |
| 26-04.4a3 | year 4 term | 5.464 | million |
| 26-04.4a4 | year 5 term | 3.726 | million |
| 26-04.4a5 | year 6 term | 1.693 | million |
| 26-04.4b | build PV | 19.09 | $M |
| 26-04.4b1 | licence PV | 14.23 | $M |
| 26-04.4b2 | royalty PV | 10.23 | $M |
| 26-04.4b3 | saving | 4.86 | $M |
| 26-04.4c | discounted break-even | 25.2 | million |
| 26-04.4c1 | multiple of plan | 1.48 | |
| 26-04.4c2 | royalty share of build cost | 54 | % |
| 26-04.4c3 | royalty share, Example 2 | 35 | % |
| 26-04.5a | royalty year 1 | 0.400 | $ |
| 26-04.5a1 | royalty year 2 | 0.320 | $ |
| 26-04.5a2 | royalty year 3 | 0.256 | $ |
| 26-04.5a3 | royalty year 4 | 0.205 | $ |
| 26-04.5b | discounted units | 31.70 | million |
| 26-04.5b0 | P/A 10% 4 | 3.1699 | |
| 26-04.5b1 | per-unit PV | 12.68 | $M |
| 26-04.5b2 | percentage PV | 9.60 | $M |
| 26-04.5c | equivalent per-unit royalty | 0.303 | $ |
| 26-04.5d | licensor's PV | 11.04 | $M |
| 26-04.5d1 | licensor's equivalent | 0.348 | $ |
| 26-04.5d2 | lowest acceptable rate | 1.84 | % |
| 26-04.5d3 | highest acceptable rate | 2.11 | % |
| 26-04.6a | total royalty | 1.25 | $ |
| 26-04.6a1 | CPU royalty | 0.45 | $ |
| 26-04.6a2 | per-unit royalties | 0.80 | $ |
| 26-04.6b | royalty share of ASP | 4.17 | % |
| 26-04.6c | margin before | 53.3 | % |
| 26-04.6c1 | margin after | 49.2 | % |
| 26-04.6d | share of gross profit | 7.8 | % |
| 26-04.7a | accelerator gain | 1.449 | |
| 26-04.7b | microcontroller gain | 1.239 | |
| 26-04.7c | accelerator area | 276.0 | mm² |
| 26-04.8a | reciprocal of claim | 0.7692 | |
| 26-04.8a1 | logic term | 0.2874 | |
| 26-04.8a2 | implied logic gain | 1.74 | |
| 26-04.8b | logic term | 0.3147 | |
| 26-04.8b1 | implied logic gain | 1.59 | |
| 26-04.9a | neutral wafer price | 2.34e4 | $ |
| 26-04.9b | cost ratio | 1.30 | |
| 26-04.9c | neutral gain | 1.50 | |
| 26-04.10a | yield ratio needed | 1.314 | |
| 26-04.10a1 | break-even D0 | 0.376 | cm⁻² |
| 26-04.10b | yield year 1 | 0.8340 | |
| 26-04.10b1 | cost year 1 | 26.79 | $ |
| 26-04.10b2 | saving year 1 | 2.56 | $ |
| 26-04.10b3 | yield year 2 | 0.8968 | |
| 26-04.10b4 | cost year 2 | 24.92 | $ |
| 26-04.10b5 | saving year 2 | 4.44 | $ |
| 26-04.10b6 | total saving | 27.4 | $M |
| 26-04.10b7 | saving without ramp | 32.0 | $M |
| 26-04.10b8 | AD0 year 1 | 0.1815 | |
| 26-04.10b9 | AD0 year 2 | 0.1089 | |
| 26-04.11a | XL dies per wafer | 82 | |
| 26-04.11a1 | XL yield | 0.5220 | |
| 26-04.11a2 | XL good die | 471.04 | $ |
| 26-04.11b | XL monolithic package | 490.95 | $ |
| 26-04.11b1 | XL chiplet package | 337.76 | $ |
| 26-04.11b2 | XL difference | 153.19 | $ |
| 26-04.11c | increment, monolithic | 355.5 | $M |
| 26-04.11c1 | increment, chiplets | 176.9 | $M |
| 26-04.11c2 | difference | 178.6 | $M |
| 26-04.11d | monolithic family | 1129.2 | $M |
| 26-04.11d1 | chiplet family | 896.2 | $M |
| 26-04.11d2 | saving | 233.0 | $M |
| 26-04.12a | N3 I/O dies per wafer | 1195 | |
| 26-04.12a1 | N3 I/O yield | 0.9465 | |
| 26-04.12a2 | N3 I/O good die | 19.80 | $ |
| 26-04.12a3 | extra die cost | 8.96 | $ |
| 26-04.12b | chiplet S package | 112.12 | $ |
| 26-04.12c | extra per S unit | 9.14 | $ |
| 26-04.13a | merchant energy | 6833 | $ |
| 26-04.13a1 | custom energy | 4783 | $ |
| 26-04.13b | merchant per equivalent | 48833 | $ |
| 26-04.13b1 | custom per equivalent | 32229 | $ |
| 26-04.13c | saving | 16604 | $ |
| 26-04.13d | break-even, equivalents | 4.82e4 | |
| 26-04.13d1 | break-even, chips | 6.02e4 | |
| 26-04.13e | energy per unit of work ratio | 0.875 | |
| 26-04.14a | merchant cost | 9000 | $ |
| 26-04.14b | price ceiling | 23794 | $ |
| 26-04.14b1 | merchant margin | 62.2 | % |
| 26-04.14c | merchant per equivalent at cost | 24644 | $ |
| 26-04.14c1 | custom per equivalent | 29439 | $ |
| 26-04.14c2 | lowest ceiling | 13794 | $ |
| 26-04.15a | tie port cost | 1.41 | $M |
| 26-04.15b | threshold probability | 0.266 | |
| 26-04.15c | build now | 30.75 | $M |
| 26-04.15c1 | license then choose | 32.82 | $M |
| 26-04.15c2 | expected volume | 17.4 | million |
| 26-04.15c3 | license both | 34.62 | $M |
| 26-04.15c4 | value of flexibility | 1.80 | $M |
| 26-04.16a | price at 40% | 10000 | $ |
| 26-04.16a1 | price at 60% | 15000 | $ |
| 26-04.16b | custom per equivalent | 36939 | $ |
| 26-04.16b1 | saving | 8706 | $ |
| 26-04.16b2 | break-even | 9.19e4 | |
| 26-04.16c | merchant gross profit | 24000 | $ |
| 26-04.16c1 | partner gross profit | 4000 | $ |
| 26-04.16c2 | buyer's capture | 20000 | $ |
