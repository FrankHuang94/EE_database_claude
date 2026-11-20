# Solutions 13-11 · Radiation and Antenna Fundamentals

Problems: [13-11 problems](../problems/13-11-problems.md) · Chapter: [13-11](../chapters/13-11-radiation-and-antennas.md). Every number below is recomputed by [verify_13_11.py](../verify/verify_13_11.py), which integrates patterns numerically over the sphere and sums array element phasors directly.

---

## Solutions

### Solution 13-11.1

λ = $c/f$: **33.31** cm at 900 MHz (dipole **16.66** cm), **12.49** cm at 2.4 GHz (**6.246** cm), **1.071** cm at 28 GHz (**0.5353** cm). Practical dipoles are cut a few per cent shorter to make the input reactance zero.

### Solution 13-11.2

ℓ/λ = 0.01/2.998 = 3.336 × 10⁻³, so $R_{rad} = (2\pi\eta_0/3)(\ell/\lambda)^2$ = **8.779** mΩ: hopeless as a radiator unless its losses are far smaller still, which they will not be.

### Solution 13-11.3

$10\log_{10}100$ = **20** dBi. EIRP = 20 + 15 = **35** dBm = $10^{3.5}$ mW = **3.162** W.

### Solution 13-11.4

$2D_a^2/\lambda = 2 \times 1^2/0.02498$ = **80.06** m. Antenna ranges for large dishes are therefore long, or use compact ranges that create a plane wave artificially.

### Solution 13-11.5

$A_e = G\lambda^2/(4\pi) = 10^4 \times 0.02498^2/(4\pi)$ = **0.4967** m². The physical area is π(0.5)² = 0.7854 m², an aperture efficiency of **63.24**%, typical of a well-fed reflector.

### Solution 13-11.6

λ = 5.169 cm; FSPL = $20\log_{10}(4\pi \times 1000/0.05169)$ = **107.7** dB. $P_r$ = 30 + 20 + 20 − 107.7 = **−37.72** dBm.

### Solution 13-11.7

The allowed path loss is 20 + 2 + 2 − (−90) = 114 dB. Solving $20\log_{10}(4\pi R/\lambda)$ = 114 with λ = 12.49 cm gives $R$ = **4.982** km in free space (far less indoors).

### Solution 13-11.8

$e_r = 73.08/(73.08 + 2)$ = **97.34**%, so $G = e_rD = 0.9734 \times 1.641$ and $10\log_{10}G$ = **2.034** dBi. A resonant dipole tolerates a couple of ohms of loss easily, unlike Problem 13-11.2's tiny antenna.

### Solution 13-11.9

Broadside, $S = P_{rad}D/(4\pi r^2)$ with D = 1.5, and $E_{peak} = \sqrt{2\eta_0S}$ = **9.484** mV/m.

### Solution 13-11.10

$1/(kr)^2 = 1/(2\pi)^2$ = **0.02533** at $r = \lambda$, and **2.533** at $r = \lambda/10$. At 2 GHz, λ = 15 cm, so a head a centimetre or two from the antenna is at about λ/10: the reactive near field dominates, which is why exposure is assessed as SAR (absorbed power) rather than far-field power density (13-04).

### Solution 13-11.11

With ψ = π sin θ, the array factor $\sin(2\psi)/(4\sin(\psi/2))$ first vanishes at ψ = ±π/2, so sin θ = ±0.5 and the nulls are at **±30**°. Integrating $\lvert\text{AF}\rvert^2$ over the sphere (the array axis along a line, elements isotropic) gives a directivity of **4** (**6.021** dBi): for isotropic elements at λ/2 spacing the directivity equals $N$ exactly.

### Solution 13-11.12

(a) Main beam at sin θ₀ = sin 40° = 0.6428. Grating lobes sit where ψ differs by 2π, sin θ_g = sin θ₀ − λ/d = 0.6428 − 1.25 = −0.6072, which is a real angle: a grating lobe at **−37.39**°, as strong as the main beam. (b) $d < \lambda/(1 + \sin 60^\circ)$ = **0.5359**λ.

### Solution 13-11.13

The density limit gives 5 dBm + 10 log₁₀(bandwidth/1 MHz): **18.01** dBm at 20 MHz, **24.03** at 80 MHz, **27.04** at 160 MHz, and **30.05** dBm at 320 MHz, which the 30 dBm cap reduces to **30** dBm. Only the widest channel is limited by the total cap.

### Solution 13-11.14

Array gain $10\log_{10}64$ = **18.06** dB. Total power $64 \times 10$ mW = 640 mW = **28.06** dBm. EIRP = total power + array gain + element gain = 28.06 + 18.06 + 5 = **51.12** dBm. EIRP grows as $N^2$ because doubling the elements doubles the transmitted power and also doubles the array gain (the fields add coherently in the beam), a 6 dB gain per doubling, which is why millimetre-wave base stations use large arrays of modest amplifiers.

### Solution 13-11.15

(a) A perfect conductor forces tangential $E$ to zero on its surface. A vertical current element and its mirror image below the plane, carrying current in the same direction, produce a tangential $E$ that cancels on the plane, so above the plane the monopole and its image are indistinguishable from a full λ/2 dipole in free space (uniqueness: same sources above, same boundary condition). Below the plane there is no field.

(b) The fields above the plane are the dipole's, but they fill only the upper half-space, so the radiated power for the same feed current is half: $R_{rad}$ = 73.08/2 = **36.54** Ω. The same peak intensity spread over half the solid angle doubles the directivity: $D$ = 2 × 1.641 = **3.282**, or **5.161** dBi. (A real ground plane of finite size and conductivity gives less.)

### Solution 13-11.16

(a) $\lvert\hat{e}_t\cdot\hat{e}_r\rvert^2 = \cos^230^\circ$ = 0.75, a loss of **1.25** dB.

(b) A circular polarization vector is $(\hat{x} \pm j\hat{y})/\sqrt2$; against any linear $\hat{e} = \hat{x}\cos\psi + \hat{y}\sin\psi$ the product has magnitude squared $\tfrac12$, so the loss is **3.010** dB whatever the rotation. This is why handsets (with randomly oriented linear antennas) and satellites often use circular polarization at one end: the loss is a fixed 3 dB instead of a deep null at an unlucky angle.

(c) $\hat{e}_{RHCP}\cdot\hat{e}_{LHCP}^* = 0$: in theory no power is received at all. Real antennas have imperfect polarization, so the isolation is large but finite; it is used deliberately to separate two channels on one frequency.

### Solution 13-11.17

(a) The open-circuit voltage of a receiving antenna in a uniform field $E$ is $E$ times its effective length, $\ell_e = (1/I_0)\int I(z)\,dz$. For a triangle of base ℓ and height $I_0$ the integral is $I_0\ell/2$, so $V_{oc} = E\ell/2$.

(b) With $R_{rad} = \tfrac14(2\pi\eta/3)(\ell/\lambda)^2$, the matched power is $\lvert V_{oc}\rvert^2/(8R_{rad})$ and

$$
A_e = \frac{(E\ell/2)^2/(8R_{rad})}{E^2/(2\eta)} = \frac{\eta\ell^2}{16R_{rad}} = \frac{\eta\ell^2}{16}\cdot\frac{4 \times 3\lambda^2}{2\pi\eta\ell^2} = \frac{3\lambda^2}{8\pi} ,
$$

the same as with uniform current: the halved voltage (power down 4) is offset by the quartered resistance. At 2.4 GHz, λ = 12.49 cm and $A_e$ = **18.6** cm². Aperture is set by the pattern (directivity 1.5 in both cases), not by the current's amplitude profile, but efficiency compares $R_{rad}$ with the loss resistance, and a quarter of an already tiny $R_{rad}$ is much harder to beat.

### Solution 13-11.18

The power pattern relative to broadside is $F(\theta) = [\cos(\tfrac\pi2\cos\theta)/\sin\theta]^2$, which is 1 at θ = 90°. Setting $F(\theta) = \tfrac12$ and solving numerically (for example by bisection: $F(50°)$ = **0.4825** and $F(52°)$ = **0.5190**, so the root lies between) gives θ = **50.96**° from the axis, so the half-power beamwidth is $2(90° - 50.96°)$ = **78.08**°, a little narrower than the Hertzian dipole's 90°.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 13-11.1a | wavelength at 900 MHz | 33.31 | cm |
| 13-11.1b | dipole at 900 MHz | 16.66 | cm |
| 13-11.1c | wavelength at 2.4 GHz | 12.49 | cm |
| 13-11.1d | dipole at 2.4 GHz | 6.246 | cm |
| 13-11.1e | wavelength at 28 GHz | 1.071 | cm |
| 13-11.1f | dipole at 28 GHz | 0.5353 | cm |
| 13-11.2a | radiation resistance | 8.779 | mΩ |
| 13-11.3a | gain of 100 | 20 | dBi |
| 13-11.3b | EIRP | 35 | dBm |
| 13-11.3c | EIRP | 3.162 | W |
| 13-11.4a | far-field distance | 80.06 | m |
| 13-11.5a | effective aperture | 0.4967 | m² |
| 13-11.5b | aperture efficiency | 63.24 | % |
| 13-11.6a | free-space path loss | 107.7 | dB |
| 13-11.6b | received power | −37.72 | dBm |
| 13-11.7a | free-space range | 4.982 | km |
| 13-11.8a | radiation efficiency | 97.34 | % |
| 13-11.8b | gain | 2.034 | dBi |
| 13-11.9a | peak field at 1 km | 9.484 | mV/m |
| 13-11.10a | ratio at one wavelength | 0.02533 | — |
| 13-11.10b | ratio at a tenth of a wavelength | 2.533 | — |
| 13-11.11a | first null | 30 | ° |
| 13-11.11b | directivity | 4 | — |
| 13-11.11c | directivity in dBi | 6.021 | dBi |
| 13-11.12a | grating-lobe direction | −37.39 | ° |
| 13-11.12b | maximum spacing for ±60° | 0.5359 | λ |
| 13-11.13a | EIRP at 20 MHz | 18.01 | dBm |
| 13-11.13b | EIRP at 80 MHz | 24.03 | dBm |
| 13-11.13c | EIRP at 160 MHz | 27.04 | dBm |
| 13-11.13d | EIRP at 320 MHz | 30 | dBm |
| 13-11.13e | density limit at 320 MHz, before the cap | 30.05 | dBm |
| 13-11.14a | array gain | 18.06 | dB |
| 13-11.14b | total transmitted power | 28.06 | dBm |
| 13-11.14c | EIRP | 51.12 | dBm |
| 13-11.15a | monopole radiation resistance | 36.54 | Ω |
| 13-11.15b | monopole directivity | 3.282 | — |
| 13-11.15c | monopole directivity | 5.161 | dBi |
| 13-11.16a | loss at 30° rotation | 1.25 | dB |
| 13-11.16b | linear-to-circular loss | 3.010 | dB |
| 13-11.17a | effective aperture at 2.4 GHz | 18.6 | cm² |
| 13-11.18a | half-power angle from the axis | 50.96 | ° |
| 13-11.18b | half-power beamwidth | 78.08 | ° |
| 13-11.18c | pattern at 50° | 0.4825 | — |
| 13-11.18d | pattern at 52° | 0.5190 | — |
