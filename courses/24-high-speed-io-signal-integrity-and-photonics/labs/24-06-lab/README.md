# Lab 24-06 · The Energy and Speed of a Short Wire

**Objective.** Measure in ngspice the supply energy of one edge on a 2 mm unterminated interposer wire and its rise time; compare them with $CV^2$ and the Elmore estimate; and compute bandwidth densities and fabric bandwidths.

**Chapter:** [24-06 · Die-to-Die Links, Memory PHYs and Scale-Up Fabrics](../../chapters/24-06-d2d-memory-phys-scale-up.md)

## Background

§3.1 showed that charging a capacitance $C$ to $V$ draws $CV^2$ from the supply whatever the resistance in the path, and that an RC wire's delay is roughly its Elmore delay $R_{on}C_{tot} + R_w(C_w/2 + C_L)$. §3.2 gave areal density as $\phi r/(8p^2)$.

## Files

- `make_wire.py` and `wire.cir`: Example 24-06.1's wire (50 Ω, 200 fF, 50 fF pads, 40 sections) driven through 50 Ω by a 0.5 V step.
- `d2d.py`: wire energies, an exact RC-ladder step response by eigen-decomposition, Elmore delay, bump and bandwidth densities, power at a given energy per bit.
- `24-06-d2d-lab.ipynb`: the notebook for all three parts.

## Procedure

**Part 1 · Energy** (ngspice and notebook). *Predict* the supply energy of one rising edge, then run `ngspice -b wire.cir` and compare its integrated supply power with $CV^2$.

**Part 2 · Speed** (ngspice and notebook). *Predict* whether the receiver's 10–90% rise time is shorter or longer than a 32 GT/s UI, then compare ngspice with the exact ladder solution and the Elmore estimate. Repeat in the notebook with a 25 Ω driver.

**Part 3 · Density and fabrics** (notebook). *Predict* the areal density at 25 µm pitch with half the bumps at 32 Gb/s, and NVL72's total GPU bandwidth, then compute them.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 24-06.a | supply energy of one edge | 75 | fJ |
| Lab 24-06.b | 10-90% rise time | 43.7 | ps |
| Lab 24-06.c | 50% delay | 16.5 | ps |
| Lab 24-06.d | Elmore delay | 22.5 | ps |
| Lab 24-06.e | 10-90% rise time with a 25 ohm driver | 28.0 | ps |
| Lab 24-06.f | areal density at 25 um | 3200 | GB/s/mm² |
| Lab 24-06.g | NVL72 total | 129.6 | TB/s |

- Part 1: ngspice integrates 74.9 fJ, within 0.2% of $CV^2$ = 75 fJ; half of it ends on the capacitors and half is burned in the resistances.
- Part 2: the rise time is 43.7 ps, longer than the 31.25 ps UI at 32 GT/s; the 50% delay is 16.5 ps, under the 22.5 ps Elmore bound. Halving the driver resistance to 25 Ω cuts the rise time to 28.0 ps, under one UI, which shows that the driver, not the wire, sets the speed of this link.
- Part 3: 3,200 GB/s/mm² at 25 µm; 129.6 TB/s for 72 GPUs at 1.8 TB/s.

## Discussion

1. Why is the supply energy $CV^2$ whatever the resistance?

   <details><summary>Answer</summary>

   The supply delivers a total charge $CV$ at voltage $V$, so it supplies $CV \cdot V$. The capacitor ends with $CV^2/2$, so the other half is dissipated in the resistances; their values change how fast this happens, not how much.

   </details>

2. Why is the Elmore delay larger than the measured 50% delay?

   <details><summary>Answer</summary>

   Elmore is the first moment of the impulse response, an upper bound on the 50% delay of an RC tree. For a single pole the 50% delay is $\ln 2 \approx 0.69$ of it; a distributed line falls between.

   </details>

3. What would reduce this link's energy per bit most: a shorter wire, a lower swing or a slower rate?

   <details><summary>Answer</summary>

   A lower swing, since energy goes as $V^2$: halving $V$ quarters the wire energy. A shorter wire reduces $C$ linearly; a slower rate does not change the energy per bit at all, though it relaxes the circuits around the wire.

   </details>

## Optional hardware

A long PCB trace driven by a fast CMOS buffer through a series resistor, observed with an oscilloscope while measuring supply current with a current probe, shows the same $CV^2$ energy and RC rise time at board scale.
