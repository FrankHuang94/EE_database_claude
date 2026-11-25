# Solutions 23-08 · Emerging Memories: MRAM, ReRAM, PCM, FeRAM

Problems: [23-08 problems](../problems/23-08-problems.md) · Chapter: [23-08](../chapters/23-08-emerging-memories.md)

Every number is recomputed by [verify_23_08.py](../verify/verify_23_08.py).

---

## Solutions

### Solution 23-08.1

(a) $3 \times (1 + 2)$ = **9** kΩ.

(b) $0.1/(3 + 1.5)\ \text{k}\Omega$ = **22.2** µA; (c) $0.1/(9 + 1.5)\ \text{k}\Omega$ = **9.52** µA.

(d) $22.22/9.524 - 1$ = **133** %. The 200% TMR shrinks to a 133% contrast once the series resistance is included.

### Solution 23-08.2

(a) $\tau = e^{50}/10^9$ = **5.18** × 10¹² s; (b) = **1.64** × 10⁵ years.

(c) $2^{26} \times 3.156 \times 10^8 \times 10^9 \times e^{-50}$ = **4085** flips.

Each bit is stable for over a hundred thousand years, yet a 64 Mib array loses thousands of bits in a decade. Array statistics, not single-bit lifetimes, set the design: this array needs a higher $\Delta$ or ECC.

### Solution 23-08.3

(a) $75 \times 298.15/398.15$ = **56.2**.

(b) $\ln(2^{24} \times 3.156 \times 10^8 \times 10^9)$ = **56.9**.

(c) $e^{56.93 - 56.16}$ = **2.15** flips: just over the target, so the array fails it narrowly. Passing needs $56.93 \times 398.15/298.15$ = **76.02** at 25 °C, so 76 is not quite enough; specify 77 for margin.

### Solution 23-08.4

(a) $I = 1.3 \times 0.8 \times 45$ = **46.8** µA; $E = 0.6 \times 46.8\ \mu\text{A} \times 10\ \text{ns}$ = **0.281** pJ.

(b) $I$ = **72.8** µA; $E$ = **0.437** pJ.

(c) $e^{70 - 45} = e^{25}$ = **7.20** × 10¹⁰.

A 56% increase in write energy buys a retention improvement of more than ten orders of magnitude.

### Solution 23-08.5

(a) $600\ \text{K}/5\ \text{K/µW}$ = **120** µW; (b) $\sqrt{120\ \mu\text{W}/3\ \text{k}\Omega}$ = **200** µA.

(c) $120\ \mu\text{W} \times 30\ \text{ns}$ = **3.6** pJ.

(d) $1.5\ \text{ns} \times \ln(600/150)$ = **2.08** ns.

(e) $600 \times (1 - e^{-3/1.5})$ = **519** K. A pulse only twice the thermal time constant stops short of melting. RESET pulses must last several time constants.

### Solution 23-08.6

(a) $t = 1.5^{1/0.05} = 1.5^{20}$ = **3325** s, about **55** minutes.

(b) $1.5^{10}$ = **57.7** s.

(c) $(3.156 \times 10^8)^{0.05}$ = **2.66**.

Halving the exponent stretches the time to a given drift by the power of 2 (from 58 s to 3,325 s, a factor of 57.7), but a 1.5× level spacing is still crossed within an hour.

### Solution 23-08.7

(a) $G = 1/6.45\ \text{k}\Omega$; $G/G_0$ = **2.00** quanta.

(b) $1/G_0$ = **12.9** kΩ; (c) $1/(3G_0)$ = **4.30** kΩ.

### Solution 23-08.8

(a) $2 \times 15\ \mu\text{C/cm}^2 \times (6 \times 10^{-6}\ \text{cm})^2$ = **1.08** fC.

(b) $1.08\ \text{fC}/20\ \text{fF}$ = **54.0** mV.

(c) $0.5 \times 10/(10 + 20)$ = **167** mV.

(d) $P_r = \dfrac{0.1667 \times 20\ \text{fF}}{2 \times 3.6 \times 10^{-11}\ \text{cm}^2}$ = **46.3** µC/cm².

Scaled FeRAM cells give less signal than a DRAM cell of similar size, unless the ferroelectric has a large polarization or the capacitor is made three-dimensional.

### Solution 23-08.9

(a) $2 \times 1.2 \times 10^8\ \text{V/m} \times 8 \times 10^{-9}\ \text{m}$ = **1.92** V.

(b) $t_{FE} = 3/(2 \times 10^8)$ m = **15** nm.

### Solution 23-08.10

(a) $15 \times 365.25 \times 86{,}400$ = **4.73** × 10⁸ writes.

(b) $10^5$ s = **27.8** hours.

(c) $4.734 \times 10^8/10^5$ = **4734** locations; (d) $/10^4$ = **47336**; (e) $/10^6$ = **473**.

Endurance matters for logging and frequently updated parameters. ReRAM rated at 10,000 cycles needs wear leveling over a large region; one-million-cycle MRAM needs far less.

### Solution 23-08.11

(a) $50 \times (0.028\ \mu\text{m})^2$ = **0.0392** µm².

(b) $32 \times 2^{20} \times 0.0392\ \mu\text{m}^2$ = **1.32** mm².

(c) $1.315/0.5$ = **2.63** mm².

(d) $32 \times 2^{20} \times 0.127/0.5\ \mu\text{m}^2$ = **8.52** mm².

On area alone, the MRAM macro is about a third the size of the SRAM one, and it is nonvolatile. SRAM remains faster to write and has unlimited endurance, so the two serve different roles.

### Solution 23-08.12

(a) $16{,}384\ \text{Mb}/9.75\ \text{Mb/mm}^2$ = **1680** mm².

(b) $1680/858$ = **1.96**.

A 16 Gb MRAM die at today's standalone density would need about twice the largest area a lithography scanner can expose. A 16 Gb DDR5 die is 66.26 mm² (23-03), so MRAM would need about **25** times today's density to match it: replacing DRAM needs a new cell, not just better devices.

### Solution 23-08.13

(a) $8 \times 2^{20}$ = **8388608** bits/s.

(b) $8.389 \times 10^6 \times 0.7\ \text{pJ}$ = **5.87** µW; (c) **33.6** µW; (d) **839** µW.

MRAM and PCM fit a 50 µW budget; NOR flash, at about 17 times the budget, does not. (NOR flash would also wear out quickly at this write rate.)

### Solution 23-08.14

(a) In steady precession, damping removes angular momentum at $\alpha\omega m/\gamma = \alpha(\gamma\mu_0H_k)(M_sV)/\gamma = \alpha\mu_0H_kM_sV$ per second. A current $I$ carries $I/q$ electrons per second, each delivering $\eta\hbar/2$, so it supplies $\eta\hbar I/(2q)$. Switching begins when the supply equals the loss:

$$
I_{c0} = \frac{2q\alpha}{\hbar\eta}\mu_0H_kM_sV = \frac{4q\alpha}{\hbar\eta}\cdot\frac{\mu_0M_sH_kV}{2} = \frac{4q\alpha}{\hbar\eta}E_b .
$$

Units: $\mu_0H_kM_sV$ is T × (A/m) × m³ = J, and C/(J·s) × J = C/s = A. ✓

(b) With $E_b = \Delta kT$, $I_{c0}/\Delta = 4 \times 1.602 \times 10^{-19} \times 0.008 \times 4.143 \times 10^{-21}/(1.0546 \times 10^{-34} \times 0.6)$ = **0.336** µA.

(c) $50 \times 0.3356$ = **16.8** µA.

(d) $\Delta_{eff} = 50 \times 0.7$ = **35**. The flip probability is $1 - \exp(-f_0te^{-35}) \approx 10^9 \times 5 \times 10^{-9} \times e^{-35}$ = **3.15** × 10⁻¹⁵.

(e) $1/3.15 \times 10^{-15}$ = **3.17** × 10¹⁴ reads, enough for a bit read once per microsecond for about ten years.

(f) $5e^{-\Delta_{eff}} \le 10^{-18}$ needs $\Delta_{eff} \ge \ln(5 \times 10^{18})$ = **43.06**, so $I/I_{c0} \le 1 - 43.06/50$ = **13.9** %.

The read current that sensing wants is the current that read disturb forbids: a 30% read is safe for this $\Delta$ = 50 cell, but the same fraction would ruin a cache-like cell with $\Delta$ = 30, whose effective barrier would fall to 21.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 23-08.1a | antiparallel resistance | 9 | kΩ |
| 23-08.1b | parallel current | 22.2 | µA |
| 23-08.1b1 | parallel current, 4 s.f. | 22.22 | µA |
| 23-08.1c | antiparallel current | 9.52 | µA |
| 23-08.1c1 | antiparallel current, 4 s.f. | 9.524 | µA |
| 23-08.1d | effective contrast | 133 | % |
| 23-08.2a | retention time | 5.18e12 | s |
| 23-08.2b | retention time | 1.64e5 | years |
| 23-08.2c | expected flips in 10 years | 4085 | |
| 23-08.3a | Delta at 125 °C | 56.2 | |
| 23-08.3a1 | Delta at 125 °C, 4 s.f. | 56.16 | |
| 23-08.3b | required Delta | 56.9 | |
| 23-08.3b1 | required Delta, 4 s.f. | 56.93 | |
| 23-08.3c | expected flips | 2.15 | |
| 23-08.3d | room-temperature Delta that passes | 76.02 | |
| 23-08.4a0 | write current, Delta 45 | 46.8 | µA |
| 23-08.4a | write energy, Delta 45 | 0.281 | pJ |
| 23-08.4b0 | write current, Delta 70 | 72.8 | µA |
| 23-08.4b | write energy, Delta 70 | 0.437 | pJ |
| 23-08.4c | retention ratio | 7.20e10 | |
| 23-08.4d | write-energy increase | 56 | % |
| 23-08.5a | RESET power | 120 | µW |
| 23-08.5b | RESET current | 200 | µA |
| 23-08.5c | RESET energy | 3.6 | pJ |
| 23-08.5d | cooling time | 2.08 | ns |
| 23-08.5e | peak rise of a 3 ns pulse | 519 | K |
| 23-08.6a | time to drift 1.5x, nu 0.05 | 3325 | s |
| 23-08.6a1 | time to drift 1.5x, nu 0.05 | 55 | min |
| 23-08.6b | time to drift 1.5x, nu 0.1 | 57.7 | s |
| 23-08.6b1 | time to drift 1.5x, nu 0.1, rounded | 58 | s |
| 23-08.6c | 10-year drift factor, nu 0.05 | 2.66 | |
| 23-08.7a | quanta in 6.45 kΩ | 2.00 | |
| 23-08.7b | one quantum | 12.9 | kΩ |
| 23-08.7c | three quanta | 4.30 | kΩ |
| 23-08.8a | switched charge | 1.08 | fC |
| 23-08.8b | FeRAM signal | 54.0 | mV |
| 23-08.8c | DRAM signal | 167 | mV |
| 23-08.8c1 | DRAM signal in volts, 4 s.f. | 0.1667 | V |
| 23-08.8d | polarization to match | 46.3 | µC/cm² |
| 23-08.8d0 | capacitor area | 3.6e-11 | cm² |
| 23-08.9a | FeFET window | 1.92 | V |
| 23-08.9b | thickness for 3 V | 15 | nm |
| 23-08.10a | writes in 15 years | 4.73e8 | |
| 23-08.10a1 | writes in 15 years, 4 s.f. | 4.734e8 | |
| 23-08.10b | NOR lifetime without leveling | 27.8 | h |
| 23-08.10c | locations for NOR | 4734 | |
| 23-08.10d | locations for ReRAM | 47336 | |
| 23-08.10e | locations for MRAM | 473 | |
| 23-08.11a | cell area | 0.0392 | µm² |
| 23-08.11b | total cell area | 1.32 | mm² |
| 23-08.11b1 | total cell area, 4 s.f. | 1.315 | mm² |
| 23-08.11c | MRAM macro area | 2.63 | mm² |
| 23-08.11d | SRAM macro area | 8.52 | mm² |
| 23-08.11e | MRAM-to-SRAM area ratio | 0.31 | |
| 23-08.12a | 16 Gb MRAM die area | 1680 | mm² |
| 23-08.12b | ratio to reticle field | 1.96 | |
| 23-08.12c | reticle field | 858 | mm² |
| 23-08.12d | density gap to a 16 Gb DDR5 die | 25 | |
| 23-08.13a | bits per second | 8388608 | |
| 23-08.13a1 | bits per second, 4 s.f. | 8.389e6 | |
| 23-08.13b | MRAM write power | 5.87 | µW |
| 23-08.13c | PCM write power | 33.6 | µW |
| 23-08.13d | NOR flash write power | 839 | µW |
| 23-08.13e | NOR flash over budget | 17 | |
| 23-08.14b | critical current per unit Delta | 0.336 | µA |
| 23-08.14b1 | kT at 300 K | 4.143e-21 | J |
| 23-08.14c | critical current at Delta 50 | 16.8 | µA |
| 23-08.14d0 | effective barrier at 30% read | 35 | |
| 23-08.14d | flip probability per read | 3.15e-15 | |
| 23-08.14e | reads per flip | 3.17e14 | |
| 23-08.14f0 | effective barrier needed | 43.06 | |
| 23-08.14f | largest read fraction | 13.9 | % |
| 23-08.14g | effective barrier of a Delta 30 cell at 30% read | 21 | |
