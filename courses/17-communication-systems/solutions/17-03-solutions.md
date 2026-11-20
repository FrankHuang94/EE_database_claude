# Solutions 17-03 · Analog Modulation (Brief)

Problems: [17-03 problems](../problems/17-03-problems.md) · Chapter: [17-03](../chapters/17-03-analog-modulation.md). Every number below is recomputed by [verify_17_03.py](../verify/verify_17_03.py): Bessel values from SciPy and from their defining integral, SSB and sideband-suppression results from simulated phasing modulators, SNR formulas in closed form and by Monte Carlo, and the radar beat by simulating a dechirped echo.

---

## Solutions

### Solution 17-03.1

The Hilbert transform turns $\cos$ into $\sin$ and $\sin$ into $-\cos$, term by term:

$$
\hat m(t) = \sin(2\pi \cdot 300t) - 0.5\cos(2\pi \cdot 2000t) .
$$

For the 300 Hz cosine, $\tfrac12[\cos\omega_mt\cos\omega_ct - \sin\omega_mt\sin\omega_ct] = \tfrac12\cos(\omega_c + \omega_m)t$: a line at **10.3** kHz of amplitude **0.5**. For the 2 kHz sine, $\tfrac12[0.5\sin\omega_mt\cos\omega_ct + 0.5\cos\omega_mt\sin\omega_ct] = 0.25\sin(\omega_c + \omega_m)t$: a line at **12** kHz of amplitude **0.25**. Each message component moves up by $f_c$ with half its amplitude and its own phase; nothing appears below 10 kHz.

### Solution 17-03.2

DSB-SC and AM occupy $2W$ = **10** kHz; SSB occupies $W$ = **5** kHz. For tone AM, $s = A_c[1 + \mu\cos\omega_mt]\cos\omega_ct$ has carrier power $A_c^2/2$ and sideband power $A_c^2\mu^2/4$, so the sideband fraction is

$$
\eta = \frac{\mu^2/4}{1/2 + \mu^2/4} = \frac{\mu^2}{2 + \mu^2} = \frac{0.64}{2.64} = \textbf{0.242} .
$$

About a quarter of the power carries the message; the rest is carrier.

### Solution 17-03.3

$\theta_i = 2\pi \cdot 10^6t + 3\sin(2\pi \cdot 1000t)$, so

$$
f_i = \frac{1}{2\pi}\frac{d\theta_i}{dt} = 10^6 + 3 \times 1000\cos(2\pi \cdot 1000t)\ \text{Hz} ,
$$

which swings between **997** and **1003** kHz. The peak deviation is 3 kHz and β = 3/1 = **3**. Carson's bandwidth is $2(3 + 1)$ = **8** kHz.

It is FM of the message $\cos(2\pi \cdot 1000t)$ with $k_f$ = 3 kHz per unit, or PM of the message $\sin(2\pi \cdot 1000t)$ with $k_p$ = 3 rad per unit. For a single tone the waveform cannot tell them apart; they differ in how deviation scales with tone frequency (FM: fixed $\Delta f$; PM: $\Delta f = k_pf_m$ grows with frequency).

### Solution 17-03.4

$J_0(1) = 0.7652$, $J_1(1) = 0.4401$, $J_2(1) = 0.1149$.

- Carrier: $J_0^2$ = **0.586** of the power.
- First pair: $2J_1^2$ = **0.387**.
- Carson's band (β + 1 = 2 pairs): $J_0^2 + 2J_1^2 + 2J_2^2$ = **0.9992**.

At β = 1 the carrier still holds most of the power; Carson's rule is generous at small indices.

### Solution 17-03.5

The narrowband signal is $A_c[\cos\omega_ct - \beta\sin\omega_mt\,\sin\omega_ct]$, a carrier plus a quadrature term, so its envelope is

$$
A_c\sqrt{1 + \beta^2\sin^2\omega_mt} ,
$$

which peaks at $A_c\sqrt{1 + \beta^2}$ = **1.020** $A_c$ for β = 0.2: 2% residual amplitude modulation. True FM's higher sidebands ($J_2$ and beyond) cancel this envelope variation exactly, because $\cos(\omega_ct + \phi)$ has unit envelope for any φ. The approximation keeps only the first-order terms of $\cos\phi \approx 1$, $\sin\phi \approx \phi$.

### Solution 17-03.6

The multiplier must raise the deviation by $75\,000/25$ = **3000**. Multiplying frequency by 3000 also multiplies the carrier: $200\ \text{kHz} \times 3000$ = **600** MHz. Mixing with a **500** MHz oscillator gives the difference frequency 100 MHz (700 MHz would also work). Mixing shifts every frequency by the same amount, so the deviation is unchanged: still 75 kHz. Only multiplication, which multiplies every instantaneous frequency, scales the deviation.

### Solution 17-03.7

The output SNR is proportional to $D^2$: doubling $D$ from 5 to 10 adds $10\log_{10}4$ = **6.02** dB. Carson's bandwidth grows from $2(75 + 15)$ = 180 kHz to $2(150 + 15)$ = **330** kHz. The threshold power is proportional to $B_T$, so it rises by $10\log_{10}(330/180)$ = **2.63** dB. The SNR gain exceeds the threshold penalty, but only for receivers that already have the extra received power.

### Solution 17-03.8

Tone AM at 100%: $s = A_c(1 + \cos\omega_mt)\cos\omega_ct$. The peak envelope is $2A_c$, so the peak envelope power is $(2A_c)^2/2 = 2A_c^2$. The average power is $(A_c^2/2)(1 + 1/2) = 0.75A_c^2$, and $\text{SNR}_{\text{AM}} = \tfrac13 \cdot 0.75A_c^2/(N_0W) = 0.25A_c^2/(N_0W)$.

SSB with one tone is a single sinusoid of amplitude $A_s$: its peak and average powers are both $A_s^2/2$, and $\text{SNR}_{\text{SSB}} = (A_s^2/2)/(N_0W)$. With equal peak power, $A_s^2/2 = 2A_c^2$, so $\text{SNR}_{\text{SSB}} = 2A_c^2/(N_0W)$.

The ratio is $2/0.25 = 8$, **9.03** dB in SSB's favour. A peak-limited transmitter delivers 8 times more useful SNR with SSB.

### Solution 17-03.9

$\lvert H_{pe}(f)\rvert = \sqrt{1 + (2\pi f\tau)^2}$. At 15 kHz with τ = 75 µs, $2\pi f\tau = 7.069$ and $\lvert H_{pe}\rvert$ = **7.14**, or **17.07** dB above low frequencies. A loud treble component would therefore drive about 7 times more deviation than the same level at low frequency. Broadcast audio processors compress and limit high frequencies (and use clippers designed for pre-emphasized audio) so the total stays within ±75 kHz, the regulatory 100%.

### Solution 17-03.10

The angle advance per sample, $2\pi f_i/f_s$, must stay below π in magnitude, so $f_s > 2\max\lvert f_i\rvert$. With the peak deviation alone, $\max\lvert f_i\rvert$ = 75 kHz and $f_s$ > **150** kHz. In practice the sample rate is higher: the signal occupies about 180 kHz (Carson) or more for stereo and its spectral tails, noise and adjacent-channel energy push the instantaneous frequency beyond the deviation, and the IF filter needs transition room. Rates of a few hundred kilosamples per second are typical for software FM receivers.

### Solution 17-03.11

For PM, $s = A_c\cos(\omega_ct + k_pm(t))$, and the demodulator outputs the phase. As in §3.7, above threshold the phase noise is the perpendicular noise component over $A_c$, with PSD $N_0/A_c^2$ over $\lvert f\rvert < B_T/2$. After the low-pass filter to $W$, the noise power is $2WN_0/A_c^2$. The signal is $k_pm$, power $k_p^2P_m$. With $S_R = A_c^2/2$,

$$
\text{SNR}_{\text{PM}} = \frac{k_p^2P_mA_c^2}{2N_0W} = k_p^2P_m\,\frac{S_R}{N_0W} = k_p^2P_m\gamma .
$$

For a tone ($P_m = 1/2$): $k_p$ = 1 rad gives 0.5, **−3.01** dB relative to DSB; $k_p = \pi/2$ gives 1.234, **+0.91** dB. PM's gain grows with the square of the phase swing, but the swing is limited to about π before the phase becomes ambiguous, so PM cannot trade bandwidth for SNR as freely as FM. The noise spectra differ because PM reads the phase (flat noise) and FM reads its derivative (noise multiplied by $f^2$).

### Solution 17-03.12

Threshold requires $S_R/(N_0B_T) = \gamma/(2(D + 1)) \ge 10$, so $D \le \gamma/20 - 1$ in linear units.

- γ = 25 dB (316.2): $D_{max}$ = **14.81**, and the tone output SNR is $\tfrac32D^2\gamma$: $25 + 10\log_{10}(1.5 \times 14.81^2)$ = **50.17** dB, 25 dB better than SSB's 25 dB.
- γ = 15 dB (31.62): $D_{max}$ = **0.581** and the output SNR is $15 + 10\log_{10}(1.5 \times 0.581^2)$ = **12.05** dB, **worse** than SSB's 15 dB.

FM pays only when there is enough received power to afford a large deviation: roughly, γ must be at least 20 dB (10 dB CNR in at least $2W$) before FM can even match a linear scheme. At low SNR, the bandwidth is better spent another way (coding, 17-08).

### Solution 17-03.13

Let the I path carry $m\cos\omega_ct$ and the Q path $g\hat m\sin(\omega_ct + \varepsilon)$, with output $I - Q$. For a tone $m = \cos\omega_mt$, $\hat m = \sin\omega_mt$:

$$
\begin{aligned}
\cos\omega_mt\cos\omega_ct &= \tfrac12[\cos(\omega_c - \omega_m)t + \cos(\omega_c + \omega_m)t] ,\\
g\sin\omega_mt\sin(\omega_ct + \varepsilon) &= \tfrac g2[\cos((\omega_c - \omega_m)t + \varepsilon) - \cos((\omega_c + \omega_m)t + \varepsilon)] .
\end{aligned}
$$

Subtracting, the upper sideband is $\tfrac12[\cos\theta_+ + g\cos(\theta_+ + \varepsilon)]$, a phasor sum of amplitude $\tfrac12\lvert1 + ge^{j\varepsilon}\rvert$, and the lower sideband has amplitude $\tfrac12\lvert1 - ge^{j\varepsilon}\rvert$. The power ratio is

$$
\frac{\lvert1 + ge^{j\varepsilon}\rvert^2}{\lvert1 - ge^{j\varepsilon}\rvert^2} = \frac{1 + 2g\cos\varepsilon + g^2}{1 - 2g\cos\varepsilon + g^2} .
$$

- ε = 1°, $g$ = 1: $\cot^2(0.5°)$, **41.18** dB.
- ε = 0, $g$ = 1.01: $(2.01/0.01)^2$, **46.06** dB.
- Both: **39.96** dB.

A tenth of a dB of gain mismatch (1.2%) or a degree of phase error limits suppression to roughly 40 dB, which is why modern transceivers calibrate their I/Q paths.

### Solution 17-03.14

The chirp slope is $S = 4\ \text{GHz}/40\ \mu\text{s} = 10^{14}$ Hz/s. An echo delayed by $\tau = 2R/c$ differs in frequency from the transmitted chirp by $S\tau$:

- $R$ = 30 m: $\tau$ = 200.1 ns and $f_b = S\tau$ = **20.0** MHz.
- $f_b$ = 10 MHz: $R = cf_b/(2S)$ = **15.0** m.
- Resolution: $c/(2B) = 3 \times 10^8/(8 \times 10^9)$ = **3.75** cm.

Two targets closer than $c/2B$ produce beat tones less than one FFT bin ($1/T_{chirp}$ = 25 kHz) apart, which is where the resolution formula comes from: $\Delta f_b = S \cdot 2\Delta R/c = 1/T$ gives $\Delta R = c/(2ST) = c/(2B)$.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 17-03.1a | USB line from the 300 Hz term | 10.3 | kHz |
| 17-03.1b | its amplitude | 0.5 | — |
| 17-03.1c | USB line from the 2 kHz term | 12 | kHz |
| 17-03.1d | its amplitude | 0.25 | — |
| 17-03.2a | DSB and AM bandwidth | 10 | kHz |
| 17-03.2b | SSB bandwidth | 5 | kHz |
| 17-03.2c | AM sideband power fraction, μ = 0.8 | 0.242 | — |
| 17-03.3a | lowest instantaneous frequency | 997 | kHz |
| 17-03.3b | highest instantaneous frequency | 1003 | kHz |
| 17-03.3c | modulation index | 3 | — |
| 17-03.3d | Carson bandwidth | 8 | kHz |
| 17-03.4a | carrier power fraction, β = 1 | 0.586 | — |
| 17-03.4b | first-pair power fraction | 0.387 | — |
| 17-03.4c | power inside Carson's band | 0.9992 | — |
| 17-03.5a | peak envelope, β = 0.2 | 1.020 | — |
| 17-03.6a | multiplication factor | 3000 | — |
| 17-03.6b | multiplied carrier | 600 | MHz |
| 17-03.6c | mixing oscillator | 500 | MHz |
| 17-03.7a | SNR change | 6.02 | dB |
| 17-03.7b | new Carson bandwidth | 330 | kHz |
| 17-03.7c | threshold power change | 2.63 | dB |
| 17-03.8a | SSB over AM at equal peak power | 9.03 | dB |
| 17-03.9a | pre-emphasis boost at 15 kHz | 7.14 | — |
| 17-03.9b | boost in dB | 17.07 | dB |
| 17-03.10a | minimum sample rate | 150 | kHz |
| 17-03.11a | PM, kp = 1, relative to DSB | −3.01 | dB |
| 17-03.11b | PM, kp = π/2, relative to DSB | 0.91 | dB |
| 17-03.12a | largest D at γ = 25 dB | 14.81 | — |
| 17-03.12b | FM output SNR at γ = 25 dB | 50.17 | dB |
| 17-03.12c | largest D at γ = 15 dB | 0.581 | — |
| 17-03.12d | FM output SNR at γ = 15 dB | 12.05 | dB |
| 17-03.13a | suppression, 1° | 41.18 | dB |
| 17-03.13b | suppression, 1% gain | 46.06 | dB |
| 17-03.13c | suppression, both | 39.96 | dB |
| 17-03.14a | beat at 30 m | 20.0 | MHz |
| 17-03.14b | range for a 10 MHz beat | 15.0 | m |
| 17-03.14c | range resolution | 3.75 | cm |
| 17-03.14d | echo delay at 30 m | 200.1 | ns |
