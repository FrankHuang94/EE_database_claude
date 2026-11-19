# Problems 09-04 · Generation, Recombination and the Continuity Equation

Chapter: [09-04](../chapters/09-04-generation-recombination-continuity.md) · Worked solutions: [09-04 solutions](../solutions/09-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** silicon at 300 K, $n_i$ = 1.0 × 10¹⁰ cm⁻³, $kT$ = 25.85 meV; thermal velocities 2.3 × 10⁷ (electrons) and 1.65 × 10⁷ cm/s (holes); $B$ = 1.1 × 10⁻¹⁴ cm³/s; $C_n$ = 1.1 × 10⁻³⁰ and $C_p$ = 0.3 × 10⁻³⁰ cm⁶/s; mobilities from the course model of 09-03 at the total impurity concentration; complete ionization and low-level injection unless stated. "Mid-gap" means $E_t = E_i$.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 09-04.1 [A]

**Lifetimes in p-type silicon.** p-type silicon with $N_A$ = 10¹⁶ cm⁻³ contains 5 × 10¹¹ cm⁻³ mid-gap traps with electron cross section 10⁻¹⁵ cm². Find the minority-electron lifetime limited by (a) SRH, (b) radiative and (c) Auger recombination (hole-assisted, $C_pp_0^2$), and (d) the combined lifetime.

### Problem 09-04.2 [A]

**Is it low-level?** n-type silicon with $N_D$ = 5 × 10¹⁵ cm⁻³ carries an excess $\Delta p = \Delta n$ = 10¹³ cm⁻³. (a) By how much does $E_{Fn}$ move? (b) By what factor does the hole density rise? (c) With $\tau_p$ = 2 µs, what is the net recombination rate?

### Problem 09-04.3 [A]

**Too much light.** n-type silicon with $N_D$ = 10¹⁵ cm⁻³ and $\tau_p$ = 2 µs is illuminated with $G_L$ = 5 × 10²⁰ cm⁻³ s⁻¹. (a) What steady excess does $\Delta p = G_L\tau_p$ predict? (b) Is the low-level assumption valid, and what changes if it is not?

### Problem 09-04.4 [B]

**A trap off mid-gap.** Traps with $\tau_{n0} = \tau_{p0}$ = 1 µs sit 0.25 eV above $E_i$. Using the full SRH formula, find the low-injection lifetime in n-type silicon with (a) $N_D$ = 10¹⁵ and (b) $N_D$ = 10¹⁴ cm⁻³. (c) Explain why the lifetime depends on doping here but not for a mid-gap trap.

### Problem 09-04.5 [B]

**Leakage of a large diode.** A diode of area 1 mm² has a 2 µm depletion region with mid-gap traps and $\tau_0$ = 10 µs. Find its generation current and current density at 300 K.

### Problem 09-04.6 [B]

**Quasi-Fermi levels in p-type silicon.** p-type silicon with $N_A$ = 10¹⁷ cm⁻³ carries $\Delta n = \Delta p$ = 10¹⁵ cm⁻³. Find (a) the shift of $E_{Fp}$, (b) $E_{Fn} - E_i$, (c) the splitting, and (d) $E_i - E_F$ in the dark.

### Problem 09-04.7 [B]

**Switching the light on.** n-type silicon with $\tau_p$ = 5 µs is uniformly illuminated from $t = 0$ with $G_L$ = 10²⁰ cm⁻³ s⁻¹. (a) Solve the continuity equation for $\Delta p(t)$. (b) Find the final excess and the time to reach 90% of it.

### Problem 09-04.8 [B]

**A long-base diode.** Electrons are held at $\Delta n(0)$ = 10¹³ cm⁻³ at the edge of a long p-type region with $N_A$ = 10¹⁶ cm⁻³ and $\tau_n$ = 10 µs. Find $\mu_n$, $D_n$, $L_n$ and the electron current density entering the region.

### Problem 09-04.9 [B]

**A thin base.** A p-type base 0.5 µm thick, doped at 10¹⁷ cm⁻³, has $\tau_n$ = 0.1 µs. Find (a) $D_n$ and $L_n$, (b) $L_n/W$, (c) the fraction of injected electrons that recombine in the base, and (d) the diffusion transit time $W^2/2D_n$.

### Problem 09-04.10 [C]

**Light and a recombining surface.** A thick n-type region ($N_D$ = 10¹⁵ cm⁻³, $\tau_p$ = 1 µs) is uniformly illuminated with $G_L$ = 10¹⁹ cm⁻³ s⁻¹; its surface at $x = 0$ has recombination velocity $S$. (a) Show that $\Delta p(x) = G_L\tau_p[1 - Ae^{-x/L_p}]$ with $A = S/(S + D_p/L_p)$. (b) Evaluate $D_p/L_p$, $A$ and $\Delta p(0)/(G_L\tau_p)$ for $S$ = 10⁴ cm/s and for $S$ = 10 cm/s. (c) What does this say about passivating the front of a solar cell?

### Problem 09-04.11 [C]

**What a lifetime tester measures.** A 300 µm wafer with bulk lifetime 1 ms has both surfaces passivated to $S$ = 10 cm/s. (a) Estimate the effective lifetime with $1/\tau_{\text{eff}} = 1/\tau_b + 2S/W$. (b) Check the condition $SW/2D_p \ll 1$ that justifies the formula (use $D_p$ at 10¹⁵ cm⁻³). (c) Why must lifetime testers passivate samples?

### Problem 09-04.12 [C]

**An Auger-limited emitter.** An n⁺ emitter is doped at 10²⁰ cm⁻³. (a) Find the Auger-limited hole lifetime. (b) Find $D_p$ (hole mobility at 10²⁰ cm⁻³) and the diffusion length. (c) Compare with an emitter depth of 0.2 µm: is the emitter "long" or "short" for holes?

### Problem 09-04.13 [B]

**Designing a fast diode.** A power diode's n-type drift region needs a minority-hole lifetime of 50 ns, set by the gold acceptor level ($\sigma_p$ = 9.0 × 10⁻¹⁵ cm²). What gold concentration is needed?

### Problem 09-04.14 [C]

**When does diffusion leakage take over?** At 300 K a junction's generation leakage is 100 times its diffusion leakage. Generation scales with $n_i$ and diffusion with $n_i^2$. Using the course $n_i(T)$ model, find the temperature at which they are equal.

### Problem 09-04.15 [B]

**Light from GaAs.** n-type GaAs with $n_0$ = 10¹⁷ cm⁻³ has $B$ = 7 × 10⁻¹⁰ cm³/s and an SRH lifetime of 10 ns. Find (a) the radiative lifetime, (b) the combined lifetime and (c) the internal radiative efficiency, the fraction of recombination events that emit light.

---

## Objective coverage

| Learning objective (chapter 09-04) | Problems |
|---|---|
| 1. Radiative, SRH and Auger rates and lifetimes | 1, 12, 15 |
| 2. SRH statistics and trap position | 4, 13 |
| 3. Low-level lifetimes; generation in depleted regions | 2, 3, 5, 14 |
| 4. Quasi-Fermi levels | 2, 6 |
| 5. Continuity and minority-carrier diffusion equations | 7, 8, 9, 10, 11 |
