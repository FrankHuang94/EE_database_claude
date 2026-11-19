# Problems 07-10 · Two-Port Networks

Chapter: [07-10](../chapters/07-10-two-port-networks.md) · Worked solutions: [07-10 solutions](../solutions/07-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** port currents flow into the upper terminal of each port; ABCD uses $-\mathbf{I}_2$; S-parameters use a 50 Ω reference unless stated. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 07-10.1 [A]

**Elements that lack parameter sets.** (a) Write the ABCD matrix of a 50 Ω series resistor and of a 0.01 S shunt conductance. (b) Explain why the first has no z-parameters and the second no y-parameters. (c) Find the ABCD matrix of the series resistor followed by the shunt conductance, and its determinant.

### Problem 07-10.2 [A]

**A Π network.** A Π network has a 100 Ω shunt resistor at port 1, a 200 Ω shunt resistor at port 2 and a 50 Ω series resistor between the ports. Find its y-parameters and, by inversion, its z-parameters.

### Problem 07-10.3 [A]

**Reciprocal or not? Symmetric or not?** Classify each: (a) $\mathbf{z} = \begin{bmatrix}5 & 3\\3 & 5\end{bmatrix}$ Ω; (b) $\mathbf{y} = \begin{bmatrix}2 & -1\\-1 & 3\end{bmatrix}$ mS; (c) $\mathbf{h}$ with $h_{11}$ = 50 Ω, $h_{12}$ = 0.5, $h_{21}$ = −0.5, $h_{22}$ = 0.01 S; (d) ABCD $\begin{bmatrix}2 & 10\ \Omega\\0.1\ \text{S} & 1\end{bmatrix}$; (e) ABCD $\begin{bmatrix}1 & 5\ \Omega\\0.2\ \text{S} & 3\end{bmatrix}$.

### Problem 07-10.4 [B]

**h from z.** Convert Example 07-10.1's z-parameters to h-parameters, and check the reciprocity condition in h form.

### Problem 07-10.5 [B]

**A transistor with internal feedback.** A transistor's h-parameters are $h_{11}$ = 2 kΩ, $h_{12} = 2\times10^{-4}$, $h_{21}$ = 150 and $h_{22}$ = 20 µS. (a) Convert them to y- and z-parameters. (b) With a 10 kΩ load, find the voltage gain and the input impedance. (c) What would the input impedance be if $h_{12}$ were zero?

### Problem 07-10.6 [B]

**Three sections, unbuffered.** Three identical RC sections ($R$ = 1 kΩ series, $C$ = 100 nF shunt) are cascaded. At $f = 1/(2\pi RC)$, find the open-circuit voltage gain (magnitude, dB and phase) and compare it with three buffered sections.

### Problem 07-10.7 [B]

**An L-section match.** A 10 Ω load must look like 50 Ω at 100 MHz. Use a series inductor next to the load and a shunt capacitor across the 50 Ω side. (a) Find $L$ and $C$ (the network's $Q = \sqrt{50/10 - 1}$; the series reactance is $QR_L$ and the shunt reactance $50/Q$). (b) Verify with ABCD matrices that $Z_{in}$ = 50 Ω at 100 MHz. (c) Find the input reflection coefficient magnitude and the return loss at 110 MHz.

### Problem 07-10.8 [B]

**A twin-T notch by adding y-parameters.** Two T networks are connected in parallel (inputs together, outputs together, common ground). T1 has series arms $R$, $R$ and shunt $2C$; T2 has series arms $C$, $C$ (impedance $1/(j\omega C)$ each) and shunt $R/2$, with $R$ = 10 kΩ and $C$ = 10 nF. (a) Why may the y-parameters be added? (b) Find the open-circuit voltage gain $-y_{21}/y_{22}$ of the combination at $f_0 = 1/(2\pi RC)$, at $f_0/2$, at $2f_0$ and at $0.9f_0$.

### Problem 07-10.9 [B]

**A matched attenuator.** A symmetric Π attenuator for a 50 Ω system has shunt resistors $R_{sh} = Z_0(K + 1)/(K - 1)$ and series resistor $R_{se} = Z_0(K^2 - 1)/(2K)$, where $K$ is the voltage attenuation ratio. (a) Find the resistors for 6 dB. (b) Build its ABCD matrix and confirm that it is reciprocal and symmetric. (c) Convert to S-parameters and confirm $S_{11}$ = 0 and $\lvert S_{21}\rvert$ = −6 dB. What fraction of the incident power does it absorb?

### Problem 07-10.10 [B]

**The Miller effect from y-parameters.** A transistor's hybrid-π model has $r_\pi$ = 2.5 kΩ, $g_m$ = 40 mS, $r_o$ = 50 kΩ, $C_\pi$ = 10 pF and a base-to-collector capacitance $C_\mu$ = 1 pF; it drives a 5 kΩ load at 1 MHz. (a) Write its y-parameters ($y_{11} = 1/r_\pi + j\omega(C_\pi + C_\mu)$, $y_{12} = -j\omega C_\mu$, $y_{21} = g_m - j\omega C_\mu$, $y_{22} = 1/r_o + j\omega C_\mu$). Is it reciprocal? (b) Find the input admittance $Y_{in} = y_{11} - y_{12}y_{21}/(y_{22} + Y_L)$ and the equivalent input capacitance $\operatorname{Im}Y_{in}/\omega$. (c) Compare with the Miller estimate $C_\pi + C_\mu(1 + g_mR_L')$, where $R_L' = r_o\parallel R_L$.

### Problem 07-10.11 [C]

**S-parameters at 5 GHz.** In a 50 Ω system at 5 GHz, find $S_{11}$, $S_{21}$, the insertion loss and the return loss of (a) a 1 pF shunt capacitor, (b) a 10 Ω series resistor, (c) the resistor followed by the capacitor. For (c), find $\lvert S_{22}\rvert$ and explain why it differs from $\lvert S_{11}\rvert$, and find the fraction of incident power absorbed.

### Problem 07-10.12 [C]

**Reflection from a mismatched load.** A load $Z_L$ = 25 + j25 Ω terminates a 50 Ω system. Find the reflection coefficient (magnitude and angle), the return loss, the mismatch loss $-10\lg(1 - \lvert\Gamma\rvert^2)$ and the voltage standing-wave ratio $(1 + \lvert\Gamma\rvert)/(1 - \lvert\Gamma\rvert)$.

---

## Objective coverage

| Learning objective (chapter 07-10) | Problems |
|---|---|
| 1. Parameter sets and their tests | 1, 2, 3 |
| 2. Parameters of circuits and transistor models | 2, 5, 10 |
| 3. Conversions; sets that do not exist | 1, 4, 5 |
| 4. Interconnections and their validity | 6, 8 |
| 5. Terminated two-ports; reciprocity and symmetry | 3, 5, 7, 9, 10 |
| 6. S-parameters, insertion and return loss | 9, 11, 12 |
