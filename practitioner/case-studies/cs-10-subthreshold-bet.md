# CS-10 · Betting on Subthreshold: Ambiq's SPOT Platform

| | |
|---|---|
| **Decision** | Build microcontrollers whose digital logic runs below the transistor threshold voltage, trading speed and design difficulty for energy per operation |
| **Company and dates** | Ambiq; first parts 2015; a 12 nm platform announced March 2026 |
| **Domain** | [Embedded and low-power systems](../playbooks/embedded.md) |
| **Sources** | [R-027], [R-314], [R-100] in the [research log](../../reference/research-log.md) |

## What was decided

**The 2015 platform.** Ambiq's SPOT (Subthreshold Power Optimized Technology) "operates transistors at sub-threshold voltages (less than 0.5V)" [R-314]. Its first Apollo microcontrollers (2015) were quoted by the company at 30 µA/MHz active and about 100 nA standby, with claims of 5–10× lower energy than competing parts [R-027] **[vendor claim; the comparisons are Contested]**.

**The 2026 platform.** A March 2026 announcement describes a 12 nm SPOT platform on TSMC's N12e with an ultra-low-power mode "engineered to operate as low as 300mV", for a part not yet shipping [R-314] **[Industry estimate: company claim]**. A later product, the Apollo4 Plus, is quoted at "4 μA/MHz executing from MRAM (with cache)", at a supply voltage that was not captured [R-100] **[Industry estimate]**.

## The engineering behind it

- **Energy per operation falls as $CV^2$.** Lowering the supply from 1 V to 0.5 V would cut switching energy by four ([19-06](../../courses/19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md)).
- **The price is speed and leakage.** Below threshold, drive current is exponential in $V_{GS}$ ([09](../../courses/09-semiconductor-devices/README.md)), so speed collapses and becomes extremely sensitive to process, temperature and voltage. Leakage energy per operation then rises as each operation takes longer. The minimum-energy point lies near or just below threshold ([18-09](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-09-ultra-low-power-design.md)). The two effects set a minimum-energy supply, usually just below threshold ([19-06 §3.6](../../courses/19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md#36-the-minimum-energy-point)).
- **The design work is in tolerating variation.** Variation-tolerant libraries, adaptive voltage and body bias, and careful timing signoff at corners where delay varies widely are needed. A fast mode for bursts is also needed, which is what Ambiq's "turboSPOT" provides [R-027].
- **The comparison should be energy per task, not per MHz.** A wearable spends most of its life asleep, so sleep current and wake-up energy can outweigh active efficiency ([27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md); C3 §3).

## What a diligence team should ask

1. What is the energy per task on the customer's workload, measured at the product's temperature range, against named competitors?
2. How does timing yield vary across process and temperature at the lowest voltage, and how is it guaranteed in production test?
3. What does moving to a new node cost: new libraries, re-characterization, a new variation model?
4. Which customer products depend on the lowest-voltage mode, and which run in the fast mode most of the time?

## Lessons that transfer

- **A "5–10×" comparison is only as good as its baseline.** Ask which competitor part, at which voltage, running which code, and whether it was measured by a third party (EEMBC ULPMark is one such benchmark; [18-09](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-09-ultra-low-power-design.md)).
- **A circuit-design moat must be rebuilt at every node.** Check that the team has done it before, and how long it took.
