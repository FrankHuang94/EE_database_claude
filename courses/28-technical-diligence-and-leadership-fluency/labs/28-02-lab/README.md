# Lab 28-02 · Restating Claims on a Common Basis

**Objective.** Use small first-principles models to see how far delivered throughput sits below a headline, how efficiency moves with the operating point, how a best-of-N headline inflates a typical result, and how respins stretch a tape-out-to-production schedule.

**Chapter:** [28-02 · Validating Claims: TOPS/W, Benchmarks, Tapeout Status](../../chapters/28-02-validating-claims.md)

## Background

The lab uses the chapter's models with its assumed parameters:

- §3.1: peak throughput $2N_{\text{MAC}}f \cdot k_{\text{prec}} \cdot k_{\text{sparse}}$ and the roofline $\min(F_{\text{peak}}, IB)$.
- §3.2–3.3: energy per operation, dynamic power $\propto V^2f$ and power at successive boundaries.
- §3.4: geometric means and the expected best of $N$ workloads, $m\,e^{\sigma \operatorname{E}[Z_{(N)}]}$.
- §3.5: the tape-out-to-production sum.

## Files

- `claimcheck.py`: the models and the chapter's constants (Example 28-02.1's NPU, the 45 nm energies of [R-208], HBM2's 3.9 pJ/bit [R-459]).
- `28-02-claims-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · The roofline under the headline** (notebook). *Predict* the attainable throughput and utilization of Example 28-02.1's NPU (78.6 TOPS dense INT8) with 64 GB/s of memory bandwidth (assumed) at 300 operations per byte. Then plot the roofline from 1 to 10,000 operations per byte, with the dense peak and the 157 TOPS headline.

**Part 2 · Along the voltage–frequency line** (notebook). *Predict* the throughput, power and efficiency of Example 28-02.3's chip at 0.75 V and 700 MHz. Then plot throughput and efficiency for operating points from (0.60 V, 400 MHz) to (0.90 V, 1.0 GHz), taking frequency linear in voltage.

**Part 3 · Best of twenty** (notebook). *Predict* the expected best-of-twenty headline for a product whose per-workload log speedups have median 1.5× and standard deviation 0.3. Then simulate 20,000 vendors, each reporting its best of 20 workloads, and compare the mean with the formula.

**Part 4 · A metal-only respin** (notebook). *Predict* Example 28-02.6's time to production if the respin is metal-only from held wafers (2 weeks of masks and 6 of fab, both assumed because no quantified data were found [R-648], then packaging and test). Then plot time to production against the number of respins, 0 to 3, for metal-only and full-layer respins.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 28-02.a | ridge point | 1229 | ops/byte |
| Lab 28-02.a1 | attainable at 300 ops/byte | 19.2 | TOPS |
| Lab 28-02.a2 | utilization | 24.4 | % |
| Lab 28-02.b | throughput at 0.75 V, 700 MHz | 140 | TOPS |
| Lab 28-02.b1 | power | 10.9 | W |
| Lab 28-02.b2 | efficiency | 12.8 | TOPS/W |
| Lab 28-02.c | expected maximum of 20 normals | 1.87 | — |
| Lab 28-02.c1 | expected best of twenty | 2.63 | — |
| Lab 28-02.d | time with a metal-only respin | 55.0 | weeks |
| Lab 28-02.d1 | time with a metal-only respin | 12.6 | months |

## Discussion

1. At 300 operations per byte the NPU is memory-bound at **19.2** TOPS, **24.4**% of its dense peak and an eighth of its headline; it reaches the peak only above **1229** operations per byte, which few inference workloads approach with weights streamed from LPDDR.
2. At 0.75 V and 700 MHz the chip delivers **140** TOPS at **10.9** W, **12.8** TOPS/W: between the two quoted points, and a defensible product point. The efficiency curve falls steadily with voltage, so every product decision is a choice of where to sit on it.
3. The best of twenty averages about **2.63**× for a product whose median is 1.5× (expected maximum **1.87**); the simulated mean sits slightly above the formula, because the exponential of a maximum averages a little above the exponential of its expected value, and individual vendors' best cases scatter widely around it.
4. A metal-only respin brings production to **55.0** weeks, **12.6** months, against 15.2 months for a full respin: the value of spare cells and held wafers, if the bug can be fixed in metal (26-05).

## Optional hardware

None. As an exercise, take any accelerator's public product brief and restate its headline as dense throughput at one precision, with the operating point and power boundary of its efficiency figure; list what the brief does not say.
