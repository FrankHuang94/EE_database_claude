# Problems 23-08 · Emerging Memories: MRAM, ReRAM, PCM, FeRAM

Chapter: [23-08](../chapters/23-08-emerging-memories.md) · Worked solutions: [23-08 solutions](../solutions/23-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** A year is 365.25 days. MRAM attempt frequency $f_0 = 10^9$ s⁻¹, and $\Delta = E_b/kT$ with a temperature-independent barrier unless stated. Temperatures in kelvin are °C + 273.15. 1 Mib = 2²⁰ bits. Values marked "assumed" are illustrative. Problems marked *(lab)* can be checked with `labs/23-08-lab/emem.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 23-08.1 [A]

**Read margin.** An MTJ has $R_P$ = 3 kΩ and a TMR of 200% (assumed). It is read at 0.1 V through 1.5 kΩ of access resistance. Find (a) $R_{AP}$, the read currents in (b) the P and (c) the AP state, and (d) the effective contrast $I_P/I_{AP} - 1$.

### Problem 23-08.2 [A]

**One bit and many.** *(lab)* A cell has $\Delta$ = 50 at its operating temperature. Find (a) its mean retention time in seconds and (b) in years. (c) How many thermal flips does a 64 Mib array expect in 10 years?

### Problem 23-08.3 [B]

**Hot retention.** A cell has $\Delta$ = 75 at 25 °C. Find (a) its $\Delta$ at 125 °C and (b) the $\Delta$ a 16 Mib array needs for at most one expected flip in 10 years. (c) How many flips does the array expect in 10 years at 125 °C, and does it meet the target?

### Problem 23-08.4 [B]

**Stability against energy.** Assume $I_{c0}$ = 0.8 µA per unit of $\Delta$, writing at 1.3 $I_{c0}$ with 10 ns pulses at 0.6 V. Find the write current and energy for (a) $\Delta$ = 45 and (b) $\Delta$ = 70. (c) By what factor does the retention time of the $\Delta$ = 70 cell exceed that of the $\Delta$ = 45 cell?

### Problem 23-08.5 [B]

**A PCM RESET design.** *(lab)* A PCM cell has $R_{th}$ = 5 K/µW, conducts with 3 kΩ during programming and must rise 600 K to melt (assumed). Its thermal time constant is 1.5 ns. Find (a) the power and (b) the current for RESET, (c) the energy of a 30 ns pulse and (d) the time to cool from 600 K to 150 K. (e) What peak rise does a 3 ns pulse at the same current reach, and does it melt the cell?

### Problem 23-08.6 [B]

**Drift exponents.** A material engineer lowers the drift exponent from 0.1 to 0.05 (assumed). Starting from $t_0$ = 1 s, how long until resistance has drifted by a factor of 1.5 with (a) $\nu$ = 0.05 and (b) $\nu$ = 0.1? (c) What is the 10-year drift factor with $\nu$ = 0.05?

### Problem 23-08.7 [A]

**Counting quanta.** (a) How many conductance quanta does a 6.45 kΩ filament carry? What resistances correspond to (b) one and (c) three quanta?

### Problem 23-08.8 [B]

**FeRAM against DRAM.** A FeRAM capacitor is 60 nm × 60 nm with $P_r$ = 15 µC/cm² on a 20 fF bitline (assumed). Find (a) the switched charge and (b) the bitline signal. (c) A DRAM cell of 10 fF storing a 0.5 V difference from the bitline precharge shares charge with the same 20 fF bitline (assumed). What is its signal? (d) What $P_r$ would the FeRAM cell need to match it?

### Problem 23-08.9 [A]

**FeFET windows.** Find (a) the memory window of a FeFET with $E_c$ = 1.2 MV/cm and an 8 nm ferroelectric, and (b) the thickness needed for a 3 V window with $E_c$ = 1 MV/cm.

### Problem 23-08.10 [B]

**Endurance budget.** An MCU logs one record per second into the same logical location for 15 years. Find (a) the number of writes. Without wear leveling, how long would a location last with (b) 10⁵-cycle NOR flash (assumed)? With wear leveling, how many physical locations must the writes be spread over for (c) NOR flash, (d) ReRAM rated for 10,000 cycles and (e) MRAM rated for one million cycles (the TSMC values in the chapter's sources)?

### Problem 23-08.11 [B]

**Embedded array area.** A 4 MiB (32 Mib) embedded MRAM uses a 50 $F^2$ cell at 28 nm with 50% array efficiency (assumed). Find (a) the cell area, (b) the total cell area and (c) the macro area. (d) What macro area would SRAM with a 0.127 µm² cell (assumed) and the same efficiency need?

### Problem 23-08.12 [C]

**"MRAM will replace DRAM."** At Everspin's 9.75 Mb/mm² (Example 23-08.8), find (a) the die area of a 16 Gb MRAM, and (b) its ratio to the 858 mm² maximum reticle field (26 mm × 33 mm). Comment on the claim.

### Problem 23-08.13 [C]

**Write-energy budget.** An edge AI device rewrites 1 MiB of weights per second in nonvolatile memory. Find (a) the bits written per second and the write power at (b) 0.7 pJ/bit (MRAM, Table 1), (c) 4 pJ/bit (Example 23-08.4's PCM RESET) and (d) 100 pJ/bit (NOR flash, Table 1). Which technologies fit a 50 µW memory budget?

### Problem 23-08.14 [C]

**Deriving the STT write current, and read disturb.** (a) The free layer of a perpendicular MTJ has moment $m = M_sV$, anisotropy field $H_k$ and barrier $E_b = \mu_0M_sH_kV/2$. Its angular momentum is $m/\gamma$; while it precesses at $\omega = \gamma\mu_0H_k$, Gilbert damping $\alpha$ removes angular momentum at the rate $\alpha\omega m/\gamma$. Each electron of the write current delivers $\hbar/2$ of spin angular momentum with efficiency $\eta$. Show that switching begins at $I_{c0} = (4q\alpha/\hbar\eta)E_b$, and check the units. Take $\hbar = 1.0546 \times 10^{-34}$ J·s and $k = 1.381 \times 10^{-23}$ J/K, and find (b) $I_{c0}$ per unit of $\Delta$ at 300 K for $\alpha$ = 0.008 and $\eta$ = 0.6 (assumed), and (c) $I_{c0}$ for $\Delta$ = 50. A read current $I$ lowers the barrier to $\Delta(1 - I/I_{c0})$. For a 5 ns read at 30% of $I_{c0}$, find (d) the effective barrier and the flip probability per read, and (e) the expected number of reads per flip. (f) What is the largest read current, as a fraction of $I_{c0}$, that keeps the flip probability per 5 ns read at or below $10^{-18}$?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Storage mechanisms | 7, 9 |
| 2. MRAM read, stability and write | 1, 2, 3, 4, 14 |
| 3. PCM thermal model and drift | 5, 6 |
| 4. ReRAM quanta and FeRAM charge | 7, 8, 9 |
| 5. Comparing technologies | 10, 11, 13 |
| 6. Business and claims | 12, 13 |
