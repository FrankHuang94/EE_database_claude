# Solutions 10-01 · Diodes and Diode Circuits

Problems: [10-01 problems](../problems/10-01-problems.md) · Chapter: [10-01](../chapters/10-01-diodes-and-diode-circuits.md). Every number below is recomputed by [verify_10_01.py](../verify/verify_10_01.py):

- diode circuits by root finding on the exponential, with the Lambert W closed form as a cross-check;
- rectifiers by integrating the circuit's differential equation until it is periodic;
- Zener regulators by solving the nodal equation at each corner.

---

## Solutions

### Solution 10-01.1

(a) Constant drop: $(3 - 0.7)/1\text{ kΩ}$ = **2.300** mA. Exactly: $V_D$ = **0.6766** V and $I_D$ = **2.323** mA. Error **−1.0**%.

(b) Constant drop: **0.300** mA. Exactly: $V_D$ = **0.6291** V and $I_D$ = **0.3709** mA. Error **−19.1**%.

The constant-drop model is good when the supply is several times the diode drop; at 1 V the 70 mV error in $V_D$ is a large fraction of the 0.3–0.4 V across the resistor. Note also that this diode, with a larger $I_S$, drops less than 0.7 V even at 2 mA: "0.7 V" is a convention.

### Solution 10-01.2

(a) D_A conducts: $V_O$ = 3.3 − 0.7 = **2.6** V. D_B has its anode at 0 V and cathode at 2.6 V: reverse-biased by **2.6** V (key: −2.6 V forward voltage).

(b) $V_O$ is still 2.6 V (assume D_A on). D_B sees 3.0 − 2.6 = **0.4** V forward, below 0.7 V, so it is off in the model. With exponential diodes sharing a cathode, D_B carries $e^{-0.3/V_T}$ = **9.12 × 10⁻⁶** of D_A's current.

(c) The output is high if either input is high: an OR gate (with a 0.7 V loss per level, which is why diode logic could not be cascaded without amplifiers).

### Solution 10-01.3

$r_d = nV_T/I_D$: **51.70** Ω for $n$ = 1 and **103.4** Ω for $n$ = 2. A 1 mV peak gives **19.34** µA and **9.670** µA. (Both are well within the small-signal limit, about 5 mV for $n$ = 1 and 10 mV for $n$ = 2.)

### Solution 10-01.4

(a) 85 °C is 60 K above 25 °C: $0.650 - 0.120$ = **0.530** V. −40 °C is 65 K below: $0.650 + 0.130$ = **0.780** V.

(b) $V_T\ln10$ at 358.15 K = **71.06** mV per decade.

(c) At 85 °C, 1 mA needs only 0.530 V, so 0.650 V is 120 mV more, worth $10^{120/71.06}$ = **48.8** times the current. A junction held at a fixed voltage carries a current that roughly doubles every 10 to 11 K over this range (every 9 K near room temperature, where the rate is highest); if that current heats it, the loop can run away. Bias junctions with a current, or with a resistor that limits the current, not with a stiff voltage.

### Solution 10-01.5

(a) $V_p$ = 10 − 0.7 = **9.3** V; $C \ge I_L/(fV_r)$ = 0.1/(60 × 1) = **1667** µF.

(b) $V_r$ = 0.1/(60 × 2200 × 10⁻⁶) = **0.758** V, so the output dips to **8.54** V. $\omega\Delta t = \sqrt{2V_r/V_p}$ = **23.13°**. $i_{D,\max} = I_L(1 + 2\pi\sqrt{2V_p/V_r})$ = **3.21** A.

(c) PIV ≈ $2V_s - V_{D0}$ = **19.3** V: the capacitor holds the cathode at 9.3 V while the anode swings to −10 V.

### Solution 10-01.6

(a) Full-wave: $C = I_L/(2fV_r)$ = 1/(120 × 0.5) = **16,667** µF (a large electrolytic, or a bank of them).

(b) Each half-winding must reach 12 + 0.8 = **12.8** V; the idle diode sees the whole winding minus the conducting diode's drop, 2 × 12.8 − 0.8 = **24.8** V.

(c) The winding must reach 12 + 1.6 = **13.6** V; each diode blocks 13.6 − 0.8 = **12.8** V.

(d) At 12 V the bridge is usual: half the PIV and no center tap, at the cost of a second diode drop (0.8 V of 13.6 V). At 2 V the center tap wins: a second 0.8 V drop would be a large fraction of the output, so a center-tapped winding with one drop (or synchronous rectifiers, §9) is preferred at low voltage.

### Solution 10-01.7

(a) $V_{Z0} = 12 - 0.021 \times 9$ = **11.81** V; at 5 mA, $V_Z$ = **11.86** V.

(b) $R \le (16 - 11.856)/(5 + 30)\text{ mA}$ = **118.4** Ω. Choose 110 Ω.

(c) Solving $(16 - V_O)/110 = 0.030 + (V_O - 11.811)/9$: $V_O$ = **11.88** V and $I_Z$ = **7.47** mA.

(d) At 20 V and no load: $I_Z = (20 - 11.811)/(110 + 9)$ = **68.8** mA, below $I_{ZM}$ = 76 mA (a modest 10% margin), and $P_Z$ = **0.855** W, below 1.3 W.

(e) Worst at 20 V and full load: **0.556** W. Use a 1 W resistor.

### Solution 10-01.8

(a) Line regulation $9/119$ = **75.6** mV/V; load regulation $-(110 \parallel 9)$ = **−8.32** mV/mA.

(b) **302.5** mV over the supply range (4 V × 75.6 mV/V) and **−249.6** mV over the load range (30 mA × 8.32 mV/mA).

### Solution 10-01.9

(a) The diode conducts when the output exceeds 2.0 + 0.7 = **2.7** V. A 1 V input passes unchanged (1 V); a 5 V input is clipped to 2.7 V.

(b) Solving $I_S(e^{(v_O - 2)/V_T} - 1) = (5 - v_O)/1\text{ kΩ}$: **2.735** V. The 2.3 mA through the diode needs 0.735 V, a little more than 0.7 V.

### Solution 10-01.10

(a) The capacitor charges to $3 - 0.7$ = 2.3 V, so the clamped output swings from **−0.7** V to **5.3** V, and the doubler captures $5.3 - 0.7$ = **4.6** V.

(b) With 0.3 V diodes: the clamp swings from −0.3 to 5.7 V and the doubler gives **5.4** V. In a doubler the losses are two diode drops; at 3 V input they cost 1.4 V of an ideal 6 V (23%) with PN diodes but 0.6 V (10%) with Schottky diodes. Multipliers for low-voltage energy harvesting therefore use Schottky diodes or MOSFETs.

### Solution 10-01.11

With $R$ = 1 kΩ, $I_S$ = 10⁻¹⁴ A and $V_{DD}$ = 1 V, the Lambert W formula gives **0.3709** mA, the same as iteration. The contraction factors are $V_T/RI_D$ = **0.0111** at 3 V and **0.0697** at 1 V: each step shrinks the error by 90 times at 3 V but only 14 times at 1 V, because less voltage falls across the resistor (smaller $RI_D$), so the diode's own logarithmic sensitivity matters more.

### Solution 10-01.12

With a constant-current load the capacitor discharges linearly. Conduction ends when the source falls faster than the load alone would discharge the capacitor, $C\omega V_s\sin\omega t = I_L$: **0.69°** after the peak. Finding the next crossing numerically: peak-to-peak ripple **0.711** V, conduction angle **22.43°**, peak diode current **3.17** A, average during conduction **1.61** A. §3.6 overstates the ripple by **6.5**%, because the capacitor really discharges for one period minus the 6% of it spent charging.

### Solution 10-01.13

(a) From 20/3 = **6.67** mΩ to 50/3 = **16.7** mΩ.

(b) MOSFET: $3^2 \times 0.010$ = **0.09** W. Schottky: **1.5** W. PN: **2.4** W.

(c) The drop is $6 \times 0.010$ = **60** mV and the loss **0.36** W. At 60 mV the MOSFET is fully on, so the controller is no longer regulating 20 mV: the drop is simply $IR_{DS(on)}$, which is why the guideline ties $R_{DS(on)}$ to the nominal current.

### Solution 10-01.14

(a) $\tau = 50 \times 12\text{ pF}$ = **0.6** ns, and $f_{3\text{dB}} = 1/(2\pi\tau)$ = **265** MHz.

(b) $2.2\tau$ = **1.32** ns.

(c) The bit period at 400 Mbps is 2.5 ns; the rise time takes **0.53** of it. That is about the limit for a clean eye, which is why the data sheet stops near 400 Mbps and why multi-gigabit lines need sub-picofarad protection.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 10-01.1a | constant-drop current at 3 V | 2.300 | mA |
| 10-01.1b | exact V_D at 3 V | 0.6766 | V |
| 10-01.1c | exact current at 3 V | 2.323 | mA |
| 10-01.1d | error at 3 V | -1.0 | % |
| 10-01.1e | constant-drop current at 1 V | 0.300 | mA |
| 10-01.1f | exact V_D at 1 V | 0.6291 | V |
| 10-01.1g | exact current at 1 V | 0.3709 | mA |
| 10-01.1h | error at 1 V | -19.1 | % |
| 10-01.2a | V_O, inputs 3.3 and 0 | 2.6 | V |
| 10-01.2b | D_B forward voltage, (a) | -2.6 | V |
| 10-01.2c | D_B forward voltage, (b) | 0.4 | V |
| 10-01.2d | current fraction | 9.12e-6 | — |
| 10-01.3a | r_d, n = 1 | 51.70 | Ω |
| 10-01.3b | r_d, n = 2 | 103.4 | Ω |
| 10-01.3c | signal current, n = 1 | 19.34 | µA |
| 10-01.3d | signal current, n = 2 | 9.670 | µA |
| 10-01.4a | drop at 85 °C | 0.530 | V |
| 10-01.4b | drop at −40 °C | 0.780 | V |
| 10-01.4c | mV per decade at 85 °C | 71.06 | mV |
| 10-01.4d | current factor at fixed 0.650 V | 48.8 | — |
| 10-01.5a | peak output | 9.3 | V |
| 10-01.5b | capacitance for 1 V | 1667 | µF |
| 10-01.5c | ripple with 2200 µF | 0.758 | V |
| 10-01.5d | minimum output | 8.54 | V |
| 10-01.5e | conduction angle | 23.13 | ° |
| 10-01.5f | peak diode current | 3.21 | A |
| 10-01.5g | PIV | 19.3 | V |
| 10-01.6a | capacitance | 16667 | µF |
| 10-01.6b | half-winding peak | 12.8 | V |
| 10-01.6c | center-tap PIV | 24.8 | V |
| 10-01.6d | bridge winding peak | 13.6 | V |
| 10-01.6e | bridge PIV | 12.8 | V |
| 10-01.7a | V_Z0 | 11.81 | V |
| 10-01.7b | V_Z at 5 mA | 11.86 | V |
| 10-01.7c | largest R | 118.4 | Ω |
| 10-01.7d | V_O at 16 V, 30 mA | 11.88 | V |
| 10-01.7e | I_Z at 16 V, 30 mA | 7.47 | mA |
| 10-01.7f | worst-case I_Z | 68.8 | mA |
| 10-01.7g | worst-case P_Z | 0.855 | W |
| 10-01.7h | worst-case resistor power | 0.556 | W |
| 10-01.8a | line regulation | 75.6 | mV/V |
| 10-01.8b | load regulation | -8.32 | mV/mA |
| 10-01.8c | change over supply range | 302.5 | mV |
| 10-01.8d | change over load range | -249.6 | mV |
| 10-01.9a | clipping level | 2.7 | V |
| 10-01.9b | exponential output at 5 V | 2.735 | V |
| 10-01.10a | clamp minimum | -0.7 | V |
| 10-01.10b | clamp maximum | 5.3 | V |
| 10-01.10c | doubler, 0.7 V diodes | 4.6 | V |
| 10-01.10d | doubler, 0.3 V diodes | 5.4 | V |
| 10-01.11a | Lambert W current | 0.3709 | mA |
| 10-01.11b | contraction factor at 3 V | 0.0111 | — |
| 10-01.11c | contraction factor at 1 V | 0.0697 | — |
| 10-01.12a | turn-off angle | 0.69 | ° |
| 10-01.12b | exact ripple | 0.711 | V |
| 10-01.12c | exact conduction angle | 22.43 | ° |
| 10-01.12d | exact peak diode current | 3.17 | A |
| 10-01.12e | exact average diode current | 1.61 | A |
| 10-01.12f | ripple overstatement | 6.5 | % |
| 10-01.13a | R_DS(on) lower bound | 6.67 | mΩ |
| 10-01.13b | R_DS(on) upper bound | 16.7 | mΩ |
| 10-01.13c | MOSFET loss at 3 A | 0.09 | W |
| 10-01.13d | Schottky loss | 1.5 | W |
| 10-01.13e | PN loss | 2.4 | W |
| 10-01.13f | MOSFET drop at 6 A | 60 | mV |
| 10-01.13g | MOSFET loss at 6 A | 0.36 | W |
| 10-01.14a | time constant | 0.6 | ns |
| 10-01.14b | 3 dB bandwidth | 265 | MHz |
| 10-01.14c | rise time | 1.32 | ns |
| 10-01.14d | rise time over bit period | 0.53 | — |
