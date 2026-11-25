# Lab 24-04 · ADC Bits, MLSD and FEC

**Objective.** See how many ADC bits a PAM4 DSP receiver needs; compare MLSD with an ideal DFE and search error events exhaustively; and compute FEC output error rates, coding gains, line rates and latencies.

**Chapter:** [24-04 · DSP-Based SerDes and FEC](../../chapters/24-04-dsp-serdes-and-fec.md)

## Background

§3.2 sized an ADC from quantization noise, $\Delta/\sqrt{12}$, and jitter, $-20\log_{10}(2\pi f\sigma_t)$. §3.3 introduced the MMSE FFE. §3.4 derived MLSD's distance gain, $10\log_{10}(1 + \alpha^2)$ on $h = (1, \alpha)$ for α ≤ 1. §3.5 and §3.6 gave the net coding gain and the latency of RS(544,514) and its inner code.

## Files

- `dsp.py`: quantizer, SQNR, jitter-limited and combined SNR; PAM symbols and a channel with pre- and post-cursors; MMSE FFE design; slicer; ideal DFE; a Viterbi detector; exhaustive error-event search; RS(544,514) failure and output BER; NCG; codeword time; burst length corrected under interleaving.
- `24-04-dsp-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · ADC bits** (notebook). PAM4 crosses $h$ = (0.1, 1, 0.5, 0.2), with the main cursor second, and noise of rms 0.075. An 11-tap MMSE FFE equalizes it. The ADC's full scale just covers the received peak, ±1.8. *Predict* how the symbol error rate changes from 4 to 8 bits, then simulate.

**Part 2 · MLSD against DFE** (notebook). Run an exhaustive error-event search for $h = (1, \alpha)$ at α = 0.5, 1 and 1.25. Then simulate NRZ on $h = (1, 1)$ through an ideal DFE and a Viterbi detector. *Predict* the SNR gap at a BER of 10⁻³.

**Part 3 · FEC curves** (notebook). Compute RS(544,514)'s output BER against its random-error input BER. *Predict* the output at an input of 2.4 × 10⁻⁴.

**Part 4 · Rates and latency** (notebook). Compute the 802.3dj inner-code line rate, the NCGs of Example 24-04.7, and the codeword and flit times of Example 24-04.5.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 24-04.a | 6-bit SQNR at full scale 3.6, PAM4 rms | 33.2 | dB |
| Lab 24-04.b | 4-bit SQNR at full scale 3.6 | 21.2 | dB |
| Lab 24-04.c | MLSD distance, alpha 0.5 | 5 | |
| Lab 24-04.d | MLSD distance, alpha 1 | 8 | |
| Lab 24-04.e | MLSD distance, alpha 1.25 | 10.25 | |
| Lab 24-04.f | MLSD distance gain, alpha 1 | 3.01 | dB |
| Lab 24-04.g | DFE noise for BER 1e-3 | 0.324 | |
| Lab 24-04.h | KP4 uncorrectable codeword ratio at 2.4e-4 | 8.15e-13 | |
| Lab 24-04.i | KP4 output BER at 2.4e-4 | 2.40e-15 | |
| Lab 24-04.j | inner-code line rate | 113.4375 | GBd |
| Lab 24-04.k | codeword time at 212.5 Gb/s | 25.6 | ns |

- Part 1: with a ±1.8 full scale, 4 bits give an SQNR of only 21.2 dB and the symbol error rate is more than ten times the ideal ADC's; at 6 bits (33.2 dB) it is within a few tens of percent of ideal, and at 7 bits indistinguishable. (SQNR here is relative to the PAM4 symbol rms.) Shrinking the full scale would help at 4 bits until clipping set in.
- Part 2: the search returns single-symbol errors as the closest events, with squared distances 5, 8 and 10.25. The simulated MLSD advantage at 10⁻³ is well short of the 3.01 dB distance gain, because the closest error events are numerous (on $h = (1, 1)$ every alternating error pattern has the same distance) and many cause several bit errors; the advantage widens toward 3 dB as the error rate falls, and the notebook prints its value. The ideal DFE reaches 10⁻³ at σ = 0.324.
- Part 3: at an input BER of 2.4 × 10⁻⁴, the uncorrectable codeword ratio is 8.15 × 10⁻¹³ and the output BER 2.40 × 10⁻¹⁵, as 03-04 found. The curve is so steep that a factor of 2 in input BER moves the output by orders of magnitude.
- Part 4: 113.4375 GBd for the inner-code lanes; 25.6 ns per codeword at 212.5 Gb/s.

## Discussion

1. Why does MLSD's advantage at moderate error rates fall short of its distance gain?

   <details><summary>Answer</summary>

   The error rate is roughly the number of error events at the minimum distance times $Q(d_{min}/2\sigma)$. A DFE has essentially one way to err per symbol; on $h = (1, 1)$ MLSD has many minimum-distance events of different lengths, each causing one or more bit errors. That multiplicity costs a fraction of a dB, a cost that shrinks as the Q function steepens at low error rates.

   </details>

2. Why is the ADC's full scale a design choice, not a given?

   <details><summary>Answer</summary>

   A larger full scale avoids clipping the ISI peaks but enlarges each quantization step; a smaller one does the reverse. The optimum depends on the channel's peak-to-rms ratio before equalization, and adaptive gain control sets it in practice.

   </details>

3. What would precoding change about Part 2?

   <details><summary>Answer</summary>

   Precoding, $1/(1 \oplus D)$ for NRZ, turns the multi-symbol error events of a 1 + D channel into at most two bit errors, so the FEC sees shorter bursts. It does not change the detection distance.

   </details>

## Optional hardware

FPGA boards with ADC-based transceivers are not generally available, but software-defined-radio boards with a few-GS/s ADC let the quantization and jitter experiments of Part 1 be repeated on real hardware at lower rates.
