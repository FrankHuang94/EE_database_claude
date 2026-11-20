# Lab 16-03 · The DFT in Practice

Chapter: [16-03 The DFT and Its Properties](../../chapters/16-03-the-dft.md)

## Objective

Build the DFT from its definition and see each of its properties at work: orthogonality, sampling of the DTFT, the limits of zero padding, wrap-around in circular convolution, fast block filtering, and the cyclic prefix that makes OFDM work.

## Background

Read §3 of the chapter. `dft.py` computes the DFT as an explicit matrix product and circular convolution directly from its definition, so every result can be compared with `numpy.fft` and `numpy.convolve`. The OFDM part of the notebook uses `numpy.fft` for speed.

## Files

- [dft.py](dft.py): `dft_matrix`, `dft`, `idft`, `dtft`, `bin_freq`, `circ_shift`, `circ_conv`, `overlap_add`, `overlap_save` and `fft_conv_cost`.
- [16-03-dft-lab.ipynb](16-03-dft-lab.ipynb): the notebook (Parts 1–5).

## Procedure

1. **Build the DFT matrix (Part 1).** For $N$ = 8, display the real parts of $\mathbf F$'s rows (eight sampled cosines), check $\mathbf F^H\mathbf F = 8\mathbf I$, and compare `dft` with `numpy.fft.fft` on random data.
2. **The DFT samples the DTFT (Part 2).** For a 16-sample Hann-shaped pulse, overlay the 16-point DFT on the DTFT, then zero-pad to 64 and 256 points. Then try to separate two tones 0.5 bins apart (in 64-sample units) by zero padding a 64-sample record to 4096 points. *Predict first:* will padding separate them?
3. **Wrap a convolution (Part 3).** Convolve a 12-sample input with a 5-tap filter by $N$-point DFTs for $N$ = 12 to 18 and plot the error against linear convolution.
4. **Filter in blocks (Part 4).** Filter 100,000 samples with a 101-tap filter by overlap-add and overlap-save at $N$ = 1024, check both against `numpy.convolve`, time all three, and plot the cost model $C(N, 101)$.
5. **Make a channel circular (Part 5).** Send 200 OFDM symbols of QPSK on 64 subcarriers (seed 5) through the channel $(1, 0.5, -0.3, 0.2, 0.1)$ with cyclic prefixes of 0 to 6 samples and no noise, equalize each subcarrier by one complex division, and record the rms error vector (as a percentage of the symbol magnitude) and the number of wrong QPSK decisions. *Predict first:* at which prefix length does the error vector vanish, and do decisions fail before that?

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Orthogonality | $\mathbf F^H\mathbf F = 8\mathbf I$ to rounding; `dft` equals `numpy.fft.fft` |
| 2 | Zero padding | the samples fill in the same DTFT curve; tones 0.5 bins apart stay merged in one peak at any padding |
| 3 | Wrap-around | nonzero error for $N < 16$, zero (to rounding) for $N \ge 16 = 12 + 5 - 1$ |
| 4 | Block filtering | both methods match `numpy.convolve` to about $10^{-12}$; cost minimum near $N$ = 1024 |
| 5 | Cyclic prefix | rms error vector 33.9% with no prefix, 3.46% with 3 samples, and zero (to rounding) from 4 samples, overhead 5.88%; wrong decisions (233 and 41 of 25,600) only for prefixes of 0 and 1, because QPSK tolerates small interference that would still eat into the noise margin |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 16-03.a | shortest error-free cyclic prefix for the 5-tap channel | 4 | samples |
| Lab 16-03.b | its overhead with 64 subcarriers | 5.88 | % |
| Lab 16-03.c | rms error vector, no prefix | 33.9 | % |
| Lab 16-03.d | rms error vector, 3-sample prefix | 3.46 | % |
| Lab 16-03.e | wrong decisions, no prefix | 233 | — |
| Lab 16-03.f | wrong decisions, 1-sample prefix | 41 | — |

## Discussion

1. In Part 2, why does zero padding make peaks look sharper without improving resolution?
2. In Part 3, where exactly does the wrapped part of the convolution land, and why?
3. In Part 4, overlap-save throws away part of every block. Why can it still be the more efficient choice in hardware?
4. In Part 5, why does a too-short prefix distort the symbols even without noise, and why do the QPSK decisions survive a prefix of 2 or 3 samples?

### Answers

1. Padding evaluates the same DTFT at more frequencies, so the curve between the original bins is drawn instead of being implied. The DTFT's main-lobe width is set by the 64 real samples (about two original bins wide), so two tones closer than that make one combined lobe, however finely it is sampled.
2. The linear convolution has $L + M - 1$ samples. With $N$ points, samples $N, N + 1, \dots$ have nowhere to go and are added onto indices $0, 1, \dots$ (the convolution is taken modulo $N$), so the first $L + M - 1 - N$ outputs are corrupted by the tail.
3. It needs no output additions and no extra output buffer: every block's kept samples are final. The discarded $M - 1$ outputs cost computation that is already part of the FFT, and the input simply overlaps, which suits streaming memory.
4. Without enough prefix, the receiver's window contains the tail of the previous symbol (inter-symbol interference) and is missing the channel's response to the start of its own symbol, so the convolution is not circular. The subcarriers then leak into each other (inter-carrier interference), and a one-tap equalizer per subcarrier cannot undo it, even with no noise. With 2 or 3 samples of prefix only the last channel taps (0.2 and 0.1) leak, so the distortion is a few percent: QPSK decisions, whose margin is about 70% of the symbol magnitude, survive, but the same interference would cost noise margin and break a dense constellation such as 1024-QAM, whose points are only a few percent apart.

## Optional hardware

With a sound card, play a multitone made of 32 on-bin sinusoids through a speaker and record it with a microphone. Take DFTs of on-bin records, divide by the transmitted spectrum, and you have measured the room's transfer function at 32 frequencies: the same one-tap-per-bin idea as OFDM. Then shift the capture window by a few samples without a prefix and watch the estimate degrade.
