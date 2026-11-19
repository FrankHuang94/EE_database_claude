# Problems 09-01 · Crystals, Energy Bands and the Semiconductor

Chapter: [09-01](../chapters/09-01-crystals-and-energy-bands.md) · Worked solutions: [09-01 solutions](../solutions/09-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** lattice constants in Å (1 Å = 10⁻⁸ cm); energies in eV; $m_0$ is the free-electron mass. Use CODATA constants: $\hbar$ = 1.054572 × 10⁻³⁴ J·s, $m_0$ = 9.109384 × 10⁻³¹ kg, $q$ = 1.602177 × 10⁻¹⁹ C, $N_A$ = 6.022141 × 10²³ mol⁻¹, $hc/q$ = 1239.84 nm·eV and $kT/q$ = 25.85 mV at 300 K. Material data, unless a problem gives its own, are those of the chapter (§3 and Example 09-01.6).

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 09-01.1 [A]

**The germanium crystal.** Germanium has the diamond structure with $a$ = 5.658 Å, and its handbook density is 5.3234 g/cm³. Find (a) the atomic density, (b) the nearest-neighbor (bond) distance, (c) the second-nearest-neighbor distance (the distance between two FCC lattice points), and (d) the molar mass that the density implies.

### Problem 09-01.2 [A]

**Naming planes.** Give the Miller indices of the planes that cut the axes at (a) $a$, $a$, $a$; (b) $a/2$, ∞, $a$; (c) $-a$, $a$, ∞; (d) $3a$, $2a$, $6a$. (e) Find the spacing of the plane family in (d) for silicon.

### Problem 09-01.3 [A]

**Angles in the cube.** (a) Find the angle between the (110) and (111) planes. (b) Find the angle between the (111) and (1̄11) planes, two faces of the octahedron that bounds anisotropic etch pits. (c) Does the direction [11̄0] lie in the (111) plane? (d) In the diamond structure, the atom at the origin bonds to neighbors at $(a/4)(1,1,1)$ and $(a/4)(1,\bar1,\bar1)$. Find the bond angle.

### Problem 09-01.4 [A]

**GaAs surfaces.** GaAs has the zinc-blende structure with $a$ = 5.65325 Å. (a) Find the total number of atoms per cm³. (b) Explain why a (100) atomic plane of GaAs contains only one element, and find the number of atoms per cm² on it. (c) The (111) atomic planes are also single-element. Find their areal density.

### Problem 09-01.5 [B]

**Orientation in fabrication.** A silicon wafer has a (001) surface. (a) A FinFET's fin runs along [110]. Which crystal plane forms its sidewalls? (b) Which plane would form them if the fin ran along [100]? (c) An anisotropic wet etch stops on {111} planes. A 10.00 µm-wide square opening in an oxide mask on the wafer, with edges along ⟨110⟩, etches into an inverted pyramid whose four sidewalls are {111} planes. Find the angle between a sidewall and the surface, the final depth and the length of a sidewall measured straight down its slope from the rim to the apex.

### Problem 09-01.6 [B]

**A weaker lattice.** Repeat Example 09-01.3 for a delta-function comb with $P$ = 1.5 and $d$ = 0.4 nm (mass $m_0$). Find (a) $E_d$; (b) the first band's bottom ($x_b$ and energy), top and width; (c) the bottom of the second band and the width of the first gap; (d) the effective mass at the bottom of the first band. (e) Compare with Example 09-01.3 and explain each difference.

### Problem 09-01.7 [C]

**The strong-barrier limit.** For the delta-function comb with large $P$: (a) Show that the bottom of the first band is near $x_b \approx \pi(1 - 2/P)$, and that the first band's width is approximately $4\pi^2E_d/P$. (*Hint:* write $x = \pi - \epsilon$ with small $\epsilon$.) (b) For $P$ = 20 and $P$ = 50, find the exact $x_b$ and band width (in units of $E_d$) numerically, and the relative error of the approximate width. (c) What physical process does the shrinking width describe, and how does the effective mass behave as $P$ grows?

### Problem 09-01.8 [B]

**A tight-binding band.** In the tight-binding picture of 04-11, a band of a one-dimensional crystal of period $d$ is $E(k) = E_0 - 2t\cos kd$, where $t$ is the coupling energy between neighboring atoms. Take $t$ = 0.5 eV and $d$ = 0.3 nm. (a) Find the band width. (b) Find the effective mass $m^* = \hbar^2/(d^2E/dk^2)$ at the band bottom and at the band top. (c) Find the largest group velocity $v_g = (1/\hbar)\,dE/dk$ and the $k$ at which it occurs.

### Problem 09-01.9 [B]

**Germanium's masses.** Germanium's conduction band has four equivalent valleys (along ⟨111⟩, at the L points) with $m_l$ = 1.6 $m_0$ and $m_t$ = 0.08 $m_0$; its hole masses are $m_{hh}$ = 0.33 $m_0$ and $m_{lh}$ = 0.043 $m_0$ [handbook, chapter source 3]. (a) Find the conductivity mass of electrons. (b) Find the density-of-states mass of one valley and of all four. (c) Find $N_C$ at 300 K and compare with Hu's 1.04 × 10¹⁹ cm⁻³. (d) Find $m_{dp}$ and $N_V$ and compare with Hu's 6.0 × 10¹⁸ cm⁻³. (e) Explain the larger disagreement in (d).

### Problem 09-01.10 [B]

**Reading band diagrams.** (a) n-type silicon ($\chi$ = 4.05 eV) has $E_C - E_F$ = 0.25 eV. Find its work function. A metal with work function 4.50 eV is to be brought into contact with it: by how much do their Fermi levels differ beforehand, and which way will electrons flow on contact? (b) In a band diagram, $E_C$ falls by 0.30 eV from left to right over 50 nm, linearly. Find the electric field (magnitude and direction) and the direction in which electrons and holes drift. (c) An electron starts at rest at the conduction-band edge on the left and crosses the region without scattering. What is its kinetic energy on the right?

### Problem 09-01.11 [B]

**A laser's temperature drift.** A GaAs laser emits close to the band-gap energy. Using Varshni's fit for GaAs, find (a) the gap at 77 K, 300 K and 400 K; (b) $dE_g/dT$ at 300 K; (c) the emission wavelength at 300 K and its rate of change $d\lambda/dT$ in nm/K; (d) the wavelength at 350 K and the shift from 300 K. (e) Why do optical-communication lasers sit on temperature-controlled mounts?

### Problem 09-01.12 [B]

**Strain from mismatch.** (a) Using Vegard's law, find the lattice constant of relaxed Si$_{0.75}$Ge$_{0.25}$, its mismatch to silicon, and the in-plane strain $(a_{Si} - a_{layer})/a_{layer}$ in a thin layer grown coherently on silicon. Is the layer under tension or compression? (b) Find the lattice constant of Ga$_{0.40}$In$_{0.60}$As and its mismatch to InP.

### Problem 09-01.13 [C]

**Designing an extended-wavelength detector.** A gas-sensing detector must absorb out to 2.00 µm at 300 K. (a) What gap does that require? (b) Using the Ga$_{1-y}$In$_y$As model of Example 09-01.6 (end-point gaps at 300 K, bowing 0.477 eV), find the indium fraction $y$ that gives this gap. (c) Find the alloy's lattice constant and its mismatch to InP. (d) Find the cutoff wavelength of pure InAs at 300 K. What does (c) imply for growing the detector on InP?

### Problem 09-01.14 [B]

**Splitting the valleys.** Strain lowers silicon's two out-of-plane conduction valleys by $\Delta E$ relative to the four in-plane ones. All six valleys have the same density-of-states mass, so in equilibrium (non-degenerate) each valley's population is proportional to $e^{-E_{\text{valley}}/kT}$. (a) Find the fraction of electrons in the two lowered valleys as a function of $\Delta E$, and check it at $\Delta E$ = 0. (b) Find the splitting at which 80% of the electrons sit in the lowered valleys at 300 K. (c) Find the fraction for a splitting of 0.10 eV.

### Problem 09-01.15 [C]

**How much of strain's gain is the mass?** In the strained silicon of Problem 09-01.14, current flows in the plane of the wafer, along $x$. (a) Show that if a fraction $f$ of the electrons occupy the two out-of-plane ($z$) valleys and the rest are shared equally among the four in-plane valleys, the conductivity mass along $x$ is

$$
\frac{1}{m_c(f)} = \frac{f}{m_t} + \frac{1 - f}{2}\left(\frac{1}{m_l} + \frac{1}{m_t}\right),
$$

and that it reduces to the chapter's result at $f = 1/3$. (b) Find $m_c$ at $f$ = 0.8 and $f$ = 1, and the mobility ratio $\mu(f)/\mu(1/3)$ at each if the scattering time is unchanged. (c) The chapter's source reports electron-mobility gains of 1.5–2.0 times for biaxial tensile strain of 0.4–1.0%. Even with every electron in the lowered valleys, what factor must come from a longer scattering time to reach the low and the high end of that range? What physical change supplies it?

---

## Objective coverage

| Learning objective (chapter 09-01) | Problems |
|---|---|
| 1. Crystal structures, atomic and planar densities, bond lengths | 1, 3, 4 |
| 2. Miller indices, spacings, angles; orientation in devices | 2, 3, 5 |
| 3. Kronig–Penney bands, gaps and effective mass | 6, 7, 8 |
| 4. Reading $E$–$k$ diagrams; conductivity and density-of-states masses | 9, 14, 15 |
| 5. Real-space band diagrams, affinity, work function, field | 10 |
| 6. Gap versus temperature and composition; mismatch and strain | 11, 12, 13 |
