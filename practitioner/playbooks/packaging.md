# Playbook · Packaging, Manufacturing and Reliability

**Use it for:** advanced packaging and chiplets, foundry and node decisions, test and burn-in, qualification and functional safety, and any company whose plan depends on someone else's fab or packaging line.

**Core chapters:** [09](../../courses/09-semiconductor-devices/README.md) (devices) and [25-01](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-01-process-flow-overview.md) to [25-12](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-12-post-silicon-validation.md).

**Method:** [28-03](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-03-silicon-maturity-scales.md) and [28-05](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md).

**Question bank:** [devices and manufacturing](../question-banks/devices-and-manufacturing.md).

## What decides it

1. **Does the plan have allocated capacity?** That means wafers at the node and capacity at the packaging line (2.5D interposers, hybrid bonding), with HBM or other known-good dies available. Allocation, not technology, often binds.
2. **What is the yield, and what does it cost?** Die yield and package or assembly yield compound, and a known-good-die strategy changes the arithmetic ([25-04](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md), [25-07](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md)).
3. **Can the package remove the heat at the product's power?** Junction temperature, thermal resistance of the stack, and the cooling the customer will provide ([25-08](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-08-thermal-engineering.md)).
4. **Is the part qualified for its market?** Consumer, industrial, automotive (AEC-Q100 and ISO 26262) and datacenter each demand different tests and durations ([25-10](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-10-qualification-and-functional-safety.md)).
5. **What does test cost, and what escapes?** Test time on the tester, coverage, burn-in, and the defect rate that reaches customers ([25-11](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-11-test-ate-sort-burn-in.md)).

## First-principles checks

| Claim | Check | Where derived |
|---|---|---|
| "Chiplets are cheaper" | Die cost = wafer cost ÷ (dies per wafer × yield) for each chiplet, plus packaging, assembly yield and the die-to-die area overhead, against the monolithic die | [25-04](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md), [25-07](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md) |
| "Yield is mature" | Defect density and the yield model (Poisson, negative binomial) at the die area; yield by lot over time | [25-04](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md) |
| "Runs cool" | $T_j = T_a + P\,\theta_{ja}$ (or the stack of $\theta$s); at the customer's ambient and airflow or coolant | [25-08](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-08-thermal-engineering.md) |
| "Qualified, x FIT" | The chi-square bound from the test's device-hours and failures; the activation energy and acceleration factor used | [25-09](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md), [28-03](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-03-silicon-maturity-scales.md) |
| "Next node gives z%" | Which parameter at which voltage? The design cost, the mask cost and the schedule at the new node | [25-05](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-05-foundries-pdks-specialty-processes.md), [26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md) |
| "First silicon works" | What fraction of the validation plan has run, at which corners, on how many units? | [25-12](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-12-post-silicon-validation.md), [28-03](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-03-silicon-maturity-scales.md) |

## Evidence ladder

From weakest to strongest:

1. a partnership announcement;
2. a test vehicle;
3. engineering samples with yield data;
4. a qualification report to the market's standard;
5. volume production with field return data.

## Red flags and green flags

**Red flags:**

- "partnership with the foundry" with no allocation;
- package yield missing from a chiplet cost case;
- thermal claims at an unrealistic ambient;
- a qualification described as "in progress" for a product already announced;
- a FIT rate with no device-hours;
- single-source packaging with no second line.

**Green flags:**

- wafer and packaging allocations in writing;
- yield-by-lot trends;
- a full thermal stack model correlated to measurement;
- qualification reports with sample sizes;
- a disclosed respin history with root causes.

## A 90-minute meeting

| Minutes | Topic |
|---|---|
| 0–15 | The product's manufacturing chain: node, foundry, packaging, memory, test house |
| 15–35 | Capacity and allocation: wafers, interposers or bonding, known-good dies |
| 35–55 | Yield and cost: die, package and test yields; the cost model and its sensitivities |
| 55–75 | Thermal and reliability: junction temperature at the customer's cooling; qualification status |
| 75–90 | Risk: single sources, the last respin, the plan for the next node |

## Documents to request

- Wafer and packaging supply agreements.
- Yield-by-lot data.
- The cost model.
- Thermal models with correlation data.
- Qualification reports.
- Test coverage and escape rates.
- The respin history.

## Go deeper

- The [C4 memo](../../capstones/C4-diligence-memo/reference/memo.md) §5.3: packaging and a yield respin at the reticle limit.
- [28-10](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-10-conversation-scenarios.md): Example 28-10.9 (a package-yield figure) and Example 28-10.21 (an automotive FIT claim).

> **Deeper:** see companion repo *Semiconductor Capital Equipment*.
