# Lab 01-10 · Multivariable Calculus II

**Chapter:** [01-10](../../chapters/01-10-multivariable-calculus-2.md) · **Notebook:** [01-10-vector-calculus.ipynb](01-10-vector-calculus.ipynb) · **Time:** about 60 minutes

## Objective

1. Evaluate double and triple integrals by adaptive quadrature and by Monte Carlo sampling, and measure how Monte Carlo error scales.
2. See how matching coordinates to the geometry reduces the work of a multiple integral.
3. Compute line integrals numerically, confirm path independence for a conservative field, verify Green's theorem, and see the "hole" of a wire-like field.
4. Count whole dies on a wafer and compare with the dies-per-wafer formula.

## Background

Chapter sections 3.1–3.4 (multiple integrals and coordinates), 3.5 (line integrals) and 3.8 (Green's theorem), and Example 01-10.3 (dies per wafer).

This chapter's lab has no ngspice netlist: its subject is fields and geometry rather than circuits. Course 13 develops field simulation.

## Procedure

1. Run all notebook cells in order.
2. **Part 1:** before running, predict how much the Monte Carlo error shrinks for 100× more samples.
3. **Part 2:** compare accuracy *and* the number of function evaluations in the two coordinate systems.
4. **Part 3:** confirm that both paths give the same answer for the conservative field, and that the wire-like field circulates only around loops that enclose the origin.
5. **Part 4:** before running, predict whether the die count depends on the grid's placement.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Monte Carlo error for N = 10², 10⁴, 10⁶ | about 5, 0.4, 0.04 W: 10× smaller per 100× samples ($1/\sqrt{N}$) |
| 1 | charged sphere | $Q = 1.047\times10^{-9}$ C, $E(R) = 941.2$ V/m |
| 2 | polar vs Cartesian | similar accuracy from $n$ instead of $n^2$ evaluations |
| 3 | conservative field, both paths | 2 |
| 3 | circulation of $(-y, x)$ at radius 2 | $8\pi$ = 25.13 |
| 3 | wire-like field | 2π around the origin, 0 around a loop that does not enclose it |
| 4 | 10 mm dies | formula 640; grid counts 640–657 depending on offset |
| 4 | 25 mm dies | formula 86.4; grid counts 86–93; 88 for the centered grid |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 01-10.a | Monte Carlo error reduction for 100× samples | 10 | — |
| Lab 01-10.b | dies-per-wafer formula, 25 mm dies | 86.4 | — |
| Lab 01-10.c | whole 25 mm dies, centered grid | 88 | — |

## Discussion questions

1. Monte Carlo error falls as $1/\sqrt{N}$ in any dimension, while a grid needs $n^d$ points. Above what dimension does Monte Carlo win? Where do high-dimensional integrals arise in chip design (hint: process-variation analysis)?
2. Why do whole-die counts vary with grid placement, and why does the variation matter more for large dies?
3. In Part 3, the wire-like field has zero curl everywhere it is defined, yet circulates. How does this square with Stokes' theorem?

## Optional hardware version

With a compass, a battery, a resistor (to limit the current to about 1 A briefly) and a long straight wire: place the compass a few centimeters from the wire and close the circuit for a moment. The needle deflects at right angles to the wire, following the circling field of Ampère's law. Move the compass around the wire and note that the deflection always points around it.
