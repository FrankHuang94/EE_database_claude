# Solutions 07-01 · Capacitors and Inductors

Problems: [07-01 problems](../problems/07-01-problems.md) · Chapter: [07-01](../chapters/07-01-capacitors-and-inductors.md). Every number below is recomputed by [verify_07_01.py](../verify/verify_07_01.py); the circuits of Problems 07-01.3, 07-01.6, 07-01.7, 07-01.11 and 07-01.14 are also confirmed in ngspice ([lab netlist](../labs/07-01-lab/storage.cir)).

---

## Solutions

### Solution 07-01.1

$i = C\,dv/dt = 47\ \text{µF}\times5\times2\pi\cdot50\cos(2\pi\cdot50\,t)$, so $i(t) = 73.83\cos(2\pi\cdot50\,t)$ mA, with peak **73.83 mA**. The current peaks when the voltage crosses zero (where its slope is steepest), a quarter period ahead of the voltage: the 90° lead of 07-05. The largest stored energy is at the voltage peak: \$\tfrac12\times47\ \text{µF}\times5^2 = \$ **587.5 µJ**.

### Solution 07-01.2

$v = L\,di/dt = 10\ \text{mH}\times(2/\tau)e^{-t/\tau} = 20e^{-t/\tau}$ V. At $0^+$: **20 V**; at 1 ms: \$20e^{-1} = \$ **7.358 V**. Final energy: \$\tfrac12\times10\ \text{mH}\times2^2 = \$ **20 mJ**. The voltage jumps from 0 to 20 V at $t = 0$ while the current starts smoothly from zero, as continuity allows.

### Solution 07-01.3

$\Delta v = \frac1C\int i\,dt$. First interval: $10\ \text{mA}\times30\ \text{ms}/100\ \text{µF} = 3$ V, so **5 V**. Second: $-5\ \text{mA}\times20\ \text{ms}/100\ \text{µF} = -1$ V, so **4 V**. The voltage is the running total of the charge delivered.

### Solution 07-01.4

(a) $3\parallel6 = 2$ mH (inductors in parallel combine reciprocally), plus 2 mH in series: **4 mH**.

(b) $6$ µF in series with $3$ µF is $6\times3/9 = 2$ µF (series capacitors combine reciprocally), in parallel with 3 µF: **5 µF**.

### Solution 07-01.5

(a) Both carry the same charge $q = C_{ser}\times9$ V with $C_{ser} = 2/3$ µF, so $q = 6$ µC: **6 V** across the 1 µF and **3 V** across the 2 µF. The smaller capacitor takes the larger voltage.

(b) After a long time no current flows in the capacitors, and the two equal leakage resistances form a resistive divider: **4.5 V** each. The capacitive division holds only while charges stay put; leakage slowly redistributes them until the resistors decide. High-voltage capacitor stacks add balancing resistors for exactly this reason.

### Solution 07-01.6

Charge is conserved: $4.7\times12 = 56.4$ µC shared by 6.9 µF gives **8.174 V**. Energy before: \$\tfrac12\times4.7\times144 = \$ **338.4 µJ**; after: \$\tfrac12\times6.9\times8.174^2 = \$ **230.5 µJ**; lost: **107.9 µJ**, which equals $\tfrac12\frac{C_1C_2}{C_1 + C_2}(\Delta V)^2$. The loss does **not** depend on the resistor: a smaller resistor gives a larger, shorter current pulse that dissipates the same energy (04-04).

### Solution 07-01.7

(a) In steady state the inductor's volt-seconds sum to zero over a period: $8.7\,D = 3.3\,(1 - D)$, so \$D = 3.3/12 = \$ **0.275**, which is just the ratio of output to input voltage.

(b) $T = 1/500\ \text{kHz} = 2$ µs, so the on-time is **0.55 µs**, and the ripple is \$\Delta i = v\,\Delta t/L = 8.7\times0.55/10 = \$ **0.4785 A** peak to peak (the same fall occurs during the off-time, $3.3\times1.45/10$).

### Solution 07-01.8

(a) $|v| = L\,\Delta i/\Delta t = 0.05\times0.5/10^{-5} = $ **2500 V**.

(b) $\tfrac12Li^2 = \tfrac12\times0.05\times0.25 = $ **6.25 mJ**.

(c) With $-30$ V across the coil, $di/dt = -30/0.05 = -600$ A/s, so the current reaches zero after \$0.5/600 = \$ **0.833 ms**. A plain flyback diode clamps at about −0.7 V, so the current would decay far more slowly (limited mainly by the coil's own resistance), and a solenoid or relay would release late. A higher clamp voltage removes the energy faster, at the price of a higher voltage on the switch: here the supply plus 30 V.

### Solution 07-01.9

(a) \$C \ge \Delta I\,\Delta t/\Delta v = 5\times50\ \text{ns}/30\ \text{mV} = \$ **8.333 µF**. Each capacitor offers $0.35\times22 = 7.7$ µF, so **2** capacitors suffice for charge.

(b) The spike is $L\,di/dt$ with $di/dt = 5\ \text{A}/2\ \text{ns}$: \$L \le 20\ \text{mV}\times2\ \text{ns}/5\ \text{A} = \$ **8 pH** in total. With 0.3 nH each, $N \ge 300/8 = 37.5$, so **38** capacitors.

(c) The inductance requirement, by a factor of 19. In practice 8 pH is barely achievable on a board at all: the fastest edges are supplied by capacitance inside the package and on the die, with the board's capacitors covering the slower part of the transient.

### Solution 07-01.10

$f_{SR} = 1/(2\pi\sqrt{0.4\ \text{nH}\times100\ \text{nF}}) = $ **25.16 MHz**. At 1 GHz the inductive term dominates: $|Z| \approx 2\pi fL - 1/(2\pi fC) = 2.513 - 0.0016 = $ **2.512 Ω**. **No**: at 1 GHz the part is an inductor of 0.4 nH. Smaller packages and capacitance closer to the load (in the package or on the die) are the cure at such frequencies.

### Solution 07-01.11

(a) $v_{out} = -\frac{1}{RC}\int v_{in}\,dt = -\frac{0.5\times2}{10^5\times10^{-6}} = $ **−10 V**.

(b) The 1 mV offset integrates at $10^{-3}/0.1 = 0.01$ V/s: **−0.1 V** after 10 s (the sign depends on the offset's), and the −12 V rail after \$12/0.01 = \$ **1200 s**. A practical integrator therefore needs a reset switch, a resistor across $C$, or an outer feedback loop (07-02).

### Solution 07-01.12

(a) $v = L\,di/dt = 10^{-3}\times2\omega\cos\omega t$ with $\omega = 2\pi\times1000$: peak \$2\times10^{-3}\times6283 = \$ **12.57 V**, leading the current by 90°.

(b) $p = vi = L\omega I^2\sin\omega t\cos\omega t = \tfrac12L\omega I^2\sin2\omega t$: peak \$\tfrac12\times10^{-3}\times6283\times4 = \$ **12.57 W**, average **0**, at **2 kHz**, twice the current's frequency.

(c) \$\tfrac12Li_{peak}^2 = \tfrac12\times10^{-3}\times4 = \$ **2 mJ**. While $|i|$ rises, power flows in and the energy grows; while $|i|$ falls, the same energy flows back to the source. Twice per cycle the inductor fills and empties, so the average power is zero; only resistance consumes power on average (07-06).

### Solution 07-01.13

(a) Without saturation, $\Delta i = 8.7\times1\ \text{µs}/10\ \text{µH} = 0.87$ A, so the current would end at **3.37 A**.

(b) Reaching 3 A takes \$0.5\times10\ \text{µH}/8.7 = \$ **0.5747 µs**. For the remaining 0.4253 µs the inductance is 2 µH, so the current rises a further $8.7\times0.4253/2 = 1.85$ A, ending at **4.85 A**, 44% above the unsaturated value.

(c) Once the core saturates, the current rises five times faster. Unless the controller limits the current cycle by cycle, the switch sees far more than its design current and can fail; this is why converters specify inductors by saturation current and use current-mode control (Course 22).

### Solution 07-01.14

At DC the capacitor is an open circuit and the inductor a short, so the source drives 2 kΩ and 4 kΩ in series: $i_L = 12/6 = $ **2 mA**, and the capacitor sits at node a, $v_C = 2\ \text{mA}\times4\ \text{kΩ} = $ **8 V**. Energies: $\tfrac12\times1\ \text{µF}\times64 = $ **32 µJ** and $\tfrac12\times10\ \text{mH}\times(2\ \text{mA})^2 = $ **20 nJ**.

### Solution 07-01.15

(a) In series, $C_{eq} = (1/2 + 1/3)^{-1}$ µF = **1.2 µF**. Series aiding, the terminal voltage is the sum, \$5 + 2 = \$ **7 V**.

(b) The two capacitors store $\tfrac12(2\ \mu\text{F})(5^2) + \tfrac12(3\ \mu\text{F})(2^2) = 25 + 6 = $ **31 µJ**. The equivalent capacitor at 7 V would store $\tfrac12(1.2\ \mu\text{F})(7^2) = $ **29.4 µJ**.

(c) Seen from the resistor, the pair behaves as 1.2 µF at 7 V, so the terminal voltage decays as $7e^{-t/\tau}$ with \$\tau = RC_{eq} = 10\ \text{k}\Omega\times1.2\ \mu\text{F} = \$ **12 ms**, to zero. The same current flows through both capacitors, so each loses the same charge, $Q = C_{eq}\times7\ \text{V} = 8.4$ µC. Their final voltages are:

- 2 µF: $5 - 8.4/2 = $ **0.8 V**;
- 3 µF: $2 - 8.4/3 = $ **−0.8 V**.

The terminal voltage is $0.8 - 0.8 = 0$, as it must be, but neither capacitor is empty.

(d) The resistor dissipates \$\int i^2R\,dt = \tfrac12C_{eq}(7^2) = \$ **29.4 µJ**, the equivalent capacitor's energy. The capacitors keep \$\tfrac12(2\ \mu\text{F})(0.8^2) + \tfrac12(3\ \mu\text{F})(0.8^2) = 0.64 + 0.96 = \$ **1.6 µJ**, exactly the difference $31 - 29.4$.

The series combination is defined by the terminal relation $i = C_{eq}\,dv/dt$. Any charge distribution with the same terminal voltage looks the same from outside. The energy trapped by the mismatch between the two capacitors' charges is invisible at the terminals and cannot be extracted through them. That is why series-connected cells or capacitors in a battery or supercapacitor stack need balancing.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 07-01.1a | peak current | 73.83 | mA |
| 07-01.1b | largest stored energy | 587.5 | µJ |
| 07-01.2a | voltage at 0+ | 20 | V |
| 07-01.2b | voltage at 1 ms | 7.358 | V |
| 07-01.2c | final energy | 20 | mJ |
| 07-01.3a | voltage after 30 ms | 5 | V |
| 07-01.3b | voltage after 50 ms | 4 | V |
| 07-01.4a | equivalent inductance | 4 | mH |
| 07-01.4b | equivalent capacitance | 5 | µF |
| 07-01.5a | voltage across 1 µF | 6 | V |
| 07-01.5b | voltage across 2 µF | 3 | V |
| 07-01.5c | voltage each after a long time | 4.5 | V |
| 07-01.6a | final voltage | 8.174 | V |
| 07-01.6b | energy before | 338.4 | µJ |
| 07-01.6c | energy after | 230.5 | µJ |
| 07-01.6d | energy lost | 107.9 | µJ |
| 07-01.7a | duty cycle | 0.275 | — |
| 07-01.7b | on-time | 0.55 | µs |
| 07-01.7c | ripple current | 0.4785 | A |
| 07-01.8a | voltage when forced to zero in 10 µs | 2500 | V |
| 07-01.8b | stored energy | 6.25 | mJ |
| 07-01.8c | time to zero with a 30 V clamp | 0.833 | ms |
| 07-01.9a | capacitance for the charge | 8.333 | µF |
| 07-01.9b | capacitors for the charge | 2 | — |
| 07-01.9c | largest total inductance | 8 | pH |
| 07-01.9d | capacitors for the inductance | 38 | — |
| 07-01.10a | self-resonant frequency | 25.16 | MHz |
| 07-01.10b | impedance at 1 GHz | 2.512 | Ω |
| 07-01.11a | integrator output after 2 s | −10 | V |
| 07-01.11b | drift in 10 s | −0.1 | V |
| 07-01.11c | time to the rail | 1200 | s |
| 07-01.12a | peak voltage | 12.57 | V |
| 07-01.12b | peak power | 12.57 | W |
| 07-01.12c | power frequency | 2 | kHz |
| 07-01.12d | peak stored energy | 2 | mJ |
| 07-01.13a | final current without saturation | 3.37 | A |
| 07-01.13b | time to reach 3 A | 0.5747 | µs |
| 07-01.13c | final current with saturation | 4.85 | A |
| 07-01.14a | inductor current | 2 | mA |
| 07-01.14b | capacitor voltage | 8 | V |
| 07-01.14c | capacitor energy | 32 | µJ |
| 07-01.14d | inductor energy | 20 | nJ |
| 07-01.15a | equivalent capacitance | 1.2 | µF |
| 07-01.15b | initial terminal voltage | 7 | V |
| 07-01.15c | energy in the two capacitors | 31 | µJ |
| 07-01.15d | energy of the equivalent | 29.4 | µJ |
| 07-01.15e | time constant | 12 | ms |
| 07-01.15f | final voltage, 2 µF | 0.8 | V |
| 07-01.15g | final voltage, 3 µF | −0.8 | V |
| 07-01.15h | energy dissipated | 29.4 | µJ |
| 07-01.15i | energy left | 1.6 | µJ |
