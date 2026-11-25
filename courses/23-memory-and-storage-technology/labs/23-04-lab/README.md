# Lab 23-04 · DRAM I/O: Termination, Reflections, Equalization and PAM

Chapter: [23-04 · DRAM Interfaces: DDR, LPDDR and GDDR](../../chapters/23-04-dram-interfaces.md)

## Objective

Measure, in a circuit simulator, the static current of pseudo-open-drain and low-voltage-swing drivers, the reflections on a terminated line, and the pulse response of a lossy channel. Then use the chapter's models to see what data bus inversion saves, and how NRZ, PAM3 and PAM4 compare through a first-order channel.

## Background

§3.4 derived the termination current and swing, §3.3 the reflection coefficients, and §3.6 the cursors of a first-order channel and the eye a DFE recovers. §3.7 compared multilevel schemes by their eye heights at the same bit rate.

## Files

- `dram_io.cir`: Part A, a 34 Ω driver pulling low against 40 Ω to 1.1 V; Part B, a 40 Ω driver pulling high against 40 Ω to ground at 0.5 V; Part C, a 1.0 V step from 34 Ω into a 40 Ω, 300 ps line with a 40 Ω, 120 Ω or open far end; Part D, a 50 Ω, 1.6 pF channel driven by one 113.636 ps pulse.
- `ddrio.py`: the chapter's models.
- `23-04-dram-io-lab.ipynb`: the notebook for Parts 2 to 4.

## Procedure

**Part 1 · Termination and reflections in ngspice.**

1. Predict the POD low level, current and power, the LVSTL high level, the far-end voltages after the first and second arrivals for each termination, and the channel's first three cursors (Examples 23-04.3, 23-04.4, 23-04.5 and 23-04.7).
2. Run `ngspice -b dram_io.cir` and compare. Plot `v(f1)`, `v(f2)` and `v(f3)` to see the reflections arrive every 600 ps.

**Part 2 · Data bus inversion** (notebook). Enumerate all 256 bytes. For each, count low wires with and without DBI. Find the average and the maximum in each case. Repeat for biased data (Problem 23-04.5).

**Part 3 · NRZ, PAM3 and PAM4 through a first-order channel** (notebook). At 48 Gb/s, find each scheme's worst-case eye for τ = 15 ps, both from the closed form and from a long random symbol sequence. Sweep τ from 5 to 32 ps.

**Part 4 · The families' bandwidths** (notebook). Tabulate the bandwidth, pins and energy per bit of Example 23-04.2's systems and Problem 23-04.11's 1 TB/s builds.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 23-04.a | NRZ worst-case eye, τ = 15 ps, 48 Gb/s | 0.501 | |
| Lab 23-04.b | PAM3 worst-case eye | 0.313 | |
| Lab 23-04.c | PAM4 worst-case eye | 0.250 | |
| Lab 23-04.d | largest number of low wires per byte with DBI | 4 | |
| Lab 23-04.e | largest number of low wires per byte without DBI | 8 | |

- Part 1: every simulated value within 0.2% of the chapter's (the channel's second post-cursor within 1%).
- Part 2: the average falls from 4 to 3.27 low wires per byte with random data.
- Part 3: with 200,000 random symbols the simulated eyes match the closed forms to four decimal places, and NRZ leads at every τ.

## Discussion

1. Why does the open-ended line in Part 1 overshoot to 1.081 V and then settle?

   <details><summary>Answer</summary>

   An open end reflects the whole incident wave ($\Gamma_L$ = 1), doubling the 0.541 V launched step at the far end. The reflection returns to the 34 Ω source, where $\Gamma_S$ = −0.0811, so only a small, inverted wave comes back, and each round trip shrinks the error by a further factor of 0.0811. A matched source would have absorbed the reflection entirely, which is why drivers are calibrated close to the line impedance.

   </details>

2. Why does the random-sequence eye in Part 3 match the closed form here, and when would it not?

   <details><summary>Answer</summary>

   The closed form assumes the worst pattern: every earlier symbol at the extreme that pushes the sample toward the threshold. At τ = 15 ps the cursors decay so fast that only the first few matter, and 200,000 random symbols contain every worst combination of those few. On a channel with a long tail of small cursors, the worst pattern spans many symbols and a random sequence almost never produces it. A short simulation then makes the eye look better than it is. Signal-integrity engineers compute worst-case eyes from the pulse response (peak distortion analysis) for that reason.

   </details>

3. When would DBI be counterproductive?

   <details><summary>Answer</summary>

   On an LVSTL bus, where ones cost energy, inverting bytes with many zeros would add ones. The rule must favour the cheap level for the bus's termination. DBI also costs an extra pin per byte and a little encode and decode latency. If data are already balanced and the pin is better spent on bandwidth, it may not pay.

   </details>

## Optional hardware

With a fast oscilloscope (at least 1 GHz bandwidth) and a few centimetres of 50 Ω coax, a pulse generator can show the reflections of Part 1 directly. Leave the far end open, then short it, then terminate it in 50 Ω, and compare each with the lattice diagram.
