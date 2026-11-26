# Lab 25-06 · I/O, Escape Routing, Power Bumps and Joint Fatigue

**Objective.** Compute perimeter and area-array I/O, size substrate escape routing and power-bump budgets, map solder-joint strain over a bump array, and find how much the weakest joint shortens a package's fatigue life.

**Chapter:** [25-06 · Packaging I](../../chapters/25-06-packaging-fundamentals.md)

## Background

§3.2 compared perimeter I/O $4D/p_w$ with area-array I/O $(D/p_a)^2$. §3.3 gave the traces between pads, $\lfloor(p - d - s)/(w + s)\rfloor$, and the layers needed to escape $R$ rows. §3.5 derived joint shear strain $\gamma = \Delta\alpha\,\Delta T\,L_{DNP}/h$, Coffin–Manson life $N_f \propto \gamma^{-2}$, and the weakest-link Weibull scale $\eta_{pkg} = (\sum_i \eta_i^{-\beta})^{-1/\beta}$.

## Files

- `package.py`: I/O counts and crossover, escape routing, power bumps, a bump grid, joint strain, and the package's weakest-link life by formula and by Monte Carlo.
- `25-06-package-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Escape routing** (notebook). For a 150 µm array with 80 µm pads and 12 µm/12 µm lines, *predict* the layers needed to escape 15 rows, then compute them and sweep the line width.

**Part 2 · Strain map** (notebook). For a 25 mm × 25 mm die on a 150 µm grid, *predict* the fraction of joints whose strain is within 10% of the corner's, then compute it and plot the strain map.

**Part 3 · Weakest link** (notebook). For a 20 mm die on a 150 µm grid (Example 25-06.4's materials and cycle), with Weibull shape 4 and $N_f \propto \gamma^{-2}$, *predict* the package's characteristic life relative to its most-strained joint, then compute it by formula and by Monte Carlo.

**Part 4 · Power bumps** (notebook). *Predict* the power bumps for a 1,500 W die at 0.70 V with 0.2 A per bump, then compute them and sweep the supply voltage.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 25-06.a | escape layers, 80 µm pads, 12/12 µm | 5 | |
| Lab 25-06.b | joints within 10% of corner strain | 2.3 | % |
| Lab 25-06.c | package scale relative to corner joint | 0.178 | |
| Lab 25-06.c1 | equivalent number of corner joints | 990 | |
| Lab 25-06.d | power bumps, 1,500 W | 1.07e4 | |

The Monte Carlo mean first-failure life agrees with the Weibull formula's mean, $\eta_{pkg}\Gamma(1 + 1/\beta)$, within 2%.

## Discussion

1. Only about 2% of the joints are near the corner strain, yet the package behaves like about 990 corner joints. Where does the rest of the weakest-link penalty come from?
2. How would underfill change Part 3's answer if it cut every joint's strain by the same factor? If it cut corner strain more than centre strain?
3. Why do substrate makers quote line and space so prominently?
4. Lowering the core supply raises the current for the same power. What does that do to the bump budget, and what does that imply for low-voltage AI chips?

## Optional hardware

None needed. Cross-sections of a failed BGA package (often available from failure-analysis labs or in published teardowns) show the crack paths at corner joints predicted here.
