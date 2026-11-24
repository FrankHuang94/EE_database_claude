# Solutions 20-02 · Two-Stage Op-Amp Design

Problems: [20-02 problem set](../problems/20-02-problems.md) · Chapter: [20-02](../chapters/20-02-two-stage-op-amp-design.md). Every number below is recomputed by [verify_20_02.py](../verify/verify_20_02.py).

---

## Solutions

### Solution 20-02.1

(a) $\omega_u = 2\pi(20\text{ MHz})$ = 1.2566 × 10⁸ rad/s.

- Slew: $(g_m/I_D)_1 \le 2\omega_u/\text{SR} = 2(1.2566 \times 10^8)/(10^7)$ = **25.13** S/A.
- Noise: $g_{m1} \ge 8kT\gamma(1 + 0.5)/\bar v_n^2 = 8(4.1419 \times 10^{-21})(2/3)(1.5)/(20 \times 10^{-9})^2$ = **82.84** µS.
- Bandwidth: $C_c = g_{m1}/\omega_u \ge$ **0.659** pF.
- Tail: $I_{SS} = 2g_{m1}/(g_m/I_D)_1 \ge 2(82.84\ \mu\text{S})/(25.13\ \text{S/A})$ = **6.59** µA.

(b) The ceiling falls to $2\omega_u/(25\text{ V/µs})$ = **10.05** S/A, so $I_{SS} \ge$ **16.48** µA, **2.5** times more. With $g_{m1}$ pinned by the noise and $(g_m/I_D)_1 = 2\omega_u/\text{SR}$, the minimum tail current is $2g_{m1}/(g_m/I_D)_1 = g_{m1}\,\text{SR}/\omega_u$: proportional to the slew rate, so the factor is 25/10. A high slew rate at a modest GBW forces the input pair into strong inversion and wastes its current as far as noise is concerned.

### Solution 20-02.2

With $x = \omega_c/\omega_u$, $x^2 = (\kappa^2/2)(\sqrt{1 + 4/\kappa^2} - 1)$ and PM = $90^\circ - \arctan(x/\kappa)$:

| $\kappa$ | $x$ | Exact PM | $90^\circ - \arctan(1/\kappa)$ |
|---|---|---|---|
| 1 | **0.786** | **51.8**° | **45.0**° |
| 2.2 | **0.922** | **67.3**° | **65.6**° |
| 3 | **0.953** | **72.4**° | **71.6**° |

The estimate is always pessimistic: it evaluates the second pole's lag at $\omega_u$, but the true crossover is lower, where the pole lags less. The error is large at small $\kappa$ (6.8° at $\kappa$ = 1) and small at large $\kappa$, where the crossover approaches $\omega_u$.

### Solution 20-02.3

(a) From $\text{SR} = 2\omega_u/(g_m/I_D)_1$ with $\omega_u$ = 6.283 × 10⁷ rad/s, $\text{SR}/\omega_u = 2/(g_m/I_D)_1$ is **80.0** mV, **133.3** mV and **400** mV, so SR = **5.03**, **8.38** and **25.1** V/µs.

(b) No MOSFET can exceed the weak-inversion limit $g_m/I_D = 1/(nV_T)$, so $\text{SR} \ge 2nV_T\,\omega_u$ = (**67.2** mV)(6.283 × 10⁷ s⁻¹) = **4.22** V/µs. A lower slew rate would need more $g_m$ per unit of tail current than diffusion physics allows; if a part slews slower, something other than the input stage is limiting it.

### Solution 20-02.4

(a) $A_0 = g_{m1}R_1g_{m6}R_2 = (100\ \mu\text{S})(1\text{ MΩ})(1\text{ mS})(50\text{ kΩ})$ = **5000**.

$$
\begin{aligned}
a_1 &= g_{m6}R_1R_2C_c + R_1(C_1 + C_c) + R_2(C_L + C_c) = 15.0\ \mu\text{s} + 0.4\ \mu\text{s} + 0.065\ \mu\text{s} = \textbf{15.465}\ \mu\text{s},\\
a_2 &= R_1R_2\,[C_1C_L + C_c(C_1 + C_L)] = (5 \times 10^{10})(0.1 + 0.33)\times 10^{-24} = \textbf{2.15} \times 10^{-14}\ \text{s}^2 .
\end{aligned}
$$

(b) The roots of $a_2s^2 + a_1s + 1$ are at **10.29** kHz and **114.5** MHz. Pole splitting gives $1/(2\pi g_{m6}R_1R_2C_c)$ = **10.61** kHz and $g_{m6}C_c/\{2\pi[C_1C_L + C_c(C_1 + C_L)]\}$ = **111.0** MHz, both about **3**% off. The naive $g_{m6}/(2\pi C_L)$ = **159.2** MHz is **39**% too high: here $C_1$ is not small against $C_c$.

(c) GBW = $g_{m1}/(2\pi C_c)$ = **53.05** MHz; RHP zero at $g_{m6}/(2\pi C_c)$ = **530.5** MHz. The exact loop gain crosses unity at **47.69** MHz with PM = **62.3**° (gain margin **20.3** dB).

### Solution 20-02.5

For the T130 PMOS ($\mu$ = 100 cm²/V·s), 10 S/A at 0.5 µm needs $IC$ = **5.64**, where $f_{T6}$ = **0.936** GHz, **3.3** times lower than the NMOS's 3.07 GHz. The bound is $f_{T6}C_c/(C_L + C_c)$ = **215.9** MHz. Placing $p_2$ at 100 MHz, now almost half the bound,

$$
g_{m6} = \frac{p_2[C_p(C_L + C_c) + C_cC_L]}{C_c - p_2(C_L + C_c)/\omega_{T6}} = \textbf{2.493}\text{ mS},
$$

with $C_1$ = 30 fF + $g_{m6}/\omega_{T6}$ = **454.1** fF and $I_6$ = **249.3** µA, **1.60** times the NMOS design's 155.8 µA. The lower mobility hurts twice: more $g_m$ is needed, and each unit of $g_m$ brings more gate capacitance.

### Solution 20-02.6

(a) $R_z = 1/g_{m6}$ = **641.8** Ω. With $R_z = 1.2/g_{m6}$, $z = 1/[C_c(R_z - 1/g_{m6})] = g_{m6}/(0.2C_c)$, a left-half-plane zero at **2.07** GHz.

(b) $1/g_{m6}$ ranges over 641.8/1.15 = **558.1** Ω to 641.8/0.85 = **755.1** Ω, and $R_z$ over **513.4** to **770.2** Ω.

- The worst right-half-plane case is the largest $1/g_{m6} - R_z$ = **241.6** Ω: $z = 1/(C_c \times 241.6\ \Omega)$, at **1.098** GHz.
- The worst left-half-plane case is the largest $R_z - 1/g_{m6}$ = **212.1** Ω, at **1.251** GHz.

The worst phase cost at the crossover is $\arctan(43.62/1098)$ = **2.28**°: removing the zero to infinity is robust even with an untracked resistor, because a residual zero lands far above the crossover either way.

(c) From §3.4, $(W/L)_z = (W/L)_6/n = (28.16/0.5)/1.3$ = **43.3**.

### Solution 20-02.7

$\tau = 1/\omega_u$ = **3.183** ns and SR·τ = **0.1111** V, the largest step followed linearly.

(a) Both steps slew.

- **0.2 V:** $t_{slew} = (0.2 - 0.1111)/(34.9\text{ V/µs})$ = **2.55** ns and $t_{lin} = \tau\ln[0.1111/(0.001 \times 0.2)]$ = **20.12** ns, total **22.66** ns.
- **1 V:** $t_{slew}$ = **25.46** ns and $t_{lin} = \tau\ln(0.1111/0.001)$ = **14.99** ns, total **40.46** ns.

The larger step spends most of its time slewing.

(b) Solving $(1 - \text{SR}\,\tau)/\text{SR} + \tau\ln(\text{SR}\,\tau/0.001)$ = 30 ns numerically gives SR = **60.9** V/µs, which needs $(g_m/I_D)_1 = 2\omega_u/\text{SR}$ = **10.3** S/A: a stronger-inverted, noisier input pair (or a larger $I_{SS}$ with the same $g_{m1}$, which is the same thing).

### Solution 20-02.8

(a) $I_6 \ge I_{SS}(1 + C_L/C_c) = 20.94\ \mu\text{A} \times (1 + 5/0.6)$ = **195.5** µA.

(b) $(I_6 - I_{SS})/C_L = (155.8 - 20.94)\ \mu\text{A}/5\text{ pF}$ = **27.0** V/µs, below the internal 34.9 V/µs: the rising edge is now limited by the output stage, while the falling edge, on which M6 can sink extra current, still slews at 34.9 V/µs.

### Solution 20-02.9

(a) Long channel, $q = (\sqrt{1 + 4IC} - 1)/2$; then $q_d$ from $q_d^2 + q_d = 0.02(q^2 + q)$ and $V_{DS,sat} = V_T[2(q - q_d) + \ln(q/q_d)]$:

| $IC$ | $q$ | $V_{DS,sat}$ |
|---|---|---|
| 0.1 | **0.0916** | **0.104** V |
| 1 | **0.618** | **0.120** V |
| 10 | **2.70** | **0.202** V |

(b) The swing is $V_{DD} - 2V_{DS,sat}$: **0.660** V at $IC$ = 1 and **0.496** V at $IC$ = 10. The faster, more strongly inverted design gives up a quarter of its swing (**0.164** V) on a 0.9 V supply.

### Solution 20-02.10

(a) With $G_1 = 1/R_1$, $G_{o6} = I_6/4\text{ V}$ and $s = j2\pi f$ in §3.10's expression, PSRR⁻ = **67.9** dB at 10 kHz and **53.6** dB at 100 kHz (from 69.2 dB at DC).

(b) The rejection reaches 40 dB at **484.5** kHz; the asymptote $f_u/f$ = 100 gives **500** kHz, **3**% higher, because the zero term $G_1G_{o6}$ still contributes slightly.

### Solution 20-02.11

(a) $C_m = 2 \times \tfrac23 W_3L_3C_{ox} = \tfrac43(3.707\ \mu\text{m})(1\ \mu\text{m})(8.6\text{ fF/µm}^2)$ = **42.5** fF; $g_{m3}$ = 10.125 × 10.47 µA = **106.0** µS. The mirror pole is $g_{m3}/(2\pi C_m)$ = **396.9** MHz, and the mirror adds a zero at twice it, **793.8** MHz (12-08 §3.3).

(b) At 43.62 MHz the doublet costs $\arctan(43.62/396.9) - \arctan(43.62/793.8)$ = **3.13**°, so PM ≈ 67.6 − 3.1 = **64.5**°.

(c) The mirror device is long (1 µm, for gain) and its node carries two gate capacitances, so its pole sits near half of a long device's $f_T$. $p_3$ belongs to the short M6 and sits near its $f_T$, about seven times higher here.

### Solution 20-02.12

(a) With $v_x$ the junction of $R_z$ and $C_c$:

$$
\begin{aligned}
(G_1 + sC_1)V_1 + (V_1 - V_x)/R_z &= -g_{m1}V_{in},\\
(V_x - V_1)/R_z + sC_c(V_x - V_o) &= 0,\\
(G_2 + sC_L)V_o + sC_c(V_o - V_x) + g_{m6}V_1 &= 0 .
\end{aligned}
$$

At a zero of transmission $V_o = 0$, so the third equation requires the current through $C_c$, $sC_cV_x$, to equal $g_{m6}V_1$ (with the sign that cancels); the second gives $V_x = V_1/(1 + sC_cR_z)$. Then $sC_c/(1 + sC_cR_z) = g_{m6}$, i.e. $s = g_{m6}/[C_c(1 - g_{m6}R_z)] = 1/[C_c(1/g_{m6} - R_z)]$.

(b) Write the three equations as a nodal matrix, with $G_z = 1/R_z$:

$$
\begin{bmatrix} G_1 + sC_1 + G_z & -G_z & 0\\ -G_z & G_z + sC_c & -sC_c\\ g_{m6} & -sC_c & G_2 + sC_L + sC_c\end{bmatrix}\begin{bmatrix}V_1\\V_x\\V_o\end{bmatrix} = \begin{bmatrix}-g_{m1}V_{in}\\0\\0\end{bmatrix} .
$$

The poles are the roots of its determinant. Expanding along the first row,

$$
\Delta = (G_1 + sC_1 + G_z)\left[(G_z + sC_c)(G_2 + sC_L + sC_c) - s^2C_c^2\right] + G_z\left[sC_cg_{m6} - G_z(G_2 + sC_L + sC_c)\right] .
$$

Collect powers of $s$. The constant term is $(G_1 + G_z)G_zG_2 - G_z^2G_2 = G_1G_2G_z$. The $s$ term is $C_1G_2G_z + C_LG_1G_z + C_c(G_1G_2 + G_1G_z + G_2G_z + G_zg_{m6})$. The $s^2$ term is $C_1C_LG_z + C_1C_c(G_2 + G_z) + C_LC_c(G_1 + G_z)$: the $s^2C_c^2$ terms cancel. The $s^3$ term is $C_1C_LC_c$. Dividing by the constant term $G_1G_2G_z$ and writing $G = 1/R$:

$$
\begin{aligned}
a_1 &= R_1C_1 + R_2C_L + R_1C_c + R_2C_c + R_zC_c + g_{m6}R_1R_2C_c,\\
a_2 &= R_1R_2[C_1C_L + C_c(C_1 + C_L)] + R_zC_c(R_1C_1 + R_2C_L),\\
a_3 &= R_1R_2R_zC_1C_LC_c ,
\end{aligned}
$$

which are §3.4's coefficients: $R_z$ adds $R_zC_c$ to $a_1$, $R_zC_c(R_1C_1 + R_2C_L)$ to $a_2$, and creates $a_3$. Dividing,

$$
\frac{a_2}{a_3} = \frac{C_1C_L + C_c(C_1 + C_L)}{R_zC_1C_LC_c} + \frac{R_1C_1 + R_2C_L}{R_1R_2C_1C_L} = \frac{1}{R_z}\left(\frac{1}{C_1} + \frac{1}{C_c} + \frac{1}{C_L}\right) + \frac{1}{R_2C_L} + \frac{1}{R_1C_1},
$$

and the last two terms are negligible (they are of the order of the open-loop pole frequencies).

(c) For the design with $R_z$ = 641.8 Ω: $a_1$ = **4.889** µs, $a_2$ = **7.321** × 10⁻¹⁵ s², $a_3$ = **4.181** × 10⁻²⁵ s³. $a_2/a_3$ gives **2.787** GHz and the capacitor form **2.777** GHz, against the exact **2.676** GHz (Example 20-02.4).

### Solution 20-02.13

(a) Comparing $s^2 + p_3s + p_2p_3$ with $s^2 + 2\zeta\omega_ns + \omega_n^2$: $\omega_n = \sqrt{p_2p_3}$ and $2\zeta\omega_n = p_3$, so $\zeta = p_3/(2\sqrt{p_2p_3}) = \tfrac12\sqrt{p_3/p_2}$.

- **Low-frequency lag.** For $\omega \ll \omega_n$ the pair's phase lag is about $2\zeta\omega/\omega_n = p_3\omega/(p_2p_3) = \omega/p_2$, the lag of a real pole at $p_2$.
- **Peak.** At $\omega_n$ the pair's magnitude is $1/(2\zeta)$, and the integrator contributes $\omega_u/\omega_n$, so $|L| \approx \omega_u/(2\zeta\omega_n) = \omega_u/p_3$.

(b) With $g_{m6}$ = 1 mS, $C_1$ = 81.8 fF:

- $p_2 \approx g_{m6}C_c/[C_1(C_L + C_c)]$ = **448.9** MHz;
- $p_3 \approx g_{mc}(C_L + C_c)/(C_LC_c)$ = **103.5** MHz;
- $\zeta \approx$ **0.240**, $f_n \approx$ **215.5** MHz;
- gain margin ≈ $20\log_{10}(p_3/\omega_u)$ = **6.3** dB.

(c) The natural frequency (within **1.2**%) and damping (within **6**%) are good, and the phase margin is high as predicted. The gain-margin estimate is **1.7** dB optimistic: it takes the peak as exactly $1/(2\zeta)$ at $\omega_n$ and ignores the extra lag from $C_x$ and the zeros, which move the −180° point to where the gain is higher. Use the estimate to choose $g_{mc}$, and the exact analysis (or simulation) to sign off.

### Solution 20-02.14

(a) $f_u = g_{m1}/(2\pi C_L)$ = **79.6** MHz and $\beta f_u$ = **26.5** MHz. Boosted gain $400 \times 101$ = **40,400**, static error $1/(\beta A)$ = **0.0074**%: below 0.01%, so the target is reachable.

(b) Tail amplitude $1/(\beta A_{unb}) = 3/400$ = **0.75**%. With $f_{ub}$ = 10 MHz, the tail alone takes $\ln(0.75/0.01)/(2\pi \times 10\text{ MHz})$ = **68.7** ns to fall to 0.01%.

(c) An ideal single-pole amplifier takes $\ln(10^4)/(\beta\omega_u)$ = **55.3** ns. With $f_{ub}$ = 100 MHz (above $\beta f_u$) the boosted amplifier matches it (55.4 ns); with $f_{ub}$ = 10 MHz (below $\beta f_u$) it takes 83.6 ns, half as long again. The exact figure exceeds (b)'s estimate because the booster here is not much slower than the closed loop, so the slow root sits below $\omega_{ub}$ and its residue is larger than $1/(\beta A_{unb})$. The fix is a faster booster, not a faster main amplifier.

### Solution 20-02.15

(a) The error shrinks by $C_s/(C_s + C_r)$ = 0.8/1.0 = **0.8** per cycle. A factor of 100 needs $N_{cyc} \ge \ln 100/\ln 1.25$ = 20.6, so **21** cycles, **420** ns at 50 MHz.

(b) $C_s/(C_s + C_r)$ = **0.889**; $N_{cyc} \ge \ln 100/\ln 1.125$ = 39.1, so **40** cycles, **800** ns.

(c) Any two of these:

- on φ2 each $C_r$ sits between one output and the control node, in parallel with $C_s$, loading the outputs and slowing the main amplifier;
- the switches inject charge proportional to their size, which a larger $C_r$ needs, and disturbs the common mode every cycle;
- a larger $C_r$ also takes more area.

Convergence of tens of cycles happens once, at start-up.

### Solution 20-02.16

(a) $\omega_u$ = 1.2566 × 10⁸ rad/s.

- $g_{m3} = 4\omega_uC_L$ = **5.027** mS;
- $C_{m1} = 4g_{m1}C_L/g_{m3}$ = **0.398** pF (equal to $g_{m1}/\omega_u$);
- $C_{m2} = 2g_{m2}C_L/g_{m3}$ = **0.199** pF.

(b) The exact phase margin of **60.0**° is within half a degree of the ideal 60.5°, with crossover **19.33** MHz and gain margin **12.2** dB. With higher stage gains than Example 20-02.6 the finite-gain error is smaller.

(c) $g_{m6} \approx 2\omega_uC_L$ = **2.513** mS: the three-stage design needs **2.0** times the output transconductance.

### Solution 20-02.17

(a) $f_uC_L/I$ = (100 MHz)(10 pF)/(2 mA) = **500** MHz·pF/mA. If the input stage limits slewing, $(g_m/I_D)_1 = 2\omega_u/\text{SR} = 2(6.283 \times 10^8)/(2 \times 10^8)$ = **6.28** S/A: strong inversion, plausible for a fast part.

(b) It would need $(g_m/I_D)_1$ = **251** S/A, **8.4** times the weak-inversion limit of **29.8** S/A: impossible. The slew rate must be limited elsewhere, for example by an output stage with too little current for its load, or by a separate small current.

(c) $2nV_T\,\omega_u$ = **42.2** V/µs.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 20-02.1a | maximum g_m/I_D | 25.13 | S/A |
| 20-02.1b | minimum g_m1 | 82.84 | µS |
| 20-02.1c | minimum C_c | 0.659 | pF |
| 20-02.1d | minimum I_SS | 6.59 | µA |
| 20-02.1e | g_m/I_D ceiling at 25 V/us | 10.05 | S/A |
| 20-02.1f | minimum I_SS at 25 V/us | 16.48 | µA |
| 20-02.1g | tail-current growth factor | 2.5 | — |
| 20-02.2a | crossover ratio, k = 1 | 0.786 | — |
| 20-02.2b | PM, k = 1 | 51.8 | ° |
| 20-02.2c | estimate, k = 1 | 45.0 | ° |
| 20-02.2d | crossover ratio, k = 2.2 | 0.922 | — |
| 20-02.2e | PM, k = 2.2 | 67.3 | ° |
| 20-02.2f | estimate, k = 2.2 | 65.6 | ° |
| 20-02.2g | crossover ratio, k = 3 | 0.953 | — |
| 20-02.2h | PM, k = 3 | 72.4 | ° |
| 20-02.2i | estimate, k = 3 | 71.6 | ° |
| 20-02.2j | estimate error at k = 1 | 6.8 | ° |
| 20-02.3a | SR/omega_u at 25 S/A | 80.0 | mV |
| 20-02.3b | SR/omega_u at 15 S/A | 133.3 | mV |
| 20-02.3c | SR/omega_u at 5 S/A | 400 | mV |
| 20-02.3d | SR at 25 S/A | 5.03 | V/µs |
| 20-02.3e | SR at 15 S/A | 8.38 | V/µs |
| 20-02.3f | SR at 5 S/A | 25.1 | V/µs |
| 20-02.3g | 2 n V_T | 67.2 | mV |
| 20-02.3h | minimum SR | 4.22 | V/µs |
| 20-02.4a | A_0 | 5000 | — |
| 20-02.4b | a_1 | 15.465 | µs |
| 20-02.4c | a_2 | 2.15e-14 | s² |
| 20-02.4d | exact p1 | 10.29 | kHz |
| 20-02.4e | exact p2 | 114.5 | MHz |
| 20-02.4f | estimated p1 | 10.61 | kHz |
| 20-02.4g | estimated p2 | 111.0 | MHz |
| 20-02.4h | g_m6/(2 pi C_L) | 159.2 | MHz |
| 20-02.4i | GBW | 53.05 | MHz |
| 20-02.4j | RHP zero | 530.5 | MHz |
| 20-02.4k | crossover | 47.69 | MHz |
| 20-02.4l | PM | 62.3 | ° |
| 20-02.4m | gain margin | 20.3 | dB |
| 20-02.4n | pole-splitting error | 3 | % |
| 20-02.4o | error of g_m6/C_L | 39 | % |
| 20-02.5a | IC of the PMOS M6 | 5.64 | — |
| 20-02.5b | f_T of the PMOS M6 | 0.936 | GHz |
| 20-02.5c | p2 bound | 215.9 | MHz |
| 20-02.5d | g_m6 | 2.493 | mS |
| 20-02.5e | C_1 | 454.1 | fF |
| 20-02.5f | I_6 | 249.3 | µA |
| 20-02.5g | current ratio to the NMOS design | 1.60 | — |
| 20-02.5h | f_T ratio, NMOS to PMOS | 3.3 | — |
| 20-02.6a | R_z for a zero at infinity | 641.8 | Ω |
| 20-02.6b | LHP zero with 1.2/g_m6 | 2.07 | GHz |
| 20-02.6c | lowest 1/g_m6 | 558.1 | Ω |
| 20-02.6d | highest 1/g_m6 | 755.1 | Ω |
| 20-02.6e | lowest R_z | 513.4 | Ω |
| 20-02.6f | highest R_z | 770.2 | Ω |
| 20-02.6g | worst RHP zero | 1.098 | GHz |
| 20-02.6h | worst LHP zero | 1.251 | GHz |
| 20-02.6i | worst phase cost | 2.28 | ° |
| 20-02.6j | triode W/L | 43.3 | — |
| 20-02.6k | largest 1/g_m6 - R_z | 241.6 | Ω |
| 20-02.6l | largest R_z - 1/g_m6 | 212.1 | Ω |
| 20-02.7i | follower time constant | 3.183 | ns |
| 20-02.7j | largest linear step | 0.1111 | V |
| 20-02.7a | slewing time, 0.2 V | 2.55 | ns |
| 20-02.7b | linear time, 0.2 V | 20.12 | ns |
| 20-02.7c | total, 0.2 V | 22.66 | ns |
| 20-02.7d | slewing time, 1 V | 25.46 | ns |
| 20-02.7e | linear time, 1 V | 14.99 | ns |
| 20-02.7f | total, 1 V | 40.46 | ns |
| 20-02.7g | SR for 30 ns | 60.9 | V/µs |
| 20-02.7h | implied g_m/I_D | 10.3 | S/A |
| 20-02.8a | minimum I_6 at 5 pF | 195.5 | µA |
| 20-02.8b | rising-edge SR at 5 pF | 27.0 | V/µs |
| 20-02.9a | q at IC = 0.1 | 0.0916 | — |
| 20-02.9b | V_DS,sat at IC = 0.1 | 0.104 | V |
| 20-02.9c | q at IC = 1 | 0.618 | — |
| 20-02.9d | V_DS,sat at IC = 1 | 0.120 | V |
| 20-02.9e | q at IC = 10 | 2.70 | — |
| 20-02.9f | V_DS,sat at IC = 10 | 0.202 | V |
| 20-02.9g | swing at IC = 1 | 0.660 | V |
| 20-02.9h | swing at IC = 10 | 0.496 | V |
| 20-02.9i | swing lost | 0.164 | V |
| 20-02.10a | PSRR- at 10 kHz | 67.9 | dB |
| 20-02.10b | PSRR- at 100 kHz | 53.6 | dB |
| 20-02.10c | frequency of 40 dB | 484.5 | kHz |
| 20-02.10d | asymptote estimate | 500 | kHz |
| 20-02.10e | asymptote error | 3 | % |
| 20-02.11a | mirror capacitance | 42.5 | fF |
| 20-02.11b | g_m3 | 106.0 | µS |
| 20-02.11c | mirror pole | 396.9 | MHz |
| 20-02.11d | mirror zero | 793.8 | MHz |
| 20-02.11e | phase cost | 3.13 | ° |
| 20-02.11f | corrected PM | 64.5 | ° |
| 20-02.12a | a_1 | 4.889 | µs |
| 20-02.12b | a_2 | 7.321e-15 | s² |
| 20-02.12c | a_3 | 4.181e-25 | s³ |
| 20-02.12d | p3 from a_2/a_3 | 2.787 | GHz |
| 20-02.12e | p3 capacitor form | 2.777 | GHz |
| 20-02.12f | exact p3 | 2.676 | GHz |
| 20-02.13a | p2 estimate | 448.9 | MHz |
| 20-02.13b | p3 estimate | 103.5 | MHz |
| 20-02.13c | damping estimate | 0.240 | — |
| 20-02.13d | natural frequency estimate | 215.5 | MHz |
| 20-02.13e | gain-margin estimate | 6.3 | dB |
| 20-02.13f | exact crossover | 52.76 | MHz |
| 20-02.13g | exact PM | 82.3 | ° |
| 20-02.13h | exact damping | 0.255 | — |
| 20-02.13i | exact natural frequency | 212.9 | MHz |
| 20-02.13j | exact gain margin | 4.64 | dB |
| 20-02.13k | natural-frequency error | 1.2 | % |
| 20-02.13l | damping error | 6 | % |
| 20-02.13m | gain-margin optimism | 1.7 | dB |
| 20-02.14a | GBW | 79.6 | MHz |
| 20-02.14b | closed-loop bandwidth | 26.5 | MHz |
| 20-02.14c | boosted gain | 40400 | — |
| 20-02.14d | static error | 0.0074 | % |
| 20-02.14e | tail amplitude | 0.75 | % |
| 20-02.14f | tail time to 0.01 % | 68.7 | ns |
| 20-02.14g | ideal single-pole time | 55.3 | ns |
| 20-02.14h | exact, f_ub = 10 MHz | 83.6 | ns |
| 20-02.14i | exact, f_ub = 100 MHz | 55.4 | ns |
| 20-02.15a | ratio per cycle, C_r = 0.2 pF | 0.8 | — |
| 20-02.15b | cycles, C_r = 0.2 pF | 21 | — |
| 20-02.15c | time, C_r = 0.2 pF | 420 | ns |
| 20-02.15d | ratio per cycle, C_r = 0.1 pF | 0.889 | — |
| 20-02.15e | cycles, C_r = 0.1 pF | 40 | — |
| 20-02.15f | time, C_r = 0.1 pF | 800 | ns |
| 20-02.16a | g_m3 | 5.027 | mS |
| 20-02.16b | C_m1 | 0.398 | pF |
| 20-02.16c | C_m2 | 0.199 | pF |
| 20-02.16d | exact PM | 60.0 | ° |
| 20-02.16e | exact crossover | 19.33 | MHz |
| 20-02.16f | exact gain margin | 12.2 | dB |
| 20-02.16g | two-stage g_m6 | 2.513 | mS |
| 20-02.16h | transconductance ratio | 2.0 | — |
| 20-02.17a | figure of merit | 500 | MHz·pF/mA |
| 20-02.17b | implied g_m/I_D, (a) | 6.28 | S/A |
| 20-02.17c | implied g_m/I_D, (b) | 251 | S/A |
| 20-02.17d | minimum input-limited SR | 42.2 | V/µs |
| 20-02.17e | ratio to the weak-inversion limit | 8.4 | — |
| 20-02.17f | weak-inversion limit | 29.8 | S/A |
