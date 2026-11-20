# Problems 12-07 · Output Stages and Power Amplifiers

Chapter: [12-07](../chapters/12-07-output-stages.md) · Worked solutions: [12-07 solutions](../solutions/12-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** supplies $\pm V_{CC}$, resistive load $R_L$, sine output of peak $V_{op}$; $V_{CE,sat}$ neglected unless stated; $V_T$ = 25.852 mV; $V_{BE}$ falls 2 mV/°C at constant current.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 12-07.1 [A]

**Class A at half swing.** A class A follower is designed for $V_{op} = V_{CC}$ with $I_Q = V_{CC}/R_L$. What is its efficiency when the output amplitude is half of $V_{CC}$?

### Problem 12-07.2 [A]

**A class B stage.** Find the maximum output power, the supply power at full swing and the efficiency of a class B stage on ±12 V driving 4 Ω.

### Problem 12-07.3 [A]

**Worst-case dissipation.** A class B stage runs from ±20 V into 8 Ω. Find the output amplitude of worst-case dissipation, the total dissipation there and the dissipation per transistor.

### Problem 12-07.4 [B]

**Sizing a class A bias.** A class A follower on ±5 V must drive the full swing into 50 Ω. Find the bias current, the supply power and the maximum load power.

### Problem 12-07.5 [B]

**Class B at a third of full power.** A class B stage delivers one third of its maximum output power. Find its efficiency.

### Problem 12-07.6 [B]

**Crossover inside a loop.** A class B stage with a ±0.7 V dead band sits inside a feedback loop whose op-amp has a gain of 10⁵. What dead band does the input see? Why does crossover distortion still rise at high frequency?

### Problem 12-07.7 [B]

**Class AB currents.** A matched class AB pair idles at 10 mA. Find both transistor currents when the load draws 200 mA, and the output resistance at idle.

### Problem 12-07.8 [B]

**A $V_{BE}$ multiplier.** Design a $V_{BE}$ multiplier for $V_{BB}$ = 1.25 V using a transistor with $V_{BE}$ = 0.6 V and 1 mA in the resistor string. Find $R_2$ (base–emitter), $R_1$ (collector–base) and the temperature coefficient of $V_{BB}$.

### Problem 12-07.9 [B]

**A heat sink.** A transistor dissipates 20 W, with $\theta_{JC}$ = 1.0 °C/W and $\theta_{CS}$ = 0.3 °C/W, at an ambient of 50 °C. Find the largest $\theta_{SA}$ for $T_J \le$ 150 °C.

### Problem 12-07.10 [B]

**Preventing runaway.** A transistor at 200 mA with fixed base voltage has $V_{CE}$ = 20 V and a total θ of 8 °C/W. Find its thermal loop gain, and the smallest emitter resistor that brings the loop gain down to 0.5.

### Problem 12-07.11 [C]

**Class D at full and low power.** A class D amplifier drives 8 Ω in BTL through two switches of 0.1 Ω each, with 1.5 W of switching and gate losses and 1 W of idle loss, both independent of output. Find its efficiency at 50 W and at 1 W.

### Problem 12-07.12 [C]

**Class B with music.** Music has a peak-to-average power ratio of about 10 dB. Model the average as a sine 10 dB below the maximum of a ±15 V, 8 Ω class B stage. Find the maximum power, the average output power, the efficiency at that level and the dissipation.

### Problem 12-07.13 [B]

**Drive current and the Darlington.** A class AB stage must deliver 20 W of sine power into 4 Ω. Its output transistors have β = 50. Find the peak output voltage and current, the peak base current, and the peak drive current if each output device is replaced by a Darlington of two β = 50 transistors. The driver is an op-amp that can source 10 mA cleanly: which version can it drive?

### Problem 12-07.14 [B]

**A current limit.** A ±24 V output stage has 0.25 Ω emitter resistors, and a limiting transistor across each turns on at 0.65 V. Find the current limit and the dissipation in the conducting output device when the output is shorted to ground. Explain what a foldback limit would change, and why the safe operating area, not the heat sink, decides whether the device survives a brief short.

### Problem 12-07.15 [C]

**Estimating crossover distortion.** For a class B stage modelled as a ±0.65 V dead band, estimate the THD at 5 V and 20 V peak with §3.2's square-wave approximation, and compare with the exact values from an FFT, 8.201% and 2.011%. Why is the approximation better at 20 V?

---

## Objective coverage

| Learning objective (chapter 12-07) | Problems |
|---|---|
| 1. Class A and class B efficiency and dissipation | 1, 2, 3, 4, 5, 12 |
| 2. Crossover distortion and class AB bias | 6, 8, 15 |
| 3. Class AB currents and output resistance | 7 |
| 4. Heat sinks, thermal runaway, drive and protection | 9, 10, 13, 14 |
| 5. Class D efficiency | 11 |
