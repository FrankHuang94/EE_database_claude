# Equation Sheet · 19 Digital VLSI Design

The relations to know cold from Course 19, each with its conditions and the chapter that derives it.

Conventions:

- $V_{TH}$ is a threshold ($V_{TN}$, $\lvert V_{TP}\rvert$) and $V_T = kT/q$ = 25.85 mV at 300 K is the thermal voltage (some chapters still write $V_T$ for the threshold; read it from context);
- square-law devices: $k = \mu C_{ox}W/L$, $r = k_n/k_p$; λ is channel-length modulation in 19-01 and the design-rule unit in 19-09;
- lumped RC delay $\ln 2\,RC \approx 0.69\,RC$; a distributed line's 50% delay 0.38 $RC$; "Elmore constant" is the unscaled $\sum R C$;
- logical effort with $\mu = \mu_n/\mu_p = 2$, $p_{inv} = 1$ and $\tau = 0.69\,RC_{inv}$;
- skew $\delta = L_2 - L_1$ (capture minus launch); negative slack fails;
- other symbols are reused between chapters, so read each row with its chapter: α is the activity factor in power rows and the alpha-power exponent in delay rows; τ is the logical-effort unit, a latch's regeneration time constant, or a ramp time; ρ is resistivity, the best stage effort or a correlation; $S$ is a size factor, the subthreshold slope or a scaling factor; utilization is $u$, while $U$ is clock uncertainty; $T$ is fault coverage in the test rows and a period elsewhere; μ is the mobility ratio in sizing rows and a margin's mean in yield rows.

## The inverter: statics

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $V_M = \dfrac{V_{TN}\sqrt r + V_{DD} - \lvert V_{TP}\rvert}{1 + \sqrt r}$ | Square law, λ = 0, both saturated; alpha-power: replace $\sqrt r$ by $r^{1/\alpha}$ | [19-01](../../courses/19-digital-vlsi-design/chapters/19-01-cmos-inverter-static.md) |
| $r = \left(\dfrac{V_{DD} - \lvert V_{TP}\rvert - V_M}{V_M - V_{TN}}\right)^2$, $\dfrac{W_p}{W_n} = \dfrac{\mu_n}{\mu_p}\cdot\dfrac1r$ | Equal L; symmetric: $W_p/W_n = \mu_n/\mu_p$ | [19-01](../../courses/19-digital-vlsi-design/chapters/19-01-cmos-inverter-static.md) |
| Symmetric: $V_{IL} = \dfrac{3V_{DD} + 2V_{TH}}{8}$, $V_{IH} = \dfrac{5V_{DD} - 2V_{TH}}{8}$, $NM_L = NM_H = \dfrac{3V_{DD} + 2V_{TH}}{8}$ | Unity-gain points; $NM_L = V_{IL} - V_{OL}$, $NM_H = V_{OH} - V_{IH}$ | [19-01](../../courses/19-digital-vlsi-design/chapters/19-01-cmos-inverter-static.md) |
| $A_v = -\dfrac{g_{mn} + g_{mp}}{g_{dsn} + g_{dsp}}$; symmetric $\lvert A_v\rvert = \dfrac{2(1 + \lambda V_{DD}/2)}{\lambda V_{ov}} \approx \dfrac{2}{\lambda V_{ov}}$ | At $V_M$; transition width ≈ $V_{DD}/\lvert A_v\rvert$ | [19-01](../../courses/19-digital-vlsi-design/chapters/19-01-cmos-inverter-static.md) |
| $\partial V_M/\partial V_{TN} = \sqrt r/(1 + \sqrt r)$; $\sigma_{V_M} = \sigma_{VT}\sqrt{r + 1}/(1 + \sqrt r)$ | Independent thresholds; $\sigma_{VT}/\sqrt2$ at $r = 1$ | [19-01](../../courses/19-digital-vlsi-design/chapters/19-01-cmos-inverter-static.md) |
| Subthreshold: $\lvert A_v\rvert = (e^{V_{DD}/(2V_T)} - 1)/n$; $V_{DD,min} = 2V_T\ln(1 + n)$ | 36–50 mV; practical designs need a few hundred mV | [19-01](../../courses/19-digital-vlsi-design/chapters/19-01-cmos-inverter-static.md) |

## The inverter: dynamics

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $C_L = C_{int} + C_{ext}$, $C_{int} = C_{dn} + C_{dp} + 2(C_{gdn} + C_{gdp})$, $C_{ext} = \sum C_g + C_w$ | Miller doubles $C_{gd}$; $\gamma = C_{int}/C_g$ | [19-02](../../courses/19-digital-vlsi-design/chapters/19-02-cmos-inverter-dynamic.md) |
| $t_{pHL} = \dfrac{C_L}{k_nV_{ov}}\left[\dfrac{2V_{TN}}{V_{ov}} + \ln\left(\dfrac{4V_{ov}}{V_{DD}} - 1\right)\right]$ | Step input, square law, $V_{TN} < V_{DD}/2$ | [19-02](../../courses/19-digital-vlsi-design/chapters/19-02-cmos-inverter-dynamic.md) |
| $t_p = \ln 2\,R_{eq}C_L$, $R_{eq} \approx 3V_{DD}/(4I_{sat})$; $t_p = (t_{pHL} + t_{pLH})/2$ | $R_{eq} \propto 1/W$ | [19-02](../../courses/19-digital-vlsi-design/chapters/19-02-cmos-inverter-dynamic.md) |
| $t_p = t_{p0}(1 + C_{ext}/(SC_{int,ref}))$, $t_{p0} = 0.69R_{ref}C_{int,ref}$; FO4 $= t_{p0}(1 + 4/\gamma)$ | Intrinsic delay is size independent; γ is logical effort's $p_{inv}$, so the course's $p_{inv} = 1$ gives FO4 = 5τ, while γ ≈ 0.5 (19-02's reading of Ho et al.) gives $9t_{p0} = 4.5\tau$ | [19-02](../../courses/19-digital-vlsi-design/chapters/19-02-cmos-inverter-dynamic.md) |
| Ring oscillator $f = 1/(2Nt_p)$ | Stage delay includes ramp-input slowdown | [19-02](../../courses/19-digital-vlsi-design/chapters/19-02-cmos-inverter-dynamic.md) |
| $t_p \propto V_{DD}/(V_{DD} - V_{TH})^\alpha$; EDP-optimal $V_{DD} = 3V_{TH}/(3 - \alpha)$ | Alpha-power law | [19-02](../../courses/19-digital-vlsi-design/chapters/19-02-cmos-inverter-dynamic.md) |

## Logic families

| Relation | Conditions / notes | Chapter |
|---|---|---|
| NAND-$N$ input capacitance $(N + \mu)/(1 + \mu)$, NOR-$N$ $(1 + N\mu)/(1 + \mu)$ of the inverter's | Sized for unit drive | [19-03](../../courses/19-digital-vlsi-design/chapters/19-03-logic-families.md) |
| Elmore constant $\tau_E = \sum_m C_mR_{km}$; $t_p \approx 0.69\,\tau_E$ | $R_{km}$ resistance shared by the paths to $k$ and $m$ | [19-03](../../courses/19-digital-vlsi-design/chapters/19-03-logic-families.md) |
| NAND-$N$ pull-down: $\tau_E = Rc\,\dfrac{N(N-1)}{2} + R[(1 + \mu)cN + C_{ext}]$ | Internal nodes charged; quadratic in fan-in | [19-03](../../courses/19-digital-vlsi-design/chapters/19-03-logic-families.md) |
| Pseudo-NMOS $V_{OL} = a - \sqrt{a^2 - 2I_{load}/k_n}$, $a = V_{DD} - V_{TN}$, $I_{load} = \tfrac12k_p(V_{DD} - \lvert V_{TP}\rvert)^2$ | Static power $V_{DD}I_{load}$ while low | [19-03](../../courses/19-digital-vlsi-design/chapters/19-03-logic-families.md) |
| Pass NMOS: $V_{out} = V_{DD} - V_{TN}(V_{out})$, $V_{TN} = V_{TN0} + \gamma_B(\sqrt{2\phi_B + V_{SB}} - \sqrt{2\phi_B})$ | Solve implicitly | [19-03](../../courses/19-digital-vlsi-design/chapters/19-03-logic-families.md) |
| TG chain $\tau_E = RC\,n(n+1)/2$; buffer every $m_{opt} \approx 1.7\sqrt{t_{buf}/RC}$ | $n$ gates of $R$, $C$ | [19-03](../../courses/19-digital-vlsi-design/chapters/19-03-logic-families.md) |
| Charge sharing: boundary $C_a/C_L = V_{TN}/(V_{DD} - V_{TN})$; below it $\Delta V = (C_a/C_L)(V_{DD} - V_{TN})$, above it $V = V_{DD}C_L/(C_L + C_a)$; hold time $C_L\Delta V/I_{leak}$ | No body effect | [19-03](../../courses/19-digital-vlsi-design/chapters/19-03-logic-families.md) |

## Sizing and logical effort

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $d = gh + p$ (units of τ); $g$: INV 1, NAND-$n$ $(n + 2)/3$, NOR-$n$ $(2n + 1)/3$; $p = np_{inv}$ | $\mu = 2$; $h = C_{out}/C_{in}$ | [19-04](../../courses/19-digital-vlsi-design/chapters/19-04-sizing-and-logical-effort.md) |
| $G = \prod g_i$, $B = \prod b_i$, $H = C_{out}/C_{in}$, $F = GBH$, $P = \sum p_i$ | $b = (C_{on} + C_{off})/C_{on}$ | [19-04](../../courses/19-digital-vlsi-design/chapters/19-04-sizing-and-logical-effort.md) |
| $\hat f = F^{1/N}$, $\hat D = NF^{1/N} + P$; size backward $C_{in,i} = g_iC_{out,i}/\hat f$ | Equal stage efforts are optimal | [19-04](../../courses/19-digital-vlsi-design/chapters/19-04-sizing-and-logical-effort.md) |
| $\rho(\ln\rho - 1) = p_{inv}$ (ρ = 3.59 at $p_{inv}$ = 1), $\hat N = \log_\rho F \approx \log_4 F$ | Flat within about 9% for stage efforts 2.4–6 | [19-04](../../courses/19-digital-vlsi-design/chapters/19-04-sizing-and-logical-effort.md) |

## Interconnect

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $R = \rho L/(Wt) = R_\square L/W$ | Narrow copper well above bulk resistivity | [19-05](../../courses/19-digital-vlsi-design/chapters/19-05-interconnect.md) |
| $rc\,\partial v/\partial t = \partial^2v/\partial x^2$; $t_{50} = 0.38\,RC$ (more exactly 0.379; a lumped RC gives 0.69 $RC$; the Elmore constant is $RC/2$, an upper bound) | Distributed RC line, step input | [19-05](../../courses/19-digital-vlsi-design/chapters/19-05-interconnect.md) |
| $t \approx 0.69R_d(C_w + C_L) + R_w(0.38C_w + 0.69C_L)$ | Driver, wire, load | [19-05](../../courses/19-digital-vlsi-design/chapters/19-05-interconnect.md) |
| $k_{opt} = \sqrt{\dfrac{0.38R_wC_w}{0.69R_0C_0}}$, $h_{opt} = \sqrt{\dfrac{R_0C_w}{R_wC_0}}$, $T_{min} = (2\sqrt{0.69 \times 0.38} + 2 \times 0.69)\sqrt{R_0C_0\,rc}\,L$ | 2.40 with 0.69 and 0.38, 2.41 with ln 2 and 0.379 (as 19-05 computes); repeated delay is linear in $L$ | [19-05](../../courses/19-digital-vlsi-design/chapters/19-05-interconnect.md) |
| Floating victim $\Delta V = \Delta V_{agg}C_c/(C_c + C_g)$; Miller coupling factor 0, 1, 2 | $C_g$ is all capacitance to quiet nodes, including non-switching neighbours; MCF for same, quiet, opposite switching | [19-05](../../courses/19-digital-vlsi-design/chapters/19-05-interconnect.md) |
| Scaling by $S$: $r \propto 1/S^2$, $c$ ≈ constant; repeated delay per length $\propto S^{-1/2}$ | Local RC roughly constant | [19-05](../../courses/19-digital-vlsi-design/chapters/19-05-interconnect.md) |

## Power

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $E = CV_{DD}^2$ per 0→1→0 cycle; $P_{dyn} = \alpha CV_{DD}^2f$ | α = 1 for clocks | [19-06](../../courses/19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md) |
| $P_{sc} = (\beta/12)(V_{DD} - 2V_{TH})^3\,\tau/T$ | Veendrick upper bound; zero for $V_{DD} < 2V_{TH}$ | [19-06](../../courses/19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md) |
| $I = I_0e^{(V_{GS} - V_{TH} + \eta V_{DS})/(nV_T)}(1 - e^{-V_{DS}/V_T})$; $S = nV_T\ln 10$; leakage ×$10^{\Delta V_{TH}/S}$ | Subthreshold; stack effect mostly DIBL | [19-06](../../courses/19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md) |
| Power-gating break-even $E_{wake}/P_{leak,saved}$ | Shorter idle periods lose energy | [19-06](../../courses/19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md) |
| Minimum energy: $L_de^{-x}(x - 2) = 2\alpha$, $x = V_{DD}/(nV_T)$; leakage share $2/x$ | Subthreshold logic | [19-06](../../courses/19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md) |

## Sequential timing

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $T_c \ge t_{pcq} + t_{pd} + t_{setup} - \delta + t_{jitter}$; $t_{ccq} + t_{cd} \ge t_{hold} + \delta$ | Hold is independent of $T_c$ | [19-07](../../courses/19-digital-vlsi-design/chapters/19-07-sequential-timing-and-clocking.md) |
| $T_c = t_L/N + t_o$, latency $t_L + Nt_o$ | $t_o = t_{pcq} + t_{setup}$ | [19-07](../../courses/19-digital-vlsi-design/chapters/19-07-sequential-timing-and-clocking.md) |
| Two-phase latches: $T_c \ge t_{L1} + t_{L2} + 2t_{pdq}$; borrow up to $T_c/2 - t_{setup}$ | 50% duty cycle | [19-07](../../courses/19-digital-vlsi-design/chapters/19-07-sequential-timing-and-clocking.md) |
| $\Delta v = \Delta v_0e^{t/\tau}$, $\tau = C/g_m$; $\text{MTBF} = e^{t_r/\tau}/(T_0f_{clk}f_{data})$ | Each extra synchronizer stage ×$e^{t/\tau}$, with $t$ the period less the flip-flop overhead | [19-07](../../courses/19-digital-vlsi-design/chapters/19-07-sequential-timing-and-clocking.md) |

## SRAM

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Read: $\tfrac12k_A(V_{DD} - \Delta V - V_{TH})^2 = k_N[(V_{DD} - V_{TH})\Delta V - \tfrac12\Delta V^2]$, need $\Delta V < V_{TN}$ | Cell ratio $k_N/k_A$ ≈ 1.5–2.5 | [19-08](../../courses/19-digital-vlsi-design/chapters/19-08-sram-design.md) |
| Write: the written node must fall below $V_{TN}$, which needs $k_P/k_A$ ≲ 0.67 for 19-08's cell; $k_P < k_A < k_N$ | Textbook W/L rules near 1–1.5 absorb the PMOS's lower mobility; both constraints bind | [19-08](../../courses/19-digital-vlsi-design/chapters/19-08-sram-design.md) |
| $t_{BL} = C_{BL}\Delta V/I_{cell}$; sense $\tau\ln(V_{DD}/\Delta V)$ | Sense at about 100 mV | [19-08](../../courses/19-digital-vlsi-design/chapters/19-08-sram-design.md) |
| Array yield $e^{-NQ(\mu/\sigma)}$; with $s$ spares, Poisson CDF up to $s$ | About 6σ cell margin |
| $Q(z) \approx \dfrac{e^{-z^2/2}}{z\sqrt{2\pi}}\left(1 - \dfrac{1}{z^2}\right)$; $Q(5) = 2.87 \times 10^{-7}$, $Q(5.5) = 1.90 \times 10^{-8}$, $Q(6) = 9.87 \times 10^{-10}$, $Q(6.5) = 4.02 \times 10^{-11}$, $Q(7) = 1.28 \times 10^{-12}$ | Standard normal upper tail; the asymptotic form is within 0.5% for $z \ge 5$ | [19-08](../../courses/19-digital-vlsi-design/chapters/19-08-sram-design.md) |

## Layout and standard cells

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Contacted pitch 8λ, uncontacted 5λ | The chapter's illustrative rules | [19-09](../../courses/19-digital-vlsi-design/chapters/19-09-layout-and-standard-cells.md) |
| One ordering must be an Euler path of both the pull-down and pull-up graphs | A connected graph has one iff 0 or 2 nodes have odd degree | [19-09](../../courses/19-digital-vlsi-design/chapters/19-09-layout-and-standard-cells.md) |
| $A_{core} = \sum A_{cells}/u$; routed gate density already includes utilization | $u$ ≈ 0.6–0.8 | [19-09](../../courses/19-digital-vlsi-design/chapters/19-09-layout-and-standard-cells.md) |
| Antenna ratio = metal area ÷ gate area ≤ limit | Fix with a jumper or a diode | [19-09](../../courses/19-digital-vlsi-design/chapters/19-09-layout-and-standard-cells.md) |

## Synthesis and static timing

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Tree covering: $\text{cost}(v) = \min_{\text{patterns } p \text{ at } v}\big[\text{cost}(p) + \sum_{\text{inputs } u \text{ of } p} \text{cost}(u)\big]$ | Dynamic programming over a tree, inputs first; area adds, delay takes the max over inputs | [19-10](../../courses/19-digital-vlsi-design/chapters/19-10-synthesis-and-sta.md) |
| Bilinear interpolation: $(1 - t_s)(1 - t_C)D_{00} + (1 - t_s)t_CD_{01} + t_s(1 - t_C)D_{10} + t_st_CD_{11}$ | $t_s, t_C$ fractional positions between table points in slew and load | [19-10](../../courses/19-digital-vlsi-design/chapters/19-10-synthesis-and-sta.md) |
| $AT(v) = \max_u[AT(u) + d_{uv}]$; $RT(u) = \min_v[RT(v) - d_{uv}]$; slack $= RT - AT$ | One topological pass each way | [19-10](../../courses/19-digital-vlsi-design/chapters/19-10-synthesis-and-sta.md) |
| Setup slack $= T_c + L_2 - t_{\text{setup}} - U - (L_1 + t_{pcq} + t_{pd})$ | $L_1, L_2$ launch and capture clock latencies, $U$ uncertainty | [19-10](../../courses/19-digital-vlsi-design/chapters/19-10-synthesis-and-sta.md) |
| Hold slack $= L_1 + t_{ccq} + t_{cd} - (L_2 + t_{\text{hold}} + U)$ | No clock period; negative means failing | [19-10](../../courses/19-digital-vlsi-design/chapters/19-10-synthesis-and-sta.md) |
| Derated setup slack $= [T_c + k_EL_2 - t_{\text{setup}} - U] - k_L[L_1 + t_{pcq} + t_{pd}]$; CRPR credit $= (k_L - k_E) \times$ common clock delay | OCV derates $k_L > 1 > k_E$ | [19-10](../../courses/19-digital-vlsi-design/chapters/19-10-synthesis-and-sta.md) |
| Path sigma $= \sigma\sqrt{N + N(N-1)\rho}$ | $N$ stages of sigma $\sigma$, correlation $\rho$; $\sigma\sqrt N$ if independent | [19-10](../../courses/19-digital-vlsi-design/chapters/19-10-synthesis-and-sta.md) |
| Output-port required time $T_c - d_{\text{out}}$; multicycle: setup $N$, hold $N - 1$ | SDC conventions | [19-10](../../courses/19-digital-vlsi-design/chapters/19-10-synthesis-and-sta.md) |

## Floorplan, place and route, signoff

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Core area $= A_{\text{cells}}/u$ | $u$ target utilization; rows rounded up | [19-11](../../courses/19-digital-vlsi-design/chapters/19-11-place-route-signoff.md) |
| Strap IR drop: $IR/8$ fed at both ends, $IR/2$ at one end; largest feed spacing $\sqrt{8\Delta V_{\max}/(ri)}$ (fed at both ends) | Uniform current $I$ (or $i$ per length) on a strap of total resistance $R$ (or $r$ per length) | [19-11](../../courses/19-digital-vlsi-design/chapters/19-11-place-route-signoff.md) |
| HPWL $= (x_{\max} - x_{\min}) + (y_{\max} - y_{\min})$; HPWL ≤ RSMT ≤ RMST ≤ 1.5 RSMT | Steiner points on the Hanan grid; Hwang's bound | [19-11](../../courses/19-digital-vlsi-design/chapters/19-11-place-route-signoff.md) |
| Quadratic placement: minimize $\sum w_{ij}[(x_i - x_j)^2 + (y_i - y_j)^2]$, i.e. solve $Q\mathbf{x} = \mathbf{b}_x$ | $Q$ the weighted Laplacian of movable cells, pads in $\mathbf b$ | [19-11](../../courses/19-digital-vlsi-design/chapters/19-11-place-route-signoff.md) |
| Zero-skew tap $x = [t_2 - t_1 + rL(C_2 + cL/2)]/[r(C_1 + C_2 + cL)]$ | From subtree 1; outside $[0, L]$ means snaking | [19-11](../../courses/19-digital-vlsi-design/chapters/19-11-place-route-signoff.md) |
| H-tree with $k$ levels: $4^k$ sinks, source-to-sink length $D(1 - 2^{-k})$, total $1.5D(2^k - 1)$ | Square of side $D$ | [19-11](../../courses/19-digital-vlsi-design/chapters/19-11-place-route-signoff.md) |
| Routed net: 50% delay $\approx R_{eff}(C_w + C_L) + R_w(0.38C_w + 0.69C_L)$, with $R_{eff}$ the Liberty delay-versus-load slope (it already contains ln 2); Elmore constant $R_{eq}(C_w + C_L) + R_w(C_w/2 + C_L)$ with $R_{eq} = R_{eff}/\ln 2$; clock power $C_{\text{clk}}V_{DD}^2f$ | Clock activity 1 | [19-11](../../courses/19-digital-vlsi-design/chapters/19-11-place-route-signoff.md) |

## Design for test

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Defect level $\text{DL} = 1 - Y^{1-T} \approx (1 - T)(-\ln Y)$ | Williams–Brown; $Y$ yield, $T$ fault coverage | [19-12](../../courses/19-digital-vlsi-design/chapters/19-12-design-for-test.md) |
| Single stuck-at faults $= 2 \times$ (stems + fanout branches) | Before collapsing; $n + 1$ tests for an $n$-input AND or NAND | [19-12](../../courses/19-digital-vlsi-design/chapters/19-12-design-for-test.md) |
| Random patterns for confidence $P_d$: $N = \ln(1 - P_d)/\ln(1 - p)$ | $p = 2^{-k}$ for $k$ required input values | [19-12](../../courses/19-digital-vlsi-design/chapters/19-12-design-for-test.md) |
| Scan cycles $P(L + 1) + L$, $L = \lceil F/C \rceil$; data $\approx 2FP$ bits | $F$ flip-flops, $C$ chains, $P$ patterns | [19-12](../../courses/19-digital-vlsi-design/chapters/19-12-design-for-test.md) |
| Maximal LFSR period $2^n - 1$; MISR aliasing $(2^{n(m-1)} - 1)/(2^{nm} - 1) \approx 2^{-n}$ | Primitive polynomial; $m$ response words | [19-12](../../courses/19-digital-vlsi-design/chapters/19-12-design-for-test.md) |
| March C−: $10n$ operations | $n$ cells | [19-12](../../courses/19-digital-vlsi-design/chapters/19-12-design-for-test.md) |

## Verification

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Equal bins: $E[T] = nH_n \approx n\ln n + 0.577n + \tfrac12$; $\Pr(\text{all covered after } t) = \sum_{k} (-1)^k\binom{n}{k}(1 - k/n)^t$ | Independent samples | [19-13](../../courses/19-digital-vlsi-design/chapters/19-13-verification-methods.md) |
| Unequal bins: $E[T] = \sum_{S \ne \emptyset} (-1)^{\lvert S\rvert+1}/p(S) \ge 1/p_{\min}$ | Inclusion–exclusion; the rarest bin dominates | [19-13](../../courses/19-digital-vlsi-design/chapters/19-13-verification-methods.md) |
| A bug needing $m$ specific input bits: $p = 2^{-m}$; 99 % detection needs $\approx 4.6 \times 2^m$ random vectors | Uniform random stimulus | [19-13](../../courses/19-digital-vlsi-design/chapters/19-13-verification-methods.md) |
| Round-robin arbiter: at most $N - 1$ grants to others while pending | Fixed priority: unbounded | [19-13](../../courses/19-digital-vlsi-design/chapters/19-13-verification-methods.md) |
| Miter $M = \bigvee_k (F_k \oplus G_k)$: equivalent iff $M \equiv 0$ | Any satisfying input is a counterexample | [19-13](../../courses/19-digital-vlsi-design/chapters/19-13-verification-methods.md) |
| ROBDD of $\sum_{i=1}^n x_iy_i$: $2n$ nodes interleaved, $2^{n+1} - 2$ separated | Node count at a level = distinct subfunctions depending on that variable | [19-13](../../courses/19-digital-vlsi-design/chapters/19-13-verification-methods.md) |
| Reachability $R_{k+1} = R_k \cup \operatorname{Post}(R_k)$; BMC: $I(s_0) \wedge \bigwedge T(s_i, s_{i+1}) \wedge \bigvee \neg P(s_i)$ | BMC is a proof only if the bound reaches the diameter | [19-13](../../courses/19-digital-vlsi-design/chapters/19-13-verification-methods.md) |
| k-induction: no violation within $k - 1$ steps, and every $T$-path of $k$ $P$-states steps to a $P$-state | Step checked over all states; CTIs need larger $k$ or a lemma | [19-13](../../courses/19-digital-vlsi-design/chapters/19-13-verification-methods.md) |
