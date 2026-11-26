# Term 6 Checkpoint · FE-Style Practice Exam

**Covers:** Courses 19–25 (digital VLSI, analog and mixed-signal IC design, RF and microwave, power electronics and power systems, memory and storage, high-speed I/O, and fabrication, packaging, test and reliability). **Questions:** 50 (multiple choice and numeric entry). **Time:** 150 minutes, the FE pace of about 3 minutes per question.
**Materials:** an FE-approved calculator and the *NCEES FE Reference Handbook* only (free PDF from NCEES); no course notes or sheets. Relations the handbook does not contain are given in the conventions below or in the question.
**Scoring:** one point per question. Score each block separately and aim for at least 70% in every block. Write every miss into your error log with its cause, and re-solve it a week later. Solutions with full explanations, each pointing to the chapter to revisit, are in [solutions.md](solutions.md); open them only after you finish.

**Conventions:**

- For numeric entry, give 3 significant figures unless the question says otherwise.
- Constants: $k$ = 1.381 × 10⁻²³ J/K = 8.617 × 10⁻⁵ eV/K; $V_T = kT/q$ = 25.85 mV at 300 K; $kT_0$ = −174 dBm/Hz; $c$ = 2.998 × 10⁸ m/s; temperatures in exponentials are absolute ($T$ = °C + 273.15).
- Digital: logical effort with $\mu$ = 2 and $p_{inv}$ = 1, so an inverter has $g$ = 1, a NAND2 $g$ = 4/3 and a NOR2 $g$ = 5/3, and an $n$-input gate has $p = n$. A lumped RC stage has 50% delay 0.69 $RC$; a distributed RC wire 0.38 $RC$.
- Data converters: a full-scale sine is quantized; the sampling-jitter limit is $\text{SNR} = -20\log_{10}(2\pi f_{in}\sigma_t)$.
- Links: $Q^{-1}(10^{-12})$ = 7.03; a test with zero errors in $N$ bits bounds the BER below $-\ln(1 - CL)/N$ at confidence $CL$.
- Power: three-phase quantities are line-to-line unless stated; per-unit impedance $Z_{pu} = Z/Z_b$ with $Z_b = V_{LL}^2/S_b$.
- Fabrication: dies per wafer $\approx \pi d^2/(4A) - \pi d/\sqrt{2A}$, rounded down; Poisson yield $e^{-AD_0}$.

---

## Block 1 · Digital VLSI (questions 1–7)

**1.** *Numeric entry.* A logic block switches 2 nF of total capacitance with an activity factor of 0.15 at 0.8 V and 2 GHz. Find its dynamic power, in W.

**2.** A path of an inverter, a NAND2 and a NOR2 (no branching) drives a load 12 times its input capacitance. Its minimum delay, in units of τ, is:
(A) 8.96 · (B) 14.0 · (C) 11.9 · (D) 31.7

**3.** *Numeric entry.* A 1 kΩ driver drives a 1 mm wire of 500 Ω and 200 fF total into a 10 fF load. Treating the driver as a lumped stage and the wire as distributed, find the 50% delay, in ps.

**4.** A register-to-register path has $t_{pcq}$ = 60 ps, $t_{pd}$ = 350 ps, $t_{setup}$ = 40 ps, zero skew and 20 ps of clock jitter. Its maximum clock frequency is:
(A) 2.22 GHz · (B) 2.86 GHz · (C) 2.13 GHz · (D) 2.04 GHz

**5.** *Numeric entry.* A product has 80% yield and its test reaches 98% fault coverage. Find its defect level, in ppm, with the Williams–Brown model $DL = 1 - Y^{1 - T}$.

**6.** A process has a subthreshold slope of 90 mV/decade. Lowering a transistor's threshold by 60 mV multiplies its off-state leakage by about:
(A) 4.64 · (B) 31.6 · (C) 2.15 · (D) 1.95

**7.** *Numeric entry.* A synchronizer flip-flop has τ = 20 ps and $T_0$ = 20 ps, and is given 400 ps to resolve. The clock is 2 GHz and the asynchronous data toggle at 100 MHz. Find the MTBF, $e^{t_r/\tau}/(T_0f_{clk}f_{data})$, in seconds.

## Block 2 · Analog and mixed-signal IC design (questions 8–14)

**8.** A MOSFET with slope factor $n$ = 1.3 operates deep in weak inversion at 300 K. Its transconductance efficiency $g_m/I_D$ is about:
(A) 38.7 V⁻¹ · (B) 22.9 V⁻¹ · (C) 10.0 V⁻¹ · (D) 29.8 V⁻¹

**9.** *Numeric entry.* A Miller-compensated two-stage op-amp has an input-pair transconductance of 1 mS and a 2 pF compensation capacitor. Find its unity-gain frequency, in MHz.

**10.** The same op-amp's input pair has a 100 µA tail current. Its slew rate is:
(A) 25.0 V/µs · (B) 50.0 V/µs · (C) 100 V/µs · (D) 314 V/µs

**11.** *Numeric entry.* Find the rms thermal noise sampled onto a 2 pF capacitor at 300 K, in µV.

**12.** The ideal signal-to-quantization-noise ratio of a 12-bit ADC is:
(A) 72.2 dB · (B) 68.0 dB · (C) 74.0 dB · (D) 77.0 dB

**13.** *Numeric entry.* A 100 MHz full-scale sine is sampled with 100 fs rms jitter. Find the jitter-limited SNR, in dB.

**14.** Two bipolar transistors with an emitter-area ratio of 8 carry equal currents at 300 K. The difference of their base-emitter voltages is:
(A) 53.8 mV · (B) 23.3 mV · (C) 207 mV · (D) 26.9 mV

## Block 3 · RF and microwave (questions 15–21)

**15.** *Numeric entry.* A receiver chain has an LNA (noise figure 1.5 dB, gain 15 dB), a mixer (10 dB, conversion gain 8 dB) and an IF amplifier (15 dB). Find the cascade noise figure, in dB.

**16.** A receiver has a 20 MHz bandwidth, a 6 dB noise figure and needs 10 dB SNR. Its sensitivity is:
(A) −95.0 dBm · (B) −158 dBm · (C) −79.0 dBm · (D) −85.0 dBm

**17.** *Numeric entry.* A 75 Ω load terminates a 50 Ω line. Find its return loss, in dB.

**18.** An L-network matches a 50 Ω source to a 10 Ω load at 2.4 GHz with a series inductor on the 10 Ω side and a shunt capacitor on the 50 Ω side. The inductor is:
(A) 3.32 nH · (B) 1.33 nH · (C) 0.663 nH · (D) 2.65 nH

**19.** *Numeric entry.* Find the free-space path loss at 5.8 GHz over 100 m, in dB.

**20.** In a two-tone test with −20 dBm per tone at the input, an amplifier outputs −5 dBm per fundamental and −55 dBm per third-order product. Its input-referred third-order intercept is:
(A) 5.0 dBm · (B) 30.0 dBm · (C) 20.0 dBm · (D) −7.5 dBm

**21.** *Numeric entry.* An ideal class-B amplifier runs at half its maximum output voltage amplitude. Find its drain efficiency, in percent.

## Block 4 · Power electronics and power systems (questions 22–29)

**22.** An ideal buck converter steps 12 V down to 1.2 V at 500 kHz with a 1 µH inductor in continuous conduction. The peak-to-peak inductor ripple is:
(A) 2.40 A · (B) 0.240 A · (C) 2.16 A · (D) 4.32 A

**23.** *Numeric entry.* An ideal boost converter in continuous conduction raises 5 V to 12 V. Find its duty cycle.

**24.** A converter delivers 1 kW at 95% efficiency. It dissipates:
(A) 50.0 W · (B) 47.6 W · (C) 5.26 W · (D) 52.6 W

**25.** *Numeric entry.* A balanced three-phase load draws 10 MVA at 13.8 kV. Find its line current, in A.

**26.** On a 100 MVA, 138 kV base, a line impedance of 20 Ω is:
(A) 0.315 pu · (B) 0.105 pu · (C) 9.52 pu · (D) 0.0606 pu

**27.** *Numeric entry.* Two buses at 1.0 pu are joined by a lossless line of 0.5 pu reactance, with a 20° angle between them. Find the real power transferred, in pu.

**28.** A 4-pole, 60 Hz induction motor runs at 1746 rpm. Its slip is:
(A) 3.00% · (B) 3.09% · (C) 51.5% · (D) 1.80%

**29.** *Numeric entry.* A bus has a Thévenin impedance of 0.1 pu on a 100 MVA, 13.8 kV base, with 1.0 pu pre-fault voltage. Find the three-phase bolted fault current, in kA.

## Block 5 · Memory and storage (questions 30–36)

**30.** A DRAM cell of 20 fF storing 1.1 V shares charge with an 80 fF bitline precharged to 0.55 V. The bitline signal is:
(A) 138 mV · (B) 220 mV · (C) 110 mV · (D) 550 mV

**31.** *Numeric entry.* A DRAM has $t_{RFC}$ = 350 ns and $t_{REFI}$ = 3.9 µs. Find the fraction of time it spends refreshing, in percent.

**32.** An HBM stack has a 1024-bit interface at 9.6 Gb/s per pin. Its peak bandwidth is:
(A) 9.83 TB/s · (B) 1.23 TB/s · (C) 0.614 TB/s · (D) 0.154 TB/s

**33.** *Numeric entry.* To sustain 1 TB/s with 100 ns of memory latency, how many kilobytes (10³ bytes) must be in flight?

**34.** A TLC NAND cell stores 3 bits in a 6 V threshold window with its levels equally spaced from end to end. The spacing between adjacent levels is:
(A) 0.750 V · (B) 2.00 V · (C) 0.400 V · (D) 0.857 V

**35.** *Numeric entry.* An SSD has 2 TB of raw flash rated for 3000 program/erase cycles, a write amplification of 3 and 1.92 TB of user capacity. Find its drive writes per day over a 5-year warranty (365-day years).

**36.** An MRAM array of 10⁸ bits may suffer at most one thermal flip in 10 years, with an attempt frequency of 1 GHz. The thermal stability factor $\Delta = E_b/kT$ must be at least about:
(A) 58.7 · (B) 25.5 · (C) 18.4 · (D) 40.3

## Block 6 · High-speed I/O (questions 37–43)

**37.** *Numeric entry.* Find the Nyquist frequency of a 112 Gb/s PAM4 lane, in GHz.

**38.** An 85 Ω differential trace feeds a 100 Ω differential termination. The reflection coefficient is:
(A) 0.150 · (B) 0.176 · (C) 0.0811 · (D) 0.0405

**39.** *Numeric entry.* A link has 0.5 ps rms random jitter and 3 ps of dual-Dirac deterministic jitter. Find its total jitter at a BER of 10⁻¹², in ps.

**40.** A 100 Gb/s link runs with zero errors. To claim BER < 10⁻¹² at 95% confidence it must run for about:
(A) 10.0 s · (B) 30.0 s · (C) 3.00 s · (D) 300 s

**41.** *Numeric entry.* Using $\alpha_d \approx 2.3f_{GHz}\tan\delta\sqrt{\varepsilon_r}$ dB/in, find the dielectric loss of a laminate with $\varepsilon_r$ = 3.4 and tan δ = 0.002 at 28 GHz, in dB/in.

**42.** An 800 Gb/s optical module draws 16 W. Its energy per bit is:
(A) 160 pJ/bit · (B) 50.0 pJ/bit · (C) 2.00 pJ/bit · (D) 20.0 pJ/bit

**43.** *Numeric entry.* Find the per-direction bandwidth of a PCIe 5.0 ×16 link (32 GT/s per lane, 128b/130b encoding), in GB/s.

## Block 7 · Fabrication, packaging, test and reliability (questions 44–50)

**44.** An EUV scanner (13.5 nm, NA 0.33) prints lines at $k_1$ = 0.30. The half-pitch, $k_1\lambda/\text{NA}$, is:
(A) 12.3 nm · (B) 40.9 nm · (C) 6.14 nm · (D) 20.5 nm

**45.** *Numeric entry.* A 200 mm² die is built on 300 mm wafers costing $17,000 at $D_0$ = 0.1 cm⁻². Find the cost per good die, in dollars.

**46.** A mechanism with $E_a$ = 0.7 eV is stressed at 125 °C for a 55 °C application. The Arrhenius acceleration factor is:
(A) 4.35 · (B) 2.27 · (C) 77.7 · (D) 41.7

**47.** *Numeric entry.* An HTOL test runs 1000 units for 1000 h at an acceleration factor of 50 with no failures. With $\chi^2_{0.90,2}$ = 4.605, find the 90% upper bound on the use failure rate, $\chi^2/(2NtAF)$, in FIT.

**48.** A 300 W chip has 0.05 K/W junction to case, 0.03 K/W through its interface material and 0.10 K/W from heat sink to 35 °C air. Its junction temperature is:
(A) 54.0 °C · (B) 89.0 °C · (C) 59.0 °C · (D) 80.0 °C

**49.** *Numeric entry.* Dies yield 80% and the test catches 99% of bad dies. Find the fraction of passing dies that are bad, in ppm.

**50.** An automotive element has λ = 200 FIT, of which 50 FIT are safe faults; a safety mechanism detects 98% of the dangerous faults. Its single-point fault metric is:
(A) 98.0% · (B) 75.0% · (C) 99.0% · (D) 98.5%
