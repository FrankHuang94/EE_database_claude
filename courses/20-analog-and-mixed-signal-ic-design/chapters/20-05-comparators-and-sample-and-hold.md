<!-- status: verified -->
# 20-05 · Comparators and Sample-and-Hold Circuits

| | |
|---|---|
| **Course** | [20 · Analog and Mixed-Signal IC Design](../README.md) |
| **University equivalent** | The sampling and comparator material of a graduate data-converter or analog IC course: sampling switches, kT/C noise, charge injection, bootstrapping, aperture jitter, latched comparators and the StrongARM latch, offset, noise, kickback and metastability (Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed., the switched-capacitor and comparator chapters; Pelgrom, *Analog-to-Digital Conversion*, 4th ed., the sample-and-hold and comparator chapters) |
| **Prerequisites** | [20-01](20-01-analog-design-fundamentals-gm-id.md) (charge-based model, $g_m/I_D$), [12-10](../../12-electronics-2/chapters/12-10-noise-in-circuits.md) (thermal noise), [08-10](../../08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md) (metastability), [10-08](../../10-electronics-1/chapters/10-08-current-sources-and-mirrors.md) (Pelgrom mismatch), [11-10](../../11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md) (sampling) |
| **Estimated study hours** | 8 |
| **Last verified** | 2026-11-24 |

**Learning objectives.** After this chapter you can:

1. Derive kT/C noise and size a sampling capacitor for a resolution target.
2. Size a sampling switch for settling and explain why bootstrapping is needed at low supply, including its residual distortion.
3. Estimate charge injection and clock feedthrough, and explain bottom-plate sampling.
4. Derive the jitter-limited SNR and combine quantization, kT/C and jitter noise into one budget.
5. Analyze a StrongARM comparator's integration gain, input-referred noise, energy, offset and kickback.
6. Derive regeneration time and metastability error rates, and budget decision time in a SAR ADC.

## 1. Big picture

Every analog-to-digital converter does two things: it **freezes** a continuously varying input at an instant (sampling), and it **decides** whether one voltage is above another (comparison). The circuits that do this are the sample-and-hold, usually a switch and a capacitor, and the latched comparator, usually a few transistors in positive feedback. They are the smallest blocks in a converter and set many of its limits. Their noise, timing accuracy, linearity and error rate are the first numbers to check in any ADC claim. This chapter designs both for a running example: the front end of a 12-bit, 100 MS/s differential SAR ADC in the illustrative T130 process with $V_{DD}$ = 1.2 V.

- **kT/C sets the capacitor, and the capacitor sets the power.** Thermal noise sampled on a capacitor has a variance of $kT/C$ whatever the switch's resistance. Each extra bit of resolution needs four times the capacitance, and with it four times the drive power.
- **Timing is a voltage error.** A sampling instant uncertain by 100 fs limits a 1 GHz input to 64 dB of SNR. High-speed ADCs are often limited by their clock, not their circuits.
- **Low supply breaks the simple switch.** At 1.2 V an NMOS switch with its gate at $V_{DD}$ cannot pass a mid-scale input. Bootstrapping, which lifts the gate with the input, is now standard in sampling front ends.
- **Comparators trade energy, noise and speed.** The StrongARM latch draws no static current, but its noise falls only as the square root of its energy, and a small input takes longer to resolve.

## 2. Intuition first

```text
   track:  S closed            hold:  S open
   v_in ──/ ──┬── v_s          v_in ──/  ┬── v_s (frozen)
              │                          │
             C_s                        C_s
              │                          │
             GND                        GND

   comparator: preamp/integrator → latch (positive feedback)
   v+ ─┐                    ┌──────────────┐
       ├─ gain A_int ──────►│ cross-coupled │──► 1 or 0
   v− ─┘  (a few ×)         │   inverters   │
                            └──────────────┘
```

*Figure 1. A sample-and-hold is a switch and a capacitor: closed, the capacitor tracks the input; opened, it holds the last value. A latched comparator amplifies the input difference a little, then lets positive feedback blow it up to a logic level.*

**A camera analogy, and its limits.** A sample-and-hold is a camera. The switch is the shutter, and the capacitor is the film. Three things blur the picture. *Thermal noise* is like grain: the film's own randomness, fixed by its size (capacitance), not by the lens. *Finite bandwidth* is like a slow shutter: the image of a moving subject is smeared because the capacitor cannot follow the input instantly. *Jitter* is like not knowing exactly when the shutter fired: a fast-moving subject is in the wrong place by its speed times the timing error. The analogy breaks at the shutter itself: a real switch, when it opens, dumps part of its own channel charge onto the capacitor, as if the shutter left a fingerprint whose size depends on the scene.

**A comparator is compounding.** A latch is two inverters connected in a loop. A small imbalance makes one side pull down slightly harder, which makes the other side pull up harder, which pulls the first side down harder still. The difference grows by a fixed *percentage* per unit time, like compound interest: $v(t) = v_0e^{t/\tau}$. A large initial difference reaches a logic level quickly. A tiny one takes a long time, and an exactly zero difference never resolves. That last case is **metastability**, which 08-10 met in flip-flops; it is the same physics, and the same exponential.

## 3. Theory

> **Conventions.** T130 NMOS (20-01): μ = 350 cm²/V·s, $C_{ox}$ = 8.6 fF/µm², $V_{TH0}$ = 0.45 V, minimum length 0.13 µm; for the switch, an illustrative body-effect coefficient $\gamma_b$ = 0.4 V$^{1/2}$ with $2\phi_F$ = 0.8 V (10-02 §3.1) and a gate-overlap capacitance of 0.3 fF per micrometer of width. $kT$ = 4.1419 × 10⁻²¹ J (300 K). The running design: differential inputs swing from 0.2 to 1.0 V around a 0.6 V common mode, so the differential full scale $V_{FS}$ is 1.6 V peak to peak and one LSB is $\Delta = V_{FS}/2^{12}$.

### 3.1 What a sample-and-hold must do

In **track** mode the switch is closed and the capacitor follows the input through the switch's resistance. In **hold** mode the switch is open and the capacitor keeps the voltage it had when the switch opened. The held value then feeds the converter: a capacitive DAC and comparator in a SAR ADC, a residue amplifier in a pipeline. Four budgets decide its quality:

1. **Noise.** The thermal noise frozen on the capacitor (§3.2).
2. **Settling.** The capacitor must get within a fraction of an LSB of the input during the track time (§3.3).
3. **Linearity.** The switch's resistance and charge depend on the input, which distorts the sample (§3.3–§3.5).
4. **Timing.** Uncertainty in the sampling instant becomes voltage error on a moving input (§3.6).

### 3.2 kT/C noise

A resistor $R$ has thermal noise with one-sided power spectral density $4kTR$ (V²/Hz; 12-10). In track mode it drives the capacitor through the low-pass $1/(1 + j\omega RC)$, so the noise on the capacitor has variance

$$
\overline{v_n^2} = \int_0^\infty \frac{4kTR}{1 + (2\pi fRC)^2}\,df .
$$

> **Math refresher — a standard integral.** $\int_0^\infty dx/(1 + x^2) = \arctan x\,\big|_0^\infty = \pi/2$. With the substitution $x = 2\pi fRC$, $df = dx/(2\pi RC)$.

Substituting,

$$
\overline{v_n^2} = \frac{4kTR}{2\pi RC}\cdot\frac{\pi}{2} = \frac{kT}{C} .
$$

The resistance cancels. A larger resistor has more noise per hertz but a proportionally narrower bandwidth. When the switch opens, the capacitor keeps whatever noise voltage it had at that instant, a random sample with variance $kT/C$. Thermodynamics gives the same answer without any circuit: by equipartition, a capacitor in thermal equilibrium stores an average energy $\tfrac12C\overline{v^2} = \tfrac12kT$. For 1 pF at 300 K, $\sqrt{kT/C}$ = 64.4 µV.

**Sizing the capacitor.** A differential sampler has a capacitor $C$ on each side; the two noises are independent, so the differential noise variance is $2kT/C$. An ideal $N$-bit quantizer adds noise of variance $\Delta^2/12$. A full-scale sine of differential amplitude $A = V_{FS}/2$ has power $A^2/2$, so

$$
\text{SNR} = \frac{A^2/2}{\Delta^2/12 + 2kT/C} .
$$

A common design choice is to make the kT/C noise equal to the quantization noise, $C = 24kT/\Delta^2$, which costs 3 dB of SNR (half a bit). The capacitance grows as $4^N$: each extra bit costs four times the capacitance, and since the driver must charge it in the same time, roughly four times the drive power. This is the most important scaling law in data converters (20-12).

### 3.3 The sampling switch

A MOSFET switch operates in triode with a small voltage across it. With terminals at $v_a$ and $v_b$, the long-channel triode current can be written symmetrically as

$$
I = K\left(V_G - V_{TH} - v_m\right)(v_a - v_b), \qquad v_m = \frac{v_a + v_b}{2}, \quad K = \mu C_{ox}\frac{W}{L} ,
$$

which is the long-channel triode law $K[(V_{GS} - V_{TH})V_{DS} - V_{DS}^2/2]$ (10-02) rewritten about the channel's mean voltage. The threshold is evaluated at that mean voltage, $V_{TH}(v_m)$, because the body effect raises it as the channel moves up (the lab and the ngspice netlist do the same). For a small difference the switch is a resistor

$$
R_{on} = \frac{1}{K\left(V_G - v_{in} - V_{TH}(v_{in})\right)}, \qquad V_{TH}(v) = V_{TH0} + \gamma_b\left(\sqrt{2\phi_F + v} - \sqrt{2\phi_F}\right),
$$

with the body at ground. Two problems follow for a plain NMOS switch with $V_G = V_{DD}$:

- **Headroom.** The overdrive $V_{DD} - v_{in} - V_{TH}$ shrinks as the input rises, and the body effect makes $V_{TH}$ rise too. In T130 at 1.2 V the switch is off above about 0.63 V: it cannot pass the upper half of the running design's input range at all (Example 20-05.2).
- **Distortion.** Even where it conducts, $R_{on}$ depends on the input, so the tracking error depends on the input (§3.4).

**Settling.** In track mode the capacitor follows a step with time constant $\tau = R_{on}C$. To settle within half an LSB of an $N$-bit full-scale step in the track time $T_{tr}$:

$$
e^{-T_{tr}/\tau} \le 2^{-(N+1)} \quad\Longrightarrow\quad \tau \le \frac{T_{tr}}{(N + 1)\ln 2} .
$$

For 12 bits, $\ln 2^{13}$ = 9.01 time constants. The same $\tau$ sets the track-mode bandwidth $1/(2\pi R_{on}C)$.

### 3.4 Bootstrapped switches

A **bootstrapped switch** holds the gate a fixed voltage above the input. The idea of a constant gate–source voltage is old; the version with a precharged capacitor as the "battery" became standard around 1999 in low-voltage converters (Abo and Gray; Dessouky and Kaiser), and Razavi's history of the circuit, which traces the precharged capacitor to Brandt, Ferguson and Rebeschini (1997), culminates in Dessouky and Kaiser's 2001 topology, which keeps every device within its voltage rating [3]. During hold, a capacitor $C_b$ is charged to $V_{DD}$. During track, it is connected between the input and the gate, so $V_G = v_{in} + V_{DD}$ and $V_{GS} = V_{DD}$ regardless of the input. The overdrive becomes $V_{DD} - V_{TH}(v_{in})$: the switch now conducts over the whole range, and its resistance varies only through the body effect. Two imperfections remain:

- **Charge sharing.** The gate's parasitic capacitance $C_p$ shares the bootstrap charge, so $V_{GS} = V_{DD}C_b/(C_b + C_p)$; $C_b$ is made several times $C_p$.
- **Body effect.** With the body at ground, $V_{TH}$ still rises with the input. A switch in its own well (a triple-well NMOS) with the body tied to the source removes this term.

![On-resistance against input voltage on a log scale for four switches sized for the running design: the plain NMOS rises steeply and turns off near 0.63 volts; a transmission gate peaks near 7.6 kilohms in mid-range; the bootstrapped switch with grounded body rises gently from about 690 to 850 ohms; with the body tied to the source it is flat near 650 ohms](../../../assets/figures/20-05/ron.svg)

*Figure 3. On-resistance of the running design's switch (W = 0.888 µm) against the input. At 1.2 V neither a plain NMOS nor a transmission gate can cover the 0.2–1.0 V range; bootstrapping holds $R_{on}$ near the 852 Ω settling target, and tying the body to the source makes it flat.*

**Tracking distortion.** In track mode the error is $v_{in} - v_{out} \approx R_{on}(v)\,C\,dv_{in}/dt$. Expand $R_{on}(v) = R_0(1 + \alpha\delta + \beta\delta^2)$ about the common mode, with $\delta = v - V_{CM}$. For $\delta = A\sin\omega t$, the product $\alpha A\sin\omega t \cdot A\omega\cos\omega t$ contains $\tfrac12\alpha A^2\omega\sin 2\omega t$, so the second harmonic relative to the fundamental is

$$
\text{HD}_2 \approx \frac{\omega R_0C\,\alpha A}{2} ,
$$

and the $\beta$ term gives a first-order third harmonic $\omega R_0C\,\beta A^2/4$. Distortion therefore grows in proportion to the input frequency. A differential sampler cancels the even harmonics, leaving the third. Near Nyquist a second-order term, in which the second-harmonic error mixes with the fundamental, grows as $\omega^2$ and dominates the third harmonic; the simulation in Example 20-05.4 shows how much.

### 3.5 Charge injection and clock feedthrough

When the switch turns off, its channel charge $Q_{ch} = WLC_{ox}(V_{GS} - V_{TH})$ must go somewhere. Roughly half flows to each side; the half that lands on $C$ shifts the held voltage by

$$
\Delta V_{inj} \approx \frac{Q_{ch}}{2C} .
$$

The split depends on the impedances on each side and on how fast the gate falls, so "half" is a first-order estimate. Because $V_{TH}$ depends on the input, $Q_{ch}$ does too, and the error is partly signal dependent. The gate's overlap capacitance $C_{ov}$ also couples the falling gate edge onto $C$: **clock feedthrough** $\Delta V_{ft} = \Delta V_G\,C_{ov}/(C_{ov} + C)$. With a bootstrapped gate, $\Delta V_G = v_{in} + V_{DD}$ is signal dependent as well.

Three remedies are standard:

- **Differential sampling.** The common part of both errors cancels between the two sides.
- **Bottom-plate sampling.** A second switch at the capacitor's other (bottom) plate, at a fixed potential, opens first. Once it is open, the capacitor's charge can no longer change, so the top-plate switch's later charge injection cannot alter the sample; the bottom switch's own charge is signal independent because its terminals sit at a fixed voltage.
- **Small switches.** $Q_{ch}$ is proportional to $W$, and so is the conductance, so a narrower switch injects less charge but settles more slowly. The product is fixed: with $\Delta V_{inj} = WLC_{ox}V_{ov}/(2C)$ and $\tau = R_{on}C = LC/(\mu C_{ox}WV_{ov})$, $\Delta V_{inj}\,\tau = L^2/(2\mu)$, independent of $W$, $C$, $C_{ox}$ and the overdrive (Problem 20-05.6). At a given channel length, speed and charge injection trade one for one; only a shorter channel or a higher mobility improves both.

### 3.6 Aperture jitter

If the sampling instant is off by $\delta t$, a moving input is sampled with error $\delta v \approx (dv/dt)\,\delta t$. For $v = A\sin\omega t$ and a random timing error of standard deviation $\sigma_t$, independent of the signal, the mean-square error is

$$
\overline{\delta v^2} = \overline{(A\omega\cos\omega t)^2}\,\sigma_t^2 = \frac{A^2\omega^2\sigma_t^2}{2} ,
$$

and since the signal power is $A^2/2$,

$$
\text{SNR}_{jitter} = \frac{1}{(\omega\sigma_t)^2} = -20\log_{10}(2\pi f_{in}\sigma_t)\ \text{dB} ,
$$

the form in which converter vendors state it [7]. The amplitude cancels. The result depends only on the input frequency and the jitter: every decade of frequency costs 20 dB. The jitter is the root-sum-square of the clock source's jitter, the clock buffers' added jitter and the switch's own aperture uncertainty. All the noise powers add:

$$
\text{SNR} = \frac{A^2/2}{\Delta^2/12 + 2kT/C + \tfrac12A^2(2\pi f_{in}\sigma_t)^2 + \sigma_{comp}^2 + \cdots} ,
$$

where $\sigma_{comp}$ is the comparator's input-referred noise (§3.8).

![Total SNR of the running design against input frequency from 1 megahertz to 2 gigahertz for 0.1, 0.3 and 1 picosecond of jitter: each curve sits at the 71 decibel quantization plus kT/C floor at low frequency and bends down to follow its jitter-only line, which falls 20 decibels per decade](../../../assets/figures/20-05/jitter.svg)

*Figure 4. The running design's SNR with jitter. Each curve leaves the 71.0 dB floor where the jitter-limited SNR (dotted) approaches it and then falls 20 dB per decade.*

### 3.7 Latched comparators and regeneration

A comparator for a converter must resolve a small differential input $v_{in}$ to a logic level within a clock phase. A linear amplifier would need enormous gain-bandwidth. A latch uses positive feedback instead.

**Regeneration.** Two cross-coupled inverters, each with transconductance $g_m$, output resistance $r$ and load capacitance $C$, form a loop. With the differential output $v$:

$$
C\frac{dv}{dt} = g_mv - \frac{v}{r} \quad\Longrightarrow\quad v(t) = v_0e^{t/\tau}, \qquad \tau = \frac{C}{g_m - 1/r} \approx \frac{C}{g_m} .
$$

The output starts from the small initial imbalance $v_0$ and grows exponentially. It reaches a logic level $V_L$ after

$$
t_{dec} = \tau\ln\frac{V_L}{v_0} .
$$

Each factor of $e$ in input takes one $\tau$ less. Because $\tau \approx C/g_m$ is related to the transistor's speed ($g_m/C_{gs} = \omega_T$), latches in fast processes regenerate in picoseconds. Near the logic level the transistors leave their linear region and the growth slows, so this is a lower bound (the lab measures the difference).

![Latch differential output on a log scale against time for inputs of half an LSB, 1 millivolt and 10 millivolts: each simulated curve is a straight line at first, matching the dotted exponential, then bends over as the current limit is reached, crossing 0.6 volts about 24 picoseconds later than the exponential predicts](../../../assets/figures/20-05/regen.svg)

*Figure 5. Regeneration from three initial imbalances (τ = 20 ps, transconductors limited to 0.3 mA). On a log scale exponential growth is a straight line; every decade of input costs the same 46 ps (τ ln 10). Near the rails the current limit slows the growth (lab Part 5).*

**A preamplifier or integration phase** in front of the latch provides an initial gain $A_0$, so $v_0 = A_0v_{in}$. This shortens the decision, divides the latch's offset and noise by $A_0$, and isolates the input from the latch's large swings (kickback, §3.8).

### 3.8 The StrongARM latch

```text
   V_DD ── MP3, MP4 (PMOS cross-coupled) and reset switches S1–S4
             │                     │
             X                     Y        outputs
             │                     │
            MN3                   MN4       NMOS cross-coupled
             │                     │
             P                     Q        integration nodes
             │                     │
            MN1 ◄── v+       v− ──► MN2     input pair
             └──────────┬──────────┘
                        MT ◄── CLK          tail
                        │
                       GND
```

| Device | Drain | Gate | Source |
|---|---|---|---|
| MT (tail) | common node | CLK | GND |
| MN1, MN2 (input pair) | P, Q | $v_+$, $v_-$ | common node |
| MN3, MN4 (NMOS cross-coupled) | X, Y | Y, X | P, Q |
| MP3, MP4 (PMOS cross-coupled) | X, Y | Y, X | $V_{DD}$ |
| S1–S4 (PMOS reset switches) | X, Y, P, Q | CLK | $V_{DD}$ |

*Figure 2. The StrongARM latch (schematic sketch). During reset (CLK low) all four internal nodes are precharged to $V_{DD}$; when CLK rises the input pair discharges P and Q, then the cross-coupled pairs regenerate.*

The StrongARM latch was first reported as a low-power SRAM sense amplifier (Kobayashi et al., 1992–93); its name, according to Razavi's tutorial, commemorates its use in DEC's StrongARM microprocessor (1996) [1], [2]. It needs no static current, gives rail-to-rail outputs, and its offset comes mainly from one differential pair. It operates in three phases.

1. **Reset.** With the clock low, the tail is off and switches precharge P, Q, X and Y to $V_{DD}$.
2. **Integration.** The clock rises and the tail current $I_T$ flows. The input pair draws $I_T/2 \pm g_mv_{in}/2$ from P and Q, discharging their capacitance $C$. The nodes fall together, and their difference grows linearly. This lasts until P and Q have fallen by about $V_{TH}$, when the NMOS cross-coupled pair turns on: $t_{int} = CV_{TH}/(I_T/2)$. At that moment

$$
\Delta V_{PQ} = \frac{g_mv_{in}\,t_{int}}{C} = \frac{g_m}{I_T/2}V_{TH}\,v_{in} \quad\Longrightarrow\quad A_{int} = \left(\frac{g_m}{I_D}\right)V_{TH} .
$$

   The integration gain is the input pair's transconductance efficiency (20-01) times a threshold: about 5 to 10, a modest preamplifier built into the latch.
3. **Regeneration.** The cross-coupled NMOS and PMOS pairs take over and amplify the difference exponentially until X and Y reach opposite rails.

**Noise.** During integration, each input device's thermal noise current, with one-sided density $4kT\gamma g_m$ (12-10), is integrated on $C$. A white noise current of one-sided density $S_i$ integrated for a time $T$ deposits a charge of variance $S_iT/2$, so each node's noise variance is $2kT\gamma g_mt_{int}/C^2$, and the differential noise variance is twice that. Dividing by the signal gain squared, $(g_mt_{int}/C)^2$, and using $g_mt_{int} = A_{int}C$:

$$
\sigma_{in}^2 = \frac{4kT\gamma}{g_mt_{int}} = \frac{4\gamma}{A_{int}}\cdot\frac{kT}{C} .
$$

The comparator's input-referred noise is a kT/C noise, reduced by the integration gain. Two other sources are smaller. The precharge switches leave kT/C noise on P and Q, a differential variance $2kT/C$ that, referred to the input, is divided by $A_{int}^2$: the input pair's term is larger by $2\gamma A_{int}$, **9.0** in the running design, in line with Razavi's observation that it is typically four to eight times the switches' term [2]. Noise from the regeneration phase is also divided by about $A_{int}^2$.

> **Going deeper — why time-domain noise analysis.** The StrongARM is never in steady state, so its noise is not a spectral density times a bandwidth. Integrating the noise current over the integration window, as above, is the simplest correct treatment for this phase; a full analysis follows the noise through the time-varying regeneration as well (Nuzzo et al., 2008, in §14).

**The energy–noise trade-off.** Each decision recharges P and Q from $V_{DD}$, drawing an energy of about $E = 2CV_{DD}^2$ (plus the output nodes' $C_{XY}V_{DD}^2$, which this estimate omits [2]). Combining with $\sigma_{in}^2$:

$$
E\,\sigma_{in}^2 = \frac{8\gamma kT\,V_{DD}^2}{A_{int}} .
$$

Halving the noise costs four times the energy, the same square-root law as averaging $N$ independent measurements to reduce a standard error by $\sqrt N$. The product $E\sigma^2$, in nJ·µV², is called the comparator's **noise-efficiency factor**. The only escape is a larger $A_{int}$, which is why recent designs add a dynamic preamplifier with more gain per joule in front of the latch (§9).

**Offset.** Mismatch in the input pair's thresholds appears directly at the input: $\sigma(V_{os}) \approx A_{VT}/\sqrt{WL}$ (Pelgrom's law, 10-08). Mismatch in the latch is divided by $A_{int}$. Unequal capacitances at P and Q, or at X and Y, add a **dynamic offset** that depends on the clock edge and the common mode. A SAR ADC tolerates a comparator offset, because the same comparator makes every decision and the offset only shifts the transfer curve. A flash ADC, with a different comparator for each threshold, does not: its offsets become nonlinearity, so flash comparators need large devices, preamplifiers or calibration.

**Kickback.** When P, Q, X and Y swing by hundreds of millivolts, the input devices' gate–drain capacitance $C_{gd}$ couples the swing back to the inputs. If the source driving the input has capacitance $C_s$ (for example a capacitive DAC), the disturbance is about $\Delta V_{drain}C_{gd}/(C_{gd} + C_s)$. Its common part cancels between the two inputs. Its differential part disturbs the next decision unless it settles first, and in a flash ADC it disturbs the shared reference ladder.

### 3.9 Metastability and decision errors

A latch given time $T$ to decide resolves only inputs larger than

$$
v_{min} = \frac{V_L}{A_0}e^{-T/\tau} .
$$

Smaller inputs leave the output undecided, and downstream logic may read it either way or, worse, read different values in different places. If the comparator's input has probability density $p(0)$ near zero, the probability of an unresolved decision is $P = 2p(0)v_{min}$, falling exponentially with $T/\tau$.

**In a SAR ADC.** For an input uniform over the full scale, the residue at the $k$-th decision is spread uniformly over a range $V_{FS}/2^{k-1}$, so the late decisions see small inputs far more often. Summing over $N$ decisions:

$$
P_{SAR} = \sum_{k=1}^{N}\frac{2v_{min}\,2^{k-1}}{V_{FS}} = \frac{2v_{min}(2^N - 1)}{V_{FS}} \approx \frac{2v_{min}}{\Delta} .
$$

A metastable decision in a SAR is not a one-LSB error. If the comparator has not resolved when the logic samples it, the logic may set the wrong bit and every later bit then works toward the wrong value, or it may stall. The error can be large, so designers budget $P$ at $10^{-9}$ per conversion or below, and add metastability detectors in asynchronous SARs.

## 4. Worked examples

All examples use the running design: 12-bit, 100 MS/s, differential, $V_{FS}$ = 1.6 V peak to peak, $V_{DD}$ = 1.2 V, T130 at 300 K, unless stated.

### Example 20-05.1 · Sizing the sampling capacitor (tier A)

**Setup.** Find the LSB, the rms quantization noise, the capacitance per side that makes the differential kT/C noise equal to the quantization noise, the kT/C noise per side and differential, and the resulting SNR and ENOB. Then find the SNR with twice and four times that capacitance.

**Solution.**

- $\Delta$ = 1.6 V/4096 = **390.6** µV, and the rms quantization noise is $\Delta/\sqrt{12}$ = **112.8** µV.
- $C = 24kT/\Delta^2$ = 24 × 4.1419 × 10⁻²¹/(390.6 µV)² = **0.651** pF per side.
- $\sqrt{kT/C}$ = **79.7** µV per side; the differential noise $\sqrt{2kT/C}$ = **112.8** µV, equal to the quantization noise by design.
- The ideal 12-bit SNR is $6.02N + 1.76$ = **74.0** dB; with equal kT/C noise, **71.0** dB, an ENOB of $(71.0 - 1.76)/6.02$ = **11.5** bits.
- With $2C$: **72.2** dB. With $4C$: **73.0** dB.

**Sanity check.** Doubling the capacitor (and its drive power) buys 1.2 dB, and quadrupling it 2.0 dB. The returns diminish quickly once kT/C noise falls below quantization noise, which is why "equal noise" is a common design point.

### Example 20-05.2 · Sizing the sampling switch (tier B)

**Setup.** Half the 10 ns period is available for tracking. (a) Find the largest time constant and on-resistance that settle a full-scale step to half an LSB. (b) Size a bootstrapped NMOS switch ($L$ = 0.13 µm, body at ground) for that resistance at the worst-case input. (c) Compare its on-resistance at inputs of 0.2, 0.6 and 1.0 V with that of the same switch with its gate at $V_{DD}$, and find the highest input at which the plain switch still meets the resistance target.

**Solution.**

(a) $\tau \le$ 5 ns/9.01 = **0.555** ns, so $R_{on} \le \tau/C$ = **852** Ω.

(b) The body effect gives $V_{TH}$ = **0.492**, **0.566** and **0.629** V at 0.2, 0.6 and 1.0 V. The bootstrapped overdrive $V_{DD} - V_{TH}$ is smallest at 1.0 V: **0.571** V. Then $W/L = 1/(\mu C_{ox}R_{on}V_{ov})$ = 1/(3.01 × 10⁻⁴ A/V² × 852 Ω × 0.571 V) = **6.83**, so $W$ = **0.888** µm.

(c) On-resistance:

| $v_{in}$ | Bootstrapped | Gate at $V_{DD}$ |
|---|---|---|
| 0.2 V | **687** Ω | **958** Ω |
| 0.6 V | **767** Ω | **14.1** kΩ |
| 1.0 V | **852** Ω | off ($V_{ov}$ = **−0.429** V) |

The plain switch meets 852 Ω only for inputs below **0.147** V, outside the input range.

**Sanity check.** The track-mode bandwidth at the worst case is $1/(2\pi\tau)$ = **287** MHz, nearly six times the 50 MHz Nyquist frequency, as it must be to settle 9 time constants in half a period. The plain switch fails not by a little but completely: at 1.2 V supplies, bootstrapping is not an optimization.

### Example 20-05.3 · Charge injection and clock feedthrough (tier B)

**Setup.** For the switch of Example 20-05.2, find the channel charge and the injection error $Q_{ch}/2C$ at inputs of 0.2, 0.6 and 1.0 V, in millivolts and in LSBs. Then find the overlap capacitance and the clock feedthrough at 0.2 V and 1.0 V (bootstrapped gate falling from $v_{in} + V_{DD}$ to 0).

**Solution.** $WLC_{ox}$ = 0.888 µm × 0.13 µm × 8.6 fF/µm² = **0.993** fF, so $Q_{ch} = WLC_{ox}(V_{DD} - V_{TH})$:

| $v_{in}$ | $Q_{ch}$ | $Q_{ch}/2C$ | in LSB |
|---|---|---|---|
| 0.2 V | **0.703** fC | **0.539** mV | **1.38** |
| 0.6 V | **0.630** fC | **0.483** mV | **1.24** |
| 1.0 V | **0.567** fC | **0.435** mV | **1.11** |

$C_{ov}$ = 0.3 fF/µm × 0.888 µm = **0.266** fF. The feedthrough is $(v_{in} + V_{DD})C_{ov}/(C_{ov} + C)$: **0.572** mV at 0.2 V and **0.899** mV at 1.0 V.

**Sanity check.** Both errors are about an LSB, and both vary with the input by a few tenths of an LSB. A differential sampler cancels the common part. The signal-dependent part of the injection (0.104 mV across the range, **0.27** LSB) is mostly linear in $v_{in}$, so between the two sides it becomes a gain error, which a gain trim or calibration absorbs; only its curvature, from the body effect, is distortion. Bottom-plate sampling removes the top-plate switch's contribution entirely, which is why every precision SAR uses it.

### Example 20-05.4 · Tracking distortion of the bootstrapped switch (tier C)

**Setup.** One side of the sampler tracks a 0.4 V-amplitude sine around 0.6 V. (a) Expand $R_{on}(v)$ about 0.6 V and estimate the second harmonic at 10 MHz and 49 MHz. (b) Simulate the tracking (the full nonlinear triode law of §3.3) and find the second and third harmonics, with the body at ground and with the body tied to the source.

**Solution.**

(a) At 0.6 V, $R_0$ = **767** Ω, $\alpha = R'/R_0$ = **0.266** V⁻¹ and $\beta = R''/2R_0$ = **0.0234** V⁻². With $\omega R_0C$ = **0.0314** at 10 MHz and **0.154** at 49 MHz, $\text{HD}_2 \approx \omega R_0C\alpha A/2$ gives **−55.5** dBc and **−41.7** dBc. The first-order third harmonic $\omega R_0C\beta A^2/4$ is **−90.6** and **−76.8** dBc.

(b) Simulated:

| | HD2, 10 MHz | HD3, 10 MHz | HD2, 49 MHz | HD3, 49 MHz |
|---|---|---|---|---|
| Body at ground | **−55.5** dBc | **−87.9** dBc | **−41.5** dBc | **−64.4** dBc |
| Body tied to source | **−80.6** dBc | **−123.6** dBc | **−53.2** dBc | **−83.1** dBc |

The second-harmonic estimate agrees with simulation to within 0.2 dB. The third-harmonic estimate is 2.7 dB optimistic at 10 MHz and 12.4 dB optimistic at 49 MHz, because the second-order term of §3.4 dominates near Nyquist.

**Sanity check.** Differential operation cancels HD2, so the sampler's spurious-free dynamic range is set by HD3: 64.4 dB near Nyquist with the body grounded, below the 74 dB a 12-bit converter needs. Tying the body to the source (a triple-well device) gains 18.7 dB. The body effect, a second-order device property, decides whether this front end is good enough for 12 bits.

### Example 20-05.5 · Jitter (tier A)

**Setup.** (a) Find the jitter-limited SNR for a 49 MHz input with 1 ps rms jitter, and the running design's total SNR including quantization and kT/C noise. (b) What jitter gives 80 dB at 50 MHz? (c) An RF-sampling ADC digitizes a 1 GHz input with 100 fs of jitter: find its jitter-limited SNR.

**Solution.**

(a) $-20\log_{10}(2\pi \times 49\text{ MHz} \times 1\text{ ps})$ = **70.2** dB. Adding the noise powers: **67.6** dB.

(b) $\sigma_t = 10^{-80/20}/(2\pi \times 50\text{ MHz})$ = **0.318** ps.

(c) $-20\log_{10}(2\pi \times 1\text{ GHz} \times 100\text{ fs})$ = **64.0** dB.

**Sanity check.** One picosecond of jitter costs the running design 3.4 dB near Nyquist: it is comparable to the quantization and kT/C noise together. A sub-picosecond clock is part of a 12-bit, 100 MS/s specification. At 1 GHz, even 100 fs allows only about 10.3 bits, whatever the converter's resolution.

### Example 20-05.6 · A StrongARM comparator for the SAR (tier B)

**Setup.** The input pair is 4 µm/0.13 µm, biased so that $g_m/I_D$ = 15 S/A at the start of integration; $V_{TH}$ = 0.45 V and γ = 2/3. (a) Find $A_{int}$ and the input-referred noise with $C$ = 20 fF. (b) Find the $C$ that makes the noise a quarter of an LSB, the energy per decision, per conversion (12 decisions) and the comparator power at 100 MS/s. (c) Find the offset's standard deviation with $A_{VT}$ = 3.5 mV·µm, and the kickback onto one side's sampling capacitor if the drain swings 1.2 V through $C_{gd}$ = 1.2 fF.

**Solution.**

(a) $A_{int}$ = 15 × 0.45 = **6.75**. $\sigma_{in} = \sqrt{4\gamma kT/(A_{int}C)}$ = **0.286** mV at 20 fF, 0.73 LSB.

(b) For $\sigma_{in} = \Delta/4$ = **97.7** µV: $C = 4\gamma kT/(A_{int}\sigma_{in}^2)$ = **172** fF. The energy is $2CV_{DD}^2$ = **0.494** pJ per decision, **5.93** pJ per conversion, and **0.593** mW at 100 MS/s.

(c) $\sigma(V_{os})$ = 3.5 mV·µm/√(4 × 0.13 µm²) = **4.85** mV, about 12 LSB. Kickback: 1.2 V × 1.2 fF/(1.2 fF + 651 fF) = **2.21** mV per side.

**Sanity check.** The offset is large but harmless in a SAR (§3.8). The noise is not: it adds to every decision. The 172 fF that makes it small is large for a comparator, so practical SAR designs use a low-noise mode only for the last few decisions, or a preamplifier with more gain per joule. The kickback is mostly common mode, but at 5.6 LSB per side its differential residue must settle before the next decision.

### Example 20-05.7 · Regeneration and metastability (tier C)

**Setup.** The latch's regenerating nodes have 60 fF and the cross-coupled devices give $g_m$ = 3 mS; $V_L$ = 0.6 V; $A_0 = A_{int}$ = 6.75. (a) Find τ and the decision time for an input of half an LSB. (b) In a synchronous SAR that allows 300 ps per decision, find $v_{min}$ and the probability per conversion of an unresolved decision. (c) How long must each decision be to reach 10⁻⁹ per conversion, and what is the mean time between errors at 100 MS/s?

**Solution.**

(a) $\tau$ = 60 fF/3 mS = **20.0** ps. For $v_{in}$ = 195.3 µV, $v_0$ = **1.32** mV and $t_{dec}$ = 20 ps × ln(0.6/1.32 mV) = **122** ps.

(b) $v_{min}$ = (0.6/6.75) $e^{-15}$ = **27.2** nV. $P_{SAR} = 2v_{min}(2^{12} - 1)/V_{FS}$ = **1.39 × 10⁻⁴** per conversion, about 14,000 errors per second at 100 MS/s.

(c) Solving $P_{SAR}$ = 10⁻⁹ for $T$: **537** ps per decision. At 100 MS/s that is still one error every **10** s on average.

**Sanity check.** Going from 300 ps to 537 ps improves the error rate by five orders of magnitude, about 12 time constants: the exponential that made metastability a problem also makes it cheap to fix, once the time is available. But 12 decisions of 537 ps take 6.4 ns, most of the 10 ns period, before any DAC settling. This is why fast SARs are asynchronous (each decision starts when the previous one finishes) and use small-τ latches.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 20-05.1a | LSB | 390.6 | µV |
| Ex 20-05.1b | rms quantization noise | 112.8 | µV |
| Ex 20-05.1c | capacitance per side | 0.651 | pF |
| Ex 20-05.1d | kT/C noise per side | 79.7 | µV |
| Ex 20-05.1e | differential kT/C noise | 112.8 | µV |
| Ex 20-05.1f | ideal SNR | 74.0 | dB |
| Ex 20-05.1g | SNR with equal kT/C noise | 71.0 | dB |
| Ex 20-05.1h | ENOB | 11.5 | bits |
| Ex 20-05.1i | SNR with 2C | 72.2 | dB |
| Ex 20-05.1j | SNR with 4C | 73.0 | dB |
| Ex 20-05.2a | largest time constant | 0.555 | ns |
| Ex 20-05.2b | largest on-resistance | 852 | Ω |
| Ex 20-05.2c | V_TH at 0.2 V | 0.492 | V |
| Ex 20-05.2d | V_TH at 0.6 V | 0.566 | V |
| Ex 20-05.2e | V_TH at 1.0 V | 0.629 | V |
| Ex 20-05.2f | worst-case bootstrapped overdrive | 0.571 | V |
| Ex 20-05.2g | W/L | 6.83 | — |
| Ex 20-05.2h | W | 0.888 | µm |
| Ex 20-05.2i | bootstrapped R_on at 0.2 V | 687 | Ω |
| Ex 20-05.2j | bootstrapped R_on at 0.6 V | 767 | Ω |
| Ex 20-05.2k | plain R_on at 0.2 V | 958 | Ω |
| Ex 20-05.2l | plain R_on at 0.6 V | 14.1 | kΩ |
| Ex 20-05.2m | plain overdrive at 1.0 V | −0.429 | V |
| Ex 20-05.2n | highest input for the plain switch | 0.147 | V |
| Ex 20-05.2o | worst-case track bandwidth | 287 | MHz |
| Ex 20-05.3a | W L C_ox | 0.993 | fF |
| Ex 20-05.3b | Q_ch at 0.2 V | 0.703 | fC |
| Ex 20-05.3c | Q_ch at 0.6 V | 0.630 | fC |
| Ex 20-05.3d | Q_ch at 1.0 V | 0.567 | fC |
| Ex 20-05.3e | injection at 0.2 V | 0.539 | mV |
| Ex 20-05.3f | injection at 0.6 V | 0.483 | mV |
| Ex 20-05.3g | injection at 1.0 V | 0.435 | mV |
| Ex 20-05.3h | injection at 0.2 V in LSB | 1.38 | LSB |
| Ex 20-05.3i | injection at 0.6 V in LSB | 1.24 | LSB |
| Ex 20-05.3j | injection at 1.0 V in LSB | 1.11 | LSB |
| Ex 20-05.3k | overlap capacitance | 0.266 | fF |
| Ex 20-05.3l | feedthrough at 0.2 V | 0.572 | mV |
| Ex 20-05.3m | feedthrough at 1.0 V | 0.899 | mV |
| Ex 20-05.3n | signal-dependent injection across the range | 0.104 | mV |
| Ex 20-05.3o | signal-dependent injection in LSB | 0.27 | LSB |
| Ex 20-05.4a | R_0 | 767 | Ω |
| Ex 20-05.4b | alpha | 0.266 | 1/V |
| Ex 20-05.4c | beta | 0.0234 | 1/V² |
| Ex 20-05.4d | omega R_0 C at 10 MHz | 0.0314 | — |
| Ex 20-05.4e | omega R_0 C at 49 MHz | 0.154 | — |
| Ex 20-05.4f | HD2 estimate, 10 MHz | −55.5 | dBc |
| Ex 20-05.4g | HD2 estimate, 49 MHz | −41.7 | dBc |
| Ex 20-05.4h | HD3 first-order estimate, 10 MHz | −90.6 | dBc |
| Ex 20-05.4i | HD3 first-order estimate, 49 MHz | −76.8 | dBc |
| Ex 20-05.4j | simulated HD2, body grounded, 10 MHz | −55.5 | dBc |
| Ex 20-05.4k | simulated HD3, body grounded, 10 MHz | −87.9 | dBc |
| Ex 20-05.4l | simulated HD2, body grounded, 49 MHz | −41.5 | dBc |
| Ex 20-05.4m | simulated HD3, body grounded, 49 MHz | −64.4 | dBc |
| Ex 20-05.4n | simulated HD2, body tied, 10 MHz | −80.6 | dBc |
| Ex 20-05.4o | simulated HD3, body tied, 10 MHz | −123.6 | dBc |
| Ex 20-05.4p | simulated HD2, body tied, 49 MHz | −53.2 | dBc |
| Ex 20-05.4q | simulated HD3, body tied, 49 MHz | −83.1 | dBc |
| Ex 20-05.4r | HD3 estimate error, 10 MHz | 2.7 | dB |
| Ex 20-05.4s | HD3 estimate error, 49 MHz | 12.4 | dB |
| Ex 20-05.4t | gain from tying the body | 18.7 | dB |
| Ex 20-05.5a | jitter SNR, 49 MHz, 1 ps | 70.2 | dB |
| Ex 20-05.5b | total SNR | 67.6 | dB |
| Ex 20-05.5c | jitter for 80 dB at 50 MHz | 0.318 | ps |
| Ex 20-05.5d | jitter SNR, 1 GHz, 100 fs | 64.0 | dB |
| Ex 20-05.5e | SNR cost of 1 ps | 3.4 | dB |
| Ex 20-05.5f | bits at 64.0 dB | 10.3 | bits |
| Ex 20-05.6a | A_int | 6.75 | — |
| Ex 20-05.6b | noise at 20 fF | 0.286 | mV |
| Ex 20-05.6c | noise at 20 fF in LSB | 0.73 | LSB |
| Ex 20-05.6d | target noise | 97.7 | µV |
| Ex 20-05.6e | capacitance for the target | 172 | fF |
| Ex 20-05.6f | energy per decision | 0.494 | pJ |
| Ex 20-05.6g | energy per conversion | 5.93 | pJ |
| Ex 20-05.6h | comparator power | 0.593 | mW |
| Ex 20-05.6i | offset sigma | 4.85 | mV |
| Ex 20-05.6j | offset in LSB | 12 | LSB |
| Ex 20-05.6k | kickback per side | 2.21 | mV |
| Ex 20-05.6l | kickback in LSB | 5.6 | LSB |
| Ex 20-05.7a | tau | 20.0 | ps |
| Ex 20-05.7b | v_0 for half an LSB | 1.32 | mV |
| Ex 20-05.7c | decision time | 122 | ps |
| Ex 20-05.7d | v_min at 300 ps | 27.2 | nV |
| Ex 20-05.7e | P per conversion at 300 ps | 1.39e-4 | — |
| Ex 20-05.7f | errors per second at 300 ps | 1.4×10⁴ | 1/s |
| Ex 20-05.7g | time per decision for 1e-9 | 537 | ps |
| Ex 20-05.7h | mean time between errors | 10 | s |
| Ex 20-05.7i | time constants gained | 12 | — |
| Ex 20-05.7j | 12 decisions at 537 ps | 6.4 | ns |
| Txt 20-05.a | sqrt(kT/C) at 1 pF | 64.4 | µV |
| Txt 20-05.b | ln 2^13 | 9.01 | — |
| Txt 20-05.c | plain switch cutoff input | 0.63 | V |
| Txt 20-05.d | 14-bit capacitance per side | 10.4 | pF |
| Txt 20-05.e | input pair to precharge noise ratio | 9.0 | — |
| Txt 20-05.f | jitter-limited SNR, 60 fs at 7.997 GHz | 50.4 | dB |
| Txt 20-05.g | jitter-limited SNR, 50 fs at 7.997 GHz | 52.0 | dB |
| Txt 20-05.h | running design's noise-efficiency factor | 4.7 | nJ·µV² |
| Txt 20-05.i | StrongARM noise-efficiency factor implied by Zhuang et al. | 16 | nJ·µV² |
| Txt 20-05.j | 90 fs at 3.5 GHz | 54.1 | dB |
| Txt 20-05.k | regeneration tau from 44 ps per decade | 19 | ps |
| Txt 20-05.l | effective bits at 50.4 dB | 8 | bits |
| Txt 20-05.m | years between errors at 1e-18 and 10.4 GS/s | 3 | years |
| Txt 20-05.n | days between errors at 1e-15 and 3 GS/s | 4 | days |
| Txt 20-05.o | tau ln 10 | 46 | ps |
| Txt 20-05.p | ADC32RF45 SNR relative to the carrier | 52.2 | dB |

## 5. Simulate it

The lab ([labs/20-05-lab](../labs/20-05-lab/README.md)) implements the switch, the jitter budget, the StrongARM's noise and the regeneration in `sh.py`, and confirms three results in ngspice.

**Predict, then run.**

1. Predict the integrated noise of an RC low-pass with $C$ = 0.651 pF for $R$ = 100 Ω and 10 kΩ, then run `ngspice -b ktc.cir` (Part 1).
2. Plot $R_{on}$ against the input for the plain and bootstrapped switches (Part 2).
3. Predict the third harmonic at 49 MHz with the body grounded and tied to the source, then run the simulation and `ngspice -b switch.cir` (Part 3).
4. Plot SNR against input frequency for jitter of 0.1, 0.3 and 1 ps (Part 4).
5. Predict the decision time for half an LSB, then simulate the current-limited latch in Python and `ngspice -b latch.cir` (Part 5).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Larger sampling capacitor | kT/C noise (SNR) | Driver power, switch size, input bandwidth; 4× per bit | Converter architect |
| Wider sampling switch | Settling, bandwidth | Charge injection, clock feedthrough, bootstrap capacitor size | Analog designer |
| Bootstrapping, triple-well switch | Linearity over the full range at low supply | Area, reliability care (gate stress), process option | Analog designer with the process team |
| Lower clock jitter | High-frequency SNR | Clock-generation power (PLL, buffers), board design | System architect (clocking) |
| Larger comparator capacitance | Comparator noise | Energy per decision (square-root law), slower regeneration | Analog designer |
| Larger input pair | Offset (flash), noise | Kickback, input capacitance | Analog designer |
| More time per decision | Metastability error rate (exponentially) | Conversion rate | Converter architect |

## 7. Numbers to know

| Quantity | Typical value | Note |
|---|---|---|
| $\sqrt{kT/C}$ at 300 K | 64.4 µV at 1 pF; 20.4 µV at 10 pF | exact; capacitance ×4 per bit of resolution |
| Jitter-limited SNR | $-20\log_{10}(2\pi f_{in}\sigma_t)$ | 64 dB at 1 GHz with 100 fs; −20 dB per decade [7] |
| Best sampling jitter (as of Nov 2026) | tens of femtoseconds | 50 fs stated in an ISSCC 2016 abstract; 50–90 fs on current TI RF-sampling ADC data sheets [R-332], [R-333] |
| Dynamic comparator noise (as of Nov 2026) | about 0.3–1.5 mV for latch-type designs; under 50 µV with dynamic preamplifiers | 1.5 mV at 92 fJ (double tail, 90 nm, 2007); 46 µV at 1 pJ (FIA, 180 nm, 2020); 38 µV at 0.48 pJ (28 nm, 2025) [R-331] |
| Comparator offset, uncalibrated | several mV | 8 mV σ (90 nm, 2007); 4.7 mV in a 28 nm design example; 1.69 mV after calibration [R-331] |
| Regeneration time constant | about 20 ps (90 nm) to about 2.5–3 ps (28 nm and below) | 19 ps derived from 44 ps per decade (Schinkel, 2007); 2.5 ps (Razavi's 28 nm example); about 3 ps "in leading-edge technology" (Murmann, 2022) [R-331], [R-332] |
| Code (metastability) error rate of RF-sampling ADCs (as of Nov 2026) | 10⁻¹⁵ to 10⁻¹⁸ errors per sample | TI ADC32RF55 and ADC12DJ5200RF data sheets [R-333] |
| Flash-ADC metastability, measured | below 10⁻¹² errors per cycle with error reduction, about 10⁻⁴ estimated without | Portmann and Meng, 1996 [R-331] |

## 8. Common mistakes

- **Thinking a smaller switch reduces kT/C noise.** The resistance cancels: only the capacitance matters (§3.2). A bigger resistance only slows settling.
- **Forgetting the factor 2 in a differential sampler.** Two capacitors, two independent noises: the differential variance is $2kT/C$.
- **Sizing the switch at mid-scale.** Size it where the overdrive is smallest, at the top of the input range with the body effect included.
- **Quoting jitter without frequency.** Jitter's cost is proportional to the input frequency; "1 ps" is generous at 1 MHz and fatal at 1 GHz.
- **Assuming differential operation removes all distortion.** It cancels even harmonics; the third harmonic remains and grows with frequency.
- **Treating comparator offset as fatal in a SAR.** One comparator makes every decision, so offset shifts the curve without distorting it; noise, not offset, is the SAR's comparator problem.
- **Treating metastability as a one-LSB error.** An unresolved decision can corrupt every later bit of a SAR conversion, or stall it.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **The circuits are decades old; their refinements are not [Established].** The StrongARM latch dates from 1992–93 [1], [2] and the precharged-capacitor bootstrapped switch from the late 1990s [3]. Both remain the default choices: Razavi's 2015 tutorials call them "circuits for all seasons," and his 2020 design example in 28 nm reaches a 2.5 ps regeneration time constant, 0.31 mV of noise and 4.7 mV of offset at about 0.2 mW and 5 GHz (simulated) [R-331].
- **Comparator energy is now spent on preamplification [Established].** A dynamic-bias preamplifier cut energy about 2.5× at equal noise (Bindra et al., 2018). The floating-inverter-amplifier (FIA) comparator reached 46 µV of noise at 1 pJ in 180 nm, reported as more than seven times the energy efficiency of a StrongARM latch (Tang et al., 2020). A stacked FIA reached 38 µV at 0.48 pJ in 28 nm, a noise-efficiency factor of 0.69 nJ·µV², which its authors report as 23 times better than a classic StrongARM (Zhuang et al., 2025), implying about **16** nJ·µV² for the StrongARM they compare against [R-331].
- **Sampling jitter is at tens of femtoseconds [Established].** An ISSCC 2016 RF ADC states that "SNR is dominated by aperture jitter of 50fs" at a 3.8 GHz input. Murmann's survey of ISSCC and VLSI converters (updated through VLSI 2026) draws 1 ps and 0.1 ps jitter lines, and his 2022 short course summarizes high-speed converters as limited by "tens of femtoseconds timing jitter" [R-332]. TI's current RF-sampling ADCs specify 50 fs (ADC12DJ5200RF with its dither off, 60 fs with it on; ADC32RF55) to 90 fs (ADC32RF45) of aperture jitter [R-333]. At 7.997 GHz, 50 fs alone allows at most **52.0** dB of SNR; at 3.5 GHz, 90 fs allows **54.1** dB relative to the carrier, and the ADC32RF45's 54.2 dBFS at a −2 dBFS input, **52.2** dB relative to the carrier, shows that jitter supplies about two-thirds of its noise there [R-333].
- **Metastability is specified, not ignored [Established].** RF-sampling ADC data sheets give code error rates of 10⁻¹⁵ to 10⁻¹⁸ per sample and attribute such errors to comparator metastability; TI's claim that its architecture is "multiple orders of magnitude better" than pipelined flash or SAR converters at equal rates is a vendor statement **[Contested]** [R-333]. For SAR converters, assuming a uniform input overestimates the signal-to-metastability ratio by up to 18 dB compared with Gaussian or Laplacian inputs (Waters et al., 2016) [R-331].

### Why it matters commercially

Sampling and comparison set the floor of every data converter, and data converters are in nearly every product in a semiconductor company's portfolio. In AI datacenter networking, 100–200 Gb/s-per-lane SerDes receivers are ADC-based, and their samplers' jitter and their comparators' metastability set the link's error floor (**Deeper:** see companion repo *Datacenter Networking*). In wireless infrastructure and radar, RF-sampling ADCs digitize gigahertz signals directly, so their aperture jitter, not their bit count, decides the usable SNR (Example 20-05.5). In wearables and IoT, a SAR ADC's comparator is often the largest consumer of its energy, and the energy–noise square-root law decides battery life per measurement. For an acquirer or investor, a converter team's competence shows in how it budgets noise, jitter and metastability against each other, not in its headline bit count.

### Marketing vs Reality

- **"12-bit ADC."** The bit count is the quantizer's. The effective number of bits at your input frequency is set by kT/C, jitter and distortion: a 12-bit converter at 8 GHz with 60 fs of jitter (the ADC12DJ5200RF with dither on) cannot exceed 50.4 dB of jitter-limited SNR, about 8 effective bits. TI's ADC12DJ5200RF specifies 49.6 dBFS at 7997 MHz, consistent with that limit [R-333].
- **"50 fs aperture jitter."** That is the converter's own contribution. The system's jitter is the root-sum-square of it and the clock source's and buffers' jitter, and TI notes the aperture jitter rises as the clock's slew rate falls [7]. Ask for the SNR at your input frequency with your clock.
- **"7× (or 23×) better than a StrongARM."** Energy-efficiency claims for comparators depend on the noise level at which they are compared, because energy scales as 1/noise². The noise-efficiency factor $E\sigma^2$ makes them comparable. Even so, the baseline matters: the chapter's idealized StrongARM model gives **4.7** nJ·µV², about a third of the 16 nJ·µV² implied for the published baseline, because real latches have parasitics, regeneration noise and output-node energy that the model omits.
- **Code error rates.** 10⁻¹⁸ errors per sample at 10.4 GS/s is about one error every three years per converter; 10⁻¹⁵ at 3 GS/s is about one every four days. Whether that matters depends on the application, and data sheets exclude the digital interface's own bit errors [R-333].
- **Sanity check.** For any converter claim, compute $-20\log_{10}(2\pi f_{in}\sigma_t)$ with the stated jitter at the stated frequency; if the claimed SNR exceeds it, something in the test conditions is different from what you assume.

### Questions for engineering leaders

1. **"What limits your SNR at the top of your input band: kT/C, jitter or distortion?"** Strong: a noise budget with each term in µV or dB at a stated frequency. Evasive: the low-frequency SNR.
2. **"What sampling-clock jitter does your specification assume, and who supplies that clock?"** Strong: a jitter number at the converter's pins, with the PLL and buffer contributions. Evasive: "the ADC has 50 fs aperture jitter."
3. **"How did you choose the comparator's noise, and what does it cost in energy?"** Strong: noise referred to the LSB, energy per decision, and why that point on the square-root curve. Evasive: "it's a StrongARM."
4. **"What is your metastability error rate, under what input distribution, and what happens when one occurs?"** Strong: a computed and measured rate, a realistic input distribution, and a bounded error size. Evasive: "we've never seen one."
5. **"How do you handle the sampling switch's linearity at your supply voltage?"** Strong: bootstrapping with body handling, measured HD3 near Nyquist. Evasive: a low-frequency SFDR only.

## 10. Concept check

**Q1.** Why does the sampled thermal noise not depend on the switch's resistance?

<details><summary>Answer</summary>

The resistor's noise density is proportional to $R$, but the RC bandwidth is proportional to $1/R$; the product, integrated, is $kT/C$. Equivalently, by equipartition a capacitor in thermal equilibrium holds $\tfrac12kT$ of energy on average whatever it is connected to.

</details>

**Q2.** A 12-bit design needs $C$ = 0.651 pF. What capacitance does a 14-bit design with the same full scale need, and why does this matter for power?

<details><summary>Answer</summary>

Two more bits make the LSB four times smaller, so $C = 24kT/\Delta^2$ grows sixteenfold, to about 10.4 pF. The input driver and reference buffer must charge that capacitance in the same time, so their power rises roughly in proportion.

</details>

**Q3.** Why can a plain NMOS switch not sample the running design's full input range at 1.2 V, and what does bootstrapping change?

<details><summary>Answer</summary>

With the gate at $V_{DD}$, the overdrive $V_{DD} - v_{in} - V_{TH}(v_{in})$ falls to zero near 0.63 V, so the switch turns off for higher inputs. Bootstrapping makes $V_G = v_{in} + V_{DD}$, so the overdrive is $V_{DD} - V_{TH}(v_{in})$ over the whole range and varies only through the body effect.

</details>

**Q4.** What limits the SNR of a 2 GHz input sampled with 50 fs of jitter, regardless of the ADC's resolution?

<details><summary>Answer</summary>

$\text{SNR} = -20\log_{10}(2\pi \times 2\text{ GHz} \times 50\text{ fs})$ ≈ 64 dB: about 10.3 effective bits, whatever the quantizer.

</details>

**Q5.** Why is the StrongARM's integration gain about $(g_m/I_D)V_{TH}$?

<details><summary>Answer</summary>

Each integration node discharges at $I_T/2$ until it has fallen by about $V_{TH}$, which takes $t_{int} = CV_{TH}/(I_T/2)$. During that time the difference current $g_mv_{in}$ builds a differential voltage $g_mv_{in}t_{int}/C = [g_m/(I_T/2)]V_{TH}v_{in}$.

</details>

**Q6.** To halve a dynamic comparator's input-referred noise at fixed integration gain, how much more energy per decision is needed?

<details><summary>Answer</summary>

Four times: $\sigma^2 \propto 1/C$ and $E \propto C$, so $E\sigma^2$ is constant.

</details>

**Q7.** Why does a SAR ADC's metastability probability depend mostly on its last decisions?

<details><summary>Answer</summary>

The comparator's input at the $k$-th decision is the residue, spread over $V_{FS}/2^{k-1}$; the last decisions see inputs of order an LSB, so small inputs, which take longest to resolve, are $2^{N-1}$ times more likely there than at the first decision.

</details>

Problems: [20-05 problem set](../problems/20-05-problems.md) · Worked solutions: [20-05 solutions](../solutions/20-05-solutions.md)

## 11. Key terms

[Sample-and-hold](../../../reference/glossary.md#sample-and-hold) · [kT/C noise](../../../reference/glossary.md#ktc-noise) · [Bootstrapped switch](../../../reference/glossary.md#bootstrapped-switch) · [Charge injection](../../../reference/glossary.md#charge-injection) · [Clock feedthrough](../../../reference/glossary.md#clock-feedthrough) · [Bottom-plate sampling](../../../reference/glossary.md#bottom-plate-sampling) · [Aperture jitter](../../../reference/glossary.md#aperture-jitter) · [StrongARM latch](../../../reference/glossary.md#strongarm-latch) · [Regeneration time constant](../../../reference/glossary.md#regeneration-time-constant) · [Kickback](../../../reference/glossary.md#kickback) · [Metastability](../../../reference/glossary.md#metastability)

## 12. Connections

- **Previous:** [20-04](20-04-ldo-regulators.md) supplies the quiet supply and [20-03](20-03-bandgap-references.md) the reference that a converter's samples and decisions are measured against.
- **Builds on:** [11-10](../../11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md) (ideal sampling), [12-10](../../12-electronics-2/chapters/12-10-noise-in-circuits.md) (thermal noise), [08-10](../../08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md) (metastability in flip-flops), [10-08](../../10-electronics-1/chapters/10-08-current-sources-and-mirrors.md) (Pelgrom mismatch), [20-01](20-01-analog-design-fundamentals-gm-id.md) ($g_m/I_D$).
- **Next:** [20-06](20-06-data-converter-fundamentals.md) defines the converter metrics (SNR, SNDR, SFDR, ENOB, figures of merit) that this chapter's noise and distortion feed.
- **Used later:** [20-07](20-07-nyquist-adcs.md) (flash, SAR and pipeline ADCs built from these blocks), [20-08](20-08-sigma-delta-converters.md), [20-10](20-10-plls-and-jitter.md) (where the sampling clock's jitter comes from), [20-12](20-12-why-analog-does-not-scale.md) (kT/C as a scaling limit).

## 13. Further study

- B. Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed., McGraw-Hill, 2017: the switched-capacitor and comparator chapters.
- M. Pelgrom, *Analog-to-Digital Conversion*, 4th ed., Springer, 2022: the sample-and-hold and comparator chapters.
- B. Razavi, "The StrongARM latch," *IEEE Solid-State Circuits Magazine*, 2015, and "The bootstrapped switch," *IEEE Solid-State Circuits Magazine*, 2015: short, clear tutorials (cited in §14).
- Lecture videos: data-converter lectures from university courses on mixed-signal IC design (search for "sample and hold kT/C lecture" and "StrongARM latch lecture").

## 14. Sources

1. T. Kobayashi, K. Nogami, T. Shirotori and Y. Fujimoto, "A current-controlled latch sense amplifier and a static power-saving input buffer for low-power architecture," *IEEE J. Solid-State Circuits*, vol. 28, no. 4, pp. 523–527, Apr. 1993, DOI 10.1109/4.210039 (VLSI Symposium version, June 1992) [R-331].
2. B. Razavi, "The StrongARM latch [A circuit for all seasons]," *IEEE Solid-State Circuits Magazine*, vol. 7, no. 2, pp. 12–17, Spring 2015, DOI 10.1109/MSSC.2015.2418155; and "The design of a comparator," vol. 12, no. 4, pp. 8–14, Fall 2020, DOI 10.1109/MSSC.2020.3021865 [R-331].
3. B. Razavi, "The bootstrapped switch [A circuit for all seasons]," *IEEE Solid-State Circuits Magazine*, vol. 7, no. 3, pp. 12–15, Summer 2015, DOI 10.1109/MSSC.2015.2449714; A. M. Abo and P. R. Gray, "A 1.5-V, 10-bit, 14.3-MS/s CMOS pipeline analog-to-digital converter," *IEEE J. Solid-State Circuits*, vol. 34, no. 5, pp. 599–606, May 1999, DOI 10.1109/4.760369; M. Dessouky and A. Kaiser, "Very low-voltage digital-audio ΔΣ modulator with 88-dB dynamic range using local switch bootstrapping," *IEEE J. Solid-State Circuits*, vol. 36, no. 3, pp. 349–355, Mar. 2001, DOI 10.1109/4.910473 [R-331].
4. P. Nuzzo, F. De Bernardinis, P. Terreni and G. Van der Plas, "Noise analysis of regenerative comparators for reconfigurable ADC architectures," *IEEE Trans. Circuits Syst. I*, vol. 55, no. 6, pp. 1441–1454, July 2008, DOI 10.1109/TCSI.2008.917991; P. M. Figueiredo and J. C. Vital, "Kickback noise reduction techniques for CMOS latched comparators," *IEEE Trans. Circuits Syst. II*, vol. 53, no. 7, pp. 541–545, July 2006 [R-331].
5. Recent comparators: D. Schinkel et al., ISSCC 2007, paper 17.7; H. S. Bindra et al., *IEEE JSSC*, July 2018; X. Tang et al., *IEEE JSSC*, Apr. 2020; H. Zhuang et al., *IEEE JSSC*, Mar. 2025; A. K. Rajendra et al., *IEEE JSSC*, June 2026 [R-331].
6. Metastability: C. L. Portmann and T. H. Y. Meng, "Power-efficient metastability error reduction in CMOS flash A/D converters," *IEEE J. Solid-State Circuits*, vol. 31, no. 8, pp. 1132–1140, Aug. 1996; A. Waters, J. Muhlestein and U.-K. Moon, "Analysis of metastability errors in conventional, LSB-first, and asynchronous SAR ADCs," *IEEE Trans. Circuits Syst. I*, vol. 63, no. 11, pp. 1898–1909, Nov. 2016 [R-331].
7. T. Neu, "Clock jitter analyzed in the time domain, Part 1," TI *Analog Applications Journal* SLYT379, 3Q 2010; National Semiconductor AN-775 (TI SNOA223), "Specifications and architectures of sample-and-hold amplifiers," 1992 [R-332].
8. R. H. Walden, "Analog-to-digital converter survey and analysis," *IEEE J. Sel. Areas Commun.*, vol. 17, no. 4, pp. 539–550, Apr. 1999; B. Murmann, "ADC Performance Survey 1997–2026," github.com/bmurmann/ADC-survey (revision 2026-08-01), and ISSCC 2022 short course; M. Straayer et al., ISSCC 2016, paper 27.5 [R-332].
9. Texas Instruments data sheets ADC12DJ5200RF (SLVSEN9H), ADC32RF45 (SBAS747C), ADC32RF55 (SBAS500B), ADC12DJ3200 (SLVSD97A) and LF398 (SNOSBI3C) [R-333].
10. Course chapters [12-10](../../12-electronics-2/chapters/12-10-noise-in-circuits.md) (thermal noise), [08-10](../../08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md) (metastability) and [10-08](../../10-electronics-1/chapters/10-08-current-sources-and-mirrors.md) (Pelgrom mismatch).
