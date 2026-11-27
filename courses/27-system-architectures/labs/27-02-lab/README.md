# Lab 27-02 · Inside a Phone SoC

**Objective.** Use small models of a phone SoC to see where big and small cores trade places, how leakage moves the most efficient frequency, how memory bandwidth bounds on-device AI, and what a die costs at 3 nm and 2 nm.

**Chapter:** [27-02 · The Smartphone SoC](../../chapters/27-02-smartphone-soc.md)

## Background

§3.2 derived energy per instruction $E = c(V_0 + kf)^2/\text{IPC} + P_s/(\text{IPC}\cdot f)$, its minimum-energy frequency and the big–little crossover. §3.3 gave LPDDR bandwidth $Rw/8$, the SLC's effect on DRAM traffic and the bandwidth bound on decode. §3.5 applied 25-04's die-cost model. All parameters are assumed, as in the chapter's examples.

## Files

- `socmodel.py`: LPDDR bandwidth and SLC traffic; voltage, energy per instruction and core power; energy at a performance target, the big–little crossover and the minimum-energy frequency; bandwidth-bound decode speed and DRAM energy per token; dies per wafer, yield and die cost; and the BOM memory-share shift.
- `27-02-soc-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Moving the crossover** (notebook). *Predict* the crossover performance of Example 27-02.2 if the little core's voltage slope falls from 0.30 to 0.25 V/GHz. Then plot both energy curves.

**Part 2 · Leakage and the best frequency** (notebook). *Predict* how the big core's minimum-energy frequency moves as leakage rises from 0.05 to 1.0 W. Then plot it.

**Part 3 · LPDDR6 and on-device models** (notebook). *Predict* the decode bound for the 3-billion-parameter, 2-bit model on a hypothetical 64 data-bit interface at LPDDR6's 14,400 MT/s. Then plot tokens/s against bits per weight for LPDDR5X-10667 and LPDDR6-14400.

**Part 4 · Die cost by node** (notebook). *Predict* the cost per good die of a 120 mm² die at 3 nm (\$18,500, $D_0$ = 0.10) and 2 nm (\$30,000, $D_0$ = 0.15). Then plot cost against area for both.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 27-02.a | crossover with a 0.25 V/GHz slope | 4.81 | GIPS |
| Lab 27-02.b | minimum-energy frequency, 0.05 W leakage | 0.578 | GHz |
| Lab 27-02.b1 | minimum-energy frequency, 1.0 W leakage | 2.20 | GHz |
| Lab 27-02.c | LPDDR6-14400 decode bound | 153.6 | tokens/s |
| Lab 27-02.c1 | gain over LPDDR5X-10667 | 35 | % |
| Lab 27-02.d | 120 mm² die cost at 3 nm | 39.51 | $ |
| Lab 27-02.d1 | 120 mm² die cost at 2 nm | 68.02 | $ |
| Lab 27-02.d2 | cost ratio | 1.72 | |

## Discussion

1. A gentler voltage curve on the little core moves the crossover up from 4.00 to **4.81** GIPS: a better small core takes over more of the workload, which is where most of a phone's battery goes.
2. The minimum-energy frequency rises from **0.578** GHz at 0.05 W of leakage to **2.20** GHz at 1.0 W. Leakage grows steeply with temperature, so a hot phone's governor should run faster and sleep sooner.
3. LPDDR6 at 14,400 MT/s raises the bound for the 2-bit model to **153.6** tokens/s, a 35% gain from the interface alone; halving the bits per weight doubles the bound on either interface.
4. A 120 mm² die costs **$39.51** at 3 nm and **$68.02** at 2 nm with the assumed early defect density. The 2 nm die costs **1.72** times as much, so the new node must deliver about 70% more value per die, through density, power or performance, to break even.

## Optional hardware

None needed. On an Android phone with developer options, watch the per-core frequencies while switching between an idle home screen, a web page and a game, and note when work moves from small to large cores.
