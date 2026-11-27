# Full-Length FE Practice Exam · Electrical and Computer

**Covers:** all seven terms, in the proportions of the NCEES FE Electrical and Computer specification ([R-001](../../reference/research-log.md#r-001--ncees-fe-electrical-and-computer-specification); counts within each area's published range, scaled to 110).

**Format:**

- **Questions:** 110, multiple choice and numeric entry.
- **Time:** two parts of 2 h 40 min each, 5 h 20 min in all, the FE's exam time.
- **Break:** take a 25-minute break between the parts, as the real exam allows.

**Materials:** an FE-approved calculator and the *NCEES FE Reference Handbook* only (free PDF from NCEES), with no notes. The handbook has the standard normal and t tables, the interest factors and the formulas used here; constants are given below.

**Scoring:**

- Score each knowledge area separately, and aim for at least 70% in every area.
- Then look at the total. The FE is pass/fail on a scaled score, so a total of about 70% is a reasonable practice target, not an official cut score.
- Solutions with full working are in [solutions.md](solutions.md).
- Every number is checked by [verify_fe.py](verify_fe.py).

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

| Part | Questions | FE knowledge areas (questions) |
|---|---|---|
| 1 | 1–54 | Mathematics (13), Probability and Statistics (4), Ethics and Professional Practice (4), Engineering Economics (5), Properties of Electrical Materials (4), Circuit Analysis (14), Linear Systems (5), Signal Processing (5) |
| 2 | 55–110 | Electronics (8), Power Systems (9), Electromagnetics (4), Control Systems (7), Communications (5), Computer Networks (4), Digital Systems (10), Computer Systems (5), Software Engineering (4) |

---

## Part 1

### Mathematics (questions 1–13)

**1.** *Numeric entry.* For $f(x) = x^3e^{-x}$, find $f'(1)$.

**2.** $\int_0^{\pi} \sin^2 x \, dx$ equals:
(A) 3.142 · (B) 1.571 · (C) 0.785 · (D) 2.000

**3.** *Numeric entry.* Solve $x + y + z = 6$, $2x - y + z = 3$, $x + 2y - z = 2$, and give $z$.

**4.** The larger eigenvalue of $\begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}$ is:
(A) 7 · (B) 10 · (C) 3.5 · (D) 5

**5.** *Numeric entry.* Find the magnitude of $(3 + j4)/(1 - j)$.

**6.** The angle of $-1 + j\sqrt3$, in degrees, is:
(A) 60 · (B) −60 · (C) 120 · (D) 240

**7.** *Numeric entry.* $dy/dt + 4y = 8$ with $y(0) = 0$. Find $y(0.25)$.

**8.** The solutions of $y'' + 4y' + 13y = 0$ oscillate at an angular frequency, in rad/s, of:
(A) 3 · (B) 2 · (C) 3.61 · (D) 13

**9.** *Numeric entry.* $F(s) = 6/[s(s + 3)]$. Find $f(t)$ at $t = 0.5$.

**10.** The second-order Taylor approximation of $\sqrt{1 + x}$ about $x = 0$, evaluated at $x = 0.1$, is:
(A) 1.050 · (B) 1.010 · (C) 1.095 · (D) 1.049

**11.** *Numeric entry.* For $f(x, y) = x^2y + 3y^2$, find the magnitude of the gradient at $(1, 2)$.

**12.** One Newton–Raphson step for $x^2 - 2 = 0$ from $x_0 = 1$ gives $x_1$ equal to:
(A) 1.25 · (B) 1.5 · (C) 1.414 · (D) 2

**13.** *Numeric entry.* Find the angle, in degrees, between $\mathbf a = (1, 2, 2)$ and $\mathbf b = (2, -1, 2)$.

### Probability and statistics (questions 14–17)

**14.** A resistor value is normal with mean 1000 Ω and standard deviation 10 Ω. The fraction within 980 Ω to 1020 Ω is:
(A) 0.6827 · (B) 0.9973 · (C) 0.9545 · (D) 0.9000

**15.** *Numeric entry.* Each part is defective with probability 0.02, independently. Find the probability that a lot of 50 has no defective part.

**16.** A test flags 95% of defective units and 5% of good ones. If 2% of units are defective, the probability that a flagged unit is defective is:
(A) 0.279 · (B) 0.950 · (C) 0.019 · (D) 0.500

**17.** *Numeric entry.* Twenty-five measurements of a 3.3 V rail have a sample standard deviation of 0.05 V. Find the half-width of the 95% confidence interval for the mean, in mV.

### Ethics and professional practice (questions 18–21)

**18.** After sign-off, an engineer finds a flaw that endangers the public. The employer declines to act. Under the NCEES Model Rules, the engineer's first obligation is to:
(A) the client · (B) the public's health, safety and welfare · (C) the employer · (D) the reputation of the profession

**19.** A vendor offers an engineer a gift while the engineer is choosing between its part and a competitor's for an employer's project. The engineer should:
(A) accept it if it is worth less than \$100 · (B) accept it and disclose it after the award · (C) accept it if the vendor's part is the best choice · (D) decline it

**20.** An engineer is asked to seal drawings that were prepared by someone outside their responsible charge. The engineer should:
(A) refuse to seal them · (B) seal them after a brief review · (C) seal them if the preparer is licensed in another state · (D) seal them for an additional fee

**21.** *Numeric entry.* A US utility patent application is filed on 1 March 2021 and granted in 2024. Ignoring term adjustments and extensions, in which year does the patent expire?

### Engineering economics (questions 22–26)

**22.** The present worth of \$10,000 received in 5 years at 8% a year, in dollars, is:
(A) 6806 · (B) 7350 · (C) 6000 · (D) 14693

**23.** *Numeric entry.* A tester costs \$50,000, lasts 6 years and is sold for \$5,000. At 7%, find its equivalent annual cost, in \$k.

**24.** A product has fixed costs of \$200,000 a year, sells for \$50 and costs \$30 per unit to make. The break-even volume, in units a year, is:
(A) 4000 · (B) 6667 · (C) 2500 · (D) 10000

**25.** *Numeric entry.* Equipment costs \$120k, has a \$20k salvage value and a 5-year life. Find its straight-line book value after 3 years, in \$k.

**26.** A nominal rate of 6% a year compounded quarterly is an effective annual rate, in percent, of:
(A) 6.00 · (B) 6.17 · (C) 6.14 · (D) 1.50

### Properties of electrical materials (questions 27–30)

**27.** *Numeric entry.* Copper ($\rho = 1.72 \times 10^{-8}$ Ω·m) wire is 100 m long and 1.0 mm in diameter. Find its resistance, in Ω.

**28.** A copper winding measures 10.0 Ω at 20 °C. With $\alpha = 0.00393$ /°C, its resistance at 75 °C, in Ω, is:
(A) 10.2 · (B) 12.2 · (C) 13.9 · (D) 11.0

**29.** *Numeric entry.* Silicon at 300 K ($n_i = 10^{10}$ cm⁻³) is doped with $N_D = 10^{16}$ cm⁻³ donors. Find the hole concentration, in cm⁻³.

**30.** A parallel-plate capacitor has plates of 1 cm², a gap of 10 µm and a dielectric with $\varepsilon_r = 4$. Its capacitance, in pF, is:
(A) 88.5 · (B) 35.4 · (C) 3540 · (D) 354

### Circuit analysis (questions 31–44)

**31.** *Numeric entry.* A 12 V source drives a divider of two 10 kΩ resistors. A 10 kΩ load is connected across the lower resistor. Find the load voltage, in V.

**32.** Seen from its terminals, a network is a 6 Ω resistor in parallel with a 3 Ω resistor, in series with 2 Ω, with all sources turned off. Its Thévenin resistance, in Ω, is:
(A) 4 · (B) 11 · (C) 2 · (D) 6

**33.** *Numeric entry.* A 2 A source feeds node 1. Resistors: 4 Ω from node 1 to ground, 2 Ω from node 1 to node 2, and 6 Ω from node 2 to ground. Find the node-2 voltage, in V.

**34.** A source has a Thévenin equivalent of 10 V and 50 Ω. The most power it can deliver to a resistive load, in W, is:
(A) 1 · (B) 2 · (C) 0.5 · (D) 0.25

**35.** *Numeric entry.* A 5 V step is applied through 10 kΩ to an uncharged 100 nF capacitor. Find the capacitor voltage 2 ms later, in V.

**36.** A 10 V source is switched onto 100 Ω in series with 10 mH. The current reaches 63% of its final value after, in ms:
(A) 1 · (B) 0.1 · (C) 10 · (D) 0.01

**37.** *Numeric entry.* Find the impedance magnitude of 30 Ω in series with 0.1 H at 60 Hz, in Ω.

**38.** The phase of that circuit's current relative to its voltage, in degrees, is:
(A) 51.5 · (B) −38.5 · (C) 0 · (D) −51.5

**39.** *Numeric entry.* Find the resonant frequency of 2 mH in series with 50 nF, in kHz.

**40.** With 10 Ω of series resistance added, that circuit's quality factor is:
(A) 20 · (B) 2 · (C) 200 · (D) 0.05

**41.** *Numeric entry.* A load draws 10 A rms at 230 V rms with a power factor of 0.8 lagging. Find its reactive power, in kvar.

**42.** At 50 Hz, the shunt capacitance that corrects that load to unity power factor, in µF, is:
(A) 26.4 · (B) 8.30 · (C) 83.0 · (D) 166

**43.** *Numeric entry.* An ideal inverting amplifier has $R_f$ = 47 kΩ and $R_{in}$ = 4.7 kΩ. Find the output, in V, for a 0.2 V input.

**44.** A non-inverting amplifier with $R_f$ = 9 kΩ and $R_g$ = 1 kΩ has a gain of:
(A) 9 · (B) 10 · (C) 11 · (D) 0.9

### Linear systems (questions 45–49)

**45.** *Numeric entry.* For $H(s) = 10/(s + 5)$, find $\lvert H(j\omega)\rvert$ at $\omega$ = 5 rad/s.

**46.** The system $H(s) = (s + 1)/(s^2 + 2s - 3)$ is:
(A) stable · (B) marginally stable · (C) impossible to classify from $H(s)$ · (D) unstable

**47.** *Numeric entry.* $x[n] = \{1, 2, 3\}$ and $h[n] = \{1, 1\}$, both starting at $n = 0$. Find $y[2]$ for $y = x * h$.

**48.** The 2% settling time of the step response of $1/(0.2s + 1)$, in s, is:
(A) 0.782 · (B) 0.200 · (C) 0.461 · (D) 1.000

**49.** *Numeric entry.* Find the magnitude of $H(s) = 1000/(s + 10)$ at $\omega$ = 100 rad/s, in dB.

### Signal processing (questions 50–54)

**50.** A signal is band-limited to 4 kHz. The minimum sampling rate that avoids aliasing, in kHz, is:
(A) 4 · (B) 16 · (C) 8 · (D) 2

**51.** *Numeric entry.* A 7 kHz tone is sampled at 10 kHz. Find the frequency at which it appears, in kHz.

**52.** A 1024-point DFT of a signal sampled at 48 kHz has a bin spacing, in Hz, of:
(A) 23.4 · (B) 46.9 · (C) 93.8 · (D) 48.0

**53.** *Numeric entry.* $H(z) = 1/(1 - 0.5z^{-1})$, causal. Find $h[3]$.

**54.** The ideal SNR of a 12-bit ADC with a full-scale sine input, in dB, is:
(A) 72.2 · (B) 61.9 · (C) 98.1 · (D) 74.0

---

## Part 2

### Electronics (questions 55–62)

**55.** *Numeric entry.* A silicon diode in series with 1 kΩ is forward-biased from 5 V. Find the current, in mA.

**56.** A 5.1 V Zener is fed from 12 V through 470 Ω and loaded by 1 kΩ. The Zener current, in mA, is:
(A) 9.58 · (B) 14.7 · (C) 5.10 · (D) 19.8

**57.** *Numeric entry.* An npn transistor ($\beta = 100$, $V_{BE}$ = 0.7 V) has 100 kΩ from a 5 V supply to its base and 1 kΩ from a 10 V supply to its collector; the emitter is grounded. Find $V_{CE}$, in V.

**58.** An NMOS transistor in saturation has $k'(W/L)$ = 2 mA/V², $V_{GS}$ = 1.5 V and $V_{TH}$ = 0.5 V. Its drain current, in mA, is:
(A) 2.00 · (B) 0.500 · (C) 1.00 · (D) 4.00

**59.** *Numeric entry.* That transistor drives a 5 kΩ drain resistor as a common-source amplifier. Ignoring $r_o$, find the small-signal voltage gain.

**60.** A full-wave rectifier at 60 Hz charges a 1000 µF capacitor that supplies 100 mA. The peak-to-peak ripple, in V, is about:
(A) 1.67 · (B) 0.833 · (C) 0.417 · (D) 8.33

**61.** *Numeric entry.* An op-amp with a 10 MHz gain-bandwidth product is set for a non-inverting gain of 20. Find the closed-loop bandwidth, in kHz.

**62.** A differential amplifier has a differential gain of 1000 and a common-mode gain of 0.1. Its CMRR, in dB, is:
(A) 60 · (B) 40 · (C) 100 · (D) 80

### Power systems (questions 63–71)

**63.** *Numeric entry.* A balanced wye load of 10 Ω resistive per phase is supplied at 480 V line to line. Find the total power, in kW.

**64.** The line current of that load, in A, is:
(A) 27.7 · (B) 48.0 · (C) 16.0 · (D) 83.1

**65.** *Numeric entry.* A 50 kVA, 7200/240 V transformer. Find its rated secondary current, in A.

**66.** On a 100 MVA, 138 kV base, the base impedance, in Ω, is:
(A) 1.38 · (B) 138 · (C) 190 · (D) 13800

**67.** *Numeric entry.* A 4-pole, 60 Hz induction motor runs at 1746 rpm. Find its slip, in percent.

**68.** The synchronous speed of a 6-pole, 50 Hz machine, in rpm, is:
(A) 1500 · (B) 1000 · (C) 3000 · (D) 750

**69.** *Numeric entry.* A load draws 40 kW and 50 kVA. Find its power factor.

**70.** A three-phase line with 2 Ω of resistance per phase delivers 10 MW at 0.9 power factor and 33 kV line to line. The line loss, in kW, is:
(A) 75.6 · (B) 680 · (C) 113 · (D) 227

**71.** *Numeric entry.* A DC motor on 240 V draws 50 A with an armature resistance of 0.2 Ω. Find its back EMF, in V.

### Electromagnetics (questions 72–75)

**72.** Two 1 µC charges 10 cm apart in vacuum repel with a force, in N, of:
(A) 0.899 · (B) 8.99 · (C) 0.0899 · (D) 89.9

**73.** *Numeric entry.* Find the magnetic flux density 5 cm from a long straight wire carrying 10 A, in µT.

**74.** At 1 GHz, the wavelength in a coaxial cable with $\varepsilon_r = 2.25$, in m, is:
(A) 0.300 · (B) 0.133 · (C) 0.200 · (D) 0.450

**75.** *Numeric entry.* A 50 Ω line is terminated in 75 Ω. Find the VSWR.

### Control systems (questions 76–82)

**76.** With unity feedback and $G(s) = 20/[s(s + 4)]$, the steady-state error to a unit ramp is:
(A) 0 · (B) 0.2 · (C) 5 · (D) 0.05

**77.** *Numeric entry.* Find the percent overshoot of a standard second-order step response with $\zeta = 0.5$.

**78.** $s^3 + 2s^2 + 3s + K$ has all its roots in the left half-plane for $0 < K < K_{max}$. $K_{max}$ is:
(A) 3 · (B) 2 · (C) 12 · (D) 6

**79.** *Numeric entry.* A closed loop has characteristic polynomial $s^2 + 4s + 25$. Find the peak time of its step response, in s.

**80.** At the gain-crossover frequency the loop's phase is −135°. The phase margin, in degrees, is:
(A) 45 · (B) 135 · (C) −45 · (D) 225

**81.** *Numeric entry.* A proportional controller $K_p = 9$ drives a plant $1/(s + 1)$ with unity feedback. Find the closed-loop DC gain.

**82.** The final value of the unit-step response of $G(s) = 5/(s^2 + 3s + 10)$ is:
(A) 5 · (B) 0 · (C) 0.5 · (D) 1.67

### Communications (questions 83–87)

**83.** *Numeric entry.* Find the Shannon capacity of a 1 MHz channel with an SNR of 15 (linear), in Mb/s.

**84.** Double-sideband AM of a 1 MHz carrier by a 5 kHz tone occupies a bandwidth, in kHz, of:
(A) 5 · (B) 10 · (C) 1000 · (D) 20

**85.** *Numeric entry.* An FM signal has a peak deviation of 75 kHz and a top modulating frequency of 15 kHz. Find its Carson's-rule bandwidth, in kHz.

**86.** The thermal noise power in a 1 MHz bandwidth at 290 K, in dBm, is:
(A) −174 · (B) −144 · (C) −84 · (D) −114

**87.** *Numeric entry.* A transmitter sends 20 dBm through a 10 dBi antenna. The path loss is 110 dB and the receive antenna is 3 dBi. Find the received power, in dBm.

### Computer networks (questions 88–91)

**88.** The number of usable host addresses in an IPv4 /26 subnet is:
(A) 62 · (B) 64 · (C) 30 · (D) 126

**89.** *Numeric entry.* Find the transmission time of a 1500-byte frame on a 100 Mb/s link, in µs.

**90.** The protocol that provides reliable, ordered delivery of a byte stream is:
(A) UDP · (B) IP · (C) TCP · (D) Ethernet

**91.** *Numeric entry.* Find the propagation delay over 2000 km of fiber with a signal speed of $2 \times 10^8$ m/s, in ms.

### Digital systems (questions 92–101)

**92.** The 8-bit two's-complement value 11110110 is, in decimal:
(A) 246 · (B) −10 · (C) −118 · (D) −9

**93.** *Numeric entry.* How many minterms does $F(A, B, C) = \bar AB + AC$ have?

**94.** Which gate can implement any Boolean function on its own?
(A) AND · (B) OR · (C) XOR · (D) NAND

**95.** *Numeric entry.* A 4-bit binary counter is clocked at 1 MHz. Find the frequency of its most significant bit, in kHz.

**96.** Hexadecimal 3F is, in decimal:
(A) 63 · (B) 36 · (C) 51 · (D) 15

**97.** *Numeric entry.* A register-to-register path has a 2 ns clock period, 0.2 ns clock-to-Q, 1.4 ns of logic and a 0.15 ns setup time. Find the setup slack, in ns.

**98.** A path has 0.1 ns clock-to-Q, 3.2 ns of logic and 0.2 ns setup. Its maximum clock frequency, in MHz, is:
(A) 313 · (B) 250 · (C) 286 · (D) 333

**99.** *Numeric entry.* A ROM has 12 address bits and 8 data bits. Find its capacity, in bits.

**100.** $F(A, B, C) = \Sigma m(0, 2, 4, 6)$ simplifies to:
(A) $\bar A$ · (B) $\bar C$ · (C) $\bar BC$ · (D) $A + C$

**101.** *Numeric entry.* Convert the binary number 1011 to Gray code, and give the result's decimal value.

### Computer systems (questions 102–106)

**102.** A cache has a 1 ns hit time, a 5% miss rate and a 60 ns miss penalty. The average memory access time, in ns, is:
(A) 3.00 · (B) 61.0 · (C) 1.05 · (D) 4.00

**103.** *Numeric entry.* 80% of a program parallelizes perfectly. Find its speedup on 8 cores.

**104.** A program executes $2 \times 10^9$ instructions at a CPI of 1.5 on a 3 GHz processor. Its execution time, in s, is:
(A) 1.00 · (B) 0.667 · (C) 2.25 · (D) 4.50

**105.** *Numeric entry.* A 32 KB direct-mapped cache with 64-byte lines serves 32-bit byte addresses. Find the number of tag bits.

**106.** An ideal 5-stage pipeline runs 100 instructions. Its speedup over the same design without pipelining is:
(A) 5.00 · (B) 4.00 · (C) 4.81 · (D) 1.04

### Software engineering (questions 107–110)

**107.** *Numeric entry.* Find the worst-case number of comparisons a binary search needs on 1,000,000 sorted items.

**108.** The structure that offers constant average-time lookup by key is a:
(A) linked list · (B) hash table · (C) binary search tree · (D) sorted array

**109.** *Numeric entry.* How many times does the body of `for i in range(3, 30, 4):` run?

**110.** The test level that checks the interaction between modules is:
(A) unit testing · (B) acceptance testing · (C) regression testing · (D) integration testing
