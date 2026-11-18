# Problems 04-03 · Gauss's Law

Chapter: [04-03](../chapters/04-03-gauss-law.md) · Worked solutions: [04-03 solutions](../solutions/04-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $e = q = 1.602176634\times10^{-19}$ C; $\varepsilon_0 = 8.8541878188\times10^{-12}$ F/m and $k_e = 1/(4\pi\varepsilon_0)$; silicon $\varepsilon_r$ = 11.7, SiO₂ $\varepsilon_r$ = 3.9. Charges are in vacuum (or air) unless stated. On closed surfaces the normal points outward. Answers to 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 04-03.1 [A]

**Flux through a roof.** A uniform field of 500 V/m points straight down. (a) Find the magnitude of the flux through a flat horizontal roof of 2 m × 3 m. (b) The roof is tilted 40° from horizontal, keeping its 2 m × 3 m size. Find the flux magnitude now. (c) What is the net flux out of a closed shed sitting in this field?

### Problem 04-03.2 [A]

**Charge from flux.** The net outward flux through a closed surface is measured as −5000 V·m. (a) Find the enclosed charge. (b) Can you tell from this one number where inside the surface the charge sits, or whether other charges sit outside? Explain.

### Problem 04-03.3 [A]

**Coulomb's law from Gauss's law.** (a) Starting from Gauss's law and the symmetry of a point charge, derive Coulomb's law for the force between two point charges. (b) Find the field 10 cm from a 5 nC charge. (c) Find the flux of that charge through a sphere of radius 10 cm and through a cube of side 1 m centered on the charge.

### Problem 04-03.4 [B]

**A charge at a cube's corner.** An 8 nC charge sits exactly at one corner of a cube of side 10 cm. (a) What is the flux through the cube? (Hint: imagine the eight cubes that meet at that corner.) (b) Which faces carry no flux, and what is the flux through each of the others?

### Problem 04-03.5 [B]

**Shell plus point charge.** A thin spherical shell of radius 10 cm carries +20 nC, and a −5 nC point charge sits at its center. Find the magnitude and direction of the field at 5 cm and at 15 cm from the center.

### Problem 04-03.6 [B]

**A charged rod.** A long cylinder of radius 1 mm holds a uniform volume charge density of 0.01 C/m³. (a) Use Gauss's law to find $E(r)$ inside and outside. (b) Evaluate it at 0.5 mm, 1 mm and 5 mm.

### Problem 04-03.7 [B]

**Nested cylinders.** A long thin cylindrical shell of radius 1 cm carries +3 nC/m, and a coaxial shell of radius 3 cm carries −1 nC/m. Find the field at 0.5 cm, 2 cm and 4 cm from the axis.

### Problem 04-03.8 [B]

**A charged slab.** A large slab 2 mm thick holds a uniform charge density of 1×10⁻⁴ C/m³. (a) Find the field at its midplane, 0.5 mm from the midplane, at its surface and 1 cm outside it. (b) Sketch $E(x)$.

### Problem 04-03.9 [B]

**How much charge can a conductor hold?** A flat metal surface in air sparks when the field just outside reaches 3 MV/m. (a) Find the largest surface charge density it can hold. (b) Express it in electrons per cm². (c) Atoms on a metal surface are about 0.3 nm apart. What fraction of surface atoms carries an extra electron at this charge?

### Problem 04-03.10 [B]

**A charge in a cavity of a charged conductor.** A conducting sphere of radius 5 cm carries a net +3 nC and has a small cavity inside it, holding a +2 nC point charge (not necessarily at the center). (a) How much charge sits on the cavity wall and on the outer surface? (b) Is the outer surface charge uniform? Why? (c) Find the outer surface charge density and the field 10 cm from the sphere's center.

### Problem 04-03.11 [C]

**Two plates, unequal charges.** Two large parallel conducting plates, each of area 100 cm², face each other. Plate A carries +4 nC and plate B carries −1 nC. (a) Find the charge on each of the four surfaces. (Use: the field inside each plate's metal is zero, and the field of each surface sheet is σ/(2ε₀).) (b) Find the field between the plates and outside them.

### Problem 04-03.12 [B]

**A one-sided junction.** A silicon junction has $N_A = 10^{18}$ cm⁻³ and $N_D = 10^{15}$ cm⁻³, and its depletion region extends 1.0 µm into the n side. (a) Find $x_p$. (b) Find the peak field in V/m and kV/cm. (c) Find the area under the field profile.

### Problem 04-03.13 [C]

**Fields across an oxide–silicon interface.** A gate oxide carries a field of 5 MV/cm, and there is no free charge at the oxide–silicon interface. (a) Using a pillbox that straddles the interface, show that $\varepsilon_{\text{ox}}E_{\text{ox}} = \varepsilon_{\text{Si}}E_{\text{Si}}$. (b) Find the field in the silicon just below the interface. (c) Find the free charge per unit area on the gate, in C/m² and in electrons per cm².

### Problem 04-03.14 [C]

**A uniform field in a hole.** A large sphere holds a uniform charge density ρ = 1×10⁻⁶ C/m³. A spherical cavity is cut out of it, with the cavity's center a distance 2 cm from the sphere's center. (a) Using superposition (the sphere plus a sphere of density −ρ filling the cavity) and the field inside a uniform sphere, show that the field everywhere in the cavity is uniform and equals $\rho\vec d/(3\varepsilon_0)$, where $\vec d$ points from the sphere's center to the cavity's center. (b) Find its magnitude.

### Problem 04-03.15 [C]

**Touch-pad overlay design.** A self-capacitance button 10 mm in diameter has a parasitic capacitance of 20 pF. Model the finger as a conducting disk covering the button. Compare (a) a 1.5 mm glass overlay (take $\varepsilon_r$ = 7) with (b) a 3 mm acrylic overlay (take $\varepsilon_r$ = 2.6): find $C_F$ and the percentage change in total capacitance for each, and their ratio. (c) Why is the parallel-plate estimate an upper bound?

### Problem 04-03.16 [C]

**Testing the inverse square.** Suppose the field of a point charge were $E = k_eq/r^{2+\delta}$. (a) Show that the flux through a concentric sphere of radius $r$ is $(q/\varepsilon_0)\,r^{-\delta}$ (with $r$ in meters). (b) For δ = 0.01, find the ratio of the flux through a 2 m sphere to that through a 1 m sphere. (c) Explain why a measurement of the field inside a charged closed conducting shell tests δ so sensitively.

---

## Objective coverage

| Learning objective (chapter 04-03) | Problems |
|---|---|
| 1. Electric flux through open and closed surfaces | 1, 2, 3, 4 |
| 2. Gauss's law, its derivation and the inverse square | 3, 4, 16 |
| 3. Symmetric distributions and Gaussian surfaces | 5, 6, 7, 8, 14 |
| 4. Conductors in equilibrium and shielding | 9, 10, 11 |
| 5. Materials: junctions, interfaces and capacitive sensing | 12, 13, 15 |
