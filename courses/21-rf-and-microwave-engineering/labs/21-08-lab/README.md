# Lab 21-08 · Transceiver Architectures: Frequency Plans, I/Q Mismatch, Complex Filters and Direct RF Sampling

Chapter: [21-08 · Transceiver Architectures](../../chapters/21-08-transceiver-architectures.md)

## Objective

- Plan a superheterodyne receiver: find the image and the spurious responses, and size the preselector, confirming it in ngspice.
- Measure the EVM that I/Q mismatch causes in a zero-IF OFDM receiver and compare it with the IRR formula.
- Confirm a complex filter's asymmetric response in ngspice.
- Sample a jittered RF tone and compare its SNR with the jitter limit, and measure the processing gain of a digital downconverter.

## Background

`trx.py` holds the planning formulas (`image`, `butterworth_bp_atten_db`, `order_for_rejection`, `spurs`, `irr_db`, `nyquist_alias`, `jitter_snr_db`, `nsd_dbfs_hz`, `processing_gain_db`) and four simulations: `ofdm_iq_evm_db` (16-QAM OFDM through a receiver whose Q branch has gain and phase error), `jitter_snr_sim` (a sinusoid sampled at jittered instants), `ddc_snr` (a tone plus ADC noise sampled at 3 GS/s, mixed to DC by an NCO, filtered and decimated by 64) and `complex_filter_db`.

`preselect.cir` is the third-order Butterworth preselector of Examples 21-08.1 and 21-08.2 (2.45 GHz, 100 MHz), analysed at the image and both half-IF spurs. `complexfilter.cir` is a first-order complex filter centred at +1 MHz with a 0.5 MHz pole, driven once with a positive-frequency and once with a negative-frequency I/Q input.

## Procedure

1. **Frequency plan.** *Predict* the image and half-IF spurs of a 2.45 GHz receiver with a 2.75 GHz LO, and the preselector order for 60 dB at the image. Run the spur search and `ngspice -b preselect.cir` (Part 1).
2. **I/Q mismatch.** *Predict* the EVM for 1% gain and 1° phase error, then run `ofdm_iq_evm_db` and plot the received constellation (Part 2).
3. **Complex filter.** *Predict* the response at +1 MHz and −1 MHz, then run `ngspice -b complexfilter.cir` and plot $H(f)$ for orders 1 to 4 (Part 3).
4. **Jitter.** *Predict* the SNR of a 3.5 GHz tone sampled at 2949.12 MSPS with 50 fs of jitter, then simulate (Part 4).
5. **Digital downconversion.** *Predict* the in-band SNR after selecting a 20 MHz channel from a 3 GS/s stream with 60 dB full-band SNR, then run `ddc_snr` (Part 5).

## Expected results

- **Part 1.** Image 3.05 GHz, half-IF spurs 2.60 and 2.90 GHz; a third-order preselector gives 62.05, 27.87 and 55.15 dB, which ngspice reproduces.
- **Part 2.** The simulated EVM equals −IRR exactly, **−39.96** dB, because each subcarrier's error is its mirror subcarrier scaled by $\nu/\mu$.
- **Part 3.** 0 dB at +1 MHz and −12.30 dB at −1 MHz.
- **Part 4.** About **59.1** dB from the seeded simulation, against the 59.18 dB limit.
- **Part 5.** The tone aliases to 550 MHz. The ideal processing gain for a 20 MHz channel is 18.75 dB, but the windowed-sinc filter's equivalent noise bandwidth is only **16.98** MHz, which predicts **79.46** dB; the seeded simulation gives **79.7** dB, within the estimate's scatter.

## Discussion

1. **Why does the I/Q-mismatch EVM not depend on the modulation?** The leakage is a scaled copy of the mirror subcarrier; with equal average power on both sides of DC its power ratio is $\lvert\nu/\mu\rvert^2 = 1/\text{IRR}$ for any constellation.
2. **Why does the complex filter's response at −1 MHz not reach zero?** A first-order pole at +1 MHz only falls as $1/\lvert f - f_{IF}\rvert$; the image is just two pole bandwidths away. Higher order or a higher IF relative to the bandwidth helps.
3. **Why is digital processing gain not free?** It removes noise outside the channel, but only if the ADC's noise is white and the channel filter is sharp; spurs and blockers inside the channel are untouched.

## Optional hardware

A low-cost SDR (a zero-IF USB receiver) shows the impairments directly: tune to an empty channel and look for the DC spike and its notch; inject a single tone offset from the LO and measure the mirror image at the opposite offset to read the IRR; then enable and disable the driver's I/Q correction.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 21-08.a | simulated OFDM EVM from 1 % and 1° | −39.96 | dB |
| Lab 21-08.b | simulated jitter-limited SNR | 59.1 | dB |
| Lab 21-08.c | DDC filter equivalent noise bandwidth | 16.98 | MHz |
| Lab 21-08.d | predicted in-band SNR | 79.46 | dB |
| Lab 21-08.e | simulated in-band SNR | 79.7 | dB |
