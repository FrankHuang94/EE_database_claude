# Equation Sheet · 23 Memory and Storage Technology

The relations to know cold from Course 23, each with its conditions and the chapter that derives it.

Conventions:

- bandwidths and capacities are decimal (1 GB = 10⁹ bytes) unless written GiB or KiB; a MAC counts as two operations;
- $E_b$ is energy per bit, $BW$ a bandwidth in bytes per second, and the factor 8 converts bytes to bits;
- in DRAM, $C_s$ is the cell and $C_{BL}$ the bitline capacitance; in flash, $C_{CG}$ is the control-gate coupling and $C_T$ the storage node's total capacitance;
- $Q(x)$ is the Gaussian tail probability; $H(p)$ is the binary entropy in bits;
- symbols reused between chapters: $\alpha$ is the physical-to-user capacity ratio (23-07) or the gate coupling ratio $\alpha_G$ (23-06); $\Delta$ is MRAM's thermal stability factor (23-08); $\tau$ is a latch, channel or thermal time constant, by context; $A$ is write amplification (23-07) or an area; $k$ is a margin in standard deviations or Boltzmann's constant, by context.

## The memory wall

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $E_{wire} = \tfrac14CV^2$ per random bit; $C \approx 0.2$ fF/µm on chip | Full-swing CMOS wire, $p_{01} = 1/4$ | [23-01](../../courses/23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md) |
| $P = 8\,BW\,E_b$; $BW_{max} = P_{budget}/(8E_b)$ | Energy per bit caps bandwidth | [23-01](../../courses/23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md) |
| $BW = N_{pins}R_{pin}/8$ | Peak, before protocol overhead | [23-01](../../courses/23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md) |
| Bytes in flight $= BW \times$ latency | Little's law | [23-01](../../courses/23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md) |
| Ridge point $= \text{FLOPS}/BW$ | Below it a kernel is memory-bound | [23-01](../../courses/23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md) |
| KV bytes per token $= 2 \times L \times n_{kv} \times d \times b$ | Layers, KV heads, head dimension, bytes per entry | [23-01](../../courses/23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md) |
| Decode rate $\le BW/\text{bytes per step}$ | Memory-bound token generation | [23-01](../../courses/23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md) |

## SRAM

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Array efficiency $=$ macro density $\times$ cell area | Periphery overhead | [23-02](../../courses/23-memory-and-storage-technology/chapters/23-02-sram-technology.md) |
| New die area $= s + (1 - s)/x$ | SRAM share $s$ does not shrink; logic shrinks $x$ times | [23-02](../../courses/23-memory-and-storage-technology/chapters/23-02-sram-technology.md) |
| $Q(k) = -\ln Y/N$ | Margin $k\sigma$ for yield $Y$ over $N$ cells without repair | [23-02](../../courses/23-memory-and-storage-technology/chapters/23-02-sram-technology.md) |
| $\sigma_{V_T} = A_{VT}/\sqrt{WL}$ | Pelgrom mismatch | [23-02](../../courses/23-memory-and-storage-technology/chapters/23-02-sram-technology.md) |
| Area per bit $= A_{cell} + A_{col}/N_{BL} + A_{other}$ | Longer bitlines amortize periphery but slow reads | [23-02](../../courses/23-memory-and-storage-technology/chapters/23-02-sram-technology.md) |

## DRAM

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\Delta V = (V_{cell} - V_{pre})\,C_s/(C_s + C_{BL})$ | Charge sharing on a precharged bitline | [23-03](../../courses/23-memory-and-storage-technology/chapters/23-03-dram-cells-arrays-refresh.md) |
| $C_{BL} \le C_s(V_{sig}/\Delta V_{min} - 1)$ | Longest bitline the sense amplifier tolerates | [23-03](../../courses/23-memory-and-storage-technology/chapters/23-03-dram-cells-arrays-refresh.md) |
| $t = \tau\ln(V_{final}/\Delta V_0)$, $\tau = C/g_m$ | Latch regeneration | [23-03](../../courses/23-memory-and-storage-technology/chapters/23-03-dram-cells-arrays-refresh.md) |
| Hit $t_{CL}$; miss $t_{RCD} + t_{CL}$; conflict $t_{RP} + t_{RCD} + t_{CL}$ | Row-buffer outcomes | [23-03](../../courses/23-memory-and-storage-technology/chapters/23-03-dram-cells-arrays-refresh.md) |
| Refresh overhead $= t_{RFC}/t_{REFI}$ | Device busy refreshing | [23-03](../../courses/23-memory-and-storage-technology/chapters/23-03-dram-cells-arrays-refresh.md) |
| $E_{sense} = N_{BL}C_{BL}V^2/2$ per row | Bitline pairs swing apart from $V/2$ | [23-03](../../courses/23-memory-and-storage-technology/chapters/23-03-dram-cells-arrays-refresh.md) |
| PARA: $P(\text{miss}) = (1 - p/2)^N$ | Neighbour refreshed with probability $p$ per activation | [23-03](../../courses/23-memory-and-storage-technology/chapters/23-03-dram-cells-arrays-refresh.md) |

## DRAM interfaces

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Bytes per access $= W \times BL/8$; core rate $=$ data rate$/n_{prefetch}$ | Burst length sets access granularity | [23-04](../../courses/23-memory-and-storage-technology/chapters/23-04-dram-interfaces.md) |
| POD: $I = V_{DDQ}/(R_{on} + R_{TT})$ while low; LVSTL: same while high | Static termination current | [23-04](../../courses/23-memory-and-storage-technology/chapters/23-04-dram-interfaces.md) |
| $\Gamma = (R - Z_0)/(R + Z_0)$; launched $V_sZ_0/(R_s + Z_0)$ | Reflections, lattice diagram | [23-04](../../courses/23-memory-and-storage-technology/chapters/23-04-dram-interfaces.md) |
| $h_0 = 1 - a$, $h_k = (1 - a)a^k$, $a = e^{-UI/\tau}$; eye $= h_0 - \sum_{k \ge 1}h_k$ | First-order channel; DFE removes the taps it cancels | [23-04](../../courses/23-memory-and-storage-technology/chapters/23-04-dram-interfaces.md) |
| PAM-M penalty $= 20\log_{10}(M - 1)$ dB; symbol rate $=$ bit rate$/\log_2M$ | Same swing | [23-04](../../courses/23-memory-and-storage-technology/chapters/23-04-dram-interfaces.md) |

## HBM

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $B = WR/8$; capacity $= N_{layers} \times$ die density$/8$ | Per stack | [23-05](../../courses/23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md) |
| $E = \tfrac14CV^2$ per bit | Short unterminated link, random data | [23-05](../../courses/23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md) |
| $C_{TSV} = 2\pi\varepsilon L/\ln(b/a)$; $R = \rho L/(\pi a^2)$ | Coaxial liner capacitance | [23-05](../../courses/23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md) |
| $\Delta T_{base} = R_L[NP_b + P_cN(N - 1)/2]$ | Heat leaves through the top | [23-05](../../courses/23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md) |
| Stack yield $= (y_{bond}y_{die})^N$ | Known-good dies | [23-05](../../courses/23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md) |
| Gross dies $= \pi d^2/(4A) - \pi d/\sqrt{2A}$ | Dies or interposers per wafer | [23-05](../../courses/23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md) |

## NAND flash

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\Delta V_T = -Q/C_{CG}$; $q/C_{CG}$ per electron | Stored charge | [23-06](../../courses/23-memory-and-storage-technology/chapters/23-06-nand-flash-and-3d-nand.md) |
| $V_{FG} = \alpha_GV_{CG} + Q/C_T$, $\alpha_G = C_{CG}/C_T$ | Coupling ratio | [23-06](../../courses/23-memory-and-storage-technology/chapters/23-06-nand-flash-and-3d-nand.md) |
| $J = AE^2e^{-B/E}$ | Fowler–Nordheim tunneling | [23-06](../../courses/23-memory-and-storage-technology/chapters/23-06-nand-flash-and-3d-nand.md) |
| ISPP: $\Delta V_T = \Delta V_{pgm}$ per pulse | Steady state, independent of cell parameters | [23-06](../../courses/23-memory-and-storage-technology/chapters/23-06-nand-flash-and-3d-nand.md) |
| $d = W/(2^n - 1)$; $\text{RBER} = \dfrac{2(L - 1)}{Ln}Q\!\left(\dfrac{d}{2\sigma}\right)$ | $L = 2^n$ Gaussian levels, Gray coding | [23-06](../../courses/23-memory-and-storage-technology/chapters/23-06-nand-flash-and-3d-nand.md) |
| $AF = \exp[(E_a/k)(1/T_u - 1/T_s)]$ | Arrhenius retention acceleration | [23-06](../../courses/23-memory-and-storage-technology/chapters/23-06-nand-flash-and-3d-nand.md) |
| Die throughput $=$ page × planes$/t_{PROG}$ | Writes are the bottleneck | [23-06](../../courses/23-memory-and-storage-technology/chapters/23-06-nand-flash-and-3d-nand.md) |

## SSD controllers

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $S_{map} = (C/IU) \times e$ | Page-mapped FTL; 4 KiB and 4 B give $C/1024$ | [23-07](../../courses/23-memory-and-storage-technology/chapters/23-07-ssd-controllers.md) |
| $u = e^{-\alpha(1 - u)}$, $A = 1/(1 - u) = \alpha/(\alpha + W(-\alpha e^{-\alpha}))$ | FIFO cleaning, uniform random writes, $\alpha = 1 + OP$ | [23-07](../../courses/23-memory-and-storage-technology/chapters/23-07-ssd-controllers.md) |
| $TBW = T N_{PE}/A$; $DWPD = TBW/(U \times 365 \times \text{years})$ | Raw capacity $T$, user capacity $U$ | [23-07](../../courses/23-memory-and-storage-technology/chapters/23-07-ssd-controllers.md) |
| $P_{fail} = P(X > t)$, $X \sim \text{Bin}(n, p)$; BCH parity $\le mt$ | Hard-decision code over GF($2^m$) | [23-07](../../courses/23-memory-and-storage-technology/chapters/23-07-ssd-controllers.md) |
| $C = 1 - H(p)$ ≥ code rate | Binary symmetric channel; limit for hard decisions | [23-07](../../courses/23-memory-and-storage-technology/chapters/23-07-ssd-controllers.md) |
| $N = XR$ | Little's law: commands in flight = IOPS × latency | [23-07](../../courses/23-memory-and-storage-technology/chapters/23-07-ssd-controllers.md) |
| $C = 2Pt_h/[\eta(V_1^2 - V_2^2)]$ | Power-loss-protection hold-up | [23-07](../../courses/23-memory-and-storage-technology/chapters/23-07-ssd-controllers.md) |

## Emerging memories

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\text{TMR} = (R_{AP} - R_P)/R_P$ | Read contrast shrinks with series resistance | [23-08](../../courses/23-memory-and-storage-technology/chapters/23-08-emerging-memories.md) |
| $r = f_0e^{-\Delta}$, $\Delta = E_b/k_BT$; $\Delta \ge \ln(Ntf_0)$ | At most one flip in $N$ bits over $t$ | [23-08](../../courses/23-memory-and-storage-technology/chapters/23-08-emerging-memories.md) |
| $I_{c0} \propto \Delta$; $E = VIt$ | STT write cost rises with stability | [23-08](../../courses/23-memory-and-storage-technology/chapters/23-08-emerging-memories.md) |
| $\Delta T = PR_{th}(1 - e^{-t/\tau})$, $\tau = R_{th}C_{th}$; quench $\tau\ln(\Delta T_m/\Delta T_x)$ | PCM thermal RC | [23-08](../../courses/23-memory-and-storage-technology/chapters/23-08-emerging-memories.md) |
| $R(t) = R(t_0)(t/t_0)^\nu$ | PCM drift | [23-08](../../courses/23-memory-and-storage-technology/chapters/23-08-emerging-memories.md) |
| $G_0 = 2e^2/h \approx 77.5$ µS | ReRAM filament conductance quantum | [23-08](../../courses/23-memory-and-storage-technology/chapters/23-08-emerging-memories.md) |
| $Q = 2P_rA$; FeFET window $\approx 2E_ct_{FE}$ | Ferroelectric switching | [23-08](../../courses/23-memory-and-storage-technology/chapters/23-08-emerging-memories.md) |

## Compute-in-memory

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $I_j = \sum_iV_iG_{ij}$; signed $w$: $G^\pm = g\max(\pm w, 0) + G_{min}$ | Virtual-ground columns | [23-09](../../courses/23-memory-and-storage-technology/chapters/23-09-compute-in-memory.md) |
| $\text{SNR}_a = 1/\sigma^2$; ENOB $= (\text{SNR}_{dB} - 1.76)/6.02$ | Zero-mean products, independent relative errors | [23-09](../../courses/23-memory-and-storage-technology/chapters/23-09-compute-in-memory.md) |
| $B = \log_2[M(2^{b_x} - 1)(2^{b_w} - 1) + 1]$ | Exact column-sum resolution | [23-09](../../courses/23-memory-and-storage-technology/chapters/23-09-compute-in-memory.md) |
| $E_{ADC/MAC} = \text{FoM}_W2^Bb_xb_w/M$; TOPS/W $= 2/E_{MAC}$ | Bit-serial inputs, bit-sliced weights | [23-09](../../courses/23-memory-and-storage-technology/chapters/23-09-compute-in-memory.md) |
| speedup $= 1/[(1 - f) + f/S]$ | Amdahl's law | [23-09](../../courses/23-memory-and-storage-technology/chapters/23-09-compute-in-memory.md) |
| Throughput $=$ ops per PE × PEs × utilization | Sze et al. | [23-09](../../courses/23-memory-and-storage-technology/chapters/23-09-compute-in-memory.md) |
