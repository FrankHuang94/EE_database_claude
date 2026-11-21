# Lab 17-11 · Diversity, Beams and Spatial Streams

Chapter: [17-11 · MIMO and Beamforming Basics](../../chapters/17-11-mimo-and-beamforming.md)

## Objective

Separate the three things multiple antennas do (array gain, diversity, multiplexing) by simulating each:

- receive combining (selection, equal-gain, maximal-ratio) over Rayleigh fading;
- Alamouti transmit diversity against receive MRC;
- beam patterns of uniform linear arrays, steering and grating lobes;
- ergodic MIMO capacity and its growth with the number of antennas;
- zero-forcing and MMSE detection of spatially multiplexed streams;
- channel hardening with many antennas.

## Background

MRC weights each branch by the conjugate of its gain, giving SNR $\|\mathbf h\|^2E_s/N_0$ (§3.1). Alamouti's code gives diversity 2 from two transmit antennas without channel knowledge, at 3 dB below MRC (§3.2). A ULA's array factor is $|\sin(N\psi/2)/(N\sin(\psi/2))|$ (§3.3). The SVD turns a MIMO channel into parallel eigenmodes, so capacity is $\sum\log_2(1 + \rho\sigma_i^2/N_t)$ (§3.4). ZF removes interference at the cost of noise enhancement; MMSE balances the two (§3.5).

## Files

- `mimo.py`: `crandn`, `combine_snr`, `sc_mean_gain`, `mrc_outage`, `sc_outage`, `ber_bpsk_mrc`, `simulate_combining`, `alamouti_encode`, `alamouti_decode`, `simulate_alamouti`, `steering`, `array_factor`, `hpbw_deg`, `first_null_deg`, `grating_free_spacing`, `capacity_equal_power`, `capacity_svd`, `waterfill`, `capacity_waterfill`, `ergodic_capacity_mc`, `ergodic_siso`, `ergodic_2x2`, `zf_sinr`, `mmse_sinr`, `simulate_spatial_mux`, `nr_max_rate_mbps`.
- `17-11-mimo-lab.ipynb`: the guided notebook.

## Procedure

1. **Combining.** Predict the BER of BPSK at 10 dB per-branch SNR with 1, 2 and 4 branches for SC, EGC and MRC; simulate.
2. **Alamouti.** Predict the BER of 2×1 Alamouti and 1×2 MRC at 10 dB; simulate both and compare their slopes from 0 to 20 dB.
3. **Beams.** Plot the array factor of 8 elements at $d = \lambda/2$, broadside and steered to 30°. Then set $d = \lambda$ and steer to 30°: predict where the grating lobe appears.
4. **Capacity scaling.** Predict, then compute by Monte Carlo, the ergodic capacity of $N \times N$ channels at 20 dB for $N$ = 1, 2, 4, 8.
5. **Linear receivers.** Simulate 2×2 QPSK spatial multiplexing with ZF and MMSE from 0 to 30 dB; then use 3 receive antennas and compare the slopes.
6. **Channel hardening.** Measure the standard deviation of $\|\mathbf h\|^2/M$ for $M$ = 1, 4, 64 and 256.

## Expected results

- Part 1: at 10 dB, MRC gives $2.3 \times 10^{-2}$, $1.6 \times 10^{-3}$ and $9.7 \times 10^{-6}$ for 1, 2 and 4 branches; SC and EGC lie above MRC (SC by about a factor of 2 with two branches).
- Part 2: Alamouti about $5.5 \times 10^{-3}$ at 10 dB against MRC's $1.6 \times 10^{-3}$: the same slope, 3 dB apart.
- Part 3: a beam of about 12.8° at broadside; with one-wavelength spacing steered to 30°, a grating lobe at −30°.
- Part 4: about 5.9, 11.3, 22.1 and 44.0 b/s/Hz: nearly linear in $N$.
- Part 5: ZF's 2×2 error rate falls only one decade per 10 dB (diversity 1); with three receive antennas it falls two decades per 10 dB. MMSE is slightly better than ZF.
- Part 6: about 1, 0.5, 0.125 and 0.0625.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 17-11.a | MRC BER, 2 branches, 10 dB | 1.60e-3 | — |
| Lab 17-11.b | Alamouti BER, 10 dB | 5.53e-3 | — |
| Lab 17-11.c | grating-lobe angle, d = λ, steered to 30° | −30 | ° |
| Lab 17-11.d | 8×8 ergodic capacity at 20 dB | 44.0 | b/s/Hz |
| Lab 17-11.e | hardening spread, M = 256 | 0.0625 | — |

## Discussion

1. Why does EGC come so close to MRC with only phase information?
2. In Part 5, why does adding one receive antenna help ZF so much more than adding one dB?
3. Why do arrays use half-wavelength spacing, and when might a designer accept larger spacing?

## Answers

1. Most of MRC's benefit comes from co-phasing (coherent addition); weighting by amplitude matters only when branches differ greatly, which in Rayleigh fading happens rarely enough that EGC loses well under 1 dB on average.
2. ZF uses all its degrees of freedom to null the other stream; a third antenna leaves one degree of freedom for diversity, changing the slope of the error curve, while an extra decibel only shifts the curve.
3. Spacing of λ/2 or less keeps grating lobes out of visible space at any scan angle. A fixed-beam or narrow-scan array (for example a backhaul dish replacement) can use wider spacing to get a narrower beam from fewer elements, accepting grating lobes outside its scan range.

## Optional hardware

Two software-defined radios with two receive channels each show MRC and selection combining directly: transmit a tone, move the receiver around a room, record both channels' envelopes, and compare the fading of each branch with the fading after co-phased combining.
