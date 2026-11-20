# Problems 16-07 · IIR Filter Design

Chapter: [16-07](../chapters/16-07-iir-filter-design.md) · Worked solutions: [16-07 solutions](../solutions/16-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** The bilinear transform is $s = 2f_s(1 - z^{-1})/(1 + z^{-1})$, so a digital frequency $f_d$ corresponds to the analog frequency $f_a = (f_s/\pi)\tan(\pi f_d/f_s)$. $A_p$ is the maximum passband loss and $A_s$ the minimum stopband attenuation, in dB; $D = (10^{A_s/10} - 1)/(10^{A_p/10} - 1)$. Problems marked *(lab)* need the lab's `iirdesign.py` or an equivalent tool.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 16-07.1 [A]

**Prewarping.** (a) At $f_s$ = 8 kHz, to what analog frequencies must digital band edges at 1, 2 and 3 kHz be prewarped? (b) A designer converts a fourth-order analog Butterworth filter with a 10 kHz cutoff to $f_s$ = 48 kHz with the bilinear transform but forgets to prewarp. Where does the −3 dB point land, and by what percentage is it off?

### Problem 16-07.2 [A]

**Stability is preserved.** (a) Map the analog pole $s = -1000 + j5000$ s⁻¹ to the z-plane with the bilinear transform at $f_s$ = 8 kHz and find its radius. (b) Show in general that $\lvert z\rvert < 1$ if and only if $\text{Re}\,s < 0$.

### Problem 16-07.3 [A]

**Comparing families.** A low-pass specification allows 1 dB of passband loss, requires 40 dB of attenuation, and has $\Omega_s/\Omega_p = 2$ (after prewarping). Compute the discrimination and the minimum Butterworth, Chebyshev and elliptic orders.

### Problem 16-07.4 [B]

**A DC blocker by the bilinear transform.** Map the first-order analog high-pass filter $H_a(s) = s/(s + \Omega_c)$ with $f_c$ = 100 Hz to $f_s$ = 48 kHz, prewarping at 100 Hz. Give $H(z)$, its pole, its high-frequency gain, and its time constant in samples and milliseconds. Compare with the DC blocker of 16-02.

### Problem 16-07.5 [B]

**Butterworth poles.** (a) List the poles of the normalized ($\Omega_c$ = 1) third-order Butterworth filter and write $H(s)$ as a product of a first-order and a second-order factor. (b) Give the angles of the fourth-order poles, and the damping ratio of each pair.

### Problem 16-07.6 [B]

**Chebyshev poles.** For a third-order Chebyshev type I filter with 1 dB ripple and $\Omega_p$ = 1, compute $\varepsilon$, the parameter $a$, the semi-axes $\sinh a$ and $\cosh a$ of the pole ellipse, and the three poles. What is the DC gain?

### Problem 16-07.7 [B]

**Impulse invariance aliases.** Map $H_a(s) = \Omega_c/(s + \Omega_c)$ with $f_c$ = 2 kHz to $f_s$ = 8 kHz by impulse invariance. Find the DC gain, the gain at Nyquist, and their ratio; compare the ratio with the analog filter's gain at 4 kHz relative to DC.

### Problem 16-07.8 [B]

**Group delay of a resonant pair.** An all-pole biquad has poles at $0.95e^{\pm j\pi/4}$. Compute its group delay at $\omega = \pi/4$, and compare with the single-pole approximation $\rho/(1 - \rho)$.

### Problem 16-07.9 [B]

**A sensor filter.** *(lab)* A 1 kHz sensor stream needs a low-pass filter with at most 0.5 dB of loss to 40 Hz and 60 dB of attenuation from 50 Hz (mains hum). (a) Find the minimum elliptic order with prewarped edges. (b) Estimate the order of an equiripple FIR filter for the same specification with Kaiser's formula of 16-06 (take the 0.5 dB as peak to peak). (c) Compare the multiplications per output: the elliptic filter as second-order sections (count with the lab's `mults_sos`) against the folded FIR filter.

### Problem 16-07.10 [C]

**A third-order Butterworth by hand.** Design the third-order Butterworth low-pass filter with a −3 dB frequency of 2 kHz at $f_s$ = 8 kHz. (Hint: the prewarping constant is $K = \tan(\pi/4) = 1$, so $s/\Omega_c$ becomes simply $(1 - z^{-1})/(1 + z^{-1})$.) Derive $H(z)$ in closed form, find its poles, and check the gains at DC and at 2 kHz.

### Problem 16-07.11 [C]

**Can an all-pass rescue linear phase?** *(lab)* The order-8 elliptic filter of Example 16-07.5 has a group delay of 7.99 samples at DC and 69.51 samples at 4 kHz. (a) What is the smallest constant delay an all-pass equalizer could produce across the passband, and how much delay must it add at DC? (b) Compare that delay in milliseconds with the 137-tap FIR filter's. (c) What does this say about IIR filters when linear phase is required?

### Problem 16-07.12 [C]

**One polynomial or four biquads?** *(lab)* Expand the order-8 elliptic filter of Example 16-07.5 into a single denominator polynomial. (a) What is its largest coefficient, and how many integer bits (plus sign) does a fixed-point format need to hold it? (b) Round the polynomial's coefficients to 16, 14, 12 and 10 fractional bits; for each, find the largest pole radius. (c) Repeat with each biquad's coefficients rounded separately, down to 8 fractional bits. (d) Explain the difference.

### Problem 16-07.13 [B]

**A band-pass design by transformation.** A band-pass filter at $f_s$ = 48 kHz must pass 1 to 2 kHz within 1 dB and attenuate by at least 40 dB below 500 Hz and above 4 kHz. (a) Prewarp the four edges. (b) Find the band-pass transformation's centre $\Omega_0$ and bandwidth $B$, and the digital centre frequency. (c) Map both stopband edges to the low-pass prototype and decide which governs. (d) Find the Butterworth prototype order, the band-pass filter's order and its number of biquads.

---

## Objective coverage

| Learning objective (chapter 16-07) | Problems |
|---|---|
| 1. Analog prototypes, orders and poles | 3, 5, 6, 10 |
| 2. Bilinear transform, stability, warping | 1, 2, 4, 10 |
| 3. Impulse invariance and aliasing | 7 |
| 4. Complete IIR designs | 4, 9, 10, 13 |
| 5. Group delay | 8, 11 |
| 6. FIR versus IIR | 9, 11, 12 |
