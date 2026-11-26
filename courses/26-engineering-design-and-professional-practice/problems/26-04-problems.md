# Problems 26-04 · Engineering Economics II: Build, Buy or License; Node; Chiplets; ASIC vs Merchant

Chapter: [26-04](../chapters/26-04-engineering-economics-2.md) · Worked solutions: [26-04 solutions](../solutions/26-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Cash flows occur at the ends of years; NRE and upfront fees are paid at year 0 unless stated.
- Dies per wafer use 25-04's formula $\pi d^2/(4A) - \pi d/\sqrt{2A}$ on 300 mm wafers, rounded down; die yield is Poisson, $e^{-AD_0}$.
- "Assumed" values are illustrative. Problems that build on a worked example keep all of its assumptions except those stated.

---

## Problems

### Problem 26-04.1 [A]

**Royalty conversions.** (a) A $0.45 per-unit royalty is paid on a chip that sells for $18. What percentage of the ASP is it? (b) What is a 1.5% royalty on a $22 chip, per unit? (c) A patent holder asks 0.5% of the price of a $300 phone, and the chip that implements the patent sells for $15. What chip-level percentage is that? (d) The chip in (c) has a 55% gross margin before this royalty. What is its margin after?

### Problem 26-04.2 [A]

**Build or license?** For each block, say whether you would build or license it, and give the main reason: (a) a USB PHY in a camera SoC; (b) the neural-network engine that is the main reason customers choose a vision chip; (c) a PCIe controller for a company's first PCIe product, due in nine months; (d) the SerDes in a network switch whose products compete on how far their links reach; (e) the standard-cell library for a foundry process.

### Problem 26-04.3 [B]

**A memory controller.** Building a DDR memory controller costs $9 M of NRE; a licence costs $1.5 M up front plus $0.25 per unit (assumed; ignore discounting). (a) Find the break-even volume. (b) At a planned 20 million units, which option is cheaper, and by how much? (c) The in-house design has a 20% chance of a respin that costs $6 M. Find the new break-even volume.

### Problem 26-04.4 [B]

**Discounted break-even with NRE over two years.** Building a block costs $10 M at year 0 and $10 M at year 1. A licence costs $4 M at year 0 plus $0.60 per unit. The chip ships 2, 6, 8, 6 and 3 million units in years 2 to 6, and the MARR is 10% (all assumed). Find (a) the discounted unit stream, (b) the present cost of each option and the cheaper one, and (c) the discounted break-even volume and its multiple of the plan.

### Problem 26-04.5 [B]

**Who bears price erosion?** A chip's ASP is $25 in year 1 and falls 20% a year; it ships 10 million units a year in years 1 to 4. A licensor offers $0.40 per unit or 1.6% of ASP; the MARR is 10% (all assumed). (a) Find the per-unit royalty in each year under the percentage form. (b) Find the present value of each form. (c) Find the per-unit royalty with the same present value as the percentage form. (d) The licensor expects only 10% erosion a year. What present value does it expect from the percentage form, and which form will each side prefer?

### Problem 26-04.6 [B]

**Royalty stacking in an SoC.** An SoC sells for $30 and costs $14 to make before royalties. It pays 1.5% of ASP for its CPU cores, $0.20 per unit for its GPU, $0.05 for its interconnect, $0.30 for its SerDes and $0.25 to a video-codec patent pool (all assumed). Find (a) the total royalty per unit, (b) as a percentage of ASP, (c) the gross margin before and after royalties, and (d) the share of the pre-royalty gross profit the royalties take.

### Problem 26-04.7 [B]

**The mix decides the shrink.** Using the N3-over-N5 gains of Example 26-04.3 (1.7× logic, 1.2× SRAM, 1.1× analog), find the effective density gain for (a) an AI accelerator die that is 60% logic, 35% SRAM and 5% analog, and (b) a microcontroller that is 20% logic, 50% SRAM (and flash interface) and 30% analog. (c) What area does a 400 mm² accelerator die at N5 shrink to? (d) Explain why the two designs gain so differently.

### Problem 26-04.8 [C]

**Reading a density claim.** TSMC quoted a 1.3× "chip density" gain for N3E over N5, for a die of 50% logic, 30% SRAM and 20% analog [R-360]. Assume analog gains 1.1×. (a) If SRAM macros do not shrink at all (N3E's bitcell is the same size as N5's [R-464]), what logic gain does the claim imply? (b) Repeat assuming SRAM macros gain 1.1× from smaller periphery. (c) What does the difference tell you about comparing density claims?

### Problem 26-04.9 [B]

**When does a new node stop paying?** (a) For Example 26-04.3's die (effective gain 1.378, equal yields, edge effects ignored), find the N3 wafer price at which cost per function equals N5's at $17,000. (b) Suppose N2 wafers cost $30,000 against $20,000 for N3E and the effective density gain is 1.15× (both assumed; public reports put N2 at $30,000 or more [R-575]). By what factor does cost per function change? (c) What effective density gain would make N2 cost-neutral?

### Problem 26-04.10 [B]

**A young node's yield.** For Example 26-04.3: (a) find the N3 defect density at which the N3 die costs the same as the N5 die; (b) suppose N3's defect density is 0.25 cm⁻² in year 1, 0.15 in year 2 and 0.10 in year 3, while the chip ships 1, 2 and 3 million units in those years. Find the N3 yield, die cost and saving per die in each year, and the total undiscounted saving. Does N3 repay its $30 M of extra NRE over these 6 million units?

### Problem 26-04.11 [C]

**A third product.** Add product XL to Example 26-04.4: four compute blocks and the I/O. Monolithic, it is one 650 mm² N3 die (still within the 858 mm² reticle field) in a $15 package, with $110 M of NRE. With chiplets it uses four compute chiplets and the I/O die in a $50 package, with $8 M of integration NRE. It ships 0.5 million units (all assumed). Find (a) the monolithic die's dies per wafer, yield and good-die cost, (b) the package cost each way, (c) the incremental cost of adding XL to each family, and (d) the three-product family totals.

### Problem 26-04.12 [B]

**What the older node is worth.** In Example 26-04.4, suppose the I/O die were made on N3 instead of N6 (55 mm², $20,000 wafers, $D_0$ = 0.10 cm⁻², $2 test). Find (a) its dies per wafer, yield and good-die cost, (b) the chiplet S package cost, and (c) the extra cost per S unit.

### Problem 26-04.13 [B]

**Expensive power.** Repeat Example 26-04.5 with electricity at $0.12/kWh and a 5-year service life, other assumptions unchanged. Find (a) each accelerator's energy cost, (b) the cost per merchant-equivalent of each, (c) the saving, and (d) the break-even fleet in merchant-equivalents and in custom chips. (e) Why does the break-even fleet fall?

### Problem 26-04.14 [C]

**How low can the merchant go?** In Example 26-04.5, suppose instead that the merchant's gross margin at $30,000 is 70%. (a) What is its unit cost? (b) What merchant price makes a 100,000-chip custom fleet exactly break even, and what margin does the merchant keep at that price? (c) Show that if the merchant priced at its unit cost, the custom program would not pay at any fleet size. What does that say about where the custom chip's advantage comes from?

### Problem 26-04.15 [C]

**More on the option to build later.** For Example 26-04.6: (a) at $p$ = 0.3, what port cost would make building now tie with licensing now and choosing later? (b) If the port cost is $1 M, above what probability of the high-volume outcome should the team build now? (c) At $p$ = 0.6 (port cost $3 M), find the expected cost of each strategy, the best one, and the value of flexibility against licensing both generations.

### Problem 26-04.16 [B]

**The design partner's margin.** A custom accelerator's silicon, HBM, package and test cost the design partner $6,000 per unit (assumed). (a) What does the buyer pay per unit at a partner gross margin of 40%, and at 60%? (b) Using Example 26-04.5's other assumptions, find the custom cost per merchant-equivalent, the saving and the break-even fleet at the 60% price. (c) If the merchant's unit cost were also $6,000, how much gross profit per unit would it earn at $30,000, how much would the partner earn at the 40% price, and how much of the merchant's margin does the buyer capture per chip before throughput and NRE?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. License against build, with risk and discounting | 2, 3, 4 |
| 2. Royalty forms and who carries the risk | 1, 5, 6 |
| 3. Node choice by cost per good function | 7, 8, 9, 10 |
| 4. Monolithic against chiplets for a family | 11, 12 |
| 5. Custom against merchant TCO | 13, 14, 16 |
| 6. Decision trees and flexibility | 15 |
