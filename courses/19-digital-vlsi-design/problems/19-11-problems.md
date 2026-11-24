# Problems 19-11 · The ASIC Flow II: Floorplan, Place and Route, Signoff

Chapter: [19-11](../chapters/19-11-place-route-signoff.md) · Worked solutions: [19-11 solutions](../solutions/19-11-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Lengths in µm unless stated; SKY130 high-density rows are 2.72 µm tall and sites 0.46 µm wide (19-09). Wire delays are Elmore constants (19-05): unscaled, suitable for balancing and comparison; a 50 % delay needs the 0.38 and 0.69 factors of 19-05. Problems marked *(lab)* can be checked with `labs/19-11-lab/pnr.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 19-11.1 [A] *(lab)*

**A tall core.** A block has 120 000 µm² of standard cells. At 70 % target utilization and an aspect ratio (height/width) of 2, find the core width, the number of rows and the core height, the number of placement sites per row, and the utilization actually achieved after rounding to whole rows.

### Problem 19-11.2 [A]

**Feeding a strap.** A strap of total resistance 2.0 Ω supplies 20 mA drawn uniformly along its length. (a) What is the worst IR drop if it is fed from both ends? From one end? (b) By what factor does the both-ends drop change if the strap is cut in half by an extra feed in the middle (two straps of half the length, each fed at both ends, with half the current each)?

### Problem 19-11.3 [A]

**Half-perimeter wirelength.** (a) Find the HPWL of a net with pins at (2, 3), (10, 5) and (6, 11). (b) Show that some rectilinear tree connecting these three pins has exactly this length. (c) Why can HPWL underestimate a net with many pins?

### Problem 19-11.4 [B] *(lab)*

**Springs in one dimension.** Pads P0 and P1 are fixed at x = 0 and x = 12. Cell A connects to P0 (weight 1), to B (weight 2) and to P1 (weight 1); cell B connects to A (weight 2) and to P1 (weight 1). (a) Write the equations and find the quadratic-placement positions. (b) Check that each cell sits at the weighted average of its neighbors. (c) What happens to the positions if both pads move right by 3?

### Problem 19-11.5 [B] *(lab)*

**A maze.** On a 7 × 7 grid of cells (rows and columns numbered 0–6), a wall blocks column 3 in rows 0 through 5. Route from row 3, column 0 to row 3, column 6 with Lee's algorithm (moves up, down, left, right). (a) What is the Manhattan distance and the length of the shortest legal path? (b) Why must any legal path be at least this long?

### Problem 19-11.6 [B] *(lab)*

**The worst case for spanning trees.** Pins sit at (0, 2), (2, 0), (2, 4) and (4, 2). (a) Find the HPWL, the RMST length and the RSMT length. (b) Compare the RMST/RSMT ratio with Hwang's bound. (c) Where is the Steiner point, and why does it help so much here?

### Problem 19-11.7 [B]

**Merging two clock subtrees.** Subtree 1 has an Elmore constant of 10.0 ps to its sinks and 40 fF of capacitance; subtree 2 has 12.0 ps and 60 fF. Their roots are joined by a 500 µm wire with r = 0.30 Ω/µm and c = 0.20 fF/µm. (a) Find the zero-skew tapping point. (b) Find the merged delay and capacitance. (c) If subtree 2's delay were 80 ps instead, what would happen, and how much extra wire on subtree 1's side would balance the two (tap at subtree 2's root)?

### Problem 19-11.8 [B]

**An H-tree.** A three-level H-tree spans a 2.0 mm × 2.0 mm core. (a) How many sinks does it reach? (b) What is the source-to-sink wire length, and the total wire length? (c) At 0.2 fF/µm, what is the tree's wire capacitance?

### Problem 19-11.9 [B]

**Clock power.** A SKY130 block has 20 000 `dfxtp_1` flip-flops (clock-pin capacitance 1.794 fF each, 19-10's Liberty data), 4.0 pF of clock wiring and 2.0 pF of clock-buffer input capacitance, at 1.8 V and 100 MHz. (a) Find the total switched clock capacitance and the clock power. (b) Which term dominates, and what does that suggest about reducing clock power?

### Problem 19-11.10 [B]

**Layer data.** SKY130's tech LEF gives sheet resistances of 0.125 Ω/□ (metal 1), 0.047 Ω/□ (metal 3) and 0.0285 Ω/□ (metal 5), minimum widths of 0.14, 0.30 and 1.6 µm, and average-current electromigration limits of 2.8, 6.8 and 10.17 mA per µm of width [R-319]. (a) Find each layer's resistance per micrometre at minimum width. (b) The open flow's estimate for metal 1 is 1.20565 Ω/µm; by what factor does it exceed (a), and why might an estimation model be set high? (c) What is the resistance of a 2 mm minimum-width metal-3 clock wire? (d) What average current may a minimum-width metal-1 wire and a minimum-width metal-3 wire carry, and how wide must a metal-1 rail be to carry 1.5 mA?

### Problem 19-11.11 [C]

**Why fixed pins are needed.** (a) Show that for a connected netlist with no fixed pins, the quadratic-placement matrix $Q$ is singular, and identify the direction in which the energy is flat. (b) Show that with at least one fixed pin in a connected netlist, $Q$ is positive definite. (c) Explain, using linearity, why moving every fixed pin by the same vector moves every cell by that vector.

### Problem 19-11.12 [C]

**A hot spot on a strap.** A 200 µm strap with r = 0.5 Ω/µm is fed at both ends. It supplies 1 mA drawn uniformly, plus a 2 mA point load (a hot macro) at 50 µm from the left end. (a) Derive the drop caused by the point load alone, as a function of position. (b) Find the worst total drop and where it occurs. (c) Compare with the uniform load's worst drop alone, and with placing the macro at the middle.

### Problem 19-11.13 [B] *(lab)*

**Slack after routing.** A driver whose Liberty delay slope is $R_{\text{eff}}$ = 1.41 kΩ drives four `inv_1` inputs (2.302 fF each). Use §3.5's 50 % estimate and the open flow's metal-1 estimate of 1.20565 Ω/µm and 0.172375 fF/µm (metal 3: 0.166281 Ω/µm and 0.214962 fF/µm) [R-319]. (a) Placement estimated the net at its HPWL, 400 µm of metal 1. Find the delay, split into its driver and wire terms. (b) The router detours around a macro, giving 600 µm of metal 1. Find the new delay and the slack lost. (c) For 300 µm of the route a neighbor runs alongside with 0.05 fF/µm of coupling capacitance, already counted in the per-length value for a quiet neighbor. Treating the change in effective coupling as spread along the wire, by how much can the neighbor's switching change the delay of (b), and in which directions? (d) Compare two fixes for (b): moving the 600 µm route to metal 3, and a driver twice as strong ($R_{\text{eff}}$ = 705 Ω). Which recovers the placement-stage delay, and what does the stronger driver cost?

### Problem 19-11.14 [A]

**Which check catches it?** For each defect, name the signoff check that catches it and what that check protects against. (a) A missing via array in a power strap leaves one region of the block with a supply droop much larger than the timing assumed. (b) Two metal-2 wires drawn 0.10 µm apart where the rule requires 0.14 µm. (c) An engineering change order swaps the two data inputs of a multiplexer in the netlist. (d) A path that met hold with estimated wires fails it at the fast corner with extracted parasitics. (e) A long metal-1 wire connected only to a transistor gate collects charge during plasma etching. (f) A metal fill shape shorts an output net to VDD. (g) A clock wire's average current density exceeds its layer's limit. (h) Timing was signed off assuming at most 5 % IR drop on a 1.80 V supply; dynamic analysis shows 8 % in one region. Express both in millivolts and say what must happen next.

### Problem 19-11.15 [C]

**One improvement step of min-cut bisection.** Six cells are joined by two-pin connections of weight 1: (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6) and (2, 5). A balanced bisection puts three cells on each side. Start from A = {1, 2, 4}, B = {3, 5, 6}. (a) Find the cut. (b) Find every cell's gain (connections to the other side minus connections to its own side). (c) Find the Kernighan–Lin swap of one cell from A with one from B that reduces the cut most, explaining the $-2w_{ab}$ correction, and the new cut. (d) Show that no further single swap reduces the cut. (e) How many distinct balanced bisections are there, and is the result the global minimum?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Floorplan sizing and IR drop | 1, 2, 12 |
| 2. Placement and wirelength | 3, 4, 11, 15 |
| 3. Clock trees | 7, 8, 9 |
| 4. Routing and Steiner trees | 5, 6 |
| 5. Extraction and post-route delay | 10, 13 |
| 6. Signoff checks | 12, 14 |
