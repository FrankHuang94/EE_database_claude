# Lab 22-07 · Converter Loops: a Type-III Buck, the Boost's RHP Zero and Slope Compensation

Chapter: [22-07 · Converter Dynamics and Control](../../chapters/22-07-converter-dynamics-and-control.md)

## Objective

- Close Example 22-07.3's voltage-mode loop in ngspice and measure its crossover and phase margin by Middlebrook injection.
- Measure an averaged boost's control-to-output response and see the right-half-plane zero's phase.
- Iterate the peak current-mode perturbation map with and without slope compensation.
- Compare the closed-loop output impedance with the $\Delta I/(2\pi f_cC)$ estimate.

## Background

`control.py` collects the chapter's results:

- plants: `buck_gvd`, `buck_zout`, `buck_f0_q`, `boost_gvd`, `boost_rhp_zero_hz`;
- compensation: `kfactor`, `type3`, `type3_components`, `crossover_and_pm`;
- current mode: `perturbation_ratio`;
- transients and delay: `droop`, `delay_phase_deg`.

The two netlists use averaged models, which have no switching and so run in AC analysis:

- `loop.cir` drives the buck's LC filter from the controlled source $V_g v_c/V_M$ and closes the loop through the type-III network of Example 22-07.3 around a high-gain op-amp. An AC source in series with the feedback path gives the loop gain $T = -\hat v_{out}/\hat v_{fb}$.
- `boost_avg.cir` replaces the boost's switch by the averaged voltage $(1 - d)v_{out}$ and its diode by the averaged current $(1 - d)i_L$, and applies a 1 V AC signal on $d$, so $\hat v_{out}$ is $G_{vd}$ directly.

## Procedure

1. **The buck loop.** *Predict* the crossover and phase margin of Example 22-07.3. Run `ngspice -b loop.cir` (Part 1), then vary $C_3$ by ±50% in the notebook.
2. **The boost.** *Predict* $|G_{vd}|$ at 1 kHz, and its magnitude and phase at the 275 kHz RHP zero. Run `ngspice -b boost_avg.cir` (Part 2).
3. **Slope compensation.** Iterate $\Delta i_{n+1} = \alpha\Delta i_n$ for Example 22-07.4 with $m_a$ = 0, $m_2/2$ and $m_2$ (Part 3).
4. **Output impedance.** Plot the closed-loop output impedance of Example 22-07.3 and compare its peak with $1/(2\pi f_cC)$ (Part 4).

## Expected results

- **Part 1.** The DC output is 1.200 V. The loop crosses over at 60.0 kHz with a 60.0° phase margin (Example 22-07.3).
- **Part 2.** The output is 5.000 V. $|G_{vd}|$ = **6.96** at 1 kHz (slightly above the DC value 6.94, because 1 kHz is already on the resonance's rising skirt). At 275 kHz, $|G_{vd}|$ = **0.0781** with a phase of **−224.5**°: the RHP zero has added −45° to the double pole's −180°, so the phase passes −180°, which no minimum-phase second-order plant can do.
- **Part 3.** Without compensation the perturbation grows by 1.94 per cycle and alternates in sign; with $m_a = m_2/2$ it shrinks by 0.49 per cycle; with $m_a = m_2$ it vanishes after one cycle.
- **Part 4.** The closed-loop output impedance peaks at **47.9** mΩ near **58.5** kHz, close to crossover and **13** % above the estimate $1/(2\pi \times 60\ \text{kHz} \times 62.5\ \mu\text{F})$ = **42.4** mΩ. Because this type-III loop has high gain at $f_0$, the LC resonance is suppressed and the capacitor estimate is a good first cut; Problem 22-07.12 shows a loop where it is not.

## Discussion

1. **Why is the phase margin exactly the design value?** The averaged netlist is the same linear model the design used; the measurement confirms the network values and the Middlebrook method, not the averaging itself. A switching simulation or bench measurement adds the modulator's sampling delay.
2. **Why measure loop gain by injection rather than by opening the loop?** Opening the loop removes the DC operating point that the integrator sets. Injecting a small AC signal in series keeps the loop closed at DC while revealing $T$ at each frequency.
3. **Why does slope compensation trade against current-mode benefits?** With $m_a \gg m_2$, the turn-off instant is set by the artificial ramp, not by the inductor current, so the loop behaves like voltage mode with its LC resonance back in the plant.

## Optional hardware

Many controller evaluation boards expose a small resistor in the feedback path for loop measurement. With a frequency-response analyzer (or a signal generator and two-channel oscilloscope at single frequencies), inject across that resistor and measure $T$; then change a compensation capacitor and watch the crossover and phase margin move.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 22-07.a | boost gain at 1 kHz | 6.96 | |
| Lab 22-07.b | boost gain at the RHP zero | 0.0781 | |
| Lab 22-07.c | boost phase at the RHP zero | −224.5 | ° |
| Lab 22-07.d | closed-loop output-impedance peak | 47.9 | mΩ |
| Lab 22-07.f | frequency of the peak | 58.5 | kHz |
| Lab 22-07.g | peak over the estimate | 13 | % |
| Lab 22-07.e | capacitor estimate at crossover | 42.4 | mΩ |
