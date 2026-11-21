# Term 5 Checkpoint · Solutions

Questions: [README.md](README.md). [verify_term5.py](verify_term5.py) checks every numerical answer and the letter of every multiple-choice answer. It recomputes each value by its own route: simulated step and ramp responses, root finding on loop gains, FFTs of synthetic signals, a Monte Carlo BPSK link, exhaustive syndrome decoding, and the Course 18 lab models. Each explanation names the chapter to revisit.

**Scoring by block:** control 13, DSP 13, communications and networks 13, embedded systems and software 11. Aim for at least 70% in each (10, 10, 10 and 8 correct).

---

## Block 1 · Control systems

**1. Answer: 25.4.** $\%OS = 100\,e^{-\zeta\pi/\sqrt{1 - \zeta^2}} = 100\,e^{-0.4\pi/\sqrt{0.84}} = 100\,e^{-1.371}$. Overshoot depends only on ζ; $\omega_n$ sets the time scale. *([15-03](../../courses/15-control-systems/chapters/15-03-time-response.md))*

**2. Answer: (B) 1.00 s.** $t_s \approx 4/(\zeta\omega_n) = 4/(0.4 \times 10)$. (A) is $4/\omega_n$, dropping ζ; (C) is the peak time $\pi/(\omega_n\sqrt{1 - \zeta^2})$, a different quantity; (D) divides by ζ twice. The exact 2% settling time of this system is a little shorter; the estimate is a design rule. *([15-03](../../courses/15-control-systems/chapters/15-03-time-response.md))*

**3. Answer: 0.167.** A type-0 loop has $e_{ss} = 1/(1 + K_p)$ with $K_p = G(0) = 20/4 = 5$, so $e_{ss} = 1/6$. *([15-04](../../courses/15-control-systems/chapters/15-04-feedback-and-steady-state-error.md))*

**4. Answer: (B) 0.100.** The loop is type 1: $K_v = \lim_{s \to 0} sG(s) = 50/5 = 10$, and the ramp error is $1/K_v$. (A) is the step error of a type-1 loop; (D) is $K_v$ itself. *([15-04](../../courses/15-control-systems/chapters/15-04-feedback-and-steady-state-error.md))*

**5. Answer: 66.0.** The Routh array's $s^1$ row is $(6 \times 11 - K)/6$, positive for $K < 66$, and the $s^0$ row needs $K > 0$. *([15-05](../../courses/15-control-systems/chapters/15-05-stability-routh-hurwitz.md))*

**6. Answer: (A) 3.32 rad/s.** At $K$ = 66 the $s^1$ row vanishes and the auxiliary polynomial from the $s^2$ row, $6s^2 + 66 = 0$, gives $s = \pm j\sqrt{11}$. *([15-05](../../courses/15-control-systems/chapters/15-05-stability-routh-hurwitz.md))*

**7. Answer: 18.0.** The gain crossover solves $10/(\omega\sqrt{1 + \omega^2}) = 1$, i.e. $\omega^4 + \omega^2 - 100 = 0$, so $\omega^2 = 9.51$ and $\omega_c$ = 3.08 rad/s. There the phase is $-90° - \arctan 3.08 = -162.0°$, so PM = 18.0°: a lightly damped loop (about 60% overshoot). *([15-07](../../courses/15-control-systems/chapters/15-07-frequency-domain-design.md))*

**8. Answer: (A) 15.6 dB.** $(j\omega + 1)(j\omega + 2)(j\omega + 3) = (6 - 6\omega^2) + j(11\omega - \omega^3)$. The phase is −180° where the imaginary part vanishes, $\omega = \sqrt{11}$; there the denominator is $6 - 66 = -60$, so $\lvert L\rvert = 10/60$ and the gain margin is 6, or $20\log_{10}6$ = 15.6 dB. (B) gives the ratio 6 labelled as decibels. *([15-07](../../courses/15-control-systems/chapters/15-07-frequency-domain-design.md))*

**9. Answer: 54.9.** $\sin\phi_{max} = (\alpha - 1)/(\alpha + 1) = 9/11$. *([15-09](../../courses/15-control-systems/chapters/15-09-lead-lag-compensation.md))*

**10. Answer: (A) 6.32 rad/s.** The maximum phase lies at the geometric mean of the zero and the pole, $\sqrt{2 \times 20}$. (B) is their arithmetic mean. *([15-09](../../courses/15-control-systems/chapters/15-09-lead-lag-compensation.md))*

**11. Answer: 0.167.** At DC, $\dot{\mathbf x} = 0$, so $\mathbf x = -A^{-1}Bu$ and $y/u = -CA^{-1}B$. Here the second state equation gives $-6x_1 - 5x_2 + u = 0$ with $x_2 = 0$ from the first, so $x_1 = u/6$. Equivalently $G(s) = 1/(s^2 + 5s + 6)$ and $G(0) = 1/6$. *([15-10](../../courses/15-control-systems/chapters/15-10-state-space-introduction.md))*

**12. Answer: (A) −2 and −3.** $\det(sI - A) = s^2 + 5s + 6 = (s + 2)(s + 3)$: the eigenvalues are the poles of $G(s)$. *([15-10](../../courses/15-control-systems/chapters/15-10-state-space-introduction.md))*

**13. Answer: 0.819.** A zero-order hold maps a pole at $s = -a$ to $z = e^{-aT} = e^{-0.2}$. *([15-11](../../courses/15-control-systems/chapters/15-11-digital-control.md))*

## Block 2 · Digital signal processing

**14. Answer: (A) 3.00 kHz.** Frequencies fold about $f_s/2$ = 5 kHz: $\lvert 7 - 10\rvert$ = 3 kHz. *([11-10](../../courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md), [16-01](../../courses/16-digital-signal-processing/chapters/16-01-discrete-time-systems-review.md))*

**15. Answer: 43.1.** $\Delta f = f_s/N$ = 44 100/1024 = 43.07 Hz. *([16-03](../../courses/16-digital-signal-processing/chapters/16-03-the-dft.md))*

**16. Answer: (A) 5120.** A radix-2 FFT has $\log_2N$ = 10 stages of $N/2$ = 512 butterflies. (C) is the $N^2$ of a direct DFT. *([16-04](../../courses/16-digital-signal-processing/chapters/16-04-the-fft.md))*

**17. Answer: 172.** Hann's first nulls are 2 bins either side of the peak, so its main lobe is 4 bins wide: $4 \times 43.07$ Hz. *([16-05](../../courses/16-digital-signal-processing/chapters/16-05-spectral-analysis-and-windowing.md))*

**18. Answer: (A) 2.50 ms.** A linear-phase FIR of $N$ taps delays every frequency by $(N - 1)/2$ = 20 samples, 20/8000 s. (B) uses $N$ samples. *([16-06](../../courses/16-digital-signal-processing/chapters/16-06-fir-filter-design.md))*

**19. Answer: 1.05.** The bilinear transform maps digital $\omega$ to analog $\Omega = (2/T)\tan(\omega/2)$: $f_a = (f_s/\pi)\tan(\pi f/f_s) = (8000/\pi)\tan(\pi/8)$ = 1.055 kHz. Designing the analog prototype at this prewarped frequency puts the digital cutoff exactly at 1 kHz. *([16-07](../../courses/16-digital-signal-processing/chapters/16-07-iir-filter-design.md))*

**20. Answer: (A) stable, with both poles at radius 0.707.** The poles solve $z^2 - 1.2z + 0.5 = 0$: $z = 0.6 \pm j0.5$, a complex pair whose product of magnitudes equals the constant term, $r^2 = 0.5$, so $r$ = 0.707 < 1. *([16-02](../../courses/16-digital-signal-processing/chapters/16-02-dtft-and-z-transform-for-dsp.md))*

**21. Answer: 98.1.** $6.02N + 1.76$ dB for a full-scale sine: $6.02 \times 16 + 1.76$. *([16-10](../../courses/16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md))*

**22. Answer: (A) 6.00 kHz.** The new rate is 12 kHz, whose Nyquist frequency is 6 kHz; anything above it would alias after the decimation. *([16-09](../../courses/16-digital-signal-processing/chapters/16-09-multirate-dsp.md))*

**23. Answer: 0.333.** $H(e^{j\omega}) = \tfrac13(1 + e^{-j\omega} + e^{-2j\omega}) = \tfrac13e^{-j\omega}(1 + 2\cos\omega)$, so $\lvert H\rvert = \lvert 1 + 2\cos\omega\rvert/3$ = 1/3 at $\omega = \pi/2$. *([16-02](../../courses/16-digital-signal-processing/chapters/16-02-dtft-and-z-transform-for-dsp.md))*

**24. Answer: (A) −12288.** 0.75 is 24 576 and −0.5 is −16 384 in Q15. Their product is −402 653 184 in Q30, and shifting right by 15 gives −12 288, which is −0.375 × 32 768. (B) forgets that the product has 30 fractional bits and shifts by 14. *([16-10](../../courses/16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md))*

**25. Answer: 1.25.** By the final-value theorem, the step response settles at $H(1) = 0.5/(1 - 0.6)$, the DC gain. *([16-02](../../courses/16-digital-signal-processing/chapters/16-02-dtft-and-z-transform-for-dsp.md))*

**26. Answer: (B) makes the bin spacing four times finer but does not improve resolution.** Zero padding samples the same DTFT of the 256-sample record more densely. Resolution, the ability to separate two close tones, is set by the record length (the window's main lobe), which is unchanged. *([16-05](../../courses/16-digital-signal-processing/chapters/16-05-spectral-analysis-and-windowing.md))*

## Block 3 · Communications and networks

**27. Answer: −114.** $kT_0B$ in dBm is −174 dBm/Hz + 10 log₁₀(10⁶) = −174 + 60. *([17-02](../../courses/17-communication-systems/chapters/17-02-noise-and-snr.md))*

**28. Answer: (A) 2.24 dB.** Friis: $F = F_1 + (F_2 - 1)/G_1 = 1.585 + 9/100 = 1.675$, or 2.24 dB. The LNA's gain suppresses the mixer's contribution; (B) adds the noise figures. *([17-02](../../courses/17-communication-systems/chapters/17-02-noise-and-snr.md))*

**29. Answer: 180.** Carson: $B \approx 2(\Delta f + W) = 2(75 + 15)$ kHz, the bandwidth of broadcast FM. *([17-03](../../courses/17-communication-systems/chapters/17-03-analog-modulation.md))*

**30. Answer: (A) 6.25 MHz.** Raised-cosine pulses occupy $(1 + \alpha)R_s/2$ at baseband: $1.25 \times 10/2$. (B) is the Nyquist minimum, $R_s/2$, without roll-off; (C) is the bandpass width $(1 + \alpha)R_s$. *([17-04](../../courses/17-communication-systems/chapters/17-04-baseband-digital-transmission.md))*

**31. Answer: 1.91e-4.** $P_b = Q(\sqrt{2E_b/N_0})$ with $E_b/N_0 = 10^{0.8} = 6.31$: $Q(3.55)$. *([17-06](../../courses/17-communication-systems/chapters/17-06-bandpass-digital-modulation.md))*

**32. Answer: (A) 4.00 Mb/s.** $C = B\log_2(1 + \text{SNR}) = 10^6 \times \log_2 16$. (B) multiplies the bandwidth by the SNR. *([17-07](../../courses/17-communication-systems/chapters/17-07-information-theory-and-shannon.md))*

**33. Answer: 80.1.** $L = 20\log_{10}(4\pi d/\lambda)$ with $\lambda$ = 0.1249 m: $20\log_{10}(10\,060)$. *([17-09](../../courses/17-communication-systems/chapters/17-09-wireless-channels.md))*

**34. Answer: (C) corrects any single error, and miscorrects double errors.** The seven columns of the parity-check matrix are the seven distinct nonzero 3-bit syndromes, so every single error is identified. Its minimum distance is 3, so two errors produce the syndrome of a third position, and the decoder flips the wrong bit. *([17-08](../../courses/17-communication-systems/chapters/17-08-channel-coding.md))*

**35. Answer: 312.5** (four significant figures, since the value is exact). $\Delta f = B/N$ = 20 MHz/64, the spacing of 802.11a/g. The useful symbol lasts $1/\Delta f$ = 3.2 µs. *([17-10](../../courses/17-communication-systems/chapters/17-10-ofdm.md))*

**36. Answer: (A) 10.5 Mb/s.** At most one window per round trip: $65\,536 \times 8\ \text{bits}/0.05\ \text{s}$. A faster link does not help; window scaling does. *([17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md))*

**37. Answer: 62.** A /26 leaves 6 host bits, 64 addresses, less the network and broadcast addresses. *([17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md))*

**38. Answer: (A) 0.368.** Slotted ALOHA's throughput $S = Ge^{-G}$ peaks at $G$ = 1 with $S = 1/e$; pure ALOHA's $Ge^{-2G}$ peaks at $1/(2e)$, (B). *([17-12](../../courses/17-communication-systems/chapters/17-12-multiple-access-and-cellular-wifi.md))*

**39. Answer: 97.5.** $1500/(8 + 14 + 1500 + 4 + 12) = 1500/1538$. With IPv4 and TCP headers inside the payload the goodput is lower still, 1460/1538. *([17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md))*

## Block 4 · Embedded systems and software

**40. Answer: (A) 2.** $\text{WS} = \lceil f\,t_{acc}\rceil - 1 = \lceil 2.5\rceil - 1$: three 10 ns cycles cover 25 ns. *([18-01](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-01-microcontroller-architecture.md))*

**41. Answer: 960.** An 8N1 frame is 10 bits: start, 8 data and stop. *([18-05](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-05-gpio-uart-spi-i2c.md))*

**42. Answer: (A) 186 ns.** The RC charges from 30% to 70% in $RC\ln(0.7/0.3) = 0.8473 \times 220$ ns. (B) is $RC$ itself. *([18-05](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-05-gpio-uart-spi-i2c.md))*

**43. Answer: 0.806.** $3.3\ \text{V}/2^{12}$. *([18-06](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-06-adc-dac-pwm.md))*

**44. Answer: (A) 0.828.** $n(2^{1/n} - 1)$ with $n$ = 2 is $2(\sqrt2 - 1)$; (B) is the limit ln 2 for many tasks, (D) the three-task value. *([18-07](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-07-rtos-concepts.md))*

**45. Answer: 9.** From $R = 3$: $3 + \lceil 3/5\rceil 2 + \lceil 3/10\rceil 2 = 7$; $3 + \lceil 7/5\rceil 2 + \lceil 7/10\rceil 2 = 9$; and 9 again, so $R$ = 9 ms ≤ 20 ms. *([18-07](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-07-rtos-concepts.md))*

**46. Answer: (A) 479 days.** $230\ \text{mAh}/20\ \mu\text{A}$ = 11 500 h. A real budget would also derate the capacity for temperature and self-discharge. *([18-09](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-09-ultra-low-power-design.md))*

**47. Answer: 10.0.** Ping-pong buffers are safe when $L + a + bN \le N/f_s$: $N \ge (a + L)f_s/(1 - bf_s) = 80 \times 10^{-6} \times 10^5/(1 - 0.2)$. *([18-04](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-04-dma-and-data-movement.md))*

**48. Answer: (A) 20.** Each comparison halves the remaining range, so $\lceil\log_2(N + 1)\rceil$ comparisons suffice: $2^{20}$ = 1 048 576 exceeds 1 000 000. *([05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md))*

**49. Answer: 4.17.** On average $(10^4 + 1)/2$ tries, at 3 s each: 15 001.5 s. A lockout after a few failures turns hours into years. *([18-11](../../courses/18-embedded-systems-and-microcontrollers/chapters/18-11-hardware-security.md))*

**50. Answer: (A) −200.** 0xFF38 is 65 336 unsigned; subtracting $2^{16}$ gives −200. Equivalently, inverting gives 0x00C7 = 199, and adding 1 gives the magnitude 200. *([05-07](../../courses/05-programming-for-engineers/chapters/05-07-bit-manipulation.md))*

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| T5.01 | percent overshoot | 25.4 | % |
| T5.02 | 2% settling time | 1.00 | s |
| T5.03 | step error, type 0 | 0.167 | — |
| T5.04 | ramp error, type 1 | 0.100 | — |
| T5.05 | largest stable K | 66.0 | — |
| T5.06 | oscillation frequency | 3.32 | rad/s |
| T5.07 | phase margin | 18.0 | ° |
| T5.08 | gain margin | 15.6 | dB |
| T5.09 | maximum lead phase | 54.9 | ° |
| T5.10 | frequency of maximum phase | 6.32 | rad/s |
| T5.11 | DC gain | 0.167 | — |
| T5.13 | discrete pole | 0.819 | — |
| T5.14 | alias frequency | 3.00 | kHz |
| T5.15 | bin spacing | 43.1 | Hz |
| T5.16 | butterflies | 5120 | — |
| T5.17 | Hann main-lobe width | 172 | Hz |
| T5.18 | group delay | 2.50 | ms |
| T5.19 | prewarped cutoff | 1.05 | kHz |
| T5.21 | ideal SQNR, 16 bits | 98.1 | dB |
| T5.22 | anti-alias edge after decimation | 6.00 | kHz |
| T5.23 | moving-average gain at π/2 | 0.333 | — |
| T5.24 | Q15 product | -12288 | — |
| T5.25 | final value | 1.25 | — |
| T5.27 | thermal noise in 1 MHz | -114 | dBm |
| T5.28 | cascade noise figure | 2.24 | dB |
| T5.29 | Carson bandwidth | 180 | kHz |
| T5.30 | raised-cosine bandwidth | 6.25 | MHz |
| T5.31 | BPSK bit error rate | 1.91e-4 | — |
| T5.32 | Shannon capacity | 4.00 | Mb/s |
| T5.33 | free-space path loss | 80.1 | dB |
| T5.35 | subcarrier spacing | 312.5 | kHz |
| T5.36 | TCP window limit | 10.5 | Mb/s |
| T5.37 | usable hosts | 62 | — |
| T5.38 | slotted ALOHA maximum | 0.368 | — |
| T5.39 | payload share of line time | 97.5 | % |
| T5.40 | wait states | 2 | — |
| T5.41 | UART bytes per second | 960 | bytes/s |
| T5.42 | I²C rise time | 186 | ns |
| T5.43 | ADC LSB | 0.806 | mV |
| T5.44 | two-task RM bound | 0.828 | — |
| T5.45 | worst response time | 9 | ms |
| T5.46 | battery life | 479 | days |
| T5.47 | smallest safe block | 10.0 | samples |
| T5.48 | binary-search comparisons | 20 | — |
| T5.49 | average brute-force time | 4.17 | h |
| T5.50 | two's-complement value | -200 | — |
