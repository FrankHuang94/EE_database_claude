# Problems 14-15 · The Roofline Model, Benchmarks and How They Are Gamed

Chapter: [14-15](../chapters/14-15-roofline-and-benchmarks.md) · Worked solutions: [14-15 solutions](../solutions/14-15-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Machine figures are those of the chapter (H100: 67 TFLOPS FP32, 989.5 TFLOPS dense BF16, 3.35 TB/s; TPU v4: 275 TFLOPS, 1.2 TB/s). FP32 values are 4 bytes and BF16 values 2 bytes. Intensities count main-memory traffic only.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 14-15.1 [A]

**A TPU roofline.** Find TPU v4's ridge point, and the attainable performance of a kernel with an intensity of 50 FLOP/byte.

### Problem 14-15.2 [A]

**Matrix–vector.** A product $y = Ax$ with an $n \times n$ FP32 matrix does $2n^2$ FLOP and, for large $n$, moves essentially only the matrix. What is its intensity, and what does it attain on H100 in FP32?

### Problem 14-15.3 [B]

**Fusion.** Two kernels run in sequence: $z = x + y$, then $w = 2z$, each reading its inputs and writing its output in FP32. A fused kernel computes $w = 2(x + y)$ directly. Find both intensities and the speedup of fusion on a bandwidth-bound machine.

### Problem 14-15.4 [B]

**Narrower data.** SAXPY in BF16 instead of FP32: what is its intensity, what can H100's bandwidth deliver, and what is the speedup?

### Problem 14-15.5 [B]

**A SPEC-style score.** Three benchmarks have reference times of 1000, 2000 and 3000 s and run in 250, 400 and 1000 s. Find the ratios and the score. A SPECrate run of the first benchmark with 16 copies finishes in 400 s; what is its ratio?

### Problem 14-15.6 [B]

**Averaging rates.** A compressor runs at 100 MB/s on one file and 400 MB/s on another of the same size. What is its average rate over both files? Compare the arithmetic mean.

### Problem 14-15.7 [B]

**The reference does not matter.** Machine A runs three programs in 2, 8 and 4 s; machine B in 4, 4 and 4 s. Compute the arithmetic and geometric means of B's times normalized to A, and of A's normalized to B. Which mean gives a consistent verdict?

### Problem 14-15.8 [B]

**Under a latency bound.** A server's latency for a batch of $b$ requests is $10 + 2b$ ms. What is its highest throughput under a 50 ms bound, and its throughput at a batch of 128 with no bound?

### Problem 14-15.9 [C]

**Translating a headline.** Chip X quotes "4000 TOPS" at FP4 with 2:4 sparsity; chip Y quotes 989.5 TFLOPS dense BF16. If sparsity doubles the rate and each halving of precision doubles it, what is X's dense BF16-equivalent rate? Compare the headline ratio with the equivalent ratio.

### Problem 14-15.10 [C]

**The missing denominator.** Accelerator A serves 500 inferences/s at 700 W, and B serves 300/s at 300 W. Compare their throughput and their inferences per joule. How many B's at equal power would match A's power budget, and what throughput would they give?

---

## Objective coverage

| Learning objective (chapter 14-15) | Problems |
|---|---|
| 1. Drawing rooflines and placing kernels | 1, 2 |
| 2. Compute- or memory-bound, and what helps | 2, 3, 4 |
| 3. SPEC ratios and means | 5, 6, 7 |
| 4. SPEC, MLPerf and Geekbench rules | 5, 8 |
| 5. Gamed results and the questions that expose them | 8, 9, 10 |
