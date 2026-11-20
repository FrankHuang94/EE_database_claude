# Lab 17-02 · Noise Budgets and Calibrated AWGN

Chapter: [17-02 · Noise and SNR in Communication Systems](../../chapters/17-02-noise-and-snr.md)

## Objective

Check the chapter's noise arithmetic against simulation and circuit analysis:

- the noise power that passes filters of different bandwidths;
- the noise figure of a cascade, measured in a time-domain model;
- the independence of bit-error rate from the sample rate once noise is calibrated to $E_b/N_0$, and the cost of calibrating it wrongly;
- the SNR gained by correlating a spread signal;
- the noise bandwidth of a one-pole filter.

Confirm with ngspice that a 50 Ω source delivers $kTB$ to a matched load and that a matched resistive pad at 290 K has a noise figure equal to its loss.

## Background

A source at temperature $T$ offers $kT$ watts per hertz to a matched load (§3.1). A two-port's noise factor is its total output noise over the part due to a 290 K source (§3.3), and a matched passive loss at 290 K has $F = L$ (§3.4). Cascades follow Friis's formula (§3.5). In a sampled simulation with unit sample spacing, white noise of one-sided density $N_0$ has variance $N_0/2$ per real sample, so the noise must be set from $E_b/N_0$ and the energy of a bit's samples, not from a per-sample SNR (§8, Problem 17-02.10).

## Files

- `noisebudget.py`: decibel helpers (`db`, `undb`, `dbm`, `watts`, `add_dbm`), thermal noise (`ktb_dbm`, `vn_rms`, `planck_factor`), noise figure and temperature (`te_from_nf`, `nf_from_te`, `lossy`, `friis`, `friis_db`, `cascade_te`, `noise_measure`), link figures (`sensitivity_dbm`, `ebn0_from_snr`, `cn0_dbhz`, `shannon_ebn0_db`) and calibrated simulation (`noise_sigma`, `awgn`, `bpsk_ber_sim`, `despread_snr`, `cascade_sim`).
- `17-02-noise-budget-lab.ipynb`: the guided notebook.
- `pad_noise.cir`: ngspice noise analysis of a 50 Ω source into a matched noiseless load, and of the same source through a 6 dB T-pad with its resistors noiseless and noisy.

## Procedure

1. **Noise in a bandwidth.** Generate white noise of one-sided density $kT_0$ at 1 MS/s. Predict its power after ideal 1, 10 and 100 kHz filters, then filter it in the frequency domain and measure.
2. **A cascade.** Predict the noise figures of Example 17-02.3's two orderings. Then run `cascade_sim`, in which each stage adds independent noise of its noise temperature before amplifying, and compare.
3. **Calibration.** Predict the BPSK bit-error rate at $E_b/N_0$ = 6 dB. Simulate it at 1, 4 and 16 samples per bit, then at 8 samples per bit with the per-sample SNR wrongly set to 6 dB.
4. **Below the noise.** Spread ±1 symbols with a 1023-chip ±1 code at a per-chip SNR of −20 dB. Predict the SNR after correlation, then measure it.
5. **Noise bandwidth.** Pass white noise through a one-pole filter with a 1 kHz corner and compare the measured noise power with $N_0f_c$ and with $N_0(\pi/2)f_c$.
6. **ngspice.** Run `ngspice -b pad_noise.cir` (or `python tools/run_spice.py 17-02` from the repository root) and read the delivered noise power, the pad's loss and its noise figure.

## Expected results

- Part 1: −143.98, −133.98 and −123.98 dBm, within about 0.1 dB.
- Part 2: about 2.29 dB with the cable first and 0.88 dB with the LNA first (Example 17-02.3).
- Part 3: about $2.4 \times 10^{-3}$ at every sample rate; the miscalibrated run makes no errors in two million bits, because it actually simulates 12 dB.
- Part 4: about −20 + 30.1 = 10.1 dB after correlation.
- Part 5: the noise exceeds $N_0f_c$ by 1.96 dB, as $\pi/2$ predicts.
- Part 6: −113.98 dBm into the matched load; a 6.00 dB loss and a 6.00 dB noise figure for the pad.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 17-02.a | noise figure of the 6 dB pad (ngspice) | 6.00 | dB |
| Lab 17-02.b | loss of the 6 dB pad (ngspice) | 6.00 | dB |
| Lab 17-02.c | noise in 1 kHz at 290 K | −143.98 | dBm |
| Lab 17-02.d | SNR after correlating 1023 chips at −20 dB | 10.1 | dB |

## Discussion

1. In Part 2, why does the receiver's contribution come out the same in both orderings?
2. In Part 3, why does the bit-error rate not depend on the number of samples per bit, once the noise is calibrated correctly?
3. In Part 4, the SNR rose by 30 dB. Did $E_b/N_0$ change?
4. In Part 6, the pad's resistors generate noise, yet the total noise at the load is exactly what a single 50 Ω resistor would deliver. Why, and why is the noise figure nonetheless 6 dB?

### Answers

1. In both orderings the receiver sits behind both the cable and the LNA, so its excess noise is divided by the same net gain $G_{LNA}/L$.
2. The detector sums a bit's samples. More samples per bit add more signal energy and proportionally more noise variance at a fixed $N_0$; the ratio, $2E_b/N_0$, does not change.
3. No. Correlation narrows the bandwidth from the chip rate to the symbol rate; the energy per symbol and the noise density are unchanged, so $E_s/N_0$ and $E_b/N_0$ are the same before and after.
4. Everything is at 290 K and matched, so the output port looks like one 50 Ω resistor at 290 K and offers $kTB$ (thermodynamic equilibrium). But the signal, and the source's share of that noise, are attenuated by 6 dB; the pad's own noise fills the difference. The ratio of total noise to source noise, the noise factor, is the loss.

## Optional hardware

A spectrum analyzer with a noise-marker function and a 50 Ω terminator can show −174 dBm/Hz plus the analyzer's own noise figure (17-01 §9). Adding a known attenuator before a low-noise preamplifier and measuring the noise floor rise with a calibrated noise source (the Y-factor method, 21-03) measures noise figure directly.
