# CS-04 · How Big Should One Domain Be? NVLink-72 Against a 9,216-Chip ICI Pod

| | |
|---|---|
| **Decision** | Choose the size and per-chip bandwidth of the tightly coupled domain that one model runs in |
| **Companies and dates** | NVIDIA (GB200 NVL72); Google (Ironwood, April 2025) |
| **Domain** | [AI accelerators](../playbooks/ai-accelerator.md), [interconnect](../playbooks/interconnect-optics.md) |
| **Sources** | [R-521], [R-690], [R-693] in the [research log](../../reference/research-log.md) |

## What was decided

**NVIDIA's choice: a small, fast, all-to-all domain.**

- 72 GPUs in one rack, each with "1.8 TB/s of GPU-to-GPU interconnect", in an NVLink domain "that acts as a single, massive GPU" [R-690] (NVIDIA's marketing description).
- Each GPU's bandwidth comes from 18 NVLinks of 100 GB/s each [R-521].
- The domain sits inside one liquid-cooled rack [R-690].

**Google's choice: a much larger domain at lower per-chip bandwidth.** (The logged source does not describe the ICI topology.)

- Ironwood scales "up to 9,216 liquid cooled chips linked with breakthrough Inter-Chip Interconnect (ICI) networking", at "1.2 TBps bidirectional" per chip [R-693].
- The pod spans "nearly 10 MW" [R-693].

**[Established as manufacturer specifications.]**

## The engineering behind it

- **Inside the domain:** traffic for tensor and expert parallelism runs at memory-like bandwidth.
- **Outside it:** traffic crosses network ports roughly an order of magnitude slower per device. Like for like, NVLink's 900 GB/s each way is **18×** a 400 Gb/s port's 50 GB/s ([C4 §3.3](../../capstones/C4-diligence-memo/reference/memo.md)).
- **A bigger domain** lets a larger model run, or a larger batch run at a tight latency target, without the slow link.
- **The cost of size.** Copper reaches only so far at these rates. A domain beyond one rack needs optics or a topology that trades per-chip bandwidth or hop count for reach ([24-06](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md), [24-09](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-09-lpo-and-cpo.md)).
- **Collectives favour large per-device bandwidth.** All-reduce time is governed by per-device link bandwidth and the number of hops ([27-07 §3.5](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md#35-collectives-the-all-reduce)).
- **Failures scale with size.** A bigger domain is a bigger blast radius for a single fault ([C4 §5.2](../../capstones/C4-diligence-memo/reference/memo.md)).

## What a diligence team should ask

1. Which workloads need the whole domain, and which fit in a fraction of it?
2. What are the bisection bandwidth and the worst-case hop count, not just per-chip link bandwidth?
3. How does the domain degrade when one chip or link fails? What is the measured restart time?
4. What does the next generation change: per-chip bandwidth, domain size, or the medium (copper or optics)?

## Lessons that transfer

- **Compare systems at the domain level.** Per-chip specifications have converged (C4 §4), and the differentiation is now the domain: its size, its bandwidth per chip and its failure behaviour.
- **Neither choice dominates.** A small, fast domain wins for latency-bound serving of models that fit it. A huge domain wins for training and serving models that do not fit any rack.
