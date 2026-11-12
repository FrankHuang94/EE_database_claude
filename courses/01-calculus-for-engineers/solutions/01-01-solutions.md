# Solutions 01-01 · Functions, Models and Units

Problems: [01-01 problems](../problems/01-01-problems.md) · Chapter: [01-01](../chapters/01-01-functions-models-and-units.md)

Every numerical answer below is listed in the answer key at the end and is recomputed independently by [verify_01_01.py](../verify/verify_01_01.py).

---

## Solutions

### Solution 01-01.1

(a) $V$ increases with $T$, so its extremes occur at the ends of the temperature range: $V(-40) = 0.5 + 0.01(-40) = 0.100$ V and $V(125) = 0.5 + 0.01(125) = 1.750$ V. **Range: 0.100 V to 1.750 V.**

(b) Substitute $V(T)$ into $N(V)$:

$$
N(T) = \frac{4096}{3.3\text{ V}}\Big(0.5\text{ V} + (0.01\text{ V/°C})\,T\Big).
$$

At 25 °C, $V = 0.75$ V and $N = 4096 \times 0.75/3.3 = $ **930.9**.

(c) The slope is the product of the two slopes: $(4096/3.3\text{ V}) \times 0.01\text{ V/°C} = $ **12.41 codes/°C**. Units check: (codes/V)(V/°C) = codes/°C ✓.

(d) Invert each stage in reverse order: $V = 3.3N/4096$, then $T = (V - 0.5)/0.01$, so

$$
T(N) = \frac{3.3N/4096 - 0.5}{0.01}\ \text{°C}.
$$

For $N = 1500$: $V = 1.2085$ V and $T = $ **70.85 °C**.

(e) $N$ is increasing in $T$, so the codes run from $N(-40) = 4096(0.1)/3.3 = $ **124.1** to $N(125) = 4096(1.75)/3.3 = $ **2172**. Only about half the ADC's 4096 codes are ever used, a design choice you could improve by matching the sensor's range to the ADC's.

### Solution 01-01.2

The rule: arguments of $\exp$, $\ln$, $\sin$ and $\cos$ must be dimensionless (chapter §3.9).

(a) **Valid.** $RC$ has units Ω·F = (V/A)(C/V) = C/A = s, so $t/(RC)$ is dimensionless.
(b) **Invalid.** Write $\ln(V/1\text{ V})$, or better, the log of a ratio of two voltages.
(c) **Valid.** $f t$ is (1/s)(s), dimensionless.
(d) **Invalid.** $2\pi f$ has units of 1/s. Probably $\cos(2\pi f t)$ was meant.
(e) **Valid.** $L/R$ has units H/Ω = (V·s/A)/(V/A) = s, so $Rt/L$ is dimensionless.
(f) **Valid.** The reference 1 mW makes the ratio dimensionless; this is the definition of dBm.
(g) **Valid.** A voltage over a voltage.
(h) **Each term alone is invalid, but the difference is fine**, because $\ln I_1 - \ln I_2 = \ln(I_1/I_2)$. Any unit chosen for the currents cancels. This is why you often see $\ln I$ in physics texts: an implied reference that cancels in the end. Write the ratio explicitly to stay safe.

### Solution 01-01.3

(a) Add exponents: $3 - 5 - (-2) = 0$, so the value is $e^0 = $ **1**.
(b) $\ln(e^4 \cdot e^{1/2}) = 4 + 1/2 = $ **4.5**.
(c) $0.001 = 10^{-3}$, so $\log_{10}0.001 = $ **−3**.
(d) $1024 = 2^{10}$, so $\log_2 1024 = $ **10**.
(e) $\ln\!\big(20 \times \tfrac{1}{5} \times \tfrac{1}{4}\big) = \ln 1 = $ **0**.
(f) $\log_2 10 = \ln 10/\ln 2 = 2.3026/0.6931 = $ **3.322**. Equivalently, $1/\log_{10}2 = 1/0.30103$.
(g) $\sqrt[3]{e^2} = e^{2/3}$, so the log is $2/3 = $ **0.6667**.

### Solution 01-01.4

(a) Divide by 5: $e^{-t/3\text{ ms}} = 0.2$. Take $\ln$: $-t/(3\text{ ms}) = \ln 0.2 = -\ln 5$. So $t = 3\ln 5$ ms $= $ **4.828 ms**.

(b) Take $\ln$: $x\ln 2 = \ln 50$, so $x = \ln 50/\ln 2 = 3.912/0.6931 = $ **5.644**. Check: $2^{5.644}$ lies between $2^5 = 32$ and $2^6 = 64$ ✓.

(c) Take $\log_{10}$: $x/10 = \log_{10}0.25 = -0.6021$, so $x = $ **−6.021**. This is just "a quarter of the power is −6.02 dB".

(d) $1.5 = 4.0e^{-10\,\mu\text{s}/\tau}$, so $10\text{ µs}/\tau = \ln(4.0/1.5) = 0.9808$, giving $\tau = $ **10.20 µs**. Sanity check: the voltage fell to 37.5% of its start, close to the 36.8% reached at one time constant, so $\tau$ should be just over 10 µs ✓.

### Solution 01-01.5

(a) $10\log_{10}2 = $ **3.010 dB**; $10\log_{10}0.01 = 10(-2) = $ **−20 dB**; $10\log_{10}1000 = $ **30 dB**; $10\log_{10}0.5 = $ **−3.010 dB**.

(b) $10^{13/10} = 10^{1.3} = $ **19.95** (about 20, since 13 dB = 10 dB + 3 dB means 10 × 2); $10^{-7/10} = $ **0.1995** (−7 dB = −10 dB + 3 dB means 0.1 × 2).

(c) An amplitude ratio uses $20\log_{10}$: $20\log_{10}0.5 = $ **−6.021 dB**. A voltage gain of 46 dB is $10^{46/20} = 10^{2.3} = $ **199.5**.

(d) $10^{100/20} = 10^5 = $ **100 000**.

### Solution 01-01.6

(a) Divide by 1 mW, then take $10\log_{10}$:

- 100 mW → $10\log_{10}100 = $ **20 dBm**;
- 1 µW = $10^{-3}$ mW → **−30 dBm**;
- 2 W = 2000 mW → $10\log_{10}2000 = 30 + 3.010 = $ **33.01 dBm**;
- 0.25 mW → $10\log_{10}0.25 = $ **−6.021 dBm**.

(b) Invert: $P = 1\text{ mW}\times10^{P_{\text{dBm}}/10}$.

- −90 dBm → $10^{-9}$ mW $= 10^{-12}$ W $= $ **1.000 pW**;
- 17 dBm → $10^{1.7} = $ **50.12 mW**.

(c) 0 dBm is 1 mW. For a sinusoid into a resistance, $P = V_{rms}^2/R$, so $V_{rms} = \sqrt{PR} = \sqrt{10^{-3}\times 50} = $ **0.2236 V**. The peak is $\sqrt{2}V_{rms} = $ **0.3162 V**.

(d) $20\log_{10}(0.2236/1) = $ **−13.01 dBV**. (Amplitude, so 20 log.)

### Solution 01-01.7

(a) $\omega = 2000\pi$ rad/s, so $f = \omega/(2\pi) = $ **1000 Hz** and $T = $ **1.000 ms**.

(b) $-0.7\text{ rad}\times(180^\circ/\pi) = $ **−40.11°**.

(c) $I_{rms} = 0.5/\sqrt{2} = $ **0.3536 mA**.

(d) At $t = 10^{-4}$ s the argument is $2000\pi \times 10^{-4} - 0.7 = 0.6283 - 0.7 = -0.0717$ rad, so $i = 0.5\cos(-0.0717) = $ **0.4987 mA**, just before the peak.

(e) Peaks occur where the argument is $2\pi k$. The first with $t > 0$ is $k = 0$: $2000\pi t = 0.7$, giving $t = 0.7/(2000\pi) = $ **0.1114 ms**. (The phase is negative, so the waveform *lags*; its peak comes after $t = 0$.)

### Solution 01-01.8

(a) $\tau = RC = 10^4 \times 10^{-7} = 10^{-3}$ s $= $ **1.000 ms**.

(b) Solve $v = 5(1 - e^{-t/\tau})$ for $t$: $e^{-t/\tau} = 1 - v/5$, so $t = \tau\ln\big(5/(5 - v)\big)$.

- $v = 2.5$ V: $t = \tau\ln 2 = $ **0.6931 ms**.
- $v = 4.5$ V: $t = \tau\ln 10 = $ **2.303 ms**.

(c) The time to reach a fraction $x$ of the final value is $t_x = \tau\ln\big(1/(1 - x)\big)$. So $t_{0.9} = \tau\ln 10$ and $t_{0.1} = \tau\ln(1/0.9)$, and

$$
t_{0.9} - t_{0.1} = \tau\left[\ln 10 - \ln\frac{10}{9}\right] = \tau\ln 9 .
$$

Evaluated: **2.197 ms**. The often-quoted "rise time ≈ 2.2τ" comes from exactly this.

(d) $v(3\text{ ms}) = 5(1 - e^{-3}) = 5(0.9502) = $ **4.751 V** (95% of final after 3τ).

(e) $x = 0.7$: $t = \tau\ln(1/0.3) = $ **1.204 ms**.

### Solution 01-01.9

(a) $V_T = kT/q$, then multiply by $\ln 10 = 2.3026$:

| $T$ (K) | $V_T$ (mV) | mV per decade |
|---|---|---|
| 250 | **21.54** | **49.61** |
| 300 | **25.85** | **59.53** |
| 400 | **34.47** | **79.37** |

The slope is proportional to absolute temperature.

(b) Each decade of current costs $V_T\ln 10 = 59.53$ mV at 300 K. 10 µA is two decades below 1 mA: $V = 0.650 - 2(0.05953) = $ **0.5309 V**. 100 mA is two decades above: $V = 0.650 + 0.1191 = $ **0.7691 V**.

(c) Take the ratio of the diode law at two voltages: $I_2/I_1 = e^{(V_2 - V_1)/V_T}$. So $I = 1\text{ mA}\times e^{0.05/0.025852} = 1\text{ mA}\times e^{1.934} = $ **6.918 mA**.

(d) A real diode has series resistance in its silicon and contacts. At 100 mA even 1 Ω drops another 0.1 V, so the measured voltage exceeds the ideal-law value. At high current the semilog I–V curve bends away from a straight line.

### Solution 01-01.10

(a) Add dB gains and losses to dBm levels:

$$
P_r = 20 - 2 + 3 - 80 + 3 = -56\ \text{dBm}.
$$

In watts: $10^{-56/10}$ mW $= 2.512\times10^{-6}$ mW $= $ **2.512×10^−9 W** (2.5 nW).

(b) Margin $= -56 - (-90) = $ **34 dB**.

(c) At 20 dB per decade of distance, 34 dB of margin buys $10^{34/20} = $ **50.12×** the distance.

(d) Doubling the power adds $10\log_{10}2 = $ **3.010 dB**. Range grows by $10^{3.010/20} = \sqrt{2} = $ **1.414×**. Doubling transmit power only gets you 41% more range in free space, a classic Marketing-vs-Reality trap.

### Solution 01-01.11

(a) Convert to radians, take the sine (which is what the firmware computes), and convert back. The relative error is $1 - \sin\theta/\theta$.

| True tilt | $\hat\theta$ | Relative error |
|---|---|---|
| 5° | **4.994°** | **0.1269%** |
| 15° | **14.83°** | **1.138%** |
| 30° | **28.65°** | **4.507%** |

The error grows roughly as $\theta^2$: tripling the angle from 5° to 15° raises it about 9×.

(b) With $\sin\theta \approx \theta - \theta^3/6$, the relative error is $1 - \sin\theta/\theta \approx \theta^2/6$. Setting $\theta^2/6 = 0.01$ gives $\theta = \sqrt{0.06} = 0.2449$ rad $= $ **14.03°**. Solving $\sin\theta/\theta = 0.99$ numerically (for example with `scipy.optimize.brentq`) gives $\theta = 0.2453$ rad $= $ **14.06°**. The closed form is accurate to 0.03°, because the next series term is tiny ([01-08](../chapters/01-08-sequences-series-and-taylor.md)). Above about 14° the firmware should use $\arcsin$.

### Solution 01-01.12

(a) $P \propto V^2$ at fixed $f$: $P = 1.5(0.8/1.0)^2 = 1.5 \times 0.64 = $ **0.96 W**.

(b) $P \propto V^2f$: $P = 1.5 \times 0.64 \times (1.6/2.0) = 1.5 \times 0.512 = $ **0.768 W**.

(c) Energy per cycle $= P/f$:

- nominal: $1.5/(2\times10^9) = $ **0.75 nJ**;
- DVFS: $0.768/(1.6\times10^9) = $ **0.48 nJ**.

This equals $\alpha CV^2$ and depends only on voltage: $0.48/0.75 = 0.64 = 0.8^2$.

(d) Time $= $ cycles$/f$; energy $= P\times$ time $=$ cycles × energy per cycle.

- Nominal: $3\times10^9/2\times10^9 = $ **1.5 s**, energy **2.25 J**.
- DVFS: $3\times10^9/1.6\times10^9 = $ **1.875 s**, energy **1.44 J**.

(e) Leakage adds $0.2\text{ W}\times$ time:

- Nominal: $(1.5 + 0.2)(1.5) = $ **2.55 J**.
- DVFS: $(0.768 + 0.2)(1.875) = $ **1.815 J**.

The saving is $1 - 1.815/2.55 = $ **28.8%**, against **36.0%** without leakage. Running slower keeps the chip on longer, and leakage is charged by the second. When leakage is a large share of total power, the best strategy can flip to "race to idle": run fast, then power down. [19-06](../../19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md) returns to this. (We held leakage constant for simplicity; in reality it also falls at lower voltage.)

### Solution 01-01.13

(a) Take $\ln$: $\ln v = \ln v_0 - t/\tau$. Against $t$ this is a line with **slope $-1/\tau$** and **intercept $\ln v_0$**.

(b) The transformed data $\ln v$ are 1.386, 0.7198, 0.0526, −0.6143, −1.280. A least-squares line fit (for example `numpy.polyfit(t, np.log(v), 1)`) gives slope −0.6667 per ms and intercept 1.386. So $\tau = 1/0.6667 = $ **1.50 ms** and $v_0 = e^{1.386} = $ **4.00 V**.

(c) $\tau = (4 - 0)\text{ ms}/\ln(4.000/0.278) = 4/2.667 = $ **1.500 ms**. With noise-free data the two-point estimate agrees with the fit. With noisy data the fit is better because it uses all the points.

(d) $v(6\text{ ms}) = 4.00\,e^{-6/1.50} = 4e^{-4} = $ **0.0733 V**.

### Solution 01-01.14

(a) Take $10\log_{10}$ of $P_r(d)/1\text{ mW}$:

$$
P_{r,\text{dBm}} = 10\log_{10}\frac{P_r(1\text{ m})}{1\text{ mW}} - 10n\log_{10}d .
$$

So $A$ is the received power at 1 m, in dBm, and the slope against $\log_{10}d$ is $-10n$.

(b) With $x = \log_{10}d = 0, 0.301, 0.699, 1, 1.301$, a least-squares fit of $P_r$ against $x$ gives slope −29.99 dB per decade and intercept −40.00 dBm. So $n = $ **3.0** and $A = $ **−40.0 dBm**.

(c) Solve $-40 - 30\log_{10}d = -90$: $\log_{10}d = 50/30$, so $d = 10^{1.667} = $ **46.4 m**.

(d) With $n = 2$: $\log_{10}d = 50/20$, so $d = 10^{2.5} = $ **316 m**. The same radio reaches about 7× less far indoors than a free-space calculation suggests. A range claim made "in free space" or "line of sight" says little about a home or factory.

(e) The data stop at 20 m. Beyond it the environment may change (more walls, other floors, outdoors), and $n$ itself depends on the building. Extrapolating a log–log fit by a factor of 10 beyond the data is exactly the mistake in chapter §8, item 7.

### Solution 01-01.15

(a) The annual factor $a$ satisfies $a^2 = 2$, so $a = \sqrt{2} = $ **1.414**, i.e. **41.42%** per year.

(b) $e^{2r} = 2$, so $r = \ln 2/2 = $ **0.3466 per year**. The time constant is $\tau = 1/r = $ **2.885 years**. The doubling time is $\tau\ln 2$, exactly the half-life formula of chapter §3.4 run forward.

(c) Ten years is five doublings: $2^5 = $ **32**.

(d) $(1 + g)^t = 2$ gives $t = \ln 2/\ln(1 + g)$. For small $g$, $\ln(1 + g) \approx g$ (the first term of its Taylor series, [01-08](../chapters/01-08-sequences-series-and-taylor.md)). So $t \approx 0.693/g = 69.3/(100g)$, rounded up to 70 for easy mental arithmetic.

(e) For 41.42%: the rule gives $70/41.42 = $ **1.690 years** against the exact 2.000 years, a 15% error. For 7%: it gives $70/7 = $ **10.00 years** against the exact $\ln 2/\ln 1.07 = $ **10.24 years**, a 2% error. The approximation $\ln(1 + g) \approx g$ is good only when $g \ll 1$. At $g = 0.414$, $\ln 1.414 = 0.347$ is far from 0.414. The same lesson holds throughout this course: linear approximations are local.

### Solution 01-01.16

(a) $\cosh 1 = (e + e^{-1})/2 = (2.71828 + 0.36788)/2 = $ **1.5431** and $\sinh 1 = (e - e^{-1})/2 = $ **1.1752**. Squaring the unrounded values, $\cosh^2 1 = 2.38110$ and $\sinh^2 1 = 1.38110$, whose difference is 1 ✓.

(b) Multiply the top and bottom of $\tanh x = \dfrac{e^x - e^{-x}}{e^x + e^{-x}}$ by $e^{-x}$: $\tanh x = \dfrac{1 - e^{-2x}}{1 + e^{-2x}}$. For large $x$, $u = e^{-2x}$ is small, and $\dfrac{1 - u}{1 + u} = (1 - u)(1 - u + u^2 - \cdots) = 1 - 2u + 2u^2 - \cdots$, so $\tanh x \approx 1 - 2e^{-2x}$.

(c) Exactly, $\tanh 3 = (1 - e^{-6})/(1 + e^{-6}) = $ **0.99505**. The approximation gives $1 - 2e^{-6} = $ **0.99504**. $\tanh 3$ is within $4.95\times10^{-3}$ (0.5%) of 1, which is why "tanh saturates beyond about 3" is a good rule.

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 01-01.1a | minimum sensor voltage | 0.100 | V |
| 01-01.1b | maximum sensor voltage | 1.750 | V |
| 01-01.1c | code at 25 °C | 930.9 | — |
| 01-01.1d | slope of N(T) | 12.41 | codes/°C |
| 01-01.1e | temperature at code 1500 | 70.85 | °C |
| 01-01.1f | minimum code | 124.1 | — |
| 01-01.1g | maximum code | 2172 | — |
| 01-01.3a | (a) | 1 | — |
| 01-01.3b | (b) | 4.5 | — |
| 01-01.3c | (c) | −3 | — |
| 01-01.3d | (d) | 10 | — |
| 01-01.3e | (e) | 0 | — |
| 01-01.3f | log2 10 | 3.322 | — |
| 01-01.3g | (g) | 0.6667 | — |
| 01-01.4a | t | 4.828 | ms |
| 01-01.4b | x | 5.644 | — |
| 01-01.4c | x | −6.021 | — |
| 01-01.4d | τ | 10.20 | µs |
| 01-01.5a | 2 in dB | 3.010 | dB |
| 01-01.5b | 0.01 in dB | −20 | dB |
| 01-01.5c | 1000 in dB | 30 | dB |
| 01-01.5d | 0.5 in dB | −3.010 | dB |
| 01-01.5e | 13 dB as ratio | 19.95 | — |
| 01-01.5f | −7 dB as ratio | 0.1995 | — |
| 01-01.5g | amplitude 0.5 in dB | −6.021 | dB |
| 01-01.5h | 46 dB voltage gain | 199.5 | — |
| 01-01.5i | 100 dB voltage gain | 100000 | — |
| 01-01.6a | 100 mW | 20 | dBm |
| 01-01.6b | 1 µW | −30 | dBm |
| 01-01.6c | 2 W | 33.01 | dBm |
| 01-01.6d | 0.25 mW | −6.021 | dBm |
| 01-01.6e | −90 dBm | 1.000 | pW |
| 01-01.6f | 17 dBm | 50.12 | mW |
| 01-01.6g | RMS voltage at 0 dBm, 50 Ω | 0.2236 | V |
| 01-01.6h | peak voltage | 0.3162 | V |
| 01-01.6i | RMS voltage in dBV | −13.01 | dBV |
| 01-01.7a | frequency | 1000 | Hz |
| 01-01.7b | period | 1.000 | ms |
| 01-01.7c | phase | −40.11 | ° |
| 01-01.7d | RMS current | 0.3536 | mA |
| 01-01.7e | i(0.1 ms) | 0.4987 | mA |
| 01-01.7f | first peak | 0.1114 | ms |
| 01-01.8a | τ | 1.000 | ms |
| 01-01.8b | time to 2.5 V | 0.6931 | ms |
| 01-01.8c | time to 4.5 V | 2.303 | ms |
| 01-01.8d | 10–90 % rise time | 2.197 | ms |
| 01-01.8e | v(3 ms) | 4.751 | V |
| 01-01.8f | time to 70 % | 1.204 | ms |
| 01-01.9a | V_T at 250 K | 21.54 | mV |
| 01-01.9b | V_T at 300 K | 25.85 | mV |
| 01-01.9c | V_T at 400 K | 34.47 | mV |
| 01-01.9d | per decade at 250 K | 49.61 | mV |
| 01-01.9e | per decade at 300 K | 59.53 | mV |
| 01-01.9f | per decade at 400 K | 79.37 | mV |
| 01-01.9g | voltage for 10 µA | 0.5309 | V |
| 01-01.9h | voltage for 100 mA | 0.7691 | V |
| 01-01.9i | current at 0.700 V | 6.918 | mA |
| 01-01.10a | received power | −56 | dBm |
| 01-01.10b | received power | 2.512×10^−9 | W |
| 01-01.10c | link margin | 34 | dB |
| 01-01.10d | distance factor | 50.12 | — |
| 01-01.10e | margin gain from 2× power | 3.010 | dB |
| 01-01.10f | range factor from 2× power | 1.414 | — |
| 01-01.11a | estimate at 5° | 4.994 | ° |
| 01-01.11b | error at 5° | 0.1269 | % |
| 01-01.11c | estimate at 15° | 14.83 | ° |
| 01-01.11d | error at 15° | 1.138 | % |
| 01-01.11e | estimate at 30° | 28.65 | ° |
| 01-01.11f | error at 30° | 4.507 | % |
| 01-01.11g | 1 % limit, series estimate | 14.03 | ° |
| 01-01.11h | 1 % limit, exact | 14.06 | ° |
| 01-01.12a | power at 0.8 V, 2 GHz | 0.96 | W |
| 01-01.12b | power at 0.8 V, 1.6 GHz | 0.768 | W |
| 01-01.12c | energy per cycle, nominal | 0.75 | nJ |
| 01-01.12d | energy per cycle, DVFS | 0.48 | nJ |
| 01-01.12e | task time, nominal | 1.5 | s |
| 01-01.12f | task energy, nominal | 2.25 | J |
| 01-01.12g | task time, DVFS | 1.875 | s |
| 01-01.12h | task energy, DVFS | 1.44 | J |
| 01-01.12i | energy with leakage, nominal | 2.55 | J |
| 01-01.12j | energy with leakage, DVFS | 1.815 | J |
| 01-01.12k | saving with leakage | 28.8 | % |
| 01-01.12l | saving without leakage | 36.0 | % |
| 01-01.13a | fitted τ | 1.50 | ms |
| 01-01.13b | fitted v0 | 4.00 | V |
| 01-01.13c | two-point τ | 1.500 | ms |
| 01-01.13d | v(6 ms) | 0.0733 | V |
| 01-01.14a | path-loss exponent n | 3.0 | — |
| 01-01.14b | A | −40.0 | dBm |
| 01-01.14c | indoor range at −90 dBm | 46.4 | m |
| 01-01.14d | free-space range | 316 | m |
| 01-01.15a | annual growth factor | 1.414 | — |
| 01-01.15b | annual growth | 41.42 | % |
| 01-01.15c | continuous rate r | 0.3466 | 1/yr |
| 01-01.15d | time constant | 2.885 | yr |
| 01-01.15e | 10-year factor | 32 | — |
| 01-01.15f | rule of 70 at 41.42 % | 1.690 | yr |
| 01-01.15g | rule of 70 at 7 % | 10.00 | yr |
| 01-01.15h | exact doubling at 7 % | 10.24 | yr |
| 01-01.16a | cosh 1 | 1.5431 | — |
| 01-01.16b | sinh 1 | 1.1752 | — |
| 01-01.16c | cosh² 1 | 2.38110 | — |
| 01-01.16d | sinh² 1 | 1.38110 | — |
| 01-01.16e | tanh 3 | 0.99505 | — |
| 01-01.16f | 1 − 2e^−6 | 0.99504 | — |
| 01-01.16g | 1 − tanh 3 | 4.95×10^-3 | — |
