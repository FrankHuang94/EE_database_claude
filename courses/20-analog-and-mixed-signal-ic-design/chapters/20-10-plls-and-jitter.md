<!-- status: verified -->
# 20-10 · PLLs and Jitter

| | |
|---|---|
| **Course** | [20 · Analog and Mixed-Signal IC Design](../README.md) |
| **University equivalent** | The frequency-synthesis material of a graduate analog/RF IC course: charge-pump PLLs and their loop dynamics, phase noise and jitter, integer-N and fractional-N synthesis, all-digital PLLs (Razavi, *Design of CMOS Phase-Locked Loops*; Banerjee, *PLL Performance, Simulation and Design*) |
| **Prerequisites** | [15-12](../../15-control-systems/chapters/15-12-control-applications-pll-regulators-thermal.md) (a first look at PLL loops), [15-07](../../15-control-systems/chapters/15-07-frequency-domain-design.md) (phase margin), [20-05](20-05-comparators-and-sample-and-hold.md) (sampling jitter), [20-08](20-08-sigma-delta-converters.md) (ΔΣ modulation) |
| **Estimated study hours** | 10 |
| **Last verified** | 2026-11-24 |

**Learning objectives.** After this chapter you can:

1. Build the phase-domain model of a charge-pump PLL and derive its open-loop gain, natural frequency, damping and phase margin.
2. Design a third-order loop filter for a chosen bandwidth and phase margin, and predict lock settling.
3. Explain how each noise source reaches the output (low-pass for the reference, high-pass for the VCO) and why reference noise grows by $20\log_{10}N$.
4. Convert phase noise to rms jitter and use the result to budget an ADC clock or a link.
5. Explain fractional-N synthesis with a ΔΣ-modulated divider, compute its noise and recognize its spurs.
6. Compare PLL architectures by their figures of merit, including all-digital PLLs limited by TDC resolution.

## 1. Big picture

Every synchronous chip needs clocks at frequencies its crystal cannot provide, and every radio needs local oscillators tunable in fine steps. A **phase-locked loop** (PLL) makes both: it locks a voltage- or digitally-controlled oscillator to a multiple of a clean reference, so the output inherits the reference's long-term accuracy and the oscillator's speed. The PLL's quality is measured by **jitter** in the time domain and **phase noise** in the frequency domain, and that quality sets the limits of systems far beyond the PLL itself.

- **Processors and SoCs** use ring-oscillator PLLs for core and memory clocks; jitter costs timing margin (19-10).
- **SerDes and optical links** in AI datacenters recover and generate clocks at tens of gigahertz; jitter sets bit-error rates.
- **Data converters** need sampling clocks whose jitter limits SNR at high input frequency (20-05): −20 log₁₀(2πf_inσ_t).
- **Radios and radar** need low-phase-noise local oscillators; automotive FMCW radar generates its chirps with fractional-N PLLs.
- **Microcontrollers** multiply a crystal or an internal RC oscillator to the core clock (18-01) with small, low-power PLLs or frequency-locked loops.

## 2. Intuition first

```text
 f_ref ──►[ PFD ]──► [ charge pump ] ──► [ loop filter ] ── V_ctrl ──► [ VCO ] ──┬──► f_out = N · f_ref
            ▲  phase error   ±I_cp pulses       R, C1, C2                        │
            └───────────────────────────── [ ÷ N ] ◄─────────────────────────────┘
```

*Figure 1. A charge-pump PLL. The phase-frequency detector compares the reference with the divided output; the charge pump turns the phase error into current pulses; the loop filter integrates them into the VCO's control voltage.*

**A metronome analogy, and its limits.** A drummer (the VCO) plays four beats for every click of a metronome (the reference). The drummer cannot hear absolute time, only whether the fourth beat lands before or after the click, and nudges the tempo accordingly. Small, steady corrections keep the drummer locked: the drummer's own wobble (VCO noise) is corrected over a few bars, while any wobble of the metronome itself is copied, magnified four times in beat-sized units (reference noise multiplied by N). Correct too aggressively and the drummer overshoots and oscillates around the beat (low phase margin); correct too gently and every drifting tendency persists (narrow loop bandwidth). The analogy breaks in two places: a PLL compares phase only once per reference period, so it cannot react faster than the reference allows (§3.3), and its "nudges" are charge packets whose own noise and mismatches create noise and spurs that a drummer does not have.

## 3. Theory

> **Conventions.** Phases in radians; $K_{VCO}$ in rad/s per volt (so a VCO with 500 MHz/V has $K_{VCO} = 2\pi \times 500\text{ MHz/V}$); $I_{cp}$ is the charge-pump current; $N$ the divide ratio. $\mathcal{L}(f)$ is the single-sideband phase noise in dBc/Hz at offset $f$; for small phase deviations it equals the two-sided phase spectral density $S_\phi(f)$ in rad²/Hz.

### 3.1 The phase-domain model

**Phase-frequency detector and charge pump.** The PFD compares the edges of the reference and the divided output. If the reference leads by Δt, the charge pump sources $I_{cp}$ for Δt each period; if it lags, it sinks. Averaged over a reference period $T_{ref}$, the current is $I_{cp}\,\Delta t/T_{ref} = I_{cp}\,\theta_e/2\pi$, where $\theta_e = 2\pi\,\Delta t/T_{ref}$ is the phase error. The PFD-plus-pump gain is therefore $K_{PD} = I_{cp}/2\pi$ A/rad. Because the PFD also detects frequency (it keeps pumping one way when the frequencies differ), the loop acquires lock from any initial frequency within the VCO's range.

**VCO.** The VCO's frequency is $\omega_{free} + K_{VCO}V_{ctrl}$; its phase is the integral of frequency, so in the phase domain the VCO is an integrator, $\theta_{out} = K_{VCO}V_{ctrl}/s$.

**Divider.** It divides phase as well as frequency: $\theta_{fb} = \theta_{out}/N$.

With a loop-filter impedance $Z(s)$ (current in, voltage out), the open-loop gain is

$$
G(s) = \frac{I_{cp}}{2\pi}\,Z(s)\,\frac{K_{VCO}}{s}\,\frac{1}{N} ,
\qquad
\frac{\theta_{out}}{\theta_{ref}} = \frac{N\,G(s)}{1 + G(s)} .
$$

At low frequency $G \gg 1$ and the output phase follows $N$ times the reference phase; at high frequency $G \ll 1$ and the output is the free VCO.

### 3.2 Loop dynamics: second and third order

**Second order.** With $Z(s) = R + 1/(sC)$, $G(s) = \dfrac{I_{cp}K_{VCO}}{2\pi NC}\cdot\dfrac{1 + sRC}{s^2}$: two integrators (the capacitor and the VCO), so the loop is **type II** and has zero static phase error, even after a reference frequency step. The closed-loop transfer is

$$
\frac{\theta_{out}}{N\,\theta_{ref}} = \frac{2\zeta\omega_ns + \omega_n^2}{s^2 + 2\zeta\omega_ns + \omega_n^2},
\qquad
\omega_n = \sqrt{\frac{I_{cp}K_{VCO}}{2\pi NC}}, \qquad \zeta = \frac{R}{2}\sqrt{\frac{I_{cp}K_{VCO}C}{2\pi N}} ,
$$

obtained by matching $1 + G = 0$ to $s^2 + 2\zeta\omega_ns + \omega_n^2 = 0$ (15-12 derives the same form). The resistor creates the stabilizing zero; without it the two integrators would oscillate.

**Third order.** The resistor makes the control voltage jump by $I_{cp}R$ during each pump pulse, which modulates the VCO every reference period (reference spurs). A small capacitor $C_2$ across the filter smooths those jumps. The filter becomes

$$
Z(s) = \frac{1 + sRC_1}{s(C_1 + C_2)(1 + sRC_1C_2/(C_1 + C_2))} ,
$$

a zero at $\omega_z = 1/RC_1$ and a pole at $\omega_p = (C_1 + C_2)/(RC_1C_2)$, with ratio $b = \omega_p/\omega_z = 1 + C_1/C_2$. The open-loop phase is $-180° + \arctan(\omega/\omega_z) - \arctan(\omega/\omega_p)$, largest at $\omega = \sqrt{\omega_z\omega_p}$, where (using $\tan(A - B) = (\tan A - \tan B)/(1 + \tan A\tan B)$ with $\tan A = \sqrt b$, $\tan B = 1/\sqrt b$)

$$
\text{PM}_{max} = \arctan\frac{b - 1}{2\sqrt b} .
$$

**Design procedure.** Choose the crossover $\omega_c$ and $b$ for the phase margin (b = 10 gives 54.9°); place $\omega_z = \omega_c/\sqrt b$ and $\omega_p = \omega_c\sqrt b$; set $\lvert G(j\omega_c)\rvert = 1$ to find $C_1 + C_2$; then $C_1 = (C_1 + C_2)(b - 1)/b$ and $R = 1/(\omega_zC_1)$ (Example 20-10.2). The closed-loop response peaks slightly above 0 dB near crossover, and its −3 dB bandwidth is larger than the crossover frequency.

![Open-loop gain and phase of the example PLL from 10 kHz to 100 MHz: the gain falls at 40 dB per decade at low frequency, crosses 0 dB at 2 MHz and keeps falling; the phase rises from minus 180 degrees to a peak of about minus 125 degrees at 2 MHz between the zero at 632 kHz and the pole at 6.32 MHz, then returns towards minus 180](../../../assets/figures/20-10/bode.svg)

*Figure 2. The open loop of Example 20-10.2. Two integrators give −180° at low frequency; the zero lifts the phase and the ripple pole brings it back; placing the crossover at the geometric mean of the two gives the 54.9° maximum.*

### 3.3 Why the bandwidth stays well below the reference

The charge pump delivers its correction as a pulse once per reference period; the continuous-time model of §3.1 averages those pulses. That approximation holds only if the loop changes little during one period, so the crossover must sit far below $f_{ref}$. Gardner analyzed the sampled loop and found a stability limit that the continuous model misses [1]. In the form taught in a widely used ISSCC tutorial it reads $\omega_c < \omega_{ref}/[\pi(1 + \pi\omega_z/\omega_{ref})]$, which approaches $f_{ref}/\pi$ = **0.32** $f_{ref}$ when the zero is far below the reference [1]. Exact sampled-loop analysis of the third-order loop puts instability at a reference-to-bandwidth ratio of about 3 to 3.7, depending on phase margin [2], and Banerjee's design guide warns of instability near 28% of the phase-detector frequency [3]. The practical rule, followed by IC designers for decades, keeps the bandwidth below about a tenth of the reference frequency [2], [3]. A narrow bandwidth also filters the pump's periodic ripple, the source of reference spurs.

### 3.4 Phase noise and how it reaches the output

**Phase noise.** An oscillator's output $\cos(\omega_0t + \phi(t))$ has a random phase $\phi$. Its **single-sideband phase noise** $\mathcal{L}(f)$ is the noise power in a 1 Hz band at offset $f$ from the carrier, relative to the carrier, in dBc/Hz. For small $\phi$, $\mathcal{L}(f)$ equals the two-sided spectral density of $\phi$ in rad²/Hz. Standards bodies and instrument makers usually quote the one-sided density instead, and then $S_\phi(f) \approx 2\mathcal{L}(f)$ [9]: the same factor of 2 that appears in the jitter integral of §3.5.

**Oscillator noise.** A free-running oscillator's phase noise falls at −20 dB per decade over most offsets: white noise in its frequency integrates into phase (a random walk), so phase noise ∝ $1/f^2$. Leeson's model expresses this through the tank's quality factor Q: the noise is shaped by the resonator's half-bandwidth $f_0/2Q$, so a higher Q lowers phase noise. Close to the carrier, flicker noise steepens the slope to −30 dB per decade. The oscillator **figure of merit** normalizes for frequency, offset and power:

$$
\text{FoM}_{osc} = -\mathcal{L}(\Delta f) + 20\log_{10}\frac{f_0}{\Delta f} - 10\log_{10}\frac{P}{1\text{ mW}} ,
$$

so that a 5 GHz oscillator with −120 dBc/Hz at 1 MHz offset and 5 mW scores 187.0 dB (Example 20-10.7).

**Noise transfer.** Inject each noise source into the phase-domain model:

- **Reference, PFD, charge pump and divider** noise enters at the loop's input and reaches the output through $NG/(1 + G)$: multiplied by $N$ in band (a phase-noise increase of $20\log_{10}N$) and low-pass filtered beyond the loop bandwidth. A charge-pump current noise $i_n$ refers to the input as $i_n/(I_{cp}/2\pi)$ rad, so a larger pump current lowers it.
- **VCO noise** reaches the output through $1/(1 + G)$: suppressed in band, where the loop corrects it, and passed unchanged far outside.

The total output noise is the reference-path noise inside the bandwidth and the VCO's own noise outside it. The bandwidth that minimizes the integrated noise is roughly where $N^2$ times the input-referred noise crosses the VCO's noise (Example 20-10.4).

![Output phase noise against offset frequency for the example PLL: the reference contribution is flat near minus 110 dBc per hertz up to about 2 MHz, peaks slightly, then falls steeply; the VCO contribution rises from very low values to a peak near minus 125 dBc per hertz around 1.5 MHz and then follows the free-running VCO curve, falling at 20 dB per decade; the dashed total follows the reference in band and the VCO outside](../../../assets/figures/20-10/noise.svg)

*Figure 3. Noise transfer in the loop of Example 20-10.2: the reference (×N², low-pass) dominates in band, the VCO (high-pass) outside; the vertical line is the crossover.*

### 3.5 From phase noise to jitter

The rms phase deviation is the integral of the phase spectrum over the offsets of interest, $\sigma_\phi^2 = \int S_\phi\,df$ taken over positive and negative offsets, which equals $2\int_{f_1}^{f_2}\mathcal{L}(f)\,df$. The rms **jitter** is that phase expressed as time at the carrier:

$$
\sigma_t = \frac{\sigma_\phi}{2\pi f_0} = \frac{1}{2\pi f_0}\sqrt{2\int_{f_1}^{f_2}\mathcal{L}(f)\,df} .
$$

The integration limits matter: the lower limit sets how much slow wander counts as jitter, and the upper limit how much broadband noise. Data sheets quote jitter "integrated from 12 kHz to 20 MHz" or similar, and the band must match the application's (a link's clock-recovery bandwidth, an ADC's full bandwidth).

**Jitter flavors.** Absolute (or time-interval-error) jitter is the deviation of each edge from an ideal clock, the σ_t above. **Period jitter** is the deviation of each period from the mean; **cycle-to-cycle jitter** is the change between adjacent periods. A free-running oscillator's absolute jitter grows without bound (its phase is a random walk, so the timing error after a delay τ grows as $\sqrt\tau$); a PLL stops that growth beyond about $1/(2\pi f_c)$, where the loop takes over.

**What jitter costs.** For an ADC, the sampling error from jitter limits SNR to $-20\log_{10}(2\pi f_{in}\sigma_t)$ (20-05). For a serial link, jitter closes the eye horizontally and must fit a budget with the transmitter's and channel's jitter; random jitter adds as a root-sum-square, deterministic jitter (spurs, crosstalk) adds linearly.

### 3.6 Fractional-N synthesis

An integer-N PLL can only produce multiples of $f_{ref}$, so a fine frequency step forces a low reference frequency and therefore a narrow loop bandwidth (§3.3) and a large $N$ (more multiplied noise). A **fractional-N** PLL switches the divide ratio between integers so that its average is fractional: to divide by 100.246, it divides by 100 most of the time and by 101 on 24.6% of reference cycles.

**The problem: periodic switching.** Done with a simple accumulator (a first-order ΔΣ modulator, 20-08), the switching pattern is periodic and the phase error it creates is a sawtooth at the fractional frequency: large **fractional spurs**.

**The ΔΣ solution.** A higher-order ΔΣ modulator (usually a MASH 1-1-1, 20-08 §3.6) drives the divider with a sequence $c[n]$ whose average is the fraction and whose error is shaped: $c = \text{frac} + (1 - z^{-1})^m e$. The output phase error is $2\pi$ times the running sum of the divide-ratio error, so the phase error is the error $e$ shaped by $(1 - z^{-1})^{m-1}$. With $e$ white of variance 1/12 at rate $f_{ref}$, the output phase noise (before the loop's filtering) is

$$
\mathcal{L}_{\Sigma\Delta}(f) = \frac{(2\pi)^2}{12f_{ref}}\left[2\sin\frac{\pi f}{f_{ref}}\right]^{2(m - 1)} ,
$$

which rises at 20(m − 1) dB per decade: the loop's low-pass response must cut it off, which is why fractional-N loops pair a third-order MASH with a loop filter of third order or higher. The formula assumes the modulator's error is "busy". A fraction that is a simple rational number, such as 123/500, makes the sequence periodic and turns the noise into spurs (Example 20-10.6); designs add a dither LSB or use a large accumulator modulus.

![Divider phase noise against offset from 30 kHz to 25 MHz for a MASH 1-1-1 fractional-N divider at a 50 MHz reference: the busy-fraction spectrum follows the dashed formula rising at 40 dB per decade from about minus 165 to minus 60 dBc per hertz, while the 123 over 500 fraction shows a comb of discrete spurs spaced 50 kHz apart instead of smooth noise](../../../assets/figures/20-10/mash.svg)

*Figure 4. A MASH 1-1-1 divider before loop filtering. A busy fraction gives the shaped noise of the formula; the fraction 123/500 repeats every 1000 reference cycles and gives a comb of spurs 50 kHz apart (Example 20-10.6).*

### 3.7 All-digital PLLs

An **all-digital PLL** (ADPLL) replaces the charge pump and analog loop filter with a time-to-digital converter (TDC) that measures the phase error, a digital loop filter, and a digitally controlled oscillator (DCO). The loop dynamics are set by digital coefficients, which do not vary with process and scale with each node; the loop filter takes no capacitor area. The TDC's resolution $\Delta t_{res}$ quantizes the phase error in steps of $2\pi\,\Delta t_{res}/T_{out}$; treated as white noise of variance $(2\pi\,\Delta t_{res}f_0)^2/12$ at rate $f_{ref}$, it sets an in-band floor

$$
\mathcal{L}_{TDC} = \frac{(2\pi)^2}{12}\,\left(\Delta t_{res}f_0\right)^2\frac{1}{f_{ref}} ,
$$

−97.8 dBc/Hz for 10 ps resolution at 5 GHz with a 50 MHz reference (Example 20-10.7). Fine-resolution TDCs (sub-gate-delay, interpolating or ΔΣ-based) are therefore at the heart of ADPLL design.

### 3.8 Comparing PLLs

A PLL's jitter can be lowered by burning power (more pump current, a stronger oscillator), so designs are compared with a **jitter-power figure of merit**:

$$
\text{FoM} = 10\log_{10}\left[\left(\frac{\sigma_t}{1\text{ s}}\right)^2\frac{P}{1\text{ mW}}\right] ,
$$

lower being better: 100 fs at 10 mW scores −250 dB. Every halving of the jitter for the same power improves it by 6 dB.

## 4. Worked examples

### Example 20-10.1 · Building blocks (tier A)

**Setup.** A PLL multiplies a 50 MHz reference by $N$ = 100 with $I_{cp}$ = 500 µA and a VCO of 500 MHz/V whose free-running frequency is 4.5 GHz at 0 V. Find the output frequency, the PFD/pump gain, and the locked control voltage. If the reference moves to 51 MHz, what are the new output frequency and control voltage?

**Solution.**

- $f_{out} = 100 \times 50\text{ MHz}$ = **5.0** GHz.
- $K_{PD} = 500\text{ µA}/2\pi$ = **79.6** µA/rad.
- Lock: $4.5\text{ GHz} + 500\text{ MHz/V} \times V = 5\text{ GHz}$, so $V_{ctrl}$ = **1.0** V.
- With 51 MHz: $f_{out}$ = **5.1** GHz and $V_{ctrl}$ = **1.2** V. A type-II loop reaches this with zero static phase error; the capacitor simply charges to the new voltage.

**Units check.** A/rad for the detector gain; V for the control voltage.

**Sanity check.** A 2% reference step moves the output by 2%, as multiplication by N requires.

### Example 20-10.2 · Designing the loop filter (tier B)

**Setup.** For the PLL of Example 20-10.1, design a third-order loop filter with a 2 MHz crossover and $b$ = 10. Find the phase margin, the filter components and the corner frequencies.

**Solution.**

- PM = $\arctan(9/(2\sqrt{10}))$ = **54.9**°.
- $\omega_z = \omega_c/\sqrt{10}$ and $\omega_p = \omega_c\sqrt{10}$: $f_z$ = **632** kHz, $f_p$ = **6.32** MHz.
- $\lvert G(j\omega_c)\rvert = 1$ with $K = I_{cp}K_{VCO}/(2\pi N)$ gives $C_1 + C_2 = (K/\omega_c^2)\sqrt{1 + b}\,/\sqrt{1 + 1/b}$ = **50.1** pF.
- $C_1$ = 0.9 × 50.1 pF = **45.1** pF, $C_2$ = **5.01** pF, $R = 1/(\omega_zC_1)$ = **5.59** kΩ.

**Units check.** $K$ in A·rad/(s·V·rad) = A/(V·s); $K/\omega^2$ in F.

**Sanity check.** The crossover is $f_{ref}/25$, comfortably inside the sampled-loop limit of §3.3, and the capacitors fit on chip. ngspice's AC analysis of this loop (lab) gives a 2.00 MHz crossover and 54.9° of phase margin.

### Example 20-10.3 · The closed loop (tier B)

**Setup.** For the loop of Example 20-10.2, find the closed-loop −3 dB bandwidth and peaking, the settling time to 0.1% after a reference phase step, and the second-order approximation's natural frequency and damping (ignoring $C_2$).

**Solution.** From the exact transfer function (lab):

- −3 dB bandwidth **3.25** MHz, peaking **2.11** dB.
- Settling to 0.1%: **1.03** µs.
- Ignoring $C_2$: $\omega_n/2\pi$ = **1.19** MHz and ζ = **0.94**.

**Units check.** Hertz and seconds; ζ dimensionless.

**Sanity check.** The second-order envelope decays as $e^{-\zeta\omega_nt}$ with $\zeta\omega_n/2\pi$ = **1.11** MHz, so reaching 0.1% takes about $\ln 1000/\zeta\omega_n$ = **0.99** µs, consistent with the exact 1.03 µs.

### Example 20-10.4 · Noise transfer (tier B)

**Setup.** In the loop of Example 20-10.2, the reference has −150 dBc/Hz of phase noise at 1 MHz offset and the VCO alone has −120 dBc/Hz there. Find each one's contribution at the output at 1 MHz offset.

**Solution.**

- Reference: multiplied by $N^2$ (+40 dB) and by the closed-loop response normalized to $N$, which at 1 MHz is **+2.09** dB of peaking: $-150 + 40 + 2.09$ = **−107.9** dBc/Hz.
- VCO: through $1/(1 + G)$, which at 1 MHz is only **−5.29** dB (1 MHz is below but close to the 2 MHz crossover): $-120 - 5.29$ = **−125.3** dBc/Hz.

The reference path dominates by **17.4** dB here: a narrower loop bandwidth would lower the total noise at this offset.

**Units check.** dBc/Hz plus dB of transfer gives dBc/Hz.

**Sanity check.** $20\log_{10}N$ = 40 dB is the price of multiplication: a 5 GHz output can never be cleaner in band than 100 times its 50 MHz reference.

### Example 20-10.5 · Jitter from phase noise (tier B)

**Setup.** A 5 GHz PLL output has a flat −100 dBc/Hz from 10 kHz to its 2 MHz bandwidth and falls at −20 dB per decade beyond. Find the rms jitter integrated from 10 kHz to 1 GHz, and the SNR it allows an ADC sampling a 1 GHz and a 100 MHz input.

**Solution.** With $\mathcal{L}_0 = 10^{-10}$ and $f_c$ = 2 MHz:

$$
\sigma_\phi^2 = 2\mathcal{L}_0(f_c - f_1) + 2\mathcal{L}_0f_c\left(1 - \frac{f_c}{f_2}\right) ,
$$

since $\int_{f_c}^{f_2}(f_c/f)^2df = f_c(1 - f_c/f_2)$. So $\sigma_\phi$ = **28.2** mrad and $\sigma_t$ = **899** fs. The ADC limits: $-20\log_{10}(2\pi f_{in}\sigma_t)$ = **45.0** dB at 1 GHz and **65.0** dB at 100 MHz.

**Units check.** $\mathcal{L}$ in 1/Hz times Hz is rad²; rad divided by rad/s is s.

**Sanity check.** Half the variance comes from the flat region and half from the tail beyond the bandwidth ($f_c - f_1 \approx f_c$): the noise just outside the loop bandwidth matters as much as the in-band plateau.

### Example 20-10.6 · A fractional-N synthesizer (tier B)

**Setup.** The PLL must produce 5.0123 GHz from 50 MHz. Find the divide ratio. With a MASH 1-1-1 modulator driving the divider, find its phase noise at 1 MHz and 10 MHz offsets before and after the loop's low-pass response (Example 20-10.2). The fraction is 123/500: what does that do?

**Solution.**

- $N = 5.0123\text{ GHz}/50\text{ MHz}$ = **100.246** = 100 + 123/500.
- MASH noise, $m$ = 3: at 1 MHz **−107.9** dBc/Hz, at 10 MHz **−69.0** dBc/Hz (rising 40 dB per decade).
- After the loop (times $\lvert H/N\rvert^2$): **−105.8** dBc/Hz at 1 MHz (in band, slightly peaked) and **−87.6** dBc/Hz at 10 MHz.
- With integer accumulators the sequence for 123/500 repeats every **1000** reference cycles, so instead of smooth noise it produces spurs at multiples of $f_{ref}/1000$ = **50** kHz (the lab shows them). A dither bit or a larger modulus breaks the period.

**Units check.** dBc/Hz throughout.

**Sanity check.** Beyond the loop bandwidth the ΔΣ noise rises faster (40 dB per decade) than the third-order loop's response falls in that region, which is why fractional-N designs keep the bandwidth modest or add a pole.

### Example 20-10.7 · Figures of merit (tier A)

**Setup.** (a) A PLL achieves 100 fs rms jitter at 10 mW. (b) A 5 GHz oscillator has −120 dBc/Hz at 1 MHz offset at 5 mW. (c) An ADPLL at 5 GHz with a 50 MHz reference uses a 10 ps TDC. Find each figure of merit or floor.

**Solution.**

- (a) $10\log_{10}[(10^{-13})^2 \times 10]$ = **−250** dB.
- (b) $120 + 20\log_{10}(5000) - 10\log_{10}5$ = **187.0** dB.
- (c) $\mathcal{L}_{TDC} = 10\log_{10}[(2\pi)^2/12 \times (10\text{ ps} \times 5\text{ GHz})^2/50\text{ MHz}]$ = **−97.8** dBc/Hz.

**Units check.** The FoMs are dB relative to 1 s² · 1 mW and to 1 Hz·mW conventions; the floor is per hertz.

**Sanity check.** The TDC floor is **2.2** dB above the in-band plateau of Example 20-10.5: a 10 ps TDC would set this ADPLL's in-band noise, so sub-10 ps resolution is needed to match an analog loop.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 20-10.1a | output frequency | 5.0 | GHz |
| Ex 20-10.1b | PFD/pump gain | 79.6 | µA/rad |
| Ex 20-10.1c | locked control voltage | 1.0 | V |
| Ex 20-10.1d | output, 51 MHz reference | 5.1 | GHz |
| Ex 20-10.1e | control voltage, 51 MHz | 1.2 | V |
| Ex 20-10.2a | phase margin | 54.9 | ° |
| Ex 20-10.2b | zero frequency | 632 | kHz |
| Ex 20-10.2c | pole frequency | 6.32 | MHz |
| Ex 20-10.2d | C1 + C2 | 50.1 | pF |
| Ex 20-10.2e | C1 | 45.1 | pF |
| Ex 20-10.2f | C2 | 5.01 | pF |
| Ex 20-10.2g | R | 5.59 | kΩ |
| Ex 20-10.2h | simulated crossover | 2.00 | MHz |
| Ex 20-10.2i | simulated phase margin | 54.9 | ° |
| Ex 20-10.3a | −3 dB bandwidth | 3.25 | MHz |
| Ex 20-10.3b | peaking | 2.11 | dB |
| Ex 20-10.3c | settling to 0.1% | 1.03 | µs |
| Ex 20-10.3d | natural frequency | 1.19 | MHz |
| Ex 20-10.3e | damping | 0.94 | — |
| Ex 20-10.3f | ζω_n / 2π | 1.11 | MHz |
| Ex 20-10.3g | second-order settling estimate | 0.99 | µs |
| Ex 20-10.4a | reference transfer at 1 MHz | 2.09 | dB |
| Ex 20-10.4b | reference contribution | −107.9 | dBc/Hz |
| Ex 20-10.4c | VCO transfer at 1 MHz | −5.29 | dB |
| Ex 20-10.4d | VCO contribution | −125.3 | dBc/Hz |
| Ex 20-10.4e | reference dominance | 17.4 | dB |
| Ex 20-10.5a | rms jitter | 899 | fs |
| Ex 20-10.5d | rms phase | 28.2 | mrad |
| Ex 20-10.5b | ADC SNR, 1 GHz | 45.0 | dB |
| Ex 20-10.5c | ADC SNR, 100 MHz | 65.0 | dB |
| Ex 20-10.6a | divide ratio | 100.246 | — |
| Ex 20-10.6b | MASH noise, 1 MHz | −107.9 | dBc/Hz |
| Ex 20-10.6c | MASH noise, 10 MHz | −69.0 | dBc/Hz |
| Ex 20-10.6d | filtered, 1 MHz | −105.8 | dBc/Hz |
| Ex 20-10.6e | filtered, 10 MHz | −87.6 | dBc/Hz |
| Ex 20-10.6f | sequence period | 1000 | cycles |
| Ex 20-10.6g | spur spacing | 50 | kHz |
| Ex 20-10.7a | jitter-power FoM | −250 | dB |
| Ex 20-10.7b | oscillator FoM | 187.0 | dB |
| Ex 20-10.7c | TDC floor | −97.8 | dBc/Hz |
| Ex 20-10.7d | TDC floor above the plateau | 2.2 | dB |
| Txt 20-10.a | Gardner limit, zero far below reference | 0.32 | f_ref |
| Txt 20-10.b | peak-to-peak/rms, 10³ edges | 6.58 | — |
| Txt 20-10.c | peak-to-peak/rms, 10⁹ edges | 12.2 | — |
| Txt 20-10.d | peak-to-peak/rms, 10¹² edges | 14.3 | — |
| Txt 20-10.e | rms phase for 3.5% EVM | 2.0 | ° |
| Txt 20-10.f | jitter for 3.5% EVM at 28 GHz | 199 | fs |
| Txt 20-10.g | sub-sampling PLL FoM | −247.7 | dB |
| Txt 20-10.h | sampling PLL FoM | −263.1 | dB |
| Txt 20-10.i | fractional-N record FoM | −260.7 | dB |
| Txt 20-10.j | wireline digital PLL FoM | −240.9 | dB |
| Txt 20-10.k | LMX2594 flat noise at 12 GHz | −114.4 | dBc/Hz |

## 5. Simulate it

The lab ([labs/20-10-lab](../labs/20-10-lab/README.md)) implements the phase-domain model in `pll.py` and confirms the open loop in ngspice.

**Predict, then run.**

1. Predict the crossover and phase margin of Example 20-10.2, then run `ngspice -b loop.cir` (Part 1).
2. Predict the closed-loop peaking and settling, then plot the step response for b = 4, 10 and 20 (Part 2).
3. Predict how the output phase noise splits between reference and VCO for loop bandwidths of 0.5, 2 and 5 MHz, then plot the total (Part 3).
4. Predict the jitter of Example 20-10.5, integrate it, and see how the integration band changes the answer (Part 4).
5. Predict where a 123/500 fractional-N divider puts its spurs, then simulate the MASH sequence and compare a "busy" fraction with the formula (Part 5).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Loop bandwidth | VCO noise suppression, lock time | More reference, pump and ΔΣ noise; must stay ≪ $f_{ref}$ | PLL designer |
| Phase margin (b) | Less peaking, better settling | Less reference-spur filtering for a given bandwidth | PLL designer |
| Charge-pump current | Lower input-referred pump noise | Power, larger capacitors for the same bandwidth, mismatch spurs | PLL designer |
| Reference frequency | Smaller N (less multiplied noise), wider bandwidth | A faster, costlier reference; coarser integer steps | System architect |
| Fractional-N with ΔΣ | Fine steps with a high reference | Shaped quantization noise, fractional spurs, linearity demands | PLL designer |
| LC versus ring oscillator | LC: far lower phase noise | LC: area (inductor), narrow tuning range | Clocking architect |
| All-digital PLL | Portable, scalable, no loop-filter area | TDC resolution floor, DCO quantization | Clocking architect |

## 7. Numbers to know

| Quantity | Typical value | Note |
|---|---|---|
| Loop bandwidth against reference | $f_c \lesssim f_{ref}/10$ by design; sampled-loop instability near $f_{ref}/3$ (28–30%) | Gardner [1], Hanumolu et al. [2], Banerjee [3] **[Established]** |
| Phase-noise convention | $\mathcal{L}(f)$ single-sideband; one-sided $S_\phi \approx 2\mathcal{L}$; $\sigma_\phi^2 = 2\int\mathcal{L}\,df$ | NIST [9], Banerjee [3] **[Established]** |
| Peak-to-peak against rms for Gaussian jitter | about $2Q^{-1}(1/2N)$ times σ: **6.58** for $10^3$ edges, **12.2** for $10^9$, **14.3** for $10^{12}$ | Banerjee's table [3]; a peak-to-peak number grows with the observation |
| LC oscillator FoM | about 186 dB for Q = 10 at 300 K; about 196 dB for a class-C design | Razavi [10] |
| Best published PLL FoM (as of Nov 2026) | −263.1 dB: 20.3 fs at 19 GHz for 12 mW (integer-N sampling PLL, 28 nm, 2021) | [12] [R-350] **[Established]** |
| Best fractional-N PLL (as of Nov 2026) | 21.6 fs, −260.7 dB, worst-case fractional spur −67.4 dBc (14 GHz, 28 nm, ISSCC 2026) | [12] [R-350] **[Established]** |
| Lowest published PLL jitter (as of Nov 2026) | 15.8 fs rms (13 GHz charge-pump PLL, ISSCC 2025; band not stated in the abstract) | [12] [R-350] |
| Commercial RF synthesizer (as of Nov 2026) | TI LMX2594: 10 MHz–15 GHz; 45 fs rms at 7.5 GHz (100 Hz–100 MHz); −110 dBc/Hz at 100 kHz on 15 GHz; normalized in-band floor −236 dBc/Hz | [13] [R-351] |
| SerDes reference clock (as of Nov 2026) | 112G PAM4: about 100 fs rms (12 kHz–20 MHz) at 312.5 MHz; 224G example: 35 fs with a 4 MHz high-pass filter | TI and Renesas notes [14] [R-352] **[Industry estimate]** |
| PCIe reference-clock limit (as of Nov 2026) | Gen 5: 0.15 ps rms; Gen 6: 0.1 ps rms, both after the standard's clock-recovery filters | TI SNAA386 table, not the PCI-SIG text [14] [R-352] |
| MCU system PLL (as of Nov 2026) | TI MSPM0G3507: period jitter 45 ps rms and cycle-to-cycle 60 ps rms at 80 MHz; 316 µA | [15] [R-351] |
| 77 GHz radar chirp PLL (as of Nov 2026) | TI AWR2944: −96 dBc/Hz at 1 MHz offset (76–77 GHz); ramps to 250 MHz/µs | [15] [R-351] |
| 5G EVM budget | 256QAM base-station EVM 3.5%: if the LO took all of it, **2.0**° rms, **199** fs at 28 GHz | 3GPP TS 38.104 [16]; our arithmetic |

## 8. Common mistakes

- **Treating the PLL as continuous at any bandwidth.** The pump samples once per reference period; keep the crossover around a tenth of $f_{ref}$ or lower.
- **Forgetting that reference noise is multiplied.** In band, the output is $20\log_{10}N$ dB noisier than the reference.
- **Comparing jitter numbers integrated over different bands.** 12 kHz–20 MHz and 10 kHz–100 MHz can differ by a large factor; always state the band.
- **Ignoring the noise just outside the loop bandwidth.** It can contribute as much jitter as the in-band plateau (Example 20-10.5).
- **Assuming a fractional-N synthesizer is free of spurs.** Simple rational fractions make the ΔΣ sequence periodic; check the fraction and the modulus.
- **Using period jitter where absolute jitter matters (or the reverse).** A link's clock recovery tracks slow wander; an ADC's sampling does not.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Sampling LC PLLs hold the records [Established].** Gao, Klumperink, Bohsali and Nauta's sub-sampling PLL (2009) removed the divider from the locked loop so that phase-detector and pump noise are "not multiplied by N²": 0.15 ps rms (10 kHz–40 MHz) at 2.2 GHz for 7.56 mW, a FoM of **−247.7** dB (our arithmetic) [8]. Its descendants lead today: Zhao and Razavi's 19 GHz sampling PLL reaches 20.3 fs (10 kHz–100 MHz) for 12 mW in 28 nm, **−263.1** dB, the best FoM in the public survey; the lowest absolute jitter in it, 15.8 fs, comes from a 13 GHz charge-pump PLL at ISSCC 2025 [12].
- **Fractional-N has nearly closed the gap [Established].** An ISSCC 2026 fractional-N PLL reaches 21.6 fs and **−260.7** dB with a worst-case fractional spur of −67.4 dBc at 14 GHz in 28 nm [12]; a 7.3–9.5 GHz design reports 34 fs and −255.5 dB from an 80 MHz reference [12].
- **Digital PLLs are mainstream [Established].** Staszewski and colleagues replaced the charge pump and loop filter with a TDC and digital filter in a 130 nm Bluetooth radio (2004) and then a 90 nm GSM/EDGE phone transmitter (2005, "the first all-digital PLL and polar transmitter for mobile phones") [7]. The best digital PLL in the survey scores −257 dB (45.9 fs at 4.75 GHz, 2025), and a 7 nm wireline bang-bang PLL with "fully synthesized" digital functions reaches 143 fs (1 kHz–100 MHz) for 40 mW, **−240.9** dB [12].
- **Rings for many lanes [Established].** LC PLLs "occupy considerable space, lack efficiency in generating multiple phases" in multi-lane SerDes, so a 2024 ring-oscillator sampling PLL targets 69.3 fs over 6.8–14 GHz for >100 Gb/s links; in the survey's data, ring PLLs trail LC PLLs by about 10 dB of FoM (our reading) [12].
- **Jitter is expensive [Established].** Razavi shows that for a VCO-limited loop "to halve σj, PVCO must quadruple", and with reference noise included power rises 16-fold per halving; clock generation "may consume a greater power than the converter itself" [10].
- **A public survey exists, with errors.** Davami and Jang's ETH Zürich survey lists 228 PLLs from JSSC and ISSCC 2020–2026 and other conferences; 23 of its FoM entries disagree with 20 log σ + 10 log P by more than 0.6 dB, so numbers here were re-checked against each paper's abstract [11] [R-350].

### Why it matters commercially

Every clocked chip in the learner's coverage contains PLLs, and their quality limits the product. In **AI datacenters**, each 112G or 224G SerDes lane needs a reference clock with about 100 fs or less of integrated jitter, and Razavi estimates that a 112 Gbaud transmitter needs a PLL below roughly 100 fs rms [10], [14]; jitter-cleaner and clock-generator chips are a distinct product line for exactly this. In **automotive radar**, the chirp is a fractional-N PLL ramping at hundreds of MHz/µs, and its phase noise sets how well a small target is seen next to a large one [15]. In **5G and Wi-Fi**, the LO's integrated phase noise consumes part of the EVM budget: Razavi cites −45 dB of integrated phase jitter for 256QAM near 30 GHz, about 30 fs [10], [16]. In **wearables and MCUs**, PLLs are small (hundreds of µA) and specified with period and cycle-to-cycle jitter in tens of picoseconds [15]; Bluetooth radios use all-digital PLLs that can run near 1.6 mW at 0.5 V [12]. In **quantum computing**, where control electronics move into the cryostat, a cryogenic fractional-N PLL reaches 19.4 fs (12 kHz–20 MHz) at 4 K and 29.7 fs at 300 K [12].

> **Deeper:** see companion repo *Datacenter Networking* for SerDes clocking and link jitter budgets, and companion repo *Quantum Computing* for cryogenic control electronics.

### Questions for engineering leaders

1. **"Over what offset band is that jitter integrated, and does it include spurs?"** Strong: the band matches the application (the link's clock-recovery filter, the ADC's full bandwidth), and spurs are either included or listed separately with levels. Evasive: "12 kHz to 20 MHz" for a 224G SerDes, or a "random jitter" number without spurs.
2. **"What is the worst-case fractional spur over all channels we will use, and how do you know?"** Strong: a sweep over channels with the worst value and its fraction. Evasive: the spur at one favorable channel.
3. **"Is the reference oscillator's power and noise inside your FoM?"** Strong: the full power, with the crystal or reference buffer stated. Evasive: a FoM with a 250 MHz reference that the product will not have.
4. **"Typical at 25 °C, or guaranteed over voltage and temperature?"** Strong: a maximum over the operating range. Evasive: a typical value only.
5. **"What happens to phase noise when the digital logic next to the PLL is busy?"** Strong: measurements under supply and substrate noise, with the isolation strategy. Evasive: data from a quiet test chip.

### Marketing vs Reality

- **The band decides the number.** In one TI analysis of an ADC clock, offsets from 10 to 100 MHz contributed about 360 fs, more than the 194 fs from 100 Hz to 10 MHz [17]. The same Zhao–Razavi PLL is 20.3 fs from 10 kHz to 100 MHz and 20.9 fs of "random jitter" from 10 kHz to 40 MHz in its journal version [12]. SiTime notes that the 12 kHz–20 MHz band was introduced in 1992 for SONET OC-48 and calls it "no longer suited for modern high-speed designs" [14]. Conversely, a part measured at 179 fs (12 kHz–20 MHz) still passes PCIe Gen 6's 100 fs limit, because that limit applies the standard's own filters [14].
- **Filtered and spur-free numbers.** TI's LMK05318B quotes 32 fs "with 4MHz 1st order high-pass filter" on its front page and 50 fs typical, 80 fs maximum without it; one of its outputs is 125 fs "excluding output crosstalk spurs" and 145 fs with them [13].
- **Two different "figures of merit".** The LMX2594's "Figure of merit: –236 dBc/Hz" is its normalized in-band noise floor: the flat noise is that number plus $20\log_{10}(f_{VCO}/f_{PD}) + 10\log_{10}(f_{PD}/1\text{ Hz})$, **−114.4** dBc/Hz at 12 GHz with a 100 MHz phase detector [13]. It is not the jitter-power FoM of §3.8, which for academic PLLs is around −250 to −263 dB.
- **The reference is often outside the FoM.** Low-power crystal oscillators reach −153 to −158 dBc/Hz at 100 kHz offset for under 0.2 mW, while a 100 MHz crystal oscillator with −178 dBc/Hz draws 1.8 W [10]. Record FoMs use 100–250 MHz references, and one ISSCC 2025 team notes that "high reference frequencies of 150 to 500 MHz are not practical for cost-effective mass deployment" [12].
- **Typical is not guaranteed.** The LMK04832 table states that typical values "are not assured", and its feature list and electrical table give different bands for the same 64 fs [13]. Banerjee warns of a few dB of part-to-part and board-to-board variation in phase noise [3].
- **Sanity check.** Convert any phase-noise plot to jitter with $\sigma_t = \sqrt{2\int\mathcal{L}\,df}/(2\pi f_0)$ over your band, recompute the FoM as $20\log_{10}\sigma_t + 10\log_{10}P$, and ask what the reference costs.

## 10. Concept check

**Q1.** Why is the VCO an integrator in the phase domain?

<details><summary>Answer</summary>

The control voltage sets the VCO's frequency, and phase is the integral of frequency: $\theta = \int K_{VCO}V_{ctrl}\,dt$, so $\theta(s) = K_{VCO}V_{ctrl}(s)/s$.

</details>

**Q2.** Why does a charge-pump PLL need a resistor in its loop filter?

<details><summary>Answer</summary>

The capacitor and the VCO are two integrators, giving 180° of phase lag at all frequencies; the loop would oscillate. The resistor adds a zero that lifts the phase near crossover and creates the phase margin.

</details>

**Q3.** How does reference noise reach the output, and why is it multiplied by N?

<details><summary>Answer</summary>

Through $NG/(1 + G)$, which is about N in band: the loop forces the output phase to N times the reference phase, so a phase wobble of the reference becomes N times larger at the output, a noise increase of $20\log_{10}N$ dB.

</details>

**Q4.** What does a wider loop bandwidth improve, and what does it worsen?

<details><summary>Answer</summary>

It suppresses the VCO's noise over a wider range and speeds up locking; it passes more reference, charge-pump, divider and ΔΣ noise, and it must stay well below the reference frequency for the sampled loop to remain stable.

</details>

**Q5.** Why does a fractional-N PLL use a higher-order ΔΣ modulator rather than a simple accumulator?

<details><summary>Answer</summary>

A simple accumulator produces a periodic switching pattern whose phase error is a sawtooth at the fractional frequency, giving large spurs. A higher-order ΔΣ modulator randomizes the switching and pushes the error to high offsets, where the loop filters it.

</details>

**Q6.** What limits an all-digital PLL's in-band noise?

<details><summary>Answer</summary>

The TDC's resolution: it quantizes the phase error, adding white noise whose in-band level is $(2\pi)^2(\Delta t_{res}f_0)^2/(12f_{ref})$.

</details>

Problems: [20-10 problem set](../problems/20-10-problems.md) · Worked solutions: [20-10 solutions](../solutions/20-10-solutions.md)

## 11. Key terms

[Phase-locked loop (PLL)](../../../reference/glossary.md#phase-locked-loop-pll) · [Phase-frequency detector](../../../reference/glossary.md#phase-frequency-detector) · [Charge pump](../../../reference/glossary.md#charge-pump) · [Voltage-controlled oscillator (VCO)](../../../reference/glossary.md#voltage-controlled-oscillator-vco) · [Phase noise](../../../reference/glossary.md#phase-noise) · [Jitter](../../../reference/glossary.md#jitter) · [Fractional-N synthesizer](../../../reference/glossary.md#fractional-n-synthesizer) · [Time-to-digital converter (TDC)](../../../reference/glossary.md#time-to-digital-converter-tdc) · [All-digital PLL (ADPLL)](../../../reference/glossary.md#all-digital-pll-adpll) · [Reference spur](../../../reference/glossary.md#reference-spur)

## 12. Connections

- **Previous:** [20-09](20-09-dacs.md) (a fast DAC's noise floor is set by its clock's jitter).
- **Builds on:** [15-12](../../15-control-systems/chapters/15-12-control-applications-pll-regulators-thermal.md) and [15-07](../../15-control-systems/chapters/15-07-frequency-domain-design.md) (loop analysis, phase margin), [20-05](20-05-comparators-and-sample-and-hold.md) (jitter and SNR), [20-08](20-08-sigma-delta-converters.md) (MASH modulators).
- **Next:** [20-11](20-11-layout-matching-pvt.md) covers the matching and layout that set charge-pump mismatch and VCO variation.
- **Used later:** link and clocking budgets in the practitioner layer.

> **Deeper:** see companion repo *Datacenter Networking* for SerDes clocking, clock-data recovery and link jitter budgets.

## 13. Further study

- B. Razavi, *Design of CMOS Phase-Locked Loops: From Circuit Level to Architecture Level*, Cambridge University Press, 2020.
- D. Banerjee, *PLL Performance, Simulation and Design*: a practitioner's book on loop-filter design and noise, available free from the author and Texas Instruments.
- The papers in §14 on charge-pump loops, oscillator phase noise and fractional-N synthesis.

## 14. Sources

1. F. M. Gardner, "Charge-pump phase-lock loops," *IEEE Trans. Commun.*, vol. 28, no. 11, pp. 1849–1858, Nov. 1980, DOI 10.1109/TCOM.1980.1094619; D. Fischette, "Practical phase-locked loop design," ISSCC 2004 tutorial (stability-limit form) [R-349].
2. P. K. Hanumolu, M. Brownlee, K. Mayaram and U.-K. Moon, "Analysis of charge-pump phase-locked loops," *IEEE Trans. Circuits Syst. I*, vol. 51, no. 9, pp. 1665–1674, Sep. 2004, DOI 10.1109/TCSI.2004.834516 [R-349].
3. D. Banerjee, *PLL Performance, Simulation, and Design*, 5th ed., Texas Instruments SNAA106C, May 2017 (loop-filter design, noise models, integrated jitter) [R-349].
4. D. B. Leeson, "A simple model of feedback oscillator noise spectrum," *Proc. IEEE*, vol. 54, no. 2, pp. 329–330, 1966, DOI 10.1109/PROC.1966.4682; A. Hajimiri and T. H. Lee, "A general theory of phase noise in electrical oscillators," *IEEE J. Solid-State Circuits*, vol. 33, no. 2, pp. 179–194, Feb. 1998, DOI 10.1109/4.658619, with corrections in vol. 33, no. 6, p. 928, June 1998, DOI 10.1109/4.678662; T. H. Lee and A. Hajimiri, "Oscillator phase noise: a tutorial," *IEEE J. Solid-State Circuits*, vol. 35, no. 3, pp. 326–336, Mar. 2000, DOI 10.1109/4.826814 [R-349].
5. B. Razavi, "A study of phase noise in CMOS oscillators," *IEEE J. Solid-State Circuits*, vol. 31, no. 3, pp. 331–343, Mar. 1996, DOI 10.1109/4.494195; J. A. McNeill, "Jitter in ring oscillators," *IEEE J. Solid-State Circuits*, vol. 32, no. 6, pp. 870–879, June 1997, DOI 10.1109/4.585289 [R-349].
6. T. A. D. Riley, M. A. Copeland and T. A. Kwasniewski, "Delta-sigma modulation in fractional-N frequency synthesis," *IEEE J. Solid-State Circuits*, vol. 28, no. 5, pp. 553–559, May 1993, DOI 10.1109/4.229400 [R-349].
7. R. B. Staszewski et al., "All-digital TX frequency synthesizer and discrete-time receiver for Bluetooth radio in 130-nm CMOS," *IEEE J. Solid-State Circuits*, vol. 39, no. 12, pp. 2278–2291, Dec. 2004, DOI 10.1109/JSSC.2004.836345, and "All-digital PLL and transmitter for mobile phones," *ibid.*, vol. 40, no. 12, pp. 2469–2482, Dec. 2005, DOI 10.1109/JSSC.2005.857417 [R-349].
8. X. Gao, E. A. M. Klumperink, M. Bohsali and B. Nauta, "A low noise sub-sampling PLL in which divider noise is eliminated and PD/CP noise is not multiplied by N²," *IEEE J. Solid-State Circuits*, vol. 44, no. 12, pp. 3253–3263, Dec. 2009, DOI 10.1109/JSSC.2009.2032723; X. Gao, E. A. M. Klumperink, P. F. J. Geraedts and B. Nauta, "Jitter analysis and a benchmarking figure-of-merit for phase-locked loops," *IEEE Trans. Circuits Syst. II*, vol. 56, no. 2, pp. 117–121, Feb. 2009, DOI 10.1109/TCSII.2008.2010189 [R-349], [R-350].
9. F. L. Walls, A. J. D. Clements, C. M. Felton, M. A. Lombardi and M. D. Vanek, "Extending the range and accuracy of phase noise measurements," *Proc. 42nd Annual Frequency Control Symposium*, 1988 (NIST) [R-349].
10. B. Razavi, "Jitter-power trade-offs in PLLs," *IEEE Trans. Circuits Syst. I*, vol. 68, no. 4, pp. 1381–1387, Apr. 2021, DOI 10.1109/TCSI.2021.3057580 [R-350].
11. P. Davami and T. Jang, "Phase-Locked Loops (PLL) Performance Survey," ETH Zürich, MIT license, last updated May 2026; W. Bae, "Benchmark figure of merit extensions for low jitter phase locked loops inspired by new PLL architectures," *IEEE Access*, vol. 10, pp. 80680–80694, 2022, DOI 10.1109/ACCESS.2022.3195687 [R-350].
12. Y. Zhao and B. Razavi, VLSI Symposium 2021, DOI 10.23919/VLSICircuits52068.2021.9492419, and Y. Zhao, M. Forghani and B. Razavi, *IEEE JSSC*, vol. 58, no. 6, pp. 1597–1609, 2023, DOI 10.1109/JSSC.2022.3225105; D. Sun et al., ISSCC 2025, paper 19.11, DOI 10.1109/ISSCC49661.2025.10904662; ISSCC 2026, paper 12.4, DOI 10.1109/ISSCC49663.2026.11409271; C.-C. Hung et al., ISSCC 2025, paper 19.3, DOI 10.1109/ISSCC49661.2025.10904550; S. Gallucci et al., *IEEE JSSC*, vol. 60, no. 12, pp. 4572–4586, 2025, DOI 10.1109/JSSC.2025.3618958; D. Pfaff et al., *IEEE JSSC*, vol. 55, no. 3, pp. 580–591, 2020, DOI 10.1109/JSSC.2019.2946134; Khalil et al., ISSCC 2024, paper 7.8, DOI 10.1109/ISSCC49657.2024.10454445; N. Pourmousavian et al., *IEEE JSSC*, vol. 53, no. 9, pp. 2572–2583, 2018, DOI 10.1109/JSSC.2018.2843337; J. Xiao et al., *IEEE JSSC*, vol. 61, no. 5, pp. 1876–1894, May 2026, DOI 10.1109/JSSC.2026.3653994 [R-350].
13. Texas Instruments, LMX2594 (SNAS696C, rev. Apr. 2019), LMK04832 (SNAS688C, rev. May 2018) and LMK05318B (SNAS801D, rev. May 2026) data sheets [R-351].
14. Texas Instruments, "112G and 224G PAM4 SerDes clocking for rapid data center switches," SNAA396A, Jan. 2025, and K. Samuel, "Clocking for PCIe applications," SNAA386, Nov. 2023; Renesas, R31AN0063EU0104 rev. 1.04, Jan. 2025; G. Giust, "Practical analysis of refclk jitter for SerDes applications," SiTime, 2024 [R-352].
15. Texas Instruments, MSPM0G3507 (SLASEX6C, rev. Oct. 2025) and AWR2944 (SWRS273E, rev. Feb. 2026) data sheets [R-351].
16. 3GPP TS 38.104 V18.5.0 (ETSI TS 138 104), base-station EVM requirements, May 2024 [R-352].
17. T. Neu, "Clock jitter analyzed in the time domain, Part 1," *TI Analog Applications Journal*, SLYT379, 3Q 2010 [R-352].
