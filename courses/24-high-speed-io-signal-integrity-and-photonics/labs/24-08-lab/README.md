# Lab 24-08 · Coupling, Grating Couplers, Bond Parasitics and Retiming

**Objective.** Compute fiber-to-chip coupling by numerical overlap and compare it with the closed form; plot a grating coupler's spectrum and find its 1-dB bandwidth; confirm in ngspice how a wire bond and a hybrid bond shape a ring modulator's drive; and compare how errors accumulate in retimed and linear links.

**Chapter:** [24-08 · Silicon Photonics and Optical Transceivers](../../chapters/24-08-silicon-photonics.md)

## Background

§3.3 derived the coupling between Gaussian modes, $\eta = (2w_1w_2/(w_1^2 + w_2^2))^2$, with lateral-offset and tilt factors. §3.4 derived the grating coupler's period $\lambda/(n_{eff} - \sin\theta)$ and its steering with wavelength. §3.5 modelled the driver, bond and modulator as a series RLC with $f_0 = 1/2\pi\sqrt{LC}$ and $\zeta = (R/2)\sqrt{C/L}$. §3.8 showed that retimed links add BER while linear links add $1/Q^2$.

## Files

- `bond.cir`: Example 24-08.6, a 50 Ω driver into a 20 fF ring through a 1 nH wire bond and through a 10 pH hybrid bond.
- `siph.py`: cutoff wavelengths, waveguide conditions, Gaussian coupling (closed form and numerical), grating-coupler period and spectrum, transmitter budgets, the RLC response, retimed and linear error accumulation, and yield.
- `24-08-siph-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Coupling** (notebook). *Predict* the coupling between a 4.6 µm fiber mode and a 1.5 µm chip mode. Compute the overlap integral numerically on a grid and compare with the closed form; then sweep the lateral offset for matched modes of 1.5, 3.0 and 4.6 µm.

**Part 2 · Grating coupler** (notebook). For Example 24-08.4's grating ($n_{eff}$ = 2.8, 10°, 1310 nm, fiber $w$ = 4.6 µm), *predict* the 1-dB bandwidth, then compute the spectrum with the exact arcsine steering and read off the band.

**Part 3 · Bond parasitics** (ngspice and notebook). *Predict* the wire bond's peaking and both bandwidths, run `ngspice -b bond.cir`, and plot both responses against the 56.7 GHz Nyquist frequency of 113.4375 GBd.

**Part 4 · Retimed against linear** (notebook). For chains of one to four segments each good for 10⁻¹² alone, *predict* the end-to-end BER with and without retiming, then compute both.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 24-08.a | numerical overlap, 4.6 and 1.5 um | 0.348 | |
| Lab 24-08.b | 1-dB band lower edge | 1288.7 | nm |
| Lab 24-08.b1 | 1-dB band upper edge | 1331.4 | nm |
| Lab 24-08.b2 | 1-dB bandwidth | 42.7 | nm |
| Lab 24-08.c | wire-bond peaking | 13.1 | dB |
| Lab 24-08.d | wire-bond bandwidth | 54.8 | GHz |
| Lab 24-08.e | hybrid-bond bandwidth | 196 | GHz |
| Lab 24-08.f | linear BER, 2 segments | 3.3e-7 | |
| Lab 24-08.g | linear BER, 3 segments | 2.4e-5 | |
| Lab 24-08.h | linear BER, 4 segments | 2.2e-4 | |
| Lab 24-08.i | wavelength shift per degree of tilt | 8.6 | nm/° |
| Lab 24-08.j | Q per segment, 4 linear segments | 14.1 | |
| Lab 24-08.k | extra SNR per segment, 4 linear segments | 6 | dB |

- Part 1: the grid overlap reproduces the closed form, 0.348, to many digits; the offset for a 0.5 dB loss scales with the mode size.
- Part 2: with the exact arcsine the 1-dB band runs from 1288.7 to 1331.4 nm, 42.7 nm wide and slightly lopsided about 1310 nm, matching the linearized estimate of 43 nm.
- Part 3: ngspice gives 13.1 dB of peaking near 35 GHz and a 54.8 GHz bandwidth through the wire bond, and 196 GHz through the hybrid bond.
- Part 4: retiming keeps the BER at $n \times 10^{-12}$; the linear chain degrades to 3.3 × 10⁻⁷, 2.4 × 10⁻⁵ and 2.2 × 10⁻⁴ for two, three and four segments. Four linear segments sit just inside the KP4 FEC threshold (2.4 × 10⁻⁴), with no margin left.

## Discussion

1. Why does the closed-form coupling match the grid overlap so closely, and when would it not?

   <details><summary>Answer</summary>

   Both integrate the same Gaussian fields; the grid only approximates the integral, and a fine, wide grid captures it almost exactly. Real waveguide modes are not Gaussian (a silicon wire's mode has evanescent tails and is not circular), so a real coupler's efficiency must come from a mode solver's fields in the same overlap integral.

   </details>

2. Inductance in series with a capacitor raised the hybrid bond's bandwidth above the bare RC value. Why not use more inductance?

   <details><summary>Answer</summary>

   A little inductance (damping ratio near 0.7 to 1) speeds the response without peaking: the inductive-peaking trick. More inductance lowers the resonance into the signal band and reduces damping, giving peaking and ringing, as the wire bond shows. Designers who use inductive peaking choose the inductance deliberately; a wire bond's is an accident of geometry.

   </details>

3. If each segment of a four-segment linear chain must reach 10⁻¹² end to end, what $Q$ must each have?

   <details><summary>Answer</summary>

   $7.03\sqrt 4 = 14.1$, twice the retimed requirement, or 6 dB more electrical SNR per segment.

   </details>

## Optional hardware

A silicon-photonics evaluation kit or a multi-project-wafer chip with grating couplers, a tunable laser and a power meter reproduces Part 2: sweep the wavelength and record the fiber-to-chip transmission. Tilting the fiber holder shifts the peak wavelength by about 1/0.117 ≈ 8.6 nm per degree, the inverse of Example 24-08.4's steering.
