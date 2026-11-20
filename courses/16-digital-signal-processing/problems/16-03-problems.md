# Problems 16-03 · The DFT and Its Properties

Chapter: [16-03](../chapters/16-03-the-dft.md) · Worked solutions: [16-03 solutions](../solutions/16-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $X[k] = \sum_{n=0}^{N-1}x[n]W_N^{kn}$ with $W_N = e^{-j2\pi/N}$ and the $1/N$ on the inverse; sequences are indexed from 0; FFT cost uses the model of §3.7 (16-04 derives it).

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 16-03.1 [A]

**A DFT by inspection.** Compute the 4-point DFT of $x = (1, 0, -1, 0)$. Which analog frequency, as a fraction of $f_s$, is this sequence?

### Problem 16-03.2 [A]

**Bins and frequencies.** A receiver captures $N$ = 4096 samples at $f_s$ = 1 MHz. Find the bin spacing, the (fractional) bin of a 100 kHz tone, and the frequency of bin 4000.

### Problem 16-03.3 [A]

**Using the properties.** With $x = (1, 2, 3, 4)$ and its DFT from Example 16-03.1, use the properties of §3.4 (not a new DFT) to find the DFT of (a) $(4, 1, 2, 3)$ and (b) $(-1)^nx[n]$.

### Problem 16-03.4 [B]

**Circular convolution by hand.** Compute the 4-point circular convolution of $x = (1, 2, 0, 1)$ and $h = (1, -1, 0, 0)$ directly from the definition, and check it by multiplying DFTs.

### Problem 16-03.5 [B]

**One FFT for one convolution.** A 200-sample record is to be filtered by a 57-tap FIR filter with a single DFT product. What is the smallest DFT length that gives the linear convolution, and the smallest power of 2?

### Problem 16-03.6 [B]

**How finely to sample a spectrum.** The DTFT of $h[n] = 0.9^nu[n]$ is sampled at $N$ points and inverse-transformed. Find the relative error of the first sample as a function of $N$, and the smallest $N$ that keeps it below 1%.

### Problem 16-03.7 [B]

**Reading amplitude and power.** A cosine of amplitude 2 V completes exactly 100 cycles in an $N$ = 2048-sample record. Find $\lvert X[100]\rvert$ and $\lvert X[1948]\rvert$, the signal's mean-square value, and check Parseval's relation.

### Problem 16-03.8 [B]

**On-bin and off-bin.** At $f_s$ = 1 kHz with $N$ = 1000, compare the largest DFT magnitude of unit cosines at 50 Hz and 50.5 Hz, relative to the on-bin value $N/2$, and in dB. Compare with the long-record limit $2/\pi$.

### Problem 16-03.9 [B]

**Overlap-add bookkeeping.** A 33-tap filter processes a 10,000-sample signal by overlap-add with 128-point FFTs. Find the block length, the number of blocks, the overlap between consecutive block outputs, and the length of the full output.

### Problem 16-03.10 [C]

**A long filter.** Using the cost model of §3.7, find the best power-of-2 FFT size for a 255-tap filter, its cost per output sample, the saving over direct convolution, and the block length.

### Problem 16-03.11 [C]

**Reading a spectrum.** $x[n] = \cos(2\pi \cdot 3n/16) + 0.5\sin(2\pi \cdot 5n/16)$, $N$ = 16. Find every nonzero DFT bin without computing a full DFT.

### Problem 16-03.12 [C]

**Sizing a cyclic prefix.** An OFDM link samples at 20 MHz and uses a 64-point DFT. (a) Its channel's impulse response spans 17 samples. What is the shortest cyclic prefix, what delay spread is that in microseconds, and what fraction of airtime does it cost? (b) For a 9-tap channel, compare the prefix overhead with a 64-point and a 256-point DFT.

---

## Objective coverage

| Learning objective (chapter 16-03) | Problems |
|---|---|
| 1. Compute DFTs; orthogonality; Parseval | 1, 7, 11 |
| 2. Bins as DTFT samples; time aliasing | 2, 6, 8 |
| 3. Properties and the circular convolution theorem | 3, 4, 11 |
| 4. Linear via circular convolution; zero padding | 4, 5 |
| 5. Overlap-add and overlap-save; cost | 9, 10 |
| 6. Cyclic prefix | 12 |
