# Lab 25-10 · Qualification Equivalence and FMEDA Metrics

**Objective.** Convert qualification stresses into field equivalents, compute FMEDA hardware metrics and find the safety-mechanism coverage they demand, and check the dual-point PMHF approximation against a Monte Carlo of latent faults and periodic self-test.

**Chapter:** [25-10 · Qualification and Functional Safety](../../chapters/25-10-qualification-and-functional-safety.md)

## Background

§3.2 gave the Coffin–Manson cycling equivalence $(\Delta T_s/\Delta T_{field})^n$ and the mission-profile stress hours $\sum w_it_{life}/AF(T_i \to T_s)$. §3.4 defined SPFM and LFM and derived the dual-point rate $\lambda_L\lambda_{DD}\tau$, with $\lambda_{DD}$ the covered dangerous-fault rate and $\tau$ half the test interval. §3.6 gave the vehicle defect fraction $1 - (1 - p)^M$.

## Files

- `qual.py`: temperature-cycling and HTOL equivalence, FMEDA metrics, the dual-point rate, a Monte Carlo of latent faults with periodic test, vehicle defect fractions and zero-failure sample sizes.
- `25-10-qual-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Coverage requirement** (notebook). For Example 25-10.4's element, *predict* the lockstep diagnostic coverage needed for a 99% SPFM, then solve for it and plot SPFM and LFM against the coverages.

**Part 2 · Activation energy** (notebook). *Predict* the stress hours at 150 °C that cover the automotive mission profile with $E_a$ = 0.5 eV, then compute them and plot against $E_a$.

**Part 3 · Latent faults by Monte Carlo** (notebook). With a latent-fault rate of 2 × 10⁻⁶/h, a covered dangerous-fault rate of 2 × 10⁻⁵/h (both scaled up so effects are visible), a 15,000 h life and a self-test every 1,000 h, *predict* how close the simulated dual-point rate comes to $\lambda_L\lambda_{DD} T/2$, then simulate it.

**Part 4 · Vehicles** (notebook). *Predict* the fraction of vehicles with 20,000 components at 0.1 ppm that carry a defect, then compute it and plot against the component rate.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 25-10.a | lockstep coverage for 99% SPFM | 98.2 | % |
| Lab 25-10.b | stress hours at 150 °C, 0.5 eV | 2.33e3 | h |
| Lab 25-10.c | simulated over approximate dual-point rate | 0.98 | |
| Lab 25-10.d | vehicles affected | 0.200 | % |

The simulated ratio falls slightly below 1 for two reasons, both second order in the rates: a latent fault can only arrive while none has arrived before (the survival factor $e^{-\lambda_Lt}$ is not quite 1 here), and the chance of a dangerous fault during an exposure $w$ is $1 - e^{-\lambda_{DD}w}$, a little less than $\lambda_{DD}w$. The first effect is the larger. With real FIT-level rates the approximation is essentially exact.

## Discussion

1. Part 1 shows SPFM depends on the safe-fault fraction as well as on coverage. Why do FMEDA reviews scrutinize the safe-fault assumptions so closely?
2. In Part 3, what happens to the ratio as the test interval approaches the vehicle life? Why?
3. Part 2: a supplier qualifies with $E_a$ = 0.7 eV, but the dominant field mechanism has 0.5 eV. What is the consequence?
4. Part 4: which is easier to improve, the component count or the per-component defect rate, and who controls each?

## Optional hardware

None needed. Automotive MCU vendors publish safety manuals and FMEDA summaries for their devices; reading one alongside this lab shows the structure of a real FMEDA.
