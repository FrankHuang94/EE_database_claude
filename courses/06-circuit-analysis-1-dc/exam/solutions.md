# Course 06 · Final Exam — Solutions

Exam: [README.md](README.md). All numbers are recomputed by [verify_06_exam.py](../verify/verify_06_exam.py), and every circuit answer (Questions 3, 4, 5, 6, 7, 8, 10, 11, 12, 13 and 14) is confirmed in ngspice by [exam_circuits.cir](exam_circuits.cir). Each solution names the chapter to revisit if you lost points.

**1.** *(06-01)* (a) $p = vi = 12\times(-0.5) = $ **−6 W** absorbed: the device delivers 6 W, so it is a **source**.

(b) $3\ \text{Ah}\times3600\ \text{s/h} = $ **10,800 C**.

(c) \$3.7\ \text{V}\times3\ \text{Ah} = \$ **11.1 Wh** $= 11.1\times3600$ J = **39.96 kJ**.

(d) $11.1/1.5 = $ **7.4 h**.

**2.** *(06-02)* (a) $R/R_0 = 1 + \alpha\Delta T$ gives $\Delta T = (2.472/2.000 - 1)/0.00393 = 60.05$ °C, so the winding is at **80.05 °C**. Measuring a winding's resistance is a standard way to measure its average temperature.

(b) $V_{max} = \sqrt{PR} = \sqrt{0.25\times10^4} = $ **50 V**; $I_{max} = \sqrt{P/R} = \sqrt{0.25/100} = $ **50 mA**.

(c) $4.7\times0.95 = $ **4.465 kΩ** to $4.7\times1.05 = $ **4.935 kΩ**.

**3.** *(06-03, 06-11)* (a) $12\times4/12 = $ **4 V**.

(b) $R_2\parallel R_L = 2$ kΩ, so \$12\times2/(8 + 2) = \$ **2.4 V**.

(c) The divider's Thévenin resistance is $8\parallel4 = 2.667$ kΩ; the loading error $R_{th}/(R_{th} + R_L)$ stays below 1% if \$R_L \ge 99R_{th} = \$ **264.0 kΩ**.

(d) The parallel resistance is 1 kΩ, so the voltage is 6 V, and the currents are **3 mA**, **2 mA** and **1 mA**: inversely proportional to resistance.

**4.** *(06-04)* (a) Nodes 1 and 2 form a supernode. In kΩ, mA and V, its KCL and the other two equations are

$$
\begin{bmatrix} 1 & -1 & 0\\ \tfrac12 & \tfrac14 + \tfrac12 & -\tfrac12\\ 0 & -\tfrac12 & 1 + \tfrac12 \end{bmatrix}
\begin{bmatrix} v_1\\ v_2\\ v_3 \end{bmatrix} =
\begin{bmatrix} 6\\ 3\\ 1 \end{bmatrix}.
$$

The first row is the constraint $v_1 - v_2 = 6$; the second is KCL for the supernode (3 mA in, leaving through R1, R2 and R3); the third is KCL at node 3.

(b) Substituting $v_1 = v_2 + 6$ into the supernode equation gives $1.25v_2 = 0.5v_3$, so $v_3 = 2.5v_2$; node 3 then gives $3.25v_2 = 1$. Hence **$v_2$ = 0.3077 V**, **$v_3$ = 0.7692 V** and **$v_1$ = 6.308 V**.

(c) KCL at node 1: 3 mA enters from I1 and $v_1/2 = 3.154$ mA leaves through R1, so 0.1538 mA flows *out of* V1's + terminal into node 1. V1 delivers \$6\times0.1538 = \$ **0.9231 mW**.

**5.** *(06-05)* (a) The current source is shared by meshes 2 and 3 and points up, against mesh 2's clockwise direction and with mesh 3's: $i_3 - i_2 = 1$. Mesh 1: $12 = 2i_1 + 4(i_1 - i_2)$. The supermesh around meshes 2 and 3 (avoiding the current source): $0 = 4(i_2 - i_1) + 3i_2 + 6i_3$. Substituting $i_3 = i_2 + 1$ gives $13i_2 - 4i_1 = -6$; with $6i_1 - 4i_2 = 12$, **$i_1$ = 2.129 A**, **$i_2$ = 0.1935 A** and **$i_3$ = 1.194 A**.

(b) R4 carries $i_1 - i_2$ downward: \$4\times1.935 = \$ **7.742 V**.

(c) V1 delivers \$12\times2.129 = \$ **25.55 W**. The current source's voltage (node 3 to 0) is $6i_3 = 7.161$ V, and it pushes 1 A up into node 3, so it delivers **7.161 W**. Check: the resistors absorb $2(2.129)^2 + 4(1.935)^2 + 3(0.1935)^2 + 6(1.194)^2 = 32.71$ W, equal to $25.55 + 7.161$.

**6.** *(06-06)* (a) KVL from b through $r_\pi$ and $R_E$: $v_b = i_br_\pi + (\beta + 1)i_bR_E$, so \$R_{in} = r_\pi + (\beta + 1)R_E = 2.5 + 101\times0.2 = \$ **22.7 kΩ**: the emitter resistor appears multiplied by $\beta + 1$.

(b) $i_b = v_s/(R_s + R_{in})$ and $v_c = -\beta i_bR_C$, so \$v_c/v_s = -100\times4/23.7 = \$ **−16.88**.

(c) With $R_E$ shorted, $R_{in} = 2.5$ kΩ and the gain is \$-100\times4/3.5 = \$ **−114.3**. $R_E$ trades gain (about 7×) for a much higher input resistance and a gain set mostly by $R_C/R_E$ rather than by β, which varies from part to part (degeneration, Course 10).

**7.** *(06-07)* (a) V1 alone (I1 open): \$10\times3/5 = \$ **6 V**. I1 alone (V1 shorted): \$3\ \text{mA}\times(2\parallel3) = \$ **3.6 V**. Total **$v_x$ = 9.6 V**.

(b) \$9.6^2/3\ \text{kΩ} = \$ **30.72 mW**, while the separate powers are $6^2/3 = 12$ mW and $3.6^2/3 = 4.32$ mW, summing to **16.32 mW**. Power is quadratic, so it does not superpose; superpose voltages or currents, then compute power.

(c) Linearity: V1's contribution doubles to 12 V, so $v_x$ = **15.6 V**.

(d) *(06-07, source transformation)* 10 V behind 2 kΩ becomes \$10/2 = \$ **5 mA** in parallel with 2 kΩ. Together with I1, 8 mA flows into $2\parallel3 = 1.2$ kΩ: \$v_x = 8\times1.2 = \$ **9.6 V**, as in (a).

**8.** *(06-08)* (a) With the port open, no current flows in R3 or the CCVS, so R1 and R2 form a divider: $v_a = 12\times3/9 = 4$ V, $i_x = 4/3$ mA, and $v_b = v_a + 2000\times(4/3\times10^{-3}) = 4 + 2.667$. The port voltage is **$V_{oc}$ = 6.667 V**.

(b) Turn off the *independent* source (V1 → short) and drive the port with a test current $I_t$ into node out. It flows through R3 and the CCVS into node a, and then splits between R1 and R2, now in parallel to ground: $v_a = I_t(6\parallel3) = 2I_t$ (kΩ), $i_x = v_a/3 = \tfrac23I_t$, and $v_b = v_a + 2i_x = 2I_t + \tfrac43I_t$ (the CCVS's 2000 V/A is 2 kΩ in these units). Then $v_{out} = v_b + 1\times I_t = \tfrac{13}{3}I_t$, so **$R_{th}$ = 4.333 kΩ**. The dependent source must stay because it is controlled by a current that the test source itself creates; zeroing it would give the wrong answer, 3 kΩ.

(c) $I_{sc} = V_{oc}/R_{th} = $ **1.538 mA**; $P_{max} = V_{oc}^2/(4R_{th}) = $ **2.564 mW**.

**9.** *(06-09)* (a) $R_L = R_{th}$ = **0.5 Ω**; \$P_{max} = 48^2/(4\times0.5) = \$ **1152 W**, at 50% efficiency.

(b) $\eta = R_L/(R_L + R_{th}) = 0.9$ gives $R_L$ = **4.5 Ω**, receiving \$48^2\times4.5/5^2 = \$ **414.7 W**, **36%** of the maximum ($4\eta(1 - \eta) = 0.36$).

(c) **Zero** source resistance: then the load receives $48^2/2$ = 1152 W. Maximum power transfer chooses the *load* for a *given* source; when the source can be chosen, lower source resistance always delivers more power to a fixed load.

**10.** *(06-10)* (a) Gain $-33/2.2 = $ **−15**; output $-15\times(-0.2) = $ **+3 V**.

(b) $1 + R_2/1 = 16$ gives $R_2$ = **15 kΩ**.

(c) $R_1 = R_f/1 = $ **20 kΩ** and $R_2 = R_f/2 = $ **10 kΩ**; output $-(0.5 + 2\times(-1)) = $ **+1.5 V**.

(d) Directly, the 10 kΩ input and the 90 kΩ source form a divider: $1\times10/100 = $ **0.1 V**. A follower draws no input current, so its input sits at the full 1 V and its output delivers **1 V** to the 10 kΩ from zero output resistance.

**11.** *(06-10)* (a) $G = 5$: \$5\times0.020 = \$ **0.1 V**.

(b) $v_+ = 2.5\times50.5/60.5 = 2.0868$ V and \$v_{out} = 2.0868\times6 - 2.5\times5 = \$ **20.66 mV**. The common-mode gain is \$0.02066/2.5 = \$ **0.008264**, and the CMRR is \$5/0.008264 = \$ **605**, or **55.6 dB**.

(c) $(1 + G)/(4t) = 6/0.04 = 150$, or **43.5 dB**: four resistors at their worst are four times worse than one.

**12.** *(06-10, 06-06)* (a) \$G = 50/(1 + 50/(2\times10^4)) = \$ **49.88**, an error of **0.249%** (noise gain over $A$); the output is \$49.875\times20\ \text{mV} = \$ **0.9975 V**.

(b) Offset: \$\pm2\ \text{mV}\times50 = \$ **±100 mV** (sign varies by unit). Bias current into the − input: it is drawn from the output through $R_2$, so \$v_{out} = +I_BR_2 = \$ **+4.9 mV**. Bias current into the + input: drawn from the source through 5 kΩ, so $v_+ = -I_BR_s$ and \$v_{out} = -I_BR_s\times50 = \$ **−25 mV**.

(c) Sum of magnitudes: **129.9 mV**. Signed: the bias terms give $4.9 - 25 = -20.1$ mV, and the worst case adds the offset in the same direction: **120.1 mV**.

(d) \$120.1/997.5 = \$ **12.0%** of the signal. The offset dominates: use a precision (low-offset) op-amp. Then balance the resistances the two inputs see. The − input sees $R_1\parallel R_2 = 0.98$ kΩ against 5 kΩ at the + input; scaling $R_1$ and $R_2$ up about fivefold (5.1 kΩ and 249.9 kΩ keep the gain at 50) makes $R_1\parallel R_2 \approx 5$ kΩ, and the two bias terms then cancel except for the offset current times $R_2$. (Buffering the sensor would not help: with zero source resistance the + term vanishes but the − term, +4.9 mV, remains.)

**13.** *(06-11)* (a) $3.3\times10/10.22 = $ **3.229 V**, **−2.15%**; corrected $3.229\times(1 + 0.22/10) = $ **3.300 V**.

(b) $5/102.5 = $ **48.78 mA**, **−2.44%**; burden $48.78\ \text{mA}\times2.5\ \Omega = $ **122.0 mV**.

(c) $0.001\times2.500 + 2\times0.001 = $ **±4.5 mV**, or **0.18%** of the reading.

**14.** *(06-03, 06-10, 06-11)* (a) Take the bridge as two dividers across $V_{ex}$: the reference half gives $V_{ex}/2$ and the gauge half (gauge on the bottom) gives $V_{ex}R(1 + x)/(R + R(1 + x))$. Their difference is

$$
v_o = V_{ex}\Bigl(\frac{1 + x}{2 + x} - \frac12\Bigr) = V_{ex}\,\frac{x}{2(2 + x)} \approx \frac{V_{ex}x}{4}\quad(x \ll 2).
$$

(b) Exact $5\times10^{-3}/(2\times2.001) = $ **1.2494 mV**; approximation **1.25 mV**; nonlinearity $1/(1 + x/2) - 1 \approx $ **−0.050%**.

(c) $G = 1 + 2\times24.7/0.0247 = $ **2001**; output $2001\times1.2494\ \text{mV} = $ **2.500 V**.

(d) Error $= v_{cm}G/\text{CMRR} = 2.5\times2001/10^5 = $ **50.0 mV** at the output, **2.0%** of the signal: even 100 dB is not much at a gain of 2001 with 2.5 V of common mode.

(e) The leads and the bridge's 350 Ω form a divider: $5\times350/351 = $ **4.986 V** across the bridge, a gain error of **−0.285%**. Cures: sense the excitation at the bridge (six-wire connection, 06-11's remote sensing), or measure ratiometrically, referencing the ADC to the bridge's own excitation.

**15.** *(Diligence; 06-11, 06-11, 06-11, 06-10)* Rubric: 2 points per claim, 1 for what is wrong or missing and 1 for a pointed question (8 in total).

(a) Resolution is not accuracy. A 24-bit converter's last bits are noise; offset, gain error, reference drift, the front end's offset and bias errors, and resistor tolerances usually dominate by orders of magnitude. *Ask:* "What is the total error budget over temperature, and the effective number of bits at your bandwidth?"

(b) The ±1% is the part's tolerance at 25 °C at its Kelvin terminals. Over temperature, add its TCR (up to hundreds of ppm/°C at the lowest values), self-heating, any copper in the sense path (+0.39%/°C) and the amplifier's offset, which dominates at low current. *Ask:* "Is the layout Kelvin, and what is the error at 10% of full scale over the full temperature range?"

(c) A supply regulates where it senses. Without remote sensing, the cable and connector drop at full current are subtracted at the load. *Ask:* "Where are the sense points, and what voltage did you measure at the load at maximum current and temperature?"

(d) 1 µV is probably typical, not maximum; the offset is multiplied by the noise gain; bias current times source resistance, resistor tolerances, drift and noise add. *Ask:* "What is the worst-case input-referred error over temperature, with every term listed?"

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X06.1a | power absorbed | −6 | W |
| X06.1b | charge | 10800 | C |
| X06.1c | energy | 11.1 | Wh |
| X06.1d | energy | 39.96 | kJ |
| X06.1e | run time at 1.5 W | 7.4 | h |
| X06.2a | winding temperature | 80.05 | °C |
| X06.2b | maximum voltage, 10 kΩ 0.25 W | 50 | V |
| X06.2c | maximum current, 100 Ω 0.25 W | 50 | mA |
| X06.2d | minimum of 4.7 kΩ ±5% | 4.465 | kΩ |
| X06.2e | maximum of 4.7 kΩ ±5% | 4.935 | kΩ |
| X06.3a | unloaded output | 4 | V |
| X06.3b | loaded output | 2.4 | V |
| X06.3c | smallest load for 1% | 264.0 | kΩ |
| X06.3d | current in 2 kΩ | 3 | mA |
| X06.3e | current in 3 kΩ | 2 | mA |
| X06.3f | current in 6 kΩ | 1 | mA |
| X06.4a | v_1 | 6.308 | V |
| X06.4b | v_2 | 0.3077 | V |
| X06.4c | v_3 | 0.7692 | V |
| X06.4d | power delivered by V1 | 0.9231 | mW |
| X06.5a | i_1 | 2.129 | A |
| X06.5b | i_2 | 0.1935 | A |
| X06.5c | i_3 | 1.194 | A |
| X06.5d | voltage across R4 | 7.742 | V |
| X06.5e | power delivered by V1 | 25.55 | W |
| X06.5f | power delivered by I1 | 7.161 | W |
| X06.5g | power absorbed by the resistors | 32.71 | W |
| X06.6a | resistance into the base | 22.7 | kΩ |
| X06.6b | voltage gain | −16.88 | — |
| X06.6c | gain with R_E shorted | −114.3 | — |
| X06.7a | contribution of V1 | 6 | V |
| X06.7b | contribution of I1 | 3.6 | V |
| X06.7c | v_x | 9.6 | V |
| X06.7d | power in R2 | 30.72 | mW |
| X06.7e | sum of separate powers | 16.32 | mW |
| X06.7f | v_x with V1 doubled | 15.6 | V |
| X06.7g | Norton current of V1 and R1 | 5 | mA |
| X06.7h | v_x from the Norton form | 9.6 | V |
| X06.8a | open-circuit voltage | 6.667 | V |
| X06.8b | Thévenin resistance | 4.333 | kΩ |
| X06.8c | short-circuit current | 1.538 | mA |
| X06.8d | maximum power | 2.564 | mW |
| X06.9a | load for maximum power | 0.5 | Ω |
| X06.9b | maximum power | 1152 | W |
| X06.9c | load for 90% efficiency | 4.5 | Ω |
| X06.9d | power at 90% efficiency | 414.7 | W |
| X06.9e | fraction of maximum | 36 | % |
| X06.10a | inverting gain | −15 | — |
| X06.10b | output for −0.2 V | 3 | V |
| X06.10c | R_2 for gain 16 | 15 | kΩ |
| X06.10d | R_1 of the summer | 20 | kΩ |
| X06.10e | R_2 of the summer | 10 | kΩ |
| X06.10f | summer output | 1.5 | V |
| X06.10g | input voltage without a buffer | 0.1 | V |
| X06.10h | input voltage with a follower | 1 | V |
| X06.11a | output | 0.1 | V |
| X06.11b | common-mode output | 20.66 | mV |
| X06.11c | common-mode gain | 0.008264 | — |
| X06.11d | CMRR | 605 | — |
| X06.11e | CMRR in dB | 55.6 | dB |
| X06.11f | worst-case CMRR in dB | 43.5 | dB |
| X06.12a | closed-loop gain | 49.88 | — |
| X06.12b | gain error | 0.249 | % |
| X06.12c | output signal | 0.9975 | V |
| X06.12d | offset term | 100 | mV |
| X06.12e | bias term at − | 4.9 | mV |
| X06.12f | bias term at + | −25 | mV |
| X06.12g | sum of magnitudes | 129.9 | mV |
| X06.12h | signed worst case | 120.1 | mV |
| X06.12i | signed worst case relative to the signal | 12.0 | % |
| X06.13a | reading | 3.229 | V |
| X06.13b | error | −2.15 | % |
| X06.13c | corrected value | 3.300 | V |
| X06.13d | ammeter reading | 48.78 | mA |
| X06.13e | ammeter error | −2.44 | % |
| X06.13f | burden voltage | 122.0 | mV |
| X06.13g | uncertainty | 4.5 | mV |
| X06.13h | relative uncertainty | 0.18 | % |
| X06.14a | exact bridge output | 1.2494 | mV |
| X06.14b | approximate output | 1.25 | mV |
| X06.14c | nonlinearity | −0.050 | % |
| X06.14d | in-amp gain | 2001 | — |
| X06.14e | in-amp output | 2.500 | V |
| X06.14f | common-mode error | 50.0 | mV |
| X06.14g | common-mode error relative to the signal | 2.0 | % |
| X06.14h | voltage across the bridge | 4.986 | V |
| X06.14i | gain error from the leads | −0.285 | % |
