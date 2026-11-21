# Term 5 Checkpoint · FE-Style Practice Exam

**Covers:** Courses 15–18 (control systems, digital signal processing, communication systems and networks, embedded systems and microcontrollers). **Questions:** 50 (multiple choice and numeric entry). **Time:** 150 minutes, the FE pace of about 3 minutes per question.
**Materials:** an FE-approved calculator and the *NCEES FE Reference Handbook* only (free PDF from NCEES); no course notes or sheets. Finding formulas in the handbook quickly is part of the practice.
**Scoring:** one point per question. Score each block separately and aim for at least 70% in every block. Write every miss into your error log with its cause, and re-solve it a week later. Solutions with full explanations, each pointing to the chapter to revisit, are in [solutions.md](solutions.md); open them only after you finish.

**Conventions:**

- For numeric entry, give 3 significant figures unless the question says otherwise.
- Control: unity negative feedback unless stated; the 2% settling time is estimated as $4/(\zeta\omega_n)$.
- DSP: $f_s$ is the sampling rate; windows are periodic; Q15 numbers are 16-bit two's complement with 15 fractional bits, products truncated by an arithmetic right shift.
- Communications: $kT_0$ = −174 dBm/Hz at $T_0$ = 290 K, from $k$ = 1.381 × 10⁻²³ J/K; $c$ = 2.998 × 10⁸ m/s; $Q(x)$ is the standard normal tail.
- Embedded: 1 KiB = 1024 bytes; UART frames are 8N1; I²C rise times are measured from 30% to 70% of the supply.

---

## Block 1 · Control systems (questions 1–13)

**1.** *Numeric entry.* A system has $T(s) = \omega_n^2/(s^2 + 2\zeta\omega_ns + \omega_n^2)$ with $\omega_n$ = 10 rad/s and ζ = 0.4. Find its percent overshoot to a step.

**2.** The 2% settling time of the system of question 1 is approximately:
(A) 0.400 s · (B) 1.00 s · (C) 0.343 s · (D) 2.50 s

**3.** *Numeric entry.* With unity feedback around $G(s) = 20/[(s + 1)(s + 4)]$, find the steady-state error to a unit step.

**4.** With unity feedback around $G(s) = 50/[s(s + 5)]$, the steady-state error to a unit ramp is:
(A) 0 · (B) 0.100 · (C) 0.0196 · (D) 10.0

**5.** *Numeric entry.* A closed loop has the characteristic polynomial $s^3 + 6s^2 + 11s + K$. Find the largest $K$ for which it is stable.

**6.** At the largest stable $K$ of question 5, the loop oscillates at:
(A) 3.32 rad/s · (B) 6.00 rad/s · (C) 11.0 rad/s · (D) 8.12 rad/s

**7.** *Numeric entry.* Find the phase margin, in degrees, of $L(s) = 10/[s(s + 1)]$.

**8.** The gain margin of $L(s) = 10/[(s + 1)(s + 2)(s + 3)]$ is:
(A) 15.6 dB · (B) 6.00 dB · (C) 21.6 dB · (D) 9.54 dB

**9.** *Numeric entry.* A lead compensator has its pole 10 times farther from the origin than its zero. Find its maximum phase lead, in degrees.

**10.** The lead compensator $(s + 2)/(s + 20)$ gives its maximum phase at:
(A) 6.32 rad/s · (B) 11.0 rad/s · (C) 20.0 rad/s · (D) 2.00 rad/s

**11.** *Numeric entry.* A system has $\dot{\mathbf x} = A\mathbf x + B u$, $y = C\mathbf x$ with $A = \begin{bmatrix} 0 & 1 \\ -6 & -5 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ and $C = [1\ \ 0]$. Find its DC gain.

**12.** The eigenvalues of the matrix $A$ of question 11 are:
(A) −2 and −3 · (B) 2 and 3 · (C) −1 and −6 · (D) −5 and 0

**13.** *Numeric entry.* $G(s) = 1/(s + 2)$ is discretized with a zero-order hold at $T$ = 0.1 s. Find the pole of the discrete transfer function.

## Block 2 · Digital signal processing (questions 14–26)

**14.** A 7 kHz tone is sampled at 10 kHz without an anti-aliasing filter. It appears at:
(A) 3.00 kHz · (B) 7.00 kHz · (C) 17.0 kHz · (D) 2.00 kHz

**15.** *Numeric entry.* Find the bin spacing, in Hz, of a 1024-point DFT of audio sampled at 44.1 kHz.

**16.** A radix-2 FFT of 1024 points performs how many butterflies?
(A) 5120 · (B) 10240 · (C) 1048576 · (D) 512

**17.** *Numeric entry.* The analysis of question 15 uses a Hann window. Find the null-to-null width of its main lobe, in Hz.

**18.** A linear-phase FIR filter with 41 taps runs at 8 kHz. Its group delay is:
(A) 2.50 ms · (B) 5.13 ms · (C) 20.0 ms · (D) 2.56 ms

**19.** *Numeric entry.* A digital filter at $f_s$ = 8 kHz is designed by the bilinear transform with a cutoff at 1 kHz. Find the prewarped analog cutoff, in kHz.

**20.** The filter $H(z) = 1/(1 - 1.2z^{-1} + 0.5z^{-2})$ is:
(A) stable, with both poles at radius 0.707 · (B) unstable, with a pole at radius 1.2 · (C) stable, with poles at radius 0.500 · (D) marginally stable, with poles on the unit circle

**21.** *Numeric entry.* Find the ideal signal-to-quantization-noise ratio of a 16-bit converter, in dB.

**22.** A signal sampled at 48 kHz is decimated by 4. The anti-aliasing filter must remove content above:
(A) 6.00 kHz · (B) 12.0 kHz · (C) 24.0 kHz · (D) 3.00 kHz

**23.** *Numeric entry.* Find the magnitude of the frequency response of the 3-point moving average $y[n] = (x[n] + x[n-1] + x[n-2])/3$ at $\omega = \pi/2$.

**24.** In Q15, 0.75 × (−0.5) gives the integer:
(A) −12288 · (B) −24576 · (C) 12288 · (D) −6144

**25.** *Numeric entry.* Find the final value of the step response of $H(z) = 0.5/(1 - 0.6z^{-1})$.

**26.** Zero-padding a 256-sample record to a 1024-point DFT:
(A) improves the frequency resolution four times · (B) makes the bin spacing four times finer but does not improve resolution · (C) raises the SNR by 6 dB · (D) removes spectral leakage

## Block 3 · Communications and networks (questions 27–39)

**27.** *Numeric entry.* Find the thermal noise power, in dBm, in a 1 MHz bandwidth at 290 K.

**28.** An LNA (gain 20 dB, noise figure 2 dB) is followed by a mixer with a 10 dB noise figure. The cascade's noise figure is:
(A) 2.24 dB · (B) 12.0 dB · (C) 2.00 dB · (D) 10.0 dB

**29.** *Numeric entry.* Find the Carson bandwidth, in kHz, of FM with 75 kHz peak deviation and 15 kHz audio.

**30.** Pulses at 10 Mbaud with raised-cosine roll-off 0.25 need a baseband bandwidth of:
(A) 6.25 MHz · (B) 5.00 MHz · (C) 12.5 MHz · (D) 10.0 MHz

**31.** *Numeric entry.* Find the bit error rate of coherent BPSK at $E_b/N_0$ = 8 dB.

**32.** The Shannon capacity of a 1 MHz channel at an SNR of 15 is:
(A) 4.00 Mb/s · (B) 15.0 Mb/s · (C) 3.91 Mb/s · (D) 1.00 Mb/s

**33.** *Numeric entry.* Find the free-space path loss, in dB, at 2.4 GHz over 100 m (isotropic antennas).

**34.** A Hamming (7,4) code with syndrome decoding:
(A) corrects any two errors · (B) detects but cannot correct single errors · (C) corrects any single error, and miscorrects double errors · (D) corrects bursts of up to three errors

**35.** *Numeric entry.* An OFDM system has 64 subcarriers across 20 MHz. Find the subcarrier spacing, in kHz.

**36.** A TCP connection with a 64 KiB window and a 50 ms round-trip time can carry at most:
(A) 10.5 Mb/s · (B) 1.31 Mb/s · (C) 83.9 Mb/s · (D) 5.24 Mb/s

**37.** *Numeric entry.* How many hosts can be addressed in the IPv4 subnet 192.168.10.64/26?

**38.** The maximum throughput of slotted ALOHA, in packets per slot, is:
(A) 0.368 · (B) 0.184 · (C) 0.500 · (D) 1.00

**39.** *Numeric entry.* An Ethernet frame carries 1500 bytes of payload. Counting the 8-byte preamble and start delimiter, the 14-byte header, the 4-byte FCS and the 12-byte inter-frame gap, find the percentage of line time that carries payload.

## Block 4 · Embedded systems and software (questions 40–50)

**40.** A microcontroller's flash has a 25 ns access time. At 100 MHz it needs how many wait states?
(A) 2 · (B) 3 · (C) 1 · (D) 0

**41.** *Numeric entry.* How many bytes per second does a 9600-baud UART carry?

**42.** An I²C line has a 2.2 kΩ pull-up and 100 pF of capacitance. Its rise time is:
(A) 186 ns · (B) 220 ns · (C) 506 ns · (D) 152 ns

**43.** *Numeric entry.* Find the LSB, in mV, of a 12-bit ADC with a 3.3 V reference.

**44.** The Liu & Layland rate-monotonic utilization bound for two tasks is:
(A) 0.828 · (B) 0.693 · (C) 1.00 · (D) 0.780

**45.** *Numeric entry.* Three tasks with $(C, T)$ = (2, 5), (2, 10) and (3, 20) ms run under rate-monotonic priorities. Find the worst-case response time of the lowest-priority task, in ms.

**46.** A sensor node draws 20 µA on average from a 230 mAh coin cell. Ignoring self-discharge, it lasts:
(A) 479 days · (B) 958 days · (C) 47.9 days · (D) 240 days

**47.** *Numeric entry.* An ADC streams 100 kS/s into ping-pong DMA buffers. Processing a block of $N$ samples takes $50\ \mu\text{s} + 2\ \mu\text{s} \times N$, and its start can be delayed by up to 30 µs. Find the smallest safe $N$.

**48.** The worst-case number of comparisons for a binary search of 1 000 000 sorted items is:
(A) 20 · (B) 1000 · (C) 500000 · (D) 6

**49.** *Numeric entry.* A 4-digit PIN can be tried once every 3 s. Find the average time, in hours, a brute-force attacker needs.

**50.** The 16-bit pattern 0xFF38, read as a two's-complement integer, is:
(A) −200 · (B) 65336 · (C) −199 · (D) −56
