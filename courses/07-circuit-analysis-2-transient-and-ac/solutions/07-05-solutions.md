# Solutions 07-05 · Sinusoidal Steady State, Phasors and Impedance

Problems: [07-05 problems](../problems/07-05-problems.md) · Chapter: [07-05](../chapters/07-05-sinusoidal-steady-state-and-impedance.md). Every number below is recomputed by [verify_07_05.py](../verify/verify_07_05.py), which solves the circuits' complex equations independently and checks steady states against time-domain simulation; values marked † are also confirmed by an ngspice AC analysis in [labs/07-05-lab](../labs/07-05-lab/README.md).

---

## Solutions

### Solution 07-05.1

(a) $Y = 1/(60 + j80) = (60 - j80)/(60^2 + 80^2) = (60 - j80)/10\,000$ S $= 6 - j8$ mS: $G$ = **6.000 mS**, $B$ = **−8.000 mS**. Inductive ($X = +80$ Ω, so $B < 0$).

(b) $Z = 1/(0.002 - j0.003) = (0.002 + j0.003)/(13\times10^{-6})$ Ω $= $ **153.8 + j230.8 Ω**. Also inductive ($X > 0$; the negative susceptance said so already).

### Solution 07-05.2

$Z = R + j\big(\omega L - 1/(\omega C)\big)$.

- 1 kHz: $X = 62.83 - 159.15 = -96.32$ Ω, so $Z = $ **108.5 Ω ∠ −62.57°**: capacitive.
- Purely resistive where $\omega L = 1/(\omega C)$: $f_0 = 1/(2\pi\sqrt{LC}) = $ **1.592 kHz**, where $Z$ = 50 Ω ∠ 0°.
- 5 kHz: $X = 314.16 - 31.83 = 282.33$ Ω, so $Z = $ **286.7 Ω ∠ 79.96°**: inductive.

Below resonance the capacitor's reactance dominates, above it the inductor's.

### Solution 07-05.3

$X = \omega L = 2\pi\times10^6\times10^{-4} = $ **628.3 Ω** and $Q = X/R_s = $ **1257**. Then $R_p = R_s(1 + Q^2) = 0.5\times(1 + 1257^2) = $ **789.6 kΩ** and $X_p = X(1 + 1/Q^2) \approx X$, so $L_p$ = **100.0 µH**. A 0.5 Ω series loss is equivalent to almost 0.8 MΩ in parallel: for a high-Q part, a small series resistance is a very large parallel one.

### Solution 07-05.4

$D = R/\lvert X\rvert$ with $\lvert X\rvert = 1/(\omega C) = 159.15$ Ω at 1 kHz, so $R_{ESR} = D/(\omega C) = $ **0.1592 Ω**. With $Q = 1/D = 1000$: $R_p = R_s(1 + Q^2) = $ **159.2 kΩ** and $C_p = C/(1 + D^2) = $ **1.000 µF** (smaller by one part in a million). With $D$ this small, series and parallel capacitance agree; only the resistances describe the loss differently.

### Solution 07-05.5

At 50 Hz, $Z_L = j31.42$ Ω and $Z_C = -j31.83$ Ω. KVL in each mesh (mesh 2's source opposes $\mathbf{I}_2$):

$$
(R_1 + j\omega L + Z_C)\,\mathbf{I}_1 - Z_C\,\mathbf{I}_2 = \mathbf{V}_1, \qquad -Z_C\,\mathbf{I}_1 + (Z_C + R_2)\,\mathbf{I}_2 = -\mathbf{V}_2 ,
$$

that is

$$
\begin{pmatrix}10 - j0.4128 & j31.83\\ j31.83 & 20 - j31.83\end{pmatrix}\begin{pmatrix}\mathbf{I}_1\\ \mathbf{I}_2\end{pmatrix} = \begin{pmatrix}100\\ -43.30 - j25.00\end{pmatrix} .
$$

Solving: $\mathbf{I}_1 = $ **1.745 A ∠ −41.06°**, $\mathbf{I}_2 = $ **2.769 A ∠ −82.17°**, and the capacitor current $\mathbf{I}_1 - \mathbf{I}_2 = $ **1.853 A ∠ 59.57°**. Note that $L$ and $C$ almost cancel in mesh 1 at 50 Hz ($j31.42 - j31.83$), which is why mesh 1's own impedance is nearly resistive.

### Solution 07-05.6

Superposition, one frequency at a time.

- **DC** (capacitor open): $V_{DC} = 5\times R_2/(R_1 + R_2) = $ **2.500 V**.
- **1 kHz:** the shunt is $Z_p = R_2\parallel\frac{1}{j\omega C} = 1/(10^{-3} + j6.283\times10^{-4})$ Ω $= 717.0 - j450.5$ Ω, and the divider gives $\mathbf{V}_{ac} = 2\,Z_p/(R_1 + Z_p) = $ **0.9540 V ∠ −17.44°**.

In time: $v(t) = 2.5 + 0.954\cos(2\pi\cdot1000\,t - 17.44°)$ V. The two parts cannot be combined into one phasor: one is a constant and the other rotates.

### Solution 07-05.7

Short the output: all the source current flows through the inductor, $\mathbf{I}_{sc} = 1/(j\omega L) = 1/(j62.83)$ A $= $ **15.92 mA ∠ −90°**. With the source shorted, the output sees $j\omega L$ in parallel with 100 Ω: $Z_N = j62.83\times100/(100 + j62.83) = $ **28.30 + j45.05 Ω** ($53.20\angle57.86°$ Ω). The Norton equivalent is $\mathbf{I}_{sc}$ in parallel with $Z_N$, valid at 1 MHz.

### Solution 07-05.8

$f_0 = 1/(2\pi\sqrt{10^{-2}\times10^{-6}}) = $ **1.592 kHz**. At resonance $j\omega L$ and $1/(j\omega C)$ cancel, so $\mathbf{I} = 1/10 = $ **0.1000 A** ∠ 0°. The inductor's voltage is $j\omega_0L\,\mathbf{I} = j100\times0.1 = $ **10.00 V** ∠ 90°, and the capacitor's **10.00 V** ∠ −90°: ten times the source, cancelling each other. $Q = \omega_0L/R = $ **10.00**, the voltage magnification (02-04). Phasor diagram: $\mathbf{V}_R$ along $\mathbf{I}$ and equal to the source; $\mathbf{V}_L$ straight up and $\mathbf{V}_C$ straight down, equal and opposite.

### Solution 07-05.9

(a) $\mathbf{I} = 10\angle{-30°} = 8.660 - j5.000$ A. $\mathbf{V}_S = 100 + (8.660 - j5)(1 + j2) = 100 + 18.66 + j12.32$, so $\lvert\mathbf{V}_S\rvert = $ **119.3 V** (at 5.93°) and the drop is **19.30 V**.

(b) The approximation gives $10(1\times\cos30° + 2\times\sin30°) = $ **18.66 V**, 0.64 V low. The rule neglects the quadrature component (here 12.3 V, far from small compared with 100 V), which adds to the magnitude in second order. It is good only when the line drop is a few percent of the voltage.

(c) The compensated line current is the in-phase part, **8.660 A** ∠ 0° (the capacitor supplies the 5 A reactive part locally). $\mathbf{V}_S = 100 + 8.66(1 + j2) = 108.66 + j17.32$, so $\lvert\mathbf{V}_S\rvert = 110.03$ V and the drop falls to **10.03 V**. Cancelling the reactive current roughly halved the drop: the line's large reactance now carries only in-phase current. This is the voltage-support side of power-factor correction (07-06).

### Solution 07-05.10

The balance condition $Z_1Z_4 = Z_2Z_3$ with $Z_1$ the series RC and $Z_2$ the parallel RC is $Z_1/Z_2 = R_3/R_4$. Compute

$$
\frac{Z_1}{Z_2} = \Big(R + \frac{1}{j\omega C}\Big)\Big(\frac{1}{R} + j\omega C\Big) = 2 + j\Big(\omega RC - \frac{1}{\omega RC}\Big) .
$$

$R_3/R_4$ is real, so balance needs the imaginary part to vanish: $\omega = 1/(RC)$, a single frequency, $f = 1/(2\pi\times10^4\times10^{-8}) = $ **1.592 kHz**. Then $Z_1/Z_2 = 2$, so $R_3/R_4 = $ **2**. Tuning $R$ (or $C$) in both arms together until the detector nulls measures an unknown frequency.

### Solution 07-05.11

Balance $Z_1Z_4 = Z_2Z_3$ gives $\big(R_x + \frac{1}{j\omega C_x}\big)R_4 = \big(R_s + \frac{1}{j\omega C_s}\big)R_3$. Real parts: $R_x = R_sR_3/R_4 = 4.4\times1000/2200 = $ **2.000 Ω**. Imaginary parts: $R_4/C_x = R_3/C_s$, so $C_x = C_sR_4/R_3 = 100\times2.2 = $ **220.0 nF**. Its dissipation factor at 1 kHz is $\omega C_xR_x = 2\pi\times1000\times220\times10^{-9}\times2 = $ **0.002765**. Like the Maxwell bridge, ω cancels from both conditions, so this bridge balances at any frequency.

### Solution 07-05.12

(a) $H = -R_f/\big(R_s + 1/(j\omega C)\big)$. Its corner is $f_c = 1/(2\pi R_sC) = 1.592$ kHz.

- 100 Hz: $\lvert H\rvert = $ **0.6271**, at −93.60°.
- 1.592 kHz: $H = -10/(1 - j) $, so $\lvert H\rvert = 10/\sqrt2 = $ **7.071**, at −135.0°.
- 100 kHz: $\lvert H\rvert = $ **9.999**, at −179.09°.

(b) The ideal differentiator's gain $\omega R_fC$ is 0.6283, 10.00 and **628.3** at the three frequencies. At 100 Hz the practical circuit is within 0.2% of ideal; at the corner it is 3 dB below; at 100 kHz it is capped at $R_f/R_s = 10$, 63 times below the ideal.

(c) It is the same fact seen in frequency: 07-02 found that the series resistor turned an impulse into a finite spike of height $(R_f/R_s)V$ and limited the response to fast changes to $R_f/R_s$. Fast changes are high frequencies, and the phasor gain tops out at exactly $R_f/R_s$.

### Solution 07-05.13

(a) $Z = R_e\parallel\big(R_i + \frac{1}{j\omega C_m}\big)$:

- 5 kHz: $Z = 495.1 - j38.66$ Ω, $\lvert Z\rvert = $ **496.6 Ω** at −4.46°.
- 50 kHz: $Z = 308.7 - j152.3$ Ω, $\lvert Z\rvert = $ **344.2 Ω** at **−26.26°**.
- 1 MHz: $Z = 188.0 - j12.41$ Ω, $\lvert Z\rvert = $ **188.4 Ω** at −3.78°.

(b) At low frequency the membrane capacitance blocks the intracellular path, so $Z \to R_e$ = **500 Ω**. At high frequency it shorts, and $Z \to R_e\parallel R_i = $ **187.5 Ω**. In between, $Z = R_e\,\dfrac{1 + j\omega R_iC_m}{1 + j\omega(R_e + R_i)C_m}$ has a pole at $1/(2\pi(R_e + R_i)C_m) = $ **39.79 kHz** and a zero at $1/(2\pi R_iC_m) = $ **106.1 kHz**, and the phase is most negative at their geometric mean, **64.97 kHz**.

(c) The two limits measure two different things: the low-frequency value is the extracellular resistance alone, and the high-frequency value adds the intracellular path. One frequency gives one complex number, a blend of both paths with weights that depend on the unknown $C_m$; measurements at several frequencies (or the full curve) let a fit separate $R_e$, $R_i$ and $C_m$, and with them extracellular and total body water. This is the principle of multi-frequency bioimpedance analysis (§9).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 07-05.1a | conductance | 6.000 | mS |
| 07-05.1b | susceptance | −8.000 | mS |
| 07-05.1c | resistance of Y | 153.8 | Ω |
| 07-05.1d | reactance of Y | 230.8 | Ω |
| 07-05.2a | $\lvert Z\rvert$ at 1 kHz | 108.5 | Ω |
| 07-05.2b | angle at 1 kHz | −62.57 | ° |
| 07-05.2c | resonant frequency | 1.592 | kHz |
| 07-05.2d | $\lvert Z\rvert$ at 5 kHz | 286.7 | Ω |
| 07-05.2e | angle at 5 kHz | 79.96 | ° |
| 07-05.3a | reactance | 628.3 | Ω |
| 07-05.3b | Q | 1257 | — |
| 07-05.3c | $R_p$ | 789.6 | kΩ |
| 07-05.3d | $L_p$ | 100.0 | µH |
| 07-05.4a | ESR | 0.1592 | Ω |
| 07-05.4b | $R_p$ | 159.2 | kΩ |
| 07-05.4c | $C_p$ | 1.000 | µF |
| 07-05.5a | $\lvert\mathbf{I}_1\rvert$ | 1.745 | A |
| 07-05.5b | angle of $\mathbf{I}_1$ | −41.06 | ° |
| 07-05.5c | $\lvert\mathbf{I}_2\rvert$ | 2.769 | A |
| 07-05.5d | angle of $\mathbf{I}_2$ | −82.17 | ° |
| 07-05.5e | $\lvert\mathbf{I}_C\rvert$ | 1.853 | A |
| 07-05.5f | angle of $\mathbf{I}_C$ | 59.57 | ° |
| 07-05.6a | DC part | 2.500 | V |
| 07-05.6b | AC amplitude | 0.9540 | V |
| 07-05.6c | AC phase | −17.44 | ° |
| 07-05.7a | $\lvert\mathbf{I}_{sc}\rvert$ | 15.92 | mA |
| 07-05.7b | $Z_N$ real part | 28.30 | Ω |
| 07-05.7c | $Z_N$ imaginary part | 45.05 | Ω |
| 07-05.8a | resonant frequency | 1.592 | kHz |
| 07-05.8b | current | 0.1000 | A |
| 07-05.8c | inductor (and capacitor) voltage | 10.00 | V |
| 07-05.8d | Q | 10.00 | — |
| 07-05.9a | $\lvert\mathbf{V}_S\rvert$ | 119.3 | V |
| 07-05.9b | drop | 19.30 | V |
| 07-05.9c | approximate drop | 18.66 | V |
| 07-05.9d | compensated line current | 8.660 | A |
| 07-05.9e | compensated drop | 10.03 | V |
| 07-05.10a | balance frequency | 1.592 | kHz |
| 07-05.10b | $R_3/R_4$ | 2 | — |
| 07-05.11a | $R_x$ | 2.000 | Ω |
| 07-05.11b | $C_x$ | 220.0 | nF |
| 07-05.11c | D at 1 kHz | 0.002765 | — |
| 07-05.12a | gain at 100 Hz | 0.6271 | — |
| 07-05.12b | gain at the corner | 7.071 | — |
| 07-05.12c | gain at 100 kHz | 9.999 | — |
| 07-05.12d | ideal gain at 100 kHz | 628.3 | — |
| 07-05.13a | $\lvert Z\rvert$ at 5 kHz | 496.6 | Ω |
| 07-05.13b | $\lvert Z\rvert$ at 50 kHz | 344.2 | Ω |
| 07-05.13c | angle at 50 kHz | −26.26 | ° |
| 07-05.13d | $\lvert Z\rvert$ at 1 MHz | 188.4 | Ω |
| 07-05.13e | low-frequency limit | 500 | Ω |
| 07-05.13f | high-frequency limit | 187.5 | Ω |
| 07-05.13g | pole frequency | 39.79 | kHz |
| 07-05.13h | zero frequency | 106.1 | kHz |
| 07-05.13i | frequency of the most negative phase | 64.97 | kHz |
