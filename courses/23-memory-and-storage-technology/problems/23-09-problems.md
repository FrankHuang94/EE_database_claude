# Problems 23-09 · Compute-in-Memory and Near-Memory Computing

Chapter: [23-09](../chapters/23-09-compute-in-memory.md) · Worked solutions: [23-09 solutions](../solutions/23-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** A multiply-accumulate (MAC) counts as two operations. ADC energy per conversion is $\text{FoM}_W \times 2^B$ (Walden). ENOB $= (\text{SNR}_{dB} - 1.76)/6.02$. Bit-serial inputs and bit-sliced weights need $b_xb_w$ binary conversions per MAC, shared across the rows of an array. Values marked "assumed" are illustrative. Problems marked *(lab)* can be checked with `labs/23-09-lab/cim.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 23-09.1 [A]

**A small crossbar.** Rows at $\mathbf{V}$ = (0.1, 0.2, 0.05) V drive a crossbar with conductances (µS)

$$
\mathbf{G} = \begin{pmatrix} 20 & 5 \\ 10 & 15 \\ 0 & 25 \end{pmatrix}
$$

into two virtual-ground columns. Find the currents in (a) column 1 and (b) column 2.

### Problem 23-09.2 [A]

**Signed weights.** *(lab)* Weights $(-2, 1, 3)$ are stored as conductance pairs with $g$ = 5 µS per unit and $G_{min}$ = 0.5 µS (assumed), and the rows are driven at (0.1, 0.1, 0.2) V. Find (a) the positive-column current, (b) the negative-column current, (c) the differential output, and (d) check it against the exact dot product.

### Problem 23-09.3 [B]

**Variation budgets.** What relative device variation $\sigma$ gives an analog array (a) 8 and (b) 4 effective bits? State the SNR in dB for each.

### Problem 23-09.4 [B]

**When rows help.** An array sums $M$ = 64 products with 10% relative variation. Find the compute SNR in dB if (a) all products are positive and equal, and (b) the products are zero-mean and uncorrelated. Explain the difference.

### Problem 23-09.5 [B]

**Sizing an ADC.** A 128-row array takes 2-bit inputs, applied in one step as four voltage levels or pulse widths, and 1-bit weights. Find (a) the largest column sum, (b) the exact ADC resolution and (c) the bits to use. With $\text{FoM}_W$ = 10 fJ per step (assumed) at that resolution, find (d) the energy per conversion and (e) the ADC energy per 2-bit × 1-bit MAC.

### Problem 23-09.6 [B]

**A better ADC.** *(lab)* A 512-row array uses 7-bit ADCs at $\text{FoM}_W$ = 2 fJ per step (assumed). Seven bits cannot represent all 513 possible binary sums; assume the sums' narrow distribution means the ADC clips only rarely (§3.4). Find the ADC energy per MAC and the TOPS/W ceiling for (a) 8-bit × 8-bit and (b) 4-bit × 4-bit MACs.

### Problem 23-09.7 [B]

**Internal bandwidth.** A DRAM die has 16 banks, each reading 256 bits every 4 ns internally, and a 16-bit external interface at 8 Gb/s per pin (assumed). Find (a) the internal and (b) the external bandwidth, and (c) their ratio.

### Problem 23-09.8 [B]

**Decode bound.** A 13-billion-parameter model stored at 4 bits per weight runs on four LPDDR5X packages. Find the bandwidth-bound token rate with (a) four 64-bit LPDDR5X-9600 interfaces and (b) four LPDDR5X-PIM packages at 614 GB/s each.

### Problem 23-09.9 [B]

**Amdahl.** PIM speeds up the memory-bound fraction of a workload 8×. Find the overall speedup if that fraction is (a) 60% and (b) 90% of the run time. (c) What is the limit for a 90% fraction as the PIM speedup grows without bound?

### Problem 23-09.10 [B]

**Boundaries.** A chip delivers 40 TOPS with its compute core drawing 2 W. On its card, 3 W of DRAM is added and both are fed through regulators of 85% efficiency (assumed). Find (a) the card's input power, (b) the card-level TOPS/W and (c) the chip-core TOPS/W.

### Problem 23-09.11 [B]

**Utilization.** An accelerator peaks at 100 TOPS at 10 W. On a model it reaches 40% utilization, and its power falls only to 7 W (assumed). Find (a) the effective TOPS/W and (b) the peak TOPS/W.

### Problem 23-09.12 [C]

**Why columns need a virtual ground.** A column of four 10 µS cells, each driven at 0.2 V, is sensed by a resistor $R_s$ to ground instead of a virtual ground. For $R_s$ = 1 kΩ, find (a) the column voltage, (b) the current and (c) the error against the ideal 8 µA. (d) What is the largest $R_s$ for a 1% error?

### Problem 23-09.13 [C]

**Testing a claim.** A start-up claims "8-bit analog inference at 100 TOPS/W" from 256-row arrays with 8-bit ADCs, bit-serial inputs and bit-sliced weights. (a) What total energy per MAC does 100 TOPS/W imply? (b) If the ADCs may use all of it, what energy per conversion is allowed? (c) What Walden figure of merit does that require, and (d) how many times better is it than the 5 fJ per step of Example 23-09.4? What else might the start-up be doing?

### Problem 23-09.14 [C]

**Error relative to full scale.** A layer's weights $w_i$ are zero-mean and independent, with RMS value $s_w$, and are mapped so that the full-scale conductance represents $w_{max} = c\,s_w$, where $c$ is the crest factor. Each device's programming error is zero-mean with standard deviation $\sigma_{FS}w_{max}$, independent of the weights and of the other devices. The inputs $x_i$ are independent of the weights, with $E[x_i^2] = s_x^2$. (a) Derive the compute SNR of an $M$-row dot product and compare it with §3.3's relative-error result. For $\sigma_{FS}$ = 1% and $c$ = 3, find (b) the SNR and the effective bits, and (c) the penalty against the relative-error model with σ = 1%. (d) What $\sigma_{FS}$ gives 6 effective bits at $c$ = 3?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Data movement and taxonomy | 7, 8 |
| 2. Crossbar arithmetic | 1, 2, 12 |
| 3. SNR, effective bits and ADC cost | 3, 4, 5, 6, 13, 14 |
| 4. PIM throughput, roofline and Amdahl | 7, 8, 9 |
| 5. Benchmarking | 10, 11, 13 |
