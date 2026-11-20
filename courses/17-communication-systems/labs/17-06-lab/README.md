# Lab 17-06 · Constellations, Error Rates and EVM

Chapter: [17-06 · Bandpass Digital Modulation and BER](../../chapters/17-06-bandpass-digital-modulation.md)

## Objective

Simulate bandpass modulation in complex baseband and check the chapter's results:

- constellation energy, minimum distance and peak-to-average ratio;
- symbol- and bit-error rates of PSK and QAM against Craig's formula and the QAM closed form;
- the benefit of Gray labelling;
- EVM from phase noise, I/Q imbalance and a compressing amplifier, and its equivalent SNR;
- DPSK and FSK against BPSK.

## Background

In complex baseband a symbol is a point $I + jQ$; white noise adds independent Gaussian components of variance $N_0/2$ to I and Q (§3.1). Detection picks the nearest point, so all error rates follow from geometry (17-05). EVM is the rms error vector relative to the rms ideal symbol; if noise-like, it acts like an SNR of $1/\text{EVM}^2$ (§3.7).

## Files

- `modulation.py`: `psk`, `qam`, `natural_qam`, `es`, `dmin`, `papr_db`, `awgn`, `detect`, `simulate`, `ser_psk_craig`, `ser_psk_nn`, `ser_qam`, `ber_dpsk`, `ber_fsk_coherent`, `ber_fsk_noncoherent`, `evm`, `phase_noise`, `iq_imbalance`, `soft_clip`, `simulate_dpsk`, `simulate_bfsk`.
- `17-06-modulation-lab.ipynb`: the guided notebook.

## Procedure

1. **Constellations.** Predict $E_s$, $d_{min}$ and the peak-to-average ratio of QPSK, 8-PSK, 16-QAM and 64-QAM; compute them.
2. **Error rates.** Predict, then simulate, BER against $E_b/N_0$ for BPSK, QPSK, 8-PSK, 16-QAM and 64-QAM.
3. **Gray coding.** Predict the BER ratio of natural to Gray labelling for 16-QAM at $E_b/N_0$ = 12 dB; simulate both.
4. **EVM.** Predict the EVM of 64-QAM with 2° rms phase noise and with a 1%, 1° I/Q imbalance; then drive a soft-clipping amplifier at several back-offs and watch EVM rise.
5. **Noncoherent options.** Simulate DPSK and noncoherent FSK at 6–12 dB against BPSK.

## Expected results

- Part 1: $E_s$ = 2, 1, 10 and 42 (with the lab's scalings), peak-to-average 0, 0, 2.55 and 3.68 dB.
- Part 2: simulations on the formulas; QPSK on top of BPSK per bit.
- Part 3: natural labelling about 1.3 times worse.
- Part 4: about 3.49% from phase noise and about 1.0% from the imbalance; amplifier EVM grows steeply as back-off falls below the peak-to-average ratio.
- Part 5: DPSK about 0.75 dB and noncoherent FSK about 3.8 dB behind BPSK at $10^{-5}$.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 17-06.a | 64-QAM average energy (levels ±1…±7) | 42 | — |
| Lab 17-06.b | EVM from 2° rms phase noise | 3.49 | % |
| Lab 17-06.c | DPSK penalty over BPSK at 1e-5 | 0.75 | dB |

## Discussion

1. Why does the soft-clipping amplifier's EVM rise so quickly once the back-off is less than the constellation's peak-to-average ratio?
2. Why is phase noise worse for 64-QAM's outer points than its inner ones, and what does that imply for 1024-QAM?
3. Why do low-power radios accept noncoherent FSK's penalty?

### Answers

1. Only the high-amplitude (corner) symbols are compressed at first, but their error vectors are large and they carry much of the average power; as the drive rises, more symbols compress.
2. A phase error moves a point by its radius times the angle, so outer points move furthest. 1024-QAM has more points at large radius and much smaller spacing, so the same oscillator costs it far more.
3. Their receivers need no carrier recovery and their transmitters run saturated, saving power and cost; at short range the 3–4 dB is affordable.

## Optional hardware

A software-defined radio pair (or a single one in loopback through an attenuator) can transmit QPSK or 16-QAM; capturing the received constellation and computing EVM with `evm` shows the effect of gain settings, frequency offset and the amplifier's drive level.
