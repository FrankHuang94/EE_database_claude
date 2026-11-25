# Problems 22-04 · Isolated Converters: Flyback and Forward

Chapter: [22-04](../chapters/22-04-isolated-converters.md) · Worked solutions: [22-04 solutions](../solutions/22-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $n = N_1/N_2$ (primary to secondary). Ideal switches and diodes unless stated. Values marked "assumed" are illustrative. Problems marked *(lab)* can be checked with `labs/22-04-lab/isolated.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 22-04.1 [A]

**A 48 V flyback.** A CCM flyback makes 12 V from 48 V with $n$ = 2. Find (a) the duty cycle and (b) the switch's off-state voltage.

### Problem 22-04.2 [A]

**Power in DCM.** A DCM flyback from 300 V has $L_m$ = 1 mH, $D$ = 0.3 and 65 kHz. Find (a) the peak magnetizing current and (b) the power it transfers.

### Problem 22-04.3 [A]

**A forward converter from 400 V.** With $n$ = 16 and a 1:1 tertiary, find (a) the duty cycle for 12 V and (b) the switch voltage during reset.

### Problem 22-04.4 [B]

**A drain-voltage budget.** The flyback of Example 22-04.1 (20 V out, $n$ = 6.4) runs from a 373.4 V bus. Its RCD clamp holds the drain at most 180 V above the bus. Find (a) the worst-case drain voltage, and with a 650 V switch (b) the margin in volts and (c) as a percentage of the rating.

### Problem 22-04.5 [B]

**When does a flyback enter DCM?** *(lab)* The flyback of Example 22-04.1 has $L_m$ = 500 µH at 100 kHz from 150 V. Find (a) the magnetizing ripple and (b) the output current below which it enters DCM.

### Problem 22-04.6 [B]

**Clamp loss against clamp voltage.** A flyback has $L_{lk}$ = 3 µH, $I_{pk}$ = 2 A, 100 kHz and a 100 V reflected voltage. Find (a) the leakage energy per cycle, (b) the leakage power without the multiplier and (c–e) the clamp loss for clamp voltages of 150, 200 and 300 V.

### Problem 22-04.7 [B]

**A different tertiary.** A forward converter's tertiary has half the primary's turns ($N_3/N_1$ = 0.5). Find (a) its maximum duty cycle and (b) its switch voltage as a multiple of $V_{in}$.

### Problem 22-04.8 [B]

**Keeping the flux in bounds.** A forward converter at 48 V, $D$ = 0.4 and 250 kHz has a core of 40 mm² cross-section. Find (a) the flux swing with 6 primary turns and (b) the number of turns (not rounded) for a 0.2 T swing.

### Problem 22-04.9 [B]

**A full bridge for a 12 V bus.** A full-bridge converter makes 12 V at 1.2 kW from a 340–380 V bus, with $D_{eff}$ no more than 0.8 at the lowest input. Find (a) the largest turns ratio, (b) the effective duty at 380 V with $n$ = 22 and (c) the approximate switch current $I/n$.

### Problem 22-04.10 [B]

**Y-capacitor leakage.** Find the line-frequency current through a 4.7 nF Y-capacitor at 264 V (a) at 50 Hz and (b) at 60 Hz. Are both within a 0.5 mA touch-current limit?

### Problem 22-04.11 [A]

**Clearance at altitude.** IEC 60664-1 gives 3.0 mm and IEC 62368-1 gives 3.8 mm of clearance for a 4.0 kV impulse [4]. Find the clearance for each at 5000 m, with an altitude factor of 1.48.

### Problem 22-04.12 [C]

**Design a 24 W universal-input flyback.** 12 V out, 88% efficiency, a 100–373 V bus, a 100 V reflected voltage, boundary conduction at the lowest bus and 65 kHz. Find (a) the turns ratio, the duty cycle (b) at 100 V and (c) at 373 V, (d) the drain voltage before the spike at 373 V, (e) the input power, (f) the peak primary current at 100 V and (g) the magnetizing inductance.

### Problem 22-04.13 [A]

**Creepage on a board.** A reinforced barrier at 400 V working voltage, pollution degree 2, needs twice the basic creepage of 2.0, 2.8 and 4.0 mm for material groups I, II and III (Example 22-04.6). (a) What reinforced creepage does a group III board need, and (b) how much shorter is the path on a group I material? (c) A transformer bobbin offers a 6.0 mm surface path between windings: which material groups can it use?

### Problem 22-04.14 [C]

**The flyback in discontinuous conduction.** A flyback makes 5 V at 2 A from 48 V at 150 kHz with $L_m$ = 30 µH and $n$ = 4. (a) From the energy delivered per cycle, derive the DCM ratio $M = D\sqrt{RT_s/(2L_m)}$ and find $D$. (b) Confirm that it is discontinuous by comparing $2L_m/(n^2RT_s)$ with $D'^2$ at the CCM duty cycle. Find (c) the peak primary current and (d) the magnetizing inductance that would put it at the CCM–DCM boundary.

### Problem 22-04.15 [C]

**A forward converter's power stage.** A forward converter with a 1:1 reset winding makes 3.3 V at 15 A from 36–72 V at 300 kHz with $n$ = 4.5. Find (a) the duty cycle at 36 V and at 72 V, and check it against $D_{max}$. (b) The output inductor sees $V_{in}/n - V$ while the switch is on; find the inductance that holds the ripple to 30% of the load at the worst-case input. (c) What output capacitance keeps the capacitive ripple within 20 mV? (d) The primary has 9 turns on a 60 mm² core: what is the flux swing, and does it depend on the input voltage?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Transformer model and core reset | 7, 8 |
| 2. Flyback ratio, stresses, CCM/DCM and magnetizing inductance | 1, 2, 4, 5, 12, 14 |
| 3. Leakage energy and the clamp | 4, 6 |
| 4. Forward converter reset and bridges | 3, 7, 8, 9, 15 |
| 5. Isolation: Y-capacitance, clearance, creepage | 10, 11, 13 |
