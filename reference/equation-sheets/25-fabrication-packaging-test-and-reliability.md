# Equation Sheet · 25 Semiconductor Fabrication, Packaging, Test and Reliability

The relations to know cold from Course 25, each with its conditions and the chapter that derives it.

Conventions:

- $k$ = 8.617 × 10⁻⁵ eV/K is Boltzmann's constant in Arrhenius factors, and temperatures inside exponentials are absolute ($T$ = °C + 273.15); the same letter is a thermal conductivity in W/(m·K) in 25-08, by context;
- FIT = failures per 10⁹ device-hours; ppm = parts per million; $D_0$ is a defect density in cm⁻² and die areas $A$ in a yield exponent are in cm² (1 cm² = 100 mm²);
- $\eta$ and $\beta$ are a Weibull scale and shape; $\eta$ is also a multisite efficiency (25-11) and $\eta_f$ a fin efficiency (25-08), by context; $\alpha$ is a negative-binomial clustering parameter (25-04), a CTE (25-06, 25-07) or the alpha-power exponent (25-05, 25-12);
- $\Phi$ is the standard normal CDF and $\operatorname{erf}$ the error function; $\chi^2_{CL,\nu}$ is the chi-square quantile at confidence $CL$ with $\nu$ degrees of freedom.

## Process flow (25-01)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $x^2 + Ax = B(t + \tau)$; $A = 2D(1/k_s + 1/h)$, $B = 2DC^*/N_1$ | Deal–Grove oxidation; $\tau$ accounts for an initial oxide $x_i$ | [25-01](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-01-process-flow-overview.md) |
| $t = x^2/B + x/(B/A)$; linear $x \approx (B/A)t$ for $x \ll A$, parabolic $x \approx \sqrt{Bt}$ for $x \gg A$ | From bare silicon; the two terms are equal at $x = A$ | [25-01](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-01-process-flow-overview.md) |
| $d_{Si} = 0.44\,x$ | Silicon consumed per oxide thickness ($N_{ox}/N_{Si}$) | [25-01](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-01-process-flow-overview.md) |
| $R_c = \rho_c/A_c$; $I_D' = I_D/(1 + g_mR_S)$ | Contact resistance and source degeneration by it | [25-01](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-01-process-flow-overview.md) |
| $t_{50} = 0.379\,RC$ for a distributed line, $\propto L^2/s^2$ | $R$, $C$ are the wire's totals; scaling width and spacing by $s$ | [25-01](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-01-process-flow-overview.md) |
| $Y = \prod y_i \approx \exp[-\sum(1 - y_i)]$ | Line yield over many steps | [25-01](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-01-process-flow-overview.md) |
| WIP $= \lambda T$ | Little's law: starts rate × cycle time | [25-01](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-01-process-flow-overview.md) |

## Lithography (25-02)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $n\sin\theta_m = s_0 + m\lambda/p$ | Grating orders from a mask of pitch $p$ | [25-02](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-02-lithography.md) |
| $p_{min} = \lambda/\text{NA}$ on-axis; $\lambda/(2\text{NA})$ off-axis | Two-beam imaging; half-pitch $k_1\lambda/\text{NA}$ with $k_1 \ge 0.25$ | [25-02](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-02-lithography.md) |
| DOF $\approx n\lambda/(2\text{NA}^2)$ | Small-NA approximation; exact form $\lambda/\{4n[1 - \sqrt{1 - (\text{NA}/n)^2}]\}$ | [25-02](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-02-lithography.md) |
| $N = DA/(hc/\lambda)$; relative shot noise $1/\sqrt N$ | Photons per feature at dose $D$ | [25-02](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-02-lithography.md) |
| wph $= 3600\ \text{s}/(t_{oh} + t_{exp})$, $t_{exp} \propto D/P$ | Scanner throughput | [25-02](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-02-lithography.md) |
| $c_{pass} = \text{price}/(\text{years} \times 8766\ \text{h} \times \text{availability} \times \text{wph})$ | Depreciation per exposure pass | [25-02](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-02-lithography.md) |

## Unit processes (25-03)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $v = [k_sh_g/(k_s + h_g)]\,C_g/N$ | CVD: reaction-limited if $k_s \ll h_g$, transport-limited if $h_g \ll k_s$ | [25-03](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-03-deposition-etch-cmp-implant-metrology.md) |
| $t_{film} = n_{cycles} \times \text{GPC}$ | Atomic-layer deposition | [25-03](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-03-deposition-etch-cmp-implant-metrology.md) |
| $dt_{Cu}/dt = jM/(nF\rho)$ | Faraday's law for electroplating | [25-03](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-03-deposition-etch-cmp-implant-metrology.md) |
| $RR = K_pPv$ | Preston's CMP removal rate | [25-03](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-03-deposition-etch-cmp-implant-metrology.md) |
| $t = QqA/I$ | Implant time for dose $Q$ over area $A$ at beam current $I$ | [25-03](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-03-deposition-etch-cmp-implant-metrology.md) |
| $N_p = Q/(\sqrt{2\pi}\Delta R_p)$; $x_j = R_p + \Delta R_p\sqrt{2\ln(N_p/N_B)}$ | Gaussian implant and its junction in background $N_B$ | [25-03](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-03-deposition-etch-cmp-implant-metrology.md) |
| $\Delta R_p'^2 = \Delta R_p^2 + 2Dt$; $N_p' = N_p\Delta R_p/\Delta R_p'$ | Anneal broadens the profile, conserving dose | [25-03](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-03-deposition-etch-cmp-implant-metrology.md) |
| $\sigma_{obs} = \sqrt{\sigma_p^2 + \sigma_m^2}$ | Metrology error adds in quadrature | [25-03](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-03-deposition-etch-cmp-implant-metrology.md) |

## Yield and die cost (25-04)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| DPW $\approx \pi d^2/(4A) - \pi d/\sqrt{2A}$ | Gross dies per wafer of diameter $d$ | [25-04](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md) |
| $Y = \int_0^\infty e^{-AD}f(D)\,dD$ | Yield averaged over the defect-density distribution | [25-04](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md) |
| Poisson $e^{-AD_0}$; Murphy $[(1 - e^{-AD_0})/AD_0]^2$; negative binomial $(1 + AD_0/\alpha)^{-\alpha}$ | Uniform, triangular and gamma-distributed $D$; small $\alpha$ = strong clustering | [25-04](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md) |
| $C_{die} = C_w/(\text{DPW} \times Y)$ | Cost per good die | [25-04](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md) |
| $Y_{\ge n-1} = y_u[y_c^n + ny_c^{n-1}(1 - y_c)]$ | Harvesting: one spare among $n$ cores | [25-04](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md) |
| $D_0(t) = D_\infty + (D_{start} - D_\infty)e^{-t/\tau}$ | Yield learning | [25-04](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md) |
| $C_{transistor} \propto C_w/(\text{density} \times Y)$ | Why cost per transistor stalls when wafer cost rises as fast as density | [25-04](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md) |

## Foundries and process options (25-05)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| delay $\propto V/(V - V_{TH})^{\alpha}$ | Alpha-power law; corners shift $V_{TH}$ | [25-05](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-05-foundries-pdks-specialty-processes.md) |
| $\Delta V_{TH}/\Delta V_{BG} = -C_{Si}C_{BOX}/[C_{ox}(C_{Si} + C_{BOX})]$ | FD-SOI back-gate coupling; $C = \varepsilon/t$ per layer | [25-05](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-05-foundries-pdks-specialty-processes.md) |
| $C_{MPW} = \max(A, A_{min}) \times p_{mm^2}$ | Multi-project wafer slot | [25-05](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-05-foundries-pdks-specialty-processes.md) |

## Packaging (25-06)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $N_{peri} \approx 4D/p_w$; $N_{area} \approx (D/p_a)^2$; area wins for $D > 4p_a^2/p_w$ | Single-row perimeter pads vs a full area array on a die of side $D$ | [25-06](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-06-packaging-fundamentals.md) |
| $n = \lfloor(p - d - s)/(w + s)\rfloor$; layers $L = \lceil R/(n + 1)\rceil$ | Traces between pads of diameter $d$; escaping $R$ rows | [25-06](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-06-packaging-fundamentals.md) |
| $\gamma \approx \Delta\alpha\,\Delta T\,L_{DNP}/h$ | Solder-joint shear strain | [25-06](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-06-packaging-fundamentals.md) |
| $N_f \propto \gamma^{-n}$ | Coffin–Manson low-cycle fatigue ($n \approx 2$ for solder) | [25-06](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-06-packaging-fundamentals.md) |
| $R_{pkg}(N) = \exp[-N^\beta\sum\eta_i^{-\beta}]$; $\eta_{pkg} = (\sum\eta_i^{-\beta})^{-1/\beta}$ | Weakest link, common shape; $N$ identical joints: $\eta N^{-1/\beta}$ | [25-06](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-06-packaging-fundamentals.md) |

## Advanced packaging and chiplets (25-07)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $N_{edge} = L/(w + s)$ per layer | Wires per mm of die edge (with $w + s$ in mm) | [25-07](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md) |
| $n_{bond} = 1/p^2$; overlay budget $\lvert e\rvert \le p/4$ per axis | Hybrid-bond density and alignment for pads $p/2$ wide | [25-07](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md) |
| $Y_{bond} = [\operatorname{erf}(p/(4\sigma\sqrt2))]^2$ | Gaussian placement error $\sigma$ per axis | [25-07](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md) |
| $\Delta T_{close} = \delta/[(\alpha_{Cu} - \alpha_d)t]$ | Anneal to close a copper recess $\delta$ in a pad of thickness $t$ | [25-07](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md) |
| $e = (1 - Y)(1 - c)/[Y + (1 - Y)(1 - c)]$ | Test escapes among passing dies, coverage $c$ | [25-07](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md) |
| $Y_{pkg} = y_a^n\prod(1 - e_i)$ | Package yield with attach yield $y_a$ per part | [25-07](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md) |
| $C = [\sum(cA_i + t)/Y_i + P]/y_a^n$ | Cost per good package: silicon $c$/mm², test $t$, package $P$ | [25-07](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md) |

## Thermal (25-08)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $R_{th} = t/(kA)$; $T_J = T_{fluid} + P\sum R_i$ | Conduction slab; series network | [25-08](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-08-thermal-engineering.md) |
| $\Delta T_{centre} = qa/k$; $R_{sp} = 8/(3\pi^2ka) \approx 0.270/(ka)$ | Uniform flux $q$ on a disk of radius $a$ on a half-space; average-temperature resistance | [25-08](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-08-thermal-engineering.md) |
| $R_{45} = t/[k\pi a(a + t)]$ | 45° spreading cone through thickness $t$ | [25-08](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-08-thermal-engineering.md) |
| $R_{conv} = 1/(hA)$ | Convection | [25-08](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-08-thermal-engineering.md) |
| $m = \sqrt{2h/(kt_f)}$; $\eta_f = \tanh(mL)/(mL)$ | Thin straight fin, adiabatic tip | [25-08](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-08-thermal-engineering.md) |
| $\Delta T_{fluid} = P/(\rho\dot Vc_p)$; $T_J \approx T_{in} + \Delta T_{fluid}/2 + P\sum R$ | Liquid cooling, mean coolant temperature | [25-08](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-08-thermal-engineering.md) |
| $T_{eq} = -E_a/\{k\ln[\sum w_ie^{-E_a/kT_i}]\}$ | Arrhenius-equivalent temperature of a mission profile | [25-08](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-08-thermal-engineering.md) |

## Reliability physics (25-09)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $AF_T = \exp[(E_a/k)(1/T_{use} - 1/T_{stress})]$ | Arrhenius acceleration | [25-09](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md) |
| $MTTF = Aj^{-n}e^{E_a/kT}$; current factor $(j_s/j_u)^n$ | Black's equation for electromigration | [25-09](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md) |
| $MTTF = Bj^{-2} + Cj^{-1}$; $n(x) = (2 + x)/(1 + x)$, $x = j/j^*$, $j^* = B/C$ | Two-phase (nucleation + growth) EM model | [25-09](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md) |
| $jL < (jL)_c = \Omega\Delta\sigma_c/(Z^*e\rho)$ | Blech immortality | [25-09](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md) |
| E: $t_{BD} = Ae^{-\gamma E}e^{E_a/kT}$; 1/E: $\tau_0e^{G/E}$; power law $t_{BD} \propto E^{-m}$ | Dielectric breakdown models; the E model is the most conservative | [25-09](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md) |
| $t_F^{chip} = \eta_{test}(A_{chip}/A_{test})^{-1/\beta}[-\ln(1 - F)]^{1/\beta}$ | Weibull area scaling to a failure fraction $F$ | [25-09](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md) |
| $\Delta V_{TH} = At^{n_t}$ | BTI power law in stress time | [25-09](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md) |
| $I_{pk} = (V_0 - V_h)/(R_{HBM} + R_{on})$; $V_{pad} = V_h + I_{pk}R_{on}$ | ESD clamp in an HBM event ($R_{HBM}$ = 1.5 kΩ) | [25-09](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md) |
| $\lambda_U = \chi^2_{CL,2f+2}/(2NtAF)$ | Upper bound on failure rate from $f$ failures in $N$ units × $t$ hours | [25-09](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md) |

## Qualification and functional safety (25-10)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $AF_{TC} = (\Delta T_s/\Delta T_{field})^n$ | Temperature-cycling acceleration (Coffin–Manson) | [25-10](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-10-qualification-and-functional-safety.md) |
| $t_{stress} = \sum w_it_{life}/AF(T_i \to T_{stress})$ | Stress time covering a mission profile | [25-10](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-10-qualification-and-functional-safety.md) |
| SPFM $= 1 - \sum(\lambda_{SPF} + \lambda_{RF})/\sum\lambda$ | Single-point fault metric; $\lambda_{RF} = \lambda_{dangerous}(1 - DC)$ | [25-10](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-10-qualification-and-functional-safety.md) |
| LFM $= 1 - \sum\lambda_{MPF,L}/\sum(\lambda - \lambda_{SPF} - \lambda_{RF})$ | Latent fault metric | [25-10](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-10-qualification-and-functional-safety.md) |
| PMHF $\approx \sum(\lambda_{SPF} + \lambda_{RF}) + \lambda_L\lambda_D\tau$ | Dual-point term for a latent fault exposed for a mean time $\tau$ | [25-10](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-10-qualification-and-functional-safety.md) |
| ASIL B/C/D: SPFM ≥ 90/97/99%; LFM ≥ 60/80/90%; PMHF < 100/100/10 FIT | ISO 26262 (2018) hardware targets | [25-10](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-10-qualification-and-functional-safety.md) |
| $P(\ge 1\ \text{bad}) = 1 - (1 - p)^N \approx Np$ | Vehicle with $N$ components at defect rate $p$ | [25-10](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-10-qualification-and-functional-safety.md) |

## Test (25-11)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $c_{test} = r(T_N + t_i)/N$ per die; $c_{good} = c_{test}/Y$ | Cell rate $r$, $N$ sites, index time $t_i$ | [25-11](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-11-test-ate-sort-burn-in.md) |
| $\eta = 1 - (T_N - T_1)/[(N - 1)T_1]$; $T_N = T_1[1 + (N - 1)(1 - \eta)]$ | Multisite efficiency | [25-11](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-11-test-ate-sort-burn-in.md) |
| Escape $= P(F < L,\ F + e \ge L + g)$; overkill $= P(F \ge L,\ F + e < L + g)$ | Parametric screen with tester error $e$ and guard band $g$ | [25-11](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-11-test-ate-sort-burn-in.md) |
| Bin fraction $= \Phi((b - \mu)/\sigma) - \Phi((a - \mu)/\sigma)$ | Gaussian $F_{max}$ between thresholds $a$ and $b$ | [25-11](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-11-test-ate-sort-burn-in.md) |
| $AF\,t_b = \eta_w[\ln(p_w/q)]^{1/\beta}$ | Burn-in that cuts a weak fraction $p_w$ to $q$ (weak Weibull $\eta_w$, $\beta$) | [25-11](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-11-test-ate-sort-burn-in.md) |

## Post-silicon validation (25-12)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Storage $= S \times D$ bits; window $= D/f$ | Trace buffer of $S$ signals and depth $D$ at clock $f$ | [25-12](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-12-post-silicon-validation.md) |
| $F_{max}(V) = K(V - V_{TH})^\alpha/V$ | Alpha-power shmoo boundary; $V_{min}$ by inversion | [25-12](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-12-post-silicon-validation.md) |
| $m(t) = a(1 - e^{-bt})$; remaining $a - m(t)$; $t_q = \ln[1/(1 - q)]/b$ | Goel–Okumoto bug-discovery model | [25-12](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-12-post-silicon-validation.md) |
| Expected cost $= \sum p_i C_i$; break-even $p$ where the branches are equal | Metal-only vs full respin decision tree | [25-12](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-12-post-silicon-validation.md) |
| $n \approx 1 + z^2/(2\delta^2)$ | Parts to know σ within a fraction $\delta$ | [25-12](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-12-post-silicon-validation.md) |
| $[\hat p + z^2/2n \pm z\sqrt{\hat p(1 - \hat p)/n + z^2/4n^2}]/(1 + z^2/n)$ | Wilson score interval for a proportion | [25-12](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-12-post-silicon-validation.md) |

## Numbers to know

| Quantity | Typical value | Chapter |
|---|---|---|
| ArF immersion / EUV / High-NA EUV wavelength and NA | 193 nm, 1.35 / 13.5 nm, 0.33 / 13.5 nm, 0.55 | 25-02 |
| Silicon consumed by thermal oxide | 0.44 of the oxide thickness | 25-01 |
| Thermal conductivity: Si, Cu, Al | 150, 400, 200 W/(m·K) | 25-08 |
| Solder-joint Coffin–Manson exponent | about 2 | 25-06 |
| EM activation energy, Cu along its cap interface | about 0.9 eV (an early-failure mode at 0.83 eV); current exponent $n$ about 1–3 | 25-09 |
| HBM ESD model | 100 pF through 1.5 kΩ | 25-09 |
| ISO 26262 ASIL D | SPFM ≥ 99%, LFM ≥ 90%, PMHF < 10 FIT | 25-10 |

Perishable values (prices, capacities, market shares, survey results) are in the chapters with their dates and research-log IDs; they are deliberately left off this sheet.
