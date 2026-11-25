# Problems 23-01 · The Memory Hierarchy and the Memory Wall

Chapter: [23-01](../chapters/23-01-memory-hierarchy-and-memory-wall.md) · Worked solutions: [23-01 solutions](../solutions/23-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** 1 GB = 10⁹ B and 1 TB/s = 10¹² B/s. Energies at 45 nm are Horowitz's [chapter source 1]. Values marked "assumed" are illustrative. Problems marked *(lab)* can be checked with `labs/23-01-lab/memwall.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 23-01.1 [A]

**Relative costs.** From the 45 nm table (32-bit SRAM read from 8 KB 5 pJ, 32-bit DRAM read 640 pJ, 32-bit integer add 0.1 pJ), find (a) the ratio of a DRAM read to an SRAM read, (b) the ratio of a DRAM read to an integer add and (c) the energy to read 1 GB from DRAM in 32-bit words.

### Problem 23-01.2 [A]

**Energy per bit and power.** A memory system delivers 4 TB/s at 5 pJ/bit (assumed). Find (a) its power, (b) the energy to read 100 GB and (c) how long that read takes.

### Problem 23-01.3 [A]

**Interfaces.** Find the bandwidth of (a) a 384-bit interface at 28 Gb/s per pin and (b) a 1,024-bit interface at 8 Gb/s per pin. (c) How many pins at 32 Gb/s deliver 1 TB/s?

### Problem 23-01.4 [A]

**Little's law at one stack.** An HBM stack delivers 1 TB/s with a loaded latency of 400 ns (assumed). Find (a) the data in flight and (b) the number of 64-byte requests it represents. (c) If the controller can track only 2,048 outstanding requests, what bandwidth can it reach?

### Problem 23-01.5 [B]

**A longer wire.** A 2 mm wire has 0.18 fF/µm and swings 0.8 V (assumed). Find (a) its capacitance, (b) the supply energy per 0 → 1 transition and the energy per bit for (c) random data and (d) alternating data. (e) A bus-inversion code lowers the transition probability to 0.2 (assumed): what is the energy per bit?

### Problem 23-01.6 [B]

**Activation energy and locality.** Opening a DRAM row of 8,192 bits costs 1.6 nJ (assumed). Find the activation energy per useful bit when (a) the whole row is used and (b) only 64 bytes are. (c) What is the ratio? (d) How many bytes must each activation deliver to keep activation energy at or below 0.5 pJ per bit?

### Problem 23-01.7 [B]

**The wall's pace.** Peak FLOPS grow 3.0× and bandwidth 1.6× every two years. (a) How long does the ridge point take to double? (b) What bandwidth growth per two years would hold the ridge constant? (c) A kernel of fixed intensity sits exactly at the ridge today. After ten years at these rates, what fraction of peak compute does it reach?

### Problem 23-01.8 [B]

**Decode at batch 1.** *(lab)* A 7-billion-parameter model runs on a 3.35 TB/s GPU. Counting weight reads only, find the largest tokens per second at batch 1 with (a) BF16 (2 bytes per weight), (b) FP8 and (c) 4-bit weights.

### Problem 23-01.9 [B]

**KV-cache sizing.** A model has 32 layers and 8 KV heads of dimension 128, with BF16 KV entries. Find (a) the KV bytes per token and (b) the KV cache of one 131,072-token sequence. (c) What would (b) be with 32 KV heads (full multi-head attention)?

### Problem 23-01.10 [B]

**Capacity sets the batch.** *(lab)* The model of Problem 23-01.9 has 7 billion BF16 parameters and serves 32,768-token contexts from an 80 GB, 3.35 TB/s GPU. Find (a) the KV cache per sequence, (b) the largest batch, (c) the bytes per decode step, (d) the memory time per step and (e) the tokens per second.

### Problem 23-01.11 [C]

**Where batching runs out.** Show that the decode intensity $I(B) = BF_1/(W + BK)$, where $F_1$ is the FLOPs per sequence per step and $K$ the KV bytes per sequence, rises monotonically with $B$ towards $F_1/K$. (a) At what batch $B_{1/2}$ does it reach half its limit, and what does that batch mean physically? (b) Evaluate $B_{1/2}$ for Example 23-01.7.

### Problem 23-01.12 [C]

**SRAM against HBM, per token.** A 40-billion-parameter FP8 model is held entirely in on-wafer SRAM at 5 pJ per 32-bit read (the 45 nm figure, assumed to apply). Find (a) the SRAM energy per bit, the weight-read energy per token at batch 1 (b) from SRAM and (c) from HBM at the all-in 6.86 pJ/bit, and (d) their ratio. (e) Name two reasons the real gap is smaller.

### Problem 23-01.13 [C]

**A memory-power target.** A future GPU must deliver 20 TB/s within a 300 W memory budget. Find (a) the largest all-in energy per bit, (b) the factor of improvement over the H200's measured 6.86 pJ/bit and (c) the number of 2,048-bit stacks at 10 Gb/s per pin needed for the bandwidth.

### Problem 23-01.14 [B]

**Can the cores fill the pipe?** A 12-core CPU's cores can each keep 24 misses of 64 bytes outstanding, and the loaded latency is 90 ns (assumed). (a) What bandwidth can the cores sustain at most? (b) If the DRAM delivers 160 GB/s, which limit binds? (c) What bandwidth can one core reach alone?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Place technologies in the hierarchy by energy and cost | 1, 6, 12 |
| 2. Derive wire energy; convert energy, bandwidth and power | 2, 5, 13 |
| 3. Interface bandwidth and Little's law | 3, 4, 14 |
| 4. Quantify the memory wall | 7, 13 |
| 5. Decode intensity, capacity, step time and energy | 8, 9, 10, 11, 12 |
