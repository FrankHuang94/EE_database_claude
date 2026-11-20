# Term 3 Checkpoint · FE-Style Practice Exam

**Covers:** Courses 09–11 (semiconductor devices; Electronics I; signals and systems). **Questions:** 50 (multiple choice and numeric entry). **Time:** 150 minutes, the FE pace of about 3 minutes per question.
**Materials:** an FE-approved calculator and the *NCEES FE Reference Handbook* only (free PDF from NCEES); no course notes or sheets. Finding formulas in the handbook quickly is part of the practice.
**Scoring:** one point per question. Score each block separately and aim for at least 70% in every block. Write every miss into your error log with its cause, and re-solve it a week later. Solutions with full explanations, each pointing to the chapter to revisit, are in [solutions.md](solutions.md); open them only after you finish.

**Conventions:**

- For numeric entry, give 3 significant figures unless the question says otherwise.
- Silicon at 300 K: $V_T$ = 25.852 mV, $q$ = 1.602 × 10⁻¹⁹ C, $n_i$ = 1.0 × 10¹⁰ cm⁻³, $\varepsilon_s$ = 1.036 × 10⁻¹² F/cm, $\varepsilon_{ox}$ = 3.453 × 10⁻¹³ F/cm, $hc$ = 1.2398 eV·µm; full ionization.
- Diodes: 0.7 V constant drop unless stated. MOSFETs: square law $i_D = \tfrac12k_nV_{ov}^2$ in saturation, $k_n(V_{ov} - v_{DS}/2)v_{DS}$ in triode. BJTs: $g_m = I_C/V_T$, $r_\pi = \beta/g_m$.
- Op-amps: single-pole, closed-loop bandwidth = GBW/noise gain. Systems are causal and at rest unless stated; DT frequency ω is in rad/sample.

---

## Block 1 · Semiconductor devices (questions 1–16)

**1.** *Numeric entry.* Silicon is doped with $N_D$ = 10¹⁶ cm⁻³ donors. How far above the intrinsic level $E_i$ is the Fermi level, in eV?

**2.** A step junction has $N_A$ = 10¹⁷ cm⁻³ and $N_D$ = 10¹⁶ cm⁻³. Its built-in potential is:
(A) 0.753 V · (B) 0.714 V · (C) 0.774 V · (D) 0.833 V

**3.** *Numeric entry.* For the junction of question 2 at zero bias, find the total depletion width, in µm.

**4.** *Numeric entry.* n-type silicon with $N_D$ = 10¹⁶ cm⁻³ has electron mobility 1248 cm²/V·s. Find its resistivity, in Ω·cm.

**5.** The diffusion coefficient of electrons with mobility 1200 cm²/V·s at 300 K is:
(A) 31.0 cm²/s · (B) 3.10 cm²/s · (C) 46.5 cm²/s · (D) 1200 cm²/s

**6.** *Numeric entry.* Minority holes have $D_p$ = 12 cm²/s and lifetime 1 µs. Find their diffusion length, in µm.

**7.** For an ideal diode ($n$ = 1) at 300 K, the forward voltage change for a tenfold increase in current is:
(A) 25.9 mV · (B) 59.5 mV · (C) 119 mV · (D) 2.30 mV

**8.** *Numeric entry.* For the junction of question 2, by what factor does the depletion capacitance per area fall when the bias changes from 0 V to −5 V (reverse)? Give $C(-5\,\text{V})/C(0)$.

**9.** The oxide capacitance of a 2.0 nm SiO₂ gate dielectric is:
(A) 1.73 fF/µm² · (B) 17.3 fF/µm² · (C) 51.8 fF/µm² · (D) 5.18 fF/µm²

**10.** *Numeric entry.* For a p-type MOS body with $N_A$ = 10¹⁷ cm⁻³, find the surface potential at threshold, $2\phi_B$, in volts.

**11.** For the body of question 10, the maximum depletion width at threshold is:
(A) 0.104 µm · (B) 0.0734 µm · (C) 0.147 µm · (D) 1.04 µm

**12.** *Numeric entry.* A long-channel MOSFET has body factor $m$ = 1.3. Find its subthreshold swing at 300 K, in mV per decade.

**13.** A bipolar transistor has common-base current gain α = 0.995. Its common-emitter current gain β is:
(A) 0.995 · (B) 199 · (C) 200 · (D) 99.5

**14.** *Numeric entry.* Find the longest wavelength that silicon ($E_g$ = 1.12 eV) absorbs by band-to-band transitions, in µm.

**15.** The photon energy of an 850 nm infrared LED is:
(A) 1.46 eV · (B) 1.12 eV · (C) 0.685 eV · (D) 2.92 eV

**16.** *Numeric entry.* A gate delay of 10.0 ps is scaled by constant-field (Dennard) scaling with κ = 1.4. Find the new delay, in ps.

## Block 2 · Electronics I (questions 17–33)

**17.** A 5.0 V source drives a silicon diode through 2.2 kΩ. With the constant-drop model, the diode current is:
(A) 2.27 mA · (B) 1.95 mA · (C) 1.64 mA · (D) 2.59 mA

**18.** *Numeric entry.* Find a diode's small-signal resistance at 1.0 mA ($n$ = 1), in Ω.

**19.** A full-wave rectifier with peak output 15 V feeds 470 µF and a 1 kΩ load from 60 Hz mains. With the small-ripple approximation, the peak-to-peak ripple is:
(A) 0.532 V · (B) 0.266 V · (C) 0.133 V · (D) 2.66 V

**20.** *Numeric entry.* A 5.1 V Zener regulator is fed from a supply that can fall to 10 V. The load draws up to 30 mA and the Zener needs at least 2 mA. Find the largest series resistor, in Ω.

**21.** An NMOS transistor with $k_n$ = 4 mA/V² and $V_{TN}$ = 0.5 V has $V_{GS}$ = 1.0 V and $V_{DS}$ = 0.3 V. Its drain current is:
(A) 0.500 mA · (B) 0.420 mA · (C) 0.600 mA · (D) 0.240 mA

**22.** *Numeric entry.* Find the transconductance of an NMOS transistor with $k_n$ = 4 mA/V² at $I_D$ = 0.5 mA, in mA/V.

**23.** A BJT with β = 100 is biased at $I_C$ = 1.0 mA. Its $r_\pi$ is:
(A) 2.59 kΩ · (B) 25.9 kΩ · (C) 259 Ω · (D) 3.87 kΩ

**24.** *Numeric entry.* A common-source stage has $g_m$ = 2 mS, $R_D$ = 10 kΩ and $r_o$ = 50 kΩ, with no load. Find its voltage gain.

**25.** A common-emitter stage at $I_C$ = 1.0 mA has $R_C$ = 5.0 kΩ and an unbypassed emitter resistor of 500 Ω. With β large, its voltage gain is:
(A) −10.0 · (B) −9.51 · (C) −193 · (D) −0.951

**26.** *Numeric entry.* A source follower has $g_m$ = 2 mS and source resistance 2 kΩ (body effect and $r_o$ ignored). Find its voltage gain.

**27.** Two stages with open-circuit gains 20 and 15 are cascaded, and loading between them reduces the signal by a factor of 0.8. The overall gain is:
(A) 49.5 dB · (B) 47.6 dB · (C) 23.8 dB · (D) 240 dB

**28.** *Numeric entry.* A matched NMOS mirror with λ = 0.1 V⁻¹ has $I_{ref}$ = 100 µA, $V_{GS}$ = 0.8 V and output $V_{DS}$ = 2.0 V. Find the output current, in µA.

**29.** A non-inverting amplifier with $R_f$ = 99 kΩ and $R_g$ = 1 kΩ uses an op-amp with a gain–bandwidth product of 10 MHz. Its closed-loop bandwidth is:
(A) 100 kHz · (B) 10.0 MHz · (C) 1.00 kHz · (D) 101 kHz

**30.** *Numeric entry.* An op-amp slews at 6.5 V/µs. Find its full-power bandwidth for a 5.0 V peak output, in kHz.

**31.** An inverting amplifier with a gain of −10 uses an op-amp with 2.0 mV input offset voltage. The resulting output offset is:
(A) 2.00 mV · (B) 20.0 mV · (C) 22.0 mV · (D) 0.182 mV

**32.** *Numeric entry.* A unity-gain difference amplifier is built with 0.1% resistors. Find the worst-case lower bound on its CMRR, $(1 + K)/(4\varepsilon)$, in dB.

**33.** A non-inverting Schmitt trigger runs from a 5.0 V rail-to-rail supply with $R_1$ = 10 kΩ and $R_2$ = 100 kΩ. Its hysteresis is:
(A) 0.500 V · (B) 0.455 V · (C) 5.00 V · (D) 50.0 V

## Block 3 · Signals and systems (questions 34–50)

**34.** The fundamental period of $\cos(40\pi t) + \sin(60\pi t)$ is:
(A) 0.100 s · (B) 0.0500 s · (C) 0.0333 s · (D) 0.300 s

**35.** *Numeric entry.* $x[n] = \{1, 1, 1\}$ and $h[n] = \{1, 2\}$, both starting at $n = 0$. Find $y[1]$ of their convolution.

**36.** Which system is both linear and time-invariant?
(A) $y(t) = x(t - 2)$ · (B) $y(t) = x(2t)$ · (C) $y(t) = t\,x(t)$ · (D) $y(t) = x(t) + 1$

**37.** *Numeric entry.* For $y[n] = 0.8y[n - 1] + x[n]$ with $\lvert x[n]\rvert \le 1$, find the largest possible $\lvert y[n]\rvert$.

**38.** The third-harmonic amplitude of a ±2 V square wave with 50% duty cycle is:
(A) 0.849 V · (B) 0.424 V · (C) 2.55 V · (D) 0.283 V

**39.** *Numeric entry.* Find the 10–90% rise time of an RC low-pass filter with $R$ = 10 kΩ and $C$ = 10 nF, in µs.

**40.** The gain of the two-point average $y[n] = \tfrac12(x[n] + x[n - 1])$ at ω = π/2 is:
(A) 0.707 · (B) 0.500 · (C) 1.00 · (D) 0

**41.** *Numeric entry.* A 21-tap symmetric FIR filter runs at 48 kHz. Find its group delay, in µs.

**42.** $H(s) = 1/[(s + 2)(s - 1)]$. Which ROC gives a BIBO-stable system, and is that system causal?
(A) −2 < σ < 1; noncausal · (B) σ > 1; causal · (C) σ > −2; causal · (D) σ < −2; anticausal

**43.** *Numeric entry.* A second-order all-pole system has poles at $-3 \pm j4$. Find its step-response overshoot, in percent.

**44.** A causal digital filter has poles at $z$ = 0.5 and $z$ = −1.2. It is:
(A) stable, since one pole is inside the unit circle · (B) unstable; its impulse response alternates in sign and grows · (C) stable, since the poles' average is inside the circle · (D) marginally stable

**45.** *Numeric entry.* A digital resonator at $f_s$ = 8 kHz has its poles at radius 0.98. Estimate its −3 dB bandwidth, in Hz.

**46.** A 7 kHz tone is sampled at 10 kHz without filtering. It appears at:
(A) 3 kHz · (B) 7 kHz · (C) 17 kHz · (D) 2 kHz

**47.** *Numeric entry.* A signal is band-limited to 22 kHz. Find its Nyquist rate, in kHz.

**48.** The ideal signal-to-quantization-noise ratio of a 12-bit ADC for a full-scale sine is:
(A) 72.2 dB · (B) 74.0 dB · (C) 98.1 dB · (D) 68.0 dB

**49.** *Numeric entry.* A conventional AM transmitter is fully modulated ($m$ = 1) by a single tone. What percentage of its power is in the sidebands?

**50.** A superheterodyne AM receiver with a 455 kHz IF and high-side LO is tuned to 900 kHz. Its image frequency is:
(A) 1810 kHz · (B) 1355 kHz · (C) 445 kHz · (D) 2265 kHz
