# Playbook · Embedded and Low-Power Systems

**Use it for:** microcontrollers and wireless SoCs, wearables, hearables, IoT nodes, sensor hubs, and any battery-life claim.

**Core chapters:** [18-01](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-01-microcontroller-architecture.md) to [18-11](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-11-hardware-security.md), [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md), [27-04](../../courses/27-system-architectures/chapters/27-04-wearables-earbuds-and-glasses.md) and [27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md).

**Method:** [28-05](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md). **Question bank:** [embedded](../question-banks/embedded.md).

**Worked example:** the [C3 wearable](../../capstones/C3-wearable-sensor-node/reference/design-report.md).

## What decides it

1. **What is the battery life on the customer's duty cycle, with every load counted?** That includes the sensors' own currents, which often dominate the microcontroller's. The C3 budget found the optical front end at about 91% and the radio at about 1.5%.
2. **Are the data-sheet currents at the voltage and conditions the product uses?** A current quoted at 3.0 V costs less from a 1.8 V rail only if the part can run there (C3 §2).
3. **Is the software ecosystem good enough for customers to ship?** That means SDK quality, RTOS support, radio stack qualification, and long-term support.
4. **Is security built in and certified?** Secure boot, key storage, update signing, and the certifications the market asks for ([18-11](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-11-hardware-security.md)).
5. **Is the part available for the product's life?** Longevity commitments, second sources and package options.

## First-principles checks

| Claim | Check | Where derived |
|---|---|---|
| "x µA/MHz" | At which voltage, from flash or RAM, running which code? Active current × time, plus every wake-up's cost | [18-09](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-09-ultra-low-power-design.md) |
| "y nA sleep" | With RTC, RAM retention and the 32 kHz oscillator? At what temperature (leakage rises steeply with it)? | [18-09](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-09-ultra-low-power-design.md) |
| "Battery lasts N days" | Usable capacity ÷ average current from the cell, through each regulator's efficiency, with every duty cycle and a reserve | [22-09](../../courses/22-power-electronics-and-energy-conversion/chapters/22-09-batteries-charging-fuel-gauging.md), C3 §3 |
| "Low-power radio" | Charge per connection event: $Q_{ev} = I_{pre}t_{pre} + I_{rx}(t_{rx} + T_{IFS}) + I_{tx}t_{tx}$, plus window widening $I_{rx}s$ | [27-03](../../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md), C3 §3.1 |
| "On-device AI at z mW" | Operations per inference × energy per operation, plus memory traffic; MLPerf Tiny-style conditions | [27-08](../../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md) |
| "No samples lost" | Buffer depth against worst-case service latency; interrupt priorities; DMA | [18-03](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-03-interrupts-exceptions-timers.md), [18-04](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-04-dma-and-data-movement.md), C3 §5 |

## Evidence ladder

From weakest to strongest:

1. a headline current from the feature list;
2. the data-sheet electrical table with conditions;
3. an energy benchmark under stated rules (such as EEMBC ULPMark);
4. a measured power profile of the customer's firmware on the board;
5. field battery-life data from shipped products.

## Red flags and green flags

**Red flags:**

- a feature-list current with no conditions;
- battery life computed without regulator losses or sensor currents;
- sleep current at 25 °C only;
- a radio stack not yet qualified;
- security as a roadmap item;
- no longevity commitment.

**Green flags:**

- the electrical table's conditions match the product;
- a published power profile of a reference application;
- qualified stacks;
- certified security;
- a 10-year or longer availability commitment;
- customers shipping on the SDK.

## A 90-minute meeting

| Minutes | Topic |
|---|---|
| 0–15 | The product and its duty cycle: what runs, how often, on which battery |
| 15–35 | The power budget: every load, at its data-sheet conditions; what dominates |
| 35–55 | Software: SDK, RTOS, radio stack, update path, developer adoption |
| 55–75 | Security and certification |
| 75–90 | Supply: longevity, packages, second sources, the roadmap's process node |

## Documents to request

- Electrical characterization at the product's voltages and temperatures.
- Measured power profiles of reference applications.
- Stack qualification certificates.
- Security certifications.
- The longevity programme.
- SDK release history.

## Go deeper

- The [C3 capstone](../../capstones/C3-wearable-sensor-node/README.md): its life requirement fails on the PPG front end's specified current, and the report says so.
- [28-10](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-10-conversation-scenarios.md): Example 28-10.10, a battery-life claim.
