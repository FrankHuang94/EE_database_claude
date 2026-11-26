# Problems 25-07 · Packaging II: 2.5D, 3D, Hybrid Bonding and Chiplets

Chapter: [25-07](../chapters/25-07-advanced-packaging-and-chiplets.md) · Worked solutions: [25-07 solutions](../solutions/25-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Reticle 26 mm × 33 mm = 858 mm² unless another basis is given.
- Shoreline wires per mm $N_{edge} = L/(w + s)$; bond density $1/p^2$.
- Hybrid-bond pads are $p/2$ wide and need $|e| \le p/4$ on each axis; die bond yield $[\operatorname{erf}(p/(4\sigma\sqrt{2}))]^2$.
- Anneal rise $\Delta T = \delta/[(\alpha_{Cu} - \alpha_d)t]$ with 17 and 0.5 ppm/K.
- Test escape $e = (1 - Y)(1 - c)/[Y + (1 - Y)(1 - c)]$; package yield $y_a^n\prod(1 - e_i)$.
- Cost per good package $[\sum(cA_i + t)/Y_i + P]/y_a^n$, with Example 25-07.9's values unless stated.
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/25-07-lab/chiplets.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 25-07.1 [A]

**Which reticle?** (a) Express TSMC's 2028 target of a 14-reticle interposer [R-587] in mm² on the 858 mm² and 830 mm² bases. (b) By what percentage do they differ? (c) Earlier 2027 targets were quoted as 6,864 mm² for 8 reticles and 7,722 mm² for 9 [R-587]. What reticle area does each imply?

### Problem 25-07.2 [A]

**Bridge pitch.** Intel's EMIB moved from 55 µm to 45 µm bump pitch, and EMIB-T was validated at 36/35 µm [R-591]. Find the bump-density gain (a) from 55 to 45 µm, (b) from 45 to 35 µm and (c) from 45 to 36 µm. SemiAnalysis described the 45 → 35/36 µm step as "a 65% increase in bump density". Which pitch does that match?

### Problem 25-07.3 [B]

**A thinner RDL.** An RDL interposer has only two routing layers at 2 µm/2 µm. (a) How many wires per millimetre of edge does it give? (b) How much edge do 2,048 HBM data wires need? (c) How many layers at this pitch fit the 2,048 wires into 2 mm of edge?

### Problem 25-07.4 [B]

**Smaller interposers.** *(lab)* (a) How many 40 mm × 40 mm interposers fit on a 300 mm wafer (exact count, no edge exclusion)? (b) What does the 25-04 formula predict? (c) How many packages a month does a line of 120,000 such wafers give at 95% package yield?

### Problem 25-07.5 [B]

**Reading capacity claims.** (a) Goldman Sachs projects 1.275 million CoWoS wafers for 2026 [R-588]. What monthly average is that? (b) Its projections of 2.73 million (2027) and 3.48 million (2028) imply what annual growth rates? (c) UBS projects industry capacity rising from 160,000 to 250,000 wafers a month between end-2026 and end-2027. What growth is that? (d) TSMC forecast a capacity CAGR above 80% for 2022–2027 and said it "nearly doubled" capacity each year for three years. What total growth does each imply? (e) Absolics' Phase 1 plant makes 12,000 m² of glass substrate a year, described as enough for two to three million H100-sized packages [R-595]. What substrate area per package does that imply?

### Problem 25-07.6 [B]

**Rotation.** A 10 mm × 10 mm die is hybrid-bonded at 6 µm pitch. (a) How far is a corner pad from the die centre? (b) What rotation, in microradians, moves that pad by the whole $p/4$ budget? (c) Express it in degrees.

### Problem 25-07.7 [B]

**Anneal budget.** (a) What temperature rise closes a 3 nm recess on a 0.5 µm pad? (b) If the anneal may rise only 225 K above room temperature, what is the largest recess a 1.0 µm pad can close?

### Problem 25-07.8 [C]

**Test escapes.** (a) Derive the escape-rate formula from Bayes' rule, stating your assumptions, and its approximation for coverage near 1. (b) Find the escape rate for die yield 0.5 and coverage 99%, exactly and by the approximation. (c) Find it for die yield 0.95 at the same coverage. What does the comparison teach?

### Problem 25-07.9 [B]

**Twelve stacks.** Repeat Example 25-07.8(b) for a package with 2 compute dies and 12 HBM stacks, the maximum of TSMC's 5.5-reticle CoWoS [R-587]. Find (a) the package yield, (b) the cost per good package for a kit of $5,400 and (c) the scrap overhead per good package.

### Problem 25-07.10 [C]

**Break-even area.** *(lab)* With Example 25-07.9's costs and a four-way split, find the total logic area at which chiplets and a monolithic die cost the same at $D_0$ = (a) 0.1, (b) 0.2 and (c) 0.05 cm⁻². Comment on (c).

### Problem 25-07.11 [B]

**Clustered defects.** Repeat Example 25-07.9 with negative-binomial yields, $\alpha$ = 2. Find (a) both die yields, (b) both costs, (c) their ratio and (d) the break-even $D_0$.

### Problem 25-07.12 [A]

**A taller HBM limit.** JEDEC was reported to be weighing a height limit of about 900 µm from HBM4E [R-594]. For a 20-high stack whose base die and mould cap take 160 µm (assumed, as in 23-05), find (a) the layer pitch and (b) the core-die thickness with a 10 µm microbump gap. What would it be with hybrid bonding and no gap?

### Problem 25-07.13 [B]

**Bridges for a 5.5-reticle package.** A 5.5-reticle package uses six 3 mm × 18 mm bridges instead of a full silicon interposer. Find (a) the ratio of silicon area and (b) the bridge sets per wafer, using Example 25-07.3's count.

### Problem 25-07.14 [C]

**Specifying a bonder.** (a) What placement σ gives 99.9% die bond yield at 4.5 µm pitch, and what is it as 3σ? (b) A bonder with 0.5 µm (3σ) placement must reach 99.9% die yield at 1 µm pitch. How large an error must each pad tolerate, and can any pad design on a 1 µm pitch provide it?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Reticle limits and interposer sizes | 1, 12 |
| 2. Interposers, RDL and bridges | 2, 3, 4, 13 |
| 3. 3D stacking and hybrid bonding | 6, 7, 14 |
| 4. Test escapes and package yield | 8, 9 |
| 5. Chiplet cost and break-even | 10, 11 |
| 6. Reading capacity and roadmap claims | 1, 5 |
