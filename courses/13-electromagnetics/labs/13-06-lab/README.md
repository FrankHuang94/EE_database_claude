# Lab 13-06 · Reflection and Transmission of Waves

Chapter: [13-06 Reflection and Transmission of Waves](../../chapters/13-06-reflection-and-transmission.md)

## Objective

Compute standing waves, Fresnel reflectances, coated and layered structures, and shielding exactly, and compare them with the chapter's formulas and approximations. Then model a dielectric boundary as a junction of transmission lines in ngspice.

## Background

Normal incidence (§3.1), layers (§3.2), Snell and Fresnel (§3.3–3.4), total internal reflection and Brewster (§3.5–3.6), and shielding (§3.7).

## Files

- [13-06-reflection.ipynb](13-06-reflection.ipynb): the notebook (Parts 1–4).
- [interface_line.cir](interface_line.cir): a 376.7 Ω line joined to a 251.2 Ω line (air to glass) with a 1 V incident step. Run with `ngspice -b interface_line.cir`, or `python tools/run_spice.py 13-06` from the repository root.

## Procedure

1. **Standing waves (Part 1).** Plot the field envelope in front of glass, an $\varepsilon_r$ = 4 dielectric, water and a perfect conductor. *Predict first:* where is each minimum?
2. **Fresnel (Part 2).** Plot TE and TM reflectance against angle from air into glass and from glass into air; read the Brewster and critical angles.
3. **Layers (Part 3).** Plot the reflectance of bare and MgF₂-coated glass across the visible band, and of a half-wave radome from 6 to 14 GHz; find the radome's 1% bandwidth.
4. **Shielding (Part 4).** Compute a 35 µm copper foil's exact shielding effectiveness from 100 kHz to 10 GHz and compare with the A + R estimate.
5. **ngspice (the chapter's guided exercise).** Predict the transmitted and reflected steps, then run `interface_line.cir`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Standing waves | Minima at the boundary for all four (Γ < 0); S of 1.5, 2, 9 and infinity |
| 2 | Angles | Brewster 56.31° (air to glass) and 33.69° (glass to air); critical 41.81° |
| 3 | Coating, radome | Coated reflectance near 1.4% at 550 nm, rising toward the band edges; radome below 1% only near 10 GHz |
| 4 | Shielding | Exact and A + R agree when the foil is several skin depths thick; they differ by up to about 1 dB at 1–10 MHz, and A + R overstates the shielding by about 8 dB at 100 kHz, where the foil is thinner than a skin depth |
| ngspice | Steps | 0.8 V transmitted, −0.2 V reflected |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 13-06.a | exact shielding effectiveness of 35 µm copper at 10 MHz | 113.0 | dB |
| Lab 13-06.b | exact shielding effectiveness of 35 µm copper at 100 MHz | 134.1 | dB |
| Lab 13-06.c | half-wave radome bandwidth for reflectance below 1% | 8.557 | % |

*These are recomputed by [verify_13_06.py](../../verify/verify_13_06.py) with its own transfer-matrix code and root finding.*

## Discussion questions

1. Why do a dielectric boundary and a junction of two transmission lines obey the same reflection formula?
2. Why is the radome's transparency band so narrow, and how could it be widened?
3. Why does the A + R estimate fail for a foil thinner than a skin depth?

### Answers

1. Both are problems of a wave in which one field (E or V) divided by the other (H or I) is fixed by the medium (η or $Z_0$), meeting a boundary where both must be continuous. The same two equations give $\Gamma = (Z_2 - Z_1)/(Z_2 + Z_1)$ in each case; Maxwell's equations for a TEM line reduce to the telegrapher's equations, which have the same form as those for a plane wave (13-07).
2. Transparency relies on the reflections from the two faces cancelling, which needs the round trip through the slab to be exactly one wavelength; off the design frequency the cancellation is incomplete, and with a large impedance step (here 2:1) the residual grows quickly. Lower-permittivity materials (a smaller step), or sandwich structures with several layers, broaden the band.
3. The estimate counts one pass through the metal and treats the reflections at the two faces separately. When the foil is thin, the wave reflected from the back face returns to the front with little attenuation and interferes with the forward wave; this multiple-reflection term reduces the shielding, slightly at a few skin depths and by several decibels when the foil is thinner than a skin depth, as Part 4 shows. In the thin-sheet limit ($t \ll \delta$) the exact value tends to $20\log_{10}(1 + \eta_0\sigma t/2)$, independent of frequency, while the A + R estimate keeps rising as the frequency falls.

## Optional hardware extension

With two small 2.4 GHz modules (or a phone and a Wi-Fi analyzer app), measure the received signal strength through an open doorway, through a window and through a closed metal-framed cabinet door. Then cover a cardboard box with aluminium foil and test with and without a slot cut in one face; turn the slot to see how its orientation relative to the antenna changes the leakage.
