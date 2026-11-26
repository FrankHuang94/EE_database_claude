# Problems 27-07 · The AI Datacenter Server and Rack

Chapter: [27-07](../chapters/27-07-ai-datacenter-server-and-rack.md) · Worked solutions: [27-07 solutions](../solutions/27-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** All system parameters are assumed unless a source is cited.

- **Training:** compute is $6ND$ FLOP.
- **Ring all-reduce:** time is $2(p-1)/p \cdot S/B + 2(p-1)\alpha$, with $B$ the bandwidth per device per direction. The hierarchical all-reduce adds a cross-domain ring on $S/p_1$.
- **Checkpoints:** a job on $N$ components of mean life $m$ has $M = m/N$, Young's interval is $\sqrt{2\delta M}$, and the lost fraction is $\delta/\tau + (\tau/2 + R)/M$.
- **Decode step:** time is $\max[(W + BK)/(\eta B_{\text{mem}}),\ 2N_{\text{act}}B/F]$.
- **Year:** 8760 hours.

---

## Problems

### Problem 27-07.1 [A]

**What binds?** For each situation name the level of the system that limits performance: HBM bandwidth, the scale-up fabric, the scale-out network, power, or reliability. Give one design response for each.

- (a) Decoding a large model at batch size 1.
- (b) Tensor parallelism across 16 GPUs in two 8-GPU servers.
- (c) A data-parallel gradient all-reduce across 4,000 GPUs as a flat ring.
- (d) Adding racks to a building with a fixed grid connection.
- (e) A synchronous job on 100,000 accelerators.

### Problem 27-07.2 [A]

**A newer rack.** NVIDIA says GB300 NVL72 has "1.5x larger HBM3E memory" and "1.5x more dense FP4 Tensor Core FLOPS" than Blackwell [R-690]. Take GB200 NVL72's 13.4 TB and 720 PFLOPS of FP4, read as dense (§3.1) **[Contested]**, as the baseline. Find GB300 NVL72's rack HBM and dense FP4, and both per GPU.

### Problem 27-07.3 [A]

**A smaller model.** A dense 70 × 10⁹-parameter model is trained on 15 × 10¹² tokens. Find its training compute and the days of compute on 4,096 GPUs achieving 400 TFLOP/s each.

### Problem 27-07.4 [B]

**A hotter rack.** Repeat Example 27-07.2 with 1.4 kW GPUs, all else equal. Find:

- (a) the busbar load and input power;
- (b) the GPU share;
- (c) the racks and GPUs that 100 MW of facility power at PUE 1.2 supports.

### Problem 27-07.5 [B]

**A server's ring.** Eight GPUs in a server all-reduce 4 GB over links of 450 GB/s per direction. Find:

- (a) the bytes each GPU sends;
- (b) the bandwidth time;
- (c) the latency term at α = 3 µs.

### Problem 27-07.6 [B]

**Could the network do it alone?** In Example 27-07.4, what network bandwidth per GPU would let a flat ring over all 1,152 GPUs match the hierarchical 24.5 ms? Ignore latency. Give it in GB/s and Tb/s and comment.

### Problem 27-07.7 [B]

**Foot the table.** Meta's table of Llama 3's 419 unexpected interruptions lists these counts [R-694]: Faulty GPU 148 (printed 30.1%), GPU HBM3 memory 72, software bug 54, network switch or cable 35, unplanned host maintenance 32, GPU SRAM memory 19, GPU system processor 17, NIC 7, NCCL watchdog timeouts 7, silent data corruption 6, GPU thermal interface and sensor 6, SSD 3, power supply 3, and five categories of 2 each. The printed percentages sum to 94.9%. The text says GPU issues are 58.7% of the total; the GPU categories are faulty GPU, HBM3, SRAM, system processor, silent data corruption, and thermal interface and sensor. Find:

- (a) the sum of the counts;
- (b) the faulty-GPU share implied by its count;
- (c) the GPU share implied by the counts;
- (d) the faulty-GPU count implied by 30.1%, and the GPU share it gives.

What do you conclude?

### Problem 27-07.8 [B]

**A hundred thousand accelerators.** Keep Example 27-07.5's MTBF per GPU-equivalent, $16\,384 \times M$. Find for a 100,000-GPU job:

- (a) the mean time between interruptions;
- (b) Young's interval with 10 s saves;
- (c) the lost fraction with 5-minute restarts, split into checkpoint and restart terms, and the effective training time.

### Problem 27-07.9 [B]

**Odds of a quiet hour.** With Example 27-07.5's mean time between interruptions, find the probability of:

- (a) no interruption in an hour;
- (b) no interruption in three hours;
- (c) at least one in a day.

### Problem 27-07.10 [B]

**Energy of a deadline.** Example 27-07.3(e)'s 40,625 GPUs at 700 W run for 30 days. Find:

- (a) the GPUs' energy in MWh;
- (b) the facility energy with the all-in factor 1.5 and PUE 1.1;
- (c) its cost at $0.08/kWh.

Why is (a) larger than Example 27-07.3's 18.4 GWh?

### Problem 27-07.11 [C]

**A latency target.** For Example 27-07.6's rack and model, find:

- (a) the largest batch that keeps every user at 50 tokens/s or more;
- (b) the throughput and energy per token at that batch;
- (c) the KV-cache memory it uses;
- (d) the compute time per step, to confirm the step is memory-bound.

### Problem 27-07.12 [C]

**Utilization and cost.** Repeat Example 27-07.6(e) at Problem 27-07.11's throughput, first at 60% utilization and then at 30%.

### Problem 27-07.13 [C]

**A synchronized pause.** 16,384 GPUs drop from 700 W to 100 W together while they wait for a checkpoint. Find the step in GPU power and the step at the rack inputs through 97%-efficient power shelves. Why is scaling the step by the all-in factor 1.5 only an upper bound, and why does the step matter to the power-delivery engineer?

### Problem 27-07.14 [B]

**Two derivations.**

- (a) Starting from the lost fraction $f(\tau) = \delta/\tau + (\tau/2 + R)/M$, derive Young's interval. Show that the save and rework terms are equal there, that their sum is $\sqrt{2\delta/M}$, and that the stationary point is a minimum.
- (b) Apply it to δ = 30 s, M = 4 h and R = 5 min: find $\tau^*$, the checkpoint and restart parts of the loss, and the total.
- (c) From the memory-bound step time $t_{\text{step}} = (W + BK)/(\eta B_{\text{mem}})$, with per-user speed $s = 1/t_{\text{step}}$ and throughput $\Theta = Bs$, derive the frontier line $\Theta = \eta B_{\text{mem}}/K - (W/K)s$. For Example 27-07.6's rack and model, find the throughput at $s \to 0$, the per-user speed at which throughput falls to zero, and the slope.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Rack anatomy and reading datasheets | 1, 2 |
| 2. Power budget and accelerators per megawatt | 4, 13 |
| 3. Training compute, time and energy | 3, 10 |
| 4. Ring and hierarchical all-reduce | 1, 5, 6 |
| 5. Interruptions, checkpoints and effective training time | 7, 8, 9, 14 |
| 6. Inference throughput, energy and cost per token | 11, 12, 14 |
