# Solutions 28-04 · Domain Question Banks I: Digital/CPU, AI Accelerators, Memory, Interconnect and Optics

Problems: [28-04 problems](../problems/28-04-problems.md) · Chapter: [28-04](../chapters/28-04-question-banks-digital-ai-memory-interconnect.md). Every number is recomputed by [verify_28_04.py](../verify/verify_28_04.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 28-04.1

- (a) **Evasive:** an adjective with no number. To be strong it needs the utilization, the conditions and the silicon it was measured on.
- (b) **Strong in form:** a number, the model, precision, batch, latency target, silicon stepping and date, and an honest limit with its mechanism. Reconcile it before relying on it: on Example 28-04.2's accelerator (2 PFLOP/s, 8 TB/s, FP8 weights), batch 32 caps decode at $2 \times 32 \times 8 \times 10^{12}/(2 \times 10^{15})$ = **25.6**% of peak, so 40% implies a ridge of at most $2 \times 32/0.40$ = **160** FLOP/byte, a different definition of utilization (bandwidth rather than FLOPs, or prefill included) or a different machine. Ask which; until it reconciles, a precise number that breaks the identities is a reason for doubt (§2).
- (c) **Partial:** it may become strong when the data arrive; until then it moves belief little. Ask what the number roughly is now, and record whether the follow-up arrives.
- (d) **Evasive:** an appeal to unnamed others. It becomes evidence only with a named customer, their setup and a result the buyer can confirm.

### Solution 28-04.2

Frequency ratio $1.30/1.12$ = **1.161**, a gain of **16.1**%. Power factor $1.161^3$ = **1.564**. Required reduction $1 - 1/1.564$ = **36.1**%, more than N2's reported 25–30% against N3E [R-552]: the claim needs design gains beyond any single node step, or lower power elsewhere.

### Solution 28-04.3

Per channel $6400 \times 10^6 \times 8$ bytes = **51.2** GB/s; total **614.4** GB/s. Per core: **4.80** GB/s with 128 cores and **6.40** GB/s with 96, a ratio of **1.33**. Bandwidth-hungry workloads may run faster per core on the smaller part, which is why question D5 asks for scaling curves.

### Solution 28-04.4

Ridge $5 \times 10^{15}/(8 \times 10^{12})$ = **625** FLOP/byte. With FP8 weights, $N_b = 625/2$ = **312.5**; with FP4, $N_b = 0.5 \times 625/2$ = **156.25**. At batch 16 with FP8: $32 \times 8 \times 10^{12}$ = **256** TFLOP/s, **5.12**% of peak. A larger compute array against the same memory makes decode use an even smaller share.

### Solution 28-04.5

Weights **405** GB; KV $64 \times 2$ = **128** GB; total **533** GB. Weights alone need $\lceil 405/192 \rceil$ = **3** accelerators, and so does everything, $\lceil 533/192 \rceil = 3$, leaving $576 - 533$ = **43** GB. A larger batch or longer contexts would need a fourth device, and in practice the devices must also hold activations and runtime buffers and tensor-parallel groups usually come in powers of two, so a real deployment would likely use four; question A4 asks for capacity at the buyer's context length.

### Solution 28-04.6

HBM3E: $1024 \times 9.2/8$ = **1177.6** GB/s. HBM4: $2048 \times 8/8$ = **2048** GB/s, a ratio of **1.74**. Eight HBM4 stacks at 11.7 Gb/s: $8 \times 2048 \times 11.7/8$ GB/s = **24.0** TB/s.

### Solution 28-04.7

$8 \times 10^{12} \times 8 \times 6.5 \times 10^{-12}$ = **416** W.

### Solution 28-04.8

$51.2 \times 10^{12} \times 5 \times 10^{-12}$ = **256** W in total, of which the analog part is **154** W. A pJ/bit quoted as analog only hides 40% of this power, which is why question I1 asks what the figure includes.

### Solution 28-04.9

$2 \times 10^{12} \times 8 = 1.6 \times 10^{13}$ bits/s: **4** W at 0.25 pJ/bit and **8** W at 0.5 pJ/bit. Die edge: $2000/165$ = **12.1** mm to $2000/1317$ = **1.52** mm. If 2 TB/s were needed *each way*, the edge would double, because the shoreline figures count both directions.

### Solution 28-04.10

Pluggable $64 \times 25$ = **1600** W; CPO $64 \times 5$ = **320** W. Energy per bit at 800 Gb/s: **31.25** and **6.25** pJ/bit. The laser delivers $10^{20/10}$ = **100** mW of light, needing $0.1/0.15$ = **0.667** W of electrical power at 15% wall-plug efficiency; lasers are a real part of an optical engine's budget and of its reliability.

### Solution 28-04.11

(a) Ratios 3, 0.4, 1 and 3: odds **3.6**, probability $3.6/4.6$ = **78.3**%.

(b) 95% is odds of 19. With the evasive answer, odds are $0.4 \times 3^n$: $n = 3$ gives 10.8, not enough; $n$ = **4** gives **32.4**, a probability of **97.0**%.

### Solution 28-04.12

(a) The claim needs $\text{IPC} \times f$ to rise by $R$, so $f$ rises by $R/g_{\text{IPC}}$. At fixed design, power rises by $(R/g_{\text{IPC}})^3$; the IPC changes multiply the switched capacitance by $g_C$, so the power factor is $g_C(R/g_{\text{IPC}})^3$. Holding power fixed needs the power at the new frequency (the energy per operation at the new operating point) to fall by the reciprocal factor: a reduction of $1 - 1/[g_C(R/g_{\text{IPC}})^3]$. Against the previous product, energy per operation falls only by $1 - 1/R$, since the same power buys $R$ times the work.

(b) Each decode step reads every weight once, $N_p b_w$ bytes, and performs $2N_p$ FLOP per sequence (one MAC per weight), so $2N_pN_b$ FLOP for a batch of $N_b$. The intensity is $2N_pN_b/(N_pb_w) = 2N_b/b_w$ FLOP per byte. It equals the ridge when $2N_b/b_w = F/B_{\text{mem}}$, that is $N_b = b_wF/(2B_{\text{mem}})$.

(c) Each way, $64 \times 32 \times 10^9$ bits/s ÷ 8 = **256** GB/s. Counting both directions the module carries 512 GB/s, so at 1,317 GB/s per mm its edge is $512/1317$ = **0.389** mm. A two-way bandwidth $W$ needs $W/(512\ \text{GB/s})$ modules; with $m$ modules per millimetre of edge (here $m = 1/0.389$), the edge is $W/(512m)$ mm, which is $W/1317$ mm for UCIe-A at its best. If the figure were read as one-way, every edge would be half what is needed: the direction convention is a boundary question like the power boundaries of §3.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 28-04.1a | decode cap at batch 32 | 25.6 | % |
| 28-04.1b | ridge implied by 40% | 160 | FLOP/byte |
| 28-04.2a | frequency ratio | 1.161 | — |
| 28-04.2b | frequency gain | 16.1 | % |
| 28-04.2c | power factor | 1.564 | — |
| 28-04.2d | required reduction | 36.1 | % |
| 28-04.3a | bandwidth per channel | 51.2 | GB/s |
| 28-04.3b | total bandwidth | 614.4 | GB/s |
| 28-04.3c | per core, 128 cores | 4.80 | GB/s |
| 28-04.3d | per core, 96 cores | 6.40 | GB/s |
| 28-04.3e | ratio | 1.33 | — |
| 28-04.4a | ridge point | 625 | FLOP/byte |
| 28-04.4b | batch at ridge, FP8 | 312.5 | sequences |
| 28-04.4c | batch at ridge, FP4 | 156.25 | sequences |
| 28-04.4d | attainable at batch 16 | 256 | TFLOP/s |
| 28-04.4e | share of peak | 5.12 | % |
| 28-04.5a | weight memory | 405 | GB |
| 28-04.5b | KV memory | 128 | GB |
| 28-04.5c | total | 533 | GB |
| 28-04.5d | accelerators for weights | 3 | — |
| 28-04.5e | accelerators for everything | 3 | — |
| 28-04.5f | memory left over | 43 | GB |
| 28-04.6a | HBM3E stack bandwidth | 1177.6 | GB/s |
| 28-04.6b | HBM4 stack bandwidth | 2048 | GB/s |
| 28-04.6c | ratio | 1.74 | — |
| 28-04.6d | eight HBM4 stacks at 11.7 Gb/s | 24.0 | TB/s |
| 28-04.7 | memory power | 416 | W |
| 28-04.8a | total SerDes power | 256 | W |
| 28-04.8b | analog part | 154 | W |
| 28-04.9a | link power at 0.25 pJ/bit | 4 | W |
| 28-04.9b | link power at 0.5 pJ/bit | 8 | W |
| 28-04.9c | edge at 165 GB/s/mm | 12.1 | mm |
| 28-04.9d | edge at 1317 GB/s/mm | 1.52 | mm |
| 28-04.10a | pluggable optics | 1600 | W |
| 28-04.10b | CPO optics | 320 | W |
| 28-04.10c | pluggable energy per bit | 31.25 | pJ/bit |
| 28-04.10d | CPO energy per bit | 6.25 | pJ/bit |
| 28-04.10e | 20 dBm | 100 | mW |
| 28-04.10f | laser electrical power | 0.667 | W |
| 28-04.11a | odds, repeat counted once | 3.6 | — |
| 28-04.11b | probability | 78.3 | % |
| 28-04.11c | strong answers needed | 4 | — |
| 28-04.11d | odds with four | 32.4 | — |
| 28-04.11e | probability with four | 97.0 | % |
| 28-04.12c | UCIe-A module bandwidth each way | 256 | GB/s |
| 28-04.12d | UCIe-A module edge | 0.389 | mm |
