# Solutions 15-06 · Root Locus

Problems: [15-06 problems](../problems/15-06-problems.md) · Chapter: [15-06](../chapters/15-06-root-locus.md)

Every number below is recomputed by [verify_15_06.py](../verify/verify_15_06.py): rules by `labs/15-06-lab/rlocus.py`, and every conclusion checked against numerically computed closed-loop roots.

---

## Solutions

### Solution 15-06.1

Poles at 0, −1, −5, −6; zero at −3.

- **Real-axis segments.** Count real poles and zeros to the right: odd on $[-1, 0]$ (1), $[-5, -3]$ (3) and $(-\infty, -6]$ (5).
- **Asymptotes.** $n - m$ = 3: angles 60°, 180°, 300°. Centroid $[(0 - 1 - 5 - 6) - (-3)]/3$ = **−3**.

### Solution 15-06.2

**(a)** The vectors from the poles to $s = -2 + j2$ have angles 135° (from 0), 45° (from −4) and 26.57° (from −6). $\angle G = -(135 + 45 + 26.57) = -206.57° \equiv$ **153.4**°, not an odd multiple of 180°: the point is **not** on the locus.

**(b)** The characteristic polynomial is $s^3 + 10s^2 + 24s + K$; the cubic test gives $K <$ **240**, and at $K$ = 240 the auxiliary polynomial $10s^2 + 240$ gives $\omega = \sqrt{24}$ = **4.899** rad/s.

### Solution 15-06.3

$d[(s + 1)(s + 3)]/ds = 2s + 4 = 0$ gives the breakaway at **−2**, where $K = 1 \times 1$ = **1**. The two poles move toward each other along $[-3, -1]$, meet at −2 and leave vertically along $\mathrm{Re}\,s = -2$ (two asymptotes at ±90° from the centroid −2).

### Solution 15-06.4

- Real-axis segments: $[-1, 0]$ and $(-\infty, -5]$.
- Asymptotes: 60°, 180°, 300° from the centroid $(0 - 1 - 5)/3$ = **−2**.
- Breakaway: $d[s(s + 1)(s + 5)]/ds = 3s^2 + 12s + 5 = 0$, root on $[-1, 0]$: **−0.4725**, with $K = 0.4725 \times 0.5275 \times 4.5275$ = **1.128**.
- Imaginary-axis crossing: $s^3 + 6s^2 + 5s + K$; the cubic test gives $K <$ **30**, and the crossing is at $\pm j\sqrt5$ = ±j**2.236** rad/s.

### Solution 15-06.5

From $p = -1 + j1$: to the other complex pole $-1 - j1$, 90°; to the pole at −3, $\angle(2 + j1)$ = 26.57°; to the zero at −2, $\angle(1 + j1)$ = 45°. So

$$
\theta_{dep} = 180° - 90° - 26.57° + 45° = \mathbf{108.4}° .
$$

### Solution 15-06.6

On the ray $s = r(-0.6 + j0.8)$, the angle condition holds at $r$ = 1.4534, so $s_0$ = **−0.872 + j1.163**. The magnitude condition gives $K = \lvert s_0\rvert\,\lvert s_0 + 2\rvert\,\lvert s_0 + 10\rvert$ = **21.7**. By the constant-sum rule, the third pole is $-12 - 2(-0.872)$ = **−10.26**, about twelve times farther left than the dominant pair: the second-order approximation is good.

### Solution 15-06.7

$s^3 + 14s^2 + 40s + K$: the cubic test gives $K <$ **560**, with crossing at $\pm j\sqrt{40}$ = ±j**6.32** rad/s. With two poles, the asymptotes were vertical lines at −2; the third pole makes three asymptotes at ±60° and 180° from the centroid $-14/3$, and the ±60° ones head into the right half-plane.

### Solution 15-06.8

With complex poles at $-0.5 \pm j\omega$ and the constant-sum rule, the third pole is at $-6 + 1$ = **−5**. Matching $(s + 5)(s^2 + s + 0.25 + \omega^2)$ to $s^3 + 6s^2 + 8s + K$: the $s$ coefficient gives $5 + 0.25 + \omega^2 = 8$, so $\omega^2$ = 2.75, and the constant gives $K = 5(0.25 + 2.75)$ = **15**. This is the upper limit of Example 15-05.6's range for keeping every pole left of −0.5: the root locus and the shifted Routh test agree.

### Solution 15-06.9

**(a)** At $s = -6 + \rho e^{j\phi}$, $\angle G = \angle(\rho e^{j\phi}) - \angle(s) - \angle(s + 2) = \phi - \angle(-6 + \rho e^{j\phi}) - \angle(-4 + \rho e^{j\phi})$. The angle condition requires $(s + 6)/[s(s + 2)]$ to be a negative real number, so $s(s + 2)/(s + 6)$ must be too. Write $w = s + 6 = \rho e^{j\phi}$: $s(s + 2) = (w - 6)(w - 4) = w^2 - 10w + 24$, and

$$
\frac{w^2 - 10w + 24}{w} = w + \frac{24}{w} - 10 .
$$

With $\lvert w\rvert^2 = 24$, $24/w = \bar w$, so this equals $w + \bar w - 10 = 2\rho\cos\phi - 10$, which is real. It is negative because $2\rho\cos\phi \le 2\sqrt{24}$ = 9.80 < 10. So every point of the circle of radius $\sqrt{24}$ = **4.899** about −6 is on the locus.

**(b)** The ray from the origin tangent to the circle makes angle $\theta$ with $\sin\theta = 4.899/6$, so $\zeta_{min} = \cos\theta$ = **0.577**. The tangent point is at distance $6\cos\theta = \sqrt{36 - 24}$ = **3.464** from the origin: $s_0 = -2 + j2.828$. The gain there is $\lvert s_0\rvert\,\lvert s_0 + 2\rvert/\lvert s_0 + 6\rvert$ = **2**.

### Solution 15-06.10

With $K < 0$, $KG = -1$ requires $\angle G = 0°$ (mod 360°). The real-axis rule flips: a point is on the locus when the count of real poles and zeros to its right is even, giving $(-1, \infty)$ and $(-\infty, -2]$. The poles move apart: one from −1 toward $+\infty$, one from −2 toward $-\infty$. The characteristic polynomial $s^2 + 3s + 2 - \lvert K\rvert$ has a root at the origin when $\lvert K\rvert$ = **2**; beyond that the loop is unstable.

### Solution 15-06.11

Multiplying out the denominator, the characteristic polynomial is $c_3s^3 + c_2s^2 + c_1s + 1 + 10^4\beta$, with $c_3 = 10^{-17}$, $c_2 = 1.101 \times 10^{-10}$ and $c_1 = 1.0111 \times 10^{-4}$. The cubic test gives

$$
10^4\beta < \frac{c_2c_1}{c_3} - 1 \;\Rightarrow\; \beta < \mathbf{0.111} ,
$$

so the closed-loop gain $1/\beta$ must be at least **8.99**. At the boundary $\omega = \sqrt{c_1/c_3}$ = **3.18 × 10⁶** rad/s. Such an amplifier is sold as "decompensated": it trades unity-gain stability for more bandwidth, and is specified as stable only above a minimum gain: the OPA637's datasheet states "stable in gain ≥ 5" (TI SBOS165C, as of Nov 2026) **[Established]** [R-230]. A datasheet's minimum gain is chosen to leave adequate phase margin, whereas the 8.99 found here is the bare boundary of oscillation for this illustrative model, so the two numbers are not directly comparable.

### Solution 15-06.12

$\tau_ps^3 + s^2 + K + \tau_z(Ks)$: $D(s) = \tau_ps^3 + s^2 + K$ and $N(s) = Ks$. The cubic test on the full polynomial needs $1 \cdot K\tau_z > \tau_pK$, so the loop becomes unstable as $\tau_z$ falls to $\tau_p$ = **0.455** µs. There the polynomial factors as $(\tau_ps + 1)(s^2 + K)$, with crossing at $\omega = \sqrt K$ = **3.015 × 10⁵** rad/s.

### Solution 15-06.13

At a complex zero $z_k$, the arrival angle is $\theta_{arr} = 180° + \sum_j\angle(z_k - p_j) - \sum_{i \ne k}\angle(z_k - z_i)$. From $z_k = -1 + j2$: to the pole at 0, $\angle(-1 + j2)$ = 116.57°; to the pole at −4, $\angle(3 + j2)$ = 33.69°; to the other zero, 90°. So $\theta_{arr} = 180 + 116.57 + 33.69 - 90 = 240.26°$, that is **−119.7**°: the branch arrives from below and to the left of the zero (an angle of 240° points down and left), travelling up and to the right as $K$ grows.

### Solution 15-06.14

The locus is the vertical line $\mathrm{Re}\,s = -2$ above $K$ = 1. For $\zeta$ = 0.5 the ray at 60° meets it at $s_0 = -2 + j3.464$, so $K = \lvert s_0 + 1\rvert\,\lvert s_0 + 3\rvert = 3.606 \times 3.606$ = **13**. Then $K_p = K/3$ = 4.333 and the step error is $1/(1 + 4.333)$ = **0.1875**. Damping and accuracy compete again (15-04); a lag compensator raises $K_p$ without moving these poles (15-09).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 15-06.1a | centroid | −3 | 1/s |
| 15-06.2a | angle of G at the test point | 153.4 | ° |
| 15-06.2b | largest stable K | 240 | 1/s³ |
| 15-06.2c | crossing frequency | 4.899 | rad/s |
| 15-06.3a | breakaway point | −2 | 1/s |
| 15-06.3b | K at the breakaway | 1 | 1/s² |
| 15-06.4a | centroid | −2 | 1/s |
| 15-06.4b | breakaway point | −0.4725 | 1/s |
| 15-06.4c | K at the breakaway | 1.128 | 1/s³ |
| 15-06.4d | largest stable K | 30 | 1/s³ |
| 15-06.4e | crossing frequency | 2.236 | rad/s |
| 15-06.5a | departure angle | 108.4 | ° |
| 15-06.6a | pole for ζ = 0.6 | −0.872 + j1.163 | 1/s |
| 15-06.6b | K | 21.7 | 1/s³ |
| 15-06.6c | third pole | −10.26 | 1/s |
| 15-06.7a | largest stable K | 560 | 1/s³ |
| 15-06.7b | crossing frequency | 6.32 | rad/s |
| 15-06.8a | third pole | −5 | 1/s |
| 15-06.8b | K | 15 | 1/s³ |
| 15-06.9a | circle radius | 4.899 | 1/s |
| 15-06.9b | smallest ζ | 0.577 | — |
| 15-06.9d | distance of the tangent point from the origin | 3.464 | 1/s |
| 15-06.9c | K at the tangent point | 2 | 1/s |
| 15-06.10a | instability threshold abs K | 2 | 1/s² |
| 15-06.11a | largest β | 0.111 | — |
| 15-06.11b | smallest closed-loop gain | 8.99 | — |
| 15-06.11c | crossing frequency | 3.18e6 | rad/s |
| 15-06.12a | critical τz | 0.455 | µs |
| 15-06.12b | crossing frequency | 3.015e5 | rad/s |
| 15-06.13a | arrival angle | −119.7 | ° |
| 15-06.14a | K | 13 | 1/s² |
| 15-06.14b | step error | 0.1875 | — |
