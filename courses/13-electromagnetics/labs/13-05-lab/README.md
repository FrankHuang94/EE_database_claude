# Lab 13-05 · Plane Waves in Lossless and Lossy Media

Chapter: [13-05 Plane Waves in Lossless and Lossy Media](../../chapters/13-05-plane-waves.md)

## Objective

See how $\vec{E}$ and $\vec{H}$ move together in lossless and lossy media; classify polarizations by tracing the field; find where the good-conductor and low-loss approximations fail for seawater; and compute the exact skin effect in a round wire. Then build the skin effect as an R–L ladder in ngspice and measure a copper surface's impedance.

## Background

Uniform plane waves (§3.1), polarization (§3.2), lossy media (§3.3) and the skin effect (§3.4).

## Files

- [13-05-plane-waves.ipynb](13-05-plane-waves.ipynb): the notebook (Parts 1–4).
- [skin_ladder.cir](skin_ladder.cir): 240 layers of copper, each δ/20 thick, as a ladder of series inductors and shunt resistors, driven by 1 A at 1 GHz. Run with `ngspice -b skin_ladder.cir`, or `python tools/run_spice.py 13-05` from the repository root.

## Procedure

1. **Snapshots (Part 1).** Plot $E_x$ and $\eta H_y$ along $z$ for a lossless wave and for a lossy one with α = β/5. *Predict first:* which way is $H$ shifted?
2. **Polarization (Part 2).** Trace $\hat{x} + \hat{y}$, $\hat{x} - j\hat{y}$, $\hat{x} + j\hat{y}$ and $\hat{x} + 2j\hat{y}$, and read the hand and axial ratio.
3. **Seawater (Part 3).** Plot α from 1 kHz to 100 GHz exactly and with both approximations, and find where the good-conductor value is 10% high.
4. **A round wire (Part 4).** Plot the current distribution in a 1 mm copper wire at several frequencies and the exact $R_{ac}/R_{dc}$ against the approximations; find where the resistance doubles.
5. **ngspice (the chapter's guided exercise).** Predict the ladder's input impedance at 1 GHz, then run `skin_ladder.cir`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Phase of $H$ | In phase with $E$ when lossless; lagging (by 11.3° here) when lossy |
| 2 | Polarization | Linear; right-hand circular; left-hand circular; left-hand elliptical with axial ratio 2 |
| 3 | Seawater | Good-conductor formula fine at low frequency, 10% high at about 170 MHz, far off above 1 GHz |
| 4 | Round wire | Current crowding toward the surface as frequency rises; ratio approaching $a/2\delta + 1/4$ |
| ngspice | Surface impedance | Real and imaginary parts both 8.25 mΩ, within 0.1% |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 13-05.a | exact R_ac/R_dc of a 1 mm copper wire at 1 MHz | 4.045 | — |
| Lab 13-05.b | frequency at which its resistance doubles | 208.0 | kHz |
| Lab 13-05.c | frequency at which the good-conductor α for seawater is 10% high (α_gc/α = 1.10) | 170.2 | MHz |

*These are recomputed by [verify_13_05.py](../../verify/verify_13_05.py) with the exact Bessel-function impedance and the exact propagation constant, solved by root finding.*

## Discussion questions

1. Why does the ladder of inductors and resistors reproduce a copper surface's impedance?
2. Why is the ratio $R_{ac}/R_{dc}$ closer to $a/2\delta + 1/4$ than to $a/2\delta$?
3. Why does the good-conductor approximation fail for seawater at microwave frequencies even though seawater conducts?

### Answers

1. Inside the metal, Faraday's law gives $dE/dz = -j\omega\mu_0H$ and Ampère's law (with the displacement current negligible) gives $dH/dz = -\sigma E$. These have exactly the form of a transmission line's equations with series inductance $\mu_0$ and shunt conductance σ per unit depth, so slicing the depth into thin layers gives a ladder of $\mu_0h$ inductors and $1/(\sigma h)$ resistors. Its input impedance is $\sqrt{j\omega\mu_0/\sigma} = (1 + j)R_s$, the surface impedance; circuit simulators use the same idea to model skin effect.
2. The thin-skin estimate treats the current as flowing in a flat sheet of thickness δ at the full radius $a$. In a round wire the sheet curves, and its current sits at radii slightly less than $a$, a smaller circumference; the first correction raises the resistance by a constant, 1/4 of $R_{dc}$, independent of frequency.
3. The approximation needs $\sigma/\omega\varepsilon \gg 1$. Seawater's high permittivity ($\varepsilon_r$ ≈ 81) makes its displacement current large, and at 1 GHz the ratio is only 0.888: the water behaves as much like a lossy dielectric as a conductor, and the exact formula must be used.

## Optional hardware extension

Measure the resistance of a 1 m length of thick copper wire (or a short busbar) with a four-wire meter, then measure its impedance with an LCR meter at 100 Hz, 10 kHz and 100 kHz (subtracting the fixture's reactance). Compare the rise in resistance with Part 4's Bessel curve for the measured radius.
