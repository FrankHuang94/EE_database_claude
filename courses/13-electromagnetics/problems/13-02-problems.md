# Problems 13-02 · Electrostatics: Boundary Conditions and Boundary-Value Problems

Chapter: [13-02](../chapters/13-02-electrostatics-boundary-value-problems.md) · Worked solutions: [13-02 solutions](../solutions/13-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $\varepsilon_0$ = 8.854 × 10⁻¹² F/m; $q$ = 1.602 × 10⁻¹⁹ C; lengths in metres unless stated; the unit normal at an interface points from medium 2 into medium 1.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 13-02.1 [A]

**Charge on a conductor.** The field just outside a conductor in air is 2 MV/m. Find the surface charge density there, and the largest surface charge density a conductor in air can hold if air breaks down at 3 MV/m.

### Problem 13-02.2 [A]

**Into glass.** Just above the plane $z$ = 0 (air), $\vec{E}_1 = 2\hat{x} + 6\hat{z}$ kV/m. Below is glass with $\varepsilon_r$ = 6 and no surface charge. Find $\vec{E}_2$, its magnitude, and the angles both fields make with the normal.

### Problem 13-02.3 [A]

**A gate stack.** A transistor gate dielectric is 1 nm of SiO₂ ($\varepsilon_r$ = 3.9) under 3 nm of a high-permittivity layer with $\varepsilon_r$ = 20 (illustrative). Find its equivalent oxide thickness and its capacitance per area in fF/µm².

### Problem 13-02.4 [B]

**Concentric spheres.** Solve Laplace's equation for the region between concentric conducting spheres of radii 1 cm and 2 cm in air, and find their capacitance. What is the capacitance of the inner sphere alone, with the outer sphere removed to infinity?

### Problem 13-02.5 [B]

**The best coaxial cable for voltage.** An air-filled coaxial line has a fixed outer radius of 5 mm. Air breaks down at 3 MV/m. Find the inner radius that maximizes the voltage the line can hold, and that voltage.

### Problem 13-02.6 [B]

**A depletion region.** The depleted side of a one-sided silicon junction ($\varepsilon_r$ = 11.7) has a uniform acceptor density of 10¹⁶ cm⁻³ over a width of 0.3 µm, and the field is zero at its far edge. Solve Poisson's equation for the voltage across it and the peak field.

### Problem 13-02.7 [B]

**A wide trough.** A rectangular trough is 2 cm wide and 1 cm high; its top is at 10 V and its other three sides are grounded. Find the potential at the centre from the first term of the series, from the first three nonzero terms, and from the converged series.

### Problem 13-02.8 [B]

**A line charge above a plane.** A line charge of 1 nC/m runs 1 cm above a grounded plane. Find the peak induced surface charge density, show that the total induced charge per metre is −1 nC/m, and find the force per metre on the line charge.

### Problem 13-02.9 [B]

**A two-wire line.** Two parallel wires of radius 0.5 mm are 6 mm apart, centre to centre, in air. Find their capacitance per metre, and compare with the thin-wire approximation $\pi\varepsilon_0/\ln(D/a)$.

### Problem 13-02.10 [B]

**A charge in a corner.** A 1 nC charge sits 1 cm from each of two grounded conducting half-planes that meet at a right angle. Place the image charges, and find the force on the charge (magnitude and direction).

### Problem 13-02.11 [C]

**Why images work, and when they fail.** (a) Prove the uniqueness theorem for Laplace's equation with the potential given on the whole boundary. (b) Use it to justify the image solution for a charge above a grounded plane. (c) Explain why images cannot be used for a charge between two grounded planes meeting at 120°.

### Problem 13-02.12 [C]

**Finite differences by hand.** Divide the square trough of Example 13-02.4 (top at 1 V) into a 3 × 3 grid of cells, giving four interior nodes. Write the finite-difference equation for each node, solve them, and compare with the exact series values at the same points.

### Problem 13-02.13 [C]

**Capacitance by energy.** For the coaxial line of Example 13-02.2 ($a$ = 0.5 mm, $b$ = 1.75 mm, $\varepsilon_r$ = 2.25) at 100 V, integrate the stored energy per metre over the dielectric and recover the capacitance per metre from $C' = 2W'_e/V_0^2$.

### Problem 13-02.14 [C]

**When the thin-wire formula fails.** For a wire of radius $a$ with its axis at height $h$ over a ground plane, find the thin-wire formula's error at $h/a$ = 2, 5, 10 and 20, and the height ratio below which the error exceeds 1%.

### Problem 13-02.15 [C]

**A sphere in a uniform field.** A grounded conducting sphere of radius $a$ = 1 mm sits in a field that is uniform, $E_0\hat{z}$ with $E_0$ = 1 MV/m, far from it. (a) Using separation of variables in spherical coordinates (solutions $r^nP_n(\cos\theta)$ and $r^{-(n+1)}P_n(\cos\theta)$, with $P_1 = \cos\theta$), find the potential outside the sphere. (b) Find the surface charge density, its largest value, and the largest field at the surface. (c) Show that the total induced charge is zero, and find the induced dipole moment.

### Problem 13-02.16 [C]

**Graded insulation.** A coaxial cable has an inner conductor of radius 0.5 mm and an outer conductor of radius 2 mm. The insulation is two layers: $\varepsilon_r$ = 4 from 0.5 to 1 mm and $\varepsilon_r$ = 2 from 1 to 2 mm. (a) Find the capacitance per metre. (b) At 1 kV, find the field at the inner conductor, on each side of the interface, and at the outer conductor. (c) Compare the largest field with that of a cable insulated throughout with $\varepsilon_r$ = 2, and explain why high-voltage cables grade their insulation this way.

---

## Objective coverage

| Learning objective (chapter 13-02) | Problems |
|---|---|
| 1. Boundary conditions at conductors and dielectric interfaces | 1, 2, 3, 15, 16 |
| 2. Poisson and Laplace in one dimension; uniqueness | 4, 5, 6, 11, 13 |
| 3. Separation of variables | 7, 12, 15 |
| 4. The method of images | 8, 9, 10, 11, 14 |
| 5. Capacitance of real structures and numerical solution | 3, 4, 9, 12, 13, 14, 16 |
