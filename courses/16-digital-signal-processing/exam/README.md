# Course 16 · Final Exam (Digital Signal Processing)

**Time limit:** 210 minutes.
**Allowed:** a scientific calculator, and the [Course 16 equation sheet](../../../reference/equation-sheets/16-digital-signal-processing.md) printed without its chapter links. No notes, no Python, no simulator.

**Instructions.**

- Answer all 14 questions and show every step.
- Question 1 [A] is worth 8 points (2 per part), each [B] 8 (2 per part), and Questions 13 and 14 [C] 12 each (Question 13: 4 per part; Question 14: 3 per part): 120 points in total. 84 or more (70%) is a strong pass.
- Give numerical answers to 3–4 significant figures, with units.
- Question 13 asks for derivations; Question 14 is a diligence question, partly graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These are the conventions of the chapters' problem sets.

- $\omega$ is in rad/sample; $\omega = 2\pi f/f_s$.
- $W_N = e^{-j2\pi/N}$; "non-trivial" twiddles exclude $W = 1$ and $W = -j$.
- Ripple "peak to peak" means $20\log_{10}((1 + \delta_p)/(1 - \delta_p))$; $A_s = -20\log_{10}\delta_s$.
- An $N$-bit quantizer covers ±1 with $\Delta = 2^{1-N}$; "LSB" is $\Delta$.
- Kaiser's formulas: $\beta = 0.5842(A - 21)^{0.4} + 0.07886(A - 21)$ for $21 \le A \le 50$, $\beta = 0.1102(A - 8.7)$ above 50; $M = (A - 8)/(2.285\Delta\omega)$. Equiripple order: $M \approx (-10\log_{10}(\delta_p\delta_s) - 13)/(2.324\Delta\omega)$.

---

**1 [A] · Discrete-time basics.** (16-01)
A system samples at $f_s$ = 8 kHz.
(a) A 9 kHz tone is sampled without filtering. At what frequency does it appear?
(b) Give the digital frequency of a 1 kHz tone.
(c) Find the gain of the 4-point moving average $y[n] = \tfrac14\sum_{k=0}^{3}x[n - k]$ at DC, 1 kHz and 2 kHz.
(d) Is $y[n] = 0.5y[n - 1] + x[n]$ stable? After how many samples does its impulse response fall by a factor of $e$?

**2 [B] · A notch filter.** (16-02)
A 60 Hz notch for a 1 kHz sensor stream has zeros at $e^{\pm j\theta}$ and poles at $0.99e^{\pm j\theta}$, $\theta = 2\pi \times 60/1000$.
(a) Write $H(z)$ with numerical coefficients.
(b) Estimate the notch's −3 dB width in hertz.
(c) Estimate the time constant of its transient, in samples and seconds.
(d) Its DC gain is not exactly 1. Compute it and say how to normalize.

**3 [B] · The DFT.** (16-03)
(a) Compute the 8-point DFT of $x = (1, 1, 0, 0, 0, 0, 0, 0)$ at $k$ = 0, 2 and 4, and $\lvert X[1]\rvert$.
(b) Give the bin spacing of a 1024-point DFT at 48 kHz.
(c) Linear convolution of a 129-tap filter with long data uses 1024-point FFTs with overlap-save. How many valid outputs does each block give?
(d) With the cost model $4(N\log_2N + N)/(N - M + 1)$ real multiplications per output (16-03), compare the fast convolution with direct filtering.

**4 [B] · The FFT.** (16-04)
(a) For a 4096-point radix-2 FFT, give the number of stages, butterflies and non-trivial twiddle multiplications.
(b) By what factor does the FFT reduce complex multiplications relative to a direct DFT ($N^2$)?
(c) Compute the 4-point DFT of $x = (1, 2, 0, -1)$ with the radix-2 decimation-in-time butterflies, showing $G$ and $H$.
(d) Why does a fixed-point FFT scale by 1/2 at each stage, and what does it cost?

**5 [B] · An ADC test.** (16-05)
An ADC samples at 100 MS/s; the test uses $N$ = 8192 points.
(a) Choose the coherent bin nearest 10 MHz that is relatively prime to $N$, and give the exact input frequency.
(b) A test at −1 dBFS gives SINAD = 70.0 dB. Give the ENOB as measured and referred to full scale.
(c) Find the processing gain (in dB) of an 8192-point FFT with a Hann window (ENBW 1.5 bins).
(d) If the converter's SNR is 72 dB, how far below the tone does the Hann-windowed noise floor sit?

**6 [B] · FIR design.** (16-06)
A low-pass filter at 48 kHz needs a 1 kHz transition, 0.1 dB peak-to-peak passband ripple and 50 dB attenuation.
(a) Which tolerance governs a Kaiser design? Compute $\beta$ and the order.
(b) Estimate the order of an equiripple design.
(c) Give the delay of the Kaiser design (round the order up) in samples and milliseconds.
(d) How many multipliers does the Kaiser design need with symmetry folding?

**7 [B] · IIR design.** (16-07)
A digital low-pass filter at $f_s$ = 8 kHz needs at most 1 dB loss to 1 kHz and 40 dB attenuation from 2 kHz.
(a) Prewarp the edges and give their ratio and the discrimination $D$.
(b) Find the minimum Butterworth and Chebyshev I orders.
(c) The elliptic order bound evaluates to 3.0012. What order do you use, and why does this case deserve care?
(d) Why must the edges be prewarped, and what would go wrong otherwise?

**8 [B] · Structures.** (16-08)
A biquad has denominator $A(z) = 1 - 1.2z^{-1} + 0.81z^{-2}$.
(a) Find its pole radius and angle.
(b) Find its reflection coefficients and decide stability.
(c) In Direct Form II, how much larger can the internal state be than a unit sinusoidal input? (The peak of $\lvert 1/A\rvert$ is at the pole angle, approximately.)
(d) Compare the delay registers of DF I and DF II for this section, and say which you would choose for 16-bit fixed point and why.

**9 [B] · Multirate.** (16-09)
A 192 kHz stream is decimated by 4 to 48 kHz.
(a) Without a filter, where do components at 30 kHz and 50 kHz land?
(b) A 64-tap decimation filter is used. Compare the multiplications per second of direct and polyphase implementations.
(c) A three-stage CIC decimates by 8 elsewhere in the chain. Give its DC gain and register growth.
(d) Why are the CIC's integrators allowed to overflow?

**10 [B] · Quantization.** (16-10)
(a) Give the full-scale-sine SQNR of a 14-bit quantizer.
(b) Find the noise gain of $1/(1 - 0.95z^{-1})$, as a ratio and in dB.
(c) Find the dead band of $y[n] = Q(0.9y[n - 1])$ with rounding.
(d) Why must recursive filters saturate rather than wrap around on overflow?

**11 [B] · Hardware.** (16-11)
(a) Size the product and accumulator of an 18 × 18-bit MAC summing 512 terms.
(b) A 256-tap symmetric FIR filter runs at 200 MS/s on DSP blocks clocked at 600 MHz. How many blocks are needed with folding?
(c) A first-order recursion uses a 1.5 ns multiplier and a 0.5 ns adder. Give its iteration bound, and the bound after look-ahead by 2.
(d) How many CORDIC iterations bring the residual angle below $2^{-10}$ rad?

**12 [B] · FIR versus IIR.** (16-06, 16-07)
For the specification of Question 7 (taking the 1 dB as peak-to-peak ripple for the FIR), the order-4 elliptic filter and the shortest equiripple FIR filter, which has 15 taps, both meet the mask.
(a) Count multiplications per output for each (the elliptic filter as two biquads whose second section has $b_0 = b_2 = 1$; the FIR folded).
(b) The elliptic filter's group delay rises from 2.69 samples at DC to a peak of 14.96 samples just below the 1 kHz edge. Give the FIR's delay and compare.
(c) Why is the FIR competitive here when it lost by a factor of 4.9 in 16-07's audio example?
(d) Name one reason to prefer each filter for this specification.

**13 [C] · Derivations.** (16-06, 16-09, 16-10)
(a) Derive $\text{SQNR} = 6.02N + 1.76$ dB for a full-scale sine on an $N$-bit quantizer, stating the noise model.
(b) Show that a symmetric FIR filter of even length (type II) has $A(\pi) = 0$.
(c) Prove the decimation noble identity: $H(z^M)$ followed by $\downarrow M$ equals $\downarrow M$ followed by $H(z)$.

**14 [C] · Diligence.** (16-06, 16-10, 16-11)
A start-up pitches an "audio DSP block: 128-tap linear-phase FIR at 48 kHz, 120 dB SNR, 4 µW, 0.1 ms latency".
(a) Compute the energy per MAC the claim implies, and compare it with the 45 nm figure for a 32-bit integer MAC (3.2 pJ, 16-11).
(b) How many bits does 120 dB of SQNR require?
(c) Compute the latency of a 128-tap linear-phase FIR at 48 kHz and compare it with the claim.
(d) List the questions you would ask the founders, and what answers would make the claims consistent.
