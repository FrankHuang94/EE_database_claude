# Lab 19-03 · Logic Families: Stacks, Ratios, Pass Gates and Dynamic Nodes

Chapter: [19-03 · Combinational Logic Families](../../chapters/19-03-logic-families.md)

## Objective

- Check the Elmore delay against exact RC responses, and see how fan-in makes a stack slow.
- Measure a pseudo-NMOS gate's output level and static current, and an NMOS pass transistor's degraded 1, in ngspice.
- Find the best buffer spacing for a transmission-gate chain.
- Map when charge sharing breaks a dynamic gate.

## Background

The Elmore constant of an RC tree is $\sum_m C_mR_{km}$, each capacitance times the resistance it shares with the path to the output, and $t_p \approx 0.69\tau_E$ (§3.3). A pseudo-NMOS gate's low level satisfies $\tfrac12k_p(V_{DD} - \lvert V_{TP}\rvert)^2 = k_n[(V_{DD} - V_{TN})V_{OL} - V_{OL}^2/2]$ (§3.4). An NMOS passes a 1 only up to $V_{DD} - V_{TN}(V_{out})$ (§3.6). A dynamic output shares its charge with internal nodes, losing $(C_a/C_L)(V_{DD} - V_{TN})$ if the transistor cuts off first, or equalizing at $V_{DD}C_L/(C_L + C_a)$ otherwise (§3.7).

Files:

- `pseudo_nmos.cir`, `pass_gate.cir`, `dynamic.cir`, `tg_ladder.cir`: ngspice netlists (level-1 model) for Examples 19-03.3, 4, 6 and 5.
- `logic.py`: sizing (`nand_sizes`, `nor_sizes`, `input_cap_ratio`), the Elmore delay (`elmore_ladder`, `nand_stack_elmore`) and exact ladder responses (`ladder_step_50`), pseudo-NMOS (`pseudo_nmos_vol`, `pseudo_nmos_static_current`, `pseudo_nmos_ratio_for_vol`), pass transistors (`vt_body`, `nmos_pass_high`, `inverter_static_current`), TG chains (`tg_chain_delay`, `tg_chain_buffered`, `tg_optimal_m`) and dynamic nodes (`charge_sharing`, `hold_time`).
- `19-03-logic-lab.ipynb`: the procedure below.

## Procedure

1. **Fan-in.** Predict the NAND-$N$ delay for $N$ = 1 to 12 with Example 19-03.2's values, and where the quadratic term overtakes the linear one; run Part 1.
2. **Elmore against exact.** Predict how the ratio of the exact 50% delay to $0.69\tau_E$ changes with the number of ladder sections; run Part 2 and `ngspice -b tg_ladder.cir`.
3. **Pseudo-NMOS.** Predict $V_{OL}$ and the static current of Example 19-03.3; run `pseudo_nmos.cir` and Part 3, which sweeps $k_n/k_p$.
4. **Pass transistor.** Predict the passed level for $\gamma_B$ = 0, 0.4 and 0.6 V$^{1/2}$; run Part 4 and `pass_gate.cir`.
5. **Buffered TG chains.** Predict the best segment length for $t_{buf}$ = 10, 30 and 100 ps; run Part 5.
6. **Charge sharing.** Predict the output for $C_a$ from 0 to 20 fF; run Part 6 and `dynamic.cir`.

## Expected results

- Part 1: delays of 79.7, 93.6, 110.9 and 131.7 ps for $N$ = 1 to 4. The quadratic term, $RcN(N-1)/2$, overtakes the linear one, $R(3cN + C_{ext})$, only at $N$ = 10.7, where each is 261 ps of Elmore constant: with a 10 fF load the internal nodes matter, but the output still dominates for practical fan-ins.
- Part 2: ratios of 1.000, 1.070, 1.087 and 1.092 for 1, 2, 4 and 12 sections, approaching about 1.09; ngspice measures 590.5 ps for the 12-section ladder.
- Part 3: $V_{OL}$ = 0.114 V and 18.1 µA, the same in ngspice; $V_{OL}$ falls roughly as $k_p/k_n$.
- Part 4: 0.85, 0.715 and 0.661 V; ngspice gives 0.715 V and a following-inverter current of 1.81 µA.
- Part 5: optimal segment lengths of 1.70, 2.94 and 5.37 sections.
- Part 6: the output falls linearly with $C_a$, by 0.085 V per fF, until $C_a/C_L$ = 0.412, where it is 0.850 V; beyond that it follows $V_{DD}C_L/(C_L + C_a)$ and crosses 0.6 V at $C_a$ = 10 fF. ngspice gives 0.945 and 0.545 V for 3 and 12 fF.

## Discussion

1. Why does the Elmore estimate become less accurate for long ladders, and in which direction?
2. Why does a pseudo-NMOS gate's $V_{OL}$ depend on the ratio $k_n/k_p$ but a static CMOS gate's does not?
3. Why is the approach of a pass transistor's output to $V_{DD} - V_{TN}$ so slow?
4. Why does a smaller output capacitance make a dynamic gate more vulnerable to charge sharing?

**Answers.**

1. The factor 0.69 is exact only for a single pole. A long ladder's far end responds later and more gradually, so its 50% point is later than $0.69\tau_E$, by about 9% for long ladders (Problem 19-03.10).
2. In pseudo-NMOS both networks conduct when the output is low, and the level is where their currents balance; in static CMOS the pull-up is off, so the output reaches 0 V whatever the sizes.
3. Its current is proportional to the square of $V_{GS} - V_{TN}$, which goes to zero as the output approaches the cut-off level, so the remaining gap closes ever more slowly (as $1/t$).
4. The charge an internal node takes is fixed by its own capacitance and voltage; the output's voltage drop is that charge divided by the output capacitance.

## Optional hardware

A CD4007 provides NMOS and PMOS transistors for a breadboard pseudo-NMOS inverter (a PMOS with its gate grounded as the load) and an NMOS pass transistor. At 5 V, measure $V_{OL}$ against a series resistor in the source of the load (to vary its strength), and the degraded 1 passed by the NMOS into a high-impedance meter.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 19-03.a | fan-in where the quadratic term equals the linear one | 10.7 | — |
| Lab 19-03.b | each term there | 261 | ps |
| Lab 19-03.c | exact over estimate, 2 sections | 1.070 | — |
| Lab 19-03.d | passed level, gamma = 0.6 | 0.661 | V |
| Lab 19-03.e | optimal segment, t_buf = 10 ps | 1.70 | — |
| Lab 19-03.f | optimal segment, t_buf = 100 ps | 5.37 | — |
| Lab 19-03.g | output at the charge-sharing boundary | 0.850 | V |
| Lab 19-03.h | Ca where the output crosses 0.6 V | 10 | fF |
| Lab 19-03.i | slope of the output in the cut-off region | 0.085 | V/fF |
