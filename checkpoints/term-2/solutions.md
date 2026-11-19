# Term 2 Checkpoint · Solutions

Questions: [README.md](README.md). Every numerical answer, and the letter of every multiple-choice answer, is checked by [verify_term2.py](verify_term2.py), which solves each circuit with its own nodal-analysis solver. Each explanation names the chapter to revisit.

**Scoring by block:** DC circuit analysis 14, transient and AC circuits 18, digital systems 18. Aim for at least 70% in each (10, 13 and 13 correct).

---

## Block 1 · DC circuit analysis

**1. Answer: (C) 324 kJ.** $W = VIt = 12 \times 2.5 \times (3 \times 3600\ \text{s}) = 324\,000$ J. (A) is the same energy in watt-hours (90.0 Wh), mislabeled; (B) uses one hour; (D) uses minutes. *([06-01](../../courses/06-circuit-analysis-1-dc/chapters/06-01-charge-current-voltage-power.md))*

**2. Answer: 6.00 kΩ.** $6 \parallel 3 = 18/9 = 2$ kΩ, plus 4 kΩ in series: 6.00 kΩ. *([06-03](../../courses/06-circuit-analysis-1-dc/chapters/06-03-kirchhoffs-laws.md))*

**3. Answer: (B) 3.33 V.** The load in parallel with the lower resistor gives $10 \parallel 10 = 5$ kΩ, so $V = 10 \times 5/(10 + 5) = 3.33$ V. (A) ignores the load: dividers are only as good as the load is light. *([06-03](../../courses/06-circuit-analysis-1-dc/chapters/06-03-kirchhoffs-laws.md))*

**4. Answer: 5.45 V.** Nodal analysis in mA, kΩ and V. Node 2: $(v_2 - 10)/2 + v_2/4 + (v_2 - v_3)/2 = 0$, so $5v_2 - 2v_3 = 20$. Node 3: $(v_3 - v_2)/2 + v_3/4 = 1$, so $3v_3 - 2v_2 = 4$. Substituting $v_2 = (20 + 2v_3)/5$ gives $11v_3 = 60$: $v_3 = 5.45$ V (and $v_2 = 6.18$ V). *([06-04](../../courses/06-circuit-analysis-1-dc/chapters/06-04-nodal-analysis.md))*

**5. Answer: 1.09 A.** One unknown node: $(v_2 - 12)/4 + v_2/6 + (v_2 - 6)/2 = 0$. Multiplying by 12: $11v_2 = 72$, so $v_2 = 6.545$ V and $i_{R2} = 6.545/6 = 1.09$ A. Mesh analysis gives the same: with mesh currents $i_1$ (left) and $i_2$ (right, clockwise), $10i_1 - 6i_2 = 12$ and $-6i_1 + 8i_2 = -6$, so $i_1 = 1.364$ A, $i_2 = 0.273$ A and $i_{R2} = i_1 - i_2 = 1.09$ A. *([06-05](../../courses/06-circuit-analysis-1-dc/chapters/06-05-mesh-analysis.md))*

**6. Answer: 40.9.** Three factors: the input divider $9/(1 + 9) = 0.9$, the source gain 50, and the output divider $1000/(100 + 1000) = 0.909$. Overall $0.9 \times 50 \times 0.909 = 40.9$. Loading at both ends costs about 18% of the open-circuit gain of 50. *([06-06](../../courses/06-circuit-analysis-1-dc/chapters/06-06-dependent-sources.md))*

**7. Answer: (B) 16.0 V.** Superposition. V1 alone (I1 open): $10 \times 20/25 = 8$ V. I1 alone (V1 shorted): 2 A into $5 \parallel 20 = 4$ Ω gives 8 V. Total 16.0 V. (A) keeps only one source. *([06-07](../../courses/06-circuit-analysis-1-dc/chapters/06-07-linearity-and-superposition.md))*

**8. Answer: (A) 8 V in series with 4 kΩ.** Open-circuit voltage: no current flows in R3, so $V_{Th} = 24 \times 3/(6 + 3) = 8$ V. With V1 shorted, $R_{Th} = (6 \parallel 3) + 2 = 4$ kΩ. (B) adds the resistors in series instead of combining R1 and R2 in parallel. *([06-08](../../courses/06-circuit-analysis-1-dc/chapters/06-08-thevenin-and-norton.md))*

**9. Answer: 4.00 mW.** Maximum power transfer: $R_L = R_{Th} = 4$ kΩ, and $P_{\max} = V_{Th}^2/(4R_{Th}) = 64/16\,000$ W = 4.00 mW. *([06-09](../../courses/06-circuit-analysis-1-dc/chapters/06-09-maximum-power-transfer.md))*

**10. Answer: 667 Ω.** Apply a test voltage $v_a$ and add the currents drawn: $i = v_a/2000 + 0.001\,v_a = 0.0015\,v_a$, so $R = v_a/i = 667$ Ω. A dependent source that draws current in proportion to its own terminal voltage behaves like a resistor of $1/g$ = 1 kΩ in parallel. *([06-06](../../courses/06-circuit-analysis-1-dc/chapters/06-06-dependent-sources.md), [06-08](../../courses/06-circuit-analysis-1-dc/chapters/06-08-thevenin-and-norton.md))*

**11. Answer: (B) −3.00 V.** Gain $-R_f/R_{in} = -47/4.7 = -10$, so $v_{out} = -3.00$ V. (D) is a non-inverting amplifier's $1 + 10 = 11$ times, with the wrong sign too. *([06-10](../../courses/06-circuit-analysis-1-dc/chapters/06-10-ideal-op-amp.md))*

**12. Answer: −0.100 V.** $v_{out} = -(10/10 \times 0.5 + 10/5 \times (-0.2)) = -(0.5 - 0.4) = -0.100$ V. *([06-10](../../courses/06-circuit-analysis-1-dc/chapters/06-10-ideal-op-amp.md))*

**13. Answer: 3.00 kΩ.** Balance means $v_b = v_c$: $R_2/(R_1 + R_2) = R_x/(R_3 + R_x)$, which rearranges to $R_x = R_2R_3/R_1 = 2 \times 1.5/1 = 3.00$ kΩ. *([06-11](../../courses/06-circuit-analysis-1-dc/chapters/06-11-practical-dc-circuits-and-measurement.md))*

**14. Answer: (B) 4.76 V.** The meter in parallel with the lower resistor gives $1 \parallel 10 = 0.909$ MΩ, so it reads $10 \times 0.909/1.909 = 4.76$ V instead of 5.00 V, a −4.8% loading error. A meter's input resistance should be at least 100 times the circuit's Thévenin resistance for a 1% error. *([06-11](../../courses/06-circuit-analysis-1-dc/chapters/06-11-practical-dc-circuits-and-measurement.md))*

## Block 2 · Transient and AC circuits, frequency response and power

**15. Answer: (B) 23.5 mA.** $i = C\,dv/dt = 47\ \mu\text{F} \times (5\ \text{V}/10\ \text{ms}) = 47 \times 10^{-6} \times 500 = 23.5$ mA. *([07-01](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-01-capacitors-and-inductors.md))*

**16. Answer: 6.99 V.** $\tau = RC = 20\ \text{k}\Omega \times 0.5\ \mu\text{F} = 10$ ms, so $v = 9(1 - e^{-15/10}) = 9 \times 0.777 = 6.99$ V. *([07-02](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md))*

**17. Answer: (B) 104 mA.** $\tau = L/R = 0.5$ ms and the final current is $12/100 = 120$ mA, so $i(1\ \text{ms}) = 120(1 - e^{-2}) = 104$ mA. (A) uses $\tau = 1$ ms; (C) is the final value. *([07-02](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md))*

**18. Answer: (B) 0.500.** $\omega_0 = 1/\sqrt{LC} = 1/\sqrt{10^{-8}} = 10^4$ rad/s and $\alpha = R/(2L) = 5000$ s⁻¹, so $\zeta = \alpha/\omega_0 = 0.500$: underdamped. Equivalently $\zeta = (R/2)\sqrt{C/L}$. *([07-03](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-03-second-order-rlc-transients.md))*

**19. Answer: 16.3%.** Overshoot $= e^{-\pi\zeta/\sqrt{1 - \zeta^2}} = e^{-\pi \times 0.5/0.866} = e^{-1.814} = 0.163$. *([07-03](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-03-second-order-rlc-transients.md))*

**20. Answer: (C) 5.00.** The poles, −1 and −2, are in the left half-plane, so the final-value theorem applies: $\lim_{s\to0} s \cdot H(s)/s = H(0) = 10/2 = 5.00$. *([07-04](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-04-laplace-domain-circuit-analysis.md))*

**21. Answer: (A) 2.00 A ∠−53.1°.** $X_L = 2\pi \times 1000 \times 6.366\ \text{mH} = 40.0$ Ω, so $Z = 30 + j40 = 50\angle53.1°$ Ω and $\mathbf{I} = 100\angle0°/50\angle53.1° = 2.00\angle{-53.1°}$ A. Current lags voltage in an inductive circuit. *([07-05](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-05-sinusoidal-steady-state-and-impedance.md))*

**22. Answer: 12.2 V.** The DC and AC parts are orthogonal, so their mean squares add: $V_{rms} = \sqrt{10^2 + (10/\sqrt2)^2} = \sqrt{150} = 12.2$ V. Adding 10 V and 7.07 V (giving 17.1 V) is the classic error. *([07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md))*

**23. Answer: (B) 1380 var.** $S = 230 \times 10 = 2300$ VA, $P = 0.8S = 1840$ W, and $Q = S\sin\phi = 2300 \times 0.6 = 1380$ var. (A) is the real power and (C) the apparent power. *([07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md))*

**24. Answer: 6.92 kvar.** $Q_C = P(\tan\phi_1 - \tan\phi_2) = 10(\tan\cos^{-1}0.70 - \tan\cos^{-1}0.95) = 10(1.020 - 0.329) = 6.92$ kvar. *([07-06](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md))*

**25. Answer: (C) −20.0 dB.** $f_c = 1/(2\pi RC) = 1/(2\pi \times 1590 \times 10^{-7}) = 1.00$ kHz. At $10f_c$ a first-order low-pass is one decade down its −20 dB/decade slope: $-10\lg(1 + 10^2) = -20.0$ dB. (A) is the gain at the corner. *([07-07](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-07-frequency-response-and-bode-plots.md))*

**26. Answer: 10.0.** Gains in dB add: $26 - 6 = 20$ dB, and $10^{20/20} = 10.0$. *([07-07](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-07-frequency-response-and-bode-plots.md))*

**27. Answer: 318 Hz.** For a series RLC, $\text{BW} = R/(2\pi L) = 20/(2\pi \times 0.01) = 318$ Hz. Equivalently, $f_0 = 1/(2\pi\sqrt{LC}) = 5.03$ kHz and $Q = (1/R)\sqrt{L/C} = 15.8$, so $\text{BW} = f_0/Q$. *([07-08](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md))*

**28. Answer: (B) 19.1 dB.** An $n$th-order Butterworth has $|H|^2 = 1/(1 + (f/f_c)^{2n})$. With $n = 2$ at $3f_c$: $10\lg(1 + 3^4) = 10\lg 82 = 19.1$ dB. (A) is the first-order value. *([07-08](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md))*

**29. Answer: (C) 200 Ω.** An ideal transformer reflects impedance by the square of the turns ratio: $5^2 \times 8 = 200$ Ω. (A) uses the ratio, not its square. *([07-09](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-09-mutual-inductance-and-transformers.md))*

**30. Answer: 14.0 dB.** $\Gamma = (75 - 50)/(75 + 50) = 0.2$, and the return loss is $-20\lg 0.2 = 14.0$ dB (VSWR 1.5). *([07-10](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-10-two-port-networks.md))*

**31. Answer: 6.40 kW.** Phase voltage $400/\sqrt3 = 230.9$ V, so the phase current is $230.9/20 = 11.55$ A. Each phase takes $230.9 \times 11.55 \times \cos 36.87° = 2133$ W, and the three take 6.40 kW. *([07-11](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-11-three-phase-circuits.md))*

**32. Answer: (A) 25.5 A.** $P = \sqrt3V_LI_L\cos\phi$, so $I_L = 15\,000/(\sqrt3 \times 400 \times 0.85) = 25.5$ A. (B) forgets the √3; (C) the power factor; (D) both. *([07-11](../../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-11-three-phase-circuits.md))*

## Block 3 · Digital systems

**33. Answer: (B) −53.** The top bit is 1, so the number is negative. Invert (0011 0100 = 52) and add 1: magnitude 53, so the value is −53. Equivalently $203 - 256 = -53$. (A) reads it as unsigned, (C) as one's complement and (D) as sign-magnitude. *([08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md))*

**34. Answer: 935.** $3 \times 256 + 10 \times 16 + 7 = 768 + 160 + 7 = 935$. *([08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md))*

**35. Answer: (A) −2048 to 2047.** An $n$-bit two's-complement number spans $-2^{n-1}$ to $2^{n-1} - 1$. *([08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md))*

**36. Answer: (B) Overflow; the result reads as −96.** $112 + 48 = 160$ exceeds +127. The 8-bit result A0₁₆ reads as $160 - 256 = -96$: two positive operands gave a negative result. The carry into the top bit is 1 and the carry out is 0, so $V = C_8 \oplus C_7 = 1$, and (D) is false. *([08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md), [08-04](../../courses/08-digital-logic-design/chapters/08-04-combinational-building-blocks.md))*

**37. Answer: (A) $AB + C$.** $AB + A\overline{B}C + \overline{A}C = AB + C(A\overline{B} + \overline{A}) = AB + C(\overline{A} + \overline{B}) = AB + C\,\overline{AB} = AB + C$, using $X + \overline{X}Y = X + Y$ twice. *([08-02](../../courses/08-digital-logic-design/chapters/08-02-boolean-algebra-and-gates.md))*

**38. Answer: (A) $(A + \overline{B})\,\overline{C}$.** De Morgan: $\overline{\overline{A}B + C} = \overline{\overline{A}B}\cdot\overline{C} = (A + \overline{B})\,\overline{C}$. *([08-02](../../courses/08-digital-logic-design/chapters/08-02-boolean-algebra-and-gates.md))*

**39. Answer: (A) $\overline{B}\,\overline{D} + BD$.** The minterms with $B = D = 0$ (0, 2, 8, 10) are the four corners of the K-map, one group, and those with $B = D = 1$ (5, 7, 13, 15) are the middle square. $F = \overline{B}\,\overline{D} + BD$ is the XNOR of $B$ and $D$; (D) is its complement. *([08-03](../../courses/08-digital-logic-design/chapters/08-03-logic-minimization.md))*

**40. Answer: 31.** A tree of 2:1 multiplexers for $N$ inputs needs $N - 1$ of them: 16 + 8 + 4 + 2 + 1 = 31, in 5 levels. *([08-04](../../courses/08-digital-logic-design/chapters/08-04-combinational-building-blocks.md))*

**41. Answer: 1.60 ns.** $2 \times 32 = 64$ gate delays at 25 ps: 1.60 ns. *([08-04](../../courses/08-digital-logic-design/chapters/08-04-combinational-building-blocks.md))*

**42. Answer: 1.18 GHz.** $T_c \ge t_{pcq} + t_{pd} + t_{\text{setup}} = 80 + 720 + 50 = 850$ ps, so $f_{\max} = 1/850\ \text{ps} = 1.18$ GHz. *([08-06](../../courses/08-digital-logic-design/chapters/08-06-latches-and-flip-flops.md))*

**43. Answer: (B) violated by 15 ps.** The hold slack is $t_{ccq} + t_{cd} - t_{\text{hold}} = 30 + 15 - 60 = -15$ ps. The clock period does not enter the hold check, so (D) is false: a hold violation is fixed by adding delay to the short path. *([08-06](../../courses/08-digital-logic-design/chapters/08-06-latches-and-flip-flops.md))*

**44. Answer: (B) 7.** $2^6 = 64 < 100 \le 128 = 2^7$, so 7 flip-flops with binary encoding. (C) would be a one-hot-per-digit scheme, and (D) a ring counter. *([08-07](../../courses/08-digital-logic-design/chapters/08-07-registers-counters-shift-registers.md))*

**45. Answer: 1023.** A maximal-length $n$-bit LFSR visits every nonzero state: $2^{10} - 1 = 1023$. The all-zero state is excluded, because XOR feedback of zeros stays at zero. *([08-07](../../courses/08-digital-logic-design/chapters/08-07-registers-counters-shift-registers.md))*

**46. Answer: (A) 4 and 12 flip-flops.** Binary needs $\lceil\log_2 12\rceil = 4$; one-hot uses one flip-flop per state, 12. *([08-08](../../courses/08-digital-logic-design/chapters/08-08-finite-state-machines.md))*

**47. Answer: (A).** Mealy outputs are functions of the state and the present inputs, so they react within the cycle. (B) describes neither machine; Moore outputs depend on the state only. (C) is backward: a Mealy machine never needs more states than the equivalent Moore machine. (D) is false: Moore outputs do not depend on the inputs at all. *([08-08](../../courses/08-digital-logic-design/chapters/08-08-finite-state-machines.md))*

**48. Answer: 18.** 256 K = $2^8 \times 2^{10} = 2^{18}$ words, so 18 address lines; the word width (16) sets the data lines, not the address lines. *([08-11](../../courses/08-digital-logic-design/chapters/08-11-memories-and-programmable-logic.md))*

**49. Answer: (A).** An asynchronous input can change inside a flip-flop's setup and hold window and leave it metastable. Two flip-flops in series give the first one a full clock period to resolve before the second samples it, which makes failures astronomically rare. (B) risks metastability and inconsistent state bits; (C) makes the design asynchronous and bounce-prone; (D) delays the problem without solving it. A mechanical button also bounces, so it needs debouncing as well. *([08-10](../../courses/08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md))*

**50. Answer: 256.** A ROM stores one output word per input combination: $2^6 \times 4 = 256$ bits. *([08-11](../../courses/08-digital-logic-design/chapters/08-11-memories-and-programmable-logic.md))*

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T2.01 | energy delivered | 324 | kJ |
| T2.02 | equivalent resistance | 6.00 | kΩ |
| T2.03 | loaded divider voltage | 3.33 | V |
| T2.04 | node-3 voltage | 5.45 | V |
| T2.05 | current in R2 | 1.09 | A |
| T2.06 | overall voltage gain | 40.9 | — |
| T2.07 | node-2 voltage | 16.0 | V |
| T2.09 | maximum load power | 4.00 | mW |
| T2.10 | input resistance | 667 | Ω |
| T2.11 | inverting amplifier output | -3.00 | V |
| T2.12 | summing amplifier output | -0.100 | V |
| T2.13 | unknown bridge resistance | 3.00 | kΩ |
| T2.14 | voltmeter reading | 4.76 | V |
| T2.15 | capacitor current | 23.5 | mA |
| T2.16 | capacitor voltage at 15 ms | 6.99 | V |
| T2.17 | inductor current at 1 ms | 104 | mA |
| T2.18 | damping ratio | 0.500 | — |
| T2.19 | percent overshoot | 16.3 | % |
| T2.20 | final value | 5.00 | — |
| T2.22 | RMS value | 12.2 | V |
| T2.23 | reactive power | 1380 | var |
| T2.24 | correction capacitor | 6.92 | kvar |
| T2.25 | filter gain at 10 kHz | -20.0 | dB |
| T2.26 | overall voltage gain | 10.0 | — |
| T2.27 | series RLC bandwidth | 318 | Hz |
| T2.28 | Butterworth attenuation at 3 kHz | 19.1 | dB |
| T2.29 | reflected resistance | 200 | Ω |
| T2.30 | return loss | 14.0 | dB |
| T2.31 | three-phase real power | 6.40 | kW |
| T2.32 | line current | 25.5 | A |
| T2.33 | signed value | -53 | — |
| T2.34 | decimal value | 935 | — |
| T2.40 | 2:1 multiplexers | 31 | — |
| T2.41 | adder delay | 1.60 | ns |
| T2.42 | maximum clock frequency | 1.18 | GHz |
| T2.44 | flip-flops for 100 states | 7 | — |
| T2.45 | LFSR period | 1023 | — |
| T2.48 | address lines | 18 | — |
| T2.50 | ROM bits | 256 | — |
