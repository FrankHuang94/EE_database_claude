<!-- status: reviewed -->
# 21-05 · Mixers

| | |
|---|---|
| **Course** | [21 · RF and Microwave Engineering](../README.md) |
| **University equivalent** | The mixer chapter of a senior or first-year graduate RF IC course: frequency translation, the image, switching (commutating) mixers and their harmonic responses, active (Gilbert) and passive mixers, the noise and noise folding of ideal switching mixers (active-mixer noise analysis is left to Razavi), image-reject architectures, harmonic-reject mixers, LO leakage and second-order distortion, N-path filters (Razavi, *RF Microelectronics*, the mixer and transceiver-architecture chapters; Lee, *The Design of CMOS Radio-Frequency Integrated Circuits*, the mixer chapter) |
| **Prerequisites** | [21-03](21-03-noise-figure-and-linearity.md) (noise figure, IIP2/IIP3), [21-04](21-04-low-noise-amplifiers.md) (the stage before the mixer), [11-05](../../11-signals-and-systems/chapters/11-05-fourier-series.md) (Fourier series), [11-11](../../11-signals-and-systems/chapters/11-11-modulation-and-filtering-applications.md) (modulation and frequency shifting) |
| **Estimated study hours** | 6 |
| **Last verified** | 2026-11-24 |

**Learning objectives.** After this chapter you can:

1. Plan a mixer's frequencies: IF, image and the harmonic responses of a switching mixer, with their conversion gains.
2. Derive the conversion gain of commutating mixers (passive and Gilbert-cell) from the Fourier series of the LO waveform.
3. Derive the image-rejection ratio of a quadrature (Hartley) receiver as a function of gain and phase error, and size the error budget for a target.
4. Explain mixer noise figure, including SSB versus DSB definitions and noise folding from LO harmonics.
5. Design a three-phase harmonic-reject LO and quantify how mismatch limits its rejection.
6. Derive the bandwidth and centre loss of an N-path filter, and explain LO leakage, self-mixing and IIP2 in zero-IF receivers.

## 1. Big picture

A radio's antenna sees gigahertz signals, but filtering, amplifying with gain and digitizing are far easier at low frequencies. A **mixer** moves a signal from one frequency to another: it multiplies the incoming RF signal by a **local oscillator** (LO), and the product contains the signal shifted to the sum and difference frequencies. Receivers shift down to an **intermediate frequency** (IF) or straight to zero (zero-IF, 21-08); transmitters shift up. The multiplication is never perfect: the mixer also converts signals at the **image** frequency and at harmonics of the LO, adds noise, leaks LO power to the antenna and distorts. This chapter derives each of these from the LO waveform and shows the circuits that tame them.

- **Every transceiver** has at least one mixer per path, usually a quadrature (I/Q) pair driven by LOs 90° apart.
- **The LO's quality** (phase noise, 21-06; harmonics; leakage) becomes the mixer's quality, because the mixer multiplies by all of it.
- **Wideband radios** (software-defined, multi-band cellular) must suppress LO-harmonic responses without fixed filters: harmonic-reject mixers and N-path filters do this in CMOS.
- **Zero-IF receivers** trade the image problem for DC offsets and second-order distortion (21-03 §3.5), which the mixer largely determines.

## 2. Intuition first

```text
   spectrum at the RF input                     after mixing with f_LO (receiver, low-side LO)
                                                 
   image        LO         wanted               IF:  wanted and image land on the SAME frequency
     |          |            |                         |
   f_LO-f_IF   f_LO       f_LO+f_IF            0     f_IF        ...  and 3f_LO ± f_IF, 5f_LO ± f_IF,
                                                                       weaker by 1/3, 1/5, if the LO
                                                                       is a square wave
```

*Figure 1. Frequency translation. Multiplying by a cosine at $f_{LO}$ shifts every input component by $\pm f_{LO}$, so two inputs, the wanted signal at $f_{LO} + f_{IF}$ and the image at $f_{LO} - f_{IF}$, both arrive at $f_{IF}$. A switching mixer also multiplies by the LO's odd harmonics.*

**A currency-exchange analogy.** A mixer is a currency exchange: it converts a sum quoted in one currency (frequency) into another at a fixed rate (the LO). The problem is that the exchange works in both directions at once: a client holding the "image currency" gets converted into the same output currency as the client you wanted to serve, and the counter cannot tell them apart afterwards. You have to turn the image client away before the exchange (an image filter), or run two exchanges in quadrature whose errors cancel (an image-reject architecture). The analogy breaks because a real exchange charges a spread proportional to volume, while a mixer's "spread" (conversion loss) is a fixed ratio set by the shape of the LO waveform.

## 3. Theory

### 3.1 Multiplication and the image

Multiply an RF input $A\cos\omega_{RF}t$ by an LO $\cos\omega_{LO}t$:

$$
A\cos\omega_{RF}t\cdot\cos\omega_{LO}t = \frac A2\cos(\omega_{RF} - \omega_{LO})t + \frac A2\cos(\omega_{RF} + \omega_{LO})t .
$$

A low-pass filter keeps the difference term at $\omega_{IF} = \lvert\omega_{RF} - \omega_{LO}\rvert$. Because only the magnitude of the difference matters, an input at $\omega_{LO} - \omega_{IF}$ produces the same IF as one at $\omega_{LO} + \omega_{IF}$: they are each other's **image**, separated by $2\omega_{IF}$. With a **low-side** LO ($f_{LO} < f_{RF}$) the image is at $2f_{LO} - f_{RF}$; with a **high-side** LO it is above. Once both are at the IF, nothing separates them, so the image must be removed before the mixer (a filter, which is easiest when $f_{IF}$ is large) or cancelled by a quadrature architecture (§3.5).

### 3.2 Switching mixers and their harmonic responses

Real mixers do not multiply by a sinusoid; they switch. A double-balanced **commutating** mixer connects the input to the output directly for half the LO period and inverted for the other half, i.e. it multiplies by a square wave $s(t) = \operatorname{sign}(\cos\omega_{LO}t)$. Its Fourier series (11-05) is

$$
s(t) = \frac4\pi\left[\cos\omega_{LO}t - \frac13\cos3\omega_{LO}t + \frac15\cos5\omega_{LO}t - \cdots\right] .
$$

Multiplying by the first term and keeping the difference frequency gives a voltage **conversion gain**

$$
G_c = \frac12\cdot\frac4\pi = \frac2\pi \qquad (-3.92\ \text{dB}),
$$

and the $n$-th harmonic (odd $n$) converts inputs at $nf_{LO} \pm f_{IF}$ to the IF with gain $2/(n\pi)$: −13.46 dB for $n$ = 3 and −17.90 dB for $n$ = 5. A wideband receiver without a filter in front of the mixer therefore also hears signals near $3f_{LO}$ and $5f_{LO}$, only 9.5 and 14 dB weaker than the wanted one (Example 21-05.1). A single-switch (unbalanced, "return-to-zero") mixer switches between the input and nothing, a 0/1 waveform $\tfrac12 + \tfrac12s(t)$: its conversion gain is $1/\pi$, and the $\tfrac12$ term passes the RF straight to the output. A **single-balanced** mixer uses a differential LO and two switches (or a switching pair), so its differential output is again multiplied by ±1 with gain $2/\pi$; but the LO, or in an active mixer the bias current times $s(t)$, feeds through to the output. A **double-balanced** mixer cancels both feedthroughs and suppresses even-order products, which is why it dominates; conversion gain is not the reason.

**The Gilbert cell.** An active mixer first converts the RF voltage to a current with a transconductor $g_m$, then steers that current with a switching quad driven by the LO into load resistors $R_L$. Gilbert's 1968 four-quadrant multiplier is the bipolar original [1]. With hard switching, the output current is $g_mv_{RF}\,s(t)$ and the voltage conversion gain is

$$
G_c = \frac2\pi\,g_mR_L ,
$$

which can exceed unity, unlike the passive mixer. Its costs are the transconductor's noise and nonlinearity, the switches' noise during the LO transitions and their flicker noise, which falls at DC in a zero-IF receiver.

**Passive mixers and transparency.** A passive mixer (MOS switches, no DC current) has no gain and no flicker noise from the switches, and is very linear. But it has no reverse isolation: "the mixer reflects the baseband impedance to the RF and vice versa through simple frequency shifting" [3]. A low baseband impedance therefore appears at RF as a low impedance near $f_{LO}$, which current-mode receivers exploit and which leads directly to the N-path filter (§3.8).

### 3.3 Noise in mixers

**SSB and DSB.** A mixer converts noise from both the signal band and the image band to the IF. If the signal occupies only one band (as in a superheterodyne), the image band's noise is extra: the **single-sideband** (SSB) noise figure counts it. If the signal occupies both bands (as in a zero-IF receiver, where the "image" is the signal's own other half), the **double-sideband** (DSB) noise figure does not. For equal conversion gain in both bands, an otherwise noiseless mixer has an SSB noise figure of 3 dB and a DSB noise figure of 0 dB, and in general $\text{NF}_{SSB} \approx \text{NF}_{DSB} + 3$ dB.

**Noise folding.** A switching mixer converts the source's noise from *every* band it responds to: the signal band, the image and the bands around $3f_{LO}$, $5f_{LO}$ and so on. Multiplying white noise by a $\pm1$ square wave leaves it white with the same density, because $s^2(t) = 1$. The wanted signal, meanwhile, is converted with power gain $(2/\pi)^2$. Without a filter before the mixer, an otherwise noiseless switching mixer therefore degrades the signal-to-noise ratio by

$$
\frac{1}{(2/\pi)^2} = \frac{\pi^2}{4} = 3.92\ \text{dB} \quad\text{(SSB)},
$$

of which the image accounts for 3 dB and the odd harmonics for the rest: summed over both sidebands of every odd harmonic, the power conversion gains total $2\sum_{n\ \text{odd}}(2/n\pi)^2 = 1$, as $s^2 = 1$ requires, and the fundamental's two bands take $2 \times 4/\pi^2$ = 0.811 of that, the higher harmonics the remaining 0.189 (Example 21-05.4). How the 3.92 dB is split between the image and the harmonics depends on which bands are removed first, because noise-factor contributions add in linear units, not in decibels: removing the image first credits it with 3 dB, removing the harmonics first credits them with 1.67 dB (Example 21-05.4). This is why a band filter (or a tuned LNA load that is itself band-limited) sits ahead of the mixer. Gain alone does not help: an LNA's amplified noise in the image and harmonic bands folds just the same.

**Passive mixers: NF ≈ conversion loss.** A passive mixer at room temperature behaves like an attenuator, whose noise figure equals its loss (17-02). Mini-Circuits' MDB-24H+ diode mixer specifies a 6.9 dB conversion loss and a 6.9 dB noise figure at 5 GHz [10].

### 3.4 Linearity, LO leakage and self-mixing

A mixer's IIP3 is set by its transconductor (active) or by how hard and how cleanly the switches switch (passive). Passive diode mixers buy linearity with LO drive: the same Mini-Circuits family gives IP3 of 15 dBm with a +7 dBm LO and 23 dBm with a +17 dBm LO (Example 21-05.6) [10].

In a zero-IF receiver, three effects land at DC, on top of the wanted signal [5, 6]:

- **LO leakage and self-mixing.** LO power that leaks to the mixer's RF port (or radiates from the antenna and returns) mixes with the LO itself and produces a DC offset, which can be far larger than the wanted signal and changes with the environment.
- **Second-order distortion.** Mismatch between the two halves of a balanced mixer lets even-order terms through, so the envelope of a strong blocker, or the IM2 product of two blockers, appears at DC (21-03 §3.5).
- **Flicker noise** of active switches and of the baseband amplifiers adds most where the zero-IF signal lives.

LO leakage also radiates from the antenna, which regulators limit; data sheets specify it as LO–RF isolation, which varies strongly across the band (§9).

### 3.5 Image rejection with quadrature mixers

Hartley's architecture mixes the RF with two LOs in quadrature, shifts one IF path by 90°, and adds: the wanted signal adds in phase in the two paths and the image adds in antiphase and cancels. Let the Q path have a relative gain $1 + \varepsilon$ and a phase error $\theta$ against the I path. Then the wanted signal's output is proportional to $\lvert 1 + (1 + \varepsilon)e^{j\theta}\rvert$ and the image's to $\lvert 1 - (1 + \varepsilon)e^{j\theta}\rvert$, so the **image-rejection ratio** is

$$
\text{IRR} = \frac{1 + 2(1 + \varepsilon)\cos\theta + (1 + \varepsilon)^2}{1 - 2(1 + \varepsilon)\cos\theta + (1 + \varepsilon)^2} \approx \frac{4}{\varepsilon^2 + \theta^2}
$$

for small errors ($\theta$ in radians): expand $\cos\theta \approx 1 - \theta^2/2$, and the denominator becomes $\varepsilon^2 + \theta^2$ to second order while the numerator is about 4. A 1% gain error and 1° phase error give 40 dB; 2% and 2° give 33.9 dB (Example 21-05.3). Achieving **60** dB needs errors near 0.1% and 0.1°, which in practice means calibration, or a very careful low-IF polyphase design [7]. Weaver's architecture replaces the 90° IF shift with a second quadrature mixing stage [8].

![Contour map of image-rejection ratio against gain error from 0 to 5 percent and phase error from 0 to 5 degrees: nested quarter-circle-like contours at 50, 45, 40, 35 and 30 dB around the origin, with the point at 1 percent and 1 degree on the 40 dB contour and Example 21-05.3's point at 2 percent and 2 degrees between the 35 and 30 dB contours](../../../assets/figures/21-05/irr.svg)

*Figure 2. Image rejection against I/Q mismatch (exact formula). Each 6 dB more rejection halves the allowed errors.*

### 3.6 Harmonic-reject mixers

A wideband receiver cannot always filter $3f_{LO}$ and $5f_{LO}$. Combine three square-wave LOs, shifted by −45°, 0 and +45°, with weights 1, $\sqrt2$, 1. The $n$-th harmonic of the composite LO is proportional to

$$
\frac1n\left[\sqrt2 + 2\cos\left(n\cdot 45°\right)\right],
$$

whose bracket equals $2\sqrt2$ for $n$ = 1 and 7 but **zero** for $n$ = 3 and 5 ($2\cos 135° = 2\cos 225° = -\sqrt2$). The composite LO approximates a sinusoid sampled at eight phases, so the first uncancelled harmonics are the 7th and 9th (at 1/7 and 1/9 of the fundamental). ![Left: one LO period of a square wave and of the harmonic-reject composite LO, which steps through four levels (±1 and ±0.414 of its peak) and approximates a sine wave; right: bar chart of odd harmonic amplitudes relative to the fundamental, 1, 0.33, 0.2, 0.14 and 0.11 for the square wave and 1, 0, 0, 0.14 and 0.11 for the harmonic-reject LO](../../../assets/figures/21-05/hr-lo.svg)

*Figure 3. The harmonic-reject LO is a staircase approximation of a sinusoid: its 3rd and 5th harmonics vanish, its 7th and 9th equal the square wave's.*

Weldon and colleagues used harmonic-reject mixers to remove a transmitter's discrete IF filter [4]. The cancellation is only as good as the weights and phases match: a 1% error in the $\sqrt2$ weight leaves the 3rd-harmonic response at −55.6 dB, and a 1° phase error at about −44 dB (Example 21-05.7). Published designs reach more than 60 dB across chips with a second rejection stage, and further with digital cancellation [4].

### 3.7 Conversion gain of a hard-switched transconductor, revisited

The factor $2/\pi$ assumes instantaneous switching. With a finite LO amplitude, the switching pair spends part of each period in its linear region, where it splits the current and passes noise from both switches to the output. Larger LO swings sharpen the transitions and approach $2/\pi$; smaller ones lose gain and add noise, which is the active-mixer counterpart of the passive mixer's LO-drive/linearity trade.

### 3.8 N-path filters: mixers as filters

Connect $N$ capacitors $C$, one at a time in rotation, to a node fed from a source resistance $R_s$, each for $1/N$ of the LO period. A signal at $f_{LO}$ meets each capacitor at the same phase of its cycle every period, so each capacitor charges toward the average of the input over its window and holds it: the node voltage reproduces the input. A signal far from $f_{LO}$ meets each capacitor at a different phase each period and averages to zero. The structure is a band-pass filter centred on $f_{LO}$, tunable by the clock [9].

**Bandwidth.** Each capacitor is connected to $R_s$ only a fraction $1/N$ of the time, so its effective time constant is $NR_sC$. When $NR_sC \gg 1/f_{LO}$, each capacitor behaves as a low-pass filter at baseband with corner $1/(2\pi NR_sC)$; translated to RF it becomes a band-pass filter of full width

$$
\text{BW}_{3\,\text{dB}} = \frac{1}{\pi NR_sC} .
$$

**Centre loss.** A capacitor holds the average of $A\cos\omega_{LO}t$ over a window of $2\pi/N$, which is $A\,\text{sinc}$-weighted by $(N/\pi)\sin(\pi/N)$; the node voltage is then a staircase of those held values, whose fundamental is again $(N/\pi)\sin(\pi/N)$ times the held amplitude. The voltage gain at the centre is

$$
\left[\frac N\pi\sin\frac\pi N\right]^2 ,
$$

0.811 (−1.82 dB) for $N$ = 4 and −0.45 dB for $N$ = 8. Both results come from averaging and are confirmed by a time-domain simulation of the switched circuit (Example 21-05.8). The same clock-defined selectivity, built into the mixer, gives the "mixer-first" receivers of §9 their blocker tolerance.

## 4. Worked examples

Unless stated, mixers are ideal hard-switched double-balanced commutators, and conversion gains are voltage ratios.

### Example 21-05.1 · A frequency plan (tier A)

**Setup.** A 2.45 GHz signal is downconverted with a 2.40 GHz LO. Find the IF, the image and the responses through the LO's 3rd harmonic, and the conversion gains for the fundamental, 3rd and 5th harmonics.

**Solution.**

- IF = 2.45 − 2.40 = **0.05** GHz (50 MHz); image $2f_{LO} - f_{RF}$ = **2.35** GHz.
- The 3rd harmonic (7.20 GHz) converts inputs at **7.15** and **7.25** GHz to 50 MHz.
- Conversion gains: $2/\pi$ = **−3.92** dB, $2/(3\pi)$ = **−13.46** dB, $2/(5\pi)$ = **−17.90** dB.

**Units check.** Frequencies in GHz; gains as voltage ratios in dB ($20\log_{10}$).

**Sanity check.** The image is only 100 MHz from the wanted signal, a 4% offset at 2.4 GHz: an RF filter cannot reject it well, which is why low-IF and zero-IF receivers use quadrature mixing instead.

### Example 21-05.2 · Gilbert-cell conversion gain (tier A)

**Setup.** A Gilbert mixer has a transconductance of 20 mS and 500 Ω loads. Find its conversion gain.

**Solution.** $G_c = (2/\pi)(0.02)(500)$ = **6.37**, or **16.1** dB.

**Units check.** S × Ω is dimensionless.

**Sanity check.** The same $g_mR_L$ without switching would give a gain of 10; commutation costs the factor $2/\pi$, 3.9 dB.

### Example 21-05.3 · An image-rejection budget (tier B)

**Setup.** (a) What IRR do a 2% gain error and a 2° phase error give, exactly and from the small-error formula? (b) With a 0.5% gain error, what phase error still gives 40 dB?

**Solution.**

- (a) Exact: **33.95** dB; approximation $10\log_{10}[4/(0.02^2 + 0.0349^2)]$ = **33.93** dB.
- (b) Solving the exact expression for 40 dB with $\varepsilon$ = 0.005 gives $\theta$ = **1.11**°.

**Units check.** $\theta$ in radians inside the approximation.

**Sanity check.** At 40 dB the budget is $\varepsilon^2 + \theta^2 = 4 \times 10^{-4}$; the gain error uses $2.5 \times 10^{-5}$ of it, leaving $\theta \approx 0.0194$ rad, about 1.1°.

### Example 21-05.4 · Noise folding in a switching mixer (tier B)

**Setup.** A noiseless double-balanced switching mixer is driven by a source whose noise is white over all frequencies. Find its SSB noise figure with no filter before it, its DSB noise figure, and its SSB noise figure if a filter removes only the image band.

**Solution.** The output noise density equals the input's (because $s^2 = 1$); the wanted signal is converted with power gain $4/\pi^2$ = 0.405.

- SSB, no filter: $\text{NF} = 10\log_{10}(\pi^2/4)$ = **3.92** dB.
- DSB (signal in both fundamental bands): $10\log_{10}(\pi^2/8)$ = **0.91** dB.
- Image removed, harmonics not: the IF noise comes from the signal band (0.405) and the harmonic bands ($1 - 2 \times 0.405$ = **0.189**), so $\text{NF} = 10\log_{10}[(0.405 + 0.189)/0.405]$ = **1.67** dB.

**Units check.** All power ratios.

**Sanity check.** Removing the image saves **2.26** dB; the remaining 1.67 dB is the harmonics' share, which only a filter or a harmonic-reject LO removes.

### Example 21-05.5 · A passive mixer in a receiver (tier B)

**Setup.** An LNA (15 dB gain, NF 1.5 dB) drives a passive mixer (conversion loss 6.9 dB, NF 6.9 dB) through an image-reject filter that removes the image and LO-harmonic bands, followed by an IF amplifier (NF 3 dB). Find the cascade NF, and the NF without the LNA.

**Solution.**

- With the LNA: $F = 1.413 + (4.898 - 1)/31.62 + (1.995 - 1)/(31.62 \times 0.204)$ = 1.690, NF = **2.28** dB.
- Without it: the mixer's loss counts in full and the IF amplifier's noise is multiplied by it: NF = $6.9 + 3.0$ = **9.9** dB.

**Units check.** Gains and noise factors as ratios; the mixer's gain is 1/4.898.

**Sanity check.** The passive mixer's loss acts like a 6.9 dB attenuator; 15 dB of LNA gain in front reduces its effect from 9.9 dB to under 1 dB.

### Example 21-05.6 · LO drive buys linearity (tier B)

**Setup.** Two diode mixers in the same family have IP3 of 15 dBm (+7 dBm LO) and 23 dBm (+17 dBm LO). Two −20 dBm tones arrive. Find the IM3 level of each in dBc.

**Solution.** IM3 = $-2(\text{IP3} - P_{in})$: **−70** dBc with the +7 dBm LO and **−86** dBc with the +17 dBm LO.

**Units check.** dBm − dBm = dB.

**Sanity check.** Ten decibels more LO power buys 8 dB of intercept and 16 dB less IM3, but the LO chain must now deliver **50** mW.

### Example 21-05.7 · A harmonic-reject LO and its mismatch (tier C)

**Setup.** Combine square-wave LOs at −45°, 0 and +45° with weights 1, $\sqrt2$, 1. Find the 3rd, 5th and 7th harmonic responses relative to the fundamental, ideally, with a 1% error in the $\sqrt2$ weight, and with a 1° error in the +45° phase.

**Solution** (FFT of the composite LO):

- Ideal: the 3rd and 5th vanish; the 7th is 1/7, **−16.90** dB.
- 1% weight error: 3rd at **−55.6** dB, 5th at **−60.0** dB.
- 1° phase error: 3rd at **−44.2** dB, 5th at **−44.2** dB.

**Units check.** Voltage ratios in dB.

**Sanity check.** A weight error $\delta$ leaves a 3rd-harmonic residue of $\sqrt2\,\delta/(3 \times 2\sqrt2) = \delta/6$, −55.6 dB for 1%; phase errors hurt more because they break both cancellations.

### Example 21-05.8 · An N-path band-pass filter (tier C)

**Setup.** A 4-path filter at 1 GHz has $R_s$ = 50 Ω and C = 200 pF per path. Find its 3 dB bandwidth and centre loss, and the centre loss of an 8-path version.

**Solution.**

- $NR_sC$ = 40 ns, much longer than the 1 ns LO period, so the averaging result holds: BW = $1/(\pi \times 4 \times 50 \times 200\ \text{pF})$ = **7.96** MHz.
- Centre gain $[(4/\pi)\sin(\pi/4)]^2$ = 0.811: loss **1.82** dB. For N = 8: **0.45** dB.
- A time-domain simulation of the switched circuit gives −1.82 dB at the centre and −3.0 dB relative to the centre at ±3.98 MHz (§5).

**Units check.** Ω × F = s; 1/s = Hz.

**Sanity check.** A 0.8% bandwidth at 1 GHz, set by a clock and two passive components: a Q of about **126** without an inductor.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 21-05.1a | IF | 0.05 | GHz |
| Ex 21-05.1b | image | 2.35 | GHz |
| Ex 21-05.1c | 3rd-harmonic response, low | 7.15 | GHz |
| Ex 21-05.1d | 3rd-harmonic response, high | 7.25 | GHz |
| Ex 21-05.1e | fundamental conversion gain | −3.92 | dB |
| Ex 21-05.1f | 3rd-harmonic conversion gain | −13.46 | dB |
| Ex 21-05.1g | 5th-harmonic conversion gain | −17.90 | dB |
| Ex 21-05.2a | Gilbert conversion gain | 6.37 | — |
| Ex 21-05.2b | Gilbert conversion gain | 16.1 | dB |
| Ex 21-05.3a | IRR exact, 2 % and 2° | 33.95 | dB |
| Ex 21-05.3b | IRR approximate | 33.93 | dB |
| Ex 21-05.3c | phase error for 40 dB at 0.5 % | 1.11 | ° |
| Ex 21-05.4a | SSB NF, no filter | 3.92 | dB |
| Ex 21-05.4b | DSB NF | 0.91 | dB |
| Ex 21-05.4c | harmonic share of the noise | 0.189 | — |
| Ex 21-05.4d | SSB NF, image filtered | 1.67 | dB |
| Ex 21-05.5a | cascade NF with LNA | 2.28 | dB |
| Ex 21-05.5b | NF without LNA | 9.9 | dB |
| Ex 21-05.6a | IM3 with +7 dBm LO | −70 | dBc |
| Ex 21-05.6b | IM3 with +17 dBm LO | −86 | dBc |
| Ex 21-05.7a | ideal 7th-harmonic response | −16.90 | dB |
| Ex 21-05.7b | 3rd, 1 % weight error | −55.6 | dB |
| Ex 21-05.7c | 5th, 1 % weight error | −60.0 | dB |
| Ex 21-05.7d | 3rd, 1° phase error | −44.2 | dB |
| Ex 21-05.7e | 5th, 1° phase error | −44.2 | dB |
| Ex 21-05.8a | 4-path bandwidth | 7.96 | MHz |
| Ex 21-05.8b | 4-path centre loss | 1.82 | dB |
| Ex 21-05.8c | 8-path centre loss | 0.45 | dB |
| Txt 21-05.a | 3rd-harmonic gain below the fundamental | 9.5 | dB |
| Txt 21-05.b | 5th-harmonic gain below the fundamental | 14 | dB |
| Txt 21-05.c | fundamental share of folded noise | 0.811 | — |
| Txt 21-05.d | IRR at 1 % and 1° | 40 | dB |
| Txt 21-05.e | 8-path centre gain | −0.45 | dB |
| Txt 21-05.f | NF saved by removing the image | 2.26 | dB |
| Txt 21-05.g | +17 dBm LO power | 50 | mW |
| Txt 21-05.h | N-path equivalent Q | 126 | — |
| Txt 21-05.i | IRR at 0.1 % and 0.1° | 60 | dB |

## 5. Simulate it

The lab ([labs/21-05-lab](../labs/21-05-lab/README.md)) collects the formulas in `mixer.py`, simulates switching mixers, noise folding and an N-path filter in the time domain, and confirms the commutating mixer's conversion gain and harmonic response with ngspice (`mixer.cir`).

**Predict, then run.**

1. Predict the IF spectrum when a 2.45 GHz tone and a 7.25 GHz tone enter a mixer driven by a 2.40 GHz square wave, then compute it with an FFT (Part 1).
2. Predict the conversion gain of an ideal commutating mixer for the fundamental and the 3rd harmonic, then run `ngspice -b mixer.cir` (Part 2).
3. Predict how much an unfiltered switching mixer degrades a signal's SNR, then multiply white noise by a square wave and measure it (Part 3).
4. Predict the IRR for a grid of gain and phase errors, then map it (Part 4).
5. Predict the harmonic responses of the three-phase harmonic-reject LO with and without errors, then compute them (Part 5).
6. Predict the bandwidth and centre loss of a 4-path filter, then simulate the switched circuit (Part 6).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Active (Gilbert) versus passive mixer | Active: conversion gain, isolation; passive: linearity, no switch flicker noise | Active: noise, power, linearity; passive: loss, transparency to baseband impedance | RF designer |
| LO drive level | Linearity, sharper switching, conversion gain | LO buffer power, LO leakage | RF designer and synthesizer designer |
| IF choice (high IF, low IF, zero IF) | High IF: image filtering; zero IF: no image, simple filtering | High IF: an image filter and a second conversion; zero IF: DC offset, flicker noise, IIP2 | Transceiver architect |
| Quadrature accuracy (layout, calibration) | Image rejection, I/Q balance | Area, calibration time and circuitry | RF designer and firmware |
| Harmonic-reject or 8-phase LO | Rejection of LO-harmonic responses without filters | More LO phases, clock power, matching | Wideband-radio architect |
| N-path / mixer-first front end | Clock-tunable selectivity, blocker tolerance | Clock power, noise figure | Front-end architect |

## 7. Numbers to know

| Quantity | Typical value | Note |
|---|---|---|
| Commutating mixer conversion gain | $2/\pi$ (−3.92 dB) single- and double-balanced; $1/\pi$ for a single-switch (0/1) mixer | Ideal hard switching |
| LO-harmonic responses | 3rd: −13.46 dB, 5th: −17.90 dB (9.5 and 14 dB below the fundamental) | Square-wave LO |
| Noise folding, noiseless switching mixer | SSB 3.92 dB unfiltered; 3 dB from the image alone | $s^2 = 1$ |
| Image rejection | $4/(\varepsilon^2 + \theta^2)$: 40 dB at 1% and 1°; "30–40 dB" typical on chip without calibration; 57–62 dB with calibration or special frequency plans | [2, 7, 12, 13] |
| Passive diode mixer | conversion loss about 5 dB, IP3 15 dBm at +7 dBm LO; 23 dBm at +17 dBm LO | Mini-Circuits ADE-1+/ADE-1H+ [10] |
| Passive mixer noise figure | about equal to its conversion loss (6.9 dB at 5 GHz) | Mini-Circuits MDB-24H+ [10] |
| Single-chip radar receiver image rejection | 30 dB | TI AWR1843 [R-373] |
| N-path filter | BW $= 1/(\pi NR_sC)$; centre loss 1.82 dB (N = 4), 0.45 dB (N = 8) | Ideal switches |

## 8. Common mistakes

- **Forgetting the image.** Every mixer converts two input bands to the same IF; plan where the image falls and how it is removed.
- **Using a sinusoidal-LO model for a switching mixer.** Real mixers respond at $3f_{LO}$, $5f_{LO}$, ... with gains of 1/3, 1/5 of the fundamental.
- **Comparing SSB and DSB noise figures.** They differ by about 3 dB; know which one a data sheet quotes and which your architecture needs.
- **Ignoring noise folding.** An unfiltered switching mixer adds noise from every harmonic band, even if the mixer itself is noiseless.
- **Quoting post-calibration image rejection as intrinsic.** Uncalibrated quadrature receivers typically reach 30–40 dB.
- **Reading typical isolation at mid-band.** LO leakage is worst at the band edges; use the minimum there.
- **Treating a passive mixer as a one-way device.** Its RF port sees the baseband impedance, frequency-shifted.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **The building blocks are classics [Established].** Gilbert's 1968 multiplier was "linear on both inputs and useful from dc to an upper frequency very close to the $f_T$ of the transistors", with precision "limited primarily by the matching of the transistors" [1]. Weaver published his third method of single-sideband generation and detection in 1956 [8]. Franks and Sandberg proposed the N-path filter in 1960 [9].
- **Zero-IF won, and its problems are understood [Established].** Abidi's and Razavi's analyses identified DC offsets, I/Q mismatch, even-order distortion, flicker noise and LO leakage as the costs of direct conversion [5, 6]. A 2023 5G receiver front end reports "calibration-free IIP2 of more than 59 dBm" with a 3.5 dB noise figure [R-375].
- **Passive current-mode mixers dominate CMOS receivers [Established].** Mirzaei and colleagues analysed how the passive mixer "reflects the baseband impedance to the RF" and how I/Q interaction "results in different high- and low-side conversion gains, and unexpected IIP2 and IIP3 values" [3]. The Blixer used a 25% duty-cycle LO to halve the switches' DC drop and double the IF impedance [14].
- **Image rejection: 30–40 dB typical uncalibrated, 57–62 dB with calibration or special designs [Established per paper].** A Berkeley course quotes typical on-chip values of "30-40 dB achieved (< 5°, < 0.6 dB)" [13]; the exact formula gives about 25 dB at that corner. Der and Razavi reported 57 dB after LMS calibration [7]; Behbahani and colleagues reached 60 dB "without trimming or calibration" at low IF with careful polyphase filters [7]; a single-chip radar specifies 30 dB [R-373]; placing the image around zero frequency reached 62 dB [12].
- **Harmonic rejection and N-path selectivity replace filters in wideband radios [Established].** Ru and colleagues reported more than 60 dB of harmonic rejection for the 2nd to 6th harmonics "over 40 chips", with digital cancellation adding more [4]. Ghaffari's 4-path filters are tunable from 0.1 to 1 GHz with IIP3 above 14 dBm and a noise figure of 3–5 dB, using 2–16 mW of clock power [9]. Andrews and Molnar's mixer-first receiver showed "NF as low as 3 dB, and 25 dBm out-of-band IIP3" from 0.1 to 1.3 GHz [11], and a 2024 design reached more than 20 dBm adjacent-channel IIP3 below 25 mW [11]. At millimetre waves, a 2025 survey puts mixer-first receivers at "13 to 89mW and 8 to 20dB", noting that "there are no SAW-equivalent filters available at these frequencies" [11].

### Why it matters commercially

- **Mixers decide what a radio can coexist with.** A phone's cellular receiver must tolerate its own transmitter and nearby Wi-Fi; harmonic responses and IIP2 set which band combinations work, and therefore which carrier-aggregation combinations a modem can claim (21-09).
- **Software-defined and wideband radios** (instrumentation, base stations, satellite terminals) replace banks of fixed filters with harmonic-reject and N-path techniques, saving board area and cost.
- **LO power is a hidden budget.** Passive mixers' linearity is bought with LO drive, which a synthesizer and its buffers must supply on every path of a MIMO radio.

### Marketing vs Reality

- **"High IP3."** For passive mixers it is bought with LO power that is not on the mixer's own line: moving from a +7 dBm to a +17 dBm LO raises the Mini-Circuits family's IP3 from 15 to 23 dBm and its P1dB from +1 to +14 dBm [10]. Ask what drives a +17 dBm LO, and at what power.
- **"60 dB image rejection."** Almost always after calibration or with a special frequency plan [7]; the uncalibrated value is set by matching, typically 30–40 dB. Ask for both, and for the calibration's drift over temperature.
- **"Excellent isolation."** The ADE-1+ data sheet gives LO–IF isolation of 65 dB typical in its lowest band but 30 dB typical and 20 dB minimum in its upper band [10]. Read the band-edge minimum.
- **"Passive, so noiseless."** A passive mixer's noise figure is about its loss: 6.9 dB for 6.9 dB at 5 GHz [10].
- **"LNA-less mixer-first receiver."** It moves the cost rather than removing it: excellent linearity and tunable selectivity, but clock power and, at millimetre waves, noise figures of 8 to 20 dB [11].

### Questions for engineering leaders

1. **"What is your IIP2 before and after calibration, and how stable is the calibration over temperature?"** *Strong:* numbers both ways, a drift plan, and the transmitter-leakage scenario that sets the requirement. *Evasive:* "We calibrate it."
2. **"What image rejection or I/Q accuracy do you get without calibration, and what sets it?"** *Strong:* a gain and phase error budget mapped to IRR with $4/(\varepsilon^2 + \theta^2)$, the quadrature LO source and the layout symmetry. *Evasive:* quotes only the calibrated 60 dB.
3. **"Where does the LO power go, and what is your LO leakage at the antenna?"** *Strong:* LO drive and buffer power, isolation at the band-edge minimum, and the regulatory emission limit. *Evasive:* mid-band typical isolation.
4. **"How do you handle the LO's 3rd and 5th harmonics in a wideband receiver?"** *Strong:* harmonic-reject or 8-phase LO with rejection quantified over many chips, plus a pre-filter plan. *Evasive:* "The SAW filter takes care of it."
5. **"Why a passive (or active) mixer here?"** *Strong:* discusses transparency, noise figure versus conversion loss, flicker noise for zero-IF, and LO duty cycle. *Evasive:* "Passive is more linear."

## 10. Concept check

**Q1.** Why can't a mixer distinguish the wanted signal from its image once both are at the IF?

<details><summary>Answer</summary>

Mixing shifts both inputs to the same frequency, $\lvert f_{RF} - f_{LO}\rvert$, so they occupy the same IF band; any later filter treats them identically. The image must be removed before the mixer or cancelled by combining two quadrature paths.

</details>

**Q2.** Why does a commutating mixer have a conversion gain of $2/\pi$ rather than 1/2 or 1?

<details><summary>Answer</summary>

It multiplies by a ±1 square wave, whose fundamental has amplitude $4/\pi$; mixing with a cosine of amplitude $4/\pi$ puts half of that, $2/\pi$, into the difference frequency. A sinusoidal multiplier with unit LO would give 1/2.

</details>

**Q3.** Why does a switching mixer respond to signals near $3f_{LO}$, and how strongly?

<details><summary>Answer</summary>

The square-wave LO contains a 3rd harmonic of amplitude $4/(3\pi)$, which converts inputs at $3f_{LO} \pm f_{IF}$ to the IF with gain $2/(3\pi)$, one third of the fundamental's (9.5 dB weaker).

</details>

**Q4.** What limits image rejection in a quadrature receiver, and roughly how much do 1% and 1° buy?

<details><summary>Answer</summary>

Mismatch between the I and Q paths: gain error ε and phase error θ leave a residue, IRR ≈ $4/(\varepsilon^2 + \theta^2)$, about 40 dB for 1% and 1°.

</details>

**Q5.** Why is a passive mixer's noise figure about equal to its conversion loss?

<details><summary>Answer</summary>

At room temperature a passive, lossy two-port behaves like an attenuator: its noise factor equals its loss (17-02). The switches add little noise of their own.

</details>

**Q6.** Why does an N-path filter's bandwidth depend on N, R and C but its centre frequency only on the clock?

<details><summary>Answer</summary>

Each capacitor is connected to the source a fraction 1/N of the time, so it low-pass filters at a corner of $1/(2\pi NR_sC)$ at baseband; the switching translates that low-pass response to a band-pass response centred on the switching frequency.

</details>

Problems: [21-05 problem set](../problems/21-05-problems.md) · Worked solutions: [21-05 solutions](../solutions/21-05-solutions.md)

## 11. Key terms

[Mixer](../../../reference/glossary.md#mixer) · [Local oscillator (LO)](../../../reference/glossary.md#local-oscillator-lo) · [Image frequency](../../../reference/glossary.md#image-frequency) · [Mixer conversion gain](../../../reference/glossary.md#mixer-conversion-gain) · [Gilbert cell](../../../reference/glossary.md#gilbert-cell) · [Image-rejection ratio (IRR)](../../../reference/glossary.md#image-rejection-ratio-irr) · [Harmonic-reject mixer](../../../reference/glossary.md#harmonic-reject-mixer) · [Noise folding](../../../reference/glossary.md#noise-folding) · [N-path filter](../../../reference/glossary.md#n-path-filter)

## 12. Connections

- **Builds on:** [11-05](../../11-signals-and-systems/chapters/11-05-fourier-series.md) (square-wave Fourier series), [11-11](../../11-signals-and-systems/chapters/11-11-modulation-and-filtering-applications.md) (frequency shifting), [21-03](21-03-noise-figure-and-linearity.md) (NF, IIP2/IIP3), [21-04](21-04-low-noise-amplifiers.md) (the stage before the mixer).
- **Next:** [21-06](21-06-oscillators-and-vcos.md) builds the local oscillator whose phase noise the mixer multiplies in.
- **Used later:** architectures in [21-08](21-08-transceiver-architectures.md), front-end coexistence in [21-09](21-09-rf-front-end.md).

## 13. Further study

- B. Razavi, *RF Microelectronics*, 2nd ed., Prentice Hall, 2012: the mixer chapter and the transceiver-architecture chapter (image-reject and zero-IF receivers).
- T. H. Lee, *The Design of CMOS Radio-Frequency Integrated Circuits*, 2nd ed., Cambridge University Press, 2004: the mixer chapter.
- A. Ghaffari et al. [9] for a clear model of N-path filters, and C. Andrews and A. C. Molnar [11] for the mixer-first receiver.

## 14. Sources

1. B. Gilbert, "A precise four-quadrant multiplier with subnanosecond response," *IEEE J. Solid-State Circuits*, vol. 3, no. 4, pp. 365–373, Dec. 1968, DOI 10.1109/JSSC.1968.1049925 [R-374].
2. B. Razavi, *RF Microelectronics*, 2nd ed., Prentice Hall, 2012.
3. A. Mirzaei, H. Darabi, J. C. Leete, X. Chen, K. Juan and A. Yazdi, "Analysis and optimization of current-driven passive mixers in narrowband direct-conversion receivers," *IEEE J. Solid-State Circuits*, vol. 44, no. 10, pp. 2678–2688, Oct. 2009, DOI 10.1109/JSSC.2009.2027937 [R-374].
4. J. A. Weldon et al., "A 1.75-GHz highly integrated narrow-band CMOS transmitter with harmonic-rejection mixers," *IEEE J. Solid-State Circuits*, vol. 36, no. 12, pp. 2003–2015, Dec. 2001, DOI 10.1109/4.972151; Z. Ru, N. A. Moseley, E. Klumperink and B. Nauta, "Digitally enhanced software-defined radio receiver robust to out-of-band interference," *IEEE J. Solid-State Circuits*, vol. 44, no. 12, pp. 3359–3375, Dec. 2009, DOI 10.1109/JSSC.2009.2032272 [R-374].
5. A. A. Abidi, "Direct-conversion radio transceivers for digital communications," *IEEE J. Solid-State Circuits*, vol. 30, no. 12, pp. 1399–1410, Dec. 1995, DOI 10.1109/4.482187 [R-367].
6. B. Razavi, "Design considerations for direct-conversion receivers," *IEEE Trans. Circuits Syst. II*, vol. 44, no. 6, pp. 428–435, Jun. 1997, DOI 10.1109/82.592569 [R-367].
7. F. Behbahani, Y. Kishigami, J. Leete and A. A. Abidi, "CMOS mixers and polyphase filters for large image rejection," *IEEE J. Solid-State Circuits*, vol. 36, no. 6, pp. 873–887, Jun. 2001, DOI 10.1109/4.924850; L. Der and B. Razavi, "A 2-GHz CMOS image-reject receiver with LMS calibration," *IEEE J. Solid-State Circuits*, vol. 38, no. 2, pp. 167–175, Feb. 2003, DOI 10.1109/JSSC.2002.807407 [R-375].
8. D. Weaver, "A third method of generation and detection of single-sideband signals," *Proc. IRE*, vol. 44, no. 12, pp. 1703–1705, Dec. 1956, DOI 10.1109/JRPROC.1956.275061 [R-374].
9. L. E. Franks and I. W. Sandberg, "An alternative approach to the realization of network transfer functions: The N-path filter," *Bell Syst. Tech. J.*, vol. 39, no. 5, pp. 1321–1350, Sep. 1960, DOI 10.1002/j.1538-7305.1960.tb03962.x; A. Ghaffari, E. A. M. Klumperink, M. C. M. Soer and B. Nauta, "Tunable high-Q N-path band-pass filters: Modeling and verification," *IEEE J. Solid-State Circuits*, vol. 46, no. 5, pp. 998–1010, May 2011, DOI 10.1109/JSSC.2011.2117010 [R-374].
10. Mini-Circuits data sheets: ADE-1+ and ADE-1H+ (Rev. G, 2020), MDB-24H+ (Rev. A, 2021) [R-376].
11. C. Andrews and A. C. Molnar, "A passive mixer-first receiver with digitally controlled and widely tunable RF interface," *IEEE J. Solid-State Circuits*, vol. 45, no. 12, pp. 2696–2708, Dec. 2010, DOI 10.1109/JSSC.2010.2077151; S. van Zanten, R. van der Zee and B. Nauta, ISSCC 2024, paper 5.5, DOI 10.1109/ISSCC49657.2024.10454419; A. G. Gadelkarim and P. Mercier, ISSCC 2025, paper 5.10, DOI 10.1109/ISSCC49661.2025.10904619 [R-375].
12. B. Razavi, *Symp. VLSI Circuits*, 2000, DOI 10.1109/VLSIC.2000.852844 (62 dB with the image placed around zero frequency) [R-375].
13. A. Niknejad, EECS 242 lecture "Receiver Architectures," UC Berkeley, PDF dated 5 Feb 2009 [R-375].
14. S. C. Blaakmeer, E. A. M. Klumperink, D. M. W. Leenaerts and B. Nauta, "The Blixer, a wideband balun-LNA-I/Q-mixer topology," *IEEE J. Solid-State Circuits*, vol. 43, no. 12, pp. 2706–2715, Dec. 2008, DOI 10.1109/JSSC.2008.2004866 [R-374].
