# Equation Sheet · 20 Analog and Mixed-Signal IC Design

The relations to know cold from Course 20, each with its conditions and the chapter that derives it.

Conventions:

- $V_T = kT/q$ = 25.85 mV at 300 K is the thermal voltage and $V_{TH}$ a threshold; $kT$ = 4.142 × 10⁻²¹ J;
- $g_m/I_D$ in V⁻¹ (S/A); $n$ is the subthreshold slope factor; $q$ the normalized inversion charge and $IC$ the inversion coefficient (20-01);
- phase noise $\mathcal L(f)$ is single-sideband, in dBc/Hz; jitter integrals carry the factor 2 for both sidebands;
- mismatch coefficients $A_{VT}$ and $A_\beta$ describe the difference of a pair;
- in 20-08, 0 dBFS means DAC levels ±1 (Δ = 2 for a 1-bit quantizer);
- symbols reused between chapters: β is a feedback factor (op-amps, LDOs, 20-12) or a gain factor (matching); η is an efficiency (LDO), an exponent of $I_S(T)$ (references) or a swing fraction (20-12); τ is a settling, regeneration or RC time constant; $N$ is a resolution in bits, a divide ratio (PLLs) or an area ratio (references).

## The transistor: charge-based model and gm/ID

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $q = -Q_i/(2nC_{ox}V_T)$; $(V_P - V_{ch})/V_T = 2q + \ln q$ | Normalized inversion charge; $n$ the slope factor | [20-01](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-01-analog-design-fundamentals-gm-id.md) |
| $I_D = I_{spec}[(q_s^2 + q_s) - (q_d^2 + q_d)]$, $I_{spec} = 2n\mu C_{ox}(W/L)V_T^2$ | All regions; saturation: $q_d \to 0$ | [20-01](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-01-analog-design-fundamentals-gm-id.md) |
| $IC = I_D/I_{spec} = q^2 + q$; $V_{ov} = nV_T(2q + \ln q)$ | Weak $IC < 0.1$, moderate 0.1–10, strong $> 10$ | [20-01](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-01-analog-design-fundamentals-gm-id.md) |
| $\dfrac{g_m}{I_D} = \dfrac{1}{nV_T(1 + q)} = \dfrac{1}{nV_T}\cdot\dfrac{2}{1 + \sqrt{1 + 4IC}}$ | Maximum $1/(nV_T)$ in weak inversion; $\approx 2/V_{ov}$ in strong | [20-01](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-01-analog-design-fundamentals-gm-id.md) |
| Velocity saturation: $I_D = I_{spec}(q^2 + q)/(1 + \lambda_cq)$, $\lambda_c = L_{sat}/L$, $L_{sat} = \mu V_T/v_{sat}$ | Lowers $g_m/I_D$ at high $IC$ | [20-01](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-01-analog-design-fundamentals-gm-id.md) |
| $f_T = \dfrac{g_m}{2\pi C_{gg}} = \dfrac{3\mu V_T}{2\pi L^2}\Delta$, $\Delta = \dfrac{q(\lambda_cq^2 + 2q + 1)}{(2q + 1)(1 + \lambda_cq)^2}$ | $C_{gg} \approx \tfrac23WLC_{ox}$; $\Delta \to q$ without velocity saturation; falls toward weak inversion | [20-01](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-01-analog-design-fundamentals-gm-id.md) |
| $A_i = g_mr_o = (g_m/I_D)V_A = (g_m/I_D)V_A'L$ | Intrinsic gain; $V_A \propto L$ to first order | [20-01](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-01-analog-design-fundamentals-gm-id.md) |
| $(g_m/I_D)f_T = \dfrac{3\mu}{2\pi nL^2}\cdot\dfrac{q}{1 + q}$ | The efficiency–speed product. Long channel ($\lambda_c = 0$): rises monotonically toward $3\mu/(2\pi nL^2)$. With velocity saturation it peaks, in moderate inversion for short channels (0.15 µm example: IC ≈ 6.9) | [20-01](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-01-analog-design-fundamentals-gm-id.md) |
| $V_{DS,sat} = V_T[2(q_s - q_d) + \ln(q_s/q_d)]$ at $q_d$ set so the reverse current is 2% of the forward; ≈ 3.91 $V_T$ in weak inversion, ≈ 0.86 $V_P$ + 2.8 $V_T$ in strong (roughly $2/(g_m/I_D)$ as a design rule) | Headroom per device | [20-02](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md) |

## The two-stage op-amp

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $A_0 = g_{m1}R_1\,g_{m6}R_2$; $z = g_{m6}/C_c$ (RHP) | Miller-compensated two-stage | [20-02](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md) |
| $p_1 \approx 1/(g_{m6}R_1R_2C_c)$, $p_2 \approx g_{m6}C_c/[C_1C_L + C_c(C_1 + C_L)]$; $\omega_u = g_{m1}/C_c$ | Pole splitting | [20-02](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md) |
| $p_{2,max} = \omega_{T6}\,C_c/(C_L + C_c)$ | Second stage's own capacitance bounds $p_2$ | [20-02](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md) |
| Nulling resistor: zero at $1/[C_c(1/g_{m6} - R_z)]$; $R_z = 1/g_{m6}$ cancels it; $R_zg_{m6} = (W/L)_6/[n(W/L)_z]$ tracks | Triode-device $R_z$ |
| Zero on $p_2$: $R_z = 1/g_{m6} + 1/(p_2C_c)$, ≈ $(1 + C_L/C_c)/g_{m6}$ when $p_2 \approx g_{m6}/C_L$ | The shortcut needs $C_1 \ll C_c, C_L$ | [20-02](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md) |
| $\text{PM} \approx 90° - \arctan(\omega_u/p_2) - \arctan(\omega_u/z)$ | Two-pole estimate; RHP zero subtracts phase | [20-02](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md) | [20-02](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md) |
| $\text{SR} = I_{SS}/C_c = 2\omega_u/(g_m/I_D)_1$; $I_6 \ge I_{SS}(1 + C_L/C_c)$ | Slewing; output stage must not starve | [20-02](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md) |
| $t_{slew} = (V - \text{SR}\,\tau)/\text{SR}$, $t_{lin} = \tau\ln[\text{SR}\,\tau/(\varepsilon V)]$ | Large-step settling | [20-02](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md) |
| Nested Miller (Butterworth): $C_{m1} = 4g_{m1}C_L/g_{m3}$, $C_{m2} = 2g_{m2}C_L/g_{m3}$, $\omega_u = g_{m3}/(4C_L)$ | Three stages | [20-02](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md) |
| Gain-boost doublet: slow settling $e^{-\omega_{ub}t}/(\beta A_{unb})$ | Keep the booster's unity-gain frequency above $\omega_u\beta$ and below the main amplifier's non-dominant pole | [20-02](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md) |

## References

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $V_{BE}(T) = V_{g0} - (V_{g0} - V_{BE0})T/T_0 - (\eta - m)V_T\ln(T/T_0)$ | Tsividis; bias current $\propto T^m$ | [20-03](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-03-bandgap-references.md) |
| $\Delta V_{BE} = V_T\ln N$ (PTAT) | Equal currents, area ratio N | [20-03](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-03-bandgap-references.md) |
| $V_{REF} = V_{BE1} + (R_2/R_1)V_T\ln N$; current mode: $V_{REF} = (R_3/R_2)(V_{BE1} + (R_2/R_1)V_T\ln N)$ | Op-amp and current-mode bandgaps | [20-03](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-03-bandgap-references.md) |
| $V_{REF}(T) = V_{g0} + (\eta - 1)V_T(T)\,[1 - \ln(T/T_c)]$ | First-order compensated at $T_c$ (PTAT bias, $m = 1$); peak $V_{g0} + (\eta - 1)V_T(T_c)$ | [20-03](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-03-bandgap-references.md) |
| $\text{TC}_{box} = (V_{max} - V_{min})/[V_{nom}(T_2 - T_1)] \times 10^6$ ppm/K | Data-sheet box method | [20-03](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-03-bandgap-references.md) |
| β-multiplier: $I = V_T\ln K/R$ | Weak inversion, bulk at ground ($nV_T\ln K/R$ if M2's bulk is tied to its source); needs a start-up circuit | [20-03](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-03-bandgap-references.md) |

## Low-dropout regulators

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\eta = V_{out}I_L/[V_{in}(I_L + I_Q)] \le V_{out}/V_{in}$ | Efficiency | [20-04](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-04-ldo-regulators.md) |
| $L_0 = A_{EA}\beta g_{mp}R_{out}$, $R_{out} = r_{ds} \parallel R_L \parallel R_{div}$; load regulation $\Delta V_{out} \approx -\Delta V_{SG}/(A_{EA}\beta)$ | Loop gain at DC | [20-04](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-04-ldo-regulators.md) |
| $\omega_c \approx A_{EA}\beta g_{mp}/C_L$; with ESR, $Z_{out} = R_{out} \parallel (R_{ESR} + 1/sC_L)$, zero at $1/(R_{ESR}C_L)$ | Output-pole dominant; worst stability at full load | [20-04](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-04-ldo-regulators.md) |
| $1/\text{PSRR}(s) = [g_{mp}(1 - k) + g_{ds}]Z_{out}(s)/(1 + L(s))$ | $k$ = fraction of supply ripple on the gate | [20-04](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-04-ldo-regulators.md) |
| $\Delta V \approx \Delta I/(\omega_cC_L) + \Delta I\,R_{ESR}$ | Load-step droop | [20-04](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-04-ldo-regulators.md) |

## Sampling and comparators

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\overline{v_n^2} = kT/C$ | Any switch resistance; 64 µV rms on 1 pF at 300 K | [20-05](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-05-comparators-and-sample-and-hold.md) |
| $\text{SNR} = (A^2/2)/(\Delta^2/12 + 2kT/C + \tfrac12A^2(2\pi f_{in}\sigma_t)^2 + \cdots)$ | Differential sampler: $2kT/C$ | [20-05](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-05-comparators-and-sample-and-hold.md) |
| $\text{SNR}_{jitter} = -20\log_{10}(2\pi f_{in}\sigma_t)$ | Full-scale sine | [20-05](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-05-comparators-and-sample-and-hold.md) |
| $\tau \le T_{tr}/[(N + 1)\ln 2]$ | Track settling to ½ LSB | [20-05](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-05-comparators-and-sample-and-hold.md) |
| Charge injection $\Delta V \approx Q_{ch}/(2C)$; plain switch $R_{on} = 1/[K(V_G - v_{in} - V_{TH}(v_{in}))]$; bootstrapped ($V_G - v_{in} = V_{DD}$) $R_{on} = 1/[K(V_{DD} - V_{TH}(v_{in}))]$ | Half the channel charge each side | [20-05](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-05-comparators-and-sample-and-hold.md) |
| Latch: $\tau \approx C/g_m$, $t_{dec} = \tau\ln(V_L/v_0)$; $v_{min} = (V_L/A_0)e^{-T/\tau}$ | Regeneration and metastability | [20-05](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-05-comparators-and-sample-and-hold.md) |
| StrongARM: $A_{int} = (g_m/I_D)V_{TH}$, $\sigma_{in}^2 = (4\gamma/A_{int})\,kT/C$, $E\sigma_{in}^2 = 8\gamma kTV_{DD}^2/A_{int}$ | Integration-phase gain and noise | [20-05](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-05-comparators-and-sample-and-hold.md) |

## Converter metrics

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\text{SQNR} = 6.02N + 1.76$ dB | Full-scale sine, uniform quantization | [20-06](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-06-data-converter-fundamentals.md) |
| $\text{DNL}_k = (T_{k+1} - T_k)/\Delta_{avg} - 1$; $\text{INL}_k = \sum_{j<k}\text{DNL}_j$ | End-point INL | [20-06](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-06-data-converter-fundamentals.md) |
| $\sigma(\text{DNL}_{mid}) = \sigma_u\sqrt{2^N - 1}$; $\sigma(\text{INL}_{mid}) \approx (\sigma_u/2)2^{N/2}$ | Binary-weighted unit elements | [20-06](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-06-data-converter-fundamentals.md) |
| $\text{ENOB} = (\text{SINAD} - 1.76)/6.02$; $\text{NSD} = -\text{SNR}_{FS} - 10\log_{10}(f_s/2)$ dBFS/Hz |  | [20-06](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-06-data-converter-fundamentals.md) |
| $\text{FoM}_W = P/(2^{\text{ENOB}}f_s)$; $\text{FoM}_S = \text{SNDR} + 10\log_{10}(BW/P)$ | Walden (J/step), Schreier (dB) | [20-06](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-06-data-converter-fundamentals.md) |
| $P/f_s = 8kT\cdot\text{SNR}$ ⇒ $\text{FoM}_S \le 10\log_{10}[1/(16kT)]$ ≈ 191.8 dB | Ideal class-B sampler at 300 K | [20-06](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-06-data-converter-fundamentals.md) |

## Nyquist ADCs

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Flash: $2^N - 1$ comparators; SAR: $N$ cycles; pipeline: one stage per 1–2 bits | Architecture costs | [20-07](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-07-nyquist-adcs.md) |
| SAR: $v_x = -v_{in} + V_{REF}\,\text{code}/2^N$; conventional switching $E = \sum_i 2^{N+1-2i}(2^i - 1)C_uV_{REF}^2$ | Charge redistribution; $E$ is for a differential SAR (two arrays) | [20-07](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-07-nyquist-adcs.md) |
| Redundancy margin $m_k = \sum_{j>k}w_j - w_k + 1$ | Sub-binary SAR | [20-07](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-07-nyquist-adcs.md) |
| 1.5-bit MDAC: $v_{res} = (2v_{in} - DV_{REF})/(1 + 1/(A\beta))$, $\beta = C_f/(C_s + C_f + C_p)$ | Finite-gain error | [20-07](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-07-nyquist-adcs.md) |
| Stage scaling: referred noise $kT/C_1(1 + \tfrac12 + \tfrac14 + \cdots) \to 2kT/C_1$ | Capacitors halve per stage | [20-07](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-07-nyquist-adcs.md) |
| Two-channel interleaving: offset spur $\Delta o^2/(2A^2)$ at $f_s/2$; gain image $(\alpha/2)^2$; skew image $(\pi f_{in}\Delta t)^2$ at $f_s/2 - f_{in}$ | Power ratios to the signal |
| $M$ channels: total skew-spur power ≈ $(2\pi f_{in}\sigma_{skew})^2$ | $\sigma_{skew}$ = per-channel rms skew; two channels: $\sigma = \Delta t/2$ | [20-07](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-07-nyquist-adcs.md) | [20-07](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-07-nyquist-adcs.md) |

## Sigma-delta converters

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Oversampling alone: $\text{SQNR} = 6.02N + 1.76 + 10\log_{10}\text{OSR}$ |  | [20-08](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-08-sigma-delta-converters.md) |
| First order: $Y = z^{-1}X + (1 - z^{-1})E$; $P_q \approx \sigma_e^2\pi^2/(3\,\text{OSR}^3)$ |  | [20-08](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-08-sigma-delta-converters.md) |
| Order $L$: $P_q \approx \dfrac{\Delta^2}{12}\cdot\dfrac{\pi^{2L}}{(2L + 1)\text{OSR}^{2L+1}}$: $(6L + 3)$ dB per octave of OSR | Ideal NTF $(1 - z^{-1})^L$ | [20-08](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-08-sigma-delta-converters.md) |
| Lee's rule $\|\text{NTF}\|_\infty \le 2$ (1.5 in practice) | 1-bit higher-order stability | [20-08](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-08-sigma-delta-converters.md) |
| Integrator leak $p = (1 + 1/A)/[1 + (1 + C_s/C_i)/A] \approx 1 - (C_s/C_i)/A$; $P_q \approx \sigma_e^2[\varepsilon^2/\text{OSR} + \pi^2/(3\,\text{OSR}^3)]$ | First-order loop; for $C_s = C_i$ leakage matters if $A < \sqrt3\,\text{OSR}/\pi$ | [20-08](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-08-sigma-delta-converters.md) |
| MASH 1-1: $Y = z^{-2}X + (1 - z^{-1})^2E_2$ | Needs matched analog and digital filters |
| MASH 1-1 leak residue $\varepsilon z^{-2}E_1$: need $\varepsilon < \pi^2/(\sqrt5\,\text{OSR}^2)$ | Far stricter than a single loop | [20-08](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-08-sigma-delta-converters.md) | [20-08](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-08-sigma-delta-converters.md) |
| CT NRZ jitter: $P_{jitter} = E[(y[n] - y[n-1])^2]\,(\sigma_tf_s)^2/\text{OSR}$ | Multi-bit feedback reduces the steps | [20-08](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-08-sigma-delta-converters.md) |
| Decimation filter: $\text{sinc}^{L+1}$ | One order above the modulator | [20-08](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-08-sigma-delta-converters.md) |

## DACs

| Relation | Conditions / notes | Chapter |
|---|---|---|
| R-2R: $V_{out} = DV_{REF}/2^N$ | Thévenin induction | [20-09](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-09-dacs.md) |
| $\sigma(\text{DNL})$: binary $\sigma_u\sqrt{2^N - 1}$; segmented $\sigma_u\sqrt{2^{B+1} - 1}$ for $B$ binary LSBs | Worst transition | [20-09](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-09-dacs.md) |
| INL bridge: $\sigma^2_{INL}(n) = \sigma_u^2\,n(N_t - n)/N_t$; yield rule $\sigma_u \le 0.5/(\lambda\sqrt{N_t})$, λ = 1.818 at 99.73% | Kolmogorov distribution of the maximum | [20-09](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-09-dacs.md) |
| Current-cell sizing: $WL = [\sqrt2A_{VT}/(V_{ov}\sigma_u)]^2$ | Pelgrom | [20-09](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-09-dacs.md) |
| Output impedance: $\text{INL} \approx xN_t^2/4$, $\text{HD2} \approx xN_t/4$, $\text{HD3} \approx (xN_t)^2/16$; differential cancels HD2 | $x = R_L/r_{unit}$ | [20-09](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-09-dacs.md) |
| Settling $t_s = (N + 1)\tau\ln 2$; NRZ $\text{sinc}(f/f_s)$; RZ $\tfrac12\text{sinc}(f/2f_s)$; mixed mode $\text{sinc}(f/2f_s)\sin(\pi f/2f_s)$ | sinc$(x) = \sin(\pi x)/(\pi x)$; NRZ droop 3.92 dB at $f_s/2$ | [20-09](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-09-dacs.md) |

## PLLs and jitter

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $G(s) = (I_{cp}/2\pi)Z(s)(K_{VCO}/s)/N$; $\theta_{out}/\theta_{ref} = NG/(1 + G)$ | Phase-domain model | [20-10](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-10-plls-and-jitter.md) |
| Second order: $\omega_n = \sqrt{I_{cp}K_{VCO}/(2\pi NC)}$, $\zeta = (R/2)\sqrt{I_{cp}K_{VCO}C/(2\pi N)}$ | R in series with C | [20-10](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-10-plls-and-jitter.md) |
| Third order: $\text{PM}_{max} = \arctan[(b - 1)/(2\sqrt b)]$, $b = 1 + C_1/C_2$ | Zero and pole $\sqrt b$ either side of crossover |
| $Z(s) = (1 + sRC_1)/[s(C_1 + C_2)(1 + sRC_1C_2/(C_1 + C_2))]$; $\omega_z = 1/(RC_1)$, $\omega_p = (C_1 + C_2)/(RC_1C_2)$; $C_1 + C_2 = K\sqrt b/\omega_c^2$, $K = I_{cp}K_{VCO}/(2\pi N)$ | Third-order loop filter; from $\lvert G(j\omega_c)\rvert = 1$ | [20-10](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-10-plls-and-jitter.md) | [20-10](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-10-plls-and-jitter.md) |
| $f_c \lesssim f_{ref}/10$; sampled-loop limit $\omega_c < \omega_{ref}/[\pi(1 + \pi\omega_z/\omega_{ref})]$ | Gardner | [20-10](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-10-plls-and-jitter.md) |
| $\sigma_t = \sqrt{2\int\mathcal L\,df}/(2\pi f_0)$ | Single-sideband $\mathcal L$ | [20-10](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-10-plls-and-jitter.md) |
| $\text{FoM}_{osc} = -\mathcal L(\Delta f) + 20\log_{10}(f_0/\Delta f) - 10\log_{10}(P/1\text{ mW})$ | Larger is better | [20-10](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-10-plls-and-jitter.md) |
| MASH divider: $\mathcal L_{\Sigma\Delta} = \dfrac{(2\pi)^2}{12f_{ref}}[2\sin(\pi f/f_{ref})]^{2(m-1)}$ | Before loop filtering | [20-10](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-10-plls-and-jitter.md) |
| TDC floor: $\mathcal L_{TDC} = \dfrac{(2\pi)^2}{12}(\Delta t_{res}f_0)^2/f_{ref}$ | ADPLL | [20-10](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-10-plls-and-jitter.md) |
| $\text{FoM} = 10\log_{10}[(\sigma_t/1\text{ s})^2(P/1\text{ mW})]$ | Jitter-power; lower is better | [20-10](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-10-plls-and-jitter.md) |

## Matching and PVT

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\sigma(\Delta V_{TH}) = A_{VT}/\sqrt{WL}$, $\sigma(\Delta\beta/\beta) = A_\beta/\sqrt{WL}$; single device $1/\sqrt2$ of the pair | Pelgrom; $A_{VT}$ ≈ 1 mV·µm per nm of oxide | [20-11](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-11-layout-matching-pvt.md) |
| Mirror: $\sigma(\Delta I/I)^2 = (g_m/I_D)^2\sigma(\Delta V_{TH})^2 + \sigma(\Delta\beta/\beta)^2$ | Low $g_m/I_D$ for mirrors | [20-11](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-11-layout-matching-pvt.md) |
| Pair: $\sigma(V_{os})^2 = \sigma(\Delta V_{TH})^2 + \sigma(\Delta\beta/\beta)^2/(g_m/I_D)^2$ | High $g_m/I_D$ for pairs | [20-11](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-11-layout-matching-pvt.md) |
| $f(V/\sigma)^2/P \propto 1/(C_{ox}A_{VT}^2)$ | Kinget's speed–accuracy–power limit | [20-11](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-11-layout-matching-pvt.md) |
| ABBA cancels linear gradients, leaves $2g_2p^2$; ABBABAAB cancels linear and quadratic | One-dimensional placement | [20-11](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-11-layout-matching-pvt.md) |
| 95% CI on σ from $n$ runs: $\hat\sigma\sqrt{(n - 1)/\chi^2_{0.975,\,n-1}}$ to $\hat\sigma\sqrt{(n - 1)/\chi^2_{0.025,\,n-1}}$; large $n$: $\hat\sigma/(1 \pm 1.96/\sqrt{2(n - 1)})$ | 100 runs: 0.878–1.162 × σ̂ | [20-11](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-11-layout-matching-pvt.md) |
| Failure-free runs for rate $< p$: $(1 - p)^n \le 0.05$, $n \approx 3/p$ | 3σ (0.27%): 1109 runs | [20-11](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-11-layout-matching-pvt.md) |

## Why analog does not scale

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Constant field by $S$: delay $1/S$, energy $1/S^3$, area $1/S^2$ | Digital | [20-12](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-12-why-analog-does-not-scale.md) |
| $C = 2kT\cdot\text{SNR}/A^2$; $P = \dfrac{16\pi kT\cdot\text{SNR}\cdot f}{\beta\eta^2(g_m/I_D)V_{DD}}$ | Class-A, swing $\eta V_{DD}$ peak-to-peak: power $\propto 1/V_{DD}$ | [20-12](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-12-why-analog-does-not-scale.md) |
| $V_{swing} \approx V_{DD} - n_{stack}V_{DS,sat}$; cascode gain ≈ $A_i^2/2$ | Headroom | [20-12](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-12-why-analog-does-not-scale.md) |
| $C_{mm}/C_n = C_{ox}A_{VT}^2/kT$ | Mismatch- versus noise-limited capacitance | [20-12](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-12-why-analog-does-not-scale.md) |
| Calibration accuracy $\varepsilon_{max}/\varepsilon$; closed-loop error $1/(1 + A_0\beta)$ | Digitally assisted analog | [20-12](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-12-why-analog-does-not-scale.md) |
