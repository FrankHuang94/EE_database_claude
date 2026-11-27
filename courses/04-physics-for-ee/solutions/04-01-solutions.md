# Solutions 04-01 · Mechanics Essentials for EE

Problems: [04-01 problems](../problems/04-01-problems.md) · Chapter: [04-01](../chapters/04-01-mechanics-essentials.md). Every number below is recomputed by [verify_04_01.py](../verify/verify_04_01.py).

---

## Solutions

### Solution 04-01.1

(a) J/C = (W·s)/(A·s) = W/A = V. In base units, $\Omega = \text{V/A} = \text{W/A}^2 = (\text{kg·m}^2/\text{s}^3)/\text{A}^2 = \text{kg·m}^2/(\text{s}^3\text{·A}^2)$.

(b) $L$ is V·s/A (from $v = L\,di/dt$), so $Li^2$ has units (V·s/A)·A² = V·A·s = W·s = J. $L/R$ = (V·s/A)/(V/A) = s.

(c) $at^3$ has units (m/s²)·s³ = m·s, not m. The correct form is $x = \tfrac12at^2$, whose units are (m/s²)·s² = m.

### Solution 04-01.2

(a) $3.6\times10^6\text{ J}/1.602176634\times10^{-19}\text{ J/eV} = $ **2.247×10²⁵ eV**.

(b) $75\times3600 = $ **270 kJ**.

(c) $2.5\times9.80665 = $ **24.52 m/s²**.

(d) $1.12\times1.602176634\times10^{-19} = $ **1.794×10⁻¹⁹ J**.

### Solution 04-01.3

(a) Suppose the period is $L^\alpha g^\beta m^\gamma$. Units: $\text{m}^\alpha(\text{m/s}^2)^\beta\text{kg}^\gamma = \text{s}$. Matching kg gives γ = 0; matching s gives $-2\beta = 1$, so β = −1/2; matching m gives $\alpha + \beta = 0$, so α = 1/2. The period is a constant times $\sqrt{L/g}$, and the mass cannot appear because nothing else carries kilograms to cancel it.

(b) $2\pi\sqrt{1/9.80665} = $ **2.006 s**.

### Solution 04-01.4

The accelerometer reads the floor's upward push per unit mass, $a + g$ (upward positive), where $a$ is the elevator's acceleration.

(a) $9.80665 + 2 = $ **11.81 m/s²**, or **1.204 *g***.

(b) Slowing while moving upward means $a = -1.5$ m/s²: \$9.80665 - 1.5 = \$ **8.307 m/s²**, or **0.8470 *g***.

(c) In free fall the floor exerts no force: **0**.

(d) The proof mass responds to the net force from its spring, which depends only on $a + g$. A larger $g$ at rest and an upward acceleration in weaker gravity produce the same push. (This is Einstein's equivalence principle; it is why inertial navigation needs a gravity model.)

### Solution 04-01.5

(a) $U = \tfrac12k_sx^2 = \tfrac12\times200\times0.05^2 = $ **0.25 J**.

(b) $\tfrac12mv^2 = 0.25$ J gives \$v = \sqrt{2\times0.25/0.02} = \$ **5 m/s** (equivalently $x\sqrt{k_s/m}$).

(c) $v = \sqrt{2\times0.9\times0.25/0.02} = $ **4.743 m/s**.

### Solution 04-01.6

(a) At constant speed the hoist force equals the weight: $P = mgv = 1000\times9.80665\times2 = $ **19.61 kW**.

(b) The counterweight's descent supplies $800\times9.80665\times2$ W, so the hoist supplies only the imbalance: \$200\times9.80665\times2 = \$ **3.923 kW**.

(c) $3922.66/0.85 = $ **4.615 kW**. A counterweight cuts the motor power fivefold, which is why every traction elevator has one.

### Solution 04-01.7

(a) Momentum: $2\times3 = (2 + 1)v_f$, so \$v_f = \$ **2 m/s**.

(b) Before: $\tfrac12\times2\times3^2 = $ **9 J**. After: $\tfrac12\times3\times2^2 = $ **6 J**. Lost: **3 J**, **33.33%**.

(c) Into heat, sound and permanent deformation of the coupling. Momentum is conserved because the forces between the carts are an action–reaction pair (third law) and cancel in the total; no external horizontal force acts.

### Solution 04-01.8

(a) $I = \tfrac12mR^2 = \tfrac12\times100\times0.3^2 = $ **4.5 kg·m²**. $\omega = 2\pi\times20{,}000/60 = $ **2094 rad/s**. $E = \tfrac12I\omega^2 = $ **9.870 MJ**, or **2.742 kWh**.

(b) $9.870\times10^6/50{,}000 = $ **197.4 s**.

(c) Energy scales as $\omega^2$: at half speed a quarter remains, so **75%** has been delivered. Flywheels deliver most of their energy over a modest speed range, which suits uninterruptible power supplies that ride through short outages.

### Solution 04-01.9

(a) $\omega_0 = \sqrt{200/0.5} = $ **20 rad/s**, $f_0 = $ **3.183 Hz**, period $2\pi/20 = $ **0.3142 s**.

(b) $v_{\max} = A\omega_0 = 0.03\times20 = $ **0.6 m/s**; $a_{\max} = A\omega_0^2 = $ **12 m/s²**.

(c) \$\tfrac12k_sA^2 = \tfrac12\times200\times0.03^2 = \$ **0.09 J** (equal to $\tfrac12mv_{\max}^2 = \tfrac12\times0.5\times0.36$ ✓).

### Solution 04-01.10

(a) 500 cycles at 100 kHz take 5 ms. $e^{-\alpha\times0.005} = \tfrac12$ gives \$\alpha = \ln2/0.005 = \$ **138.6 s⁻¹**.

(b) $Q = \omega_0/(2\alpha) = 2\pi\times10^5/(2\times138.63) = $ **2266**.

(c) The amplitude halves in 500 cycles, so the energy falls to a quarter: the fraction lost per cycle is exactly $1 - 4^{-1/500} = 1 - e^{-2\alpha/f_0}$ = **0.2769%**. The light-damping formula $2\pi/Q$ gives 0.2773%, the same to 0.15%.

(d) $f_0/Q = $ **44.13 Hz**.

### Solution 04-01.11

(a) In series the springs carry the same force and their stretches add: $1/k = 1/100 + 1/300$, so \$k = \$ **75 N/m**. In parallel they share one stretch and their forces add: \$k = \$ **400 N/m**.

(b) Each spring is a capacitance $C = 1/k_s$: 0.01 F and 3.333 mF. Springs in series share one force, which maps to one voltage, so the capacitors are in **parallel**: \$0.01 + 0.003333 = \$ **0.01333 F** = 1/75 ✓. Springs in parallel share one velocity, which maps to one current, so their capacitors are in series: $1/(100 + 300)$ F. The force–voltage analogy inverts series and parallel for springs.

### Solution 04-01.12

(a) $x/g = 9.80665/(2\pi f_0)^2$: **248.4 nm** at 1 kHz, **15.53 nm** at 4 kHz, **0.9703 nm** at 16 kHz.

(b) With $Q = 1/\sqrt2$, the −3 dB bandwidth equals $f_0$: 1, 4 and 16 kHz.

(c) $0.9703\text{ nm}/1000 = $ **0.9703 pm**, about 1/240 of the 0.235 nm Si–Si bond length: wide-bandwidth sensors need extraordinary readout resolution.

### Solution 04-01.13

(a) From $a_n^2 = 4kT\omega_0/(mQ)$: $m = 4kT\omega_0/(Qa_n^2)$. With $a_n = 20\times10^{-6}\times9.80665 = 1.961\times10^{-4}$ m/s²/√Hz and $\omega_0 = 2\pi\times2000$:

$$
m = \frac{4\times1.380649\times10^{-23}\times300\times12{,}566.4}{2\times(1.961\times10^{-4})^2} = 2.706\times10^{-9}\ \text{kg} .
$$

So **2.706 µg**.

(b) $k_s = m\omega_0^2 = $ **0.4273 N/m**; deflection per *g* $= g/\omega_0^2 = $ **62.10 nm**.

(c) $a_n \propto 1/\sqrt Q$: the floor falls by \$\sqrt{1000/2} = \$ **22.36**. But a Q of 1000 makes the sensor ring for about 1000/π ≈ 300 cycles after every bump and peaks its response 1000-fold at resonance; the design then needs closed-loop (force-feedback) control or electronic damping.

### Solution 04-01.14

(a) The displacement responds to force through $H(\omega) = 1/(k_s - m\omega^2 + jb\omega)$, so $\overline{x^2} = \int_0^\infty G_F|H(2\pi f)|^2\,df$.

(b) With $df = d\omega/(2\pi)$: $\overline{x^2} = \frac{G_F}{2\pi}\int_0^\infty\frac{d\omega}{(k_s - m\omega^2)^2 + b^2\omega^2} = \frac{G_F}{2\pi}\cdot\frac{\pi}{2k_sb} = \frac{G_F}{4k_sb}$.

(c) $\tfrac12k_s\cdot G_F/(4k_sb) = \tfrac12kT$ gives $G_F = 4kTb$: the damper's force noise, the mechanical twin of $4kTR$.

(d) $\sqrt{kT/k_s}$: **64.36 pm** for 1 N/m and **2.035 pm** for 1000 N/m. The mass does not appear because equipartition fixes the spring's average energy at $\tfrac12kT$ whatever the mass; mass and damping only shape the noise spectrum, as R did for kT/C.

### Solution 04-01.15

(a) $v = \sqrt{2\times9.80665\times1.2} = $ **4.851 m/s**.

(b) $a_{\text{pk}} = (\pi/2)v/\Delta t \le 1500\times9.80665 = 14{,}710$ m/s², so \$\Delta t \ge (\pi/2)\times4.851/14{,}710 = \$ **0.5181 ms**.

(c) For $a = a_{\text{pk}}\sin(\pi t/\Delta t)$ with $v(0) = v_0 = 2a_{\text{pk}}\Delta t/\pi$, integrating gives $v(t) = (a_{\text{pk}}\Delta t/\pi)\big(1 + \cos(\pi t/\Delta t)\big)$, and integrating again over $[0, \Delta t]$ gives the stopping distance $a_{\text{pk}}\Delta t^2/\pi = v_0\Delta t/2$. Here \$4.851\times0.0005181/2 = \$ **1.257 mm**: the cushioning must compress at least that much while decelerating the device smoothly.

### Solution 04-01.16

(a) At −10 °C: $-0.035\times(-35)^2 = $ **−42.88 ppm**. At 60 °C: $-0.035\times35^2 = $ **−42.88 ppm**: the parabola is symmetric about the turnover, and the crystal runs slow on both sides.

(b) \$42.875\times10^{-6}\times86{,}400 = \$ **3.704 s** per day; over a year, $42.875\times10^{-6}\times365.25\times86{,}400 = 1353$ s, or **22.55 min**.

(c) $-0.035\times7^2 = -1.715$ ppm; over 30 days, \$1.715\times10^{-6}\times30\times86{,}400 = \$ **4.445 s**.

(d) The error is systematic and quadratic in temperature, so it can be measured and cancelled: temperature-compensated oscillators measure the temperature and correct the frequency (or the count) electronically, holding a few ppm over a wide range. Wearables and phones also correct their clocks from the network.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 04-01.2a | 1 kWh | 2.247×10^25 | eV |
| 04-01.2b | 75 Wh | 270 | kJ |
| 04-01.2c | 2.5 g | 24.52 | m/s² |
| 04-01.2d | 1.12 eV | 1.794×10^-19 | J |
| 04-01.3a | pendulum period, 1 m | 2.006 | s |
| 04-01.4a | reading, accelerating up | 11.81 | m/s² |
| 04-01.4b | reading, accelerating up | 1.204 | g |
| 04-01.4c | reading, slowing upward | 8.307 | m/s² |
| 04-01.4d | reading, slowing upward | 0.8470 | g |
| 04-01.4e | reading in free fall | 0 | m/s² |
| 04-01.5a | spring energy | 0.25 | J |
| 04-01.5b | launch speed | 5 | m/s |
| 04-01.5c | speed with 10% loss | 4.743 | m/s |
| 04-01.6a | hoist power, no counterweight | 19.61 | kW |
| 04-01.6b | hoist power, counterweight | 3.923 | kW |
| 04-01.6c | electrical input | 4.615 | kW |
| 04-01.7a | final speed | 2 | m/s |
| 04-01.7b | kinetic energy before | 9 | J |
| 04-01.7c | kinetic energy after | 6 | J |
| 04-01.7d | energy lost | 3 | J |
| 04-01.7e | fraction lost | 33.33 | % |
| 04-01.8a | moment of inertia | 4.5 | kg·m² |
| 04-01.8b | angular speed | 2094 | rad/s |
| 04-01.8c | stored energy | 9.870 | MJ |
| 04-01.8d | stored energy | 2.742 | kWh |
| 04-01.8e | run time at 50 kW | 197.4 | s |
| 04-01.8f | energy delivered at half speed | 75 | % |
| 04-01.9a | angular frequency | 20 | rad/s |
| 04-01.9b | frequency | 3.183 | Hz |
| 04-01.9c | period | 0.3142 | s |
| 04-01.9d | maximum speed | 0.6 | m/s |
| 04-01.9e | maximum acceleration | 12 | m/s² |
| 04-01.9f | total energy | 0.09 | J |
| 04-01.10a | decay rate | 138.6 | 1/s |
| 04-01.10b | quality factor | 2266 | — |
| 04-01.10c | energy lost per cycle | 0.2769 | % |
| 04-01.10d | half-power bandwidth | 44.13 | Hz |
| 04-01.11a | springs in series | 75 | N/m |
| 04-01.11b | springs in parallel | 400 | N/m |
| 04-01.11c | parallel capacitance for the series springs | 0.01333 | F |
| 04-01.12a | deflection per g, 1 kHz | 248.4 | nm |
| 04-01.12b | deflection per g, 4 kHz | 15.53 | nm |
| 04-01.12c | deflection per g, 16 kHz | 0.9703 | nm |
| 04-01.12d | deflection per mg, 16 kHz | 0.9703 | pm |
| 04-01.13a | noise target | 1.961×10^-4 | m/s²/√Hz |
| 04-01.13b | minimum proof mass | 2.706 | µg |
| 04-01.13c | spring constant | 0.4273 | N/m |
| 04-01.13d | deflection per g | 62.10 | nm |
| 04-01.13e | noise reduction in vacuum | 22.36 | — |
| 04-01.14a | rms thermal motion, 1 N/m | 64.36 | pm |
| 04-01.14b | rms thermal motion, 1000 N/m | 2.035 | pm |
| 04-01.15a | impact speed | 4.851 | m/s |
| 04-01.15b | shortest pulse | 0.5181 | ms |
| 04-01.15c | stopping distance | 1.257 | mm |
| 04-01.16a | error at −10 °C | −42.88 | ppm |
| 04-01.16b | error at 60 °C | −42.88 | ppm |
| 04-01.16c | loss per day at −10 °C | 3.704 | s |
| 04-01.16d | loss per year at −10 °C | 22.55 | min |
| 04-01.16e | error at 32 °C | −1.715 | ppm |
| 04-01.16f | loss in 30 days at 32 °C | 4.445 | s |
