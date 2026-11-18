<!-- status: verified -->
# 04-05 · Current, Resistance and Conduction

| | |
|---|---|
| **Course** | [04 · Physics for EE](../README.md) |
| **University equivalent** | Current and resistance in University Physics II (Halliday, Resnick & Walker, the chapter on current and resistance; Purcell & Morin, chapter 4; MIT 8.02, weeks 5–6), with the Drude model from an introductory solid-state course |
| **Prerequisites** | [04-04 Electric Potential, Capacitance and Dielectrics](04-04-potential-capacitance-and-dielectrics.md), [04-01](04-01-mechanics-essentials.md) (Newton's law, momentum), [01-10](../../01-calculus-for-engineers/chapters/01-10-multivariable-calculus-2.md) (flux, divergence), [02-02](../../02-complex-numbers-des-and-linear-algebra/chapters/02-02-first-order-linear-odes.md) (first-order ODEs) |
| **Estimated study hours** | 8 |
| **Last verified** | 2026-11-18 |

**Learning objectives.** After this chapter you can:

1. Define current and current density, relate them to carrier density and drift velocity, and apply charge conservation (the continuity equation and KCL).
2. Derive Ohm's law from the Drude model, and compute conductivity, mobility, mean free time and mean free path for metals and semiconductors.
3. Compute resistance from resistivity and geometry, including sheet resistance, temperature dependence and the size effect in narrow wires.
4. Compute Joule heating and power density, and explain the current-density limits set by electromigration.
5. Estimate the RC delay of on-chip wires and explain the tradeoffs among metals, barriers, dielectrics and wire geometry.

## 1. Big picture

Charges at rest gave us fields, potentials and capacitance. This chapter lets them move. **Current** is charge flowing; **resistance** is how hard a material makes that flow, and it turns electrical energy into heat. Ohm's law, $V = IR$, looks like a definition, but it is a statement about how electrons collide inside a material, and it fails in instructive ways: at high fields, in tiny wires and at high frequencies. On a modern chip, resistance has become a first-order problem: the wires connecting billions of transistors are now so narrow that their resistance, not the transistors, often limits speed and power.

- **Every circuit:** Ohm's law and Joule heating are the starting point of [06](../../06-circuit-analysis-1-dc/README.md), and charge conservation becomes KCL.
- **Semiconductors:** the conductivity of silicon is set by its carrier density and mobility, the quantities a transistor modulates ([09-03](../../09-semiconductor-devices/chapters/09-03-drift-and-diffusion.md)).
- **Interconnect:** wire resistance times wire capacitance sets delay; metal choice, barrier layers and low-k dielectrics are major process decisions ([19-05](../../19-digital-vlsi-design/chapters/19-05-interconnect.md)).
- **Reliability and power delivery:** current density limits (electromigration) and resistive voltage drop shape power grids, including the move to backside power delivery ([25-09](../../25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md)).

## 2. Intuition first

**A crowd in a hallway.** Picture electrons in a metal as a dense crowd of people moving very fast in random directions, bouncing off pillars (vibrating atoms and defects). With no field, the random motion averages to zero: no current. Apply a field and every person feels a gentle push in one direction between bounces. Each collision scrambles the direction again, so the push never accumulates into high speed; the crowd acquires only a slow average **drift**. Current is that slow drift multiplied by an enormous number of carriers.

**Fast signals, slow electrons.** In a copper wire carrying an ampere, electrons drift at well under a millimeter per second, yet a light switch works instantly. The wire is already full of electrons; pushing at one end moves the whole column, as water flows from a full hose the instant you open the tap. The *signal* travels at a large fraction of the speed of light, carried by the electromagnetic field around the wire ([04-08](04-08-maxwell-preview.md)).

**Resistance is friction.** Collisions transfer the energy the field gives the electrons to the lattice, which heats up. More collisions per second (higher temperature, more impurities, narrower wires whose surfaces scatter electrons) mean more resistance.

**A finance analogy, and its limits.** Current is like cash flow: a rate, not a stock. Resistance is like transaction friction that converts some value into waste (heat) at every transfer. *Where it breaks:* electrical "friction" is linear over an enormous range (double the voltage, double the current), whereas transaction costs rarely scale so neatly; and charge, unlike money, can never be created or destroyed, so every node's inflows and outflows balance exactly (KCL).

![Left: two simulated electron paths, one wandering randomly with no field and one with the same random flights plus a steady drift opposite the field. Right: a log-scale bar chart comparing the drift speed of electrons carrying 1 A in a 1 mm² wire, the classical thermal speed, copper's Fermi speed and the speed of light.](../../../assets/figures/04-05/drude-drift.svg)

*Figure 1. Random motion is fast; drift is slow. The drift speed of a working current is about ten orders of magnitude below the electrons' actual speed.*

## 3. Theory

> **Notation for this chapter.** $I$ is current (A), $\vec J$ current density (A/m²), $n$ carrier density (m⁻³), $v_d$ drift velocity, $\sigma$ conductivity (S/m) and $\rho$ resistivity (Ω·m), which here is *not* charge density. µ is mobility (m²/V·s, usually quoted in cm²/V·s), τ the mean free time and λ the mean free path. $e$ is the elementary charge; device chapters write it $q$.

### 3.1 Current and current density

**Current** is the rate at which charge crosses a surface: $I = dQ/dt$, measured in amperes (1 A = 1 C/s). By convention its direction is that in which positive charge would move; in a metal, electrons actually move the opposite way.

The **current density** $\vec J$ describes flow point by point: its direction is the flow direction and its magnitude is current per unit area perpendicular to the flow. The current through a surface is its flux ([01-10](../../01-calculus-for-engineers/chapters/01-10-multivariable-calculus-2.md)):

$$
I = \iint_S\vec J\cdot\hat n\,dA .
$$

**Microscopic picture.** Suppose carriers of charge $q$, density $n$, all drift at velocity $\vec v_d$. In time $dt$, those within a distance $v_d\,dt$ of a surface of area $A$ cross it: $nAv_d\,dt$ carriers carrying charge $qnAv_d\,dt$. So

$$
\vec J = nq\vec v_d .
$$

For electrons ($q = -e$), $\vec J$ points opposite to their velocity. Copper has one conduction electron per atom; from its density (8.96 g/cm³) and molar mass (63.55 g/mol), $n = 8.49\times10^{28}$ m⁻³. A current of 1 A through 1 mm² ($J = 10^6$ A/m²) then drifts at $J/(ne) = 74$ µm/s (Example 04-05.1).

**Charge conservation.** Charge cannot appear or vanish. If more current flows out of a closed surface than in, the charge inside must fall:

$$
\oint_S\vec J\cdot\hat n\,dA = -\frac{dQ_{\text{enc}}}{dt}, \qquad \nabla\cdot\vec J = -\frac{\partial\rho_q}{\partial t} ,
$$

the second form (the **continuity equation**) following from the divergence theorem, with $\rho_q$ the charge density. At a circuit node that stores negligible charge, the outflows sum to zero: **Kirchhoff's current law**. When a node does store charge (it always has some capacitance), the imbalance charges it: $C\,dV/dt = \sum I_{\text{in}}$ (Problem 04-05.9).

### 3.2 Ohm's law from the Drude model

In 1900 Paul Drude modeled a metal's electrons as a gas of particles that accelerate freely in a field and collide at random, each collision erasing their memory of the field. It is classical and partly wrong, but it gives the right *form* of Ohm's law and good estimates.

**The model.** An electron of mass $m$ in a field $\vec E$ feels a force $-e\vec E$. Collisions occur at random, on average once per **mean free time** τ, and each resets the electron's velocity to a random direction (zero on average). Averaged over many electrons, the collisions act like a drag that removes momentum at rate $m\vec v_d/\tau$, so the average (drift) velocity obeys

$$
m\frac{d\vec v_d}{dt} = -e\vec E - \frac{m\vec v_d}{\tau} .
$$

This first-order ODE ([02-02](../../02-complex-numbers-des-and-linear-algebra/chapters/02-02-first-order-linear-odes.md)) settles within a few τ, femtoseconds in a metal, to the steady state

$$
\vec v_d = -\frac{e\tau}{m}\vec E = -\mu\vec E, \qquad \mu = \frac{e\tau}{m} .
$$

The **mobility** µ is drift speed per unit field. Then $\vec J = -ne\vec v_d$ gives

$$
\vec J = \sigma\vec E, \qquad \sigma = \frac{ne^2\tau}{m} = ne\mu, \qquad \rho = \frac{1}{\sigma} .
$$

This is **Ohm's law** in its local form: current density proportional to field, with a **conductivity** σ that depends on the material, not on the field. Its ingredients are physical: more carriers (larger $n$) or rarer collisions (larger τ) mean better conduction.

**Copper by the numbers.** With $\rho = 1.68$ µΩ·cm ([R-080](../../../reference/research-log.md#r-080--conduction-interconnect-metals-electromigration-and-backside-power)), $\sigma = 5.95\times10^7$ S/m and $\tau = \sigma m/(ne^2) = 24.9$ fs, so electrons collide about $4\times10^{13}$ times per second. Copper's mobility, 44 cm²/V·s, is *lower* than silicon's: metals conduct well because they have vast numbers of carriers, not because each is especially mobile.

**The mean free path, and Drude's mistake.** How far does an electron fly between collisions? Drude multiplied τ by the classical thermal speed, $\sqrt{3kT/m} \approx 1.2\times10^5$ m/s at 300 K, and got about 3 nm, comparable to a few atomic spacings, which made collisions with atoms look plausible. Quantum mechanics ([04-11](04-11-intro-solid-state-physics.md)) shows the conducting electrons move at the much higher **Fermi speed**, about $1.57\times10^6$ m/s in copper in the free-electron model, giving $\lambda = v_F\tau \approx 39$ nm (Example 04-05.2). That matches modern first-principles values for copper of 39–40 nm ([R-080](../../../reference/research-log.md#r-080--conduction-interconnect-metals-electromigration-and-backside-power)). Electrons in a perfect crystal do not hit atoms at all; they scatter off lattice vibrations, impurities, grain boundaries and surfaces. That 39 nm figure is why copper wires narrower than about 40 nm get worse (§3.4).

> **Going deeper — what Drude got right and wrong.** The relaxation-time picture survives into modern transport theory (the Boltzmann equation), and $\sigma = ne^2\tau/m$ remains correct with $m$ replaced by an effective mass and τ evaluated for electrons near the Fermi energy. Drude's predictions of heat capacity and the speed of electrons were badly wrong, because electrons obey Fermi–Dirac statistics: only those near the Fermi energy can change state. That correction (Sommerfeld, 1928) is the start of 04-11.

**Semiconductors.** In silicon both electrons (density $n$, mobility µₙ) and holes (density $p$, mobility µₚ) carry current, so

$$
\sigma = e(n\mu_n + p\mu_p) .
$$

For lightly doped silicon at room temperature, µₙ ≈ 1400 cm²/V·s and µₚ ≈ 470 cm²/V·s ([R-080](../../../reference/research-log.md#r-080--conduction-interconnect-metals-electromigration-and-backside-power)). Pure silicon has only about $10^{10}$ carriers of each type per cm³ (against copper's $8.5\times10^{22}$), so its resistivity is about $3\times10^5$ Ω·cm. Doping with $10^{15}$ donors per cm³ (one atom in $5\times10^7$) cuts it to about 4.5 Ω·cm (Example 04-05.3). That controllability, across many orders of magnitude, is why semiconductors make switches and metals do not ([09-02](../../09-semiconductor-devices/chapters/09-02-carriers-doping-fermi-level.md)).

**Where Ohm's law fails.** Drift velocity cannot grow without limit: in silicon above roughly $10^4$ V/cm it saturates as electrons shed energy to the lattice faster than they gain it (velocity saturation, [09-03](../../09-semiconductor-devices/chapters/09-03-drift-and-diffusion.md)). At frequencies approaching $1/(2\pi\tau)$, terahertz in metals, electrons cannot follow the field (Problem 04-05.15). And in wires shorter than λ, electrons cross without scattering at all (ballistic transport). Diodes and transistors are non-ohmic by design.

### 3.3 Resistance

For a uniform conductor of length $L$, cross-section $A$ and resistivity ρ, a voltage $V$ makes a uniform field $E = V/L$, so $I = JA = \sigma EA = \sigma AV/L$:

$$
R = \frac VI = \frac{\rho L}{A} .
$$

Resistance grows with length and falls with area, like a pipe's resistance to flow. For non-uniform shapes, add the resistances of thin slices in series: $R = \int\rho\,dx/A(x)$ (Problem 04-05.11).

**Sheet resistance.** Films and traces have a fixed thickness $t$ set by the process. Writing $R = (\rho/t)(L/W)$ separates the process from the layout:

$$
R_s = \frac{\rho}{t}\quad(\Omega/\square), \qquad R = R_s\cdot\frac LW .
$$

$R_s$ is quoted "per square", because any square of the film, of whatever size, has resistance $R_s$ from edge to edge; a trace's resistance is $R_s$ times its number of squares. Standard "1 oz" circuit-board copper (one ounce per square foot) is 34 µm thick, so $R_s \approx 0.49$ mΩ/□ (Example 04-05.4).

**Temperature.** In a metal, raising the temperature makes the lattice vibrate harder, shortening τ, so resistivity rises roughly linearly near room temperature:

$$
\rho(T) \approx \rho_0[1 + \alpha(T - T_0)] .
$$

For annealed copper, α = 0.00393 per °C at 20 °C ([R-080](../../../reference/research-log.md#r-080--conduction-interconnect-metals-electromigration-and-backside-power)): a copper winding gains 31% resistance between 20 and 100 °C. Engineers turn this around to measure winding temperatures from resistance (Example 04-05.5). Semiconductors and thermistors go the other way: more heat frees more carriers, so resistance falls.

**The size effect.** When a wire's width approaches the mean free path, electrons scatter off its surfaces (the Fuchs–Sondheimer mechanism) and off the boundaries between its crystal grains, which shrink with the wire (the Mayadas–Shatzkes mechanism). Below about 40 nm, copper's resistivity therefore rises above its bulk value ([R-080](../../../reference/research-log.md#r-080--conduction-interconnect-metals-electromigration-and-backside-power)). Worse, copper atoms diffuse into silicon dioxide and degrade it, so every copper line needs a **barrier and liner** (such as TaN plus Co) that conducts poorly and, according to imec, cannot be made thinner than about 2–3 nm in total. In a 20 nm line that thin shell takes 30% of the cross-section (Example 04-05.6). Both effects favor metals with shorter mean free paths that need no barrier, even if their bulk resistivity is higher: the figure of merit for narrow wires is roughly $\rho_0\lambda$, not $\rho_0$ alone (§9).

### 3.4 Joule heating and current-density limits

**Power.** Moving charge $dQ$ through a potential drop $V$ releases energy $V\,dQ$, so the power delivered to a resistor is

$$
P = IV = I^2R = \frac{V^2}{R} .
$$

Locally, the power per unit volume is $p = \vec J\cdot\vec E = \sigma E^2 = \rho J^2$: heating is concentrated where current is crowded, at narrow necks and corners. This **Joule heating** is the useful product of toasters and fuses and a waste and a limit everywhere else.

**Electromigration.** At high current density the "electron wind" transfers enough momentum to the metal ions to move them, slowly, in the direction of electron flow. Atoms pile up at one end of a wire (hillocks that can short to neighbors) and leave voids at the other (opens). The time to failure falls steeply with current density and rises exponentially with decreasing temperature (Black's equation, [25-09](../../25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md)). Design rules therefore cap the DC current density in each wire. For minimum-width copper lines, the 2015 International Technology Roadmap for Semiconductors projected that limit falling from 1.8 MA/cm² in 2018 to 0.3 MA/cm² in 2026, while the current density needed to drive even four logic gates was rising above 2 MA/cm² (Figure 2, [R-080](../../../reference/research-log.md#r-080--conduction-interconnect-metals-electromigration-and-backside-power)). Bidirectional signal currents do less damage than one-way supply currents, which is why the problem concentrates in power grids.

![Bar chart of the ITRS 2015 projection of the maximum tolerable DC current density in minimum-width copper lines at 105 degrees Celsius, falling from 1.8 MA/cm² in 2018 to 0.2 MA/cm² in 2028, with markers showing the current density needed to drive four inverters rising from 2.29 to 5.35 MA/cm².](../../../assets/figures/04-05/em-limit.svg)

*Figure 2. A projection made in 2015, not measured data: it shows why electromigration became a design-limiting constraint. Source: Lienig and Thiele (2018), reproducing ITRS 2015 [R-080].*

**IR drop.** A chip drawing 100 A from a 0.7 V supply through a few tenths of a milliohm loses tens of millivolts, several percent of its supply, to resistance alone (Problem 04-05.10). Power-delivery networks are designed around this, and it is the motivation for **backside power delivery**, which moves the power wires to the back of the wafer where they can be thick and short (§9).

### 3.5 RC delay of wires

A wire on a chip has resistance per unit length $r = \rho/A$ and capacitance per unit length $c$ to its neighbors and to the layers above and below (04-04). Neither is concentrated at one point: each piece of the wire charges the capacitance beyond it through the resistance before it. For a long wire of length $L$ driven by a step at one end and open at the other, the voltage obeys a diffusion equation, and the far end reaches 50% at

$$
t_{50} \approx 0.38\,RC, \qquad R = rL,\quad C = cL ,
$$

a result that the lab and the netlist confirm by simulation (Figure 3). Two scalings follow:

- **Delay grows as $L^2$**, because both $R$ and $C$ grow with $L$. Doubling a wire's length quadruples its delay. Long wires are therefore broken by **repeaters** (buffers) so delay grows only linearly (Problem 04-05.16), or routed on thick upper metal layers.
- **Shrinking the cross-section hurts.** If a wire's width, thickness and spacing all shrink by a factor $s$, its resistance per length rises by $1/s^2$ while its capacitance per length, set by ratios of dimensions, stays about the same. Local wires that shrink in length with the transistors roughly keep their delay; wires that must cross a whole chip get slower with every node.

That is why interconnect engineering has three levers: lower the resistivity of narrow wires (metal choice, thinner barriers), lower the dielectric constant between them (low-k, air gaps; [04-04](04-04-potential-capacitance-and-dielectrics.md)), and change the architecture (repeaters, more metal layers, backside power).

![Left: cross-section of two adjacent copper lines 20 nm wide and 40 nm tall, each wrapped in a 2.5 nm barrier and liner, separated by low-k dielectric. Right: the wire's 50% delay against length on log axes, a straight line of slope two passing 14 ps at 100 µm and 1.4 ns at 1 mm.](../../../assets/figures/04-05/wire-rc.svg)

*Figure 3. Narrow wires pay a barrier tax and an RC delay that grows with the square of their length.*

## 4. Worked examples

### Example 04-05.1 — How slowly do electrons drift? (tier A)

**Setup.** (a) How many electrons per second make 1 A? (b) A copper wire of 1 mm² cross-section carries 1 A. Find the current density in A/m² and A/cm². (c) Find the drift speed. (d) How long would an electron take to drift 1 m?

**Solution.** (a) $1/e = $ **6.242×10¹⁸** electrons per second.

(b) $J = 1/10^{-6} = $ **10⁶ A/m²**, which is **100 A/cm²**.

(c) $v_d = J/(ne) = 10^6/(8.49\times10^{28}\times1.602\times10^{-19}) = $ **73.51 µm/s**.

(d) $1/(73.51\times10^{-6})$ s = **3.779 hours**.

**Sanity check.** The signal still travels at a large fraction of the speed of light: it is carried by the field, not by any one electron's journey.

### Example 04-05.2 — Copper in the Drude model (tier B)

**Setup.** Copper has $\rho = 1.68$ µΩ·cm and $n = 8.49\times10^{28}$ m⁻³. Find (a) σ, (b) τ, (c) the mobility in cm²/V·s, (d) the mean free path using the Fermi speed $1.57\times10^6$ m/s, and (e) the classical thermal speed $\sqrt{3kT/m}$ at 300 K and the mean free path it would imply.

**Solution.** (a) $\sigma = 1/\rho = 1/(1.68\times10^{-8}) = $ **5.952×10⁷ S/m**.

(b) $\tau = \sigma m/(ne^2) = 5.952\times10^7\times9.109\times10^{-31}/(8.49\times10^{28}\times(1.602\times10^{-19})^2) = $ **24.88 fs**.

(c) $\mu = e\tau/m = $ 4.375×10⁻³ m²/V·s = **43.75 cm²/V·s**.

(d) $\lambda = v_F\tau = 1.57\times10^6\times24.88\times10^{-15} = $ **39.06 nm**.

(e) $\sqrt{3\times1.381\times10^{-23}\times300/9.109\times10^{-31}} = $ **1.168×10⁵ m/s**, giving $\lambda = $ **2.905 nm**, a factor of 13 too short.

**Interpretation.** Only the quantum (Fermi) speed gives the measured 39–40 nm. The free-electron Fermi speed is itself an approximation for copper, so the agreement is partly fortunate; the first-principles value agrees.

### Example 04-05.3 — Silicon's controllable resistivity (tier B)

**Setup.** Using µₙ = 1400 and µₚ = 470 cm²/V·s, find (a) the resistivity of pure silicon with $n = p = 10^{10}$ cm⁻³, (b) the resistivity of n-type silicon with $10^{15}$ donors per cm³ (take $n = 10^{15}$ cm⁻³ and neglect holes), and (c) how many times more resistive pure silicon is than copper.

**Solution.** Work in cm: $e = 1.602\times10^{-19}$ C.

(a) $\rho = 1/[e\,n_i(\mu_n + \mu_p)] = 1/(1.602\times10^{-19}\times10^{10}\times1870) = $ **3.338×10⁵ Ω·cm**.

(b) $\rho = 1/(e\,n\,\mu_n) = 1/(1.602\times10^{-19}\times10^{15}\times1400) = $ **4.458 Ω·cm**.

(c) $3.338\times10^5/1.68\times10^{-6} = $ **1.987×10¹¹**.

**Interpretation.** One donor per $5\times10^7$ atoms lowers resistivity 75,000-fold. At higher doping, impurity scattering lowers the mobility, so this simple scaling overestimates the effect ([09-03](../../09-semiconductor-devices/chapters/09-03-drift-and-diffusion.md)).

### Example 04-05.4 — A circuit-board trace (tier B)

**Setup.** "1 oz" copper means one avoirdupois ounce (28.3495 g) per square foot (929.03 cm²). (a) Find its thickness. (b) Find its sheet resistance at $\rho = 1.68$ µΩ·cm. (c) A trace 0.25 mm wide and 50 mm long carries 2 A. Find its number of squares, resistance, voltage drop and power dissipated.

**Solution.** (a) $t = 28.3495/(929.03\times8.96) = 3.406\times10^{-3}$ cm = **34.06 µm**.

(b) $R_s = \rho/t = 1.68\times10^{-8}/34.06\times10^{-6} = $ **0.4933 mΩ/□**.

(c) $L/W = 50/0.25 = $ **200 squares**, so $R = $ **98.66 mΩ**. The drop is $IR$ = **0.1973 V** and the power $I^2R$ = **0.3946 W**.

**Sanity check.** Almost 0.2 V lost on a 1 V rail would be unacceptable, which is why power is carried on wide planes, not traces; and 0.4 W in a thin trace heats it noticeably, which is what board current-capacity tables guard against.

### Example 04-05.5 — Resistance as a thermometer (tier B)

**Setup.** A copper coil measures 10.0 Ω at 20 °C. (a) By what factor does its resistance rise at 100 °C? (b) After running, it measures 12.5 Ω. What is its average temperature?

**Solution.** (a) $1 + 0.00393\times80 = $ **1.314**.

(b) $T = 20 + (12.5/10 - 1)/0.00393 = $ **83.61 °C**.

**Interpretation.** This "resistance method" is how motor and transformer winding temperatures are routinely checked: the copper is its own thermometer, averaged over the whole winding.

### Example 04-05.6 — An on-chip wire: barrier tax and RC delay (tier C)

**Setup.** A copper line is 20 nm wide and 40 nm tall, lined on its sides and bottom with a 2.5 nm barrier that carries negligible current. Neighbors at 20 nm spacing on each side, and layers 40 nm above and below, are separated by low-k dielectric ($\varepsilon_r$ = 2.8). Use bulk copper resistivity (an optimistic lower bound) and parallel-plate capacitance (ignoring fringing). Find (a) the copper area and its fraction of the line, (b) the resistance per µm with and without the barrier, (c) the capacitance per µm, (d) $R$, $C$ and $RC$ for 100 µm and 1 mm of wire, and (e) the 50% delays, taking $t_{50} = 0.3787RC$. (f) Confirm the 1 mm delay in ngspice.

**Solution.** (a) The copper core is $(20 - 5)\times(40 - 2.5) = $ **562.5 nm²**, a fraction **0.7031** of the 800 nm² line.

(b) $r = \rho/A_{\text{Cu}} = 1.68\times10^{-8}/562.5\times10^{-18}$ = 2.987×10⁷ Ω/m = **29.87 Ω/µm**; without the barrier it would be **21 Ω/µm**.

(c) Two sidewalls, each a parallel plate of height 40 nm across a 20 nm gap, plus a top and a bottom of width 20 nm across 40 nm: $c = 2\varepsilon(40/20) + 2\varepsilon(20/40) = 5\varepsilon$ per unit length, with $\varepsilon = 2.8\times8.854\times10^{-12}$ F/m, which is **0.1240 fF/µm**.

(d) For 100 µm: $R$ = **2987 Ω**, $C$ = **12.40 fF**, $RC$ = **37.02 ps**. For 1 mm: $R$ = **29.87 kΩ**, $C$ = **124.0 fF**, $RC$ = **3.702 ns**, 100 times more.

(e) $t_{50}$ = **14.02 ps** for 100 µm and **1.402 ns** for 1 mm.

(f) The netlist [labs/04-05-lab/wire_rc.cir](../labs/04-05-lab/wire_rc.cir) models the 1 mm wire as 20 π-sections and measures 1.402 ns.

**Interpretation.** Real narrow-line resistivity is higher than bulk (the size effect), so real delays are longer. A millimeter is a short distance on a large chip, and 1.4 ns is several clock cycles at multi-gigahertz rates: long wires need repeaters or thick upper-level metal.

### Example 04-05.7 — Electromigration and the narrow wire (tier C)

**Setup.** The wire of Example 04-05.6 carries 50 µA DC. (a) Find the current density in its copper core in MA/cm². (b) Using the ITRS 2015 projected limit for 2026 of 0.3 MA/cm², find the largest DC current the wire may carry. (c) By what factor does 50 µA exceed it? (d) Find the Joule power density at the limit.

**Solution.** The core area is 562.5 nm² = 5.625×10⁻¹² cm².

(a) $J = 50\times10^{-6}/5.625\times10^{-12} = 8.889\times10^6$ A/cm² = **8.889 MA/cm²**.

(b) $I_{\max} = 0.3\times10^6\times5.625\times10^{-12} = $ **1.688 µA**.

(c) **29.63** times.

(d) $p = \rho J^2 = 1.68\times10^{-8}\times(3\times10^9)^2 = $ **1.512×10¹¹ W/m³**: large per volume, tiny per wire (about 0.1 nW per µm), and readily conducted away. Electromigration, not heating, sets this limit.

**Interpretation.** A minimum-width wire can carry only microamperes of DC. Supply currents must be spread over many wide wires, which is why power grids consume so much of the upper metal stack, and why moving them to the back of the wafer is attractive.

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 04-05.1a | electrons per second in 1 A | 6.242×10^18 | s⁻¹ |
| Ex 04-05.1b | current density | 1×10^6 | A/m² |
| Ex 04-05.1c | current density | 100 | A/cm² |
| Ex 04-05.1d | drift speed | 73.51 | µm/s |
| Ex 04-05.1e | time to drift 1 m | 3.779 | h |
| Ex 04-05.2a | copper conductivity | 5.952×10^7 | S/m |
| Ex 04-05.2b | mean free time | 24.88 | fs |
| Ex 04-05.2c | copper mobility | 43.75 | cm²/V·s |
| Ex 04-05.2d | mean free path (Fermi speed) | 39.06 | nm |
| Ex 04-05.2e | classical thermal speed | 1.168×10^5 | m/s |
| Ex 04-05.2f | mean free path (thermal speed) | 2.905 | nm |
| Ex 04-05.3a | intrinsic silicon resistivity | 3.338×10^5 | Ω·cm |
| Ex 04-05.3b | n-type silicon resistivity | 4.458 | Ω·cm |
| Ex 04-05.3c | intrinsic silicon over copper | 1.987×10^11 | — |
| Ex 04-05.4a | 1 oz copper thickness | 34.06 | µm |
| Ex 04-05.4b | sheet resistance | 0.4933 | mΩ/□ |
| Ex 04-05.4c | number of squares | 200 | — |
| Ex 04-05.4d | trace resistance | 98.66 | mΩ |
| Ex 04-05.4e | voltage drop at 2 A | 0.1973 | V |
| Ex 04-05.4f | power at 2 A | 0.3946 | W |
| Ex 04-05.5a | resistance ratio, 100 °C over 20 °C | 1.314 | — |
| Ex 04-05.5b | coil temperature | 83.61 | °C |
| Ex 04-05.6a | copper core area | 562.5 | nm² |
| Ex 04-05.6b | copper fraction | 0.7031 | — |
| Ex 04-05.6c | resistance per µm with barrier | 29.87 | Ω/µm |
| Ex 04-05.6d | resistance per µm without barrier | 21 | Ω/µm |
| Ex 04-05.6e | capacitance per µm | 0.1240 | fF/µm |
| Ex 04-05.6f | RC of 100 µm | 37.02 | ps |
| Ex 04-05.6g | RC of 1 mm | 3.702 | ns |
| Ex 04-05.6h | 50% delay of 100 µm | 14.02 | ps |
| Ex 04-05.6i | 50% delay of 1 mm | 1.402 | ns |
| Ex 04-05.6j | resistance of 100 µm | 2987 | Ω |
| Ex 04-05.6k | capacitance of 100 µm | 12.40 | fF |
| Ex 04-05.6l | resistance of 1 mm | 29.87 | kΩ |
| Ex 04-05.6m | capacitance of 1 mm | 124.0 | fF |
| Ex 04-05.7a | current density at 50 µA | 8.889 | MA/cm² |
| Ex 04-05.7b | largest DC current at 0.3 MA/cm² | 1.688 | µA |
| Ex 04-05.7c | overload factor | 29.63 | — |
| Ex 04-05.7d | power density at the limit | 1.512×10^11 | W/m³ |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T 04-05.a | conduction electrons per m³ in copper | 8.49×10^28 | m⁻³ |
| T 04-05.b | distributed-line 50% delay coefficient | 0.3787 | — |
| T 04-05.c | copper resistance rise, 20 to 100 °C | 31 | % |

## 5. Simulate it

The lab ([labs/04-05-lab/](../labs/04-05-lab/README.md)) is a notebook plus an ngspice netlist:

1. **A Drude gas in a computer:** simulate thousands of electrons with random collisions in a field, and measure the drift velocity and mobility. *Predict first:* does doubling τ double the drift velocity?
2. **Resistance by slicing:** integrate a tapered trace's resistance and compare with simple approximations.
3. **Self-heating:** find the steady temperature of a copper conductor whose resistance rises as it heats, and the condition for thermal runaway.
4. **The distributed RC line:** simulate a wire as a ladder of R and C sections and find the 50% delay coefficient as the number of sections grows.

The netlist `wire_rc.cir` simulates the 1 mm wire of Example 04-05.6.

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Wire cross-section (width, thickness) | Lower resistance and electromigration risk | Area and routing density; thicker wires raise sidewall capacitance | Process architects and layout designers |
| Interconnect metal (Cu with barrier vs barrierless Mo, Ru, Co) | Narrow-line resistance, reliability | New deposition and etch tools, integration risk, higher bulk resistivity | Back-end process integration |
| Repeater insertion on long wires | Delay grows linearly instead of quadratically | Area, power, placement constraints | Physical-design teams |
| Power-grid metal share (and backside power) | Lower IR drop and current density | Routing resources, wafer thinning and bonding cost | Power-integrity and process teams |
| Doping level of a resistor or channel | Resistivity across orders of magnitude | Mobility falls, temperature dependence changes | Device and circuit designers |
| PCB copper weight and trace width | Lower resistance, cooler traces | Cost, etch precision, board thickness | Board designers |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Copper bulk resistivity | 1.68 µΩ·cm | [R-080](../../../reference/research-log.md#r-080--conduction-interconnect-metals-electromigration-and-backside-power) |
| Copper conduction-electron density | 8.49×10²⁸ m⁻³ | One per atom |
| Copper mean free time; mean free path | about 25 fs; 39–40 nm | Free-electron Drude estimate; first-principles value |
| Drift speed, 1 A in 1 mm² of copper | about 74 µm/s | |
| Copper temperature coefficient | 0.00393 /°C at 20 °C | +31% from 20 to 100 °C |
| Silicon mobilities (lightly doped) | µₙ ≈ 1400, µₚ ≈ 470 cm²/V·s | [R-080](../../../reference/research-log.md#r-080--conduction-interconnect-metals-electromigration-and-backside-power) |
| 1 oz PCB copper | 34 µm; 0.49 mΩ/□ | |
| Distributed-RC 50% delay | 0.38 RC; delay ∝ L² | |
| Electromigration limit, minimum Cu lines (ITRS 2015 projection) | 1.8 MA/cm² (2018) → 0.3 MA/cm² (2026) | **[Industry estimate]** |

## 8. Common mistakes

1. **Confusing current direction with electron motion.** Conventional current flows opposite to electron drift.
2. **Thinking electrons carry signals at their drift speed.** The field carries the signal; drift is micrometers per second.
3. **Equating high conductivity with high mobility.** Copper's electrons are less mobile than silicon's; copper wins on carrier density.
4. **Using bulk resistivity for nanometer wires.** Below the mean free path, surface and grain-boundary scattering raise resistivity, and barriers steal area.
5. **Forgetting that RC delay grows with length squared.** Halving a wire's length quarters its delay.
6. **Treating Ohm's law as universal.** It fails at high fields (velocity saturation), high frequencies, short lengths and in junctions.
7. **Mixing units in device problems.** Mobility in cm²/V·s with densities in m⁻³ gives answers off by 10⁴; convert first.
8. **Ignoring temperature.** A copper conductor at 100 °C has 31% more resistance than at 20 °C, and current ratings assume a temperature.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Copper is running out of room.** An imec tutorial (2024) notes that commercial chips have minimum interconnect pitches around 25 nm, heading below 20 nm, and that the combined barrier and liner "cannot be reduced below 2 to 3 nm without compromising functionality"; copper's mean free path is about 40 nm, so narrow copper lines suffer a large size effect ([R-080](../../../reference/research-log.md#r-080--conduction-interconnect-metals-electromigration-and-backside-power)) **[Established]**.
- **Alternative metals.** Bulk resistivities: Cu 1.68, Mo 5.3, Co 5.1–9.1 and Ru 5.7–7.4 µΩ·cm (the last two depend on crystal direction). Gall's first-principles analysis (2016) found that "in the limit of narrow wires … Mo, Co, and Ru approximately match the Cu resistivity", and they can be used without a barrier. Cobalt is already in commercial local interconnects; imec considers barrierless ruthenium with air gaps "the leading candidate for logic interconnects" ([R-080](../../../reference/research-log.md#r-080--conduction-interconnect-metals-electromigration-and-backside-power)) **[Established for Co; Contested for Ru]**.
- **Molybdenum in production.** In February 2025 Lam Research launched an atomic-layer-deposition tool for molybdenum, claiming better than 50% lower resistance than conventional tungsten "in most instances"; Micron said the tool let it bring molybdenum into mass production in its NAND ([R-080](../../../reference/research-log.md#r-080--conduction-interconnect-metals-electromigration-and-backside-power)) **[Established for the launch; the performance figure is a vendor claim]**.
- **Backside power delivery.** Intel's 18A process combines gate-all-around transistors with PowerVia backside power, first shipping in its Panther Lake client processors from late 2025; Intel's 2023 test chip reported more than 30% improvement in voltage droop and a 6% frequency benefit (vendor claims). TSMC's A16 node with "Super Power Rail" was first targeted for the second half of 2026; TSMC's April 2026 symposium materials showed it in 2027 ([R-080](../../../reference/research-log.md#r-080--conduction-interconnect-metals-electromigration-and-backside-power)) **[Established for Intel; TSMC timing Contested]**.
- **Electromigration.** The ITRS 2015 projection of tolerable current density in minimum copper lines (Figure 2) is a decade-old forecast; it is the trend, not the numbers, that has held up **[Industry estimate]**.

### Why it matters commercially

Interconnect has become a large share of the cost and the performance budget of leading-edge logic, and every lever here is a market. New metals (Mo, Ru) and their deposition and etch tools are a battleground for equipment makers; backside power delivery adds wafer bonding and thinning steps and changes how chips are designed; and power delivery from the board to the die (voltage regulators, package resistance) is a major differentiator for AI accelerators drawing hundreds of amperes at under a volt. For a corporate-development team, a credible interconnect or power-delivery story is often the difference between a node that delivers its promised performance and one that does not.

### Marketing vs Reality

- **"Our new metal has 50% lower resistance."** *Reality:* than what, at what line width, including which barrier? Bulk resistivity, narrow-line resistivity and the resistance of a finished via or contact are different numbers. Ask for line resistance per µm at the target width and its spread.
- **"Backside power gives 15–20% lower power."** *Reality:* vendor numbers compare a specific design at a specific point. Ask what share came from IR-drop reduction versus freed front-side routing, and what the extra process steps cost.
- **"Wires scale with the node."** *Reality:* local wire delay roughly holds, but global wire delay worsens every node at fixed die size. Ask how many metal layers, which are thick, and how repeaters are budgeted.
- **"The part is rated 3 A."** *Reality:* at what temperature rise and ambient? Current ratings are thermal statements.

### Questions for engineering leaders

1. **"What is the resistance per micrometer of your minimum-width wire, and how much of it comes from the barrier and the size effect?"** *Strong:* measured numbers at the target width, the barrier thickness and the metal choice, with plans for the next node. *Evasive:* bulk resistivity.
2. **"What sets your power grid's design: IR drop or electromigration, and at what current density?"** *Strong:* both limits, the worst-case current density, the temperature assumed and the EM lifetime model. *Evasive:* "we meet the foundry rules".
3. **"How do you handle global wires: repeaters, upper metal, or architectural changes?"** *Strong:* fraction of power and area spent on repeaters, the top-metal stack, and partitioning decisions. *Evasive:* no numbers.
4. **"What did backside power actually buy you on this design?"** *Strong:* droop, frequency and density gains measured on silicon, separated by mechanism, with the cost and yield impact. *Evasive:* the press-release percentage.

## 10. Concept check

1. Copper's electrons move at about $1.6\times10^6$ m/s. Why does 1 A in a 1 mm² copper wire correspond to a drift of only 74 µm/s?

   <details><summary>Answer</summary>

   The fast motion is random in direction and averages to zero. A field adds only a tiny bias between collisions, erased every 25 fs or so, so the net drift is minute. The current is large because there are $8.5\times10^{28}$ carriers per cubic meter.

   </details>

2. Which conducts better, a material with high mobility and few carriers or one with low mobility and many? Give an example of each.

   <details><summary>Answer</summary>

   Conductivity is $ne\mu$, so it depends on the product. Pure silicon has much higher mobility than copper but $10^{12}$ times fewer carriers, so copper conducts about $10^{11}$ times better.

   </details>

3. Why does a metal's resistance rise with temperature while a semiconductor's falls?

   <details><summary>Answer</summary>

   In a metal the carrier density is fixed and stronger lattice vibrations shorten τ. In a semiconductor, heat frees many more carriers (n rises exponentially), which outweighs the drop in mobility.

   </details>

4. Two traces have the same sheet resistance. One is 1 mm wide and 10 mm long, the other 0.1 mm wide and 1 mm long. Compare their resistances.

   <details><summary>Answer</summary>

   Both are 10 squares, so they have the same resistance, $10R_s$.

   </details>

5. Why does a wire's RC delay grow with the square of its length, and what is the standard fix?

   <details><summary>Answer</summary>

   Both $R$ and $C$ grow in proportion to length, so their product grows as length squared. Inserting repeaters splits the wire into segments, making total delay grow linearly.

   </details>

6. Why is electromigration mainly a power-grid problem rather than a signal-wire problem?

   <details><summary>Answer</summary>

   Supply currents flow one way continuously, steadily pushing metal atoms in one direction. Signal currents reverse as wires charge and discharge, so much of the atomic motion is undone.

   </details>

7. Why can't copper simply be made narrower without penalty below about 20 nm?

   <details><summary>Answer</summary>

   Its barrier and liner (2–3 nm minimum) take a growing share of the cross-section, and surfaces and grain boundaries within one mean free path (about 40 nm) scatter electrons and raise its resistivity.

   </details>

Problem set: [04-05 problems](../problems/04-05-problems.md) · [solutions](../solutions/04-05-solutions.md).

## 11. Key terms

[Electric current](../../../reference/glossary.md#electric-current) ·
[Current density](../../../reference/glossary.md#current-density) ·
[Continuity equation](../../../reference/glossary.md#continuity-equation) ·
[Drift velocity](../../../reference/glossary.md#drift-velocity) ·
[Drude model](../../../reference/glossary.md#drude-model) ·
[Mobility](../../../reference/glossary.md#mobility) ·
[Resistivity](../../../reference/glossary.md#resistivity) ·
[Ohm's law](../../../reference/glossary.md#ohms-law) ·
[Mean free path](../../../reference/glossary.md#mean-free-path) ·
[Sheet resistance](../../../reference/glossary.md#sheet-resistance) ·
[Temperature coefficient of resistance](../../../reference/glossary.md#temperature-coefficient-of-resistance) ·
[Joule heating](../../../reference/glossary.md#joule-heating) ·
[Electromigration](../../../reference/glossary.md#electromigration) ·
[Distributed RC line](../../../reference/glossary.md#distributed-rc-line) ·
[Backside power delivery](../../../reference/glossary.md#backside-power-delivery)

## 12. Connections

- **Previous:** [04-04](04-04-potential-capacitance-and-dielectrics.md) (potential and capacitance; low-k dielectrics), [04-01](04-01-mechanics-essentials.md) (Newton's law with drag), [01-10](../../01-calculus-for-engineers/chapters/01-10-multivariable-calculus-2.md) (flux and the divergence theorem behind KCL).
- **Next:** [04-06 Magnetic Fields and Forces](04-06-magnetic-fields-and-forces.md): moving charges also feel and produce magnetic forces, including the Hall effect, which measures carrier density and sign.
- **Used in:** [06-01](../../06-circuit-analysis-1-dc/chapters/06-01-charge-current-voltage-power.md) and [06-02](../../06-circuit-analysis-1-dc/chapters/06-02-circuit-elements-and-ohms-law.md) (circuit current and Ohm's law), [09-03](../../09-semiconductor-devices/chapters/09-03-drift-and-diffusion.md) (drift, mobility and velocity saturation), [19-05](../../19-digital-vlsi-design/chapters/19-05-interconnect.md) (interconnect RC and repeaters), [25-09](../../25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md) (electromigration).

## 13. Further study

- Halliday, D., Resnick, R. and Walker, J., *Fundamentals of Physics*, the chapter on current and resistance.
- Purcell, E. M. and Morin, D. J., *Electricity and Magnetism*, 3rd ed., Cambridge University Press, 2013, chapter 4.
- Ashcroft, N. W. and Mermin, N. D., *Solid State Physics*, Saunders, 1976, chapters 1–2 (the Drude and Sommerfeld models).
- Soulié, J.-P. et al., "Selecting alternative metals for advanced interconnects", *Journal of Applied Physics* 136, 171101, 2024 (arXiv:2406.09106), a readable tutorial on the interconnect problem.

## 14. Sources

1. Halliday, D., Resnick, R. and Walker, J., *Fundamentals of Physics*, Wiley (any recent edition).
2. Ashcroft, N. W. and Mermin, N. D., *Solid State Physics*, Saunders, 1976 (free-electron Fermi velocity of copper, $1.57\times10^6$ m/s, as tabulated by HyperPhysics). [R-080]
3. NIST, 2022 CODATA recommended values ($m_e$; exact $e$, $k$). [R-073]
4. Soulié, J.-P. et al. (imec), "Selecting alternative metals for advanced interconnects", *J. Appl. Phys.* 136, 171101, 2024. [R-080]
5. Gall, D., "Electron mean free path in elemental metals", *J. Appl. Phys.* 119, 085101, 2016; Zhou, T., Jog, A. and Gall, D., *Appl. Phys. Lett.* 120, 241603, 2022. [R-080]
6. Hu, C., *Modern Semiconductor Devices for Integrated Circuits*, Pearson, 2010, Table 2-1 (silicon mobilities). [R-080]
7. Lienig, J. and Thiele, M., "The pressing need for electromigration-aware physical design", *Proc. ISPD*, 2018 (reproducing ITRS 2015). [R-080]
8. Copper Development Association and ASTM B193 / IEC 60028 (copper temperature coefficient 0.00393 /°C). [R-080]
9. Lam Research press release, 19 February 2025; Intel press release, 5 June 2023; eeNews Europe, 15 October 2025; SemiEngineering, 25 April 2024 and 27 April 2026. [R-080]
