# Lab 13-09 · The Smith Chart and Impedance Matching

Chapter: [13-09 The Smith Chart and Impedance Matching](../../chapters/13-09-smith-chart-and-matching.md)

## Objective

Build a Smith chart from its definition and use it to move along lines, design L-network and single-stub matches, and see how adding sections widens a match until it meets the Bode–Fano limit. Then confirm two matches in ngspice.

## Background

The chart's construction (§3.1), reading and moving (§3.2), L-networks (§3.3), stubs (§3.4), and bandwidth limits (§3.5).

## Files

- [13-09-smith-matching.ipynb](13-09-smith-matching.ipynb): the notebook (Parts 1–4).
- [match.cir](match.cir): Example 13-09.4's L-network at 2.4 GHz and Example 13-09.5's stub match at 1 GHz, each driven by 1 A AC. Run with `ngspice -b match.cir`, or `python tools/run_spice.py 13-09` from the repository root.

## Procedure

1. **Points and moves (Part 1).** Plot three loads and their λ/4 paths toward the generator. *Predict first:* where does each land?
2. **L-networks (Part 2).** Design both forms for 10 Ω at 2.4 GHz and plot |Γ| against frequency.
3. **Stubs (Part 3).** Find both shorted-stub solutions for 25 − j50 Ω and draw the paths.
4. **Sections and limits (Part 4).** Compare one, two and three L-sections; tabulate the Bode–Fano bound for 50 Ω ∥ 1 pF.
5. **ngspice (the chapter's guided exercise).** Predict both input impedances, then run `match.cir`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | λ/4 moves | Each load lands on $Z_0^2/Z_L$: 20 − j10, 20 + j40 and 200 Ω |
| 2 | L-networks | Q = 2 for both forms; about 11% bandwidth for |Γ| < 0.1 |
| 3 | Stubs | d = 0.06313λ with a 0.08975λ stub, or d = 0.2067λ with 0.4102λ |
| 4 | Sections | About 11%, 19% and 62% bandwidth for one, two and three sections; Bode–Fano bounds of 8.7, 5.8, 4.3 and 2.9 GHz at 10, 15, 20 and 30 dB |
| ngspice | Input impedances | 50 Ω for both |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 13-09.a | three-section L-match bandwidth, 10 to 50 Ω, Γ below 0.1 | 62.05 | % |
| Lab 13-09.b | Bode–Fano bound, 50 Ω ∥ 1 pF, 15 dB return loss | 5.791 | GHz |

*These are recomputed by [verify_13_09.py](../../verify/verify_13_09.py) by nodal analysis of the cascaded network and root finding on the Bode–Fano relation.*

## Discussion questions

1. Why do the λ/4 moves land exactly on $Z_0^2/Z_L$?
2. Why do more sections widen the match, and why can they not widen it without limit for a reactive load?
3. When would you choose the high-pass L-network over the low-pass one?

### Answers

1. A quarter wavelength rotates Γ by 180°, turning Γ into −Γ, and $Z_0(1 - \Gamma)/(1 + \Gamma)$ is $Z_0^2/Z_L$: the impedance-inverter property of 13-08 seen on the chart.
2. Each section steps the resistance by a smaller ratio, so its Q is lower and its reactances drift more slowly with frequency. For a purely resistive load the bandwidth can grow without bound as sections are added; with a fixed reactive part in the load, the Bode–Fano integral caps the total area under ln(1/|Γ|), so extra sections can only reshape the response toward the ideal rectangle, not exceed it.
3. When a DC path to ground is needed at the port (the shunt inductor provides it, for example to bias a transistor or bleed static charge) or a DC block in the signal path (the series capacitor), and when harmonic suppression is not the priority; the low-pass form filters harmonics and passes DC through the series inductor.

## Optional hardware extension

With a NanoVNA-class instrument, measure a 10 Ω resistor (or two 22 Ω in parallel) at a few hundred megahertz, design an L-network with standard surface-mount parts on the chart, build it on a small board, and measure the return loss across frequency. Compare the bandwidth with the notebook's prediction, and see how the parts' own parasitics shift the match.
