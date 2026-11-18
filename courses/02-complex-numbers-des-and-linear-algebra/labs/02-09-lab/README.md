# Lab 02-09 · Systems of Linear ODEs and the Matrix Exponential

**Chapter:** [02-09](../../chapters/02-09-systems-of-odes-and-matrix-exponential.md) · **Notebook:** [02-09-state-space.ipynb](02-09-state-space.ipynb) · **Netlists:** [coupled_rc.cir](coupled_rc.cir), [thermal_analog.cir](thermal_analog.cir), [foster_pulse.cir](foster_pulse.cir) · **Time:** about 75 minutes

## Objective

1. Solve a state-space model three ways (eigenvectors, `expm`, a numerical ODE solver) and confirm they agree.
2. See why the Taylor series is a dubious way to compute $e^{\mathbf{A}t}$, and why scaling and squaring is used instead.
3. Read stability and trajectory shape from phase portraits and the trace–determinant plane.
4. Extract a datasheet-style Foster thermal model from a two-node physical model, and use it for pulses.
5. Compare exact zero-order-hold sampling with forward Euler, and find Euler's stability limit.
6. See how a sampled state-space layer's step size controls its memory.

## Background

Chapter sections 3.1–3.7, and Examples 02-09.2, 02-09.4, 02-09.5 and 02-09.6.

## Procedure

1. Run all notebook cells in order, writing down a prediction before each **🔮 Predict** cell.
2. **Part 2:** predict how many correct digits the Taylor series gives for $e^{-20}$.
3. **Part 3:** predict what happens to the spiral as its trace passes through zero.
4. **Part 4:** read the Foster model, and the largest stable Euler step for the thermal model.
5. **Part 5:** predict Euler's stability limit for the coupled capacitors.
6. **Part 6:** predict the memory length at τ/Δ = 20.
7. **Part 7:** from the repository root, run `python tools/run_spice.py 02-09`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | three solution methods | agree to about $10^{-13}$; $v_2$ peaks at 0.1925 at $t = 0.5493\tau$ |
| 2 | Taylor series for $e^{-20}$ | no correct digits (relative error near 200%); `expm` is accurate |
| 3 | spiral with trace $2a$ | decays for $a < 0$, closed orbits at $a = 0$ (a center), grows for $a > 0$; the center $x'' = -4x$ has period π s |
| 4 | Foster model of Example 02-09.5 | $R$ = 0.4616 and 1.538 K/W, τ = 0.9611 and 78.04 s; $Z_{th}$(0.1 s) = 0.04758 K/W; largest stable Euler step 1.922 s |
| 5 | coupled capacitors | Euler stable up to $T = 2\tau/3$ (0.66 ms stable, 0.67 ms unstable); exact sampling always stable |
| 6 | memory length | 1% decay after about $(\tau/\Delta)\ln100$ steps: 92.10 at τ/Δ = 20 (93 steps counted in the simulation) |
| 7 | ngspice | `coupled_rc.cir`, `thermal_analog.cir` and `foster_pulse.cir` match Examples 02-09.2 and 02-09.5 and Problems 02-09.9 and 02-09.14 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 02-09.a | Zth at 0.1 s, Example 02-09.5 | 0.04758 | K/W |
| Lab 02-09.b | memory length at τ/Δ = 20 | 92.10 | steps |
| Lab 02-09.c | largest stable Euler step, thermal model | 1.922 | s |
| Lab 02-09.d | period of the center x'' = −4x | 3.142 | s |

## Discussion questions

1. The thermal model's fastest time constant is about 1 s, but the quantity you care about (the sink temperature) settles over minutes. Why does an explicit simulator still have to take steps of about a second, and what would an implicit method buy?
2. Foster models cannot be cascaded, but every datasheet gives them. How would you build a junction-to-ambient model for a device mounted on a heat sink you designed?
3. A state-space sequence layer with a fixed Δ forgets at a fixed rate. Why might a model want Δ to depend on the input, as selective state-space models do?

## Optional hardware version

Build Example 02-09.2 with 1 kΩ resistors and 1 µF capacitors (τ = 1 ms). Charge capacitor 1 to a known voltage through a push-button from a supply, release it, and capture both capacitor voltages on a two-channel oscilloscope (single-shot trigger). Capacitor 2 should peak at about 19% of the starting voltage after about 0.55 ms. Either 1× or 10× probes are fine here: their loading (1–10 MΩ and at most a few hundred picofarads) is negligible against 1 kΩ and 1 µF.
