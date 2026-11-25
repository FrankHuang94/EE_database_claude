# Equation Sheet · 22 Power Electronics and Energy Conversion

The relations to know cold from Course 22, each with its conditions and the chapter that derives it.

Conventions:

- converters are in periodic steady state; $D$ is the main switch's duty cycle and $D' = 1 - D$; $T_s = 1/f_s$; ripples written Δ are peak-to-peak; $R$ is the load resistance unless a subscript says otherwise;
- in the converter chapters, $V$ and $I$ are the DC output voltage and current, $V_{in}$ or $V_g$ the input, and $I_L$ the inductor's average current; the small-ripple approximation holds unless stated;
- turns ratios are $n = N_1/N_2$ (primary over secondary);
- symbols reused between chapters: $k$ is the type-III placement factor (22-07), a Steinmetz coefficient (22-05), a motor constant (22-11) or a temperature coefficient (22-06); $K = 2L/(RT_s)$ is the conduction parameter (22-02, 22-03); $R$ is also a governor droop (22-12); $Q$ is a quality factor, a charge or a cell's capacity, by context; $z$ is state of charge;
- three-phase voltages are line-to-line RMS and powers are three-phase totals unless "per phase" is written; per-unit quantities sit on stated bases.

## Conversion principles

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $P_{loss} = P_{out}(1 - \eta)/\eta$; $dP_{loss}/d\eta = -P_{out}/\eta^2$ | Near 100%, each point of efficiency is worth about 1% of $P_{out}$ | [22-01](../../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md) |
| $\eta_{chain} = \prod\eta_k$ | Stages in series | [22-01](../../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md) |
| $\eta_{LDO} = V_{out}I_{out}/[V_{in}(I_{out} + I_Q)] \le V_{out}/V_{in}$ | Linear regulator | [22-01](../../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md) |
| $\langle v_{sw}\rangle = DV_{in}$; harmonics $\dfrac{2V_{in}}{n\pi}\sin(n\pi D)$ | Switch-node square wave; an LC filter keeps the average | [22-01](../../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md) |
| $E_R = \tfrac12CV^2$ charging $C$ from a step $V$ through any $R$; sharing $E = \tfrac12\dfrac{C_1C_2}{C_1 + C_2}(V_1 - V_2)^2$ | Why switches must not short capacitors; $N$ steps lose $\tfrac12CV^2/N$ | [22-01](../../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md) |
| $P_{loss} = P_0 + aI + RI^2$; peak efficiency at $I^* = \sqrt{P_0/R}$ | Fixed, proportional and conduction loss | [22-01](../../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md) |
| $N \to N + 1$ phases above $I = \sqrt{N(N + 1)P_0/R}$ | Phase shedding; $R$ per phase | [22-01](../../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md) |
| $\rho = P_{out}/\text{Vol} \le q\,\eta/(1 - \eta)$ | $q$ = heat rejected per unit volume | [22-01](../../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md) |
| $C = 2P_{bus}t_{hold}/(V_1^2 - V_2^2)$ | Hold-up from $V_1$ down to $V_2$ | [22-01](../../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md) |

## The buck converter

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\langle v_L\rangle = 0$, $\langle i_C\rangle = 0$ | Volt-second and charge balance | [22-02](../../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md) |
| $V = DV_{in}$ | CCM | [22-02](../../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md) |
| $\Delta i_L = V(1 - D)/(f_sL)$; $\Delta v_C = \Delta i_L/(8f_sC)$; ESR adds $\Delta i_L R_{ESR}$ | The ESR and capacitive terms peak at different times | [22-02](../../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md) |
| $I_{L,rms} = I\sqrt{1 + r^2/12}$, $r = \Delta i_L/I$; $I_{HS} = \sqrt D\,I_{L,rms}$, $I_{LS} = \sqrt{D'}\,I_{L,rms}$ | RMS ratings | [22-02](../../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md) |
| $I_{C_{in},rms} = I\sqrt{D(1 - D) + Dr^2/12} \approx I\sqrt{D(1 - D)}$ | Worst at $D$ = 0.5 | [22-02](../../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md) |
| $V = DV_{in} - IR_{eq}$, $R_{eq} = DR_{HS} + D'R_{LS} + R_L$; $\eta = 1/(1 + R_{eq}/R)$ | Conduction losses | [22-02](../../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md) |
| Diode rectifier: $V = DV_{in} - D'V_F - I(DR_{HS} + R_L)$, $P_{diode} \approx D'V_FI$ | Non-synchronous | [22-02](../../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md) |
| $I_{crit} = \Delta i_L/2$; $K = 2L/(RT_s)$, CCM if $K > K_{crit} = 1 - D$ | CCM/DCM boundary | [22-02](../../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md) |
| DCM: $M = 2/(1 + \sqrt{1 + 4K/D_1^2})$; $D_2 = D_1(V_{in} - V)/V$ | Gain depends on load | [22-02](../../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md) |
| PFM pulse charge $Q = \tfrac12i_{pk}T_{on}V_{in}/V$ | Pulse-frequency mode | [22-02](../../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md) |

## Boost, buck-boost and other topologies

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Boost: $V = V_{in}/D'$, $I_L = I/D'$, $\Delta i_L = V_{in}DT_s/L$, $\Delta v = ID/(f_sC)$ | CCM | [22-03](../../courses/22-power-electronics-and-energy-conversion/chapters/22-03-boost-buck-boost-topologies.md) |
| $V/V_{in} = \dfrac{1}{D'}\cdot\dfrac{1}{1 + R_L/(D'^2R)}$; $\eta = 1/(1 + R_L/(D'^2R))$ | Boost with inductor resistance $R_L$ | [22-03](../../courses/22-power-electronics-and-energy-conversion/chapters/22-03-boost-buck-boost-topologies.md) |
| $M_{max} = \tfrac12\sqrt{R/R_L}$ at $D' = \sqrt{R_L/R}$ | Beyond it the gain falls | [22-03](../../courses/22-power-electronics-and-energy-conversion/chapters/22-03-boost-buck-boost-topologies.md) |
| Buck-boost: $V = -(D/D')V_{in}$; switch and diode block $V_{in} + \lvert V\rvert$; $I_L = I/D'$ | Inverting | [22-03](../../courses/22-power-electronics-and-energy-conversion/chapters/22-03-boost-buck-boost-topologies.md) |
| Ćuk: $V = -(D/D')V_{in}$; SEPIC: $V = (D/D')V_{in}$ | Capacitor-coupled | [22-03](../../courses/22-power-electronics-and-energy-conversion/chapters/22-03-boost-buck-boost-topologies.md) |
| Boost DCM: $M = \tfrac12\left(1 + \sqrt{1 + 4D^2/K}\right)$; CCM if $K > K_{crit} = DD'^2$ | Light load | [22-03](../../courses/22-power-electronics-and-energy-conversion/chapters/22-03-boost-buck-boost-topologies.md) |

## Isolated converters

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\Delta B = V_{in}DT_s/(N_1A_e)$ | Volt-seconds on a winding set the flux swing | [22-04](../../courses/22-power-electronics-and-energy-conversion/chapters/22-04-isolated-converters.md) |
| Flyback: $V = (V_{in}/n)\,D/D'$; $V_{DS,off} = V_{in} + nV$ (plus the leakage spike) | CCM | [22-04](../../courses/22-power-electronics-and-energy-conversion/chapters/22-04-isolated-converters.md) |
| DCM flyback: $P = \tfrac12L_mI_{pk}^2f_s$ | Energy per cycle | [22-04](../../courses/22-power-electronics-and-energy-conversion/chapters/22-04-isolated-converters.md) |
| Clamp: $t_c = L_{lk}I_{pk}/(V_c - V_R)$, $E_c = \tfrac12L_{lk}I_{pk}^2\,V_c/(V_c - V_R)$ | $V_R = nV$; $V_c$ above the input | [22-04](../../courses/22-power-electronics-and-energy-conversion/chapters/22-04-isolated-converters.md) |
| Forward: $V = DV_{in}/n$; $D_{max} = 1/(1 + N_3/N_1)$; $V_{DS,off} = V_{in}(1 + N_1/N_3)$ | Reset winding $N_3$; $2V_{in}$ and 0.5 for $N_3 = N_1$ | [22-04](../../courses/22-power-electronics-and-energy-conversion/chapters/22-04-isolated-converters.md) |
| Reset needs $V_{in}D = V_{in}(N_1/N_3)D_r$ | Volt-second balance of $L_m$ | [22-04](../../courses/22-power-electronics-and-energy-conversion/chapters/22-04-isolated-converters.md) |

## Magnetics

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $NI = \Phi(\mathcal R_c + \mathcal R_g)$, $\mathcal R = \ell/(\mu A)$; $L = N^2/(\mathcal R_c + \mathcal R_g) = \mu_0N^2A_e/(g + \ell_e/\mu_r)$ | Gapped core | [22-05](../../courses/22-power-electronics-and-energy-conversion/chapters/22-05-magnetics-design.md) |
| $\mu_e = \mu_r/(1 + \mu_rg/\ell_e)$; $B = LI/(NA_e)$ | Effective permeability; flux density | [22-05](../../courses/22-power-electronics-and-energy-conversion/chapters/22-05-magnetics-design.md) |
| $W = \dfrac{B^2}{2\mu_0}A_e(g + \ell_e/\mu_r)$; gap share $g/(g + \ell_e/\mu_r)$ | The gap stores the energy | [22-05](../../courses/22-power-electronics-and-energy-conversion/chapters/22-05-magnetics-design.md) |
| $N = LI_{pk}/(B_{max}A_e)$, $g = \mu_0N^2A_e/L - \ell_e/\mu_r$ | Inductor design | [22-05](../../courses/22-power-electronics-and-energy-conversion/chapters/22-05-magnetics-design.md) |
| $p_{eddy} = \pi^2f^2B_{pk}^2t^2/(6\rho)$ | Lamination of thickness $t$, sinusoid | [22-05](../../courses/22-power-electronics-and-energy-conversion/chapters/22-05-magnetics-design.md) |
| Steinmetz $P_v = kf^\alpha B_{pk}^\beta$; iGSE triangle $P_v = k_i(\Delta B)^\beta f^\alpha[D^{1 - \alpha} + D'^{1 - \alpha}]$ | $k_i = k/[(2\pi)^{\alpha - 1}\int_0^{2\pi}\lvert\cos\theta\rvert^\alpha2^{\beta - \alpha}d\theta]$ | [22-05](../../courses/22-power-electronics-and-energy-conversion/chapters/22-05-magnetics-design.md) |
| $R_{dc} = \rho N\,\text{MLT}/A_w$; $\delta = \sqrt{\rho/(\pi f\mu_0)}$ | Copper: 17.24 nΩ·m at 20 °C, +0.393%/K | [22-05](../../courses/22-power-electronics-and-energy-conversion/chapters/22-05-magnetics-design.md) |
| Dowell: $F_R = \Delta\left[\dfrac{\sinh2\Delta + \sin2\Delta}{\cosh2\Delta - \cos2\Delta} + \dfrac{2(M^2 - 1)}{3}\cdot\dfrac{\sinh\Delta - \sin\Delta}{\cosh\Delta + \cos\Delta}\right] \approx 1 + \dfrac{5M^2 - 1}{45}\Delta^4$ | $\Delta$ = layer thickness/δ, $M$ layers; approximation for small Δ | [22-05](../../courses/22-power-electronics-and-energy-conversion/chapters/22-05-magnetics-design.md) |
| $A_p = A_eW_A \ge LI_{pk}I_{rms}/(K_uJB_{max})$; $K_g = A_e^2W_A/\text{MLT} \ge \rho L^2I_{pk}^2I_{rms}^2/(B_{max}^2P_{cu}K_u)$ | Area product; core geometry | [22-05](../../courses/22-power-electronics-and-energy-conversion/chapters/22-05-magnetics-design.md) |
| $\Delta B_{opt} = (2b/(\beta a))^{1/(\beta + 2)}$, $P_{fe}/P_{cu} = 2/\beta$ | $P_{fe} = a\Delta B^\beta$, $P_{cu} = b/\Delta B^2$ | [22-05](../../courses/22-power-electronics-and-energy-conversion/chapters/22-05-magnetics-design.md) |
| $L_{lk} = \dfrac{\mu_0N^2\,\text{MLT}}{b_w}\left(\dfrac{h_p}{3} + d + \dfrac{h_s}{3}\right)$; interleaved: $h/12$ and $d/2$ | Leakage of a two-winding stack | [22-05](../../courses/22-power-electronics-and-energy-conversion/chapters/22-05-magnetics-design.md) |

## Switching losses and wide-bandgap devices

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $P_{ov} = \tfrac12VI(t_{on} + t_{off})f_s$ | Hard switching, linear ramps | [22-06](../../courses/22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md) |
| Hard turn-on: $E_{C,on} = Q_{oss}V$ (not $E_{oss}$) | Half bridge: own $E_{oss}$ plus the partner's charging loss | [22-06](../../courses/22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md) |
| $E_{rr} \approx Q_{rr}V$ | Body-diode recovery; zero for GaN | [22-06](../../courses/22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md) |
| $P_g = Q_gV_{drv}f_s$; dead time $2V_{SD}It_df_s$ | Gate drive; reverse conduction | [22-06](../../courses/22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md) |
| $P(R) = I_{rms}^2R + (RQ)V_{drv}f_s/R$; $R^* = \sqrt{(RQ)V_{drv}f_s}/I_{rms}$, $P_{min} = 2I_{rms}\sqrt{(RQ)V_{drv}f_s}$ | Device size; same form with $R\cdot Q_{oss}$ and $V$ | [22-06](../../courses/22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md) |
| $T_j = \dfrac{T_a + R_{th}I^2R_{25}(1 - 25k)}{1 - R_{th}I^2R_{25}k}$ | $R(T) = R_{25}[1 + k(T - 25)]$; runaway when the denominator reaches 0 | [22-06](../../courses/22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md) |
| ZVS: $t_{tr} = 2Q_{oss}/I = 2C_{o(tr)}V/I \le t_d$, so $I \ge 2Q_{oss}/t_d$ | Inductor current swings the node | [22-06](../../courses/22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md) |
| LLC half bridge: $I_{m,pk} = V/(8L_mf_s)$; $f_r = 1/(2\pi\sqrt{L_rC_r})$ | ZVS from magnetizing current | [22-06](../../courses/22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md) |

## Converter dynamics and control

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Buck: $G_{vd} = \dfrac{V_g}{1 + sL/R + s^2LC}$, $G_{vg} = \dfrac{D}{1 + sL/R + s^2LC}$, $Z_{out} = \dfrac{sL}{1 + sL/R + s^2LC}$ | Averaged, linearized; $f_0 = 1/(2\pi\sqrt{LC})$, $Q = R\sqrt{C/L}$ | [22-07](../../courses/22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md) |
| Boost: $G_{vd} = \dfrac{V}{D'}\cdot\dfrac{1 - sL/(D'^2R)}{1 + sL/(D'^2R) + s^2LC/D'^2}$ | RHP zero at $D'^2R/(2\pi L)$; $f_0 = D'/(2\pi\sqrt{LC})$ | [22-07](../../courses/22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md) |
| $T(s) = G_c(s)\,G_{vd}(s)\,H/V_M$; PM $= 180° + \angle T(j\omega_c)$ | Voltage mode | [22-07](../../courses/22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md) |
| Type III: $G_c = \dfrac{\omega_I}{s}\cdot\dfrac{(1 + s/\omega_z)^2}{(1 + s/\omega_p)^2}$; $B = \text{PM} - 90° - \varphi_p$, $k = \tan\!\left(\dfrac{B/2 + 90°}{2}\right)$ | Zeros at $f_c/k$, poles at $kf_c$; $\lvert G_c(j\omega_c)\rvert = (\omega_I/\omega_c)k^2$ | [22-07](../../courses/22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md) |
| Op-amp network: $\omega_I = 1/(R_1(C_1 + C_2))$; zeros $1/(R_2C_1)$, $1/((R_1 + R_3)C_3)$; poles $(C_1 + C_2)/(R_2C_1C_2)$, $1/(R_3C_3)$ | Realization | [22-07](../../courses/22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md) |
| Peak current mode: $\alpha = -(m_2 - m_a)/(m_1 + m_a)$; stable if $\lvert\alpha\rvert < 1$ | Subharmonic instability above $D$ = 0.5 without $m_a$ | [22-07](../../courses/22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md) |
| $G_{vc} \approx (R/R_i)/(1 + sRC)$ | Current mode: one pole | [22-07](../../courses/22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md) |
| $\Delta V \approx \Delta I/(2\pi f_cC)$; delay phase $\varphi_d = 360°f_ct_d$ | Load step; digital control | [22-07](../../courses/22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md) |

## PMICs

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\eta_{chain} = \eta_{buck}V_{out}/V_{mid}$ | Buck then LDO | [22-08](../../courses/22-power-electronics-and-energy-conversion/chapters/22-08-pmics.md) |
| $P_{PWM} = P_f + RI^2$, $P_{PFM} = V_{in}I_q + \alpha I + R_pI^2$ | Mode crossover where they are equal | [22-08](../../courses/22-power-electronics-and-energy-conversion/chapters/22-08-pmics.md) |
| $E_{day} = \sum_iP_it_i/\eta_i + V_{bat}I_qT_{day}$ | Battery life = usable energy / $E_{day}$ | [22-08](../../courses/22-power-electronics-and-energy-conversion/chapters/22-08-pmics.md) |
| DVS: $I_C = CS$ for slew $S$; tracking lead $e_{ramp} = (S/\omega_I)(1 - V_M/V_g)$ | Up-ramp; type-III loop | [22-08](../../courses/22-power-electronics-and-energy-conversion/chapters/22-08-pmics.md) |
| AVS saving $1 - (V_2/V_1)^2$ | Dynamic power $\propto V^2$ at fixed $f$ | [22-08](../../courses/22-power-electronics-and-energy-conversion/chapters/22-08-pmics.md) |
| Soft start dissipates $\tfrac12CV^2$ whatever the ramp; gating break-even $t_{be} = (CV^2 + E_{state})/P_{leak}$ | Power gating | [22-08](../../courses/22-power-electronics-and-energy-conversion/chapters/22-08-pmics.md) |

## Batteries, charging and fuel gauging

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $E = -\Delta G/(nF)$; $q_{th} = F/(3.6M)$ mAh/g | Cell voltage; capacity per mole of Li stored | [22-09](../../courses/22-power-electronics-and-energy-conversion/chapters/22-09-batteries-charging-fuel-gauging.md) |
| $dz/dt = -i/Q$; $v = V_{OC}(z) - iR_0 - v_1$ | Equivalent-circuit model, one RC pair | [22-09](../../courses/22-power-electronics-and-energy-conversion/chapters/22-09-batteries-charging-fuel-gauging.md) |
| Pulse: $v(t) = V_{OC} - IR_0 - IR_1(1 - e^{-t/\tau_1})$ | Constant-current step | [22-09](../../courses/22-power-electronics-and-energy-conversion/chapters/22-09-batteries-charging-fuel-gauging.md) |
| $I_{max} = (V_{OC}(z) - V_{cut})/R$; usable end $V_{OC}(z_{end}) = V_{cut} + IR$ | Rate and temperature shrink usable capacity | [22-09](../../courses/22-power-electronics-and-energy-conversion/chapters/22-09-batteries-charging-fuel-gauging.md) |
| CC/CV: $V_{OC}(z_{cv}) = V_{max} - I_{cc}R$; $i(t) = I_{cc}e^{-t/(RC_{eff})}$; $t_{cv} = RC_{eff}\ln(I_{cc}/I_{term})$ | $C_{eff} = Q/(dV_{OC}/dz)$ | [22-09](../../courses/22-power-electronics-and-energy-conversion/chapters/22-09-batteries-charging-fuel-gauging.md) |
| Coulomb counting $z = z_0 - \frac1Q\int i\,dt$; capacity learning $Q_{max} = \Delta q/(z_1 - z_2)$ | SOC anchors from rest OCV | [22-09](../../courses/22-power-electronics-and-energy-conversion/chapters/22-09-batteries-charging-fuel-gauging.md) |
| SEI growth $L = \sqrt{2D't}$ | Diffusion-limited calendar fade | [22-09](../../courses/22-power-electronics-and-energy-conversion/chapters/22-09-batteries-charging-fuel-gauging.md) |
| $T_{life} = Q_{rated}f_{age}f_{temp}f_{cut}/I_{avg}$ | Derated battery life | [22-09](../../courses/22-power-electronics-and-energy-conversion/chapters/22-09-batteries-charging-fuel-gauging.md) |

## Datacenter power delivery

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $P_{in} = P_{chip}/\prod\eta_i$; facility power = $P_{in}\times$ PUE | Grid to transistor | [22-10](../../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md) |
| $P_{loss} = I^2R = P^2R/V^2$; uniform taps: $I^2(2R)/3$ | $R$ one way; $2R$ the loop | [22-10](../../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md) |
| $\dfrac{P_{DC}/2}{P_{AC}/n_c} = \dfrac{n_cV_{DC}}{2\sqrt3V_{LL}\cos\varphi}$ | Power per conductor of equal rating | [22-10](../../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md) |
| $\Delta I_\Sigma = \dfrac{V_{in}T}{L}\cdot\dfrac{(ND - m)(m + 1 - ND)}{N}$, $m = \lfloor ND\rfloor$ | Interleaved buck; ripple at $Nf_s$, zero when $ND$ is an integer | [22-10](../../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md) |
| Slew $N(V_{in} - V_o)/L$ | All phases on | [22-10](../../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md) |
| $V_{out} = V_{ID} - R_{LL}I_{out}$; $Z_t = \Delta V_{allowed}/\Delta I_{max}$ | Load line; target impedance | [22-10](../../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md) |
| $f_0 = 1/(2\pi\sqrt{LC})$, $Z_0 = \sqrt{L/C}$; first droop $\Delta I\sqrt{L/C}$; damping ESR $\approx Z_0/2$ | Package inductance into die capacitance | [22-10](../../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md) |
| $R_{sq} = \rho/t$; plane resistance $R_{sq}\times$ length/width | Lateral delivery | [22-10](../../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md) |
| Storage $\tfrac12C(V_1^2 - V_2^2)$ | Capacitor bank between $V_1$ and $V_2$ | [22-10](../../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md) |

## Electric machines and drives

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $e = B\ell v$, $F = Bi\ell$; $ei = T\omega$ | Conductor moving at $v$ in a field | [22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md) |
| DC: $E_a = K\Phi\omega$, $T = K\Phi I_a$, $V = E_a + I_aR_a$; $\omega = V/k - (R_a/k^2)T$ | PM machine $k = K\Phi$ | [22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md) |
| Rotating field $\tfrac32B_m\cos(\theta - \omega t)$; $n_s = 120f/P$ rpm | Three windings 120° apart; $P$ poles | [22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md) |
| $s = (n_s - n)/n_s$; rotor frequency $sf$ | Slip | [22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md) |
| $P_{ag} = 3I_2^2R_2/s$; rotor copper $sP_{ag}$; $P_{mech} = (1 - s)P_{ag}$; $T = P_{ag}/\omega_s$ | Air-gap power split | [22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md) |
| $T(s) = \dfrac{3V_{th}^2(R_2/s)}{\omega_s[(R_{th} + R_2/s)^2 + (X_{th} + X_2)^2]}$ | Thevenin of the stator and magnetizing branch | [22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md) |
| $s_{max} = \dfrac{R_2}{\sqrt{R_{th}^2 + (X_{th} + X_2)^2}}$, $T_{max} = \dfrac{3V_{th}^2}{2\omega_s[R_{th} + \sqrt{R_{th}^2 + (X_{th} + X_2)^2}]}$ | $T_{max}$ does not depend on $R_2$ | [22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md) |
| $P = 3VE_f\sin\delta/X_s$; $\mathbf V = \mathbf E_f + jX_s\mathbf I_a$ | Synchronous motor, per-phase $V$ and $E_f$ | [22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md) |
| $V \approx 4.44fN\Phi$: constant $V/f$ keeps the flux | Below base speed | [22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md) |
| SPWM $V_{LL,rms} = \dfrac{\sqrt3}{2\sqrt2}mV_{dc} \approx 0.612mV_{dc}$; SVPWM max $V_{dc}/\sqrt2$ | 15.5% more with third-harmonic injection | [22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md) |
| Fans and pumps: $P \propto n^3$ | Affinity laws | [22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md) |

## Power systems

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $I_b = S_b/(\sqrt3V_b)$, $Z_b = V_b^2/S_b$; $Z_{pu,new} = Z_{pu,old}(V_{b,old}/V_{b,new})^2(S_{b,new}/S_{b,old})$ | Three-phase bases | [22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md) |
| $L = (\mu_0/2\pi)\ln(D/r')$, $C = 2\pi\varepsilon_0/\ln(D/r)$ per metre; $r' = 0.7788r$ | Per phase, equilateral or GMD spacing | [22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md) |
| $Z_c = \sqrt{L/C}$; SIL $= V_{LL}^2/Z_c$; Ferranti $V_R = V_S/\cos(\beta\ell)$ | Lossless line | [22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md) |
| $P = \dfrac{V_1V_2}{X}\sin\delta$, $Q_1 = \dfrac{V_1^2 - V_1V_2\cos\delta}{X}$, $Q_2 = \dfrac{V_1V_2\cos\delta - V_2^2}{X}$ | Two buses through $X$; $V_1$ leads by δ | [22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md) |
| $\Delta V \approx (RP + XQ)/V$; quadrature $\delta V = (XP - RQ)/V$ adds about $\delta V^2/(2V)$ | Voltage drop | [22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md) |
| $I_f = V_f/Z_{th}$, fault MVA $= S_b/Z_{th,pu}$; SLG $I_a = 3V_f/(Z_1 + Z_2 + Z_0)$ | Faults | [22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md) |
| $E_k = HS$; RoCoF $= -\Delta Pf_0/(2HS)$ | Inertial response | [22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md) |
| $\Delta P_g = -(S/R)(\Delta f/f_0)$; $\Delta f_{ss} = -\Delta P/[\sum S_i/(R_if_0) + D]$ | Droop $R$; load damping $D$ in MW/Hz | [22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md) |
