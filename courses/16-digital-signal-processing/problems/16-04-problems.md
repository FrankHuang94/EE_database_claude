# Problems 16-04 · The FFT Algorithm

Chapter: [16-04](../chapters/16-04-the-fft.md) · Worked solutions: [16-04 solutions](../solutions/16-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $W_N = e^{-j2\pi/N}$; "complex multiplications" counts every twiddle product, "non-trivial" excludes $W = 1$ and $W = -j$; a complex multiplication costs four real multiplications unless stated.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 16-04.1 [A]

**Counting.** For $N$ = 256, give the number of stages, butterflies, complex multiplications and non-trivial complex multiplications of a radix-2 FFT, and the ratio of direct-DFT to FFT complex multiplications.

### Problem 16-04.2 [A]

**Bit reversal.** For $N$ = 16, where do input indices 3, 6 and 11 appear in bit-reversed order? Which indices of a 16-point transform stay in place?

### Problem 16-04.3 [A]

**Butterfly spans.** In a 64-point decimation-in-time FFT, how far apart are the two inputs of a butterfly in each stage, and how many distinct twiddle factors does each stage use?

### Problem 16-04.4 [B]

**A four-point FFT.** Compute the DFT of $x = (0, 1, 0, -1)$ with the radix-2 DIT FFT, showing $G$, $H$ and both butterflies.

### Problem 16-04.5 [B]

**Decimation in frequency.** For $x = (1, 1, 1, 1, 0, 0, 0, 0)$, use the DIF split of §3.4: form the sequences that feed the even-bin and odd-bin 4-point DFTs, and compute $X[0]$, $X[1]$, $X[2]$ and $X[3]$.

### Problem 16-04.6 [B]

**Real multipliers.** For a 256-point radix-2 FFT, how many real multiplications do the non-trivial twiddles cost with the four-multiplication complex product, and with a three-multiplication form?

### Problem 16-04.7 [B]

**Radix-4.** Compare the complex multiplications of radix-2 and radix-4 FFTs for $N$ = 1024 and $N$ = 4096 using the counts of §3.2 and §3.6.

### Problem 16-04.8 [B]

**Real data.** A 1024-point FFT of real samples is computed as a 512-point complex FFT plus $N/2$ extra twiddle multiplications. How many complex multiplications is that, and what fraction of the 1024-point complex FFT?

### Problem 16-04.9 [B]

**Inverse by forward.** Use the conjugation trick of §3.6 to compute the inverse DFT of $X = (10, -2 + 2j, -2, -2 - 2j)$ with a forward 4-point FFT.

### Problem 16-04.10 [C]

**A memory-based engine.** A wideband receiver needs continuous 4096-point FFTs of a 250 MS/s stream, using radix-2 butterfly units that each finish one butterfly per cycle at 1 GHz. How many butterflies per transform, what time is available per transform, and how many butterfly units are needed?

### Problem 16-04.11 [C]

**A streaming pipeline.** For a 1024-point R2SDF FFT with 16-bit real and imaginary parts, give the butterfly units, general complex multipliers, delay memory in words and in bytes, and the butterfly utilization.

### Problem 16-04.12 [C]

**Word length.** A 4096-point FFT processes 12-bit signed real ADC samples. (a) How many bits must the internal words have to rule out overflow without scaling? (b) With 1/2 scaling at every stage, what output magnitude does a full-scale on-bin cosine (amplitude 2047) produce, and how many bits of the 12-bit output range does it use?

### Problem 16-04.13 [B]

**The overflow that halving misses.** *(lab)* A butterfly of the lab's 8-point Q1.15 FFT (twiddle $W_8^1 = 23170 - j23170$, products rounded by $2^{15}$, outputs halved by an arithmetic shift) receives $b = 26000 + j26000$. (a) Compute $W_8^1b$. (b) For $a = 20000$ (real), compute both outputs before saturation. (c) Find the largest real $a$ for which the sum output stays within 16 bits. (d) Explain why halving every stage does not prevent this overflow.

---

## Objective coverage

| Learning objective (chapter 16-04) | Problems |
|---|---|
| 1. Radix-2 DIT, butterflies, bit reversal | 2, 3, 4 |
| 2. Decimation in frequency | 5 |
| 3. Operation counts, radix-4, real inputs | 1, 6, 7, 8 |
| 4. FFTs by hand; inverse via forward | 4, 5, 9 |
| 5. FFT hardware sizing | 10, 11 |
| 6. Word growth and scaling | 12, 13 |
