# Lab 25-03 · CVD Regimes, Dopant Diffusion, CMP and Gauge Noise

**Objective.** Map CVD's two regimes on an Arrhenius plot; follow an implant through an anneal with a finite-difference diffusion solver that includes the wafer surface; model CMP planarization; and see how gauge noise distorts process capability.

**Chapter:** [25-03 · Deposition, Etch, CMP, Implant and Metrology](../../chapters/25-03-deposition-etch-cmp-implant-metrology.md)

## Background

§3.1 derived the CVD growth rate $v = (C_g/N)k_sh_g/(k_s + h_g)$. §3.6–3.7 gave the Gaussian implant profile and its broadening by $2Dt$, ignoring the surface; here the surface is a zero-flux boundary, handled exactly by adding a mirror-image Gaussian and numerically by finite differences. §3.5 applied Preston's law to raised features at area fraction $\rho$. §3.8 showed that measurement and process variances add.

## Files

- `units.py`: Arrhenius scaling, CVD rate and crossover temperature, ALD cycles, plating rate, stop-layer loss and a wafer map of clearing times, Preston rate and step removal, Gaussian profiles, junction depth, boron diffusivity, an explicit finite-difference diffusion solver with a zero-flux surface, the image-method solution, apparent $C_{pk}$ and simulated measurements.
- `25-03-units-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · CVD regimes** (notebook). Using Example 25-03.1's constants, *predict* the temperature at which $k_s = h_g$, then plot the growth rate against $1/T$ and find it.

**Part 2 · Implant and anneal** (notebook). Start from Example 25-03.6's profile (dose 10¹⁵ cm⁻², $R_p$ = 30 nm, $\Delta R_p$ = 12 nm) and anneal it for 30 min at 1000 °C. *Predict* the junction depth against the 10¹⁸ cm⁻³ background, then compute it with the finite-difference solver and with the image method, and compare with the as-implanted 70.9 nm and the spike-annealed profile.

**Part 3 · CMP** (notebook). *Predict* how long Example 25-03.5's process takes to remove a 300 nm step where raised features cover 25% of the area, then compute it and sweep the density.

**Part 4 · Gauge noise** (notebook). *Predict* the apparent $C_{pk}$ of Example 25-03.8's process measured with $\sigma_m$ = 0.05 nm, then simulate 10,000 measurements.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 25-03.a | temperature where ks = hg | 875 | °C |
| Lab 25-03.b | junction depth after furnace anneal, with surface | 244 | nm |
| Lab 25-03.b1 | surface concentration after furnace anneal | 9.80e19 | cm⁻³ |
| Lab 25-03.c | time to remove a 300 nm step at 25% density | 0.38 | min |
| Lab 25-03.d | apparent Cpk with a 0.05 nm gauge | 0.99 | |

The finite-difference and image-method junction depths agree to well under a nanometre; the simulated $C_{pk}$ is within 2% of the formula.

## Discussion

1. Why does the reflecting surface deepen the junction slightly compared with the no-surface Gaussian of §3.7?
2. Part 2's furnace anneal moves the junction from 71 nm to about 244 nm. Which modern anneals avoid this, and what do they give up?
3. Part 3's model lets only raised features touch the pad. What would a compliant pad change, and why do real recessed areas start polishing before the step is gone?
4. In Part 4, how much does halving the gauge noise improve the apparent $C_{pk}$? When is a better gauge not worth buying?

## Optional hardware

None needed. A university cleanroom typically offers a four-point probe and an ellipsometer; measuring sheet resistance before and after an anneal shows activation directly.
