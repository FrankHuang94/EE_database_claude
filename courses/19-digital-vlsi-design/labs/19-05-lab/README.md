# Lab 19-05 · Wires: Distributed RC, Repeaters and Crosstalk

Chapter: [19-05 · Interconnect](../../chapters/19-05-interconnect.md)

## Objective

- Compare the distributed RC line's exact step response with lumped, Elmore and ladder approximations.
- Check the driver–wire–load estimate against simulation in Python and ngspice.
- Optimize repeaters for a long wire and measure how flat the optimum is.
- Compute crosstalk on floating and switching victims, and the effect of wire scaling.

## Background

A distributed RC line obeys the diffusion equation $rc\,\partial v/\partial t = \partial^2v/\partial x^2$; its far end reaches 50% at $0.379RC$ (§3.3). A driven wire's delay is about $0.69R_d(C_w + C_L) + R_w(0.38C_w + 0.69C_L)$ (§3.4). As in the chapter, 0.69 and 0.38 stand for $\ln 2$ and 0.379, kept unrounded in every calculation. Optimal repeaters give $T_{min} = 2.41\sqrt{R_0C_0\,rc}\,L$ (§3.5). A floating victim moves by $\Delta V_{agg}C_c/(C_c + C_g)$, and coupling capacitance counts 0, 1 or 2 times when the victim switches (§3.6).

Files:

- `rcline.cir`: Example 19-05.3's 1 mm wire as a 100-section ladder, bare and with a 1 kΩ driver and a 10 fF load.
- `glitch.cir`: Problem 19-05.14's driven victim for three combinations of driver resistance and aggressor ramp.
- `wires.py`: `wire_resistance`, `sheet_resistance`, `plate_cap_per_length`, `coupling_cap_per_length`, `line_step_response` and `line_t50` (the Fourier series), `ladder_t50` (exact ladder response by the matrix exponential), `driver_wire_load_delay`, `repeater_optimum`, `repeated_delay`, `floating_victim_noise` and `effective_cap`.
- `19-05-wires-lab.ipynb`: the procedure below.

## Procedure

1. **The distributed line.** Predict where the far end of a step-driven line reaches 50%, in units of $RC$. Run Part 1, which plots the Fourier-series response against lumped and Elmore estimates.
2. **Ladders.** Predict how many ladder sections are needed to get within 1% of the distributed result; run Part 2 and `ngspice -b rcline.cir`.
3. **Driver, wire and load.** Predict the delay of Example 19-05.3(b); compare the formula with the ladder simulation (Part 3).
4. **Repeaters.** Predict the penalty for using half or twice the optimal number of repeaters, and half or twice the optimal size; run Part 4.
5. **Crosstalk and scaling.** Predict the floating-victim disturbance against $C_c/C_g$, and the repeated-wire delay per millimetre if $R_0C_0$ halves (Part 5).

## Expected results

- Part 1: 50% at 0.379 $RC$ (lumped 0.69, Elmore 0.35).
- Part 2: an $n$-section ladder overestimates the delay by about $1/n$: 9.9% for 10 sections, 2.0% for 50 and 1.0% for 100. The 100-section ladder in ngspice gives 1007.4 ps for the bare wire and 1262.8 ps with its driver and load.
- Part 3: the formula gives 1234.4 ps; ladders converge to 1253.2 ps as the sections increase, so the formula is 1.5% low.
- Part 4: half or twice the optimal number of repeaters costs 10.6%; half or twice the optimal size costs 14.4%.
- Part 5: the disturbance rises from 0 to half the aggressor swing as $C_c$ grows to $C_g$; halving $R_0C_0$ cuts the delay per millimetre from 123.7 to 87.5 ps.

## Discussion

1. Why does a ladder overestimate the distributed line's delay, and why does the error fall as $1/n$?
2. Why is the delay so insensitive to the number and size of repeaters near the optimum?
3. In `rcline.cir`, why is the driven wire's delay (1262.8 ps) more than the bare wire's (1007.4 ps) plus the driver's own $\ln 2\,R_d(C_w + C_L)$ (144.2 ps)?
4. Why do memories and dynamic logic care more about floating-victim crosstalk than static logic does?

**Answers.**

1. A ladder places each section's capacitance after its full resistance, so on average the capacitance is charged through slightly more resistance than in the continuous line; the excess per section is a fraction $1/n$ of the total.
2. At an optimum the first derivative is zero, so small departures cost only in second order: halving or doubling a variable changes the sum $ax + b/x$ by $(0.5 + 2)/2 - 1$ = 25% of that pair of terms, which is a fraction of the total.
3. The load's 10 fF is charged through the whole wire ($\ln 2\,R_wC_L$ = 92.2 ps), and the driver's resistance slows the wire's own diffusion as well as charging it.
4. A floating node has no driver to restore it, so any coupled charge stays until the next precharge; a static gate's driver pulls a disturbed node back.

## Optional hardware

A long, thin PCB trace is too conductive to show RC diffusion, but a chain of resistors and capacitors on a breadboard (for example ten 10 kΩ resistors and ten 1 nF capacitors) does: drive it with a square wave from a function generator and compare the far-end waveform with the near end, then insert a buffer (an op-amp follower) halfway and watch the delay fall.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 19-05.a | 100-section ladder, bare wire | 1007.4 | ps |
| Lab 19-05.b | 100-section ladder, with driver and load | 1262.8 | ps |
| Lab 19-05.c | ladder excess, 10 sections | 9.9 | % |
| Lab 19-05.d | ladder excess, 50 sections | 2.0 | % |
| Lab 19-05.e | ladder excess, 100 sections | 1.0 | % |
| Lab 19-05.f | penalty for half or twice the repeater count | 10.6 | % |
| Lab 19-05.g | penalty for half or twice the repeater size | 14.4 | % |
| Lab 19-05.h | repeated delay per mm with R0C0 halved | 87.5 | ps |
| Lab 19-05.i | load charged through the wire | 92.2 | ps |
