# Equation Sheet · 12 Electronics II

The relations to know cold from Course 12, each with its conditions and the chapter that derives it.

Conventions:

- square-law MOSFETs: $I_D = (k/2)V_{ov}^2$, $g_m = 2I_D/V_{ov}$, $r_o = 1/(\lambda I_D)$; bipolar $g_m = I_C/V_T$, $V_T$ = 25.852 mV;
- loop gain $T$ positive for negative feedback; oscillator loop gain $L = A\beta$ for positive feedback;
- noise densities one-sided; $T$ = 300 K, $4kT$ = 1.657 × 10⁻²⁰ J.

## Differential pairs and multistage amplifiers

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $A_{dm} = g_mR_D$ (differential out), $g_mR_D/2$ single-ended; $A_{cm} = g_mR_D/(1 + 2g_mR_{SS}) \approx R_D/(2R_{SS})$ | Half circuits; $R_{SS}$ the tail's resistance | [12-01](../../courses/12-electronics-2/chapters/12-01-differential-pairs.md) |
| MOS pair fully switches at $\lvert v_{id}\rvert = \sqrt{2I_{SS}/k}$; BJT pair $\Delta i = I_{EE}\tanh(v_{id}/2V_T)$ | Large signal | [12-01](../../courses/12-electronics-2/chapters/12-01-differential-pairs.md) |
| Offset $\sigma_{V_{OS}} = A_{VT}/\sqrt{WL}$ (Pelgrom) | Mismatch scales with area | [12-01](../../courses/12-electronics-2/chapters/12-01-differential-pairs.md) |
| Five-transistor OTA: $A = g_{m1}(r_{o2} \parallel r_{o4})$ | Mirror load | [12-02](../../courses/12-electronics-2/chapters/12-02-active-loads-cascodes-multistage.md) |
| Cascode $R_{out} = r_{o1} + r_{o2} + g_{m2}r_{o2}r_{o1}$; open-circuit gain $g_{m1}r_{o1}(1 + g_{m2}r_{o2})$ | Telescopic: both sides cascoded | [12-02](../../courses/12-electronics-2/chapters/12-02-active-loads-cascodes-multistage.md) |

## Frequency response

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $f_T = g_m/[2\pi(C_{gs} + C_{gd})]$ | Current gain = 1 | [12-03](../../courses/12-electronics-2/chapters/12-03-frequency-response-miller-poles-zeros.md) |
| Miller: $C_{in} = C(1 + \lvert A\rvert)$, $C_{out} = C(1 + 1/\lvert A\rvert)$ | Inverting gain $-\lvert A\rvert$ | [12-03](../../courses/12-electronics-2/chapters/12-03-frequency-response-miller-poles-zeros.md) |
| CS stage zero $+g_m/C_{gd}$ (right half-plane) | Feed-forward through $C_{gd}$ | [12-03](../../courses/12-electronics-2/chapters/12-03-frequency-response-miller-poles-zeros.md) |
| OCTC: $b_1 = \sum R_{i0}C_i$, $f_{-3dB} \approx 1/(2\pi b_1)$; $R_{gd} = R_S + R_L + g_mR_SR_L$ | Conservative; poles apart | [12-04](../../courses/12-electronics-2/chapters/12-04-high-frequency-analysis-methods.md) |
| SCTC: $\omega_L \approx \sum 1/(R_{is}C_i)$ | Low corner, conservative | [12-04](../../courses/12-electronics-2/chapters/12-04-high-frequency-analysis-methods.md) |
| Pole splitting: $p_1 \approx 1/(g_{m2}R_1R_2C_c)$, $p_2 \approx g_{m2}C_c/[C_1C_2 + C_c(C_1 + C_2)]$ | Miller capacitor | [12-04](../../courses/12-electronics-2/chapters/12-04-high-frequency-analysis-methods.md) |

## Feedback and stability

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $A_f = A/(1 + T) = (1/\beta)\,T/(1 + T)$; $dA_f/A_f = (dA/A)/(1 + T)$ | $T = A\beta$ | [12-05](../../courses/12-electronics-2/chapters/12-05-feedback-topologies.md) |
| Single pole: bandwidth × $(1 + T_0)$, GBW constant | Bandwidth extension | [12-05](../../courses/12-electronics-2/chapters/12-05-feedback-topologies.md) |
| Series ×$(1 + T)$, shunt ÷$(1 + T)$ (input mixing, output sampling) | Four topologies | [12-05](../../courses/12-electronics-2/chapters/12-05-feedback-topologies.md) |
| $A_f = A_\infty T/(1 + T) + A_{\mathrm{dir}}/(1 + T)$; $Z = Z^{(0)}(1 + T_{sc})/(1 + T_{oc})$ | Return ratio; Blackman | [12-05](../../courses/12-electronics-2/chapters/12-05-feedback-topologies.md) |
| PM $= 180^\circ + \angle T(j\omega_c)$; GM $= -20\log\lvert T(j\omega_{180})\rvert$ | Bode criterion | [12-06](../../courses/12-electronics-2/chapters/12-06-stability-and-compensation.md) |
| Two-pole loop: $Q = \sqrt{f_u/f_2}$; 60° at $f_2 = 1.5f_u$ (8.8% overshoot); 45° ≈ 23% | $f_u = T_0f_1$ | [12-06](../../courses/12-electronics-2/chapters/12-06-stability-and-compensation.md) |
| Miller: GBW $= g_{m1}/(2\pi C_c)$, $p_2 \approx g_{m2}/C_L$, zero $g_{m2}/C_c$; $g_{m2} \approx 10g_{m1}$, $C_c \approx 0.22C_L$ → about 60° | Two-stage | [12-06](../../courses/12-electronics-2/chapters/12-06-stability-and-compensation.md) |
| Nulling resistor: $z = 1/[C_c(1/g_{m2} - R_z)]$; $R_z = 1/g_{m2}$ removes it; $(1 + C_L/C_c)/g_{m2}$ cancels $p_2$ | New pole $\approx 1/(R_zC_1)$ | [12-06](../../courses/12-electronics-2/chapters/12-06-stability-and-compensation.md) |

## Output stages and op-amps

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Class A: η ≤ 25%; class B: $\eta = (\pi/4)V_{op}/V_{CC}$ ≤ 78.5% | Resistive load | [12-07](../../courses/12-electronics-2/chapters/12-07-output-stages.md) |
| Class B worst dissipation $2V_{CC}^2/(\pi^2R_L)$ at $V_{op} = 2V_{CC}/\pi$ | 50% efficiency there | [12-07](../../courses/12-electronics-2/chapters/12-07-output-stages.md) |
| Class AB: $i_Ni_P = I_Q^2$; $V_{BB} = V_{BE}(1 + R_1/R_2)$; $R_{out} = V_T/(2I_Q)$ at idle | Translinear | [12-07](../../courses/12-electronics-2/chapters/12-07-output-stages.md) |
| $T_J = T_A + P_D\sum\theta$; runaway if $V_{CE}\theta g_m(2\ \text{mV/°C})/(1 + g_mR_E) \ge 1$ | Thermal | [12-07](../../courses/12-electronics-2/chapters/12-07-output-stages.md) |
| Two-stage op-amp gain $g_{m1}R_1 \cdot g_{m6}R_2$; SR $= I_{SS}/C_c$ (rising also ≤ $I_7/(C_L + C_c)$) | $\text{SR}/\omega_u = V_{ov1}$ (MOS), $2V_T$ (BJT) | [12-08](../../courses/12-electronics-2/chapters/12-08-op-amp-internals.md) |
| Full-power bandwidth $\text{SR}/(2\pi V_p)$; folded cascode GBW $g_{m1}/(2\pi C_L)$ | | [12-08](../../courses/12-electronics-2/chapters/12-08-op-amp-internals.md) |
| CM error without CMFB $\Delta I\cdot R_{out}$; with CMFB ÷$(1 + g_{m,cm}R_{out})$ | Fully differential | [12-08](../../courses/12-electronics-2/chapters/12-08-op-amp-internals.md) |

## Oscillators and noise

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Barkhausen $L(j\omega_0) = 1$; Wien $\omega_0 = 1/RC$, gain 3; RC ladder $\omega_0 = \sqrt6/RC$, gain 29 | Positive feedback | [12-09](../../courses/12-electronics-2/chapters/12-09-oscillators.md) |
| Colpitts $\omega_0^2 = (C_1 + C_2)/(LC_1C_2)$, $g_mR \ge C_2/C_1$; cross-coupled $-2/g_m$, start if $g_m > 2/R_p$ | LC | [12-09](../../courses/12-electronics-2/chapters/12-09-oscillators.md) |
| Crystal $f_p = f_s\sqrt{1 + C_m/C_0}$; with $C_L$: $f_s\sqrt{1 + C_m/(C_0 + C_L)}$ | Pulling | [12-09](../../courses/12-electronics-2/chapters/12-09-oscillators.md) |
| Ring $f = 1/(2Nt_{pd})$; linear model $\omega_0 = \tan(\pi/N)/\tau$, gain $1/\cos(\pi/N)$ | Odd $N$ | [12-09](../../courses/12-electronics-2/chapters/12-09-oscillators.md) |
| Thermal $4kTR$ (1 kΩ ≈ 4.07 nV/√Hz); shot $2qI$; kT/C (1 pF ≈ 64.4 µV) | One-sided | [12-10](../../courses/12-electronics-2/chapters/12-10-noise-in-circuits.md) |
| MOSFET $4kT\gamma/g_m$; BJT $2kT/g_m$; 1/f integral $S_wf_c\ln(f_2/f_1)$ | Input-referred | [12-10](../../courses/12-electronics-2/chapters/12-10-noise-in-circuits.md) |
| $\overline{v^2} = 4kTR_s + e_n^2 + i_n^2R_s^2$; $F$ = that ÷ $4kTR_s$; $R_{opt} = e_n/i_n$, $F_{min} = 1 + e_ni_n/(2kT)$ | Noise figure | [12-10](../../courses/12-electronics-2/chapters/12-10-noise-in-circuits.md) |
