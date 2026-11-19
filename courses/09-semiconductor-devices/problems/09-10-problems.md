# Problems 09-10 · Short-Channel Effects and Leakage

Chapter: [09-10](../chapters/09-10-short-channel-effects-and-leakage.md) · Worked solutions: [09-10 solutions](../solutions/09-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** n-channel devices at 300 K unless stated; $n_i$ = 1.0 × 10¹⁰ cm⁻³, $V_T$ = 25.852 mV, $\varepsilon_s$ = 11.7ε₀, $\varepsilon_{ox}$ = 3.9ε₀, $E_g$ = 1.12 eV. Oxide thicknesses are SiO₂-equivalent; a 2 nm oxide gives $C_{ox}$ = 1.727 µF/cm². Use Hu's velocity-saturation model of chapter §3.1 with $\mathcal E_{sat} = 2v_{sat}/\mu_{ns}$, $v_{sat}$ = 8 × 10⁶ cm/s for electrons and 6 × 10⁶ cm/s for holes. Currents are per micrometer of width where stated. "Numerical" problems expect a short script or the lab notebook.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 09-10.1 [A]

**When is a channel short?** An NMOS has $\mu_{ns}$ = 200 cm²/V·s. Find $\mathcal E_{sat}$, and the channel length at which $\mathcal E_{sat}L$ equals the overdrive for $V_{ov}$ = 0.1, 0.5 and 1.0 V. What do the three lengths say about digital and low-power analog design?

### Problem 09-10.2 [A]

**Linear in overdrive.** In the fully velocity-saturated limit ($\mathcal E_{sat}L \ll V_{ov}$, and neglecting the $m\mathcal E_{sat}L$ term), find $I_{Dsat}$ per micrometer of width for a 2 nm oxide at $V_{ov}$ = 0.4 V and 0.8 V. By what factor does doubling the overdrive raise the current, and what would the square law predict?

### Problem 09-10.3 [B]

**Saturation current against length.** For $C_{ox}$ = 1.727 µF/cm², $\mu_{ns}$ = 183 cm²/V·s, $m$ = 1.2 and $V_{ov}$ = 0.65 V, find $V_{Dsat}$, $I_{Dsat}$ (mA/µm) and its ratio to the long-channel value for $L$ = 1 µm, 200 nm, 50 nm and 20 nm. How much does $I_{Dsat}$ rise from 200 nm to 20 nm, against the tenfold rise the long-channel law promises?

### Problem 09-10.4 [B]

**The PMOS penalty.** A PMOS matches the NMOS of Example 09-10.1 ($L$ = 50 nm, 2 nm oxide, $m$ = 1.2, $|V_{ov}|$ = 0.65 V) but has a hole surface mobility of 61 cm²/V·s, a third of the electron value. Find $\mathcal E_{sat}$, $\mathcal E_{sat}L$, $|V_{Dsat}|$ and $|I_{Dsat}|$, and the ratio of the PMOS to the NMOS current (0.4968 mA/µm). Why is the ratio much closer to one half than to one third?

### Problem 09-10.5 [B]

**Velocity saturation in the linear region.** For the transistor of Problem 09-10.3 at $L$ = 50 nm, find $I_D$ at $V_{DS}$ = 50 mV and 100 mV with and without velocity saturation, the reduction factor $1 + V_{DS}/\mathcal E_{sat}L$ and the channel resistance $V_{DS}/I_D$ (Ω·µm) with velocity saturation.

### Problem 09-10.6 [B]

**A series-resistance budget.** For the transistor of Example 09-10.1 ($I_{Dsat0}$ = 0.4968 mA/µm at $V_{ov}$ = 0.65 V), what source resistance (Ω·µm) would cost 20% of the saturation current (a) according to Hu's closed form, and (b) self-consistently with the full velocity-saturation model? Why does (b) give a smaller tolerable resistance?

### Problem 09-10.7 [B]

**Extracting R_ds and ΔL.** Three test transistors of width 10 µm differ only in drawn length. At small $V_{DS}$ the measured $V_{DS}/I_D$ is:

| $L_{drawn}$ (µm) | $V_{ov}$ = 1 V | $V_{ov}$ = 2 V |
|---|---|---|
| 0.5 | 265.8 Ω | 207.9 Ω |
| 1.0 | 410.6 Ω | 280.3 Ω |

Using $V_{DS}/I_D = R_{ds} + (L_{drawn} - \Delta L)/(WC_{ox}\mu_{ns}V_{ov})$, find the two slopes, $\Delta L$, $R_{ds}$ and $\mu_{ns}C_{ox}$.

### Problem 09-10.8 [B]

**Measuring the characteristic length.** A technology shows DIBL of 20 mV/V at $L$ = 40 nm and 90 mV/V at $L$ = 25 nm. In Hu's model the DIBL equals the coupling ratio $C_d/C_{ox}$, which falls as $e^{-L/l_d}$; because the model is semi-quantitative, allow a prefactor: DIBL $= Ae^{-L/l_d}$. Find $l_d$ and $A$, the threshold roll-off at $V_{DS}$ = 50 mV and at 1.0 V for $L$ = 25 nm, and the length at which DIBL equals 50 mV/V.

### Problem 09-10.9 [B]

**Vertical scaling.** (a) If $T_{ox}$, $W_{dep}$ and $X_j$ all shrink by 0.7, by what factor does $l_d$ shrink? (b) If only the oxide shrinks by 0.7? (c) A new node needs $l_d$ to shrink by 0.7, but gate leakage limits the oxide to a 0.9 reduction. By what factor must the product $W_{dep}X_j$ shrink, and each of the two if they shrink equally?

### Problem 09-10.10 [B]

**A multi-threshold library.** A library offers low, standard and high thresholds of 0.20, 0.27 and 0.34 V, with $S$ = 75 mV/decade at $V_{DD}$ = 0.7 V. Taking the on-current proportional to $V_{DD} - V_t$ (velocity-saturated), find each flavor's off-current and on-current relative to the low-$V_t$ device. If 5% of a block's transistors use low $V_t$ and the rest high $V_t$, what is the block's leakage relative to an all-low-$V_t$ design?

### Problem 09-10.11 [B]

**DIBL and the hot corner.** A transistor has a linear-region threshold of 0.30 V (measured at $V_{DS}$ = 50 mV), DIBL of 60 mV/V and $S$ = 75 mV/decade at 300 K, and runs at $V_{DD}$ = 0.75 V. (a) Find the saturation threshold at $V_{DD}$ and the factor by which DIBL raises the off-current. (b) At 85 °C the swing scales with absolute temperature and the threshold falls by 0.8 mV/K. Find the swing and saturation threshold at 85 °C. (c) Find the off-current at 85 °C relative to the 300 K value at $V_{DD}$, and relative to a naive estimate using the room-temperature linear threshold. Keep the current-defined threshold convention.

### Problem 09-10.12 [B]

**GIDL and oxide thickness.** For an n⁺-polysilicon gate over an n⁺ drain, find the largest drain-to-gate voltage that keeps the silicon surface field below 0.5 MV/cm for 1.5 nm and 3 nm oxides. Then find the surface field at $V_{DG}$ = 1.8 V (an I/O supply) for each. Which oxide would you use for I/O transistors, and why?

### Problem 09-10.13 [B]

**A leakage budget.** A chip has 10⁹ transistors at $V_{DD}$ = 0.75 V. At 25 °C each leaks 1 nA subthreshold (on average) and has a gate area of 100 nm × 20 nm with a gate tunneling density of 10 A/cm²; junction leakage is negligible. (a) Find the gate leakage per transistor, the chip's subthreshold and gate leakage currents and the total leakage power. (b) At 85 °C subthreshold leakage rises tenfold and gate leakage by 20%. Find the hot leakage power and the subthreshold share. Which mechanism would you attack first?

### Problem 09-10.14 [C]

**Doping and dopant fluctuation (numerical).** A planar NMOS has $W = L$ = 40 nm and a 1.5 nm oxide, with uniform doping and $W_{dep}$ set by the threshold condition ($\phi_s = 2\phi_B$). (a) At $N_A$ = 10¹⁸ cm⁻³, find $\phi_B$, $W_{dep}$, the mean dopant count and the depth-weighted $\sigma_{V_t}$. (b) Find the matching coefficient $A_{V_t} = \sigma_{V_t}\sqrt{WL}$ (mV·µm). (c) Find the doping at which $\sigma_{V_t}$ reaches 30 mV, and the mean dopant count there.

### Problem 09-10.15 [C]

**Choosing the minimum length.** A technology has $l_d$ = 8 nm, $V_{DD}$ = 0.7 V and $S$ = 75 mV/decade. (a) Find the minimum length at which the roll-off at $V_{DD}$ (Hu's model) raises the off-current by no more than 10×, and express it in units of $l_d$. (b) If manufacturing variation makes a device 10% shorter than this minimum, find its roll-off, the extra factor of off-current relative to a device at the minimum, and the total factor relative to a long-channel device.

---

## Objective coverage

| Learning objective (chapter 09-10) | Problems |
|---|---|
| 1. Velocity saturation and the injection limit | 1, 2, 3, 4, 5 |
| 2. Parasitic source/drain resistance | 6, 7 |
| 3. Threshold roll-off and DIBL | 8, 9, 11, 15 |
| 4. Swing limit and the I_on–I_off trade-off | 10, 11 |
| 5. GIDL and the leakage budget | 12, 13 |
| 6. Random dopant fluctuation | 14 |
