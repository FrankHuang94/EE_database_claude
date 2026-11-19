# Lab 07-06 · AC Power and Power Factor

**Chapter:** [07-06](../../chapters/07-06-ac-power-and-power-factor.md) · **Notebook:** [07-06-power.ipynb](07-06-power.ipynb) · **Time:** about 2 hours

## Objective

1. See real and reactive power in waveforms: the average of $p(t)$ and the double-frequency swing around it.
2. Confirm that RMS values of harmonics add in quadrature.
3. Correct a power factor and check that complex power balances element by element.
4. Explore how a rectifier's current pulses set power factor and harmonic distortion.

## Background

Chapter sections 3.2 to 3.8 and Examples 07-06.1 to 07-06.6. You need Python with NumPy, SciPy and Matplotlib, and ngspice for the simulator check (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [07-06-power.ipynb](07-06-power.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [power.cir](power.cir) | Time-domain average power, RMS current and the effect of the correction capacitor for Examples 07-06.1 and 07-06.3 | Chapter answer key |

Run the netlist from the repository root:

```bash
python tools/run_spice.py 07-06
```

## Procedure

1. **Power in waveforms (Part 1).** *Predict first:* for a load at PF 0.5, what fraction of each cycle is the instantaneous power negative?
2. **RMS by quadrature (Part 2).** *Predict first:* the RMS of $10\cos\omega t + 3\cos3\omega t + 1\cos5\omega t$.
3. **Correction and balance (Part 3).** *Predict first:* how the source current of Example 07-06.3 changes as the capacitor grows from zero past the unity-PF value.
4. **Pulse width (Part 4).** *Predict first:* whether wider rectifier pulses raise or lower the power factor (the chapter's guided exercise).

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | negative power | grows as the power factor falls; zero for a resistor, half the cycle for a pure reactance |
| 2 | RMS | equals the square root of the sum of the squared component RMS values |
| 3 | source current | falls to a minimum at unity power factor (60.87 A), then rises again as the load turns leading |
| 4 | pulse width | wider pulses give a higher power factor (see the key) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 07-06.a | power factor with 5 ms pulses at 100 W | 0.9003 | — |

## Discussion questions

1. Why does a utility bill industrial customers for poor power factor but usually not households?
2. In Part 3, why does over-correcting make the current rise again?
3. In Part 4, why can't a capacitor improve the rectifier's power factor?
4. A "true RMS" meter and an "average-responding" meter disagree on a rectifier's input current. Which is right, and why?

<details><summary>Answers to the discussion questions</summary>

1. Industrial loads (motors, transformers) draw large reactive currents that load the utility's network, and industrial meters measure kVA or power factor; household meters typically record only energy (kWh), and household reactive loads are smaller relative to the network. Tariffs differ by utility (§9).
2. Past unity, the capacitor's leading current exceeds the load's lagging current, so the net reactive current grows again, now leading; the current is minimal only when the reactive currents cancel exactly.
3. The poor power factor comes from harmonics, not from a phase shift of the fundamental. A capacitor shifts the fundamental (adding a leading component) and can even make things worse; only reshaping the current toward a sinusoid (active PFC) removes the harmonic part.
4. The true-RMS meter, provided its bandwidth and crest-factor rating cover the waveform. An average-responding meter scales the rectified average by the sine's ratio (1.111), which is correct only for sinusoids; for peaky pulses it reads low.

</details>
