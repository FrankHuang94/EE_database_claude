# Equation Sheet · 28 Technical Diligence and Engineering Leadership Fluency

The relations to know cold from Course 28, each with its conditions and the chapter that derives it.

Conventions:

- probabilities as fractions, odds $O = P/(1 - P)$, likelihood ratios dimensionless;
- money in the units of each chapter ($M unless stated), discount rates per year;
- a year is 8,766 hours in 28-05 to 28-10;
- sensitivities, false-positive rates, prior weights and likelihood ratios in the chapters are illustrative assumptions; sourced values are dated in each chapter's §7 and §9.

## A framework for evaluating a chip company (28-01)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $S = \sum_i w_is_i$; $G = \prod_i s_i^{w_i}$ | Weighted arithmetic and geometric scores; $G$ punishes a weak dimension; gates override both | [28-01](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md) |
| $\sigma_S^2 = \sum_i w_i^2\sigma_i^2$ (+ $2\rho\sum_{i<j}w_iw_j\sigma_i\sigma_j$); $P(D < 0) = \Phi(-\mu_D/\sigma_D)$ | Score uncertainty and the chance two targets' ranking reverses | [28-01](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md) |
| $O(T \mid E) = O(T)\,\Lambda$, $\Lambda = P(E \mid T)/P(E \mid \bar T)$ | Bayes in odds form; independent evidence multiplies | [28-01](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md) |
| $\Lambda_{\text{req}} = \frac{p_1/(1 - p_1)}{p_0/(1 - p_0)}$ | Evidence needed to move a belief from $p_0$ to $p_1$ | [28-01](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md) |
| $P = \prod_j p_j$; $PV = pX/(1 + r)^t$ | Milestone chains; an earn-out to a risk-neutral party | [28-01](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md) |
| $\text{EVPI} = pU - \max(pU + (1 - p)L, 0)$ | Upper bound on what any diligence step is worth | [28-01](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md) |

## Validating claims (28-02)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $F_{\text{peak}} = 2N_{\text{MAC}}f\,k_{\text{prec}}k_{\text{sparse}}$ | Peak operations per second; state precision and sparsity | [28-02](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md) |
| $\text{TPP} = 2 \times \text{MacTOPS} \times$ bit length | Precision-normalized; export thresholds use it | [28-02](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md) |
| $F_{\text{att}} = \min(F_{\text{peak}}, IB)$; ridge $F_{\text{peak}}/B$ | Roofline; utilization $u = F_{\text{delivered}}/F_{\text{peak}}$ | [28-02](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md) |
| $E_{\text{op}} = 1/(\eta \times 10^{12})$ J; $E_{\text{op}} \ge E_{\text{arith}} + \sum_\ell E_\ell/I_\ell$ | TOPS/W as energy per operation, and its floor | [28-02](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md) |
| $P \propto CV^2f$ | Scale power between operating points | [28-02](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md) |
| $P_{\text{sys}} = k_{\text{sys}}P_{\text{card}}$; $P_{\text{fac}} = \text{PUE}\cdot P_{\text{sys}}$ | Power at successive boundaries; compare at the same one | [28-02](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md) |
| $\text{GM}_i(t_B/t_A)$; best of $N \approx m\,e^{\sigma E[Z_{(N)}]}$, $E[Z_{(N)}]$ = 1.16, 1.54, 1.87 for 5, 10, 20 | Geometric mean of ratios; best-of-N inflation | [28-02](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md) |

## Maturity scales (28-03)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $P_k = \prod_{j \ge k}p_j$; $T_k = \sum_{j \ge k}t_j$; $V_k/V = P_k/(1 + r)^{T_k/12}$ | Probability, months to go and value multiplier from level $k$ | [28-03](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-03-silicon-maturity-scales.md) |
| $\text{AF} = \exp\left[\frac{E_a}{k_B}\left(\frac{1}{T_u} - \frac{1}{T_s}\right)\right]$ | Arrhenius acceleration; $k_B = 8.617 \times 10^{-5}$ eV/K, kelvin | [28-03](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-03-silicon-maturity-scales.md) |
| $\lambda_C = \chi^2_{C;\,2r+2}/(2nt\,\text{AF})$; zero failures: $-\ln(1 - C)/T_{\text{eq}}$ | Failure-rate bound (× $10^9$ for FIT); sample size by inversion | [28-03](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-03-silicon-maturity-scales.md) |
| $m(t) = a(1 - e^{-bt})$; remaining $= ae^{-bt} = \lambda(t)/b$ | Goel–Okumoto defect discovery | [28-03](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-03-silicon-maturity-scales.md) |

## Question banks I: digital, AI, memory, interconnect, optics (28-04)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Reduction $= 1 - 1/[g_C(R/g_{\text{IPC}})^3]$ | Power cut at the new operating point an iso-power claim of ratio $R$ needs (against the old product, energy per operation falls by $1 - 1/R$) | [28-04](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-04-question-banks-digital-ai-memory-interconnect.md) |
| $I_{\text{decode}} = 2N_b/b_w$; ridge batch $N_b = b_wF/(2B_{\text{mem}})$ | Decode intensity with $N_b$ sequences and $b_w$ bytes per weight | [28-04](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-04-question-banks-digital-ai-memory-interconnect.md) |
| Stack GB/s = bits × Gb/s ÷ 8; power = bits/s × J/bit | Memory and link bandwidth and power | [28-04](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-04-question-banks-digital-ai-memory-interconnect.md) |
| Edge = bandwidth ÷ shoreline density; port pJ/bit = W ÷ bits/s | Die-to-die shoreline; optics per port | [28-04](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-04-question-banks-digital-ai-memory-interconnect.md) |
| Posterior odds = prior odds × Π LR (independent answers) | Scoring an interview | [28-04](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-04-question-banks-digital-ai-memory-interconnect.md) |

## Question banks II: analog, RF, power, packaging, embedded (28-05)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\text{ENOB} = (\text{SNDR} - 1.76)/6.02$; $\text{FoM}_W = P/(f_s2^{\text{ENOB}})$; $\text{FoM}_S = \text{SNDR} + 10\log_{10}(f_s/2P)$ | Converter figures of merit | [28-05](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md) |
| $\text{FoM}_S = 10\log_{10}(1/16kT) \approx 191.8$ dB at 300 K (ideal class-B bound $10\log_{10}(1/8kT) \approx 194.8$ dB) | Conservative 8kT·SNR reference line; a claim above about 192 dB needs an explanation | [28-05](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md) |
| $\text{SNR}_j = -20\log_{10}(2\pi f_{in}\sigma_t)$; noises add in power | Clock jitter | [28-05](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md) |
| Class B $\eta = (\pi/4)10^{-\text{BO}/20}$; Doherty $2\times$ that below half amplitude | Ideal PA efficiency at back-off | [28-05](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md) |
| $P_{\text{loss}} = P_{\text{out}}(1/\eta - 1)$; $\eta_{\text{chain}} = \prod\eta_i$ | Converter heat and chains | [28-05](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md) |
| Density $= 10^6/p^2$ per mm²; $Y_{\text{pkg}} = Y_{\text{asm}}\prod Y_i$; $T_j = T_{\text{ref}} + P\theta$ | Packaging | [28-05](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md) |
| $I_{\text{avg}} = I_{\text{sleep}} + \sum_k I_kt_k/T_k$ | Duty-cycled current; life = capacity ÷ $I_{\text{avg}}$ | [28-05](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md) |
| $C_{pk} = (\text{USL} - \mu)/3\sigma$; beyond-limit fraction $\Phi(-3C_{pk})$; $\sigma \le s\sqrt{(n - 1)/\chi^2_{1-C;\,n-1}}$ | Typical against guaranteed | [28-05](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md) |

## Red and green flags (28-06)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\text{LR}^+ = s/f$; $\text{LR}^- = (1 - s)/(1 - f)$ | A flag as a diagnostic test | [28-06](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-06-red-and-green-flags.md) |
| $P(\ge 1 \mid \text{healthy}) = 1 - (1 - f)^n \approx 1 - e^{-nf}$ | Checklist false alarms | [28-06](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-06-red-and-green-flags.md) |
| LR of $K \ge k$ = $P(K \ge k; n, s)/P(K \ge k; n, f)$ | Weight of a count *threshold* (a decision rule), valid only when all you know is that it was crossed | [28-06](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-06-red-and-green-flags.md) |
| LR of exactly $K = k$ = $(\text{LR}^+)^k(\text{LR}^-)^{n - k}$ | Weight of an *observed* count; use this to update | [28-06](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-06-red-and-green-flags.md) |
| $1 - (1 - q)^{mt}$; $\text{HHI} = \sum x_i^2$ (shares $x_i$), effective customers $1/\text{HHI}$ | Key-person risk; customer concentration | [28-06](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-06-red-and-green-flags.md) |
| $V = N p R \cdot \frac1n\sum(1 + r)^{-k}$ | Risk-adjusted design-win funnel | [28-06](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-06-red-and-green-flags.md) |

## Evaluating engineering teams (28-07)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\hat\theta = (\alpha_0 + s)/(n_0 + n)$; weight $n/(n_0 + n)$ | Beta-binomial track-record shrinkage | [28-07](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-07-evaluating-engineering-teams.md) |
| $\hat T = T_{\text{plan}}e^{\mu}$; $P(\text{on time}) = \Phi(-\mu/\sigma)$; $T_{90} = T_{\text{plan}}e^{\mu + 1.2816\sigma}$ | Reference-class schedule calibration (log-ratios) | [28-07](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-07-evaluating-engineering-teams.md) |
| $P(\text{lose}) = q^k$, or $c + (1 - c)q'^k$ with group departures | Bench depth | [28-07](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-07-evaluating-engineering-teams.md) |
| $T = Nt/(Cu)$; retained value $NV\rho$ | Regression capacity; retention | [28-07](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-07-evaluating-engineering-teams.md) |

## Integration risk (28-08)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\text{PV} = S[1 - (1 + r)^{-n}]/r$; late and partial: $\times\rho(1 + r)^{-d}$ | Synergy value | [28-08](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-08-integration-risk.md) |
| Lost gross profit $\approx m\,R\,d_m/12$ for $d_m$ months (revenue $R\,d_m/12$ times margin $m$) | Delay in a fixed market window; compare profit, not revenue, with a cost | [28-08](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-08-integration-risk.md) |
| Gain $= W[1 - P(\text{both fail}) - \max(p_1, p_2)]$ | Parallel paths | [28-08](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-08-integration-risk.md) |
| $\text{EL} = \sum_i p_iI_i$; earn-out PV $= pC(1 + r)^{-T}$ | Risk register; contingent payments | [28-08](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-08-integration-risk.md) |

## Business ↔ engineering translation (28-09)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\text{DPW} \approx \pi d^2/(4A) - \pi d/\sqrt{2A}$; $Y = e^{-AD_0}$; $C_{\text{die}} = W/(\text{DPW}\,Y)$ | Unit cost | [28-09](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md) |
| $\varepsilon = d\ln C/d\ln A \approx 1 + AD_0$ (+ edge) | Die-cost elasticity | [28-09](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md) |
| $\text{GM} = 1 - (C_{\text{die}} + C_{\text{pkg+test}})/\text{ASP}$ | Gross margin; reverse it for an area budget | [28-09](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md) |
| $E_{\text{cost}} = P\cdot\text{PUE}\cdot h\cdot p_e$; capacity gain $1/(1 - s) - 1$ | Customer energy and capacity | [28-09](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md) |
| Failures $= \lambda N t \times 10^{-9}$ | FIT to field failures | [28-09](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md) |

## Conversation scenarios (28-10)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Brier $= \frac1n\sum(p_i - o_i)^2$; $E = (p - q)^2 + q(1 - q)$ | Calibration; a proper scoring rule | [28-10](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-10-conversation-scenarios.md) |
| Group answers by cause, then multiply ratios | Debrief arithmetic | [28-10](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-10-conversation-scenarios.md) |
