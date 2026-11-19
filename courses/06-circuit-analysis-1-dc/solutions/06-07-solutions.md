# Solutions 06-07 · Linearity and Superposition

Problems: [06-07 problems](../problems/06-07-problems.md) · Chapter: [06-07](../chapters/06-07-linearity-and-superposition.md). Every number below is recomputed by [verify_06_07.py](../verify/verify_06_07.py); the circuits of Problems 06-07.4, 06-07.5, 06-07.7 and 06-07.12 are also confirmed in ngspice ([lab netlist](../labs/06-07-lab/superposition.cir)).

---

## Solutions

### Solution 06-07.1

(a) Only $y = 3x$ is linear. $y = 3x + 2$ is affine (doubling $x$ does not double $y$); $y = x^2$ fails both homogeneity and additivity; $y = |x|$ fails homogeneity for negative scale factors ($|-x| \ne -|x|$) and additivity ($|1 + (-1)| \ne |1| + |-1|$).

(b) Homogeneity: the output scales with the input, so $2\times12/5 = $ **4.8 V**.

(c) A diode's current is exponential in its voltage, so the circuit's output is not proportional to its input; you would have to solve it again (or use a small-signal model for small changes).

### Solution 06-07.2

(a) *10 V alone* (15 V shorted): node a sees $10\parallel10 = 5$ Ω to ground, so $v_a' = 10\times5/(5 + 5) = $ **5 V**. *15 V alone*: node a sees $5\parallel10 = 3.333$ Ω, so $v_a'' = 15\times3.333/(10 + 3.333) = $ **3.75 V**. Total **8.75 V**.

(b) Millman: $(10/5 + 15/10 + 0/10)/(1/5 + 1/10 + 1/10) = 3.5/0.4 = 8.75$ V ✓.

### Solution 06-07.3

Transform 24 V with 6 Ω into **4 A** in parallel with 6 Ω. With the 3 Ω, that is 4 A in parallel with $6\parallel3 = $ **2 Ω**; transform back to 8 V behind 2 Ω. Adding the series 2 Ω: 8 V behind 4 Ω. The 4 Ω load draws $8/(4 + 4) = $ **1 A** at **4 V**.

### Solution 06-07.4

(a) The resistance seen at node a with all sources off is $3\parallel6 = 2$ Ω. *6 V alone*: $6\times6/9 = $ **4 V**. *1 A alone*: $1\times2 = $ **2 V**. *0.5 A drawn out alone*: $-0.5\times2 = $ **−1 V**. Total $v_a = $ **5 V**.

(b) True power: $5^2/6 = $ **4.167 W**. Single-source powers: $(16 + 4 + 1)/6 = $ **3.5 W**. The cross terms ($2\times(4\times2 - 4\times1 - 2\times1)/6 = 0.667$ W) make up the difference.

(c) $(6 - 5)/3 = $ **0.3333 A** out of its + terminal.

### Solution 06-07.5

(a) In kΩ, mA, mS. Node 1: $(v_1 - V_s)/2 + (v_1 - v_2)/2 = 0$, so $v_1 - 0.5v_2 = V_s/2$. Node 2: $(v_2 - v_1)/2 + v_2/4 + 0.25v_1 = I_s$, so $-0.25v_1 + 0.75v_2 = I_s$.

*6 V alone* ($I_s = 0$): row 2 gives $v_1 = 3v_2$; row 1, $2.5v_2 = 3$: $v_2' = $ **1.2 V**, $v_1' = $ **3.6 V**.

*1 mA alone* ($V_s = 0$, VCCS kept): row 1 gives $v_1 = 0.5v_2$; row 2, $0.625v_2 = 1$: $v_2'' = $ **1.6 V**, $v_1'' = $ **0.8 V**.

Sums: $v_1 = $ **4.4 V**, $v_2 = $ **2.8 V**.

(b) Both at once: $v_1 - 0.5v_2 = 3$ and $-0.25v_1 + 0.75v_2 = 1$. From the first, $v_1 = 3 + 0.5v_2$; substituting, $0.625v_2 = 1.75$, so $v_2 = 2.8$ V and $v_1 = 4.4$ V ✓.

(c) Without the VCCS, row 2 would be $-0.5v_1 + 0.75v_2 = 1$ and the 1 mA contribution would come out as $v_1 = 1$ V, $v_2 = 2$ V: wrong, because the VCCS is part of the circuit's structure.

### Solution 06-07.6

(a) Assume $v_{out}$ = 1 V. The 6 kΩ carries $1/6$ mA, and so does the 3 kΩ, so the middle node is at $1 + 3/6 = 1.5$ V. The 2 kΩ shunt carries 0.75 mA, the 1 kΩ series resistor $0.1667 + 0.75 = 0.9167$ mA, and $v_{in} = 1.5 + 0.9167 = 2.4167$ V. So $v_{out}/v_{in} = 1/2.4167 = $ **0.4138** (exactly 12/29).

(b) $12\times0.4138 = $ **4.966 V**.

(c) $R_{in} = 2.4167\ \text{V}/0.9167\ \text{mA} = $ **2.636 kΩ** (exactly 29/11 kΩ).

### Solution 06-07.7

(a) Millman with the load as a fourth branch (0 V behind 0.5 Ω):

$$
V_{bus} = \frac{12.6/0.05 + 12.4/0.06 + 12.2/0.08}{1/0.05 + 1/0.06 + 1/0.08 + 1/0.5} = \frac{252 + 206.67 + 152.5}{20 + 16.667 + 12.5 + 2} = \mathbf{11.94\ V}.
$$

Battery currents $(V_k - V_{bus})/R_k$: **13.11 A**, **7.590 A** and **3.192 A**, all discharging, adding to the load's $11.94/0.5 = $ **23.89 A**.

(b) Without the load, $V_{bus} = 611.17/49.167 = $ **12.43 V**. The 12.6 V battery delivers $(12.6 - 12.43)/0.05 = $ **3.390 A**; the 12.4 V and 12.2 V batteries take **0.5085 A** and **2.881 A**: both are charging, fed by the strongest one, until their voltages equalize.

### Solution 06-07.8

(a) Worst case: $10 + 4 + 6 + 3 = $ **23 mV**, **0.92%** of 2.5 V. RSS: $\sqrt{100 + 16 + 36 + 9} = \sqrt{161} = $ **12.69 mV**, **0.51%**.

(b) $\sqrt{1 + 16 + 36 + 9} = $ **7.874 mV**. The offset dominated; trimming it removed most of the error.

(c) RSS is appropriate when the contributions are independent and random from unit to unit (so they rarely all reach their extremes together), and when a small fraction of units outside the total is acceptable or screened at test. It is wrong for correlated errors (two that move together with temperature should be added directly) and for safety-critical bounds, where worst case is required. And it is only as meaningful as the limits it combines: the result is a 3σ total only if each input limit is a 3σ value.

### Solution 06-07.9

(a) Independent: noise powers (mean squares) add, so $\sqrt{4^2 + 3^2} = $ **5 nV/√Hz**.

(b) Perfectly correlated, in phase: amplitudes add, **7 nV/√Hz**; anticorrelated: **1 nV/√Hz**. These are the two extremes of the cross term in §3.3 of the chapter.

(c) $5\ \text{nV/√Hz}\times\sqrt{10^4\ \text{Hz}} = $ **500 nV** RMS.

(d) Because independent contributions add as squares, the largest one dominates: removing the 3 nV/√Hz source entirely only lowers the total from 5 to 4 nV/√Hz, while halving the 4 nV/√Hz source lowers it to $\sqrt{4 + 9} = 3.6$ nV/√Hz.

### Solution 06-07.10

(a) Total conductance $1 + 0.5 + 0.25 + 0.125 + 0.125 = 2$ mS. The LSB contributes $4\times0.125/2 = $ **0.25 V**, and full scale (1111) is $15\times0.25 = $ **3.75 V**.

(b) With 1.005 kΩ, the MSB conductance is 0.99502 mS and the total 1.99502 mS. Code 0111: $4\times0.875/1.99502 = $ **1.7544 V**. Code 1000: $4\times0.99502/1.99502 = $ **1.9950 V**. The step is 0.2406 V, so DNL $= 0.2406/0.25 - 1 = $ **−0.037 LSB**. INL at 1000: $(1.9950 - 2.000)/0.25 = $ **−0.020 LSB**.

### Solution 06-07.11

(a) $\beta = R_1/(R_1 + R_2) = 1/11$, so the gain is $A/(1 + A\beta) = 10^5/(1 + 9091) = $ **10.9988** (06-06).

(b) The offset source sits in series with the signal at the + input, so both see the same gain. Signal alone: $10.9988\times50 = $ **549.94 mV**. Offset alone: $10.9988\times2 = $ **22.00 mV**. Total: **571.94 mV**.

(c) The ideal gain would give $11\times52 = 572$ mV; the finite $A$ costs 0.011%, while the offset adds a 22 mV error (4% of the signal) that no amount of loop gain removes: it is amplified exactly like the signal.

### Solution 06-07.12

(a) KCL at node d: $(5 - v_d)/1000 + 0.001 = I_S(e^{v_d/V_T} - 1)$. A bracketing root-finder gives $v_d = $ **0.6979 V** (diode current 5.302 mA).

(b) 5 V alone: **0.6925 V** (Problem 06-04.13). 1 mA alone, with the 5 V source shorted (so the 1 kΩ goes to ground): **0.6291 V**. Their sum, **1.322 V**, is nearly double the true answer.

(c) The diode is nonlinear: its stamp depends on its voltage, so the circuit's matrix changes with the sources and the proof of §3.1 does not apply. Superposition works only for *small changes* about an operating point, using the linearized (small-signal) diode: at the 5 V operating point the diode current is 4.307 mA, its incremental resistance $V_T/I_D$ is 6.002 Ω, and 1 mA into $1\ \text{kΩ}\parallel6.002\ \Omega = 5.966$ Ω raises $v_d$ by 5.97 mV, to **0.6985 V**: within 0.6 mV of the exact answer, even though 1 mA is not very small compared with 4.3 mA.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 06-07.1a | output for 12 V | 4.8 | V |
| 06-07.2a | v_a, 10 V alone | 5 | V |
| 06-07.2b | v_a, 15 V alone | 3.75 | V |
| 06-07.2c | v_a | 8.75 | V |
| 06-07.3a | Norton current | 4 | A |
| 06-07.3b | combined shunt resistance | 2 | Ω |
| 06-07.3c | load current | 1 | A |
| 06-07.3d | load voltage | 4 | V |
| 06-07.4a | 6 V contribution | 4 | V |
| 06-07.4b | 1 A contribution | 2 | V |
| 06-07.4c | 0.5 A contribution | −1 | V |
| 06-07.4d | v_a | 5 | V |
| 06-07.4e | true 6 Ω power | 4.167 | W |
| 06-07.4f | sum of single-source powers | 3.5 | W |
| 06-07.4g | 6 V source current | 0.3333 | A |
| 06-07.5a | v_1, 6 V alone | 3.6 | V |
| 06-07.5b | v_2, 6 V alone | 1.2 | V |
| 06-07.5c | v_1, 1 mA alone | 0.8 | V |
| 06-07.5d | v_2, 1 mA alone | 1.6 | V |
| 06-07.5e | v_1 | 4.4 | V |
| 06-07.5f | v_2 | 2.8 | V |
| 06-07.5g | wrong v_1 with the VCCS off | 1 | V |
| 06-07.5h | wrong v_2 with the VCCS off | 2 | V |
| 06-07.6a | voltage ratio | 0.4138 | — |
| 06-07.6b | output for 12 V | 4.966 | V |
| 06-07.6c | input resistance | 2.636 | kΩ |
| 06-07.7a | bus voltage with load | 11.94 | V |
| 06-07.7b | 12.6 V battery current | 13.11 | A |
| 06-07.7c | 12.4 V battery current | 7.590 | A |
| 06-07.7d | 12.2 V battery current | 3.192 | A |
| 06-07.7e | load current | 23.89 | A |
| 06-07.7f | bus voltage, no load | 12.43 | V |
| 06-07.7g | 12.6 V battery current, no load | 3.390 | A |
| 06-07.7h | 12.4 V battery charging current | 0.5085 | A |
| 06-07.7i | 12.2 V battery charging current | 2.881 | A |
| 06-07.8a | worst case | 23 | mV |
| 06-07.8b | worst case, % of full scale | 0.92 | % |
| 06-07.8c | RSS | 12.69 | mV |
| 06-07.8d | RSS, % of full scale | 0.51 | % |
| 06-07.8e | RSS after trimming | 7.874 | mV |
| 06-07.9a | independent total | 5 | nV/√Hz |
| 06-07.9b | correlated total | 7 | nV/√Hz |
| 06-07.9c | anticorrelated total | 1 | nV/√Hz |
| 06-07.9d | RMS in 10 kHz | 500 | nV |
| 06-07.9e | after halving the larger source | 3.6 | nV/√Hz |
| 06-07.10a | LSB | 0.25 | V |
| 06-07.10b | full scale | 3.75 | V |
| 06-07.10c | code 0111 | 1.7544 | V |
| 06-07.10d | code 1000 | 1.9950 | V |
| 06-07.10e | DNL | −0.037 | LSB |
| 06-07.10f | INL at 1000 | −0.020 | LSB |
| 06-07.11a | closed-loop gain | 10.9988 | — |
| 06-07.11b | output from the signal | 549.94 | mV |
| 06-07.11c | output from the offset | 22.00 | mV |
| 06-07.11d | total output | 571.94 | mV |
| 06-07.12a | v_d, both sources | 0.6979 | V |
| 06-07.12b | v_d, 5 V alone | 0.6925 | V |
| 06-07.12c | v_d, 1 mA alone | 0.6291 | V |
| 06-07.12d | superposed sum | 1.322 | V |
| 06-07.12e | small-signal estimate | 0.6985 | V |
| 06-07.12f | diode current, both sources | 5.302 | mA |
| 06-07.12g | incremental resistance | 6.002 | Ω |
