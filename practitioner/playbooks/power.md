# Playbook · Power

**Use it for:** DC-DC converters and PMICs, GaN and SiC devices, power supplies, datacenter power delivery, batteries and chargers.

**Core chapters:** [22-01](../../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md) to [22-10](../../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md).

**Method:** [28-05 §3.3](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md#33-power-conversion). **Question bank:** [power](../question-banks/power.md).

## What decides it

1. **What is the efficiency at the load points the customer actually runs?** Light-load and full-load efficiency diverge, and the standard's weighting may differ from the customer's profile.
2. **Where is the box around the power-density figure?** What is inside it: hold-up capacitance, fans, connectors, heat sinks ([22-01](../../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md)).
3. **Is the device technology qualified and second-sourced?** GaN and SiC supply has shifted fast, with foundries entering and exiting (as of Nov 2026) ([22-06](../../courses/22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md); R-432).
4. **Is the control loop robust across components and conditions?** That means capacitor derating, inductor tolerance and input range. In the [C1 buck](../../capstones/C1-analog-design/README.md), the first compensator failed its gain margin because the error amplifier's bandwidth is part of the plant; the second missed its load-step margin at the high-inductance, low-capacitance corner.
5. **For datacenter power: does the design follow the rack's architecture change?** Busbar voltage, shelf power and energy storage are all moving ([22-10](../../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md); [CS-06](../case-studies/cs-06-rack-voltage.md)).
6. **For SiC: what does overcapacity do to price and to the target's position?** An analyst estimate put upstream SiC utilization near 50% and device lines near 70% in late 2025, with the downturn expected to last until 2027–2028, and Chinese companies holding about 40% of wafer and epiwafer capacity [R-432] **[Industry estimate, as of Dec 2025]**. Ask how the target's cost per good die and its customer contracts hold up through the downturn.

## First-principles checks

| Claim | Check | Where derived |
|---|---|---|
| "x% efficient" | At which load, input voltage and temperature? A chain's efficiency is the product of its stages' | [22-01](../../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md) |
| "Tiny output capacitance" | The effective capacitance at DC bias; the load step it was tested with; $\Delta V \approx \Delta I/(2\pi f_c C)$ | [22-02](../../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md), [22-07](../../courses/22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md) |
| "MHz switching" | Minimum on-time against duty cycle: $t_{on} = D/f_s$; switching loss $\propto V I (t_r + t_f) f_s$ | [22-02](../../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md), [22-06](../../courses/22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md) |
| "GaN beats silicon" | Compare the figure of merit $R_{on}Q_g$ and the output charge at the operating voltage; check dynamic $R_{on}$ and threshold drift | [22-06](../../courses/22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md) |
| "Fast transient response" | Crossover frequency, phase and gain margin across corners; the error amplifier's own bandwidth | [22-07](../../courses/22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md), C1 option B |
| "Battery lasts N days" | Usable capacity ÷ average current, with converter efficiency and every duty cycle; aging and temperature reserve | [22-09](../../courses/22-power-electronics-and-energy-conversion/chapters/22-09-batteries-charging-fuel-gauging.md), C3 §3 |

## Evidence ladder

From weakest to strongest:

1. a reference-design press release;
2. an evaluation board measured by the vendor;
3. independent measurements with stated conditions;
4. qualification data, including dynamic $R_{on}$ and high-temperature reverse-bias and gate-bias (HTRB and HTGB) life tests;
5. field return rates at volume.

## Red flags and green flags

**Red flags:**

- a single efficiency number;
- density with no dimensions;
- nominal capacitance in the loop analysis;
- a GaN supply that depends on one foundry with no transfer plan;
- no data on dynamic $R_{on}$;
- control-loop margins at the typical corner only.

**Green flags:**

- efficiency curves at several input voltages;
- a recomputable box;
- derated components in the stability analysis;
- second-source wafers;
- published qualification to the relevant JEDEC or AEC standards.

## A 90-minute meeting

| Minutes | Topic |
|---|---|
| 0–15 | The load profile and the operating points that matter |
| 15–35 | Efficiency and density: conditions, box, thermal derating |
| 35–55 | Devices and supply: technology, foundry, qualification, second source |
| 55–75 | Control and robustness: corners, component tolerance, protection behaviour |
| 75–90 | Roadmap: architecture changes in the target market (for example, rack power) |

## Documents to request

- Efficiency and thermal test reports.
- Box dimensions and bill of materials.
- The qualification report.
- Wafer supply agreements.
- The control-loop analysis across corners.
- Field return data.

## Go deeper

- The [C1 option B buck](../../capstones/C1-analog-design/option-b-buck/design-report.md): a compensator that failed and was redesigned.
- [28-10](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-10-conversation-scenarios.md): Example 28-10.8, efficiency points.
