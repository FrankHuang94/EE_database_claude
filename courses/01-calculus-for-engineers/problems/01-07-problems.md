# Problems 01-07 · Applications of Integration

Chapter: [01-07](../chapters/01-07-applications-of-integration.md) · Worked solutions: [01-07 solutions](../solutions/01-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** peak values are written $X_p$ and RMS values $X_{rms}$; $\varepsilon_0 = 8.854\times10^{-12}$ F/m; answers to 4 significant figures unless stated. Use a calculator or Python freely, but show the integral behind each result.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 01-07.1 [A]

Find the average and RMS values over one period of:

(a) a full-wave rectified sine of 10 V peak;
(b) a half-wave rectified sine of 10 V peak;
(c) a sawtooth rising linearly from 0 to 4 V, then resetting.

(d) Give the crest factors of a sine, a square wave and a triangle wave.

### Problem 01-07.2 [A]

An LED driver applies 5 V pulses with 20% duty cycle across a 10 Ω current-setting resistor.

(a) Find the average and RMS voltage.
(b) Find the power dissipated in the resistor.
(c) What power would a designer wrongly compute from the average voltage?

### Problem 01-07.3 [A]

(a) A solar inverter's DC bus has 470 µF charged to 400 V. How much energy is stored? (This is why such capacitors must be discharged before servicing.)
(b) A 10 µH inductor carries 20 A. How much energy does it store?

### Problem 01-07.4 [A]

(a) Show that a variable uniform on $[-\Delta/2, \Delta/2]$ has mean 0 and variance $\Delta^2/12$. Find the RMS error for $\Delta = 1$ mV.
(b) A component has an exponential lifetime with failure rate $\lambda = 10^{-6}$ per hour. What is the probability that it survives one year (8760 h)?

### Problem 01-07.5 [B]

A switching power supply draws $i(t) = 10\sin\omega t + 3\sin3\omega t + \sin5\omega t$ A.

(a) Find its RMS current.
(b) Find its THD (01-06).
(c) The supply's wiring has 0.1 Ω of resistance. Compare the wiring loss with the loss if only the fundamental flowed.

### Problem 01-07.6 [B]

A load has $v = 325\cos\omega t$ V and $i = 8\cos(\omega t - 45^\circ)$ A.

(a) Compute the average power by integrating $v\cdot i$ over a period.
(b) Find the apparent power and the power factor.
(c) Find the reactive power $Q = V_{rms}I_{rms}\sin\phi$.

### Problem 01-07.7 [B]

A 1 F supercapacitor charged to 5 V backs up a memory controller that draws a constant 0.5 W through a regulator that works down to 2.5 V input.

(a) Find the usable energy.
(b) For a constant-power load, $dE/dt = -P$. Find the hold-up time.
(c) Write $v(t)$ during the discharge. (Hint: $\tfrac{1}{2}Cv^2 = \tfrac{1}{2}CV_1^2 - Pt$.)

### Problem 01-07.8 [B]

**Work and energy in a capacitor.**

(a) How much work moves 1 nC of charge through 5 V? How many eV is 1 J?
(b) A parallel-plate capacitor (plate area 1 cm², vacuum gap) holds a fixed charge $Q = 10$ nC. Find the attractive force between the plates.
(c) Find the work needed to pull the plates from 1 mm to 2 mm apart, by integrating the force. Verify that it equals the increase in stored energy $Q^2/(2C)$.

### Problem 01-07.9 [B]

Resistor values from a production line are Gaussian with mean 10 kΩ and standard deviation 50 Ω.

(a) What fraction lies within ±1% of nominal?
(b) Within ±0.5%?
(c) The process improves to σ = 25 Ω. What fraction now lies within ±0.5%?

### Problem 01-07.10 [B]

A server contains 1000 components, each with a constant failure rate of $2\times10^{-7}$ per hour, any one of which fails the server.

(a) Find the server's failure rate and MTBF.
(b) What is the probability that a server runs 30 days (720 h) without failure?
(c) Using integration by parts, show that the mean of an exponential lifetime is $1/\lambda$.

### Problem 01-07.11 [B]

(a) Find the ideal SNR of a 16-bit and of a 10-bit ADC.
(b) A converter measures SINAD = 70 dB. What is its ENOB?
(c) Oversampling by a factor $K$ spreads the same quantization noise power over $K$ times the bandwidth. After digital filtering to the original band, the in-band noise falls by $10\log_{10}K$ dB. How much SNR does $K = 4$ gain, and what is that in bits?

### Problem 01-07.12 [C]

**Fuse and pulse ratings ($I^2t$).** A fuse blows when $\int i^2\,dt$ exceeds its rating (A²s), and power transistors have similar pulse-energy limits.

(a) A capacitor bank's inrush current is $i(t) = 50e^{-t/\tau}$ A with $\tau = 1$ ms. Find $\int_0^\infty i^2\,dt$.
(b) Find the duration of a rectangular 50 A pulse with the same $I^2t$.
(c) Will a fuse rated at 2 A²s survive the inrush? What about a 1 A²s fuse?

### Problem 01-07.13 [C]

**Battery energy versus capacity.** A Li-ion cell's voltage during discharge is modeled (illustratively) as $V(q) = 4.2 - 0.6\,(q/Q) - 0.3\,(q/Q)^2$ V, where $q$ is the charge removed and $Q = 3000$ mAh.

(a) Find the energy delivered by a full discharge, in Wh.
(b) Find the charge-weighted average voltage. Compare it with the end-point average $(4.2 + 3.3)/2$, and explain the difference.
(c) If the device shuts down at 3.5 V, how much charge and energy are left unused?

### Problem 01-07.14 [C]

**RMS currents in a buck converter.** The inductor current is a DC level $I_0 = 2$ A plus a triangular ripple of 0.6 A peak-to-peak. The high-side switch conducts this current for a fraction $D = 0.3$ of each period.

(a) Show that a triangular ripple of peak-to-peak $\Delta$ contributes $\Delta^2/12$ to the mean square, and find the inductor's RMS current.
(b) Find the conduction loss in an inductor with 20 mΩ winding resistance.
(c) Find the high-side switch's RMS current.

### Problem 01-07.15 [C]

**Noise peaks and meters.** Thermal noise is Gaussian with zero mean and standard deviation σ.

(a) What is the probability that a sample exceeds 3σ in magnitude? 6σ?
(b) Show that the mean of $\lvert x\rvert$ is $\sigma\sqrt{2/\pi}$.
(c) An average-responding meter (calibrated for sines with form factor 1.111) measures this noise. What does it read, as a fraction of the true RMS σ? What is the error in percent?

---

## Objective coverage

| Learning objective (chapter 01-07) | Problems |
|---|---|
| 1. Average, RMS, crest and form factors | 1, 2, 15(c) |
| 2. Average AC power; RMS currents and conduction loss | 5, 6, 12, 14 |
| 3. Stored and usable energy; work | 3, 7, 8, 13 |
| 4. Probability densities: uniform, exponential, Gaussian | 4, 9, 10, 15 |
| 5. ADC SNR and ENOB | 4(a), 11 |
