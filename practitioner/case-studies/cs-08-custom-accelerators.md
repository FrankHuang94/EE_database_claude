# CS-08 · Building Your Own Accelerator: The Hyperscalers' Custom Silicon

| | |
|---|---|
| **Decision** | Large cloud operators design their own AI accelerators, usually with a custom-silicon partner, instead of buying only merchant GPUs |
| **Companies and dates** | Google, AWS, Microsoft, Meta; Broadcom and Marvell as partners; 2025 to 2026 |
| **Domain** | [AI accelerators](../playbooks/ai-accelerator.md) |
| **Sources** | [R-642], [R-643], [R-644] in the [research log](../../reference/research-log.md) |

## What happened

The operators' announcements, as of Nov 2026 [R-644] **[Established: vendor statements; performance figures are vendor claims]**:

- **AWS Trainium3** (December 2025) is "our first 3nm AWS AI chip", with "2.52 petaflops (PFLOPs) of FP8 compute … 144 GB of HBM3e memory, and 4.9 TB/s of memory bandwidth".
- **Microsoft Maia 200** (January 2026) has "216GB HBM3e at 7 TB/s", "over 10 petaFLOPS in 4-bit precision", and "30% better performance per dollar than the latest generation hardware in our fleet today", "all within a 750W SoC TDP envelope".
- **Meta** deploys "hundreds of thousands of MTIA chips for inference workloads". It announced with Broadcom a plan to "co-develop multiple generations" under a commitment "that exceeds 1GW".
- **Google's** TPU line continued with TPU 8t and 8i in April 2026.

The partners' results show the business [R-642, R-643] **[Established: company results]**:

- Broadcom reported fiscal 2025 AI revenue of USD 20 billion, up 65%, and USD 16.7 billion of AI semiconductor revenue in its third quarter of fiscal 2026.
- Marvell said its custom business "scaled from zero revenue to \$1.5 billion in fiscal 2026".

## The engineering behind it

- **A custom chip serves one owner's workloads.** It drops the generality a merchant GPU carries, and spends the area and power on the precisions, memory and interconnect those workloads need ([14-14](../../courses/14-computer-organization-and-architecture/chapters/14-14-ai-accelerators.md)).
- **The partner brings what is hard to build in-house:** SerDes and die-to-die IP, packaging, HBM integration and foundry access ([24-06](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md), [25-07](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md)). The operator brings the architecture, the software and the guaranteed volume that amortizes the design cost ([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md)).
- **"Performance per dollar against our fleet" is an internal comparison.** It compares against the operator's own installed base, at the operator's own prices, on the operator's own workloads. It cannot be checked from outside ([28-02](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md)).

## What a diligence team should ask

**A merchant accelerator vendor:**

1. Which of your largest customers are building their own accelerators?
2. For which workloads would a custom chip displace yours?

**A custom-silicon partner:**

1. How concentrated is the revenue by customer?
2. How many generations are committed?
3. Who owns the design IP?

**An operator:**

1. What fraction of the fleet's work runs on the custom chip?
2. What is the custom chip's software maturity on new model types?

## Lessons that transfer

- **Customer concentration is the defining risk of the custom-silicon business.** Score it in the commercial dimension and look for multi-generation commitments ([28-10](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-10-conversation-scenarios.md), Example 28-10.14).
- **A vendor's largest customers are often its future competitors.** Ask about this in any merchant-silicon diligence.
