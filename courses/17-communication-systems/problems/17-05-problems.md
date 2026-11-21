# Problems 17-05 · Matched Filters and Optimal Detection

Chapter: [17-05](../chapters/17-05-matched-filters-and-detection.md) · Worked solutions: [17-05 solutions](../solutions/17-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** White Gaussian noise has two-sided PSD $N_0/2$, so each signal-space dimension carries noise variance $N_0/2$. $Q(x)$ is the Gaussian tail probability. Problems marked *(lab)* can be checked with the lab's `detection.py` or an equivalent tool.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 17-05.1 [A]

**A ramp pulse.** $s(t) = At/T$ for $0 \le t < T$, with $A$ = 2 V and $T$ = 3 µs, in white noise with $N_0$ = $10^{-7}$ V²/Hz. Find the matched filter's impulse response, the pulse energy and the peak output SNR in dB.

### Problem 17-05.2 [A]

**BPSK error rates.** Compute the BPSK bit-error rate at $E_b/N_0$ = 0, 4, 7 and 9.6 dB.

### Problem 17-05.3 [A]

**Required $E_b/N_0$.** What $E_b/N_0$ does BPSK need for bit-error rates of $10^{-3}$, $10^{-9}$ and $10^{-12}$?

### Problem 17-05.4 [B]

**Integrate-and-dump with a timing error.** *(lab)* An integrate-and-dump receiver for rectangular antipodal pulses integrates over a window shifted by a quarter of a symbol. Ignoring the neighbouring symbol, what SNR loss does the shorter overlap cause? Including a random neighbouring symbol that now falls partly in the window, what is the worst-case eye opening relative to the ideal?

### Problem 17-05.5 [B]

**Gram–Schmidt with four signals.** *(lab)* On $[0, 1)$: $s_1 = 1$; $s_2 = 1$ on the first half, 0 on the second; $s_3 = 0$ then 1; $s_4 = s_2 - s_3$. Find the dimension of the signal space, an orthonormal basis, the four vectors, and the distances $d_{23}$ and $d_{14}$.

### Problem 17-05.6 [B]

**Union bound for four points.** Four equally likely points at $(\pm a, \pm a)$ have $E_s = 2a^2$. At $E_s/N_0$ = 10 dB, compute the exact symbol-error probability, the union bound and the nearest-neighbour approximation.

### Problem 17-05.7 [B]

**MAP with mild priors.** Antipodal signals $\pm1$ in noise with $N_0$ = 1, with $P(+1)$ = 0.6. Find the MAP threshold and the MAP and ML error probabilities.

### Problem 17-05.8 [B]

**M-PAM requirements.** Find the $E_s/N_0$ that 2-, 4- and 8-PAM need for a symbol-error probability of $10^{-5}$.

### Problem 17-05.9 [B]

**A faster one-pole filter.** For the one-pole receive filter of Example 17-05.2 with τ = T/2, find the SNR relative to the matched filter.

### Problem 17-05.10 [C]

**Coloured noise.** *(lab)* A rectangular pulse of duration $T$ is received in Gaussian noise with PSD $S_n(f) = (N_0/2)\,[1 + 9/(1 + (fT)^2)]$, white plus a low-frequency excess. Compute, relative to $2E/N_0$ with white noise of density $N_0/2$, (a) the SNR of the filter matched to the pulse alone (ignoring the colour), and (b) the SNR of the optimal filter $H \propto S^*/S_n$. How much does accounting for the colour gain?

### Problem 17-05.11 [C]

**Matched against brick-wall.** A transmitter uses a root-raised-cosine pulse with α = 0.35. Instead of the matched RRC filter, a receiver uses an ideal low-pass filter of bandwidth $(1 + \alpha)/(2T)$. Show that the SNR relative to the matched filter is $\big(\int\sqrt{H_{RC}}\,df\big)^2/\big(\int H_{RC}\,df \cdot (1 + \alpha)/T\big)$ and evaluate it.

### Problem 17-05.12 [C]

**Orthogonal signalling gets better with M.** Using the union bound $(M - 1)Q\big(\sqrt{E_s/N_0}\big)$ with $E_s = E_b\log_2M$, evaluate the symbol-error bound at $E_b/N_0$ = 6 dB for M = 2, 16 and 64, and the bandwidth expansion $M/\log_2M$ relative to binary antipodal signalling (one dimension per bit). What limit does this trend approach?

### Problem 17-05.13 [C]

**Pulse compression.** A radar transmits a 20 µs linear chirp sweeping 50 MHz. Find the time–bandwidth product (and in dB), the range resolution, the duration of an unmodulated pulse with the same resolution, and how much higher that pulse's peak power must be to carry the same energy.

### Problem 17-05.14 [C]

**GPS acquisition.** A GPS receiver at $C/N_0$ = 46.87 dB-Hz correlates for 1 ms. Find the matched filter's peak SNR in dB. Treat the correlator output as real (carrier phase known) and set the detection threshold at half the expected correlation peak: what are the probability of missing the signal in the right cell and the probability of a false alarm in each wrong cell? With 1023 code phases searched at half-chip spacing and 20 Doppler bins, how many false alarms are expected per full search?

---

## Objective coverage

| Learning objective (chapter 17-05) | Problems |
|---|---|
| 1. Matched filter and correlator | 1, 4, 9, 10, 11 |
| 2. Signal space and Gram–Schmidt | 5, 6 |
| 3. ML and MAP detection | 7 |
| 4. Error probabilities | 2, 3, 8, 12 |
| 5. Union bound | 6, 12 |
| 6. Practical receivers, pulse compression | 4, 9, 13, 14 |
