# Lab 17-10 · Building and Breaking OFDM

Chapter: [17-10 · OFDM](../../chapters/17-10-ofdm.md)

## Objective

Build an OFDM link from an IFFT, a cyclic prefix and an FFT, then check what keeps it working and what breaks it:

- subcarrier orthogonality, and its loss when the window is wrong;
- the cyclic prefix against channels longer and shorter than it;
- per-subcarrier SNR on a frequency-selective channel, with ZF and MMSE one-tap equalizers;
- inter-carrier interference from a frequency offset;
- the peak-to-average power of OFDM and of DFT-spread OFDM;
- NR's timing arithmetic.

## Background

Subcarriers spaced by $1/T$ are orthogonal over a window of length $T$ (§3.1). With a prefix at least as long as the channel's memory, each subcarrier sees $Y_k = H_kX_k + W_k$ (§3.3). A frequency offset ε (in subcarrier spacings) leaks a fraction $1 - |\sin\pi\varepsilon/(N\sin(\pi\varepsilon/N))|^2 \approx (\pi\varepsilon)^2/3$ of each subcarrier's power into the others (§3.5). OFDM samples are nearly complex Gaussian, so their PAPR exceeded with probability $p$ is about $\ln(N/p)$ (§3.6).

## Files

- `ofdm.py`: `qam`, `nearest`, `ofdm_mod`, `ofdm_demod`, `channel_response`, `apply_channel`, `equalize`, `simulate_link`, `cfo_attenuation`, `cfo_ici_power`, `ici_small_offset`, `ici_doppler`, `measure_ici`, `papr_db`, `ofdm_papr`, `dfts_papr`, `papr_ccdf_theory`, `papr_at`, `nr_symbol`, `nr_slot_duration`, `nr_guardband_khz`, and the constants `TC`, `KAPPA`.
- `17-10-ofdm-lab.ipynb`: the guided notebook.

## Procedure

1. **Orthogonality.** Predict the normalized correlation between subcarriers one and two spacings apart when the window is 0.9 of a symbol; compute both numerically.
2. **The cyclic prefix.** Send 16-QAM on 64 subcarriers through a 6-tap channel at 30 dB SNR with prefixes of 0, 3, 5 and 8 samples. Predict which prefixes give error-free decisions.
3. **Per-subcarrier quality.** Use a channel with a deep notch. At 20 dB SNR, measure the QPSK symbol-error rate on each subcarrier and compare with the prediction from $|H_k|^2 \cdot$ SNR. Check that ZF and bias-corrected MMSE make identical decisions.
4. **Frequency offset.** Predict the ICI for ε = 0.02, 0.05 and 0.1 on 256 subcarriers, then measure it by applying the offset to random symbols.
5. **PAPR.** Measure the PAPR CCDF of OFDM and of DFT-spread OFDM with 300 subcarriers (4× oversampled) and compare with the approximation.
6. **NR numerology.** Tabulate $T$, $T_{CP}$ and the slot length for μ = 0 to 4, and check that a subframe is exactly 1 ms.

## Expected results

- Part 1: about 0.109 and 0.104: a 10% window error couples subcarriers at about −19 dB.
- Part 2: prefixes of 5 and 8 samples work (the channel has 5 samples of memory); 0 and 3 leave an error floor.
- Part 3: per-subcarrier error rates follow the AWGN formula at each subcarrier's own SNR; ZF and MMSE decisions agree.
- Part 4: −28.8, −20.9 and −14.9 dB, measured within a few tenths of a decibel.
- Part 5: OFDM about 11 dB at $10^{-3}$ (slightly above the 11.0 dB approximation); DFT-spread OFDM several decibels lower.
- Part 6: slots of 1000, 500, 250, 125 and 62.5 μs; each subframe sums to 1 ms.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 17-10.a | correlation two spacings apart, 0.9 T window | 0.104 | — |
| Lab 17-10.b | shortest prefix for the 6-tap channel | 5 | samples |
| Lab 17-10.c | ICI at ε = 0.05, N = 256 | −20.9 | dB |
| Lab 17-10.d | PAPR approximation at 1e-3, N = 300 | 11.0 | dB |
| Lab 17-10.e | slot length at μ = 4 | 62.5 | μs |

## Discussion

1. Why does the one-tap equalizer need the prefix to be at least the channel length minus one, and what fails first if it is not?
2. In Part 3, why does coding across subcarriers rescue the notched subcarriers that equalization cannot?
3. Why is DFT-spread OFDM attractive for a phone's uplink but less so for a base station's downlink?

## Answers

1. Only then does every delayed copy of the symbol inside the FFT window look like a circular shift of it. With a shorter prefix, part of the previous symbol enters the window (ISI) and the delayed copy is no longer circular, so the FFT sees leakage between subcarriers (ICI); both produce an error floor that no SNR removes.
2. The notched subcarriers carry a few unreliable bits; a decoder that knows they are unreliable (their LLRs are small) recovers them from the redundancy spread over the many good subcarriers, whereas equalization can only rescale a subcarrier's own SNR.
3. A phone's power amplifier dominates its transmit power budget, so a lower PAPR buys battery life and coverage. A base station multiplexes many users with flexible, non-contiguous allocations and can afford linearization (DPD, crest-factor reduction), so OFDM's flexibility wins there.

## Optional hardware

A software-defined radio can transmit the lab's OFDM frames over a short cable or over the air. Measuring the received constellation per subcarrier shows the channel's frequency response, the effect of an uncorrected frequency offset (a rotating, spreading constellation) and the benefit of estimating and removing it from the cyclic prefix.
