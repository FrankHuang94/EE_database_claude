# Lab 09-14 · Optoelectronic Devices

**Chapter:** [09-14](../../chapters/09-14-optoelectronic-devices.md) · **Notebook:** [09-14-optoelectronics.ipynb](09-14-optoelectronics.ipynb) · **Netlist:** [solarcell.cir](solarcell.cir) · **Time:** about 2 hours

## Objective

1. Compute solar-cell I–V and power curves, and see how open-circuit voltage, fill factor and efficiency respond to light intensity and series resistance.
2. Simulate photon arrivals at an image-sensor pixel and build a photon-transfer curve that separates shot noise from read noise.
3. Simulate a SPAD time-of-flight histogram with ambient light and locate the target.
4. Ray-trace photons inside a planar LED chip and measure the fraction that escapes.
5. Confirm $V_{oc}$ and the maximum-power operating point in ngspice.

## Background

Chapter sections 3.1–3.7 and Examples 09-14.1 to 09-14.8. The solar cell is the ideal diode of 09-06 with a photocurrent: $J = J_{sc} - J_0(e^{V/V_T} - 1)$, with $J_{sc}$ = 40 mA/cm² at 100 mW/cm² and $J_0$ = 10⁻¹³ A/cm². Photon counts are Poisson (03-02); the simulations are seeded so the numbers repeat. You need Python with NumPy, SciPy and Matplotlib, and optionally ngspice (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [09-14-optoelectronics.ipynb](09-14-optoelectronics.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s, which compare with the chapter's examples and the answer key below |
| [solarcell.cir](solarcell.cir) | ngspice: an open-circuited cell and a cell driving the maximum-power load | `* EXPECT` lines tied to Example 09-14.8 (run by `tools/run_spice.py`) |

## Procedure

1. **Solar cell (Part 1, the chapter's guided exercise).** *Predict first:* if the light intensity doubles, by how much does $V_{oc}$ rise, and does the efficiency rise, fall or stay the same? Then compute both, and add series resistance.
2. **Photon transfer (Part 2).** *Predict first:* on a log–log plot of noise against signal, what slope does the shot-noise region have? Then simulate.
3. **Time of flight (Part 3).** *Predict first:* with 0.1 detected signal photons per pulse, how many pulses are needed before the target peak stands out from ambient light? Then simulate.
4. **LED extraction (Part 4).** *Predict first:* what fraction of photons escapes through the top face of a flat GaAs chip? Then ray-trace and compare with $(1 - \cos\theta_c)/2$.
5. **ngspice (optional).** Run `ngspice -b solarcell.cir` and compare with Example 09-14.8.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | $V_{oc}$, $V_{mp}$, fill factor, efficiency at 1 sun | 0.6906 V, 0.6079 V, 0.844, 23.3% (Example 09-14.8) |
| 1 | $V_{oc}$ rise and efficiency at 2 suns; maximum-power load | see the answer key |
| 2 | Photon-transfer slope in the shot-noise region | 1/2 |
| 3 | Target peak | 33.4 ns (5.00 m) |
| 4 | Ray-traced escape fraction | within 5% of 0.0235 |
| 5 | ngspice $V_{oc}$ and $V_{mp}$ | 0.6906 V and 0.6079 V |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 09-14.a | V_oc rise for doubled light | 17.9 | mV |
| Lab 09-14.b | efficiency at 2 suns | 24.0 | % |
| Lab 09-14.c | maximum-power load, 1 cm² cell | 15.84 | Ω |

## Discussion questions

1. Why does $V_{oc}$ rise only logarithmically with light, and why does the efficiency rise at all?
2. Why does the photon-transfer curve flatten at low signal?
3. Why does ambient light limit a dToF sensor's range more than its depth resolution?
4. Why does the ray-traced escape fraction agree with the cone formula only for an absorbing chip?

<details><summary>Answers to the discussion questions</summary>

1. $V_{oc} = V_T\ln(J_{sc}/J_0 + 1)$, so doubling $J_{sc}$ adds $V_T\ln 2$ = **17.9** mV. The current doubles with the light, so output power rises slightly faster than the input power because the voltage also rises: the efficiency goes from 23.3% to **24.0**%. This is the physics behind concentrator cells. The 1-sun maximum-power load for a 1 cm² cell is **15.84** Ω, which the netlist uses.
2. At low signal, read noise (constant) dominates the shot noise ($\sqrt N$), so the noise floor is flat; at higher signal the shot noise takes over with slope 1/2 on log–log axes.
3. Ambient photons arrive uniformly in time and raise the histogram floor everywhere. Far targets return fewer photons (falling as the inverse square of distance), so the peak sinks into the floor. Depth resolution depends on the timing jitter, not the photon count.
4. The formula counts photons on their first arrival at the surface. In a transparent chip, totally reflected photons bounce and get further chances (especially after scattering), so more escape; the formula is the single-pass estimate, valid when the chip absorbs trapped light quickly.

</details>

## Optional extension

Add a temperature dependence to the solar cell: let $J_0 \propto T^3e^{-E_g/kT}$ with $E_g$ = 1.12 eV, normalized to 10⁻¹³ A/cm² at 300 K. Find $dV_{oc}/dT$ at 300 K and the efficiency at 60 °C, and compare with the 1-sun value.
