# Solutions 06-11 · Practical DC Circuits and Measurement

Problems: [06-11 problems](../problems/06-11-problems.md) · Chapter: [06-11](../chapters/06-11-practical-dc-circuits-and-measurement.md). Every number below is recomputed by [verify_06_11.py](../verify/verify_06_11.py); the circuits of Problems 06-11.1, 06-11.2, 06-11.4, 06-11.8, 06-11.9 and 06-11.12 are also confirmed in ngspice ([lab netlist](../labs/06-11-lab/measure.cir)).

---

## Solutions

### Solution 06-11.1

The meter and the source's resistance form a divider: $V_m = 10\,R_{in}/(0.1\ \text{MΩ} + R_{in})$.

(a) $10\times10/10.1 = $ **9.901 V**, an error of $-0.1/10.1 = $ **−0.99%**.

(b) $10\times10{,}000/10{,}000.1 = $ **9.9999 V**, an error of **−10 ppm**.

### Solution 06-11.2

Without the meter $I_0 = 1.5/15 = 100$ mA. With it, $1.5/(15 + 2) = $ **88.24 mA**, an error of **−11.8%**. The burden voltage is $88.24\ \text{mA}\times2\ \Omega = $ **176.5 mV**. The circuit seen from the break is 15 Ω, so the corrected current is $88.24\times(1 + 2/15) = $ **100.0 mA**.

### Solution 06-11.3

$0.0005\times12.47 + 0.01 = 0.01624$ V: **±16.2 mV**, or **0.130%** of the reading.

### Solution 06-11.4

With input resistance $R_{in}$ the reading is $V_m = V_{th}R_{in}/(R_{th} + R_{in})$. Two readings (in volts, resistances in MΩ):

$$
4.5\,(R_{th} + 10) = 10\,V_{th},
\qquad
4.0\,(R_{th} + 5) = 5\,V_{th}.
$$

The second gives $V_{th} = 0.8\,(R_{th} + 5)$; substituting, $4.5R_{th} + 45 = 8R_{th} + 40$, so $R_{th} = 5/3.5 = $ **1.429 MΩ** and $V_{th} = 0.8\times6.429 = $ **5.143 V**. The meter alone read 12.5% low: a 10 MΩ meter on a megohm source.

### Solution 06-11.5

(a) $R = 50\ \text{mV}/5\ \text{A} = $ **10 mΩ**; $P = 5^2\times0.01 = $ **0.25 W**.

(b) $5\ \text{A}\times1\ \text{mΩ} = $ **5 mV** full scale; $P = 25\times0.001 = $ **25 mW**.

(c) $50\ \text{µV}/50\ \text{mV} = $ **0.1%** of full scale with 10 mΩ, and $50\ \text{µV}/5\ \text{mV} = $ **1%** with 1 mΩ. The tenfold saving in power costs tenfold in relative offset: the shunt tradeoff in one line.

### Solution 06-11.6

(a) $R_\square = \rho/t = 1.7241\times10^{-8}/35\times10^{-6} = $ **0.4926 mΩ/□**; squares $40/0.5 = $ **80**; $R = 80\times0.4926 = $ **39.41 mΩ**.

(b) Drop $2\times39.41 = $ **78.82 mV**; dissipation $2^2\times0.03941 = $ **157.6 mW**.

(c) $39.41\times(1 + 0.00393\times65) = $ **49.47 mΩ**, 26% higher.

### Solution 06-11.7

The motor current develops $3\ \text{A}\times20\ \text{mΩ} = $ **60 mV** across the shared trace, which adds to (or subtracts from) the sensor signal as seen by the ADC: **6%** of full scale. Cures: give the motor its own return path to the supply (a star ground), or measure the sensor differentially (Kelvin sensing of its output relative to its own ground, 06-05).

### Solution 06-11.8

(a) $10 + 100 = $ **110 mΩ**, **11** times the true value. (b) $1\ \text{A}\times10\ \text{mΩ} = $ **10 mV**, independent of the force leads; the sense leads carry essentially no current.

### Solution 06-11.9

(a) The ratio is $10/150 = 1/15$, so the ADC sees $48/15 = $ **3.2 V**.

(b) The divider's Thévenin resistance is $140\parallel10 = 9.333$ kΩ, so the 1 MΩ input loads it by $-9.333/(9.333 + 1000) = $ **−0.925%**. Including it, the bottom leg is $10\ \text{kΩ}\parallel1\ \text{MΩ} = 9.901$ kΩ and the ADC sees $48\times9.901/(140 + 9.901) = $ **3.170 V**. This is systematic: the firmware should use the loaded ratio.

(c) The ratio $R_2/(R_1 + R_2)$ is highest with $R_2$ high and $R_1$ low: $10.1/(138.6 + 10.1) = 0.067922$, **+1.88%**; lowest with $R_2$ low and $R_1$ high: $9.9/(141.4 + 9.9) = 0.065433$, **−1.85%**.

(d) Worst-case total: $1.01883\times1.005 - 1 = $ **+2.39%** and $0.98149\times0.995 - 1 = $ **−2.34%**.

(e) With 0.1% resistors the ratio errors are **±0.19%**, and the totals become **+0.69%** and **−0.69%**: the ADC now dominates.

### Solution 06-11.10

(a) $0.5\ \text{V}/10\ \text{A} = $ **50 mΩ**.

(b) 16 AWG has 13.17 mΩ/m (Example 06-11.6), and the pair has twice the one-way length: $0.05/(2\times0.01317) = $ **1.90 m**.

(c) $d_{14} = 0.127\times92^{22/39} = $ **1.628 mm**, so $A = 2.081$ mm² and $\rho/A = $ **8.285 mΩ/m**; the longest pair is $0.05/(2\times0.008285) = $ **3.02 m**.

### Solution 06-11.11

2 mΩ: $P = 15^2\times0.002 = $ **0.45 W**, a rise of $0.45\times50 = $ **22.5 °C**, and a worst-case change of $250\ \text{ppm/°C}\times22.5\ \text{°C} = $ **0.56%**.

5 mΩ: $P = 225\times0.005 = $ **1.125 W**, above the 1.0 W rating: **not usable** without a larger package.

3 mΩ: $P = 0.675$ W, a rise of **33.75 °C**, and a change of $75\times33.75\ \text{ppm} = $ **0.25%**. Its signal is **45 mV** against **30 mV** for the 2 mΩ part. The larger value runs hotter yet drifts less, because its TCR band is three times better; it also gives 50% more signal. Choose it if 0.675 W is acceptable for the board's thermal design.

### Solution 06-11.12

(a) Looking into the terminals of one resistor with the source shorted: 1 MΩ in parallel with the other two (2 MΩ), **666.7 kΩ**; the open-circuit voltage is 3 V.

(b) $3\times10/(10 + 0.6667) = $ **2.8125 V** across each; the sum is **8.4375 V**.

(c) $3\times10{,}000/10{,}000.667 = $ **2.9998 V**.

Each 10 MΩ reading is taken with the meter connected across a different resistor, changing the circuit each time; the three readings never coexist. If all three meters were connected at once, the three loaded resistors would have equal voltages summing exactly to 9 V. KVL is never violated.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 06-11.1a | reading with 10 MΩ | 9.901 | V |
| 06-11.1b | error with 10 MΩ | −0.99 | % |
| 06-11.1c | reading with 10 GΩ | 9.9999 | V |
| 06-11.1d | error with 10 GΩ | −10 | ppm |
| 06-11.2a | reading | 88.24 | mA |
| 06-11.2b | error | −11.8 | % |
| 06-11.2c | burden voltage | 176.5 | mV |
| 06-11.2d | corrected current | 100.0 | mA |
| 06-11.3a | uncertainty | 16.2 | mV |
| 06-11.3b | relative uncertainty | 0.130 | % |
| 06-11.4a | Thévenin resistance | 1.429 | MΩ |
| 06-11.4b | open-circuit voltage | 5.143 | V |
| 06-11.5a | shunt for 50 mV at 5 A | 10 | mΩ |
| 06-11.5b | dissipation of the 10 mΩ shunt | 0.25 | W |
| 06-11.5c | full-scale signal with 1 mΩ | 5 | mV |
| 06-11.5d | dissipation of the 1 mΩ shunt | 25 | mW |
| 06-11.5e | offset with 10 mΩ, % of full scale | 0.1 | % |
| 06-11.5f | offset with 1 mΩ, % of full scale | 1 | % |
| 06-11.6a | sheet resistance | 0.4926 | mΩ/□ |
| 06-11.6b | squares | 80 | — |
| 06-11.6c | resistance at 20 °C | 39.41 | mΩ |
| 06-11.6d | voltage drop | 78.82 | mV |
| 06-11.6e | dissipation | 157.6 | mW |
| 06-11.6f | resistance at 85 °C | 49.47 | mΩ |
| 06-11.7a | error voltage | 60 | mV |
| 06-11.7b | error as % of full scale | 6 | % |
| 06-11.8a | two-wire reading | 110 | mΩ |
| 06-11.8b | factor | 11 | — |
| 06-11.8c | four-wire sensed voltage | 10 | mV |
| 06-11.9a | nominal ADC voltage | 3.2 | V |
| 06-11.9b | loading error | −0.925 | % |
| 06-11.9c | nominal ADC voltage with loading | 3.170 | V |
| 06-11.9d | worst-case ratio error, high | 1.88 | % |
| 06-11.9e | worst-case ratio error, low | −1.85 | % |
| 06-11.9f | total worst case, high | 2.39 | % |
| 06-11.9g | total worst case, low | −2.34 | % |
| 06-11.9h | ratio error with 0.1% resistors | 0.19 | % |
| 06-11.9i | total worst case with 0.1%, high | 0.69 | % |
| 06-11.9j | total worst case with 0.1%, low | −0.69 | % |
| 06-11.10a | maximum round-trip resistance | 50 | mΩ |
| 06-11.10b | longest 16 AWG pair | 1.90 | m |
| 06-11.10c | 14 AWG diameter | 1.628 | mm |
| 06-11.10d | 14 AWG resistance per meter | 8.285 | mΩ/m |
| 06-11.10e | longest 14 AWG pair | 3.02 | m |
| 06-11.11a | dissipation, 2 mΩ | 0.45 | W |
| 06-11.11b | temperature rise, 2 mΩ | 22.5 | °C |
| 06-11.11c | worst-case change, 2 mΩ | 0.56 | % |
| 06-11.11d | dissipation, 5 mΩ | 1.125 | W |
| 06-11.11e | temperature rise, 3 mΩ | 33.75 | °C |
| 06-11.11f | worst-case change, 3 mΩ | 0.25 | % |
| 06-11.11g | signal, 3 mΩ | 45 | mV |
| 06-11.11h | signal, 2 mΩ | 30 | mV |
| 06-11.12a | Thévenin resistance across one resistor | 666.7 | kΩ |
| 06-11.12b | reading with 10 MΩ | 2.8125 | V |
| 06-11.12c | sum of three readings | 8.4375 | V |
| 06-11.12d | reading with 10 GΩ | 2.9998 | V |
