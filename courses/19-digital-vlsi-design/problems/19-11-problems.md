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

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Floorplan sizing and IR drop | 1, 2, 12 |
| 2. Placement and wirelength | 3, 4, 11 |
| 3. Clock trees | 7, 8, 9 |
| 4. Routing and Steiner trees | 5, 6 |
| 5. Extraction and post-route delay | 10 |
| 6. Signoff checks | 9, 10, 12 |
