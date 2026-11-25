# Problems 22-12 · Power Systems Fundamentals

Chapter: [22-12](../chapters/22-12-power-systems-fundamentals.md) · Worked solutions: [22-12 solutions](../solutions/22-12-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Three-phase systems, 60 Hz unless stated; per-unit values on the stated base; resistance neglected unless given. Values marked "assumed" are illustrative. Problems marked *(lab)* can be checked with `labs/22-12-lab/grid.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 22-12.1 [A]

**A 500 kV base.** On a 500 MVA, 500 kV base, find (a) the impedance base, (b) the current base and (c) a 25 Ω line in per unit.

### Problem 22-12.2 [A]

**Changing base twice.** A generator has $X''_d$ = 0.15 pu on 200 MVA, 20 kV. Express it on a 100 MVA, 22 kV base.

### Problem 22-12.3 [A]

**Referring an impedance.** A 10 Ω load sits on the 13.8 kV side of a 13.8/138 kV transformer. What impedance does it present on the 138 kV side?

### Problem 22-12.4 [B]

**SIL and loadability.** A 500 kV line has $Z_c$ = 250 Ω. Find (a) its SIL and (b) its planning loadability at 150 km using the rule of §3.2.

### Problem 22-12.5 [B]

**The angle for 2 pu.** *(lab)* Bus 1 at 1.02 pu feeds bus 2 at 1.00 pu through $X$ = 0.25 pu. For 2.0 pu of real power, find (a) the angle, the reactive power (b) arriving at bus 2 and (c) leaving bus 1.

### Problem 22-12.6 [A]

**A 69 kV voltage drop.** A 69 kV line with $R$ = 2 Ω and $X$ = 8 Ω carries 30 MW and 10 Mvar. Estimate the voltage drop (a) in volts and (b) as a percentage.

### Problem 22-12.7 [B]

**Fault MVA through a transformer.** A 138 kV bus has a short-circuit level of 5000 MVA. A 100 MVA, 138/13.8 kV transformer with 10% impedance feeds a 13.8 kV bus. On a 100 MVA base, find (a) the source impedance, (b) the fault MVA at the 13.8 kV bus and (c) the fault current there.

### Problem 22-12.8 [C]

**When the ground fault is worse.** At a bus with $Z_1 = Z_2$ = j0.12 pu and $Z_0$ = j0.06 pu, find (a) the three-phase fault current, (b) the single-line-to-ground fault current, and (c) their ratio.

### Problem 22-12.9 [B]

**A bigger grid.** *(lab)* A 100 GW system with $H$ = 5 s loses 3 GW. Find the RoCoF (a) as is and (b) if $H$ falls to 3 s.

### Problem 22-12.10 [B]

**Two governors.** A 300 MW unit with 4% droop and a 500 MW unit with 5% droop share an 80 MW load increase. Find (a) the frequency change and how much each unit picks up: (b) the 300 MW unit and (c) the 500 MW unit.

### Problem 22-12.11 [B]

**A datacenter trips.** 1500 MW of load drops off an interconnection whose synchronous kinetic energy is 400 GW·s and whose combined governor and load response is 25 GW/Hz (assumed). Find (a) the initial RoCoF and (b) the steady frequency rise.

### Problem 22-12.12 [A]

**What the projections imply.** LBNL reports 192 TWh of US datacenter use in 2024 as 4.7% of US electricity, and projects 649 TWh as 11.8% in 2030. What total US consumption does each figure imply, (a) for 2024 and (b) for 2030?

### Problem 22-12.13 [C]

**The Ferranti effect.** An open-ended 300 km line has a wave speed of 0.979$c$. Find the ratio of receiving-end to sending-end voltage at 60 Hz.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Per-unit and transformers | 1, 2, 3 |
| 2. Line parameters, SIL and line models | 4, 13 |
| 3. Power flow and voltage drop | 5, 6 |
| 4. Faults | 7, 8 |
| 5. Frequency, inertia and large loads | 9, 10, 11, 12 |
