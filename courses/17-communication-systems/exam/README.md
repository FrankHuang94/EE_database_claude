# Course 17 · Final Exam (Communication Systems)

**Time limit:** 240 minutes.
**Allowed:** a scientific calculator with the normal distribution, and the [Course 17 equation sheet](../../../reference/equation-sheets/17-communication-systems.md) printed without its chapter links. No notes, no Python, no simulator.

**Instructions.**

- Answer all 14 questions and show every step.
- Question 1 [A] is worth 8 points (2 per part), each [B] 8 (2 per part), and Questions 13 and 14 [C] 12 each (Question 13: 4 per part; Question 14: 3 per part): 120 points in total. 84 or more (70%) is a strong pass.
- Give numerical answers to 3–4 significant figures, with units.
- Question 13 asks for derivations; Question 14 is a diligence question, partly graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These are the conventions of the chapters' problem sets.

- $Q(x) = 1 - \Phi(x) = \tfrac12\operatorname{erfc}(x/\sqrt2)$, the tail of the standard normal distribution.
- White noise has two-sided PSD $N_0/2$; $kT_0$ = −174 dBm/Hz ($T_0$ = 290 K); $c = 2.998 \times 10^8$ m/s.
- Energies and powers of voltage waveforms are into 1 Ω (V²·s and V²).
- Raised-cosine pulses with roll-off α occupy $(1 + \alpha)R_s/2$ at baseband and $(1 + \alpha)R_s$ around a carrier.
- $\bar\gamma$ is the average SNR per branch; "Rayleigh" means $|h|^2$ is exponential with mean 1.
- Ethernet on the wire adds an 8-byte preamble and SFD, a 14-byte header, a 4-byte FCS and a 12-byte inter-frame gap, and pads its payload to at least 46 bytes; IPv4 and TCP headers are 20 bytes each, UDP 8.

---

**1 [A] · Random processes.** (17-01)
(a) $X(t) = A\cos(2\pi f_0t + \Theta)$ with $A$ = 2 V, $f_0$ = 1 kHz and Θ uniform on $[0, 2\pi)$. Find its mean and autocorrelation $R_X(\tau)$. Is it wide-sense stationary?
(b) Give its average power and its PSD.
(c) White noise with $N_0/2 = 10^{-8}$ V²/Hz drives a one-pole RC low-pass filter with unit DC gain and $f_{3\text{dB}}$ = 10 kHz. Find the filter's noise bandwidth, and the output noise variance and rms value.
(d) Find the correlation coefficient between output samples taken 20 µs apart, and the smallest spacing for which it falls below 0.1.

**2 [B] · A receiver front end.** (17-02)
A receiver's antenna sees a 290 K environment. The chain is an LNA (gain 15 dB, NF 1.5 dB), a mixer (conversion loss 8 dB, NF 8 dB) and an IF amplifier (gain 30 dB, NF 4 dB).
(a) Find the cascade noise factor and noise figure, and say which stage contributes most after the LNA.
(b) Give the cascade's equivalent noise temperature.
(c) A filter with 2 dB of loss, at 290 K, is moved in front of the LNA. What is the new noise figure?
(d) Without the filter, find the sensitivity for a 20 MHz noise bandwidth and a required SNR of 10 dB. If the link carries 40 Mb/s, what $E_b/N_0$ does that SNR correspond to?

**3 [B] · Analog modulation.** (17-03)
A wireless microphone uses FM with a peak deviation of 40 kHz and audio bandwidth $W$ = 10 kHz.
(a) Find the deviation ratio and the Carson bandwidth.
(b) A 10 kHz test tone at full deviation gives β = 4, with $J_0(4) = -0.3971$, $J_1 = -0.0660$, $J_2 = 0.3641$, $J_3 = 0.4302$, $J_4 = 0.2811$, $J_5 = 0.1321$. What fraction of the power is in the carrier, and what fraction lies inside the Carson band?
(c) Above threshold, by how much does FM's output SNR for that tone exceed DSB's at the same received power and noise density? What bandwidth does each use?
(d) An AM transmitter is modulated by a tone to index 0.5. Find its power efficiency and its output-SNR penalty against DSB with an envelope detector above threshold.

**4 [B] · A 56 Gb/s link.** (17-04)
A chip-to-chip link carries 56 Gb/s over a channel modelled as one pole at 12 GHz, sampled at the end of each symbol.
(a) Give the symbol rate and Nyquist frequency of NRZ and of PAM4.
(b) What baseband bandwidth would PAM4 occupy with raised-cosine pulses of α = 0.3?
(c) Find τ and $r = e^{-T/\tau}$ for each format, and the worst-case eye opening of each as a fraction of NRZ's ideal (ISI-free) eye. Which format is better on this channel?
(d) At equal peak amplitude, what SNR penalty does PAM4's eye carry without ISI, and why?

**5 [B] · Matched filtering and detection.** (17-05)
A rectangular pulse of amplitude 2 mV and duration $T$ = 0.5 µs arrives in white noise with $N_0/2 = 10^{-14}$ V²/Hz.
(a) Find the pulse energy and the matched filter's peak output SNR (ratio and dB).
(b) An RC low-pass filter with τ = 2T replaces the matched filter and is sampled at $t = T$. Its output signal is $A(1 - e^{-T/\tau})$ and its output noise variance $N_0/(4\tau)$. Find its SNR and its loss against the matched filter.
(c) At $E_b/N_0$ = 9 dB, find the bit-error probabilities of antipodal and of orthogonal binary signalling.
(d) Antipodal symbols ±1 are received in noise with $N_0$ = 0.8, and +1 is sent with probability 0.7. Find the MAP threshold, the MAP error probability and the ML error probability.

**6 [B] · Bandpass modulation.** (17-06)
(a) QPSK runs at 25 Msymbol/s with root-raised-cosine pulses, α = 0.2. Give the bit rate, occupied bandwidth and spectral efficiency, and the BER at $E_b/N_0$ = 7 dB.
(b) For Gray-coded 16-QAM at $E_b/N_0$ = 14 dB, find the symbol-error probability and the approximate BER.
(c) What SNRs correspond to transmitter EVMs of 4.5% and 8%, if the impairments are noise-like?
(d) A transmitter with 5% EVM feeds a channel whose own SNR is 25 dB. What is the effective SNR at the receiver?

**7 [B] · Information theory.** (17-07)
(a) A source emits five symbols with probabilities 0.35, 0.25, 0.20, 0.12 and 0.08. Find its entropy, a Huffman code and its average length, and the code's efficiency.
(b) Find the capacity of a binary symmetric channel with crossover probability 0.05.
(c) Find the Shannon capacity of a 10 MHz AWGN channel at 15 dB SNR.
(d) What is the minimum $E_b/N_0$ for reliable communication at 3 b/s/Hz, and as the spectral efficiency tends to zero?

**8 [B] · Channel coding.** (17-08)
(a) The (7,4) Hamming code is used on a binary symmetric channel with $p$ = 0.01 and decodes single errors. Give its rate, $d_{min}$ and $t$, and compare its block-error probability with the probability that four uncoded bits contain an error.
(b) A 16-bit CRC protects a packet. Which error bursts does it always detect, and roughly what fraction of random error patterns escapes it?
(c) A rate-1/2, K = 9 convolutional code has $d_{free}$ = 12. Give its asymptotic soft-decision coding gain, and the approximate gain with hard decisions.
(d) The Reed–Solomon code RS(255,223) over GF($2^8$) (8-bit symbols) protects a storage or broadcast link. How many symbol errors does it correct, what is its overhead, and what is the longest bit burst it always corrects?

**9 [B] · Wireless channels.** (17-09)
(a) Find the free-space path loss at 915 MHz over 300 m, and the received power from a 20 dBm transmitter with 0 dBi antennas.
(b) With antennas at 10 m and 1.5 m, find the two-ray breakpoint at 2.4 GHz and the path loss at 2 km beyond it.
(c) A user moves at 90 km/h on a 2.6 GHz carrier. Find the maximum Doppler shift and the coherence time (0.5 correlation). Is the channel slow or fast over a 0.5 ms slot? (If your calculator evaluates $J_0$, also give the correlation across the slot.)
(d) Find the average BER of coherent BPSK in Rayleigh fading at $\bar\gamma$ = 25 dB, with one antenna and with two-branch MRC (exact, from the equation sheet's $L$-branch formula, and the high-SNR approximation).

**10 [B] · OFDM and MIMO.** (17-10, 17-11)
(a) For NR's 15 kHz numerology with the normal cyclic prefix (144/2048 of the useful symbol), find the useful symbol and CP durations, the CP overhead and the longest excess path length the CP absorbs.
(b) A 2.6 GHz receiver with 30 kHz spacing has an uncorrected oscillator error of 0.2 ppm. Find the normalized frequency offset ε and the approximate ICI power.
(c) Find the capacity of the 2×2 channel $\mathbf H = \begin{pmatrix}1 & 0.5\\ 0.5 & 1\end{pmatrix}$ at a total SNR of 20 dB with equal power per antenna and no transmitter channel knowledge, and compare with a SISO channel of unit gain.
(d) A channel has $|h_1|^2$ = 1.2 and $|h_2|^2$ = 0.6, and $E_s/N_0$ = 10 dB. Compare the SNR of 1×2 MRC with that of 2×1 Alamouti coding.

**11 [B] · Multiple access and cellular systems.** (17-12)
(a) Find the throughput of slotted and of pure ALOHA at an offered load of $G$ = 0.75.
(b) Find the blocking probability of 8 channels offered 3 Erlangs, and the number of channels needed to carry 10 Erlangs at 1% blocking.
(c) With six first-tier interferers and a path-loss exponent of 3.5, what is the smallest valid hexagonal cluster size that gives at least 10 dB SIR at the cell edge?
(d) HARQ retransmits a block, with at most three attempts, and independent attempts each fail with probability 0.2. Give the throughput relative to one attempt per block, the mean number of transmissions, and the residual failure probability.

**12 [B] · Networks.** (17-13)
(a) Find the wire efficiency of a 200-byte UDP payload over IPv4 and Ethernet.
(b) 172.16.0.0/20 is to be split into equal subnets of at least 100 hosts each. Which prefix, how many hosts and how many subnets?
(c) A TCP receiver offers 65 535 bytes without window scaling on an 80 ms path. Find the throughput limit, the window needed to fill 2.5 Gb/s, and the smallest RFC 7323 shift count that allows it.
(d) Routers P, Q, R, S and T are joined by links of cost P–Q 3, P–R 1, Q–R 1, Q–S 2, R–S 6, R–T 5 and S–T 1. Run Dijkstra's algorithm from P: give each router's distance and P's shortest path to T. Which router does P forward T-bound packets to?

**13 [C] · Derivations.** (17-05, 17-07, 17-10)
(a) Derive the matched filter: show that the filter maximizing the output SNR of a known pulse $s(t)$ in white noise at $t = T$ is $h(t) = ks(T - t)$, and that the maximum SNR is $2E/N_0$.
(b) From the Shannon–Hartley formula, derive the minimum $E_b/N_0$ at spectral efficiency η, and show that it tends to $\ln 2$ (−1.59 dB) as η → 0.
(c) Show that a cyclic prefix of at least $L - 1$ samples on an $L$-tap channel makes the received block, after the prefix is removed, the circular convolution of the transmitted block with the channel, so that $Y[k] = H[k]X[k]$ on every subcarrier.

**14 [C] · Diligence.** (17-02, 17-07, 17-09)
An IoT start-up pitches a sub-GHz radio at 868 MHz: "1 Mb/s at −137 dBm sensitivity, 20 km range from a 14 dBm transmitter, one antenna." Assume a 6 dB noise figure and 0 dBi antennas.
(a) What $E_b/N_0$ does −137 dBm imply at 1 Mb/s? Compare it with the Shannon limit.
(b) What is the highest bit rate −137 dBm can support at the Shannon limit, and at a practical $E_b/N_0$ of 5 dB?
(c) The link budget is 14 dBm − (−137 dBm) = 151 dB. Find the range in free space, and for the two-ray model with antennas at 15 m and 1 m, with and without a 10 dB fade margin. Then find the two-ray range at 1 Mb/s with $E_b/N_0$ = 5 dB.
(d) List the questions you would ask the founders, and what answers would make the claims consistent.
