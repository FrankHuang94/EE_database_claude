# Solutions 04-08 · Energy in Fields and Maxwell's Equations (Preview)

Problems: [04-08 problems](../problems/04-08-problems.md) · Chapter: [04-08](../chapters/04-08-maxwell-preview.md). Every number below is recomputed by [verify_04_08.py](../verify/verify_04_08.py).

---

## Solutions

### Solution 04-08.1

$u_E = \tfrac12\varepsilon_0E^2 = 0.5\times8.854\times10^{-12}\times10^8 = $ **4.427×10⁻⁴ J/m³**; $u_B = B^2/(2\mu_0) = 10^{-4}/(2\times1.2566\times10^{-6}) = $ **39.79 J/m³**. Ratio **8.988×10⁴**: a modest magnetic field stores far more energy than a substantial electric field. (In SI units the two are equal when $E = cB$, which is the plane-wave case.)

### Solution 04-08.2

$\lambda = c/f$: **4997 km** at 60 Hz; **12.49 cm** at 2.4 GHz; **10.71 mm** at 28 GHz; **1.550 µm** at 193.4 THz.

### Solution 04-08.3

Delay $= L\sqrt{\varepsilon}/c$. Stripline: $0.3\times\sqrt{3.66}/c = $ **1.914 ns**. Microstrip: $0.3\times\sqrt{2.9}/c = $ **1.704 ns**. Skew **210.3 ps**: matched lengths on different layers do not give matched delays, which matters for differential pairs and parallel buses.

### Solution 04-08.4

The current is $i = C\,dv/dt$; for $v = V\sin\omega t$ its amplitude is $\omega CV = 2\pi\times10^6\times10^{-8}\times1 = $ **62.83 mA**. Inside the dielectric no charge flows, but the field $E = q/(\varepsilon A)$ changes, and the displacement current $\varepsilon\,d\Phi_E/dt = dq/dt$ equals the lead current exactly, so Ampère's law gives the same magnetic field around the capacitor as around its leads.

### Solution 04-08.5

$\langle S\rangle = E_0^2/(2\eta_0)$, so $E_0 = \sqrt{2\eta_0\times1000} = $ **868.0 V/m** and $B_0 = E_0/c = $ **2.895 µT**.

### Solution 04-08.6

(a) $\eta_2 = \eta_0/\sqrt4 = $ **188.4 Ω**.

(b) Incident, reflected and transmitted electric amplitudes $E_i$, $E_r$, $E_t$; the magnetic fields are $E/\eta$ with the reflected one reversed (it travels backward). Continuity of tangential E: $E_i + E_r = E_t$. Continuity of tangential H: $(E_i - E_r)/\eta_1 = E_t/\eta_2$. Eliminating $E_t$: $\Gamma = E_r/E_i = (\eta_2 - \eta_1)/(\eta_2 + \eta_1) = (188.4 - 376.7)/(565.1) = $ **−0.3333**: the reflected wave is inverted.

(c) Reflected power fraction $\Gamma^2 = $ **0.1111**; transmitted **0.8889**. The same formula, with $Z_0$ values, gives reflections on transmission lines ([13-07](../../13-electromagnetics/chapters/13-07-transmission-lines-time-domain.md)).

### Solution 04-08.7

(a) Between the conductors $E = V/(r\ln(b/a))$ (04-04) and $H = I/(2\pi r)$ (04-06), perpendicular, so $S = EH$, directed along the cable toward the load. At $r = a$: $\frac{10}{0.45\times10^{-3}\times1.1872}\times\frac{0.2}{2\pi\times0.45\times10^{-3}} = $ **1.324×10⁶ W/m²**.

(b) $\int_a^bS\,2\pi r\,dr = \int_a^b\frac{V}{r\ln(b/a)}\frac{I}{2\pi r}2\pi r\,dr = \frac{VI}{\ln(b/a)}\int_a^b\frac{dr}{r} = VI = $ **2 W** ✓. The power travels in the dielectric between the conductors, concentrated near the inner one.

### Solution 04-08.8

$\langle S\rangle = 0.2/(4\pi\times0.05^2) = $ **6.366 W/m²**. Rough because at 5 cm a phone's fields are in the reactive near field, not a simple outgoing spherical wave; the antenna is not isotropic; the body absorbs and reflects; and average transmit power is usually much lower. Compliance is therefore tested by SAR measurement.

### Solution 04-08.9

$\alpha = \pi f\sqrt{\varepsilon_r}\tan\delta/c = \pi\times28\times10^9\times1.913\times0.0037/c = $ **2.077 Np/m** = **18.04 dB/m**. At millimeter-wave frequencies even a low-loss laminate loses tens of dB per meter, which is why millimeter-wave front ends integrate antennas next to the chip.

### Solution 04-08.10

For a sinusoid, $J_c = \sigma E$ and $J_d = \varepsilon\,\partial E/\partial t$ has amplitude $\omega\varepsilon E$, so their ratio is $\omega\varepsilon/\sigma$.

(a) Copper: $2\pi\times10^9\times8.854\times10^{-12}/5.95\times10^7 = $ **9.350×10⁻¹⁰**: displacement current is utterly negligible in metals, even at gigahertz.

(b) Seawater: $2\pi\times10^9\times81\times8.854\times10^{-12}/4 = $ **1.127**: comparable. Seawater conducts well enough that radio waves are absorbed within centimeters to meters (the skin depth is small), which is why submarines use very low frequencies, where the skin depth is meters to tens of meters.

### Solution 04-08.11

$\partial^2E/\partial x^2 = -k^2E$ and $\partial^2E/\partial t^2 = -\omega^2E$, so the equation requires $k^2 = \mu\varepsilon\omega^2$, i.e. $\omega/k = 1/\sqrt{\mu\varepsilon}$. In $\varepsilon_r$ = 4.6 at 10 GHz, $\lambda = 13.98$ mm and $k = 2\pi/\lambda = $ **449.5 rad/m**.

### Solution 04-08.12

$t/L = \sqrt{\varepsilon_{\text{eff}}}/c$, so $\varepsilon_{\text{eff}} = (c\times5.9\ \text{ps/mm})^2 = (2.998\times10^8\times5.9\times10^{-9})^2 = $ **3.129**. A microstrip's field lies partly in the air above the trace (ε = 1) and partly in the laminate, so the wave sees a weighted average between 1 and 4.6.

### Solution 04-08.13

(a) $0.02/0.010 = $ **2 W/kg**: exactly at ICNIRP's local limit.

(b) $0.3\times0.02/0.001 = $ **6 W/kg**, nearly four times the FCC's 1.6 W/kg.

(c) The same exposure can pass a 10 g-averaged limit and fail a 1 g-averaged one, because small averaging volumes see hot spots. The numerical limits cannot be compared without their averaging masses; antenna design aims to spread absorbed power.

### Solution 04-08.14

$i = \omega CV = 2\pi\times10^7\times10^{-9}\times10 = $ **0.6283 A**. At the edge, the full displacement current is enclosed: $B = \mu_0i/(2\pi R) = $ **6.283 µT**.

### Solution 04-08.15

(a) Gauss's law around the inner conductor (charge λ per length) gives $E = \lambda/(2\pi\varepsilon r)$, and $V = \int_a^bE\,dr = (\lambda/2\pi\varepsilon)\ln(b/a)$, so $E(r) = V/\big(r\ln(b/a)\big)$, pointing radially outward. Ampère's law around the inner conductor gives $H(r) = I/(2\pi r)$, circling it. $\vec E$ and $\vec H$ are perpendicular, so $S = EH = \dfrac{VI}{2\pi r^2\ln(b/a)}$, directed along the cable toward the load. At $r$ = 1 mm: $E = 10/(10^{-3}\times\ln4)$ = **7213 V/m**, $H = 2/(2\pi\times10^{-3})$ = **318.3 A/m**, $S$ = **2.296×10⁶ W/m²**.

(b) $P = \int_a^bS\,2\pi r\,dr = \dfrac{VI}{\ln(b/a)}\int_a^b\frac{dr}{r} = VI$ = **20.00 W**, exactly the power the load absorbs. *Units:* (V/m)(A/m) = W/m², times area gives W ✓.

(c) Through the dielectric between the conductors. The copper only guides the fields (and, if resistive, absorbs a little power that flows into it from the surrounding field). The same picture explains why a cable's dielectric, not its conductors, sets the wave speed (§3.4 of the chapter).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 04-08.1a | electric energy density at 10 kV/m | 4.427×10^-4 | J/m³ |
| 04-08.1b | magnetic energy density at 10 mT | 39.79 | J/m³ |
| 04-08.1c | ratio | 8.988×10^4 | — |
| 04-08.2a | wavelength at 60 Hz | 4997 | km |
| 04-08.2b | wavelength at 2.4 GHz | 12.49 | cm |
| 04-08.2c | wavelength at 28 GHz | 10.71 | mm |
| 04-08.2d | wavelength at 193.4 THz | 1.550 | µm |
| 04-08.3a | stripline delay | 1.914 | ns |
| 04-08.3b | microstrip delay | 1.704 | ns |
| 04-08.3c | skew | 210.3 | ps |
| 04-08.4a | displacement current amplitude | 62.83 | mA |
| 04-08.5a | electric-field amplitude | 868.0 | V/m |
| 04-08.5b | magnetic-field amplitude | 2.895 | µT |
| 04-08.6a | dielectric wave impedance | 188.4 | Ω |
| 04-08.6b | reflection coefficient | −0.3333 | — |
| 04-08.6c | reflected power fraction | 0.1111 | — |
| 04-08.6d | transmitted power fraction | 0.8889 | — |
| 04-08.7a | Poynting vector at the inner conductor | 1.324×10^6 | W/m² |
| 04-08.7b | total power in the coax | 2 | W |
| 04-08.8a | intensity at 5 cm | 6.366 | W/m² |
| 04-08.9a | attenuation at 28 GHz | 2.077 | Np/m |
| 04-08.9b | attenuation at 28 GHz | 18.04 | dB/m |
| 04-08.10a | displacement/conduction ratio, copper | 9.350×10^-10 | — |
| 04-08.10b | displacement/conduction ratio, seawater | 1.127 | — |
| 04-08.11a | wavenumber at 10 GHz in ε_r 4.6 | 449.5 | rad/m |
| 04-08.12a | effective permittivity | 3.129 | — |
| 04-08.13a | SAR over 10 g | 2 | W/kg |
| 04-08.13b | SAR in the hottest 1 g | 6 | W/kg |
| 04-08.14a | current amplitude | 0.6283 | A |
| 04-08.14b | magnetic field at the edge | 6.283 | µT |
| 04-08.15a | field at 1 mm | 7213 | V/m |
| 04-08.15b | H at 1 mm | 318.3 | A/m |
| 04-08.15c | Poynting vector at 1 mm | 2.296×10^6 | W/m² |
| 04-08.15d | total power through the annulus | 20.00 | W |
