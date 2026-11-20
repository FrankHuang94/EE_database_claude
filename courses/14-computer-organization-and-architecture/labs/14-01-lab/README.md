# Lab 14-01 · Performance, Power and the Iron Law

Chapter: [14-01 Performance, Power and the Iron Law](../../chapters/14-01-performance-power-iron-law.md)

## Objective

Use the iron law to see where a program's time goes, compare Amdahl's and Gustafson's views of parallel speedup and see how overheads cap it, find the energy-optimal clock of a leaky core, and watch the arithmetic mean of benchmark ratios contradict itself. Then measure in ngspice the energy cost of switching a capacitor.

## Background

The iron law and CPI (§3.2), Amdahl's and Gustafson's laws (§3.3), means (§3.4), dynamic and static power (§3.5) and energy and DVFS (§3.6).

## Files

- [14-01-performance-power.ipynb](14-01-performance-power.ipynb): the notebook (Parts 1–4).
- [switched_cap.cir](switched_cap.cir): a 1 pF capacitor charged and discharged from a 0-to-1 V, 100 MHz square wave through 100 Ω and then 300 Ω. Run with `ngspice -b switched_cap.cir`, or `python tools/run_spice.py 14-01` from the repository root.

## Procedure

1. **Iron law (Part 1).** Compute CPI, time and each class's share of time for Example 14-01.2's mix; then improve the loads. *Predict first:* what share of the time do the loads take?
2. **Parallel speedup (Part 2).** Plot Amdahl's curves for $p$ = 0.5, 0.9, 0.95 and 0.99, Gustafson's line, and a model with an overhead of $10^{-4}N$ added to the run time.
3. **DVFS (Part 3).** Plot the energy of a 10⁹-cycle task against frequency for the core of Problem 14-01.11. *Predict first:* is the lowest frequency the most efficient?
4. **Means (Part 4).** For two machines and five benchmarks, compare the total-time ratio with the arithmetic and geometric means of speed ratios against two different reference machines.
5. **ngspice (the chapter's guided exercise).** Predict the supply power and the energy lost in the resistor per charge, then run `switched_cap.cir`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Time shares | Loads 25% of instructions, 40.7% of time; a 1.172× speedup from the better cache |
| 2 | Speedup | Amdahl curves flatten at $1/(1 - p)$; with overhead the speedup peaks near 100 processors and then falls |
| 3 | Energy | A minimum near 0.89 GHz; energy rises at lower frequencies because of leakage |
| 4 | Means | The arithmetic mean flips which machine looks faster when the reference changes; the geometric mean does not |
| ngspice | Switching energy | 100 µW and 0.5 pJ per charge for both resistor values |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 14-01.a | peak speedup, p = 0.99 with overhead 10⁻⁴N | 33.44 | — |
| Lab 14-01.b | total-time ratio A/B, five benchmarks | 6.011 | — |
| Lab 14-01.c | arithmetic-mean ratio B/A, reference R1 | 1.388 | — |
| Lab 14-01.d | arithmetic-mean ratio B/A, reference R2 | 0.3493 | — |
| Lab 14-01.e | geometric-mean ratio B/A, either reference | 1.046 | — |

*These are recomputed by [verify_14_01.py](../../verify/verify_14_01.py) by evaluating the overhead model at every processor count and by computing the means directly from the data.*

## Discussion questions

1. Why does the overhead model's speedup peak instead of levelling off?
2. Why is there an energy-optimal frequency, and what would move it lower?
3. Why must the square wave's edges be much faster than the RC time constant for the netlist to show exactly $CV^2$ per cycle?

### Answers

1. The overhead term $10^{-4}N$ grows with the number of processors while the parallel term $0.99/N$ shrinks; their sum is smallest where they are equal, at $N = \sqrt{0.99/10^{-4}}$ ≈ 99.5, and beyond that each added processor costs more in overhead than it saves in parallel time.
2. Dynamic energy falls as the voltage (and so the frequency) falls, but leakage energy is leakage power times run time, and the run time grows as $1/f$. The sum has a minimum where the two rates of change balance. Less leakage (a better process, a higher threshold voltage, or power gating of unused parts) moves the optimum to lower frequencies; more leakage moves it up, toward racing to idle.
3. If the source voltage rises slowly compared with RC, the capacitor follows it and the current flows at a small voltage difference, so less energy is lost in the resistor and the source delivers less than $CV^2$. This is adiabatic charging: in the limit of an infinitely slow ramp almost no energy is lost. Real CMOS drivers switch fast compared with their RC, so $CV^2$ per cycle is the right model, which is why the netlist uses a 0.1 ps edge against time constants of 100 and 300 ps.

## Optional hardware extension

On a laptop, run a CPU-bound benchmark (for example a compression of a large file) with the operating system's power plan set to maximum performance and then to battery saver, and measure the run time and the battery drain (or the wall-plug energy with a plug-in power meter). Compute the energy per run in each mode and compare with the chapter's DVFS and race-to-idle discussion.
