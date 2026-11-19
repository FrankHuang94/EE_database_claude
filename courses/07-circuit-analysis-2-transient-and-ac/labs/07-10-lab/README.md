# Lab 07-10 · Two-Port Networks

**Chapter:** [07-10](../../chapters/07-10-two-port-networks.md) · **Notebook:** [07-10-two-ports.ipynb](07-10-two-ports.ipynb) · **Time:** about 2 hours

## Objective

1. Measure z-, y- and h-parameters by applying open- and short-circuit tests, numerically and in ngspice.
2. Convert between parameter sets and check the conversions against measurements.
3. Build filters and matching networks by multiplying ABCD matrices, and see what loading costs.
4. Compute S-parameters, and check reciprocity and losslessness.

## Background

Chapter sections 3.1 to 3.9 and Examples 07-10.1 to 07-10.6. You need Python with NumPy and Matplotlib, and ngspice for the simulator checks (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [07-10-two-ports.ipynb](07-10-two-ports.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [ex1_params.cir](ex1_params.cir) | Example 07-10.1's y-parameters with shorted ports; Example 07-10.4's input impedance, gain and output impedance | Chapter answer key |
| [ex3_loading.cir](ex3_loading.cir) | Unbuffered RC cascades of two and three sections (Example 07-10.3, Problem 07-10.6) | Chapter and solutions answer keys |
| [ex6_sparams.cir](ex6_sparams.cir) | S-parameters in 50 Ω (Example 07-10.6, Problem 07-10.11) and the guided exercise | Answer keys and this handout |

Run the netlists from the repository root:

```bash
python tools/run_spice.py 07-10
```

## Procedure

1. **Measure, don't assume (Part 1).** *Predict first:* the T network's $z_{12}$ and $y_{12}$. Then apply the tests numerically and check $\mathbf{y} = \mathbf{z}^{-1}$.
2. **Conversions (Part 2).** *Predict first:* which parameter sets exist for a series inductor, a shunt capacitor and an ideal transformer.
3. **Chains (Part 3).** *Predict first:* the open-circuit gain of five unbuffered RC sections at $\omega RC = 1$. Then build Problem 07-10.7's L-match and sweep its return loss from 50 to 200 MHz.
4. **S-parameters (Part 4).** *Predict first* (the chapter's guided exercise): $\lvert S_{21}\rvert$ and $\lvert S_{11}\rvert$ of a 1 pF shunt capacitor at 10 GHz.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | $z_{12}$, $y_{12}$ | 30 Ω and −0.02727 S; $\mathbf{y}\mathbf{z} = \mathbf{I}$ |
| 2 | existence | series L: y and ABCD only (no z); shunt C: z and ABCD only (no y); ideal transformer: h and ABCD only |
| 3 | five sections | the gain keeps falling much faster than the buffered $0.7071^5$; the L-match's return loss peaks at 100 MHz |
| 4 | 1 pF at 10 GHz | see the key; the capacitor now reflects most of the power |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 07-10.a | $\lvert S_{21}\rvert$, 1 pF shunt at 10 GHz | 0.5370 | — |
| Lab 07-10.b | $\lvert S_{11}\rvert$, 1 pF shunt at 10 GHz | 0.8436 | — |

## Discussion questions

1. Why do the y-parameters you measured in Part 1 equal the inverse of the z-parameters?
2. Why does an ideal transformer have ABCD parameters but no z- or y-parameters?
3. In Part 3, why does each added unbuffered section cost more than the buffered 3 dB?
4. In Part 4, the capacitor's $\lvert S_{11}\rvert^2 + \lvert S_{21}\rvert^2$ stays exactly 1 at every frequency. Why, and what would change it?

<details><summary>Answers to the discussion questions</summary>

1. Both describe the same linear relation between port voltages and currents, $\mathbf{V} = \mathbf{z}\mathbf{I}$ and $\mathbf{I} = \mathbf{y}\mathbf{V}$, so the matrices are inverses wherever both exist.
2. Its defining tests fail: with one port open no current flows in either winding, so the open-circuit voltages are not determined by the currents; with one port shorted the other is shorted too. Its ABCD relations, $\mathbf{V}_1 = n\mathbf{V}_2$ and $\mathbf{I}_1 = (1/n)(-\mathbf{I}_2)$, are perfectly well defined.
3. Each section draws current from the one before it through that section's resistor (the $BC$ terms of the product), so the earlier sections' outputs sag below their unloaded values.
4. A capacitor stores energy but dissipates none, so incident power is either transmitted or reflected. Any resistance in the network, such as the series resistor of Problem 07-10.11, makes the sum fall below 1.

</details>

## Optional hardware

If you have access to a vector network analyzer (many university labs and some makerspaces have low-cost ones covering up to a few gigahertz), measure $S_{11}$ and $S_{21}$ of a 50 Ω SMA through-adapter, a 6 dB attenuator and a small capacitor soldered across an SMA connector. Compare with Problems 07-10.9 and 07-10.11, and notice how much a millimeter of lead adds above 1 GHz. Calibrate the analyzer first; without calibration the cables' own S-parameters dominate.
