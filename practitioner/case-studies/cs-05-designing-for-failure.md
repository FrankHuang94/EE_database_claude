# CS-05 · Designing for Failure at 16,000 GPUs: Llama 3 Pre-Training

| | |
|---|---|
| **Decision** | Run a frontier training job on a cluster where hardware fails every few hours, and keep effective training time above 90% |
| **Company and date** | Meta, paper of July 2024 (revised November 2024) |
| **Domain** | [AI accelerators](../playbooks/ai-accelerator.md), [reliability](../playbooks/packaging.md) |
| **Sources** | [R-694] in the [research log](../../reference/research-log.md) |

## What happened

**The run.** Meta trained a 405-billion-parameter model with 3.8 × 10²⁵ FLOPs on "up to 16K H100 GPUs, each running at 700W TDP with 80GB HBM3". It reached "an overall BF16 Model FLOPs Utilization … of 38-43%" [R-694].

**The failures.** In a 54-day snapshot it saw "466 job interruptions. Of these, 47 were planned … The remaining 419 were unexpected". About 78% of the unexpected ones were attributed to confirmed or suspected hardware issues, and "GPU issues are the largest category, accounting for 58.7%". Even so, it achieved "higher than 90% effective training time", and "significant manual intervention was required only three times" [R-694] **[Established as Meta's reported figures]**.

**A data problem.** The failure table's percentages are inconsistent with its counts. The counts sum to 419, but 148 faulty-GPU events are 35.3% of 419, not the printed 30.1% [R-694] **[Contested: one printed figure is wrong]**.

## The engineering behind it

- **Rates add across components.** At this scale even small per-part failure rates add up ([25-09](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md)). The interval between interruptions falls as the cluster grows.
- **Checkpoint interval is an optimization.** Checkpointing too often wastes time writing state; too rarely loses work at each failure. The optimum depends on the checkpoint cost and the failure rate ([27-07 §3.6](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md#36-reliability-at-scale-and-checkpointing)).
- **Utilization below peak** reflects communication, pipeline bubbles and memory traffic as much as failures ([27-07](../../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md)).
- **Environment and grid effects.** Meta also reports a diurnal 1–2% throughput variation from temperature acting on GPU voltage and frequency scaling. It reports synchronized power swings "on the order of tens of megawatts, stretching the limits of the power grid" [R-694]. The diurnal effect is a thermal and cooling question; the megawatt swings are the reason for rack-level energy storage ([22-10](../../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md)).

## What a diligence team should ask a cluster operator or accelerator vendor

1. What are the interruption rates per device-year, by cause, measured on a fleet, not in qualification?
2. What is the effective training time, and how is it defined?
3. How long does recovery take after a fault, from detection to training again?
4. How many devices does one fault stall (C4 §5.2)?

## Lessons that transfer

- **Reliability at scale is a software and operations capability as much as a hardware property.** Score it under implementation and team, not just under the chip's qualification.
- **Check internal consistency of every table**, even in an excellent paper. The arithmetic in [28-02](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md) applies to good sources too.
