# Lab 21-07 · Power Amplifiers: Classes, Back-off, Doherty, ACLR and Predistortion

Chapter: [21-07 · Power Amplifiers](../../chapters/21-07-power-amplifiers.md)

## Objective

- Compute efficiency and output power against conduction angle, and see a class-E amplifier's zero-voltage switching in ngspice.
- Plot efficiency against back-off for classes A and B, the Doherty and envelope tracking, and average them over an OFDM envelope.
- Confirm a Doherty amplifier's load modulation in ngspice.
- Measure the ACLR of a cubic PA driven by OFDM and compare it with the formula $\text{ACLR} = (P/P_{IIP3})^2/3$.
- Linearize a saturating PA with polynomial digital predistortion and find where clipping, not the predistorter, sets the limit.

## Background

`pa.py` holds `r_opt` (load line), `conduction` (Fourier coefficients and efficiency against conduction angle), `eta_backoff`, `eta_doherty`, `class_f3_eta`, `class_e` (normalized design values) and `average_efficiency` (expectation over a Rayleigh envelope with the peak at a given PAPR). For signals it has `ofdm` (seeded 16-QAM OFDM, 128 of 1024 subcarriers, unit power), `rapp` and `cubic` PA models, `aclr_db`, `evm_pct`, and an indirect-learning polynomial predistorter (`fit_postinverse`, `apply_poly`, `dpd_loop`).

`classe.cir` simulates the class-E design of Example 21-07.3 with an ideal switch, a 1 µH choke and a Q = 30 output resonator. `doherty.cir` simulates the ideal Doherty of Example 21-07.6 at three drive levels, with half-wave-rectified current sources for the class-B devices and a 25 Ω quarter-wave line.

## Procedure

1. **Conduction angle.** *Predict* the efficiency at 360°, 240°, 180° and 120°, then plot efficiency and relative output power against conduction angle (Part 1).
2. **Class E.** *Predict* the output power, efficiency and peak switch voltage. Run `ngspice -b classe.cir`, then plot the switch voltage and current over two cycles and check that the voltage reaches zero with zero slope just before the switch closes (Part 2).
3. **Back-off and averages.** *Predict* the efficiency of each architecture at 6 and 10 dB back-off, then plot the curves over the OFDM envelope's density and compute the averages (Part 3).
4. **Doherty in ngspice.** *Predict* the main device's voltage swing and the efficiency at $x$ = 0.5, 2/3 and 1, then run `ngspice -b doherty.cir` (Part 4).
5. **ACLR of a cubic PA.** *Predict* the ACLR for $a_3$ = −0.05 and an input power 20 dB below unity ($P/P_{IIP3}$ = −33.0 dB), then simulate (Part 5).
6. **Predistortion.** *Predict* whether DPD helps more at 12 dB or at 10 dB of saturation margin. Apply the fifth-order predistorter and the ideal clipping inverse at both, and plot the spectra (Part 6).

## Expected results

- **Part 1.** 50.0%, 66.1%, 78.5% and 89.7%; class AB at 240° gives 0.3 dB more power than class A, class C at 120° 1.1 dB less (at full swing the power follows $I_1$, so the comparison is $10\log_{10}$ of the current ratio).
- **Part 2.** About 1.01 W at 99.95% efficiency, peak switch voltage near 11.9 V (the ideal 1.000 W and 11.75 V, raised 1–2% by the finite Q and choke). The voltage returns to zero with zero slope at the switching instant.
- **Part 3.** Class B 29.2%, Doherty 54.9% and envelope tracking (20% floor, 85% modulator) 65.5% average efficiency, against class A's 5.4%.
- **Part 4.** The main drain swings 28.0 V at both 0.5 and full drive; efficiency 78.5%, 69.8% and 78.5%.
- **Part 5.** The formula gives **−70.79** dBc; the 16-QAM OFDM simulation gives **−70.5** dBc, a few tenths of a decibel higher because a 128-subcarrier signal is only approximately Gaussian and the channel edges fall on discrete bins.
- **Part 6.** With 12 dB of margin, the fifth-order DPD improves the ACLR from **−48.6** dBc to **−66.4** dBc and the EVM from 0.88% to 0.10%. With 10 dB of margin it reaches only −48.3 dBc from −41.8 dBc, and even an ideal inverse stops at −55.2 dBc: the peaks above saturation are clipped whatever the predistorter does.

## Discussion

1. **Why does the Doherty's efficiency dip between its two peaks?** Between them the auxiliary device conducts but is not yet at full swing, so it draws DC current while its voltage, and therefore its efficiency, is low.
2. **Why does DPD stop working near saturation?** The inverse of a saturating characteristic needs unbounded drive as the output approaches saturation. A polynomial fitted to such data is poorly conditioned and can make things worse; in practice crest-factor reduction keeps the peaks below saturation and DPD linearizes what remains.
3. **Why is the ACLR formula independent of the signal's bandwidth?** Both the distortion and the signal scale with the same spectral shape; only their ratio and the fraction of the triple-convolution bump that lands next door, one-sixth, matter.

## Optional hardware

An evaluation board for a handset PA module or a small GaN transistor, a signal generator with a modulated (LTE or Wi-Fi) waveform, a spectrum analyzer and a DC supply with a current readout make this lab real: sweep the input power, record output power, DC current and ACLR, and plot efficiency against back-off and ACLR against output power. If the generator supports it, compare a clipped (crest-factor-reduced) waveform with the original.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 21-07.a | cubic-model ACLR, formula | −70.79 | dBc |
| Lab 21-07.b | cubic-model ACLR, OFDM simulation | −70.5 | dBc |
| Lab 21-07.c | ACLR at 12 dB margin, no DPD | −48.6 | dBc |
| Lab 21-07.d | ACLR at 12 dB margin, fifth-order DPD | −66.4 | dBc |
| Lab 21-07.e | EVM at 12 dB margin, no DPD | 0.88 | % |
| Lab 21-07.f | EVM at 12 dB margin, fifth-order DPD | 0.10 | % |
