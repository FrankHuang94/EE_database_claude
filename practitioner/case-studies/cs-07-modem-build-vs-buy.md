# CS-07 · Build Versus Buy: Apple's First Modems

| | |
|---|---|
| **Decision** | Design the cellular modem in-house instead of buying it from a merchant supplier |
| **Company and dates** | Apple; C1 shipped February 2025, C1X September 2025 |
| **Domain** | [RF and wireless](../playbooks/rf.md) |
| **Sources** | [R-660] in the [research log](../../reference/research-log.md) |

## What happened

**The first part.** Apple introduced the C1 in the iPhone 16e (February 2025) as "the first modem designed by Apple and the most power-efficient modem ever on an iPhone" [R-660].

**The second part.** Seven months later the C1X followed, "up to 2x faster than C1". Apple says it is, "for the same cellular technologies, … even faster than the modem in iPhone 16 Pro, while using 30 percent less energy overall" [R-660] **[Established: company statements; performance figures are vendor claims]**.

**The third part.** With the iPhone 18 Pro (9 Sep 2026), Apple said "C2 delivers meaningfully faster uploads when compared to C1X while consuming 15 percent less energy, and now supports mmWave in the U.S." [R-660] **[Established: company statement; the figures are vendor claims]**. Coverage widened one step at a time.

**What is not known.** Apple does not disclose clock speeds, transistor counts, NPU TOPS or DRAM capacity, nor detailed modem specifications. A press report that a later flagship uses a merchant modem was not verified [R-660].

## The engineering behind it

- **A modem is several hard products in one.** It needs a baseband processor that implements a large, evolving standard, RF transceivers and front-end integration, and years of carrier certification ([21-08](../../courses/21-rf-and-microwave-engineering/chapters/21-08-transceiver-architectures.md), [21-12](../../courses/21-rf-and-microwave-engineering/chapters/21-12-modem-baseband-and-standards.md)).
- **Why sequencing matters.** The first products cover the subset of bands and features needed by the devices that ship them. The later ones extend coverage. The first part ships in the product where its limits matter least.
- **The prize is system energy.** A modem's power at the user's actual traffic, including idle and paging, matters more to battery life than peak throughput ([27-02](../../courses/27-system-architectures/chapters/27-02-smartphone-soc.md)). That is the claim Apple chose to make, and it is the right claim to test.
- **The economics.** The design cost is large and fixed, and a captive volume amortizes it ([26-03](../../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md); the build-or-buy comparison is in [26-04](../../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md)). Merchant pricing and patent licensing are also part of a modem's cost, so in-house design changes the cost structure as well as the performance.

## What a diligence team should ask a company that plans to build instead of buy

1. Which bands, carriers and features does the first product cover, and which does it leave out?
2. How many certification cycles does the plan assume, and how long is each?
3. What does the energy claim compare: the same technologies, the same traffic, the same conditions?
4. What standard-essential patent licences remain, whatever is designed in-house?

## Lessons that transfer

- **A vertical-integration claim reads well as "better on the metric we chose, on the subset we cover".** Ask for the comparison on the customer's own usage, and for the features left out.
- **The second generation's ratio to the first is the most informative number in the set.** It shows the team's learning rate.
