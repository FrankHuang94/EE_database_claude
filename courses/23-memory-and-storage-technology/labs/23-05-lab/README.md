# Lab 23-05 · An HBM Stack's Heat and an Interposer Link's Energy

Chapter: [23-05 · HBM in Depth](../../chapters/23-05-hbm-in-depth.md)

## Objective

Solve an HBM stack's one-dimensional thermal network with a circuit simulator, using the electrical analogy, and measure the supply energy of a short, unterminated interposer link. Then use the chapter's models to explore stack height, gap conductivity and bandwidth.

## Background

§3.5 derived the base die's temperature rise for a stack whose heat leaves through the top, and §3.2 the energy of charging an unterminated wire. The thermal-electrical analogy maps temperature to voltage, heat flow to current and thermal resistance to electrical resistance, so a resistor chain with current sources solves the stack exactly.

## Files

- `hbm_lab.cir`: Part A, the thermal ladder for 12 and 16 layers (0.04877 K/W per layer, 10 W base die, 1 W per core die); Part B, a 50 Ω driver charging a five-section, 25 Ω, 1.0 pF interposer line and a 0.3 pF load to 0.4 V.
- `hbm.py`: the chapter's models.
- `23-05-hbm-lab.ipynb`: the notebook for Parts 2 and 3.

## Procedure

**Part 1 · ngspice.**

1. Predict the base rise for 12 and 16 layers (Example 23-05.6) and the supply energy per rising transition (Example 23-05.3).
2. Run `ngspice -b hbm_lab.cir` and compare.
3. Double the driver resistance and run again. Predict first: does the energy change?

**Part 2 · Stack height and gap conductivity** (notebook). Sweep the layer count from 4 to 20 for gap conductivities of 1.5 and 3 W/m·K and for hybrid bonding. Find the largest layer count that keeps the base rise at or below 10 K with 1.5 W/m·K gaps, and the gap conductivity that would let a 16-high stack match a 12-high stack's rise.

**Part 3 · Bandwidth and capacity** (notebook). Tabulate bandwidth and capacity for each generation and vendor pin rate in Example 23-05.1, and the stacks needed for 1 TB of memory at 20 TB/s (treat both the 1 TB and the stacks' 36 GB as decimal, as vendor marketing does).

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 23-05.a | largest layer count with base rise ≤ 10 K (1.5 W/m·K gaps) | 12 | |
| Lab 23-05.b | gap conductivity for 16 layers to match 12 | 2.29 | W/m·K |
| Lab 23-05.c | 36 GB HBM4 stacks for 1 TB, both decimal | 28 | |
| Lab 23-05.e | rise growth, 12 to 16 layers | 1.51 | |
| Lab 23-05.f | linear-law growth, 12 to 16 layers | 1.33 | |
| Lab 23-05.g | square-law growth, 12 to 16 layers | 1.78 | |
| Lab 23-05.d | stacks for 20 TB/s at 2.048 TB/s each | 10 | |

- Part 1: the base rises within 0.1% of the closed form; the rising-transition energy within 0.5% of $CV^2$ = 0.208 pJ, and unchanged when the driver resistance doubles.
- Part 2: with gaps the rise grows faster than linearly with the layer count (from 12 to 16 layers it grows 1.51 times, between the 1.33 of a linear law and the 1.78 of a square law, because the base die's term is linear and the core dies' term quadratic); with hybrid bonding it stays below 1 K.

## Discussion

1. Why doesn't the driver's resistance change the energy per transition?

   <details><summary>Answer</summary>

   The supply delivers charge $CV$ at voltage $V$, so it supplies $CV^2$ whatever the path. Half is stored on the capacitance and half dissipated in the resistances; a larger resistance dissipates the same energy over a longer time (04-04, 23-01).

   </details>

2. Why does the base die's rise grow faster than the layer count?

   <details><summary>Answer</summary>

   Adding a layer adds one more resistance in the heat's path and one more die whose heat must cross all the layers above it. The total is a sum of an arithmetic series, so the core dies' contribution grows as $N(N - 1)/2$ (§3.5).

   </details>

3. What would change if heat could also leave through the bottom, into the interposer?

   <details><summary>Answer</summary>

   The stack would become a network with two exits, and the hottest die would move up from the base into the stack. In practice the interposer and substrate below are much more resistive than the lid above, so most heat still leaves through the top, but accurate models include both paths.

   </details>

## Optional hardware

An infrared camera on a GPU with its heat sink removed (and run only briefly at low power) shows the HBM stacks' surface temperatures next to the processor's. Compare their temperature with the processor's hot spots.
