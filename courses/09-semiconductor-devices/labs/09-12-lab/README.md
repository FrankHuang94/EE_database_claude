# Lab 09-12 · Advanced Transistors

**Chapter:** [09-12](../../chapters/09-12-finfet-gaa-cfet-backside-power.md) · **Notebook:** [09-12-multigate.ipynb](09-12-multigate.ipynb) · **Time:** about 2 hours

## Objective

1. Solve the center-potential equation of a double-gate transistor along the channel by finite differences, and follow the barrier and DIBL as the body thins.
2. Solve Laplace's equation in two dimensions for a double-gate body with its oxides, and test the parabolic scale-length model against it.
3. Compare effective width and drive per footprint for fins and nanosheet stacks.
4. Solve a power-rail resistor ladder and compare front-side and backside power delivery.

## Background

Chapter sections 3.2–3.6 and Examples 09-12.1 to 09-12.6. The double-gate model: $u'' = u/\lambda^2$ along the channel, with $u$ = 0.2 V at the source and 0.2 V + $V_{DS}$ at the drain, $\lambda^2 = (\varepsilon_s/2\varepsilon_{ox})t_{si}t_{ox} + t_{si}^2/8$. Part 2 solves $\nabla\cdot(\varepsilon\nabla\phi) = 0$ on a 0.1 nm grid covering silicon and both oxides, with the gates as fixed-potential boundaries. There is no ngspice file: SPICE's built-in MOSFET levels do not model multigate electrostatics, and the BSIM-CMG compact model that does needs foundry parameters. You need Python with NumPy, SciPy and Matplotlib (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [09-12-multigate.ipynb](09-12-multigate.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s, which compare with the chapter's examples and the answer key below |

## Procedure

1. **The barrier (Part 1, the chapter's guided exercise).** *Predict first:* at $L$ = 20 nm, by what factor does DIBL fall when a double-gate body thins from 7 nm to 5 nm? Then compute it, and compare with the ratio $e^{L/2\lambda_5 - L/2\lambda_7}$ that the long-channel approximation predicts. Find the gate length at which the 7 nm body reaches 50 mV/V.
2. **Two dimensions (Part 2).** *Predict first:* will the full 2D solution show more or less barrier lowering than the parabolic model? Then solve and compare the center-potential minimum.
3. **Width per footprint (Part 3).** *Predict first:* how many 50 nm fins match a three-sheet stack? Then sweep sheet count and width.
4. **Power rails (Part 4).** *Predict first:* how does the worst-case drop change when a rail is fed from both ends instead of one? Then solve the ladder.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | DIBL at 20 nm, 7 nm and 5 nm bodies | 51.6 and 28.5 mV/V (Example 09-12.2) |
| 1 | DIBL ratio, its exponential estimate, and the 50 mV/V length | see the answer key |
| 2 | 2D barrier lowering against the parabolic model | agreement within a few percent |
| 3 | Fin-equivalent of a three-sheet stack | 2.04 (Example 09-12.3) |
| 4 | Worst-case drop, both ends against one end | 15.6 and 62.5 mV (Example 09-12.6) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 09-12.a | length where DIBL = 50 mV/V, 7 nm body | 20.3 | nm |
| Lab 09-12.b | DIBL ratio, 7 nm to 5 nm body at 20 nm | 1.81 | — |
| Lab 09-12.c | exponential estimate of that ratio | 1.85 | — |

## Discussion questions

1. Why does the exponential estimate slightly overstate the DIBL ratio?
2. Why does the parabolic approximation work so well for these thin bodies?
3. Why do nanosheet stacks stop paying off beyond a few sheets?
4. Why does feeding a rail from both ends cut the worst drop by four, not two?

<details><summary>Answers to the discussion questions</summary>

1. Thinning the body from 7 to 5 nm cuts DIBL by **1.81**×, while $e^{L/2\lambda_5 - L/2\lambda_7}$ predicts **1.85**×. The estimate uses only the leading exponential; at $L/\lambda$ ≈ 5 the exact minimum also depends on the $\sqrt{b}$ factor and the $\sinh$ terms, which weaken the dependence slightly. The 7 nm body reaches 50 mV/V at **20.3** nm.
2. Across a body only a few nanometers thick the potential has little room to bend, so a parabola in $y$ captures it well. The approximation degrades when the body becomes comparable to the gate length.
3. Each sheet adds width but also capacitance (fringing between gate and contacts) and series resistance in the taller source/drain; the IRDS notes that the energy–delay benefit "seems to quickly saturate and then decline with increasing device height".
4. Fed from both ends, each half carries half the current over half the resistance, and each half's drop is itself a one-end problem: $(I/2)(R/2)/2 = IR/8$, a quarter of $IR/2$.

</details>

## Optional extension

Extend Part 2 to a single-gate thin body on a thick buried oxide (replace the lower gate with a 20 nm oxide and a grounded substrate). Compare the barrier with the single-gate scale length of Problem 09-12.3, and see how much the back interface leaks compared with the front.
