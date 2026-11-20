<!-- status: verified -->
# 13-05 · Plane Waves in Lossless and Lossy Media

| | |
|---|---|
| **Course** | [13 · Electromagnetics](../README.md) |
| **University equivalent** | The plane-wave chapter of a junior electromagnetics course: the wave equation and its travelling solutions, uniform plane waves and intrinsic impedance, polarization, propagation in lossy dielectrics and good conductors, the skin effect and surface resistance (Ulaby & Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 7; Cheng, *Field and Wave Electromagnetics*, ch. 8; Pozar, *Microwave Engineering*, ch. 1) |
| **Prerequisites** | [13-04 Maxwell's Equations and Time-Varying Fields](13-04-maxwells-equations.md), [04-09 Waves and Optics Basics](../../04-physics-for-ee/chapters/04-09-waves-and-optics.md), [02-01 Complex Numbers, Euler and Phasors](../../02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md) |
| **Estimated study hours** | 10 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Derive the uniform plane wave from Maxwell's equations, and compute its wavelength, phase velocity, intrinsic impedance and power density in any lossless medium.
2. Classify a wave's polarization (linear, circular, elliptical, and the hand of rotation) from its phasor, and compute polarization mismatch.
3. Compute the propagation constant and intrinsic impedance of a lossy medium exactly, and with the low-loss and good-conductor approximations, knowing when each applies.
4. Compute skin depth, surface resistance and the AC resistance of conductors.
5. Estimate the attenuation of signals in board laminates, cables and seawater, and separate conductor loss from dielectric loss.

---

## 1. Big picture

Far from any source, every radiated wave looks locally like a **plane wave**: fields uniform across a flat front, moving at a fixed speed, with $\vec{E}$, $\vec{H}$ and the direction of travel mutually perpendicular. The plane wave is to electromagnetics what the sinusoid is to circuits: the simplest solution, the building block for everything else, and the model behind every link budget. The same equations, with conductivity added, describe how waves die out in lossy materials, and in metals they become the skin effect, which sets the high-frequency resistance of every wire, trace and cable.

- **Wireless links** use the plane-wave power density $E^2/2\eta$ at the receiver (13-11, Course 17).
- **The skin effect** makes a conductor's resistance grow as $\sqrt{f}$: the dominant loss in cables, package traces and on-chip inductors at gigahertz frequencies.
- **Dielectric loss** grows as $f$ and dominates long board traces at tens of gigahertz, which drives the choice of laminate for AI-server and switch boards (§9).
- **Polarization** decides how much power an antenna captures; mismatched polarization costs decibels in every satellite, phone and radar link.

## 2. Intuition first

**A travelling pattern.** In a plane wave, a pattern of electric and magnetic field slides along at the speed of light in the medium. At any instant, $\vec{E}$ and $\vec{H}$ are perpendicular to each other and to the direction of travel, in phase, with a fixed ratio $E/H = \eta$, a property of the medium measured in ohms. Freeze time and you see a sinusoidal pattern of wavelength λ; watch one point and you see the fields oscillate at frequency $f$; together they move at $v = f\lambda$.

**Loss as friction, and why metals are shallow.** In a lossy medium the moving charges convert some of the wave's energy into heat each cycle, so the amplitude decays exponentially with distance. In a good conductor the decay is so fast that the field barely gets in: at 1 GHz the field in copper falls by $e$ (to 37%) in about 2 µm. That **skin depth** is why a solid wire, a hollow tube and a plated plastic part all have the same high-frequency resistance.

**An analogy from finance, and its limits.** Attenuation is compounding in reverse: a fixed fraction of the remaining amplitude is lost per metre, so the loss in decibels adds linearly with distance, just as continuously compounded returns add in log space. The analogy fails in two places. The "rate" itself depends on frequency (as $\sqrt{f}$ for conductors and $f$ for dielectrics), so a broadband signal is distorted, not just shrunk. And a wave also carries phase, which accumulates at a different rate from the decay; in a good conductor the two rates happen to be equal.

## 3. Theory

> **Conventions.** Phasor fields $\tilde{\vec{E}}$, $\tilde{\vec{H}}$ with peak amplitudes and time dependence $e^{j\omega t}$; $\varepsilon = \varepsilon_r\varepsilon_0$, $\mu = \mu_r\mu_0$; conductivity σ. The propagation constant is $\gamma = \alpha + j\beta$ (attenuation α in Np/m, phase constant β in rad/m), and a wave travelling in $+z$ varies as $e^{-\gamma z}$. 1 Np = 8.686 dB. $\eta$ is the intrinsic impedance of a medium and $\eta_0$ = 376.7 Ω that of free space. Copper: σ = 5.8 × 10⁷ S/m (100% IACS at 20 °C [1]).

### 3.1 The uniform plane wave

13-04 derived the Helmholtz equation $\nabla^2\tilde{\vec{E}} + k^2\tilde{\vec{E}} = 0$, $k = \omega\sqrt{\mu\varepsilon}$, for a source-free, lossless, uniform region. Look for a field that points along $x$ and depends only on $z$, uniform over every plane $z$ = constant:

$$
\frac{d^2\tilde E_x}{dz^2} + k^2\tilde E_x = 0 \quad\Rightarrow\quad \tilde E_x(z) = E_0^+e^{-jkz} + E_0^-e^{+jkz} .
$$

In the time domain the first term is $\lvert E_0^+\rvert\cos(\omega t - kz + \phi)$, a pattern that moves toward $+z$: a point of constant phase obeys $\omega t - kz$ = constant, so it moves at the **phase velocity**

$$
v_p = \frac{\omega}{k} = \frac{1}{\sqrt{\mu\varepsilon}} = \frac{c}{\sqrt{\mu_r\varepsilon_r}}, \qquad \lambda = \frac{2\pi}{k} = \frac{v_p}{f} .
$$

The second term moves toward $-z$. Take the forward wave alone. Faraday's law, $\nabla\times\tilde{\vec{E}} = -j\omega\mu\tilde{\vec{H}}$, gives $\hat{y}\,d\tilde E_x/dz = -jkE_0^+e^{-jkz}\hat{y} = -j\omega\mu\tilde{\vec{H}}$, so

$$
\tilde{\vec{H}} = \frac{E_0^+}{\eta}e^{-jkz}\,\hat{y}, \qquad \eta = \frac{\omega\mu}{k} = \sqrt{\frac{\mu}{\varepsilon}} .
$$

Three facts follow, and they hold for every uniform plane wave in a lossless medium:

- $\vec{E}$, $\vec{H}$ and the direction of travel $\hat{k}$ are mutually perpendicular (a **TEM** wave, transverse electromagnetic), with $\tilde{\vec{H}} = \hat{k}\times\tilde{\vec{E}}/\eta$.
- $\vec{E}$ and $\vec{H}$ are in phase, and their ratio is the **intrinsic impedance** η: 376.7 Ω in free space ($\approx 120\pi$), and $\eta_0/\sqrt{\varepsilon_r}$ in a nonmagnetic dielectric.
- The time-average power density is $\vec{S}_{av} = \tfrac12\text{Re}\{\tilde{\vec{E}}\times\tilde{\vec{H}}^*\} = \dfrac{\lvert E_0\rvert^2}{2\eta}\hat{k}$.

The electric and magnetic energy densities are equal ($\tfrac12\varepsilon E^2 = \tfrac12\mu H^2$ when $E = \eta H$), and the power density equals the total energy density times $v_p$ (Problem 13-05.12).

> **Going deeper — why "plane" is an idealization.** A uniform plane wave has infinite extent and infinite total power, so no source makes one exactly. But the field of any finite source, observed far enough away and over a small enough region, has a nearly flat front: a spherical wave of radius $r$ deviates from its tangent plane by $d^2/(8r)$ across a width $d$, which is a negligible fraction of a wavelength when $r \gg d^2/\lambda$. That is the far-field condition antennas use (13-11).

### 3.2 Polarization

The **polarization** of a wave is the figure traced by the tip of $\vec{E}$ at a fixed point over one cycle. For a wave travelling in $+z$, write the general transverse field as

$$
\tilde{\vec{E}} = (E_x\hat{x} + E_ye^{j\phi}\hat{y})\,e^{-jkz}, \qquad E_x, E_y \ge 0 .
$$

At $z$ = 0 the field is $\vec{E}(t) = E_x\cos\omega t\,\hat{x} + E_y\cos(\omega t + \phi)\,\hat{y}$.

- **Linear** when $\phi$ = 0 or 180°: the tip moves back and forth along a line at angle $\arctan(E_y/E_x)$ (or its mirror image) from $x$.
- **Circular** when $E_x = E_y$ and $\phi = \pm 90°$: the tip traces a circle at constant magnitude.
- **Elliptical** otherwise. The **axial ratio** is the ratio of the ellipse's major to minor axis: 1 for circular, infinite for linear.

**Which hand?** The IEEE convention: point your right thumb along the direction of travel; if the fingers curl the way $\vec{E}$ rotates in time, the wave is **right-hand** polarized. For $\phi$ = −90° (that is, $\tilde{\vec{E}} \propto \hat{x} - j\hat{y}$), $\vec{E}(t) = E_0(\cos\omega t\,\hat{x} + \sin\omega t\,\hat{y})$ rotates from $x$ toward $y$, counterclockwise when seen from $+z$ looking back at the source: right-hand circular for a wave going in $+z$. $\hat{x} + j\hat{y}$ is left-hand.

**Polarization mismatch.** A receiving antenna responds only to the component of $\vec{E}$ along its own polarization. A linearly polarized antenna at angle ψ to a linearly polarized wave captures a fraction $\cos^2\psi$ of the power; a linear antenna receiving a circular wave captures exactly half (−3.010 dB) at any orientation; a circular antenna of the opposite hand ideally captures nothing. Satellite links use circular polarization so that the receiver's orientation does not matter and so that the rotation of linear polarization in the ionosphere (Faraday rotation) does not cause fading.

### 3.3 Lossy media: the propagation constant

With conductivity, Ampère–Maxwell becomes $\nabla\times\tilde{\vec{H}} = (\sigma + j\omega\varepsilon)\tilde{\vec{E}}$, and the same steps as §3.1 give $d^2\tilde E_x/dz^2 = \gamma^2\tilde E_x$ with

$$
\gamma = \alpha + j\beta = \sqrt{j\omega\mu(\sigma + j\omega\varepsilon)}, \qquad \eta_c = \sqrt{\frac{j\omega\mu}{\sigma + j\omega\varepsilon}} .
$$

The forward wave is $\tilde E_x = E_0e^{-\alpha z}e^{-j\beta z}$: its amplitude decays as $e^{-\alpha z}$ while its phase advances at β per metre. The intrinsic impedance is now complex, so $\vec{H}$ lags $\vec{E}$. Squaring and separating real and imaginary parts of $\gamma^2 = -\omega^2\mu\varepsilon + j\omega\mu\sigma$ gives $\alpha^2 - \beta^2 = -\omega^2\mu\varepsilon$ and $2\alpha\beta = \omega\mu\sigma$, whose solution is

$$
\begin{aligned}
\alpha &= \omega\sqrt{\frac{\mu\varepsilon}{2}}\left[\sqrt{1 + \Big(\frac{\sigma}{\omega\varepsilon}\Big)^2} - 1\right]^{1/2}, \\
\beta &= \omega\sqrt{\frac{\mu\varepsilon}{2}}\left[\sqrt{1 + \Big(\frac{\sigma}{\omega\varepsilon}\Big)^2} + 1\right]^{1/2} .
\end{aligned}
$$

Everything depends on the ratio $\sigma/\omega\varepsilon$ from 13-04, and two limits cover most engineering.

**Low-loss dielectric** ($\sigma/\omega\varepsilon \ll 1$). Expanding the square root, $\beta \approx \omega\sqrt{\mu\varepsilon}$ (as if lossless), $\eta_c \approx \sqrt{\mu/\varepsilon}$, and

$$
\alpha \approx \frac{\sigma}{2}\sqrt{\frac{\mu}{\varepsilon}} = \frac{\beta\tan\delta}{2} = \frac{\pi f\sqrt{\varepsilon_r}\tan\delta}{c} \quad\text{(nonmagnetic)},
$$

using $\sigma_{eff} = \omega\varepsilon\tan\delta$ (13-04). At constant loss tangent the attenuation grows in proportion to frequency.

**Good conductor** ($\sigma/\omega\varepsilon \gg 1$). Now $\gamma \approx \sqrt{j\omega\mu\sigma} = (1 + j)\sqrt{\pi f\mu\sigma}$, so

$$
\alpha = \beta = \frac{1}{\delta}, \qquad \delta = \frac{1}{\sqrt{\pi f\mu\sigma}}, \qquad \eta_c = (1 + j)\sqrt{\frac{\pi f\mu}{\sigma}} = \frac{1 + j}{\sigma\delta} .
$$

The **skin depth** δ is the distance over which the field falls by $e$ (8.686 dB). In copper it is 8.5 mm at 60 Hz, 66 µm at 1 MHz and 2.1 µm at 1 GHz (Example 13-05.3). Because $\alpha = \beta$, the field also turns through one radian of phase per skin depth, and the wavelength inside the metal is $2\pi\delta$: a wave in copper at 1 GHz travels about 13 µm per cycle, at a phase velocity of $\omega\delta$ = 13 km/s, against 3 × 10⁸ m/s outside. The intrinsic impedance is tiny (milliohms) with a 45° angle, so a conductor presents almost a short circuit to an arriving wave, which is why metals reflect (13-06).

![Log-log plot of skin depth against frequency from 10 Hz to 100 GHz for copper and aluminium, falling as one over the square root of frequency through 8.5 mm at 60 Hz, 66 µm at 1 MHz and 2.1 µm at 1 GHz for copper, with copper's surface resistance rising as the square root of frequency on the right axis](../../../assets/figures/13-05/skin-depth.svg)

*Figure 1. Skin depth of copper and aluminium, and copper's surface resistance, against frequency. Every decade of frequency divides the skin depth by √10 and multiplies the surface resistance by √10; aluminium's lower conductivity gives a skin depth 29% larger and a surface resistance 29% higher than copper's.*

> **Math refresher — square roots of complex numbers.** $\sqrt{j} = e^{j\pi/4} = (1 + j)/\sqrt2$, so $\sqrt{j\omega\mu\sigma} = (1 + j)\sqrt{\omega\mu\sigma/2}$. In general take $\sqrt{re^{j\theta}} = \sqrt r\,e^{j\theta/2}$ with $-\pi < \theta \le \pi$, which puts the result in the right half-plane, so that α ≥ 0 and the wave decays in its direction of travel (02-01).

### 3.4 The skin effect and surface resistance

Inside a good conductor occupying $z > 0$, the current density follows the field: $\tilde J(z) = \sigma\tilde E(z) = J_0e^{-(1 + j)z/\delta}$. The total current per unit width is

$$
\int_0^\infty J_0e^{-(1 + j)z/\delta}\,dz = \frac{J_0\delta}{1 + j} .
$$

Its magnitude is $J_0\delta/\sqrt2$, and the power dissipated per unit area, $\int\tfrac12\lvert J\rvert^2/\sigma\,dz = \lvert J_0\rvert^2\delta/(4\sigma)$, is exactly what a *uniform* current of the same total, flowing in a layer of thickness δ, would dissipate. So for loss calculations a conductor at high frequency behaves like a sheet one skin depth thick with the DC conductivity, whose resistance per square is the **surface resistance**

$$
R_s = \frac{1}{\sigma\delta} = \sqrt{\frac{\pi f\mu}{\sigma}} = \text{Re}\{\eta_c\} \quad(\Omega\text{ per square}).
$$

For copper at 1 GHz, $R_s$ = 8.250 mΩ. Since the tangential $H$ at the surface equals the surface current per width (13-03's boundary condition, with the field inside decaying to zero), the loss per unit area is $\tfrac12R_s\lvert H_t\rvert^2$. This is how conductor losses are computed in every cavity, waveguide and transmission line (13-08, 13-10).

**A round wire.** When $\delta \ll a$, the current flows in a ring of circumference $2\pi a$ and effective thickness δ, so the AC resistance per length is

$$
R'_{ac} \approx \frac{R_s}{2\pi a} = \frac{1}{2\pi a\sigma\delta}, \qquad \frac{R'_{ac}}{R'_{dc}} = \frac{\pi a^2}{2\pi a\delta} = \frac{a}{2\delta} .
$$

A 1 mm diameter copper wire at 100 MHz has 38 times its DC resistance (Example 13-05.4). The exact solution, using Bessel functions, is in the lab: the ratio is closer to $a/(2\delta) + \tfrac14$, so the simple form is low by about $\delta/(2a)$, within 5% once $a > 10\delta$. Remedies are to increase surface area (wide flat conductors, plating, the many insulated strands of Litz wire for switching-converter magnetics), not cross-section.

### 3.5 Dispersion and group velocity

In a lossless dielectric with constant ε, every frequency travels at the same speed, and a pulse keeps its shape. When β is not proportional to ω, as in conductors, plasmas, waveguides (13-10) and real dielectrics whose ε varies with frequency, different frequency components travel at different phase velocities and a pulse spreads: **dispersion**. A narrowband signal's envelope then moves at the **group velocity**

$$
v_g = \frac{d\omega}{d\beta} ,
$$

which is the speed at which energy and information travel. In a good conductor, $\beta = \sqrt{\omega\mu\sigma/2}$, so $v_g = 2\omega\delta$: twice the phase velocity. For digital links the practical consequence is that a lossy line attenuates high frequencies more than low ones (conductor loss ∝ $\sqrt f$, dielectric ∝ $f$), smearing edges into inter-symbol interference, which equalizers then undo (Course 24).

## 4. Worked examples

### Example 13-05.1 · A Wi-Fi wave in air and in a dielectric (tier A)

**Setup.** A 2.4 GHz plane wave has a peak electric field of 1 V/m in air. Find λ, $k$, the peak $H$ and the power density. Then find λ, η and $v_p$ in a lossless nonmagnetic dielectric with $\varepsilon_r$ = 4.

**Solution.** In air $\lambda = c/f$ = **12.49** cm and $k = 2\pi/\lambda$ = **50.30** rad/m. $H = E/\eta_0$ = **2.654** mA/m and $S = E^2/(2\eta_0)$ = **1.327** mW/m². In the dielectric, $\sqrt{\varepsilon_r}$ = 2 halves the speed and the wavelength and the impedance: λ = **6.246** cm, η = **188.4** Ω, $v_p$ = **1.499 × 10⁸** m/s.

**Units check.** (V/m)/Ω = A/m; (V/m)²/Ω = W/m².

**Sanity check.** The 12.5 cm wavelength sets the size of a Wi-Fi antenna (a half-wave dipole is about half of it); in a dielectric the wavelength, and so the antenna, shrinks, which is why compact antennas are often loaded with ceramics.

### Example 13-05.2 · Polarization and mismatch (tier A)

**Setup.** (a) Classify $\tilde{\vec{E}} = (3\hat{x} + 4\hat{y})e^{-jkz}$ and $\tilde{\vec{E}} = E_0(\hat{x} - j\hat{y})e^{-jkz}$. (b) A linearly polarized antenna receives the second wave. What fraction of the available power does it capture, in dB?

**Solution.** (a) The first has $\phi$ = 0: **linear**, at $\arctan(4/3)$ = **53.13**° from $x$. The second has equal amplitudes and $\phi$ = −90°: **circular**, and by §3.2, **right-hand** for travel in $+z$. (b) Whatever its orientation, a linear antenna picks out one component of the rotating field, half the power: $10\log_{10}0.5$ = **−3.010** dB.

**Sanity check.** Rotating the linear antenna changes only which instant of the cycle it "sees" the peak, not the time-average power: the circular wave has the same amplitude in every direction.

### Example 13-05.3 · Skin depth in copper (tier B)

**Setup.** Find the skin depth of copper at 60 Hz, 1 MHz, 1 GHz and 10 GHz, and its surface resistance at 1 GHz.

**Solution.** $\delta = 1/\sqrt{\pi f\mu_0\sigma}$ with σ = 5.8 × 10⁷ S/m: **8.532** mm at 60 Hz, **66.09** µm at 1 MHz, **2.090** µm at 1 GHz and **0.6609** µm at 10 GHz. At 1 GHz, $R_s = 1/(\sigma\delta)$ = **8.250** mΩ per square.

**Units check.** $[\text{s}^{-1}\,\text{H/m}\,\text{S/m}]^{-1/2}$ = $[\text{(Ω·s)/m} \cdot \text{1/(Ω·m)} \cdot \text{s}^{-1}]^{-1/2}$ = m.

**Sanity check.** δ scales as $1/\sqrt f$: each factor of 100 in frequency divides it by 10, as the 1 MHz and 10 GHz values show (a factor of 10⁴ in frequency, 100 in depth). At 60 Hz, 8.5 mm means that the core of a power conductor much thicker than two skin depths carries little current, which is why large busbars are flat or hollow.

### Example 13-05.4 · The AC resistance of a wire (tier B)

**Setup.** A copper wire of 1 mm diameter carries a 100 MHz current. Find δ, the DC resistance per metre, the AC resistance per metre and their ratio.

**Solution.** δ = **6.609** µm, much smaller than the 0.5 mm radius. $R'_{dc} = 1/(\sigma\pi a^2)$ = **21.95** mΩ/m. $R'_{ac} = 1/(2\pi a\sigma\delta)$ = **0.8305** Ω/m. The ratio is $a/(2\delta)$ = **37.83**.

**Sanity check.** The current uses a ring 6.6 µm thick out of a 500 µm radius: the conducting area is $2\pi a\delta$ against $\pi a^2$, a fraction $2\delta/a$, so the resistance rises by the inverse.

### Example 13-05.5 · Loss in board laminates (tier B)

**Setup.** Estimate the dielectric attenuation at 10 GHz of a plane wave (or a TEM line) in an FR-4-like laminate ($\varepsilon_r$ = 4.0, $\tan\delta$ = 0.02) and in a low-loss laminate ($\varepsilon_r$ = 3.45, $\tan\delta$ = 0.0031, the values of a commercial low-loss material [2]). Give each in Np/m and dB/m.

**Solution.** With $\alpha = \pi f\sqrt{\varepsilon_r}\tan\delta/c$: FR-4-like, **4.192** Np/m = **36.41** dB/m (0.36 dB/cm); low-loss, **0.6034** Np/m = **5.241** dB/m. The low-loss laminate has **6.947** times less dielectric attenuation.

**Sanity check.** Both scale with $f$: at 28 GHz the FR-4-like loss would be **1.019** dB/cm, which is why millimetre-wave and 100+ Gb/s boards cannot use standard FR-4 for their fast nets. Conductor loss adds to this (Problem 13-05.13 compares the two for a coax).

### Example 13-05.6 · Radio under the sea (tier C)

**Setup.** Seawater has σ = 4 S/m and $\varepsilon_r$ = 81. (a) Show that it is a good conductor at 10 kHz and find the skin depth there and at 1 MHz. (b) Find the attenuation in dB over 20 m at 10 kHz. (c) At 1 GHz, compute α and β from the exact formulas and compare with the good-conductor value $1/\delta$.

**Solution.** (a) At 10 kHz, $\sigma/\omega\varepsilon$ = **8.88 × 10⁴** ≫ 1. δ = $1/\sqrt{\pi f\mu_0\sigma}$ = **2.516** m at 10 kHz and **0.2516** m at 1 MHz. (b) 20 m is **7.95** skin depths, so the loss is $20/\delta \times 8.686$ = **69.03** dB. (c) At 1 GHz $\sigma/\omega\varepsilon$ = 0.888, neither limit. The exact formulas give α = **77.44** Np/m and β = **203.9** rad/m, while the good-conductor formula would give $1/\delta$ = **125.7** Np/m for both: **62**% too high for α, and much too low for β.

**Sanity check.** At 1 GHz the field falls by 8.686 × 77.44 = **672.7** dB per metre: radio cannot penetrate the sea at microwave frequencies at all. At 10 kHz a submarine a few metres down can still receive, which is why very-low-frequency transmitters (with enormous antennas) serve submarines.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T 13-05.a | copper wavelength inside the metal at 1 GHz | 13 | µm |
| T 13-05.b | copper phase velocity inside the metal at 1 GHz | 13 | km/s |
| Ex 13-05.1a | wavelength in air | 12.49 | cm |
| Ex 13-05.1b | wavenumber | 50.30 | rad/m |
| Ex 13-05.1c | peak H | 2.654 | mA/m |
| Ex 13-05.1d | power density | 1.327 | mW/m² |
| Ex 13-05.1e | wavelength in the dielectric | 6.246 | cm |
| Ex 13-05.1f | intrinsic impedance of the dielectric | 188.4 | Ω |
| Ex 13-05.1g | phase velocity in the dielectric | 1.499 × 10⁸ | m/s |
| Ex 13-05.2a | angle of the linear polarization | 53.13 | ° |
| Ex 13-05.2b | linear antenna on a circular wave | −3.010 | dB |
| Ex 13-05.3a | skin depth at 60 Hz | 8.532 | mm |
| Ex 13-05.3b | skin depth at 1 MHz | 66.09 | µm |
| Ex 13-05.3c | skin depth at 1 GHz | 2.090 | µm |
| Ex 13-05.3d | skin depth at 10 GHz | 0.6609 | µm |
| Ex 13-05.3e | surface resistance at 1 GHz | 8.250 | mΩ |
| Ex 13-05.4a | skin depth at 100 MHz | 6.609 | µm |
| Ex 13-05.4b | DC resistance per metre | 21.95 | mΩ/m |
| Ex 13-05.4c | AC resistance per metre | 0.8305 | Ω/m |
| Ex 13-05.4d | AC/DC ratio | 37.83 | — |
| Ex 13-05.5a | FR-4-like attenuation | 4.192 | Np/m |
| Ex 13-05.5b | FR-4-like attenuation | 36.41 | dB/m |
| Ex 13-05.5c | low-loss attenuation | 0.6034 | Np/m |
| Ex 13-05.5d | low-loss attenuation | 5.241 | dB/m |
| Ex 13-05.5e | ratio of the two | 6.947 | — |
| Ex 13-05.5f | FR-4-like attenuation at 28 GHz | 1.019 | dB/cm |
| Ex 13-05.6a | seawater skin depth at 10 kHz | 2.516 | m |
| Ex 13-05.6b | seawater skin depth at 1 MHz | 0.2516 | m |
| Ex 13-05.6c | loss over 20 m at 10 kHz | 69.03 | dB |
| Ex 13-05.6d | exact α at 1 GHz | 77.44 | Np/m |
| Ex 13-05.6e | exact β at 1 GHz | 203.9 | rad/m |
| Ex 13-05.6f | good-conductor 1/δ at 1 GHz | 125.7 | Np/m |
| Ex 13-05.6g | attenuation at 1 GHz | 672.7 | dB/m |
| Ex 13-05.6h | 20 m in skin depths at 10 kHz | 7.95 | — |
| Ex 13-05.6i | good-conductor α error at 1 GHz | 62 | % |
| Ex 13-05.6j | σ/ωε at 10 kHz | 8.88 × 10⁴ | — |
| Prac 13-05.a | RG-58 fitted conductor loss at 100 MHz | 4.02 | dB/100 ft |
| Prac 13-05.b | RG-58 fitted dielectric loss at 100 MHz | 0.88 | dB/100 ft |
| Prac 13-05.c | RG-58 fitted conductor loss at 1 GHz | 12.72 | dB/100 ft |
| Prac 13-05.d | RG-58 fitted dielectric loss at 1 GHz | 8.78 | dB/100 ft |
| Prac 13-05.e | copper skin depth at 20 kHz | 0.4673 | mm |
| Sim 13-05.a | simulated surface resistance at 1 GHz | 8.250 | mΩ |
| Sim 13-05.b | simulated surface reactance at 1 GHz | 8.250 | mΩ |

*Every value is recomputed by [verify_13_05.py](../verify/verify_13_05.py): wave quantities by solving the one-dimensional Helmholtz equation numerically, γ and η by complex arithmetic checked against the closed forms, skin depths and surface resistance by solving the diffusion equation in the conductor numerically and integrating its loss, the round wire by the exact Bessel-function solution, and the polarization by tracing the field over a cycle. The surface impedance is also simulated in ngspice as an R–L ladder.*

## 5. Simulate it

The lab, [labs/13-05-lab](../labs/13-05-lab/README.md), has a notebook and an ngspice netlist:

1. Animates (as snapshots) $\vec{E}$ and $\vec{H}$ of a plane wave in a lossless and a lossy medium.
2. Traces the tip of $\vec{E}$ over a cycle for linear, circular and elliptical polarizations and computes the axial ratio.
3. Plots α and β against frequency for seawater from the exact formulas, with the low-loss and good-conductor approximations, and finds where each is accurate.
4. Solves the current distribution in a round copper wire exactly (Bessel functions) and plots the AC resistance against frequency with the $a/2\delta$ approximation.

The netlist [skin_ladder.cir](../labs/13-05-lab/skin_ladder.cir) models one square of a copper surface as a ladder of series inductors ($\mu_0$ times the layer thickness) and shunt resistors (the layer's sheet resistance), the circuit form of the field equations inside the conductor, and measures its input impedance at 1 GHz.

**Guided exercise (predict, then run).** **Before running the netlist**, predict the real and imaginary parts of the ladder's input impedance at 1 GHz. Then run it. (Both are $R_s$ = **8.250** mΩ: a good conductor's surface impedance is $(1 + j)R_s$.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Lower-$\tan\delta$ laminate | Dielectric loss ∝ $f\sqrt{\varepsilon_r}\tan\delta$, reach at high data rates | Material cost (several times FR-4), processing | SI engineer, PCB designer |
| Smoother copper foil | Conductor loss at tens of GHz (roughness adds to $R_s$) | Adhesion, cost | PCB fabricator, SI engineer |
| Wider traces or larger coax | Lower conductor loss ($R_s$ over a larger perimeter) | Density, thickness, impedance constraints | SI engineer, mechanical designer |
| Litz wire, flat or hollow conductors | Lower AC resistance in magnetics and busbars | Cost, fill factor | Power-electronics designer |
| Circular polarization | Orientation-independent links, no Faraday-rotation fading | 3 dB loss to linear receivers, antenna complexity | RF and antenna engineer |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Impedance of free space | 376.7 Ω | ≈ 120π; $\eta_0/\sqrt{\varepsilon_r}$ in a dielectric |
| Copper conductivity (100% IACS, 20 °C) | 5.8 × 10⁷ S/m | 1.7241 µΩ·cm [1] |
| Copper skin depth | 8.5 mm at 60 Hz; 66 µm at 1 MHz; 2.1 µm at 1 GHz | $\propto 1/\sqrt f$ |
| Copper surface resistance | 8.25 mΩ at 1 GHz | $\propto\sqrt f$ |
| 1 neper | 8.686 dB | Field falls by $e$ |
| Dielectric loss, FR-4-like at 10 GHz | about 0.36 dB/cm | $\propto f$ at constant $\tan\delta$ |
| Linear antenna on a circular wave | −3 dB | Any orientation |

## 8. Common mistakes

- **Using the good-conductor formula where σ/ωε is near 1.** Seawater at 1 GHz is neither conductor nor dielectric; use the exact γ.
- **Confusing nepers and decibels.** An attenuation of 1 Np/m is 8.686 dB/m in power or field ratio terms; for fields, dB = 20 log₁₀ and $e^{-\alpha z}$ gives 8.686 αz dB.
- **Assuming a thicker wire always helps at high frequency.** Only the surface carries current; perimeter matters, not area.
- **Reading polarization hand from the wrong side.** The IEEE convention is defined with the thumb along the propagation direction; reverse the direction and the same rotation is the opposite hand.
- **Treating $\vec{H}$ as in phase with $\vec{E}$ in a lossy medium.** With complex η it lags, by 45° in a good conductor.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Coax loss splits into conductor and dielectric parts.** Belden's RG-58 data sheet gives 4.9 dB/100 ft at 100 MHz and 21.5 dB/100 ft at 1 GHz [3] **[Established]**. Fitting $a\sqrt f + bf$ to those two points (our arithmetic, a two-point fit, not a manufacturer split) attributes **4.02** dB of the 100 MHz loss to the conductors and **0.88** dB to the dielectric, and **12.72** and **8.78** dB at 1 GHz: conductor loss dominates at low frequency, and dielectric loss catches up as frequency rises.
- **Laminate choice is a loss-tangent decision.** Commercial low-loss laminates quote $D_f$ near 0.003 at 10 GHz, against about 0.02 for standard FR-4-class material [2] **[Established]** (vendor data at stated test conditions). Example 13-05.5 turns that into a factor of about 7 in dielectric attenuation.
- **Copper's conductivity is a standard.** The International Annealed Copper Standard defines 100% conductivity as 1.7241 µΩ·cm at 20 °C (58 MS/m) [1] **[Established]**; thin films and rough foils perform worse, and high-speed design uses roughness models that raise the effective $R_s$ by tens of per cent at tens of gigahertz **[Industry estimate]**.

### Why it matters commercially

- **Reach of electrical links.** Every copper link (PCIe, Ethernet over backplanes, die-to-die) has a loss budget in dB at its Nyquist frequency; skin and dielectric loss set how far a signal can go before a retimer or optics is needed (Course 24).
- **Material and cable costs.** Low-loss laminates and low-loss cable assemblies cost several times more than standard ones; knowing whether conductor or dielectric loss dominates tells you which to pay for.
- **Wireless coverage.** Building materials and the human body are lossy dielectrics at radio frequencies; penetration loss rises with frequency, one reason millimetre-wave cells are small.

### Marketing vs Reality

- **"High-purity copper audio cable for better sound."** *Reality:* at 20 kHz copper's skin depth is **0.4673** mm (our arithmetic), larger than the radius of typical speaker-cable strands, so the skin effect is negligible across the audio band and resistance per length is what matters. *Sanity check:* compare the cable's resistance per metre, not its purity grade.
- **"Ultra-low-loss laminate."** *Reality:* $D_f$ depends on frequency, temperature and resin content, and conductor loss (foil roughness) may dominate. *Sanity check:* ask for insertion loss in dB per inch at your Nyquist frequency on a test coupon with your copper foil.

### Questions for engineering leaders

1. **"What fraction of your channel's insertion loss is conductor loss and what fraction is dielectric?"**
   *Strong:* a split from a field solver or measured coupons, with the roughness model named. *Evasive:* a single total in dB.
2. **"Why did you choose this laminate over a cheaper one?"**
   *Strong:* the loss at Nyquist and the reach it buys, against the cost per board. *Evasive:* "it's the industry standard."
3. **"How does your antenna's polarization match the devices it talks to?"**
   *Strong:* a stated polarization, with the mismatch loss counted in the link budget for typical orientations. *Evasive:* "the antenna is omnidirectional."

## 10. Concept check

**Q1.** Why are $\vec{E}$ and $\vec{H}$ in phase in a lossless plane wave but not in a lossy one?

<details><summary>Answer</summary>

Their ratio is the intrinsic impedance $\sqrt{j\omega\mu/(\sigma + j\omega\varepsilon)}$. With σ = 0 it is real ($\sqrt{\mu/\varepsilon}$), so they are in phase; with conductivity it is complex, and $\vec{H}$ lags $\vec{E}$ by up to 45° (a good conductor).

</details>

**Q2.** What is the polarization of $(\hat{x} + j\hat{y})e^{-jkz}$?

<details><summary>Answer</summary>

Circular, and left-hand: at $z$ = 0, $\vec{E} = \cos\omega t\,\hat{x} - \sin\omega t\,\hat{y}$ rotates from $x$ toward $-y$, the left-handed sense about the $+z$ direction of travel (the left thumb along $+z$, fingers curling from $x$ to $-y$).

</details>

**Q3.** Why does a conductor's AC resistance grow as $\sqrt f$?

<details><summary>Answer</summary>

The current is confined to about one skin depth, and $\delta \propto 1/\sqrt f$, so the effective conducting area shrinks as $1/\sqrt f$ and the resistance grows as $\sqrt f$.

</details>

**Q4.** When can you use $\alpha \approx \pi f\sqrt{\varepsilon_r}\tan\delta/c$?

<details><summary>Answer</summary>

For a nonmagnetic dielectric with low loss, $\sigma/\omega\varepsilon = \tan\delta \ll 1$; the error is of order $\tan^2\delta$, negligible for any practical laminate.

</details>

**Q5.** Why do metals reflect radio waves?

<details><summary>Answer</summary>

Their intrinsic impedance is milliohms against 377 Ω for air: the boundary looks almost like a short circuit, so nearly all the incident power is reflected, and the small fraction that enters dies within a few skin depths (13-06).

</details>

**Q6.** In a good conductor, how do the phase and group velocities compare?

<details><summary>Answer</summary>

$v_p = \omega/\beta = \omega\delta$ and, because $\beta \propto \sqrt\omega$, $v_g = d\omega/d\beta = 2\omega\delta = 2v_p$. Both are tiny compared with $c$.

</details>

Next: the [13-05 problem set](../problems/13-05-problems.md).

## 11. Key terms

[Uniform plane wave](../../../reference/glossary.md#uniform-plane-wave) · [Intrinsic impedance](../../../reference/glossary.md#intrinsic-impedance) · [Impedance of free space](../../../reference/glossary.md#impedance-of-free-space) · [Phase velocity](../../../reference/glossary.md#phase-velocity) · [Group velocity](../../../reference/glossary.md#group-velocity) · [Propagation constant](../../../reference/glossary.md#propagation-constant) · [Polarization (light)](../../../reference/glossary.md#polarization-light) · [Axial ratio](../../../reference/glossary.md#axial-ratio) · [Skin effect](../../../reference/glossary.md#skin-effect) · [Skin depth](../../../reference/glossary.md#skin-depth) · [Surface resistance](../../../reference/glossary.md#surface-resistance) · [Neper](../../../reference/glossary.md#neper)

## 12. Connections

- **Builds on:** the Helmholtz equation, σ/ωε and the Poynting vector from [13-04](13-04-maxwells-equations.md); waves from [04-09](../../04-physics-for-ee/chapters/04-09-waves-and-optics.md); complex roots from [02-01](../../02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md).
- **Next:** [13-06 Reflection and Transmission of Waves](13-06-reflection-and-transmission.md) sends these waves into boundaries between media.
- **Used later:** γ and $Z_0$ of transmission lines ([13-08](13-08-transmission-lines-sinusoidal-steady-state.md)), whose loss comes from $R_s$ and $\tan\delta$; conductor losses in waveguides and cavities ([13-10](13-10-waveguides-and-resonators.md)); polarization and power density in antennas ([13-11](13-11-radiation-and-antennas.md)).

## 13. Further study

- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 7 (plane-wave propagation).
- D. K. Cheng, *Field and Wave Electromagnetics*, ch. 8 (plane electromagnetic waves).
- D. M. Pozar, *Microwave Engineering*, ch. 1 (plane waves, surface resistance).
- MIT OpenCourseWare 6.013, *Electromagnetics and Applications*, lectures on waves in media.

## 14. Sources

1. NBS Handbook 100, *Copper Wire Tables* (1966): the International Annealed Copper Standard. [R-101](../../../reference/research-log.md#r-101--resistors-preferred-values-film-technologies-copper-and-shunts).
2. Isola I-Tera MT40 and 370HR laminate data sheets; Rogers RO4350B. [R-193](../../../reference/research-log.md#r-193--pcb-laminate-dielectric-constants-and-loss-tangents).
3. Belden 8262 RG-58 coaxial cable data sheet. [R-194](../../../reference/research-log.md#r-194--rg-58-coaxial-cable-data-sheets).

The physics (plane waves, polarization, skin effect) is textbook material (Further study).
