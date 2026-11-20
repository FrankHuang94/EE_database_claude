# Problems 13-04 · Maxwell's Equations and Time-Varying Fields

Chapter: [13-04](../chapters/13-04-maxwells-equations.md) · Worked solutions: [13-04 solutions](../solutions/13-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $\varepsilon_0$ = 8.854 × 10⁻¹² F/m; $\mu_0$ = 4π × 10⁻⁷ H/m; $c$ = 2.998 × 10⁸ m/s; $\eta_0$ = 376.7 Ω; phasors are peak amplitudes with a cosine reference.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 13-04.1 [A]

**Hum in a loop.** A 10 cm × 10 cm wiring loop sits near a power transformer, where the 60 Hz magnetic field through it is uniform at 0.2 mT peak. Find the peak EMF induced around the loop.

### Problem 13-04.2 [A]

**Displacement current in air.** A 1 GHz field of 1 kV/m peak exists in air. Find the peak displacement current density.

### Problem 13-04.3 [A]

**Relaxation in silicon.** Find the charge relaxation time of silicon ($\varepsilon_r$ = 11.7) doped to a resistivity of 0.5 Ω·cm, and of intrinsic silicon with a resistivity of about 2.3 × 10⁵ Ω·cm. Above roughly what frequency does each behave as a dielectric?

### Problem 13-04.4 [B]

**From $\vec{H}$ to $\vec{E}$.** In free space, $\tilde{\vec{H}} = 0.1e^{-j2z}\,\hat{y}$ A/m (with $z$ in metres). (a) Find ω and the frequency. (b) Use the Ampère–Maxwell law to find $\tilde{\vec{E}}$, and write $\vec{E}(z, t)$. (c) Find the time-average Poynting vector.

### Problem 13-04.5 [A]

**Continuity.** In a region, the current density is $\vec{J} = J_0(x/a)\,\hat{x}$ with $J_0$ = 1 A/m² and $a$ = 1 cm. Find the rate of change of the charge density. Is charge building up or draining away?

### Problem 13-04.6 [B]

**A lossy laminate.** A board dielectric has $\varepsilon_r'$ = 4.3 and $\tan\delta$ = 0.02 at 1 GHz. Find its equivalent conductivity at 1 GHz and the time-average power dissipated per cubic metre by a 100 V/m peak field.

### Problem 13-04.7 [B]

**Charging a capacitor, seen from the fields.** An air-filled capacitor has circular plates of radius 1 cm, 1 mm apart. Its voltage is rising at 1 kV/µs and is 100 V at the instant of interest. Find the capacitance, the displacement current, $H$ at the rim of the gap, the Poynting vector there, and the total power flowing in through the rim. Show it equals $d/dt(\tfrac12Cv^2)$.

### Problem 13-04.8 [B]

**A safe distance.** An antenna radiates with an effective isotropic radiated power (EIRP) of 1 kW at 2 GHz. Using the far-field formula $S = \text{EIRP}/(4\pi r^2)$, find the distance at which the power density falls to the US general-population limit of 1 mW/cm², and the rms electric field there.

### Problem 13-04.9 [A]

**Lumped or not?** For a board dielectric with $\varepsilon_r$ = 4, find the wavelength at 1 GHz and the longest trace that a λ/10 rule would treat as lumped at 1 GHz and at 10 GHz.

### Problem 13-04.10 [B]

**Power between the planes.** A circuit board delivers 10 A at 1.0 V through a pair of wide supply and ground planes, 2 cm wide and 0.1 mm apart. Treating the fields between the planes as uniform, find $E$, $H$ and the Poynting vector between them, and the total power flow. Where does the power travel?

### Problem 13-04.11 [C]

**Loss in a capacitor, two ways.** A parallel-plate capacitor has 1 cm² plates 1 mm apart, filled with the laminate of Problem 13-04.6 (take $\tan\delta$ = 0.02 at 100 MHz too). It has 10 V peak across it at 100 MHz. (a) Find the equivalent conductivity at 100 MHz and the power dissipated from $\tfrac12\sigma_{eff}\lvert E\rvert^2$ integrated over the volume. (b) Model the capacitor as $C$ in parallel with $G = \omega C\tan\delta$, and find $C$, $G$ and $\tfrac12GV^2$.

### Problem 13-04.12 [B]

**A generator.** A coil of 100 turns, each of area 0.01 m², rotates at 60 revolutions per second in a uniform field of 0.5 T, about an axis perpendicular to the field. Find the peak and rms EMF.

### Problem 13-04.13 [C]

**A waveguide field.** In an air-filled rectangular pipe of width $a$, consider $\tilde{\vec{E}} = E_0\sin(\pi x/a)\,e^{-j\beta z}\,\hat{y}$. (a) Show that it satisfies the Helmholtz equation if $\beta^2 = \omega^2\mu_0\varepsilon_0 - (\pi/a)^2$, and that it is zero on the side walls $x$ = 0 and $x = a$. (b) For $a$ = 22.86 mm (the WR-90 size), find the frequency below which β is imaginary (no propagation), and β and the guide wavelength $2\pi/\beta$ at 10 GHz.

### Problem 13-04.14 [C]

**Light from circuits.** (a) Derive the Helmholtz equation for $\tilde{\vec{H}}$ in a source-free, lossless, uniform region. (b) From $\mu_0$ and $\varepsilon_0$ alone, compute the speed of an electromagnetic wave and the ratio $\sqrt{\mu_0/\varepsilon_0}$.

### Problem 13-04.15 [C]

**Is this field allowed?** Between perfectly conducting walls at $x = 0$ and $x = a$ (air, no free charge or current inside), a proposed field is $\vec{E} = E_0\sin(\pi x/a)\cos(\omega t - \beta z)\,\hat{y}$ with $E_0$ = 2 kV/m, $a$ = 22.86 mm and $f$ = 10 GHz. (a) Show that it satisfies Gauss's law and the boundary condition on the walls. (b) Find $\vec{H}$ from Faraday's law. (c) Substitute into Ampère's law and find the β for which the field is a solution of Maxwell's equations; evaluate it. (d) Find the amplitudes of $H_x$ and $H_z$.

---

## Objective coverage

| Learning objective (chapter 13-04) | Problems |
|---|---|
| 1. Maxwell's equations in integral and differential form | 1, 5, 12, 14, 15 |
| 2. The displacement current | 2, 7 |
| 3. Conductors, dielectrics and relaxation | 3, 6, 11 |
| 4. Phasor form | 4, 13, 14 |
| 5. The Poynting theorem | 4, 7, 8, 10, 11 |
| 6. When circuit theory is enough | 9 |
