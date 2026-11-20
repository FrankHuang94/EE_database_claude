# Course 12 · Final Exam (Electronics II)

**Time limit:** 210 minutes.
**Allowed:** a scientific calculator, and the [Course 12 equation sheet](../../../reference/equation-sheets/12-electronics-2.md) printed without its chapter links. No notes, no Python, no simulator.

**Instructions.**

- Answer all 14 questions and show every step.
- Question 1 [A] is worth 5 points, each [B] 8, and Questions 13 and 14 [C] 12 each: 117 points in total. 82 or more (about 70%) is a strong pass.
- Within a question the lettered parts carry equal weight.
- Give numerical answers to 3–4 significant figures, with units.
- Question 13 asks for derivations; Question 14 is a short-answer diligence question, graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These are the conventions of the chapters' problem sets.

- Square-law MOSFETs: $I_D = (k/2)V_{ov}^2$, $g_m = \sqrt{2kI_D} = 2I_D/V_{ov}$, $r_o = 1/(\lambda I_D)$; bipolar $g_m = I_C/V_T$ with $V_T$ = 25.852 mV; $T$ = 300 K for noise, $k$ = 1.380649 × 10⁻²³ J/K.
- Loop gains $T$ are positive for negative feedback; phase margin is $180^\circ + \angle T$ at $\lvert T\rvert = 1$, with unwrapped phase.
- Noise densities are one-sided; uncorrelated sources add in power.

---

**1 [A] · A MOS differential pair.** (12-01)
An NMOS pair has $k$ = 2 mA/V² per device, tail current $I_{SS}$ = 200 µA with output resistance $R_{SS}$ = 100 kΩ, and drain resistors $R_D$ = 10 kΩ.
(a) Find $g_m$ and the differential-output gain.
(b) Find the single-ended differential gain, the single-ended common-mode gain and the CMRR in decibels.
(c) Find the differential input at which the pair fully switches.

**2 [B] · Active loads and cascodes.** (12-02)
All devices have $g_m$ = 1 mA/V and $r_o$ = 100 kΩ.
(a) Find the gain of a five-transistor OTA (input pair with a current-mirror load).
(b) A telescopic cascode replaces it, with cascoded input devices and a cascoded load. Find each side's output resistance, the total output resistance and the gain.

**3 [B] · A common-source stage's frequency response.** (12-03)
$g_m$ = 2 mA/V, $R_S$ = 10 kΩ, $R_L$ = 5 kΩ, $C_{gs}$ = 100 fF, $C_{gd}$ = 20 fF, $C_L$ = 100 fF.
(a) Find the midband gain and the Miller input capacitance, and the input-pole estimate.
(b) Find the output-pole estimate (with $C_{gd}$'s output-side Miller capacitance) and the right-half-plane zero.
(c) The exact −3 dB frequency is 44.01 MHz. Which estimate is closer, and why is the input-pole estimate high?

**4 [B] · Open-circuit time constants.** (12-04)
For Question 3's stage, find the resistance seen by $C_{gd}$, the sum of open-circuit time constants $b_1$, the bandwidth estimate $1/(2\pi b_1)$, and $C_{gd}$'s share of $b_1$.

**5 [B] · Feedback.** (12-05)
A voltage amplifier with $A$ = 2000, input resistance 10 kΩ, output resistance 1 kΩ and a single pole at 50 kHz is placed in a series–shunt loop with β = 0.05.
(a) Find the loop gain and closed-loop gain.
(b) Estimate the closed-loop input and output resistances and the closed-loop bandwidth.

**6 [B] · Phase margin.** (12-06)
A loop gain has $T_0$ = 500 and poles at 10 kHz and 8 MHz.
(a) Find $f_u = T_0f_1$, the ratio $r = f_2/f_u$, and the exact crossover and phase margin.
(b) Using the two-pole model, find the closed-loop $Q$ and step overshoot.

**7 [B] · Miller compensation.** (12-06)
A two-stage amplifier has $g_{m1}$ = 0.4 mA/V, $g_{m2}$ = 4 mA/V and $C_L$ = 3 pF.
(a) Using the rules of 12-06, find $C_c$, the GBW, $p_2$ and the right-half-plane zero.
(b) Find the nulling resistor that removes the zero, and the one that cancels $p_2$.

**8 [B] · A class B output stage.** (12-07)
±12 V supplies, an 8 Ω load.
(a) Find the maximum output power, the supply power at full output and the efficiency.
(b) Find the amplitude of worst-case dissipation, the total and per-transistor dissipation there, and the largest $\theta_{SA}$ that keeps $T_J \le$ 125 °C at 50 °C ambient with $\theta_{JC} + \theta_{CS}$ = 3 °C/W.

**9 [B] · Op-amp slew rate.** (12-08)
A two-stage CMOS op-amp has $I_{SS}$ = 40 µA, input overdrive 0.2 V, $C_c$ = 2 pF, second-stage current $I_7$ = 150 µA and $C_L$ = 8 pF.
(a) Find $g_{m1}$ and the GBW.
(b) Find the internal and output-stage slew limits, the rising and falling slew rates, and the full-power bandwidth at 2 V peak.

**10 [B] · Oscillators.** (12-09)
(a) A Colpitts oscillator has $L$ = 4.7 µH, $C_1$ = 1 nF, $C_2$ = 4 nF and a 1.5 kΩ drain load. Find its frequency and minimum $g_m$.
(b) A nine-stage ring oscillator has 25 ps per stage. Find its frequency.

**11 [B] · Amplifier noise.** (12-10)
(a) A common-source stage has $g_m$ = 10 mA/V, γ = 2/3 and $R_D$ = 1 kΩ. Find its equivalent noise resistance and input noise density, and the RMS input noise over 1 MHz.
(b) Find the kT/C noise of a 2 pF sampling capacitor.

**12 [B] · Noise figure.** (12-10)
An amplifier has $e_n$ = 3 nV/√Hz and $i_n$ = 0.5 pA/√Hz.
(a) Find its noise factor and noise figure from a 1 kΩ source.
(b) Find its optimum source resistance and minimum noise figure.

**13 [C] · Derivations.**
(a) A circuit has one controlled source $Px$. With the source replaced by an independent source $s_c$ and input $u$, the output and controlling variable are $y = au + bs_c$ and $x = cu + ds_c$. Derive the closed-loop gain and show it equals $A_\infty T/(1 + T) + A_{\mathrm{dir}}/(1 + T)$, defining $T$, $A_\infty$ and $A_{\mathrm{dir}}$.
(b) Derive the maximum efficiency of a class B stage and the output amplitude at which its transistors dissipate the most.
(c) Derive the RMS noise voltage on the capacitor of an RC low-pass driven by the resistor's thermal noise, and explain why it does not depend on $R$.

**14 [C] · Diligence: "0.5 nV/√Hz at 1 µA".**
A start-up pitches a sensor amplifier for wearables with "0.5 nV/√Hz input noise at 1 µA total supply current, rail-to-rail inputs, and a 1 MHz bandwidth".
(a) For an ideal bipolar input transistor at 1 µA, find $g_m$ and the minimum input noise density (collector shot noise only). How far, as a power ratio, is the claim from it, and what current would a single transistor need to reach 0.5 nV/√Hz?
(b) Name two other ways the claim could be technically true but misleading, and the question you would ask to expose each.
(c) What three specifications would you ask for before believing any input-noise number?
