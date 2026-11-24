# Lab 20-05 · Sampling Noise, Switch Distortion, Jitter and Latch Regeneration

Chapter: [20-05 · Comparators and Sample-and-Hold Circuits](../../chapters/20-05-comparators-and-sample-and-hold.md)

## Objective

- Confirm in ngspice that the noise sampled on a capacitor is $kT/C$ whatever the resistance.
- See why a plain NMOS switch fails at 1.2 V and how bootstrapping fixes it.
- Simulate the bootstrapped switch's tracking distortion, with and without the body effect, and confirm it in ngspice.
- Build the full SNR budget against input frequency for several jitter values.
- Simulate a current-limited latch and compare its decision time with the exponential estimate.

## Background

The running design is the front end of a 12-bit, 100 MS/s differential SAR ADC in T130 with $V_{DD}$ = 1.2 V: 0.651 pF per side, a bootstrapped NMOS switch 0.888 µm wide (body at ground), and a StrongARM comparator with $A_{int}$ = 6.75. The switch follows the symmetric triode law $I = K(V_G - V_{TH}(v_m) - v_m)(v_a - v_b)$ with a body-effect threshold (chapter §3.3). The latch is two cross-coupled transconductors $i = I_{max}\tanh(-g_mv/I_{max})$ loading 60 fF each, with $g_m$ = 3 mS and $I_{max}$ = 0.3 mA, so τ = 20 ps.

Files:

- `sh.py`: the threshold with body effect (`vth`), on-resistance (`ron`), capacitor sizing (`ktc_cap`), the SNR budget (`snr_db`, `jitter_snr_db`), the tracking simulation (`track`), the StrongARM model (`strongarm`), decision time and metastability (`decision_time`, `meta_vmin`, `sar_meta_probability`), and the current-limited latch (`regen`).
- `ktc.cir`: RC noise analysis for $R$ = 100 Ω and 10 kΩ with 0.651 pF, and 1 kΩ with 1 pF.
- `switch.cir`: the bootstrapped switch at 49 MHz with the body grounded and tied to the source.
- `latch.cir`: the current-limited latch from three initial imbalances.
- `20-05-sampling-lab.ipynb`: the procedure below.

## Procedure

1. **kT/C.** Predict the integrated noise for $R$ = 100 Ω and 10 kΩ with 0.651 pF. Run `ngspice -b ktc.cir` (Part 1).
2. **On-resistance.** Plot $R_{on}$ against the input from 0.1 to 1.1 V for the plain and bootstrapped switches, and mark the 852 Ω target (Part 2).
3. **Tracking distortion.** Predict HD2 and HD3 at 49 MHz from the chapter's estimates, simulate both body connections, and run `ngspice -b switch.cir` (Part 3).
4. **SNR budget.** Plot the total SNR from 1 MHz to 1 GHz for 0.1, 0.3 and 1 ps of jitter, with the quantization and kT/C floor (Part 4).
5. **Regeneration.** Predict the decision time for half an LSB from $\tau\ln(V_L/v_0)$. Simulate the latch for inputs of half an LSB, 1 mV and 10 mV, and run `ngspice -b latch.cir` (Part 5).

## Expected results

- **Part 1.** 79.7 µV for both resistances and 64.4 µV for 1 pF (Example 20-05.1 and §3.2).
- **Part 2.** The plain switch's resistance rises steeply and it turns off at 0.63 V; the bootstrapped switch stays between 687 and 852 Ω (Example 20-05.2).
- **Part 3.** HD2 −41.5 dBc and HD3 −64.4 dBc with the body grounded; HD3 −83.1 dBc with the body tied to the source (Example 20-05.4). ngspice agrees to a few thousandths of a decibel.
- **Part 4.** At low frequency the SNR sits at the 71.0 dB floor. It is 3 dB below the floor where the jitter noise equals the other two, at **44.9** MHz for 1 ps (ten times higher for 0.1 ps), and falls 20 dB per decade beyond.
- **Part 5.** The current-limited latch takes **146.5** ps for half an LSB, **113.9** ps for 1 mV and **67.4** ps for 10 mV, against exponential estimates of 122 ps, **89.7** ps and **43.7** ps. The difference, about **24** ps in every case, is the time spent near the rails, where the transconductors saturate and the growth becomes linear.

## Discussion

1. **Why does the resistance not matter for kT/C, but matter for everything else?** It sets the noise bandwidth and the noise density in exactly compensating ways (§3.2). It still sets settling, distortion and charge injection.
2. **Where does the constant 24 ps come from?** Once the per-side swing exceeds about $I_{max}/g_m$ = 0.1 V, each transconductor delivers its maximum current, so the last part of the swing is a fixed slew, the same for every input. Only the exponential part depends on the input.
3. **Is the switch model complete?** It omits charge injection at turn-off, the gate's parasitic capacitance (charge sharing, Problem 20-05.4), and the sampling instant's own dependence on the input (the switch turns off when $V_{GS}$ crosses $V_{TH}$, which itself moves with the input). Each adds error; the last one is a signal-dependent aperture delay.

## Optional hardware

A CD4066-style analog switch, a 1 nF capacitor and an oscilloscope show charge injection directly: switch a DC input on and off and watch the held voltage step as the switch opens. Vary the input from the bottom to the top of the supply to see the step change with the signal. An audio-band ADC evaluation board driven from a low-noise generator shows the jitter law if you can change its clock source: compare the SNR at a low and a high input frequency.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 20-05.a | simulated decision time, half an LSB | 146.5 | ps |
| Lab 20-05.b | simulated decision time, 1 mV | 113.9 | ps |
| Lab 20-05.c | simulated decision time, 10 mV | 67.4 | ps |
| Lab 20-05.d | exponential estimate, 1 mV | 89.7 | ps |
| Lab 20-05.e | exponential estimate, 10 mV | 43.7 | ps |
| Lab 20-05.f | extra time near the rails | 24 | ps |
| Lab 20-05.g | linear range per side | 0.1 | V |
| Lab 20-05.h | 3 dB jitter knee for 1 ps | 44.9 | MHz |
