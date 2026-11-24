# Lab 22-05 · Magnetics: Saturation, Leakage, Winding Loss and the Flux-Swing Optimum

Chapter: [22-05 · Magnetics Design](../../chapters/22-05-magnetics-design.md)

## Objective

- Watch a gapped ferrite inductor ramp linearly and then saturate, using a physical B–H curve inside ngspice.
- Measure a transformer's leakage inductance with a short-circuit test, with and without interleaving.
- Map Dowell's AC-resistance factor and find the foil thickness that minimizes a winding's loss.
- Find a transformer's optimum flux swing and see how flat the minimum is.
- Evaluate a powder core's DC-bias roll-off from the vendor's curve fit.

## Background

`magnetics.py` collects the chapter's formulas:

- magnetic circuit: `reluctance`, `gapped_inductance`, `effective_permeability`, `gap_for_inductance`, `fringed_gap_area`;
- energy and saturation: `peak_flux_density`, `gap_energy_fraction`, `max_energy`, `turns_for`;
- core loss: `steinmetz`, `igse_ki`, `igse_triangle`, `eddy_loss_lamination`;
- winding loss: `rho_cu`, `skin_depth`, `winding_resistance`, `dowell_fr`, `dowell_fr_low`;
- design: `area_product`, `kg_required`, `kg_of_core`, `optimum_flux_swing`, `leakage_inductance`, `leakage_interleaved`.

The two netlists:

- `saturation.cir` models Example 22-05.3's flyback core: TDK's ETD 34/17/11 in N87, 32 turns, and the 0.513 mm gap that gives 223 µH in the linear limit. The ferrite follows $B = B_{sat}\tanh(\mu_r\mu_0H/B_{sat}) + \mu_0H$, with $B_{sat}$ = 390 mT (N87 at 100 °C) and $\mu_r$ = 1675 (the ungapped set's effective permeability). An integrator turns the winding voltage into flux linkage. A node solves the B–H curve implicitly for the core's field $H$, and the winding current follows from $Ni = H\ell_e + Bg/\mu_0$. A 100 V step drives it.
- `leakage.cir` builds Example 22-05.8's transformer as coupled inductors, with the leakage split equally between the windings, and runs AC short-circuit tests (layered and interleaved) and an open-circuit test at 100 kHz.

## Procedure

1. **Saturation.** *Predict* the current at the flyback's 5.61 µs on-time, the time at which $B$ reaches 390 mT, and the current 0.4 µs later if the inductance stayed 223 µH. Run `ngspice -b saturation.cir` (Part 1) and plot the current in the notebook.
2. **Leakage.** *Predict* Example 22-05.8's leakage with and without interleaving, then run `ngspice -b leakage.cir` (Part 2).
3. **Winding loss.** *Predict* how $F_R$ grows with $\Delta$ for 1 to 5 layers, and the foil thickness that minimizes Example 22-05.6's four-layer loss. Plot both in the notebook (Part 3).
4. **Flux swing and powder cores.** *Predict* Example 22-05.8's optimum and how much 9 turns cost against it. Then evaluate the 60µ Kool Mµ roll-off at 50 and 100 Oe (Part 4).

## Expected results

- **Part 1.** The current at 5.61 µs is **2.53** A, within 1% of the linear 2.52 A. At 11.5 µs, with $B$ at 95% of $B_{sat}$, it is **5.55** A, only 8% above the linear value. The flux density reaches 390 mT at **12.1** µs; by 12.5 µs the current is **29.2** A against a linear **5.61** A. A gapped ferrite gives almost no warning before it saturates.
- **Part 2.** The short-circuit test gives 0.147 µH layered and 0.0442 µH interleaved, and the open-circuit test 210.7 µH, matching Example 22-05.8.
- **Part 3.** $F_R$ rises roughly as $M^2\Delta^4$ for thin layers; the four-layer loss is smallest at 0.159 mm (Example 22-05.6).
- **Part 4.** The optimum is 0.140 T with 8.55 turns, and 9 turns cost less than 1% more loss. The 60µ Kool Mµ fit gives 76.7% of initial permeability at 50 Oe and 47.7% at 100 Oe.

## Discussion

1. **Why does the gapped core give so little warning?** Below saturation, the gap carries over 90% of the magnetomotive force, so the core's falling permeability barely changes the total reluctance. Once the ferrite saturates, its permeability falls toward $\mu_0$ and its 78.6 mm path becomes an air gap 150 times longer than the real one. The inductance collapses by roughly that factor and the current ramps at the air-core rate. A powder core, whose permeability falls gradually, gives the warning a ferrite does not.
2. **Why is the measured leakage slightly below $L_{lk}$?** The short-circuit test measures $L_1(1 - k^2) = L_{lk}(L_m + L_{lk}/4)/(L_m + L_{lk}/2)$, which is $L_{lk}$ less a fraction $L_{lk}/(4L_m)$ of itself: 0.02% here.
3. **Why does a thicker foil lose more?** Its DC resistance falls as $1/h$, but in a multilayer section its proximity loss rises as $h^4$ for thin layers and faster for thick ones. The product has a minimum below one skin depth.

## Optional hardware

An LCR meter and two ferrite core halves with a few spacer shims show the gap at work. Wind 20 turns, measure the inductance ungapped and with each shim (the shim appears in all legs of an E core, so its effect is double in the centre leg's path). Compare with $\mu_0N^2A_e/g$ and the vendor's $A_L$. Then short a second winding and measure the leakage.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 22-05.a | current at the 5.61 µs on-time | 2.53 | A |
| Lab 22-05.b | current at 11.5 µs | 5.55 | A |
| Lab 22-05.c | current at 12.5 µs | 29.2 | A |
| Lab 22-05.d | time to reach 390 mT | 12.1 | µs |
| Lab 22-05.e | linear current at 12.5 µs | 5.61 | A |
