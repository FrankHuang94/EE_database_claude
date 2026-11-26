# Lab 26-03 · Cost Stacks, Break-Even and the Price of a Slip

**Objective.** Build a chip's cost waterfall, see how late yield losses and volume change its cost, value a program with discounted cash flows, and find which assumptions move that value most.

**Chapter:** [26-03 · Engineering Economics I: NRE, Die Cost, ASP and Gross Margin](../../chapters/26-03-engineering-economics-1.md)

## Background

§3.1 derived the cascaded cost stack $C_{good} = [(C_{die} + C_{pkg})/Y_{asm} + C_{test}]/Y_{test}$. §3.2 gave NRE amortization and the break-even volume $V^* = \text{NRE}/(\text{ASP} - \text{COGS})$. §3.3 derived the interest factors, NPV and IRR, and §3.4 the program model with a slip and a closing market window. §3.5 introduced the tornado analysis.

## Files

- `econ.py`: interest factors and effective rates; NPV, IRR (bisection) and payback; dies per wafer and the cascaded cost stack; break-even volume; program cash flows with a fractional-year slip and a window that prorates the final year's sales; a one-at-a-time tornado.
- `26-03-econ-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Cost waterfall** (notebook). *Predict* how much Example 26-03.2's COGS rises if final-test yield falls from 98% to 90%, then compute it and draw the waterfall from die to COGS for both yields.

**Part 2 · Volume** (notebook). *Predict* the lifetime volume at which Example 26-03.3's $60 M of NRE falls below $2 a unit, then plot the fully loaded cost and margin against volume from 1 to 50 million units.

**Part 3 · Slip** (notebook). *Predict* the NPV of Example 26-03.5's program after a six-month slip, with the final year's sales cut in proportion to the part of that year that falls past the window (end of year 5), then compute the NPV for slips from 0 to 12 months.

**Part 4 · Tornado** (notebook). *Predict* the order of the bars for ±10% changes in ASP (the 2% royalty moves with it), volume, manufacturing cost (COGS before the royalty) and NRE, then draw the tornado (Problem 26-03.14 computes the same swings by hand).

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 26-03.a | COGS at 90% final-test yield | 39.97 | $ |
| Lab 26-03.a1 | increase | 3.16 | $ |
| Lab 26-03.a2 | gross margin at 90% | 33.4 | % |
| Lab 26-03.b | volume for $2 of NRE per unit | 30 | million |
| Lab 26-03.c | NPV after a six-month slip | 75.6 | $M |
| Lab 26-03.c1 | NPV lost | 20.9 | $M |
| Lab 26-03.c2 | value lost to a half-year delay | 5.5 | % |
| Lab 26-03.c3 | value lost to a one-year delay | 10.7 | % |

## Discussion

1. An eight-point drop in final-test yield costs $3.16 a unit and over five points of margin (38.7% to 33.4%), because every failing unit has already paid for its die, package and test. Moving screening earlier, or improving the test's own escapes and overkill (25-11), is worth real money.
2. NRE per unit falls as $1/V$, so the first few million units matter most; beyond about 30 million units the NRE is a minor part of the cost, and the business is decided by COGS and ASP.
3. With the final year prorated, a six-month slip costs $20.9 M, slightly more than half the one-year loss ($39.9 M), because the cost of discounting is concave in the delay: a half-year costs $1 - 1.12^{-0.5}$ = 5.5% of value, more than half of a full year's 10.7%.
4. The tornado ranks ASP first, manufacturing cost second, volume third and NRE last: price and cost per unit, not development budget, decide a high-volume chip's value.

## Optional hardware

None needed. If you have access to a company's public filings, rebuild its gross margin from segment revenue and COGS for two years, and identify which change (price, mix, cost) explains the difference.
