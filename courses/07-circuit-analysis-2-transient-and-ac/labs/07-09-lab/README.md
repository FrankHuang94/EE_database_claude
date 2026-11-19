# Lab 07-09 · Mutual Inductance and Transformers

**Chapter:** [07-09](../../chapters/07-09-mutual-inductance-and-transformers.md) · **Notebook:** [07-09-transformers.ipynb](07-09-transformers.ipynb) · **Time:** about 2 hours

## Objective

1. Solve coupled-coil circuits for any coupling coefficient and see the reflected impedance.
2. Watch a pair of coupled coils approach an ideal transformer as $k \to 1$.
3. Sweep a transformer's efficiency against load and find its maximum.
4. Explore a loosely coupled wireless-power link, with and without resonant tuning.

## Background

Chapter sections 3.1 to 3.9 and Examples 07-09.1 to 07-09.6. You need Python with NumPy, SciPy and Matplotlib, and ngspice for the simulator checks (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [07-09-transformers.ipynb](07-09-transformers.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [ex2_coupled.cir](ex2_coupled.cir) | Example 07-09.2 with ngspice's coupled-inductor element `K`, and the guided exercise at $k$ = 0.99 | Chapter answer key and this handout |
| [ex3_matching.cir](ex3_matching.cir) | Example 07-09.3: an ideal transformer built from two controlled sources | Chapter answer key |
| [p12_wireless.cir](p12_wireless.cir) | Problem 07-09.12: a resonant wireless link at three coupling coefficients, and untuned | Solutions answer key |

Run the netlists from the repository root:

```bash
python tools/run_spice.py 07-09
```

## Procedure

1. **Coupled coils (Part 1).** *Predict first:* in Example 07-09.2, does the load power rise or fall as $k$ goes from 0.5 to 0.99? (The chapter's guided exercise.)
2. **Toward the ideal transformer (Part 2).** *Predict first:* with $k$ = 0.9999 and both inductances multiplied by 10, how close are the voltage ratio $V_2/V_1$ and the current ratio $I_1/I_2$ to $\sqrt{L_2/L_1}$ = 2?
3. **Efficiency curve (Part 3).** *Predict first:* for Example 07-09.4's transformer, at what load is the efficiency highest? Then overlay the amorphous design of Example 07-09.5.
4. **Wireless link (Part 4).** *Predict first:* how does the link efficiency fall as the coils separate (as $k$ falls from 0.3 to 0.01), and what does removing the tuning capacitor do?

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | $k$ = 0.99 | see the key: the load power rises almost tenfold |
| 2 | ratios | both within about 0.1% of 2; with only $k$ = 0.99 and inductances 100 times larger, leakage collapses the voltage ratio |
| 3 | maximum efficiency | at 42.6% load (Example 07-09.4) |
| 4 | link efficiency | falls slowly at first, then steeply once the reflected resistance nears the primary coil's own |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 07-09.a | load power at k = 0.99 | 0.9941 | W |
| Lab 07-09.b | input resistance past $R_1$ at k = 0.99 | 21.15 | Ω |

## Discussion questions

1. Why does the load power in Part 1 rise so much with tighter coupling?
2. In Part 2, why do the inductances need to grow as well as $k$ for the coils to behave like an ideal transformer?
3. Why do utilities care more about core loss than about full-load efficiency?
4. Why must a wireless charger's secondary be tuned to resonance?

<details><summary>Answers to the discussion questions</summary>

1. With $k$ = 0.5 most of the primary's flux misses the secondary, so the reflected resistance is small (5.4 Ω) and most of the source's power goes into $R_1$. At $k$ = 0.99 the load reflects as about 21 Ω, comparable to $R_1$, so far more power crosses to the load.
2. Two things must vanish: leakage, whose reactance $(1 - k^2)\omega L_2$ grows with the inductances unless $k$ approaches 1 faster, and magnetizing current, $V_1/(\omega L_1)$, which shrinks only as the inductances grow. The ideal transformer is the limit in which both happen.
3. A distribution transformer is energized all year but lightly loaded most of the time, so its constant core loss dominates the energy it wastes (Example 07-09.5).
4. Untuned, the secondary's own reactance limits the induced current, so little resistance is reflected; at resonance the secondary loop is purely resistive and reflects a large resistance, so most of the primary's power reaches the load (Problem 07-09.12).

</details>

## Optional hardware

Wind two coils of 20 turns each on a toilet-paper tube, a few centimeters apart. Drive one from a function generator through a 100 Ω resistor at 100 kHz to 1 MHz and watch the other on an oscilloscope. Slide the coils together and apart and record the secondary voltage; then add a capacitor across the secondary to tune it to the drive frequency and repeat. The tuned secondary's voltage rises sharply at resonance, a small-scale version of wireless charging. Keep voltages low; nothing here needs more than a few volts.
