# Playbook · AI Accelerators

**Use it for:** training and inference chips, rack-scale systems, edge NPUs, and any TOPS, TOPS/W or "×N faster than" claim.

**Core chapters:** [14-13](../../courses/14-computer-organization-and-architecture/chapters/14-13-gpus-and-simt.md), [14-14](../../courses/14-computer-organization-and-architecture/chapters/14-14-ai-accelerators.md), [14-15](../../courses/14-computer-organization-and-architecture/chapters/14-15-roofline-and-benchmarks.md), [23-05](../../courses/23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md), [24-06](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md), [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) and [27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md).

**Method:** [28-02](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md) and [28-04 §3.2](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-04-question-banks-digital-ai-memory-interconnect.md#32-ai-accelerators).

**Worked example:** the [C4 memo on the GB200 NVL72](../../capstones/C4-diligence-memo/reference/memo.md).

## What decides it

1. **What is the delivered utilization on the customer's model, not the peak?** Model FLOPs utilization on real training runs sits well below peak (C4 §3.4 cites a measured 38–43% at scale).
2. **Is the workload compute-bound or bandwidth-bound at the operating point?** Decode is usually bandwidth-bound, so memory bandwidth, not TOPS, sets throughput.
3. **What fits in one scale-up domain?** The memory capacity and link bandwidth of the domain decide which models run without the slow network. In the C4 memo this, not the chip, is the moat.
4. **Is the software ready for the customer's models, frameworks and precisions?** Most accelerator start-ups lose on software, not silicon.
5. **Can it be built and deployed?** Packaging and HBM allocation, rack power and cooling, and export-control status.

## First-principles checks

| Claim | Check | Where derived |
|---|---|---|
| "X PFLOPS" | Dense or sparse? Which precision? Divide the system figure by the device count and compare with the per-device table | [28-02](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md), C4 §3.2 |
| "Y× faster than the incumbent" | Decompose into bandwidth, dense-compute and precision ratios. Whatever is left over comes from the operating point: batch, latency target, model size | C4 §3.3 |
| "Runs model M at Z tokens/s" | Roofline: attainable FLOP/s = min(peak, intensity × bandwidth). For decode, each token reads the weights and KV cache once | [14-15](../../courses/14-computer-organization-and-architecture/chapters/14-15-roofline-and-benchmarks.md), [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| "TOPS/W leadership" | At which precision, utilization and voltage? Is DRAM energy included? Energy per byte from DRAM usually exceeds energy per MAC | [14-14](../../courses/14-computer-organization-and-architecture/chapters/14-14-ai-accelerators.md), [23-01](../../courses/23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md) |
| "Scales linearly" | All-reduce time: about $2(N-1)/N$ × message ÷ link bandwidth, plus latency; the ratio of compute to communication | [27-07 §3.5](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md#35-collectives-the-all-reduce) |
| "Lower TCO" | Energy cost = power × PUE × hours × price, plus capital over its life; per token at the buyer's utilization | [28-09](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md), [22-10](../../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md) |
| "FP4 with no accuracy loss" | On which models and tasks, against which baseline? Is the accuracy delta reported per model? | [14-04](../../courses/14-computer-organization-and-architecture/chapters/14-04-computer-arithmetic-and-number-formats.md), [16-10](../../courses/16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md) |

## Evidence ladder

From weakest to strongest:

1. peak TOPS;
2. a vendor benchmark at one operating point;
3. MLPerf-style results with stated rules;
4. the customer's model on the customer's cluster, with utilization and accuracy;
5. a production fleet with failure rates and the utilization it actually sustains.

## Red flags and green flags

**Red flags:**

- sparse figures next to competitors' dense ones;
- a single operating point with no curve;
- power with no definition (chip, board or wall);
- "full software stack" with no customer running their own code;
- no answer on HBM and packaging allocation;
- a domain-size claim with no failure-handling plan.

**Green flags:**

- throughput-against-latency curves across model sizes;
- utilization and accuracy published per model;
- upstream framework support;
- named customers in production;
- disclosed packaging and memory supply.

## A 90-minute meeting

| Minutes | Topic |
|---|---|
| 0–15 | The workload: models, precisions, batch and latency targets that the business depends on |
| 15–35 | The claim decomposed: bandwidth, compute and precision ratios; the operating point |
| 35–55 | Delivered utilization and accuracy on real models; the software stack and who maintains it |
| 55–75 | Scale-up and scale-out: domain size, failure blast radius, collectives |
| 75–90 | Supply and deployment: packaging, HBM, rack power and cooling, export controls |

## Documents to request

- Benchmark reports with full configurations, including dense and sparse figures and precisions.
- Utilization and accuracy by model.
- Fleet reliability data: interruptions per device-year and their causes.
- The software release history and its upstream contributions.
- Packaging and HBM supply agreements.
- Rack power and cooling specifications.
- The export classification.

## Go deeper

- [27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md), Example 27-07.6, on serving a model from a rack.
- [28-10](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-10-conversation-scenarios.md): Example 28-10.1 (the utilization claim) and Example 28-10.2.

> **Deeper:** see companion repo *LLM Inference Engineering* (for serving systems) and *Datacenter Networking* (for scale-out fabrics).
