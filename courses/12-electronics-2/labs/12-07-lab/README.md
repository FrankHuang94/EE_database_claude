# Lab 12-07 · Output Stages and Power Amplifiers

Chapter: [12-07 Output Stages and Power Amplifiers](../../chapters/12-07-output-stages.md)

## Objective

Compare the efficiency and dissipation of class A, class B and class D stages across output level; measure crossover distortion with and without feedback and with class AB bias; plot class AB currents; watch a transistor run away thermally and an emitter resistor prevent it. Simulate a real class B stage in ngspice.

## Background

Class A (§3.1), class B and crossover (§3.2), class AB and the $V_{BE}$ multiplier (§3.3), thermal design (§3.4) and class D (§3.5).

## Files

- [12-07-output-stages.ipynb](12-07-output-stages.ipynb): the notebook (Parts 1–4).
- [class_b.cir](class_b.cir): ngspice transient simulation of a ±15 V class B stage with bipolar transistor models driving 8 Ω, measuring load power, supply power and efficiency. Run with `ngspice -b class_b.cir`, or `python tools/run_spice.py 12-07` from the repository root.

## Procedure

1. **Efficiency (Part 1).** Plot efficiency and dissipation against amplitude for the three classes and locate the class B dissipation peak.
2. **Crossover (Part 2).** Tabulate THD at 0.1, 1 and 10 V for the open dead band, the dead band inside a loop of gain 10⁴, and a class AB stage idling at 20 mA.
3. **Class AB currents (Part 3).** Plot both device currents against load current.
4. **Thermal runaway (Part 4).** Start a transistor 1 °C above its equilibrium and step its temperature with and without a 0.47 Ω emitter resistor.
5. **ngspice (the chapter's guided exercise).** *Predict first:* will the real class B stage beat or miss the ideal 6.25 W and 52.36%? Then run `class_b.cir`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Class B dissipation peak | 5.699 W at 9.55 V, as in Example 12-07.2 |
| 2 | THD | The open dead band passes nothing at 0.1 V; the loop and class AB bias both bring THD below 1% |
| 3 | Currents | Neither device cuts off; their product stays at $I_Q^2$ |
| 4 | Temperature | Runs away within a minute without $R_E$; settles with it |
| ngspice | Class B stage | Less power and efficiency than ideal |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 12-07.a | simulated load power | 5.098 | W |
| Lab 12-07.b | simulated supply power | 10.44 | W |
| Lab 12-07.c | simulated efficiency | 48.82 | % |

*These are recomputed by [verify_12_07.py](../../verify/verify_12_07.py) with its own Ebers–Moll solution of the same stage (ngspice's default temperature of 27 °C, $I_S$ = 10⁻¹³ A, $\beta_F$ = 100), sample by sample over a cycle.*

## Discussion questions

1. In Part 2, why does class AB distortion at 1 V exceed that at 10 V, even though there is no dead band?
2. In Part 4, why does the runaway accelerate near the end?
3. Why does the ngspice stage lose more efficiency than its lost swing alone would suggest?

### Answers

1. The stage's incremental output resistance changes with current (from $V_T/(2I_Q)$ at idle to $V_T/i$ for one device at high current), so its gain into 8 Ω varies over the cycle; at small amplitude that variation is a larger share of the signal.
2. The current depends exponentially on temperature with fixed base voltage, so each degree raises the current, and with it the dissipation, more than the last.
3. Efficiency is load power over supply power: the $V_{BE}$ drop removes load power while the supplies still deliver the full current through the transistors, whose $V_{CE}$ includes the lost swing. The dead band also removes output near zero.

## Optional hardware extension

Build a class B stage from a complementary pair (for example 2N3904/2N3906 for a small-signal version) driving 100 Ω from ±5 V, view the output on an oscilloscope with a 1 kHz sine input, and observe the crossover notch. Add two diodes between the bases (biased by resistors from the rails) to convert it to class AB and watch the notch disappear.
