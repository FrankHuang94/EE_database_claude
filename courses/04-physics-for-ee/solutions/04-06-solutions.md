# Solutions 04-06 · Magnetic Fields and Forces

Problems: [04-06 problems](../problems/04-06-problems.md) · Chapter: [04-06](../chapters/04-06-magnetic-fields-and-forces.md). Every number below is recomputed by [verify_04_06.py](../verify/verify_04_06.py).

---

## Solutions

### Solution 04-06.1

$\vec v = (2\times10^5, 0, 0)$ m/s and $\vec B = 0.2(\cos30°, \sin30°, 0)$ T. Then $\vec v\times\vec B = (0, 0, v_xB_y) = (0, 0, 2\times10^5\times0.1)$, so $\vec F = e\vec v\times\vec B$ points along $+z$ with magnitude $evB\sin30° = 1.602\times10^{-19}\times2\times10^5\times0.2\times0.5 = $ **3.204×10⁻¹⁵ N**. Only the field component perpendicular to $\vec v$ matters.

### Solution 04-06.2

(a) $50\times10^{-6}/10^{-4} = $ **0.5 G**.

(b) $B = \mu_0I/(2\pi r) = 2\times10^{-7}\times10/0.01 = $ **200 µT**, which is **2 G**: four times the Earth's field.

### Solution 04-06.3

(a) $f_c = eB/(2\pi m_p) = 1.602\times10^{-19}\times1.5/(2\pi\times1.6726\times10^{-27}) = $ **22.87 MHz**.

(b) $v = \sqrt{2K/m_p} = \sqrt{2\times1.602\times10^{-13}/1.6726\times10^{-27}} = 1.384\times10^7$ m/s (4.6% of $c$, so non-relativistic is fair), and $r = m_pv/(eB) = $ **9.633 cm**.

### Solution 04-06.4

(a) $v = E/B = 10^5/0.05 = $ **2×10⁶ m/s**.

(b) $V = m_ev^2/(2e) = 9.109\times10^{-31}\times4\times10^{12}/(3.204\times10^{-19}) = $ **11.37 V**.

### Solution 04-06.5

$r = \sqrt{2mV/e}/B$. ¹⁰B⁺: **9.857 cm**; ¹¹B⁺: **10.34 cm**. After a half circle they land $2\Delta r$ = **9.622 mm** apart. Higher voltage increases the radii (as $\sqrt V$) and the separation; higher field shrinks both.

### Solution 04-06.6

$F = ILB\sin\theta = 10\times0.5\times0.2\times\sin60° = $ **0.8660 N**, perpendicular to both the wire and the field.

### Solution 04-06.7

(a) $m = NIA = 50\times0.2\times(0.03\times0.04) = $ **0.012 A·m²**.

(b) $\tau = mB\sin30° = 0.012\times0.3\times0.5 = $ **1.8×10⁻³ N·m**.

(c) $U = -mB\cos\theta$ ranges from $-mB$ to $+mB$: a difference of $2mB$ = **7.2×10⁻³ J**.

### Solution 04-06.8

From the segment formula with $x$ from −5 to +5 cm at $y$ = 2 cm: $B = \dfrac{\mu_0I}{4\pi y}\cdot\dfrac{2\times0.05}{\sqrt{0.05^2 + 0.02^2}} = \dfrac{10^{-7}\times5}{0.02}\times1.857 = $ **46.42 µT**. An infinite wire gives $\mu_0I/(2\pi y)$ = **50 µT**: the segment delivers **0.9285** of it, because at 2 cm the 10 cm segment already looks fairly long.

### Solution 04-06.9

(a) $F/L = \mu_0I_1I_2/(2\pi d) = 2\times10^{-7}\times15/0.04 = $ **7.5×10⁻⁵ N/m**, **repulsive** (opposite currents).

(b) Midway, each wire's field circles it; between antiparallel currents the two fields point the same way and add: $B = \frac{\mu_0}{2\pi(0.02)}(3 + 5) = $ **80 µT**.

### Solution 04-06.10

(a) $B = \mu_0(N/L)I$, so $I = BL/(\mu_0N) = 0.01\times0.3/(1.2566\times10^{-6}\times600) = $ **3.979 A**.

(b) $B = \mu_0NI/(2\pi r)$: **5 mT** at 4 cm and **3.333 mT** at 6 cm.

### Solution 04-06.11

Inside, $B = \mu_0Ir/(2\pi a^2)$: at 0.5 mm, $2\times10^{-7}\times10\times0.5\times10^{-3}/10^{-6} = $ **1 mT**. At the surface: **2 mT**. Outside, $\mu_0I/(2\pi r)$: at 5 mm, **0.4 mT**.

### Solution 04-06.12

(a) $V_H = IB/(net) = 10\times0.5/(8.49\times10^{28}\times1.602\times10^{-19}\times10^{-4}) = $ **3.675 µV**.

(b) $n = 10^{21}$ m⁻³: $V_H = 0.5\times10^{-3}\times0.05/(10^{21}\times1.602\times10^{-19}\times5\times10^{-6}) = $ **31.21 mV**, nearly 10,000 times larger with 1/20,000 of the current.

(c) $R_H = 1/(ne) = $ **6.242×10⁻³ m³/C** in magnitude (negative for electrons).

### Solution 04-06.13

(a) $p = IB/(etV_H) = 10^{-3}\times0.1/(1.602\times10^{-19}\times5\times10^{-4}\times2.50\times10^{-3}) = 4.993\times10^{20}$ m⁻³ = **4.993×10¹⁴ cm⁻³**.

(b) $\mu_p = 1/(ep\rho) = 1/(1.602\times10^{-19}\times4.993\times10^{14}\times27.7) = $ **451.3 cm²/V·s**, consistent with the lightly doped hole mobility of 04-05.

### Solution 04-06.14

(a) Each leg gives $\mu_0I/(2\pi d) = 2\times10^{-7}\times10/10^{-3} = $ **2 mT** at its plate. The legs carry opposite currents, so the fields at the two plates are opposite: +2 mT and −2 mT (taking plate 1's sense as positive).

(b) Each plate also sees the stray +0.5 mT: plate 1 reads 2.5 mT, plate 2 reads −1.5 mT. The difference is **4 mT**: twice the signal, with the stray field cancelled exactly.

(c) A single plate would read 2.5 mT instead of 2 mT: a **25%** error. Differential sensing is why integrated current sensors tolerate nearby motors and wiring.

### Solution 04-06.15

(a) Around the core, $H_{\text{core}}l + H_{\text{gap}}g = NI$. $B$ is continuous across the gap, with $H_{\text{core}} = B/(\mu_r\mu_0)$ and $H_{\text{gap}} = B/\mu_0$, so

$$
B = \frac{\mu_0NI}{l/\mu_r + g} = \frac{1.2566\times10^{-6}\times20}{0.05/2000 + 0.0005}\,I ,
$$

which is **0.04787 T/A**: the 0.5 mm gap has 20 times the magnetic "resistance" of the 50 mm of ferrite.

(b) $I_{\text{sat}} = 0.39/0.04787 = $ **8.147 A**.

(c) **21** times the ungapped 0.388 A. The cost: inductance falls by the same factor of 21 (it scales with flux per ampere, 04-07), so more turns are needed, and flux fringing around the gap causes extra loss in nearby windings.

### Solution 04-06.16

(a) For $z \gg R$, $(R^2 + z^2)^{3/2} \approx z^3$, so $B \approx \mu_0IR^2/(2z^3) = \mu_0(I\pi R^2)/(2\pi z^3) = \mu_0m/(2\pi z^3)$.

(b) Exact: $1.2566\times10^{-6}\times10^{-4}/(2\times(0.0101)^{3/2}) = $ **61.90 nT**. Dipole: $m = \pi\times10^{-4}$ A·m², giving **62.83 nT**. Ratio **0.9852**: within 1.5% at ten radii, the correction being $(1 + R^2/z^2)^{-3/2} \approx 1 - \tfrac32(R/z)^2$.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 04-06.1a | force on the proton | 3.204×10^-15 | N |
| 04-06.2a | 50 µT in gauss | 0.5 | G |
| 04-06.2b | field 1 cm from 10 A | 200 | µT |
| 04-06.2c | field 1 cm from 10 A | 2 | G |
| 04-06.3a | proton cyclotron frequency | 22.87 | MHz |
| 04-06.3b | proton orbit radius at 1 MeV | 9.633 | cm |
| 04-06.4a | selected speed | 2×10^6 | m/s |
| 04-06.4b | accelerating voltage | 11.37 | V |
| 04-06.5a | ¹⁰B⁺ radius | 9.857 | cm |
| 04-06.5b | ¹¹B⁺ radius | 10.34 | cm |
| 04-06.5c | separation after a half circle | 9.622 | mm |
| 04-06.6a | force on the wire | 0.8660 | N |
| 04-06.7a | coil moment | 0.012 | A·m² |
| 04-06.7b | torque | 1.8×10^-3 | N·m |
| 04-06.7c | energy difference | 7.2×10^-3 | J |
| 04-06.8a | segment field | 46.42 | µT |
| 04-06.8b | infinite-wire field | 50 | µT |
| 04-06.8c | segment over infinite | 0.9285 | — |
| 04-06.9a | force per meter | 7.5×10^-5 | N/m |
| 04-06.9b | field midway | 80 | µT |
| 04-06.10a | solenoid current | 3.979 | A |
| 04-06.10b | toroid field, inner radius | 5 | mT |
| 04-06.10c | toroid field, outer radius | 3.333 | mT |
| 04-06.11a | field at 0.5 mm | 1 | mT |
| 04-06.11b | field at 1 mm | 2 | mT |
| 04-06.11c | field at 5 mm | 0.4 | mT |
| 04-06.12a | Hall voltage, copper | 3.675 | µV |
| 04-06.12b | Hall voltage, silicon | 31.21 | mV |
| 04-06.12c | Hall coefficient magnitude, silicon | 6.242×10^-3 | m³/C |
| 04-06.13a | hole density | 4.993×10^14 | cm⁻³ |
| 04-06.13b | hole mobility | 451.3 | cm²/V·s |
| 04-06.14a | current's field at each plate | 2 | mT |
| 04-06.14b | differential signal | 4 | mT |
| 04-06.14c | single-plate error | 25 | % |
| 04-06.15a | flux density per ampere, gapped | 0.04787 | T/A |
| 04-06.15b | saturation current, gapped, 100 °C | 8.147 | A |
| 04-06.15c | improvement factor | 21 | — |
| 04-06.16a | exact on-axis field | 61.90 | nT |
| 04-06.16b | dipole approximation | 62.83 | nT |
| 04-06.16c | exact over dipole | 0.9852 | — |
