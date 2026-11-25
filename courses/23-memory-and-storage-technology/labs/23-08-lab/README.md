# Lab 23-08 · Heating a Phase-Change Cell and Flipping Magnets

Chapter: [23-08 · Emerging Memories](../../chapters/23-08-emerging-memories.md)

## Objective

Simulate a phase-change cell's RESET and SET pulses as a thermal RC circuit in ngspice, and measure its peak temperature, quench time and SET plateau. Then use the chapter's models to explore MRAM thermal stability against array size and temperature, and simulate thermal flips in a small, deliberately unstable array.

## Background

§3.3 modelled a PCM cell's active region as a thermal capacitance $C_{th}$ behind a thermal resistance $R_{th}$, heated by Joule power $I^2R$. That is exactly an RC circuit driven by a current source, with temperature rise as voltage. §3.2 showed that an MRAM array of $N$ bits held for time $t$ expects $Nt f_0 e^{-\Delta}$ thermal flips.

## Files

- `pcm_thermal.cir`: the cell of Example 23-08.4 (2 kΩ, $R_{th}$ = 7.5 K/µW, $\tau$ = 2 ns) driven by a 200 µA, 50 ns RESET pulse and a 141.42 µA, 150 ns SET pulse.
- `emem.py`: the chapter's models.
- `23-08-emem-lab.ipynb`: the notebook for Parts 2 and 3.

## Procedure

**Part 1 · ngspice.**

1. Predict the RESET peak rise, the time to cool from a 500 K to a 125 K rise, and the SET plateau.
2. Run `ngspice -b pcm_thermal.cir` and compare (`dtreset`, `tquench`, `dtset`).
3. Halve `cth`. *Predict first:* what happens to the quench time and to the peak rise?

**Part 2 · MRAM thermal stability** (notebook). Plot the room-temperature $\Delta$ needed for 10-year retention against array size at 25, 85 and 150 °C (chapter Figure 1). Find the required $\Delta$ for a 1 Gb array at its operating temperature, and the room-temperature $\Delta$ that delivers it at 85 °C.

**Part 3 · Watching bits flip** (notebook). Simulate 10,000 bits with $\Delta$ = 25 for one second, drawing each bit's flip time from an exponential distribution, and compare the number of flips with $N t f_0 e^{-\Delta}$.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 23-08.a | RESET peak temperature rise | 600 | K |
| Lab 23-08.b | cooling time from a 500 K to a 125 K rise | 2.77 | ns |
| Lab 23-08.c | SET plateau temperature rise | 300 | K |
| Lab 23-08.d | Delta needed for 1 Gb, 10 years, at operating temperature | 61.1 | |
| Lab 23-08.e | room-temperature Delta for that at 85 °C | 73.4 | |
| Lab 23-08.f | expected flips, 10,000 bits at Delta 25 for 1 s | 139 | |

- Part 1: the peak and plateau match $PR_{th}$ within 0.1%, because the pulses last 25 and 75 thermal time constants. The cooling time matches $\tau\ln 4$. Halving $C_{th}$ halves the quench time but leaves the peaks unchanged.
- Part 3: the simulated count scatters around 139 by about its square root (Poisson statistics).

## Discussion

1. Why does the peak temperature not depend on $C_{th}$ for a 50 ns pulse?

   <details><summary>Answer</summary>

   The steady-state rise is $PR_{th}$; $C_{th}$ only sets how fast it is approached. A 50 ns pulse lasts 25 time constants, so the cell reaches steady state. $C_{th}$ matters for short pulses and for the quench.

   </details>

2. Why must the RESET pulse's fall be fast, and what limits it in a real circuit?

   <details><summary>Answer</summary>

   The melt must pass through the crystallization range faster than crystals can nucleate and grow. In the model the cooling is set by $\tau$ once the current stops; in a real circuit, the driver's fall time and the bitline's RC can slow the current's turn-off, so drivers are designed to cut current sharply.

   </details>

3. What does the thermal model leave out?

   <details><summary>Answer</summary>

   The cell's resistance changes with temperature and phase (the amorphous state switches to a conductive state above a threshold voltage), heat flows into the electrodes and neighbours with several time constants, and crystallization and melting absorb latent heat. Real cells are modelled with coupled electro-thermal and phase-field simulations.

   </details>

## Optional hardware

Evaluation boards for standalone MRAM and FeRAM parts are available from their makers. Writing a block, removing power, and reading it back after a bake in a laboratory oven (not a kitchen oven) is a simple, if slow, retention experiment. Respect the parts' rated storage temperature.
