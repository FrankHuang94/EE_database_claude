# Term 4 Checkpoint · FE-Style Practice Exam

**Covers:** Courses 12–14 (Electronics II, electromagnetics, computer organization and architecture). **Questions:** 50 (multiple choice and numeric entry). **Time:** 150 minutes, the FE pace of about 3 minutes per question.
**Materials:** an FE-approved calculator and the *NCEES FE Reference Handbook* only (free PDF from NCEES); no course notes or sheets. Finding formulas in the handbook quickly is part of the practice.
**Scoring:** one point per question. Score each block separately and aim for at least 70% in every block. Write every miss into your error log with its cause, and re-solve it a week later. Solutions with full explanations, each pointing to the chapter to revisit, are in [solutions.md](solutions.md); open them only after you finish.

**Conventions:**

- For numeric entry, give 3 significant figures unless the question says otherwise.
- MOSFETs: square law $I_D = \tfrac12kV_{ov}^2$, $g_m = 2I_D/V_{ov}$. Loop gain $T = A\beta$. Noise at 300 K, with $k_B$ = 1.381 × 10⁻²³ J/K.
- $c$ = 2.998 × 10⁸ m/s, $\varepsilon_0$ = 8.854 × 10⁻¹² F/m, $\mu_0$ = 4π × 10⁻⁷ H/m, $\eta_0$ = 376.7 Ω. Fields are peak phasors. Media are lossless and nonmagnetic unless stated.
- 1 KiB = 1024 bytes for memory sizes; 1 GB/s = 10⁹ bytes/s for bandwidths. RISC-V RV32I unless stated.

---

## Block 1 · Electronics II (questions 1–17)

**1.** *Numeric entry.* A MOS differential pair has a 200 µA tail current, $k$ = 2 mA/V² for each transistor and 20 kΩ drain resistors. Find its small-signal differential gain, taking the output between the two drains.

**2.** The pair of question 1 steers the whole tail current into one transistor when the differential input reaches:
(A) 0.316 V · (B) 0.447 V · (C) 0.632 V · (D) 0.224 V

**3.** *Numeric entry.* A differential pair has $g_m$ = 1 mS per transistor, $R_D$ = 10 kΩ and a tail source with 100 kΩ output resistance. Taking the output from one drain, find its common-mode rejection ratio, in dB.

**4.** A MOS cascode has $r_{o1} = r_{o2}$ = 50 kΩ and cascode transconductance $g_{m2}$ = 2 mS. Its output resistance is:
(A) 5.00 MΩ · (B) 100 kΩ · (C) 5.10 MΩ · (D) 2.55 MΩ

**5.** *Numeric entry.* A MOSFET has $g_m$ = 5 mS, $C_{gs}$ = 50 fF and $C_{gd}$ = 10 fF. Find its transition frequency $f_T$, in GHz, neglecting the feed-forward current through $C_{gd}$.

**6.** A common-source stage has a gain of −20 from gate to drain, $C_{gs}$ = 40 fF and $C_{gd}$ = 10 fF. With the Miller approximation, its input capacitance is:
(A) 240 fF · (B) 50.0 fF · (C) 210 fF · (D) 250 fF

**7.** *Numeric entry.* A common-source stage is driven from 10 kΩ. It has $g_m$ = 2 mS, a total drain load of 5 kΩ, $C_{gs}$ = 100 fF, $C_{gd}$ = 20 fF and 200 fF from drain to ground. Estimate its −3 dB bandwidth with open-circuit time constants, in MHz.

**8.** An amplifier with open-loop gain 10,000 is placed in a negative-feedback loop with β = 0.01. Its closed-loop gain is:
(A) 99.0 · (B) 100 · (C) 101 · (D) 9.90

**9.** *Numeric entry.* The open-loop gain of the amplifier in question 8 falls by 10%, to 9000. Find the exact percentage by which the closed-loop gain falls.

**10.** A loop gain has a DC value of 10⁵, a dominant pole at 10 Hz and a second pole at 1.0 MHz. Its phase margin is:
(A) 45.0° · (B) 51.8° · (C) 60.0° · (D) 76.3°

**11.** *Numeric entry.* A Miller-compensated two-stage op-amp has input-pair transconductance $g_{m1}$ = 1 mS and compensation capacitor $C_c$ = 2 pF. Find its gain–bandwidth product, in MHz.

**12.** The op-amp of question 11 has a tail current of 100 µA. Its slew rate, limited by charging $C_c$, is:
(A) 25.0 V/µs · (B) 100 V/µs · (C) 50.0 V/µs · (D) 0.0500 V/µs

**13.** *Numeric entry.* A class B push-pull stage on ±12 V supplies delivers a 10 V peak sine to a resistive load. Find its efficiency, in percent.

**14.** A class B stage on ±15 V supplies drives an 8 Ω load. The worst-case total dissipation in its two output transistors, over all sine amplitudes, is:
(A) 5.70 W · (B) 2.85 W · (C) 14.1 W · (D) 11.4 W

**15.** *Numeric entry.* A Wien-bridge oscillator uses $R$ = 10 kΩ and $C$ = 10 nF in both arms. Find its oscillation frequency, in kHz.

**16.** A Colpitts oscillator has $L$ = 10 µH and $C_1 = C_2$ = 1.0 nF. It oscillates at:
(A) 1.13 MHz · (B) 1.59 MHz · (C) 14.1 MHz · (D) 2.25 MHz

**17.** *Numeric entry.* Find the rms thermal-noise voltage of a 10 kΩ resistor in a 1.0 MHz bandwidth at 300 K, in µV.

## Block 2 · Electromagnetics (questions 18–34)

**18.** A coaxial cable has an inner conductor of radius 0.50 mm, an outer conductor of inner radius 1.75 mm and polyethylene insulation with $\varepsilon_r$ = 2.25. Its capacitance per metre is:
(A) 44.4 pF/m · (B) 99.9 pF/m · (C) 50.0 pF/m · (D) 230 pF/m

**19.** *Numeric entry.* Find the characteristic impedance of the cable of question 18, in Ω.

**20.** A point charge of 1.0 nC sits 1.0 cm above a large grounded conducting plane. The magnitude of the force on it is:
(A) 22.5 µN · (B) 89.9 µN · (C) 11.2 µN · (D) 44.9 µN

**21.** *Numeric entry.* A 200-turn coil is wound on a core with $\mu_r$ = 2000, a 20 cm mean path and 1.0 cm² cross-section, cut by a 1.0 mm air gap. Neglecting fringing and leakage, find its inductance, in mH.

**22.** The skin depth of copper ($\sigma$ = 5.8 × 10⁷ S/m) at 100 MHz is:
(A) 66.1 µm · (B) 2.09 µm · (C) 6.61 µm · (D) 9.35 µm

**23.** *Numeric entry.* A plane wave in free space has a peak electric field of 10 V/m. Find its time-average power density, in W/m².

**24.** A plane wave in air strikes glass ($n$ = 1.5) at normal incidence. The fraction of the incident power reflected is:
(A) 20.0% · (B) 4.00% · (C) 96.0% · (D) 2.00%

**25.** *Numeric entry.* Find the Brewster angle for light passing from air into glass with $n$ = 1.5, in degrees.

**26.** A short dipole of length λ/20 carries a uniform current along its length. Its radiation resistance is:
(A) 0.493 Ω · (B) 73.1 Ω · (C) 39.4 Ω · (D) 1.97 Ω

**27.** *Numeric entry.* A 50 Ω line is terminated in $Z_L$ = 75 + j25 Ω. Find the voltage standing-wave ratio.

**28.** The return loss of the termination in question 27 is:
(A) 11.1 dB · (B) 5.57 dB · (C) 0.348 dB · (D) 22.3 dB

**29.** *Numeric entry.* Find the characteristic impedance of a quarter-wave transformer that matches a 100 Ω resistive load to a 50 Ω line, in Ω.

**30.** A 3.0 V step source with 25 Ω internal resistance drives a lossless 50 Ω line of one-way delay $T$, open at the far end. Between $t = 3T$ and $t = 5T$ the voltage at the open end is:
(A) 4.00 V · (B) 3.00 V · (C) 2.67 V · (D) 3.11 V

**31.** *Numeric entry.* A time-domain reflectometer on a cable with velocity factor 0.66 sees a reflection 4.0 ns after it launches its step. Find the distance to the discontinuity, in cm.

**32.** The reflected step in question 31 is +0.20 times the incident step on the 50 Ω cable. The discontinuity's impedance is:
(A) 33.3 Ω · (B) 75.0 Ω · (C) 60.0 Ω · (D) 62.5 Ω

**33.** *Numeric entry.* Find the TE₁₀ cutoff frequency of an air-filled rectangular waveguide with broad dimension $a$ = 22.86 mm, in GHz.

**34.** A 2.4 GHz link transmits 1.0 W through a 10 dBi antenna to a 10 dBi receiving antenna 100 m away in free space. The received power is:
(A) −50.1 dBm · (B) −40.1 dBm · (C) −60.1 dBm · (D) −30.1 dBm

## Block 3 · Computer systems (questions 35–50)

**35.** *Numeric entry.* A program executes 10⁹ instructions: 50% ALU operations at 1 cycle each, 30% loads and stores at 2 cycles, and 20% branches at 3 cycles. Find its run time on a 2.0 GHz processor, in seconds.

**36.** 90% of a program's run time parallelizes perfectly. Its speedup on 16 cores is:
(A) 6.40 · (B) 14.5 · (C) 10.0 · (D) 16.0

**37.** *Numeric entry.* A processor's supply drops from 1.0 V to 0.8 V and its clock from 3.0 GHz to 2.4 GHz, with switching activity and capacitance unchanged. Find its new dynamic power as a percentage of the old.

**38.** A five-stage pipeline has stage delays of 300, 200, 250, 350 and 200 ps and 20 ps of pipeline-register overhead per stage. With no hazards, the time to execute 1000 instructions is:
(A) 370 ns · (B) 1850 ns · (C) 371 ns · (D) 1320 ns

**39.** *Numeric entry.* On the classic five-stage pipeline (forwarding, branches resolved in EX, predict not-taken), a 100-instruction sequence has 10 load-use stalls and 15 taken branches. Counting every cycle from the first instruction's fetch to the last one's write-back, find its CPI.

**40.** A processor has a base CPI of 1.0. Branches are 20% of instructions, 5% of them are mispredicted, and each misprediction costs 15 cycles. Its CPI is:
(A) 1.75 · (B) 1.15 · (C) 1.01 · (D) 4.00

**41.** *Numeric entry.* A 32 KiB, 4-way set-associative cache with 64-byte blocks serves 32-bit addresses. How many tag bits does each line hold?

**42.** An L1 cache hits in 1 cycle and misses 5% of the time. The L2 hits in 10 cycles and misses 20% of the L1 misses that reach it. Memory takes 200 cycles. The average memory access time is:
(A) 41.5 cycles · (B) 1.50 cycles · (C) 11.5 cycles · (D) 3.50 cycles

**43.** *Numeric entry.* Under RISC-V Sv32, the virtual address 0x1234_5678 maps through a 4 KiB leaf page-table entry whose physical page number is 0x0ABCD. Give the physical address in hexadecimal.

**44.** An L1 cache is virtually indexed and physically tagged, with 8 ways and 4 KiB pages. The largest capacity it can have without aliasing is:
(A) 32 KiB · (B) 4 KiB · (C) 8 KiB · (D) 128 KiB

**45.** *Numeric entry.* Find the per-direction bandwidth of a PCIe 4.0 x16 link (16 GT/s per lane, 128b/130b encoding), in GB/s.

**46.** The average hop count between two nodes of an 8 × 8 mesh network-on-chip under uniform random traffic, a node sending to itself included, is:
(A) 8.00 · (B) 14.0 · (C) 5.25 · (D) 5.33

**47.** *Numeric entry.* Give the IEEE 754 single-precision (FP32) bit pattern of −6.25 in hexadecimal.

**48.** Two cores run the MESI snooping protocol and block A starts uncached. Core 0 reads A, core 0 writes A, core 1 reads A, then core 1 writes A. How many bus transactions occur, and what are the final states?
(A) 4; core 0 Invalid, core 1 Modified · (B) 3; core 0 Invalid, core 1 Modified · (C) 3; core 0 Shared, core 1 Modified · (D) 2; core 0 Invalid, core 1 Exclusive

**49.** *Numeric entry.* In a 32-thread warp, 24 threads take the *then* side of a branch (10 instructions) and 8 take the *else* side (20 instructions). Find the SIMD efficiency of the branch, in percent.

**50.** An accelerator has 100 TFLOP/s of peak compute and 2.0 TB/s of memory bandwidth. A kernel with an arithmetic intensity of 10 FLOP/byte can reach at most:
(A) 100 TFLOP/s · (B) 50.0 TFLOP/s · (C) 10.0 TFLOP/s · (D) 20.0 TFLOP/s
