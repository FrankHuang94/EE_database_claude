<!-- status: verified -->
# 14-14 · AI Accelerators: Systolic Arrays, Dataflow and Low Precision

| | |
|---|---|
| **Course** | [14 · Computer Organization and Architecture](../README.md) |
| **University equivalent** | The domain-specific-architecture material of a computer architecture course: why specialized accelerators, matrix-multiply engines and systolic arrays, dataflow taxonomies (weight-, output- and input-stationary), on-chip SRAM against HBM, quantization and sparsity (Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*, ch. 7; Sze, Chen, Yang & Emer, *Efficient Processing of Deep Neural Networks*) |
| **Prerequisites** | [14-13 GPUs and SIMT](14-13-gpus-and-simt.md), [14-09 Memory Hierarchy and Caches](14-09-memory-hierarchy-and-caches.md), [14-04 Computer Arithmetic and Number Formats](14-04-computer-arithmetic-and-number-formats.md) |
| **Estimated study hours** | 9 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Explain why neural-network workloads reward specialized hardware, in terms of operation mix, data reuse and energy per operation.
2. Trace a systolic array through a matrix multiplication, and compute its latency, throughput and utilization, including for large matrices tiled onto it.
3. Compare weight-, output- and input-stationary dataflows by the data each keeps in place and the reuse it needs, and compute the reuse that makes data movement cheaper than arithmetic.
4. Quantize tensors to low-precision integers, and estimate the resulting error and signal-to-quantization-noise ratio.
5. Use peak compute and memory bandwidth to tell whether a workload (such as large-language-model decoding) is compute- or memory-bound on a given accelerator.

---

## 1. Big picture

General-purpose processors pay a large overhead to be programmable. Horowitz's 45 nm figures put a simple processor's energy per instruction at about 70 pJ, against "a few pJ for an operation" [1, R-208]. Deep learning is dominated by one operation, multiply-accumulate, repeated billions of times on large matrices with predictable access patterns. A **domain-specific accelerator** removes most of the overhead:

- it executes thousands of multiply-accumulates (MACs) per instruction, in a **matrix unit**;
- it keeps operands in large on-chip SRAMs and reuses them many times;
- it uses narrow number formats (BF16, FP8, INT8, FP4) whose multipliers are small and cheap.

Google's TPU, NVIDIA's tensor cores, and the neural engines in phones and PCs are all variations on these ideas.

- **The matrix unit is the heart.** TPU v4 has eight 128 × 128 MAC arrays per chip, 131,072 MACs per cycle [2, R-222].
- **Data movement, not arithmetic, sets the energy and the speed.** A DRAM access costs thousands of times an 8-bit MAC [1, R-208], so accelerators are designed around reuse.
- **Low precision is a lever as big as the hardware.** Halving the bits roughly halves the memory traffic, and shrinks the multiplier by more than half.

## 2. Intuition first

**A bucket brigade.** A row of people passes buckets along a line. No one walks to the well; each person only reaches to the neighbour. A **systolic array** is a grid of simple processing elements (PEs) that pass data to their neighbours in rhythm, like the pulse that gives it its name. Each PE does one multiply-accumulate per beat on the values passing through. A value fetched once from memory is used by every PE it passes, so a 128 × 128 array reuses each fetched operand up to 128 times.

**A kitchen that keeps ingredients on the counter.** A cook preparing hundreds of identical dishes keeps the common ingredients within reach (on-chip SRAM) and fetches from the storeroom (DRAM) only rarely. Which ingredient stays on the counter, the weights, the partial results or the inputs, is the **dataflow** choice.

**Where the analogies break.** A real array must be filled and drained, which costs cycles every time the matrices change. And the "ingredients" are numbers whose precision can be traded for speed, which a cook cannot do with flour.

## 3. Theory

### 3.1 What neural networks compute

A fully connected layer computes $y = W x$; a batch of inputs turns it into a matrix multiplication $Y = X W^\top$. Convolutions can be rewritten as matrix multiplications, and transformer attention and projections are matrix multiplications. A product of an $M \times K$ matrix by a $K \times N$ matrix needs $MKN$ MACs ($2MKN$ FLOP) but touches only $MK + KN + MN$ values. Its **arithmetic intensity** grows with the matrix sizes, which is why matrix multiplication can run near peak while element-wise operations cannot (14-13).

### 3.2 Systolic arrays

An **output-stationary** systolic array of $P \times P$ PEs computes $C = AB$:

- Row $i$ of $A$ enters the left edge, delayed by $i$ cycles, and moves one PE right per cycle.
- Column $j$ of $B$ enters the top edge, delayed by $j$ cycles, and moves one PE down per cycle.
- PE $(i, j)$ holds the accumulator for $C_{ij}$.

With these delays (the **skew**), $a_{ik}$ and $b_{kj}$ meet in PE $(i, j)$ at cycle

$$
t = k + i + j,
$$

so each PE sees exactly the pairs it needs, in order. The last product, in PE $(M-1, N-1)$ with $k = K - 1$, happens at cycle $K + M + N - 3$. Counting from cycle 0, a multiplication of an $M \times K$ by a $K \times N$ matrix takes

$$
T = K + M + N - 2 \text{ cycles}.
$$

The array performs at most $P^2$ MACs per cycle, so its **utilization** is $MKN / (P^2 T)$. The $M + N - 2$ cycles of **fill and drain** are overhead. They are negligible when $K$ is large, and dominant when it is small (Example 14-14.2).

Each operand fetched at the edge is used by up to $P$ PEs: $a_{ik}$ by the whole row, $b_{kj}$ by the whole column. That is the reuse that makes the array efficient. Only nearest-neighbour wires are needed, so the array scales without long global wires.

### 3.3 Tiling large matrices

Real matrices are far larger than the array. They are cut into **tiles**: each $P \times P$ block of $C$ is computed by streaming the matching row strip of $A$ and column strip of $B$ through the array. A product of $M \times K$ and $K \times N$ matrices on a $P \times P$ array needs $\lceil M/P \rceil \lceil N/P \rceil$ output tiles. Done one after another, each costs $K + 2(P-1)$ cycles. Real designs overlap one tile's drain with the next tile's fill (double buffering), which brings utilization close to 100% for large $K$.

### 3.4 Dataflows

What stays in place inside the array defines the **dataflow** [3]:

| Dataflow | Stays in the PEs | Moves | Good when |
|---|---|---|---|
| Output-stationary | partial sums $C_{ij}$ | inputs and weights | large $K$ (long accumulations) |
| Weight-stationary | weights $W$ | inputs in, partial sums out | weights reused across many inputs (large batch) |
| Input-stationary | inputs | weights in, partial sums out | inputs reused across many filters |

A weight-stationary array, for example, loads a tile of weights into the PEs once and streams a whole batch of activations past them. Every choice aims at the same goal, to fetch each value from the expensive level of memory as few times as possible and reuse it from cheap registers and SRAM.

**Energy per MAC with movement.** If each MAC must fetch its operands from a level that costs $E_\text{fetch}$ per byte, and each fetched byte is reused $R$ times, the data-movement energy per MAC is $2E_\text{fetch}/R$ for two 1-byte operands. It falls below the MAC's own energy only when

$$
R \ge \frac{2 E_\text{fetch}}{E_\text{MAC}}.
$$

With Horowitz's 45 nm figures, that is about 22 reuses for a 32 KB SRAM and about 1400 for DRAM (Example 14-14.4) [1, R-208]. Accelerators therefore build hierarchies of buffers (registers in the PEs, local SRAM, global SRAM, HBM) and schedule the computation so that most operands are reused hundreds of times on chip.

### 3.5 Low precision: quantization

Neural networks tolerate low-precision arithmetic. **Quantization** maps real values to $b$-bit integers. In **symmetric per-tensor** quantization,

$$
s = \frac{\max |x|}{2^{b-1} - 1}, \qquad q = \operatorname{round}(x / s), \qquad \hat{x} = s\,q.
$$

The rounding error is at most $s/2$. For signals that use the full range, the **signal-to-quantization-noise ratio** follows the familiar $6.02b + 1.76$ dB rule for a full-scale sinusoid (11-10), about 6 dB per bit (Example 14-14.5). Practical schemes refine this:

- per-channel or per-block scales;
- block formats such as OCP MX, which share an exponent per block of values (14-04);
- calibration on real data, and training aware of quantization.

The arithmetic rewards fewer bits sharply. A multiplier's area grows roughly with the square of the operand width, and Horowitz lists an 8-bit integer multiply at 0.2 pJ against 3.1 pJ for 32 bits [1, R-208].

### 3.6 Sparsity

Many weights can be pruned to zero. Unstructured sparsity is hard for hardware to exploit, because the zeros are scattered. **Structured sparsity** (such as 2 zeros in every 4 weights) lets a matrix unit skip zeros predictably, for up to 2× throughput: NVIDIA's tensor cores support 2:4 (14-13), and TPU7x pairs its TensorCores with separate SparseCores [2, R-222]. Headline throughput figures that assume sparsity apply only to models pruned that way (14-13).

### 3.7 SRAM against HBM, and the memory wall

An accelerator's chip area is split between MAC arrays and SRAM, and its package between compute dies and HBM stacks (14-09). The ratio of peak compute to memory bandwidth, the **ridge point** of the roofline (14-15), says how much reuse a workload needs to stay compute-bound:

- TPU v4: 275 TFLOPS against 1.2 TB/s, a ridge of about 229 FLOP/byte [2, R-222];
- TPU7x (Ironwood): 2307 TFLOPS against 7380 GB/s, about 313 FLOP/byte [2, R-222].

Large-language-model inference at small batch sizes has an intensity near 1 FLOP per weight byte, two orders of magnitude below these ridges, so it is limited by memory bandwidth (Example 14-14.6). That is why HBM bandwidth per chip has grown about sixfold from v4 to Ironwood, and why batching, quantization of weights and caches, and speculative decoding matter so much in serving.

> **Deeper:** see companion repo *LLM Inference Engineering* for batching, KV caches and serving systems.

### 3.8 The lab's models

The lab has two parts:

- `systolic.py` simulates an output-stationary array cycle by cycle (registers, skewed inputs, MACs). It returns the product, the cycles and the MAC count; it also estimates tiled cycles and implements symmetric quantization.
- `systolic4.v` is a 4 × 4 array of signed 8-bit PEs in Verilog. Its self-checking testbench compares all 16 accumulators with a reference after every cycle, and confirms that they are first all correct after exactly $K + 6$ cycles.

## 4. Worked examples

### Example 14-14.1 · Counting MACs (tier A)

**Setup.** A TPU v4 chip has 2 TensorCores, each with four 128 × 128 matrix units, and runs at 1050 MHz [2, R-222]. How many MACs per cycle does the chip perform, and what peak does that give? How does that compare with the 275 TFLOPS in the paper, and with H100's dense BF16 tensor rate (989.5 TFLOPS, 14-13)?

**Solution.** Each unit has $128^2 = 16{,}384$ MACs, so the chip has $2 \times 4 \times 16384$ = **131,072** MACs per cycle. At 2 FLOP per MAC and 1.05 GHz, that is $131072 \times 2 \times 1.05 \times 10^9$ = **275.25** TFLOPS, the paper's 275. H100's dense BF16 rate is $989.5 / 275.25$ = **3.6** times higher, two years later and on a newer process.

**Units check.** MACs/cycle × FLOP/MAC × cycles/s = FLOP/s.

**Sanity check.** The paper's figure is exactly what the array count implies, so the peak assumes every MAC busy every cycle.

### Example 14-14.2 · A small systolic array (tier B)

**Setup.** A 4 × 4 output-stationary array multiplies a 4 × K matrix by a K × 4 matrix. Find the cycles and the utilization for K = 4 and K = 16. For a 128 × 128 array with M = N = 128 and K = 1000, what is the utilization?

**Solution.** $T = K + M + N - 2$:

- K = 4: $4 + 4 + 4 - 2$ = **10** cycles, for $4 \times 4 \times 4 = 64$ MACs in $16 \times 10 = 160$ MAC-slots: **40**% utilization.
- K = 16: **22** cycles, $256/352$ = **72.7**%.
- 128 × 128 array, K = 1000: $1000 + 254 = 1254$ cycles, $1000/1254$ = **79.7**%.

The Python simulator and the Verilog array both reach the correct product in exactly 10 and 22 cycles.

**Units check.** Utilization = MACs / (PEs × cycles).

**Sanity check.** Fill and drain cost $M + N - 2$ cycles regardless of K, so utilization approaches 100% only as K grows, or when tiles are overlapped.

### Example 14-14.3 · Tiling a large multiplication (tier B)

**Setup.** A 1024 × 1024 × 1024 matrix multiplication runs on one 128 × 128 array, tile after tile with no overlap. Find the cycles, the ideal cycles at 100% utilization, and the utilization.

**Solution.** There are $(1024/128)^2 = 64$ output tiles, each taking $1024 + 2 \times 127 = 1278$ cycles: **81,792** cycles. The ideal is $1024^3 / 128^2$ = **65,536** cycles. Utilization is **80.1**%. Overlapping each tile's drain with the next tile's fill removes almost all of the difference.

**Units check.** Tiles × cycles per tile.

**Sanity check.** The per-tile overhead, 254 of 1278 cycles, is the same fraction as in Example 14-14.2's K = 1000 case.

### Example 14-14.4 · How much reuse? (tier B)

**Setup.** Using Horowitz's 45 nm figures [1, R-208], an INT8 MAC costs about 0.23 pJ (0.2 pJ multiply plus 0.03 pJ add). A 64-bit read from a 32 KB SRAM costs 20 pJ, and a DRAM access 1.3 nJ per 64 bits (the low end of the paper's range). Find the energy to fetch the two 1-byte operands of a MAC from each level, and the reuse at which data movement costs no more than the MAC.

**Solution.**

- **SRAM:** 20 pJ per 8 bytes is 2.5 pJ per byte, so two operands cost **5** pJ, 21.7 times the MAC. Reuse must be at least **22**.
- **DRAM:** 1300 pJ per 8 bytes is 162.5 pJ per byte, so two operands cost **325** pJ. Reuse must be at least **1414**.

**Units check.** pJ/B × B = pJ.

**Sanity check.** A 128 × 128 array reuses each edge operand 128 times internally. The rest of the reuse must come from buffering tiles in SRAM, so that each weight fetched from HBM serves thousands of MACs. (The accumulator add is really 32 bits wide, about 0.1 pJ, which changes the thresholds only modestly.)

### Example 14-14.5 · Quantizing to INT8 and INT4 (tier B)

**Setup.** The 64 samples $x_k = \sin(2\pi k/64)$ are quantized symmetrically to 8 and to 4 bits. Find the scale, the largest error, and the SQNR, and compare with $6.02b + 1.76$ dB.

**Solution.**

- **8 bits:** $\max|x| = 1$, so $s = 1/127$ = **0.00787**. The largest error is **0.00369**, within $s/2$. The SQNR, signal power over error power, is **48.7** dB against **49.9** dB from the formula.
- **4 bits:** $s = 1/7$ = **0.143**, the largest error **0.0667**, and the SQNR **25.2** dB against 25.8.

**Units check.** dB = 10 log₁₀ of a power ratio.

**Sanity check.** Four bits fewer cost about 24 dB, 6 dB per bit. The formula assumes the error is uniform and independent of the signal; with only 64 samples of a periodic signal that is roughly, not exactly, true.

### Example 14-14.6 · Is decoding memory-bound? (tier C)

**Setup.** Generating one token of a 7-billion-parameter language model at batch size 1 multiplies every weight once: 2 FLOP per parameter, with BF16 weights (2 bytes). (a) What is the arithmetic intensity, and how does it compare with the ridge points of TPU v4 (275 TFLOPS, 1.2 TB/s) and TPU7x (2307 TFLOPS, 7380 GB/s) [2, R-222]? (b) What token rate does memory bandwidth allow on each chip, ignoring everything but weights? (c) At what batch size does TPU v4 become compute-bound?

**Solution.**

(a) $2$ FLOP / $2$ bytes = **1** FLOP/byte, against ridges of **229** and **313** FLOP/byte. Decoding is deeply memory-bound.

(b) Each token reads all $1.4 \times 10^{10}$ bytes of weights:

- TPU v4: $1.2 \times 10^{12} / 1.4 \times 10^{10}$ = **85.7** tokens/s, using $1.2$ TFLOPS, **0.44**% of peak;
- TPU7x: **527** tokens/s.

(c) With a batch of $B$ sequences, each weight read serves $B$ tokens, so the intensity is $B$ FLOP/byte. The chip becomes compute-bound at $B \approx$ **230**.

**Units check.** (B/s)/(B/token) = tokens/s.

**Sanity check.** This is why serving systems batch requests aggressively and quantize weights to 8 or 4 bits: both raise FLOP per byte of memory traffic.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 14-14.1a | MACs per cycle per chip | 131072 | — |
| Ex 14-14.1b | peak | 275.25 | TFLOPS |
| Ex 14-14.1c | H100 dense BF16 / TPU v4 | 3.6 | — |
| Ex 14-14.2a | cycles, K = 4 | 10 | — |
| Ex 14-14.2b | utilization, K = 4 | 40 | % |
| Ex 14-14.2c | cycles, K = 16 | 22 | — |
| Ex 14-14.2d | utilization, K = 16 | 72.7 | % |
| Ex 14-14.2e | utilization, 128 × 128, K = 1000 | 79.7 | % |
| Ex 14-14.3a | cycles, tiled | 81792 | — |
| Ex 14-14.3b | ideal cycles | 65536 | — |
| Ex 14-14.3c | utilization | 80.1 | % |
| Ex 14-14.4a | operand energy from SRAM | 5 | pJ |
| Ex 14-14.4b | reuse needed, SRAM | 22 | — |
| Ex 14-14.4c | operand energy from DRAM | 325 | pJ |
| Ex 14-14.4d | reuse needed, DRAM | 1414 | — |
| Ex 14-14.5a | INT8 scale | 0.00787 | — |
| Ex 14-14.5b | INT8 largest error | 0.00369 | — |
| Ex 14-14.5c | INT8 SQNR | 48.7 | dB |
| Ex 14-14.5d | 8-bit formula | 49.9 | dB |
| Ex 14-14.5e | INT4 scale | 0.143 | — |
| Ex 14-14.5f | INT4 largest error | 0.0667 | — |
| Ex 14-14.5g | INT4 SQNR | 25.2 | dB |
| Ex 14-14.6a | arithmetic intensity | 1 | FLOP/B |
| Ex 14-14.6b | TPU v4 ridge | 229 | FLOP/B |
| Ex 14-14.6c | TPU7x ridge | 313 | FLOP/B |
| Ex 14-14.6d | tokens/s, TPU v4 | 85.7 | — |
| Ex 14-14.6e | fraction of v4 peak used | 0.44 | % |
| Ex 14-14.6f | tokens/s, TPU7x | 527 | — |
| Ex 14-14.6g | batch for compute-bound, v4 | 230 | — |

## 5. Simulate it

The lab, [labs/14-14-lab](../labs/14-14-lab/README.md), provides the Python systolic simulator and the Verilog 4 × 4 array. You:

1. **Run the Verilog testbench** and watch the skewed operands march through the array in the waveform.
2. **Sweep K, M and N** in the Python simulator and confirm $T = K + M + N - 2$; plot utilization against K.
3. **Tile a large multiplication** and compare tiled cycles with the ideal.
4. **Quantize** weights and activations to 8, 6 and 4 bits, and measure the error of a matrix product.

**Guided exercise (predict, then run).** **Before Part 2,** predict the cycles for M = 3, K = 5, N = 2 on a 4 × 4 array. ($5 + 3 + 2 - 2 = 8$.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Array size $P$ | Peak MACs per cycle, reuse per fetch | Fill and drain overhead, utilization on small or odd-shaped matrices | Accelerator architect |
| Dataflow choice | Reuse of the dominant operand | Flexibility across layer shapes | Accelerator architect, compiler team |
| On-chip SRAM | Reuse, fewer HBM accesses | Die area, leakage | SoC architect |
| HBM stacks | Bandwidth for low-intensity work (decoding) | Cost, power, supply (Course 23) | Product architect |
| Narrower formats (FP8, INT8, FP4) | Throughput, memory traffic, energy | Accuracy; calibration and tooling | Architect with ML scientists |
| Structured sparsity | Up to 2× throughput | Pruned models only; accuracy | Architect, model developers |
| Programmability (vector units, general cores) | Covers non-matrix operations | Area taken from matrix units | Product architect |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Systolic latency | $K + M + N - 2$ cycles; utilization $MKN/(P^2 T)$ | §3.2 |
| Energy, 45 nm | INT8 multiply 0.2 pJ; 32 KB SRAM 20 pJ per 64 bits; DRAM 1.3–2.6 nJ | [1, R-208] |
| Reuse to beat movement (INT8) | about 22 (32 KB SRAM), about 1400 (DRAM) | Example 14-14.4 |
| Quantization SQNR | about 6 dB per bit | §3.5 |
| TPU v4 | 8 × (128 × 128) MXUs, 1050 MHz, 275 TFLOPS, 32 GiB HBM2 at 1200 GB/s | [2, R-222] |
| TPU7x (Ironwood) | 2307 TFLOPS BF16, 4614 FP8, 192 GiB at 7380 GB/s, pods of 9216 | [2, R-222] |
| LLM decoding, batch 1 | about 1 FLOP per byte of BF16 weights | Example 14-14.6 |

## 8. Common mistakes

- **Treating peak TOPS as delivered throughput.** Fill and drain, odd shapes, memory stalls and non-matrix operations lower utilization.
- **Ignoring data movement.** Arithmetic is cheap; fetching operands from DRAM costs over a thousand times more.
- **Quantizing without a scale strategy.** A single per-tensor scale wastes range when values vary across channels; per-channel or block scales fix this.
- **Comparing numbers at different precisions or with sparsity.** FP8 or sparse figures are not comparable with dense BF16 ones.
- **Assuming large-model inference is compute-bound.** At small batch it is bandwidth-bound by two orders of magnitude.
- **Forgetting the rest of the model.** Softmax, normalization and embeddings run on vector units and can dominate once matrix multiplication is fast.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **TPU generations.** TPU v4 (deployed 2020) reached 275 TFLOPS with 1.2 TB/s of HBM2 [2, R-222]. Google's TPU7x (Ironwood) lists 2307 TFLOPS BF16, 4614 FP8 and 192 GiB of HBM at 7380 GB/s per chip, in pods of up to 9216 chips [2, R-222] **[Established]** (vendor specifications).
- **GPUs with tensor cores** remain the most widely used AI accelerators (14-13), with FP4 support on Blackwell (R-221) **[Established]**.
- **Formats keep narrowing**: FP8 is in production, and FP4 and block-scaled MX formats (14-04) are spreading **[Established]**.

### Why it matters commercially

- **Custom silicon economics.** Hyperscalers build accelerators to cut cost per training and inference operation, but only workloads matching the design reach high utilization. The software stack (compilers, kernels) is the long pole.
- **Memory is the bill of materials.** HBM capacity and bandwidth increasingly decide which chip serves large models, and its supply decides how many can be built (Course 23).

### Marketing vs Reality

- **"X POPS."** *Reality:* peak at the narrowest format, often with sparsity, at 100% utilization. *Sanity check:* ask for measured throughput on a named model at a stated precision and batch size.
- **"Up to N× faster than a GPU."** *Reality:* usually on one favourable benchmark. *Sanity check:* ask for a range of models, end-to-end including non-matrix operations and data loading.
- **"Lossless INT4."** *Reality:* accuracy depends on the model, calibration and scale granularity. *Sanity check:* ask for accuracy on your evaluation suite, against BF16.

### Questions for engineering leaders

1. **"What utilization does your array reach on our layer shapes?"**
   *Strong:* measured per-layer utilization, including small and odd shapes. *Evasive:* peak only.
2. **"Where does your memory hierarchy put the weights and activations of our largest model?"**
   *Strong:* a placement plan with bandwidth per level. *Evasive:* "it fits in HBM".
3. **"What precision do you deploy, and what accuracy loss did you measure?"**
   *Strong:* numbers on named benchmarks, with calibration method. *Evasive:* "negligible".
4. **"How is decoding throughput limited on your chip?"**
   *Strong:* bandwidth-bound analysis, batching strategy, measured tokens/s at stated latency. *Evasive:* a TOPS figure.

## 10. Concept check

**Q1.** Why do neural networks suit specialized hardware?

<details><summary>Answer</summary>

They are dominated by one operation (multiply-accumulate) on large matrices with regular, predictable access patterns and high data reuse, and they tolerate low-precision arithmetic.

</details>

**Q2.** Why does a systolic array need skewed inputs?

<details><summary>Answer</summary>

So that $a_{ik}$ and $b_{kj}$ arrive at PE $(i, j)$ in the same cycle ($k + i + j$), as they move one PE per cycle from the edges.

</details>

**Q3.** Why does utilization rise with K?

<details><summary>Answer</summary>

The fill and drain overhead ($M + N - 2$ cycles) is fixed, while the useful work grows with K.

</details>

**Q4.** What does a weight-stationary dataflow optimize?

<details><summary>Answer</summary>

It keeps each weight in a PE and streams many inputs past it, so each weight is fetched once and reused for every input in the batch.

</details>

**Q5.** About how much does each bit of precision buy in SQNR?

<details><summary>Answer</summary>

About 6 dB (a factor of 4 in noise power), following $6.02b + 1.76$ dB for a full-scale sinusoid.

</details>

**Q6.** Why is LLM decoding at batch 1 memory-bound?

<details><summary>Answer</summary>

Each weight is used for one multiply-accumulate per token, about 1 FLOP per byte of BF16 weights, far below accelerators' ridge points of hundreds of FLOP per byte.

</details>

Now work the [problem set](../problems/14-14-problems.md).

## 11. Key terms

[Domain-specific accelerator](../../../reference/glossary.md#domain-specific-accelerator) · [Systolic array](../../../reference/glossary.md#systolic-array) · [Processing element (PE)](../../../reference/glossary.md#processing-element-pe) · [Multiply-accumulate (MAC)](../../../reference/glossary.md#multiply-accumulate-mac) · [Dataflow (accelerator)](../../../reference/glossary.md#dataflow-accelerator) · [Weight-stationary](../../../reference/glossary.md#weight-stationary) · [Output-stationary](../../../reference/glossary.md#output-stationary) · [Quantization (neural networks)](../../../reference/glossary.md#quantization-neural-networks) · [Arithmetic intensity](../../../reference/glossary.md#arithmetic-intensity) · [Ridge point](../../../reference/glossary.md#ridge-point) · [Structured sparsity](../../../reference/glossary.md#structured-sparsity)

## 12. Connections

- **Builds on:** GPUs and tensor cores ([14-13](14-13-gpus-and-simt.md)); caches, reuse and HBM ([14-09](14-09-memory-hierarchy-and-caches.md)); number formats ([14-04](14-04-computer-arithmetic-and-number-formats.md)); quantization noise ([11-10](../../11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md)).
- **Next:** [14-15 The Roofline Model, Benchmarks and How They Are Gamed](14-15-roofline-and-benchmarks.md), which turns ridge points into a general method.
- **Used later:** the memory wall and HBM ([23-01](../../23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md), [23-05](../../23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md)); compute-in-memory ([23-09](../../23-memory-and-storage-technology/chapters/23-09-compute-in-memory.md)); scale-up links ([24-06](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md)).

## 13. Further study

- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, ch. 7 (domain-specific architectures).
- V. Sze, Y.-H. Chen, T.-J. Yang and J. S. Emer, *Efficient Processing of Deep Neural Networks*, Morgan & Claypool, 2020 (dataflows, reuse, energy).
- H. T. Kung, "Why Systolic Architectures?", *IEEE Computer* 15(1), 1982.
- N. P. Jouppi et al., "In-Datacenter Performance Analysis of a Tensor Processing Unit," ISCA 2017, and "TPU v4," ISCA 2023.

## 14. Sources

1. M. Horowitz, "Computing's Energy Problem (and What We Can Do About It)," ISSCC 2014. [R-208](../../../reference/research-log.md#r-208--energy-per-operation-at-45-nm-horowitz-isscc-2014)
2. N. P. Jouppi et al., "TPU v4," ISCA 2023 (arXiv 2304.01433), and Google Cloud's TPU documentation (v5p, v6e, TPU7x). [R-222](../../../reference/research-log.md#r-222--google-tpu-v4-and-later-tpus)
3. Sze, Chen, Yang and Emer, *Efficient Processing of Deep Neural Networks* (the dataflow taxonomy; textbook).

Systolic arrays, dataflows, quantization and the roofline are textbook material (Further study). Every number in the examples is recomputed by the verify script, from the cycle-accurate simulator, the Verilog testbench and the logged specifications.
