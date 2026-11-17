# Solutions 02-04 · Forced Response and Resonance

Problems: [02-04 problems](../problems/02-04-problems.md) · Chapter: [02-04](../chapters/02-04-forced-response-and-resonance.md)

Every numerical answer below is listed in the answer key at the end and is recomputed independently by [verify_02_04.py](../verify/verify_02_04.py).

---

## Solutions

### Solution 02-04.1

The homogeneous roots decide when the duplication rule applies.

(a) Roots ±2j. A quadratic input needs a full quadratic: $y_p = At^2 + Bt + C$.
(b) $e^{2t}$ is not a homogeneous solution: $y_p = Ae^{2t}$.
(c) $\sin2t$ *is* a homogeneous solution (roots ±2j): $y_p = t(A\cos2t + B\sin2t)$.
(d) $s^2 - 2s + 1 = (s - 1)^2$: a double root at 1, so both $e^t$ and $te^t$ are homogeneous: $y_p = At^2e^t$.
(e) Roots $-1 \pm 2j$, so $e^{-t}\cos2t$ is homogeneous: $y_p = te^{-t}(A\cos2t + B\sin2t)$.

### Solution 02-04.2

A constant guess gives $4y_p = 8$, so $y_p = 2$. Then $y = 2 + c_1\cos2t + c_2\sin2t$; $y(0) = 0$ gives $c_1 = -2$ and $y'(0) = 0$ gives $c_2 = 0$:

$$
y(t) = 2 - 2\cos2t .
$$

The largest value is **4**, first at $2t = \pi$, $t = $ **1.571**. With no damping, ζ = 0 and the overshoot formula of 02-03 gives $e^{0} = 1$, that is, 100%: nothing removes the energy that carried the system past its new equilibrium, so it swings as far beyond as it started below.

### Solution 02-04.3

$p(s) = s^2 + 2s + 5$, and $p(-3) = 9 - 6 + 5 = 8 \ne 0$, so $y_p = 10e^{-3t}/8 = $ **1.25** $e^{-3t}$.

### Solution 02-04.4

$p(j) = (j)^2 + 2j + 5 = 4 + 2j$. The steady state is $\operatorname{Re}\big[e^{jt}/(4 + 2j)\big] = \frac{1}{\lvert4 + 2j\rvert}\cos\big(t - \angle(4 + 2j)\big)$: amplitude $1/\sqrt{20} = $ **0.2236**, phase $-\arctan(2/4) = $ **−26.57°**.

### Solution 02-04.5

(a) $p(s) = s^2 + 9$ has roots $\pm3j$, so the input is resonant. With $p'(3j) = 6j$, the resonant response formula gives $y_p = \operatorname{Re}\big[6te^{j3t}/(6j)\big] = \operatorname{Re}\big[-jt(\cos3t + j\sin3t)\big] = t\sin3t$. The envelope at $t = 4$ is **4**, growing linearly.

(b) $p(s) = s^2 - s - 2 = (s - 2)(s + 1)$ has a simple root at 2, and $p'(2) = 2(2) - 1 = 3$. So $y_p = \dfrac{te^{2t}}{3}$. **Check:** with $y = te^{2t}/3$, $y' = (1 + 2t)e^{2t}/3$ and $y'' = (4 + 4t)e^{2t}/3$, so $y'' - y' - 2y = \frac{e^{2t}}{3}(4 + 4t - 1 - 2t - 2t) = e^{2t}$ ✓.

### Solution 02-04.6

$p(j) = -1 + 3j + 2 = 1 + 3j$, so $y_p = \operatorname{Re}\big[10e^{jt}/(1 + 3j)\big] = \operatorname{Re}\big[(1 - 3j)(\cos t + j\sin t)\big] = \cos t + 3\sin t$, with amplitude $\sqrt{10} = $ **3.162**. The total is $y = c_1e^{-t} + c_2e^{-2t} + \cos t + 3\sin t$. The initial conditions give $c_1 + c_2 + 1 = 0$ and $-c_1 - 2c_2 + 3 = 0$, so $c_2 = 4$ and $c_1 = -5$:

$$
y(t) = \underbrace{-5e^{-t} + 4e^{-2t}}_{\text{transient}} + \underbrace{\cos t + 3\sin t}_{\text{steady state}}, \qquad y(1) = 1.767 .
$$

### Solution 02-04.7

(a) $r_{peak} = \sqrt{1 - 2(0.01)} = $ **0.9899**, and the peak is $1/\big(0.2\sqrt{0.99}\big) = $ **5.025**, or **14.02 dB**.

(b) At $r = 1$, $\lvert H\rvert = 1/(2\zeta) = Q = $ **5**: just below the peak, as expected for light damping.

(c) $H(10) = 1/(1 - 100 + j2) $, with magnitude **0.01010**, or **−39.91 dB**, within 0.1 dB of the −40 dB asymptote.

### Solution 02-04.8

(a) $\omega_0 = 1/\sqrt{10^{-3}\times10^{-8}} = $ **316.2 krad/s**, $f_0 = $ **50.33 kHz**, and $Q = \omega_0L/R = 316.2/10 = $ **31.62**.

(b) Bandwidth $f_0/Q = $ **1.592 kHz**. From chapter §3.5, $f_{1,2} = f_0\big(\sqrt{1 + 1/(4Q^2)} \mp 1/(2Q)\big)$ = **49.54 kHz** and **51.13 kHz**.

(c) $49.540\times51.131 = 2533.0$ kHz², and $f_0^2 = 50.329^2 = 2533.0$ kHz² ✓: the band is centered geometrically.

### Solution 02-04.9

(a) $\omega_0 = 1/\sqrt{10^{-4}\times10^{-9}} = $ **3.162 Mrad/s**, $f_0 = $ **503.3 kHz**, and $Q = R\sqrt{C/L} = 10^4\sqrt{10^{-5}} = $ **31.62**.

(b) At resonance the inductor's and capacitor's admittances cancel, so the tank looks like $R$ alone: $V = 1\text{ mA}\times10\text{ kΩ} = $ **10 V** (peak). The capacitor current is $\omega_0CV = 3.162\times10^6\times10^{-9}\times10 = $ **31.62 mA**, which is $Q$ times the source current. The inductor carries an equal current in the opposite phase. The energy circulates between L and C, and the source only replaces what the resistor dissipates, so the circulating current can far exceed the source's.

### Solution 02-04.10

(a) $\cos A + \cos B = 2\cos\frac{A + B}{2}\cos\frac{A - B}{2}$, so the sum is $2\cos(2\pi\cdot441t)\cos(2\pi\cdot1\cdot t)$.

(b) You hear a pitch of **441 Hz** whose loudness follows $\lvert\cos(2\pi t)\rvert$, which peaks **2** times per second: the beat rate equals the difference frequency, 442 − 440 Hz.

### Solution 02-04.11

(a) With $y_1 = \cos t$, $y_2 = \sin t$ and $W = \cos^2t + \sin^2t = 1$: $u_1' = -\sin t\sec t = -\tan t$, so $u_1 = \ln(\cos t)$ (cos t > 0 on the interval); $u_2' = \cos t\sec t = 1$, so $u_2 = t$. Hence $y_p = \cos t\ln(\cos t) + t\sin t$, and $y_p(\pi/4) = 0.7071\times\ln0.7071 + 0.7854\times0.7071 = $ **0.3103**.

(b) $u_1' = -\sin t\tan t = -\dfrac{\sin^2t}{\cos t} = -\sec t + \cos t$, so $u_1 = -\ln(\sec t + \tan t) + \sin t$. $u_2' = \cos t\tan t = \sin t$, so $u_2 = -\cos t$. Then

$$
y_p = \cos t\big(\sin t - \ln(\sec t + \tan t)\big) - \sin t\cos t = -\cos t\,\ln(\sec t + \tan t),
$$

and $y_p(\pi/4) = -0.7071\ln(1.4142 + 1) = $ **−0.6232**.

### Solution 02-04.12

(a) $\omega_0 = 1/\sqrt{10^{-3}\times10^{-6}} = 31.62$ krad/s, so $f_0 = $ **5.033 kHz**, and $Q = \omega_0L/R = 31.62/5 = $ **6.325**.

(b) At resonance the impedance is $R$: $I = 10/5 = $ **2 A** rms and $P = I^2R = $ **20 W**. The capacitor voltage is $I/(\omega_0C) = 2/(31\,623\times10^{-6}) = $ **63.25 V** rms, which is $Q$ times the source voltage.

(c) No. 63.25 V rms is 89.4 V peak, far above the 50 V rating, even though the source is only 10 V. Resonant circuits need components rated for $Q$ times the drive.

### Solution 02-04.13

(a) $f_0/Q = 25\,000/10\,000 = $ **2.5 Hz**.

(b) $1/\alpha = 2Q/\omega_0 = 2\times10^4/(2\pi\times25\,000) = $ **0.1273 s**, and 99% takes $\ln100/\alpha = $ **0.5863 s**.

(c) $1/\sqrt{1 + (2Q\Delta f/f_0)^2} = 1/\sqrt{1 + 0.8^2} = $ **0.7809**.

(d) The resonance shifts with temperature, packaging stress and manufacturing spread by far more than its 2.5 Hz bandwidth, so a fixed drive frequency would land on the skirt and lose amplitude (and sensitivity, which is proportional to the drive amplitude). A loop that measures the phase between drive and motion, and holds it at the resonant −90°, keeps the drive on the peak automatically.

### Solution 02-04.14

(a) Each harmonic is multiplied by $\lvert H_{BP}\rvert = 1/\sqrt{1 + Q^2(r - 1/r)^2}$ with $r = n/3$:

| $n$ | Input $4/(n\pi)$ (V) | $\lvert H_{BP}\rvert$ | Output (V) |
|---|---|---|---|
| 1 | 1.273 | 0.03747 | **0.04771** |
| 3 | 0.4244 | 1 | **0.4244** |
| 5 | 0.2546 | 0.09334 | **0.02377** |
| 7 | 0.1819 | 0.05243 | **0.009536** |

(b) The output is very nearly a 30 kHz sine of 0.4244 V amplitude: the circuit has *tripled* the frequency. The largest unwanted component, the 10 kHz fundamental, is **11.24%** of the wanted one (−18.98 dB).

(c) Higher $Q$ narrows the band, so the fundamental and the 5th harmonic are suppressed further (for large $Q$ their gains fall roughly as $1/Q$), at the cost of a slower build-up and more sensitivity to tuning errors.

### Solution 02-04.15

(a) The load sees the capacitor in parallel with the supply branch ($R$ in series with $L$, the regulator being an AC short):

$$
Z = \frac{R + j\omega L}{1 + j\omega C(R + j\omega L)} = \frac{R + j\omega L}{1 - \omega^2LC + j\omega RC}.
$$

At $\omega_0 = 1/\sqrt{LC}$ the real part of the denominator vanishes, so $Z = \dfrac{R + j\omega_0L}{j\omega_0RC} \approx \dfrac{j\omega_0L}{j\omega_0RC} = \dfrac{L}{RC}$ when $R \ll \omega_0L$. Since $Q = \sqrt{L/C}/R$, this is $Q\sqrt{L/C}$: the characteristic impedance multiplied by $Q$.

(b) $f_0 = $ **100.7 MHz**. At $f_0$, $\lvert Z\rvert = $ **250.5 mΩ** (the approximation gives 250 mΩ). At 50 MHz, $\lvert Z\rvert = $ **10.50 mΩ**. At DC it is just $R = $ **1.000 mΩ**.

(c) The ripple is $\lvert Z\rvert\times1$ A: **250.5 mV** at resonance, **10.50 mV** at 50 MHz and **1.000 mV** at DC. A workload whose activity oscillates at the PDN resonance pumps it like a swing, producing a ripple 250 times larger than the DC drop, enough to cause timing failures in some code loops and not others. Hardware teams damp and lower the impedance peak; some products also detect droop on the fly and stretch the clock, and validation teams write "power virus" tests that deliberately toggle at the resonance to find the worst case.

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 02-04.2a | maximum of y | 4 | — |
| 02-04.2b | time of the maximum | 1.571 | — |
| 02-04.3a | particular-solution coefficient | 1.25 | — |
| 02-04.4a | steady-state amplitude | 0.2236 | — |
| 02-04.4b | phase | −26.57 | ° |
| 02-04.5a | envelope at t = 4 | 4 | — |
| 02-04.5b | p′(2) | 3 | — |
| 02-04.6a | steady-state amplitude | 3.162 | — |
| 02-04.6b | c1 | −5 | — |
| 02-04.6c | c2 | 4 | — |
| 02-04.6d | y(1) | 1.767 | — |
| 02-04.7a | peak frequency ratio | 0.9899 | — |
| 02-04.7b | peak gain | 5.025 | — |
| 02-04.7c | peak gain in dB | 14.02 | dB |
| 02-04.7d | gain at r = 1 | 5 | — |
| 02-04.7e | gain at r = 10 | 0.01010 | — |
| 02-04.7f | gain at r = 10 in dB | −39.91 | dB |
| 02-04.8a | ω0 | 316.2 | krad/s |
| 02-04.8b | f0 | 50.33 | kHz |
| 02-04.8c | Q | 31.62 | — |
| 02-04.8d | bandwidth | 1.592 | kHz |
| 02-04.8e | lower half-power frequency | 49.54 | kHz |
| 02-04.8f | upper half-power frequency | 51.13 | kHz |
| 02-04.8g | product of the half-power frequencies | 2533.0 | kHz² |
| 02-04.9a | ω0 | 3.162 | Mrad/s |
| 02-04.9b | f0 | 503.3 | kHz |
| 02-04.9c | Q | 31.62 | — |
| 02-04.9d | tank voltage | 10 | V |
| 02-04.9e | capacitor current | 31.62 | mA |
| 02-04.10a | perceived pitch | 441 | Hz |
| 02-04.10b | loudness swells per second | 2 | — |
| 02-04.11a | y_p(π/4) for sec t | 0.3103 | — |
| 02-04.11b | y_p(π/4) for tan t | −0.6232 | — |
| 02-04.12a | f0 | 5.033 | kHz |
| 02-04.12b | Q | 6.325 | — |
| 02-04.12c | current | 2 | A |
| 02-04.12d | power | 20 | W |
| 02-04.12e | capacitor voltage, rms | 63.25 | V |
| 02-04.12f | capacitor voltage, peak | 89.4 | V |
| 02-04.13a | bandwidth | 2.5 | Hz |
| 02-04.13b | build-up time constant | 0.1273 | s |
| 02-04.13c | time to 99 % | 0.5863 | s |
| 02-04.13d | relative amplitude 1 Hz off | 0.7809 | — |
| 02-04.14a | 1st-harmonic output | 0.04771 | V |
| 02-04.14b | 3rd-harmonic output | 0.4244 | V |
| 02-04.14c | 5th-harmonic output | 0.02377 | V |
| 02-04.14d | 7th-harmonic output | 0.009536 | V |
| 02-04.14e | 1st-harmonic gain | 0.03747 | — |
| 02-04.14f | 5th-harmonic gain | 0.09334 | — |
| 02-04.14g | 7th-harmonic gain | 0.05243 | — |
| 02-04.14h | largest unwanted / wanted | 11.24 | % |
| 02-04.14i | the same in dB | −18.98 | dB |
| 02-04.14j | input fundamental amplitude 4/π | 1.273 | V |
| 02-04.14k | input 5th harmonic 4/(5π) | 0.2546 | V |
| 02-04.14l | input 7th harmonic 4/(7π) | 0.1819 | V |
| 02-04.15a | resonant frequency | 100.7 | MHz |
| 02-04.15b | impedance at f0 | 250.5 | mΩ |
| 02-04.15c | approximation L/(RC) | 250 | mΩ |
| 02-04.15d | impedance at 50 MHz | 10.50 | mΩ |
| 02-04.15e | impedance at DC | 1.000 | mΩ |
| 02-04.15f | ripple at f0 | 250.5 | mV |
| 02-04.15g | ripple at 50 MHz | 10.50 | mV |
| 02-04.15h | ripple at DC | 1.000 | mV |
