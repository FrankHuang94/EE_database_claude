<!-- status: verified -->
# 21-03 · Noise Figure and Linearity

| | |
|---|---|
| **Course** | [21 · RF and Microwave Engineering](../README.md) |
| **University equivalent** | The receiver-performance chapters of a senior RF circuits course: two-port noise parameters and noise circles, noise-figure measurement, memoryless nonlinearity, gain compression, second- and third-order intercepts, cascaded linearity, blocking, reciprocal mixing and dynamic range (Razavi, *RF Microelectronics*, the chapter on basic concepts in RF design; Pozar, *Microwave Engineering*, the chapter on noise and nonlinear distortion) |
| **Prerequisites** | [17-02](../../17-communication-systems/chapters/17-02-noise-and-snr.md) (noise temperature, noise figure, the Friis cascade, sensitivity), [12-10](../../12-electronics-2/chapters/12-10-noise-in-circuits.md) (input-referred $e_n$ and $i_n$, optimum source resistance), [21-01](21-01-s-parameters.md) (reflection coefficients), [21-02](21-02-impedance-matching-networks.md) (matching) |
| **Estimated study hours** | 8 |
| **Last verified** | 2026-11-24 |

**Learning objectives.** After this chapter you can:

1. Derive a two-port's noise factor as a function of its source admittance from its noise parameters ($F_{min}$, $R_n$, $\Gamma_{opt}$), and draw noise circles.
2. Measure noise figure with the Y-factor method, including the cold-temperature and second-stage corrections.
3. Derive harmonics, gain compression, and second- and third-order intermodulation from a memoryless polynomial, and extract IIP2 and IIP3 from a two-tone test.
4. Compute the noise figure and IIP3 of a receiver chain, and explain why gain helps one and hurts the other.
5. Quantify desensitization by a blocker, through gain compression and through reciprocal mixing with local-oscillator phase noise.
6. Compute sensitivity and spurious-free dynamic range, and reconstruct a published 3GPP reference-sensitivity figure from its noise-figure assumption.

## 1. Big picture

A receiver has to hear a whisper while someone shouts nearby. The whisper sets a floor: the wanted signal must stay above the receiver's own noise, which is what noise figure measures. The shout sets a ceiling: strong unwanted signals (blockers) drive the amplifiers and mixers into their nonlinear region, where they compress the wanted signal, generate new frequencies that land on top of it, and mix the local oscillator's noise into the channel. Everything a radio designer does at the front end is a negotiation between that floor and that ceiling. Chapter 17-02 built the floor for a system engineer: noise temperature, noise figure, the Friis cascade and sensitivity. This chapter adds what the circuit designer controls: how a transistor's noise depends on the impedance it sees, how noise figure is measured, and the whole ceiling, from compression and intercept points to blocking and dynamic range.

- **Every receiver specification** is a list of floor and ceiling numbers: reference sensitivity, adjacent-channel selectivity, blocking, intermodulation, maximum input level (§9).
- **Every LNA data sheet** quotes a noise figure at a stated source impedance and an input IP3 from one two-tone test; reading them correctly needs both halves of this chapter.
- **Zero-IF receivers**, now dominant in phones, Wi-Fi and IoT radios, live or die by second-order linearity (IIP2), because their second-order products land at DC (21-08).
- **Phase noise becomes a noise figure problem** in the presence of a blocker, through reciprocal mixing (§3.8, 21-06).

## 2. Intuition first

![Output power in dBm against input power in dBm, both on decibel axes: the fundamental rises with slope 1 and bends over near the top; the third-order product rises with slope 3; the dashed straight-line extensions of both meet at the third-order intercept point, about 9 dB above the input 1 dB compression point; a horizontal noise-floor line at the bottom marks where the spurious-free dynamic range begins](../../../assets/figures/21-03/intercept.svg)

*Figure 1. The floor and the ceiling on one plot. The fundamental grows 1 dB per dB, the third-order intermodulation product 3 dB per dB; their extrapolations cross at the intercept point (IP3), which no real amplifier reaches. The spurious-free dynamic range is the window between the noise floor and the input at which the third-order product reaches it.*

**A trading-desk analogy.** Think of a market maker quoting a price. Noise figure is the bid–ask spread: a cost charged on every trade, however small, and charged again by every intermediary in the chain, though later intermediaries matter less once the first has added volume (gain). Nonlinearity is market impact: small orders move the price in proportion, but a large order moves it disproportionately, and a very large order elsewhere in the book (a blocker) moves the price you get on your own small order. The analogy breaks in one important way: market impact is roughly one-sided, while an amplifier's nonlinearity creates entirely new frequencies, so a shout at one frequency can bury a whisper at another.

## 3. Theory

### 3.1 Noise figure and the cascade: a recap

From 17-02, a two-port's **noise factor** compares the signal-to-noise ratio at its input and output with the input noise fixed by a matched source at $T_0$ = 290 K:

$$
F = \frac{S_i/N_i}{S_o/N_o} = 1 + \frac{T_e}{T_0}, \qquad \text{NF} = 10\log_{10}F\ \text{dB},
$$

where $T_e$ is the two-port's equivalent input noise temperature. The available noise density of a matched source at $T_0$ is $kT_0$ = **−173.98** dBm/Hz, usually rounded to −174 [10, 5]. In a cascade, each stage's excess noise is divided by the available gain in front of it (the Friis formula):

$$
F_{tot} = F_1 + \frac{F_2 - 1}{G_1} + \frac{F_3 - 1}{G_1G_2} + \cdots ,
$$

and a passive loss $L$ at $T_0$ has $F = L$. Two facts carry the whole chapter: the first stage dominates the noise once its gain is large, and the gains are **available** gains, which depend on the impedances between stages. The rest of this section asks how the first stage's $F$ depends on the impedance driving it.

### 3.2 Noise parameters: why the source impedance matters

**The model.** Any noisy linear two-port can be replaced by the same two-port made noiseless, preceded by two noise sources at its input: a series voltage $e_n$ and a shunt current $i_n$ (12-10 used this model with a resistive source). At radio frequencies the two are usually **correlated**, because both arise partly from the same physical noise (in a FET, the channel's thermal noise appears at the drain and, through the gate capacitance, at the gate). Split the current into a part fully correlated with $e_n$ and an uncorrelated remainder,

$$
i_n = Y_{cor}\,e_n + i_u ,
$$

with $Y_{cor} = G_{cor} + jB_{cor}$ the **correlation admittance**. Express each density as an equivalent resistor or conductor at $T_0$: $\overline{e_n^2} = 4kT_0R_n\Delta f$ and $\overline{i_u^2} = 4kT_0G_u\Delta f$, where $R_n$ (Ω) is the **noise resistance** and $G_u$ (S) the uncorrelated noise conductance.

**The noise factor.** Drive the two-port from a source admittance $Y_s = G_s + jB_s$, whose own noise current has $\overline{i_s^2} = 4kT_0G_s\Delta f$. Convert everything to a Norton current at the input: the voltage source $e_n$ in series with $Y_s$ becomes a current $Y_se_n$, so the total noise current driving the input node is $i_s + i_n + Y_se_n = i_s + i_u + (Y_s + Y_{cor})e_n$. The three terms are independent ($i_s$ belongs to the source, $i_u$ is uncorrelated by construction), so their mean squares add, and the noise factor is the total divided by the source's share:

$$
F = 1 + \frac{\overline{i_u^2} + \lvert Y_s + Y_{cor}\rvert^2\,\overline{e_n^2}}{\overline{i_s^2}} = 1 + \frac{G_u + R_n\left[(G_s + G_{cor})^2 + (B_s + B_{cor})^2\right]}{G_s} .
$$

**The optimum source.** The susceptance appears only in the squared term, so $F$ is smallest at $B_s = B_{opt} = -B_{cor}$: tune out the correlation susceptance. With that, $F = 1 + [G_u + R_n(G_s + G_{cor})^2]/G_s$; setting $\partial F/\partial G_s = 0$ gives $R_nG_s^2 = G_u + R_nG_{cor}^2$, so

$$
G_{opt} = \sqrt{\frac{G_u}{R_n} + G_{cor}^2}, \qquad F_{min} = 1 + 2R_n\left(G_{opt} + G_{cor}\right) .
$$

**The standard form.** Expanding $F$ around the optimum (add and subtract $F_{min}$ and complete the square) gives the result of Rothe and Dahlke and of the IRE noise subcommittee led by Haus [3, 4]:

$$
F = F_{min} + \frac{R_n}{G_s}\,\lvert Y_s - Y_{opt}\rvert^2 , \qquad Y_{opt} = G_{opt} + jB_{opt} .
$$

Four real numbers, $F_{min}$, $R_n$ and the complex $Y_{opt}$, describe a two-port's noise completely and do not depend on the circuit outside it; data sheets and Touchstone files (21-01) give them as $F_{min}$, $\Gamma_{opt}$ and $R_n$. In reflection-coefficient form, with $r_n = R_n/Z_0$,

$$
F = F_{min} + \frac{4r_n\,\lvert\Gamma_s - \Gamma_{opt}\rvert^2}{\left(1 - \lvert\Gamma_s\rvert^2\right)\lvert 1 + \Gamma_{opt}\rvert^2} .
$$

$R_n$ is the **sensitivity**: a device with a small $R_n$ tolerates a mismatched source, one with a large $R_n$ punishes it.

> **Math refresher — completing the square.** For $f(x) = ax^2 + bx + c$ with $a > 0$, write $f = a(x + b/2a)^2 + c - b^2/4a$: the minimum is $c - b^2/4a$ at $x = -b/2a$, and the distance from the minimum is a perfect square. The noise factor is a quadratic in $G_s$ and $B_s$ divided by $G_s$, and the same move turns it into a minimum plus a squared distance from the optimum.

**Noise circles.** Setting $F$ to a constant $F_i$ in the reflection form and rearranging (it is a circle equation in $\Gamma_s$) gives circles with

$$
N = \frac{F_i - F_{min}}{4r_n}\,\lvert 1 + \Gamma_{opt}\rvert^2, \qquad C_F = \frac{\Gamma_{opt}}{N + 1}, \qquad R_F = \frac{\sqrt{N\left(N + 1 - \lvert\Gamma_{opt}\rvert^2\right)}}{N + 1} .
$$

As $F_i \to F_{min}$ the circle shrinks to $\Gamma_{opt}$; as $F_i$ grows, it widens and its centre slides toward the origin (Figure 2, Example 21-03.3).

**Noise match versus power match.** The source reflection that minimizes noise, $\Gamma_{opt}$, is generally not the one that maximizes gain, $\Gamma_s = \Gamma_{in}^*$ (21-01). A low-noise amplifier's input is therefore usually matched for noise, and its input return loss can look poor: 21-02 §9 showed a Wi-Fi front end with a 7 dB return loss next to a 1.8 dB noise figure. The design techniques that bring the two optima together (inductive source degeneration) are the subject of 21-04.

![Source reflection plane with the unit circle, the minimum-noise point Gamma_opt at 0.45 at 60 degrees, two noise circles for 1.0 and 1.5 dB centred on the line from the origin to Gamma_opt, the matched point at the origin lying just outside the 1.0 dB circle, and the conjugate-match point at 0.6 at minus 40 degrees lying outside the 1.5 dB circle](../../../assets/figures/21-03/noise-circles.svg)

*Figure 2. Noise circles for the device of Example 21-03.3. A 50 Ω source costs 0.27 dB over the minimum; matching for maximum gain instead costs 1.24 dB.*

### 3.3 Measuring noise figure: the Y-factor method

Noise figure is a ratio of noise powers, and the cleanest way to measure a ratio is to switch between two known inputs. A **noise source** (an avalanche diode behind an attenuator) presents a matched source at a hot temperature $T_h$ when on and at the ambient temperature $T_c$ when off. Its **excess noise ratio** is defined as [5]

$$
\text{ENR} = \frac{T_h - T_c}{T_0} \qquad\text{(with } T_c = T_0 \text{ in the definition)},
$$

so an ENR of 0 dB is a 290 K difference ($T_h$ = 580 K), not "noise equal to $kTB$", a common misreading the application note warns against [5]. The device's output noise power is proportional to the source temperature plus its own $T_e$, so the ratio of the two readings, the **Y-factor**, is

$$
Y = \frac{N_{on}}{N_{off}} = \frac{T_h + T_e}{T_c + T_e} \quad\Longrightarrow\quad T_e = \frac{T_h - YT_c}{Y - 1} .
$$

With $T_c = T_0$ and $T_h = T_0(\text{ENR} + 1)$, $F = 1 + T_e/T_0$ simplifies to

$$
F = \frac{\text{ENR}}{Y - 1} ,
$$

and if the cold source is at a different temperature, $F = [\text{ENR} - Y(T_c/T_0 - 1)]/(Y - 1)$ [5]. Only a ratio of powers enters, so the analyzer's absolute power accuracy does not matter. Two corrections remain. The analyzer has its own noise figure $F_2$, so the measurement gives the cascade $F_{12}$, and Friis in reverse recovers the device: $F_1 = F_{12} - (F_2 - 1)/G_1$, with $G_1$ measured from the same on/off powers. And the method loses resolution when $Y$ approaches 1: the application note's rule is that it is "not used when the noise figure is more than 10 dB above the ENR of the noise source" [5].

### 3.4 Memoryless nonlinearity

Every amplifier is nonlinear. When the nonlinearity is fast compared with the signal (no memory), expand the output in a power series of the input:

$$
y(t) = a_1x(t) + a_2x^2(t) + a_3x^3(t) + \cdots ,
$$

where $a_1$ is the small-signal gain. For a bipolar transistor driven at the base, $i_C = I_Se^{(V_{BE} + v)/V_T} = I_C(1 + v/V_T + v^2/2V_T^2 + v^3/6V_T^3 + \cdots)$, so $a_1 = I_C/V_T$, $a_2 = I_C/(2V_T^2)$ and $a_3 = I_C/(6V_T^3)$. For an emitter-coupled pair, the differential output current is $I_{EE}\tanh(v_d/2V_T)$ (12-01), whose series $u - u^3/3 + \cdots$ has no even terms: $a_1 = I_{EE}/(2V_T)$, $a_2 = 0$ and $a_3 = -I_{EE}/(24V_T^3)$.

**One tone: harmonics and compression.** With $x = A\cos\omega t$, use $\cos^2\theta = (1 + \cos 2\theta)/2$ and $\cos^3\theta = (3\cos\theta + \cos 3\theta)/4$:

$$
y = \frac{a_2A^2}{2} + \left(a_1A + \frac{3a_3A^3}{4}\right)\cos\omega t + \frac{a_2A^2}{2}\cos 2\omega t + \frac{a_3A^3}{4}\cos 3\omega t .
$$

The second and third **harmonic distortion** ratios are $\text{HD}_2 = \tfrac12\lvert a_2/a_1\rvert A$ and $\text{HD}_3 = \tfrac14\lvert a_3/a_1\rvert A^2$. The fundamental's gain is $a_1 + \tfrac34a_3A^2$: if $a_3$ has the opposite sign to $a_1$ (as in the differential pair and in almost every amplifier at large signals), the gain falls as the input grows. The **1 dB compression point** is the input amplitude at which it has fallen by 1 dB:

$$
20\log_{10}\left\lvert 1 - \frac34\left\lvert\frac{a_3}{a_1}\right\rvert A_{1dB}^2\right\rvert = -1 \quad\Longrightarrow\quad A_{1dB} = \sqrt{0.145\left\lvert\frac{a_1}{a_3}\right\rvert} ,
$$

since $\tfrac34\lvert a_3/a_1\rvert A^2 = 1 - 10^{-1/20}$ = **0.1087** and $\tfrac43 \times 0.1087$ = **0.145**. A bare bipolar transistor driven by a voltage is the exception: its $a_3$ has the same sign as $a_1$, so its gain *expands* until the bias shifts; compression in real amplifiers comes from degeneration, the load line and the supply.

### 3.5 Two tones: intermodulation and intercept points

Harmonics of a narrowband signal fall far out of band and a filter removes them. The damage is done when two signals mix. Let $x = A\cos\omega_1t + A\cos\omega_2t$ with $\omega_1$ and $\omega_2$ close together. Expanding $x^2$ gives, besides harmonics and DC, terms at $\omega_1 \pm \omega_2$ with amplitude $a_2A^2$: the **second-order intermodulation** (IM2). Expanding $x^3$ (collect the terms $3A^3\cos^2\omega_1t\cos\omega_2t$ and use the identities above) gives terms at $2\omega_1 - \omega_2$ and $2\omega_2 - \omega_1$ with amplitude $\tfrac34a_3A^3$: the **third-order intermodulation** (IM3). The IM3 products lie at $\omega_1 - (\omega_2 - \omega_1)$ and $\omega_2 + (\omega_2 - \omega_1)$, right next to the tones: if two blockers sit at offsets Δ and 2Δ from a wanted channel, one of their IM3 products lands exactly on it, and no filter can remove it.

**Intercept points.** At small inputs the fundamental grows as $A$ (slope 1 on a dB plot), IM3 as $A^3$ (slope 3) and IM2 as $A^2$ (slope 2). The input amplitude at which the extrapolated IM3 would equal the extrapolated fundamental is the **input third-order intercept**:

$$
a_1A_{IIP3} = \frac34\lvert a_3\rvert A_{IIP3}^3 \quad\Longrightarrow\quad A_{IIP3} = \sqrt{\frac43\left\lvert\frac{a_1}{a_3}\right\rvert} ,
$$

and similarly $A_{IIP2} = \lvert a_1/a_2\rvert$. The intercepts are extrapolations, not operating points: the amplifier compresses long before it gets there. Dividing the two results, $A_{IIP3}/A_{1dB} = \sqrt{(4/3)/0.145}$, so for a cubic nonlinearity

$$
\text{IIP3} - P_{1dB} = 20\log_{10}\sqrt{\frac{4/3}{0.145}} = 9.64\ \text{dB}
$$

(**9.64** dB, from the exact 0.1087 rather than the rounded 0.145). Real devices have higher-order terms too, and the spread in data sheets is several decibels either side (§9).

**Measuring them.** Apply two equal tones of $P_{in}$ dBm each and read the output fundamental $P_{fund}$ and the output IM3 $P_{IM3}$, both in dBm. Because the gap between them closes 2 dB per dB of input, it closes to zero after $(P_{fund} - P_{IM3})/2$ more decibels of input:

$$
\text{IIP3} = P_{in} + \frac{P_{fund} - P_{IM3}}{2}, \qquad \text{IIP2} = P_{in} + (P_{fund} - P_{IM2}) .
$$

These hold only in the small-signal region, where the slopes really are 1, 2 and 3; a measurement taken too close to compression gives a wrong intercept (Example 21-03.1). Equivalently, the IM3 level relative to the fundamental is $-2(\text{IIP3} - P_{in})$ dBc.

**Why IIP2 matters.** In a superheterodyne receiver, IM2 products near DC are filtered away. In a zero-IF receiver the wanted signal itself is converted to DC, so the IM2 products of any two strong signals, or the envelope of a single amplitude-modulated blocker, demodulate straight into the baseband [6, 7]. In frequency-division duplex phones the strongest such signal is the phone's own transmitter leaking through the duplexer (Problem 21-03.13).

### 3.6 Cascaded linearity

Let stage 1 have polynomial coefficients $a_1, a_3$ and stage 2 have $b_1, b_3$. Substituting $y_1 = a_1x + a_3x^3$ into $y_2 = b_1y_1 + b_3y_1^3$ and keeping terms to third order gives an overall cubic coefficient $a_3b_1 + b_3a_1^3$, against an overall gain $a_1b_1$. The cascade's intercept therefore satisfies

$$
\frac{1}{A_{IIP3}^2} = \frac34\left\lvert\frac{a_3b_1 + b_3a_1^3}{a_1b_1}\right\rvert \le \frac{1}{A_{IIP3,1}^2} + \frac{a_1^2}{A_{IIP3,2}^2} ,
$$

with equality when the two cubic terms add in phase (the worst case, and the usual assumption). In power units, with $G_1$ the first stage's power gain,

$$
\frac{1}{\text{IIP3}_{tot}} = \frac{1}{\text{IIP3}_1} + \frac{G_1}{\text{IIP3}_2} + \frac{G_1G_2}{\text{IIP3}_3} + \cdots \qquad\text{(linear units, e.g. mW)} .
$$

Compare it with Friis: there, gain *divides* later stages' noise; here, gain *multiplies* later stages' nonlinearity, because they see larger signals. The first stage sets the noise figure; the last stages usually set the intercept. More LNA gain improves the noise figure and degrades IIP3 at the same time (Example 21-03.5), which is why receivers switch LNA gain in steps as the signal grows.

### 3.7 Blocking and desensitization by compression

A strong blocker of amplitude $A_B$ and a weak wanted signal $A_w$ pass through the same nonlinearity. Expanding $a_3(A_w\cos\omega_wt + A_B\cos\omega_Bt)^3$ and keeping the term in $A_wA_B^2$ at $\omega_w$ gives a wanted-signal gain of

$$
a_1 + \frac32a_3A_B^2 = a_1\left(1 - \frac{2A_B^2}{A_{IIP3}^2}\right)
$$

(using $\tfrac32\lvert a_3/a_1\rvert = 2/A_{IIP3}^2$). The coefficient is $3/2$, twice the $3/4$ of self-compression, so a blocker reduces the gain of a small signal by 1 dB at an amplitude $\sqrt2$ smaller than the amplifier's own 1 dB compression point: 3 dB lower in power. The receiver is **desensitized**: the wanted signal shrinks while the noise from later stages does not. If the blocker is amplitude-modulated, the same term transfers its modulation onto the wanted signal (**cross-modulation**).

### 3.8 Reciprocal mixing

The local oscillator that converts the signal to baseband (21-05) is not a pure tone: its phase noise $\mathcal{L}(\Delta f)$ (dBc/Hz, 20-10, 21-06) spreads its power over nearby frequencies. The mixer multiplies every input signal by the whole LO spectrum, so a blocker at offset Δf from the wanted channel is mixed by the LO's noise skirt at that offset straight into the channel. In a channel of bandwidth $B$ the resulting noise is

$$
N_{rm} = P_B + \mathcal{L}(\Delta f) + 10\log_{10}B\ \text{dBm},
$$

with $P_B$ the blocker power in dBm, assuming the phase noise is flat across the channel. It adds to the thermal floor $kT_0B\cdot F$ like any other noise. This is why receiver blocking tests are as much a test of the LO as of the LNA (Example 21-03.7).

### 3.9 Sensitivity and dynamic range

**Sensitivity.** The weakest signal a receiver can demodulate is its noise floor plus the signal-to-noise ratio the demodulator needs (17-02):

$$
P_{sens} = -174\ \text{dBm/Hz} + 10\log_{10}B + \text{NF} + \text{SNR}_{min}\ (+\ \text{margins}) .
$$

3GPP writes exactly this for 5G handsets, with an implementation margin and a diversity gain added, and the published reference sensitivities can be reconstructed from it (Example 21-03.6) [8, 9].

**Spurious-free dynamic range.** At the bottom the input-referred noise floor is $N = -174 + 10\log_{10}B + \text{NF}$ dBm. At the top, two equal input tones of $P_{in}$ create input-referred IM3 products at $3P_{in} - 2\,\text{IIP3}$ dBm. The largest input with no visible spurious product is the one where IM3 just reaches the floor, $3P_{in} - 2\,\text{IIP3} = N$, so $P_{in} = (2\,\text{IIP3} + N)/3$, and

$$
\text{SFDR} = P_{in} - N = \frac23\left(\text{IIP3} - N\right)\ \text{dB}.
$$

The factor 2/3 is worth remembering: 3 dB more intercept buys only 2 dB more dynamic range, and a 1 dB worse noise figure costs 2/3 dB.

> **Going deeper — what the polynomial misses.** The power series assumes the nonlinearity has no memory and that two tones are representative. Real amplifiers have bias networks and thermal time constants that make IM3 depend on tone spacing, odd-order terms beyond the cubic that bend the IM3 slope away from 3 near compression, and modulated signals whose peak-to-average ratio matters more than any single-tone figure. Volterra series extend the analysis to circuits with memory; Razavi's and Pozar's texts give the starting points [1, 2].

## 4. Worked examples

All powers are in dBm referred to 50 Ω; "dBc" is relative to the fundamental at the same port. Voltage amplitudes are peak values; a peak amplitude $A$ across 50 Ω carries $A^2/100$ W.

### Example 21-03.1 · Reading a two-tone test (tier A)

**Setup.** An amplifier is driven with two tones of −30 dBm each. Each output tone is −12 dBm, the output IM3 products are −72 dBm and the output IM2 product at the difference frequency is −60 dBm. Find the gain, IIP3, OIP3 and IIP2. Predict the IM3 level at −40 dBm per tone, and estimate the input 1 dB compression point from the cubic model.

**Solution.**

- Gain $G$ = −12 − (−30) = **18** dB.
- $\text{IIP3} = -30 + (-12 + 72)/2$ = **0** dBm; $\text{OIP3} = \text{IIP3} + G$ = **18** dBm.
- $\text{IIP2} = -30 + (-12 + 60)$ = **18** dBm.
- At −40 dBm per tone, IM3 is $-2(0 + 40)$ = **−80** dBc; the output tones are **−22** dBm and the IM3 products **−102** dBm. Ten decibels less input bought 30 dB less IM3.
- Cubic model: $P_{1dB} \approx \text{IIP3} - 9.64$ = **−9.6** dBm.

**Units check.** dBm − dBm = dB; dB added to dBm gives dBm.

**Sanity check.** At −30 dBm in, the amplifier is 20 dB below its estimated compression point, so the slopes 1 and 3 hold and the extrapolation is legitimate.

### Example 21-03.2 · A Y-factor measurement (tier A)

**Setup.** A noise source with ENR = 15.0 dB drives an LNA of 20 dB gain, followed by a spectrum analyzer with an 8 dB noise figure. The measured Y-factor is 13.5 dB with the source off at 290 K. Find the system noise figure, the LNA's noise figure, and its noise temperature. Repeat if the source's cold temperature is really 300 K.

**Solution.**

- ENR = $10^{1.5}$ = 31.62 and $Y = 10^{1.35}$ = 22.39, so $F_{12} = 31.62/21.39$ = 1.478: system NF = **1.70** dB.
- Second-stage correction: $F_1 = 1.478 - (6.31 - 1)/100$ = 1.425: LNA NF = **1.54** dB; $T_e = (F_1 - 1)\times 290$ = **123** K.
- With $T_c$ = 300 K: $F_{12} = [31.62 - 22.39(300/290 - 1)]/21.39$ = 1.443, NF **1.59** dB; corrected LNA NF **1.43** dB.

**Units check.** ENR and Y are power ratios; temperatures in K.

**Sanity check.** The analyzer's 8 dB noise figure adds only **0.16** dB, because 20 dB of LNA gain divides its excess noise by 100. A 10 K error in the cold temperature moves the answer by **0.11** dB, more than the difference between many competing LNAs.

### Example 21-03.3 · Noise parameters and noise circles (tier B)

**Setup.** A transistor at 2.4 GHz has $\text{NF}_{min}$ = 0.80 dB, $R_n$ = 8 Ω and $\Gamma_{opt} = 0.45\angle 60°$ in a 50 Ω system. (a) What noise figure does it give with a 50 Ω source? (b) With the source that conjugate-matches its input for maximum gain, $\Gamma_s = 0.6\angle{-40°}$? (c) Find the 1.0 dB and 1.5 dB noise circles.

**Solution.**

- $r_n = 8/50$ = 0.16, $F_{min} = 10^{0.08}$ = 1.202, and $\lvert 1 + \Gamma_{opt}\rvert^2 = (1 + 0.225)^2 + 0.3897^2$ = 1.652.
- (a) $\Gamma_s = 0$: $F = 1.202 + 4(0.16)(0.45)^2/1.652$ = 1.281, NF = **1.07** dB.
- (b) $\lvert\Gamma_s - \Gamma_{opt}\rvert^2$ = 0.5908 and $1 - \lvert\Gamma_s\rvert^2$ = 0.64, so $F = 1.202 + 4(0.16)(0.5908)/(0.64 \times 1.652)$ = 1.599, NF = **2.04** dB.
- (c) For 1.0 dB: $N = (1.259 - 1.202)(1.652)/0.64$ = 0.1463; centre $0.45/1.1463$ = **0.393**∠60°, radius $\sqrt{0.1463(1.1463 - 0.2025)}/1.1463$ = **0.324**. For 1.5 dB: centre **0.292**∠60°, radius **0.553**.

**Units check.** $r_n$, $N$ and reflection coefficients are dimensionless.

**Sanity check.** The origin is 0.393 from the 1.0 dB centre, just outside its 0.324 radius, so a 50 Ω source gives a little more than 1.0 dB, as (a) found. The power-match point costs 1.24 dB over the minimum: matching this device for gain would waste most of its low-noise advantage.

### Example 21-03.4 · Distortion of a bipolar transistor and a differential pair (tier B)

**Setup.** At 300 K ($V_T$ = 25.85 mV): (a) for a bipolar transistor driven at its base, find the input IIP3 amplitude and its power across 50 Ω; then the second and third harmonic ratios for a 5 mV tone, from the series and exactly, and the IM3 level for two 5 mV tones. (b) For an emitter-coupled pair, find the IIP3 amplitude, the 1 dB compression amplitude from the cubic model and exactly, and the IM3 level for two differential tones of 10 mV each.

**Solution.**

- (a) $A_{IIP3} = \sqrt{(4/3)(a_1/a_3)} = \sqrt{(4/3)\times 6}\,V_T = \sqrt8\,V_T$ = **73.12** mV, which across 50 Ω is $0.07312^2/100$ W = **−12.72** dBm. With $x = A/V_T$ = 0.1934, the series gives $\text{HD}_2 = x/4$ = 4.835% and $\text{HD}_3 = x^2/24$ = 0.1559%. Exactly, the harmonics of $e^{x\cos\theta}$ are modified Bessel functions, $\text{HD}_n = I_n(x)/I_1(x)$: **4.828**% and **0.1555**%. Two 5 mV tones give IM3 at $\tfrac34a_3A^3/(a_1A) = x^2/8$, or −46.60 dBc from the series and **−46.66** dBc exactly.
- (b) With $a_1 = I_{EE}/2V_T$ and $\lvert a_3\rvert = I_{EE}/24V_T^3$: $A_{IIP3} = \sqrt{(4/3)\times 12}\,V_T = 4V_T$ = **103.4** mV (**−9.71** dBm across 50 Ω). The cubic model's compression point is $\sqrt{0.1087 \times (4/3) \times 12}\,V_T$ = **34.10** mV; solving exactly for the amplitude at which the fundamental of $\tanh(u\cos\theta)$ is 1 dB below linear gives **36.85** mV. Two 10 mV tones give IM3 of **−40.87** dBc (the series estimate is −40.58).
- ngspice confirms the harmonic ratios and both IM3 levels to four figures (§5, `bjt_im.cir`).

**Units check.** $V_T$ in volts; $A^2/R$ in watts.

**Sanity check.** The pair's exact compression point lies **0.67** dB above the cubic estimate, because the fifth-order term of tanh opposes the cubic one; its IIP3 − P1dB is **8.96** dB, not 9.64. A pair's IIP3 amplitude is $\sqrt2$ ≈ **1.41** times the bare transistor's, and its even-order products cancel by symmetry: the netlist's IM2 residue is about $10^{-8}$ of the fundamental.

### Example 21-03.5 · A receiver line-up (tier B)

**Setup.** A receiver consists of a duplexer (2 dB loss, IIP3 +40 dBm), an LNA (gain 15 dB, NF 1.2 dB, IIP3 −8 dBm), a mixer (conversion gain 8 dB, NF 10 dB, IIP3 +5 dBm) and a baseband amplifier (gain 20 dB, NF 15 dB, IIP3 +15 dBm). Find the cascade noise figure and IIP3. Then raise the LNA gain to 20 dB, keeping its IIP3, and repeat.

**Solution.**

- Noise: $F = 1.585 + (1.318 - 1)/0.631 + (10 - 1)/(0.631 \times 31.62) + (31.62 - 1)/(0.631 \times 31.62 \times 6.31)$ = 2.785: NF = **4.45** dB.
- IIP3, in mW: $1/\text{IIP3} = 1/10^4 + 0.631/0.158 + 0.631 \times 31.62/3.16 + 0.631 \times 31.62 \times 6.31/31.6$ = 0.0001 + 3.98 + 6.31 + 3.98, so IIP3 = **−11.5** dBm. The mixer contributes the largest term.
- With 20 dB of LNA gain: NF = **3.63** dB, but IIP3 = **−15.6** dBm.

**Units check.** Gains and noise factors as ratios; intercepts in mW.

**Sanity check.** Five decibels more LNA gain bought **0.8** dB of noise figure and cost **4.1** dB of intercept. The duplexer's loss counts fully in the noise figure (it comes first) and not at all in the intercept (it is linear).

### Example 21-03.6 · Where 3GPP's sensitivity numbers come from (tier B)

**Setup.** 3GPP's study of 5G handset sensitivity writes $P_{sens} = -174 + 10\log_{10}B + \text{NF} + \text{SNR} + \text{IM} - \text{diversity gain}$ with SNR = −1 dB for the QPSK reference channel, an implementation margin of 2.5 dB and a two-receiver diversity gain of 3 dB [9]. The occupied bandwidth is $N_{RB} \times 12 \times$ the subcarrier spacing. Reconstruct the reference sensitivity of band n1 (15 kHz spacing) in a 5 MHz channel ($N_{RB}$ = 25) and a 10 MHz channel (52), assuming NF = 9 dB, and of band n78 (30 kHz) in a 100 MHz channel (273), with the agreed NF of 10 dB. Then find the spurious-free dynamic range of Example 21-03.5's receiver in a 4.5 MHz bandwidth.

**Solution.**

- n1, 5 MHz: $B$ = 4.5 MHz, $P_{sens} = -174 + 66.53 + 9 - 1 + 2.5 - 3$ = **−99.97** dBm; 10 MHz: $B$ = 9.36 MHz, **−96.79** dBm.
- n78, 100 MHz: $B$ = 98.28 MHz, $P_{sens} = -174 + 79.92 + 10 - 1.5$ = **−85.58** dBm.
- The published values are −100.0, −96.8 and −85.6 dBm [8, R-368], the computed values rounded down to one decimal place as the specification's note on rounding says.
- Example 21-03.5's receiver: $N = -173.98 + 66.53 + 4.45$ = **−103.0** dBm, and SFDR = $\tfrac23(-11.5 + 103.0)$ = **61.0** dB.

**Units check.** dBm/Hz + dB(Hz) = dBm.

**Sanity check.** The 9 dB for band n1 is inferred from the formula: we found no 3GPP text that states it directly, though the study states the 10 dB for n78 explicitly [9]. A handset with a 9 dB noise figure looks poor next to a 1 dB LNA, but the figure includes the duplexer, switches and the whole receiver at the antenna port, across temperature and band.

### Example 21-03.7 · A blocker, two ways (tier C)

**Setup.** A receiver whose LNA has IIP3 = −8 dBm must receive a weak signal in a 4.5 MHz channel while a −25 dBm blocker sits nearby. Its noise figure is 9 dB. (a) How much does the blocker compress the wanted signal's gain? (b) The LO has −140 dBc/Hz of phase noise at the blocker's offset. How large is the reciprocal-mixing noise, and how much does it desensitize the receiver? (c) What phase noise would limit the desensitization to 0.5 dB?

**Solution.**

- (a) $A_B^2/A_{IIP3}^2 = 10^{(-25 + 8)/10}$ = 0.01995; gain change $20\log_{10}(1 - 2 \times 0.01995)$ = **−0.354** dB.
- (b) $N_{rm} = -25 - 140 + 66.53$ = **−98.47** dBm. The thermal floor is $-173.98 + 66.53 + 9$ = **−98.44** dBm. They are equal, so the total noise doubles: desensitization **3.00** dB.
- (c) For 0.5 dB, $N_{rm}$ may be $10^{0.05} - 1$ = 0.122 of the thermal floor, −107.58 dBm, so $\mathcal{L} \le -107.58 + 25 - 66.53$ = **−149.1** dBc/Hz.

**Units check.** dBm + dBc/Hz + dB(Hz) = dBm.

**Sanity check.** Compression costs a third of a decibel; reciprocal mixing costs 3 dB. At this blocker level the oscillator, not the amplifier, limits the receiver, which is why blocking specifications drive synthesizer phase-noise targets.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 21-03.1a | gain | 18 | dB |
| Ex 21-03.1b | IIP3 | 0 | dBm |
| Ex 21-03.1c | OIP3 | 18 | dBm |
| Ex 21-03.1d | IIP2 | 18 | dBm |
| Ex 21-03.1e | IM3 at −40 dBm per tone | −80 | dBc |
| Ex 21-03.1f | output IM3 at −40 dBm per tone | −102 | dBm |
| Ex 21-03.1g | estimated input P1dB | −9.6 | dBm |
| Ex 21-03.2a | system noise figure | 1.70 | dB |
| Ex 21-03.2b | LNA noise figure | 1.54 | dB |
| Ex 21-03.2c | LNA noise temperature | 123 | K |
| Ex 21-03.2d | system noise figure, Tc 300 K | 1.59 | dB |
| Ex 21-03.2e | LNA noise figure, Tc 300 K | 1.43 | dB |
| Ex 21-03.3a | NF with a 50 ohm source | 1.07 | dB |
| Ex 21-03.3b | NF at the conjugate-match source | 2.04 | dB |
| Ex 21-03.3c | 1.0 dB circle centre magnitude | 0.393 | — |
| Ex 21-03.3d | 1.0 dB circle radius | 0.324 | — |
| Ex 21-03.3e | 1.5 dB circle centre magnitude | 0.292 | — |
| Ex 21-03.3f | 1.5 dB circle radius | 0.553 | — |
| Ex 21-03.4a | BJT IIP3 amplitude | 73.12 | mV |
| Ex 21-03.4b | BJT IIP3 across 50 ohm | −12.72 | dBm |
| Ex 21-03.4c | HD2 from the series | 4.835 | % |
| Ex 21-03.4d | HD3 from the series | 0.1559 | % |
| Ex 21-03.4e | HD2 exact | 4.828 | % |
| Ex 21-03.4f | HD3 exact | 0.1555 | % |
| Ex 21-03.4g | BJT IM3, two 5 mV tones, exact | −46.66 | dBc |
| Ex 21-03.4h | BJT IM3 from the series | −46.60 | dBc |
| Ex 21-03.4i | pair IIP3 amplitude | 103.4 | mV |
| Ex 21-03.4j | pair IIP3 across 50 ohm | −9.71 | dBm |
| Ex 21-03.4k | pair 1 dB amplitude, cubic model | 34.10 | mV |
| Ex 21-03.4l | pair 1 dB amplitude, exact | 36.85 | mV |
| Ex 21-03.4m | pair IIP3 − P1dB, exact | 8.96 | dB |
| Ex 21-03.4n | pair IM3, two 10 mV tones, exact | −40.87 | dBc |
| Ex 21-03.4o | pair IM3 from the series | −40.58 | dBc |
| Ex 21-03.5a | cascade NF | 4.45 | dB |
| Ex 21-03.5b | cascade IIP3 | −11.5 | dBm |
| Ex 21-03.5c | cascade NF, 20 dB LNA | 3.63 | dB |
| Ex 21-03.5d | cascade IIP3, 20 dB LNA | −15.6 | dBm |
| Ex 21-03.6a | n1 5 MHz sensitivity | −99.97 | dBm |
| Ex 21-03.6b | n1 10 MHz sensitivity | −96.79 | dBm |
| Ex 21-03.6c | n78 100 MHz sensitivity | −85.58 | dBm |
| Ex 21-03.6d | noise floor in 4.5 MHz | −103.0 | dBm |
| Ex 21-03.6e | SFDR | 61.0 | dB |
| Ex 21-03.7a | blocker gain compression | −0.354 | dB |
| Ex 21-03.7b | reciprocal-mixing noise | −98.47 | dBm |
| Ex 21-03.7c | thermal floor | −98.44 | dBm |
| Ex 21-03.7d | desensitization | 3.00 | dB |
| Ex 21-03.7e | phase noise for 0.5 dB | −149.1 | dBc/Hz |
| Txt 21-03.a | kT0 | −173.98 | dBm/Hz |
| Txt 21-03.b | 1 − 10^(−1/20) | 0.1087 | — |
| Txt 21-03.c | IIP3 − P1dB for a cubic | 9.64 | dB |
| Txt 21-03.d | NF penalty of a 50 ohm source, Ex 3 | 0.27 | dB |
| Txt 21-03.e | NF penalty of the power match, Ex 3 | 1.24 | dB |
| Txt 21-03.f | 4/3 times 0.1087 | 0.145 | — |
| Ex 21-03.1h | output tones at −40 dBm per tone | −22 | dBm |
| Ex 21-03.2f | analyzer contribution | 0.16 | dB |
| Ex 21-03.2g | effect of a 10 K cold-temperature error | 0.11 | dB |
| Ex 21-03.4p | pair exact P1dB above the cubic estimate | 0.67 | dB |
| Ex 21-03.4q | pair over single-transistor IIP3 amplitude | 1.41 | — |
| Ex 21-03.5e | NF gained with 5 dB more LNA gain | 0.8 | dB |
| Ex 21-03.5f | IIP3 lost with 5 dB more LNA gain | 4.1 | dB |
| Txt 21-03.g | concept check IIP3 | 5 | dBm |
| Txt 21-03.h | concept check IM3 at −30 dBm | −70 | dBc |

## 5. Simulate it

The lab ([labs/21-03-lab](../labs/21-03-lab/README.md)) collects the chapter's formulas in `rfnl.py`, simulates nonlinearities with FFTs and noise measurements with random numbers, and confirms the transistor distortion of Example 21-03.4 in ngspice (`bjt_im.cir`).

**Predict, then run.**

1. Predict the noise figure of Example 21-03.3's device over the whole source plane, then map it and overlay the noise circles (Part 1).
2. Predict how far a Y-factor measurement scatters when each noise power is averaged over a finite number of samples, then simulate many measurements (Part 2).
3. Predict the IM3 slope and the intercept of a cubic amplifier, run a two-tone sweep through it with an FFT, and see where the slope bends away from 3 (Part 3).
4. Predict the harmonic and intermodulation levels of a bipolar transistor and a differential pair, compute them exactly, and run `ngspice -b bjt_im.cir` (Part 4).
5. Predict which stage dominates a line-up's noise figure and which its IIP3, then sweep the LNA gain and plot both (Part 5).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| LNA gain | Cascade noise figure | Cascade IIP3, blocker tolerance | RF system architect |
| Source impedance at $\Gamma_{opt}$ (noise match) | Noise figure | Input return loss, gain | LNA designer |
| Bias current in the front end | Linearity (IIP3, P1dB), and often noise | Power, battery life | RF designer and product owner |
| Filter before the LNA | Blocker rejection, IIP3 margin | Noise figure (its loss adds directly) | Front-end architect |
| Differential versus single-ended circuits | IIP2 (even orders cancel), common-mode rejection | Twice the devices, baluns, area | RF designer |
| LO phase noise | Reciprocal-mixing desensitization | Oscillator power and area (21-06) | Synthesizer designer |
| Gain switching (steps) | Dynamic range across signal levels | Control complexity, gain-step transients | Radio software and RF designer |

## 7. Numbers to know

| Quantity | Typical value | Note |
|---|---|---|
| $kT_0$ | −173.98 dBm/Hz (−174) | 290 K reference [5, 10] |
| IIP3 − P1dB | 9.64 dB for a pure cubic; 8.96 dB for a differential pair; 8 to 13 dB in four LNA and front-end data sheets | Model result, not a rule (§9) [R-369] |
| IM3 slope | 3 dB per dB; IM3 level $-2(\text{IIP3} - P_{in})$ dBc | Small-signal region only |
| SFDR | $\tfrac23(\text{IIP3} - N)$ | 3 dB of IIP3 buys 2 dB |
| Bipolar transistor IIP3 | $\sqrt8\,V_T$ = 73 mV peak (−12.7 dBm across 50 Ω) | Degeneration raises it |
| Differential-pair IIP3 | $4V_T$ = 103 mV peak (differential) | Even orders cancel |
| Discrete LNA noise figure | 0.6 dB typical (1.1 dB max) at 2.6 GHz; 1.6 dB typical at 5.5 GHz | Infineon data sheets, 2021 and 2023 [R-369] |
| Wi-Fi 7 front-end receive path | NF 1.8 dB typical, IIP3 +8 dBm, IP1dB −5 dBm | Qorvo QPF4609, Sep 2024 [R-369] |
| 77 GHz single-chip radar receiver | NF 12 to 15 dB | TI AWR2944 and AWR1843 data sheets [R-369] |
| 5G handset NF assumed by 3GPP | about 9 dB (legacy bands, inferred), 10 to 10.5 dB (n77–n79, stated) | TR 38.817-01 [9, R-368] |
| 5G reference sensitivity, two receivers | −100.0 dBm (n1, 5 MHz); −85.6 dBm (n78, 100 MHz) | TS 38.101-1 V19.7.0, Sep 2026 [8, R-368] |
| 5G wide-band intermodulation test | two interferers of −46 dBm each (one CW, one modulated), wanted 6 to 9 dB above REFSENS | TS 38.101-1 §7.8.2 [8, R-368] |
| Y-factor limit | not used when NF exceeds the source's ENR by more than about 10 dB | Agilent AN 57-1 [5] |

## 8. Common mistakes

- **Quoting noise figure without the source impedance.** A noise figure is meaningful only with the $\Gamma_s$ it was measured at; $F_{min}$ is reached only at $\Gamma_{opt}$.
- **Matching an LNA for maximum gain and expecting minimum noise.** The two optima differ (Example 21-03.3).
- **Extrapolating IIP3 from a measurement near compression.** Check the IM3 slope first; outside the small-signal region the formula $P_{in} + \Delta/2$ is wrong.
- **Mixing input- and output-referred intercepts.** OIP3 = IIP3 + gain; a cascade formula needs all stages referred to the same point.
- **Adding gain to fix noise without checking linearity.** Gain divides later noise and multiplies later distortion (Example 21-03.5).
- **Ignoring the oscillator in a blocking test.** Reciprocal mixing can desensitize a receiver far more than compression (Example 21-03.7).
- **Reading ENR as "noise above kTB".** An ENR of 0 dB means a 290 K difference between hot and cold, i.e. a hot temperature of 580 K [5].
- **Forgetting the analyzer's noise.** A Y-factor measurement gives the cascade; subtract the second stage with Friis.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **The definitions are from the 1940s to 1960s [Established].** Friis defined the noise figure of a two-port in 1944 as the ratio of input to output signal-to-noise ratios [10]; Rothe and Dahlke (1956) reduced a noisy two-port to a noiseless one with a preceding noise network characterized by an equivalent noise conductance, resistance and "complex correlation admittance" [3]; and the IRE noise subcommittee (1960) showed that the noise factor "is a function of four parameters which are independent of the circuit external to the twoport" [4]. The IRE adopted 290 K as the reference temperature, which makes $kT_0$ "the even number 4.00 x 10-21 watts per hertz" [5].
- **Measurement is a ratio [Established].** The Y-factor method remains the standard bench method; Agilent's application note gives the cold-temperature correction and warns that ENR "is not the 'on' noise relative to kTB as is often erroneously believed" [5]. Vector network analyzers now include noise receivers and noise tuners for measuring noise parameters (21-01 §9).
- **Discrete LNAs reach well under 1 dB [Established].** Infineon's BGA9H1BN6 (SiGe, 2.3–2.7 GHz, December 2023) specifies 0.6 dB typical and 1.1 dB maximum at 2.6 GHz with 20.3 dB of gain and an IIP3 of −7 dBm typical at 5.5 mA [R-369]. For scale, Shaeffer and Lee's landmark 1997 CMOS LNA reached 3.5 dB at 1.5 GHz with 22 dB of gain while drawing 30 mW [11].
- **Integrated front ends trade noise for integration [Established].** Qorvo's QPF4609 Wi-Fi 7 front end specifies a receive noise figure of 1.8 dB typical (2.2 dB maximum), IIP3 of +8 dBm and input P1dB of −5 dBm [R-369]. Texas Instruments' single-chip 77 GHz radars specify 12 dB (AWR2944) and 14 to 15 dB (AWR1843) noise figure, with an in-band IIP2 of 16 dBm on the latter, because their FMCW receivers convert to an IF near DC [R-369].
- **Standards encode the floor and the ceiling [Established].** 3GPP's 5G handset specification (TS 38.101-1 V19.7.0, Release 19, September 2026) defines reference sensitivity as the power at which throughput reaches at least 95% of the reference channel's maximum, measured in FDD bands with the handset's own transmitter at full power; it adds adjacent-channel selectivity, in-band and out-of-band blocking (out-of-band CW blockers up to −15 dBm), narrow-band blocking and a wide-band intermodulation test with two −46 dBm interferers [8, R-368]. The study behind the sensitivity table writes it as $-174 + 10\log B + \text{NF} + \text{SNR} + \text{IM} - \text{diversity gain}$ and agrees noise figures of 10.5, 10 and 10 dB for bands n77 to n79 [9].
- **Second-order linearity is the zero-IF tax [Established].** Razavi's and Abidi's analyses of direct-conversion receivers identified DC offsets, even-order distortion, flicker noise and LO leakage as the architecture's problems [6, 7]; in FDD handsets the transmitter's own leakage through the duplexer is a strong second-order aggressor, and 3GPP tests reference sensitivity with that transmitter at full power [8] (Problem 21-03.13).

### Why it matters commercially

- **Sensitivity is range and battery life.** Every decibel of noise figure is a decibel of link budget (21-11): more range, fewer retransmissions, or lower transmit power at the other end.
- **Linearity is coexistence.** Phones carry cellular, Wi-Fi, Bluetooth, UWB and GNSS radios side by side; the blocking and intermodulation tests of the standards, and the operators' own coexistence tests, decide whether a radio ships.
- **Front-end modules are sold on these numbers.** Noise figure, IIP3 and P1dB are the first rows of every LNA and front-end module data sheet, and small differences decide sockets.

### Marketing vs Reality

- **"0.6 dB noise figure."** It is typical, at one frequency, at 25 °C, with a 50 Ω source and the vendor's matching network, often with the board's losses subtracted. The same Infineon part's maximum is 1.1 dB; another of its LNAs specifies 1.6 dB typical and 2.5 dB maximum, and its footnotes read "PCB losses are subtracted" and "Verification based on AQL; not 100% tested in production" [R-369]. Qorvo's front-end data sheet states that its "Specifications are not guaranteed over all recommended operating conditions" [R-369]. Ask for the maximum over temperature and band edges.
- **"IIP3 of +8 dBm."** It comes from one two-tone test, typically 1 MHz spacing at one tone power. It says nothing about wider spacings (bias-network memory), other power levels (where the slope departs from 3) or modulated blockers. Across four LNA and front-end data sheets, IIP3 − IP1dB ranges from 8 to 13 dB, not the textbook 9.64 [R-369].
- **"Psat +32 dBm."** On the transmit side of the same Wi-Fi front end, saturated power is +32 dBm and output P1dB +30 dBm typical, but the power at which it meets the Wi-Fi 7 MCS13 error-vector requirement is +15.5 dBm, and only with digital predistortion, with the error measured relative to the test source's own floor [R-369]. Usable linear power can be 16 dB below the headline.
- **"−96.5 dBm sensitivity."** TI's CC2340R5 Bluetooth LE chip quotes −96.5 dBm at 1 Mb/s against the specification's −70 dBm reference (a figure we could confirm only from secondary sources), measured conducted on TI's reference design at one channel and 25 °C [R-370]. Competitors' figures are comparable only if packet length, bit- or packet-error criterion, channel and conducted versus radiated measurement all match.
- **Units betray carelessness.** One radar data sheet's feature list gives a receiver noise figure as "12dBm"; its specification table correctly says 12 dB [R-369]. Small, but a prompt to read the tables, not the bullets.

### Questions for engineering leaders

1. **"What are your noise figure and IIP3 maximums over temperature and band edges, not typicals at mid-band and 25 °C?"** *Strong:* gives distributions from production or characterization lots and the guard band to the specification. *Evasive:* quotes the data-sheet typical.
2. **"What tone spacing and power did you use for IIP3, and does it hold for a modulated blocker at the standard's offsets?"** *Strong:* cites the 3GPP wide-band intermodulation test (−46 dBm CW plus −46 dBm modulated) and shows the measured margin. *Evasive:* "IIP3 is IIP3."
3. **"Which stage sets your cascade noise figure, and which sets your IIP3? What happens when you switch LNA gain?"** *Strong:* shows the Friis and intercept contributions per stage and the gain-switching thresholds. *Evasive:* "The LNA dominates everything."
4. **"In your FDD bands, what duplexer isolation and IIP2 do you assume for reference sensitivity with the transmitter at full power?"** *Strong:* gives the leakage level, the IIP2 target with calibration, and the measured desensitization. *Evasive:* "We meet REFSENS."
5. **"How much of your blocking margin is set by LO phase noise?"** *Strong:* computes reciprocal mixing at each blocking offset and shows the synthesizer's phase-noise mask meets it. *Evasive:* "Our LNA is very linear."

## 10. Concept check

**Q1.** Why does a two-port's noise figure depend on the impedance of the source driving it?

<details><summary>Answer</summary>

Its noise is equivalent to a voltage source $e_n$ and a current source $i_n$ at the input. The voltage source's contribution is converted to current by the source admittance ($Y_se_n$), and the current source's is not, so the total noise relative to the source's own noise changes with $Y_s$. The balance point, where the two contributions and their correlation trade off best, is $Y_{opt}$.

</details>

**Q2.** A data sheet gives $F_{min}$ = 0.5 dB and $R_n$ = 4 Ω for one transistor, and $F_{min}$ = 0.4 dB and $R_n$ = 40 Ω for another. Which would you prefer for a broadband LNA?

<details><summary>Answer</summary>

Probably the first. $R_n$ sets how fast the noise figure rises as the source moves away from $\Gamma_{opt}$; over a wide band the source cannot stay at $\Gamma_{opt}$, and the low-$R_n$ device degrades ten times more slowly.

</details>

**Q3.** Why is ENR not the ratio of the hot noise power to $kTB$?

<details><summary>Answer</summary>

ENR is defined as the difference between hot and cold temperatures, divided by 290 K. The hot noise power relative to $kT_0B$ is ENR + 1 (in linear terms), so a 0 dB ENR source is at 580 K, twice $kT_0B$, not equal to it.

</details>

**Q4.** Two tones at −20 dBm each produce IM3 at −50 dBc. What is IIP3, and what would IM3 be at −30 dBm per tone?

<details><summary>Answer</summary>

$\text{IIP3} = -20 + 50/2$ = **+5** dBm. At −30 dBm, IM3 is $-2(5 + 30)$ = **−70** dBc: 10 dB less input gives 20 dB lower IM3 relative to the tones (30 dB lower in absolute terms).

</details>

**Q5.** Why does adding LNA gain improve noise figure but degrade IIP3?

<details><summary>Answer</summary>

Later stages' noise is referred to the input by dividing by the gain in front of them, so more gain shrinks it. Later stages' distortion grows with the signal they see, which the gain increases, so more gain makes their input-referred intercepts worse.

</details>

**Q6.** Why does a zero-IF receiver need a high IIP2 while a superheterodyne usually does not?

<details><summary>Answer</summary>

Second-order products of two strong signals, and the demodulated envelope of one AM blocker, fall near DC. A superheterodyne's wanted signal is at an intermediate frequency, so a filter removes them; a zero-IF receiver's wanted signal is itself at DC, so they land on top of it.

</details>

**Q7.** A blocker 3 MHz away desensitizes a receiver by 3 dB, but its LNA is far from compression. What is the likely cause?

<details><summary>Answer</summary>

Reciprocal mixing: the LO's phase noise at 3 MHz offset, multiplied by the blocker's power, adds noise in the channel equal to the thermal floor (Example 21-03.7).

</details>

Problems: [21-03 problem set](../problems/21-03-problems.md) · Worked solutions: [21-03 solutions](../solutions/21-03-solutions.md)

## 11. Key terms

[Noise figure](../../../reference/glossary.md#noise-figure) · [Noise temperature](../../../reference/glossary.md#noise-temperature) · [Friis noise formula](../../../reference/glossary.md#friis-noise-formula) · [Noise parameters](../../../reference/glossary.md#noise-parameters) · [Noise circle](../../../reference/glossary.md#noise-circle) · [Y-factor method](../../../reference/glossary.md#y-factor-method) · [Excess noise ratio (ENR)](../../../reference/glossary.md#excess-noise-ratio-enr) · [P1dB (1 dB compression point)](../../../reference/glossary.md#p1db-1-db-compression-point) · [Third-order intercept point (IP3)](../../../reference/glossary.md#third-order-intercept-point-ip3) · [Second-order intercept point (IP2)](../../../reference/glossary.md#second-order-intercept-point-ip2) · [Intermodulation distortion](../../../reference/glossary.md#intermodulation-distortion) · [Desensitization](../../../reference/glossary.md#desensitization) · [Reciprocal mixing](../../../reference/glossary.md#reciprocal-mixing) · [Spurious-free dynamic range (SFDR)](../../../reference/glossary.md#spurious-free-dynamic-range-sfdr) · [Reference sensitivity (REFSENS)](../../../reference/glossary.md#reference-sensitivity-refsens)

## 12. Connections

- **Builds on:** [17-02](../../17-communication-systems/chapters/17-02-noise-and-snr.md) (noise temperature, Friis, sensitivity), [12-10](../../12-electronics-2/chapters/12-10-noise-in-circuits.md) ($e_n$, $i_n$, optimum source), [12-01](../../12-electronics-2/chapters/12-01-differential-pairs.md) (the tanh characteristic), [21-01](21-01-s-parameters.md) and [21-02](21-02-impedance-matching-networks.md) (reflection and matching).
- **Next:** [21-04](21-04-low-noise-amplifiers.md) designs LNAs that reach $F_{min}$ and a power match at once.
- **Used later:** mixer noise and linearity in [21-05](21-05-mixers.md), phase noise in [21-06](21-06-oscillators-and-vcos.md), PA linearity in [21-07](21-07-power-amplifiers.md), architecture choices in [21-08](21-08-transceiver-architectures.md), link budgets in [21-11](21-11-link-budgets.md).

## 13. Further study

- B. Razavi, *RF Microelectronics*, 2nd ed., Prentice Hall, 2012: the chapter on basic concepts (nonlinearity, noise, sensitivity and dynamic range).
- D. M. Pozar, *Microwave Engineering*, 4th ed., Wiley, 2012: the chapter on noise and nonlinear distortion, and the amplifier-design chapter for noise circles.
- Agilent Application Note 57-1, *Fundamentals of RF and Microwave Noise Figure Measurements* [5]: the Y-factor method and its corrections, clearly explained.

## 14. Sources

1. B. Razavi, *RF Microelectronics*, 2nd ed., Prentice Hall, 2012, ISBN 978-0-13-713473-1.
2. D. M. Pozar, *Microwave Engineering*, 4th ed., Wiley, 2012.
3. H. Rothe and W. Dahlke, "Theory of Noisy Fourpoles," *Proc. IRE*, vol. 44, no. 6, pp. 811–818, Jun. 1956, DOI 10.1109/JRPROC.1956.274998 [R-367].
4. H. A. Haus et al. (IRE Subcommittee 7.9 on Noise), "Representation of Noise in Linear Twoports," *Proc. IRE*, vol. 48, no. 1, pp. 69–74, Jan. 1960, DOI 10.1109/JRPROC.1960.287381 [R-367].
5. Agilent Technologies, Application Note 57-1, *Fundamentals of RF and Microwave Noise Figure Measurements*, 5952-8255E, Oct. 2000 [R-367].
6. B. Razavi, "Design considerations for direct-conversion receivers," *IEEE Trans. Circuits Syst. II*, vol. 44, no. 6, pp. 428–435, Jun. 1997, DOI 10.1109/82.592569 [R-367].
7. A. A. Abidi, "Direct-conversion radio transceivers for digital communications," *IEEE J. Solid-State Circuits*, vol. 30, no. 12, pp. 1399–1410, Dec. 1995, DOI 10.1109/4.482187 [R-367].
8. 3GPP TS 38.101-1 V19.7.0 (2026-09), *NR; User Equipment (UE) radio transmission and reception; Part 1: Range 1 Standalone*, §7 [R-368].
9. 3GPP TR 38.817-01 V16.4.0 (2022-09), §6.2 (UE reference-sensitivity derivation) [R-368].
10. H. T. Friis, "Noise Figures of Radio Receivers," *Proc. IRE*, vol. 32, no. 7, pp. 419–422, Jul. 1944, DOI 10.1109/JRPROC.1944.232049 [R-367].
11. D. K. Shaeffer and T. H. Lee, "A 1.5-V, 1.5-GHz CMOS low noise amplifier," *IEEE J. Solid-State Circuits*, vol. 32, no. 5, pp. 745–759, May 1997, DOI 10.1109/4.568846 [R-367].
12. Data sheets: Infineon BGA9H1BN6 (Rev. 2.1, Dec 2023) and BGA8U1BN6 (Rev. 3.2, Apr 2021); Qorvo QPF4609 (Rev. C, Sep 2024, preliminary); Texas Instruments AWR1843 (SWRS222D, rev. Sep 2024) and AWR2944 (SWRS273E, rev. Feb 2026) [R-369]; Texas Instruments CC2340R5 (SWRS272F, rev. May 2026) [R-370].
