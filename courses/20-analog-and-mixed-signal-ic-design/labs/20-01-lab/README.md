# Lab 20-01 · Transconductance Efficiency, Speed and Gain

Chapter: [20-01 · Analog Design Fundamentals in Nanometer CMOS](../../chapters/20-01-analog-design-fundamentals-gm-id.md)

## Objective

- Plot $g_m/I_D$ against the inversion coefficient from weak to strong inversion, and see where the square law fails.
- Build a $g_m/I_D$ "design chart" (current density, $f_T$ and intrinsic gain against $g_m/I_D$) for three channel lengths, and use it to size a transistor.
- Find where $(g_m/I_D)\cdot f_T$ peaks for each length, and explain why the peak moves.
- See how current bias protects $g_m$ from threshold corners, and how temperature still moves it.
- Measure a transistor's intrinsic gain in ngspice and match it to $(g_m/I_D)\,V_A$.

## Background

The chapter's model (§3.2–3.4) describes a saturated MOSFET by its normalized source charge $q$, with $V_P/V_T = 2q + \ln q$, $I_D = I_{spec}(q^2 + q)/(1 + \lambda_cq)$ and $I_{spec} = 2n\mu C_{ox}(W/L)V_T^2$. The inversion coefficient $IC = I_D/I_{spec}$ sets $g_m/I_D$, which is at most $1/(nV_T)$; $f_T = 3\mu V_T\Delta/(2\pi L^2)$ with $\Delta$ the normalized transconductance (§3.5); and the intrinsic gain is $(g_m/I_D)V_A'L$ (§3.6). All quantities are per unit width except the width itself, which is sized last (§3.9).

Files:

- `gmid.py`: the model for the illustrative T130 process (`Process`), with `gm_over_id`, `vov_of_ic`, `ft`, `id_per_w`, `intrinsic_gain`, `ic_for_gm_over_id`, `size_for_gm` and `drain_current`.
- `gain.cir`: a level-1 NMOS carrying 20 µA from an ideal current source, self-biased through 1 GΩ, with its 1 kHz gain measured for two values of `LAMBDA`.
- `20-01-gmid-lab.ipynb`: the procedure below.

## Procedure

1. **Efficiency.** Predict $g_m/I_D$ at $IC$ = 0.01, 1 and 100, and the square law's answer at the same overdrive. Plot both against $IC$ from $10^{-3}$ to $10^3$, with and without velocity saturation at 0.15 µm (Part 1).
2. **The design chart.** For $L$ = 0.15, 0.5 and 1 µm, plot current density, $f_T$ and intrinsic gain against $g_m/I_D$ from 3 to 28 S/A. Predict which curves move with $L$ and which do not. Re-size Example 20-01.2 from the table (Part 2).
3. **The sweet spot.** Predict whether the peak of $(g_m/I_D)\,f_T$ moves to weaker or stronger inversion as $L$ grows; find it for the three lengths (Part 3).
4. **Corners and temperature.** For Example 20-01.1's transistor, plot the current against a threshold shift from −80 to +80 mV with the gate voltage fixed, and $g_m$ against temperature from −40 to 125 °C with the current fixed (Part 4).
5. **Intrinsic gain in SPICE.** Predict the gain of `gain.cir` for each `LAMBDA` from $g_m/I_D$ and $V_A = (1 + \lambda V_{DS})/\lambda$; run `ngspice -b gain.cir` (Part 5).

## Expected results

- Part 1: $g_m/I_D$ = 29.46, 18.39 and 2.83 S/A at $IC$ = 0.01, 1 and 100 (long channel); at 0.15 µm velocity saturation lowers the last to 1.48 S/A. The square law exceeds the weak-inversion limit of 29.8 S/A for every overdrive below 67 mV.
- Part 2: current density and $f_T$ fall with $L$ at fixed $g_m/I_D$, while $g_m/I_D$ itself depends on $L$ only through velocity saturation; intrinsic gain grows in proportion to $L$. The table re-creates Example 20-01.2's 43.8 µm.
- Part 3: the peak lies at $IC$ = 6.86 for 0.15 µm, **22.6** for 0.5 µm and **44.9** for 1 µm ($g_m/I_D$ = 8.00, **5.12** and **3.84** S/A): it moves into strong inversion as velocity saturation weakens.
- Part 4: ±50 mV of threshold changes the current by ×0.430 and ×1.92 with the gate voltage fixed; with the current fixed, $g_m$ falls from 362.6 µS at −40 °C to **234.2** µS at 125 °C.
- Part 5: ngspice measures gains of **154.0** and **295.1**; the level-1 device runs at $g_m/I_D$ = **14.55** S/A with $V_A$ = **10.59** V, and halving `LAMBDA` almost doubles the gain.

## Discussion

1. Why does the square law's $g_m/I_D = 2/V_{ov}$ exceed the physical limit at small overdrive, and what does the charge-based model do differently?
2. Why do the curves of the design chart not depend on the width?
3. Why does the sweet spot move into stronger inversion for longer channels?
4. The level-1 model has no weak inversion. Which of this lab's conclusions would change if `gain.cir` biased the transistor at 1 µA instead of 20 µA?

**Answers.**

1. The square law keeps only drift current, which vanishes at zero overdrive, so $2/V_{ov}$ grows without bound. In weak inversion the current is diffusion, exponential in $V_{GS}$, and $g_m/I_D$ saturates at $1/(nV_T)$; the model's $2q + \ln q$ relation contains both mechanisms and joins them smoothly (§3.2–3.3).
2. At fixed length, $g_m$, $I_D$ and $C_{gg}$ are all proportional to $W$, so their ratios ($g_m/I_D$, $I_D/W$, $f_T$, $g_m/g_{ds}$) are functions of the inversion level alone. One simulation per length therefore sizes every width (§3.3).
3. The peak exists only because velocity saturation flattens $f_T$ while $g_m/I_D$ keeps falling. A longer channel saturates at a higher inversion coefficient ($\lambda_c \propto 1/L$), so the flattening, and with it the peak, moves to higher $IC$ (§3.8).
4. At 1 µA the 10 µm/1 µm transistor sits at $IC$ ≈ **0.19**, at the weak-inversion edge of moderate inversion, where the charge-based model gives $g_m/I_D$ ≈ **25.5** S/A. The level-1 model has no weak inversion and would still report the square law's $2/V_{ov}$ at a **31** mV overdrive, about **65** S/A, more than twice the physical value and above the 29.8 S/A limit, overstating the gain in proportion. The intrinsic-gain relation $(g_m/I_D)V_A$ still holds, but the $g_m/I_D$ that goes into it must come from a model that includes weak inversion.

## Optional hardware

A CD4007 or ALD1106 MOSFET array lets you measure $g_m/I_D$ directly: force a drain current with a source-measure unit or an op-amp current source, step it by a few percent, and record the change in $V_{GS}$ ($g_m/I_D = \Delta\ln I_D/\Delta V_{GS}$). Sweep the current over four decades to see the weak-inversion plateau near $1/(nV_T)$ and the fall in strong inversion, then warm the package with a hair dryer and repeat a weak-inversion point to see the $1/T$ dependence.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 20-01.a | ngspice gain, LAMBDA = 0.1 | 154.0 | — |
| Lab 20-01.b | ngspice gain, LAMBDA = 0.05 | 295.1 | — |
| Lab 20-01.c | level-1 g_m/I_D, LAMBDA = 0.1 | 14.55 | S/A |
| Lab 20-01.d | level-1 Early voltage, LAMBDA = 0.1 | 10.59 | V |
| Lab 20-01.e | g_m/I_D at IC = 0.01 | 29.46 | S/A |
| Lab 20-01.f | g_m/I_D at IC = 1 | 18.39 | S/A |
| Lab 20-01.g | g_m/I_D at IC = 100, long channel | 2.83 | S/A |
| Lab 20-01.h | g_m/I_D at IC = 100, 0.15 um | 1.48 | S/A |
| Lab 20-01.i | overdrive below which the square law exceeds the limit | 67 | mV |
| Lab 20-01.j | sweet-spot IC at 0.5 um | 22.6 | — |
| Lab 20-01.k | sweet-spot IC at 1 um | 44.9 | — |
| Lab 20-01.l | sweet-spot g_m/I_D at 0.5 um | 5.12 | S/A |
| Lab 20-01.m | sweet-spot g_m/I_D at 1 um | 3.84 | S/A |
| Lab 20-01.n | g_m at 125 C | 234.2 | µS |
| Lab 20-01.o | IC of the lab transistor at 1 uA | 0.19 | — |
| Lab 20-01.p | model g_m/I_D at 1 uA | 25.5 | S/A |
| Lab 20-01.q | level-1 2/V_ov at 1 uA | 65 | S/A |
| Lab 20-01.r | level-1 overdrive at 1 uA | 31 | mV |
