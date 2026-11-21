# Problems 17-09 · Wireless Channels: Fading and Multipath

Chapter: [17-09](../chapters/17-09-wireless-channels.md) · Worked solutions: [17-09 solutions](../solutions/17-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $c$ = 299 792 458 m/s except in TR 38.901 formulas, which use $3.0 \times 10^8$ m/s. Path losses are between isotropic antennas unless gains are given. "Coherence" uses a correlation threshold of 0.5 unless stated. Rayleigh fading has unit mean power. Problems marked *(lab)* can be checked with the lab's `channels.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 17-09.1 [A]

**Free-space loss.** Find the free-space path loss at 5.8 GHz over 1 km and at 60 GHz over 100 m.

### Problem 17-09.2 [A]

**A millimetre-wave link.** A 28 GHz base station transmits 23 dBm through a 25 dBi array to a phone with a 15 dBi array 200 m away in free space. Find the received power.

### Problem 17-09.3 [A]

**Fixed apertures.** Two ideal dishes of effective area 0.1 m² face each other 10 km apart. By how many decibels does the received power change when the frequency rises from 3 GHz to 30 GHz? What is each dish's gain at 30 GHz?

### Problem 17-09.4 [B]

**Two rays.** A 900 MHz base station at 30 m serves a handset at 1.5 m. Find the two-ray breakpoint, the approximate two-ray loss at 5 km ($40\log_{10}d - 20\log_{10}h_t - 20\log_{10}h_r$, metres), and the free-space loss at the same distance.

### Problem 17-09.5 [B]

**Log-distance budget.** A measured path loss is 80 dB at 100 m with exponent 3.5. Find the loss at 1 km, the maximum range for a 125 dB budget, and the range when an 8 dB lognormal shadowing must be covered with 90% probability.

### Problem 17-09.6 [B]

**UMi at 28 GHz.** *(lab)* For TR 38.901 UMi-Street Canyon (base station at 10 m, user at 1.5 m) at 28 GHz and 50 m horizontal distance, find the LOS breakpoint and the LOS and NLOS path losses.

### Problem 17-09.7 [B]

**Two equal paths.** A channel has two equal-power paths 1 μs apart. Find its rms delay spread, the spacing of the nulls in $|H(f)|$, and the 50% coherence bandwidth.

### Problem 17-09.8 [B]

**Indoor coherence bandwidth.** For an exponential PDP with τ_rms = 50 ns, find the coherence bandwidth at correlation 0.5 and at 0.9.

### Problem 17-09.9 [B]

**Doppler.** Find $f_D$ and the coherence time for a pedestrian at 5 km/h on 5.8 GHz Wi-Fi and for a train at 300 km/h on a 2.6 GHz cellular band.

### Problem 17-09.10 [B]

**Deep fades.** For Rayleigh fading with $f_D$ = 50 Hz, find the probability that the envelope is more than 20 dB below its rms value, how many such fades occur per second, and how long they last on average.

### Problem 17-09.11 [B]

**Rayleigh statistics.** Show that the mean of a Rayleigh envelope is $\sigma\sqrt{\pi/2}$ and its rms value $\sigma\sqrt2$, and find their ratio. Express the median power relative to the mean power in decibels.

### Problem 17-09.12 [C]

**DPSK in fading.** Derive the average error rate of binary DPSK, $P_b = \tfrac12e^{-\gamma}$ in AWGN, over Rayleigh fading with mean $\bar\gamma$. Evaluate it and coherent BPSK at $\bar\gamma$ = 30 dB.

### Problem 17-09.13 [C]

**Combining for outage.** With two independent unit-mean Rayleigh branches and a threshold 10 dB below the mean, find the outage probability with one branch, with selection combining (use the stronger), and with maximal-ratio combining (add the powers; the sum of two unit exponentials has CDF $1 - e^{-x}(1 + x)$).

### Problem 17-09.14 [C]

**Pilot spacing for a fast train.** A 3.5 GHz NR carrier with 30 kHz subcarriers (14 symbols in a 0.5 ms slot) serves a train at 500 km/h. Treating the channel's time variation as bandlimited to $\pm f_D$, find $f_D$, the longest pilot spacing that samples it at the Nyquist rate, and the largest whole number of OFDM symbols between pilots.

### Problem 17-09.15 [B]

**Rician outage.** *(lab)* A link has a 10 dB fade margin. (a) Find the outage probability (the chance that $|h|^2$ falls below 0.1 of its mean) for Rayleigh fading. (b) Repeat for Rician fading with $K$ = 6 dB, normalized to unit mean power, using the Marcum-Q form of §3.6 (the lab's `rician_outage` evaluates it). (c) Evaluate the small-$x$ approximation $(K + 1)e^{-K}x$ and explain why it is poor here. (d) What outage does each give at a 30 dB margin?

### Problem 17-09.16 [B]

**Deriving Rayleigh.** The complex gain is $h = X + jY$ with $X$ and $Y$ independent $\mathcal N(0, \sigma^2)$. (a) Derive the joint density of the envelope $r = |h|$ and the phase θ, and show that θ is uniform and independent of $r$. (b) Derive the density of $r$ and that of the power $s = r^2$. (c) Find the mean and the median of $r$ in units of σ.

---

## Objective coverage

| Learning objective (chapter 17-09) | Problems |
|---|---|
| 1. Free space, two-ray, path-loss models and shadowing | 1, 2, 3, 4, 5, 6 |
| 2. Delay spread and coherence bandwidth | 7, 8 |
| 3. Doppler and coherence time | 9, 14 |
| 4. Rayleigh/Rician statistics, outage, level crossings | 10, 11, 13, 15, 16 |
| 5. Error rates in fading and diversity | 12, 13 |
