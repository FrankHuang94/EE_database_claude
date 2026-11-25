# Problems 23-03 · DRAM Cells, Arrays and Refresh

Chapter: [23-03](../chapters/23-03-dram-cells-arrays-refresh.md) · Worked solutions: [23-03 solutions](../solutions/23-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Bitlines are precharged to half the array voltage. Transistors follow the square law with λ = 0 and no body effect (09-09). 1 Gib = 2³⁰ bits. Values marked "assumed" are illustrative; data-sheet values cite the chapter's sources. Problems marked *(lab)* can be checked with `labs/23-03-lab/dramtech.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 23-03.1 [A]

**Charge sharing.** A 10 fF cell sits on a 60 fF bitline; the array voltage is 1.1 V (assumed). Find (a) the signal for a stored 1, (b) the signal for a stored 0, (c) the transfer ratio and (d) the electrons a stored 1 holds relative to a 0.

### Problem 23-03.2 [A]

**Reading a data sheet.** Micron's 16 Gb DDR4 x16 part has 8 banks in 2 bank groups, 131,072 rows per bank and 1,024 columns, each 16 bits wide (chapter source [2]). Find (a) the page size in bits, (b) the device's capacity in bits, (c) the rows per bank each of 8,192 REF commands must refresh and (d) the share of an open page that one 8-transfer burst (BL8) uses.

### Problem 23-03.3 [A]

**DDR5 refresh arithmetic.** DDR5 refreshes 8,192 times in 32 ms up to 85 °C and in 16 ms from 85 to 95 °C (chapter source [1]). Find (a) tREFI in each range (a, b). For an assumed tRFC of 295 ns, find (c, d) the refresh overhead in each range.

### Problem 23-03.4 [B]

**Bitline length.** *(lab)* The worst-case cell signal is 0.40 V and the sense amplifier needs 50 mV. Each cell adds 0.07 fF and the fixed part is 3 fF (assumed). For a 7 fF cell find (a) the largest bitline capacitance and (b) the largest number of cells per bitline. (c) Repeat for a 5 fF cell. (d) What storage capacitance just supports 512 cells per bitline?

### Problem 23-03.5 [B]

**The weak 1.** An access transistor with $V_{TH}$ = 0.45 V and $k$ = 25 µA/V² charges a 6 fF cell from 0, with the bitline and wordline both at 1.1 V (assumed). Find (a) the voltage the cell approaches, (b) the cell voltage after 5 ns and (c) the time to reach 90% of the limit. (d) What wordline voltage is the minimum for a full 1?

### Problem 23-03.6 [B]

**Latch timing.** A sense amplifier's inverters each have $g_m$ = 25 µS around balance and each bitline is 50 fF (assumed). (a) Find the time constant and (b) the linear-model time to grow a 60 mV signal to 1.0 V. (c) What $g_m$ would cut that time to 3 ns? (d) With the original $g_m$, find the time for a 30 mV signal and (e) the extra time.

### Problem 23-03.7 [B]

**Page policy.** A DDR5-6400 device has tAA = tRCD = tRP = 16 ns (chapter source [1]). Find (a) the row-hit, (b) row-miss and (c) row-conflict latencies, and (d) the average for 40% hits, 20% misses and 40% conflicts (assumed). (e) For a workload whose accesses are either hits or conflicts, above what hit rate does an open-page policy beat a closed-page policy?

### Problem 23-03.8 [B]

**Banks and Little's law.** A 32-bit-wide DDR5-6400 channel moves 4 bytes per transfer (assumed). With 64-byte accesses and an assumed tRAS of 32 ns (tRP = 16 ns), find (a) one bank's bandwidth when every access opens a new row, (b) the channel's peak bandwidth and (c) the number of banks that must work in parallel. (d) Using Little's law, how many 64-byte requests must be in flight to sustain the peak with a 48 ns service time per request?

### Problem 23-03.9 [B]

**Retention.** *(lab)* A 6 fF cell may lose 0.15 V (assumed). (a) What leakage keeps it within DDR4's 32 ms window at 95 °C? If leakage halves every 10 °C (assumed), find (b) that cell's leakage at 25 °C and (c) its retention time at 25 °C. Retention times at 95 °C are lognormal with a median of 2 s and $\sigma_{\ln}$ = 0.8 (assumed). For 2³⁴ cells find the expected number failing (d) a 32 ms window and (e) a 16 ms window.

### Problem 23-03.10 [B]

**Activation and refresh energy.** A 16 Gb DDR5 x8 device has 32 banks of 65,536 rows with 8,192-bit pages (chapter source [1]). Each bitline is 35 fF and swings at 1.1 V (assumed). Find (a) the energy to sense and restore one row, the refresh power (b) up to 85 °C (32 ms) and (c) from 85 to 95 °C (16 ms), and (d) the activation energy per bit when a row is opened for one 128-bit burst.

### Problem 23-03.11 [B]

**Hammering a DDR5 device.** Assume tRC = 48 ns. Find (a) the activations of one row possible in a 32 ms window, (b) the activations per 3.906 µs tREFI and (c) the time for 9,600 activations. For PARA, find the probability $p$ that keeps the chance of missing a victim at 10⁻¹⁵ when the threshold is (d) 4,800 and (e) 1,000 activations.

### Problem 23-03.12 [C]

**The boosted write.** Derive the shortfall $u(t) = V_{ARY} - V$ of a cell charged from 0 through an access transistor that stays in its linear region, and show that it decays exponentially for small $u$. With $V_{PP}$ = 2.0 V, $V_{TH}$ = 0.5 V, $V_{ARY}$ = 1.1 V, $k$ = 20 µA/V² and $C_s$ = 8 fF (assumed), find (a) the shortfall after 5 ns and (b) the time to come within 1 mV.

### Problem 23-03.13 [C]

**Capacitor geometry.** A 6 fF capacitor uses a 6 nm dielectric with $\varepsilon_r$ = 25 (assumed). Find (a) the electrode area needed. As the outer wall of a pillar 25 nm in diameter, find (b) its height and (c) its height-to-diameter ratio. (d) Using both walls of a cylinder of the same diameter, what height is needed? (e) What $\varepsilon_r$ would give a 1.0 µm double-walled cylinder? (f) What single-walled height is needed if the dielectric is thinned to 5 nm?

### Problem 23-03.14 [C]

**Sense-amplifier offset and bitline length.** *(lab)* A 16 Gib device must work with 99% probability with no repair of sense amplifiers. A drooped cell's signal relative to the precharge level is 0.25 V, $C_s$ = 8 fF, and each bitline has 0.08 fF per cell plus 4 fF (assumed). With 512 cells per bitline (2²⁵ sense amplifiers), find (a) the sigma each sense amplifier needs, (b) the signal and (c) the largest offset standard deviation allowed. With 256 cells per bitline (2²⁶ sense amplifiers), find (d) the sigma, (e) the signal and (f) the largest offset standard deviation.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Read signal and bitline sizing | 1, 4, 14 |
| 2. Destructive read, boosting, write and sensing times | 5, 6, 12 |
| 3. Organization, latency and bank parallelism | 2, 7, 8 |
| 4. Refresh overhead, power and retention | 3, 9, 10 |
| 5. Row hammer and mitigations | 11 |
| 6. Cell scaling limits | 13, 14 |
