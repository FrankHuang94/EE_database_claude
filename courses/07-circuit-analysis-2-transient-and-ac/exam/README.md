# Course 07 · Final Exam (Circuit Analysis II, Transient and AC)

**Time limit:** 210 minutes.
**Allowed:** a scientific calculator, and the [Course 07 equation sheet](../../../reference/equation-sheets/07-circuit-analysis-2-transient-and-ac.md) printed without its chapter links. No notes, no Python, no simulator.

**Instructions.**

- Answer all 15 questions and show every step.
- Each [A] is worth 5 points, each [B] 8 and each [C] 12: 122 points in total. 85 or more (about 70%) is a strong pass.
- Within a question the lettered parts carry equal weight, unless the question says otherwise.
- Questions 5, 13 and 14 ask for short derivations. Show the reasoning, not just the formula.
- Give numerical answers to 4 significant figures unless told otherwise, with units and signs.
- Question 15 is a short-answer diligence question, graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.**

- Passive sign convention throughout.
- Circuits are given as element lists: "R1, node 1 to node 2, 2 kΩ" places a resistor between those nodes, and node 0 is ground. For a source, the first node named is its + terminal.
- Sinusoids are cosines. A phasor $\mathbf{V}$ is the peak amplitude and phase, so the average power is $\tfrac12\operatorname{Re}(\mathbf{V}\mathbf{I}^*)$, unless a quantity is labeled RMS. Mains and three-phase voltages and currents are RMS, as power engineers quote them.
- Three-phase supplies have positive sequence (a, b, c).
- S-parameters use a 50 Ω reference.
- Op-amps are ideal unless a non-ideality is given.

---

**1 [A] · Storage elements.**
(a) The voltage across a 10 µF capacitor rises linearly from 0 to 5 V in 2 ms. Find its current.
(b) The current in a 100 µH inductor rises linearly from 0 to 3 A in 10 µs. Find its voltage, and the energy it stores at 3 A.
(c) Uncharged 4.7 µF and 2.2 µF capacitors are connected in series across 12 V. Find the equivalent capacitance and the final voltage across each.
(d) A processor's load current steps up by 2 A, and its regulator needs 1 µs to respond. The bulk capacitor supplies the extra current meanwhile; treat it as ideal. Find the smallest capacitance that keeps the rail droop below 50 mV for that microsecond.

**2 [A] · RC timing.** A 3.3 V step at $t = 0$ drives $R$ = 10 kΩ in series with an uncharged $C$ = 100 nF.
(a) Find the time constant and the capacitor voltage at $t$ = 2 ms.
(b) Find the 10–90% rise time, the −3 dB bandwidth of this RC low-pass, and their product.
(c) The capacitor is the sampling capacitor of a 12-bit ADC. From a full-scale step, how long must it settle to come within half an LSB of its final value?
(d) Find the energy dissipated in the resistor during a complete charge.

**3 [B] · Switching twice.** The circuit has these elements:

- V1, node 1 (+) to node 0, 12 V;
- R1, node 1 to node a, 4 kΩ;
- R2, node a to node 0, 12 kΩ;
- C, node a to node 0, 10 µF;
- R3, 6 kΩ, from node a to node 0 through a switch S.

S has been open for a long time. It closes at $t = 0$ and opens again at $t$ = 40 ms.
(a) Find $v_C(0^-)$.
(b) For $0 < t < 40$ ms, find the value the capacitor voltage heads toward, the time constant, and $v_C(t)$.
(c) Find, at $t = 0^+$, the current in R3 and the capacitor current $i_C$ (into the capacitor at node a).
(d) When does $v_C$ pass through 7 V?
(e) Find $v_C$ at $t$ = 40 ms, the time constant after S opens, and $v_C$ at $t$ = 100 ms.

**4 [B] · A ringing step response.** A 10 V step is applied at $t = 0$ to a series RLC circuit at rest, with $R$ = 20 Ω, $L$ = 1 mH and $C$ = 1 µF. The output is the capacitor voltage.
(a) Find $\omega_0$, $f_0$, α, ζ and $Q$.
(b) Find the ringing frequency $\omega_d$ and $f_d$.
(c) Find the overshoot, the peak capacitor voltage and the time at which it occurs.
(d) Find the peak current and the time at which it occurs.
(e) Find the series resistance that makes the circuit critically damped, and the resistance that limits the overshoot to 5%.

**5 [B] · Laplace with initial conditions.** The circuit has these elements:

- $v_{in}$, node 1 (+) to node 0;
- R1, node 1 to node 2, 1 kΩ;
- C1, node 2 to node 0, 1 µF;
- R2, node 2 to node 3, 1 kΩ;
- C2, node 3 to node 0, 1 µF.

The input has been 2 V for a long time and steps to 5 V at $t = 0$.
(a) Find both capacitor voltages at $t = 0^-$.
(b) Draw the s-domain circuit, with each capacitor's initial-condition source. Write the nodal equations and solve them for $V_3(s)$.
(c) Show that $V_3(s) = 2/s + 3H(s)/s$, where $H(s) = V_3/V_{in}$ with zero initial conditions. Find $H(s)$, its poles and its damping ratio.
(d) Find $v_3(t)$ by partial fractions.
(e) Evaluate $v_3$ at 1 ms and at 2 ms. Check $v_3(0^+)$, $dv_3/dt(0^+)$ and $v_3(\infty)$ with the initial- and final-value theorems.

**6 [B] · Phasors and the conjugate match.** The circuit has these elements:

- $v_s = 10\cos(10^4t)$ V, node 1 (+) to node 0;
- R1, node 1 to node 2, 20 Ω;
- L, node 2 to node 0, 10 mH;
- C, node 2 to node 3, 10 µF;
- R2, node 3 to node 0, 10 Ω.

(a) Find the impedance of L and of C at this frequency, and the impedance the source sees.
(b) Find $v_2(t)$, and the current $i_{R2}(t)$ in R2 from node 3 to node 0.
(c) Find the average power absorbed by R2 and the average power delivered by the source.
(d) Remove R2. Find the Thévenin equivalent seen looking into nodes 3 and 0.
(e) Find the load impedance at nodes 3 and 0 that would absorb the most power, and that power. Explain why it equals the power that the source and R1 alone could deliver to a matched load.

**7 [B] · Power factor and harmonics.** A 230 V (RMS), 50 Hz supply feeds a 10 kW load at power factor 0.75 lagging.
(a) Find the apparent power, the reactive power and the line current.
(b) Find the capacitance that, connected across the load, raises the power factor to 0.95 lagging.
(c) Find the new line current and the percentage reduction in the feeder's $I^2R$ loss.
(d) A second load's current has a fundamental of 10 A (RMS), in phase with the voltage, and harmonics of 3 A at the 3rd and 1.5 A at the 5th (RMS). Find its RMS current, its THD and its power factor. Could a capacitor improve this power factor?

**8 [B] · Bode plots and phase margin.**
(a) Sketch the Bode magnitude and phase asymptotes of the lead network $H(s) = (1 + s/10^3)/(1 + s/10^4)$, with $s$ in rad/s.
(b) Find the exact gain in dB at $\omega = 10^3$ and $10^4$ rad/s, and compare it with the asymptotes.
(c) Find the frequency of maximum phase lead, the maximum lead, and the gain there.
(d) An op-amp has open-loop gain $A(s) = 10^5/[(1 + s/\omega_1)(1 + s/\omega_2)]$, with $f_1$ = 10 Hz and $f_2$ = 2 MHz. Find its gain–bandwidth product. Connected as a unity-gain follower (β = 1), find the crossover frequency of the loop gain $A\beta$ and the phase margin.
(e) Repeat (d) for a non-inverting gain of 10 (β = 0.1). Which configuration is harder to stabilize, and why?

**9 [B] · Resonance and an active filter.**
(a) A series RLC circuit with $L$ = 10 µH, $C$ = 1 nF and $R$ = 5 Ω is driven by a 1 V (peak) source, and the output is taken across R. Find $f_0$, $Q$, the −3 dB bandwidth, and the amplitude of the capacitor voltage at resonance.
(b) Find the output's gain (dB) and phase at 1.5 MHz and at 1.7 MHz.
(c) Design a unity-gain Sallen–Key Butterworth low-pass with $f_0$ = 1 kHz and $R_1 = R_2$ = 10 kΩ. Find $C_1$ (from the middle node to the output) and $C_2$ (from the op-amp's input to ground).
(d) Find this second-order filter's attenuation at 3 kHz. Find the lowest Butterworth order that gives at least 40 dB at 3 kHz with its −3 dB corner at 1 kHz, and the attenuation that order gives.

**10 [B] · Coupled coils and transformers.**
(a) Two coupled coils have $L_1$ = 4 mH, $L_2$ = 1 mH and $M$ = 1.8 mH. Find the coupling coefficient, and the inductance of the two coils in series aiding and in series opposing.
(b) The secondary is loaded with 50 Ω, and the primary is driven at 10 kHz. Find the reflected impedance, the input impedance and the ratio of secondary to primary current magnitudes.
(c) An ideal transformer must make an 8 Ω speaker look like 800 Ω to an amplifier. Find the turns ratio.
(d) A 10 kVA, 2400/240 V transformer has 80 W of core loss, and 200 W of copper loss at full load. Find:

- its efficiency at full load and power factor 0.8;
- the load fraction for maximum efficiency;
- that maximum efficiency at power factor 0.8.

**11 [B] · A two-port.** A T network has series arms $Z_a$ = 10 Ω (port 1 side) and $Z_b$ = 20 Ω (port 2 side), and a shunt arm $Z_c$ = 100 Ω.
(a) Find its z-parameters from the open-circuit tests. Is it reciprocal? Is it symmetric?
(b) Convert to ABCD parameters and check $AD - BC$.
(c) With a 50 Ω load at port 2, find the input impedance and the voltage gain $\mathbf{V}_2/\mathbf{V}_1$.
(d) In a 50 Ω system, find:

- $S_{11}$, $S_{21}$ and $S_{22}$;
- the insertion loss, and the return loss at port 1;
- the fraction of the power incident at port 1 that the network absorbs.

Why do $S_{11}$ and $S_{22}$ differ?

**12 [B] · Three-phase.** A balanced Δ load of $Z$ = 30 + j40 Ω per phase is connected to a 400 V (line-to-line), 50 Hz, three-phase supply.
(a) Find the phase current, the line current, and the total $P$, $Q$ and power factor.
(b) Find the two wattmeter readings, with the current coils in lines a and c and both voltage coils returning to line b. Recover $P$ and $Q$ from them.
(c) Find:

- the capacitance per phase, connected in Y, that brings the power factor to unity;
- the new line current;
- the capacitance per phase that a Δ-connected bank would need.

**13 [C] · A buck converter's output filter.** A buck converter's switch node is a 0–12 V square wave at 500 kHz with a 25% duty cycle. It drives $L$ = 2.2 µH in series to the output node. At the output, $C$ = 47 µF (with an ESR of 10 mΩ in series) and a 1 Ω load go to ground. Each part carries 3 points.
(a) Ignoring the ESR, find:

- the filter's $f_0$;
- its characteristic impedance $Z_0 = \sqrt{L/C}$;
- its $Q$ with the 1 Ω load;
- the gain from the switch node to the output at $f_0$, in dB.

(b) Find the DC output voltage. Find the amplitude of the 500 kHz fundamental at the output, with the ESR and without it. Which element sets the ripple, and why?
(c) The control loop is frozen, with the switch node held at its average, and the load current steps up by 2 A at $t = 0$. Ignoring the ESR, derive the output deviation $v(t)$, and find its peak and when the peak occurs. Compare the peak with the estimate $\Delta I\cdot Z_0$.
(d) Find $Q$ and the gain at $f_0$ at a light load of 10 Ω. Explain what this does to the load-step ringing, and name two ways designers damp it.

**14 [C] · Matching a load at 2.4 GHz.** A 12.5 Ω resistive antenna feed point must be matched to a 50 Ω radio at 2.4 GHz.
(a) Without a match, find the reflection coefficient, the return loss and the mismatch loss.
(b) Design a low-pass L-section: a series inductor next to the load, and a shunt capacitor across the 50 Ω side. Derive the design equations from the requirement $Z_{in}$ = 50 Ω, showing that $Q = \sqrt{R_{high}/R_{low} - 1}$. Find $L$ and $C$.
(c) Confirm with ABCD matrices that $Z_{in}$ = 50 Ω at 2.4 GHz.
(d) Find $\lvert\Gamma\rvert$ and the return loss at 2.2 GHz and at 2.6 GHz. Does the match meet a 10 dB return-loss requirement across 2.2–2.6 GHz?
(e) Find the mismatch loss at 2.6 GHz with the match, and compare it with (a).

**15 [B] · Diligence: four claims.** For each claim, say in two or three sentences what is wrong or missing, and give the one question you would ask.
(a) "Our board carries 2,000 µF of decoupling capacitance, so the supply is clean up to 1 GHz."
(b) "Our 30 A, 415 V three-phase rack feed supports 21.6 kW per rack."
(c) "Our anti-aliasing filter's −3 dB bandwidth is 1 MHz, so our 1 MHz signal passes undistorted."
(d) "Our op-amp's 100 MHz gain–bandwidth product gives our unity-gain buffer 100 MHz of clean bandwidth."
