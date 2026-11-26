# Equation Sheet · 26 Engineering Design and Professional Practice

The relations to know cold from Course 26, each with its conditions and the chapter that derives it.

Conventions:

- money in dollars unless stated; $i$ is the interest rate (MARR) per period; cash flows at period ends;
- $\Phi$ is the standard normal CDF; FIT = failures per 10⁹ device-hours;
- dies per wafer use $\pi d^2/(4A) - \pi d/\sqrt{2A}$ (rounded down) and die yield is Poisson $e^{-AD_0}$ with $A$ in cm² (25-04).

## Requirements and budgets (26-01)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\bar I = \sum_i d_iI_i$; $t_{life} = uQ/\bar I$ | Duty-cycle average current; usable fraction $u$ of capacity $Q$ | [26-01](../../courses/26-engineering-design-and-professional-practice/chapters/26-01-requirements-and-specifications.md) |
| $\lvert E\rvert \le \sum_i b_i$ | Worst-case stack of error bounds | [26-01](../../courses/26-engineering-design-and-professional-practice/chapters/26-01-requirements-and-specifications.md) |
| $\sigma_E = \sqrt{\sum_i\sigma_i^2 + 2\sum_{i<j}\rho_{ij}\sigma_i\sigma_j}$ | RSS budget; independent terms drop the cross sum | [26-01](../../courses/26-engineering-design-and-professional-practice/chapters/26-01-requirements-and-specifications.md) |
| $P_{out} = 1 - \Phi\big(\frac{L - \mu}{\sigma_E}\big) + \Phi\big(\frac{-L - \mu}{\sigma_E}\big)$ | Fraction outside a ±$L$ specification for a normal total | [26-01](../../courses/26-engineering-design-and-professional-practice/chapters/26-01-requirements-and-specifications.md) |
| $C = N[p_1c_1 + (1 - p_1)\bar c_{down}]$; $\partial C/\partial p_1 = -N(\bar c_{down} - c_1)$ | Error-cost escalation; $\bar c_{down} = \sum_{k\ge2} c_kp_k\prod_{2\le m<k}(1 - p_m)$, with $p$ = 1 for the last stage (the field) | [26-01](../../courses/26-engineering-design-and-professional-practice/chapters/26-01-requirements-and-specifications.md) |
| $S_a = \sum_j w_js_{aj}$; tie weight $w^* = \frac{R_a - R_b}{(R_a - R_b) - (s_{ac} - s_{bc})}$ | Weighted decision matrix; $R$ = average over the other criteria | [26-01](../../courses/26-engineering-design-and-professional-practice/chapters/26-01-requirements-and-specifications.md) |

## Reviews and standards (26-02)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $P_{found}(k) = 1 - (1 - p)^k$; $E[\text{escapes}] = N(1 - p)^k$ | $k$ independent reviewers, equal detection $p$ | [26-02](../../courses/26-engineering-design-and-professional-practice/chapters/26-02-design-reviews-and-standards.md) |
| $C(k) = kC_r + C_eN(1 - p)^k$; optimum: the largest integer $k$ with $k \le 1 + \frac{\ln[C_r/(C_eNp)]}{\ln(1 - p)}$ | Cost-optimal team | [26-02](../../courses/26-engineering-design-and-professional-practice/chapters/26-02-design-reviews-and-standards.md) |
| $P_{found}(k) = \sum_j f_j[1 - (1 - p_j)^k]$ | Defect classes of different difficulty; ceiling $\sum_{p_j>0}f_j$ | [26-02](../../courses/26-engineering-design-and-professional-practice/chapters/26-02-design-reviews-and-standards.md) |
| $\hat N = n_1n_2/m$; Chapman $\hat N_C = \frac{(n_1 + 1)(n_2 + 1)}{m + 1} - 1$ | Capture–recapture; Lincoln–Petersen is biased high for small samples and Chapman stays finite at $m$ = 0; both read low when difficulty varies | [26-02](../../courses/26-engineering-design-and-professional-practice/chapters/26-02-design-reviews-and-standards.md) |
| Return ≥ 75% of the balloting group; Approve ≥ 75% of Approve + Do Not Approve; invalid at ≥ 30% abstentions | IEEE SA ballot rules [R-632] | [26-02](../../courses/26-engineering-design-and-professional-practice/chapters/26-02-design-reviews-and-standards.md) |
| $R = B\sum_ir_i$; top-down $R_i = r_{agg}Bs_i$ | Royalty stacking on base $B$; changing the base from device to chip scales $R$ by the price ratio | [26-02](../../courses/26-engineering-design-and-professional-practice/chapters/26-02-design-reviews-and-standards.md) |

## Engineering economics I (26-03)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $C_{die} = C_w/(\text{DPW}\,Y)$; $C_{good} = \frac{(C_{die} + C_{pkg})/Y_{asm} + C_{test}}{Y_{test}}$ | Cascaded cost stack: yields divide accumulated cost | [26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md) |
| GM $= (\text{ASP} - \text{COGS})/\text{ASP}$; markup $= \text{GM}/(1 - \text{GM})$ | | [26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md) |
| $V^* = \text{NRE}/(\text{ASP} - \text{COGS})$ | Break-even volume | [26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md) |
| $(F/P) = (1 + i)^n$; $(P/A) = \frac{1 - (1 + i)^{-n}}{i}$; $(A/P) = \frac{i(1 + i)^n}{(1 + i)^n - 1}$; $(F/A) = \frac{(1 + i)^n - 1}{i}$ | FE interest factors; $(A/F) = (A/P) - i$ | [26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md) |
| $i_{eff} = (1 + r/m)^m - 1$; continuous $e^r - 1$ | Nominal $r$ compounded $m$ times a year | [26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md) |
| CR $= P(A/P) - S(A/F)$; EUAC = CR + annual operating cost | Capital recovery with salvage $S$ | [26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md) |
| NPV $= \sum_t CF_t(1 + i)^{-t}$; IRR: NPV = 0 | Program value; payback from cumulative cash | [26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md) |
| $D = (P - S)/n$ | Straight-line depreciation; tax shield $tD$ a year | [26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md) |

## Engineering economics II (26-04)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $U = \sum_t V_t(1 + i)^{-t}$ | Discounted unit stream; a per-unit charge $r$ is worth $rU$ | [26-04](../../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md) |
| $\text{PV}_L = F + rU$; $\text{PV}_B = N_B + p_sC_s$; $U^* = (N_B + p_sC_s - F)/r$ | License against build | [26-04](../../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md) |
| Percentage royalty PV $= \rho\sum_t P_tV_t(1 + i)^{-t}$; $r_{eq}$ = PV/$U$ | A percentage royalty puts the price risk on the licensor; with erosion $e$ a year, $P_t = P_1(1 - e)^{t-1}$ | [26-04](../../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md) |
| $R = \sum_k r_k + P\sum_k\rho_k$ | Royalty stacking; margin falls by $R/P$ | [26-04](../../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md) |
| $s_{eff} = 1/\sum_k(f_k/s_k)$ | Mix-weighted density gain (harmonic mean); capped by the non-shrinking blocks | [26-04](../../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md) |
| $\frac{C_{new}}{C_{old}} \approx \frac{W_{new}}{W_{old}}\cdot\frac{1}{s_{eff}}\cdot\frac{Y_{old}}{Y_{new}}$; $V^* = \frac{\Delta N}{C_{old} - C_{new} + \Delta v}$ | Node choice | [26-04](../../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md) |
| $C_{pkg} = \frac{\sum_k(W_k/\text{DPW}_k + T)/Y_k + P}{a^n}$; family total $= \text{NRE} + \sum_jV_jC_j$ | Chiplets; reuse lowers NRE | [26-04](../../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md) |
| $T = P + O + E$, $E = P_{el}\,\text{PUE}\,8760L\,c_e$; $\tau = T/\theta$ | Accelerator TCO per unit of throughput | [26-04](../../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md) |
| $N_{eq}^* = N/(\tau_m - \tau_c)$; $P_m^* = \theta_m(\tau_c + N/N_{eq}) - O - E_m$ | Break-even fleet; merchant price ceiling | [26-04](../../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md) |
| $E[\min(X, Y)] \le \min(E[X], E[Y])$ | Free flexibility never has negative value | [26-04](../../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md) |

## Schedule and risk (26-05)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\mu = (a + 4m + b)/6$, $\sigma = (b - a)/6$ | PERT; means and variances add along a path | [26-05](../../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md) |
| $P(\max_jD_j \le T) = \prod_j P(D_j \le T)$ | Merge bias at a join of independent paths | [26-05](../../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md) |
| $E[N] = 1 + (1 - q_1) + (1 - q_1)(1 - q_2) + \cdots$; geometric $1/q$; expected delay $(E[N] - 1)t_r$ for respin time $t_r$ | Expected tape-outs | [26-05](../../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md) |
| Fab time ≈ layers × days per layer | Full respin against metal-only ECO from held wafers | [26-05](../../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md) |
| EMV $= \sum_ip_iC_i$; mitigate if $(p_i - p_i')C_i > M_i$ | Risk register | [26-05](../../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md) |
| $\lambda(t) = \phi N_0e^{-t/\tau}$; $P_r = 1 - e^{-\lambda}$; $f(t) = c_wt + C_rP_r$ | Bug discovery and Poisson escapes | [26-05](../../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md) |
| $\lambda^*e^{-\lambda^*} = c_w\tau/C_r$ (smaller root); $t^* = \tau\ln(\phi N_0/\lambda^*)$ | Optimal tape-out; the larger root is the cost maximum | [26-05](../../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md) |
| $P_{miss} = \Phi(-\Delta/\sigma)$ | Margin $\Delta$ against a normal model error | [26-05](../../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md) |

## Teams (26-06)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Channels $= n(n - 1)/2$ | Pairwise communication | [26-06](../../courses/26-engineering-design-and-professional-practice/chapters/26-06-team-structures-and-sizing.md) |
| $O(n) = n[1 - c(n - 1)]$; $n^* = (1 + 1/c)/2$; zero at $n = 1 + 1/c$ | Flat-team output with coordination cost $c$ | [26-06](../../courses/26-engineering-design-and-professional-practice/chapters/26-06-team-structures-and-sizing.md) |
| $O = km[1 - c(m - 1)][1 - c_x(k - 1)]$ | $k$ teams of $m$ with a cross-team cost $c_x$ | [26-06](../../courses/26-engineering-design-and-professional-practice/chapters/26-06-team-structures-and-sizing.md) |
| $T_{add} = r + \frac{W - (n - \mu a)er}{(n + a)e}$, $e = 1 - c(n + a - 1)$ | Brooks's law: $a$ hires with ramp $r$, each taking a fraction $\mu$ of an experienced engineer's time during the ramp (here $\mu$ is not a PERT mean); valid if $W > (n - \mu a)er$; without hires $T_0 = W/(ne_0)$, $e_0 = 1 - c(n - 1)$ | [26-06](../../courses/26-engineering-design-and-professional-practice/chapters/26-06-team-structures-and-sizing.md) |
| Managers ≈ $N/(s - 1)$; layers ≈ $\lceil\log_sN\rceil$ | Span of control $s$ | [26-06](../../courses/26-engineering-design-and-professional-practice/chapters/26-06-team-structures-and-sizing.md) |
| Add base staff while $P(L > B) > C_e/C_c$ | Newsvendor rule; break-even utilization $C_e/C_c$ | [26-06](../../courses/26-engineering-design-and-professional-practice/chapters/26-06-team-structures-and-sizing.md) |
| Engineer-years $= \ell D/w$ | Design cost to people | [26-06](../../courses/26-engineering-design-and-professional-practice/chapters/26-06-team-structures-and-sizing.md) |

## Ethics, safety and compliance (26-07)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $P_{any} = 1 - (1 - p)^N \approx 1 - e^{-Np}$ | Fleet-level risk | [26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md) |
| $E[\text{failures}] = \lambda_{FIT} \times 10^{-9} \times Nt$ | Failures across a fleet's device-hours | [26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md) |
| $P_{both} \approx \beta p + [(1 - \beta)p]^2$ | Beta-factor common cause; dominates once $\beta \gtrsim p$ | [26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md) |
| $\lambda_U = -\ln(1 - C)/T$ (≈ 3/T at 95%); with $k$ failures $\chi^2_{C,2k+2}/(2T)$ | Upper confidence bound on a rate | [26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md) |
| TPP $= 2 \times \text{MacTOPS} \times$ bit length; density = TPP/mm² | 2023 ECCN 3A090.a.1: TPP ≥ 4800; 3A090.a.2: TPP ≥ 1600 with density ≥ 5.92; 3A090.b.1: 2400 ≤ TPP < 4800 with 1.6 ≤ density < 5.92; 3A090.b.2: TPP ≥ 1600 with 3.2 ≤ density < 5.92; items not designed or marketed for datacenters are excluded below TPP 4800 [R-659] | [26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md) |
| Patent: 20 years from filing; mask work: 10 years, to year end | US terms [R-658] | [26-07](../../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md) |
