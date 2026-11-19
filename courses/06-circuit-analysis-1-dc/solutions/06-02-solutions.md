# Solutions 06-02 · Circuit Elements and Ohm's Law

Problems: [06-02 problems](../problems/06-02-problems.md) · Chapter: [06-02](../chapters/06-02-circuit-elements-and-ohms-law.md). Every number below is recomputed by [verify_06_02.py](../verify/verify_06_02.py); the circuit results of Problems 06-02.7 and 06-02.12 are also confirmed in ngspice ([lab netlists](../labs/06-02-lab/README.md)).

---

## Solutions

### Solution 06-02.1

(a) $i = v/R = 3.3/2200 = $ **1.5 mA**; $p = v^2/R = 3.3^2/2200 = $ **4.95 mW**.

(b) $v = i/G = 0.050/0.010 = $ **5 V**; $p = i^2/G = 0.050^2/0.010 = $ **0.25 W** (check: $vi = 5\times0.05$ ✓).

### Solution 06-02.2

(a) Any current at zero voltage: a **short circuit**. (b) Zero current at any voltage: an **open circuit**. (c) $i = (2\ \text{mA/V})\,v$ is a resistor with $G$ = 2 mS, $R = 1/G = $ **500 Ω**. (d) Fixed voltage at any current: an **ideal 3.3 V voltage source**. (e) A **practical source**: open-circuit voltage $V_{oc}$ = **8 V** (where $i = 0$), short-circuit current $I_{sc}$ = **4 mA** (where $v = 0$), internal resistance $R_{int} = V_{oc}/I_{sc} = 8/0.004 = $ **2 kΩ**. Equivalently an 8 V source in series with 2 kΩ, or a 4 mA source in parallel with 2 kΩ.

### Solution 06-02.3

(a) **Allowed**: KVL is satisfied (5 − 5 = 0), but the split of current between the two sources is undetermined. (b) **Not allowed**: KVL around the loop of the two sources gives 5 − 3.3 = 0, a contradiction. (c) **Allowed**: KCL at the joining node is satisfied, but the split of voltage between the sources is undetermined. (d) **Not allowed**: 1 mA enters the joining node and 2 mA leave it, violating KCL. (e) **Not allowed**: the source's current has no path, so KCL fails at its terminals. (f) **Not allowed**: the wire forces $v = 0$ while the source demands 9 V. (g) **Allowed**: the loop current is fixed at 1 mA by the current source, the resistor drops 1 V, and the current source takes up whatever voltage KVL leaves (8 V or 10 V, depending on the orientations).

### Solution 06-02.4

(a) E12: $10^{1/12} = $ **1.212** (about 21% per step). E96: $10^{1/96} = $ **1.024** (about 2.4%).

(b) The E12 neighbours of 4.1 are 3.9 and 4.7: $4.1/3.9 = 1.051$, $4.7/4.1 = 1.146$. **3.9 kΩ** is closer.

(c) $4.1/4.02 = 1.020$ and $4.12/4.1 = 1.005$: **4.12 kΩ**.

(d) The E24 step is $10^{1/24} = 1.101$, about 10%. Each value's ±5% band reaches halfway to its neighbours, so the bands of adjacent values just about touch and every resistance in the decade lies within the tolerance of some E24 value. A tighter tolerance with E24 would leave gaps of unreachable values; a looser one would make neighbouring values overlap, wasting part numbers.

### Solution 06-02.5

(a) The round trip is 40 m of conductor: $R = \rho L/A = 1.7241\times10^{-8}\times40/2.08\times10^{-6} = $ **0.3316 Ω**.

(b) Drop $= 10\times0.3316 = $ **3.316 V** (about 3% of a 120 V outlet, 1.4% of 230 V); loss $= 10^2\times0.3316 = $ **33.16 W**, spread along 40 m of wire.

(c) At 100 A the loss would be $100^2\times0.3316 = $ **3316 W**: 100 times as much, since loss scales as $I^2$. That heat cannot escape a thin cord fast enough, and the insulation would melt; cords and wires are rated for the current at which their temperature rise stays acceptable, and fuses or breakers enforce it.

### Solution 06-02.6

$R = R_{20}[1 + \alpha(T - 20)]$, so $T = 20 + (R/R_{20} - 1)/\alpha = 20 + (2.400/2.000 - 1)/0.00393 = 20 + 0.200/0.00393 = $ **70.9 °C**. Motor and transformer standards use exactly this "resistance method" to measure average winding temperature, because the winding's inside is otherwise inaccessible.

### Solution 06-02.7

(a) The terminal line is $v = V_{oc} - R_{int}i$. From the two points: $R_{int} = (11.6 - 11.0)/(5.0 - 2.0) = $ **0.20 Ω**, and $V_{oc} = 11.6 + 2.0\times0.20 = $ **12.0 V**.

(b) $I_{sc} = 12.0/0.20 = $ **60 A**; the Norton form is a 60 A current source in parallel with 0.20 Ω.

(c) $v = 12.0 - 8.0\times0.20 = $ **10.4 V**.

### Solution 06-02.8

(a) The power $v^2/R$ is largest at the highest voltage and the lowest resistance: $13.2^2/950 = $ **0.1834 W**; smallest at the lowest voltage and the highest resistance: $10.8^2/1050 = $ **0.1111 W**.

(b) At half-rating the part must be rated at least $2\times0.1834 = 0.367$ W: **1/2 W**. A 1/4 W part would run at 73% of its rating in the worst case.

### Solution 06-02.9

(a) Over 100 K: thick film $10.00\times(1 + 100\times10^{-6}\times100) = $ **10.10 kΩ** (+1%); thin film $10.00\times(1 + 25\times10^{-6}\times100) = $ **10.025 kΩ** (+0.25%).

(b) Both change by the same factor, so their **ratio is unchanged** and the divider's output stays put. This is why precision dividers use matched resistor networks (same material, same substrate, tracking TCR) rather than two independent parts.

(c) $R_1/R_2 = (1 + 0.01)/(1 - 0.01) = 1.0202$: a ratio change of **2.02%**, twice the drift of either resistor. A ±100 ppm/K specification bounds each part's drift, not how two parts track each other.

### Solution 06-02.10

(a) $R = R_\square L/W$: $L/W = 10\,000/200 = 50$ squares, so $L = 50\times1.00 = $ **50 µm**.

(b) With $L$ fixed at 50 µm: $W$ = 0.95 µm gives $200\times50/0.95 = $ **10.53 kΩ**; $W$ = 1.05 µm gives $200\times50/1.05 = $ **9.524 kΩ**: about ±5%.

(c) The width error is a fixed amount (±0.05 µm here) set by lithography and etching, so its *relative* effect is smaller on a wider resistor: at 10 µm width the same error is ±0.5%. Wider resistors also average out local variations, so matched pairs track better. The price is area.

### Solution 06-02.11

(a) $R_{\max} = 100\ \text{mV}/20\ \text{A} = $ **5 mΩ**.

(b) $P = I^2R = 20^2\times0.005 = $ **2 W**: a substantial heat source on a board, which itself warms the shunt.

(c) Tolerance 1% plus TCR over a 60 °C rise, $35\times10^{-6}\times60 = 0.21\%$: worst case **1.21%**.

(d) Signal $20\times0.5\ \text{mΩ} = $ **10 mV**; power $20^2\times0.0005 = $ **0.2 W**; worst-case error $1\% + 350\times10^{-6}\times60 = 1\% + 2.1\% = $ **3.1%**. The 0.5 mΩ part wastes a tenth of the power but gives a tenth of the signal (so amplifier offset and noise matter ten times more) and drifts ten times more with temperature, plausibly because its copper terminations are a larger share of its resistance. The 5 mΩ part is the better measurement; the 0.5 mΩ part is the better choice only when the 2 W or the 100 mV drop is unacceptable, and then calibration over temperature or a better amplifier must recover the accuracy.

### Solution 06-02.12

(a) KCL at the common + terminal, with each cell's current out of its + terminal $(V_k - v)/R$:

$$
2\cdot\frac{4.0 - v}{0.06} + \frac{3.7 - v}{0.06} = 0 \;\Rightarrow\; 8.0 + 3.7 = 3v \;\Rightarrow\; v = \textbf{3.90 V}.
$$

(b) Each 4.0 V cell delivers $(4.0 - 3.9)/0.06 = $ **1.667 A**; the 3.7 V cell's current out of its + terminal is $(3.7 - 3.9)/0.06 = -3.333$ A: **3.333 A flows into it**.

(c) Heat: $2\times1.667^2\times0.06 + 3.333^2\times0.06 = 0.333 + 0.667 = $ **1.00 W**. The strong cells deliver $2\times4.0\times1.667 = 13.33$ W; the weak cell absorbs $3.7\times3.333 = 12.33$ W; $13.33 = 12.33 + 1.00$ ✓.

### Solution 06-02.13

(a) Inverting the diode law, $v = V_T\ln(i/I_s + 1)$, and $dv/di = V_T/(i + I_s)$:

| Current | $v$ | Static $v/i$ | Incremental $dv/di$ |
|---|---|---|---|
| 1 mA | **0.6548 V** | **654.8 Ω** | **25.85 Ω** |
| 10 mA | **0.7143 V** | **71.43 Ω** | **2.585 Ω** |

(b) $\Delta i \approx \Delta v/(dv/di) = 1\ \text{mV}/25.85\ \Omega = $ **38.7 µA**.

(c) The **incremental** resistance: it is the slope of the curve at the operating point, which is what governs small changes about that point. The static resistance relates the total voltage to the total current and would predict $1\ \text{mV}/654.8\ \Omega = 1.5$ µA, 25 times too small. Every small-signal model in electronics rests on this distinction.

### Solution 06-02.14

(a) Two-wire: the meter's test current flows through both leads and the resistor, and it measures the total voltage: $0.050 + 0.100 + 0.050 = $ **0.200 Ω**, an error of **+100%**.

(b) Four-wire: the voltage-sensing leads carry essentially no current, so they drop no voltage, and the meter sees only the voltage across the resistor itself: **0.100 Ω**. (06-11 develops Kelvin sensing.)

(c) $0.100/10\,000 = 10^{-5}$: **0.001%**, negligible. Lead resistance matters only for low-value resistors.

### Solution 06-02.15

(a) $I_{sc} = 12/0.1 = $ **120 A**, and all $12^2/0.1 = $ **1440 W** is dissipated inside the supply: an unprotected supply would be destroyed.

(b) **12 V**, and **0 W** (no current).

(c) In current limit the supply becomes, in effect, a 5 A current source: a short forces **0 V** at the output with **5 A** flowing. A bench supply's front panel shows exactly this ("CC" mode). The linear $V_{oc}$–$R_{int}$ model holds only within the supply's regulated range.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 06-02.1a | current | 1.5 | mA |
| 06-02.1b | power | 4.95 | mW |
| 06-02.1c | voltage | 5 | V |
| 06-02.1d | power | 0.25 | W |
| 06-02.2a | resistance of (c) | 500 | Ω |
| 06-02.2b | open-circuit voltage of (e) | 8 | V |
| 06-02.2c | short-circuit current of (e) | 4 | mA |
| 06-02.2d | internal resistance of (e) | 2 | kΩ |
| 06-02.4a | E12 step | 1.212 | — |
| 06-02.4b | E96 step | 1.024 | — |
| 06-02.5a | round-trip resistance | 0.3316 | Ω |
| 06-02.5b | drop at 10 A | 3.316 | V |
| 06-02.5c | loss at 10 A | 33.16 | W |
| 06-02.5d | loss at 100 A | 3316 | W |
| 06-02.6a | winding temperature | 70.9 | °C |
| 06-02.7a | internal resistance | 0.20 | Ω |
| 06-02.7b | open-circuit voltage | 12.0 | V |
| 06-02.7c | short-circuit current | 60 | A |
| 06-02.7d | terminal voltage at 8 A | 10.4 | V |
| 06-02.8a | maximum power | 0.1834 | W |
| 06-02.8b | minimum power | 0.1111 | W |
| 06-02.9a | thick-film value at 125 °C | 10.10 | kΩ |
| 06-02.9b | thin-film value at 125 °C | 10.025 | kΩ |
| 06-02.9c | ratio change, opposite TCRs | 2.02 | % |
| 06-02.10a | length for 10 kΩ | 50 | µm |
| 06-02.10b | resistance at 0.95 µm | 10.53 | kΩ |
| 06-02.10c | resistance at 1.05 µm | 9.524 | kΩ |
| 06-02.11a | largest shunt | 5 | mΩ |
| 06-02.11b | power in 5 mΩ at 20 A | 2 | W |
| 06-02.11c | worst-case error, 5 mΩ | 1.21 | % |
| 06-02.11d | signal of 0.5 mΩ at 20 A | 10 | mV |
| 06-02.11e | power in 0.5 mΩ at 20 A | 0.2 | W |
| 06-02.11f | worst-case error, 0.5 mΩ | 3.1 | % |
| 06-02.12a | terminal voltage | 3.90 | V |
| 06-02.12b | current from each 4.0 V cell | 1.667 | A |
| 06-02.12c | current into the 3.7 V cell | 3.333 | A |
| 06-02.12d | heat | 1.00 | W |
| 06-02.13a | diode voltage at 1 mA | 0.6548 | V |
| 06-02.13b | static resistance at 1 mA | 654.8 | Ω |
| 06-02.13c | incremental resistance at 1 mA | 25.85 | Ω |
| 06-02.13d | diode voltage at 10 mA | 0.7143 | V |
| 06-02.13e | static resistance at 10 mA | 71.43 | Ω |
| 06-02.13f | incremental resistance at 10 mA | 2.585 | Ω |
| 06-02.13g | current change for 1 mV | 38.7 | µA |
| 06-02.14a | two-wire reading | 0.200 | Ω |
| 06-02.14b | four-wire reading | 0.100 | Ω |
| 06-02.15a | short-circuit current | 120 | A |
| 06-02.15b | internal dissipation when shorted | 1440 | W |
