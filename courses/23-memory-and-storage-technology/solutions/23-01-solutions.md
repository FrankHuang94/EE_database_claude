# Solutions 23-01 · The Memory Hierarchy and the Memory Wall

Problems: [23-01 problems](../problems/23-01-problems.md) · Chapter: [23-01](../chapters/23-01-memory-hierarchy-and-memory-wall.md)

Every number is recomputed by [verify_23_01.py](../verify/verify_23_01.py).

---

## Solutions

### Solution 23-01.1

(a) 640/5 = **128**; (b) 640/0.1 = **6400**.

(c) 1 GB is $10^9/4$ words of 4 bytes, so $(10^9/4) \times 640$ pJ = **0.16** J. That is the energy of reading a modest model's weights once, at 45 nm, before counting any arithmetic.

### Solution 23-01.2

(a) $P = 8\,BW\,E_b = 8 \times 4 \times 10^{12} \times 5 \times 10^{-12}$ = **160** W.

(b) $8 \times 100 \times 10^9 \times 5 \times 10^{-12}$ = **4.0** J; (c) $100\ \text{GB}/4\ \text{TB/s}$ = **25** ms. Check: 160 W × 25 ms = 4 J. ✓

### Solution 23-01.3

$BW = Nr/8$: (a) $384 \times 28 \times 10^9/8$ = **1.344** TB/s; (b) $1024 \times 8 \times 10^9/8$ = **1.024** TB/s. The narrow, fast interface and the wide, slow one deliver about the same bandwidth; they differ in energy per bit and reach.

(c) $N = 8\,BW/r = 8 \times 10^{12}/(32 \times 10^9)$ = **250** pins.

### Solution 23-01.4

(a) $D = BW \times t = 10^{12} \times 400 \times 10^{-9}$ = **400** KB; (b) 400 KB/64 B = **6250** requests.

(c) With at most 2,048 requests in flight, $BW = 2048 \times 64\ \text{B}/400\ \text{ns}$ = **327.7** GB/s, a third of the stack's capability. The controller's request tracking, not the DRAM, would set the bandwidth.

### Solution 23-01.5

(a) $C = 0.18\ \text{fF/µm} \times 2000\ \mu\text{m}$ = **360** fF; (b) $CV^2 = 360\ \text{fF} \times 0.64\ \text{V}^2$ = **230.4** fJ.

Only 0 → 1 transitions draw from the supply, so $E_b = p_{01}CV^2$: (c) random data, $p_{01}$ = 1/4: **57.6** fJ; (d) alternating data, $p_{01}$ = 1/2: **115.2** fJ; (e) $p_{01}$ = 0.2: **46.1** fJ.

Alternating data is the worst case: every other bit charges the wire. Coding that cuts transitions saves energy in proportion.

### Solution 23-01.6

(a) $1.6\ \text{nJ}/8192$ = **0.195** pJ per bit; (b) $1.6\ \text{nJ}/512$ = **3.125** pJ per bit; (c) **16** times.

(d) $1.6\ \text{nJ}/(0.5\ \text{pJ} \times 8)$ = **400** bytes per activation. Access patterns that use only a 64-byte line per row opened pay the activation energy many times over. This is the energy argument for row-buffer locality and for the fine-grained activation that FGDRAM proposed [chapter source 3].

### Solution 23-01.7

The ridge grows by a factor $3.0/1.6$ every two years.

(a) Doubling time: $2\ln 2/\ln 1.875$ = **2.21** years.

(b) Bandwidth must grow as fast as compute: **3.0** times every two years.

(c) After ten years the ridge is $(3.0/1.6)^5$ times higher, so a kernel of fixed intensity reaches $(1.6/3.0)^5$ = **4.32** % of peak. Workloads must keep raising their reuse just to stand still.

### Solution 23-01.8

At batch 1 each token reads every weight once, so tokens per second ≤ $BW/W$:

(a) $3.35 \times 10^{12}/(14 \times 10^9)$ = **239** tokens/s; (b) **479**; (c) **957**. Halving the bytes per weight doubles the bound: quantization is a bandwidth multiplier.

### Solution 23-01.9

(a) $k = 2Ln_{kv}d_hb_{kv} = 2 \times 32 \times 8 \times 128 \times 2$ = **131 072** B per token.

(b) $131\,072 \times 131\,072$ = **17.18** GB for one sequence, more than the model's own 14 GB of BF16 weights.

(c) With 32 KV heads, four times as much: **68.72** GB. Grouped-query attention's 4:1 sharing is what makes long contexts fit at all.

### Solution 23-01.10

(a) $131\,072 \times 32\,768$ = **4.295** GB per sequence.

(b) $(80 - 14)\ \text{GB}/4.295\ \text{GB}$, rounded down: **15** sequences.

(c) $14 + 15 \times 4.295$ = **78.42** GB; (d) $78.42\ \text{GB}/3.35\ \text{TB/s}$ = **23.41** ms; (e) $15/23.41\ \text{ms}$ = **641** tokens/s.

The KV caches are over four fifths of the traffic, so a faster GPU with the same memory would barely help; more memory capacity and bandwidth would.

### Solution 23-01.11

**Monotonic.** $I(B) = BF_1/(W + BK)$. Its derivative is

$$
\frac{dI}{dB} = \frac{F_1(W + BK) - BF_1K}{(W + BK)^2} = \frac{F_1W}{(W + BK)^2} > 0 ,
$$

so $I$ rises with $B$. As $B \to \infty$, $I \to BF_1/(BK) = F_1/K$.

(a) Setting $I(B) = F_1/(2K)$: $2BK = W + BK$, so

$$
B_{1/2} = \frac{W}{K} .
$$

That is the batch at which the KV caches read per step equal the weights read per step. Beyond it, extra sequences add mostly KV traffic, and batching buys little more intensity.

(b) For Example 23-01.7, $W$ = 70 GB and $K$ = 5.369 GB, so $B_{1/2}$ = **13.0**. The 40-sequence batch is already well past it.

### Solution 23-01.12

(a) $5\ \text{pJ}/32$ = **0.15625** pJ per bit.

(b) $8 \times 40 \times 10^9 \times 0.15625 \times 10^{-12}$ = **0.05** J per token from SRAM; (c) $8 \times 40 \times 10^9 \times 6.86 \times 10^{-12}$ = **2.20** J from HBM; (d) a ratio of **43.9**.

(e) Reasons the real gap is smaller:

- the 5 pJ figure is for a small 8 KB array, while tens of gigabytes of SRAM spread over a wafer mean long wires from the arrays to the compute;
- an SRAM-only design holds only as much model as it has SRAM, so larger models stream weights from external memory or across chips;
- SRAM leaks, and its static power is paid whether or not the bits are read.

The real gap is still large, which is why SRAM-centric accelerators can win on latency and energy per token for models that fit.

### Solution 23-01.13

(a) $E_b \le P/(8\,BW) = 300/(8 \times 20 \times 10^{12})$ = **1.875** pJ/bit.

(b) $6.86/1.875$ = **3.66** times better than the H200's all-in figure. That is close to FGDRAM's 2 pJ/bit research target [chapter source 3]: it needs both lower internal data-movement energy and lower background power.

(c) Stacks: $8 \times 20 \times 10^{12}/(2048 \times 10 \times 10^9)$, rounded up: **8** stacks.

### Solution 23-01.14

(a) $12 \times 24 \times 64\ \text{B}/90\ \text{ns}$ = **204.8** GB/s.

(b) The cores could sustain more than the DRAM delivers, so the DRAM's **160** GB/s binds: the system is bandwidth-bound.

(c) One core alone reaches only $24 \times 64\ \text{B}/90\ \text{ns}$ = **17.1** GB/s. With few active cores, the per-core concurrency limit binds first.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 23-01.1a | DRAM / SRAM read ratio | 128 | |
| 23-01.1b | DRAM read / integer add ratio | 6400 | |
| 23-01.1c | energy to read 1 GB from DRAM | 0.16 | J |
| 23-01.2a | memory power | 160 | W |
| 23-01.2b | energy to read 100 GB | 4.0 | J |
| 23-01.2c | time to read 100 GB | 25 | ms |
| 23-01.3a | 384-bit at 28 Gb/s | 1.344 | TB/s |
| 23-01.3b | 1,024-bit at 8 Gb/s | 1.024 | TB/s |
| 23-01.3c | pins at 32 Gb/s for 1 TB/s | 250 | |
| 23-01.4a | data in flight | 400 | KB |
| 23-01.4b | requests in flight | 6250 | |
| 23-01.4c | bandwidth with 2,048 requests | 327.7 | GB/s |
| 23-01.5a | capacitance | 360 | fF |
| 23-01.5b | supply energy per transition | 230.4 | fJ |
| 23-01.5c | energy per bit, random data | 57.6 | fJ |
| 23-01.5d | energy per bit, alternating data | 115.2 | fJ |
| 23-01.5e | energy per bit, bus-inverted | 46.1 | fJ |
| 23-01.6a | activation energy per bit, whole row | 0.195 | pJ |
| 23-01.6b | activation energy per bit, 64 bytes | 3.125 | pJ |
| 23-01.6c | ratio | 16 | |
| 23-01.6d | bytes per activation for 0.5 pJ/bit | 400 | B |
| 23-01.7a | ridge doubling time | 2.21 | years |
| 23-01.7b | bandwidth growth to hold the ridge | 3.0 | |
| 23-01.7c | fraction of peak after ten years | 4.32 | % |
| 23-01.8a | tokens/s, BF16 | 239 | |
| 23-01.8b | tokens/s, FP8 | 479 | |
| 23-01.8c | tokens/s, 4-bit | 957 | |
| 23-01.9a | KV bytes per token | 131072 | B |
| 23-01.9b | KV cache per 131,072-token sequence | 17.18 | GB |
| 23-01.9c | same with 32 KV heads | 68.72 | GB |
| 23-01.10a | KV cache per 32,768-token sequence | 4.295 | GB |
| 23-01.10b | largest batch | 15 | |
| 23-01.10c | bytes per step | 78.42 | GB |
| 23-01.10d | memory time per step | 23.41 | ms |
| 23-01.10e | tokens per second | 641 | |
| 23-01.11b | half-limit batch for Example 23-01.7 | 13.0 | |
| 23-01.12a | SRAM energy per bit | 0.15625 | pJ |
| 23-01.12b | weight-read energy per token, SRAM | 0.05 | J |
| 23-01.12c | weight-read energy per token, HBM | 2.20 | J |
| 23-01.12d | HBM-to-SRAM ratio | 43.9 | |
| 23-01.13a | largest all-in energy per bit | 1.875 | pJ |
| 23-01.13b | improvement over H200 | 3.66 | |
| 23-01.13c | stacks needed | 8 | |
| 23-01.14a | core-sustainable bandwidth | 204.8 | GB/s |
| 23-01.14b | binding limit (DRAM bandwidth) | 160 | GB/s |
| 23-01.14c | one core's bandwidth | 17.1 | GB/s |
