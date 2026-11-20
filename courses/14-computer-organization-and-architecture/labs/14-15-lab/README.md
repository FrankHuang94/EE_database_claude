# Lab 14-15 · The Roofline Model and Benchmark Arithmetic

Chapter: [14-15 The Roofline Model, Benchmarks and How They Are Gamed](../../chapters/14-15-roofline-and-benchmarks.md)

## Objective

Turn datasheet numbers into expectations. Draw rooflines for the accelerators of Course 14, place the course's kernels on them, and find each kernel's bottleneck. Then recompute benchmark scores with different means, and see how the choice of mean and of reference machine changes the verdict.

## Background

The roofline (§3.1), placing kernels (§3.2), benchmark rules (§3.3) and averaging (§3.4).

## Tools

Python with matplotlib.

## Files

- [roofline.py](roofline.py): machine figures (H100 FP32 and dense BF16, TPU v4, TPU7x; from R-220 and R-222), kernel FLOP and byte counts, `attainable`, `ridge`, `gemm_intensity`, `amean`, `gmean`, `hmean` and `spec_ratio`.
- The chapter's figure is produced by `assets/figures/src/fig_14_15.py` from the same module.

## Procedure

1. **Rooflines (Part 1).** Plot the four machines' rooflines on one log–log chart and mark the kernels. *Predict first:* which machine is fastest for LLM decoding at 1 FLOP/byte?
2. **Bottlenecks (Part 2).** For each kernel and machine, report attainable TFLOPS, the fraction of peak, and the intensity it would need to reach the roof.
3. **Means (Part 3).** Build a table of three machines' times on five programs, normalize to each machine in turn, and compare the arithmetic, geometric and harmonic means.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Decoding at 1 FLOP/byte | TPU7x attains 7.38 TFLOPS, the most of the four, because it has the most bandwidth |
| 2 | Ridges | 20 and about 295 FLOP/byte (H100 FP32, BF16), 229 (TPU v4), about 313 (TPU7x) |
| 3 | Means | the arithmetic mean's ranking can change with the reference machine; the geometric mean's cannot |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 14-15.a | TPU7x attainable at 1 FLOP/byte | 7.38 | TFLOPS |
| Lab 14-15.b | TPU7x ridge | 312.6 | FLOP/B |
| Lab 14-15.c | TPU v4 attainable at 1 FLOP/byte | 1.2 | TFLOPS |

*These are recomputed by [verify_14_15.py](../../verify/verify_14_15.py).*

## Discussion questions

1. A measured kernel sits at 10% of the bandwidth roof. What are the likely causes?
2. Why might a vendor prefer to report SPEC peak rather than base, and why does SPEC make base mandatory?
3. If you could choose one number to compare two accelerators for your workload, what would it be?

### Answers

1. Latency that is not hidden (too little parallelism or occupancy, 14-13), poor access patterns (uncoalesced, strided, TLB misses, 14-09, 14-10), or overheads (synchronization, launches). The roofline says what is possible; the gap is an optimization opportunity.
2. Peak allows per-benchmark tuning and feedback-directed optimization, which raises scores. Base, with uniform flags, is closer to what an ordinary application built with one set of flags would see, and making it mandatory keeps every published result comparable on that footing.
3. Measured throughput on that workload, at the latency and accuracy it needs, per watt or per dollar as the business requires. Any single datasheet number is a proxy for that.

## Optional hardware extension

Measure your own machine's roofline. Time a large vector add (bandwidth) and a large matrix multiply with an optimized library (compute), compute the achieved GB/s and GFLOPS, and compare them with the processor's specifications.
