# Problems 17-03 · Analog Modulation (Brief)

Chapter: [17-03](../chapters/17-03-analog-modulation.md) · Worked solutions: [17-03 solutions](../solutions/17-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $m(t)$ has bandwidth $W$, power $P_m$ and peak $\lvert m\rvert \le 1$; $\gamma = S_R/(N_0W)$ is the baseband reference SNR with one-sided noise density $N_0$. $J_n$ is the Bessel function of the first kind. Problems marked *(lab)* can be checked with the lab's `analogmod.py` or an equivalent tool.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 17-03.1 [A]

**Hilbert transforms and an SSB spectrum.** A message is $m(t) = \cos(2\pi \cdot 300t) + 0.5\sin(2\pi \cdot 2000t)$. Find $\hat m(t)$. Write the upper-sideband SSB signal $(1/2)\,[m\cos\omega_ct - \hat m\sin\omega_ct]$ for $f_c$ = 10 kHz as a sum of sinusoids, giving each frequency and amplitude.

### Problem 17-03.2 [A]

**Bandwidth and power efficiency.** A 5 kHz message is sent by DSB-SC, SSB and AM. Give each RF bandwidth. For AM with a single tone at modulation index μ = 0.8, what fraction of the transmitted power is in the sidebands?

### Problem 17-03.3 [A]

**Instantaneous frequency.** $s(t) = \cos(2\pi \cdot 10^6t + 3\sin(2\pi \cdot 1000t))$. Find the instantaneous frequency, its range, the modulation index and Carson's bandwidth. Is this FM or PM of a tone? (Both answers can be right; say what each assumes about the message.)

### Problem 17-03.4 [B]

**Where the power goes.** *(lab)* For tone FM with β = 1, find the fraction of power in the carrier, in the first sideband pair, and inside Carson's bandwidth.

### Problem 17-03.5 [B]

**Narrowband FM has a little AM.** The narrowband approximation of tone FM is $A_c[\cos\omega_ct - \beta\sin(\omega_mt)\sin\omega_ct]$. Find its envelope and the largest envelope for β = 0.2. Why does true FM not have this amplitude variation?

### Problem 17-03.6 [B]

**An Armstrong transmitter.** A crystal-controlled narrowband modulator at 200 kHz produces 25 Hz of peak deviation. The output must have 75 kHz deviation at 100 MHz. What frequency multiplication is needed, at what frequency does the multiplied carrier land, and what local-oscillator frequency brings it to 100 MHz by mixing down? Does mixing change the deviation?

### Problem 17-03.7 [B]

**Doubling the deviation.** For the FM receiver of Example 17-03.4 (β = 5, $W$ = 15 kHz), the deviation is doubled to 150 kHz. By how much do the output SNR (above threshold), Carson's bandwidth and the threshold received power change?

### Problem 17-03.8 [B]

**Equal peak power.** A transmitter is limited by its peak envelope power. Compare the output SNR of 100%-modulated tone AM with that of SSB carrying the same tone when both transmit the same peak envelope power.

### Problem 17-03.9 [B]

**Pre-emphasis and deviation.** With a 75 µs pre-emphasis network $1 + j2\pi f\tau$, by what factor (and how many dB) is a 15 kHz tone boosted relative to a low-frequency tone? What does this imply for a transmitter's audio processing?

### Problem 17-03.10 [B]

**A digital FM discriminator.** *(lab)* A receiver computes $f_i[n] = (f_s/2\pi)\arg\{z[n]z^*[n - 1]\}$ on complex baseband samples of a broadcast-style FM signal (75 kHz deviation, 15 kHz audio). What is the smallest sample rate at which the discriminator never wraps for the peak deviation alone? Why is a higher rate used in practice?

### Problem 17-03.11 [C]

**PM noise performance.** Derive the output SNR of a phase demodulator, $\text{SNR}_{\text{PM}} = k_p^2P_m\gamma$, following §3.7. For a tone with $k_p$ = 1 rad and with $k_p$ = π/2 rad, how does PM compare with DSB? Why is the noise spectrum flat for PM but parabolic for FM?

### Problem 17-03.12 [C]

**Choosing the deviation.** With the threshold at 10 dB CNR in Carson's bandwidth, find the largest deviation ratio $D$ an FM link can use at γ = 25 dB and the tone output SNR it then delivers. Repeat for γ = 15 dB and compare with SSB. What does this say about when FM is worth its bandwidth?

### Problem 17-03.13 [C]

**Unwanted-sideband suppression of the phasing method.** In the phasing modulator, the 90° network has phase error ε and the Q path has gain $g$ relative to the I path. Show that the ratio of wanted to unwanted sideband power is $(1 + 2g\cos\varepsilon + g^2)/(1 - 2g\cos\varepsilon + g^2)$. Evaluate it in dB for ε = 1°, $g$ = 1; for ε = 0, $g$ = 1.01; and for both errors together. The same formula gives the image rejection of an I/Q receiver (21-08).

### Problem 17-03.14 [C]

**FM measures distance.** A radar transmits a linear chirp sweeping 4 GHz in 40 µs. The echo from a target at range $R$ returns after $2R/c$; mixing it with the transmitted chirp gives a beat tone. Find the beat frequency for a target at 30 m, the range of a target producing a 10 MHz beat, and the range resolution $c/(2B)$.

---

## Objective coverage

| Learning objective (chapter 17-03) | Problems |
|---|---|
| 1. SSB, the Hilbert transform, carrier errors | 1, 2, 13 |
| 2. Instantaneous frequency, modulation index, deviation | 3, 6, 10, 14 |
| 3. Bessel spectra and Carson's rule | 3, 4, 5, 7 |
| 4. Output SNR, threshold, pre-emphasis | 7, 8, 9, 11, 12 |
| 5. Choosing among schemes | 2, 8, 12 |
