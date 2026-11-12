# Solutions 01-03 · Derivatives: Rates of Change in Circuits

Problems: [01-03 problems](../problems/01-03-problems.md) · Chapter: [01-03](../chapters/01-03-derivatives.md)

Every numerical answer below is listed in the answer key at the end and is recomputed independently by [verify_01_03.py](../verify/verify_01_03.py).

---

## Solutions

### Solution 01-03.1

(a) $f(1 + h) = 3(1 + 2h + h^2) - (1 + h) = 2 + 5h + 3h^2$, and $f(1) = 2$. So

$$
\frac{f(1 + h) - f(1)}{h} = \frac{5h + 3h^2}{h} = 5 + 3h \;\to\; \mathbf{5}.
$$

Check with the rules: $f'(x) = 6x - 1 = 5$ at $x = 1$ ✓.

(b) $\dfrac{1/(2 + h) - 1/2}{h} = \dfrac{-h}{2h(2 + h)} = \dfrac{-1}{2(2 + h)} \to$ **−0.25**. Check: $-1/x^2 = -1/4$ ✓.

### Solution 01-03.2

(a) $12x^2 - 2$, which is **46** at $x = 2$.
(b) $-2x^{-3}$, which is **−2** at $x = 1$.
(c) $\tfrac{1}{2}x^{-1/2}$, which is $\tfrac{1}{2}\cdot\tfrac{1}{3} = $ **0.1667** at $x = 9$.
(d) $5x^{-3} \to -15x^{-4}$, which is **−15** at $x = 1$.

### Solution 01-03.3

(a) $-3e^{-3t}$, which is **−3** at $t = 0$.
(b) $\ln(5x) = \ln 5 + \ln x$, so the derivative is $1/x$, which is **0.5** at $x = 2$. (The constant factor 5 disappears, as the log law predicts.)
(c) $377\cos(377t)$, which is **377** at $t = 0$ (in 1/s).
(d) $2^x\ln 2$, which is $8\ln 2 = $ **5.545** at $x = 3$.
(e) $\sec^2 x = 1 + \tan^2 x$, which is $1 + 1 = $ **2** at $\pi/4$.

### Solution 01-03.4

(a) Product rule: $2xe^x + x^2e^x = (2x + x^2)e^x$, which is $3e = $ **8.155** at $x = 1$.

(b) Quotient rule: $\dfrac{x\cos x - \sin x}{x^2}$. At $\pi/2$, $\cos = 0$ and $\sin = 1$, so the value is $-1/(\pi/2)^2 = -4/\pi^2 = $ **−0.4053**.

(c) $\dfrac{(1)(x - 1) - (x + 1)(1)}{(x - 1)^2} = \dfrac{-2}{(x - 1)^2}$, which is $-2/4 = $ **−0.5** at $x = 3$.

### Solution 01-03.5

(a) $5(3x + 1)^4\cdot 3 = 15(3x + 1)^4$, which is **15** at $x = 0$.
(b) $\tfrac{1}{2}(1 + x^2)^{-1/2}\cdot 2x = x/\sqrt{1 + x^2}$, which is $1/\sqrt{2} = $ **0.7071** at $x = 1$.
(c) $e^{-t^2}\cdot(-2t)$, which is $-2e^{-1} = $ **−0.7358** at $t = 1$.
(d) $-V_m\omega\sin(\omega t + \phi)$, equivalently $V_m\omega\cos(\omega t + \phi + \pi/2)$.

### Solution 01-03.6

(a) C/s = **A**: current.
(b) A/V = **S** (siemens): a conductance, such as the small-signal conductance of a diode or the transconductance of a transistor.
(c) **V/µs**: an output's rate of change; its maximum is the slew rate.
(d) **rad/s**: an angular frequency. For a sinusoid, $d(\omega t + \phi)/dt = \omega$. A drifting phase gives a frequency offset, which is how phase-locked loops work.
(e) **Ω/K**: a resistor's temperature sensitivity. Divided by $R$, it becomes the temperature coefficient in 1/K (often quoted in ppm/K).

### Solution 01-03.7

(a) $i = C\,dv/dt$ in each interval:

| Interval | $dv/dt$ | $i$ |
|---|---|---|
| 0–2 ms | $10/0.002 = 5000$ V/s | $10^{-5}\times5000 = $ **50 mA** |
| 2–5 ms | 0 | **0** |
| 5–6 ms | $-10/0.001 = -10\,000$ V/s | **−100 mA** |
| after 6 ms | 0 | 0 |

The current is a set of rectangular pulses (Figure 3 of the chapter).

(b) $w = \tfrac{1}{2}Cv^2 = \tfrac{1}{2}(10^{-5})(100) = 5\times10^{-4}$ J $= $ **0.5 mJ**.

(c) At 1 ms, $v = 5$ V and $i = 50$ mA, so $p = $ **0.25 W**. Just before 2 ms, $v \to 10$ V, so $p \to $ **0.5 W**. Check: the energy delivered over the ramp is the average power times the time, $0.25\text{ W}\times2\text{ ms} = 0.5$ mJ, matching (b) ✓.

(d) The voltage is continuous (no infinite current is available). Its *slope* changes abruptly at 2 ms, and the current is proportional to the slope, so the current jumps from 50 mA to 0. A corner in $v$ is a jump in $i$.

### Solution 01-03.8

(a) $\dfrac{d}{dt}V_p\sin\omega t = \omega V_p\cos\omega t$, whose maximum magnitude is $\omega V_p$, reached at the zero crossings. The output can follow only if $\omega V_p \le SR$, i.e. $2\pi fV_p \le SR$, so

$$
f_{max} = \frac{SR}{2\pi V_p}.
$$

(b) $SR = 1\text{ V/µs} = 10^6$ V/s. For 10 V: $10^6/(2\pi\cdot10) = $ **15.92 kHz**. For 1 V: **159.2 kHz**.

(c) $0.3\times10^6/(2\pi\cdot10) = $ **4.775 kHz**. Above that frequency, a large sine is distorted into a triangle wave, because the output can only ramp at the slew rate.

### Solution 01-03.9

(a) $v = L\,di/dt = L\cdot0.5\,\omega\cos\omega t$, with $\omega = 2\pi\cdot50\,000 = 3.1416\times10^5$ rad/s. The amplitude is $10^{-4}\times0.5\times3.1416\times10^5 = $ **15.71 V**. The ratio $V/I = \omega L = $ **31.42 Ω**, the inductive reactance. It grows with frequency, unlike a resistance.

(b) $di/dt = v_L/L = 8.7/4.7\times10^{-6} = 1.851\times10^6$ A/s $= $ **1.851 A/µs**. Over 0.3 µs the current rises by $1.851\times0.3 = $ **0.5553 A**. This peak-to-peak ripple current is a key buck-converter design parameter ([22-02](../../22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md)).

### Solution 01-03.10

(a) Product and chain rules:

$$
\frac{dv}{dt} = 5e^{-200t}\big(-200\sin 1000t + 1000\cos 1000t\big).
$$

At $t = 0$: $dv/dt = 5\times1000 = 5000$ V/s, so $i = 2\times10^{-6}\times5000 = $ **10.00 mA**.

(b) Set $dv/dt = 0$. The exponential is never zero, so $1000\cos 1000t = 200\sin 1000t$, i.e. $\tan 1000t = 5$. The first positive solution is $t_1 = \arctan(5)/1000 = 1.3734\times10^{-3}$ s $= $ **1.373 ms**.

(c) $v(t_1) = 5e^{-0.2747}\sin(1.3734) = 5\times0.7598\times0.9806 = $ **3.725 V**. It is below 5 V for two reasons: the envelope has decayed by $e^{-0.2747}$, and the peak occurs slightly before the undamped peak (where $\sin = 1$ at $1000t = \pi/2$), because the decay pulls the maximum earlier.

### Solution 01-03.11

(a) For $y = kx^n$: $\dfrac{x}{y}\dfrac{dy}{dx} = \dfrac{x}{kx^n}nkx^{n-1} = n$. For a product, $\ln y = \ln f + \ln g$, and differentiating with respect to $\ln x$ adds the elasticities: $S^{y}_{x} = S^{f}_{x} + S^{g}_{x}$.

(b) At fixed $f$: $S^{P}_{V} = $ **2**. With $f \propto V$: $P \propto V^2\cdot V$, so $S = 2 + 1 = $ **3**.

(c) $T = E/P$ gives $S^{T}_{V} = -S^{P}_{V} = -3$. A −1% change in $V$ therefore gives about **+3%** runtime. Exactly: $T_{new}/T = 1/0.99^3 = 1.0306$, a **3.061%** gain. The elasticity is a first-order estimate, accurate for small changes.

(d) $f_c \propto R^{-1}$, so $S^{f_c}_{R} = $ **−1**. A +5% resistor gives about **−5%**. Exactly: $1/1.05 - 1 = $ **−4.762%** for +5%, and $1/0.95 - 1 = $ **+5.263%** for −5%. The asymmetry is second-order, which the elasticity ignores.

### Solution 01-03.12

(a) Differentiate implicitly: $2x + 2y\,y' = 0$, so $y' = -x/y = -3/4 = $ **−0.75**. Check: the radius to $(3, 4)$ has slope 4/3, and a tangent is perpendicular to the radius: $(4/3)(-3/4) = -1$ ✓.

(b) $1/(1 + x^2) = $ **0.5** at $x = 1$.

(c) $dV/dI = V_T\cdot\dfrac{1}{I/I_s}\cdot\dfrac{1}{I_s} = \dfrac{V_T}{I}$. At 1 mA: **25.85 Ω**. At 10 mA: **2.585 Ω**. This is the reciprocal of $g_d = I/V_T$, as it must be. The derivative of an inverse function is the reciprocal of the original derivative: $dV/dI = 1/(dI/dV)$.

### Solution 01-03.13

(a) $\cos 1 = 0.540302$.

| Method | $h$ | Estimate | Error |
|---|---|---|---|
| Central | 0.1 | **0.539402** | $-9.0\times10^{-4}$ |
| Central | 0.01 | **0.540293** | $-9.0\times10^{-6}$ |
| Forward | 0.1 | **0.497364** | $-4.29\times10^{-2}$ |

The central error falls 100× when $h$ falls 10× (second order). At the same $h = 0.1$, the forward difference is about 48 times worse.

(b) $-\tfrac{h^2}{6}\cos 1 = -\tfrac{0.01}{6}\times0.5403 = $ **−9.005×10^−4**, matching the observed $-9.0005\times10^{-4}$ ✓.

(c) $h^3 = 3\epsilon_{\text{mach}} = 6.66\times10^{-16}$, so $h = $ **8.7×10^−6**. At that step both error terms are about $10^{-11}$, giving roughly 10–11 correct digits, against about 8 for the forward difference.

### Solution 01-03.14

(a) For $x < 0$, ReLU $= 0$, with slope **0**. For $x > 0$, ReLU $= x$, with slope **1**. At 0 the left and right difference quotients are 0 and 1, so there is a corner and no derivative.

(b) Chain rule: $s'(x) = \dfrac{e^x}{1 + e^x} = \dfrac{1}{e^{-x} + 1}$.

(c) $s(0) = \ln 2 = $ **0.6931**; $s'(0) = 1/2 = $ **0.5**; $s(5) = \ln(1 + e^5) = $ **5.007**; $s'(5) = $ **0.9933**. Softplus exceeds ReLU by **0.6931** at 0 and by only **0.0067** at 5. Far from the corner, the two agree; near it, softplus rounds it off.

(d) Where ReLU's derivative is 0, small weight changes produce no change in output, so training stops updating that neuron (a "dead" unit). Smooth variants (softplus) or leaky variants (slope 0.01 instead of 0 for $x < 0$) keep a nonzero derivative, so gradients keep flowing.

(e) The thermal voltage $V_T$ sets the smoothing scale. The diode's current changes by a factor $e$ for every $V_T$ (about 26 mV), so over a few tens of millivolts the "corner" is smooth. Softplus with a scale parameter, $V_T\ln(1 + e^{V/V_T})$, has the same structure.

### Solution 01-03.15

(a) $i = C\,dv/dt = 10^{-6}\times170\times377\cos(377t) = 0.06409\cos(377t)$ A, an amplitude of **64.09 mA**. Then

$$
p(t) = 170\times0.06409\,\sin(377t)\cos(377t) = \tfrac{1}{2}(10.90)\sin(754t)\ \text{W}.
$$

It oscillates at $2\times60 = 120$ Hz and averages zero over each cycle.

(b) The peak is $\tfrac{1}{2}CV_m^2\omega = \tfrac{1}{2}(10^{-6})(170^2)(377) = $ **5.448 W**.

(c) $\dfrac{d}{dt}\tfrac{1}{2}Cv^2 = Cv\dfrac{dv}{dt} = v\cdot i = p$ ✓ (chain rule).

(d) $Q = V_{rms}^2\omega C = (170/\sqrt{2})^2\times377\times10^{-6} = \tfrac{1}{2}V_m^2\omega C$, the same expression as the peak power: **5.448 var**. Energy sloshes into the capacitor for a quarter cycle and back out the next. Current flows (and heats the wires and the source), but no net energy is consumed. Utilities care about this because the circulating current costs real losses in the grid; power-factor correction manages it ([07-06](../../07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md)).

### Solution 01-03.16

(a) Write $\text{SNR} = 10^{x/10}$ with $x = \text{SNR}_{\text{dB}}$, so $d\,\text{SNR}/dx = \text{SNR}\cdot\ln 10/10$. Also $dC/d\,\text{SNR} = B/\big((1 + \text{SNR})\ln 2\big)$. By the chain rule,

$$
\frac{dC}{dx} = \frac{B}{(1 + \text{SNR})\ln 2}\cdot\frac{\ln 10}{10}\text{SNR}.
$$

(b) $B\ln 10/(10\ln 2) = 20\times10^6\times0.33219 = 6.644$ Mb/s per dB, multiplied by $\text{SNR}/(1 + \text{SNR})$:

- at 30 dB (SNR = 1000): **6.637 Mb/s per dB**;
- at 0 dB (SNR = 1): **3.322 Mb/s per dB**.

(c) Exact: $C(31\text{ dB}) - C(30\text{ dB}) = 20\times10^6\big[\log_2(1 + 10^{3.1}) - \log_2 1001\big] = $ **6.638 Mb/s**. The derivative predicts 6.637, so it is excellent here, because at high SNR the capacity is almost exactly linear in dB.

(d) At high SNR each dB, a 26% increase in power, adds only about $B/3$ bits per second: 6.6 Mb/s, about 3% of this 200 Mb/s link. Doubling power (+3 dB) adds about $B$ bits per second, while doubling bandwidth doubles the capacity. Bandwidth is the stronger lever at high SNR, which is why spectrum is so valuable.

### Solution 01-03.17

(a) $\ln y = x\ln x$, so $y'/y = \ln x + 1$ and $y' = x^x(1 + \ln x)$. At $x = 2$: $4(1 + 0.6931) = $ **6.773**.

(b) $(\tanh x)' = 1 - \tanh^2x$. At 0.5, $\tanh 0.5 = 0.4621$, so the derivative is $1 - 0.2135 = $ **0.7864**.

(c) By the chain rule, $g_m = \dfrac{I_{EE}}{2V_T}\left[1 - \tanh^2\!\left(\dfrac{v_{id}}{2V_T}\right)\right]$. At $v_{id} = 0$: $g_m = I_{EE}/(2V_T) = 1\text{ mA}/51.7\text{ mV} = $ **19.34 mS**. Units: A/V = S ✓.

(d) We need $1 - \tanh^2u = 1/\cosh^2u = \tfrac12$, so $\cosh u = \sqrt2$ and $u = \operatorname{arccosh}\sqrt2 = $ **0.8814**. Then $v_{id} = 2V_Tu = $ **45.57 mV**. The pair is linear only for inputs of a few tens of millivolts; beyond about ±45 mV its gain has halved and it acts as a current switch. That is why a bipolar differential pair makes a good limiter and needs emitter degeneration for linearity ([12](../../12-electronics-2/README.md)).

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 01-03.1a | f'(1) | 5 | — |
| 01-03.1b | g'(2) | −0.25 | — |
| 01-03.2a | (a) | 46 | — |
| 01-03.2b | (b) | −2 | — |
| 01-03.2c | (c) | 0.1667 | — |
| 01-03.2d | (d) | −15 | — |
| 01-03.3a | (a) | −3 | — |
| 01-03.3b | (b) | 0.5 | — |
| 01-03.3c | (c) | 377 | 1/s |
| 01-03.3d | (d) | 5.545 | — |
| 01-03.3e | (e) | 2 | — |
| 01-03.4a | (a) | 8.155 | — |
| 01-03.4b | (b) | −0.4053 | — |
| 01-03.4c | (c) | −0.5 | — |
| 01-03.5a | (a) | 15 | — |
| 01-03.5b | (b) | 0.7071 | — |
| 01-03.5c | (c) | −0.7358 | — |
| 01-03.7a | current, 0–2 ms | 50 | mA |
| 01-03.7b | current, 5–6 ms | −100 | mA |
| 01-03.7c | peak stored energy | 0.5 | mJ |
| 01-03.7d | power at 1 ms | 0.25 | W |
| 01-03.7e | power just before 2 ms | 0.5 | W |
| 01-03.8a | f_max, 1 V/µs, 10 V | 15.92 | kHz |
| 01-03.8b | f_max, 1 V/µs, 1 V | 159.2 | kHz |
| 01-03.8c | f_max, 0.3 V/µs, 10 V | 4.775 | kHz |
| 01-03.9a | inductor voltage amplitude | 15.71 | V |
| 01-03.9b | reactance | 31.42 | Ω |
| 01-03.9c | di/dt | 1.851 | A/µs |
| 01-03.9d | ripple current | 0.5553 | A |
| 01-03.10a | i(0) | 10.00 | mA |
| 01-03.10b | t1 | 1.373 | ms |
| 01-03.10c | v(t1) | 3.725 | V |
| 01-03.11a | runtime gain, exact | 3.061 | % |
| 01-03.11b | corner change for +5 % R | −4.762 | % |
| 01-03.11c | corner change for −5 % R | 5.263 | % |
| 01-03.11d | voltage elasticity at fixed f | 2 | — |
| 01-03.11e | voltage elasticity with f ∝ V | 3 | — |
| 01-03.11f | runtime elasticity | −3 | — |
| 01-03.11g | runtime gain, first order | 3 | % |
| 01-03.11h | corner elasticity to R | −1 | — |
| 01-03.11i | corner change for +5 % R, first order | −5 | % |
| 01-03.12a | slope of circle at (3, 4) | −0.75 | — |
| 01-03.12b | d/dx arctan x at 1 | 0.5 | — |
| 01-03.12c | r at 1 mA | 25.85 | Ω |
| 01-03.12d | r at 10 mA | 2.585 | Ω |
| 01-03.13a | central, h = 0.1 | 0.539402 | — |
| 01-03.13b | central, h = 0.01 | 0.540293 | — |
| 01-03.13c | forward, h = 0.1 | 0.497364 | — |
| 01-03.13d | predicted central error, h = 0.1 | −9.005×10^-4 | — |
| 01-03.13e | best central step | 8.7×10^-6 | — |
| 01-03.14a | s(0) | 0.6931 | — |
| 01-03.14b | s'(0) | 0.5 | — |
| 01-03.14c | s(5) | 5.007 | — |
| 01-03.14d | s'(5) | 0.9933 | — |
| 01-03.14e | softplus − ReLU at 5 | 0.0067 | — |
| 01-03.15a | current amplitude | 64.09 | mA |
| 01-03.15b | peak instantaneous power | 5.448 | W |
| 01-03.15c | reactive power | 5.448 | var |
| 01-03.16a | dC/dSNR_dB at 30 dB | 6.637 | Mb/s per dB |
| 01-03.16b | dC/dSNR_dB at 0 dB | 3.322 | Mb/s per dB |
| 01-03.16c | exact gain 30 → 31 dB | 6.638 | Mb/s |
| 01-03.17a | derivative of x^x at 2 | 6.773 | — |
| 01-03.17b | tanh 0.5 | 0.4621 | — |
| 01-03.17c | derivative of tanh at 0.5 | 0.7864 | — |
| 01-03.17d | differential-pair g_m at 0 | 19.34 | mS |
| 01-03.17e | 2V_T | 51.7 | mV |
| 01-03.17f | arccosh √2 | 0.8814 | — |
| 01-03.17g | input for half g_m | 45.57 | mV |
