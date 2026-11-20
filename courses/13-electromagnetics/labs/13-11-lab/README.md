# Lab 13-11 · Radiation and Antenna Fundamentals

Chapter: [13-11 Radiation and Antenna Fundamentals](../../chapters/13-11-radiation-and-antennas.md)

## Objective

Compute the near and far fields of a Hertzian dipole from its retarded potential, build the patterns of longer dipoles by summing elements, run link budgets across frequency for fixed-gain and fixed-area antennas, and steer phased arrays and find their grating lobes. Then see in ngspice that a matched small antenna still radiates only a quarter of the power it accepts.

## Background

Retarded potentials and the Hertzian dipole (§3.1–3.2), patterns and directivity (§3.3), the half-wave dipole (§3.4), Friis (§3.5) and arrays (§3.6).

## Files

- [13-11-antennas.ipynb](13-11-antennas.ipynb): the notebook (Parts 1–4).
- [small_antenna.cir](small_antenna.cir): Example 13-11.1's λ/50 antenna (0.3156 Ω radiation resistance plus 1 Ω loss) matched to 50 Ω at 100 MHz. Run with `ngspice -b small_antenna.cir`, or `python tools/run_spice.py 13-11` from the repository root.

## Procedure

1. **Near and far (Part 1).** Plot the magnitudes of the three terms of $E_\theta$ against $kr$. *Predict first:* where do they cross?
2. **Dipole patterns (Part 2).** Sum Hertzian elements along dipoles of λ/2, λ and 1.5λ; plot the patterns and compute directivity.
3. **Link budgets (Part 3).** Plot received power against frequency for fixed-gain and fixed-area antennas over 100 m.
4. **Arrays (Part 4).** Plot array factors for 4, 8 and 16 elements at λ/2, steer to 30°, and space them at 0.8λ to see a grating lobe.
5. **ngspice (the chapter's guided exercise).** Predict the radiated share of the available power, then run `small_antenna.cir`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Crossing | All three terms equal at $kr$ = 1 ($r = \lambda/2\pi$) |
| 2 | Directivity | 1.64 for λ/2, 2.41 for λ; the 1.5λ dipole has its main lobes off broadside |
| 3 | Link | Fixed-gain received power falls 20 dB per decade of frequency; fixed-area power rises 20 dB per decade |
| 4 | Arrays | Beamwidths of about 26°, 13° and 6.4° for 4, 8 and 16 elements; a full-height grating lobe at 0.8λ when steered to 40° |
| ngspice | Small antenna | 24.0% of the available power radiated |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 13-11.a | directivity of a full-wave dipole | 2.411 | — |
| Lab 13-11.b | broadside beamwidth, 16 elements at λ/2 | 6.359 | ° |

*These are recomputed by [verify_13_11.py](../../verify/verify_13_11.py) by summing Hertzian elements along the full-wave dipole's current and by direct phasor summation for the array.*

## Discussion questions

1. Why is the reactive near field "reactive"?
2. Why does a full-wave dipole have more directivity than a half-wave one, and why does a 1.5λ dipole not continue the trend broadside?
3. Why does matching a small antenna not fix its efficiency?

### Answers

1. In the near field the electric and magnetic fields are nearly 90° out of phase with each other, so the Poynting vector averages to almost nothing: energy sloshes back and forth between the antenna and the space around it each cycle, like the energy in a capacitor or inductor, instead of flowing outward. The radiating part is the in-phase $1/r$ component that dominates beyond $r \approx \lambda/2\pi$.
2. A full-wave dipole's two half-wave current halves are in phase, so their fields add broadside while partly cancelling at other angles, narrowing the beam. On a 1.5λ dipole the current reverses direction along part of the wire; those out-of-phase segments cancel broadside and push the main lobes off to the side.
3. Matching makes the antenna accept all the power the source can deliver, but inside the antenna that power divides between the radiation resistance and the loss resistance in proportion to their values. With $R_{rad}$ = 0.3156 Ω and 1 Ω of loss, three quarters is dissipated whatever the match. Only a larger antenna (more $R_{rad}$) or lower loss raises efficiency.

## Optional hardware extension

With two Wi-Fi devices (or a phone and a Wi-Fi analyzer app) outdoors, measure received signal strength at distances of 1, 2, 4, 8 and 16 m in a clear line of sight. Plot it against log distance: free space predicts 6 dB less per doubling. Then repeat indoors and note how far the measurements depart from Friis.
