<!-- status: reviewed -->
# 04-07 · Faraday's Law, Lenz's Law and Inductance

| | |
|---|---|
| **Course** | [04 · Physics for EE](../README.md) |
| **University equivalent** | Induction and inductance in University Physics II (Halliday, Resnick & Walker, the chapter on induction and inductance; Purcell & Morin, chapter 7; MIT 8.02, weeks 9–11) |
| **Prerequisites** | [04-06 Magnetic Fields and Forces](04-06-magnetic-fields-and-forces.md), [04-04](04-04-potential-capacitance-and-dielectrics.md) (potential, energy in fields), [04-05](04-05-current-resistance-and-conduction.md) (resistivity), [07-02](../../07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md) (RL transients) |
| **Estimated study hours** | 10 |
| **Last verified** | 2026-11-18 |

**Learning objectives.** After this chapter you can:

1. Compute magnetic flux and the EMF induced by a changing field, a moving conductor or a rotating coil, using Faraday's law with Lenz's law for direction.
2. Explain eddy currents and the skin effect, and compute skin depth and its effect on a wire's AC resistance.
3. Define self- and mutual inductance and derive them for solenoids, toroids, gapped cores (with reluctance) and coupled coils.
4. Compute stored magnetic energy and energy density, and explain why a gapped inductor stores its energy in the gap.
5. Analyze ideal transformers and inductive power transfer, and read a power inductor's datasheet (DCR, saturation current, self-resonance).

## 1. Big picture

[04-06](04-06-magnetic-fields-and-forces.md) showed that currents make magnetic fields. In 1831 Michael Faraday found the converse that makes electrical engineering possible: a *changing* magnetic flux makes a voltage. Every generator in every power plant, every transformer on the grid, every inductor in a phone's power supply, every wireless charger and every induction cooktop runs on this one law. Its sign, **Lenz's law**, says the induced current always opposes the change, which is why inductors resist sudden changes in current and why a magnet falls slowly through a copper pipe. And it explains when voltage stops being a simple, path-independent quantity, the source of ground loops and pickup in fast circuits.

- **Power conversion:** inductors and transformers store and transfer energy in every DC-DC converter and power supply ([22](../../22-power-electronics-and-energy-conversion/README.md)).
- **The grid and machines:** generators, transformers and motors (with their back-EMF) all follow from Faraday's law.
- **Signal integrity:** inductance of wires, packages and bond wires sets ringing and supply noise; changing flux through a loop is how crosstalk and ground bounce arise ([24](../../24-high-speed-io-signal-integrity-and-photonics/README.md)).
- **RF and wireless:** on-chip inductors set the quality of oscillators and filters; coupled coils deliver wireless charging ([21](../../21-rf-and-microwave-engineering/README.md)).

## 2. Intuition first

**Change makes voltage.** A steady magnet beside a loop of wire does nothing. Move it, or change its strength, or turn the loop, and a voltage appears around the loop for as long as the magnetic flux through the loop is changing. The faster the change, the bigger the voltage. Faraday's law is a rate law: what matters is $d\Phi/dt$, not Φ.

**Nature resists change.** The induced current always flows so as to oppose the change in flux that caused it (Lenz's law). Push a magnet toward a coil and the coil's current makes a field that pushes back; pull it away and the coil pulls it back. If the induced current *helped* the change, a nudge would grow without limit and create energy from nothing. Lenz's law is energy conservation.

**Inductance is electrical inertia.** A coil's own changing current changes its own flux, so the coil induces a voltage on itself opposing the change. Current through an inductor behaves like the velocity of a heavy flywheel: it cannot change instantly, and trying to stop it suddenly produces an enormous voltage (the "inductive kick" of [07-02](../../07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md)). The energy lives in the magnetic field, as a capacitor's lives in the electric field.

**A finance analogy, and its limits.** Inductance is like momentum in a trend-following portfolio: it resists changes in the flow, carrying it through brief shocks. *Where it breaks:* market momentum is a statistical tendency that can reverse without warning; an inductor's opposition to change is exact ($v = L\,di/dt$), and the energy it stores is returned in full (minus losses), never "evaporates".

![Left: the magnetic flux through a loop as a small magnet passes through it, rising to a peak and falling, with the induced EMF, its negative derivative, swinging negative then positive. Right: skin depth in copper against frequency on log axes, falling from 8.4 mm at 60 Hz to 65 µm at 1 MHz and 2.1 µm at 1 GHz.](../../../assets/figures/04-07/faraday-and-skin.svg)

*Figure 1. Faraday's law responds to the rate of change of flux. At high frequency, induced currents also push current to a conductor's surface, within the skin depth.*

## 3. Theory

> **Notation for this chapter.** $\Phi_B$ (or Φ) is magnetic flux in webers (1 Wb = 1 T·m² = 1 V·s). ℰ is electromotive force (EMF), a voltage around a closed path. $L$ is self-inductance and $M$ mutual inductance, in henries (1 H = 1 Wb/A = 1 V·s/A). $\mathcal R$ is reluctance (A/Wb). δ is skin depth. Following [notation.md](../../../reference/notation.md), time-varying voltages and currents are $v$ and $i$.

### 3.1 Magnetic flux and Faraday's law

The **magnetic flux** through a surface is $\Phi_B = \iint\vec B\cdot\hat n\,dA$, or $BA\cos\theta$ for a uniform field through a flat loop. **Faraday's law** states that the EMF around a closed loop equals minus the rate of change of the flux through it:

$$
\mathcal E = \oint\vec E\cdot d\vec l = -\frac{d\Phi_B}{dt}, \qquad \mathcal E = -N\frac{d\Phi_B}{dt}\ \ \text{for a coil of }N\text{ turns} .
$$

The flux can change because $B$ changes, because the loop's area changes, or because the loop turns; Faraday's law covers all three.

**The field is no longer conservative.** In electrostatics, $\oint\vec E\cdot d\vec l = 0$ made voltage well defined (04-04). A changing magnetic flux makes the loop integral nonzero: the induced electric field circulates, and "the voltage between two points" now depends on the path between them. A voltmeter's leads form a loop; if changing flux threads that loop, the reading depends on how the leads are routed. This is why oscilloscope probes use short ground springs on fast signals, and why circuit boards keep signal and return paths close (small loop area, small induced voltage, [24](../../24-high-speed-io-signal-integrity-and-photonics/README.md)). KVL holds only for loops through which flux is not changing.

### 3.2 Lenz's law

**The induced current flows in the direction that opposes the change in flux.** It is the minus sign in Faraday's law, and the way to get directions without vector bookkeeping: if flux into a loop is increasing, the induced current makes a field out of the loop; if it is decreasing, the induced current tries to maintain it.

Consequences are everywhere. A magnet dropped through a copper pipe falls slowly: the pipe's induced currents oppose its motion (eddy-current braking, used in trains and roller coasters). Induction cooktops drive a high-frequency field into a steel pan, whose induced currents heat it. Metal detectors sense the field of the currents they induce in buried metal.

### 3.3 Motional EMF and generators

**A sliding rod.** A conducting rod of length $\ell$ slides at speed $v$ along two rails in a perpendicular field $B$, closing a circuit with resistance $R$. The loop's area grows at rate $\ell v$, so $|\mathcal E| = B\ell v$. The same result comes from the magnetic force on the rod's charges, $qvB$ along the rod, whose work per unit charge over length $\ell$ is $B\ell v$: motional EMF is the Lorentz force in disguise.

The current $I = B\ell v/R$ in the rod feels a force $I\ell B$ opposing its motion (Lenz). Pushing the rod at constant speed takes mechanical power $Fv = (B\ell)^2v^2/R$, which equals the electrical power $I^2R$ dissipated: the magnetic field converts mechanical work into electrical energy without doing any work itself (Example 04-07.2).

**A generator.** A coil of $N$ turns and area $A$ rotating at angular speed ω in a field $B$ has flux $NBA\cos\omega t$ linking it, so

$$
\mathcal E = NBA\omega\sin\omega t ,
$$

a sinusoid at the rotation frequency. Every AC generator works this way. Run the same machine as a motor and the rotating coil generates a **back-EMF** opposing the supply; the current, and so the torque, is set by the difference. A motor's back-EMF is why its current is large at start-up and small at speed.

### 3.4 Eddy currents and the skin effect

In a solid conductor, a changing flux induces currents that swirl in closed loops within the metal: **eddy currents**. They dissipate power ($I^2R$) and, by Lenz's law, oppose the change that drives them. Transformer and motor cores are therefore built from thin insulated laminations (which cut the eddy-current loops) or from ferrites and powder cores (which are poor conductors).

**The skin effect.** Inside a wire carrying AC, the changing magnetic field of the current induces eddy currents that oppose the current at the wire's center and reinforce it near the surface. The current crowds into a layer of thickness about the **skin depth**

$$
\delta = \sqrt{\frac{2\rho}{\omega\mu}} = \sqrt{\frac{\rho}{\pi f\mu}} ,
$$

where $\mu = \mu_r\mu_0$. In copper, δ is 8.4 mm at 60 Hz, 65 µm at 1 MHz and 2.1 µm at 1 GHz (Figure 1). A wire much thicker than δ carries current only in a surface shell about δ thick, so its resistance rises roughly as $\sqrt f$. High-frequency conductors therefore use stranded, insulated **litz wire**, flat strips or plated surfaces, and the roughness of a circuit board's copper matters at tens of gigahertz ([24](../../24-high-speed-io-signal-integrity-and-photonics/README.md)).

> **Going deeper — where δ comes from.** Inside a good conductor, Faraday's law with Ampère's law (with $\vec J = \sigma\vec E$) gives a diffusion equation, $\nabla^2\vec B = \mu\sigma\,\partial\vec B/\partial t$. For a sinusoid at angular frequency ω entering a flat conductor, the solution is $B\propto e^{-x/\delta}\cos(\omega t - x/\delta)$ with $\delta = \sqrt{2/(\omega\mu\sigma)}$: the field, and the current, decay by $1/e$ every skin depth and lag in phase as they go. For a round wire, the exact current distribution involves Bessel functions (Example 04-07.3); [13](../../13-electromagnetics/README.md) develops the derivation.

### 3.5 Inductance

**Self-inductance.** A coil's current $i$ produces flux through its own turns. Define the **flux linkage** $\lambda = N\Phi_B$; for a coil without saturating material it is proportional to the current, and the constant is the **inductance**:

$$
\lambda = Li, \qquad v = \frac{d\lambda}{dt} = L\frac{di}{dt}
$$

(with the passive sign convention, the voltage across the inductor equals the EMF the coil develops opposing the change). An inductor resists *changes* in current: steady current passes freely (apart from wire resistance), while a sudden change produces a large voltage. With a resistor, current rises or decays with time constant $\tau = L/R$ ([07-02](../../07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md)).

**A long solenoid.** $N$ turns, length $\ell$, cross-section $A$: $B = \mu_0Ni/\ell$ (04-06), so $\lambda = N\cdot BA = \mu_0N^2Ai/\ell$ and

$$
L = \frac{\mu_0N^2A}{\ell} .
$$

Inductance grows as the *square* of the turns: doubling the turns doubles both the field per ampere and the number of turns it links.

**Cores and the magnetic circuit.** Fill the solenoid with a material of relative permeability $\mu_r$ and $L$ rises by $\mu_r$. For a core of any shape, think of it as a **magnetic circuit**: the "magnetomotive force" $Ni$ drives flux Φ through the core's **reluctance** $\mathcal R = l/(\mu_r\mu_0A)$, as voltage drives current through resistance. Reluctances in series add: a core of path length $l_c$ with an air gap $g$ has

$$
\mathcal R = \frac{l_c}{\mu_r\mu_0A} + \frac{g}{\mu_0A}, \qquad \Phi = \frac{Ni}{\mathcal R}, \qquad L = \frac{N^2}{\mathcal R} .
$$

Because $\mu_r$ is in the thousands, even a fraction of a millimeter of gap can dominate the reluctance. This is the quantitative form of 04-06's result: a gap lowers inductance and raises saturation current in the same ratio (Example 04-07.5).

**A coaxial line.** Between conductors of radii $a$ and $b$, $B = \mu_0i/(2\pi r)$; the flux per unit length through the space between them is $\int_a^b\mu_0i\,dr/(2\pi r)$, so $L/\ell = (\mu_0/2\pi)\ln(b/a)$. Together with 04-04's $C/\ell = 2\pi\varepsilon/\ln(b/a)$, it fixes the cable's characteristic impedance and wave speed ([04-08](04-08-maxwell-preview.md), [13-07](../../13-electromagnetics/chapters/13-07-transmission-lines-time-domain.md)).

**Mutual inductance.** Current $i_1$ in coil 1 links flux through coil 2: $\lambda_2 = Mi_1$, inducing $v_2 = M\,di_1/dt$. By symmetry the same $M$ works the other way. It is bounded by the self-inductances, $M = k\sqrt{L_1L_2}$ with **coupling coefficient** $0 \le k \le 1$: near 1 for windings on a shared core, much less for separated coils such as a wireless charger's (Example 04-07.7).

### 3.6 Energy in the magnetic field

Building up current $i$ in an inductor against its own EMF takes power $vi = Li\,di/dt$, so the energy stored is

$$
U = \int_0^IL\,i\,di = \frac12LI^2 .
$$

For a long solenoid, $\tfrac12LI^2 = \tfrac12(\mu_0N^2A/\ell)I^2$, and since $B = \mu_0NI/\ell$ this equals $(B^2/2\mu_0)\cdot A\ell$. The energy density of a magnetic field is therefore

$$
u_B = \frac{B^2}{2\mu} ,
$$

the magnetic counterpart of $\tfrac12\varepsilon E^2$. At 1 T in air it is about 0.4 MJ/m³.

**Why the gap stores the energy.** In a gapped core the flux density $B$ is nearly the same in the core and in the gap, but $u = B^2/(2\mu)$ is $\mu_r$ times larger where µ is smaller. A half-millimeter gap in a ferrite core with $\mu_r$ = 2000 holds 95% of the inductor's energy (Example 04-07.5). Energy-storage inductors in power converters are therefore built with gaps (or with powder cores, whose gaps are distributed between particles): the gap is where the energy goes, and the core merely guides the flux to it.

### 3.7 Transformers and inductive power transfer

Two windings on a shared high-permeability core are linked by the same flux Φ. Faraday's law gives $v_1 = N_1\,d\Phi/dt$ and $v_2 = N_2\,d\Phi/dt$, so for an **ideal transformer** (perfect coupling, no loss, negligible magnetizing current)

$$
\frac{v_2}{v_1} = \frac{N_2}{N_1}, \qquad \frac{i_2}{i_1} = \frac{N_1}{N_2}, \qquad R_{\text{seen}} = \Big(\frac{N_1}{N_2}\Big)^2R_{\text{load}} ,
$$

the current ratio following from power conservation ($v_1i_1 = v_2i_2$). A transformer changes voltage, current and impedance levels, and isolates the two sides galvanically. It works only with changing flux: DC passes no power through it.

![An ideal transformer: a rectangular core with N1 turns on the left leg and N2 turns on the right; a single flux circulates around the core, so each winding's voltage is its turns times the rate of change of flux, and the voltage ratio equals the turns ratio.](../../../assets/figures/04-07/transformer.svg)

*Figure 2. One flux, two windings: the voltage per turn is the same on both.*

**Wireless charging.** A Qi charger is a transformer with an air gap: a transmitter coil in the pad and a receiver coil in the phone, coupled weakly ($k$ well below 1) across a few millimeters. Both coils are resonated with capacitors so that a modest current in the transmitter induces a useful voltage in the receiver. The Qi standard has grown from 5 W in 2010 to 25 W in 2025, adding magnets for alignment (which raises and stabilizes $k$) and a 360 kHz operating frequency in its magnetic power profile ([R-082](../../../reference/research-log.md#r-082--inductive-power-transfer-power-inductors-and-integrated-magnetics)).

**Real inductors.** A practical inductor is specified by its inductance, its winding resistance (DCR), its **saturation current** (at which inductance has fallen by a stated percentage, often 20–30%), its **rms current rating** (for a stated temperature rise from $I^2R$ heating), and its **self-resonant frequency**, above which the winding's own capacitance dominates and the part stops acting as an inductor. On chips, spiral inductors are limited by metal resistance and substrate eddy currents to quality factors $Q = \omega L/R$ of roughly 5–20 at gigahertz frequencies ([R-082](../../../reference/research-log.md#r-082--inductive-power-transfer-power-inductors-and-integrated-magnetics)).

![Left: inductance and saturation current of a ferrite core against air-gap length on a log scale: inductance falls from about 800 µH while saturation current rises from about 0.4 A, crossing near 1 mm. Right: energy stored at saturation rises almost linearly with gap length.](../../../assets/figures/04-07/gapped-inductor.svg)

*Figure 3. The gap trade (Example 04-07.5): inductance down, saturation current up, stored energy up.*

## 4. Worked examples

### Example 04-07.1 — EMF from a changing field (tier A)

**Setup.** A 100-turn coil of area 10 cm² sits perpendicular to a field that ramps uniformly from 0 to 0.2 T in 10 ms. Find (a) the change in flux per turn, (b) the EMF, and (c) the current if the coil's circuit has 10 Ω. (d) Which way does the current circulate?

**Solution.** (a) $\Delta\Phi = \Delta B\cdot A = 0.2\times10^{-3} = $ **2×10⁻⁴ Wb**.

(b) $|\mathcal E| = N\,\Delta\Phi/\Delta t = 100\times2\times10^{-4}/0.01 = $ **2 V**.

(c) $I = 2/10 = $ **0.2 A**.

(d) By Lenz's law, the current makes a field opposing the increase: opposite to the applied field inside the coil.

**Units check.** Wb/s = T·m²/s = (V·s/m²)(m²)/s = V ✓.

### Example 04-07.2 — A sliding rod and a generator (tier B)

**Setup.** (a) A rod 0.5 m long slides at 4 m/s on rails in a 0.5 T field, closing a 2 Ω circuit. Find the EMF, the current, the retarding force and the mechanical power required. (b) A generator coil of 200 turns and 0.01 m² rotates at 3000 rpm in 0.5 T. Find the peak and rms EMF.

**Solution.** (a) $\mathcal E = B\ell v = $ **1 V**; $I = 1/2 = $ **0.5 A**; $F = I\ell B = $ **0.125 N**; $P = Fv = $ **0.5 W**, equal to $I^2R = 0.25\times2$ ✓.

(b) 3000 rpm is 50 rev/s, ω = 2π×50 = 314.16 rad/s. Peak $NBA\omega = 200\times0.5\times0.01\times314.16 = $ **314.2 V**; rms $314.2/\sqrt2 = $ **222.1 V**.

### Example 04-07.3 — Skin depth and AC resistance (tier B)

**Setup.** (a) Find the skin depth in copper (ρ = 1.68 µΩ·cm, $\mu_r$ = 1) at 60 Hz, 100 kHz, 1 MHz and 1 GHz. (b) A copper wire 1 mm in diameter carries 1 MHz current. Estimate its AC-to-DC resistance ratio with the thin-shell approximation $R_{ac}/R_{dc} \approx a/(2\delta)$. (c) The exact result for a round wire uses Bessel functions; the lab computes it as 4.094. Why is the shell estimate low?

**Solution.** (a) $\delta = \sqrt{\rho/(\pi f\mu_0)}$: **8.422 mm**, **0.2063 mm**, **65.23 µm** and **2.063 µm**.

(b) The current flows in a shell of area about $2\pi a\delta$ instead of $\pi a^2$, so $R_{ac}/R_{dc} \approx a/(2\delta) = 0.5/(2\times0.06523) = $ **3.832**.

(c) For a flat conductor, exponential decay is exactly equivalent to a uniform layer of thickness δ, so the decay itself is not the error; curvature is. A shell of thickness δ in a round wire has area $\pi a^2 - \pi(a - \delta)^2 = 2\pi a\delta - \pi\delta^2$, smaller than $2\pi a\delta$; using it gives $a^2/(2a\delta - \delta^2)$ = **4.100**, whose first-order form is $a/(2\delta) + \tfrac14$ = **4.082**. The exact Bessel-function result, **4.094**, lies between them.

**Interpretation.** A 1 mm wire at 1 MHz has four times its DC resistance; at the 100 kHz to few-MHz frequencies of switching converters, winding loss is dominated by skin and proximity effects, which is why litz wire and flat foil windings exist.

### Example 04-07.4 — An air-core solenoid (tier B)

**Setup.** A solenoid of 500 turns is 10 cm long with a radius of 1 cm. Find (a) its inductance (long-solenoid formula), (b) the energy stored at 2 A, (c) the field inside, and (d) the energy density and the energy it implies over the coil's volume.

**Solution.** (a) $L = \mu_0N^2\pi r^2/\ell = 1.2566\times10^{-6}\times2.5\times10^5\times3.1416\times10^{-4}/0.1 = $ **0.9870 mH**.

(b) $U = \tfrac12LI^2 = $ **1.974 mJ**.

(c) $B = \mu_0NI/\ell = $ **12.57 mT**.

(d) $u = B^2/(2\mu_0) = $ **62.83 J/m³**; times the volume $\pi r^2\ell = 3.142\times10^{-5}$ m³ gives **1.974 mJ** ✓. (A real 10 cm × 1 cm coil is not quite "long": its inductance is about 8% lower, Nagaoka's end correction, which the lab computes.)

### Example 04-07.5 — A gapped ferrite inductor (tier C)

**Setup.** The core of 04-06 Example 8 (path length 5 cm, $\mu_r$ = 2000, 20 turns) has a cross-section of 40 mm² and a 0.5 mm gap. Find (a) the core's and the gap's reluctance, (b) the inductance with and without the gap, (c) the saturation current at 100 °C ($B_s$ = 0.39 T), (d) the energy stored at that current, and the fraction in the gap, and (e) the energy an ungapped core stores at its own saturation.

**Solution.** (a) $\mathcal R_c = l_c/(\mu_r\mu_0A) = 0.05/(2000\times1.2566\times10^{-6}\times4\times10^{-5})$ = **4.974×10⁵ A/Wb**; $\mathcal R_g = g/(\mu_0A)$ = **9.947×10⁶ A/Wb**, twenty times larger.

(b) $L = N^2/\mathcal R$: **38.30 µH** gapped and **804.2 µH** ungapped.

(c) Saturation when $\Phi = B_sA$: $I = B_sA\mathcal R/N = 0.39\times4\times10^{-5}\times1.0445\times10^7/20 = $ **8.147 A**.

(d) $U = \tfrac12LI^2 = $ **1.271 mJ**; the fraction in the gap is $\mathcal R_g/\mathcal R$ = **95.24%** (energy divides like voltage across series resistors, since the same flux crosses both).

(e) Ungapped, saturation comes at 0.388 A, storing only **60.52 µJ**: the gap multiplies the storable energy by 21.

### Example 04-07.6 — A transformer (tier A)

**Setup.** A transformer steps 230 V rms down to 12 V rms with 1150 primary turns. (a) How many secondary turns? (b) The secondary supplies 2 A to a load. Find the primary current (ideal transformer). (c) A 6 Ω load on the secondary looks like what resistance from the primary?

**Solution.** (a) $N_2 = 1150\times12/230 = $ **60 turns**.

(b) $i_1 = i_2N_2/N_1 = 2\times60/1150 = $ **0.1043 A**.

(c) $(1150/60)^2\times6 = $ **2204 Ω**.

### Example 04-07.7 — Coupled coils of a wireless charger (tier B)

**Setup.** A transmitter coil and a receiver coil each have 10 µH, with coupling $k$ = 0.5 (an illustrative value). The transmitter carries a 1 A-amplitude sinusoid at 360 kHz. Find (a) the mutual inductance, (b) the open-circuit voltage amplitude at the receiver, and (c) the voltage across the transmitter coil. (d) Repeat (b) for $k$ = 0.2 and 0.8. Confirm (b) and (c) in ngspice.

**Solution.** (a) $M = k\sqrt{L_1L_2} = $ **5 µH**.

(b) $|v_2| = \omega M|i_1| = 2\pi\times360\times10^3\times5\times10^{-6}\times1 = $ **11.31 V**.

(c) $|v_1| = \omega L_1|i_1| = $ **22.62 V**.

(d) Proportional to $k$: **4.524 V** at 0.2 and **18.10 V** at 0.8.

**Simulation.** The netlist [labs/04-07-lab/coupled_coils.cir](../labs/04-07-lab/coupled_coils.cir) uses ngspice's coupled-inductor (`K`) element and reproduces both voltages.

**Interpretation.** Misalignment lowers $k$ and with it the received voltage; that is why Qi's magnetic power profile adds magnets that pull the phone into alignment.

### Example 04-07.8 — Why integrated regulators run at high frequency (tier C)

**Setup.** A buck converter steps 1.7 V down to 1.05 V. Its inductor sees $v_L = V_{in} - V_{out}$ for the fraction $D = V_{out}/V_{in}$ of each switching period, so the current ripple is $\Delta i = (V_{in} - V_{out})DT/L$. (a) Find $D$. (b) With a 2 nH inductor (an assumed value, typical of a package trace) at 140 MHz, find the ripple. (c) What inductance would give the same ripple at 1 MHz?

**Solution.** (a) $D = 1.05/1.7 = $ **0.6176**.

(b) $\Delta i = 0.65\times0.6176/(140\times10^6\times2\times10^{-9}) = $ **1.434 A**.

(c) Ripple scales as $1/(fL)$, so 140 times the inductance: **280 nH**.

**Interpretation.** Faraday's law, $v = L\,di/dt$, trades frequency for inductance: at 140 MHz, nanohenries of air-core inductance printed in the package suffice, as in Intel's integrated voltage regulators ([R-082](../../../reference/research-log.md#r-082--inductive-power-transfer-power-inductors-and-integrated-magnetics)). The price is switching loss, which grows with frequency.

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 04-07.1a | change in flux per turn | 2×10^-4 | Wb |
| Ex 04-07.1b | induced EMF | 2 | V |
| Ex 04-07.1c | induced current | 0.2 | A |
| Ex 04-07.2a | motional EMF | 1 | V |
| Ex 04-07.2b | current | 0.5 | A |
| Ex 04-07.2c | retarding force | 0.125 | N |
| Ex 04-07.2d | mechanical power | 0.5 | W |
| Ex 04-07.2e | generator peak EMF | 314.2 | V |
| Ex 04-07.2f | generator rms EMF | 222.1 | V |
| Ex 04-07.3a | skin depth at 60 Hz | 8.422 | mm |
| Ex 04-07.3b | skin depth at 100 kHz | 0.2063 | mm |
| Ex 04-07.3c | skin depth at 1 MHz | 65.23 | µm |
| Ex 04-07.3d | skin depth at 1 GHz | 2.063 | µm |
| Ex 04-07.3e | AC/DC resistance, shell estimate | 3.832 | — |
| Ex 04-07.3f | AC/DC resistance, exact | 4.094 | — |
| Ex 04-07.3g | AC/DC resistance, curved shell | 4.100 | — |
| Ex 04-07.3h | AC/DC resistance, first-order curvature correction | 4.082 | — |
| Ex 04-07.4a | solenoid inductance | 0.9870 | mH |
| Ex 04-07.4b | stored energy at 2 A | 1.974 | mJ |
| Ex 04-07.4c | field inside | 12.57 | mT |
| Ex 04-07.4d | energy density | 62.83 | J/m³ |
| Ex 04-07.4e | energy from density times volume | 1.974 | mJ |
| Ex 04-07.5a | core reluctance | 4.974×10^5 | A/Wb |
| Ex 04-07.5b | gap reluctance | 9.947×10^6 | A/Wb |
| Ex 04-07.5c | inductance with gap | 38.30 | µH |
| Ex 04-07.5d | inductance without gap | 804.2 | µH |
| Ex 04-07.5e | saturation current with gap | 8.147 | A |
| Ex 04-07.5f | energy at saturation, gapped | 1.271 | mJ |
| Ex 04-07.5g | fraction of energy in the gap | 95.24 | % |
| Ex 04-07.5h | energy at saturation, ungapped | 60.52 | µJ |
| Ex 04-07.6a | secondary turns | 60 | — |
| Ex 04-07.6b | primary current | 0.1043 | A |
| Ex 04-07.6c | reflected resistance | 2204 | Ω |
| Ex 04-07.7a | mutual inductance | 5 | µH |
| Ex 04-07.7b | open-circuit receiver voltage | 11.31 | V |
| Ex 04-07.7c | transmitter coil voltage | 22.62 | V |
| Ex 04-07.7d | receiver voltage at k = 0.2 | 4.524 | V |
| Ex 04-07.7e | receiver voltage at k = 0.8 | 18.10 | V |
| Ex 04-07.8a | duty cycle | 0.6176 | — |
| Ex 04-07.8b | ripple at 140 MHz with 2 nH | 1.434 | A |
| Ex 04-07.8c | inductance for the same ripple at 1 MHz | 280 | nH |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T 04-07.a | magnetic energy density at 1 T in air | 3.979×10^5 | J/m³ |
| T 04-07.b | copper skin depth at 1 GHz | 2.063 | µm |

## 5. Simulate it

The lab ([labs/04-07-lab/](../labs/04-07-lab/README.md)) is a notebook plus an ngspice netlist:

1. **Faraday's law numerically:** compute the flux of a moving magnet through a loop and differentiate it. *Predict first:* how does the peak EMF change if the magnet moves twice as fast?
2. **The skin effect:** the exact current distribution in a round wire and its AC resistance against frequency.
3. **Inductance by integration:** compute a finite solenoid's inductance from Biot–Savart and compare with the long-solenoid formula.
4. **Mutual inductance of two loops** by Neumann's double integral, against separation.
5. **Gapped cores:** inductance, saturation current and stored energy against gap.

The netlist `coupled_coils.cir` simulates Example 04-07.7.

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Switching frequency of a converter | Smaller inductors and capacitors (ripple ∝ 1/(fL)) | Switching and core losses, EMI | Power-converter designers |
| Core air gap | Saturation current, stored energy, tolerance of µ variation | Inductance per turn (more turns, more copper loss), fringing loss | Magnetics designers |
| Winding construction (solid, litz, foil) | AC resistance at high frequency | Cost, fill factor, manufacturability | Magnetics designers |
| Core material and laminations | Lower eddy-current and hysteresis loss | Saturation flux (ferrite), cost, size | Magnetics and motor designers |
| Coil coupling in wireless power (alignment, magnets, spacing) | Efficiency and power transfer | Mechanical constraints, cost, standards compliance | Product and standards teams |
| On-chip inductor geometry and shielding | Quality factor (oscillator noise, filter loss) | Area, self-resonance, coupling to neighbors | RFIC designers |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Faraday's law | ℰ = −N dΦ/dt | 1 Wb/s = 1 V |
| Solenoid; gapped core | $\mu_0N^2A/\ell$; $N^2/\mathcal R$ | $L\propto N^2$ |
| Magnetic energy; density | $\tfrac12LI^2$; $B^2/(2\mu)$ ≈ 0.4 MJ/m³ at 1 T in air | |
| Copper skin depth | 8.4 mm (60 Hz), 0.21 mm (100 kHz), 65 µm (1 MHz), 2.1 µm (1 GHz) | $\delta\propto1/\sqrt f$ |
| Ideal transformer | $v_2/v_1 = N_2/N_1$; impedance × $(N_1/N_2)^2$ | |
| Qi wireless charging, as of Nov 2026 | 5 W (2010) → 15 W (2015) → 25 W (Qi2 25W, 2025); MPP at 360 kHz | [R-082](../../../reference/research-log.md#r-082--inductive-power-transfer-power-inductors-and-integrated-magnetics) |
| On-chip spiral inductor Q | roughly 5–20 at GHz | [R-082](../../../reference/research-log.md#r-082--inductive-power-transfer-power-inductors-and-integrated-magnetics) |

## 8. Common mistakes

1. **Using flux instead of its rate of change.** A large steady flux induces nothing.
2. **Losing the sign.** Use Lenz's law: the induced current opposes the change, not the field.
3. **Applying KVL around loops threaded by changing flux.** The loop integral of E is no longer zero there.
4. **Forgetting $N^2$.** Inductance scales with the square of the turns.
5. **Ignoring the gap.** In a gapped core, the gap, not the core, sets inductance and holds the energy.
6. **Expecting a transformer to pass DC.** It needs changing flux; DC saturates the core.
7. **Using DC resistance at high frequency.** Above the frequency where the skin depth approaches the conductor size, resistance rises roughly as $\sqrt f$.
8. **Reading an inductor's saturation current as its operating current.** The rms (thermal) rating is usually lower, and the saturation current falls when hot.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Wireless charging.** The Wireless Power Consortium's Qi specification went from 5 W (version 1.0, 2010) to 15 W (version 1.2, 2015); version 2.0 (April 2023) introduced the Magnetic Power Profile, with magnetic attachment and alignment and a 360 kHz operating frequency; version 2.2 (April 2025) supports up to 25 W, and the current version is 2.2.1, branded "Qi2 25W" at its July 2025 launch. The WPC reports more than 1.5 billion Qi2-certified products within a year of introduction ([R-082](../../../reference/research-log.md#r-082--inductive-power-transfer-power-inductors-and-integrated-magnetics)) **[Established; the device count is an Industry estimate]**.
- **Power inductors.** A representative voltage-regulator inductor, Coilcraft's XAL7070-102 (2012 datasheet revision), is 1.0 µH with 2.55 mΩ typical DCR, a 34.8 A saturation current (defined as a 30% inductance drop), a 20 A rms rating for a 20 °C rise, and a 64 MHz self-resonant frequency ([R-082](../../../reference/research-log.md#r-082--inductive-power-transfer-power-inductors-and-integrated-magnetics)) **[Established]**.
- **Integrated voltage regulators.** Intel's FIVR (APEC 2014) put 140 MHz multiphase buck regulators on the processor die with non-magnetic package-trace inductors: 59 inductors on 10 rails in a 20 mm × 8 mm area ([R-082](../../../reference/research-log.md#r-082--inductive-power-transfer-power-inductors-and-integrated-magnetics)) **[Established]**.
- **On-chip inductors.** Spiral inductors in standard CMOS reach quality factors of only about 5–20 at gigahertz frequencies, limited by metal resistance and substrate losses; patterned ground shields improved Q by up to 33% at 1–2 GHz in a classic 1998 study ([R-082](../../../reference/research-log.md#r-082--inductive-power-transfer-power-inductors-and-integrated-magnetics)) **[Established]**.

### Why it matters commercially

Magnetics are often the largest, costliest and least scalable components in a power path, and power delivery is now a central constraint for AI accelerators and data centers drawing kilowatts per board at under a volt. The industry's levers are higher switching frequency (wide-bandgap transistors, [22](../../22-power-electronics-and-energy-conversion/README.md)), better core materials, and integration of voltage regulation closer to the die, each a battleground for component makers, power-IC vendors and packaging houses. In consumer devices, wireless charging is a standards-driven market where coupling physics shows up as charging speed and heat.

### Marketing vs Reality

- **"25 W wireless charging."** *Reality:* the maximum under ideal alignment and temperature; coupling falls with misalignment, and heat throttles power. Ask for efficiency and power versus alignment and temperature.
- **"Saturation current 35 A."** *Reality:* defined by a stated inductance drop (here 30%) at a stated temperature; at hot operating temperature it is lower, and the rms thermal rating (20 A here) may be the real limit.
- **"Integrated inductor, no external magnetics."** *Reality:* integrated inductors are small and low-Q; the design compensates with high frequency and multiphase operation, paying in switching loss. Ask for end-to-end efficiency at the real load.
- **"Low-ESR, high-frequency inductor."** *Reality:* DCR is a DC number; at switching frequency, AC winding loss and core loss can dominate. Ask for loss at the operating ripple and frequency.

### Questions for engineering leaders

1. **"Where do the losses go in your power stage: switching, conduction, core or winding?"** *Strong:* a loss breakdown at the operating point, with how magnetics loss was measured. *Evasive:* only a peak efficiency number.
2. **"How does your inductor behave at maximum temperature and peak current?"** *Strong:* inductance versus current at hot temperature, margin to saturation, and thermal rating. *Evasive:* datasheet room-temperature values.
3. **"What sets your converter's switching frequency?"** *Strong:* the trade among magnetics size, switching loss, control bandwidth and EMI, with numbers. *Evasive:* "industry standard".
4. **"How do you handle coupling and alignment in your wireless charger?"** *Strong:* coupling coefficient range, magnetic alignment, foreign-object detection and thermal strategy. *Evasive:* only the headline wattage.

## 10. Concept check

1. A strong permanent magnet sits motionless inside a coil connected to a voltmeter. What does the voltmeter read? What if you pull the magnet out quickly?

   <details><summary>Answer</summary>

   Zero while it is stationary: flux is constant. Pulling it out changes the flux and induces an EMF; faster removal gives a larger, shorter pulse (the integral of the voltage, the total flux change, is the same).

   </details>

2. Why does a magnet fall slowly through a copper pipe but not through a plastic one?

   <details><summary>Answer</summary>

   The moving magnet's changing flux induces eddy currents in the conducting copper; by Lenz's law their field opposes the magnet's motion. Plastic does not conduct, so no currents flow.

   </details>

3. A voltmeter connected to two points on a circuit board near a switching power supply gives readings that change when you move its leads. Is the meter broken?

   <details><summary>Answer</summary>

   No. Changing magnetic flux through the loop formed by the leads and the board induces an EMF that depends on the loop's area and orientation. With changing flux, "the voltage between two points" depends on the path.

   </details>

4. Why does doubling a coil's turns quadruple its inductance?

   <details><summary>Answer</summary>

   Doubling the turns doubles the flux per ampere (twice the ampere-turns) and also doubles the number of turns that flux links. $L = N\Phi/i\propto N^2$.

   </details>

5. Where is the energy of a gapped ferrite inductor stored, and why?

   <details><summary>Answer</summary>

   Mostly in the gap. The flux density is nearly the same in core and gap, but energy density $B^2/(2\mu)$ is $\mu_r$ (thousands of) times higher in air, so a gap a hundredth of the core's length holds most of the energy.

   </details>

6. Why can't a transformer step up a DC voltage?

   <details><summary>Answer</summary>

   Induction needs changing flux. A steady primary current makes a steady flux, which induces nothing in the secondary (and a large DC current would saturate the core). DC-DC converters chop DC into AC first.

   </details>

7. Why do high-frequency windings use many fine insulated strands instead of one thick wire?

   <details><summary>Answer</summary>

   At high frequency, current flows only within about a skin depth of each conductor's surface. Many strands, each thinner than the skin depth and transposed along the length (litz wire), use the copper's full cross-section.

   </details>

Problem set: [04-07 problems](../problems/04-07-problems.md) · [solutions](../solutions/04-07-solutions.md).

## 11. Key terms

[Magnetic flux](../../../reference/glossary.md#magnetic-flux) ·
[Faraday's law](../../../reference/glossary.md#faradays-law) ·
[Lenz's law](../../../reference/glossary.md#lenzs-law) ·
[Motional EMF](../../../reference/glossary.md#motional-emf) ·
[Back-EMF](../../../reference/glossary.md#back-emf) ·
[Eddy currents](../../../reference/glossary.md#eddy-currents) ·
[Skin effect](../../../reference/glossary.md#skin-effect) ·
[Inductance](../../../reference/glossary.md#inductance) ·
[Reluctance](../../../reference/glossary.md#reluctance) ·
[Mutual inductance](../../../reference/glossary.md#mutual-inductance) ·
[Coupling coefficient](../../../reference/glossary.md#coupling-coefficient) ·
[Magnetic energy density](../../../reference/glossary.md#magnetic-energy-density) ·
[Transformer](../../../reference/glossary.md#transformer) ·
[Self-resonant frequency](../../../reference/glossary.md#self-resonant-frequency)

## 12. Connections

- **Previous:** [04-06](04-06-magnetic-fields-and-forces.md) (fields of currents, saturation and gaps), [04-04](04-04-potential-capacitance-and-dielectrics.md) (path-independent potential, which changing flux breaks; electric energy density), [07-02](../../07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md) (RL transients and inductive kick).
- **Next:** [04-08 Energy in Fields and Maxwell's Equations (Preview)](04-08-maxwell-preview.md) completes Ampère's law with the displacement current and shows that changing electric and magnetic fields sustain each other as waves.
- **Used in:** [07](../../07-circuit-analysis-2-transient-and-ac/README.md) (inductors in AC circuits), [13-03](../../13-electromagnetics/chapters/13-03-magnetostatics-and-inductance.md) and [13-04](../../13-electromagnetics/chapters/13-04-maxwells-equations.md) (inductance of structures, Maxwell's equations), [21](../../21-rf-and-microwave-engineering/README.md) (on-chip inductors), [22](../../22-power-electronics-and-energy-conversion/README.md) (magnetics design, motors, transformers), [24](../../24-high-speed-io-signal-integrity-and-photonics/README.md) (loop inductance, crosstalk, skin effect).

## 13. Further study

- Halliday, D., Resnick, R. and Walker, J., *Fundamentals of Physics*, the chapter on induction and inductance.
- Purcell, E. M. and Morin, D. J., *Electricity and Magnetism*, 3rd ed., Cambridge University Press, 2013, chapter 7.
- MIT OpenCourseWare 8.02 (Physics II: Electricity and Magnetism), the lectures on Faraday's law, inductance and transformers.
- Erickson, R. W. and Maksimović, D., *Fundamentals of Power Electronics*, the chapters on magnetics, for inductor and transformer design.

## 14. Sources

1. Halliday, D., Resnick, R. and Walker, J., *Fundamentals of Physics*, Wiley (any recent edition).
2. Purcell, E. M. and Morin, D. J., *Electricity and Magnetism*, 3rd ed., Cambridge University Press, 2013.
3. NIST, 2022 CODATA recommended values (µ₀). [R-073]
4. Wireless Power Consortium, "History of the Qi Specifications" (accessed November 2026) and news release of 23 July 2025. [R-082]
5. Coilcraft, Document 856-1, "Shielded Power Inductors – XAL7070", revised 25 July 2012. [R-082]
6. Burton, E. A. et al., "FIVR — Fully integrated voltage regulators on 4th generation Intel Core SoCs", *IEEE APEC*, 2014. [R-082]
7. Yue, C. P. and Wong, S. S., "On-chip spiral inductors with patterned ground shields for Si-based RF ICs", *IEEE JSSC* 33(5), 1998; Dai, C.-L. et al., "High Q-factor CMOS-MEMS inductor", DTIP 2008 (arXiv:0805.0915). [R-082]
