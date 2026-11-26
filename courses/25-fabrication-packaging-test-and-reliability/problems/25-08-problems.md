# Problems 25-08 · Thermal Engineering

Chapter: [25-08](../chapters/25-08-thermal-engineering.md) · Worked solutions: [25-08 solutions](../solutions/25-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Slab $R = t/(kA)$; hotspot centre rise $qa/k$ and average spreading resistance $8/(3\pi^2ka)$; 45° spreading $t/(k\pi a(a + t))$.
- Fin efficiency $\tanh(mL)/mL$ with $m = \sqrt{2h/(kt_f)}$; coolant rise $P/(\rho c_p\dot{V})$.
- Junction $T_J = T_{in} + \Delta T_{fluid}/2 + P\sum R$.
- Air: 1.2 kg/m³, 1,005 J/(kg·K); water: 1,000 kg/m³, 4,180 J/(kg·K); 1 CFM = 4.719 × 10⁻⁴ m³/s.
- Conductivities: silicon 150, copper 400, aluminium 200 W/(m·K) unless stated.
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/25-08-lab/thermal.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 25-08.1 [A]

**A solder TIM.** Replace Example 25-08.1's polymer TIM with a 100 µm indium layer ($k$ = 80 W/(m·K), assumed) over the same 800 mm². Find its resistance and how many times lower it is than the polymer TIM's.

### Problem 25-08.2 [B]

**A bigger hotspot.** (a) Spread Example 25-08.2's 2 W of excess power over a disk 2 mm in diameter. Find the excess flux, the centre rise and the average spreading resistance. (b) Keep instead the original 2.55 W/mm² of excess flux over the 2 mm disk. What excess power is that, and what is the centre rise?

### Problem 25-08.3 [B]

**A small die on a big lid.** *(lab)* A 5 mm radius die sits on Example 25-08.3's lid (3 mm copper, 35 mm radius, ideal cooling below). Find (a) the one-dimensional footprint resistance, (b) the 45° estimate and (c) the exact value from the lab's finite-difference solve. (d) What is the 45° error now?

### Problem 25-08.4 [C]

**The fin.** (a) Derive the fin equation and the efficiency $\tanh(mL)/mL$ for an insulated tip, stating each assumption. (b) Find the efficiency of Example 25-08.4's fin in copper. (c) Find it for an aluminium fin twice as tall (80 mm). What do (b) and (c) teach about fin design?

### Problem 25-08.5 [A]

**Server airflow.** A 2U server dissipates 2.4 kW (assumed), and its exhaust may run 20 K above its inlet. Find the airflow in m³/s and CFM.

### Problem 25-08.6 [B]

**How much power can the plate take?** *(lab)* With Example 25-08.6's 0.035 K/W, 45 °C inlet and a 105 °C limit, find the largest power at (a) 2 L/min and (b) 4 L/min. What limits the power?

### Problem 25-08.7 [B]

**Colder water.** For 2,300 W with 0.035 K/W and 2 L/min, find (a) the junction temperature with a 30 °C inlet, and (b) the inlet temperature needed for 105 °C.

### Problem 25-08.8 [B]

**An AMD rack.** AMD's Helios rack holds 72 MI455X GPUs with a maximum board power of 2,500 W each [R-598]. Find (a) the GPU board power at maximum and (b) the water flow to carry it with a 10 K rise.

### Problem 25-08.9 [A]

**Reading a pod.** Google's Ironwood pod has 9,216 chips, spans "nearly 10 MW", has 192 GB of HBM per chip and 4,614 TFLOPS peak per chip [R-599]. Find (a) the power per chip, (b) the pod's HBM in petabytes and (c) its peak compute in exaflops. What does (a) include that a chip TDP would not?

### Problem 25-08.10 [B]

**Provisioning.** NVIDIA's power-provisioning software reduces provisioned rack power from 125 to 90 kW for GB200 NVL72 and from 136 to 101 kW for Vera Rubin NVL72 [R-601]. (a) What fractional increase in racks does each allow in a fixed power envelope? (b) How many Vera Rubin racks fit in 10 MW of IT power before and after?

### Problem 25-08.11 [C]

**Activation energy.** *(lab)* Repeat Example 25-08.8(b) with activation energies of (a) 1.0 eV and (b) 0.4 eV. Explain the trend.

### Problem 25-08.12 [A]

**Power profiles.** SemiAnalysis reports that Rubin's higher power profile raises rack power 20% for a smaller performance gain [R-597]. If the gain were 10% (assumed), by what percentage would performance per watt change?

### Problem 25-08.13 [B]

**Why heat pipes work.** Water's latent heat of evaporation is about 2.26 MJ/kg. (a) What mass flow of evaporating water carries 100 W? (b) How many times more heat does a kilogram of evaporating water carry than a kilogram warming by 10 K?

### Problem 25-08.14 [B]

**Finer channels.** Repeat Example 25-08.9(a)–(e) with 200 channels 0.15 mm wide, keeping the depth, length and total flow. By what factors do $h$, the ideal-wall resistance and the pressure drop change?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Junction-to-coolant budgets | 1, 6, 7 |
| 2. Hotspots and spreading | 2, 3 |
| 3. Fins and air cooling | 4, 5 |
| 4. Coolant flow and cold plates | 6, 7, 8, 13, 14 |
| 5. Mission profiles and Arrhenius | 11 |
| 6. Reading power and cooling claims | 8, 9, 10, 12 |
