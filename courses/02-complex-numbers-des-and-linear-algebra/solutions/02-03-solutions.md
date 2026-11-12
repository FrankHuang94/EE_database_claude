# Solutions 02-03 · Second-Order Linear ODEs and the Characteristic Equation

Problems: [02-03 problems](../problems/02-03-problems.md) · Chapter: [02-03](../chapters/02-03-second-order-linear-odes.md)

Every numerical answer below is listed in the answer key at the end and is recomputed independently by [verify_02_03.py](../verify/verify_02_03.py).

---

## Solutions

### Solution 02-03.1

(a) Series: α = $R/(2L) = 50/0.02 = $ **2500 s⁻¹**, $\omega_0 = 1/\sqrt{10^{-2}\times10^{-6}} = $ **1.000×10⁴ rad/s**, so ζ = **0.25**: underdamped.

(b) Parallel: α = $1/(2RC) = 1/(2\times1000\times10^{-6}) = $ **500 s⁻¹**, $\omega_0 = 10^4$ rad/s, so ζ = **0.05**: lightly underdamped. The same $L$ and $C$ with a 1 kΩ *parallel* resistor ring far more than with 50 Ω in series.

(c) $\omega_0 = \sqrt{k_s/m} = \sqrt{80/0.2} = $ **20 rad/s**, α = $b/(2m) = 2/0.4 = $ **5 s⁻¹**, so ζ = **0.25**: underdamped.

### Solution 02-03.2

(a) $s^2 + 5s + 6 = (s + 2)(s + 3)$: roots −2 and −3, overdamped. $y = c_1e^{-2t} + c_2e^{-3t}$.

(b) $s^2 + 4s + 4 = (s + 2)^2$: a double root at −2, critically damped. $y = (c_1 + c_2t)e^{-2t}$.

(c) $s = -1 \pm\sqrt{1 - 10} = -1 \pm 3j$: underdamped, with $\omega_0 = \sqrt{10} = $ **3.162** and ζ = $1/\sqrt{10} = $ **0.3162**. $y = e^{-t}(A\cos3t + B\sin3t)$.

### Solution 02-03.3

From Solution 2(a), $y = c_1e^{-2t} + c_2e^{-3t}$. The conditions give $c_1 + c_2 = 1$ and $-2c_1 - 3c_2 = 0$, so $c_1 = 3$ and $c_2 = -2$:

$$
y(t) = 3e^{-2t} - 2e^{-3t}, \qquad y(1) = 3e^{-2} - 2e^{-3} = 0.3064 .
$$

**Check:** $y'(0) = -6 + 6 = 0$ ✓.

### Solution 02-03.4

$s_1 = \omega_0\big(-\zeta + \sqrt{\zeta^2 - 1}\big) = \omega_0\big(-\zeta + \zeta\sqrt{1 - 1/\zeta^2}\big)$. For large ζ, $\sqrt{1 - u} \approx 1 - u/2$ with $u = 1/\zeta^2$, so $s_1 \approx \omega_0\big(-\zeta + \zeta - 1/(2\zeta)\big) = -\omega_0/(2\zeta)$.

For ζ = 5: exactly $s_1/\omega_0 = -5 + \sqrt{24} = $ **−0.1010**; approximately $-1/10 = -0.1$. The approximation is **1.0%** too small in magnitude. The slow time constant, $2\zeta/\omega_0$, *grows* with damping: an overdamped system gets slower as damping increases.

### Solution 02-03.5

$y = (c_1 + c_2t)e^{-2t}$ with $c_1 = y(0) = 2$. Then $y' = (c_2 - 2c_1 - 2c_2t)e^{-2t}$, so $y'(0) = c_2 - 4 = -1$ and $c_2 = 3$:

$$
y(t) = (2 + 3t)e^{-2t}, \qquad y(1) = 5e^{-2} = 0.6767 .
$$

Since $2 + 3t > 0$ for all $t > 0$, $y$ never crosses zero: a critically damped response crosses zero at most once, and here not at all.

### Solution 02-03.6

(a) A constant particular solution $y_p = X$ satisfies $\omega_0^2X = \omega_0^2X$. So $y = X + (c_1 + c_2t)e^{-\omega_0t}$. From $y(0) = 0$, $c_1 = -X$. Differentiating, $y'(0) = c_2 - \omega_0c_1 = 0$, so $c_2 = -\omega_0X$. Hence $y = X\big[1 - (1 + \omega_0t)e^{-\omega_0t}\big]$.

(b) Solve $(1 + x)e^{-x} = 0.1$ numerically: $x = $ **3.890**. With $\omega_0 = 10^4$ rad/s, $t = x/\omega_0 = $ **389.0 µs**.

### Solution 02-03.7

(a) Differentiate $y = X\big[1 - e^{-\alpha t}\big(\cos\omega_dt + \frac{\alpha}{\omega_d}\sin\omega_dt\big)\big]$:

$$
y' = Xe^{-\alpha t}\left[\alpha\cos\omega_dt + \frac{\alpha^2}{\omega_d}\sin\omega_dt + \omega_d\sin\omega_dt - \alpha\cos\omega_dt\right] = X\frac{\alpha^2 + \omega_d^2}{\omega_d}e^{-\alpha t}\sin\omega_dt .
$$

Since $\alpha^2 + \omega_d^2 = \omega_0^2$, this is $X\frac{\omega_0^2}{\omega_d}e^{-\alpha t}\sin\omega_dt$. It is positive until $\omega_dt = \pi$, so the first peak is at $t_p = \pi/\omega_d$.

(b) $\omega_d = 1000\sqrt{1 - 0.09} = $ **953.9 rad/s**, $t_p = \pi/953.9 = $ **3.293 ms**, and the overshoot is $\exp(-0.3\pi/\sqrt{0.91}) = $ **37.23%**.

### Solution 02-03.8

(a) α = $R/(2L) = $ **1000 s⁻¹**, $\omega_0 = 1/\sqrt{10^{-3}\times10^{-5}} = $ **1.000×10⁴ rad/s**, and $\omega_d = \sqrt{10^8 - 10^6} = $ **9950 rad/s**. The capacitor starts uncharged, $v_C(0) = 0$, and the loop current flows into it: $v_C'(0) = i(0)/C = 1/10^{-5} = $ **1.000×10⁵ V/s**.

(b) By chapter §3.7, $A = 0$ and $B = v_C'(0)/\omega_d = $ **10.05 V**:

$$
v_C(t) = 10.05\,e^{-1000t}\sin(9950t)\text{ V}.
$$

(c) $v_C' = 10.05e^{-1000t}\big(9950\cos9950t - 1000\sin9950t\big) = 0$ when $\tan(9950t) = 9.950$, so $t = \arctan(9.950)/9950 = $ **147.8 µs**, where $v_C = $ **8.626 V**. At that instant $v_C' = 0$, so the current is zero and all the remaining energy is in the capacitor: $\tfrac12(10^{-5})(8.626)^2 = $ **0.3720 mJ**, which is **74.41%** of the inductor's initial $\tfrac12(10^{-3})(1)^2 = 0.5$ mJ. The rest was dissipated in the resistor.

### Solution 02-03.9

(a) α = $1/(2RC) = 1/(2\times200\times10^{-6}) = $ **2500 s⁻¹**, $\omega_0 = 10^4$ rad/s, ζ = **0.25**, and $\omega_d = \sqrt{10^8 - 6.25\times10^6} = $ **9682 rad/s**.

(b) KCL: $Cv' + v/R + i_L = 0$, so $v'(0) = -\big(10/200 + 0\big)/10^{-6} = $ **−5.000×10⁴ V/s**.

(c) $A = v(0) = 10$ V and $B = \big(v'(0) + \alpha A\big)/\omega_d = (-5\times10^4 + 2.5\times10^4)/9682 = $ **−2.582 V**:

$$
v(t) = e^{-2500t}\big(10\cos9682t - 2.582\sin9682t\big)\text{ V}.
$$

### Solution 02-03.10

(a) $W = e^{s_1t}\cdot s_2e^{s_2t} - s_1e^{s_1t}\cdot e^{s_2t} = (s_2 - s_1)e^{(s_1 + s_2)t}$, nonzero because $s_1 \ne s_2$ and exponentials never vanish.

(b) With $y_2 = te^{-\alpha t}$, $y_2' = (1 - \alpha t)e^{-\alpha t}$. So $W = e^{-\alpha t}(1 - \alpha t)e^{-\alpha t} - (-\alpha e^{-\alpha t})te^{-\alpha t} = e^{-2\alpha t} \ne 0$.

(c) Let $c = \cos\omega_dt$ and $s = \sin\omega_dt$. Then $y_1' = e^{-\alpha t}(-\alpha c - \omega_ds)$ and $y_2' = e^{-\alpha t}(-\alpha s + \omega_dc)$, so

$$
W = e^{-2\alpha t}\big[c(-\alpha s + \omega_dc) - s(-\alpha c - \omega_ds)\big] = \omega_de^{-2\alpha t}(c^2 + s^2) = \omega_de^{-2\alpha t} \ne 0 .
$$

At $t = 0$ with $\omega_d = 3$: $W = $ **3**.

### Solution 02-03.11

With OS = 0.10, $\ln\text{OS} = -2.303$, so $\zeta = 2.303/\sqrt{\pi^2 + 2.303^2} = $ **0.5912**. The peak time gives $\omega_d = \pi/(50\text{ µs}) = $ **62.83 krad/s**, so $\omega_0 = \omega_d/\sqrt{1 - \zeta^2} = $ **77.90 krad/s**, and $Q = 1/(2\zeta) = $ **0.8458**. A loop with about 10% overshoot and ζ near 0.6 is a common, reasonable PLL design point.

### Solution 02-03.12

(a) $\omega_0 = 1/\sqrt{10^{-4}\times10^{-7}} = $ **316.2 krad/s** and $Q = \frac{1}{R}\sqrt{L/C} = 2\sqrt{1000} = $ **63.25**.

(b) $Q/\pi = $ **20.13** cycles.

(c) α = $R/(2L) = 2500$ s⁻¹ and $\omega_d \approx \omega_0$. The energy decays as $e^{-2\alpha t}$, so over one period $2\pi/\omega_d$ the fraction lost is $1 - e^{-4\pi\alpha/\omega_d} = $ **9.457%**. The estimate $2\pi/Q = $ **9.935%** is the first-order term of that exponential; it is good for high $Q$ and overestimates the loss as $Q$ falls.

### Solution 02-03.13

(a) $\omega_0 = 1/\sqrt{2\times10^{-9}\times2\times10^{-12}} = $ **1.581×10¹⁰ rad/s**, so $f_0 = $ **2.516 GHz**. $\zeta = \frac{R}{2}\sqrt{C/L} = 5\sqrt{10^{-3}} = $ **0.1581**.

(b) Overshoot $= \exp\big(-\pi\times0.1581/\sqrt{1 - 0.025}\big) = $ **60.47%**: a 1 V edge would ring up to about 1.6 V at the pad, stressing the input and reflecting noise back.

(c) $R = 2\zeta\sqrt{L/C} = 1.4\times31.62 = $ **44.27 Ω** gives ζ = 0.7 and an overshoot of **4.60%**. The cost is speed: the larger resistance slows the edge (the response time scales with $1/(\zeta\omega_0)$ for the decay and with $RC$ for charging the pad), which eats into timing margin at high data rates. Package designers therefore also attack $L$ (shorter bonds, flip-chip bumps) rather than relying on resistance alone.

### Solution 02-03.14

(a) $Z_t = 0.8\times0.05/50 = $ **0.8 mΩ**. $\sqrt{L/C} = \sqrt{5\times10^{-12}/10^{-6}} = $ **2.236 mΩ**, about 2.8× the target: the design does not meet it.

(b) First droop $\approx \Delta I\sqrt{L/C} = 50\times2.236\text{ mΩ} = $ **111.8 mV**, or **13.98%** of the rail against the 5% allowed. The network resonates at $f_0 = 1/\big(2\pi\sqrt{LC}\big) = $ **71.18 MHz**.

(c) To make $\sqrt{L/C} = Z_t$: with $L = 5$ pH, $C = L/Z_t^2 = $ **7.813 µF**; with $C = 1$ µF, $L = Z_t^2C = $ **0.64 pH**. Neither is easy, which is why high-current processors combine more on-die and in-package capacitance, many more power bumps (lower $L$), and voltage regulation inside the package.

### Solution 02-03.15

(a) α = $R/(2L) = -2/(2\times10^{-3}) = -1000$ s⁻¹, so $s = 1000 \pm j9950$ s⁻¹, with $\omega_d = \sqrt{10^8 - 10^6} = 9950$ rad/s. The roots lie in the **right half-plane**: the system is unstable.

(b) $f = 9950/2\pi = $ **1584 Hz**. The envelope grows as $e^{1000t}$, with time constant **1.000 ms**.

(c) $e^{1000t} = 1000$ gives $t = \ln1000/1000 = $ **6.908 ms**, which is $6.908\text{ ms}\times1584\text{ Hz} = $ **10.94** cycles.

(d) A net resistance of **zero** puts the roots on the imaginary axis, giving a steady sinusoid. In a real oscillator the active device's negative resistance weakens as the amplitude grows (its gain compresses), so the amplitude rises until the net resistance averages to zero, then holds: nonlinearity, not linear theory, sets the final amplitude ([12-09](../../12-electronics-2/chapters/12-09-oscillators.md)).

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 02-03.1a | α, series | 2500 | 1/s |
| 02-03.1b | ω0, series and parallel | 1.000×10^4 | rad/s |
| 02-03.1c | ζ, series | 0.25 | — |
| 02-03.1d | α, parallel | 500 | 1/s |
| 02-03.1e | ζ, parallel | 0.05 | — |
| 02-03.1f | ω0, mass–spring | 20 | rad/s |
| 02-03.1g | α, mass–spring | 5 | 1/s |
| 02-03.1h | ζ, mass–spring | 0.25 | — |
| 02-03.2a | ω0 for (c) | 3.162 | — |
| 02-03.2b | ζ for (c) | 0.3162 | — |
| 02-03.3a | y(1) | 0.3064 | — |
| 02-03.4a | exact s1/ω0 at ζ = 5 | −0.1010 | — |
| 02-03.4b | relative error of the approximation | 1.0 | % |
| 02-03.5a | y(1) | 0.6767 | — |
| 02-03.6a | ω0·t for 90 % | 3.890 | — |
| 02-03.6b | time to 90 % | 389.0 | µs |
| 02-03.7a | ωd | 953.9 | rad/s |
| 02-03.7b | peak time | 3.293 | ms |
| 02-03.7c | overshoot | 37.23 | % |
| 02-03.8a | α | 1000 | 1/s |
| 02-03.8b | ω0 | 1.000×10^4 | rad/s |
| 02-03.8c | ωd | 9950 | rad/s |
| 02-03.8d | initial slope of v_C | 1.000×10^5 | V/s |
| 02-03.8e | sine amplitude B | 10.05 | V |
| 02-03.8f | time of first peak | 147.8 | µs |
| 02-03.8g | first peak of v_C | 8.626 | V |
| 02-03.8h | capacitor energy at the peak | 0.3720 | mJ |
| 02-03.8i | fraction of initial energy | 74.41 | % |
| 02-03.9a | α | 2500 | 1/s |
| 02-03.9b | ζ | 0.25 | — |
| 02-03.9c | ωd | 9682 | rad/s |
| 02-03.9d | v′(0) | −5.000×10^4 | V/s |
| 02-03.9e | sine coefficient B | −2.582 | V |
| 02-03.10a | Wronskian (c) at t = 0 | 3 | — |
| 02-03.11a | ζ | 0.5912 | — |
| 02-03.11b | ωd | 62.83 | krad/s |
| 02-03.11c | ω0 | 77.90 | krad/s |
| 02-03.11d | Q | 0.8458 | — |
| 02-03.12a | ω0 | 316.2 | krad/s |
| 02-03.12b | Q | 63.25 | — |
| 02-03.12c | cycles to fall by e | 20.13 | — |
| 02-03.12d | energy lost per cycle, exact | 9.457 | % |
| 02-03.12e | estimate 2π/Q | 9.935 | % |
| 02-03.13a | ω0 | 1.581×10^10 | rad/s |
| 02-03.13b | f0 | 2.516 | GHz |
| 02-03.13c | ζ | 0.1581 | — |
| 02-03.13d | overshoot | 60.47 | % |
| 02-03.13e | resistance for ζ = 0.7 | 44.27 | Ω |
| 02-03.13f | overshoot at ζ = 0.7 | 4.60 | % |
| 02-03.14a | target impedance | 0.8 | mΩ |
| 02-03.14b | characteristic impedance | 2.236 | mΩ |
| 02-03.14c | first droop | 111.8 | mV |
| 02-03.14d | droop as % of the rail | 13.98 | % |
| 02-03.14e | resonant frequency | 71.18 | MHz |
| 02-03.14f | capacitance to meet the target | 7.813 | µF |
| 02-03.14g | inductance to meet the target | 0.64 | pH |
| 02-03.15a | oscillation frequency | 1584 | Hz |
| 02-03.15b | envelope time constant | 1.000 | ms |
| 02-03.15c | time to grow 1000-fold | 6.908 | ms |
| 02-03.15d | cycles to grow 1000-fold | 10.94 | — |
