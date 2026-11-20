# Problems 14-14 · AI Accelerators: Systolic Arrays, Dataflow and Low Precision

Chapter: [14-14](../chapters/14-14-ai-accelerators.md) · Worked solutions: [14-14 solutions](../solutions/14-14-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Systolic arrays are output-stationary as in the chapter: an $M \times K$ by $K \times N$ product takes $K + M + N - 2$ cycles, and tiles run one after another unless stated.
- Energies are Horowitz's 45 nm figures as in Example 14-14.4. Quantization is symmetric per tensor, rounding to the nearest integer.
- Accelerator specifications are those of the chapter (R-222, R-220).

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 14-14.1 [A]

**A bigger array.** A matrix unit is a 256 × 256 array clocked at 940 MHz. How many MACs does it perform per cycle, and what is its peak in TFLOPS?

### Problem 14-14.2 [A]

**Timing.** An 8 × 8 array multiplies an 8 × 32 matrix by a 32 × 8 matrix. Find the cycles and the utilization.

### Problem 14-14.3 [A]

**Intensity of a square product.** For an $n \times n$ by $n \times n$ product in BF16 (2 bytes per value), with each matrix moved once, what is the arithmetic intensity? Is $n = 512$ compute-bound on TPU v4 (ridge 229.2 FLOP/byte)? From what $n$ on is it?

### Problem 14-14.4 [B]

**Overlapping tiles.** A 2048 × 512 by 512 × 2048 product runs on a 128 × 128 array. (a) Find the cycles and utilization with tiles run one after another. (b) If consecutive tiles overlap perfectly, so that only the first fill and the last drain are exposed, what are the cycles and utilization?

### Problem 14-14.5 [B]

**Batching pays for weights.** A weight-stationary design fetches each 1-byte weight from DRAM once per batch and uses it for $B$ MACs. Each 1-byte activation comes from a 32 KB SRAM and is reused 128 times across the array. Find the data-movement energy per MAC for $B$ = 1, 16 and 256, and compare it with the 0.23 pJ MAC.

### Problem 14-14.6 [B]

**Quantize by hand.** Quantize $x = (0.5, -1.2, 0.031, 2.54, -2.54, 1.0)$ to INT8. Give the scale, the integers, and the largest error.

### Problem 14-14.7 [B]

**Bits and bytes.** (a) What SQNR does the $6.02b + 1.76$ dB rule give for 6 bits? (b) How large are the weights of a 7-billion-parameter model in BF16, INT8 and INT4?

### Problem 14-14.8 [B]

**Decoding on TPU v5p.** TPU v5p has 459 TFLOPS BF16 and 2765 GB/s per chip. For a 7-billion-parameter model at batch 1, find the token rate with BF16 and with INT8 weights (counting only weight traffic), and the ridge point.

### Problem 14-14.9 [C]

**What sparsity buys.** An accelerator quotes 2000 TFLOPS "with 2:4 sparsity". (a) What is its dense rate? (b) A model pruned 2:4 spends 80% of its time in matrix multiplications. If those run twice as fast, what is the overall speedup?

### Problem 14-14.10 [C]

**Amortizing fill and drain.** On the lab's 4 × 4 array, how many cycles does K = 100 take, and what is the utilization? What K gives 90% utilization?

### Problem 14-14.11 [C]

**A pod-scale training run.** A TPU7x pod has 9216 chips at 2307 TFLOPS BF16. How long does a training run of $10^{25}$ FLOP take at 40% utilization?

### Problem 14-14.12 [C]

**Bandwidth per FLOP.** Rank TPU v4, TPU v5p, TPU7x and H100 (dense BF16 989.5 TFLOPS, 3.35 TB/s) by ridge point. Which is best suited to batch-1 decoding of a model that fits in its memory, and why?

---

## Objective coverage

| Learning objective (chapter 14-14) | Problems |
|---|---|
| 1. Why specialized hardware | 1, 9 |
| 2. Systolic latency, throughput and tiling | 2, 4, 10 |
| 3. Dataflows and reuse | 5 |
| 4. Quantization | 6, 7 |
| 5. Compute- or memory-bound | 3, 8, 11, 12 |
