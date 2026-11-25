# Solutions 24-01 · Signal Integrity Fundamentals

Problems: [24-01 problems](../problems/24-01-problems.md) · Chapter: [24-01](../chapters/24-01-signal-integrity-fundamentals.md)

Every number is recomputed by [verify_24_01.py](../verify/verify_24_01.py).

---

## Solutions

### Solution 24-01.1

(a) PAM4 carries 2 bits per symbol: $106.25/2$ = **53.125** GBd, $f_N$ = **26.5625** GHz and UI = **18.82** ps.

(b) NRZ: 25.78125 GBd, $f_N$ = **12.89** GHz and UI = **38.79** ps.

### Solution 24-01.2

$\delta = 1/\sqrt{\pi f\mu_0\sigma}$ and $R_s = 1/(\sigma\delta)$.

(a) At 4 GHz: δ = **1.045** µm and $R_s$ = **16.5** mΩ.

(b) At 28 GHz: δ = **0.395** µm and $R_s$ = **43.7** mΩ.

Seven times the frequency shrinks the skin depth by $\sqrt7$ and raises the surface resistance by the same factor.

### Solution 24-01.3

(a) $R' = R_s/w = 43.66\ \text{m}\Omega/(4 \times 25.4\ \mu\text{m})$ = **430** Ω/m.

(b) $\alpha_c = R'/(2Z_0) = 429.7/85$ = 5.055 Np/m; × 8.686 × 0.0254 = **1.115** dB/in.

(c) $36\sqrt{28}/(4 \times 42.5)$ = **1.121** dB/in.

(d) $10 \times 1.115$ = **11.15** dB.

A narrow, low-impedance trace is a conductor-loss problem: PCIe's 85 Ω pairs pay for their lower impedance in copper loss.

### Solution 24-01.4

(a) $\alpha_d = \pi \times 53.125 \times 10^9 \times \sqrt{3.3} \times 0.0015/(2.998 \times 10^8)$, × 8.686 × 0.0254 = **0.335** dB/in.

(b) $R_s$ at 53.125 GHz over a 4-mil width, divided by $2 \times 50$ Ω: **1.306** dB/in.

(c) **1.64** dB/in.

(d) It lies inside the 1.27–1.8 dB/in range. At 53 GHz even the best laminates are conductor-dominated, so smoother copper and wider traces matter as much as the resin.

### Solution 24-01.5

(a) $K_r = 1.5$ needs $\arctan[1.4(\Delta/\delta)^2] = \pi/4$, so $1.4(\Delta/\delta)^2 = 1$ and $\Delta = \delta/\sqrt{1.4}$. With δ = 0.3949 µm at 28 GHz, $\Delta_{rms}$ = **0.334** µm.

(b) At 4 GHz, δ = 1.045 µm, so $1.4(\Delta/\delta)^2 = (\delta_{28}/\delta_4)^2 = 4/28$ = 0.1429 and $K_r$ = **1.09**.

Roughness that costs 50% extra loss at 28 GHz costs only 9% at 4 GHz, which is why older links could ignore it.

### Solution 24-01.6

(a) At 1 GHz, conductor loss is $36\sqrt1/(5 \times 50)$ by the rule, or exactly **0.1433** dB/in from the model; dielectric loss is $2.3 \times 1 \times 0.014 \times 2.098$, exactly **0.0679** dB/in.

(b) Conductor loss scales as $\sqrt f$ and dielectric loss as $f$, so they are equal where $\sqrt{f/1\ \text{GHz}} = 0.1433/0.06789$, that is $f$ = **4.46** GHz.

(c) Each is then 0.3025 dB/in, a total of **0.605** dB/in.

Above about 4.5 GHz this laminate is dielectric-limited, which is why moving from FR-4 to a low-loss laminate is the first step for any multi-gigabit board.

### Solution 24-01.7

(a) $8.0 + 8.5 + 15.5$ = **32** dB.

The trace gets $15.5 - 1.5 - 2 \times 0.6$ = **12.8** dB.

(b) $12.8/0.7097$ = **18.0** in. (c) $12.8/1.0$ = **12.8** in.

PCIe 6.0 kept PCIe 5.0's Nyquist frequency but cut 4 dB from the budget to pay for PAM4's smaller eye, so the same board reaches less far.

### Solution 24-01.8

(a) $\Gamma = (60 - 50)/(60 + 50)$ = **0.0909**.

(b) $-20\log_{10}0.0909$ = **20.8** dB. (c) $-10\log_{10}(1 - 0.0909^2)$ = **0.0360** dB.

(d) 15 dB means $\lvert\Gamma\rvert \le 10^{-15/20}$ = **0.178**. Then $Z = 50(1 + \Gamma)/(1 - \Gamma)$ ranges from **34.9** to **71.6** Ω.

### Solution 24-01.9

(a) $T_d = 3 \times 25.4\ \text{mm} \times \sqrt{3.6}/c$ = **482** ps.

(b) The round trip is $2T_d$, so the ripple repeats every $1/(2T_d)$ = **1.037** GHz.

(c) $20\log_{10}[(1 + 0.0225)/(1 - 0.0225)]$ = **0.391** dB.

A 1 GHz ripple period means the echo arrives about 1 ns late, tens of UIs at PCIe rates: a reflection that the receiver's equalizer cannot reach.

### Solution 24-01.10

(a) $c/(4 \times 2.4\ \text{mm} \times \sqrt{3.7})$ = **16.24** GHz.

(b) $c/(4 \times 0.25\ \text{mm} \times \sqrt{3.7})$ = **155.9** GHz.

(c) $\ell = c/(4 \times 1.5 \times 32\ \text{GHz} \times \sqrt{3.7})$ = **0.812** mm (**32.0** mil).

The un-drilled stub would notch right at PCIe 5.0's 16 GHz Nyquist frequency; back-drilling moves it far out of band.

### Solution 24-01.11

(a) $v = c/\sqrt{3.6}$ = **1.580** × 10⁸ m/s, so $T_D = 0.1/v$ = **632.9** ps. $K_b = \tfrac14(0.03 + 0.03)$ = 0.015, so NEXT = $0.015 \times 0.5$ = **7.5** mV, lasting $2T_D$ = **1266** ps. In stripline $C_m/C = L_m/L$, so FEXT = **0**.

(b) $V_{FEXT} = \tfrac12 \times 632.9\ \text{ps} \times (0.03 - 0.05) \times 0.5\ \text{V}/20\ \text{ps}$ = **−158** mV, almost a third of the aggressor.

(c) $\lvert V_{FEXT}/V_a\rvert = (\ell/2v)(0.02)/t_r \le 0.02$ gives $\ell \le 2vt_r$ = **6.32** mm.

Long, fast microstrip buses are a FEXT disaster; stripline, or wide spacing over short runs, is the cure.

### Solution 24-01.12

(a) Let $V_a(t)$ ramp from 0 at $t = 0$ to $V_a$ at $t_r$. For $2T_D < t_r$, $V_a(t) - V_a(t - 2T_D)$ grows until $t = 2T_D$, then equals the ramp's rise over a window of $2T_D$, $V_a(2T_D/t_r)$, until the first term stops rising at $t = t_r$; after that it falls. So the peak is $K_bV_a(2T_D/t_r)$, held from $2T_D$ to $t_r$.

(b) $T_D = 1\ \text{mm}/(1.5 \times 10^8)$ = **6.67** ps, so $2T_D/t_r$ = **0.444** and the peak is $0.03 \times 1 \times 0.444$ = **13.3** mV, not the saturated 30 mV.

(c) $\ell_{sat} = vt_r/2$ = **2.25** mm.

Below the saturation length, NEXT grows in proportion to coupled length, as FEXT always does.

### Solution 24-01.13

$N \le 100\ \text{mV} \times 80\ \text{ps}/(0.15\ \text{nH} \times 12\ \text{mA})$ = 4.44, so **4** drivers.

### Solution 24-01.14

(a) $Z_{target} = 0.75 \times 0.025/40$ = **0.469** mΩ.

(b) $2\pi \times 100\ \text{MHz} \times 15\ \text{pH}$ = **9.42** mΩ, twenty times the target.

(c) $f = Z_{target}/(2\pi L)$ = **4.97** MHz.

Even 15 pH, a very low package inductance, exceeds a high-current core's target above a few megahertz. On-die capacitance, and the die's own resistance, must carry everything faster.

### Solution 24-01.15

(a) $-20\log_{10}0.5$ = **6.02** dB. (b) $-20\log_{10}0.2$ = **13.98** dB.

(c) $1 - 0.5^2 - 0.2^2$ = **0.71**, or 71%. A passive channel cannot create power, so the rest was dissipated in its conductors and dielectric (or radiated): that is the insertion loss beyond mismatch.

### Solution 24-01.16

A backward wave born at position $z$ when the aggressor's edge passes ($t = z/v$) reaches the near end after another $z/v$. Summing the contributions,

$$
V_{NEXT}(t) = \frac{1}{2v}\left(\frac{C_m}{C} + \frac{L_m}{L}\right)\int_0^{\ell}V_a'\!\left(t - \frac{2z}{v}\right)dz .
$$

Substitute $u = t - 2z/v$, $dz = -(v/2)\,du$: the integral becomes $[V_a(t) - V_a(t - 2T_D)]\,v/2$ with $T_D = \ell/v$, so $V_{NEXT} = K_b[V_a(t) - V_a(t - 2T_D)]$ with $K_b = \tfrac14(C_m/C + L_m/L)$. For a ramp, $V_a(t) - V_a(t - 2T_D)$ is the rise over a window $2T_D$ long: it reaches the full $V_a$ if the window spans the whole edge ($2T_D \ge t_r$), and otherwise at most the slope times the window, $V_a(2T_D/t_r)$.

Here $K_b = \tfrac14(0.04 + 0.06)$ = **0.025**.

(a) $2T_D = 2 \times 1\ \text{mm}/(1.5 \times 10^8)$ = **13.3** ps < 30 ps: peak $25 \times 13.3/30$ = **11.1** mV.

(b) $2T_D$ = **66.7** ps ≥ 30 ps: the full **25.0** mV.

### Solution 24-01.17

(a) $\Delta t = \ell\sqrt{\varepsilon_r}/c = 3 \times 25.4\ \mu\text{m} \times \sqrt{3.4}/c$ = **0.469** ps.

(b) $\lvert S_{CD21}\rvert = \lvert\sin(\pi f\Delta t)\rvert$: **−28.2** dB at 26.5625 GHz.

(c) **−22.1** dB at 53.125 GHz: doubling the rate raises the conversion by 6 dB.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 24-01.1a | PAM4 symbol rate | 53.125 | GBd |
| 24-01.1a1 | PAM4 Nyquist frequency | 26.5625 | GHz |
| 24-01.1a2 | PAM4 UI | 18.82 | ps |
| 24-01.1b | NRZ Nyquist frequency | 12.89 | GHz |
| 24-01.1b1 | NRZ UI | 38.79 | ps |
| 24-01.2a | skin depth at 4 GHz | 1.045 | µm |
| 24-01.2a1 | surface resistance at 4 GHz | 16.5 | mΩ |
| 24-01.2b | skin depth at 28 GHz | 0.395 | µm |
| 24-01.2b1 | surface resistance at 28 GHz | 43.7 | mΩ |
| 24-01.2b2 | surface resistance at 28 GHz, 4 s.f. | 43.66 | mΩ |
| 24-01.2b3 | skin depth at 28 GHz, 4 s.f. | 0.3949 | µm |
| 24-01.3a | resistance per metre | 430 | Ω/m |
| 24-01.3a1 | resistance per metre, 4 s.f. | 429.7 | Ω/m |
| 24-01.3b0 | conductor attenuation | 5.055 | Np/m |
| 24-01.3b | conductor loss | 1.115 | dB/in |
| 24-01.3c | rule-of-thumb loss | 1.121 | dB/in |
| 24-01.3d | loss of 10 inches | 11.15 | dB |
| 24-01.4a | dielectric loss at 53.125 GHz | 0.335 | dB/in |
| 24-01.4b | conductor loss at 53.125 GHz | 1.306 | dB/in |
| 24-01.4c | total loss | 1.64 | dB/in |
| 24-01.5a | roughness for factor 1.5 | 0.334 | µm |
| 24-01.5a1 | roughness for factor 1.5, 4 s.f. | 0.3338 | µm |
| 24-01.5b0 | roughness argument at 4 GHz | 0.1429 | |
| 24-01.5b | factor at 4 GHz | 1.09 | |
| 24-01.6a | conductor loss at 1 GHz | 0.1433 | dB/in |
| 24-01.6a1 | dielectric loss at 1 GHz | 0.0679 | dB/in |
| 24-01.6a2 | dielectric loss at 1 GHz, 4 s.f. | 0.06789 | dB/in |
| 24-01.6b | crossover frequency | 4.46 | GHz |
| 24-01.6c0 | each loss at the crossover | 0.3025 | dB/in |
| 24-01.6c | total at the crossover | 0.605 | dB/in |
| 24-01.7a | PCIe 6.0 budget total | 32 | dB |
| 24-01.7a1 | trace allocation | 12.8 | dB |
| 24-01.7b | reach on Megtron 6 | 18.0 | in |
| 24-01.7c | reach at 1.0 dB/in | 12.8 | in |
| 24-01.8a | connector reflection coefficient | 0.0909 | |
| 24-01.8b | connector return loss | 20.8 | dB |
| 24-01.8c | connector mismatch loss | 0.0360 | dB |
| 24-01.8d0 | reflection coefficient for 15 dB | 0.178 | |
| 24-01.8d | lowest impedance for 15 dB | 34.9 | Ω |
| 24-01.8d1 | highest impedance for 15 dB | 71.6 | Ω |
| 24-01.9a | one-way delay | 482 | ps |
| 24-01.9b | ripple period | 1.037 | GHz |
| 24-01.9c | ripple peak to peak | 0.391 | dB |
| 24-01.9c1 | squared reflection coefficient | 0.0225 | |
| 24-01.10a | notch of a 2.4 mm stub | 16.24 | GHz |
| 24-01.10b | notch after back-drilling | 155.9 | GHz |
| 24-01.10c | stub limit for PCIe 7.0 | 0.812 | mm |
| 24-01.10c1 | stub limit for PCIe 7.0, mils | 32.0 | mil |
| 24-01.11a | stripline velocity | 1.580e8 | m/s |
| 24-01.11a1 | coupled delay | 632.9 | ps |
| 24-01.11a2 | backward coefficient | 0.015 | |
| 24-01.11a3 | NEXT amplitude | 7.5 | mV |
| 24-01.11a4 | NEXT duration | 1266 | ps |
| 24-01.11a5 | stripline FEXT | 0 | mV |
| 24-01.11b | microstrip FEXT | -158 | mV |
| 24-01.11c | coupled length for 2% FEXT | 6.32 | mm |
| 24-01.12b0 | coupled delay, 1 mm | 6.67 | ps |
| 24-01.12b1 | ratio of round trip to rise time | 0.444 | |
| 24-01.12b | NEXT peak, 1 mm | 13.3 | mV |
| 24-01.12b2 | saturated NEXT | 30 | mV |
| 24-01.12c | saturation length | 2.25 | mm |
| 24-01.13a | drivers allowed, unrounded | 4.44 | |
| 24-01.13 | drivers allowed | 4 | |
| 24-01.14a | core target impedance | 0.469 | mΩ |
| 24-01.14b | package path impedance at 100 MHz | 9.42 | mΩ |
| 24-01.14b1 | ratio to target | 20 | |
| 24-01.14c | frequency above which the target is exceeded | 4.97 | MHz |
| 24-01.15a | insertion loss | 6.02 | dB |
| 24-01.15b | return loss | 13.98 | dB |
| 24-01.15c | power neither reflected nor transmitted | 0.71 | |
| 24-01.16a0 | backward coefficient | 0.025 | |
| 24-01.16a1 | 2T_D at 1 mm | 13.3 | ps |
| 24-01.16a | NEXT peak at 1 mm | 11.1 | mV |
| 24-01.16b0 | 2T_D at 5 mm | 66.7 | ps |
| 24-01.16b | NEXT peak at 5 mm | 25.0 | mV |
| 24-01.17a | skew | 0.469 | ps |
| 24-01.17b | mode conversion at 26.6 GHz | -28.2 | dB |
| 24-01.17c | mode conversion at 53.1 GHz | -22.1 | dB |
