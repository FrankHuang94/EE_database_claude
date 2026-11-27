# Lab 25-04 · Dies, Defects and Dollars

**Objective.** Count dies exactly and compare with the formula; simulate random and clustered defects and compare with the yield models; find how cost per good silicon grows with die area; and see how learning speed moves the yield schedule.

**Chapter:** [25-04 · Yield Models and Die Cost](../../chapters/25-04-yield-and-die-cost.md)

## Background

§3.1 gave the dies-per-wafer estimate $\pi d^2/(4A) - \pi d/\sqrt{2A}$. §3.2–3.3 derived the Poisson yield $e^{-AD_0}$ and, by letting the defect density vary as a gamma distribution, the negative-binomial yield $(1 + AD_0/\alpha)^{-\alpha}$. §3.4 defined cost per good die, and §3.5 modelled defect density falling exponentially toward a floor.

## Files

- `yieldcost.py`: the formula and an exact die count over grid offsets, the three yield models, a Monte Carlo of defects per die (uniform or gamma-mixed density), cost per good die and per good mm², harvesting, and the month a yield target is reached.
- `25-04-yieldcost-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Counting dies** (notebook). For 10.1 mm die pitch on a 294 mm usable diameter (Example 25-04.1), *predict* whether an optimized grid beats the formula's 601, then search grid offsets and plot the best layout.

**Part 2 · Clustering** (notebook). For 1 cm² dies at an average 1 cm⁻², *predict* the yield with uniform defects and with gamma-clustered defects ($\alpha$ = 3), then simulate 2,000 wafers of 600 dies each and compare with the formulas.

**Part 3 · Cost against area** (notebook). On a \$20,000 wafer with $D_0$ = 0.1 cm⁻² and $\alpha$ = 3, *predict* the die area at which cost per good mm² is twice that of a 50 mm² die, then sweep the area.

**Part 4 · Learning** (notebook). *Predict* when Example 25-04.4's 1 cm² die reaches 80% yield if the learning time constant halves to 3 months, then compute it and plot both learning curves.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 25-04.a | exact dies per wafer, 10.1 mm pitch | 612 | |
| Lab 25-04.b | clustered yield, alpha = 3, AD0 = 1 | 0.422 | |
| Lab 25-04.b1 | uniform (Poisson) yield, AD0 = 1 | 0.368 | |
| Lab 25-04.c | area at which cost per good mm² doubles | 602 | mm² |
| Lab 25-04.d | month for 80% with tau = 3 months | 3.1 | months |

The simulated yields fall within 1% of the formulas.

## Discussion

1. Why does an optimized grid beat the formula, and by more for some die sizes than others?
2. In Part 2 the clustered simulation has the same average defect count per die as the uniform one. Where do its "extra" defects go?
3. Beyond about 600 mm², every square millimetre costs twice as much as at 50 mm². How does that shape the choice between a monolithic die and chiplets?
4. What could a fab do to halve its learning time constant, and what would it cost?

## Optional hardware

None needed.
