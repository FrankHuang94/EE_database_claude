# Solutions 06-01 · Charge, Current, Voltage, Power and the Lumped Circuit Abstraction

Problems: [06-01 problems](../problems/06-01-problems.md) · Chapter: [06-01](../chapters/06-01-charge-current-voltage-power.md). Every number below is recomputed by [verify_06_01.py](../verify/verify_06_01.py); the circuit results of Problems 06-01.6 and 06-01.13 are also confirmed in ngspice ([lab netlist](../labs/06-01-lab/power_balance.cir)).

---

## Solutions

### Solution 06-01.1

(a) Charge: $4000\ \text{mAh} = 4.000\ \text{A}\times 3600\ \text{s} = $ **14 400 C**. Energy: $4.000\ \text{Ah}\times 3.7\ \text{V} = $ **14.8 Wh**, and $14.8\ \text{Wh}\times 3600\ \text{J/Wh} = 53\,280$ J $=$ **53.28 kJ**.

(b) $q = I t = 50\times10^{-6}\ \text{A}\times(365\times 86\,400\ \text{s}) = $ **1577 C** (1576.8 C). In mAh: $1576.8\ \text{C}/3.6\ \text{C/mAh} = $ **438 mAh**, more than the whole capacity of a coin cell. Leakage matters.

(c) $1\ \text{kWh} = 1000\ \text{W}\times 3600\ \text{s} = $ **3.6×10⁶ J**; a 10 W lamp runs $1000/10 = $ **100 h**.

**Units check.** A × s = C; Ah × V = Wh; W × s = J ✓.

### Solution 06-01.2

(a) $i = dq/dt$. With $\tau$ = 2 ms, $\dfrac{d}{dt}\left[5(1 - e^{-t/\tau})\right] = \dfrac{5}{\tau}e^{-t/\tau}$, and $5\ \mu\text{C}/2\ \text{ms} = 2.5$ mA, so $i(t) = $ **2.5 e^{−t/2 ms} mA** for $t \ge 0$.

(b) $i(0) = $ **2.5 mA**; $i(2\ \text{ms}) = 2.5/e = $ **0.920 mA**.

(c) As $t\to\infty$, $q \to$ **5 µC**. Check by integration: $\int_0^\infty 2.5\ \text{mA}\,e^{-t/\tau}dt = 2.5\ \text{mA}\times\tau = 5\ \mu\text{C}$ ✓.

### Solution 06-01.3

The passive convention needs the current *entering* the + terminal; $p = vi$ with that current is the absorbed power.

(a) $p = 10\times 2 = $ **20 W**, absorbed.

(b) The current entering + is −2 A: $p = 10\times(-2) = $ **−20 W**: the element **delivers** 20 W.

(c) $p = (-5)(-3) = $ **15 W**, absorbed. (Both signs reversed: the actual voltage and current are both opposite to their references, which leaves the product unchanged.)

(d) A current of −4 A out of terminal A is +4 A into it, and A is the + terminal: $p = 3\times 4 = $ **12 W**, absorbed.

### Solution 06-01.4

(a) From 04-05, $I = n e A v_d$, so $v_d = I/(neA) = 1.0/(8.491\times10^{28}\times1.602\,176\,634\times10^{-19}\times1.0\times10^{-6}) = $ **7.35×10⁻⁵ m/s**, about 0.07 mm/s.

(b) $t = 1\ \text{m}/7.35\times10^{-5}\ \text{m/s} = 1.36\times10^4$ s $=$ **3.78 h**.

(c) $t = 1\ \text{m}/(\tfrac23\times 299\,792\,458\ \text{m/s}) = $ **5.00 ns**.

(d) The wire is already full of mobile electrons. Closing the switch launches an electromagnetic wave along the wires that sets *all* of them drifting almost at once, so current flows in the lamp within nanoseconds, although each electron moves only a fraction of a millimeter per second.

**Units check.** A/(m⁻³ · C · m²) = (C/s)/(C/m) = m/s ✓.

### Solution 06-01.5

(a) Convert each current to "entering the + terminal", then $p = vi$:

| Element | Current entering + | Absorbed power |
|---|---|---|
| A | −3 A | $12\times(-3) = $ **−36 W** |
| B | 3 A | **12 W** |
| C | 1 A | **8 W** |
| D | +1.5 A (−1.5 A out = 1.5 A in) | $8\times1.5 = $ **12 W** |

(b) Tellegen: the absorbed powers sum to zero, so $p_E = -(-36 + 12 + 8 + 12) = $ **4 W** (absorbed).

(c) $i_E = p_E/v_E = 4/2 = $ **2 A**, into its + terminal.

(d) Only **A** delivers energy (36 W); B, C, D and E absorb $12 + 8 + 12 + 4 = 36$ W ✓.

### Solution 06-01.6

(a) With reference currents into node A through each series resistor and out of it through the load:

$$
\frac{9 - v_A}{1} + \frac{12 - v_A}{2} = \frac{v_A}{4} \;\Rightarrow\; 4(9 - v_A) + 2(12 - v_A) = v_A \;\Rightarrow\; 60 = 7v_A ,
$$

so $v_A = 60/7 = $ **8.571 V**, $i_1 = 9 - 8.571 = $ **0.4286 A**, $i_2 = (12 - 8.571)/2 = $ **1.714 A** and $i_3 = 8.571/4 = $ **2.143 A** ($i_1 + i_2 = i_3$ ✓).

(b) Absorbed powers: 9 V source $9\times(-0.4286) = $ **−3.857 W**; 12 V source $12\times(-1.714) = $ **−20.571 W**; 1 Ω: $0.4286^2\times1 = $ **0.1837 W**; 2 Ω: $1.714^2\times2 = $ **5.878 W**; 4 Ω: $2.143^2\times4 = $ **18.367 W**. Sum: $-3.857 - 20.571 + 0.184 + 5.878 + 18.367 = 0$ ✓. Both sources deliver this time.

(c) The 9 V source carries no current when $v_A = 9$ V. Then the load takes $9/4 = 2.25$ A, all of which must come through the 2 Ω resistor: $(V_2 - 9)/2 = 2.25$, so $V_2 = $ **13.5 V**.

(d) For $V_2 > 13.5$ V, $v_A$ exceeds 9 V, $i_1$ becomes negative, and current flows *into* the 9 V source's + terminal: it absorbs power. If it is a rechargeable battery, it is being charged; if it is a primary cell or a power supply that cannot sink current, this is a fault condition, which is why real designs add diodes or "ideal-diode" controllers to stop back-feeding.

### Solution 06-01.7

(a) Energy is the area under $p(t)$: $2.0\ \text{W}\times0.10\ \text{s} + \tfrac12\times2.0\ \text{W}\times0.20\ \text{s} = 0.20 + 0.20 = $ **0.40 J** per flash.

(b) $P_{\text{avg}} = 0.40\ \text{J}/2.0\ \text{s} = $ **0.20 W**.

(c) Per day: $0.20\ \text{W}\times86\,400\ \text{s} = $ **17 280 J** $= 17\,280/3600 = $ **4.8 Wh**.

### Solution 06-01.8

The period is $T$ = 1 ms; the average voltage is $\overline v = 2.5$ V in every case.

(a) $p = 10$ W for half the period and 0 for the other half: $\overline{p} = $ **5 W**. $\overline i = 1$ A, so $\overline v\,\overline i = $ **2.5 W**.

(b) The current flows only when the voltage is zero: $p = 0$ always, $\overline p = $ **0 W**; but $\overline v\,\overline i = $ **2.5 W** again.

(c) $p = 5$ W for half the period: $\overline p = $ **2.5 W** $= \overline v\,\overline i$.

The average of a product depends on *when* the two factors are large together. Only when one factor is constant (case c, or DC) does $\overline{vi} = \overline v\,\overline i$. In AC circuits the timing is the phase between voltage and current, and this is the origin of the power factor (07-06).

### Solution 06-01.9

(a) $I_{\text{avg}} = 5\ \mu\text{A} + 10\ \text{mA}\times\dfrac{0.050}{60} + 40\ \text{mA}\times\dfrac{1.0}{900} = 5 + 8.333 + 44.44 = $ **57.78 µA**.

(b) Life $= 2500\ \text{mAh}/0.05778\ \text{mA} = $ **43 269 h** $= 43\,269/8766 = $ **4.94 years**.

(c) Radio share $= 44.44/57.78 = $ **76.9%**.

(d) Transmitting hourly: $40\times1/3600 = 11.11$ µA, so $I_{\text{avg}} = 5 + 8.333 + 11.11 = 24.44$ µA and the life is $2500/0.02444 = 102\,273$ h $=$ **11.7 years**.

(e) Any of: alkaline cells self-discharge over years, so their shelf life rather than the load may end the battery; capacity falls at low temperature and at high pulse currents (the 40 mA bursts); the node may stop working above the cells' end-of-life voltage, before the rated capacity is used. A design life beyond about 5 to 10 years on alkaline cells is not credible whatever the arithmetic says.

### Solution 06-01.10

(a) $t_d < t_r/6 = 1000\ \text{ps}/6 = 166.7$ ps, so $\ell < 166.7/7.154 = $ **23.3 mm**.

(b) $\ell < 16.67/7.154 = $ **2.33 mm**: at 100 ps edges almost every board trace is a transmission line.

(c) Delay $= \sqrt{3.0}/c = 5.777\times10^{-9}$ s/m $=$ **5.78 ps/mm**. Longest lumped wire: $(20/6)\ \text{ps}/5.778\ \text{ps/mm} = $ **0.577 mm**.

(d) On-chip wires are thin and resistive, so their delay is dominated by distributed RC charging, which grows as the square of length (04-05), long before the speed-of-light delay matters. Long on-chip wires are broken up with repeaters for that reason.

### Solution 06-01.11

The loss is $I^2R$ and the drop $IR$, with $I = P/V$.

(a) $I = 100/20 = 5$ A: loss $5^2\times0.20 = $ **5.0 W**; drop $5\times0.20 = 1.0$ V, $1.0/20 = $ **5.0%**.

(b) $I = 240/48 = 5$ A: loss **5.0 W**; drop 1.0 V, $1.0/48 = $ **2.08%**.

(c) $I = 240/20 = 12$ A: loss $12^2\times0.20 = $ **28.8 W**; drop 2.4 V, **12%**.

(d) The current, and hence the cable's loss and heating, is the same in (a) and (b), yet (b) delivers 2.4 times the power with a smaller fractional drop. Raising the current instead (c) would multiply the loss by $(12/5)^2 = 5.76$ and require thicker conductors and connectors rated for 12 A. Keeping the cable's 5 A limit and raising the voltage is the cheap direction, at the price of insulation and protection suited to 48 V.

### Solution 06-01.12

(a) $I = P/V$: at 54 V, $120\,000/54 = $ **2222 A**; at 800 V, $120\,000/800 = $ **150 A**.

(b) $I^2R$ with 50 µΩ: at 54 V, $2222^2\times50\times10^{-6} = $ **246.9 W**; at 800 V, $150^2\times50\times10^{-6} = $ **1.125 W**.

(c) Equal loss means $P^2R/V^2$ is the same, so $R$ may grow as $V^2$; resistance is inversely proportional to cross-section (06-02), so the area shrinks by $(800/54)^2 = $ **219.5**. Two hundred times less copper for the same loss: this is the economic argument for high-voltage DC distribution in AI data centers.

(d) Any two: 800 V needs much larger insulation and creepage distances and arc-safe connectors; it falls under stricter electrical-safety rules for service personnel; it adds a high-ratio conversion stage (800 V down to the board's 48 V or 12 V) with its own efficiency and cost; the protection and fault-handling equipment for high-voltage DC is less mature than for AC.

### Solution 06-01.13

(a) KCL at node A in circuit 2: $\dfrac{6 - v'}{1} + \dfrac{0 - v'}{1} = \dfrac{v'}{1}$, so $3v' = 6$ and $v' = $ **2 V**; $i_1' = 6 - 2 = $ **4 A**, $i_2' = 0 - 2 = $ **−2 A**, $i_3' = $ **2 A**.

(b) Circuit 1's branch voltages (+ to −) are $V_1$: 12 V, $R_1$: 4 V, $V_2$: 6 V, $R_2$: −2 V, $R_3$: 8 V (Example 06-01.2). Circuit 2's currents entering each + terminal are $V_1$: $-i_1' = -4$ A, $R_1$: $i_1' = 4$ A, $V_2$: $-i_2' = 2$ A, $R_2$: $i_2' = -2$ A, $R_3$: $i_3' = 2$ A. So

$$
\sum_k v_k i'_k = 12(-4) + 4(4) + 6(2) + (-2)(-2) + 8(2) = -48 + 16 + 12 + 4 + 16 = \mathbf{0}.
$$

(c) The proof of §3.5 used only two facts: circuit 1's voltages are differences of node voltages (KVL), and circuit 2's currents sum to zero at each node (KCL). Both hold here because the two circuits share a graph, so the sum vanishes, even though $v_k i'_k$ is the voltage of one circuit times the current of another and is not a power. This form of the theorem is the basis of reciprocity and of adjoint sensitivity analysis.

### Solution 06-01.14

(a) The field along the wire is $E = V/L = 10/0.50 = $ **20 V/m**. By Ampère's law (04-06), $H$ at radius $a$ around a straight current is $I/(2\pi a) = 2.0/(2\pi\times0.25\times10^{-3}) = $ **1273 A/m**.

(b) $\vec E$ points along the wire (in the direction of the current) and $\vec H$ circles it, so $\vec S = \vec E\times\vec H$ points **radially inward**, into the wire, with magnitude $EH = 20\times1273 = $ **2.546×10⁴ W/m²**.

(c) Surface area $2\pi a L = 2\pi\times0.25\times10^{-3}\times0.50 = 7.854\times10^{-4}$ m², so the inflow is $2.546\times10^4\times7.854\times10^{-4} = $ **20.0 W** $= VI = 10\times2.0$ ✓. Symbolically, $(V/L)\,(I/2\pi a)\,(2\pi a L) = VI$ for any wire.

(d) The energy that heats a resistor arrives through the space around it, carried by the fields, and enters through its surface; the conduction electrons only set up the fields. Circuit theory's $p = vi$ gives the right total while saying nothing about the path.

### Solution 06-01.15

(a) SPICE reports a voltage source's current as positive when it flows *into* its + terminal (the passive convention). So 1.5 A flows into the battery's + terminal: it **absorbs** $3.7\times1.5 = $ **5.55 W** and is **charging**.

(b) A negative absorbed power means the battery **delivers 2.0 W**: it is discharging. The current is $i = p/v = -2.0/3.7 = $ **−0.541 A**, that is 0.541 A flowing out of its + terminal.

(c) Because SPICE treats every element, sources included, with the passive convention, the current of a source that is delivering power flows out of its + terminal and is reported negative. The sign tells you the direction of energy flow, not that anything is wrong.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 06-01.1a | charge in 4000 mAh | 14400 | C |
| 06-01.1b | energy at 3.7 V | 14.8 | Wh |
| 06-01.1c | energy at 3.7 V | 53.28 | kJ |
| 06-01.1d | charge of 50 µA for a year | 1577 | C |
| 06-01.1e | the same in mAh | 438 | mAh |
| 06-01.1f | joules in 1 kWh | 3.6×10^6 | J |
| 06-01.1g | run time of a 10 W lamp | 100 | h |
| 06-01.2a | i(0) | 2.5 | mA |
| 06-01.2b | i(2 ms) | 0.920 | mA |
| 06-01.2c | total charge | 5 | µC |
| 06-01.3a | absorbed power, case (a) | 20 | W |
| 06-01.3b | absorbed power, case (b) | −20 | W |
| 06-01.3c | absorbed power, case (c) | 15 | W |
| 06-01.3d | absorbed power, case (d) | 12 | W |
| 06-01.4a | drift speed | 7.35×10^-5 | m/s |
| 06-01.4b | time to drift 1 m | 3.78 | h |
| 06-01.4c | signal time over 1 m | 5.00 | ns |
| 06-01.5a | power absorbed by A | −36 | W |
| 06-01.5b | power absorbed by D | 12 | W |
| 06-01.5c | power absorbed by E | 4 | W |
| 06-01.5d | current of E | 2 | A |
| 06-01.6a | node voltage | 8.571 | V |
| 06-01.6b | i_1 | 0.4286 | A |
| 06-01.6c | i_2 | 1.714 | A |
| 06-01.6d | i_3 | 2.143 | A |
| 06-01.6e | power absorbed by the 9 V source | −3.857 | W |
| 06-01.6f | power absorbed by the 12 V source | −20.571 | W |
| 06-01.6g | power absorbed by the 1 Ω resistor | 0.1837 | W |
| 06-01.6h | power absorbed by the 2 Ω resistor | 5.878 | W |
| 06-01.6i | power absorbed by the 4 Ω resistor | 18.367 | W |
| 06-01.6j | second source voltage for zero current in the first | 13.5 | V |
| 06-01.7a | energy per flash | 0.40 | J |
| 06-01.7b | average power | 0.20 | W |
| 06-01.7c | energy per day | 17280 | J |
| 06-01.7d | energy per day | 4.8 | Wh |
| 06-01.8a | average power, case (a) | 5 | W |
| 06-01.8b | average power, case (b) | 0 | W |
| 06-01.8c | average power, case (c) | 2.5 | W |
| 06-01.8d | product of averages | 2.5 | W |
| 06-01.9a | average current | 57.78 | µA |
| 06-01.9b | battery life | 43269 | h |
| 06-01.9c | battery life | 4.94 | years |
| 06-01.9d | radio share | 76.9 | % |
| 06-01.9e | life with hourly transmission | 11.7 | years |
| 06-01.10a | longest lumped trace, 1 ns edges | 23.3 | mm |
| 06-01.10b | longest lumped trace, 100 ps edges | 2.33 | mm |
| 06-01.10c | on-chip delay per mm | 5.78 | ps/mm |
| 06-01.10d | longest lumped on-chip wire, 20 ps edges | 0.577 | mm |
| 06-01.11a | cable loss at 100 W, 20 V | 5.0 | W |
| 06-01.11b | drop fraction at 100 W, 20 V | 5.0 | % |
| 06-01.11c | drop fraction at 240 W, 48 V | 2.08 | % |
| 06-01.11d | cable loss at 240 W, 20 V | 28.8 | W |
| 06-01.11e | drop fraction at 240 W, 20 V | 12 | % |
| 06-01.12a | current at 54 V | 2222 | A |
| 06-01.12b | current at 800 V | 150 | A |
| 06-01.12c | busbar loss at 54 V | 246.9 | W |
| 06-01.12d | busbar loss at 800 V | 1.125 | W |
| 06-01.12e | copper area ratio | 219.5 | — |
| 06-01.13a | node voltage of circuit 2 | 2 | V |
| 06-01.13b | i_1' | 4 | A |
| 06-01.13c | i_2' | −2 | A |
| 06-01.13d | sum of v_k i'_k | 0 | V·A |
| 06-01.14a | axial field at the surface | 20 | V/m |
| 06-01.14b | H at the surface | 1273 | A/m |
| 06-01.14c | Poynting magnitude | 2.546×10^4 | W/m² |
| 06-01.14d | power through the surface | 20.0 | W |
| 06-01.15a | power absorbed while charging | 5.55 | W |
| 06-01.15b | current while delivering 2 W | −0.541 | A |
