# Course 25 · Final Exam Solutions

Exam: [README.md](README.md). Every number below is recomputed by [verify_25_exam.py](../verify/verify_25_exam.py). About half of the values are recomputed by a second route; the rest are closed-form re-evaluations of the same formulas:

- Question 1(a, b): oxide growth by integrating the Deal–Grove rate equation as an initial-value problem that stops at the target thickness;
- Question 3(a, c): the projected range and the annealed junction by root-finding on the Gaussian profile;
- Question 4(b): the clustered yields by integrating Poisson yield over a gamma-distributed (and a triangular) defect density;
- Question 5(a): the restoring supply by root-finding; 5(c): the burn-in times by solving the weak population's survival numerically;
- Question 7(b): the bond yield from the normal CDF; 7(c): the escape rate by Monte Carlo;
- Question 8(c): fin efficiency by solving the fin ODE as a boundary-value problem;
- Question 9(b): the E-model and power-law fits by least squares in transformed coordinates;
- Question 11(a): the time offset by integrating the growth law from the initial oxide; 11(b): the package scale and the corner fraction by integrating the survival and hazard functions; 11(c): the mean exposure by simulating fault arrivals; 11(d): the clustered yields by integration and the large-α limit;
- Question 12(a): the defect density by root-finding on the full cost model; 12(d): the Wilson bound by solving the score inequality.

---

## Solutions

### Solution 1

(a) From bare silicon, $t = x^2/B + x/(B/A)$ with $B/A = 0.0117/0.165$ = **0.0709** µm/h. For 0.10 µm, $0.01/0.0117 + 0.10/0.0709$ = **2.26** h; for 0.50 µm, $0.25/0.0117 + 0.50/0.0709$ = **28.4** h. Five times the thickness takes **12.5** times as long, because the parabolic (diffusion) term takes over.

(b) Silicon consumed is 0.44 of the oxide thickness, so the oxide must be $50/0.44$ = **114** nm. Then, with $x$ = **0.1136** µm, $t = 0.1136^2/0.0117 + 0.1136/0.0709$ = **2.71** h.

(c) The start rate is λ = 60,000/30 = 2,000 wafers a day, so Little's law gives $T = \text{WIP}/\lambda = 1.5 \times 10^5/2000$ = **75.0** days. At the same λ, cutting 20 days frees $2000 \times 20$ = **4.00e4** wafers of inventory, a working-capital release as much as a speed gain.

(d) $t_{50} = 0.3787RC = 0.3787 \times 24\ \text{k}\Omega \times 0.4\ \text{pF}$ = **3.64e3** ps (3.64 ns). Halving the length halves both $R$ and $C$: **909** ps, a quarter.

### Solution 2

(a) $p_{min} = \lambda/(2\,\text{NA})$: **71.5** nm (193 nm immersion), **20.5** nm (EUV) and **12.3** nm (High-NA).

(b) $13.5/0.33^2$ = **124** nm and $13.5/0.55^2$ = **44.6** nm. High-NA keeps $(0.33/0.55)^2$ = **0.360** of the focus budget: it gains resolution as $1/\text{NA}$ but loses focus as $1/\text{NA}^2$.

(c) Photon energy $hc/\lambda$ = **1.47e-17** J; the energy delivered is $300\ \text{J/m}^2 \times (20 \times 10^{-9}\ \text{m})^2$ = **1.20e-13** J, so **8.16e3** photons, and $1/\sqrt{N}$ = **1.11**% shot noise.

(d) $3600/(10 + 12)$ = **164** wafers per hour; with 24 s of exposure, **106** wph.

### Solution 3

(a) $N_p = Q/(\sqrt{2\pi}\,\Delta R_p) = 10^{15}/(2.507 \times 2 \times 10^{-6})$ = **1.99e20** cm⁻³. The junction lies $\Delta R_p\sqrt{2\ln(N_p/N_B)}$ beyond the peak, with $N_p/N_B$ = **1995**: $20\sqrt{2\ln 1995}$ = **78.0** nm. So $R_p = 150 - 78.0$ = **72.0** nm.

(b) With $2Dt = 4 \times 10^{-12}$ cm² = 400 nm², $\Delta R_p' = \sqrt{20^2 + 400}$ = **28.3** nm; the dose is conserved, so the peak falls in proportion to **1.41e20** cm⁻³.

(c) \$x_j' = R_p + \Delta R_p'\sqrt{2\ln(N_p'/N_B)} = 72.0 + \$ **28.28** $\sqrt{2\ln 1410}$ (with $N_p'/N_B$ = **1410**), where the second term is **107.7** nm, so $x_j'$ = **180** nm. The anneal moved the junction **29.8** nm deeper, which is why implant energies are chosen with the downstream thermal budget in mind.

(d) $k_{eff} = k_sh_g/(k_s + h_g) = 5/6$ = **0.833** cm/s: close to $k_s$, so the surface reaction limits the process (reaction-limited, and temperature-sensitive). For plating, Faraday's law inverted gives $j = x\,nF\rho/(Mt) = 10^{-4}\ \text{cm} \times 2 \times 96{,}485 \times 8.96/(63.55 \times 120\ \text{s})$ = **22.7** mA/cm². Units: cm × (C/mol) × (g/cm³)/((g/mol) × s) = C/(cm²·s) = A/cm². ✓

### Solution 4

(a) $\pi \times 300^2/600 - \pi \times 300/\sqrt{300}$ = **416.8**, so **417** dies.

(b) $AD_0 = 1.5 \times 0.15$ = **0.225**: Poisson $e^{-0.225}$ = **0.799** (unrounded **0.7985**, used below); Murphy $[(1 - e^{-0.225})/0.225]^2$ = **0.802**; negative binomial $(1 + 0.225/2)^{-2}$ = **0.808**.

(c) $18{,}000/(417 \times 0.7985)$ = **\$54.1**.

(d) $18{,}000/(417 \times 0.808)$ = **\$53.4**. Clustering concentrates defects on fewer dies, raising yield for the same average density; the difference is small for a modest die and grows with area (Solution 11(d)).

### Solution 5

(a) Delay ∝ $V/(V - V_{TH})^{1.3}$, so slow over typical is $(0.45/0.41)^{1.3}$ = **1.13**. To restore the typical delay, solve $f(V) = V/(V - 0.34)^{1.3}$ equal to the typical $0.75/0.45^{1.3}$ = **2.118**. Bisection: $f(0.80)$ = **2.195** (too slow), $f(0.85)$ = **2.040** (fast enough), and a few more halvings give $V$ = **0.824** V, **74** mV above nominal. The supply must rise by more than the 40 mV threshold shift because the $V$ in the numerator (the charge to be moved) grows too; slow-corner silicon pays this in power.

(b) In units of ε₀/nm, $C_{ox}$ = 3.9/1.0 = 3.9 and $C_{Si}$ = 11.7/6 = 1.95. The coupling is the series capacitance of body and BOX over $C_{ox}$, so the series value must be $0.075 \times 3.9$ = **0.2925**. Then $1/C_{BOX} = 1/0.2925 - 1/1.95$ = **2.906**, and $t_{BOX} = 3.9 \times 2.906$ = **11.3** nm. Cancelling 40 mV takes $40/75$ = **0.533** V of forward back-gate bias.

(c) A weak part survives use-equivalent time $t_e$ with probability $e^{-(t_e/\eta)^\beta}$, so the weak fraction left is $p_we^{-(t_e/\eta)^\beta}$. Setting it to $q$ gives $t_e = \eta[\ln(p_w/q)]^{1/\beta}$, with $\ln(0.01/50 \times 10^{-6}) = \ln 200$ = **5.30**.

- β = 0.5: $t_e = 200 \times 5.30^2$ = **5.61e3** h, so $t_b = 5.61 \times 10^3/40$ = **140** h.
- β = 1: $t_e = 200 \times 5.30$ = **1.06e3** h, so $t_b$ = **26.5** h.

The ratio of the two is $\ln 200$ itself, **5.30**: when the weak population's hazard falls with age (β < 1), the last weak parts are the hardest to find, and every further decade of screening costs more.

(d) Analog circuits, I/O and passives shrink little or not at all (their size is set by matching, noise, voltage and inductors), so a shrink cuts mainly the digital area while wafer cost rises.

### Solution 6

(a) $D = 4p_a^2/p_w = 4 \times 0.11^2/0.045$ = **1.08** mm.

(b) $n = \lfloor(130 - 75 - 10)/20\rfloor$ = **2** traces, so 3 rows per layer and $\lceil 18/3\rceil$ = **6** layers.

(c) $\gamma = 13.4 \times 10^{-6} \times 120 \times 12/0.08$ = **0.241**. The reference joint has $\gamma_0 = 13.4 \times 10^{-6} \times 100 \times 10/0.07$ = **0.191**, so life scales by $(0.191/0.241)^2$ = **0.630**.

(d) $500^{-1/5}$ = **0.289**.

### Solution 7

(a) $(1000/5)^2$ = **4.0e4** per mm²; budget **1.25** µm.

(b) $[\operatorname{erf}(1.25/(0.35\sqrt 2))]^2 = 0.99964^2$ = **99.93**%.

(c) $e = 0.15 \times 0.02/(0.85 + 0.003)$ = **0.352**%; $Y_{pkg} = 0.998^7(1 - 0.00352)(0.996)^6$ = **0.959**.

(d) Monolithic: $Y = e^{-0.72}$ = **0.487**, so $[(180 + 3)/0.487 + 50]/0.99$ = **\$430**. Chiplets: $Y = e^{-0.264}$ = **0.768**, so $[3(66 + 3)/0.768 + 90]/0.99^3$ = **\$371**. Ratio **0.861**.

### Solution 8

(a) $30 \times 10^{-6}/(4 \times 600 \times 10^{-6})$ = **0.0125** K/W; **12.5** K at 1,000 W.

(b) $q = 3/(\pi \times 0.4^2)$ W/mm²; centre rise $qa/k$ = **15.9** K; $R_{sp} = 8/(3\pi^2 \times 150 \times 0.4 \times 10^{-3})$ = **4.50** K/W.

(c) $m = \sqrt{2 \times 60/(200 \times 0.0008)}$ = **27.4** m⁻¹; $mL$ = **0.822**; $\eta_f = \tanh 0.822/0.822$ = **0.823**.

(d) $\Delta T = 1200/(1000 \times 4180 \times 2.5 \times 10^{-5})$ = **11.5** K. The mean coolant sits **5.74** K above the inlet, so $T_J = 40 + 5.74 + 1200 \times 0.030$ = **81.7** °C.

### Solution 9

(a) $AF_T = \exp[(0.85/k)(1/383.15 - 1/553.15)]$ = **2.73e3**; with $4^{1.5}$ = 8, total **2.18e4**.

(b) E model: $\gamma = \ln 10/0.5$ = **4.61** (MV/cm)⁻¹, and $t(6) = 30\,e^{4\gamma} = 30 \times 10^{4/0.5} = 30 \times 10^8$ = **3.00e9** s. Power law: $m = \ln 10/\ln(10/9.5)$ = **44.89**, and $t(6) = 30 \times (10/6)^{44.89}$ = **2.73e11** s, a factor of **91** longer.

(c) $1.8326 \times 10^9/(2 \times 2000 \times 1000 \times 50)$ = **9.16** FIT; with one failure, $4.0446/1.8326$ times that: **20.2** FIT.

(d) The two models have different shapes in field and agree only at the two stress points; extrapolating 3.5 MV/cm below them lets the shapes diverge, by the factor of 91 here. The E model predicts the shorter life and is the conservative one (25-09).

### Solution 10

(a) The field sees $15 \times 365.25 \times 3$ = **1.64e4** cycles of 50 K; the test range is 150 − (−55) = 205 K.

- $n$ = 2: $AF = (205/50)^2$ = **16.81**, so **16,436**/16.81 = **978** test cycles.
- $n$ = 2.5: $AF$ = **34.0**, so **483** cycles.

Grade 1's 1,000 cycles cover this profile for either exponent, but with almost no margin if $n$ is 2: the exponent, not the cycle count, is the assumption to challenge.

(b) Total **165** FIT (150 + 15); the dangerous rate is 150 − 50 = 100 FIT, so the residual is $0.02 \times 100$ = **2.0** FIT; latent $0.2 \times 15$ = **3.0** FIT. SPFM $= 1 - 2/165$ = **98.8**%; LFM $= 1 - 3/(165 - 2) = 1 - 3/$**163** = **98.2**%.

(c) SPFM meets ASIL C (≥ 97%) but not D (≥ 99%); LFM meets D (≥ 90%). The element supports **ASIL C** metrics; for D the diagnostic coverage must rise above **98.35**% (or the dangerous rate fall).

(d) $1 - (1 - 0.5 \times 10^{-6})^{12{,}000}$ = **0.598**%.

### Solution 11

(a) Separating variables, $(2x + A)\,dx = B\,dt$. Integrating from $x_i$ at $t = 0$ to $x$ at $t$:

$$
x^2 + Ax - (x_i^2 + Ax_i) = Bt \quad\Longrightarrow\quad x^2 + Ax = B(t + \tau),\qquad \tau = \frac{x_i^2 + Ax_i}{B} .
$$

The initial oxide behaves as if growth had started τ earlier from bare silicon. Here $\tau = (0.025^2 + 0.165 \times 0.025)/0.0117$ = **0.406** h, and $t = (0.30^2 + 0.165 \times 0.30)/0.0117 - \tau$ = **11.92** − 0.406 = **11.5** h. The 25 nm start saves less than half an hour, because a thin oxide grows quickly in the linear regime anyway.

(b) Joint $i$ survives to $t$ with probability $e^{-(t/\eta_i)^\beta}$; independence multiplies the survivals:

$$
R_{pkg}(t) = \exp\Bigl(-t^\beta\sum_i\eta_i^{-\beta}\Bigr) = \exp[-(t/\eta_{pkg})^\beta],\qquad \eta_{pkg} = \Bigl(\sum_i\eta_i^{-\beta}\Bigr)^{-1/\beta},
$$

a Weibull with the same shape. Each joint's hazard is $h_i(t) = \beta t^{\beta - 1}\eta_i^{-\beta}$, so with $S = \sum\eta_i^{-\beta}$ the package hazard is $h(t) = \beta t^{\beta - 1}S$ and group $G$'s is $h_G = (S_G/S)h$. The probability that the first failure is in $G$ is $\int_0^\infty h_G(t)R_{pkg}(t)\,dt = (S_G/S)\int_0^\infty h R_{pkg}\,dt = S_G/S$, since $hR_{pkg}$ is the package's failure density and integrates to 1. In units of $\eta_c^{-\beta}$, the other joints contribute $20{,}000 \times 3^{-4.5}$ = **142.6**, so $S$ = **542.6**, $\eta_{pkg} = 542.6^{-1/4.5}$ = **0.247** $\eta_c$, and the corners start **73.7**% of failures: 2% of the joints cause three-quarters of the failures, which is why corner joints get underfill fillets, dummy balls or larger pads.

(c) If faults arrive at random, a latent fault is equally likely to appear anywhere in the interval between tests, so the time until the next test reveals it is uniform on $[0, T]$, with mean $T/2$. During that exposure the element is unprotected: a dangerous fault the mechanism would have caught arrives with probability $\lambda_{DD}T/2$ (small), and the combination violates the safety goal. Multiplying by the arrival rate of latent faults gives the violation rate $\lambda_L\lambda_{DD}T/2$. Here $3 \times 10^{-9} \times 10^{-7} \times 1000$ /h = **3.00e-4** FIT. It reaches 0.01 FIT at $T = 2 \times 10^{-11}/(3 \times 10^{-9} \times 10^{-7})$ = **6.67e4** h, so a start-up test every drive cycle keeps this term negligible against a 10 FIT ASIL D budget.

(d) With $f(D) = D^{\alpha - 1}e^{-D/\theta}/[\Gamma(\alpha)\theta^\alpha]$ and $\theta = D_0/\alpha$ (so the mean is $\alpha\theta = D_0$):

$$
Y = \int_0^\infty e^{-AD}f(D)\,dD = \frac{1}{\Gamma(\alpha)\theta^\alpha}\int_0^\infty D^{\alpha - 1}e^{-D(A + 1/\theta)}\,dD = \frac{1}{\Gamma(\alpha)\theta^\alpha}\cdot\frac{\Gamma(\alpha)}{(A + 1/\theta)^\alpha} = (1 + A\theta)^{-\alpha} = \Bigl(1 + \frac{AD_0}{\alpha}\Bigr)^{-\alpha},
$$

using $\int_0^\infty D^{\alpha - 1}e^{-cD}dD = \Gamma(\alpha)/c^\alpha$. As α → ∞, $\ln Y = -\alpha\ln(1 + AD_0/\alpha) = -\alpha[AD_0/\alpha - (AD_0)^2/(2\alpha^2) + \dots] \to -AD_0$, the Poisson yield: a gamma density with infinite shape is a spike at $D_0$. With $AD_0$ = 0.6: α = 1 gives $1/1.6$ = **0.625**, α = 3 gives $1.2^{-3}$ = **0.579**, and Poisson gives $e^{-0.6}$ = **0.549**. Stronger clustering (smaller α) piles defects onto fewer dies and leaves more dies clean.

### Solution 12

(a) At $D_0$ = 0.1 cm⁻²: $Y_M = e^{-0.8}$ = **0.449** and $Y_C = e^{-0.22}$ = **0.803**, so $C_M = [(0.30 \times 800 + 3)/0.449 + 50]/0.99$ = **\$597** and $C_C = [4(0.30 \times 220 + 3)/0.803 + 110]/0.99^4$ = **\$473**: a saving of **20.8**%, not 30%. Solving $C_C/C_M = 0.70$ for $D_0$ (bisection on the two cost lines) gives $D_0$ = **0.122** cm⁻², **21.6**% above the model's value. There, $AD_0$ is **0.973** for the monolithic die and **0.268** per chiplet, $Y_M$ = **0.378** and $Y_C$ = **0.765**, and

$$
C_M = \frac{243/0.378 + 50}{0.99} = \$700, \qquad C_C = \frac{4 \times 69/0.765 + 110}{0.99^4} = \$490 .
$$

The startup's 30% therefore rests on its launch defect density (or on smaller interface overhead or cheaper packaging). Ask which, and for the foundry's $D_0$ data at its tape-out date.

(b) The heat sink may take $95 - 35 - 1500 \times 0.015$ = 60 − **22.5** = **37.5** K, so it needs $37.5/1500$ = **0.0250** K/W, **2.51** times better than the 0.0627 K/W sink. That is outside what a practical air heat sink delivers at 1.5 kW. Ask for the cooling solution's measured resistance, or plan for liquid cooling.

(c) When a fix is needed, the ECO path costs $3 + 12 \times 4$ = **51** \$M for certain, plus a 0.3 chance of the respin's $30 + 24 \times 4$ = **126** \$M. So the expected cost is $51 + 0.3 \times 126$ = **\$88.8 M** and the expected delay $12 + 0.3 \times 24$ = **19.2** weeks. Weighted by the 0.95 chance of needing a fix, the plan omits **\$84.4 M** and **18.2** weeks of expected schedule. Delay, not masks, is most of it, and the plan needs the funding runway to survive it.

(d) With $\hat p = 1$ the Wilson numerator is $1 + z^2/(2n) - z\sqrt{z^2/(4n^2)} = 1$, so the lower end is $1/(1 + z^2/n) = n/(n + z^2) = 4/(4 + 3.8416)$ = **51.0**%. Even that lower end is **10.2** times the survey's 5%, so the record is evidence of a strong team. But four chips is a small sample, and earlier chips may have been smaller, on mature nodes or without chiplets. Questions:

1. *"What is your plan if first silicon has a bug that needs a hardware fix?"* Strong: spare cells and a metal-only ECO path, chicken bits and patch RAM, and a budget and runway for a respin. Evasive: "our verification is thorough."
2. *"What were your last four chips: node, size, packaging, and what did first silicon need before production?"* Strong: specifics, including steppings, ECOs and workarounds that "first time" glossed over. Evasive: "they all worked; this team has never missed."

---

## Rubric for Question 12

| Part | Points | Award for |
|---|---|---|
| (a) | 2 + 1 | 2: saving at $D_0$ = 0.1 and the $D_0$ for 30% with both cost lines. 1: naming what the claim depends on (launch defect density, interface overhead, package cost) and the evidence to ask for. |
| (b) | 2 + 1 | 2: required resistance and the ratio. 1: the conclusion (no practical air sink at this power; ask for measurements or plan liquid). |
| (c) | 2 + 1 | 2: conditional and unconditional expected cost and delay. 1: the implication (schedule dominates; the plan needs runway for a likely fix). |
| (d) | 1 + 1 + 1 | 1: the bound and the comparison with the survey. 1 for each question with a strong and an evasive answer. |

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| X25.1a | time for 0.10 µm | 2.26 | h |
| X25.1a0 | B/A | 0.0709 | µm/h |
| X25.1a1 | time for 0.50 µm | 28.4 | h |
| X25.1a2 | time ratio | 12.5 | |
| X25.1b | sacrificial oxide | 114 | nm |
| X25.1b0 | sacrificial oxide | 0.1136 | µm |
| X25.1b1 | time for it | 2.71 | h |
| X25.1c | cycle time | 75.0 | days |
| X25.1c1 | inventory freed | 4.00e4 | wafers |
| X25.1d | wire delay | 3.64e3 | ps |
| X25.1d1 | half-length delay | 909 | ps |
| X25.2a | min pitch, ArF immersion | 71.5 | nm |
| X25.2a1 | min pitch, EUV | 20.5 | nm |
| X25.2a2 | min pitch, High-NA | 12.3 | nm |
| X25.2b | DOF, EUV | 124 | nm |
| X25.2b1 | DOF, High-NA | 44.6 | nm |
| X25.2b2 | DOF fraction kept | 0.360 | |
| X25.2c | photon energy | 1.47e-17 | J |
| X25.2c0 | energy delivered | 1.20e-13 | J |
| X25.2c1 | photons | 8.16e3 | |
| X25.2c2 | shot noise | 1.11 | % |
| X25.2d | throughput | 164 | wph |
| X25.2d1 | throughput, double dose | 106 | wph |
| X25.3a | peak concentration | 1.99e20 | cm⁻³ |
| X25.3a0 | peak over background | 1995 | |
| X25.3a1 | junction beyond peak | 78.0 | nm |
| X25.3a2 | projected range needed | 72.0 | nm |
| X25.3b | new straggle | 28.3 | nm |
| X25.3b1 | new peak | 1.41e20 | cm⁻³ |
| X25.3b0 | new straggle, unrounded | 28.28 | nm |
| X25.3b2 | new peak over background | 1410 | |
| X25.3c0 | junction beyond peak after anneal | 107.7 | nm |
| X25.3c | junction after anneal | 180 | nm |
| X25.3c1 | junction moved | 29.8 | nm |
| X25.3d | effective rate constant | 0.833 | cm/s |
| X25.3d1 | plating current density | 22.7 | mA/cm² |
| X25.4a0 | dies per wafer, unrounded | 416.8 | |
| X25.4a | dies per wafer | 417 | |
| X25.4b0 | AD0 | 0.225 | |
| X25.4b | Poisson yield | 0.799 | |
| X25.4b3 | Poisson yield, unrounded | 0.7985 | |
| X25.4b1 | Murphy yield | 0.802 | |
| X25.4b2 | negative-binomial yield | 0.808 | |
| X25.4c | cost, Poisson | 54.1 | $ |
| X25.4d | cost, negative binomial | 53.4 | $ |
| X25.5a | slow corner | 1.13 | |
| X25.5a0 | typical delay function | 2.118 | |
| X25.5a1 | f(0.80) | 2.195 | |
| X25.5a2 | f(0.85) | 2.040 | |
| X25.5a3 | restoring supply | 0.824 | V |
| X25.5a4 | supply increase | 74 | mV |
| X25.5b0 | series capacitance needed | 0.2925 | ε0/nm |
| X25.5b1 | 1/C_BOX | 2.906 | nm/ε0 |
| X25.5b | BOX thickness | 11.3 | nm |
| X25.5b2 | back-gate voltage | 0.533 | V |
| X25.5c0 | ln(pw/q) | 5.30 | |
| X25.5c1 | use-equivalent, beta 0.5 | 5.61e3 | h |
| X25.5c | burn-in, beta 0.5 | 140 | h |
| X25.5c3 | use-equivalent, beta 1 | 1.06e3 | h |
| X25.5c2 | burn-in, beta 1 | 26.5 | h |
| X25.5c4 | ratio | 5.30 | |
| X25.6a | crossover die size | 1.08 | mm |
| X25.6b | traces between pads | 2 | |
| X25.6b1 | layers | 6 | |
| X25.6c | shear strain | 0.241 | |
| X25.6c0 | reference strain | 0.191 | |
| X25.6c1 | life ratio | 0.630 | |
| X25.6d | package scale | 0.289 | |
| X25.7a | bond density | 4.0e4 | /mm² |
| X25.7a1 | overlay budget | 1.25 | µm |
| X25.7b | die bond yield | 99.93 | % |
| X25.7c | escape rate | 0.352 | % |
| X25.7c1 | package yield | 0.959 | |
| X25.7d3 | monolithic yield | 0.487 | |
| X25.7d | monolithic cost | 430 | $ |
| X25.7d4 | chiplet yield | 0.768 | |
| X25.7d1 | chiplet cost | 371 | $ |
| X25.7d2 | ratio | 0.861 | |
| X25.8a | TIM resistance | 0.0125 | K/W |
| X25.8a1 | TIM drop | 12.5 | K |
| X25.8b | hotspot centre rise | 15.9 | K |
| X25.8b1 | spreading resistance | 4.50 | K/W |
| X25.8c0 | fin parameter m | 27.4 | 1/m |
| X25.8c | mL | 0.822 | |
| X25.8c1 | fin efficiency | 0.823 | |
| X25.8d | coolant rise | 11.5 | K |
| X25.8d0 | mean coolant above inlet | 5.74 | K |
| X25.8d1 | junction temperature | 81.7 | °C |
| X25.9a | thermal AF | 2.73e3 | |
| X25.9a1 | total AF | 2.18e4 | |
| X25.9b | gamma | 4.61 | cm/MV |
| X25.9b1 | E-model life at 6 MV/cm | 3.00e9 | s |
| X25.9b2 | power-law exponent | 44.89 | |
| X25.9b3 | power-law life at 6 MV/cm | 2.73e11 | s |
| X25.9b4 | ratio of lives | 91 | |
| X25.9c | FIT, no failures | 9.16 | FIT |
| X25.9c1 | FIT, one failure | 20.2 | FIT |
| X25.10a0 | field cycles | 1.64e4 | |
| X25.10a | AF, n = 2 | 16.81 | |
| X25.10a4 | field cycles, unrounded | 16436 | |
| X25.10a1 | test cycles, n = 2 | 978 | |
| X25.10a2 | AF, n = 2.5 | 34.0 | |
| X25.10a3 | test cycles, n = 2.5 | 483 | |
| X25.10b2 | total rate | 165 | FIT |
| X25.10b3 | residual rate | 2.0 | FIT |
| X25.10b4 | latent rate | 3.0 | FIT |
| X25.10b5 | LFM denominator | 163 | FIT |
| X25.10b | SPFM | 98.8 | % |
| X25.10b1 | LFM | 98.2 | % |
| X25.10c | coverage needed for ASIL D SPFM | 98.35 | % |
| X25.10d | vehicles affected | 0.598 | % |
| X25.11a | time offset | 0.406 | h |
| X25.11a0 | equivalent time from bare silicon | 11.92 | h |
| X25.11a1 | time to 0.30 µm | 11.5 | h |
| X25.11b0 | other joints' sum | 142.6 | |
| X25.11b1 | summed eta^-beta | 542.6 | |
| X25.11b | package scale | 0.247 | |
| X25.11b2 | corner fraction | 73.7 | % |
| X25.11c | dual-point rate | 3.00e-4 | FIT |
| X25.11c1 | interval for 0.01 FIT | 6.67e4 | h |
| X25.11d | yield, alpha 1 | 0.625 | |
| X25.11d1 | yield, alpha 3 | 0.579 | |
| X25.11d2 | yield, Poisson | 0.549 | |
| X25.12a11 | monolithic yield at 0.1 | 0.449 | |
| X25.12a12 | chiplet yield at 0.1 | 0.803 | |
| X25.12a1 | monolithic cost at 0.1 | 597 | $ |
| X25.12a2 | chiplet cost at 0.1 | 473 | $ |
| X25.12a | model saving | 20.8 | % |
| X25.12a3 | D0 for 30% | 0.122 | cm⁻² |
| X25.12a4 | D0 above model | 21.6 | % |
| X25.12a5 | AD0 monolithic | 0.973 | |
| X25.12a6 | AD0 chiplet | 0.268 | |
| X25.12a7 | monolithic yield | 0.378 | |
| X25.12a8 | chiplet yield | 0.765 | |
| X25.12a9 | monolithic cost | 700 | $ |
| X25.12a10 | chiplet cost | 490 | $ |
| X25.12b0 | junction-to-base drop | 22.5 | K |
| X25.12b2 | drop available to the sink | 37.5 | K |
| X25.12b | sink resistance needed | 0.0250 | K/W |
| X25.12b1 | improvement needed | 2.51 | |
| X25.12c0 | respin path cost | 126 | $M |
| X25.12c4 | ECO path fixed cost | 51 | $M |
| X25.12c | expected cost of a fix | 88.8 | $M |
| X25.12c1 | expected delay of a fix | 19.2 | weeks |
| X25.12c2 | omitted cost | 84.4 | $M |
| X25.12c3 | omitted delay | 18.2 | weeks |
| X25.12d | Wilson lower bound | 51.0 | % |
| X25.12d1 | ratio to survey | 10.2 | |
