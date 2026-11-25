# Problems 24-09 · Linear-Drive and Co-Packaged Optics

Chapter: [24-09](../chapters/24-09-lpo-and-cpo.md) · Worked solutions: [24-09 solutions](../solutions/24-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Energy per bit is power divided by bit rate; a "port" is 800 Gb/s unless stated.
- Linear chains add $1/Q^2$; the KP4 threshold is BER 2.4 × 10⁻⁴ ($Q$ = 3.49); margins are electrical dB, $20\log_{10}$ of the $Q$ ratio.
- Zero-failure 95% bounds use $\lambda_U = -\ln(0.05)/T$; with $r$ failures, $\lambda_U = \chi^2_{0.95,\,2r+2}/(2T)$.
- A year is 8766 h. "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/24-09-lab/cpo.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 24-09.1 [A]

**A 102.4 Tb/s CPO switch.** Broadcom's TH6-Davisson has 16 optical engines of 6.4 Tb/s and uses about 3.5 W per 800 Gb/s port [R-545]. Find (a) the switch bandwidth, (b) the number of 800 Gb/s ports, (c) the optics power, (d) the optics power with 16 W pluggables and (e) the saving.

### Problem 24-09.2 [A]

**ELSFP power classes.** Convert the LP (11 dBm), HP (17 dBm) and SHP (26 dBm) classes [R-548] to milliwatts. What power ratio separates SHP from LP?

### Problem 24-09.3 [B]

**Another LPO budget.** *(lab)* Host channels each give $Q$ = 12 and the optical path $Q$ = 7 (assumed). Find the linear link's (a) $Q$, (b) BER and (c) margin above KP4.

### Problem 24-09.4 [B]

**What 22 dB does to a signal.** A transmitter launches 1 V peak to peak. What amplitude in millivolts arrives after (a) 22 dB and (b) 4 dB of channel loss [R-543]?

### Problem 24-09.5 [B]

**A brighter laser.** *(lab)* Repeat Example 24-09.4(a) with an SHP source at 26 dBm. How many lanes could it feed, and how many with binary splitting?

### Problem 24-09.6 [B]

**More hours.** *(lab)* Press accounts mention later CPO tests of 15 million and over 50 million device-hours (unconfirmed [R-546]). Suppose each had no failures. (a) What 95% FIT bound does each give? (b) If one failure had occurred in 15 million hours, what would the bound be?

### Problem 24-09.7 [B]

**Faster repair.** *(lab)* With Example 24-09.7's failure rates (200 FIT per pluggable, 400 FIT per 8-port engine), (a) what is the ratio of port-hours lost if a spare switch restores service in 4 h instead of 24 h? (b) At what repair time would a CPO port lose no more than a pluggable port?

### Problem 24-09.8 [A]

**NVIDIA's 2025 figure.** NVIDIA's August 2025 material quoted CPO power "as low as 9W" [R-543]. If that is per 1.6 Tb/s port, what is the energy per bit?

### Problem 24-09.9 [B]

**LRO and LPO at cluster scale.** A cluster uses 100,000 modules of 1.6 Tb/s. Using Semtech's figures of about 20 W for digital modules, under 15 W for LRO [R-535] and 50–60% savings for LPO against retimed modules [R-535], find the power saved by (a) LRO and (b) LPO at each end of its range.

### Problem 24-09.10 [B]

**Paying in stock.** For Marvell's Celestial AI deal [R-547], find (a) the cash share of the upfront consideration and (b) the stock share of the maximum consideration. (c) If Marvell's share price doubled before all contingent shares were issued, what would the maximum consideration be worth?

### Problem 24-09.11 [C]

**A laser plan for a CPO switch.** A 102.4 Tb/s CPO switch has 512 lanes of 200 Gb/s and uses one laser channel per four lanes [R-543]. Each ELSFP module provides 8 channels at 23 dBm (assumed), and lasers convert electrical to optical power at 15% (assumed). Find (a) the laser channels and (b) ELSFP modules needed, (c) the total optical power, (d) its electrical power, and (e) that as a fraction of Problem 24-09.1's 448 W.

### Problem 24-09.12 [C]

**Checking the baselines.** (a) Against what pluggable power would Davisson's 3.5 W be exactly a 70% reduction? (b) What pluggable power does NVIDIA's "5x" with 5 W per port imply? (c) Explain why the two vendors' claims cannot be ranked from these figures alone.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Where link energy goes; LPO, LRO and CPO | 1, 9 |
| 2. Linear budgets and 200 Gb/s lanes | 3, 4 |
| 3. Converting vendor claims to energy per bit | 8, 12 |
| 4. External laser sources | 2, 5, 11 |
| 5. Reliability bounds and blast radius | 6, 7 |
| 6. Ecosystem, timing and deal economics | 10 |
