<!-- status: verified -->
# 16-03 · The DFT and Its Properties

| | |
|---|---|
| **Course** | [16 · Digital Signal Processing](../README.md) |
| **University equivalent** | The discrete Fourier transform chapter of a senior DSP course: the DFT as samples of the DTFT, its properties, circular convolution, zero padding, and linear convolution by blocks (Oppenheim & Schafer, *Discrete-Time Signal Processing*, ch. 8; Lyons, *Understanding Digital Signal Processing*, ch. 3) |
| **Prerequisites** | [16-02 DTFT and z-Transform for DSP](16-02-dtft-and-z-transform-for-dsp.md), [11-07 Discrete-Time Fourier Transform](../../11-signals-and-systems/chapters/11-07-discrete-time-fourier-transform.md), [11-05 Fourier Series](../../11-signals-and-systems/chapters/11-05-fourier-series.md), [02-06 Vectors, Matrices and Linear Systems](../../02-complex-numbers-des-and-linear-algebra/chapters/02-06-vectors-matrices-and-linear-systems.md) |
| **Estimated study hours** | 8 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Compute small DFTs by hand and by matrix, prove the inverse from the orthogonality of the DFT basis, and check results with Parseval's relation.
2. Interpret DFT bins as samples of the DTFT: convert bin index to frequency, predict which bin a tone lands in, and explain time aliasing when the spectrum is undersampled.
3. Apply the DFT's properties (linearity, circular shift, modulation, conjugate symmetry, Parseval) and the circular convolution theorem.
4. Choose a DFT length that makes circular convolution equal linear convolution, and explain what zero padding does and does not add.
5. Implement linear filtering of long signals with overlap-add and overlap-save, and estimate when it beats direct convolution.
6. Explain why OFDM systems add a cyclic prefix, and size it from the channel's length.

---

## 1. Big picture

The DTFT of 16-02 is a continuous function of frequency: beautiful for analysis, impossible to store in a computer. The **discrete Fourier transform** (DFT) keeps only $N$ samples of it, and in return gets an exact, invertible map between $N$ numbers in time and $N$ numbers in frequency that a processor can compute, especially with the fast algorithm of 16-04. Almost every spectrum you will ever see on an instrument, and a large share of all filtering in modern communication chips, goes through a DFT. The price is a set of subtleties: the DFT treats every signal as if it repeated forever, so shifts and convolutions "wrap around", and a spectrum sampled too coarsely aliases in time. This chapter makes those effects precise and turns them into tools.

- **Spectrum analysis.** Oscilloscopes, spectrum analyzers and ADC test benches compute DFTs of captured records (16-05).
- **Fast filtering.** Long FIR filters (room reverberation, channel emulation, matched filters in radar) run as products of DFTs in blocks, faster than direct convolution.
- **OFDM.** Wi-Fi, LTE and 5G, DSL and cable modems put data on DFT bins; a cyclic prefix makes the channel's convolution circular, so each bin sees one complex gain.
- **Radar and imaging.** FMCW automotive radar computes range with a DFT across each chirp and velocity with a second DFT across chirps.

## 2. Intuition first

**A set of tuning forks that fit the window.** Take a record of $N$ samples. The DFT asks: how much of each sinusoid that completes exactly $k$ whole cycles in the window is present, for $k = 0, 1, \dots, N - 1$? Those $N$ sinusoids are mutually orthogonal over the window (like perpendicular axes), so the answer for each is found by a single correlation, and together they rebuild the record exactly. A tone that also completes a whole number of cycles in the window lands in one bin. A tone that does not falls between the forks and is shared among several bins: **leakage**, the subject of 16-05.

**Everything wraps around.** Because the forks are periodic with period $N$, the DFT cannot tell the window from an infinite repetition of it. Push a signal past the right edge and it reappears on the left: a **circular shift**. Convolve two windows and the tail of the result wraps onto the start: **circular convolution**. Pad the window with enough zeros and there is nothing to wrap, so circular convolution becomes ordinary convolution.

**Analogy: a price series sampled at month ends.** A monthly sampling of a yearly cycle can show the seasonal pattern, but a 13-month cycle sampled for 12 months does not fit the window, and its energy smears across "frequencies". Where the analogy breaks: financial series are not periodic, and the DFT's implicit repetition (December followed by the same January) is a modelling artifact a finance analyst would never accept for prices. The DSP engineer accepts it knowingly, and manages it with windows (16-05) and padding.

## 3. Theory

### 3.1 Definition, inverse and orthogonality

For a sequence $x[0], \dots, x[N-1]$, the $N$-point DFT is

$$
X[k] = \sum_{n=0}^{N-1}x[n]\,W_N^{kn}, \qquad W_N = e^{-j2\pi/N}, \qquad k = 0, 1, \dots, N - 1 ,
$$

and the inverse DFT is

$$
x[n] = \frac{1}{N}\sum_{k=0}^{N-1}X[k]\,W_N^{-kn} .
$$

**Why the inverse works.** Substitute the forward transform into the inverse:

$$
\frac1N\sum_{k}\sum_{m}x[m]W_N^{km}W_N^{-kn} = \sum_m x[m]\,\frac1N\sum_{k=0}^{N-1}W_N^{k(m - n)} .
$$

The inner sum is a geometric series with ratio $r = W_N^{m-n}$. If $m - n$ is a multiple of $N$, $r = 1$ and the sum is $N$. Otherwise $r \ne 1$ and $r^N = e^{-j2\pi(m - n)} = 1$, so the sum is $(1 - r^N)/(1 - r) = 0$. So $\frac1N\sum_kW_N^{k(m-n)} = 1$ if $m = n$ and 0 otherwise (for $m$ and $n$ in $0..N-1$), and the double sum collapses to $x[n]$. This is the **orthogonality** of the DFT basis vectors $e_k[n] = W_N^{-kn}$: their inner products are $N$ when $k = l$ and 0 otherwise.

> **Math refresher — the DFT as a matrix.** Collect the samples into a vector $\mathbf x$ and the transform into $\mathbf X$. Then $\mathbf X = \mathbf F\mathbf x$ with $F_{kn} = W_N^{kn}$, and orthogonality says $\mathbf F^H\mathbf F = N\mathbf I$, so $\mathbf F^{-1} = \mathbf F^H/N$ (02-06, 02-08). The matrix $\mathbf F/\sqrt N$ is unitary: a rotation of $N$-dimensional complex space. A direct matrix–vector product costs $N^2$ complex multiplies; 16-04's FFT factors $\mathbf F$ into sparse matrices and costs about $(N/2)\log_2N$.

**Parseval's relation.** Because $\mathbf F/\sqrt N$ is unitary, it preserves length:

$$
\sum_{n=0}^{N-1}\lvert x[n]\rvert^2 = \frac1N\sum_{k=0}^{N-1}\lvert X[k]\rvert^2 .
$$

Energy can be counted in either domain; this is how spectrum analyzers report total power and how 16-05 measures noise.

### 3.2 The DFT samples the DTFT

Compare the DFT with the DTFT of the same finite sequence, $X(e^{j\omega}) = \sum_{n=0}^{N-1}x[n]e^{-j\omega n}$ (16-02). At $\omega = 2\pi k/N$ the two sums are identical:

$$
X[k] = X(e^{j\omega})\big|_{\omega = 2\pi k/N} .
$$

The DFT is the DTFT sampled at $N$ equally spaced frequencies around the unit circle. For data sampled at $f_s$, bin $k$ sits at

$$
f_k = \frac{k f_s}{N}\quad\text{for } k < N/2, \qquad f_k = \frac{(k - N) f_s}{N}\quad\text{for } k > N/2 ,
$$

because the DTFT is periodic and bins above $N/2$ are the negative frequencies. The **bin spacing** $f_s/N$ is the reciprocal of the record length $NT$: a one-second record gives 1 Hz bins, whatever the sample rate.

**A tone that fits the window.** $x[n] = A\cos(2\pi k_0n/N)$ with integer $k_0$ completes $k_0$ cycles. Writing the cosine as two exponentials and using orthogonality, $X[k_0] = X[N - k_0] = AN/2$ and every other bin is exactly zero. A tone at a non-integer bin is not orthogonal to any basis vector, and its energy spreads over all bins (Example 16-03.2).

![Two panels. Left: the DTFT magnitude of a 16-sample Hann-shaped pulse from 0 to 2 pi, a smooth low-pass curve peaking at 8.5 at 0 and 2 pi and near zero in between; open circles mark the 16-point DFT values, which lie exactly on the curve at multiples of 2 pi/16, and small dots mark a 64-point zero-padded DFT, which fills in the same curve four times more densely. Right: 1024-point DFT magnitudes in dB relative to N/2 for bins 0 to 80 at fs = 48 kHz: a 3 kHz cosine gives a single line at 0 dB in bin 64 and nothing elsewhere, while a 1 kHz cosine at bin 21.33 peaks at -1.7 dB in bin 21 and leaks into every bin, falling to about -37 dB at bin 0 and -44 dB at bin 80.](../../../assets/figures/16-03/dft-samples.svg)

*Figure 1. Left: DFT samples lie on the DTFT; zero padding samples the same curve more finely (§3.6). Right: an on-bin tone occupies one bin; an off-bin tone leaks into all of them (Example 16-03.2).*

**For real signals the spectrum is conjugate-symmetric:** $X[N - k] = X^*[k]$, so bins $0$ to $N/2$ carry all the information. Bin 0 is the sum (DC); for even $N$, bin $N/2$ is the alternating sum, at $f_s/2$.

### 3.3 Sampling the spectrum aliases in time

What if the sequence is longer than $N$, or infinite, and we still take $N$ samples of its DTFT? Sampling in time aliased the spectrum (11-10); sampling in frequency aliases the time signal. Let $\tilde x[n]$ be the inverse DFT of $X(e^{j2\pi k/N})$. Substituting the DTFT and using the orthogonality sum of §3.1, which picks out every $m$ congruent to $n$ modulo $N$,

$$
\tilde x[n] = \frac1N\sum_k\sum_m x[m]e^{-j2\pi km/N}e^{j2\pi kn/N} = \sum_{r=-\infty}^{\infty}x[n + rN], \qquad 0 \le n \le N - 1 .
$$

The record is folded onto itself every $N$ samples. If $x$ has length at most $N$, nothing overlaps and $\tilde x = x$; otherwise the tail adds onto the beginning (Example 16-03.4). This is the reason a spectrum must be sampled at least as finely as the reciprocal of the signal's duration, the frequency-domain twin of the Nyquist rate.

### 3.4 Properties

With $((m))_N$ denoting $m$ modulo $N$:

| Property | Time | DFT |
|---|---|---|
| Linearity | $ax[n] + by[n]$ | $aX[k] + bY[k]$ |
| Circular shift | $x[((n - m))_N]$ | $W_N^{km}X[k]$ |
| Modulation | $W_N^{-ln}x[n]$ | $X[((k - l))_N]$ |
| Conjugate symmetry (real $x$) | $x[n]$ real | $X[((-k))_N] = X^*[k]$ |
| Circular time reversal | $x[((-n))_N]$ | $X[((-k))_N]$ |
| Circular convolution | $y_c[n] = \sum_m h[m]x[((n - m))_N]$ | $X[k]H[k]$ |
| Parseval | $\sum\lvert x\rvert^2$ | $\frac1N\sum\lvert X\rvert^2$ |

*Proof of the shift property.* $\sum_n x[((n - m))_N]W_N^{kn}$: substitute $p = ((n - m))_N$, so $n \equiv p + m$ and $W_N^{kn} = W_N^{k(p + m)}$ because $W_N^{kN} = 1$. The sum becomes $W_N^{km}\sum_p x[p]W_N^{kp}$. The shift is circular because the DFT only knows the window: a sample pushed past $N - 1$ comes back at 0.

### 3.5 Circular convolution

Define the $N$-point **circular convolution**

$$
y_c[n] = \sum_{m=0}^{N-1}h[m]\,x[((n - m))_N] ,
$$

written $y_c = x \circledast h$.

**Theorem.** Its DFT is $X[k]H[k]$. *Proof:* take the DFT, swap the sums, and apply the shift property to $x[((n - m))_N]$:

$$
\sum_n\sum_m h[m]x[((n - m))_N]W_N^{kn} = \sum_m h[m]\,W_N^{km}X[k] = H[k]X[k] .
$$

Multiplying DFTs therefore convolves *circularly*, not linearly: the part of the linear convolution that would extend beyond $N - 1$ wraps around and adds onto the start (Example 16-03.3). **The fix is zero padding.** Linear convolution of a length-$L$ input with a length-$M$ filter has length $L + M - 1$. If both are padded with zeros to $N \ge L + M - 1$, nothing reaches past the window, nothing wraps, and

$$
x * h = \text{IDFT}_N\{\text{DFT}_N\{x\}\cdot\text{DFT}_N\{h\}\}\quad\text{when } N \ge L + M - 1 .
$$

![Two stem plots for Example 16-03.3. Left: the linear convolution of (1, 2, 3) with (1, 1), values 1, 3, 5, 3 at n = 0 to 3, with the last sample highlighted. Right: the 3-point circular convolution, values 4, 3, 5; the value 4 at n = 0 is drawn as a stacked bar of 1 from the linear result at n = 0 plus 3 wrapped around from n = 3.](../../../assets/figures/16-03/circular.svg)

*Figure 2. Circular convolution wraps the tail of the linear convolution onto its start (Example 16-03.3).*

### 3.6 Zero padding: finer sampling, not finer resolution

Padding a length-$L$ record with zeros to length $N > L$ leaves its DTFT unchanged (zeros add nothing to the sum) and samples that DTFT more densely, at spacing $2\pi/N$ instead of $2\pi/L$. Peaks are located more precisely and the plot looks smoother. But the DTFT itself is set by the $L$ real samples: two tones closer than about one bin of the *unpadded* record, $f_s/L$, blur into one peak whatever $N$ is. **Resolution comes from record length; padding only interpolates.** 16-05 makes this quantitative with windows.

### 3.7 Long filters: overlap-add and overlap-save

A streaming input is too long for one DFT, so it is cut into blocks.

- **Overlap-add.** Split $x$ into blocks of $L$ samples. Convolve each block with $h$ (length $M$) by $N$-point DFTs with $N \ge L + M - 1$, so each block's linear convolution is exact; each result is $L + M - 1$ long, so consecutive results overlap by $M - 1$ samples, and are **added** there.
- **Overlap-save.** Take overlapping input blocks of $N$ samples, each starting $L = N - M + 1$ samples after the previous one. The $N$-point circular convolution of a block with $h$ is correct except for its first $M - 1$ outputs, which are corrupted by wrap-around; **discard** them and keep the last $L$.

Both produce exactly the linear convolution. Per block they need one forward DFT of the input, one product with the precomputed $H[k]$, and one inverse DFT, and they deliver $L = N - M + 1$ new outputs. With the radix-2 FFT's $(N/2)\log_2N$ complex multiplies per transform (16-04) and four real multiplies per complex one, the cost per output sample is

$$
C(N, M) = \frac{4\left[N\log_2N + N\right]}{N - M + 1}\ \text{real multiplies},
$$

against $M$ for direct convolution. Large $N$ amortizes the overhead but each FFT grows; the best $N$ is typically a few times $M$ (Example 16-03.5). The price is **latency**: a block of $L$ samples must arrive before any of its outputs can be computed.

### 3.8 The cyclic prefix: making a channel circular

OFDM (orthogonal frequency-division multiplexing) puts one data symbol on each DFT bin, forms the time signal with an inverse DFT, and recovers the symbols at the receiver with a DFT. The radio or cable channel convolves the transmitted signal *linearly* with its impulse response $c[n]$ of length $M$. If the receiver's DFT saw a *circular* convolution, the theorem of §3.5 would give $Y[k] = C[k]X[k]$: each bin multiplied by one complex number, undone by one complex division (a one-tap equalizer per subcarrier). The trick is to copy the last $G$ samples of each $N$-sample symbol to its front before transmission: the **cyclic prefix**. If $G \ge M - 1$, then over the $N$ samples the receiver keeps (discarding the prefix), every delayed copy of the symbol that the channel adds looks exactly like a circular shift, because the samples that "fall off the end" were placed at the start in advance. Linear convolution with a periodically extended input is circular convolution. The prefix also absorbs the tail of the previous symbol, so symbols do not interfere. Its cost is overhead: a fraction $G/(N + G)$ of the airtime carries no new data (Problem 16-03.12).

## 4. Worked examples

### Example 16-03.1 · A four-point DFT by hand (tier A)

**Setup.** Compute the 4-point DFT of $x = (1, 2, 3, 4)$, check it with Parseval's relation, and verify the conjugate symmetry.

**Solution.** $W_4 = e^{-j\pi/2} = -j$, so the powers $W_4^{kn}$ cycle through $1, -j, -1, j$.

- $X[0] = 1 + 2 + 3 + 4$ = **10**.
- $X[1] = 1 + 2(-j) + 3(-1) + 4(j) = -2 + 2j$.
- $X[2] = 1 - 2 + 3 - 4$ = **−2**.
- $X[3] = 1 + 2(j) + 3(-1) + 4(-j) = -2 - 2j$.

Conjugate symmetry: $X[3] = X^*[1]$, as it must be for real $x$. Parseval: $\sum x^2 = 1 + 4 + 9 + 16$ = **30**, and $\frac14(100 + 8 + 4 + 8) = 30$.

**Units check.** $X[k]$ has the units of $x$ (a sum of samples).

**Sanity check.** $X[0]$ is the sum and $X[N/2]$ the alternating sum, as §3.2 says.

### Example 16-03.2 · Which bin, and how much leaks? (tier B)

**Setup.** An audio analyzer takes $N$ = 1024-point DFTs of data sampled at 48 kHz. (a) What is the bin spacing? (b) A unit-amplitude 3 kHz cosine: which bin, and what is $\lvert X\rvert$ there? (c) A unit-amplitude 1 kHz cosine: between which bins does it fall, and how large is the biggest bin compared with (b)?

**Solution.** (a) $f_s/N = 48{,}000/1024$ = **46.875** Hz, set by the record length of 21.3 ms.

(b) $3000/46.875$ = **64** exactly: the tone completes 64 cycles in the record. All its energy is in bins 64 and $1024 - 64 = 960$, each of magnitude $AN/2$ = **512**; every other bin is zero to rounding.

(c) $1000/46.875$ = **21.33**: between bins 21 and 22, nearer 21. The largest bin, 21, has magnitude 422.2, which is **0.825** of the on-bin value, or **−1.68** dB (the "scalloping loss"); bin 22 holds 0.416 of it, and the rest is spread thinly across the spectrum. A spectrum analyzer that reported the biggest bin as the tone's amplitude would read 1.7 dB low, which is why analyzers use windows with flatter peaks (16-05).

**Units check.** Hz/(Hz per bin) = bins.

**Sanity check.** Parseval for (b): the tone's energy $\sum\cos^2 = N/2 = 512$ equals $\frac1N(512^2 + 512^2) = 512$.

### Example 16-03.3 · Circular against linear convolution (tier B)

**Setup.** $x = (1, 2, 3)$ and $h = (1, 1)$. Find the linear convolution, the 3-point circular convolution, and the smallest $N$ for which circular equals linear.

**Solution.** Linear: $(1, 3, 5, 3)$, length $3 + 2 - 1 = 4$. Circular with $N$ = 3: the fourth term (3) wraps onto index 0, giving $(1 + 3, 3, 5)$ = **(4, 3, 5)**. Directly from the definition, $y[0] = h[0]x[0] + h[1]x[((-1))_3] = 1 + x[2] = 4$. With $N \ge 4$ = **4** there is no wrap: the 4-point circular convolution of the zero-padded sequences is $(1, 3, 5, 3)$.

**Units check.** Products of samples and coefficients.

**Sanity check.** The circular result sums to $4 + 3 + 5 = 12$, the same as the linear one ($1 + 3 + 5 + 3$): wrapping moves samples, it does not lose them.

### Example 16-03.4 · Time aliasing from an undersampled spectrum (tier B)

**Setup.** $x[n] = 0.5^nu[n]$ has DTFT $1/(1 - 0.5e^{-j\omega})$. Sample the DTFT at $N$ = 4 frequencies and inverse-DFT. What comes out, and why?

**Solution.** By §3.3, the result is $\tilde x[n] = \sum_r 0.5^{n + 4r}$ over $r \ge 0$, a geometric series: $\tilde x[n] = 0.5^n/(1 - 0.5^4) = 0.5^n/0.9375$. So $\tilde x$ = (**1.0667**, 0.5333, 0.2667, 0.1333): each sample **6.7**% too large, because the infinite tail beyond $n = 3$ has been folded back onto the window. With $N$ = 16 the error would be $1/(1 - 0.5^{16}) - 1 \approx 1.5 \times 10^{-5}$.

**Units check.** Dimensionless.

**Sanity check.** $\tilde x[0] = 1/0.9375$, and inverse-transforming the four samples numerically gives the same values (verify script).

### Example 16-03.5 · When does FFT convolution pay? (tier C)

**Setup.** A 101-tap FIR filter runs on a long audio stream. Using §3.7's cost model, compare direct convolution with overlap-save for FFT sizes from 128 to 4096, find the best FFT size, and give its block latency at 48 kHz. Under the same model, find the shortest filter for which FFT convolution needs fewer multiplies than direct.

**Solution.** Direct convolution: **101** real multiplies per output. Overlap-save with $L = N - 100$:

| $N$ | $L$ | Real multiplies per output |
|---|---|---|
| 128 | 28 | 146.3 |
| 256 | 156 | 59.1 |
| 512 | 412 | 49.7 |
| 1024 | 924 | **48.8** |
| 2048 | 1948 | 50.5 |
| 4096 | 3996 | 53.3 |

The best size is $N$ = **1024**, about **2.07** times fewer multiplies than direct. Its blocks are 924 samples, **19.25** ms at 48 kHz, before any processing time. Searching the model over filter lengths, FFT convolution first wins at $M$ = **44** taps (43.3 multiplies per output at its best $N$). In practice the crossover moves lower with real-input FFT tricks (which roughly halve the transform cost) and higher on processors with single-cycle MACs and no FFT accelerator; the model gives the shape of the tradeoff, not a universal threshold.

**Units check.** Multiplies per output sample; latency in samples and ms.

**Sanity check.** At $N = 128$ the block is only 28 samples, so the fixed cost of two FFTs is spread over few outputs: more expensive than direct, as the table shows.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 16-03.1a | X[0] | 10 | — |
| Ex 16-03.1b | X[1] | −2+j2 | — |
| Ex 16-03.1c | X[2] | −2 | — |
| Ex 16-03.1d | X[3] | −2−j2 | — |
| Ex 16-03.1e | energy | 30 | — |
| Ex 16-03.2a | bin spacing | 46.875 | Hz |
| Ex 16-03.2b | bin of 3 kHz | 64 | — |
| Ex 16-03.2c | magnitude at that bin | 512 | — |
| Ex 16-03.2d | bin position of 1 kHz | 21.33 | — |
| Ex 16-03.2e | largest bin relative to on-bin | 0.825 | — |
| Ex 16-03.2f | scalloping loss | −1.68 | dB |
| Ex 16-03.2g | bin 22 relative to on-bin | 0.416 | — |
| Ex 16-03.2h | largest bin magnitude for 1 kHz | 422.2 | — |
| Ex 16-03.2i | record length | 21.3 | ms |
| Ex 16-03.3a | smallest N without wrap | 4 | — |
| Ex 16-03.4a | first aliased sample | 1.0667 | — |
| Ex 16-03.4b | aliasing error with N = 16 | 1.5e-5 | — |
| Ex 16-03.5a | cost, N = 128 | 146.3 | per output |
| Ex 16-03.5b | cost, N = 256 | 59.1 | per output |
| Ex 16-03.5c | cost, N = 512 | 49.7 | per output |
| Ex 16-03.5d | cost, N = 1024 | 48.8 | per output |
| Ex 16-03.5e | cost, N = 2048 | 50.5 | per output |
| Ex 16-03.5f | cost, N = 4096 | 53.3 | per output |
| Ex 16-03.5g | saving at the best N | 2.07 | — |
| Ex 16-03.5h | block latency | 19.25 | ms |
| Ex 16-03.5i | crossover filter length | 44 | taps |
| Ex 16-03.5j | cost at the crossover | 43.3 | per output |
| Ex 16-03.4c | excess of each aliased sample | 6.7 | % |
| Txt 16-03.a | worst-case scalloping, long records | −3.92 | dB |
| Txt 16-03.b | Q1 DC bin of the constant | 8 | — |
| Txt 16-03.c | Q2 frequency of bin 480 | −400 | Hz |
| Txt 16-03.d | Q5 discarded outputs | 63 | — |
| Txt 16-03.e | Q5 kept outputs | 193 | — |
| Txt 16-03.f | Q6 shortest prefix | 4 | samples |
| Txt 16-03.g | shortest exact prefix for the lab's 5-tap channel | 4 | samples |
| Txt 16-03.h | 802.11a/g prefix overhead | 20 | % |
| Txt 16-03.i | LTE normal-prefix overhead per slot | 6.67 | % |
| Txt 16-03.j | NR normal prefix at 240 kHz spacing | 0.293 | µs |

## 5. Simulate it

The lab, [labs/16-03-lab](../labs/16-03-lab/README.md), provides `dft.py`: the DFT from its definition and as a matrix, the DTFT of a finite sequence, bin frequencies, circular shift and circular convolution computed directly, overlap-add and overlap-save, and the FFT-convolution cost model. You:

1. **Build the DFT matrix** for $N$ = 8, check $\mathbf F^H\mathbf F = N\mathbf I$, and compare `dft` with `numpy.fft.fft`.
2. **Watch the DFT sample the DTFT**: overlay the DFT of a short record on its DTFT, then zero-pad and see the samples fill in without new detail.
3. **Wrap a convolution**: compare circular and linear convolution as $N$ grows past $L + M - 1$.
4. **Filter a long signal in blocks** with overlap-add and overlap-save, check both against `numpy.convolve`, and plot the cost model against $N$.
5. **Make a channel circular**: send random QPSK symbols on 64 subcarriers through a 5-tap channel with cyclic prefixes of 0 to 6 samples, equalize each subcarrier with one complex division, and measure the residual distortion.

**Guided exercise (predict, then run).** **Before Part 5,** predict the residual distortion with no noise for prefixes of 0, 3 and 4 samples on the 5-tap channel. (A prefix of at least $M - 1$ = **4** samples makes the one-tap equalizer exact; shorter prefixes leave inter-symbol and inter-carrier interference even without noise, large with no prefix and a few percent with 3 samples.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| DFT length $N$ (record length) | Finer bins ($f_s/N$) and resolution | Longer capture, more latency, more computation | Measurement or algorithm engineer |
| Zero padding | Smoother, better-located peaks | Computation; no new resolution | Algorithm engineer |
| FFT size in block convolution | Fewer multiplies per output, up to an optimum | Block latency ($L$ samples); memory for buffers | DSP architect |
| Overlap-add versus overlap-save | OLA: no discarded work; OLS: no output additions, simpler streaming | OLA needs the overlap additions; OLS computes outputs it throws away | Firmware or hardware designer |
| OFDM cyclic prefix length $G$ | Tolerates channels with delay spread up to $G + 1$ samples | Overhead $G/(N + G)$ of throughput and energy | Standards body, system architect |
| Number of OFDM subcarriers $N$ | Lower overhead for a fixed prefix; flatter per-subcarrier channel | Longer symbols: more latency, more sensitivity to frequency offset and Doppler | Standards body |

## 7. Numbers to know

| Quantity | Value | Source |
|---|---|---|
| Bin spacing | $f_s/N$ = 1 / record length | §3.2 |
| On-bin tone of amplitude $A$ | $\lvert X[k_0]\rvert = AN/2$ in each of bins $k_0$ and $N - k_0$ | §3.2 |
| Worst-case scalloping (rectangular window, tone halfway between bins) | −3.92 dB ($2/\pi$) for long records | 16-05 preview; Example 16-03.2 shows −1.68 dB at a third of a bin; Problem 16-03.8 |
| Circular = linear convolution | $N \ge L + M - 1$ | §3.5 |
| Direct DFT against FFT | $N^2$ against about $(N/2)\log_2N$ complex multiplies | §3.1, 16-04 |
| FFT convolution crossover (simple model) | 44 taps; best FFT size a few times the filter length | Example 16-03.5 |

## 8. Common mistakes

- **Reading bins above $N/2$ as high positive frequencies.** They are the negative frequencies.
- **Expecting zero padding to separate close tones.** It interpolates the same DTFT; only a longer record resolves them.
- **Multiplying DFTs and expecting linear convolution.** Without $N \ge L + M - 1$ the result wraps.
- **Forgetting the $1/N$** (or the $N/2$ for a real tone) when reading amplitudes off a DFT; libraries differ in where they put the scaling.
- **Reading a tone's amplitude from the largest bin** when the tone is off-bin: the scalloping loss can be several dB.
- **Sampling a spectrum too coarsely** (fewer points than the impulse response length) and being surprised by time aliasing.
- **Making the OFDM cyclic prefix shorter than the channel's delay spread.** The subcarriers stop being independent and a one-tap equalizer no longer works.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **OFDM is the dominant physical layer for wireless and wireline broadband.** Wi-Fi, LTE and 5G NR, DSL and DOCSIS cable all use DFT-based multicarrier modulation with a cyclic prefix, because it turns equalization of a long channel into one complex multiply per subcarrier **[Established; textbook]**. The numbers show the design tradeoff of §3.8 (R-236) **[Established]**:
  - *802.11a/g Wi-Fi* uses a 64-point FFT at 20 MHz: 312.5 kHz subcarrier spacing, 48 data and 4 pilot subcarriers, a 3.2 µs useful symbol and a 0.8 µs (16-sample) guard interval, for a 4.0 µs symbol and **20**% prefix overhead. 802.11n added an optional 0.4 µs short guard interval for short indoor channels.
  - *LTE* uses 15 kHz subcarriers (a 2048-point FFT at 30.72 MHz): a 66.7 µs useful symbol and normal cyclic prefixes of 160 and 144 samples (5.2 and 4.7 µs), an overhead of **6.67**% of each 0.5 ms slot. The prefix tolerates about six times the delay spread of Wi-Fi's, because outdoor cells have far longer echoes.
  - *5G NR* scales the LTE numerology by $2^\mu$: subcarrier spacings of 15 × $2^\mu$ kHz for $\mu$ = 0 to 6 (15 to 960 kHz), with the normal prefix shrinking as $2^{-\mu}$, so the same 144-sample prefix lasts **0.293** µs at 240 kHz spacing. Wider spacing buys shorter symbols, lower latency and robustness to phase noise and Doppler at high carrier frequencies, at the price of tolerating less delay spread; an extended prefix is defined only at 60 kHz.
- **Spectrum analysis is DFT-based.** Modern signal and spectrum analyzers digitize an IF or baseband signal and compute FFTs of windowed records; real-time analyzers overlap and process records continuously so that short events are not missed between captures **[Established; textbook]**.
- **Long filters run in the frequency domain.** Convolution reverbs, acoustic echo cancellers and channel emulators with thousands of taps use partitioned overlap-save (the filter itself split into blocks to keep latency low) **[Established; textbook]**.

### Why it matters commercially

The DFT is where DSP meets silicon area and power most directly. A Wi-Fi or 5G baseband spends a large share of its digital datapath on FFTs and per-subcarrier processing, and the FFT size, word length and number of parallel streams set its area. In radar SoCs for cars, range and Doppler FFTs dominate the on-chip compute and memory. When a company claims a cheaper baseband or radar chip, the questions are about FFT throughput, memory for the data cube, and word length: the same four currencies as 16-01, applied to the most-used DSP kernel.

### Marketing vs Reality

- **"Frequency resolution of X Hz."** Often quoted from the bin spacing after zero padding. True resolution is set by the record length (and the window); ask for the unpadded record length.
- **"Measures amplitude to 0.1 dB."** Only for on-bin tones or with a flat-top window; an off-bin tone with a rectangular window can read nearly 4 dB low.
- **"Zero-latency convolution reverb / echo canceller."** FFT block processing adds at least one block of latency; low-latency products use partitioned convolution with small first blocks, trading computation for latency.
- **"Our OFDM link has no equalizer."** It has one complex divide per subcarrier, which works only because of the cyclic prefix; ask what happens when the delay spread exceeds the prefix.

### Questions for engineering leaders

1. **"What sets the frequency resolution of this measurement, and is it the bin spacing or the record length?"** *Strong:* distinguishes them and names the window. *Evasive:* quotes the padded bin spacing.
2. **"How do you choose the FFT size for block filtering, and what latency does it cost?"** *Strong:* shows the cost-versus-$N$ curve and the latency budget. *Evasive:* "we use the biggest FFT that fits".
3. **"What delay spread does your cyclic prefix tolerate, and what happens beyond it?"** *Strong:* gives the prefix in microseconds and samples, the target channels, and the degradation mechanism (inter-symbol and inter-carrier interference). *Evasive:* "the standard takes care of it".
4. **"What fraction of baseband area and power is FFT and per-subcarrier processing?"** *Strong:* gives a breakdown and how it scales with bandwidth and streams. *Evasive:* no breakdown.
5. **"How do you scale amplitudes out of your FFT, and how was the scaling verified?"** *Strong:* states the convention (1/N, 1/√N, none) and a calibration with a known tone. *Evasive:* unsure where the factors of N go.

## 10. Concept check

**Q1.** What is the 8-point DFT of $x = (1, 0, 0, 0, 0, 0, 0, 0)$, and of $x = (1, 1, 1, 1, 1, 1, 1, 1)$?

<details><summary>Answer</summary>

The unit sample has $X[k] = 1$ for all $k$ (flat spectrum). The constant has $X[0] = 8$ and $X[k] = 0$ for $k \ne 0$ (all energy at DC).

</details>

**Q2.** At $f_s$ = 10 kHz with $N$ = 500, which frequency does bin 480 represent?

<details><summary>Answer</summary>

$k > N/2$, so it is a negative frequency: $(480 - 500) \times 10{,}000/500$ = −400 Hz.

</details>

**Q3.** Why does multiplying two DFTs give circular, not linear, convolution?

<details><summary>Answer</summary>

The DFT treats each sequence as one period of a periodic signal; shifts are modulo $N$, so the convolution of two periodic sequences wraps the tail past $N - 1$ back onto the start. Zero padding to $N \ge L + M - 1$ leaves nothing to wrap.

</details>

**Q4.** You zero-pad a 100-sample record to 4096 points. Can you now separate two tones 0.2 bins apart in the original (100-point) bin spacing?

<details><summary>Answer</summary>

No. Padding samples the same DTFT more finely; that DTFT is set by the 100 samples and blurs tones closer than about one 100-point bin. A longer record is needed.

</details>

**Q5.** In overlap-save with a 64-tap filter and 256-point FFTs, how many outputs of each block are discarded and how many kept?

<details><summary>Answer</summary>

$M - 1$ = 63 are corrupted by wrap-around and discarded; $N - M + 1$ = 193 are kept.

</details>

**Q6.** An OFDM system has a 5-tap channel. What is the shortest cyclic prefix that makes the channel look circular?

<details><summary>Answer</summary>

$M - 1$ = 4 samples.

</details>

Practice: [Problems 16-03](../problems/16-03-problems.md) · [Solutions](../solutions/16-03-solutions.md)

## 11. Key terms

[Discrete Fourier transform (DFT)](../../../reference/glossary.md#discrete-fourier-transform-dft) · [DFT bin](../../../reference/glossary.md#dft-bin) · [Circular shift](../../../reference/glossary.md#circular-shift) · [Circular convolution](../../../reference/glossary.md#circular-convolution) · [Zero padding](../../../reference/glossary.md#zero-padding) · [Time aliasing](../../../reference/glossary.md#time-aliasing) · [Parseval's relation](../../../reference/glossary.md#parsevals-relation) · [Spectral leakage](../../../reference/glossary.md#spectral-leakage) · [Scalloping loss](../../../reference/glossary.md#scalloping-loss) · [Overlap-add](../../../reference/glossary.md#overlap-add) · [Overlap-save](../../../reference/glossary.md#overlap-save) · [OFDM](../../../reference/glossary.md#ofdm) · [Cyclic prefix](../../../reference/glossary.md#cyclic-prefix)

## 12. Connections

- **Builds on:** [16-02](16-02-dtft-and-z-transform-for-dsp.md) (the DTFT and frequency response), [11-05 Fourier Series](../../11-signals-and-systems/chapters/11-05-fourier-series.md) (orthogonal harmonics), [11-07 DTFT](../../11-signals-and-systems/chapters/11-07-discrete-time-fourier-transform.md), [11-10 Sampling](../../11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md) (aliasing, now in time), [02-06 Vectors and Matrices](../../02-complex-numbers-des-and-linear-algebra/chapters/02-06-vectors-matrices-and-linear-systems.md).
- **Next:** [16-04 The FFT Algorithm](16-04-the-fft.md) computes the DFT in $O(N\log N)$.
- **Used later:** windows, leakage and resolution in [16-05](16-05-spectral-analysis-and-windowing.md); frequency-sampling FIR design in [16-06](16-06-fir-filter-design.md); polyphase filter banks in [16-09](16-09-multirate-dsp.md); OFDM in Course 17.

## 13. Further study

- Oppenheim & Schafer, *Discrete-Time Signal Processing*, 3rd ed., ch. 8 (the DFT, its properties, circular convolution, linear convolution with the DFT).
- Lyons, *Understanding Digital Signal Processing*, 3rd ed., ch. 3 (the DFT, leakage, zero padding) and ch. 13 (fast convolution).
- MIT OCW 6.341 *Discrete-Time Signal Processing* (Fall 2005), lectures on the DFT and block convolution.

## 14. Sources

1. A. V. Oppenheim and R. W. Schafer, *Discrete-Time Signal Processing*, 3rd ed., Pearson, 2010, ch. 8.
2. R. G. Lyons, *Understanding Digital Signal Processing*, 3rd ed., Prentice Hall, 2011, ch. 3.
3. 3GPP TS 36.211 (LTE) and TS 38.211 (NR) physical channels and modulation, Rel-19, as published by ETSI (TS 136 211 V19.3.0, TS 138 211 V19.5.0); IEEE 802.11 document 11-05/1102r4 (OFDM timing parameters of 802.11a/g and 802.11n). Research log [R-236].
