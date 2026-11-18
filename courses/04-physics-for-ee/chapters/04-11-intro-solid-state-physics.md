<!-- status: reviewed -->
# 04-11 · Introduction to Solid-State Physics

| | |
|---|---|
| **Course** | [04 · Physics for EE](../README.md) |
| **University equivalent** | Modern physics / introductory solid-state physics: crystals, the free-electron gas and energy bands (Kittel, *Introduction to Solid State Physics*, chs. 1, 6 and 7 at introductory depth; Hu, *Modern Semiconductor Devices for Integrated Circuits*, ch. 1) |
| **Prerequisites** | [04-10](04-10-intro-quantum-mechanics.md) (quantum mechanics), [04-05](04-05-current-resistance-and-conduction.md) (the Drude model), [02-08](../../02-complex-numbers-des-and-linear-algebra/chapters/02-08-eigenvalues-and-eigenvectors.md) (eigenvalues) |
| **Estimated study hours** | 10 |
| **Last verified** | 2026-11-18 |

**Learning objectives.** After this chapter you can:

1. Describe face-centered cubic and diamond crystals, and compute atomic densities and neighbor distances from a lattice constant.
2. Derive the free-electron Fermi energy, Fermi speed and density of states; apply the Fermi–Dirac distribution; and explain how Sommerfeld's quantum picture corrects Drude's classical one.
3. Explain how a periodic potential turns atomic levels into energy bands separated by gaps, in the tight-binding and nearly-free-electron pictures, and compute band widths and gaps in simple models.
4. Define the effective mass from band curvature and holes as missing electrons, and compute both from E–k relations.
5. Classify metals, semiconductors and insulators by band filling, and estimate how the intrinsic carrier concentration depends on band gap and temperature.
6. Relate band gaps to optical absorption (direct and indirect) and to the choice of silicon, GaAs, GaN or SiC for a product.

## 1. Big picture

Why does copper conduct, silicon conduct a little, and silicon dioxide hardly at all? The answer is **energy bands**. When atoms bond into a crystal, each sharp atomic level (04-10) spreads into a band of closely spaced levels, separated from other bands by forbidden ranges called **band gaps**. Whether a material conducts depends on how its electrons fill the bands. This chapter builds the picture from 04-10's quantum mechanics, first for a metal's electron gas (Sommerfeld's correction of 04-05's Drude model), then for electrons in a periodic crystal, and ends with the vocabulary every device chapter assumes: band gap, effective mass, hole, intrinsic carrier concentration, direct and indirect gaps.

- **Transistors** rely on silicon's 1.12 eV gap: wide enough that few electrons cross it at room temperature, narrow enough that doping supplies carriers ([09-01](../../09-semiconductor-devices/chapters/09-01-crystals-and-energy-bands.md)).
- **Leakage** grows exponentially with temperature because carriers are thermally excited across the gap.
- **Optoelectronics:** the gap sets which wavelengths a material detects or emits, and whether it is direct or indirect decides whether it makes an efficient LED or laser.
- **Power electronics:** wide-bandgap SiC and GaN are displacing silicon in electric-vehicle inverters, chargers and data-center power ([09-13](../../09-semiconductor-devices/chapters/09-13-compound-and-wide-bandgap-semiconductors.md)).

## 2. Intuition first

**From one atom to a crystal.** Bring two identical atoms close and each atomic level splits in two: a lower, bonding combination and a higher, antibonding one. Bring $N$ atoms together and each level becomes $N$ levels packed into a **band**. The splitting comes from electrons tunneling (04-10) between neighbors, so closer atoms give wider bands. Between bands grown from different atomic levels lie **band gaps** with no allowed states (Figure 1).

**A circuit analogy, and its limits.** Two identical LC resonators coupled by mutual inductance (04-07) have two normal modes, one above and one below the original frequency; a chain of $N$ coupled resonators has $N$ modes filling a band, and a periodic chain of two kinds of resonator has a stopband, as RF filters exploit. *Where it breaks:* a resonator mode can hold any energy, but each electron state holds at most two electrons (one per spin). How bands *fill* separates metals from insulators, and resonators have no counterpart.

**Filling the levels.** A metal has about $10^{23}$ conduction electrons per cm³, and the Pauli principle lets at most two share a state, so even at absolute zero they fill the levels up to a sharp top, the **Fermi energy**, several electronvolts high, far above $kT$ = 0.026 eV. Like a stadium filled from the front, only people at the back edge can move to an empty seat: only electrons near the Fermi energy can absorb heat or respond to a field. *Where it breaks:* electrons are indistinguishable, and at finite temperature the edge is blurred over a few $kT$.

**Metal, semiconductor, insulator.** A partly filled band has empty states right next to the occupied ones, so a tiny field moves electrons: a **metal**. A completely full band with a gap above it cannot respond, because there is no nearby empty state: an **insulator**. A **semiconductor** is an insulator whose gap is small enough that heat, light or added impurities put a controllable number of electrons into the upper band, leaving empty states, **holes**, in the lower one.

![Left: energy levels of tight-binding chains of 1, 2, 3, 4, 6, 10, 30 and 100 atoms. Each of two atomic levels splits into as many levels as there are atoms, filling a band; a gap remains between the two bands. Right: the band energy E0 minus 2t cos ka against wavenumber, with the allowed points for a 12-atom ring and a dashed parabola matching the bottom of the band.](../../../assets/figures/04-11/bands-from-atoms.svg)

*Figure 1. Left: $N$ coupled atoms give $N$ levels per atomic level, filling a band of width $4t$. Right: the band against wavenumber $k$; near the bottom it is a parabola, which defines the effective mass.*

## 3. Theory

> **Notation for this chapter.** $a$ is a lattice constant, $n$ an electron density, $k$ a wavenumber (m⁻¹), and $k$ in $kT$ Boltzmann's constant. $E_F$ is the Fermi energy, $T_F = E_F/k$ the Fermi temperature, $g(E)$ a density of states, $f(E)$ the Fermi–Dirac occupation, $m_0$ the free-electron mass and $m^*$ an effective mass. Constants are exact SI values and CODATA 2022 ([R-073](../../../reference/research-log.md#r-073--codata-2022-fundamental-constants)); $kT$ = 25.85 meV at 300 K.

### 3.1 Crystals

A **crystal** repeats a group of atoms (the **basis**) at every point of a **lattice**. For cubic crystals we use the **conventional cubic unit cell** of side $a$, the **lattice constant**.

- **Face-centered cubic (FCC):** atoms at the 8 corners (each shared by 8 cells) and the 6 face centers (each shared by 2): $8\times\tfrac18 + 6\times\tfrac12 = 4$ atoms per cell. Copper and aluminum are FCC.
- **Diamond:** FCC with a two-atom basis, the second atom displaced by $(a/4)(1,1,1)$, giving **8 atoms per cubic cell**. Each atom has 4 nearest neighbors at the corners of a tetrahedron, at distance $\sqrt3\,a/4$. Silicon, germanium and diamond take this structure; GaAs takes it with alternating Ga and As (zinc blende).

Silicon's four valence electrons form four covalent bonds, one to each neighbor. With $a$ = 0.543102 nm ([R-086](../../../reference/research-log.md#r-086--crystals-band-gaps-intrinsic-carriers-and-wide-bandgap-markets)), silicon has $8/a^3 = 4.994\times10^{22}$ atoms per cm³ (Example 04-11.1). Doping is measured against this: $10^{16}$ dopants per cm³ is one per five million silicon atoms.

Lattice constants are measured by X-ray diffraction (04-09): atomic planes a distance $d$ apart reflect strongly only where reflections from successive planes add in phase, $2d\sin\theta = m\lambda$ (**Bragg's law**; here θ is measured from the planes, not from their normal as in 04-09's refraction). The same condition applied to electron waves inside the crystal creates band gaps (§3.4).

### 3.2 The free-electron gas: Fermi energy and Sommerfeld's correction

**Counting states.** Treat a metal's valence electrons as free particles in a box of side $L$, the ions only a uniform positive background. Plane waves $e^{i\vec k\cdot\vec r}$ that repeat after a distance $L$ (periodic boundary conditions, which give the same bulk results as hard walls for large $L$) need

$$
\vec k = \frac{2\pi}{L}(n_x, n_y, n_z), \qquad n_x, n_y, n_z = 0, \pm1, \pm2, \dots
$$

Each allowed $\vec k$ claims a volume $(2\pi/L)^3$ of "$k$-space", and states with energy $\hbar^2k^2/2m$ below $E$ lie inside a sphere of radius $\sqrt{2mE}/\hbar$.

> **Math refresher — counting points in a sphere.** When grid cells are tiny compared with a sphere, the number of grid points inside is its volume divided by the volume per point, $\tfrac43\pi k^3/(2\pi/L)^3$, with a relative error of order $1/(kL)$ from cells cut by the surface. The lab counts points directly and watches the error shrink.

At absolute zero the $N$ electrons fill the lowest states, two per $\vec k$ (spin up and down), up to the **Fermi wavenumber** $k_F$:

$$
N = 2\times\frac{\tfrac43\pi k_F^3}{(2\pi/L)^3} = \frac{V k_F^3}{3\pi^2}
\quad\Longrightarrow\quad
k_F = (3\pi^2 n)^{1/3}, \qquad n = N/V .
$$

The top occupied energy is the **Fermi energy**, and electrons there move at the **Fermi speed**:

$$
E_F = \frac{\hbar^2k_F^2}{2m} = \frac{\hbar^2}{2m}(3\pi^2n)^{2/3}, \qquad v_F = \frac{\hbar k_F}{m}, \qquad T_F = \frac{E_F}{k} .
$$

*Units:* (J·s)²·m⁻²/kg = J. For copper, one conduction electron per atom and $n = 8.49\times10^{28}$ m⁻³ (04-05) give $E_F$ = 7.044 eV, $v_F = 1.574\times10^6$ m/s and $T_F = 8.17\times10^4$ K (Example 04-11.2): the Fermi speed 04-05 borrowed from tables, now derived. $E_F$ is about 270 times $kT$ at room temperature, so a metal's electron gas is "cold" in the quantum sense even in a furnace.

**Density of states.** The number of states below $E$ is $N(E) = (V/3\pi^2)(2mE/\hbar^2)^{3/2}$, so the number per unit energy is

$$
g(E) = \frac{dN}{dE} = \frac{V}{2\pi^2}\Big(\frac{2m}{\hbar^2}\Big)^{3/2} E^{1/2} .
$$

Because $N\propto E^{3/2}$, $g(E_F) = \tfrac32N/E_F$. The average energy of the filled sphere is $\int_0^{E_F}E\,g\,dE\big/\int_0^{E_F}g\,dE = \tfrac25E_F^{5/2}\big/\tfrac23E_F^{3/2} = \tfrac35E_F$: 4.226 eV in copper, against the 0.039 eV ($\tfrac32kT$) of a classical gas at 300 K.

**Temperature: the Fermi–Dirac distribution.** At $T > 0$ the probability that a state of energy $E$ is occupied is

$$
f(E) = \frac{1}{1 + e^{(E - E_F)/kT}} .
$$

It is ½ at $E_F$ and falls from 0.9 to 0.1 over $2kT\ln 9 = 4.394\,kT$, about 0.11 eV at 300 K (Figure 2). Many $kT$ above $E_F$, $f \approx e^{-(E-E_F)/kT}$, the classical **Boltzmann factor**. (The energy where $f = \tfrac12$ is strictly the chemical potential, which in metals differs from the 0 K value by a fraction of order $(kT/E_F)^2$; engineers call it the **Fermi level** at any temperature.)

> **Math refresher — where the Boltzmann factor comes from.** In air at temperature $T$, a layer of thickness $dh$ supports the weight above it: $dp = -nmg\,dh$, with $n$ molecules per volume. The ideal-gas law $p = nkT$ gives $kT\,dn = -nmg\,dh$, so $n(h)\propto e^{-mgh/kT}$: the chance of a molecule having potential energy $E = mgh$ falls as $e^{-E/kT}$. This factor, true for any energy in equilibrium, is 03-05's Arrhenius law.

**Deriving Fermi–Dirac.** Electrons trade energy with the vibrating lattice, a classical heat bath that gives up energy $\Delta E$ less often, by a factor $e^{-\Delta E/kT}$, than it absorbs it. For states of energy $E_1 < E_2$ with occupations $f_1$, $f_2$, an electron can jump up only if state 1 is full and state 2 empty, at a rate proportional to $f_1(1-f_2)e^{-(E_2-E_1)/kT}$; the reverse rate is proportional to $f_2(1-f_1)$. Balancing them:

$$
f_1(1-f_2)\,e^{-(E_2-E_1)/kT} = f_2(1-f_1)
\quad\Longrightarrow\quad
\frac{f_1}{1-f_1}e^{E_1/kT} = \frac{f_2}{1-f_2}e^{E_2/kT} .
$$

Each side depends on one state only, so both equal a constant, written $e^{E_F/kT}$. Solving $f/(1-f) = e^{-(E-E_F)/kT}$ gives Fermi–Dirac. The $(1-f)$ factors are the Pauli principle; drop them and the same argument gives the Boltzmann distribution.

![Left: the Fermi–Dirac occupation against energy measured from the Fermi energy, a sharp step at 0 K that softens at 300, 1000 and 3000 K. Right: for copper's free-electron gas, the density of states rising as the square root of energy and the filled states at 0 K up to 7.04 eV, with the occupation at an exaggerated 3000 K rounding only the top edge.](../../../assets/figures/04-11/fermi-dirac.svg)

*Figure 2. Left: the Fermi–Dirac edge blurs over a few $kT$. Right: in copper only a thin slice near $E_F$ feels temperature; deeper electrons have no empty state nearby.*

**What Sommerfeld fixed: heat capacity.** Drude's classical electrons would each absorb $\tfrac32k$ per kelvin, but experiments found metals' heat capacity barely above insulators'. Heating can only promote the roughly $g(E_F)kT$ electrons within $kT$ of $E_F$, each by about $kT$, so the extra energy is of order $g(E_F)(kT)^2$ and the heat capacity of order $3Nk(T/T_F)$. The careful calculation (verified numerically in the lab) gives

$$
C_{\text{el}} = \frac{\pi^2}{3}g(E_F)k^2T = \frac{\pi^2}{2}Nk\frac{T}{T_F} ,
$$

a fraction $(\pi^2/3)(T/T_F)$ of the classical value, 1.2% for copper at 300 K and small beside the lattice's $3R$ (Example 04-11.3).

> **Going deeper — the Sommerfeld expansion.** For smooth $H(E)$, $\int_0^\infty H f\,dE \approx \int_0^\mu H\,dE + \frac{\pi^2}{6}(kT)^2H'(\mu)$, because $-\partial f/\partial E$ is a narrow symmetric peak at $\mu$ whose second moment is $\pi^2(kT)^2/3$. Applying it to the electron number and the energy gives $C_{\text{el}}$ (Ashcroft and Mermin, ch. 2).

**What Sommerfeld fixed: the mean free path.** A field $\mathcal E$ pushes every electron's wavenumber at the rate $\hbar\,dk/dt = -e\mathcal E$ (§3.5), so the filled sphere slides until collisions, every τ on average, stop it at a shift $e\mathcal E\tau/\hbar$. The current comes from the slight excess of electrons on one side of the Fermi surface, all moving at about $v_F$, and works out to exactly Drude's $\sigma = ne^2\tau/m$. What changes is the speed behind τ: the mean free path is $v_F\tau$ = 39 nm in copper, not Drude's 3 nm. A perfect, motionless crystal would not scatter electrons at all (§3.4); they scatter off impurities, surfaces and lattice vibrations, whose quanta are called **phonons**.

### 3.3 From atoms to bands: tight binding

Now restore the ions, starting from bound electrons that can tunnel between neighbors.

**Two atoms.** Each atom has a level $E_0$; tunneling couples them with energy $-t$ ($t > 0$, growing as the atoms approach). In the basis "electron on atom 1", "electron on atom 2" the energy matrix

$$
\mathbf H = \begin{pmatrix} E_0 & -t \\ -t & E_0 \end{pmatrix}
$$

has eigenvalues (02-08) $E_0 - t$, eigenvector $(1, 1)/\sqrt2$ (the **bonding** state), and $E_0 + t$, eigenvector $(1, -1)/\sqrt2$ (**antibonding**). Two electrons of opposite spin in the bonding state lower the energy by $2t$: a covalent bond.

**A chain of N atoms.** With atoms at $x_n = na$, each coupled to two neighbors, the amplitudes $c_n$ satisfy

$$
E\,c_n = E_0\,c_n - t\,(c_{n-1} + c_{n+1}) .
$$

Try $c_n = e^{ikna}$ and divide by $c_n$:

$$
E = E_0 - t\,(e^{-ika} + e^{ika}) = E_0 - 2t\cos ka .
$$

This **tight-binding band** runs from $E_0 - 2t$ ($k = 0$, all atoms in phase) to $E_0 + 2t$ ($k = \pm\pi/a$, neighbors in antiphase): a **band width** of $4t$. Closing the chain into a ring of $N$ atoms requires $e^{ikNa} = 1$, so $k = 2\pi m/(Na)$, $m = 0, 1, \dots, N-1$. Wavenumbers differing by $2\pi/a$ give identical $c_n$, so all distinct states fit in $-\pi/a < k \le \pi/a$, the **first Brillouin zone**, and there are exactly $N$ of them: **one atomic level becomes one band of $N$ states**, $2N$ with spin (Figure 1). Different atomic levels make different bands, with gaps between them if their ranges do not overlap.

Because $t$ comes from tunneling, it falls roughly exponentially with distance (04-10): inner-shell electrons form very narrow bands and valence electrons bands several electronvolts wide. Squeezing a crystal changes its bands, which is why mechanical **strain** is one of the knobs device engineers use to raise carrier mobility.

### 3.4 Bands from Bragg reflection: nearly free electrons

Now start from free electrons, $E = \hbar^2k^2/2m$, and add a weak periodic potential.

**Bragg reflection.** Each row of ions reflects part of a wave $e^{ikx}$. The reflections add in phase when the round trip between neighbors, $2a$, is a whole number of wavelengths, that is, at

$$
k = \pm\frac{m\pi}{a}, \qquad m = 1, 2, \dots
$$

Elsewhere they cancel and the electron passes almost freely. At $k = \pm\pi/a$ forward and reflected waves are equal and form two **standing waves**, $\psi_+ = \sqrt2\cos(\pi x/a)$ and $\psi_- = \sqrt2\sin(\pi x/a)$ (normalized so $|\psi|^2$ averages to 1). $|\psi_+|^2 = 1 + \cos(2\pi x/a)$ piles charge on the ions at $x = 0, a, \dots$; $|\psi_-|^2 = 1 - \cos(2\pi x/a)$ between them. Their kinetic energies are equal ($|k| = \pi/a$); their potential energies are not.

**The gap, derived.** Take $V(x) = 2U\cos(2\pi x/a)$, the simplest potential with the lattice period ($U < 0$ when attractive ions sit at $x = 0, a, \dots$). Averaging over one period, with $\langle\cos\rangle = 0$ and $\langle\cos^2\rangle = \tfrac12$:

$$
\langle V\rangle_\pm = \frac1a\int_0^a \Big(1 \pm \cos\frac{2\pi x}{a}\Big)\,2U\cos\frac{2\pi x}{a}\,dx = \pm U ,
$$

so

$$
E_\pm = \frac{\hbar^2}{2m}\Big(\frac{\pi}{a}\Big)^2 \pm U, \qquad E_g = 2|U| .
$$

No traveling state lies between them: an electron there would be Bragg-reflected completely. This first-order estimate is very accurate for weak potentials; in Example 04-11.5 the exact numerical gap differs from $2|U|$ by 0.03%. A Fourier component $2U_m\cos(2\pi mx/a)$ opens a gap $2|U_m|$ at $k = \pm m\pi/a$ (Figure 3, left).

Tight binding (narrow bands) and nearly free electrons (narrow gaps) are two limits of the same physics. Real semiconductors lie between and are computed numerically, but both pictures predict bands, gaps at the zone boundary and $2N$ states per band.

> **Going deeper — Bloch's theorem.** In any periodic potential the energy eigenstates can be written $\psi_k(x) = e^{ikx}u_k(x)$ with $u_k$ repeating every cell, so $|\psi|^2$ is the same in every cell. Such a Bloch wave travels without scattering: a perfect crystal has no resistance from its ions, and only departures from periodicity (vibrations, impurities, surfaces) scatter electrons. Both the tight-binding wave and the standing waves above are Bloch waves.

![Left: energy against wavenumber for a weak periodic potential, following the free-electron parabola except near k equals plus or minus pi over a and 2 pi over a, where it splits and leaves shaded band gaps. Right: schematic band filling for a metal (copper) with a half-filled band, a semiconductor (silicon, 1.12 eV gap) with a full lower band and a few electrons thermally excited into the upper band leaving holes, and an insulator (diamond 5.5 eV, SiO2 about 9 eV) with a full lower band and a wide gap.](../../../assets/figures/04-11/bands-and-gaps.svg)

*Figure 3. Left: a weak periodic potential opens gaps where Bragg reflection occurs. Right: partly filled bands, or full bands with a small or large gap above, make a metal, semiconductor or insulator.*

### 3.5 Electrons in a band: velocity, crystal momentum, effective mass

**1. Velocity.** An electron is a wavepacket of states near some $k$. In 04-09's beats, two waves with slightly different frequencies and wavenumbers form an envelope moving at $\Delta\omega/\Delta k$; in the limit, the packet moves at the group velocity $d\omega/dk$. With $E = \hbar\omega$,

$$
v = \frac{1}{\hbar}\frac{dE}{dk} .
$$

A free electron gets $\hbar k/m = p/m$. In the tight-binding band $v = (2ta/\hbar)\sin ka$: zero at the bottom, maximal at $k = \pm\pi/2a$, zero again at the zone edge, where the electron is a standing wave.

**2. Crystal momentum.** An external force $F$ (from a field, $F = -e\mathcal E$) does work at the rate $Fv$, so $dE/dt = Fv$. But $dE/dt = (dE/dk)(dk/dt)$. Equating and using step 1:

$$
\frac{dE}{dk}\frac{dk}{dt} = F\,\frac1\hbar\frac{dE}{dk}
\quad\Longrightarrow\quad
\hbar\frac{dk}{dt} = F .
$$

$\hbar k$, the **crystal momentum**, responds to external forces; the ions' forces are already built into $E(k)$.

**3. Effective mass.** Differentiating the velocity,

$$
\frac{dv}{dt} = \frac1\hbar\frac{d^2E}{dk^2}\frac{dk}{dt} = \frac{F}{m^*}, \qquad \frac{1}{m^*} = \frac{1}{\hbar^2}\frac{d^2E}{dk^2} .
$$

A band electron responds to external forces with an **effective mass** set by the band's curvature: strongly curved (wide) bands give light, mobile carriers. Near the tight-binding band's bottom, $\cos ka \approx 1 - (ka)^2/2$ gives

$$
E \approx (E_0 - 2t) + t a^2 k^2 = (E_0 - 2t) + \frac{\hbar^2k^2}{2m^*}, \qquad m^* = \frac{\hbar^2}{2ta^2} .
$$

> **Math refresher — curvature from a Taylor series.** Near a minimum at $k_0$, $E(k) \approx E(k_0) + \tfrac12E''(k_0)(k-k_0)^2$ (01-08). Matching $\hbar^2(k-k_0)^2/2m^*$ gives $m^* = \hbar^2/E''(k_0)$: any smooth band minimum looks like a free-electron parabola with its own mass.

Near the band *top* the curvature, and so $m^*$, is negative: a force toward $+x$ accelerates the electron toward $-x$ as it approaches a Bragg reflection. This leads directly to holes (§3.7). Real semiconductor carriers typically have effective masses that are fractions of $m_0$ (04-10 used 0.067 $m_0$ for GaAs electrons), different along different crystal directions; [09-01](../../09-semiconductor-devices/chapters/09-01-crystals-and-energy-bands.md) tabulates them.

> **Going deeper — Bloch oscillations.** Since $\hbar\,dk/dt = F$, a constant force sweeps $k$ to the zone edge, where the electron Bragg-reflects; in a perfect crystal a DC field would make it oscillate, not conduct. Collisions every 0.01–1 ps reset $k$ long before that (Problem 04-11.7); Bloch oscillations appear only in engineered superlattices with periods of several nanometers.

### 3.6 Metals, semiconductors and insulators

**Capacity.** A band has one $k$ state per primitive cell of the crystal (§3.3 in 3-D) and two spins per $k$: **two electrons per primitive cell**.

**A full band carries no current.** Crystal bands satisfy $E(-k) = E(k)$, so $v(-k) = -v(k)$ and a full band's velocities cancel. A field shifts every $k$ equally, but a full band stays full ($k$ is defined only up to $2\pi/a$, so states pushed past the zone edge reappear at the other side). **Only partly filled bands conduct.** Hence (Figure 3, right):

- **Metals** have a partly filled band. Copper and sodium have one conduction electron per primitive cell, half-filling a band. Calcium, with two per cell, would fill one exactly, but its bands overlap in energy, leaving two partly filled.
- **Insulators** have full bands and a large gap: diamond (5.5 eV) and silicon dioxide (about 9 eV) ([R-086](../../../reference/research-log.md#r-086--crystals-band-gaps-intrinsic-carriers-and-wide-bandgap-markets)).
- **Semiconductors** have a modest gap. Silicon's primitive cell has 2 atoms of 4 valence electrons: 8 electrons, filling exactly 4 **valence bands**. The **conduction band** starts 1.12 eV higher. The valence-band top is $E_v$, the conduction-band bottom $E_c$, and $E_g = E_c - E_v$.

**Thermal excitation across the gap.** In a pure (**intrinsic**) semiconductor each electron excited into the conduction band leaves one empty valence state, and Fermi–Dirac is symmetric about $E_F$, so $E_F$ sits near mid-gap. Conduction states are then about $E_g/2$ above $E_F$, many $kT$, so their occupation is close to the Boltzmann factor. With $N_c$ and $N_v$ the effective numbers of conduction and valence states per volume:

$$
n = N_c\,e^{-(E_c - E_F)/kT}, \qquad p = N_v\,e^{-(E_F - E_v)/kT}
\quad\Longrightarrow\quad
np = N_cN_v\,e^{-E_g/kT} ,
$$

independent of $E_F$. In a pure crystal $n = p = n_i$, the **intrinsic carrier concentration**:

$$
n_i = \sqrt{N_cN_v}\;e^{-E_g/2kT} .
$$

$N_c$ and $N_v$ grow as $T^{3/2}$ ([09-02](../../09-semiconductor-devices/chapters/09-02-carriers-doping-fermi-level.md) derives them). For silicon, rounded values $N_c \approx 3\times10^{19}$ and $N_v \approx 1\times10^{19}$ cm⁻³ give $n_i \approx 6.8\times10^9$ cm⁻³ at 300 K (Example 04-11.6) against the best measured $9.65\times10^9$ cm⁻³ ([R-086](../../../reference/research-log.md#r-086--crystals-band-gaps-intrinsic-carriers-and-wide-bandgap-markets)); the rounded prefactors explain the difference: with $N_c = 3\times10^{19}$, an $N_v$ near $2\times10^{19}$ cm⁻³ would reproduce the measured value, so the one-digit $N_v$ is the main culprit. The exponential is what matters:

- Silicon's ~$10^{10}$ cm⁻³ is one carrier per $5\times10^{12}$ atoms, so pure silicon barely conducts (04-05). That is what makes it useful: $10^{15}$–$10^{20}$ cm⁻³ of donors or acceptors (**doping**, 09-02) set the carrier density by design rather than by temperature.
- From 300 to 400 K silicon's $n_i$ rises several hundredfold, and junction leakage (proportional to $n_i$ or $n_i^2$ by mechanism) with it: the Arrhenius behavior of 03-05, and a main reason chips have maximum junction temperatures.
- 4H-SiC's gap of about 3.26 eV makes its exponential factor ~$10^{-18}$ of silicon's, so its intrinsic carriers stay negligible far above the temperatures silicon devices are rated for.

### 3.7 Holes

Describe a nearly full band by its few empty states. Let a band be full except for state $j$.

**Current.** A full band carries none: $-e\sum_{\text{all}} v_i = 0$. Without electron $j$,

$$
J = -e\sum_{i\ne j} v_i = -e\Big(\sum_{\text{all}} v_i - v_j\Big) = +e\,v_j ,
$$

the current of one **positive** charge moving with the missing electron's velocity: a **hole**.

**Mass.** Empty states collect at the valence-band top, where the missing electron's effective mass is negative, $m^*_j = -|m^*|$. In a field the missing state's velocity changes as $dv_j/dt = (-e\mathcal E)/m^*_j = +e\mathcal E/|m^*|$, exactly like a positive charge with positive mass $m_h = |m^*|$. Holes are real: the Hall effect (04-06) shows a positive carrier sign in p-type semiconductors. Hole energy increases *downward* on an electron band diagram, because moving a hole deeper means lifting an electron to fill it.

CMOS uses both: NMOS conducts with conduction-band electrons, PMOS with valence-band holes. Silicon's holes are heavier and less mobile (µₚ ≈ 470 against µₙ ≈ 1400 cm²/V·s, 04-05), so PMOS transistors are traditionally drawn wider to match NMOS drive.

### 3.8 Band gaps, light and materials

A photon can lift a valence electron into the conduction band only if $hf \ge E_g$ (04-10), so a semiconductor absorbs wavelengths shorter than $\lambda_c = 1239.84\text{ eV·nm}/E_g$; LEDs and lasers emit near $E_g$ when electrons and holes recombine.

**Direct and indirect gaps.** A near-infrared photon's wavenumber is of order $10^{-3}$ of the crystal-momentum scale $\pi/a$ that sets silicon's Brillouin zone (Problem 04-11.10), so optical transitions change an electron's energy but hardly its $k$: they are vertical on an $E$–$k$ diagram.

- In a **direct-gap** material (GaAs, GaN) the conduction-band minimum lies above the valence-band maximum at $k = 0$; electrons and holes recombine by emitting a photon alone, so LEDs and lasers use direct gaps.
- In an **indirect-gap** material (Si, Ge, 4H-SiC, diamond) the conduction minimum sits at another $k$; recombination must also create or absorb a phonon to supply the crystal momentum, a much less likely process. Silicon is a poor emitter but a fine detector (absorption well above the gap is strong), which is why silicon photonics borrows its lasers from III–V materials ([24-07](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-07-photonics-fundamentals.md)).

| Material | $E_g$ at 300 K (eV) | Gap | Cut-off | Typical role |
|---|---|---|---|---|
| Ge | 0.66–0.67 | indirect | ≈ 1.85 µm | Telecom photodetectors, SiGe transistors |
| Si | 1.12 | indirect | ≈ 1.11 µm | CMOS logic, memory, image sensors, power |
| GaAs | 1.42 | direct | ≈ 873 nm | RF amplifiers, lasers and VCSELs (with alloys) |
| 4H-SiC | ≈ 3.2–3.26 | indirect | ≈ 380 nm | High-voltage power (EV inverters) |
| GaN | 3.4 | direct | ≈ 365 nm | Fast power switches, RF, blue and white LEDs (with InGaN) |
| β-Ga₂O₃ | 4.9 | — | ≈ 253 nm | Research-stage ultrawide-bandgap power |
| Diamond | 5.5 | indirect | ≈ 225 nm | Research-stage power, heat spreaders |

Gaps are from [R-086](../../../reference/research-log.md#r-086--crystals-band-gaps-intrinsic-carriers-and-wide-bandgap-markets). The second decimal varies by source: 4H-SiC is quoted as 3.2, 3.23 or 3.26 eV, and one textbook table gives diamond 6.0 eV where a recent review gives 5.5 **[Contested at the second decimal]**. Gaps also shrink slightly as temperature rises.

**Why wide gaps for power.** Breakdown occurs when carriers gain enough energy between collisions to knock electrons across the gap (**impact ionization**, [09-06](../../09-semiconductor-devices/chapters/09-06-pn-junction-iv-and-capacitance.md)). A wider gap demands more energy per event, so the material withstands much stronger fields, and a device can block a given voltage with a thinner, more heavily doped drift region and lower on-resistance. Together with negligible $n_i$ at high temperature, that is the case for SiC and GaN in power electronics.

> **Deeper:** see companion repo *Semiconductor Capital Equipment* for how SiC and GaN wafers are grown and processed.

## 4. Worked examples

### Example 04-11.1 · The silicon crystal

**Setup.** Silicon is diamond-structured with $a$ = 0.543102 nm. Find (a) atoms per cubic cell, (b) the atomic density, (c) the nearest-neighbor distance, (d) the mass density for a molar mass of 28.0855 g/mol, and (e) the valence-electron density.

**Solution.** (a) FCC's 4, doubled by the two-atom basis: **8**. (b) $a^3 = 1.6019\times10^{-22}$ cm³, so $8/a^3$ = **4.994×10²² cm⁻³**. (c) $\sqrt3\,a/4$ = **0.2352 nm**. (d) $nM/N_A = 4.994\times10^{22}\times28.0855/6.02214\times10^{23}$ = **2.329 g/cm³**. (e) 4 per atom: **1.998×10²³ cm⁻³**.

**Units check.** (cm⁻³)(g/mol)/(mol⁻¹) = g/cm³ ✓. **Sanity check.** The result matches silicon's handbook density of 2.33 g/cm³, so the lattice constant and atom count agree.

### Example 04-11.2 · Copper's Fermi sea

**Setup.** Copper has $n = 8.49\times10^{28}$ m⁻³. Find (a) $k_F$, (b) $E_F$, (c) $v_F$, (d) $T_F$, (e) the 0 K average energy, (f) the classical $\tfrac32kT$ at 300 K, and (g) the Fermi wavelength.

**Solution.** (a) $(3\pi^2n)^{1/3} = (2.5138\times10^{30})^{1/3}$ = **1.360×10¹⁰ m⁻¹**. (b) $\hbar^2k_F^2/2m = (1.05457\times10^{-34}\times1.3597\times10^{10})^2/(2\times9.1094\times10^{-31}) = 1.1285\times10^{-18}$ J = **7.044 eV**. (c) $\hbar k_F/m$ = **1.574×10⁶ m/s**. (d) $E_F/k$ = **8.174×10⁴ K**. (e) $\tfrac35E_F$ = **4.226 eV**. (f) $\tfrac32\times25.85$ meV = **38.78 meV**. (g) $2\pi/k_F$ = **0.4621 nm**, comparable to copper's cubic lattice constant, $(4/n)^{1/3}$ ≈ 0.36 nm.

**Units check.** $\hbar k/m$: (kg·m²/s)(m⁻¹)/kg = m/s ✓. **Sanity check.** $v_F$ matches the $1.57\times10^6$ m/s 04-05 took from tables. At 0 K the electrons average 4.2 eV of kinetic energy, over 100 times classical thermal energy: the Pauli principle, not heat, sets their speed.

### Example 04-11.3 · What Sommerfeld fixed

**Setup.** For copper at 300 K ($E_F$ = 7.044 eV, $T_F = 8.174\times10^4$ K, ρ = 1.68 µΩ·cm), find (a) the fraction of electrons within $kT$ of $E_F$, $g(E_F)kT/N$; (b) the electronic heat capacity as a fraction of Drude's; (c) the electronic heat capacity per mole; (d) the lattice's $3R$; (e) τ from $\sigma = ne^2\tau/m$; (f) the mean free path $v_F\tau$.

**Solution.** (a) $\tfrac32kT/E_F = 1.5\times0.025852/7.044$ = **0.005505**, one electron in 180. (b) $(\pi^2/3)(T/T_F) = 3.290\times300/81{,}740$ = **0.01207**. (c) $\tfrac{\pi^2}{2}R\,T/T_F$ = **0.1506 J/(mol·K)**. (d) $3R$ = **24.94 J/(mol·K)**. (e) $m/(ne^2\rho) = 9.1094\times10^{-31}/(8.49\times10^{28}\times(1.6022\times10^{-19})^2\times1.68\times10^{-8})$ = **2.488×10⁻¹⁴ s**. (f) $1.574\times10^6\times2.488\times10^{-14}$ = **39.16 nm**.

**Sanity check.** The electrons add 0.6% to the lattice heat capacity, as experiments found. The mean free path agrees with 04-05's 39.06 nm (from the rounded $1.57\times10^6$ m/s) and with first-principles values of 39–40 nm.

### Example 04-11.4 · A tight-binding band

**Setup.** Atoms spaced $a$ = 0.25 nm have a level with coupling $t$ = 1.0 eV. Find (a) the band width, (b) $m^*$ at the bottom, (c) the maximum group velocity, (d) $m^*$ at the top.

**Solution.** (a) $4t$ = **4.0 eV**. (b) $\hbar^2/(2ta^2) = 1.1121\times10^{-68}/(2\times1.6022\times10^{-19}\times6.25\times10^{-20}) = 5.553\times10^{-31}$ kg = **0.6096 m₀**. (c) $2ta/\hbar = 2\times1.6022\times10^{-19}\times0.25\times10^{-9}/1.0546\times10^{-34}$ = **7.596×10⁵ m/s**. (d) Near $k = \pi/a$, $\cos ka \approx -1 + (ka-\pi)^2/2$, so $E \approx E_0 + 2t - ta^2(k-\pi/a)^2$: **−0.6096 m₀**.

**Units check.** $\hbar^2/(Ea^2)$: J²s²/(J·m²) = kg ✓. **Sanity check.** Doubling $t$ halves $m^*$: wide bands mean light carriers.

### Example 04-11.5 · A band gap from Bragg reflection

**Setup.** A 1-D lattice of period $a$ = 0.5 nm has $V(x) = 2U\cos(2\pi x/a)$ with $U$ = 0.2 eV. Find (a) the zone-edge wavenumber, (b) the free-electron energy there, (c), (d) the two standing-wave energies, and (e) the exact gap.

**Solution.** (a) $\pi/a$ = **6.283×10⁹ m⁻¹**; the wavelength is $2a$ = 1 nm, the Bragg condition. (b) $\hbar^2(\pi/a)^2/2m = 2.410\times10^{-19}$ J = **1.504 eV**. (c) $1.504 - 0.2$ = **1.304 eV**; (d) **1.704 eV**. (e) Diagonalizing the Hamiltonian in 21 plane waves (the lab's method; it uses 31, which changes nothing at this precision) gives edges 1.3009 and 1.7007 eV and a gap of **0.3999 eV**: mixing with other plane waves lowers both edges by about 3 meV but the gap by only 0.1 meV.

**Sanity check.** The gap is twice the potential's Fourier amplitude whatever $a$ and $m$; $a$ only sets where the gap appears.

### Example 04-11.6 · Intrinsic carriers, band gap and temperature

**Setup.** (a) Evaluate $e^{-E_g/2kT}$ for silicon (1.12 eV) at 300 K. (b) Estimate $n_i$ with $N_c = 3\times10^{19}$, $N_v = 1\times10^{19}$ cm⁻³. (c) By what factor does $n_i\propto T^{3/2}e^{-E_g/2kT}$ grow from 300 to 400 K at fixed gap? (d) Compare the fit $n_i = 5.29\times10^{19}(T/300)^{2.54}e^{-6726/T}$ cm⁻³ ([R-086](../../../reference/research-log.md#r-086--crystals-band-gaps-intrinsic-carriers-and-wide-bandgap-markets)). (e) How much smaller is 4H-SiC's factor (3.26 eV) at 300 K? (f) At what temperature does SiC's factor equal silicon's at 300 K?

**Solution.** (a) $1.12/0.051704 = 21.662$; $e^{-21.662}$ = **3.912×10⁻¹⁰**. (b) $\sqrt{3\times10^{38}} = 1.732\times10^{19}$, times (a): **6.776×10⁹ cm⁻³** (measured: 9.65×10⁹). (c) $(4/3)^{3/2} = 1.540$; the exponent changes by $(E_g/2k)(1/300 - 1/400) = 5.416$, a factor 224.9; together **346.2**. (d) $(4/3)^{2.54}e^{6726(1/300-1/400)} = 2.076\times271.8$ = **564.4**, faster because silicon's gap shrinks as it warms. (e) $e^{-2.14/0.051704} = e^{-41.39}$ = **1.059×10⁻¹⁸**. (f) Equal $E_g/T$: $300\times3.26/1.12$ = **873.2 K**.

**Sanity check.** 2.14 eV of extra gap costs a factor of $10^{18}$; differences in $N_c$, $N_v$ between materials change these results by factors of a few, not powers of ten.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 04-11.1a | atoms per diamond cubic cell | 8 | — |
| Ex 04-11.1b | silicon atomic density | 4.994×10^22 | cm⁻³ |
| Ex 04-11.1c | nearest-neighbor distance | 0.2352 | nm |
| Ex 04-11.1d | silicon mass density | 2.329 | g/cm³ |
| Ex 04-11.1e | valence-electron density | 1.998×10^23 | cm⁻³ |
| Ex 04-11.2a | copper Fermi wavenumber | 1.360×10^10 | m⁻¹ |
| Ex 04-11.2b | copper Fermi energy | 7.044 | eV |
| Ex 04-11.2c | copper Fermi speed | 1.574×10^6 | m/s |
| Ex 04-11.2d | Fermi temperature | 8.174×10^4 | K |
| Ex 04-11.2e | average energy at 0 K | 4.226 | eV |
| Ex 04-11.2f | classical 3kT/2 at 300 K | 38.78 | meV |
| Ex 04-11.2g | Fermi wavelength | 0.4621 | nm |
| Ex 04-11.3a | fraction within kT of E_F | 0.005505 | — |
| Ex 04-11.3b | electronic over classical heat capacity | 0.01207 | — |
| Ex 04-11.3c | electronic heat capacity per mole | 0.1506 | J/(mol·K) |
| Ex 04-11.3d | lattice heat capacity 3R | 24.94 | J/(mol·K) |
| Ex 04-11.3e | collision time | 2.488×10^-14 | s |
| Ex 04-11.3f | mean free path | 39.16 | nm |
| Ex 04-11.4a | band width | 4.0 | eV |
| Ex 04-11.4b | effective mass at the bottom | 0.6096 | m₀ |
| Ex 04-11.4c | maximum group velocity | 7.596×10^5 | m/s |
| Ex 04-11.4d | effective mass at the top | −0.6096 | m₀ |
| Ex 04-11.5a | zone-edge wavenumber | 6.283×10^9 | m⁻¹ |
| Ex 04-11.5b | free-electron energy at the zone edge | 1.504 | eV |
| Ex 04-11.5c | lower standing-wave energy | 1.304 | eV |
| Ex 04-11.5d | upper standing-wave energy | 1.704 | eV |
| Ex 04-11.5e | exact numerical gap | 0.3999 | eV |
| Ex 04-11.6a | silicon Boltzmann factor | 3.912×10^-10 | — |
| Ex 04-11.6b | estimated silicon n_i | 6.776×10^9 | cm⁻³ |
| Ex 04-11.6c | n_i ratio 400 K/300 K, fixed gap | 346.2 | — |
| Ex 04-11.6d | n_i ratio 400 K/300 K, fit | 564.4 | — |
| Ex 04-11.6e | SiC over Si exponential factor | 1.059×10^-18 | — |
| Ex 04-11.6f | SiC temperature matching Si at 300 K | 873.2 | K |

Values quoted in the theory sections:

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T 04-11.a | kT at 300 K | 25.85 | meV |
| T 04-11.b | Fermi–Dirac 90%–10% width | 4.394 | kT |

## 5. Simulate it

The lab ([labs/04-11-lab/](../labs/04-11-lab/README.md)) is a notebook in five parts:

1. **Fill the box:** enumerate the allowed $\vec k$ in a periodic box, fill them two electrons at a time, and compare the top level with $E_F$. *Predict first:* how many electrons for 1% agreement?
2. **Sommerfeld numerically:** solve for the chemical potential at fixed electron number, differentiate the energy, and compare with $(\pi^2/2)Nk(T/T_F)$.
3. **Bands from atoms:** diagonalize ever-longer tight-binding chains and extract $m^*$ from the curvature.
4. **Bands from Bragg reflection:** plot $E(k)$ from the plane-wave Hamiltonian and compare the gap with $2|U|$ as $U$ grows.
5. **Intrinsic carriers:** compare $n_i(T)$ across silicon, GaAs, GaN and 4H-SiC.

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Band gap (choice of material) | Wider: higher breakdown field, far fewer intrinsic carriers, hot operation, UV/blue emission | Costlier, more defective substrates; less mature processes | Product and technology leadership |
| Direct versus indirect gap | Direct: efficient LEDs and lasers | III–V materials cost more and integrate poorly with CMOS | Photonics architects |
| Effective mass (material, strain, orientation) | Lighter: higher mobility | Lower density of states; more tunneling through thin barriers | Device and process engineers |
| Junction temperature limit | Higher: more power density, smaller heat sinks | Leakage rises exponentially with temperature | Product and reliability engineers |
| Doping level | Carrier density set by design, far above $n_i$ | Lower mobility; band-gap narrowing at high doping | Device engineers |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Thermal energy at 300 K | $kT$ = 25.85 meV | |
| Silicon lattice | 0.5431 nm; 5.0×10²² atoms/cm³ | [R-086](../../../reference/research-log.md#r-086--crystals-band-gaps-intrinsic-carriers-and-wide-bandgap-markets) |
| Copper free-electron gas | $E_F$ ≈ 7.0 eV, $v_F$ ≈ 1.57×10⁶ m/s, $T_F$ ≈ 82,000 K | |
| Fermi–Dirac edge | 4.4 kT from 90% to 10% (0.11 eV at 300 K) | |
| Band gaps at 300 K | Ge 0.66–0.67, Si 1.12, GaAs 1.42, 4H-SiC ≈ 3.2–3.26, GaN 3.4, diamond 5.5, SiO₂ ≈ 9 eV | [R-086](../../../reference/research-log.md#r-086--crystals-band-gaps-intrinsic-carriers-and-wide-bandgap-markets) |
| Silicon $n_i$ at 300 K | 9.65×10⁹ cm⁻³ (≈10¹⁰; the old 1.45×10¹⁰ is superseded); ≈ 560× higher at 400 K | [R-086](../../../reference/research-log.md#r-086--crystals-band-gaps-intrinsic-carriers-and-wide-bandgap-markets) |

## 8. Common mistakes

1. **Using Drude's thermal speed for metal electrons.** They move at $v_F\sim10^6$ m/s whatever the temperature.
2. **Thinking all electrons conduct.** Only those near $E_F$ change state; full bands carry no current.
3. **Using the Boltzmann factor where Fermi–Dirac is needed.** It holds only many $kT$ from $E_F$: not in metals or heavily doped silicon.
4. **Writing $e^{-E_g/kT}$ for $n_i$.** The Fermi level sits mid-gap, so $n_i\propto e^{-E_g/2kT}$; $e^{-E_g/kT}$ is $n_i^2$.
5. **Using $m_0$ in semiconductors.** Use the band's effective mass.
6. **Treating holes as a mere picture.** They carry real positive current and show a positive Hall coefficient.
7. **Quoting a gap or $n_i$ without source and temperature.** Sources differ in the second decimal, and silicon's long-quoted $n_i$ of 1.45×10¹⁰ cm⁻³ has been replaced by 9.65×10⁹ cm⁻³, a third lower.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Reference values move.** Silicon's 300 K intrinsic carrier concentration, long quoted as 1.45×10¹⁰ cm⁻³, was shown to be inconsistent with the best data: a review proposed 1.08×10¹⁰, and a 1991 measurement gave about 1.0×10¹⁰; a 2003 reassessment accounting for band-gap narrowing gave 9.65×10⁹ cm⁻³ **[Established]**. A 2025 review of simulation parameters traces much of 4H-SiC's 3.2–3.26 eV spread to low-temperature excitonic values **[Contested at the second decimal]** ([R-086](../../../reference/research-log.md#r-086--crystals-band-gaps-intrinsic-carriers-and-wide-bandgap-markets)).
- **Wide-bandgap power.** Yole Group forecasts, as reported in the trade press in June and August 2026 (Yole's own pages were not reachable) **[Industry estimate]**:
  - power SiC devices reach $11 billion by 2031, a 20% compound annual growth rate (CAGR) from 2025, with 800 V platforms about half of battery-EV shipments by 2031;
  - xEV power devices reach $14.5 billion by 2031, with SiC MOSFETs growing at 21.5% a year while silicon IGBT modules remain a market of almost $7 billion; Bosch, Renesas and Rohm were reported to be reassessing SiC manufacturing footprints amid overcapacity;
  - power GaN reaches $3.5 billion by 2031 at a 35% CAGR, consumer and mobile the largest segment ($1.7 billion), Innoscience the 2025 leader; the previous edition forecast $3 billion by 2030 at 42% ([R-086](../../../reference/research-log.md#r-086--crystals-band-gaps-intrinsic-carriers-and-wide-bandgap-markets)).

### Why it matters commercially

Band structure is where materials meet markets. Silicon's 1.12 eV indirect gap explains its dominance (a stable oxide, controllable doping, low room-temperature leakage) and its holes in the portfolio: it cannot emit light efficiently, cannot see telecom wavelengths, and loses to SiC and GaN as voltage, temperature and switching speed climb. Each hole is a market for another material and its substrates, epitaxy tools and packaging. The corporate-development questions are how fast substitution happens, who controls substrate supply and cost, and how cyclical overcapacity resets valuations.

### Marketing vs Reality

- **"Wide-bandgap means better."** *Reality:* better at high voltage, temperature and switching speed; worse on cost, substrate defects and process maturity. At low voltage silicon MOSFETs remain cheaper and very good. Ask for the voltage class and cost per ampere against silicon.
- **"Our market grows 42% a year."** *Reality:* the same analyst's GaN forecast moved from 42% to 35% CAGR in one year. Ask for the forecast's history, not just its latest number.
- **"Our device runs at 200 °C."** *Reality:* the semiconductor may; packages, die attach, gate oxides and passives often fail first. Ask what limits the system and at what temperature lifetime was demonstrated.

### Questions for engineering leaders

1. **"How does leakage scale from 25 °C to maximum junction temperature, and what activation energy do you extract?"** *Strong:* measured Arrhenius slopes compared with $E_g$ or $E_g/2$ to identify the mechanism, and margin to specification. *Evasive:* "it is within the datasheet limit".
2. **"Why SiC (or GaN) rather than silicon here, and where is the crossover?"** *Strong:* quantified conduction and switching losses, system cost including cooling and passives, and the voltage and frequency where the choice flips. *Evasive:* "wide-bandgap is the future".
3. **"Which band-gap, effective-mass and $n_i$ values does your device simulation use, and how were they calibrated?"** *Strong:* named sources and calibration against measured devices. *Evasive:* "the tool defaults".
4. **"What limits your substrate cost and defect density, and how is it trending?"** *Strong:* wafer-diameter roadmap, yield-killing defect types, supply contracts. *Evasive:* headline device specifications only.

## 10. Concept check

1. Why does each atomic level become a band in a crystal of $N$ atoms?

   <details><summary>Answer</summary>

   Tunneling couples the $N$ identical levels; like $N$ coupled resonators, the system has $N$ states spread over a width set by the coupling ($4t$ in a 1-D chain).

   </details>

2. Why can't most electrons in copper absorb thermal energy?

   <details><summary>Answer</summary>

   Every state within a few $kT$ of a deep electron is already occupied (Pauli). Only electrons within about $kT$ of $E_F$ can move, so the electronic heat capacity is about 1% of the classical value.

   </details>

3. Why does a gap open at $k = \pm\pi/a$?

   <details><summary>Answer</summary>

   There the Bragg condition makes reflections from successive ions add in phase, forming two standing waves, one on the ions and one between them, with different potential energies; no traveling state lies between.

   </details>

4. Why does a completely filled band carry no current even in a strong field?

   <details><summary>Answer</summary>

   Every state with velocity $v$ is matched by one with $-v$; a field shifts all states, but the band stays full, so the cancellation persists.

   </details>

5. Why does $n_i$ go as $e^{-E_g/2kT}$ rather than $e^{-E_g/kT}$?

   <details><summary>Answer</summary>

   The Fermi level of a pure semiconductor sits near mid-gap, only $E_g/2$ below the conduction band; $np\propto e^{-E_g/kT}$, and each of $n$, $p$ is its square root.

   </details>

6. Why is silicon a good photodetector but a poor LED?

   <details><summary>Answer</summary>

   Its gap is indirect. Absorption well above the gap is strong, but emitting a photon at the gap needs a phonon to supply crystal momentum, a slow process that loses to non-radiative recombination.

   </details>

Problem set: [04-11 problems](../problems/04-11-problems.md) · [solutions](../solutions/04-11-solutions.md).

## 11. Key terms

[Crystal lattice](../../../reference/glossary.md#crystal-lattice) ·
[Fermi energy](../../../reference/glossary.md#fermi-energy) ·
[Fermi–Dirac distribution](../../../reference/glossary.md#fermi-dirac-distribution) ·
[Density of states](../../../reference/glossary.md#density-of-states) ·
[Phonon](../../../reference/glossary.md#phonon) ·
[Energy band](../../../reference/glossary.md#energy-band) ·
[Band gap](../../../reference/glossary.md#band-gap) ·
[Bloch's theorem](../../../reference/glossary.md#blochs-theorem) ·
[Effective mass](../../../reference/glossary.md#effective-mass) ·
[Hole](../../../reference/glossary.md#hole) ·
[Intrinsic carrier concentration](../../../reference/glossary.md#intrinsic-carrier-concentration) ·
[Direct band gap](../../../reference/glossary.md#direct-band-gap) ·
[Wide-bandgap semiconductor](../../../reference/glossary.md#wide-bandgap-semiconductor)

## 12. Connections

- **Previous:** [04-10](04-10-intro-quantum-mechanics.md) (levels, tunneling), [04-05](04-05-current-resistance-and-conduction.md) (the Drude model corrected here), [04-09](04-09-waves-and-optics.md) (diffraction, beats).
- **Next:** [05-01](../../05-programming-for-engineers/chapters/05-01-python-fundamentals.md) starts Course 05; devices resume in [09-01](../../09-semiconductor-devices/chapters/09-01-crystals-and-energy-bands.md).
- **Used in:** [09-02](../../09-semiconductor-devices/chapters/09-02-carriers-doping-fermi-level.md) (carriers and doping), [09-03](../../09-semiconductor-devices/chapters/09-03-drift-and-diffusion.md) (mobility), [09-14](../../09-semiconductor-devices/chapters/09-14-optoelectronic-devices.md) (direct and indirect gaps), [22](../../22-power-electronics-and-energy-conversion/README.md) (SiC and GaN converters).

## 13. Further study

- Kittel, C., *Introduction to Solid State Physics*, 8th ed., Wiley, 2005, chapters 1, 6 and 7.
- Ashcroft, N. W. and Mermin, N. D., *Solid State Physics*, Saunders, 1976, chapters 2, 8 and 9 (Sommerfeld, Bloch, nearly free electrons).
- Hu, C., *Modern Semiconductor Devices for Integrated Circuits*, Pearson, 2010, chapter 1 (free from the author's site).

## 14. Sources

1. Kittel, C., *Introduction to Solid State Physics*, 8th ed., Wiley, 2005.
2. Ashcroft, N. W. and Mermin, N. D., *Solid State Physics*, Saunders, 1976.
3. NIST, 2022 CODATA recommended values (constants; silicon lattice parameter). [R-073], [R-086]
4. Hu, C., *Modern Semiconductor Devices for Integrated Circuits*, Pearson, 2010, Table 1–1. [R-086]
5. Tsao, J. Y. et al., "Ultrawide-bandgap semiconductors: research opportunities and challenges", *Advanced Electronic Materials* 4, 1600501, 2018. [R-086]
6. Burin, J. et al., "TCAD parameters for 4H-SiC: a review", arXiv:2410.06798, v8, 2025. [R-086]
7. Honsberg, C. and Bowden, S., *PVEducation*, "General Properties of Silicon" and "Intrinsic Carrier Concentration". [R-086]
8. Sproul, A. B. and Green, M. A., *J. Appl. Phys.* 70, 846, 1991; Altermatt, P. P. et al., *J. Appl. Phys.* 93, 1598, 2003. [R-086]
9. Yole Group forecasts as reported by *Compound Semiconductor* (16 June 2026) and *Semiconductor Today* (17 and 20 August 2026). [R-086]
