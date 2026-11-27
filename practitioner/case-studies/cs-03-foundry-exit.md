# CS-03 · When the Foundry Leaves: GaN at TSMC

| | |
|---|---|
| **Decision** | A foundry ends production of a specialty technology; its fabless customers must requalify elsewhere |
| **Companies and date** | TSMC and Navitas, reported July 2025; production to end by July 2027 |
| **Domain** | [Power](../playbooks/power.md), [manufacturing](../playbooks/packaging.md) |
| **Sources** | [R-432], [R-423] in the [research log](../../reference/research-log.md) |

## What happened

Navitas was "informed by TSMC that it will end GaN wafer foundry production by end-July 2027" [R-432] **[Established as reported]**. This was reported by Semiconductor Today, citing a Form 8-K that was not read directly.

An industry analysis of 2026 adds that foundries "VIS and … PSMC are absorbing volume as customers move off TSMC". The same analysis reports onsemi collaborating with GlobalFoundries on 650 V GaN-on-silicon at 200 mm [R-432] **[Industry estimate]**.

## The engineering behind it

- **A specialty process is not portable like a digital PDK.** GaN-on-silicon devices depend on the epitaxial stack, the gate structure and the passivation. Their threshold drift, dynamic $R_{on}$ and breakdown change with the process ([22-06](../../courses/22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md)).
- **Moving fabs is close to a redesign.** It means new device characterization, new models, new reliability qualification (high-temperature reverse bias and gate bias, dynamic $R_{on}$ under switching) and new customer qualification ([25-10](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-10-qualification-and-functional-safety.md)).
- **The timeline is set by qualification, not by design.** Customers in automotive and datacenter power requalify the end product too.
- **The commercial setting.** The same vendor's datacenter power-supply claims ("137W/in³ and over 97% efficiency" for a 4.5 kW reference design [R-423] **[Industry estimate]**) depend on devices that now need a new fab.

## What a diligence team should ask a fabless specialty-process company

1. Which foundries can run your process today, and which are qualified with customers?
2. What is the transfer plan, its cost and its timeline? Which customer qualifications must be repeated?
3. How much last-time-buy inventory covers the gap, and what does it cost in working capital?
4. Do the devices from the new fab match the old ones on dynamic $R_{on}$ and threshold drift, and on what evidence?

## Lessons that transfer

- **"We have a partnership with the foundry" is weak evidence** ([28-01 §3.1](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md#31-the-seven-dimensions-and-their-evidence)). For a specialty process, single-foundry dependence belongs in the supply dimension's gate, not in a footnote.
- **Foundry strategy follows the foundry's own economics.** A specialty line that is small against the foundry's main business is the one most likely to close.
