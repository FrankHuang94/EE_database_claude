# Lab 16-06 · Designing FIR Filters Four Ways

Chapter: [16-06 FIR Filter Design](../../chapters/16-06-fir-filter-design.md)

## Objective

Design low-pass FIR filters by truncation, with fixed and Kaiser windows, by frequency sampling and by the Parks–McClellan algorithm; check every design against its specification; and see the delay, the attenuation and the cost of a linear-phase filter in an actual filtered signal.

## Background

Read §3 of the chapter. `firdesign.py` builds everything from definitions: the ideal impulse response, symmetric windows (Kaiser's from a power series for $I_0$), Kaiser's design formulas, the amplitude response $A(\omega)$ of all four linear-phase types, a mask checker that evaluates each band on 20,000 points, the frequency-sampling formula of §3.6, and order estimates. The equiripple designs call SciPy's `remez` with a dense grid; `alternations` then counts the weighted error's alternating extrema to confirm the alternation theorem. The verify script cross-checks the window and Kaiser designs against `scipy.signal.firwin` and every response against `scipy.signal.freqz`.

## Files

- [firdesign.py](firdesign.py): `deltas`, `ideal_lowpass`, `i0`, `window`, `window_lowpass`, `kaiser_beta`, `kaiser_order`, `fir_type`, `amplitude`, `measure`, `freq_sampling_lowpass`, `remez_lowpass`, `min_taps`, `order_kaiser_pm`, `length_bellanger`, `alternations`.
- [16-06-fir-design-lab.ipynb](16-06-fir-design-lab.ipynb): the notebook (Parts 1–6).

## Procedure

1. **Types and zeros (Part 1).** Plot $A(\omega)$ for one filter of each type and their zeros in the z-plane; confirm the forced zeros of §3.2 and the reciprocal pairs.
2. **Gibbs (Part 2).** Truncate the ideal half-band filter at $M$ = 20, 50, 100 and 400 and tabulate the overshoot and its distance from the cutoff. *Predict first:* how the overshoot changes from $M$ = 20 to 400.
3. **The window table (Part 3).** Rebuild the table of §3.4 for $M$ = 50, 100 and 200 and for several cutoffs.
4. **Kaiser (Part 4).** Design Example 16-06.3; then the 70 dB design of Problem 16-06.6, repairing it first by adding taps at the same $\beta$ and then by re-running the formulas with 1 dB of margin.
5. **Frequency sampling (Part 5).** Sweep the transition sample of Example 16-06.4 from 0 to 1 and plot the stopband peak.
6. **Equiripple and a real signal (Part 6).** Find the shortest equiripple filter for the running example, count its alternations, and filter (i) a 3 kHz + 6 kHz two-tone signal and (ii) a Gaussian-windowed 2 kHz burst. Measure the tones' gains from the steady-state output and the delay from the burst's envelope.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Types | type II has $A(\pi) = 0$; type III has zeros at $\pm1$; zeros of every type come in reciprocal pairs |
| 2 | Gibbs | overshoot 9.12%, 8.97%, 8.96% and 8.95% for $M$ = 20, 50, 100, 400, peaking ever closer to the cutoff |
| 3 | Window table | errors within a few tenths of a dB of §3.4 at every $M$, except Hamming's, which wanders by 1 to 2 dB with $M$ and the cutoff |
| 4 | Kaiser | Example 16-06.3: 60.21 dB at $M$ = 174. At 70 dB: 69.93 dB at $M$ = 173; 192 taps at the same $\beta$, or 176 after redesign |
| 5 | Frequency sampling | stopband peak −20.5 dB at $T = 0$, best −42.5 dB at $T \approx 0.393$ |
| 6 | Equiripple | 137 taps, 70 alternations; 3 kHz passes at −0.048 dB, 6 kHz is attenuated by 74.09 dB; the burst emerges 68 samples (1.417 ms) late, undistorted |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 16-06.a | overshoot, half-band, M = 400 | 8.95 | % |
| Lab 16-06.b | overshoot, half-band, M = 50 | 8.97 | % |
| Lab 16-06.c | gain at 3 kHz, 137-tap equiripple | −0.048 | dB |
| Lab 16-06.d | attenuation at 6 kHz | 74.09 | dB |
| Lab 16-06.e | burst delay | 68 | samples |

## Discussion

1. In Part 2, why does the overshoot not fall as the filter lengthens, while the ringing gets narrower?
2. In Part 4, why does adding taps at a fixed $\beta$ barely change the attenuation?
3. In Part 6, the 6 kHz tone is attenuated by 74 dB, not 60 dB. Is the filter over-designed?
4. In Part 6, why does the burst come out with its shape intact, only delayed?

### Answers

1. The overshoot is the first maximum of the running integral of the window's spectrum, $\tfrac12 + \text{Si}(\pi)/\pi$ for the rectangular window, and the shape of that spectrum does not depend on $M$; only its width does, scaling as $1/M$. So the ripple pattern compresses toward the cutoff without changing height (§3.3).
2. Once $M$ is long enough for the transition band to fit between the edges, the stopband error of a window design is set by the window's sidelobe structure, a property of its shape ($\beta$): $M$ then only scales the frequency axis, narrowing the transition without changing the sidelobe heights (§3.4, §3.5). Below that length the transition spills past the stopband edge and the attenuation there falls quickly (1.4 dB for one tap fewer in Example 16-06.3).
3. No. 60 dB is the *worst* attenuation anywhere above 5 kHz; an equiripple stopband touches −60 dB only at its ripple peaks, and 6 kHz happens to fall near a null between peaks. A tone at an unlucky frequency would see 60.36 dB.
4. The filter is linear phase: every frequency in the burst's band is delayed by exactly 68 samples, and the passband gain is flat to within ±0.05 dB, so the output is the input shifted by 68 samples and scaled by a passband gain within 0.05 dB of 1.

## Optional hardware

On any microcontroller with a hardware multiplier (or a laptop's sound card through Python), run the 137-tap filter in real time at 48 kHz using the folded form of §3.8. Measure the processor load, then try the 175-tap Kaiser filter and compare. Feed a tone sweep from a signal generator or phone app and observe the stopband on the output.
