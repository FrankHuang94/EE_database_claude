# Problems 28-05 · Domain Question Banks II: Analog/Mixed-Signal, RF, Power, Packaging, Embedded

Chapter: [28-05](../chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md) · Worked solutions: [28-05 solutions](../solutions/28-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Parameters are assumed unless a source is cited. $k_B = 1.380649 \times 10^{-23}$ J/K and room temperature is 300 K. $\text{ENOB} = (\text{SNDR} - 1.76)/6.02$; $\text{FoM}_W = P/(f_s 2^{\text{ENOB}})$; $\text{FoM}_S = \text{SNDR} + 10\log_{10}(f_s/2P)$. Ideal class-B efficiency is $(\pi/4)\,10^{-\text{BO}/20}$; an ideal symmetric Doherty below half amplitude has twice that. A year is 8,766 hours.

---

## Problems

### Problem 28-05.1 [A]

**Strong, partial or evasive?** Classify each answer and say what would make the weaker ones strong:

- (a) To "what is your ADC's SNDR near Nyquist?": "Our SNR is 72 dB."
- (b) To "what is your PA's average efficiency with the real signal?": "47% average with a 100 MHz NR signal at 7.5 dB PAPR, ACLR −46 dBc after our DPD, whose 120 mW is included; at 85 °C it drops to 44%."
- (c) To "is your power density cased or open-frame?": "It's the highest in the industry."
- (d) To "what is standby current at 85 °C?": "We'll pull that from characterization; at 25 °C it's 0.9 µA typical."

### Problem 28-05.2 [B]

**A pipelined ADC.** A 250 MS/s ADC reports 70 dB SNDR near Nyquist at 150 mW, including its input buffer and references. Find its ENOB, Walden and Schreier figures, the gap to the best published result at 100 MS/s or faster (181.5 dB [R-336]), the 8kT·SNR power floor, and the ratio of its power to that floor.

### Problem 28-05.3 [B]

**Clock budgets.** (a) What clock jitter alone would limit SNR to 70 dB for a 400 MHz input? (b) What is the jitter-limited SNR for a 1 GHz input with a 50 fs clock? (c) And for a 3 GHz input?

### Problem 28-05.4 [B]

**The ceiling.** Find the 8kT·SNR ceiling on the Schreier figure at 300 K and at 85 °C (358.15 K). A paper claims 193 dB at room temperature; by how much does it exceed the 300 K ceiling, and what would you ask?

### Problem 28-05.5 [B]

**Back-off.** Find the ideal class-B efficiency at half the peak amplitude and at 10 dB back-off, and the ideal symmetric Doherty efficiency at the same two points. A PA delivers 5 W average at 45% average efficiency; find its DC power and dissipation.

### Problem 28-05.6 [A]

**EVM in dB.** Express 3GPP's 3.5% and 2.5% EVM limits [R-275] in dB, and Wi-Fi 7's −38 dB [R-383] as a percentage. What SNR does each correspond to if noise dominates?

### Problem 28-05.7 [B]

**Two supplies.** Find the volume of a 3 kW supply at 32 W/in³ and of an 8 kW supply at 100 W/in³ [R-423], and the loss of a 3 kW supply at 96% and at 97.5% efficiency.

### Problem 28-05.8 [B]

**Another chain.** Power reaches 1,200 W of processor load through a supply at 97.5%, an intermediate bus converter at 97% and core regulators at 91% (all assumed). Find the chain efficiency, the input power, the total loss and each stage's loss.

### Problem 28-05.9 [B]

**Finer pitch, more stacks.** (a) By how much does density rise from a 9 µm to a 6 µm and to a 4.5 µm hybrid-bond pitch [R-589]? (b) What is the ratio of TSMC's 14,000 signals per mm² for face-to-face bonding to 1,500 for face-to-back stacking [R-589]? (c) Repeat Example 28-05.5(c) with twelve stacks. (d) With the die at 99% and assembly at 98%, what survival per stack would twelve stacks need for a 95% package yield?

### Problem 28-05.10 [A]

**Cooling margin.** A 1,200 W device has 0.05 K/W from junction to coolant, with coolant at 35 °C. Find its junction temperature, and the most power it can dissipate for a 105 °C junction limit.

### Problem 28-05.11 [B]

**Less frequent wake-ups.** In Example 28-05.6, the MCU wakes every 5 s instead of every second (other parameters unchanged, CoreMark figure). Find the average current and battery life at 25 °C and at 85 °C.

### Problem 28-05.12 [C]

**Typical against guaranteed.** A standby current has an upper specification limit of 4 µA. Characterization of 30 parts gives a mean of 1.5 µA and a standard deviation of 0.4 µA (assume normality).

- (a) Find Cpk and the expected parts per million above the limit.
- (b) Repeat if the true σ is 0.8 µA.
- (c) Using the chi-square quantile $\chi^2_{0.05;\,29}$, find the 95% upper bound on σ and the Cpk it implies.

### Problem 28-05.13 [C]

**Three derivations.**

- (a) From $P/f_s = 8k_BT \cdot \text{SNR}$, derive the ceiling on $\text{FoM}_S$ and show it does not depend on $f_s$ or SNR.
- (b) For an ideal class-B stage with a half-sine drain current of peak $I_p$, derive $\eta = (\pi/4)(V_o/V_{DD})$; then show that a carrier amplifier that reaches full voltage swing at half the peak amplitude (the Doherty's low-power region) has twice that efficiency.
- (c) Show that a normally distributed parameter with capability $C_{pk}$ against a one-sided upper limit has a fraction $\Phi(-3C_{pk})$ beyond the limit, and that $\sigma \le s\sqrt{(n-1)/\chi^2_{1-C;\,n-1}}$ with confidence $C$.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Converters against the frontier; jitter budgets | 1, 2, 3, 4, 13 |
| 2. PA efficiency at back-off; EVM | 1, 5, 6, 13 |
| 3. Converter heat, chains and density | 1, 7, 8 |
| 4. Packaging density, yield and thermal; battery life | 9, 10, 11 |
| 5. Typical, guaranteed and Cpk | 1, 12, 13 |
