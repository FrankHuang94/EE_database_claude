# Lab 16-05 · Windows, Noise Floors and an ADC Test

Chapter: [16-05 Spectral Analysis and Windowing](../../chapters/16-05-spectral-analysis-and-windowing.md)

## Objective

Measure what windows do, see processing gain move the noise floor without changing the SNR, tame the scatter of noise spectra by averaging, and run a complete FFT test of a simulated ADC, including what happens when the test is not coherent.

## Background

Read §3 of the chapter. `spectral.py` builds the windows of §3.2 from their cosine coefficients (checked against `scipy.signal.windows`) and computes their figures of merit from the definitions. `adc_metrics` analyses a coherent record with a rectangular window; `adc_metrics_window` analyses any record with a window, collecting the power within a guard band around the fundamental and its harmonics; `sine_fit3` gives SINAD in the time domain.

## Files

- [spectral.py](spectral.py): `window`, `coherent_gain`, `enbw_bins`, `scalloping_db`, `highest_sidelobe_db`, `periodogram`, `welch`, `coherent_bin`, `adc_metrics`, `adc_metrics_window`, `sine_fit3`.
- [16-05-spectral-lab.ipynb](16-05-spectral-lab.ipynb): the notebook (Parts 1–5).

## Procedure

1. **Compare windows (Part 1).** Plot the six windows' spectra in dB (zero-padded to show the sidelobes) and reproduce the table of §3.2.
2. **Hunt a weak tone (Part 2).** Reproduce Example 16-05.3, then lower the weak tone until each window loses it.
3. **Processing gain (Part 3).** Quantize a coherent full-scale sine to 12 bits for $N$ = 1024 to 65,536 and plot the average floor depth and the SNR against $N$. *Predict first:* the slope of each.
4. **Average a noise spectrum (Part 4).** For white noise, compare one periodogram with Welch averages of 4, 16 and 64 segments and measure the scatter.
5. **Test an ADC (Part 5).** Run Example 16-05.5's test coherently, then move the input to 1637.3 cycles per record and analyse it naively (rectangular window, fundamental in one bin), with guard bands, with Hann and with Blackman–Harris.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Window table | as in §3.2 (Hann ENBW 1.500 bins, −31.5 dB sidelobes; Blackman–Harris −92 dB) |
| 2 | Weak tone | rectangular loses a −60 dB tone 9.5 bins away; Hann just keeps it; Blackman–Harris keeps it with a wide margin |
| 3 | Processing gain | floor depth rises 3 dB per doubling of $N$ (theory 119.2 dB at 65,536 points; the simulation lands within 0.3 dB); SNR stays near 74 dB |
| 4 | Averaging | scatter about 1, 0.5, 0.25 and 0.13 of the mean |
| 5 | ADC test | coherent: SINAD 67.85 dB, ENOB 10.98; non-coherent with a naive rectangular analysis: SINAD 4.47 dB; with Hann 49.8 dB; with Blackman–Harris 67.82 dB, within 0.04 dB of the coherent result |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 16-05.a | floor depth, ideal 12-bit, 65,536 points | 119.2 | dB |
| Lab 16-05.b | non-coherent SINAD, naive rectangular analysis | 4.47 | dB |
| Lab 16-05.c | non-coherent SINAD, Hann | 49.8 | dB |
| Lab 16-05.d | non-coherent SINAD, Blackman–Harris | 67.82 | dB |

## Discussion

1. In Part 3, why does the SNR not improve with $N$ when the floor plainly drops?
2. In Part 4, why does averaging help while a longer single record does not?
3. In Part 5, why does the naive analysis of the non-coherent record report an ENOB below 1 bit?
4. In Part 5, why does Hann recover only part of the SINAD while Blackman–Harris recovers nearly all of it?

### Answers

1. The total noise power is fixed by the converter; a longer record spreads it over more bins, so each bin holds less, while the tone stays in one bin. SNR integrates all the bins, so it does not change.
2. A periodogram bin is an exponential random variable whose scatter equals its mean whatever the record length; a longer record only makes more such bins. Averaging independent estimates of the same bin reduces the scatter as $1/\sqrt K$.
3. With the tone 0.3 bin off-centre, the rectangular window's leakage spreads most of the tone's energy far outside bin 1637; the naive analysis counts all of that as noise, so the "noise" is almost as large as the signal.
4. The analysis treats everything outside the guard bands as noise. Hann's leakage falls only at 18 dB per octave, so at the hundreds of bins that make up the noise region it still adds noise-like power above the converter's floor. Blackman–Harris's sidelobes are below −92 dB and keep falling, under the 12-bit floor everywhere, so only the converter's own noise remains.

## Optional hardware

With any sound card and a signal generator (or a phone app generating a pure tone), record a tone at 48 kHz, compute SNR, THD and SINAD with `adc_metrics_window` and a Blackman–Harris window, and compare with the card's specifications. Repeat at several levels to see where noise and distortion dominate.
