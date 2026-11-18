# Problems 04-07 · Faraday's Law, Lenz's Law and Inductance

Chapter: [04-07](../chapters/04-07-faraday-lenz-and-inductance.md) · Worked solutions: [04-07 solutions](../solutions/04-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $\mu_0 = 1.25663706127\times10^{-6}$ N/A²; $\varepsilon_0 = 8.8541878188\times10^{-12}$ F/m; $c = 299\,792\,458$ m/s; copper ρ = 1.68 µΩ·cm, $\mu_r$ = 1. Sinusoids are given by amplitude unless stated as rms. Answers to 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 04-07.1 [A]

**A collapsing field.** A 50-turn coil of area 20 cm² is perpendicular to a 0.5 T field that falls uniformly to zero in 0.1 s. Find the average EMF, and state the direction of the induced current relative to the original field.

### Problem 04-07.2 [A]

**Pulling a loop out of a field.** A square loop of side 10 cm and resistance 0.5 Ω is pulled at a steady 2 m/s out of a region of uniform 0.3 T field, perpendicular to its plane. While one side is still inside, find (a) the EMF, (b) the current, (c) the force needed and (d) the power dissipated.

### Problem 04-07.3 [A]

**Designing a generator coil.** A 50 Hz generator coil of area 0.02 m² turns in a 1.2 T field. How many turns are needed for 230 V rms?

### Problem 04-07.4 [B]

**Back-EMF.** A DC motor on a 12 V supply has armature resistance 0.5 Ω and back-EMF constant 0.02 V per rad/s. (a) Find the back-EMF and the current at 500 rad/s. (b) Find the current at stall (zero speed). (c) How much electrical power is converted to mechanical power at 500 rad/s?

### Problem 04-07.5 [B]

**Skin depths.** (a) Find the skin depth in copper at 50 kHz and at 10 GHz. (b) Find it at 50 Hz in transformer steel (take ρ = 0.1 µΩ·m and $\mu_r$ = 1000). Why are transformer laminations a few tenths of a millimeter thick?

### Problem 04-07.6 [B]

**A toroid's inductance.** A toroid of 100 turns has a rectangular cross-section: inner radius 2 cm, outer radius 3 cm, height 1 cm. (a) Derive $L = \mu_0N^2h\ln(b/a)/(2\pi)$ for an air core, and evaluate it. (b) Find $L$ with a ferrite core of $\mu_r$ = 2000 (assume it is linear).

### Problem 04-07.7 [B]

**An RL circuit.** A 10 mH inductor in series with 5 Ω is switched onto 10 V. Find (a) the time constant, (b) the final current, (c) the final stored energy and (d) the time for the current to reach 1 A.

### Problem 04-07.8 [B]

**A cable's inductance and impedance.** For the coaxial cable of 04-04 Problem 9 (radii 0.45 mm and 1.475 mm, $\varepsilon_r$ = 2.25), find (a) its inductance per meter, (b) its characteristic impedance $\sqrt{L/C}$ using $C/\ell = 2\pi\varepsilon/\ln(b/a)$, and (c) the wave speed $1/\sqrt{LC}$ per unit length, as a fraction of $c$.

### Problem 04-07.9 [B]

**Why motors are magnetic.** Compare the energy density of a 1.5 T magnetic field in air with that of a 3 MV/m electric field in air (air's breakdown limit). What does the ratio say about electromagnetic actuators?

### Problem 04-07.10 [B]

**Coupled windings.** Two windings have 100 µH and 25 µH with coupling 0.98. Find (a) the mutual inductance and (b) the turns ratio of an equivalent ideal transformer, $\sqrt{L_2/L_1}$.

### Problem 04-07.11 [A]

**Impedance matching.** What turns ratio makes an 8 Ω speaker look like 800 Ω to an amplifier?

### Problem 04-07.12 [C]

**Designing a gapped inductor.** Design a 10 µH inductor that must not saturate below 10 A at 100 °C ($B_s$ = 0.39 T), on a ferrite core of cross-section 40 mm², neglecting the core's own reluctance. (a) Find the minimum number of turns (round up). (b) Find the gap that gives 10 µH with that many turns. (c) Check the saturation current.

### Problem 04-07.13 [C]

**Eddy-current loss in laminations.** A lamination of thickness $t$ (thin compared with its width) carries a sinusoidal flux density of amplitude $B$ at frequency $f$. (a) By computing the EMF around a thin rectangular path at depth $x$ from the midplane and integrating the resulting $J^2\rho$, show that the time-averaged eddy loss per volume is $\pi^2f^2B^2t^2/(6\rho)$. (b) Evaluate it for silicon steel (ρ = 0.47 µΩ·m, density 7650 kg/m³) 0.35 mm thick at 50 Hz and 1.5 T, in W/m³ and W/kg. (c) Evaluate it at 400 Hz (aircraft power) with 0.1 mm laminations.

### Problem 04-07.14 [C]

**Ground bounce.** A chip's ground connection has 1 nH of inductance. (a) Output drivers switch 100 mA in 100 ps. Find the voltage induced across the ground connection. (b) Find it with ten such connections in parallel, neglecting their mutual inductance. (c) Why does mutual inductance make (b) optimistic?

### Problem 04-07.15 [C]

**Litz wire.** Using the exact round-wire result (computed in the lab), the AC/DC resistance ratio at 100 kHz is 1.466 for a 1 mm copper wire and 1.000 for a 0.1 mm strand. (a) Find the skin depth at 100 kHz. (b) Explain, using the ratio of radius to skin depth, why the thin strand is unaffected. (c) Why must litz strands be insulated and transposed, not just bundled?

### Problem 04-07.16 [C]

**Efficiency of a wireless link.** The coils of Example 04-07.7 (10 µH each, $k$ = 0.5, 360 kHz) are each resonated with a series capacitor, so only resistances remain at resonance. Each coil has 0.1 Ω of resistance and the receiver drives a 5 Ω load. (a) Show that the receiver reflects a resistance $(\omega M)^2/(R_2 + R_L)$ into the transmitter, and evaluate it. (b) Find the link efficiency $\eta = \frac{R_{\text{refl}}}{R_{\text{refl}} + R_1}\cdot\frac{R_L}{R_2 + R_L}$. (c) Find each coil's quality factor $\omega L/R$.

---

## Objective coverage

| Learning objective (chapter 04-07) | Problems |
|---|---|
| 1. Flux, Faraday's and Lenz's laws, motional EMF, generators and motors | 1, 2, 3, 4 |
| 2. Eddy currents and the skin effect | 5, 13, 15 |
| 3. Self- and mutual inductance, cores and reluctance | 6, 7, 8, 10, 12, 14 |
| 4. Magnetic energy and energy density | 7, 9, 12 |
| 5. Transformers, wireless power, practical inductors | 10, 11, 16 |
