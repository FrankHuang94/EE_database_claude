# Full-Length FE Practice Exam · Electrical and Computer

**Covers:** all seven terms, in the proportions of the NCEES FE Electrical and Computer specification ([R-001](../../reference/research-log.md#r-001--ncees-fe-electrical-and-computer-specification)): each area's question count lies inside its published range, scaled to 110.

**Format:**

- **Questions:** 110, of which 64 are multiple choice and 46 numeric entry.
- **Time:** two parts of 2 h 40 min each, 5 h 20 min in all, the FE's exam time.
- **Break:** take a short break between the parts, as the real exam's appointment allows.

**Materials:** an FE-approved calculator and the *NCEES FE Reference Handbook* only (free PDF from NCEES), with no notes. Compute every interest factor from its formula, since tables cover only selected rates. Constants are given below.

**What this exam is and is not.** It covers every knowledge area at FE depth and in FE proportions, but it is not a replica:

- **No figures:** every circuit and block diagram is described in words, where the real exam shows a drawing.
- **Mostly one or two steps:** the real exam has more multi-step items and other item formats.

Use it to find weak areas and to rehearse pacing, not to predict a score.

**Scoring:**

- Score each knowledge area separately, and aim for at least 70% in every area.
- Then look at the total. The FE is pass/fail on a scaled score, so a total of about 70% is a reasonable practice target, not an official cut score.
- Solutions with full working, and the mistake behind every wrong option, are in [solutions.md](solutions.md).
- Every number is checked by [verify_fe.py](verify_fe.py), and the circuit results are also simulated in ngspice ([fe_circuits.cir](fe_circuits.cir)).

**Conventions:**

- For numeric entry, give 3 significant figures unless the question says otherwise or the answer is an integer.
- Constants:
  - $\varepsilon_0 = 8.854 \times 10^{-12}$ F/m, $\mu_0 = 4\pi \times 10^{-7}$ H/m;
  - $1/(4\pi\varepsilon_0) = 8.988 \times 10^9$ N·m²/C²;
  - $c = 3.00 \times 10^8$ m/s;
  - thermal noise density at 290 K is −174 dBm/Hz.
- Money: cash flows at the end of each period; $i$ is the rate per period.
- Diodes: the constant-voltage model with 0.7 V unless stated.
- MOSFET in saturation: $I_D = \tfrac12 k'(W/L)(V_{GS} - V_{TH})^2$.
- Phasors: peak amplitude, cosine reference.

| Part | Questions | FE knowledge areas (questions) |
|---|---|---|
| 1 | 1–55 | Mathematics (12), Probability and statistics (5), Ethics and professional practice (4), Engineering economics (5), Properties of electrical materials (4), Circuit analysis (11), Linear systems (7), Signal processing (7) |
| 2 | 56–110 | Electronics (9), Power systems (9), Electromagnetics (4), Control systems (7), Communications (5), Computer networks (4), Digital systems (8), Computer systems (5), Software engineering (4) |

---

## Part 1

### Mathematics (questions 1–12)

**1.** The solutions of $y'' + 4y' + 13y = 0$ oscillate at an angular frequency, in rad/s, of:
(A) 3.61 · (B) 13 · (C) 2 · (D) 3

**2.** *Numeric entry.* Find the angle, in degrees, between $\mathbf a = (1, 2, 2)$ and $\mathbf b = (2, -1, 2)$.

**3.** For $f(x) = x^3e^{-x}$, $f'(1)$ equals:
(A) 1.10 · (B) −0.368 · (C) 0.736 · (D) 0.368

**4.** The second-order Taylor approximation of $\sqrt{1 + x}$ about $x = 0$, evaluated at $x = 0.4$, is:
(A) 1.160 · (B) 1.183 · (C) 1.180 · (D) 1.200

**5.** The angle of $-1 + j\sqrt3$, in degrees, is:
(A) 240 · (B) 60 · (C) 120 · (D) −60

**6.** *Numeric entry.* $dy/dt + 4y = 8$ with $y(0) = 0$. Find $y(0.25)$.

**7.** The larger eigenvalue of $\begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}$ is:
(A) 7 · (B) 10 · (C) 2 · (D) 5

**8.** One Newton–Raphson step for $x^2 - 2 = 0$ from $x_0 = 1$ gives $x_1$ equal to:
(A) 1.500 · (B) 0.500 · (C) 1.414 · (D) 2.000

**9.** *Numeric entry.* Find the magnitude of $(3 + j4)/(1 - j)$.

**10.** $\int_0^{\pi} \sin^2 x \, dx$ equals:
(A) 2.000 · (B) 1.571 · (C) 0.785 · (D) 3.142

**11.** *Numeric entry.* For $f(x, y) = x^2y + 3y^2$, find the magnitude of the gradient at $(1, 2)$.

**12.** *Numeric entry.* Solve $x + y + z = 6$, $2x - y + z = 3$, $x + 2y - z = 2$, and give $z$.

### Probability and statistics (questions 13–17)

**13.** *Numeric entry.* A part shows no failures in $10^8$ device-hours. Assuming a constant failure rate, find the 95% upper confidence bound on the rate, in FIT (failures per $10^9$ device-hours).

**14.** A test flags 95% of defective units and 5% of good ones. If 2% of units are defective, the probability that a flagged unit is defective is:
(A) 0.019 · (B) 0.950 · (C) 0.068 · (D) 0.279

**15.** Each part is defective with probability 0.02, independently. The probability that a lot of 50 has at most one defective part is:
(A) 0.364 · (B) 0.264 · (C) 0.736 · (D) 0.372

**16.** A resistor value is normal with mean 1000 Ω and standard deviation 10 Ω. The fraction within 980 Ω to 1020 Ω is:
(A) 0.9545 · (B) 0.4772 · (C) 0.6827 · (D) 0.9973

**17.** *Numeric entry.* Twenty-five measurements of a 3.3 V rail have a sample standard deviation of 0.05 V. Find the half-width of the 95% confidence interval for the mean, in mV.

### Ethics and professional practice (questions 18–21)

**18.** *Numeric entry.* A US utility patent application is filed on 1 March 2021 and granted in 2024. Ignoring term adjustments and extensions, in which year does the patent expire?

**19.** A vendor offers an engineer a gift while the engineer is choosing between its part and a competitor's for an employer's project. Under the NSPE Code, the engineer should:
(A) accept it if the vendor's part is the best choice · (B) accept it and disclose it after the award · (C) decline it · (D) accept it if it is worth less than \$100

**20.** An engineer is asked to seal drawings that someone else prepared outside the engineer's direction and control. Under the NSPE Code, the engineer should:
(A) seal them after a brief review · (B) refuse to seal them · (C) seal them if the preparer is licensed in another state · (D) seal them if the client agrees in writing

**21.** After sign-off, an engineer finds a flaw that endangers the public. The employer declines to act. Under the NSPE Code of Ethics, the engineer's first obligation is to:
(A) the client · (B) the employer · (C) the reputation of the profession · (D) the public's safety, health and welfare

### Engineering economics (questions 22–26)

**22.** *Numeric entry.* Equipment costs \$120k, has a \$20k salvage value and a 5-year life. Find its straight-line book value after 3 years, in \$k.

**23.** The present worth of \$10,000 received in 5 years at 8% a year, in dollars, is:
(A) 7143 · (B) 6000 · (C) 6806 · (D) 14693

**24.** A nominal rate of 6% a year compounded quarterly is an effective annual rate, in percent, of:
(A) 6.00 · (B) 6.18 · (C) 6.14 · (D) 1.50

**25.** *Numeric entry.* A tester costs \$50,000, lasts 6 years and is sold for \$5,000 at the end. At 8% a year, find its equivalent annual cost, in \$k.

**26.** A product has fixed costs of \$200,000 a year, sells for \$50 and costs \$30 per unit to make. The break-even volume, in units a year, is:
(A) 4000 · (B) 10000 · (C) 6667 · (D) 2500

### Properties of electrical materials (questions 27–30)

**27.** A copper winding measures 10.0 Ω at 20 °C. With $\alpha = 0.00393$ /°C, its resistance at 75 °C, in Ω, is:
(A) 12.2 · (B) 2.16 · (C) 8.22 · (D) 12.9

**28.** A parallel-plate capacitor has plates of 1 cm², a gap of 10 µm and a dielectric with $\varepsilon_r = 4$. Its capacitance, in pF, is:
(A) 22.1 · (B) 354 · (C) 35.4 · (D) 88.5

**29.** *Numeric entry.* Copper ($\rho = 1.72 \times 10^{-8}$ Ω·m) wire is 100 m long and 1.0 mm in diameter. Find its resistance, in Ω.

**30.** *Numeric entry.* Silicon at 300 K ($n_i = 10^{10}$ cm⁻³) is doped with $N_D = 10^{16}$ cm⁻³ donors. Find the hole concentration, in cm⁻³.

### Circuit analysis (questions 31–41)

**31.** *Numeric entry.* Find the impedance magnitude of 30 Ω in series with 0.1 H at 60 Hz, in Ω.

**32.** A periodic voltage is +10 V for 25% of each period and −2 V for the rest. Its rms value, in V, is:
(A) 5.00 · (B) 1.00 · (C) 5.29 · (D) 4.69

**33.** *Numeric entry.* A 2 A source feeds node 1. Resistors: 4 Ω from node 1 to ground, 2 Ω from node 1 to node 2, and 6 Ω from node 2 to ground. Find the node-2 voltage, in V.

**34.** *Numeric entry.* A load draws 10 A rms at 230 V rms with a power factor of 0.8 lagging. Find its reactive power, in kvar.

**35.** A source has a Thévenin equivalent of 10 V and 50 Ω. The most power it can deliver to a resistive load, in W, is:
(A) 0.500 · (B) 0.250 · (C) 2.00 · (D) 1.00

**36.** Seen from its terminals, a network is a 6 Ω resistor in parallel with a 3 Ω resistor, in series with 2 Ω, with all sources turned off. Its Thévenin resistance, in Ω, is:
(A) 4 · (B) 2 · (C) 11 · (D) 2.73

**37.** A 12 V source connects through 2 Ω to node a. From node a to ground are a 4 Ω resistor and a voltage-controlled current source that draws $0.25v_a$ A out of node a, where $v_a$ is the node-a voltage. Then $v_a$, in V, is:
(A) 1.26 · (B) 6.00 · (C) 12.0 · (D) 8.00

**38.** *Numeric entry.* At $\omega$ = 1000 rad/s, a source of phasor $10\angle 0°$ V drives a 4 Ω resistor into node a. From node a to ground are a 4 mH inductor and a second branch, 2 Ω in series with 500 µF. Find the amplitude of the current in the 2 Ω branch, in A.

**39.** A 50 Hz load draws 10 A rms at 230 V rms with a power factor of 0.8 lagging. The shunt capacitance that corrects it to unity power factor, in µF, is:
(A) 166 · (B) 69.2 · (C) 83.0 · (D) 111

**40.** A voltage source drives 30 Ω in series with 0.1 H at 60 Hz. The phase of the current relative to the voltage, in degrees, is:
(A) 51.5 · (B) −38.5 · (C) −0.899 · (D) −51.5

**41.** *Numeric entry.* A 12 V source drives a divider of two 10 kΩ resistors. A 10 kΩ load is connected across the lower resistor. Find the load voltage, in V.

### Linear systems (questions 42–48)

**42.** The 2% settling time of the step response of $1/(0.2s + 1)$, in s, is:
(A) 1.00 · (B) 0.200 · (C) 0.461 · (D) 0.782

**43.** *Numeric entry.* $F(s) = 6/[s(s + 3)]$. Find $f(t)$ at $t = 0.5$.

**44.** *Numeric entry.* A 5 V step is applied through 10 kΩ to an uncharged 100 nF capacitor. Find the capacitor voltage 2 ms later, in V.

**45.** The system $H(s) = (s + 1)/(s^2 + 2s - 3)$ is:
(A) impossible to classify from $H(s)$ · (B) stable · (C) marginally stable · (D) unstable

**46.** A 10 V source is switched onto 100 Ω in series with 10 mH. The current 0.2 ms later, in mA, is:
(A) 13.5 · (B) 86.5 · (C) 100 · (D) 63.2

**47.** *Numeric entry.* Find the magnitude of $H(s) = 1000/(s + 10)$ at $\omega$ = 100 rad/s, in dB.

**48.** A series circuit of 2 mH, 50 nF and 10 Ω has a quality factor of:
(A) 0.0500 · (B) 3.18 · (C) 200 · (D) 20.0

### Signal processing (questions 49–55)

**49.** The ideal SNR of a 12-bit ADC with a full-scale sine input, in dB, is:
(A) 74.0 · (B) 70.5 · (C) 72.2 · (D) 36.1

**50.** A ±1 V square wave with 50% duty cycle has a fundamental component of amplitude, in V:
(A) 1.00 · (B) 0.900 · (C) 0.637 · (D) 1.27

**51.** The Nyquist rate of a signal band-limited to 4 kHz, in kHz, is:
(A) 4 · (B) 2 · (C) 8 · (D) 50.3

**52.** A 1024-point DFT of a signal sampled at 44.1 kHz has a bin spacing, in Hz, of:
(A) 86.1 · (B) 44.1 · (C) 43.1 · (D) 21.5

**53.** *Numeric entry.* $H(z) = 1/(1 - 0.5z^{-1})$, causal. Find $h[3]$.

**54.** *Numeric entry.* A 7 kHz tone is sampled at 10 kHz. Find the frequency at which it appears, in kHz.

**55.** *Numeric entry.* $x[n] = \{1, 2, 3\}$ and $h[n] = \{1, -1, 2\}$, both starting at $n = 0$. Find $y[2]$ for $y = x * h$.

---

## Part 2

### Electronics (questions 56–64)

**56.** An NMOS transistor in saturation has $k'(W/L)$ = 2 mA/V², $V_{GS}$ = 1.3 V and $V_{TH}$ = 0.5 V. Its drain current, in mA, is:
(A) 0.800 · (B) 0.640 · (C) 1.69 · (D) 1.28

**57.** *Numeric entry.* The NMOS transistor of the previous question ($k'(W/L)$ = 2 mA/V², $V_{GS}$ = 1.3 V, $V_{TH}$ = 0.5 V) has a 5 kΩ drain resistor to a 5 V supply. Ignoring $r_o$, find the small-signal voltage gain of this common-source amplifier.

**58.** A differential amplifier has a differential gain of 1000 and a common-mode gain of 0.1. Its CMRR, in dB, is:
(A) 60 · (B) 40 · (C) 80 · (D) −80

**59.** A full-wave rectifier on a 60 Hz supply (12 V peak) charges a 1000 µF capacitor that supplies a steady 100 mA. The peak-to-peak ripple, in V, is about:
(A) 0.833 · (B) 0.133 · (C) 1.67 · (D) 0.241

**60.** *Numeric entry.* A silicon diode in series with 1 kΩ is forward-biased from 5 V. Find the current, in mA.

**61.** *Numeric entry.* An npn transistor ($\beta = 100$, $V_{BE}$ = 0.7 V) has 100 kΩ from a 5 V supply to its base and 1 kΩ from a 10 V supply to its collector; the emitter is grounded. Find $V_{CE}$, in V.

**62.** *Numeric entry.* An op-amp with a 10 MHz gain-bandwidth product is set for a non-inverting gain of 20. Find the closed-loop bandwidth, in kHz.

**63.** A 120 Ω strain gauge with a gauge factor of 2.0 is one arm of a Wheatstone bridge whose other arms are fixed 120 Ω resistors, excited at 5 V. At a strain of 500 µε, the bridge output, in mV, is about:
(A) 5.00 · (B) 2.50 · (C) 0.625 · (D) 1.25

**64.** A 5.1 V Zener is fed from 12 V through 470 Ω and loaded by 1 kΩ. The Zener current, in mA, is:
(A) 9.58 · (B) 19.8 · (C) 5.10 · (D) 14.7

### Power systems (questions 65–73)

**65.** *Numeric entry.* A balanced wye load of 10 Ω resistive per phase is supplied at 480 V line to line. Find the total power, in kW.

**66.** On a 100 MVA three-phase base and a 138 kV line-to-line base, the base impedance, in Ω, is:
(A) 63.5 · (B) 0.00525 · (C) 1.38 · (D) 190

**67.** A three-phase line with 2 Ω of resistance per phase delivers 10 MW at 0.9 power factor and 33 kV line to line. The line loss, in kW, is:
(A) 680 · (B) 227 · (C) 75.6 · (D) 184

**68.** *Numeric entry.* A single-phase 50 kVA, 7200/240 V transformer. Find its rated secondary current, in A.

**69.** A balanced wye load of 10 Ω resistive per phase is supplied at 480 V line to line. Its line current, in A, is:
(A) 16.0 · (B) 48.0 · (C) 83.1 · (D) 27.7

**70.** The synchronous speed of a 6-pole, 50 Hz machine, in rpm, is:
(A) 960 · (B) 1000 · (C) 500 · (D) 2000

**71.** *Numeric entry.* A 4-pole, 60 Hz induction motor runs at 1746 rpm. Find its slip, in percent.

**72.** A load draws 40 kW at 0.8 power factor lagging. Capacitors supplying 18 kvar are added. The new power factor is:
(A) 0.912 · (B) 0.640 · (C) 0.800 · (D) 0.958

**73.** An ideal buck converter in continuous conduction steps 12 V down to 3.3 V. Its duty cycle is:
(A) 3.64 · (B) 0.216 · (C) 0.725 · (D) 0.275

### Electromagnetics (questions 74–77)

**74.** At 1 GHz, the wavelength in a coaxial cable with $\varepsilon_r = 2.25$, in m, is:
(A) 0.133 · (B) 0.200 · (C) 0.450 · (D) 0.300

**75.** *Numeric entry.* Find the magnetic flux density 5 cm from a long straight wire carrying 10 A, in µT.

**76.** *Numeric entry.* A 50 Ω line is terminated in 25 Ω. Find the VSWR.

**77.** A lossless quarter-wave section of 50 Ω line is terminated in 100 Ω. Its input impedance, in Ω, is:
(A) 25.0 · (B) 100 · (C) 50.0 · (D) 200

### Control systems (questions 78–84)

**78.** The final value of the unit-step response of $G(s) = 5/(s^2 + 3s + 10)$ is:
(A) 1.67 · (B) 0.500 · (C) 0.00 · (D) 5.00

**79.** With unity feedback and $G(s) = 20/[s(s + 4)]$, the steady-state error to a unit ramp is:
(A) 0.200 · (B) 5.00 · (C) 0.00 · (D) 0.0500

**80.** *Numeric entry.* $s^3 + 2s^2 + 3s + K$ has all its roots in the left half-plane for $0 < K < K_{max}$. Find $K_{max}$.

**81.** At the gain-crossover frequency the loop's phase is −135°. The phase margin, in degrees, is:
(A) 225 · (B) 135 · (C) 45 · (D) −45

**82.** A controller of gain 5 drives a plant $1/(s + 2)$; a sensor of gain 1.2 feeds the output back to a negative summing junction. The closed-loop DC gain from reference to output is:
(A) 0.750 · (B) 0.714 · (C) 2.50 · (D) 0.625

**83.** *Numeric entry.* Find the percent overshoot of a standard second-order step response with $\zeta = 0.5$.

**84.** *Numeric entry.* A closed loop has characteristic polynomial $s^2 + 4s + 25$. Find the peak time of its step response, in s.

### Communications (questions 85–89)

**85.** *Numeric entry.* A transmitter sends 20 dBm through a 10 dBi antenna. The path loss is 110 dB and the receive antenna is 3 dBi. Find the received power, in dBm.

**86.** *Numeric entry.* An FM signal has a peak deviation of 75 kHz and a top modulating frequency of 15 kHz. Find its Carson's-rule bandwidth, in kHz.

**87.** *Numeric entry.* Find the Shannon capacity of a 1 MHz channel with an SNR of 15 (linear), in Mb/s.

**88.** A 16-QAM link runs at 10 Msymbol/s. Its raw bit rate, in Mb/s, is:
(A) 40 · (B) 20 · (C) 2.5 · (D) 160

**89.** The thermal noise power in a 1 MHz bandwidth at 290 K, in dBm, is:
(A) −234 · (B) −144 · (C) −114 · (D) −174

### Computer networks (questions 90–93)

**90.** The protocol that provides reliable, ordered delivery of a byte stream is:
(A) UDP · (B) IP · (C) TCP · (D) Ethernet

**91.** *Numeric entry.* Find the transmission time of a 1500-byte frame on a 100 Mb/s link, in µs.

**92.** A sender appends a message authentication code (MAC), computed with a key it shares with the receiver, to each packet. The MAC gives the receiver:
(A) integrity and authenticity of the data · (B) non-repudiation · (C) protection against denial of service · (D) confidentiality of the data

**93.** The number of usable host addresses in an IPv4 /26 subnet is:
(A) 62 · (B) 30 · (C) 126 · (D) 64

### Digital systems (questions 94–101)

**94.** *Numeric entry.* A 4-bit binary counter is clocked at 1 MHz. Find the frequency of its most significant bit, in kHz.

**95.** Which gate can implement any Boolean function on its own?
(A) OR · (B) NAND · (C) XOR · (D) AND

**96.** A path has 0.12 ns clock-to-Q, 3.1 ns of logic and 0.18 ns setup. Its maximum clock frequency, in MHz, is:
(A) 305 · (B) 329 · (C) 323 · (D) 294

**97.** *Numeric entry.* Convert the binary number 1011 to Gray code, and give the result's decimal value.

**98.** The 8-bit two's-complement value 11110110 is, in decimal:
(A) 246 · (B) −10 · (C) −9 · (D) −118

**99.** A Moore machine detects the input sequence 101, overlaps allowed, with an output of 1 for one clock after each detection. The minimum number of states is:
(A) 4 · (B) 3 · (C) 8 · (D) 2

**100.** *Numeric entry.* A register-to-register path has a 2 ns clock period, 0.2 ns clock-to-Q, 1.4 ns of logic and a 0.15 ns setup time. Find the setup slack, in ns.

**101.** $F(A, B, C, D) = \Sigma m(1, 3, 5, 7, 9, 11) + d(13, 15)$, with $A$ the most significant bit. Its minimal sum of products is:
(A) $\bar AD$ · (B) $D$ · (C) $\bar BD$ · (D) $\bar AD + \bar BD$

### Computer systems (questions 102–106)

**102.** *Numeric entry.* 80% of a program parallelizes perfectly. Find its speedup on 8 cores.

**103.** A cache has a 1 ns hit time, a 5% miss rate and a 60 ns miss penalty. The average memory access time, in ns, is:
(A) 3.00 · (B) 4.00 · (C) 61.0 · (D) 1.05

**104.** A program executes $2 \times 10^9$ instructions at a CPI of 1.5 on a 3 GHz processor. Its execution time, in s, is:
(A) 0.444 · (B) 2.25 · (C) 1.00 · (D) 0.667

**105.** *Numeric entry.* A 32 KB direct-mapped cache with 64-byte lines serves 32-bit byte addresses. Find the number of tag bits.

**106.** A 5-stage pipeline with balanced stages and no hazards runs 100 instructions. Counting the cycles to fill the pipeline, its speedup over the same design without pipelining is:
(A) 4.81 · (B) 4.76 · (C) 5.00 · (D) 1.04

### Software engineering (questions 107–110)

**107.** The test level that checks the interaction between modules is:
(A) unit testing · (B) acceptance testing · (C) regression testing · (D) integration testing

**108.** *Numeric entry.* Find the worst-case number of comparisons a binary search needs on 1,000,000 sorted items.

**109.** *Numeric entry.* How many times does the loop body run?

```text
i ← 3
while i < 30:
    (body)
    i ← i + 4
```

**110.** The structure that offers constant average-time lookup by key is a:
(A) hash table · (B) sorted array · (C) binary search tree · (D) linked list
