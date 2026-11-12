# Lab 02-03 · Second-Order Linear ODEs

**Chapter:** [02-03](../../chapters/02-03-second-order-linear-odes.md) · **Notebook:** [02-03-second-order.ipynb](02-03-second-order.ipynb) · **Netlists:** [rlc_natural.cir](rlc_natural.cir), [pdn_droop.cir](pdn_droop.cir) · **Time:** about 75 minutes

## Objective

1. Connect characteristic roots in the complex plane with the shape of the natural response.
2. Measure overshoot, peak time and settling time from simulations, and confirm the formulas of chapter §3.8.
3. Confirm the energy balance $dw/dt = -Ri^2$.
4. Explore the power-delivery design space: how droop depends on $L$ and $C$.
5. Confirm the chapter's ring-down and droop results in ngspice.

## Background

Chapter sections 3.3–3.6 (the three cases), 3.7 (initial conditions), 3.8 (step-response specifications), 3.9 (roots in the complex plane) and 3.11 (energy), and Examples 02-03.2, 02-03.3 and 02-03.5.

## Procedure

1. Run all notebook cells in order, writing down a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict how many cycles a ζ = 0.1 ring-down lasts before falling below 5%.
3. **Part 2:** predict which ζ settles into ±2% fastest, then read the table.
4. **Part 3:** confirm that the stored energy drains exactly through the resistor.
5. **Part 4:** predict whether doubling $C$ or halving $L$ cuts the droop more.
6. **Part 5:** from the repository root, run `python tools/run_spice.py 02-03`. Then edit `pdn_droop.cir` to halve `L1` to 12.5 pH, predict the new droop, and re-run.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | ζ = 0.1 ring-down to 5% | $\omega_0t = \ln20/0.1 = 30.0$, about 4.74 cycles |
| 2 | overshoot and peak time | simulation equals the formulas: 16.303% and $3.628/\omega_0$ at ζ = 0.5 |
| 2 | 2% settling | fastest near ζ = 0.78 ($3.605/\omega_0$); critical damping $5.834/\omega_0$ |
| 3 | energy | 12.500 µJ at the start; $dw/dt + Ri^2 \approx 0$ to numerical precision |
| 3 | first negative peak | −3.023 V at 10.06 µs |
| 4 | droop with C doubled or L halved | 114.0 mV either way, from 160.3 mV |
| 5 | `rlc_natural.cir` | −3.023 V at 10.06 µs; 8.626 V at 147.8 µs |
| 5 | `pdn_droop.cir` | 160.3 mV at 2.535 ns; 24.95 mV with 4.938 µF |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 02-03.a | ω0·t for a ζ = 0.1 envelope to reach 5 % | 30.0 | — |
| Lab 02-03.b | cycles to 5 % at ζ = 0.1 | 4.74 | — |
| Lab 02-03.c | initial stored energy | 12.500 | µJ |
| Lab 02-03.d | droop with C doubled | 114.0 | mV |
| Lab 02-03.e | droop with L halved | 114.0 | mV |
| Lab 02-03.f | ζ = 0.5 peak time, ω0·tp | 3.628 | — |

## Discussion questions

1. Part 2 shows that critical damping is not the fastest way to settle. Why might a designer still choose ζ ≥ 1, for example in a circuit driving a sensitive load?
2. In Part 4, doubling $C$ and halving $L$ give the same droop. What else differs between the two fixes, and why might a power-integrity engineer prefer one?
3. A colleague proposes damping the supply by adding series resistance in the supply path. Using Example 02-03.5, explain the cost, and suggest where damping resistance is better placed.

## Optional hardware version

With a 10 mH inductor, a 100 nF capacitor, resistors of 10 Ω, 100 Ω and 680 Ω, a function generator and an oscilloscope: build the series RLC ($f_0 \approx 5$ kHz) and drive it with a low-frequency square wave through the resistor. Measure the capacitor voltage. With 10 Ω (plus the inductor's own winding resistance) it rings; with about 630 Ω ($2\sqrt{L/C}$) it is close to critically damped. From the 10 Ω trace, read the overshoot and ringing period and infer ζ and $\omega_0$ as in Example 02-03.4. The inferred ζ will exceed the value computed from 10 Ω alone, because the inductor's winding resistance adds damping.
