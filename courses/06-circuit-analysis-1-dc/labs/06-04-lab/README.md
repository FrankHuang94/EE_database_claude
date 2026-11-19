# Lab 06-04 · Nodal Analysis: a Mini-SPICE and a Power Grid

**Chapter:** [06-04](../../chapters/06-04-nodal-analysis.md) · **Notebook:** [06-04-nodal.ipynb](06-04-nodal.ipynb) · **Time:** about 90 minutes (plus 45 minutes for the optional hardware part)

## Objective

1. Write a modified-nodal-analysis solver that reads a SPICE-style netlist, stamps every element and solves the system.
2. Confirm that it agrees with ngspice on the chapter's examples.
3. Compute the static IR drop of a power grid with a sparse matrix, and see how bump placement changes it.
4. Measure how dense and sparse solvers scale with the size of a grid.

## Background

Chapter sections 3.3 to 3.6 and Examples 06-04.1 to 06-04.5. You need Python with NumPy, SciPy and Matplotlib, and ngspice for Part 2 (see [SETUP.md](../../../../SETUP.md)); without ngspice the notebook skips the comparison and the rest still runs.

## Files

| File | What it does | Checks against |
|---|---|---|
| [06-04-nodal.ipynb](06-04-nodal.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [nodal.cir](nodal.cir) | Examples 06-04.1 to 06-04.4 and Problems 06-04.6, 06-04.7 and 06-04.13 (the diode, solved by ngspice's Newton iteration) | Chapter and solution answer keys |
| [ir_grid.cir](ir_grid.cir) | The 5 × 5 grid of Example 06-04.5 and the three 3 × 3 grids of Problem 06-04.10 | Chapter and solution answer keys |

Both netlists are run in CI by [`tools/run_spice.py`](../../../../tools/run_spice.py).

## Procedure

1. **A mini-SPICE (Part 1).** *Predict first:* how large is the MNA matrix of Example 06-04.3, and how many of its entries are zero? Then read the 40-line `mna()` function, run it on Examples 06-04.1, 06-04.3 and Problem 06-04.7, and print the matrix.
2. **Agree with ngspice (Part 2).** Run [nodal.cir](nodal.cir) and compare node voltages and source currents with the mini-SPICE.
3. **IR drop (Part 3).** Solve Example 06-04.5's grid with a sparse matrix and plot the drop map. *Predict first:* how much does a fifth bump at the center improve the worst drop, and where does the worst node move?
4. **Sparse versus dense (Part 4).** *Predict first:* how should each solver's time grow as the grid grows? Then time both for grids from 10 × 10 to 150 × 150 (dense only up to 50 × 50).

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Example 06-04.3's MNA matrix | 5 × 5, 13 nonzeros and 12 zeros; symmetric, with a zero 2 × 2 block for the two voltage sources |
| 2 | mini-SPICE versus ngspice | agreement to the six significant digits ngspice prints (for example $j_1$ = −3.33333 A) |
| 3 | worst IR drop | 20.6 mV at the center with four corner bumps; 10.0 mV with a fifth bump at the center, now at the middles of the edges |
| 4 | timing | dense time grows steeply (toward a factor of 8 per doubling of the unknowns); sparse time grows nearly in proportion to the unknowns; sparse wins by more than an order of magnitude at 50 × 50 (machine-dependent, not asserted) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 06-04.a | MNA size, Example 06-04.3 | 5 | — |
| Lab 06-04.b | zero entries in that matrix | 12 | — |
| Lab 06-04.c | worst drop with a fifth bump at the center | 10.0 | mV |
| Lab 06-04.d | unknowns with five bumps | 20 | — |

## Discussion questions

1. Your mini-SPICE and ngspice agree on every linear circuit. What would you have to add to `mna()` to handle the diode in `nodal.cir`?
2. Why does the MNA matrix have a zero block, and why does that matter for the choice of factorization?
3. The fifth bump halves the worst drop. Why does it not reduce it further, and where would a sixth bump help most?
4. Why can a chip's power grid not be analyzed with a dense solver, even on a large server?

<details><summary>Answers to the discussion questions</summary>

1. A Newton loop: start from a guess, replace the diode by its companion model (a conductance $g = f'(v)$ and a current source $f(v) - g v$, stamped like a resistor and a current source), solve, update the guess, and repeat until the change is below a tolerance (Problem 06-04.13). A practical simulator also limits each step of the junction voltage, because the exponential can overshoot badly from a poor guess.
2. A voltage source's constraint row $v_a - v_b = V_s$ contains no source current, and no source's current appears in another source's constraint, so the rows and columns belonging to the source currents meet in a block of zeros. The matrix is then not positive definite (a zero diagonal entry rules that out), so Cholesky factorization cannot be used; simulators use LU with pivoting chosen for both sparsity and numerical stability.
3. With a center bump, the worst nodes are the middles of the edges, each about two edges from its nearest bumps; the drop now depends on those paths, not on the center. A sixth bump helps most near the new worst nodes: placing bumps at the edge midpoints would attack exactly those. In a real chip, bumps are spread in a regular array for this reason.
4. Memory and time: a grid with $10^6$ nodes has a dense matrix of $10^{12}$ entries (8 TB in double precision), and dense LU would need about $3\times10^{17}$ operations. The sparse matrix has about $5\times10^6$ nonzeros (tens of megabytes), and sparse or iterative solvers handle it in seconds to minutes. Real power grids have far more than $10^6$ nodes, so only sparse methods are even possible.

</details>

## Optional hardware version

Build Example 06-04.1 at a safe scale: 2 kΩ, 2 kΩ and 4 kΩ resistors, with two bench supplies in constant-current mode delivering 4 mA and 1 mA (set each supply's voltage limit above 10 V so that it stays in current mode). Every voltage stays the same as in the example, because scaling resistances up by 1000 and currents down by 1000 leaves every product $iR$ unchanged. Measure $v_1$ and $v_2$ with a multimeter and compare with 7 V and 6 V. Then measure every resistor's voltage and confirm that the branch voltages around each loop sum to zero: KVL holds automatically for differences of node voltages.
