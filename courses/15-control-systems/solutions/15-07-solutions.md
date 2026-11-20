# Solutions 15-07 · Frequency-Domain Design: Bode, Nyquist and Margins

Problems: [15-07 problems](../problems/15-07-problems.md) · Chapter: [15-07](../chapters/15-07-frequency-domain-design.md)

Every number below is recomputed by [verify_15_07.py](../verify/verify_15_07.py): margins by root finding with `labs/15-07-lab/freqdomain.py`, Nyquist encirclements by tracing the contour, integrals by quadrature, and stability cross-checked with closed-loop roots.

---

## Solutions

### Solution 15-07.1

The phase is $-90° - \arctan(\omega/2) - \arctan(\omega/10)$. It equals −180° when the two arctangents sum to 90°, that is $(\omega/2)(\omega/10) = 1$: $\omega_{180} = \sqrt{20}$ = **4.472** rad/s. There

$$
\lvert L\rvert = \frac{40}{4.472 \times \sqrt{20 + 4} \times \sqrt{20 + 100}} = \frac{40}{240} ,
$$

so GM = **6** (**15.6** dB). Numerically, $\lvert L\rvert = 1$ at $\omega_c$ = **1.559** rad/s, where PM = **43.2**°. Routh on $s^3 + 12s^2 + 20s + K$ gives $K < 240$, six times 40, as the gain margin says.

### Solution 15-07.2

PM = 180° − 125° = **55**°. Inverting the standard-loop relation gives $\zeta$ ≈ **0.541**, so the step response should overshoot by about **13.3**% (if the loop behaves like the standard one). The delay margin is $55° \times \pi/180$ rad divided by $2\pi \times 1000$ rad/s = **152.8** µs.

### Solution 15-07.3

At $\omega = z$ both have magnitude $\lvert 1 \pm j\rvert = \sqrt2$, that is **3.01** dB. The left-half-plane zero has phase **+45**°, the right-half-plane zero **−45**°. A right-half-plane zero adds lag while raising the gain, the opposite of what a stable crossover needs. Its lag reaches −90° above $z$, so crossover must stay well below $z$, typically by a factor of 3 to 10.

### Solution 15-07.4

**(a)** The phase $-3\arctan\omega$ reaches −180° at $\omega = \tan 60° = \sqrt3$ = **1.732** rad/s, where $\lvert L\rvert = K/(1 + 3)^{3/2} = K/8$. The plot crosses the negative real axis at $-K/8$.

**(b)** With $K$ = 4 the crossing is at −0.5: GM = **2** (**6.02** dB). Numerically $\omega_c$ = 1.233 rad/s and PM = **27.1**°.

**(c)** The loop is stable while the crossing stays to the right of −1, that is $K < 8$: the same limit Routh gave in Example 15-05.3, with the same boundary frequency $\sqrt3$.

### Solution 15-07.5

$\lvert L\rvert = K/\omega$, so $\omega_c = K$, and the phase is $-90° - \omega T$. A 60° margin needs $\omega_cT$ = 30° = $\pi/6$ rad, so $K = \pi/(6T)$ = **261.8** s⁻¹. The phase crossover is at $\omega T = \pi/2$, so $\omega_{180}$ = 785.4 rad/s and GM = $\omega_{180}/\omega_c$ = **3** (**9.54** dB).

### Solution 15-07.6

A 60° margin corresponds to $\zeta$ = **0.612**. With $2\zeta\omega_n = 5$, $\omega_n$ = 4.082 rad/s and $K = \omega_n^2$ = **16.7**. Check: $\omega_c$ = **2.887** rad/s, where the phase is $-90° - \arctan(2.887/5) = -120.0°$, so PM = 60.0°.

### Solution 15-07.7

- Buffer ($\beta$ = 1): $f_c$ = **0.786** MHz and PM = **51.8**°. The second pole equals the GBW, which gives exactly $\zeta$ = 0.5 (Example 15-07.6's guided exercise).
- Gain of 10 ($\beta$ = 0.1): the loop gain is ten times smaller, so crossover falls to **99.5** kHz, where the second pole adds only about 5.7° of lag: PM = **84.3**°.

Higher closed-loop gain means lower loop gain and more margin; unity gain is the hardest case.

### Solution 15-07.8

The load pole is at $1/(2\pi \times 50 \times 10^{-9})$ = **3.18** MHz, below the 9.10 MHz crossover. Recomputing with the third pole: $f_c$ = **5.12** MHz, PM = **17.5**°, and now the phase reaches −180° at a finite frequency, giving GM = **2.32** (**7.30** dB). The buffer, which had 65.5° of margin unloaded, rings badly with 1 nF. This is why data sheets plot phase margin against load capacitance, and why isolation resistors are used.

### Solution 15-07.9

At the phase crossover, $L = -1/\text{GM}$, so the distance to −1 is $1 - 1/\text{GM}$. It must be at least $1/M_s$: $\text{GM} \ge M_s/(M_s - 1)$ = **3** (**9.54** dB). At the gain crossover, $L$ lies on the unit circle at angle $-180° + \text{PM}$, at distance $2\sin(\text{PM}/2)$ from −1, which must be at least $1/M_s$: $\text{PM} \ge 2\arcsin[1/(2M_s)]$ = **38.9**°.

### Solution 15-07.10

**(a)** $S(0) = 1/(1 + 2)$ = **0.333**: disturbances at DC are cut to a third.

**(b)** $\lvert S\rvert = 1$ where $\lvert 1 + L\rvert = 1$. Numerically, $\lvert S\rvert > 1$ above $\omega$ = **2** rad/s: there the loop amplifies disturbances.

**(c)** $M_s$ = **1.21** at **3.21** rad/s.

**(d)** The integral is **0** (to numerical precision). $L$ has relative degree 2 and no right-half-plane poles, so Bode's integral requires the negative area below 2 rad/s (where $\ln\lvert S\rvert < 0$) to be exactly balanced by the positive area above it. Rejection at low frequency is paid for by amplification near crossover.

### Solution 15-07.11

**(a)** Numerically, $\omega_c$ = **4.81 × 10⁵** rad/s and PM = **55.1**°.

**(b)** The phase $-180° + \arctan(\omega\tau_z) - \arctan(\omega\tau_p)$ peaks at $\omega = 1/\sqrt{\tau_z\tau_p}$ = **6.63 × 10⁵** rad/s, with margin $\arctan[(b - 1)/(2\sqrt b)]$ = **56.4**° for $b$ = 11.

**(c)** Crossover there needs $K = \omega^{*2}\,\lvert 1 + j\omega^*\tau_p\rvert/\lvert 1 + j\omega^*\tau_z\rvert$ = **1.327 × 10¹¹** s⁻², **1.46** times the design gain. The design gives up 1.3° of margin to keep a lower bandwidth (less reference noise passes); the margin peak is flat, so this costs little.

### Solution 15-07.12

**(a)** The characteristic polynomial is $s^2 - 100 + K(s + 5) = s^2 + Ks + (5K - 100)$. Degree 2: stable for $K >$ **20**.

**(b)** $P$ = 1 (the plant pole at +10). Tracing the Nyquist contour at $K$ = 40 gives one counterclockwise encirclement, $N = -1$, so $Z = N + P$ = **0**: stable. The closed-loop poles are −37.3 and −2.68.

**(c)** Numerically $\omega_c$ = 37.7 rad/s and PM = **82.4**°.

**(d)** At $K$ = 15 the encirclement disappears, $N$ = 0, and $Z$ = **1**: one unstable closed-loop pole, matching Routh (the polynomial $s^2 + 15s - 25$ has a positive root).

### Solution 15-07.13

The original delay margin is $51.8° \times \pi/180/7.86$ = **0.115** s. Adding 50 ms subtracts $7.86 \times 0.05$ rad = 22.5° at crossover: the new PM is **29.3**°. The added phase lag creates a phase crossover at 13.1 rad/s, where the gain margin is **2.15** (**6.65** dB). A delay equal to 43% of the delay margin removes 43% of the phase margin, since the lost phase is $\omega_cT$.

### Solution 15-07.14

A 3 dB gain margin means the gain can rise by a factor of $10^{3/20}$ = **1.41** before oscillation. That is fragile: a 41% gain change from process, temperature or load is common. The 45° phase margin alone looks acceptable, which is why both margins (and ideally $M_s$) must be checked. Next ask: what varies the gain (and by how much across corners), and what is the closest approach of the Nyquist plot to −1.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 15-07.1a | phase crossover | 4.472 | rad/s |
| 15-07.1b | gain margin | 6 | — |
| 15-07.1c | gain margin | 15.6 | dB |
| 15-07.1d | gain crossover | 1.559 | rad/s |
| 15-07.1e | phase margin | 43.2 | ° |
| 15-07.2a | phase margin | 55 | ° |
| 15-07.2b | ζ | 0.541 | — |
| 15-07.2c | overshoot | 13.3 | % |
| 15-07.2d | delay margin | 152.8 | µs |
| 15-07.3a | magnitude at ω = z | 3.01 | dB |
| 15-07.3b | phase, LHP zero | 45 | ° |
| 15-07.3c | phase, RHP zero | −45 | ° |
| 15-07.4a | phase crossover | 1.732 | rad/s |
| 15-07.4b | gain margin | 2 | — |
| 15-07.4c | gain margin | 6.02 | dB |
| 15-07.4d | phase margin | 27.1 | ° |
| 15-07.5a | K | 261.8 | 1/s |
| 15-07.5b | gain margin | 3 | — |
| 15-07.5c | gain margin | 9.54 | dB |
| 15-07.6a | ζ | 0.612 | — |
| 15-07.6b | K | 16.7 | 1/s² |
| 15-07.6c | crossover | 2.887 | rad/s |
| 15-07.7a | crossover, buffer | 0.786 | MHz |
| 15-07.7b | phase margin, buffer | 51.8 | ° |
| 15-07.7c | crossover, gain 10 | 99.5 | kHz |
| 15-07.7d | phase margin, gain 10 | 84.3 | ° |
| 15-07.8a | load pole | 3.18 | MHz |
| 15-07.8b | crossover | 5.12 | MHz |
| 15-07.8c | phase margin | 17.5 | ° |
| 15-07.8d | gain margin | 2.32 | — |
| 15-07.8e | gain margin | 7.30 | dB |
| 15-07.9a | minimum gain margin | 3 | — |
| 15-07.9b | minimum gain margin | 9.54 | dB |
| 15-07.9c | minimum phase margin | 38.9 | ° |
| 15-07.10a | abs S at DC | 0.333 | — |
| 15-07.10b | frequency where abs S = 1 | 2 | rad/s |
| 15-07.10c | sensitivity peak | 1.21 | — |
| 15-07.10d | frequency of the peak | 3.21 | rad/s |
| 15-07.10e | Bode integral | 0 | rad/s |
| 15-07.11a | crossover | 4.81e5 | rad/s |
| 15-07.11b | phase margin | 55.1 | ° |
| 15-07.11c | frequency of maximum margin | 6.63e5 | rad/s |
| 15-07.11d | maximum margin | 56.4 | ° |
| 15-07.11e | K for crossover there | 1.327e11 | 1/s² |
| 15-07.11f | ratio to the design gain | 1.46 | — |
| 15-07.12a | smallest stable K | 20 | — |
| 15-07.12b | unstable poles at K = 40 | 0 | — |
| 15-07.12c | phase margin at K = 40 | 82.4 | ° |
| 15-07.12d | unstable poles at K = 15 | 1 | — |
| 15-07.13a | original delay margin | 0.115 | s |
| 15-07.13b | new phase margin | 29.3 | ° |
| 15-07.13c | new gain margin | 2.15 | — |
| 15-07.13d | new gain margin | 6.65 | dB |
| 15-07.14a | gain factor | 1.41 | — |
