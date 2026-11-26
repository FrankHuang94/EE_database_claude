# Lab 25-08 · Spreading, Fins, Cold Plates and Mission Profiles

**Objective.** Compare the 45° spreading estimate with a finite-difference solution, check the fin-efficiency formula against a numerical solution of the fin equation, find the power limit of a cold plate, and weight a mission profile by Arrhenius damage.

**Chapter:** [25-08 · Thermal Engineering](../../chapters/25-08-thermal-engineering.md)

## Background

§3.2 derived the hotspot rise $qa/k$, the spreading resistance $8/(3\pi^2ka)$ and the 45° estimate $t/(k\pi a(a + t))$ for a lid. §3.3 derived the fin equation $\theta'' = m^2\theta$ and the efficiency $\tanh(mL)/mL$. §3.4 gave the coolant rise $P/(\rho c_p\dot{V})$ and the junction budget, and §3.5 the Arrhenius-equivalent temperature of a mission profile.

## Files

- `thermal.py`: slab and hotspot resistances, an axisymmetric finite-volume solver for a disk source on a cylindrical spreader, the 45° estimate, fin efficiency by formula and by solving the boundary-value problem, coolant flow, the junction budget and the Arrhenius-equivalent temperature.
- `25-08-thermal-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Spreading** (notebook). For Example 25-08.3's die (16 mm radius) on copper lids 1 to 10 mm thick, *predict* whether the 45° estimate gets better or worse as the lid thickens, then compare it with the finite-volume solution and plot the temperature field for the 3 mm lid.

**Part 2 · Fins** (notebook). *Predict* the efficiency of Example 25-08.4's fin made of copper, then compute it by formula and by solving the fin equation, and plot efficiency against $mL$.

**Part 3 · Cold-plate limit** (notebook). With 0.035 K/W, 45 °C inlet, 2 L/min and a 105 °C limit, *predict* the largest power, then solve for it and sweep the flow.

**Part 4 · Mission profile** (notebook). *Predict* the AM625 automotive profile's Arrhenius-equivalent temperature with a 1.0 eV activation energy, then compute it and plot it against activation energy.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 25-08.a | 45° error, 1 mm lid | -2.6 | % |
| Lab 25-08.a1 | 45° error, 10 mm lid | -10.0 | % |
| Lab 25-08.b | copper fin efficiency | 0.885 | |
| Lab 25-08.c | cold-plate power limit | 1.55e3 | W |
| Lab 25-08.d | equivalent temperature, 1.0 eV | 102 | °C |

The numerical fin solution agrees with $\tanh(mL)/mL$ to better than 0.1%, and the finite-volume spreading resistance changes by less than 0.2% when the grid is doubled.

## Discussion

1. Why does the 45° rule underestimate the spreading resistance more for thicker lids (it assumes more spreading than occurs), and what would happen with a poorly cooled underside instead of an isothermal one?
2. Part 2's fin efficiency barely depends on the fin's depth. Why, and what does set how deep a heat sink should be?
3. Part 3 shows the flow matters little at 2 L/min. At what flow would the coolant rise become the dominant term?
4. How would you choose an activation energy for Part 4 when several wear-out mechanisms act at once (25-09)?

## Optional hardware

An inexpensive experiment: mount a power resistor on an aluminium plate with and without thermal paste and log its temperature with a thermocouple; the change in steady-state rise per watt measures the interface resistance directly.
