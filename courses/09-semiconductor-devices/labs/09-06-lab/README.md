# Lab 09-06 · PN Junction I–V, Capacitance and Breakdown

**Chapter:** [09-06](../../chapters/09-06-pn-junction-iv-and-capacitance.md) · **Notebook:** [09-06-diode.ipynb](09-06-diode.ipynb) · **Netlist:** [diode.cir](diode.cir) · **Time:** about 2.5 hours

## Objective

1. Assemble a real diode's I–V characteristic from its physical parts (diffusion, depletion-region recombination, high-level injection, series resistance), and recover the parameters from a synthetic measurement.
2. Measure a diode's forward-voltage temperature coefficient and build a PTAT thermometer.
3. Solve the time-dependent diffusion equation for reverse recovery, and compare the storage time with the charge-control and Kingston formulas.
4. Evaluate the impact-ionization integral: breakdown voltage against doping and multiplication against voltage, from electron- and hole-initiated forms.
5. Confirm in ngspice that the SPICE diode model reproduces the chapter's operating point and follows charge control for storage time.

## Background

Chapter sections 3.1–3.9 and Examples 09-06.1 to 09-06.7. The reverse-recovery solver works in dimensionless units: distance in diffusion lengths and time in lifetimes, so that $\partial u/\partial t = \partial^2u/\partial x^2 - u$. It starts from the steady forward profile $u = e^{-x}$ and reverses the flux at $x = 0$ to $I_R/I_F$ times its forward value. It steps in time with the Crank–Nicolson method (unconditionally stable and second-order accurate, [02-10](../../../02-complex-numbers-des-and-linear-algebra/chapters/02-10-numerical-methods.md)). The storage time is when $u(0, t)$ reaches zero. The avalanche part integrates the current-continuity equations through the depletion region with SciPy's `solve_ivp`. You need Python with NumPy, SciPy and Matplotlib, and optionally ngspice (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [09-06-diode.ipynb](09-06-diode.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s, which compare with Examples 09-06.1 to 09-06.7 and the answer key below |
| [diode.cir](diode.cir) | ngspice: operating point at 10 µA and storage time of the SPICE diode model | `* EXPECT` lines tied to the chapter's answer key (run by `tools/run_spice.py`) |

## Procedure

1. **A real I–V curve (Part 1).** *Predict first:* with $R_s$ = 50 Ω, at what current does the series-resistance drop equal one thermal voltage? Then build the four-part model of Figure 2, plot it on semilog axes, and compute the local ideality factor against voltage. Finally, fit a synthetic data set for $I_0$, $\eta$ and $R_s$.
2. **Temperature (Part 2).** *Predict first:* will $dV/dT$ be larger in magnitude at 1 µA or at 1 mA? Then compute $V(T)$ at several currents from 250 K to 400 K, and the PTAT difference between two currents.
3. **Reverse recovery (Part 3, the chapter's guided exercise).** *Predict first:* if the reverse current is doubled from $I_F$ to $2I_F$, does the exact storage time halve, fall by more than half, or by less, and does charge control predict the same factor? Then solve for $I_R/I_F$ = 1 and 2 and plot $u(0, t)$ and the profiles.
4. **Avalanche (Part 4).** *Predict first:* by how much does the multiplication factor rise between 80% and 95% of the breakdown voltage? Then compute $V_B(N)$ for 10¹⁵ to 10¹⁷ cm⁻³, $M(V)$ for 10¹⁶ cm⁻³, and confirm that electron- and hole-initiated breakdown agree.
5. **ngspice (optional).** Run `ngspice -b diode.cir` and compare the printed operating point and storage time with Examples 09-06.1 and 09-06.6.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Local ideality factor | close to 2 near 0.2 V, falling to nearly 1 around 0.6 V, rising steeply above 0.65 V (Figure 2) |
| 1 | Current where $IR_s = V_T$ | see the answer key |
| 2 | $dV/dT$ at 10 µA, 300 K | −2.217 mV/K (Example 09-06.4) |
| 3 | $t_s/\tau_p$ for $I_R = I_F$ | 0.2275 exact, 0.693 charge control (Example 09-06.6) |
| 3 | $t_s/\tau_p$ for $I_R = 2I_F$ | see the answer key |
| 4 | $V_B$ at 10¹⁶ cm⁻³ | 54.7 V by both forms (Example 09-06.7) |
| 5 | ngspice | 0.6133 V at 10 µA; storage time 0.693 µs with a 1 µs transit-time parameter |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 09-06.a | exact t_s/τ for I_R = 2 I_F | 0.0928 | — |
| Lab 09-06.b | charge-control t_s/τ for I_R = 2 I_F | 0.405 | — |
| Lab 09-06.c | exact reduction factor from doubling I_R | 2.45 | — |
| Lab 09-06.d | charge-control reduction factor | 1.71 | — |
| Lab 09-06.e | hole-initiated V_B at 1e16 | 54.7 | V |
| Lab 09-06.f | current where I R_s = V_T (R_s = 50 Ω) | 0.517 | mA |

## Discussion questions

1. Part 1's fitted ideality factor depends on which voltage range you fit. Why do datasheets and SPICE models still use a single $\eta$?
2. In Part 2, why is the magnitude of $dV/dT$ larger at low current?
3. In Part 3, why does doubling the reverse current more than halve the exact storage time, while charge control predicts a smaller reduction?
4. In Part 4, why must electron- and hole-initiated multiplication give the same breakdown voltage even though their multiplication factors below breakdown differ?
5. The ngspice model's storage time matches charge control, not the exact diffusion solution. What does that imply for a designer using SPICE to size a snubber or estimate switching loss?

<details><summary>Answers to the discussion questions</summary>

1. Over the range where a circuit operates, usually one or two decades of current, a single exponential fits well, and simulators need a compact model. The single $\eta$ is a local fit, not physics. A diode that works across many decades (a logarithmic amplifier, a temperature sensor at microamps) needs the full multi-component model, or a fit made at its own operating current.
2. $dV/dT = (V - V_{g0} - 3V_T)/T$. A lower current means a lower $V$, which makes the numerator more negative. Physically, the junction at low bias sits farther below the bandgap voltage that it approaches as $T \to 0$, so it has farther to move per kelvin.
3. The exact storage phase ends when the *edge* density reaches zero. A larger reverse current steepens the extraction gradient at the edge, emptying it before the deeper charge is touched, so the time falls by a factor of **2.45**. Charge control looks only at the *total* charge, which drains at a rate $I_R + Q/\tau$; doubling $I_R$ shortens that by only **1.71**. The two answers are $t_s/\tau_p$ = **0.0928** exact against **0.405** by charge control.
4. Breakdown is the condition at which the current becomes self-sustaining: the multiplication factor diverges for *any* injected carrier, because each carrier's offspring of both types keep regenerating the chain. Below breakdown, which carrier starts the chain matters, since electrons ionize more readily than holes at moderate fields; at the divergence it does not. Part 4 finds **54.7** V by both routes.
5. SPICE's transit-time parameter is fitted to measured switching data (often the measured storage time or reverse-recovery charge at a specified condition). It reproduces that condition but scales with $I_F/I_R$ according to charge control. A designer extrapolating to very different drive conditions should check against measured recovery data at those conditions, or use a model fitted there.

</details>

## Optional extension

Add depletion-region recombination to the reverse-recovery solver's boundary, or replace the long diode with a short one (an absorbing boundary at $x = W_n/L_p$), and find how the ratio of exact to charge-control storage time changes. For a short diode, the stored charge empties in about a transit time, and the two methods disagree less.
