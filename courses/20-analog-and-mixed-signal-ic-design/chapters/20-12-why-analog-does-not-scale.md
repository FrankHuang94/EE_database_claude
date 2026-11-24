<!-- status: verified -->
# 20-12 · Why Analog Does Not Scale Like Digital

| | |
|---|---|
| **Course** | [20 · Analog and Mixed-Signal IC Design](../README.md) |
| **University equivalent** | The technology-scaling discussion that closes a graduate analog IC course: supply headroom, intrinsic gain, kT/C noise and matching against scaling, and digitally assisted analog (Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed., the nanometer-design chapter; Kinget, "Device mismatch and tradeoffs in the design of analog circuits", 2005; Murmann, "Digitally assisted analog circuits", 2006) |
| **Prerequisites** | [09-11](../../09-semiconductor-devices/chapters/09-11-cmos-and-scaling.md) (constant-field scaling), [20-01](20-01-analog-design-fundamentals-gm-id.md) ($g_m/I_D$, intrinsic gain), [20-05](20-05-comparators-and-sample-and-hold.md) (kT/C), [20-06](20-06-data-converter-fundamentals.md) (the 8kT·SNR limit), [20-11](20-11-layout-matching-pvt.md) (Pelgrom's law) |
| **Estimated study hours** | 5 |
| **Last verified** | 2026-11-24 |

**Learning objectives.** After this chapter you can:

1. Contrast what constant-field scaling gives a logic gate with what it gives a noise-limited analog circuit.
2. Derive why a thermal-noise-limited circuit's power rises as the supply voltage falls.
3. Explain why intrinsic gain and headroom shrink together, and check a transistor stack against a supply.
4. Distinguish mismatch-limited from noise-limited circuits, and say which of them benefits from scaling.
5. Compute what a digital calibration must achieve to replace analog precision.
6. Judge claims about analog scaling, analog area and chiplet partitioning against dated data.

## 1. Big picture

Every new process node makes logic smaller, faster and cheaper per function, and the industry's economics are built on that. Analog circuits come along for the ride only partly. A logic gate needs to tell two levels apart; an analog circuit must hold a signal well above a noise floor set by temperature, with gain and matching set by device physics. Shrinking the supply squeezes the signal while the floor stays put; shrinking the transistor lowers its gain; and the area that matching demands is set by the accuracy target, not by the lithography. This chapter derives those limits, shows where scaling still helps analog (speed, and matching per unit of capacitance), and explains the industry's answer: do as little as possible in analog and fix the rest with cheap digital logic.

- **System-on-chip area:** analog and mixed-signal blocks (PLLs, data converters, regulators, I/O) occupy a growing share of an advanced-node die because they shrink less than logic.
- **Power:** a high-resolution converter or low-noise amplifier does not get cheaper in energy just because the node is newer.
- **Architecture:** SAR and time-interleaved ADCs, digital PLLs and calibrated pipelines exist because they turn analog problems into digital ones (20-07, 20-10).
- **Partitioning:** chiplet designs place I/O and analog functions on older, cheaper nodes when they gain little from the newest one (§9).
- **Diligence:** "our analog scales with the process" is a claim to test, not to accept.

## 2. Intuition first

```text
 supply            1.8 V ┤███████████████████ signal swing          0.8 V ┤████████ signal swing
                         │                                                │
 thermal noise floor     ┤▒ kT/C (same physics at every node)            ┤▒ kT/C (unchanged)
                         └──────────────────────                          └──────────────────────
                           older node: big swing, same floor                newer node: less room above the same floor
```

*Figure 1. Scaling lowers the ceiling, not the floor. To keep the same signal-to-noise ratio with a smaller swing, the noise floor must come down, which means larger capacitors and more current.*

**Two weighing scales.** A digital gate is like a postal scale that only has to say "over or under 1 kg": a cheaper, smaller scale works as well, and the industry has made scales smaller and cheaper for decades. An analog circuit is like a laboratory balance that must read to a microgram: its precision is limited by the jitter of air molecules on the pan (thermal noise) and by how well its two arms are machined (matching). Making the balance smaller does nothing for the air molecules and makes the arms harder to match. The analogy breaks in two places, both treated below: a smaller analog "balance" does respond faster (higher $f_T$), and newer processes do make better-matched arms per unit of the capacitance they cost (§3.4).

## 3. Theory

### 3.1 What scaling gives digital

Constant-field scaling (09-11) divides every dimension and voltage by a factor $S > 1$. A gate's capacitance falls by $S$ (area $1/S^2$, oxide $1/S$), its voltage by $S$ and its current by $S$, so:

- the gate delay $CV/I$ falls by $S$;
- the switching energy $CV^2$ falls by $S^3$;
- the area per gate falls by $S^2$;
- the power density stays constant.

A digital designer receives all four at once, at no cost in correctness, because a gate's output only needs to land on the right side of a threshold. Real scaling since about 2005 has held the supply nearly constant (the threshold cannot fall without leakage, 09-11), so the energy gain has been closer to $S$ than $S^3$, but density and speed have kept improving.

### 3.2 Headroom against the kT/C floor

Consider any circuit whose accuracy is set by thermal noise sampled on a capacitor: a sample-and-hold, a switched-capacitor stage, the input of an ADC. From 20-05, the sampled noise variance is $kT/C$ whatever the switch resistance. A sine of peak amplitude $A$ has power $A^2/2$, so the signal-to-noise ratio is

$$
\text{SNR} = \frac{A^2/2}{kT/C} \quad\Longrightarrow\quad C = \frac{2kT\cdot\text{SNR}}{A^2} .
$$

Let the swing use a fraction $\eta$ of the supply, $A = \eta V_{DD}/2$. Then $C = 8kT\cdot\text{SNR}/(\eta^2V_{DD}^2)$: **halving the supply quadruples the capacitance** for the same SNR.

Now drive that capacitor. A class-A stage with transconductance $g_m$ and feedback factor $\beta$ settles with closed-loop bandwidth $f = \beta g_m/(2\pi C)$, so it needs $g_m = 2\pi fC/\beta$ and a current $I = g_m/(g_m/I_D)$. Its supply power is $P = V_{DD}I$:

$$
P = \frac{V_{DD}\cdot 2\pi f C}{\beta\,(g_m/I_D)} = \frac{16\pi\,kT\cdot\text{SNR}\cdot f}{\beta\,\eta^2\,(g_m/I_D)\,V_{DD}} .
$$

Every factor on the right except $V_{DD}$ is set by the specification or by physics. So **at fixed SNR and bandwidth, the power of a thermal-noise-limited circuit rises as $1/V_{DD}$** (Example 20-12.2), the opposite of digital's $CV^2$. Units: J × Hz / (V⁻¹ × V) = J/s = W.

Two effects make it worse in practice. First, the swing fraction η falls at low supply, because each transistor in the signal path needs a fixed $V_{DS,sat}$ of roughly 100–150 mV (20-01) that does not scale with the node; η enters squared. Second, the threshold voltage scales slowly (subthreshold leakage, 09-11), so a low supply leaves little room for the gate overdrive that sets $V_{DS,sat}$.

Compare the survey's 8kT·SNR line of 20-06, $P = 8kT\cdot\text{SNR}\cdot f_s$, which has no $V_{DD}$: it is the bound for an ideal class-B driver that swings rail to rail and wastes no supply voltage (evaluated conservatively at $f = f_s$). The formula above shows why real class-A circuits, which waste the supply-minus-swing headroom, lose ground as the supply falls.

![Power of the 74 dB, 100 MHz buffer against supply from 0.45 to 3.3 V on a log scale: with the swing fixed at 80 percent of the supply the power falls slowly from about 120 microwatts to 17 as the supply rises; with a swing of the supply minus 0.3 V it rises steeply below 1 V to about 700 microwatts at 0.45 V; a dashed digital C V squared curve does the opposite, falling toward low supplies](../../../assets/figures/20-12/power.svg)

*Figure 2. The buffer of Example 20-12.2 (dots at 1.8 V and 0.8 V). With a swing proportional to the supply, power rises as $1/V_{DD}$; with a fixed 0.3 V of headroom it rises far faster. A digital $CV^2f$ load, matched at 1.8 V, goes the other way.*

### 3.3 Intrinsic gain and the stack

One transistor's maximum voltage gain is its **intrinsic gain** (20-01):

$$
A_i = g_mr_o = \frac{g_m}{I_D}\,V_A ,
$$

where the Early voltage $V_A$ grows roughly in proportion to channel length. Short channels lower $V_A$ through channel-length modulation and drain-induced barrier lowering (09-10), so at minimum length a planar transistor's intrinsic gain fell with each generation; Annema et al. measured "a factor 2 in four generations" at fixed bias [2]. FinFETs recovered some of it (§7), but an op-amp needs far more than one device gives (20-02).

The classic remedy is the **cascode** (12-02): stacking a second transistor multiplies the output resistance by about $g_mr_o$, so a cascoded stage with an equally cascoded load (which halves the output resistance seen) gains roughly $A_i^2/2$; with an ideal current-source load it would gain $A_i^2$. But every device in the stack needs its $V_{DS,sat}$, and the signal swing gets what is left:

$$
V_{swing} \approx V_{DD} - n_{stack}V_{DS,sat} .
$$

A telescopic cascode op-amp stacks five devices between the rails (tail, input, two cascodes, load). At 1.8 V that is comfortable; at 0.8 V it leaves almost nothing (Example 20-12.3). Designers fall back on longer channels (more gain, less speed, more area), multistage amplifiers (more gain, but compensation costs bandwidth and power, 20-02), gain boosting (20-02), or architectures that need less gain in the first place.

![Output resistance of a single short-channel transistor and of a cascode against output voltage on a 0.8 V supply: the single device is flat at 74 kilohms above about 0.15 volt of output; the cascode is about 230 kilohms at 0.3 V and jumps to over 5 megohms once the output exceeds about 0.35 V](../../../assets/figures/20-12/stack.svg)

*Figure 3. The cascode's price. It multiplies the output resistance by about $g_mr_o$ (here 75 times), but only above about 0.35 V of output: on a 0.8 V supply that is almost half the range (the lab confirms it in ngspice).*

### 3.4 Matching: the limit that scaling does help

Pelgrom's law (20-11) gives a pair's threshold mismatch as $\sigma(\Delta V_{TH}) = A_{VT}/\sqrt{WL}$. For a target σ the gate area is $A_{VT}^2/\sigma^2$ and its capacitance $C_{mm} = C_{ox}A_{VT}^2/\sigma^2$.

Compare that with the capacitance kT/C noise demands for the same voltage error: $\sigma^2 = kT/C_n$, so $C_n = kT/\sigma^2$. The ratio does not depend on σ:

$$
\frac{C_{mm}}{C_n} = \frac{C_{ox}A_{VT}^2}{kT} .
$$

With $A_{VT}$ = 3.5 mV·µm and $C_{ox}$ = 10 fF/µm² it is about **30** (Example 20-12.4): a circuit whose accuracy is set by mismatch needs some thirty times the capacitance, and so the power, of one whose accuracy is set by thermal noise. Kinget made this comparison and concluded that for MOS circuits "the power constraints due to matching are several orders of magnitude higher than for thermal noise" [1]; the ratio depends on how accuracy is defined, but the direction does not.

Here scaling helps. Empirically $A_{VT}$ falls roughly in proportion to the gate dielectric's thickness, about 1 mV·µm per nanometer (§7) [4], while $C_{ox}$ rises in inverse proportion, so their product $C_{ox}A_{VT}^2$ falls in proportion to the thickness. **Mismatch-limited circuits gain from thinner oxides; noise-limited circuits do not.** Once mismatch is removed by calibration, trimming or chopping, the circuit drops to the kT/C limit, which is why calibrated designs can be far more efficient than raw ones.

### 3.5 Speed: where analog does gain

Scaling raises $f_T$ (20-01): a shorter channel and smaller capacitances mean more bandwidth per unit of current. Circuits limited by speed rather than noise or gain benefit directly: high-speed comparators and SAR logic (20-05, 20-07), sampling switches whose on-resistance falls with length, RF front ends that need $f_T$ far above the carrier, and wide-bandwidth time-interleaved converters. This is why the fastest ADCs and DACs (20-07, 20-09) are built in the newest nodes, even though their precision analog parts are a small fraction of the die.

### 3.6 Digitally assisted analog

If precise analog is expensive and digital logic is cheap, build imprecise analog and correct it digitally. The pattern has many forms in this course:

- **Calibration** of gain and offset errors: pipeline ADC stages (20-07), time-interleaved channel mismatch (20-07), sigma-delta DAC elements (20-08).
- **Redundancy:** a 1.5-bit stage or a SAR with redundant bits tolerates comparator errors that digital logic later removes (20-07).
- **Dynamic element matching:** rotating unit elements turns mismatch into shaped noise (20-09).
- **Time-domain and digital-PLL design:** a TDC and a digital loop filter replace the charge pump and analog filter (20-10).

The calibration must measure the error accurately enough. If an analog stage has a gain error ε and the system needs a total gain error below $\varepsilon_{max}$, the digital estimate of ε must be accurate to $\varepsilon_{max}/\varepsilon$ of itself (Example 20-12.5). The calibration also has to track temperature and supply drift, which is why many designs calibrate in the background, continuously, rather than once at power-up. The digital logic costs power and area too, but it is cheap: Murmann's 2005 comparison put one conversion of a then state-of-the-art 10-bit ADC at the energy of "1nJ/6fJ= 166,666" gate operations in 0.13 µm CMOS [5], and a few thousand gates cost far less than the tens of decibels of extra open-loop gain they replace (about 50 dB in Example 20-12.5).

### 3.7 Economics and partitioning

If analog area shrinks slowly while the wafer cost per unit area rises with each node, an analog block can cost more on a newer node than on an older one. Designers respond by keeping analog circuits small and digital-heavy on the advanced die, and increasingly by moving analog and I/O functions to separate chips in an older node, connected in one package. AMD said so directly when it split its server processors into chiplets: memory interfaces and SerDes "see a very small shrink factor to 7nm and very little performance or power gain from advanced nodes" [11]. The dated evidence is in §9.

## 4. Worked examples

### Example 20-12.1 · One node of constant-field scaling (tier A)

**Setup.** A process is scaled by $S$ = 1.4 at constant field. Find the factors by which a logic gate's delay, switching energy and area change. Then find the factors for the capacitance and power of a thermal-noise-limited analog stage with the same SNR, bandwidth, swing fraction and $g_m/I_D$.

**Solution.**

- Digital: delay $1/S$ = **0.714**; energy $1/S^3$ = **0.364**; area $1/S^2$ = **0.510**.
- Analog: $C \propto 1/V_{DD}^2$ grows by $S^2$ = **1.96**; $P \propto 1/V_{DD}$ grows by $S$ = **1.4**.

**Units check.** All factors are ratios.

**Sanity check.** The gate gets cheaper on every axis; the noise-limited stage needs twice the capacitance and 40% more power. Nothing in the analog result depends on the lithography: only on the supply.

### Example 20-12.2 · The kT/C budget at two supplies (tier B)

**Setup.** A unity-feedback ($\beta$ = 1) sampling buffer must reach SNR = 74 dB (about 12 bits) for a single-ended sine whose peak-to-peak swing is 80% of $V_{DD}$, with a closed-loop bandwidth of 100 MHz, $g_m/I_D$ = 15 V⁻¹ and T = 300 K. Find the sampling capacitance, its rms noise, the current and the power at $V_{DD}$ = 1.8 V and at 0.8 V.

**Solution.** SNR = $10^{7.4}$ = 2.512 × 10⁷ and $kT$ = 4.142 × 10⁻²¹ J.

- 1.8 V: $A$ = 0.72 V, $C = 2kT\cdot\text{SNR}/A^2$ = **0.401** pF with rms noise $\sqrt{kT/C}$ = **102** µV; $g_m = 2\pi fC$ = 0.252 mS, $I$ = **16.8** µA, $P$ = **30.3** µW.
- 0.8 V: $A$ = 0.32 V, $C$ = **2.03** pF, noise **45.1** µV; $g_m$ = 1.28 mS, $I$ = **85.1** µA, $P$ = **68.1** µW.

The lower supply costs **2.25** times the power, exactly $1.8/0.8$.

**Units check.** J/V² = F; F × Hz = S; S/V⁻¹ = A; A × V = W.

**Sanity check.** A logic gate moving from 1.8 V to 0.8 V would have cut its energy to $(0.8/1.8)^2$ = **0.198** of its old value at equal capacitance. The analog buffer went the other way.

### Example 20-12.3 · Intrinsic gain and the stack (tier B)

**Setup.** At minimum length a transistor has $V_A$ = 2.5 V and runs at $g_m/I_D$ = 12 V⁻¹ with $V_{DS,sat}$ ≈ 0.15 V. Find its intrinsic gain, the gain of a cascoded stage ($\approx A_i^2/2$), and the swing a five-device telescopic stack leaves at 1.8 V and at 0.8 V. Compare a two-stage amplifier of simple stages (gain ≈ $(A_i/2)^2$) whose output stage stacks two devices.

**Solution.**

- $A_i$ = 12 × 2.5 = **30**, or **29.5** dB.
- Cascoded stage: $30^2/2$ = **450**, **53.1** dB.
- Telescopic swing: 1.8 − 5 × 0.15 = **1.05** V; 0.8 − 0.75 = **0.05** V, unusable.
- Two simple stages: $(30/2)^2$ = **225**, **47.0** dB, with an output swing of 0.8 − 2 × 0.15 = **0.5** V at 0.8 V.

**Units check.** V⁻¹ × V is dimensionless; the swing is in volts.

**Sanity check.** At 0.8 V the designer trades the telescopic's single-stage simplicity and speed for a two-stage amplifier that needs Miller compensation (20-02): lower bandwidth for the same power, which is the low-voltage tax.

### Example 20-12.4 · Mismatch or noise? (tier B)

**Setup.** A process has $A_{VT}$ = 3.5 mV·µm and $C_{ox}$ = 10 fF/µm². A comparator needs a 0.5 mV error budget. Find the gate capacitance that mismatch demands, the capacitance that kT/C noise demands at 300 K, and their ratio. Then repeat for a hypothetical process with half the oxide thickness (twice $C_{ox}$, half $A_{VT}$).

**Solution.**

- Mismatch: $C_{mm} = C_{ox}A_{VT}^2/\sigma^2 = 10 \times 3.5^2/0.5^2$ fF = **490** fF.
- Noise: $C_n = kT/\sigma^2$ = 4.142 × 10⁻²¹/(0.5 × 10⁻³)² F = **16.6** fF.
- Ratio $C_{ox}A_{VT}^2/kT$ = **29.6**.
- Half the oxide: $C_{ox}A_{VT}^2$ halves, so $C_{mm}$ = **245** fF and the ratio is **14.8**; $C_n$ is unchanged.

**Units check.** fF/µm² × (mV·µm)²/mV² = fF; J/V² = F.

**Sanity check.** Thinner oxide halved the mismatch-limited capacitance (and the power to drive it) but did nothing for the noise-limited one. Calibrating away the offset would let the comparator shrink to the noise limit, thirty times smaller.

### Example 20-12.5 · Replacing gain with calibration (tier B)

**Setup.** A residue amplifier with a nominal gain of 2 uses an op-amp of open-loop gain $A_0$ = 30 (Example 20-12.3) with feedback factor β = 1/2. Its closed-loop gain error is $\varepsilon = 1/(1 + A_0\beta)$. (a) Find ε. (b) What open-loop gain would bring ε below 1/4096 (12-bit accuracy) without calibration? (c) With digital calibration instead, how accurately must the calibration estimate ε?

**Solution.**

- (a) $\varepsilon = 1/(1 + 15)$ = **6.25**%.
- (b) $1 + A_0/2 \ge 4096$ gives $A_0 \ge$ **8190**, or **78.3** dB: more than one cascoded stage gives at this node (53.1 dB), so it needs a second gain stage or gain boosting, with the compensation and power those bring.
- (c) The residual error is ε times the calibration's relative error, so the estimate must be within $(1/4096)/0.0625$ = **0.39**% of ε.

**Units check.** All quantities are ratios.

**Sanity check.** A digital multiplier that scales the backend's code by $1/(1 - \hat\varepsilon)$ replaces about 50 dB of analog gain. The lab's two-step converter applies the same 6.25% error, but to a residue amplified by 16 behind a 4-bit coarse stage, so a residual gain error moves the output only 1/16 as much: it shows 50.1 dB SNDR uncorrected and 73.4 dB corrected, and a 2% estimation error still gives 73.0 dB. Its tolerance to estimation error is correspondingly looser (**6.25**% for one 12-bit LSB) than this gain-2 stage's 0.39%.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 20-12.1a | delay factor | 0.714 | — |
| Ex 20-12.1b | energy factor | 0.364 | — |
| Ex 20-12.1c | area factor | 0.510 | — |
| Ex 20-12.1d | analog capacitance factor | 1.96 | — |
| Ex 20-12.1e | analog power factor | 1.4 | — |
| Ex 20-12.2a | C at 1.8 V | 0.401 | pF |
| Ex 20-12.2b | noise at 1.8 V | 102 | µV |
| Ex 20-12.2c | current at 1.8 V | 16.8 | µA |
| Ex 20-12.2d | power at 1.8 V | 30.3 | µW |
| Ex 20-12.2e | C at 0.8 V | 2.03 | pF |
| Ex 20-12.2f | noise at 0.8 V | 45.1 | µV |
| Ex 20-12.2g | current at 0.8 V | 85.1 | µA |
| Ex 20-12.2h | power at 0.8 V | 68.1 | µW |
| Ex 20-12.2i | power ratio | 2.25 | — |
| Ex 20-12.2j | digital energy ratio | 0.198 | — |
| Ex 20-12.3a | intrinsic gain | 30 | — |
| Ex 20-12.3b | intrinsic gain | 29.5 | dB |
| Ex 20-12.3c | cascoded gain | 450 | — |
| Ex 20-12.3d | cascoded gain | 53.1 | dB |
| Ex 20-12.3e | telescopic swing, 1.8 V | 1.05 | V |
| Ex 20-12.3f | telescopic swing, 0.8 V | 0.05 | V |
| Ex 20-12.3g | two-stage gain | 225 | — |
| Ex 20-12.3h | two-stage gain | 47.0 | dB |
| Ex 20-12.3i | two-stage swing, 0.8 V | 0.5 | V |
| Ex 20-12.4a | mismatch capacitance | 490 | fF |
| Ex 20-12.4b | noise capacitance | 16.6 | fF |
| Ex 20-12.4c | ratio | 29.6 | — |
| Ex 20-12.4d | mismatch capacitance, half oxide | 245 | fF |
| Ex 20-12.4e | ratio, half oxide | 14.8 | — |
| Ex 20-12.5a | gain error | 6.25 | % |
| Ex 20-12.5b | open-loop gain needed | 8190 | — |
| Ex 20-12.5c | open-loop gain needed | 78.3 | dB |
| Ex 20-12.5d | calibration accuracy | 0.39 | % |
| Ex 20-12.5e | SNDR uncorrected | 50.1 | dB |
| Ex 20-12.5f | SNDR corrected | 73.4 | dB |
| Ex 20-12.5g | SNDR, 2% estimate error | 73.0 | dB |
| Txt 20-12.a | cascode resistance ratio | 75 | — |
| Txt 20-12.b | mismatch-to-noise capacitance ratio | 30 | — |
| Txt 20-12.c | supply over high-density threshold, 2024 | 2.4 | — |
| Txt 20-12.d | cost per analog copy, 1.2× shrink | 1.5 | — |
| Txt 20-12.e | cost per analog copy, 1.1× shrink | 1.65 | — |
| Txt 20-12.f | wafer price ratio, 5 nm over 7 nm | 1.82 | — |
| Txt 20-12.g | best Schreier FoM below the thermal line | 2.6 | dB |
| Txt 20-12.h | lab two-step estimate tolerance | 6.25 | % |

## 5. Simulate it

The lab ([labs/20-12-lab](../labs/20-12-lab/README.md)) collects the chapter's scaling models in `scaling.py` and confirms the cascode's headroom cost in ngspice.

**Predict, then run.**

1. Predict how a gate's delay, energy and area and a noise-limited stage's capacitance and power change over three nodes of constant-field scaling, then tabulate them (Part 1).
2. Predict the power of Example 20-12.2's buffer as the supply falls from 3.3 V to 0.6 V, with the swing fraction fixed and then shrinking with the stack's $V_{DS,sat}$, then plot it (Part 2).
3. Predict the output resistance of a single short-channel transistor and of a cascode at 0.6 V and at 0.3 V output, then run `ngspice -b stack.cir` (Part 3).
4. Predict the capacitance ratio of Example 20-12.4 for three processes, then compute it (Part 4).
5. Predict the SNDR of a two-step converter with a 6.25% residue-gain error, uncorrected and corrected with estimates of varying accuracy, then simulate it (Part 5).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Advanced node for the analog block | Speed ($f_T$), digital assistance, integration | Headroom, intrinsic gain, wafer cost per mm² | SoC architect |
| Thick-oxide (I/O) devices for analog | Headroom, gain, lower leakage | Speed, area, extra masks | Analog lead |
| Longer channel length | Intrinsic gain, matching, flicker noise | Speed, area | Analog designer |
| Cascoding | Gain, output resistance | Headroom ($V_{DS,sat}$ per device) | Analog designer |
| Larger capacitors | kT/C noise | Power, area, speed | Analog designer |
| Digital calibration | Relaxed analog gain and matching | Digital power and area, calibration time, verification complexity | Mixed-signal architect |
| Separate analog/I/O chiplet in an older node | Cost, reuse, voltage range | Package cost, die-to-die power and latency | Product and packaging architects |

## 7. Numbers to know

| Quantity | Typical value | Note |
|---|---|---|
| Supply history | 5 V (early 1990s) → 1.8 V (180 nm) → 1.1 V (65 nm) → 0.8 V (7 nm, roadmap) | Annema et al.; ITRS via Stillmaker and Baas [2], [3] |
| Logic $V_{DD}$ roadmap (as of Nov 2026) | 0.70 V now, 0.60 V from 2027; raised to 0.75 V in 2021 for FinFET leakage | IRDS 2024 [3] [R-357] **[Industry estimate]** |
| Threshold at the same node | $V_{t,sat}$ ≈ 0.16 V (high performance) to 0.29 V (high density) | IRDS 2024; $V_{DD}/V_{t}$ ≈ **2.4** [3] |
| Analog and I/O supplies | many I/Os still signal at 1.8 V "despite core VDD reduction"; precision analog uses thick-oxide devices or separate, higher supplies | Loke [6] |
| $A_{VT}$ | ≈ 1 mV·µm per nm of oxide; 3.5 mV·µm at 65 nm; 0.7–1.4 mV·µm in fully depleted FinFET and FD-SOI devices | ITRS 2003, Pelgrom; IEDM 2013 [4] [R-358] |
| Mismatch energy against kT | $C_{ox}A_{VT}^2$ ≈ 30–70 times kT | Example 20-12.4; Pelgrom's slides say 70 [4] **[Contested]** (definition-dependent) |
| FinFET intrinsic gain | "3×" (Loke, Qualcomm; baseline not stated); 3.8 times 28 nm planar (Jeong et al., Samsung, 14 nm RF FinFET) | [6], [7] |
| Analog and I/O area per node | 0.8–0.9×, against 0.5× for logic and SRAM; IRDS assumes 0.9× per node | Loke; IRDS 2024 [3], [6] **[Industry estimate]** |
| TSMC N3 against N5 (2020 claim) | logic up to 1.7×, SRAM 1.2×, analog 1.1× density | press report of TSMC's symposium [9] **[Industry estimate]** |
| ADC energy trend | median Walden FoM down about 575× from 1997–99 to 2024–26; best Schreier FoM 189.2 dB (2025, 0.18 µm), **2.6** dB below the 191.8 dB thermal line | Murmann's survey; our extraction [8] [R-359] |
| Wafer price (estimates) | 28 nm $2,891 → 7 nm $9,346 → 5 nm $16,988 (2020 model) | CSET [10] **[Industry estimate]** |

## 8. Common mistakes

- **Expecting analog area to shrink with the node.** A matching or noise target fixes the capacitance; the lithography does not enter.
- **Assuming lower supply saves analog power.** For a noise-limited circuit at fixed SNR and bandwidth, power rises as $1/V_{DD}$.
- **Quoting intrinsic gain at a long channel and designing at minimum length.** $V_A$ shrinks with $L$, and with it the gain.
- **Forgetting the stack.** Each cascode costs a $V_{DS,sat}$; at sub-1 V supplies, the telescopic topology runs out of swing.
- **Treating calibration as free.** It must measure the error to the required accuracy, track drift, and be verified like any other function.
- **Confusing mismatch-limited and noise-limited design.** Scaling and calibration help the first; only more capacitance, more power or more swing helps the second.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **The supply has stopped falling [Industry estimate: roadmap values].** IRDS puts logic $V_{DD}$ at 0.70 V, after a bump to 0.75 V in 2021 because of "higher than anticipated leakage of FinFET transistors", and sees "no solutions left to reduce the supply voltage" below about 0.6 V [3]. With thresholds of 0.16–0.29 V, a core device has little more than two thresholds of supply. Analog blocks therefore run on thicker-oxide devices or higher separate supplies, and many I/Os still signal at 1.8 V "despite core VDD reduction" [6].
- **FinFETs helped analog, partly [Established].** Fully depleted fins cut drain-induced barrier lowering and random dopant fluctuation: Loke et al. (Qualcomm) list "3× intrinsic gain" and "less RDF mismatch", and Samsung reported 3.8 times the intrinsic gain of 28 nm planar for its 14 nm RF FinFET [6], [7]. The same slides flag "High S/D resistance" as a "big deal" [6]; fins also bring larger parasitic capacitance, stronger layout-dependent effects and device widths quantized in whole fins.
- **Converters improved anyway, by changing architecture [Established].** Murmann's survey of ISSCC and VLSI papers shows the median Walden figure falling about 575× over 27 years (our extraction) [8]. The gains came from SAR, dynamic and digitally assisted designs that use scaling for speed and logic; the best noise-limited results are not in the newest nodes: the best Schreier figure, 189.2 dB (2025), is in 0.18 µm, and in 2022–2026 no published ADC with SNDR ≥ 90 dB used a node at or below 16 nm, while all 51 at ≥ 1 GS/s used 28 nm or below (our extraction) [8].
- **Scaling-friendly analog is an established field [Established].** VCO-based sigma-delta ADCs (Straayer and Perrott, 2008), a "mostly digital" ring-oscillator ADC that "does not contain analog integrators, feedback DACs, comparators, or reference voltages" (Taylor and Galton, 2010), ring amplifiers whose "performance … scales with process technology" (Hershberg et al., 2012), inverter-based switched-capacitor modulators at 0.7 V (Chae and Han, 2009) and Staszewski's digital RF (20-10) all turn analog functions into timing and logic [12].

### Why it matters commercially

Analog and I/O decide how much of a leading-edge die is "wasted" area, and the industry now partitions around that. AMD's chiplet processors put memory interfaces and SerDes on an older node because they "see a very small shrink factor to 7nm and very little performance or power gain from advanced nodes" [11]; its fourth-generation EPYC pairs 5 nm cores with 6 nm I/O dies, explaining that the core process is on "a different innovation path" from the one the analog circuitry needs [11]. AMD estimated its first chiplet server cost about 0.59 of a monolithic design despite using about 10% more silicon [11]. The economics are simple: CSET's model has a 5 nm wafer at **1.82** times the price of a 7 nm one [10]; if an analog block shrank only 1.1–1.2× across such a step, each copy would cost about **1.5–1.65** times more (our arithmetic). For the learner's coverage: **AI datacenter** accelerators are surrounded by SerDes and HBM PHYs that shrink slowly and increasingly sit on I/O dies; **wearables and IoT** MCUs stay on mature nodes partly because their analog (ADCs, regulators, radios, sensors) would not benefit; **automotive** parts need high-voltage and precision analog that advanced nodes do not offer. In diligence, an analog IP company's portability across nodes, and its share of the die, are value drivers.

### Questions for engineering leaders

1. **"What fraction of the die is analog and I/O, and what shrink did those blocks get on the new node?"** Strong: block-by-block areas on both nodes. Evasive: the logic density figure.
2. **"Is this block noise-limited, mismatch-limited or speed-limited?"** Strong: a clear answer with the specification that sets power. Evasive: "it will scale with the process."
3. **"What is calibrated, how often, and what happens to the specification before calibration converges?"** Strong: background calibration with tracking data over temperature. Evasive: foreground calibration at room temperature only.
4. **"Which devices does the analog use: core, thick-oxide or a separate supply?"** Strong: the supply plan and its cost. Evasive: "standard cells and core devices only," for a precision block.
5. **"Why is this function on this die rather than a cheaper one?"** Strong: a cost, power and latency comparison with a chiplet or companion-chip option. Evasive: "integration is always better."

### Marketing vs Reality

- **"The new node is 1.7× denser."** For logic. TSMC's own 2020 figures for N3 against N5 were 1.2× for SRAM and 1.1× for analog, and its "chip density" for N3E, which assumes 50% logic, 30% SRAM and 20% analog, was 1.3× [9]. IRDS assumes analog and I/O area shrinks only to 0.9× per node, against a 1.42× step in logic gate density (2024 to 2025) [3].
- **"Moving our ADC to 3 nm will cut its power."** Only for its speed-limited and digital parts. Noise-limited precision does not move with the node (§3.2), which is why the record noise-limited converter is in 0.18 µm (189.2 dB, 2025) [8]. Ask what the converter's SNDR is and where its energy goes.
- **"Record figure of merit."** Murmann's survey takes power "as specified by the authors. Sometimes this number includes power for clocks, references, etc.; sometimes it doesn't" [8]. Check references, buffers, clocks and decimation.
- **"All-digital."** An all-digital PLL still has an analog oscillator whose "imperfections … are compensated through digital means" [12], and a mostly digital ADC still has ring oscillators and calibration. The value is portability and area, not freedom from physics.
- **"Cost per transistor keeps falling."** [Contested.] CSET notes that "some analysts claim that decreases have stopped past the 28 nm node … while others disagree" [10]. For a block that does not shrink, the question is settled: it costs more per copy on the newer, pricier wafer.
- **Sanity check.** Ask how much of the claimed gain is digital, how much is architecture, and how much is the analog itself; only the first two follow the roadmap.

## 10. Concept check

**Q1.** Why does a logic gate tolerate the smaller supply of a new node while an analog sampler does not?

<details><summary>Answer</summary>

The gate only has to land on the correct side of its switching threshold; noise far smaller than the supply does not matter. The sampler must hold its signal a fixed ratio above the kT/C noise, which does not shrink with the node, so a smaller swing needs a larger capacitor.

</details>

**Q2.** At fixed SNR and bandwidth, how does a class-A noise-limited stage's power depend on the supply, and why?

<details><summary>Answer</summary>

As $1/V_{DD}$. The capacitance must grow as $1/V_{DD}^2$ to keep the SNR with a smaller swing, the current grows with the capacitance at fixed bandwidth and $g_m/I_D$, and power is supply times current.

</details>

**Q3.** What two things does a cascode cost in a low-voltage process?

<details><summary>Answer</summary>

Headroom: each stacked device needs its own $V_{DS,sat}$, which reduces the signal swing (and the swing enters the kT/C budget squared). It also adds a node and its capacitance, which can lower bandwidth.

</details>

**Q4.** Why do mismatch-limited circuits benefit from thinner gate oxides while noise-limited ones do not?

<details><summary>Answer</summary>

The capacitance that matching requires is $C_{ox}A_{VT}^2/\sigma^2$, and $C_{ox}A_{VT}^2$ falls roughly in proportion to oxide thickness. The capacitance that noise requires is $kT/\sigma^2$, which contains no process parameter.

</details>

**Q5.** A calibration engine removes a 5% gain error. What does it need to achieve for 14-bit accuracy?

<details><summary>Answer</summary>

It must estimate the error to within $2^{-14}/0.05$, about 0.12% of the error itself, and keep tracking it over temperature and supply.

</details>

**Q6.** Name two kinds of analog circuit that do benefit from scaling.

<details><summary>Answer</summary>

Speed-limited ones, such as high-speed comparators, sampling switches and RF circuits that need a high $f_T$; and circuits that are mostly switches and logic, such as SAR ADCs and digital PLLs, whose precision is set by capacitor matching or by digital resolution rather than by amplifier gain.

</details>

Problems: [20-12 problem set](../problems/20-12-problems.md) · Worked solutions: [20-12 solutions](../solutions/20-12-solutions.md)

## 11. Key terms

[Constant-field scaling](../../../reference/glossary.md#constant-field-scaling) · [Headroom](../../../reference/glossary.md#headroom) · [kT/C noise](../../../reference/glossary.md#ktc-noise) · [Intrinsic gain](../../../reference/glossary.md#intrinsic-gain) · [Cascode](../../../reference/glossary.md#cascode) · [Pelgrom's law](../../../reference/glossary.md#pelgroms-law) · [Digitally assisted analog](../../../reference/glossary.md#digitally-assisted-analog) · [Background calibration](../../../reference/glossary.md#background-calibration) · [Chiplet](../../../reference/glossary.md#chiplet)

## 12. Connections

- **Previous:** [20-11](20-11-layout-matching-pvt.md) (matching and the speed–accuracy–power limit).
- **Builds on:** [09-11](../../09-semiconductor-devices/chapters/09-11-cmos-and-scaling.md) (scaling), [20-01](20-01-analog-design-fundamentals-gm-id.md) (intrinsic gain), [20-05](20-05-comparators-and-sample-and-hold.md) and [20-06](20-06-data-converter-fundamentals.md) (kT/C and the converter thermal limit).
- **Applies to:** the architecture choices of [20-07](20-07-nyquist-adcs.md) (SAR and calibrated pipelines), [20-09](20-09-dacs.md) (dynamic element matching) and [20-10](20-10-plls-and-jitter.md) (digital PLLs).
- **Next:** Course 21 takes the same devices to radio frequencies, where scaling's speed gains matter most.

## 13. Further study

- B. Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed., McGraw-Hill, 2017: the chapter on nanometer design studies.
- P. R. Kinget, "Device mismatch and tradeoffs in the design of analog circuits," *IEEE J. Solid-State Circuits*, 2005.
- B. Murmann, "Digitally assisted analog circuits," *IEEE Micro*, 2006, and his public ADC performance survey (20-06).

## 14. Sources

1. P. R. Kinget, "Device mismatch and tradeoffs in the design of analog circuits," *IEEE J. Solid-State Circuits*, vol. 40, no. 6, pp. 1212–1224, June 2005, DOI 10.1109/JSSC.2005.848021 [R-353].
2. Annema, Nauta, van Langevelde and Tuinhout, "Analog circuits in ultra-deep-submicron CMOS," *IEEE J. Solid-State Circuits*, vol. 40, no. 1, pp. 132–143, Jan. 2005, DOI 10.1109/JSSC.2004.837247 [R-357].
3. IEEE IRDS, More Moore tables (2020–2024 editions) and 2024 Executive Summary; A. Stillmaker and B. Baas, "Scaling equations for the accurate prediction of CMOS device performance from 180 nm to 7 nm," *Integration*, vol. 58, pp. 74–81, 2017, DOI 10.1016/j.vlsi.2017.02.002 [R-357].
4. ITRS 2003, "RF and AMS Technologies for Wireless Communications" (Tables 53a/b); M. Pelgrom, TWEPP-13 slides, Sep. 2013; Paul et al., IEDM 2013, DOI 10.1109/IEDM.2013.6724625 [R-354], [R-358].
5. B. Murmann, "Digitally assisted analog circuits," Hot Chips 17 talk, Aug. 2005, DOI 10.1109/HOTCHIPS.2005.7476593 (slides) [R-359].
6. Loke et al. (Qualcomm), "Analog/mixed-signal design challenges in 7-nm CMOS and beyond," CICC 2018, DOI 10.1109/CICC.2018.8357060, and CERN talk slides, Sep. 2017 [R-358].
7. Jeong et al. (Samsung), VLSI Technology Symposium 2017, DOI 10.23919/VLSIT.2017.7998155; V. Subramanian et al., *IEEE Trans. Electron Devices*, vol. 53, no. 12, pp. 3071–3079, 2006, DOI 10.1109/TED.2006.885649 [R-322], [R-358].
8. B. Murmann, "ADC Performance Survey 1997–2026," rev. 2026-08-01, and "Digitally assisted analog circuits," *IEEE Micro*, vol. 26, no. 2, pp. 38–47, 2006, DOI 10.1109/MM.2006.33; CICC 2008, DOI 10.1109/CICC.2008.4672032 [R-336], [R-359].
9. A. Shilov, Tom's Hardware, reports of the TSMC Technology Symposia, 24 Aug. 2020 and 16 June 2022 [R-360].
10. S. M. Khan and A. Mann, *AI Chips: What They Are and Why They Matter*, CSET, April 2020 (Table 9, wafer prices) [R-360].
11. S. Naffziger et al., "AMD chiplet architecture for high-performance server and desktop products," ISSCC 2020, pp. 44–45, DOI 10.1109/ISSCC19947.2020.9063103; Naffziger et al., ISCA 2021, DOI 10.1109/ISCA52012.2021.00014 (cost figures as reported by The Next Platform); AMD, "4th Gen AMD EPYC Processor Architecture" white paper, May 2024 [R-360].
12. M. Z. Straayer and M. H. Perrott, *IEEE JSSC*, vol. 43, no. 4, pp. 805–814, 2008, DOI 10.1109/JSSC.2008.917500; G. Taylor and I. Galton, *IEEE JSSC*, vol. 45, no. 12, pp. 2634–2646, 2010, DOI 10.1109/JSSC.2010.2073193; B. Hershberg et al., *IEEE JSSC*, vol. 47, no. 12, pp. 2928–2942, 2012, DOI 10.1109/JSSC.2012.2217865; Y. Chae and G. Han, *IEEE JSSC*, vol. 44, no. 2, pp. 458–472, 2009, DOI 10.1109/JSSC.2008.2010973; R. B. Staszewski et al., *IEEE TCAS-II*, vol. 50, no. 11, pp. 815–828, 2003, DOI 10.1109/TCSII.2003.819128 [R-359].
