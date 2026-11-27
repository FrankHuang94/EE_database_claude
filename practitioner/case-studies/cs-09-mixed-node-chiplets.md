# CS-09 · Mixed-Node Chiplets: Compute on 3 nm, the Rest on 6 nm

| | |
|---|---|
| **Decision** | Put the compute dies on the leading node and the I/O and memory interface on an older, cheaper node, joined in one package |
| **Company and date** | AMD, Instinct MI355X (specifications as of Nov 2026) |
| **Domain** | [Packaging](../playbooks/packaging.md), [AI accelerators](../playbooks/ai-accelerator.md) |
| **Sources** | [R-692] in the [research log](../../reference/research-log.md) |

## What was decided

AMD lists the MI355X's lithography as "TSMC 3nm | 6nm FinFET". The part has "Transistor Count 185 Billion", "288GB HBM3E memory, 8TB/s bandwidth" and "Typical Board Power (TBP) 1400W" [R-692] **[Established as manufacturer specifications]**. The page does not say which die is on which node; the split of compute on 3 nm and I/O on 6 nm is the usual pattern, but here it is an inference.

## The engineering behind it

**What does not shrink.** SerDes and analog circuits, I/O pads and the HBM PHYs shrink far less than logic from one node to the next ([20-12](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-12-why-analog-does-not-scale.md), [24-06](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md)). Large SRAM arrays have also shrunk more slowly than logic ([19-08](../../courses/19-digital-vlsi-design/chapters/19-08-sram-design.md)). On a leading node they cost the most per mm² and gain the least.

**Why splitting helps.**

- **Cost:** a mature node has a lower wafer price and higher yield.
- **Reuse:** the I/O die can carry across generations while the compute die moves to the next node.
- **Yield:** smaller compute dies yield better ($Y \approx e^{-AD_0}$; [25-04](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md)).

**What it costs.**

- Every crossing between dies spends energy per bit and area at both edges ([24-06](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md)).
- Assembly yield multiplies across the dies.
- Thermal design is harder, because the dies have different power densities ([25-07](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md), [25-08](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-08-thermal-engineering.md)).

**When the split wins.** It wins when the leading-node area saved, at the leading node's cost per good mm², exceeds the die-to-die overhead plus the assembly yield loss. The translation table gives the comparison ([chiplet against monolithic](../translation-table.md#cost-and-margin)).

## What a diligence team should ask

1. Which functions are on which die and node, and why?
2. What fraction of the package's power goes to die-to-die links?
3. What is the assembly yield, and what is tested before assembly?
4. Which dies carry over to the next generation, and what does the carry-over save in design cost and schedule?

## Lessons that transfer

- **Partitioning is an economic decision as much as a technical one.** Ask for the cost model behind it, with its sensitivity to wafer price, defect density and assembly yield.
- **"Transistor count" across a multi-node package mixes very different kinds of area.** It is not a measure of capability, and comparing it across vendors says little.
