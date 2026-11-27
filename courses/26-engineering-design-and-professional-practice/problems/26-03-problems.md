# Problems 26-03 · Engineering Economics I: NRE, Die Cost, ASP and Gross Margin

Chapter: [26-03](../chapters/26-03-engineering-economics-1.md) · Worked solutions: [26-03 solutions](../solutions/26-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Cash flows occur at the ends of periods unless stated; the interest rate is per period.
- Dies per wafer use 25-04's formula $\pi d^2/(4A) - \pi d/\sqrt{2A}$, rounded down; die yield is Poisson, $e^{-AD_0}$.
- "Assumed" values are illustrative.

---

## Problems

### Problem 26-03.1 [A]

**Single payments.** (a) What does $10,000 invested at 6% a year grow to in 8 years? (b) What is $50,000 received in 5 years worth today at 7%?

### Problem 26-03.2 [A]

**Effective rates.** Find the effective annual rate for a nominal 12% compounded (a) monthly and (b) continuously.

### Problem 26-03.3 [B]

**Saving toward a purchase.** (a) Derive $(F/A, i, n)$ by summing the future values of $n$ end-of-period payments. (b) Evaluate $(F/A, 5\%, 10)$. (c) What equal annual deposit grows to \$1.0 M in 10 years at 5%?

### Problem 26-03.4 [B]

**Financing EDA licenses.** A three-year EDA license bundle costing $12 M up front is financed at 9% a year with equal annual payments. Find the capital recovery factor and the annual payment.

### Problem 26-03.5 [B]

**A small project.** A test-automation project costs $10 M now and returns $4 M a year for three years and $2 M in year 4 (assumed). (a) Find its NPV at 10%. (b) Find its IRR. (c) Find its simple payback.

### Problem 26-03.6 [B]

**A mature-node cost stack.** A 200 mm² die is made on 300 mm wafers costing \$12,000 at $D_0$ = 0.15 cm⁻². The package costs \$6.00 and assembly yields 98.5%; final test costs \$2.50 per unit tested and yields 96%; a royalty of \$0.50 is paid per unit sold; the ASP is \$95 (all assumed). Find (a) the dies per wafer, die yield and cost per good die; (b) the cost after assembly and after test; (c) the COGS; (d) the gross margin and markup.

### Problem 26-03.7 [B]

**Where yield loss hurts most.** Starting from Example 26-03.2, find the increase in COGS if (a) assembly yield falls from 99% to 97%, or instead (b) final-test yield falls from 98% to 96%. (c) Explain the difference.

### Problem 26-03.8 [B]

**Break-even at a mature node.** A 12 nm chip has $25 M of NRE, sells for $20 and contributes $8 a unit (assumed). (a) Find the break-even volume. (b) A competitor forces a 10% price cut with no change in cost. Find the new break-even volume and the percentage increase. (c) At the original price, the chip sells 5 million units over its life. Find the NRE per unit, the fully loaded cost and the fully loaded margin.

### Problem 26-03.9 [B]

**Pricing for a margin.** A chip costs $30 to make before royalties, and its royalty is 3% of the selling price (assumed). What ASP gives a 55% gross margin?

### Problem 26-03.10 [C]

**Price erosion.** A program spends $40 M of NRE in each of years 0 and 1 and sells 2, 5, 6 and 4 million units in years 2 to 5. ASP starts at $40 and falls 10% a year; COGS stays at $22 (all assumed). At a 12% MARR, find (a) the yearly ASPs, contributions and cash flows, (b) the NPV, and (c) the annual price erosion at which the NPV falls to zero.

### Problem 26-03.11 [C]

**Splitting the cost of a slip.** For Example 26-03.5's program: (a) find the present value of its sales cash flows; (b) find the NPV if every sales year is delayed by half a year with no loss of units (discount the sales by $1.12^{0.5}$ more); (c) repeat for a full year with no loss of units; (d) Example 26-03.5 found a \$39.9 M loss when the one-year slip also lost the year-5 units. What share of that loss is due to the closing window, and what share to discounting?

### Problem 26-03.12 [B]

**Testers with different lives.** Tester A costs $2.0 M, lasts 4 years and costs $0.3 M a year to run; tester B costs $3.0 M, lasts 6 years and costs $0.2 M a year (no salvage, assumed). At a 10% MARR, which has the lower equivalent annual cost, and by how much?

### Problem 26-03.13 [B]

**Depreciation and the tax shield.** Equipment costs $5.0 M, has a $0.5 M salvage value and a 5-year life. (a) Find the straight-line depreciation and the book value after 2 years. (b) At a 21% tax rate, find the annual tax saving from depreciation and its present value at 10% over 5 years.

### Problem 26-03.14 [C]

**A tornado.** For Example 26-03.5's program, compute the NPV change for a ±10% change in (a) ASP (the 2% royalty moves with it), (b) lifetime volume (all years scaled), (c) the manufacturing cost (COGS before the royalty, $35.61) and (d) NRE, and rank them. Use the discounted unit stream of 6.61 million units.

### Problem 26-03.15 [A]

**Fixed or variable?** Classify each cost as fixed (NRE or overhead) or variable (per unit), and say whether it falls in COGS: (a) production wafers; (b) the prototype mask set; (c) final-test time; (d) EDA licences; (e) per-unit patent royalties; (f) qualification testing (25-10).

### Problem 26-03.16 [B]

**A growing cost.** A test floor's maintenance costs \$50,000 in year 1 and rises by \$10,000 a year through year 5 (assumed). At 8%: (a) derive or evaluate $(P/G, 8\%, 5)$ and $(A/G, 8\%, 5)$; (b) find the present worth of the five years of maintenance; (c) find its equivalent uniform annual cost, and check it against (b).

### Problem 26-03.17 [B]

**Benefit–cost and the increment.** (a) A company endows a university chair that pays $300,000 a year forever; at 6%, what is its capitalized cost? (b) A yield-learning program costs $4.0 M now and $1.0 M a year for 4 years, and saves $3.0 M a year for those 4 years; an expanded version costs $6.0 M now and $1.2 M a year, and saves $3.8 M a year (all assumed). At 10%, find each version's B/C ratio and NPV (counting annual costs as costs). (c) Find the incremental B/C of the expanded version over the base, and choose.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Cost stack, margin and markup | 6, 7, 9, 15 |
| 2. NRE amortization and break-even | 8 |
| 3. Time-value factors and rates | 1, 2, 3, 4, 13, 16, 17 |
| 4. NPV, IRR, payback and slips | 5, 10, 11 |
| 5. Alternatives and sensitivity | 12, 14 |
