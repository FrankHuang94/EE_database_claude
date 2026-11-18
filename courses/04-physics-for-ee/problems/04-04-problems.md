# Problems 04-04 · Electric Potential, Capacitance and Dielectrics

Chapter: [04-04](../chapters/04-04-potential-capacitance-and-dielectrics.md) · Worked solutions: [04-04 solutions](../solutions/04-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $e = 1.602176634\times10^{-19}$ C; $\varepsilon_0 = 8.8541878188\times10^{-12}$ F/m and $k_e = 1/(4\pi\varepsilon_0)$; SiO₂ $\varepsilon_r$ = 3.9. Potentials are zero at infinity unless stated. Air breaks down at 3 MV/m. Answers to 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 04-04.1 [A]

**Potential and work.** A 5 nC point charge sits at the origin. (a) Find the potential 10 cm and 30 cm away. (b) How much work must you do to move a 1 nC charge from 30 cm to 10 cm?

### Problem 04-04.2 [A]

**Electron-volts.** (a) Express 1 keV in joules. (b) An electron moves from a point at 0 V to a point at +5 V. Find the change in its potential energy in joules. (c) If it started at rest and only the field acted, what is its kinetic energy in eV?

### Problem 04-04.3 [A]

**A uniform field.** A uniform field of 500 V/m points along $+x$. Find $V(4\ \text{cm}, 0) - V(0, 0)$ and $V(0, 4\ \text{cm}) - V(0, 0)$. Which way do the equipotentials run?

### Problem 04-04.4 [B]

**The disk's potential.** A disk of radius 1 cm carries a uniform 1 µC/m². (a) Find the potential on its axis 1 mm from the center and at the center. (b) Differentiate the potential to find the field at 1 mm, and compare it with Example 04-02.5.

### Problem 04-04.5 [B]

**A dipole's potential and field.** A dipole of moment $10^{-12}$ C·m points along $z$. At $r$ = 10 cm and θ = 60° from its axis, (a) find the potential, and (b) find the field's radial and angular components from $E_r = -\partial V/\partial r$ and $E_\theta = -(1/r)\,\partial V/\partial\theta$, and its magnitude.

### Problem 04-04.6 [B]

**Two spheres joined by a wire.** Conducting spheres of radii 1 cm and 10 cm, far apart, are connected by a thin wire and carry 22 nC in total. Find (a) the charge on each, (b) their common potential, (c) each surface field and (d) each surface charge density.

### Problem 04-04.7 [B]

**A capacitor network.** Capacitors of 2 µF and 3 µF in series are connected in parallel with a 4 µF capacitor, and 10 V is applied across the combination. Find (a) the equivalent capacitance, (b) the charge on the series pair, (c) the voltage across the 2 µF and 3 µF capacitors, and (d) the total stored energy.

### Problem 04-04.8 [B]

**A half-filled gap.** Plates of 100 cm² are 2 mm apart. (a) A 1 mm slab with $\varepsilon_r$ = 4 fills half the gap's thickness. Find $C$, and with 100 V applied, the field and voltage in the air and in the slab. (b) Instead, a slab 2 mm thick with $\varepsilon_r$ = 4 fills half the plates' *area*. Find $C$.

### Problem 04-04.9 [B]

**A cable's capacitance.** A coaxial cable has an inner conductor 0.9 mm in diameter and a dielectric 2.95 mm in diameter (take $\varepsilon_r$ = 2.25). Find its capacitance per meter, and the capacitance of a 1.5 m length.

### Problem 04-04.10 [B]

**Energy two ways.** (a) Find the energy density of a 3 MV/m field in air. (b) An isolated conducting sphere of radius 10 cm is held at 100 kV. Find its stored energy from $\tfrac12CV^2$, then confirm it by integrating $\tfrac12\varepsilon_0E^2$ over all space outside the sphere.

### Problem 04-04.11 [C]

**Designing a high-voltage coax.** (a) For a coax of fixed outer radius $b$ in a medium that breaks down at $E_{\text{bd}}$, prove that the breakdown voltage is maximized when $b/a = e$. (b) For $b$ = 5 mm in air, find the optimal $a$ and the maximum voltage. (c) Compare with $a$ = 0.5 mm.

### Problem 04-04.12 [B]

**Decoupling with derated MLCCs.** A processor's load current steps by 2 A for 0.5 µs before the regulator responds, and the charge comes from a decoupling capacitor. Find the voltage droop with (a) the nominal 100 µF, (b) 90 µF (an X5R part at 1.8 V, per Murata's example), and (c) 60 µF (a Y5V part at the same bias).

### Problem 04-04.13 [C]

**Designing a gate stack.** A gate stack must reach an EOT of 0.9 nm using a 0.4 nm SiO₂ interface layer under HfO₂ ($\varepsilon_r$ = 25). (a) How thick must the HfO₂ be? (b) What is the total physical thickness? (c) What is the capacitance per area, in µF/cm²?

### Problem 04-04.14 [C]

**DRAM sense margin.** A cell of 8 fF stores 1.1 V (a "1") and shares charge with an 80 fF bit line precharged to 0.55 V. (a) Find the bit-line signal. (b) The sense amplifier needs at least 40 mV. What is the lowest cell voltage that still reads as a "1"? (c) How much voltage, charge and how many electrons may the cell lose to leakage before the next refresh?

### Problem 04-04.15 [C]

**A chuck with a gap.** For the electrostatic chuck of Example 04-04.8 (200 mm wafer, alumina $\varepsilon_r$ = 8.8 and 0.54 mm thick, 1 kV), find the clamping force with a uniform vacuum gap of (a) 0, (b) 1 µm and (c) 10 µm, using $F = \varepsilon_0SV^2/[2(g + l/\varepsilon_r)^2]$. (d) Why are chucks so sensitive to particles and wafer bow?

### Problem 04-04.16 [C]

**A sphere's capacitance from its field energy.** A conducting sphere of radius 5 cm carries 10 nC. (a) Integrate $\tfrac12\varepsilon_0E^2$ over all space to find its energy. (b) Use $U = Q^2/2C$ to find $C$, and compare with $4\pi\varepsilon_0R$. (c) What fraction of the energy lies within one radius of the surface ($R < r < 2R$)?

---

## Objective coverage

| Learning objective (chapter 04-04) | Problems |
|---|---|
| 1. Conservative field, potential energy and potential | 1, 2, 3, 4, 5 |
| 2. Field as negative gradient; equipotentials; conductors | 3, 4, 5, 6 |
| 3. Capacitance and combinations | 7, 8, 9, 11, 16 |
| 4. Dielectrics, layered stacks, EOT, real capacitors | 8, 9, 12, 13 |
| 5. Energy, energy density, charge sharing and force | 10, 14, 15, 16 |
