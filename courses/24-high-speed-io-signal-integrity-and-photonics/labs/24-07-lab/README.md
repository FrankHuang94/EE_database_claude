# Lab 24-07 · TIA, Dispersion, Modulators and Sensitivity

**Objective.** Confirm a shunt-feedback TIA's transimpedance and bandwidth in ngspice; propagate a pulse through dispersive fiber and compare with the analytic broadening; explore Mach–Zehnder and ring transfer functions; and plot BER against received optical power.

**Chapter:** [24-07 · Photonics Fundamentals](../../chapters/24-07-photonics-fundamentals.md)

## Background

§3.2 gave dispersion-induced spreading $D L\Delta\lambda$. For a Gaussian pulse of 1/e intensity half-width $T_0$, the exact result is a width growing by $\sqrt{1 + (L/L_D)^2}$ with dispersion length $L_D = T_0^2/\lvert\beta_2\rvert$ and $\beta_2 = -D\lambda^2/2\pi c$. §3.4 derived the MZM's $\cos^2(\Delta\phi/2)$ and the ring's resonance shift, §3.5 the sensitivity $Q\sigma/\mathcal R$ and its penalties, and §3.6 the TIA's $Z_T$ and bandwidth $(1 + A)/2\pi R_FC_{in}$.

## Files

- `tia.cir`: Example 24-07.9's TIA, an ideal gain-of-10 inverting amplifier with 1 kΩ feedback and 100 fF of input capacitance.
- `optics.py`: responsivity and dBm conversions, fiber delay, dispersion and an FFT pulse propagator, MZM and ring transfer functions, OOK and PAM4 BER against power, penalties, WDM spacing, TIA formulas.
- `24-07-optics-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · TIA** (ngspice and notebook). *Predict* the transimpedance and bandwidth, run `ngspice -b tia.cir`, then double $R_F$ in the notebook's formulas and predict again.

**Part 2 · Dispersion** (notebook). Propagate a Gaussian pulse with $T_0$ = 5 ps through 2 km of fiber at 1550 nm ($D$ = 18) and at 1310 nm ($D$ = 3.5). *Predict* each broadening factor, then compare the FFT result with $\sqrt{1 + (L/L_D)^2}$.

**Part 3 · Modulators** (notebook). Plot the MZM transfer curve with a half-$V_\pi$ drive and the ring's notch at 0, 1 and 2.3 K of heating. *Predict* the extinction ratio and how far the notch moves.

**Part 4 · Sensitivity** (notebook). Plot BER against average received power for OOK and PAM4 with Example 24-07.7's receiver. *Predict* the power for 10⁻¹² in each.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 24-07.a | TIA transimpedance | 909 | Ω |
| Lab 24-07.b | TIA bandwidth | 17.5 | GHz |
| Lab 24-07.c | TIA bandwidth with 2 kohm | 8.75 | GHz |
| Lab 24-07.d | broadening factor at 1550 nm | 2.09 | |
| Lab 24-07.e | broadening factor at 1310 nm | 1.032 | |
| Lab 24-07.f | dispersion length at 1550 nm | 1.09 | km |
| Lab 24-07.g | MZM extinction ratio, half-Vpi drive | 7.66 | dB |
| Lab 24-07.h | ring shift for 2.3 K | 0.129 | nm |
| Lab 24-07.i | OOK power for 1e-12 | -15.7 | dBm |
| Lab 24-07.j | PAM4 power for 1e-12 | -10.9 | dBm |
| Lab 24-07.k | PAM4 minus OOK at 1e-12 | 4.75 | dB |

- Part 1: ngspice gives 909 Ω and 17.5 GHz, as the formulas predict; doubling $R_F$ halves the bandwidth to 8.75 GHz while halving the resistor's noise power.
- Part 2: at 1550 nm the pulse broadens by 2.09 over 2 km (the dispersion length is 1.09 km); at 1310 nm by only 1.032. The FFT propagation matches the analytic factor to many digits.
- Part 3: a half-$V_\pi$ drive at quadrature gives 7.66 dB of extinction; 2.3 K moves the ring's notch 0.129 nm, one linewidth.
- Part 4: OOK reaches 10⁻¹² at −15.7 dBm and PAM4 at −10.9 dBm, 4.75 dB apart: a hair less than the 4.77 dB eye ratio, because PAM4's BER is three quarters of its symbol-error probability.

## Discussion

1. Why does the pulse broaden less than the simple $DL\Delta\lambda$ estimate suggests at 1310 nm, but about as much at 1550 nm?

   <details><summary>Answer</summary>

   Spreading adds roughly in quadrature to the original width. When $DL\Delta\lambda$ is small against $T_0$ (1310 nm) the width barely grows; when it is comparable or larger (1550 nm) it dominates.

   </details>

2. Why does doubling $R_F$ help sensitivity even though it halves the bandwidth?

   <details><summary>Answer</summary>

   The resistor's noise current density falls as $1/\sqrt{R_F}$; if the link can tolerate the lower bandwidth (for example with equalization after the TIA), the total noise falls. If it cannot, the ISI from too little bandwidth costs more than the noise saved.

   </details>

3. What would a 3 dB extinction ratio do to Part 4's curves?

   <details><summary>Answer</summary>

   It shifts them right by $10\log_{10}((ER + 1)/(ER - 1))$ with $ER$ = 2, that is 4.77 dB, as much as going from OOK to PAM4.

   </details>

## Optional hardware

An SFP+ or QSFP evaluation board with a variable optical attenuator and a bit-error-rate tester reproduces Part 4: sweep the attenuation and record BER against received power to find the module's sensitivity and the shape of its waterfall curve.
