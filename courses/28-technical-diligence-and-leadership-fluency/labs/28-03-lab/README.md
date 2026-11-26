# Lab 28-03 · Maturity, Life Tests and Bug Curves

**Objective.** Use small models to see how a programme's value rises as it climbs the maturity scale, what a life test of a given size proves about failure rates, how a defect-discovery curve is fitted to a bug tracker's history, and how much a FIT claim depends on its assumed activation energy.

**Chapter:** [28-03 · Maturity Scales for Silicon](../../chapters/28-03-silicon-maturity-scales.md)

## Background

The lab uses the chapter's models with its assumed parameters:

- §3.2: the probability $\prod p_j$, time $\sum t_j$ and value multiplier $P_k/(1 + r)^{T_k/12}$ from a maturity level.
- §3.3: the Arrhenius acceleration factor and the bound $\chi^2_{C;\,2r+2}/(2nt\,\text{AF})$.
- §3.4: the Goel–Okumoto curve $m(t) = a(1 - e^{-bt})$.

## Files

- `matscale.py`: the models (stage chains, acceleration factors, failure-rate bounds and sample sizes, the Goel–Okumoto fit, rate and remaining defects).
- `28-03-maturity-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Value by level** (notebook). *Predict* the value multiplier at L3 for Example 28-03.2's chain. Then compute and plot the multiplier at L2, L3, L4 and L5.

**Part 2 · Bound against sample size** (notebook). *Predict* the 60% and 90% FIT bounds for 1,000 devices on a zero-failure 1000-hour test at 125 °C, for a 55 °C use junction and 0.7 eV. Then plot the bounds against device count from 77 to 10,000.

**Part 3 · Fitting a bug curve** (notebook). Weekly cumulative counts for 20 weeks are generated from Example 28-03.4's model ($a$ = 500, $e^{-10b} = 0.4$) and rounded to whole defects. *Predict* what a least-squares fit recovers. Then fit, plot the data and curve, and compute the defects remaining at week 20.

**Part 4 · The activation energy behind a FIT claim** (notebook). *Predict* Example 28-03.3's 60% bound if the activation energy is 0.5 eV, and if it is 1.0 eV. Then plot the bound against activation energy from 0.4 to 1.1 eV.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 28-03.a | multiplier at L2 | 0.501 | — |
| Lab 28-03.a1 | multiplier at L3 | 0.555 | — |
| Lab 28-03.a2 | multiplier at L4 | 0.744 | — |
| Lab 28-03.a3 | multiplier at L5 | 0.928 | — |
| Lab 28-03.b | bound for 1,000 devices, 60% | 11.8 | FIT |
| Lab 28-03.b1 | bound for 1,000 devices, 90% | 29.7 | FIT |
| Lab 28-03.c | fitted total defects | 500 | defects |
| Lab 28-03.c1 | fitted rate constant | 0.0916 | 1/week |
| Lab 28-03.c2 | fitted remaining at week 20 | 80.0 | defects |
| Lab 28-03.d | acceleration factor at 0.5 eV | 22.4 | — |
| Lab 28-03.d1 | bound at 0.5 eV | 177 | FIT |
| Lab 28-03.d2 | acceleration factor at 1.0 eV | 501 | — |
| Lab 28-03.d3 | bound at 1.0 eV | 7.91 | FIT |

## Discussion

1. The multiplier rises from **0.501** at tape-out to **0.555** at first silicon, **0.744** with engineering samples and **0.928** after qualification. The biggest step is from L3 to L4, where respins are resolved, which is where milestone payments do the most work.
2. A thousand devices bound the rate at **11.8** FIT (60%) and **29.7** FIT (90%). The bound falls only inversely with the sample, so each halving of the claim doubles the test.
3. The fit recovers about **500** defects and a rate constant of **0.0916** per week, and estimates **80.0** remaining at week 20, matching the two-point fit: rounding to whole defects barely disturbs it. On real trackers, changes in test effort bend the curve, which is why the fit should be redone as data arrive.
4. At 0.5 eV the acceleration factor is **22.4** and the bound **177** FIT; at 1.0 eV it is **501** and **7.91** FIT. A factor of more than twenty from one assumption is why a FIT claim without its activation energy is not a claim.

## Optional hardware

None. As an exercise, take a public reliability report from any semiconductor supplier and recompute its FIT figure from its stated devices, hours, failures, temperatures, activation energy and confidence.
