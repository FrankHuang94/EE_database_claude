# Problems 09-03 · Carrier Transport: Drift and Diffusion

Chapter: [09-03](../chapters/09-03-drift-and-diffusion.md) · Worked solutions: [09-03 solutions](../solutions/09-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** silicon at 300 K, $kT/q$ = 25.85 mV, complete ionization. Use the course mobility model of chapter §3.3 ($\mu_n = 92 + 1268/[1 + (N/1.3\times10^{17})^{0.91}]$, $\mu_p = 48 + 402/[1 + (N/6.3\times10^{16})^{0.76}]$ cm²/V·s, with $N$ the total ionized impurity concentration), the lattice mobility $\mu_{L,n} = 1430(300/T)^{2.2}$ cm²/V·s, and the velocity–field fits of §3.5. Conductivity masses: 0.26 $m_0$ (electrons), 0.39 $m_0$ (holes).

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 09-03.1 [A]

**Holes on the move.** For p-type silicon with $N_A$ = 10¹⁶ cm⁻³, find (a) the hole mobility, (b) the mean free time, (c) the drift velocity at 500 V/cm, and (d) the mean free path, using the thermal velocity $\sqrt{3kT/m^*}$ and the hole conductivity mass $m^*$ = 0.39 $m_0$.

### Problem 09-03.2 [A]

**Matthiessen's rule.** (a) A sample's lattice-limited mobility is 1430 cm²/V·s and its impurity-limited mobility is 3000 cm²/V·s. What is its mobility? (b) What impurity-limited mobility would bring the total down to 1000 cm²/V·s?

### Problem 09-03.3 [A]

**From resistivity to doping.** Wafers are specified by resistivity. Find the doping of (a) an n-type and (b) a p-type wafer of 10 Ω·cm, solving $\rho = 1/(qN\mu(N))$ numerically, and the mobility in each.

### Problem 09-03.4 [A]

**The cost of compensation.** Silicon contains $N_D$ = 2 × 10¹⁷ and $N_A$ = 10¹⁷ cm⁻³. (a) Find $n$, the electron mobility and the resistivity. (b) Compare with silicon doped only with 10¹⁷ cm⁻³ donors.

### Problem 09-03.5 [B]

**Designing a resistor.** A diffused layer has $R_s$ = 200 Ω/□. (a) How many squares, and what length at 2 µm width, give 50 kΩ (ignore contacts)? (b) What does a four-point probe read on this layer with 1 mA?

### Problem 09-03.6 [B]

**A layered film.** An n-type film has a 0.2 µm top layer doped at 10¹⁹ cm⁻³ over a 0.8 µm layer doped at 10¹⁷ cm⁻³. (a) Find the sheet resistance of the stack. (b) Which layer carries most of the current, and what fraction? (c) Find the sheet resistance of each layer alone.

### Problem 09-03.7 [B]

**Holes at high field.** (a) Using the hole velocity–field fit at 300 K, find the hole drift velocity at 10⁴, 10⁵ and 2 × 10⁵ V/cm. (b) Estimate the time for holes to cross a 50 nm channel with 1 V across it, assuming a uniform field, and compare with electrons.

### Problem 09-03.8 [B]

**Diffusion of holes.** (a) Find $D_p$ in silicon doped with 10¹⁷ cm⁻³ donors (holes are minority carriers; use the hole mobility at that total impurity concentration). (b) How far do holes diffuse, $\sqrt{D_pt}$, in 100 ns? (c) What is $kT/q$ at 400 K, and how does the Einstein ratio change?

### Problem 09-03.9 [B]

**Diffusion from a profile.** An electron density decays as $n(x) = 10^{15}e^{-x/L}$ cm⁻³ with $L$ = 10 µm in lightly doped silicon. (a) Find the electron diffusion current density at $x = 0$ and at $x = 2L$. (b) In which direction does the current flow?

### Problem 09-03.10 [B]

**A built-in field from a linear grade.** n-type silicon's donor concentration falls linearly from 10¹⁷ cm⁻³ at $x = 0$ to 10¹⁶ cm⁻³ at $x$ = 1 µm. In equilibrium: (a) find the built-in field at $x = 0$, at the midpoint and at $x$ = 1 µm, and its direction; (b) find the electrostatic potential difference across the region.

### Problem 09-03.11 [B]

**Temperature coefficients of resistance.** (a) Show that a resistor whose mobility is lattice-limited, $\mu \propto T^{-2.2}$, has a temperature coefficient $d\ln R/dT = 2.2/T$, and evaluate it at 300 K in ppm/K. (b) For a resistor doped at 10¹⁷ cm⁻³, use Matthiessen's rule with $\mu_I \propto T^{3/2}$ fitted to the course model at 300 K (chapter Example 09-03.4) and find its temperature coefficient at 300 K numerically.

### Problem 09-03.12 [C]

**A zero-temperature-coefficient resistor.** In the model of Problem 09-03.11(b), find (a) the condition on $\mu_I/\mu_L$ for $d\mu/dT = 0$ at 300 K, (b) the resulting mobility, and (c) the doping that gives it in the course model. (d) Why would a real design still need measurement?

### Problem 09-03.13 [C]

**Kinetic theory and Einstein.** In three dimensions, a gas of particles with speed $v_{th}$ and mean free path $\lambda$ has $D = v_{th}\lambda/3$. (a) Evaluate it for electrons in lightly doped silicon (Example 09-03.1). (b) Show algebraically that, with $v_{th} = \sqrt{3kT/m^*}$ and $\lambda = v_{th}\tau$, this reproduces the Einstein relation exactly. (c) Why is the agreement in (a) not a coincidence?

### Problem 09-03.14 [C]

**A Hall measurement.** An n-type silicon bar 0.5 mm thick, doped with 1.0 × 10¹⁵ cm⁻³ phosphorus (from the growth record, fully ionized), carries 1.0 mA in a 0.5 T field and shows a Hall voltage of magnitude 7.05 mV; its resistivity is 4.64 Ω·cm. (a) Find the Hall density $n_H = IB/(qt|V_H|)$ and the Hall coefficient (in cm³/C). (b) Find the Hall mobility. (c) Compare with the course model's drift mobility at the known doping, find the Hall factor $r_H = \mu_H/\mu$, and check that $r_Hn_H$ recovers the doping.

### Problem 09-03.15 [C]

**Sizing a detector's drift region.** A photodiode's depletion region is 5 µm thick, and photogenerated carriers must cross it in 100 ps (a speed of 5 × 10⁶ cm/s). (a) Assuming a uniform field, find the field and voltage that give electrons this average velocity, and likewise for holes. (b) What is the shortest possible crossing time for each carrier? (c) Which carrier sets the required bias?

---

## Objective coverage

| Learning objective (chapter 09-03) | Problems |
|---|---|
| 1. Drift velocity, mobility, mean free time and path | 1, 13 |
| 2. Matthiessen's rule, mobility models, resistivity and sheet resistance | 2, 3, 4, 5, 6, 11, 12, 14 |
| 3. Velocity saturation and transit times | 7, 15 |
| 4. Diffusion and the Einstein relation | 8, 9, 13 |
| 5. Drift and diffusion together; built-in fields | 10 |
