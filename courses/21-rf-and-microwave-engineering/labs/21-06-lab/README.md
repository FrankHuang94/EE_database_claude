# Lab 21-06 · Oscillators and VCOs: Amplitude, ISF, Phase-Noise Budgets, Tuning, Quadrature and Injection Locking

Chapter: [21-06 · Oscillators and VCOs](../../chapters/21-06-oscillators-and-vcos.md)

## Objective

- Predict an LC oscillator's amplitude by the describing function and confirm it, and the Groszkowski frequency shift, in ngspice.
- Measure the impulse sensitivity function by kicking a simulated oscillator at different phases.
- Build a phase-noise budget from the tank, the transistors, the flicker corner and the tuning line.
- Map a capacitor-bank VCO's bands and its $K_{VCO}$ spread.
- Compute an RC-CR network's image rejection across a band and with process spread, and confirm the network in ngspice.
- Watch injection locking and pulling, and compare the beat frequency with Adler's equation.

## Background

`vco.py` holds the closed forms of the chapter: `tank`, `describing_function`, `amplitude_df` and `amplitude_hard`; `isf_phase_noise`, `leeson`, `fom`, `control_noise_pn`, `fm_spur_dbc` and `rms_phase_one_pole`; `freq` for the tuning plan; `irr_db`, `rc_cr` and `div2_phase_error_deg` for quadrature; `lock_range` and `beat` for injection. It also integrates a normalized oscillator ($L = C = 1$, $R_p = Q$, so $\omega_0 = 1$) driven by $i = I_0\tanh(v/V_0)$: `settle`, `isf` (charge kicks), `free_running_shift`, `groszkowski_shift` and `injection_beat`.

`vco.cir` models the oscillator of Example 21-06.1 (1 nH, 1.0132 pF, 362.49 Ω, a tanh current source for a bipolar pair with a 2 mA tail) twice: free-running, and with a 10% injected current at 5.010 GHz. `polyphase.cir` is an RC-CR network centred at 2.45 GHz, analysed at 2.40 GHz.

## Procedure

1. **Amplitude and frequency.** *Predict* the amplitude from $(4/\pi)I_0R_p$ and from the describing function, and the frequency from $1/(2\pi\sqrt{LC})$. Run `ngspice -b vco.cir` and compare; then compute the Groszkowski shift from the harmonic currents (Part 1).
2. **ISF.** *Predict* the phase shift per unit charge at 0°, 90°, 180° and 270°. Kick the normalized oscillator at 16 phases, plot $\Gamma(\theta)$ against $-\sin\theta$, and compute $\Gamma_{rms}$ and $\Gamma_{dc}$; repeat at Q = 50 (Part 2).
3. **Phase-noise budget.** *Predict* the total at 1 MHz from the tank and devices (Example 21-06.2, $F$ = 2) and from a 1 kΩ resistor on a 400 MHz/V tuning line (Example 21-06.4). Plot each contribution from 1 kHz to 10 MHz with the devices' 22.5 kHz flicker corner, which makes the total's corner 11.25 kHz because the tank resistor has no 1/f noise (Part 3).
4. **Band map.** *Predict* how $K_{VCO}$ changes from code 0 to code 7 in Example 21-06.3, then plot all eight bands (Part 4).
5. **Quadrature.** *Predict* the worst IRR of the RC-CR network over 2.40–2.50 GHz with RC at ±10% of nominal; sweep it, and run `ngspice -b polyphase.cir` (Part 5).
6. **Injection.** *Predict* whether injection at 0.9 and at 2 lock ranges (Q = 10, 5% injection, measured from the free-running frequency) locks, and the beat frequency if not. Simulate and plot the relative phase (Part 6).

## Expected results

- **Part 1.** Hard limit 0.4615 V, describing function 0.4591 V; ngspice agrees with the describing function to better than 0.1%. The frequency is not 5 GHz but about 4.9968 GHz: the harmonics' Groszkowski shift of −0.064%, which ngspice reproduces to a few parts in 10⁵.
- **Part 2.** $\Gamma(\theta)$ follows $-\sin\theta$: $\Gamma_{rms}$ within about 2% of 0.707 and $\Gamma_{dc}$ near zero at Q = 11.5; the small departures (a few per cent at the zero crossings, a small non-zero value at the peaks) come from the waveform's harmonics and amplitude-to-phase conversion, and shrink at Q = 50.
- **Part 3.** −115.73 dBc/Hz (tank and devices) and −118.78 dBc/Hz (tuning line) add to **−113.98** dBc/Hz at 1 MHz; both fall at 20 dB per decade, so the sum at 100 kHz is **−93.98** dBc/Hz before the flicker corner adds its share. Cutting $K_{VCO}$ to 50 MHz/V removes almost all of the tuning-line term.
- **Part 4.** Eight overlapping bands from 4.224 to 5.459 GHz, with $K_{VCO}$ falling from 426 to 242 MHz/V.
- **Part 5.** At the nominal RC the band edges give 39.7 and 39.9 dB. The worst corner of the ±10% spread is RC 10% low at 2.40 GHz, **24.03** dB; RC 10% high at 2.50 GHz gives **24.78** dB. ngspice gives −0.1791 dB and exactly 90° at 2.40 GHz.
- **Part 6.** The normalized lock range is **2.503 × 10⁻³** (Q = 10, 5%). At 0.9 lock ranges the relative phase settles: locked. At 2 lock ranges it slips steadily at about the predicted beat of **4.336 × 10⁻³**, within a few per cent.

## Discussion

1. **Why must detuning be measured from the actual free-running frequency?** The lock range is a few times $10^{-3}$ of $\omega_0$ here, and the Groszkowski shift is of the same order; measured from $1/\sqrt{LC}$, an injection inside the lock range can appear outside it.
2. **Why is the simulated ISF not exactly $-\sin\theta$?** The oscillator's state does not move on a perfect circle (the voltage has harmonics), and amplitude perturbations change the frequency slightly while they decay (AM-to-PM conversion). Both effects scale with 1/Q.
3. **Why does a capacitor bank's $K_{VCO}$ fall in the lower bands?** $K_{VCO} = (f/2C_{tot})\,dC/dV$, and both $f$ and $1/C_{tot}$ fall as the bank adds capacitance, giving $C_{tot}^{-3/2}$.

## Optional hardware

A discrete LC oscillator is easy to build at a few megahertz: a cross-coupled pair of small-signal transistors, a hand-wound inductor and a varactor diode. With an oscilloscope, measure the amplitude against tail current to find the current-limited and voltage-limited regimes. With a spectrum analyzer, inject a weak tone from a signal generator through a small capacitor and watch the oscillator's line jump to the injected frequency inside the lock range, and the pulled, beating spectrum just outside it.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 21-06.a | budget, tank + devices + tuning line, 1 MHz | −113.98 | dBc/Hz |
| Lab 21-06.b | budget at 100 kHz, before flicker | −93.98 | dBc/Hz |
| Lab 21-06.c | worst IRR over band and ±10% RC | 24.03 | dB |
| Lab 21-06.d | IRR, RC 10% high, 2.50 GHz | 24.78 | dB |
| Lab 21-06.e | normalized lock range, Q = 10, 5% | 2.503e-3 | |
| Lab 21-06.f | predicted normalized beat at 2 lock ranges | 4.336e-3 | |
