# Lab 19-11 · Power Straps, Placement, Routing and Clock Trees

Chapter: [19-11 · The ASIC Flow II: Floorplan, Place and Route, Signoff](../../chapters/19-11-place-route-signoff.md)

## Objective

- Size a floorplan and check a power strap's IR drop against the closed form and against ngspice.
- Solve quadratic placement as a linear system and see why it needs spreading.
- Route with Lee's maze algorithm, and measure how much Steiner points save over spanning trees.
- Build a zero-skew clock merge and confirm its equal Elmore delays in ngspice.
- Estimate a routed net's delay on different metal layers.

## Background

The chapter's §3.1 derives the strap drop ($IR/8$ fed at both ends), §3.2 quadratic placement, §3.3 H-trees and the zero-skew tapping point, §3.4 maze routing and Steiner trees, and §3.5 the Elmore delay of a routed net.

Files:

- `pnr.py`: `core_dimensions`; `strap_drop_continuous`, `strap_drop_ladder` (nodal solution of a discretized strap, exact at its nodes), `max_strap_spacing`; `quadratic_place`, `hpwl`; `lee_route`, `rmst_length`, `rmst_edges`, `rsmt_points`, `rsmt_length` (exhaustive over Hanan points, for small nets); `zero_skew_tap`, `merged`, `snake_length`, `elmore_tree`, `wire_elmore`.
- `strap.cir`: ngspice model of Problem 19-11.12's strap (200 one-micrometre segments, a uniform load and a hot spot). Run `ngspice -b strap.cir`.
- `merge.cir`: ngspice model of Problem 19-11.7's zero-skew merge, with each wire as a 40-section π ladder. The Elmore delay to each sink is measured as the area above its unit-step response, $\int_0^\infty (1 - v(t))\,dt$, which equals the first moment of the impulse response. Run `ngspice -b merge.cir`.
- `net.cir`: ngspice model of Example 19-11.6(a), a 1 mm metal-1 net (40-section π ladder) driven through 5.64 kΩ into 2.302 fF; it measures the Elmore delay (by the same integral) and the 50 % delay. Run `ngspice -b net.cir`.
- `19-11-pnr-lab.ipynb`: the procedure below.

## Procedure

1. **Floorplan and straps.** Reproduce Example 19-11.1. Then predict the drop at the middle of Problem 12's strap (100 µm), and run `strap.cir` (Part 1).
2. **Placement.** Solve Example 19-11.3, then a random 40-cell netlist with pads on the boundary. Predict where the cells end up before you plot them (Part 2).
3. **Routing.** Route Problem 5's maze; then compute the RMST/RSMT ratio for 200 random five-pin nets on a 10 × 10 grid (seed 1). Predict the average ratio and the largest (Part 3).
4. **Clock merge.** Compute Problem 7's tapping point and run `merge.cir`. Predict how the tap moves as subtree 2's load grows from 20 to 200 fF (Part 4).
5. **Layers.** For Example 19-11.6's net, predict the length beyond which metal 3 beats metal 1, with the weak `inv_1` driver and with a driver eight times stronger; then sweep the length. Run `net.cir` and compare its Elmore delay and 50 % delay (Part 5).

## Expected results

- Part 1: Example 1 gives a 707.11 µm core of 260 rows; the strap's drop is 46.875 mV at the hot spot (50 µm) and 37.5 mV at the middle, and ngspice agrees to the microvolt.
- Part 2: Example 3's cells sit at (2.5, 1.2), (5.0, 2.4), (7.5, 1.2) and (5.0, 4.8). The random netlist's cells crowd toward the middle of the region, the reason real placers add spreading forces.
- Part 3: the maze route is 12 steps. Over 200 random five-pin nets the spanning tree is on average 9.3 % longer than the Steiner tree (mean ratio 1.093), and at worst 1.333 times, inside Hwang's 3/2 bound.
- Part 4: the tap is 308.3 µm from subtree 1 and both sinks see 16.55 ps in ngspice; as subtree 2's load grows, the tap slides toward it.
- Part 5: metal 3 overtakes metal 1 beyond about 2764 µm with the weak driver and 321 µm with the strong one; `net.cir` gives an Elmore delay of 1091.87 ps (Example 6a) and a 50 % delay of 767.66 ps, 0.70 times the Elmore value.

## Discussion

1. Why is the strap drop at the hot spot almost four times what the uniform load alone causes?
2. Why does quadratic placement crowd cells toward the middle, and why is that not a bad first step?
3. Why do routers accept Steiner heuristics that are a few percent from optimal?
4. Why is the Elmore delay a good target for zero-skew merging even though real delays are 50 % crossings?

**Answers.**

1. The point load is twice the uniform total and is drawn at one place, so all of it flows through part of the strap; the uniform load is spread out, and half of it returns to each feed over a short distance.
2. With only pads fixed, every movable cell is a weighted average of its neighbors, so the solution is pulled to the centroid of the pads; cells have no area in the model. The result still captures which cells belong together, which is the hard part, and spreading then preserves that relative order.
3. Optimal Steiner trees are NP-hard in general, and routing must handle millions of nets; heuristics within a few percent are fast, and the final length is dominated anyway by detours around congestion and blockages.
4. For RC trees the Elmore delay is an upper bound on the 50 % delay and tracks it closely when the paths being compared are similar; balancing Elmore delays makes the real delays nearly equal, and the closed-form tap makes bottom-up construction fast. Signoff then measures the real skew.

## Optional extensions

- With OpenROAD-flow-scripts installed, run the `gcd` design on the `sky130hd` platform and read its reports: core utilization, placement density, clock skew after CTS, global-routing overflow and the final worst slack. Compare the clock skew and the wirelength with what this lab's models suggest.

## Optional hardware

None: physical design is a software activity. Designs made with the open flow can be fabricated on shared multi-project wafers; see the chapter's §9 for the current state of such services.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 19-11.a | strap drop at its middle, Problem 12 | 37.5 | mV |
| Lab 19-11.b | mean RMST/RSMT ratio, 200 random five-pin nets | 1.093 | — |
| Lab 19-11.c | largest RMST/RSMT ratio among them | 1.333 | — |
| Lab 19-11.d | length where metal 3 overtakes metal 1, weak driver | 2764 | µm |
| Lab 19-11.e | length where metal 3 overtakes metal 1, strong driver | 321 | µm |
| Lab 19-11.f | 50 % delay of the 1 mm metal-1 net | 767.66 | ps |
