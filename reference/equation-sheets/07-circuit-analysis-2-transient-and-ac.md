# Equation Sheet · 07 Circuit Analysis II (Transient and AC)

The relations to know cold from Course 07, each with its conditions and the chapter that derives it.

Conventions:

- passive sign convention;
- node 0 is ground;
- sinusoids are cosines;
- a phasor $\mathbf{V} = V_m\angle\phi$ is the *peak* amplitude, and RMS phasors $\mathbf{V}_{rms} = \mathbf{V}/\sqrt2$ appear only in power work (mains and three-phase values are RMS);
- lg is $\log_{10}$.

## Capacitors and inductors

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $i = C\,dv/dt$, $v(t) = v(t_0) + \frac1C\int_{t_0}^ti\,d\xi$; $v = L\,di/dt$, $i(t) = i(t_0) + \frac1L\int_{t_0}^tv\,d\xi$ | Current into the + terminal | [07-01](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-01-capacitors-and-inductors.md) |
| $w_C = \tfrac12Cv^2$; $w_L = \tfrac12Li^2$ | Net energy over a periodic steady state is zero | [07-01](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-01-capacitors-and-inductors.md) |
| $v_C$ and $i_L$ are continuous; at DC, C is an open circuit and L a short | $i_C$, $v_L$ and resistor quantities can jump | [07-01](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-01-capacitors-and-inductors.md) |
| Parallel C add, series C combine reciprocally; inductors the other way round. Divider: $v_1 = v\,C_2/(C_1 + C_2)$ | Uncharged series capacitors share the same charge | [07-01](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-01-capacitors-and-inductors.md) |
| Interrupted inductor current: $v = L\,di/dt$ spike, so provide a flyback path | Clamp or snubber | [07-01](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-01-capacitors-and-inductors.md) |
| Real capacitor: ESR + ESL + C in series; $f_{SR} = 1/(2\pi\sqrt{L_{ESL}C})$, inductive above $f_{SR}$ | Class II ceramics lose capacitance under DC bias | [07-01](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-01-capacitors-and-inductors.md) |
| Decoupling: $C \ge \Delta I\,\Delta t/\Delta V$; ESL spike $L\,di/dt$; ESR step $\Delta I\cdot\text{ESR}$ | Parallel parts divide ESL and ESR | [07-01](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-01-capacitors-and-inductors.md) |

## First-order transients

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\tau = R_{Th}C$ or $L/R_{Th}$ | $R_{Th}$ seen by the storage element, independent sources off | [07-02](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md) |
| $x(t) = x(\infty) + [x(t_0^+) - x(\infty)]e^{-(t - t_0)/\tau}$ | Any variable, constant sources after $t_0$; recompute τ after each switching | [07-02](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md) |
| Time to reach a fraction: $t = \tau\ln[(x_0 - x_\infty)/(x - x_\infty)]$; 63.2% at τ, 99.3% at 5τ | | [07-02](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md) |
| $t_r$(10–90%) $= \tau\ln9 \approx 2.2\tau$; $f_{3dB} = 1/(2\pi\tau)$; $t_rf_{3dB} = \ln9/2\pi \approx 0.35$ | Exact for a single pole | [07-02](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md) |
| Settling to ½ LSB of an $N$-bit converter: $(N + 1)\tau\ln2$ | 12 bits: 9.0τ; 16 bits: 11.8τ | [07-02](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md) |
| Charging C to V from a fixed source loses $\tfrac12CV^2$ in the resistance, whatever $R$ | $P_{dyn} = \alpha CV_{DD}^2f$ (CMOS) | [07-02](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md) |
| $x(t) = x(0)e^{-t/\tau} + \frac1\tau\int_0^te^{-(t - \lambda)/\tau}u(\lambda)\,d\lambda$ | General input $u$ (convolution form) | [07-02](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md) |
| Integrator $v_{out} = -\frac{1}{RC}\int v_{in}\,dt$; differentiator $v_{out} = -RC\,dv_{in}/dt$ | Ideal op-amp | [07-02](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md) |

## Second-order transients

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Series RLC: $\alpha = R/2L$; parallel RLC: $\alpha = 1/(2RC)$; both $\omega_0 = 1/\sqrt{LC}$ | Characteristic equation $s^2 + 2\alpha s + \omega_0^2 = 0$ | [07-03](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-03-second-order-rlc-transients.md) |
| $\zeta = \alpha/\omega_0$, $Q = 1/(2\zeta)$; $Z_0 = \sqrt{L/C}$; series $Q = Z_0/R$, parallel $Q = R/Z_0$ | Critical damping: series $R = 2Z_0$, parallel $R = Z_0/2$ | [07-03](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-03-second-order-rlc-transients.md) |
| Roots $s = -\alpha \pm \sqrt{\alpha^2 - \omega_0^2}$: overdamped (ζ > 1), critical (ζ = 1), underdamped (ζ < 1, $\omega_d = \sqrt{\omega_0^2 - \alpha^2}$) | Every variable has the same roots | [07-03](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-03-second-order-rlc-transients.md) |
| Underdamped: $x = x(\infty) + e^{-\alpha t}\big(D\cos\omega_dt + \frac{\dot x(0^+) + \alpha D}{\omega_d}\sin\omega_dt\big)$, $D = x(0^+) - x(\infty)$ | Needs $x(0^+)$ and $\dot x(0^+)$ from the $0^+$ circuit | [07-03](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-03-second-order-rlc-transients.md) |
| Step from rest (all-pole): overshoot $e^{-\pi\zeta/\sqrt{1 - \zeta^2}}$ at $t_p = \pi/\omega_d$; ±2% settling ≈ $4/\alpha$ | 5% overshoot needs ζ = 0.690 | [07-03](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-03-second-order-rlc-transients.md) |
| Hot plug of an LC: $i_{pk} \approx V/Z_0$, capacitor overshoot up to nearly $2V$ | Light damping | [07-03](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-03-second-order-rlc-transients.md) |
| State form: $s^2 - (\operatorname{tr}\mathbf{A})s + \det\mathbf{A} = 0$, so $2\alpha = -\operatorname{tr}\mathbf{A}$ and $\omega_0^2 = \det\mathbf{A}$ | Any two-storage circuit | [07-03](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-03-second-order-rlc-transients.md) |
| RC damper across C: $R_d \approx Z_0$ with $C_d$ several times C, so $Q \approx 1$; loss up to $C_dV^2f_{sw}$ | Circuits of only R and C cannot ring | [07-03](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-03-second-order-rlc-transients.md) |

## Laplace-domain analysis

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $Z_R = R$; $Z_L = sL$ with a series source $Li(0^-)$ (or a parallel $i(0^-)/s$); $Z_C = 1/(sC)$ with a series source $v(0^-)/s$ (or a parallel $Cv(0^-)$) | Initial conditions become sources | [07-04](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-04-laplace-domain-circuit-analysis.md) |
| $H(s) = Y(s)/X(s)$ with zero initial conditions; $h(t) = \mathcal{L}^{-1}\{H\}$; $Y = HX$, i.e. $y = h * x$ | Response = zero-input + zero-state | [07-04](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-04-laplace-domain-circuit-analysis.md) |
| Poles: natural frequencies (denominator roots); zeros: transmission nulls | Stable if all poles have $\operatorname{Re}s < 0$ | [07-04](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-04-laplace-domain-circuit-analysis.md) |
| Residue $K_k = (s - p_k)F(s)\rvert_{s = p_k}$; a complex pair gives $2\lvert K\rvert e^{-\alpha t}\cos(\omega t + \angle K)$ | Simple poles | [07-04](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-04-laplace-domain-circuit-analysis.md) |
| $f(0^+) = \lim_{s\to\infty}sF(s)$; $f(\infty) = \lim_{s\to0}sF(s)$ | The final-value theorem needs all poles of $sF$ in the open left half-plane | [07-04](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-04-laplace-domain-circuit-analysis.md) |
| Sinusoidal steady state: $\lvert H(j\omega)\rvert$ and $\angle H(j\omega)$ | Stable $H$ | [07-04](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-04-laplace-domain-circuit-analysis.md) |

## Phasors and impedance

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $V_m\cos(\omega t + \phi) \leftrightarrow \mathbf{V} = V_m\angle\phi$; $d/dt \to j\omega$ | Single frequency, steady state | [07-05](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-05-sinusoidal-steady-state-and-impedance.md) |
| $Z_R = R$, $Z_L = j\omega L$, $Z_C = 1/(j\omega C) = -j/(\omega C)$; $Y = 1/Z = G + jB$ | KCL, KVL, nodal, mesh, superposition and Thévenin all carry over | [07-05](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-05-sinusoidal-steady-state-and-impedance.md) |
| Series to parallel: $R_p = R_s(1 + Q^2)$, $X_p = X_s(1 + 1/Q^2)$, $Q = X_s/R_s$ | Equivalent at one frequency | [07-05](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-05-sinusoidal-steady-state-and-impedance.md) |
| Sources at different frequencies: superpose in time, never add their phasors | | [07-05](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-05-sinusoidal-steady-state-and-impedance.md) |

## AC power

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $P = \tfrac12V_mI_m\cos\theta = V_{rms}I_{rms}\cos\theta$, θ = $\theta_v - \theta_i$ | Average power | [07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md) |
| RMS: sinusoid $X_m/\sqrt2$; square $A$; triangle $A/\sqrt3$; half-wave sine $A/2$; different frequencies add in quadrature | Crest factor = peak/RMS | [07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md) |
| $S = \mathbf{V}_{rms}\mathbf{I}_{rms}^* = \tfrac12\mathbf{V}\mathbf{I}^* = P + jQ$; $P = I_{rms}^2R$, $Q = I_{rms}^2X$ | $Q > 0$ inductive (lagging), $Q < 0$ capacitive | [07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md) |
| $I = P/(V\,\text{PF})$; line loss $\propto 1/\text{PF}^2$ | Ratings are in VA | [07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md) |
| Correction: $C = P(\tan\theta_1 - \tan\theta_2)/(\omega V_{rms}^2)$ | Shunt capacitor | [07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md) |
| $\text{PF} = \cos\phi_1/\sqrt{1 + \text{THD}^2}$, $\text{THD} = \sqrt{I_2^2 + I_3^2 + \cdots}/I_1$ | Sinusoidal voltage; capacitors cannot fix distortion | [07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md) |
| Maximum power: $Z_L = Z_{Th}^*$, $P_{max} = \lvert\mathbf{V}_{Th}\rvert^2/(8R_{Th}) = V_{Th,rms}^2/(4R_{Th})$ | Load free to choose | [07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md) |

## Frequency response and Bode plots

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Gain in dB $= 20\lg\lvert H\rvert$ (amplitude), $10\lg$ (power); 3.01 dB is √2 in amplitude, 6.02 dB is 2 | dBm referred to 1 mW | [07-07](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-07-frequency-response-and-bode-plots.md) |
| Real pole: −20 dB/decade, −3.01 dB and −45° at the corner, phase from $0.1\omega_c$ to $10\omega_c$; a zero is the mirror image | Right-half-plane zero: gain like a zero, phase like a pole | [07-07](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-07-frequency-response-and-bode-plots.md) |
| Second-order pair: −40 dB/decade; correction $20\lg Q$ at $\omega_0$; peak $1/(2\zeta\sqrt{1 - \zeta^2})$ at $\omega_0\sqrt{1 - 2\zeta^2}$ | Peak only for ζ < 0.707 | [07-07](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-07-frequency-response-and-bode-plots.md) |
| Closed-loop gain × bandwidth = GBW $= A_0f_1$; gain error ≈ $1/(A_0\beta)$ | Dominant-pole op-amp, non-inverting | [07-07](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-07-frequency-response-and-bode-plots.md) |
| Phase margin $= 180° + \angle T(j\omega_c)$ where $\lvert T(j\omega_c)\rvert = 1$, $T = A\beta$ | Two poles: 65.5° gives ζ = 0.707, 51.8° gives ζ = 0.5 | [07-07](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-07-frequency-response-and-bode-plots.md) |

## Resonance and filters

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\omega_0 = 1/\sqrt{LC}$; series $Q = \omega_0L/R = Z_0/R$; parallel $Q = R/(\omega_0L) = R/Z_0$; $\text{BW} = \omega_0/Q$ | $Q = 2\pi$ × (stored energy)/(energy lost per cycle) | [07-08](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md) |
| $\omega_{1,2} = \omega_0\big(\sqrt{1 + 1/4Q^2} \mp 1/2Q\big)$; $\omega_1\omega_2 = \omega_0^2$ | Half-power frequencies, geometric symmetry | [07-08](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md) |
| At series resonance $\lvert\mathbf{V}_L\rvert = \lvert\mathbf{V}_C\rvert = Q\lvert\mathbf{V}\rvert$; at parallel resonance the branch currents are $Q$ times the line current | Component ratings | [07-08](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md) |
| Butterworth: $\lvert H\rvert^2 = 1/[1 + (\omega/\omega_c)^{2n}]$; poles equally spaced on a circle; order $n \ge \lg(10^{A/10} - 1)/[2\lg(\omega_s/\omega_c)]$ | −20$n$ dB/decade; cascaded sections need different $Q$s | [07-08](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md) |
| Unity-gain Sallen–Key: $\omega_0 = 1/\sqrt{R_1R_2C_1C_2}$, $Q = \sqrt{R_1R_2C_1C_2}/[C_2(R_1 + R_2)]$; equal R: $Q = \tfrac12\sqrt{C_1/C_2}$ | $C_1$ to the output, $C_2$ to ground | [07-08](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md) |
| Equal-component Sallen–Key: $\omega_0 = 1/RC$, $Q = 1/(3 - K)$ | Sensitivity $KQ$ | [07-08](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md) |
| Insertion loss of a resonator: $-20\lg(1 - Q_L/Q_u)$ dB | Needs $Q_u \gg Q_L \approx f_0/B$ | [07-08](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md) |

## Coupled coils and transformers

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $v_1 = L_1\,di_1/dt \pm M\,di_2/dt$; $k = M/\sqrt{L_1L_2} \le 1$ | + when both currents enter dotted terminals | [07-09](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-09-mutual-inductance-and-transformers.md) |
| $w = \tfrac12L_1i_1^2 + \tfrac12L_2i_2^2 \pm Mi_1i_2$; series $L_1 + L_2 \pm 2M$ | Aiding (+) or opposing (−) | [07-09](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-09-mutual-inductance-and-transformers.md) |
| Reflected impedance $(\omega M)^2/(j\omega L_2 + Z_L)$; $Z_{in} = j\omega L_1 + (\omega M)^2/(j\omega L_2 + Z_L)$ | Inductive secondary reflects as capacitive | [07-09](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-09-mutual-inductance-and-transformers.md) |
| Ideal: $\mathbf{V}_1/\mathbf{V}_2 = N_1/N_2$, $\mathbf{I}_1/\mathbf{I}_2 = N_2/N_1$, $Z_{in} = (N_1/N_2)^2Z_L$ | $\mathbf{I}_2$ out of the secondary's dot | [07-09](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-09-mutual-inductance-and-transformers.md) |
| $V_{rms} = 4.443\,fNAB_m$ | Sinusoidal flux | [07-09](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-09-mutual-inductance-and-transformers.md) |
| Open-circuit test gives $R_c$, $X_m$; short-circuit test gives $R_{eq}$, $X_{eq}$ | Refer with $(N_1/N_2)^2$ | [07-09](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-09-mutual-inductance-and-transformers.md) |
| $\eta = xS\,\text{PF}/(xS\,\text{PF} + P_{core} + x^2P_{cu,FL})$, maximum at $x = \sqrt{P_{core}/P_{cu,FL}}$; regulation ≈ $I(R_{eq}\cos\theta + X_{eq}\sin\theta)/V$ | $x$ = load fraction, lagging θ | [07-09](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-09-mutual-inductance-and-transformers.md) |

## Two-port networks

| Relation | Conditions / notes | Chapter |
|---|---|---|
| z: $\mathbf{V} = \mathbf{z}\mathbf{I}$; y: $\mathbf{I} = \mathbf{y}\mathbf{V}$; h: $[\mathbf{V}_1, \mathbf{I}_2]^T = \mathbf{h}[\mathbf{I}_1, \mathbf{V}_2]^T$; ABCD: $[\mathbf{V}_1, \mathbf{I}_1]^T = [A\ B; C\ D][\mathbf{V}_2, -\mathbf{I}_2]^T$ | Port currents into the + terminals | [07-10](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-10-two-port-networks.md) |
| z by open-circuit tests, y by short-circuit tests; $A = z_{11}/z_{21}$, $B = \Delta_z/z_{21}$, $C = 1/z_{21}$, $D = z_{22}/z_{21}$ | A set may not exist (series Z has no z) | [07-10](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-10-two-port-networks.md) |
| Reciprocal: $z_{12} = z_{21}$, $y_{12} = y_{21}$, $h_{12} = -h_{21}$, $AD - BC = 1$; symmetric: $z_{11} = z_{22}$, $A = D$ | R, L, C, coupled coils, transformers are reciprocal | [07-10](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-10-two-port-networks.md) |
| Cascade: multiply ABCD; series: add z; parallel: add y | Series/parallel need the port condition to hold | [07-10](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-10-two-port-networks.md) |
| $Z_{in} = (AZ_L + B)/(CZ_L + D)$; $\mathbf{V}_2/\mathbf{V}_1 = Z_L/(AZ_L + B)$; $Y_{in} = y_{11} - y_{12}y_{21}/(y_{22} + Y_L)$ | Terminated two-port | [07-10](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-10-two-port-networks.md) |
| $\Gamma = (Z - Z_0)/(Z + Z_0)$; $S_{11} = (A + B/Z_0 - CZ_0 - D)/\Delta$, $S_{21} = 2/\Delta$, $\Delta = A + B/Z_0 + CZ_0 + D$ | Reference $Z_0$, usually 50 Ω | [07-10](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-10-two-port-networks.md) |
| Return loss $-20\lg\lvert S_{11}\rvert$; insertion loss $-20\lg\lvert S_{21}\rvert$; mismatch loss $-10\lg(1 - \lvert\Gamma\rvert^2)$; VSWR $(1 + \lvert\Gamma\rvert)/(1 - \lvert\Gamma\rvert)$ | Lossless: $\lvert S_{11}\rvert^2 + \lvert S_{21}\rvert^2 = 1$ | [07-10](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-10-two-port-networks.md) |
| L-section match: $Q = \sqrt{R_{high}/R_{low} - 1}$; series reactance $QR_{low}$, shunt reactance $R_{high}/Q$ | Shunt element on the high side (Problem 07-10.7) | [07-10](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-10-two-port-networks.md) |

## Three-phase circuits

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Y: $\mathbf{V}_{ab} = \sqrt3\mathbf{V}_{an}\angle30°$, $I_L = I_p$; Δ: $V_p = V_L$, $\mathbf{I}_a = \sqrt3\mathbf{I}_{ab}\angle{-30°}$ | Positive sequence (a, b, c) | [07-11](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-11-three-phase-circuits.md) |
| Balanced: solve one phase (per-phase Y equivalent); $Z_Y = Z_\Delta/3$ | Neutral carries no current | [07-11](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-11-three-phase-circuits.md) |
| $S = \sqrt3V_LI_L\angle\theta$, $P = \sqrt3V_LI_L\cos\theta$; instantaneous power constant, $3V_pI_p\cos\theta$ | θ is the load impedance angle | [07-11](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-11-three-phase-circuits.md) |
| Two wattmeters (currents in a and c, voltages to b): $P = W_1 + W_2$; balanced $W_1 = V_LI_L\cos(30° + \theta)$, $W_2 = V_LI_L\cos(30° - \theta)$, $Q = \sqrt3(W_2 - W_1)$ | $W_1 = 0$ at PF 0.5, negative below | [07-11](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-11-three-phase-circuits.md) |
| Correction capacitors: $C_Y = Q_{phase}/(\omega V_p^2)$, $C_\Delta = C_Y/3$ | Δ parts rated for $V_L$ | [07-11](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-11-three-phase-circuits.md) |
| Neutral current $\mathbf{I}_n = \mathbf{I}_a + \mathbf{I}_b + \mathbf{I}_c$; triplen harmonics add, $I_n = 3I_3$ | Four-wire unbalanced loads | [07-11](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-11-three-phase-circuits.md) |
