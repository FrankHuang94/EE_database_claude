# Problems 25-04 · Yield Models and Die Cost

Chapter: [25-04](../chapters/25-04-yield-and-die-cost.md) · Worked solutions: [25-04 solutions](../solutions/25-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Dies per wafer use $\pi d^2/(4A) - \pi d/\sqrt{2A}$ on a 300 mm wafer with no edge exclusion unless stated.
- Negative-binomial yield is $(1 + AD_0/\alpha)^{-\alpha}$; Poisson is $e^{-AD_0}$.
- Cost per good die is wafer cost ÷ (DPW × yield), excluding test and packaging unless stated.
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/25-04-lab/yieldcost.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 25-04.1 [A]

**Area matters.** With Poisson defects at $D_0$ = 0.2 cm⁻², find the yield of (a) a 0.5 cm² die and (b) a 4.0 cm² die.

### Problem 25-04.2 [C]

**Deriving Murphy's model.** (a) Let defect density be triangular on $[0, 2D_0]$, peaking at $D_0$. Show that averaging $e^{-AD}$ over it gives $Y = [(1 - e^{-AD_0})/(AD_0)]^2$. (b) Evaluate it at $AD_0$ = 2.

### Problem 25-04.3 [B]

**Three models for a big die.** At $AD_0$ = 2, compare Seeds' model ($\alpha$ = 1), the negative binomial with $\alpha$ = 3 and Poisson.

### Problem 25-04.4 [B]

**A reticle-sized die.** *(lab)* Estimate dies per wafer for a 25 mm × 30 mm die, showing both terms of the formula.

### Problem 25-04.5 [B]

**Its cost.** For Problem 25-04.4's die on a $30,000 wafer with $D_0$ = 0.1 cm⁻² and $\alpha$ = 3 (assumed), find (a) the yield, (b) the good dies per wafer and (c) the cost per good die.

### Problem 25-04.6 [C]

**Splitting into chiplets.** *(lab)* The same design is split into four chiplets, each a quarter of the area plus 10% for die-to-die interfaces (assumed), on the same wafer and process. Find (a) each chiplet's area, (b) its dies per wafer, (c) its yield and (d) its cost per good chiplet. (e) What is the silicon cost of one product, and how much packaging, assembly and test cost could the chiplet version absorb before it loses its advantage?

### Problem 25-04.7 [B]

**Memory repair.** A 1.0 cm² SRAM array sees Poisson defects at 0.2 cm⁻². (a) What is its yield without repair? (b) With spares that can repair up to two defects?

### Problem 25-04.8 [B]

**A 16-core die.** Each of 16 cores is defect-free with probability 0.97, and the uncore logic with probability 0.95 (assumed). Find the probability that (a) all cores work and (b) at least 15 work.

### Problem 25-04.9 [B]

**Faster learning.** *(lab)* Repeat Example 25-04.4 with the learning time constant halved to 3 months. When does the 1 cm² die reach 80% yield?

### Problem 25-04.10 [B]

**An older fab.** IBS estimated about $20 B for a 3 nm fab of similar capacity (50,000 wafer starts per month) [R-575]. With five-year straight-line depreciation and full loading, find (a) the depreciation per wafer and (b) its share of a $20,000 wafer price.

### Problem 25-04.11 [A]

**Break-even density.** If an N2 wafer costs $30,000 and an N3 wafer $20,000, what density gain would N2 need for equal cost per transistor at equal yield?

### Problem 25-04.12 [B]

**What does 50% mean?** A reported 50% yield [R-574] is assumed to refer to a 100 mm² die. Find the implied defect density under (a) the Poisson model and (b) the negative binomial with $\alpha$ = 3.

### Problem 25-04.13 [B]

**Critical area by layer.** A die's critical areas and killer-defect densities for three layers are 0.3 cm² at 0.3 cm⁻², 0.2 cm² at 0.5 cm⁻² and 0.4 cm² at 0.2 cm⁻² (assumed). Find (a) the expected killer defects per die and (b) the Poisson yield.

### Problem 25-04.14 [B]

**Separating systematic loss.** A product of 1.0 cm² dies measures 72% yield. Inline inspection suggests random killer defects at 0.15 cm⁻². Under the Poisson model, find (a) the random-defect yield and (b) the implied systematic yield.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Dies per wafer | 4, 6 |
| 2. Yield models and their derivations | 1, 2, 3, 13 |
| 3. Cost per good die, redundancy and harvesting | 5, 6, 7, 8 |
| 4. Yield learning | 9 |
| 5. Wafer cost and cost per transistor | 10, 11 |
| 6. Reading yield claims | 12, 14 |
