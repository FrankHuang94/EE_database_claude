# Term 2 Checkpoint · FE-Style Practice Exam

**Covers:** Courses 06–08 (DC circuit analysis; transient and AC circuits, frequency response, AC and three-phase power; digital logic design). **Questions:** 50 (multiple choice and numeric entry). **Time:** 150 minutes, the FE pace of about 3 minutes per question.
**Materials:** an FE-approved calculator and the *NCEES FE Reference Handbook* only (free PDF from NCEES); no course notes or sheets. Finding formulas in the handbook quickly is part of the practice.
**Scoring:** one point per question. Score each block separately and aim for at least 70% in every block. Write every miss into your error log with its cause, and re-solve it a week later. Solutions with full explanations, each pointing to the chapter to revisit, are in [solutions.md](solutions.md); open them only after you finish.

**Conventions:**

- For numeric entry, give 3 significant figures unless the question says otherwise.
- Circuits are given as element lists: "R1, node 1 to node 2, 2 kΩ" places a resistor between those nodes, and node 0 is ground. For a voltage source the first node named is its + terminal; a current source "into node $k$" drives its current from ground into node $k$.
- Op-amps are ideal. Sinusoidal sources are given as amplitudes (peak) unless labeled RMS; mains and three-phase quantities are RMS.
- "8-bit" numbers are two's complement unless called unsigned.

---

## Block 1 · DC circuit analysis (questions 1–14)

**1.** A 12 V battery delivers a steady 2.5 A for 3 hours. The energy it delivers is:
(A) 90.0 kJ · (B) 108 kJ · (C) 324 kJ · (D) 5.40 kJ

**2.** *Numeric entry.* A 6 kΩ resistor in parallel with a 3 kΩ resistor is connected in series with a 4 kΩ resistor. What is the equivalent resistance, in kΩ?

**3.** A 10 V source drives two 10 kΩ resistors in series. A 10 kΩ load is connected across the lower resistor. The load voltage is:
(A) 5.00 V · (B) 3.33 V · (C) 6.67 V · (D) 2.50 V

**4.** *Numeric entry.* Find the voltage at node 3, in volts:

- V1, node 1 to node 0, 10 V;
- R1, node 1 to node 2, 2 kΩ;
- R2, node 2 to node 0, 4 kΩ;
- R3, node 2 to node 3, 2 kΩ;
- R4, node 3 to node 0, 4 kΩ;
- I1, 1 mA into node 3.

**5.** *Numeric entry.* Find the current, in amperes, in R2 (flowing from node 2 to node 0):

- V1, node 1 to node 0, 12 V;
- R1, node 1 to node 2, 4 Ω;
- R2, node 2 to node 0, 6 Ω;
- R3, node 2 to node 3, 2 Ω;
- V2, node 3 to node 0, 6 V.

**6.** *Numeric entry.* An amplifier is modeled as follows. A source $v_s$ with 1 kΩ of internal resistance drives the amplifier's 9 kΩ input resistance, which carries the voltage $v_{in}$. The amplifier's output is a voltage-controlled voltage source of $50\,v_{in}$ in series with 100 Ω, driving a 1 kΩ load. What is the overall voltage gain $v_{load}/v_s$?

**7.** In the circuit below, the voltage at node 2 is:

- V1, node 1 to node 0, 10 V;
- R1, node 1 to node 2, 5 Ω;
- R2, node 2 to node 0, 20 Ω;
- I1, 2 A into node 2.

(A) 8.00 V · (B) 16.0 V · (C) 12.0 V · (D) 18.0 V

**8.** The Thévenin equivalent seen at node 3 (relative to node 0) of this circuit is:

- V1, node 1 to node 0, 24 V;
- R1, node 1 to node 2, 6 kΩ;
- R2, node 2 to node 0, 3 kΩ;
- R3, node 2 to node 3, 2 kΩ.

(A) 8 V in series with 4 kΩ · (B) 8 V in series with 11 kΩ · (C) 16 V in series with 4 kΩ · (D) 12 V in series with 2 kΩ

**9.** *Numeric entry.* A load resistor is connected between node 3 and node 0 of the circuit of question 8, and chosen to receive the most power. What is that power, in mW?

**10.** *Numeric entry.* A 2 kΩ resistor connects terminal a to node 0, and in parallel with it a voltage-controlled current source draws $g\,v_a$ from terminal a to node 0, with $g$ = 1 mS and $v_a$ the voltage of terminal a. What resistance, in ohms, is seen looking into terminal a?

**11.** An inverting amplifier has an input resistor of 4.7 kΩ and a feedback resistor of 47 kΩ. For an input of +0.3 V, the output is:
(A) 3.00 V · (B) −3.00 V · (C) −3.30 V · (D) 3.30 V

**12.** *Numeric entry.* An inverting summing amplifier has a 10 kΩ feedback resistor and two inputs: $v_1$ = 0.5 V through 10 kΩ and $v_2$ = −0.2 V through 5 kΩ. What is the output voltage, in volts?

**13.** *Numeric entry.* A Wheatstone bridge is supplied between node a and node 0. One arm has $R_1$ = 1 kΩ from node a to node b and $R_2$ = 2 kΩ from node b to node 0. The other has $R_3$ = 1.5 kΩ from node a to node c and an unknown $R_x$ from node c to node 0. The detector between b and c reads zero. What is $R_x$, in kΩ?

**14.** Two 1 MΩ resistors in series are connected across 10 V. A voltmeter with 10 MΩ input resistance is connected across the lower resistor. It reads:
(A) 5.00 V · (B) 4.76 V · (C) 4.55 V · (D) 4.17 V

## Block 2 · Transient and AC circuits, frequency response and power (questions 15–32)

**15.** The voltage across a 47 µF capacitor rises linearly from 0 to 5 V in 10 ms. The capacitor current is:
(A) 2.35 mA · (B) 23.5 mA · (C) 235 mA · (D) 0.470 mA

**16.** *Numeric entry.* A 9 V source is connected at $t = 0$ through 20 kΩ to an uncharged 0.5 µF capacitor. What is the capacitor voltage, in volts, at $t$ = 15 ms?

**17.** A 12 V source is connected at $t = 0$ to a 100 Ω resistor in series with a 50 mH inductor carrying no initial current. The current at $t$ = 1 ms is:
(A) 75.9 mA · (B) 104 mA · (C) 120 mA · (D) 16.2 mA

**18.** A series RLC circuit has $R$ = 10 Ω, $L$ = 1 mH and $C$ = 10 µF. Its damping ratio is:
(A) 0.250 · (B) 0.500 · (C) 1.00 · (D) 2.00

**19.** *Numeric entry.* A second-order system with damping ratio 0.5 receives a step input. What is its percent overshoot?

**20.** A system with transfer function $H(s) = \dfrac{10}{s^2 + 3s + 2}$ receives a unit step. Its output settles to:
(A) 0 · (B) 3.33 · (C) 5.00 · (D) 10.0

**21.** A 100 V (peak), 1 kHz source drives a 30 Ω resistor in series with a 6.366 mH inductor. The current phasor, with the source at 0°, is:
(A) 2.00 A ∠−53.1° · (B) 2.00 A ∠53.1° · (C) 1.43 A ∠−53.1° · (D) 3.33 A ∠0°

**22.** *Numeric entry.* What is the RMS value, in volts, of $v(t) = 10 + 10\cos\omega t$ V?

**23.** A single-phase load draws 10 A RMS from 230 V RMS at a power factor of 0.8 lagging. Its reactive power is:
(A) 1840 var · (B) 1380 var · (C) 2300 var · (D) 1035 var

**24.** *Numeric entry.* A 10 kW load runs at a power factor of 0.70 lagging. How much capacitive reactive power, in kvar, raises the power factor to 0.95 lagging?

**25.** A first-order RC low-pass filter has $R$ = 1.59 kΩ and $C$ = 100 nF. Its gain at 10 kHz is closest to:
(A) −3.0 dB · (B) −10.0 dB · (C) −20.0 dB · (D) −40.0 dB

**26.** *Numeric entry.* An amplifier with a voltage gain of 26 dB drives a cable with 6 dB of loss. What is the overall voltage gain as a plain ratio?

**27.** *Numeric entry.* A series RLC circuit has $R$ = 20 Ω, $L$ = 10 mH and $C$ = 100 nF. What is its −3 dB bandwidth, in Hz?

**28.** A second-order Butterworth low-pass filter has its cutoff at 1 kHz. Its attenuation at 3 kHz is:
(A) 9.5 dB · (B) 19.1 dB · (C) 38.2 dB · (D) 3.0 dB

**29.** An 8 Ω loudspeaker is driven through an ideal transformer with a 5:1 turns ratio (primary to secondary). The resistance seen at the primary is:
(A) 40 Ω · (B) 1.6 Ω · (C) 200 Ω · (D) 0.32 Ω

**30.** *Numeric entry.* A 75 Ω resistive load terminates a 50 Ω line. What is the return loss, in dB?

**31.** *Numeric entry.* A balanced star-connected load, with each phase $20\ \Omega\angle36.87°$, is supplied at 400 V RMS line to line. What is the total real power, in kW?

**32.** A balanced three-phase motor takes 15 kW from a 400 V (line-to-line) supply at a power factor of 0.85. Its line current is:
(A) 25.5 A · (B) 44.1 A · (C) 21.7 A · (D) 37.5 A

## Block 3 · Digital systems (questions 33–50)

**33.** The 8-bit two's-complement pattern 1100 1011 represents:
(A) 203 · (B) −53 · (C) −52 · (D) −75

**34.** *Numeric entry.* What is the hexadecimal number 3A7 in decimal?

**35.** The range of a 12-bit two's-complement number is:
(A) −2048 to 2047 · (B) −2047 to 2047 · (C) 0 to 4095 · (D) −4096 to 4095

**36.** An 8-bit adder adds 70₁₆ and 30₁₆ as signed numbers. Which statement is true?
(A) No overflow; the result is +160 · (B) Overflow; the result reads as −96 · (C) No overflow; the result reads as −96 · (D) The carry out of the top bit is 1

**37.** $F = AB + A\overline{B}C + \overline{A}C$ simplifies to:
(A) $AB + C$ · (B) $A + C$ · (C) $AB + \overline{A}C$ · (D) $C$

**38.** The complement of $\overline{A}B + C$ is:
(A) $(A + \overline{B})\,\overline{C}$ · (B) $A\overline{B} + \overline{C}$ · (C) $(\overline{A} + B)C$ · (D) $A + \overline{B} + \overline{C}$

**39.** The minimal sum of products of $F(A, B, C, D) = \sum m(0, 2, 5, 7, 8, 10, 13, 15)$ (with $A$ the most significant bit) is:
(A) $\overline{B}\,\overline{D} + BD$ · (B) $BD$ · (C) $\overline{A}\,\overline{B}\,\overline{D} + BD$ · (D) $\overline{B}D + B\overline{D}$

**40.** *Numeric entry.* How many 2:1 multiplexers does a 32:1 multiplexer built as a tree need?

**41.** *Numeric entry.* A 32-bit ripple-carry adder has a delay of 2 gate delays per bit, and each gate delay is 25 ps. What is the adder's delay, in ns?

**42.** *Numeric entry.* A register-to-register path has clock-to-Q delay 80 ps, logic delay 720 ps and setup time 50 ps. What is the maximum clock frequency, in GHz?

**43.** A short path between two flip-flops on the same ideal clock has a minimum clock-to-Q delay of 30 ps and a minimum logic delay of 15 ps; the receiving flip-flop's hold time is 60 ps. The hold check is:
(A) met by 45 ps · (B) violated by 15 ps · (C) met by 15 ps · (D) met or violated depending on the clock period

**44.** The fewest flip-flops a counter needs to count through 100 states is:
(A) 6 · (B) 7 · (C) 10 · (D) 100

**45.** *Numeric entry.* What is the period of a maximal-length 10-bit linear-feedback shift register?

**46.** A state machine has 12 states. With binary and with one-hot encoding it needs:
(A) 4 and 12 flip-flops · (B) 3 and 12 flip-flops · (C) 4 and 4 flip-flops · (D) 12 and 4 flip-flops

**47.** Which statement about Moore and Mealy machines is true?
(A) A Mealy machine's outputs depend on its state and its present inputs, so they can respond in the same clock cycle as the input · (B) A Moore machine's outputs depend on its present inputs only · (C) A Mealy machine always needs more states than an equivalent Moore machine · (D) Moore outputs can glitch when the inputs change between clock edges

**48.** *Numeric entry.* How many address lines does a 256 K × 16 memory need?

**49.** A push-button signal, asynchronous to the system clock, must drive a synchronous state machine. The standard safe practice is to:
(A) pass it through two flip-flops in series clocked by the system clock before use · (B) connect it directly to the state register's D inputs · (C) use it as the clock of the state register · (D) pass it through an inverter chain to delay it

**50.** *Numeric entry.* How many bits does a ROM need to implement a function with 6 inputs and 4 outputs?
