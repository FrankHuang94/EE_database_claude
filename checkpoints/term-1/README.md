# Term 1 Checkpoint · FE-Style Practice Exam

**Covers:** Courses 00–05 (orientation, calculus, complex numbers, differential equations and linear algebra, probability and statistics, physics for EE, programming). **Questions:** 50 (multiple choice and numeric entry). **Time:** 150 minutes, the FE pace of about 3 minutes per question.
**Materials:** an FE-approved calculator and the *NCEES FE Reference Handbook* only (free PDF from NCEES); no course notes or sheets. Finding formulas in the handbook quickly is part of the practice.
**Scoring:** one point per question. Score each block separately and aim for at least 70% in every block. Write every miss into your error log with its cause, and re-solve it a week later. Solutions with full explanations, each pointing to the chapter to revisit, are in [solutions.md](solutions.md); open them only after you finish.

**Conventions:** for numeric entry, give 3 significant figures unless the question says otherwise. Constants: $e = 1.602\times10^{-19}$ C, $\varepsilon_0 = 8.854\times10^{-12}$ F/m, $\mu_0 = 4\pi\times10^{-7}$ H/m, $k_e = 8.988\times10^9$ N·m²/C², $hc$ = 1239.84 eV·nm.

---

## Block 1 · Mathematics (questions 1–18)

**1.** The derivative of $f(x) = x^2e^{-x}$ at $x = 1$ is:
(A) 0.000 · (B) 0.368 · (C) 0.736 · (D) 1.104

**2.** *Numeric entry.* Evaluate $\displaystyle\int_0^{\pi}\sin^2 t\,dt$.

**3.** $\displaystyle\lim_{x\to0}\frac{1 - \cos x}{x^2}$ equals:
(A) 0 · (B) 0.5 · (C) 1 · (D) ∞

**4.** $e^{0.1}$ is approximated by $1 + x + x^2/2$ at $x = 0.1$. The magnitude of the error is closest to:
(A) 1.7×10⁻⁶ · (B) 1.7×10⁻⁵ · (C) 1.7×10⁻⁴ · (D) 1.7×10⁻³

**5.** *Numeric entry.* A 10 V source with 50 Ω internal resistance drives a load resistor $R_L$. What is the largest power, in watts, that $R_L$ can receive?

**6.** For $f(x, y) = x^2y + 3y$, the magnitude of the gradient at $(1, 2)$ is:
(A) 4.00 · (B) 5.66 · (C) 8.00 · (D) 4.47

**7.** *Numeric entry.* A 10 µF capacitor, initially uncharged, charges through 10 kΩ from a 5 V source. What is its voltage, in volts, 20 ms after the source is connected?

**8.** The damping ratio of the system $y'' + 4y' + 13y = 0$ is:
(A) 0.31 · (B) 0.55 · (C) 0.83 · (D) 1.00

**9.** A signal has the Laplace transform $F(s) = \dfrac{5}{s(s + 2)}$. Its final value $\lim_{t\to\infty} f(t)$ is:
(A) 0 · (B) 2.5 · (C) 5 · (D) ∞

**10.** *Numeric entry.* Solve $y' + 2y = 6$ with $y(0) = 0$, and give $y(1)$.

**11.** *Numeric entry.* Compute the determinant of $\begin{bmatrix} 2 & 1 & 0 \\ 1 & 3 & 1 \\ 0 & 1 & 2 \end{bmatrix}$.

**12.** For the system $2x + y = 5$, $x - y = 1$, the value of $x$ is:
(A) 1 · (B) 2 · (C) 3 · (D) 4

**13.** The eigenvalues of $\begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}$ are:
(A) 1 and 6 · (B) 2 and 5 · (C) 3 and 4 · (D) −2 and −5

**14.** *Numeric entry.* Give the entry in row 2, column 2 of the inverse of $\begin{bmatrix} 3 & 1 \\ 2 & 1 \end{bmatrix}$.

**15.** The magnitude of $(3 + j4)(1 - j2)$ is:
(A) 7.07 · (B) 11.18 · (C) 12.50 · (D) 25.00

**16.** $10\angle30^\circ + 10\angle{-30^\circ}$ equals:
(A) 20∠0° · (B) 17.32∠0° · (C) 14.14∠0° · (D) 10∠0°

**17.** *Numeric entry.* The phasor of $v(t) = 5\cos(\omega t + 60^\circ)$ V is written in rectangular form. What is its real part, in volts?

**18.** *Numeric entry.* The three roots of $z^3 = 8$ lie on a circle in the complex plane. What is the distance between two neighboring roots?

## Block 2 · Probability and statistics (questions 19–28)

**19.** Each chip in a batch of 10 is defective independently with probability 0.05. The probability that none is defective is:
(A) 0.315 · (B) 0.500 · (C) 0.599 · (D) 0.950

**20.** *Numeric entry.* Failures of a server arrive as a Poisson process at 2 per year. What is the probability of at least one failure in a given year?

**21.** A resistor's value is normally distributed with mean 1000 Ω and standard deviation 10 Ω. The probability that it lies within 1000 ± 20 Ω is:
(A) 0.683 · (B) 0.866 · (C) 0.954 · (D) 0.997

**22.** *Numeric entry.* A component has exponentially distributed lifetime with mean (MTTF) 10,000 h. What is its probability of surviving 2000 h?

**23.** A test detects a defect with probability 0.99 and flags a good part with probability 0.02. If 1% of parts are defective, the probability that a flagged part is actually defective is closest to:
(A) 0.01 · (B) 0.33 · (C) 0.50 · (D) 0.99

**24.** *Numeric entry.* Two independent resistors, each 1 kΩ with standard deviation 10 Ω, are connected in series. What is the standard deviation, in ohms, of the total resistance?

**25.** A measurement has a known standard deviation of 4 mV. The half-width of a 95% confidence interval for the mean of 25 measurements, in mV, is:
(A) 0.78 · (B) 1.32 · (C) 1.57 · (D) 7.84

**26.** *Numeric entry.* An ideal quantizer rounds to the nearest multiple of 1 mV, and its error is uniformly distributed. What is the RMS quantization error, in mV?

**27.** A random variable takes the values 0, 1 and 2 with probabilities 0.5, 0.3 and 0.2. Its variance is:
(A) 0.49 · (B) 0.61 · (C) 0.70 · (D) 1.10

**28.** *Numeric entry.* On a control chart with ±3σ limits, what is the probability that a point from a process in control (normally distributed) falls outside the limits?

## Block 3 · Physics and electrical materials (questions 29–40)

**29.** Two charges of +1 µC are 10 cm apart in vacuum. The force between them is:
(A) 0.090 N · (B) 0.899 N · (C) 8.99 N · (D) 89.9 N

**30.** *Numeric entry.* A parallel-plate capacitor has plates of 1 cm² separated by 10 µm of a dielectric with relative permittivity 4. What is its capacitance, in pF?

**31.** A 10 µF capacitor charged to 5 V stores:
(A) 25 µJ · (B) 50 µJ · (C) 125 µJ · (D) 250 µJ

**32.** *Numeric entry.* What is the resistance, in ohms, of a copper wire 10 m long and 1.0 mm in diameter ($\rho = 1.72\times10^{-8}$ Ω·m)?

**33.** *Numeric entry.* A copper winding measures 100 Ω at 20 °C; copper's temperature coefficient is 0.00393 /°C. What is its resistance, in ohms, at 70 °C? (Give 5 significant figures.)

**34.** The magnetic flux density 1 cm from a long straight wire carrying 10 A is:
(A) 20 µT · (B) 200 µT · (C) 2000 µT · (D) 0.2 µT

**35.** *Numeric entry.* An air-core solenoid 10 cm long has 500 turns of cross-sectional area 1 cm². Using the long-solenoid formula, what is its inductance, in µH?

**36.** The flux through a 50-turn coil changes by 0.5 mWb in 1 ms. The magnitude of the average induced emf is:
(A) 0.025 V · (B) 0.5 V · (C) 25 V · (D) 50 V

**37.** *Numeric entry.* What is the photon energy, in eV, of light with a wavelength of 1550 nm?

**38.** Which of these materials can absorb (and so detect) 1550 nm light by band-to-band transitions?
(A) Si ($E_g$ = 1.12 eV) · (B) GaAs (1.42 eV) · (C) Ge (0.66 eV) · (D) GaN (3.4 eV)

**39.** *Numeric entry.* Silicon is doped n-type with $N_D = 10^{16}$ cm⁻³, all ionized, and electron mobility 1350 cm²/(V·s). Neglecting holes, what is its resistivity, in Ω·cm?

**40.** The skin depth of copper ($\rho = 1.72\times10^{-8}$ Ω·m, $\mu_r = 1$) at 1 MHz is:
(A) 6.6 µm · (B) 66 µm · (C) 660 µm · (D) 2100 µm

## Block 4 · Software engineering and computing (questions 41–50)

**41.** In 8-bit two's complement, −45 is:
(A) 0x2D · (B) 0xAD · (C) 0xD2 · (D) 0xD3

**42.** *Numeric entry.* Convert the hexadecimal number 0x3FF to decimal.

**43.** The running time of the following, as a function of $n$, is:

```python
# not run
for i in range(n):
    for j in range(i):
        work()
```

(A) O(n) · (B) O(n log n) · (C) O(n²) · (D) O(2ⁿ)

**44.** *Numeric entry.* What is the maximum number of comparisons (each a three-way less/equal/greater test) binary search needs to find a key among 1,000,000 sorted items?

**45.** Bytes arrive in an interrupt handler and are processed later, in arrival order, by the main loop. The most suitable data structure is:
(A) a stack · (B) a queue implemented as a ring buffer · (C) a binary search tree · (D) a hash table

**46.** *Numeric entry.* In Python, what is `-17 % 5`?

**47.** In C, the expression `7 / 2 * 2.0` evaluates to:
(A) 6.0 · (B) 7.0 · (C) 3.5 · (D) 8.0

**48.** *Numeric entry.* A recursive function is defined by $f(0) = 0$ and $f(n) = f(n - 1) + 2n$ for $n \ge 1$. What is $f(5)$?

**49.** Which sorting algorithm is stable and has $O(n\log n)$ worst-case running time?
(A) quicksort · (B) heapsort · (C) merge sort · (D) selection sort

**50.** *Numeric entry.* What is the cyclomatic complexity of this function? Count each `and` and `or` as a decision.

```python
# not run
def f(x):
    if x < 0:
        x = -x
    while x > 10:
        x = x // 2
    if x % 2 == 0 and x > 4:
        return 1
    return 0
```
