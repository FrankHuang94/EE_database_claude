# Problems 23-07 · SSD Controllers and Storage Systems

Chapter: [23-07](../chapters/23-07-ssd-controllers.md) · Worked solutions: [23-07 solutions](../solutions/23-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Capacities and bandwidths are decimal (1 TB = 10¹² bytes, 1 GB/s = 10⁹ bytes/s); indirection units and pages are binary (4 KiB = 4,096 bytes). Over-provisioning is relative to user capacity, $OP = (T - U)/U$, and $\alpha = 1 + OP$. Write amplification under random writes uses the chapter's FIFO model, $A = \alpha/(\alpha + W(-\alpha e^{-\alpha}))$, unless stated. A 5-year rating has 1,825 days. Values marked "assumed" are illustrative. Problems marked *(lab)* can be checked with `labs/23-07-lab/ssd.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 23-07.1 [A]

**Links.** PCIe 4.0 runs 16 GT/s per lane with 128b/130b encoding. Find the per-direction bandwidth of (a) PCIe 4.0 x4 and (b) PCIe 5.0 x2, and (c) the raw per-direction rate of PCIe 6.0 x8.

### Problem 23-07.2 [A]

**Mapping tables.** Find (a) the mapping-table size of a 3.84 TB drive with 4 KiB units and 4-byte entries. A 122.88 TB drive uses 16 KiB units. Find (b) its number of entries and (c) the address bits each entry needs. (d) How large is its table with 5-byte entries?

### Problem 23-07.3 [B]

**Over-provisioning.** *(lab)* For (a) 10% and (b) 20% over-provisioning under random writes, find the victim blocks' valid fraction and the write amplification. Express each OP as (c) and (d) a spare factor $S_f = (T - U)/T$.

### Problem 23-07.4 [B]

**The model behind the formula.** (a) Show that if the victim blocks are on average a fraction $u$ valid, the write amplification is $1/(1 - u)$. (b) Explain why, under FIFO cleaning and uniform random writes, $u = e^{-\alpha(1 - u)}$. (c) Solve for $u$ and $A$ at $\alpha$ = 1.5 and check that your $u$ satisfies the equation.

### Problem 23-07.5 [B]

**What TRIM buys.** *(lab)* A drive with 7% over-provisioning holds data on only 80% of its user capacity; the host has trimmed the rest, and its random writes go only to the live data. Find (a) the effective $\alpha$ and (b) the write amplification, and (c) compare it with a full drive.

### Problem 23-07.6 [B]

**A capacity QLC drive.** A 30.72 TB QLC drive carries 33.0 TB of raw flash rated for 1,000 P/E cycles (assumed). Find (a) its over-provisioning, (b) the worst-case random-write amplification, (c) its host TBW and (d) its DWPD over 5 years. (e) If it uses 16 KiB indirection units and the host writes random 4 KiB blocks, what DWPD does it offer?

### Problem 23-07.7 [B]

**A BCH design.** A codeword holds 2 KiB of data and a BCH code over GF($2^{15}$) correcting 60 errors. Find (a) the parity bits and (b) the codeword length. At a raw error rate of 2 × 10⁻³, find (c) the mean errors per codeword and (d) the failure probability. (e) Up to what raw error rate does the codeword fail with probability at most 10⁻¹⁵, and (f) what mean error count is that?

### Problem 23-07.8 [B]

**Capacity with less spare.** A page stores 16 KiB of data with 1 KiB of spare (assumed). Find (a) its code rate, (b) the highest raw error rate any hard-decision code at that rate could tolerate and (c) the hard-decision capacity at a raw error rate of 0.5%.

### Problem 23-07.9 [A]

**Little's law.** (a) What IOPS does a drive deliver at queue depth 32 if the average latency is 80 µs? (b) What does it deliver at queue depth 1 with the same latency? (c) How many commands must be outstanding for 2 million IOPS at 120 µs?

### Problem 23-07.10 [B]

**Channels or dies?** A drive has 8 channels at 2.4 GB/s, 4 dies per channel, 4 independent planes per die and $t_R$ = 60 µs (assumed). For random 4 KiB reads, find (a) the transfer time of one 4 KiB read on a channel, (b) the channel-limited IOPS of one channel and (c) of all eight, and (d) the die-limited IOPS. (e) Which limits the drive?

### Problem 23-07.11 [B]

**Hold-up.** A drive needs 15 W for 40 ms after power loss (assumed). Its capacitors charge to 28 V and the converter runs down to 10 V at 88% efficiency (assumed). Find (a) the energy drawn from the bank and (b) the capacitance. (c) How much energy is left in the bank at 10 V, and (d) what fraction of the initial stored energy is that?

### Problem 23-07.12 [B]

**The SLC-cache cliff.** A client TLC drive has a 200 GB SLC cache that absorbs writes at 6 GB/s; once it is full, writes go straight to TLC at 1.5 GB/s (assumed). Find (a) the time to fill the cache, (b) the time for the next 100 GB and (c) the average rate for a 300 GB copy. (d) How much TLC-mode capacity does a 200 GB SLC cache occupy?

### Problem 23-07.13 [C]

**Designing for 3 DWPD.** TLC flash rated at 3,000 P/E cycles (assumed) must deliver 3 DWPD over 5 years under worst-case random writes. (a) Write DWPD as a function of $\alpha$ alone. Find (b) the required $\alpha$, (c) the write amplification there and (d) the over-provisioning. (e) What user capacity can 8.8 TB of raw flash then offer? Comment on how real 3 DWPD drives manage with far less over-provisioning.

### Problem 23-07.14 [C]

**"Unlimited random-write endurance."** A 122.88 TB QLC drive with about 130 TB of raw flash (assumed) can sustain at most 0.5 GB/s of random writes, and its write amplification for its rated workload is 2 (both assumed). Find (a) the host data written in 5 years at full speed, (b) the resulting NAND writes and (c) the P/E cycles they consume. (d) If the flash is rated for 1,500 cycles (assumed), is the claim plausible?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Architecture and bandwidth | 1, 10 |
| 2. FTL and mapping tables | 2, 6 |
| 3. Write amplification and endurance | 3, 4, 5, 6, 13, 14 |
| 4. ECC sizing | 7, 8 |
| 5. Queues and power-loss protection | 9, 10, 11 |
| 6. Evaluating specifications | 12, 13, 14 |
