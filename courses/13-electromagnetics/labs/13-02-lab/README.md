# Lab 13-02 · Electrostatics: Boundary-Value Problems

Chapter: [13-02 Electrostatics: Boundary Conditions and Boundary-Value Problems](../../chapters/13-02-electrostatics-boundary-value-problems.md)

## Objective

Solve Laplace's equation numerically and check the solution against the series of §3.5; compute the capacitance of a strip over a ground plane, including fringing, from the stored energy; integrate the charge induced on a ground plane by a point charge; and solve the trough with an analogue computer, a grid of equal resistors, in ngspice.

## Background

Boundary conditions (§3.2), Laplace and Poisson (§3.3), uniqueness (§3.4), separation of variables (§3.5), images (§3.6) and finite differences (§3.7).

## Files

- [13-02-electrostatics.ipynb](13-02-electrostatics.ipynb): the notebook (Parts 1–4).
- [resistor_grid.cir](resistor_grid.cir): a 5 × 5 grid of 1 kΩ resistors with the top edge at 1 V and the other edges grounded. Run with `ngspice -b resistor_grid.cir`, or `python tools/run_spice.py 13-02` from the repository root.

## Procedure

1. **Finite differences (Part 1).** Solve the square trough on grids of spacing $a/10$ to $a/160$ and plot the error at $(a/2, 3a/4)$ against the spacing on log axes. *Predict first:* what slope will the error line have?
2. **A strip over a ground plane (Part 2).** Compute the capacitance per length of a zero-thickness strip of width $w$ at height $h$ over a ground plane in air, for $w/h$ from 0.5 to 10, from the stored energy, and divide by the parallel-plate value $\varepsilon_0w/h$.
3. **Images (Part 3).** Map the potential of a charge above a plane with its image, and integrate the induced surface charge over growing discs.
4. **Refraction (Part 4).** Plot field lines crossing an interface for several permittivity ratios.
5. **ngspice (the chapter's guided exercise).** Predict the centre node's voltage, then run `resistor_grid.cir`. Compare the node one row above the centre with the continuous series at the same point.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Error against grid spacing | A straight line of slope 2 on log axes: halving the spacing quarters the error |
| 2 | Fringing factor | Well above 1 for narrow strips, falling slowly toward 1 as $w/h$ grows |
| 3 | Induced charge | Tends to $-Q$ as the disc grows; about 29% lies within one height of the foot |
| 4 | Refraction | Lines bend away from the normal entering the higher-permittivity side |
| ngspice | Grid voltages | Centre exactly 0.25 V; the node above it within 0.005 V of the continuous solution |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 13-02.a | grid node above the centre, at (a/2, 2a/3) | 0.41925 | V |
| Lab 13-02.b | continuous series at the same point | 0.4238 | V |
| Lab 13-02.c | strip fringing factor C'/(ε₀w/h) at w = h (grid h/30, box 20h × 10h) | 3.04 | — |

*These are recomputed by [verify_13_02.py](../../verify/verify_13_02.py) with its own finite-difference solver and series.*

## Discussion questions

1. Why is the grid's centre voltage exactly 0.25 V however coarse the grid, while the node above it differs from the continuous value?
2. Why does fringing matter more for narrow strips?
3. In Part 3, why does the induced charge converge so slowly with the disc radius?

### Answers

1. The discrete equations have the same symmetry and linearity as the continuous ones: the four rotations of the problem superpose to a grid held entirely at 1 V, and the centre is shared equally by all four. Away from the centre there is no such argument, and the discretization error, of order $h^2$, shows.
2. The parallel-plate estimate counts only the field directly under the strip. The fringing field around the edges adds roughly a fixed amount per edge, which is a large fraction of the total when the strip is narrow and a small one when it is wide.
3. The surface charge density falls only as $1/r^3$, so the charge outside radius $R$ falls as $h/R$: to capture 99% of it the disc must reach about 100 heights.

## Optional hardware extension

Build the 5 × 5 resistor grid on a breadboard with 1 kΩ resistors (1% tolerance), hold the top row of junctions at a known voltage from a bench supply, and measure the interior nodes with a multimeter. Compare with the ngspice values and estimate how much the resistor tolerance moves them.
