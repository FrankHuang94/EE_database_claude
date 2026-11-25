# Problems 23-02 · SRAM Technology

Chapter: [23-02](../chapters/23-02-sram-technology.md) · Worked solutions: [23-02 solutions](../solutions/23-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Transistors follow the square law with λ = 0 (09-08). 1 Mb = 10⁶ bits unless a problem says otherwise; 1 MiB = 2²³ bits. Values marked "assumed" are illustrative. Problems marked *(lab)* can be checked with `labs/23-02-lab/sramtech.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 23-02.1 [A]

**Intel's cells.** Find the raw bitcell density of (a) Intel 7's 0.0312 µm² cell and (b) Intel 4's 0.024 µm² cell, and (c) the area shrink from one to the other.

### Problem 23-02.2 [A]

**What is a megabit?** A paper reports 38.1 Mb/mm² meaning 2²⁰ bits per Mb. Find (a) the density in 10⁶ bits/mm² and (b) the array efficiency with a 0.021 µm² cell.

### Problem 23-02.3 [A]

**Sigma for an L2.** *(lab)* What margin, in standard deviations, does a 256 KiB array (2²¹ bits) need for 99.9% yield without repair?

### Problem 23-02.4 [B]

**A cache-heavy die.** A die is 55% SRAM (assumed). On the next node logic shrinks 1.7 times and the bitcell 1.05 times (assumed). Find (a) the new die area as a fraction of the old, (b) the SRAM share of the new die and (c) the effective shrink.

### Problem 23-02.5 [B]

**Read disturb.** With $V_{DD}$ = 0.8 V and $V_{TN}$ = 0.32 V and the wordline at $V_{DD}$, find the read-disturb voltage for (a) $k_{PD} = k_{PG}$ and (b) $k_{PD} = 2k_{PG}$ (cell ratio 2). (c) By what percentage does the cell ratio of 2 cut the disturbance?

### Problem 23-02.6 [B]

**Write margin and assist.** *(lab)* A cell has $V_{DD}$ = 0.75 V, $V_{TN} = |V_{TP}|$ = 0.3 V, $k_{PG} = k_{PD}$ = 120 µA/V² and $k_{PU}$ = 60 µA/V² (assumed). Find (a) the switching threshold of the inverter that must flip and (b) the written node with nominal devices. With a mismatch δ against the write (pass gate $V_{TN}$ + δ, pull-up $|V_{TP}|$ − δ), find (c) the δ at which the write just fails, (d) the written node at δ = 100 mV and (e) the negative bitline that restores that write.

### Problem 23-02.7 [B]

**A long bitline.** A bitline carries 1,024 cells of 0.08 fF each plus 4 fF fixed. The sense amplifier needs 80 mV, and the cell sinks 25 µA (assumed). Find (a) the bitline time and (b) the cell current that would cut it to 150 ps. (c) By what factor must the cell current rise?

### Problem 23-02.8 [B]

**Bitline length and density.** *(lab)* With a 0.021 µm² cell, 0.8 µm² of column periphery per bitline and 0.0015 µm² of other overhead per bit (assumed), find the area per bit and the density for (a, b) 128 and (c, d) 256 cells per bitline, and (e) the density gain.

### Problem 23-02.9 [B]

**Vmin with and without ECC.** A margin has slope 0.25 V/V, vanishes at 0.2 V and has σ = 0.5 σ_VT, with σ_VT = 22 mV (assumed). For a 32 MiB array (2²⁸ bits) at 99% yield, find (a) the sigma needed and (b) Vmin. (c) ECC relaxes the per-cell requirement to 4.5σ (assumed): what is Vmin then? (d) How much Vmin does ECC save?

### Problem 23-02.10 [B]

**Retention.** A 32 MiB array (2²⁸ bits) leaks 8 pA per bit at 0.75 V (assumed). Find (a) the leakage current and (b) the power. In retention at 0.50 V, with leakage halving every 90 mV (assumed), find (c) the leakage factor, (d) the current, (e) the power and (f) the saving.

### Problem 23-02.11 [C]

**Read disturb for any cell ratio.** Derive the read-disturb voltage for a cell ratio $\beta = k_{PD}/k_{PG}$ with the wordline at $V_{DD}$, and show that it reduces to §3.4's result for $\beta = 1$. With $V_{DD} - V_{TN}$ = 0.4 V, evaluate it for (a) β = 1, (b) β = 1.5 and (c) β = 2. (d) What cell ratio keeps it at or below 80 mV?

### Problem 23-02.12 [C]

**What repair buys.** A 128 MiB cache (2³⁰ bits) must work with 99% probability. (a, b) Without repair, what sigma does each cell need, and what Vmin results with Example 23-02.3's margin model (σ_VT = 25 mV)? Spare rows and columns can now replace up to 100 failing cells, so the array works if the number of failures, a Poisson variable with mean $\lambda = Np$, is at most 100. Find (c) the largest λ allowed, (d) the sigma then needed, (e) the new Vmin, (f) the Vmin saved and (g) the sigma saved.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. What sets bitcell area; the scaling stall | 1, 4 |
| 2. Cell versus macro density; bitline length | 2, 7, 8 |
| 3. Sigma for an array and Vmin | 3, 9, 12 |
| 4. Read and write assists | 5, 6, 11 |
| 5. Leakage, retention and die-area cost | 4, 10 |
