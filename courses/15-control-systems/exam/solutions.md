# Course 15 · Final Exam Solutions (Control Systems)

Exam: [README.md](README.md). Every number below is recomputed by [verify_15_exam.py](../verify/verify_15_exam.py):

- polynomial roots, Routh arrays and margins by root finding;
- time responses from exact step responses;
- designs from their formulas, each confirmed by the margins or poles of the resulting loop.

---

## Solutions

### Solution 1

(a) $T = T_A + PR$ = 25 + 20 × 2.5 = **75** °C.

(b) $\tau = RC$ = 2.5 × 4 = **10** s.

(c) $T(10\ \text{s}) = 25 + 50(1 - e^{-1})$ = **56.6** °C.

(d) A rise $\delta T$ adds $0.1\,\delta T$ watts, which raises the temperature by $2.5 \times 0.1\,\delta T$: $G = R\,dP/dT$ = **0.25**. Deviations decay with $\tau/(1 - G) = 10/0.75$ = **13.3** s: the positive feedback slows recovery, and at $G = 1$ the die would run away (15-01).

### Solution 2

(a) $T = KP/(1 + KP) = \dfrac{10K}{s^2 + 2s + 10K}$.

(b) For $K$ = 1: $\omega_n = \sqrt{10}$ = **3.162** rad/s and $2\zeta\omega_n = 2$, so $\zeta = 1/\sqrt{10}$ = **0.316**.

(c) $Y/D = P/(1 + KP) = 10/(s^2 + 2s + 10K)$. By the final value theorem, the steady output for a unit step is its DC value $1/K$ = **1**. The plant's integrator does not reject a disturbance entering before it; only an integrator upstream of the disturbance does (15-04).

(d) $S = 1/(1 + L) = s(s + 2)/(s^2 + 2s + 10)$. At $s = j$: $\lvert j(2 + j)\rvert/\lvert 9 + 2j\rvert = \sqrt5/\sqrt{85}$ = **0.243**. Output disturbances at 1 rad/s are attenuated to about a quarter.

### Solution 3

(a) $\text{OS} = e^{-\pi\zeta/\sqrt{1 - \zeta^2}} = e^{-\pi/3}$ = **35.1**%.

(b) $t_p = \pi/(\omega_n\sqrt{1 - \zeta^2}) = \pi/3$ = **1.047** s.

(c) $4/(\zeta\omega_n) = 4/1$ = **4.0** s. (The exact 2% settling time is 3.54 s; the estimate uses the envelope and is conservative here.)

(d) 10% overshoot needs $\zeta = -\ln0.1/\sqrt{\pi^2 + \ln^20.1}$ = 0.591. Since $2\zeta\omega_n = 2$ is fixed, $\omega_n = 1/0.591 = 1.692$ rad/s and $K = \omega_n^2/10$ = **0.286**.

### Solution 4

(a) $L = 20(s + 2)/[s(s + 4)(s + 10)]$ has one pole at the origin: **type 1**. $K_p = \infty$, $K_v = \lim sL = 20 \times 2/(4 \times 10)$ = **1** s⁻¹ and $K_a$ = **0**.

(b) Step: **0**. Ramp: $1/K_v$ = **1**. Parabola: **unbounded**.

(c) The characteristic polynomial is $s(s + 4)(s + 10) + 20(s + 2) = s^3 + 14s^2 + 60s + 40$. Routh's first column is 1, 14, $(14 \times 60 - 40)/14$ = **57.14**, 40: no sign changes, so it is stable.

(d) $Y/D = P/(1 + CP) = 1/[s(s + 4) + C(s)]$, whose DC value is $1/C(0) = 1/4$ = **0.25**. The plant's integrator sits after the disturbance, so it does not reject it. Adding integral action to $C$ (an integrator before the disturbance's entry point) makes the steady output zero, at a cost in phase that must be checked.

### Solution 5

(a) Rows: $s^4$: 1, 3, $K$; $s^3$: 2, 2; $s^2$: $(2 \times 3 - 2)/2 = 2$, $K$; $s^1$: $(2 \times 2 - 2K)/2 = 2 - K$; $s^0$: $K$.

(b) All first-column entries positive: $0 < K <$ **2**.

(c) At $K$ = 2 the $s^1$ row vanishes; the auxiliary polynomial $2s^2 + 2$ gives $s = \pm j$: **1** rad/s.

(d) For $K$ = 3 the first column is 1, 2, 2, −1, 3: two sign changes, so **2** right-half-plane poles.

### Solution 6

(a) Centroid $(0 - 2 - 4)/3$ = **−2**; angles **60°**, **180°** and 300° (that is, ±60° and 180°).

(b) $dK/ds = 0$ with $K = -s(s + 2)(s + 4)$: $3s^2 + 12s + 8 = 0$, $s = -2 \pm 2/\sqrt3$. The point on the locus (between 0 and −2) is **−0.845**, where $K = \lvert s(s + 2)(s + 4)\rvert$ = **3.08**.

(c) The characteristic polynomial is $s^3 + 6s^2 + 8s + K$; Routh gives $6 \times 8 = K$: $K$ = **48**, with the auxiliary $6s^2 + 48 = 0$, $\omega = \sqrt8$ = **2.828** rad/s.

(d) On the ray $\zeta$ = 0.5 the pair is $s = r(-0.5 \pm j0.866)$, the roots of $s^2 + rs + r^2$. With the third pole at $-p$, match coefficients: $(s^2 + rs + r^2)(s + p) = s^3 + (r + p)s^2 + (r^2 + pr)s + pr^2$ must equal $s^3 + 6s^2 + 8s + K$. So $r + p = 6$ and $r^2 + pr = r(r + p) = 6r = 8$: $r = 4/3$ and $p = 14/3$. The pair is at **−0.667 ± j1.155** (ω_n = 4/3 rad/s), the third pole at **−4.667**, and $K = pr^2 = (14/3)(16/9) = 224/27$ = **8.30**.

### Solution 7

(a) $\lvert L(j\omega)\rvert = 1$ means $\omega^2(\omega^2 + 4)(\omega^2 + 100) = 1600$. With $x = \omega^2$: $x^3 + 104x^2 + 400x - 1600 = 0$. Newton's method from $x_0$ = 2 ($x_{k+1} = x_k - f/f'$ with $f' = 3x^2 + 208x + 400$) gives 2.454, 2.4296, 2.4295, so $\omega_c = \sqrt{2.4295}$ = **1.559** rad/s. The phase there is $-90° - \arctan(\omega_c/2) - \arctan(\omega_c/10)$, so PM = **43.2**°.

(b) The phase is −180° where $\arctan(\omega/2) + \arctan(\omega/10) = 90°$, that is $\omega^2 = 20$: $\omega_{180}$ = **4.472** rad/s. There $\lvert L\rvert = 40/(\sqrt{20}\sqrt{24}\sqrt{120}) = 1/6$, so GM = **6** (**15.6** dB).

(c) PM in radians is $43.2° \times \pi/180$ = **0.754** rad, so the delay margin is $0.754/1.559$ = **0.484** s.

(d) The open loop has no right-half-plane poles ($P$ = 0; the pole at the origin is indented around). As given, the plot crosses the negative real axis at $-1/6$, to the right of −1: **0** encirclements, so $Z = N + P$ = **0** closed-loop poles in the right half-plane. With 8 times the gain the crossing moves to $-8/6 = -1.33$, left of −1, and the plot circles −1 clockwise **2** times: $Z$ = **2** unstable closed-loop poles. (Routh agrees: $s^3 + 12s^2 + 20s + 40k$ needs $12 \times 20 > 40k$, that is $k < 6$.)

### Solution 8

(a) The plant's phase is $-3\arctan\omega$, which reaches −180° at $\arctan\omega = 60°$, $\omega = \sqrt3$ rad/s. There its magnitude is $1/(1 + 3)^{3/2} = 1/8$, so a proportional gain of $K_u$ = **8** brings the loop to the edge of oscillation at $\sqrt3$ rad/s: $P_u = 2\pi/\sqrt3$ = **3.628** s. (Routh on $s^3 + 3s^2 + 3s + 1 + K$ gives the same: $9 > 1 + K$.)

(b) $K_p$ = **4.8**, $T_i$ = **1.814** s, $T_d$ = **0.4534** s; $K_i = K_p/T_i$ = **2.646** s⁻¹ and $K_d = K_pT_d$ = **2.177** s.

(c) While the actuator is saturated, the loop is open: the error stays large and the integrator keeps accumulating, so when the output finally reaches the setpoint the integrator holds far too much and the response overshoots badly and recovers slowly. Remedies: stop integrating while saturated (clamping, or a velocity-form controller whose output is clamped), or back-calculation, which feeds the difference between the commanded and the saturated output back into the integrator with a tracking time constant (15-08).

### Solution 9

(a) $K_v = \lim sKP = 2K$, so $K$ = **10** and $L = 40/[s(s + 2)]$. Crossover: $\omega^2(\omega^2 + 4) = 1600$, so $\omega_c$ = **6.17** rad/s, and PM = $90° - \arctan(6.17/2)$ = **18.0**°.

(b) $\phi_{max} = 50 - 18.0 + 10$ = **42.0**°, and $\alpha = (1 + \sin\phi_{max})/(1 - \sin\phi_{max})$ = **5.05**.

(c) The lead adds $10\log_{10}\alpha$ dB at $\omega_m$, so $\omega_m$ is where $\lvert L\rvert = 1/\sqrt\alpha$: $\omega^2(\omega^2 + 4) = 1600\alpha$, giving $\omega_m$ = **9.38** rad/s. Then $T = 1/(\omega_m\sqrt\alpha)$ = **0.0474** s; the zero is at $1/(\alpha T)$ = **4.17** rad/s and the pole at $1/T$ = **21.1** rad/s.

(d) At $\omega_m$ the compensated loop's magnitude is $\sqrt\alpha \times (1/\sqrt\alpha) = 1$, so 9.38 rad/s is the new crossover, and the phase there is $-90° - \arctan(9.38/2) + \phi_{max} = -90° - 77.96° + 42.04°$. PM = 180° − 125.9° = **54.1**°, above the 50° target. (The 10° allowance pays for the extra lag of $KP$ at the higher crossover, $77.96° - 72.04°$ = 5.9°, so 4° of it is left over.)

### Solution 10

(a) $\det(sI - A) = s^2 + 3s + 2$: eigenvalues **−1** and **−2**, and $G(s) = C(sI - A)^{-1}B = 1/(s^2 + 3s + 2)$.

(b) $[B\ \ AB] = \begin{bmatrix} 0 & 1 \\ 1 & -3 \end{bmatrix}$ has determinant −1 ≠ 0: rank 2, **controllable**.

(c) $A - BK = \begin{bmatrix} 0 & 1 \\ -2 - k_1 & -3 - k_2 \end{bmatrix}$ has characteristic polynomial $s^2 + (3 + k_2)s + 2 + k_1$. Matching $(s + 4)^2 + 16 = s^2 + 8s + 32$: $k_1$ = **30**, $k_2$ = **5**. With $u = -K\mathbf{x} + Nr$, $Y/R = N/(s^2 + 8s + 32)$, so $N$ = **32**.

(d) $A - LC = \begin{bmatrix} -l_1 & 1 \\ -2 - l_2 & -3 \end{bmatrix}$ has characteristic polynomial $s^2 + (3 + l_1)s + 3l_1 + 2 + l_2$. Matching $(s + 10)^2 = s^2 + 20s + 100$: $l_1$ = **17**, $l_2$ = 100 − 2 − 51 = **47**.

### Solution 11

(a) $z = e^{sT} = e^{-0.1}e^{j0.2}$: magnitude **0.905**, angle 0.2 rad = **11.46**°.

(b) $G(z) = (1 - e^{-0.3})/(z - e^{-0.3})$ = **0.2592**/(z − **0.7408**).

(c) $u_k = u_{k-1} + (K_p + K_iT/2)e_k + (-K_p + K_iT/2)e_{k-1} = u_{k-1} +$ **2.1**$e_k$ **− 1.9**$e_{k-1}$.

(d) $\omega_cT/2 = 10 \times 0.01$ = 0.1 rad = **5.73**°.

### Solution 12

(a) $\sqrt b = \tan50° + \sec50° = 1.192 + 1.556$ = **2.747** and $b$ = **7.549**.

(b) With $\omega_c = 2\pi \times 500$ kHz = 3.1416 × 10⁶ rad/s: $\tau_z = \sqrt b/\omega_c$ = **0.8745** µs, $\tau_p = 1/(\sqrt b\,\omega_c)$ = **0.1159** µs, and $K = \omega_c^2/\sqrt b$ = **3.592 × 10¹²** s⁻².

(c) $C + C_2 = I_{cp}K_v/(2\pi NK) = 2 \times 10^{-4} \times 4 \times 10^8/(40 \times 3.592 \times 10^{12})$ = **556.8** pF; $C_2 = 556.8/7.549$ = **73.76** pF; $C$ = **483.0** pF; $R = \tau_z/C$ = **1.811** kΩ.

(d) $\pi f_c/f_{ref} = \pi/40$ rad = **4.5**°; $f_c = f_{ref}/40$ is well inside the $f_{ref}/10$ rule.

### Solution 13

**(a)** With unity feedback, $E = R/(1 + L)$. For a unit ramp $R = 1/s^2$, and the final value theorem (valid because the closed loop is stable) gives

$$
e_{ss} = \lim_{s \to 0} s\,\frac{1}{s^2}\,\frac{1}{1 + L(s)} = \lim_{s \to 0}\frac{1}{s + sL(s)} = \frac{1}{\lim_{s \to 0}sL(s)} = \frac{1}{K_v} ,
$$

since $sL(s)$ tends to the finite nonzero $K_v$ for a type-1 loop and $s \to 0$. For Question 4, $K_v$ = 1 s⁻¹, so $e_{ss}$ = **1**.

**(b)** The phase is $\phi(\omega) = \arctan(\alpha\omega T) - \arctan(\omega T)$. Setting $d\phi/d\omega = \alpha T/(1 + \alpha^2\omega^2T^2) - T/(1 + \omega^2T^2) = 0$ gives $\alpha(1 + \omega^2T^2) = 1 + \alpha^2\omega^2T^2$, so $\omega^2T^2 = 1/\alpha$ and $\omega_m = 1/(T\sqrt\alpha)$, the geometric mean of the zero and pole frequencies. There, with $\tan(a - b) = (\tan a - \tan b)/(1 + \tan a\tan b)$, $\tan\phi_{max} = (\sqrt\alpha - 1/\sqrt\alpha)/2 = (\alpha - 1)/(2\sqrt\alpha)$, which is equivalent to $\sin\phi_{max} = (\alpha - 1)/(\alpha + 1)$ (a right triangle with legs $\alpha - 1$ and $2\sqrt\alpha$ has hypotenuse $\alpha + 1$). For $\alpha$ = 4: $\phi_{max} = \arcsin(3/5)$ = **36.87**° at $\omega_m = 1/(0.05 \times 2)$ = **10** rad/s.

**(c)** At $s = j\omega$, factor $e^{-j\omega T/2}$ out of the numerator:

$$
H(j\omega) = \frac{e^{-j\omega T/2}\left(e^{j\omega T/2} - e^{-j\omega T/2}\right)}{j\omega T} = e^{-j\omega T/2}\,\frac{2j\sin(\omega T/2)}{j\omega T} = e^{-j\omega T/2}\,\frac{\sin(\omega T/2)}{\omega T/2} .
$$

For $0 < \omega T/2 < \pi$, that is below the sampling frequency $2\pi/T$, the sinc factor is positive and real, so the phase is exactly $-\omega T/2$ and the magnitude is $\sin(\omega T/2)/(\omega T/2)$. At $\omega$ = 50 rad/s and $T$ = 10 ms: $\omega T/2$ = 0.25 rad, a phase of **−14.32**° and a magnitude of **0.990**.

### Solution 14

**(a)** The delay is $1.5/(2\ \text{MHz})$ = 0.75 µs, costing $360° \times f \times 0.75\ \mu\text{s}$. At 1 MHz: **270**°, far more than any loop can afford: the claim is physically impossible for this architecture. For at most 30°: $f_c = 30/(360 \times 0.75 \times 10^{-6})$ = **111** kHz.

**(b)** Load line: $\Delta V = \Delta I/(\omega_cC) = 5/(2\pi \times 5 \times 10^4 \times 2 \times 10^{-4})$ = **79.6** mV. Critically damped PI: its crossover is $1.029\,\omega_0$ with $\omega_0 = g/C$, so at a 50 kHz crossover $\omega_0/2\pi$ = 48.6 kHz and the peak is $(2/e)\Delta I/(\omega_0C) = (2/e) \times 79.6 \times 1.029$ = **60.3** mV. Meeting 20 mV needs $f_c = \Delta I/(2\pi C\Delta V)$ = **199** kHz for a load line and $1.029 \times (2/e) \times 199$ = **151** kHz for the PI design, 4.0 and 3.0 times the stated crossover. Both also exceed the 111 kHz that the digital delay of (a) allows, so the droop claim and the architecture are inconsistent with each other, not merely optimistic. Either the capacitance, the crossover or the droop number is wrong, or the measurement excludes the fastest part of the step.

**(c)** $P_{sus} = (95 - 35)/12$ = **5** W. The claimed 12 W is **2.4** times what the thermal path can remove indefinitely; no algorithm changes the heat that must flow through 12 K/W. Prediction can only make the transition smoother or spend the thermal capacitance more cleverly.

**(d)** Rubric (3 points; any four well-chosen questions with strong answers earn full credit):

1. *"What is your measured loop crossover and phase margin, and what is the sample-to-PWM latency?"* Strong: Bode plots measured by injection, a delay budget consistent with (a). Evasive: "simulation shows 1 MHz".
2. *"Show a load-step measurement at the load, with the output capacitance and step slew rate stated."* Strong: a scope capture at the processor's sense point, capacitance including derating. Evasive: only the regulator's output pin or an unstated step edge.
3. *"What sustained power does the SoC reach after 10 minutes in a production phone at 35 °C?"* Strong: a thermal measurement with skin and junction temperatures. Evasive: a burst benchmark of under a minute.
4. *"What does 'predictive' predict, and what happens when the prediction is wrong?"* Strong: a model, its error bounds and a fallback limiter. Evasive: "AI-based".
5. *"How are the loops verified across process, temperature, load and capacitor tolerance?"* Strong: margin sweeps and corner data. Evasive: one typical-case plot.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| X15.1a | final temperature | 75 | °C |
| X15.1b | time constant | 10 | s |
| X15.1c | temperature at 10 s | 56.6 | °C |
| X15.1d | leakage loop gain | 0.25 | — |
| X15.1e | new time constant | 13.3 | s |
| X15.2a | natural frequency | 3.162 | rad/s |
| X15.2b | damping ratio | 0.316 | — |
| X15.2c | steady output from the disturbance | 1 | — |
| X15.2d | sensitivity magnitude at 1 rad/s | 0.243 | — |
| X15.3a | overshoot | 35.1 | % |
| X15.3b | peak time | 1.047 | s |
| X15.3c | settling estimate | 4.0 | s |
| X15.3d | exact settling time | 3.54 | s |
| X15.3e | damping for 10% overshoot | 0.591 | — |
| X15.3f | gain for 10% overshoot | 0.286 | — |
| X15.3g | natural frequency for 10% overshoot | 1.692 | rad/s |
| X15.4a | velocity error constant | 1 | 1/s |
| X15.4b | acceleration error constant | 0 | 1/s² |
| X15.4c | ramp error | 1 | — |
| X15.4d | Routh entry | 57.14 | — |
| X15.4e | steady output from the disturbance | 0.25 | — |
| X15.5a | upper gain limit | 2 | — |
| X15.5b | oscillation frequency | 1 | rad/s |
| X15.5c | right-half-plane poles at K = 3 | 2 | — |
| X15.6a | centroid | −2 | 1/s |
| X15.6b | asymptote angle | 60 | ° |
| X15.6c | breakaway point | −0.845 | 1/s |
| X15.6d | gain at breakaway | 3.08 | — |
| X15.6e | gain at the axis crossing | 48 | — |
| X15.6f | crossing frequency | 2.828 | rad/s |
| X15.6g | dominant pair | −0.667 + j1.155 | 1/s |
| X15.6h | gain for ζ = 0.5 | 8.30 | — |
| X15.6i | third pole | −4.667 | 1/s |
| X15.7a | gain crossover | 1.559 | rad/s |
| X15.7b | phase margin | 43.2 | ° |
| X15.7c | phase crossover | 4.472 | rad/s |
| X15.7d | gain margin | 6 | — |
| X15.7e | gain margin | 15.6 | dB |
| X15.7f | delay margin | 0.484 | s |
| X15.7g | closed-loop RHP poles, gain as given | 0 | — |
| X15.7h | clockwise encirclements, 8 × gain | 2 | — |
| X15.7i | closed-loop RHP poles, 8 × gain | 2 | — |
| X15.7j | PM in radians | 0.754 | rad |
| X15.7k | x = ω² at crossover | 2.4295 | rad²/s² |
| X15.8a | ultimate gain | 8 | — |
| X15.8b | ultimate period | 3.628 | s |
| X15.8c | Kp | 4.8 | — |
| X15.8d | Ti | 1.814 | s |
| X15.8e | Td | 0.4534 | s |
| X15.8f | Ki | 2.646 | 1/s |
| X15.8g | Kd | 2.177 | s |
| X15.9a | gain K | 10 | — |
| X15.9b | uncompensated crossover | 6.17 | rad/s |
| X15.9c | uncompensated phase margin | 18.0 | ° |
| X15.9d | required lead | 42.0 | ° |
| X15.9e | α | 5.05 | — |
| X15.9f | ωm | 9.38 | rad/s |
| X15.9g | T | 0.0474 | s |
| X15.9h | lead zero | 4.17 | rad/s |
| X15.9i | lead pole | 21.1 | rad/s |
| X15.9j | compensated phase margin | 54.1 | ° |
| X15.10a | slow eigenvalue | −1 | 1/s |
| X15.10b | fast eigenvalue | −2 | 1/s |
| X15.10c | k1 | 30 | — |
| X15.10d | k2 | 5 | — |
| X15.10e | N | 32 | — |
| X15.10f | l1 | 17 | — |
| X15.10g | l2 | 47 | — |
| X15.11a | pole magnitude | 0.905 | — |
| X15.11b | pole angle | 11.46 | ° |
| X15.11c | ZOH gain | 0.2592 | — |
| X15.11d | ZOH pole | 0.7408 | — |
| X15.11e | b0 | 2.1 | — |
| X15.11f | b1 | −1.9 | — |
| X15.11g | hold phase lag | 5.73 | ° |
| X15.12a | √b | 2.747 | — |
| X15.12k | crossover | 3.1416e6 | rad/s |
| X15.12b | b | 7.549 | — |
| X15.12c | τz | 0.8745 | µs |
| X15.12d | τp | 0.1159 | µs |
| X15.12e | K | 3.592e12 | 1/s² |
| X15.12f | C + C2 | 556.8 | pF |
| X15.12g | C2 | 73.76 | pF |
| X15.12h | C | 483.0 | pF |
| X15.12i | R | 1.811 | kΩ |
| X15.12j | sampling phase cost | 4.5 | ° |
| X15.13a | ramp error | 1 | — |
| X15.13b | maximum lead phase | 36.87 | ° |
| X15.13c | frequency of maximum phase | 10 | rad/s |
| X15.13d | hold phase at 50 rad/s | −14.32 | ° |
| X15.13e | hold magnitude at 50 rad/s | 0.990 | — |
| X15.14a | delay phase at 1 MHz | 270 | ° |
| X15.14i | total digital delay | 0.75 | µs |
| X15.14b | largest crossover for 30° | 111 | kHz |
| X15.14c | load-line droop | 79.6 | mV |
| X15.14d | PI droop | 60.3 | mV |
| X15.14e | crossover needed, load line | 199 | kHz |
| X15.14f | crossover needed, PI | 151 | kHz |
| X15.14g | sustained power | 5 | W |
| X15.14h | ratio of claimed to sustainable power | 2.4 | — |
