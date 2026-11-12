# Solutions 02-01 · Complex Numbers, Euler's Formula and Phasors

Problems: [02-01 problems](../problems/02-01-problems.md) · Chapter: [02-01](../chapters/02-01-complex-numbers-euler-and-phasors.md)

Every numerical answer below is listed in the answer key at the end and is recomputed independently by [verify_02_01.py](../verify/verify_02_01.py).

---

## Solutions

### Solution 02-01.1

**Method.** $r = \sqrt{x^2 + y^2}$. For the angle, sketch the point, then use $\operatorname{atan2}(y, x)$, which is $\arctan(y/x)$ corrected for the quadrant (chapter §3.3).

(a) $-3 + j3$ is in quadrant II. $r = \sqrt{9 + 9} = \sqrt{18} = 4.243$. $\arctan(3/(-3)) = -45^\circ$ points into quadrant IV, the wrong way, so add $180^\circ$: $\theta = 135^\circ$. **Answer: $4.243\angle 135^\circ$.**

(b) $-2 - j5$ is in quadrant III. $r = \sqrt{4 + 25} = \sqrt{29} = 5.385$. $\arctan(-5/-2) = \arctan(2.5) = 68.20^\circ$ points into quadrant I, so subtract $180^\circ$: $\theta = 68.20^\circ - 180^\circ = -111.80^\circ$. **Answer: $5.385\angle -111.80^\circ$.**

(c) $j7$ lies on the positive imaginary axis: $r = 7$, $\theta = 90^\circ$. **Answer: $7\angle 90^\circ$.**

(d) $-4$ lies on the negative real axis: $r = 4$, $\theta = 180^\circ$ (the principal value includes $+180^\circ$). **Answer: $4\angle 180^\circ$.**

### Solution 02-01.2

**Method.** $x = r\cos\theta$, $y = r\sin\theta$.

(a) $10\cos 120^\circ = 10(-0.5) = -5.000$; $10\sin 120^\circ = 10(0.8660) = 8.660$. **Answer: $-5.000 + j8.660$.**

(b) $2e^{-j\pi/3} = 2\angle -60^\circ$: $2\cos(-60^\circ) = 1.000$, $2\sin(-60^\circ) = -1.732$. **Answer: $1.000 - j1.732$.**

(c) $5\angle -90^\circ$: $5\cos(-90^\circ) = 0$, $5\sin(-90^\circ) = -5$. **Answer: $-j5$.**

(d) $0.5\angle 210^\circ$: $0.5\cos 210^\circ = 0.5(-0.8660) = -0.4330$; $0.5\sin 210^\circ = 0.5(-0.5) = -0.2500$. **Answer: $-0.4330 - j0.2500$** (quadrant III, as 210° should be). Note that $210^\circ$ and $-150^\circ$ are the same direction.

### Solution 02-01.3

The powers of $j$ repeat every 4: $j^1 = j$, $j^2 = -1$, $j^3 = -j$, $j^4 = 1$.

(a) $j^7 = j^4\cdot j^3 = -j$.
(b) $j^{-3} = 1/j^3 = 1/(-j) = -1/j = -(-j) = j$, using $1/j = -j$. Alternatively, $j^{-3} = j^{-4}j^{1} = j$.
(c) $1/j = \dfrac{1}{j}\cdot\dfrac{-j}{-j} = \dfrac{-j}{-j^2} = \dfrac{-j}{1} = -j$.
(d) $(1 + j)(1 - j) = 1 - j + j - j^2 = 1 + 1 = 2$. This is $zz^{\ast} = \lvert z\rvert^2$ with $\lvert 1 + j\rvert^2 = 2$.
(e) $2026 = 4\times 506 + 2$, so $j^{2026} = (j^4)^{506}j^2 = -1$.

### Solution 02-01.4

(a) Already in cosine form: $\mathbf{V} = 12\angle -45^\circ$ V (at $\omega = 377$ rad/s, which is 60 Hz).

(b) $-\sin x = \cos(x + 90^\circ)$, so $-3\sin(2\pi\cdot 50\,t) = 3\cos(2\pi\cdot 50\,t + 90^\circ)$: $\mathbf{I} = 3\angle 90^\circ = j3$ A.

(c) $\sin x = \cos(x - 90^\circ)$, so $4\sin(\omega t + 60^\circ) = 4\cos(\omega t - 30^\circ)$: $\mathbf{V} = 4\angle -30^\circ$ V.

(d) $v(t) = \operatorname{Re}\lbrace 8e^{-j150^\circ}e^{j1000t}\rbrace = 8\cos(1000t - 150^\circ)$ V.

(e) $-j2 = 2\angle -90^\circ$, so $i(t) = 2\cos(\omega t - 90^\circ) = 2\sin\omega t$ A.

### Solution 02-01.5

With $z_1 = 2 - j3$ and $z_2 = -1 + j4$, so $z_2^{\ast} = -1 - j4$:

(a) $z_1z_2^{\ast} = (2 - j3)(-1 - j4) = -2 - j8 + j3 + j^2 12 = (-2 - 12) + j(-8 + 3) = -14 - j5$.

(b) $\dfrac{z_1}{z_2} = \dfrac{z_1z_2^{\ast}}{z_2z_2^{\ast}} = \dfrac{-14 - j5}{1 + 16} = -0.8235 - j0.2941$.

(c) $z_1 + z_2 = 1 + j1$, so $\lvert z_1 + z_2\rvert = \sqrt{2} = 1.414$. Compare $\lvert z_1\rvert + \lvert z_2\rvert = \sqrt{13} + \sqrt{17} = 7.73$: magnitudes do not add, because the two arrows point in nearly opposite directions.

(d) $z_1^2 = (2 - j3)^2 = 4 - j12 + j^2 9 = -5 - j12$. Check: $\lvert z_1\rvert^2 = 13$ and $\lvert -5 - j12\rvert = 13$. ✓

(e) $z_1z_2 = (2 - j3)(-1 + j4) = -2 + j8 + j3 - j^2 12 = 10 + j11$, so $\operatorname{Re}\lbrace z_1z_2\rbrace = 10$. Note that $\operatorname{Re}\lbrace z_1\rbrace\operatorname{Re}\lbrace z_2\rbrace = -2 \ne 10$: real parts do not multiply.

(f) From (b): magnitude $\sqrt{0.8235^2 + 0.2941^2} = 0.8745$. The point is in quadrant III, so $\theta = \arctan(0.2941/0.8235) - 180^\circ = 19.65^\circ - 180^\circ = -160.35^\circ$. **Check with the polar rule:** $\lvert z_1\rvert/\lvert z_2\rvert = \sqrt{13}/\sqrt{17} = 0.8745$ ✓. $\angle z_1 - \angle z_2 = (-56.31^\circ) - (104.04^\circ) = -160.35^\circ$ ✓.

### Solution 02-01.6

(a) $z_1z_2 = (ac - bd) + j(ad + bc)$, so

$$
\begin{aligned}
\lvert z_1z_2\rvert^2 &= (ac - bd)^2 + (ad + bc)^2\\
&= a^2c^2 - 2abcd + b^2d^2 + a^2d^2 + 2abcd + b^2c^2\\
&= a^2(c^2 + d^2) + b^2(c^2 + d^2) = (a^2 + b^2)(c^2 + d^2) = \lvert z_1\rvert^2\lvert z_2\rvert^2 .
\end{aligned}
$$

Both sides are non-negative, so taking square roots gives $\lvert z_1z_2\rvert = \lvert z_1\rvert\lvert z_2\rvert$. ∎

(b) Let $q = z_1/z_2$, so $z_1 = qz_2$. By (a), $\lvert z_1\rvert = \lvert q\rvert\lvert z_2\rvert$, hence $\lvert q\rvert = \lvert z_1\rvert/\lvert z_2\rvert$ (allowed because $\lvert z_2\rvert \ne 0$). ∎

(c) $(z_1z_2)^{\ast} = (ac - bd) - j(ad + bc)$. And $z_1^{\ast}z_2^{\ast} = (a - jb)(c - jd) = ac - jad - jbc + j^2bd = (ac - bd) - j(ad + bc)$. They are equal. ∎ (In polar form this is immediate: conjugation negates angles, and negated angles still add.)

### Solution 02-01.7

(a) By Euler and De Moivre, $\cos 3\theta + j\sin 3\theta = e^{j3\theta} = (e^{j\theta})^3 = (\cos\theta + j\sin\theta)^3$. Let $c = \cos\theta$, $s = \sin\theta$ and expand with the binomial theorem:

$$
(c + js)^3 = c^3 + 3c^2(js) + 3c(js)^2 + (js)^3 = c^3 + j3c^2s - 3cs^2 - js^3 .
$$

The real part is $c^3 - 3cs^2$. Equating real parts and using $s^2 = 1 - c^2$:

$$
\cos 3\theta = c^3 - 3c(1 - c^2) = 4c^3 - 3c = 4\cos^3\theta - 3\cos\theta. \quad\blacksquare
$$

(Equating imaginary parts gives $\sin 3\theta = 3\sin\theta - 4\sin^3\theta$ for free.)

(b) Use $\sin x = (e^{jx} - e^{-jx})/(2j)$ for both factors:

$$
\sin\alpha\sin\beta = \frac{(e^{j\alpha} - e^{-j\alpha})(e^{j\beta} - e^{-j\beta})}{(2j)^2}
= \frac{e^{j(\alpha+\beta)} - e^{j(\alpha-\beta)} - e^{-j(\alpha-\beta)} + e^{-j(\alpha+\beta)}}{-4}.
$$

Group conjugate pairs using $e^{jx} + e^{-jx} = 2\cos x$:

$$
\sin\alpha\sin\beta = \frac{2\cos(\alpha+\beta) - 2\cos(\alpha-\beta)}{-4} = \tfrac{1}{2}\big[\cos(\alpha - \beta) - \cos(\alpha + \beta)\big]. \quad\blacksquare
$$

**Engineering meaning.** If $\alpha = \omega_1 t$ and $\beta = \omega_2 t$, multiplying two sinusoids (what a mixer does) creates components at $\omega_1 - \omega_2$ and $\omega_1 + \omega_2$. Every superheterodyne radio relies on this ([21-05](../../21-rf-and-microwave-engineering/chapters/21-05-mixers.md)).

### Solution 02-01.8

$-8j = 8\angle -90^\circ$. The cube roots have magnitude $8^{1/3} = 2$ and angles $(-90^\circ + 360^\circ k)/3 = -30^\circ + 120^\circ k$ for $k = 0, 1, 2$:

| $k$ | Polar | Rectangular |
|---|---|---|
| 0 | $2\angle -30^\circ$ | $2\cos(-30^\circ) + j2\sin(-30^\circ) = 1.732 - j1.000$ |
| 1 | $2\angle 90^\circ$ | $j2$ |
| 2 | $2\angle 210^\circ = 2\angle -150^\circ$ | $-1.732 - j1.000$ |

They are equally spaced by 120° on a circle of radius 2.

**Verification of $k = 1$:** $(j2)^3 = 8j^3 = 8(-j) = -8j$. ✓

**Note.** The coefficients of $z^3 + 8j$ are not all real, so the roots need not come in conjugate pairs, and they don't.

### Solution 02-01.9

1. Cosine form: $-3\sin\omega t = 3\cos(\omega t + 90^\circ)$.
2. Phasors: $4\angle 60^\circ$, $3\angle 90^\circ$, $2\angle -135^\circ$ (V).
3. Rectangular:
   - $4\angle 60^\circ = 2.000 + j3.464$;
   - $3\angle 90^\circ = 0 + j3.000$;
   - $2\angle -135^\circ = -1.414 - j1.414$.
4. Sum: real part $2.000 + 0 - 1.414 = 0.5858$; imaginary part $3.464 + 3.000 - 1.414 = 5.050$. So $\mathbf{V} = 0.5858 + j5.050$ V.
5. Polar: $\lvert\mathbf{V}\rvert = \sqrt{0.5858^2 + 5.050^2} = 5.084$ V; angle $\arctan(5.050/0.5858) = 83.38^\circ$ (quadrant I).

**Answer:** $v(t) = 5.084\cos(\omega t + 83.38^\circ)$ V.

**Sanity check.** The largest possible amplitude is $4 + 3 + 2 = 9$ V; the result is less, because the arrows partly cancel. The result points mostly "up" (near 90°), as two of the three phasors do. ✓

### Solution 02-01.10

(a) Phase $= 360^\circ \times f \times t_d = 360 \times (100\times10^{6}) \times (1.5\times10^{-9}) = 54.0^\circ$.

(b) Delay $t_d = \dfrac{\ell}{v} = \dfrac{0.050\ \text{m}}{1.5\times10^{8}\ \text{m/s}} = 3.333\times10^{-10}\ \text{s} = 333.3$ ps.
Phase $= 360 \times (2.4\times10^{9}) \times (3.333\times10^{-10}) = 288.0^\circ$ (equivalently $-72^\circ$ as a principal value, but here the total accumulated phase is the physically meaningful number).

(c) $\lambda = v/f = (1.5\times10^{8})/(2.4\times10^{9}) = 0.0625$ m $= 62.50$ mm. The trace is $50/62.5 = 0.8$ wavelengths long, and $0.8 \times 360^\circ = 288^\circ$. ✓

**Engineering meaning.** At 2.4 GHz, a few centimeters of trace is a large fraction of a wavelength. This is the regime where transmission-line effects matter ([13-07](../../13-electromagnetics/chapters/13-07-transmission-lines-time-domain.md)).

### Solution 02-01.11

1. Phasor transform with $\omega = 4$ rad/s: $\frac{d}{dt} \to j4$, so $(2\cdot j4 + 8)\mathbf{Y} = 10\angle 30^\circ$, i.e. $(8 + j8)\mathbf{Y} = 10\angle 30^\circ$.
2. $8 + j8 = 11.31\angle 45^\circ$ (magnitude $8\sqrt{2}$).
3. $\mathbf{Y} = \dfrac{10\angle 30^\circ}{11.31\angle 45^\circ} = 0.8839\angle -15^\circ$.
4. **Answer:** $y_{ss}(t) = 0.8839\cos(4t - 15^\circ)$.

**Verification by substitution.**

- $\dfrac{dy}{dt} = -4(0.8839)\sin(4t - 15^\circ) = 3.536\cos(4t - 15^\circ + 90^\circ) = 3.536\cos(4t + 75^\circ)$.
- Left side: $2(3.536)\cos(4t + 75^\circ) + 8(0.8839)\cos(4t - 15^\circ) = 7.071\cos(4t + 75^\circ) + 7.071\cos(4t - 15^\circ)$.
- As phasors: $7.071\angle 75^\circ + 7.071\angle -15^\circ = (1.830 + j6.830) + (6.830 - j1.830) = 8.660 + j5.000 = 10\angle 30^\circ$. ✓ This equals the right side.

### Solution 02-01.12

(a) $\omega = 2\pi(1000) = 6283$ rad/s, so $\omega L = 6283 \times 0.010 = 62.83\ \Omega$.
$Z = 50 + j62.83\ \Omega$; $\lvert Z\rvert = \sqrt{50^2 + 62.83^2} = 80.30\ \Omega$; $\angle Z = \arctan(62.83/50) = 51.49^\circ$.

(b) $\mathbf{I} = \dfrac{20\angle 0^\circ}{80.30\angle 51.49^\circ} = 0.2491\angle -51.49^\circ$ A, so $i(t) = 0.2491\cos(2\pi\cdot 1000\,t - 51.49^\circ)$ A. The current lags the voltage, as expected in an inductive circuit.

(c) Resistor: $\lvert\mathbf{V}_R\rvert = R\lvert\mathbf{I}\rvert = 50 \times 0.2491 = 12.45$ V.
Inductor: $\lvert\mathbf{V}_L\rvert = \omega L\lvert\mathbf{I}\rvert = 62.83 \times 0.2491 = 15.65$ V.
Their amplitudes sum to 28.1 V, more than 20 V. That is fine, because the two voltages are 90° out of phase ($\mathbf{V}_L = j\omega L\mathbf{I}$ leads $\mathbf{V}_R = R\mathbf{I}$ by 90°) and so never peak at the same instant. KVL holds for the phasors: $\mathbf{V}_R + \mathbf{V}_L = (R + j\omega L)\mathbf{I} = \mathbf{V}_s$. The magnitudes combine like the sides of a right triangle: $\sqrt{12.45^2 + 15.65^2} = 20.0$ V. ✓

### Solution 02-01.13

(a) $\omega_0 = \dfrac{1}{\sqrt{(10^{-3})(10\times10^{-9})}} = \dfrac{1}{\sqrt{10^{-11}}} = 3.162\times10^{5}$ rad/s (316 228 rad/s), and $f_0 = \omega_0/(2\pi) = 50.33$ kHz.

(b) At 25 kHz, $\omega = 1.571\times10^{5}$ rad/s. $X_L = \omega L = 157.1\ \Omega$ and $X_C = 1/(\omega C) = 636.6\ \Omega$.
$Z = 100 + j(157.1 - 636.6) = 100 - j479.5\ \Omega = 489.9\angle -78.22^\circ\ \Omega$.
The reactance is negative, so the circuit is **capacitive** below resonance (the capacitor's impedance dominates at low frequency).

(c) At 100 kHz, $\omega = 6.283\times10^{5}$ rad/s. $X_L = 628.3\ \Omega$ and $X_C = 159.2\ \Omega$.
$Z = 100 + j469.2\ \Omega = 479.7\angle 77.97^\circ\ \Omega$: **inductive** above resonance.

(d) At $f_0$, $X_L = X_C$ (both $316.2\ \Omega$) and $Z = R = 100\ \Omega$, purely resistive and the minimum possible magnitude.

### Solution 02-01.14

(a) Transform with $d/dt \to j\omega$:

$$
\big[(j\omega)^2 + 2\zeta\omega_n(j\omega) + \omega_n^2\big]\mathbf{Y} = \omega_n^2\mathbf{X}
\quad\Rightarrow\quad
H(j\omega) = \frac{\omega_n^2}{\omega_n^2 - \omega^2 + j2\zeta\omega_n\omega}.
$$

Divide the numerator and denominator by $\omega_n^2$ and let $u = \omega/\omega_n$:

$$
H = \frac{1}{(1 - u^2) + j2\zeta u}, \qquad
\lvert H\rvert = \frac{1}{\sqrt{(1 - u^2)^2 + (2\zeta u)^2}}, \qquad
\angle H = -\operatorname{atan2}\big(2\zeta u,\ 1 - u^2\big).
$$

The atan2 matters: above resonance $1 - u^2 < 0$, the denominator is in quadrant II, and the phase lag exceeds 90°.

(b) With $\zeta = 0.1$:

- $\omega = 500$ ($u = 0.5$): denominator $0.75 + j0.10$, magnitude $0.7566$, so $\lvert H\rvert = 1.322$; $\angle H = -\arctan(0.10/0.75) = -7.59^\circ$. **$H = 1.322\angle -7.59^\circ$.**
- $\omega = 1000$ ($u = 1$): denominator $0 + j0.2$, so **$H = 5.000\angle -90.00^\circ$**.
- $\omega = 2000$ ($u = 2$): denominator $-3 + j0.4$ (quadrant II), magnitude $3.027$, so $\lvert H\rvert = 0.3304$; the denominator angle is $180^\circ - 7.59^\circ = 172.41^\circ$. **$H = 0.3304\angle -172.41^\circ$.**

(c) $\lvert H\rvert$ is largest where $D(u) = (1 - u^2)^2 + 4\zeta^2u^2$ is smallest. Treat $D$ as a function of $w = u^2$: $D = (1 - w)^2 + 4\zeta^2 w$. Setting $dD/dw = -2(1 - w) + 4\zeta^2 = 0$ gives $w = 1 - 2\zeta^2$, which is positive only if $\zeta < 1/\sqrt{2}$. So $u_{pk} = \sqrt{1 - 2\zeta^2}$ and $\omega_{pk} = \omega_n\sqrt{1 - 2\zeta^2}$. Substituting back:

$$
D_{min} = (2\zeta^2)^2 + 4\zeta^2(1 - 2\zeta^2) = 4\zeta^2 - 4\zeta^4 = 4\zeta^2(1 - \zeta^2),
\qquad \lvert H\rvert_{max} = \frac{1}{2\zeta\sqrt{1 - \zeta^2}} .
$$

For $\zeta = 0.1$: $\omega_{pk} = 1000\sqrt{0.98} = 989.9$ rad/s and $\lvert H\rvert_{max} = 1/(0.2\times 0.99499) = 5.025$. The peak sits just below $\omega_n$ and is barely higher than the value 5.000 at $\omega_n$.

(d) A lightly damped system amplifies inputs near its resonance by about $1/(2\zeta)$. A chip's power-delivery network (package inductance with on-die capacitance) is such a resonator. If the processor's current demand fluctuates near that resonant frequency, for example a workload that toggles at that rate, the supply voltage can ring far more than the same current step would cause at other frequencies, causing timing failures. Designers add damping (decoupling capacitors with resistance, on-die damping) for this reason ([22-10](../../22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md)).

### Solution 02-01.15

(a) Expand the claimed parts:

$$
k_1 - k_3 = c(a + b) - b(c + d) = ac + bc - bc - bd = ac - bd, \qquad
k_1 + k_2 = c(a + b) + a(d - c) = ac + bc + ad - ac = ad + bc .
$$

These are exactly the real and imaginary parts of $(a + jb)(c + jd)$ from §3.2. ✓

Cost: **3 multiplications** ($k_1, k_2, k_3$) and **5 additions/subtractions** ($a + b$, $d - c$, $c + d$, $k_1 - k_3$, $k_1 + k_2$), against 4 multiplications and 2 additions for the direct form.

(b) If $c + jd$ is a known constant (a twiddle factor), then $d - c$ and $c + d$ are constants too and can be stored in a table. Each multiply then costs **3 real multiplications and 3 additions** ($a + b$, $k_1 - k_3$, $k_1 + k_2$).

(c) Butterflies: $(N/2)\log_2 N = 2048 \times 12 = 24\,576$ complex multiplications.
4-multiplier form: $4 \times 24\,576 = 98\,304$ real multiplications.
3-multiplier form: $3 \times 24\,576 = 73\,728$, a saving of 24 576 (25%).
(Real FFT implementations skip the trivial twiddles $\pm 1$, $\pm j$, so actual counts are lower. The relative saving is the point here.)

(d) Any two of:

- **More adders and a longer critical path:** the pre-addition ($a + b$) sits in series before the multiplier, which can limit clock speed unless an extra pipeline stage is added.
- **Word growth:** $a + b$ needs one more bit than $a$ or $b$, so the multiplier input is wider.
- **Different rounding behavior**, which must be re-analyzed in the quantization-noise budget ([16-10](../../16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md)).
- **Less regular structure:** harder to map onto fixed DSP blocks in an FPGA.

Whether the 25% multiplier saving wins depends on the relative area and energy of multipliers versus adders in the target technology. Multipliers grow roughly with the square of word length and adders linearly, so the saving matters more at wide word lengths.

### Solution 02-01.16

(a) Write each cosine as the real part of an exponential and factor out the average frequency $\bar\omega = (\omega_1 + \omega_2)/2$ with half-difference $\Delta = (\omega_1 - \omega_2)/2$, so that $\omega_1 = \bar\omega + \Delta$ and $\omega_2 = \bar\omega - \Delta$:

$$
e^{j\omega_1t} + e^{j\omega_2t} = e^{j\bar\omega t}\big(e^{j\Delta t} + e^{-j\Delta t}\big) = 2\cos(\Delta t)\,e^{j\bar\omega t}.
$$

Because $2\cos(\Delta t)$ is real, taking real parts gives $\cos\omega_1t + \cos\omega_2t = 2\cos(\Delta t)\cos(\bar\omega t)$. ∎

(b) The fast oscillation is at $(440 + 444)/2 = 442$ Hz. The envelope factor $2\cos(2\pi\cdot 2\,t)$ has frequency 2 Hz, but loudness depends on its **magnitude**, which peaks twice per envelope cycle. The loudness therefore pulses at $444 - 440 = 4$ Hz, with period $1/4 = 0.25$ s. Musicians tune by listening for these beats to slow down and vanish.

(c) A phasor is a snapshot of arrows rotating at one shared rate. Here one arrow rotates 4 turns per second faster than the other, so their relative angle keeps changing. They line up (loud) and oppose (silent) 4 times per second. No fixed complex number can describe that, because the sum's amplitude itself varies in time. Phasor addition requires a common frequency.

### Solution 02-01.17

(a) The product-to-sum identity $\cos A\cos B = \tfrac{1}{2}[\cos(A - B) + \cos(A + B)]$ follows from Euler exactly as in Solution 02-01.7. With $A = \omega t + \theta_v$ and $B = \omega t + \theta_i$:

$$
p(t) = V_mI_m\cos A\cos B = \tfrac{1}{2}V_mI_m\cos(\theta_v - \theta_i) + \tfrac{1}{2}V_mI_m\cos(2\omega t + \theta_v + \theta_i). \quad\blacksquare
$$

(b) The second term oscillates at $2\omega$ and averages to zero over a period, so $P = \tfrac{1}{2}V_mI_m\cos(\theta_v - \theta_i)$. Now compute $\mathbf{V}\mathbf{I}^{\ast} = V_me^{j\theta_v}I_me^{-j\theta_i} = V_mI_me^{j(\theta_v - \theta_i)}$, whose real part is $V_mI_m\cos(\theta_v - \theta_i)$. Therefore $P = \tfrac{1}{2}\operatorname{Re}\lbrace\mathbf{V}\mathbf{I}^{\ast}\rbrace$. ∎

(c) $\theta_v - \theta_i = 30^\circ - (-15^\circ) = 45^\circ$, so
$P = \tfrac{1}{2}(10)(2)\cos 45^\circ = 10 \times 0.7071 = 7.071$ W.
The incorrect quantity: $\mathbf{V}\mathbf{I} = 20\angle 15^\circ$, so $\tfrac{1}{2}\operatorname{Re}\lbrace\mathbf{V}\mathbf{I}\rbrace = 10\cos 15^\circ = 9.659$ W, which is wrong. Average power depends on the angle *between* voltage and current ($\theta_v - \theta_i$), which the conjugate produces. Multiplying phasors directly adds the angles instead, a quantity with no physical meaning here. Units: V × A = W ✓.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 02-01.1a | $-3 + j3$ polar | 4.243∠135.00° | — |
| 02-01.1b | $-2 - j5$ polar | 5.385∠−111.80° | — |
| 02-01.1c | $j7$ polar | 7.000∠90.00° | — |
| 02-01.1d | $-4$ polar | 4.000∠180.00° | — |
| 02-01.2a | $10\angle 120^\circ$ | −5.000 + j8.660 | — |
| 02-01.2b | $2e^{-j\pi/3}$ | 1.000 − j1.732 | — |
| 02-01.2c | $5\angle -90^\circ$ | −j5.000 | — |
| 02-01.2d | $0.5\angle 210^\circ$ | −0.4330 − j0.2500 | — |
| 02-01.3a | $j^7$ | −j1 | — |
| 02-01.3b | $j^{-3}$ | j1 | — |
| 02-01.3c | $1/j$ | −j1 | — |
| 02-01.3d | $(1+j)(1-j)$ | 2 | — |
| 02-01.3e | $j^{2026}$ | −1 | — |
| 02-01.4a | phasor of $12\cos(377t - 45^\circ)$ | 12.00∠−45.00° | V |
| 02-01.4b | phasor of $-3\sin(2\pi 50 t)$ | 3.000∠90.00° | A |
| 02-01.4c | phasor of $4\sin(\omega t + 60^\circ)$ | 4.000∠−30.00° | V |
| 02-01.4d | phase of $v(t)$ for $8\angle -150^\circ$ | −150.0 | ° |
| 02-01.4e | phase of $i(t)$ for $-j2$ | −90.0 | ° |
| 02-01.5a | $z_1 z_2^{\ast}$ | −14 − j5 | — |
| 02-01.5b | $z_1 / z_2$ | −0.8235 − j0.2941 | — |
| 02-01.5c | $\lvert z_1 + z_2\rvert$ | 1.414 | — |
| 02-01.5d | $z_1^2$ | −5 − j12 | — |
| 02-01.5e | $\operatorname{Re}\lbrace z_1 z_2\rbrace$ | 10 | — |
| 02-01.5f | $z_1/z_2$ polar | 0.8745∠−160.35° | — |
| 02-01.8a | root $k = 0$ | 1.732 − j1.000 | — |
| 02-01.8b | root $k = 1$ | j2.000 | — |
| 02-01.8c | root $k = 2$ | −1.732 − j1.000 | — |
| 02-01.9a | $\mathbf{V}$ rectangular | 0.5858 + j5.050 | V |
| 02-01.9b | $\mathbf{V}$ polar | 5.084∠83.38° | V |
| 02-01.10a | phase of 1.5 ns at 100 MHz | 54.0 | ° |
| 02-01.10b | trace delay | 333.3 | ps |
| 02-01.10c | trace phase at 2.4 GHz | 288.0 | ° |
| 02-01.10d | wavelength on trace | 62.50 | mm |
| 02-01.11 | $\mathbf{Y}$ | 0.8839∠−15.00° | — |
| 02-01.12a | $Z$ | 50.00 + j62.83 | Ω |
| 02-01.12b | $Z$ polar | 80.30∠51.49° | Ω |
| 02-01.12c | $\mathbf{I}$ | 0.2491∠−51.49° | A |
| 02-01.12d | resistor voltage amplitude | 12.45 | V |
| 02-01.12e | inductor voltage amplitude | 15.65 | V |
| 02-01.13a | $\omega_0$ | 316228 | rad/s |
| 02-01.13b | $f_0$ | 50.33 | kHz |
| 02-01.13c | $Z$ at 25 kHz | 100.0 − j479.5 | Ω |
| 02-01.13d | $Z$ at 25 kHz polar | 489.9∠−78.22° | Ω |
| 02-01.13e | $Z$ at 100 kHz | 100.0 + j469.2 | Ω |
| 02-01.13f | $Z$ at 100 kHz polar | 479.7∠77.97° | Ω |
| 02-01.14a | $H$ at 500 rad/s | 1.322∠−7.59° | — |
| 02-01.14b | $H$ at 1000 rad/s | 5.000∠−90.00° | — |
| 02-01.14c | $H$ at 2000 rad/s | 0.3304∠−172.41° | — |
| 02-01.14d | $\omega_{pk}$ | 989.9 | rad/s |
| 02-01.14e | $\lvert H\rvert_{max}$ | 5.025 | — |
| 02-01.15a | complex multiplications, N = 4096 | 24576 | — |
| 02-01.15b | real multiplications, 4-mult form | 98304 | — |
| 02-01.15c | real multiplications, 3-mult form | 73728 | — |
| 02-01.16a | beat (loudness) frequency | 4 | Hz |
| 02-01.16b | beat period | 0.25 | s |
| 02-01.16c | fast-oscillation frequency | 442 | Hz |
| 02-01.17a | average power $P$ | 7.071 | W |
| 02-01.17b | incorrect $\tfrac{1}{2}\operatorname{Re}\lbrace\mathbf{V}\mathbf{I}\rbrace$ | 9.659 | W |
