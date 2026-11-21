# Lab 19-09 · Euler Paths, Pitches and Area

Chapter: [19-09 · Layout, Design Rules and Standard Cells](../../chapters/19-09-layout-and-standard-cells.md)

## Objective

- Turn series-parallel transistor networks into graphs and find the input orderings that give unbroken diffusion.
- Compute transistor pitches and strip lengths from a rule set.
- Estimate block area from cell counts, gate density and utilization.

## Background

A static gate's transistors fit in single diffusion strips if one input ordering is an Euler path in both the pull-down network and its dual pull-up network (§3.3). Rules set the contacted pitch (poly, two contact-to-gate spacings and a contact) and the uncontacted pitch (poly plus poly spacing) (§3.2). Core area is cell area over utilization (§3.4).

Files:

- `layout.py`: `to_edges`, `dual`, `is_euler_path`, `common_euler_orders`, `diffusion_breaks` (exact fewest breaks for one ordering), `stack_variants` (every reordering of the series stacks), `fewest_breaks` (best ordering over all stack orders), the illustrative rule set `RULES`, `contacted_pitch`, `uncontacted_pitch`, `strip_length`, `cell_area`, `core_area` and `gates_area_mm2`.
- `19-09-layout-lab.ipynb`: the procedure below.

There is no circuit simulation in this lab: layout tools (Magic, KLayout, the OpenLane flow) are introduced in 19-11.

## Procedure

1. **NAND, NOR and complex gates.** Predict the number of valid orderings for NAND3, NOR3, OAI21, AOI22, AOI211 and OAI22; run Part 1.
2. **Breaks.** For the AOI22, count the breaks the orderings A-B-C-D and A-C-B-D need in each network (Part 2).
3. **Larger gates.** Count the valid orderings of $\overline{AB + C(D + E)}$. Then predict whether $\overline{A(BC + DE)}$ has a common Euler path for any stack order, and the fewest breaks it needs (Part 3).
4. **Rules.** Change the contact-to-gate spacing to 3λ and recompute both pitches and the three-transistor strip lengths (Part 4).
5. **Area.** Estimate a block of 500 kGates and 30 000 flip-flops at 65% and 80% utilization (Part 5).

## Expected results

- Part 1: NAND3 2, NOR3 2 (for a fixed stack order), OAI21 4, AOI22 8, AOI211 4, OAI22 8.
- Part 2: A-B-C-D needs one break in the pull-down and none in the pull-up; A-C-B-D needs one in each.
- Part 3: $\overline{AB + C(D + E)}$ has 6 valid orderings of 120. $\overline{A(BC + DE)}$ has none for any of its 16 stack-order combinations: in the pull-down, A hangs off the loop formed by the two stacks, so every walk starts or ends with A and takes each stack's two transistors back to back. In the pull-up those two transistors are a parallel pair, and taking a pair back to back returns the walk to the node it left. After A the walk is at VDD or the output, which only one pair touches; that pair brings it back there, and the other pair cannot continue. (A last is the same walk reversed.) The best ordering needs 1 break in total (A-B-C-D-E: none in a suitably stacked pull-down, one in the pull-up).
- Part 4: contacted pitch 10λ (uncontacted unchanged at 5λ); strips of 24λ (end contacts only) and 34λ (all contacted).
- Part 5: logic 4.17 mm²; flip-flop core area 0.924 mm² (65%) or 0.751 mm² (80%).

## Discussion

1. Why do the AOI22 and OAI22 have the same number of valid orderings?
2. Why is a fixed series order so restrictive, and why is it not a real restriction?
3. Why might a library team choose a slightly larger cell over a smaller one with a diffusion break?

**Answers.**

1. Each gate's pull-down network is the other's pull-up network; the pair of graphs is identical.
2. A chain admits only its two end-to-end walks, but series transistors can be stacked in any order without changing the logic, so the designer simply chooses the stack order to match a good ordering.
3. A break needs extra spacing and contacts, and it also changes the parasitic capacitance of the nodes on either side; a layout with fewer breaks is usually both smaller and faster, but pin access and routing on the cell can favor other choices.

## Optional hardware

None: layout is a software activity. For a free hands-on next step, install KLayout and open a cell from the SkyWater SKY130 library (`sky130_fd_sc_hd__nand2_1` GDS) to see the layers described in §3.1.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 19-09.a | valid NOR3 orderings, fixed order | 2 | — |
| Lab 19-09.b | valid orderings of AB + C(D + E) | 6 | — |
| Lab 19-09.c | strip length, all contacted, 3λ spacing | 34 | λ |
| Lab 19-09.d | strip length, end contacts, 3λ spacing | 24 | λ |
| Lab 19-09.e | common Euler paths of A(BC + DE), any stack order | 0 | — |
| Lab 19-09.f | fewest total breaks for A(BC + DE) | 1 | — |
