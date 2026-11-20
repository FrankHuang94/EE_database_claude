# Equation Sheet · 13 Electromagnetics

The relations to know cold from Course 13, each with its conditions and the chapter that derives it.

Conventions:

- $c$ = 2.998 × 10⁸ m/s, $\varepsilon_0$ = 8.854 × 10⁻¹² F/m, $\mu_0$ = 4π × 10⁻⁷ H/m, $\eta_0$ = 376.7 Ω;
- phasors use $e^{j\omega t}$ and peak amplitudes; a wave travelling in $+z$ varies as $e^{-\gamma z}$;
- decibels: power ratios $10\log_{10}$, field and voltage ratios $20\log_{10}$; dBi is gain relative to an isotropic antenna.

## Vector calculus

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\nabla f$, $\nabla\cdot\vec{A}$, $\nabla\times\vec{A}$ with scale factors $(1, 1, 1)$, $(1, \rho, 1)$, $(1, r, r\sin\theta)$ | Cartesian, cylindrical $(\rho, \phi, z)$, spherical $(r, \theta, \phi)$ | [13-01](../../courses/13-electromagnetics/chapters/13-01-vector-calculus-refresher.md) |
| Spherical $\nabla\cdot\vec{A} = \frac{1}{r^2}\frac{\partial(r^2A_r)}{\partial r} + \frac{1}{r\sin\theta}\frac{\partial(\sin\theta A_\theta)}{\partial\theta} + \frac{1}{r\sin\theta}\frac{\partial A_\phi}{\partial\phi}$; cylindrical $\nabla\cdot\vec{A} = \frac{1}{\rho}\frac{\partial(\rho A_\rho)}{\partial\rho} + \frac{1}{\rho}\frac{\partial A_\phi}{\partial\phi} + \frac{\partial A_z}{\partial z}$ | Radial fields: only the first term | [13-01](../../courses/13-electromagnetics/chapters/13-01-vector-calculus-refresher.md) |
| Divergence theorem $\oint_S\vec{A}\cdot d\vec{S} = \int_v\nabla\cdot\vec{A}\,dv$; Stokes $\oint_C\vec{A}\cdot d\vec\ell = \int_S(\nabla\times\vec{A})\cdot d\vec{S}$ | Closed surface; open surface with boundary $C$ (right-hand rule) | [13-01](../../courses/13-electromagnetics/chapters/13-01-vector-calculus-refresher.md) |
| $\nabla\times\nabla f = 0$, $\nabla\cdot\nabla\times\vec{A} = 0$, $\nabla\times\nabla\times\vec{A} = \nabla(\nabla\cdot\vec{A}) - \nabla^2\vec{A}$; $\nabla^2(1/r) = -4\pi\delta^3(\vec{r})$ | Identities behind potentials and waves | [13-01](../../courses/13-electromagnetics/chapters/13-01-vector-calculus-refresher.md) |

## Electrostatics

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\nabla\cdot\vec{D} = \rho_v$, $\nabla\times\vec{E} = 0$, $\vec{E} = -\nabla V$, $\vec{D} = \varepsilon\vec{E}$; Poisson $\nabla^2V = -\rho_v/\varepsilon$ | Linear, isotropic media | [13-02](../../courses/13-electromagnetics/chapters/13-02-electrostatics-boundary-value-problems.md) |
| Boundaries: $E_{t1} = E_{t2}$; $D_{n1} - D_{n2} = \rho_s$; at a conductor $E_t = 0$, $D_n = \rho_s$ | Normal from medium 2 into 1 | [13-02](../../courses/13-electromagnetics/chapters/13-02-electrostatics-boundary-value-problems.md) |
| Images: charge $q$ at height $d$ over a grounded plane → $-q$ at $-d$; force $q^2/[4\pi\varepsilon(2d)^2]$, attractive | Valid in the region above the plane only | [13-02](../../courses/13-electromagnetics/chapters/13-02-electrostatics-boundary-value-problems.md) |
| Parallel plates $C = \varepsilon A/d$; layers in series $C = A/\sum(d_i/\varepsilon_i)$; coax $C' = 2\pi\varepsilon/\ln(b/a)$, $E_{max} = V/[a\ln(b/a)]$ | Fringing neglected | [13-02](../../courses/13-electromagnetics/chapters/13-02-electrostatics-boundary-value-problems.md) |
| Two wires $C' = \pi\varepsilon/\cosh^{-1}(D/2a)$; wire over plane $C' = 2\pi\varepsilon/\cosh^{-1}(h/a)$ | Centre spacing $D$, height $h$ | [13-02](../../courses/13-electromagnetics/chapters/13-02-electrostatics-boundary-value-problems.md) |
| Energy $W = \tfrac12\int\vec{D}\cdot\vec{E}\,dv = \tfrac12CV^2$ |  | [13-02](../../courses/13-electromagnetics/chapters/13-02-electrostatics-boundary-value-problems.md) |

## Magnetostatics and inductance

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\nabla\cdot\vec{B} = 0$, $\nabla\times\vec{H} = \vec{J}$; Ampère $\oint\vec{H}\cdot d\vec\ell = I_{enc}$; $\vec{B} = \nabla\times\vec{A}$, $\nabla^2\vec{A} = -\mu\vec{J}$ | Coulomb gauge | [13-03](../../courses/13-electromagnetics/chapters/13-03-magnetostatics-and-inductance.md) |
| Biot–Savart $d\vec{B} = (\mu I/4\pi)\,d\vec\ell\times\hat{R}/R^2$; wire $B = \mu I/(2\pi\rho)$; loop centre $\mu I/(2a)$ |  | [13-03](../../courses/13-electromagnetics/chapters/13-03-magnetostatics-and-inductance.md) |
| Boundaries: $B_{n1} = B_{n2}$; $\hat{n}\times(\vec{H}_1 - \vec{H}_2) = \vec{K}$ |  | [13-03](../../courses/13-electromagnetics/chapters/13-03-magnetostatics-and-inductance.md) |
| $L = N\Phi/I = 2W_m/I^2$, $W_m = \tfrac12\int\vec{B}\cdot\vec{H}\,dv$; coax $L' = (\mu/2\pi)\ln(b/a)$ (external); two wires $L' = (\mu/\pi)\cosh^{-1}(D/2a)$ | Internal inductance of a round wire $\mu/(8\pi)$ at DC | [13-03](../../courses/13-electromagnetics/chapters/13-03-magnetostatics-and-inductance.md) |
| Magnetic circuit: $\mathcal{R} = \ell/(\mu A)$, $NI = \Phi\sum\mathcal{R}$, $L = N^2/\sum\mathcal{R}$; a gap of length $g$ acts like $\mu_rg$ of core | Fringing and leakage neglected | [13-03](../../courses/13-electromagnetics/chapters/13-03-magnetostatics-and-inductance.md) |
| Lossless line: $L'C' = \mu\varepsilon$ | TEM, homogeneous dielectric | [13-03](../../courses/13-electromagnetics/chapters/13-03-magnetostatics-and-inductance.md) |

## Maxwell's equations and plane waves

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\nabla\times\vec{E} = -\partial\vec{B}/\partial t$, $\nabla\times\vec{H} = \vec{J} + \partial\vec{D}/\partial t$, $\nabla\cdot\vec{D} = \rho_v$, $\nabla\cdot\vec{B} = 0$; continuity $\nabla\cdot\vec{J} = -\partial\rho_v/\partial t$ | Phasors: $\partial/\partial t \to j\omega$ | [13-04](../../courses/13-electromagnetics/chapters/13-04-maxwells-equations.md) |
| Conduction/displacement $\sigma/(\omega\varepsilon)$: ≫ 1 good conductor, ≪ 1 good dielectric; relaxation $\tau = \varepsilon/\sigma$; $\varepsilon_c = \varepsilon - j\sigma/\omega$, $\tan\delta = \sigma/(\omega\varepsilon)$ |  | [13-04](../../courses/13-electromagnetics/chapters/13-04-maxwells-equations.md) |
| Poynting $\vec{S} = \vec{E}\times\vec{H}$; time average $\tfrac12\operatorname{Re}(\tilde{\vec{E}}\times\tilde{\vec{H}}^*)$; plane wave $S_{av} = E_0^2/(2\eta)$ | Peak phasors | [13-04](../../courses/13-electromagnetics/chapters/13-04-maxwells-equations.md) |
| Lumped (circuit) model valid when the size is ≲ λ/10 (or delay ≪ rise time) |  | [13-04](../../courses/13-electromagnetics/chapters/13-04-maxwells-equations.md) |
| $k = \omega\sqrt{\mu\varepsilon}$, $v_p = 1/\sqrt{\mu\varepsilon} = c/n$, $\eta = \sqrt{\mu/\varepsilon} = \eta_0/n$, $\vec{H} = \hat{k}\times\vec{E}/\eta$ | Lossless; $\eta_0$ = 376.7 Ω | [13-05](../../courses/13-electromagnetics/chapters/13-05-plane-waves.md) |
| $\gamma = \alpha + j\beta = \sqrt{j\omega\mu(\sigma + j\omega\varepsilon)}$, $\eta_c = \sqrt{j\omega\mu/(\sigma + j\omega\varepsilon)}$; low loss: $\alpha \approx (\sigma/2)\eta$ | General medium | [13-05](../../courses/13-electromagnetics/chapters/13-05-plane-waves.md) |
| Good conductor: $\alpha = \beta = 1/\delta$, $\delta = 1/\sqrt{\pi f\mu\sigma}$, $\eta_c = (1 + j)/(\sigma\delta)$, $R_s = 1/(\sigma\delta)$; λ inside $= 2\pi\delta$; 8.686 dB per δ | Copper: δ = 66 µm at 1 MHz, 2.1 µm at 1 GHz | [13-05](../../courses/13-electromagnetics/chapters/13-05-plane-waves.md) |
| Round wire, $a \gg \delta$: $R_{ac}/R_{dc} \approx a/(2\delta)$ (exact adds about $\delta/2a$) | Current in the outer skin | [13-05](../../courses/13-electromagnetics/chapters/13-05-plane-waves.md) |
| Group velocity $v_g = d\omega/d\beta$; dispersion when $v_p$ depends on frequency |  | [13-05](../../courses/13-electromagnetics/chapters/13-05-plane-waves.md) |

## Reflection and transmission

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Normal incidence: $\Gamma = (\eta_2 - \eta_1)/(\eta_2 + \eta_1)$, $\tau = 1 + \Gamma$; power $\lvert\Gamma\rvert^2$ reflected, $\lvert\tau\rvert^2\eta_1/\eta_2$ transmitted | Lossless media | [13-06](../../courses/13-electromagnetics/chapters/13-06-reflection-and-transmission.md) |
| Quarter-wave layer (medium 1, layer 2, medium 3 behind): $\eta_{in} = \eta_2^2/\eta_3$; match with $\eta_2 = \sqrt{\eta_1\eta_3}$ ($n_2 = \sqrt{n_1n_3}$), thickness $\lambda_0/(4n_2)$; half-wave layer is transparent | At the design wavelength | [13-06](../../courses/13-electromagnetics/chapters/13-06-reflection-and-transmission.md) |
| Snell $n_1\sin\theta_i = n_2\sin\theta_t$; Fresnel $\Gamma_\perp = \frac{\eta_2\cos\theta_i - \eta_1\cos\theta_t}{\eta_2\cos\theta_i + \eta_1\cos\theta_t}$, $\Gamma_\parallel = \frac{\eta_2\cos\theta_t - \eta_1\cos\theta_i}{\eta_2\cos\theta_t + \eta_1\cos\theta_i}$ | Ulaby's sign convention for $\Gamma_\parallel$ | [13-06](../../courses/13-electromagnetics/chapters/13-06-reflection-and-transmission.md) |
| Critical angle $\sin\theta_c = n_2/n_1$ ($n_1 > n_2$), then $\lvert\Gamma\rvert = 1$; Brewster $\tan\theta_B = n_2/n_1$ (TM only, nonmagnetic) |  | [13-06](../../courses/13-electromagnetics/chapters/13-06-reflection-and-transmission.md) |
| Shielding (thick sheet): $SE \approx A + R$, $A = 8.686\,t/\delta$ dB, $R \approx 20\log_{10}[\eta_0/(4\lvert\eta_c\rvert)]$ dB | Far-field plane wave, $t \gg \delta$ | [13-06](../../courses/13-electromagnetics/chapters/13-06-reflection-and-transmission.md) |

## Transmission lines

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Telegrapher's: $\partial v/\partial z = -L'\partial i/\partial t$, $\partial i/\partial z = -C'\partial v/\partial t$; $Z_0 = \sqrt{L'/C'}$, $v_p = 1/\sqrt{L'C'}$ | Lossless | [13-07](../../courses/13-electromagnetics/chapters/13-07-transmission-lines-time-domain.md) |
| Launched wave $v^+ = V_sZ_0/(R_s + Z_0)$; $\Gamma = (Z - Z_0)/(Z + Z_0)$ at each end; final value = DC divider | Bounce diagram: round trip multiplies by $\Gamma_L\Gamma_S$ | [13-07](../../courses/13-electromagnetics/chapters/13-07-transmission-lines-time-domain.md) |
| Capacitive load: $v_L = 2v^+(1 - e^{-t/Z_0C})$; mid-line shunt $C$: $\tau = Z_0C/2$, dip area $-v^+Z_0C/2$; series $L$: $\tau = L/(2Z_0)$ | Ideal step | [13-07](../../courses/13-electromagnetics/chapters/13-07-transmission-lines-time-domain.md) |
| TDR: distance $= v_p t/2$; impedance from $\rho$: $Z = Z_0(1 + \rho)/(1 - \rho)$ |  | [13-07](../../courses/13-electromagnetics/chapters/13-07-transmission-lines-time-domain.md) |
| $\gamma = \sqrt{(R' + j\omega L')(G' + j\omega C')}$, $Z_0 = \sqrt{(R' + j\omega L')/(G' + j\omega C')}$; low loss $\alpha \approx R'/(2Z_0) + G'Z_0/2$ | Distortionless if $R'/L' = G'/C'$ | [13-08](../../courses/13-electromagnetics/chapters/13-08-transmission-lines-sinusoidal-steady-state.md) |
| $Z_{in} = Z_0\frac{Z_L + jZ_0\tan\beta\ell}{Z_0 + jZ_L\tan\beta\ell}$; $\Gamma(d) = \Gamma_Le^{-j2\beta d}$; λ/2 repeats, λ/4 inverts: $Z_0^2/Z_L$ | Lossless | [13-08](../../courses/13-electromagnetics/chapters/13-08-transmission-lines-sinusoidal-steady-state.md) |
| Short stub $jZ_0\tan\beta\ell$, open stub $-jZ_0\cot\beta\ell$ (short open stub ≈ $C'\ell$) |  | [13-08](../../courses/13-electromagnetics/chapters/13-08-transmission-lines-sinusoidal-steady-state.md) |
| VSWR $= (1 + \lvert\Gamma\rvert)/(1 - \lvert\Gamma\rvert)$; RL $= -20\log_{10}\lvert\Gamma\rvert$; ML $= -10\log_{10}(1 - \lvert\Gamma\rvert^2)$; $V_{max}$ where $\angle\Gamma(d) = 0$, $V_{min}$ λ/4 away |  | [13-08](../../courses/13-electromagnetics/chapters/13-08-transmission-lines-sinusoidal-steady-state.md) |
| Quarter-wave transformer $Z_1 = \sqrt{Z_0R_L}$ | Real load; narrowband | [13-08](../../courses/13-electromagnetics/chapters/13-08-transmission-lines-sinusoidal-steady-state.md) |

## Smith chart and matching

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $z = Z/Z_0 = (1 + \Gamma)/(1 - \Gamma)$; constant-$r$ circles centre $r/(1 + r)$, radius $1/(1 + r)$; constant-$x$ circles centre $(1, 1/x)$, radius $1/\lvert x\rvert$ | Moving toward the generator rotates clockwise, once per λ/2 | [13-09](../../courses/13-electromagnetics/chapters/13-09-smith-chart-and-matching.md) |
| L-network: $Q = \sqrt{R_{high}/R_{low} - 1}$, series $X = QR_{low}$, shunt $B = Q/R_{high}$; bandwidth roughly $\propto 1/Q$ | Shunt element on the high side | [13-09](../../courses/13-electromagnetics/chapters/13-09-smith-chart-and-matching.md) |
| Bode–Fano (parallel RC load): $\int_0^\infty\ln(1/\lvert\Gamma\rvert)\,d\omega \le \pi/(RC)$ | Limit for any lossless match | [13-09](../../courses/13-electromagnetics/chapters/13-09-smith-chart-and-matching.md) |
| Conjugate match $Z_S = Z_L^*$ maximizes power; noise match $\Gamma_{opt}$ differs |  | [13-09](../../courses/13-electromagnetics/chapters/13-09-smith-chart-and-matching.md) |

## Waveguides, cavities and fibre

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Rectangular guide $f_{c,mn} = \frac{c}{2}\sqrt{(m/a)^2 + (n/b)^2}$; TE₁₀ $f_c = c/(2a)$ | Air-filled; divide by $\sqrt{\varepsilon_r}$ if filled | [13-10](../../courses/13-electromagnetics/chapters/13-10-waveguides-and-resonators.md) |
| $\beta = k\sqrt{1 - (f_c/f)^2}$, $\lambda_g = \lambda/\sqrt{1 - (f_c/f)^2}$, $v_pv_g = c^2$ (air-filled; $1/(\mu\varepsilon)$ in general), $Z_{TE} = \eta/\sqrt{1 - (f_c/f)^2}$, $Z_{TM} = \eta\sqrt{1 - (f_c/f)^2}$ | Above cutoff | [13-10](../../courses/13-electromagnetics/chapters/13-10-waveguides-and-resonators.md) |
| Below cutoff: $\alpha = \sqrt{k_c^2 - k^2} \approx k_c$; TE₁₀ power $P = E_0^2ab/(4Z_{TE})$ |  | [13-10](../../courses/13-electromagnetics/chapters/13-10-waveguides-and-resonators.md) |
| Cavity $f_{mn\ell} = \frac{c}{2}\sqrt{(m/a)^2 + (n/b)^2 + (\ell/d)^2}$; $Q = \omega_0W/P_{loss}$; $1/Q_L = 1/Q_0 + 1/Q_e$ | Critical coupling: $Q_L = Q_0/2$ | [13-10](../../courses/13-electromagnetics/chapters/13-10-waveguides-and-resonators.md) |
| Fibre: $\text{NA} = \sqrt{n_1^2 - n_2^2}$, $V = (2\pi a/\lambda)\text{NA}$; single-mode for $V < 2.405$; about $V^2/2$ modes for large $V$ | Step index, weak guidance | [13-10](../../courses/13-electromagnetics/chapters/13-10-waveguides-and-resonators.md) |

## Radiation and antennas

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Hertzian dipole far field $E_\theta = j\eta kI\ell\sin\theta\,e^{-jkr}/(4\pi r)$, $H_\phi = E_\theta/\eta$; near-field terms grow as $1/(kr)^2$ | Uniform current, $\ell \ll \lambda$ | [13-11](../../courses/13-electromagnetics/chapters/13-11-radiation-and-antennas.md) |
| $R_{rad} = (2\pi\eta_0/3)(\ell/\lambda)^2 \approx 789(\ell/\lambda)^2$ Ω; $D = 1.5$ | Triangular current (real short dipole): ¼ of this | [13-11](../../courses/13-electromagnetics/chapters/13-11-radiation-and-antennas.md) |
| Half-wave dipole $R_{rad}$ = 73.1 Ω, $D$ = 1.64 (2.15 dBi) |  | [13-11](../../courses/13-electromagnetics/chapters/13-11-radiation-and-antennas.md) |
| $D = 4\pi U_{max}/P_{rad}$; $G = e_rD$, $e_r = R_{rad}/(R_{rad} + R_{loss})$; EIRP $= P_tG_t$ |  | [13-11](../../courses/13-electromagnetics/chapters/13-11-radiation-and-antennas.md) |
| $A_e = G\lambda^2/(4\pi)$; Friis $P_r = P_tG_tG_r[\lambda/(4\pi R)]^2$; FSPL $= 20\log_{10}(4\pi R/\lambda)$ dB | Far field, matched, co-polarized | [13-11](../../courses/13-electromagnetics/chapters/13-11-radiation-and-antennas.md) |
| Far field beyond $2D_a^2/\lambda$ (aperture size $D_a$) |  | [13-11](../../courses/13-electromagnetics/chapters/13-11-radiation-and-antennas.md) |
| Array factor $\text{AF} = \sum_ne^{jn(kd\sin\theta + \beta)}$, $\lvert\text{AF}\rvert = \lvert\sin(N\psi/2)/\sin(\psi/2)\rvert$; steering $\beta = -kd\sin\theta_0$; no grating lobes for $d < \lambda/(1 + \lvert\sin\theta_{max}\rvert)$ | Pattern = element pattern × AF | [13-11](../../courses/13-electromagnetics/chapters/13-11-radiation-and-antennas.md) |
| $N$ coherent elements: array gain $N$, EIRP $\propto N^2$ | Equal power per element | [13-11](../../courses/13-electromagnetics/chapters/13-11-radiation-and-antennas.md) |
