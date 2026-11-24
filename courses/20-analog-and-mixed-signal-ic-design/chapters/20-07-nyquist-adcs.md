<!-- status: verified -->
# 20-07 · Nyquist ADCs: Flash, SAR and Pipeline

| | |
|---|---|
| **Course** | [20 · Analog and Mixed-Signal IC Design](../README.md) |
| **University equivalent** | The Nyquist-rate converter material of a graduate data-converter course: flash, successive-approximation and pipelined ADCs, redundancy and digital correction, time interleaving and calibration (Pelgrom, *Analog-to-Digital Conversion*, 4th ed.; Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed., the data-converter chapters) |
| **Prerequisites** | [20-05](20-05-comparators-and-sample-and-hold.md) (sampling, comparators), [20-06](20-06-data-converter-fundamentals.md) (DNL, INL, SNR, figures of merit), [20-02](20-02-two-stage-op-amp-design.md) (op-amp gain and settling), [08-09](../../08-digital-logic-design/chapters/08-09-arithmetic-circuits.md) (binary arithmetic) |
| **Estimated study hours** | 10 |
| **Last verified** | 2026-11-24 |

**Learning objectives.** After this chapter you can:

1. Explain how flash, SAR and pipeline ADCs trade comparators, cycles and amplifiers against resolution and speed.
2. Derive the charge-redistribution SAR's operation and compute its switching energy for conventional and monotonic switching.
3. Explain redundancy in SAR and pipeline converters and compute the decision errors it tolerates.
4. Derive a 1.5-bit pipeline stage's residue, its comparator-offset tolerance and the op-amp gain it needs, and refer stage noise to the input.
5. Compute the spurs that offset, gain and timing-skew mismatch produce in a time-interleaved ADC, and the matching each spur budget requires.
6. Choose an architecture for a speed and resolution target and justify it with published figures of merit.

## 1. Big picture

20-05 built the sampler and comparator and 20-06 defined the metrics. This chapter assembles them into converters. A Nyquist-rate ADC produces one output per input sample, with an input bandwidth up to half the sample rate. Three architectures dominate, and they differ in how they spend comparators, clock cycles and amplifiers:

- **Flash** compares the input against all $2^N - 1$ thresholds at once: one clock cycle, but exponentially many comparators. It is fast and simple and practical only to about 6 bits.
- **SAR** (successive approximation) makes one comparison per bit with a single comparator and a capacitor DAC: $N$ cycles, almost no static power and no amplifier. It dominates below about 100 MS/s and, interleaved, at the highest speeds.
- **Pipeline** resolves a few bits per stage and passes an amplified residue to the next stage, so many samples are in flight at once: high throughput at medium-to-high resolution, at the cost of precise amplifiers.
- **Time interleaving** runs $M$ copies in rotation to multiply the rate by $M$, at the price of mismatch spurs that must be calibrated.

Every modern design mixes these ideas: pipelined-SAR hybrids, SARs with flash front ends, interleaved arrays of SARs. Knowing the three building blocks and their cost laws is what lets you read an ADC paper or a vendor's architecture slide.

## 2. Intuition first

```text
 Flash (one step)            SAR (N steps)                Pipeline (one stage per step, overlapped)
 v ─┬─► comp T1 ─┐           v ─► S/H ─┐                  v ─► [S/H ─ ADC ─ DAC ─ ×2] ─► [stage 2] ─► ... ─► backend
    ├─► comp T2 ─┤ encoder           comp ◄── DAC              │ bits                │ bits
    ├─►   ...    ├─► code             ▲          ▲              └──────────────► digital correction ─► code
    └─► comp T2^N-1                SAR logic ──┘
```

*Figure 1. The three Nyquist architectures. Flash uses $2^N - 1$ comparators in parallel; SAR uses one comparator $N$ times with a DAC; a pipeline passes an amplified residue from stage to stage.*

**A guessing-game analogy, and its limits.** To find a number between 0 and 1023, you can ask 1023 people at once "is it above k?" (flash), ask one person ten binary-search questions in turn (SAR), or pass the problem down an assembly line in which each worker settles a couple of bits and hands the remainder, magnified, to the next (pipeline: while worker 2 works on number 1, worker 1 already starts on number 2). Interleaving is hiring several identical assembly lines and feeding them numbers in turn. The analogy breaks where physics enters: the "remainder" in a pipeline is an analog voltage that must be amplified precisely, the SAR's "questions" are answered by a capacitor DAC that consumes energy and must settle, and interleaved lines are never quite identical.

## 3. Theory

> **Conventions.** $N$ bits; reference $V_{REF}$; for single-ended examples the input range is $[0, V_{REF})$, for pipeline stages $[-V_{REF}, V_{REF}]$. Energies are in units of $C_uV_{REF}^2$, with $C_u$ the unit capacitor. "Differential" energies count both arrays.

### 3.1 Flash ADCs

A flash ADC compares the input with $2^N - 1$ reference levels from a resistor ladder (20-06, Example 20-06.2) at once. The comparator outputs form a **thermometer code**: all ones below the input, all zeros above. An encoder converts it to binary.

- **Cost grows as $2^N$.** Each extra bit doubles the comparators, their power and their input capacitance, and the offset requirement tightens: a comparator offset is a transition error (20-06), and keeping all $2^N - 1$ offsets within half an LSB with high yield needs σ ≈ LSB/8 (Problem 20-05.11). By Pelgrom's law, that area grows fourfold per bit on top of the doubling count (Example 20-07.1).
- **Bubbles.** Noise or metastability can produce a thermometer code with an isolated zero below a one (a "bubble"). An encoder that looks for the first 1→0 transition then errs by many codes; a **ones-counting** (Wallace-tree) encoder, whose output is the number of comparators that fired, errs by at most one code.
- **Where it is used.** Flash survives at low resolution and the highest speeds: as the coarse quantizer inside pipelines and SARs, in interleaved arrays, and in serial-link receivers. Murmann's short course describes flash as "typically" used for 6 bits or fewer [3].

### 3.2 The charge-redistribution SAR

The SAR performs a binary search with one comparator and a capacitive DAC that doubles as the sampling capacitor (McCreary and Gray, 1975 [1]). In the single-ended version, bit $i$ has capacitor $2^iC_u$, plus one dummy $C_u$, so the total is $C_{tot} = 2^NC_u$.

1. **Sample.** The bottom plates track $v_{in}$ while the top plate is held at ground. The top plate stores charge $Q = -C_{tot}v_{in}$.
2. **Hold.** The top plate is released and all bottom plates are switched to ground; charge conservation puts the top plate at $v_x = -v_{in}$.
3. **Search.** For each bit from the MSB down, the trial bit's bottom plate is switched to $V_{REF}$ (keeping the bits already decided). Charge conservation on the top plate gives

$$
v_x = -v_{in} + V_{REF}\sum_i b_i\frac{C_i}{C_{tot}} = -v_{in} + V_{REF}\frac{\text{code}}{2^N} .
$$

   The comparator checks the sign of $v_x$: if $v_x > 0$ the trial code is too large and the bit is cleared; otherwise it is kept.

After $N$ steps the code is the largest one with $V_{REF}\,\text{code}/2^N \le v_{in}$ (Example 20-07.2). The comparator always compares with zero, so its offset shifts every transition equally (20-05) and its input common mode is that of the top plate.

**Switching energy.** The reference supplies charge to every bottom plate it is connected to whenever the top plate moves. Bookkeeping this charge for each step and averaging over all codes gives, for the conventional trial-and-revert sequence with a differential pair of arrays,

$$
E_{conv} = \sum_{i=1}^{N}2^{N+1-2i}\left(2^i - 1\right)C_uV_{REF}^2 ,
$$

**1363.3** $C_uV_{REF}^2$ for 10 bits. A failed trial is expensive: charging the MSB and then discharging it wastes energy. **Monotonic switching** (Liu et al., 2010 [2]) samples the input on the top plates of both arrays, makes the first comparison with no switching at all, and then only ever switches one capacitor per step, on one side, from $V_{REF}$ to ground. Its average is $\sum_{i=1}^{N-1}2^{N-2-i}C_uV_{REF}^2$, **255.5** for 10 bits, an 81% reduction, with half the total capacitance; the price is a common-mode voltage that drifts during conversion, which the comparator must tolerate [2]. The lab computes both by explicit charge bookkeeping for every code (Example 20-07.3).

![Switching energy drawn from the reference for each of the 1024 output codes of a 10-bit differential SAR: the conventional curve falls from about 1705 at code 0 to about 683 at the top code, while the monotonic curve stays between about 171 and 298, peaking at mid-scale](../../../assets/figures/20-07/sar_energy.svg)

*Figure 2. Switching energy per conversion for every code of a 10-bit differential SAR, from the lab's charge bookkeeping. Conventional switching costs most at code 0, where every trial fails and each capacitor is charged and then discharged (1704.7 down to 682.7 $C_uV_{REF}^2$); monotonic switching never charges a capacitor it may have to discharge and stays between 170.7 and 298.2. The differential conventional curve assumes two single-ended arrays switching identically; only its average, 1363.3, is free of that assumption.*

**Speed.** A synchronous SAR needs at least $N$ comparator-and-DAC cycles plus sampling per conversion. Each DAC step must settle before its comparison. The largest step is the MSB's, half the full scale, and its remaining error must be below half an LSB by the last comparison; requiring that within one bit period gives the conservative bound $\tau_{DAC} \le T_{bit}/\ln 2^{N+1}$. Asynchronous SARs (Chen and Brodersen, 2006 [4]) start each comparison as soon as the previous one resolves, so fast decisions lend time to slow ones (20-05 §3.9).

### 3.3 Redundancy

A binary search cannot recover from a wrong decision: if the MSB is decided wrongly because the DAC had not settled, the remaining bits can only reach within one LSB of the wrong half. **Redundancy** spends extra steps so that later steps can correct earlier ones. Give the bits weights $w_1 > w_2 > \cdots$ (in LSB) summing to the full scale. Decision $k$ can be wrong by up to

$$
m_k = \sum_{j>k}w_j - w_k + 1
$$

LSB and still be corrected, because the remaining weights can reach further than the current one. Binary weights give $m_k = 0$ everywhere. Making some weights smaller than binary (a **sub-binary radix**) and adding steps buys margin where it is needed, usually in the early decisions, whose DAC steps are largest and settle slowest. The lab's 11-step design with weights 480, 256, 128, 64, 32, 32, 16, 8, 4, 2, 1 tolerates a first-decision error of 64 LSB (Example 20-07.4).

### 3.4 Pipeline ADCs and the 1.5-bit stage

A pipeline stage samples its input, quantizes it coarsely, subtracts the quantized value with a DAC and amplifies the remainder (the **residue**) for the next stage. With a sample-and-hold in every stage, stage 1 can start on a new sample while stage 2 works on the previous one: throughput is one sample per clock, latency is a few clocks.

**The 1.5-bit stage.** A stage with two comparators, at $\pm V_{REF}/4$, decides $D \in \{-1, 0, +1\}$ and produces

$$
v_{res} = 2v_{in} - D\,V_{REF} .
$$

For $v_{in}$ in $[-V_{REF}, V_{REF}]$ the residue stays in $[-V_{REF}/2, V_{REF}/2]$ if the comparators are ideal. A comparator offset up to $V_{REF}/4$ only moves the decision boundary, so the residue may reach $\pm V_{REF}$ but never leaves the next stage's range: the error is corrected digitally when the stage outputs are added with weights 2:1. This is the same redundancy as §3.3; with ±$V_{REF}/4$ thresholds it was described by Lewis et al. (1992) [5], and it is why pipeline comparators can be small and fast (Example 20-07.5).

**The residue amplifier sets the accuracy.** A flip-around **MDAC** (multiplying DAC) samples $v_{in}$ on $C_s$ and $C_f$; in the hold phase $C_f$ closes the op-amp's feedback and $C_s$ is switched to $DV_{REF}$. Charge conservation at the summing node, with op-amp gain $A$ and parasitic $C_p$ there, gives

$$
v_{res} = \frac{(C_s + C_f)v_{in} - C_sDV_{REF}}{C_f + (C_s + C_f + C_p)/A} = \frac{2v_{in} - DV_{REF}}{1 + 1/(A\beta)}, \qquad \beta = \frac{C_f}{C_s + C_f + C_p}
$$

for $C_s = C_f$. The gain error $1/(A\beta)$ must keep the residue's error below the remaining stages' LSB: for an $N$-bit converter whose first stage resolves one effective bit, $1/(A\beta) < 2^{-(N-1)}$, so $A > 2^{N-1}/\beta$. A 12-bit pipeline with β = 0.45 needs more than 73 dB of op-amp gain (Example 20-07.5). Unlike comparator offset, gain error is *not* corrected by redundancy; it causes DNL errors and missing codes at the stage's decision points, which calibration must remove (lab Part 3).

**The residue amplifier sets the speed too.** In the hold phase the MDAC is a feedback loop with factor β. A single-pole op-amp with transconductance $g_m$ driving the capacitance at its output,

$$
C_{L,eff} = C_{load} + \frac{C_f(C_s + C_p)}{C_s + C_f + C_p} ,
$$

(the next stage's sampling capacitor plus the feedback capacitor in series with the summing node's capacitance) has unity-gain frequency $\omega_t = g_m/C_{L,eff}$, and the closed loop settles with time constant $\tau = 1/(\beta\omega_t)$. Settling the residue to half an LSB of an $N$-bit converter within the hold time $T_h$ takes $(N + 1)\ln 2$ time constants, so

$$
\omega_t \ge \frac{(N + 1)\ln 2}{\beta T_h} .
$$

For 12 bits at 200 MS/s ($T_h$ = 2.5 ns) with β = 0.45, $f_t \ge 9.01/(2\pi \times 0.45 \times 2.5\ \text{ns})$ = **1.27** GHz, before any slewing (Example 20-07.8). β enters twice: a small β demands both more DC gain and more bandwidth, so every femtofarad of $C_p$ costs power; and capacitors made larger for lower kT/C raise $C_{L,eff}$ in proportion, so each 3 dB of SNR doubles the amplifier's current. This bandwidth, not the DC gain, usually sets a pipeline's power.

![Left: residue of a 1.5-bit stage against input, three line segments of slope 2 within plus or minus 0.5 volt for ideal thresholds; with the upper threshold moved up by 0.2 volt the middle segment extends to 0.9 volt, still inside the next stage's range of plus or minus 1 volt. Right: DNL of the 10-bit pipeline against code, zero except at codes near 384 and 640, where a stage-1 gain of 0.99 gives DNL of minus 1 (missing codes) and a gain of 1.01 gives plus 1 (double-width codes)](../../../assets/figures/20-07/pipeline.svg)

*Figure 3. What redundancy forgives and what it does not. (a) A comparator offset of 0.2 V moves a decision point; the residue grows but stays inside the next stage's range, and the digital addition corrects it. (b) An interstage gain error is not corrected: at stage 1's two decision points a gain of 0.99 leaves missing codes (DNL −1) and 1.01 produces double-width codes (DNL +0.99). A gain above 1 also makes the transfer non-monotonic: just past each decision point the output steps back by about 1% of the 256-code backend range (two to three codes), which a code-count DNL reports only as wide codes. The two codes at each end are excluded; there the error is a range compression, not DNL.*

**Noise and stage scaling.** Noise added in stage $k$ is divided by the gain before it, $2^{k-1}$, when referred to the input. Stage 2 can therefore use a capacitor half as large as stage 1 (its kT/C noise doubles, but is divided by 4), stage 3 a quarter, and so on; the referred noise is then $kT/C_1(1 + \tfrac12 + \tfrac14 + \cdots) \to 2kT/C_1$, at a fraction of the power of equal stages (Example 20-07.6).

### 3.5 Time interleaving

$M$ identical ADCs, each at $f_s/M$, sample in rotation to make one converter at $f_s$. Any difference between channels repeats with period $M$ samples and appears as spurs. For two channels and a sine of amplitude $A$ at $f_{in}$:

- **Offset mismatch** $\Delta o$ adds a square wave of amplitude $\Delta o/2$ at $f_s/2$: a tone of power $(\Delta o/2)^2$, or $\Delta o^2/(2A^2)$ relative to the signal, independent of the input frequency.
- **Gain mismatch** α (relative) multiplies the signal by a square wave, giving an image at $f_s/2 - f_{in}$ with power ratio $(\alpha/2)^2$, an SNR of $4/\alpha^2$ (Razavi, 2013 [6]).
- **Timing skew** Δt between the channels' sampling instants also gives an image at $f_s/2 - f_{in}$, with power ratio $(\pi f_{in}\Delta t)^2$, an SNR of $1/(\pi^2f_{in}^2\Delta t^2)$ [6]. Like jitter (20-05), skew's cost grows with input frequency, but it is deterministic and can be calibrated.

With $M$ channels the spurs move to multiples of $f_s/M$ and around them. A data sheet for a 4× interleaved converter lists "interleaving spurs" at $f_s/2 - f_{in}$ and $f_s/4 \pm f_{in}$ [9]. For a 60 dBc target at 500 MHz, skew must stay below 0.64 ps (Example 20-07.7), which is why interleaved converters calibrate timing in the background.

![Three spectra of a two-channel interleaved ADC at 1 gigasample per second with a 0.8 volt input at 244.38 megahertz: with 1 millivolt offset mismatch a spur at minus 61.1 dBc at 500 megahertz; with 1 percent gain mismatch an image at minus 46.1 dBc at 255.6 megahertz; with 1 picosecond skew an image at minus 62.3 dBc at 255.6 megahertz](../../../assets/figures/20-07/ti_spurs.svg)

*Figure 4. Example 20-07.7 simulated. Offset mismatch gives a fixed tone at $f_s/2$; gain and timing mismatch give an image at $f_s/2 - f_{in}$, whose skew part grows with $f_{in}$.*

### 3.6 Calibration and the modern landscape

Redundancy absorbs comparator errors, but gain errors, capacitor mismatch, interleaving mismatch and amplifier nonlinearity must be measured and corrected. **Foreground** calibration measures errors during a dedicated phase (at power-up); **background** calibration does it while converting, by injecting known signals, by correlation, or by swapping in a spare channel. Digital correction let designers replace precise closed-loop amplifiers with simpler ones and fix their errors digitally (Murmann and Boser, 2003 [7]); ring amplifiers made efficient closed-loop residue amplification possible in nanometer processes (Hershberg et al., 2012 [8]). As a result, the boundaries between architectures have blurred: the most efficient designs today are SARs below about 10 MS/s, pipelined-SAR hybrids up to about 1 GS/s, and interleaved arrays of SARs or pipelines above that (§9).

## 4. Worked examples

### Example 20-07.1 · The cost of flash resolution (tier A)

**Setup.** (a) How many comparators do 6-bit and 8-bit flash ADCs need? (b) For a 1.0 V full scale and σ(offset) = LSB/8 with $A_{VT}$ = 3.5 mV·µm, find the input-pair area per comparator at 8 bits and the total input capacitance ($\tfrac23C_{ox}WL$ per comparator, T130's 8.6 fF/µm²) at 6 and 8 bits.

**Solution.**

(a) $2^N - 1$: **63** and **255**.

(b) At 8 bits, LSB = **3.906** mV and σ = **0.488** mV, so $WL = (A_{VT}/\sigma)^2$ = **51.4** µm². The input capacitance is 255 × ⅔ × 8.6 × 51.4 fF = **75.1** pF. At 6 bits ($WL$ = 3.21 µm²) it is **1.16** pF.

**Sanity check.** Two more bits multiply the count by about 4 and each device's area by 16: about 65 times the input capacitance. No driver can charge 75 pF at gigahertz rates, which is why flash stops at about 6 bits unless offsets are calibrated or averaged.

### Example 20-07.2 · A SAR conversion, step by step (tier A)

**Setup.** A 4-bit charge-redistribution SAR with $V_{REF}$ = 1 V converts $v_{in}$ = 0.6 V. Trace $v_x$ and the decisions.

**Solution.** $v_x = -0.6 + \text{code}/16$:

| Step | Trial code | $v_x$ (V) | Decision |
|---|---|---|---|
| 1 | 1000 | **−0.1** | keep |
| 2 | 1100 | **+0.15** | clear |
| 3 | 1010 | **+0.025** | clear |
| 4 | 1001 | **−0.0375** | keep |

The result is 1001 = **9**: 9/16 = 0.5625 ≤ 0.6 < 10/16 = 0.625.

**Sanity check.** Each step halves the remaining interval, and $v_x$ ends within one LSB (62.5 mV) below zero: −37.5 mV.

### Example 20-07.3 · Switching energy (tier B)

**Setup.** For a 10-bit differential SAR, find the average switching energy of conventional and monotonic switching and the saving. With $C_u$ = 1 fF and $V_{REF}$ = 1 V, find the energy per conversion and the power at 100 MS/s. Repeat the conventional figure for 12 bits.

**Solution.** From §3.2: conventional **1363.3** and monotonic **255.5** $C_uV_{REF}^2$, a saving of **81.3**%. With 1 fF and 1 V: **1.363** pJ and **0.256** pJ per conversion, **136** µW and **25.6** µW at 100 MS/s. At 12 bits the conventional figure is **5459.3** $C_uV_{REF}^2$.

**Sanity check.** The energy grows about fourfold per bit (5459/1363 ≈ 4.0), because the array doubles in size and the reference charge per step doubles. Whether the DAC's switching power matters depends on the unit capacitor: with this example's 1 fF and 1 V, a 12-bit conventional array draws **0.546** mW at 100 MS/s, about as much as the 0.59 mW comparator of 20-05, while the 20-05 design's smaller unit (0.651 pF/4096 ≈ 0.16 fF) would draw about a sixth of that at the same reference. The saving matters most when the array is large or the converter is otherwise frugal.

### Example 20-07.4 · Redundancy against DAC settling (tier B)

**Setup.** A 10-bit SAR's first DAC step has not fully settled: the first comparison sees a DAC value 3% of $V_{REF}$ too high. Compare a binary SAR (weights 512…1) with an 11-step redundant SAR (weights 480, 256, 128, 64, 32, 32, 16, 8, 4, 2, 1). Find the redundancy margins of the first five decisions and the worst-case output error of each converter (lab model).

**Solution.** The margins $m_k$ are **64**, **32**, **32**, **32** and **32** LSB; binary weights have none. A 3% error is **31** LSB. The binary SAR's worst-case error is **31** LSB: every input in that band gets the wrong MSB and cannot recover. The redundant SAR's worst case is **0** LSB: the error is within the 64 LSB margin, and later steps correct it.

**Sanity check.** Redundancy costs one extra cycle here and buys a large settling tolerance for the MSB, the step with the largest DAC transient. The same weights sum to 1023, so the full scale is unchanged.

### Example 20-07.5 · A 1.5-bit pipeline stage (tier B)

**Setup.** (a) An MDAC with $C_s = C_f$ = 0.5 pF and $C_p$ = 0.1 pF processes $v_{in}$ = 0.3 V with $DV_{REF}$ = 0.5 V. Find the ideal residue, and the residue and gain error with op-amp gains of 1000 and 100. (b) What op-amp gain do 10-bit and 12-bit pipelines need with this β? (c) In the lab's 10-bit pipeline (eight 1.5-bit stages and a 2-bit backend), what happens with comparator offsets up to ±0.2 $V_{REF}$, an offset of 0.3 $V_{REF}$, and first-stage gain errors of 0.2% and 1%?

**Solution.**

(a) Ideal: 2 × 0.3 − 0.5 = **0.1** V. β = 0.5/1.1, so $1/(A\beta)$ = **0.22**% at $A$ = 1000 and **2.2**% at 100; the residues are **0.099780** V and **0.097847** V. ngspice confirms both (`mdac.cir`).

(b) $A > 2^{N-1}/\beta$: **1126** (**61.0** dB) for 10 bits and **4506** (**73.1** dB) for 12 bits.

(c) Offsets uniform within ±0.2 $V_{REF}$ (below the $V_{REF}/4$ tolerance) change **no** output code. An offset of 0.3 $V_{REF}$ in one comparator produces errors of up to **26** codes. A first-stage gain error of 0.2% gives a worst DNL of **−0.255** LSB; 1% gives **4** missing codes, two at each of stage 1's decision points: the residue reaches only ±0.495 V instead of ±0.5 V on each side of the threshold, a gap of 256 × 0.01 = 2.56 LSB that no input fills. (The range also shrinks by 1%, so the two codes at each end are never reached; Part 3 of the lab counts these separately.)

**Sanity check.** Redundancy forgives comparator offsets completely, up to its margin, and not at all beyond it. Gain error is never forgiven: it is the residue amplifier's precision, not the comparators', that limits a pipeline.

### Example 20-07.6 · Pipeline noise and stage scaling (tier B)

**Setup.** Three stages of gain 2 sample on 1, 0.5 and 0.25 pF. (a) Find the input-referred kT/C noise as a multiple of $kT/C_1$ and in µV. (b) Repeat with three 1 pF stages. (c) For the 12-bit, 1.6 V design of 20-05, with all stages scaled by half and the total kT/C noise equal to the quantization noise, what first-stage capacitance per side is needed?

**Solution.**

(a) $kT/C_1(1 + \tfrac{2}{4} + \tfrac{4}{16})$ = **1.75** $kT/C_1$, **85.1** µV rms.

(b) $1 + \tfrac14 + \tfrac1{16}$ = **1.3125** $kT/C_1$, **73.7** µV rms, for twice the capacitance in stages 2 and 3.

(c) The referred noise approaches $2kT/C_1$, so the first stage needs twice 20-05's 0.651 pF: **1.30** pF per side.

**Sanity check.** Scaling costs about 1.2 dB of noise over equal stages in this three-stage example and saves most of the later stages' capacitance and amplifier power; the series converges, so later stages barely matter.

### Example 20-07.7 · Interleaving spurs (tier B)

**Setup.** Two channels make a 1 GS/s converter; a 0.8 V sine at 244.38 MHz is applied. Find the spur from (a) a 1 mV offset difference, (b) a 1% gain difference, (c) 1 ps of skew. (d) What skew, gain mismatch and offset difference keep spurs at −60, −60 and −80 dBc for a 500 MHz input?

**Solution.**

(a) A tone at 500 MHz: $10\log_{10}[\Delta o^2/(2A^2)]$ = **−61.1** dBc.

(b) An image at $f_s/2 - f_{in}$ = 255.62 MHz: $20\log_{10}(\alpha/2)$ = **−46.0** dBc. The simulation gives **−46.06** dBc, which is $(\alpha/2)/(1 + \alpha/2)$: the two gains, 1 and 1.01, average 1.005, and the image is measured against that mean signal. Razavi's SNR $4/\alpha^2$ = **46.0** dB.

(c) The same image frequency: $20\log_{10}(\pi f_{in}\Delta t)$ = **−62.3** dBc.

(d) Skew $\Delta t = 1/(\pi f_{in}10^{60/20})$ = **0.64** ps; gain mismatch $2 \times 10^{-60/20}$ = **0.2**%; offset difference $A\sqrt{2 \times 10^{-8}}$ = **0.113** mV.

**Sanity check.** A picosecond is the time of flight of only about 0.15 mm of on-chip wire even at the speed of light in silicon dioxide (RC-limited wires are slower still), or a few millivolts of threshold mismatch in a clock buffer; the requirement tightens in proportion to input frequency, which is why GHz interleaved converters calibrate skew to tens of femtoseconds.

### Example 20-07.8 · Settling the MDAC (tier B)

**Setup.** The MDAC of Example 20-07.5 ($C_s = C_f$ = 0.5 pF, $C_p$ = 0.1 pF) is the first stage of a 12-bit, 200 MS/s pipeline. The next stage loads it with 0.5 pF, and the hold phase lasts 2.5 ns. Find the closed-loop time constant needed, β, the effective load, the op-amp's unity-gain frequency and $g_m$, and the current per side at $g_m/I_D$ = 12 V⁻¹.

**Solution.**

- Settling to half an LSB at 12 bits: $\tau \le 2.5\ \text{ns}/(13\ln 2)$ = **0.277** ns.
- β = 0.5/1.1 = **0.455**.
- $C_{L,eff} = 0.5 + 0.5 \times 0.6/1.1$ = **0.773** pF.
- $f_t = 1/(2\pi\beta\tau)$ = **1.26** GHz, so $g_m = 2\pi f_tC_{L,eff}$ = **6.13** mS: **0.511** mA per side.

**Units check.** $C/(\beta\tau)$ is F/s, that is siemens.

**Sanity check.** With $T_h = 1/(2f_s)$, the requirement is $f_t/f_s = (N + 1)\ln 2/(\pi\beta)$ = **6.3**: a first-stage op-amp needs a unity-gain frequency several times the sample rate. Later stages, with scaled capacitors and fewer bits left to resolve, need much less. Slewing adds to this budget, because a large residue step must first be slewed before it settles linearly.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 20-07.1a | comparators, 6 bits | 63 | — |
| Ex 20-07.1b | comparators, 8 bits | 255 | — |
| Ex 20-07.1c | 8-bit LSB | 3.906 | mV |
| Ex 20-07.1d | offset sigma | 0.488 | mV |
| Ex 20-07.1e | input-pair area | 51.4 | µm² |
| Ex 20-07.1f | input capacitance, 8 bits | 75.1 | pF |
| Ex 20-07.1g | input capacitance, 6 bits | 1.16 | pF |
| Ex 20-07.1h | ratio 8 to 6 bits | 65 | — |
| Ex 20-07.2a | v_x step 1 | −0.1 | V |
| Ex 20-07.2b | v_x step 2 | 0.15 | V |
| Ex 20-07.2c | v_x step 3 | 0.025 | V |
| Ex 20-07.2d | v_x step 4 | −0.0375 | V |
| Ex 20-07.2e | output code | 9 | — |
| Ex 20-07.3a | conventional energy, 10 bits | 1363.3 | C_u V² |
| Ex 20-07.3b | monotonic energy, 10 bits | 255.5 | C_u V² |
| Ex 20-07.3c | saving | 81.3 | % |
| Ex 20-07.3d | conventional energy per conversion | 1.363 | pJ |
| Ex 20-07.3e | monotonic energy per conversion | 0.256 | pJ |
| Ex 20-07.3f | conventional power | 136 | µW |
| Ex 20-07.3g | monotonic power | 25.6 | µW |
| Ex 20-07.3h | conventional energy, 12 bits | 5459.3 | C_u V² |
| Ex 20-07.3i | ratio 12 to 10 bits | 4.0 | — |
| Ex 20-07.4a | margin step 1 | 64 | LSB |
| Ex 20-07.4b | margin step 2 | 32 | LSB |
| Ex 20-07.4c | margin step 3 | 32 | LSB |
| Ex 20-07.4d | margin step 4 | 32 | LSB |
| Ex 20-07.4e | margin step 5 | 32 | LSB |
| Ex 20-07.4f | settling error | 31 | LSB |
| Ex 20-07.4g | binary worst-case error | 31 | LSB |
| Ex 20-07.4h | redundant worst-case error | 0 | LSB |
| Ex 20-07.5a | ideal residue | 0.1 | V |
| Ex 20-07.5b | gain error, A = 1000 | 0.22 | % |
| Ex 20-07.5c | gain error, A = 100 | 2.2 | % |
| Ex 20-07.5d | residue, A = 1000 | 0.099780 | V |
| Ex 20-07.5e | residue, A = 100 | 0.097847 | V |
| Ex 20-07.5f | gain needed, 10 bits | 1126 | — |
| Ex 20-07.5g | gain needed, 10 bits, dB | 61.0 | dB |
| Ex 20-07.5h | gain needed, 12 bits | 4506 | — |
| Ex 20-07.5i | gain needed, 12 bits, dB | 73.1 | dB |
| Ex 20-07.5j | code errors with 0.3 V_REF offset | 26 | codes |
| Ex 20-07.5k | worst DNL, 0.2% gain error | −0.255 | LSB |
| Ex 20-07.5l | interior missing codes, 1% gain error | 4 | — |
| Ex 20-07.6a | referred noise, scaled | 1.75 | kT/C_1 |
| Ex 20-07.6b | referred noise, scaled | 85.1 | µV |
| Ex 20-07.6c | referred noise, equal | 1.3125 | kT/C_1 |
| Ex 20-07.6d | referred noise, equal | 73.7 | µV |
| Ex 20-07.6e | first-stage capacitance | 1.30 | pF |
| Ex 20-07.6f | noise cost of scaling | 1.2 | dB |
| Ex 20-07.7a | offset spur | −61.1 | dBc |
| Ex 20-07.7b | gain-mismatch spur | −46.0 | dBc |
| Ex 20-07.7i | gain-mismatch spur, simulated | −46.06 | dBc |
| Ex 20-07.7c | Razavi gain-mismatch SNR | 46.0 | dB |
| Ex 20-07.7d | skew spur | −62.3 | dBc |
| Ex 20-07.7e | skew for 60 dBc at 500 MHz | 0.64 | ps |
| Ex 20-07.7f | gain mismatch for 60 dBc | 0.2 | % |
| Ex 20-07.7g | offset for −80 dBc | 0.113 | mV |
| Ex 20-07.7h | image frequency | 255.62 | MHz |
| Txt 20-07.a | skew for 60 dBc at 500 MHz | 0.64 | ps |
| Txt 20-07.b | Schreier figure, ADS8881 at 1 kHz | 179.5 | dB |
| Txt 20-07.c | power increase with background calibration | 22 | % |
| Txt 20-07.d | Schreier figure, ADC12DJ5200RF per channel | 144.0 | dB |
| Txt 20-07.e | channels of the 72 GS/s design | 64 | — |
| Txt 20-07.f | effective bits at 36.1 dB SNDR | 5.7 | bits |
| Ex 20-07.8a | time constant | 0.277 | ns |
| Ex 20-07.8b | feedback factor | 0.455 | — |
| Ex 20-07.8c | effective load | 0.773 | pF |
| Ex 20-07.8d | unity-gain frequency | 1.26 | GHz |
| Ex 20-07.8e | transconductance | 6.13 | mS |
| Ex 20-07.8f | current per side | 0.511 | mA |
| Ex 20-07.8g | unity-gain frequency over sample rate | 6.3 | — |
| Txt 20-07.g | unity-gain frequency for 12 bits, beta 0.45 | 1.27 | GHz |
| Txt 20-07.h | 12-bit conventional DAC power at 1 fF | 0.546 | mW |

## 5. Simulate it

The lab ([labs/20-07-lab](../labs/20-07-lab/README.md)) implements the architectures in `nyq.py` and confirms the MDAC in ngspice.

**Predict, then run.**

1. Predict what a single bubble does to a first-transition encoder and to a ones-counting encoder (Part 1).
2. Predict the conventional and monotonic switching energies for 10 bits, then compute them for every code; plot energy against code (Part 2).
3. Predict which errors redundancy forgives: run the 10-bit pipeline with comparator offsets, a large offset and gain errors; plot the DNL (Part 3). Run `ngspice -b mdac.cir`.
4. Predict the three interleaving spurs of Example 20-07.7, then simulate them and look at the spectra (Part 4).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Flash resolution | Speed (one cycle) | $2^N$ comparators, input capacitance, offset area | Converter architect |
| SAR resolution | Energy efficiency | $N$ cycles per sample, DAC matching and settling | Converter architect |
| Redundancy (extra SAR cycles, 1.5-bit stages) | Tolerance to comparator offset and DAC settling | Cycles, comparators, digital logic | Analog designer |
| Monotonic or other low-energy switching | DAC switching energy, capacitance | Common-mode drift, comparator design | Analog designer |
| Residue-amplifier gain and bandwidth | Pipeline linearity and speed | Power, headroom; or calibration complexity | Analog designer |
| Stage scaling | Power and area | A little noise | Converter architect |
| Interleaving factor $M$ | Sample rate | Mismatch spurs, calibration, clock distribution, input loading | System and converter architects |
| Background calibration | Robustness over temperature and aging | Power, area, convergence time | Product definition |

## 7. Numbers to know

| Quantity | Typical value | Note |
|---|---|---|
| Flash comparators | $2^N - 1$; used to about 6 bits | Murmann's short course: "Typically use for B≤6" [3] |
| Flash comparator area for fixed yield | fourfold per bit, on top of the doubling count | Pelgrom scaling (Example 20-07.1) |
| SAR cycles per sample | $N$ comparisons, plus any redundant ones | §3.2, §3.3 |
| SAR switching energy, 10 bits, differential | 1363.3 (conventional) and 255.5 (monotonic) $C_uV_{REF}^2$ | Example 20-07.3; Liu et al. report "about 81%" less energy and 50% less capacitance [2] |
| 1.5-bit stage offset tolerance | $\pm V_{REF}/4$ | Razavi, citing Lewis et al. [5] |
| Residue-amplifier gain | $A > 2^{N-1}/\beta$: about 73 dB at 12 bits, 86 dB at 14 bits | Example 20-07.5, Problem 20-07.8 |
| Noise of a stage-scaled pipeline | about $2kT/C_1$ | §3.4 |
| Two-channel skew for 60 dBc at 500 MHz | 0.64 ps | Example 20-07.7 |
| Best Schreier figure by speed (as of Nov 2026) | 186.8 dB (SAR, < 1 MS/s); 181.5 dB (pipelined-SAR, 130 MS/s); 173.3 dB (pipeline, 1 GS/s); 159.3 dB (interleaved pipeline, 12 GS/s); 150.1 dB (interleaved SAR, 200 GS/s) | Murmann survey [11], [12] [R-339] |
| Fastest published (as of Nov 2026) | single-channel SAR 2.4 GS/s (7 b, 2017); interleaved 200 GS/s (8 b, 2024) | [11], [12] [R-339] |
| Commercial precision SAR (as of Nov 2026) | 18 b, 1 MS/s, 5.5 mW, SINAD 99.9 dB at 1 kHz: a Schreier figure of about **179.5** dB | TI ADS8881 [15] [R-340] |
| Commercial RF-sampling interleaved ADC (as of Nov 2026) | 12 b, up to 10.4 GS/s, 4.0–5.0 W whole chip | TI ADC12DJ5200RF [10] [R-340] |

## 8. Common mistakes

- **Extrapolating flash beyond 6 bits.** Comparator count doubles per bit and offset area quadruples; input capacitance grows about 65× for two bits.
- **Treating SAR DAC energy as the SAR's power.** In fast SARs, the comparator, logic and reference buffer usually dominate.
- **Assuming redundancy fixes gain errors.** It absorbs decision errors only; residue gain errors and capacitor mismatch need calibration.
- **Sizing pipeline stages equally.** Later stages' noise is divided by the gain squared; scaling them saves power at small noise cost.
- **Ignoring skew in interleaved converters.** Its spur grows with input frequency like jitter's noise, and a picosecond is far too much at GHz inputs.
- **Reading an interleaved converter's SNR without its spurs.** Some data sheets exclude interleaving spurs from SNR; check SFDR and the footnotes.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **SAR-based architectures dominate [Established].** Murmann's 2022 short course sums up the field as "Going hybrid & dominance of SAR-based architectures" [3]. In his survey (August 2026 revision), 48 Nyquist-rate converters were published at ISSCC and the VLSI Symposium in 2024–2026; 25 of them are time-interleaved and none is a pure flash or folding design [11] [R-339]. Flash now lives mainly inside other converters, as a coarse quantizer.
- **Each architecture owns a speed range [Established; the category assignment is our extraction from the survey].** By the Schreier figure at high input frequency, SARs lead below 10 MS/s (186.8 dB, ISSCC 2018), pipelined-SAR hybrids from 10 MS/s to 1 GS/s (182.3 dB at 50 MS/s, ISSCC 2024; 181.5 dB at 130 MS/s, ISSCC 2022), a single-channel pipeline at 1 GS/s (173.3 dB, ISSCC 2025), interleaved pipelines between 10 and 100 GS/s (159.3 dB at 12 GS/s, ISSCC 2024) and interleaved SARs above 100 GS/s (150.1 dB) [11], [12]. This is the boundary list of §3.6, with dates.
- **Speed records come from interleaving SARs [Established].** A 64× interleaved SAR reached 90 GS/s at 8 bits and 667 mW in 32 nm SOI in 2014; a 64-way 5 nm design reached 60 GS/s at 7 bits and 109.3 mW, with 34.3 dB SNDR up to 32 GHz, in 2024 [12]. The fastest entry in the survey is a 200 GS/s, 8-bit receiver built into an 800 Gb/s coherent-optics DSP (ISSCC 2024); the survey lists 41.5 dB SNDR at low frequency and 36.1 dB at 20 GHz, and the abstract gives neither the channel count nor the sub-ADC type [12]. Hybrids interleave too: a 2025 converter reaches 72 GS/s at 9 bits from 1.125 GS/s pipelined-SAR units, that is **64** channels, with 37.0 dB SNDR at Nyquist and 393.6 mW [12]. Single-channel SARs top out near 2.4 GS/s at 7 bits (ISSCC 2017) [11].
- **Pipelines survive by changing their amplifiers [Established].** Digital calibration of open-loop or imprecise amplifiers [7] and ring amplifiers [8] removed the precision op-amp that made pipelines hard to scale. A 16 nm single-channel ring-amplifier pipeline reaches 1 GS/s with 10.91 ENOB at 17.8 mW, calibrating DAC mismatch and interstage gain in the background with dither (VLSI 2024) [12].
- **High-speed converters calibrate continuously [Established].** Published examples include comparator offsets calibrated "by detecting patterns in the SAR output decisions" [12], correlation-based timing-skew calibration [14] and Razavi's background timing calibration, which held the skew image to −75 dB above 500 MHz [6]. A 2025 paper adds that skew calibration alone "only provides first-order correction for bandwidth mismatch" [12]. Commercial parts swap in a spare core so that the others can be recalibrated without stopping [10].
- **Low-energy switching schemes [Contested as a ranking].** Splitting the MSB capacitor saves 37%, monotonic switching about 81% and merged-capacitor switching 93.4%, each against its own "conventional" baseline, with different assumptions about references and reset [2], [13]. Treat them as each paper's claim, not as a league table.

### Why it matters commercially

Nyquist ADCs sit in nearly every product the learner covers, and the architecture tells you where the engineering value lies. In **MCUs, wearables and IoT nodes**, the converter is almost always a SAR (18-06): it has no static amplifier, so its power scales with sample rate. TI's 18-bit ADS8881 draws 5.5 mW at 1 MS/s and 0.55 mW at 100 kS/s, and its data sheet says "Power consumption directly scales with speed" [15], which is what a duty-cycled sensor needs. In **AI datacenters**, high-speed optical and electrical receivers increasingly digitize the line with an interleaved ADC and equalize in DSP; the survey's fastest converter is exactly such a receiver, inside an 800 Gb/s coherent DSP [12]. In **automotive radar, 5G and test equipment**, RF-sampling interleaved ADCs such as the ADC12DJ5200RF sample gigahertz signals directly [10]; their interleaving spurs and calibration behavior are system issues, not footnotes.

The scaling story matters for valuations and roadmaps. SAR-based designs are mostly switches, capacitors and logic, so they improve with each digital node; pipelines depended on precision op-amps, which "created a migration to SAR architectures" in nanometer CMOS (Razavi [5]). Ginsburg and Chandrakasan chose an interleaved SAR in 2007 "due to its simplicity versus flash and its amenability to scaled technologies versus pipelined, which relies on operational amplifiers" [13]. A converter IP portfolio built on calibration algorithms and SAR cores ports to new nodes more cheaply than one built on precision analog blocks. The converse risk is that calibration is where the hard-won know-how sits, and it is the least visible part of a data sheet.

> **Deeper:** see companion repo *Datacenter Networking* for ADC-based serial-link and coherent-optics receivers.

### Questions for engineering leaders

1. **"Which architecture is the core, and why that one at this speed and resolution?"** Strong: places the design on the survey's frontier at its rate, quotes the Schreier figure at Nyquist and says which power is included. Evasive: "a proprietary architecture"; a figure of merit at low input frequency only.
2. **"How much of the performance comes from calibration, and what happens when it is interrupted or the temperature moves?"** Strong: foreground versus background, convergence time, residual spurs over temperature, and what the output does while cores are swapped. Evasive: "calibration takes care of it."
3. **"What are the interleaving spurs at the top of the band, typical and worst case, and are they in the SNR?"** Strong: $f_s/2 - f_{in}$ and $f_s/M \pm f_{in}$ levels across parts and temperature, with the SNR footnotes stated. Evasive: an SNR that excludes interleaving spurs, quoted alone.
4. **"What do the reference buffer, input driver and clock cost?"** Strong: a package-level power breakdown, including the reference buffer that must recharge the SAR DAC every cycle and the clock that sets the skew. Evasive: core-only power.
5. **"How does this design move to the next node?"** Strong: which blocks are digital (SAR logic, calibration) and which analog (sampler, reference, amplifiers), with the redesign effort for each. Evasive: "it's basically digital."

### Marketing vs Reality

- **"81% (or 93%) less switching energy."** Each figure is against its own baseline [2], [13], and the DAC is only part of a SAR's power; the comparator, logic, reference buffer and clock often dominate at high speed. Liu et al.'s converter, with its 81% saving, draws 0.826 mW at 50 MS/s for 57.0 dB SNDR [2].
- **"SNR excludes interleaving spurs."** The ADC12DJ5200RF data sheet says so explicitly: "SNR results exclude DC, HD2 to HD9 and interleaving spurs; SINAD, ENOB, and SFDR results exclude DC and fixed-frequency interleaving spurs." Its $f_s/2 - f_{in}$ spur is specified separately: −68 dBFS typical and −56 dBFS maximum at 2.4 GHz [10]. Read the worst case, not just the typical.
- **"Background calibration."** It costs power and can disturb the data. The same part draws 4.90 W with background calibration against 4.01 W with foreground calibration, **22**% more, and warns that "small brief glitches may still occur on the converter data as the cores are swapped" [10].
- **"Record figure of merit."** The survey's Readme warns that power "Sometimes … includes power for clocks, references, etc.; sometimes it doesn't" [11]. Academic interleaved cores reach 150–160 dB; the ADC12DJ5200RF computes to about **144.0** dB per channel (53.9 dBFS SINAD at 2397 MHz, $f_s$ = 5.12 GS/s, and half of its 5.03 W dual-channel power), which includes a JESD204C interface, input buffers and a spare core. Neither number is wrong; they measure different things. Watch labels too: one 2025 abstract calls a 53.7 fJ/conversion-step Walden figure "FoMs" [12].
- **"200 GS/s, 8 bits."** At 20 GHz the record receiver's survey entry is 36.1 dB SNDR, about **5.7** effective bits [12]. For wideband converters, ask for ENOB at the top of the band.
- **Sanity check.** For any interleaved claim, compute the skew it implies: a two-channel spur of −60 dBc at 500 MHz needs $\Delta t$ ≤ 0.64 ps (§3.5). If the claimed spur needs tens of femtoseconds, ask how skew is calibrated and over what temperature range. For any architecture claim, place it on the survey's Schreier-versus-speed plot.

## 10. Concept check

**Q1.** Why does flash resolution stop at about 6 bits?

<details><summary>Answer</summary>

Comparator count doubles per bit, and the offset requirement (σ ≈ LSB/8 for good yield) quadruples each comparator's input-pair area per bit. Power and input capacitance therefore grow roughly eightfold per bit.

</details>

**Q2.** In a charge-redistribution SAR, why does the comparator always compare with zero, and what does that mean for its offset?

<details><summary>Answer</summary>

The DAC subtracts the trial value from the sampled input on the top plate, so the comparator only senses the sign of $v_x$. Its offset shifts every transition by the same amount: an offset error, not nonlinearity.

</details>

**Q3.** Why does monotonic switching save energy?

<details><summary>Answer</summary>

It never charges a capacitor to the reference on a trial that may fail. The first comparison needs no switching, and each later step switches one capacitor on one side from the reference to ground, which draws far less charge from the reference than charging and then discharging large capacitors.

</details>

**Q4.** What decision error can a redundant SAR step absorb?

<details><summary>Answer</summary>

Up to $m_k = \sum_{j>k}w_j - w_k + 1$ LSB: the amount by which the remaining weights can reach beyond the current one. Binary weights have no margin.

</details>

**Q5.** Why does a 1.5-bit pipeline stage tolerate comparator offsets up to $V_{REF}/4$, but not residue-amplifier gain error?

<details><summary>Answer</summary>

An offset moves the decision boundary; the residue changes by $V_{REF}$ there but stays within the next stage's range, and the digital addition of overlapping stage outputs undoes it. A gain error scales the residue itself, so the next stages measure the wrong quantity and no later decision can tell.

</details>

**Q6.** Why does a 2× interleaved ADC with timing skew show a spur at $f_s/2 - f_{in}$ that grows with $f_{in}$?

<details><summary>Answer</summary>

Every other sample is taken Δt late, so it is in error by about $\Delta t\,dv/dt$, proportional to $f_{in}$. Errors that alternate sign every sample modulate the signal by a square wave at $f_s/2$, producing an image at $f_s/2 - f_{in}$ of relative amplitude $\pi f_{in}\Delta t$.

</details>

Problems: [20-07 problem set](../problems/20-07-problems.md) · Worked solutions: [20-07 solutions](../solutions/20-07-solutions.md)

## 11. Key terms

[Flash ADC](../../../reference/glossary.md#flash-adc) · [Thermometer code](../../../reference/glossary.md#thermometer-code) · [Successive-approximation (SAR) ADC](../../../reference/glossary.md#successive-approximation-sar-adc) · [Charge-redistribution DAC](../../../reference/glossary.md#charge-redistribution-dac) · [Monotonic switching](../../../reference/glossary.md#monotonic-switching) · [Redundancy (ADC)](../../../reference/glossary.md#redundancy-adc) · [Pipeline ADC](../../../reference/glossary.md#pipeline-adc) · [Residue](../../../reference/glossary.md#residue) · [Multiplying DAC (MDAC)](../../../reference/glossary.md#multiplying-dac-mdac) · [Time-interleaved ADC](../../../reference/glossary.md#time-interleaved-adc) · [Timing skew](../../../reference/glossary.md#timing-skew)

## 12. Connections

- **Previous:** [20-06](20-06-data-converter-fundamentals.md) defined the metrics these architectures are judged by.
- **Builds on:** [20-05](20-05-comparators-and-sample-and-hold.md) (sampler, comparator, metastability), [20-02](20-02-two-stage-op-amp-design.md) (op-amp gain and settling for residue amplifiers), [10-08](../../10-electronics-1/chapters/10-08-current-sources-and-mirrors.md) (mismatch).
- **Next:** [20-08](20-08-sigma-delta-converters.md) trades sample rate for resolution with oversampling and noise shaping.
- **Used later:** [20-09](20-09-dacs.md) (the DACs inside these converters), [20-10](20-10-plls-and-jitter.md) (the clocks interleaved converters depend on), [20-11](20-11-layout-matching-pvt.md) (matching and calibration).

## 13. Further study

- M. Pelgrom, *Analog-to-Digital Conversion*, 4th ed., Springer, 2022: the chapters on Nyquist converters.
- B. Razavi, "A tale of two ADCs: Pipelined versus SAR," *IEEE Solid-State Circuits Magazine*, 2015, and "Design considerations for interleaved ADCs," *IEEE JSSC*, 2013 (§14 [5], [6]): short, rigorous treatments; both are posted on the author's UCLA page.
- B. Murmann, ADC Performance Survey (github.com/bmurmann/ADC-survey): filter the spreadsheet by architecture and plot figure of merit against speed.

## 14. Sources

1. J. L. McCreary and P. R. Gray, "All-MOS charge redistribution analog-to-digital conversion techniques—Part I," *IEEE J. Solid-State Circuits*, vol. SC-10, no. 6, pp. 371–379, Dec. 1975, DOI 10.1109/JSSC.1975.1050629 [R-337].
2. C.-C. Liu, S.-J. Chang, G.-Y. Huang and Y.-Z. Lin, "A 10-bit 50-MS/s SAR ADC with a monotonic capacitor switching procedure," *IEEE J. Solid-State Circuits*, vol. 45, no. 4, pp. 731–740, Apr. 2010, DOI 10.1109/JSSC.2010.2042254 [R-337].
3. B. Murmann, "Introduction to ADCs/DACs: Metrics, Topologies, Trade Space, and Applications," ISSCC Short Course, Feb. 2022, slides 16, 18, 28 and 91 (PDF in github.com/bmurmann/ADC-survey) [R-339].
4. S.-W. M. Chen and R. W. Brodersen, "A 6-bit 600-MS/s 5.3-mW asynchronous ADC in 0.13-µm CMOS," *IEEE J. Solid-State Circuits*, vol. 41, no. 12, pp. 2669–2680, Dec. 2006, DOI 10.1109/JSSC.2006.884231 [R-337].
5. S. H. Lewis, H. S. Fetterman, G. F. Gross, R. Ramachandran and T. R. Viswanathan, "A 10-b 20-Msample/s analog-to-digital converter," *IEEE J. Solid-State Circuits*, vol. 27, no. 3, pp. 351–358, Mar. 1992, DOI 10.1109/4.121557; B. Razavi, "A tale of two ADCs: Pipelined versus SAR," *IEEE Solid-State Circuits Magazine*, vol. 7, no. 3, pp. 38–46, Summer 2015, DOI 10.1109/MSSC.2015.2442372 [R-338].
6. B. Razavi, "Design considerations for interleaved ADCs," *IEEE J. Solid-State Circuits*, vol. 48, no. 8, pp. 1806–1817, Aug. 2013, DOI 10.1109/JSSC.2013.2258814 [R-338].
7. B. Murmann and B. E. Boser, "A 12-bit 75-MS/s pipelined ADC using open-loop residue amplification," *IEEE J. Solid-State Circuits*, vol. 38, no. 12, pp. 2040–2050, Dec. 2003, DOI 10.1109/JSSC.2003.819167 [R-338].
8. B. Hershberg, S. Weaver, K. Sobue, S. Takeuchi, K. Hamashita and U.-K. Moon, "Ring amplifiers for switched capacitor circuits," *IEEE J. Solid-State Circuits*, vol. 47, no. 12, pp. 2928–2942, Dec. 2012, DOI 10.1109/JSSC.2012.2217865 [R-338].
9. Texas Instruments, *ADC32RF45 Dual-Channel, 14-Bit, 3.0-GSPS, Analog-to-Digital Converter*, data sheet SBAS747C, rev. Dec. 2016 [R-340].
10. Texas Instruments, *ADC12DJ5200RF*, data sheet SLVSEN9H, rev. Aug. 2026 [R-340].
11. B. Murmann, "ADC Performance Survey 1997–2026," github.com/bmurmann/ADC-survey (xls/ADCsurvey_latest.xlsx, revision of Aug. 2026), accessed 24 Nov 2026 [R-339].
12. C. Nani et al., "A 5nm 60GS/s 7b 64-way time interleaved partial loop unrolled SAR ADC achieving 34dB SNDR up to 32GHz," VLSI Symp. 2024, DOI 10.1109/VLSITechnologyandCir46783.2024.10631522; L. Kull et al., ISSCC 2014, DOI 10.1109/ISSCC.2014.6757477; R. L. Nguyen et al., ISSCC 2024, pp. 344–346, DOI 10.1109/ISSCC49657.2024.10454385; Zhang et al., ISSCC 2025, pp. 436–438, DOI 10.1109/ISSCC49661.2025.10904672; Lagos et al., VLSI Symp. 2024, DOI 10.1109/VLSITechnologyandCir46783.2024.10631330; Cao et al., ISSCC 2025, paper 24.2, DOI 10.1109/ISSCC49661.2025.10904766 [R-339].
13. B. P. Ginsburg and A. P. Chandrakasan, ISCAS 2005, pp. 184–187, DOI 10.1109/ISCAS.2005.1464555, and "500-MS/s 5-bit ADC in 65-nm CMOS with split capacitor array DAC," *IEEE J. Solid-State Circuits*, vol. 42, no. 4, pp. 739–747, Apr. 2007, DOI 10.1109/JSSC.2007.892169; V. Hariprasath, J. Guerber, S.-H. Lee and U.-K. Moon, *Electronics Letters*, vol. 46, no. 9, pp. 620–621, Apr. 2010, DOI 10.1049/el.2010.0706 [R-337].
14. M. El-Chammas and B. Murmann, "A 12-GS/s 81-mW 5-bit time-interleaved flash ADC with background timing skew calibration," *IEEE J. Solid-State Circuits*, vol. 46, no. 4, pp. 838–847, Apr. 2011, DOI 10.1109/JSSC.2011.2108125; S. M. Jamal et al., *IEEE J. Solid-State Circuits*, vol. 37, no. 12, pp. 1618–1627, Dec. 2002, DOI 10.1109/JSSC.2002.804327 [R-338].
15. Texas Instruments, *ADS8881* data sheet SBAS547D, rev. Aug. 2015 [R-340].
16. W. C. Black and D. A. Hodges, "Time interleaved converter arrays," *IEEE J. Solid-State Circuits*, vol. SC-15, no. 6, pp. 1022–1029, Dec. 1980, DOI 10.1109/JSSC.1980.1051512 (the first interleaved converter arrays); S. H. Lewis and P. R. Gray, *IEEE J. Solid-State Circuits*, vol. SC-22, no. 6, pp. 954–961, Dec. 1987, DOI 10.1109/JSSC.1987.1052843 (an early CMOS pipeline with digital correction) [R-338].
