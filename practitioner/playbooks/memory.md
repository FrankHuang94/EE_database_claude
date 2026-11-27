# Playbook · Memory

**Use it for:** DRAM and HBM makers and their customers, NAND and SSD controllers, emerging memories (MRAM, ReRAM, PCM, FeRAM), and compute-in-memory start-ups.

**Core chapters:** [23-01](../../courses/23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md) to [23-09](../../courses/23-memory-and-storage-technology/chapters/23-09-compute-in-memory.md).

**Method:** [28-04 §3.3](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-04-question-banks-digital-ai-memory-interconnect.md#33-memory). **Question bank:** [memory](../question-banks/memory.md).

## What decides it

1. **Cost per bit at volume.** Memory is a cost-per-bit business, decided by die size, layer count, yield and wafer cost. A cell that is better in every other way but costs more per bit rarely wins outside a niche ([23-06](../../courses/23-memory-and-storage-technology/chapters/23-06-nand-flash-and-3d-nand.md), [25-04](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md)).
2. **Qualification at the customer's pin rate, stack height and temperature.** HBM generations are won by whoever qualifies first ([23-05](../../courses/23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md)).
3. **Endurance and retention over temperature.** An emerging memory's endurance and retention must be measured on arrays, not single cells, at the product's temperature ([23-08](../../courses/23-memory-and-storage-technology/chapters/23-08-emerging-memories.md)).
4. **For SSD controllers: the full system.** Write amplification, the error-correction margin as the NAND ages, firmware maturity and tail latency ([23-07](../../courses/23-memory-and-storage-technology/chapters/23-07-ssd-controllers.md)).
5. **For compute-in-memory: accuracy and the analog-to-digital overhead.** The converters at the array edge often dominate the energy, and accuracy must be shown on real models ([23-09](../../courses/23-memory-and-storage-technology/chapters/23-09-compute-in-memory.md)).

## First-principles checks

| Claim | Check | Where derived |
|---|---|---|
| "x TB/s per stack" | Bandwidth = interface width × pin rate ÷ 8; at which pin rate is it qualified? | [23-05](../../courses/23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md) |
| "Lower power memory" | Energy per bit at the interface and in the array; refresh power at temperature | [23-03](../../courses/23-memory-and-storage-technology/chapters/23-03-dram-cells-arrays-refresh.md), [23-04](../../courses/23-memory-and-storage-technology/chapters/23-04-dram-interfaces.md) |
| "Denser NAND" | Bits per mm² from layers × bits per cell ÷ cell footprint; the cost of the extra layers and their yield | [23-06](../../courses/23-memory-and-storage-technology/chapters/23-06-nand-flash-and-3d-nand.md) |
| "SSD endurance N drive-writes per day" | Raw program/erase cycles ÷ write amplification, over the warranty period, with the ECC margin at end of life | [23-07](../../courses/23-memory-and-storage-technology/chapters/23-07-ssd-controllers.md) |
| "Universal memory" | Compare speed, endurance, retention, density and cost against SRAM, DRAM and NAND together. No technology wins all five | [23-08](../../courses/23-memory-and-storage-technology/chapters/23-08-emerging-memories.md) |
| "In-memory compute, 100× TOPS/W" | Is the converter and digital periphery energy included? At which precision, and what is the accuracy on a full model? | [23-09](../../courses/23-memory-and-storage-technology/chapters/23-09-compute-in-memory.md) |

## Evidence ladder

From weakest to strongest:

1. single-cell results in a paper;
2. a test array with distributions;
3. a full-chip prototype with yield;
4. customer qualification at stated conditions;
5. volume production with field reliability data.

## Red flags and green flags

**Red flags:**

- endurance from single cells;
- bandwidth at a pin rate not yet qualified;
- cost-per-bit claims with no die size or yield;
- compute-in-memory energy without converters;
- SSD performance only at fresh-out-of-box state.

**Green flags:**

- distributions across arrays and lots;
- qualification dates with named customers;
- yield trends;
- steady-state SSD benchmarks with tail latency;
- full-model accuracy with the hardware's own noise.

## A 90-minute meeting

| Minutes | Topic |
|---|---|
| 0–15 | The product's position: which customers, which generation, which competitors |
| 15–35 | Cost per bit: die size, layers or stack height, yield, wafer cost |
| 35–55 | Qualification and reliability: pin rate, temperature, endurance and retention distributions |
| 55–75 | The interface and the system: controller, ECC, firmware, packaging |
| 75–90 | Capacity and roadmap: wafer starts, packaging capacity, next generation |

## Documents to request

- Qualification reports by customer and generation.
- Yield trends.
- Reliability distributions: endurance, retention, disturb.
- Die-size and cost models.
- Firmware release history (for controllers).
- Packaging capacity commitments.

## Go deeper

- [28-10](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-10-conversation-scenarios.md): Example 28-10.3, an HBM pin-rate claim.
- [28-04](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-04-question-banks-digital-ai-memory-interconnect.md): Example 28-04.3.
