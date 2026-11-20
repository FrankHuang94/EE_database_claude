# Solutions 13-06 · Reflection and Transmission of Waves

Problems: [13-06 problems](../problems/13-06-problems.md) · Chapter: [13-06](../chapters/13-06-reflection-and-transmission.md). Every number below is recomputed by [verify_13_06.py](../verify/verify_13_06.py), which solves each boundary as a linear system of field-continuity equations and each layered structure by the transfer-matrix method.

---

## Solutions

### Solution 13-06.1

$\eta_2 = \eta_0/2$, so $\Gamma = (\eta_0/2 - \eta_0)/(\eta_0/2 + \eta_0)$ = **−0.3333** (−1/3) and τ = **0.6667** (2/3). Reflected power $\Gamma^2$ = **11.11**%; transmitted $(\eta_1/\eta_2)\tau^2 = 2 \times 4/9$ = **88.89**%. $S = (1 + 1/3)/(1 - 1/3)$ = **2**.

### Solution 13-06.2

$\eta_2 = \eta_0/9$: Γ = (1/9 − 1)/(1/9 + 1) = **−0.8**, reflecting **64**% of the power, with $S$ = 1.8/0.2 = **9**. A high-permittivity medium is a strong mismatch to air, which is why water is a good radar reflector.

### Solution 13-06.3

λ = $c/f$ = 2.998 cm. The zeros are λ/2 = **1.499** cm apart (the first at the conductor), and the first maximum is λ/4 = **0.7495** cm in front of it.

### Solution 13-06.4

$\theta_c = \arcsin(1/1.33)$ = **48.75**°. For 30°: $\sin\theta_t = 1.33\sin 30^\circ$ = 0.665, so $\theta_t$ = **41.68**° in air. A diver looking up sees the whole sky compressed into a cone of half-angle 48.75° (Snell's window); outside it the surface acts as a mirror.

### Solution 13-06.5

$\theta_B = \arctan 1.5$ = 56.31°; at Brewster the transmitted ray is perpendicular to the reflected one, so $\theta_t = 90° - 56.31°$ = **33.69**°. Then

$$
\Gamma_\perp = \frac{(\eta_0/1.5)\cos 56.31^\circ - \eta_0\cos 33.69^\circ}{(\eta_0/1.5)\cos 56.31^\circ + \eta_0\cos 33.69^\circ} = \mathbf{-0.3846}
$$

(exactly −5/13), and the TE reflectance is **14.79**%. Unpolarized light reflected at this angle is purely TE.

### Solution 13-06.6

The layer's impedance must be $\sqrt{\eta_0 \times \eta_0/3} = \eta_0/\sqrt3$, so its relative permittivity is $\sqrt{1 \times 9}$ = **3**. Its thickness is a quarter of the wavelength inside it: $c/(4f\sqrt3)$ = **4.327** mm.

### Solution 13-06.7

Half a wavelength in the slab at 10 GHz: $c/(2f\sqrt{\varepsilon_r})$ = **7.495** mm. At other frequencies, use the layer formula of §3.2 with $\eta_2 = \eta_0/2$, $\eta_3 = \eta_0$ and $k_2d = \pi f/f_0$:

$$
\eta_{in} = \eta_2\,\frac{\eta_0 + j\eta_2\tan(\pi f/f_0)}{\eta_2 + j\eta_0\tan(\pi f/f_0)}, \qquad R = \Big\lvert\frac{\eta_{in} - \eta_0}{\eta_{in} + \eta_0}\Big\rvert^2 .
$$

At 11 GHz, $R$ = **5.098**%; at 12 GHz, **16.27**%. A 10% frequency offset already reflects 5% of the power each way through the radome.

### Solution 13-06.8

$\text{NA} = \sqrt{1.47^2 - 1.46^2}$ = **0.1712**, acceptance half-angle $\arcsin(0.1712)$ = **9.856**°, and $\theta_c = \arcsin(1.46/1.47)$ = **83.31**°.

### Solution 13-06.9

$\eta_c = \sqrt{j\omega\mu_0/(\sigma + j\omega\varepsilon)}$ = **0.09935 + j0.09935** Ω (a good conductor, so the real and imaginary parts are equal to four figures). $\Gamma = (\eta_c - \eta_0)/(\eta_c + \eta_0)$ = **−0.9995** (to four figures, with a tiny imaginary part). The transmitted power is $1 - \lvert\Gamma\rvert^2$ = **0.1054**%. For real $\eta_0$ this is exactly $(\lvert\eta_c + \eta_0\rvert^2 - \lvert\eta_c - \eta_0\rvert^2)/\lvert\eta_c + \eta_0\rvert^2 = 4\eta_0\text{Re}\{\eta_c\}/\lvert\eta_c + \eta_0\rvert^2$, and with $\lvert\eta_c\rvert \ll \eta_0$ the denominator is nearly $\eta_0^2$, giving the estimate $4\,\text{Re}\{\eta_c\}/\eta_0$ = **0.1055**%. Almost everything reflects, and the little that enters is then attenuated by the skin depth of 2.5 m (13-05).

### Solution 13-06.10

δ = $1/\sqrt{\pi f\mu_0\sigma}$ = 85.07 µm, so $t/\delta$ = 5.877 and $A$ = **51.05** dB. $\lvert\eta_c\rvert = \sqrt2/(\sigma\delta)$ = 0.4750 mΩ, so $R = 20\log_{10}(376.7/(4 \times 0.4750\ \text{mΩ}))$ = **105.9** dB. Total **157.0** dB. At 1 MHz the sheet is still effectively perfect against plane waves; against a low-frequency magnetic near field the reflection term would be far smaller.

### Solution 13-06.11

(a) In the transmission-line picture, the metal is a short circuit, and a quarter-wave section of air transforms it into an open circuit at the sheet's position. The sheet, 376.7 Ω per square, then appears as a resistance $\eta_0$ in parallel with an open circuit: exactly the free-space impedance, so Γ = 0. All the power is absorbed in the sheet.

(b) At $1.2f_0$ the air gap is $1.2 \times 90° = 108°$ long, so the shorted section presents $j\eta_0\tan 108^\circ = -j3.078\eta_0$. In parallel with $\eta_0$: $\eta_{in} = \eta_0(0.9046 - j0.2939)$, and $\lvert\Gamma\rvert$ = **0.1604** = **−15.90** dB, reflecting **2.571**% of the power. The screen absorbs well over a band, not just at one frequency.

### Solution 13-06.12

$\theta_c = \arcsin(1/1.5)$ = 41.8° < 60°, so the wave is totally reflected. $\alpha = k_0\sqrt{n^2\sin^2\theta - 1}$ with $k_0 = 2\pi/1550$ nm: $\alpha$ = **3.361** µm⁻¹, and the field falls by $e$ in **297.5** nm, about a fifth of the vacuum wavelength.

### Solution 13-06.13

$\tau_\perp = 1 + \Gamma_\perp = 1 - 0.3033$ = **0.6967**. $T = (\eta_0\cos 28.13^\circ)/((\eta_0/1.5)\cos 45^\circ) \times 0.6967^2$ = **0.9080**, and $R = 0.3033^2$ = 0.09201, so $R + T$ = **1**, as energy conservation requires at a lossless boundary.

### Solution 13-06.14

With Γ = −1/3: the maximum is $1 + 1/3$ = **1.333** V/m and the minimum $1 - 1/3$ = **0.6667** V/m. Γ is negative, so the minimum is at the boundary itself (the incident and reflected fields subtract there), and the nearest maximum is λ/4 = **7.495** mm in front of it.

### Solution 13-06.15

(a) With the boundary at $z = 0$ and the fields of §3.4 (incident $\tilde{\vec{E}}^i = E_0(\hat{x}\cos\theta_i - \hat{z}\sin\theta_i)$, $\tilde{\vec{H}}^i = (E_0/\eta_1)\hat{y}$; reflected $\Gamma_\parallel E_0(\hat{x}\cos\theta_i + \hat{z}\sin\theta_i)$ and $-(\Gamma_\parallel E_0/\eta_1)\hat{y}$; transmitted $\tau_\parallel E_0(\hat{x}\cos\theta_t - \hat{z}\sin\theta_t)$ and $(\tau_\parallel E_0/\eta_2)\hat{y}$), the tangential components are $E_x$ and $H_y$. Continuity of each at $z = 0$ gives

$$
(1 + \Gamma_\parallel)\cos\theta_i = \tau_\parallel\cos\theta_t, \qquad \frac{1 - \Gamma_\parallel}{\eta_1} = \frac{\tau_\parallel}{\eta_2} .
$$

The second gives $\tau_\parallel = (\eta_2/\eta_1)(1 - \Gamma_\parallel)$; substituting into the first, $\eta_1\cos\theta_i(1 + \Gamma_\parallel) = \eta_2\cos\theta_t(1 - \Gamma_\parallel)$, so

$$
\Gamma_\parallel = \frac{\eta_2\cos\theta_t - \eta_1\cos\theta_i}{\eta_2\cos\theta_t + \eta_1\cos\theta_i}, \qquad \tau_\parallel = (1 + \Gamma_\parallel)\frac{\cos\theta_i}{\cos\theta_t} .
$$

(b) Snell: $\sin\theta_t = \sin30^\circ/1.5$, so $\theta_t$ = **19.47**°. With $\eta_2 = \eta_1/1.5$, $\cos\theta_i$ = 0.8660 and $\cos\theta_t$ = 0.9428: $\Gamma_\parallel$ = **−0.1589**, $\tau_\parallel$ = **0.7726**, and the reflected power is $\Gamma_\parallel^2$ = **2.525**%.

(c) $T = 0.7726^2 \times 1.5 \times 0.9428/0.8660$ = **97.475**%, and $R + T$ = 2.525% + 97.475% = 100%: the extra factor accounts for the transmitted beam's different cross-section ($\cos\theta_t/\cos\theta_i$) and impedance. Note $\lvert\tau_\parallel\rvert^2$ alone (59.7%) is not the power fraction.

(d) $\Gamma_\perp = (\eta_2\cos\theta_i - \eta_1\cos\theta_t)/(\eta_2\cos\theta_i + \eta_1\cos\theta_t)$ = **−0.2404**, a reflectance of **5.78**%, more than twice the TM value: at 30° the TM reflection is already heading toward its zero at the Brewster angle (56.31°).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 13-06.1a | reflection coefficient | −0.3333 | — |
| 13-06.1b | transmission coefficient | 0.6667 | — |
| 13-06.1c | reflected power | 11.11 | % |
| 13-06.1d | transmitted power | 88.89 | % |
| 13-06.1e | standing-wave ratio | 2 | — |
| 13-06.2a | reflection coefficient | −0.8 | — |
| 13-06.2b | reflected power | 64 | % |
| 13-06.2c | standing-wave ratio | 9 | — |
| 13-06.3a | spacing of the zeros | 1.499 | cm |
| 13-06.3b | first maximum | 0.7495 | cm |
| 13-06.4a | critical angle | 48.75 | ° |
| 13-06.4b | angle in air | 41.68 | ° |
| 13-06.5a | transmission angle | 33.69 | ° |
| 13-06.5b | TE reflection coefficient | −0.3846 | — |
| 13-06.5c | TE reflected power | 14.79 | % |
| 13-06.6a | layer permittivity | 3 | — |
| 13-06.6b | layer thickness | 4.327 | mm |
| 13-06.7a | radome thickness | 7.495 | mm |
| 13-06.7b | reflectance at 11 GHz | 5.098 | % |
| 13-06.7c | reflectance at 12 GHz | 16.27 | % |
| 13-06.8a | numerical aperture | 0.1712 | — |
| 13-06.8b | acceptance half-angle | 9.856 | ° |
| 13-06.8c | critical angle | 83.31 | ° |
| 13-06.9a | real part of the impedance | 0.09935 | Ω |
| 13-06.9b | imaginary part of the impedance | 0.09935 | Ω |
| 13-06.9c | reflection coefficient (real part) | −0.9995 | — |
| 13-06.9d | transmitted power | 0.1054 | % |
| 13-06.9e | estimate | 0.1055 | % |
| 13-06.10a | absorption loss | 51.05 | dB |
| 13-06.10b | reflection loss | 105.9 | dB |
| 13-06.10c | shielding effectiveness | 157.0 | dB |
| 13-06.11a | reflection magnitude at 1.2 f0 | 0.1604 | — |
| 13-06.11b | in dB | −15.90 | dB |
| 13-06.11c | reflected power | 2.571 | % |
| 13-06.12a | decay constant | 3.361 | µm⁻¹ |
| 13-06.12b | 1/e distance | 297.5 | nm |
| 13-06.13a | TE transmission coefficient | 0.6967 | — |
| 13-06.13b | transmitted power fraction | 0.9080 | — |
| 13-06.13c | R + T | 1 | — |
| 13-06.14a | maximum field | 1.333 | V/m |
| 13-06.14b | minimum field | 0.6667 | V/m |
| 13-06.14c | distance to the nearest maximum | 7.495 | mm |
| 13-06.15a | transmission angle | 19.47 | ° |
| 13-06.15b | TM reflection coefficient | −0.1589 | — |
| 13-06.15c | TM transmission coefficient | 0.7726 | — |
| 13-06.15d | TM reflected power | 2.525 | % |
| 13-06.15e | TM transmitted power | 97.475 | % |
| 13-06.15f | TE reflection coefficient | −0.2404 | — |
| 13-06.15g | TE reflected power | 5.78 | % |
