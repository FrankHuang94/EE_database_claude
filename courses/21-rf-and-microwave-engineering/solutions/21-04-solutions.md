# Solutions 21-04 · Low-Noise Amplifiers

Problems: [21-04 problem set](../problems/21-04-problems.md) · Chapter: [21-04](../chapters/21-04-low-noise-amplifiers.md). Every number below is recomputed by [verify_21_04.py](../verify/verify_21_04.py).

---

## Solutions

### Solution 21-04.1

The source and termination divide the signal by two and present 25 Ω to the amplifier. Referred to the source, the termination doubles the noise ($F$ = 2), and the amplifier's excess noise, $F_A - 1$ relative to the divided source's noise, counts four times because the signal power at its input is a quarter of the source's available EMF power: $F = 2 + 4(1.5 - 1)$ = 4, or **6.02** dB.

### Solution 21-04.2

- $\omega_T = 2\pi \times 40$ GHz, so $C_{gs} = g_m/\omega_T$ = **119.4** fF and $L_s = R_s/\omega_T$ = **0.199** nH.
- $L_g = 1/(\omega_0^2C_{gs}) - L_s$ = **6.816** nH.
- $Q_{in} = 1/(2\omega_0R_sC_{gs})$ = **2.42**; $G_m = \omega_T/(2\omega_0R_s)$ = **72.7** mS.
- $F = 1 + 0.03 \times 50 \times (5.5/40)^2$ = 1.0284: NF = **0.121** dB.

### Solution 21-04.3

Let the channel current, flowing from drain to source into the source node $x$, be $-g_mv_x + i_n$ (gate at AC ground). KCL at $x$: $(v_s - v_x)/R_s - g_mv_x + i_n = 0$, so $v_x = (v_s/R_s + i_n)/(1/R_s + g_m)$. The drain current equals the channel current:

$$
i_d = -g_mv_x + i_n = \frac{-g_mv_s/R_s + i_n/R_s}{1/R_s + g_m} = \frac{-g_mv_s + i_n}{1 + g_mR_s} .
$$

The signal term is $g_mv_s/(1 + g_mR_s)$ and the noise term $i_n/(1 + g_mR_s)$. With $\overline{v_s^2} = 4kT_0R_s$ and $\overline{i_n^2} = 4kT_0xg_m$, the ratio of output noise to the source's share is

$$
F = 1 + \frac{xg_m}{g_m^2R_s} = 1 + \frac{x}{g_mR_s} .
$$

For $g_m$ = 30 mS and $x$ = 2/3: $F = 1 + 0.667/1.5$ = 1.444, NF = **1.60** dB. The input impedance is $1/g_m$ = **33.3** Ω, so $\Gamma = (33.3 - 50)/(33.3 + 50)$ = **−0.200** and the return loss is **13.98** dB.

The extra transconductance buys 0.62 dB of noise figure (against 2.22 dB at the match) and costs 50% more current and a deliberate mismatch, still better than the usual 10 dB return-loss requirement.

### Solution 21-04.4

At resonance the input loop's impedance is $2R_s$, so $i_{in} = v_s/2R_s$ and $v_{gs} = i_{in}/(j\omega_0C_{gs})$, whose magnitude is $v_s/(2\omega_0R_sC_{gs})$. Then $G_m = g_m\lvert v_{gs}/v_s\rvert = g_m/(2\omega_0R_sC_{gs}) = \omega_T/(2\omega_0R_s)$, because $g_m/C_{gs} = \omega_T$. Width scales $g_m$ and $C_{gs}$ together and cancels. At 2.4 GHz: **50** mS for $f_T$ = 12 GHz and **100** mS for 24 GHz.

### Solution 21-04.5

The noise figure as a function of $Q_L$ (re-matched, §3.5) is solved for 0.8 dB by bisection: $Q_L$ = **22.2**. Only a good off-chip part, or an unusually good on-chip spiral, meets it.

### Solution 21-04.6

Re-match with $\omega_TL_s = R_s - r_g$, so the loop resistance at resonance is still $R_s + r_g + \omega_TL_s = 2R_s$ and $G_m = \omega_T/(2\omega_0R_s)$ is unchanged. The drain noise drives a loop current $i = -j\omega_0L_si_{nd}/(2R_s)$, so the fed-back current is $g_mv_{gs} = -(\omega_TL_s/2R_s)i_{nd} = -[(R_s - r_g)/2R_s]\,i_{nd}$ and the output carries $i_{nd}(R_s + r_g)/(2R_s)$. The gate loss contributes like the source, $G_m^2 \cdot 4kT_0r_g$. Dividing by the source's share $G_m^2 \cdot 4kT_0R_s$:

$$
F = 1 + \frac{r_g}{R_s} + \frac{xg_m}{G_m^2R_s}\left(\frac{R_s + r_g}{2R_s}\right)^2 = 1 + \frac{r_g}{R_s} + xg_m\frac{(R_s + r_g)^2}{R_s}\left(\frac{\omega_0}{\omega_T}\right)^2 .
$$

For $r_g$ = 5 Ω: $F = 1 + 0.1 + 0.04 \times 55^2/50 \times 0.04$ = 1.197, NF = **0.780** dB. The shortcut $1 + r_g/R_s + xg_mR_s(\omega_0/\omega_T)^2$ = 1.18 gives **0.719** dB: **0.06** dB optimistic, because less of the drain noise is cancelled when part of the real input impedance comes from a resistor.

### Solution 21-04.7

The source EMF reaches the intercept at $0.25/2$ = 0.125 V, an available power of $0.125^2/(8 \times 50)$ W = **−14.08** dBm. For −10 dBm the EMF must be $\sqrt{8 \times 50 \times 10^{-4}}$ = 0.2 V, so $Q_{in} \le 0.25/0.2$ = **1.25**.

### Solution 21-04.8

$F_1 = 10^{0.15}$ = 1.413 and $F_2 = 10^{1.2}$ = 15.85: $G_1 = 14.85/[1.413(10^{0.02} - 1)]$ = 223, or **23.5** dB. With 25 dB: $F = 1.413 + 14.85/316.2$ = 1.460, NF = **1.64** dB.

### Solution 21-04.9

Solve $1 + 1/(50g_{m2}) + 1/(300g_{m2}) + 1/(g_{m2}^2 \times 300 \times 50) = 10^{0.1}$ for $g_{m2}$: **92.9** mS, which at 10 S/A takes **9.29** mA.

### Solution 21-04.10

From §3.8, M1's noise reaches the output with coefficient $(g_{m2}R_2R_s - R_1)/2$ and the signal with gain $A = (R_1/R_s + g_{m2}R_2)/2$. Adding M2's noise ($R_2^2 \cdot 4kT_0xg_{m2}$) and the load resistors' ($4kT_0R_1$, $4kT_0R_2$):

$$
F = 1 + \frac{xg_{m1}\left[(g_{m2}R_2R_s - R_1)/2\right]^2 + xg_{m2}R_2^2 + R_1 + R_2}{A^2R_s} .
$$

For $R_1$ = 900, 1000 and 1100 Ω: **0.830**, **0.768** and **0.724** dB. Minimizing numerically gives $R_1$ = **1465** Ω and **0.668** dB.

Cancellation is not the noise optimum: raising $R_1$ increases the common-gate path's signal gain linearly while M1's uncancelled noise grows only quadratically from zero, so a small overshoot helps. In a real circuit $R_1$ carries M1's bias current, $g_{m1}/(g_m/I_D)$ = 2 mA at 10 S/A, which drops **2.0** V across 1 kΩ and **2.9** V across 1.46 kΩ; with a low supply there is no room, and the larger $R_1$ also lowers the pole it forms with the drain capacitance. Designs therefore sit near cancellation, where the noise figure is also least sensitive to the two paths' mismatch.

### Solution 21-04.11

At resonance $Z_{in} = R_s$; away from it, $Z_{in} = R_s + jX$ with $X = \omega L_{tot} - 1/(\omega C_{gs})$, so $\lvert\Gamma\rvert = \lvert X\rvert/\sqrt{4R_s^2 + X^2}$. For $\lvert\Gamma\rvert$ = 0.316, $\lvert X\rvert = 2R_s \times 0.316/\sqrt{1 - 0.1}$ = **33.3** Ω. Solving $\omega L_{tot} - 1/(\omega C_{gs}) = \pm 33.3$ Ω gives **2.101** and **2.741** GHz: a 10 dB band of **26.7**%, set by the input loop's Q.

### Solution 21-04.12

- Lossless: $Q_{in}$ = 2.07 and NF = **0.20** dB.
- On-chip, $Q$ = 12: re-matching gives $r_g$ = **16.70** Ω and NF = **1.51** dB, just failing the 1.5 dB target.
- Off-chip, $Q$ = 40: $r_g$ = **4.95** Ω and NF = **0.63** dB, comfortably inside it.

The gate inductor sets the answer. The choice is between an external part (cost, board area, a pin's parasitics), a better on-chip inductor (thick metal, a shield, 21-02 §9) or a topology with a smaller $L_g$.

### Solution 21-04.13

Noise figure: $F = 1.262 + (10 - 1)/100$ = 1.352, **1.31** dB. IIP3 (mW): $1/\text{IIP3} = 1/0.144 + 100/3.162$ = 6.95 + 31.6, so IIP3 = **−15.86** dBm. The mixer sets the intercept: 20 dB of LNA gain multiplies its nonlinearity a hundredfold.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 21-04.1a | noise figure | 6.02 | dB |
| 21-04.2a | Cgs | 119.4 | fF |
| 21-04.2b | Ls | 0.199 | nH |
| 21-04.2c | Lg | 6.816 | nH |
| 21-04.2d | Qin | 2.42 | — |
| 21-04.2e | Gm | 72.7 | mS |
| 21-04.2f | noise figure | 0.121 | dB |
| 21-04.3a | noise figure | 1.60 | dB |
| 21-04.3b | input impedance | 33.3 | Ω |
| 21-04.3c | reflection coefficient | −0.200 | — |
| 21-04.3d | return loss | 13.98 | dB |
| 21-04.3e | NF improvement over the match | 0.62 | dB |
| 21-04.4a | Gm at 12 GHz | 50 | mS |
| 21-04.4b | Gm at 24 GHz | 100 | mS |
| 21-04.5a | gate-inductor Q for 0.8 dB | 22.2 | — |
| 21-04.6a | NF with rg 5 ohm | 0.780 | dB |
| 21-04.6b | shortcut NF | 0.719 | dB |
| 21-04.6c | shortcut error | 0.06 | dB |
| 21-04.7a | IIP3 at Qin 2 | −14.08 | dBm |
| 21-04.7b | largest Qin for −10 dBm | 1.25 | — |
| 21-04.8a | LNA gain | 23.5 | dB |
| 21-04.8b | cascade NF at 25 dB | 1.64 | dB |
| 21-04.9a | gm2 | 92.9 | mS |
| 21-04.9b | M2 current | 9.29 | mA |
| 21-04.10a | NF at R1 900 | 0.830 | dB |
| 21-04.10b | NF at R1 1000 | 0.768 | dB |
| 21-04.10c | NF at R1 1100 | 0.724 | dB |
| 21-04.10d | optimum R1 | 1465 | Ω |
| 21-04.10e | optimum NF | 0.668 | dB |
| 21-04.10f | drop across 1 kohm | 2.0 | V |
| 21-04.10g | drop across 1.46 kohm | 2.9 | V |
| 21-04.11a | reactance at 10 dB return loss | 33.3 | Ω |
| 21-04.11b | lower edge | 2.101 | GHz |
| 21-04.11c | upper edge | 2.741 | GHz |
| 21-04.11d | fractional bandwidth | 26.7 | % |
| 21-04.12a | lossless NF | 0.20 | dB |
| 21-04.12b | rg at Q 12 | 16.70 | Ω |
| 21-04.12c | NF at Q 12 | 1.51 | dB |
| 21-04.12d | rg at Q 40 | 4.95 | Ω |
| 21-04.12e | NF at Q 40 | 0.63 | dB |
| 21-04.13a | cascade NF | 1.31 | dB |
| 21-04.13b | cascade IIP3 | −15.86 | dBm |
