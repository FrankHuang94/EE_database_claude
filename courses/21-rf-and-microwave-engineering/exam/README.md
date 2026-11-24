# Course 21 · Final Exam (RF and Microwave Engineering)

**Time limit:** 240 minutes.
**Allowed:** a scientific calculator and the [Course 21 equation sheet](../../../reference/equation-sheets/21-rf-and-microwave-engineering.md) printed without its chapter links. No notes, no Python and no simulator.

**Instructions.**

- Answer all 14 questions and show every step.
- Questions 1–12 [B] are worth 8 points each (2 per part), and Questions 13 and 14 [C] 12 each (3 per part): 120 points in total. 84 or more (70%) is a strong pass.
- Give numerical answers to 3–4 significant figures, with units.
- Question 13 asks for derivations: results quoted from the equation sheet earn no credit unless derived. Question 14 is a diligence question, partly graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These follow the chapters.

- $Z_0$ = 50 Ω. Noise floors use −174 dBm/Hz (290 K); Question 6 uses $T$ = 300 K, so $kT$ = 4.142 × 10⁻²¹ J.
- Gains, noise factors and intercept points combine in linear units in cascades; IIP3 is input-referred, in dBm per tone.
- Tank quantities in Question 6 are differential. Phase noise $\mathcal L$ is single-sideband, in dBc/Hz.
- Butterworth band-pass filters use the normalized frequency $x = (f_0/B)(f/f_0 - f_0/f)$ with $B$ the 3 dB bandwidth.
- $c$ = 299,792,458 m/s; $GM$ = 3.986 × 10¹⁴ m³/s²; $R_E$ = 6371 km; $Q^{-1}(0.1)$ = 1.2816 (the standard normal's upper 10% point).

---

**1 [B] · S-parameters.** (21-01)
(a) A 25 Ω load terminates a 50 Ω line. Find Γ, the return loss, the VSWR and the mismatch loss.
(b) A 20 Ω resistor is connected in series between two 50 Ω ports. Find $S_{11}$, $S_{21}$, the insertion loss in dB and the fraction of the incident power the resistor absorbs.
(c) A transistor at 2 GHz has $S_{11}$ = 0.5∠−140°, $S_{21}$ = 4.0∠80°, $S_{12}$ = 0.04∠40° and $S_{22}$ = 0.45∠−45°. Find $\lvert\Delta\rvert$, $K$ and μ. Is it unconditionally stable? Find its MSG and $G_{max}$ in dB.
(d) Find $\Gamma_{in}$ (magnitude and angle) when the transistor drives a load with $\Gamma_L$ = 0.5∠60°.

**2 [B] · Matching a PA.** (21-02)
(a) Design a low-pass L-network (series L, shunt C) that transforms a 50 Ω load to the 4 Ω the PA needs at 2.4 GHz. Find Q, the inductance and the capacitance.
(b) Over what bandwidth does the match keep $\lvert\Gamma\rvert \le 0.1$? Use the first-order formula on the equation sheet and its large-Q approximation.
(c) The same match is made with two L-sections through the geometric mean. Find the intermediate resistance and the section Q, and, with inductors of $Q_u$ = 20, compare the inductor loss of the one- and two-section designs. A distributed alternative is a two-section binomial quarter-wave transformer: find its section impedances.
(d) The transistor's output is better modelled as 4 Ω in parallel with 40 pF. What is the widest band over which any lossless network can keep $\lvert\Gamma\rvert \le 0.1$?

**3 [B] · A receiver cascade.** (21-03)
A receiver chain is an LNA (gain 16 dB, NF 1.8 dB, IIP3 −8 dBm), then a passive, perfectly linear filter with 2.5 dB loss, then a mixer (gain 10 dB, NF 9 dB, IIP3 +3 dBm).
(a) Find the cascaded noise figure.
(b) Find the cascaded IIP3.
(c) For a 20 MHz channel and 5 dB minimum SNR, find the sensitivity and the spurious-free dynamic range.
(d) What Y-factor (in dB) should a noise-figure meter read for this cascade with a 15 dB ENR source?

**4 [B] · An inductively degenerated LNA.** (21-04)
A 5.5 GHz LNA uses a device with $f_T$ = 55 GHz and $C_{gs}$ = 150 fF from a 50 Ω source, with γ/α = 1.
(a) Find $L_s$ and $L_g$ for a 50 Ω match.
(b) Find $Q_{in}$ and $G_m$. If the transistor's own IIP3, referred to its gate–source voltage, corresponds to +5 dBm, what is the LNA's IIP3 referred to the source?
(c) Find $g_m$ and the noise figure with ideal inductors. Then let $L_g$ have $Q_L$ = 20: find $r_g$ (using the $L_g$ of part a), the re-matched $L_s$ and the new noise figure.
(d) A mixer with NF 10 dB follows. What LNA gain keeps the mixer from adding more than 0.5 dB to the lossy LNA's noise figure?

**5 [B] · Mixers.** (21-05)
(a) Find the conversion gain (dB) of an ideal passive switching mixer and of a Gilbert cell with $g_m$ = 25 mS and $R_L$ = 400 Ω. What is the ideal switching mixer's SSB noise figure for white source noise with no filter ahead of it?
(b) An image-reject receiver's I and Q paths have a 0.3 dB gain error and a 3° phase error. Find ε, the exact IRR and the small-error approximation.
(c) With a square-wave LO, how far below the wanted response is the response to an input at $3f_{LO}$? With the ideal three-phase harmonic-reject LO, the 3rd and 5th vanish: how far below is the response at $7f_{LO}$?
(d) A 6-path filter has $R_s$ = 50 Ω and 25 pF per path. Find its 3 dB bandwidth and its centre-frequency voltage gain in dB.

**6 [B] · An LC VCO.** (21-06)
A 6 GHz cross-coupled VCO has a 0.6 nH (differential) inductor with $Q_L$ = 12 and capacitors with $Q_C$ = 30. Its tail current is 3 mA from 1.0 V, and the pair switches hard.
(a) Find the tank Q, the capacitance that resonates at 6 GHz and $R_p$.
(b) Find the differential amplitude, the efficiency $P_s/P_{DC}$ and the tank signal power $P_s$.
(c) Find the phase noise at 1 MHz offset from the tank's noise alone, and with an excess-noise factor $F$ = 3 (Leeson).
(d) Find the FoM with $F$ = 3 and $P_{DC}$ = 3 mW, and the phase noise at 1 MHz offset after an ideal divide-by-2.

**7 [B] · A power amplifier.** (21-07)
A handset PA must deliver 28 dBm from $V_{DD}$ = 3.4 V with a knee of 0.4 V.
(a) Find $R_{opt}$ and the Q of an L-network that transforms 50 Ω to it.
(b) Find the ideal drain efficiency for conduction angles of 360°, 240°, 180° and 120°. What is the class-A efficiency with the 0.4 V knee?
(c) The PA's IIP3 is +6 dBm and its gain 30 dB. What is the highest average input power for which the cubic model's ACLR stays at or below −40 dBc, and what output power is that? How far is it below the 28 dBm saturated power, and where do the signal's peaks (9.64 dB PAPR) fall?
(d) Find the ideal efficiency of a symmetric Doherty and of class B at 8 dB back-off, and of the Doherty at 3 dB back-off. An envelope-tracking PA instead holds 65% drain efficiency at every level with an 85%-efficient supply modulator: what is its overall efficiency?

**8 [B] · Architectures.** (21-08)
(a) A 5.8 GHz receiver uses a 400 MHz IF with a low-side LO. Find the LO, the image and both half-IF spur frequencies.
(b) A fourth-order Butterworth preselector is centred at 5.8 GHz with 200 MHz bandwidth. Find its rejection at the image and at each half-IF frequency.
(c) A low-IF receiver must tolerate an adjacent channel (its image) 30 dB stronger than the wanted signal, which needs 12 dB SNR. Find the IRR it needs, and the largest phase error allowed if the gains match exactly.
(d) A direct-sampling ADC has NSD = −153 dBFS/Hz and a full scale of +2 dBm. Find its noise figure, the gain needed ahead of it so that it degrades a 2 dB front end by at most 1 dB, and the rms clock jitter that keeps the jitter-limited SNR at 55 dB for a 6 GHz input.

**9 [B] · Filters and switches.** (21-09)
(a) A BAW resonator has $f_s$ = 3.55 GHz and $f_p$ = 3.65 GHz. Find $k^2_{eff}$ (exact and approximate) and $C_m/C_0$.
(b) A Band 3 handset duplexer has 2.5 dB transmit loss and 50 dB transmit-to-receive isolation in the transmit band. For 26 dBm at the antenna, what must the PA deliver, and what reaches the LNA? The PA's noise in the receive band is −138 dBm/Hz; with a 4 dB receiver noise figure and 6 dB margin, what receive-band isolation is needed?
(c) An SOI switch has $R_{on}$ = 2.4 Ω and $C_{off}$ = 100 fF. Find its figure of merit, cut-off frequency, on-state loss and off-state isolation at 3.5 GHz (series switch between 50 Ω ports).
(d) The switch must survive 33 dBm into 50 Ω at VSWR 4:1, and each transistor tolerates 3.0 V peak. Find the line's peak voltage, the worst-case peak and the number of stacked transistors. What is the mismatch loss at VSWR 4?

**10 [B] · A phased array.** (21-10)
An 8 × 8 array at 39 GHz has λ/2 spacing at 39 GHz, element gain 5 dBi and 8 dBm per element.
(a) Find the EIRP at broadside and, with cosine scan loss, at 50°.
(b) Phase shifters steer each row of 8 to 50° at 39 GHz. Where does the beam point at 37 GHz? Estimate the row's 3 dB squint bandwidth.
(c) With 2-bit phase shifters and decorrelated errors, find the gain loss, the floor of scattered power relative to the peak and the rms phase error. What is the fewest bits that puts the floor below −40 dB?
(d) Is the array free of grating lobes when scanned to 50° at 42 GHz? Give the spacing in wavelengths and the limit.

**11 [B] · A wearable link.** (21-11)
A 2.44 GHz wrist wearable transmits 0 dBm through 1 dB of loss into a −6 dBi antenna. The phone has a −1 dBi antenna, 1.5 dB of front-end loss, NF 7 dB and needs $E_b/N_0$ = 11 dB at 1 Mb/s. The body adds 10 dB; shadowing has σ = 6 dB and the link must close 90% of the time.
(a) Find the EIRP and the sensitivity.
(b) Find the shadowing margin and the maximum allowable path loss.
(c) With free-space loss to 1 m and exponent 3 beyond, find the 1 m loss and the range.
(d) A coded mode runs at 125 kb/s and needs $E_b/N_0$ = 5 dB. Find its sensitivity and range.

**12 [B] · Modems and positioning.** (21-12)
(a) A phone aggregates an 80 MHz (217 resource blocks) and a 60 MHz (162 resource blocks) carrier, both at 30 kHz with 4 layers of 256-QAM and 14% overhead, with $R_{max}$ = 948/1024 and scaling factor $f$ = 1. Find each carrier's peak rate and the total.
(b) Find the two-stream rate of a 160 MHz Wi-Fi 7 channel (1960 data subcarriers) at 1024-QAM, rate 5/6, with a 1.6 µs guard interval.
(c) Two UWB devices run single-sided ranging: the initiator's clock is 5 ppm fast, the responder's 15 ppm slow, and the reply time is 300 µs. Find the range error, and the longest reply time that keeps it under 10 cm.
(d) For a satellite at 1200 km, find the orbital speed, the largest line-of-sight speed toward a ground user, the Doppler shift at 2 GHz and that shift in 15 kHz subcarriers.

**13 [C] · Derivations.** (21-03, 21-10, 21-11)
(a) Starting from $y = a_1x + a_3x^3$ with $a_3/a_1 < 0$, derive the 1 dB compression amplitude and the input intercept amplitude, and show that IIP3 − P1dB ≈ 9.64 dB. What is P1dB for an IIP3 of −10 dBm?
(b) From the definition of noise temperature, derive Friis's formula for two stages, $T_e = T_1 + T_2/G_1$, and convert it to noise factors. Evaluate the equivalent noise temperature of Question 3's cascade.
(c) For an array that must reach EIRP $E$ with $N$ elements of gain $G_e$, PA efficiency η and per-element overhead $P_{oh}$, derive the element count that minimizes DC power, the minimum power, and the penalty for using twice or half that count. Evaluate for $E$ = 65 dBm, $G_e$ = 5 dBi, η = 20% and $P_{oh}$ = 50 mW.
(d) From Shannon's capacity, derive the minimum $E_b/N_0$ at spectral efficiency η and its limit as η → 0. Evaluate at η = 2 and 6 b/s/Hz.

**14 [C] · Diligence: a front-end claim.** (21-07, 21-09, 21-03)
A start-up pitches a single-chip 3.5 GHz front end: "one series SOI switch with 0.2 dB loss and 40 dB isolation; a PA at 45% average efficiency delivering 26 dBm average on 100 MHz OFDM; and a 1.0 dB-NF LNA for best-in-class sensitivity."
(a) For one series switch between 50 Ω ports at 3.5 GHz, find the largest $R_{on}$ and $C_{off}$ that meet the claim and their product. Compare it with the ~100 fs of today's SOI processes (21-09 §9). What would you conclude?
(b) The OFDM signal has a 9.64 dB PAPR. Find the PA's peak output power, and the DC power and battery current (3.8 V) at the claimed 45%. 21-07 found an average efficiency of 29.2% for ideal class B and 54.9% for an ideal symmetric Doherty on this signal: find the DC power for each, and judge the claim.
(c) The receive path is the switch, a filter with 1.5 dB loss, the LNA (NF 1.0 dB, gain 18 dB) and a transceiver with NF 6 dB. Find the system noise figure with the claimed 0.2 dB switch and with a 0.5 dB switch.
(d) List four questions you would ask the start-up's chief architect, with what a strong answer contains.
