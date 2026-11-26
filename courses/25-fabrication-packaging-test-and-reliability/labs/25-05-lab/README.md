# Lab 25-05 · Corners, Back Bias, Shuttles and Shrinks

**Objective.** Simulate how global and local variation spread path delays around the corners; check the FD-SOI back-gate coupling formula against a numerical electrostatics solve; price shuttles against dedicated runs; and see how analog content limits the payoff of a shrink.

**Chapter:** [25-05 · Foundries, PDKs and Specialty Processes](../../chapters/25-05-foundries-pdks-specialty-processes.md)

## Background

§3.3 placed corners at ±3σ of global variation and used the alpha-power delay model to price them. §3.5 derived the back-gate coupling $C_{Si}C_{BOX}/[C_{ox}(C_{Si} + C_{BOX})]$ by treating the stack as series capacitors with the front surface pinned at threshold. §3.4 gave the shuttle break-even area, mask cost divided by price per mm².

## Files

- `foundry.py`: delay and corner ratios, a Monte Carlo of global plus local threshold shifts, the coupling formula and a finite-difference Laplace solve of the gate-oxide/silicon/BOX stack, shuttle cost and break-even, and die-area migration.
- `25-05-foundry-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Corners and local variation** (notebook). The global threshold spread is σ = 15 mV with the slow corner at +45 mV (3σ); each critical path adds a local σ = 10 mV (assumed). *Predict* the fraction of paths whose threshold exceeds the slow corner, then simulate 100,000 paths and plot the delay histogram with the corners marked.

**Part 2 · Back-gate coupling** (notebook). *Predict* how Example 25-05.5's coupling changes when the silicon body thins from 7 nm to 5 nm, then compute it with the formula and with the numerical solve, and sweep the BOX thickness.

**Part 3 · Shuttle or dedicated** (notebook). *Predict* the break-even area for a €3 M dedicated run on the €17,820/mm² shuttle, then compute it.

**Part 4 · Shrink economics** (notebook). Repeat Example 25-05.6 with analog and I/O at 60% of the 40 nm die (digital and NVM in a 2:1 ratio for the rest). *Predict* whether the die gets cheaper, then compute it and sweep the analog fraction.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 25-05.a | fraction of paths beyond the slow corner | 6.3e-3 | |
| Lab 25-05.b | coupling with a 5 nm body | 55.4 | mV/V |
| Lab 25-05.c | break-even area, €3 M | 168 | mm² |
| Lab 25-05.d | migrated area, 60% analog | 6.42 | mm² |
| Lab 25-05.d1 | die cost ratio, 60% analog | 1.16 | |

The simulated fraction is within 10% of the analytical value (Monte Carlo noise); the formula and the numerical solve agree to better than 0.01%.

## Discussion

1. Local variation pushes about five times as many paths past the slow corner as global variation alone (Problem 25-05.12). How do signoff methods account for it?
2. Thinning the body raised the coupling only slightly, while thinning the BOX doubled it. Why?
3. Why might a startup pay for a dedicated run even below the break-even area?
4. At what analog fraction does Example 25-05.6's shrink stop paying, and what does that say about mixed-signal product roadmaps?

## Optional hardware

None needed. Open PDKs (SkyWater SKY130, GF180MCU) can be downloaded and inspected: their DRC decks, SPICE corner models and pcells are the real counterparts of §3.2.
