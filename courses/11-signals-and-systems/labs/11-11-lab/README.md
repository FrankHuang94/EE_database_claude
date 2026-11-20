# Lab 11-11 · Modulation and Filtering Applications

Chapter: [11-11 Modulation and Filtering Applications](../../chapters/11-11-modulation-and-filtering-applications.md)

## Objective

Modulate and demodulate signals in simulation, see what carrier errors and detector time constants do, watch an image become inseparable after mixing, and compare classical filter families on one specification.

## Background

DSB-SC and coherent demodulation (§3.1–3.2), conventional AM and envelope detection (§3.3), mixers and images (§3.4), and filter families (§3.6).

## Files

- [11-11-modulation.ipynb](11-11-modulation.ipynb): the notebook (Parts 1–4).

## Procedure

1. **DSB-SC (Part 1).** Modulate a two-tone message onto a 100 kHz carrier, plot the spectrum, then demodulate with phase errors of 0°, 30° and 90° and with a 2 Hz frequency error.
2. **Envelope detection (Part 2, the chapter's guided exercise).** *Predict first:* for $m$ = 0.5 and a 5 kHz tone on a 1 MHz carrier, how does the detected tone's distortion change as $RC$ goes from 20 to 55 to 150 µs? Then simulate an ideal-diode RC detector and measure the second-harmonic level.
3. **Images (Part 3).** Mix a wanted station at 1000 kHz and an image at 1910 kHz with a 1455 kHz LO and show both land at 455 kHz.
4. **Filter families (Part 4).** Design Butterworth, Chebyshev I, elliptic and Bessel filters to Example 11-11.4's specification (Bessel at the elliptic's order for comparison) and compare magnitude, group delay and step response.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Demodulated amplitude | 1, 0.866, 0 for 0°, 30°, 90°; a 2 Hz beat with a frequency error |
| 2 | Distortion | Small below 55 µs, a sharp rise above it (diagonal clipping) |
| 3 | Mixer outputs | Station and image both at 455 kHz |
| 4 | Filters | Orders 17, 8, 5; elliptic sharpest; Bessel with the flattest delay and under 1% step overshoot |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 11-11.a | demodulated amplitude at 30° | 0.866 | — |
| Lab 11-11.b | image's IF after mixing | 455 | kHz |
| Lab 11-11.c | elliptic step overshoot | 15.1 | % |
| Lab 11-11.d | fifth-order Bessel step overshoot | 0.8 | % |

## Discussion questions

1. Why does the DSB-SC output with a 90° phase error vanish, while conventional AM's envelope detector does not care about the carrier's phase?
2. In Part 3, what would an image-reject mixer (which uses two LOs 90° apart) do differently?
3. Why does the elliptic filter's step response ring while the Bessel's does not?

### Answers

1. Coherent demodulation multiplies by the local carrier and averages; at 90° the product averages to zero ($\cos 90° = 0$). The envelope detector measures the magnitude of the signal, whatever its phase.
2. It forms the signal's in-phase and quadrature products and combines them so that the wanted band adds and the image cancels: the analog version of separating positive and negative frequencies with complex signals (Course 17).
3. Its poles sit close to the $j\omega$ axis (high-Q sections), and poles near the axis ring (11-08 §3.7); the Bessel's poles are well damped, chosen for flat group delay.

## Optional hardware extension

With a software-defined radio receiver (or an AM radio and a signal generator), tune near a known AM station and look for its image $2f_{IF}$ away; measure how much weaker it is than the direct reception, and compare with a tuned-circuit estimate.
