# Solutions 11-09 · The z-Transform

Problems: [11-09 problems](../problems/11-09-problems.md) · Chapter: [11-09](../chapters/11-09-z-transform.md). Every number below is recomputed by [verify_11_09.py](../verify/verify_11_09.py), which sums the defining series numerically, runs the difference equations, finds roots with `numpy.roots` and evaluates responses on the unit circle.

---

## Solutions

### Solution 11-09.1

$X_1(z) = 1/(1 - 0.8z^{-1})$ for $\lvert z\rvert > 0.8$ and $X_2(z) = 1/(1 - 0.8z^{-1})$ for $\lvert z\rvert < 0.8$: the same formula, outside and inside the circle through the pole. $X_1(2) = 1/(1 - 0.4)$ = **1.667**. $X_2(0.5) = 1/(1 - 1.6)$ = **−1.667**. At $z = 2$ the series $-\sum_{n\le-1}0.8^n2^{-n} = -\sum_{m\ge1}(2/0.8)^m$ diverges; the formula returns a number, but it is not the transform of $x_2$ there.

### Solution 11-09.2

$X(z) = 1 + 2z^{-1} + 3z^{-2}$, which converges for every $z \ne 0$ (property 3: a finite sequence with samples at $n > 0$). $X(1) = 1 + 2 + 3$ = **6** (the sum) and $X(-1) = 1 - 2 + 3$ = **2** (the alternating sum, the DTFT at π). In positive powers, $X = (z^2 + 2z + 3)/z^2$: zeros at $-1 \pm j\sqrt2$, at distance $\sqrt{1 + 2} = \sqrt3$ = **1.732** from the origin, and a double pole at $z = 0$. Zeros outside the unit circle are allowed (they do not affect stability); they make the filter non-minimum-phase.

### Solution 11-09.3

Pole at $z = 0.9$, zero at $z = -1$. Causal with its only pole inside the unit circle: stable. DC ($z = 1$): $2/0.1$ = **20**. At ω = π/2 ($z = j$, so $z^{-1} = -j$): $\lvert 1 - j\rvert/\lvert 1 + 0.9j\rvert = \sqrt2/\sqrt{1.81}$ = **1.051**. At ω = π ($z = -1$): the zero sits exactly there, so the gain is **0**. A low-pass filter: the pole near $z = 1$ lifts DC, the zero at $z = -1$ kills the highest frequency. Geometrically, at DC the zero is 2 away and the pole 0.1 away, a ratio of 20.

### Solution 11-09.4

Poles at radii 0.5 and 1.5. **$\lvert z\rvert > 1.5$:** causal, unstable (the unit circle is outside the ROC). **$0.5 < \lvert z\rvert < 1.5$:** two-sided, so noncausal, and stable (the ring contains the unit circle). **$\lvert z\rvert < 0.5$:** anticausal and unstable. Residues: at 0.5, $1/(1 - 3)$ = **−0.5**; at 1.5, $1/(1 - 1/3)$ = **1.5**. In the stable ring, $h[n] = -0.5(0.5)^nu[n] - 1.5(1.5)^nu[-n - 1]$, so $h[0]$ = **−0.5** and $h[-1] = -1.5/1.5$ = **−1**.

### Solution 11-09.5

Residues: at 0.8, $(1 - 0.2/0.8)/(1 + 0.4/0.8) = 0.75/1.5$ = **0.5**; at −0.4, $(1 + 0.2/0.4)/(1 + 0.8/0.4) = 1.5/3$ = **0.5**. The ROC is outside both poles, so

$$
x[n] = 0.5(0.8)^n + 0.5(-0.4)^n, \qquad n \ge 0 .
$$

So $x[0]$ = **1**, $x[1] = 0.4 - 0.2$ = **0.2**, $x[2] = 0.32 + 0.08$ = **0.4**. Long division: the denominator is $1 - 0.4z^{-1} - 0.32z^{-2}$, so $x[n] = b_n + 0.4x[n - 1] + 0.32x[n - 2]$: $x[0] = 1$, $x[1] = -0.2 + 0.4 = 0.2$, $x[2] = 0.08 + 0.32 = 0.4$. They agree.

### Solution 11-09.6

The recursion is $x[n] = \delta[n] + x[n - 1] - 0.5x[n - 2]$: $x[0]$ = **1**, $x[1]$ = **1**, $x[2] = 1 - 0.5$ = **0.5**, $x[3] = 0.5 - 0.5$ = **0**, $x[4] = 0 - 0.25$ = **−0.25**. Poles: $z^2 - z + 0.5 = 0$ gives $z = 0.5 \pm 0.5j$, radius $\sqrt{0.5}$ = **0.7071** and angle π/4. The formula gives $x[4] = 0.7071^4\sin(5\pi/4)/\sin(\pi/4) = 0.25 \times (-1)$, the same −0.25.

### Solution 11-09.7

$Y(z) - 0.8[z^{-1}Y(z) + y[-1]] = 1/(1 - z^{-1})$, so

$$
Y(z) = \frac{-4}{1 - 0.8z^{-1}} + \frac{1}{(1 - 0.8z^{-1})(1 - z^{-1})} .
$$

Zero-input: $-4(0.8)^n$. Zero-state: residues $1/(1 - 0.8) = 5$ at $z = 1$ and $1/(1 - 1.25) = -4$ at 0.8, so $5 - 4(0.8)^n$. Total: $y[n] = 5 - 8(0.8)^n$. Then $y[0]$ = **−3** (check: $0.8 \times (-5) + 1$), $y[1]$ = **−1.4**, and the final value is **5**. Within 1% means $8(0.8)^n < 0.05$, or $n > \ln(0.00625)/\ln 0.8 = 22.74$: first at $n$ = **23**.

### Solution 11-09.8

$H(z) = 1 - z^{-4} = (z^4 - 1)/z^4$: zeros at the four fourth roots of unity, $z = 1, j, -1, -j$, and four poles at $z = 0$ (an FIR filter, always stable). On the unit circle the zeros at angles 0, π/2 and π remove **0**, **2** and **4** kHz (DC, $f_s/4$ and $f_s/2$). $\lvert H(e^{j\omega})\rvert = \lvert 1 - e^{-j4\omega}\rvert = 2\lvert\sin 2\omega\rvert$, whose largest value **2** occurs at ω = π/4 and 3π/4, that is at **1** kHz and 3 kHz, halfway between the nulls.

### Solution 11-09.9

$\theta = 2\pi \times 1000/16\,000$ = **0.3927** rad/sample. The bandwidth in rad/sample is $2\pi \times 50/16\,000 = 0.01963$, so $1 - r = 0.009817$ and $r$ = **0.9902**. Then $a_1 = -2r\cos\theta$ = **−1.8296** and $a_2 = r^2$ = **0.9805**. Numerically, $1/\lvert A(e^{j\omega})\rvert$ peaks at **999.7** Hz with gain **133.7**, and its −3 dB bandwidth is **50.28** Hz: the estimate $2(1 - r)$ is excellent at this radius. The peak gain of about $1/[(1 - r)\cdot2\sin\theta]$ is why resonators are usually scaled by $(1 - r)$ or given zeros, to keep their gain near 1.

### Solution 11-09.10

- (i) $\lvert a_2\rvert = 0.95 < 1$ and $1.9 < 1.95$: **stable**, with margin $1 + a_2 - \lvert a_1\rvert$ = **0.05** (poles near $z = 1$).
- (ii) $\lvert a_2\rvert = 1.2 > 1$: **unstable** (the product of the roots exceeds 1).
- (iii) $1.6 > 1 + 0.55$: **unstable**. $P(1) = 1 - 1.6 + 0.55$ = **−0.05** < 0, so a real root exceeds 1: the roots of $z^2 - 1.6z + 0.55$ are 0.5 and **1.1**.
- (iv) $\lvert a_2\rvert = 0.3$ and $1.0 < 1.3$: **stable**. Since $a_1^2 = 1 < 4a_2 = 1.2$, the poles are complex, with radius $\sqrt{0.3}$ = **0.5477**.

### Solution 11-09.11

(a) $T = 10^{-4}$ s, and $h[n] = Te^{-1000nT} = T(e^{-0.1})^n$, so $H(z) = T/(1 - e^{-0.1}z^{-1})$: the pole is $e^{-0.1}$ = **0.9048** (from $z = e^{sT}$). The DC gain is $T/(1 - 0.9048)$ = **1.051** × 10⁻³, against the analog $1/1000$: **5.1**% high, because impulse invariance aliases the response's tail back onto DC.

(b) $z = (1 + sT/2)/(1 - sT/2)$ with $sT/2 = -0.05$: the pole is $0.95/1.05$ = **0.9048** as well (to four digits). DC maps to $z = 1$, so the DC gain is exactly 1/1000. The corner maps to $\omega = 2\arctan(1000T/2)$ = **0.09992** rad/sample, against $\Omega T = 0.1$: warping is negligible because the corner is far below the sample rate.

### Solution 11-09.12

The width in rad/sample is $2\pi \times 1/500 = 0.01257$, so $1 - r = 0.006283$ and $r$ = **0.9937**. The exact −3 dB width is **1.003** Hz. The transient's time constant is $-1/\ln r$ = **158.7** samples, **0.3173** s, and decaying to 1% takes $\ln 0.01/\ln r$ = **731** samples, **1.461** s. The cost of a narrow notch is time: it takes over a second to adapt when the hum's amplitude or phase changes, and an ECG front end must decide whether that settling is acceptable.

### Solution 11-09.13

With $q = 2^{-8}$, the largest $a_2$ below 1 is $1 - q$, so $r = \sqrt{1 - q}$ = **0.99804**. The realizable values of $\lvert a_1\rvert$ are multiples of $2^{-8}$; just below $2r$ = **1.99609** the largest is $510/256 = 2 - 2q$ = **1.9922** (the next one, 511/256, exceeds $2r$ and would put the poles on the real axis). The smallest angle is $\arccos(1.9922/2r)$ = **0.06254** rad/sample: **477.8** Hz at 48 kHz and **79.63** Hz at 8 kHz. Below those frequencies the coefficients cannot place a pole near the unit circle at all with 8 fractional bits.

### Solution 11-09.14

(a) $1 - z^{-8} = (z^8 - 1)/z^8$ has zeros at the eight eighth roots of unity. The pole of $1/(1 - z^{-1})$ at $z = 1$ cancels the zero at $z = 1$, leaving zeros at $e^{j2\pi k/8}$ for $k = 1, \ldots, 7$ and seven poles at the origin: an 8-tap FIR boxcar.

(b) DC gain: $\frac18 \times 8$ = **1** (the sum of the taps). First null: ω = 2π/8 = **0.25**π. At π/8, $\lvert H\rvert = \lvert\sin(8\omega/2)/(8\sin(\omega/2))\rvert = 1/(8\sin(\pi/16))$ = **0.6407**, or **−3.87** dB.

(c) Three in cascade: $0.6407^3$ = **0.2630**, or **−11.60** dB. Cubing deepens the nulls and attenuates everything between them, which is why sinc³ filters are used before decimation (the ADS1292R's filter is this with $N$ = 256 at its default rate).

(d) In wraparound (two's-complement) arithmetic every register computes its value modulo $2^W$. The comb subtracts two integrator outputs taken $N$ samples apart; that difference equals the true boxcar sum, which is bounded, so as long as $W$ bits can represent the output range, the modular difference is exactly right even though the integrator itself has wrapped many times. The unbounded growth of the marginally stable integrator never reaches the output; it would if the arithmetic saturated instead of wrapping, or if the coefficients were not exact.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 11-09.1a | X₁(2) | 1.667 | — |
| 11-09.1b | X₂(0.5) | −1.667 | — |
| 11-09.2a | X(1) | 6 | — |
| 11-09.2b | X(−1) | 2 | — |
| 11-09.2c | zero distance from the origin | 1.732 | — |
| 11-09.3a | DC gain | 20 | — |
| 11-09.3b | gain at π/2 | 1.051 | — |
| 11-09.3c | gain at π | 0 | — |
| 11-09.4a | residue at 0.5 | −0.5 | — |
| 11-09.4b | residue at 1.5 | 1.5 | — |
| 11-09.4c | stable h[0] | −0.5 | — |
| 11-09.4d | stable h[−1] | −1 | — |
| 11-09.5a | residue at 0.8 | 0.5 | — |
| 11-09.5b | residue at −0.4 | 0.5 | — |
| 11-09.5c | x[0] | 1 | — |
| 11-09.5d | x[1] | 0.2 | — |
| 11-09.5e | x[2] | 0.4 | — |
| 11-09.6a | x[0] | 1 | — |
| 11-09.6b | x[1] | 1 | — |
| 11-09.6c | x[2] | 0.5 | — |
| 11-09.6d | x[3] | 0 | — |
| 11-09.6e | x[4] | −0.25 | — |
| 11-09.6f | pole radius | 0.7071 | — |
| 11-09.7a | y[0] | −3 | — |
| 11-09.7b | y[1] | −1.4 | — |
| 11-09.7c | final value | 5 | — |
| 11-09.7d | first n within 1% | 23 | — |
| 11-09.8a | null at DC | 0 | kHz |
| 11-09.8b | null at f_s/4 | 2 | kHz |
| 11-09.8c | null at f_s/2 | 4 | kHz |
| 11-09.8d | largest gain | 2 | — |
| 11-09.8e | first frequency of largest gain | 1 | kHz |
| 11-09.9a | θ | 0.3927 | rad/sample |
| 11-09.9b | r | 0.9902 | — |
| 11-09.9c | a₁ | −1.8296 | — |
| 11-09.9d | a₂ | 0.9805 | — |
| 11-09.9e | peak frequency | 999.7 | Hz |
| 11-09.9f | peak gain | 133.7 | — |
| 11-09.9g | exact bandwidth | 50.28 | Hz |
| 11-09.9h | bandwidth in rad/sample | 0.01963 | rad/sample |
| 11-09.9i | 1 − r | 0.009817 | — |
| 11-09.10a | margin of (i) | 0.05 | — |
| 11-09.10b | P(1) of (iii) | −0.05 | — |
| 11-09.10c | offending root of (iii) | 1.1 | — |
| 11-09.10d | pole radius of (iv) | 0.5477 | — |
| 11-09.11a | impulse-invariant pole | 0.9048 | — |
| 11-09.11b | impulse-invariant DC gain | 1.051 | 10⁻³ |
| 11-09.11c | DC gain error | 5.1 | % |
| 11-09.11d | bilinear pole | 0.9048 | — |
| 11-09.11e | mapped corner | 0.09992 | rad/sample |
| 11-09.12a | r | 0.9937 | — |
| 11-09.12b | exact width | 1.003 | Hz |
| 11-09.12c | time constant | 158.7 | samples |
| 11-09.12d | time constant | 0.3173 | s |
| 11-09.12e | samples to 1% | 731 | — |
| 11-09.12f | time to 1% | 1.461 | s |
| 11-09.12g | width in rad/sample | 0.01257 | rad/sample |
| 11-09.12h | 1 − r | 0.006283 | — |
| 11-09.13a | r | 0.99804 | — |
| 11-09.13b | largest a₁ magnitude | 1.9922 | — |
| 11-09.13c | smallest angle | 0.06254 | rad/sample |
| 11-09.13d | at 48 kHz | 477.8 | Hz |
| 11-09.13e | at 8 kHz | 79.63 | Hz |
| 11-09.13f | 2r | 1.99609 | — |
| 11-09.14a | DC gain | 1 | — |
| 11-09.14b | first null | 0.25 | π rad/sample |
| 11-09.14c | gain at π/8 | 0.6407 | — |
| 11-09.14d | gain at π/8 | −3.87 | dB |
| 11-09.14e | sinc³ gain at π/8 | 0.2630 | — |
| 11-09.14f | sinc³ gain at π/8 | −11.60 | dB |
