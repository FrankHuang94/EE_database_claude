# Lab 23-03 · A DRAM Cell, Its Sense Amplifier, Refresh and Row Hammer

Chapter: [23-03 · DRAM Cells, Arrays and Refresh](../../chapters/23-03-dram-cells-arrays-refresh.md)

## Objective

Simulate a DRAM cell's read and write at transistor level: charge sharing, writing a 1 with and without a boosted wordline, and a full read in which a latch sense amplifier resolves the bitlines and restores the cell. Then use the chapter's models to see how refresh overhead scales, how the weak-cell tail sets the refresh window, and how probabilistic row-hammer mitigation behaves.

## Background

§3.1 derived the signal from charge conservation, §3.3 the write through the access transistor in its saturated and linear regions, and §3.4 the latch's exponential regeneration with time constant $C/g_m$. The netlist uses square-law (level-1) transistors with no junction or overlap capacitance, so the charge-sharing and write results can be compared exactly with the closed forms. The latch run cannot: its devices start near cutoff and its sense-enable lines ramp, which the linear model ignores.

## Files

- `dram_cell.cir`: Part A, charge sharing (8 fF cell at 1.0 V, 40 fF bitline at 0.5 V, wordline 1.8 V); Part B, three cells written from 0 with the wordline at 1.0 V, 1.5 V and 1.8 V; Part C, a full read with a cross-coupled latch (n- and p-channel devices with $k$ = 100 µA/V² and threshold magnitude 0.3 V) whose sense-enable lines move from 0.5 V to 0 and 1.0 V at 5 ns.
- `dramtech.py`: the chapter's models.
- `23-03-dram-lab.ipynb`: the notebook for Parts 2 to 4.

## Procedure

**Part 1 · The cell in ngspice.**

1. Predict the bitline voltage after charge sharing, and each written cell's voltage at 10 ns (Examples 23-03.1 and 23-03.3).
2. Predict, with §3.4 and $g_m$ = 40 µS, $C$ = 40 fF, the time after sense enable for the bitline difference to reach 0.9 V.
3. Run `ngspice -b dram_cell.cir` and compare. Plot `v(bl)`, `v(blbar)` and `v(snc)` against time to see charge sharing, regeneration and restore.

**Part 2 · Refresh overhead** (notebook). Plot $t_{RFC}/t_{REFI}$ against density for DDR4's $t_{RFC1}$ values (160, 260, 350 and 350 ns for 2 to 16 Gb) at both temperature ranges.

**Part 3 · The weak-cell tail** (notebook). With retention lognormal (median 10 s, $\sigma_{\ln}$ = 1.0, assumed) over 2³⁴ cells, plot the expected number of cells failing against the refresh window from 4 ms to 1 s. Find the window at which fewer than one cell is expected to fail.

**Part 4 · PARA Monte Carlo** (notebook). With $p$ = 0.002 and $N_{th}$ = 2,000 (a deliberately weak setting, so misses are common enough to count), simulate 20,000 attacks and compare the fraction that never refresh the victim with $(1 - p/2)^{N_{th}}$. Then plot $p$ against $N_{th}$ for a 10⁻¹⁵ miss target.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 23-03.a | cell after 10 ns, wordline at 1.5 V | 0.926 | V |
| Lab 23-03.b | latch time to a 0.9 V difference after enable (simulated) | 3.46 | ns |
| Lab 23-03.c | restored cell voltage at 40 ns | 1.000 | V |
| Lab 23-03.d | latch time to 0.9 V, linear estimate | 2.38 | ns |
| Lab 23-03.e | window with under one expected weak cell | 15.9 | ms |
| Lab 23-03.f | PARA miss probability, p = 0.002, 2,000 activations | 0.135 | |
| Lab 23-03.g | shift in standard deviations from halving the window | 0.69 | |
| Lab 23-03.h | Monte Carlo standard error, 20,000 attacks | 0.0024 | |

- Part 1: charge sharing within 0.001% of 83.3 mV; written cells within 0.2% of 0.431 V and 0.926 V; the boosted cell's shortfall within 2% of 0.2075 mV.
- Part 2: overhead from 2.05% to 4.48% at up to 85 °C, doubled from 85 to 95 °C.
- Part 4: the Monte Carlo fraction lands within about 0.005 of 0.135 (its standard error is 0.0024).

## Discussion

1. Why does the simulated latch take about 1.5 times the linear estimate?

   <details><summary>Answer</summary>

   The linear model assumes full transconductance from the start. In the circuit, the latch's transistors start with zero gate overdrive (their sources sit at the 0.5 V precharge level), so for the first few hundred picoseconds the sense-enable ramps are only turning them on. Their transconductance also falls once one side swings far, and the bitline holding the cell carries an extra 8 fF. Designers use the linear model to compare options, and simulation to set timing.

   </details>

2. The wordline at 1.5 V equals $V_{ARY} + V_{TH}$. Why does the cell still reach only 0.926 V in 10 ns?

   <details><summary>Answer</summary>

   At exactly $V_{ARY} + V_{TH}$ the transistor is saturated all the way, and the shortfall falls only as $1/t$ (§3.3): the cell approaches 1.0 V but slowly. A boost above that level puts the transistor in its linear region near the end of the write, where the shortfall decays exponentially.

   </details>

3. Halving the refresh window from 64 ms to 32 ms cut the expected weak cells by about 48 times in Example 23-03.8. Why so much more than 2?

   <details><summary>Answer</summary>

   The weak cells sit in the far tail of the retention distribution, where the normal density in log time falls off faster than exponentially. A factor of 2 in time is a shift of $\ln 2/\sigma_{\ln}$ = 0.69 standard deviations at about 5 sigma, and the tail probability falls by a large factor over that shift.

   </details>

## Optional hardware

Open-source memory testers built on FPGA boards let researchers issue raw DRAM commands to a real DDR4 module, without the controller's refresh. Such a setup can measure retention failures against the refresh interval and temperature, and row-hammer thresholds for specific rows. Run such experiments only on hardware you own. Never run row-hammer code on shared or production systems.
