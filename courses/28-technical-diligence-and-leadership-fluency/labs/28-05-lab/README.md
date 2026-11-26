# Lab 28-05 · Curves Behind Single-Point Claims

**Objective.** Use small models to place a converter claim against the published figure-of-merit frontier and the thermal ceiling, see how clock jitter limits SNR as input frequency rises, compare class-B and Doherty efficiency across back-off, and see how battery life depends on duty cycle, code loop and temperature.

**Chapter:** [28-05 · Domain Question Banks II](../../chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md)

## Background

The lab uses the chapter's models with its assumed parameters:

- §3.1: ENOB, the Walden and Schreier figures, the 8kT·SNR ceiling $10\log_{10}(1/16k_BT)$, and jitter-limited SNR $-20\log_{10}(2\pi f_{in}\sigma_t)$.
- §3.2: ideal class-B efficiency $(\pi/4)a$ and the ideal symmetric Doherty, $(\pi/2)a$ below half amplitude and $(\pi/2)a^2/(3a - 1)$ above it, for output amplitude $a$ relative to peak.
- §3.3–3.5: converter loss and chains, area-array density, compound yield, duty-cycled current and battery life.
- §3.6: Cpk, the normal tail and the chi-square bound on σ.

## Files

- `bankcheck.py`: the models.
- `28-05-bankcheck-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · A claim against the frontier** (notebook). *Predict* the Schreier figure of Example 28-05.1's claim (66 dB SNDR, 1 GS/s) at 5 mW. Recompute the published 1 GS/s result of [R-336] (68.2 dB SNDR at 15.3 mW). Then plot Schreier figure against power for the claim, with the published point and the ceiling.

**Part 2 · Jitter against input frequency** (notebook). *Predict* the highest input frequency at which a 50 fs clock still allows 60 dB SNR, and the jitter-limited SNR at 2 GHz. Then plot jitter-limited SNR against input frequency for 25, 50, 100 and 200 fs.

**Part 3 · Efficiency against back-off** (notebook). *Predict* the ideal Doherty and class-B efficiencies at 9 dB back-off. Then plot both against back-off from 0 to 12 dB, find the Doherty's dip between its peaks, and mark the published GaN range of 38.5–46.5% at 6 dB [R-385].

**Part 4 · Battery life against duty cycle** (notebook). *Predict* Example 28-05.6's average current and battery life if the MCU wakes every 10 s instead of every second (25 °C, CoreMark figure). Then plot life against the wake interval for the CoreMark and `while(1)` figures at 25 °C and the CoreMark figure at 85 °C.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 28-05.a | Schreier figure of the claim at 5 mW | 176.0 | dB |
| Lab 28-05.a1 | published 1 GS/s point, recomputed | 173.3 | dB |
| Lab 28-05.b | highest input for 60 dB at 50 fs | 3.18 | GHz |
| Lab 28-05.b1 | SNR at 2 GHz with 50 fs | 64.0 | dB |
| Lab 28-05.c | Doherty at 9 dB back-off | 55.7 | % |
| Lab 28-05.c1 | class B at 9 dB back-off | 27.9 | % |
| Lab 28-05.c2 | Doherty dip at two-thirds amplitude | 69.8 | % |
| Lab 28-05.d | average current, 10 s wake | 3.90 | µA |
| Lab 28-05.d1 | battery life, 10 s wake | 6.59 | years |

## Discussion

1. At 5 mW the claim would score **176.0** dB, about 3 dB above the published **173.3** dB at this speed. Each halving of power adds 3 dB to the Schreier figure, so a power claim a few times below the frontier at the same SNDR is a claim to beat the literature, and needs the measurement behind it.
2. A 50 fs clock allows 60 dB up to **3.18** GHz and gives **64.0** dB at 2 GHz. Every doubling of input frequency costs 6 dB, so direct RF sampling at higher bands is a clocking problem as much as a converter problem.
3. At 9 dB back-off the ideal Doherty reaches **55.7**% against class B's **27.9**%, and between its peaks it dips only to **69.8**%. Published GaN results sit well below the ideal curve, which is why a claim near the ideal needs its signal, ACLR and DPD stated.
4. Waking every 10 s cuts the average current to **3.90** µA and stretches the life to **6.59** years, before battery derating; at long intervals the sleep and radio currents dominate and the code loop matters less, while temperature matters more.

## Optional hardware

With a low-power MCU development board, a coin cell holder and a current-measurement tool (a source-measure unit or an energy-profiling board), measure the average current of a duty-cycled loop at room temperature and, if a warm chamber or hot plate is available, at an elevated temperature, and compare with the data-sheet model.
