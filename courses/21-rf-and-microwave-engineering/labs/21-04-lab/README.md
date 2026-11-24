# Lab 21-04 · Low-Noise Amplifiers: Match, Noise, Inductor Loss and Noise Cancelling

Chapter: [21-04 · Low-Noise Amplifiers](../../chapters/21-04-low-noise-amplifiers.md)

## Objective

- See the inductively degenerated LNA's real input impedance appear from reactances, and measure the bandwidth of its match.
- Measure how the gate inductor's quality factor sets the noise figure.
- Explore the trade between the input network's Q, noise figure and IIP3.
- Compare a common-gate input with a noise-cancelling wideband LNA, and confirm all four noise figures in ngspice.

## Background

`lna.py` holds the chapter's formulas (`nf_resistive_termination`, `nf_common_gate`, `nf_noise_cancelling`, `design_ind_degen`, `design_with_gate_q`, `nf_ind_degen`, `zin_ind_degen`, `iip3_shift_db`) and a nodal solver of the degenerated LNA's small-signal model (`solve_ind_degen`). `lna_noise.cir` builds four LNA input stages from ideal elements; each channel-noise current comes from a resistor in its own loop, mirrored between drain and source by a current-controlled current source, so the transistor's transconductance itself stays noiseless and ngspice's noise analysis gives the drain-noise-only noise figure of the chapter.

## Procedure

1. **The match.** Plot the input impedance and return loss of Example 21-04.2's LNA from 1 to 4 GHz; *predict* the 10 dB band from the input loop's Q, then read it off (Part 1).
2. **Inductor Q.** Sweep the gate inductor's Q from 5 to 100, re-matching at each step, and plot the noise figure; *predict* the Q that gives 1 dB (Part 2).
3. **Q, noise and linearity.** At fixed $g_m$ = 40 mS, sweep $f_T$ from 6 to 48 GHz; plot the noise figure and the IIP3 shift $20\log_{10}Q_{in}$ (Part 3).
4. **Wideband.** Plot the noise-cancelling LNA's noise figure against $g_{m2}$ (keeping $R_1$ at cancellation, $R_2$ = 200 Ω) next to the common-gate limit; then sweep $R_1$ at $g_{m2}$ = 100 mS (Part 4).
5. **ngspice.** Run `ngspice -b lna_noise.cir` and compare the four noise figures with the formulas (Part 5).

## Expected results

- **Part 1.** The input is exactly 50 Ω at 2.4 GHz; the 10 dB return-loss band runs from 2.101 to 2.741 GHz (26.7%).
- **Part 2.** The noise figure falls from **2.19** dB at $Q$ = 5 toward 0.33 dB; it crosses 1 dB at $Q$ ≈ **15.3**.
- **Part 3.** Raising $f_T$ lowers the noise figure as $(f_0/f_T)^2$ but raises $Q_{in}$ in proportion, costing $20\log_{10}Q_{in}$ of IIP3: 6 dB per doubling.
- **Part 4.** With cancellation the noise figure is **1.48** dB at $g_{m2}$ = 50 mS, 0.77 dB at 100 mS and **0.39** dB at 200 mS, all below the common gate's 2.22 dB; at 100 mS it is 0.83, 0.77 and 0.72 dB for $R_1$ = 900, 1000 and 1100 Ω.
- **Part 5.** ngspice: 0.334, 1.011, 2.218 and 0.768 dB, matching Examples 21-04.2, 21-04.3, 21-04.1 and 21-04.5.

## Discussion

1. **Where does the degenerated LNA's 50 Ω come from, if not from a resistor?** From the transconductance current flowing in the source inductor: it develops a voltage in phase with the input current, so the input looks resistive at all frequencies, $\omega_TL_s$, while dissipating nothing itself. Near resonance, where the reactances cancel, that term is the whole input impedance.
2. **Why does the drain noise reach the output halved?** The noise current also flows through $L_s$, drives the matched input loop, and produces a gate voltage whose transconductance current cancels half of it (§3.4).
3. **Why is the noise-cancelling LNA's noise not limited by its match?** The match is set by M1 ($g_{m1} = 1/R_s$), but M1's noise is cancelled; what remains is M2's, which falls as $g_{m2}$ grows, at the cost of current.

## Optional hardware

An evaluation board for a discrete LNA (most vendors offer one) with a noise-figure analyzer or a spectrum analyzer with a noise source lets you measure the noise figure, then swap the input inductor for one of lower Q (a smaller-case-size part of the same value) and watch the noise figure rise, as in Part 2.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 21-04.a | gate-inductor Q for 1 dB | 15.3 | — |
| Lab 21-04.d | NF at gate-inductor Q of 5 | 2.19 | dB |
| Lab 21-04.b | noise-cancelling NF at gm2 = 50 mS | 1.48 | dB |
| Lab 21-04.c | noise-cancelling NF at gm2 = 200 mS | 0.39 | dB |
