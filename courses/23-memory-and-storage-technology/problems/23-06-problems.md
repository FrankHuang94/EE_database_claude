# Problems 23-06 · NAND Flash and 3D NAND

Chapter: [23-06](../chapters/23-06-nand-flash-and-3d-nand.md) · Worked solutions: [23-06 solutions](../solutions/23-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $q = 1.602 \times 10^{-19}$ C and $k = 8.617 \times 10^{-5}$ eV/K. Die densities follow vendors in counting 1 Gb = 2³⁰ bits, so 1 Tb = 1,024 Gb. Throughputs use 1 MB/s = 10⁶ bytes/s, and a 16 KiB page holds 16,384 bytes. Values marked "assumed" are illustrative; vendor values cite the chapter's sources. Fowler–Nordheim constants are the chapter's representative $A = 1.25 \times 10^{-6}$ A/V² and $B = 2.33 \times 10^{10}$ V/m. Problems marked *(lab)* can be checked with `labs/23-06-lab/nand.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 23-06.1 [A]

**Electrons and volts.** A cell's control-gate coupling capacitance is 20 aF (assumed). Find (a) the threshold shift per stored electron and (b) the electrons needed to raise the threshold by 2 V. A TLC cell spreads its 8 levels over a 5.6 V window (assumed). Find (c) the level spacing and (d) the electrons that separate adjacent levels.

### Problem 23-06.2 [A]

**Coupling ratio and threshold.** A storage node couples to the control gate through 18 aF and to the channel, source and drain through 12 aF (assumed). The transistor turns on when the node reaches 0.9 V (assumed). Find (a) the coupling ratio and (b) the control-gate threshold of an uncharged cell. With 160 electrons stored, find (c) the threshold shift and (d) the new threshold.

### Problem 23-06.3 [B]

**Tunneling current.** *(lab)* A 6 nm tunnel oxide sits under a storage node at 9 V, with the channel at 0 V. Find (a) the oxide field in MV/cm and (b) the Fowler–Nordheim current density. Over a 40 nm × 40 nm area, find (c) the current and (d) the time for 50 electrons to tunnel at that current. (e) By what factor is the current density at 15 MV/cm larger than at 13 MV/cm?

### Problem 23-06.4 [B]

**Why ISPP steps are exact.** (a) Show that if every program pulse ends when the storage-node voltage falls to the same value, raising the gate pulse by $\Delta V_{pgm}$ adds charge $C_{CG}\,\Delta V_{pgm}$ and raises the threshold by $\Delta V_{pgm}$. (b) For $C_{CG}$ = 16 aF and a 0.3 V step (assumed), how many electrons does each pulse add? (c) Does the answer to (b) depend on the coupling ratio?

### Problem 23-06.5 [A]

**Program time.** A QLC page moves cells from −3 V to +5 V (assumed) with pulse-and-verify loops of 25 µs (assumed). Find (a) the pulses and (b) the program time for a 0.2 V step, and (c) the pulses and (d) the time for a 0.1 V step.

### Problem 23-06.6 [B]

**Margins.** *(lab)* A 6.4 V window has level distributions with σ = 0.07 V (assumed). For MLC find (a) the spacing and (b) the margin $d/2\sigma$. For TLC find (c) the spacing, (d) the margin and (e) the raw bit error rate. For QLC find (f) the spacing, (g) the margin and (h) the raw bit error rate. (i) What margin, and (j) what σ, would give QLC a raw bit error rate of 2 × 10⁻³?

### Problem 23-06.7 [B]

**Gray codes and page reads.** (a) Write a Gray code for the four MLC levels, and show that misreading a cell as an adjacent level corrupts exactly one of its two bits. (b) A TLC cell's three pages need 2, 3 and 2 of the 7 read references. What is the average number of references per page read?

### Problem 23-06.8 [B]

**Density.** A 1 Tb TLC die with 286 layers occupies 50 mm² (assumed). Find (a) its areal density, (b) its density per layer and per bit and (c) the die area per vertical string. (d) How many layers would a TLC die at this lateral density need to match Kioxia's 37.6 Gb/mm²?

### Problem 23-06.9 [B]

**Decks.** A 400-layer stack has a 40 nm layer pitch and a 100 nm channel hole (assumed). Find (a) the stack height, (b) the aspect ratio of a single etch and (c) the aspect ratio per deck with three decks. (d) If one etch can reach an aspect ratio of at most 70 (assumed), what is the ratio of the full stack's aspect ratio to that limit, and (e) how many decks are needed?

### Problem 23-06.10 [B]

**Retention bakes.** A qualification plan assumes an activation energy of 1.0 eV (assumed). Find (a) the acceleration factor of a 125 °C bake over 25 °C use and (b) the bake hours that stand in for 10 years at 25 °C. The dominant mechanism actually has 0.6 eV (assumed). Find (c) its acceleration factor and (d) the years at 25 °C that the bake of (b) really represents.

### Problem 23-06.11 [B]

**Endurance rating.** A 3.84 TB TLC drive is rated at 1 drive write per day for 5 years (assumed). Find (a) its rated host writes and (b) the P/E cycles its NAND must survive at a write amplification of 3 (assumed). (c) What DWPD can a QLC drive of any capacity offer over 5 years with 1,500 cycles (assumed) at the same write amplification?

### Problem 23-06.12 [B]

**Throughput.** A die has 6 planes of 16 KiB pages (assumed). Find its write throughput with (a) a TLC $t_{PROG}$ of 400 µs and (b) a QLC $t_{PROG}$ of 2 ms (assumed). How many dies does a 12 GB/s write rate need with (c) TLC and (d) QLC? (e) What is the throughput in SLC mode at $t_{PROG}$ = 60 µs (assumed)?

### Problem 23-06.13 [C]

**Choosing bits per cell.** An SSD's ECC can correct raw bit error rates up to 5 × 10⁻³ (assumed). The window is 6 V, and at end of life σ = 0.09 V (assumed). (a) Find QLC's margin and (b) its raw bit error rate. Does QLC meet the ECC limit? (c) Find TLC's margin and (d) its raw bit error rate. (e) What is the largest end-of-life σ at which QLC still meets the limit, and (f) what margin does that correspond to?

### Problem 23-06.14 [C]

**Testing a vendor's claims.** A vendor's new 2 Tb QLC die "writes at 4.8 Gb/s". It has 6 planes of 16 KiB pages and $t_{PROG}$ = 2.5 ms (assumed). Find (a) its sustained write throughput and (b) that as a percentage of the 600 MB/s interface. (c) How many such dies must share one channel to keep its interface busy with writes? A second claim is a 400-layer TLC die at 30 Gb/mm². Find (d) its density per layer and per bit and (e) how far that falls below the 332-layer QLC die of Example 23-06.5, in percent.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Charge and threshold | 1, 2 |
| 2. Tunneling and ISPP | 3, 4, 5 |
| 3. Multi-level cells and RBER | 6, 7, 13 |
| 4. Array, 3D structure and density | 8, 9, 14 |
| 5. Endurance and retention | 10, 11 |
| 6. Throughput and claims | 12, 14 |
