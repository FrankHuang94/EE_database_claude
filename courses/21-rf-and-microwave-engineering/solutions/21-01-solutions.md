# Solutions 21-01 · S-Parameters and Network Analysis

Problems: [21-01 problem set](../problems/21-01-problems.md) · Chapter: [21-01](../chapters/21-01-s-parameters.md). Every number below is recomputed by [verify_21_01.py](../verify/verify_21_01.py).

---

## Solutions

### Solution 21-01.1

100 Ω: Γ = 50/150 = **0.333**. 25 Ω: Γ = −25/75 = **−0.333**. Both: return loss **9.54** dB, VSWR **2.00**, mismatch loss **0.512** dB. The magnitudes match because 100 Ω and 25 Ω are a factor of 2 above and below 50 Ω; only the sign of Γ (the side of the Smith chart) differs.

### Solution 21-01.2

$\lvert\Gamma\rvert = 10^{-20/20}$ = **0.1**; VSWR = 1.1/0.9 = **1.22**; mismatch loss −10 log₁₀(0.99) = **0.044** dB.

### Solution 21-01.3

$Y = j2\pi \times 2\ \text{GHz} \times 1\ \text{pF} = j0.01257$ S, so $YZ_0 = j0.628$. $S_{11} = -j0.628/(2 + j0.628)$ = **0.300**∠**−107.4**°; $S_{21} = 2/(2 + j0.628)$ = **0.954**∠**−17.4**°; insertion loss **0.41** dB. The network is lossless: 0.300² + 0.954² = 1.

### Solution 21-01.4

With port 2 matched, port 1 sees $Z_0 \parallel (1/Y) = Z_0/(1 + YZ_0)$. Then $S_{11} = \Gamma = [Z_0/(1 + YZ_0) - Z_0]/[Z_0/(1 + YZ_0) + Z_0] = -YZ_0/(2 + YZ_0)$. Both ports share one node voltage, $\mathbf{V}_2 = \mathbf{V}_1 = \sqrt{Z_0}\,a_1(1 + S_{11})$, and with port 2 matched $b_2 = \mathbf{V}_2/\sqrt{Z_0}$, so $S_{21} = 1 + S_{11} = 2/(2 + YZ_0)$.

### Solution 21-01.5

$S = (Z - 50I)(Z + 50I)^{-1}$ with $Z - 50I = \begin{bmatrix}70 & 100\\ 100 & 70\end{bmatrix}$ and $Z + 50I = \begin{bmatrix}170 & 100\\ 100 & 170\end{bmatrix}$ (determinant 18900): $S_{11} = S_{22}$ = **0.1005**, $S_{21} = S_{12}$ = **0.529**. Insertion loss **5.53** dB; absorbed fraction $1 - 0.1005^2 - 0.529^2$ = **71.0**%.

### Solution 21-01.6

θ = 90°: $A = D = 0$, $B = j70.71$ Ω, $C = j/70.71$ S. $\Delta_A = j(1.4142 + 0.7071)$, so $S_{11} = j(1.4142 - 0.7071)/\Delta_A$ = **0.333**∠**0**° and $S_{21} = 2/\Delta_A$ = **0.943**∠**−90**°. Terminated in 100 Ω, $Z_{in} = B/(C \cdot 100) = Z_c^2/100$ = **50.0** Ω: the quarter-wave transformer of 13-09, matched to 50 Ω even though the bare line, in a 50 Ω system, reflects.

### Solution 21-01.7

K = 1.4125: $R_{sh}$ = **292.4** Ω and $R_{se}$ = **17.61** Ω. Each pad has $S_{21}$ = 0.708 (−3.00 dB) and $S_{11}$ = 0 (matched), so the cascade of pad, line and pad has $S_{21}$ = 0.708 × $e^{-j60°}$ × 0.708: **−6.00** dB at **−60.0**°. With matched pieces the T-matrix product reduces to multiplying the transmissions.

### Solution 21-01.8

Each line multiplies $S_{21}$ by $e^{-j30°}$, so the device has $S_{21}$ = 0.8∠(−100° + 60°) = **0.8**∠**−40**°.

### Solution 21-01.9

$e_{00} = M_L$; $e_{11} = (M_S + M_O - 2e_{00})/(M_O - M_S)$ = **0.0800** + $j$**0.0300**; $t = (M_O - e_{00})(1 - e_{11})$ = **0.850**∠**−50.0**°. Corrected: Γ = **0.300**∠**−120.0**°.

### Solution 21-01.10

$S_{12} \ne S_{21}$: **not reciprocal**. Column 1 has $\lvert S_{11}\rvert^2 + \lvert S_{21}\rvert^2$ = **0.85**, so it is lossy (**15**% of the power entering port 1 is absorbed); column 2 sums to 0.34, so much more is absorbed from port 2. A passive non-reciprocal device that passes forward and attenuates backward is an isolator (a ferrite device); if the device should have been reciprocal, the data are wrong.

### Solution 21-01.11

$\Delta = S_{11}S_{22} - S_{12}S_{21}$ gives $\lvert\Delta\rvert$ = **0.299**; K = **0.709**; μ = **0.786**; MSG = 3.5/0.08 = 43.75 (**16.4** dB). K < 1: **potentially unstable**.

### Solution 21-01.12

Cascade a shunt R at port 2 with T-matrices, compute μ as a function of R, and solve μ(R) = 1: R = **240** Ω, where K = 1 and $G_{max}$ = MSG = **43.75** (**16.4** dB). A smaller R gives more margin and less gain. A shunt (or series) resistor at one port is a reciprocal two-port in cascade: it scales $S_{21}$ and $S_{12}$ by the same factor, so their ratio, the MSG, does not change; what changes is K, and with it the gain that can actually be extracted stably.

### Solution 21-01.13

ABCD from S: $A = D = [(1 + S_{11})(1 - S_{22}) + S_{12}S_{21}]/(2S_{21})$ = **1.050**, $B = Z_0[(1 + S_{11})(1 + S_{22}) - S_{12}S_{21}]/(2S_{21})$ = **10.25** Ω, $C = [(1 - S_{11})(1 - S_{22}) - S_{12}S_{21}]/(2Z_0S_{21})$ = **0.0100** S. Each fixture is $\begin{bmatrix}1 & 5\\ 0 & 1\end{bmatrix}$, with inverse $\begin{bmatrix}1 & -5\\ 0 & 1\end{bmatrix}$. Removing both leaves $\begin{bmatrix}1 & 0\\ 0.01 & 1\end{bmatrix}$: a shunt admittance of 0.01 S, a **100** Ω resistor, whose own S-parameters are $S_{11}$ = **−0.2** and $S_{21}$ = **0.8**.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 21-01.1a | Γ for 100 Ω | 0.333 | — |
| 21-01.1b | Γ for 25 Ω | −0.333 | — |
| 21-01.1c | return loss | 9.54 | dB |
| 21-01.1d | VSWR | 2.00 | — |
| 21-01.1e | mismatch loss | 0.512 | dB |
| 21-01.2a | magnitude of Γ | 0.1 | — |
| 21-01.2b | VSWR | 1.22 | — |
| 21-01.2c | mismatch loss | 0.044 | dB |
| 21-01.3a | magnitude of S11 | 0.300 | — |
| 21-01.3b | angle of S11 | −107.4 | ° |
| 21-01.3c | magnitude of S21 | 0.954 | — |
| 21-01.3d | angle of S21 | −17.4 | ° |
| 21-01.3e | insertion loss | 0.41 | dB |
| 21-01.5a | S11 | 0.1005 | — |
| 21-01.5b | S21 | 0.529 | — |
| 21-01.5c | insertion loss | 5.53 | dB |
| 21-01.5d | absorbed fraction | 71.0 | % |
| 21-01.6a | magnitude of S11 | 0.333 | — |
| 21-01.6b | angle of S11 | 0 | ° |
| 21-01.6c | magnitude of S21 | 0.943 | — |
| 21-01.6d | angle of S21 | −90 | ° |
| 21-01.6e | input impedance | 50.0 | Ω |
| 21-01.7a | shunt arm | 292.4 | Ω |
| 21-01.7b | series arm | 17.61 | Ω |
| 21-01.7c | cascade S21 | −6.00 | dB |
| 21-01.7d | cascade S21 angle | −60.0 | ° |
| 21-01.8a | device S21 magnitude | 0.8 | — |
| 21-01.8b | device S21 angle | −40 | ° |
| 21-01.9a | e11 real part | 0.0800 | — |
| 21-01.9b | e11 imaginary part | 0.0300 | — |
| 21-01.9c | tracking magnitude | 0.850 | — |
| 21-01.9d | tracking angle | −50.0 | ° |
| 21-01.9e | corrected magnitude | 0.300 | — |
| 21-01.9f | corrected angle | −120.0 | ° |
| 21-01.10a | column power sum | 0.85 | — |
| 21-01.10b | absorbed fraction | 15 | % |
| 21-01.11a | Δ | 0.299 | — |
| 21-01.11b | K | 0.709 | — |
| 21-01.11c | μ | 0.786 | — |
| 21-01.11d | MSG | 16.4 | dB |
| 21-01.12a | shunt resistor | 240 | Ω |
| 21-01.12b | Gmax | 43.75 | — |
| 21-01.12c | Gmax | 16.4 | dB |
| 21-01.13a | A and D | 1.050 | — |
| 21-01.13b | B | 10.25 | Ω |
| 21-01.13c | C | 0.0100 | S |
| 21-01.13d | shunt resistor | 100 | Ω |
| 21-01.13e | its S11 | −0.2 | — |
| 21-01.13f | its S21 | 0.8 | — |
