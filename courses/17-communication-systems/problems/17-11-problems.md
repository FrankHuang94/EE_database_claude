# Problems 17-11 · MIMO and Beamforming Basics

Chapter: [17-11](../chapters/17-11-mimo-and-beamforming.md) · Worked solutions: [17-11 solutions](../solutions/17-11-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Rayleigh branches are i.i.d. with unit mean power unless stated; ρ is the total transmit SNR, split equally over $N_t$ antennas when the transmitter has no channel knowledge. ULAs have uniform weights. NR rates use TS 38.306's formula with $R_{max} = 948/1024$ and $f = 1$. Problems marked *(lab)* can be checked with the lab's `mimo.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 17-11.1 [A]

**Which gain?** For each, say whether it provides array gain, diversity gain, multiplexing gain, or a combination: (a) MRC with two antennas whose fading is fully correlated; (b) selection combining over independent antennas; (c) Alamouti 2×1; (d) 4×4 spatial multiplexing in rich scattering.

### Problem 17-11.2 [A]

**EGC against MRC.** Two branches have gains $h = [1, 0.5]$ (already co-phased). Find the output SNR gain (relative to one unit-gain branch) of equal-gain combining, $(\sum|h_k|)^2/N$, and of MRC, $\sum|h_k|^2$.

### Problem 17-11.3 [A]

**Selection's diminishing returns.** Find the mean SNR gain of selection combining with 3 and with 8 branches, and how far the 8-branch figure falls short of MRC's in dB.

### Problem 17-11.4 [B]

**Three-branch outage.** For a threshold at 0.1 of the per-branch mean, find the MRC outage with 3 branches, its small-$x$ approximation $x^3/3!$, and the selection-combining outage.

### Problem 17-11.5 [B]

**SNR for $10^{-6}$.** *(lab)* Find the average per-branch SNR at which BPSK reaches $10^{-6}$ with 1, 2 and 4 MRC branches in Rayleigh fading.

### Problem 17-11.6 [B]

**A 16-element array.** For a 16-element half-wavelength ULA, find the array gain, the broadside half-power beamwidth (numerically), the first null, and the largest spacing that avoids grating lobes when scanning to 45°.

### Problem 17-11.7 [B]

**Beamforming at both ends.** A millimetre-wave link uses 64-element arrays at both ends, each beamforming with full array gain. By what factor does the free-space range increase compared with single isotropic elements at the same transmit power?

### Problem 17-11.8 [B]

**Line of sight.** A 2×2 channel has every entry equal to 1 (a line-of-sight channel between compact arrays). Find its singular values and its equal-power capacity at ρ = 20 dB, and compare with $\mathbf H = \mathbf I_2$.

### Problem 17-11.9 [B]

**Water-filling at low SNR.** For $\mathbf H = \text{diag}(1, 0.3)$ at ρ = 0 dB, compare the equal-power capacity with the water-filling capacity.

### Problem 17-11.10 [C]

**An ill-conditioned channel.** For $\mathbf H = \begin{bmatrix}1 & 0.9\\0.9 & 1\end{bmatrix}$ at ρ = 20 dB, find the singular values, the condition number, the per-stream ZF SNR, the ZF sum rate and the capacity. What SNR would one stream get if the other were absent and the receiver used MRC on its column?

### Problem 17-11.11 [C]

**Capacity slope.** Using the 2×2 eigenvalue density of Example 17-11.5, find the ergodic 2×2 capacity at 10 dB and 30 dB, and the increase from 20 to 30 dB; compare with the SISO increase (closed form).

### Problem 17-11.12 [B]

**NR rates.** Using TS 38.306's formula, find the peak uplink rate of a 100 MHz FR1 carrier at 30 kHz (273 RBs) with 2 layers of 256-QAM (overhead 0.08), and the downlink rate of a 400 MHz FR2 carrier at 120 kHz (264 RBs) with 2 layers of 64-QAM (overhead 0.18).

### Problem 17-11.13 [A]

**Channel hardening.** For $M$ i.i.d. Rayleigh antennas, the standard deviation of $\|\mathbf h\|^2/M$ is $1/\sqrt M$. What is it for $M$ = 100, and what does that imply for scheduling?

### Problem 17-11.14 [C]

**Alamouti against MRC at 20 dB.** Find the BPSK error rate of 1×2 MRC and of 2×1 Alamouti at an average per-branch SNR of 20 dB, and the SNR Alamouti needs to match MRC's error rate at 20 dB.

---

## Objective coverage

| Learning objective (chapter 17-11) | Problems |
|---|---|
| 1. Array, diversity and multiplexing gains | 1, 7, 13 |
| 2. Combining and Alamouti | 2, 3, 4, 5, 14 |
| 3. Uniform linear arrays | 6, 7 |
| 4. MIMO capacity | 8, 9, 11 |
| 5. ZF and MMSE receivers | 10 |
| 6. NR layers and peak rates | 12 |
