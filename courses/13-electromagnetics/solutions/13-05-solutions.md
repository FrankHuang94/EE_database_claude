# Solutions 13-05 · Plane Waves in Lossless and Lossy Media

Problems: [13-05 problems](../problems/13-05-problems.md) · Chapter: [13-05](../chapters/13-05-plane-waves.md). Every number below is recomputed by [verify_13_05.py](../verify/verify_13_05.py), which uses complex arithmetic for γ and η, numerical solution of the field equations inside conductors, numerical integration of loss and energy, and a time trace of the field for polarization.

---

## Solutions

### Solution 13-05.1

$\beta = \omega\sqrt{\varepsilon_r}/c$ gives $\sqrt{\varepsilon_r} = 42c/(2\pi \times 10^9)$ = 2.004, so $\varepsilon_r$ = **4.016**. Then $\eta = \eta_0/\sqrt{\varepsilon_r}$ = **188.0** Ω. $\vec{H}$ has amplitude $5/\eta$ = **26.60** mA/m along $+\hat{y}$ (so that $\hat{x}\times\hat{y} = \hat{z}$ is the direction of travel), in phase with $\vec{E}$. $S_{av} = 5^2/(2\eta)$ = **66.49** mW/m² along $+z$.

### Solution 13-05.2

$\lambda = c/f$: **4997** km at 60 Hz (power lines are electrically short, except across continents), **12.49** cm at 2.4 GHz, **1.071** cm at 28 GHz (millimetre waves), and **1.550** µm at 193.4 THz, the infrared wavelength of long-haul optical fibre.

### Solution 13-05.3

(a) In phase, equal amplitudes: **linear** at 45° between $x$ and $y$.

(b) Equal amplitudes, $\phi$ = +90°: at $z$ = 0, $\vec{E} = \cos\omega t\,\hat{x} - \sin\omega t\,\hat{y}$, rotating from $x$ toward $-y$. With the left thumb along $+z$ the fingers curl that way: **left-hand circular**.

(c) $\vec{E} = \cos\omega t\,\hat{x} - 2\sin\omega t\,\hat{y}$: an ellipse with semi-axes 2 (along $y$) and 1 (along $x$), traced in the same sense as (b): **left-hand elliptical** with axial ratio **2**.

### Solution 13-05.4

$S = E_0^2/(2\eta_0)$ gives $E_0 = \sqrt{2\eta_0S}$ = **86.80** V/m peak, and $H_0 = E_0/\eta_0$ = **0.2304** A/m. With $\varepsilon_r$ = 81, $\eta = \eta_0/9$ = **41.86** Ω. (Real water is lossy at most frequencies; this is the lossless idealization.)

### Solution 13-05.5

$\delta = 1/\sqrt{\pi f\mu_0\sigma}$ at 1 GHz: aluminium **2.690** µm, gold **2.486** µm (copper is 2.090 µm). Aluminium's $R_s = 1/(\sigma\delta)$ = **10.62** mΩ, 29% above copper's 8.250 mΩ, since $R_s \propto 1/\sqrt\sigma$.

### Solution 13-05.6

Dividing the exact α (§3.3) by $\sqrt{\pi f\mu\sigma} = \omega\sqrt{\mu\varepsilon/2}\,\sqrt{x}$:

$$
\frac{\alpha}{\alpha_{gc}} = \sqrt{\frac{\sqrt{1 + x^2} - 1}{x}},
$$

a function of $x$ alone. It tends to $1 - 1/(2x)$ for large $x$, so the good-conductor value is too high by about $1/(2x)$. Setting the ratio to 0.99 and solving numerically: $x$ = **49.75**. For seawater, $x = \sigma/(2\pi f\varepsilon)$ ≥ 49.75 below **17.84** MHz.

### Solution 13-05.7

$\alpha = \pi f\sqrt{\varepsilon_r}\tan\delta/c = \pi \times 10^9 \times 1.5 \times 0.0002/(2.998 \times 10^8)$ = **3.144 × 10⁻³** Np/m = **0.02731** dB/m.

### Solution 13-05.8

$R_{dc} = \ell/(\sigma wt) = 0.1/(5.8 \times 10^7 \times 10^{-4} \times 35 \times 10^{-6})$ = **0.4926** Ω. At 1 GHz, δ = 2.090 µm ≪ 35 µm, and with current on both faces the conducting width is $2w$: $R_{ac} = R_s\ell/(2w) = 8.250\ \text{mΩ} \times 0.1/(2 \times 10^{-4})$ = **4.125** Ω, **8.374** times the DC value. (In a real microstrip most of the current crowds onto the face nearest the ground plane and the edges, so the true value is higher still; field solvers handle that.)

### Solution 13-05.9

At 10 kHz, δ = 2.516 m, so α = 8.686/δ = **3.452** dB/m. 100 dB is lost at **28.97** m. At 100 Hz δ is 10 times larger, and the 100 dB depth is **289.7** m. Lower frequencies reach deeper, at the price of tiny bandwidth and enormous antennas.

### Solution 13-05.10

With ω = 2π × 10⁹ rad/s, $\sigma + j\omega\varepsilon$ = 4 + j4.506 S/m. Then

$$
\gamma = \sqrt{j\omega\mu_0(4 + j4.506)} = 77.44 + j203.9\ \text{m}^{-1}, \qquad
\eta_c = \sqrt{\frac{j\omega\mu_0}{4 + j4.506}} = 33.84 + j12.85\ \Omega .
$$

So α = **77.44** Np/m, β = **203.9** rad/m, $\lvert\eta_c\rvert$ = **36.20** Ω at **20.80**°. Neither approximation holds: the low-loss formula would need $\sigma/\omega\varepsilon \ll 1$ and the good-conductor one $\gg 1$, while here the ratio is 0.888.

### Solution 13-05.11

(a) $\int_0^\infty J_0e^{-(1 + j)z/\delta}dz = J_0\delta/(1 + j)$. The surface current per width equals the tangential $H$ just outside (the field inside decays to zero), so $\lvert H_t\rvert = \lvert J_0\rvert\delta/\sqrt2$. The loss per area is

$$
P' = \int_0^\infty\frac{\lvert J_0\rvert^2e^{-2z/\delta}}{2\sigma}dz = \frac{\lvert J_0\rvert^2\delta}{4\sigma} = \frac{1}{2}\,\frac{1}{\sigma\delta}\,\frac{\lvert J_0\rvert^2\delta^2}{2} = \frac12R_s\lvert H_t\rvert^2 .
$$

(b) $\tfrac12 \times 8.250\ \text{mΩ} \times 1^2$ = **4.125** mW/m².

### Solution 13-05.12

With $H = E/\eta$ and $\eta = \sqrt{\mu/\varepsilon}$: $\tfrac12\mu H^2 = \tfrac12\mu E^2\varepsilon/\mu = \tfrac12\varepsilon E^2$, so the two are equal at every instant. The total time-average energy density is $u = 2 \times \tfrac14\varepsilon E_0^2 = \tfrac12\varepsilon E_0^2$, and $u\,v_p = \tfrac12\varepsilon E_0^2/\sqrt{\mu\varepsilon} = E_0^2/(2\eta) = S_{av}$. For 10 W/m² in air, $u = S/c$ = **3.336 × 10⁻⁸** J/m³.

### Solution 13-05.13

$R_s$ = 8.250 mΩ at 1 GHz, so $R' = (8.250 \times 10^{-3}/2\pi)(2000 + 571.4)$ = **3.376** Ω/m. Then $\alpha_c = R'/(2Z_0)$ = 0.03371 Np/m = **0.2928** dB/m. The dielectric adds $\alpha_d$ = **0.02731** dB/m (Problem 13-05.7), for a total of **0.3201** dB/m. Conductor loss is more than ten times dielectric loss here: with a low-loss dielectric, coax loss is mostly copper, and most of that is on the small inner conductor (the $1/a$ term).

### Solution 13-05.14

Resolve the field along the ellipse's axes: the components have amplitudes 2 and 1 (in units of the minor semi-axis) and are 90° apart in time, so their powers add, in the proportion 4 : 1. A linear antenna along the major axis captures 4/5 = **0.8** of the power (**−0.9691** dB); along the minor axis, 1/5 (**−6.990** dB). Circular polarization (axial ratio 1) is the case where the two are equal at −3 dB.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 13-05.1a | relative permittivity | 4.016 | — |
| 13-05.1b | intrinsic impedance | 188.0 | Ω |
| 13-05.1c | H amplitude | 26.60 | mA/m |
| 13-05.1d | power density | 66.49 | mW/m² |
| 13-05.2a | wavelength at 60 Hz | 4997 | km |
| 13-05.2b | wavelength at 2.4 GHz | 12.49 | cm |
| 13-05.2c | wavelength at 28 GHz | 1.071 | cm |
| 13-05.2d | wavelength at 193.4 THz | 1.550 | µm |
| 13-05.3a | axial ratio in (c) | 2 | — |
| 13-05.4a | peak E | 86.80 | V/m |
| 13-05.4b | peak H | 0.2304 | A/m |
| 13-05.4c | impedance with εr = 81 | 41.86 | Ω |
| 13-05.5a | aluminium skin depth | 2.690 | µm |
| 13-05.5b | gold skin depth | 2.486 | µm |
| 13-05.5c | aluminium surface resistance | 10.62 | mΩ |
| 13-05.6a | σ/ωε for 1% error | 49.75 | — |
| 13-05.6b | seawater frequency limit | 17.84 | MHz |
| 13-05.7a | dielectric attenuation | 3.144 × 10⁻³ | Np/m |
| 13-05.7b | dielectric attenuation | 0.02731 | dB/m |
| 13-05.8a | DC resistance | 0.4926 | Ω |
| 13-05.8b | AC resistance at 1 GHz | 4.125 | Ω |
| 13-05.8c | ratio | 8.374 | — |
| 13-05.9a | attenuation at 10 kHz | 3.452 | dB/m |
| 13-05.9b | depth for 100 dB at 10 kHz | 28.97 | m |
| 13-05.9c | depth for 100 dB at 100 Hz | 289.7 | m |
| 13-05.10a | attenuation constant | 77.44 | Np/m |
| 13-05.10b | phase constant | 203.9 | rad/m |
| 13-05.10c | impedance magnitude | 36.20 | Ω |
| 13-05.10d | impedance angle | 20.80 | ° |
| 13-05.11a | loss per area | 4.125 | mW/m² |
| 13-05.12a | energy density | 3.336 × 10⁻⁸ | J/m³ |
| 13-05.13a | resistance per metre | 3.376 | Ω/m |
| 13-05.13b | conductor attenuation | 0.2928 | dB/m |
| 13-05.13c | dielectric attenuation | 0.02731 | dB/m |
| 13-05.13d | total attenuation | 0.3201 | dB/m |
| 13-05.14a | best-orientation fraction | 0.8 | — |
| 13-05.14b | best orientation | −0.9691 | dB |
| 13-05.14c | worst orientation | −6.990 | dB |
