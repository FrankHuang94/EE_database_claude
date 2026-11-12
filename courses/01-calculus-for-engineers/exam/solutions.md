# Course 01 · Final Exam — Solutions

Exam: [README.md](README.md). All numbers are recomputed by [verify_01_exam.py](../verify/verify_01_exam.py). Each solution names the chapter to revisit if you lost points.

**1.** *(01-01)* (a) Decibels add along a chain: $20 - 6 + 14 = 28$ dB. As a voltage ratio, $10^{28/20} = 25.12$; as a power ratio, $10^{28/10} = 631.0$. Check: $25.12^2 = 631$ ✓. (b) Solve $e^{-t/\tau} = 0.01$: $t = \tau\ln 100 = 2\text{ ms}\times\ln 100 = 9.210$ ms, about 4.6 time constants.

**2.** *(01-02)* (a) Rewrite as $3\cdot\dfrac{\sin 3x}{3x}$. As $x \to 0$, $3x \to 0$ and $\sin u/u \to 1$, so the limit is **3**.

(b) Divide top and bottom by $f$:

$$
f\,H(f) = \frac{f}{\sqrt{1 + (f/f_c)^2}} = \frac{f_c}{\sqrt{(f_c/f)^2 + 1}} \;\xrightarrow{f\to\infty}\; f_c = 1000\text{ Hz}.
$$

So at high frequency $H(f) \approx f_c/f$: the gain falls in proportion to $1/f$, which is −20 dB per decade, on a line that passes through 0 dB at $f = f_c$.

(c) Continuity at $t = 1$ s needs the left limit $2(1) = 2$ to equal the right value $a - 1$, so $a = 3$ V. The slopes are 2 V/s on the left and −1 V/s on the right, so the derivative is **not** continuous: $v$ has a corner. The capacitor current $i = C\,dv/dt$ jumps from $2C$ to $-C$ amperes (with $C$ in farads) at $t = 1$ s. That is physically allowed. A capacitor's *voltage* must be continuous, but its current can jump.

**3.** *(01-03)* (a) By the product rule,

$$
\frac{dv}{dt} = 5e^{-t/\tau}\left(\omega\cos\omega t - \frac{1}{\tau}\sin\omega t\right) \text{ V/s},
$$

so at $t = 0$, $dv/dt = 5\omega = 3.142\times10^7$ V/s. Then $i(0) = C\,dv/dt = 10^{-8} \times 3.142\times10^7 = 0.3142$ A $= 314.2$ mA. Units: F·V/s = C/s = A ✓. Sanity check: at 1 MHz the capacitor's reactance is $1/(\omega C) = 15.92\ \Omega$, and 5 V across 15.92 Ω is 314 mA ✓.

(b) By the chain rule, $\dfrac{d}{dx}\ln(1 + x^2) = \dfrac{2x}{1 + x^2}$. At $x = 2$ this is $4/5 = 0.8$.

(c) Differentiate both sides of $I = I_S(e^{V/V_T} - 1)$ with respect to $I$: $1 = \dfrac{I_S}{V_T}e^{V/V_T}\dfrac{dV}{dI}$. Since $I_S e^{V/V_T} = I + I_S$,

$$
\frac{dV}{dI} = \frac{V_T}{I + I_S} \approx \frac{V_T}{I}.
$$

At 1 mA this is $25.85\text{ mV}/1\text{ mA} = 25.85\ \Omega$. This is the diode's small-signal resistance, which reappears in Course 10.

**4.** *(01-04)* (a) The load power is $P = V_s^2R_L/(R_s + R_L)^2$. By the quotient rule,

$$
\frac{dP}{dR_L} = V_s^2\,\frac{(R_s + R_L)^2 - 2R_L(R_s + R_L)}{(R_s + R_L)^4} = V_s^2\,\frac{R_s - R_L}{(R_s + R_L)^3}.
$$

This is zero at $R_L = R_s = 50\ \Omega$. It is positive below and negative above, so that point is a maximum. $P_{max} = V_s^2/(4R_s) = 100/200 = 0.5000$ W.

(b) $P = 100 \times (10/150)^2 = 0.4444$ W, which is **88.89%** of the maximum.

(c) $P = 25 \times (10/75)^2 = 0.4444$ W, the same. Write $x = R_L/R_s$: then $P/P_{max} = 4x/(1 + x)^2$, which is unchanged when $x \to 1/x$. A mismatch by a factor $k$ in either direction costs $1 - 4k/(1 + k)^2 = \big((k - 1)/(k + 1)\big)^2$, which is $(1/3)^2 = 11.11\%$ for $k = 2$. The loss is small because the slope is zero at the peak: near a maximum, the loss grows with the *square* of the mismatch. This is why power-matched systems tolerate component spread.

**5.** *(01-04)* (a) KCL says the diode current equals the resistor current:

$$
g(V) = I_S\left(e^{V/V_T} - 1\right) - \frac{5 - V}{R} = 0, \qquad g'(V) = \frac{I_S}{V_T}e^{V/V_T} + \frac{1}{R}.
$$

At $V_0 = 0.7$ V, $I_Se^{V_0/V_T} = 5.760$ mA and the resistor carries 4.300 mA. So $g(V_0) = 1.460$ mA and $g'(V_0) = 5.760\text{ mA}/25.85\text{ mV} + 1\text{ mS} = 0.2238$ S. Newton's step is $g/g' = 6.522$ mV, so $V_1 = 0.6935$ V. Repeating at $V_1$ gives a step of 0.97 mV, so $V_2 = 0.69251$ V.

(b) A third iteration moves $V$ by only 0.02 mV. The converged value is $V = 0.69249$ V, and $I = (5 - 0.69249)/1000 = 4.308$ mA. The number of correct digits roughly doubles each step: quadratic convergence.

(c) $r_d = V_T/(I + I_S) = 25.85\text{ mV}/4.308\text{ mA} = 6.001\ \Omega$.

(d) For small changes, the diode acts like $r_d$, so it and $R$ form a voltage divider:

$$
\Delta V \approx \Delta V_s\,\frac{r_d}{R + r_d} = 0.1 \times \frac{6.001}{1006.0} = 0.5965\text{ mV}.
$$

The exact rise is 0.590 mV, so the linear estimate is about 1% high. When the supply rises, the current rises, so $r_d = V_T/I$ falls and each further increment of supply lifts $V$ a little less. $V$ is therefore a *concave* function of $V_s$, and a tangent line lies above a concave curve. This is the small-signal idea in action: the linear model is excellent for small changes, and its error is second order.

**6.** *(01-05)* (a) $Q = \int_0^\infty 3e^{-t/\tau}\,dt$ mA $= 3\text{ mA}\times\tau = 3\text{ mA}\times2\text{ ms} = 6.000$ µC. Units: A·s = C ✓.

(b) $Q(2\text{ ms}) = 6\text{ µC}\,(1 - e^{-1}) = 3.793$ µC, which is **63.21%** of the total. One time constant always delivers $1 - 1/e$ of the total.

**7.** *(01-06)* (a) By parts with $u = x$ and $dv = e^x\,dx$:

$$
\int_0^1 xe^x\,dx = \Big[xe^x\Big]_0^1 - \int_0^1 e^x\,dx = e - (e - 1) = 1.
$$

(b) Partial fractions give $\dfrac{1}{(x+1)(x+2)} = \dfrac{1}{x+1} - \dfrac{1}{x+2}$. So the integral is $\Big[\ln(x+1) - \ln(x+2)\Big]_0^1 = (\ln 2 - \ln 3) - (0 - \ln 2) = \ln(4/3) = 0.2877$.

(c) The resistor power is $p = v^2/R = (V_0^2/R)\,e^{-2t/RC}$. Then

$$
W = \int_0^\infty \frac{V_0^2}{R}e^{-2t/RC}\,dt = \frac{V_0^2}{R}\cdot\frac{RC}{2} = \tfrac12 CV_0^2.
$$

$R$ cancels: a small $R$ dissipates more power for a shorter time. Numerically, $W = 0.5 \times 10^{-6} \times 100 = 50.00$ µJ, exactly the energy the capacitor stored.

**8.** *(01-07)* Let the period be $T = 2\pi/\omega$.

(a) $V_{avg} = \dfrac{1}{T}\displaystyle\int_0^{T/2}10\sin\omega t\,dt = \dfrac{10}{T}\cdot\dfrac{2}{\omega} = \dfrac{10}{\pi} = 3.183$ V.

(b) $\overline{v^2} = \dfrac{1}{T}\displaystyle\int_0^{T/2}100\sin^2\omega t\,dt = \dfrac{1}{T}\cdot100\cdot\dfrac{T}{4} = 25\text{ V}^2$, so $V_{rms} = 5.000$ V. Half the time, the waveform has the full-wave mean square of 50 V².

(c) $P = V_{rms}^2/R = 25/50 = 0.5000$ W.

(d) $V_{avg}^2/R = 3.183^2/50 = 0.2026$ W, too low by a factor of $\pi^2/4 = 2.467$. Power is a *square*, and the average of a square is not the square of the average. Average value matters for DC (what a moving-coil meter or a battery charger sees). RMS matters for heating.

**9.** *(01-07)* (a) The density is $1/\Delta$ on $[-\Delta/2, \Delta/2]$, and the mean is zero, so

$$
\overline{e^2} = \frac{1}{\Delta}\int_{-\Delta/2}^{\Delta/2}e^2\,de = \frac{1}{\Delta}\cdot\frac{2}{3}\left(\frac{\Delta}{2}\right)^3 = \frac{\Delta^2}{12}, \qquad e_{rms} = \frac{\Delta}{\sqrt{12}}.
$$

(b) $\Delta = 1/4096$ V $= 244.1$ µV, and $e_{rms} = 244.1/\sqrt{12} = 70.48$ µV.

(c) The sine has amplitude 0.5 V and RMS $0.5/\sqrt2 = 0.3536$ V. So SNR $= 20\log_{10}(0.3536/70.48\times10^{-6}) = 74.01$ dB.

(d) For $N$ bits, the full-scale sine has RMS $2^N\Delta/(2\sqrt2)$, and the noise is $\Delta/\sqrt{12}$. Their ratio is $2^N\sqrt{12}/(2\sqrt2) = 2^N\sqrt{3/2}$. In dB,

$$
\text{SNR} = 20N\log_{10}2 + 20\log_{10}\sqrt{1.5} = 6.021N + 1.761\text{ dB}.
$$

Each bit adds 6.021 dB, because it halves $\Delta$. For $N = 12$: $72.25 + 1.761 = 74.01$ dB ✓. The rule of thumb, with its rounded coefficient, gives $6.02 \times 12 + 1.76 = 74.00$ dB; the 0.01 dB gap is rounding.

**10.** *(01-08)* (a) $P_3(0.1) = 1 + 0.1 + 0.005 + 0.0001667 = 1.105167$. The Lagrange remainder is $R_3 = e^{\xi}x^4/4!$ for some $\xi$ in (0, 0.1). We may not use the value of $e^{0.1}$ we are estimating, but $1 < e^{\xi} < e^{0.1} < 3^{0.1} < 1.2$ is safe. So the error lies between $10^{-4}/24 = 4.167\times10^{-6}$ and $1.2\times10^{-4}/24 = 5.0\times10^{-6}$. The actual error, $e^{0.1} - P_3 = 4.251\times10^{-6}$, is inside that range ✓.

(b) $\ln(1 + x) = x - x^2/2 + x^3/3 - x^4/4 + \cdots$. At $x = 0.2$, three terms give $0.2 - 0.02 + 0.002667 = 0.1827$. The true value is $\ln 1.2 = 0.1823$, so the actual error is $3.451\times10^{-4}$. The terms alternate in sign and shrink, so the error is smaller than the first omitted term, $0.2^4/4 = 4.0\times10^{-4}$ ✓.

(c) Let $a = 0.1$ and $\theta = \omega t$. Expanding,

$$
e^{a\cos\theta} \approx 1 + a\cos\theta + \frac{a^2}{2}\cos^2\theta = \left(1 + \frac{a^2}{4}\right) + a\cos\theta + \frac{a^2}{4}\cos2\theta.
$$

The second-harmonic amplitude over the fundamental is $(a^2/4)/a = a/4 = 2.5\%$. The next correction is a relative factor of about $1 - a^2/24$, a change of only 0.04%: the exact value, $I_2(0.1)/I_1(0.1)$ from modified Bessel functions, is 2.499%.

(d) With $f(x) = 1/x^2$, the remainder $\sum_{k=21}^\infty1/k^2$ lies between $\int_{21}^\infty x^{-2}dx = 1/21 = 0.04762$ and $\int_{20}^\infty x^{-2}dx = 1/20 = 0.05$. The actual error is $\pi^2/6 - S_{20} = 1.644934 - 1.596163 = 0.04877$, inside the bracket ✓. Twenty terms leave the second decimal wrong: this series converges slowly, as its $1/n$ remainder says.

**11.** *(01-10)* (a) Gross dies $= \pi d^2/(4A) - \pi d/\sqrt{2A}$ with $d = 300$ mm.

- 300 mm²: $235.6 - 38.48 = 197.1$.
- 600 mm²: $117.8 - 27.21 = 90.60$.

Doubling the area cuts gross dies by a factor of 2.18, not 2, because edge loss is a larger fraction for big dies.

(b) $A D_0$ is 0.21 and 0.42 (area in cm²).

- 300 mm²: $Y = e^{-0.21} = 81.06\%$, so 159.8 good dies.
- 600 mm²: $Y = e^{-0.42} = 65.70\%$, so 59.53 good dies.

(c) Cost per good die is \$17,000/159.8 = **\$106.4** for the small die and \$17,000/59.53 = **\$285.6** for the large one. The ratio is **2.68×**, not 2×.

(d) Rubric: 2 of the question's 5 points. Award 1 for the reasoning and 1 for two good questions.

- **Reasoning:** cost per good die grows faster than area for two reasons. Fewer dies fit, with relatively more edge loss, and yield falls exponentially with area. Here the result is 2.7× rather than 2×, and the gap widens with higher defect density.
- **Good questions:**
  - What defect density does the foundry quote for this node, and at what maturity?
  - Does the design have redundancy (spare cores or memory repair) that raises the effective yield?
  - Did you consider splitting it into two 300 mm² chiplets, and what would the advanced packaging and die-to-die interface cost?
  - What are the test and packaging costs per die, which also scale with area?

**12.** *(01-09)* (a) $f_0 = 1/\big(2\pi\sqrt{10^{-5}\times10^{-10}}\big) = 1/(2\pi\times3.162\times10^{-8}) = 5.033$ MHz.

(b) Take logs: $\ln f_0 = -\ln 2\pi - \tfrac12\ln L - \tfrac12\ln C$. Then $\dfrac{L}{f_0}\dfrac{\partial f_0}{\partial L} = \dfrac{\partial\ln f_0}{\partial\ln L} = -0.5$, and likewise $-0.5$ for $C$. So $\dfrac{\Delta f_0}{f_0} \approx -\tfrac12\dfrac{\Delta L}{L} - \tfrac12\dfrac{\Delta C}{C}$.

(c) Worst case, both errors add: $\tfrac12(2 + 5) = 3.5\%$.

(d) RSS: $\tfrac12\sqrt{2^2 + 5^2} = 2.693\%$. The capacitor contributes $25/29 = 86.2\%$ of the variance, so tighten it first. A ±1% capacitor would give $\tfrac12\sqrt{4 + 1} = 1.118\%$.

**13.** *(01-09)* (a) Form $\mathcal{L} = R_1I_1^2 + R_2I_2^2 - \lambda(I_1 + I_2 - I)$ and set the partial derivatives to zero: $2R_1I_1 = \lambda$ and $2R_2I_2 = \lambda$. So $R_1I_1 = R_2I_2$, and $I_1/I_2 = R_2/R_1 = 1.5$. With $I_1 + I_2 = 100$ A, $I_1 = 60$ A and $I_2 = 40$ A. The loss is $0.010 \times 3600 + 0.015 \times 1600 = 36 + 24 = 60.00$ W.

(b) $\lambda = 2R_1I_1 = 2 \times 0.010 \times 60 = 1.200$ W/A. It is the marginal loss: one more ampere of total load costs about 1.2 W of extra loss at the optimum. Check: the optimum loss is $R_{par}I^2$ with $R_{par} = R_1R_2/(R_1 + R_2) = 6$ mΩ, so $dP^*/dI = 2R_{par}I = 1.200$ W/A ✓.

(c) An equal split loses $0.010 \times 2500 + 0.015 \times 2500 = 62.50$ W, 4.17% more. The optimum condition $R_1I_1 = R_2I_2$ (= 0.6 V here) is exactly what two resistors in parallel do: they share the same voltage, so the current divides inversely to resistance. Physical parallel resistors settle into the current split that minimizes total dissipation, a fact worth remembering when converters are designed to share current.

(d) On the constraint, $P(I_1) = R_1I_1^2 + R_2(I - I_1)^2$, a parabola with $P'' = 2(R_1 + R_2) = 0.050\ \Omega > 0$. So the critical point is a minimum. The loss function is convex, so this minimum is global.

**14.** *(01-10 §3.6 and Problem 01-10.16)* (a) Take a cylinder of radius $r$ and length $\ell$. By symmetry $\vec{E}$ is radial and depends only on $r$, so the end caps carry no flux. Gauss's law gives $\varepsilon E\cdot2\pi r\ell = \lambda\ell$, with $\varepsilon = \varepsilon_0\varepsilon_r$, so

$$
E(r) = \frac{\lambda}{2\pi\varepsilon r}, \qquad a < r < b.
$$

(b) $V = \displaystyle\int_a^b \frac{\lambda}{2\pi\varepsilon r}\,dr = \frac{\lambda}{2\pi\varepsilon}\ln\frac{b}{a}$.

(c) Then

$$
C' = \frac{\lambda}{V} = \frac{2\pi\varepsilon_0\varepsilon_r}{\ln(b/a)} = \frac{2\pi \times 8.854\times10^{-12} \times 2.25}{\ln 3.5} = 99.92\text{ pF/m}.
$$

Here $\ln 3.5 = 1.253$ and $b = 1.575$ mm. Units: F/m ✓. Sanity check: about 100 pF/m is typical of polyethylene-insulated 50 Ω coax. This geometry gives a characteristic impedance of $\big(\sqrt{\mu_0/\varepsilon_0}/(2\pi\sqrt{\varepsilon_r})\big)\ln(b/a) = 50.1\ \Omega$, a result derived in Course 13.

(d) The charge is $\lambda = C'V = 99.92\text{ pF/m} \times 100\text{ V} = 9.992$ nC/m. The field is largest where $r$ is smallest, at the inner conductor's surface: $E(a) = V/\big(a\ln(b/a)\big) = 100/(0.45\times10^{-3} \times 1.253) = 177.4$ kV/m. This is why breakdown starts at the inner conductor, and why fine center wires limit a cable's voltage rating.

**15.** *(01-10)* (a) In polar coordinates, $dA = r\,dr\,d\theta$:

$$
I = \int_0^{2\pi}\!\!\int_0^a J_0\frac{r^2}{a^2}\,r\,dr\,d\theta = 2\pi J_0\frac{a^2}{4} = \frac{\pi J_0a^2}{2} = \frac{\pi \times 10\text{ A/mm}^2 \times 0.25\text{ mm}^2}{2} = 3.927\text{ A}.
$$

This is half of what a uniform $J_0$ would carry ($\pi J_0a^2 = 7.854$ A), because the density is low near the center.

(b) By symmetry $B$ is the same everywhere on a circle of radius $a$ and points around it, so $B\cdot2\pi a = \mu_0I$:

$$
B = \frac{\mu_0I}{2\pi a} = \frac{4\pi\times10^{-7} \times 3.927}{2\pi \times 5\times10^{-4}} = 1.571\text{ mT}.
$$

(c) The curl test: $\partial F_2/\partial x = 2x$ and $\partial F_1/\partial y = 2x$ agree everywhere in the plane, which has no holes, so $\vec{F}$ is conservative. Integrate $\partial\varphi/\partial x = 2xy + 1$ to get $\varphi = x^2y + x + h(y)$. Then $\partial\varphi/\partial y = x^2 + h'(y)$ must equal $x^2$, so $h$ is a constant and $\varphi = x^2y + x$. The work is $\varphi(1, 2) - \varphi(0, 0) = 2 + 1 = 3$, for any path.

(d) $\nabla\cdot\vec G = 1 + 1 + 2z$, so $\iiint\nabla\cdot\vec G\,dV = 1 + 1 + \int_0^1 2z\,dz = 3$. Outward fluxes: on $x = 1$ ($\hat n = \hat x$), $\iint G_x\,dA = \iint 1\,dA = 1$; on $x = 0$ ($\hat n = -\hat x$), $G_x = 0$, so 0. Likewise 1 on $y = 1$ and 0 on $y = 0$. On $z = 1$, $G_z = z^2 = 1$, giving 1; on $z = 0$, $G_z = 0$, giving 0. Total outward flux $= 3$, matching the volume integral ✓.

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X01.1a | total gain | 28 | dB |
| X01.1b | voltage ratio | 25.12 | — |
| X01.1c | power ratio | 631.0 | — |
| X01.1d | time to fall to 1% | 9.210 | ms |
| X01.2a | limit of sin(3x)/x | 3 | — |
| X01.2b | high-frequency limit of f·H(f) | 1000 | Hz |
| X01.2c | a for continuity | 3 | V |
| X01.3a | capacitor current at t = 0 | 314.2 | mA |
| X01.3b | derivative of ln(1 + x²) at x = 2 | 0.8 | — |
| X01.3c | diode small-signal resistance at 1 mA | 25.85 | Ω |
| X01.3d | capacitor reactance at 1 MHz | 15.92 | Ω |
| X01.4a | optimal load | 50 | Ω |
| X01.4b | maximum load power | 0.5000 | W |
| X01.4c | load power at 100 Ω | 0.4444 | W |
| X01.4d | fraction of maximum at 100 Ω | 88.89 | % |
| X01.4e | load power at 25 Ω | 0.4444 | W |
| X01.4f | loss for a factor-of-2 mismatch | 11.11 | % |
| X01.5l | diode exponential term at V0 | 5.760 | mA |
| X01.5m | resistor current at V0 | 4.300 | mA |
| X01.5a | g(V0) | 1.460 | mA |
| X01.5b | g'(V0) | 0.2238 | S |
| X01.5c | first Newton step | 6.522 | mV |
| X01.5d | V1 | 0.6935 | V |
| X01.5e | second Newton step | 0.97 | mV |
| X01.5f | V2 | 0.69251 | V |
| X01.5n | third Newton step | 0.02 | mV |
| X01.5g | converged V | 0.69249 | V |
| X01.5h | diode current | 4.308 | mA |
| X01.5i | small-signal resistance | 6.001 | Ω |
| X01.5j | linearized rise in V | 0.5965 | mV |
| X01.5k | exact rise in V | 0.590 | mV |
| X01.6a | total charge | 6.000 | µC |
| X01.6b | charge in first 2 ms | 3.793 | µC |
| X01.6c | fraction in first time constant | 63.21 | % |
| X01.7a | integral of x e^x on [0, 1] | 1 | — |
| X01.7b | partial-fraction integral | 0.2877 | — |
| X01.7c | energy dissipated in the resistor | 50.00 | µJ |
| X01.8a | average value | 3.183 | V |
| X01.8f | mean square | 25 | V² |
| X01.8b | RMS value | 5.000 | V |
| X01.8c | average power in 50 Ω | 0.5000 | W |
| X01.8d | wrong power from the average | 0.2026 | W |
| X01.8e | ratio of correct to wrong power | 2.467 | — |
| X01.9a | ADC step | 244.1 | µV |
| X01.9b | RMS quantization error | 70.48 | µV |
| X01.9c | sine RMS | 0.3536 | V |
| X01.9d | SNR, 12 bits | 74.01 | dB |
| X01.9e | dB per bit | 6.021 | dB |
| X01.9f | constant term | 1.761 | dB |
| X01.9g | 12 × 6.021 dB | 72.25 | dB |
| X01.9h | rule-of-thumb SNR | 74.00 | dB |
| X01.10a | third-order estimate of e^0.1 | 1.105167 | — |
| X01.10b | lower edge of error range | 4.167×10^-6 | — |
| X01.10c | Lagrange error bound | 5.0×10^-6 | — |
| X01.10d | actual error | 4.251×10^-6 | — |
| X01.10e | three-term estimate of ln 1.2 | 0.1827 | — |
| X01.10f | ln 1.2 | 0.1823 | — |
| X01.10g | actual error | 3.451×10^-4 | — |
| X01.10h | alternating-series bound | 4.0×10^-4 | — |
| X01.10i | second-harmonic distortion | 2.5 | % |
| X01.11a | first term, 300 mm² | 235.6 | — |
| X01.11b | edge term, 300 mm² | 38.48 | — |
| X01.11c | gross dies, 300 mm² | 197.1 | — |
| X01.11d | first term, 600 mm² | 117.8 | — |
| X01.11e | edge term, 600 mm² | 27.21 | — |
| X01.11f | gross dies, 600 mm² | 90.60 | — |
| X01.11g | gross-die ratio | 2.18 | — |
| X01.11h | yield, 300 mm² | 81.06 | % |
| X01.11i | good dies, 300 mm² | 159.8 | — |
| X01.11j | yield, 600 mm² | 65.70 | % |
| X01.11k | good dies, 600 mm² | 59.53 | — |
| X01.11l | cost per good die, 300 mm² | 106.4 | US$ |
| X01.11m | cost per good die, 600 mm² | 285.6 | US$ |
| X01.11n | cost ratio | 2.68 | — |
| X01.12a | oscillation frequency | 5.033 | MHz |
| X01.12h | square root of LC | 3.162×10^-8 | s |
| X01.12b | sensitivity to L | −0.5 | — |
| X01.12c | sensitivity to C | −0.5 | — |
| X01.12d | worst-case error | 3.5 | % |
| X01.12e | RSS error | 2.693 | % |
| X01.12f | capacitor share of variance | 86.2 | % |
| X01.12g | RSS error with a ±1% capacitor | 1.118 | % |
| X01.13a | optimal I1 | 60 | A |
| X01.13b | optimal I2 | 40 | A |
| X01.13c | minimum loss | 60.00 | W |
| X01.13d | Lagrange multiplier | 1.200 | W/A |
| X01.13e | parallel resistance | 6 | mΩ |
| X01.13f | loss with equal split | 62.50 | W |
| X01.13g | excess loss of equal split | 4.17 | % |
| X01.13h | common voltage drop | 0.6 | V |
| X01.13i | second derivative on the constraint | 0.050 | Ω |
| X01.14a | outer radius b | 1.575 | mm |
| X01.14b | ln(b/a) | 1.253 | — |
| X01.14c | capacitance per meter | 99.92 | pF/m |
| X01.14d | characteristic impedance | 50.1 | Ω |
| X01.14e | charge per meter at 100 V | 9.992 | nC/m |
| X01.14f | peak field at the inner conductor | 177.4 | kV/m |
| X01.15a | wire current | 3.927 | A |
| X01.15b | current with uniform J0 | 7.854 | A |
| X01.15c | B at the surface | 1.571 | mT |
| X01.15d | work from (0, 0) to (1, 2) | 3 | — |
| X01.10j | exact HD2 from Bessel functions | 2.499 | % |
| X01.10k | relative correction a²/24 | 0.04 | % |
| X01.10l | lower bracket 1/21 | 0.04762 | — |
| X01.10m | upper bracket 1/20 | 0.05 | — |
| X01.10n | π²/6 | 1.644934 | — |
| X01.10o | S20 | 1.596163 | — |
| X01.10p | actual error of S20 | 0.04877 | — |
| X01.15e | volume integral of div G | 3 | — |
| X01.15f | total outward flux | 3 | — |
