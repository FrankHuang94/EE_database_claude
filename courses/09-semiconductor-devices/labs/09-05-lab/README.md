# Lab 09-05 · PN Junction Electrostatics

**Chapter:** [09-05](../../chapters/09-05-pn-junction-electrostatics.md) · **Notebook:** [09-05-junction.ipynb](09-05-junction.ipynb) · **Time:** about 2 hours

## Objective

1. Reproduce the depletion-approximation results by integrating the charge numerically and root-finding the width.
2. Solve the full nonlinear Poisson equation for a step junction with Newton's method, and measure how soft the depletion edges really are.
3. Simulate a capacitance–voltage measurement and extract the doping and built-in potential from it.
4. Solve a linearly graded junction self-consistently.

## Background

Chapter sections 3.3–3.9 and Examples 09-05.2 to 09-05.7. In Part 2 the unknown is the potential $\psi(x)$ measured from the Fermi level, with Boltzmann carriers $n = n_ie^{q\psi/kT}$ and $p = n_ie^{-q\psi/kT}$; Newton's method linearizes $\psi'' + \rho(\psi)/\varepsilon_s = 0$ around the current guess and solves a tridiagonal system each step. You need Python with NumPy, SciPy and Matplotlib (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [09-05-junction.ipynb](09-05-junction.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s and the answer key below |

## Procedure

1. **Depletion approximation, numerically (Part 1).** *Predict first:* the width and peak field of the 10¹⁷/10¹⁶ cm⁻³ junction. Then integrate and compare with Example 09-05.2.
2. **The exact solution (Part 2, the chapter's guided exercise).** *Predict first:* the width of the n-side transition from 10% to 90% of $N_D$, in Debye lengths, and whether the exact peak field is larger or smaller than the approximation's. Then solve.
3. **C–V (Part 3).** *Predict first:* will the fitted doping be $N_D$, $N_A$ or something else? Then fit $1/C^2$ against $V_A$ for the P⁺N junction.
4. **Graded junction (Part 4).** *Predict first:* how $W$ changes when the grading constant rises a hundredfold. Then solve for $a$ = 10²⁰ and 10²² cm⁻⁴.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | step junction | $W$ = 0.3318 µm, peak field 4.665 × 10⁴ V/cm |
| 2 | exact solution | see the answer key |
| 3 | C–V fit | $N_AN_D/(N_A + N_D)$ = 4.998 × 10¹⁵ cm⁻³ and $V_{bi}$ = 0.875 V |
| 4 | graded junction | $W$ = 0.8029 µm ($a$ = 10²⁰) and 0.1860 µm ($a$ = 10²²) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 09-05.a | n-side transition, 10% to 90% | 140.9 | nm |
| Lab 09-05.b | transition in Debye lengths | 3.45 | — |
| Lab 09-05.c | exact peak field | 4.53e4 | V/cm |
| Lab 09-05.d | peak field below the approximation | 2.9 | % |
| Lab 09-05.e | width ratio for a hundredfold grading | 0.232 | — |

## Discussion questions

1. Why is the exact peak field slightly *lower* than the depletion approximation's?
2. The transition at each edge spans about three and a half Debye lengths. Why does it scale with $L_D$ and not with $W$?
3. In Part 3, why does the C–V fit return $N_AN_D/(N_A + N_D)$ rather than $N_D$, and when does the difference matter?
4. A hundredfold increase in the grading constant shrinks $W$ by a factor of about 4.3, not 10. Why?

<details><summary>Answers to the discussion questions</summary>

1. In the exact solution the depletion edges are soft: near them, carriers partly screen the dopant ions, so less ionic charge is uncovered than in the rectangular model. The field at the junction equals the total charge on one side divided by $\varepsilon_s$, so slightly less charge means a slightly lower peak.
2. Near the edge the potential differs from its bulk value by only a few $kT/q$, so Poisson's equation can be linearized there, and its solutions decay as $e^{-x/L_D}$: the Debye length is the only length in that linearized problem. The total width $W$ depends on $V_{bi}$, which only matters deep inside the depleted region.
3. The voltage changes the depletion edges on *both* sides; the capacitance is $\varepsilon_s/W$ with $W^2 \propto (1/N_A + 1/N_D)$, so the fit measures the series combination $1/(1/N_A + 1/N_D)$. It matters when the two dopings are within a factor of about ten of each other; for a P⁺N junction with 2000:1 asymmetry the difference is 0.05%.
4. $W \propto (V/a)^{1/3}$ for a graded junction, so a hundredfold $a$ shrinks $W$ by $100^{1/3}$ = 4.6 at fixed voltage, and the built-in potential also rises (from 0.667 to 0.830 V) because the edge doping rises, which widens $W$ slightly: the net ratio is **0.232**, a factor of **4.3**.

</details>

## Optional extension

Add forward bias to the Poisson solver by giving electrons and holes separate quasi-Fermi levels that differ by $qV_A$ across the junction (constant on each side), and watch the depletion approximation fail as $V_A$ approaches $V_{bi}$.
