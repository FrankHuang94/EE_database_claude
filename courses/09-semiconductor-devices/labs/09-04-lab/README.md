# Lab 09-04 · Generation, Recombination and the Continuity Equation

**Chapter:** [09-04](../../chapters/09-04-generation-recombination-continuity.md) · **Notebook:** [09-04-recombination.ipynb](09-04-recombination.ipynb) · **Time:** about 2 hours

## Objective

1. Integrate the four capture and emission processes of a trap level in time and confirm that the minority-carrier lifetime equals the minority capture time.
2. See how strongly generation depends on the trap's energy.
3. Solve the steady minority-carrier diffusion equation as a boundary-value problem and compare long and short regions with the closed forms.
4. Simulate a lifetime measurement on a wafer with recombining surfaces and see when the measurement reflects the surfaces rather than the bulk.

## Background

Chapter sections 3.4–3.8 and Examples 09-04.2, 09-04.3, 09-04.5 and 09-04.6. Part 1 integrates the rate equations for $n$, $p$ and the trap occupation $f_t$ with a stiff ODE solver; Part 4 discretizes the diffusion equation in space (method of lines) with Robin boundary conditions $D\,\partial\Delta p/\partial x = \pm S\Delta p$ at the two surfaces. The exact slowest decay mode of a wafer of thickness $W$ with equal surfaces satisfies $y\tan y = SW/2D$, with $1/\tau_{\text{eff}} = 1/\tau_b + D(2y/W)^2$. You need Python with NumPy, SciPy and Matplotlib (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [09-04-recombination.ipynb](09-04-recombination.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s and the answer key below |

## Procedure

1. **A trap in time (Part 1).** *Predict first:* in n-type silicon with gold-like traps, does the excess decay with $\tau_{p0}$, $\tau_{n0}$ or their sum? Then integrate and fit.
2. **Trap energy (Part 2).** *Predict first:* by how many decades does generation fall when the trap moves 0.3 eV from mid-gap? Then sweep.
3. **Diffusion profiles (Part 3).** *Predict first:* how much does the exact short-region current exceed the linear-profile estimate for $W$ = 5 µm and $L_p$ = 33.5 µm? Then solve.
4. **A lifetime measurement (Part 4, the chapter's guided exercise).** *Predict first:* the effective lifetime of a 300 µm, 1 ms wafer with $S$ = 10⁴ cm/s on both faces. Then simulate, and compare with the exact mode and with the weak-surface formula.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | decay time | equals $\tau_{p0}$ = 673 ns for $N_t$ = 10¹³ cm⁻³, within 2% |
| 2 | generation | peak 5.0 × 10¹⁵ cm⁻³ s⁻¹ at mid-gap; about 4.7 decades lower 0.3 eV away |
| 3 | short region | exact current 361.7 mA/cm², 0.7% above the linear estimate |
| 4 | effective lifetime | see the answer key |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 09-04.a | τ_p0 for N_t = 1e13 gold | 673 | ns |
| Lab 09-04.b | effective lifetime, S = 1e4 (exact mode) | 9.31 | µs |
| Lab 09-04.c | weak-surface formula, S = 1e4 | 1.50 | µs |
| Lab 09-04.d | surface-limited bound, S → ∞ | 8.07 | µs |
| Lab 09-04.e | effective lifetime, S = 10 (exact mode) | 601.1 | µs |
| Lab 09-04.f | weak-surface formula, S = 10 | 600.0 | µs |
| Lab 09-04.g | decades of generation lost at 0.3 eV | 4.7 | — |

## Discussion questions

1. In Part 1, why does the fitted decay not depend on the electron capture time $\tau_{n0}$, even though it is eighty times longer than $\tau_{p0}$?
2. Why does the weak-surface formula $1/\tau_{\text{eff}} = 1/\tau_b + 2S/W$ give 1.5 µs at $S$ = 10⁴ cm/s, *shorter* than the true 9.3 µs?
3. The effective lifetime cannot fall below about 8 µs however large $S$ becomes. What sets that floor?
4. A colleague reports "lifetime 10 µs" for a wafer that was not passivated. What can you conclude about its bulk lifetime?

<details><summary>Answers to the discussion questions</summary>

1. In n-type material the traps are almost all filled by electrons at every instant (electron capture is fast because electrons are plentiful: $c_nn_0 \gg c_pp$), so each recombination waits for a hole. The rate-limiting step is hole capture, $1/\tau_{p0}$; the electron capture time sets only how quickly an emptied trap refills, which is negligible.
2. The formula assumes carriers stay uniform across the wafer, so that the surfaces drain them at the full rate $S$. When $S$ is large, the surfaces empty the nearby region and carriers must diffuse there first; diffusion, not $S$, becomes the bottleneck, so the true loss rate is lower than the formula predicts. The validity condition $SW/2D \ll 1$ is badly violated: $SW/2D$ = **13.4** here.
3. With infinitely fast surfaces, the excess is pinned to zero at both faces and the slowest mode is a half-sine across the wafer, which decays at $D\pi^2/W^2$ in addition to bulk recombination. For $W$ = 300 µm and $D_p$ = 11.2 cm²/s that floor is about **8.07** µs: diffusion to the surfaces takes that long.
4. Almost nothing about the bulk, except that it is at least about 10 µs: the measurement is near the surface-limited floor, so the bulk could be 10 µs or 10 ms. The wafer must be passivated (or measured at several thicknesses) to extract the bulk value.

</details>

## Optional extension

Repeat Part 4 with one surface passivated ($S$ = 10 cm/s) and the other not ($S$ = 10⁴ cm/s), as in a solar cell before its back side is passivated. Find the effective lifetime, and compare it with the case of two bad surfaces.
