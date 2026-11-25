# Course 24 · Final Exam (High-Speed I/O, Signal Integrity and Photonics)

**Time limit:** 270 minutes, best taken in two sittings of about 135 minutes: Questions 1–6, then Questions 7–12.
**Allowed:** a scientific calculator and the [Course 24 equation sheet](../../../reference/equation-sheets/24-high-speed-io-signal-integrity-and-photonics.md) printed without its chapter links. No notes, no Python and no simulator.

**Instructions.**

- Answer all 12 questions and show every step.
- Questions 1–10 [B] are worth 8 points each (2 per part), and Questions 11 and 12 [C] 12 each (3 per part): 104 points in total. 73 or more (70%) is a strong pass.
- Give numerical answers to 3 significant figures, with units, unless a part asks otherwise. Bit error rates within ±5% of the key earn full credit.
- Question 11 asks for derivations: results quoted from the equation sheet earn no credit unless derived. Question 12 is a diligence question, partly graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These follow the chapters.

- $c$ = 2.998 × 10⁸ m/s, $h$ = 6.626 × 10⁻³⁴ J·s, $q$ = 1.602 × 10⁻¹⁹ C, $k$ = 1.381 × 10⁻²³ J/K, $T$ = 300 K; 1 Np = 8.686 dB; 1 in = 25.4 mm.
- Dielectric loss is $\alpha_d = \pi f\sqrt{\varepsilon_r}\tan\delta/c$ Np/m; smooth-copper conductor loss is $\alpha_c \approx 36\sqrt{f_{GHz}}/(w_{mil}Z_0)$ dB/in.
- $Q(x)$ is the Gaussian tail probability; for $x \gtrsim 3$, $Q(x) \approx \dfrac{e^{-x^2/2}}{x\sqrt{2\pi}}\left(1 - \dfrac{1}{x^2}\right)$, which you may invert by trial. Useful values: $Q^{-1}(10^{-12})$ = 7.03, $Q^{-1}(10^{-6})$ = 4.75, $Q^{-1}(10^{-15})$ = 7.94, $Q^{-1}(2.4 \times 10^{-4})$ = 3.49.
- PAM4 BER from an eye is $\tfrac34Q(V_{eye}/2\sigma)$. Linear chains add $1/Q^2$; retimed chains add BER. When a question gives a link or chain $Q$ directly (Questions 9, 10, 11 and 12), take its BER as $Q(Q)$ and the KP4 threshold (BER 2.4 × 10⁻⁴) as $Q$ = 3.49. Link margins are electrical: $20\log_{10}(Q/Q_{req})$.
- Optical penalties: $10\log_{10}3$ for PAM4 and $10\log_{10}((ER + 1)/(ER - 1))$ for extinction ratio. Spectral width is $\lambda^2\Delta f/c$ with $\Delta f$ the symbol rate.
- Failure-rate bounds: $\lambda_U = -\ln(0.05)/T$ with no failures, $\chi^2_{0.95,4}/(2T)$ = 4.744/$T$ with one. A year is 8766 h.

---

**1 [B] · Channel loss and reflections.** (24-01)
A 200 GbE lane runs 212.5 Gb/s PAM4.
(a) Find its symbol rate, unit interval and Nyquist frequency.
(b) A 4 mil, 50 Ω stripline has $\varepsilon_r$ = 3.4 and $\tan\delta$ = 0.002. Find the dielectric and conductor loss per inch at Nyquist, the total per inch, and the loss of 8 inches.
(c) Find the notch frequency of a 0.3 mm via stub and of a 1.0 mm stub in this dielectric. What is the longest stub whose notch stays at or above twice the Nyquist frequency?
(d) A 92 Ω connector sits in a 100 Ω differential channel. Find its reflection coefficient and return loss. Two coupled striplines in this homogeneous dielectric have $C_m/C = L_m/L$ = 0.03, and the aggressor swings 0.8 V with a 15 ps rise. Find the NEXT plateau, the length beyond which NEXT saturates, and the FEXT.

**2 [B] · Eyes, jitter and BER.** (24-02)
A channel's response to an isolated one-UI pulse of the full 1 V swing (levels 0 and 1 V) has cursors $h_{-1}$ = 0.04, $h_0$ = 0.60, $h_1$ = 0.18, $h_2$ = 0.06 and $h_3$ = 0.02 V. All cursors are positive, so the eye opening in volts equals the peak-distortion eye $E$ × 1 V.
(a) Find the peak-distortion eye height for NRZ and for PAM4.
(b) Repeat (a) after a DFE cancels $h_1$ to $h_3$ exactly.
(c) For the equalized PAM4 eye with 12 mV rms noise, find $V_{eye}/2\sigma$ and the BER.
(d) At 106.25 GBd the link has RJ = 0.15 ps rms and DJ(δδ) = 1.2 ps. Find the total jitter at 10⁻¹² and the eye width in ps and UI. How many bits must run without error to show BER < 10⁻¹² with 95% confidence, and how long does that take at 212.5 Gb/s?

**3 [B] · SerDes circuits.** (24-03)
(a) A two-tap transmit FFE ($c_0$, $c_1$) must cancel the first post-cursor of a channel with $h_0$ = 0.60 and $h_1$ = 0.20 (no other cursors) under the swing limit $\lvert c_0\rvert + \lvert c_1\rvert = 1$. Find $c_0$ and $c_1$, the equalized main cursor $g_0$, the new second post-cursor $g_2$, and the de-emphasis $20\log_{10}(1/(c_0 + c_1))$.
(b) A driver must deliver 1.0 V peak-to-peak differential into a double-terminated 50 Ω-per-side link. Find the tail current and power of a CML driver from 0.9 V, the power of a voltage-mode (SST) driver from a 1.0 V regulated supply, and the ratio (driver power only, excluding the regulator).
(c) A source-degenerated CTLE has $g_m$ = 25 mS, $R_S$ = 320 Ω, $C_S$ = 250 fF and $R_D$ = 200 Ω. Find the peaking in dB, the zero and first-pole frequencies, and the DC and high-frequency gains.
(d) A linear first-order CDR with a 20 MHz loop bandwidth tracks a 200 ppm frequency offset at 106.25 GBd. Find the steady-state phase error in UI.

**4 [B] · DSP SerDes and FEC.** (24-04)
(a) Find the jitter-limited SNR of an ADC sampling a 53.125 GHz tone with 50 fs rms clock jitter, and the equivalent number of bits ($(\text{SNR} - 1.76)/6.02$).
(b) A 6-bit ADC spans ±1.5 times the outer PAM4 level (levels ±1 and ±1/3). Find the step, the rms quantization noise and its ratio to the ISI-free half-eye of 1/3.
(c) Find MLSD's gain over a DFE for the channel $1 + 0.7D$.
(d) Find the net coding gain of RS(544,514) from an input BER of 2.4 × 10⁻⁴ to an output of 10⁻¹⁵, and the time one codeword (544 ten-bit symbols) takes to arrive at 212.5 Gb/s.

**5 [B] · Interconnect standards.** (24-05)
(a) Find the bandwidth per direction of a PCIe 5.0 x16 link (32 GT/s, 128b/130b) in GB/s.
(b) With 24 bytes of overhead per TLP, find the efficiency and the effective bandwidth for 128-byte payloads.
(c) What credit buffer covers a 500 ns round trip at the bandwidth found in (a)?
(d) Find the lane rate of a 200 Gb/s Ethernet MAC lane with 256b/257b transcoding and RS(544,514), and the hosts of a non-blocking two-tier leaf-spine fabric built from radix-64 and from radix-512 switches.

**6 [B] · Die-to-die links.** (24-06)
(a) An unterminated die-to-die wire presents 150 fF and swings 0.4 V. Find the energy per bit and the power at 32 Gb/s.
(b) A terminated link is driven from a 0.4 V supply through a 50 Ω driver into a 50 Ω termination at 32 Gb/s. Find its energy per bit.
(c) Bumps on a 36 µm square grid, half carrying data at 32 Gb/s: find the areal bandwidth density.
(d) A 2 mm on-package wire has $R_w$ = 50 Ω and $C_w$ = 200 fF; the driver has $R_{on}$ = 100 Ω and 50 fF of pad, and the receiver loads 50 fF. Find the total capacitance and the Elmore delay $R_{on}C_{tot} + R_w(C_w/2 + C_L)$. Which term dominates, and what would you improve first?

**7 [B] · Fiber and modulators.** (24-07)
(a) A 1310 nm photodiode has quantum efficiency 0.85. Find its responsivity, the power of −8 dBm in µW, and the photocurrent.
(b) A 106.25 GBd PAM4 signal at 1310 nm crosses 2 km with $D$ = 3.5 ps/(nm·km). Find the spectral width, the spread and the spread in UI.
(c) An MZM is biased at quadrature and driven over 0.6 $V_\pi$ peak to peak. Find the high and low output fractions, the extinction ratio as a ratio and in dB, and the OMA as a fraction of $P_{in}$.
(d) A receiver has 0.85 A/W and 18 pA/√Hz over 55 GHz. Find σ, the OOK sensitivity at the KP4 threshold in µW and dBm, the penalty of a 4 dB extinction ratio, and the PAM4 sensitivity with that extinction ratio.

**8 [B] · Receivers and link budgets.** (24-07)
(a) A CWDM4 lane launches 3 dBm over 2 km at 0.36 dB/km through two 0.5 dB connectors, a 1.8 dB multiplexer and a 1.8 dB demultiplexer. Find the received power and its margin over Question 7(d)'s PAM4 sensitivity.
(b) A shunt-feedback TIA has $A$ = 12, $R_F$ = 600 Ω and $C_{in}$ = 90 fF. Find its transimpedance, bandwidth, $R_F$'s noise density, and that noise integrated over the bandwidth.
(c) What wavelength spacing is an 800 GHz grid at 1310 nm, and what frequency spacing is 4.5 nm there?
(d) A silicon ring at 1310 nm has $n_g$ = 3.9 and $Q$ = 7,500, and silicon's index rises 1.8 × 10⁻⁴ per kelvin. Find the shift per kelvin, the linewidth, and the temperature change that moves the resonance by one linewidth.

**9 [B] · Silicon photonics.** (24-08)
(a) Find the coupling efficiency and loss between modes of 1/e field radii 4.6 µm (fiber) and 2.5 µm (chip), the extra loss of a 0.8 µm lateral offset, and the total.
(b) A grating coupler at 1310 nm has $n_{eff}$ = 2.75 and radiates at 12°. Find the period, the angular dispersion and the steer across 20 nm.
(c) A 50 Ω driver drives a 30 fF modulator through 0.2 nH. Find $f_0$, ζ, the peak gain and peaking in dB, the peak frequency, and $f_{3dB}$.
(d) A linear chain has segments of $Q$ = 8, 7 and 8. Find its $Q$ and BER, and the BER if each boundary retimed.

**10 [B] · Linear-drive and co-packaged optics.** (24-09)
(a) Find the energy per bit of a 4 W CPO port and a 14 W pluggable, both 800 Gb/s, and CPO's saving.
(b) An HP-class ELSFP (17 dBm) feeds lanes through 2 dB of path loss and 1 dB of splitter excess loss; each lane needs 2.0 dBm. Find the power available for splitting in dB and as a factor, and the lanes with binary splitting.
(c) Find the 95% failure-rate bound after 3 million device-hours with no failures, and with one.
(d) A pluggable fails at 150 FIT and is replaced in 0.5 h; a CPO engine serving 16 ports fails at 300 FIT and takes 8 h to restore. Find the ratio of port-hours lost per port.

**11 [C] · Derivations.** (24-01, 24-03, 24-08)
(a) Starting from $\alpha_d = G'Z_0/2$ with $G' = \omega C'\tan\delta$, derive $\alpha_d = \pi f\sqrt{\varepsilon_r}\tan\delta/c$. Evaluate it in dB/in at 26.5625 GHz for $\varepsilon_r$ = 3.0 and $\tan\delta$ = 0.0015.
(b) For a differential pair degenerated by $R_S$ in parallel with $C_S$ (half circuit: $R_S/2$ in parallel with $2C_S$) with load $R_D$, derive $H(s)$ and show $H(\infty)/H(0) = 1 + g_mR_S/2$. Evaluate the peaking for $g_m$ = 30 mS and $R_S$ = 300 Ω, as a ratio and in dB.
(c) Derive the power coupling between two circular Gaussian modes of $1/e$ field radii $w_1$ and $w_2$. Evaluate it for 4.6 µm and 3.0 µm, as a ratio and in dB.
(d) Show that independent Gaussian noises in a linear chain give $1/Q^2 = \sum 1/Q_i^2$, and that a zero-failure test of $T$ device-hours bounds the rate at $-\ln(0.05)/T$ with 95% confidence. Evaluate the $Q$ and BER for segments of 9, 7 and 9, and the bound for 5 million hours in FIT.

**12 [C] · Diligence: a linear-drive start-up.** (24-02, 24-08, 24-09)
A start-up pitches: "Our 1.6 Tb/s LPO module draws 8 W, against 25 W for DSP modules. In a 100,000-GPU cluster with four modules per GPU, that saves megawatts. With our partner's host SerDes, each 200 Gb/s lane runs at 10⁻¹² pre-FEC: the host channels give $Q$ = 11 each and our optics $Q$ = 6.5. Two million device-hours without a failure show our FIT rate is below 100."
(a) Find both modules' energy per bit, the cluster's module power with each, and the saving.
(b) Find the linear link's $Q$, its BER and its margin over KP4. What $Q$ would 10⁻¹² need? Is the claim consistent?
(c) Find the 95% bound from two million failure-free hours in FIT and the test in device-years. What exposure would support "below 100 FIT"?
(d) List four questions you would ask the start-up's chief architect, with what a strong answer contains.
