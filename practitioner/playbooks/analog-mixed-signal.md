# Playbook · Analog and Mixed-Signal

**Use it for:** data converters, references and regulators, PLLs and clocking, sensor front ends, and analog IP blocks inside SoCs.

**Core chapters:** [20-01](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-01-analog-design-fundamentals-gm-id.md) to [20-12](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-12-why-analog-does-not-scale.md), with [12](../../courses/12-electronics-2/README.md) for amplifier theory.

**Method:** [28-05](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md). **Question bank:** [analog and mixed-signal](../question-banks/analog-and-mixed-signal.md).

## What decides it

1. **Where does the part sit against the published frontier?** Compare it on the figure of merit for its class, at its own speed. Schreier for high resolution, Walden for low resolution at high speed ([20-06](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-06-data-converter-fundamentals.md); [28-05 §3.1](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md)).
2. **Are the numbers guaranteed or typical?** Ask for the limits over temperature, supply and process, and the production test that enforces them.
3. **What did calibration buy, and what does it cost?** Calibration gives back accuracy, but costs power, area, start-up time and test time. It can also fail in the field.
4. **Can the block move to the next node?** Analog does not shrink like logic ([20-12](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-12-why-analog-does-not-scale.md)). A roadmap that assumes it does is a red flag.
5. **How many good analog designers are there, and who are they?** Analog teams are small, slow to hire and hard to replace ([28-07](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-07-evaluating-engineering-teams.md)).
6. **Who owns the process, and how long must the parts be supplied?** Catalogue analog companies often run their own specialty fabs and sell thousands of parts for decades; a fabless entrant depends on a foundry's specialty process staying open ([25-05](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-05-foundries-pdks-specialty-processes.md); [CS-03](../case-studies/cs-03-foundry-exit.md)). Ask for the catalogue's breadth, the revenue tail from old parts and the plan for end-of-life notices.

## First-principles checks

| Claim | Check | Where derived |
|---|---|---|
| "N-bit ADC" | ENOB = (SINAD − 1.76)/6.02 at the stated input frequency. Thermal noise sets a floor of $kT/C$ on the sampling capacitor | [20-06](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-06-data-converter-fundamentals.md), [20-05](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-05-comparators-and-sample-and-hold.md) |
| "SNR at GHz input" | Aperture jitter limit: $\text{SNR} = -20\log_{10}(2\pi f_{in}\sigma_t)$. Ask whose clock was used | [20-10](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-10-plls-and-jitter.md) |
| "Low-power converter" | The figure of merit at the part's own speed and resolution, against the survey frontier | [20-06](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-06-data-converter-fundamentals.md), [20-07](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-07-nyquist-adcs.md) |
| "x ppm/°C reference" | Box method over which range, and is it guaranteed? Drift, hysteresis and long-term aging are separate specifications | [20-03](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-03-bandgap-references.md) |
| "Matched to 0.1%" | Pelgrom: $\sigma(\Delta V_{TH}) = A_{VT}/\sqrt{WL}$, so the area needed scales as the square of the precision | [20-11](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-11-layout-matching-pvt.md) |
| "Stable LDO with any capacitor" | Pole positions against load current and capacitor ESR; PSRR at the switching frequency of the upstream converter | [20-04](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-04-ldo-regulators.md) |

## Evidence ladder

From weakest to strongest:

1. simulation at the typical corner;
2. simulation across corners and Monte Carlo;
3. measured on a few units at room temperature;
4. characterized across temperature, supply and lots;
5. production-tested limits with yield data.

## Red flags and green flags

**Red flags:**

- only typical values published;
- a figure of merit computed at a different speed from the headline;
- the jitter of a lab-grade clock used for an SoC product;
- calibration that needs a factory trim nobody costed;
- a roadmap that scales analog area with logic.

**Green flags:**

- characterization reports with distributions;
- measured performance on several lots;
- calibration that is background and self-checking;
- designers with several shipped generations;
- honest frontier positioning ("second quartile at our speed, at half the area").

## A 90-minute meeting

| Minutes | Topic |
|---|---|
| 0–15 | The specification that matters to the customer, and its operating point |
| 15–35 | Measured against simulated; typical against guaranteed; temperature and lot spread |
| 35–55 | Architecture and calibration: what limits the part (noise, matching, jitter), and why this architecture |
| 55–75 | Porting: the next node, the PDK and its device models, area and power at the new node |
| 75–90 | The team: who designed it, who validated it, how many could do it again |

## Documents to request

- Characterization reports, with histograms across temperature, supply and lots.
- Production test limits and yield.
- Errata.
- The calibration design and test-time budget.
- The porting history across nodes.
- An organization chart of the analog team, with tenures.

## Go deeper

- The [C1 capstone](../../capstones/C1-analog-design/README.md): an op-amp and a buck, verified across corners.
- [28-10](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-10-conversation-scenarios.md): Example 28-10.6, an ADC against the frontier.
