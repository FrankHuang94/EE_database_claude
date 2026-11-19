# Problems 09-02 · Carriers, Doping and the Fermi Level

Chapter: [09-02](../chapters/09-02-carriers-doping-fermi-level.md) · Worked solutions: [09-02 solutions](../solutions/09-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** silicon at 300 K with the course values $E_g$ = 1.12 eV, $N_C$ = 3.2 × 10¹⁹ cm⁻³, $N_V$ = 1.8 × 10¹⁹ cm⁻³, $n_i$ = 1.0 × 10¹⁰ cm⁻³ and $kT$ = 25.85 meV. Assume complete ionization and non-degenerate (Boltzmann) statistics unless a problem says otherwise. For other temperatures, use $N_C, N_V \propto T^{3/2}$ and the course model of $n_i(T)$ (chapter §3.8, with Varshni's fit $E_g(T) = 1.17 - 4.73\times10^{-4}T^2/(T + 636)$ eV). Donor level of phosphorus: 45 meV below $E_C$; acceptor levels: boron 45 meV and indium 157 meV above $E_V$; degeneracy factors $g_D$ = 2, $g_A$ = 4.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 09-02.1 [A]

**Effective densities of states.** (a) Compute $N_C$ for GaAs at 300 K with the band-edge mass 0.067 $m_0$ and with the room-temperature mass 0.063 $m_0$, and compare with Hu's tabulated 4.7 × 10¹⁷ cm⁻³. (b) Find silicon's $N_C$ at 77 K and at 400 K.

### Problem 09-02.2 [A]

**Reading the Fermi function.** (a) Find the probability that a state is occupied at $kT$, $3kT$ and $10kT$ above $E_F$. (b) By what fraction does the Boltzmann factor $e^{-(E - E_F)/kT}$ overstate each? (c) What is the probability that a state 0.10 eV *below* $E_F$ is empty at 300 K?

### Problem 09-02.3 [A]

**An n-type wafer.** Silicon is doped with $N_D$ = 5 × 10¹⁵ cm⁻³. Find $n$, $p$, $E_F - E_i$ and $E_C - E_F$.

### Problem 09-02.4 [A]

**From the Fermi level back to doping.** In a p-type silicon sample, $E_F$ lies 0.20 eV above $E_V$. Find $p$, $n$, the acceptor concentration, and $E_i - E_F$.

### Problem 09-02.5 [B]

**Counter-doping.** A p-type region with $N_A$ = 3 × 10¹⁶ cm⁻³ is implanted with $N_D$ = 5 × 10¹⁶ cm⁻³ phosphorus. (a) What type is it now? (b) Find $n$, $p$ and $E_F - E_i$. (c) What total density of ionized impurities scatters the carriers, and why does that matter?

### Problem 09-02.6 [B]

**Intrinsic silicon off room temperature.** Using the course model, find $E_g$ and $n_i$ at 250 K and at 350 K, and the ratio of the two values of $n_i$.

### Problem 09-02.7 [B]

**When the law of mass action fails.** An n-type sample in the dark has $n$ = 2.0 × 10¹⁵ cm⁻³. (a) What is $p$? (b) Under steady illumination, $n$ rises to 2.1 × 10¹⁵ and $p$ to 1.0 × 10¹⁴ cm⁻³. Compute $np/n_i^2$. (c) Explain why this does not contradict the chapter, and what replaces the single Fermi level.

### Problem 09-02.8 [B]

**Donors in GaAs.** Use the hydrogen model for a donor in GaAs ($m^*$ = 0.067 $m_0$, $\varepsilon_r$ = 12.9). (a) Find the ionization energy and the orbit radius. (b) At what concentration do the orbits touch? (c) Why do GaAs donors stay ionized to much lower temperatures than silicon donors of the same concentration, and why are lightly doped GaAs samples already near the impurity-band regime?

### Problem 09-02.9 [B]

**Shallow and deep acceptors.** Silicon is doped with 10¹⁶ cm⁻³ of (a) boron and (b) indium. For each, find the hole density and the ionized fraction at 300 K, ignoring electrons. (Write $N_A^- = p$ and derive the quadratic as in chapter §3.6, with $g_A$ = 4.) (c) Why is indium rarely used as a dopant in silicon devices?

### Problem 09-02.10 [B]

**Hot silicon.** At 600 K: (a) by how much has $E_i$ moved from mid-gap, if $N_V/N_C$ keeps its 300 K value? (b) Find $n_i$ with the course model. (c) For $N_D$ = 10¹⁵ cm⁻³, find $n$, $p$ and $E_F - E_i$. Is the region still usefully n-type?

### Problem 09-02.11 [B]

**How fast leakage grows with temperature.** Using the course model: (a) find $n_i/n_i(300\ \text{K})$ and $n_i^2/n_i^2(300\ \text{K})$ at 310 K, 350 K and 400 K; (b) find the temperature rise above 300 K that doubles $n_i$, and the rise that doubles $n_i^2$. (c) A junction's diffusion leakage scales with $n_i^2$. How should a reliability engineer read a datasheet that quotes leakage only at 25 °C?

### Problem 09-02.12 [C]

**Degenerate p-type silicon.** Silicon is doped with $N_A$ = 10¹⁹ cm⁻³ boron, assumed fully ionized. (a) Find $E_F - E_V$ with Boltzmann statistics. (b) Solve $p = N_V\mathcal F_{1/2}(\eta)$, with $\eta = (E_V - E_F)/kT$, numerically, and compare with the two-term approximation $\eta \approx \ln r + r/\sqrt8$. (c) Which way, and by how much, does Boltzmann statistics misplace $E_F$?

### Problem 09-02.13 [C]

**Doping for a hot environment.** An n-type region must keep $n_i$ below one tenth of its doping, so that the carrier density stays within 1% of $N_D$. Find the minimum $N_D$ that meets this at (a) 423 K (150 °C) and (b) 473 K (200 °C). (c) Why do power devices, whose drift regions must be lightly doped to block high voltages, run into this limit first?

### Problem 09-02.14 [C]

**Counting dopants in a transistor.** Dopant atoms land independently at random, so the number in a volume $V$ at average concentration $N$ is a Poisson random variable with mean $NV$ (03-02). (a) A planar transistor's depletion region under the gate is 30 nm × 30 nm × 10 nm and doped at 10¹⁸ cm⁻³. Find the mean number of dopants, its standard deviation and the relative spread. (b) A fin 7 nm wide, 40 nm high and 20 nm long is lightly doped at 10¹⁷ cm⁻³. Find the mean number of dopants, the probability of finding none, and the probability of two or more. (c) What doping would reduce the relative spread in (a) to 10%? (d) Explain why modern multigate transistors use lightly doped channels.

### Problem 09-02.15 [C]

**Compensation and freeze-out.** At 77 K, compare silicon with $N_D$ = 10¹⁶ cm⁻³ phosphorus alone and the same silicon with an added $N_A$ = 10¹⁵ cm⁻³ boron. (a) Explain why the acceptors are fully ionized in the compensated sample. (b) Write charge neutrality for the compensated sample and solve it numerically for $n$, $E_C - E_F$ and the fraction of donors ionized. (c) Compare with the uncompensated $n$ (Example 09-02.5) and explain both differences.

---

## Objective coverage

| Learning objective (chapter 09-02) | Problems |
|---|---|
| 1. Density of states, $N_C$ and $N_V$ | 1 |
| 2. Fermi–Dirac and Boltzmann statistics; degeneracy | 2, 12 |
| 3. Intrinsic concentration, $E_i$, law of mass action | 6, 7, 10, 11 |
| 4. Donors and acceptors; doped, compensated and partly ionized material | 3, 4, 5, 8, 9, 14, 15 |
| 5. Temperature dependence and its limits | 10, 11, 13, 15 |
