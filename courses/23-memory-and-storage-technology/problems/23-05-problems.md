# Problems 23-05 · HBM in Depth

Chapter: [23-05](../chapters/23-05-hbm-in-depth.md) · Worked solutions: [23-05 solutions](../solutions/23-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** 1 GB = 10⁹ bytes and 1 Gb = 10⁹ bits for bandwidth; die densities in Gb are 2³⁰ bits but stack capacities follow vendors in counting 24 Gb × 12 = 36 GB. Values marked "assumed" are illustrative; specification and vendor values cite the chapter's sources. Problems marked *(lab)* can be checked with `labs/23-05-lab/hbm.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 23-05.1 [A]

**Capacity.** Find the capacity of (a) an 8-high HBM3 stack of 16 Gb dies, (b) a 16-high HBM4 stack of 32 Gb dies, (c) eight stacks of (b) and (d) an 8-high stack of 24 Gb dies.

### Problem 23-05.2 [A]

**Bandwidth and channels.** Find the bandwidth of (a) a 1,024-bit HBM3E stack at 8 Gb/s and (b) a 2,048-bit HBM4 stack at 10 Gb/s. How many pseudo-channels does (c) an HBM3 stack and (d) an HBM4 stack have, and how many data bits does each pseudo-channel carry in (e) HBM3 and (f) HBM4?

### Problem 23-05.3 [A]

**Decode speed.** A 70-billion-parameter model is stored at one byte per parameter. (a) How long does a GPU with 19.2 TB/s take to read it once? (b) What is the resulting upper bound on tokens per second for one sequence? (c) Repeat (b) for four HBM3E stacks at 9.6 Gb/s.

### Problem 23-05.4 [B]

**HBM4 interface energy.** *(lab)* An HBM4 data wire presents 0.9 pF and swings the full 0.75 V of a $V_{DDQ}$ option (both assumed). Find (a) the energy of a 0-to-1 transition, (b) the energy per random bit and (c) the interface power of a stack at 2,048 GB/s.

### Problem 23-05.5 [B]

**A fatter TSV.** *(lab)* A TSV has a 3 µm copper radius, a 0.5 µm oxide liner and a length of 40 µm (assumed). Find (a) its capacitance and (b) its resistance. (c) What is the capacitance with a 0.25 µm liner?

### Problem 23-05.6 [B]

**Keep-out area.** A design uses 30,000 TSVs, each with a 30 µm square keep-out zone, on an 11 × 11 mm die (assumed). What fraction of the die is blocked?

### Problem 23-05.7 [B]

**Height budget.** *(lab)* A 775 µm stack has 150 µm of base die and mold and 15 µm bond gaps (assumed). Find the layer pitch and die thickness for (a, b) 12, (c, d) 16 and (e, f) 20 layers.

### Problem 23-05.8 [B]

**Better gap fill.** *(lab)* Repeat Example 23-05.6 with a gap conductivity of 2.5 W/m·K. Find (a) the gap's thermal resistance, (b) the layer's, and the base rise for (c) 16 and (d) 12 layers.

### Problem 23-05.9 [C]

**Which dies run hot?** *(lab)* In Example 23-05.6's 16-high stack (1.5 W/m·K gaps), the lid holds the top die at 75 °C. Derive the temperature of each die, and find (a) the base die's temperature, (b) the temperature of core die 5 (counting from the bottom), (c) that of core die 6 and (d) how many core dies run above 85 °C, where DRAM refresh doubles.

### Problem 23-05.10 [B]

**Stack yield targets.** (a) What is the yield of a 16-high stack with 99.8% per-layer bond yield? (b) What per-layer yield gives a 16-high stack 95% yield? (c) What would untested dies of 95% yield give?

### Problem 23-05.11 [B]

**Wafers per bit.** HBM takes 25% of a maker's wafers but yields 10% of its bits (assumed). Find (a) HBM's wafers per bit relative to conventional DRAM. If HBM dies hold 1.5 times fewer bits per area and stacks yield 90% (assumed), (b) what factor do these two explain, and (c) what factor remains?

### Problem 23-05.12 [C]

**Bigger packages.** Using the gross-die estimate, find the whole interposers per 300 mm wafer at (a) 2,000 mm² and (b) 4,000 mm², and the packages per month at 120,000 wafers per month and 85% assembly yield (assumed) for (c) 2,000 mm² and (d) 4,000 mm².

### Problem 23-05.13 [A]

**Checking a press release.** Samsung's HBM4 runs at 11.7 Gb/s and its HBM3E at up to 9.6 Gb/s; the HBM4 standard is 8 Gb/s (chapter sources [2], [4]). Find (a) 11.7/8, (b) 11.7/9.6 and (c) 13/9.6, and compare with Samsung's "approximately 46%" and "1.22x".

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Bandwidth and capacity | 1, 2, 3, 13 |
| 2. Interface energy | 4 |
| 3. TSVs | 5, 6 |
| 4. Height and heat | 7, 8, 9 |
| 5. Yield and wafers | 10, 11 |
| 6. Packaging and the business | 12, 13 |
