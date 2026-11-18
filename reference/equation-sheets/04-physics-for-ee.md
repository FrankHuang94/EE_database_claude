# Equation Sheet · 04 Physics for EE

The relations to know cold from Course 04, each with its conditions and the chapter that derives it. Constants: $e = 1.602\,176\,634\times10^{-19}$ C, $h = 6.626\,070\,15\times10^{-34}$ J·s, $k = 1.380\,649\times10^{-23}$ J/K, $c = 299\,792\,458$ m/s (exact); $\varepsilon_0 = 8.854\times10^{-12}$ F/m, $\mu_0 = 1.2566\times10^{-6}$ H/m, $m_0 = 9.109\times10^{-31}$ kg; $kT$ = 25.85 meV at 300 K; $hc$ = 1239.84 eV·nm.

## Mechanics

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $W = \int\vec F\cdot d\vec s = \Delta K$; $P = Fv = \tau\omega$; $\vec J = \int\vec F\,dt = \Delta\vec p$ | Work–energy and impulse–momentum | [04-01](../../courses/04-physics-for-ee/chapters/04-01-mechanics-essentials.md) |
| Drop from height $h$: $v = \sqrt{2gh}$; half-sine pulse peak = $(\pi/2)\times$ average | Shock design | [04-01](../../courses/04-physics-for-ee/chapters/04-01-mechanics-essentials.md) |
| $\omega_0 = \sqrt{k_s/m}$, $Q = m\omega_0/b$, $\zeta = 1/(2Q)$; energy decays by $e$ in $Q/\pi$ cycles | Spring–mass–damper ≡ series RLC | [04-01](../../courses/04-physics-for-ee/chapters/04-01-mechanics-essentials.md) |
| Accelerometer: $x/a = 1/\omega_0^2$; Brownian floor $a_n = \sqrt{4kT\omega_0/(mQ)}$ per √Hz | Below resonance; equipartition $\tfrac12k_s\overline{x^2} = \tfrac12kT$ | [04-01](../../courses/04-physics-for-ee/chapters/04-01-mechanics-essentials.md) |

## Electrostatics and Gauss's law

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $F = k_eq_1q_2/r^2$, $k_e = 1/(4\pi\varepsilon_0) = 8.988\times10^9$ N·m²/C²; $\vec E = \vec F/q$; superpose vectors | Point charges | [04-02](../../courses/04-physics-for-ee/chapters/04-02-charge-coulomb-and-electric-fields.md) |
| Line $\lambda/(2\pi\varepsilon_0r)$; sheet $\sigma/(2\varepsilon_0)$; between ±σ plates $\sigma/\varepsilon_0$ | Infinite geometries | [04-02](../../courses/04-physics-for-ee/chapters/04-02-charge-coulomb-and-electric-fields.md) |
| Dipole $p = qd$: far field $2k_ep/r^3$ on axis, $k_ep/r^3$ broadside; torque $\vec p\times\vec E$; energy $-\vec p\cdot\vec E$ | $r\gg d$ | [04-02](../../courses/04-physics-for-ee/chapters/04-02-charge-coulomb-and-electric-fields.md) |
| $\Phi_E = \oint\vec E\cdot d\vec A = Q_{\text{enc}}/\varepsilon_0$ | Always true; useful with symmetry | [04-03](../../courses/04-physics-for-ee/chapters/04-03-gauss-law.md) |
| Solid sphere: $k_eQr/R^3$ inside, $k_eQ/r^2$ outside; shell: 0 inside | Uniform charge | [04-03](../../courses/04-physics-for-ee/chapters/04-03-gauss-law.md) |
| Conductor: $E = 0$ inside, $E = \sigma/\varepsilon_0$ just outside, normal to the surface | Electrostatic equilibrium | [04-03](../../courses/04-physics-for-ee/chapters/04-03-gauss-law.md) |
| In a material $\oint\vec D\cdot d\vec A = Q_{\text{free}}$; junction peak field $qN_Ax_p/\varepsilon_s = qN_Dx_n/\varepsilon_s$ | Depletion approximation | [04-03](../../courses/04-physics-for-ee/chapters/04-03-gauss-law.md) |
| HBM: 100 pF through 1.5 kΩ, $I_{pk} = V/1500$, τ = 150 ns | ESD qualification model | [04-02](../../courses/04-physics-for-ee/chapters/04-02-charge-coulomb-and-electric-fields.md) |

## Potential, capacitance and dielectrics

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $V_B - V_A = -\int_A^B\vec E\cdot d\vec\ell$; $\vec E = -\nabla V$; point charge $V = k_eq/r$ | Conservative field | [04-04](../../courses/04-physics-for-ee/chapters/04-04-potential-capacitance-and-dielectrics.md) |
| $K = qV$; $v = \sqrt{2qV/m}$; 1 eV = $1.602\times10^{-19}$ J | Non-relativistic | [04-04](../../courses/04-physics-for-ee/chapters/04-04-potential-capacitance-and-dielectrics.md) |
| $C$: plates $\varepsilon A/d$; coax $2\pi\varepsilon\ell/\ln(b/a)$; sphere $4\pi\varepsilon_0R$ | Best coax for breakdown: $b/a = e$ | [04-04](../../courses/04-physics-for-ee/chapters/04-04-potential-capacitance-and-dielectrics.md) |
| Parallel $C_1 + C_2$; series $C_1C_2/(C_1 + C_2)$; EOT $= \sum t_i\,(3.9/\varepsilon_{r,i})$ | Gate stacks | [04-04](../../courses/04-physics-for-ee/chapters/04-04-potential-capacitance-and-dielectrics.md) |
| $U = \tfrac12CV^2$; $u = \tfrac12\varepsilon E^2$; pressure $\tfrac12\varepsilon E^2$ | Field energy | [04-04](../../courses/04-physics-for-ee/chapters/04-04-potential-capacitance-and-dielectrics.md) |
| Charge sharing: $V_f = (C_1V_1 + C_2V_2)/(C_1 + C_2)$; loss $\tfrac12\frac{C_1C_2}{C_1+C_2}(\Delta V)^2$ | Any resistance | [04-04](../../courses/04-physics-for-ee/chapters/04-04-potential-capacitance-and-dielectrics.md) |

## Current and conduction

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $J = nqv_d$; $\sigma = nq\mu$; $\mu = q\tau/m$; Drude $\sigma = ne^2\tau/m$ | Copper: τ ≈ 25 fs; mean free path $v_F\tau$ ≈ 39 nm | [04-05](../../courses/04-physics-for-ee/chapters/04-05-current-resistance-and-conduction.md) |
| $\nabla\cdot\vec J = -\partial\rho/\partial t$ (KCL in steady state) | Continuity | [04-05](../../courses/04-physics-for-ee/chapters/04-05-current-resistance-and-conduction.md) |
| $R = \rho L/A$; sheet $R_\square = \rho/t$; $R(T) = R_{20}[1 + \alpha(T - 20)]$, $\alpha_{Cu} = 0.00393$/°C | Bulk Cu 1.68 µΩ·cm | [04-05](../../courses/04-physics-for-ee/chapters/04-05-current-resistance-and-conduction.md) |
| Joule heating $P = I^2R$, $p = J^2\rho$; distributed RC 50% delay ≈ 0.38 $rcL^2$ | Delay ∝ $L^2$ | [04-05](../../courses/04-physics-for-ee/chapters/04-05-current-resistance-and-conduction.md) |

## Magnetism

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\vec F = q\vec v\times\vec B$; $r = mv/(qB)$; $f_c = qB/(2\pi m)$ (28.0 GHz/T for electrons) | Lorentz force | [04-06](../../courses/04-physics-for-ee/chapters/04-06-magnetic-fields-and-forces.md) |
| $\vec F = I\vec\ell\times\vec B$; torque $\vec\mu\times\vec B$, $\mu = NIA$ | Motors, meters | [04-06](../../courses/04-physics-for-ee/chapters/04-06-magnetic-fields-and-forces.md) |
| Biot–Savart $d\vec B = \frac{\mu_0}{4\pi}\frac{I\,d\vec\ell\times\hat r}{r^2}$; wire $\mu_0I/(2\pi r)$; loop center $\mu_0I/(2R)$ |  | [04-06](../../courses/04-physics-for-ee/chapters/04-06-magnetic-fields-and-forces.md) |
| $\oint\vec B\cdot d\vec\ell = \mu_0I_{\text{enc}}$: solenoid $\mu_0nI$, toroid $\mu_0NI/(2\pi r)$; $\oint\vec B\cdot d\vec A = 0$ | Ampère; no monopoles | [04-06](../../courses/04-physics-for-ee/chapters/04-06-magnetic-fields-and-forces.md) |
| Parallel wires $F/\ell = \mu_0I_1I_2/(2\pi d)$; Hall $V_H = IB/(nqt)$ | Low $n$ → large $V_H$ | [04-06](../../courses/04-physics-for-ee/chapters/04-06-magnetic-fields-and-forces.md) |
| $B = \mu_0\mu_rH$; gapped core: the gap stores most energy and sets $L$ | Saturation limits $B$ | [04-06](../../courses/04-physics-for-ee/chapters/04-06-magnetic-fields-and-forces.md) |

## Induction

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\mathcal E = -N\,d\Phi/dt$ (Lenz's sign); motional $\mathcal E = B\ell v$ | KVL fails where $d\Phi/dt \ne 0$ | [04-07](../../courses/04-physics-for-ee/chapters/04-07-faraday-lenz-and-inductance.md) |
| $L = N\Phi/I$: solenoid $\mu_0N^2A/\ell$; gapped core $N^2/\mathcal R$; $v = L\,di/dt$ |  | [04-07](../../courses/04-physics-for-ee/chapters/04-07-faraday-lenz-and-inductance.md) |
| $M = k\sqrt{L_1L_2}$; ideal transformer $v_2/v_1 = N_2/N_1$, impedance × $(N_1/N_2)^2$ | Open secondary: $V = \omega MI$ | [04-07](../../courses/04-physics-for-ee/chapters/04-07-faraday-lenz-and-inductance.md) |
| $U = \tfrac12LI^2$; $u = B^2/(2\mu)$ | ≈ 0.4 MJ/m³ at 1 T in air | [04-07](../../courses/04-physics-for-ee/chapters/04-07-faraday-lenz-and-inductance.md) |
| Skin depth $\delta = \sqrt{\rho/(\pi f\mu)}$ (Cu: 65 µm at 1 MHz) | $\delta\propto1/\sqrt f$ | [04-07](../../courses/04-physics-for-ee/chapters/04-07-faraday-lenz-and-inductance.md) |

## Maxwell's equations and waves

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Displacement current $I_D = \varepsilon_0\,d\Phi_E/dt$; Ampère–Maxwell $\oint\vec B\cdot d\vec\ell = \mu_0(I + I_D)$ | Completes Maxwell's equations | [04-08](../../courses/04-physics-for-ee/chapters/04-08-maxwell-preview.md) |
| $c = 1/\sqrt{\mu_0\varepsilon_0}$; $\eta_0 = \sqrt{\mu_0/\varepsilon_0} = 376.7$ Ω; in a dielectric $v = c/\sqrt{\varepsilon_r}$, $\eta = \eta_0/\sqrt{\varepsilon_r}$ | Plane wave $E/H = \eta$ | [04-08](../../courses/04-physics-for-ee/chapters/04-08-maxwell-preview.md) |
| Poynting $\vec S = \vec E\times\vec H$; intensity $E_0^2/(2\eta)$ | Energy flows through the field | [04-08](../../courses/04-physics-for-ee/chapters/04-08-maxwell-preview.md) |
| Dielectric attenuation $\pi f\sqrt{\varepsilon_r}\tan\delta/c$ Np/m | Small tan δ; ∝ f | [04-08](../../courses/04-physics-for-ee/chapters/04-08-maxwell-preview.md) |

## Waves and optics

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $v = \lambda f$; string $\sqrt{T/\mu}$; light in a medium $c/n$ |  | [04-09](../../courses/04-physics-for-ee/chapters/04-09-waves-and-optics.md) |
| Two slits: bright at $d\sin\theta = m\lambda$, spacing $\lambda L/d$; standing waves $L = m\lambda/2$ | Interference | [04-09](../../courses/04-physics-for-ee/chapters/04-09-waves-and-optics.md) |
| Single slit first null $\sin\theta = \lambda/a$; circular $1.22\lambda/D$; lithography CD $= k_1\lambda/\text{NA}$, $k_1 \ge 0.25$ | Diffraction | [04-09](../../courses/04-physics-for-ee/chapters/04-09-waves-and-optics.md) |
| Snell $n_1\sin\theta_1 = n_2\sin\theta_2$; critical $\sin\theta_c = n_2/n_1$; reflectance $((n_1 - n_2)/(n_1 + n_2))^2$ | Normal incidence for $R$ | [04-09](../../courses/04-physics-for-ee/chapters/04-09-waves-and-optics.md) |
| Fiber NA $= \sqrt{n_1^2 - n_2^2}$; Malus $I = I_0\cos^2\theta$; Brewster $\tan\theta_B = n_2/n_1$ |  | [04-09](../../courses/04-physics-for-ee/chapters/04-09-waves-and-optics.md) |

## Quantum mechanics

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $E = hf = hc/\lambda$, $E[\text{eV}] = 1239.84/\lambda[\text{nm}]$; $p = h/\lambda$ | Photons | [04-10](../../courses/04-physics-for-ee/chapters/04-10-intro-quantum-mechanics.md) |
| Photoelectric $K_{\max} = hf - \varphi$; responsivity $\eta e\lambda/(hc) = \eta\lambda[\mu\text{m}]/1.24$ A/W |  | [04-10](../../courses/04-physics-for-ee/chapters/04-10-intro-quantum-mechanics.md) |
| de Broglie $\lambda = h/p = h/\sqrt{2mE}$ (1.226 nm/√V for electrons); $\Delta x\,\Delta p \ge \hbar/2$ |  | [04-10](../../courses/04-physics-for-ee/chapters/04-10-intro-quantum-mechanics.md) |
| $-\frac{\hbar^2}{2m}\psi'' + V\psi = E\psi$; infinite well $E_n = n^2h^2/(8mL^2)$ (0.376 eV for $m_0$, 1 nm) | Use $m^*$ in semiconductors | [04-10](../../courses/04-physics-for-ee/chapters/04-10-intro-quantum-mechanics.md) |
| Hydrogen $E_n = -13.6\text{ eV}/n^2$; Bohr radius 0.0529 nm |  | [04-10](../../courses/04-physics-for-ee/chapters/04-10-intro-quantum-mechanics.md) |
| Tunneling $T \approx 16\frac{E}{V_0}(1 - \frac{E}{V_0})e^{-2\kappa d}$, $\kappa = \sqrt{2m(V_0 - E)}/\hbar$ | $\kappa d\gg1$ | [04-10](../../courses/04-physics-for-ee/chapters/04-10-intro-quantum-mechanics.md) |
| Qubit $\alpha|0\rangle + \beta|1\rangle$: $P(0) = |\alpha|^2$; $n$ qubits need $2^n$ amplitudes |  | [04-10](../../courses/04-physics-for-ee/chapters/04-10-intro-quantum-mechanics.md) |

## Solid-state physics

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Diamond lattice: 8 atoms per cubic cell; Si $a$ = 0.5431 nm, $5.0\times10^{22}$ atoms/cm³ |  | [04-11](../../courses/04-physics-for-ee/chapters/04-11-intro-solid-state-physics.md) |
| $k_F = (3\pi^2n)^{1/3}$, $E_F = \hbar^2k_F^2/2m$, $v_F = \hbar k_F/m$; $g(E)\propto\sqrt E$, $g(E_F) = 3N/(2E_F)$ | Free-electron gas | [04-11](../../courses/04-physics-for-ee/chapters/04-11-intro-solid-state-physics.md) |
| Fermi–Dirac $f = 1/(1 + e^{(E - E_F)/kT})$; 90%→10% over $4.39kT$; $C_{\text{el}} = (\pi^2/2)Nk(T/T_F)$ | Boltzmann limit far above $E_F$ | [04-11](../../courses/04-physics-for-ee/chapters/04-11-intro-solid-state-physics.md) |
| Tight binding $E = E_0 - 2t\cos ka$ (width $4t$); Bragg gap $E_g = 2|U|$ at $k = \pm\pi/a$ | 2 electrons per primitive cell per band | [04-11](../../courses/04-physics-for-ee/chapters/04-11-intro-solid-state-physics.md) |
| $v = \hbar^{-1}dE/dk$; $\hbar\,dk/dt = F$; $1/m^* = \hbar^{-2}d^2E/dk^2$ | Holes: $+e$, mass $|m^*|$ | [04-11](../../courses/04-physics-for-ee/chapters/04-11-intro-solid-state-physics.md) |
| $np = N_cN_v e^{-E_g/kT}$; $n_i = \sqrt{N_cN_v}\,e^{-E_g/2kT}$ (Si $9.65\times10^9$ cm⁻³ at 300 K) | Non-degenerate | [04-11](../../courses/04-physics-for-ee/chapters/04-11-intro-solid-state-physics.md) |
| Absorption edge $\lambda_c = 1239.84/E_g$ nm; direct gaps emit efficiently, indirect need a phonon |  | [04-11](../../courses/04-physics-for-ee/chapters/04-11-intro-solid-state-physics.md) |

## Numbers to know

| Quantity | Value | Chapter |
|---|---|---|
| Breakdown fields | air ≈ 3 MV/m; thermal SiO₂ > 10 MV/cm | [04-02](../../courses/04-physics-for-ee/chapters/04-02-charge-coulomb-and-electric-fields.md) |
| Relative permittivity | SiO₂ 3.9; Si 11.7; HfO₂ ≈ 25; low-k 2.7–2.9 | [04-04](../../courses/04-physics-for-ee/chapters/04-04-potential-capacitance-and-dielectrics.md) |
| Copper | 1.68 µΩ·cm; $n = 8.49\times10^{28}$ m⁻³; $E_F$ ≈ 7.0 eV; $v_F$ ≈ 1.57×10⁶ m/s | [04-05](../../courses/04-physics-for-ee/chapters/04-05-current-resistance-and-conduction.md), [04-11](../../courses/04-physics-for-ee/chapters/04-11-intro-solid-state-physics.md) |
| Silicon mobilities | µₙ ≈ 1400, µₚ ≈ 470 cm²/V·s | [04-05](../../courses/04-physics-for-ee/chapters/04-05-current-resistance-and-conduction.md) |
| Field 1 cm from 1 A | 20 µT (Earth ≈ 50 µT) | [04-06](../../courses/04-physics-for-ee/chapters/04-06-magnetic-fields-and-forces.md) |
| Board delay | ≈ 7 ps/mm at $\varepsilon_r$ ≈ 4.6 | [04-08](../../courses/04-physics-for-ee/chapters/04-08-maxwell-preview.md) |
| Photon energies | 850 nm 1.46 eV; 1310 nm 0.95 eV; 1550 nm 0.80 eV; 13.5 nm 92 eV | [04-10](../../courses/04-physics-for-ee/chapters/04-10-intro-quantum-mechanics.md) |
| Band gaps (300 K) | Ge 0.66–0.67, Si 1.12, GaAs 1.42, 4H-SiC ≈ 3.2–3.26, GaN 3.4, SiO₂ ≈ 9 eV | [04-11](../../courses/04-physics-for-ee/chapters/04-11-intro-solid-state-physics.md) |

Perishable values (market sizes, product specifications, standards) are deliberately left off this sheet; they are dated and sourced in each chapter's Numbers to know and Practitioner lens sections.
