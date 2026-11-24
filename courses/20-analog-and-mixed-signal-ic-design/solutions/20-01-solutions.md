# Solutions 20-01 · Analog Design Fundamentals in Nanometer CMOS

Problems: [20-01 problem set](../problems/20-01-problems.md) · Chapter: [20-01](../chapters/20-01-analog-design-fundamentals-gm-id.md). Every number below is recomputed by [verify_20_01.py](../verify/verify_20_01.py).

---

## Solutions

### Solution 20-01.1

$I_{spec} = I_{spec,\square}\,W/L = 0.523 \times 5$ = **2.615** µA.

| $I_D$ | $IC = I_D/I_{spec}$ | Region | $q = (\sqrt{1 + 4IC} - 1)/2$ | $g_m/I_D = 1/[nV_T(1 + q)]$ |
|---|---|---|---|---|
| 0.2 µA | **0.0765** | weak | **0.0714** | **27.77** S/A |
| 4 µA | **1.530** | moderate | **0.834** | **16.22** S/A |
| 200 µA | **76.5** | strong | **8.26** | **3.21** S/A |

A thousandfold change in current moves $g_m/I_D$ by a factor of only **8.64**: the transistor is efficient over a wide range, but the last factor of ten in current buys almost nothing.

### Solution 20-01.2

(a) As $IC \to 0$, $\sqrt{1 + 4IC} \to 1$ and the expression tends to $2/(2nV_T) = 1/(nV_T)$. For $IC \gg 1$, $\sqrt{1 + 4IC} \approx 2\sqrt{IC}$ and $g_m/I_D \to 1/(nV_T\sqrt{IC})$. In strong inversion $IC \approx q^2$ and $V_{ov} \approx 2nV_Tq$, so $\sqrt{IC} = V_{ov}/(2nV_T)$ and $g_m/I_D \to 2/V_{ov}$.

(b) $V_T = kT/q_e$: at 233.15 K, $1/(nV_T)$ = **38.29** S/A; at 398.15 K, **22.42** S/A. The best possible efficiency falls by **41** % from a cold to a hot chip.

### Solution 20-01.3

(a) Doubling $W$ doubles $I_{spec}$ to 20.92 µA, so $IC$ halves to **0.956** and $g_m/I_D$ rises from 14.77 to **18.37** S/A (with velocity saturation at 0.5 µm).

(b) At fixed current, a wider transistor runs in weaker inversion, so it delivers more $g_m$ per microampere; the cost is gate area and capacitance, which lower $f_T$ and load whatever drives the gate. The gain in $g_m$ is sublinear: doubling the width here raises $g_m$ by **24** %, and the returns vanish as $g_m/I_D$ approaches $1/(nV_T)$.

(c) At fixed length, $I_D$, $g_m$, $g_{ds}$ and $C_{gg}$ are all proportional to $W$ at a given inversion level, so the ratios $g_m/I_D$, $I_D/W$, $f_T$ and $g_m/g_{ds}$ depend only on $IC$. A table of these ratios against $g_m/I_D$ therefore serves every width.

### Solution 20-01.4

(a) $V_{ov} = nV_T(2q + \ln q)$ with $nV_T$ = 33.61 mV:

| $IC$ | 0.01 | 0.1 | 1 | 10 | 100 |
|---|---|---|---|---|---|
| $V_{ov}$ (mV) | **−154.4** | **−74.2** | **25.4** | **215.0** | **715.1** |

(b) $V_{ov} = 0$ when $2q + \ln q = 0$, at $q$ = 0.4263, so $IC = q^2 + q$ = **0.608**: a transistor biased exactly at threshold is already in moderate inversion.

(c) A negative overdrive means the gate sits below the threshold voltage and the current flows by diffusion. As a design variable, overdrive is poor for two reasons: in weak and moderate inversion the current is not a simple function of it, and it references $V_{TH}$, which varies with corner, length and drain voltage. $IC$ and $g_m/I_D$ depend only on current and size.

### Solution 20-01.5

$I_D = 1\ \text{mS}/20\ \text{S/A}$ = **50.0** µA. At 0.5 µm, $g_m/I_D$ = 20 S/A requires $IC$ = **0.695**, whose current density is $0.695 \times 0.523/0.5$ = **0.727** µA/µm. So $W = 50/0.727$ = **68.8** µm. Then $f_T$ = **0.807** GHz, intrinsic gain $20 \times 8 \times 0.5$ = **80** and $C_{gg} = \tfrac23 \times 68.8 \times 0.5 \times 8.6$ fF = **197.2** fF.

### Solution 20-01.6

(a) $L = A_i/[(g_m/I_D)V_A']$: at 20 S/A, $100/(20 \times 8)$ = **0.625** µm; at 12 S/A, **1.042** µm.

(b) At 0.625 µm and 20 S/A, $f_T$ = **0.521** GHz; at 1.042 µm and 12 S/A, $f_T$ = **0.565** GHz.

(c) The longer, more strongly inverted transistor is slightly faster. Moving from 20 to 12 S/A raises $f_T$ (more inversion), but the length needed for the same gain rises by **1.67** times, which cuts $f_T$ by about $1.67^2$; the two effects nearly cancel here. For a fixed gain, $f_T$ is therefore flat over a wide range of $g_m/I_D$, and the deciding factor becomes the current: the 20 S/A design draws **40** % less current for the same $g_m$.

### Solution 20-01.7

(a) For large $q$, $IC = (q^2 + q)/(1 + \lambda_cq) \to q/\lambda_c$, so $I_D \to I_{spec}\,q/\lambda_c = 2n\mu C_{ox}\frac WLV_T^2q\cdot\frac{Lv_{sat}}{\mu V_T} = 2nC_{ox}WV_Tv_{sat}\,q$. With $V_{ov} \approx 2nV_Tq$ in strong inversion, $I_D \to WC_{ox}v_{sat}V_{ov}$.

(b) $\lambda_c = \mu V_T/(v_{sat}L)$: **0.0754** at 0.15 µm and **0.189** at 60 nm. $f_T \to 3v_{sat}/(4\pi L)$: **127.3** GHz and **318.3** GHz.

(c) A velocity-saturated transistor's current, and so its $g_m$, no longer grows as $1/L$: carriers cross at a fixed speed, so the transit time is proportional to $L$, not $L^2$. With $C_{gg} \propto L$, $f_T \propto 1/L$.

### Solution 20-01.8

(a) $2q + \ln q = V_{ov}/(nV_T) = 0.2/0.03361 = 5.951$, so $q$ = **2.514** and $f_T = 3\mu V_Tq/(2\pi L^2)$ = **1.086** GHz.

(b) 09-09's formula gives **1.285** GHz, **18** % higher. It assumes $V_{ov} = 2nV_Tq$, ignoring the $\ln q$ part of the charge–potential relation; at 0.2 V that term absorbs $nV_T\ln q$ = **31** mV of the overdrive, so the true charge, and $g_m$, are lower. The two agree only deep in strong inversion.

### Solution 20-01.9

(a) $IC = 0.5/10.46$ = **0.0478**, weak inversion; the gate voltage is $V_{TH} + nV_T(2q + \ln q)$ = **0.3494** V, **101** mV below threshold.

(b) With $V_{TH}$ 30 mV higher the model gives **0.210** µA (×**0.421**); 30 mV lower, **1.150** µA (×**2.30**). The weak-inversion approximation gives ×**0.410** and ×**2.44**. The approximation is slightly off because at $IC$ = 0.048 the drift term is not yet negligible.

(c) With the current fixed, $IC$ and therefore $g_m/I_D$ and $g_m$ are unchanged in the model: the gate voltage simply moves by 30 mV. This is why analog transistors are biased by currents.

### Solution 20-01.10

| Temperature | $I_D/(nV_T)$ | Model $g_m$ |
|---|---|---|
| −40 °C | **38.29** µS | **34.76** µS |
| 27 °C | **29.76** µS | **27.30** µS |
| 125 °C | **22.42** µS | **20.78** µS |

The model's values are **9.2** %, **8.3** % and **7.3** % lower because 1 µA is not deep weak inversion: $IC$ = **0.108**, **0.096** and **0.083**, so $g_m/I_D$ is already below its limit. Both fall roughly as $1/T$, the model's $g_m$ by **40** % from −40 °C to 125 °C.

### Solution 20-01.11

At $L$ = 0.3 µm ($\lambda_c$ = **0.0377**) the product peaks at $IC$ = **13.6**, $g_m/I_D$ = **6.25** S/A and $f_T$ = **13.7** GHz, a peak value of **85.7** GHz/V. At 0.15 µm the peak was at $IC$ = 6.86 and 8.00 S/A. Halving $\lambda_c$ by doubling $L$ delays velocity saturation to a higher inversion level, so the flattening of $f_T$, and with it the peak, moves into stronger inversion; the peak value falls about as $1/L^{1.7}$ here (exponent **1.72**), between the velocity-saturated $1/L$ and the long-channel $1/L^2$.

### Solution 20-01.12

(a) With $V_P/V_T = 2q + \ln q$, $dq/d(V_P/V_T) = q/(2q + 1)$. The quotient rule gives

$$
\frac{d\,IC}{dq} = \frac{(2q + 1)(1 + \lambda_cq) - \lambda_c(q^2 + q)}{(1 + \lambda_cq)^2} = \frac{\lambda_cq^2 + 2q + 1}{(1 + \lambda_cq)^2} .
$$

Since $g_m = I_{spec}\,\frac{d\,IC}{dq}\frac{dq}{dV_P}\frac{dV_P}{dV_{GS}}$ with $dV_P/dV_{GS} = 1/n$,

$$
\frac{g_m}{I_D} = \frac{1}{nV_T}\cdot\frac{\lambda_cq^2 + 2q + 1}{(1 + \lambda_cq)^2}\cdot\frac{q}{2q + 1}\cdot\frac{1 + \lambda_cq}{q^2 + q} = \frac{1}{nV_T}\cdot\frac{\lambda_cq^2 + 2q + 1}{(2q + 1)(1 + \lambda_cq)(1 + q)} .
$$

(b) With $\lambda_c = 0$ the numerator equals $2q + 1$ and cancels, leaving $1/[nV_T(1 + q)]$. For large $q$ the numerator tends to $\lambda_cq^2$ and the denominator to $2q \cdot \lambda_cq \cdot q$, so the ratio tends to $1/(2nV_Tq)$.

(c) At $IC$ = 10 and $L$ = 0.15 µm, $g_m/I_D$ = **6.58** S/A, against **8.04** S/A for a long channel: velocity saturation costs 18% of the efficiency at this inversion level.

### Solution 20-01.13

(a) $f_T$ rises with inversion, so the highest $g_m/I_D$ that meets 10 GHz is where $f_T$ = 10 GHz exactly: $IC$ = **0.837**, $g_m/I_D$ = **18.51** S/A. The current is $2\ \text{mS}/18.51$ = **108.0** µA, and $W$ = **37.0** µm.

(b) At 8 S/A the current is **250** µA, **2.31** times more, the width **10.5** µm and $f_T$ = **35.4** GHz, far more speed than required.

(c) For a battery-powered product, (a): it meets the specification with **57** % less current. The sweet spot would win if the transistor's own gate capacitance mattered (the 37 µm device loads its driver **3.5** times more), if large signals required a larger $V_{DS,sat}$, or if the $f_T$ margin had to cover slow corners and parasitics that this model omits.

### Solution 20-01.14

(a) At 25 S/A: $I_D$ = **20** µA, $W$ = **87.1** µm, area **43.5** µm². At 10 S/A: $I_D$ = **50** µA, $W$ = **9.04** µm, area **4.52** µm².

(b) The area ratio is **9.64**, so mismatch improves by $\sqrt{9.64}$ = **3.10** times. The weak-inversion design saves **60** % of the current and matches three times better, at the price of nearly ten times the area and gate capacitance.

### Solution 20-01.15

(a) At 0.15 µm, 22 S/A needs $IC$ = **0.423** (weak to moderate inversion), giving $f_T$ = **6.00** GHz and an intrinsic gain of $22 \times 8 \times 0.15$ = **26.4**.

(b) Useful questions: *"What is the driver's bandwidth, and what $f_T$ margin do you have at the slow corner?"* (6 GHz may be ample for a 50 MHz driver and marginal for 1 GHz; a strong answer gives the ratio at the worst corner). *"How do you reach the loop gain you need with an intrinsic gain of about 26 per device?"* (a strong answer names the cascodes or gain stages and the settling-error budget they meet). *"Why minimum length at such weak inversion?"* (minimum length buys $f_T$ that weak inversion then gives away; a strong answer explains the area or capacitance constraint behind it, or the team realizes a longer channel would cost little speed and add gain).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 20-01.1a | specific current | 2.615 | µA |
| 20-01.1b | IC at 0.2 uA | 0.0765 | — |
| 20-01.1c | g_m/I_D at 0.2 uA | 27.77 | S/A |
| 20-01.1d | IC at 4 uA | 1.530 | — |
| 20-01.1e | g_m/I_D at 4 uA | 16.22 | S/A |
| 20-01.1f | IC at 200 uA | 76.5 | — |
| 20-01.1g | g_m/I_D at 200 uA | 3.21 | S/A |
| 20-01.2a | weak-inversion limit at -40 C | 38.29 | S/A |
| 20-01.2b | weak-inversion limit at 125 C | 22.42 | S/A |
| 20-01.3a | IC at twice the width | 0.956 | — |
| 20-01.3b | g_m/I_D at twice the width | 18.37 | S/A |
| 20-01.4a | overdrive at IC = 0.01 | -154.4 | mV |
| 20-01.4b | overdrive at IC = 0.1 | -74.2 | mV |
| 20-01.4c | overdrive at IC = 1 | 25.4 | mV |
| 20-01.4d | overdrive at IC = 10 | 215.0 | mV |
| 20-01.4e | overdrive at IC = 100 | 715.1 | mV |
| 20-01.4f | IC at zero overdrive | 0.608 | — |
| 20-01.5a | drain current | 50.0 | µA |
| 20-01.5b | inversion coefficient | 0.695 | — |
| 20-01.5c | current density | 0.727 | µA/µm |
| 20-01.5d | width | 68.8 | µm |
| 20-01.5e | f_T | 0.807 | GHz |
| 20-01.5f | intrinsic gain | 80 | — |
| 20-01.5g | gate capacitance | 197.2 | fF |
| 20-01.6a | length at 20 S/A | 0.625 | µm |
| 20-01.6b | length at 12 S/A | 1.042 | µm |
| 20-01.6c | f_T at 20 S/A | 0.521 | GHz |
| 20-01.6d | f_T at 12 S/A | 0.565 | GHz |
| 20-01.7a | lambda_c at 0.15 um | 0.0754 | — |
| 20-01.7b | lambda_c at 60 nm | 0.189 | — |
| 20-01.7c | f_T limit at 0.15 um | 127.3 | GHz |
| 20-01.7d | f_T limit at 60 nm | 318.3 | GHz |
| 20-01.8a | normalized charge | 2.514 | — |
| 20-01.8b | f_T from the model | 1.086 | GHz |
| 20-01.8c | f_T from 09-09 | 1.285 | GHz |
| 20-01.9a | IC at 0.5 uA | 0.0478 | — |
| 20-01.9b | gate voltage | 0.3494 | V |
| 20-01.9c | current, threshold up 30 mV | 0.210 | µA |
| 20-01.9d | current, threshold down 30 mV | 1.150 | µA |
| 20-01.9e | weak-inversion factor, up | 0.410 | — |
| 20-01.9f | weak-inversion factor, down | 2.44 | — |
| 20-01.10a | limit g_m at -40 C | 38.29 | µS |
| 20-01.10b | model g_m at -40 C | 34.76 | µS |
| 20-01.10c | limit g_m at 27 C | 29.76 | µS |
| 20-01.10d | model g_m at 27 C | 27.30 | µS |
| 20-01.10e | limit g_m at 125 C | 22.42 | µS |
| 20-01.10f | model g_m at 125 C | 20.78 | µS |
| 20-01.10g | IC at -40 C | 0.108 | — |
| 20-01.11a | IC at the peak | 13.6 | — |
| 20-01.11b | g_m/I_D at the peak | 6.25 | S/A |
| 20-01.11c | f_T at the peak | 13.7 | GHz |
| 20-01.11d | peak product | 85.7 | GHz/V |
| 20-01.12a | g_m/I_D at IC = 10, 0.15 um | 6.58 | S/A |
| 20-01.12b | long-channel g_m/I_D at IC = 10 | 8.04 | S/A |
| 20-01.13a | IC meeting 10 GHz | 0.837 | — |
| 20-01.13b | g_m/I_D meeting 10 GHz | 18.51 | S/A |
| 20-01.13c | current | 108.0 | µA |
| 20-01.13d | width | 37.0 | µm |
| 20-01.13e | current at 8 S/A | 250 | µA |
| 20-01.13f | width at 8 S/A | 10.5 | µm |
| 20-01.13g | f_T at 8 S/A | 35.4 | GHz |
| 20-01.14a | current at 25 S/A | 20 | µA |
| 20-01.14b | width at 25 S/A | 87.1 | µm |
| 20-01.14c | area at 25 S/A | 43.5 | µm² |
| 20-01.14d | current at 10 S/A | 50 | µA |
| 20-01.14e | width at 10 S/A | 9.04 | µm |
| 20-01.14f | area at 10 S/A | 4.52 | µm² |
| 20-01.14g | area ratio | 9.64 | — |
| 20-01.14h | mismatch improvement | 3.10 | — |
| 20-01.15a | IC at 22 S/A, 0.15 um | 0.423 | — |
| 20-01.15b | f_T | 6.00 | GHz |
| 20-01.15c | intrinsic gain | 26.4 | — |
| 20-01.1h | q at 0.2 uA | 0.0714 | — |
| 20-01.1i | q at 4 uA | 0.834 | — |
| 20-01.1j | q at 200 uA | 8.26 | — |
| 20-01.1k | ratio of g_m/I_D over the range | 8.64 | — |
| 20-01.2c | fall of the limit from -40 C to 125 C | 41 | % |
| 20-01.3c | rise of g_m from doubling the width | 24 | % |
| 20-01.6e | length ratio | 1.67 | — |
| 20-01.6f | current saved at 20 S/A | 40 | % |
| 20-01.8d | 09-09 formula over the model | 18 | % |
| 20-01.8e | overdrive absorbed by the logarithm | 31 | mV |
| 20-01.9g | gate below threshold | 101 | mV |
| 20-01.9h | model current factor, up | 0.421 | — |
| 20-01.9i | model current factor, down | 2.30 | — |
| 20-01.10h | model below limit at -40 C | 9.2 | % |
| 20-01.10i | model below limit at 27 C | 8.3 | % |
| 20-01.10j | model below limit at 125 C | 7.3 | % |
| 20-01.10k | IC at 27 C | 0.096 | — |
| 20-01.10l | IC at 125 C | 0.083 | — |
| 20-01.10m | fall of model g_m from -40 C to 125 C | 40 | % |
| 20-01.11e | lambda_c at 0.3 um | 0.0377 | — |
| 20-01.11f | exponent of the peak's fall with L | 1.72 | — |
| 20-01.13h | current ratio | 2.31 | — |
| 20-01.13i | current saved | 57 | % |
| 20-01.13j | gate-load ratio | 3.5 | — |
| 20-01.14i | current saved at 25 S/A | 60 | % |
