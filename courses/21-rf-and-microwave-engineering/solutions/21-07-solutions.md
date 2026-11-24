# Solutions 21-07 · Power Amplifiers

Problems: [21-07 problem set](../problems/21-07-problems.md) · Chapter: [21-07](../chapters/21-07-power-amplifiers.md). Every number below is recomputed by [verify_21_07.py](../verify/verify_21_07.py).

---

## Solutions

### Solution 21-07.1

(a) 20 dBm = 100 mW, so η = 100/250 = **40.0** %.

(b) $P_{in}$ = 20 − 8 = 12 dBm = **15.85** mW.

(c) PAE = (100 − 15.85)/250 = **33.7** %: low gain costs almost 6 points.

(d) PAE = η − $P_{in}/P_{DC}$, so the gap is below one point when $P_{in}$ < 2.5 mW, i.e. a gain above 100/2.5 = 40, **16.0** dB. Millimetre-wave PAs rarely have that much gain per stage, which is why their PAE trails their drain efficiency.

### Solution 21-07.2

(a) $R_{opt} = (5 - 0.5)^2/(2 \times 2)$ = **5.06** Ω.

(b) 50/5.0625 = **9.88**, and (c) $Q = \sqrt{9.88 - 1}$ = **2.98**.

(d) $(3.4 - 0.4)^2/(2 \times 40)$ = **0.1125** Ω, and (e) a ratio of **444**. A single L-match would need Q ≈ 21, with a fractional bandwidth of only a few per cent and high loss in its components: 40 W must come from a higher supply or from many combined amplifiers.

### Solution 21-07.3

(a) $\eta_A = \tfrac12(1 - V_k/V_{DD}) = \tfrac12 \times 0.9$ = **45.0** %.

(b) The class-B swing is limited the same way: $(\pi/4)(1 - V_k/V_{DD})$ = **70.69** %.

### Solution 21-07.4

With $I_{max}$ = 1, $c = \cos(\alpha/2)$, $I_{DC} = (2\sin(\alpha/2) - \alpha c)/[2\pi(1 - c)]$ and $I_1 = (\alpha - \sin\alpha)/[2\pi(1 - c)]$:

- 300° (class AB): $I_{DC}$ = 0.4720, $I_1$ = 0.5204, (a) η = **55.13** %, (c) **+0.35** dB, (e) $R_{opt}$ = **1.921** $V_{DD}/I_{max}$.
- 150° (class C): $I_{DC}$ = 0.2693, $I_1$ = 0.4548, (b) η = **84.43** %, (d) **−0.82** dB, (f) **2.199** $V_{DD}/I_{max}$.

### Solution 21-07.5

(a) $R = 0.5768 \times 25/2$ = **7.210** Ω.

(b) $\omega$ = 5.655 × 10⁹ rad/s, $C = 0.1836/(\omega R)$ = **4.503** pF.

(c) $X = 1.1525R$ = **8.309** Ω and (d) $L_x = X/\omega$ = **1.469** nH.

(e) 3.562 × 5 V = **17.81** V.

(f) $I_{DC} = P/V_{DD}$ = **0.400** A and (g) the peak switch current is 2.862 × 0.4 = **1.145** A.

(h) The switch must see at most 12 V, so $V_{DD} \le 12/3.562$ = **3.369** V, and (i) with the same $R$ the power scales as $V_{DD}^2$: **0.908** W. A low-breakdown process gives up power, or needs a lower $R$ (a harder match) or stacked devices.

### Solution 21-07.6

(a) $v'(\theta) = V_1\sin\theta - 3V_3\sin3\theta = V_1\left(\sin\theta - \tfrac16\sin3\theta\right) = V_1\left(\tfrac12\sin\theta + \tfrac23\sin^3\theta\right) \ge 0$ for $0 \le \theta \le \pi$, so the minimum is at θ = 0, where $v = V_{DD} - V_1 + V_1/18 = V_{DD} - \tfrac{17}{18}V_1$. Hence $V_1 = \tfrac{18}{17}V_{DD}$ = **1.059** $V_{DD}$.

(b) η = $(\pi/4)(18/17)$ = **83.16** %: half the third-harmonic voltage buys about half of class F3's 9.8-point gain over class B.

### Solution 21-07.7

$x = 10^{-\text{BO}/20}$; class A $\tfrac12x^2$, class B $(\pi/4)x$, Doherty $(\pi/2)x$ for $x \le \tfrac12$ and $(\pi/2)x^2/(3x - 1)$ above.

- 3 dB ($x$ = 0.7079): (a) **25.06** %, (b) **55.60** %, (c) **70.05** %.
- 6 dB ($x$ = 0.5012, just above the Doherty's turn-on point): (d) **12.56** %, (e) **39.36** %, (f) **78.36** %.
- 10 dB ($x$ = 0.3162): (g) **5.00** %, (h) **24.84** %, (i) **49.67** %.

Below the first peak the Doherty is a class-B amplifier with twice the load, so its efficiency is exactly twice class B's.

### Solution 21-07.8

Integrating over the exponential envelope power as in Example 21-07.5, with the peak 8 dB above average:

(a) class B **35.23** %, (b) Doherty **61.23** %.

(c) $P_{DC}$ = 10/0.3523 = **28.38** W, (d) 10/0.6123 = **16.33** W, (e) a saving of **12.05** W, more than the output power itself.

### Solution 21-07.9

(a) The load must let the main reach full swing when only it conducts, at $x = 1/(1 + \gamma)$: $R_L = R_{opt}/(1 + \gamma)$ = **8.33** Ω. (b) $Z_0 = R_{opt}$ = **25** Ω.

(c) At peak both devices swing $V_{DD}$, the main with $I_{max}$ = 1.12 A and the auxiliary with $2I_{max}$: $P = (1 + \gamma)V_{DD}I_{max}/2$ = **47.04** W.

(d) The main sees $Z_0^2/R_L = 3R_{opt}$ and reaches full swing at $x$ = 1/3, a back-off of $20\log_{10}3$ = **9.54** dB, where (e) it delivers $P/9$ = **5.23** W at π/4.

(f) Above $x$ = 1/3 the auxiliary current is $(3x - 1)I_{max}$. The line gives $\lvert V_L\rvert = xV_{DD}$, and the load node needs $3xI_{max}$, so the line's output current is $I_{max}$ and the main stays at $V_{DD}$. Output power $x^2V_{DD}^2(1 + \gamma)/(2R_{opt})$, DC power $(2/\pi)V_{DD}I_{max}(x + 3x - 1)$:

$$
\eta = \frac{3\pi}{4}\cdot\frac{x^2}{4x - 1} .
$$

(g) Setting the derivative to zero, $2x(4x - 1) = 4x^2$, gives $x$ = **0.5**, where (h) η = $(3\pi/4)(1/4)$ = **58.90** %: deeper than the symmetric dip.

(i) Averaging over the OFDM envelope: **60.10** %, about 5 points better than the symmetric Doherty's 54.90%, because the first peak now sits near the signal's average power.

### Solution 21-07.10

$\eta_{ET} = \eta_{PA}\eta_{mod} \ge 54.90\%$:

(a) with the floor, $\eta_{PA}$ = 77.03% (Example 21-07.7), so $\eta_{mod} \ge$ **71.27** %;

(b) with perfect tracking, 78.54%, so $\eta_{mod} \ge$ **69.90** %.

A modulator that keeps 70% efficiency while tracking a 100 MHz-class envelope is the whole challenge.

### Solution 21-07.11

(a) $2(P_{in} - \text{IIP3}) - 4.77 \le -38$ gives $P_{in} - \text{IIP3} \le -16.61$ dB, so $P_{in} \le$ **−11.61** dBm.

(b) Third-order products span 3 × 100 = **300** MHz and (c) fifth-order **500** MHz: the observation receiver of a DPD system must capture that much.

### Solution 21-07.12

(a) $b_3 = -a_3/a_1$ = **0.2** V⁻².

(b) With $u = x(1 + b_3\lvert x\rvert^2)$, $u\lvert u\rvert^2 = x\lvert x\rvert^2(1 + b_3\lvert x\rvert^2)^3 = x\lvert x\rvert^2 + 3b_3x\lvert x\rvert^4 + \cdots$, so the output is $a_1x + (a_1b_3 + a_3)x\lvert x\rvert^2 + 3a_3b_3x\lvert x\rvert^4 + \cdots$; the third-order term vanishes and the fifth-order coefficient is $3a_3b_3$ = **−1.2** V⁻⁴.

(c) $\lvert a_3\rvert\lvert x\rvert^3$ = **0.25** V, (d) $1.2\lvert x\rvert^5$ = **0.0375** V, (e) an improvement of $20\log_{10}(0.25/0.0375)$ = **16.5** dB.

### Solution 21-07.13

(a) With $x = 10^{0.8}$ = 6.310, $e^{-x}$ = **1.82 × 10⁻³**.

(b) EVM = $10^{-39.25/20}$ = **1.09** %.

(c) 61.23 − 54.90 = **6.33** points (Problem 21-07.8 and Example 21-07.5). Clipping costs about 1% of EVM, affordable for most constellations, and the spectral regrowth it causes is filtered in baseband.

### Solution 21-07.14

(a) 26 dBm = **398.1** mW; (b) 26 − 28 = −2 dBm = **0.631** mW.

(c) $P_{DC} = (P_{out} - P_{in})/\text{PAE}$ = 397.5/0.4 = 993.7 mW, **261.5** mA from 3.8 V; (d) 795.0 mW, **209.2** mA.

(e) **52.3** mA, a fifth of the PA's current while transmitting.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 21-07.1a | drain efficiency | 40.0 | % |
| 21-07.1b | input power | 15.85 | mW |
| 21-07.1c | PAE | 33.7 | % |
| 21-07.1d | gain for a one-point gap | 16.0 | dB |
| 21-07.2a | R_opt, 2 W from 5 V | 5.06 | Ω |
| 21-07.2b | transformation ratio | 9.88 | |
| 21-07.2c | L-match Q | 2.98 | |
| 21-07.2d | R_opt, 40 W from 3.4 V | 0.1125 | Ω |
| 21-07.2e | transformation ratio | 444 | |
| 21-07.3a | tuned class A | 45.0 | % |
| 21-07.3b | class B | 70.69 | % |
| 21-07.4a | efficiency, 300° | 55.13 | % |
| 21-07.4b | efficiency, 150° | 84.43 | % |
| 21-07.4c | power vs class A, 300° | 0.35 | dB |
| 21-07.4d | power vs class A, 150° | −0.82 | dB |
| 21-07.4e | normalized R_opt, 300° | 1.921 | |
| 21-07.4f | normalized R_opt, 150° | 2.199 | |
| 21-07.5a | R | 7.210 | Ω |
| 21-07.5b | shunt C | 4.503 | pF |
| 21-07.5c | excess reactance | 8.309 | Ω |
| 21-07.5d | excess inductance | 1.469 | nH |
| 21-07.5e | peak switch voltage | 17.81 | V |
| 21-07.5f | DC current | 0.400 | A |
| 21-07.5g | peak switch current | 1.145 | A |
| 21-07.5h | highest supply for 12 V breakdown | 3.369 | V |
| 21-07.5i | power at that supply | 0.908 | W |
| 21-07.6a | largest V1 | 1.059 | V_DD |
| 21-07.6b | efficiency | 83.16 | % |
| 21-07.7a | class A, 3 dB | 25.06 | % |
| 21-07.7b | class B, 3 dB | 55.60 | % |
| 21-07.7c | Doherty, 3 dB | 70.05 | % |
| 21-07.7d | class A, 6 dB | 12.56 | % |
| 21-07.7e | class B, 6 dB | 39.36 | % |
| 21-07.7f | Doherty, 6 dB | 78.36 | % |
| 21-07.7g | class A, 10 dB | 5.00 | % |
| 21-07.7h | class B, 10 dB | 24.84 | % |
| 21-07.7i | Doherty, 10 dB | 49.67 | % |
| 21-07.8a | class B average, 8 dB PAPR | 35.23 | % |
| 21-07.8b | Doherty average, 8 dB PAPR | 61.23 | % |
| 21-07.8c | DC power, class B | 28.38 | W |
| 21-07.8d | DC power, Doherty | 16.33 | W |
| 21-07.8e | saving | 12.05 | W |
| 21-07.9a | load | 8.33 | Ω |
| 21-07.9b | inverter impedance | 25 | Ω |
| 21-07.9c | peak power | 47.04 | W |
| 21-07.9d | first-peak back-off | 9.54 | dB |
| 21-07.9e | power at the first peak | 5.23 | W |
| 21-07.9g | dip location | 0.5 | |
| 21-07.9h | dip efficiency | 58.90 | % |
| 21-07.9i | average efficiency, OFDM | 60.10 | % |
| 21-07.10a | modulator efficiency, 20 % floor | 71.27 | % |
| 21-07.10b | modulator efficiency, perfect tracking | 69.90 | % |
| 21-07.11a | highest average input power | −11.61 | dBm |
| 21-07.11b | third-order bandwidth | 300 | MHz |
| 21-07.11c | fifth-order bandwidth | 500 | MHz |
| 21-07.12a | b3 | 0.2 | V⁻² |
| 21-07.12b | residual fifth-order coefficient | −1.2 | V⁻⁴ |
| 21-07.12c | original third-order term | 0.25 | V |
| 21-07.12d | residual | 0.0375 | V |
| 21-07.12e | improvement | 16.5 | dB |
| 21-07.13a | clipping probability | 1.82e-3 | |
| 21-07.13b | EVM from clipping | 1.09 | % |
| 21-07.13c | Doherty efficiency gain | 6.33 | points |
| 21-07.14a | output power | 398.1 | mW |
| 21-07.14b | input power | 0.631 | mW |
| 21-07.14c | battery current at 40 % PAE | 261.5 | mA |
| 21-07.14d | battery current at 50 % PAE | 209.2 | mA |
| 21-07.14e | saving | 52.3 | mA |
