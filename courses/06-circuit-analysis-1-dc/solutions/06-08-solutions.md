# Solutions 06-08 · Thévenin and Norton Equivalents

Problems: [06-08 problems](../problems/06-08-problems.md) · Chapter: [06-08](../chapters/06-08-thevenin-and-norton.md). Every number below is recomputed by [verify_06_08.py](../verify/verify_06_08.py); the circuits of Problems 06-08.2, 06-08.4, 06-08.5 and 06-08.10 are also confirmed in ngspice ([lab netlist](../labs/06-08-lab/thevenin.cir)).

---

## Solutions

### Solution 06-08.1

(a) $I_N = 9/3 = $ **3 mA** in parallel with 3 kΩ. (b) $V_{th} = 0.020\times250 = $ **5 V** in series with 250 Ω. (c) $R_{th} = 2.4\ \text{V}/8\ \text{mA} = $ **300 Ω**.

### Solution 06-08.2

With the 6 Ω removed, the 2 A source's current has only one path: from node a through the 4 Ω into the 12 V source. So $v_{oc} = 12 + 2\times4 = $ **20 V** (the 4 Ω drops 8 V with node a on the high side). Switching off the sources (12 V shorted, 2 A opened) leaves the 4 Ω alone: $R_{th} = $ **4 Ω**. Reconnecting 6 Ω: $v_a = 20\times6/(4 + 6) = 12$ V ✓, as found by superposition in Example 06-07.1.

### Solution 06-08.3

$v_L = 5R_L/(50 + R_L)$ and the error is $50/(50 + R_L)$: 50 Ω → **2.5 V**, **50%**; 450 Ω → **4.5 V**, **10%**; 4950 Ω → **4.95 V**, **1%**. A 1% error needs $R_L = 99R_{th}$.

### Solution 06-08.4

(a) Left divider output: $2.5\times350.7/700.7 = 1.251249$ V; right: 1.25 V. $V_{th} = $ **1.249 mV**. With the excitation shorted, each divider's midpoint sees its two arms in parallel: $R_{th} = 350\parallel350.7 + 350\parallel350 = 175.17 + 175 = $ **350.2 Ω**.

(b) $1.2488\times10{,}000/10{,}350.2 = $ **1.207 mV**: a loss of **3.38%**, larger than the strain signal's own 0.1% nonlinearity: the amplifier's input resistance must be in the error budget.

(c) $R_{th}/(R_{th} + R_{in}) < 0.001$ requires $R_{in} > 999\times350.2 = $ **349.8 kΩ**; in practice an instrumentation amplifier with gigaohm inputs is used (06-10).

### Solution 06-08.5

(a) Open circuit: the input loop gives $i_b = v_s/(R_s + r_\pi + (\beta + 1)R_E)$ and the emitter voltage is $(\beta + 1)i_bR_E$, so the gain is $101\times1/(1 + 2.5 + 101) = $ **0.9665**.

(b) Short the source and inject $i_t$ into the emitter. The emitter node sees $R_E$ to ground and, looking back into the transistor, the base loop: a voltage $v_e$ at the emitter drives $i_b = -v_e/(R_s + r_\pi)$, and the transistor's emitter current $(\beta + 1)i_b$ flows *into* the emitter node from the transistor (negative here, since $i_b < 0$), so $-(\beta + 1)i_b$ leaves through the transistor. KCL: $i_t = v_e/R_E + (\beta + 1)v_e/(R_s + r_\pi)$, so

$$
R_{out} = R_E\parallel\frac{R_s + r_\pi}{\beta + 1} = 1000\parallel34.65\ \Omega = \mathbf{33.49\ \Omega}.
$$

The resistance in the base circuit is divided by $\beta + 1$ when seen from the emitter: the dual of the reflection in Example 06-06.3.

(c) $0.9665\times100/(33.49 + 100) = $ **0.7240**.

### Solution 06-08.6

(a) $R_{th} = (3.70 - 3.58)/2 = $ **60 mΩ**.

(b) At 5 A: $3.70 - 5\times0.060 = $ **3.40 V**; internal loss $5^2\times0.060 = $ **1.5 W**; delivered $5\times3.40 = $ **17.0 W**.

(c) A battery is not a linear network: its open-circuit voltage falls with state of charge and its internal resistance changes with temperature, age, state of charge and current (and has a time-dependent part from chemical diffusion). The equivalent is a small-signal description valid near the conditions where it was measured.

### Solution 06-08.7

(a) Load 1 is the meter alone, 10,000 kΩ; load 2 is 10 kΩ in parallel with 10,000 kΩ = 9.990 kΩ. With $1/v_k = a + b/R_k$:

$$
\frac{1}{4.99750} = a + \frac{b}{10{,}000}, \qquad \frac{1}{3.33222} = a + \frac{b}{9.990},
$$

giving $V_{th} = 1/a = $ **5.000 V** and $R_{th} = b/a = $ **5.000 kΩ**.

(b) Ignoring the meter (taking 4.99750 V as $V_{th}$ and 10 kΩ as the second load) gives $10\times(4.99750/3.33222 - 1) = $ **4.9975 kΩ**: only 0.05% low. Here $R_{th}$ is 2000 times smaller than the meter's resistance, so the meter barely loads the source; in Example 06-08.5 the source resistance was 20 times *larger* than the meter's, and ignoring the meter was disastrous.

### Solution 06-08.8

(a) Type 1: $I = 15.4/44 = $ **0.35 A**, PD voltage $44 - 0.35\times20 = $ **37.0 V**, PD power $15.4 - 0.35^2\times20 = $ **12.95 W**, efficiency **84.1%**. Type 2 Class 4: $I = 30/50 = $ **0.6 A**, **42.5 V**, **25.5 W**, efficiency **85.0%**. Both match the class figures (Example 06-08.4).

(b) A constant-power load satisfies $v(50 - v)/6.25 = 25.5$, that is $v^2 - 50v + 159.4 = 0$; the upper root is $v = (50 + \sqrt{2500 - 637.5})/2 = $ **46.58 V**, so $I = 25.5/46.58 = $ **0.5475 A** and the source delivers $50\times0.5475 = $ **27.37 W** (cable loss 1.87 W). Four-pair powering leaves plenty of margin.

### Solution 06-08.9

(a) The load draws $i = P/v$, and the source gives $i = (V_{th} - v)/R_{th}$. Equating and multiplying by $vR_{th}$: $v^2 - V_{th}v + PR_{th} = 0$. With 12 V, 1 Ω and 20 W: $v = (12 \pm \sqrt{144 - 80})/2 = $ **10 V** or **2 V**. The normal operating point is 10 V (2 A, 4 W lost in the source). The 2 V solution (10 A, 100 W lost) is the "wrong side" of the curve. To see which point is stable, let the voltage dip by δ: the source then supplies $\delta/R_{th}$ more current, while the load (drawing $P/v$) demands $P\delta/v^2$ more. The point recovers if the source's extra current wins, that is if $v^2/P > R_{th}$. At 10 V, $100/20 = 5\ \Omega > 1\ \Omega$: stable (a 1 V dip gives 1 A more from the source against 0.2 A more demanded). At 2 V, $4/20 = 0.2\ \Omega < 1\ \Omega$: a dip makes the load demand 5 A more per volt against 1 A supplied, so the voltage collapses.

(b) Real solutions need $V_{th}^2 \ge 4PR_{th}$, so the largest power is $V_{th}^2/(4R_{th}) = $ **36 W**, at a load voltage of $V_{th}/2 = $ **6 V** (maximum power transfer, 06-09).

(c) There is no operating point: the converter's input voltage collapses, and real converters shut down at their undervoltage lockout (or oscillate between starting and stopping). This is the DC version of the "voltage collapse" studied in power systems.

### Solution 06-08.10

(a) With the drain shorted to small-signal ground, KCL at the source node: $v_s/R_S + v_s/r_o = g_m(1 - v_s)$, so $v_s(1 + 0.02 + 2) = 2$ and $v_s = 0.6623$ V. The current entering the drain from the short is $g_m(1 - v_s) + (0 - v_s)/r_o = 0.6755 - 0.0132 = 0.6623$ mA per volt (equal to $v_s/R_S$, as it must be). With the problem set's convention ($I_N$ flows out of terminal a, the drain, through the short), $I_N = $ **−0.6623 mA** per volt.

(b) The Norton source drives $R_N\parallel R_D = 151\parallel10 = 9.379$ kΩ. The current flows into the drain, out of the $R_D$ side, so $v_d = -0.6623\times9.379 = $ **−6.211 V** per volt: exactly Example 06-06.2's gain, now as "transconductance × total resistance at the output".

### Solution 06-08.11

(a) $10\times\frac{100}{10 + 100}\times\frac{1000}{100 + 1000} = 10\times0.9091\times0.9091 = $ **8.264**.

(b) With 10 MΩ: $10\times\frac{10{,}000}{10{,}010}\times0.9091 = $ **9.082**.

(c) In (a) both interfaces lose 9.1%; in (b) the input loses only 0.1%, and the output interface (100 Ω into 1 kΩ) dominates.

### Solution 06-08.12

(a) With every bit line a voltage source (shorted when switched off), the three resistors are in parallel: $1\parallel2\parallel4 = $ **0.5714 kΩ**, independent of the code.

(b) Code 101: by Millman, $V_{th} = 4\times(1/1 + 1/4)/(1 + 0.5 + 0.25) = $ **2.857 V**.

(c) $2.857\times4/(4 + 0.5714) = $ **2.5 V** ✓. Any load forms a divider with the 571 Ω output resistance and scales every code by the same factor: a gain error, harmless if constant but troublesome if the load varies (or is nonlinear), which is why DAC outputs are usually buffered.

### Solution 06-08.13

(a) Open circuit: the divider gives **$V_{th}$ = 5 V**. With the source shorted, the output sees $2\parallel2 = $ **1 kΩ**. Norton: $I_N = 5/1 = $ **5 mA** in parallel with 1 kΩ.

(b) Either form: $v = 5\times4/(1 + 4) = $ **4 V**, $p = 4^2/4 = $ **4 mW**. That is what an equivalent guarantees.

(c) *Original.* The load takes 1 mA and the 2 kΩ shunt $4/2 = 2$ mA, so the source supplies 3 mA, delivering $10\times3 = 30$ mW. Inside: $3^2\times2 + 2^2\times2 = 18 + 8 = $ **26 mW**; efficiency $4/30 = $ **13.3%**.
*Thévenin.* Its 1 kΩ carries the load's 1 mA: **1 mW** inside, source power 5 mW, efficiency **80%**.
*Norton.* Its 1 kΩ has 4 V across it: **16 mW** inside; the 5 mA source at 4 V delivers 20 mW; efficiency **20%**.
Only the original network's figure is real. The equivalents agree with it, and with each other, at the terminals only; internally they are different circuits.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 06-08.1a | Norton current | 3 | mA |
| 06-08.1b | Thévenin voltage | 5 | V |
| 06-08.1c | R_th | 300 | Ω |
| 06-08.2a | V_th | 20 | V |
| 06-08.2b | R_th | 4 | Ω |
| 06-08.2c | v_a reconnected | 12 | V |
| 06-08.3a | load voltage, 50 Ω | 2.5 | V |
| 06-08.3b | error, 50 Ω | 50 | % |
| 06-08.3c | load voltage, 450 Ω | 4.5 | V |
| 06-08.3d | error, 450 Ω | 10 | % |
| 06-08.3e | load voltage, 4950 Ω | 4.95 | V |
| 06-08.3f | error, 4950 Ω | 1 | % |
| 06-08.3g | load ratio for 1% | 99 | — |
| 06-08.4a | V_th | 1.249 | mV |
| 06-08.4b | R_th | 350.2 | Ω |
| 06-08.4c | voltage at the amplifier | 1.207 | mV |
| 06-08.4d | loading loss | 3.38 | % |
| 06-08.4e | input resistance for 0.1% | 349.8 | kΩ |
| 06-08.5a | open-circuit gain | 0.9665 | — |
| 06-08.5b | output resistance | 33.49 | Ω |
| 06-08.5c | gain into 100 Ω | 0.7240 | — |
| 06-08.5d | base-side resistance seen from the emitter | 34.65 | Ω |
| 06-08.6a | R_th | 60 | mΩ |
| 06-08.6b | voltage at 5 A | 3.40 | V |
| 06-08.6c | internal loss at 5 A | 1.5 | W |
| 06-08.6d | delivered power at 5 A | 17.0 | W |
| 06-08.7a | V_th | 5.000 | V |
| 06-08.7b | R_th | 5.000 | kΩ |
| 06-08.7c | R_th ignoring the meter | 4.9975 | kΩ |
| 06-08.8a | Type 1 current | 0.35 | A |
| 06-08.8b | Type 1 PD voltage | 37.0 | V |
| 06-08.8c | Type 1 PD power | 12.95 | W |
| 06-08.8d | Type 1 efficiency | 84.1 | % |
| 06-08.8e | Type 2 current | 0.6 | A |
| 06-08.8f | Type 2 PD voltage | 42.5 | V |
| 06-08.8g | Type 2 PD power | 25.5 | W |
| 06-08.8h | Type 2 efficiency | 85.0 | % |
| 06-08.8i | 50 m PD voltage | 46.58 | V |
| 06-08.8j | 50 m current | 0.5475 | A |
| 06-08.8k | 50 m source power | 27.37 | W |
| 06-08.8l | 50 m cable loss | 1.87 | W |
| 06-08.9a | upper solution | 10 | V |
| 06-08.9b | lower solution | 2 | V |
| 06-08.9c | maximum power | 36 | W |
| 06-08.9d | voltage at maximum power | 6 | V |
| 06-08.10a | v_s with the drain shorted | 0.6623 | V |
| 06-08.10b | Norton current per volt (out of the drain) | −0.6623 | mA |
| 06-08.10c | R_N ∥ R_D | 9.379 | kΩ |
| 06-08.10d | gain | −6.211 | — |
| 06-08.11a | overall gain, 100 kΩ input | 8.264 | — |
| 06-08.11b | overall gain, 10 MΩ input | 9.082 | — |
| 06-08.12a | R_th | 0.5714 | kΩ |
| 06-08.12b | V_th, code 101 | 2.857 | V |
| 06-08.12c | output with R_L | 2.5 | V |
| 06-08.13a | V_th | 5 | V |
| 06-08.13b | R_th | 1 | kΩ |
| 06-08.13c | I_N | 5 | mA |
| 06-08.13d | load voltage | 4 | V |
| 06-08.13e | load power | 4 | mW |
| 06-08.13f | internal power, original | 26 | mW |
| 06-08.13g | internal power, Thévenin form | 1 | mW |
| 06-08.13h | internal power, Norton form | 16 | mW |
| 06-08.13i | efficiency, original | 13.3 | % |
| 06-08.13j | efficiency, Thévenin form | 80 | % |
| 06-08.13k | efficiency, Norton form | 20 | % |
