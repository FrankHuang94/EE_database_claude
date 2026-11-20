# Problems 14-13 · GPUs and SIMT

Chapter: [14-13](../chapters/14-13-gpus-and-simt.md) · Worked solutions: [14-13 solutions](../solutions/14-13-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Warps have 32 threads, numbered by `tid` within the warp.
- Sectors are 32 bytes, and shared memory has 32 banks of 4-byte words.
- The SM of Example 14-13.5 has 65,536 registers, 192 KB of shared memory, 64 warps and 32 blocks.
- H100 figures are from the chapter (R-220).
- Each instruction occupies one issue slot.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 14-13.1 [A]

**Partial warps.** A kernel is launched with blocks of 200 threads. How many warps does a block occupy, how many lanes of its last warp are active, and what fraction of the allocated lanes do useful work?

### Problem 14-13.2 [A]

**Peak arithmetic.** A GPU has 100 SMs of 128 FP32 lanes, each completing one fused multiply-add per cycle at 1.8 GHz. What is its peak FP32 rate?

### Problem 14-13.3 [B]

**Nested divergence.** In a warp, threads with `tid < 8` run path A, threads with `8 <= tid < 16` path B (both inside `if (tid < 16)`), and the rest path C. Each path is 10 instructions. Find the issue slots and the SIMD efficiency.

### Problem 14-13.4 [B]

**Uneven loops.** Each thread loops `tid % 8 + 1` times over a 1-instruction body. Find the warp's iterations and its SIMD efficiency.

### Problem 14-13.5 [B]

**Arrays of structures.** Each element is a structure of four floats (16 bytes) and each thread reads only the first field of element `tid`. How many sectors does the warp touch, and what fraction of the fetched bytes is used? What if the fields are stored as four separate arrays?

### Problem 14-13.6 [B]

**A transpose through shared memory.** A naive transpose writes `out[j][i] = in[i][j]` for a 32 × 32 tile of floats, so a warp's writes are 128 bytes apart. (a) How many sectors does one warp's write touch, against a coalesced write? (b) Staging the tile in shared memory, a warp reads one column of an unpadded 32 × 32 tile. How many passes does it take, and with a padded tile (33 words per row)?

### Problem 14-13.7 [B]

**More strides.** Find the shared-memory conflict degree for word strides of 3, 6 and 64.

### Problem 14-13.8 [B]

**Register pressure.** A kernel uses 128-thread blocks and no shared memory. Find the resident warps and the occupancy with 128 registers per thread and with 40.

### Problem 14-13.9 [B]

**Enough warps?** Memory latency is 400 cycles and each scheduler can have at most 16 warps. How many warps does a scheduler need if a warp issues 20 instructions between dependent loads, and is latency hidden? What if each warp keeps two independent loads in flight (40 instructions between waits)?

### Problem 14-13.10 [C]

**Memory-bound or not?** On H100 (67 TFLOPS FP32, 3.35 TB/s):

- (a) What can SAXPY ($y \leftarrow a x + y$, FP32) attain?
- (b) A square FP32 matrix multiply of size $n = 4096$ does $2n^3$ FLOP and must move at least $3n^2$ values of 4 bytes. What is its arithmetic intensity in that best case, and which side of the ridge point is it on?

### Problem 14-13.11 [C]

**Days of training.** A training run needs $10^{21}$ FLOP in BF16. Each H100 delivers 40% of its *dense* tensor rate. How long does the run take on one GPU and on 1024 GPUs (assuming perfect scaling)? How far off would an estimate from the sparse headline figure be?

### Problem 14-13.12 [C]

**Reading a rack specification.** From the GB200 NVL72 figures (72 GPUs, 13.4 TB of HBM3E, 576 TB/s) and the DGX B200 figures (8 GPUs, 1,440 GB, 64 TB/s), derive the per-GPU capacity and bandwidth from each. By what factor does the per-GPU bandwidth exceed H100's?

---

## Objective coverage

| Learning objective (chapter 14-13) | Problems |
|---|---|
| 1. Throughput design, SIMD and SIMT | 1, 2 |
| 2. Divergence and SIMD efficiency | 3, 4 |
| 3. Coalescing and bank conflicts | 5, 6, 7 |
| 4. Occupancy and latency hiding | 8, 9 |
| 5. Peak figures and attainable performance | 10, 11, 12 |
