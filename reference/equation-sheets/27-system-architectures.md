# Equation Sheet · 27 System Architectures

The relations to know cold from Course 27, each with its conditions and the chapter that derives it.

Conventions:

- powers in watts and energies in joules or watt-hours as stated; a day is 24 h and a year 8760 h (3.1536 × 10⁷ s);
- symbols follow each chapter, and a few letters change meaning between chapters (for example $b$ is bytes per parameter in 27-01 and bits in 27-05; $B$ is link bandwidth in an all-reduce and batch size in a decode step), so each row states its own;
- "assumed" parameters in the chapters are illustrative; vendor figures are dated in each chapter's §7 and §9;
- the relations are first-order models: each chapter's Common mistakes section says where they break down.

## System analysis method (27-01)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $P_{batt} = \sum_k P_k/\eta_k$; $\eta_{sys} = \sum_k P_k/P_{batt}$; LDO $\eta \le V_{out}/V_{in}$ | Converter-chain power budget | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |
| $t = E_u/\bar P_{batt}$, $\bar P_{batt} = \sum_m d_mP_{batt,m}$ | Battery life from mode duty cycles $d_m$ | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |
| $P_{sus} = (T_{s,max} - T_a)/\theta_{sa}$ | Sustained power at the skin or case limit (junction limit checked separately) | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |
| $T(t) = T_\infty - (T_\infty - T_0)e^{-t/\tau}$; $t_b = \tau\ln\frac{T_\infty - T_0}{T_\infty - T_{s,max}}$ | First-order thermal RC: $T_\infty = T_a + P_b\theta_{sa}$, $\tau = \theta_{sa}C_{th}$; a finite burst time needs $T_\infty > T_{s,max}$ | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |
| $d_{max} = \frac{P_{sus} - P_i}{P_b - P_i}$ | Burst duty that keeps the average at $P_{sus}$; valid for bursts much shorter than $\tau$ | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |
| $\text{GM} = (\text{ASP} - \text{COGS})/\text{ASP}$; $\Delta\text{GM} = -\Delta c/\text{ASP}$ | Gross margin; a unit-cost change $\Delta c$ moves it by $\Delta c/\text{ASP}$ | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |
| $\Pi_{att} = \min(\Pi, I\beta)$; ridge $I^* = \Pi/\beta$; tokens/s $\approx \beta/(N_pb)$ | Roofline; bandwidth-bound decode with $b$ **bytes** per parameter | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |
| $S = 1/\sum_k (f_k/s_k)$ | Amdahl: fractions $f_k$ of the work sped up by $s_k$ ($\sum f_k = 1$) | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |
| $L = \lambda W$; pipeline rate $r = \min_k r_k$ | Little's law (items in flight = rate × time in system); a pipeline runs at its slowest stage | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |
| $d\ln(\text{perf})/dP = 1/(3P_{dyn})$; wider core pays if $g > p^{1/3}$ | Shadow price of a watt under a power cap ($P_{dyn} \propto f^3$) | [27-01](../../courses/27-system-architectures/chapters/27-01-system-analysis-method.md) |

## Smartphone SoC (27-02)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $P = cV^2f + P_s$ | Dynamic plus static power | [27-02](../../courses/27-system-architectures/chapters/27-02-smartphone-soc.md) |
| $E_{inst}(f) = c(V_0 + kf)^2/\text{IPC} + P_s/(\text{IPC}\,f)$ | Energy per instruction with $V = V_0 + kf$ and leakage $P_s$ | [27-02](../../courses/27-system-architectures/chapters/27-02-smartphone-soc.md) |
| $2ck(V_0 + kf^*)f^{*2} = P_s$ | Energy-optimal frequency | [27-02](../../courses/27-system-architectures/chapters/27-02-smartphone-soc.md) |
| $\beta = Rw/8$ | DRAM bandwidth: transfer rate $R$, bus width $w$ bits | [27-02](../../courses/27-system-architectures/chapters/27-02-smartphone-soc.md) |
| $T_{DRAM} = \sum_k D_k(1 - h_k)$ | DRAM traffic after system-cache hit rates $h_k$ | [27-02](../../courses/27-system-architectures/chapters/27-02-smartphone-soc.md) |

## Wearables I: the smartwatch (27-03)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $L = 24\ \text{h} \times u\,\eta\,E_b/E_{day}$, $E_{day} = \sum_i P_it_i$ | Battery life in hours: usable fraction $u$, conversion $\eta$, rail energy $E_{day}$ | [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md) |
| $\Phi = \pi L_vA$; $P_{emit} = \pi L_vA\,\text{APL}/\eta_v$; $P_{drv} = P_0 + E_ff_r$ | Lambertian emitter; display emission power; driver power with refresh rate $f_r$ | [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md) |
| $t_{hold} = C_{st}\Delta V/I_{off}$ | LTPO pixel hold time | [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md) |
| $P_{AP}(N) = f_sE_s + f_sE_w/N$; $N \le f_s\tau$; $P_{hub} = P_h + f_sE_h + rE_w$ | Batching on the AP (latency bound $\tau$) against a sensor hub | [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md) |
| $t_{pkt} = 8(n_{pre} + 4 + 2 + n_{pay} + n_{MIC} + 3)/R$ | BLE packet time at PHY rate $R$ | [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md) |
| $Q_{ev} = I_{pre}t_{pre} + I_{rx}(t_{rx} + T_{IFS}) + I_{tx}t_{tx}$; $I_{avg} = I_{sl} + I_{rx}s + Q_{ev}/T$ | BLE connection-event charge and average current ($s$ = window-widening fraction) | [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md) |
| $I_{avg} = I_{sl} + Q_p/T_c$ | Cellular paging (DRX) average current | [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md) |
| $V_t = V_{oc} - IR_{int}$ | Cell terminal voltage; cold brownout | [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md) |

## Wearables II: earbuds, glasses and XR (27-04)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $P_{el} = 1\ \text{mW} \times 10^{(\text{SPL} - S)/10}$; $P_{in} = P_{el}/\eta + P_q$ | Speaker power from loudness and sensitivity $S$; class-D input power with quiescent $P_q$ | [27-04](../../courses/27-system-architectures/chapters/27-04-wearables-earbuds-and-glasses.md) |
| $\lvert R\rvert^2 = (1 - g\cos\phi)^2 + (g\sin\phi)^2$, $\phi = 2\pi f\tau$; attenuation $= -20\log_{10}\lvert R\rvert$ | ANC residual with delay $\tau$ and gain $g$; $\lvert R\rvert = 1 - g$ at $\tau = 0$ | [27-04](../../courses/27-system-architectures/chapters/27-04-wearables-earbuds-and-glasses.md) |
| $\lvert R\rvert = 2\lvert\sin(\pi f\tau)\rvert$; $\tau \le \arcsin(10^{-A/20}/2)/(\pi f)$ | Perfect gain; amplifies between $1/(6\tau)$ and $5/(6\tau)$; delay allowed for $A$ dB at $f$ | [27-04](../../courses/27-system-architectures/chapters/27-04-wearables-earbuds-and-glasses.md) |
| $n = BT_f/8$ octets; 2M packet time $8(n + 15)/2$ µs; $N = \eta_tE_{case}/(2E_b)$ | LE Audio frame and encrypted packet time; case recharges of a pair | [27-04](../../courses/27-system-architectures/chapters/27-04-wearables-earbuds-and-glasses.md) |
| $P = hA\Delta T$; $P = L_v\,\text{APL}/(\eta_{wg}\eta_{src})$ | Glasses' heat limit; waveguide display power | [27-04](../../courses/27-system-architectures/chapters/27-04-wearables-earbuds-and-glasses.md) |
| Pixel rate $2WHf_r$; $w = x + (1 - x)s^2$, $x = (\theta_f/\theta_{FOV})^2$; $\theta_{err} = \omega\tau$ | Headset pixel rate; foveated shading work; registration error | [27-04](../../courses/27-system-architectures/chapters/27-04-wearables-earbuds-and-glasses.md) |

## The PC SoC (27-05)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\bar P_{SoC} = \sum_i r_iP_i$; $L = E_b/(\bar P_{SoC} + P_{plat})$ | Residency-weighted power; life with display and platform power | [27-05](../../courses/27-system-architectures/chapters/27-05-pc-soc.md) |
| $t_{turbo} = \tau\ln\frac{P_2 - P_0}{P_2 - P_1}$ | Time at PL2 under an exponentially weighted PL1 limit | [27-05](../../courses/27-system-architectures/chapters/27-05-pc-soc.md) |
| $BW = wR/8$; tokens/s $\le BW/(N_pb/8)$; $t_{prefill} = 2N_pT/(\text{TOPS}\times u)$ | Decode bound with $b$ **bits** per parameter (27-05's convention); prefill time | [27-05](../../courses/27-system-architectures/chapters/27-05-pc-soc.md) |
| $C = (\sum_k C_{die,k} + C_{pkg})/Y_{asm}$; link power $8BE_{bit}$ | Chiplet cost per good part (tiles tested before assembly; dies from 25-04); die-to-die link power at $B$ bytes/s | [27-05](../../courses/27-system-architectures/chapters/27-05-pc-soc.md) |

## Automotive E/E architecture and ADAS compute (27-06)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $N_{bits}(n) = 34 + 8n + 13 + \lfloor(34 + 8n - 1)/4\rfloor$ | Worst-case classic CAN frame: 11-bit identifier, $n$ data bytes, 3-bit interframe space included | [27-06](../../courses/27-system-architectures/chapters/27-06-automotive-ee-architecture.md) |
| $U = \sum_i C_i/T_i$; $R_i = B_i + C_i + \sum_{j\in hp(i)}\lceil(w_i + \tau_{bit})/T_j\rceil C_j$ | Bus load; response time ($C$ frame time, $T$ period, $B_i$ longest lower-priority frame, $\tau_{bit}$ bit time; iterate $w_i$) | [27-06](../../courses/27-system-architectures/chapters/27-06-automotive-ee-architecture.md) |
| $R_{cam} = Pfb$; $\text{TOPS}_{peak} = N_cfG/u$ | Camera data rate; compute sizing | [27-06](../../courses/27-system-architectures/chapters/27-06-automotive-ee-architecture.md) |
| $\Delta R/R = P_c/(P_c + P_d)$, $P_d = ev$ | Range cost of compute | [27-06](../../courses/27-system-architectures/chapters/27-06-automotive-ee-architecture.md) |
| $d_{stop} = vt + v^2/(2a)$; $\lambda_{res} = \lambda(1 - DC)$ | Stopping distance with latency; residual failure rate | [27-06](../../courses/27-system-architectures/chapters/27-06-automotive-ee-architecture.md) |

## The AI datacenter server and rack (27-07)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Machine balance $= F_{peak}/B_{mem}$ | Normalize precision and sparsity first | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| $P_{in} = (\sum_k n_kP_k + P_{fans})/\eta_{conv}$; facility $= P_{in}\,\text{PUE}$ | Rack power budget | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| $C_{train} \approx 6ND$; $t = 6ND/(nF_{peak}u)$; $E = nP_{acc}k_{sys}\,\text{PUE}\,t$ | Training compute, time with MFU $u$, and energy over elapsed time | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| $T_{ring} = 2\frac{p-1}{p}\frac{S}{B} + 2(p-1)\alpha$ | Ring all-reduce; $B$ = link bandwidth per direction | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| $T_{hier} = 2\frac{p_1-1}{p_1}\frac{S}{B_1} + 2\frac{p_2-1}{p_2}\frac{S}{p_1B_2}$ | Hierarchical all-reduce, $p = p_1p_2$, ignoring latency | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| $M = m/N$; $\tau^* = \sqrt{2\delta M}$; $f = \sqrt{2\delta/M} + R/M$ | Job MTBF, Young's interval, lost fraction; $\delta \ll \tau \ll M$, $R$ = restart time | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| $t_{step} = \max\left(\frac{W + BK}{\eta B_{mem}}, \frac{2N_{act}B}{F}\right)$ | Decode step; here $B$ = batch, $W$ weight bytes, $K$ KV bytes per sequence | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| $\Theta = B/t_{step}$; $s = 1/t_{step}$; $\Theta = \eta B_{mem}/K - (W/K)s$; $B_{max} = \lfloor(C - W)/K\rfloor$ | Throughput, per-user speed, the memory-bound frontier, HBM capacity limit; energy per token $P_{rack}/\Theta$ | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| cost/$10^6$ tokens $= \frac{K_{cap}/L + P\,\text{PUE}\cdot 8760\,c_e}{\Theta U \cdot 3.1536\times 10^7/10^6}$ | Token economics: $P$ in kW, $c_e$ in $/kWh, $U$ utilization, $3.1536 \times 10^7$ s per year | [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |

## Edge AI and IoT (27-08)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\text{MACs} = HWC_{out}k^2C_{in}$; DS ratio $1/C_{out} + 1/k^2$ | Convolution and depthwise-separable cost | [27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md) |
| $t_{inf} = \text{MACs}/(muf)$; $P_{avg} = rE_{inf} + P_{fe} + P_{sleep}$ | Inference time and the always-on budget | [27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md) |
| Compute locally if $P_{local} + R_{res}e_{bit} < R_{raw}e_{bit}$ | Send the answer, not the data | [27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md) |
| $T_s = 2^{SF}/BW$; $T = (n_{pre} + 4.25)T_s + n_{pay}T_s$ | LoRa time on air | [27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md) |
| $n_{pay} = 8 + \max\left(\left\lceil\frac{8PL - 4SF + 28 + 16CRC - 20IH}{4(SF - 2DE)}\right\rceil(CR + 4), 0\right)$ | Payload symbols (SX1276 data sheet); $CR = 1$ for 4/5, $DE = 1$ when $T_s > 16$ ms | [27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md) |
| $E_{day} = NE_{msg} + P_{sleep}\cdot 86\,400$ s; life $= \eta_uE_{batt}/(E_{day} + E_{sd,day})$ | Daily energy and battery life with self-discharge | [27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md) |
| $P_h = (E_v/K)A\eta_{pv}\eta_c$; $C = 2E/(V_{max}^2 - V_{min}^2)$ | Indoor PV harvest; supercapacitor sizing | [27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md) |
