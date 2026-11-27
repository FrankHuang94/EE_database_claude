# Business ↔ Engineering Translation Table

**Each row runs both ways.**

- **Forward:** what does this engineering choice cost or earn?
- **Backward:** what must the engineering deliver to hit this business target?

The derivations, worked examples and sensitivities are in [28-09](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md). This page is the quick-reference version, extended by domain. It holds formulas only. Take the numbers from the linked chapters, with their dates.

## Cost and margin

| Business quantity | Engineering drivers | First-order translation | Chapter |
|---|---|---|---|
| Die cost | Wafer price $W$, die area $A$, defect density $D_0$ | $C_{die} = W/(\text{DPW}\cdot Y)$, with $Y \approx e^{-AD_0}$ (Poisson) or the negative-binomial form | [25-04](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md) |
| Gross margin | Die, package and test cost against average selling price | $\text{GM} = 1 - (C_{die} + C_{pkg+test})/\text{ASP}$ | [28-09](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md) |
| Chiplet against monolithic cost | Each chiplet's area and yield, assembly yield, die-to-die area overhead | $\sum_i C_{die,i} + C_{assembly}$, divided by the assembly yield, against $C_{die}$ of the large die | [25-07](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md) |
| Test cost | Tester time, sites, coverage, burn-in | Seconds per die × tester cost rate ÷ sites; escapes × field cost | [25-11](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-11-test-ate-sort-burn-in.md) |
| Memory cost per bit | Bits per mm², layers or stack height, yield | Wafer cost ÷ (good bits per wafer) | [23-06](../courses/23-memory-and-storage-technology/chapters/23-06-nand-flash-and-3d-nand.md) |

## Time and risk

| Business quantity | Engineering drivers | First-order translation | Chapter |
|---|---|---|---|
| Time to revenue | Tape-out date, respins, qualification | Delay cost ≈ lost gross profit: $m R\,d_m/12$ for $d_m$ months in a fixed market window | [26-05](../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md), [28-08](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-08-integration-risk.md) |
| Cost of a respin | Masks, wafers, engineering time, delay | Masks + engineering months × loaded cost + delay cost | [28-09](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md) |
| Risk-adjusted value | Milestone probabilities by maturity level | $V\prod_k p_k/(1+r)^{T/12}$ | [28-01](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md), [28-03](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-03-silicon-maturity-scales.md) |
| Value of more diligence | Prior, test accuracy, decision payoff | Expected value with the information minus without it | [28-01 §3.5](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md#35-the-value-of-information) |

## Customer value

| Business quantity | Engineering drivers | First-order translation | Chapter |
|---|---|---|---|
| Datacenter energy cost | Power, PUE, hours, electricity price | $E = P \cdot \text{PUE} \cdot h \cdot p_e$ | [22-10](../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md), [27-07](../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md) |
| Cost per token or per inference | Throughput at the latency target, power, capital cost, utilization | (capital ÷ life + energy cost) ÷ tokens served per year | [27-07](../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md), [C4 §3.3](../capstones/C4-diligence-memo/reference/memo.md) |
| Value of a power-supply efficiency point | Efficiency, load, the upstream chain | ΔP at the wall = $P_{out}(1/\eta_1 - 1/\eta_2)$, times the upstream stages' multiplier | [22-01](../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md) |
| Battery life of a device | Average current from the cell, usable capacity | Life = usable mAh ÷ average mA, through each regulator's efficiency | [22-09](../courses/22-power-electronics-and-energy-conversion/chapters/22-09-batteries-charging-fuel-gauging.md), [C3 §3](../capstones/C3-wearable-sensor-node/reference/design-report.md) |
| Wireless coverage | Transmit power, antenna gains, sensitivity, losses | Range at margin $M$: $d = d_0 \cdot 10^{(\text{link margin at } d_0 - M)/(10n)}$ for path-loss exponent $n$ | [21-11](../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md) |
| Performance premium | Delivered performance at the buyer's operating point | Customer value from total cost of ownership and revenue, not peak specifications | [28-02](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md) |

## Quality and liability

| Business quantity | Engineering drivers | First-order translation | Chapter |
|---|---|---|---|
| Warranty and field cost | Failure rate (FIT), installed base, hours | Failures = $\lambda N t$ with $\lambda$ in FIT × 10⁻⁹ per hour; cost = failures × cost each | [25-09](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md), [28-09](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md) |
| What a qualification proves | Device-hours, failures, acceleration factor | Upper bound on $\lambda$ from the chi-square distribution | [28-03](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-03-silicon-maturity-scales.md) |
| Fleet availability | Failures per device-year, blast radius, recovery time | Lost capacity ≈ failures × devices stalled per failure × recovery hours | [27-07 §3.6](../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md#36-reliability-at-scale-and-checkpointing), [C4 §5.2](../capstones/C4-diligence-memo/reference/memo.md) |

## Market access

| Business quantity | Engineering drivers | First-order translation | Chapter |
|---|---|---|---|
| Export licensing | Dense throughput, bit length, die area | TPP = 2 × MacTOPS × bit length; performance density = TPP ÷ die area, against the ECCN 3A090 thresholds | [26-07](../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md), [28-02](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md) |
| Revenue forecast | Design wins, conversion rates, lag | Funnel: wins × conversion × volume × ASP, shifted by the design-in lag | [28-06](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-06-red-and-green-flags.md) |
