# Lab 17-07 · Entropy, Capacity and Water-Filling

Chapter: [17-07 · Information Theory and Shannon Capacity](../../chapters/17-07-information-theory-and-shannon.md)

## Objective

Compute the chapter's information measures and check its claims numerically:

- the entropy of a text and how close a Huffman code comes to it;
- channel capacity by the Blahut–Arimoto algorithm, against closed forms for the BSC and the Z-channel;
- how capacity responds to bandwidth at high and at low SNR;
- the capacity of BPSK with soft and with hard decisions against the Gaussian-input bound;
- water-filling over the subcarriers of a frequency-selective channel.

## Background

Entropy $H = -\sum p_i\log_2p_i$ is the least average number of bits per symbol a lossless code can achieve (§3.2). Capacity is the largest mutual information over input distributions (§3.4); the Blahut–Arimoto algorithm finds it for any discrete channel by alternately computing the output distribution and reweighting each input by $2^{D(x)}$, where $D(x)$ is the divergence between that input's output distribution and the overall one. For the Gaussian channel $C = B\log_2(1 + S/(N_0B))$ (§3.5); a binary input caps it at 1 bit per use, and hard slicing lowers it further (§3.7). Over parallel channels the optimum power is $p_k = (\mu - 1/g_k)^+$ (§3.8).

## Files

- `infotheory.py`: `entropy`, `binary_entropy`, `empirical_entropy`, `huffman`, `average_length`, `kraft`, `encode`, `decode`, `mutual_info`, `blahut_arimoto`, `bsc_capacity`, `bec_capacity`, `z_capacity`, `gaussian_diff_entropy`, `awgn_real`, `shannon_hartley`, `capacity_from_sn0`, `bpsk_soft_capacity`, `bpsk_hard_capacity`, `gaussian_real_capacity`, `required_es_n0_db`, `shannon_limit_db`, `waterfill`, `equal_power_capacity`, plus `SAMPLE_TEXT` and `letters_only`.
- `17-07-infotheory-lab.ipynb`: the guided notebook.

## Procedure

1. **Compression.** Reduce `SAMPLE_TEXT` to lower-case letters and spaces. Predict its entropy per character (English letters carry roughly 4 bits each when only their frequencies are used), then compute it, Huffman-code the text, check that it decodes exactly, and compare the average length with the entropy and with $\log_2$ of the alphabet size.
2. **Capacity by algorithm.** Predict the BSC capacity at $p$ = 0.1; confirm it with `blahut_arimoto`. Repeat for the Z-channel with $q$ = 0.5 and note the optimal input distribution.
3. **Bandwidth at fixed power.** With $S/N_0$ fixed, double the bandwidth starting from an SNR of 30 dB and from −10 dB. Predict each capacity ratio, then compute.
4. **Constrained inputs.** Plot Gaussian-input, BPSK-soft and BPSK-hard capacity against $E_s/N_0$, and find the $E_b/N_0$ at which each reaches rate 1/2.
5. **Water-filling.** A 64-subcarrier channel has response $H_k = 1 + 0.9e^{-j2\pi k/64}$, so subcarrier $k$ has gain $g_k = |H_k|^2$ for a transmit SNR of 0 dB per unit power. With total power 64, predict which subcarriers are switched off, then compute the allocation and compare its capacity with equal power.

## Expected results

- Part 1: about 4.0 bits per character from 25 distinct symbols (against $\log_225$ = 4.64), and a Huffman code within 0.04 bits of the entropy.
- Part 2: 0.531 bits per use for the BSC, uniform input; 0.322 for the Z-channel, with $P(X = 1)$ = 0.4.
- Part 3: about 1.8 times the capacity at high SNR, almost no change at −10 dB.
- Part 4: rate 1/2 at 0 dB (Gaussian), 0.19 dB (soft) and 1.77 dB (hard).
- Part 5: the 15 subcarriers around the channel's null at $k$ = 32 get no power; water-filling beats equal power by about 0.17 b/s/Hz per subcarrier.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 17-07.a | entropy of the sample text | 4.01 | bits/char |
| Lab 17-07.b | Huffman average length | 4.05 | bits/char |
| Lab 17-07.c | BSC capacity at p = 0.1 | 0.531 | bits/use |
| Lab 17-07.d | capacity ratio, bandwidth doubled at 30 dB | 1.80 | — |
| Lab 17-07.e | capacity ratio, bandwidth doubled at −10 dB | 1.024 | — |
| Lab 17-07.f | subcarriers given no power | 15 | — |
| Lab 17-07.g | water-filling capacity per subcarrier | 1.487 | b/s/Hz |
| Lab 17-07.h | equal-power capacity per subcarrier | 1.313 | b/s/Hz |

## Discussion

1. Why does the Huffman code on single characters fall well short of the true information rate of English, which Shannon's 1951 prediction experiments put at roughly 0.6–1.3 bits per letter?
2. Why is the Z-channel's optimal input not uniform, while the BSC's is?
3. In Part 5, why does water-filling help more at low SNR than at high SNR?

## Answers

1. Character frequencies ignore context: after "th", "e" is far more likely than its average frequency suggests. Coding words or using a predictive model (as modern compressors do) captures those dependencies and approaches the lower rate.
2. The BSC treats both inputs symmetrically, so by symmetry the uniform input is optimal. In the Z-channel a 0 always arrives intact while a 1 is often corrupted into a 0, so sending the reliable symbol more often increases the mutual information.
3. At high SNR every subcarrier's $\log_2(1 + g_kp_k)$ is in its logarithmic region, where moving power changes little; at low SNR capacity is nearly linear in $g_kp_k$, so putting power where the gain is largest pays off directly.

## Optional hardware

Compress a few real files (text, an image, an already-compressed archive) with a standard tool and compare the compressed sizes with the single-character entropy computed by `empirical_entropy` on their bytes. Text compresses well beyond that estimate because of context; the archive barely compresses at all.
