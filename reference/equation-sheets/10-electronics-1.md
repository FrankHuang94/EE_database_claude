# Equation Sheet · 10 Electronics I

The relations to know cold from Course 10, each with its conditions and the chapter that derives it.

Conventions and course values:

- $V_T = kT/q$ = 25.852 mV at 300 K; total, DC and small-signal quantities written $v_{GS}$, $V_{GS}$, $v_{gs}$;
- diodes: $i_D = I_S(e^{v_D/nV_T} - 1)$, constant-drop model 0.7 V; MOSFETs: square law with $k_n = \mu_nC_{ox}W/L$; BJTs: $V_{BE}$ = 0.7 V, $V_{CE,sat}$ = 0.2 V;
- capacitors are short circuits and DC sources are signal ground at midband; the passive sign convention throughout.

## Diodes and diode circuits

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $i_D = I_S(e^{v_D/nV_T} - 1)$; small-signal $r_d = nV_T/I_D$ | Forward bias, low frequency | [10-01](../../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md) |
| 60 mV per decade of current ($n$ = 1); $V_D$ falls about 2 mV/K | At fixed current | [10-01](../../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md) |
| Peak rectifier ripple $V_r \approx V_p/(fRC)$ (half-wave), $V_p/(2fRC)$ (full-wave) | $V_r \ll V_p$; $f$ the line frequency | [10-01](../../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md) |
| Conduction angle $\omega\Delta t \approx \sqrt{2V_r/V_p}$; peak diode current ≫ average | Small ripple | [10-01](../../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md) |
| Zener series resistor: $R \le (V_{in,min} - V_Z)/(I_{L,max} + I_{Z,min})$ | Worst case at lowest input, highest load | [10-01](../../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md) |

## Transistor DC operation

| Relation | Conditions / notes | Chapter |
|---|---|---|
| NMOS saturation $i_D = \tfrac12k_n(v_{GS} - V_{TN})^2(1 + \lambda v_{DS})$ for $v_{DS} \ge v_{GS} - V_{TN}$ | Triode: $k_n(V_{ov} - v_{DS}/2)v_{DS}$ | [10-02](../../courses/10-electronics-1/chapters/10-02-mosfet-dc-operation-and-biasing.md) |
| Degenerated bias: $V_G = V_{GS} + I_DR_S$; sensitivity to $V_{TN}$ divided by $1 + g_mR_S$ | Source resistor as feedback | [10-02](../../courses/10-electronics-1/chapters/10-02-mosfet-dc-operation-and-biasing.md) |
| Body effect $V_{TN} = V_{TN0} + \gamma(\sqrt{2\phi_F + V_{SB}} - \sqrt{2\phi_F})$ | Source above body | [10-02](../../courses/10-electronics-1/chapters/10-02-mosfet-dc-operation-and-biasing.md) |
| BJT active: $I_C = \beta I_B = \alpha I_E$, $\alpha = \beta/(\beta + 1)$ | $V_{BE}$ ≈ 0.7 V, $V_{CE} > V_{CE,sat}$ | [10-03](../../courses/10-electronics-1/chapters/10-03-bjt-dc-operation-and-biasing.md) |
| Four-resistor bias $I_E = (V_{Th} - V_{BE})/[R_E + R_{Th}/(\beta + 1)]$ | Stable when $R_E \gg R_{Th}/(\beta + 1)$ | [10-03](../../courses/10-electronics-1/chapters/10-03-bjt-dc-operation-and-biasing.md) |
| Thermal loop gain $(\partial I_C/\partial T)V_{CE}R_{\theta}$; runaway when it reaches 1 | Fixed $V_{BE}$ drive | [10-03](../../courses/10-electronics-1/chapters/10-03-bjt-dc-operation-and-biasing.md) |

## Small-signal models

| Relation | Conditions / notes | Chapter |
|---|---|---|
| MOSFET $g_m = k_nV_{ov} = 2I_D/V_{ov} = \sqrt{2k_nI_D}$; $r_o \approx 1/(\lambda I_D)$; $g_{mb} = \chi g_m$, $\chi = \gamma/(2\sqrt{2\phi_F + V_{SB}})$ | Saturation | [10-04](../../courses/10-electronics-1/chapters/10-04-small-signal-models.md) |
| BJT $g_m = I_C/V_T$; $r_\pi = \beta/g_m$; $r_e = \alpha/g_m$; $r_o = V_A/I_C$; $r_\pi = (\beta + 1)r_e$ | Active region | [10-04](../../courses/10-electronics-1/chapters/10-04-small-signal-models.md) |
| Intrinsic gain $g_mr_o$: $2/(\lambda V_{ov})$ (MOS), $V_A/V_T$ (BJT) | Independent of current | [10-04](../../courses/10-electronics-1/chapters/10-04-small-signal-models.md) |
| $g_m/I$: $2/V_{ov}$ (strong inversion), up to $1/nV_T$ (weak inversion), $1/V_T$ (BJT) | Crossover near $V_{ov} = 2nV_T$ | [10-04](../../courses/10-electronics-1/chapters/10-04-small-signal-models.md) |
| $\text{HD}_2 = \hat v/4V_T$ (BJT), $\hat v/4V_{ov}$ (square law); BJT $\text{HD}_3 \approx (\hat v/V_T)^2/24$ | First order; degeneration divides HD₂ by $(1 + g_mR_S)^2$ at fixed input | [10-04](../../courses/10-electronics-1/chapters/10-04-small-signal-models.md), [10-06](../../courses/10-electronics-1/chapters/10-06-mos-single-stage-amplifiers.md) |

## Amplifier fundamentals

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $A_p = A_vA_i$; dB: $10\log P$, $20\log V$ (a power ratio only for equal resistances) | | [10-05](../../courses/10-electronics-1/chapters/10-05-amplifier-fundamentals.md) |
| $v_o/v_{sig} = \frac{R_i}{R_i + R_{sig}}A_{vo}\frac{R_L}{R_L + R_o}$ | Unilateral voltage amplifier | [10-05](../../courses/10-electronics-1/chapters/10-05-amplifier-fundamentals.md) |
| $A_{vo} = G_mR_o = R_m/R_i = A_{is}R_o/R_i$ | Model conversion | [10-05](../../courses/10-electronics-1/chapters/10-05-amplifier-fundamentals.md) |
| $R_o = R_L(v_{oc}/v_L - 1)$; $R_i = R_sv_i/(v_s - v_i)$ | Two-reading measurements | [10-05](../../courses/10-electronics-1/chapters/10-05-amplifier-fundamentals.md) |
| $Y_{in} = y_{11} - y_{12}y_{21}/(y_{22} + Y_L)$ | Bilateral two-port | [10-05](../../courses/10-electronics-1/chapters/10-05-amplifier-fundamentals.md) |
| Coupling corner $1/[2\pi C(R_{sig} + R_i)]$; class-A efficiency ≤ 25% (resistive), 50% (inductive); class B π/4 | | [10-05](../../courses/10-electronics-1/chapters/10-05-amplifier-fundamentals.md) |

## Single-stage amplifiers

| Stage | Gain | $R_{in}$ | $R_{out}$ | Chapter |
|---|---|---|---|---|
| Common source | $-g_m(R_D \parallel r_o)$; $\lvert A\rvert = 2V_{RD}/V_{ov}$ without $r_o$ | ∞ | $R_D \parallel r_o$ | [10-06](../../courses/10-electronics-1/chapters/10-06-mos-single-stage-amplifiers.md) |
| CS + $R_S$ | $-R_D/(1/g_m + R_S)$ | ∞ | $R_D \parallel [r_o + R_S + (g_m + g_{mb})r_oR_S]$ | [10-06](../../courses/10-electronics-1/chapters/10-06-mos-single-stage-amplifiers.md) |
| Common gate | $(g_m + g_{mb} + 1/r_o)(R_D \parallel r_o)$ | $(r_o + R_D)/[1 + (g_m + g_{mb})r_o]$ | $R_D \parallel [r_o(1 + (g_m + g_{mb})R_{sig}) + R_{sig}]$ | [10-06](../../courses/10-electronics-1/chapters/10-06-mos-single-stage-amplifiers.md) |
| Source follower | $g_mR_{eq}/(1 + g_mR_{eq})$, $R_{eq} = R_S \parallel r_o \parallel 1/g_{mb}$; ≤ $1/(1 + \chi)$ | ∞ | $1/(g_m + g_{mb}) \parallel r_o \parallel R_S$ | [10-06](../../courses/10-electronics-1/chapters/10-06-mos-single-stage-amplifiers.md) |
| Common emitter | $-g_m(R_C \parallel r_o)$; $\lvert A\rvert = V_{RC}/V_T$ without $r_o$ | $r_\pi$ | $R_C \parallel r_o$ | [10-07](../../courses/10-electronics-1/chapters/10-07-bjt-single-stage-amplifiers.md) |
| CE + $R_E$ | $-\alpha R_C/(r_e + R_E)$ | $(\beta + 1)(r_e + R_E)$ | $R_C \parallel \{r_o[1 + g_mR_{E\pi}r_\pi/(r_\pi + R_{sig})] + R_{E\pi}\}$, $R_{E\pi} = R_E \parallel (r_\pi + R_{sig})$; ≤ $(\beta + 1)r_o + r_\pi$ | [10-07](../../courses/10-electronics-1/chapters/10-07-bjt-single-stage-amplifiers.md) |
| Common base | $g_mR_C$ | $r_e$ (+ $R_B/(\beta + 1)$) | $R_C \parallel$ (degenerated, large) | [10-07](../../courses/10-electronics-1/chapters/10-07-bjt-single-stage-amplifiers.md) |
| Emitter follower ($R_E' = R_E \parallel R_L$) | $(\beta + 1)R_E'/[R_{sig} + r_\pi + (\beta + 1)R_E']$ | $r_\pi + (\beta + 1)R_E'$ | $R_E \parallel (r_\pi + R_{sig})/(\beta + 1)$ | [10-07](../../courses/10-electronics-1/chapters/10-07-bjt-single-stage-amplifiers.md) |

Cascode: $R_{out} \approx g_mr_o^2$, gain with an ideal current-source load about $(g_mr_o)^2$ ([10-06](../../courses/10-electronics-1/chapters/10-06-mos-single-stage-amplifiers.md)).

## Current sources and mirrors

| Relation | Conditions / notes | Chapter |
|---|---|---|
| MOS mirror $I_{out} = I_{ref}\frac{(W/L)_2}{(W/L)_1}\frac{1 + \lambda V_{DS2}}{1 + \lambda V_{GS}}$; $R_{out} = r_o$; compliance $V_{ov}$ | Matched, saturated | [10-08](../../courses/10-electronics-1/chapters/10-08-current-sources-and-mirrors.md) |
| BJT mirror $I_{out} = I_{ref}(1 + V_{CE2}/V_A)/(1 + V_{CE1}/V_A + 2/\beta)$; β helper: $2/[\beta(\beta + 1)]$ | Base current $I_Se^{V_{BE}/V_T}/\beta$ | [10-08](../../courses/10-electronics-1/chapters/10-08-current-sources-and-mirrors.md) |
| Cascode mirror $R_{out} \approx g_mr_o^2$; compliance $V_{TN} + 2V_{ov}$ (or $2V_{ov}$, low-voltage) | | [10-08](../../courses/10-electronics-1/chapters/10-08-current-sources-and-mirrors.md) |
| Wilson: error $2/(\beta^2 + 2\beta + 2)$, $R_{out} \approx \beta r_o/2$ | Bipolar | [10-08](../../courses/10-electronics-1/chapters/10-08-current-sources-and-mirrors.md) |
| Widlar: $V_T\ln(I_{ref}/I_{out}) = I_{out}R_E$; $R_{out} \approx r_o[1 + g_m(R_E \parallel r_\pi)]$ | Base currents neglected | [10-08](../../courses/10-electronics-1/chapters/10-08-current-sources-and-mirrors.md) |
| Mismatch $\sigma(\Delta V_{TH}) = A_{VT}/\sqrt{WL}$, $\sigma(\Delta\beta_n/\beta_n) = A_\beta/\sqrt{WL}$; mirror $\sigma^2(\Delta I/I) = (2/V_{ov})^2\sigma^2(\Delta V_{TH}) + \sigma^2(\Delta\beta_n/\beta_n)$ | Pelgrom; closely spaced devices | [10-08](../../courses/10-electronics-1/chapters/10-08-current-sources-and-mirrors.md) |
| Resistor reference supply sensitivity $\partial I/\partial V_{DD} = 1/(R + 1/g_m)$ | | [10-08](../../courses/10-electronics-1/chapters/10-08-current-sources-and-mirrors.md) |

## Real op-amps and applications

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $A_f = A/(1 + A\beta)$; gain error ≈ noise gain/$A$ | Noise gain $1/\beta = 1 + R_2/R_1$ | [10-09](../../courses/10-electronics-1/chapters/10-09-real-op-amps-nonidealities.md) |
| $f_{-3dB}$ = GBW/noise gain; 1% and 0.1% magnitude limits at 0.14 and 0.045 of $f_{-3dB}$ | Single pole | [10-09](../../courses/10-electronics-1/chapters/10-09-real-op-amps-nonidealities.md) |
| Slew boundary $\text{SR}\cdot\tau$, $\tau = 1/(2\pi f_{-3dB})$; full-power bandwidth $\text{SR}/(2\pi V_p)$ | | [10-09](../../courses/10-electronics-1/chapters/10-09-real-op-amps-nonidealities.md) |
| Input-referred errors: $V_{OS}$ + drift × ΔT; $\Delta V_{CM}$/CMRR; $\Delta V_S$/PSRR; $I_BR_2$ for an inverting or non-inverting stage with feedback resistor $R_2$ (or $I_{OS}R_2$ with a compensating resistor $R_1 \parallel R_2$) | Superpose; worst case or RSS | [10-09](../../courses/10-electronics-1/chapters/10-09-real-op-amps-nonidealities.md) |
| Difference-amp CMRR $\ge (1 + K)/(4\varepsilon)$; INA multiplies by its first-stage gain | Resistor tolerance ε | [10-10](../../courses/10-electronics-1/chapters/10-10-op-amp-application-circuits.md) |
| Lossy integrator corner $1/(2\pi RCA_0)$; offset ramp $V_{OS}/RC$ | | [10-10](../../courses/10-electronics-1/chapters/10-10-op-amp-application-circuits.md) |
| Precision-rectifier dead time: two-diode inverting $2V_D/\text{SR}$; superdiode $t_{OR} + (V_{rail} + V_D)/\text{SR}$ | The superdiode saturates on the off half-cycle | [10-10](../../courses/10-electronics-1/chapters/10-10-op-amp-application-circuits.md) |
| Non-inverting Schmitt: $V_U = V_{ref}(1 + R_1/R_2)$, hysteresis $V_{DD}R_1/R_2$ | Rail-to-rail output | [10-10](../../courses/10-electronics-1/chapters/10-10-op-amp-application-circuits.md) |
| Relaxation oscillator: $T = 2RC\ln[(1 + \beta)/(1 - \beta)]$, $\beta = R_1/(R_1 + R_2)$ | Symmetric output swing | [10-10](../../courses/10-electronics-1/chapters/10-10-op-amp-application-circuits.md) |
| TIA: $v_o/i = -R_F\omega_t/[R_F(C_{in} + C_F)s^2 + (1 + \omega_tR_FC_F)s + \omega_t]$; without $C_F$: $f_0 = \sqrt{\text{GBW}/(2\pi R_FC_{in})}$, $Q = \sqrt{\omega_tR_FC_{in}}$; Butterworth ($Q = 1/\sqrt2$): $C_F = \sqrt{2\omega_tR_FC_{in} - 1}/(\omega_tR_F) \approx \sqrt{2C_{in}/(\omega_tR_F)}$ | Single-pole op-amp | [10-10](../../courses/10-electronics-1/chapters/10-10-op-amp-application-circuits.md) |
