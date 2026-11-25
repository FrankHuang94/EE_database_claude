# Course 23 · Final Exam Solutions

Exam: [README.md](README.md). Every number below is recomputed by [verify_23_exam.py](../verify/verify_23_exam.py). About half the values are recomputed by a second route, listed below; the rest are closed-form re-evaluations of the same formulas:

- Question 2(c): the margin by root finding on the array yield $(1 - Q(k))^N$ itself;
- Question 3(a) and 11(a): the charge-sharing signal from conservation of charge solved as a linear system;
- Question 4(c): the far-end voltages by summing a lattice diagram; 4(d): the cursors by integrating the channel's step response;
- Question 5(c): the stack's temperatures by solving the thermal ladder's nodal equations;
- Questions 6(c), 8(a) and 8(b): tail probabilities by direct summation and root finding;
- Questions 7(b), 7(c) and 11(c): the fixed point by iteration, checked against Lambert W;
- Question 8(c): the hold-up capacitance by integrating the bank's discharge;
- Question 9(c): the PCM pulse by integrating the thermal ODE;
- Questions 10(a) and 10(d): the crossbar by per-cell summation, the Amdahl fraction by root finding.

---

## Solutions

### Solution 1

(a) $80/(5.5 \times 10^{-12} \times 8)$ = **1.82** TB/s. At 6 TB/s, $6 \times 10^{12} \times 8 \times 5.5 \times 10^{-12}$ = **264** W. Energy per bit, not pin count, caps bandwidth (23-01).

(b) $1024 \times 8\ \text{Gb/s}/8$ = **1024** GB/s per stack; six stacks give **6.14** TB/s.

(c) Little's law: $6 \times 10^{12} \times 500 \times 10^{-9}$ = **3.0** MB in flight, or $3.0\ \text{MB}/64\ \text{B}$ = **46875** requests.

(d) $3 \times 10^{15}/6 \times 10^{12}$ = **500** FLOP/B. A kernel at 2 FLOP/B is memory-bound and can use at most $2/500$ = **0.4** % of peak compute.

### Solution 2

(a) $1/0.024\ \mu\text{m}^2$ = **41.7** × 10⁶ bits/mm², so the efficiency is $30/41.67$ = **72.0** %.

(b) $0.35 + 0.65/1.5$ = **78.3** % of the old die; the SRAM share becomes $0.35/0.7833$ = **44.7** %; the effective shrink is $1/0.7833$ = **1.28** times, against 1.5 for logic.

(c) The yield is $(1 - Q(k))^{N} \approx e^{-NQ(k)}$, so $Q(k) = -\ln 0.99/2^{25} = 3.00 \times 10^{-10}$, and $k$ = **6.19**.

(d) $2^{27} \times 4\ \text{pA}$ = **0.537** mA, and × 0.75 V = **0.403** mW. Dropping 300 mV cuts leakage by $2^{-3}$ = **0.125**, so the retention power is $0.537\ \text{mA} \times 0.125 \times 0.45$ = **0.0302** mW, **13.3** times lower.

### Solution 3

(a) $\Delta V = (1.1 - 0.55) \times 6/(6 + 36)$ = **78.6** mV.

(b) $C_{BL} \le 6\,(0.45/0.07 - 1)$ = **32.6** fF, so $N \le (32.57 - 3)/0.07$ = **422** cells. A power-of-two array uses **256**, since 512 exceeds the limit.

(c) $410/7812.5$ = **5.25** %; $410/3906.25$ = **10.5** %.

(d) $0.8\ \text{s} \times 2^{-4}$ = **50** ms at 85 °C, which **fails** the 64 ms window. At 95 °C, $0.8 \times 2^{-5}$ = **25** ms, which **fails** the 32 ms window. The cell must be remapped or refreshed more often.

### Solution 4

(a) $16 \times 16/8$ = **32** bytes per access; $8.0 \times 10^9 \times 16/8$ = **16** GB/s.

(b) $I = 1.1/(40 + 48)$ = **12.5** mA; $V_{low} = 1.1 - 12.5\ \text{mA} \times 48$ = **0.5** V; power while low $1.1 \times 12.5\ \text{mA}$ = **13.75** mW. At 8 Gb/s with half the bits low, $13.75\ \text{mW}/8 \times 10^9 \times 0.5$ = **0.859** pJ/bit.

(c) $\Gamma_L = (60 - 40)/(60 + 40)$ = **0.2**; $\Gamma_S = (30 - 40)/(30 + 40)$ = **−0.143**. The launched wave is $1 \times 40/70$ = **0.571** V. First arrival: $0.5714 \times 1.2$ = **0.686** V. Second: $0.6857 + 0.5714 \times 0.2 \times (-0.1429) \times 1.2$ = **0.666** V. Final: $60/90$ = **0.667** V.

(d) $a = e^{-1/0.8}$ = **0.287**; $h_0 = 1 - a$ = **0.713**; $h_1 = (1 - a)a$ = **0.204**. The post-cursors sum to $a$, so the NRZ eye is $h_0 - a$ = **0.427** of the swing. Removing $h_1$ leaves $h_0 - (a - h_1)$ = **0.631**.

### Solution 5

(a) $2048 \times 10 \times 10^9/8$ = **2.56** TB/s; eight stacks **20.48** TB/s; $12 \times 24/8$ = **36** GB.

(b) $\tfrac14 \times 0.8\ \text{pF} \times 0.4^2$ = **0.032** pJ/bit; $2048 \times 10^{10} \times 0.032\ \text{pJ}$ = **0.655** W.

(c) $\Delta T = R_L[NP_b + P_cN(N - 1)/2] = 0.03 \times (16 \times 12 + 1.2 \times 120)$ = **10.1** K.

(d) $0.995^{16}$ = **92.3** %; $0.9^{1/16}$ = **99.34** % per layer.

### Solution 6

(a) $q/18\ \text{aF}$ = **8.90** mV per electron; QLC spacing $5.8/15$ = **0.387** V, or $0.3867/8.901\ \text{mV}$ = **43.4** electrons.

(b) $(4.2 + 1.8)/0.2$ = **30** pulses; $30 \times 22$ = **660** µs.

(c) $k = 0.3867/0.14$ = **2.76**; RBER $= \tfrac{2 \times 15}{16 \times 4}Q(2.762)$ = **1.35** × 10⁻³.

(d) $AF = \exp[(1.0/8.617 \times 10^{-5})(1/313.15 - 1/398.15)]$ = **2728**; one year (8,766 h) is $8766/2728$ = **3.21** h.

### Solution 7

(a) $15.36 \times 10^{12}/4096 \times 4$ = **15.0** GB; with 16 KiB units **3.75** GB.

(b) At α = 1.12, iterating $u = e^{-1.12(1 - u)}$ gives $u$ = **0.794** and $A$ = **4.85**. At α = 1.25, $A$ = **2.69**.

(c) $OP = 17.2/15.36 - 1$ = **11.98** %; $A$ = **4.85**; $TBW = 17.2 \times 3000/4.853$ = **10632** TB; $DWPD = 10632/(15.36 \times 1825)$ = **0.379**.

(d) $3.2 \times 10^6 \times 90\ \mu\text{s}$ = **288** commands; $3.2 \times 10^6 \times 4096$ = **13.1** GB/s; $1/90\ \mu\text{s}$ = **11111** IOPS.

### Solution 8

(a) Parity $13 \times 48$ = **624** bits; $n = 8192 + 624$ = **8816**; mean $8816 \times 0.002$ = **17.6**. The binomial tail $P(X > 48)$ = **6.16** × 10⁻¹⁰. (A Poisson approximation with λ = 17.6 gives **6.51** × 10⁻¹⁰, close enough for a design decision.)

(b) Rate $16/18.5$ = **0.865**; $1 - H(0.01)$ = **0.919**; solving $1 - H(p) = 0.865$ gives $p$ = **1.89** %.

(c) $25 \times 0.03/0.9$ = **0.833** J; $C = 2 \times 0.8333/(36^2 - 12^2)$ = **1.45** mF.

(d) Rereading at shifted references tells the decoder which bits are unreliable; LDPC decoding uses that soft information to correct far more errors than a hard decoder at the same code rate (and, information-theoretically, raises the channel's capacity). The cost is latency: each soft level adds reads and decoding, so a worn drive's tail latency grows.

### Solution 9

(a) $R_{AP} = 5 \times 2.2$ = **11** kΩ; $I_P = 0.12/7.5\ \text{k}\Omega$ = **16.0** µA; $I_{AP} = 0.12/13.5\ \text{k}\Omega$ = **8.89** µA; contrast $16/8.889 - 1$ = **80** %.

(b) $\Delta = \ln(2^{27} \times 3.156 \times 10^8 \times 10^9)$ = **59.0**; at 25 °C it must be $59.0 \times 378.15/298.15$ = **74.8**.

(c) $(250\ \mu\text{A})^2 \times 1.6\ \text{k}\Omega$ = **100** µW; $R_{th} = 620/100\ \mu\text{W}$ = **6.2** K/µW; $100\ \mu\text{W} \times 40\ \text{ns}$ = **4.0** pJ; $1.5 \ln(620/140)$ = **2.23** ns.

(d) $(3.156 \times 10^7)^{0.08}$ = **3.98**; $1.5^{1/0.08}$ = **159** s.

### Solution 10

(a) $G^+$ columns: (16.5, 0.5, 8.5) and (0.5, 24.5, 8.5) µS; $G^-$: (0.5, 8.5, 0.5) and (8.5, 0.5, 0.5) µS. Currents: $I_1^+$ = **1.75** µA, $I_1^-$ = **1.35** µA, $I_2^+$ = **4.55** µA, $I_2^-$ = **0.55** µA. Outputs: **0.40** µA and **4.00** µA. Exact products: $0.5 \times 2 - 1.5 + 1$ = **0.5** and $-0.5 + 4.5 + 1$ = **5**; at 0.8 µA per unit, 0.4 and 4.0 µA. ✓

(b) $10\log_{10}(1/0.03^2)$ = **30.5** dB; ENOB $= (30.46 - 1.76)/6.02$ = **4.77** bits.

(c) $3\ \text{fJ} \times 2^8 \times 16/256$ = **48** fJ per MAC; $2/48\ \text{fJ}$ = **41.7** TOPS/W.

(d) $1/(0.3 + 0.7/6)$ = **2.40**; for 2.5×, $f = (1 - 1/2.5)/(1 - 1/6)$ = **0.72**.

### Solution 11

(a) Before the wordline opens, the cell holds $C_sV_{cell}$ and the bitline $C_{BL}V_{pre}$. Charge is conserved when they connect, and they settle to a common $V$:

$$
C_sV_{cell} + C_{BL}V_{pre} = (C_s + C_{BL})V \;\Longrightarrow\; \Delta V = V - V_{pre} = (V_{cell} - V_{pre})\frac{C_s}{C_s + C_{BL}} .
$$

Transfer ratio $7/42$ = **0.167**; signal $0.525 \times 0.1667$ = **87.5** mV.

(b) During pulse $k$, $V_{FG} = \alpha_GV_{pgm,k} + Q_k/C_T$ with $\alpha_G = C_{CG}/C_T$. If every pulse ends at the same $V_{FG}^*$, equating pulses $k$ and $k + 1$ gives $Q_{k+1} - Q_k = -\alpha_GC_T\Delta V_{pgm} = -C_{CG}\Delta V_{pgm}$, so $\Delta V_T = -\Delta Q/C_{CG} = \Delta V_{pgm}$. Electrons per pulse: $18\ \text{aF} \times 0.25/q$ = **28.1**.

(c) A page written at the log's head survives until the log wraps: all $T$ physical pages are written once, of which $(1 - u)T$ are host writes. Each overwrites the page's LBA with probability $1/U$, so the page survives with probability $(1 - 1/U)^{(1 - u)T} \approx e^{-\alpha(1 - u)}$, which is the victim's valid fraction $u$. Cleaning a victim frees $(1 - u)$ of a block for host data while the flash writes the whole block, so $A = 1/(1 - u)$. At α = 1.2: $u$ = **0.686**, $A$ = **3.19**; check $e^{-1.2 \times 0.3137}$ = **0.686**. ✓

(d) $y = \sum_i p_i(1 + \epsilon_i)$ has error $e = \sum_ip_i\epsilon_i$ with variance $\sigma^2\sum_ip_i^2$. For zero-mean uncorrelated $p_i$, $E[y^2] = \sum_iE[p_i^2]$, so $\text{SNR} = 1/\sigma^2$ = **28.0** dB. For equal positive $p_i = p$, the signal is $M^2p^2$ and the error variance $M\sigma^2p^2$, so $\text{SNR} = M/\sigma^2$ = **49.0** dB.

### Solution 12

(a) $8 \times 614$ = **4.91** TB/s; the model is $70 \times 10^9 \times 0.5$ B = **35** GB; $4.912\ \text{TB/s}/35\ \text{GB}$ = **140** tokens/s. With ordinary LPDDR5X: $8 \times 76.8/35$ = **17.6** tokens/s.

(b) $1/(0.2 + 0.8/8)$ = **3.33**; $17.55 \times 3.333$ = **58.5** tokens/s. The "140" is the bandwidth bound with every phase accelerated; Amdahl's law gives less than half of it.

(c) $2 \times 80 \times 8 \times 128 \times 1$ = **163840** B per token; × 32,768 = **5.37** GB per sequence; $(128 - 35)/5.369$ = 17.3, so **17** sequences.

(d) $8\ \text{TB/s}/35\ \text{GB}$ = **229** tokens/s, **3.91** times the realistic PIM figure. Questions, with strong answers:

1. *"What fraction of decode time does PIM accelerate on this model, measured?"* Strong: a profile split by phase (weights, attention, sampling) with the accelerated share.
2. *"What precision does the PIM logic support, and what accuracy do you get at 4-bit weights?"* Strong: named formats and accuracy on standard benchmarks.
3. *"How does throughput scale with batch and context length, given 128 GB?"* Strong: measured tokens per second at batches up to the 17 sequences of (c), and KV-cache handling.
4. *"What software and model coverage exist?"* Strong: a compiler or runtime with named models, and which operators fall back to the host.

Rubric: (a)–(c) 3 points each for the numbers; (d) 1 point for the numbers and 2 for at least three well-posed questions with strong answers.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| X23.1a | bandwidth at 80 W | 1.82 | TB/s |
| X23.1a1 | power at 6 TB/s | 264 | W |
| X23.1b | bandwidth per stack | 1024 | GB/s |
| X23.1b1 | total bandwidth | 6.14 | TB/s |
| X23.1c | data in flight | 3.0 | MB |
| X23.1c1 | requests in flight | 46875 | |
| X23.1d | ridge point | 500 | FLOP/B |
| X23.1d1 | usable share of peak | 0.4 | % |
| X23.2a | raw bitcell density | 41.7 | Mb/mm² |
| X23.2a1 | array efficiency | 72.0 | % |
| X23.2a2 | raw density, 4 s.f. | 41.67 | Mb/mm² |
| X23.2b | new die area | 78.3 | % |
| X23.2b1 | SRAM share | 44.7 | % |
| X23.2b2 | effective shrink | 1.28 | |
| X23.2b3 | new die area, 4 s.f. | 0.7833 | |
| X23.2c0 | target tail probability | 3.00e-10 | |
| X23.2c | margin | 6.19 | |
| X23.2d | leakage current | 0.537 | mA |
| X23.2d1 | leakage power | 0.403 | mW |
| X23.2d2 | leakage factor | 0.125 | |
| X23.2d3 | retention power | 0.0302 | mW |
| X23.2d4 | power ratio | 13.3 | |
| X23.3a | signal | 78.6 | mV |
| X23.3b | largest bitline capacitance | 32.6 | fF |
| X23.3b1 | largest bitline capacitance, 4 s.f. | 32.57 | fF |
| X23.3b2 | largest cell count | 422 | |
| X23.3b3 | power-of-two choice | 256 | |
| X23.3c | refresh overhead at 7.8125 µs | 5.25 | % |
| X23.3c1 | refresh overhead at 3.90625 µs | 10.5 | % |
| X23.3d | retention at 85 °C | 50 | ms |
| X23.3d1 | retention at 95 °C | 25 | ms |
| X23.4a | bytes per access | 32 | B |
| X23.4a1 | channel bandwidth | 16 | GB/s |
| X23.4b | POD current | 12.5 | mA |
| X23.4b1 | low voltage | 0.5 | V |
| X23.4b2 | power while low | 13.75 | mW |
| X23.4b3 | energy per bit | 0.859 | pJ |
| X23.4c | load reflection coefficient | 0.2 | |
| X23.4c1 | source reflection coefficient | -0.143 | |
| X23.4c2 | launched voltage | 0.571 | V |
| X23.4c3 | first arrival | 0.686 | V |
| X23.4c4 | second arrival | 0.666 | V |
| X23.4c5 | final value | 0.667 | V |
| X23.4c6 | launched voltage, 4 s.f. | 0.5714 | V |
| X23.4c7 | first arrival, 4 s.f. | 0.6857 | V |
| X23.4c8 | source coefficient, 4 s.f. | -0.1429 | |
| X23.4d | a | 0.287 | |
| X23.4d1 | main cursor | 0.713 | |
| X23.4d2 | first post-cursor | 0.204 | |
| X23.4d3 | NRZ eye | 0.427 | |
| X23.4d4 | eye with one-tap DFE | 0.631 | |
| X23.5a | stack bandwidth | 2.56 | TB/s |
| X23.5a1 | eight stacks | 20.48 | TB/s |
| X23.5a2 | stack capacity | 36 | GB |
| X23.5b | energy per bit | 0.032 | pJ |
| X23.5b1 | interface power | 0.655 | W |
| X23.5c | base-die rise | 10.1 | K |
| X23.5d | stack yield | 92.3 | % |
| X23.5d1 | per-layer yield for 90% | 99.34 | % |
| X23.6a | shift per electron | 8.90 | mV |
| X23.6a1 | QLC spacing | 0.387 | V |
| X23.6a2 | electrons per level | 43.4 | |
| X23.6a3 | QLC spacing, 4 s.f. | 0.3867 | V |
| X23.6a4 | shift per electron, 4 s.f. | 8.901 | mV |
| X23.6b | pulses | 30 | |
| X23.6b1 | program time | 660 | µs |
| X23.6c | margin | 2.76 | |
| X23.6c1 | margin, 4 s.f. | 2.762 | |
| X23.6c2 | RBER | 1.35e-3 | |
| X23.6d | acceleration factor | 2728 | |
| X23.6d1 | bake time | 3.21 | h |
| X23.6d2 | hours in a year | 8766 | h |
| X23.7a | mapping table, 4 KiB | 15.0 | GB |
| X23.7a1 | mapping table, 16 KiB | 3.75 | GB |
| X23.7b | valid fraction at 12% OP | 0.794 | |
| X23.7b1 | write amplification at 12% OP | 4.85 | |
| X23.7b2 | write amplification at 25% OP | 2.69 | |
| X23.7c | OP | 11.98 | % |
| X23.7c1 | write amplification | 4.85 | |
| X23.7c2 | TBW | 10632 | TB |
| X23.7c3 | DWPD | 0.379 | |
| X23.7c4 | write amplification, 4 s.f. | 4.853 | |
| X23.7d | commands in flight | 288 | |
| X23.7d1 | data rate | 13.1 | GB/s |
| X23.7d2 | IOPS at queue depth 1 | 11111 | |
| X23.8a | parity bits | 624 | |
| X23.8a1 | codeword length | 8816 | |
| X23.8a2 | mean errors | 17.6 | |
| X23.8a3 | failure probability | 6.16e-10 | |
| X23.8a4 | Poisson approximation | 6.51e-10 | |
| X23.8b | code rate | 0.865 | |
| X23.8b1 | capacity at 1% | 0.919 | |
| X23.8b2 | hard-decision limit | 1.89 | % |
| X23.8c | energy from the bank | 0.833 | J |
| X23.8c1 | capacitance | 1.45 | mF |
| X23.8c2 | energy, 4 s.f. | 0.8333 | J |
| X23.9a | antiparallel resistance | 11 | kΩ |
| X23.9a1 | parallel current | 16.0 | µA |
| X23.9a2 | antiparallel current | 8.89 | µA |
| X23.9a3 | contrast | 80 | % |
| X23.9a4 | antiparallel current, 4 s.f. | 8.889 | µA |
| X23.9b | required Delta | 59.0 | |
| X23.9b1 | 25 °C Delta for 105 °C | 74.8 | |
| X23.9c | RESET power | 100 | µW |
| X23.9c1 | thermal resistance | 6.2 | K/µW |
| X23.9c2 | RESET energy | 4.0 | pJ |
| X23.9c3 | quench time | 2.23 | ns |
| X23.9d | one-year drift factor | 3.98 | |
| X23.9d1 | time to drift 1.5x | 159 | s |
| X23.10a | I1+ | 1.75 | µA |
| X23.10a1 | I1- | 1.35 | µA |
| X23.10a2 | I2+ | 4.55 | µA |
| X23.10a3 | I2- | 0.55 | µA |
| X23.10a4 | output 1 | 0.40 | µA |
| X23.10a5 | output 2 | 4.00 | µA |
| X23.10a6 | exact product 1 | 0.5 | |
| X23.10a7 | exact product 2 | 5 | |
| X23.10a8 | current per unit product | 0.8 | µA |
| X23.10b | compute SNR | 30.5 | dB |
| X23.10b1 | effective bits | 4.77 | bits |
| X23.10b2 | compute SNR, 4 s.f. | 30.46 | dB |
| X23.10c | ADC energy per MAC | 48 | fJ |
| X23.10c1 | TOPS/W ceiling | 41.7 | TOPS/W |
| X23.10d | speedup | 2.40 | |
| X23.10d1 | fraction for 2.5x | 0.72 | |
| X23.11a | transfer ratio | 0.167 | |
| X23.11a1 | signal | 87.5 | mV |
| X23.11b | electrons per pulse | 28.1 | |
| X23.11c | valid fraction | 0.686 | |
| X23.11c1 | write amplification | 3.19 | |
| X23.11c2 | fixed-point check | 0.686 | |
| X23.11c3 | 1 - u | 0.3137 | |
| X23.11d | SNR, zero-mean | 28.0 | dB |
| X23.11d1 | SNR, equal positive | 49.0 | dB |
| X23.12a | card bandwidth | 4.91 | TB/s |
| X23.12a1 | model size | 35 | GB |
| X23.12a2 | PIM bound | 140 | tokens/s |
| X23.12a3 | LPDDR5X bound | 17.6 | tokens/s |
| X23.12a4 | LPDDR5X bound, 4 s.f. | 17.55 | tokens/s |
| X23.12b | realistic speedup | 3.33 | |
| X23.12b1 | realistic tokens per second | 58.5 | tokens/s |
| X23.12c | KV bytes per token | 163840 | B |
| X23.12c1 | cache per sequence | 5.37 | GB |
| X23.12c2 | sequences | 17 | |
| X23.12c3 | cache per sequence, 4 s.f. | 5.369 | GB |
| X23.12d | HBM GPU bound | 229 | tokens/s |
| X23.12d1 | ratio to realistic PIM | 3.91 | |
