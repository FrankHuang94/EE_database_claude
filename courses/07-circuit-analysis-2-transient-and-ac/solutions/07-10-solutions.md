# Solutions 07-10 · Two-Port Networks

Problems: [07-10 problems](../problems/07-10-problems.md) · Chapter: [07-10](../chapters/07-10-two-port-networks.md). Every number below is recomputed by [verify_07_10.py](../verify/verify_07_10.py), which measures parameters by numerically applying the open- and short-circuit tests to nodal models of each circuit; the circuit results that ngspice also confirms are named in the `* EXPECT` lines of the netlists in [labs/07-10-lab](../labs/07-10-lab/README.md).

---

## Solutions

### Solution 07-10.1

(a) Series 50 Ω: $\begin{bmatrix}1 & 50\ \Omega\\0 & 1\end{bmatrix}$. Shunt 0.01 S: $\begin{bmatrix}1 & 0\\0.01\ \text{S} & 1\end{bmatrix}$.

(b) z-parameters need each port's voltage when currents are forced with the other port open. With both ports of a series resistor open, no current can flow, and $\mathbf{V}_1$ and $\mathbf{V}_2$ are not fixed by the currents (only their difference is). Dually, a shunt conductance makes $\mathbf{V}_1 = \mathbf{V}_2$ always, so the y test, which sets one port's voltage while shorting the other, is impossible: y-parameters cannot be defined. (Both elements do have h-parameters: the series resistor $\begin{bmatrix}50\ \Omega & 1\\-1 & 0\end{bmatrix}$ and the shunt conductance $\begin{bmatrix}0 & 1\\-1 & 0.01\ \text{S}\end{bmatrix}$.)

(c) $\begin{bmatrix}1 & 50\\0 & 1\end{bmatrix}\begin{bmatrix}1 & 0\\0.01 & 1\end{bmatrix} = \begin{bmatrix}1.5 & 50\ \Omega\\0.01\ \text{S} & 1\end{bmatrix}$, with determinant $1.5 - 0.5$ = **1.000**: reciprocal, as passive networks must be.

### Solution 07-10.2

$Y_a$ = 0.01 S, $Y_b$ = 0.005 S, $Y_c$ = 0.02 S. From §3.3: $y_{11}$ = **0.03000 S**, $y_{12} = y_{21}$ = **−0.02000 S**, $y_{22}$ = **0.02500 S**. $\Delta_y = 0.03\times0.025 - 0.0004 = 3.5\times10^{-4}$ S², so $z_{11} = y_{22}/\Delta_y$ = **71.43 Ω**, $z_{12} = z_{21} = -y_{12}/\Delta_y$ = **57.14 Ω**, $z_{22} = y_{11}/\Delta_y$ = **85.71 Ω**.

### Solution 07-10.3

- (a) $z_{12} = z_{21}$ and $z_{11} = z_{22}$: **reciprocal and symmetric**.
- (b) $y_{12} = y_{21}$, $y_{11} \ne y_{22}$: **reciprocal, not symmetric**.
- (c) $h_{12} = -h_{21}$: **reciprocal**. $\Delta_h = 50\times0.01 - 0.5\times(-0.5) = $ **0.75** $\ne 1$: **not symmetric**.
- (d) $AD - BC = 2 - 1$ = **1**: reciprocal; $A \ne D$: not symmetric.
- (e) $AD - BC = 3 - 1$ = **2**: **not reciprocal** (an active network); $A \ne D$: not symmetric either.

### Solution 07-10.4

$\Delta_z$ = 1100 Ω² (Example 07-10.1). $h_{11} = \Delta_z/z_{22}$ = **22.00 Ω**; $h_{12} = z_{12}/z_{22}$ = **0.6000**; $h_{21} = -z_{21}/z_{22}$ = **−0.6000**; $h_{22} = 1/z_{22}$ = **0.02000 S**. Reciprocity in h form, $h_{12} = -h_{21}$ ✓. (Check $h_{11}$ directly: with port 2 shorted, port 1 sees $10 + 30\parallel20 = 22$ Ω ✓.)

### Solution 07-10.5

(a) $\Delta_h = h_{11}h_{22} - h_{12}h_{21} = 0.04 - 0.03$ = **0.01000**. The y-parameters ($y_{11} = 1/h_{11}$, $y_{12} = -h_{12}/h_{11}$, $y_{21} = h_{21}/h_{11}$, $y_{22} = \Delta_h/h_{11}$): **0.5000 mS**, **−0.1000 µS**, **75.00 mS**, **5.000 µS**. The z-parameters ($z_{11} = \Delta_h/h_{22}$, $z_{12} = h_{12}/h_{22}$, $z_{21} = -h_{21}/h_{22}$, $z_{22} = 1/h_{22}$): **500.0 Ω**, **10.00 Ω**, **−7.500 MΩ**, **50.00 kΩ**.

(b) $A_v = -h_{21}Z_L/(h_{11} + \Delta_hZ_L) = -1.5\times10^6/2100$ = **−714.3**. $Z_{in} = h_{11} - h_{12}h_{21}Z_L/(1 + h_{22}Z_L) = 2000 - 300/1.2$ = **1750 Ω**.

(c) With $h_{12}$ = 0 it would be $h_{11}$ = **2000 Ω**. The small reverse ratio lowers the input impedance by 12.5% because the large output voltage feeds back to the input: a first look at the Miller effect (Problem 07-10.10).

### Solution 07-10.6

Each section at $\omega RC$ = 1: $\mathbf{T} = \begin{bmatrix}1 + j & R\\j/R & 1\end{bmatrix}$. Two sections give $\mathbf{T}^2 = \begin{bmatrix}3j & R(2 + j)\\(-1 + 2j)/R & 1 + j\end{bmatrix}$ (Example 07-10.3), and a third gives $A_{total} = 3j(1 + j) + R(2 + j)(j/R) = -4 + 5j$. The open-circuit gain $1/A_{total}$ has magnitude $1/\sqrt{41}$ = **0.1562** (**−16.13 dB**) at **−128.66°**. Three buffered sections give $0.7071^3$, **−9.03 dB**. Loading costs **7.10 dB** here, growing with each added section.

### Solution 07-10.7

(a) $Q = \sqrt{50/10 - 1}$ = 2. Series reactance $QR_L$ = 20 Ω, so $L = 20/(2\pi\times10^8)$ = **31.83 nH**; shunt reactance $50/Q$ = 25 Ω, so $C = 1/(2\pi\times10^8\times25)$ = **63.66 pF**.

(b) $\mathbf{T} = \begin{bmatrix}1 & 0\\j\omega C & 1\end{bmatrix}\begin{bmatrix}1 & j\omega L\\0 & 1\end{bmatrix}$ and $Z_{in} = (AR_L + B)/(CR_L + D)$. At 100 MHz: $j\omega C = j0.04$ S and $j\omega L = j20$ Ω give $\mathbf{T} = \begin{bmatrix}1 & j20\\j0.04 & 0.2\end{bmatrix}$, so $Z_{in} = (10 + j20)/(j0.4 + 0.2) = (10 + j20)/(0.2 + j0.4)$ = **50.00 Ω** ✓.

(c) At 110 MHz the reactances scale and $Z_{in}$ = 51.38 − j18.99 Ω, so $\lvert\Gamma\rvert = \lvert(Z_{in} - 50)/(Z_{in} + 50)\rvert$ = **0.1846** and the return loss is **14.68 dB**: a single L-section matches well only near its design frequency.

### Solution 07-10.8

(a) Both T networks share the common (ground) terminal at both ports, so connecting inputs and outputs in parallel leaves each network's port currents equal and opposite: the port condition holds and the y-parameters add (§3.7).

(b) For a T with series arms $Z_a$, $Z_b$ and shunt $Z_c$, $\mathbf{z} = \begin{bmatrix}Z_a + Z_c & Z_c\\Z_c & Z_b + Z_c\end{bmatrix}$, so with $\Delta_z = Z_aZ_b + Z_aZ_c + Z_bZ_c$ the inverse gives $y_{21} = -Z_c/\Delta_z$ and $y_{22} = (Z_a + Z_c)/\Delta_z$. Write $x = sRC$:

- T1 ($Z_a = Z_b = R$, $Z_c = 1/(2sC)$): $\Delta_z = R^2(1 + x)/x$, so $y_{21} = -\dfrac{1}{2R(1 + x)}$ and $y_{22} = \dfrac{1 + 2x}{2R(1 + x)}$.
- T2 ($Z_a = Z_b = 1/(sC)$, $Z_c = R/2$): $\Delta_z = R^2(1 + x)/x^2$, so $y_{21} = -\dfrac{x^2}{2R(1 + x)}$ and $y_{22} = \dfrac{x(2 + x)}{2R(1 + x)}$.

Adding:

$$
y_{21} = -\frac{1 + x^2}{2R(1 + x)}, \qquad y_{22} = \frac{1 + 4x + x^2}{2R(1 + x)}, \qquad H = -\frac{y_{21}}{y_{22}} = \frac{1 + (sRC)^2}{1 + 4sRC + (sRC)^2} = \frac{s^2 + \omega_0^2}{s^2 + 4\omega_0s + \omega_0^2} ,
$$

with $\omega_0 = 1/RC$. The numerator vanishes at $s = \pm j\omega_0$. At $s = j\omega_0/2$, $H = 0.75/(0.75 + j2)$. With $f_0$ = **1.592 kHz**:

| Frequency | Gain $-y_{21}/y_{22}$ |
|---|---|
| $f_0$ | **0** (a perfect notch) |
| $f_0/2$ and $2f_0$ | **0.3511** (−9.09 dB) |
| $0.9f_0$ | **0.05270** (−25.56 dB) |

At $f_0$ the two paths' transfer admittances are equal and opposite, so the output receives nothing: the low-pass T's lagging current cancels the high-pass T's leading one.

### Solution 07-10.9

(a) $K = 10^{6/20}$ = 1.995: $R_{sh} = 50\times2.995/0.995$ = **150.5 Ω** and $R_{se} = 50\times(3.981 - 1)/3.990$ = **37.35 Ω**.

(b) $\mathbf{T}$ = shunt × series × shunt $= \begin{bmatrix}1.248 & 37.35\ \Omega\\0.01494\ \text{S} & 1.248\end{bmatrix}$: $AD - BC$ = **1.000** (reciprocal) and $A = D$ (symmetric).

(c) $\Delta = A + B/Z_0 + CZ_0 + D$ = 3.990, so $S_{11} = (A + B/Z_0 - CZ_0 - D)/\Delta$ = **0** (matched) and $S_{21} = 2/\Delta$ = **0.5012**, i.e. **−6.00 dB**. The attenuator absorbs $1 - 0.5012^2$ = **74.9%** of the incident power, as a 6 dB pad must.

### Solution 07-10.10

(a) At 1 MHz, $j\omega C_\mu = j6.283$ µS. $y_{12} = -j6.283$ µS and $y_{21} = 40\ \text{mS} - j6.283\ \text{µS}$: not equal, so **not reciprocal** (the transconductance passes signal forward only).

(b) With $Y_L$ = 0.2 mS: $Y_{in}$ = **0.4328 + j1.211 mS**, an equivalent input capacitance of $1.211\times10^{-3}/(2\pi\times10^6)$ = **192.7 pF** in parallel with **2311 Ω**.

(c) $R_L' = 50\parallel5$ kΩ = 4545 Ω, $g_mR_L'$ = 181.8, so the Miller estimate is $10 + 1\times182.8$ = **192.8 pF**. The 1 pF feedback capacitor looks like 183 pF at the input because the output swings 182 times the input in antiphase: the input must charge $C_\mu$ through the whole difference. This **Miller effect** often sets an amplifier's bandwidth (Course 10).

### Solution 07-10.11

At 5 GHz a 1 pF capacitor has $Y = j31.42$ mS, $YZ_0 = j1.571$.

| Network | $\lvert S_{11}\rvert$ (angle) | $\lvert S_{21}\rvert$ (angle) | Insertion loss | Return loss |
|---|---|---|---|---|
| (a) shunt 1 pF | **0.6177** (**−128.15°**) | **0.7864** (**−38.15°**) | **2.087 dB** | **4.185 dB** |
| (b) series 10 Ω | **0.09091** (0°) | **0.9091** (0°) | **0.828 dB** | **20.83 dB** |
| (c) 10 Ω then 1 pF | **0.4392** (**−121.55°**) | **0.6904** (**−40.59°**) | **3.219 dB** | **7.146 dB** |

For (c), $\lvert S_{22}\rvert$ = **0.6543**: the network is not symmetric, so it reflects differently from each side (the capacitor is closer to port 2). $\lvert S_{11}\rvert^2 + \lvert S_{21}\rvert^2$ = 0.6695, so **33.1%** of the incident power is absorbed in the resistor. A 1 pF pad capacitance that was nearly invisible at 1 GHz (Example 07-10.6) reflects 38% of the power at 5 GHz.

### Solution 07-10.12

$\Gamma = (-25 + j25)/(75 + j25)$ = **0.4472 ∠ 116.57°**. Return loss $-20\lg0.4472$ = **6.99 dB**; mismatch loss $-10\lg(1 - 0.2)$ = **0.969 dB** (20% of the power is reflected); VSWR $= 1.4472/0.5528$ = **2.618**.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 07-10.1a | determinant of the cascade | 1.000 | — |
| 07-10.2a | $y_{11}$ | 0.03000 | S |
| 07-10.2b | $y_{12}$ | −0.02000 | S |
| 07-10.2c | $y_{22}$ | 0.02500 | S |
| 07-10.2d | $z_{11}$ | 71.43 | Ω |
| 07-10.2e | $z_{12}$ | 57.14 | Ω |
| 07-10.2f | $z_{22}$ | 85.71 | Ω |
| 07-10.3a | determinant (d) | 1 | — |
| 07-10.3b | determinant (e) | 2 | — |
| 07-10.3c | $\Delta_h$ (c) | 0.75 | — |
| 07-10.4a | $h_{11}$ | 22.00 | Ω |
| 07-10.4b | $h_{12}$ | 0.6000 | — |
| 07-10.4c | $h_{21}$ | −0.6000 | — |
| 07-10.4d | $h_{22}$ | 0.02000 | S |
| 07-10.5a | $\Delta_h$ | 0.01000 | — |
| 07-10.5b | $y_{11}$ | 0.5000 | mS |
| 07-10.5c | $y_{12}$ | −0.1000 | µS |
| 07-10.5d | $y_{21}$ | 75.00 | mS |
| 07-10.5e | $y_{22}$ | 5.000 | µS |
| 07-10.5f | $z_{11}$ | 500.0 | Ω |
| 07-10.5g | $z_{12}$ | 10.00 | Ω |
| 07-10.5h | $z_{21}$ | −7.500 | MΩ |
| 07-10.5i | $z_{22}$ | 50.00 | kΩ |
| 07-10.5j | voltage gain | −714.3 | — |
| 07-10.5k | input impedance | 1750 | Ω |
| 07-10.5l | input impedance without feedback | 2000 | Ω |
| 07-10.6a | unbuffered gain | 0.1562 | — |
| 07-10.6b | in dB | −16.13 | dB |
| 07-10.6c | phase | −128.66 | ° |
| 07-10.6d | buffered gain | −9.03 | dB |
| 07-10.6e | cost of loading | 7.10 | dB |
| 07-10.7a | L | 31.83 | nH |
| 07-10.7b | C | 63.66 | pF |
| 07-10.7c | input impedance at 100 MHz | 50.00 | Ω |
| 07-10.7d | reflection magnitude at 110 MHz | 0.1846 | — |
| 07-10.7e | return loss at 110 MHz | 14.68 | dB |
| 07-10.8a | $f_0$ | 1.592 | kHz |
| 07-10.8b | gain at $f_0$ | 0 | — |
| 07-10.8c | gain at $f_0/2$ and $2f_0$ | 0.3511 | — |
| 07-10.8d | in dB | −9.09 | dB |
| 07-10.8e | gain at $0.9f_0$ | 0.05270 | — |
| 07-10.8f | in dB | −25.56 | dB |
| 07-10.9a | shunt resistors | 150.5 | Ω |
| 07-10.9b | series resistor | 37.35 | Ω |
| 07-10.9c | A = D | 1.248 | — |
| 07-10.9d | C | 0.01494 | S |
| 07-10.9e | determinant | 1.000 | — |
| 07-10.9f | $S_{11}$ | 0 | — |
| 07-10.9g | $S_{21}$ | 0.5012 | — |
| 07-10.9h | in dB | −6.00 | dB |
| 07-10.9i | power absorbed | 74.9 | % |
| 07-10.10a | input conductance | 0.4328 | mS |
| 07-10.10b | input susceptance | 1.211 | mS |
| 07-10.10c | equivalent input capacitance | 192.7 | pF |
| 07-10.10d | equivalent input resistance | 2311 | Ω |
| 07-10.10e | Miller estimate | 192.8 | pF |
| 07-10.11a | $\lvert S_{11}\rvert$, shunt | 0.6177 | — |
| 07-10.11b | its angle | −128.15 | ° |
| 07-10.11c | $\lvert S_{21}\rvert$, shunt | 0.7864 | — |
| 07-10.11d | its angle | −38.15 | ° |
| 07-10.11e | insertion loss, shunt | 2.087 | dB |
| 07-10.11f | return loss, shunt | 4.185 | dB |
| 07-10.11g | $\lvert S_{11}\rvert$, series | 0.09091 | — |
| 07-10.11h | $\lvert S_{21}\rvert$, series | 0.9091 | — |
| 07-10.11i | insertion loss, series | 0.828 | dB |
| 07-10.11j | return loss, series | 20.83 | dB |
| 07-10.11k | $\lvert S_{11}\rvert$, cascade | 0.4392 | — |
| 07-10.11l | its angle | −121.55 | ° |
| 07-10.11m | $\lvert S_{21}\rvert$, cascade | 0.6904 | — |
| 07-10.11n | its angle | −40.59 | ° |
| 07-10.11o | insertion loss, cascade | 3.219 | dB |
| 07-10.11p | return loss, cascade | 7.146 | dB |
| 07-10.11q | $\lvert S_{22}\rvert$, cascade | 0.6543 | — |
| 07-10.11r | power absorbed, cascade | 33.1 | % |
| 07-10.11s | power reflected by the shunt capacitor | 38 | % |
| 07-10.12a | reflection magnitude | 0.4472 | — |
| 07-10.12b | its angle | 116.57 | ° |
| 07-10.12c | return loss | 6.99 | dB |
| 07-10.12d | mismatch loss | 0.969 | dB |
| 07-10.12e | VSWR | 2.618 | — |
