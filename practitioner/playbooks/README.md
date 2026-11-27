# Diligence Playbooks

A playbook is a field guide for one technical domain: what decides a deal, which first-principles checks to run on the numbers you are shown, what strong and weak evidence look like, and how to spend a 90-minute technical meeting. Each one points back to the chapters that derive the checks, to the [question banks](../question-banks/README.md) for depth, and to [Course 28](../../courses/28-technical-diligence-and-leadership-fluency/README.md) for the method.

| Playbook | Use it for | Core chapters |
|---|---|---|
| [Digital logic and CPUs](digital-cpu.md) | CPU and SoC IP, custom silicon, RISC-V | 14, 19, [28-04 §3.1](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-04-question-banks-digital-ai-memory-interconnect.md#31-digital-logic-and-cpus) |
| [AI accelerators](ai-accelerator.md) | Training and inference chips, racks, edge NPUs | 14-14, 14-15, 27-07, [28-04 §3.2](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-04-question-banks-digital-ai-memory-interconnect.md#32-ai-accelerators) |
| [Analog and mixed-signal](analog-mixed-signal.md) | Data converters, references, PLLs, sensor front ends | 20, [28-05 §3.1](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md) |
| [RF and wireless](rf.md) | Transceivers, front-end modules, mmWave, connectivity SoCs | 17, 21 |
| [Power](power.md) | Converters, PMICs, GaN and SiC, datacenter power | 22 |
| [Memory](memory.md) | DRAM, HBM, NAND, SSD controllers, emerging memories | 23 |
| [Interconnect and optics](interconnect-optics.md) | SerDes, PCIe/CXL/Ethernet, die-to-die, optical modules, CPO | 24 |
| [Packaging, manufacturing and reliability](packaging.md) | Advanced packaging, foundry and node choices, test, qualification | 09, 25 |
| [Embedded and low-power systems](embedded.md) | MCUs, wireless SoCs, wearables, IoT | 18, 27-03, 27-08 |

## How to use a playbook

1. **Before the meeting:** frame the decision with the [28-01](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md) seven dimensions and weights, send the document request from the playbook, and run its first-principles checks on whatever the company has published.
2. **In the meeting:** follow the playbook's sequence. Ask the decisive questions first, and keep the live checks from the [28-10 pocket card](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-10-conversation-scenarios.md#35-the-pocket-card) at hand.
3. **After the meeting:** score the evidence, not the impression. Update the scorecard with an uncertainty for each dimension, and record each red or green flag with the evidence behind it ([28-06](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-06-red-and-green-flags.md)).

The [C4 capstone memo](../../capstones/C4-diligence-memo/reference/memo.md) shows the whole method applied to one public product.

## Rules that apply to every domain

- **Every headline number has an operating point.** Ask for the conditions before judging the number: voltage, temperature, load, precision, sparsity, batch, distance, corner.
- **Typical is not guaranteed.** A data sheet's typical column describes one unit at 25 °C. Designs are built on the limits ([28-05 §3.6](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md)).
- **Strong evidence is measured on artefacts** (silicon, code, contracts, people); weak evidence is a statement about them ([28-01 §3.1](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md#31-the-seven-dimensions-and-their-evidence)).
- **Perishable facts expire.** Every number in a memo carries its date and source; check the chapter's "Numbers to know" date before reusing one.
