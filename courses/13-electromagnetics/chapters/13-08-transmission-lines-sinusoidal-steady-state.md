<!-- status: verified -->
# 13-08 · Transmission Lines: Sinusoidal Steady State

| | |
|---|---|
| **Course** | [13 · Electromagnetics](../README.md) |
| **University equivalent** | The sinusoidal transmission-line chapter of a junior electromagnetics course: phasor telegrapher's equations, propagation constant and characteristic impedance with loss, reflection coefficient along the line, input impedance, standing waves and VSWR, return and mismatch loss, stubs, the quarter-wave transformer and lossy lines (Ulaby & Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 2; Pozar, *Microwave Engineering*, ch. 2) |
| **Prerequisites** | [13-07 Transmission Lines: Time Domain](13-07-transmission-lines-time-domain.md), [13-05 Plane Waves in Lossless and Lossy Media](13-05-plane-waves.md), [07-05 Sinusoidal Steady State and Impedance](../../07-circuit-analysis-2-transient-and-ac/chapters/07-05-sinusoidal-steady-state-and-impedance.md) |
| **Estimated study hours** | 10 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Write the phasor telegrapher's equations and compute γ and $Z_0$ for a lossy line, exactly and in the low-loss approximation.
2. Track the reflection coefficient along a line and compute the input impedance of any length of line with any load.
3. Compute standing-wave patterns, VSWR, return loss, mismatch loss and delivered power.
4. Design shorted and open stubs as reactances, and quarter-wave transformers as matching networks, including their bandwidth.
5. Explain how line loss masks a mismatch, and why a distortionless line needs $R'/L' = G'/C'$.

---

## 1. Big picture

At a single frequency, a transmission line becomes an impedance transformer. A load seen through a length of line looks like a different impedance, one that depends on the line's length in wavelengths. This one idea underlies RF design: matching networks built from line sections, filters built from stubs, antenna feeds, and the reading of every network-analyzer measurement. Loss adds a second effect: it attenuates the signal and hides mismatches from the input.

- **Matching.** Power amplifiers, low-noise amplifiers and antennas are matched to 50 Ω with line sections and stubs (13-09).
- **Measurement.** A vector network analyzer reports the reflection coefficient $S_{11}$, return loss and VSWR, all defined in this chapter.
- **Distributed elements.** At microwave frequencies, inductors and capacitors are made from short line stubs, because lumped parts stop behaving ideally.
- **Cable and channel loss.** The attenuation constant α sets how far a signal can go; its split into conductor and dielectric parts (13-05) decides what to improve.

## 2. Intuition first

**The load seen through a window.** A sinusoidal wave goes down the line, reflects at the load and comes back. At any point the voltage is the sum of the two, and their ratio to the current gives an impedance. Move along the line and the relative phase of the forward and reflected waves changes, by twice the electrical distance (out and back), so the impedance you see cycles every half wavelength. A quarter wavelength turns a large impedance into a small one; a half wavelength gives back the load itself.

**Standing waves.** Where forward and reflected waves add in phase the voltage is largest; a quarter wavelength away they subtract. The ratio of the two, the VSWR, measures the mismatch without needing phase information, which is how mismatches were measured before network analyzers.

**An analogy from finance, and its limits.** Input impedance resembles a periodic payoff: the same underlying (the load) seen through an instrument whose behaviour repeats with a fixed period (half a wavelength), and inverts halfway. The analogy breaks because the line is linear, lossless lines conserve energy exactly, and the "period" depends on frequency, so the transformation is only exact at one frequency: matching networks have finite bandwidth.

## 3. Theory

> **Conventions.** Phasors are peak amplitudes. The line has $R'$, $L'$, $G'$, $C'$ per metre. Distance $d$ is measured **from the load toward the source**, so the load is at $d$ = 0. $\Gamma_L = (Z_L - Z_0)/(Z_L + Z_0)$; $\Gamma(d)$ is the ratio of reflected to forward voltage at distance $d$. Return loss RL = $-20\log_{10}\lvert\Gamma\rvert$ (a positive number); mismatch loss ML = $-10\log_{10}(1 - \lvert\Gamma\rvert^2)$.

### 3.1 Phasor telegrapher's equations

At one frequency, $\partial/\partial t \to j\omega$ in 13-07's equations, with loss included:

$$
\frac{d\mathbf{V}}{dz} = -(R' + j\omega L')\mathbf{I}, \qquad \frac{d\mathbf{I}}{dz} = -(G' + j\omega C')\mathbf{V} .
$$

Eliminating $\mathbf{I}$ gives $d^2\mathbf{V}/dz^2 = \gamma^2\mathbf{V}$, with

$$
\gamma = \alpha + j\beta = \sqrt{(R' + j\omega L')(G' + j\omega C')}, \qquad Z_0 = \sqrt{\frac{R' + j\omega L'}{G' + j\omega C'}} ,
$$

and solutions $\mathbf{V}(z) = V_0^+e^{-\gamma z} + V_0^-e^{\gamma z}$, $\mathbf{I}(z) = (V_0^+e^{-\gamma z} - V_0^-e^{\gamma z})/Z_0$. Compare 13-05's plane waves: $R' + j\omega L'$ plays the role of $j\omega\mu$, and $G' + j\omega C'$ that of $\sigma + j\omega\varepsilon$.

**Low-loss lines.** When $R' \ll \omega L'$ and $G' \ll \omega C'$, expanding the square roots to first order gives

$$
\beta \approx \omega\sqrt{L'C'}, \qquad Z_0 \approx \sqrt{\frac{L'}{C'}}, \qquad
\alpha \approx \underbrace{\frac{R'}{2Z_0}}_{\alpha_c} + \underbrace{\frac{G'Z_0}{2}}_{\alpha_d} .
$$

The conductor term grows as $\sqrt f$ (because $R' \propto R_s$, 13-05) and the dielectric term as $f$ (because $G' = \omega C'\tan\delta$). This is the formula behind Problem 13-05.13's coax loss.

### 3.2 Reflection along the line and input impedance

At the load ($d$ = 0), $\mathbf{V} = Z_L\mathbf{I}$ fixes $\Gamma_L$. Moving a distance $d$ toward the source, the forward wave is $e^{\gamma d}$ larger in phase and amplitude and the reflected one $e^{-\gamma d}$ smaller, so

$$
\Gamma(d) = \Gamma_Le^{-2\gamma d} .
$$

On a lossless line ($\gamma = j\beta$) the magnitude stays constant and the phase rotates clockwise by $2\beta d$: a full turn every half wavelength. With loss, it also shrinks by $e^{-2\alpha d}$. The impedance at any point follows from $Z = Z_0(1 + \Gamma)/(1 - \Gamma)$, which simplifies to the **input impedance** of a line of length ℓ terminated in $Z_L$:

$$
Z_{in} = Z_0\,\frac{Z_L + Z_0\tanh(\gamma\ell)}{Z_0 + Z_L\tanh(\gamma\ell)}
\quad\xrightarrow{\text{lossless}}\quad
Z_0\,\frac{Z_L + jZ_0\tan(\beta\ell)}{Z_0 + jZ_L\tan(\beta\ell)} .
$$

Special lengths of lossless line:

- **λ/2:** $\tan\beta\ell$ = 0, so $Z_{in} = Z_L$; a half-wave line is transparent (at that frequency).
- **λ/4:** $\tan\beta\ell \to \infty$, so $Z_{in} = Z_0^2/Z_L$; a quarter-wave line inverts the impedance (an open becomes a short).
- **Matched load** ($Z_L = Z_0$): $Z_{in} = Z_0$ for any length.

### 3.3 Stubs: reactances from line

Terminate a lossless line in a short or an open and the input is purely reactive:

$$
Z_{sc} = jZ_0\tan\beta\ell, \qquad Z_{oc} = -jZ_0\cot\beta\ell .
$$

A short shorted stub (ℓ < λ/4) is an inductor; a short open stub is a capacitor. Their equivalent values depend on frequency differently from lumped parts ($\tan$ against $\omega$), but near the design frequency they behave the same. At microwave frequencies stubs are easier to make precise than lumped inductors and capacitors, whose parasitics dominate (Example 13-08.3).

### 3.4 Standing waves, VSWR and power

The voltage magnitude along a lossless line is

$$
\lvert\mathbf{V}(d)\rvert = \lvert V_0^+\rvert\,\lvert 1 + \Gamma_Le^{-j2\beta d}\rvert ,
$$

varying between $\lvert V_0^+\rvert(1 + \lvert\Gamma_L\rvert)$ and $\lvert V_0^+\rvert(1 - \lvert\Gamma_L\rvert)$. Maxima occur where $\Gamma(d)$ is real and positive, minima where it is real and negative, a quarter wavelength apart. The **voltage standing-wave ratio** is

$$
\text{VSWR} = \frac{1 + \lvert\Gamma\rvert}{1 - \lvert\Gamma\rvert}, \qquad \lvert\Gamma\rvert = \frac{\text{VSWR} - 1}{\text{VSWR} + 1} .
$$

The current pattern is the same shape shifted by a quarter wavelength (current maxima at voltage minima). Measuring the VSWR and the position of a minimum is enough to find the load (Problem 13-08.7).

![Voltage magnitude against distance from the load over one wavelength for five loads on a 50 ohm line: a short and an open give full standing waves between 0 and 2 V, offset by a quarter wavelength; a matched load gives a flat 1 V; 100 ohm and 25 ohm loads both swing between 0.67 and 1.33 V but with maxima and minima swapped](../../../assets/figures/13-08/standing-waves.svg)

*Figure 1. Standing waves on a lossless 50 Ω line (load at the right). The short and the open give zeros every half wavelength; the 100 Ω and 25 Ω loads have the same VSWR of 2 but opposite positions of their maxima, which is how a slotted-line measurement tells them apart.*

**Power.** On a lossless line the time-average power flowing toward the load is the forward power minus the reflected power:

$$
P = \frac{\lvert V_0^+\rvert^2}{2Z_0}\left(1 - \lvert\Gamma_L\rvert^2\right) ,
$$

the same at every point. The fraction $1 - \lvert\Gamma\rvert^2$ in decibels is the **mismatch loss**; the reflected fraction in decibels is the **return loss**. A VSWR of 2 means $\lvert\Gamma\rvert$ = 1/3, a return loss of 9.5 dB and a mismatch loss of 0.51 dB.

### 3.5 The quarter-wave transformer

A quarter-wave section of impedance $Z_1$ between a line $Z_0$ and a resistive load $R_L$ presents $Z_1^2/R_L$. Choosing

$$
Z_1 = \sqrt{Z_0R_L}
$$

matches the load at the design frequency. Away from it the section is no longer a quarter wave, and a reflection appears. The bandwidth over which $\lvert\Gamma\rvert$ stays below a limit depends on the impedance ratio: small steps match over wide bands, large steps over narrow ones. Several quarter-wave sections in cascade, with gradually stepped impedances, widen the band (binomial and Chebyshev transformers, Course 21). This is the same structure as 13-06's antireflection coating.

### 3.6 Lossy lines and what loss hides

Loss shrinks the reflection on its way back: a load seen through a line of one-way loss $A$ dB has its return loss improved by $2A$ dB at the input. A badly mismatched antenna at the end of a long, lossy cable can look well matched at the radio, while the power it fails to radiate is dissipated in the cable on the way (Example 13-08.6). Measure mismatches at the device, or correct for the cable.

**The distortionless line.** In general α and the phase velocity depend on frequency, so pulses spread. Heaviside showed that if

$$
\frac{R'}{L'} = \frac{G'}{C'} ,
$$

then $\gamma = \sqrt{R'G'} + j\omega\sqrt{L'C'}$ exactly: α is independent of frequency, the velocity is constant, and $Z_0 = \sqrt{L'/C'}$ is real. Early telephone lines were loaded with series inductors ("loading coils") to approach this condition; modern links instead equalize the channel electronically (Course 24).

## 4. Worked examples

### Example 13-08.1 · A real coax at 1 GHz (tier A)

**Setup.** The coaxial line of 13-02 to 13-05 has $L'$ = 250.6 nH/m, $C'$ = 99.92 pF/m, $R'$ = 3.376 Ω/m at 1 GHz (Problem 13-05.13) and a polyethylene dielectric with $\tan\delta$ = 0.0002. Find $G'$, then γ and $Z_0$ exactly, and compare α with the low-loss formula.

**Solution.** $G' = \omega C'\tan\delta$ = **1.256 × 10⁻⁴** S/m. The exact square roots give α = **0.03686** Np/m (**0.3201** dB/m), β = **31.44** rad/m (a wavelength of **19.99** cm) and $Z_0$ = **50.08 − j0.04869** Ω. The low-loss formula $R'/(2Z_0) + G'Z_0/2$ gives the same α to four figures.

**Sanity check.** $Z_0$ is almost exactly the lossless value: its imaginary part is a thousandth of its real part, of order $(R'/\omega L' - G'/\omega C')/2$. Loss matters for attenuation long before it matters for impedance.

### Example 13-08.2 · Input impedance of λ/8, λ/4 and λ/2 lines (tier A)

**Setup.** A 100 Ω load terminates a lossless 50 Ω line. Find the input impedance for lengths of λ/8, λ/4 and λ/2.

**Solution.** At λ/8, $\tan\beta\ell$ = 1:

$$
Z_{in} = 50\,\frac{100 + j50}{50 + j100} = \mathbf{40 - j30}\ \Omega .
$$

At λ/4, $Z_{in} = 50^2/100$ = **25** Ω. At λ/2, $Z_{in} = Z_L$ = **100** Ω.

**Sanity check.** All three have the same $\lvert\Gamma\rvert$ = 1/3, as they must on a lossless line: $(40 - j30 - 50)/(40 - j30 + 50)$ has magnitude $\sqrt{100 + 900}/\sqrt{8100 + 900}$ = 1/3.

### Example 13-08.3 · Stubs as an inductor and a capacitor (tier B)

**Setup.** At 1 GHz, on a 50 Ω air line (λ = 29.98 cm), find the reactance and equivalent inductance of a 2 cm shorted stub, and the reactance and equivalent capacitance of a 5 cm open stub.

**Solution.** Shorted: βℓ = 2π × 2/29.98 = 0.4192 rad, so $X = 50\tan 0.4192$ = **22.28** Ω, equivalent to $X/\omega$ = **3.546** nH. Open: βℓ = 1.048 rad, so $X = -50\cot 1.048$ = **−28.82** Ω, equivalent to $1/(\omega\lvert X\rvert)$ = **5.523** pF.

**Sanity check.** For short stubs, $\tan\beta\ell \approx \beta\ell$ gives $L \approx L'\ell = Z_0\ell/c$ = **3.336** nH; the exact value is **6.3**% higher because βℓ = 0.42 rad is not small enough for the approximation. An open stub approaches $C'\ell$ in the same way.

### Example 13-08.4 · VSWR, return loss and delivered power (tier B)

**Setup.** A 75 Ω load terminates a lossless 50 Ω line carrying a forward wave of 10 V peak. Find Γ, VSWR, return loss, mismatch loss, the power delivered, and the maximum and minimum voltages on the line.

**Solution.** Γ = 25/125 = **0.2**, VSWR = 1.2/0.8 = **1.5**, return loss $-20\log 0.2$ = **13.98** dB, mismatch loss $-10\log 0.96$ = **0.1773** dB. Delivered power: $10^2/(2 \times 50) \times 0.96$ = **0.96** W. The voltage swings between 10 × 1.2 = **12** V (at the load, where Γ is real and positive) and 10 × 0.8 = **8** V, λ/4 toward the source.

**Sanity check.** A 75 Ω load on a 50 Ω system (connecting video cable to RF gear, say) reflects only 4% of the power: mismatches of this size cost little power but can matter for ripple and filter response.

### Example 13-08.5 · A quarter-wave transformer and its bandwidth (tier B)

**Setup.** Match a 100 Ω load to a 50 Ω line at 2.4 GHz with a quarter-wave section of coax whose velocity is $2c/3$. Find its impedance and length, and the fractional bandwidth over which $\lvert\Gamma\rvert$ < 0.1.

**Solution.** $Z_1 = \sqrt{50 \times 100}$ = **70.71** Ω. The wavelength in the coax is $(2c/3)/f$, so a quarter is **2.082** cm. Away from 2.4 GHz the section's electrical length is $90° \times f/f_0$; computing $Z_{in}$ and Γ against frequency and solving for $\lvert\Gamma\rvert$ = 0.1 gives a bandwidth of **36.70**% of the centre frequency.

**Sanity check.** At the band edges the section is about 74° or 106° long, far from a quarter wave, yet the reflection is still only 0.1: a 2:1 impedance step is mild. A 10:1 step would have a much narrower band for the same limit.

### Example 13-08.6 · A lossy cable hides a short circuit (tier C)

**Setup.** A cable with 3 dB of one-way loss is terminated in a short circuit. What return loss and VSWR does an instrument at the other end measure?

**Solution.** The reflected wave suffers the loss twice: $\lvert\Gamma_{in}\rvert = 10^{-6/20}$ = **0.5012**, a return loss of **6** dB and a VSWR of **3.010**, although the load reflects everything.

**Sanity check.** Each decibel of cable loss improves the apparent return loss by two. A mismatch measured through a long cable must be corrected for the cable, or measured at the device.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T 13-08.a | return loss at VSWR 2 | 9.5 | dB |
| T 13-08.b | mismatch loss at VSWR 2 | 0.51 | dB |
| Ex 13-08.1a | shunt conductance | 1.256 × 10⁻⁴ | S/m |
| Ex 13-08.1b | attenuation constant | 0.03686 | Np/m |
| Ex 13-08.1c | attenuation | 0.3201 | dB/m |
| Ex 13-08.1d | phase constant | 31.44 | rad/m |
| Ex 13-08.1e | wavelength on the line | 19.99 | cm |
| Ex 13-08.1f | Z0 real part | 50.08 | Ω |
| Ex 13-08.1g | Z0 imaginary part | −0.04869 | Ω |
| Ex 13-08.2a | λ/8 input resistance | 40 | Ω |
| Ex 13-08.2b | λ/8 input reactance | −30 | Ω |
| Ex 13-08.2c | λ/4 input impedance | 25 | Ω |
| Ex 13-08.2d | λ/2 input impedance | 100 | Ω |
| Ex 13-08.3a | shorted-stub reactance | 22.28 | Ω |
| Ex 13-08.3b | equivalent inductance | 3.546 | nH |
| Ex 13-08.3c | open-stub reactance | −28.82 | Ω |
| Ex 13-08.3d | equivalent capacitance | 5.523 | pF |
| Ex 13-08.3e | short-stub approximation L'ℓ | 3.336 | nH |
| Ex 13-08.3f | exact over approximate | 6.3 | % |
| Ex 13-08.4a | reflection coefficient | 0.2 | — |
| Ex 13-08.4b | VSWR | 1.5 | — |
| Ex 13-08.4c | return loss | 13.98 | dB |
| Ex 13-08.4d | mismatch loss | 0.1773 | dB |
| Ex 13-08.4e | delivered power | 0.96 | W |
| Ex 13-08.4f | maximum voltage | 12 | V |
| Ex 13-08.4g | minimum voltage | 8 | V |
| Ex 13-08.5a | transformer impedance | 70.71 | Ω |
| Ex 13-08.5b | transformer length | 2.082 | cm |
| Ex 13-08.5c | fractional bandwidth for Γ < 0.1 | 36.70 | % |
| Ex 13-08.6a | apparent reflection magnitude | 0.5012 | — |
| Ex 13-08.6b | apparent return loss | 6 | dB |
| Ex 13-08.6c | apparent VSWR | 3.010 | — |
| Prac 13-08.a | RG-58 loss at 1 GHz | 0.7054 | dB/m |
| Prac 13-08.b | 10 m of RG-58 at 1 GHz | 7.054 | dB |
| Prac 13-08.c | apparent return loss of a VSWR-2 antenna through it | 23.65 | dB |
| Sim 13-08.a | simulated λ/8 input resistance | 40 | Ω |
| Sim 13-08.b | simulated λ/8 input reactance | −30 | Ω |
| Sim 13-08.c | simulated quarter-wave transformer input | 50 | Ω |

*Every value is recomputed by [verify_13_08.py](../verify/verify_13_08.py): γ and $Z_0$ by complex square roots, input impedances by integrating the phasor telegrapher's equations numerically from the load to the input (an ODE solve, not the closed-form formula), standing-wave extrema by sampling the computed voltage, and bandwidths by root finding. The λ/8 line and the quarter-wave transformer are also simulated in ngspice.*

## 5. Simulate it

The lab, [labs/13-08-lab](../labs/13-08-lab/README.md), has a notebook and an ngspice netlist:

1. Plots standing-wave patterns of voltage and current for open, short, matched, resistive and reactive loads.
2. Traces $Z_{in}$ and Γ as the line lengthens: Γ circles the origin, the picture behind the Smith chart (13-09).
3. Plots a quarter-wave transformer's reflection against frequency for several impedance ratios.
4. Shows how cable loss improves apparent return loss, and checks the distortionless condition by sending a pulse down two lossy lines.

The netlist [line_impedance.cir](../labs/13-08-lab/line_impedance.cir) drives a λ/8 line with a 100 Ω load and a quarter-wave transformer with 1 A at 1 GHz and prints the input impedances.

**Guided exercise (predict, then run).** **Before running the netlist**, predict both input impedances. Then run it. (**40 − j30** Ω for the λ/8 line, and **50** Ω for the transformer.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Quarter-wave transformer (single section) | Simple, exact match at one frequency | Bandwidth shrinks as the impedance ratio grows | RF designer |
| Multi-section transformer | Bandwidth | Length, loss, layout area | RF designer |
| Stubs instead of lumped L and C | Predictable at microwave frequencies | Area, narrower bandwidth, dispersion | RF and microwave designer |
| Lower-loss cable or line | Signal level, noise figure | Cost, size, flexibility | System and RF engineers |
| Measuring at the device (calibration plane) | True match | Fixture design, calibration effort | Test engineer |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| λ/4 line | $Z_{in} = Z_0^2/Z_L$ | Inverts; open ↔ short |
| λ/2 line | $Z_{in} = Z_L$ | Repeats |
| VSWR 1.5 | Γ = 0.2, RL 14.0 dB, ML 0.18 dB | Common component spec |
| VSWR 2 | Γ = 1/3, RL 9.5 dB, ML 0.51 dB | Common antenna spec |
| Loss masking | RL improves by 2 dB per dB of line loss | Measure at the device |
| RG-58 at 1 GHz | 0.71 dB/m | 21.5 dB/100 ft, as of Nov 2026 [1] |

## 8. Common mistakes

- **Measuring distance from the wrong end.** $\Gamma(d) = \Gamma_Le^{-2\gamma d}$ uses distance from the load.
- **Forgetting the factor of 2 in the phase.** The reflection coefficient rotates by $2\beta d$, a full turn per half wavelength.
- **Mixing return loss signs.** Return loss is positive in dB; $S_{11}$ in dB is negative. Say which you mean.
- **Trusting a VSWR measured through a long cable.** Loss improves it by twice the cable's loss in dB.
- **Using a quarter-wave transformer for a complex load directly.** It matches only a real impedance; add a length of line first to make the load real (13-09).

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Cable loss figures.** Belden specifies RG-58 (8262) at 21.5 dB per 100 ft at 1 GHz [1] **[Established]**: **0.7054** dB/m, so 10 m loses **7.054** dB (our arithmetic). An antenna with a VSWR of 2 (return loss 9.54 dB) at the end of that cable shows an apparent return loss of **23.65** dB at the radio: a "great match" that is really a lossy cable.
- **Impedance is specified as return loss.** Interface and component specifications typically state return-loss masks against frequency rather than impedance tolerances, because return loss is what a network analyzer measures directly **[Established]** (industry practice).
- **Distributed matching is routine on chips and boards.** Millimetre-wave transceivers use on-chip transmission-line stubs and quarter-wave transformers because lumped elements are too lossy or self-resonant there **[Established]** (textbook practice; Course 21).

### Why it matters commercially

- **Power amplifier efficiency and battery life.** A mismatched antenna reflects power back into the PA; phones use tunable matching networks to keep the match as hands and heads detune the antenna.
- **Link budgets.** Every decibel of cable or board loss and every decibel of mismatch loss comes out of the margin that determines range or data rate.
- **Test economics.** VNA measurements and their calibration standards (short, open, load, through) are built on the input-impedance relations of this chapter.

### Marketing vs Reality

- **"VSWR below 1.5 across the band."** *Reality:* measured where? Through how much cable? *Sanity check:* ask for the reference plane and whether the cable loss was de-embedded.
- **"Broadband match."** *Reality:* a single quarter-wave section matches a 2:1 step over about 37% of its centre frequency for |Γ| < 0.1 (Example 13-08.5), much less for larger steps. *Sanity check:* ask for |Γ| against frequency and the number of matching sections.

### Questions for engineering leaders

1. **"Where is your reference plane for antenna match, and how did you remove the cable?"**
   *Strong:* calibration at the antenna connector, or de-embedding with a measured cable model. *Evasive:* "we measured at the radio."
2. **"How does your antenna match change when a user holds the device?"**
   *Strong:* measured detuning with hand and head phantoms, and a tunable matching network or margin to cover it. *Evasive:* "the antenna is designed for 50 Ω."
3. **"What is the loss budget from your PA to the antenna?"**
   *Strong:* a line-item budget (trace, switch, filter, cable, mismatch) in dB. *Evasive:* a single "less than 2 dB."

## 10. Concept check

**Q1.** Why does a quarter-wave line invert impedance?

<details><summary>Answer</summary>

The reflection coefficient rotates by $2\beta\ell$ = 180° over a quarter wavelength, so Γ becomes −Γ, and $Z_0(1 - \Gamma)/(1 + \Gamma) = Z_0^2/Z_L$: a high impedance becomes low and vice versa.

</details>

**Q2.** Why does $\lvert\Gamma\rvert$ stay constant along a lossless line but shrink on a lossy one?

<details><summary>Answer</summary>

$\Gamma(d) = \Gamma_Le^{-2\gamma d}$; with γ = jβ only the phase changes. With α > 0, the reflected wave is attenuated relative to the forward wave by $e^{-2\alpha d}$ (once going out and once coming back).

</details>

**Q3.** What do return loss and mismatch loss measure?

<details><summary>Answer</summary>

Return loss is the reflected power relative to the incident, in dB ($-20\log\lvert\Gamma\rvert$); mismatch loss is the reduction in delivered power, $-10\log(1 - \lvert\Gamma\rvert^2)$. A large return loss means a small mismatch loss.

</details>

**Q4.** Why can a shorted stub act as a capacitor?

<details><summary>Answer</summary>

$Z_{sc} = jZ_0\tan\beta\ell$ is inductive for βℓ below 90° and capacitive between 90° and 180°: a shorted stub between a quarter and a half wavelength long is capacitive.

</details>

**Q5.** What does the distortionless condition buy?

<details><summary>Answer</summary>

With $R'/L' = G'/C'$, the attenuation and the velocity are independent of frequency and $Z_0$ is real, so a pulse arrives smaller but undistorted.

</details>

**Q6.** Why does cable loss make a bad load look good?

<details><summary>Answer</summary>

The reflected wave crosses the cable twice, so its level at the input falls by twice the cable loss in dB, improving the apparent return loss; the power missing from the reflection is heat in the cable, not power delivered.

</details>

Next: the [13-08 problem set](../problems/13-08-problems.md).

## 11. Key terms

[Propagation constant](../../../reference/glossary.md#propagation-constant) · [Characteristic impedance](../../../reference/glossary.md#characteristic-impedance) · [Input impedance](../../../reference/glossary.md#input-impedance) · [Reflection coefficient](../../../reference/glossary.md#reflection-coefficient) · [Voltage standing-wave ratio](../../../reference/glossary.md#voltage-standing-wave-ratio-vswr) · [Return loss](../../../reference/glossary.md#return-loss) · [Mismatch loss](../../../reference/glossary.md#mismatch-loss) · [Stub](../../../reference/glossary.md#stub) · [Quarter-wave transformer](../../../reference/glossary.md#quarter-wave-transformer) · [Distortionless line](../../../reference/glossary.md#distortionless-line)

## 12. Connections

- **Builds on:** the time-domain line of [13-07](13-07-transmission-lines-time-domain.md); lossy propagation and $R_s$ from [13-05](13-05-plane-waves.md); phasors from [07-05](../../07-circuit-analysis-2-transient-and-ac/chapters/07-05-sinusoidal-steady-state-and-impedance.md); layers as impedance transformers in [13-06](13-06-reflection-and-transmission.md).
- **Next:** [13-09 The Smith Chart and Impedance Matching](13-09-smith-chart-and-matching.md) turns these relations into a graphical tool and designs matching networks.
- **Used later:** waveguides as lines ([13-10](13-10-waveguides-and-resonators.md)); RF design in Course 21; channel loss and equalization in Course 24.

## 13. Further study

- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 2.
- D. M. Pozar, *Microwave Engineering*, ch. 2 (transmission-line theory) and ch. 5 (quarter-wave transformers).
- D. K. Cheng, *Field and Wave Electromagnetics*, ch. 9.

## 14. Sources

1. Belden 8262 RG-58 coaxial cable data sheet. [R-194](../../../reference/research-log.md#r-194--rg-58-coaxial-cable-data-sheets).

The physics (phasor line theory, matching) is textbook material (Further study).
