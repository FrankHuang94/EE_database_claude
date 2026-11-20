# Equation Sheet · 14 Computer Organization and Architecture

The relations to know cold from Course 14, each with its conditions and the chapter that derives it.

Conventions:

- times in seconds or cycles, rates in operations per second;
- 1 KiB = 1024 bytes for memory sizes, 1 GB/s = 10⁹ bytes/s for bandwidths;
- RISC-V RV32I unless stated.

## Performance and power

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $T = \text{IC} \times \text{CPI} / f$ (the iron law) | Instruction count, cycles per instruction, clock frequency | [14-01](../../courses/14-computer-organization-and-architecture/chapters/14-01-performance-power-iron-law.md) |
| Amdahl: $S = 1/\bigl((1-p) + p/N\bigr)$, limit $1/(1-p)$ | Fixed problem size; fraction $p$ parallel on $N$ units | [14-01](../../courses/14-computer-organization-and-architecture/chapters/14-01-performance-power-iron-law.md) |
| Gustafson: $S = (1-p) + pN$ | Problem grows with $N$ | [14-01](../../courses/14-computer-organization-and-architecture/chapters/14-01-performance-power-iron-law.md) |
| $P_\text{dyn} = \alpha C V^2 f$; energy per operation $\propto CV^2$ | Switching activity $\alpha$ | [14-01](../../courses/14-computer-organization-and-architecture/chapters/14-01-performance-power-iron-law.md) |

## ISA, assembly and numbers

| Relation | Conditions / notes | Chapter |
|---|---|---|
| R/I/S/B/U/J formats: opcode [6:0], rd [11:7], funct3 [14:12], rs1 [19:15], rs2 [24:20]; immediate sign in bit 31 | RV32I | [14-02](../../courses/14-computer-organization-and-architecture/chapters/14-02-isa-risc-v-arm-x86.md) |
| Branches reach ±4 KiB (13-bit even offset); jal ±1 MiB; constants: `lui` upper 20 bits + `addi` lower 12 (add 1 to the upper part if bit 11 is set) |  | [14-02](../../courses/14-computer-organization-and-architecture/chapters/14-02-isa-risc-v-arm-x86.md) |
| Callee-saved: s0–s11, sp; caller-saved: t0–t6, a0–a7, ra; sp 16-byte aligned | RISC-V psABI | [14-03](../../courses/14-computer-organization-and-architecture/chapters/14-03-assembly-and-the-compilation-stack.md) |
| $n$-bit two's complement: $-2^{n-1} \ldots 2^{n-1}-1$; overflow when operands of one sign give a result of the other | | [14-04](../../courses/14-computer-organization-and-architecture/chapters/14-04-computer-arithmetic-and-number-formats.md) |
| FP32 $= (-1)^s\,1.f \times 2^{e-127}$; spacing above 1 is $2^{-23}$; round to nearest even; bfloat16 = top 16 bits of FP32 | Normal numbers | [14-04](../../courses/14-computer-organization-and-architecture/chapters/14-04-computer-arithmetic-and-number-formats.md) |
| Symmetric quantization: $s = \max|x|/(2^{b-1}-1)$, $q = \text{round}(x/s)$, error ≤ $s/2$; SQNR ≈ $6.02b + 1.76$ dB | Full-scale sinusoid for the SQNR rule | [14-14](../../courses/14-computer-organization-and-architecture/chapters/14-14-ai-accelerators.md) |

## Datapaths, pipelines and prediction

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Single-cycle clock = slowest instruction's path (usually the load) | | [14-05](../../courses/14-computer-organization-and-architecture/chapters/14-05-single-cycle-datapath.md) |
| Pipeline clock = slowest stage + register overhead; ideal speedup → number of stages | Balanced stages, no hazards | [14-06](../../courses/14-computer-organization-and-architecture/chapters/14-06-pipelining-and-hazards.md) |
| Five-stage cycles $= N + 4 + S + 2T$ | $S$ load-use stalls, $T$ taken branches resolved in EX | [14-06](../../courses/14-computer-organization-and-architecture/chapters/14-06-pipelining-and-hazards.md) |
| CPI = base + (branch fraction) × (misprediction rate) × penalty; added CPI = MPKI/1000 × penalty | | [14-07](../../courses/14-computer-organization-and-architecture/chapters/14-07-branch-prediction-and-speculation.md) |
| 2-bit counter: predict taken in states 2–3; one anomaly flips no prediction | | [14-07](../../courses/14-computer-organization-and-architecture/chapters/14-07-branch-prediction-and-speculation.md) |

## Out-of-order execution

| Relation | Conditions / notes | Chapter |
|---|---|---|
| RAW true; WAR and WAW name dependences, removed by renaming | | [14-08](../../courses/14-computer-organization-and-architecture/chapters/14-08-out-of-order-and-superscalar.md) |
| Dataflow limit: cycles ≥ critical path; IPC ≤ $N$/critical path | Unlimited resources, perfect prediction | [14-08](../../courses/14-computer-organization-and-architecture/chapters/14-08-out-of-order-and-superscalar.md) |
| Little's law: occupancy = throughput × time in system; window ≈ width × latency to hide | Steady state | [14-08](../../courses/14-computer-organization-and-architecture/chapters/14-08-out-of-order-and-superscalar.md) |

## Caches and memory

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Sets $S = C/(B \cdot A)$; offset $\log_2 B$, index $\log_2 S$, tag = rest | Capacity $C$, block $B$, ways $A$ | [14-09](../../courses/14-computer-organization-and-architecture/chapters/14-09-memory-hierarchy-and-caches.md) |
| AMAT $= t_1 + m_1(t_2 + m_{2,\text{local}} t_\text{mem})$; global L2 rate = $m_1 m_{2,\text{local}}$ | | [14-09](../../courses/14-computer-organization-and-architecture/chapters/14-09-memory-hierarchy-and-caches.md) |
| MPKI = 1000 × accesses/instruction × miss rate; ΔCPI = accesses/instruction × $m$ × penalty | In-order, blocking cache | [14-09](../../courses/14-computer-organization-and-architecture/chapters/14-09-memory-hierarchy-and-caches.md) |
| Three Cs: compulsory (first touch), capacity (fully associative LRU also misses), conflict (the rest) | Conflict can be negative (LRU is not optimal) | [14-09](../../courses/14-computer-organization-and-architecture/chapters/14-09-memory-hierarchy-and-caches.md) |
| Bandwidth = outstanding misses × block / latency | Little's law | [14-09](../../courses/14-computer-organization-and-architecture/chapters/14-09-memory-hierarchy-and-caches.md) |
| HBM per stack = pin rate × width / 8 (1024 bits HBM3/3E, 2048 HBM4) | | [14-09](../../courses/14-computer-organization-and-architecture/chapters/14-09-memory-hierarchy-and-caches.md) |

## Virtual memory and traps

| Relation | Conditions / notes | Chapter |
|---|---|---|
| PA = PPN(VPN) × page size + offset | | [14-10](../../courses/14-computer-organization-and-architecture/chapters/14-10-virtual-memory.md) |
| Sv32: VPN[1] = bits 31–22, VPN[0] = 21–12, offset 11–0; 2 levels of 1024 4-byte PTEs; 4 MiB megapages | | [14-10](../../courses/14-computer-organization-and-architecture/chapters/14-10-virtual-memory.md) |
| TLB reach = entries × page size; translation overhead = $m_\text{TLB}$ × walk cost | | [14-10](../../courses/14-computer-organization-and-architecture/chapters/14-10-virtual-memory.md) |
| VIPT without aliasing: cache size / associativity ≤ page size | | [14-10](../../courses/14-computer-organization-and-architecture/chapters/14-10-virtual-memory.md) |
| Cause codes: 8 ecall from U; 12/13/15 instruction/load/store page fault; interrupt bit set for 5/7 S/M timer, 9/11 S/M external; vectored pc = BASE + 4 × cause | RISC-V privileged | [14-10](../../courses/14-computer-organization-and-architecture/chapters/14-10-virtual-memory.md) |

## I/O, multicore and consistency

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Polling cost = polls/s × cycles/poll; interrupt cost = events/s × cycles/interrupt | | [14-11](../../courses/14-computer-organization-and-architecture/chapters/14-11-io-buses-and-interconnect.md) |
| Link bandwidth per direction = GT/s × lanes × encoding efficiency / 8 (8b/10b: 0.8; 128b/130b: 0.985) | Before Flit/FEC overhead (PCIe 6+) | [14-11](../../courses/14-computer-organization-and-architecture/chapters/14-11-io-buses-and-interconnect.md) |
| Mesh $k \times k$: average hops $2(k^2-1)/(3k)$; bisection $k$ links per direction | Uniform traffic | [14-11](../../courses/14-computer-organization-and-architecture/chapters/14-11-io-buses-and-interconnect.md) |
| MESI: read miss BusRd (E if alone, else S); write in S BusUpgr; write miss BusRdX; E → M silently | | [14-12](../../courses/14-computer-organization-and-architecture/chapters/14-12-multicore-coherence-consistency.md) |
| Full-map directory overhead ≈ $N/(8B)$ of data | $N$ cores, $B$-byte blocks | [14-12](../../courses/14-computer-organization-and-architecture/chapters/14-12-multicore-coherence-consistency.md) |
| SB litmus test: SC 3 outcomes, TSO 4 (adds 0, 0); a fence between store and load restores SC | | [14-12](../../courses/14-computer-organization-and-architecture/chapters/14-12-multicore-coherence-consistency.md) |

## GPUs, accelerators and the roofline

| Relation | Conditions / notes | Chapter |
|---|---|---|
| SIMD efficiency = useful lane-slots / (32 × issue slots); divergent branches cost the sum of paths | 32-thread warps | [14-13](../../courses/14-computer-organization-and-architecture/chapters/14-13-gpus-and-simt.md) |
| Sectors per warp = min(32, 4 × stride) for 4-byte elements; bank-conflict degree = gcd(stride, 32) | 32-byte sectors, 32 banks | [14-13](../../courses/14-computer-organization-and-architecture/chapters/14-13-gpus-and-simt.md) |
| Warps to hide latency $\ge 1 + L/k$ | $k$ instructions between waits | [14-13](../../courses/14-computer-organization-and-architecture/chapters/14-13-gpus-and-simt.md) |
| Systolic latency $T = K + M + N - 2$; utilization $MKN/(P^2 T)$ | Output-stationary $P \times P$ array | [14-14](../../courses/14-computer-organization-and-architecture/chapters/14-14-ai-accelerators.md) |
| Reuse needed so movement ≤ MAC energy: $R \ge 2E_\text{fetch}/E_\text{MAC}$ | Two 1-byte operands | [14-14](../../courses/14-computer-organization-and-architecture/chapters/14-14-ai-accelerators.md) |
| Roofline: attainable = min(peak, bandwidth × intensity); ridge = peak / bandwidth | Intensity in FLOP per byte of memory traffic | [14-15](../../courses/14-computer-organization-and-architecture/chapters/14-15-roofline-and-benchmarks.md) |
| SPEC ratio = reference time / measured time (× copies); score = geometric mean; harmonic mean for rates over equal work | | [14-15](../../courses/14-computer-organization-and-architecture/chapters/14-15-roofline-and-benchmarks.md) |
