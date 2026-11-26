# Problems 27-02 · The Smartphone SoC

Chapter: [27-02](../chapters/27-02-smartphone-soc.md) · Worked solutions: [27-02 solutions](../solutions/27-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Core, cache, DRAM-energy and cost parameters are assumed unless a source is cited. Energy per instruction is $E = c(V_0 + kf)^2/\text{IPC} + P_s/(\text{IPC}\cdot f)$ and core power is $c(V_0 + kf)^2f + P_s$ (c in nF, f in GHz, V in volts). The big core of Example 27-02.2 has IPC 6, $c$ = 1.2 nF, $V = 0.45 + 0.12f$, $P_s$ = 0.10 W and $f_{max}$ = 4.2 GHz. Bandwidth is $Rw/8$ for a data rate $R$ and a bus width $w$ bits. Dies per wafer and yield follow 25-04 (300 mm wafers, rounded down; Poisson yield).

---

## Problems

### Problem 27-02.1 [A]

**Which block?** Name the SoC block best suited to each task and say why in a phrase: (a) listening for a wake word with the screen off; (b) encoding 4K video; (c) syncing email in the background; (d) a game's 3D rendering; (e) merging several exposures into one HDR photo.

### Problem 27-02.2 [A]

**LPDDR6 bandwidth.** Find the peak bandwidth of a 64-bit interface at 14,400 MT/s and at 10,667 MT/s (the ends of LPDDR6's range [R-667]), and their ratio.

### Problem 27-02.3 [B]

**The display's share.** A 2,400 × 1,080 display at 4 bytes per pixel refreshes at 120 Hz. Find the bandwidth of one read per refresh, the same at an always-on 1 Hz refresh, and their ratio. Why do phones drop the refresh rate when the screen is static?

### Problem 27-02.4 [B]

**What the SLC saves.** Clients demand 60 GB/s, of which 45 GB/s comes from clients whose traffic the SLC catches 35% of the time. Find the DRAM traffic and, at 4.0 pJ/bit of DRAM energy, the power saved.

### Problem 27-02.5 [B]

**A mid-size core.** A core has IPC 4, $c$ = 0.6 nF, $V = 0.45 + 0.15f$ and $P_s$ = 0.05 W. At 2.0 GHz find (a) the energy per instruction, (b) the power and the performance, and (c) check that power equals energy per instruction times performance.

### Problem 27-02.6 [B]

**Its minimum-energy point.** For the core of Problem 27-02.5, find the minimum-energy frequency, the voltage there and the energy per instruction.

### Problem 27-02.7 [B]

**"50 percent more bandwidth."** Apple says A20 Pro has "50 percent more memory bandwidth than A19 Pro" [R-660]. If the earlier chip used a 64-bit interface at 9,600 MT/s (an assumption for this problem), find (a) the data rate a 64-bit bus would need, (b) the bus width at 9,600 MT/s, and (c) the resulting bandwidth. Which of (a) or (b) falls inside LPDDR6's data-rate range [R-667]?

### Problem 27-02.8 [B]

**A gentler throttle.** For the big core of the conventions, find the frequency at which it draws 2.0 W, its fraction of 4.2 GHz and its performance in GIPS.

### Problem 27-02.9 [B]

**A bigger model.** A 7-billion-parameter model with 4-bit weights runs on a 64-bit LPDDR6 interface at 14,400 MT/s. Find (a) the bytes per token and the bandwidth-bound decode speed, and (b) the share of a 12 GB DRAM that the weights occupy.

### Problem 27-02.10 [B]

**Integrate the modem or not?** A 126.2 mm² AP with an integrated modem is built on $18,500 wafers at $D_0$ = 0.10 cm⁻². Removing the modem would cut the AP to 111.2 mm²; a separate 25 mm² modem on an older $12,000 wafer at $D_0$ = 0.08 cm⁻² would add $1.50 of package and link cost (all assumed). Find (a) the integrated AP's cost per good die, (b) the smaller AP's cost, (c) the separate modem's cost and the total. Which is cheaper, and what else would the decision weigh?

### Problem 27-02.11 [C]

**Race or pace?** A task of 2 × 10⁹ instructions must finish within 1 s on the big core of the conventions. Option A paces the core at the slowest frequency that meets the deadline and leaves it on for the full second. Option B runs at 4.2 GHz and then power-gates the core (no leakage afterwards). (a) Find each option's energy. (b) Repeat with a hot die, $P_s$ = 0.6 W. (c) What decides which option wins?

### Problem 27-02.12 [C]

**Memory prices and margin.** A phone's BOM is $500, of which memory is $50; other COGS add $40; the net price is $1,099. Memory prices triple, other costs unchanged. Find (a) memory's new share of the BOM, (b) the gross margin before and after, and (c) the price that would restore the original margin.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Block diagram and integration choices | 1, 10 |
| 2. Heterogeneous cores, crossover and minimum energy | 5, 6, 11 |
| 3. Memory bandwidth, SLC and on-device models | 2, 3, 4, 7, 9 |
| 4. Peak against sustained power | 8, 11 |
| 5. Die cost and the BOM | 10, 12 |
