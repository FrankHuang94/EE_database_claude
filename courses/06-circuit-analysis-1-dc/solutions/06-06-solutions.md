# Solutions 06-06 · Dependent Sources

Problems: [06-06 problems](../problems/06-06-problems.md) · Chapter: [06-06](../chapters/06-06-dependent-sources.md). Every number below is recomputed by [verify_06_06.py](../verify/verify_06_06.py); the circuits of Problems 06-06.3, 06-06.5, 06-06.7, 06-06.11, 06-06.12 and 06-06.14 are also confirmed in ngspice ([lab netlist](../labs/06-06-lab/dependent.cir)).

---

## Solutions

### Solution 06-06.1

(a) A current set by a voltage: a **VCCS** with $g$ = 0.04 S = **40 mS**: a MOSFET's $g_m$. (b) A voltage set by a current: a **CCVS** with $r$ = **5 kΩ**: a transimpedance amplifier, which turns a photodiode's current into a voltage. (c) A current set by a current: a **CCCS** with $\beta$ = **80**: a bipolar transistor. (d) A voltage set by a voltage: a **VCVS** with $\mu$ = **−20**: an inverting amplifier.

### Solution 06-06.2

(a) $v_x = 2\times3/(1 + 3) = $ **1.5 V**. The VCVS produces $10\times1.5 = 15$ V, divided between 100 Ω and 500 Ω: $v_L = 15\times500/600 = $ **12.5 V**.

(b) Load: $12.5^2/500 = $ **0.3125 W**. The VCVS drives $15/600 = 25$ mA at 15 V: **0.375 W** (the 100 Ω takes the other 0.0625 W). The 2 V source drives $2/4\ \text{kΩ} = 0.5$ mA: **1 mW**.

(c) The dependent source delivers 375 times the input power. In a real amplifier that power comes from the DC supply, which the model does not show; the dependent source stands for the supply's power steered by the input.

### Solution 06-06.3

(a) In kΩ, mA and V, with $i_x = v_1/5$. Node 1: $v_1/5 + (v_1 - v_2)/10 = 2$. Node 2: $(v_2 - v_1)/10 + v_2/2 = 4i_x = 0.8\,v_1$. Moving the dependent term to the left:

$$
\begin{bmatrix} 0.3 & -0.1 \\ -0.1 - 0.8 & 0.6 \end{bmatrix}
\begin{bmatrix} v_1 \\ v_2 \end{bmatrix} =
\begin{bmatrix} 2 \\ 0 \end{bmatrix},
$$

with $G_{21} = -0.9 \ne G_{12} = -0.1$ mS: not symmetric. Determinant $0.18 - 0.09 = $ **0.09 mS²**.

(b) Row 2 gives $v_2 = 1.5\,v_1$; row 1, $0.3v_1 - 0.15v_1 = 2$: $v_1 = $ **13.33 V**, $v_2 = $ **20 V**, $i_x = $ **2.667 mA**, and the CCCS pushes $4\times2.667 = $ **10.67 mA**.

(c) The 2 mA source delivers $2\times13.33 = $ **26.67 mW**; the CCCS pushes 10.67 mA into a node at 20 V: **213.3 mW**. Resistors: $13.33^2/5 + 6.667^2/10 + 20^2/2 = 35.56 + 4.44 + 200 = $ **240.0 mW** $= 26.67 + 213.3$ ✓.

### Solution 06-06.4

(a) Node 2 with general $g$: $-0.25v_1 + 0.5v_2 + g\,v_1 = 0$, so $v_2 = (0.25 - g)v_1/0.5 = (0.5 - 2g)\,v_1$. Node 1: $0.75v_1 - 0.25v_2 = 1$; substituting, $(0.75 - 0.125 + 0.5g)\,v_1 = 1$, so $v_1 = 1/(0.625 + 0.5g)$ ✓ (at $g$ = 1 this gives Example 06-06.1's 0.8889 V).

(b) $\det\begin{bmatrix} 0.75 & -0.25 \\ g - 0.25 & 0.5\end{bmatrix} = 0.375 + 0.25(g - 0.25) = 0.3125 + 0.25g$, which vanishes at $g = $ **−1.25 mS**. A negative $g$ means the VCCS pushes current *into* node 2 when $v_1$ rises; that raises $v_2$, which through the 4 kΩ raises $v_1$ further: positive feedback.

(c) At $g = -1$ mS the determinant is **0.0625 mS²** and $v_1 = 1/0.125 = $ **8 V**, $v_2 = 2.5\times8 = $ **20 V**: nine times Example 06-06.1's $v_1$ for the same 1 mA input. Near the singular gain the circuit amplifies its own disturbances enormously; at $g$ = −1.25 mS it would have no finite DC solution. In a real circuit with only node capacitances this is a growing response that does not oscillate (a real pole at the origin): the circuit latches up or runs away.

### Solution 06-06.5

(a) Mesh 1: $10 = (2 + 4)i_1 - 4i_2$. Mesh 2, with the CCVS a rise of $3i_1$: $4(i_2 - i_1) + 6i_2 = 3i_1$, that is, $-7i_1 + 10i_2 = 0$. Matrix $\begin{bmatrix} 6 & -4 \\ -7 & 10\end{bmatrix}$ Ω, not symmetric; determinant $60 - 28 = $ **32 Ω²**.

(b) $i_1 = 10\times10/32 = $ **3.125 A** and $i_2 = 70/32 = $ **2.1875 A**.

(c) The 10 V source delivers $10\times3.125 = $ **31.25 W**. The CCVS has value $3\times3.125 = 9.375$ V and carries $i_2$ in its rise direction: **20.51 W**. Resistors: $2\times3.125^2 + 4\times0.9375^2 + 6\times2.1875^2 = 19.53 + 3.52 + 28.71 = $ **51.76 W** $= 31.25 + 20.51$ ✓.

### Solution 06-06.6

(a) $g_mr_o = 4\times25 = $ **100**.

(b) The VCCS $g_mv_{gs}$ flows into $r_o\parallel R_D\parallel R_L = 25\parallel5\parallel20 = $ **3.448 kΩ**, so $v_{out}/v_{gs} = -4\times3.448 = $ **−13.79**.

(c) Looking back from the load with $v_{gs} = 0$, the VCCS is off (an open circuit), leaving $r_o\parallel R_D = $ **4.167 kΩ**.

### Solution 06-06.7

(a) $g_m = I_C/V_T = 1\ \text{mA}/25.852\ \text{mV} = $ **38.68 mS** for either $\beta$. $r_\pi = \beta/g_m$: **3.102 kΩ** at $\beta$ = 120 and **1.551 kΩ** at $\beta$ = 60.

(b) By the mesh analysis of Example 06-06.3 with $R_E = 0$: $v_o/v_s = -\beta R_C/(R_s + r_\pi)$. $\beta$ = 120: $-600/5.102 = $ **−117.6**; $\beta$ = 60: $-300/3.551 = $ **−84.48**. The gain magnitude falls by **28.2%**.

(c) With $R_E$ = 200 Ω: $v_o/v_s = -\beta R_C/\bigl(R_s + r_\pi + (\beta + 1)R_E\bigr)$. $\beta$ = 120: $-600/(2 + 3.102 + 24.2) = $ **−20.48**; $\beta$ = 60: $-300/(2 + 1.551 + 12.2) = $ **−19.05**. Now the gain falls by only **7.0%**: a factor of four less sensitivity for a factor of six less gain.

(d) $R_{in} = r_\pi + (\beta + 1)R_E = 3.102 + 24.2 = $ **27.30 kΩ**, and the gain is $-600/27.30 = $ **−21.98**, close to $-R_C/R_E = $ **−25**. The difference: dividing numerator and denominator by $\beta + 1$, the gain is $-\frac{\beta}{\beta+1}\cdot\frac{R_C}{R_E + r_\pi/(\beta + 1)}$, and $r_\pi/(\beta + 1) \approx 1/g_m = 25.9$ Ω adds to $R_E$.

### Solution 06-06.8

Inject $i_t$ into the drain. It flows through the parallel combination of $r_o$ and the VCCS to the source node, then through $R_S$: $v_s = i_tR_S$. The gate is grounded, so $v_{gs} = -v_s = -i_tR_S$ and the VCCS carries $g_mv_{gs} = -g_mR_Si_t$ from drain to source. KCL at the drain: the current in $r_o$ is $i_t - g_mv_{gs} = i_t(1 + g_mR_S)$. So

$$
v_d = v_s + r_o\,i_t(1 + g_mR_S) \;\Rightarrow\; R_{out} = \frac{v_d}{i_t} = R_S + r_o(1 + g_mR_S).
$$

With the numbers: $1 + 50\times(1 + 2\times1) = $ **151 kΩ**, about three times $r_o$. The VCCS fights any change in current, so the drain looks stiffer.

### Solution 06-06.9

(a) $R_f/(1 + A) = 1\ \text{MΩ}/201 = $ **4.975 kΩ** (Example 06-06.4).

(b) The 10 kΩ source resistance and 4.975 kΩ divide the 10 mV: $v_{in} = 10\times4.975/14.975 = $ **3.322 mV**, and $v_{out} = -200\times3.322 = $ **−664.5 mV**.

(c) Overall gain $-664.5/10 = $ **−66.45**. The Miller effect makes the 1 MΩ feedback resistor look like 4.975 kΩ at the input, which loads the 10 kΩ source and throws away two-thirds of the signal before it is amplified.

### Solution 06-06.10

(a) The node sees 10 kΩ in parallel with $-R_n$: conductance $1/10 - 1/R_n$ mS. For $R_n$ = 20 kΩ: $0.1 - 0.05 = 0.05$ mS, so $v = 1/0.05 = $ **20 V**. For 12.5 kΩ: $0.1 - 0.08 = 0.02$ mS, so $v = $ **50 V**.

(b) As $R_n \to 10$ kΩ the net conductance, which is the 1 × 1 nodal matrix, goes to zero: the matrix becomes singular and the voltage grows without bound. Physically the negative resistance supplies exactly the power the 10 kΩ dissipates; any small disturbance persists or grows. Combined with a resonant LC tank, a negative resistance that cancels the tank's loss is the condition for an oscillator ([12-09](../../12-electronics-2/chapters/12-09-oscillators.md)); with capacitance alone it latches instead.

(c) KCL at the node with the VCCS pushing $g\,v$ in: $v/R - g\,v = I$, so the VCCS adds a conductance $-g$, a resistance $-1/g$. For $R_n$ = 20 kΩ, $g = $ **50 µS** (0.05 mS).

### Solution 06-06.11

(a) With $v_+ = 0$, the output is $v_{out} = -A\,v_-$, so $v_- = -v_{out}/A$. KCL at the − input (no input current): $(v_- - v_{in})/R_1 + (v_- - v_{out})/R_2 = 0$. Substituting $v_-$ and multiplying by $R_2$:

$$
-\frac{v_{out}}{A}\Bigl(\frac{R_2}{R_1} + 1\Bigr) - \frac{R_2}{R_1}v_{in} - v_{out} = 0
\;\Rightarrow\;
\frac{v_{out}}{v_{in}} = -\frac{R_2/R_1}{1 + (1 + R_2/R_1)/A}.
$$

(b) $-10/(1 + 11/10^4) = $ **−9.9890**: an error of **1099 ppm** (0.11%), about $(1 + R_2/R_1)/A$.

(c) For $v_{in}$ = 1 V, $v_{out} = -9.989$ V and $v_- = 9.989/10^4 = $ **0.9989 mV**: close to ground, but not exactly ("virtual ground").

(d) $R_{in} = v_{in}/i_{in} = R_1/(1 - v_-/v_{in}) = 1/(1 - 0.000999) = $ **1.0010 kΩ**, essentially $R_1$.

### Solution 06-06.12

Unknowns $(v_1, v_2, v_3, j)$, in S and A. R1 (1 mS) adds ±0.001 between nodes 1 and 2; R2 adds 0.001 at (2,2); R3 adds 0.0005 at (3,3); G1's current $0.01\,v_2$ leaves node 3, adding +0.01 at row 3, column 2 (and nothing at row 2, column 3); V1 adds the voltage-source row and column:

$$
\begin{bmatrix}
0.001 & -0.001 & 0 & 1 \\
-0.001 & 0.002 & 0 & 0 \\
0 & 0.01 & 0.0005 & 0 \\
1 & 0 & 0 & 0
\end{bmatrix}
\begin{bmatrix} v_1 \\ v_2 \\ v_3 \\ j \end{bmatrix} =
\begin{bmatrix} 0 \\ 0 \\ 0 \\ 1 \end{bmatrix}.
$$

Row 4: $v_1$ = 1 V. Row 2: $v_2$ = **0.5 V**. Row 3: $0.01\times0.5 + 0.0005v_3 = 0$, so $v_3$ = **−10 V**. Row 1: $0.001 - 0.0005 + j = 0$, so $j$ = **−0.5 mA** (V1 delivers 0.5 mA). Gain $v_3/v_1$ = **−10**.

### Solution 06-06.13

(a) KCL at the source node (drain grounded, so $r_o$ and $R_S$ both go from the source node to ground): $v_s/(r_o\parallel R_S) = g_m(v_g - v_s)$, so

$$
\frac{v_s}{v_g} = \frac{g_m(r_o\parallel R_S)}{1 + g_m(r_o\parallel R_S)} = \frac{2\times1.923}{1 + 3.846} = \mathbf{0.7937},
$$

with $r_o\parallel R_S = 50\parallel2 = $ **1.923 kΩ**.

(b) With $v_g = 0$ and a test voltage $v_t$ at the source, $i_t = v_t/(r_o\parallel R_S) + g_mv_t$ (the VCCS now carries $g_m v_t$ out of the node), so $R_{out} = (r_o\parallel R_S)\parallel(1/g_m) = 1.923\parallel0.5 = $ **396.8 Ω**, dominated by $1/g_m$ = 500 Ω: the transistor itself acts like a resistor $1/g_m$.

### Solution 06-06.14

(a) KCL at the output node: the current from the supply through $R_L$ equals the mirror's 0.1 mA plus the current in $r_o$. In kΩ, mA and V: $(5 - v_o)/20 = 0.1 + v_o/100$, so $5 - v_o = 2 + 0.2\,v_o$ and $v_o = $ **2.5 V**. The output current is $0.1 + 2.5/100 = $ **0.125 mA**: a **25%** error.

(b) With $r_o$ = 1 MΩ: $5 - v_o = 2 + 0.02\,v_o$, so $v_o = $ **2.941 V**, the current is $0.1 + 0.002941 = $ **0.1029 mA**, and the error is **2.94%**.

(c) An ideal current source's current does not depend on its voltage, which is what infinite output resistance means. With finite $r_o$, the error is the output voltage divided by $r_o$ relative to the nominal current, so stacking devices to raise $r_o$ (cascoding, Problem 06-06.8) is the standard cure.

### Solution 06-06.15

(a) The dependent source joins two non-reference nodes, so nodes 1 and 2 form a supernode. Its KCL (current in through the 4 Ω, out through 3 Ω and 6 Ω) is $(12 - v_1)/4 = v_1/3 + v_2/6$. The constraint is $v_1 - v_2 = 2i_x$ with the controlling current written in node voltages, $i_x = (12 - v_1)/4$, so $v_2 = v_1 - (12 - v_1)/2 = 1.5v_1 - 6$. Substituting: $3 - 0.25v_1 = v_1/3 + 0.25v_1 - 1$, so $0.8333v_1 = 4$: **$v_1$ = 4.8 V**, **$v_2$ = 1.2 V**, **$i_x$ = 1.8 A** (and the source's voltage is $2\times1.8 = 3.6$ V).

(b) Node 2 connects only to the source and the 6 Ω, so the source's current, from node 1 to node 2 through it, is $1.2/6 = 0.2$ A, entering its + terminal: it absorbs $3.6\times0.2 = $ **0.72 W**. Balance: the 12 V source delivers $12\times1.8 = 21.6$ W; the resistors absorb $1.8^2\times4 + 4.8^2/3 + 1.2^2/6 = 12.96 + 7.68 + 0.24 = 20.88$ W; $20.88 + 0.72 = 21.6$ ✓.

(c) Sense $i_x$ with a zero-volt source in series with the 4 Ω, then use an H element (CCVS) whose value is volts per ampere of the sensing source's current:

```text
V1   a  0  DC 12
Vx   a  ax DC 0        ; senses i_x, flowing a -> ax
R4   ax n1 4
H1   n1 n2 Vx 2        ; v(n1) - v(n2) = 2 * i(Vx)
R3   n1 0  3
R6   n2 0  6
```

### Solution 06-06.16

(a) The dependent source points up in the branch shared by both meshes: mesh 2's clockwise current flows up there and mesh 1's down, so $i_2 - i_1 = 0.5i_x$, with $i_x = i_2$ (the 4 Ω carries only mesh 2's current, downward). Hence $i_1 = 0.5i_2$. The supermesh KVL around the outside, avoiding the current source: $10 = 2i_1 + 3i_2 + 4i_2 = i_2 + 7i_2$, so **$i_2$ = 1.25 A** and **$i_1$ = 0.625 A**.

(b) KVL around mesh 1 gives the source's voltage (node 2 relative to node 0): $10 - 2\times0.625 = $ **8.75 V**. Its current, $i_2 - i_1 = 0.625$ A, leaves its top (+) terminal, so it delivers $8.75\times0.625 = $ **5.469 W**. Balance: the 10 V source delivers 6.25 W; the resistors absorb $2(0.625)^2 + 3(1.25)^2 + 4(1.25)^2 = 0.781 + 4.688 + 6.25 = 11.72$ W $= 6.25 + 5.469$ ✓. The dependent source supplies most of the power: in a real circuit it is a transistor drawing that power from a hidden supply.

(c) Sense $i_x$ with a zero-volt source in series with the 4 Ω, then use an F element (CCCS). Its current flows from its first node, through the source, to its second, so "from node 0 into node 2" is written `0 n2`:

```text
V1  n1 0  DC 10
R2  n1 n2 2
R3  n2 n3 3
Vx  n3 x3 DC 0        ; senses i_x, flowing n3 -> x3
R4  x3 0  4
F1  0  n2 Vx 0.5      ; 0.5 * i(Vx) from node 0 through F1 into n2
```

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 06-06.1a | VCCS gain | 40 | mS |
| 06-06.1b | CCVS gain | 5 | kΩ |
| 06-06.1c | CCCS gain | 80 | — |
| 06-06.1d | VCVS gain | −20 | — |
| 06-06.2a | v_x | 1.5 | V |
| 06-06.2b | load voltage | 12.5 | V |
| 06-06.2c | load power | 0.3125 | W |
| 06-06.2d | VCVS power | 0.375 | W |
| 06-06.2e | input source power | 1 | mW |
| 06-06.3a | determinant | 0.09 | mS² |
| 06-06.3b | v_1 | 13.33 | V |
| 06-06.3c | v_2 | 20 | V |
| 06-06.3d | i_x | 2.667 | mA |
| 06-06.3e | CCCS current | 10.67 | mA |
| 06-06.3f | power from the 2 mA source | 26.67 | mW |
| 06-06.3g | power from the CCCS | 213.3 | mW |
| 06-06.3h | total resistor power | 240.0 | mW |
| 06-06.4a | singular gain | −1.25 | mS |
| 06-06.4b | determinant at g = −1 mS | 0.0625 | mS² |
| 06-06.4c | v_1 at g = −1 mS | 8 | V |
| 06-06.4d | v_2 at g = −1 mS | 20 | V |
| 06-06.5a | determinant | 32 | Ω² |
| 06-06.5b | i_1 | 3.125 | A |
| 06-06.5c | i_2 | 2.1875 | A |
| 06-06.5d | power from the 10 V source | 31.25 | W |
| 06-06.5e | power from the CCVS | 20.51 | W |
| 06-06.5f | total resistor power | 51.76 | W |
| 06-06.6a | intrinsic gain | 100 | — |
| 06-06.6b | load seen by the VCCS | 3.448 | kΩ |
| 06-06.6c | voltage gain | −13.79 | — |
| 06-06.6d | output resistance | 4.167 | kΩ |
| 06-06.7a | g_m | 38.68 | mS |
| 06-06.7b | r_π at β = 120 | 3.102 | kΩ |
| 06-06.7c | r_π at β = 60 | 1.551 | kΩ |
| 06-06.7d | gain, no R_E, β = 120 | −117.6 | — |
| 06-06.7e | gain, no R_E, β = 60 | −84.48 | — |
| 06-06.7f | change, no R_E | 28.2 | % |
| 06-06.7g | gain, R_E, β = 120 | −20.48 | — |
| 06-06.7h | gain, R_E, β = 60 | −19.05 | — |
| 06-06.7i | change, with R_E | 7.0 | % |
| 06-06.7j | input resistance, (d) | 27.30 | kΩ |
| 06-06.7k | gain, (d) | −21.98 | — |
| 06-06.8a | output resistance | 151 | kΩ |
| 06-06.9a | Miller input resistance | 4.975 | kΩ |
| 06-06.9b | amplifier input voltage | 3.322 | mV |
| 06-06.9c | output voltage | −664.5 | mV |
| 06-06.9d | overall gain | −66.45 | — |
| 06-06.10a | node voltage, R_n = 20 kΩ | 20 | V |
| 06-06.10b | node voltage, R_n = 12.5 kΩ | 50 | V |
| 06-06.10c | VCCS gain for −20 kΩ | 50 | µS |
| 06-06.11a | closed-loop gain | −9.9890 | — |
| 06-06.11b | gain error | 1099 | ppm |
| 06-06.11c | voltage at the − input | 0.9989 | mV |
| 06-06.11d | input resistance | 1.0010 | kΩ |
| 06-06.12a | v_2 | 0.5 | V |
| 06-06.12b | v_3 | −10 | V |
| 06-06.12c | j | −0.5 | mA |
| 06-06.12d | gain v_3/v_1 | −10 | — |
| 06-06.13a | r_o ∥ R_S | 1.923 | kΩ |
| 06-06.13b | follower gain | 0.7937 | — |
| 06-06.13c | output resistance | 396.8 | Ω |
| 06-06.14a | output voltage, r_o = 100 kΩ | 2.5 | V |
| 06-06.14b | output current, r_o = 100 kΩ | 0.125 | mA |
| 06-06.14c | error, r_o = 100 kΩ | 25 | % |
| 06-06.14d | output voltage, r_o = 1 MΩ | 2.941 | V |
| 06-06.14e | output current, r_o = 1 MΩ | 0.1029 | mA |
| 06-06.14f | error, r_o = 1 MΩ | 2.94 | % |
| 06-06.15a | v_1 | 4.8 | V |
| 06-06.15b | v_2 | 1.2 | V |
| 06-06.15c | i_x | 1.8 | A |
| 06-06.15d | power absorbed by the dependent source | 0.72 | W |
| 06-06.16a | i_2 | 1.25 | A |
| 06-06.16b | i_1 | 0.625 | A |
| 06-06.16c | voltage across the dependent source | 8.75 | V |
| 06-06.16d | power delivered by the dependent source | 5.469 | W |
