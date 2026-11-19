# Solutions 06-09 · Maximum Power Transfer

Problems: [06-09 problems](../problems/06-09-problems.md) · Chapter: [06-09](../chapters/06-09-maximum-power-transfer.md). Every number below is recomputed by [verify_06_09.py](../verify/verify_06_09.py); the load sweeps of Problems 06-09.1, 06-09.5 and 06-09.12 are also confirmed in ngspice ([lab netlist](../labs/06-09-lab/maxpower.cir)).

---

## Solutions

### Solution 06-09.1

(a) $p_{max} = 6^2/(4\times300) = $ **30 mW** into **300 Ω**.

(b) 100 Ω: $36\times100/400^2 = $ **22.5 mW**; 900 Ω: $36\times900/1200^2 = $ **22.5 mW**. They are equal because $100\times900 = 300^2$: loads $R_{th}/k$ and $kR_{th}$ receive the same power (here $k$ = 3).

### Solution 06-09.2

(a) $\eta = 4/(1 + 4) = $ **80%**. (b) $p/p_{max} = 4\times4/(1 + 4)^2 = 16/25 = $ **0.64**, and $4\times0.8\times0.2 = 0.64$ ✓.

### Solution 06-09.3

$R_{th}$ = 2 kΩ, so the matched load is **2 kΩ**. The 10 mA splits equally: 5 mA into the load at **10 V**, giving $p_{max} = I_N^2R_{th}/4 = 0.01^2\times2000/4 = $ **50 mW**.

### Solution 06-09.4

(a) $4^2/(4\times3\ \text{kΩ}) = $ **1.333 mW**, into a 3 kΩ load.

(b) $(119.05\ \text{mV})^2/(4\times1023.8\ \Omega) = $ **3.461 µW**, into a **1.024 kΩ** meter. That is all the power the bridge's imbalance can give any meter, which is why galvanometers needed to be extraordinarily sensitive.

### Solution 06-09.5

(a) $48^2/(4\times0.25) = $ **2304 W**, at 96 A and 50% efficiency.

(b) $R_L = 0.95\times0.25/0.05 = $ **4.75 Ω**; the current is $48/5 = 9.6$ A and the load receives $9.6^2\times4.75 = $ **437.8 W**.

(c) At 30 A the internal drop is 7.5 V, so the load sees **40.5 V** and receives $30\times40.5 = $ **1215 W** at **84.4%** efficiency (the pack dissipates 225 W, a thermal problem in itself).

### Solution 06-09.6

(a) The resistance may drop at most 0.25 V at 2 A: **0.125 Ω** in total.

(b) $4.75/5 = $ **95%**.

(c) The theorem picks a load for a given source. Here the load (the device) is given and we design the source: lower resistance is strictly better (more voltage at the device, less loss). A supply "matched" to a 2.375 Ω device would put only 2.5 V across it.

### Solution 06-09.7

$R_L$ = **33.49 Ω** and $p_{max} = 0.9665^2/(4\times0.03349) = $ **6.973 mW** per V² of input (in V and kΩ). The real limit is large-signal: the transistor must source the load current through its emitter, and with a resistive emitter load it can only pull the output down as far as $R_E$ allows; the swing (and the bias current) caps the deliverable power well before the small-signal formula matters for large inputs.

### Solution 06-09.8

(a) $v = V_{th}R_L/(R_{th} + R_L)$. For 100 Ω: $100/50 = $ **2 V**, power $4/100 = $ **40 mW**. For 60 Ω: $60/10 = $ **6 V**, power $36/60 = $ **600 mW**.

(b) The denominator $R_L - 50$ goes to zero: voltage, current and power grow without bound. In a real circuit the dependent source saturates or the circuit oscillates.

(c) The derivation found a stationary point of $p(R_L)$ assuming $R_{th} > 0$; with $R_{th} < 0$, $p$ has a pole at $R_L = -R_{th}$ instead of a maximum, and $V_{th}^2/4R_{th}$ (negative) is meaningless.

### Solution 06-09.9

(a) $\Delta T$ = 20 K: $V_{oc}$ = 0.8 V, $p_{max} = 0.8^2/16 = $ **40 mW**. $\Delta T$ = 10 K: $V_{oc}$ = 0.4 V, $p_{max} = $ **10 mW** (power scales with $\Delta T^2$).

(b) At 20 K, 0.4 V is exactly $V_{oc}/2$: **40 mW**. At 10 K, 0.4 V equals $V_{oc}$: no current flows, **0 mW**.

(c) A fixed 4 Ω equals $R_{th}$ at both temperatures, so it receives the maximum: **40 mW** and **10 mW**.

(d) For a linear source with constant internal resistance, a fixed matched *resistance* tracks the maximum automatically, while a fixed *voltage* does not. Real harvesters' internal resistances change with conditions, and solar cells are nonlinear, so practical converters track the maximum by measurement.

### Solution 06-09.10

(a) Minimum loss: $76.71/\sqrt{2.1} = $ **52.93 Ω**; maximum power: $30.0/\sqrt{2.1} = $ **20.70 Ω** (the optimal ratios $b/a$ are unchanged; only $Z_0$ scales with $1/\sqrt{\varepsilon_r}$).

(b) $b/a = \exp(50\sqrt{2.1}/60) = $ **3.345**. Loss relative to the minimum: $f(3.345)/f(3.591) = $ **1.002** (0.2% above the optimum); power capacity relative to the maximum: $g(3.345)/g(1.649) = $ **0.587**. With a solid dielectric, 50 Ω is essentially the low-loss design.

### Solution 06-09.11

(a) By voltage division, $8/8.05 = $ **99.38%** of the open-circuit voltage reaches the speaker. If the 0.05 Ω were a physical resistor, the same current would flow through it and the speaker, so the same 99.38% would be the fraction of power delivered (0.62% lost in it). In a feedback amplifier the 0.05 Ω is mostly created by feedback and dissipates nothing itself; the amplifier's efficiency is then set by its output transistors.

(b) $8/0.05 = $ **160**.

(c) A matched amplifier would deliver only half its open-circuit voltage to the speaker, so it would need twice the voltage swing for the same speaker power; if its 8 Ω were a physical resistor it would also waste as much power as it delivers and run hot. And it would lose control of the speaker: the low output resistance also damps the speaker cone's own motion (hence "damping factor"), which an 8 Ω output would not.

### Solution 06-09.12

(a) From Example 06-07.3 the two sources combine (Millman) into **8.571 V** behind **1.714 Ω**. The matched load is 1.714 Ω, receiving $8.571^2/(4\times1.714) = $ **10.71 W** at a load voltage of 4.286 V.

(b) At 4.286 V the 12 V source delivers $(12 - 4.286)/4 = $ **1.929 A** and the 6 V source $(6 - 4.286)/3 = $ **0.5714 A**. Both deliver power; neither absorbs.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 06-09.1a | maximum power | 30 | mW |
| 06-09.1b | matched load | 300 | Ω |
| 06-09.1c | power into 100 Ω | 22.5 | mW |
| 06-09.1d | power into 900 Ω | 22.5 | mW |
| 06-09.2a | efficiency | 80 | % |
| 06-09.2b | fraction of maximum | 0.64 | — |
| 06-09.3a | matched load | 2 | kΩ |
| 06-09.3b | load voltage | 10 | V |
| 06-09.3c | maximum power | 50 | mW |
| 06-09.4a | maximum power, divider | 1.333 | mW |
| 06-09.4b | maximum power to the meter | 3.461 | µW |
| 06-09.4c | matched meter resistance | 1.024 | kΩ |
| 06-09.5a | maximum power | 2304 | W |
| 06-09.5b | current at maximum power | 96 | A |
| 06-09.5c | load for 95% | 4.75 | Ω |
| 06-09.5d | power at 95% | 437.8 | W |
| 06-09.5e | current at 95% | 9.6 | A |
| 06-09.5f | load voltage at 30 A | 40.5 | V |
| 06-09.5g | power at 30 A | 1215 | W |
| 06-09.5h | efficiency at 30 A | 84.4 | % |
| 06-09.5i | pack dissipation at 30 A | 225 | W |
| 06-09.6a | maximum total resistance | 0.125 | Ω |
| 06-09.6b | efficiency | 95 | % |
| 06-09.6c | device voltage if matched | 2.5 | V |
| 06-09.7a | matched load | 33.49 | Ω |
| 06-09.7b | maximum power per V² | 6.973 | mW |
| 06-09.8a | voltage, 100 Ω | 2 | V |
| 06-09.8b | power, 100 Ω | 40 | mW |
| 06-09.8c | voltage, 60 Ω | 6 | V |
| 06-09.8d | power, 60 Ω | 600 | mW |
| 06-09.9a | maximum power, 20 K | 40 | mW |
| 06-09.9b | maximum power, 10 K | 10 | mW |
| 06-09.9c | fixed 0.4 V, 10 K | 0 | mW |
| 06-09.10a | minimum-loss Z_0, PTFE | 52.93 | Ω |
| 06-09.10b | maximum-power Z_0, PTFE | 20.70 | Ω |
| 06-09.10c | b/a at 50 Ω, PTFE | 3.345 | — |
| 06-09.10d | loss relative to minimum | 1.002 | — |
| 06-09.10e | power capacity relative to maximum | 0.587 | — |
| 06-09.11a | fraction of the voltage (and, for a physical R_out, of the power) at the speaker | 99.38 | % |
| 06-09.11b | damping factor | 160 | — |
| 06-09.12a | equivalent voltage | 8.571 | V |
| 06-09.12b | equivalent resistance | 1.714 | Ω |
| 06-09.12c | maximum power | 10.71 | W |
| 06-09.12d | load voltage at the match | 4.286 | V |
| 06-09.12e | 12 V source current | 1.929 | A |
| 06-09.12f | 6 V source current | 0.5714 | A |
