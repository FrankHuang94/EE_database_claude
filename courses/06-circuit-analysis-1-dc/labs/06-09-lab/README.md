# Lab 06-09 · Maximum Power Transfer

**Chapter:** [06-09](../../chapters/06-09-maximum-power-transfer.md) · **Notebook:** [06-09-maxpower.ipynb](06-09-maxpower.ipynb) · **Time:** about 60 minutes (plus 45 minutes for the optional hardware part)

## Objective

1. Find maximum power by sweeping a load in ngspice, and see how flat the maximum is.
2. Confirm that the power–efficiency tradeoff $p/p_{max} = 4\eta(1 - \eta)$ holds for every source that is a voltage behind a physical series resistance.
3. Track the maximum-power point of a linear source and of a nonlinear (solar-cell) source with a perturb-and-observe algorithm.
4. Reproduce the coax optima behind the 50 Ω and 75 Ω standards, and see how the dielectric moves them.

## Background

Chapter sections 3.1 to 3.5 and Examples 06-09.1 to 06-09.5. You need Python with NumPy, SciPy and Matplotlib, and ngspice for Part 1 (see [SETUP.md](../../../../SETUP.md)); without ngspice the notebook skips the simulator cell.

## Files

| File | What it does | Checks against |
|---|---|---|
| [06-09-maxpower.ipynb](06-09-maxpower.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [maxpower.cir](maxpower.cir) | Load-voltage sweeps for Examples 06-09.1, 06-09.2 and 06-09.4 and Problems 06-09.1, 06-09.5 and 06-09.12 | Chapter and solution answer keys |

The netlist is run in CI by [`tools/run_spice.py`](../../../../tools/run_spice.py).

## Procedure

1. **Load sweeps (Part 1).** *Predict first:* the peak power for 10 V behind 8 Ω, and the power with the load a factor of 2 off.
2. **One curve (Part 2).** *Predict first:* will random sources and loads fall on $4\eta(1 - \eta)$?
3. **Tracking (Part 3).** *Predict first:* will the tracker settle at half the open-circuit voltage for both the TEG and the solar cell?
4. **Coax (Part 4).** *Predict first:* does the dielectric change the optimal ratios $b/a$, or only the impedances?

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | peaks | 3.125 W (Example 06-09.1), 360 W, 31.25 mW, 2304 W, 10.71 W; a factor-2 mismatch keeps 88.9% |
| 2 | tradeoff | every point on $4\eta(1 - \eta)$ to rounding error |
| 3 | tracking | TEG: 0.25 V = 50% of $V_{oc}$; solar cell: $V_{oc}$ = 0.6874 V, maximum-power point 0.5800 V (84.4% of $V_{oc}$), 27.18 mW |
| 4 | coax | optimal ratios 3.591 and 1.649 for any dielectric; 50 Ω has 10.3% extra loss in air, 0.2% in PTFE |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 06-09.a | power kept with a factor-2 mismatch | 88.9 | % |
| Lab 06-09.b | solar-cell open-circuit voltage | 0.6874 | V |
| Lab 06-09.c | solar-cell maximum-power voltage | 0.5800 | V |
| Lab 06-09.d | solar-cell maximum power | 27.18 | mW |
| Lab 06-09.e | maximum-power voltage as a fraction of V_oc | 84.4 | % |
| Lab 06-09.f | power at V_oc/2 as a fraction of the maximum | 63 | % |
| Lab 06-09.g | efficiency giving half the maximum power (low) | 14.6 | % |
| Lab 06-09.h | efficiency giving half the maximum power (high) | 85.4 | % |
| Lab 06-09.i | minimum-loss Z_0 with ε_r = 1.4 | 64.8 | Ω |

## Discussion questions

1. Why does the perturb-and-observe tracker oscillate around the maximum instead of settling exactly on it?
2. Part 2 shows one universal curve. Why does it not depend on $V_{th}$ or $R_{th}$?
3. Why is the solar cell's maximum-power point so much closer to its open-circuit voltage than the TEG's?
4. Coax for high-power transmitters is often 50 Ω, while cable-TV distribution is 75 Ω. Use Part 4 to explain the choice.

<details><summary>Answers to the discussion questions</summary>

1. It must keep moving to detect which direction increases power; once at the top, every step goes down, so it reverses each time and dithers by about one step around the maximum. Smaller steps reduce the dither but slow the response to changing conditions: a classic tracking tradeoff.
2. For a voltage behind a physical series resistance, both $p/p_{max}$ and $\eta$ depend only on the ratio $R_L/R_{th}$; eliminating that ratio leaves a relation between them alone, so scaling the source's voltage or resistance moves a point along the curve, never off it. The curve does not apply to a general network, whose Thévenin model says nothing about its internal loss (chapter §3.2).
3. A linear source's current falls in proportion to its voltage, so power peaks halfway. An illuminated diode supplies nearly its full photocurrent until its voltage approaches the junction's turn-on, then the current collapses within a few $nV_T$; the product peaks just before the collapse, at a large fraction of $V_{oc}$.
4. For a transmitter, peak power capacity and ruggedness matter, and 50 Ω keeps 86% of the air line's maximum power capacity (more than 75 Ω's 56%). For cable TV, signals are weak and runs are long, so loss matters most: 75 Ω is within 0.03% of the air line's minimum loss, and with the foam dielectrics such cables use it is still closer to the loss optimum than 50 Ω (1.5% against 3.9% extra loss at ε_r = 1.4). With solid polyethylene the advantage reverses.

</details>

## Optional hardware version

Measure the maximum-power point of a small solar cell (or a garden-light panel) in steady light: connect a 1 kΩ potentiometer as the load, record voltage and current at about 15 settings from short circuit to open circuit, and plot power against voltage. Compare the maximum-power voltage with half the open-circuit voltage. Then repeat in dimmer light and note how the maximum-power voltage moves (much less than the current).
