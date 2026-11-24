# Lab 21-12 · The Modem in Numbers: Peak Rates, Ranging and Satellites

Chapter: [21-12 · Modem Baseband Architecture and Wireless Standards](../../chapters/21-12-modem-baseband-and-standards.md)

## Objective

- Compute peak rates from the 3GPP capability formula for different carrier combinations.
- Simulate single- and double-sided UWB two-way ranging with drifting clocks.
- Estimate distance from a Bluetooth Channel Sounding phase sweep with multipath, two ways.
- Simulate the noise cost of the GNSS ionosphere-free combination.
- Trace the Doppler shift across a low-orbit satellite pass.

## Background

`modem.py` holds the capability arithmetic (`nr_rate_mbps`, `l2_buffer_bytes`, `soft_buffer_bytes`, `fft_cmults`, `wifi_rate_bps`), two-way ranging (`twr_simulate`, which times every interval with each device's own drifting clock), phase-based ranging (`pbr_phases`, `pbr_slope_distance`, `pbr_ifft_distance`), GNSS (`iono_free_coeffs`) and satellite Doppler (`leo_doppler_hz`). A modem is digital, so the lab simulates algorithms rather than circuits; there is no ngspice netlist.

## Procedure

1. **Peak rates.** *Predict* the rate of two 100 MHz carriers (4 layers, 256-QAM) plus a 20 MHz carrier (2 layers, 64-QAM), and how many times the five-carrier configuration of Example 21-12.1 exceeds it (Part 1).
2. **Two-way ranging.** *Predict* the rms and worst-case single-sided range error for clocks uniform within ±20 ppm and a 1 ms reply, then simulate a thousand exchanges, and compare with double-sided ranging (Part 2).
3. **Phase-based ranging.** *Predict* what a 72-tone sweep (2402–2473 MHz) reports for a 12 m path plus a half-amplitude reflection at 20 m, by phase slope and by inverse FFT (Part 3).
4. **Ionosphere-free noise.** *Predict* the standard deviation of the L1/L5 combination when each pseudorange has 1 m of independent noise, then simulate (Part 4).
5. **Doppler over a pass.** *Predict* the Doppler at 10°, 30° and 60° elevation for a 600 km satellite at 2 GHz, then plot it over a pass (Part 5).

## Expected results

- **Part 1.** **4844.1** Mb/s; the five-carrier 1024-QAM configuration is **2.28** times higher.
- **Part 2.** With $e_A - e_B$ triangular on ±40 ppm, the single-sided error has an rms of **2.45** m and a worst case of **6.00** m; the simulation agrees, and double-sided ranging stays below 1 mm.
- **Part 3.** The phase slope reports **11.94** m and the inverse-FFT peak **11.97** m (the oversampled grid step): the reflection 8 m behind the direct path, only about four resolution cells (2.08 m each) away, still biases the slope fit.
- **Part 4.** The combination's noise is $\sqrt{2.261^2 + 1.261^2}$ = 2.59 m; the simulation agrees to within a percent.
- **Part 5.** **45.4** kHz at 10°, **39.9** kHz at 30° and **23.1** kHz at 60°, falling through zero overhead and reversing as the satellite recedes.

## Discussion

1. **Why does double-sided ranging cancel the clock error?** Each device's clock error multiplies both a round time and a reply time; the product form of the estimator makes the terms proportional to the reply times cancel, leaving an error of about the range times the mean clock offset, a fraction of a millimetre here.
2. **Why do the slope and IFFT estimates disagree with multipath?** The slope fits the phase of the sum of both paths, which wobbles around the direct path's line; the IFFT separates paths only to about $c/(2B)$, so a reflection within a few resolution cells still pulls the peak.
3. **Why does a satellite modem need to know where it is?** The Doppler swings by about ±46 kHz over a pass; without its own position and the satellite's orbit, the phone would have to search that range before it could synchronize.

## Optional hardware

Two UWB development boards running double-sided ranging, or two Bluetooth 6.0 boards with Channel Sounding, measured along a corridor against a tape measure, show the bias that multipath adds near walls; repeat in an open space to see it shrink.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 21-12.a | three-carrier peak rate | 4844.1 | Mb/s |
| Lab 21-12.b | five-carrier over three-carrier | 2.28 | |
| Lab 21-12.c | single-sided rms error | 2.45 | m |
| Lab 21-12.d | single-sided worst case | 6.00 | m |
| Lab 21-12.e | phase-slope distance with multipath | 11.94 | m |
| Lab 21-12.f | inverse-FFT distance with multipath | 11.97 | m |
| Lab 21-12.g | Doppler at 10° | 45.4 | kHz |
| Lab 21-12.h | Doppler at 30° | 39.9 | kHz |
| Lab 21-12.i | Doppler at 60° | 23.1 | kHz |
