# Solutions 13-09 · The Smith Chart and Impedance Matching

Problems: [13-09 problems](../problems/13-09-problems.md) · Chapter: [13-09](../chapters/13-09-smith-chart-and-matching.md). Every number below is recomputed by [verify_13_09.py](../verify/verify_13_09.py), which marches the line equations numerically, solves each matching network by nodal analysis, and finds positions and optima by root finding and minimization.

---

## Solutions

### Solution 13-09.1

$\Gamma = (z - 1)/(z + 1) = (-0.5 - j0.5)/(1.5 - j0.5)$ = **−0.2 − j0.4**: magnitude **0.4472** at **−116.6**°. VSWR = **2.618**. The point lies on the same |Γ| circle as Example 13-09.1's load 2 + j1, so a length of line would carry one into the other.

### Solution 13-09.2

The $r$ = 0.5 circle: centre $(r/(1 + r), 0)$ = **(0.3333, 0)**, radius $1/(1 + r)$ = **0.6667**. The $x$ = −2 circle: centre $(1, 1/x)$ = **(1, −0.5)**, radius $1/\lvert x\rvert$ = **0.5**.

### Solution 13-09.3

$z$ = 1 + j1 has Γ = j1/(2 + j1) = 0.2 + j0.4; −Γ = −0.2 − j0.4 reads as **0.5 − j0.5**, which equals $1/(1 + j1)$. The point $z$ = 1 + j1 lies on the $r$ = 1 circle; its admittance lies on the $g$ = 0.5 circle.

### Solution 13-09.4

$z_L$ = 0.6 + j0.8, so $\Gamma_L$ = (−0.4 + j0.8)/(1.6 + j0.8) = 0.5 at 90°. Rotating clockwise by $2\beta d$ = 108° gives Γ = 0.5 at −18°, and $Z_{in} = 50(1 + \Gamma)/(1 - \Gamma)$ = **125.4 − j51.68** Ω, matching the 13-08 formula.

### Solution 13-09.5

$\Gamma_L = (50 + j100)/(150 + j100)$, magnitude 0.6202 at 29.74°. The impedance is real where Γ(d) is real; the nearest such point toward the generator is where the angle reaches 0°, a rotation of 29.74°, so $d = 29.74/720$ = **0.04131**λ. There Γ is real and positive, so $Z_{in} = Z_0 \times \text{VSWR}$ = **213.3** Ω (VSWR **4.266**). A further λ/4 gives the minimum, $Z_0/\text{VSWR}$.

### Solution 13-09.6

$Q = \sqrt{200/50 - 1}$ = **1.732**. The shunt element goes across the higher resistance (the 200 Ω load) and the series element on the 50 Ω side. Shunt susceptance $Q/200$ = 8.660 mS, here an inductor: $1/(\omega B)$ = **183.8** nH. Series reactance $Q \times 50$ = 86.60 Ω, a capacitor: $1/(\omega X)$ = **18.38** pF. Check: 200 ∥ (j173.2) = 50 + j86.60 Ω, and the series −j86.60 cancels the reactance.

### Solution 13-09.7

The network of Example 13-09.4 needed a total series reactance of +20 Ω next to 10 Ω. The load already contributes +5 Ω, so the added inductor supplies 15 Ω: **0.9947** nH. The shunt capacitor is unchanged, **2.653** pF, because the resistive part is still 10 Ω.

### Solution 13-09.8

$y_L$ = 0.5. Rotating toward the generator until $g$ = 1: at $d$ = **0.1520**λ, $y$ = 1 + j0.7071; at $d$ = **0.3480**λ, $y$ = 1 − j0.7071. An open stub has $y = j\tan\beta\ell$. For the first, it must supply −j0.7071: $\tan\beta\ell$ = −0.7071, the shortest length **0.4020**λ. For the second, +j0.7071: ℓ = **0.09796**λ. The second solution has the shorter stub; the first the shorter line.

### Solution 13-09.9

$R_i = \sqrt{500}$ = 22.36 Ω. Each section steps by a ratio of $\sqrt5$, so each has $Q = \sqrt{\sqrt5 - 1}$ = **1.112**, against 2 for the single section. Designing each section with the formulas of §3.3 and sweeping the cascade, $\lvert\Gamma\rvert$ < 0.1 holds over **18.56**% of the centre frequency, against 11.25% for one section: lower Q, wider band.

### Solution 13-09.10

With the ideal rectangular response, $\Delta\omega\ln(1/\Gamma_m) \le \pi R/L$, so $\Delta f \le R/[2L\ln(1/\Gamma_m)] = 10/(2 \times 10^{-8} \times \ln 10)$ = **217.1** MHz. Covering many cellular bands from 600 MHz to 6 GHz with one small antenna at that match is impossible; phones use tuners and multiple antennas.

### Solution 13-09.11

$\Gamma = (12.5 - 50)/62.5$ = −0.6, VSWR **4**. Along the line the impedance is real at the |Γ| circle's two real-axis crossings: the smallest, **12.5** Ω (the load itself, $Z_0$/VSWR), and λ/4 away the largest, **200** Ω ($Z_0 \times$ VSWR).

### Solution 13-09.12

With $b$ fixed, $\alpha_c \propto (1/a + 1/b)/\ln(b/a) = (1 + x)/(b\ln x)$. Setting the derivative with respect to $x$ to zero: $\ln x - (1 + x)/x = 0$, that is $\ln x = 1 + 1/x$. Numerically $x$ = **3.591**, and $Z_0 = (\eta_0/2\pi)\ln x$ = **76.65** Ω.

### Solution 13-09.13

The peak field is at the inner conductor, $E(a) = V/[a\ln x]$, so the largest voltage is $E_{bd}a\ln x$ and the power $V^2/(2Z_0) \propto a^2\ln^2x/\ln x = (b^2/x^2)\ln x$. Maximizing $\ln x/x^2$: $(1 - 2\ln x)/x^3 = 0$, so $\ln x = 1/2$, $x = \sqrt e$ = **1.649**, and $Z_0 = (\eta_0/2\pi)/2$ = **29.98** Ω. The geometric mean with 76.65 Ω is **47.94** Ω.

### Solution 13-09.14

$B = \omega C$ = 0.04 S, normalized $b = BZ_0$ = 2. An open stub gives $j\tan\beta\ell$, so $\tan\beta\ell$ = 2, βℓ = 1.107 rad, ℓ = **0.1762**λ. At 2.4 GHz λ = 12.49 cm, so ℓ = **2.201** cm.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 13-09.1a | Γ real part | −0.2 | — |
| 13-09.1b | Γ imaginary part | −0.4 | — |
| 13-09.1c | Γ magnitude | 0.4472 | — |
| 13-09.1d | Γ angle | −116.6 | ° |
| 13-09.1e | VSWR | 2.618 | — |
| 13-09.2a | r = 0.5 centre | 0.3333 | — |
| 13-09.2b | r = 0.5 radius | 0.6667 | — |
| 13-09.2c | x = −2 centre (imaginary coordinate) | −0.5 | — |
| 13-09.2d | x = −2 radius | 0.5 | — |
| 13-09.3a | normalized conductance | 0.5 | — |
| 13-09.3b | normalized susceptance | −0.5 | — |
| 13-09.4a | input resistance | 125.4 | Ω |
| 13-09.4b | input reactance | −51.68 | Ω |
| 13-09.5a | distance to a real impedance | 0.04131 | λ |
| 13-09.5b | impedance there | 213.3 | Ω |
| 13-09.5c | VSWR | 4.266 | — |
| 13-09.6a | network Q | 1.732 | — |
| 13-09.6b | shunt inductance | 183.8 | nH |
| 13-09.6c | series capacitance | 18.38 | pF |
| 13-09.7a | added series inductance | 0.9947 | nH |
| 13-09.7b | shunt capacitance | 2.653 | pF |
| 13-09.8a | first position | 0.1520 | λ |
| 13-09.8b | first open-stub length | 0.4020 | λ |
| 13-09.8c | second position | 0.3480 | λ |
| 13-09.8d | second open-stub length | 0.09796 | λ |
| 13-09.9a | Q of each section | 1.112 | — |
| 13-09.9b | two-section bandwidth | 18.56 | % |
| 13-09.10a | Bode–Fano bandwidth | 217.1 | MHz |
| 13-09.11a | VSWR | 4 | — |
| 13-09.11b | smallest impedance | 12.5 | Ω |
| 13-09.11c | largest impedance | 200 | Ω |
| 13-09.12a | minimum-loss radius ratio | 3.591 | — |
| 13-09.12b | minimum-loss impedance | 76.65 | Ω |
| 13-09.13a | maximum-power radius ratio | 1.649 | — |
| 13-09.13b | maximum-power impedance | 29.98 | Ω |
| 13-09.13c | geometric mean | 47.94 | Ω |
| 13-09.14a | stub length | 0.1762 | λ |
| 13-09.14b | stub length | 2.201 | cm |
