# Lab 07-04 · Laplace-Domain Circuit Analysis

**Chapter:** [07-04](../../chapters/07-04-laplace-domain-circuit-analysis.md) · **Notebook:** [07-04-laplace.ipynb](07-04-laplace.ipynb) · **Time:** about 2 hours

## Objective

1. Build a circuit's s-domain equations symbolically, and see that the determinant of the nodal matrix gives the same natural frequencies as 07-03's state matrix.
2. Solve a switched circuit with initial-condition sources and confirm it in the time domain.
3. See what a zero does to a step response by moving it.
4. Watch a pair of poles cross the imaginary axis as an amplifier's gain rises, and confirm it with ngspice's pole–zero analysis.

## Background

Chapter sections 3.2 to 3.8 and Examples 07-04.1 to 07-04.6. You need Python with NumPy, SciPy, SymPy and Matplotlib, and ngspice for the simulator checks (see [SETUP.md](../../../../SETUP.md)); without ngspice the notebook skips them.

## Files

| File | What it does | Checks against |
|---|---|---|
| [07-04-laplace.ipynb](07-04-laplace.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [examples.cir](examples.cir) | Examples 07-04.1, 07-04.2 and 07-04.3 in the time domain | Chapter answer key |
| [ex2_pz.cir](ex2_pz.cir) | ngspice's pole–zero analysis of Example 07-04.2's filter | Chapter answer key |
| [ex6_wien_pz.cir](ex6_wien_pz.cir) | ngspice's pole–zero analysis of the Wien bridge at K = 2.9 | Chapter answer key |
| [problems.cir](problems.cir) | Problems 07-04.4, 07-04.6 and 07-04.11 | Solution answer key |

The pole–zero analyses have netlists of their own because `.pz` reports the poles of everything in a netlist. Each netlist begins with `* EXPECT` lines naming the measurement and the published answer it must reproduce. Run them all from the repository root:

```bash
python tools/run_spice.py 07-04
```

## Procedure

1. **Determinants (Part 1).** *Predict first:* how many roots does the determinant of Example 07-04.2's nodal matrix have, and do any of them depend on where the output is taken?
2. **Initial conditions (Part 2).** *Predict first:* the initial and final values of Example 07-04.1's capacitor voltage, from the limit theorems alone.
3. **Moving a zero (Part 3).** *Predict first:* how the peak of Example 07-04.3 changes as its zero moves from −1000 s⁻¹ to −20 000 s⁻¹ with the poles and DC gain fixed (the chapter's guided exercise).
4. **Crossing the axis (Part 4).** *Predict first:* the Wien-bridge gain at which the poles reach the imaginary axis, and the oscillation frequency there.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | determinant | three roots, the same for every output: −6.283 Mrad/s and −3.142 ± j5.441 Mrad/s |
| 2 | Example 07-04.1 | starts at 8 V, ends at 12 V; 13.73 V at 0.5 ms |
| 3 | moving the zero | the peak falls from 6.066 V toward the all-pole 1.144 V (see the key) |
| 4 | Wien bridge | poles on the axis at K = 3, at 1.592 kHz |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 07-04.a | peak with the zero at −20 000 s⁻¹ | 1.173 | V |

## Discussion questions

1. In Part 1, why can the determinant's roots not depend on which node is the output?
2. In Part 2, the s-domain never asked for $dv_C/dt$ at $0^+$, which 07-03 needed. Where did that information go?
3. In Part 3, why does a zero far to the left of the poles barely change the response, while one close to the origin changes it a lot?
4. In Part 4, the simulator's `.pz` analysis and your symbolic determinant agree. What could make them disagree on a large circuit?

<details><summary>Answers to the discussion questions</summary>

1. The determinant is a property of the circuit's equations alone; the choice of output only changes the numerator (Cramer's rule replaces one column by the source vector). A natural frequency can be missing from a particular transfer function if it cancels, but it cannot move.
2. Into the initial-condition sources. The inductor's $L\,i_L(0^-)$ fixes the initial current through the capacitor, which is exactly what sets $dv_C/dt(0^+)$; the algebra carries it without you having to name it.
3. The zero adds $1/z$ times the derivative of the all-pole response. A zero far out ($z$ large) multiplies the derivative by a tiny factor; a zero near the origin multiplies it by a large one. At −20 000 s⁻¹ the extra term is a twentieth of what it is at −1000 s⁻¹.
4. ngspice's manual warns that its pole–zero search is a sub-optimal numerical method that may miss roots or report spurious ones on large circuits; closely spaced or nearly cancelling poles and zeros, and very different time scales, make the search harder. Cross-check with an AC sweep or a transient simulation.

</details>
