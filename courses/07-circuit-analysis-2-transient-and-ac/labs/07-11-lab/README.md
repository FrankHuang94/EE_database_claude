# Lab 07-11 · Three-Phase Circuits

**Chapter:** [07-11](../../chapters/07-11-three-phase-circuits.md) · **Notebook:** [07-11-three-phase.ipynb](07-11-three-phase.ipynb) · **Time:** about 1.5 hours

## Objective

1. Draw the phasor diagrams of Y and Δ systems and see the $\sqrt3\angle30°$ relations.
2. Watch three pulsating phase powers sum to a constant.
3. Compute neutral currents for unbalanced and harmonic loads, and see what an open neutral does.
4. Read three-phase power with two wattmeters.

## Background

Chapter sections 3.1 to 3.7 and Examples 07-11.1 to 07-11.6. You need Python with NumPy and Matplotlib, and ngspice for the simulator checks (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [07-11-three-phase.ipynb](07-11-three-phase.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [ac_three_phase.cir](ac_three_phase.cir) | AC analyses of a balanced Y load, an unbalanced four-wire load, the same load with the neutral open (the guided exercise), and the two wattmeter readings | Chapter answer key and this handout |
| [tran_power.cir](tran_power.cir) | A transient simulation showing the balanced load's instantaneous power is constant | Solutions answer key |
| [p13_p14.cir](p13_p14.cir) | Problems 07-11.13 (negative sequence, two wattmeters) and 07-11.14 (unbalanced Δ load from a Δ source) | Solution answer key |

Run the netlists from the repository root:

```bash
python tools/run_spice.py 07-11
```

## Procedure

1. **Phasors (Part 1).** *Predict first:* the angle between $\mathbf{V}_{an}$ and $\mathbf{V}_{ab}$, and between a Δ load's phase current and its line current.
2. **Constant power (Part 2).** *Predict first:* the minimum and maximum of a single-phase 12.8 kW load's instantaneous power at power factor 0.8, and of the three-phase total.
3. **Neutral (Part 3).** *Predict first* (the chapter's guided exercise): with Example 07-11.4's loads (10, 20 and 40 Ω on a 230/400 V supply) and the neutral wire broken, which phase's load voltage rises most? Then add third-harmonic currents and watch the neutral.
4. **Two wattmeters (Part 4).** *Predict first:* how the two readings change as the load's power factor falls from 1 to 0.3.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | angles | $\mathbf{V}_{ab}$ leads $\mathbf{V}_{an}$ by 30°; a Δ line current lags its phase current by 30° |
| 2 | power swing | single phase −3.2 to 28.8 kW; three phase constant at 12.8 kW |
| 3 | open neutral | the lightly loaded phases' voltages rise far above 230 V; see the key |
| 4 | wattmeters | equal at unity power factor; one reaches zero at 0.5 and goes negative below |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 07-11.a | phase a load voltage, neutral open | 150.6 | V |
| Lab 07-11.b | phase b load voltage, neutral open | 260.8 | V |
| Lab 07-11.c | phase c load voltage, neutral open | 301.1 | V |
| Lab 07-11.d | star-point displacement | 86.93 | V |

## Discussion questions

1. Why does a broken neutral damage equipment on the lightly loaded phases?
2. Why can a balanced three-wire load be analyzed one phase at a time even though it has no neutral wire?
3. Why do fifth-harmonic currents not appear in the neutral while third harmonics do?
4. Why is the two-wattmeter method valid for unbalanced three-wire loads but not for four-wire ones?

<details><summary>Answers to the discussion questions</summary>

1. Without the neutral the three loads are in a floating star whose center moves toward the heaviest load; the light loads then see a large share of the line voltage (here up to 301 V instead of 230 V), which overheats or destroys equipment rated for 230 V.
2. In a balanced load the star point sits at the source's neutral potential, because the three currents sum to zero; connecting the two points with a wire would carry no current, so each phase behaves as if it were connected (§3.2).
3. The fifth harmonics of the three phases are shifted by 5 × 120° = 600°, equivalent to 240°, so they still form a balanced set (in reverse sequence) and cancel; the third harmonics are shifted by 360°, so they are in phase and add.
4. The derivation uses $\mathbf{I}_b = -(\mathbf{I}_a + \mathbf{I}_c)$, which holds only when no current returns through a neutral; a four-wire system needs three wattmeters.

</details>

## Optional hardware

Three-phase mains is dangerous; do not experiment on it. A safe alternative is a three-channel function generator (or three phase-locked outputs of a USB audio interface) at a few volts and tens of hertz, driving three resistor–capacitor loads in Y. Measure each phase voltage and the star-point voltage with an oscilloscope, then disconnect the star point from the generator's common terminal and watch it move as you unbalance the resistors.
