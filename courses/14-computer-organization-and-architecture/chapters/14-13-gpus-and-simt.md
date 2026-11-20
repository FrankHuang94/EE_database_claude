<!-- status: verified -->
# 14-13 · GPUs and SIMT

| | |
|---|---|
| **Course** | [14 · Computer Organization and Architecture](../README.md) |
| **University equivalent** | The data-level-parallelism material of a computer architecture course: SIMD and vector machines, the GPU execution model (warps, SIMT, divergence), the GPU memory hierarchy (coalescing, shared-memory banks), occupancy and latency hiding, and tensor cores (Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*, ch. 4; Kirk & Hwu, *Programming Massively Parallel Processors*) |
| **Prerequisites** | [14-12 Multicore, Coherence and Memory Consistency](14-12-multicore-coherence-consistency.md), [14-09 Memory Hierarchy and Caches](14-09-memory-hierarchy-and-caches.md) (Little's law, bandwidth), [14-04 Computer Arithmetic and Number Formats](14-04-computer-arithmetic-and-number-formats.md) (low-precision formats) |
| **Estimated study hours** | 7 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Contrast latency-oriented CPU cores with throughput-oriented GPUs, and SIMD vector instructions with the SIMT model of warps and threads.
2. Compute the SIMD efficiency of divergent branches and loops in a warp.
3. Count the memory sectors a warp's access touches and the shared-memory bank conflicts it causes, and fix both by changing the access pattern.
4. Compute an SM's occupancy from its resource limits, and the warps needed to hide memory latency, using Little's law.
5. Relate a GPU's peak compute and memory bandwidth (and the dense and sparse tensor-core figures) to the performance a kernel can actually reach.

---

## 1. Big picture

A CPU core spends most of its transistors on making *one* thread fast: branch prediction, out-of-order windows, large caches (14-07 to 14-09). A **GPU** spends them on arithmetic units and on *many* threads. It runs tens of thousands of threads at once, switches between them every cycle to hide memory latency, and executes groups of threads in lockstep so that one instruction fetch and decode serves 32 arithmetic lanes. The result is an order of magnitude more arithmetic throughput and memory bandwidth than a CPU of similar power, for programs with enough parallel work: graphics, scientific simulation and, above all, the matrix multiplications of AI.

- **GPUs dominate AI training and much of inference.** NVIDIA's H100 has 132 streaming multiprocessors, 16,896 FP32 lanes, 528 tensor cores and 80 GB of HBM3 at 3.35 TB/s [1, R-220].
- **Throughput comes from hiding latency, not avoiding it.** A GPU tolerates hundreds of cycles of memory latency by having other warps ready to run.
- **The programming model leaks.** Divergent branches, uncoalesced accesses and bank conflicts can cost factors of 2 to 32, and the programmer controls them.

## 2. Intuition first

**A rowing eight.** Thirty-two rowers in one long boat follow one coxswain's calls, so a single command moves 32 oars. That is SIMD: one instruction, many data. If the coxswain calls "port side only," the starboard rowers sit idle for that stroke. That is **divergence**. The boat is fast only when everyone rows the same stroke.

**A busy restaurant kitchen with many tables.** A waiter (the scheduler) does not stand at one table waiting for the kitchen. They serve whichever table is ready, so the kitchen's 20-minute cooking time (memory latency) is hidden as long as there are enough tables (warps) in progress. That is latency hiding by **occupancy**.

**Where the analogies break.** A GPU's "rowers" are threads with their own registers and their own program counters in principle. The hardware groups them into warps dynamically, and recent GPUs can even schedule diverged paths independently. And memory is not a kitchen: the order in which 32 threads ask for data decides whether one transaction or 32 are needed.

## 3. Theory

### 3.1 Latency against throughput

A CPU's design goal is the shortest time for one thread; a GPU's is the most work per second across many threads. By Little's law (14-08, 14-09), the parallelism needed to keep a machine busy is throughput × latency. A GPU that wants thousands of operations in flight per cycle, against memory latencies of hundreds of cycles, needs hundreds of thousands of independent operations. It gets them from threads, not from out-of-order windows. Each thread is simple and in order, and the hardware interleaves many.

### 3.2 SIMD and SIMT

**SIMD** (single instruction, multiple data) machines apply one instruction to a vector of elements: x86 AVX, Arm SVE, the RISC-V V extension. The program sees vector registers and explicit vector instructions.

GPUs use **SIMT** (single instruction, multiple threads). The programmer writes a *scalar* program for one thread (a **kernel**) and launches it over a **grid** of thread **blocks**. The hardware groups 32 consecutive threads of a block into a **warp**, which shares one program counter and issues one instruction for all 32 **lanes** at a time. Each lane has its own registers and computes on its own data.

When the threads of a warp disagree at a branch, the warp executes both paths one after the other, with an **active mask** disabling the lanes not on the current path, and reconverges afterwards. Correctness is automatic; efficiency is not.

### 3.3 GPU organization

A GPU is an array of **streaming multiprocessors (SMs)**. Each SM has:

- several warp schedulers, each issuing an instruction from a ready warp every cycle;
- arithmetic lanes (FP32, INT32, FP64), special-function units, load/store units and tensor cores;
- a very large **register file**, which holds the registers of every resident thread, so switching warps costs nothing;
- **shared memory**, a software-managed scratchpad shared by a block's threads and combined with the L1 cache.

All SMs share an L2 cache and the HBM memory. NVIDIA's H100 SXM, for example, has 132 SMs with 128 FP32 lanes and 4 tensor cores each, 256 KB of combined L1 and shared memory per SM, a 50 MB L2, and 80 GB of HBM3 in 5 stacks at 3.35 TB/s [1, R-220].

### 3.4 Divergence

A warp's **SIMD efficiency** is the fraction of lane-slots doing useful work:

$$
\eta = \frac{\sum_\text{issued instructions} (\text{active lanes})}{32 \times \text{issued instructions}}.
$$

- **Branches.** An `if` whose condition differs within a warp costs the sum of both paths' lengths. One whose condition is uniform across the warp costs only the path taken. Branching on `warp_id` is free; branching on `thread_id % 2` halves the throughput.
- **Loops.** A loop with per-thread trip counts runs for the *maximum* trip count in the warp. Lanes that have finished sit masked off.

The remedies are to make conditions uniform within a warp (sort or bin the work), or to replace branches with arithmetic (predication, `select`).

### 3.5 Memory: coalescing and bank conflicts

**Coalescing.** A warp's 32 loads are serviced together. The memory system moves data in **sectors** of 32 bytes (and cache lines of 128 bytes), so the cost of an access is the number of distinct sectors the 32 addresses touch:

- consecutive 4-byte elements (stride 1) touch 4 sectors: one 128-byte line, 100% of the bytes used;
- a stride of 2 elements touches 8 sectors, 50% used;
- a stride of 8 or more elements touches 32 sectors, one per thread, 12.5% used.

Structure-of-arrays layouts, in which consecutive threads read consecutive elements, coalesce; arrays of structures usually do not.

**Shared-memory bank conflicts.** Shared memory is divided into 32 **banks** of 4-byte words; word $w$ lives in bank $w \bmod 32$. A warp's access completes in one pass if every lane touches a different bank (or the same word). If $d$ lanes touch different words in one bank, the access serializes into $d$ passes. For a stride of $s$ words, the conflict degree is $\gcd(s, 32)$:

- stride 1: no conflict;
- stride 2: 2-way;
- stride 32, such as reading a column of a 32 × 32 tile: 32-way.

Padding each row to 33 words makes the column stride 33, which is coprime with 32, so the conflict disappears.

> **Math refresher — gcd and modular strides.** The lanes $i = 0 \ldots 31$ access banks $s\,i \bmod 32$. Two lanes $i \ne j$ collide when $s(i - j) \equiv 0 \pmod{32}$, which happens for $|i - j|$ a multiple of $32/\gcd(s, 32)$. The 32 lanes therefore fall into $32/\gcd(s,32)$ banks, $\gcd(s,32)$ lanes per bank.

### 3.6 Occupancy and latency hiding

An SM holds as many warps as its resources allow. Each thread needs registers, each block needs shared memory, and the SM has a maximum number of resident warps and blocks. **Occupancy** is the number of resident warps divided by the maximum. The limiting resource is whichever runs out first (Example 14-13.5).

Occupancy matters because it supplies the latency hiding. Suppose each warp issues $k$ independent instructions and then waits $L$ cycles for memory. A scheduler issuing one instruction per cycle stays busy only if it has

$$
N \ge 1 + \frac{L}{k}
$$

warps to choose from (Little's law again). Kernels with long memory latencies and little work between loads need high occupancy. Kernels with more independent work per thread (instruction-level parallelism, several loads in flight per thread) need less.

### 3.7 Tensor cores and low precision

Matrix multiplication dominates AI. **Tensor cores** are units that perform a small matrix multiply-accumulate (a tile product such as $D = AB + C$) per instruction, in low-precision formats: FP16, BF16, FP8 and, on newer parts, FP4 (14-04). The gain is large because each operand fetched from a register feeds many multiplications.

On H100, the dense BF16 tensor rate is about 989.5 TFLOPS, against 67 TFLOPS for ordinary FP32 lanes [1, R-220].

Vendors often quote tensor throughput **with sparsity**. NVIDIA's "fine-grained structured sparsity" lets the hardware skip zeros in matrices pruned to a 2:4 pattern, "doubling the performance of standard Tensor Core operations" [1, R-220]. Dense workloads see half the headline figure. H100's product page footnotes its tensor numbers "With sparsity", and the Blackwell pages note that "Dense is one-half sparse spec shown" [2, R-221].

### 3.8 The programming model and its memory model

A CUDA-style kernel is launched over a grid. Threads within a block can synchronize (a barrier) and share data through shared memory. Blocks are independent and may run in any order on any SM. GPU caches are not kept coherent the way CPU caches are (14-12): communication between blocks goes through global memory with explicit atomic operations and memory fences. This weaker contract is part of what lets GPUs scale to thousands of threads.

### 3.9 The lab's models

The lab's `simt.py` contains small exact models:

- a warp executor for structured branches and loops with an active mask, counting issue slots and useful lane-slots;
- sector counting for a warp's addresses;
- bank-conflict counting for shared memory;
- an occupancy calculator;
- the latency-hiding estimate.

The verify script cross-checks each against closed forms: SIMD efficiencies from lane counts, sectors from strides, conflict degrees from $\gcd(s, 32)$.

## 4. Worked examples

### Example 14-13.1 · What the peak numbers mean (tier A)

**Setup.** H100 SXM has 132 SMs with 128 FP32 lanes each, and NVIDIA quotes 67 TFLOPS of FP32 and 1,979 TFLOPS of BF16 tensor throughput "with sparsity" [1, R-220]. (a) How many FP32 lanes are there, and what clock does the FP32 figure imply if each lane does one fused multiply-add (2 FLOP) per cycle? (b) What is the dense BF16 rate, and how many times the FP32 rate is it?

**Solution.**

(a) $132 \times 128$ = **16,896** lanes. The FP32 figure implies $67 \times 10^{12} / (16{,}896 \times 2)$ = **1.98** GHz. NVIDIA's page states no clock, so this is an inference.

(b) Dense is half the sparse figure: **989.5** TFLOPS, **14.8** times the FP32 lanes.

**Units check.** FLOP/s ÷ (lanes × FLOP/cycle) = cycles/s.

**Sanity check.** Tensor cores win by an order of magnitude because each operand feeds many multiplications, and because their BF16 multipliers are much smaller than FP32 ones (14-04).

### Example 14-13.2 · Divergence (tier B)

**Setup.** In a 32-thread warp, (a) threads with `tid % 4 == 0` run a 20-instruction path and the others a 10-instruction path; (b) threads with `tid < 16` do the same; (c) each thread runs a loop of `tid` iterations of one instruction. Find the issue slots and SIMD efficiency in each case.

**Solution.**

(a) Both paths are taken, so the warp issues $20 + 10$ = **30** slots. Useful lane-slots: $8 \times 20 + 24 \times 10 = 400$ of $30 \times 32 = 960$, an efficiency of **41.7**%.

(b) Again 30 slots; useful $16 \times 20 + 16 \times 10 = 480$, or **50**%.

(c) The warp runs the longest loop, **31** iterations. Useful work is $0 + 1 + \cdots + 31 = 496$ lane-iterations of $31 \times 32 = 992$: **50**%.

**Units check.** Lane-slots are lanes × issue slots.

**Sanity check.** If the condition in (a) were on the warp index instead, each warp would take one path only, at 100% efficiency. The total work is the same; only its grouping changes.

### Example 14-13.3 · Coalescing (tier B)

**Setup.** A warp's 32 threads load 4-byte floats from addresses base + 4 × stride × tid. How many 32-byte sectors does the access touch, and what fraction of the fetched bytes is used, for strides of 1, 2 and 32 elements?

**Solution.** The warp uses 128 bytes in every case.

- Stride 1: the addresses span 128 consecutive bytes, **4** sectors, **100**% used.
- Stride 2: they span 256 bytes, **8** sectors, **50**% used.
- Stride 32: each thread is 128 bytes from the next, a different sector each: **32** sectors, 1024 bytes fetched for 128 used, **12.5**%.

**Units check.** Sectors × 32 bytes = bytes fetched.

**Sanity check.** Reading a column of a row-major matrix is the stride-32 case. Transposing through shared memory, reading rows and writing columns there, turns it into coalesced accesses (Problem 14-13.6).

### Example 14-13.4 · Shared-memory bank conflicts (tier B)

**Setup.** A warp reads 4-byte words at word indices $s \times \text{tid}$ from shared memory (32 banks). Find the number of serialized passes for $s$ = 1, 2, 32 and 33.

**Solution.** The passes equal the conflict degree $\gcd(s, 32)$:

- $s = 1$: **1** pass;
- $s = 2$: **2**;
- $s = 32$: **32**, with every lane in bank 0;
- $s = 33$: **1**.

Padding a 32-word row to 33 words turns a column read from 32 passes into 1.

**Units check.** Passes are counts.

**Sanity check.** With $s = 33$, lane $i$ uses bank $33i \bmod 32 = i \bmod 32$, a different bank per lane.

### Example 14-13.5 · Occupancy (tier B)

**Setup.** An SM has 65,536 registers, 192 KB of shared memory, and room for 64 warps and 32 blocks. A kernel uses 256-thread blocks with 32 KB of shared memory per block. Find the resident warps, occupancy and limiting resource with 64 registers per thread, and with 32.

**Solution.** Each block is 8 warps.

- **64 registers per thread:** registers allow $65536 / (64 \times 256)$ = 4 blocks; shared memory allows $196608 / 32768$ = 6; warp slots allow 8. Registers limit it to 4 blocks = **32** warps, **50**% occupancy.
- **32 registers per thread:** registers allow 8 blocks, so shared memory (6 blocks) now limits: **48** warps, **75**%.

**Units check.** Blocks × warps per block = warps.

**Sanity check.** Lowering register use raised occupancy until another resource took over. Beyond that, only less shared memory per block helps.

### Example 14-13.6 · Hiding latency and hitting the memory wall (tier C)

**Setup.** (a) Memory latency is 500 cycles and a warp issues 10 instructions between dependent loads. How many warps does one scheduler need? With 64 warps shared by 4 schedulers, is that achievable? What if the code is restructured so that 4 independent loads are in flight per warp (40 instructions between waits)? (b) On H100 (67 TFLOPS FP32, 3.35 TB/s), where is the ridge point in FLOP per byte, and what fraction of peak can a vector add $z = x + y$ in FP32 reach?

**Solution.**

(a) $N \ge 1 + 500/10$ = **51** warps per scheduler, but each scheduler has at most $64/4 = 16$. Latency is exposed and the SM idles most of the time. With 4 loads in flight per warp, $1 + 500/40 = 13.5$, so **14** warps suffice: instruction-level parallelism substitutes for occupancy.

(b) The ridge is $67 \times 10^{12} / 3.35 \times 10^{12}$ = **20** FLOP/byte. A vector add does 1 FLOP per 12 bytes (two 4-byte loads, one store), so memory limits it to $3.35 \times 10^{12} / 12$ = **0.279** TFLOPS, **0.42**% of peak. For dense BF16 tensor work the ridge is $989.5 / 3.35$ = **295** FLOP/byte, which is why AI kernels must reuse every byte hundreds of times (14-14, 14-15).

**Units check.** (FLOP/s)/(B/s) = FLOP/B.

**Sanity check.** A GPU's arithmetic is so cheap relative to its bandwidth that most simple kernels are memory-bound; peak FLOPS is reached only by tiled matrix work.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 14-13.1a | FP32 lanes | 16896 | — |
| Ex 14-13.1b | implied clock | 1.98 | GHz |
| Ex 14-13.1c | dense BF16 tensor rate | 989.5 | TFLOPS |
| Ex 14-13.1d | ratio to FP32 | 14.8 | — |
| Ex 14-13.2a | issue slots, tid % 4 | 30 | — |
| Ex 14-13.2b | efficiency, tid % 4 | 41.7 | % |
| Ex 14-13.2c | efficiency, tid < 16 | 50 | % |
| Ex 14-13.2d | loop iterations | 31 | — |
| Ex 14-13.2e | efficiency, loop | 50 | % |
| Ex 14-13.3a | sectors, stride 1 | 4 | — |
| Ex 14-13.3b | bytes used, stride 1 | 100 | % |
| Ex 14-13.3c | sectors, stride 2 | 8 | — |
| Ex 14-13.3d | bytes used, stride 2 | 50 | % |
| Ex 14-13.3e | sectors, stride 32 | 32 | — |
| Ex 14-13.3f | bytes used, stride 32 | 12.5 | % |
| Ex 14-13.4a | passes, stride 1 | 1 | — |
| Ex 14-13.4b | passes, stride 2 | 2 | — |
| Ex 14-13.4c | passes, stride 32 | 32 | — |
| Ex 14-13.4d | passes, stride 33 | 1 | — |
| Ex 14-13.5a | warps, 64 registers | 32 | — |
| Ex 14-13.5b | occupancy, 64 registers | 50 | % |
| Ex 14-13.5c | warps, 32 registers | 48 | — |
| Ex 14-13.5d | occupancy, 32 registers | 75 | % |
| Ex 14-13.6a | warps needed, 10 instructions | 51 | — |
| Ex 14-13.6b | warps needed, 40 instructions | 14 | — |
| Ex 14-13.6c | FP32 ridge point | 20 | FLOP/B |
| Ex 14-13.6d | vector-add attainable | 0.279 | TFLOPS |
| Ex 14-13.6e | fraction of FP32 peak | 0.42 | % |
| Ex 14-13.6f | BF16 dense ridge point | 295 | FLOP/B |

## 5. Simulate it

The lab, [labs/14-13-lab](../labs/14-13-lab/README.md), provides `simt.py`. In the notebook you:

1. **Measure divergence** for branch conditions on `tid` and on the warp index, and for loops with uneven trip counts.
2. **Count sectors** for strided and random accesses, and plot efficiency against stride.
3. **Map bank conflicts** for strides 1 to 64 and check them against $\gcd(s, 32)$.
4. **Explore occupancy** by sweeping registers per thread and shared memory per block.

**Guided exercise (predict, then run).** **Before Part 3,** predict the conflict degree for a stride of 16 words and for a stride of 48. (16 and 16: $\gcd(16, 32) = \gcd(48, 32) = 16$.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| More SMs and lanes | Peak throughput | Die area, power; needs more parallelism and bandwidth | GPU architect |
| Register file size | Occupancy, latency hiding | Area and access energy (the largest SRAM on an SM) | GPU architect |
| Shared memory against L1 split | Programmer-managed reuse against automatic caching | Programming effort | Architect; kernel developer per kernel |
| Tensor cores and low precision | Throughput per watt on matrix math | Accuracy management, generality | Architect, ML framework teams |
| Structured sparsity | Up to 2× tensor throughput | Requires pruned models; headline numbers mislead | Architect, model developers |
| Threads per block, registers per thread | Occupancy against per-thread ILP | Tuning effort; spills when too few registers | Kernel developer |
| HBM stacks | Bandwidth, capacity | Cost, power, packaging (14-09, Course 23) | Product architect |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Warp | 32 threads | NVIDIA |
| Shared memory | 32 banks of 4 bytes; conflict degree $\gcd(s, 32)$ | §3.5 |
| Sector / line | 32 bytes / 128 bytes | §3.5 |
| Warps to hide latency | $1 + L/k$ per scheduler | §3.6 |
| H100 SXM | 132 SMs, 16,896 FP32 lanes, 528 tensor cores, 50 MB L2, 80 GB HBM3 at 3.35 TB/s, up to 700 W | [1, R-220] |
| H100 SXM throughput | FP32 67 TFLOPS; BF16 tensor 1,979 sparse (989.5 dense) | [1, R-220] |
| Blackwell (GB200 NVL72) | 72 GPUs, 13.4 TB HBM3E at 576 TB/s per rack; about 8 TB/s per GPU | [2, R-221] |

## 8. Common mistakes

- **Comparing sparse and dense numbers.** Tensor-core headlines are often "with sparsity", twice the dense rate.
- **Ignoring divergence.** Data-dependent branches on thread IDs can halve or quarter throughput.
- **Uncoalesced access.** Strided or array-of-structures layouts can waste up to 7/8 of memory bandwidth.
- **Chasing occupancy blindly.** Occupancy hides latency, but beyond what is needed it only adds register pressure; ILP is an alternative.
- **Expecting peak FLOPS from simple kernels.** Element-wise operations are memory-bound by a factor of tens to hundreds.
- **Assuming CPU-style coherence.** Blocks cannot see each other's writes without explicit atomics and fences.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Hopper (H100).** 132 SMs, 80 GB HBM3 at 3.35 TB/s, up to 700 W; 1,979 TFLOPS BF16 tensor with sparsity, half that dense [1, R-220] **[Established]**.
- **Blackwell.** NVIDIA's GB200 NVL72 rack joins 72 Blackwell GPUs with 13.4 TB of HBM3E at 576 TB/s, about 8 TB/s per GPU, and quotes tensor rates in FP4 [2, R-221] **[Established]** (vendor specifications).
- **Low precision keeps falling.** Each generation adds a narrower tensor format: FP8 on Hopper, FP4 on Blackwell [1, 2, R-220, R-221] **[Established]**.

### Why it matters commercially

- **AI compute is GPU-shaped.** Data-centre capital spending on AI is largely spending on GPUs, HBM and the networks between them. The figures that decide value are delivered tokens or FLOPs per dollar and per watt, not peak TFLOPS.
- **The software moat.** Kernel libraries tuned for coalescing, occupancy and tensor cores are as much a part of a GPU's value as its silicon.

### Marketing vs Reality

- **"X PFLOPS."** *Reality:* usually sparse, at the narrowest format, at peak clock. *Sanity check:* ask for dense throughput at the precision your model uses, and measured utilization on your workload.
- **"Y TB/s of memory bandwidth."** *Reality:* achieved bandwidth on real kernels is lower, and many kernels are bandwidth-bound. *Sanity check:* ask for a roofline of key kernels.

### Questions for engineering leaders

1. **"What utilization (MFU) do you reach on our model, at which precision?"**
   *Strong:* measured model-FLOPs utilization with the precision stated. *Evasive:* the peak figure.
2. **"Which kernels are memory-bound, and what is your plan for them?"**
   *Strong:* roofline placement, fusion and tiling plans. *Evasive:* "the next GPU is faster".
3. **"How do you handle divergence-heavy or sparse workloads?"**
   *Strong:* specific restructuring (binning, compaction), measured efficiency. *Evasive:* "the hardware handles it".
4. **"What does sparsity buy on our models in practice?"**
   *Strong:* accuracy and speed with 2:4 pruning, measured. *Evasive:* the doubled headline.

## 10. Concept check

**Q1.** How does SIMT differ from SIMD?

<details><summary>Answer</summary>

SIMD exposes vector registers and vector instructions to the program. SIMT lets the programmer write scalar per-thread code, which the hardware groups into warps that share an instruction stream, using masks to handle divergence.

</details>

**Q2.** Why does divergence cost throughput?

<details><summary>Answer</summary>

A warp issues one instruction for all its lanes. When threads take different paths, the warp executes each path in turn with the other lanes masked off, so lane-slots go unused.

</details>

**Q3.** What makes a warp's memory access coalesced?

<details><summary>Answer</summary>

Consecutive threads accessing consecutive addresses, so that the 32 accesses fall into as few 32-byte sectors (128-byte lines) as possible.

</details>

**Q4.** Why does padding a shared-memory tile by one word remove bank conflicts on column reads?

<details><summary>Answer</summary>

It changes the stride from 32 words, which maps every row to the same bank, to 33, which is coprime with 32, so consecutive rows fall in consecutive banks.

</details>

**Q5.** Why does a GPU need high occupancy?

<details><summary>Answer</summary>

To hide memory latency: while some warps wait for memory, the scheduler needs other ready warps. By Little's law, the number needed is about one plus the latency divided by the instructions issued between waits.

</details>

**Q6.** Why are most element-wise kernels far below peak FLOPS?

<details><summary>Answer</summary>

They do one or two operations per element loaded, far below the ridge point (tens of FLOP per byte for FP32 on H100), so memory bandwidth, not arithmetic, limits them.

</details>

Now work the [problem set](../problems/14-13-problems.md).

## 11. Key terms

[Graphics processing unit (GPU)](../../../reference/glossary.md#graphics-processing-unit-gpu) · [SIMT](../../../reference/glossary.md#simt) · [Warp](../../../reference/glossary.md#warp) · [Streaming multiprocessor (SM)](../../../reference/glossary.md#streaming-multiprocessor-sm) · [Kernel (GPU)](../../../reference/glossary.md#kernel-gpu) · [Branch divergence](../../../reference/glossary.md#branch-divergence) · [Memory coalescing](../../../reference/glossary.md#memory-coalescing) · [Shared memory (GPU)](../../../reference/glossary.md#shared-memory-gpu) · [Bank conflict](../../../reference/glossary.md#bank-conflict) · [Occupancy](../../../reference/glossary.md#occupancy) · [Tensor core](../../../reference/glossary.md#tensor-core) · [Structured sparsity](../../../reference/glossary.md#structured-sparsity)

## 12. Connections

- **Builds on:** multicore and memory models ([14-12](14-12-multicore-coherence-consistency.md)); caches, bandwidth and HBM ([14-09](14-09-memory-hierarchy-and-caches.md)); low-precision formats ([14-04](14-04-computer-arithmetic-and-number-formats.md)).
- **Next:** [14-14 AI Accelerators](14-14-ai-accelerators.md), which specializes even further for matrix math.
- **Used later:** rooflines and benchmarks ([14-15](14-15-roofline-and-benchmarks.md)); HBM in depth ([23-05](../../23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md)); scale-up links between GPUs ([24-06](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md)).

> **Deeper:** see companion repo *LLM Inference Engineering* for GPU kernels and serving at scale.

## 13. Further study

- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, ch. 4 (data-level parallelism in vector, SIMD and GPU architectures).
- D. B. Kirk and W. W. Hwu, *Programming Massively Parallel Processors* (coalescing, shared memory, occupancy).
- NVIDIA, *CUDA C++ Programming Guide* and *CUDA C++ Best Practices Guide* (the programming model, memory hierarchy and performance guidelines).
- E. Lindholm, J. Nickolls, S. Oberman and J. Montrym, "NVIDIA Tesla: A Unified Graphics and Computing Architecture," *IEEE Micro* 28(2), 2008 (the SIMT design).

## 14. Sources

1. NVIDIA, "NVIDIA H100 Tensor Core GPU" product page, and "NVIDIA Hopper Architecture In-Depth" (NVIDIA Technical Blog, Mar 2022). [R-220](../../../reference/research-log.md#r-220--nvidia-h100-hopper-specifications)
2. NVIDIA, GB200 NVL72 and DGX B200 product pages. [R-221](../../../reference/research-log.md#r-221--nvidia-blackwell-systems-gb200-nvl72-dgx-b200)

SIMT execution, coalescing, bank conflicts, occupancy and latency hiding are textbook material (Further study). Every number in the examples is recomputed by the verify script, from the lab's models and independent closed forms.
