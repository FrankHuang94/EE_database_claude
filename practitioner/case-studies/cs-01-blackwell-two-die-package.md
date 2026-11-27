# CS-01 · Going Past the Reticle: Blackwell's Two-Die Package and Its Yield Respin

| | |
|---|---|
| **Decision** | Build one GPU from two near-reticle dies joined by a 10 TB/s link on a bridge-based 2.5D package, rather than one die at the reticle limit |
| **Company and date** | NVIDIA, announced March 2024; mask change disclosed August 2024 |
| **Domain** | [Packaging](../playbooks/packaging.md), [AI accelerators](../playbooks/ai-accelerator.md) |
| **Sources** | [R-149], [R-586], [R-646] in the [research log](../../reference/research-log.md) |

## What was decided

The B200 GPU is "manufactured using a custom-built 4NP TSMC process with two-reticle limit GPU dies connected by 10 TB/second chip-to-chip link", about 208 billion transistors in all [R-149] **[Established: vendor-disclosed]**. A teardown found two near-reticle dies and eight HBM3E stacks on TSMC's CoWoS-L, a local-silicon-interconnect bridge in an organic interposer: "NVIDIA's first use of a bridge-based 2.5D integration technology" [R-586] **[Established]**.

## The engineering behind it

- **The reticle caps die area.** One exposure field limits a single die to roughly 830 to 858 mm² [R-586] ([25-02](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-02-lithography.md)). More transistors on one product therefore means more dies.
- **Yield falls exponentially with area** ($Y \approx e^{-AD_0}$; [25-04](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md)). Two dies that are each tested before assembly yield more good silicon than one die of twice the area, which could not be exposed anyway.
- **The price is the die-to-die link.** It needs enough bandwidth that software sees one GPU, at low energy per bit, across a bridge ([24-06](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md)).
- **Why a bridge.** A full silicon interposer large enough for two such dies and eight HBM stacks runs into its own size and cost limits. Local bridges carry the dense wiring only where it is needed ([25-07](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md)).

## What happened

On the August 2024 earnings call, NVIDIA's CFO said: "We executed a change to the Blackwell GPU [mask] to improve production yields." Gross margin was affected by "inventory provisions for low-yielding Blackwell material". The CEO said: "The change to the mask is complete. There were no functional changes necessary" [R-646] **[Established: management statements, secondary transcript]**. The production ramp was scheduled for the fourth quarter.

## What a diligence team should have asked

1. Which yield is the problem: die yield, bridge and assembly yield, or HBM stacks? Where is it measured?
2. How much of the package is tested before final assembly, and what does a failure after assembly scrap?
3. Is packaging capacity allocated for the ramp, and from how many lines?
4. What does a mask change cost in time, and was the schedule built with room for one ([26-05](../../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md))?

## Lessons that transfer

- **Even the leaders respin.** Plan the schedule and the inventory for one yield fix on any new package at the reticle limit ([28-03](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-03-silicon-maturity-scales.md)).
- **A first use of a packaging technology is a maturity reset**, even inside an experienced company. Score it as such in the implementation and supply dimensions of the scorecard ([28-01](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md)).
