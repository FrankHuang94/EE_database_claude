# Problems 17-04 · Baseband Digital Transmission

Chapter: [17-04](../chapters/17-04-baseband-digital-transmission.md) · Worked solutions: [17-04 solutions](../solutions/17-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Symbol period $T$, symbol rate $1/T$; M-PAM levels $\pm1, \pm3, \ldots$ unless stated; cursors $h_k$ are samples of the overall pulse response at the sampling instants; $\operatorname{sinc}x = \sin(\pi x)/(\pi x)$. Problems marked *(lab)* can be checked with the lab's `baseband.py` or an equivalent tool.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 17-04.1 [A]

**Rates.** (a) 400 Gb/s is carried over four PAM4 lanes; ignoring coding overhead, find each lane's bit rate, symbol rate and Nyquist frequency. (b) A PAM4 link is quoted at 64 GT/s, counting bits. Find its symbol rate and Nyquist frequency. (c) A three-level (PAM3) code maps 3 bits to 2 symbols. How many bits per symbol does it carry, and what fraction of the PAM3 maximum $\log_23$ is that?

### Problem 17-04.2 [A]

**Coding overhead.** Find the payload rate of (a) a 10.3125 Gb/s line with 64b/66b coding, (b) a 2.5 Gb/s line with 8b/10b coding, and (c) an 8 GT/s NRZ lane with 128b/130b coding. For (c), what is the payload of 16 lanes in GB/s per direction?

### Problem 17-04.3 [A]

**Level spacing.** For M = 2, 4 and 8 with levels $\pm1, \pm3, \ldots$, find $\mathbb{E}[a^2]$. Then find the level spacing of 4-PAM and 8-PAM relative to 2-PAM, in dB, (a) at equal peak amplitude and (b) at equal average power.

### Problem 17-04.4 [B]

**The Manchester spectrum.** Derive the Fourier transform of the Manchester pulse ($+1$ on $[0, T/2)$, $-1$ on $[T/2, T)$) and the PSD for independent equiprobable bits. Evaluate the PSD at $f = 1/T$, where NRZ has a null, in units of $A^2T$.

### Problem 17-04.5 [B]

**Which spectra give zero ISI?** *(lab)* Apply the folded-spectrum test to (a) $H = T(1 - \lvert f\rvert T)$ for $\lvert f\rvert < 1/T$; (b) $H = T$ for $\lvert f\rvert < 0.6/T$ and 0 elsewhere; (c) $H = T$ for $\lvert f\rvert < 0.5/T$; (d) $H = T$ for $\lvert f\rvert < 0.3/T$, falling linearly to 0 at $0.7/T$. For the one that fails, compute the first ISI sample $h(T)/h(0)$.

### Problem 17-04.6 [B]

**Fitting a channel.** A radio channel is 6 MHz wide. With raised-cosine filtering of roll-off 0.25, what is the highest symbol rate, and what bit rate does 64-QAM (6 bits per symbol) then carry? Repeat for roll-off 0.1.

### Problem 17-04.7 [B]

**From eye to error rate.** A binary ±1 link has a worst-case eye opening (half-height) of 0.6, an ISI-free main cursor of 1, and Gaussian noise of σ = 0.12 at the sampler. Give the bit-error rate's upper bound from the worst-case eye and its lower bound from the ISI-free cursor.

### Problem 17-04.8 [B]

**A faster one-pole channel.** A channel has a 10 GHz pole. At what NRZ bit rate is the worst-case eye 50% open? What is the worst-case eye at 56 Gb/s?

### Problem 17-04.9 [B]

**Timing error, quantified.** *(lab)* With the sampling instant 0.25T late, compute the main cursor, the worst-case ISI summed over ±200 symbols, and the worst-case eye for a raised-cosine pulse with α = 0.35 and for a sinc pulse.

### Problem 17-04.10 [B]

**Decision feedback.** For the channel of Example 17-04.5 ($h_{-1}$ = 0.1, $h_0$ = 1, $h_1$ = 0.4, $h_2$ = 0.15), find the worst-case eye with a one-tap and a two-tap DFE, assuming correct past decisions. Compare with the three-tap ZF equalizer and say what each costs.

### Problem 17-04.11 [C]

**Proving Nyquist's criterion.** Derive $\sum_mH(f - m/T) = T$ from $h(kT) = \delta_k$ using Poisson summation, and show that any spectrum band-limited to $1/T$ whose roll-off is odd-symmetric about $1/(2T)$ satisfies it. Check numerically for the raised cosine with α = 0.5 at $f = 0.4/T$: find $H(0.4/T)/T$ and $H(-0.6/T)/T$.

### Problem 17-04.12 [C]

**Duobinary.** The duobinary pulse has $h(t) = \operatorname{sinc}(t/T) + \operatorname{sinc}((t - T)/T)$. Find its spectrum, its bandwidth and its samples $h(kT)$. For ±1 symbols, what levels appear at the sampler and with what probabilities? How tall is its eye relative to binary NRZ with the same peak amplitude? Why is the controlled ISI useful, and what problem does precoding solve?

### Problem 17-04.13 [B]

**When does PAM4 pay?** At 112 Gb/s, find the smallest loss slope for which PAM4 beats NRZ before equalization (equal peak swing), (a) for loss $a \cdot f$ dB with $f$ in GHz, and (b) for loss $b\sqrt f$ dB. For (b), what is the corresponding loss at 28 GHz?

### Problem 17-04.14 [C]

**A statistical eye by hand.** *(lab)* A binary ±1 link has $h_{-1}$ = 0.1, $h_0$ = 1, $h_1$ = 0.3 and Gaussian noise σ = 0.1 at the sampler. List the noiseless sample values for $a_0 = +1$, compute the exact BER by averaging over the interfering patterns, and compare it with the worst-case bound and the ISI-free value.

### Problem 17-04.15 [B]

**Design a zero-forcing equalizer.** *(lab)* A channel's sampled pulse response has $h_{-1}$ = 0.15, $h_0$ = 1, $h_1$ = 0.5 and $h_2$ = 0.2 (zero elsewhere). (a) Set up and solve the equations for a three-tap ZF FFE $(c_{-1}, c_0, c_1)$ that forces $q_{-1} = q_1 = 0$ and $q_0 = 1$. (b) Find the combined response $q_k$ for $k = -2$ to 3 and its residual ISI $\sum_{k\ne0}\lvert q_k\rvert$. (c) Compare the worst-case binary eye opening before and after equalization. (d) Find the noise enhancement $\sum c_j^2$ for independent noise samples, in dB, and say whether the trade was worth it.

---

## Objective coverage

| Learning objective (chapter 17-04) | Problems |
|---|---|
| 1. PAM rates, levels and energy | 1, 3 |
| 2. Line codes, spectra and overhead | 2, 4 |
| 3. ISI and peak distortion | 8, 9, 10 |
| 4. Nyquist criterion and raised-cosine design | 5, 6, 11, 12 |
| 5. Eye diagrams and BER | 7, 9, 14 |
| 6. Equalization and PAM4 trade-offs | 10, 13, 15 |
