# Term 4 Checkpoint · Solutions

Questions: [README.md](README.md). [verify_term4.py](verify_term4.py) checks every numerical answer and the letter of every multiple-choice answer. It recomputes each value by its own route: solved device equations, nodal analysis, field integrals, a simulated transmission line, synthetic traces and the Course 14 lab models. Each explanation names the chapter to revisit.

**Scoring by block:** Electronics II 17, electromagnetics 17, computer systems 16. Aim for at least 70% in each (12, 12 and 12 correct).

---

## Block 1 · Electronics II

**1. Answer: 12.6.** Each transistor carries $I_D$ = 100 µA, so $V_{ov} = \sqrt{2I_D/k}$ = 0.316 V and $g_m = 2I_D/V_{ov}$ = 0.632 mS. Taken between the drains, the differential gain is $g_mR_D$ = 0.632 mS × 20 kΩ. Single-ended, it would be half that. *([12-01](../../courses/12-electronics-2/chapters/12-01-differential-pairs.md))*

**2. Answer: (B) 0.447 V.** One transistor carries all of $I_{SS}$ when its overdrive reaches $\sqrt{2I_{SS}/k}$, while the other sits exactly at threshold. That gives $\lvert v_{id}\rvert = \sqrt{2 \times 200\ \mu\text{A}/2\ \text{mA/V}^2} = \sqrt{0.2}$ V. (A) is the quiescent overdrive $\sqrt{2I_D/k}$, and (C) is $\sqrt{4I_{SS}/k}$. *([12-01](../../courses/12-electronics-2/chapters/12-01-differential-pairs.md))*

**3. Answer: 40.0 dB.**

- Single-ended differential gain: $g_mR_D/2$ = 5.
- Common-mode gain: $g_mR_D/(1 + 2g_mR_{SS})$ = 10/201 = 0.0498.
- CMRR: 5/0.0498 = 100.5, i.e. 40.0 dB.

With perfectly matched halves and a differential output, the common-mode gain would be zero. Single-ended outputs and mismatch are what make CMRR finite. *([12-01](../../courses/12-electronics-2/chapters/12-01-differential-pairs.md))*

**4. Answer: (C) 5.10 MΩ.** $R_{out} = r_{o1} + r_{o2} + g_{m2}r_{o2}r_{o1}$ = 50 kΩ + 50 kΩ + 2 mS × 50 kΩ × 50 kΩ = 0.1 MΩ + 5.0 MΩ. (A) keeps only the gain term. (B) adds the two $r_o$ and forgets the cascode's boost. *([12-02](../../courses/12-electronics-2/chapters/12-02-active-loads-cascodes-multistage.md))*

**5. Answer: 13.3 GHz.** $f_T = g_m/[2\pi(C_{gs} + C_{gd})] = 5\ \text{mS}/(2\pi \times 60\ \text{fF})$. Including the feed-forward current through $C_{gd}$ raises the exact unity-current-gain frequency by about 1.4%. That is why exams state which definition they use. *([12-03](../../courses/12-electronics-2/chapters/12-03-frequency-response-miller-poles-zeros.md))*

**6. Answer: (D) 250 fF.** $C_{in} = C_{gs} + C_{gd}(1 + \lvert A\rvert)$ = 40 + 10 × 21 = 250 fF. (A) uses $\lvert A\rvert$ instead of $1 + \lvert A\rvert$. (B) ignores the Miller multiplication. (C) drops $C_{gs}$. *([12-03](../../courses/12-electronics-2/chapters/12-03-frequency-response-miller-poles-zeros.md))*

**7. Answer: 37.0 MHz.** The open-circuit time constants sum to $b_1$:

- $R_SC_{gs}$ = 10 kΩ × 100 fF = 1.0 ns;
- $R_{gd} = R_S + R_L + g_mR_SR_L$ = 15 kΩ + 100 kΩ = 115 kΩ, so $R_{gd}C_{gd}$ = 2.3 ns;
- $R_LC_L$ = 1.0 ns.

So $b_1$ = 4.3 ns and $f_{-3\text{dB}} \approx 1/(2\pi b_1)$. The $C_{gd}$ term dominates because of the Miller effect. This circuit's poles are real, so the estimate is conservative: the exact bandwidth is a little higher. *([12-04](../../courses/12-electronics-2/chapters/12-04-high-frequency-analysis-methods.md))*

**8. Answer: (A) 99.0.** $A_f = A/(1 + A\beta)$ = 10,000/101. (B) is the ideal $1/\beta$. (C) is $(1 + T)/T$ × 100, a common slip. *([12-05](../../courses/12-electronics-2/chapters/12-05-feedback-topologies.md))*

**9. Answer: 0.110%.** $A_f$ goes from 10,000/101 = 99.010 to 9000/91 = 98.901, a drop of 0.110%. The differential rule $(dA/A)/(1 + T)$ = 10%/101 gives 0.099%. It underestimates slightly because a 10% change is not small. Feedback cut the sensitivity about a hundredfold. *([12-05](../../courses/12-electronics-2/chapters/12-05-feedback-topologies.md))*

**10. Answer: (B) 51.8°.**

- The unity-gain frequency of the dominant-pole loop is $f_u = T_0f_1$ = 1 MHz, so the second pole sits at $r = f_2/f_u$ = 1.
- Solving $x^2(1 + x^2) = 1$ gives the crossover at $x$ = 0.786 of $f_u$.
- PM = 90° − arctan(0.786) = 51.8°.

(A) assumes crossover at the second pole. (C) is the usual design target, reached at $r$ = 1.5. *([12-06](../../courses/12-electronics-2/chapters/12-06-stability-and-compensation.md))*

**11. Answer: 79.6 MHz.** GBW = $g_{m1}/(2\pi C_c)$ = 1 mS/(2π × 2 pF). *([12-06](../../courses/12-electronics-2/chapters/12-06-stability-and-compensation.md))*

**12. Answer: (C) 50.0 V/µs.** During slewing, one input transistor carries the whole tail current, and all of it charges $C_c$: SR = $I_{SS}/C_c$ = 100 µA/2 pF = 50 V/µs. (A) uses half the tail current. (D) has the units wrong by 10⁶. *([12-08](../../courses/12-electronics-2/chapters/12-08-op-amp-internals.md))*

**13. Answer: 65.4%.** $\eta = (\pi/4)V_{op}/V_{CC} = (\pi/4)(10/12)$. *([12-07](../../courses/12-electronics-2/chapters/12-07-output-stages.md))*

**14. Answer: (A) 5.70 W.** The dissipation peaks at $V_{op} = 2V_{CC}/\pi$ = 9.55 V, where $P_D = 2V_{CC}^2/(\pi^2R_L)$ = 2 × 225/(9.87 × 8) = 5.70 W. (B) is the share of each transistor. (C) is the maximum output power $V_{CC}^2/(2R_L)$. *([12-07](../../courses/12-electronics-2/chapters/12-07-output-stages.md))*

**15. Answer: 1.59 kHz.** $f_0 = 1/(2\pi RC) = 1/(2\pi \times 10^{-4}\ \text{s})$. At $f_0$ the network's phase is zero and its gain is 1/3, so the amplifier needs a gain of 3. *([12-09](../../courses/12-electronics-2/chapters/12-09-oscillators.md))*

**16. Answer: (D) 2.25 MHz.** The tank capacitance is $C_1$ and $C_2$ in series, 0.5 nF, so $f_0 = 1/(2\pi\sqrt{10\ \mu\text{H} \times 0.5\ \text{nF}})$. (A) adds the capacitors in parallel. (B) uses one of them. (C) reports ω in rad/s as if it were hertz. *([12-09](../../courses/12-electronics-2/chapters/12-09-oscillators.md))*

**17. Answer: 12.9 µV.** $v_{rms} = \sqrt{4kTRB} = \sqrt{1.657 \times 10^{-20} \times 10^4 \times 10^6}$ V. A 1 kΩ resistor has 4.07 nV/√Hz, so 10 kΩ has 12.9 nV/√Hz; over √(10⁶ Hz) = 1000 √Hz that is 12.9 µV. *([12-10](../../courses/12-electronics-2/chapters/12-10-noise-in-circuits.md))*

## Block 2 · Electromagnetics

**18. Answer: (B) 99.9 pF/m.** $C' = 2\pi\varepsilon_0\varepsilon_r/\ln(b/a) = 2\pi \times 8.854 \times 10^{-12} \times 2.25/\ln 3.5$. (A) forgets $\varepsilon_r$. (C) uses $\pi$ for $2\pi$. (D) uses $\log_{10}$. *([13-02](../../courses/13-electromagnetics/chapters/13-02-electrostatics-boundary-value-problems.md))*

**19. Answer: 50.1 Ω.** $Z_0 = \sqrt{L'/C'}$ with $L' = (\mu_0/2\pi)\ln(b/a)$ = 0.251 µH/m. Equivalently, $Z_0 = (\eta_0/2\pi\sqrt{\varepsilon_r})\ln(b/a)$ = 40.0 Ω × 1.253. This is the standard 50 Ω cable geometry. *([13-07](../../courses/13-electromagnetics/chapters/13-07-transmission-lines-time-domain.md))*

**20. Answer: (A) 22.5 µN.** The plane acts like an image charge −1 nC at 1 cm below it, 2 cm from the real charge: $F = q^2/[4\pi\varepsilon_0(2d)^2] = 8.988 \times 10^9 \times 10^{-18}/(0.02)^2$ N. The force is attractive. (B) uses $d$ instead of $2d$. *([13-02](../../courses/13-electromagnetics/chapters/13-02-electrostatics-boundary-value-problems.md))*

**21. Answer: 4.57 mH.** $L = N^2\mu_0A/(\ell/\mu_r + g)$ = 40,000 × 1.257 × 10⁻⁶ × 10⁻⁴/(0.1 mm + 1.0 mm). The 1 mm gap has ten times the reluctance of the 20 cm core: without it, $L$ would be 50.3 mH. *([13-03](../../courses/13-electromagnetics/chapters/13-03-magnetostatics-and-inductance.md))*

**22. Answer: (C) 6.61 µm.** $\delta = 1/\sqrt{\pi f\mu_0\sigma}$, and δ scales as $1/\sqrt{f}$. Copper's δ is 66 µm at 1 MHz, so at 100 MHz it is 6.6 µm. (A) is the 1 MHz value and (B) the 1 GHz value. (D) has an extra √2. *([13-05](../../courses/13-electromagnetics/chapters/13-05-plane-waves.md))*

**23. Answer: 0.133 W/m².** $S_{av} = E_0^2/(2\eta_0)$ = 100/753.4. The ½ is there because $E_0$ is a peak amplitude. *([13-04](../../courses/13-electromagnetics/chapters/13-04-maxwells-equations.md))*

**24. Answer: (B) 4.00%.** $\Gamma = (\eta_2 - \eta_1)/(\eta_2 + \eta_1) = (1/1.5 - 1)/(1/1.5 + 1)$ = −0.2, and the reflected power fraction is $\lvert\Gamma\rvert^2$ = 0.04. (A) is $\lvert\Gamma\rvert$ and (C) the transmitted fraction. *([13-06](../../courses/13-electromagnetics/chapters/13-06-reflection-and-transmission.md))*

**25. Answer: 56.3°.** $\tan\theta_B = n_2/n_1$ = 1.5. At this angle the TM (parallel) reflection vanishes. *([13-06](../../courses/13-electromagnetics/chapters/13-06-reflection-and-transmission.md))*

**26. Answer: (D) 1.97 Ω.** For a uniform current, $R_{rad} = (2\pi\eta_0/3)(\ell/\lambda)^2$ = 789 Ω × (1/20)². (A) is the triangular-current (real short dipole) value, a quarter of this. (B) is the half-wave dipole. (C) forgets to square $\ell/\lambda$. *([13-11](../../courses/13-electromagnetics/chapters/13-11-radiation-and-antennas.md))*

**27. Answer: 1.77.** $\Gamma = (25 + j25)/(125 + j25)$, so $\lvert\Gamma\rvert$ = 35.36/127.5 = 0.277. Then VSWR = $(1 + 0.277)/(1 - 0.277)$. *([13-08](../../courses/13-electromagnetics/chapters/13-08-transmission-lines-sinusoidal-steady-state.md))*

**28. Answer: (A) 11.1 dB.** RL = $-20\log_{10}\lvert\Gamma\rvert = -20\log_{10}0.277$. (B) uses 10 log. (C) is the mismatch loss $-10\log_{10}(1 - \lvert\Gamma\rvert^2)$. (D) uses 40 log. *([13-08](../../courses/13-electromagnetics/chapters/13-08-transmission-lines-sinusoidal-steady-state.md))*

**29. Answer: 70.7 Ω.** $Z_1 = \sqrt{Z_0R_L} = \sqrt{50 \times 100}$. A quarter-wave line transforms 100 Ω into $Z_1^2/100$ = 50 Ω. *([13-08](../../courses/13-electromagnetics/chapters/13-08-transmission-lines-sinusoidal-steady-state.md))*

**30. Answer: (C) 2.67 V.**

1. The launched wave is $v^+ = 3 \times 50/75$ = 2 V. The open end reflects with $\Gamma_L$ = +1, so the far end jumps to 4 V at $t = T$.
2. The reflection returns to the source, where $\Gamma_S = (25 - 50)/75 = -1/3$. That sends −2/3 V forward.
3. The −2/3 V wave doubles on arrival at the open end, so at $3T$ the voltage drops by 4/3 V to 2.67 V.

The voltage then rings toward the DC value of 3 V. (A) is the first plateau, (B) the final value and (D) the plateau after $5T$. *([13-07](../../courses/13-electromagnetics/chapters/13-07-transmission-lines-time-domain.md))*

**31. Answer: 39.6 cm.** $d = v_pt/2 = 0.66 \times 2.998 \times 10^8 \times 4.0 \times 10^{-9}/2$ m. The 4.0 ns is a round trip. *([13-07](../../courses/13-electromagnetics/chapters/13-07-transmission-lines-time-domain.md))*

**32. Answer: (B) 75.0 Ω.** $Z = Z_0(1 + \rho)/(1 - \rho) = 50 \times 1.2/0.8$. A positive reflection means a higher impedance. (A) inverts the ratio. (C) and (D) each keep only half of it. *([13-07](../../courses/13-electromagnetics/chapters/13-07-transmission-lines-time-domain.md))*

**33. Answer: 6.56 GHz.** $f_c = c/(2a) = 2.998 \times 10^8/(2 \times 0.02286)$ Hz. This is the standard X-band guide, used from about 8.2 to 12.4 GHz. *([13-10](../../courses/13-electromagnetics/chapters/13-10-waveguides-and-resonators.md))*

**34. Answer: (D) −30.1 dBm.**

- $\lambda$ = 0.125 m, so FSPL = $20\log_{10}(4\pi R/\lambda)$ = 80.05 dB.
- $P_r$ = 30 dBm + 10 dBi + 10 dBi − 80.05 dB = −30.05 dBm, which rounds to −30.1 dBm.

(A) drops both antenna gains, (B) one of them, and (C) takes 1 W as 0 dBm. *([13-11](../../courses/13-electromagnetics/chapters/13-11-radiation-and-antennas.md))*

## Block 3 · Computer systems

**35. Answer: 0.850 s.** CPI = 0.5 × 1 + 0.3 × 2 + 0.2 × 3 = 1.7, so $T = \text{IC} \times \text{CPI}/f = 10^9 \times 1.7/(2 \times 10^9)$ s. *([14-01](../../courses/14-computer-organization-and-architecture/chapters/14-01-performance-power-iron-law.md))*

**36. Answer: (A) 6.40.** Amdahl's law gives $S = 1/(0.1 + 0.9/16)$ = 1/0.15625. (B) is Gustafson's scaled speedup, (C) the limit as cores → ∞, and (D) assumes perfect scaling. *([14-01](../../courses/14-computer-organization-and-architecture/chapters/14-01-performance-power-iron-law.md))*

**37. Answer: 51.2%.** $P \propto V^2f$, so the new power is (0.8)² × 0.8 = 0.512 of the old. Each operation's energy fell to 64% ($\propto V^2$). The lower clock accounts for the rest. *([14-01](../../courses/14-computer-organization-and-architecture/chapters/14-01-performance-power-iron-law.md))*

**38. Answer: (C) 371 ns.** The clock is the slowest stage plus overhead: 350 + 20 = 370 ps. The pipeline needs 5 cycles to fill, then completes one instruction per cycle, so 1000 instructions take 1004 cycles × 370 ps = 371.48 ns. (A) ignores the fill. (B) runs each instruction through all five stages alone. (D) is the single-cycle design (1300 + 20 ps per instruction). *([14-06](../../courses/14-computer-organization-and-architecture/chapters/14-06-pipelining-and-hazards.md))*

**39. Answer: 1.44.** Cycles = $N + 4 + S + 2T$ = 100 + 4 + 10 + 30 = 144, so CPI = 144/100. Each taken branch resolved in EX flushes the two instructions fetched behind it. *([14-06](../../courses/14-computer-organization-and-architecture/chapters/14-06-pipelining-and-hazards.md))*

**40. Answer: (B) 1.15.** CPI = 1 + 0.20 × 0.05 × 15. (A) forgets that only 20% of instructions are branches. (C) forgets the penalty. (D) charges the penalty on every branch. *([14-07](../../courses/14-computer-organization-and-architecture/chapters/14-07-branch-prediction-and-speculation.md))*

**41. Answer: 19.**

- Sets: 32,768/(64 × 4) = 128, so 7 index bits.
- Offset: 64-byte blocks, so 6 bits.
- Tag: 32 − 7 − 6 = 19 bits.

*([14-09](../../courses/14-computer-organization-and-architecture/chapters/14-09-memory-hierarchy-and-caches.md))*

**42. Answer: (D) 3.50 cycles.** AMAT = $t_1 + m_1(t_2 + m_{2}t_{mem})$ = 1 + 0.05 × (10 + 0.2 × 200) = 1 + 0.05 × 50. (A) forgets to multiply the memory term by the L1 miss rate. (B) ignores memory. (C) treats every L1 miss as an L2 miss. *([14-09](../../courses/14-computer-organization-and-architecture/chapters/14-09-memory-hierarchy-and-caches.md))*

**43. Answer: 0x0ABCD678.** The 12-bit page offset 0x678 passes through unchanged. VPN[1] = 0x048 and VPN[0] = 0x345 select the two page-table entries. The PA is PPN × 4096 + offset = 0x0ABCD000 + 0x678. *([14-10](../../courses/14-computer-organization-and-architecture/chapters/14-10-virtual-memory.md))*

**44. Answer: (A) 32 KiB.** Aliasing cannot occur when the index and offset bits all lie within the page offset, i.e. capacity/associativity ≤ page size. That allows 8 × 4 KiB. (B) is the direct-mapped limit, the page size itself. (C) assumes 2 ways. *([14-10](../../courses/14-computer-organization-and-architecture/chapters/14-10-virtual-memory.md))*

**45. Answer: 31.5 GB/s.** 16 GT/s × 16 lanes × 128/130 ÷ 8 bits per byte. The usual "32 GB/s" headline ignores the encoding overhead. Packet headers reduce delivered throughput further. *([14-11](../../courses/14-computer-organization-and-architecture/chapters/14-11-io-buses-and-interconnect.md))*

**46. Answer: (C) 5.25.** The average is $2(k^2 - 1)/(3k)$ = 2 × 63/24. (A) is $k$. (B) is the worst case, $2(k - 1)$. (D) is the large-$k$ approximation $2k/3$. *([14-11](../../courses/14-computer-organization-and-architecture/chapters/14-11-io-buses-and-interconnect.md))*

**47. Answer: 0xC0C80000.** −6.25 = −1.5625 × 2².

- Sign: 1.
- Exponent: 2 + 127 = 129 = 1000 0001.
- Fraction: 0.5625 = 0.1001 in binary, so 1001 followed by 19 zeros.

Grouped in fours: 1100 0000 1100 1000 0000 … = 0xC0C80000. *([14-04](../../courses/14-computer-organization-and-architecture/chapters/14-04-computer-arithmetic-and-number-formats.md))*

**48. Answer: (B) 3; core 0 Invalid, core 1 Modified.**

1. Core 0's read misses with no other holder, so BusRd leaves it Exclusive.
2. Core 0's write upgrades E to M silently, with no bus transaction.
3. Core 1's read misses. Its BusRd makes core 0 flush the dirty data, and both cores end in Shared.
4. Core 1's write in S sends BusUpgr, which invalidates core 0.

That is three transactions. (A) counts the silent upgrade as one. *([14-12](../../courses/14-computer-organization-and-architecture/chapters/14-12-multicore-coherence-consistency.md))*

**49. Answer: 41.7%.** The warp issues both sides in turn: 10 + 20 = 30 issue slots. Useful lane-slots: 24 × 10 + 8 × 20 = 400 out of 32 × 30 = 960. *([14-13](../../courses/14-computer-organization-and-architecture/chapters/14-13-gpus-and-simt.md))*

**50. Answer: (D) 20.0 TFLOP/s.** Attainable = min(peak, bandwidth × intensity) = min(100, 2.0 × 10) TFLOP/s. The ridge sits at 100/2 = 50 FLOP/byte, so this kernel is memory-bound. (A) assumes it is compute-bound. (B) is the ridge's value used as a speed. *([14-15](../../courses/14-computer-organization-and-architecture/chapters/14-15-roofline-and-benchmarks.md))*

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| T4.01 | differential gain | 12.6 | — |
| T4.02 | full-switching input | 0.447 | V |
| T4.03 | CMRR | 40.0 | dB |
| T4.04 | cascode output resistance | 5.10 | MΩ |
| T4.05 | f_T | 13.3 | GHz |
| T4.06 | Miller input capacitance | 250 | fF |
| T4.07 | OCTC bandwidth | 37.0 | MHz |
| T4.08 | closed-loop gain | 99.0 | — |
| T4.09 | closed-loop gain drop | 0.110 | % |
| T4.10 | phase margin | 51.8 | ° |
| T4.11 | gain–bandwidth product | 79.6 | MHz |
| T4.12 | slew rate | 50.0 | V/µs |
| T4.13 | class B efficiency | 65.4 | % |
| T4.14 | worst-case dissipation | 5.70 | W |
| T4.15 | Wien frequency | 1.59 | kHz |
| T4.16 | Colpitts frequency | 2.25 | MHz |
| T4.17 | thermal noise | 12.9 | µV |
| T4.18 | coax capacitance | 99.9 | pF/m |
| T4.19 | coax impedance | 50.1 | Ω |
| T4.20 | image force | 22.5 | µN |
| T4.21 | gapped-core inductance | 4.57 | mH |
| T4.22 | skin depth | 6.61 | µm |
| T4.23 | power density | 0.133 | W/m² |
| T4.24 | reflected power | 4.00 | % |
| T4.25 | Brewster angle | 56.3 | ° |
| T4.26 | radiation resistance | 1.97 | Ω |
| T4.27 | VSWR | 1.77 | — |
| T4.28 | return loss | 11.1 | dB |
| T4.29 | transformer impedance | 70.7 | Ω |
| T4.30 | far-end voltage, 3T to 5T | 2.67 | V |
| T4.31 | TDR distance | 39.6 | cm |
| T4.32 | discontinuity impedance | 75.0 | Ω |
| T4.33 | TE₁₀ cutoff | 6.56 | GHz |
| T4.34 | received power | −30.1 | dBm |
| T4.35 | run time | 0.850 | s |
| T4.36 | Amdahl speedup | 6.40 | — |
| T4.37 | new power | 51.2 | % |
| T4.38 | time for 1000 instructions | 371 | ns |
| T4.39 | CPI | 1.44 | — |
| T4.40 | CPI with mispredictions | 1.15 | — |
| T4.41 | tag bits | 19 | bits |
| T4.42 | AMAT | 3.50 | cycles |
| T4.43 | physical address | 0x0ABCD678 | — |
| T4.44 | largest alias-free VIPT cache | 32 | KiB |
| T4.45 | PCIe 4.0 x16 bandwidth | 31.5 | GB/s |
| T4.46 | average mesh hops | 5.25 | hops |
| T4.47 | FP32 pattern of −6.25 | 0xC0C80000 | — |
| T4.49 | SIMD efficiency | 41.7 | % |
| T4.50 | attainable throughput | 20.0 | TFLOP/s |
