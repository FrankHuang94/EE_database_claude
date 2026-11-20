# Solutions 15-12 · Applications: PLLs, Voltage Regulators and Thermal Management

Problems: [15-12 problems](../problems/15-12-problems.md) · Chapter: [15-12](../chapters/15-12-control-applications-pll-regulators-thermal.md)

Every number below is recomputed by [verify_15_12.py](../verify/verify_15_12.py): PLL designs by the closed forms of §3.2 and by the margins of the resulting loops, closed-loop poles by root finding, overshoot and peaking from exact responses, jitter by numerical integration, LDO margins by root finding, and thermal responses with the matrix exponential.

---

## Solutions

### Solution 15-12.1

$$
K = \frac{I_{cp}K_v}{2\pi N(C + C_2)} = \frac{50 \times 10^{-6} \times 2\pi \times 5 \times 10^8}{2\pi \times 64 \times 5 \times 10^{-10}} = \mathbf{7.81 \times 10^{11}}\ \text{s}^{-2} .
$$

The steady phase error after a reference frequency step is **zero**: the loop has two integrators (the VCO and the filter capacitor), so it is type 2, and a type-2 loop follows a ramp of phase (a frequency step) with zero error (15-04).

### Solution 15-12.2

With $\sqrt b = \tan\text{PM} + \sec\text{PM}$, $C/C_2 = b - 1$ and $\zeta = (\sqrt b - 1)/2$:

| PM | $\sqrt b$ | $b$ | $C/C_2$ | $\zeta$ |
|---|---|---|---|---|
| 45° | **2.414** | **5.83** | **4.83** | **0.707** |
| 50° | **2.747** | **7.55** | **6.55** | **0.874** |
| 65° | **4.511** | **20.35** | **19.35** | **1.755** |

The pair is real when $\zeta \ge 1$, that is $\sqrt b \ge 3$: of these, only the **65°** design (with the 60° design of Example 15-12.3) has all-real poles. The 45° design's pair has $\zeta = 1/\sqrt2$ exactly, since $\sqrt b = 1 + \sqrt2$. The capacitor ratio grows steeply with the margin: from 4.83 at 45° to 19.35 at 65°, four times the capacitor spread for 20° more margin.

### Solution 15-12.3

**(a)** $f_c \le f_{ref}/10$ = **2.5** MHz. At 1 MHz, the sampling cost is about $\pi f_c/f_{ref} = \pi/25$ rad = **7.2**°.

**(b)** Identical stages peaking at the same frequency multiply their gains there, so the decibels add: 20 × 0.1 = **2** dB, an amplitude ratio of $10^{2/20}$ = **1.259**. This is why clock-recovery chains specify very small peaking per stage.

### Solution 15-12.4

$x = \tan55° + \sec55° = 1.428 + 1.743$ = **3.172** and $b$ = **10.06**. With $\omega_c = 2\pi \times 10^6$ rad/s:

- $\tau_z = x/\omega_c$ = **0.5048** µs and $\tau_p = 1/(x\omega_c)$ = **50.18** ns;
- $K = \omega_c^2/x$ = **1.245 × 10¹³** s⁻²;
- $C + C_2 = I_{cp}K_v/(2\pi NK) = 2 \times 10^{-4} \times 10^9/(48 \times 1.245 \times 10^{13})$ = **334.7** pF;
- $C_2 = 334.7/10.06$ = **33.28** pF, $C$ = **301.5** pF and $R = \tau_z/C$ = **1.674** kΩ.

The reference is 50 times the crossover, so the sampling cost is about $180° \times f_c/f_{ref}$ = **3.6**°. Since $x > 3$, the closed-loop poles are all real ($\zeta$ = 1.086).

### Solution 15-12.5

For PM = 45°, $x = 1 + \sqrt2$ and $\zeta = (x - 1)/2 = 1/\sqrt2$. The poles are $-\omega_c$ and the roots of $s^2 + \sqrt2\,\omega_cs + \omega_c^2$: **−1** and **−0.707 ± j0.707** in units of $\omega_c$.

Exact responses of $T$: the frequency-step overshoot is **33.6**% and the jitter-transfer peak **3.20** dB at **0.713**$\omega_c$. The 60° design of Example 15-12.3 has 18.8% and 1.70 dB at 0.466$\omega_c$. Fifteen degrees of margin cost about 2.7 times the capacitor ratio (13.93 − 1 against 5.83 − 1) and buy roughly half the overshoot and the peaking.

### Solution 15-12.6

$$
\phi_{rms} = \sqrt{2 \times 10^{-10} \times (10^6 - 10^4)} = \mathbf{14.07}\ \text{mrad},
$$

and the jitter is $0.01407/(2\pi \times 10^9)$ = **2.24** ps. Because the integral runs over hertz, not decades, the top decade (100 kHz to 1 MHz) contributes **90.9**% of the total: flat noise is dominated by its highest offsets.

### Solution 15-12.7

**(a)** At $R_L$ = 1 kΩ the crossover is **635** kHz and the margin **53.7**° (against 621 kHz and 54.3° at 10 Ω). Above the output pole, $Z(s) \approx R_{ESR} + 1/(sC_L)$ whatever $R_L$ is, so the loop gain near crossover is $A_0\beta g_m(1 + sR_{ESR}C_L)/[sC_L(1 + s/\omega_a)(1 + s/\omega_g)]$, independent of $R_L$. Raising $R_L$ a hundredfold raises the DC loop gain a hundredfold but lowers the output pole a hundredfold, and nothing changes near crossover.

**(b)** With $g_m$ = 0.05 A/V the loop gain near crossover falls tenfold: crossover drops to **86.9** kHz and the margin is **60.2**°. The 45° ESR window moves to **0.193** Ω to **5.81** Ω: at the lower crossover, a zero needs to sit lower (more ESR) to help.

**(c)** At full load 0.15 Ω is inside the window (margin 55.6°). At light load it is below the new lower limit: the margin is **37.2**° at a 68.3 kHz crossover, stable but below the 45° criterion, with more ringing on load steps. The capacitor must be chosen for the whole load range, which is why LDO datasheets plot the stable region against load current.

### Solution 15-12.8

Load line: $C = \Delta I/(\omega_c\Delta V) = 100/(2\pi \times 10^5 \times 0.04)$ = **3.98** mF. Critically damped PI: the peak is $(2/e)$ times smaller for the same $C$, so $C = (2/e) \times 3.98$ mF = **2.93** mF. Either way, the capacitance is millifarads; doubling the regulator's bandwidth would halve it.

### Solution 15-12.9

Frequency first: the PLL relocks to 1.0 GHz while the core is stalled for **20** µs. Then the voltage falls 250 mV at 10 mV/µs in **25** µs, with the core running at 1.0 GHz. Dynamic power falls to $(0.75/1.00)^2 \times 1.0/2.0$ = **0.281** of its value; energy per cycle to $(0.75)^2$ = **0.5625**.

### Solution 15-12.10

$P_{sus} = (95 - 30)/(0.15 + 0.25)$ = **162.5** W. At 200 W the junction sits 30 K above the heat sink, so throttling starts when the heat sink reaches 35 K out of a final 200 × 0.25 = 50 K. One-pole estimate with $R_{CA}C_H$ = 75 s: $75\ln(50/15)$ = **90.3** s. The exact two-node response gives **93.3** s. The permitted power then decays toward 162.5 W with $C_H(R_{JC} \parallel R_{CA}) = 300 \times 0.09375$ = **28.1** s. The better heat sink raises sustained power by 25% and lengthens the full-power window by about 18 s.

### Solution 15-12.11

With leakage, a temperature rise $\delta\theta_J$ adds $(dP_L/dT)\delta\theta_J$ of power, so $\theta_J = Z_{th}(P + 0.6\,\theta_J)$ and the plant becomes $Z_{th}/(1 - 0.6Z_{th})$, where $Z_{th}(s) = \theta_J/P$ of the two-node model.

- At DC, $Z_{th}$ = 0.5 K/W, and with leakage $0.5/(1 - 0.3)$ = **0.714** K/W: 43% more gain.
- At 2 rad/s, $\lvert Z_{th}\rvert$ = **0.0828** K/W, and with leakage **0.0850** K/W: under 3% more.

The throttling loop crosses over near 2 rad/s, where leakage barely changes the plant, so its margin and speed are almost unaffected. The large change is at low frequency: the same power raises the temperature more, and at the limit the thermal network still removes only 130 W in total, of which leakage at 95 °C takes its share. Leakage therefore costs sustained useful performance much more than it costs loop stability (as long as $R\,dP_L/dT$ stays below 1, the runaway boundary of 15-01).

### Solution 15-12.12

Crossing: $-115 + 20\log_{10}(1\ \text{MHz}/f) = -100$ gives $f = 10^{-0.75}$ MHz = **178** kHz. The numerical optimum is also **178** kHz, where the rms phase is **12.3** mrad and the jitter $0.0123/(2\pi \times 10^9)$ = **1.95** ps.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 15-12.1a | K | 7.81e11 | 1/s² |
| 15-12.1b | steady phase error after a frequency step | 0 | rad |
| 15-12.2a | √b, 45° | 2.414 | — |
| 15-12.2b | b, 45° | 5.83 | — |
| 15-12.2c | C/C2, 45° | 4.83 | — |
| 15-12.2d | ζ, 45° | 0.707 | — |
| 15-12.2e | √b, 50° | 2.747 | — |
| 15-12.2f | b, 50° | 7.55 | — |
| 15-12.2g | C/C2, 50° | 6.55 | — |
| 15-12.2h | ζ, 50° | 0.874 | — |
| 15-12.2i | √b, 65° | 4.511 | — |
| 15-12.2j | b, 65° | 20.35 | — |
| 15-12.2k | C/C2, 65° | 19.35 | — |
| 15-12.2l | ζ, 65° | 1.755 | — |
| 15-12.2m | design with all-real poles | 65 | ° |
| 15-12.3a | largest crossover | 2.5 | MHz |
| 15-12.3b | sampling cost at 1 MHz | 7.2 | ° |
| 15-12.3c | chain peaking | 2 | dB |
| 15-12.3d | chain peaking | 1.259 | — |
| 15-12.4a | √b | 3.172 | — |
| 15-12.4b | b | 10.06 | — |
| 15-12.4c | τz | 0.5048 | µs |
| 15-12.4d | τp | 50.18 | ns |
| 15-12.4e | K | 1.245e13 | 1/s² |
| 15-12.4f | C + C2 | 334.7 | pF |
| 15-12.4g | C2 | 33.28 | pF |
| 15-12.4h | C | 301.5 | pF |
| 15-12.4i | R | 1.674 | kΩ |
| 15-12.4j | sampling cost | 3.6 | ° |
| 15-12.5a | real pole | −1 | ωc |
| 15-12.5b | complex pair | −0.707 + j0.707 | ωc |
| 15-12.5c | overshoot | 33.6 | % |
| 15-12.5d | jitter-transfer peak | 3.20 | dB |
| 15-12.5e | frequency of the peak | 0.713 | ωc |
| 15-12.6a | rms phase | 14.07 | mrad |
| 15-12.6b | rms jitter | 2.24 | ps |
| 15-12.6c | share of the top decade | 90.9 | % |
| 15-12.7a | crossover at 1 kΩ | 635 | kHz |
| 15-12.7b | phase margin at 1 kΩ | 53.7 | ° |
| 15-12.7c | crossover at light load | 86.9 | kHz |
| 15-12.7d | phase margin at light load | 60.2 | ° |
| 15-12.7e | lowest ESR for 45°, light load | 0.193 | Ω |
| 15-12.7f | highest ESR for 45°, light load | 5.81 | Ω |
| 15-12.7g | margin with 0.15 Ω, light load | 37.2 | ° |
| 15-12.8a | load-line capacitance | 3.98 | mF |
| 15-12.8b | PI capacitance | 2.93 | mF |
| 15-12.9a | stall | 20 | µs |
| 15-12.9b | voltage ramp | 25 | µs |
| 15-12.9c | dynamic power ratio | 0.281 | — |
| 15-12.9d | energy-per-cycle ratio | 0.5625 | — |
| 15-12.10a | sustained power | 162.5 | W |
| 15-12.10b | full power, one-pole estimate | 90.3 | s |
| 15-12.10c | full power, exact | 93.3 | s |
| 15-12.10d | decay time constant | 28.1 | s |
| 15-12.11a | DC gain with leakage | 0.714 | K/W |
| 15-12.11b | gain at 2 rad/s | 0.0828 | K/W |
| 15-12.11c | gain at 2 rad/s with leakage | 0.0850 | K/W |
| 15-12.12a | noise crossing | 178 | kHz |
| 15-12.12b | optimal crossover | 178 | kHz |
| 15-12.12c | rms phase at the optimum | 12.3 | mrad |
| 15-12.12d | rms jitter at the optimum | 1.95 | ps |
