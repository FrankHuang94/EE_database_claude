<!-- status: reviewed -->
# 21-01 · S-Parameters and Network Analysis

| | |
|---|---|
| **Course** | [21 · RF and Microwave Engineering](../README.md) |
| **University equivalent** | The network-analysis opening of a senior microwave-engineering course: power waves, the scattering matrix and its properties, conversions to Z, Y and ABCD, reference planes, vector network analyzer calibration and de-embedding, and two-port stability (Pozar, *Microwave Engineering*, the chapters on network analysis and amplifier stability) |
| **Prerequisites** | [07-10](../../07-circuit-analysis-2-transient-and-ac/chapters/07-10-two-port-networks.md) (Z, Y and ABCD two-ports), [13-08](../../13-electromagnetics/chapters/13-08-transmission-lines-sinusoidal-steady-state.md) (reflection coefficient, lines in sinusoidal steady state), [13-09](../../13-electromagnetics/chapters/13-09-smith-chart-and-matching.md) (Smith chart) |
| **Estimated study hours** | 8 |
| **Last verified** | 2026-11-24 |

**Learning objectives.** After this chapter you can:

1. Define incident and reflected power waves and the S-matrix, and translate $\lvert S_{11}\rvert$ and $\lvert S_{21}\rvert$ into return loss, VSWR, mismatch loss and insertion loss.
2. Derive the S-parameters of series, shunt and transmission-line two-ports, and convert between S, Z and ABCD.
3. Use reciprocity and losslessness to sanity-check S-parameter data.
4. Move reference planes, cascade networks with transfer matrices, and de-embed a fixture.
5. Derive the one-port error model of a vector network analyzer and calibrate it with short, open and load standards.
6. Test a two-port for unconditional stability (K–Δ and μ tests), draw stability circles, and compute the maximum stable and available gains.

## 1. Big picture

At low frequencies we describe circuits by voltages and currents measured at nodes. At radio and microwave frequencies that breaks down: a probe's own capacitance loads the node, wires are a sizable fraction of a wavelength, and an open or short circuit, the conditions that define Z and Y parameters, is hard to make and can make an active device oscillate. RF engineers instead describe a network by how it scatters waves: what fraction of a wave sent into one port comes back, and what fraction comes out of each other port, with every port terminated in a matched load. These **scattering parameters** are what vector network analyzers measure, what data sheets publish and what every RF simulator speaks.

- **Every RF data sheet** gives S-parameters (for transistors, filters, switches, connectors, cables, packages) in a standard file format.
- **Return loss and insertion loss** are how antennas, filters and front-end modules are specified.
- **High-speed digital** links (PCIe, Ethernet SerDes, HBM channels in AI accelerators) specify their channels and packages with S-parameters too.
- **Stability** of every amplifier is checked from S-parameters before it is built.
- **Measurement credibility** rests on calibration and de-embedding: a data sheet's S-parameters are only as good as the reference planes they were measured at.

## 2. Intuition first

```text
            a1 →                         → b2
   port 1 ──────[        two-port        ]────── port 2
            ← b1                         ← a2

   S11 = b1/a1 with port 2 matched (a2 = 0): the echo at port 1
   S21 = b2/a1 with port 2 matched:          what gets through
```

*Figure 1. Waves at a two-port. Each port has an incident wave $a$ and a reflected or emerging wave $b$. With the far port matched, nothing comes back into it, so each S-parameter is a simple ratio of two waves.*

**A sonar analogy.** Imagine sending a pulse into a pipe and listening at both ends. The echo you hear back at your end tells you about obstacles near you ($S_{11}$); the sound that arrives at the far end tells you how much got through ($S_{21}$). If the far end of the pipe were a hard wall, it would echo too and confuse your measurement, so you put an anechoic termination there: that is the "matched port" condition. The analogy breaks in one way: RF waves carry both amplitude and phase, and S-parameters are complex numbers that keep both.

## 3. Theory

### 3.1 Power waves

At a port with voltage phasor $\mathbf{V}$ and current phasor $\mathbf{I}$ (into the port, peak-amplitude phasors) and a real reference impedance $Z_0$ (usually 50 Ω), define the incident and reflected waves

$$
a = \frac{\mathbf{V} + Z_0\mathbf{I}}{2\sqrt{Z_0}}, \qquad b = \frac{\mathbf{V} - Z_0\mathbf{I}}{2\sqrt{Z_0}} ,
$$

with units of √W. Inverting, $\mathbf{V} = \sqrt{Z_0}(a + b)$ and $\mathbf{I} = (a - b)/\sqrt{Z_0}$. The power delivered into the port is

$$
P = \tfrac12\text{Re}(\mathbf{V}\mathbf{I}^*) = \tfrac12\text{Re}\left[(a + b)(a - b)^*\right] = \tfrac12\left(\lvert a\rvert^2 - \lvert b\rvert^2\right) ,
$$

because the cross terms $b a^* - a b^*$ are purely imaginary. So $\lvert a\rvert^2/2$ is the incident power and $\lvert b\rvert^2/2$ the reflected power: the waves are normalized so that their squared magnitudes are powers (the ½ comes from peak-amplitude phasors). On a line of characteristic impedance $Z_0$ these are exactly the forward and backward traveling waves of 13-08, scaled by $1/\sqrt{Z_0}$. Kurokawa's original power waves allow a complex reference impedance [1]; with a real $Z_0$, as here and in every VNA, the definitions coincide [2].

A one-port with impedance $Z$ has $\mathbf{V} = Z\mathbf{I}$, so its reflection coefficient is

$$
\Gamma = \frac{b}{a} = \frac{Z - Z_0}{Z + Z_0} ,
$$

the same Γ as in 13-08. The common figures of merit follow:

- **Return loss** $\text{RL} = -20\log_{10}\lvert\Gamma\rvert$ dB (larger is better);
- **VSWR** $= (1 + \lvert\Gamma\rvert)/(1 - \lvert\Gamma\rvert)$, the ratio of maximum to minimum voltage along a line feeding the load;
- **Mismatch loss** $= -10\log_{10}(1 - \lvert\Gamma\rvert^2)$ dB, the power lost to reflection.

### 3.2 The scattering matrix

For an $N$-port the waves are related linearly, $\mathbf{b} = S\mathbf{a}$. (In this chapter the matrices $S$, $Z$ and $T$ and the identity $I$ are written in plain type, and transposes as $^T$ and $^H$, because bold is reserved for the wave and port vectors $\mathbf{a}$, $\mathbf{b}$, $\mathbf{V}$ and $\mathbf{I}$.) For two ports,

$$
\begin{bmatrix}b_1\\ b_2\end{bmatrix} = \begin{bmatrix}S_{11} & S_{12}\\ S_{21} & S_{22}\end{bmatrix}\begin{bmatrix}a_1\\ a_2\end{bmatrix} , \qquad S_{ij} = \left.\frac{b_i}{a_j}\right|_{a_k = 0,\ k \ne j} .
$$

The condition $a_k = 0$ means port $k$ is terminated in $Z_0$: a matched load reflects nothing back. So $S_{11}$ is the input reflection coefficient with the output matched, $S_{21}$ the forward transmission (gain), $S_{12}$ the reverse transmission (isolation) and $S_{22}$ the output reflection coefficient. **Insertion loss** is $-20\log_{10}\lvert S_{21}\rvert$, and **gain** in dB is $20\log_{10}\lvert S_{21}\rvert$, the transducer gain between matched source and load.

**Two properties that check data.**

- **Reciprocity.** A network of linear, passive, isotropic materials (resistors, capacitors, inductors, lines, but not transistors, ferrites or amplifiers) has $Z = Z^T$, and therefore $S = S^T$: $S_{12} = S_{21}$.
- **Losslessness.** Power conservation for every possible input means $\sum\lvert b_i\rvert^2 = \sum\lvert a_i\rvert^2$, that is $\mathbf{a}^H(S^HS - I)\mathbf{a} = 0$ for all $\mathbf{a}$, so $S^HS = I$: S is unitary. For a two-port, each column has unit norm, $\lvert S_{11}\rvert^2 + \lvert S_{21}\rvert^2 = 1$, and the columns are orthogonal. A passive lossy network has $\lvert S_{11}\rvert^2 + \lvert S_{21}\rvert^2 < 1$; the shortfall is the fraction of input power absorbed.

### 3.3 S-parameters of simple two-ports

**Series impedance Z between the ports.** Drive port 1 with port 2 terminated in $Z_0$. The input impedance is $Z + Z_0$, so $S_{11} = (Z + Z_0 - Z_0)/(Z + Z_0 + Z_0) = Z/(Z + 2Z_0)$. The output voltage is $\mathbf{V}_2 = \mathbf{V}_1 Z_0/(Z + Z_0)$ with $\mathbf{V}_1 = \sqrt{Z_0}(a_1 + b_1) = \sqrt{Z_0}\,a_1(1 + S_{11})$, and with port 2 matched $b_2 = \mathbf{V}_2/\sqrt{Z_0}$:

$$
S_{21} = \frac{(1 + S_{11})Z_0}{Z + Z_0} = \frac{2Z_0}{Z + 2Z_0}, \qquad S_{11} = S_{22} = \frac{Z}{Z + 2Z_0} .
$$

**Shunt admittance Y to ground.** By the same steps (input impedance $Z_0\parallel 1/Y$), $S_{11} = -YZ_0/(2 + YZ_0)$ and $S_{21} = 2/(2 + YZ_0)$.

**Matched line.** A lossless line of impedance $Z_0$ and electrical length $\theta = \beta\ell$ just delays the wave: $S_{11} = 0$, $S_{21} = e^{-j\theta}$.

**Mismatched line.** A line of impedance $Z_c \ne Z_0$ is easiest through its ABCD matrix (13-08): $A = D = \cos\theta$, $B = jZ_c\sin\theta$, $C = j\sin\theta/Z_c$, then the conversion of §3.4.

![Magnitude in dB of S11 and S21 of a 75 ohm line that is an eighth wavelength long at 1 GHz, in a 50 ohm system, from 0 to 8 GHz: S11 dips to nothing at 0, 4 and 8 GHz and peaks at about minus 8.3 dB at 2 and 6 GHz, while S21 stays within about 0.7 dB of 0 dB; a dashed line marks 1 GHz](../../../assets/figures/21-01/line.svg)

*Figure 2. The mismatched line of Example 21-01.3 over frequency. Its reflection vanishes where it is a whole number of half waves long and peaks where it is an odd number of quarter waves, at $(Z_c^2 - Z_0^2)/(Z_c^2 + Z_0^2)$ = **0.385** (−**8.3** dB).*

### 3.4 Conversions and cascades

**From Z.** With $\mathbf{V} = Z\mathbf{I}$ for the port vectors, $\sqrt{Z_0}(\mathbf{a} + \mathbf{b}) = Z(\mathbf{a} - \mathbf{b})/\sqrt{Z_0}$, so $(Z + Z_0I)\mathbf{b} = (Z - Z_0I)\mathbf{a}$ and

$$
S = (Z - Z_0I)(Z + Z_0I)^{-1}, \qquad Z = Z_0(I + S)(I - S)^{-1} ,
$$

the matrix version of Γ.

**From ABCD.** With $\mathbf{V}_1 = A\mathbf{V}_2 - B\mathbf{I}_2$ and $\mathbf{I}_1 = C\mathbf{V}_2 - D\mathbf{I}_2$ (ABCD uses current flowing *out* of port 2), substituting the waves and solving gives

$$
S_{11} = \frac{A + B/Z_0 - CZ_0 - D}{\Delta_A}, \quad S_{21} = \frac{2}{\Delta_A}, \quad S_{12} = \frac{2(AD - BC)}{\Delta_A}, \quad S_{22} = \frac{-A + B/Z_0 - CZ_0 + D}{\Delta_A} ,
$$

with $\Delta_A = A + B/Z_0 + CZ_0 + D$. A reciprocal network has $AD - BC = 1$, so $S_{12} = S_{21}$.

**Cascades.** S-matrices do not multiply in a chain, because port 2 of one network feeds port 1 of the next with waves going both ways. Two remedies: convert to ABCD and multiply, or use **transfer (T) parameters**, which relate the waves on the left to those on the right:

$$
\begin{bmatrix}b_1\\ a_1\end{bmatrix} = T\begin{bmatrix}a_2\\ b_2\end{bmatrix}, \qquad T = \begin{bmatrix}S_{12} - S_{11}S_{22}/S_{21} & S_{11}/S_{21}\\ -S_{22}/S_{21} & 1/S_{21}\end{bmatrix} .
$$

The waves leaving port 2 of one network are the waves entering port 1 of the next, so a chain is the product $T_{total} = T_1T_2\cdots T_n$.

**Moving reference planes.** Adding a matched line of electrical length $\theta_k$ in front of port $k$ delays the incident wave and the reflected wave by $\theta_k$ each, so

$$
S'_{ij} = S_{ij}\,e^{-j(\theta_i + \theta_j)} : \qquad S'_{11} = S_{11}e^{-2j\theta_1} .
$$

A reflection measured through a length of line rotates clockwise on the Smith chart by twice the line's electrical length.

### 3.5 Measuring S-parameters: the vector network analyzer

A **vector network analyzer** (VNA) generates a sine at each test frequency, separates incident from reflected waves with directional couplers or bridges at each port, and measures their ratios with coherent receivers, giving magnitude and phase. Its hardware is imperfect: the coupler leaks some incident wave into the reflected channel (finite **directivity**), the test port is not a perfect 50 Ω (**source match**), and the cables and receivers have their own frequency response (**tracking**). Calibration measures these errors with known standards and removes them mathematically.

**The one-port error model.** Between the ideal reflectometer and the device lies an error two-port with terms $e_{00}$ (directivity), $e_{11}$ (source match) and $e_{10}e_{01}$ (reflection tracking). The measured reflection is the input reflection of that error box terminated in the device's Γ (the formula of §3.7 applied to the error box):

$$
\Gamma_m = e_{00} + \frac{e_{10}e_{01}\,\Gamma}{1 - e_{11}\Gamma} .
$$

Three unknowns need three standards. With an ideal load (Γ = 0), short (Γ = −1) and open (Γ = +1), measured as $M_L$, $M_S$ and $M_O$:

- the load gives $e_{00} = M_L$ directly;
- writing $t = e_{10}e_{01}$, the short gives $M_S - e_{00} = -t/(1 + e_{11})$ and the open $M_O - e_{00} = t/(1 - e_{11})$;
- dividing, $(M_O - e_{00})/(M_S - e_{00}) = -(1 + e_{11})/(1 - e_{11})$, which solves to $e_{11} = (M_S + M_O - 2e_{00})/(M_O - M_S)$, and then $t = (M_O - e_{00})(1 - e_{11})$.

Inverting the error model corrects any later measurement: $\Gamma = (\Gamma_m - e_{00})/[t + e_{11}(\Gamma_m - e_{00})]$ (Example 21-01.5). A full two-port calibration adds transmission terms (the **12-term model**: six error terms per direction) and is done with short-open-load-through (SOLT) standards or with through-reflect-line (TRL), which uses a transmission line as the impedance reference and needs no precisely known load [7, 9]. Real standards are not ideal: their small deviations are described by the calibration kit's models, and the calibration is only as accurate as those models.

### 3.6 De-embedding

A transistor or chip cannot be connected directly to coaxial cables: it sits in a fixture (a board, a package, probe pads). Calibration moves the reference plane to the cable ends; **de-embedding** moves it further, through the fixture, to the device. If the fixture halves A and B have been characterized (from a thru, from simulation, or from separate standards), the measurement is the cascade $T_m = T_AT_{DUT}T_B$, so

$$
T_{DUT} = T_A^{-1}\,T_m\,T_B^{-1} .
$$

Errors in the fixture model go straight into the device data, which is why de-embedded S-parameters carry a note of how they were obtained. On wafer, the usual first step subtracts the pads using "open" and "short" dummy structures [13].

### 3.7 Two-port stability

Terminate a two-port in a load with reflection $\Gamma_L$. The output wave $b_2$ reflects back as $a_2 = \Gamma_Lb_2$; eliminating $a_2$ from the S-equations gives the input reflection

$$
\Gamma_{in} = S_{11} + \frac{S_{12}S_{21}\Gamma_L}{1 - S_{22}\Gamma_L} ,
$$

and symmetrically $\Gamma_{out} = S_{22} + S_{12}S_{21}\Gamma_S/(1 - S_{11}\Gamma_S)$. If $\lvert\Gamma_{in}\rvert > 1$ for some passive load, the input presents a negative resistance and the circuit can oscillate. A two-port is **unconditionally stable** if $\lvert\Gamma_{in}\rvert < 1$ and $\lvert\Gamma_{out}\rvert < 1$ for every passive source and load ($\lvert\Gamma_S\rvert, \lvert\Gamma_L\rvert < 1$).

**Stability circles.** The boundary $\lvert\Gamma_{in}\rvert = 1$ maps, in the $\Gamma_L$ plane, to a circle (a bilinear map sends circles to circles). Setting $\lvert S_{11} - \Delta\Gamma_L\rvert = \lvert 1 - S_{22}\Gamma_L\rvert$ with $\Delta = S_{11}S_{22} - S_{12}S_{21}$ and completing the square gives the **output (load) stability circle**:

$$
C_L = \frac{(S_{22} - \Delta S_{11}^*)^*}{\lvert S_{22}\rvert^2 - \lvert\Delta\rvert^2}, \qquad R_L = \left\lvert\frac{S_{12}S_{21}}{\lvert S_{22}\rvert^2 - \lvert\Delta\rvert^2}\right\rvert .
$$

Which side is stable is decided by one test point: at $\Gamma_L = 0$, $\Gamma_{in} = S_{11}$, so if $\lvert S_{11}\rvert < 1$ the side containing the origin is stable.

**Tests.** The device is unconditionally stable if and only if

$$
K = \frac{1 - \lvert S_{11}\rvert^2 - \lvert S_{22}\rvert^2 + \lvert\Delta\rvert^2}{2\lvert S_{12}S_{21}\rvert} > 1 \quad\text{and}\quad \lvert\Delta\rvert < 1 ,
$$

the Rollett test, which says the stability circles lie entirely outside the unit circle [4, 5]. A single-parameter equivalent is Edwards and Sinsky's [6]

$$
\mu = \frac{1 - \lvert S_{11}\rvert^2}{\lvert S_{22} - \Delta S_{11}^*\rvert + \lvert S_{12}S_{21}\rvert} > 1 ,
$$

which is the distance from the origin of the $\Gamma_L$ plane to the nearest unstable point; a larger μ means more margin.

![Load reflection plane for the 500 MHz transistor of Example 21-01.6: the unit circle of passive loads, a dashed stability circle of large radius whose arc cuts across the upper part of the disk, the region of the disk above that arc shaded as unstable, and a dotted circle of radius 0.498 around the origin touching the arc](../../../assets/figures/21-01/stability.svg)

*Figure 3. The stability circle at work (Example 21-01.6, 500 MHz). Loads in the shaded segment give $\lvert\Gamma_{in}\rvert > 1$; μ is the radius of the largest circle around the matched point that stays clear of them.*

**Gains.** A source with reflection $\Gamma_S$ and source wave $b_s$ has available power $P_{avs} = \lvert b_s\rvert^2/[2(1 - \lvert\Gamma_S\rvert^2)]$, and the wave it launches into the two-port is $a_1 = b_s/(1 - \Gamma_S\Gamma_{in})$. The output wave is $b_2 = S_{21}a_1/(1 - S_{22}\Gamma_L)$, and the load absorbs $P_L = \tfrac12\lvert b_2\rvert^2(1 - \lvert\Gamma_L\rvert^2)$. Their ratio is the **transducer gain**

$$
G_T = \frac{P_L}{P_{avs}} = \frac{\lvert S_{21}\rvert^2(1 - \lvert\Gamma_S\rvert^2)(1 - \lvert\Gamma_L\rvert^2)}{\lvert 1 - \Gamma_S\Gamma_{in}\rvert^2\,\lvert 1 - S_{22}\Gamma_L\rvert^2} .
$$

With the load conjugately matched to the output ($\Gamma_L = \Gamma_{out}^*$) it becomes the **available gain**, a function of the source alone. Using $1 - \lvert\Gamma_{out}\rvert^2 = (\lvert 1 - S_{11}\Gamma_S\rvert^2 - \lvert S_{22} - \Delta\Gamma_S\rvert^2)/\lvert 1 - S_{11}\Gamma_S\rvert^2$ and expanding,

$$
G_A = \frac{\lvert S_{21}\rvert^2(1 - \lvert\Gamma_S\rvert^2)}{D_2 - 2\,\text{Re}(C_1\Gamma_S) + D_1\lvert\Gamma_S\rvert^2}, \qquad D_1 = \lvert S_{11}\rvert^2 - \lvert\Delta\rvert^2,\quad D_2 = 1 - \lvert S_{22}\rvert^2,\quad C_1 = S_{11} - \Delta S_{22}^* .
$$

**Maximizing it** gives the simultaneous conjugate match. Choose the phase of $\Gamma_S$ so that $\text{Re}(C_1\Gamma_S) = \lvert C_1\rvert r$ with $r = \lvert\Gamma_S\rvert$; then minimize $f(r) = (D_2 - 2\lvert C_1\rvert r + D_1r^2)/(1 - r^2)$. Setting $f'(r) = 0$ and collecting terms gives $\lvert C_1\rvert r^2 - B_1r + \lvert C_1\rvert = 0$ with $B_1 = D_1 + D_2 = 1 + \lvert S_{11}\rvert^2 - \lvert S_{22}\rvert^2 - \lvert\Delta\rvert^2$. Its roots multiply to 1, so the passive one is the smaller,

$$
\Gamma_{S,opt} = \frac{B_1 - \sqrt{B_1^2 - 4\lvert C_1\rvert^2}}{2C_1} ,
$$

and symmetrically for $\Gamma_L$ with $B_2 = 1 + \lvert S_{22}\rvert^2 - \lvert S_{11}\rvert^2 - \lvert\Delta\rvert^2$ and $C_2 = S_{22} - \Delta S_{11}^*$. At a stationary point $f$ equals the ratio of the derivatives of its numerator and denominator, $f = \lvert C_1\rvert/r - D_1$, and $1/r$ is the larger root, $[B_1 + \sqrt{B_1^2 - 4\lvert C_1\rvert^2}]/(2\lvert C_1\rvert)$. Two identities finish the job: $\lvert C_1\rvert^2 = \lvert S_{12}S_{21}\rvert^2 + D_1D_2$ (expand both sides), so $B_1^2 - 4\lvert C_1\rvert^2 = (D_2 - D_1)^2 - 4\lvert S_{12}S_{21}\rvert^2 = 4\lvert S_{12}S_{21}\rvert^2(K^2 - 1)$, because $D_2 - D_1 = 2K\lvert S_{12}S_{21}\rvert$ by the definition of K. Then $f_{min} = \lvert S_{12}S_{21}\rvert(K + \sqrt{K^2 - 1})$, and since $(K + \sqrt{K^2 - 1})(K - \sqrt{K^2 - 1}) = 1$, the **maximum available gain** is

$$
G_{max} = \frac{\lvert S_{21}\rvert^2}{f_{min}} = \left\lvert\frac{S_{21}}{S_{12}}\right\rvert\left(K - \sqrt{K^2 - 1}\right) .
$$

A real, passive solution exists only when $B_1^2 > 4\lvert C_1\rvert^2$, that is $K > 1$, with the "−" root passive when $B_1 > 0$: simultaneous conjugate matching requires unconditional stability. The **maximum stable gain** $\text{MSG} = \lvert S_{21}/S_{12}\rvert$, the limit of $G_{max}$ as K → 1, is the most gain obtainable from a conditionally stable device, after enough resistive loading to bring K to 1.

A transistor is often unconditionally stable at high frequency and only conditionally stable at low frequency, where its gain is highest (Example 21-01.6): stability must be checked across the whole band where the device has gain, not just the operating band.

> **Going deeper — why K > 1 and |Δ| < 1 together.** K > 1 alone ensures that the stability circle does not cut the unit disk, but the disk could lie entirely inside the unstable region; |Δ| < 1 (or, equivalently, $B_1 = 1 + \lvert S_{11}\rvert^2 - \lvert S_{22}\rvert^2 - \lvert\Delta\rvert^2 > 0$) rules that out. The μ test combines both in one number.

## 4. Worked examples

All examples use $Z_0$ = 50 Ω.

### Example 21-01.1 · A 75 Ω load in a 50 Ω system (tier A)

**Setup.** A 75 Ω antenna feed is connected to a 50 Ω transceiver. Find Γ, return loss, VSWR, mismatch loss and the fraction of power reflected.

**Solution.**

- Γ = (75 − 50)/(75 + 50) = **0.2**.
- RL = −20 log₁₀ 0.2 = **13.98** dB; VSWR = 1.2/0.8 = **1.50**.
- Reflected power $\lvert\Gamma\rvert^2$ = **4**%, a mismatch loss of −10 log₁₀ 0.96 = **0.177** dB.

**Units check.** All quantities are ratios.

**Sanity check.** A 1.5:1 VSWR loses less than 0.2 dB: small mismatches cost little transmitted power, which is why 10–15 dB return loss is a common specification.

### Example 21-01.2 · A series R + jX (tier A)

**Setup.** A two-port is a series 10 Ω resistor and an inductor with 40 Ω reactance at 1 GHz. Find its S-parameters, insertion loss and the fraction of incident power it dissipates.

**Solution.** $Z = 10 + j40$ Ω and $Z + 2Z_0 = 110 + j40$ Ω.

- $S_{11} = Z/(Z + 100)$ = **0.352**∠**56.0**°.
- $S_{21} = 100/(110 + j40)$ = **0.854**∠**−20.0**°: insertion loss **1.37** dB.
- Dissipated fraction $1 - \lvert S_{11}\rvert^2 - \lvert S_{21}\rvert^2$ = **14.6**%; the rest is reflected (12.4%) or transmitted (73.0%).

**Units check.** Ω/Ω.

**Sanity check.** The network is reciprocal and symmetric ($S_{12} = S_{21}$, $S_{22} = S_{11}$), and lossy, so the power sum is below 1. With R = 0 it would be exactly 1. ngspice reproduces all four numbers (§5).

### Example 21-01.3 · A mismatched line (tier B)

**Setup.** A lossless 75 Ω line one-eighth of a wavelength long (θ = 45°) sits in a 50 Ω system. Find its S-parameters and check losslessness.

**Solution.** ABCD: $A = D = \cos 45°$ = 0.7071, $B = j75\sin 45°$ = $j$53.03 Ω, $C = j\sin 45°/75$ = $j$0.009428 S. Then $\Delta_A = 1.4142 + j(1.0607 + 0.4714) = 1.4142 + j1.5321$, and

- $S_{11} = j(1.0607 - 0.4714)/\Delta_A$ = **0.283**∠**42.7**°;
- $S_{21} = 2/\Delta_A$ = **0.959**∠**−47.3**°.

$0.283^2 + 0.959^2$ = **1.000**: lossless, as it must be.

**Units check.** B/Z₀ and CZ₀ are dimensionless.

**Sanity check.** The transmission phase is not exactly −45°: multiple reflections inside the mismatched section add a little. This 75 Ω section reflects **8**% of the power, a return loss of **11** dB; the reflection depends on the section's length and vanishes at multiples of half a wavelength.

### Example 21-01.4 · Removing a feed line (tier B)

**Setup.** A reflection of 0.3∠−40° is measured at 10 GHz at the end of a 5 mm microstrip line with effective permittivity 4. What is the reflection at the device?

**Solution.** $\beta = 2\pi f\sqrt{\varepsilon_{eff}}/c$ = 419.2 rad/m, so θ = βℓ = **120.1**° one way and **240.2**° round trip. The device's reflection is $S'_{11}e^{+2j\theta}$ = 0.3∠(−40° + 240.2°) = **0.3**∠**−159.8**°.

**Units check.** rad/m × m = rad.

**Sanity check.** Lossless line: the magnitude is unchanged, only the angle rotates. Getting the length wrong by even 1 mm (**48**° of round-trip phase at 10 GHz) moves the device's impedance noticeably on the Smith chart: reference planes matter.

### Example 21-01.5 · Calibrating a one-port (tier B)

**Setup.** A reflectometer reads, for an ideal short, open and load, $M_S = -0.6757 + j0.3961$, $M_O = 0.8857 - j0.5264$ and $M_L = 0.0500 + j0.0200$. It then reads $M = 0.4507 + j0.2690$ for a device. Find the error terms and the device's true reflection.

**Solution.**

- $e_{00} = M_L$ = 0.0500 + $j$0.0200.
- $e_{11} = (M_S + M_O - 2e_{00})/(M_O - M_S)$ = **0.1000** − $j$**0.0500**.
- $t = (M_O - e_{00})(1 - e_{11})$ = 0.7795 − $j$0.4500 = **0.900**∠**−30.0**°.
- $\Gamma = (M - e_{00})/[t + e_{11}(M - e_{00})]$ = **0.500**∠**60.0**°. The raw reading, 0.525∠30.8°, was 30° off in phase.

**Units check.** Reflection coefficients are dimensionless.

**Sanity check.** Plugging Γ = 0.5∠60° into the error model reproduces the raw reading. The phase error came mostly from the tracking term's −30°: uncalibrated phase is meaningless.

### Example 21-01.6 · Is the transistor stable? (tier B)

**Setup.** A transistor's S-parameters are, at 2 GHz, $S_{11}$ = 0.6∠−160°, $S_{21}$ = 4.0∠80°, $S_{12}$ = 0.05∠50°, $S_{22}$ = 0.5∠−40°; and at 500 MHz, $S_{11}$ = 0.85∠−60°, $S_{21}$ = 9∠120°, $S_{12}$ = 0.03∠60°, $S_{22}$ = 0.7∠−25°. Test stability at each frequency and find the gains; at 500 MHz, find the load stability circle.

**Solution.**

- 2 GHz: $\lvert\Delta\rvert$ = **0.161**, K = **1.040**, μ = **1.019**: unconditionally stable, just. MSG = 4/0.05 = 80 (**19.0** dB); $G_{max}$ = 80(1.040 − √(1.040² − 1)) = **60.3** (**17.8** dB).
- 500 MHz: $\lvert\Delta\rvert$ = **0.674**, K = **0.449**, μ = **0.498**: potentially unstable. MSG = 300 (**24.8** dB).
- Load stability circle at 500 MHz: centre **8.20**∠**77.7**°, radius **7.70**. The circle's nearest point to the origin is 8.20 − 7.70 = **0.498** from it (equal to μ), so loads with $\lvert\Gamma_L\rvert$ above about 0.5 near 77.7° make the input unstable. Since $\lvert S_{11}\rvert < 1$, the origin side (outside the circle) is the stable one.

**Units check.** All dimensionless; gains in dB use 10 log₁₀ because K, MSG and $G_{max}$ are power ratios.

**Sanity check.** Lower frequency: more gain, and input and output closer to the edge of the Smith chart (less resistive loss), even though $S_{12}$ is smaller here. Low-frequency instability is common, and designers add resistive loading or feedback that costs little gain at the operating frequency.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 21-01.1a | reflection coefficient | 0.2 | — |
| Ex 21-01.1b | return loss | 13.98 | dB |
| Ex 21-01.1c | VSWR | 1.50 | — |
| Ex 21-01.1d | reflected power | 4 | % |
| Ex 21-01.1e | mismatch loss | 0.177 | dB |
| Ex 21-01.2a | magnitude of S11 | 0.352 | — |
| Ex 21-01.2b | angle of S11 | 56.0 | ° |
| Ex 21-01.2c | magnitude of S21 | 0.854 | — |
| Ex 21-01.2d | angle of S21 | −20.0 | ° |
| Ex 21-01.2e | insertion loss | 1.37 | dB |
| Ex 21-01.2f | dissipated power | 14.6 | % |
| Ex 21-01.2g | reflected power | 12.4 | % |
| Ex 21-01.2h | transmitted power | 73.0 | % |
| Ex 21-01.3a | magnitude of S11 | 0.283 | — |
| Ex 21-01.3b | angle of S11 | 42.7 | ° |
| Ex 21-01.3c | magnitude of S21 | 0.959 | — |
| Ex 21-01.3d | angle of S21 | −47.3 | ° |
| Ex 21-01.3e | power sum | 1.000 | — |
| Ex 21-01.3f | return loss | 11 | dB |
| Ex 21-01.3g | reflected power | 8 | % |
| Ex 21-01.4a | one-way electrical length | 120.1 | ° |
| Ex 21-01.4b | round-trip rotation | 240.2 | ° |
| Ex 21-01.4c | device reflection magnitude | 0.3 | — |
| Ex 21-01.4d | device reflection angle | −159.8 | ° |
| Ex 21-01.4e | round-trip phase per mm | 48 | ° |
| Ex 21-01.5a | e11 real part | 0.1000 | — |
| Ex 21-01.5b | e11 imaginary part | −0.0500 | — |
| Ex 21-01.5c | tracking magnitude | 0.900 | — |
| Ex 21-01.5d | tracking angle | −30.0 | ° |
| Ex 21-01.5e | corrected magnitude | 0.500 | — |
| Ex 21-01.5f | corrected angle | 60.0 | ° |
| Ex 21-01.5g | raw magnitude | 0.525 | — |
| Ex 21-01.5h | raw angle | 30.8 | ° |
| Ex 21-01.6a | Δ at 2 GHz | 0.161 | — |
| Ex 21-01.6b | K at 2 GHz | 1.040 | — |
| Ex 21-01.6c | μ at 2 GHz | 1.019 | — |
| Ex 21-01.6d | MSG at 2 GHz | 19.0 | dB |
| Ex 21-01.6e | Gmax | 60.3 | — |
| Ex 21-01.6f | Gmax | 17.8 | dB |
| Ex 21-01.6g | Δ at 500 MHz | 0.674 | — |
| Ex 21-01.6h | K at 500 MHz | 0.449 | — |
| Ex 21-01.6i | μ at 500 MHz | 0.498 | — |
| Ex 21-01.6j | MSG at 500 MHz | 24.8 | dB |
| Ex 21-01.6k | circle centre magnitude | 8.20 | — |
| Ex 21-01.6l | circle centre angle | 77.7 | ° |
| Ex 21-01.6m | circle radius | 7.70 | — |
| Ex 21-01.6n | nearest unstable distance | 0.498 | — |
| Txt 21-01.a | peak reflection of the 75 Ω line | 0.385 | — |
| Txt 21-01.b | peak reflection of the 75 Ω line | −8.3 | dB |
| Txt 21-01.c | reflection magnitude at 10 dB return loss | 0.316 | — |
| Txt 21-01.d | VSWR at 10 dB return loss | 1.92 | — |
| Txt 21-01.e | mismatch loss at 10 dB return loss | 0.46 | dB |
| Txt 21-01.f | reflection magnitude at 20 dB return loss | 0.100 | — |
| Txt 21-01.g | VSWR at 20 dB return loss | 1.22 | — |
| Txt 21-01.h | mismatch loss at 20 dB return loss | 0.04 | dB |
| Txt 21-01.i | dynamic range gained per decade of narrower IF bandwidth | 10 | dB |
| Txt 21-01.j | effective directivity with a VSWR 1.5 adapter | 14 | dB |
| Txt 21-01.k | lowest reading of a true 20 dB return loss | 19.6 | dB |
| Txt 21-01.l | highest reading of a true 20 dB return loss | 20.5 | dB |
| Txt 21-01.m | lowest reading of a true 35 dB return loss | 32.8 | dB |
| Txt 21-01.n | highest reading of a true 35 dB return loss | 37.9 | dB |
| Txt 21-01.o | reflection added by 46 dB residual directivity | 0.005 | — |

## 5. Simulate it

The lab ([labs/21-01-lab](../labs/21-01-lab/README.md)) collects the chapter's formulas in `sparam.py` and confirms three two-ports with ngspice's S-parameter analysis.

**Predict, then run.**

1. Predict which loads between 10 Ω and 250 Ω give the same return loss, then tabulate them (Part 1).
2. Predict the S-parameters of Examples 21-01.2 and 21-01.3 and of a 6 dB attenuator built from standard resistors, then run `ngspice -b sparams.cir` (Part 2).
3. Predict the result of converting a Z-matrix to S and back, and of cascading two pads and a line with T-matrices, then compute them (Part 3).
4. Predict how far off a raw reflectometer reading can be, then calibrate a simulated one with short, open and load and correct a sweep (Part 4).
5. Predict where the 500 MHz transistor of Example 21-01.6 is unstable, map $\lvert\Gamma_{in}\rvert$ over the load plane, and find the output shunt resistor that stabilizes Problem 11's transistor (Part 5).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Reference impedance (50 Ω versus 75 Ω or differential 100 Ω) | Compatibility with instruments and standards | Mismatch to devices whose natural impedance differs | System architect |
| Calibration type (SOLT, TRL, electronic) | Accuracy at the reference plane | Time, standards cost, frequency-range limits | Test engineer |
| De-embedding by model versus by measured standards | Access to the bare device | Error from fixture models; more test structures | Device or modeling engineer |
| Resistive stabilization of a transistor | Unconditional stability over all frequencies | Gain and noise figure at the operating frequency | RF designer |
| Frequency points and IF bandwidth in a VNA sweep | Resolution and dynamic range | Sweep time | Test engineer |

## 7. Numbers to know

| Quantity | Typical value | Note |
|---|---|---|
| Return loss 10 dB | $\lvert\Gamma\rvert$ = **0.316**, VSWR **1.92**, mismatch loss **0.46** dB | A common antenna and module specification |
| Return loss 20 dB | $\lvert\Gamma\rvert$ = **0.100**, VSWR **1.22**, mismatch loss **0.04** dB | A good instrument or connector port |
| Reference impedance | 50 Ω (RF instruments and coax), 75 Ω (video and cable TV), 100 Ω differential (high-speed serial links) | Conventions, not physics [Established] |
| VNA system dynamic range, 10 Hz IF bandwidth | specified 129 to 146 dB from about 0.5 to 50 GHz (typical up to 151 dB; much less below 50 MHz); typical 96 to 111 dB up to 110 GHz | Three vendors' data sheets, Aug 2022 to Aug 2026 [R-362] |
| Narrower IF bandwidth | **10** dB more dynamic range per decade of bandwidth | Receiver noise power is proportional to bandwidth |
| Residual errors after a coaxial calibration | directivity 46 to 60 dB, source match 31 to 43 dB (46 dB typical), load match 42 to 58 dB | Two vendors' specified values (typical where stated), as of Apr–Aug 2026 [R-362] |
| Adapter with VSWR 1.5 after calibration | effective directivity about **14** dB | HP application note [9, R-361] |
| Return-loss uncertainty with 46 dB residual directivity and 43 dB source match | 20 dB reads as **19.6** to **20.5** dB; 35 dB as **32.8** to **37.9** dB | Worst-case phases of those two terms only (Marketing vs Reality, §9) |
| Unconditional stability | $K > 1$ and $\lvert\Delta\rvert < 1$, or $\mu > 1$ | At every frequency where the device has gain |

## 8. Common mistakes

- **Treating S-parameters as properties of the device alone.** They depend on the reference impedance and the reference planes; quote both.
- **Multiplying S-matrices to cascade networks.** Use ABCD or T matrices.
- **Forgetting the round trip.** A line of electrical length θ rotates a reflection by 2θ.
- **Confusing return loss's sign.** Return loss is a positive number of dB; $\lvert S_{11}\rvert$ in dB is negative. "−15 dB return loss" means 15 dB.
- **Checking stability only in band.** Transistors are most prone to oscillate at low frequency, where gain is highest.
- **Using K > 1 without |Δ| < 1** (or use μ, which needs no second condition).
- **Trusting uncalibrated phase.** Raw VNA phase includes cables and coupler errors.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **The definitions are sixty years old and settled [Established].** Kurokawa defined power waves in 1965, with a possibly complex reference impedance, and stated the simultaneous-match and unconditional-stability conditions in S-parameter terms [1]. Hewlett-Packard's 1967 *HP Journal* article, later reissued as Application Note 95-1, carried them into instrument practice [3]. Marks and Williams separated traveling waves, defined by a line's own characteristic impedance, from pseudo-waves, defined by an arbitrary reference impedance [2]; what a VNA reports and what this chapter uses are pseudo-waves with a real 50 Ω reference, and the subtleties matter only for complex reference impedances and lossy lines.
- **The stability tests have a lineage [Established].** Rollett's 1962 factor was defined with immittance parameters and called "the basic invariant stability factor" [4]; Woods reworked the unconditional-stability conditions in S-parameters in 1976 [5]; Edwards and Sinsky showed in 1992 that "mu >1 alone is necessary and sufficient" [6]. Simulators report both K and μ.
- **Calibration is the measurement [Established].** The HP/Agilent application note describes twelve-term error correction, "a total of twelve error terms" with six in each direction, prefers SOLT in coax and recommends TRL for "noncoaxial environments, such as testing waveguide, using test fixtures, or making on-wafer measurements with probes" [9]. TRL, published by Engen and Hoer in 1979, removed the need for a precisely known short or other calibration circuit [7]; NIST's multiline TRL uses several redundant lines for better accuracy and bandwidth [8]. On wafer, the open–short de-embedding of Koolen and colleagues (1991) is still the standard first step [13]. Rohde & Schwarz calls SOLT "TOSM" [R-362].
- **Instruments [Established for the data, Industry estimate for any comparison].** Keysight's PNA-X Pro data sheet (August 2026) specifies 144 dB of system dynamic range for its 50 GHz model between 582 MHz and 7 GHz (150 dB typical) and 129 dB at 46–50 GHz; Rohde & Schwarz's ZNA (April 2026) quotes more than 129 dB specified, 147 dB typical with options and "up to 170 dB (maximum attainable range, allowing full 2-port correction)"; Anritsu's VectorStar broadband system covers 70 kHz to 110 GHz with 96 to 111 dB and the note "All values are typical" [R-362]. A USB VNA from Copper Mountain lists 152 dB typical at 10 Hz IF bandwidth up to 9 GHz [R-362].
- **The file format is Touchstone [Established].** The IBIS Open Forum ratified Touchstone 2.0 in April 2009 and 2.1 in January 2024; 2.1 is the current version as of Oct 2026. The format originated at Agilent, and no version 1.0 specification was ever published: files in the original syntax are simply called version 1.0 files [11, R-363]. Defaults matter: GHz, S-parameters, magnitude–angle, 50 Ω. A version-1.0 file normalizes the noise resistance $R_n$ to the reference resistance, while 2.0 and 2.1 files give it in ohms; mixing them changes $R_n$ by a factor of 50 [R-363].
- **High-speed digital runs on S-parameters [Established].** IEEE 802.3's Channel Operating Margin tool takes the victim channel and each aggressor as 4-port S-parameter models (.s4p files) [R-363], and IEEE Std 370-2020 standardizes the electrical characterization of printed-circuit interconnect up to 50 GHz [14]; channel models are routinely screened for passivity, reciprocity and causality before use. Differential channels use the mixed-mode S-parameters of Bockelman and Eisenstadt [12].

> **Deeper:** see companion repo *Datacenter Networking* for SerDes channels, COM and mixed-mode S-parameters at 100–200 Gb/s per lane.

### Why it matters commercially

- **S-parameter files are part of the product.** Every RF transistor, filter, switch, module and connector ships with them; a customer's first simulation, and often the design win, depends on how good they are and at which reference plane they were taken.
- **Characterization is a cost line.** It needs VNA time, calibration kits, fixtures and on-wafer probe stations, and de-embedding structures take area on every test wafer.
- **Oscillating amplifiers are field failures.** A device that is only conditionally stable at a frequency nobody simulated oscillates on a customer's board; the cost appears as returns and redesigns, not on the data sheet.

### Marketing vs Reality

- **"150 dB dynamic range."** It is usually a typical value, in the best band, in the high-gain receiver mode, at a 10 Hz IF bandwidth, without averaging and excluding crosstalk. Keysight's own data sheet defines "typical" as performance that "does not include guardbands" and "is not covered by the product warranty" [R-362]. Ask which column (specified or typical), which band and which IF bandwidth; and remember that a 1 Hz IF bandwidth buys 10 dB more by sweeping ten times slower.
- **"Return loss better than 35 dB."** Even a good coaxial calibration leaves residual directivity of about 46 dB, which adds an unknown reflection of $10^{-46/20}$ = **0.005** to every reading; with 43 dB of residual source match as well, a true 20 dB return loss reads anywhere from 19.6 to 20.5 dB, but a true 35 dB reads anywhere from 32.8 to 37.9 dB. Very high return-loss claims need a better calibration than the one used for ordinary parts. An adapter added after calibration is worse: a VSWR of 1.5 leaves an effective directivity of only about 14 dB [9].
- **"Unconditionally stable."** Ask where. Infineon's BGA8U1BN6 LNA data sheet states $k > 1$ from 20 MHz to 10 GHz with the footnote "Guaranteed by device design; not tested in production", and its gain and noise numbers carry "PCB losses are subtracted" [R-362]. That is an honest data sheet; a claim without such conditions should prompt the question of what was checked, at which bias and temperature, and whether the auxiliary condition (or μ) was included.
- **"Measured S-parameters."** Measured where? On-wafer data are de-embedded to the device terminals; packaged data include the package; evaluation-board data include the board. None is what the device sees on a customer's board, and each is right only for its own reference plane.

### Questions for engineering leaders

1. **"Over what frequency range did you check stability, and what is the minimum μ?"** *Strong:* from near DC to beyond the device's $f_{max}$, across bias, temperature and package corners, with the minimum μ and where it occurs. *Evasive:* "It's stable in our band."
2. **"Where are the reference planes of these S-parameters, and how was the fixture removed?"** *Strong:* names the calibration (SOLT, TRL, multiline TRL), the de-embedding structures and a check standard used to validate them. *Evasive:* "These are the measured data."
3. **"Is that dynamic range (or directivity) specified or typical, and under what conditions?"** *Strong:* gives the column, band, IF bandwidth and averaging. *Evasive:* quotes the brochure's headline.
4. **"Do your S-parameter models pass passivity, reciprocity and causality checks?"** *Strong:* runs them routinely, with quantified metrics, before releasing a model. *Evasive:* "The simulator handles that."
5. **"What is the measurement uncertainty on your return-loss specification?"** *Strong:* derives it from residual directivity and source match, and tests to a guard-banded limit. *Evasive:* "Our VNA is calibrated."

## 10. Concept check

**Q1.** Why are S-parameters measured with matched terminations rather than opens and shorts?

<details><summary>Answer</summary>

At RF, good opens and shorts are hard to realize (parasitic capacitance and inductance), and terminating an active device in an open or short can make it oscillate. A matched 50 Ω load is easy to make broadband and keeps the device stable during measurement.

</details>

**Q2.** A passive two-port has $\lvert S_{11}\rvert = 0.3$ and $\lvert S_{21}\rvert = 0.9$. What fraction of the input power does it absorb?

<details><summary>Answer</summary>

$1 - 0.09 - 0.81 = 0.10$: 10% is dissipated inside the network.

</details>

**Q3.** How would you tell from measured data that a network contains an amplifier or a ferrite?

<details><summary>Answer</summary>

It would not be reciprocal: $S_{12} \ne S_{21}$. An amplifier also has $\lvert S_{21}\rvert > 1$, which no passive network can.

</details>

**Q4.** What does each of the three one-port error terms represent physically?

<details><summary>Answer</summary>

$e_{00}$ (directivity): incident signal that leaks into the reflected channel without reaching the device. $e_{11}$ (source match): the test port's own reflection, which re-reflects the device's echo. $e_{10}e_{01}$ (tracking): the frequency response of the path to and from the device.

</details>

**Q5.** Why is a transistor more likely to be potentially unstable at low frequency?

<details><summary>Answer</summary>

At low frequency the device's input and output are nearly lossless ($\lvert S_{11}\rvert$ and $\lvert S_{22}\rvert$ approach 1), so the numerator of K, $1 - \lvert S_{11}\rvert^2 - \lvert S_{22}\rvert^2 + \lvert\Delta\rvert^2$, shrinks, while $\lvert S_{21}\rvert$ (and MSG) is largest. In Example 21-01.6 the numerator nearly halves even though $S_{12}$ itself is smaller.

</details>

**Q6.** What does de-embedding require, and what limits its accuracy?

<details><summary>Answer</summary>

A model or measurement of the fixture's S-parameters (or T-matrices) on each side of the device. Its accuracy is limited by how well the fixture is known: any error in the fixture model appears directly in the device's de-embedded data.

</details>

Problems: [21-01 problem set](../problems/21-01-problems.md) · Worked solutions: [21-01 solutions](../solutions/21-01-solutions.md)

## 11. Key terms

[S-parameters](../../../reference/glossary.md#s-parameters) · [Reflection coefficient](../../../reference/glossary.md#reflection-coefficient) · [Return loss](../../../reference/glossary.md#return-loss) · [VSWR](../../../reference/glossary.md#voltage-standing-wave-ratio-vswr) · [Insertion loss](../../../reference/glossary.md#insertion-loss) · [Vector network analyzer](../../../reference/glossary.md#vector-network-analyzer) · [De-embedding](../../../reference/glossary.md#de-embedding) · [Stability circle](../../../reference/glossary.md#stability-circle) · [Rollett stability factor](../../../reference/glossary.md#rollett-stability-factor)

## 12. Connections

- **Builds on:** [07-10](../../07-circuit-analysis-2-transient-and-ac/chapters/07-10-two-port-networks.md) (two-port parameters), [13-08](../../13-electromagnetics/chapters/13-08-transmission-lines-sinusoidal-steady-state.md) and [13-09](../../13-electromagnetics/chapters/13-09-smith-chart-and-matching.md) (lines, Γ and the Smith chart).
- **Next:** [21-02](21-02-impedance-matching-networks.md) designs the networks that transform impedances to $Z_0$.
- **Used later:** amplifier stability and gain in [21-04](21-04-low-noise-amplifiers.md) and [21-07](21-07-power-amplifiers.md); front-end modules in [21-09](21-09-rf-front-end.md).

## 13. Further study

- D. M. Pozar, *Microwave Engineering*, 4th ed., Wiley, 2012: the chapters on microwave network analysis and on microwave amplifier design (stability and gain).
- Hewlett-Packard Application Note 95-1, *S-Parameter Techniques for Faster, More Accurate Network Design* [3], and Application Note 1287-3, *Applying Error Correction to Network Analyzer Measurements* [9]: the classic practical introductions to S-parameters and VNA calibration. D. F. Williams, "Traveling Waves and Power Waves" [2], for the subtleties of wave definitions.

## 14. Sources

1. K. Kurokawa, "Power Waves and the Scattering Matrix," *IEEE Trans. Microwave Theory Tech.*, vol. 13, no. 2, pp. 194–202, Mar. 1965, DOI 10.1109/TMTT.1965.1125964 [R-361].
2. R. B. Marks and D. F. Williams, "A General Waveguide Circuit Theory," *J. Res. NIST*, vol. 97, no. 5, pp. 533–562, 1992, DOI 10.6028/jres.097.024; D. F. Williams, "Traveling Waves and Power Waves," *IEEE Microwave Magazine*, vol. 14, no. 7, pp. 38–45, Nov. 2013, DOI 10.1109/MMM.2013.2279494 [R-361].
3. Hewlett-Packard, Application Note 95-1, *S-Parameter Techniques for Faster, More Accurate Network Design* (based on R. W. Anderson's February 1967 *HP Journal* article; 1997 edition) [R-361].
4. J. M. Rollett, "Stability and Power-Gain Invariants of Linear Twoports," *IRE Trans. Circuit Theory*, vol. 9, no. 1, pp. 29–32, 1962, DOI 10.1109/TCT.1962.1086854 [R-361].
5. D. Woods, "Reappraisal of the unconditional stability criteria for active 2-port networks in terms of S parameters," *IEEE Trans. Circuits Syst.*, vol. 23, no. 2, pp. 73–81, Feb. 1976, DOI 10.1109/TCS.1976.1084179 [R-361].
6. M. L. Edwards and J. H. Sinsky, "A new criterion for linear 2-port stability using a single geometrically derived parameter," *IEEE Trans. Microwave Theory Tech.*, vol. 40, no. 12, pp. 2303–2311, Dec. 1992, DOI 10.1109/22.179894 [R-361].
7. G. F. Engen and C. A. Hoer, "Thru-Reflect-Line: An Improved Technique for Calibrating the Dual Six-Port Automatic Network Analyzer," *IEEE Trans. Microwave Theory Tech.*, vol. 27, no. 12, pp. 987–993, Dec. 1979, DOI 10.1109/TMTT.1979.1129778 [R-361].
8. R. B. Marks, "A multiline method of network analyzer calibration," *IEEE Trans. Microwave Theory Tech.*, vol. 39, no. 7, pp. 1205–1215, Jul. 1991, DOI 10.1109/22.85388 [R-361].
9. Hewlett-Packard, Application Note 1287-3, *Applying Error Correction to Network Analyzer Measurements*, literature no. 5965-7709E, 1997 [R-361].
10. D. M. Pozar, *Microwave Engineering*, 4th ed., Wiley, 2012.
11. IBIS Open Forum, *Touchstone File Format Specification*, Version 2.1, ratified 26 Jan 2024 (Version 2.0 ratified 24 Apr 2009) [R-363].
12. D. E. Bockelman and W. R. Eisenstadt, "Combined differential and common-mode scattering parameters: theory and simulation," *IEEE Trans. Microwave Theory Tech.*, vol. 43, no. 7, pp. 1530–1539, Jul. 1995, DOI 10.1109/22.392911 [R-363].
13. M. C. A. M. Koolen, J. A. M. Geelen and M. P. J. G. Versleijen, "An improved de-embedding technique for on-wafer high-frequency characterization," *Proc. Bipolar Circuits and Technology Meeting*, 1991, pp. 188–191, DOI 10.1109/BIPOL.1991.160985 [R-361].
14. *IEEE Std 370-2020*, "IEEE Standard for Electrical Characterization of Printed Circuit Board and Related Interconnects at Frequencies up to 50 GHz," DOI 10.1109/IEEESTD.2021.9316329 (title and scope only; the clauses were not read) [R-363].
15. Vendor data sheets: Keysight PNA-X Pro (3124-1589.EN, Aug 2026); Rohde & Schwarz ZNA specifications (v24.00, Apr 2026); Anritsu VectorStar ME7838A4 (11410-00704 Rev. P, Aug 2022); Copper Mountain Cobalt 9 GHz; Infineon BGA8U1BN6 (Rev. 3.2, Apr 2021) [R-362].
