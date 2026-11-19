# Lab 06-01 · Signs, Power Balance, Energy Budgets and the Limits of Lumped Circuits

**Chapter:** [06-01](../../chapters/06-01-charge-current-voltage-power.md) · **Notebook:** [06-01-power.ipynb](06-01-power.ipynb) · **Time:** about 90 minutes (plus 45 minutes for the optional hardware part)

## Objective

1. Read a circuit simulator's currents and powers correctly, including the negative current of a source that delivers power.
2. Confirm Tellegen's theorem from the simulator's own numbers, and use it as a check.
3. Find, by sweeping a source, the point at which a battery stops absorbing power and starts delivering it.
4. Build an energy budget from a duty-cycled current profile and see which activity dominates battery life.
5. See with your own eyes when a wire stops being a node: simulate a transmission line with fast and slow edges, and reproduce the result with a bounce-diagram calculation.

## Background

Chapter sections 3.3 (lumped matter discipline and the $t_d < t_r/6$ rule), 3.4 (passive sign convention and SPICE's convention for sources), 3.5 (Tellegen's theorem) and 3.6 (energy and duty cycling); Examples 06-01.2 to 06-01.4. You need Python with NumPy and Matplotlib, and ngspice for Parts 1, 2 and 4 (see [SETUP.md](../../../../SETUP.md)); without ngspice the notebook skips those cells and still runs.

## Files

| File | What it does | Checks against |
|---|---|---|
| [06-01-power.ipynb](06-01-power.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [power_balance.cir](power_balance.cir) | Operating points of Example 06-01.2 and Problems 06-01.6 and 06-01.13, with source and resistor powers; a sweep of the battery voltage | Chapter and solution answer keys |
| [tline_edges.cir](tline_edges.cir) | A 1 ns transmission line driven through 10 Ω by edges of 0.1, 2, 6 and 20 ns | This handout's answer key |

Both netlists are run in CI by [`tools/run_spice.py`](../../../../tools/run_spice.py), which compares each `* EXPECT` measurement with the published value.

## Procedure

1. **Signs in SPICE (Part 1).** *Predict first:* in Example 06-01.2, what sign will ngspice give for `i(V1)` and for `@V1[p]`? For `@V2[p]`? Run `ngspice -b power_balance.cir` (or the notebook cell) and compare. Then add up the five powers.
2. **A battery that becomes a load (Part 2).** *Predict first:* in Example 06-01.2's circuit, for what value of $V_2$ does the battery carry no current? (Hint: with $i_2 = 0$, node A is a divider of $V_1$ across $R_1$ and $R_3$.) The netlist sweeps $V_2$ from 0 to 12 V and reports the crossing; the notebook plots the battery's absorbed power across the sweep.
3. **Energy budget (Part 3).** Rebuild Example 06-01.4's current profile at 1 ms resolution, integrate it numerically, and compare with the duty-cycle formula. *Predict first:* which shortens battery life more: doubling the sensing time to 40 ms, or transmitting every second instead of every 10 s? And how much does halving the sensing time to 10 ms gain?
4. **When Kirchhoff fails (Part 4).** *Predict first:* for which of the four edge rates (0.1, 2, 6 and 20 ns) does the far end overshoot the final 1 V by more than 10%? Run `tline_edges.cir`, then compare with the notebook's bounce-diagram calculation and plot.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Example 06-01.2 in ngspice | `v(a)` = 8 V; `i(V1)` = −2 A; `i(V2)` = +0.667 A; `@V1[p]` = −24 W; `@V2[p]` = +4 W; resistors 8, 1.333 and 10.667 W; total 0 |
| 2 | battery voltage at which it stops absorbing | 9 V: below it the battery is charged, above it the battery delivers power |
| 3 | battery life for (sensing time, radio interval) | (20 ms, 10 s): 330.1 days; (10 ms, 10 s): 571.6 days; (40 ms, 10 s): about 179 days; (20 ms, 1 s): 187.5 days. Doubling the sensing time costs slightly more than transmitting ten times as often |
| 4 | far-end peak voltage for edges of 0.1, 2, 6 and 20 ns | 1.667, 1.667, 1.173 and 1.039 V: 66.7%, 66.7%, 17.3% and 3.9% overshoot |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 06-01.a | battery voltage at which its current reverses | 9 | V |
| Lab 06-01.b | far-end peak, 0.1 ns edge | 1.667 | V |
| Lab 06-01.c | far-end peak, 2 ns edge | 1.667 | V |
| Lab 06-01.d | far-end peak, 6 ns edge | 1.173 | V |
| Lab 06-01.e | far-end peak, 20 ns edge | 1.039 | V |
| Lab 06-01.f | battery life with 10 ms sensing | 571.6 | days |
| Lab 06-01.g | battery life with a radio packet every second | 187.5 | days |

## Discussion questions

1. A colleague reads `i(V1) = -2` in a simulation and concludes the supply is "sinking current". What would you tell them?
2. Why did the battery stop absorbing power at exactly 9 V, and why does that value not depend on $R_2$?
3. In Part 3, the radio's current is 4000 times the sleep current, yet it is under a tenth of the budget. Under what change of usage would it dominate?
4. The 2 ns edge overshoots exactly as much as the 0.1 ns edge, although it is twenty times slower. Why? And why does the 6 ns edge, which meets the $t_r/6$ rule's boundary, still overshoot by 17%?

<details><summary>Answers to the discussion questions</summary>

1. SPICE reports a voltage source's current with the passive sign convention: positive *into* the + terminal. A supply that is delivering power to the circuit therefore shows a negative current; −2 A means 2 A flowing out of its + terminal, and `@V1[p]` = −24 W confirms it is delivering 24 W. A supply that truly sinks current would show a positive value.
2. The battery's current is zero when node A sits at exactly the battery's voltage, because then there is no voltage across $R_2$. With no current in $R_2$, node A is set by $V_1$, $R_1$ and $R_3$ alone, as a divider: $12\times6/(2 + 6) = 9$ V. Since $R_2$ carries no current at that point, its value cannot matter. Above 9 V the battery pushes current into node A and delivers power; below, the supply pushes current into the battery.
3. The radio's share is its current times its duty cycle: $8\ \text{mA}\times 3\ \text{ms}/10\ \text{s} = 2.4$ µA of average current, against 24 µA for sensing. Transmitting every second (Part 3's second variant) raises it to 24 µA, equal to sensing; streaming data (a radio on 10% of the time) would make it 800 µA and dominate everything. The budget depends on usage, which is why battery-life claims must state the usage profile.
4. The far end first sees the incident wave at $t_d$ = 1 ns and the first reflection from the source returns at $3t_d$ = 3 ns. A 2 ns edge has finished rising before that reflection arrives, so the first plateau reaches the full $1.667$ V, the same as for an instantaneous edge; only edges slower than the round trip ($2t_d$ = 2 ns) start to blend the reflections together. The $t_r/6$ rule describes when reflections start to blur into the edge, not when they vanish: with a badly matched 10 Ω driver (reflection coefficient −0.67) the residual ringing at the boundary is still 17%. A matched driver or a slower edge reduces it, which is why fast interfaces are terminated rather than merely kept short.

</details>

## Optional hardware version

With a bench supply, two resistors (for example 100 Ω and 220 Ω, 0.25 W) and a digital multimeter, build a series circuit and measure the voltage across each element and the current. Compute each element's power with the passive sign convention and check that the supply's (negative) power balances the resistors'. Then reverse the meter leads on one measurement and note how the sign of your bookkeeping must change with it. Keep every resistor's power below its rating: at 5 V, 320 Ω total draws 15.6 mA and the 220 Ω resistor dissipates 54 mW.
