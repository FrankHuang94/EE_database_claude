# Lab 20-12 · Why Analog Does Not Scale Like Digital

Chapter: [20-12 · Why Analog Does Not Scale Like Digital](../../chapters/20-12-why-analog-does-not-scale.md)

## Objective

- Tabulate what constant-field scaling does for a logic gate and for a noise-limited analog stage.
- Plot the power of a kT/C-limited buffer against supply voltage, with and without a swing that loses fixed headroom.
- Measure in ngspice what a cascode gains in output resistance and what it costs in headroom.
- Compare mismatch-limited and noise-limited capacitance across processes.
- Watch digital calibration repair a converter whose residue amplifier has too little gain.

## Background

`scaling.py` contains `constant_field`, `ktc_capacitance` and `thermal_power` (§3.1–3.2), `intrinsic_gain` and `stack_swing` (§3.3), `level1_id` and `cascode_current` (a square-law model of `stack.cir`), and `two_step_adc` with `sndr` (§3.6). `stack.cir` sweeps a single short-channel NMOS current sink and a cascoded one from 0.1 V to 0.8 V of output voltage (level-1 model, $V_{TO}$ = 0.4 V, $K_P$ = 300 µA/V², W/L = 10/0.5, λ = 0.2 V⁻¹; bottom gates at 0.55 V, cascode gate at 0.75 V) and reports the small-signal output resistance $1/(dI/dV)$.

## Procedure

1. **Scaling factors.** Tabulate delay, energy and area of a gate, and capacitance and power of a noise-limited stage, for one, two and three nodes of $S$ = 1.4 (Part 1).
2. **Power against supply.** For the buffer of Example 20-12.2, plot power from 3.3 V down to 0.6 V with the swing fixed at 80% of the supply, then with a swing of $V_{DD}$ − 0.3 V (Part 2).
3. **The cascode in ngspice.** *Predict* the output resistance of each sink at 0.6 V and of the cascode at 0.3 V, then run `ngspice -b stack.cir` and compare with `cascode_current` (Part 3).
4. **Mismatch or noise.** Compute the capacitance ratio $C_{ox}A_{VT}^2/kT$ for the processes of Example 20-12.4 and Problem 20-12.8 (Part 4).
5. **Calibration.** Run a coherent sine (1021 cycles in 8192 samples, amplitude 0.49 around 0.5) through `two_step_adc` with no gain error, with a 6.25% error uncorrected, corrected exactly, and corrected with estimates 0.39% and 2% off (Part 5).

## Expected results

- **Part 1.** Each node multiplies the gate's energy by 0.364 and the analog stage's power by 1.4; after three nodes the gate's energy is about 5% of the original and the analog stage's power 2.7 times it.
- **Part 2.** With a proportional swing, power rises as $1/V_{DD}$; with a fixed 0.3 V of headroom it rises much faster and diverges as the supply approaches 0.3 V.
- **Part 3.** The single device shows **74.1** kΩ at every output voltage in saturation. The cascode shows **5.58** MΩ at 0.6 V, about 75 times more, but only **232** kΩ at 0.3 V, where its upper transistor has left saturation. The cascode needs about 0.35 V of the 0.8 V supply before it delivers its gain.
- **Part 4.** About 30 for Example 20-12.4's process and 13.6 for Problem 20-12.8's: mismatch dominates in both unless it is calibrated away.
- **Part 5.** About 73.9 dB with no error; 50.1 dB uncorrected; 73.4 dB with exact correction (0.5 dB below ideal because the fine quantizer's top codes go unused); 73.3 dB with a 0.39% estimate error and 73.0 dB with 2%.

## Discussion

1. **Why does the corrected converter not reach the ideal SNDR?** The residue only spans 93.75% of the fine quantizer's range, so after correction the fine step is 1/0.9375 times larger. Real designs add redundancy so that the fine stage's range covers the residue with margin.
2. **Why is the cascode's output resistance about 75 times the single device's, not exactly $g_mr_o$?** The cascode multiplies by $1 + (g_m + g_{mb})r_o$ of the upper device at its own operating point, and the square-law model's $r_o$ depends on the drain voltage.
3. **Why does Part 2's curve diverge?** As the supply approaches the fixed headroom, the swing goes to zero and the capacitance needed for a fixed SNR goes to infinity.

## Optional hardware

On a breadboard, compare a 2N7000 current sink with and without a cascode device (a second 2N7000 with its gate on a divider) from a 3.3 V supply and a 1.5 V supply: measure output current against output voltage with a potentiometer and a multimeter, and note where the cascode's current flattens.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 20-12.a | single-device output resistance | 74.1 | kΩ |
| Lab 20-12.b | cascode output resistance at 0.6 V | 5.58 | MΩ |
| Lab 20-12.c | cascode output resistance at 0.3 V | 232 | kΩ |
| Lab 20-12.d | SNDR, no gain error | 73.9 | dB |
| Lab 20-12.e | SNDR, estimate 0.39% off | 73.3 | dB |
| Lab 20-12.f | gate energy after three nodes | 5 | % |
| Lab 20-12.g | analog power after three nodes | 2.7 | — |
