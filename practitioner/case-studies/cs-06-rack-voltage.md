# CS-06 · Changing the Rack's Voltage: From 54 V to 800 VDC

| | |
|---|---|
| **Decision** | Move AI datacenter power distribution from 54 V in-rack busbars to 800 VDC, for megawatt racks |
| **Company and date** | NVIDIA with partners, announced May 2025, "starting in 2027" |
| **Domain** | [Power](../playbooks/power.md) |
| **Sources** | [R-444], [R-691], [R-098] in the [research log](../../reference/research-log.md) |

## What was decided

**Today's rack.** The GB200 rack's power shelves "convert AC power into nominal 50V-51V DC output and distribute it through the bus bar to the rack components". Rack consumption is about 120 kW [R-444]. Other vendors quote 132 kW nominal and about 192 kW provisioned [R-098] **[Contested by definition]**.

**The announcement.** NVIDIA wrote that "Traditional 54 V in-rack power distribution, designed for kilowatt (KW)-scale racks, isn't designed to support the megawatt (MW)-scale racks coming soon". It is "leading the transition to 800 VDC data center power infrastructure to support 1 MW IT racks and beyond, starting in 2027". With 54 VDC, "power shelves would consume up to 64 U of rack space" at megawatt scale [R-691] **[Established as NVIDIA's statements]**.

## The engineering behind it

- **Current sets the copper and the loss.** For a given power, current is $I = P/V$ and conduction loss is $I^2R$. Raising the voltage by a factor $k$ cuts the current by $k$ and the loss in a given conductor by $k^2$; from 54 V to 800 V, $k$ is about 15. You can keep the loss and shrink the copper instead ([22-10](../../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md)).
- **The vendor's own comparison depends on assumptions.** NVIDIA's "85% more power transmission through the same conductor size" against 415 VAC depends on the conductor count and power factor assumed; 22-10 §3.2 shows how [R-691].
- **The conversion chain must be redesigned.** Higher-voltage DC means new isolated converters in the rack and new protection: arc-fault and DC breaking are harder than AC ([22-04](../../courses/22-power-electronics-and-energy-conversion/chapters/22-04-isolated-converters.md), [22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md)).
- **The upstream transformer is open.** NVIDIA and partners "are actively studying the CapEx and, OpEx, and safety implications of both traditional transformer-based and solid-state transformer (SST) approaches" [R-691].

## What a diligence team should ask

**A power-component supplier:**

1. Which parts of your portfolio work at 800 VDC?
2. Which are qualified to the new safety standards?
3. What is your share of the conversion stages that move or disappear?

**A datacenter operator:**

1. What does a site built today need to change in 2027?
2. Who pays for it?

**A rack vendor:**

1. How does energy storage at the rack interact with the new distribution? (Compare the GB300 power-smoothing design in [R-444].)

## Lessons that transfer

- **An architecture change upstream reshuffles the value chain downstream.** Stages disappear, new ones appear, and incumbents in the old stages lose share.
- **Ask about the transition, not just the end state.** Mixed fleets of 54 V and 800 V racks will coexist for years, and the dual inventory and training cost falls on the operator.
