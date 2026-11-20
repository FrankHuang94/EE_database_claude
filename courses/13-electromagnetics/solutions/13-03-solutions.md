# Solutions 13-03 · Magnetostatics and Inductance

Problems: [13-03 problems](../problems/13-03-problems.md) · Chapter: [13-03](../chapters/13-03-magnetostatics-and-inductance.md). Every number below is recomputed by [verify_13_03.py](../verify/verify_13_03.py), which works each problem by an independent route: numerical Biot–Savart integration for the fields, numerical flux and energy integrals for the inductances, a Neumann double integral for the partial inductances, and a linear solve of each magnetic circuit.

---

## Solutions

### Solution 13-03.1

Midway, each wire is 5 mm away and contributes $\mu_0I/(2\pi \times 0.005)$ = 400 µT. With opposite currents the two contributions point the same way between the wires (use the right-hand rule on each), so $B$ = **800.0** µT. The force per metre on either wire is its current times the other's field at its location: $F' = I\,\mu_0I/(2\pi d) = 2 \times 10^{-7} \times 100/0.01$ = **2.000** mN/m. Opposite currents **repel**. Units: A × T = A × N/(A·m) = N/m.

### Solution 13-03.2

Tangential $H$ is continuous with no surface current: $H_{1x} = B_{1x}/\mu_0 = 0.3 \times 10^{-3}/\mu_0$ = **238.7** A/m, the same in the iron, so $B_{2x} = 500\mu_0H_{2x}$ = 150 mT. Normal $B$ is continuous: $B_{2z}$ = 1.2 mT. So $\vec{B}_2 = 150\hat{x} + 1.2\hat{z}$ mT, magnitude **150.0** mT. The angles from the normal are $\arctan(0.3/1.2)$ = **14.0**° in air and $\arctan(150/1.2)$ = **89.54**° in the iron. Their tangents are in the ratio 1/500: in the iron the field runs almost along the surface, and it leaves almost perpendicular.

### Solution 13-03.3

By symmetry $H_\phi$ depends only on $\rho$, and Ampère's law around a circle inside the core gives $H_\phi = NI/(2\pi\rho)$. The flux through the rectangular section is

$$
\Phi = \int_a^b\frac{\mu NI}{2\pi\rho}\,h\,d\rho = \frac{\mu NIh}{2\pi}\ln\frac{b}{a}, \qquad L = \frac{N\Phi}{I} = \frac{\mu N^2h}{2\pi}\ln\frac{b}{a}.
$$

With air, $L = 2 \times 10^{-7} \times 500^2 \times 0.01 \times \ln 1.5$ = **202.7** µH; with ferrite, 2000 times more, **405.5** mH. At 1 A, $H$ = 500/(2π × 0.02) = **3979** A/m at the inner radius and **2653** A/m at the outer. The bar approximation, $\mu_0N^2A/\ell$ with $A$ = 1 cm² and $\ell = 2\pi \times 0.025$ m, gives **200.0** µH, **1.35**% low: the field is stronger near the inner radius, and the mean-path formula underweights it. Units: (H/m)(m) = H.

### Solution 13-03.4

(a) In cylindrical coordinates, for $\vec{A} = A_z(\rho)\hat{z}$, the curl has only one term: $B_\phi = -\partial A_z/\partial\rho$. With $A_z = (\mu_0I/2\pi)\ln(\rho_0/\rho)$, $-\partial A_z/\partial\rho = \mu_0I/(2\pi\rho)$, the field of the wire. The constant $\rho_0$ drops out of the derivative: like the electric potential, the vector potential has a free reference. $\nabla\cdot\vec{A} = \partial A_z/\partial z = 0$, so this is in the Coulomb gauge.

(b) Take a rectangle in a plane containing the wire, with sides of 1 m along $z$ at $\rho_1$ = 1 mm and $\rho_2$ = 1 cm. $\vec{A}$ is along $z$, so the radial sides contribute nothing, and the circulation is $A_z(\rho_1) - A_z(\rho_2) = (\mu_0I/2\pi)\ln(\rho_2/\rho_1)$ per metre = $2 \times 10^{-7}\ln 10$ = **460.5** nWb/m. Directly, $\int_{\rho_1}^{\rho_2}\mu_0I\,d\rho/(2\pi\rho)$ gives the same, as Stokes's theorem requires. The reference $\rho_0$ cancels in the difference.

### Solution 13-03.5

(a) Put the loop in the $xy$ plane, centred on the origin, and the field point at $(0, 0, z)$. Every element $d\vec\ell'$ is perpendicular to the vector from it to the field point, whose length is $\sqrt{R^2 + z^2}$, so each contributes $dH = I\,d\ell'/[4\pi(R^2 + z^2)]$ at right angles to that vector. By symmetry the components across the axis cancel around the loop; the axial component is a fraction $R/\sqrt{R^2 + z^2}$ of each. Adding $2\pi R$ of length:

$$
B_z = \frac{\mu_0I}{4\pi}\,\frac{2\pi R}{R^2 + z^2}\,\frac{R}{\sqrt{R^2 + z^2}} = \frac{\mu_0IR^2}{2(R^2 + z^2)^{3/2}} .
$$

(b) At the centre, $\mu_0I/(2R)$ = **62.83** µT; at $z = R$, the factor $1/2^{3/2}$ makes it **22.21** µT.

(c) The midpoint is $R/2$ from each loop. Each contributes $\mu_0IR^2/[2(5R^2/4)^{3/2}]$, and together $\mu_0I(4/5)^{3/2}/R$ = **89.92** µT. With this spacing, the second derivative of the field along the axis also cancels at the midpoint, making the field there unusually uniform: the Helmholtz pair used to calibrate magnetic sensors.

### Solution 13-03.6

The long-solenoid formula scales as $1/\ell$: from 78.96 µH at 5 cm it is **197.4** µH at 2 cm and **19.74** µH at 20 cm. Corrected: $0.8181 \times 197.4$ = **161.5** µH and $0.9791 \times 19.74$ = **19.33** µH. The long formula is high by $1/K - 1$: **22.2**% for the 2 cm coil (length twice the diameter) and **2.1**% for the 20 cm coil (twenty diameters). With Example 13-03.3's 8.7% at five diameters, the error falls roughly as diameter over length.

### Solution 13-03.7

(a) Flux linkage two ways: $N\Phi = LI$ by definition, and $\Phi = BA$ for a uniform core, so $LI = NBA$. At the limits, $N \ge LI/(B_{max}A) = 100 \times 10^{-6} \times 5/(0.3 \times 10^{-4})$ = 16.67, so the fewest whole turns are **17**.

(b) $L = N^2/\mathcal{R} = \mu_0N^2A/(g + \ell_c/\mu_r)$, so $g + \ell_c/\mu_r = \mu_0N^2A/L$ = 0.3632 mm. The core contributes $\ell_c/\mu_r$ = 0.05/2000 = 0.025 mm of "equivalent air", so the gap is **0.3382** mm.

(c) $B = LI/(NA) = 100 \times 10^{-6} \times 5/(17 \times 10^{-4})$ = **0.2941** T, under the limit because 17 exceeds 16.67. The energy is $\tfrac12LI^2$ = **1.25** mJ. Core and gap carry the same flux, so they store energy in proportion to their reluctances: the gap's share is $g/(g + \ell_c/\mu_r)$ = **93.12**%. Without the gap, 17 turns on this core would give $\mu_r\mu_0N^2A/\ell_c$ = **1.453** mH, and the core would reach 0.3 T at only $B_{max}\ell_c/(\mu_r\mu_0N)$ = **0.3511** A, a fourteenth of the 5 A it must carry.

### Solution 13-03.8

(a) The wire's field at distance $\rho$ is $\mu_0I/(2\pi\rho)$, perpendicular to the plane of the loop. The flux through the loop is

$$
\Phi = \int_{d}^{d + w}\frac{\mu_0I}{2\pi\rho}\,h\,d\rho = \frac{\mu_0Ih}{2\pi}\ln\frac{d + w}{d},
$$

so $M = \Phi/I = 2 \times 10^{-7} \times 0.02 \times \ln 3$ = **4.394** nH.

(b) $\lvert v\rvert = M\,dI/dt = 4.394\ \text{nH} \times 1\ \text{A/ns}$ = **4.394** V. Fast current edges in power wiring couple volts into nearby loops; the cure is to shrink the victim loop's area or move it away.

### Solution 13-03.9

(a) Inside the wire the enclosed current is $I\rho^2/a^2$, so $H_\phi = I\rho/(2\pi a^2)$. The energy per metre stored inside is

$$
W'_m = \frac{\mu}{2}\int_0^a\Big(\frac{I\rho}{2\pi a^2}\Big)^2 2\pi\rho\,d\rho = \frac{\mu I^2}{4\pi a^4}\int_0^a\rho^3\,d\rho = \frac{\mu I^2}{16\pi},
$$

and $L'_{int} = 2W'_m/I^2 = \mu/8\pi$: **50.00** nH/m for nonmagnetic metal. The radius cancels because a thicker wire spreads the same energy over more area at a lower field.

(b) In the outer conductor ($b < \rho < c$) the enclosed current falls from $I$ to zero: $I_{enc} = I(c^2 - \rho^2)/(c^2 - b^2)$, so $H_\phi = I(c^2 - \rho^2)/[2\pi\rho(c^2 - b^2)]$. The same energy integral gives

$$
L'_{outer} = \frac{\mu}{2\pi(c^2 - b^2)^2}\Big[c^4\ln\frac{c}{b} - c^2(c^2 - b^2) + \frac{c^4 - b^4}{4}\Big] .
$$

With $b$ = 1.75 mm and $c$ = 2.0 mm this is **9.506** nH/m. The total low-frequency inductance is 250.6 + 50.00 + 9.506 = **310.1** nH/m: the internal terms add **59.51** nH/m, almost a quarter of the external value. As frequency rises and the skin effect confines the current to the facing surfaces (13-05), both internal terms fade and the inductance falls toward 250.6 nH/m.

### Solution 13-03.10

With the image wire, $L' = (\mu_0/2\pi)\cosh^{-1}(h/a) = 2 \times 10^{-7}\cosh^{-1}3$ = **352.5** nH/m, unaffected by the nonmagnetic dielectric. 13-02's capacitance scales with $\varepsilon$: $C' = 2\pi\varepsilon_r\varepsilon_0/\cosh^{-1}3$ = **135.7** pF/m. Then $\sqrt{L'/C'}$ = **50.97** Ω and $\sqrt{L'C'} = \sqrt{\varepsilon_r}/c$ = **6.917** ps/mm. A wire 0.2 mm across, 0.2 mm above its plane in FR-4-like material, makes a line close to 50 Ω; printed traces (flat, with the dielectric only below) need the field solvers of 13-02 and 13-07.

### Solution 13-03.11

(a) Four equal inductors in parallel without coupling: $L/4$ = **0.25** nH.

(b) Each wire carries $I/4$. The voltage across one wire is its own $L\,d(I/4)/dt$ plus $M\,d(I/4)/dt$ from each of the other three:

$$
v = \frac{L + 3M}{4}\,\frac{dI}{dt}, \qquad L_{eff} = \frac{1 + 3 \times 0.3}{4} = \mathbf{0.475}\ \text{nH}.
$$

Coupling nearly doubles the effective inductance, which is why parallel bonds are spread out, and why alternating supply and ground bonds (whose mutual inductance subtracts) helps.

(c) $dI/dt$ = 0.1 A/100 ps = 10⁹ A/s: the bounce is **0.25** V uncoupled and **0.475** V coupled.

### Solution 13-03.12

The winding is an MMF source of $NI$ in the centre leg. The centre leg and its gap carry the whole flux; it then splits equally between the two outer legs, which are in parallel. Reluctances:

- centre leg: $0.04/(2000\mu_0 \times 2 \times 10^{-4})$ = **7.958 × 10⁴** A/Wb;
- gap: $0.5 \times 10^{-3}/(\mu_0 \times 2 \times 10^{-4})$ = **1.989 × 10⁶** A/Wb;
- each outer leg: $0.08/(2000\mu_0 \times 10^{-4})$ = **3.183 × 10⁵** A/Wb, so the pair is $1.592 \times 10^5$ A/Wb.

The total is **2.228 × 10⁶** A/Wb, so $L = 50^2/\mathcal{R}$ = **1.122** mH, and the gap carries **89.29**% of the reluctance. At 1 A, $\Phi = 50/\mathcal{R}$ = 22.44 µWb, so the centre leg has $B$ = **0.1122** T; each outer leg carries half the flux through half the area, also **0.1122** T. Making the outer legs half the centre's area is what keeps the flux density uniform around the core.

### Solution 13-03.13

(a) With $\ell$ = 1 cm and $d = a$ = 0.1 mm, a side's partial self-inductance is **8.617** nH. With $d$ = 1 cm, opposite sides have $M_p$ = **0.9343** nH.

(b) The partial mutual inductance between two segments is proportional to $d\vec\ell_1\cdot d\vec\ell_2$ integrated over both (the Neumann formula), which is zero for perpendicular segments. Opposite sides of a loop carry the current in opposite directions, so their $d\vec\ell_1\cdot d\vec\ell_2$ is negative.

(c) The loop inductance sums every partial term with its sign: four self terms, and each of the two opposite pairs counted twice ($M_{12}$ and $M_{21}$):

$$
L = 4L_p - 4M_p = 4(8.617 - 0.9343) = \mathbf{30.73}\ \text{nH}.
$$

The textbook formula gives **30.65** nH, **0.26**% lower: it uses the same physics with a thin-wire approximation. A 1 cm loop of thin wire has about 31 nH; shrinking the loop area is the strongest way to reduce it.

### Solution 13-03.14

(a) At fixed flux, the magnetic circuit stores $W = \tfrac12\Phi\mathcal{F} = \tfrac12\Phi^2\mathcal{R}$, with $\mathcal{R} = \mathcal{R}_c + g/(\mu_0A)$. If the gap closes by $dg$ with the flux held fixed (no energy from the source), the mechanical work equals the fall in stored energy:

$$
F = -\frac{dW}{dg}\Big|_\Phi = -\frac{\Phi^2}{2}\,\frac{1}{\mu_0A} \quad\Rightarrow\quad \lvert F\rvert = \frac{\Phi^2}{2\mu_0A} = \frac{B^2A}{2\mu_0},
$$

with the minus sign meaning the force acts to close the gap. The faces attract with a pressure $B^2/(2\mu_0)$, equal to the energy density in the gap.

(b) At 1 A, $B$ = 0.11968 T: $F = 0.11968^2 \times 10^{-4}/(2\mu_0)$ = **0.5699** N. At 0.3 T: **3.581** N. Relays and solenoid actuators use exactly this force; in a power inductor it makes the core halves vibrate at the switching frequency, which is the source of audible "coil whine" when that frequency falls in the audio band.

### Solution 13-03.15

(a) $\vec{M} = M\hat{z}$ is uniform, so $\vec{J}_b = \nabla\times\vec{M} = 0$ inside. On the curved side the outward normal is $\hat\rho$, so $\vec{K}_b = \vec{M}\times\hat{n} = M\hat{z}\times\hat\rho = M\hat\phi$: a surface current of **8 × 10⁵** A/m circling the rod. On the end faces $\hat{n} = \pm\hat{z}$ is parallel to $\vec{M}$, so $\vec{K}_b = 0$ there. The magnet is magnetically identical to a solenoid with $nI$ = 8 × 10⁵ A/m, such as 1000 turns per metre carrying 800 A.

(b) A long solenoid has $B = \mu_0nI$ inside, so $B \approx \mu_0M$ = **1.005** T, and $H = B/\mu_0 - M \approx 0$.

(c) A ring of radius $a$ and current $dI$ at axial distance $s$ gives $dB_z = \mu_0a^2\,dI/[2(a^2 + s^2)^{3/2}]$ on the axis (the loop result of the chapter, off centre). With $dI = K_b\,dz$, summing rings over the rod's length $L$ gives, at the centre,

$$
B = \frac{\mu_0Ma^2}{2}\int_{-L/2}^{L/2}\frac{dz}{(a^2 + z^2)^{3/2}} = \mu_0M\frac{L/2}{\sqrt{(L/2)^2 + a^2}} ,
$$

which is **1.005** T (0.02% below $\mu_0M$). At the end face the rings lie on one side only, from 0 to $L$: $B = (\mu_0M/2)\,L/\sqrt{L^2 + a^2}$ = **0.5026** T. Each half of a long solenoid contributes half of the central field, and at the end only one half is present.

(d) At the centre $H = B/\mu_0 - M = M[(L/2)/\sqrt{(L/2)^2 + a^2} - 1]$ = **−160** A/m. $H$ is small but negative: it points against $\vec{M}$. Because $\nabla\cdot\vec{B} = 0$ and $\vec{B} = \mu_0(\vec{H} + \vec{M})$, $\nabla\cdot\vec{H} = -\nabla\cdot\vec{M}$, so the ends of the magnet act as sources of $\vec{H}$ ("magnetic poles") whose field inside opposes the magnetization. This **demagnetizing field** is small for a long thin rod and large for a short fat one, which is why permanent magnets are specified by their resistance to demagnetization (coercivity) and why short magnets need high-coercivity materials.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 13-03.1a | flux density midway | 800.0 | µT |
| 13-03.1b | force per metre | 2.000 | mN/m |
| 13-03.2a | tangential H | 238.7 | A/m |
| 13-03.2b | magnitude of B in the iron | 150.0 | mT |
| 13-03.2c | angle in air | 14.0 | ° |
| 13-03.2d | angle in iron | 89.54 | ° |
| 13-03.3a | air-core toroid | 202.7 | µH |
| 13-03.3b | ferrite toroid | 405.5 | mH |
| 13-03.3c | H at the inner radius | 3979 | A/m |
| 13-03.3d | H at the outer radius | 2653 | A/m |
| 13-03.3e | mean-path approximation | 200.0 | µH |
| 13-03.3f | its error | 1.35 | % |
| 13-03.4a | flux per metre | 460.5 | nWb/m |
| 13-03.5a | field at the centre | 62.83 | µT |
| 13-03.5b | field on axis at z = R | 22.21 | µT |
| 13-03.5c | Helmholtz midpoint field | 89.92 | µT |
| 13-03.6a | long formula, 2 cm | 197.4 | µH |
| 13-03.6b | long formula, 20 cm | 19.74 | µH |
| 13-03.6c | corrected, 2 cm | 161.5 | µH |
| 13-03.6d | corrected, 20 cm | 19.33 | µH |
| 13-03.6e | excess, 2 cm | 22.2 | % |
| 13-03.6f | excess, 20 cm | 2.1 | % |
| 13-03.7a | fewest turns | 17 | — |
| 13-03.7b | gap length | 0.3382 | mm |
| 13-03.7c | peak flux density | 0.2941 | T |
| 13-03.7d | stored energy | 1.25 | mJ |
| 13-03.7e | gap's share of the energy | 93.12 | % |
| 13-03.7f | ungapped inductance | 1.453 | mH |
| 13-03.7g | ungapped saturation current | 0.3511 | A |
| 13-03.8a | mutual inductance | 4.394 | nH |
| 13-03.8b | induced voltage | 4.394 | V |
| 13-03.9a | internal inductance of the wire | 50.00 | nH/m |
| 13-03.9b | inside the outer conductor | 9.506 | nH/m |
| 13-03.9c | total low-frequency inductance | 310.1 | nH/m |
| 13-03.9d | added by the internal terms | 59.51 | nH/m |
| 13-03.10a | inductance per metre | 352.5 | nH/m |
| 13-03.10b | capacitance per metre | 135.7 | pF/m |
| 13-03.10c | impedance | 50.97 | Ω |
| 13-03.10d | delay | 6.917 | ps/mm |
| 13-03.11a | uncoupled effective inductance | 0.25 | nH |
| 13-03.11b | coupled effective inductance | 0.475 | nH |
| 13-03.11c | bounce, uncoupled | 0.25 | V |
| 13-03.11d | bounce, coupled | 0.475 | V |
| 13-03.12a | centre-leg reluctance | 7.958 × 10⁴ | A/Wb |
| 13-03.12b | gap reluctance | 1.989 × 10⁶ | A/Wb |
| 13-03.12c | each outer leg | 3.183 × 10⁵ | A/Wb |
| 13-03.12d | total reluctance | 2.228 × 10⁶ | A/Wb |
| 13-03.12e | inductance | 1.122 | mH |
| 13-03.12f | gap's share | 89.29 | % |
| 13-03.12g | centre-leg flux density | 0.1122 | T |
| 13-03.12h | outer-leg flux density | 0.1122 | T |
| 13-03.13a | partial self-inductance of a side | 8.617 | nH |
| 13-03.13b | opposite-side partial mutual | 0.9343 | nH |
| 13-03.13c | loop inductance | 30.73 | nH |
| 13-03.13d | textbook formula | 30.65 | nH |
| 13-03.13e | formula below partial-inductance sum | 0.26 | % |
| 13-03.14a | force at 1 A | 0.5699 | N |
| 13-03.14b | force at 0.3 T | 3.581 | N |
| 13-03.15a | bound surface current | 8 × 10⁵ | A/m |
| 13-03.15b | long-rod estimate of B | 1.005 | T |
| 13-03.15c | B at the centre | 1.005 | T |
| 13-03.15d | B at the end face | 0.5026 | T |
| 13-03.15e | H at the centre | −160 | A/m |
