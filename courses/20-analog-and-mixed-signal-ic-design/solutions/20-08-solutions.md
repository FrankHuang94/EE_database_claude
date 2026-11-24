# Solutions 20-08 · Oversampling and Sigma-Delta Converters

Problems: [20-08 problem set](../problems/20-08-problems.md) · Chapter: [20-08](../chapters/20-08-sigma-delta-converters.md). Every number below is recomputed by [verify_20_08.py](../verify/verify_20_08.py).

---

## Solutions

### Solution 20-08.1

Nyquist SQNR: $20\log_{10}2^{10} + 1.76$ = 61.97 dB. Oversampling keeps $1/16$ of the noise: $+10\log_{10}16$ = 12.04 dB, so **74.0** dB, the SQNR of a **12.0**-bit Nyquist converter. Sixteen times the sample rate bought two bits.

### Solution 20-08.2

Each step adds $x - y$ = −1.4 when $u \ge 0$ and +0.6 when $u < 0$:

| $n$ | $u[n]$ | $y[n]$ |
|---|---|---|
| 0 | 0.3 | +1 |
| 1 | **−1.1** | −1 |
| 2 | **−0.5** | −1 |
| 3 | **0.1** | +1 |
| 4 | **−1.3** | −1 |

The integrator stays within $1 + \lvert x\rvert$ = 1.4. The output average must equal −0.4, so the fraction $p$ of +1s satisfies $p - (1 - p) = -0.4$: $p$ = **0.3**. The values are $0.3 - 0.4n$ modulo 1, which repeat after **10** samples (three +1s, seven −1s).

### Solution 20-08.3

Tones at multiples of $xf_s$ = 0.004 × 2.56 MHz = **10.24** kHz, amplitude $2x$ = 0.008: **−41.9** dBFS. The band edge is $f_s/(2\,\text{OSR})$ = **20** kHz, so the tone is in band. Tones fall in band for $\lvert x\rvert < 1/(2 \times 64)$ = **0.0078**.

### Solution 20-08.4

Quantizer term at −6 dBFS, 1-bit: $10\log_{10}[(0.25/2)/(1/3)]$ = −4.26 dB. Penalty: $10\log_{10}(\pi^6/7)$ = 21.41 dB. Slope: $70\log_{10}32$ = 105.36 dB. SQNR = −4.26 − 21.41 + 105.36 = **79.7** dB. A 16-level quantizer adds $20\log_{10}15$ = 23.52 dB: **103.2** dB. (A real third-order 1-bit loop would need Lee's rule and lose much of this; the 16-level loop is far more likely to be stable with the pure NTF.)

### Solution 20-08.5

Solve $(20L + 10)\log_{10}\text{OSR} = 90 + 4.26 + 10\log_{10}[\pi^{2L}/(2L + 1)]$:

- $L = 1$: $30\log_{10}\text{OSR} = 90 + 4.26 + 5.17$, OSR = **2062**.
- $L = 2$: $50\log_{10}\text{OSR} = 90 + 4.26 + 12.90$, OSR = **139**.

One extra integrator saves a factor of **14.8** in clock rate.

### Solution 20-08.6

With $t = \omega/\omega_B$ and $a = \omega_z/\omega_B$, the in-band noise is proportional to $\int_0^1(t^2 - a^2)^2dt = 1/5 - 2a^2/3 + a^4$. Setting the derivative $-4a/3 + 4a^3$ to zero gives $a^2 = 1/3$. The zeros sit at $24\text{ kHz}/\sqrt3$ = **13.9** kHz, and the noise falls from $1/5$ to $4/45$: **3.5** dB.

### Solution 20-08.7

$\lvert 1 - e^{-j\omega}\rvert^2 = 4\sin^2(\omega/2)$ per factor, so $\lvert\text{NTF}\rvert^2 = 16\sin^4(\omega/2)$.

- At $f_s/4$ (ω = π/2): $16 \times (1/\sqrt2)^4$ = **4** (a magnitude of 2).
- At $f_s/2$: $\lvert\text{NTF}\rvert = 4\sin^2(\pi/2)$ = **4**.
- At the band edge (ω = π/64): $16\sin^4(\pi/128)$ = 5.80 × 10⁻⁶, or **−52.4** dB.

### Solution 20-08.8

$Y_1 = z^{-2}X + (1 - z^{-1})^2E_1$ and $Y_2 = -z^{-1}E_1 + (1 - z^{-1})E_2$. The $E_1$ terms in $D_1Y_1 + D_2Y_2$ are $D_1(1 - z^{-1})^2 - D_2z^{-1}$, which vanish for $D_1 = z^{-1}$ and $D_2 = (1 - z^{-1})^2$. Then

$$
Y = z^{-3}X + (1 - z^{-1})^3E_2 ,
$$

a **3**rd-order NTF. Its linear-model SQNR is that of Problem 4's 1-bit loop at OSR = 64: $-4.26 - 21.41 + 70\log_{10}64$ = **100.8** dB, from two stable low-order loops, if the digital filters match the analog ones.

### Solution 20-08.9

Signal power $2.5^2/2$ = 3.125 V²; noise budget $3.125 \times 10^{-12}$ V². $C = kT/(\text{budget} \times \text{OSR})$:

- OSR 256: $4.1419 \times 10^{-21}/(3.125 \times 10^{-12} \times 256)$ = **5.18** pF.
- OSR 64: **20.7** pF.

### Solution 20-08.10

(a) Leakage ε ≈ $(C_s/C_i)/A$ must stay below $\pi/(\sqrt3\,\text{OSR})$: $A > 0.5\sqrt3 \times 128/\pi$ = **35.3**. Halving $C_s/C_i$ halves the leakage, cancelling the doubled OSR.

(b) ε < $\pi^2/(\sqrt5\,\text{OSR}^2)$: $A > \sqrt5 \times 128^2/\pi^2$ = **3712**, that is **71.4** dB.

### Solution 20-08.11

The denominator is $1 - dz^{-1} + dz^{-2}$; its poles satisfy $z^2 - dz + d = 0$, of radius $\sqrt d$ = **0.5**. At $z = -1$: $\lvert\text{NTF}\rvert = 2/(1 + 2d)$ = **1.33**, against 2 with no delay. The delay adds poles that flatten the NTF and raise in-band noise slightly; a first-order loop stays stable for $d < 1$.

### Solution 20-08.12

Budget: $0.125 \times 10^{-7}$ = 1.25 × 10⁻⁸. From $E[(\Delta y)^2]\,(\sigma_tf_s)^2/\text{OSR} \le$ budget:

- 1-bit: $\sigma_tf_s \le \sqrt{1.25 \times 10^{-8} \times 16/2.36}$ = 2.91 × 10⁻⁴, $\sigma_t \le$ **0.455** ps.
- 16 levels: $\sigma_t \le$ **4.05** ps.

The multi-bit loop relaxes the clock by a factor of **8.9** (the square root of the step-variance ratio).

### Solution 20-08.13

The integrate-and-dump input filter gives $\sin(\pi/64)/[\pi(1 - 1/64)]$ = 0.0159: **−36.0** dB. A discrete-time modulator samples its input directly, so the interferer aliases onto the band edge unattenuated; it needs an explicit anti-aliasing filter.

### Solution 20-08.14

(a) $K \ge L + 1$ = **4**.

(b) The band edge is $f_B = f_s/256$: $\lvert H\rvert = [\sin(32\pi/256)/(32\sin(\pi/256))]^4$ = 0.902, **−0.90** dB, to be equalized in the half-band stages.

(c) $K\log_2M = 4 \times 5$ = **20** bits beyond the modulator's word.

### Solution 20-08.15

Solve as in Solution 5 with a 70 dB target:

- Second order, 1-bit: $50\log_{10}\text{OSR} = 70 + 4.26 + 12.90$, OSR = **55.4**, $f_s = 2 \times 20\text{ MHz} \times 55.4$ = **2.21** GHz.
- Third order, 16 levels: $70\log_{10}\text{OSR} = 70 + 4.26 - 23.52 + 21.41$, OSR = **10.7**, $f_s$ = **0.429** GHz.

The multi-bit third-order loop runs **5.2** times slower, is easier to keep stable, and (Example 20-08.7) is far less sensitive to clock jitter, at the cost of a 16-level DAC that needs element matching. Wide-bandwidth CT modulators are built this way.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 20-08.1a | in-band SQNR | 74.0 | dB |
| 20-08.1b | equivalent bits | 12.0 | bits |
| 20-08.2a | u[1] | −1.1 | — |
| 20-08.2b | u[2] | −0.5 | — |
| 20-08.2c | u[3] | 0.1 | — |
| 20-08.2d | u[4] | −1.3 | — |
| 20-08.2e | fraction of +1 | 0.3 | — |
| 20-08.2f | period | 10 | samples |
| 20-08.3a | tone frequency | 10.24 | kHz |
| 20-08.3b | tone amplitude | −41.9 | dBFS |
| 20-08.3c | band edge | 20 | kHz |
| 20-08.3d | threshold input | 0.0078 | — |
| 20-08.4a | SQNR, 1-bit | 79.7 | dB |
| 20-08.4b | SQNR, 16 levels | 103.2 | dB |
| 20-08.5a | OSR, first order | 2062 | — |
| 20-08.5b | OSR, second order | 139 | — |
| 20-08.5c | ratio of OSRs | 14.8 | — |
| 20-08.6a | zero frequency | 13.9 | kHz |
| 20-08.6b | noise saving | 3.5 | dB |
| 20-08.7a | power gain at fs/4 | 4 | — |
| 20-08.7b | gain at fs/2 | 4 | — |
| 20-08.7c | power gain at band edge | −52.4 | dB |
| 20-08.8a | NTF order | 3 | — |
| 20-08.8b | SQNR | 100.8 | dB |
| 20-08.9a | capacitor, OSR 256 | 5.18 | pF |
| 20-08.9b | capacitor, OSR 64 | 20.7 | pF |
| 20-08.10a | single-loop gain | 35.3 | — |
| 20-08.10b | MASH gain | 3712 | — |
| 20-08.10c | MASH gain in dB | 71.4 | dB |
| 20-08.11a | pole radius | 0.5 | — |
| 20-08.11b | NTF at fs/2 | 1.33 | — |
| 20-08.12a | jitter, 1-bit | 0.455 | ps |
| 20-08.12b | jitter, 16 levels | 4.05 | ps |
| 20-08.12c | jitter relaxation | 8.9 | — |
| 20-08.13a | alias attenuation | −36.0 | dB |
| 20-08.14a | CIC order | 4 | — |
| 20-08.14b | droop | −0.90 | dB |
| 20-08.14c | register growth | 20 | bits |
| 20-08.15a | OSR, second order 1-bit | 55.4 | — |
| 20-08.15b | clock, second order | 2.21 | GHz |
| 20-08.15c | OSR, third order 16 levels | 10.7 | — |
| 20-08.15d | clock, third order | 0.429 | GHz |
| 20-08.15e | clock ratio | 5.2 | — |
