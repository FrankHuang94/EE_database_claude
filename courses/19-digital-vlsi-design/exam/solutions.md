# Course 19 · Final Exam Solutions (Digital VLSI Design)

Exam: [README.md](README.md). Every number below is recomputed by [verify_19_exam.py](../verify/verify_19_exam.py). Answers with a non-trivial route are recomputed independently, as listed here; closed-form arithmetic is re-evaluated directly:

- the inverter by solving the square-law current balance numerically, and its delay by integrating the discharge ODE;
- Elmore constants by building the RC networks as matrices; pseudo-NMOS and charge sharing by root finding;
- logical-effort sizing by numerical minimization of path delay over the gate sizes and the stage count;
- the repeater optimum by numerical minimization over $(k, h)$, with the distributed line's 0.38 coefficient confirmed from its Fourier-series step response;
- power, leakage and DVFS by root finding on the alpha-power law; synchronizer MTBF from its definition;
- SRAM read disturbance with the 19-08 lab model, yield by Poisson sums;
- Euler orderings by brute force over all 24 orderings with the 19-09 lab's graph tools;
- the timing graph by a separate topological pass, path sigma from the covariance matrix;
- the zero-skew tap by equating Elmore delays numerically; wirelengths with the 19-11 lab;
- defect level, scan cycles and coverage closure by direct simulation or exact sums; BMC by state-graph search;
- the diligence numbers from first principles.

---

## Solutions

### Solution 1

(a) Equal widths give $r = k_n/k_p = \mu_n/\mu_p$ = 2.4, $\sqrt r = 1.5492$:

$$
V_M = \frac{0.30 \times 1.5492 + 1.0 - 0.35}{1 + 1.5492} = \frac{1.1148}{2.5492} = 0.4373\ \text{V} .
$$

The stronger NMOS pulls $V_M$ below the midpoint.

(b) $r = \left(\frac{V_{DD} - \lvert V_{TP}\rvert - V_M}{V_M - V_{TN}}\right)^2 = (0.15/0.20)^2$ = **0.5625**, so $W_p/W_n = (\mu_n/\mu_p)/r = 2.4/0.5625$ = **4.267**. Raising $V_M$ to 0.50 V costs a PMOS more than four times wider than the NMOS, because $V_M$ moves only with $\sqrt r$.

(c) With $r = 1$: $V_{IL} = (3V_{DD} + 2V_{TH})/8 = (3 + 0.6)/8$ = **0.450** V and $V_{IH} = (5V_{DD} - 2V_{TH})/8$ = **0.550** V. With $V_{OL} = 0$ and $V_{OH} = V_{DD}$, both noise margins are **0.450** V, 45% of the supply.

(d) At $V_M$ = 0.5 V, $V_{ov}$ = 0.2 V. Exact symmetric form: $\lvert A_v\rvert = 2(1 + \lambda V_{DD}/2)/(\lambda V_{ov}) = 2 \times 1.04/0.016$ = **130**; approximation $2/(\lambda V_{ov})$ = **125**. The output swings over about $V_{DD}/\lvert A_v\rvert$ = **7.69** mV of input. $\sigma_{V_M} = \sigma_{VT}\sqrt{r + 1}/(1 + \sqrt r) = 20/\sqrt2$ = **14.14** mV: each threshold moves $V_M$ by half its own shift ($\partial V_M/\partial V_{TN} = -\partial V_M/\partial\lvert V_{TP}\rvert = \tfrac12$), so each contributes a quarter of $\sigma_{VT}^2$, and together half.

### Solution 2

(a) $C_{in} = 1.1 \times 1.5$ = **1.65** fF; $C_{int} = 0.9 \times 1.5$ = **1.35** fF; $C_{ext} = 3 \times 1.65 + 3$ = **7.95** fF; $C_L$ = **9.30** fF; $\gamma = C_{int}/C_g = 1.35/1.65$ = **0.818**.

(b) $V_{ov} = 0.70$ V and $V_{TN} < V_{DD}/2$, so

$$
t_{pHL} = \frac{C_L}{k_nV_{ov}}\left[\frac{2V_{TN}}{V_{ov}} + \ln\left(\frac{4V_{ov}}{V_{DD}} - 1\right)\right] = \frac{12\ \text{fF}}{250\ \mu\text{A/V}^2 \times 0.7\ \text{V}}\,[0.8571 + \ln 1.8] = 68.57\ \text{ps} \times 1.4449 = 99.08\ \text{ps} .
$$

(c) $I_{sat} = \tfrac12 \times 250\ \mu\text{A/V}^2 \times 0.49\ \text{V}^2$ = **61.25** µA; $R_{eq} = 3 \times 1.0/(4 \times 61.25\ \mu\text{A})$ = **12.24** kΩ; $t_p = \ln 2 \times 12.24\ \text{k}\Omega \times 12\ \text{fF}$ = **101.9** ps, a few percent above the exact value.

(d) $t_p = 1/(2Nf) = 1/(2 \times 41 \times 320\ \text{MHz})$ = **38.11** ps. In a ring each stage is driven by the previous stage's slow ramp, not a step: the driving transistor turns on gradually and both transistors conduct for part of the transition, so the stage delay exceeds the step-input value (19-02 measured almost 2×).

### Solution 3

(a) NAND4: four series NMOS of width **4**, parallel PMOS of width 2; input capacitance $(4 + 2)/3$ = **2.00** times the inverter's. NOR4: four series PMOS of width **8**, parallel NMOS of width 1; $(1 + 8)/3$ = **3.00**. The NOR is 50% heavier because the slow PMOS are the stacked ones.

(b) The output node carries $(1 + \mu)cN + C_{ext} = 3 \times 0.6 \times 3 + 15 = 20.4$ fF through all $3R/3 = R$ of the stack; the internal nodes carry $cN$ = 1.8 fF each through $R/3$ and $2R/3$:

$$
\tau_E = Rc\,\frac{N(N-1)}{2} + R\left[(1 + \mu)cN + C_{ext}\right] = 8\ \text{k}\Omega \times 1.8\ \text{fF} + 8\ \text{k}\Omega \times 20.4\ \text{fF} = 14.4 + 163.2 = 177.6\ \text{ps},
$$

and $t_p \approx 0.69\,\tau_E$ = **122.5** ps.

(c) $I_{load} = \tfrac12 \times 60\ \mu\text{A/V}^2 \times 0.7^2$ = **14.7** µA. With $a = V_{DD} - V_{TN} = 0.7$ V, $V_{OL} = a - \sqrt{a^2 - 2I_{load}/k_n} = 0.7 - \sqrt{0.49 - 0.098}$ = **0.0739** V. Check the load: the PMOS has $V_{SD} = 1.0 - 0.0739 = 0.926$ V, above $V_{SG} - \lvert V_{TP}\rvert = 0.7$ V, so it is saturated as assumed. Static power while low: $1.0\ \text{V} \times 14.7\ \mu\text{A}$ = **14.7** µW.

(d) The boundary is $C_a/C_L = V_{TN}/(V_{DD} - V_{TN}) = 0.3/0.7$ = **0.4286**. For $C_a$ = 4 fF ($C_a/C_L$ = 0.333, below the boundary) full sharing would give $12/16 = 0.75$ V, above $V_{DD} - V_{TN}$ = 0.7 V, so the connecting transistor cuts off first: the internal node stops at 0.7 V, the output loses $\Delta V = (C_a/C_L)(V_{DD} - V_{TN})$ = **0.233** V and settles at **0.767** V. For $C_a$ = 6 fF (above the boundary) the nodes equalize: $12/18$ = **0.667** V, close to an inverter's switching threshold.

### Solution 4

(a) $G = g_{NOR2}\,g_{INV}\,g_{NAND3}\,g_{INV} = \tfrac53 \times 1 \times \tfrac53 \times 1$ = **2.778**; $B$ = **3** (the inverter drives three NAND3 inputs, one on the path); $H = 180/6$ = **30**; $F = GBH$ = **250**. $P = 2 + 1 + 3 + 1$ = **7**.

(b) $\hat f = F^{1/4} = 250^{1/4}$ = **3.976**; $\hat D = 4 \times 3.976 + 7$ = **22.91** τ.

(c) Backward, $C_{in} = gC_{out}/\hat f$: last inverter $180/3.976$ = **45.27**; NAND3 $\tfrac53 \times 45.27/3.976$ = **18.97**; the inverter drives $3 \times 18.97 = 56.92$, so its input is $56.92/3.976$ = **14.31**; NOR2 $\tfrac53 \times 14.31/3.976$ = **6.00**, matching the given input: the sizing is consistent.

(d) $\hat N = \ln F/\ln\rho = \ln 250/\ln 3.59$ = **4.32**, so four or five stages. Five (one extra inverter, $P$ = 8): $5 \times 250^{1/5} + 8$ = **23.09** τ, slightly worse because the extra stage's parasitic delay outweighs the lower stage effort; and five stages would also invert the logic. Keep four: $22.91 \times 12$ ps = **274.9** ps.

### Solution 5

(a) $R_w = 8 \times 2000$ = **16** kΩ, $C_w = 0.2 \times 2000$ = **400** fF, $R_wC_w$ = 6.4 ns. Distributed: $0.38 \times 6.4$ = **2.432** ns; lumped: $0.69 \times 6.4$ = **4.416** ns, a large overestimate.

(b) $t \approx 0.69R_d(C_w + C_L) + R_w(0.38C_w + 0.69C_L) = 0.69 \times 2\ \text{k}\Omega \times 420\ \text{fF} + 16\ \text{k}\Omega \times (152 + 13.8)\ \text{fF} = 0.580 + 2.653$ = **3.232** ns; the wire-resistance term is **82.1** % of it, so a bigger driver barely helps.

(c) $k_{opt} = \sqrt{0.38R_wC_w/(0.69R_0C_0)} = \sqrt{2.432\ \text{ns}/1.38\ \text{ps}}$ = **41.98** (use **42** repeaters, about **48** µm apart); $h_{opt} = \sqrt{R_0C_w/(R_wC_0)} = \sqrt{4\ \text{ns}/3.2\ \text{ps}}$ = **35.36**. $T_{min} = (2\sqrt{0.69 \times 0.38} + 1.38)\sqrt{R_0C_0R_wC_w} = 2.404 \times \sqrt{2\ \text{ps} \times 6.4\ \text{ns}} = 2.404 \times 113.1\ \text{ps}$ = **272.0** ps, **11.88** times faster than (b).

(d) The quiet neighbor and the ground capacitance both hold the victim: $\Delta V = 1.0 \times 30/(30 + 30 + 40)$ = **0.300** V. Effective capacitance $C_g + \text{MCF} \times \sum C_c$: both switching with it, MCF 0: **40** fF; both quiet, MCF 1: **100** fF; both against it, MCF 2: **160** fF. A 4× spread in load is why timing analysis must know the neighbors' switching windows.

### Solution 6

(a) $P = 0.12 \times 400\ \text{pF} \times 0.75^2 \times 1.5\ \text{GHz}$ = **40.5** mW. Clock: $150\ \text{pF} \times 0.5625 \times 1.5\ \text{GHz}$ = **126.6** mW, three times the logic, which is why clocks are gated; gated 40% of the time it falls to **75.9** mW.

(b) $S = nV_T\ln 10 = 1.35 \times 25.85\ \text{mV} \times 2.3026$ = **80.35** mV/decade. A 60 mV lower threshold multiplies leakage by $10^{60/80.35}$ = **5.58**.

(c) Frequency scales as $(V_{DD} - V_{TH})^{1.3}/V_{DD}$; at 0.9 V this is $0.6^{1.3}/0.9$. Halving it, $(V - 0.3)^{1.3}/V = \tfrac12 \times 0.6^{1.3}/0.9 = 0.2860$, has the root $V$ = **0.536** V (by iteration). Power scales as $V^2f$: $(0.536/0.9)^2 \times 0.5$ = **0.178**; energy per operation as $V^2$: **0.355**. Halving the speed cuts power more than fivefold and energy per operation almost threefold.

(d) The rail draws $CV^2 = 800\ \text{pF} \times 0.5625\ \text{V}^2$ = **0.45** nJ from the supply; with control, **0.50** nJ. Break-even: $0.50\ \text{nJ}/3\ \text{mW}$ = **166.7** ns. Gating shorter idle periods costs energy.

### Solution 7

(a) $T_c \ge t_{pcq} + t_{pd} + t_{setup} - \delta + t_{jitter} = 45 + 380 + 25 - 20 + 12$ = **442** ps, so $f_{max}$ = **2.262** GHz. The late capture clock helps setup.

(b) Hold slack $= t_{ccq} + t_{cd} - t_{hold} - \delta = 25 + 10 - 20 - 20$ = **−5** ps. Add at least 5 ps of delay to the short path (buffers); slowing the clock does nothing, because hold does not depend on the period. The same skew that helped setup hurts hold.

(c) $T_c = t_L/N + t_o \le 400$ ps needs $N \ge 1800/330 = 5.45$, so **6** stages: $T_c = 300 + 70 = 370$ ps, **2.703** GHz; latency $6 \times 370$ = **2220** ps, longer than the unpipelined 1800 ps; overhead share $70/370$ = **18.9** %.

(d) $\text{MTBF} = e^{t_r/\tau}/(T_0f_{clk}f_{data}) = e^{600/18}/(15\ \text{ps} \times 1.5\ \text{GHz} \times 80\ \text{MHz}) = 3.00 \times 10^{14}/1.8 \times 10^6$ = **1.66 × 10⁸** s, about **5.27** years: too short for a product. A second flip-flop adds a full 666.7 ps cycle, multiplying the MTBF by $e^{666.7/18}$ = **1.22 × 10¹⁶**.

### Solution 8

(a) Solve $\tfrac12k_A(V_{DD} - \Delta V - V_{TH})^2 = k_N[(V_{DD} - V_{TH})\Delta V - \tfrac12\Delta V^2]$ with $k_N = 180$ µA/V²: $50(0.6 - \Delta V)^2 = 180(0.6\Delta V - 0.5\Delta V^2)$, i.e. $140\Delta V^2 - 168\Delta V + 18 = 0$, whose smaller root is $\Delta V$ = **0.1189** V. The margin to $V_{TN}$ is **0.181** V.

(b) $C_{BL} = 512 \times 0.07 + 12$ = **47.84** fF; $t = C_{BL}\Delta V/I_{cell} = 47.84\ \text{fF} \times 0.09\ \text{V}/18\ \mu\text{A}$ = **239.2** ps. Regeneration: $\tau\ln(V_{DD}/\Delta V) = 12\ \text{ps} \times \ln 10$ = **27.63** ps. Small-swing sensing makes the bitline the dominant term.

(c) From the sheet's table, $Q(5.5)$ = **1.90 × 10⁻⁸**; expected failures $2^{28} \times 1.90 \times 10^{-8}$ = **5.10**; yield without repair $e^{-5.10}$ = **0.611** %. With redundancy that repairs $s$ failing cells, the yield is the Poisson probability of at most $s$ failures: $s = 10$ gives 98.44 % and $s$ = **11** gives **99.37** %. For 99% without repair, $Q(z) = -\ln 0.99/2^{28}$ = **3.74 × 10⁻¹¹**, so $z$ = **6.51** σ (between the table's 6.5σ and 7σ entries, or by iterating the asymptotic form). Half a sigma of margin is worth eleven spare rows or columns.

(d) Bitcells: $64 \times 2^{20} \times 0.0175\ \mu\text{m}^2$ = **1.174** mm²; macro $1.174/0.72$ = **1.631** mm²; density $67.11\ \text{Mb}/1.631\ \text{mm}^2$ = **41.1** Mb/mm².

### Solution 9

(a) Contacted pitch $2 + 2 \times 2 + 2$ = **8** λ; uncontacted $2 + 3$ = **5** λ. Each end of the strip needs $1 + 2 + 2 = 5\lambda$ (enclosure, contact, contact-to-gate). Uncontacted internals: $2 \times 5 + 4 \times 2 + 3 \times 3$ = **27** λ = **2.43** µm. Contacting every internal node: $2 \times 5 + 4 \times 2 + 3 \times 6$ = **36** λ = **3.24** µm, a third longer. Internal stack nodes are left uncontacted.

(b) Pull-down, as drawn: output – ($A \parallel B$) – $C$ – $D$ – ground; pull-up (the dual): ($A$ in series with $B$) in parallel with $C$ and with $D$, between $V_{DD}$ and the output. An ordering must be an Euler path of both graphs. In the pull-down, $A$ and $B$ join the same two nodes (output and the $A \parallel B$/$C$ node), and the output node has degree 2, so the path must start or end there with $A$ and $B$ adjacent; $C$ and $D$ then follow in the stack's order, so they are adjacent at the other end. Checking the $4! = 24$ orderings, **4** satisfy both graphs: A-B-C-D, B-A-C-D, D-C-A-B and D-C-B-A. If the series stack may be reordered (for example $C$ – ($A \parallel B$) – $D$, or $D$ next to the output), more orderings open up: **8** in all (A-B-C-D, A-B-D-C, B-A-C-D, B-A-D-C, C-D-A-B, C-D-B-A, D-C-A-B, D-C-B-A), because the parallel pair only has to sit at one end of the stack.

(c) Logic: $350/150$ = **2.333** mm²; flip-flops $20\,000 \times 25\ \mu\text{m}^2/0.65$ = **0.769** mm² (routed density already includes utilization; flip-flop cell area does not). Block ≈ **3.103** mm².

(d) Gate area $0.3\ \mu\text{m}^2$; allowed metal area $250 \times 0.3 = 75\ \mu\text{m}^2$; length $75/0.25$ = **300** µm. (Real rules such as SKY130's also count the line's sidewall area, which shortens the limit considerably; see 19-09.)

### Solution 10

(a) Arrival times: $AT(G1) = \max(0, 0.10) + 0.20$ = **0.30** ns; $AT(G2) = 0.10 + 0.35$ = **0.45** ns; $AT(G3) = \max(0.30, 0.45) + 0.15$ = **0.60** ns. Required times backward: G3 0.70; G1 and G2 $0.70 - 0.15$ = 0.55; $a$: $0.55 - 0.20 = 0.35$; $b$: $\min(0.55 - 0.20, 0.55 - 0.35)$ = 0.20. Slacks: $a$ **0.35**, $b$ **0.10**, G1 **0.25**, G2 **0.10**, G3 **0.10** ns. The critical path is $b \to$ G2 $\to$ G3, with slack 0.10 ns.

(b) $\text{slack} = T_c + L_2 - t_{setup} - U - (L_1 + t_{pcq} + t_{pd}) = 1.20 + 0.28 - 0.06 - 0.05 - 1.09$ = **0.28** ns. Shortest period $1.20 - 0.28$ = **0.92** ns, **1.087** GHz.

(c) Hold: $(0.35 + 0.09 + 0.04) - (0.28 + 0.03 + 0.02)$ = **0.15** ns. With $L_2$ = 0.60 ns: setup slack **0.60** ns, hold slack $0.48 - 0.65$ = **−0.17** ns. Add at least 0.17 ns to the short path. Inserted on a segment only the short path uses, setup is untouched; even on a shared segment, setup slack falls only to **0.43** ns. Skew that helps setup hurts hold by the same amount.

(d) $\sigma_{path} = \sigma\sqrt{N + N(N-1)\rho} = 8\sqrt{12 + 132 \times 0.2} = 8\sqrt{38.4}$ = **49.57** ps; 3σ = **148.7** ps. Independent: $3 \times 8\sqrt{12}$ = **83.14** ps. Correlation nearly doubles the margin: random variation averages out along a path only when it is independent.

### Solution 11

(a) Core $1.20/0.70$ = **1.714** mm²; side $\sqrt{1.714}$ = **1.309** mm.

(b) $r = 0.047/1.6 = 0.02938$ Ω/µm, $R = 0.02938 \times 400$ = **11.75** Ω. Both ends: $IR/8 = 3\ \text{mA} \times 11.75\ \Omega/8$ = **4.41** mV; one end: $IR/2$ = **17.6** mV. Current per length $i$ = 7.5 µA/µm; largest spacing $\sqrt{8\Delta V/(ri)} = \sqrt{0.08/(0.02938 \times 7.5 \times 10^{-6})}$ = **602.6** µm.

(c) $rL = 150$ Ω, $cL = 60$ fF:

$$
x = \frac{t_2 - t_1 + rL(C_2 + cL/2)}{r(C_1 + C_2 + cL)} = \frac{5\ \text{ps} + 150 \times 60\ \text{fF}}{0.5 \times 110\ \text{fF}} = \frac{14\ \text{ps}}{0.055\ \text{ps/µm}} = 254.5\ \mu\text{m} .
$$

Delay to sink 1: $rx(cx/2 + C_1) + t_1 = 127.3\ \Omega \times 45.45\ \text{fF} + 50\ \text{ps}$ = **55.79** ps; to sink 2: $22.73\ \Omega \times 34.55\ \text{fF} + 55\ \text{ps}$ = 55.79 ps. Zero skew.

(d) HPWL $= (40 - 0) + (50 - 0)$ = **90** µm. Spanning tree (Manhattan distances, Prim): (0,0)–(40,10) 50, (40,10)–(30,30) 30, (30,30)–(10,50) 40, total **120** µm. Steiner tree: one Steiner point on the Hanan grid at (10, 30) joins (0, 0) (40 µm), (10, 50) (20 µm) and (30, 30) (20 µm), and (30, 30) connects to (40, 10) (30 µm): **110** µm, the minimum over Hanan-grid Steiner points. Check: $90 \le 110 \le 120 \le 1.5 \times 110$ ✓.

### Solution 12

(a) $\text{DL} = 1 - 0.85^{0.02}$ = 0.003245 = **3245** DPPM. For 200 DPPM: $1 - T = \ln(1 - 2 \times 10^{-4})/\ln 0.85 = 1.231 \times 10^{-3}$, so $T$ = **99.877** %.

(b) $L = 200\,000/100 = 2000$; cycles $P(L + 1) + L = 3000 \times 2001 + 2000$ = **6 005 000**; at 50 MHz, **120.1** ms. Data ≈ $2FP = 2 \times 200\,000 \times 3000 = 1.2 \times 10^9$ bits = **150** MB, before compression.

(c) Inclusion–exclusion: singles $1/0.6 + 1/0.3 + 1/0.1 = 15.000$; pairs $1/0.9 + 1/0.7 + 1/0.4 = 5.040$; all three $1/1 = 1$. $E = 15.000 - 5.040 + 1$ = **10.96** transactions, only 10% above $1/p_{\min}$ = **10**: the rare bin dominates.

(d) From 0 the counter visits 0 to 5 and returns: **6** states are reachable, and 6 and 7 are not. The property is not 1-inductive: the unreachable state **6** satisfies $x \ne 7$ and steps to 7, a counterexample to induction. For $k = 2$ the step needs two consecutive $P$-states before a 7, i.e. a predecessor of 6, and 6 has none (5 goes to 0), so no such path exists; with the base case (no violation within one step of 0) the property is **2**-inductive. The lemma $x \le 5$ holds at 0 and is preserved by every step from 0 to 5, so it is 1-inductive and implies $x \ne 7$.

### Solution 13

(a) *Assumptions:* square law, λ = 0, both transistors saturated at $V_{in} = V_{out} = V_M$ (true near the threshold). Equate currents: $\tfrac12k_n(V_M - V_{TN})^2 = \tfrac12k_p(V_{DD} - V_M - \lvert V_{TP}\rvert)^2$. Both overdrives are positive, so take square roots: $\sqrt r(V_M - V_{TN}) = V_{DD} - V_M - \lvert V_{TP}\rvert$, giving $V_M = (V_{TN}\sqrt r + V_{DD} - \lvert V_{TP}\rvert)/(1 + \sqrt r)$. With $r = 1$ and $V_{TN} = \lvert V_{TP}\rvert$, $V_M = V_{DD}/2$. Differentiating, $\partial V_M/\partial V_{TN} = \sqrt r/(1 + \sqrt r)$; for $r$ = 2.4, **0.608**: the stronger device's threshold matters more. *Rubric (4):* current balance with saturation justified (1), algebra (1), symmetric case (1), sensitivity and value (1).

(b) Set the partial derivatives to zero. $\partial T/\partial k = 0.69R_0C_0 - 0.38R_wC_w/k^2 = 0 \Rightarrow k_{opt} = \sqrt{0.38R_wC_w/(0.69R_0C_0)}$. $\partial T/\partial h = -0.69R_0C_w/h^2 + 0.69R_wC_0 = 0 \Rightarrow h_{opt} = \sqrt{R_0C_w/(R_wC_0)}$. Each segment has wire $R_w/k$, $C_w/k$, so its distributed delay is $0.38R_wC_w/k^2$, which at $k_{opt}$ equals $0.69R_0C_0$, the delay of a repeater driving a copy of itself. Both terms are balanced, as in any optimum of $a/k + bk$. For Question 5: $0.69 \times 10\ \text{k}\Omega \times 0.2\ \text{fF}$ = **1.38** ps. *Rubric:* both derivatives (2), the equality (1), the value (1).

(c) $D = \sum f_i + P$ with $\prod f_i = F$ fixed. By the AM–GM inequality, $\tfrac1N\sum f_i \ge (\prod f_i)^{1/N} = F^{1/N}$, with equality iff all $f_i$ are equal; so $\hat f = F^{1/N}$ and $\hat D = NF^{1/N} + P$. (Equivalently, a Lagrange multiplier on $\sum \ln f_i = \ln F$ gives $f_i = \text{const}$.) Now let $N$ vary, each added inverter adding $p_{inv}$: $D(N) = NF^{1/N} + P_0 + (N - n_0)p_{inv}$. Then $dD/dN = F^{1/N} - F^{1/N}\ln F/N + p_{inv} = 0$; with $\rho = F^{1/N}$, $\ln F/N = \ln\rho$, so $\rho(\ln\rho - 1) = p_{inv}$. For $p_{inv}$ = 1.5, solving numerically gives ρ = **3.97**. *Rubric:* AM–GM or Lagrange (2), derivative (1), root (1).

### Solution 14

(a) $P_{dyn} = 0.25 \times 1.6\ \mu\text{F} \times 0.75^2 \times 1.2\ \text{GHz}$ = **270** W, leaving **180** W (40% of 450 W) for leakage, I/O, SerDes and memory interfaces; power density **0.75** W/mm². The numbers hang together if leakage and I/O really are 40%, which is high but possible for a large leaky 3 nm die at high temperature. Ask for the measured or simulated breakdown (dynamic, leakage at temperature, I/O, HBM interface), the corner (typical or worst case), and the cooling plan for 0.75 W/mm². *Rubric (3):* dynamic power (1), remainder and density (1), sensible questions (1).

(b) Frequency scales by $\left(\frac{0.55}{0.45}\right)^{1.3}\frac{0.75}{0.85}$ = **1.145**, giving **1.374** GHz, not 2.0 GHz. Dynamic power rises by $(0.85/0.75)^2 \times 1.145$ = **1.471**, to **397** W before leakage, which rises too. By the same law a 2 GHz turbo would need about **1.34** V, which is beyond the process's reliability limits and the thermal budget. *Rubric:* frequency (1), power (1), conclusion (1).

(c) $\text{DL} = 1 - 0.55^{0.03}$ = **17 775** DPPM (**1.78** %), not 50. 50 DPPM needs $T$ = **99.9916** %. Ask which fault models (stuck-at, transition, cell-aware, memory BIST) and what coverage each reaches, the burn-in and system-level test plan, the in-field self-test plan for a datacenter part (silent data corruption), and how the 55% yield was estimated. *Rubric:* defect level (1), required coverage (1), questions (1).

(d) 512 MB = $2^{32}$ bits; $4.295 \times 10^9 \times 0.021\ \mu\text{m}^2$ = **90.19** mm² of bitcells, **128.8** mm² at 70% efficiency, **21.5** % of the die: plausible. The verification claim is not: in the Siemens/Wilson functional verification study released in September 2026 [Industry estimate], only 5% of IC/ASIC respondents reported first-silicon success (14.4% in 2024). Read that with its caveats: a tool vendor sponsors the survey, the recruitment method changed in 2024, and 5% of 320 is at most about 16 respondents. Even so, the direction is clear, and no team "fully verifies" a large SoC. Questions: (1) "What was your coverage closure, with which waivers, and which blocks are formally proven?" (2) "When did your compiler and runtime first run on emulation, and for how many cycles?" (3) "What is your plan and budget for a respin, and which bugs would a metal-only fix cover?" *Rubric:* SRAM area and share (1), the first-silicon data with its source and caveats (1), three good questions (1).

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| X19.1a | switching threshold, equal widths | 0.4373 | V |
| X19.1b | ratio r for V_M = 0.50 V | 0.5625 | — |
| X19.1c | W_p/W_n for V_M = 0.50 V | 4.267 | — |
| X19.1d | V_IL, symmetric | 0.450 | V |
| X19.1e | V_IH, symmetric | 0.550 | V |
| X19.1f | gain at V_M, exact symmetric form | 130 | — |
| X19.1g | gain, approximation | 125 | — |
| X19.1h | transition input width | 7.69 | mV |
| X19.1i | sigma of V_M | 14.14 | mV |
| X19.2a | input capacitance | 1.65 | fF |
| X19.2b | C_int | 1.35 | fF |
| X19.2c | C_ext | 7.95 | fF |
| X19.2d | C_L | 9.30 | fF |
| X19.2e | gamma | 0.818 | — |
| X19.2f | exact t_pHL | 99.08 | ps |
| X19.2g | I_sat | 61.25 | µA |
| X19.2h | R_eq | 12.24 | kΩ |
| X19.2i | RC-model delay | 101.9 | ps |
| X19.2j | ring stage delay | 38.11 | ps |
| X19.3a | NAND4 NMOS width | 4 | — |
| X19.3b | NAND4 input capacitance ratio | 2.00 | — |
| X19.3c | NOR4 PMOS width | 8 | — |
| X19.3d | NOR4 input capacitance ratio | 3.00 | — |
| X19.3e | NAND3 Elmore constant | 177.6 | ps |
| X19.3f | NAND3 delay estimate | 122.5 | ps |
| X19.3g | pseudo-NMOS load current | 14.7 | µA |
| X19.3h | pseudo-NMOS V_OL | 0.0739 | V |
| X19.3i | static power while low | 14.7 | µW |
| X19.3j | charge-sharing boundary | 0.4286 | — |
| X19.3k | output with 4 fF | 0.767 | V |
| X19.3l | output with 6 fF | 0.667 | V |
| X19.3m | charge-sharing loss with 4 fF | 0.233 | V |
| X19.3n | load PMOS source-drain voltage | 0.926 | V |
| X19.4a | path logical effort | 2.778 | — |
| X19.4b | branching effort | 3 | — |
| X19.4c | electrical effort | 30 | — |
| X19.4d | path effort | 250 | — |
| X19.4e | parasitic delay | 7 | τ |
| X19.4f | stage effort | 3.976 | — |
| X19.4g | minimum delay | 22.91 | τ |
| X19.4h | last inverter input | 45.27 | units |
| X19.4i | NAND3 input | 18.97 | units |
| X19.4j | second inverter input | 14.31 | units |
| X19.4k | NOR2 input check | 6.00 | units |
| X19.4l | best stage count | 4.32 | — |
| X19.4m | five-stage delay | 23.09 | τ |
| X19.4n | delay at τ = 12 ps | 274.9 | ps |
| X19.5a | wire resistance | 16 | kΩ |
| X19.5b | wire capacitance | 400 | fF |
| X19.5c | distributed 50 % delay | 2.432 | ns |
| X19.5d | lumped delay | 4.416 | ns |
| X19.5e | driver–wire–load delay | 3.232 | ns |
| X19.5f | wire-resistance share | 82.1 | % |
| X19.5g | optimal repeater count | 41.98 | — |
| X19.5h | optimal repeater size | 35.36 | — |
| X19.5i | repeated delay | 272.0 | ps |
| X19.5j | speed-up | 11.88 | — |
| X19.5k | floating-victim noise | 0.300 | V |
| X19.5l | effective capacitance, same direction | 40 | fF |
| X19.5m | effective capacitance, quiet | 100 | fF |
| X19.5n | effective capacitance, opposite | 160 | fF |
| X19.5o | repeaters used | 42 | — |
| X19.5p | repeater spacing | 48 | µm |
| X19.6a | logic dynamic power | 40.5 | mW |
| X19.6b | clock power | 126.6 | mW |
| X19.6c | gated clock power | 75.9 | mW |
| X19.6d | subthreshold slope | 80.35 | mV/dec |
| X19.6e | leakage factor | 5.58 | — |
| X19.6f | supply for half frequency | 0.536 | V |
| X19.6g | power ratio | 0.178 | — |
| X19.6h | energy ratio | 0.355 | — |
| X19.6i | break-even time | 166.7 | ns |
| X19.6j | rail recharge energy | 0.45 | nJ |
| X19.6k | total wake energy | 0.50 | nJ |
| X19.7a | minimum period | 442 | ps |
| X19.7b | maximum frequency | 2.262 | GHz |
| X19.7c | hold slack | -5 | ps |
| X19.7d | pipeline stages | 6 | — |
| X19.7e | pipelined frequency | 2.703 | GHz |
| X19.7f | latency | 2220 | ps |
| X19.7g | overhead share | 18.9 | % |
| X19.7h | synchronizer MTBF | 1.66e8 | s |
| X19.7i | MTBF in years | 5.27 | years |
| X19.7j | second flip-flop factor | 1.22e16 | — |
| X19.8a | read disturbance | 0.1189 | V |
| X19.8b | margin to V_TN | 0.181 | V |
| X19.8c | bitline time | 239.2 | ps |
| X19.8d | sense time | 27.63 | ps |
| X19.8e | Q(5.5) | 1.90e-8 | — |
| X19.8f | expected failing cells | 5.10 | — |
| X19.8g | yield without repair | 0.611 | % |
| X19.8h | repairable cells for 99 % yield | 11 | — |
| X19.8m | yield with 11 repairs | 99.37 | % |
| X19.8n | Q target for 99 % without repair | 3.74e-11 | — |
| X19.8o | bitline capacitance | 47.84 | fF |
| X19.8i | margin for 99 % yield | 6.51 | σ |
| X19.8j | bitcell area | 1.174 | mm² |
| X19.8k | macro area | 1.631 | mm² |
| X19.8l | density | 41.1 | Mb/mm² |
| X19.9a | contacted pitch | 8 | λ |
| X19.9b | uncontacted pitch | 5 | λ |
| X19.9c | strip, uncontacted internals | 27 | λ |
| X19.9d | strip length in µm | 2.43 | µm |
| X19.9e | strip, contacted internals | 36 | λ |
| X19.9f | contacted strip in µm | 3.24 | µm |
| X19.9g | valid orderings, stack as drawn | 4 | — |
| X19.9j | valid orderings, stack reorderable | 8 | — |
| X19.9k | logic area | 2.333 | mm² |
| X19.9l | flip-flop area | 0.769 | mm² |
| X19.9h | block area | 3.103 | mm² |
| X19.9i | antenna length limit | 300 | µm |
| X19.10a | arrival at G1 | 0.30 | ns |
| X19.10b | arrival at G2 | 0.45 | ns |
| X19.10c | arrival at G3 | 0.60 | ns |
| X19.10d | slack at a | 0.35 | ns |
| X19.10e | slack at b | 0.10 | ns |
| X19.10f | slack at G1 | 0.25 | ns |
| X19.10g | setup slack | 0.28 | ns |
| X19.10h | shortest period | 0.92 | ns |
| X19.10i | highest frequency | 1.087 | GHz |
| X19.10j | hold slack | 0.15 | ns |
| X19.10k | setup slack with L2 = 0.60 ns | 0.60 | ns |
| X19.10l | hold slack with L2 = 0.60 ns | -0.17 | ns |
| X19.10m | path sigma | 49.57 | ps |
| X19.10n | 3-sigma margin | 148.7 | ps |
| X19.10o | independent 3-sigma margin | 83.14 | ps |
| X19.10p | setup slack after a shared-segment fix | 0.43 | ns |
| X19.10q | slack at G2 | 0.10 | ns |
| X19.10r | slack at G3 | 0.10 | ns |
| X19.11a | core area | 1.714 | mm² |
| X19.11b | core side | 1.309 | mm |
| X19.11c | strap resistance | 11.75 | Ω |
| X19.11d | IR drop, both ends | 4.41 | mV |
| X19.11e | IR drop, one end | 17.6 | mV |
| X19.11f | largest feed spacing | 602.6 | µm |
| X19.11g | zero-skew tap from subtree 1 | 254.5 | µm |
| X19.11h | tap-to-sink delay | 55.79 | ps |
| X19.11i | HPWL | 90 | µm |
| X19.11j | spanning-tree length | 120 | µm |
| X19.11k | Steiner-tree length | 110 | µm |
| X19.12a | defect level | 3245 | DPPM |
| X19.12b | coverage for 200 DPPM | 99.877 | % |
| X19.12c | scan clock cycles | 6005000 | — |
| X19.12d | scan test time | 120.1 | ms |
| X19.12e | test data volume | 150 | MB |
| X19.12f | expected transactions | 10.96 | — |
| X19.12g | floor 1/p_min | 10 | — |
| X19.12h | reachable states | 6 | — |
| X19.12i | counterexample to induction | 6 | — |
| X19.12j | smallest k | 2 | — |
| X19.13a | sensitivity of V_M to V_TN | 0.608 | — |
| X19.13b | repeater intrinsic delay | 1.38 | ps |
| X19.13c | best stage effort, p_inv = 1.5 | 3.97 | — |
| X19.14a | dynamic power | 270 | W |
| X19.14b | remainder | 180 | W |
| X19.14c | power density | 0.75 | W/mm² |
| X19.14d | frequency ratio at 0.85 V | 1.145 | — |
| X19.14e | frequency at 0.85 V | 1.374 | GHz |
| X19.14f | dynamic power ratio | 1.471 | — |
| X19.14g | dynamic power at 0.85 V | 397 | W |
| X19.14h | implied defect level | 17775 | DPPM |
| X19.14i | coverage for 50 DPPM | 99.9916 | % |
| X19.14n | implied defect level as a percentage | 1.78 | % |
| X19.14j | SRAM bitcell area | 90.19 | mm² |
| X19.14k | SRAM macro area | 128.8 | mm² |
| X19.14l | SRAM share of the die | 21.5 | % |
| X19.14m | supply for 2 GHz | 1.34 | V |
