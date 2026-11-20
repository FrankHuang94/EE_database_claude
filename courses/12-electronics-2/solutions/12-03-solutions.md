# Solutions 12-03 · Frequency Response: Device Capacitances, Miller Effect, Poles and Zeros

Problems: [12-03 problems](../problems/12-03-problems.md) · Chapter: [12-03](../chapters/12-03-frequency-response-miller-poles-zeros.md). Every number below is recomputed by [verify_12_03.py](../verify/verify_12_03.py), which solves each circuit by complex nodal analysis rather than reusing these formulas.

---

## Solutions

### Solution 12-03.1

$f_T = g_m/[2\pi(C_{gs} + C_{gd})] = 2\ \text{mA/V}/(2\pi \times 60\ \text{fF})$ = **5.305** GHz.

### Solution 12-03.2

Input: $C(1 + A_v) = 5 \times 41$ = **205** fF. Output: $C(1 + 1/A_v) = 5 \times 1.025$ = **5.125** fF. The capacitor looks 41 times bigger from the input and about its own size from the output.

### Solution 12-03.3

$g_m = 1\ \text{mA}/25.852\ \text{mV}$ = **38.68** mA/V. $C_\pi + C_\mu = g_m/(2\pi f_T)$ = **12.31** pF, so $C_\pi$ = **11.81** pF. With $C_{je}$ = 2 pF, the diffusion part is 9.81 pF $= \tau_Fg_m$, so $\tau_F$ = **0.2537** ns.

### Solution 12-03.4

$b_1 = 1/\omega_1 + 1/\omega_2$, so $1/(2\pi b_1) = 1/(1/10 + 1/100)$ MHz = **9.091** MHz. Exactly, $\lvert H\rvert^2 = 1/2$ when $(1 + x^2)(1 + x^2/100) = 2$ with $x = f/10\ \text{MHz}$: $x^4/100 + 1.01x^2 - 1 = 0$, so $x^2$ = 0.9806 and $f$ = **9.902** MHz. A decade of separation leaves the estimate 8% low.

### Solution 12-03.5

Gain $g_mR_L$ = **20**. $b_1 = 5\ \text{k}\Omega[50 + 10 \times 21]\ \text{fF} + 10\ \text{k}\Omega \times 60\ \text{fF} = 1.3 + 0.6$ = **1.9** ns, so $1/(2\pi b_1)$ = **83.77** MHz. $b_2 = 5\ \text{k}\Omega \times 10\ \text{k}\Omega \times (500 + 2500 + 500)\ \text{fF}^2$ = **1.75** × 10⁻¹⁹ s². The roots of $1 + b_1s + b_2s^2$ are at **88.28** MHz and **1640** MHz; the right-half-plane zero is at $g_m/(2\pi C_{gd})$ = **31.83** GHz. Solving $\lvert H\rvert = 20/\sqrt2$ gives **88.02** MHz. Here the Miller input term (1.3 ns) dominates and the poles are well separated, so the estimate is within 5%.

### Solution 12-03.6

Input: $R/(1 + A_v) = 1\ \text{M}\Omega/100$ = **10** kΩ. Output: $R/(1 + 1/A_v)$ = **0.99** MΩ. The resistor's current at the input is $(1 + A_v)$ times what its voltage alone would drive, because the output moves opposite to the input; this is shunt feedback (12-05), and it lowers the input resistance by the loop's gain.

### Solution 12-03.7

Gain $g_mR_L/(1 + g_mR_S) = 10/2$ = **5**. Input pole: $(200\ \Omega \parallel 200\ \Omega)$ = 100 Ω with 100 fF, **15.92** GHz. Output pole: $1/(2\pi \times 2\ \text{k}\Omega \times 200\ \text{fF})$ = **397.9** MHz, which sets the bandwidth.

### Solution 12-03.8

$V_o/V_i = (g_m + sC_{gs})/[g_m + s(C_{gs} + C_L)]$. Pole: $1\ \text{mA/V}/[2\pi \times 172.67\ \text{fF}]$ = **921.7** MHz. Zero (left half-plane): $1\ \text{mA/V}/(2\pi \times 72.67\ \text{fF})$ = **2.190** GHz.

### Solution 12-03.9

M1's drain sees about $1/g_{m2}$, so its gain is $-g_{m1}/g_{m2}$ = **−2** and $C_{in} = C_{gs} + C_{gd}(1 + 2) = 50 + 30$ = **80** fF. Without the cascode: $50 + 10 \times 31$ = **360** fF, 4.5 times more.

### Solution 12-03.10

GBW $= g_m/(2\pi C) = 4\ \text{mA/V}/(2\pi \times 1\ \text{pF})$ = **636.6** MHz. For a gain of 10, $R_L = 10/g_m$ = **2.5** kΩ and the bandwidth is $636.6/10$ = **63.66** MHz.

### Solution 12-03.11

The zero is at $1\ \text{mA/V}/(2\pi \times 6\ \text{fF})$ = **26.53** GHz. A right-half-plane zero contributes $-\arctan(f/f_z)$ of phase: at 1 GHz, **2.159**° of lag; at the zero itself, **45**° of lag, with the magnitude up 3 dB. A left-half-plane zero at the same frequency would give the same magnitude but phase *lead*. Lag without attenuation is what makes right-half-plane zeros harmful in feedback loops.

### Solution 12-03.12

The Miller input time constant is $R_S \times 198.67$ fF and the output's is $20\ \text{k}\Omega \times 106\ \text{fF}$ = 2.12 ns, so they are equal at $R_S$ = **10.67** kΩ. Then $b_1$ = **4.24** ns and $1/(2\pi b_1)$ = **37.54** MHz, while the exact −3 dB frequency is **41.58** MHz: with two equal time constants the dominant-pole estimate errs **10**% low, and the Miller input estimate alone (75.07 MHz) would be **81**% high.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 12-03.1a | f_T | 5.305 | GHz |
| 12-03.2a | input capacitance | 205 | fF |
| 12-03.2b | output capacitance | 5.125 | fF |
| 12-03.3a | g_m | 38.68 | mA/V |
| 12-03.3b | C_π + C_μ | 12.31 | pF |
| 12-03.3c | C_π | 11.81 | pF |
| 12-03.3d | forward transit time | 0.2537 | ns |
| 12-03.4a | dominant-pole estimate | 9.091 | MHz |
| 12-03.4b | exact −3 dB | 9.902 | MHz |
| 12-03.4c | x² at the −3 dB point | 0.9806 | — |
| 12-03.4d | estimate's shortfall | 8 | % |
| 12-03.5a | gain | 20 | — |
| 12-03.5b | b_1 | 1.9 | ns |
| 12-03.5c | dominant-pole estimate | 83.77 | MHz |
| 12-03.5d | b_2 | 1.75 × 10⁻¹⁹ | s² |
| 12-03.5e | first pole | 88.28 | MHz |
| 12-03.5f | second pole | 1640 | MHz |
| 12-03.5g | zero | 31.83 | GHz |
| 12-03.5h | exact −3 dB | 88.02 | MHz |
| 12-03.5i | estimate's shortfall | 5 | % |
| 12-03.6a | input resistance | 10 | kΩ |
| 12-03.6b | output resistance | 0.99 | MΩ |
| 12-03.7a | gain | 5 | — |
| 12-03.7b | input pole | 15.92 | GHz |
| 12-03.7c | output pole | 397.9 | MHz |
| 12-03.8a | pole | 921.7 | MHz |
| 12-03.8b | zero | 2.190 | GHz |
| 12-03.9a | gate-to-drain gain | −2 | — |
| 12-03.9b | input capacitance with cascode | 80 | fF |
| 12-03.9c | input capacitance without | 360 | fF |
| 12-03.9d | ratio | 4.5 | — |
| 12-03.10a | gain–bandwidth product | 636.6 | MHz |
| 12-03.10b | load resistance for gain 10 | 2.5 | kΩ |
| 12-03.10c | bandwidth at gain 10 | 63.66 | MHz |
| 12-03.11a | zero frequency | 26.53 | GHz |
| 12-03.11b | phase lag at 1 GHz | 2.159 | ° |
| 12-03.11c | phase lag at the zero | 45 | ° |
| 12-03.12a | R_S for equal time constants | 10.67 | kΩ |
| 12-03.12b | b_1 | 4.24 | ns |
| 12-03.12c | dominant-pole estimate | 37.54 | MHz |
| 12-03.12d | exact −3 dB | 41.58 | MHz |
| 12-03.12e | Miller-only estimate | 75.07 | MHz |
| 12-03.12f | Miller-only estimate's excess | 81 | % |
| 12-03.12g | dominant-pole estimate's shortfall | 10 | % |
