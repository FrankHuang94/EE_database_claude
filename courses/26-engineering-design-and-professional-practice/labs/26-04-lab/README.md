# Lab 26-04 · License or Build, Which Node, Chiplets or Not, Custom or Merchant

**Objective.** Turn the four sourcing decisions of chapter 26-04 into curves you can read a decision from: present cost against volume for licensing and building, density gain against logic shrink, family cost against product volume, and the custom accelerator's break-even fleet against the merchant's price.

**Chapter:** [26-04 · Engineering Economics II: Build, Buy or License; Node; Chiplets; ASIC vs Merchant](../../chapters/26-04-engineering-economics-2.md)

## Background

§3.2 derived the present costs $\text{PV}_L = F + rU$ and $\text{PV}_B = N_B + p_sC_s$ and the discounted break-even $U^*$. §3.4 derived the mix-weighted density gain $s_{eff} = 1/\sum_k f_k/s_k$ and the node break-even volume. §3.5 extended 25-07's chiplet cost model to a product family with reuse and mixed nodes. §3.6 built the accelerator TCO per unit of throughput, the break-even fleet and the merchant price ceiling. §3.7 solved a two-generation decision tree.

## Files

- `sourcing.py`: the discounted unit stream, per-unit and percentage royalties, licence and build present costs and the discounted break-even; the effective density gain, cost per good die and node break-even; chiplet package and family costs; slot TCO, cost per unit of throughput and the merchant price ceiling; the two-generation decision tree. It imports dies per wafer from Lab 26-03's `econ.py`.
- `26-04-sourcing-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · License or build** (notebook). *Predict* the in-house NRE at which building Example 26-04.2's PHY would tie with licensing it at the planned volume, keeping the 25% chance of a $15 M slip. Then plot both present costs against the discounted unit stream from 0 to 40 million units and mark the plan and the break-even.

**Part 2 · Amdahl's law for area** (notebook). *Predict* the logic density gain a die of 50% logic, 30% SRAM and 20% analog needs for an overall gain of 1.5×, with SRAM at 1.2× and analog at 1.1×. Then plot $s_{eff}$ against $s_L$ from 1 to 10 and draw the ceiling of Example 26-04.3(b).

**Part 3 · Chiplet family** (notebook). *Predict* how large product S's lifetime volume must grow, with L fixed at 1 million units, before the monolithic family of Example 26-04.4 becomes cheaper than the chiplet family. Then sweep S's volume from 0 to 25 million units and plot both family totals.

**Part 4 · Custom or merchant** (notebook). *Predict* the merchant price at which Example 26-04.5's custom accelerator saves nothing per merchant-equivalent, however large the fleet. Then plot the break-even fleet against merchant prices from $15,000 to $40,000.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 26-04.a | build NRE that ties with the licence | 11.95 | $M |
| Lab 26-04.b | logic gain for an overall 1.5× | 2.13 | |
| Lab 26-04.b1 | SRAM and analog terms | 0.4318 | |
| Lab 26-04.b2 | overall gain at 3× logic | 1.67 | |
| Lab 26-04.b3 | overall gain at 10× logic | 2.08 | |
| Lab 26-04.c | S volume at which the families tie | 15.5 | million |
| Lab 26-04.d | merchant price with no saving | 13794 | $ |

## Discussion

1. The build option ties only if its NRE falls to $11.95 M, about half the assumed $24 M: at this volume, a silicon-proven licence is much the cheaper route, and the case for building must rest on reuse or differentiation (Example 26-04.6).
2. A 1.5× overall gain needs logic to shrink 2.13×, far beyond the 1.7× quoted, because SRAM and analog alone already take 0.4318 of the original area. The curve flattens quickly: tripling logic density gives an overall **1.67**×, and a tenfold gain only **2.08**×.
3. The chiplet family stays cheaper until S reaches 15.5 million units, with L fixed at 1 million. Beyond that, S's $4.72 unit-cost penalty outweighs the reuse saving: the higher the volume of the small products, the more a dedicated monolithic die is worth.
4. At a merchant price of $13,794 the custom chip's cost per merchant-equivalent equals the merchant's, so no fleet size recovers the NRE; the break-even fleet grows without limit as the merchant price approaches it. Above it, each dollar of merchant margin shrinks the fleet needed.

## Optional hardware

None needed. If you have access to two public datasheets for chips in the same family on different nodes (for example, a microcontroller migrated from 40 nm to 22 nm), compare the die areas, where published, with the effective density gain your own guess of the block mix predicts.
