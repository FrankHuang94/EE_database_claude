# Solutions 14-15 · The Roofline Model, Benchmarks and How They Are Gamed

Problems: [14-15 problems](../problems/14-15-problems.md) · Chapter: [14-15](../chapters/14-15-roofline-and-benchmarks.md). Every number below is recomputed by [verify_14_15.py](../verify/verify_14_15.py) from the logged machine figures (R-220, R-222) and the definitions of the means.

---

## Solutions

### Solution 14-15.1

The ridge is $275/1.2$ = **229.2** FLOP/byte. At 50 FLOP/byte the kernel attains $\min(275, 1.2 \times 50)$ = **60** TFLOPS, 22% of peak.

### Solution 14-15.2

$2n^2$ FLOP over $4n^2$ bytes = **0.5** FLOP/byte. On H100 that gives $3.35 \times 0.5$ = **1.675** TFLOPS. Matrix–vector products, such as LLM decoding (14-14), are bandwidth-bound on every modern machine.

### Solution 14-15.3

- **Unfused:** the first kernel moves 12 bytes for 1 FLOP, and the second 8 bytes (read $z$, write $w$) for 1 FLOP: 2 FLOP over 20 bytes = **0.1** FLOP/byte.
- **Fused:** reads $x$ and $y$ and writes $w$, 12 bytes for 2 FLOP: **0.167** FLOP/byte.

On a bandwidth-bound machine the speedup is the traffic ratio, $20/12$ = **1.667**. The intermediate $z$ never touches memory. This is why compilers for AI accelerators fuse element-wise operations.

### Solution 14-15.4

Six bytes per element (two 2-byte reads, one write) for 2 FLOP: **0.333** FLOP/byte. Bandwidth delivers $3.35 \times 0.333$ = **1.117** TFLOPS, a speedup of **2** over FP32. Narrower data helps memory-bound kernels exactly in proportion to the bytes saved.

### Solution 14-15.5

The ratios are $1000/250 = 4$, $2000/400 = 5$ and $3000/1000 = 3$, and the score is their geometric mean, $\sqrt[3]{60}$ = **3.915**. The SPECrate ratio is $16 \times 1000/400$ = **40**.

### Solution 14-15.6

Over two equal files, the average rate is total bytes over total time, the harmonic mean: $2/(1/100 + 1/400)$ = **160** MB/s. The arithmetic mean, **250** MB/s, overstates it, because the slow file takes four times as long.

### Solution 14-15.7

- **Normalized to A:** B's ratios are 2, 0.5 and 1, an arithmetic mean of **1.167** (B looks 17% slower).
- **Normalized to B:** A's ratios are 0.5, 2 and 1, also an arithmetic mean of 1.167 (A looks 17% slower).
- **Geometric mean:** **1** both ways, a consistent verdict: equal.

### Solution 14-15.8

$10 + 2b \le 50$ gives $b \le 20$, so the highest throughput is $20/0.050$ = **400** requests/s. Without a bound, a batch of 128 takes 266 ms: $128/0.266$ = **481.2**/s. The offline figure is only 20% higher, but at 5.3 times the latency.

### Solution 14-15.9

Removing sparsity, then going from FP4 to FP8 and from FP8 to BF16, halves the rate three times: $4000/8$ = **500** TFLOPS dense BF16-equivalent. The headline ratio is $4000/989.5$ = **4.04**; the equivalent ratio is **0.505**. X looks four times faster and is half as fast, on dense BF16 work. (Whether X's lower-precision rates are *useful* depends on whether the models run accurately at FP4 with sparsity.)

### Solution 14-15.10

A delivers **0.714** inferences per joule and B **1.0**. B is 1.4 times more efficient, although A has 1.67 times the throughput. In A's 700 W budget, $700/300$ = **2.33** B's would deliver **700** inferences/s, 40% more than A. In power-limited data centres, per-watt numbers often decide.

### Solution 14-15.11

(a) The Closed division requires a model equivalent to the reference, with only calibration for quantization allowed, while the Open division allows any model, pre- and post-processing and retraining [R-224]. An Open result may come from a smaller, retrained or differently quantized model, so it measures a different task. The rules require the qualified name "MLPerf Open" for exactly this reason.

(b) The server figure, **250** samples/s. The server scenario sends queries at random (Poisson) times and counts only throughput that meets the latency bound; offline hands the system all queries at once, so it can batch freely. The gap, 400 against 250, is the price of meeting the latency target.

(c) $0.65 \times 3000 + 0.35 \times 2000$ = 1950 + 700 = **2650**. With Floating Point at 2400 the composite is 1950 + 840 = 2790, a rise of 140/2650 = **5.28**%: a 20% gain in one subsection is diluted by its 35% weight.

(d) The geometric mean scales by the fourth root of the factor: $2^{1/4}$ = 1.189, a rise of **18.9**%. A geometric mean dampens any single workload, which is one reason suites use it.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 14-15.1a | TPU v4 ridge | 229.2 | FLOP/B |
| 14-15.1b | attainable at 50 FLOP/B | 60 | TFLOPS |
| 14-15.2a | matrix–vector intensity | 0.5 | FLOP/B |
| 14-15.2b | attainable on H100 | 1.675 | TFLOPS |
| 14-15.3a | unfused intensity | 0.1 | FLOP/B |
| 14-15.3b | fused intensity | 0.167 | FLOP/B |
| 14-15.3c | fusion speedup | 1.667 | — |
| 14-15.4a | BF16 SAXPY intensity | 0.333 | FLOP/B |
| 14-15.4b | attainable | 1.117 | TFLOPS |
| 14-15.4c | speedup over FP32 | 2 | — |
| 14-15.5a | score | 3.915 | — |
| 14-15.5b | SPECrate ratio | 40 | — |
| 14-15.6a | average rate | 160 | MB/s |
| 14-15.6b | arithmetic mean | 250 | MB/s |
| 14-15.7a | arithmetic mean, normalized to A | 1.167 | — |
| 14-15.7b | arithmetic mean, normalized to B | 1.167 | — |
| 14-15.7c | geometric mean | 1 | — |
| 14-15.8a | throughput under 50 ms | 400 | /s |
| 14-15.8b | throughput at batch 128 | 481.2 | /s |
| 14-15.9a | X dense BF16-equivalent | 500 | TFLOPS |
| 14-15.9b | headline ratio | 4.04 | — |
| 14-15.9c | equivalent ratio | 0.505 | — |
| 14-15.10a | A, inferences per joule | 0.714 | /J |
| 14-15.10b | B, inferences per joule | 1.0 | /J |
| 14-15.10c | B's per A's power | 2.33 | — |
| 14-15.10d | throughput of those B's | 700 | /s |
| 14-15.11a | server-scenario throughput | 250 | /s |
| 14-15.11b | Geekbench composite | 2650 | — |
| 14-15.11c | composite change from +20% FP | 5.28 | % |
| 14-15.11d | subsection rise from one doubled workload | 18.9 | % |
