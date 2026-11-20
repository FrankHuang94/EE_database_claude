# Problems 13-03 · Magnetostatics and Inductance

Chapter: [13-03](../chapters/13-03-magnetostatics-and-inductance.md) · Worked solutions: [13-03 solutions](../solutions/13-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $\mu_0$ = 4π × 10⁻⁷ H/m (accurate to a part in 10⁹); $\varepsilon_0$ = 8.854 × 10⁻¹² F/m; lengths in metres unless stated; the unit normal at an interface points from medium 2 into medium 1; fringing at air gaps is neglected.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 13-03.1 [A]

**Two wires.** Two long parallel wires 1 cm apart carry 10 A each in opposite directions, in air. Find the flux density midway between them and the force per metre between them. Do they attract or repel?

### Problem 13-03.2 [A]

**Into iron.** Just above the plane $z$ = 0 (air), $\vec{B}_1 = 0.3\hat{x} + 1.2\hat{z}$ mT. Below is iron with $\mu_r$ = 500 and no surface current. Find the tangential $H$ in air, $\vec{B}_2$ in the iron, its magnitude, and the angles both fields make with the normal.

### Problem 13-03.3 [A]

**A toroid.** A toroid has 500 turns on an air core of rectangular cross-section, with inner radius 2 cm, outer radius 3 cm and height 1 cm. Find its inductance; its inductance if the core is ferrite with $\mu_r$ = 2000; and $H$ at the inner and outer radii at 1 A. How far off is the approximation that treats the core as a straight bar of the mean path length $2\pi \times 2.5$ cm?

### Problem 13-03.4 [B]

**The vector potential of a wire.** (a) Show that $\vec{A} = (\mu_0I/2\pi)\ln(\rho_0/\rho)\,\hat{z}$ gives the field of a long wire on the $z$ axis, for any constant $\rho_0$. (b) Use $\Phi = \oint\vec{A}\cdot d\vec\ell$ around a rectangle 1 m long to find the flux per metre between $\rho$ = 1 mm and $\rho$ = 1 cm at 1 A, and check it by integrating $B$ directly.

### Problem 13-03.5 [B]

**A loop and a Helmholtz pair.** (a) From the Biot–Savart law, derive the on-axis field of a circular loop of radius $R$ carrying current $I$. (b) For $R$ = 1 cm and $I$ = 1 A, find the field at the centre and 1 cm along the axis. (c) Two such loops share an axis, 1 cm apart (the spacing equals the radius), with the same current in the same direction. Find the field at the midpoint.

### Problem 13-03.6 [B]

**How long is long?** The coil of Example 13-03.3 (200 turns, radius 5 mm) is wound to lengths of 2 cm and 20 cm. The Nagaoka factors for these shapes are 0.8181 and 0.9791. Find the long-solenoid and corrected inductances for each, and how much the long formula overestimates in each case.

### Problem 13-03.7 [C]

**Design a gapped inductor.** You need 100 µH at a peak current of 5 A on a ferrite core ($\mu_r$ = 2000) with a 1 cm² cross-section and a 5 cm magnetic path, without the flux density exceeding 0.3 T. (a) Show that $LI = NBA$, and find the fewest whole turns. (b) Find the gap length that gives 100 µH with that many turns. (c) Find the peak flux density and the stored energy at 5 A, and the share of that energy stored in the gap.

### Problem 13-03.8 [B]

**Coupling into a loop.** A rectangular loop, 2 cm along the direction of a long straight wire and 1 cm across, lies in a plane with the wire, its near side 5 mm from the wire. (a) Find the mutual inductance. (b) The wire's current rises by 1 A in 1 ns. Find the voltage induced around the loop.

### Problem 13-03.9 [C]

**Internal inductance.** (a) For a round wire of radius $a$ carrying a uniformly distributed current, use the energy method to show that the internal inductance per metre is $\mu/8\pi$, whatever the radius. (b) For the coaxial line of Example 13-03.1 (outer conductor from 1.75 to 2.0 mm), find the low-frequency inductance per metre stored inside the outer conductor, and the total low-frequency inductance per metre. Compare with the external value.

### Problem 13-03.10 [B]

**A wire over a ground plane in a dielectric.** A round wire of radius 0.1 mm has its axis 0.3 mm above a ground plane, embedded in a uniform dielectric with $\varepsilon_r$ = 4.3. Find $L'$, $C'$, $\sqrt{L'/C'}$, and the delay $\sqrt{L'C'}$ in picoseconds per millimetre.

### Problem 13-03.11 [B]

**Parallel bond wires.** A chip grounds its I/O ring through 4 bond wires in parallel, each with a partial self-inductance of 1 nH. (a) Ignoring coupling, find the effective inductance. (b) Each pair of wires has a mutual inductance of 0.3 nH (taken equal for all pairs). Find the effective inductance now. (c) Find the ground bounce for a 100 mA current step in 100 ps in each case.

### Problem 13-03.12 [C]

**An E-core.** An E-shaped ferrite core ($\mu_r$ = 2000) carries a 50-turn winding on its centre leg. The centre leg has a 2 cm² cross-section, a 4 cm magnetic path and a 0.5 mm gap; each outer leg has a 1 cm² cross-section and an 8 cm path (including its share of the yokes). Draw the magnetic circuit, find each reluctance, the inductance, the gap's share of the total reluctance, and the flux densities in the centre and outer legs at 1 A.

### Problem 13-03.13 [C]

**A square loop from partial inductances.** A square loop of wire, 1 cm on a side, has wire radius 0.1 mm. The partial mutual inductance of two parallel filaments of length $\ell$ a distance $d$ apart is $M_p = (\mu_0/2\pi)\,[\ell\sinh^{-1}(\ell/d) - \sqrt{\ell^2 + d^2} + d]$, and a side's partial self-inductance is $M_p$ with $d$ = $a$. (a) Find each side's partial self-inductance and the partial mutual inductance of opposite sides. (b) Why do perpendicular sides contribute nothing, and why do opposite sides subtract? (c) Find the loop inductance, and compare with the textbook square-loop formula $(2\mu_0s/\pi)\,[\ln(s/a) - 0.774]$.

### Problem 13-03.14 [C]

**The force on a gap.** (a) For a magnetic circuit holding a fixed flux $\Phi$, write the stored energy in terms of the reluctance, and use virtual work on the gap length to show that the faces of a gap of area $A$ attract with force $B^2A/(2\mu_0)$. (b) Find the force across the gap of Example 13-03.4 at 1 A, and the force if the same gap carried 0.3 T.

---

## Objective coverage

| Learning objective (chapter 13-03) | Problems |
|---|---|
| 1. Ampère's law and the Biot–Savart law | 1, 3, 5 |
| 2. The vector potential and flux | 4, 13 |
| 3. Boundary conditions on $\vec{B}$ and $\vec{H}$ | 2 |
| 4. Inductance of practical structures | 3, 6, 8, 9, 10, 11, 13 |
| 5. Magnetic circuits and air gaps | 7, 12, 14 |
