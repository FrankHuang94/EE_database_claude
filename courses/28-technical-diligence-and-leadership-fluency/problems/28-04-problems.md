# Problems 28-04 · Domain Question Banks I: Digital/CPU, AI Accelerators, Memory, Interconnect and Optics

Chapter: [28-04](../chapters/28-04-question-banks-digital-ai-memory-interconnect.md) · Worked solutions: [28-04 solutions](../solutions/28-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Parameters are assumed unless a source is cited. Dynamic power scales as $f^3$ along the voltage–frequency line. Decode intensity is $2B/b_w$ FLOP per byte (KV cache ignored). Power is bits per second × energy per bit.

---

## Problems

### Problem 28-04.1 [A]

**Strong, partial or evasive?** Classify each answer to "what utilization do you reach on our 70B model at 50 ms per token?" and say what it would take to make the weaker ones strong:

- (a) "Our architecture is designed for exactly this workload."
- (b) "About 40%, on Llama-class 70B at FP8, batch 32, measured last month on B0 silicon; it drops to about 25% at 20 ms per token because the batch must shrink."
- (c) "We'll send you the numbers after the meeting."
- (d) "Customers tell us we beat the GPU."

### Problem 28-04.2 [B]

**Another iso-power claim.** A vendor claims 30% more performance at the same power with 12% more IPC, and says capacitance is unchanged. Find the frequency gain, the power factor it costs, and the reduction in energy per operation required.

### Problem 28-04.3 [B]

**Bandwidth per core.** A server CPU has 12 channels of DDR5-6400 (64 data bits per channel). Find the bandwidth per channel and in total, the bandwidth per core for 128 cores and for 96 cores, and their ratio.

### Problem 28-04.4 [B]

**A bigger accelerator.** An accelerator has 5 PFLOP/s of dense FP8 and 8 TB/s. Find its ridge point; the batch at which decode reaches the ridge with FP8 weights and with FP4 weights; and the attainable throughput and share of peak at batch 16 with FP8 weights.

### Problem 28-04.5 [B]

**Will it fit?** A 405-billion-parameter model at FP8 serves 64 sequences with 2 GB of KV cache each, on accelerators with 192 GB each. Find the weight memory, the KV memory, the total, the accelerators needed for weights alone and for everything, and the memory left over.

### Problem 28-04.6 [B]

**HBM generations.** Find the bandwidth per stack of Micron's HBM3E at 1,024 bits and 9.2 GT/s [R-475] and of JEDEC HBM4 at 2,048 bits and 8 Gb/s [R-520], their ratio, and the total for eight HBM4 stacks at 11.7 Gb/s.

### Problem 28-04.7 [A]

**Memory power.** What does 8 TB/s of reads cost at 6.5 pJ/bit?

### Problem 28-04.8 [B]

**A 51.2 Tb/s switch.** Its SerDes use 3 pJ/bit analog plus 2 pJ/bit of DSP (assumed). Find the total SerDes power and the analog part.

### Problem 28-04.9 [B]

**A chiplet link.** Two chiplets exchange 2 TB/s. Find the link power at 0.25 and 0.5 pJ/bit [R-524], and the die edge needed at UCIe-A's shoreline of 165 and 1,317 GB/s per mm.

### Problem 28-04.10 [B]

**A smaller optical switch.** A switch has 64 ports of 800 Gb/s. Using 25 W (pluggable) and 5 W (CPO) per port [R-543], find the optics power each way and the energy per bit. An external laser module delivers 20 dBm per fiber core [R-548]; find that power in milliwatts and the electrical power it needs at an assumed 15% wall-plug efficiency.

### Problem 28-04.11 [C]

**Scoring with care.** (a) In Example 28-04.6, count the two repeated "strong" answers once and find the posterior. (b) From a prior of 0.5, with one evasive answer (ratio 0.4) already recorded, how many independent strong answers (ratio 3 each) are needed to reach 95%?

### Problem 28-04.12 [C]

**Three derivations.**

- (a) From performance $= \text{IPC} \times f$ and $P \propto Cf^3$ along the voltage–frequency line, derive the energy-per-operation reduction an iso-power claim of ratio $R$ with IPC ratio $g_{\text{IPC}}$ and capacitance ratio $g_C$ requires.
- (b) Show that decode with $B$ sequences and $b_w$ bytes per weight has intensity $2B/b_w$ FLOP per byte of weights, and derive the batch at which it reaches a ridge point $F/B_{\text{mem}}$.
- (c) Show that a link's power is its bit rate times its energy per bit, and that for a fixed power budget the bit rate is inversely proportional to the energy per bit.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Digital and CPU claims | 2, 3, 12 |
| 2. AI accelerator claims | 4, 5, 12 |
| 3. Memory bandwidth and power | 6, 7 |
| 4. Interconnect and optics | 8, 9, 10, 12 |
| 5. Scoring answers as evidence | 1, 11 |
