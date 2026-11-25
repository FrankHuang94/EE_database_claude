# Lab 23-06 · Programming a Flash Cell and Counting Its Errors

Chapter: [23-06 · NAND Flash and 3D NAND](../../chapters/23-06-nand-flash-and-3d-nand.md)

## Objective

Program a flash cell in a circuit simulator with incremental-step pulses and Fowler–Nordheim tunneling, and confirm that its threshold settles into rising one step per pulse. Then use the chapter's models to explore raw bit error rates against level width, and check the formula with a Monte Carlo simulation.

## Background

§3.1 showed that stored charge $Q$ shifts the threshold by $-Q/C_{CG}$, and §3.2 that incremental-step pulse programming (ISPP) raises it by exactly the step $\Delta V_{pgm}$ once each pulse ends at the same storage-node voltage. §3.3 derived the raw bit error rate of $2^n$ Gaussian levels in a window $W$. The circuit model is the cell's two capacitances with a current source that implements $J = AE^2e^{-B/E}$: a behavioral source in ngspice can compute any current from node voltages.

## Files

- `ispp.cir`: the cell of Example 23-06.2 (16 aF control-gate coupling, 12.33 aF tunnel oxide, 7 nm SiO₂, 50 nm × 50 nm) driven by 30 pulses of 10 µs, starting at 15 V and rising 0.25 V per pulse, with 0 V verify windows between them.
- `nand.py`: the chapter's models.
- `23-06-nand-lab.ipynb`: the notebook for Parts 2 and 3.

## Procedure

**Part 1 · ngspice.**

1. Predict the threshold rise per pulse after the first few pulses (§3.2).
2. Run `ngspice -b ispp.cir` and compare the 29th and 30th steps (`step29`, `step30`) with your prediction, and note the first pulse's shift (`vt1`).
3. Make the tunnel oxide 6 nm: change `tox`, scale `ctox` by 7/6 and update the capacitance in the `dvt` line to match. *Predict first:* does the first step grow or shrink? Does the steady-state step change?

**Part 2 · Error rate against level width** (notebook). Plot the raw bit error rate of SLC to QLC in a 6 V window against σ from 0.02 to 0.2 V (chapter Figure 2). Find the σ at which TLC and QLC reach a raw error rate of 10⁻³.

**Part 3 · Monte Carlo** (notebook). Draw 100,000 QLC cells with Gray-coded levels and σ = 0.08 V, add Gaussian noise, read them with midpoint references and count bit errors. Compare with the formula of §3.3.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 23-06.a | threshold shift after the first pulse | 1.917 | V |
| Lab 23-06.b | threshold rise from the 30th pulse | 0.2500 | V |
| Lab 23-06.c | threshold shift after 30 pulses | 9.709 | V |
| Lab 23-06.d | σ for a TLC raw error rate of 10⁻³ (6 V window) | 0.146 | V |
| Lab 23-06.e | σ for a QLC raw error rate of 10⁻³ (6 V window) | 0.0700 | V |

- Part 1: the first pulse moves the threshold much more than 0.25 V, because the uncharged cell starts with a strong field. Within a few pulses each step settles to 0.25 V. With a 6 nm oxide the first step grows, but the steady-state step stays 0.25 V.
- Part 3: with 100,000 cells (400,000 bits) the Monte Carlo error rate agrees with the formula's 2.91 × 10⁻³ (Example 23-06.4) to within a few percent, the scatter expected from over a thousand counted errors.

## Discussion

1. Why is the steady-state step independent of the oxide thickness, though the first step is not?

   <details><summary>Answer</summary>

   The first pulses must raise the field to the point where tunneling turns on, and how much charge they deliver depends on the oxide and the tunneling constants. Once each pulse ends at the same stalled storage-node voltage, the charge per pulse is set only by $C_{CG}\Delta V_{pgm}$ (§3.2). A thinner oxide changes the stall voltage, not the step.

   </details>

2. Why is the tunneling current a voltage-controlled source in the netlist rather than a resistor?

   <details><summary>Answer</summary>

   Fowler–Nordheim current is a steep nonlinear function of the field, not proportional to voltage. A behavioral source evaluates $AE^2e^{-B/E}$ at each time step from the floating-gate voltage. A resistor would make the current proportional to voltage, and the cell would neither turn on sharply nor self-limit.

   </details>

3. What does the model leave out?

   <details><summary>Answer</summary>

   Charge-trap physics (charge stored in discrete traps that spread over time), the channel's own inversion and the current needed to form it, coupling to neighbouring cells, and verify-inhibit: in a real page, cells that reach their target are switched off by raising their bitline. The model also has no noise, so every cell would land on exactly the same threshold. Real distributions have the width that §3.3 analyses.

   </details>

## Optional hardware

A USB flash drive or SD card can show endurance in practice. Tools such as `f3` (Fight Flash Fraud) write and verify the whole device and report capacity and errors. Running them repeatedly wears the device, so use one you can sacrifice.
