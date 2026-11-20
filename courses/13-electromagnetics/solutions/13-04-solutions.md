# Solutions 13-04 · Maxwell's Equations and Time-Varying Fields

Problems: [13-04 problems](../problems/13-04-problems.md) · Chapter: [13-04](../chapters/13-04-maxwells-equations.md). Every number below is recomputed by [verify_13_04.py](../verify/verify_13_04.py), which checks the field relations symbolically (sympy curls and divergences) and the power flows by numerical surface integration.

---

## Solutions

### Solution 13-04.1

$\Phi = BA\cos\omega t$ with $A$ = 0.01 m², so the EMF amplitude is $\omega BA = 2\pi \times 60 \times 2 \times 10^{-4} \times 0.01$ = **0.7540** mV. Small, but in a high-gain audio or sensor input it is the familiar mains hum; twisting the wires so successive loops alternate in sign cancels it.

### Solution 13-04.2

$J_d = \omega\varepsilon_0E = 2\pi \times 10^9 \times 8.854 \times 10^{-12} \times 10^3$ = **55.63** A/m². Units: (1/s)(F/m)(V/m) = (C/(V·m·s))(V/m) = A/m².

### Solution 13-04.3

$\tau_r = \varepsilon/\sigma = \varepsilon\rho$ with $\rho$ in Ω·m. Doped: $11.7\varepsilon_0 \times 0.5 \times 10^{-2}$ = **5.180 × 10⁻¹³** s, so it behaves as a dielectric only above $1/(2\pi\tau_r)$ = **307.3** GHz. Intrinsic: $11.7\varepsilon_0 \times 2.3 \times 10^3$ = **2.383 × 10⁻⁷** s, a dielectric above **668.0** kHz. Doped silicon is a conductor at all circuit frequencies; nearly intrinsic silicon (as in high-resistivity RF substrates) behaves as a dielectric at radio frequencies, which is why it is chosen to reduce substrate loss under on-chip inductors and transmission lines.

### Solution 13-04.4

(a) In free space $\beta = \omega/c$, so $\omega = 2c$ = **5.996 × 10⁸** rad/s and $f$ = **95.43** MHz.

(b) With no conduction current, $\nabla\times\tilde{\vec{H}} = j\omega\varepsilon_0\tilde{\vec{E}}$. For $\tilde{\vec{H}} = \tilde H_y(z)\hat{y}$, $\nabla\times\tilde{\vec{H}} = -\partial\tilde H_y/\partial z\,\hat{x} = j2(0.1)e^{-j2z}\hat{x}$. So

$$
\tilde{\vec{E}} = \frac{j0.2e^{-j2z}}{j\omega\varepsilon_0}\hat{x} = \frac{0.2}{\omega\varepsilon_0}e^{-j2z}\hat{x} = \mathbf{37.67}\,e^{-j2z}\,\hat{x}\ \text{V/m},
$$

which is $\eta_0 \times 0.1$. In the time domain, $\vec{E} = 37.67\cos(\omega t - 2z)\,\hat{x}$ V/m.

(c) $\vec{S}_{av} = \tfrac12\text{Re}\{\tilde E_x\tilde H_y^*\}\,(\hat{x}\times\hat{y}) = \tfrac12 \times 37.67 \times 0.1\,\hat{z}$ = **1.884** W/m² along $+z$.

### Solution 13-04.5

$\nabla\cdot\vec{J} = \partial J_x/\partial x = J_0/a$ = 100 A/m³, so $\partial\rho_v/\partial t = -\nabla\cdot\vec{J}$ = **−100** C/(m³·s). More current leaves each small volume than enters it (the current density grows with $x$), so charge is draining away.

### Solution 13-04.6

$\sigma_{eff} = \omega\varepsilon_0\varepsilon_r'\tan\delta = 2\pi \times 10^9 \times 4.3\varepsilon_0 \times 0.02$ = **4.784** mS/m. The time-average power density is $\tfrac12\sigma_{eff}\lvert E\rvert^2 = \tfrac12 \times 4.784 \times 10^{-3} \times 100^2$ = **23.92** W/m³. Units: (S/m)(V/m)² = W/m³.

### Solution 13-04.7

$C = \varepsilon_0\pi r^2/d$ = **2.782** pF, and the displacement current equals $C\,dv/dt = 2.782\ \text{pF} \times 10^9\ \text{V/s}$ = **2.782** mA. By the Ampère–Maxwell law around the rim (all the displacement current is enclosed), $H = I_d/(2\pi r)$ = **44.27** mA/m. With $E = v/d$ = 10⁵ V/m pointing from the higher plate to the lower, $\vec{E}\times\vec{H}$ points radially inward, with $S = EH$ = **4427** W/m². Over the rim's area $2\pi rd$ = 6.283 × 10⁻⁵ m², the inflow is **0.2782** W. And

$$
\frac{d}{dt}\Big(\frac12Cv^2\Big) = Cv\frac{dv}{dt} = 2.782 \times 10^{-12} \times 100 \times 10^9 = \mathbf{0.2782}\ \text{W}.
$$

The energy a capacitor stores enters through the open edge of the gap, from the field around it, not along the wires.

### Solution 13-04.8

Setting $\text{EIRP}/(4\pi r^2)$ = 10 W/m² (1 mW/cm²): $r = \sqrt{1000/(40\pi)}$ = **2.821** m. There, for a plane wave, $E_{rms} = \sqrt{S\eta_0} = \sqrt{10 \times 376.7}$ = **61.38** V/m. (Close to a real antenna the far-field formula does not apply, and compliance distances are computed or measured more carefully.)

### Solution 13-04.9

$v = c/\sqrt{\varepsilon_r} = c/2$, so $\lambda = v/f$ = **14.99** cm at 1 GHz. A λ/10 rule allows **1.499** cm at 1 GHz and **1.499** mm at 10 GHz.

### Solution 13-04.10

$E = V/d = 1.0/10^{-4}$ V/m = **10** kV/m, directed from the supply plane to the ground plane. For wide planes carrying opposite surface currents $K = I/w$, the field between them is $H = K = 10/0.02$ = **500** A/m (Ampère's law around one plane, as for a long sheet pair). $S = EH$ = **5 × 10⁶** W/m², along the planes toward the load, and over the cross-section $wd$ = 2 × 10⁻⁶ m² the power is **10** W = $VI$. The power travels in the thin dielectric between the planes; the copper carries the currents that set up $H$, and its resistance takes a small inward flow as loss.

### Solution 13-04.11

(a) $\sigma_{eff} = 2\pi \times 10^8 \times 4.3\varepsilon_0 \times 0.02$ = **0.4784** mS/m. With $E = V/d$ = 10⁴ V/m in a volume of 10⁻⁷ m³, $P = \tfrac12 \times 0.4784 \times 10^{-3} \times 10^8 \times 10^{-7}$ = **2.392** mW.

(b) $C = 4.3\varepsilon_0 \times 10^{-4}/10^{-3}$ = **3.807** pF, $G = \omega C\tan\delta$ = **47.84** µS, and $\tfrac12GV^2$ = **2.392** mW, the same. The two descriptions are identical because $G/C = \sigma_{eff}/\varepsilon$ for any parallel-plate geometry: the circuit model's conductance is the field model's equivalent conductivity times the same geometric factor $A/d$.

### Solution 13-04.12

The flux through each turn is $BA\cos\omega t$ with $\omega = 2\pi \times 60$ rad/s, so the EMF is $NBA\omega\sin\omega t$, with peak $100 \times 0.5 \times 0.01 \times 376.99$ = **188.5** V and rms value **133.3** V. Seen from the coil, this is Faraday's law; seen from the lab, it is the motional EMF $\vec{v}\times\vec{B}$ on the moving wires, and both give the same answer.

### Solution 13-04.13

(a) With $\tilde E_y = E_0\sin(\pi x/a)e^{-j\beta z}$, $\partial^2\tilde E_y/\partial x^2 = -(\pi/a)^2\tilde E_y$ and $\partial^2\tilde E_y/\partial z^2 = -\beta^2\tilde E_y$, while the $y$ derivative is zero. The Helmholtz equation $\nabla^2\tilde E_y + k^2\tilde E_y = 0$ becomes $[-(\pi/a)^2 - \beta^2 + k^2]\tilde E_y = 0$, so $\beta^2 = k^2 - (\pi/a)^2$ with $k^2 = \omega^2\mu_0\varepsilon_0$. Also $\nabla\cdot\tilde{\vec{E}} = \partial\tilde E_y/\partial y = 0$, as required. At $x$ = 0 and $x = a$, $\sin$ is zero, so the tangential field vanishes on the conducting side walls ($\tilde E_y$ is normal to the top and bottom walls, where it may be nonzero).

(b) β is real only when $k > \pi/a$, that is above $f_c = c/(2a)$ = **6.557** GHz. At 10 GHz, $k$ = 209.6 rad/m and $\pi/a$ = 137.4 rad/m, so β = **158.2** rad/m and the guide wavelength is **3.971** cm, longer than the 3.0 cm free-space wavelength. 13-10 develops this mode, called TE₁₀.

### Solution 13-04.14

(a) Take the curl of the Ampère–Maxwell phasor law with no current: $\nabla\times\nabla\times\tilde{\vec{H}} = j\omega\varepsilon\nabla\times\tilde{\vec{E}} = j\omega\varepsilon(-j\omega\mu\tilde{\vec{H}}) = \omega^2\mu\varepsilon\tilde{\vec{H}}$. With $\nabla\times\nabla\times\tilde{\vec{H}} = \nabla(\nabla\cdot\tilde{\vec{H}}) - \nabla^2\tilde{\vec{H}}$ and $\nabla\cdot\tilde{\vec{H}} = 0$, this is $\nabla^2\tilde{\vec{H}} + \omega^2\mu\varepsilon\tilde{\vec{H}} = 0$, the same Helmholtz equation as for $\tilde{\vec{E}}$.

(b) $1/\sqrt{\mu_0\varepsilon_0}$ = **2.998 × 10⁸** m/s and $\sqrt{\mu_0/\varepsilon_0}$ = **376.7** Ω. With the rounded $\varepsilon_0$ = 8.854 × 10⁻¹² F/m these come out the same to four figures.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 13-04.1a | peak EMF | 0.7540 | mV |
| 13-04.2a | displacement current density | 55.63 | A/m² |
| 13-04.3a | relaxation time, doped | 5.180 × 10⁻¹³ | s |
| 13-04.3b | dielectric above, doped | 307.3 | GHz |
| 13-04.3c | relaxation time, intrinsic | 2.383 × 10⁻⁷ | s |
| 13-04.3d | dielectric above, intrinsic | 668.0 | kHz |
| 13-04.4a | angular frequency | 5.996 × 10⁸ | rad/s |
| 13-04.4b | frequency | 95.43 | MHz |
| 13-04.4c | electric field amplitude | 37.67 | V/m |
| 13-04.4d | time-average power density | 1.884 | W/m² |
| 13-04.5a | rate of change of charge density | −100 | C/(m³·s) |
| 13-04.6a | equivalent conductivity | 4.784 | mS/m |
| 13-04.6b | power density | 23.92 | W/m³ |
| 13-04.7a | capacitance | 2.782 | pF |
| 13-04.7b | displacement current | 2.782 | mA |
| 13-04.7c | H at the rim | 44.27 | mA/m |
| 13-04.7d | Poynting vector at the rim | 4427 | W/m² |
| 13-04.7e | power inflow | 0.2782 | W |
| 13-04.7f | rate of energy storage | 0.2782 | W |
| 13-04.8a | distance to 1 mW/cm² | 2.821 | m |
| 13-04.8b | rms electric field there | 61.38 | V/m |
| 13-04.9a | wavelength at 1 GHz | 14.99 | cm |
| 13-04.9b | lumped limit at 1 GHz | 1.499 | cm |
| 13-04.9c | lumped limit at 10 GHz | 1.499 | mm |
| 13-04.10a | electric field between the planes | 10 | kV/m |
| 13-04.10b | magnetic field between the planes | 500 | A/m |
| 13-04.10c | Poynting vector | 5 × 10⁶ | W/m² |
| 13-04.10d | power flow | 10 | W |
| 13-04.11a | equivalent conductivity at 100 MHz | 0.4784 | mS/m |
| 13-04.11b | dissipated power, field view | 2.392 | mW |
| 13-04.11c | capacitance | 3.807 | pF |
| 13-04.11d | conductance | 47.84 | µS |
| 13-04.11e | dissipated power, circuit view | 2.392 | mW |
| 13-04.12a | peak EMF | 188.5 | V |
| 13-04.12b | rms EMF | 133.3 | V |
| 13-04.13a | cutoff frequency | 6.557 | GHz |
| 13-04.13b | phase constant at 10 GHz | 158.2 | rad/m |
| 13-04.13c | guide wavelength at 10 GHz | 3.971 | cm |
| 13-04.14a | wave speed | 2.998 × 10⁸ | m/s |
| 13-04.14b | impedance of free space | 376.7 | Ω |
