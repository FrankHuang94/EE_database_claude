# Lab 17-05 · Matched Filters and Decisions

Chapter: [17-05 · Matched Filters and Optimal Detection](../../chapters/17-05-matched-filters-and-detection.md)

## Objective

Check the chapter's optimum-receiver results by simulation:

- the matched filter's peak SNR $2E/N_0$, for pulses of different shapes and equal energy;
- the loss of a simple one-pole filter and its optimum time constant;
- Gram–Schmidt on sampled waveforms;
- error rates of antipodal, orthogonal, on-off and PAM4 signalling against their formulas and bounds;
- pulse compression of a linear chirp.

## Background

White noise of two-sided PSD $N_0/2$, simulated on a grid of spacing $\Delta t$, has sample variance $N_0/(2\Delta t)$, so that integrals $\int n\phi\,dt \approx \sum n\phi\,\Delta t$ have variance $N_0/2$ for unit-energy $\phi$ (§3.3). With this calibration, a correlator's output SNR can be compared directly with $2E/N_0$, and signal-space points can be simulated with independent Gaussian noise of variance $N_0/2$ per dimension.

## Files

- `detection.py`: `white_noise`, `energy`, `inner`, `matched_filter_output`, `correlate`, `mf_peak_snr_mc`, `one_pole_ratio`, `gram_schmidt`, `coordinates`, `ml_decide`, `map_decide`, `simulate_ser`, `pe_pair`, `ber_bpsk`, `ber_orthogonal`, `ser_pam`, `union_bound`, `nearest_neighbour`, `chirp`, `compress`, `mainlobe_width`.
- `17-05-detection-lab.ipynb`: the guided notebook.

## Procedure

1. **The matched filter's SNR.** For a 1 µs rectangular pulse with $N_0 = 2 \times 10^{-8}$ V²/Hz, predict $2E/N_0$. Measure the correlator's output SNR for the rectangle, a half-sine and a chirp scaled to the same energy.
2. **Mismatch.** Predict the SNR of a one-pole filter relative to the matched filter for $T/\tau$ from 0.2 to 5, then sweep it and locate the optimum.
3. **Signal space.** Run `gram_schmidt` on Example 17-05.3's signals and on four random waveforms of 3 samples each; predict the dimension first.
4. **Error rates.** Predict, then simulate, the BER of antipodal, orthogonal and on-off signalling from 0 to 10 dB, and the PAM4 symbol-error rate with its formula and nearest-neighbour approximation.
5. **Pulse compression.** For a 10 µs chirp sweeping 10 MHz, predict the compression ratio and main-lobe width; add noise to a delayed echo and compress it.

## Expected results

- Part 1: about 100 (20 dB) for all three pulses, within Monte Carlo scatter.
- Part 2: a maximum of 0.815 (−0.89 dB) at $T/\tau$ ≈ 1.256.
- Part 3: two dimensions for Example 17-05.3; three for random 3-sample waveforms.
- Part 4: simulations on the formulas; orthogonal and on-off 3 dB to the right of antipodal.
- Part 5: compression ratio $TB$ = 100 and a main lobe about 0.1 µs wide; the echo stands out clearly although it is buried in noise before compression.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 17-05.a | predicted 2E/N0, rectangular pulse | 100 | — |
| Lab 17-05.b | optimum T/τ for the one-pole filter | 1.2564 | — |
| Lab 17-05.c | compression ratio, 10 µs × 10 MHz | 100 | — |

## Discussion

1. Why did the half-sine and the chirp give the same SNR as the rectangle, although they look nothing alike?
2. Why is the one-pole filter's loss so small near its optimum?
3. In Part 5, what limits how close two echoes can be and still be separated, and what limits how weak an echo can be and still be detected?

### Answers

1. The matched filter's peak SNR depends only on the energy, $2E/N_0$ (§3.2); shapes differ in their autocorrelation width and spectrum, not detectability.
2. Near the optimum the filter's impulse response overlaps most of the pulse while rejecting most of the noise outside the pulse's band; SNR is a smooth function of τ with a broad maximum, so small mismatches cost little (Example 17-05.2).
3. Separation is set by the main-lobe width, about $1/B$; detectability by the echo's energy over $N_0$, which grows with the chirp duration.

## Optional hardware

With a two-channel oscilloscope that can record waveforms, transmit a pseudo-random burst through a cable or acoustic path, record the received signal and correlate it with the transmitted burst on a computer: the correlation peak locates the delay even when the burst is invisible in the raw trace.
