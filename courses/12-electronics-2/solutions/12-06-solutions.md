# Solutions 12-06 · Stability and Frequency Compensation

Problems: [12-06 problems](../problems/12-06-problems.md) · Chapter: [12-06](../chapters/12-06-stability-and-compensation.md). Every number below is recomputed by [verify_12_06.py](../verify/verify_12_06.py), which finds crossovers and margins by root finding on the loop gain and solves the two-stage amplifier by complex nodal analysis rather than reusing these formulas.

---

## Solutions

### Solution 12-06.1

PM $= 180^\circ - 125^\circ$ = **55**°. GM $= -20\log_{10}0.2$ = **13.98** dB. The loop could tolerate 55° more lag or five times more gain before oscillating.

### Solution 12-06.2

$\lvert T \rvert = 10^4/\sqrt{1 + (f/100)^2} = 1$ gives $f_c = 100\sqrt{10^8 - 1}$ Hz = **1.000** MHz. The phase there is $-\arctan(10^4)$ = −89.99°, so PM = **90.0**°. The closed-loop pole is at $f_1(1 + T_0)$ = **1.000** MHz: a single-pole loop has no overshoot and can never oscillate.

### Solution 12-06.3

With $r$ = 1, $x^2(1 + x^2) = 1$ gives $x^2 = (\sqrt5 - 1)/2$, so $x$ = 0.7862 and PM $= 90^\circ - \arctan(0.7862)$ = **51.83**°. $Q = 1/\sqrt{r}$ = **1**, $\zeta$ = 0.5, and the overshoot is $e^{-\pi \times 0.5/0.8660}$ = **16.30**%.

### Solution 12-06.4

PM = 45° means $\arctan(x/r) = 45^\circ$, so the crossover sits on the second pole, $x = r$. Then $x^2(1 + 1) = 1$ gives $x = r = 1/\sqrt2$ = **0.7071**. $Q = 1/\sqrt r = 2^{1/4}$ = **1.189**, $\zeta = 1/(2Q)$ = **0.4204**, and the overshoot is $e^{-\pi\zeta/\sqrt{1 - \zeta^2}}$ = **23.32**%.

### Solution 12-06.5

The phase reaches −180° at 33.32 MHz regardless of β, where $\lvert A \rvert$ = 81.83 (Example 12-06.3). The loop gain there is $81.83\beta$, which must be below one: $\beta < 1/81.83$ = **0.01222**. The closed-loop gain must therefore exceed about **81.83** V/V, or **38.26** dB. This is the sense in which a decompensated amplifier is "stable above a minimum gain".

### Solution 12-06.6

(a) $f_d = 2\ \text{MHz}/10^5$ = **20** Hz. Solving $\lvert T \rvert$ = 1 gives a crossover of 1.569 MHz, where the 2 MHz pole contributes 38.11° and the 20 MHz pole 4.49°; with the dominant pole's 90.00°, PM = **47.40**°.

(b) Solving PM = 45° numerically gives $f_d$ = **22.18** Hz, with the crossover at **1.689** MHz. The rule "cross over at the first non-dominant pole" lands close to 45° because that pole contributes about 45° there, minus a little because the crossover falls below $A_0f_d$, plus the far pole's few degrees.

### Solution 12-06.7

$C_c = 0.22 \times 2\ \text{pF}$ = **0.44** pF. GBW $= 0.5\ \text{mA/V}/(2\pi \times 0.44\ \text{pF})$ = **180.9** MHz. $p_2 \approx 5\ \text{mA/V}/(2\pi \times 2\ \text{pF})$ = **397.9** MHz, which is 2.2 times the GBW. The zero is at $5\ \text{mA/V}/(2\pi \times 0.44\ \text{pF})$ = **1809** MHz, ten times the GBW. PM ≈ $90 - 24.44 - 5.71$ = **59.85**°.

### Solution 12-06.8

The zero is now at $g_{m2}/C_c = g_{m1}/C_c = \omega_u$, so at crossover it contributes $\arctan(1)$ = 45° of lag. PM ≈ $90 - 24.44 - 45$ = **20.56**°. The right-half-plane zero caused the loss: it costs as much phase as a pole at the same frequency while lifting the gain, which is why $g_{m2}$ has to be several times $g_{m1}$.

### Solution 12-06.9

To remove the zero, $R_z = 1/g_{m2}$ = **200** Ω. To cancel $p_2$, $R_z = (1 + C_L/C_c)/g_{m2} = (1 + 4.545)/5\ \text{mA/V}$ = **1109** Ω. The third pole is near $1/(2\pi R_zC_1) = 1/(2\pi \times 1109\ \Omega \times 0.1\ \text{pF})$ = **1435** MHz.

### Solution 12-06.10

$p_2 \approx g_{m2}/(2\pi C_L)$ = **159.2** MHz, now close to the 144.7 MHz GBW. PM ≈ $90 - \arctan(144.7/159.2) - 5.71$ = **42.02**°. The exact 45.91° is higher because the true crossover (110.8 MHz) is well below the GBW, where both non-dominant terms add less lag. Either way, doubling the load cost about **13**° (exact) to **18**° (estimated) of margin.

### Solution 12-06.11

The zero costs $\arctan(g_{m1}/g_{m2})$ = 5.711° whatever $C_c$ is, so $p_2$ may cost $90 - 60 - 5.711$ = 24.29°, that is $\omega_u/p_2 = \tan 24.29^\circ$ = **0.4513**. Writing $x = 1/C_c$ in pF⁻¹,

$$
\frac{\omega_u}{p_2} = \frac{g_{m1}}{g_{m2}}\left[\frac{C_1C_L}{C_c^2} + \frac{C_1 + C_L}{C_c}\right] = 0.1\,(x^2 + 5.2x) = 0.4513 ,
$$

so $x^2 + 5.2x - 4.513 = 0$, $x$ = 0.7575 pF⁻¹ and $C_c$ = **1.320** pF. The estimate takes the crossover as $g_{m1}/C_c$, but the non-dominant pole pulls the true crossover lower, where every lag term is smaller; the estimate is therefore conservative. At 1.320 pF the true margin is 62.20°, and 1.180 pF already gives 60°.

### Solution 12-06.12

From the overshoot, $\zeta = -\ln(0.2)/\sqrt{\pi^2 + \ln^2(0.2)}$ = **0.4559**, so $Q = 1/(2\zeta)$ = **1.097** and $r = 1/Q^2$ = **0.8316**. Solving $x^2(1 + x^2/r^2) = 1$ and PM $= 90^\circ - \arctan(x/r)$ gives PM = **48.15**°. A scope and Table 1 together give a quick read of a loop's margin without breaking the loop.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 12-06.1a | phase margin | 55 | ° |
| 12-06.1b | gain margin | 13.98 | dB |
| 12-06.2a | crossover | 1.000 | MHz |
| 12-06.2b | phase margin | 90.0 | ° |
| 12-06.2c | closed-loop pole | 1.000 | MHz |
| 12-06.3a | phase margin | 51.83 | ° |
| 12-06.3b | Q | 1 | — |
| 12-06.3c | overshoot | 16.30 | % |
| 12-06.4a | f_2/f_u | 0.7071 | — |
| 12-06.4b | Q | 1.189 | — |
| 12-06.4c | damping ratio | 0.4204 | — |
| 12-06.4d | overshoot | 23.32 | % |
| 12-06.5a | largest feedback factor | 0.01222 | — |
| 12-06.5b | minimum closed-loop gain | 81.83 | — |
| 12-06.5c | minimum closed-loop gain | 38.26 | dB |
| 12-06.6a | dominant pole by the rule | 20 | Hz |
| 12-06.6b | phase margin by the rule | 47.40 | ° |
| 12-06.6c | dominant pole for 45° | 22.18 | Hz |
| 12-06.6d | crossover for 45° | 1.689 | MHz |
| 12-06.7a | compensation capacitor | 0.44 | pF |
| 12-06.7b | GBW | 180.9 | MHz |
| 12-06.7c | p_2 | 397.9 | MHz |
| 12-06.7d | right-half-plane zero | 1809 | MHz |
| 12-06.7e | phase margin estimate | 59.85 | ° |
| 12-06.8a | phase margin estimate | 20.56 | ° |
| 12-06.9a | R_z removing the zero | 200 | Ω |
| 12-06.9b | R_z cancelling p_2 | 1109 | Ω |
| 12-06.9c | third pole | 1435 | MHz |
| 12-06.10a | p_2 estimate | 159.2 | MHz |
| 12-06.10b | phase margin estimate | 42.02 | ° |
| 12-06.10c | exact phase margin | 45.91 | ° |
| 12-06.10d | exact crossover | 110.8 | MHz |
| 12-06.11a | allowed ω_u/p_2 | 0.4513 | — |
| 12-06.11b | estimated C_c | 1.320 | pF |
| 12-06.11c | exact phase margin there | 62.20 | ° |
| 12-06.11d | exact C_c for 60° | 1.180 | pF |
| 12-06.12a | damping ratio | 0.4559 | — |
| 12-06.12b | Q | 1.097 | — |
| 12-06.12c | f_2/f_u | 0.8316 | — |
| 12-06.12d | phase margin | 48.15 | ° |
| 12-06.2d | phase at crossover | −89.99 | ° |
| 12-06.3d | normalized crossover x | 0.7862 | — |
| 12-06.6e | crossover by the rule | 1.569 | MHz |
| 12-06.6f | 2 MHz pole's lag there | 38.11 | ° |
| 12-06.6g | 20 MHz pole's lag there | 4.49 | ° |
| 12-06.6h | dominant pole's lag there | 90.00 | ° |
| 12-06.9d | C_L/C_c | 4.545 | — |
| 12-06.10e | exact margin lost | 13 | ° |
| 12-06.10f | estimated margin lost | 18 | ° |
| 12-06.11e | zero's phase cost | 5.711 | ° |
| 12-06.11f | phase allowed for p_2 | 24.29 | ° |
| 12-06.11g | 1/C_c | 0.7575 | pF⁻¹ |
