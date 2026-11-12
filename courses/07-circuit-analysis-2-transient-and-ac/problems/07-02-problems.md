# Problems 07-02 · First-Order RC and RL Transients

Chapter: [07-02](../chapters/07-02-first-order-rc-rl-transients.md) · Worked solutions: [07-02 solutions](../solutions/07-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** passive sign convention; switches act instantaneously; "a long time" means DC steady state; $u(t)$ is the unit step (0 for $t < 0$, 1 for $t > 0$); answers to 3–4 significant figures. Use Boltzmann's constant $k = 1.381\times10^{-23}$ J/K and $T = 300$ K where needed.

Several problems have an ngspice netlist in [labs/07-02-lab](../labs/07-02-lab/README.md) that confirms the published answer. Try the problem first, then run the netlist.

---

## Problems

### Problem 07-02.1 [A]

Compute the time constant of each circuit and give it in convenient units:

(a) $R = 2.2$ kΩ, $C = 47$ µF  (b) $L = 5$ mH, $R = 50\ \Omega$  (c) $R = 10$ kΩ, $C = 10$ pF

(d) In one or two sentences, explain why increasing R lengthens an RC time constant but shortens an RL time constant.

### Problem 07-02.2 [A]

For any first-order response:

(a) What percentage of the total change remains after $3\tau$?
(b) How many time constants are needed to complete 99.9% of the change?
(c) How many time constants are needed to complete 50% of the change?

### Problem 07-02.3 [A]

A 10 V source in series with a 1 kΩ resistor is connected at $t = 0$ (by a switch) to node A. From node A to ground are a 4 kΩ resistor and an initially uncharged 1 µF capacitor. Find $v_C(0^+)$, $i_C(0^+)$, $v_C(\infty)$, $i_C(\infty)$, the Thevenin resistance seen by the capacitor, τ, and $v_C(t)$.

### Problem 07-02.4 [A]

A 9 V source drives a 3 Ω resistor in series with a 2 mH inductor and has done so for a long time. Find the inductor current, the inductor voltage and the energy stored in the inductor.

### Problem 07-02.5 [B] (design)

A microcontroller's supply **hold-up** capacitor (10 µF, charged to 3.3 V) must keep the circuit running briefly after the main supply fails, long enough to save data. When the supply is removed, the capacitor must keep the voltage across the load $R$ at or above 3.0 V for at least 50 ms. Model the load as a pure resistor. What is the minimum value of $R$?

### Problem 07-02.6 [B]

An RC low-pass ($R = 10$ kΩ, $C = 1$ µF, initially uncharged) is driven by a single rectangular pulse: 5 V from $t = 0$ to $t = 5$ ms, and 0 V otherwise.

(a) Find $v_C$ at $t = 5$ ms and at $t = 15$ ms.
(b) Find the resistor current just after $t = 0$ and just after $t = 5$ ms (with sign, positive toward the capacitor).
(c) Sketch $v_C(t)$ from 0 to 30 ms.

### Problem 07-02.7 [B]

A 2 A current source drives current *up* into a top node; $R_1 = 10\ \Omega$ connects that node to ground (the bottom node). At $t = 0$ a switch connects a series combination of $R_2 = 15\ \Omega$ and $L = 50$ mH from the top node to ground. The inductor carries no current before $t = 0$.

(a) Find the Norton/Thevenin resistance seen by the inductor, τ and $i_L(\infty)$.
(b) Find $v_L(0^+)$.
(c) Write $i_L(t)$ and evaluate $i_L(3\text{ ms})$.

### Problem 07-02.8 [B]

A 12 V source in series with $R_1 = 2$ kΩ feeds node A, where a 5 µF capacitor goes to ground. The circuit has been in this state for a long time. At $t = 0$ a switch connects a second resistor, $R_2 = 2$ kΩ, from node A to ground.

(a) Find $v_C(0^-)$ and $v_C(\infty)$.
(b) Find τ.
(c) Find $i_{R2}(0^-)$, $i_{R2}(0^+)$, $i_C(0^+)$ and $i_{R2}(\infty)$. Which of these quantities jump at $t = 0$?
(d) Write $v_C(t)$ and $i_{R2}(t)$.

### Problem 07-02.9 [B]

(a) An oscilloscope channel, modeled as a single pole, has a 10–90% rise time of 3.5 ns. Estimate its bandwidth using the 0.35 rule. What does the exact single-pole relation give?
(b) An RC low-pass has $R = 1$ kΩ and $C = 10$ nF. Find its 3 dB frequency, its 10–90% rise time and its 50% delay.

### Problem 07-02.10 [B]

An RC low-pass with $\tau = 1$ ms, initially at rest, is driven by a ramp input $mt$ with slope $m = 2$ V/ms.

(a) Using the general solution (chapter §3.10), write the output $x(t)$.
(b) Evaluate $x(5\text{ ms})$.
(c) In steady state, by how much time does the output lag the input, and what is the constant voltage error?

### Problem 07-02.11 [B]

An inverting op-amp integrator has $R = 10$ kΩ and $C = 100$ nF, with the capacitor initially uncharged. At $t = 0$ the input steps from 0 to −1 V. Treat the op-amp as ideal.

(a) Find $v_{out}(t)$ and evaluate it at $t = 5$ ms.
(b) The op-amp runs from ±12 V supplies, and its output saturates at the rails. At what time does the output saturate?
(c) A resistor $R_f = 100$ kΩ is now placed in parallel with $C$ (a leaky integrator). Find the time constant, the final output voltage and $v_{out}(10\text{ ms})$. Compare with the ideal integrator at 10 ms.

### Problem 07-02.12 [B]

A 0/1 V square wave of frequency 1 kHz (50% duty) drives an RC low-pass. Using the steady-state results of chapter §3.9:

(a) For $\tau = 0.5$ ms, find $V_{max}$, $V_{min}$ and the peak-to-peak ripple.
(b) For $\tau = 5$ ms, find $V_{max}$, $V_{min}$ and the ripple, and compare the ripple with the approximation $VT/(4\tau)$.
(c) Which choice of τ would you use to turn a PWM signal into a steady DC level? What is the cost of making τ larger?

### Problem 07-02.13 [C] (energy and CMOS power)

(a) Prove that charging an initially uncharged capacitor $C$ to $V$ from a constant voltage source through any resistance $R$ dissipates $\tfrac{1}{2}CV^2$ in the resistor.
(b) Prove that charging in $N$ equal voltage steps, letting each step settle, dissipates a total of $CV^2/(2N)$.
(c) A logic node has $C = 2$ fF and $V_{DD} = 0.75$ V. How much energy does each 0 → 1 transition draw from the supply?
(d) The node has activity factor $\alpha = 0.15$ at $f = 3$ GHz. Find its average dynamic power.
(e) How many such nodes switching together would dissipate 50 W?
(f) By what percentage does dynamic power fall if $V_{DD}$ is reduced from 0.75 V to 0.65 V at the same frequency? What would you expect to happen to the maximum clock frequency, and why?

### Problem 07-02.14 [C] (design: relay flyback)

A relay coil, modeled as $L = 100$ mH in series with its winding resistance $R_{coil} = 200\ \Omega$, has its top terminal at +12 V. A **low-side** transistor switch connects its bottom terminal to ground. The transistor is rated for 30 V.

(a) Find the coil current $I_0$ just before the transistor turns off.
(b) A resistor $R_f$ is connected across the coil as a flyback path. Find the largest $R_f$ that keeps the transistor voltage at or below 30 V at turn-off.
(c) With that $R_f$, find the time constant of the current decay.
(d) Find the time for the coil current to fall to 10% of $I_0$ (the relay releases at about this point).
(e) The resistor is replaced by a diode with a constant 0.7 V forward drop. Find the transistor voltage at turn-off and the time constant of the decay.
(f) With the diode, find the time for the current to fall to 10% of $I_0$. Hint: the diode acts as a constant voltage source in the loop, so the current approaches $-0.7\text{ V}/R_{coil}$, not zero; it is clamped at zero when it gets there.
(g) How much energy is dissipated in total during release, and does it depend on the flyback method?
(h) Back to the resistor flyback of (b): while the relay is **on**, how much power does $R_f$ dissipate, and how much current must the transistor carry? Suggest a flyback network that keeps the fast release without this cost.

### Problem 07-02.15 [C] (design: ADC front end)

A 12-bit SAR ADC with a 3.3 V full scale has a 10 pF sampling capacitor and a 100 ns acquisition window.

(a) How many time constants are needed for ½-LSB settling?
(b) What is the largest allowable time constant, and the largest allowable total series resistance?
(c) Compute the kT/C noise and express it in LSBs.
(d) The same front end is reused with a 16-bit ADC (same full scale and capacitor). Express the kT/C noise in 16-bit LSBs. An ideal converter's quantization noise is $1/\sqrt{12}$ LSB rms; combine the two (they are independent, so add their squares) and find how many bits of effective resolution the kT/C noise costs.
(e) To bring kT/C noise down to 0.1 LSB rms at 16 bits, how large must the sampling capacitor be? With that capacitor and the same 100 ns window, what is the largest allowable series resistance? Explain the tradeoff this exposes.

### Problem 07-02.16 [C] (the two-capacitor puzzle)

A 1 µF capacitor charged to 10 V is connected at $t = 0$ through a 1 kΩ resistor to an identical, uncharged 1 µF capacitor.

(a) Find the final voltage on each capacitor (hint: charge is conserved).
(b) Find the time constant of the transient. (Hint: what single capacitance does the resistor see?)
(c) Compute the stored energy before and after, and the energy dissipated. Does the dissipated energy depend on the resistor value?
(d) If the resistor were literally zero, where would the "missing" energy go? (Discuss briefly.)

### Problem 07-02.17 [B] (dependent source; test-source method)

Node A connects to ground through $R_1 = 2$ kΩ and through a capacitor $C = 10$ µF. A voltage-controlled current source (VCCS) pushes a current $g\,v_A$ *into* node A from ground. At $t = 0$ the capacitor voltage is 1 V.

(a) Using a test voltage source $v_T$ at node A (capacitor removed), find the Thevenin resistance seen by the capacitor as a function of $g$.
(b) For $g = 0.25$ mS, find $R_{Th}$ and τ, write $v_A(t)$, and evaluate $v_A(40\text{ ms})$.
(c) For $g = 1$ mS, find $R_{Th}$ and the "time constant". Write $v_A(t)$, evaluate it at 20 ms and 100 ms, and describe what happens physically. For what values of $g$ does this occur?
(d) Where in electronics is this behavior *wanted*? (Hint: think of a circuit that must decide quickly between 0 and 1.)

### Problem 07-02.18 [B] (two-position switch; step-function notation)

A two-position switch has held a 1 µF capacitor connected through $R_a = 1$ kΩ to a +5 V source for a long time. At $t = 0$ it moves to position b, which connects the capacitor through $R_b = 4$ kΩ to a −10 V source.

(a) Find $v_C(0^-)$, τ after switching and $v_C(\infty)$.
(b) Write $v_C(t)$ for $t \ge 0$, then write a single expression valid for **all** $t$ using the unit step $u(t)$.
(c) Find the current from the −10 V source into the capacitor at $t = 0^+$ (with sign), the time at which $v_C$ crosses zero, and $v_C(8\text{ ms})$.
(d) Real two-position switches are either break-before-make or make-before-break. Which would you specify here, and does the brief overlap of a make-before-break switch harm anything?

---

## Objective coverage

| Learning objective (chapter 07-02) | Problems |
|---|---|
| 1. Derive and solve the first-order ODE (natural and step response) | 1, 3, 4, 7, 16, 17 |
| 2. Initial and final values; τ from $R_{Th}$ (including dependent sources) | 3, 4, 7, 8, 17, 18 |
| 3. Initial–final–τ method; sequential switching; periodic drive; step-function notation | 6, 8, 12, 18 |
| 4. Energy in transients; ½CV² loss; CMOS dynamic power | 4, 13, 14, 16 |
| 5. Delay, rise time, settling, ADC settling, bandwidth | 2, 5, 9, 15 |
| 6. Op-amp integrators; ramp response | 10, 11 |
