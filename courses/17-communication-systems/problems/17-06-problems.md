# Problems 17-06 · Bandpass Digital Modulation and BER

Chapter: [17-06](../chapters/17-06-bandpass-digital-modulation.md) · Worked solutions: [17-06 solutions](../solutions/17-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $s(t) = I\cos\omega_ct - Q\sin\omega_ct$; noise variance $N_0/2$ per signal-space dimension; square M-QAM uses levels $\pm1, \pm3, \ldots$ in each dimension; error rates are for AWGN with coherent ML detection unless stated. Problems marked *(lab)* can be checked with the lab's `modulation.py` or an equivalent tool.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 17-06.1 [A]

**Reading I and Q.** A symbol is transmitted as $s(t) = 3\cos\omega_ct + 4\sin\omega_ct$. What are $I$, $Q$, the complex envelope, the amplitude and the phase?

### Problem 17-06.2 [A]

**QPSK geometry.** Draw a Gray-labelled QPSK constellation with $E_s = 2$. Give the coordinates of each point, the minimum distance, and the bits that differ between diagonal neighbours.

### Problem 17-06.3 [A]

**Spectral efficiency.** Find the spectral efficiency of 1024-QAM with roll-off 0.05 and of 16-QAM with roll-off 0.35.

### Problem 17-06.4 [B]

**8-PSK.** *(lab)* At $E_s/N_0$ = 18 dB, compute the 8-PSK symbol-error rate by the nearest-neighbour approximation and by Craig's formula, and the corresponding $E_b/N_0$.

### Problem 17-06.5 [B]

**64-QAM.** Compute the average symbol energy of 64-QAM with levels ±1, ±3, ±5, ±7, its peak-to-average ratio, and its symbol-error rate at $E_s/N_0$ = 25 dB.

### Problem 17-06.6 [B]

**Why Gray coding.** For 4-PAM levels −3, −1, 1, 3, compare natural binary labels (00, 01, 10, 11) with Gray labels (00, 01, 11, 10). At high SNR, when errors are only to nearest neighbours, by what factor is the natural-label bit-error rate higher?

### Problem 17-06.7 [B]

**EVM arithmetic.** Convert −25 dB to EVM in percent and 8% EVM to an equivalent SNR. A transmitter with 3% EVM feeds a receiver whose own noise gives 30 dB SNR; what is the combined SNR, assuming both are noise-like and independent?

### Problem 17-06.8 [B]

**Phase noise.** *(lab)* A local oscillator adds Gaussian phase noise of 2° rms to every symbol of a constant-amplitude constellation. Derive the EVM, $\sqrt{2 - 2e^{-\sigma^2/2}}$ for rms phase σ in radians, evaluate it and the equivalent SNR, and say which NR modulation it would rule out.

### Problem 17-06.9 [B]

**DPSK at $10^{-6}$.** Find the $E_b/N_0$ that DPSK needs for a BER of $10^{-6}$ and its penalty relative to BPSK.

### Problem 17-06.10 [B]

**MSK and GFSK spacing.** For continuous-phase binary FSK at 1 Mb/s with modulation index $h = \Delta f\,T = 0.5$, find the tone spacing $\Delta f$ and the peak frequency deviation from the carrier. How do these compare with Bluetooth LE's nominal index of about 0.5?

### Problem 17-06.11 [C]

**The QAM figure of merit.** Derive $E_s = 2(M - 1)/3$ for square M-QAM with levels $\pm1, \pm3, \ldots$, then $d_{min}^2/(4E_b) = 3\log_2M/(2(M - 1))$. Check that it equals 1 for $M = 4$ and explain why.

### Problem 17-06.12 [C]

**A fuller union bound for 8-PSK.** At $E_s/N_0$ = 15 dB, compute the full union bound for 8-PSK, including all seven other points, and compare it with the nearest-neighbour approximation and Craig's exact value.

### Problem 17-06.13 [C]

**I/Q imbalance as EVM.** *(lab)* A quadrature modulator has a 1% gain mismatch and a 1° phase error between its I and Q paths. Using the image-suppression ratio of Problem 17-03.13, estimate the EVM it contributes and the equivalent SNR.

### Problem 17-06.14 [C]

**Link adaptation.** A modem chooses the highest of QPSK, 16-, 64- and 256-QAM whose uncoded symbol-error rate stays below $10^{-3}$. Find each threshold $E_s/N_0$. At an SNR of 18 dB in a 20 MHz channel with roll-off 0.25, which modulation is chosen and what bit rate results?

---

## Objective coverage

| Learning objective (chapter 17-06) | Problems |
|---|---|
| 1. I/Q and complex envelope | 1, 2 |
| 2. Constellations, energy, distance, PAPR | 2, 5, 11 |
| 3. PSK and QAM error rates | 4, 5, 6, 12, 14 |
| 4. Coherent, differential, noncoherent, constant envelope | 9, 10 |
| 5. Spectral efficiency | 3, 14 |
| 6. EVM | 7, 8, 13 |
