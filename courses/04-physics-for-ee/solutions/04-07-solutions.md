# Solutions 04-07 · Faraday's Law, Lenz's Law and Inductance

Problems: [04-07 problems](../problems/04-07-problems.md) · Chapter: [04-07](../chapters/04-07-faraday-lenz-and-inductance.md). Every number below is recomputed by [verify_04_07.py](../verify/verify_04_07.py).

---

## Solutions

### Solution 04-07.1

$|\mathcal E| = N\,\Delta\Phi/\Delta t = 50\times0.5\times20\times10^{-4}/0.1 = $ **0.5 V**. The flux is decreasing, so by Lenz's law the induced current makes a field in the *same* direction as the original, trying to maintain it.

### Solution 04-07.2

(a) The flux inside is $Bx\ell$ with $x$ shrinking at 2 m/s: $|\mathcal E| = B\ell v = 0.3\times0.1\times2 = $ **0.06 V**.

(b) $I = 0.06/0.5 = $ **0.12 A**.

(c) The side still in the field feels $I\ell B = 0.12\times0.1\times0.3 = $ **3.6×10⁻³ N**, opposing the pull (Lenz), so you must supply that force.

(d) $I^2R = $ **7.2×10⁻³ W**, equal to $Fv$ ✓.

### Solution 04-07.3

Peak EMF $NBA\omega = \sqrt2\times230 = 325.3$ V, so $N = 325.3/(1.2\times0.02\times2\pi\times50) = $ **43.14**: 44 turns.

### Solution 04-07.4

(a) Back-EMF $0.02\times500 = $ **10 V**; current $(12 - 10)/0.5 = $ **4 A**.

(b) At stall there is no back-EMF: $12/0.5 = $ **24 A**, six times the running current. Motor drivers limit start-up current for this reason.

(c) The power converted is back-EMF × current, $10\times4 = $ **40 W** (the other $4^2\times0.5 = 8$ W heats the winding).

### Solution 04-07.5

(a) $\delta = \sqrt{\rho/(\pi f\mu_0)}$: at 50 kHz, **0.2917 mm**; at 10 GHz, **0.6523 µm**.

(b) $\delta = \sqrt{10^{-7}/(\pi\times50\times1000\times1.2566\times10^{-6})} = $ **0.7118 mm**. Steel's high permeability makes the skin depth small even at mains frequency. A solid core would carry flux only near its surface and suffer large eddy losses; laminations thinner than the skin depth (a few tenths of a millimeter) let flux penetrate fully and cut the eddy-current paths.

### Solution 04-07.6

(a) Inside the toroid, $B = \mu_0Ni/(2\pi r)$. The flux through one turn's rectangular cross-section is $\int_a^bB\,h\,dr = \frac{\mu_0Nih}{2\pi}\ln\frac ba$, linked by $N$ turns, so $L = \mu_0N^2h\ln(b/a)/(2\pi)$. Numerically, $1.2566\times10^{-6}\times10^4\times0.01\times\ln1.5/(2\pi) = $ **8.109 µH**.

(b) With $\mu_r$ = 2000: **16.22 mH**.

### Solution 04-07.7

(a) $\tau = L/R = $ **2 ms**. (b) $I_\infty = 10/5 = $ **2 A**. (c) $\tfrac12LI^2 = $ **20 mJ**. (d) $i = 2(1 - e^{-t/\tau}) = 1$ at $t = \tau\ln2 = $ **1.386 ms**.

### Solution 04-07.8

(a) $L/\ell = (\mu_0/2\pi)\ln(1.475/0.45) = 2\times10^{-7}\times1.187 = $ **0.2374 µH/m**.

(b) With $C/\ell$ = 105.4 pF/m: $\sqrt{L/C} = $ **47.45 Ω**, close to the 50 Ω standard.

(c) $1/\sqrt{LC} = $ **1.999×10⁸ m/s**, which is **c/1.5**: exactly $c/\sqrt{\varepsilon_r}$, because the product $LC$ per unit length is $\mu_0\varepsilon$ for any coaxial geometry ([04-08](../chapters/04-08-maxwell-preview.md)).

### Solution 04-07.9

$u_B = B^2/(2\mu_0) = 2.25/(2\times1.2566\times10^{-6}) = $ **8.952×10⁵ J/m³**; $u_E = \tfrac12\varepsilon_0E^2 = $ **39.84 J/m³**. Ratio **2.247×10⁴**. Magnetic fields can store (and exert, since pressure equals energy density) about twenty thousand times more than electric fields in air before breakdown, which is why motors and actuators are magnetic. Electrostatic actuators win only at the micro scale, where gaps are tiny.

### Solution 04-07.10

(a) $M = k\sqrt{L_1L_2} = 0.98\times\sqrt{100\times25}$ µH = **49 µH**.

(b) $\sqrt{25/100} = $ **0.5**: since $L\propto N^2$ on a shared core, the inductance ratio gives the turns ratio squared.

### Solution 04-07.11

$R_{\text{seen}} = (N_1/N_2)^2R_L$, so $N_1/N_2 = \sqrt{800/8} = $ **10**.

### Solution 04-07.12

(a) At saturation the flux linkage is $N B_sA = LI$, so $N = LI/(B_sA) = 10^{-5}\times10/(0.39\times4\times10^{-5}) = $ **6.410**; round up to 7 turns.

(b) Neglecting the core, $L = \mu_0N^2A/g$, so $g = \mu_0\times49\times4\times10^{-5}/10^{-5} = $ **0.2463 mm**.

(c) $B = \mu_0NI/g$ reaches 0.39 T at $I = 0.39\times2.463\times10^{-4}/(1.2566\times10^{-6}\times7) = $ **10.92 A**, above 10 A ✓. (The problem neglects the core's reluctance. For a typical ferrite path, 5 cm long with $\mu_r$ = 2000, it would be $0.05/(2000\times2.463\times10^{-4}) \approx 10\%$ of the gap's, raising the saturation current slightly further while lowering $L$ by a similar fraction; a real design iterates.)

### Solution 04-07.13

(a) Take the lamination in the $yz$-plane with thickness $t$ along $x$, and flux along $z$. A thin rectangular path at $\pm x$ (width $w$ along $y$, $w \gg t$) encloses flux $B(t)\cdot2xw$, so the EMF around it is $2xw\,dB/dt$; the path length is about $2w$, so $E = x\,dB/dt$ and $J = (x/\rho)\,dB/dt$. The loss per volume averaged over the thickness is

$$
\frac1t\int_{-t/2}^{t/2}\rho J^2\,dx = \frac{1}{\rho}\Big(\frac{dB}{dt}\Big)^2\frac{t^2}{12} .
$$

With $B = B_{\max}\sin\omega t$, the time average of $(dB/dt)^2$ is $\omega^2B_{\max}^2/2$, giving $\omega^2B^2t^2/(24\rho) = \pi^2f^2B^2t^2/(6\rho)$.

(b) $\pi^2\times50^2\times1.5^2\times(3.5\times10^{-4})^2/(6\times4.7\times10^{-7}) = $ **2412 W/m³**, which is **0.3152 W/kg**. (Real cores also have hysteresis and "excess" loss, typically larger than this classical eddy part.)

(c) At 400 Hz with 0.1 mm: **1.647 W/kg**. Loss scales as $(ft)^2$: eight times the frequency multiplies it by 64 and $(0.1/0.35)^2 = 0.082$ divides most of that back out, so the loss still rises about 5.2 times. Frequency enters squared, so thinner laminations only partly compensate.

### Solution 04-07.14

(a) $v = L\,di/dt = 10^{-9}\times0.1/10^{-10} = $ **1 V**: on a 1 V supply, a disaster.

(b) Ten in parallel: $L/10$, so **0.1 V**.

(c) Parallel connections close together share flux: their mutual inductance adds to each one's effective inductance, so ten pins give less than a tenfold reduction. Interleaving power and ground pins (so their currents' fields cancel) helps; this is why packages alternate supply and ground and why decoupling capacitors sit close to the die.

### Solution 04-07.15

(a) $\delta = \sqrt{\rho/(\pi f\mu_0)} = $ **0.2063 mm** at 100 kHz.

(b) The 1 mm wire's radius is 2.4 skin depths, so its center carries less current and the ratio is 1.466. The 0.1 mm strand's radius is 0.24 skin depths: the field barely varies across it and current fills it uniformly (ratio 1.000).

(c) Uninsulated strands act as one thick conductor, so the skin effect returns. And each strand must visit inner and outer positions along the bundle (transposition), so each links the same flux and carries an equal share; otherwise the proximity effect crowds current into the outer strands.

### Solution 04-07.16

(a) At resonance the receiver loop is purely resistive, $R_2 + R_L$. A transmitter current $i_1$ induces $j\omega Mi_1$ in it, driving $i_2 = j\omega Mi_1/(R_2 + R_L)$; that current induces back $j\omega Mi_2 = -(\omega M)^2i_1/(R_2 + R_L)$ in the transmitter, which looks like an added series resistance $(\omega M)^2/(R_2 + R_L)$. With $\omega M = 11.31$ Ω: $127.9/5.1 = $ **25.08 Ω**.

(b) $\eta = \frac{25.08}{25.18}\times\frac{5}{5.1} = $ **0.9765**.

(c) $Q = \omega L/R = 2\pi\times360\times10^3\times10^{-5}/0.1 = $ **226.2**. High-Q coils and good coupling ($kQ \gg 1$) are what make efficient wireless power possible; real phone coils have lower Q and coupling, and real systems lose more in rectifiers and electronics.

### Solution 04-07.17

(a) By symmetry the induced $E$ circles the axis with the same magnitude everywhere on a circle of radius $r$. Faraday's law, $\oint\vec E\cdot d\vec\ell = -d\Phi/dt$, gives $E\cdot2\pi r = \pi r^2\,dB/dt$ inside, so $E = \frac r2\frac{dB}{dt} = 0.005\times0.5$ = **2.500 mV/m**.

(b) Outside, the circle encloses all the flux, $\pi R^2B$: $E\cdot2\pi r = \pi R^2\,dB/dt$, so $E = \frac{R^2}{2r}\frac{dB}{dt} = \frac{4\times10^{-4}}{0.06}\times0.5$ = **3.333 mV/m**.

(c) $\mathcal E = \pi R^2\,dB/dt = \pi\times4\times10^{-4}\times0.5$ = **0.6283 mV**, whatever the loop's radius as long as it encloses the solenoid. The field outside is not zero because Faraday's law links $E$ to the flux *enclosed by the path*, not to $B$ on the path: the changing flux inside drives a circulating $E$ everywhere around it. This non-conservative field is why the voltage a meter reads near a transformer depends on how its leads are routed.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 04-07.1a | average EMF | 0.5 | V |
| 04-07.2a | EMF | 0.06 | V |
| 04-07.2b | current | 0.12 | A |
| 04-07.2c | pulling force | 3.6×10^-3 | N |
| 04-07.2d | power dissipated | 7.2×10^-3 | W |
| 04-07.3a | turns for 230 V rms | 43.14 | — |
| 04-07.4a | back-EMF at 500 rad/s | 10 | V |
| 04-07.4b | running current | 4 | A |
| 04-07.4c | stall current | 24 | A |
| 04-07.4d | power converted | 40 | W |
| 04-07.5a | copper skin depth at 50 kHz | 0.2917 | mm |
| 04-07.5b | copper skin depth at 10 GHz | 0.6523 | µm |
| 04-07.5c | steel skin depth at 50 Hz | 0.7118 | mm |
| 04-07.6a | air toroid inductance | 8.109 | µH |
| 04-07.6b | ferrite toroid inductance | 16.22 | mH |
| 04-07.7a | time constant | 2 | ms |
| 04-07.7b | final current | 2 | A |
| 04-07.7c | stored energy | 20 | mJ |
| 04-07.7d | time to reach 1 A | 1.386 | ms |
| 04-07.8a | coax inductance per meter | 0.2374 | µH/m |
| 04-07.8b | characteristic impedance | 47.45 | Ω |
| 04-07.8c | wave speed | 1.999×10^8 | m/s |
| 04-07.8d | c over wave speed | 1.5 | — |
| 04-07.9a | magnetic energy density at 1.5 T | 8.952×10^5 | J/m³ |
| 04-07.9b | electric energy density at 3 MV/m | 39.84 | J/m³ |
| 04-07.9c | ratio | 2.247×10^4 | — |
| 04-07.10a | mutual inductance | 49 | µH |
| 04-07.10b | equivalent turns ratio | 0.5 | — |
| 04-07.11a | turns ratio | 10 | — |
| 04-07.12a | minimum turns before rounding | 6.410 | — |
| 04-07.12b | gap length | 0.2463 | mm |
| 04-07.12c | saturation current with 7 turns | 10.92 | A |
| 04-07.13a | eddy loss per volume, 50 Hz | 2412 | W/m³ |
| 04-07.13b | eddy loss per mass, 50 Hz | 0.3152 | W/kg |
| 04-07.13c | eddy loss per mass, 400 Hz, 0.1 mm | 1.647 | W/kg |
| 04-07.14a | ground bounce, one connection | 1 | V |
| 04-07.14b | ground bounce, ten connections | 0.1 | V |
| 04-07.15a | copper skin depth at 100 kHz | 0.2063 | mm |
| 04-07.15b | AC/DC ratio, 1 mm wire | 1.466 | — |
| 04-07.15c | AC/DC ratio, 0.1 mm strand | 1.000 | — |
| 04-07.16a | reflected resistance | 25.08 | Ω |
| 04-07.16b | link efficiency | 0.9765 | — |
| 04-07.16c | coil quality factor | 226.2 | — |
| 04-07.17a | induced field at 1.0 cm | 2.500 | mV/m |
| 04-07.17b | induced field at 3.0 cm | 3.333 | mV/m |
| 04-07.17c | EMF around the 3.0 cm loop | 0.6283 | mV |
