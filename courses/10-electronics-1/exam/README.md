# Course 10 · Final Exam (Electronics I)

**Time limit:** 210 minutes.
**Allowed:** a scientific calculator, and the [Course 10 equation sheet](../../../reference/equation-sheets/10-electronics-1.md) printed without its chapter links. No notes, no Python, no simulator.

**Instructions.**

- Answer all 14 questions and show every step.
- Question 1 [A] is worth 5 points, each [B] 8 and Question 14 [C] 12: 113 points in total. 79 or more (about 70%) is a strong pass.
- Within a question the lettered parts carry equal weight.
- Give numerical answers to 3–4 significant figures, with units.
- Question 13 asks for derivations; Question 14 is a short-answer diligence question, graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These are the conventions of the chapters' problem sets.

- $V_T$ = 25.852 mV (300 K). Diodes: 0.7 V constant drop unless stated; small-signal resistance $V_T/I_D$.
- MOSFETs: square law $i_D = \tfrac12k_n(v_{GS} - V_{TN})^2$ in saturation, $g_m = \sqrt{2k_nI_D}$, $r_o = 1/(\lambda I_D)$, $g_{mb} = \chi g_m$.
- BJTs: $V_{BE}$ = 0.7 V for bias; $g_m = I_C/V_T$, $r_\pi = \beta/g_m$, $r_e = \alpha/g_m$, $r_o = V_A/I_C$.
- Capacitors are short circuits at signal frequencies; $r_o$ is ignored unless $V_A$ or λ is given.
- Op-amps: single-pole, gain error ≈ noise gain/$A_0$, bandwidth GBW/noise gain.

---

**1 [A] · Diode models.** (10-01)
A 3 V source drives a silicon diode through 1 kΩ.
(a) Find the diode current with the constant-drop model.
(b) Find the diode's small-signal resistance at that current.

**2 [B] · A power supply.** (10-01)
A transformer delivers 12 V rms at 60 Hz to a full-wave bridge (two 0.7 V drops conduct at a time) with a 1000 µF reservoir capacitor and a 500 Ω load.
(a) Find the transformer's peak voltage and the peak output voltage.
(b) Find the peak-to-peak ripple with the small-ripple approximation.
(c) Find the average output voltage and the load current.

**3 [B] · A Zener regulator.** (10-01)
A 5.1 V Zener regulator is fed from 9 V ± 1 V. The load draws 0 to 20 mA, and the Zener needs at least 1 mA.
(a) Find the series resistor.
(b) Find the largest Zener current and the Zener's largest dissipation.

**4 [B] · MOSFET bias.** (10-02)
An NMOS ($k_n$ = 2 mA/V², $V_{TN}$ = 0.5 V, λ = 0) has its gate held at 3 V by a divider, $R_S$ = 2 kΩ and $R_D$ = 3 kΩ from $V_{DD}$ = 9 V.
(a) Find $V_{ov}$, $V_{GS}$ and $I_D$.
(b) Find $V_D$, $V_S$ and $V_{DS}$, and confirm the region.
(c) If $V_{TN}$ rises by 50 mV, find the new current and its change in percent.

**5 [B] · BJT bias.** (10-03)
A four-resistor bias has $V_{CC}$ = 10 V, $R_1$ = 33 kΩ, $R_2$ = 10 kΩ, $R_E$ = 1 kΩ, $R_C$ = 3.3 kΩ and β = 120.
(a) Find the Thévenin equivalent of the divider.
(b) Find $I_E$ and $I_C$.
(c) Find $V_C$, $V_E$ and $V_{CE}$, and confirm the region.

**6 [B] · Small-signal parameters.** (10-04)
(a) For the BJT of Question 5 with $V_A$ = 80 V, find $g_m$, $r_\pi$, $r_o$ and the intrinsic gain.
(b) For the MOSFET of Question 4 with λ = 0.05 V⁻¹, find $g_m$, $r_o$ and the intrinsic gain.
(c) Compare the two devices' $g_m/I$, and explain the difference in one sentence.

**7 [B] · Loading and cascades.** (10-05)
A source with $R_{sig}$ = 5 kΩ drives a stage A ($R_i$ = 20 kΩ, $A_{vo}$ = −40, $R_o$ = 4 kΩ) that must drive a 1 kΩ load.
(a) Find the overall gain with A driving the load directly, in V/V and dB.
(b) An emitter follower ($R_i$ = 200 kΩ, $A_{vo}$ = 0.98, $R_o$ = 50 Ω) is inserted between A and the load. Find the overall gain in V/V and dB.

**8 [B] · MOS amplifiers.** (10-06)
Use the MOSFET of Questions 4 and 6(b).
(a) With $R_S$ bypassed and a 10 kΩ load coupled to the drain, find the gain including $r_o$.
(b) With $R_S$ unbypassed (ignore $r_o$), find the gain into the same load.
(c) The same transistor, biased by an ideal current source, is used as a source follower with χ = 0.2 ($r_o$ ignored). Find its output resistance and its largest possible gain.

**9 [B] · BJT amplifiers.** (10-07)
Use the bias of Questions 5 and 6(a), with $R_E$ fully bypassed, a 1 kΩ source and a 10 kΩ load coupled to the collector.
(a) Find the input resistance, the input factor, the gain from the base (including $r_o$) and the overall gain.
(b) Now leave 100 Ω of $R_E$ unbypassed ($r_o$ ignored). Find $r_e$, the input resistance at the base and of the stage, the gain from the base and the overall gain.

**10 [B] · Current mirrors.** (10-08)
NMOS mirror transistors carry 100 µA with $g_m$ = 1 mS, $r_o$ = 50 kΩ, $V_{TN}$ = 0.45 V and $V_{ov}$ = 0.2 V.
(a) Find the output resistance of a basic mirror and of a cascode mirror.
(b) Find the compliance of the basic, simple cascode and low-voltage cascode mirrors.
(c) With $A_{VT}$ = 3.5 mV·µm and $WL$ = 20 µm², find σ(ΔI/I). What area gives σ = 0.2%?

**11 [B] · Real op-amps.** (10-09)
A non-inverting amplifier of gain 20 uses an op-amp with $A_0$ = 100 dB, GBW = 5 MHz, SR = 2 V/µs and $V_{OS}$ = 0.5 mV.
(a) Find the exact DC gain and its error.
(b) Find the closed-loop bandwidth and the full-power bandwidth for a 3 V peak output.
(c) Find the output error due to offset.

**12 [B] · Applications.** (10-10)
(a) A non-inverting Schmitt trigger on 3.3 V has $V_{ref}$ = 1.65 V and $R_2$ = 100 kΩ. Find $R_1$ for 50 mV of hysteresis, and the thresholds.
(b) A photodiode TIA has $R_F$ = 200 kΩ, $C_{in}$ = 10 pF and an op-amp of GBW 20 MHz. Find $f_0$ and $Q$ without a feedback capacitor, the $C_F$ that makes $Q = 1/\sqrt2$, and the resulting bandwidth.

**13 [B] · Derivations.** (10-04, 10-06, 10-07)
(a) From $i_C = I_Se^{v_{BE}/V_T}$ and $i_B = i_C/\beta$, derive $g_m$, $r_\pi$ and $r_e$, and show $r_\pi = (\beta + 1)r_e$.
(b) Derive the gain of a source follower with body effect, $r_o$ and load $R_S$, and show that it cannot exceed $1/(1 + \chi)$.
(c) Using the T model, derive the gain of a common-emitter stage with an unbypassed $R_E$, and explain why it becomes nearly independent of β and of the bias current when $R_E \gg r_e$.

**14 [C] · Diligence.** (all chapters)
A start-up pitches a biopotential (ECG) front-end chip for patches: "a single-stage amplifier with a gain of 1000, 120 dB CMRR, 1 µV offset, all at 5 µW from a 1.2 V supply." Using this course's results:
(a) Find the total current budget, and the largest $g_m$ each of two input transistors could have if they share it equally (weak inversion, $n$ = 1.3).
(b) Identify at least four claims that need evidence or are inconsistent with device or circuit limits, and say what you would ask for each.
(c) Name two architectural features you would expect in a credible design.

---

[Solutions](solutions.md)
