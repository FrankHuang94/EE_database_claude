# Solutions 13-08 · Transmission Lines: Sinusoidal Steady State

Problems: [13-08 problems](../problems/13-08-problems.md) · Chapter: [13-08](../chapters/13-08-transmission-lines-sinusoidal-steady-state.md). Every number below is recomputed by [verify_13_08.py](../verify/verify_13_08.py), which integrates the phasor telegrapher's equations numerically from the load to the input instead of using the closed-form input-impedance formula.

---

## Solutions

### Solution 13-08.1

$Z_0 = \sqrt{L'/C'}$ and $v = 1/\sqrt{L'C'}$ give $L' = Z_0/v$ = **375.0** nH/m and $C' = 1/(Z_0v)$ = **66.67** pF/m. At 100 MHz, β = ω/v = **3.142** rad/m (a 2 m wavelength).

### Solution 13-08.2

$Z_{in} = Z_0^2/Z_L = 2500/(25 + j25)$ = **50 − j50** Ω. An inductive load became capacitive: a quarter wave inverts reactance as well as resistance.

### Solution 13-08.3

|Γ| = 0.1: return loss **20** dB, VSWR **1.222**, mismatch loss **0.04365** dB. |Γ| = 0.3: return loss **10.46** dB, VSWR **1.857**, mismatch loss **0.4096** dB.

### Solution 13-08.4

βℓ = 0.6π = 108°, so $\tan\beta\ell$ = −3.078. Then

$$
Z_{in} = 50\,\frac{(30 - j40) + j50(-3.078)}{50 + j(30 - j40)(-3.078)} = \mathbf{56.63 + j61.08}\ \Omega .
$$

(Carry the complex arithmetic carefully: the denominator is $50 - 123.1 - j92.33$.)

### Solution 13-08.5

$jZ_0\tan\beta\ell = j\omega L$ needs $\tan\beta\ell = 2\pi \times 10^9 \times 10^{-8}/50$ = 1.257, so βℓ = **0.8986** rad, or **0.1430**λ, and with λ = 29.98 cm, **4.288** cm.

### Solution 13-08.6

A 2 pF capacitor has $X = -1/(\omega C)$ = **−79.58** Ω. $-jZ_0\cot\beta\ell = -j79.58$ gives $\tan\beta\ell = 50/79.58$, βℓ = 0.5610 rad, and the length **2.677** cm.

### Solution 13-08.7

$\lvert\Gamma_L\rvert = (2 - 1)/(2 + 1)$ = **0.3333**. At a voltage minimum Γ(d) is real and negative: $\Gamma_Le^{-j2\beta d} = -1/3$ with $2\beta d = 2 \times 2\pi \times 0.1 = 0.4\pi$. So $\Gamma_L = -\tfrac13e^{j0.4\pi} = \tfrac13e^{j1.4\pi}$, an angle of **−108**°. Then $Z_L = 50(1 + \Gamma_L)/(1 - \Gamma_L)$ = **33.74 − j24.07** Ω.

### Solution 13-08.8

The generator is matched to the line, so it launches $V_0^+ = 10/2$ = 5 V whatever the load. $\Gamma_L = 1/3$, and $P = 5^2/(2 \times 50)(1 - 1/9)$ = **0.2222** W, against **0.25** W into a matched load: an 11% (0.51 dB) shortfall.

### Solution 13-08.9

VSWR 3 means |Γ| = 0.5, a return loss of $-20\log 0.5$ = 6.021 dB at the antenna. Through 7.054 dB of cable the reflection is reduced by twice that, so the radio sees **20.13** dB: still an apparently good match from a load that reflects a quarter of the power reaching it.

### Solution 13-08.10

(a) Scanning frequency with $Z_1$ = 70.71 Ω and solving for |Γ| = 0.05 gives **18.09**%, half the bandwidth for |Γ| < 0.1. (b) With $Z_1 = \sqrt{500}$ = 22.36 Ω, |Γ| < 0.1 holds over only **14.34**%, against 36.70% for the 2:1 step: larger ratios need multisection transformers.

### Solution 13-08.11

At 1 MHz, $\omega L'$ = 1.571 Ω/m is only three times $R'$, so

$$
\gamma = \sqrt{(0.5 + j1.571)(j6.283 \times 10^{-4})} = 0.004939 + j0.03180\ \text{m}^{-1}, \qquad
Z_0 = \sqrt{\frac{0.5 + j1.571}{j6.283 \times 10^{-4}}} = 50.61 - j7.861\ \Omega ,
$$

that is α = **0.004939** Np/m (**0.04290** dB/m) and $Z_0$ = **50.61 − j7.861** Ω. At 100 MHz, $R'$ is negligible beside $\omega L'$ = 157 Ω/m: α = **0.005000** Np/m and $Z_0$ = **50.00 − j0.07958** Ω. At low frequency the series resistance is comparable to the series reactance, so $(R' + j\omega L')$ has a large phase angle and $Z_0$ inherits half of it. Audio and telephone lines live in this regime.

### Solution 13-08.12

$G' = R'C'/L' = 0.5 \times 100 \times 10^{-12}/(250 \times 10^{-9})$ = **2 × 10⁻⁴** S/m. Then α = $\sqrt{R'G'}$ = **0.01** Np/m at every frequency, $Z_0 = \sqrt{L'/C'}$ = **50** Ω (real), and $v = 1/\sqrt{L'C'}$ = **2 × 10⁸** m/s. The price is double the attenuation at high frequency (the added $G'$ contributes as much as $R'$); the gain is a frequency-independent response.

### Solution 13-08.13

λ/2: $Z_{in} = Z_L$ = **20 + j30** Ω. λ/4: $Z_{in} = 2500/(20 + j30)$ = **38.46 − j57.69** Ω.

### Solution 13-08.14

$\Gamma_L = (25 - 50)/75 = -1/3$, real and negative, so the voltage minimum is **at the load**, $1 - 1/3$ = **0.6667** V, and the nearest maximum, **1.333** V, is λ/4 = **7.495** cm toward the source. The current is largest where the voltage is smallest: at the load, $\lvert I\rvert = (1/50)(1 + 1/3)$ = **26.67** mA (equal to 0.6667 V / 25 Ω, as it must be).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 13-08.1a | inductance per metre | 375.0 | nH/m |
| 13-08.1b | capacitance per metre | 66.67 | pF/m |
| 13-08.1c | phase constant | 3.142 | rad/m |
| 13-08.2a | input resistance | 50 | Ω |
| 13-08.2b | input reactance | −50 | Ω |
| 13-08.3a | return loss at 0.1 | 20 | dB |
| 13-08.3b | VSWR at 0.1 | 1.222 | — |
| 13-08.3c | mismatch loss at 0.1 | 0.04365 | dB |
| 13-08.3d | return loss at 0.3 | 10.46 | dB |
| 13-08.3e | VSWR at 0.3 | 1.857 | — |
| 13-08.3f | mismatch loss at 0.3 | 0.4096 | dB |
| 13-08.4a | input resistance | 56.63 | Ω |
| 13-08.4b | input reactance | 61.08 | Ω |
| 13-08.5a | electrical length | 0.8986 | rad |
| 13-08.5b | length in wavelengths | 0.1430 | — |
| 13-08.5c | length | 4.288 | cm |
| 13-08.6a | capacitor reactance | −79.58 | Ω |
| 13-08.6b | stub length | 2.677 | cm |
| 13-08.7a | reflection magnitude | 0.3333 | — |
| 13-08.7b | reflection angle | −108 | ° |
| 13-08.7c | load resistance | 33.74 | Ω |
| 13-08.7d | load reactance | −24.07 | Ω |
| 13-08.8a | power to the load | 0.2222 | W |
| 13-08.8b | power if matched | 0.25 | W |
| 13-08.9a | apparent return loss | 20.13 | dB |
| 13-08.10a | bandwidth for 0.05, 2:1 | 18.09 | % |
| 13-08.10b | bandwidth for 0.1, 5:1 | 14.34 | % |
| 13-08.11a | attenuation at 1 MHz | 0.004939 | Np/m |
| 13-08.11b | attenuation at 1 MHz | 0.04290 | dB/m |
| 13-08.11c | Z0 real part at 1 MHz | 50.61 | Ω |
| 13-08.11d | Z0 imaginary part at 1 MHz | −7.861 | Ω |
| 13-08.11e | attenuation at 100 MHz | 0.005000 | Np/m |
| 13-08.11f | Z0 real part at 100 MHz | 50.00 | Ω |
| 13-08.11g | Z0 imaginary part at 100 MHz | −0.07958 | Ω |
| 13-08.12a | shunt conductance | 2 × 10⁻⁴ | S/m |
| 13-08.12b | attenuation | 0.01 | Np/m |
| 13-08.12c | characteristic impedance | 50 | Ω |
| 13-08.12d | velocity | 2 × 10⁸ | m/s |
| 13-08.13a | λ/2 input resistance | 20 | Ω |
| 13-08.13b | λ/2 input reactance | 30 | Ω |
| 13-08.13c | λ/4 input resistance | 38.46 | Ω |
| 13-08.13d | λ/4 input reactance | −57.69 | Ω |
| 13-08.14a | minimum voltage | 0.6667 | V |
| 13-08.14b | maximum voltage | 1.333 | V |
| 13-08.14c | distance to the maximum | 7.495 | cm |
| 13-08.14d | current at the load | 26.67 | mA |
