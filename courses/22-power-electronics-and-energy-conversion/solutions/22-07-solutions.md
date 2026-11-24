# Solutions 22-07 · Converter Dynamics and Control

Problems: [22-07 problem set](../problems/22-07-problems.md) · Chapter: [22-07](../chapters/22-07-converter-dynamics-and-control.md). Every number below is recomputed by [verify_22_07.py](../verify/verify_22_07.py).

---

## Solutions

### Solution 22-07.1

(a) $f_0 = 1/(2\pi\sqrt{10\ \mu\text{H} \times 100\ \mu\text{F}})$ = **5.03** kHz; (b) $Q = 1.2\sqrt{100/10}$ = **3.79**; (c) $20\log_{10}48$ = **33.6** dB.

### Solution 22-07.2

At $s = j\omega_0$, $s^2LC = -1$, so the denominator $1 + j\omega_0L/R - 1 = j\omega_0L/R$, and $Z_{out} = j\omega_0L/(j\omega_0L/R) = R$: the inductor and capacitor cancel and only the load is left. For Problem 22-07.1, **1.2** Ω. With $Q$ = 3.8, that is the peak: the output impedance at resonance is 1.2 Ω, far above its value at other frequencies, which is why the loop must have gain there.

### Solution 22-07.3

$D$ = 0.75, $D'$ = 0.25, $f_{RHP} = D'^2R/(2\pi L)$.

(a) $R$ = 48 Ω: **21.7** kHz; (b) $R$ = 9.6 Ω: **4.34** kHz; (c) **868** Hz. A 4:1 boost at full load can barely cross over at 1 kHz: high-ratio boosts are slow, which is one reason isolated or two-stage designs are preferred for large ratios.

### Solution 22-07.4

(a) $B = 45° - 90° + 170°$ = **125**°; (b) $k = \tan((62.5° + 90°)/2)$ = **4.09**.

### Solution 22-07.5

(a) $1/(2\pi RC) = 1/(2\pi \times 0.12 \times 62.5\ \mu\text{F})$ = **21.2** kHz.

(b) $-\arctan(60/21.22)$ = **−70.5**°.

(c) PM $= 180° + (-90° + B) + \varphi_p$, so $B = 60° - 90° + 70.5°$ = **40.5**°.

(d) A type II with its zero at $f_c/k$ and pole at $kf_c$ gives $B = \arctan k - \arctan(1/k) = 2\arctan k - 90°$, so $\arctan k = 65.26°$ and $k$ = **2.17**.

(e) $60/2.17$ = **27.6** kHz; (f) $60 \times 2.17$ = **130** kHz. A single zero–pole pair suffices because current mode removed the LC resonance from the outer loop.

### Solution 22-07.6

(a) $12/22\ \mu\text{H}$ = **0.545** A/µs; (b) $36/22\ \mu\text{H}$ = **1.64** A/µs; (c) $-m_2/m_1$ = **−3.00**; (d) $(m_2 - m_1)/2$ = **0.545** A/µs; (e) $-(1.636 - 0.818)/(0.545 + 0.818)$ = **−0.60**.

### Solution 22-07.7

$C = \Delta I/(2\pi f_c\Delta V) = 100/(2\pi \times 200\ \text{kHz} \times 30\ \text{mV})$ = **2.65** mF.

### Solution 22-07.8

(a) $f_c = 30°/(360° \times 1\ \mu\text{s})$ = **83.3** kHz; (b) the delay costs $360 \times 0.1$ = 36°, leaving **24**°.

### Solution 22-07.9

Feedback divides the open-loop line-to-output gain by $1 + T$. Well below $f_0$, $G_{vg} \approx D$ = 0.25, so (a) $0.25/301$ = **8.3** × 10⁻⁴, (b) **−61.6** dB.

### Solution 22-07.10

(a) Perturb with $v_g$ fixed: $sL\hat\imath = V_g\hat d - V\hat d + D'\hat v$ and $sC\hat v = -D'\hat\imath + I\hat d - \hat v/R$, where $V < 0$ and the inductor's DC current is $I = -V/(D'R) > 0$. With $V = -V_gD/D'$, the first equation gives $\hat\imath = ((V_g - V)\hat d + D'\hat v)/(sL)$ and $V_g - V = V_g/D'$. Substituting,

$$
\hat v\left(sC + \frac{D'^2}{sL} + \frac{1}{R}\right) = \hat d\left(I - \frac{D'V_g}{D'sL}\right).
$$

Multiplying by $sL/D'^2$ and using $I = V_gD/(D'^2R)$:

$$
G_{vd}(s) = -\frac{V_g}{D'^2}\cdot\frac{1 - s\dfrac{DL}{D'^2R}}{1 + s\dfrac{L}{D'^2R} + s^2\dfrac{LC}{D'^2}},
$$

with an RHP zero at $\omega_z = D'^2R/(DL)$. The overall minus sign is the inversion (more duty makes the output more negative).

(b) $D = D'$ = 0.5: $f_z = 0.25 \times 6/(2\pi \times 0.5 \times 10\ \mu\text{H})$ = **47.7** kHz; (c) $12/0.25$ = **48** V per unit duty.

### Solution 22-07.11

(a) $1/(\omega_IR_1) = 1/(5000 \times 20\ \text{k}\Omega)$ = **10.0** nF; (b) $C_1 = 10(1 - 1/16)$ = **9.375** nF; (c) $C_2 = 10/16$ = **0.625** nF; (d) $R_2 = 1/(2\pi \times 12.5\ \text{kHz} \times 9.375\ \text{nF})$ = **1358** Ω; (e) $R_3 = 20\ \text{k}\Omega/15$ = **1333** Ω; (f) $C_3 = 1/(2\pi \times 200\ \text{kHz} \times 1333\ \Omega)$ = **0.597** nF.

### Solution 22-07.12

(a) At 20 kHz, $|Z_{out}|$ = **0.0847** Ω; (b) $|1 + T| = |1 - j| = \sqrt2$, so **0.0599** Ω; (c) $1/(2\pi \times 20\ \text{kHz} \times 100\ \mu\text{F})$ = **0.0796** Ω.

(d) A numerical sweep finds the closed-loop peak at **0.295** Ω, (e) at **5.12** kHz, close to $f_0$, where the open-loop impedance is $R$ = 1.2 Ω and the loop gain is only about 4.

The estimate $\Delta V \approx \Delta I/(2\pi f_cC)$ assumes the loop has suppressed the LC resonance, which a well-designed type-III loop does by having its gain rise steeply below crossover. A plain integrator crossing at only four times $f_0$ leaves a resonant peak nearly four times larger than the estimate, and a load step would ring at about 5 kHz. Always check the closed-loop impedance over frequency, not just at $f_c$.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 22-07.1a | resonant frequency | 5.03 | kHz |
| 22-07.1b | quality factor | 3.79 | |
| 22-07.1c | low-frequency gain | 33.6 | dB |
| 22-07.2 | output impedance at resonance | 1.2 | Ω |
| 22-07.3a | RHP zero at 1 A | 21.7 | kHz |
| 22-07.3b | RHP zero at 5 A | 4.34 | kHz |
| 22-07.3c | crossover limit at 5 A | 868 | Hz |
| 22-07.4a | phase boost | 125 | ° |
| 22-07.4b | k | 4.09 | |
| 22-07.5a | plant pole | 21.2 | kHz |
| 22-07.5b | plant phase at 60 kHz | −70.5 | ° |
| 22-07.5c | phase boost | 40.5 | ° |
| 22-07.5d | k | 2.17 | |
| 22-07.5e | zero frequency | 27.6 | kHz |
| 22-07.5f | pole frequency | 130 | kHz |
| 22-07.6a | up-slope | 0.545 | A/µs |
| 22-07.6b | down-slope | 1.64 | A/µs |
| 22-07.6c | ratio without compensation | −3.00 | |
| 22-07.6d | minimum compensation slope | 0.545 | A/µs |
| 22-07.6e | ratio with m_a = m2/2 | −0.60 | |
| 22-07.7 | output capacitance | 2.65 | mF |
| 22-07.8a | crossover for 30° of delay | 83.3 | kHz |
| 22-07.8b | remaining phase margin | 24 | ° |
| 22-07.9a | closed-loop line gain | 8.3e-4 | |
| 22-07.9b | closed-loop line gain | −61.6 | dB |
| 22-07.10b | buck-boost RHP zero | 47.7 | kHz |
| 22-07.10c | low-frequency gain magnitude | 48 | V |
| 22-07.11a | C1 + C2 | 10.0 | nF |
| 22-07.11b | C1 | 9.375 | nF |
| 22-07.11c | C2 | 0.625 | nF |
| 22-07.11d | R2 | 1358 | Ω |
| 22-07.11e | R3 | 1333 | Ω |
| 22-07.11f | C3 | 0.597 | nF |
| 22-07.12a | open-loop output impedance at 20 kHz | 0.0847 | Ω |
| 22-07.12b | closed-loop output impedance at 20 kHz | 0.0599 | Ω |
| 22-07.12c | capacitor estimate | 0.0796 | Ω |
| 22-07.12d | closed-loop peak | 0.295 | Ω |
| 22-07.12e | frequency of the peak | 5.12 | kHz |
