# Course 22 · Final Exam Solutions

Exam: [README.md](README.md). Every number below is recomputed by [verify_22_exam.py](../verify/verify_22_exam.py). About half the values are recomputed by a second route, listed below; the rest are closed-form re-evaluations of the same formulas:

- Questions 1 and 8: efficiencies and crossovers by numerical optimization and root finding, and the hold-up time by integrating the constant-power discharge;
- Questions 2, 3 and 6(d): ripples, RMS currents and discontinuous-conduction duty cycles from sampled switching waveforms over one period;
- Question 4: duty cycles by solving volt-second balance, and the clamp energy by integrating the clamp's voltage times its current;
- Question 5: the inductance from the stored field energy, and core loss by integrating the iGSE over sampled flux waveforms;
- Questions 7 and 13(b): the loop by evaluating the transfer functions numerically, the current-mode ratio by iterating the peak-current map, and the right-half-plane zero by linearizing the averaged boost numerically;
- Question 9: the pulse and the CC/CV charge by integrating the cell model in time;
- Questions 10 and 14: the busbar by summing discrete taps, the summed ripple by adding shifted phase currents, and the first droop by simulating the L–C network;
- Questions 11 and 12: torques by sweeping slip, phasors by complex arithmetic, fault currents through symmetrical components, and frequency by integrating the swing equation with governors;
- Question 13: the charging losses by integrating $i^2R$, and the optimal flux swing by numerical minimization.

---

## Solutions

### Solution 1

(a) $P_{in} = 1200/0.965$ = **1243.5** W, so the loss is **43.52** W. At 97.5%, $P_{in}$ = 1230.8 W and the loss is **30.77** W. One point of efficiency removes **12.75** W, **29.3**% of the loss: near 100%, $dP_{loss}/d\eta = -P_{out}/\eta^2$ makes each point worth about $P_{out}$/100.

(b) The LDO's input current is the load plus its quiescent current, 15.025 mA, so

$$
\eta_{LDO} = \frac{1.2 \times 15}{3.6 \times 15.025} = \mathbf{33.28}\ \%,
$$

and the battery current is **15.025** mA. The buck draws $1.2 \times 15\ \text{mA}/(0.9 \times 3.6)$ = **5.556** mA. The LDO takes **2.70** times as much: an LDO's efficiency can never beat $V_{out}/V_{in}$ = 33.3%.

(c) The efficiency $VI/(VI + P_0 + aI + RI^2)$ is highest where the loss per ampere $P_0/I + a + RI$ is lowest, at $I^* = \sqrt{P_0/R} = \sqrt{0.3/0.012}$ = **5.00** A, where $RI^{*2} = P_0$. The loss is 0.3 + 0.1 + 0.3 = 0.7 W on 9 W out, so η = 9/9.7 = **92.78**%. At 20 A the loss is 0.3 + 0.4 + 4.8 = 5.5 W and η = 36/41.5 = **86.75**%. With two phases, $2P_0 + aI + RI^2/2$ = 0.6 + 0.4 + 2.4 = 3.4 W and η = 36/39.4 = **91.37**%. Two phases win once the conduction they save, $RI^2(1 - \tfrac12)$, exceeds the extra $P_0$: above $I = \sqrt{2P_0/R}$ = **7.07** A. This is phase shedding.

(d) The capacitor must supply $Pt$ = 60 J between 54 and 40 V:

$$
C = \frac{2Pt}{V_1^2 - V_2^2} = \frac{2 \times 3000 \times 0.02}{54^2 - 40^2} = \frac{120}{1316} = \mathbf{91.19}\ \text{mF}.
$$

It uses $1 - (40/54)^2$ = **45.1**% of its stored energy: energy goes as $V^2$, so the top quarter of the voltage range (54 to 40 V) holds 45.1% of the energy, and the **55**% left below 40 V is stranded by the converter's minimum input voltage.

### Solution 2

(a) $D$ = 1.0/5 = 0.2.

$$
\Delta i_L = \frac{V(1 - D)}{f_sL} = \frac{1.0 \times 0.8}{2\ \text{MHz} \times 220\ \text{nH}} = \frac{0.8}{0.44} = \mathbf{1.818}\ \text{A},
$$

so $r$ = **0.303** and the peak is 6 + 0.909 = **6.909** A. The capacitive ripple is $\Delta i_L/(8f_sC) = 1.818/(8 \times 2\ \text{MHz} \times 47\ \mu\text{F})$ = **2.418** mV. A 2 mΩ ESR alone adds $\Delta i_L \times$ ESR = **3.64** mV, more than the capacitance does. The two do not simply add, because the ESR term peaks with the current and the capacitive term a quarter cycle later, so the combined ripple lies between the larger of the two and their sum.

(b) $I_{L,rms} = I\sqrt{1 + r^2/12} = 6\sqrt{1 + 0.0918/12}$ = **6.023** A. Each switch carries the inductor current for its share of the period: $I_{HS} = \sqrt{0.2} \times 6.023$ = **2.694** A and $I_{LS} = \sqrt{0.8} \times 6.023$ = **5.387** A. The input capacitor carries the pulsed switch current minus its average:

$$
I_{C_{in}} = I\sqrt{D(1 - D) + Dr^2/12} = 6\sqrt{0.16 + 0.0015} = \mathbf{2.411}\ \text{A}.
$$

(c) $R_{eq} = DR_{HS} + D'R_{LS} + R_L = 0.2 \times 12 + 0.8 \times 5 + 3$ = **9.4** mΩ, the conduction loss is $I^2R_{eq} = 36 \times 0.0094$ = **0.338** W, and with $R$ = 1/6 Ω,

$$
\eta = \frac{1}{1 + R_{eq}/R} = \frac{1}{1 + 0.0564} = \mathbf{94.66}\ \%.
$$

To hold 1.0 V, solve $V = DV_{in} - I(DR_{HS} + D'R_{LS} + R_L)$ for $D$:

$$
D = \frac{V + I(R_{LS} + R_L)}{V_{in} - I(R_{HS} - R_{LS})} = \frac{1.048}{4.958} = \mathbf{0.2114}.
$$

The loop finds this duty cycle automatically; the model shows the converter needs about 6% more duty cycle than ideal.

(d) $I_{crit} = \Delta i_L/2$ = **0.909** A. At 0.4 A, $R$ = 2.5 Ω and

$$
K = \frac{2L}{RT_s} = \frac{2 \times 220\ \text{nH} \times 2\ \text{MHz}}{2.5} = \mathbf{0.352},
$$

below $K_{crit} = 1 - D$ = 0.8, so the converter is discontinuous. The sheet's $M = 2/(1 + \sqrt{1 + 4K/D_1^2})$ rearranges to $\sqrt{1 + 4K/D_1^2} = (2 - M)/M$; squaring, $4K/D_1^2 = ((2 - M)^2 - M^2)/M^2 = 4(1 - M)/M^2$, so $M^2 = D_1^2(1 - M)/K$. With $M$ = 0.2, $D_1 = M\sqrt{K/(1 - M)} = 0.2\sqrt{0.44}$ = **0.1327**. Volt-second balance gives $D_2 = D_1(V_{in} - V)/V$ = **0.5307**, and the peak is $(V_{in} - V)D_1T_s/L = 4 \times 0.1327 \times 0.5\ \mu\text{s}/220\ \text{nH}$ = **1.206** A. Check: the average current $\tfrac12 \times 1.206 \times (0.1327 + 0.5307)$ = 0.400 A. ✓

### Solution 3

(a) $D = 1 - 3/12$ = **0.75**, $I_L = I/D'$ = **2.00** A, $\Delta i_L = V_{in}DT_s/L = 3 \times 0.75 \times 1\ \mu\text{s}/4.7\ \mu\text{H}$ = **0.479** A, and the output ripple (the capacitor alone supplies the load while the switch is on) is $ID/(f_sC) = 0.5 \times 0.75/(1\ \text{MHz} \times 22\ \mu\text{F})$ = **17.05** mV.

(b) Only the winding resistance $R_L$ = 50 mΩ is lossy, and it carries $I_L$ all the time. With $R$ = 24 Ω,

$$
\eta = \frac{1}{1 + R_L/(D'^2R)} = \frac{1}{1 + 0.05/(0.0625 \times 24)} = \mathbf{96.77}\ \%,
$$

and $V = (V_{in}/D')\eta$ = **11.61** V. The gain with resistance is $M = D'/(D'^2 + R_L/R)$; setting it to 4 gives $D'^2 - 0.25D' + 0.002083 = 0$, whose larger root is $D'$ = 0.2414, so $D$ = **0.7586** and η = $D'V/V_{in}$ = **96.55**%. The largest gain is $M_{max} = \tfrac12\sqrt{R/R_L} = \tfrac12\sqrt{480}$ = **10.95**, at $D' = \sqrt{R_L/R}$ = 0.0456, $D$ = **0.9544**. Beyond that, more duty cycle lowers the output, and a controller that keeps pushing latches up at maximum duty.

(c) $\lvert V\rvert = (D/D')V_{in}$ gives $D$ = 12/17 = **0.7059**. The inductor carries $I/D'$ = 0.3/0.2941 = **1.020** A, the switch blocks $V_{in} + \lvert V\rvert$ = **17** V, and the input current is $DI_L$ = **0.720** A, equal to $P/V_{in}$ = 3.6/5. ✓ The inductor carries $1/D'$ times the load current: at large step-up ratios the buck-boost's currents grow as $1/D'$.

(d) $R$ = 600 Ω, so $K = 2L/(RT_s) = 2 \times 4.7\ \mu\text{H}/(600 \times 1\ \mu\text{s})$ = **0.01567**, and $K_{crit} = DD'^2 = 0.75 \times 0.0625$ = **0.0469**. $K < K_{crit}$, so it is discontinuous. From $M(M - 1) = D^2/K$, $D = \sqrt{KM(M - 1)} = \sqrt{0.01567 \times 12}$ = **0.4336**, well below the CCM value of 0.75.

### Solution 4

(a) From $V = (V_{in}/n)(D/D')$, $D/D' = nV/V_{in} = 36/V_{in}$: at 36 V, $D/D'$ = 1 and $D$ = **0.500**; at 48 V, 0.75 and $D$ = **0.4286**; at 72 V, 0.5 and $D$ = **0.3333**. Off, the switch sees the input plus the reflected output, $V_{in} + nV$ = 72 + 36 = **108** V.

(b) The reflected voltage is $V_R = nV$ = 36 V, so

$$
t_c = \frac{L_{lk}I_{pk}}{V_c - V_R} = \frac{1.2\ \mu\text{H} \times 2.5}{24} = \mathbf{125}\ \text{ns}, \qquad E_c = \frac12L_{lk}I_{pk}^2\,\frac{V_c}{V_c - V_R} = 3.75\ \mu\text{J} \times 2.5 = \mathbf{9.375}\ \mu\text{J}.
$$

The clamp loss is $9.375\ \mu\text{J} \times 150\ \text{kHz}$ = **1.41** W, and the drain peaks at $V_{in} + V_c$ = **132** V. The leakage stores **3.75** µJ; the clamp absorbs **2.5** times as much, because the magnetizing inductance keeps pushing current into the clamp until the leakage current has fallen.

(c) $V = DV_{in}/n$ gives $n = DV_{in}/V = 0.495 \times 36/3.3$ = **5.40**, and at 72 V, $D = nV/V_{in}$ = **0.2475**. Reset needs $D \le 1/(1 + N_3/N_1) = 1/1.8$ = **0.556**. The switch blocks $V_{in}(1 + N_1/N_3) = 72 \times 2.25$ = **162** V at 72 V. Fewer reset turns allow a longer duty cycle, at the price of a higher switch voltage.

(d) In normal operation $V_{in}D = nV$ = 17.82 V, whatever the input, so

$$
\Delta B = \frac{V_{in}DT_s}{N_1A_e} = \frac{17.82 \times 3.333\ \mu\text{s}}{15 \times 50\ \text{mm}^2} = \mathbf{0.0792}\ \text{T}.
$$

A transient that drives $D$ to 0.556 at 72 V gives $72 \times 0.556 \times 3.333\ \mu\text{s}/(750\ \text{mm}^2)$ = **0.178** T, **2.24** times the normal swing. The core must take it without saturating, or the controller must limit the volt-seconds per cycle. The magnetizing ripple is $17.82 \times 3.333\ \mu\text{s}/250\ \mu\text{H}$ = **0.238** A.

### Solution 5

(a) The reluctances (in H⁻¹, the same as A/Wb) are

$$
\mathcal R_c = \frac{\ell_e}{\mu_r\mu_0A_e} = \frac{0.06}{2500 \times 4\pi \times 10^{-7} \times 80 \times 10^{-6}} = \mathbf{2.387} \times 10^5, \qquad \mathcal R_g = \frac{g}{\mu_0A_e} = \mathbf{7.958} \times 10^6 .
$$

The gap dominates. $L = N^2/(\mathcal R_c + \mathcal R_g) = 900/8.196 \times 10^6$ = **109.8** µH, and $\mu_e = \mu_r/(1 + \mu_rg/\ell_e) = 2500/34.33$ = **72.82**.

(b) $I_{sat} = B_{max}NA_e/L = 0.32 \times 30 \times 80 \times 10^{-6}/109.8\ \mu\text{H}$ = **6.994** A, and $W = \tfrac12LI_{sat}^2$ = **2.686** mJ. The gap holds $g/(g + \ell_e/\mu_r) = 0.8/0.824$ = **97.1**% of it: the gap is where the energy lives, and the core only guides the flux.

(c) $P_v = kf^\alpha B_{pk}^\beta = 3.0 \times 10^7 \times 0.1^{2.5}$ = **94.87** kW/m³, and with $V_e$ = 4.8 cm³ the loss is **0.455** W. For the triangle, $\Delta B$ = 0.2 T and

$$
P_v = k_i(\Delta B)^\beta f^\alpha\left[D^{1 - \alpha} + (1 - D)^{1 - \alpha}\right], \qquad k_i(\Delta B)^\beta f^\alpha = 0.1873 \times 0.01789 \times 10^7 = 33.51\ \text{kW/m}^3 .
$$

At $D$ = 0.5 the bracket is $2 \times 0.5^{-0.4}$ = 2.639, giving **88.4** kW/m³, **0.932** times the sinusoid. At $D$ = 0.1 it is $0.1^{-0.4} + 0.9^{-0.4}$ = 3.555, giving **119** kW/m³, **1.256** times: the fast edge's high $dB/dt$ costs more than the slow edge saves, so the sinusoidal Steinmetz figure underestimates loss at extreme duty cycles.

(d) $\delta = \sqrt{\rho/(\pi f\mu_0)} = \sqrt{22.66 \times 10^{-9}/(\pi \times 2 \times 10^5 \times 4\pi \times 10^{-7})}$ = **0.1694** mm, so $\Delta = 0.12/0.1694$ = **0.708** and

$$
F_R \approx 1 + \frac{5M^2 - 1}{45}\Delta^4 = 1 + \frac{44}{45} \times 0.2518 = \mathbf{1.246}.
$$

Dowell's full formula gives **1.244**, so the approximation is good at this Δ. The three layers cost 25% more resistance than DC; thicker foil would lower $R_{dc}$ but raise $F_R$ as $\Delta^4$.

### Solution 6

(a) $P_{ov} = \tfrac12VI(t_{on} + t_{off})f_s = \tfrac12 \times 380 \times 12 \times 40\ \text{ns} \times 80\ \text{kHz}$ = **7.30** W, and the conduction loss is $8^2 \times 0.04$ = **2.56** W. At 380 V, overlap dominates.

(b) A hard turn-on dissipates $Q_{oss}V$ = 70 nC × 380 V = **26.6** µJ, so **2.13** W. An $E_{oss}$-only estimate gives 9 µJ, **0.72** W, about a third: the switch burns its own stored $E_{oss}$ and also the $Q_{oss}V - E_{oss}$ lost while the bus charges the other switch's output capacitance through it. Reverse recovery adds $Q_{rr}V$ = 90 nC × 380 V = **34.2** µJ, **2.74** W. A GaN HEMT has no minority-carrier diode, so its reverse-recovery loss is **0** W, which is what makes hard-switched totem-pole PFC practical.

(c) $R \cdot Q_{oss}$ = 40 mΩ × 70 nC = 2.8 × 10⁻⁹ Ω·C, so $(RQ)Vf_s$ = 0.0851 W·Ω and

$$
R^* = \frac{\sqrt{(RQ)Vf_s}}{I_{rms}} = \frac{0.2918}{8} = \mathbf{36.5}\ \text{m}\Omega, \qquad P_{min} = 2I_{rms}\sqrt{(RQ)Vf_s} = \mathbf{4.67}\ \text{W}.
$$

At 160 kHz the minimum rises by √2 to **6.60** W. A 20 mΩ device at 80 kHz loses $64 \times 0.02 + 0.0851/0.02$ = 1.28 + 4.26 = **5.54** W: halving the resistance doubles the output charge, and the switch ends up worse. Only a better figure of merit lowers the minimum.

(d) ZVS needs $I \ge 2Q_{oss}/t_d$ = 16 nC/8 ns = **2.00** A flowing the other way when the high side turns on. The valley $I - \Delta i_L/2$ must reach −2 A, so $\Delta i_L = 2(5 + 2)$ = **14.0** A and

$$
L = \frac{V(1 - D)}{f_s\Delta i_L} = \frac{12 \times 0.75}{400\ \text{kHz} \times 14} = \mathbf{1.607}\ \mu\text{H}.
$$

The peak is 5 + 7 = **12.0** A and the RMS $5\sqrt{1 + 2.8^2/12}$ = **6.43** A, so the conduction loss exceeds that of a ripple-free 5 A by a factor of $(6.43/5)^2$ = **1.653**. TCM trades that conduction loss for zero turn-on loss.

### Solution 7

(a) $f_0 = 1/(2\pi\sqrt{LC}) = 1/(2\pi\sqrt{2.35 \times 10^{-10}})$ = **10.38** kHz, $Q = 0.12\sqrt{940}$ = **3.68**, and $G_{vd}(0) = V_g$ = 12, or **21.58** dB. At 40 kHz, $\omega^2LC$ = 14.844 and $\omega L/R$ = 1.047, so the denominator is −13.844 + j1.047: $\lvert G_{vd}\rvert = 12/13.884$ = **0.864** at **−175.7**°.

(b) $B = \text{PM} - 90° - \varphi_p = 55 - 90 + 175.67$ = **140.7**°, and $k = \tan((70.34° + 90°)/2) = \tan 80.17°$ = **5.77**. The zeros go at 40/5.770 = **6.93** kHz and the poles at 40 × 5.770 = **230.8** kHz, below $f_s/2$. The compensator must have $\lvert G_c\rvert = V_M/(\lvert G_{vd}\rvert H)$ = **1.157** at crossover, and each zero–pole pair contributes $k$ there, so $\omega_I = 1.157\,\omega_c/k^2$ and $f_I$ = 1.157 × 40 kHz/33.30 = **1.390** kHz. As a check, not a required answer: evaluating $T(j\omega)$ numerically confirms the crossover at **40.0** kHz with a **55.0**° margin.

(c) $m_1 = (12 - 7.5)/3.3\ \mu\text{H}$ = **1.364** A/µs and $m_2 = 7.5/3.3\ \mu\text{H}$ = **2.273** A/µs, so α = $-m_2/m_1$ = **−1.67**: with $D$ = 0.625 > 0.5, each perturbation grows and alternates, the subharmonic oscillation. Stability needs $m_2 - m_a < m_1 + m_a$, that is $m_a > (m_2 - m_1)/2$ = **0.455** A/µs. With $m_a = m_2/2$ = 1.136 A/µs, $\alpha = -(2.273 - 1.136)/(1.364 + 1.136)$ = **−0.455**, and after five cycles a perturbation is $\lvert\alpha\rvert^5$ = **0.0194** of its initial size, alternating in sign.

(d) $\Delta V \approx \Delta I/(2\pi f_cC) = 5/(2\pi \times 40\ \text{kHz} \times 470\ \mu\text{F})$ = **42.3** mV. The delay costs $360° \times f_ct_d = 360 \times 40\ \text{kHz} \times 1\ \mu\text{s}$ = **14.4**°, leaving **40.6**° of the 55° margin. Keeping the cost to 10° needs $f_c \le 10/(360 \times 1\ \mu\text{s})$ = **27.8** kHz, which would raise the droop by 44%: delay, not the plant, then limits the transient.

### Solution 8

(a) $\eta = 0.9 \times 0.8/1.0$ = **72.0**%, and the battery supplies $80\ \text{mW}/(0.72 \times 3.8\ \text{V})$ = **29.24** mA. A buck straight to 0.8 V draws $80/(0.87 \times 3.8)$ = **24.20** mA, so the cascade costs **5.04** mA more (21%). The cascade buys the LDO's ripple rejection; whether that is worth 21% of the rail's battery current depends on what the rail feeds.

(b) Setting $P_{PWM} = P_{PFM}$: $0.35I^2 + 0.06I + 1.9\ \mu\text{W} - 12\ \text{mW} = 0$, so $I$ = **118.3** mA. At 0.5 mA ($P_{out}$ = 0.5 mW), PWM loses 12.0 mW for **4.00**% while PFM loses 1.9 + 30 + 0.125 = 32.0 µW for **93.98**%. At 200 mA, PWM loses 18.0 mW for **91.74**% and PFM 32.0 mW for **86.21**%: above the crossover the order reverses.

(c) The daily energy terms are:

- sleep: 20 µW × 84 600 s/0.8 = **2.115** J;
- active: 6 mW × 1500 s/0.9 = **10.00** J;
- radio: 45 mW × 300 s/0.88 = **15.34** J;
- quiescent: 3.8 V × 1.5 µA × 86 400 s = **0.4925** J.

The total is **27.95** J/day, an average of **0.3235** mW. The cell holds 0.150 Ah × 3.8 V × 3600 = 2052 J, so it lasts **73.4** days. The radio's 5 minutes cost more than the other 23 h 55 min together; a usage profile, not a sleep current, decides battery life.

(d) $I_C = C\,dV/dt = 47\ \mu\text{F} \times 0.3\ \text{V}/15\ \mu\text{s}$ = **0.94** A on top of the load. AVS saves $1 - (0.88/0.95)^2$ = **14.2**% of the dynamic power. The domain breaks even after

$$
t_{be} = \frac{CV^2 + E_{state}}{P_{leak}} = \frac{3.872\ \text{nJ} + 300\ \text{nJ}}{2\ \text{mW}} = \mathbf{151.9}\ \mu\text{s},
$$

so idle periods shorter than that should not be gated. Here state retention, not the capacitance, sets the break-even.

### Solution 9

(a) LiC₆ stores one lithium per six carbons, $M$ = 6 × 12.011 = 72.07 g per mole of lithium:

$$
q_{th} = \frac{F}{3.6M} = \frac{96\,485}{3.6 \times 72.07} = \mathbf{371.9}\ \text{mAh/g}.
$$

The cell holds 4.2 Ah × 3.6 V = **15.12** Wh, and 6 A is **1.43**C.

(b) $v(t) = V_{OC} - IR_0 - IR_1(1 - e^{-t/\tau_1})$: at 0⁺, 3.8 − 0.12 = **3.680** V; at 50 s, 3.680 − 0.075 × 0.632 = **3.633** V; at 200 s, 3.680 − 0.075 × 0.982 = **3.606** V. At the start of a pulse only $R_0$ acts, so the cell can deliver $(3.8 - 3.0)/0.040$ = **20.0** A; held long enough, $R_0 + R_1$ acts and the limit falls to 0.8/0.065 = **12.31** A. A pulse rating and a continuous rating are different numbers.

(c) $Q$ = 15 120 C and $dV_{OC}/dz$ = 0.5 V, so $C_{eff} = Q/(dV_{OC}/dz)$ = **30 240** F and the CV time constant is $RC_{eff}$ = 1814 s = **30.24** min. With $I_{cc}$ = 2.94 A, CV begins at $V_{OC} = 4.2 - 2.94 \times 0.06$ = 4.0236 V, that is $z_{cv}$ = **0.647**. The CC phase takes (0.6472 − 0.2) × 4.2 Ah/2.94 A = **38.33** min. The CV phase decays from 2.94 A to $I_{term}$ = 0.21 A in $\tau\ln(14)$ = **79.81** min, for a total of **118.1** min. Charging ends at $V_{OC} = 4.2 - 0.21 \times 0.06$ = 4.1874 V, $z$ = **0.975**, having added $(I_{cc} - I_{term})\tau$ = **1.376** Ah in CV, which matches $(0.9748 - 0.6472) \times 4.2$ Ah. ✓ The CV phase takes two thirds of the time to deliver 42% of the charge.

(d) The offset integrates to 50 µA × 720 h = **36.0** mAh, 0.86% of capacity a month, which is why gauges re-anchor to OCV at rest. Capacity learning gives $Q_{max} = \Delta q/(z_1 - z_2) = 2.1/0.55$ = **3.818** Ah, a state of health of **90.9**%.

### Solution 10

(a) At 54 V the rack draws 132 kW/54 V = **2444** A; at 800 V, **165.0** A. With the full current over the 80 µΩ loop the loss would be $2444^2 \times 80\ \mu\Omega$ = **478.0** W; tapped uniformly it is a third of that, **159.3** W. At 800 V the same bar loses $165^2 \times 80\ \mu\Omega/3$ = **0.726** W, $(800/54)^2$ = **219.5** times less, so the bar can be made far smaller. Per conductor,

$$
\frac{n_cV_{DC}}{2\sqrt3\,V_{LL}\cos\varphi} = \frac{3 \times 800}{2\sqrt3 \times 480 \times 0.95} = \mathbf{1.519},
$$

52% more power per conductor for DC.

(b) $D$ = 0.75/12 = **0.0625** and each phase carries **50.0** A. One phase's ripple is $V(1 - D)/(f_sL) = 0.75 \times 0.9375/(800\ \text{kHz} \times 100\ \text{nH})$ = **8.79** A. With $ND$ = 0.75 and $m$ = 0,

$$
\Delta I_\Sigma = \frac{V_{in}T}{L}\cdot\frac{(ND - m)(m + 1 - ND)}{N} = 150 \times \frac{0.75 \times 0.25}{12} = \mathbf{2.34}\ \text{A},
$$

**0.267** of one phase's ripple, at $Nf_s$ = **9.6** MHz. Twelve phases cancel most of the ripple and multiply its frequency, so the output capacitor's job shrinks on both counts.

(c) $Z_t = 30\ \text{mV}/400\ \text{A}$ = **75** µΩ. With $R_{LL}$ = 75 µΩ, the output at 600 A is $0.80 - 75\ \mu\Omega \times 600$ = **0.755** V. The bulk capacitance must carry the step until the loop responds: $C \ge \Delta I/(2\pi f_c\Delta V) = 400/(2\pi \times 300\ \text{kHz} \times 0.03)$ = **7.07** mF.

(d) $f_0 = 1/(2\pi\sqrt{0.8\ \text{pH} \times 80\ \mu\text{F}})$ = **19.89** MHz and $Z_0 = \sqrt{L/C}$ = **100** µΩ. The first droop is $\Delta IZ_0$: **30.0** mV for 300 A and **40.0** mV for 400 A, which fails the 30 mV allowance. Meeting it needs $C \ge L\Delta I^2/\Delta V^2 = 0.8\ \text{pH} \times 400^2/0.03^2$ = **142.2** µF of die capacitance (or less package inductance), and the $Z_0/2$ rule puts the droop-minimizing ESR at about $Z_0/2$ = **50** µΩ. (A simulation of the damped L–C network puts the exact minimum at **0.53** $Z_0$ ≈ **53** µΩ; the optimum is flat, so the rule is close enough.)

### Solution 11

(a) With no load, $E_a = V$, so ω = $V/k$ = **400** rad/s, **3820** rpm. At stall, $I = V/R_a$ = 192 A and $T = kI$ = **23.04** N·m. At 3 N·m, $I = T/k$ = **25.0** A and ω = $(V - IR_a)/k = (48 - 6.25)/0.12$ = **347.9** rad/s; the efficiency is $T\omega/(VI) = 347.9/400$ = **86.98**%. With no mechanical loss, a DC motor's efficiency is just $E_a/V$, its speed as a fraction of no-load speed.

(b) $n_s = 120 \times 50/8$ = 750 rpm, so $s$ = 22.5/750 = **0.030** and the rotor currents run at $sf$ = **1.50** Hz. The rotor copper loss is $sP_{ag}$ = **600** W, the mechanical power $(1 - s)P_{ag}$ = **19.4** kW, and the torque $P_{ag}/\omega_s = 20\,000/78.54$ = **254.6** N·m.

(c) ω_s = 188.5 rad/s and $\sqrt{R_{th}^2 + (X_{th} + X_2)^2} = \sqrt{0.09 + 3.24}$ = 1.8248 Ω. Then $s_{max}$ = 0.35/1.8248 = **0.1918**, at **1455** rpm, and

$$
T_{max} = \frac{3V_{th}^2}{2\omega_s(R_{th} + 1.8248)} = \frac{187\,500}{2 \times 188.5 \times 2.1248} = \mathbf{234.1}\ \text{N·m}.
$$

At $s$ = 1, $T = 3 \times 62\,500 \times 0.35/(188.5 \times (0.65^2 + 3.24))$ = **95.06** N·m, and at $s$ = 0.03 ($R_2/s$ = 11.67 Ω), $T$ = **79.25** N·m. Starting torque is only 41% of the peak; adding rotor resistance would move the peak toward standstill.

(d) $V$ = 4160/√3 = 2401.8 V per phase, so $\sin\delta = PX_s/(3VE_f) = 12 \times 10^6/20.175 \times 10^6$ = 0.5948 and δ = **36.50**°. The pull-out power is $3VE_f/X_s$ = **2.522** MW. From $\mathbf V = \mathbf E_f + jX_s\mathbf I_a$ with $\mathbf E_f$ lagging by δ,

$$
\mathbf I_a = \frac{2401.8 - 2800\angle{-36.50°}}{j8} = \frac{150.9 + j1665.4}{j8} = 208.2 - j18.87\ \text{A},
$$

so $\lvert\mathbf I_a\rvert$ = **209.0** A at a power factor of **0.996** lagging, and the motor draws $3 \times 2401.8 \times 18.87$ = **0.136** MVAr. Unity power factor puts $\mathbf I_a$ in phase with $\mathbf V$, so $\mathbf E_f = V - jX_sI$ and $E_f = \sqrt{V^2 + (X_sI)^2}$ with $I = P/(3V)$ = 208.2 A: **2923** V. More field current would make the motor supply reactive power, as a synchronous condenser does.

### Solution 12

(a) $I_b = S_b/(\sqrt3V_b) = 100\ \text{MVA}/(\sqrt3 \times 345\ \text{kV})$ = **167.3** A and $Z_b = V_b^2/S_b$ = **1190** Ω. The transformer's 0.09 pu on 75 MVA becomes $0.09 \times 100/75$ = **0.120** pu, and the line's 57.0 Ω is 57.0/1190.25 = **0.0479** pu, for a total of **0.1679** pu.

(b) $\sin\delta = PX/(V_1V_2) = 2.0 \times 0.1679/1.02$ = 0.3292, so δ = **19.22**° and cos δ = 0.9443. Then

$$
Q_1 = \frac{1.02^2 - 1.02 \times 0.9443}{0.1679} = \mathbf{0.460}\ \text{pu}, \qquad Q_2 = \frac{1.02 \times 0.9443 - 1}{0.1679} = \mathbf{-0.220}\ \text{pu}.
$$

The negative $Q_2$ means bus 2 must also supply reactive power into the line: the link absorbs $Q_1 - Q_2$ = **0.680** pu (its $I^2X$). The largest transfer is $V_1V_2/X$ = **6.08** pu, 608 MW. At 200 MW the link runs at a third of its steady-state limit yet already draws reactive power from both ends, mostly in the transformer, which is why heavily loaded links need voltage support.

(c) $I_f = 1/0.20$ = **5.00** pu = 5 × 167.3 A = **0.837** kA, and the fault MVA is 100/0.20 = **500** MVA. For a single-line-to-ground fault,

$$
I_a = \frac{3V_f}{Z_1 + Z_2 + Z_0} = \frac{3}{0.50} = \mathbf{6.00}\ \text{pu} = \mathbf{1.004}\ \text{kA},
$$

larger than the three-phase fault because $Z_0 < Z_1$, as near solidly grounded transformers. Breakers must be rated for the worse of the two.

(d) The machines store $E_k = HS$ = 4.5 s × 80 GVA = **360** GJ. The initial RoCoF is $-\Delta Pf_0/(2HS) = -1200 \times 60/(2 \times 4.5 \times 80\,000)$ = **−0.100** Hz/s, falling. The governors contribute $S/(Rf_0) = 30\,000/(0.05 \times 60)$ = 10 000 MW/Hz, so

$$
\Delta f_{ss} = -\frac{1200}{10\,000 + 1500} = \mathbf{-0.1043}\ \text{Hz},
$$

and the governors pick up $10\,000 \times 0.1043$ = **1043** MW, the load's damping the other 157 MW. Secondary control then restores 60 Hz.

### Solution 13

(a) KVL around the loop after the step gives $V = Ri + v_C$ with $i = C\,dv_C/dt$, so $RC\,dv_C/dt + v_C = V$ with $v_C(0) = 0$. Its solution is $v_C = V(1 - e^{-t/RC})$, and the current is $i = C\,dv_C/dt = (V/R)e^{-t/RC}$. Then

$$
E_R = \int_0^\infty i^2R\,dt = \frac{V^2}{R}\int_0^\infty e^{-2t/RC}dt = \frac{V^2}{R}\cdot\frac{RC}{2} = \frac12CV^2 ,
$$

in which $R$ cancels. The source delivers charge $CV$ at voltage $V$, so it supplies $CV^2$: half is stored and half is lost, whatever the resistance. In $N$ equal steps, each step charges $C$ through $R$ by $V/N$ from a source at the new level, which by the same integral dissipates $\tfrac12C(V/N)^2$; the $N$ steps dissipate $N \times \tfrac12C(V/N)^2 = \tfrac12CV^2/N$. For 40 nF to 0.9 V: one step loses $\tfrac12CV^2$ = **16.2** nJ, four steps lose 16.2/4 = **4.05** nJ, and the supply delivers $CV^2$ = **32.4** nJ to a one-step charge; at 10 000 wake-ups per second the loss is **162** µW, and with four steps **40.5** µW. This is why soft start does not save the charging energy (it only limits the current), and why stepped or adiabatic charging does.

(b) The averaged boost obeys $L\,d\langle i\rangle/dt = v_g - d'\langle v\rangle$ and $C\,d\langle v\rangle/dt = d'\langle i\rangle - \langle v\rangle/R$. Write $d' = D' - \hat d$, $\langle i\rangle = I_L + \hat\imath$, $\langle v\rangle = V + \hat v$, keep first-order terms and transform:

$$
sL\hat\imath = -D'\hat v + V\hat d, \qquad sC\hat v = D'\hat\imath - I_L\hat d - \hat v/R .
$$

Substitute $\hat\imath = (V\hat d - D'\hat v)/(sL)$ into the second, multiply by $sL$, and use the inductor's DC current $I_L = V/(D'R)$:

$$
\hat v\left(s^2LC + \frac{sL}{R} + D'^2\right) = \hat d\left(D'V - \frac{sLV}{D'R}\right) \quad\Rightarrow\quad G_{vd}(s) = \frac{V}{D'}\cdot\frac{1 - s\dfrac{L}{D'^2R}}{1 + s\dfrac{L}{D'^2R} + s^2\dfrac{LC}{D'^2}} .
$$

The numerator's root is at $s = +D'^2R/L$, in the right half plane. Physically, raising $d$ first starves the output (the inductor is connected to it for less of the cycle) before the extra inductor current arrives. For 5 V to 12 V at 2 A: $D$ = **0.5833**, $D'$ = 0.4167, $R$ = 6 Ω. The DC gain is $V/D'$ = **28.8** V (**29.19** dB), $f_0 = D'/(2\pi\sqrt{LC})$ = **5.32** kHz, $Q = D'R\sqrt{C/L}$ = **9.43**, and the zero sits at $D'^2R/(2\pi L)$ = **50.2** kHz. Crossover must stay well below the zero, around a fifth of it or less, even though the resonance is only a decade lower.

(c) $P = a\Delta B^\beta + b\Delta B^{-2}$, so

$$
\frac{dP}{d\Delta B} = \beta a\Delta B^{\beta - 1} - 2b\Delta B^{-3} = 0 \quad\Rightarrow\quad \Delta B_{opt} = \left(\frac{2b}{\beta a}\right)^{1/(\beta + 2)},
$$

and at the optimum $\beta P_{fe} = 2P_{cu}$, so $P_{fe}/P_{cu} = 2/\beta$. The second derivative is positive, so this is a minimum. Here $a = 3/0.2^{2.6}$ = **197.0** W/T^2.6 and $b = 1 \times 0.2^2$ = **0.0400** W·T². Then $\Delta B_{opt}$ = **0.1488** T, $P_{fe}$ = **1.390** W, $P_{cu}$ = **1.807** W and the total is **3.197** W, against 4.00 W at 0.2 T; the ratio is 2/2.6 = **0.769**. The optimum does not put equal loss in core and copper, as a common rule of thumb says.

(d) With $\mathbf V_r = V_r\angle0$, the delivered power $P + jQ = \mathbf V_r\mathbf I^*$ gives $\mathbf I = (P - jQ)/V_r$. Then

$$
\mathbf V_s = V_r + (R + jX)\frac{P - jQ}{V_r} = V_r + \frac{RP + XQ}{V_r} + j\,\frac{XP - RQ}{V_r} ,
$$

so the in-phase drop is $\Delta V = (RP + XQ)/V_r$ and the quadrature term $\delta V = (XP - RQ)/V_r$. Since $\lvert\mathbf V_s\rvert = \sqrt{(V_r + \Delta V)^2 + \delta V^2} \approx V_r + \Delta V + \delta V^2/(2(V_r + \Delta V))$, the first-order estimate is $V_r + \Delta V$. Here $\Delta V$ = 0.016 + 0.030 = **0.0460** and $\delta V$ = 0.080 − 0.006 = **0.0740**, so the estimate is **1.046** pu; exactly, $\lvert\mathbf V_s\rvert = \sqrt{1.046^2 + 0.074^2}$ = **1.0486** pu, and the corrected estimate $1.046 + 0.005476/2.092$ = **1.0486** pu matches it.

### Solution 14

(a) The module delivers 0.75 V × 2000 A = 1.5 kW, so it draws 1500/0.93 = **1613** W, loses **112.9** W and takes **33.6** A at 48 V. With a 97.5% first stage, the second must reach 0.93/0.975 = **95.4**% at 0.75 V and 2 kA. The 22-10 chain of 97.5% and 87.0% is **84.8**% efficient and draws 1500/0.8483 = **1768** W, so the claimed 93% would save **155** W of conversion loss.

(b) One 70 µm plane has $R_{sq} = \rho/t = 17.24\ \text{n}\Omega\text{·m}/70\ \mu\text{m}$ = **0.246** mΩ per square, and six in parallel 41.0 µΩ. The path is 25/50 = 0.5 square each way, so the loop is **41.0** µΩ. At 2000 A the drop is **82.1** mV, 11% of the rail, and the loss is $I^2R$ = **164** W. With $n$ planes per polarity the loss is $985/n$ W, below 150 W at **7** planes (**140.7** W).

(c) $Z_0 = \sqrt{0.4\ \text{pH}/150\ \mu\text{F}}$ = **51.6** µΩ, so a 1000 A step droops **51.6** mV, **6.89**% of 0.75 V, at the resonance $f_0$ = **20.5** MHz. A 5% allowance means $Z_t$ = 37.5 mV/1000 A = **37.5** µΩ, which needs $C \ge L\Delta I^2/\Delta V^2$ = **284** µF at this inductance. A module under the package shortens the board path but leaves the package and die loop, which sets the first droop. "Eliminates PDN droop" is false; at most the module shrinks the lower-frequency part of the impedance.

(d) The 150 W could be the efficiency gain over a conventional chain (part a: 155 W) or the lateral planes' $I^2R$ (part b: 164 W on six planes). These are different losses at different boundaries, so which applies, and whether both do, depends on where each efficiency is measured.

- *On 22-10's boundary they add.* In 22-10's Intel model the 87.0% covers the regulator alone, and the plane $I^2R$ is listed separately. The lateral regulator must then supply 1500 + 164 = 1664 W, and the chain draws $1664/0.8483$ = **1962** W, about **349** W more than the module's 1613 W (if the module's 93% is measured all the way to the die).
- *If the start-up's baseline was measured at the die,* the plane loss is already inside its efficiency, and adding the two savings would double-count it.

Either way, a saving quoted without its boundary cannot be checked. Questions for the chief architect, with what a strong answer contains:

1. **"Where exactly is 93% measured, from which terminal to which, at what load and temperature?"** *Strong:* 48 V at the module input to the die bumps (or to the module output, stated as such), at 25%, 50% and 100% load, at the module's operating temperature, with the measurement method. *Evasive:* "peak efficiency" with no boundary.
2. **"What is your lateral baseline: how many planes, what copper weight, what distance, and which losses does it include?"** *Strong:* a named reference design with the plane stackup and a loss breakdown that adds to the claimed saving. *Evasive:* "150 W, per our simulation."
3. **"What does the die see for a 1000 A step, and what package inductance and die capacitance did you assume?"** *Strong:* a measured or simulated first droop and impedance profile against a target impedance, with the loop bandwidth of the module. *Evasive:* "no droop because we are under the package."
4. **"How do you remove 113 W from under the package, and what happens to the board's power and signal routing there?"** *Strong:* a thermal stack with the cooling path, junction temperatures at full load, and how the module coexists with the package's signal escape and the board's backside components. *Evasive:* "the cold plate handles it."

**Rubric for (d), 3 points.**

- **1 point:** identifies the two candidate savings with numbers (about 155 W of conversion loss and about 164 W of plane $I^2R$), and explains that whether they add depends on where each efficiency is measured: additive on 22-10's boundary (about 349 W), double-counted if the baseline was measured at the die.
- **0.5 point for each of four questions** that names a measurable boundary or quantity and says what a strong answer contains: the efficiency boundary, load and temperature; the baseline stackup and loss breakdown; the first droop with the assumed $L$ and $C$; the thermal path for about 113 W and the routing impact.
- **0.25 point** for a relevant question without strong-answer content.

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X22.1a | input power at 96.5% | 1243.5 | W |
| X22.1b | loss at 96.5% | 43.52 | W |
| X22.1c | loss at 97.5% | 30.77 | W |
| X22.1d | loss reduction | 12.75 | W |
| X22.1e | loss reduction | 29.3 | % |
| X22.1f | LDO efficiency | 33.28 | % |
| X22.1g | LDO battery current | 15.025 | mA |
| X22.1h | buck battery current | 5.556 | mA |
| X22.1i | ratio of battery currents | 2.70 |  |
| X22.1j | current of peak efficiency | 5.00 | A |
| X22.1k | peak efficiency | 92.78 | % |
| X22.1l | efficiency at 20 A, one phase | 86.75 | % |
| X22.1m | efficiency at 20 A, two phases | 91.37 | % |
| X22.1n | one-to-two-phase crossover | 7.07 | A |
| X22.1o | hold-up capacitance | 91.19 | mF |
| X22.1p | stored energy used | 45.1 | % |
| X22.1q | energy left below 40 V | 55 | % |
| X22.2a | inductor ripple | 1.818 | A |
| X22.2b | ripple ratio | 0.303 |  |
| X22.2c | peak inductor current | 6.909 | A |
| X22.2d | capacitive output ripple | 2.418 | mV |
| X22.2e | ESR ripple | 3.64 | mV |
| X22.2g | inductor RMS current | 6.023 | A |
| X22.2h | high-side RMS current | 2.694 | A |
| X22.2i | low-side RMS current | 5.387 | A |
| X22.2j | input-capacitor RMS current | 2.411 | A |
| X22.2k | equivalent resistance | 9.4 | mΩ |
| X22.2l | conduction loss | 0.338 | W |
| X22.2m | efficiency | 94.66 | % |
| X22.2n | duty cycle with losses | 0.2114 |  |
| X22.2o | critical current | 0.909 | A |
| X22.2p | K at 0.4 A | 0.352 |  |
| X22.2q | D1 | 0.1327 |  |
| X22.2r | D2 | 0.5307 |  |
| X22.2s | DCM peak current | 1.206 | A |
| X22.3a | boost duty cycle | 0.75 |  |
| X22.3b | inductor current | 2.00 | A |
| X22.3c | inductor ripple | 0.479 | A |
| X22.3d | output ripple | 17.05 | mV |
| X22.3e | efficiency at D = 0.75 | 96.77 | % |
| X22.3f | output at D = 0.75 | 11.61 | V |
| X22.3g | duty cycle for 12 V | 0.7586 |  |
| X22.3h | efficiency at that duty cycle | 96.55 | % |
| X22.3i | maximum gain | 10.95 |  |
| X22.3j | duty cycle of maximum gain | 0.9544 |  |
| X22.3k | buck-boost duty cycle | 0.7059 |  |
| X22.3l | buck-boost inductor current | 1.020 | A |
| X22.3m | switch blocking voltage | 17 | V |
| X22.3n | average input current | 0.720 | A |
| X22.3o | K at 20 mA | 0.01567 |  |
| X22.3p | K_crit | 0.0469 |  |
| X22.3q | DCM duty cycle | 0.4336 |  |
| X22.4a | flyback D at 36 V | 0.500 |  |
| X22.4b | flyback D at 48 V | 0.4286 |  |
| X22.4c | flyback D at 72 V | 0.3333 |  |
| X22.4d | off-state voltage at 72 V | 108 | V |
| X22.4e | clamp interval | 125 | ns |
| X22.4f | clamp energy per cycle | 9.375 | µJ |
| X22.4g | clamp loss | 1.41 | W |
| X22.4h | peak drain voltage | 132 | V |
| X22.4i | leakage energy | 3.75 | µJ |
| X22.4j | clamp-to-leakage energy ratio | 2.5 |  |
| X22.4k | forward turns ratio | 5.40 |  |
| X22.4l | forward D at 72 V | 0.2475 |  |
| X22.4m | maximum duty cycle | 0.556 |  |
| X22.4n | forward off-state voltage | 162 | V |
| X22.4o | normal flux swing | 0.0792 | T |
| X22.4p | worst-case flux swing | 0.178 | T |
| X22.4r | worst-case to normal swing | 2.24 |  |
| X22.4q | magnetizing ripple | 0.238 | A |
| X22.5a | core reluctance | 2.387 | 10⁵ H⁻¹ |
| X22.5b | gap reluctance | 7.958 | 10⁶ H⁻¹ |
| X22.5c | inductance | 109.8 | µH |
| X22.5d | effective permeability | 72.82 |  |
| X22.5e | saturation current | 6.994 | A |
| X22.5f | stored energy | 2.686 | mJ |
| X22.5g | energy in the gap | 97.1 | % |
| X22.5h | sinusoidal loss density | 94.87 | kW/m³ |
| X22.5i | core loss | 0.455 | W |
| X22.5j | triangular loss density, D = 0.5 | 88.4 | kW/m³ |
| X22.5k | ratio to sinusoid, D = 0.5 | 0.932 |  |
| X22.5l | triangular loss density, D = 0.1 | 119 | kW/m³ |
| X22.5m | ratio to sinusoid, D = 0.1 | 1.256 |  |
| X22.5n | skin depth | 0.1694 | mm |
| X22.5o | Δ | 0.708 |  |
| X22.5p | F_R, low-Δ approximation | 1.246 |  |
| X22.5q | F_R, Dowell | 1.244 |  |
| X22.6a | overlap loss | 7.30 | W |
| X22.6b | conduction loss | 2.56 | W |
| X22.6c | output-charge energy | 26.6 | µJ |
| X22.6d | output-charge loss | 2.13 | W |
| X22.6e | E_oss-only estimate | 0.72 | W |
| X22.6f | reverse-recovery energy | 34.2 | µJ |
| X22.6g | reverse-recovery loss | 2.74 | W |
| X22.6h | GaN reverse-recovery loss | 0 | W |
| X22.6i | optimal on-resistance | 36.5 | mΩ |
| X22.6j | minimum loss | 4.67 | W |
| X22.6k | minimum loss at 160 kHz | 6.60 | W |
| X22.6l | loss with 20 mΩ | 5.54 | W |
| X22.6m | negative current for ZVS | 2.00 | A |
| X22.6n | TCM ripple | 14.0 | A |
| X22.6o | TCM inductance | 1.607 | µH |
| X22.6p | TCM peak current | 12.0 | A |
| X22.6q | TCM RMS current | 6.43 | A |
| X22.6r | conduction-loss factor | 1.653 |  |
| X22.7a | resonant frequency | 10.38 | kHz |
| X22.7b | Q | 3.68 |  |
| X22.7c | DC control-to-output gain | 21.58 | dB |
| X22.7d | plant magnitude at 40 kHz | 0.864 |  |
| X22.7e | plant phase at 40 kHz | −175.7 | ° |
| X22.7f | phase boost | 140.7 | ° |
| X22.7g | k | 5.77 |  |
| X22.7h | zero frequency | 6.93 | kHz |
| X22.7i | pole frequency | 230.8 | kHz |
| X22.7j | compensator gain at crossover | 1.157 |  |
| X22.7k | integrator frequency | 1.390 | kHz |
| X22.7l | crossover (numerical check) | 40.0 | kHz |
| X22.7m | phase margin (numerical check) | 55.0 | ° |
| X22.7n | on-time slope | 1.364 | A/µs |
| X22.7o | off-time slope | 2.273 | A/µs |
| X22.7p | alpha without compensation | −1.67 |  |
| X22.7q | minimum compensating slope | 0.455 | A/µs |
| X22.7r | alpha with m_a = m2/2 | −0.455 |  |
| X22.7s | perturbation after five cycles | 0.0194 |  |
| X22.7t | load-step deviation | 42.3 | mV |
| X22.7u | phase lost to delay | 14.4 | ° |
| X22.7v | phase margin left | 40.6 | ° |
| X22.7w | crossover for 10° delay | 27.8 | kHz |
| X22.8a | cascade efficiency | 72.0 | % |
| X22.8b | cascade battery current | 29.24 | mA |
| X22.8c | direct-buck battery current | 24.20 | mA |
| X22.8d | extra current | 5.04 | mA |
| X22.8e | PFM/PWM crossover | 118.3 | mA |
| X22.8f | PWM efficiency at 0.5 mA | 4.00 | % |
| X22.8g | PFM efficiency at 0.5 mA | 93.98 | % |
| X22.8h | PWM efficiency at 200 mA | 91.74 | % |
| X22.8i | PFM efficiency at 200 mA | 86.21 | % |
| X22.8j | sleep energy | 2.115 | J |
| X22.8k | active energy | 10.00 | J |
| X22.8l | radio energy | 15.34 | J |
| X22.8m | quiescent energy | 0.4925 | J |
| X22.8n | daily energy | 27.95 | J |
| X22.8o | average battery power | 0.3235 | mW |
| X22.8p | battery life | 73.4 | days |
| X22.8q | DVS capacitor current | 0.94 | A |
| X22.8r | AVS saving | 14.2 | % |
| X22.8s | break-even time | 151.9 | µs |
| X22.9a | graphite capacity | 371.9 | mAh/g |
| X22.9b | cell energy | 15.12 | Wh |
| X22.9c | C-rate of 6 A | 1.43 |  |
| X22.9d | voltage at 0⁺ | 3.680 | V |
| X22.9e | voltage at 50 s | 3.633 | V |
| X22.9f | voltage at 200 s | 3.606 | V |
| X22.9g | pulse current limit | 20.0 | A |
| X22.9h | steady current limit | 12.31 | A |
| X22.9i | incremental capacitance | 30240 | F |
| X22.9j | CV time constant | 30.24 | min |
| X22.9k | SOC at start of CV | 0.647 |  |
| X22.9l | CC time | 38.33 | min |
| X22.9m | CV time | 79.81 | min |
| X22.9n | total time | 118.1 | min |
| X22.9o | SOC at termination | 0.975 |  |
| X22.9p | charge added in CV | 1.376 | Ah |
| X22.9q | coulomb-counter error | 36.0 | mAh |
| X22.9r | learned capacity | 3.818 | Ah |
| X22.9s | state of health | 90.9 | % |
| X22.10a | current at 54 V | 2444 | A |
| X22.10b | current at 800 V | 165.0 | A |
| X22.10c | lumped loss at 54 V | 478.0 | W |
| X22.10d | distributed loss at 54 V | 159.3 | W |
| X22.10e | distributed loss at 800 V | 0.726 | W |
| X22.10v | loss ratio, 800 V to 54 V | 219.5 |  |
| X22.10f | per-conductor ratio | 1.519 |  |
| X22.10g | duty cycle | 0.0625 |  |
| X22.10h | current per phase | 50.0 | A |
| X22.10i | phase ripple | 8.79 | A |
| X22.10j | summed ripple | 2.34 | A |
| X22.10k | ratio | 0.267 |  |
| X22.10l | summed-ripple frequency | 9.6 | MHz |
| X22.10m | target impedance | 75 | µΩ |
| X22.10n | voltage at 600 A | 0.755 | V |
| X22.10o | bulk capacitance | 7.07 | mF |
| X22.10p | package resonance | 19.89 | MHz |
| X22.10q | characteristic impedance | 100 | µΩ |
| X22.10r | first droop, 300 A | 30.0 | mV |
| X22.10s | first droop, 400 A | 40.0 | mV |
| X22.10t | die capacitance for 30 mV | 142.2 | µF |
| X22.10u | damping ESR, Z0/2 rule | 50 | µΩ |
| X22.10x | droop-minimizing ESR, as a fraction of Z0 (simulated) | 0.53 | |
| X22.10y | droop-minimizing ESR (simulated) | 53 | µΩ |
| X22.11a | no-load speed | 400 | rad/s |
| X22.11b | no-load speed | 3820 | rpm |
| X22.11c | stall torque | 23.04 | N·m |
| X22.11d | current at 3 N·m | 25.0 | A |
| X22.11e | speed at 3 N·m | 347.9 | rad/s |
| X22.11f | efficiency at 3 N·m | 86.98 | % |
| X22.11g | slip | 0.030 |  |
| X22.11h | rotor frequency | 1.50 | Hz |
| X22.11i | rotor copper loss | 600 | W |
| X22.11j | mechanical power | 19.4 | kW |
| X22.11k | induced torque | 254.6 | N·m |
| X22.11l | slip of maximum torque | 0.1918 |  |
| X22.11m | speed of maximum torque | 1455 | rpm |
| X22.11n | maximum torque | 234.1 | N·m |
| X22.11o | starting torque | 95.06 | N·m |
| X22.11p | torque at 3% slip | 79.25 | N·m |
| X22.11q | power angle | 36.50 | ° |
| X22.11r | pull-out power | 2.522 | MW |
| X22.11s | armature current | 209.0 | A |
| X22.11t | power factor (lagging) | 0.996 |  |
| X22.11u | reactive power drawn | 0.136 | MVAr |
| X22.11v | E_f for unity power factor | 2923 | V |
| X22.12a | base current | 167.3 | A |
| X22.12b | base impedance | 1190 | Ω |
| X22.12c | transformer reactance | 0.120 | pu |
| X22.12d | line reactance | 0.0479 | pu |
| X22.12e | total reactance | 0.1679 | pu |
| X22.12f | power angle | 19.22 | ° |
| X22.12g | Q leaving bus 1 | 0.460 | pu |
| X22.12h | Q arriving at bus 2 | −0.220 | pu |
| X22.12i | line reactive consumption | 0.680 | pu |
| X22.12j | maximum transfer | 6.08 | pu |
| X22.12k | three-phase fault current | 5.00 | pu |
| X22.12l | three-phase fault current | 0.837 | kA |
| X22.12m | fault MVA | 500 | MVA |
| X22.12n | SLG fault current | 6.00 | pu |
| X22.12o | SLG fault current | 1.004 | kA |
| X22.12p | stored kinetic energy | 360 | GJ |
| X22.12q | initial RoCoF | −0.100 | Hz/s |
| X22.12r | settling deviation | −0.1043 | Hz |
| X22.12s | governor pickup | 1043 | MW |
| X22.13a | charging loss | 16.2 | nJ |
| X22.13w | four-step charging loss | 4.05 | nJ |
| X22.13b | supply energy | 32.4 | nJ |
| X22.13c | loss power, one step | 162 | µW |
| X22.13d | loss power, four steps | 40.5 | µW |
| X22.13e | boost duty cycle | 0.5833 |  |
| X22.13f | DC gain | 28.8 | V |
| X22.13g | DC gain | 29.19 | dB |
| X22.13h | resonant frequency | 5.32 | kHz |
| X22.13i | Q | 9.43 |  |
| X22.13j | RHP zero | 50.2 | kHz |
| X22.13k | core-loss coefficient a | 197.0 | W/T^2.6 |
| X22.13l | copper-loss coefficient b | 0.0400 | W·T² |
| X22.13m | optimal flux swing | 0.1488 | T |
| X22.13n | core loss at optimum | 1.390 | W |
| X22.13o | copper loss at optimum | 1.807 | W |
| X22.13p | total at optimum | 3.197 | W |
| X22.13q | loss ratio | 0.769 |  |
| X22.13r | in-phase drop | 0.0460 | pu |
| X22.13s | quadrature drop | 0.0740 | pu |
| X22.13t | first-order sending voltage | 1.046 | pu |
| X22.13u | exact sending voltage | 1.0486 | pu |
| X22.13v | corrected estimate | 1.0486 | pu |
| X22.14a | module input power | 1613 | W |
| X22.14b | module loss | 112.9 | W |
| X22.14c | input current | 33.6 | A |
| X22.14d | required second stage | 95.4 | % |
| X22.14e | conventional chain efficiency | 84.8 | % |
| X22.14f | conventional input power | 1768 | W |
| X22.14g | implied saving | 155 | W |
| X22.14h | sheet resistance | 0.246 | mΩ |
| X22.14i | loop resistance | 41.0 | µΩ |
| X22.14j | lateral IR drop | 82.1 | mV |
| X22.14k | lateral loss | 164 | W |
| X22.14l | planes for under 150 W | 7 |  |
| X22.14m | lateral loss with 7 planes | 140.7 | W |
| X22.14n | characteristic impedance | 51.6 | µΩ |
| X22.14o | first droop | 51.6 | mV |
| X22.14p | droop as % of 0.75 V | 6.89 | % |
| X22.14q | resonant frequency | 20.5 | MHz |
| X22.14r | target impedance | 37.5 | µΩ |
| X22.14s | die capacitance needed | 284 | µF |
| X22.14t | lateral chain input with plane loss added | 1962 | W |
| X22.14u | additive saving on 22-10's boundary | 349 | W |
