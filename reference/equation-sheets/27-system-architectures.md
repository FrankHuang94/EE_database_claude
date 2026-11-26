# Equation Sheet · 27 System Architectures

The relations to know cold from Course 27, each with its conditions and the chapter that derives it.

Conventions:

- powers in watts and energies in joules or watt-hours as stated; a day is 24 h and a year 8760 h;
- "assumed" parameters in the chapters are illustrative; vendor figures are dated in each chapter's §7 and §9;
- the relations are first-order models: each chapter's Common mistakes section says where they break down.

## System analysis method (27-01)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $P_{batt} = \sum_k P_k/\eta_k$; $\eta_{sys} = \sum_k P_k/P_{batt}$; LDO $\eta \le V_{out}/V_{in}$ | Converter-chain power budget | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |
| $t = E_u/\bar P_{batt}$, $\bar P_{batt} = \sum_m d_mP_{batt,m}$ | Battery life from mode duty cycles $d_m$ | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |
| $P_{sus} = (T_{s,max} - T_a)/\theta_{sa}$ | Sustained power at the skin or case limit | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |
| $T(t) = T_\infty - (T_\infty - T_0)e^{-t/\tau}$; $t_b = \tau\ln\frac{T_\infty - T_0}{T_\infty - T_{s,max}}$; $d_{max} = \frac{P_{sus} - P_i}{P_b - P_i}$ | First-order thermal RC, $T_\infty = T_a + P\theta_{sa}$, $\tau = \theta_{sa}C_{th}$; burst time and duty | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |
| $\text{GM} = (\text{ASP} - \text{COGS})/\text{ASP}$ | Gross margin from the BOM roll-up | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |
| $P_{att} = \min(\Pi, I\beta)$; tokens/s $\approx \beta/(N_pb)$ | Roofline; bandwidth-bound decode with $b$ bytes per parameter | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |
| $d\ln(\text{perf})/dP = 1/(3P_{dyn})$; wider core pays if $g > p^{1/3}$ | Shadow price of a watt under a power cap ($P \propto f^3$) | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |

## Smartphone SoC (27-02)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $E_{inst}(f) = c(V_0 + kf)^2/\text{IPC} + P_s/(\text{IPC}\,f)$ | Energy per instruction with $V = V_0 + kf$ and leakage $P_s$ | [27-02](../../courses/27-system-architectures/chapters/27-02-smartphone-soc.md) |
| $2ck(V_0 + kf^*)f^{*2} = P_s$ | Energy-optimal frequency | [27-02](../../courses/27-system-architectures/chapters/27-02-smartphone-soc.md) |
| $\beta = Rw/8$ | DRAM bandwidth: transfer rate $R$, bus width $w$ bits | [27-02](../../courses/27-system-architectures/chapters/27-02-smartphone-soc.md) |
| $T_{DRAM} = \sum_k D_k(1 - h_k)$ | DRAM traffic after system-cache hit rates $h_k$ | [27-02](../../courses/27-system-architectures/chapters/27-02-smartphone-soc.md) |

## Wearables I: the smartwatch (27-03)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $L = 24\ \text{h} \times u\,\eta\,E_b/E_{day}$, $E_{day} = \sum_i P_it_i$ | Days of battery: usable fraction $u$, conversion $\eta$ | [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md) |
| $\Phi = \pi L_vA$; $P_{emit} = \pi L_vA\,\text{APL}/\eta_v$ | Lambertian emitter; display power from luminance and average pixel level | [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md) |
| $t_{hold} = C_{st}\Delta V/I_{off}$ | LTPO pixel hold time | [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md) |
| $P_{AP}(N) = f_sE_s + f_sE_w/N$; $N \le f_s\tau$ | Batching sensor samples; latency bound $\tau$ | [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md) |
| $Q_{ev} = I_{pre}t_{pre} + I_{rx}(t_{rx} + T_{IFS}) + I_{tx}t_{tx}$; $I_{avg} = I_{sl} + I_{rx}s + Q_{ev}/T$ | BLE connection-event charge and average current (window widening $s$) | [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md) |
| $V_t = V_{oc} - IR_{int}$ | Cell terminal voltage; cold brownout | [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md) |

## Wearables II: earbuds, glasses and XR (27-04)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $P_{el} = 1\ \text{mW} \times 10^{(\text{SPL} - S)/10}$ | Speaker power from loudness and sensitivity $S$ | [27-04](../../courses/27-system-architectures/chapters/27-04-wearables-earbuds-and-glasses.md) |
| $\lvert R\rvert = 2\lvert\sin(\pi f\tau)\rvert$; $\lvert R\rvert^2 = (1 - g\cos\phi)^2 + (g\sin\phi)^2$ | ANC residual with delay $\tau$ and gain $g$; amplifies above $1/(6\tau)$ | [27-04](../../courses/27-system-architectures/chapters/27-04-wearables-earbuds-and-glasses.md) |
| $n = BT_f/8$ octets; $N = \eta_tE_{case}/(2E_b)$ | LE Audio frame size; case recharges of a pair | [27-04](../../courses/27-system-architectures/chapters/27-04-wearables-earbuds-and-glasses.md) |
| $P = hA\Delta T$; $P = L_v\,\text{APL}/(\eta_{wg}\eta_{src})$ | Glasses' heat limit; waveguide display power | [27-04](../../courses/27-system-architectures/chapters/27-04-wearables-earbuds-and-glasses.md) |
| $w = x + (1 - x)s^2$, $x = (\theta_f/\theta_{FOV})^2$; $\theta_{err} = \omega\tau$ | Foveated shading work; registration error | [27-04](../../courses/27-system-architectures/chapters/27-04-wearables-earbuds-and-glasses.md) |

## The PC SoC (27-05)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\bar P_{SoC} = \sum_i r_iP_i$ | Residency-weighted power | [27-05](../../courses/27-system-architectures/chapters/27-05-pc-soc.md) |
| $t_{turbo} = \tau\ln\frac{P_2 - P_0}{P_2 - P_1}$ | Time at PL2 under an exponentially weighted PL1 limit | [27-05](../../courses/27-system-architectures/chapters/27-05-pc-soc.md) |
| $BW = wR/8$; tokens/s $\le BW/(N_pb/8)$; $t_{prefill} = 2N_pT/(\text{TOPS}\times u)$ | Decode bound ($b$ bits per parameter) and prefill time | [27-05](../../courses/27-system-architectures/chapters/27-05-pc-soc.md) |
| $C = (\sum_k C_{die,k} + C_{pkg})/Y_{asm}$ | Chiplet cost per good part (dies from 25-04) | [27-05](../../courses/27-system-architectures/chapters/27-05-pc-soc.md) |

## Automotive E/E architecture and ADAS compute (27-06)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $N_{bits}(n) = 34 + 8n + 13 + \lfloor(34 + 8n - 1)/4\rfloor$ | Worst-case classic CAN frame with stuffing | [27-06](../../courses/27-system-architectures/chapters/27-06-automotive-ee-architecture.md) |
| $R_i = B_i + C_i + \sum_{j\in hp(i)}\lceil(w_i + \tau_{bit})/T_j\rceil C_j$ | CAN response time (iterate $w_i$) | [27-06](../../courses/27-system-architectures/chapters/27-06-automotive-ee-architecture.md) |
| $R_{cam} = Pfb$; $\text{TOPS}_{peak} = N_cfG/u$ | Camera data rate; compute sizing | [27-06](../../courses/27-system-architectures/chapters/27-06-automotive-ee-architecture.md) |
| $\Delta R/R = P_c/(P_c + P_d)$, $P_d = ev$ | Range cost of compute | [27-06](../../courses/27-system-architectures/chapters/27-06-automotive-ee-architecture.md) |
| $d_{stop} = vt + v^2/(2a)$; $\lambda_{res} = \lambda(1 - DC)$ | Stopping distance with latency; residual failure rate | [27-06](../../courses/27-system-architectures/chapters/27-06-automotive-ee-architecture.md) |

## The AI datacenter server and rack (27-07)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Machine balance $= F_{peak}/B_{mem}$ | Normalize precision and sparsity first | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| $P_{in} = (\sum_k n_kP_k + P_{fans})/\eta_{conv}$; facility $= P_{in}\,\text{PUE}$ | Rack power budget | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| $C_{train} \approx 6ND$; $t = 6ND/(nF_{peak}u)$ | Training compute and time with MFU $u$ | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| $T_{ring} = 2\frac{p-1}{p}\frac{S}{B} + 2(p-1)\alpha$ | Ring all-reduce | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| $T_{hier} = 2\frac{p_1-1}{p_1}\frac{S}{B_1} + 2\frac{p_2-1}{p_2}\frac{S}{p_1B_2}$ | Hierarchical all-reduce; the network term falls by the domain size | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| $M = m/N$; $\tau^* = \sqrt{2\delta M}$; $f = \sqrt{2\delta/M} + R/M$ | Job MTBF, Young's interval, lost fraction | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| $t_{step} = \max\left(\frac{W + BK}{\eta B_{mem}}, \frac{2N_{act}B}{F}\right)$; $\Theta = \eta B_{mem}/K - (W/K)s$ | Decode step; throughput–interactivity line | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| cost/$10^6$ tokens $= \frac{K_{cap}/L + P\,\text{PUE}\cdot 8760\,c_e}{\Theta U \cdot 3.15\times 10^7/10^6}$ | Token economics | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |

## Edge AI and IoT (27-08)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\text{MACs} = HWC_{out}k^2C_{in}$; DS ratio $1/C_{out} + 1/k^2$ | Convolution and depthwise-separable cost | [27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md) |
| $t_{inf} = \text{MACs}/(muf)$; $P_{avg} = rE_{inf} + P_{fe} + P_{sleep}$ | Inference time and the always-on budget | [27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md) |
| Compute locally if $P_{local} + R_{res}e_{bit} < R_{raw}e_{bit}$ | Send the answer, not the data | [27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md) |
| $T_s = 2^{SF}/BW$; $T = (n_{pre} + 4.25)T_s + n_{pay}T_s$ | LoRa time on air (payload symbols from the SX1276 data sheet) | [27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md) |
| life $= \eta_uE_{batt}/(E_{day} + E_{sd,day})$ | Battery life with self-discharge | [27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md) |
| $P_h = (E_v/K)A\eta_{pv}\eta_c$; $C = 2E/(V_{max}^2 - V_{min}^2)$ | Indoor PV harvest; supercapacitor sizing | [27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md) |
