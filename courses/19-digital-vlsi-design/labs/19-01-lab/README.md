# Lab 19-01 · The Inverter's Transfer Curve

Chapter: [19-01 · The CMOS Inverter: Static Characteristics](../../chapters/19-01-cmos-inverter-static.md)

## Objective

- Measure an inverter's switching threshold and gain in ngspice, and match them to the closed forms.
- Compute the transfer curve, unity-gain points and noise margins numerically, and see how they move with sizing.
- Watch a chain of inverters regenerate a degraded level.
- Estimate the spread of the switching threshold from threshold variation, and explore the subthreshold inverter near its minimum supply.

## Background

The static output is the voltage at which the PMOS sources what the NMOS sinks (§3.1). The switching threshold is $V_M = (V_{TN}\sqrt r + V_{DD} - \lvert V_{TP}\rvert)/(1 + \sqrt r)$ with $r = k_n/k_p$ (§3.2); the unity-gain points bound the inputs read reliably, and the noise margins are $NM_L = V_{IL}$ and $NM_H = V_{DD} - V_{IH}$ (§3.3). The gain at $V_M$ is $-(g_{mn} + g_{mp})/(g_{dsn} + g_{dsp})$ (§3.4), and in subthreshold it is $(e^{V_{DD}/2V_T} - 1)/n$ (§3.5).

Files:

- `vtc.cir`: three inverters with SPICE's level-1 (square-law) model, swept from 0 to 1.2 V; it measures $V_M$ for each and the gain of the third by a central difference.
- `inverter.py`: the `Inverter` class (square-law and alpha-power transistors with channel-length modulation; `vout`, `vtc`, `vm`, `gain`, `unity_gain_points`, `noise_margins`), the closed forms (`vm_closed_form`, `ratio_for_vm`, `vil_closed_form`, `vih_closed_form`, `gain_at_vm`), the subthreshold inverter (`subthreshold_vtc`, `subthreshold_gain`, `subthreshold_vdd_min`) and `chain`.
- `19-01-inverter-lab.ipynb`: the procedure below.

## Procedure

1. **Switching threshold.** Predict $V_M$ for Examples 19-01.1 and 19-01.2. Run `ngspice -b vtc.cir` and the notebook's Part 1.
2. **Gain.** Predict the gain at $V_M$ for λ = 0.05, 0.1 and 0.2 V⁻¹; run Part 2. In `vtc.cir`, change the third inverter's `LAMBDA` and compare.
3. **Noise margins against sizing.** Predict which margin shrinks as $r$ grows; plot both for $r$ from 0.25 to 4 (Part 3).
4. **Regeneration.** Predict how many stages bring 0.55 V to a rail; run Part 4.
5. **Variation.** Predict $\sigma_{V_M}$ for 25 mV of threshold sigma; run the Monte Carlo (Part 5).
6. **Subthreshold.** Predict the midpoint slope at 45, 100 and 200 mV with $n$ = 1.4; run Part 6.

## Expected results

- Part 1: $V_M$ = 0.6000 V (symmetric) and 0.5243 V (equal widths) in Python; ngspice's swept curve gives 0.5244 V.
- Part 2: gains of **164.8**, 84.8 and **44.8**, each equal to $2(1 + \lambda V_{DS})/(\lambda V_{ov})$: halving λ roughly doubles the gain. ngspice measures 84.80 for λ = 0.1 V⁻¹.
- Part 3: at $r$ = 1 both margins are 0.5375 V; as $r$ grows $NM_L$ falls and $NM_H$ rises, and the smaller of the two is largest at $r$ = 1.
- Part 4: the levels are 0.55, 1.119, then exactly 0 and 1.2 V: the second stage already sits on a rail, because 1.119 V turns its PMOS off.
- Part 5: about 17.7 mV, matching $\sigma_{VT}/\sqrt2$.
- Part 6: gains of 1.00, 4.23 and 33.5; the curve at 45 mV is barely an inverter, and at 200 mV it is a good one.

## Discussion

1. Why does $V_M$ change so little when $W_p$ doubles?
2. Why does the ngspice gain differ from $2/(\lambda V_{ov})$?
3. In Part 4, why is the second stage's output exactly 0 V rather than merely close to it?
4. Why do practical subthreshold circuits run at a few hundred millivolts, when Part 6 shows gain at 45 mV?

**Answers.**

1. $V_M$ depends on $\sqrt r$ through a weighted average of $V_{TN}$ and $V_{DD} - \lvert V_{TP}\rvert$; doubling $W_p$ changes $\sqrt r$ by a factor of 0.707 and moves $V_M$ by 43 mV (§3.2).
2. SPICE's level-1 model multiplies the saturation current by $(1 + \lambda V_{DS})$, so $g_m = 2I_D/V_{ov}$ while $g_{ds} = \lambda I_D/(1 + \lambda V_{DS})$; the approximation $g_{ds} \approx \lambda I_D$ drops that factor (§3.4).
3. The first output, 1.119 V, is above $V_{DD} - \lvert V_{TP}\rvert$ = 0.85 V, so the second stage's PMOS is off and its conducting NMOS carries no current: region E, an exact rail.
4. Gain above 1 is only the threshold of regeneration; circuits also need noise margins, speed (subthreshold currents are tiny) and robustness to variation, which acts exponentially in subthreshold (§3.5, Problem 19-01.12).

## Optional hardware

A CD4007 (a classic CMOS array with three complementary pairs) on a breadboard at 5 V, with a slow ramp or a potentiometer on the input and a multimeter or oscilloscope in X-Y mode, shows the transfer curve directly; compare its $V_M$ with the formula using thresholds measured on the same chip.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 19-01.a | first output of the chain from 0.55 V | 1.119 | V |
| Lab 19-01.b | gain at V_M, lambda = 0.05 per volt | 164.8 | — |
| Lab 19-01.c | gain at V_M, lambda = 0.2 per volt | 44.8 | — |
