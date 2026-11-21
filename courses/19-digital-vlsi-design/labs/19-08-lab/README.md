# Lab 19-08 · The 6T Cell: Stability, Sensing and Yield

Chapter: [19-08 · SRAM Design](../../chapters/19-08-sram-design.md)

## Objective

- Measure a 6T cell's read disturbance and a write half-cell's level in ngspice, and match them to the closed forms.
- Draw butterfly curves and compute the static noise margin in hold and in read.
- Estimate read timing and the yield of large arrays with and without repair.

## Background

During a read the node storing 0 rises to the level where the saturated access transistor balances the linear pull-down; during a write the node storing 1 falls to where the linear access transistor balances the saturated pull-up (§3.2–3.3). The SNM is the side of the largest square in the smaller butterfly lobe (§3.4). Bitline swing develops at $I_{cell}/C_{BL}$ and a sense amplifier regenerates it in $\tau\ln(V_{DD}/\Delta V)$ (§3.5). Array yield without repair is $e^{-NQ(\mu/\sigma)}$ (§3.7).

Files:

- `cell.cir`: a full 6T cell read at cell ratio 2, and a write half-cell at pull-up ratio 0.5 (level-1 model).
- `sram.py`: `read_disturb`, `write_level`, `inverter_vtc`, `static_noise_margin`, `bitline_time`, `sense_time`, `array_area_mm2`, `cell_fail_probability` and `array_yield`.
- `19-08-sram-lab.ipynb`: the procedure below.

## Procedure

1. **Read and write in ngspice.** Predict the read disturbance at CR = 2 and the write level at PR = 0.5; run `ngspice -b cell.cir` and Part 1.
2. **Butterflies.** Plot the hold and read butterflies for CR = 1, 2 and 3 and compute their SNMs (Part 2).
3. **Sizing window.** Plot the read disturbance against CR and the write level against PR, and find the window that satisfies both conservative criteria (Part 3).
4. **Read timing.** Plot bitline and sense time against rows per bitline (Part 4).
5. **Yield.** Plot yield against margin in σ for 1 Mib, 64 Mib and 1 Gib, with and without 32 repairs (Part 5).

## Expected results

- Part 1: 0.1285 V (read, CR = 2) and 0.2050 V (write, PR = 0.5), in both ngspice and Python.
- Part 2: hold SNM 0.397 V; read SNM 0.184, 0.226 and 0.249 V for CR = 1, 2 and 3.
- Part 3: in this ideal cell every CR ≥ 1 keeps the read disturbance below 0.3 V (0.205 V at CR = 1), a 0.1 V target needs CR ≥ 2.77, and the write criterion needs PR ≤ 0.673.
- Part 4: the bitline time grows linearly with rows (177.4 ps at 256 rows), the sense time not at all (34.5 ps).
- Part 5: at 6σ, 64 Mib yields 93.6% without repair; 1 Gib needs 6.72σ for 99%.

## Discussion

1. Why are the read-disturb level at CR = 1 and the write level at PR = 0.5 the same number?
2. Why does ngspice agree exactly with the closed form for the read disturbance in `cell.cir`?
3. Why is the read SNM always smaller than the hold SNM?
4. Why does a little redundancy improve yield so dramatically?

**Answers.**

1. Both are a saturated transistor of strength $k$ against a linear one of strength $2k$, with the same supply and thresholds; the equations are identical.
2. The disturbed node (0.128 V) stays below $V_T$, so the other inverter's NMOS remains off and its output stays exactly at $V_{DD}$, which is the closed form's assumption.
3. The access transistors load the storage nodes during a read, raising the low output of each inverter and shrinking both butterfly lobes.
4. Failures are rare and roughly Poisson; if the expected count is a few, the probability of more than a handful is tiny, so a few spares cover almost every die.

## Optional hardware

Two CD4069 inverters cross-coupled form a latch; adding series resistors to two "bitline" voltage sources through CD4066 analog switches (the access transistors) lets you see read disturbance and write success on a voltmeter as you vary the series resistance, a direct analog of the cell and pull-up ratios.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 19-08.a | read disturbance in ngspice terms | 0.1285 | V |
| Lab 19-08.b | write level in ngspice terms | 0.2050 | V |
