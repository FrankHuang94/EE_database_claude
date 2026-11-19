# Problems 07-05 · Sinusoidal Steady State, Phasors and Impedance

Chapter: [07-05](../chapters/07-05-sinusoidal-steady-state-and-impedance.md) · Worked solutions: [07-05 solutions](../solutions/07-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** peak-amplitude phasors, cosine reference, angles in degrees; passive sign convention. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 07-05.1 [A]

**Impedance and admittance.** (a) Find the admittance of $Z = 60 + j80$ Ω, and state its conductance and susceptance. (b) Find the impedance of $Y = 2 - j3$ mS. Is each network inductive or capacitive?

### Problem 07-05.2 [A]

**A series RLC across frequency.** A series RLC has $R$ = 50 Ω, $L$ = 10 mH and $C$ = 1 µF. Find $Z$ in polar form at 1 kHz, at the frequency where it is purely resistive, and at 5 kHz. Is the circuit inductive or capacitive at each?

### Problem 07-05.3 [A]

**An inductor's Q and its parallel equivalent.** A 100 µH inductor has 0.5 Ω of series resistance at 1 MHz. Find its reactance and $Q$, and the parallel equivalent $R_p$ and $L_p$ at that frequency.

### Problem 07-05.4 [B]

**A film capacitor's loss.** A 1 µF film capacitor has a dissipation factor of 0.001 at 1 kHz. Find its equivalent series resistance, and its parallel-equivalent resistance and capacitance at 1 kHz.

### Problem 07-05.5 [B]

**Mesh analysis at 50 Hz.** Mesh 1 contains a source $\mathbf{V}_1 = 100\angle0°$ V, $R_1$ = 10 Ω and $L$ = 0.1 H, and shares a 100 µF capacitor with mesh 2. Mesh 2 contains the capacitor, $R_2$ = 20 Ω and a source $\mathbf{V}_2 = 50\angle30°$ V that pushes current counterclockwise. Take both mesh currents clockwise. Find $\mathbf{I}_1$, $\mathbf{I}_2$ and the capacitor current $\mathbf{I}_1 - \mathbf{I}_2$.

### Problem 07-05.6 [B]

**A DC and an AC source together.** A source $v_s(t) = 5 + 2\cos(2\pi\cdot1000\,t)$ V drives $R_1$ = 1 kΩ into a node that has $R_2$ = 1 kΩ and $C$ = 100 nF to ground. Find the node voltage $v(t)$.

### Problem 07-05.7 [B]

**A Norton equivalent at 1 MHz.** A 1 V (peak) source at 1 MHz feeds a 10 µH inductor in series to an output terminal, which has a 100 Ω resistor to ground. Find the Norton equivalent at the output: the short-circuit current and the Norton impedance.

### Problem 07-05.8 [B]

**Voltage magnification at resonance.** A 1 V source drives a series RLC with $R$ = 10 Ω, $L$ = 10 mH and $C$ = 1 µF at its resonant frequency. Find the frequency, the current, the voltage across the inductor and the capacitor, and $Q$. Sketch the phasor diagram.

### Problem 07-05.9 [B]

**A heavily loaded line.** A load draws 10 A at 30° lagging from a $100\angle0°$ V load voltage, through a line of $1 + j2$ Ω. (a) Find the source voltage exactly, and the drop. (b) How good is the approximation of chapter §3.5 here, and why? (c) A capacitor at the load cancels the load's reactive current, so that the line current becomes the in-phase part alone. Find the new source voltage and drop.

### Problem 07-05.10 [B]

**The Wien bridge as a frequency meter.** A Wien bridge has one arm a series RC and the adjacent arm a parallel RC, both with $R$ = 10 kΩ and $C$ = 10 nF, and two resistive arms $R_3$ and $R_4$. Show that it balances at only one frequency, find that frequency, and find the ratio $R_3/R_4$ required at balance.

### Problem 07-05.11 [B]

**A capacitance comparison bridge.** Arm 1 is an unknown capacitor modeled as $C_x$ in series with $R_x$; arm 2 is a standard 100 nF capacitor in series with an adjustable resistor $R_s$; arms 3 and 4 are resistors. Balance $Z_1Z_4 = Z_2Z_3$ is reached at 1 kHz with $R_3$ = 1 kΩ, $R_4$ = 2.2 kΩ and $R_s$ = 4.4 Ω. Find $C_x$, $R_x$ and the unknown's dissipation factor at 1 kHz.

### Problem 07-05.12 [C]

**The practical differentiator in phasors.** Problem 07-02.19's differentiator ($R_s$ = 1 kΩ in series with $C$ = 100 nF at the input, $R_f$ = 10 kΩ in feedback) has gain $-Z_f/Z_i$. (a) Find $H(j\omega)$ in magnitude and phase at 100 Hz, at the corner $1/(2\pi R_sC)$, and at 100 kHz. (b) Compare each magnitude with the ideal differentiator's $\omega R_fC$. (c) Relate the result to 07-02's time-domain conclusion that the series resistor caps the gain.

### Problem 07-05.13 [C]

**A tissue impedance model.** A simplified model of biological tissue puts an extracellular resistance $R_e$ = 500 Ω in parallel with an intracellular path, a resistance $R_i$ = 300 Ω in series with a cell-membrane capacitance $C_m$ = 5 nF. (a) Find $Z$ at 5 kHz, 50 kHz and 1 MHz. (b) What are its limits at very low and very high frequency, and why? (c) Explain why measuring at several frequencies can separate extracellular from intracellular fluid, while a single frequency cannot.

---

## Objective coverage

| Learning objective (chapter 07-05) | Problems |
|---|---|
| 1. Impedance and admittance; R, X, G, B, Q, D | 1, 2, 3, 4, 13 |
| 2. Series–parallel equivalents; LCR-meter modes | 3, 4, 11 |
| 3. Phasor nodal, mesh, Thévenin/Norton, superposition | 5, 6, 7 |
| 4. Phasor diagrams; voltage drop | 8, 9 |
| 5. AC bridges and op-amp circuits | 10, 11, 12 |
| 6. When phasors apply; impedance in practice | 6, 12, 13 |
