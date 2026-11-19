# Lab 07-08 · Filters and Resonance

**Chapter:** [07-08](../../chapters/07-08-filters-and-resonance.md) · **Notebook:** [07-08-filters.ipynb](07-08-filters.ipynb) · **Time:** about 2.5 hours

## Objective

1. Measure a resonator's $Q$ four ways (bandwidth, energy, ring-down, pole location) and see that they agree.
2. See how source and load resistances lower a tank's $Q$ and where the power goes.
3. Design Butterworth filters of any order and check the section $Q$ values.
4. Measure how component tolerances and the op-amp's gain–bandwidth product disturb a Sallen–Key section.
5. Connect resonator $Q$ to a filter's insertion loss.

## Background

Chapter sections 3.1 to 3.9 and Examples 07-08.1 to 07-08.6. You need Python with NumPy, SciPy and Matplotlib, and ngspice for the simulator checks (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [07-08-filters.ipynb](07-08-filters.ipynb) | The guided notebook (Parts 1 to 5) | Its own `assert`s |
| [ex1_series.cir](ex1_series.cir) | Example 07-08.1: resonance, half-power frequencies, current and capacitor voltage | Chapter answer key |
| [ex2_tank.cir](ex2_tank.cir) | Example 07-08.2: the loaded tank's impedance and bandwidth | Chapter answer key |
| [ex3_butter.cir](ex3_butter.cir) | Example 07-08.3: the 50 Ω Butterworth low-pass | Chapter answer key |
| [ex5_sallen_key.cir](ex5_sallen_key.cir) | Example 07-08.5 and the guided exercise: Sallen–Key sections with an ideal and a finite-GBW op-amp | Chapter answer key and this handout |
| [ex6_ex7.cir](ex6_ex7.cir) | Example 07-08.6 (a lossy four-resonator Butterworth band-pass ladder at 2 GHz) and Example 07-08.7 (the Sallen–Key high-pass and MFB low-pass voice-band cascade) | Chapter answer key |
| [p15_p17.cir](p15_p17.cir) | Problems 07-08.15 (loaded tank), 07-08.16 (MFB low-pass) and 07-08.17 (Sallen–Key high-pass) | Solution answer key |

Run the netlists from the repository root:

```bash
python tools/run_spice.py 07-08
```

## Procedure

1. **Four Q's (Part 1).** *Predict first:* for Example 07-08.1's circuit, how many cycles does the free oscillation take to decay by a factor $e$?
2. **Loading (Part 2).** *Predict first:* in Example 07-08.2, which resistor (source, load or the coil's own) takes the largest share of the power? Then raise the load to 100 kΩ and watch the bandwidth.
3. **Butterworth (Part 3).** *Predict first:* the $Q$ of the highest-$Q$ section of a sixth-order Butterworth filter. Then let the notebook compute every section for orders 1 to 8.
4. **Tolerances and GBW (Part 4).** Run [ex5_sallen_key.cir](ex5_sallen_key.cir). *Predict first* (the chapter's guided exercise): with an op-amp of GBW 100 kHz (100 times the cutoff), does the gain at 1 kHz move by more or less than 0.1 dB? With 10 kHz? Then run the notebook's Monte Carlo with 5% and 1% capacitors.
5. **Insertion loss (Part 5).** *Predict first:* the unloaded $Q$ needed for 0.5 dB of loss per resonator when $Q_L$ = 100.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | decay by $e$ | about $Q/\pi$ = 32 cycles |
| 2 | largest share | the coil (55%); the bandwidth narrows as the load rises |
| 3 | sixth order | highest $Q$ = 1.932 |
| 4 | finite GBW | see the key below |
| 5 | $Q_u$ for 0.5 dB | 1788 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 07-08.a | gain at 1 kHz with GBW 100 kHz | −3.048 | dB |
| Lab 07-08.b | gain at 1 kHz with GBW 10 kHz | −3.221 | dB |
| Lab 07-08.c | cycles to decay by e, Example 07-08.1 | 32 | — |
| Lab 07-08.d | highest section Q, sixth-order Butterworth | 1.932 | — |
| Lab 07-08.e | $Q_u$ for 0.5 dB at $Q_L$ = 100 | 1788 | — |

## Discussion questions

1. Why does a tank's bandwidth widen when the next stage loads it more heavily?
2. Why is the unity-gain Sallen–Key design preferred over the equal-component design for high-$Q$ sections?
3. In Part 4, why does a finite-GBW op-amp change the filter's response near its cutoff even though the op-amp is "only a follower"?
4. Why can't a filter at 2 GHz with a 1% bandwidth be built from on-chip inductors?

<details><summary>Answers to the discussion questions</summary>

1. The load appears in parallel with the tank's own loss resistance, lowering the total shunt resistance and so the loaded $Q$; the bandwidth $f_0/Q_L$ grows.
2. In the equal-component design $Q = 1/(3 - K)$, so near $K$ = 3 a small gain error causes a large $Q$ error (the sensitivity is $KQ$); the unity-gain design sets $Q$ by a capacitor ratio, which is stable, and has no gain resistors at all.
3. The follower's gain $A/(1 + A)$ falls below 1 and gains phase lag as frequency approaches GBW; that changes the feedback through $C_1$, which is what sets $Q$. With GBW only 10 times the cutoff the error is already visible.
4. A 1% bandwidth needs a loaded $Q$ of about 100, so the resonators need an unloaded $Q$ of several hundred or more for acceptable loss; on-chip inductors fall far short of that (§9).

</details>

## Optional hardware

Build Example 07-08.5's Sallen–Key section on a breadboard with any general-purpose op-amp, 11 kΩ resistors (or the nearest you have) and film or C0G capacitors of 20 nF and 10 nF (two 10 nF in parallel for 20 nF). Drive it with a function generator at about 1 V and sweep from 100 Hz to 10 kHz, recording the output amplitude; the −3 dB point should land within a few percent of 1 kHz. Then swap $C_1$ for a high-permittivity ceramic (X7R or Y5V) of the same nominal value and repeat with a DC offset on the input: the cutoff and peaking shift as the capacitor loses capacitance under bias (07-01).
