<!-- status: reviewed -->
# 14-15 · The Roofline Model, Benchmarks and How They Are Gamed

| | |
|---|---|
| **Course** | [14 · Computer Organization and Architecture](../README.md) |
| **University equivalent** | The performance-evaluation material of a computer architecture course: the roofline model, benchmark suites (SPEC, MLPerf), summarizing results with means, and the pitfalls of benchmarking (Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*, ch. 1 and ch. 4; Williams, Waterman & Patterson, "Roofline", CACM 2009) |
| **Prerequisites** | [14-14 AI Accelerators](14-14-ai-accelerators.md), [14-13 GPUs and SIMT](14-13-gpus-and-simt.md), [14-01 Performance, Power and the Iron Law](14-01-performance-power-iron-law.md) |
| **Estimated study hours** | 4 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Draw a roofline for a processor from its peak compute and memory bandwidth, and place a kernel on it from its arithmetic intensity.
2. Decide whether a kernel is compute- or memory-bound, and what optimization would help it.
3. Compute SPEC-style ratios and their geometric mean, and explain why the geometric mean is used for ratios.
4. Describe how SPEC CPU, MLPerf and Geekbench define their workloads, rules and scores.
5. Recognize the common ways benchmark results are made to look better than delivered performance, and ask the questions that expose them.

---

## 1. Big picture

Every chapter of this course has ended with the same question: how fast is it, really? Two tools answer it. The **roofline model** bounds what a kernel can achieve on a machine from just two hardware numbers and one property of the code. **Benchmarks** measure what machines actually achieve on agreed workloads. Both can be misused, and the commercial stakes of a benchmark win are large enough that misuse is common. This survey chapter equips you to read performance claims critically, which is where the course's technical content meets the boardroom.

- **The roofline turns datasheets into expectations.** Peak FLOPS and memory bandwidth bound every kernel's speed, and most kernels sit far below peak.
- **Benchmarks are contracts.** Their rules (fixed code, fixed accuracy, mandatory baselines) are what make results comparable, and the fine print is where comparisons go wrong.
- **Means matter.** The wrong average of normalized results can make either of two machines look faster.

## 2. Intuition first

**A factory with a loading dock.** A factory's output is limited either by its machines (compute) or by how fast trucks can unload raw materials (bandwidth). A product that needs a lot of machining per kilogram of material (high **arithmetic intensity**) is limited by the machines. A product that is mostly material, with little work, is limited by the dock. The **ridge point** is the ratio of machine capacity to dock capacity: products above it saturate the machines, products below it the dock.

**A car's quoted top speed.** A benchmark result is like a car's top speed: real, but measured on a closed track, with a tail wind, by the manufacturer. The rules of a benchmark are the track's rules. Read them before comparing cars.

**Where the analogies break.** A kernel's intensity is not fixed: tiling and caching can raise it (14-09, 14-14), so the same computation can move from the dock-limited to the machine-limited region. And a benchmark score summarizes many workloads into one number, which a top speed does not.

## 3. Theory

### 3.1 The roofline

Let $P$ be a machine's peak compute (FLOP/s), $B$ its memory bandwidth (bytes/s), and $I$ a kernel's **arithmetic intensity**: the FLOP it performs per byte it moves to or from memory. The kernel's attainable performance is bounded by

$$
\text{attainable} = \min(P,\; B \cdot I).
$$

On log–log axes this is a sloped line (bandwidth-bound) meeting a flat roof (compute-bound) at the **ridge point** $I^* = P/B$:

- kernels with $I < I^*$ are **memory-bound**: the cure is to raise intensity (tiling, fusion, lower-precision data) or to buy bandwidth;
- kernels with $I > I^*$ are **compute-bound**: the cure is better use of the arithmetic units (vectorization, tensor cores, lower-precision arithmetic).

Real rooflines add two kinds of ceiling. **In-core** ceilings sit below the peak: code that uses no FMA, no SIMD or no tensor cores tops out lower. **Memory** ceilings change the slope: a hierarchical roofline gives each cache level its own bandwidth line, and those lines lie *above* the DRAM slope, so a kernel whose data fits in cache can exceed the DRAM roof. A measured point below all applicable ceilings means the code is losing performance to something else, such as latency, divergence or synchronization (14-13).

### 3.2 Placing kernels

The intensity of a kernel counts the FLOP per byte of *main-memory* traffic:

| Kernel (FP32 unless stated) | FLOP | Bytes | Intensity (FLOP/byte) |
|---|---|---|---|
| Vector add $z = x + y$ | 1 | 12 | 0.083 |
| SAXPY $y = ax + y$ | 2 | 12 | 0.167 |
| 7-point stencil (each point read once) | 8 | 8 | 1 |
| LLM decoding, BF16 weights (14-14) | 2 | 2 | 1 |
| Square matrix product, $n = 4096$, each matrix moved once | $2n^3$ | $12n^2$ | 682.7 |

The byte counts assume stores write memory without first reading their line (no write-allocate, as with streaming stores). With write-allocate, every store also reads its line: the vector add then moves 16 bytes per element (**0.0625** FLOP/byte) and the stencil 12 (**0.667**). The stencil's 8 FLOP assume two coefficients, one for the centre and one shared by the six neighbours (2 multiplies, 6 adds), and its 8 bytes assume the cache supplies every neighbour after its first read.

On an H100 (67 TFLOPS FP32, 3.35 TB/s; ridge 20 FLOP/byte [1, R-220]), everything but the matrix product is memory-bound. The vector add reaches 0.28 TFLOPS, under half a percent of peak (Example 14-15.2). This is the roofline's main lesson: for most code, bandwidth, not FLOPS, is the number that matters.

![A log–log roofline plot for the H100 SXM. The FP32 roof is flat at 67 TFLOPS with a bandwidth slope of 3.35 TB/s meeting it at 20 FLOP/byte; the dense BF16 tensor roof is flat at 989.5 TFLOPS, meeting the same slope at about 295 FLOP/byte. Points mark the vector add at 0.083 FLOP/byte (0.28 TFLOPS), SAXPY at 0.167 (0.56 TFLOPS) and the 7-point stencil at 1 (3.35 TFLOPS), all on the bandwidth slope, and a 4096-cubed FP32 matrix product at 683 FLOP/byte on the FP32 roof.](../../../assets/figures/14-15/roofline.svg)

*Figure 1. The H100 roofline, from NVIDIA's published peak and bandwidth (R-220). Only the matrix product reaches a roof; every other kernel is limited by memory bandwidth.*

### 3.3 Benchmarks and their rules

A **benchmark** is a fixed workload with rules about how it may be run and reported. Three widely quoted families:

**SPEC CPU** measures processors, memory and compilers on real applications [2, R-223]:

- **SPECspeed** suites time one copy of each benchmark; **SPECrate** suites measure the throughput of many concurrent copies.
- Each benchmark's **ratio** is the reference machine's time divided by the measured time (times the copies, for SPECrate). The suite's score is the **geometric mean** of the ratios.
- **Base** results, mandatory, use the same compiler flags for every benchmark in a language. **Peak** results, optional, allow per-benchmark flags and feedback-directed optimization.
- SPEC CPU 2026, released in May 2026 with 52 benchmarks, has replaced SPEC CPU 2017, which SPEC retired on 17 November 2026. When reading a result, check which suite it comes from: scores from the two suites are not comparable.

**MLPerf** (MLCommons) measures machine-learning training and inference [3, R-224]:

- The **Closed** division requires the reference model and processing (inference allows calibration for quantization, but no retraining), so it compares systems.
- The **Open** division allows any model or method, and its results must be called "MLPerf Open".
- Inference **scenarios** differ in what they measure: single stream (90th-percentile latency), multistream (99th-percentile latency), server or interactive (throughput under a latency bound, with random Poisson arrivals; the rules list the two together) and offline (pure throughput) [3, R-224].

**Geekbench** is a widely quoted consumer CPU benchmark [4, R-225]:

- Geekbench 6 scores are calibrated so that a reference desktop scores 2,500.
- Each subsection score is the geometric mean of its workloads; the overall score is a *weighted arithmetic* mean of the integer (65%) and floating-point (35%) subsections.
- Its multi-core test has threads cooperate on one task.
- Geekbench 7 was released in July 2026; its scoring details were not available to this course.

### 3.4 Averaging results

Suppose machine A runs two programs in 10 s and 40 s, and machine B in 20 s and 20 s. Normalize to A, and B's times are 2.0 and 0.5 of A's: an arithmetic mean of 1.25, so "B is 25% slower". Normalize to B, and A's are 0.5 and 2.0: also a mean of 1.25, so "A is 25% slower". The arithmetic mean of normalized ratios depends on which machine is the reference.

The **geometric mean** does not: $\sqrt{2 \times 0.5} = 1$ either way. In general, $\text{gmean}(x_i / y_i) = \text{gmean}(x_i)/\text{gmean}(y_i)$, so the comparison between two machines is independent of the reference (Example 14-15.4). That is why SPEC uses it.

Two other rules complete the picture:

- To average **rates** over equal amounts of work (for example MB/s on files of equal size), use the **harmonic** mean, which corresponds to total work over total time.
- The geometric mean has its own blind spot. It weights a 2× gain on a trivial benchmark the same as a 2× gain on the one that matters to you. Always look at the per-benchmark results.

### 3.5 How benchmarks are gamed

The mechanisms recur across fields. Each has a question that exposes it.

| Mechanism | What happens | The question to ask |
|---|---|---|
| Peak against delivered | Quote theoretical peak (all units busy, maximum clock) rather than measured throughput | "What utilization do you measure on this workload?" |
| Precision and sparsity | Quote FP8 or FP4 rates, or rates "with sparsity", against a competitor's dense BF16 (14-13, 14-14) | "Dense, at which precision?" |
| Benchmark-specific tuning | Flags or code paths that help only the benchmark; SPEC's mandatory base results exist to limit this | "Base or peak? Same flags for all?" |
| Cherry-picking | Report the subset of benchmarks, sizes or batch sizes that win | "Show the whole suite, and the per-benchmark ratios." |
| Changing the rules | Compare an Open-division or modified-model result with Closed ones | "Which division, and is the model the reference one?" |
| Throughput against latency | Large batches raise throughput but also latency; quote throughput without the latency bound | "At what latency, and which percentile?" |
| Short runs and thermals | A short benchmark runs at boost clocks a sustained workload cannot hold | "Sustained, after how long, at what power?" |
| Missing the denominator | Performance without power, cost or chip count | "Per watt? Per dollar? Per chip?" |

None of these requires dishonesty in the narrow sense: every number can be true. The skill is to ask which number answers *your* question.

### 3.6 The lab's model

The lab's `roofline.py` holds the machines' peak and bandwidth figures from the research log (R-220, R-222) and the kernels' FLOP and byte counts. It computes intensities, attainable performance and ridge points, and provides the SPEC ratio and the three means. The figure script draws Figure 1 from the same data.

## 4. Worked examples

### Example 14-15.1 · Ridge points (tier A)

**Setup.** Find the ridge points of H100 for FP32 (67 TFLOPS) and dense BF16 tensor work (989.5 TFLOPS), both with 3.35 TB/s [1, R-220]. What does a kernel of intensity 4 FLOP/byte attain in FP32?

**Solution.** FP32: $67/3.35$ = **20** FLOP/byte. BF16: $989.5/3.35$ = **295.4** FLOP/byte. At an intensity of 4, the kernel attains $\min(67, 3.35 \times 4)$ = **13.4** TFLOPS, 20% of the FP32 peak, limited by bandwidth.

**Units check.** (FLOP/s)/(B/s) = FLOP/B.

**Sanity check.** The tensor ridge is about 15 times higher than the FP32 one: faster arithmetic makes *more* kernels memory-bound, not fewer.

### Example 14-15.2 · Placing four kernels (tier B)

**Setup.** On H100 in FP32, find the attainable performance of the vector add, SAXPY, the 7-point stencil and the $n = 4096$ matrix product of §3.2.

**Solution.**

| Kernel | Intensity | Attainable |
|---|---|---|
| Vector add | 1/12 FLOP/byte | **0.279** TFLOPS |
| SAXPY | 1/6 | **0.558** TFLOPS |
| Stencil | 1 | **3.35** TFLOPS |
| Matrix product | 682.7 | the roof, **67** TFLOPS |

Only the matrix product is compute-bound; the vector add uses **0.42**% of peak.

**Units check.** B/s × FLOP/B = FLOP/s.

**Sanity check.** These are upper bounds. Real kernels lose a further fraction to latency and overheads, and a matrix product reaches its roof only if tiling actually keeps traffic near the minimum.

### Example 14-15.3 · SPEC arithmetic (tier B)

**Setup.** SPEC's documentation gives two worked examples: a reference time of 1775 s against a measured 354.329738 s, and a SPECrate run of 8 copies with reference 1592 s and measured 541.52471 s [2, R-223]. Compute both ratios. Then find the score of a machine whose three benchmark ratios are 4, 9 and 16, and compare it with the arithmetic mean.

**Solution.**

- Ratios: $1775/354.329738$ = **5.009**, and $8 \times 1592/541.52471$ = **23.52**. (SPEC's document prints 5.009458 and 23.518776.)
- Score: $\sqrt[3]{4 \times 9 \times 16}$ = **8.32**, against an arithmetic mean of **9.67**.

**Units check.** Ratios are dimensionless.

**Sanity check.** The geometric mean is always at most the arithmetic mean, with equality only when all ratios are equal.

### Example 14-15.4 · Which machine is faster? (tier B)

**Setup.** Machine A runs two programs in 10 s and 40 s; machine B in 20 s and 20 s. Compare them by the arithmetic mean of times normalized to A, normalized to B, and by the geometric mean.

**Solution.**

- **Normalized to A:** B's ratios are 2 and 0.5, an arithmetic mean of **1.25**, so B looks 25% slower.
- **Normalized to B:** A's ratios are 0.5 and 2, also **1.25**, so A looks 25% slower.
- **Geometric mean:** **1** in both normalizations, so the machines are equal.
- **Total time:** 50 s for A and 40 s for B. B is faster on this particular mix, which is a different question, weighting each program by its run time.

**Units check.** Ratios of times.

**Sanity check.** The paradox disappears with the geometric mean because the gmean of ratios equals the ratio of gmeans, whatever the reference.

### Example 14-15.5 · A Geekbench-style composite (tier B)

**Setup.** A machine's integer workloads score 2000, 3000 and 2500, and its floating-point workloads 4000 and 1000. Compute the subsection scores and the composite with Geekbench 6's weights (65% integer, 35% floating point) [4, R-225].

**Solution.** Integer: $\sqrt[3]{2000 \times 3000 \times 2500}$ = **2466.2**. Floating point: $\sqrt{4000 \times 1000}$ = **2000**. Composite: $0.65 \times 2466.2 + 0.35 \times 2000$ = **2303.0**.

**Units check.** Scores are dimensionless, relative to a baseline of 2500.

**Sanity check.** The floating-point workloads differ by a factor of 4, yet their geometric mean (2000) sits well below their arithmetic mean (2500). A single weak workload drags a geometric mean down more than an arithmetic one.

### Example 14-15.6 · Throughput against latency (tier C)

**Setup.** An inference server answers a batch of 1 in 20 ms and a batch of 32 in 80 ms. (a) Find the throughput of each. (b) Under a 50 ms latency bound, which can it use? (c) How large is the gap between the two throughputs, and between the latencies?

**Solution.**

(a) By Little's law, throughput is batch size over latency: $1/0.020$ = **50** inferences/s, and $32/0.080$ = **400**/s.

(b) Only batch 1 meets 50 ms. The 400/s figure is an offline-scenario number, not a server-scenario one.

(c) Batching gives **8** times the throughput at **4** times the latency.

**Units check.** Inferences / s.

**Sanity check.** This is why MLPerf separates offline from server scenarios: the same hardware gives very different numbers under the two rules.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 14-15.1a | FP32 ridge point | 20 | FLOP/B |
| Ex 14-15.1b | BF16 ridge point | 295.4 | FLOP/B |
| Ex 14-15.1c | attainable at 4 FLOP/B | 13.4 | TFLOPS |
| Ex 14-15.2a | vector add | 0.279 | TFLOPS |
| Ex 14-15.2b | SAXPY | 0.558 | TFLOPS |
| Ex 14-15.2c | stencil | 3.35 | TFLOPS |
| Ex 14-15.2d | matrix product | 67 | TFLOPS |
| Ex 14-15.2e | vector add, fraction of peak | 0.42 | % |
| Ex 14-15.3a | SPECspeed ratio | 5.009 | — |
| Ex 14-15.3b | SPECrate ratio | 23.52 | — |
| Ex 14-15.3c | geometric mean of 4, 9, 16 | 8.32 | — |
| Ex 14-15.3d | arithmetic mean | 9.67 | — |
| Ex 14-15.4a | arithmetic mean normalized to A | 1.25 | — |
| Ex 14-15.4b | arithmetic mean normalized to B | 1.25 | — |
| Ex 14-15.4c | geometric mean | 1 | — |
| Ex 14-15.5a | integer subsection | 2466.2 | — |
| Ex 14-15.5b | floating-point subsection | 2000 | — |
| Ex 14-15.5c | composite | 2303.0 | — |
| Ex 14-15.6a | throughput, batch 1 | 50 | /s |
| Ex 14-15.6b | throughput, batch 32 | 400 | /s |
| Ex 14-15.6c | throughput gain | 8 | — |
| Ex 14-15.6d | latency increase | 4 | — |
| Txt 14-15.a | vector add with write-allocate | 0.0625 | FLOP/B |
| Txt 14-15.b | stencil with write-allocate | 0.667 | FLOP/B |

## 5. Simulate it

The lab, [labs/14-15-lab](../labs/14-15-lab/README.md), provides `roofline.py`. In the notebook you:

1. **Draw rooflines** for H100 (FP32 and BF16), TPU v4 and TPU7x, and place the course's kernels on them.
2. **Find each kernel's bottleneck** and the intensity it would need to reach each roof.
3. **Recompute SPEC-style scores** with arithmetic, geometric and harmonic means on a small table of times, and watch the arithmetic mean's verdict flip with the reference machine.

**Guided exercise (predict, then run).** **Before Part 1,** predict which of the four machines gives the highest attainable performance for LLM decoding at 1 FLOP/byte. (TPU7x: at 1 FLOP/byte every machine is bandwidth-bound, and TPU7x has the most bandwidth, 7.38 TB/s.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| More bandwidth (HBM stacks) | Every memory-bound kernel | Cost, power, packaging | Product architect |
| More peak compute | Compute-bound kernels only | Area and power wasted on memory-bound work | Architect |
| Software intensity (tiling, fusion, quantized data) | Moves kernels toward the roof | Engineering effort per kernel | Kernel and compiler teams |
| Benchmark choice and rules | Comparable, honest results | Results look less impressive | Marketing with engineering |
| Summary statistic | Reference-independent comparison (gmean) | Hides per-workload detail | Benchmark designers |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Roofline | attainable = min(peak, bandwidth × intensity) | §3.1 |
| H100 ridge points | 20 FLOP/B (FP32), about 295 (dense BF16) | [1, R-220] |
| Vector add / SAXPY intensity | 1/12 and 1/6 FLOP/B (FP32) | §3.2 |
| SPEC CPU | ratio = reference time / measured time; geometric mean; base mandatory | [2, R-223] |
| SPEC CPU 2026 | 52 benchmarks; released May 2026; CPU 2017 retired 17 Nov 2026 | [2, R-223] |
| MLPerf | Closed against Open; single stream, multistream, server, offline | [3, R-224] |
| Geekbench 6 | baseline 2500; integer 65%, floating point 35% | [4, R-225] |

## 8. Common mistakes

- **Using the arithmetic mean of normalized ratios.** Its verdict depends on the reference machine; use the geometric mean.
- **Comparing peak with measured.** Peak is a ceiling, not a result.
- **Ignoring the memory roof.** Doubling FLOPS does nothing for a memory-bound kernel.
- **Mixing divisions or scenarios.** MLPerf Open and Closed results, or offline and server ones, are not comparable.
- **Forgetting the denominator.** Performance per chip, per watt and per dollar can rank systems differently.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **SPEC CPU 2026** is now SPEC's current CPU suite: 52 benchmarks, released 5 May 2026, with SPEC CPU 2017 retired on 17 November 2026 [2, R-223] **[Established]**.
- **MLPerf** rounds continue for training and inference, with rules revised each round. The current training table lists large language models among its closed-division workloads [3, R-224] **[Established]**.
- **Geekbench 7** was released on 23 July 2026, with new media workloads and a revised multi-core test [4, R-225] **[Established]**. Its scoring details were not verified.

### Why it matters commercially

- **Benchmarks move markets.** Launch claims, procurement decisions and analyst comparisons lean on a handful of benchmarks. Knowing their rules is a negotiating advantage.
- **The roofline is a due-diligence tool.** For any accelerator pitch, the first question is where the customer's workloads sit relative to the ridge point. That decides whether the headline FLOPS are relevant at all.

### Marketing vs Reality

- **"N× faster."** *Reality:* on which benchmark, at which precision, which division, which batch size, and against which baseline? *Sanity check:* ask for the full table and the rules followed.
- **"Industry-leading SPEC score."** *Reality:* base or peak, and which suite version (2017 or 2026)? *Sanity check:* compare base results on the same suite.
- **"Record MLPerf result."** *Reality:* records are per benchmark, per scenario, per division and often per system size. *Sanity check:* find the matching result for the competitor in the same category.

### Questions for engineering leaders

1. **"Where do our top five workloads sit on your roofline?"**
   *Strong:* measured intensities and achieved FLOPS, plotted. *Evasive:* peak TFLOPS.
2. **"Which benchmark results are base, Closed, dense and sustained?"**
   *Strong:* each qualifier answered. *Evasive:* "industry standard".
3. **"What is your performance per watt and per dollar on our workload?"**
   *Strong:* measured, with the power and price basis. *Evasive:* performance alone.
4. **"How did you choose the workloads you report?"**
   *Strong:* a stated selection rule, with losses shown. *Evasive:* only wins.

## 10. Concept check

**Q1.** What two hardware numbers define a roofline, and where is the ridge?

<details><summary>Answer</summary>

Peak compute $P$ and memory bandwidth $B$; the ridge is at intensity $P/B$.

</details>

**Q2.** How do you tell whether a kernel is memory-bound?

<details><summary>Answer</summary>

Compute its arithmetic intensity (FLOP per byte of memory traffic); if it is below the ridge point, bandwidth limits it.

</details>

**Q3.** Why does SPEC use the geometric mean?

<details><summary>Answer</summary>

Because the geometric mean of ratios equals the ratio of geometric means, the comparison of two machines does not depend on which reference machine the ratios are normalized to.

</details>

**Q4.** What is the difference between SPEC base and peak?

<details><summary>Answer</summary>

Base (mandatory) uses the same compiler flags for all benchmarks in a language; peak (optional) allows per-benchmark flags and feedback-directed optimization.

</details>

**Q5.** Why are MLPerf Closed and Open results not comparable?

<details><summary>Answer</summary>

Closed requires the reference model and processing, so it compares systems; Open allows any model or method, so it mixes system and algorithm improvements.

</details>

Now work the [problem set](../problems/14-15-problems.md).

## 11. Key terms

[Roofline model](../../../reference/glossary.md#roofline-model) · [Arithmetic intensity](../../../reference/glossary.md#arithmetic-intensity) · [Ridge point](../../../reference/glossary.md#ridge-point) · [Benchmark](../../../reference/glossary.md#benchmark) · [SPEC CPU](../../../reference/glossary.md#spec-cpu) · [MLPerf](../../../reference/glossary.md#mlperf) · [Geometric mean](../../../reference/glossary.md#geometric-mean)

## 12. Connections

- **Builds on:** the iron law ([14-01](14-01-performance-power-iron-law.md)); bandwidth and caches ([14-09](14-09-memory-hierarchy-and-caches.md)); GPUs and accelerators ([14-13](14-13-gpus-and-simt.md), [14-14](14-14-ai-accelerators.md)).
- **Next:** this is the last chapter of Course 14; the course exam and equation sheet follow.
- **Used later:** the memory wall ([23-01](../../23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md)); performance claims across the practitioner layer.

> **Deeper:** see companion repo *LLM Inference Engineering* for serving benchmarks and their latency targets.

## 13. Further study

- S. Williams, A. Waterman and D. Patterson, "Roofline: An Insightful Visual Performance Model for Multicore Architectures," *Communications of the ACM* 52(4), 2009.
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, ch. 1 (measuring and summarizing performance) and ch. 4 (the roofline model, applied to SIMD and GPU architectures).
- P. J. Fleming and J. J. Wallace, "How Not to Lie with Statistics: The Correct Way to Summarize Benchmark Results," *Communications of the ACM* 29(3), 1986.
- SPEC CPU and MLPerf documentation (Sources).

## 14. Sources

1. NVIDIA, H100 product page and Hopper blog. [R-220](../../../reference/research-log.md#r-220--nvidia-h100-hopper-specifications)
2. SPEC, CPU 2017 overview and retirement notice; SPEC CPU 2026 release and overview. [R-223](../../../reference/research-log.md#r-223--spec-cpu-2017-and-spec-cpu-2026)
3. MLCommons, MLPerf Inference and Training rules. [R-224](../../../reference/research-log.md#r-224--mlperf-divisions-and-scenarios)
4. Primate Labs, "Geekbench 6 Benchmark Internals" (May 2024) and the Geekbench 7 announcement. [R-225](../../../reference/research-log.md#r-225--geekbench-6-scoring-and-geekbench-7)

The roofline model, benchmark means and benchmarking pitfalls are textbook material (Further study). Every number in the examples is recomputed by the verify script from the logged figures.
