<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 27 · System Architectures (Case-Study Course)

End-to-end analyses of real product classes (smartphone SoC, wearables, PC SoC, automotive E/E and ADAS compute, the AI datacenter server and rack, edge AI/IoT), each decomposed with the tools of the earlier courses into power, thermal, area, cost and performance budgets.

| | |
|---|---|
| **Term** | 7 |
| **Study hours** | ≈ 60 |
| **University equivalents** | Systems-design case-study capstone seminar |
| **Textbook alignment** | Selected public sources (Hot Chips, ISSCC, teardown reports, company technical docs) cited per chapter |
| **Free courses** | Hot Chips symposium presentations (public) |
| **Prerequisites** | [18 · Embedded Systems and Microcontrollers](../18-embedded-systems-and-microcontrollers/README.md), [19 · Digital VLSI Design](../19-digital-vlsi-design/README.md), [20 · Analog and Mixed-Signal IC Design](../20-analog-and-mixed-signal-ic-design/README.md), [21 · RF and Microwave Engineering](../21-rf-and-microwave-engineering/README.md), [22 · Power Electronics and Energy Conversion](../22-power-electronics-and-energy-conversion/README.md), [23 · Memory and Storage Technology](../23-memory-and-storage-technology/README.md), [24 · High-Speed I/O, Signal Integrity and Photonics](../24-high-speed-io-signal-integrity-and-photonics/README.md), [25 · Semiconductor Fabrication, Packaging, Test and Reliability](../25-fabrication-packaging-test-and-reliability/README.md) |
| **FE areas** | — |
| **Deeper** | Companion repo(s): datacenter networking; LLM inference engineering |

## Learning objectives

1. Decompose a product into subsystems with power, thermal, area, BOM and performance budgets.
2. Explain the architecture of each case-study system and the tradeoffs that shaped it.
3. Trace a system-level requirement down to device- and circuit-level consequences.
4. Identify where value and margin accrue in each system's silicon content.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [27-01 · Method: Analyzing a System End to End](chapters/27-01-system-analysis-method.md) | 4 | ✅ verified | [problems](problems/27-01-problems.md) · [solutions](solutions/27-01-solutions.md) · [lab](labs/27-01-lab/README.md) · [verify](verify/verify_27_01.py) |
| [27-02 · The Smartphone SoC](chapters/27-02-smartphone-soc.md) | 8 | ✅ verified | [problems](problems/27-02-problems.md) · [solutions](solutions/27-02-solutions.md) · [lab](labs/27-02-lab/README.md) · [verify](verify/verify_27_02.py) |
| [27-03 · Wearables I: The Smartwatch](chapters/27-03-wearables-smartwatch.md) | 7 | ✅ verified | [problems](problems/27-03-problems.md) · [solutions](solutions/27-03-solutions.md) · [lab](labs/27-03-lab/README.md) · [verify](verify/verify_27_03.py) |
| [27-04 · Wearables II: Earbuds and Smart Glasses / XR](chapters/27-04-wearables-earbuds-and-glasses.md) | 8 | ✅ verified | [problems](problems/27-04-problems.md) · [solutions](solutions/27-04-solutions.md) · [lab](labs/27-04-lab/README.md) · [verify](verify/verify_27_04.py) |
| [27-05 · The PC SoC](chapters/27-05-pc-soc.md) | 6 | ✅ verified | [problems](problems/27-05-problems.md) · [solutions](solutions/27-05-solutions.md) · [lab](labs/27-05-lab/README.md) · [verify](verify/verify_27_05.py) |
| [27-06 · Automotive E/E Architecture and ADAS Compute](chapters/27-06-automotive-ee-architecture.md) | 9 | ✅ verified | [problems](problems/27-06-problems.md) · [solutions](solutions/27-06-solutions.md) · [lab](labs/27-06-lab/README.md) · [verify](verify/verify_27_06.py) |
| [27-07 · The AI Datacenter Server and Rack](chapters/27-07-ai-datacenter-server-and-rack.md) | 10 | ✅ verified | [problems](problems/27-07-problems.md) · [solutions](solutions/27-07-solutions.md) · [lab](labs/27-07-lab/README.md) · [verify](verify/verify_27_07.py) |
| [27-08 · Edge AI and IoT](chapters/27-08-edge-ai-and-iot.md) | 6 | ✅ verified | [problems](problems/27-08-problems.md) · [solutions](solutions/27-08-solutions.md) · [lab](labs/27-08-lab/README.md) · [verify](verify/verify_27_08.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/27-system-architectures.csv) · [Equation sheet](../../reference/equation-sheets/27-system-architectures.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 27 is planned at about 60 hours: the chapters' own estimates add to 58, plus about 2 hours of review; allow a further 3 hours for the exam. It is a case-study course. Each chapter takes one product class and asks the same questions: what binds first (energy, heat, bandwidth, latency, cost or reliability), how much each block costs in that currency, and which knob moves the answer most. 27-01 teaches the method, and the other seven chapters apply it from a coin cell to a 100 kW rack. The skill is not memorizing products. It is building a small, honest budget quickly, finding the term that dominates, and knowing where the first-order model stops being true. The course draws on almost every earlier course:

- Courses 14 and 23: roofline and machine balance, caches, DRAM, HBM and the KV cache;
- Courses 18, 21 and 22: low-power MCUs, link budgets and radios, converters, batteries and datacenter power delivery;
- Course 24: SerDes, scale-up links and optics;
- Course 25: thermal resistance and liquid cooling, dies per wafer and yield, reliability and functional safety;
- Course 26: requirements, error budgets, cost stacks and TCO.

The eight chapters fall into four blocks:

- **Method (27-01).** Converter-chain power budgets and battery life; sustained power and burst time from a first-order thermal model; BOM and margin; bottlenecks by roofline, Amdahl and Little's law; and the shadow price of a watt under a power cap.
- **Personal devices (27-02 to 27-05).** The phone SoC's DVFS energy optimum and memory traffic; the smartwatch's always-on domain, display physics, sensor batching and BLE connection events; earbuds' ANC delay limits, LE Audio and case recharges; glasses' heat budget and headsets' pixels and latency; the laptop's residency-weighted battery life, turbo under an exponentially weighted limit, local-AI decode and prefill bounds, and chiplet cost.
- **The car (27-06).** CAN from first principles (stuffing, load, response-time analysis); sensor bandwidth and compute sizing; the range cost of compute; latency as stopping distance; diagnostic coverage against an ASIL budget.
- **The AI datacenter and the edge (27-07 and 27-08).** Rack datasheets normalized per device; rack and facility power; training compute, utilization and energy; ring and hierarchical all-reduce; failures and Young's checkpoint interval; the inference frontier and token cost. Then microcontroller inference, "send the answer, not the data", LoRa airtime and duty cycles, battery life with self-discharge, energy harvesting, and the cost of security over a product's life.

Work at least the [A] and [B] problems of every chapter; the [C] problems are where a model meets a decision. The labs are Python models imported by their notebooks, all run in CI:

- `sysbudget.py` (27-01): power trees, thermal RC bursts, BOM roll-up and bottleneck tools;
- `socmodel.py` (27-02): energy per instruction against frequency, memory traffic and the SoC power envelope;
- `watchmodel.py` (27-03): the day-in-the-life budget, display power, batching and BLE events;
- `headworn.py` (27-04): speaker power, ANC residual, LE Audio airtime, glasses heat and foveation;
- `pcsoc.py` (27-05): residency, turbo, decode and prefill bounds, NPU energy and chiplet cost;
- `automodel.py` (27-06): CAN frames and response times, sensor rates, range loss and stopping distance;
- `rackmodel.py` (27-07): rack power, training compute, all-reduce, checkpointing and token economics;
- `edgemodel.py` (27-08): MCU inference, LoRa time on air, battery life, harvesting and security costs.

**What to master cold.** The [equation sheet](../../reference/equation-sheets/27-system-architectures.md) collects the relations; these are the ideas behind them:

- every product has one binding constraint at a time, and the budget that exposes it is more useful than any spec sheet (27-01);
- sustained power is set by heat leaving the case, not by the chip; bursts borrow thermal capacitance and must be repaid (27-01, 27-04);
- energy per operation has a minimum: below the optimal frequency, leakage per instruction rises faster than dynamic energy falls (27-02);
- always-on design is Amdahl's law for energy: shrink the biggest term, then the next one becomes the problem (27-03, 27-08);
- a delay of $\tau$ caps active noise cancellation, and gain error caps it at low frequency (27-04);
- local AI on a laptop or phone is bounded by memory bandwidth for decode and by compute for prefill (27-05);
- worst-case response time, not average load, is the safety number on a shared bus; latency is distance at speed (27-06);
- normalize rack datasheets per device, per direction and per precision before comparing; machine balance converges because HBM is shared technology (27-07);
- the bandwidth ladder (HBM, scale-up, scale-out) decides which parallelism runs where; a bigger scale-up domain divides network traffic (27-07);
- large jobs fail in proportion to their size; checkpoints are tuned by a square root, but restart time dominates at scale (27-07);
- inference trades throughput against per-user speed along a frontier, and capital, through utilization, dominates token cost (27-07);
- at the edge, send the answer, not the data; range is bought with airtime, and the network's density is a battery-life specification (27-08).

**After this course.** Course 28 turns these case studies into technical diligence: evaluating a technology, validating claims, judging silicon maturity, and asking each chapter's Practitioner-lens questions. Capstone C3 (a wearable sensor node) applies 27-01, 27-03 and 27-08 directly. The Term 7 FE checkpoint follows Course 28.
