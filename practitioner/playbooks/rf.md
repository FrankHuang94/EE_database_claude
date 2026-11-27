# Playbook · RF and Wireless

**Use it for:** transceivers, power amplifiers and front-end modules, mmWave and phased arrays, and connectivity SoCs (Bluetooth, Wi-Fi, cellular, UWB).

**Core chapters:** [17-06](../../courses/17-communication-systems/chapters/17-06-bandpass-digital-modulation.md) and [17-09](../../courses/17-communication-systems/chapters/17-09-wireless-channels.md), [21-01](../../courses/21-rf-and-microwave-engineering/chapters/21-01-s-parameters.md) to [21-12](../../courses/21-rf-and-microwave-engineering/chapters/21-12-modem-baseband-and-standards.md).

**Question bank:** [electromagnetics, communications and RF](../question-banks/rf-and-wireless.md).

## What decides it

1. **What link margin does the product have at the distance, body position and phone that matter?** Range is set by the link budget, not by the radio's headline sensitivity ([21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md); C3 §4).
2. **What is the PA efficiency at the average output power, not at peak?** Modulated signals run backed off, where efficiency falls ([21-07](../../courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md)).
3. **Does it pass the standard's tests and the regulator's limits with margin?** Error vector magnitude, spectral mask, spurious emissions, coexistence with the other radios in the same device.
4. **How much of the value is in the front end, and who supplies the filters and switches?** Front-end modules are often the binding supply and IP constraint ([21-09](../../courses/21-rf-and-microwave-engineering/chapters/21-09-rf-front-end.md)).
5. **Is the software stack qualified?** Bluetooth and Wi-Fi qualification, cellular carrier certification, and the cost of maintaining them.

## First-principles checks

| Claim | Check | Where derived |
|---|---|---|
| "−X dBm sensitivity" | $-174 + 10\log_{10}B + \text{NF} + \text{SNR}_{min}$ dBm, at which bit or packet error rate, conducted or radiated? | [21-03](../../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md), [21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md) |
| "Range of N metres" | Friis: received power = $P_t + G_t + G_r - 20\log_{10}(4\pi d/\lambda)$, minus body and wall losses; indoors the exponent exceeds 2 | [21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md), [17-09](../../courses/17-communication-systems/chapters/17-09-wireless-channels.md) |
| "PA efficiency Y%" | At peak or at average power? Back-off from the signal's peak-to-average ratio; Doherty or envelope tracking? | [21-07](../../courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md) |
| "High linearity" | IIP3 and the third-order intercept slope; compression point; intermodulation at the customer's channel spacing | [21-03](../../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md) |
| "Phased array with N elements" | EIRP rises as $N^2$ (array gain times total power); scan loss; beam squint across the bandwidth | [21-10](../../courses/21-rf-and-microwave-engineering/chapters/21-10-antennas-arrays-mmwave.md) |
| "Low-jitter synthesizer" | Integrated phase noise converted to EVM and to SNR at the converter | [21-06](../../courses/21-rf-and-microwave-engineering/chapters/21-06-oscillators-and-vcos.md), [20-10](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-10-plls-and-jitter.md) |

## Evidence ladder

From weakest to strongest:

1. a data-sheet typical, conducted, at 25 °C;
2. measured across channels and temperature;
3. radiated measurements in the product enclosure;
4. certified (standard qualification, regulatory approval);
5. field performance at scale, such as dropped-call or reconnection rates.

## Red flags and green flags

**Red flags:**

- sensitivity quoted at a looser error rate than the standard's;
- range claims with no antenna gain or body loss;
- PA efficiency at saturation only;
- no coexistence data in a multi-radio product;
- a front end single-sourced from a competitor.

**Green flags:**

- link budgets with every assumption stated;
- radiated data in the real enclosure;
- certification history;
- efficiency curves against output power;
- second-source filters.

## A 90-minute meeting

| Minutes | Topic |
|---|---|
| 0–15 | The link: distance, body, environment, the other end's receiver |
| 15–35 | Receiver: noise figure, sensitivity at the standard's criterion, blocking and coexistence |
| 35–55 | Transmitter: power, efficiency at average power, linearity, spectral mask |
| 55–75 | Front end and antenna: who supplies what, radiated performance, enclosure effects |
| 75–90 | Certification, software maintenance, roadmap to the next standard revision |

## Documents to request

- Conducted and radiated test reports.
- Certification records.
- Efficiency-against-power curves.
- Coexistence test data.
- The front-end bill of materials, with its sources.
- Customer field metrics.

## Go deeper

- The [C3 capstone](../../capstones/C3-wearable-sensor-node/README.md): a BLE link budget with the phone's sensitivity as the deciding assumption.
- [28-10](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-10-conversation-scenarios.md): Example 28-10.7, a PA at back-off.
