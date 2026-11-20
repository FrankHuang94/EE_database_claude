# Solutions 16-02 · DTFT and z-Transform for DSP

Problems: [16-02 problems](../problems/16-02-problems.md) · Chapter: [16-02](../chapters/16-02-dtft-and-z-transform-for-dsp.md). Every number below is recomputed by [verify_16_02.py](../verify/verify_16_02.py): frequency responses directly from the coefficients and from the pole–zero vectors, group delays in closed form and by numerical differentiation, band edges by root finding, and impulse responses by simulation.

---

## Solutions

### Solution 16-02.1

$H(z) = (1 - z^{-1})/(1 - 0.8z^{-1}) = (z - 1)/(z - 0.8)$: zero at $z$ = 1, pole at $z$ = 0.8, causal ROC $\lvert z\rvert > 0.8$, which contains the unit circle: stable. At DC the point $z = 1$ sits on the zero: $\lvert H\rvert$ = **0**. At $\pi$, $z = -1$: distance 2 to the zero and 1.8 to the pole, $\lvert H\rvert = 2/1.8$ = **1.111**.

### Solution 16-02.2

Zeros: $1 - z^{-2} = 0$ at $z = \pm1$. Poles: $z^2 = -0.81$, so $z = \pm j0.9$. Both poles are inside the circle.

- $\omega = 0$ and $\omega = \pi$: the point is on a zero: $\lvert H\rvert$ = **0** at both.
- $\omega = \pi/2$ ($z = j$): zero distances $\lvert j - 1\rvert = \lvert j + 1\rvert = \sqrt2$, product 2; pole distances $\lvert j - j0.9\rvert = 0.1$ and $\lvert j + j0.9\rvert = 1.9$, product 0.19. $\lvert H\rvert = 2/0.19$ = **10.53**.

### Solution 16-02.3

Poles at 0.5 and 2. The ROC is an annulus bounded by poles: (i) $\lvert z\rvert < 0.5$ (left-sided, anticausal, unstable), (ii) $0.5 < \lvert z\rvert < 2$ (two-sided, contains the unit circle: **stable**, not causal), (iii) $\lvert z\rvert > 2$ (right-sided, **causal**, unstable). No ROC is both.

Partial fractions: $H = A/(1 - 0.5z^{-1}) + B/(1 - 2z^{-1})$ with $A = 1/(1 - 2/0.5) = -1/3$ and $B = 1/(1 - 0.5/2) = 4/3$. In ROC (ii) the pole at 0.5 gives a right-sided term and the pole at 2 a left-sided one (11-09):

$$
h[n] = -\tfrac13(0.5)^n u[n] - \tfrac43\,2^n u[-n-1] .
$$

So $h[0] = -1/3$ = **−0.333**, and $h[-1] = -\tfrac43 \times 2^{-1}$ = **−0.667**.

### Solution 16-02.4

$\lvert H\rvert$ at $\pi$ is $2/(1 + a)$. Near DC the zero at 1 gives a distance $\approx\omega$ and the pole at $a$ a distance $\approx\sqrt{(1 - a)^2 + \omega^2}$, so the corner is where $\omega \approx 1 - a$: $1 - a \approx 2\pi \times 20/48{,}000 = 0.002618$, $a \approx$ **0.997382**. Solving $\lvert H(e^{j\omega})\rvert = (2/(1 + a))/\sqrt2$ exactly: this $a$ gives a −3 dB point of **20.03** Hz, and the $a$ that gives exactly 20 Hz is **0.997385**. The estimate is excellent because $1 - a$ is tiny.

### Solution 16-02.5

The width rule $\Delta\omega \approx 2(1 - r)$ with $\Delta\omega = 2\pi \times 2/1000$ gives $r = 1 - 0.006283$ = **0.99372**. With $\omega_0 = 2\pi \times 60/1000$, the denominator is $1 - 2r\cos\omega_0z^{-1} + r^2z^{-2} = 1 - $ **1.84787** $z^{-1} +$ **0.98747** $z^{-2}$; the numerator $1 - 2\cos\omega_0z^{-1} + z^{-2}$, scaled by $g$ for unit DC gain, is **0.99400** $-$ **1.84839** $z^{-1} +$ **0.99400** $z^{-2}$. The exact −3 dB width is **2.01** Hz.

The time constant is $-1/\ln r$ = **158.7** samples (0.159 s). Wise? Mains frequency in many grids is held within a fraction of a hertz, but a 2 Hz notch is centred on 60 Hz only to within its width; a drift of ±1 Hz would sit at the band edge. The long transient also means the notch takes about half a second to reach full depth. A wider notch, or an adaptive one that tracks the mains frequency, is usually better.

### Solution 16-02.6

Rules: peak $\approx 1/(1 - r)$ = 20 and $Q \approx \omega_0/[2(1 - r)] = (\pi/3)/0.1$ = **10.47**. Exactly: at $\omega_0$ the zero distances multiply to $2\sin(\pi/3) = 1.7321$; the near pole is 0.05 away and the far pole $\lvert e^{j\pi/3} - 0.95e^{-j\pi/3}\rvert = 1.6889$ away, so the gain at $\omega_0$ is $1.7321/(0.05 \times 1.6889)$ = **20.51**. A fine search gives the peak, also **20.51**, at **1.0480** rad/sample (just above $\pi/3 = 1.0472$); the −3 dB bandwidth is **0.1024** rad/sample, so $Q$ = **10.23**.

### Solution 16-02.7

A pole at $\rho = 0.9$, $\theta = 0$ contributes $-\tau_{zero}$ from §3.4: $\tau(\omega) = (\rho\cos\omega - \rho^2)/(1 - 2\rho\cos\omega + \rho^2)$. At DC: $(0.9 - 0.81)/(0.01)$ = **9** samples, the long ringing of a pole near $z = 1$ seen as delay. At $\pi$: $(-0.9 - 0.81)/(1 + 1.8 + 0.81) = -1.71/3.61$ = **−0.474** samples. The negative value is legitimate: far from the pole, its phase lag is *decreasing* with frequency (the pole's phase rises back toward zero as $\omega$ approaches $\pi$), and group delay is minus the slope.

### Solution 16-02.8

$h[n] = h[2 - n]$: symmetric with $N$ = 3, so by §3.4, $H(e^{j\omega}) = e^{-j\omega}(-2.5 + 2\cos\omega)$, a real function times $e^{-j\omega}$: linear phase, group delay **1** sample. Zeros of $1 - 2.5z^{-1} + z^{-2}$, that is of $z^2 - 2.5z + 1$: $z = 2$ and $z = 0.5$, a reciprocal pair, as linear phase requires. Gains: DC $\lvert 1 - 2.5 + 1\rvert$ = **0.5**; $\pi$: $\lvert 1 + 2.5 + 1\rvert$ = **4.5**.

### Solution 16-02.9

$1 - 2.5z^{-1} + z^{-2} = (1 - 0.5z^{-1})(1 - 2z^{-1})$. Reflecting the zero at 2 to 0.5 multiplies the magnitude by $1/2$, so multiply the gain by 2: $H_{min} = 2(1 - 0.5z^{-1})^2$, so $h_{min}$ = **(2, −2, 0.5)**. Reflecting the zero at 0.5 to 2 instead gives the time-reverse, $h_{max}$ = **(0.5, −2, 2)**. All three have total energy $1 + 6.25 + 1 = 4 + 4 + 0.25 = 8.25$.

| Filter | First-sample energy fraction | Group delay at DC |
|---|---|---|
| minimum phase (2, −2, 0.5) | 4/8.25 = **0.485** | **−2** samples |
| linear phase (1, −2.5, 1) | 1/8.25 = **0.121** | **1** sample |
| maximum phase (0.5, −2, 2) | 0.25/8.25 = **0.0303** | **4** samples |

Each reflection of a zero at radius 0.5 adds the all-pass delay $(1 + 0.5)/(1 - 0.5) = 3$ samples at DC: $-2 + 3 = 1$ and $1 + 3 = 4$.

### Solution 16-02.10

DC delay $(1 + a)/(1 - a) = 0.5$ gives $1 + a = 0.5 - 0.5a$, so $a$ = **−1/3** (−0.3333). At $\pi$: $(1 - a)/(1 + a) = (4/3)/(2/3)$ = **2** samples. At $\omega = \pi/4$ the all-pass phase is **−23.40**°, against $-0.5 \times 45° = -22.5°$ for an ideal half-sample delay: an error of **−0.90**°. The approximation is good at low frequencies and degrades toward Nyquist, which is why fractional-delay filters are run oversampled or use higher orders.

### Solution 16-02.11

(a) $C(z) = 0.6 + z^{-1} = 0.6(1 + z^{-1}/0.6)$: zero at $-1/0.6 = -1.667$, outside the circle: **not** minimum phase.

(b) By Example 16-02.5's algebra the residual after $K$ taps is $0.6^K$. $0.6^9 = 0.0101$ is just above 1% and $0.6^{10}$ = **0.0060** is below it: $K$ = **10** taps. The equalized main tap arrives at delay 10, against 1 for the channel's main cursor: **9** symbols of added latency.

(c) The mirror channel $1 + 0.6z^{-1}$ is minimum phase; the truncated causal inverse $\sum_{k=0}^{K-1}(-0.6)^kz^{-k}$ convolved with it gives $1 - (-0.6)^Kz^{-K}$: the same residual $0.6^K$ after the main tap, so the same **10** taps, but **0** symbols of added latency.

### Solution 16-02.12

The zero at 3 lies outside the circle; reflect it to 1/3 and scale by 3: $1 - 3z^{-1} = -3(z^{-1} - \tfrac13)$, so

$$
H = \underbrace{\frac{3(1 - \tfrac13z^{-1})}{1 - 0.5z^{-1}}}_{H_{min}}\cdot\underbrace{\left(-\frac{z^{-1} - \tfrac13}{1 - \tfrac13z^{-1}}\right)}_{H_{ap}} .
$$

The minus sign is a constant phase of 180°, with no effect on group delay.

- $H_{ap}$ ($a = 1/3$): DC $(1 + a)/(1 - a)$ = **2**; $\pi$: $(1 - a)/(1 + a)$ = **0.5**.
- $H_{min}$: zero at 1/3 contributes $-\tfrac{1/3}{2/3} = -0.5$ at DC and $+\tfrac{1/3}{4/3} = 0.25$ at $\pi$; pole at 0.5 contributes $+1$ at DC and $-\tfrac{0.5}{1.5} = -0.333$ at $\pi$. Totals: **0.5** at DC and **−0.0833** at $\pi$.
- $H$: **2.5** at DC and **0.4167** at $\pi$, equal to the sums $0.5 + 2$ and $-0.0833 + 0.5$.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 16-02.1a | gain at DC | 0 | — |
| 16-02.1b | gain at π | 1.111 | — |
| 16-02.2a | gain at π/2 | 10.53 | — |
| 16-02.2b | gain at DC | 0 | — |
| 16-02.3a | h[0] | −0.333 | — |
| 16-02.3b | h[−1] | −0.667 | — |
| 16-02.4a | estimated a | 0.997382 | — |
| 16-02.4b | −3 dB point with the estimate | 20.03 | Hz |
| 16-02.4c | exact a for 20 Hz | 0.997385 | — |
| 16-02.5a | r | 0.99372 | — |
| 16-02.5b | a1 magnitude | 1.84787 | — |
| 16-02.5c | a2 | 0.98747 | — |
| 16-02.5d | scaled b0 = b2 | 0.99400 | — |
| 16-02.5e | scaled b1 magnitude | 1.84839 | — |
| 16-02.5f | exact −3 dB width | 2.01 | Hz |
| 16-02.5g | time constant | 158.7 | samples |
| 16-02.6a | rule-of-thumb Q | 10.47 | — |
| 16-02.6b | gain at ω0 | 20.51 | — |
| 16-02.6c | peak gain | 20.51 | — |
| 16-02.6d | peak frequency | 1.0480 | rad/sample |
| 16-02.6e | −3 dB bandwidth | 0.1024 | rad/sample |
| 16-02.6f | Q | 10.23 | — |
| 16-02.7a | group delay at DC | 9 | samples |
| 16-02.7b | group delay at π | −0.474 | samples |
| 16-02.8a | group delay | 1 | samples |
| 16-02.8b | gain at DC | 0.5 | — |
| 16-02.8c | gain at π | 4.5 | — |
| 16-02.9a | first-sample fraction, minimum phase | 0.485 | — |
| 16-02.9b | first-sample fraction, linear phase | 0.121 | — |
| 16-02.9c | first-sample fraction, maximum phase | 0.0303 | — |
| 16-02.9d | DC group delay, minimum phase | −2 | samples |
| 16-02.9e | DC group delay, maximum phase | 4 | samples |
| 16-02.10a | all-pass coefficient a | −0.3333 | — |
| 16-02.10b | group delay at π | 2 | samples |
| 16-02.10c | phase at π/4 | −23.40 | ° |
| 16-02.10d | phase error at π/4 | −0.90 | ° |
| 16-02.11a | residual with 10 taps | 0.0060 | — |
| 16-02.11b | taps for residual below 1% | 10 | — |
| 16-02.11c | added latency | 9 | symbols |
| 16-02.12a | all-pass delay at DC | 2 | samples |
| 16-02.12b | all-pass delay at π | 0.5 | samples |
| 16-02.12c | minimum-phase delay at DC | 0.5 | samples |
| 16-02.12d | minimum-phase delay at π | −0.0833 | samples |
| 16-02.12e | total delay at DC | 2.5 | samples |
| 16-02.12f | total delay at π | 0.4167 | samples |
