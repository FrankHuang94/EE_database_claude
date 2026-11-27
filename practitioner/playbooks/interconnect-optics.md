# Playbook · Interconnect and Optics

**Use it for:** SerDes IP and retimers, PCIe, CXL and Ethernet silicon, die-to-die interfaces, scale-up fabrics, optical modules, silicon photonics, linear-drive and co-packaged optics.

**Core chapters:** [24-01](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md) to [24-09](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-09-lpo-and-cpo.md).

**Method:** [28-04 §3.4](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-04-question-banks-digital-ai-memory-interconnect.md#34-electrical-interconnect) and [§3.5](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-04-question-banks-digital-ai-memory-interconnect.md#35-optics).

**Question bank:** [high-speed I/O and photonics](../question-banks/interconnect-and-photonics.md).

## What decides it

1. **What is the energy per bit, all-in?** Include the PHY, the DSP or equalization, FEC, the retimer and the optics, at the reach the customer uses ([24-04](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-04-dsp-serdes-and-fec.md)).
2. **What bit error rate and link-flap rate does the link achieve at the channel loss that matters, over temperature and many units?** Per-link reliability multiplies across thousands of links ([24-02](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-02-eye-diagrams-jitter-ber.md)).
3. **Is it compliant and interoperable?** Standards compliance, plugfest results and interoperability with the major switch and NIC vendors ([24-05](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-05-pcie-cxl-ethernet.md)).
4. **For optics: what is the laser's reliability, and how serviceable is the design?** Co-packaged optics trades serviceability for power ([24-09](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-09-lpo-and-cpo.md)). Who supplies the lasers, and is there a second source?
5. **Is the IP silicon-proven on the customer's node?** A SerDes or die-to-die PHY proven on one process is a new design on the next; ask for test-chip data on the node the customer will use ([24-06](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md)).
6. **Who owns the standard's direction?** Interconnect value accrues to those inside the standards process and the dominant ecosystems.

## First-principles checks

| Claim | Check | Where derived |
|---|---|---|
| "x pJ/bit" | Power ÷ data rate, with what included? Per lane or per port, and at which reach and loss? | [24-03](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-03-serdes-architecture.md), [24-04](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-04-dsp-serdes-and-fec.md) |
| "Supports y dB of loss" | Insertion loss at the Nyquist frequency; the equalizer's taps; the margin to the specification's channel | [24-01](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md), [24-03](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-03-serdes-architecture.md) |
| "BER 1e-12" | Pre-FEC or post-FEC? Measured over how many bits? Zero errors in $n$ bits bound the BER at $3/n$ at 95% | [24-02](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-02-eye-diagrams-jitter-ber.md), [28-10](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-10-conversation-scenarios.md) Example 28-10.5 |
| "Low latency" | FEC and DSP add latency; count the pipeline stages at the stated rate | [24-04](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-04-dsp-serdes-and-fec.md) |
| "Die-to-die at z Tb/s/mm" | Shoreline bandwidth density = lanes per mm × rate, counting both directions; bump pitch | [24-06](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md) |
| "CPO saves w%" | Against which baseline (DSP pluggable, linear-drive pluggable)? Laser power and the external laser's wall-plug efficiency included? | [24-09](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-09-lpo-and-cpo.md) |

## Evidence ladder

From weakest to strongest:

1. simulated eye diagrams;
2. a test chip on a lab channel;
3. compliance testing on the specification's channels;
4. interoperability at a plugfest and with major hosts;
5. a deployed fleet with link-flap and failure-in-time data.

## Red flags and green flags

**Red flags:**

- pJ/bit with nothing said about what it includes;
- BER from a short test with no confidence bound;
- a single lab channel;
- no interoperability data;
- CPO savings against an old baseline;
- laser reliability from accelerated tests only.

**Green flags:**

- energy-per-bit budgets by block;
- compliance reports;
- named interoperability partners;
- long-duration BER and flap data;
- laser FIT data from fielded units;
- a serviceability plan.

## A 90-minute meeting

| Minutes | Topic |
|---|---|
| 0–15 | The link: rate, reach, medium, the host and switch at each end |
| 15–35 | Power and margin: energy per bit by block, channel loss, equalization, FEC |
| 35–55 | Reliability at fleet scale: BER, flaps, temperature, units tested |
| 55–75 | Compliance and interoperability; standards participation |
| 75–90 | Roadmap: next lane rate, optics transition, serviceability |

## Documents to request

- The energy-per-bit budget.
- Compliance and interoperability reports.
- BER and flap test logs with bit counts.
- Laser reliability data.
- Standards-body roles and contributions.

## Go deeper

- [28-10](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-10-conversation-scenarios.md): Example 28-10.4 (SerDes power, all-in) and Example 28-10.5 (a million link-hours).

> **Deeper:** see companion repo *Datacenter Networking*.
