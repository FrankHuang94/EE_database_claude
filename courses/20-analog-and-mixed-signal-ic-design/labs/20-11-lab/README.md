# Lab 20-11 · Mismatch, Gradients and Statistical Design

Chapter: [20-11 · Layout, Matching and PVT Variation](../../chapters/20-11-layout-matching-pvt.md)

## Objective

- Watch Pelgrom's area law emerge from a Monte Carlo of independent fixed-size patches under the gate.
- Compare how current mirrors and differential pairs respond to $g_m/I_D$, and confirm the mirror's threshold sensitivity in ngspice.
- Compute the gradient residuals of common placement patterns and see which cancel linear and quadratic gradients.
- Turn σ into yield, and find out how much a Monte Carlo of 100 or 1000 runs really tells you.

## Background

`matching.py` contains `pelgrom_sigma`, `mirror_sigma` and `pair_offset_sigma` (the formulas of §3.1–3.2), `pattern_residuals` and `gradient_offset` (§3.4), `mc_pair` (a seeded Monte Carlo of unit-cell threshold errors), `zero_failure_runs` and `sigma_ci` (§3.7). `mirror.cir` holds three square-law current mirrors (W/L = 10/1, $K_P$ = 200 µA/V², $V_{TO}$ = 0.5 V) whose output transistor's threshold is 1 mV higher than the input's, at reference currents of 10, 100 and 400 µA. Those currents give overdrives of 0.1, 0.316 and 0.632 V, that is $g_m/I_D = 2/V_{ov}$ = 20, 6.32 and 3.16 V⁻¹.

## Procedure

1. **Area law.** Divide each gate into patches of a fixed 0.01 µm², each with an independent 24.75 mV threshold error, so a larger gate has more patches; simulate 4000 pairs at several gate areas and plot σ(ΔV_TH) against $1/\sqrt{WL}$ (Part 1). *Predict* the slope.
2. **Mirrors and pairs.** Plot the mirror's σ(ΔI/I) and the pair's σ(V_os) of Example 20-11.2 against $g_m/I_D$ from 3 to 25 V⁻¹. Then *predict* the current mismatch of each mirror in `mirror.cir` and run `ngspice -b mirror.cir` (Part 2).
3. **Gradients.** Compute the linear and quadratic residuals of AB, AABB, ABAB, ABBA and ABBABAAB, and the offset of each for the gradient of Example 20-11.4 (Part 3). *Predict* which patterns cancel each order.
4. **Yield.** Draw 10⁶ offsets with σ = 1.107 mV and count those outside ±3 mV; compare with Example 20-11.5 (Part 4).
5. **How many runs?** Repeat a 100-run Monte Carlo 2000 times and histogram the estimated σ; check how often the chi-square interval built from each run's estimate contains the true σ, and compare the estimate's own spread with its sampling interval. Then tabulate the failure-free runs needed for 3σ, 4σ and 4.5σ yield claims (Part 5).

## Expected results

- **Part 1.** σ(ΔV_TH) falls on a straight line through the origin against $1/\sqrt{WL}$ with a slope of about 3.5 mV·µm, equal to $\sigma_{patch}\sqrt{2a_{patch}}$ = 24.75 × √0.02: the area law comes out of averaging more patches, and $A_{VT}$ is an output, not an input.
- **Part 2.** The mirror's mismatch grows almost linearly with $g_m/I_D$ while the pair's offset falls toward σ(ΔV_TH). ngspice gives current mismatches of **1.99**%, **0.631**% and **0.316**% for the three mirrors; the linear formula $(g_m/I_D)\Delta V_{TH}$ gives **2.00**%, **0.632**% and **0.316**%. The small differences are the square law's second-order term, $(\Delta V_T/V_{ov})^2$.
- **Part 3.** AB and ABAB both leave one pitch of linear residual: however long an interdigitated row is, its two centroids stay one pitch apart (the one-pitch offset of §3.4), while AABB leaves two pitches, a gap that grows with the number of cells per device. ABBA cancels the linear term and leaves 2 pitch² of quadratic; ABBABAAB cancels both, reproducing Example 20-11.4.
- **Part 4.** About 0.67% of the draws fall outside ±3 mV.
- **Part 5.** The interval 0.878 σ̂ to 1.162 σ̂, built from each run's estimate σ̂, contains the true σ in about 95% of runs. (The estimates themselves scatter within 0.861–1.139 times the true σ, 95% of the time: a different interval, because it is centred on the truth rather than on the estimate.) A 3σ claim needs about 1109 failure-free runs; a 4.5σ claim needs hundreds of thousands, which is why high-sigma yield needs importance sampling or extrapolation rather than brute force.

## Discussion

1. **Why does the area law need independent patches?** A device's threshold is the average of many local contributions; if they are independent, the variance of the average falls as one over their number, which is proportional to area. Correlated contributions, such as gradients, do not average away.
2. **Why do mirrors and pairs want opposite $g_m/I_D$?** In a mirror, a threshold error is converted into a current error by $g_m/I_D$; in a pair, a gain-factor error is converted into a voltage error by dividing by $g_m/I_D$.
3. **Why is a clean 100-run Monte Carlo weak evidence?** Zero failures in 100 runs only shows, at 95% confidence, that the failure rate is below about 3%.

## Optional hardware

Measure $V_{GS}$ at a fixed drain current for each transistor of a few CD4007 or ALD1106 arrays (matched-pair MOSFET packages) with a bench supply and a multimeter, and compute the spread of the differences. Compare pairs within one package with pairs across packages: the second spread includes global variation.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 20-11.a | ngspice mismatch, 10 µA | 1.99 | % |
| Lab 20-11.b | ngspice mismatch, 100 µA | 0.631 | % |
| Lab 20-11.c | ngspice mismatch, 400 µA | 0.316 | % |
| Lab 20-11.d | linear formula, 10 µA | 2.00 | % |
| Lab 20-11.e | linear formula, 100 µA | 0.632 | % |
| Lab 20-11.f | linear formula, 400 µA | 0.316 | % |
