# Term 6 Checkpoint · Solutions

Questions: [README.md](README.md). [verify_term6.py](verify_term6.py) checks every numerical answer and the letter of every multiple-choice answer. Where a second route exists it recomputes the value that way:

- numerical minimization for logical effort;
- an RC-ladder transient for the wire delay;
- integrating the thermal-noise spectrum for $kT/C$;
- quantizing and jitter-sampling synthetic sines;
- noise temperatures for the cascade;
- impedance arithmetic for the match;
- intercept-line solving for IIP3;
- half-sine current integration for class B;
- phasor arithmetic for power flow and faults;
- charge conservation on the bitline;
- root-finding for the MRAM barrier and the zero-error test;
- Bayes' rule by enumeration for escapes.

Each explanation names the chapter to revisit.

**Scoring by block:** digital VLSI 7, analog and mixed-signal 7, RF 7, power 8, memory 7, high-speed I/O 7, fabrication and reliability 7. Aim for at least 70% in each (5 in each block of 7, and 6 in power).

---

## Block 1 · Digital VLSI

**1. Answer: 0.384.** $P = \alpha CV_{DD}^2f = 0.15 \times 2\ \text{nF} \times 0.64\ \text{V}^2 \times 2\ \text{GHz}$, in watts. The activity factor counts full 0→1→0 cycles per clock. *([19-06](../../courses/19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md))*

**2. Answer: (B) 14.0.** $G = 1 \times \tfrac43 \times \tfrac53 = \tfrac{20}{9}$ and $H$ = 12, so $F = GH = \tfrac{80}{3}$; the best stage effort is $F^{1/3}$ and $P = 1 + 2 + 2 = 5$, so $\hat D = 3F^{1/3} + P$. (A) drops the parasitic delay; (C) ignores logical effort ($F = H$); (D) adds $F$ and $P$ as if the path had one stage. *([19-04](../../courses/19-digital-vlsi-design/chapters/19-04-sizing-and-logical-effort.md))*

**3. Answer: 186.** $t \approx 0.69R_d(C_w + C_L) + R_w(0.38C_w + 0.69C_L) = 0.69 \times 1\ \text{kΩ} \times 210\ \text{fF} + 500\ \Omega \times (76 + 6.9)\ \text{fF}$, in ps. The driver sees all the capacitance; the wire's own resistance sees its distributed capacitance at 0.38 and the load at 0.69. *([19-05](../../courses/19-digital-vlsi-design/chapters/19-05-interconnect.md))*

**4. Answer: (C) 2.13 GHz.** $T_c \ge t_{pcq} + t_{pd} + t_{setup} + t_{jitter}$ = 470 ps. (A) ignores jitter; (B) uses only the logic delay; (D) counts the jitter twice. *([19-07](../../courses/19-digital-vlsi-design/chapters/19-07-sequential-timing-and-clocking.md))*

**5. Answer: 4.45e3.** $DL = 1 - 0.8^{0.02}$, expressed in parts per million of shipped parts. The approximation $(1 - T)(-\ln Y)$ gives nearly the same value. Even 98% coverage leaves thousands of ppm, which is why high-reliability products push coverage much higher. *([19-12](../../courses/19-digital-vlsi-design/chapters/19-12-design-for-test.md))*

**6. Answer: (A) 4.64.** Subthreshold current rises one decade per slope $S$, so the factor is $10^{60/90}$. (B) inverts the exponent; (C) uses twice the slope; (D) uses $e$ instead of 10. *([19-06](../../courses/19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md))*

**7. Answer: 121.** $e^{400/20}/(20\ \text{ps} \times 2\ \text{GHz} \times 100\ \text{MHz}) = e^{20}/(4 \times 10^6\ \text{s}^{-1})$. Two minutes is far too short for a product; a second flip-flop stage multiplies the MTBF by about $e^{t/\tau}$ again. *([19-07](../../courses/19-digital-vlsi-design/chapters/19-07-sequential-timing-and-clocking.md))*

## Block 2 · Analog and mixed-signal IC design

**8. Answer: (D) 29.8 V⁻¹.** Deep in weak inversion $g_m/I_D \to 1/(nV_T) = 1/(1.3 \times 25.85\ \text{mV})$, the largest value any operating point reaches. (A) omits $n$; (B) uses $n^2$; (C) is the strong-inversion $2/V_{ov}$ at 0.2 V. *([20-01](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-01-analog-design-fundamentals-gm-id.md))*

**9. Answer: 79.6.** $\omega_u = g_{m1}/C_c$, so $f_u = 1\ \text{mS}/(2\pi \times 2\ \text{pF})$, in MHz. *([20-02](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md))*

**10. Answer: (B) 50.0 V/µs.** During slewing the whole tail current charges $C_c$: SR $= I_{SS}/C_c$. (A) uses half the tail current; (C) doubles it; (D) multiplies by 2π. *([20-02](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md))*

**11. Answer: 45.5.** $v_n = \sqrt{kT/C} = \sqrt{1.381 \times 10^{-23} \times 300/(2 \times 10^{-12})}$, in µV. The switch resistance cancels: a larger $R$ means more noise density but less bandwidth. *([20-05](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-05-comparators-and-sample-and-hold.md))*

**12. Answer: (C) 74.0 dB.** SQNR $= 6.02N + 1.76$ dB for a full-scale sine. (A) drops the 1.76 dB; (B) is the 11-bit value; (D) adds 3 dB as if the converter were oversampled twice. *([20-06](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-06-data-converter-fundamentals.md))*

**13. Answer: 84.0.** $-20\log_{10}(2\pi \times 10^8 \times 10^{-13})$. About 14 effective bits at 100 MHz, so a 16-bit converter at this input frequency is limited by its clock. *([20-05](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-05-comparators-and-sample-and-hold.md))*

**14. Answer: (A) 53.8 mV.** $\Delta V_{BE} = V_T\ln N = 25.85\ \text{mV} \times \ln 8$, the PTAT voltage of a bandgap. (B) uses $\log_{10}$; (C) multiplies by $N$; (D) halves the result. *([20-03](../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-03-bandgap-references.md))*

## Block 3 · RF and microwave

**15. Answer: 2.67.** In linear terms $F = F_1 + (F_2 - 1)/G_1 + (F_3 - 1)/(G_1G_2)$, with $F_1 = 10^{0.15}$, $G_1 = 10^{1.5}$, $F_2 = 10$, $G_2 = 10^{0.8}$ and $F_3 = 10^{1.5}$; then NF $= 10\log_{10}F$. The LNA's gain hides most of the mixer's 10 dB. *([21-03](../../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md))*

**16. Answer: (D) −85.0 dBm.** $-174 + 10\log_{10}(2 \times 10^7) + 6 + 10$. (A) forgets the SNR; (B) forgets the bandwidth; (C) counts the noise figure twice. *([21-03](../../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md))*

**17. Answer: 14.0.** $\Gamma = (75 - 50)/(75 + 50) = 0.2$ and RL $= -20\log_{10}0.2$. The VSWR is 1.5. *([21-01](../../courses/21-rf-and-microwave-engineering/chapters/21-01-s-parameters.md))*

**18. Answer: (B) 1.33 nH.** $Q = \sqrt{50/10 - 1} = 2$; the series reactance is $QR_{low}$ = 20 Ω, so $L = 20/(2\pi \times 2.4\ \text{GHz})$. (A) uses 50 Ω; (C) uses 10 Ω; (D) doubles the reactance. *([21-02](../../courses/21-rf-and-microwave-engineering/chapters/21-02-impedance-matching-networks.md))*

**19. Answer: 87.7.** $\lambda = c/f$ and FSPL $= 20\log_{10}(4\pi d/\lambda)$. Each doubling of distance adds 6.02 dB. *([21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md))*

**20. Answer: (A) 5.0 dBm.** IIP3 $= P_{in} + (P_{fund} - P_{IM3})/2 = -20 + 50/2$. (B) forgets to halve; (C) is the output-referred OIP3; (D) divides by 4. *([21-03](../../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md))*

**21. Answer: 39.3.** An ideal class-B stage has $\eta = (\pi/4)x$ at amplitude fraction $x$, so $\eta = (\pi/4)(0.5)$: half the 78.5% peak. Efficiency falls in proportion to amplitude, which is why back-off hurts. *([21-07](../../courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md))*

## Block 4 · Power electronics and power systems

**22. Answer: (C) 2.16 A.** $D = 1.2/12 = 0.1$ and $\Delta i_L = V(1 - D)/(f_sL) = 1.2 \times 0.9/(5 \times 10^5 \times 10^{-6})$. (A) omits $(1 - D)$; (B) uses $D$ instead of $1 - D$; (D) doubles the ripple. *([22-02](../../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md))*

**23. Answer: 0.583.** $V = V_{in}/(1 - D)$, so $D = 1 - 5/12 = 7/12$. *([22-03](../../courses/22-power-electronics-and-energy-conversion/chapters/22-03-boost-buck-boost-topologies.md))*

**24. Answer: (D) 52.6 W.** $P_{loss} = P_{out}(1 - \eta)/\eta = 1000 \times 0.05/0.95$. (A) takes 5% of the output instead of the input; (B) divides by 1.05; (C) is a factor of ten too small. *([22-01](../../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md))*

**25. Answer: 418.** $I = S/(\sqrt3V_{LL}) = 10^7/(\sqrt3 \times 13{,}800)$, in A. *([22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md))*

**26. Answer: (B) 0.105 pu.** $Z_b = V_{LL}^2/S_b = 138^2/100$ = 190.44 Ω, so $Z_{pu} = 20/190.44$. (A) uses the phase voltage in $Z_b$; (C) inverts the ratio; (D) divides by $\sqrt3$. *([22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md))*

**27. Answer: 0.684.** $P = (V_1V_2/X)\sin\delta = (1/0.5)\sin 20°$. Real power follows the angle; reactive power follows the voltage magnitudes. *([22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md))*

**28. Answer: (A) 3.00%.** $n_s = 120f/P$ = 1800 rpm and $s = (1800 - 1746)/1800$. (B) divides by the rotor speed; (C) uses the 2-pole synchronous speed; (D) is the rotor frequency in hertz ($sf$), not the slip. *([22-11](../../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md))*

**29. Answer: 41.8.** $I_{f,pu} = 1/0.1 = 10$ pu, the fault level is $S_b/Z_{th,pu}$ = 1000 MVA, and $I_f = 1000\ \text{MVA}/(\sqrt3 \times 13.8\ \text{kV})$, in kA. *([22-12](../../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md))*

## Block 5 · Memory and storage

**30. Answer: (C) 110 mV.** $\Delta V = (V_{cell} - V_{pre})C_s/(C_s + C_{BL}) = 0.55 \times 20/100$. (A) divides by $C_{BL}$ alone; (B) uses the full 1.1 V instead of the difference from precharge; (D) ignores charge sharing. *([23-03](../../courses/23-memory-and-storage-technology/chapters/23-03-dram-cells-arrays-refresh.md))*

**31. Answer: 8.97.** $t_{RFC}/t_{REFI} = 350/3900$. High-density DRAMs lose almost a tenth of their time to refresh. *([23-03](../../courses/23-memory-and-storage-technology/chapters/23-03-dram-cells-arrays-refresh.md))*

**32. Answer: (B) 1.23 TB/s.** $B = WR/8 = 1024 \times 9.6\ \text{Gb/s}/8$. (A) forgets the 8 bits per byte; (C) halves it; (D) divides by 64. *([23-05](../../courses/23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md))*

**33. Answer: 100.** Little's law: bytes in flight $= BW \times$ latency $= 10^{12} \times 10^{-7}$ bytes. A processor that cannot keep that many requests outstanding cannot reach the bandwidth. *([23-01](../../courses/23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md))*

**34. Answer: (D) 0.857 V.** Eight levels have seven gaps: $d = W/(2^n - 1) = 6/7$. (A) divides by the number of levels; (B) divides by the number of bits; (C) is the QLC spacing ($6/15$). *([23-06](../../courses/23-memory-and-storage-technology/chapters/23-06-nand-flash-and-3d-nand.md))*

**35. Answer: 0.571.** TBW $= TN_{PE}/A = 2 \times 3000/3$ = 2000 TB, and DWPD $= 2000/(1.92 \times 365 \times 5)$. Write amplification divides the endurance directly. *([23-07](../../courses/23-memory-and-storage-technology/chapters/23-07-ssd-controllers.md))*

**36. Answer: (A) 58.7.** At most one flip means $Ntf_0e^{-\Delta} \le 1$, so $\Delta \ge \ln(Ntf_0) = \ln(10^8 \times 3.156 \times 10^8\ \text{s} \times 10^9\ \text{s}^{-1})$. (B) uses $\log_{10}$; (C) keeps only the bit count; (D) ignores the bit count, which gives the familiar "about 40" for a single bit. *([23-08](../../courses/23-memory-and-storage-technology/chapters/23-08-emerging-memories.md))*

## Block 6 · High-speed I/O

**37. Answer: 28.0.** PAM4 carries 2 bits per symbol, so 56 GBd, and the Nyquist frequency is half the symbol rate. *([24-01](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md))*

**38. Answer: (C) 0.0811.** $\Gamma = (Z_L - Z_0)/(Z_L + Z_0) = 15/185$, a return loss of about 22 dB. (A) divides by 100; (B) divides by 85; (D) halves Γ. *([24-01](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md))*

**39. Answer: 10.0.** $TJ = 2Q^{-1}(10^{-12})RJ + DJ = 2 \times 7.03 \times 0.5 + 3$, in ps. Random jitter counts about 14 times its rms value at this BER. *([24-02](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-02-eye-diagrams-jitter-ber.md))*

**40. Answer: (B) 30.0 s.** $N = -\ln(0.05)/10^{-12} \approx 3.0 \times 10^{12}$ bits, which takes 30 s at 100 Gb/s. (A) uses $1/\text{BER}$ bits (63% confidence); (C) and (D) are off by a factor of ten. *([24-02](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-02-eye-diagrams-jitter-ber.md))*

**41. Answer: 0.237.** $2.3 \times 28 \times 0.002 \times \sqrt{3.4}$, in dB/in. Dielectric loss grows linearly with frequency, so it dominates at these rates. *([24-01](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md))*

**42. Answer: (D) 20.0 pJ/bit.** $16\ \text{W}/(800 \times 10^9\ \text{b/s})$. (A) divides by the rate in bytes per second; (B) inverts the ratio; (C) slips a decimal. *([24-09](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-09-lpo-and-cpo.md))*

**43. Answer: 63.0.** $32 \times 16 \times (128/130)/8$, in GB/s per direction. PCI-SIG's headline figure counts both directions. *([24-05](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-05-pcie-cxl-ethernet.md))*

## Block 7 · Fabrication, packaging, test and reliability

**44. Answer: (A) 12.3 nm.** $0.30 \times 13.5/0.33$. (B) omits $k_1$; (C) halves the result; (D) is $\lambda/(2\text{NA})$, the off-axis minimum pitch rather than this half-pitch. *([25-02](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-02-lithography.md))*

**45. Answer: 67.9.** $\pi \times 300^2/(4 \times 200) - \pi \times 300/\sqrt{400}$, rounded down, gives 306 dies; $AD_0 = 2\ \text{cm}^2 \times 0.1\ \text{cm}^{-2} = 0.2$, so $Y = e^{-0.2}$; the cost is $17{,}000/(306\,Y)$ dollars. *([25-04](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md))*

**46. Answer: (C) 77.7.** $AF = \exp[(0.7/8.617 \times 10^{-5})(1/328.15 - 1/398.15)]$. (A) is the exponent itself; (B) is the ratio of Celsius temperatures; (D) uses 0.6 eV. *([25-09](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md))*

**47. Answer: 46.1.** $4.605/(2 \times 1000 \times 1000\ \text{h} \times 50) \times 10^9$ FIT. Zero failures still give a nonzero bound, set by the device-hours. *([25-09](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md))*

**48. Answer: (B) 89.0 °C.** $T_J = 35 + 300 \times (0.05 + 0.03 + 0.10)$. (A) is the rise without the ambient; (C) leaves out the heat sink; (D) leaves out the interface material. *([25-08](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-08-thermal-engineering.md))*

**49. Answer: 2.49e3.** Bad dies that pass are $(1 - Y)(1 - c) = 0.2 \times 0.01$ of all dies; good dies all pass; so the escape fraction among passing dies is $0.002/(0.8 + 0.002)$. *([25-07](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md))*

**50. Answer: (D) 98.5%.** The dangerous rate is 150 FIT, 2% of it is residual (3 FIT), and SPFM $= 1 - 3/200$. (A) is the diagnostic coverage; (B) is the safe fraction; (C) is the ASIL D target, which this element misses. *([25-10](../../courses/25-fabrication-packaging-test-and-reliability/chapters/25-10-qualification-and-functional-safety.md))*

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| T6.01 | dynamic power | 0.384 | W |
| T6.02 | minimum path delay | 14.0 | τ |
| T6.03 | driver-plus-wire delay | 186 | ps |
| T6.04 | maximum clock frequency | 2.13 | GHz |
| T6.05 | defect level | 4.45e3 | ppm |
| T6.06 | leakage factor | 4.64 | — |
| T6.07 | synchronizer MTBF | 121 | s |
| T6.08 | weak-inversion gm/ID | 29.8 | V⁻¹ |
| T6.09 | unity-gain frequency | 79.6 | MHz |
| T6.10 | slew rate | 50.0 | V/µs |
| T6.11 | kT/C noise | 45.5 | µV |
| T6.12 | 12-bit SQNR | 74.0 | dB |
| T6.13 | jitter-limited SNR | 84.0 | dB |
| T6.14 | PTAT voltage | 53.8 | mV |
| T6.15 | cascade noise figure | 2.67 | dB |
| T6.16 | sensitivity | -85.0 | dBm |
| T6.17 | return loss | 14.0 | dB |
| T6.18 | series inductor | 1.33 | nH |
| T6.19 | free-space path loss | 87.7 | dB |
| T6.20 | IIP3 | 5.0 | dBm |
| T6.21 | class-B efficiency at half amplitude | 39.3 | % |
| T6.22 | buck ripple | 2.16 | A |
| T6.23 | boost duty cycle | 0.583 | — |
| T6.24 | converter dissipation | 52.6 | W |
| T6.25 | line current | 418 | A |
| T6.26 | per-unit impedance | 0.105 | pu |
| T6.27 | power transfer | 0.684 | pu |
| T6.28 | slip | 3.00 | % |
| T6.29 | fault current | 41.8 | kA |
| T6.30 | bitline signal | 110 | mV |
| T6.31 | refresh overhead | 8.97 | % |
| T6.32 | HBM bandwidth | 1.23 | TB/s |
| T6.33 | bytes in flight | 100 | kB |
| T6.34 | TLC level spacing | 0.857 | V |
| T6.35 | drive writes per day | 0.571 | — |
| T6.36 | MRAM stability factor | 58.7 | — |
| T6.37 | Nyquist frequency | 28.0 | GHz |
| T6.38 | reflection coefficient | 0.0811 | — |
| T6.39 | total jitter | 10.0 | ps |
| T6.40 | zero-error test time | 30.0 | s |
| T6.41 | dielectric loss | 0.237 | dB/in |
| T6.42 | energy per bit | 20.0 | pJ/bit |
| T6.43 | PCIe 5.0 x16 bandwidth | 63.0 | GB/s |
| T6.44 | EUV half-pitch | 12.3 | nm |
| T6.45 | cost per good die | 67.9 | $ |
| T6.46 | Arrhenius acceleration | 77.7 | — |
| T6.47 | 90% FIT bound | 46.1 | FIT |
| T6.48 | junction temperature | 89.0 | °C |
| T6.49 | escapes among passing dies | 2.49e3 | ppm |
| T6.50 | single-point fault metric | 98.5 | % |
| T6.17a | VSWR | 1.5 | — |
| T6.26a | base impedance | 190.44 | Ω |
| T6.33a | bytes in flight | 1.0e5 | bytes |
| T6.35a | terabytes written | 2000 | TB |
| T6.36a | seconds in 10 years | 3.156e8 | s |
| T6.38a | return loss | 22 | dB |
| T6.40a | bits needed | 3.0e12 | bits |
| T6.45a | dies per wafer | 306 | — |
