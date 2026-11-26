# Course 25 · Final Exam Solutions

Exam: [README.md](README.md). Every number below is recomputed by [verify_25_exam.py](../verify/verify_25_exam.py). About a third of the values are recomputed by a second route; the rest are closed-form re-evaluations of the same formulas:

- Question 1(a): oxide growth by integrating the Deal–Grove rate equation numerically;
- Question 3(b): the junction depth by root-finding on the Gaussian profile;
- Question 4(b): the clustered yields by integrating Poisson yield over a gamma-distributed defect density;
- Question 7(b): the bond yield from the normal CDF; 7(c): escapes from the joint probability table;
- Question 8(c): fin efficiency by solving the fin ODE as a boundary-value problem;
- Question 9(b): the E-model and power-law fits by least squares in transformed coordinates;
- Question 11(b): the package scale by integrating the product of joint survival functions.

---

## Solutions

### Solution 1

(a) From bare silicon, $t = x^2/B + x/(B/A)$: for 0.10 µm, $0.01/0.0117 + 0.10/0.0709$ = **2.26** h; for 0.50 µm, $0.25/0.0117 + 0.50/0.0709$ = **28.4** h. Five times the thickness takes over twelve times as long, because the parabolic (diffusion) term takes over.

(b) Silicon consumed is 0.44 of the oxide thickness: **0.044** µm.

(c) WIP = λT = (60,000/30 per day) × 90 days = **1.80e5** wafers.

(d) $t_{50} = 0.379RC = 0.379 \times 24\ \text{k}\Omega \times 0.4\ \text{pF}$ = **3.64e3** ps (3.64 ns). Halving the length halves both $R$ and $C$: **910** ps, a quarter.

### Solution 2

(a) $p_{min} = \lambda/(2\,\text{NA})$: **71.5** nm (193 nm immersion), **20.5** nm (EUV) and **12.3** nm (High-NA).

(b) $13.5/(2 \times 0.33^2)$ = **62.0** nm and $13.5/(2 \times 0.55^2)$ = **22.3** nm: High-NA gains resolution but loses almost two-thirds of the focus budget.

(c) Photon energy $hc/\lambda$ = 1.47 × 10⁻¹⁷ J; energy delivered $300\ \text{J/m}^2 \times (20 \times 10^{-9})^2$ = 1.2 × 10⁻¹³ J, so **8.16e3** photons, and $1/\sqrt{N}$ = **1.11**% shot noise.

(d) $3600/(10 + 12)$ = **164** wafers per hour; with 24 s of exposure, **106** wph.

### Solution 3

(a) $N_p = Q/(\sqrt{2\pi}\,\Delta R_p) = 10^{15}/(2.507 \times 2 \times 10^{-6})$ = **1.99e20** cm⁻³.

(b) $x_j = R_p + \Delta R_p\sqrt{2\ln(N_p/N_B)} = 50 + 20\sqrt{2\ln 1995}$ = **128** nm.

(c) $\Delta R_p' = \sqrt{(2 \times 10^{-6})^2 + 2 \times 2 \times 10^{-12}}$ cm = **28.3** nm; the peak falls in proportion to **1.41e20** cm⁻³, since the dose is conserved.

(d) $k_{eff} = k_sh_g/(k_s + h_g) = 5/6$ = **0.833** cm/s: closer to $k_s$, so the surface reaction limits the process (it is reaction-limited, and temperature-sensitive). Plating: $jM/(nF\rho) = 0.020 \times 63.55/(2 \times 96{,}485 \times 8.96)$ cm/s = **0.441** µm/min.

### Solution 4

(a) $\pi \times 300^2/600 - \pi \times 300/\sqrt{300}$ = 416.8, so **417** dies.

(b) $AD_0 = 1.5 \times 0.15 = 0.225$: Poisson $e^{-0.225}$ = **0.799**; Murphy $[(1 - e^{-0.225})/0.225]^2$ = **0.802**; negative binomial $(1 + 0.225/2)^{-2}$ = **0.808**.

(c) $18{,}000/(417 \times 0.799)$ = **$54.1**.

(d) $18{,}000/(417 \times 0.808)$ = **$53.4**. Clustering concentrates defects on fewer dies, raising yield for the same average density; the difference is small for a modest die and grows with area.

### Solution 5

(a) Delay ∝ $V/(V - V_{TH})^{1.3}$: slow $(0.45/0.41)^{1.3}$ = **1.13**, fast $(0.45/0.49)^{1.3}$ = **0.895**, spread **1.26**.

(b) In units of ε₀/nm: $C_{ox}$ = 3.9, $C_{Si}$ = 11.7/6 = 1.95, $C_{BOX}$ = 3.9/20 = 0.195. Coupling $C_{Si}C_{BOX}/[C_{ox}(C_{Si} + C_{BOX})]$ = **45.5** mV/V.

(c) The minimum applies: $4 \times 15{,}000$ = **€60,000**.

(d) Analog circuits, I/O and passives shrink little or not at all (their size is set by matching, noise, voltage and inductors), so a shrink cuts mainly the digital area while wafer cost rises.

### Solution 6

(a) $D = 4p_a^2/p_w = 4 \times 0.11^2/0.045$ = **1.08** mm.

(b) $n = \lfloor(130 - 75 - 10)/20\rfloor$ = **2** traces, so 3 rows per layer and $\lceil 18/3\rceil$ = **6** layers.

(c) $\gamma = 13.4 \times 10^{-6} \times 120 \times 12/0.08$ = **0.241**. The reference joint has $\gamma_0 = 13.4 \times 10^{-6} \times 100 \times 10/0.07 = 0.191$, so life scales by $(0.191/0.241)^2$ = **0.630**.

(d) $500^{-1/5}$ = **0.289**.

### Solution 7

(a) $(1000/5)^2$ = **4.0e4** per mm²; budget **1.25** µm.

(b) $[\operatorname{erf}(1.25/(0.35\sqrt 2))]^2 = 0.99964^2$ = **99.93**%.

(c) $e = 0.15 \times 0.02/(0.85 + 0.003)$ = **0.352**%; $Y_{pkg} = 0.998^7(1 - 0.00352)(0.996)^6$ = **0.959**.

(d) Monolithic: $Y = e^{-0.72}$, $[(180 + 3)/0.487 + 50]/0.99$ = **$430**. Chiplets: $Y = e^{-0.264}$, $[3(66 + 3)/0.768 + 90]/0.99^3$ = **$371**. Ratio **0.861**.

### Solution 8

(a) $30 \times 10^{-6}/(4 \times 600 \times 10^{-6})$ = **0.0125** K/W; **12.5** K at 1,000 W.

(b) $q = 3/(\pi \times 0.4^2)$ W/mm²; centre rise $qa/k$ = **15.9** K; $R_{sp} = 8/(3\pi^2 \times 150 \times 0.4 \times 10^{-3})$ = **4.50** K/W.

(c) $m = \sqrt{2 \times 60/(200 \times 0.0008)}$ = 27.4 m⁻¹; $mL$ = **0.822**; $\eta_f = \tanh 0.822/0.822$ = **0.823**.

(d) $\Delta T = 1200/(1000 \times 4180 \times 2.5 \times 10^{-5})$ = **11.5** K; $T_J = 40 + 5.74 + 1200 \times 0.030$ = **81.7** °C.

### Solution 9

(a) $AF_T = \exp[(0.85/k)(1/383.15 - 1/553.15)]$ = **2.73e3**; with $4^{1.5}$ = 8, total **2.18e4**.

(b) E model: $\gamma = \ln 10/0.5$ = **4.61** (MV/cm)⁻¹; $t(6) = 30\,e^{4.61 \times 4}$ = **3.0e9** s. Power law: $m = \ln 10/\ln(10/9.5)$ = **44.9**; $t(6) = 30 \times (10/6)^{44.9}$ = **2.73e11** s.

(c) $1.833 \times 10^9/(2 \times 2000 \times 1000 \times 50)$ = **9.16** FIT; with one failure, $4.045/1.833$ times that: **20.2** FIT.

(d) The two models have different shapes in field and agree only at the stress points; extrapolating four MV/cm below them magnifies the difference by about two orders of magnitude here. The E model predicts the shorter life and is the conservative one (25-09).

### Solution 10

(a) The range is 150 − (−55) = 205 K, so $AF = (205/40)^2$ = **26.3**; 1,000 test cycles equal $1000\,AF$ field cycles, or $1000\,AF/(2 \times 365.25)$ = **36.0** years.

(b) Total 165 FIT; residual $0.02 \times 100 = 2$ FIT; latent $0.2 \times 15 = 3$ FIT. SPFM $= 1 - 2/165$ = **98.8**%; LFM $= 1 - 3/163$ = **98.2**%.

(c) SPFM meets ASIL C (≥ 97%) but not D (≥ 99%); LFM meets D (≥ 90%). The element supports **ASIL C** metrics; for D the diagnostic coverage must rise above 98.35% (or the dangerous rate fall).

(d) $1 - (1 - 0.5 \times 10^{-6})^{12{,}000}$ = **0.598**%.

### Solution 11

(a) In steady state the fluxes through the gas boundary layer, the oxide and the interface are equal; eliminating the interface concentrations gives $dx/dt = (k_sC^*/N_1)/(1 + k_s/h + k_sx/D)$, which integrates to $x^2 + Ax = B(t + \tau)$ (25-01). For $x \ll A$ the linear term dominates: $x \approx (B/A)(t + \tau)$, limited by the interface reaction. For $x \gg A$, $x^2 \approx Bt$, limited by diffusion through the oxide. The two terms are equal at $x$ = $A$ = **0.165** µm, reached at $t = (A^2 + A^2)/B$ = **4.65** h.

(b) Each joint survives to $N$ with probability $e^{-(N/\eta_i)^\beta}$; independence multiplies them: $R(N) = \exp(-N^\beta\sum\eta_i^{-\beta})$, a Weibull of the same shape with $\eta_{pkg} = (\sum\eta_i^{-\beta})^{-1/\beta}$. Here $(100 \times 1 + 10{,}000 \times 4^{-4})^{-1/4} = 139.1^{-1/4}$ = **0.291**: the 10,000 lower-strain joints still add 39% to the hazard.

(c) A latent fault arrives at rate $\lambda_L$ and stays hidden for τ; a dangerous fault during that time, probability $\lambda_D\tau$ for small values, violates the goal. The rate of such pairs is $\lambda_L\lambda_D\tau$, with τ = half the test interval = 1,000 h: $3 \times 10^{-9} \times 10^{-7} \times 1000$ /h = **3.0e-4** FIT.

(d) $n = -d\ln MTTF/d\ln j = (2Bj^{-2} + Cj^{-1})/(Bj^{-2} + Cj^{-1}) = (2 + x)/(1 + x)$ with $x = j/j^*$, $j^* = B/C$. Setting $n$ = 1.6: $2 + x = 1.6 + 1.6x$, $x$ = **0.667**.

### Solution 12

(a) The model gives a saving of **20.8**% (Example 25-07.9), not 30%. To reach 30% the startup must assume a higher defect density, smaller interface overhead or cheaper packaging; ask which.

(b) $(95 - 35 - 1500 \times 0.020)/1500$ = **0.020** K/W, **3.1** times better than the 0.0627 K/W sink. Air cooling at 1.5 kW is outside what a practical air heat sink delivers; ask for the cooling solution's measured resistance, or plan for liquid.

(c) $0.02 \times 20{,}000/500$ = **0.8** h; 5% buys **2.0** h and 7% **2.8** h. Leading AI parts reportedly spend 5–7% of selling price on test [R-618]; 2% implies either much less burn-in and system-level test or an optimistic plan.

(d) Upper bound **7.97**% (about 8%). Questions (rubric: 3 points for two well-posed questions with a strong and an evasive answer each):

1. *"What is your plan if first silicon has a bug that needs a hardware fix?"* Strong: spare cells and a metal-only ECO path, chicken bits and patch RAM, and a budget for a respin. Evasive: "our verification is thorough."
2. *"How long from first silicon to boot and to production on your team's previous chips?"* Strong: dates, steppings and causes. Evasive: "this team has never missed."

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| X25.1a | time for 0.10 µm | 2.26 | h |
| X25.1a1 | time for 0.50 µm | 28.4 | h |
| X25.1b | silicon consumed | 0.044 | µm |
| X25.1c | WIP | 1.80e5 | wafers |
| X25.1d | wire delay | 3.64e3 | ps |
| X25.1d1 | half-length delay | 910 | ps |
| X25.2a | min pitch, ArF immersion | 71.5 | nm |
| X25.2a1 | min pitch, EUV | 20.5 | nm |
| X25.2a2 | min pitch, High-NA | 12.3 | nm |
| X25.2b | DOF, EUV | 62.0 | nm |
| X25.2b1 | DOF, High-NA | 22.3 | nm |
| X25.2c | photons | 8.16e3 | |
| X25.2c1 | shot noise | 1.11 | % |
| X25.2d | throughput | 164 | wph |
| X25.2d1 | throughput, double dose | 106 | wph |
| X25.3a | peak concentration | 1.99e20 | cm⁻³ |
| X25.3b | junction depth | 128 | nm |
| X25.3c | new straggle | 28.3 | nm |
| X25.3c1 | new peak | 1.41e20 | cm⁻³ |
| X25.3d | effective rate constant | 0.833 | cm/s |
| X25.3d1 | plating rate | 0.441 | µm/min |
| X25.4a | dies per wafer | 417 | |
| X25.4b | Poisson yield | 0.799 | |
| X25.4b1 | Murphy yield | 0.802 | |
| X25.4b2 | negative-binomial yield | 0.808 | |
| X25.4c | cost, Poisson | 54.1 | $ |
| X25.4d | cost, negative binomial | 53.4 | $ |
| X25.5a | slow corner | 1.13 | |
| X25.5a1 | fast corner | 0.895 | |
| X25.5a2 | spread | 1.26 | |
| X25.5b | back-gate coupling | 45.5 | mV/V |
| X25.5c | MPW cost | 60000 | € |
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
| X25.7d | monolithic cost | 430 | $ |
| X25.7d1 | chiplet cost | 371 | $ |
| X25.7d2 | ratio | 0.861 | |
| X25.8a | TIM resistance | 0.0125 | K/W |
| X25.8a1 | TIM drop | 12.5 | K |
| X25.8b | hotspot centre rise | 15.9 | K |
| X25.8b1 | spreading resistance | 4.50 | K/W |
| X25.8c | mL | 0.822 | |
| X25.8c1 | fin efficiency | 0.823 | |
| X25.8d | coolant rise | 11.5 | K |
| X25.8d1 | junction temperature | 81.7 | °C |
| X25.9a | thermal AF | 2.73e3 | |
| X25.9a1 | total AF | 2.18e4 | |
| X25.9b | gamma | 4.61 | cm/MV |
| X25.9b1 | E-model life at 6 MV/cm | 3.0e9 | s |
| X25.9b2 | power-law exponent | 44.9 | |
| X25.9b3 | power-law life at 6 MV/cm | 2.73e11 | s |
| X25.9c | FIT, no failures | 9.16 | FIT |
| X25.9c1 | FIT, one failure | 20.2 | FIT |
| X25.10a | TC acceleration | 26.3 | |
| X25.10a1 | field years | 36.0 | years |
| X25.10b | SPFM | 98.8 | % |
| X25.10b1 | LFM | 98.2 | % |
| X25.10c | coverage needed for ASIL D SPFM | 98.35 | % |
| X25.10d | vehicles affected | 0.598 | % |
| X25.11a | equal-term thickness | 0.165 | µm |
| X25.11a1 | time to reach it | 4.65 | h |
| X25.11b | package scale | 0.291 | |
| X25.11b1 | hazard added by other joints | 39 | % |
| X25.11c | dual-point rate | 3.0e-4 | FIT |
| X25.11d | x for n = 1.6 | 0.667 | |
| X25.12a | model saving | 20.8 | % |
| X25.12b | sink resistance needed | 0.020 | K/W |
| X25.12b1 | improvement needed | 3.1 | |
| X25.12c | hours at 2% | 0.8 | h |
| X25.12c1 | hours at 5% | 2.0 | h |
| X25.12c2 | hours at 7% | 2.8 | h |
| X25.12d | Wilson upper bound | 7.97 | % |
