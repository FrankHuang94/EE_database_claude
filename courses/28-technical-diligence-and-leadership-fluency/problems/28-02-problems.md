# Problems 28-02 · Validating Claims: TOPS/W, Benchmarks, Tapeout Status

Chapter: [28-02](../chapters/28-02-validating-claims.md) · Worked solutions: [28-02 solutions](../solutions/28-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** A MAC is two operations. Parameters are assumed unless a source is cited. Dynamic power scales as $V^2f$ and leakage is ignored unless stated. A month is 30.44 days and a week 168 hours.

---

## Problems

### Problem 28-02.1 [A]

**Which product is the headline?** A 128 × 128 systolic array of INT8 MACs runs at 940 MHz. The brief says "123 TOPS". Find the dense INT8 peak, the peaks with INT4 alone and with INT4 plus 2:4 sparsity, and the delivered dense INT8 throughput at 40% utilization. Which combination is the headline?

### Problem 28-02.2 [A]

**Efficiencies as energies.** Convert 10, 2.5 and 50 TOPS/W to femtojoules per operation and picojoules per MAC.

### Problem 28-02.3 [B]

**A roofline.** An accelerator has 200 TOPS of dense peak and 3.2 TB/s of HBM. Find its ridge point, and its attainable throughput and utilization at 40 and at 10 operations per byte.

### Problem 28-02.4 [B]

**An energy floor.** At an advanced node the arithmetic costs 0.05 pJ per operation and on-chip SRAM 0.6 pJ per byte (both assumed). A kernel performs 10 operations per SRAM byte and 500 per HBM2 byte (31.2 pJ per byte [R-459]). Find the minimum energy per operation, the best possible efficiency, and each term's share.

### Problem 28-02.5 [B]

**The efficiency at peak.** A chip measures 30 TOPS/W at 0.55 V; its peak throughput is quoted at 0.85 V. With dynamic power only, what is its efficiency at the peak point?

### Problem 28-02.6 [B]

**An edge module.** An NPU delivers 26 TOPS and its brief claims 10 TOPS/W, measured on the NPU's own rail at 2.6 W. The module's SoC draws 4.0 W in all, its LPDDR 1.2 W and its I/O 0.3 W, through a PMIC that is 85% efficient (all assumed). Find the module's battery-side power and efficiency.

### Problem 28-02.7 [B]

**Export screening.** Find the TPP of (a) a GPU with 1,000 dense FP16 TFLOPS (500 MacTOPS at 16 bits) and (b) a chip with 600 dense INT8 TOPS. (c) Find (a)'s performance density on an 800 mm² die (TPP per mm²), and compare both with the thresholds of 4800 and 5.92 [R-659].

### Problem 28-02.8 [B]

**The reference machine matters.** Two workloads take 10 s and 10 s on reference machine R, and 5 s and 20 s on reference machine R′. Machine A takes 5 s and 20 s; machine B takes 8 s and 8 s. Compute A's and B's arithmetic and geometric mean speedups against R and against R′. Which average gives a ranking that does not depend on the reference?

### Problem 28-02.9 [B]

**Best of five, best of twenty.** A product's per-workload log speedups have median 1.3× and standard deviation 0.25. Using $\operatorname{E}[Z_{(5)}]$ and $\operatorname{E}[Z_{(20)}]$, find the expected best-of-five and best-of-twenty headlines.

### Problem 28-02.10 [A]

**Reading MLPerf.** For each claim, say which MLPerf division and scenario would support it, or why the cited result does not: (a) "our chip serves a chatbot at the lowest cost per token within a 50 ms per-token latency"; (b) "our new model runs faster on our chip than the reference model on the leader's" (an open-division result); (c) "highest images per second" (an offline result) used to support a claim about a camera that must process every frame within 30 ms.

### Problem 28-02.11 [A]

**Fab cycle from layers.** A process uses 70 mask layers. Find the fab cycle in weeks at 1.2 and at 1.5 days per layer [R-020].

### Problem 28-02.12 [C]

**A twelve-month plan.** A plan reaches production 12 months after tape-out with one metal-only respin. Assume masks 2.5 weeks, fab 14 weeks, packaging and test 3 weeks, bring-up 10 weeks; a metal-only respin from held wafers takes 1 week of masks and 5 weeks of fab, plus packaging and test; a full respin repeats 2.5 + 14 + 3 weeks; qualification is 1000 hours plus 2 weeks.

- (a) Find the time to production with a metal-only respin and with a full respin, in weeks and months.
- (b) If a metal-only fix suffices with probability 0.6 and a full respin is needed otherwise, find the expected time and the probability of meeting 12 months.

### Problem 28-02.13 [C]

**A startup's inference claim.** A startup claims 1,000 TOPS (INT8) at 75 W, with 200 GB/s of LPDDR, and "4,000 tokens per second on a 7-billion-parameter INT8 model". Find the claimed efficiency, the batch-1 decode bound (weights read once per token, 27-05 §3.4), and the batch the claim implies if it is a throughput across sequences. What should you ask?

### Problem 28-02.14 [C]

**Three derivations.**

- (a) From $P = \alpha CV^2f$ and $F \propto f$, show that the energy per operation does not depend on $f$, and derive the ratio of efficiencies at two voltages. Evaluate it for 0.60 V and 0.90 V.
- (b) Show that the ratio of two machines' geometric-mean speedups over a reference does not depend on the reference.
- (c) From $E_{\text{op}} \ge E_{\text{arith}} + E_\ell/I_\ell$, derive the minimum intensity $I_\ell$ for a memory level to use at most a fraction $\beta$ of a budget $E_{\text{op}}$.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Peak, precision, sparsity and delivered throughput | 1, 3, 7, 13 |
| 2. Efficiency as energy per operation | 2, 4, 5, 14 |
| 3. Operating point and power boundary | 5, 6 |
| 4. Benchmarks: divisions, means and selection | 8, 9, 10, 14 |
| 5. Silicon status and schedules | 11, 12 |
