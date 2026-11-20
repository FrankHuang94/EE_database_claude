# Solutions 15-05 · Stability and the Routh–Hurwitz Criterion

Problems: [15-05 problems](../problems/15-05-problems.md) · Chapter: [15-05](../chapters/15-05-stability-routh-hurwitz.md)

Every number below is recomputed by [verify_15_05.py](../verify/verify_15_05.py): Routh arrays by `labs/15-05-lab/routh.py`, symbolic gain limits by sympy, and every conclusion checked against numerically computed roots or simulated responses.

---

## Solutions

### Solution 15-05.1

- (a) The $s^1$ coefficient is missing: **not stable** (at least one root on the axis or in the right half-plane).
- (b) A negative coefficient: **not stable**.
- (c) Degree 2 with positive coefficients: **stable** (roots −1 and −2).
- (d) All coefficients positive, but the cubic test fails: $a_2a_1 = 1 < a_3a_0 = 2$, so it is **unstable**, with two right-half-plane roots.

### Solution 15-05.2

**(a)**

$$
\begin{array}{c|cc}
s^3 & 1 & 5 \\ s^2 & 4 & 2 \\ s^1 & (20 - 2)/4 = 4.5 & \\ s^0 & 2 &
\end{array}
$$

No sign changes: **0** right-half-plane roots (they are −2, −1, −1).

**(b)**

$$
\begin{array}{c|cc}
s^3 & 1 & 2 \\ s^2 & 1 & 8 \\ s^1 & (2 - 8)/1 = -6 & \\ s^0 & 8 &
\end{array}
$$

Two sign changes: **2** right-half-plane roots (they are $0.5 \pm j1.94$; the third is −2).

### Solution 15-05.3

- (a) Pole at −1: **BIBO stable**.
- (b) Pole at 0: an integrator; a step input produces a ramp. **Not BIBO stable.**
- (c) Poles at $\pm j2$: marginally stable, **not BIBO stable** (a bounded input at 2 rad/s resonates, Problem 15-05.14).
- (d) Poles at −2 and −3: **BIBO stable**. The right-half-plane zero affects the response shape (15-03), not stability.
- (e) Pole at +1: **unstable**.

### Solution 15-05.4

The characteristic polynomial is $s(s - 1)(s + 6) + K(s + 1) = s^3 + 5s^2 + (K - 6)s + K$:

$$
\begin{array}{c|cc}
s^3 & 1 & K - 6 \\ s^2 & 5 & K \\ s^1 & \dfrac{5(K - 6) - K}{5} = \dfrac{4K - 30}{5} & \\ s^0 & K &
\end{array}
$$

Stability needs $4K - 30 > 0$ and $K > 0$: $K >$ **7.5**. Feedback stabilizes the unstable plant, but only above a minimum gain. At $K$ = 7.5 the auxiliary polynomial $5s^2 + 7.5$ gives $\omega = \sqrt{1.5}$ = **1.225** rad/s.

### Solution 15-05.5

The first two rows are 1, 6, 8 and 1, 6, 8, so the $s^3$ row is all zeros. The auxiliary polynomial from the $s^4$ row is $A(s) = s^4 + 6s^2 + 8$, with $dA/ds = 4s^3 + 12s$:

$$
\begin{array}{c|ccc}
s^5 & 1 & 6 & 8 \\ s^4 & 1 & 6 & 8 \\ s^3 & 4 & 12 & \\ s^2 & (24 - 12)/4 = 3 & 8 & \\ s^1 & (36 - 32)/3 = 4/3 & & \\ s^0 & 8 & &
\end{array}
$$

No sign changes, so **0** roots in the right half-plane. $A(s) = (s^2 + 2)(s^2 + 4)$ gives **4** roots on the imaginary axis, at $\pm j\sqrt2$ = ±j**1.414** and ±j**2** rad/s. Dividing out $A(s)$ leaves $s + 1$, so the fifth root is −1. With simple poles on the axis, the system is marginally stable and **not BIBO stable**.

### Solution 15-05.6

$$
\begin{array}{c|ccc}
s^4 & 1 & 4 & 5 \\ s^3 & 2 & 8 & \\ s^2 & (8 - 8)/2 = 0 \to \varepsilon & 5 & \\ s^1 & (8\varepsilon - 10)/\varepsilon \approx -10/\varepsilon & & \\ s^0 & 5 & &
\end{array}
$$

The first column is $+, +, +, -, +$: **2** right-half-plane roots. (They are $0.201 \pm j1.877$; the others are −1 and −1.403.)

### Solution 15-05.7

**(a)** Five inversions give a net inversion, which is 180° of phase; the five poles must supply the other 180°, so 36° each at the oscillation frequency.

**(b)** A single pole lags by $\arctan(\omega/\omega_0)$, so $\omega = \omega_0\tan 36°$ = **0.727** $\omega_0$. At that frequency each stage's magnitude is $A\cos 36°$, and the loop gain is 1 when $A = 1/\cos 36°$ = **1.236**.

**(c)** With $x = s/\omega_0$, the characteristic polynomial is $(1 + x)^5 + A^5$. At $A$ = 1.236 its roots include $\pm j0.727$ exactly, and for larger $A$ that pair moves into the right half-plane.

**(d)** $0.727 \times 1$ GHz = **727** MHz. More stages allow less gain per stage but oscillate more slowly relative to each stage's bandwidth.

### Solution 15-05.8

**(a)** Substitute $s = z - 1$: $(z - 1)^3 + 6(z - 1)^2 + 8(z - 1) + K = z^3 + 3z^2 - z + (K - 3)$. The $z$ coefficient is **−1** for every $K$, so the necessary condition fails: no gain puts all poles left of −1.

**(b)** The poles at 0 and −2 move toward each other as $K$ rises, meet at the root of $d[s(s + 2)(s + 4)]/ds = 3s^2 + 12s + 8 = 0$ nearest the origin, $s$ = **−0.845**, and then leave the real axis moving right (15-06). The best guaranteed decay rate is therefore $\sigma$ = 0.845 s⁻¹, at $K = 0.845 \times 1.155 \times 3.155$ = **3.08**. Proportional gain alone cannot make this loop settle faster than about $4/0.845$ = 4.7 s.

### Solution 15-05.9

**(a)** The loop gain is $L_0/[(1 + s/a)(1 + s/b)(1 + s/c)]$ with $a$ = 6.283 × 10⁴, $b$ = 10⁵ and $c$ = 6.283 × 10⁶ rad/s. Multiplying out, the characteristic polynomial is $\dfrac{s^3}{abc} + \dfrac{a + b + c}{abc}s^2 + \dfrac{ab + bc + ca}{abc}s + 1 + L_0$, and the cubic test gives

$$
1 + L_0 < \frac{(a + b + c)(ab + bc + ca)}{abc} \;\Rightarrow\; L_0 < \mathbf{167} .
$$

**(b)** At the boundary the auxiliary polynomial gives $\omega^2 = ab + bc + ca$, so $\omega$ = 1.015 × 10⁶ rad/s, or **161.5** kHz.

**(c)** $L_0$ = 2500 is fifteen times the limit: the regulator oscillates. Its closed-loop poles are at $+7.26 \times 10^5 \pm j3.46 \times 10^6$ s⁻¹, growing with a time constant of 1.4 µs. The two-pole model of 15-02 already showed $\zeta$ = 0.02; the third pole tips it over. Real LDOs use a dominant pole far below the others, or a zero from the output capacitor's ESR (15-12).

### Solution 15-05.10

**(a)** The characteristic polynomial is $\tau_p\tau_3s^4 + (\tau_p + \tau_3)s^3 + s^2 + K\tau_zs + K$. Building the array symbolically: the $s^2$ row's first entry is $b_1 = 1 - K/(6.4 \times 10^{11})$, and the $s^1$ entry is positive only for $K < 4.992 \times 10^{12}/11$. So the loop is stable for $0 < K <$ **4.54 × 10¹¹** s⁻². (The $s^1$ condition is the tighter one, so $b_1$ stays positive.)

**(b)** $4.54 \times 10^{11}/9.09 \times 10^{10}$ = **4.99**, a gain margin of **14.0** dB.

**(c)** At the boundary the auxiliary polynomial $b_1s^2 + K$ gives $\omega = \sqrt{K/b_1}$ = 1.249 × 10⁶ rad/s, or **198.8** kHz.

### Solution 15-05.11

**(a)** With $P = -K_cT_s$ and $T_s = T/(\tau_ss + 1)$, the loop gives $(RCs + 1 - G)(\tau_ss + 1) + RK_c = 0$:

$$
RC\tau_s\,s^2 + [RC + \tau_s(1 - G)]\,s + (1 - G + RK_c) = 0 .
$$

**(b)** Degree 2, so stability needs positive coefficients. The constant term needs $K_c > (G - 1)/R$ = 0.2/0.8 = **0.25** W/K. The $s$ coefficient needs $RC > \tau_s(G - 1)$, that is $16 > 0.02$, which holds easily (it would fail only for a sensor lag above 80 s).

**(c)** Feedback can stabilize a physically unstable plant (runaway) if it acts strongly enough and fast enough. The required gain is the excess loop gain $G - 1$ divided by $R$: throttling must remove more power per kelvin than the leakage adds.

### Solution 15-05.12

The cubic test with positive coefficients: $a > 0$, $K > 0$ and $4a > K$. The region is the wedge $0 < K < 4a$. On the boundary $K = 4a$, the auxiliary polynomial $as^2 + K = a(s^2 + 4)$ gives $\omega$ = **2** rad/s for every $a$: the boundary frequency is $\sqrt{a_1/a_3}$, fixed by the coefficients that do not change.

### Solution 15-05.13

**(a)** With the Padé form, $s(1 + s/2) + K(1 - s/2) = 0$, that is $0.5s^2 + (1 - K/2)s + K = 0$. Degree 2: stable for $0 < K <$ **2**.

**(b)** The exact limit is $\pi/2$ = **1.571**. The approximation overestimates it by **27.3**%: a first-order Padé form is accurate only well below $\omega = 2/T$, and the crossover here is near $\omega = K$.

### Solution 15-05.14

With $U = 2/(s^2 + 4)$, $Y = 2/(s^2 + 4)^2$. Using the transform pair $\mathcal{L}\{\sin\omega t - \omega t\cos\omega t\} = 2\omega^3/(s^2 + \omega^2)^2$ with $\omega = 2$: $2/(s^2 + 4)^2 = (1/8)\,\mathcal{L}\{\sin 2t - 2t\cos 2t\}$. So $y(t) = (\sin 2t - 2t\cos 2t)/8$. At $t$ = 10 s, $y$ = **−0.906**; the envelope of the growing term is $2t/8 = t/4$ = **2.5**. The output grows without bound from a bounded input.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 15-05.1a | right-half-plane roots (d) | 2 | — |
| 15-05.2a | third first-column entry (a) | 4.5 | — |
| 15-05.2b | right-half-plane roots (a) | 0 | — |
| 15-05.2c | third first-column entry (b) | −6 | — |
| 15-05.2d | right-half-plane roots (b) | 2 | — |
| 15-05.4a | smallest stable K | 7.5 | — |
| 15-05.4b | boundary frequency | 1.225 | rad/s |
| 15-05.5a | right-half-plane roots | 0 | — |
| 15-05.5b | imaginary-axis roots | 4 | — |
| 15-05.5c | lower axis frequency | 1.414 | rad/s |
| 15-05.5d | upper axis frequency | 2 | rad/s |
| 15-05.6a | right-half-plane roots | 2 | — |
| 15-05.7a | ω/ω0 | 0.727 | — |
| 15-05.7b | minimum stage gain | 1.236 | — |
| 15-05.7c | oscillation frequency | 727 | MHz |
| 15-05.8a | z coefficient after the shift | −1 | 1/s |
| 15-05.8b | best decay rate (breakaway) | −0.845 | 1/s |
| 15-05.8c | K at the breakaway | 3.08 | 1/s³ |
| 15-05.9a | largest stable L0 | 167 | — |
| 15-05.9b | boundary frequency | 161.5 | kHz |
| 15-05.10a | largest stable K | 4.54e11 | 1/s² |
| 15-05.10b | gain factor to the boundary | 4.99 | — |
| 15-05.10c | gain margin | 14.0 | dB |
| 15-05.10d | boundary frequency | 198.8 | kHz |
| 15-05.11a | smallest stabilizing Kc | 0.25 | W/K |
| 15-05.12a | boundary frequency | 2 | rad/s |
| 15-05.13a | Padé limit | 2 | — |
| 15-05.13b | exact limit | 1.571 | — |
| 15-05.13c | overestimate | 27.3 | % |
| 15-05.14a | y at 10 s | −0.906 | — |
| 15-05.14b | envelope at 10 s | 2.5 | — |
