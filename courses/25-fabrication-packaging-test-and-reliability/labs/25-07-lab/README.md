# Lab 25-07 · Interposers, Hybrid-Bond Yield and Chiplet Cost

**Objective.** Count interposers per wafer, compute die-to-wafer hybrid-bond yield by formula and by Monte Carlo, and find where four chiplets break even against a monolithic die, with Poisson and clustered defects.

**Chapter:** [25-07 · Packaging II](../../chapters/25-07-advanced-packaging-and-chiplets.md)

## Background

§3.3 converted interposer wafers into packages, $W n_{wafer} Y_{pkg}$, with $n_{wafer}$ counted like dies per wafer (25-04). §3.5 derived the overlay budget $|e| \le p/4$ for pads half the pitch wide and the die bond yield $[\operatorname{erf}(p/(4\sigma\sqrt{2}))]^2$. §3.6 derived test escapes, and §3.7 the cost of a good package, $[\sum(cA_i + t)/Y_i + P]/y_a^n$.

## Files

- `chiplets.py`: reticle multiples, an exact count of rectangles on a wafer, shoreline wires, bond density, die bond yield (formula and Monte Carlo), the anneal rise, test escapes, package yield, and the monolithic and chiplet cost models with their break-even.
- `25-07-chiplets-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Interposers per wafer** (notebook). *Predict* how many 50 mm × 65 mm interposers fit on a 300 mm wafer, then count them exactly, compare with the 25-04 formula, and sweep the interposer size.

**Part 2 · Bond yield** (notebook). At 6 µm pitch with a placement σ of 0.6 µm per axis, *predict* the die bond yield, then compute it by formula and by Monte Carlo, and plot yield against σ/pitch.

**Part 3 · Clustered defects** (notebook). *Predict* how clustering ($\alpha$ = 2) moves Example 25-07.9's break-even defect density, then solve for it.

**Part 4 · Break-even area** (notebook). *Predict* the total logic area at which four chiplets match a monolithic die at $D_0$ = 0.1 cm⁻², then find it and plot both costs against area.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 25-07.a | 50 × 65 mm interposers per wafer | 14 | |
| Lab 25-07.a1 | formula estimate | 10.1 | |
| Lab 25-07.b | die bond yield, sigma 0.6 µm | 97.53 | % |
| Lab 25-07.c | break-even D0, alpha = 2 | 0.067 | cm⁻² |
| Lab 25-07.d | break-even logic area at 0.1 cm⁻² | 562 | mm² |

The Monte Carlo bond yield (200,000 dies) agrees with the formula within 0.1 percentage point.

## Discussion

1. Why does the 25-04 dies-per-wafer formula underestimate the count for interposers this large, and what would edge exclusion and saw streets do to the exact count?
2. Part 2 assumes each axis's error is independent and Gaussian. How would a systematic offset shared by every die (a bonder calibration error) change the yield curve?
3. Part 3's clustered yields favour the monolithic die. Which kind of defect (random particles or systematic, layout-dependent defects) would you expect to dominate early in a new node, and what does that imply for the first chiplet products on it?
4. The cost model ignores edge loss. Rebuild it with the exact dies-per-wafer count for each die size. Does the break-even area move up or down, and why?

## Optional hardware

None needed. Published cross-sections of hybrid-bonded stacks (for example in IEDM and ECTC papers) show the bonded copper pads and the oxide interface modelled here.
