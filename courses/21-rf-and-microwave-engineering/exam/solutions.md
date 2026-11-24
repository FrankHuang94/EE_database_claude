# Course 21 · Final Exam Solutions

Exam: [README.md](README.md). Every number below is recomputed by [verify_21_exam.py](../verify/verify_21_exam.py), mostly by a second route:

- Question 1: the S-parameters by solving the circuit, and the stability tests by sweeping passive loads;
- Question 2: the matches by evaluating the network's impedance and sweeping it in frequency;
- Questions 3 and 13: the cascade through noise temperatures and a two-tone simulation;
- Question 4: the LNA's input impedance and noise from its small-signal equations;
- Question 5: the mixer responses from Fourier series of the LO waveforms;
- Questions 6 and 7: the oscillator and PA quantities by numerical integration;
- Questions 8 and 9: the filters from scipy's Butterworth design and the resonator from its impedance;
- Question 10: the array from its array factor;
- Questions 11 to 14: the budgets, rates and geometry from their definitions.

---

## Solutions

### Solution 1

(a) $\Gamma = (25 - 50)/(25 + 50)$ = **−0.333**. Return loss $-20\log_{10}(1/3)$ = **9.54** dB; VSWR $(1 + 1/3)/(1 - 1/3)$ = **2.00**; mismatch loss $-10\log_{10}(1 - 1/9)$ = **0.512** dB.

(b) $S_{11} = Z/(Z + 2Z_0) = 20/120$ = **0.167** and $S_{21} = 2Z_0/(Z + 2Z_0) = 100/120$ = **0.833**, so the insertion loss is $-20\log_{10}0.833$ = **1.584** dB. The resistor absorbs $1 - \lvert S_{11}\rvert^2 - \lvert S_{21}\rvert^2 = 1 - 0.0278 - 0.6944$ = **0.278** of the incident power: lossy networks fail the unitarity test, which is how you spot loss in measured data.

(c) $\Delta = S_{11}S_{22} - S_{12}S_{21}$: $S_{11}S_{22} = 0.225\angle{-185°}$ and $S_{12}S_{21} = 0.16\angle 120°$, so $\Delta = (-0.2241 + 0.0196j) - (-0.0800 + 0.1386j) = -0.1441 - 0.1190j$, $\lvert\Delta\rvert$ = **0.187**.

$$
K = \frac{1 - 0.25 - 0.2025 + 0.0349}{2 \times 0.16} = \frac{0.5824}{0.32} = \mathbf{1.820}, \qquad \mu = \frac{1 - 0.25}{\lvert S_{22} - \Delta S_{11}^*\rvert + 0.16} = \mathbf{1.366} .
$$

The μ denominator is $\lvert S_{22} - \Delta S_{11}^*\rvert$ = **0.389** plus 0.16. $K > 1$ with $\lvert\Delta\rvert < 1$ (and μ > 1): **unconditionally stable**. MSG $= 10\log_{10}(4/0.04)$ = **20.0** dB; $G_{max} = 10\log_{10}[100(K - \sqrt{K^2 - 1})] = 10\log_{10}(100 \times 0.2993)$ = **14.76** dB.

(d) $S_{22}\Gamma_L = 0.225\angle 15°$ and $S_{12}S_{21}\Gamma_L = 0.08\angle 180°$, so

$$
\Gamma_{in} = 0.5\angle{-140°} + \frac{0.08\angle 180°}{1 - 0.225\angle 15°} = (-0.3830 - 0.3214j) + (-0.1017 - 0.0076j) ,
$$

$\lvert\Gamma_{in}\rvert$ = **0.586** at **−145.8**°. Because $S_{12} \ne 0$ the load changes the input match, which is why LNA input and output matches are designed together.

### Solution 2

(a) $Q = \sqrt{50/4 - 1}$ = **3.391**. The series reactance is $QR_{low}$ = 13.56 Ω, so $L = 13.56/(2\pi \times 2.4\ \text{GHz})$ = **0.900** nH; the shunt susceptance is $Q/R_{high}$ = 0.06782 S, so $C = 0.06782/(2\pi \times 2.4\ \text{GHz})$ = **4.498** pF, placed across the 50 Ω load. The series L faces the 4 Ω PA.

(b) $\Delta f = f_0 \cdot 2\Gamma_m\sqrt{1 + Q^2}/Q^2 = 2.4\ \text{GHz} \times 0.2\sqrt{12.5}/11.5$ = **147.6** MHz (6.1%); the large-Q form $2\Gamma_m/Q$ gives **141.5** MHz. An exact sweep of the network's input impedance gives **148.4** MHz, slightly more, because $\lvert\Gamma\rvert$ grows a little slower than linearly away from the centre.

(c) $R_m = \sqrt{4 \times 50}$ = **14.14** Ω; each section has $Q = \sqrt{\sqrt{12.5} - 1}$ = **1.592**. Inductor loss: one section $10\log_{10}(1 + 3.391/20)$ = **0.680** dB; two sections $2 \times 10\log_{10}(1 + 1.592/20)$ = **0.665** dB. For this 12.5:1 ratio the two designs lose about the same, because the sum of the section Qs (3.18) is close to the single Q (3.39); two sections mainly widen the band. At larger ratios the saving grows: at 100:1, one section (Q = 9.95) loses **1.754** dB and two sections (Q = 3 each) **1.214** dB, which is the sense of 21-02 §3.5.

The binomial transformer splits the logarithmic step $\ln 12.5$ in the ratio 1:2:1 (from $\Gamma_n \approx \tfrac12\ln(Z_{n+1}/Z_n)$ with binomial weights), so from the PA side $Z_1 = 4 \times 12.5^{1/4}$ = **7.52** Ω and $Z_2 = 4 \times 12.5^{3/4}$ = **26.59** Ω, each a quarter wavelength long at 2.4 GHz. Lines of such low impedance are wide, which is one reason PA matches are often lumped or mixed.

(d) Bode–Fano: $\Delta f \le 1/[2RC\ln(1/\Gamma_m)] = 1/(2 \times 4 \times 40\ \text{pF} \times \ln 10)$ = **1.357** GHz. No lossless network of any order can do better. The 40 pF must be absorbed into the match (it is a 1.66 Ω reactance at 2.4 GHz, so it dominates the load), and the limit says a well-designed multi-section match could still reach a band several times wider than part (b)'s.

### Solution 3

(a) Linear values: $G_1$ = 39.81, $F_1$ = 1.514; the filter has $F_2 = L$ = 1.778 and $G_2$ = 1/1.778; $F_3$ = 7.943.

$$
F = 1.514 + \frac{0.778}{39.81} + \frac{6.943}{39.81/1.778} = 1.514 + 0.0195 + 0.3101 = 1.843 ,
$$

NF = **2.66** dB. The mixer, behind only 13.5 dB of net gain, adds about 0.8 dB to the LNA's 1.8 dB.

(b) In milliwatts, $1/\text{IIP3} = 1/0.1585 + (39.81/1.778)/1.995 = 6.31 + 11.22$, so IIP3 = **0.0570** mW = **−12.44** dBm. The mixer dominates the linearity, because the LNA's gain multiplies its contribution.

(c) $N = -174 + 73.01 + 2.66$ = −98.33 dBm, so the sensitivity is −98.33 + 5 = **−93.3** dBm, and SFDR $= \tfrac23(-12.44 + 98.33)$ = **57.3** dB.

(d) From $F = \text{ENR}/(Y - 1)$, $Y = 1 + \text{ENR}/F = 1 + 31.62/1.843 = 18.16$, or **12.59** dB. A lower noise figure gives a larger Y: an ideal noiseless receiver would read $1 + \text{ENR}$, **15.14** dB.

### Solution 4

(a) $\omega_T = 2\pi \times 55$ GHz = 3.456 × 10¹¹ rad/s, so $L_s = R_s/\omega_T$ = **144.7** pH. Resonance: $L_g + L_s = 1/(\omega_0^2C_{gs}) = 1/[(3.456 \times 10^{10})^2 \times 150\ \text{fF}]$ = 5.582 nH, so $L_g$ = **5.438** nH.

(b) $Q_{in} = 1/(2\omega_0R_sC_{gs}) = 1/(2 \times 3.456 \times 10^{10} \times 50 \times 150 \times 10^{-15})$ = **1.929**; $G_m = \omega_T/(2\omega_0R_s) = 10/100$ = **100.0** mS. The gate sees $Q_{in}$ times the source EMF, so the source-referred IIP3 is $5 - 20\log_{10}1.929$ = **−0.71** dBm.

(c) $g_m = \omega_TC_{gs}$ = **51.84** mS. Ideal inductors: $F = 1 + 1 \times 0.05184 \times 50 \times (0.1)^2 = 1.0259$, NF = **0.111** dB. With $Q_L$ = 20: $r_g = \omega_0L_g/Q_L = 3.456 \times 10^{10} \times 5.438\ \text{nH}/20$ = **9.40** Ω; re-matching $\omega_TL_s = R_s - r_g$ gives $L_s$ = **117.5** pH; and

$$
F = 1 + \frac{9.40}{50} + 0.05184 \times \frac{59.40^2}{50} \times 0.01 = 1 + 0.1879 + 0.0366 = 1.2245 ,
$$

NF = **0.880** dB. The gate inductor's loss, not the transistor, dominates: this is why low-NF LNAs use high-Q off-chip or bond-wire inductors.

(d) $G_1 = (F_2 - 1)/[F_1(10^{0.05} - 1)] = 9/(1.2245 \times 0.1220)$ = **60.2**, or **17.80** dB.

### Solution 5

(a) Passive: $20\log_{10}(2/\pi)$ = **−3.92** dB. Gilbert: $(2/\pi) \times 0.025 \times 400 = 6.37$, **16.08** dB. Ideal SSB noise figure with unfiltered white source noise $10\log_{10}(\pi^2/4)$ = **3.92** dB: the image band contributes 3 dB and the odd-harmonic bands the remaining 0.92 dB. A filter that removes the image and harmonic bands lowers it (21-05).

(b) $\varepsilon = 10^{0.3/20} - 1$ = **0.0351**; θ = 0.05236 rad. Exact: numerator $1 + 2(1.0351)\cos 3° + 1.0351^2 = 4.1390$, denominator $1 - 2.0674 + 1.0715 = 0.004072$, IRR = **1016**, **30.07** dB. Approximation $4/(0.0351^2 + 0.0524^2) = 4/0.003976$: **30.03** dB.

(c) A square wave's third harmonic is 1/3 of its fundamental: **−9.54** dB. For the harmonic-reject LO the 7th harmonic's weight is $\tfrac17[\sqrt2 + 2\cos 315°] = 2\sqrt2/7$, against $2\sqrt2$ for the fundamental: **−16.90** dB, the same as a square wave's 7th. Harmonic rejection removes only the 3rd and 5th.

(d) $\text{BW} = 1/(\pi NR_sC) = 1/(\pi \times 6 \times 50 \times 25\ \text{pF})$ = **42.44** MHz. Centre gain $[(6/\pi)\sin(\pi/6)]^2 = 0.9119$: **−0.801** dB. Fewer paths widen the band for the same capacitance per path but lose more at the centre, because each capacitor averages over a wider slice of the LO period.

### Solution 6

(a) $1/Q = 1/12 + 1/30$, Q = **8.57**. $\omega_0L$ = 22.62 Ω, so $C = 1/(\omega_0^2L) = 1/[(3.770 \times 10^{10})^2 \times 0.6\ \text{nH}]$ = **1.173** pF and $R_p = Q\omega_0L = 8.571 \times 22.62$ Ω = **193.9** Ω (all differential).

(b) $V = (2/\pi)I_{tail}R_p = 0.6366 \times 3\ \text{mA} \times 193.9$ = **0.370** V. η = $V/(\pi V_{DD})$ = **11.8**%. $P_s = V^2/(2R_p)$ = **0.354** mW.

(c) $\mathcal L = kT/(R_pC^2V^2\Delta\omega^2) = 4.142 \times 10^{-21}/(193.9 \times 1.375 \times 10^{-24} \times 0.1371 \times 3.948 \times 10^{13})$ = **2.87e-12** per hertz, **−115.4** dBc/Hz. With $F$ = 3: +4.77 dB, **−110.7** dBc/Hz.

(d) FoM $= 110.65 + 20\log_{10}(6000) - 10\log_{10}3 = 110.65 + 75.56 - 4.77$ = **181.4** dB: a mediocre oscillator, held back by the low tank Q, the small inductor (low $R_p$, so low swing for the current) and the power spent outside the tank. Divide by 2: −110.65 − 6.02 = **−116.7** dBc/Hz.

### Solution 7

(a) 28 dBm = 0.631 W, so $R_{opt} = (3.4 - 0.4)^2/(2 \times 0.631)$ = **7.13** Ω and $Q = \sqrt{50/7.13 - 1}$ = **2.452**.

(b) $\eta(\alpha) = (\alpha - \sin\alpha)/\{2[2\sin(\alpha/2) - \alpha\cos(\alpha/2)]\}$: 360° gives **50.0**%, 240° (class AB) **66.1**%, 180° (class B) **78.5**% and 120° (class C) **89.7**%. Class A with the knee: $\tfrac12(1 - 0.4/3.4)$ = **44.1**%.

(c) $\text{ACLR} = 2(P_{in} - \text{IIP3}) - 4.77 \le -40$, with 4.77 dB = $10\log_{10}3$, gives $P_{in} \le 6 - 17.61$ = **−11.61** dBm, an output of **18.39** dBm: **9.61** dB below the 28 dBm saturated power. The signal's $10^{-4}$ peaks then reach 18.39 + 9.64 = **28.03** dBm, just at saturation, so the cubic model (which knows nothing of clipping) is self-consistent here. Running the average closer to saturation would clip the peaks, and DPD cannot restore power the PA does not have: that needs crest-factor reduction as well as DPD (21-07 §3.4, §3.7).

(d) 8 dB back-off is $x = 10^{-8/20} = 0.398$. Doherty: $(\pi/2)x$ = **62.5**%; class B: $(\pi/4)x$ = **31.3**%. At 3 dB, $x$ = 0.708 > ½: $(\pi/2)x^2/(3x - 1)$ = **70.1**%. Envelope tracking: $\eta_{ET} = \eta_{PA}\eta_{mod} = 0.65 \times 0.85$ = **55.3**%, flat across the envelope, which is why ET wins on signals that spend most of their time deep in back-off.

### Solution 8

(a) LO = 5.8 − 0.4 = **5.4** GHz; image $f_{LO} - f_{IF}$ = **5.0** GHz. The half-IF spurs satisfy $\lvert 2f_{LO} - 2f_{RF}\rvert = f_{IF}$, so $f_{RF} = f_{LO} \pm f_{IF}/2$: **5.6** GHz (halfway between the LO and the wanted signal) and **5.2** GHz (halfway between the image and the LO). Each one's second harmonic mixes with the LO's second harmonic to the IF: $2 \times 5.6 - 2 \times 5.4$ = 0.4 GHz.

(b) Image: $x = 29(5.0/5.8 - 5.8/5.0) = -8.640$, so $10\log_{10}(1 + x^8)$ = **74.9** dB. Half-IF at 5.6 GHz: $x = 29(5.6/5.8 - 5.8/5.6) = -2.036$, **24.7** dB; at 5.2 GHz: $x = -6.346$, **64.2** dB. The near half-IF spur sits only 200 MHz from the wanted signal; the mixer's second-order balance must do the rest.

(c) IRR ≥ 30 + 12 = **42** dB. With ε = 0, $4/\theta^2 = 10^{4.2}$, so θ = $2 \times 10^{-2.1}$ = 0.0159 rad = **0.910**°.

(d) $\text{NF}_{ADC} = -153 + 2 + 174$ = **23** dB. Friis: $F_1 + (F_{ADC} - 1)/G \le F_1 \times 10^{0.1}$ gives $G \ge 198.5/(1.585 \times 0.2589)$ = **484**, **26.85** dB. Jitter: $\sigma_t = 10^{-55/20}/(2\pi \times 6\ \text{GHz})$ = **47.2** fs.

### Solution 9

(a) $x = (\pi/2)(3.55/3.65) = 1.5278$; $k^2_{eff} = x\cot x$ = **6.58**%; approximation $(\pi^2/4)(0.10/3.65)$ = **6.76**%. $C_m/C_0 = (f_p/f_s)^2 - 1$ = **0.0571**.

(b) The PA must deliver 26 + 2.5 = **28.5** dBm; 28.5 − 50 = **−21.5** dBm reaches the LNA, which sets its compression and the receiver's IIP2/IIP3 needs. The receiver's noise floor referred to the antenna is −174 + 4 = −170 dBm/Hz, so the PA's noise must arrive at or below −176 dBm/Hz: isolation ≥ −138 − (−176) = **38** dB in the receive band. Isolation is needed in both bands: against the carrier for linearity and against the PA's noise for sensitivity.

(c) FoM $2.4 \times 100$ fF = **240** fs; $f_c = 1/(2\pi R_{on}C_{off})$ = **663** GHz. On: $20\log_{10}(1 + 2.4/100)$ = **0.206** dB. Off: $x = 2 \times 50 \times 2\pi \times 3.5\ \text{GHz} \times 100\ \text{fF} = 0.2199$, $\lvert S_{21}\rvert = 0.2148$, isolation **13.36** dB.

(d) $V_{pk} = \sqrt{2 \times 50 \times 1.995}$ = **14.13** V. VSWR 4 is $\lvert\Gamma\rvert$ = 0.6, worst case $\times 1.6$ = **22.60** V, so $N \ge 7.53$: **8** transistors. Mismatch loss $-10\log_{10}(1 - 0.36)$ = **1.94** dB.

### Solution 10

(a) $8 + 5 + 20\log_{10}64$ = **49.12** dBm; at 50°, $+10\log_{10}\cos 50° = -1.92$ dB: **47.20** dBm.

(b) $\sin\theta = (39/37)\sin 50° = 0.8075$, θ = **53.85**°. $B_{3dB} \approx 0.886 \times 39\ \text{GHz}/(8 \times 0.5 \times \sin 50°)$ ≈ **11.28** GHz: an 8-element row barely squints over a 400 MHz carrier. The large-N formula is approximate for N = 8; the exact array factor gives **11.35** GHz.

(c) 2 bits: $x = \pi/4$, $S = (\sin x/x)^2 = 0.8106$: gain loss **0.912** dB; floor $10\log_{10}(0.1894/64)$ = **−25.29** dB; rms error $180°/(4\sqrt3)$ = **25.98**°. Each extra bit lowers the floor by about 6 dB: 4 bits give **−36.99** dB and 5 bits **−43.00** dB, so **5** bits are the fewest for a floor below −40 dB.

(d) At 42 GHz, $d/\lambda = 0.5 \times 42/39$ = **0.538**; the limit for 50° is $1/(1 + \sin 50°)$ = **0.566**. Yes, it stays free of grating lobes, with little room to spare.

### Solution 11

(a) EIRP = 0 − 1 − 6 = **−7** dBm. Sensitivity $-174 + 60 + 11 + 7$ = **−96** dBm.

(b) $M = 6\,Q^{-1}(0.1) = 6 \times 1.2816$ = **7.69** dB. MAPL = −7 − 1 − 1.5 + 96 − 7.69 − 10 = **68.81** dB.

(c) λ = 0.1229 m, so $PL(1\ \text{m}) = 20\log_{10}(4\pi/\lambda)$ = **40.20** dB; $d = 10^{(68.81 - 40.20)/30}$ = **8.99** m. A wrist-to-pocket link is fine; across a house it is not.

(d) $-174 + 50.97 + 5 + 7$ = **−111.0** dBm, 15.0 dB better, so $d = 8.99 \times 10^{15.03/30}$ = **28.5** m, at eight times the airtime per bit.

### Solution 12

(a) At 30 kHz, $T_s = 10^{-3}/28$ s. 80 MHz: $4 \times 8 \times 0.9258 \times 217 \times 12 \times 28{,}000 \times 0.86$ = **1857.6** Mb/s; 60 MHz: **1386.8** Mb/s; total **3244.4** Mb/s.

(b) $2 \times 1960 \times 10 \times \tfrac56/14.4\ \mu\text{s}$ = **2268.5** Mb/s.

(c) With the initiator's error $e_A = +5$ ppm and the responder's $e_B = -15$ ppm, $(e_A - e_B)T_{reply}/2 = 20 \times 10^{-6} \times 300\ \mu\text{s}/2$ = 3 ns: the range reads **0.899** m long. For 10 cm: $T_{reply} \le 2 \times (0.1/c)/(20 \times 10^{-6})$ = **33.4** µs; double-sided ranging removes the dependence instead.

(d) $v = \sqrt{GM/(R_E + h)}$ = **7256** m/s; line of sight $vR_E/(R_E + h)$ = **6106** m/s; Doppler $6106 \times 2 \times 10^9/c$ = **40.7** kHz, **2.72** subcarriers. A higher orbit moves more slowly and is seen at a shallower angle, so the Doppler falls only modestly from the 46 kHz of 600 km: the phone must still pre-compensate it from GNSS and the satellite's ephemeris.

### Solution 13

(a) **One tone.** With $x = A\cos\omega t$, $x^3 = A^3(\tfrac34\cos\omega t + \tfrac14\cos3\omega t)$, so the fundamental is $(a_1 + \tfrac34a_3A^2)A$. Compression by 1 dB means $1 + \tfrac34(a_3/a_1)A^2 = 10^{-1/20}$, so $A_{1dB}^2 = \tfrac43(1 - 10^{-0.05})\lvert a_1/a_3\rvert = 0.1450\lvert a_1/a_3\rvert$.

**Two tones.** With $x = A(\cos\omega_1t + \cos\omega_2t)$, the cube contains $3A^3\cos^2\omega_1t\cos\omega_2t = \tfrac32A^3\cos\omega_2t + \tfrac34A^3[\cos(2\omega_1 - \omega_2)t + \cos(2\omega_1 + \omega_2)t]$, so the IM3 product at $2\omega_1 - \omega_2$ has amplitude $\tfrac34\lvert a_3\rvert A^3$. The intercept is defined where the extrapolated small-signal lines meet: the fundamental's line $a_1A$ (slope 1 in dB) and the IM3 line $\tfrac34\lvert a_3\rvert A^3$ (slope 3). The fundamental's own cubic terms ($\tfrac94a_3A^3$ with two tones) are part of compression, not of the asymptote, so they are left out. Setting $a_1A = \tfrac34\lvert a_3\rvert A^3$ gives $A_{IIP3}^2 = \tfrac43\lvert a_1/a_3\rvert$.

The ratio in dB is $10\log_{10}(A_{IIP3}^2/A_{1dB}^2) = 10\log_{10}[1/(1 - 10^{-0.05})]$ = **9.64** dB, so an IIP3 of −10 dBm means P1dB = **−19.64** dBm. Real circuits deviate by a dB or two, because higher-order terms matter near compression.

(b) Let a source at temperature $T_s$ drive stage 1 (available gain $G_1$, noise temperature $T_1$), followed by stage 2 ($G_2$, $T_2$), in bandwidth B. Each stage's noise is modelled as an extra source temperature at its own input, and uncorrelated noise powers add. The available output noise is

$$
N_o = G_1G_2k(T_s + T_1)B + G_2kT_2B = G_1G_2k\left(T_s + T_1 + \frac{T_2}{G_1}\right)B ,
$$

so the cascade looks like one stage with $T_e = T_1 + T_2/G_1$. The gains must be available gains, because noise temperature is defined with available power. Substituting $T_i = T_0(F_i - 1)$ gives $F - 1 = (F_1 - 1) + (F_2 - 1)/G_1$, which is Friis's formula. For Question 3: $T_1$ = 148.9 K, $T_2$ = 225.7 K (a loss L at $T_0$ has $T = T_0(L - 1)$), $T_3$ = 2013.5 K, and $T_e = 148.9 + 225.7/39.81 + 2013.5/22.39$ = **244.5** K.

(c) Each element radiates $P_e$ with gain $G_e$, and the coherent array has gain $NG_e$ for total power $NP_e$, so $E = N^2P_eG_e$ and $P_e = E/(N^2G_e)$. Then $P_{DC} = N(P_e/\eta + P_{oh}) = E/(NG_e\eta) + NP_{oh}$. Setting $dP_{DC}/dN = -E/(N^2G_e\eta) + P_{oh} = 0$ gives $N^* = \sqrt{E/(G_e\eta P_{oh})}$. Since $d^2P_{DC}/dN^2 = 2E/(N^3G_e\eta) > 0$, it is a minimum, and $P_{DC}(N^*) = 2\sqrt{EP_{oh}/(G_e\eta)}$: the two terms are equal there. At $N = kN^*$, $P_{DC}/P_{DC}(N^*) = (1/k + k)/2$, which is **1.25** for $k$ = 2 or ½. With $E$ = 3162 W and $G_e$ = 3.162: $N^* = \sqrt{3162/(3.162 \times 0.2 \times 0.05)}$ = **316** elements and $P_{DC}$ = **31.62** W.

(d) $C = B\log_2(1 + S/N)$, and with bit rate R, $S = E_bR$ and $N = N_0B$, so $S/N = (E_b/N_0)\eta$ with $\eta = R/B$. Reliable transmission needs $R \le C$, that is $\eta \le \log_2(1 + \eta E_b/N_0)$, so $E_b/N_0 \ge (2^\eta - 1)/\eta$. The right side increases with η (its derivative is positive for η > 0), so its infimum is the limit as η → 0. There $2^\eta = e^{\eta\ln2} \approx 1 + \eta\ln2$, so the limit is $\ln 2$ = **−1.59** dB. At η = 2: 3/2, **1.76** dB; at η = 6: 63/6, **10.21** dB.

### Solution 14

(a) On: $20\log_{10}(1 + R_{on}/100) \le 0.2$ gives $R_{on} \le$ **2.33** Ω. Off: $x/\sqrt{1 + x^2} \le 0.01$ gives $x \le 0.0100$, $C_{off} \le 0.0100/(2\pi \times 3.5\ \text{GHz} \times 100\ Ω)$ = **4.55** fF. The product is **10.6** fs, about **9.4** times better than a ~100 fs process. One series switch cannot meet both numbers: either the isolation comes from a series-shunt arrangement (whose loss is then higher than 0.2 dB), or the numbers are at different frequencies or from simulation. Ask for the topology and measured part-level data.

(b) Peak = 26 + 9.64 = **35.64** dBm (**3.66** W). At 45%: $P_{DC}$ = 398.1 mW/0.45 = **884.7** mW, **232.8** mA from 3.8 V. Ideal class B: **1363** mW; ideal symmetric Doherty: **725.1** mW. 45% is plausible only for a Doherty or envelope-tracked PA (ideal 54.9%, and real devices lose several points); it is implausible for class AB. The claim is also out of proportion to handsets: an NR handset of power class 3 transmits up to 23 dBm and may back off by up to 6.5 dB (MPR) on CP-OFDM (3GPP TS 38.101-1, as of Nov 2026; 21-07 §7), while 26 dBm average with an uncompressed 9.64 dB PAPR implies a 3.7 W peak. Ask which waveform, power class and crest-factor reduction they assume.

(c) Behind the passive losses, the LNA and transceiver give $10\log_{10}(1.259 + 2.981/63.10) = 1.16$ dB. Passive losses at the input add dB for dB: 0.2 + 1.5 + 1.16 = **2.86** dB as claimed, **3.16** dB with a 0.5 dB switch. "1.0 dB NF" describes the LNA, not the receiver; the system figure is **1.86** dB worse as claimed and more with a realistic switch.

(d) Rubric (3 points: about 0.75 per question with a sound strong answer):

1. "What are the switch's measured $R_{on}$ and $C_{off}$ at the package pin, and its topology?" *Strong:* part-level numbers, a series-shunt topology for isolation, harmonics at full power into 3:1 VSWR. *Evasive:* process figures of merit.
2. "What PAPR, crest-factor reduction and DPD does the 45% assume, and is it measured over temperature and VSWR?" *Strong:* average efficiency on a stated 3GPP waveform with ACLR and EVM met. *Evasive:* peak efficiency.
3. "What is the receive noise figure at the antenna port, including switch, filter and module losses?" *Strong:* a system figure, measured. *Evasive:* the LNA's own NF.
4. "How do PA, LNA and switch coexist on one die: isolation, thermal coupling, and which bands and duplexers are supported?" *Strong:* measured TX-to-RX isolation and desensitization data. *Evasive:* "integration solves it".

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| X21.1a | reflection coefficient | −0.333 |  |
| X21.1b | return loss | 9.54 | dB |
| X21.1c | VSWR | 2.00 |  |
| X21.1d | mismatch loss | 0.512 | dB |
| X21.1e | S11 of series 20 Ω | 0.167 |  |
| X21.1f | S21 of series 20 Ω | 0.833 |  |
| X21.1g | insertion loss | 1.584 | dB |
| X21.1h | fraction absorbed | 0.278 |  |
| X21.1i | magnitude of Δ | 0.187 |  |
| X21.1j | K | 1.820 |  |
| X21.1k | μ | 1.366 |  |
| X21.1p | μ denominator term | 0.389 |  |
| X21.1l | MSG | 20.0 | dB |
| X21.1m | Gmax | 14.76 | dB |
| X21.1q | K − √(K² − 1) | 0.2993 |  |
| X21.1n | magnitude of Γin | 0.586 |  |
| X21.1o | angle of Γin | −145.8 | ° |
| X21.2a | L-network Q | 3.391 |  |
| X21.2b | series inductance | 0.900 | nH |
| X21.2c | shunt capacitance | 4.498 | pF |
| X21.2d | bandwidth, formula | 147.6 | MHz |
| X21.2e | bandwidth, large-Q form | 141.5 | MHz |
| X21.2k | bandwidth, exact sweep | 148.4 | MHz |
| X21.2f | intermediate resistance | 14.14 | Ω |
| X21.2g | section Q | 1.592 |  |
| X21.2h | inductor loss, one section | 0.680 | dB |
| X21.2i | inductor loss, two sections | 0.665 | dB |
| X21.2l | binomial section next to the PA | 7.52 | Ω |
| X21.2m | binomial section next to the load | 26.59 | Ω |
| X21.2n | inductor loss at 100:1, one section | 1.754 | dB |
| X21.2o | inductor loss at 100:1, two sections | 1.214 | dB |
| X21.2j | Bode–Fano bandwidth | 1.357 | GHz |
| X21.3a | cascaded NF | 2.66 | dB |
| X21.3b | cascaded IIP3 | −12.44 | dBm |
| X21.3f | cascaded IIP3 in milliwatts | 0.0570 | mW |
| X21.3c | sensitivity | −93.3 | dBm |
| X21.3d | SFDR | 57.3 | dB |
| X21.3e | Y-factor | 12.59 | dB |
| X21.3g | Y-factor of a noiseless receiver | 15.14 | dB |
| X21.4a | Ls | 144.7 | pH |
| X21.4b | Lg | 5.438 | nH |
| X21.4c | Qin | 1.929 |  |
| X21.4d | Gm | 100.0 | mS |
| X21.4e | source-referred IIP3 | −0.71 | dBm |
| X21.4f | gm | 51.84 | mS |
| X21.4g | NF, ideal inductors | 0.111 | dB |
| X21.4h | gate-inductor loss resistance | 9.40 | Ω |
| X21.4i | re-matched Ls | 117.5 | pH |
| X21.4j | NF with lossy Lg | 0.880 | dB |
| X21.4k | LNA gain needed | 17.80 | dB |
| X21.4l | LNA gain needed (linear) | 60.2 |  |
| X21.5a | passive mixer gain | −3.92 | dB |
| X21.5b | Gilbert cell gain | 16.08 | dB |
| X21.5c | SSB noise figure | 3.92 | dB |
| X21.5d | gain error ε | 0.0351 |  |
| X21.5e | IRR exact | 30.07 | dB |
| X21.5k | IRR exact (linear) | 1016 |  |
| X21.5f | IRR approximate | 30.03 | dB |
| X21.5g | 3rd-harmonic response | −9.54 | dB |
| X21.5h | 7th-harmonic response, HR LO | −16.90 | dB |
| X21.5i | N-path bandwidth | 42.44 | MHz |
| X21.5j | N-path centre gain | −0.801 | dB |
| X21.6a | tank Q | 8.57 |  |
| X21.6b | tank capacitance | 1.173 | pF |
| X21.6c | Rp | 193.9 | Ω |
| X21.6d | amplitude | 0.370 | V |
| X21.6e | efficiency | 11.8 | % |
| X21.6f | tank signal power | 0.354 | mW |
| X21.6k | phase noise, tank only (linear) | 2.87e-12 | per Hz |
| X21.6g | phase noise, tank only | −115.4 | dBc/Hz |
| X21.6h | phase noise, F = 3 | −110.7 | dBc/Hz |
| X21.6i | FoM | 181.4 | dB |
| X21.6j | phase noise after divide-by-2 | −116.7 | dBc/Hz |
| X21.7a | Ropt | 7.13 | Ω |
| X21.7b | matching Q | 2.452 |  |
| X21.7c | efficiency, 360° | 50.0 | % |
| X21.7d | efficiency, 240° | 66.1 | % |
| X21.7e | efficiency, 180° | 78.5 | % |
| X21.7f | efficiency, 120° | 89.7 | % |
| X21.7g | class A with knee | 44.1 | % |
| X21.7h | largest input power | −11.61 | dBm |
| X21.7i | output power | 18.39 | dBm |
| X21.7m | margin below saturated power | 9.61 | dB |
| X21.7n | 10⁻⁴ peak output power | 28.03 | dBm |
| X21.7j | Doherty, 8 dB back-off | 62.5 | % |
| X21.7k | class B, 8 dB back-off | 31.3 | % |
| X21.7l | Doherty, 3 dB back-off | 70.1 | % |
| X21.7o | envelope-tracking efficiency | 55.3 | % |
| X21.8a | LO | 5.4 | GHz |
| X21.8b | image | 5.0 | GHz |
| X21.8c | near half-IF frequency | 5.6 | GHz |
| X21.8k | far half-IF frequency | 5.2 | GHz |
| X21.8d | image rejection | 74.9 | dB |
| X21.8e | near half-IF rejection | 24.7 | dB |
| X21.8l | far half-IF rejection | 64.2 | dB |
| X21.8f | IRR needed | 42 | dB |
| X21.8g | phase error allowed | 0.910 | ° |
| X21.8h | ADC noise figure | 23 | dB |
| X21.8i | gain ahead of ADC | 26.85 | dB |
| X21.8m | gain ahead of ADC (linear) | 484 |  |
| X21.8j | rms jitter | 47.2 | fs |
| X21.9a | k²eff exact | 6.58 | % |
| X21.9b | k²eff approximate | 6.76 | % |
| X21.9c | Cm/C0 | 0.0571 |  |
| X21.9d | PA output power | 28.5 | dBm |
| X21.9m | carrier at the LNA | −21.5 | dBm |
| X21.9n | receive-band isolation needed | 38 | dB |
| X21.9e | switch figure of merit | 240 | fs |
| X21.9f | cut-off frequency | 663 | GHz |
| X21.9g | on-state loss | 0.206 | dB |
| X21.9h | off-state isolation | 13.36 | dB |
| X21.9i | peak voltage | 14.13 | V |
| X21.9j | worst-case peak | 22.60 | V |
| X21.9k | stacked transistors | 8 |  |
| X21.9l | mismatch loss at VSWR 4 | 1.94 | dB |
| X21.10a | EIRP at broadside | 49.12 | dBm |
| X21.10b | EIRP at 50° | 47.20 | dBm |
| X21.10c | beam direction at 37 GHz | 53.85 | ° |
| X21.10d | squint bandwidth, estimate | 11.28 | GHz |
| X21.10j | squint bandwidth, exact array factor | 11.35 | GHz |
| X21.10e | quantization gain loss, 2 bits | 0.912 | dB |
| X21.10f | quantization floor, 2 bits | −25.29 | dB |
| X21.10g | rms phase error, 2 bits | 25.98 | ° |
| X21.10k | floor, 4 bits | −36.99 | dB |
| X21.10l | floor, 5 bits | −43.00 | dB |
| X21.10m | fewest bits for a −40 dB floor | 5 |  |
| X21.10h | spacing at 42 GHz | 0.538 | λ |
| X21.10i | grating-lobe limit at 50° | 0.566 | λ |
| X21.11a | EIRP | −7 | dBm |
| X21.11b | sensitivity | −96 | dBm |
| X21.11c | shadowing margin | 7.69 | dB |
| X21.11d | MAPL | 68.81 | dB |
| X21.11e | 1 m path loss | 40.20 | dB |
| X21.11f | range | 8.99 | m |
| X21.11g | coded sensitivity | −111.0 | dBm |
| X21.11h | coded range | 28.5 | m |
| X21.12a | 80 MHz carrier | 1857.6 | Mb/s |
| X21.12b | 60 MHz carrier | 1386.8 | Mb/s |
| X21.12c | total | 3244.4 | Mb/s |
| X21.12d | Wi-Fi 7 rate | 2268.5 | Mb/s |
| X21.12e | UWB range error | 0.899 | m |
| X21.12f | longest reply time | 33.4 | µs |
| X21.12g | orbital speed | 7256 | m/s |
| X21.12h | line-of-sight speed | 6106 | m/s |
| X21.12i | Doppler at 2 GHz | 40.7 | kHz |
| X21.12j | Doppler in subcarriers | 2.72 |  |
| X21.13a | IIP3 − P1dB | 9.64 | dB |
| X21.13b | P1dB | −19.64 | dBm |
| X21.13c | cascade noise temperature | 244.5 | K |
| X21.13d | optimal element count | 316 |  |
| X21.13e | minimum DC power | 31.62 | W |
| X21.13f | penalty at 2N* or N*/2 | 1.25 |  |
| X21.13g | Eb/N0 limit as η → 0 | −1.59 | dB |
| X21.13h | Eb/N0 at η = 2 | 1.76 | dB |
| X21.13i | Eb/N0 at η = 6 | 10.21 | dB |
| X21.14a | largest Ron | 2.33 | Ω |
| X21.14b | largest Coff | 4.55 | fF |
| X21.14c | required figure of merit | 10.6 | fs |
| X21.14d | improvement over 100 fs | 9.4 |  |
| X21.14e | PA peak power | 35.64 | dBm |
| X21.14l | PA peak power | 3.66 | W |
| X21.14f | DC power at 45% | 884.7 | mW |
| X21.14g | battery current | 232.8 | mA |
| X21.14h | DC power, class B | 1363 | mW |
| X21.14i | DC power, Doherty | 725.1 | mW |
| X21.14j | system NF, claimed switch | 2.86 | dB |
| X21.14k | system NF, 0.5 dB switch | 3.16 | dB |
| X21.14m | system NF above the LNA NF, claimed switch | 1.86 | dB |
