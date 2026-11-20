# Lab 14-13 · GPUs and SIMT

Chapter: [14-13 GPUs and SIMT](../../chapters/14-13-gpus-and-simt.md)

## Objective

Quantify the three ways a GPU kernel loses throughput: divergence within warps, uncoalesced global-memory accesses and shared-memory bank conflicts. Then find what limits occupancy, and how much occupancy is enough to hide memory latency. All without a GPU, using small exact models of the mechanisms.

## Background

SIMT and warps (§3.2), divergence (§3.4), coalescing and banks (§3.5), occupancy and latency hiding (§3.6).

## Tools

Python only. (With access to an NVIDIA GPU, the optional extension measures the same effects for real.)

## Files

- [simt.py](simt.py): `run_warp` and `efficiency` (a masked warp executor for structured branches and loops), `sectors`, `bank_conflict`, `occupancy`, `warps_to_hide`.
- [14-13-simt-lab.ipynb](14-13-simt-lab.ipynb): the notebook (Parts 1–4).

## Procedure

1. **Divergence (Part 1).** Measure the SIMD efficiency of branches on `tid % k` for $k$ = 1, 2, 4, 8, 32, and on the warp index; then of loops with uneven trip counts.
2. **Coalescing (Part 2).** Plot the sectors per warp and the fraction of bytes used against the stride from 1 to 64, and for random addresses.
3. **Bank conflicts (Part 3).** Tabulate the conflict degree for strides 1 to 64 and compare with $\gcd(s, 32)$. *Predict first:* strides 16 and 48.
4. **Occupancy (Part 4).** Sweep registers per thread from 16 to 255 and shared memory per block from 0 to 96 KB, and map the limiting resource.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Divergence | `tid % 2` with equal 10-instruction paths: 50%; a branch on the warp index: 100% |
| 2 | Coalescing | sectors = min(32, 4 × stride); a stride of 3 touches 12 sectors |
| 3 | Banks | conflict degree = gcd(stride, 32); 16 for strides 16 and 48 |
| 4 | Occupancy | with 256-thread blocks and no shared memory, registers become the limit above 32 registers per thread; large shared-memory tiles limit occupancy instead |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 14-13.a | conflict degree, stride 16 | 16 | — |
| Lab 14-13.b | conflict degree, stride 48 | 16 | — |
| Lab 14-13.c | efficiency, tid % 2 branch | 50 | % |
| Lab 14-13.d | sectors, stride 3 | 12 | — |

*These are recomputed by [verify_14_13.py](../../verify/verify_14_13.py).*

## Discussion questions

1. The warp executor runs the `then` side before the `else` side. Does the order matter for efficiency? For correctness?
2. Why does a GPU prefer many simple threads to a few complex ones, given the same transistor budget?
3. When is lower occupancy *better*?

### Answers

1. Not for efficiency: both sides run with their lanes masked, whatever the order. Correctness does not depend on it either for independent threads. But threads that communicate inside divergent code (for example, one waiting on a flag another sets) can deadlock if the waiting side is scheduled first and never yields. Newer GPUs with independent thread scheduling interleave the paths to avoid this.
2. Throughput per watt and per area. Simple in-order lanes spend their energy on arithmetic rather than on prediction and reordering, and the parallelism needed to hide latency comes from threads, which cost only register-file space.
3. When each thread does more independent work. More registers per thread allow more ILP and data reuse in registers (as in tiled matrix multiplication), which can beat higher occupancy. The aim is enough warps to hide latency, not the maximum.

## Optional hardware extension

On a machine with an NVIDIA GPU, write a CUDA kernel that reads an array with a configurable stride and time it for strides 1 to 32; use the profiler (Nsight Compute) to read the sectors per request and the achieved occupancy, and compare with Parts 2 and 4.
