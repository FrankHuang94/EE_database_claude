# Lab 17-08 · Block, Convolutional, LDPC and Polar Codes

Chapter: [17-08 · Channel Coding](../../chapters/17-08-channel-coding.md)

## Objective

Build and run every class of code in the chapter and check its claims:

- the weight structure and block error rate of Hamming codes;
- the burst-detection guarantees of a CRC, by exhaustive test;
- Viterbi decoding of the $K$ = 3 and $K$ = 7 convolutional codes against their union bounds, with soft and hard decisions;
- the threshold behaviour of an iteratively decoded LDPC code;
- channel polarization and a successive-cancellation polar decoder;
- Reed–Solomon failure probability against raw bit-error rate.

## Background

A linear code is fixed by its generator matrix $G$ or parity-check matrix $H$; distances are weights of codewords (§3.2). A CRC misses an error pattern only if the generator polynomial divides it (§3.4). A convolutional code's error rate follows from the weights of paths that leave and rejoin the zero state, $P_b \le \sum_dB_dQ(\sqrt{2RdE_b/N_0})$ (§3.7). LDPC decoders pass log-likelihood ratios between bits and checks; polar decoders decode bits in order on polarized channels (§3.8). Reed–Solomon codes fail when more than $t$ of $n$ symbols are wrong (§3.6).

## Files

- `coding.py`: GF(2) helpers (`gf2_matmul`, `gf2_rref`, `gf2_rank`, `gf2_nullspace`); block codes (`hamming`, `hamming74`, `encode_block`, `all_codewords`, `weight_distribution`, `min_distance`, `syndrome`, `syndrome_decode`, `block_error_bsc`); `rs_codeword_error`, `rs_burst_bits`; CRCs (`NR_CRC`, `poly_bits`, `crc_remainder`, `crc_append`, `crc_check`); convolutional codes (`conv_encode`, `viterbi`, `path_metric_hard`, `distance_spectrum`, `free_distance`, `union_bound_ber`); LDPC (`gallager_ldpc`, `min_sum_decode`); polar (`bec_polarize`, `polar_encode`, `polar_sc_decode`, `polar_design`); `bpsk_awgn`.
- `17-08-coding-lab.ipynb`: the guided notebook.

The convolutional encoder takes generators in octal with the most significant bit tapping the current input, the usual convention. It does not model CCSDS's inversion of the second output, which changes no distance property.

## Procedure

1. **Hamming codes.** Predict how many weight-3 codewords the (15,11) Hamming code has, then enumerate its weight distribution. Simulate its block error rate on a BSC with $p = 10^{-2}$ and compare with the binomial formula.
2. **CRC bursts.** For CRC6 ($x^6 + x^5 + 1$), predict which burst lengths are always detected and what fraction of 7-, 8- and 9-bit bursts slip through; test every burst pattern.
3. **Viterbi.** Predict the union-bound BER of the $K$ = 3 and $K$ = 7 codes at $E_b/N_0$ = 3.5 dB, then simulate both with soft decisions; repeat the $K$ = 7 code with hard decisions and estimate the soft-decision advantage in decibels.
4. **LDPC.** Build a (3,6)-regular Gallager code of length 504, find its rank and a generator, and simulate frame-error rate and mean iterations at 1.5–3 dB.
5. **Polar codes.** Plot the sorted erasure probabilities for $N$ = 8, 64 and 1024 at ε = 0.5 and measure the fraction still "undecided" (between 0.1 and 0.9). Then design a (256,128) code and simulate it at 2–4 dB.
6. **Reed–Solomon.** Plot the failure probability of RS(544,514) and RS(528,514) against raw BER and find the BER at which each reaches $10^{-12}$.

## Expected results

- Part 1: 35 codewords of weight 3 ($d_{min}$ = 3); simulation on the formula.
- Part 2: all bursts up to 6 bits detected; 1 of the 32 seven-bit patterns and 1/64 of longer ones missed.
- Part 3: union bounds of about $2.8 \times 10^{-3}$ ($K$ = 3) and $1.2 \times 10^{-4}$ ($K$ = 7) at 3.5 dB. Long simulations land below them (about half, for $K$ = 7); short ones scatter by a factor of 2 or more because each decoding error event flips several bits. Hard decisions need roughly 2 dB more.
- Part 4: rank 250 of 252 rows, so the code has $k$ = 254; frame errors fall from about 20% at 1.5 dB to almost none by 3 dB, with fewer iterations at higher SNR.
- Part 5: undecided fraction 0.75 at $N$ = 8, 0.31 at 64 and 0.13 at 1024; the (256,128) code reaches a frame-error rate below 1% near 3 dB.
- Part 6: thresholds of $2.4 \times 10^{-4}$ (KP4) and $2.3 \times 10^{-5}$ (KR4).

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 17-08.a | weight-3 codewords of the (15,11) code | 35 | — |
| Lab 17-08.b | 7-bit bursts missed by CRC6 (of 32) | 1 | — |
| Lab 17-08.c | 9-bit burst miss fraction | 0.015625 | — |
| Lab 17-08.d | K = 3 union bound at 3.5 dB | 2.75e-3 | — |
| Lab 17-08.e | K = 7 union bound at 3.5 dB | 1.2e-4 | — |
| Lab 17-08.f | undecided polar channels, N = 1024 | 0.131 | — |
| Lab 17-08.g | KP4 raw BER for failure 1e-12 | 2.43e-4 | — |

## Discussion

1. Why does the union bound overestimate the BER at low SNR but become tight at high SNR?
2. The LDPC code here has length 504; why would a length-64 800 code (DVB-S2) have a much sharper waterfall?
3. Why does NR use polar codes for control information but LDPC for data?

## Answers

1. The bound adds the probabilities of overlapping error events as if they were disjoint; at low SNR many events happen together and are counted several times, while at high SNR one dominant event is rare enough that overlaps are negligible.
2. Longer codes average over more noise: the fraction of bits a frame can afford to get wrong is concentrated near its mean, so the transition from "almost always fails" to "almost never fails" narrows toward the code's threshold. Long codes also have fewer short cycles in their graphs, so belief propagation is closer to optimal.
3. Control payloads are short (tens to hundreds of bits), where CRC-aided list-decoded polar codes perform well and latency matters; data blocks run to thousands of bits per code block, where quasi-cyclic LDPC decoders achieve the highest throughput per area and support incremental-redundancy retransmission.

## Optional hardware

Software-defined radios or a microcontroller pair can carry coded packets: send a CRC-protected payload with and without a convolutional code through an attenuator, and count delivered and corrupted packets as the attenuation rises. The lab's encoder and decoder run fast enough in Python for low-rate experiments.
