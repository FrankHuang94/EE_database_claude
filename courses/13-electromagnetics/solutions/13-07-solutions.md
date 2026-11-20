# Solutions 13-07 · Transmission Lines: Time Domain

Problems: [13-07 problems](../problems/13-07-problems.md) · Chapter: [13-07](../chapters/13-07-transmission-lines-time-domain.md). Every number below is recomputed by [verify_13_07.py](../verify/verify_13_07.py), which solves the telegrapher's equations by finite differences with the sources, loads and lumped elements as boundary conditions, independently of the bounce-diagram sums used here.

---

## Solutions

### Solution 13-07.1

$Z_0 = \sqrt{333.6\ \text{nH}/133.4\ \text{pF}}$ = **50.01** Ω; $v = 1/\sqrt{L'C'}$ = **1.499 × 10⁸** m/s; delay **6.671** ps/mm. Since $L'C' = \varepsilon_r/c^2$, $\varepsilon_r = c^2L'C'$ = **4.000**.

### Solution 13-07.2

$\Gamma_L = (R_L - 50)/(R_L + 50)$: short **−1**, open **+1**, 25 Ω **−0.3333**, 75 Ω **0.2**, 100 Ω **0.3333**.

### Solution 13-07.3

$v^+ = 3.3 \times 50/(25 + 50)$ = **2.2** V. The line, not the receiver, sets this first step.

### Solution 13-07.4

$v^+ = 1 \times 50/150$ = **0.3333** V, $\Gamma_S = (100 - 50)/150$ = **0.3333**, $\Gamma_L = (25 - 50)/75$ = **−0.3333**. At the load each arrival adds $v^+(1 + \Gamma_L)(\Gamma_S\Gamma_L)^k$:

- first arrival ($T_D$): 0.3333 × 0.6667 = **0.2222** V;
- second ($3T_D$): plus 0.2222 × (−1/9), giving **0.1975** V;
- third ($5T_D$): **0.2003** V.

The final value is the divider $1 \times 25/125$ = **0.2** V. $\Gamma_S\Gamma_L$ = −1/9 is small, so the voltage settles within a few round trips, alternating around 0.2 V.

### Solution 13-07.5

The total source resistance must be 50 Ω, so the series resistor is **35** Ω. The launched wave is 1.8/2 = **0.9** V; at the open receiver it doubles to **1.8** V at 0.8 ns and stays there. Just after the resistor the voltage is **0.9** V until the reflection returns, for $2T_D$ = **1.6** ns.

### Solution 13-07.6

Parallel to ground: $3.3^2/50$ = **0.2178** W while high, nothing while low. Thevenin, line high (the driver holds the node at 3.3 V): the resistor to 3.3 V has no voltage across it, and the one to ground dissipates $3.3^2/100$ = **0.1089** W. With the driver off, the pair draws $3.3/200$ = 16.5 mA continuously: **0.05445** W of standing power, in every state. The Thevenin split halves the worst-case driver current but adds a constant drain.

### Solution 13-07.7

The capacitor charges through the line's impedance: τ = $Z_0C$ = 50 × 5 pF = **250** ps. The final voltage is $2v^+$ = **1** V (an open end at DC). The 10–90% rise time of $1 - e^{-t/\tau}$ is $\tau\ln 9$ = **549.3** ps: the receiver's capacitance, not the driver, now limits the edge.

### Solution 13-07.8

$z = v\,t_{rt}/2 = 0.66 \times 2.998 \times 10^8 \times 4.2\ \text{ns}/2$ = **0.4155** m.

### Solution 13-07.9

The delay is 6.671 ps/mm. One sixth of 100 ps is 16.67 ps, so the critical length is **2.498** mm; at 1 ns it is **2.498** cm. Rise time, not clock frequency, decides: a slow 10 MHz clock with a 100 ps edge still needs transmission-line care.

### Solution 13-07.10

**Series inductance.** At the inductor the incoming line acts as a Thévenin source $2v^+$ behind $Z_0$ (chapter §3.5), and the continuing matched line is a resistor $Z_0$, so the loop is $2v^+$ driving $Z_0 + sL + Z_0$. The voltage across the inductor plus the continuing line, as seen at the junction, is the "load" voltage $v = v^+ + v^-$; in the Laplace domain the load impedance is $Z = sL + Z_0$, and

$$
\Gamma(s) = \frac{Z - Z_0}{Z + Z_0} = \frac{sL}{2Z_0 + sL} = \frac{s\tau}{1 + s\tau}, \qquad \tau = \frac{L}{2Z_0} .
$$

For an ideal step ($V^+ = v^+/s$), $V^- = v^+\tau/(1 + s\tau)$, so $\rho(t) = v^-/v^+ = e^{-t/\tau}$: a positive spike of area τ. More generally the area of the reflection is $\int v^-dt = V^-(0) = \lim_{s\to0}\Gamma(s)V^+(s)$; any step of height $v^+$, however slow its edge, has $V^+(s) \to v^+/s$ as $s \to 0$, so the normalized area is $\lim_{s\to0}\Gamma(s)/s = \tau$. Hence $L = 2Z_0\int\rho\,dt$ = 2 × 50 Ω × 10 ps = **1** nH.

**Shunt capacitance.** Now the load at the junction is $C$ in parallel with the continuing line: $Z = Z_0/(1 + sZ_0C)$, and

$$
\Gamma(s) = \frac{Z_0/(1 + sZ_0C) - Z_0}{Z_0/(1 + sZ_0C) + Z_0} = -\frac{sZ_0C}{2 + sZ_0C} = -\frac{s\tau}{1 + s\tau}, \qquad \tau = \frac{Z_0C}{2} .
$$

An ideal step gives $\rho(t) = -e^{-t/\tau}$, and by the same limit the area is $-\tau$ for any edge. So $C = -2\int\rho\,dt/Z_0$ = 2 × 25 ps/50 Ω = **1** pF. The derivation shows why the method is robust: the area depends only on $\Gamma(s)$ near $s = 0$, which the element sets, not on the instrument's rise time, which only spreads the shape.

### Solution 13-07.11

For $v = f(t - z/v)$ and $i = f(t - z/v)/Z_0$: $\partial v/\partial z = -f'/v$ and $-L'\partial i/\partial t = -L'f'/Z_0$, which are equal because $L'/Z_0 = \sqrt{L'C'} = 1/v$. The second equation, $\partial i/\partial z = -C'\partial v/\partial t$, holds the same way because $C'Z_0 = \sqrt{L'C'} = 1/v$; the backward wave works with both signs flipped. From the data, $v$ = 0.66c = 1.979 × 10⁸ m/s, so $L' = 1/(v^2C')$ = **252.9** nH/m and $Z_0 = 1/(vC')$ = **50.04** Ω: the data sheet's 50 Ω is consistent with its capacitance and velocity to 0.1%.

### Solution 13-07.12

$v^+ = 1 \times 75/100$ = **0.75** V; $\Gamma_L = (150 - 75)/225$ = **0.3333**; $\Gamma_S = (25 - 75)/100$ = **−0.5**. At the load: **1.000** V at $T_D$, then **0.8333**, **0.8611** and **0.8565** V, converging to $1 \times 150/175$ = **0.8571** V.

### Solution 13-07.13

The pattern repeats every $4T_D$ (two round trips, since each reflection from the source inverts the wave), so the ringing frequency is $1/(4\ \text{ns})$ = **250** MHz.

### Solution 13-07.14

At the junction the second line acts as a 75 Ω load: $\Gamma = (75 - 50)/125$ = 0.2 and $\tau = 1 + \Gamma$ = **1.2**. The wave reaching the matched load is 1.2 × 0.5 = **0.6** V, and **0.1** V reflects back to the (matched) source, where it is absorbed. Steady state: 0.6 V everywhere, the divider $1 \times 75/(50 + 75)$.

### Solution 13-07.15

(a) A wave's current is its voltage divided by $\pm Z_0$: $i^+ = v^+/Z_0$ and $i^- = -v^-/Z_0$. With $v^- = \Gamma v^+$, $i^- = -\Gamma i^+$, so currents reflect with $-\Gamma$: an open end ($\Gamma$ = +1) sends back a current that cancels the incident one, as it must. Here $v^+ = 1 \times 50/60$ = 0.8333 V and $i^+$ = **16.67** mA; $\Gamma_L$ = 150/250 = 0.6 and $\Gamma_S$ = −40/60 = −2/3, so the current coefficients are −0.6 at the load and +2/3 at the source.

(b) At the load after 1 ns, $i_L = (1 - \Gamma_L)i^+$ = **6.667** mA (check: $v_L$ = 1.6 × 0.8333 = 1.333 V, and 1.333/200 = 6.667 mA). The reflected wave is $v^-$ = 0.5 V. At the source the current is $i^+$ = **16.67** mA until 2 ns, when the 0.5 V wave arrives and re-reflects as −0.3333 V: the source-end voltage becomes 0.8333 + 0.5 − 0.3333 = 1.000 V, equal to the source voltage, so the source current is $(1 - 1.000)/10$ = **0** mA from 2 to 4 ns. The −0.3333 V wave reaches the load at 3 ns: $v_L$ = 1.333 + 1.6 × (−0.3333) = 0.8 V and $i_L$ = **4** mA. At 4 ns its reflection (−0.2 V) reaches the source, which re-reflects +0.1333 V; the source-end voltage drops to 0.9333 V and the source current is $(1 - 0.9333)/10$ = **6.667** mA.

(c) Finally the line is a wire: $I = 1/(10 + 200)$ = **4.762** mA. The source current is zero from 2 to 4 ns because the charge stored on the line by the first trip holds the source end at exactly the source voltage; the line, not the source, is then supplying the load (a line is a distributed capacitor charged by the first wave).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 13-07.1a | characteristic impedance | 50.01 | Ω |
| 13-07.1b | velocity | 1.499 × 10⁸ | m/s |
| 13-07.1c | delay | 6.671 | ps/mm |
| 13-07.1d | relative permittivity | 4.000 | — |
| 13-07.2a | short | −1 | — |
| 13-07.2b | open | 1 | — |
| 13-07.2c | 25 Ω | −0.3333 | — |
| 13-07.2d | 75 Ω | 0.2 | — |
| 13-07.2e | 100 Ω | 0.3333 | — |
| 13-07.3a | launched step | 2.2 | V |
| 13-07.4a | launched wave | 0.3333 | V |
| 13-07.4b | source reflection coefficient | 0.3333 | — |
| 13-07.4c | load reflection coefficient | −0.3333 | — |
| 13-07.4d | first arrival | 0.2222 | V |
| 13-07.4e | second arrival | 0.1975 | V |
| 13-07.4f | third arrival | 0.2003 | V |
| 13-07.4g | final value | 0.2 | V |
| 13-07.5a | series resistor | 35 | Ω |
| 13-07.5b | launched wave | 0.9 | V |
| 13-07.5c | receiver voltage | 1.8 | V |
| 13-07.5d | source-side plateau | 0.9 | V |
| 13-07.5e | plateau duration | 1.6 | ns |
| 13-07.6a | parallel termination, high | 0.2178 | W |
| 13-07.6b | Thevenin, high | 0.1089 | W |
| 13-07.6c | Thevenin, standing | 0.05445 | W |
| 13-07.7a | time constant | 250 | ps |
| 13-07.7b | final voltage | 1 | V |
| 13-07.7c | 10–90% rise time | 549.3 | ps |
| 13-07.8a | distance to the break | 0.4155 | m |
| 13-07.9a | critical length at 100 ps | 2.498 | mm |
| 13-07.9b | critical length at 1 ns | 2.498 | cm |
| 13-07.10a | series inductance | 1 | nH |
| 13-07.10b | shunt capacitance | 1 | pF |
| 13-07.11a | inductance per metre | 252.9 | nH/m |
| 13-07.11b | characteristic impedance | 50.04 | Ω |
| 13-07.12a | launched wave | 0.75 | V |
| 13-07.12b | load reflection coefficient | 0.3333 | — |
| 13-07.12c | source reflection coefficient | −0.5 | — |
| 13-07.12d | first arrival | 1.000 | V |
| 13-07.12e | second arrival | 0.8333 | V |
| 13-07.12f | third arrival | 0.8611 | V |
| 13-07.12g | fourth arrival | 0.8565 | V |
| 13-07.12h | final value | 0.8571 | V |
| 13-07.13a | ringing frequency | 250 | MHz |
| 13-07.14a | junction transmission coefficient | 1.2 | — |
| 13-07.14b | voltage at the load | 0.6 | V |
| 13-07.14c | reflected wave | 0.1 | V |
| 13-07.15a | launched current | 16.67 | mA |
| 13-07.15b | load current after 1 ns | 6.667 | mA |
| 13-07.15c | source current, 0 to 2 ns | 16.67 | mA |
| 13-07.15d | source current, 2 to 4 ns | 0 | mA |
| 13-07.15e | load current after 3 ns | 4 | mA |
| 13-07.15f | source current after 4 ns | 6.667 | mA |
| 13-07.15g | final current | 4.762 | mA |
