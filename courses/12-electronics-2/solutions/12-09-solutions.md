# Solutions 12-09 · Oscillators

Problems: [12-09 problems](../problems/12-09-problems.md) · Chapter: [12-09](../chapters/12-09-oscillators.md). Every number below is recomputed by [verify_12_09.py](../verify/verify_12_09.py), which finds oscillation frequencies and gain conditions from each circuit's characteristic polynomial and computes describing functions by numerical integration.

---

## Solutions

### Solution 12-09.1

$L = 10 \times 0.12$ = **1.2**, so noise grows and the oscillator starts. It settles where the amplifier's effective gain is $1/0.12$ = **8.333**.

### Solution 12-09.2

$f_0 = 1/(2\pi \times 4.7\ \text{k}\Omega \times 22\ \text{nF})$ = **1539** Hz, and $R_2/R_1$ = **2** for a gain of 3.

### Solution 12-09.3

$f = 1/(2 \times 7 \times 15\ \text{ps})$ = **4.762** GHz.

### Solution 12-09.4

With $Z_s = R_1 + 1/(j\omega C_1)$ and $Y_p = 1/R_2 + j\omega C_2$, the feedback fraction is $1/(1 + Z_sY_p)$, and

$$
Z_sY_p = \frac{R_1}{R_2} + \frac{C_2}{C_1} + j\left(\omega R_1C_2 - \frac{1}{\omega R_2C_1}\right) .
$$

The imaginary part vanishes at $\omega_0 = 1/\sqrt{R_1R_2C_1C_2}$, where $\beta = 1/(1 + R_1/R_2 + C_2/C_1)$. Here $f_0$ = **1125** Hz and $\beta = 1/(1 + 1 + 2)$ = **0.25**, so the gain must be **4**.

### Solution 12-09.5

$R = \sqrt6/(2\pi f_0C) = \sqrt6/(2\pi \times 10\ \text{kHz} \times 10\ \text{nF})$ = **3898** Ω, with an inverting gain of at least **29**.

### Solution 12-09.6

$C_1C_2/(C_1 + C_2)$ = **1.6** nF, so $f_0 = 1/(2\pi\sqrt{10\ \mu\text{H} \times 1.6\ \text{nF}})$ = **1.258** MHz. $g_mR \ge C_2/C_1$ = 4, so $g_m \ge$ **2** mA/V.

### Solution 12-09.7

$f_0$ = **5.033** GHz; $R_p = Q\omega_0L$ = **474.3** Ω; $g_m > 2/R_p$ = **4.216** mA/V.

### Solution 12-09.8

$Q = \omega L/R_s = 2\pi \times 5\ \text{GHz} \times 2\ \text{nH}/1\ \Omega$ = **62.83**. Exactly, $R_p = R_s(1 + Q^2)$ = **3949** Ω; the approximation $Q^2R_s$ gives **3948** Ω.

### Solution 12-09.9

$L_m = 1/[(2\pi \times 32\,768)^2 \times 2\ \text{fF}]$ = **1.180 × 10⁴** H (about 11.8 kH: no physical inductor could do this). $Q = 2\pi f_sL_m/R_m$ = **6.071 × 10⁴**.

### Solution 12-09.10

$\Delta f = f_s\left(\sqrt{1 + \frac{C_m}{C_0 + 10\ \text{pF}}} - \sqrt{1 + \frac{C_m}{C_0 + 12\ \text{pF}}}\right)$ = **979.6** Hz, or **97.96** ppm (downward, since more load capacitance lowers the frequency toward $f_s$). The first-order formula $f_s\frac{C_m}{2}\left(\frac{1}{C_0 + 10\ \text{pF}} - \frac{1}{C_0 + 12\ \text{pF}}\right)$ gives **980.4** Hz.

### Solution 12-09.11

Each stage must contribute 36°: $\omega_0 = \tan 36^\circ/\tau$, so $f_0$ = **11.56** GHz, and the gain must be at least $1/\cos 36^\circ$ = **1.236**. Three stages need 2; longer rings need less gain per stage because each contributes less phase.

### Solution 12-09.12

The limiter's output fundamental is $N(a) \cdot a = 4V_s/\pi$ = **1.273** V, independent of $a$; the bridge passes a third of it, so the amplitude at its output is **0.4244** V. (The square wave's harmonics are attenuated by the bridge but not removed, so the waveform at the bridge's output is visibly distorted.)

### Solution 12-09.13

(a) $f_p - f_s = f_s(\sqrt{1 + C_m/C_0} - 1)$, or $\sqrt{1 + 4/1500} - 1$ as a fraction: **1332** ppm (33.3 kHz at 25 MHz).

(b) $C_L = C_1C_2/(C_1 + C_2) + C_{stray}$ = 9 + 3 = **12** pF. The motional branch resonates with $C_0 + C_L$ = 13.5 pF in series, so the circuit oscillates $\sqrt{1 + 4/13\,500} - 1$ = **148.1** ppm above $f_s$: inside the inductive region, near its lower end.

(c) $R_{neg} = -g_m/(\omega^2C_1C_2) = -5\ \text{mA/V}/[(2\pi \times 25\ \text{MHz})^2 \times (18\ \text{pF})^2]$ = **−625.4** Ω (the oscillation frequency is within 0.015% of 25 MHz, which changes nothing at four figures). Against $R_m$ = 30 Ω that is a gain margin of **20.85**: the circuit starts reliably, well above the factor of 5 that vendors' guides ask for in MHz oscillators (12-09 §9). Note how the margin falls as $1/\omega^2$ and as $1/(C_1C_2)$: doubling both capacitors to raise $C_L$ cuts it by four.

### Solution 12-09.14

With $y = sRC$, the input resistance $R$ at node 3 adds a third current there: $(V_2 - V_3)/R = sCV_3 + V_3/R$, so $V_2 = V_3(2 + y)$. Then

$$
V_1 = V_2(2 + y) - V_3 = V_3(3 + 4y + y^2), \qquad V_{in} = V_1(2 + y) - V_2 = V_3(2 + y)(2 + 4y + y^2) = V_3(4 + 10y + 6y^2 + y^3) .
$$

At $y = jx$ the denominator is $(4 - 6x^2) + j(10x - x^3)$. It is real at $x = \sqrt{10}$ = **3.162**, so $\omega_0 = 3.162/(RC)$ (against $\sqrt6$ = 2.449 for the buffered ladder), and there it equals $4 - 60 = -56$: the amplifier must invert with a gain of at least **56** (against 29). Loading the last node steals current from the ladder, so each section must shift its phase at a higher frequency, where the ladder also attenuates more.

### Solution 12-09.15

(a) $T = 2RC\ln[(1 + \beta)/(1 - \beta)] = 2 \times 47\ \mu\text{s} \times \ln 2$ = **65.16** µs, so $f$ = **15.35** kHz.

(b) $f = 1/[(R_A + 2R_B)C\ln2]$ = **14.62** kHz, with duty cycle $(R_A + R_B)/(R_A + 2R_B)$ = **52.38**%. The charging path always includes $R_A$ as well as $R_B$, while the discharge path is $R_B$ alone, so the high time is always longer; $R_A$ cannot be zero, because the discharge transistor would then short the supply. A diode across $R_B$ (so that charging bypasses it) or a different connection is needed for 50%.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 12-09.1a | loop gain | 1.2 | — |
| 12-09.1b | settled amplifier gain | 8.333 | — |
| 12-09.2a | frequency | 1539 | Hz |
| 12-09.2b | R_2/R_1 | 2 | — |
| 12-09.3a | frequency | 4.762 | GHz |
| 12-09.4a | frequency | 1125 | Hz |
| 12-09.4b | feedback fraction | 0.25 | — |
| 12-09.4c | required gain | 4 | — |
| 12-09.5a | R | 3898 | Ω |
| 12-09.5b | required gain | 29 | — |
| 12-09.6a | series capacitance | 1.6 | nF |
| 12-09.6b | frequency | 1.258 | MHz |
| 12-09.6c | minimum g_m | 2 | mA/V |
| 12-09.7a | frequency | 5.033 | GHz |
| 12-09.7b | parallel loss resistance | 474.3 | Ω |
| 12-09.7c | minimum g_m | 4.216 | mA/V |
| 12-09.8a | Q | 62.83 | — |
| 12-09.8b | exact R_p | 3949 | Ω |
| 12-09.8c | approximate R_p | 3948 | Ω |
| 12-09.9a | motional inductance | 1.180 × 10⁴ | H |
| 12-09.9b | Q | 6.071 × 10⁴ | — |
| 12-09.10a | frequency change | 979.6 | Hz |
| 12-09.10b | frequency change | 97.96 | ppm |
| 12-09.10c | first-order frequency change | 980.4 | Hz |
| 12-09.11a | five-stage frequency | 11.56 | GHz |
| 12-09.11b | minimum stage gain | 1.236 | — |
| 12-09.12a | output fundamental | 1.273 | V |
| 12-09.12b | amplitude at the bridge output | 0.4244 | V |
| 12-09.13a | f_p − f_s | 1332 | ppm |
| 12-09.13b | load capacitance | 12 | pF |
| 12-09.13c | pulled offset | 148.1 | ppm |
| 12-09.13d | negative resistance | −625.4 | Ω |
| 12-09.13e | gain margin | 20.85 | — |
| 12-09.14a | normalized frequency ωRC | 3.162 | — |
| 12-09.14b | inverting gain needed | 56 | — |
| 12-09.15a | astable period | 65.16 | µs |
| 12-09.15b | astable frequency | 15.35 | kHz |
| 12-09.15c | 555 frequency | 14.62 | kHz |
| 12-09.15d | 555 duty cycle | 52.38 | % |
