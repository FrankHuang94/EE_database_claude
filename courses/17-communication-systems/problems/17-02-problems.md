# Problems 17-02 · Noise and SNR in Communication Systems

Chapter: [17-02](../chapters/17-02-noise-and-snr.md) · Worked solutions: [17-02 solutions](../solutions/17-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $k = 1.380649 \times 10^{-23}$ J/K and $T_0$ = 290 K, so $kT_0$ = −173.98 dBm/Hz; where a problem says "−174 dBm/Hz", use the 3GPP rounding. Noise densities $N_0$ are one-sided. Problems marked *(lab)* can be checked with the lab's `noisebudget.py` or an equivalent tool.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 17-02.1 [A]

**Noise floors.** Compute the available thermal noise power $kT_0B$ in dBm for $B$ = 1 Hz, 200 kHz, 20 MHz and 400 MHz. What open-circuit rms noise voltage does a 50 Ω resistor at 290 K produce in 400 MHz?

### Problem 17-02.2 [A]

**Noise figure and temperature.** Convert noise figures of 0.5, 2 and 10 dB to noise temperatures, and noise temperatures of 35 K and 150 K to noise figures.

### Problem 17-02.3 [A]

**Lossy components.** Find the noise figure of a matched 3 dB attenuator at 290 K. Find its noise temperature and noise figure when it is cooled to 77 K. A 0.5 dB filter inside a hot phone runs at 330 K: what are its noise temperature and noise figure?

### Problem 17-02.4 [B]

**A three-stage receiver.** An LNA (NF 1.2 dB, gain 15 dB) drives a mixer (NF 9 dB, conversion gain 8 dB), which drives an IF amplifier (NF 4 dB, gain 30 dB). Find the cascade noise figure and noise temperature and each stage's contribution to the noise factor. What LNA gain would bring the cascade to 1.5 dB with the same LNA noise figure?

### Problem 17-02.5 [B]

**Noise bandwidth.** (a) Show that a one-pole low-pass filter with 3 dB bandwidth $f_c$ has noise bandwidth $(\pi/2)f_c$, and find the SNR error (in dB) made by using $f_c$ instead. (b) An $n$th-order Butterworth filter has $\lvert H\rvert^2 = 1/(1 + (f/f_c)^{2n})$; its noise bandwidth is $f_c\,(\pi/2n)/\sin(\pi/2n)$. Evaluate the ratio $B_N/f_c$ and the error for $n$ = 4.

### Problem 17-02.6 [B]

**QPSK figures of merit.** A QPSK link sends 2 Msymbol/s with root-raised-cosine pulses of roll-off 0.25 and operates at $E_b/N_0$ = 10 dB. Find $E_s/N_0$, the occupied RF bandwidth, the SNR measured in that occupied bandwidth, the SNR at the output of the matched filter (noise bandwidth equal to the symbol rate), and $C/N_0$.

### Problem 17-02.7 [B]

**A satellite downlink.** A dish sees $T_A$ = 50 K. A feed with 0.3 dB loss at 290 K connects it to a low-noise block (LNB) with $T_e$ = 60 K and 55 dB gain, followed by a receiver with NF 10 dB. Find the system noise temperature at the antenna terminals and the contribution of each element. For a carrier of −95 dBm at the antenna terminals, find $C/N_0$ and $E_s/N_0$ at 30 Msymbol/s. How many dB of $C/N_0$ does the 0.3 dB feed loss cost?

### Problem 17-02.8 [B]

**An IoT radio.** A 1 Mb/s receiver filters to a 1 MHz noise bandwidth, has NF 7 dB, needs 9 dB SNR and keeps a 2 dB implementation margin. (a) Find its sensitivity with −174 dBm/Hz. (b) A long-range mode sends 125 kb/s. If the receiver kept the same 1 MHz bandwidth and the same required $E_b/N_0$, what would the sensitivity be? (c) In free space, received power falls as $1/d^2$. By what factor does the range grow?

### Problem 17-02.9 [B]

**3GPP at 100 MHz.** For band n78 at 30 kHz subcarrier spacing, TS 38.101-1 gives the two-port REFSENS as $-96.1 + 10\log_{10}(N_{RB}/24)$ dBm, and a 100 MHz carrier has $N_{RB}$ = 273. (a) Evaluate it. (b) Evaluate the 3GPP sensitivity equation with Example 17-02.5's assumptions (NF 10 dB, SNR −1 dB, IM 2.5 dB, diversity gain 3 dB) for the 273-RB bandwidth. (c) Evaluate the equation at 24 RB and explain the small difference between (a) and (b).

### Problem 17-02.10 [B]

**Calibrating a simulation.** *(lab)* A BPSK simulation uses rectangular pulses of amplitude ±1, 8 samples per bit, real samples and a sample-sum (matched filter) detector. (a) For $E_b/N_0$ = 6 dB, what noise variance per sample is needed, and what is the per-sample SNR? (b) A colleague sets the per-sample SNR to 6 dB instead. What $E_b/N_0$ does the simulation then represent, and what bit-error rates do the correct and the incorrect simulations produce?

### Problem 17-02.11 [B]

**GPS indoors.** Indoors the GPS signal of Example 17-02.6 is attenuated to −150 dBm, with the same system noise temperature (210.3 K). (a) Find $C/N_0$. (b) How long must the receiver integrate coherently to reach $CT/N_0$ = 15 dB? (c) The 50 b/s data bits can flip sign every 20 ms. How many 20 ms blocks must the receiver combine (ignoring the extra loss of non-coherent combining) to collect the same energy?

### Problem 17-02.12 [C]

**Ordering two amplifiers.** (a) Derive the three-stage Friis formula in noise temperatures. (b) Show that for two amplifiers, $F_1 + (F_2 - 1)/G_1 \le F_2 + (F_1 - 1)/G_2$ exactly when the **noise measure** $M = (F - 1)/(1 - 1/G)$ of amplifier 1 is the smaller. (c) Amplifier A has NF 1 dB and 10 dB gain; B has NF 0.8 dB and 6 dB gain. Which goes first, and what are the two cascade noise figures?

### Problem 17-02.13 [C]

**Gain ahead of an ADC.** An RF-sampling ADC has a noise figure of 23 dB (17-01 §9) and is preceded by an LNA with NF 1 dB. (a) Find the cascade noise figure for LNA gains of 10, 20 and 30 dB. (b) What gain holds the cascade to 2 dB? (c) The ADC's full scale is +0.97 dBm. With the gain of (b), what input power at the LNA fills the ADC's full scale? Comment on the tradeoff.

### Problem 17-02.14 [C]

**How far from Shannon?** Shannon's capacity $C = B\log_2(1 + \text{SNR})$ is derived in 17-07. (a) Show that a system operating at capacity with spectral efficiency $\eta = C/B$ needs $E_b/N_0 = (2^\eta - 1)/\eta$. (b) Evaluate it in dB for $\eta$ = 0.5, 1, 4 and 8, and its limit as $\eta \to 0$. (c) How far from this bound are the two links of Example 17-02.4?

---

## Objective coverage

| Learning objective (chapter 17-02) | Problems |
|---|---|
| 1. Available noise power, dBm and temperature | 1, 2 |
| 2. Noise factor, temperature, lossy components | 2, 3, 7 |
| 3. Friis cascades and gain placement | 4, 7, 12, 13 |
| 4. AWGN, SNR, $E_s/N_0$, $E_b/N_0$, $C/N_0$ | 5, 6, 10, 14 |
| 5. Receiver sensitivity | 8, 9 |
| 6. Correlation, averaging and signals below the noise | 10, 11 |
