# Problems 01-01 · Functions, Models and Units

Chapter: [01-01](../chapters/01-01-functions-models-and-units.md) · Worked solutions: [01-01 solutions](../solutions/01-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $\ln$ is the natural log; angles in radians unless degrees are stated; answers to 4 significant figures unless stated. Use $V_T = kT/q$ with $k = 1.380649\times10^{-23}$ J/K and $q = 1.602176634\times10^{-19}$ C. Use a calculator or Python freely, but show the method.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 01-01.1 [A]

A temperature sensor outputs $V(T) = 0.5\text{ V} + (10\text{ mV/°C})\,T$ for $-40\text{ °C} \le T \le 125\text{ °C}$. Its output feeds a 12-bit ADC whose code is $N(V) = 4096\,V/(3.3\text{ V})$ (ignore rounding to whole codes).

(a) What is the range of $V$?
(b) Write the composition $N(T)$. What code corresponds to 25 °C?
(c) What is the slope of $N(T)$, with units?
(d) Find the inverse function $T(N)$ and the temperature that produces code 1500.
(e) What is the range of codes the ADC will ever see?

### Problem 01-01.2 [A]

Which of these expressions are dimensionally valid? For each invalid one, write a corrected version. ($t$ is time, $R$ resistance, $C$ capacitance, $L$ inductance, $f$ frequency in Hz, $V$ and $V_T$ voltages, $P$ power, $I_1$ and $I_2$ currents.)

(a) $e^{-t/(RC)}$  (b) $\ln V$  (c) $\sin(2\pi f t)$  (d) $\cos(2\pi f)$  (e) $e^{-Rt/L}$  (f) $10\log_{10}(P/1\text{ mW})$  (g) $e^{V/V_T}$  (h) $\ln I_1 - \ln I_2$

### Problem 01-01.3 [A]

Simplify without a calculator (except in (f)).

(a) $e^{3}e^{-5}/e^{-2}$  (b) $\ln\!\left(e^{4}\sqrt{e}\right)$  (c) $\log_{10}0.001$  (d) $\log_2 1024$  (e) $\ln 20 - \ln 5 + \ln\tfrac{1}{4}$  (f) $\log_2 10$, using the change-of-base rule  (g) $\ln\!\left(\sqrt[3]{e^{2}}\right)$

### Problem 01-01.4 [A]

Solve for the unknown.

(a) $5e^{-t/(3\text{ ms})} = 1$  (b) $2^{x} = 50$  (c) $10^{x/10} = 0.25$
(d) A voltage decays exponentially from 4.0 V to 1.5 V in 10 µs. Find the time constant $\tau$.

### Problem 01-01.5 [A]

Decibel conversions.

(a) Express these power ratios in dB: 2, 0.01, 1000, 0.5.
(b) Convert to power ratios: 13 dB, −7 dB.
(c) An amplitude (voltage) ratio of 0.5, across equal impedances, in dB. A voltage gain of 46 dB as a ratio.
(d) An op-amp's open-loop voltage gain is specified as 100 dB. What is it as a ratio?

### Problem 01-01.6 [A]

Absolute power levels.

(a) Express in dBm: 100 mW, 1 µW, 2 W, 0.25 mW.
(b) Express in watts or milliwatts: −90 dBm, 17 dBm.
(c) A Bluetooth Low Energy radio transmits 0 dBm into a 50 Ω antenna. What are the RMS and peak voltages of the (sinusoidal) signal?
(d) Express that RMS voltage in dBV.

### Problem 01-01.7 [A]

A current is $i(t) = 0.5\cos(2000\pi t - 0.7)$ mA, with $t$ in seconds.

(a) Find the frequency and period.
(b) Express the phase in degrees.
(c) Find the RMS value.
(d) Evaluate $i(0.1\text{ ms})$.
(e) When is the first positive peak after $t = 0$?

### Problem 01-01.8 [B]

A 5 V step charges a capacitor through a resistor: $v(t) = 5\left(1 - e^{-t/\tau}\right)$ V with $R = 10$ kΩ and $C = 100$ nF.

(a) Find $\tau = RC$.
(b) How long until $v = 2.5$ V? Until $v = 4.5$ V?
(c) The **10–90% rise time** is the time to go from 10% to 90% of the final value. Show that it equals $\tau\ln 9$ and evaluate it.
(d) Evaluate $v(3\text{ ms})$.
(e) A logic gate reads the input as high once it exceeds 70% of 5 V. How long after the step does that happen?

### Problem 01-01.9 [B]

The ideal diode law is $I = I_s e^{V/V_T}$ in forward bias (the −1 is negligible). Ignore the temperature dependence of $I_s$ here; [09-06](../../09-semiconductor-devices/chapters/09-06-pn-junction-iv-and-capacitance.md) shows it is strong.

(a) Compute $V_T$ and the millivolts per decade of current, $V_T\ln 10$, at 250 K, 300 K and 400 K.
(b) At 300 K, a diode carries 1 mA at 0.650 V. What voltage gives 10 µA? What voltage gives 100 mA?
(c) What current flows at 0.700 V?
(d) Why does a real diode at 100 mA usually need *more* voltage than your answer to (b)?

### Problem 01-01.10 [B]

A short-range radio link has the following budget: transmitter output 20 dBm, cable loss 2 dB, transmit antenna gain 3 dBi, path loss 80 dB, receive antenna gain 3 dBi. The receiver needs at least −90 dBm (its **sensitivity**).

(a) Find the received power in dBm and in watts.
(b) What is the **link margin** (received power minus sensitivity)?
(c) In free space, received power falls as $1/d^2$, i.e. 20 dB per decade of distance. By what factor could the distance grow before the margin is used up?
(d) If the transmitter power doubles, by how many dB does the margin grow, and by what factor does the free-space range grow?

### Problem 01-01.11 [B]

A tilt sensor uses an accelerometer that measures $a_x = g\sin\theta$ for a tilt angle $\theta$. To save computation, the firmware estimates the angle as $\hat\theta = a_x/g$ (in radians), the small-angle approximation.

(a) For true tilts of 5°, 15° and 30°, find the estimate $\hat\theta$ in degrees and the relative error $1 - \hat\theta/\theta$ in percent.
(b) Up to what tilt is the relative error at most 1%? First use $\sin\theta \approx \theta - \theta^3/6$ to get a closed-form estimate, then solve numerically.

### Problem 01-01.12 [B]

A processor core's dynamic power is $P = \alpha CV^2f$. At 1.0 V and 2.0 GHz it consumes 1.5 W.

(a) The supply is reduced to 0.8 V at the same frequency. Find the power.
(b) Under DVFS, the frequency is scaled with voltage to 1.6 GHz at 0.8 V. Find the power.
(c) Find the energy per clock cycle, $P/f$, at the nominal point and at the DVFS point.
(d) A task needs $3\times10^9$ cycles. Find its run time and energy at each point.
(e) Now add a constant leakage power of 0.2 W, drawn whenever the core is on. Recompute the task energy at both points and the percentage saving from DVFS. Compare with the saving without leakage, and explain the difference.

### Problem 01-01.13 [B]

A capacitor discharging through a resistor is sampled every millisecond (synthetic data):

| $t$ (ms) | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $v$ (V) | 4.000 | 2.054 | 1.054 | 0.541 | 0.278 |

(a) Show that the model $v = v_0e^{-t/\tau}$ becomes a straight line on semilog axes. What are its slope and intercept?
(b) Fit the line by least squares. Report $\tau$ and $v_0$ to 3 significant figures.
(c) Estimate $\tau$ from only the first and last points.
(d) Use the fitted model (with the rounded values from (b)) to predict $v(6\text{ ms})$.

### Problem 01-01.14 [C]

Indoors, walls and furniture make radio signals fall off faster than in free space. A common empirical model is the **log-distance path-loss model**, $P_r(d) = P_r(1\text{ m}) \cdot d^{-n}$ with $d$ in meters, where the exponent $n$ is 2 in free space and larger indoors. You measure (synthetic data):

| $d$ (m) | 1 | 2 | 5 | 10 | 20 |
|---|---|---|---|---|---|
| $P_r$ (dBm) | −40.0 | −49.0 | −61.0 | −70.0 | −79.0 |

(a) Show that in dBm the model is $P_{r,\text{dBm}} = A - 10n\log_{10}d$, a straight line against $\log_{10}d$. What is $A$?
(b) Fit the line. Report $n$ to 2 significant figures and $A$ to the nearest 0.1 dBm.
(c) With the rounded values from (b), at what distance does the received power reach a receiver sensitivity of −90 dBm?
(d) What range would the same $A$ give in free space ($n = 2$)? Comment on what this means for specifying an indoor product from free-space numbers.
(e) Why should you be cautious about using the fit at 200 m?

### Problem 01-01.15 [C]

Doubling times, rates and the "rule of 70".

(a) A quantity doubles every 2 years. What is its annual growth factor and annual percentage growth?
(b) Write it as a continuous exponential $e^{rt}$. What is $r$? What is the corresponding time constant $\tau = 1/r$?
(c) By what factor does it grow in 10 years?
(d) The finance "rule of 70" estimates doubling time as $70/(\text{percent growth per period})$. Derive it from $(1 + g)^{t} = 2$, stating the approximation it makes.
(e) Apply the rule to the 41.42%/year growth from (a), and to 7%/year growth. Compare each with the exact doubling time, and explain why the rule works much better in one case.

---

## Objective coverage

| Learning objective (chapter 01-01) | Problems |
|---|---|
| 1. Functions with domain, range and units; function families | 1, 2, 12 |
| 2. Exponential and logarithm laws; solving for time or rate | 3, 4, 8, 9, 15 |
| 3. Decibels for power and amplitude; dBm | 5, 6, 10, 14 |
| 4. Sinusoids in radian form; small-angle approximations | 7, 11 |
| 5. Fitting exponential and power-law models by linearization | 12, 13, 14 |
