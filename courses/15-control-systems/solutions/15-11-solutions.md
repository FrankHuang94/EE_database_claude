# Solutions 15-11 · Digital Control

Problems: [15-11 problems](../problems/15-11-problems.md) · Chapter: [15-11](../chapters/15-11-digital-control.md)

Every number below is recomputed by [verify_15_11.py](../verify/verify_15_11.py): discretizations by scipy and by the matrix exponential, stability by roots and by the Jury conditions, and frequency responses on the unit circle.

---

## Solutions

### Solution 15-11.1

$z = e^{sT}$ with $T$ = 0.05 s:

- $s = -1$: $z = e^{-0.05}$ = **0.951**.
- $s = -10$: $z = e^{-0.5}$ = **0.607**.
- $s = -1 \pm j10$: magnitude $e^{-0.05}$ = 0.951, angle $\pm 10 \times 0.05$ rad = ±**28.6**°.

Poles with the same real part map to the same circle; the imaginary part sets the angle.

### Solution 15-11.2

$\omega_cT/2 = 2\pi \times 1000/(2 \times 20{,}000)$ = 0.157 rad = **9.0**°.

### Solution 15-11.3

$G(z) = (1 - e^{-0.5})/(z - e^{-0.5})$ = **0.393**/(z − **0.607**). At $z$ = 1 it equals 0.393/0.393 = **1**, the plant's DC gain.

### Solution 15-11.4

Without prewarping: $C(z) = (2.604z - 1.663)/(z - 0.0592)$, and its phase peaks at **4.17** rad/s, 6% below the design frequency (the peak value, 37.0°, is preserved; Tustin warps frequency, not phase). With prewarping at $\omega_m$ = 4.4248 rad/s: $C(z) = (\mathbf{2.553}z - \mathbf{1.578})/(z - \mathbf{0.0251})$, with its peak exactly at **4.42** rad/s. At this coarse rate ($\omega T$ = 0.88 rad) the difference matters for a lead, whose job is to deliver its phase exactly at crossover.

### Solution 15-11.5

**(a)** $\lvert a_0\rvert = 0.5 < 1$, $1 - 1.2 + 0.5 = 0.3 > 0$, $1 + 1.2 + 0.5 > 0$: **stable**, with roots $0.6 \pm j0.374$ (magnitude **0.707**).

**(b)** $1 - a_1 + a_0 = 1 - 0.5 - 0.6 = -0.1 < 0$: **unstable**; the roots are **−1.064** (outside the circle) and **0.564**.

### Solution 15-11.6

- Forward Euler: $z = 1 + sT$ = **−1.5**, outside the unit circle: the discrete controller is unstable.
- Backward Euler: $z = 1/(1 - sT)$ = **0.286**, stable.
- Tustin: $z = (1 + sT/2)/(1 - sT/2)$ = **−0.111**, stable (but on the negative real axis: it alternates sign each sample).
- Exact: $e^{-2.5}$ = **0.0821**.

Forward Euler is unstable whenever $\lvert sT\rvert > 2$ for a real pole; here the sample period is too long for the 10 ms time constant.

### Solution 15-11.7

$K_{max} = (1 - e^{-T})/(1 - e^{-T} - Te^{-T})$ (Example 15-11.5) = 0.3935/0.0902 = **4.36** at $T$ = 0.5 s, between the values for 0.1 s (20.3) and 1 s (2.39).

### Solution 15-11.8

The hold costs about $\omega_cT/2 = 5.24 \times 0.05$ rad = **15.0**°, leaving about **45**° of margin. Equivalently, the effective delay rises from 0.1 s to 0.15 s; redesigning for 60° would lower $\omega_c$ to $(\pi/6)/0.15$ = 3.49 rad/s.

### Solution 15-11.9

12 bits: 150/4096 = **0.0366** K per step. 16 bits: 150/65,536 = **0.00229** K. A thermal controller rarely needs better than 0.1 K, so 12 bits suffice for control; the extra bits help filtering and calibration.

### Solution 15-11.10

Tustin maps a continuous frequency $\omega_a$ to the discrete frequency $\omega_d = (2/T)\arctan(\omega_aT/2)$, so $f_d = (f_s/\pi)\arctan(\pi f_a/f_s)$ = (4000/π) arctan(π/4) = **848** Hz: the notch lands 15% low and misses the 1 kHz tone it was meant to remove. Prewarping at 1 kHz places it at **1000** Hz exactly.

### Solution 15-11.11

Backward Euler: $d_k = \dfrac{T_f}{T_f + T}d_{k-1} + \dfrac{K_d}{T_f + T}(e_k - e_{k-1})$ with $T_f + T$ = 25 ms, so the pole is $5/25$ = **0.2** and the gain $0.1/0.025$ = **4**. For a unit step at $k = 0$: $d_0 = 4$, then $d_1 = 0.2 \times 4 + 4 \times 0$ = **0.8**, decaying by a factor of 5 each sample.

Tustin: $s \leftarrow (2/T)(z - 1)/(z + 1) = 100(z - 1)/(z + 1)$, so

$$
D(z) = \frac{0.1 \times 100(z - 1)}{(z + 1) + 0.005 \times 100(z - 1)} = \frac{10(z - 1)}{1.5z + 0.5} = 6.667\,\frac{z - 1}{z + 0.3333} .
$$

The pole is **−0.333** (that is $(2T_f - T)/(2T_f + T)$) and the gain **6.667**: $d_k = -0.3333\,d_{k-1} + 6.667(e_k - e_{k-1})$. The step gives $d_0 = 6.667$ and $d_1$ = **−2.222**: the derivative output alternates in sign, a high-frequency ripple on the actuator. With $T > 2T_f$ the filter is too fast for the sample rate to represent, and backward Euler's monotonic response is the safer choice.

### Solution 15-11.12

$L(z) = G(z)$ has one pole at $z = 1$: **type 1**. $K_v = \lim_{z \to 1}(z - 1)G(z)/T = (n_1 + n_0)/[T(1 - e^{-T})]$, and $n_1 + n_0 = (T - 1 + e^{-T}) + (1 - e^{-T} - Te^{-T}) = T(1 - e^{-T})$, so $K_v$ = **1** s⁻¹ and the sampled ramp error is $1/K_v$ = **1**, exactly as for the continuous loop $1/[s(s + 1)]$. Sampling slows and destabilizes this loop (Example 15-11.5), but it does not change its steady-state accuracy.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 15-11.1a | z for s = −1 | 0.951 | — |
| 15-11.1b | z for s = −10 | 0.607 | — |
| 15-11.1c | angle for s = −1 ± j10 | 28.6 | ° |
| 15-11.2a | phase lost | 9.0 | ° |
| 15-11.3a | gain | 0.393 | — |
| 15-11.3b | pole | 0.607 | — |
| 15-11.3c | DC gain | 1 | — |
| 15-11.4a | peak frequency without prewarping | 4.17 | rad/s |
| 15-11.4b | peak frequency with prewarping | 4.42 | rad/s |
| 15-11.4c | b0 without prewarping | 2.604 | — |
| 15-11.4d | b1 without prewarping | −1.663 | — |
| 15-11.4e | pole without prewarping | 0.0592 | — |
| 15-11.4f | b0 with prewarping | 2.553 | — |
| 15-11.4g | b1 with prewarping | −1.578 | — |
| 15-11.4h | pole with prewarping | 0.0251 | — |
| 15-11.5a | root of (b) outside the circle | −1.064 | — |
| 15-11.5b | root magnitude of (a) | 0.707 | — |
| 15-11.5c | root of (b) inside | 0.564 | — |
| 15-11.6a | forward Euler | −1.5 | — |
| 15-11.6b | backward Euler | 0.286 | — |
| 15-11.6c | Tustin | −0.111 | — |
| 15-11.6d | exact | 0.0821 | — |
| 15-11.7a | largest stable K | 4.36 | 1/s² |
| 15-11.8a | extra phase lost | 15.0 | ° |
| 15-11.8b | remaining margin | 45 | ° |
| 15-11.8c | crossover for 60° with 0.15 s | 3.49 | rad/s |
| 15-11.9a | 12-bit step | 0.0366 | K |
| 15-11.9b | 16-bit step | 0.00229 | K |
| 15-11.10a | notch without prewarping | 848 | Hz |
| 15-11.10b | notch with prewarping | 1000 | Hz |
| 15-11.11a | backward-Euler pole | 0.2 | — |
| 15-11.11b | backward-Euler gain | 4 | — |
| 15-11.11c | backward-Euler second output | 0.8 | — |
| 15-11.11d | Tustin pole | −0.333 | — |
| 15-11.11e | Tustin gain | 6.667 | — |
| 15-11.11f | Tustin second output | −2.222 | — |
| 15-11.12a | system type | 1 | — |
| 15-11.12b | velocity constant | 1 | 1/s |
| 15-11.12c | ramp error | 1 | — |
