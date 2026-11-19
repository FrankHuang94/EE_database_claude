# Solutions 06-10 · The Ideal Op-Amp

Problems: [06-10 problems](../problems/06-10-problems.md) · Chapter: [06-10](../chapters/06-10-ideal-op-amp.md). Every number below is recomputed by [verify_06_10.py](../verify/verify_06_10.py); the circuits of Problems 06-10.1, 06-10.3, 06-10.4, 06-10.9 and 06-10.11 are also confirmed in ngspice ([lab netlist](../labs/06-10-lab/opamps.cir)).

---

## Solutions

### Solution 06-10.1

Gain $-100/4.7 = $ **−21.28**; output for 0.1 V: **−2.128 V**; input resistance **4.7 kΩ** (the source sees $R_1$ to a virtual ground).

### Solution 06-10.2

$1 + R_2/R_1 = 25$ gives $R_2$ = **24 kΩ**. Output $25\times0.2 = $ **5 V**; input resistance infinite (rule 1).

### Solution 06-10.3

$v_{out} = -20\,(1/10 - 0.5/20 + 2/40) = -20\times0.125 = $ **−2.5 V** (each term in mA, times 20 kΩ).

### Solution 06-10.4

(a) Matched: $G = 10$, so $10\times(2.05 - 2.00) = $ **0.5 V**.

(b) With $R_4$ = 101 kΩ: $v_+ = 2.05\times101/111 = 1.8653$ V, so $v_{out} = 1.8653\times11 - 2.00\times10 = $ **0.5185 V**, an error of **18.47 mV** (3.7%). With both inputs at 2.00 V the output is **18.02 mV** instead of zero.

(c) A 2 V common-mode input produces $2/111$ V = 18.02 mV: a common-mode gain of $1/111 = $ **0.009009** and a CMRR of $10\times111 = $ **1110** (**60.9 dB**). The approximation for a single mismatched resistor, $(1 + G)/t = 11/0.01 = $ **1100**, is close; four resistors each up to $t$ off give the $4t$ of the chapter's formula. One resistor 1% off is enough to make the common-mode term a large part of a small differential signal.

### Solution 06-10.5

(a) $v_{out} = -R_f\,i$: **0 to −2.5 V**.

(b) The bias current also flows through $R_f$, adding $I_BR_f$ at the output. LM358: $250\ \text{nA}\times500\ \text{kΩ} = $ **125 mV** (5% of full scale). OPA187: $350\ \text{pA}\times500\ \text{kΩ} = $ **175 µV** (0.007%). Only the OPA187 is usable for a precise measurement; transimpedance amplifiers with large $R_f$ need picoamp bias currents.

### Solution 06-10.6

(a) $1\times10/(100 + 10) = $ **0.0909 V**: 91% of the signal lost.

(b) The follower draws no current, so its input sits at 1 V and its output delivers **1 V** to the ADC from zero output resistance.

(c) $A/(1 + A) = 10^5/(1 + 10^5) = $ **0.99999**: the follower's gain error is $1/A$.

### Solution 06-10.7

(a) **−10**. (b) The offset acts at the + input, and from there to the output the circuit is a non-inverting amplifier of gain $1 + R_2/R_1 = 11$, the noise gain: **22 mV**. The signal sees $-R_2/R_1$, but the op-amp's own errors see $1 + R_2/R_1$.

### Solution 06-10.8

(a) With the + input grounded, the − input is a virtual ground and the bias current into it must come through $R_2$: an output error of $I_BR_2 = 100\ \text{nA}\times100\ \text{kΩ} = $ **10 mV**.

(b) Put $R_3 = R_1\parallel R_2 = $ **9.091 kΩ** in series with the + input. The + bias current through $R_3$ shifts both inputs by $I_{B+}R_3$, and the errors cancel except for the difference of the currents: $I_{OS}R_2 = 10\ \text{nA}\times100\ \text{kΩ} = $ **1 mV**.

### Solution 06-10.9

(a) $|v_{out}| \le 12$ V requires $|v_{in}| \le 12/4.7 = $ **2.553 V**.

(b) For 3 V the output would need −14.1 V, so it sits at **−12 V**. The − input is then set by the divider between the input and the stuck output: $v_- = (3\times47 + (-12)\times10)/57 = $ **0.3684 V**, while $v_+$ = 0. The virtual short needs the output to be free to move; once it saturates, there is no feedback and the inputs separate.

### Solution 06-10.10

(a) $1 + 2R/R_G = G$ gives $R_G = 2R/(G - 1)$: **49.45 Ω** for 1000 and **499.0 Ω** for 100.

(b) Difference stage: $(1 + 1)/(4\times0.0002) = $ **2500**. The first stage multiplies by its gain, 100: overall **250,000**, about **108 dB**.

### Solution 06-10.11

(a) With $v_+ = 0$ the op-amp gives $v_{out} = A(0 - v_-)$, so $v_- = -v_{out}/A$: no longer exactly zero. No current enters the op-amp, so KCL at the − input is

$$
\frac{v_{in} - v_-}{R_1} = \frac{v_- - v_{out}}{R_2}.
$$

Multiply by $R_2$ and substitute $v_- = -v_{out}/A$:

$$
\frac{R_2}{R_1}\Bigl(v_{in} + \frac{v_{out}}{A}\Bigr) = -\frac{v_{out}}{A} - v_{out}
\;\Rightarrow\;
\frac{R_2}{R_1}v_{in} = -v_{out}\Bigl(1 + \frac{1 + R_2/R_1}{A}\Bigr),
$$

so $v_{out}/v_{in} = -(R_2/R_1)/\bigl(1 + (1 + R_2/R_1)/A\bigr)$, as stated. As $A \to \infty$ it tends to the ideal $-R_2/R_1$. Numerically, $-100/(1 + 101/10^4) = -100/1.0101 = $ **−99.00**.

(b) **1.0%**, set by the noise gain $1 + R_2/R_1 = 101$ divided by $A$, not by the signal gain.

### Solution 06-10.12

(a) $0.1\%\times50\ \text{mV} = $ **50 µV**.

(b) The LM358's 7 mV maximum offset is 140 times the budget: unusable without calibration. The OPA187's 10 µV fits, using **20%** of the budget and leaving room for resistor and gain errors.


### Solution 06-10.13

(a) The divider gives $5\times20/(30 + 20) = $ **2.0 V** at the − input (no current enters it, rule 1).

(b) At 1.8 V the + input is below the threshold, so the output sits at **−12 V**; at 2.3 V it is above, so the output sits at **+12 V**.

(c) The inputs are $2.3 - 2.0 = $ **0.3 V** apart. The virtual short is a consequence of negative feedback, which pulls the inputs together; with no feedback, nothing does, and the output simply saturates in the direction of the difference.

(d) $12/10^5 = $ **120 µV**: a difference that small already saturates the output, which is why a comparator's output is effectively a logic level.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 06-10.1a | gain | −21.28 | — |
| 06-10.1b | output for 0.1 V | −2.128 | V |
| 06-10.1c | input resistance | 4.7 | kΩ |
| 06-10.2a | R_2 | 24 | kΩ |
| 06-10.2b | output for 0.2 V | 5 | V |
| 06-10.3a | output | −2.5 | V |
| 06-10.4a | matched output | 0.5 | V |
| 06-10.4b | output with R_4 1% high | 0.5185 | V |
| 06-10.4c | error | 18.47 | mV |
| 06-10.4d | output with equal inputs | 18.02 | mV |
| 06-10.4e | common-mode gain | 0.009009 | — |
| 06-10.4f | CMRR | 1110 | — |
| 06-10.4g | CMRR in dB | 60.9 | dB |
| 06-10.4h | single-resistor approximation (1 + G)/t | 1100 | — |
| 06-10.5a | full-scale output | −2.5 | V |
| 06-10.5b | LM358 bias error | 125 | mV |
| 06-10.5c | OPA187 bias error | 175 | µV |
| 06-10.6a | ADC voltage without buffer | 0.0909 | V |
| 06-10.6b | ADC voltage with follower | 1 | V |
| 06-10.6c | follower gain with A = 1e5 | 0.99999 | — |
| 06-10.7a | signal gain | −10 | — |
| 06-10.7b | output offset | 22 | mV |
| 06-10.8a | uncompensated error | 10 | mV |
| 06-10.8b | compensation resistor | 9.091 | kΩ |
| 06-10.8c | remaining error | 1 | mV |
| 06-10.9a | linear input limit | 2.553 | V |
| 06-10.9b | output for 3 V | −12 | V |
| 06-10.9c | inverting-input voltage | 0.3684 | V |
| 06-10.10a | R_G for gain 1000 | 49.45 | Ω |
| 06-10.10b | R_G for gain 100 | 499.0 | Ω |
| 06-10.10c | difference-stage CMRR | 2500 | — |
| 06-10.10d | overall CMRR | 250000 | — |
| 06-10.10e | overall CMRR in dB | 108 | dB |
| 06-10.11a | gain | −99.00 | — |
| 06-10.11b | gain error | 1.0 | % |
| 06-10.12a | error budget | 50 | µV |
| 06-10.12b | OPA187 share of the budget | 20 | % |
| 06-10.12c | LM358 offset over budget | 140 | — |
| 06-10.13a | threshold | 2.0 | V |
| 06-10.13b | output at 1.8 V | −12 | V |
| 06-10.13c | output at 2.3 V | 12 | V |
| 06-10.13d | input difference at 2.3 V | 0.3 | V |
| 06-10.13e | difference that saturates the output | 120 | µV |
