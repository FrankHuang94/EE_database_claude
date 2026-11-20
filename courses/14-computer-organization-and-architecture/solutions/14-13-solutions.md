# Solutions 14-13 · GPUs and SIMT

Problems: [14-13 problems](../problems/14-13-problems.md) · Chapter: [14-13](../chapters/14-13-gpus-and-simt.md). Every number below is recomputed by [verify_14_13.py](../verify/verify_14_13.py).

- Efficiencies come from the lab's masked warp executor and are re-derived from lane counts.
- Sectors are checked against min(32, 4 × stride), and bank conflicts against gcd(stride, 32).

---

## Solutions

### Solution 14-13.1

$\lceil 200/32 \rceil$ = **7** warps. The last warp has $200 - 6 \times 32$ = **8** active lanes. Only $200 / 224$ = **89.3**% of the allocated lanes do useful work, which is why block sizes are chosen as multiples of 32.

### Solution 14-13.2

$100 \times 128 \times 2 \times 1.8 \times 10^9$ = **46.08** TFLOPS.

### Solution 14-13.3

The warp runs A (8 lanes), B (8 lanes) and C (16 lanes) one after another: $10 + 10 + 10$ = **30** slots. The useful lane-slots are $8 \times 10 + 8 \times 10 + 16 \times 10 = 320$ of 960, an efficiency of **33.3**%. Each further level of divergence can split the warp again.

### Solution 14-13.4

The trip counts run from 1 to 8, so the warp iterates **8** times. The average trip count is 4.5, so the efficiency is $4.5/8$ = **56.25**%.

### Solution 14-13.5

The first fields are 16 bytes apart, so 32 threads span 512 bytes: **16** sectors, of which only 128 bytes are used, **25**%. As four separate arrays (structure of arrays), the 32 first fields are consecutive: **4** sectors and 100% use. That is the standard reason GPU code prefers structures of arrays.

### Solution 14-13.6

(a) Writes 128 bytes apart touch **32** sectors per warp, against **4** for a coalesced write: 8 times the transactions.

(b) A column of an unpadded tile has stride 32 words, so every lane hits the same bank: **32** passes. With 33 words per row the stride is 33, coprime with 32: **1** pass. The tile costs 32 extra words (3%) of shared memory.

### Solution 14-13.7

The degree is $\gcd(s, 32)$: **1** for a stride of 3, **2** for 6 and **32** for 64. Odd strides never conflict.

### Solution 14-13.8

Each block is 4 warps.

- **128 registers:** registers allow $65536 / (128 \times 128) = 4$ blocks, **16** warps, **25**% occupancy.
- **40 registers:** $65536 / (40 \times 128) = 12.8$, so 12 blocks, **48** warps, **75**%. Registers still limit it, since 16 blocks would fit in the warp slots.

### Solution 14-13.9

(a) $1 + 400/20$ = **21** warps per scheduler, more than the 16 available, so some latency stays exposed.

(b) With two loads in flight, $1 + 400/40$ = **11** warps suffice, and latency is hidden.

### Solution 14-13.10

(a) SAXPY does 2 FLOP per 12 bytes (load $x$, load $y$, store $y$): $3.35 \times 10^{12} \times 2/12$ = **0.558** TFLOPS, under 1% of peak.

(b) $2n^3 / (12 n^2) = n/6$ = **682.7** FLOP/byte, far above the 20 FLOP/byte ridge, so the multiply is compute-bound if the implementation actually achieves near-minimal traffic, by tiling (14-09).

### Solution 14-13.11

Delivered rate: $0.4 \times 989.5$ = **395.8** TFLOPS.

- **One GPU:** $10^{21} / 3.958 \times 10^{14} = 2.53 \times 10^6$ s = **29.2** days.
- **1024 GPUs:** **41.1** minutes, if the scaling were perfect, which it is not (communication, 14-12, 24-06).

Using the sparse headline (1,979 TFLOPS) would make the estimate **2** times too optimistic for a dense model.

### Solution 14-13.12

- **GB200 NVL72:** $13.4 \text{ TB}/72$ = **186.1** GB and $576/72$ = **8** TB/s per GPU.
- **DGX B200:** $1440/8$ = **180** GB and $64/8$ = **8** TB/s per GPU.

The bandwidths agree. The capacities differ slightly, presumably by product configuration; both come from NVIDIA's pages (R-221). Against H100's 3.35 TB/s, the per-GPU bandwidth is **2.39** times higher.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 14-13.1a | warps per block | 7 | — |
| 14-13.1b | active lanes in the last warp | 8 | — |
| 14-13.1c | lanes doing useful work | 89.3 | % |
| 14-13.2a | peak FP32 | 46.08 | TFLOPS |
| 14-13.3a | issue slots | 30 | — |
| 14-13.3b | SIMD efficiency | 33.3 | % |
| 14-13.4a | iterations | 8 | — |
| 14-13.4b | SIMD efficiency | 56.25 | % |
| 14-13.5a | sectors, array of structures | 16 | — |
| 14-13.5b | bytes used | 25 | % |
| 14-13.5c | sectors, structure of arrays | 4 | — |
| 14-13.6a | sectors, naive transpose write | 32 | — |
| 14-13.6b | sectors, coalesced write | 4 | — |
| 14-13.6c | passes, unpadded column | 32 | — |
| 14-13.6d | passes, padded column | 1 | — |
| 14-13.7a | conflict degree, stride 3 | 1 | — |
| 14-13.7b | conflict degree, stride 6 | 2 | — |
| 14-13.7c | conflict degree, stride 64 | 32 | — |
| 14-13.8a | warps, 128 registers | 16 | — |
| 14-13.8b | occupancy, 128 registers | 25 | % |
| 14-13.8c | warps, 40 registers | 48 | — |
| 14-13.8d | occupancy, 40 registers | 75 | % |
| 14-13.9a | warps needed, 20 instructions | 21 | — |
| 14-13.9b | warps needed, 40 instructions | 11 | — |
| 14-13.10a | SAXPY attainable | 0.558 | TFLOPS |
| 14-13.10b | GEMM intensity | 682.7 | FLOP/B |
| 14-13.11a | delivered rate | 395.8 | TFLOPS |
| 14-13.11b | time on one GPU | 29.2 | days |
| 14-13.11c | time on 1024 GPUs | 41.1 | min |
| 14-13.11d | error factor from the sparse figure | 2 | — |
| 14-13.12a | capacity per GPU, NVL72 | 186.1 | GB |
| 14-13.12b | bandwidth per GPU, NVL72 | 8 | TB/s |
| 14-13.12c | capacity per GPU, DGX B200 | 180 | GB |
| 14-13.12d | bandwidth per GPU, DGX B200 | 8 | TB/s |
| 14-13.12e | ratio to H100 bandwidth | 2.39 | — |
