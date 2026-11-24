# Solutions 20-03 · Bandgap and Voltage References

Problems: [20-03 problem set](../problems/20-03-problems.md) · Chapter: [20-03](../chapters/20-03-bandgap-references.md). Every number below is recomputed by [verify_20_03.py](../verify/verify_20_03.py).

---

## Solutions

### Solution 20-03.1

$V_{BE0} = V_T\ln(I/I_{S0})$ and, for PTAT bias, $dV_{BE}/dT = (V_{BE0} - V_{g0} - 2V_T)/T_0$:

| Current | $V_{BE0}$ | Slope |
|---|---|---|
| 1 µA | **0.6369** V | **−2.052** mV/K |
| 20 µA | **0.7143** V | **−1.794** mV/K |

The higher current density gives the flatter junction voltage: $V_{BE0}$ is closer to $V_{g0}$, and the slope is the distance to $V_{g0}$ divided by $T_0$ (plus the small curvature term).

### Solution 20-03.2

$(k/q)\ln N$ is **179.2** µV/K for $N$ = 8 and **273.9** µV/K for $N$ = 24, so $K$ = 1.914/0.1792 = **10.68** and 1.914/0.2739 = **6.99**. The larger $N$ needs less gain, so the op-amp's offset and noise reach the output multiplied by less (Problem 20-03.13); the price is area and a less symmetric layout.

### Solution 20-03.3

(a) With $m$ = 0, §3.1 gives $V_{BE}(T) = V_{g0} - (V_{g0} - V_{BE0})T/T_0 - \eta V_T\ln(T/T_0)$. Adding $KV_T\ln N$ (linear in $T$) and setting the slope to zero at $T_c$ gives $K(k/q)\ln N = (V_{g0} - V_{BE0})/T_0 + \eta(k/q)\,[\ln(T_c/T_0) + 1]$. Substituting back, the linear terms in $V_{g0} - V_{BE0}$ cancel and

$$
V_{REF}(T) = V_{g0} + \eta V_T(T)\left[1 - \ln\frac{T}{T_c}\right],
$$

whose value at $T_c$ is $V_{g0} + \eta V_T(T_c)$.

(b) At 300 K: $V_{g0} + 3V_T$ = **1.2785** V, against **1.2526** V for PTAT bias. A constant bias current also gives a larger curvature coefficient (η instead of η − 1), and so a box TC about **47**% larger (not quite 50%, because $V_{nom}$ also rises).

### Solution 20-03.4

Centering $T_c$ so that the arch $V_{g0} + 2V_T[1 - \ln(T/T_c)]$ is equal at both ends:

| Range | Centered $T_c$ | Variation | Box TC |
|---|---|---|---|
| −55 to 125 °C | **30.5** °C | **2.304** mV | **10.21** ppm/K |
| −40 to 85 °C | **20.3** °C | **1.149** mV | **7.34** ppm/K |
| −40 to 125 °C (chapter) | 38.9 °C | 1.884 mV | 9.10 ppm/K |

The TC grows with the range because the arch's height grows roughly as the square of the range, while the box divides by the range only once.

### Solution 20-03.5

$V_{BE0}$ = $V_T\ln(2\ \mu\text{A}/2 \times 10^{-17}\ \text{A})$ = **0.6548** V; $R_1 = V_T\ln 24/2\ \mu\text{A}$ = **41.08** kΩ; zero TC at 312.0 K gives $K$ = **7.30** and $R_2$ = **299.9** kΩ. The output at 300 K is **1.25463** V, the same as the original design. From §3.3, a first-order bandgap's output is $V_{g0} + (\eta - 1)V_T(T)\,[1 - \ln(T/T_c)]$: it depends only on $V_{g0}$, η and the chosen $T_c$, not on the current, $N$ or the resistors, which only fix how the zero slope is reached.

### Solution 20-03.6

A 20% lower $I_S$ raises every $V_{BE}$ by $-V_T\ln 0.8$, so the output error is **+5.77** mV at 300 K with slope **+19.2** µV/K (PTAT). Trimming means changing $K$ by $\Delta K/K = \ln(0.8)/(K\ln 8)$ = **−1.00**%, i.e. lowering $R_2$ by 1.00%, which removes the error at all temperatures. The exact circuit solution gives the same −1.00%.

### Solution 20-03.7

The 0.2 mV offset lowers the 300 K output by **2.55** mV (about $1 + R_2/R_1$ times the offset). Trimming $R_2$ to restore 1.25463 V at 300 K adds a PTAT slope: the box TC becomes **12.7** ppm/K and the error at 125 °C **+0.837** mV. That is still worse than the untrimmed curvature floor of 9.10 ppm/K, but far better than the 34.6 ppm/K of the 1 mV case: the trimmed TC penalty scales with the offset.

### Solution 20-03.8

(a) A 0.5% higher $R_2$ multiplies the PTAT term $KV_T\ln N$ (0.5741 V at 300 K) by 1.005: the error is **+2.88** mV at 300 K, proportional to $V_T$ and hence PTAT, and it is removed by the same one-temperature trim.

(b) Nothing happens to the output: it depends only on the ratio $R_2/R_1$, which a common temperature coefficient leaves unchanged. The current $V_T\ln N/R_1$ changes by the PTAT factor 400/300 = **1.333** divided by the resistor factor 1 + 2000 × 10⁻⁶ × 100 = **1.2**, so it rises by a factor of **1.111** instead of 1.333. (The junction current then is no longer exactly PTAT, which slightly changes the curvature; the lab can show by how much.)

### Solution 20-03.9

(a) Each branch carries 10.89 µA (as in Example 20-03.4), so $R_3$ = 0.5 V/10.89 µA = **45.92** kΩ.

(b) The junction current is PTAT: 5 µA × 233.15/300 at −40 °C, and $V_{BE1}$ = **0.805** V there. With 0.15 V for the current source, the supply must exceed about **0.955** V. The cold corner sets the minimum supply, not room temperature.

### Solution 20-03.10

(a) From §3.1 with the same $V_{BE0}$:

$$
V_{BE,m=1} - V_{BE,m=0} = -(\eta - 1)V_T\ln\frac{T}{T_0} + \eta V_T\ln\frac{T}{T_0} = V_T\ln\frac{T}{T_0} .
$$

(b) Uncompensated, $c = \eta - 1$ = 2.5: box TC **11.25** ppm/K. Compensated with α = 2, $c$ = 0.5: **2.35** ppm/K, an improvement of **4.79**. The residual coefficient 0.5 is a quarter of the design value 2, so the correction removes only about **80**% of the curvature.

### Solution 20-03.11

(a) $I = V_T\ln K/R$, so $R = V_T\ln 8/(1\ \mu\text{A})$ = **53.76** kΩ.

(b) $I = nV_T\ln K/R$, so $R$ = **69.89** kΩ.

(c) Both circuits are self-biased and also satisfy their equations with zero current (all devices off), so they can power up dead.

### Solution 20-03.12

(a) The M1 curve rises exponentially with the gate voltage; the M2 + $R$ curve starts at four times M1's current (small $IR$) and then bends over as the resistor's drop grows. They meet at $V_G$ = **0.363** V, $I$ = **0.372** µA (Example 20-03.6), and again only in the limit of zero current.

(b) In the zero-current limit both devices are off and every node voltage is consistent with no current: a valid solution of the circuit equations, but no reference.

(c) M1 carries $I_P + δ$ and M2 carries $I_P$. In weak inversion $I_{M1} = I_0e^{V_P/V_T}$ and $I_{M2} = KI_0e^{(V_P - I_PR)/V_T}$; dividing, $(I_P + δ)/I_P = e^{I_PR/V_T}/K$, so $I_PR = V_T\ln[K(I_P + δ)/I_P]$. To first order $\Delta I_P \approx (V_T/R)(δ/I_P) = δ/\ln K$ = **0.72** nA, **0.19**% of the current. The exact charge-based model gives **+0.77** nA (**0.21**%): a startup leak of a nanoampere is already a 0.2% error.

### Solution 20-03.13

(a) The op-amp's noise reaches the output like its offset, multiplied by $1 + K$ = **11.72**: **352** nV/√Hz. Over 10 kHz the rms noise is 352 nV × √10⁴ = **35.2** µV, **28.0** ppm of 1.2546 V.

(b) With $N$ = 24, $K$ = **7.01**, so the gain is **8.01** and the noise **24.0** µV rms, 32% less.

### Solution 20-03.14

(a) The box method bounds the variation over the range by TC × $V_{nom}$ × ΔT = 3 × 165 = 495 ppm. Adding the ±500 ppm initial accuracy, the worst-case band is **995** ppm, **2.49** mV on 2.5 V.

(b) A 12-bit LSB is **244** ppm and a 16-bit LSB **15.3** ppm. The reference uses about four 12-bit LSBs of the error budget, and is far from adequate for absolute 16-bit accuracy without system calibration. (Gain calibration at one temperature removes the initial error, leaving the 495 ppm of temperature drift.)

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 20-03.1a | V_BE0 at 1 uA | 0.6369 | V |
| 20-03.1b | slope at 1 uA | −2.052 | mV/K |
| 20-03.1c | V_BE0 at 20 uA | 0.7143 | V |
| 20-03.1d | slope at 20 uA | −1.794 | mV/K |
| 20-03.2a | PTAT slope, N = 8 | 179.2 | µV/K |
| 20-03.2b | PTAT slope, N = 24 | 273.9 | µV/K |
| 20-03.2c | K, N = 8 | 10.68 | — |
| 20-03.2d | K, N = 24 | 6.99 | — |
| 20-03.3a | magic voltage, constant current | 1.2785 | V |
| 20-03.3b | magic voltage, PTAT current | 1.2526 | V |
| 20-03.3c | box-TC increase for constant-current bias | 47 | % |
| 20-03.4a | centered T_c, −55 to 125 C | 30.5 | °C |
| 20-03.4b | variation, −55 to 125 C | 2.304 | mV |
| 20-03.4c | box TC, −55 to 125 C | 10.21 | ppm/K |
| 20-03.4d | centered T_c, −40 to 85 C | 20.3 | °C |
| 20-03.4e | variation, −40 to 85 C | 1.149 | mV |
| 20-03.4f | box TC, −40 to 85 C | 7.34 | ppm/K |
| 20-03.5a | V_BE0 at 2 uA | 0.6548 | V |
| 20-03.5b | R_1 | 41.08 | kΩ |
| 20-03.5c | K | 7.30 | — |
| 20-03.5d | R_2 | 299.9 | kΩ |
| 20-03.5e | output at 300 K | 1.25463 | V |
| 20-03.6a | error from I_S − 20 % | 5.77 | mV |
| 20-03.6b | its slope | 19.2 | µV/K |
| 20-03.6c | change of K | −1.00 | % |
| 20-03.7a | error from 0.2 mV offset | −2.55 | mV |
| 20-03.7b | trimmed box TC | 12.7 | ppm/K |
| 20-03.7c | error at 125 C after trim | 0.837 | mV |
| 20-03.8a | error from R_2 + 0.5 % | 2.88 | mV |
| 20-03.8b | PTAT factor 400/300 | 1.333 | — |
| 20-03.8c | resistor factor | 1.2 | — |
| 20-03.8d | current factor | 1.111 | — |
| 20-03.9a | R_3 for 0.5 V | 45.92 | kΩ |
| 20-03.9b | V_BE1 at −40 C | 0.805 | V |
| 20-03.9c | minimum supply | 0.955 | V |
| 20-03.10a | box TC, eta = 3.5, uncompensated | 11.25 | ppm/K |
| 20-03.10b | box TC, eta = 3.5, alpha = 2 | 2.35 | ppm/K |
| 20-03.10c | improvement | 4.79 | — |
| 20-03.10d | fraction of the curvature removed | 80 | % |
| 20-03.11a | R, bulks grounded | 53.76 | kΩ |
| 20-03.11b | R, source-tied well | 69.89 | kΩ |
| 20-03.12a | gate voltage at the operating point | 0.363 | V |
| 20-03.12b | operating current | 0.372 | µA |
| 20-03.12c | first-order current change | 0.72 | nA |
| 20-03.12d | exact current change | 0.77 | nA |
| 20-03.12e | exact relative change | 0.21 | % |
| 20-03.12f | first-order relative change | 0.19 | % |
| 20-03.13a | noise gain 1 + K | 11.72 | — |
| 20-03.13b | output noise density | 352 | nV/√Hz |
| 20-03.13c | rms noise in 10 kHz | 35.2 | µV |
| 20-03.13d | rms noise in ppm | 28.0 | ppm |
| 20-03.13e | K, N = 24 | 7.01 | — |
| 20-03.13f | noise gain, N = 24 | 8.01 | — |
| 20-03.13g | rms noise, N = 24 | 24.0 | µV |
| 20-03.13h | reduction | 32 | % |
| 20-03.14a | worst-case band | 995 | ppm |
| 20-03.14b | worst-case band | 2.49 | mV |
| 20-03.14c | 12-bit LSB | 244 | ppm |
| 20-03.14d | 16-bit LSB | 15.3 | ppm |
| 20-03.14e | temperature part of the band | 495 | ppm |
