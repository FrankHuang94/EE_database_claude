# Solutions 01-06 · Techniques of Integration

Problems: [01-06 problems](../problems/01-06-problems.md) · Chapter: [01-06](../chapters/01-06-techniques-of-integration.md)

Every numerical answer below is listed in the answer key at the end and is recomputed independently by [verify_01_06.py](../verify/verify_01_06.py).

---

## Solutions

### Solution 01-06.1

(a) $u = 3x$, $du = 3\,dx$, limits $0 \to \pi/2$: $\tfrac{1}{3}\int_0^{\pi/2}\cos u\,du = \tfrac{1}{3}\big[\sin u\big]_0^{\pi/2} = $ **0.3333**.

(b) $u = x^2 + 5$, $du = 2x\,dx$, limits $5 \to 9$: $\tfrac{1}{2}\int_5^9u^{1/2}\,du = \tfrac{1}{3}\big[u^{3/2}\big]_5^9 = \tfrac{1}{3}(27 - 11.180) = $ **5.273**.

(c) $u = \ln x$, $du = dx/x$, limits $0 \to 1$: $\int_0^1u\,du = $ **0.5**.

(d) $u = \cos x$, $du = -\sin x\,dx$: $\big[-\ln\cos x\big]_0^{\pi/4} = -\ln(1/\sqrt{2}) = \tfrac{1}{2}\ln 2 = $ **0.3466**.

### Solution 01-06.2

(a) $u = x$, $dv = \sin x\,dx$: $\big[-x\cos x\big]_0^\pi + \int_0^\pi\cos x\,dx = \pi + 0 = $ **3.142**.

(b) $u = \ln x$, $dv = dx$: $\big[x\ln x - x\big]_1^e = (e - e) - (0 - 1) = $ **1**.

(c) Tabular: derivatives of $x^2$ are $2x$, 2, 0; repeated integrals of $e^x$ are $e^x$. The antiderivative is $e^x(x^2 - 2x + 2)$, so the integral is $e(1) - 2 = e - 2 = $ **0.7183**.

(d) $u = \arctan x$, $dv = dx$: $\big[x\arctan x\big]_0^1 - \int_0^1\frac{x}{1 + x^2}dx = \frac{\pi}{4} - \frac{1}{2}\ln 2 = $ **0.4388**. (The last integral is a substitution.)

### Solution 01-06.3

(a) $\int_0^\pi\frac{1 - \cos2x}{2}dx = \frac{\pi}{2} = $ **1.571**.

(b) Orthogonality, since $3 \ne 5$: **0**.

(c) $\int_0^{2\pi}\frac{1 + \cos8x}{2}dx = $ **3.142** (π).

(d) $\int_0^{\pi/2}(1 - \cos^2x)\sin x\,dx$. With $u = \cos x$, the limits run $1 \to 0$: $\int_0^1(1 - u^2)\,du = 1 - \tfrac{1}{3} = $ **0.6667**.

### Solution 01-06.4

(a) $\dfrac{1}{x^2 - 1} = \dfrac{1}{2}\left(\dfrac{1}{x - 1} - \dfrac{1}{x + 1}\right)$, by cover-up at $x = \pm1$. So the integral is $\tfrac{1}{2}\big[\ln\frac{x - 1}{x + 1}\big]_2^3 = \tfrac{1}{2}\left(\ln\tfrac{2}{4} - \ln\tfrac{1}{3}\right) = \tfrac{1}{2}\ln1.5 = $ **0.2027**.

(b) Cover-up: $A = \dfrac{3(-1) + 5}{-1 + 3} = 1$ and $B = \dfrac{3(-3) + 5}{-3 + 1} = 2$. So $\dfrac{1}{x + 1} + \dfrac{2}{x + 3}$, and the integral is $\ln2 + 2\ln\tfrac{4}{3} = $ **1.2685**.

(c) $\dfrac{1}{x(x + 1)^2} = \dfrac{A}{x} + \dfrac{B}{x + 1} + \dfrac{C}{(x + 1)^2}$.

- Cover-up at $x = 0$ gives $A = 1$.
- At $x = -1$ (for the highest power) gives $C = 1/(-1) = -1$.
- Comparing the $x^2$ coefficients after multiplying out, $0 = A + B$, gives $B = -1$.

So the integral is $\big[\ln x - \ln(x + 1) + \frac{1}{x + 1}\big]_1^2 = \ln\tfrac{4}{3} + \left(\tfrac{1}{3} - \tfrac{1}{2}\right) = 0.2877 - 0.1667 = $ **0.1210**.

### Solution 01-06.5

(a) $\big[-1/x\big]_1^\infty = $ **1**: converges ($p = 2 > 1$).
(b) $\big[2\sqrt{x}\big]_1^b \to \infty$: **diverges** ($p = \tfrac{1}{2} \le 1$).
(c) $\big[2\sqrt{x}\big]_\epsilon^1 \to 2$: converges to **2** ($p = \tfrac{1}{2} < 1$ near 0).
(d) $\big[-\tfrac{1}{2}e^{-2t}\big]_0^\infty = $ **0.5**.
(e) By parts twice (or the $n!$ rule): $2! = $ **2**.

### Solution 01-06.6

(a) Elmore delay $= \tau = $ **50 ps**. 50% delay $= \tau\ln2 = $ **34.66 ps**.

(b) Substitute $x = t/\tau$: $\int_0^\infty\frac{t}{\tau^2}e^{-t/\tau}dt = \int_0^\infty xe^{-x}dx = 1! = 1$ ✓. The first moment is $\int_0^\infty t\cdot\frac{t}{\tau^2}e^{-t/\tau}dt = \tau\int_0^\infty x^2e^{-x}dx = 2\tau$. The centroid is $2\tau = $ **100 ps**.

(c) The impulse response of a chain is the convolution of the stages' responses ([11-03](../../11-signals-and-systems/chapters/11-03-convolution.md)), and the centroids of convolved (non-negative, unit-area) functions add. This is why Elmore delays add along a path, and why they are so convenient inside optimization.

### Solution 01-06.7

(a) $W = \tfrac{1}{2}\int_0^\infty e^{-2at}\,dt - \tfrac{1}{2}\int_0^\infty e^{-2at}\cos2bt\,dt$. The first term is $\frac{1}{4a}$. By the loop formula with exponent $-2a$ and frequency $2b$, evaluated from 0 to ∞:

$$
\int_0^\infty e^{-2at}\cos2bt\,dt = \left[\frac{e^{-2at}\big(-2a\cos2bt + 2b\sin2bt\big)}{4a^2 + 4b^2}\right]_0^\infty = \frac{2a}{4(a^2 + b^2)} .
$$

So the second term is $\frac{a}{4(a^2 + b^2)}$, and $W = \frac{1}{4a} - \frac{a}{4(a^2 + b^2)} = \frac{b^2}{4a(a^2 + b^2)}$.

(b) $W = \dfrac{10^6}{400\times1.01\times10^6} = $ **2.475×10^−3 J** (2.475 mJ). The "average ½" approximation gives $1/(4a) = $ **2.5×10^−3 J**, within 1%. The oscillation (1000 rad/s) is ten times faster than the decay (100 s⁻¹), so $\sin^2$ averages out over many cycles before the envelope changes much. The exact factor $b^2/(a^2 + b^2) = 0.990$ measures that ratio.

### Solution 01-06.8

(a) $b_1 = 8/\pi^2 = $ **0.8106**.

(b) The fundamental's power is $b_1^2/2 = 0.3285$, against a total of $1/3$, so the fraction is **98.55%**. A triangle wave is "almost a sine", while a square wave puts 19% of its power in harmonics.

(c) Harmonic amplitudes fall faster the smoother the signal. A square wave jumps (it is discontinuous), so its coefficients fall as $1/n$. A triangle is continuous, but its slope jumps, so its coefficients fall as $1/n^2$. Integrating by parts in the coefficient formula gains one factor of $1/n$ for each derivative that remains continuous. This is the mathematical reason that fast edges spread energy to high frequencies, and why edge-rate control reduces electromagnetic interference ([24-01](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md)).

### Solution 01-06.9

(a) $A = \dfrac{10}{(-2 + 5)} = 10/3 = $ **3.333** and $B = \dfrac{10}{(-5 + 2)} = $ **−3.333**. So $H(s) = \dfrac{10/3}{s + 2} - \dfrac{10/3}{s + 5}$.

(b) $h(t) = \tfrac{10}{3}\left(e^{-2t} - e^{-5t}\right)$ (Figure 4 of the chapter).

(c) $h'(t) = \tfrac{10}{3}(-2e^{-2t} + 5e^{-5t}) = 0$ gives $e^{3t} = 2.5$, so $t = \ln(2.5)/3 = $ **0.3054 s**. The peak is $h = \tfrac{10}{3}(e^{-0.6109} - e^{-1.5272}) = $ **1.086**.

### Solution 01-06.10

(a) $(\pi/2)\times1\text{ kHz} = $ **1.571 kHz**.

(b) $\sqrt{4kTR} = \sqrt{4\times1.380649\times10^{-23}\times300\times1000} = $ **4.070 nV/√Hz**. The RMS noise is $4.070\text{ nV/√Hz}\times\sqrt{1571\text{ Hz}} = $ **0.1613 µV**.

(c) $4kTR\cdot\frac{\pi}{2}\cdot\frac{1}{2\pi RC} = \frac{4kTR}{4RC} = \frac{kT}{C}$. $R$ cancels.

(d) $\sqrt{kT/C} = \sqrt{4.142\times10^{-21}/10^{-12}} = $ **64.36 µV**. A 12-bit ADC with a 1 V range has an LSB of 244 µV, comfortably above this. A 16-bit one has an LSB of 15 µV, below it, which is why high-resolution converters need sampling capacitors of tens of pF or more.

### Solution 01-06.11

(a) $h = 0.25$, with samples $e^{-x^2}$ at 0, 0.25, 0.5, 0.75, 1: 1, 0.93941, 0.77880, 0.56978, 0.36788. Then $S = \frac{0.25}{3}\big[1 + 4(0.93941) + 2(0.77880) + 4(0.56978) + 0.36788\big] = $ **0.74686**, an error of **3.1×10^−5** with just five function evaluations.

(b) $h = \pi/8$, with nine samples of $\sin x/x$ (the first equal to 1). Simpson gives **1.8520**, against the accurate value 1.85194.

(c) $\frac{2}{\pi}\times1.85194 = $ **1.1790**: the partial sums overshoot 1 by 0.179, which is **8.95%** of the jump of 2. The overshoot moves closer to the edge as harmonics are added, but its height never shrinks. Ringing near sharp edges in band-limited systems (and in filtered images) is a practical consequence.

### Solution 01-06.12

(a) $\overline{(A_1\sin\omega t + A_3\sin3\omega t)^2} = A_1^2\overline{\sin^2\omega t} + 2A_1A_3\overline{\sin\omega t\sin3\omega t} + A_3^2\overline{\sin^23\omega t} = \frac{A_1^2}{2} + 0 + \frac{A_3^2}{2}$. The cross term vanishes by orthogonality.

(b) The total mean square is 1 and the fundamental contributes $\tfrac{1}{2}(4/\pi)^2 = 8/\pi^2$. The harmonics therefore contribute $1 - 8/\pi^2$, so $\tfrac{1}{2}\sum_{n\ge3}A_n^2 = 1 - 8/\pi^2$. Then

$$
\text{THD} = \sqrt{\frac{\sum_{n\ge3}A_n^2}{A_1^2}} = \sqrt{\frac{2(1 - 8/\pi^2)}{16/\pi^2}} = \sqrt{\frac{\pi^2}{8} - 1} = \mathbf{0.4834}
$$

i.e. **48.34%**.

(c) $A_3/A_1 = 10^{-4}$, which is $20\log_{10}10^{-4} = $ **−80 dB**.

### Solution 01-06.13

(a) $\int_1^{10^6}\frac{K}{f}df = K\ln10^6 = $ **1.382×10^−11 V²**, so the RMS voltage is **3.717 µV**.

(b) $K\ln10^8 = 1.842\times10^{-11}$ V², so the RMS voltage is **4.292 µV**. Two more decades raised the power by a third but the RMS by only 15%.

(c) $\int_f^{10f}\frac{K}{f'}df' = K\ln10$, the same for every starting frequency $f$: **2.303×10^−12 V²** per decade.

(d) The divergence at $f \to 0$ is logarithmic, so very slow. In a real measurement lasting time $T_{obs}$, frequencies below about $1/T_{obs}$ look like drift rather than noise, and they set the effective lower limit. Each additional decade, for example a measurement 10 times longer, adds the same small amount of power. Designers handle the very-low-frequency part with chopping, autozeroing or periodic calibration.

### Solution 01-06.14

(a) With $u = 1 - v/\phi$, $dv = -\phi\,du$, and the limits $v: 0 \to V$ become $u: 1 \to 1 - V/\phi = 8.143$:

$$
q = \int_1^{8.143}\frac{C_0}{\sqrt{u}}(-\phi\,du) = -2C_0\phi\Big[\sqrt{u}\Big]_1^{8.143} = -2(10\text{ pF})(0.7)(2.8536 - 1) = \mathbf{-25.95\ pC}.
$$

(b) $\lvert q/V\rvert = 25.95/5 = $ **5.190 pF**. The small-signal capacitance is $C(-5) = 10/\sqrt{8.143} = $ **3.504 pF**.

(c) The **small-signal** capacitance, 3.504 pF. For a small swing about the bias, the charge changes by $C(V)\,\Delta v$, the local slope $dq/dv$. The effective (average) capacitance describes a large swing from 0 V, which an RF tuning application does not use. Tuning the bias changes $C(V)$, and with it the frequency.

### Solution 01-06.15

(a) $\displaystyle\int_0^\infty e^{-(s + a)t}dt = \frac{1}{s + a}$ for $s + a > 0$. At $s = 2$, $a = 1$: **0.3333**. If $a < 0$, convergence needs $s > -a$, i.e. $s > \lvert a\rvert$: the decaying factor $e^{-st}$ must beat the growth.

(b) By parts: $\displaystyle\int_0^\infty te^{-st}dt = \frac{1}{s^2}$. At $s = 2$: **0.25**.

(c) By the loop formula (sine version) with exponent $-s$: $\displaystyle\int_0^\infty\sin\omega t\,e^{-st}dt = \frac{\omega}{s^2 + \omega^2}$. At $s = 2$, $\omega = 3$: $3/13 = $ **0.2308**.

These are the Laplace transforms of $e^{-at}$, $t$ and $\sin\omega t$, three entries of the table used throughout circuit analysis ([07-04](../../07-circuit-analysis-2-transient-and-ac/chapters/07-04-laplace-domain-circuit-analysis.md)).

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 01-06.1a | (a) | 0.3333 | — |
| 01-06.1b | (b) | 5.273 | — |
| 01-06.1c | (c) | 0.5 | — |
| 01-06.1d | (d) | 0.3466 | — |
| 01-06.2a | (a) | 3.142 | — |
| 01-06.2b | (b) | 1 | — |
| 01-06.2c | (c) | 0.7183 | — |
| 01-06.2d | (d) | 0.4388 | — |
| 01-06.3a | (a) | 1.571 | — |
| 01-06.3b | (b) | 0 | — |
| 01-06.3c | (c) | 3.142 | — |
| 01-06.3d | (d) | 0.6667 | — |
| 01-06.4a | (a) | 0.2027 | — |
| 01-06.4b | (b) | 1.2685 | — |
| 01-06.4c | (c) | 0.1210 | — |
| 01-06.5a | (a) | 1 | — |
| 01-06.5b | (c) | 2 | — |
| 01-06.5c | (d) | 0.5 | — |
| 01-06.5d | (e) | 2 | — |
| 01-06.6a | Elmore delay, one stage | 50 | ps |
| 01-06.6b | 50 % delay, one stage | 34.66 | ps |
| 01-06.6c | Elmore delay, two stages | 100 | ps |
| 01-06.7a | dissipated energy | 2.475×10^-3 | J |
| 01-06.7b | average-½ approximation | 2.5×10^-3 | J |
| 01-06.8a | triangle fundamental | 0.8106 | — |
| 01-06.8b | power fraction in fundamental | 98.55 | % |
| 01-06.9a | A | 3.333 | — |
| 01-06.9b | B | −3.333 | — |
| 01-06.9c | peak time | 0.3054 | s |
| 01-06.9d | peak value | 1.086 | — |
| 01-06.10a | noise bandwidth | 1.571 | kHz |
| 01-06.10b | noise density of 1 kΩ | 4.070 | nV/√Hz |
| 01-06.10c | RMS noise | 0.1613 | µV |
| 01-06.10d | kT/C noise at 1 pF | 64.36 | µV |
| 01-06.11a | Simpson, e^(−x²) | 0.74686 | — |
| 01-06.11b | Simpson error | 3.1×10^-5 | — |
| 01-06.11c | Simpson, Si(π) | 1.8520 | — |
| 01-06.11d | Gibbs peak | 1.1790 | — |
| 01-06.11e | overshoot as % of jump | 8.95 | % |
| 01-06.12a | square-wave THD | 48.34 | % |
| 01-06.12b | 3rd harmonic at 0.01 % THD | −80 | dB |
| 01-06.13a | power, 1 Hz to 1 MHz | 1.382×10^-11 | V² |
| 01-06.13b | RMS, 1 Hz to 1 MHz | 3.717 | µV |
| 01-06.13c | RMS, 0.01 Hz to 1 MHz | 4.292 | µV |
| 01-06.13d | power per decade | 2.303×10^-12 | V² |
| 01-06.14a | stored charge | −25.95 | pC |
| 01-06.14b | effective capacitance | 5.190 | pF |
| 01-06.14c | small-signal capacitance at −5 V | 3.504 | pF |
| 01-06.15a | (a) | 0.3333 | — |
| 01-06.15b | (b) | 0.25 | — |
| 01-06.15c | (c) | 0.2308 | — |
