# Lab 27-01 · Closing the Budgets

**Objective.** Use small models of a product's power tree, thermal path, memory roofline and power cap to find which budget binds, and to price one budget in the units of another.

**Chapter:** [27-01 · Method: Analyzing a System End to End](../../chapters/27-01-system-analysis-method.md)

## Background

§3.2 derived the battery-side power of a converter tree, $P_{batt} = \sum_k P_k/\eta_k$. §3.3 derived the sustained power $P_{sus} = (T_{max} - T_a)/\theta$ and the burst duration $t_b = \tau\ln[(T_\infty - T_0)/(T_\infty - T_{max})]$ from a first-order thermal RC model. §3.5 gave the roofline $\min(\Pi, I\beta)$, and §3.6 the shadow price of a watt under a cap, $1/(3P_{dyn})$.

## Files

- `sysbudget.py`: power tree and LDO efficiency, run time and duty-cycle averages, sustained power, the thermal RC response and burst duration, burst duty, roofline and ridge point, bandwidth-bound decode speed, pipeline throughput and Little's law, Amdahl's law, BOM roll-up, and performance under a power cap with its shadow price.
- `27-01-budget-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · A better boost converter** (notebook). *Predict* how many minutes Example 27-01.1's run time gains if the display's boost converter improves from 85% to 92%. Then compute it.

**Part 2 · Burst duration against power** (notebook). *Predict* how long a 12 W burst lasts from Example 27-01.2's 2 W steady state. Then plot the burst duration for bursts from 5 to 15 W.

**Part 3 · Batching to the ridge** (notebook). *Predict* the batch size at which Example 27-01.3's decode becomes compute bound. Then plot attainable rate against batch size.

**Part 4 · What a watt is worth** (notebook). *Predict* the exact and linear performance gains if power gating saves a full watt in Example 27-01.6. Then plot both against the watts saved, from 0 to 1.5 W.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 27-01.a | battery power with a 92% boost | 4.87 | W |
| Lab 27-01.a1 | run time | 3.56 | h |
| Lab 27-01.a2 | minutes gained | 4.6 | min |
| Lab 27-01.a3 | battery power saved | 0.11 | W |
| Lab 27-01.b | 12 W burst duration | 69.0 | s |
| Lab 27-01.b1 | hottest sustainable power | 4.5 | W |
| Lab 27-01.c | batch at the ridge | 125 | |
| Lab 27-01.d | exact gain for 1 W | 10.06 | % |
| Lab 27-01.d1 | linear estimate for 1 W | 11.1 | % |

## Discussion

1. A 7-point better boost converter saves about 0.11 W of battery power and **4.6** minutes of run time, about half of what replacing the sensors' LDO saved (Example 27-01.1(d)). Fix the worst converter first, not the largest load.
2. The burst duration falls steeply with burst power: a 12 W burst lasts **69.0** s, against 106 s at 9 W, and any power at or below **4.5** W lasts indefinitely. Short benchmarks measure the burst; long workloads measure the sustained limit.
3. Decode stays bandwidth bound until a batch of **125**; beyond it, extra users cost compute but no extra memory traffic, which is why serving many users at once is so much cheaper per token.
4. The linear shadow price (11.1% per watt) slightly overstates the gain from large savings (**10.06**% exact for 1 W), because performance rises only as the cube root of dynamic power. For savings of a few tenths of a watt the linear estimate is within a few percent of the exact one.

## Optional hardware

None needed. If you have a laptop or phone with a power or thermal monitor, run a heavy benchmark for ten minutes and watch the clock frequency fall from its burst value to its sustained value.
