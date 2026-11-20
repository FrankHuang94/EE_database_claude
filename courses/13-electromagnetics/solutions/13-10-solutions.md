# Solutions 13-10 · Waveguides and Resonators

Problems: [13-10 problems](../problems/13-10-problems.md) · Chapter: [13-10](../chapters/13-10-waveguides-and-resonators.md). Every number below is recomputed by [verify_13_10.py](../verify/verify_13_10.py), which solves the guide's eigenproblem on a finite-difference grid, integrates wall losses and stored energy numerically from the mode fields, and solves the fibre's radial wave equation numerically as well as by the Bessel-function condition.

---

## Solutions

### Solution 13-10.1

$f_c = c/(2a) = 2.998 \times 10^8/(2 \times 0.072136)$ = **2.078** GHz. (WR-284's recommended band, about 2.6 to 3.95 GHz, is S band.)

### Solution 13-10.2

$\lambda_g = \lambda/\sqrt{1 - (f_c/f)^2}$ with λ = 2.498 cm and $f_c/f$ = 0.5464: $\lambda_g$ = **2.983** cm. $Z_{TE} = \eta_0/\sqrt{1 - (f_c/f)^2}$ = **449.8** Ω, closer to 377 Ω than at 10 GHz (499 Ω) because the frequency is further above cutoff.

### Solution 13-10.3

$f_c = c/(2a\sqrt{\varepsilon_r})$ = 6.557/1.5 = **4.371** GHz. Filling a guide lowers its cutoff by $\sqrt{\varepsilon_r}$, a way to make a smaller guide for a given band (at the cost of dielectric loss).

### Solution 13-10.4

The delay is $L/v_g$ with $v_g = c\sqrt{1 - (f_c/f)^2}$: **4.870** ns at 9 GHz and **4.154** ns at 11 GHz, a difference of **0.7153** ns. A short pulse containing both frequencies spreads by most of a nanosecond over just 1 m; waveguide runs are kept short or the dispersion is equalized for wideband signals.

### Solution 13-10.5

$k_c = \pi/0.003$ = 1047 rad/m and $k$ = 51.3 rad/m, so $\alpha = \sqrt{k_c^2 - k^2}$ = **1046** Np/m, and through 1 mm the attenuation is **9.085** dB. The real screen does much better because each hole is tiny compared with the 12.2 cm wavelength: a small aperture couples very weakly to the field outside it (its transmission scales roughly as the cube of its size in wavelengths), and the below-cutoff decay comes on top of that.

### Solution 13-10.6

$f_{101} = (c/2)\sqrt{(1/a)^2 + (1/d)^2}$ with $a = d$ = 5 cm: **4.240** GHz. In a cube the three axes are equivalent, so TE₀₁₁ and TM₁₁₀ resonate at the same frequency: the modes are **degenerate**, which designers break by making the sides unequal.

### Solution 13-10.7

At 4.240 GHz, $R_s = \sqrt{\pi f\mu_0/\sigma}$ = **16.99** mΩ. With $a = b = d$ = 5 cm the TE₁₀₁ Q formula gives $Q_c$ = **1.642 × 10⁴**. The larger cavity (in wavelengths and in volume per surface) has twice the Q of the X-band cavity.

### Solution 13-10.8

Minimizing $\alpha_c(f)$ numerically gives a minimum at **15.39** GHz, where $\alpha_c$ = **0.09428** dB/m. That is above the TE₂₀ cutoff (13.11 GHz), so outside the single-mode band: within the usable band the attenuation falls steadily with frequency, which is one reason the band starts well above cutoff.

### Solution 13-10.9

$V = (2\pi \times 25\ \mu\text{m}/0.85\ \mu\text{m}) \times 0.2$ = **36.96**, so about $V^2/2$ = **683** modes. Such multimode fibre is easy to couple to (large core, many modes) but suffers modal dispersion, which limits it to short links.

### Solution 13-10.10

$V < 2.405$ at λ = 1.26 µm requires $a < 2.405\lambda/(2\pi\,\text{NA})$ = **4.019** µm.

### Solution 13-10.11

The TE₁₀ transverse field is $E_y = E_0\sin(\pi x/a)$ and $H_x = -E_y/Z_{TE}$. The power is

$$
P = \frac{1}{2Z_{TE}}\int_0^b\!\!\int_0^aE_0^2\sin^2\frac{\pi x}{a}\,dx\,dy = \frac{E_0^2ab}{4Z_{TE}} .
$$

With $E_0$ = 3 MV/m and $Z_{TE}$ = 499.0 Ω at 10 GHz: $P$ = **1.047** MW. (In practice a safety factor of several is applied, and pressurized or gas-filled guides are used for radar transmitters.)

### Solution 13-10.12

$Z_{TE} = 376.7/\sqrt{1 - (6.557/7)^2}$ = **1076** Ω. Close to cutoff the impedance and attenuation rise steeply and change rapidly with frequency (and with small dimensional tolerances), and the group velocity, hence dispersion, becomes extreme.

### Solution 13-10.13

At critical coupling the external loss equals the internal loss, so $1/Q_L = 1/Q_0 + 1/Q_e = 2/Q_0$: $Q_L$ = 3919 and the bandwidth doubles to $f_0/Q_L$ = **2.366** MHz. Maximum power transfer into the cavity comes with half the unloaded Q.

### Solution 13-10.14

With $u$ = 1.618 and $w = \sqrt{V^2 - u^2}$ = 1.627, the intensity is $J_0^2(u\rho/a)$ in the core and $K_0^2(w\rho/a)$ (scaled for continuity) outside. Integrating $\int I\rho\,d\rho$ numerically over the core and over all space, the core holds **80.82**% of the power; the remaining fifth travels in the cladding.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 13-10.1a | WR-284 TE10 cutoff | 2.078 | GHz |
| 13-10.2a | guide wavelength at 12 GHz | 2.983 | cm |
| 13-10.2b | wave impedance at 12 GHz | 449.8 | Ω |
| 13-10.3a | filled cutoff | 4.371 | GHz |
| 13-10.4a | delay at 9 GHz | 4.870 | ns |
| 13-10.4b | delay at 11 GHz | 4.154 | ns |
| 13-10.4c | difference | 0.7153 | ns |
| 13-10.5a | attenuation constant | 1046 | Np/m |
| 13-10.5b | attenuation through 1 mm | 9.085 | dB |
| 13-10.6a | cube TE101 resonance | 4.240 | GHz |
| 13-10.7a | surface resistance | 16.99 | mΩ |
| 13-10.7b | conductor Q | 1.642 × 10⁴ | — |
| 13-10.8a | frequency of minimum loss | 15.39 | GHz |
| 13-10.8b | minimum attenuation | 0.09428 | dB/m |
| 13-10.9a | V-number | 36.96 | — |
| 13-10.9b | approximate number of modes | 683 | — |
| 13-10.10a | largest core radius | 4.019 | µm |
| 13-10.11a | maximum power | 1.047 | MW |
| 13-10.12a | wave impedance at 7 GHz | 1076 | Ω |
| 13-10.13a | loaded bandwidth | 2.366 | MHz |
| 13-10.14a | power fraction in the core | 80.82 | % |
