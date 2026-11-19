# Problems 10-07 · BJT Single-Stage Amplifiers

Chapter: [10-07](../chapters/10-07-bjt-single-stage-amplifiers.md) · Worked solutions: [10-07 solutions](../solutions/10-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** hybrid-π model with $g_m = I_C/V_T$, $r_\pi = \beta/g_m$, $r_e = \alpha/g_m$, $r_o = V_A/I_C$, $V_T$ = 25.852 mV; $r_o$ ignored unless $V_A$ is given; capacitors are short circuits at signal frequencies; bias currents are set by ideal sources unless a network is given.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 10-07.1 [A]

**Reflection.** A BJT at $I_C$ = 1 mA has β = 120. (a) Find $r_\pi$ and the resistance looking into the base with 220 Ω in the emitter. (b) Find $r_e$ and the resistance looking into the emitter with 12 kΩ in the base.

### Problem 10-07.2 [A]

**The gain budget.** A CE stage drops 2 V across $R_C$. (a) Find its gain magnitude at 1 mA and at 0.2 mA. (b) What would a MOSFET at $V_{ov}$ = 0.2 V give for the same 2 V?

### Problem 10-07.3 [A]

**An emitter follower.** At $I_C$ = 2 mA with β = 150 and an emitter resistance of 500 Ω (no other load), driven directly from an ideal source: find $r_e$, the gain, the input resistance and the output resistance.

### Problem 10-07.4 [B]

**Designing a degenerated stage.** A CE stage at $I_C$ = 2 mA (β = 100) has $R_C$ = 2.2 kΩ and a bias network with $R_B$ = 10 kΩ. (a) Find the unbypassed $R_{E1}$ for a gain of −10 from the base. (b) Find the input resistance at the base and of the stage.

### Problem 10-07.5 [B]

**Output resistance and its ceiling.** At $I_C$ = 0.5 mA, β = 200 and $V_A$ = 80 V, with the base grounded for signals: (a) find $g_m$, $r_\pi$ and $r_o$; (b) find the collector output resistance with $R_E$ = 2 kΩ; (c) find the ceiling as $R_E \to \infty$.

### Problem 10-07.6 [B]

**Common base from a resistive source.** A CB stage at $I_C$ = 0.25 mA (β = 100) with $R_C$ = 20 kΩ is driven from a 1 kΩ source. Find $R_{in}$, the gain from the emitter, the input factor and the overall gain. What does the result say about where CB stages belong?

### Problem 10-07.7 [B]

**A follower driven from a high resistance.** An emitter follower at 1 mA (β = 100) is driven from a 100 kΩ source. Find its output resistance (ignore $R_E$) and compare with $r_e$.

### Problem 10-07.8 [B]

**A BJT input on a 1 MΩ sensor.** A sensor with 1 MΩ source resistance drives (a) a bypassed CE stage at 1 mA (β = 100) and (b) the same stage at 10 µA. For each find $r_\pi$, the input factor, and the DC offset produced by the base current flowing through the sensor resistance. (c) What does a MOSFET input give?

### Problem 10-07.9 [C]

**Output resistance with a source resistance.** Derive $R_{out,C} = r_o[1 + g_mR_E'r_\pi/(r_\pi + R_{sig})] + R_E'$ with $R_E' = R_E \parallel (r_\pi + R_{sig})$ (as in §3.2), and evaluate it at $I_C$ = 1 mA, β = 100, $V_A$ = 50 V, $R_E$ = 1 kΩ for $R_{sig}$ = 0 and 10 kΩ. Why does the source resistance lower it?

### Problem 10-07.10 [B]

**Follower swing into a coupled load.** An emitter follower is biased at $I_E$ = 1 mA by $R_E$ = 5 kΩ to a negative supply, and drives a 1 kΩ load through a coupling capacitor. (a) Find the largest negative output swing before cutoff. (b) What bias current, with $R_E$ unchanged, allows a 2 V peak? (c) What negative supply does that need, if the emitter sits at −0.7 V?

### Problem 10-07.11 [B]

**β spread at the system level.** Example 10-07.7's stage (440 Ω unbypassed, $R_C$ = 4.7 kΩ, 1 mA) has a bias network $R_B$ = 50 kΩ and is driven from a 10 kΩ source. Find the stage input resistance and the overall gain at β = 100 and β = 300, and repeat for the fully bypassed stage (gain $-g_mR_C$ from the base).

### Problem 10-07.12 [C]

**A follower in front of a CE stage.** A 50 kΩ source drives a CE stage at 1 mA (β = 100, $R_C$ = 5 kΩ, bypassed). (a) Find the overall gain. (b) Insert an emitter follower at 0.1 mA (β = 100, biased by an ideal current source) between the source and the CE base. Find its input resistance, its gain, the input factor and the overall gain.

---

## Objective coverage

| Learning objective (chapter 10-07) | Problems |
|---|---|
| 1. Gain, $R_{in}$, $R_{out}$ of CE, CB, CC | 2, 3, 6, 7 |
| 2. Reflection rules | 1, 3, 7, 12 |
| 3. Degenerated output resistance and its ceiling | 5, 9 |
| 4. Discrete CE design with bias and loading | 4, 11 |
| 5. MOS against BJT | 2, 8 |
| Swing and multistage use | 10, 12 |
