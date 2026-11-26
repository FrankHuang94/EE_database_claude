# Solutions 28-02 · Validating Claims: TOPS/W, Benchmarks, Tapeout Status

Problems: [28-02 problems](../problems/28-02-problems.md) · Chapter: [28-02](../chapters/28-02-validating-claims.md). Every number is recomputed by [verify_28_02.py](../verify/verify_28_02.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 28-02.1

$N_{\text{MAC}} = 128 \times 128 = 16\,384$. Dense INT8: $2 \times 16\,384 \times 0.94 \times 10^9$ = **30.8** TOPS. INT4 alone: **61.6** TOPS. INT4 with 2:4 sparsity: **123** TOPS, the headline. At 40% utilization, dense INT8 delivers **12.3** TOPS, a tenth of the headline.

### Solution 28-02.2

$E_{\text{op}} = 1/(\eta \times 10^{12})$ J. At 10 TOPS/W: **100** fJ per operation, **0.2** pJ per MAC. At 2.5 TOPS/W: **400** fJ, **0.8** pJ per MAC. At 50 TOPS/W: **20** fJ, **0.04** pJ per MAC.

### Solution 28-02.3

Ridge point $200 \times 10^{12}/3.2 \times 10^{12}$ = **62.5** operations per byte. At 40 operations per byte: $40 \times 3.2 \times 10^{12}$ = **128** TOPS, **64**% utilization. At 10: **32** TOPS, **16**%. Both are memory-bound; the peak is reached only above 62.5.

### Solution 28-02.4

$E_{\text{op}} \ge 0.05 + 0.6/10 + 31.2/500 = 0.05 + 0.06 + 0.0624$ = **0.172** pJ, so the efficiency is at most $1/0.1724$ = **5.80** TOPS/W. Shares: arithmetic **29.0**%, SRAM **34.8**%, HBM **36.2**%. Data movement takes **71.0**% of the energy even with good reuse, which is why architectures compete on dataflow rather than on multipliers.

### Solution 28-02.5

$30 \times (0.55/0.85)^2$ = **12.6** TOPS/W. The peak-throughput point is less than half as efficient as the quoted figure.

### Solution 28-02.6

$(4.0 + 1.2 + 0.3)/0.85$ = **6.47** W at the battery, so $26/6.47$ = **4.02** TOPS/W, against the **10.0** TOPS/W measured on the NPU rail. For battery life (27-03), the module figure is the one that matters.

### Solution 28-02.7

(a) $2 \times 500 \times 16$ = **16000**, over 4800. (b) $2 \times 300 \times 8$ = **4800**, exactly at the threshold (the rule's own example). (c) $16\,000/800$ = **20.0** per mm², above 5.92. Both parts fall within ECCN 3A090's scope by TPP [R-659]; whether a license is needed for a given destination is a legal question, but the screening is arithmetic.

### Solution 28-02.8

Against R: A's speedups are $10/5 = 2$ and $10/20 = 0.5$, arithmetic **1.25**, geometric **1.00**; B's are $10/8 = 1.25$ twice, arithmetic **1.25**, geometric **1.25**. Against R′: A's are $5/5 = 1$ and $20/20 = 1$, arithmetic **1.00**, geometric **1.00**; B's are $5/8 = 0.625$ and $20/8 = 2.5$, arithmetic **1.5625**, geometric **1.25**. Against R″: A's are $20/5 = 4$ and $1/20 = 0.05$, arithmetic **2.025**, geometric **0.447**; B's are $20/8 = 2.5$ and $1/8 = 0.125$, arithmetic **1.3125**, geometric **0.559**.

The arithmetic mean calls A and B equal against R, puts B ahead against R′ (1.5625 against 1.00) and puts *A* ahead against R″: the ranking reverses with the reference. The geometric mean puts B ahead of A by a factor of 1.25 against every reference, because the reference times cancel in the ratio.

### Solution 28-02.9

$\operatorname{E}[Z_{(5)}]$ = **1.163**, so the best of five is $1.3\,e^{0.25 \times 1.163}$ = **1.74**×. $\operatorname{E}[Z_{(20)}]$ = **1.867**, so the best of twenty is **2.07**×. The more workloads tested, the higher the best case, though slowly.

### Solution 28-02.10

(a) A **closed-division server (or interactive) scenario** result, which measures throughput under a latency bound with Poisson arrivals, at the stated latency target; cost per token then needs the system's price and power. An offline result would not support it.

(b) An **open-division** result compares a different model with the reference; it shows what the vendor's own model achieves, not that its hardware is faster. The claim needs a closed-division comparison on the same model, and the open result must be labeled "MLPerf Open" [R-224].

(c) **Offline** throughput allows arbitrary batching, so it says nothing about a 30 ms per-frame deadline. The camera claim needs a **single-stream** (or multistream) latency result, whose percentile latency must fall within 30 ms.

### Solution 28-02.11

$70 \times 1.2$ = 84 days = **12.0** weeks; $70 \times 1.5$ = 105 days = **15.0** weeks.

### Solution 28-02.12

(a) First silicon and bring-up: $2.5 + 14 + 3 + 10 = 29.5$ weeks. Qualification: $1000/168 + 2 = 7.95$ weeks. Metal-only respin: $1 + 5 + 3 = 9$ weeks, total **46.5** weeks, **10.7** months. Full respin: $2.5 + 14 + 3 = 19.5$ weeks, total **57.0** weeks, **13.1** months.

(b) Expected $0.6 \times 46.5 + 0.4 \times 57.0$ = **50.7** weeks, **11.6** months. Twelve months is **52.2** weeks, so the plan holds only if the metal-only fix works: probability **0.6**. The plan is credible only with a full-respin branch and a statement of which bugs a metal fix cannot reach.

### Solution 28-02.13

Efficiency $1000/75$ = **13.3** TOPS/W, plausible at the chip boundary. Batch-1 decode reads all 7 GB of weights per token, so $200 \times 10^9/7 \times 10^9$ = **28.6** tokens/s. The claim is $4000/28.6$ = **140** times that: it can only be an aggregate across about 140 concurrent sequences (with their KV caches also read each step), or the weights must sit on chip, which 7 GB cannot. Ask: at what batch, what per-user speed and what latency, and how much memory holds the weights and caches?

### Solution 28-02.14

(a) With $P = \alpha CV^2f$ and operations per second $F = kf$, the energy per operation is $P/F = \alpha CV^2/k$, independent of $f$. The efficiency $\eta = F/P$ is its inverse, so $\eta_2/\eta_1 = (V_1/V_2)^2$. From 0.60 V to 0.90 V the efficiency falls by $(0.90/0.60)^2$ = **2.25** times.

(b) With $r_{A,i} = t_{R,i}/t_{A,i}$, $\text{GM}(r_A)/\text{GM}(r_B) = \left[\prod_i (t_{R,i}/t_{A,i})/(t_{R,i}/t_{B,i})\right]^{1/n} = \left[\prod_i t_{B,i}/t_{A,i}\right]^{1/n}$, in which $t_{R,i}$ has canceled.

(c) Require $E_\ell/I_\ell \le \beta E_{\text{op}}$, so $I_\ell \ge E_\ell/(\beta E_{\text{op}})$. With DRAM's 160 pJ per byte, $\beta = 0.1$ and $E_{\text{op}} = 10$ fJ, $I \ge 160{,}000$ operations per byte (Example 28-02.2).

### Solution 28-02.15

- (a) **Proves** that the design functions on real silicon, at small sample size. **Leaves open** yield, cost, volume and the product's own masks and lot (the shuttle's masks are shared). **Ask:** "How many dies did you test, at which corners, and when do dedicated masks tape out?"
- (b) **Proves** that the dedicated first silicon powers up and that enough logic works to run software. **Leaves open** the validation plan: corners, temperatures, analog and I/O blocks, power and performance at the target clock. **Ask:** "What fraction of the validation plan has passed, and what bugs are open?"
- (c) **Proves** two mask revisions: B0 changed the base layers (a full respin, repeating the fab cycle) and A1, by the usual naming, changed only metal. The ordering in the claim is muddled (A1 precedes B0), which is itself a question. **Leaves open** whether B0 has been validated as fully as A0 and whether more fixes are pending. **Ask:** "Which stepping will ship, and what does its errata list contain?"
- (d) **Proves**, if true, that the part passed stress tests to some standard. **Leaves open** which standard, grade and conditions. **Ask:** "Qualified to which standard and revision (JESD47 or AEC-Q100 grade), on which stepping, how many lots and units, and with how many failures?"

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 28-02.1a | dense INT8 peak | 30.8 | TOPS |
| 28-02.1b | INT4 peak | 61.6 | TOPS |
| 28-02.1c | INT4 with sparsity | 123 | TOPS |
| 28-02.1d | delivered at 40% | 12.3 | TOPS |
| 28-02.2a | energy per op at 10 TOPS/W | 100 | fJ |
| 28-02.2b | energy per MAC at 10 TOPS/W | 0.2 | pJ |
| 28-02.2c | energy per op at 2.5 TOPS/W | 400 | fJ |
| 28-02.2d | energy per MAC at 2.5 TOPS/W | 0.8 | pJ |
| 28-02.2e | energy per op at 50 TOPS/W | 20 | fJ |
| 28-02.2f | energy per MAC at 50 TOPS/W | 0.04 | pJ |
| 28-02.3a | ridge point | 62.5 | ops/byte |
| 28-02.3b | attainable at 40 ops/byte | 128 | TOPS |
| 28-02.3c | utilization at 40 ops/byte | 64 | % |
| 28-02.3d | attainable at 10 ops/byte | 32 | TOPS |
| 28-02.3e | utilization at 10 ops/byte | 16 | % |
| 28-02.4a | energy floor | 0.172 | pJ |
| 28-02.4b | best efficiency | 5.80 | TOPS/W |
| 28-02.4c | arithmetic share | 29.0 | % |
| 28-02.4d | SRAM share | 34.8 | % |
| 28-02.4e | HBM share | 36.2 | % |
| 28-02.4f | data-movement share | 71.0 | % |
| 28-02.5 | efficiency at the peak point | 12.6 | TOPS/W |
| 28-02.6a | module power | 6.47 | W |
| 28-02.6b | module efficiency | 4.02 | TOPS/W |
| 28-02.6c | NPU-rail efficiency | 10.0 | TOPS/W |
| 28-02.7a | TPP of the GPU | 16000 | — |
| 28-02.7b | TPP at 600 INT8 TOPS | 4800 | — |
| 28-02.7c | performance density | 20.0 | per mm² |
| 28-02.8a | A vs R, arithmetic | 1.25 | — |
| 28-02.8b | A vs R, geometric | 1.00 | — |
| 28-02.8c | B vs R, arithmetic | 1.25 | — |
| 28-02.8d | B vs R, geometric | 1.25 | — |
| 28-02.8e | A vs R′, arithmetic | 1.00 | — |
| 28-02.8f | A vs R′, geometric | 1.00 | — |
| 28-02.8g | B vs R′, arithmetic | 1.5625 | — |
| 28-02.8h | B vs R′, geometric | 1.25 | — |
| 28-02.8i | A vs R″, arithmetic | 2.025 | — |
| 28-02.8j | A vs R″, geometric | 0.447 | — |
| 28-02.8k | B vs R″, arithmetic | 1.3125 | — |
| 28-02.8l | B vs R″, geometric | 0.559 | — |
| 28-02.9a | expected maximum of 5 | 1.163 | — |
| 28-02.9b | best of five | 1.74 | — |
| 28-02.9c | expected maximum of 20 | 1.867 | — |
| 28-02.9d | best of twenty | 2.07 | — |
| 28-02.11a | cycle at 1.2 days per layer | 12.0 | weeks |
| 28-02.11b | cycle at 1.5 days per layer | 15.0 | weeks |
| 28-02.12a | metal-only path | 46.5 | weeks |
| 28-02.12b | metal-only path | 10.7 | months |
| 28-02.12c | full-respin path | 57.0 | weeks |
| 28-02.12d | full-respin path | 13.1 | months |
| 28-02.12e | expected time | 50.7 | weeks |
| 28-02.12f | expected time | 11.6 | months |
| 28-02.12g | twelve months | 52.2 | weeks |
| 28-02.12h | probability of meeting 12 months | 0.6 | — |
| 28-02.12i | qualification and reports | 7.95 | weeks |
| 28-02.13a | claimed efficiency | 13.3 | TOPS/W |
| 28-02.13b | batch-1 decode bound | 28.6 | tokens/s |
| 28-02.13c | implied batch | 140 | — |
| 28-02.14a | efficiency ratio, 0.60 to 0.90 V | 2.25 | — |
