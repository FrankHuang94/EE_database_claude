<!-- status: verified -->
# 20-11 · Layout, Matching and PVT Variation

| | |
|---|---|
| **Course** | [20 · Analog and Mixed-Signal IC Design](../README.md) |
| **University equivalent** | The matching, layout and variability material of a graduate analog IC course: device mismatch and Pelgrom's law, gradients and common-centroid layout, layout-dependent effects, guard rings and latch-up, parasitics, process corners and Monte Carlo (Hastings, *The Art of Analog Layout*; Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed., the layout chapter) |
| **Prerequisites** | [20-01](20-01-analog-design-fundamentals-gm-id.md) ($g_m/I_D$), [03-04](../../03-probability-statistics-and-random-variables/chapters/03-04-joint-distributions-and-clt.md) (sums of random variables), [03-05](../../03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md) (estimation and confidence), [19-11](../../19-digital-vlsi-design/chapters/19-11-place-route-signoff.md) (physical design) |
| **Estimated study hours** | 7 |
| **Last verified** | 2026-11-24 |

**Learning objectives.** After this chapter you can:

1. Derive Pelgrom's area law and size devices for a mismatch target.
2. Compute the mismatch of current mirrors and the offset of differential pairs from threshold and gain-factor terms, and choose $g_m/I_D$ accordingly.
3. Explain the speed–accuracy–power limit that mismatch imposes.
4. Design placement patterns that cancel linear and quadratic gradients, and list the layout-dependent effects that patterns cannot cancel.
5. Plan a verification over corners and Monte Carlo, including how many runs a yield claim needs.
6. Explain guard rings, latch-up and the role of parasitic extraction.

## 1. Big picture

Two transistors drawn identically are never identical. Random atomic-scale variations (the number of dopant atoms under the gate, the roughness of the gate's edge, the grain of the gate material) give every device a slightly different threshold voltage and gain factor; smooth gradients across the wafer and the layout's own surroundings add systematic differences on top. Digital circuits tolerate this, because a logic gate only needs to tell 0 from 1. Analog circuits do not: an amplifier's offset, a DAC's linearity, a bandgap's accuracy and a comparator's threshold are all set by how well devices match. And beyond matching, every circuit must work at every combination of **process**, **voltage** and **temperature** (PVT) its product will see.

- **Offsets and linearity** of amplifiers, comparators, converters and references are mismatch-limited (20-05 to 20-09).
- **Area and power** of precision analog blocks are set by matching: halving an offset costs four times the area (§3.1).
- **Layout** decides whether systematic errors cancel: the same transistors placed carelessly can be ten times worse.
- **Verification** of analog blocks is statistical: corners, Monte Carlo and the confidence those runs actually buy.
- **Automotive and industrial** products widen the PVT space (−40 °C to 125 °C or 150 °C) and make variability a qualification issue.

## 2. Intuition first

```text
 side by side           common centroid (ABBA)          one row, gradient g(x) of V_TH
  [ A ][ B ]              [ A ][ B ][ B ][ A ]            A:   x = −1.5p, +1.5p   → mean 0
  A sees g(x_A),          each device's centroid          B:   x = −0.5p, +0.5p   → mean 0
  B sees g(x_B)           sits at the same point          linear part cancels; x² part does not
```

*Figure 1. Gradients and placement. A linear gradient shifts two side-by-side devices differently; splitting each into halves placed symmetrically (ABBA) gives both the same average position, so the linear part cancels.*

**A polling analogy, and its limits.** A transistor's threshold is like the average opinion of the dopant atoms under its gate. A small gate polls few atoms, so its average is noisy; a gate four times larger polls four times as many and its random error halves: that is Pelgrom's law. A *systematic* error is like a regional bias in a survey: polling more people in the same region does not help, but sampling both devices from the same mix of regions (common centroid) does. The analogy breaks at the edges: real devices also respond to their neighbors (stress from nearby isolation, dopant scattered from a nearby well edge), which no amount of averaging or symmetry removes unless the neighbors are also made identical, which is what dummy devices do.

## 3. Theory

### 3.1 Random mismatch and Pelgrom's law

Divide a gate of area $WL$ into many small patches, each with an independent random contribution to the device's threshold. The device's threshold is the average over its patches; the average of $n$ independent terms has a standard deviation $1/\sqrt n$ of one term's, and $n$ is proportional to area. So the threshold's random part scales as $1/\sqrt{WL}$. Pelgrom, Duinmaijer and Welbers wrote this for the **difference** between two nominally identical devices [1] (Lakshmikumar, Hadaway and Copeland had modeled mismatch against device dimensions three years earlier [2]):

$$
\sigma(\Delta V_{TH}) = \frac{A_{VT}}{\sqrt{WL}}, \qquad \sigma\!\left(\frac{\Delta\beta}{\beta}\right) = \frac{A_\beta}{\sqrt{WL}} ,
$$

with technology constants $A_{VT}$ (mV·µm), the Pelgrom coefficient for the threshold $V_{TH}$, and $A_\beta$ (%·µm), plus a distance term that is negligible for devices close together. A single device's deviation from the mean is $1/\sqrt2$ of the pair value. Because $\sigma^2 \propto 1/(WL)$, **halving a mismatch requires four times the area**; this is the most important design law of precision analog.

![Log-log plot of the standard deviation of a pair's threshold difference against gate area from 0.1 to 1000 square micrometres: a straight line falling with slope minus one half, from about 11 mV at 0.1 square micrometre to 0.11 mV at 1000, with Monte Carlo points lying on it; annotations mark 3.50 mV at 1 square micrometre and 0.35 mV at 100](../../../assets/figures/20-11/pelgrom.svg)

*Figure 2. Pelgrom's law for $A_{VT}$ = 3.5 mV·µm. The dots are a Monte Carlo of gates divided into fixed 0.01 µm² patches with independent 24.75 mV errors, so larger gates average more patches: the law follows from averaging, with no fitting.*

$A_{VT}$ tracks the gate dielectric: in a well-engineered process it is roughly 1 mV·µm per nanometer of gate oxide [4], because the dominant random term is the number of dopant atoms under the gate, converted to a voltage through the oxide capacitance. The trend paused at 65 nm, the last silicon-oxynitride generation, resumed with high-k metal gates, and improved again with the lightly doped channels of FD-SOI and FinFETs [5], [6]. Pelgrom's original 2.5 µm process had $A_{VT}$ = 30 mV·µm; recent processes are below 2 mV·µm (§7). Beware comparing published values: some authors quote the single-device σ, which differs from the pair value by $\sqrt2$, and FinFET values depend on whether area means footprint or the full fin surface [5].

### 3.2 Mirrors and differential pairs

**Current mirrors.** Two transistors with the same $V_{GS}$ carry currents that differ through both terms. In strong inversion, $I \propto \beta(V_{GS} - V_{TH})^2$, so a threshold difference changes the current by $\Delta I/I = -(g_m/I_D)\,\Delta V_{TH}$, and a gain-factor difference by $\Delta\beta/\beta$. With independent terms,

$$
\sigma\!\left(\frac{\Delta I}{I}\right)^2 = \left(\frac{g_m}{I_D}\right)^2\sigma(\Delta V_{TH})^2 + \sigma\!\left(\frac{\Delta\beta}{\beta}\right)^2 ,
$$

which holds in every inversion region if $g_m/I_D$ is the device's actual value (20-01). A mirror that must match well should run at **low** $g_m/I_D$ (large overdrive): the threshold error then matters less.

**Differential pairs.** The input offset is the gate voltage difference that balances the drain currents: $V_{os} = \Delta V_{TH} + \Delta\beta/\beta \cdot I_D/g_m$ (the gain-factor error is converted to an input voltage by dividing by $g_m/I_D$):

$$
\sigma(V_{os})^2 = \sigma(\Delta V_{TH})^2 + \left(\frac{I_D}{g_m}\right)^2\sigma\!\left(\frac{\Delta\beta}{\beta}\right)^2 .
$$

A pair that must have low offset should run at **high** $g_m/I_D$, where the threshold term dominates and only area can reduce it. The opposite preferences for mirrors and pairs are a standard design rule (Example 20-11.2).

![Mismatch against gm/ID from 3 to 25 per volt for 10 by 1 micrometre devices: the mirror's current mismatch in percent rises almost linearly from about 0.5 to 2.8, while the pair's offset in millivolts falls from about 1.5 toward the 1.1 mV threshold mismatch shown as a dashed line; the curves cross near gm/ID of 10](../../../assets/figures/20-11/gmid.svg)

*Figure 3. The same devices as a mirror and as a pair (Example 20-11.2): the threshold term grows with $g_m/I_D$ in a mirror and dominates the pair's offset at high $g_m/I_D$.*

### 3.3 The speed–accuracy–power limit

Suppose a differential pair must reach an offset σ (accuracy). Pelgrom's law fixes its area, $WL = A_{VT}^2/\sigma^2$, and so its gate capacitance $C = C_{ox}WL = C_{ox}A_{VT}^2/\sigma^2$. Driving that capacitance over a signal swing $V$ at a bandwidth $f$ (speed) takes a power proportional to $CV^2f$. Rearranging,

$$
\frac{f\,(V/\sigma)^2}{P} \propto \frac{1}{C_{ox}A_{VT}^2} :
$$

speed times accuracy squared per unit of power is fixed by the technology's matching. Each extra bit of mismatch-limited accuracy (a factor of 2 in $V/\sigma$) costs four times the power at the same speed. Kinget formalized this limit and found that for MOS circuits the power that matching demands is far above what thermal noise demands (20-05; 20-12 derives a version of the comparison) [3], which is why precision converters calibrate or trim instead of buying accuracy with area (Example 20-11.3).

### 3.4 Gradients and placement

Smooth variations across a die (oxide thickness, doping, temperature from a nearby power device, mechanical stress) add a **systematic** term: a parameter $p(x) = p_0 + g_1x + g_2x^2 + \cdots$ along the row. A device split into unit cells sees the average of $p$ over its cells' positions.

- **Side by side** (AB), centers a distance $d$ apart: the difference is $g_1d$ for a linear gradient. It does not average away with area.
- **Common centroid** (ABBA): A's cells at $\pm1.5$ pitches, B's at $\pm0.5$. Both average positions are zero, so the linear term cancels. The quadratic term does not: A averages $2.25$ pitch², B $0.25$, a residual of $2g_2$ pitch².
- **Higher-order centroids** (ABBABAAB over eight cells): the average positions and the average squared positions both match, cancelling linear and quadratic gradients (Example 20-11.4).

In two dimensions the same logic gives cross-coupled quads (A and B on the diagonals). **Interdigitation** (ABAB…) keeps the two devices' centroids one pitch apart however long the row is: it reduces a linear gradient's error to that of adjacent unit cells but does not cancel it, and it keeps routing simple (the lab compares the patterns).

### 3.5 Layout-dependent effects, dummies and guard rings

Some systematic effects depend on the *surroundings* of each device rather than its position:

- **Well-proximity effect (WPE):** ions scattered from the photoresist edge during well implantation raise the doping near a well edge, shifting $V_{TH}$ of devices close to it.
- **Length-of-diffusion (LOD) and shallow-trench-isolation (STI) stress:** the mechanical stress from nearby isolation changes carrier mobility and threshold, depending on the distance from the gate to the diffusion's edge.
- **Etch and lithography effects:** the outermost fingers of an array are patterned differently from interior ones.

Symmetric patterns do not cancel these unless every device sees the same surroundings. Hence **dummy devices** at the ends of arrays (so that every active finger has a neighbor), keeping matched devices far from well edges, and equal diffusion lengths. Modern design kits model WPE and LOD in post-layout simulation. The effects are not small: well proximity has shifted thresholds by up to 100 mV within about a micrometer of a well edge, and layout-dependent effects can move bias points by 20–30% [7] (§7).

**Guard rings and latch-up.** A CMOS process contains a parasitic PNP and NPN bipolar pair (p+ in the n-well, n-well, p-substrate, n+) that forms a thyristor. If the loop gain of the two bipolars exceeds one and enough current is injected (by a pin driven beyond the rails, or a substrate current spike), the thyristor latches and shorts the supply. **Guard rings** (heavily doped rings tied to the supplies around sensitive or injecting devices) collect injected carriers and lower the parasitic resistances that turn the bipolars on; they also isolate sensitive analog blocks from substrate noise.

### 3.6 Parasitics and extraction

A schematic has ideal wires; a layout does not. Each wire adds resistance (IR drops that unbalance mirrors, RC delays that skew clocks) and capacitance (loading, coupling of digital noise into analog nodes). Matched signal paths must have matched parasitics: equal wire lengths to the two inputs of a pair, symmetric routing of differential signals, and mirror sources connected with low-resistance, symmetric wiring (a 1 mV IR drop in one source line is a 1 mV offset). **Parasitic extraction** turns the layout back into a netlist with these resistors and capacitors (and the layout-dependent device parameters of §3.5), and post-layout simulation is the only way to check them.

### 3.7 Corners, temperature and Monte Carlo

**Global variation and corners.** Wafer-to-wafer and lot-to-lot variation moves all devices on a die together. Foundries capture it with **corner models**: typical (TT) and fast or slow NMOS and PMOS (FF, SS, FS, SF), commonly described as about ±3σ of the global distribution, though each foundry defines its own; one public design kit bounds them by its electrical specifications and warns that they are "primarily for predicting static logic delay" [10]. Corners are combined with supply voltage (often ±10% of nominal [9]) and temperature limits (commercial, industrial and automotive grades, §7). A corner is not automatically the worst case of every specification: a circuit's gain may be worst at one corner and its bandwidth at another, so all must be simulated.

**Local variation and Monte Carlo.** Mismatch is local and random; corners do not capture it. **Monte Carlo** simulation draws random global and local parameters from the foundry's statistical models and repeats the simulation. Its results are statistics, and their precision depends on the number of runs:

- **Estimated σ.** From $n$ Gaussian runs, the 95% confidence interval on σ is $\sigma\sqrt{(n - 1)/\chi^2_{0.975}}$ to $\sigma\sqrt{(n - 1)/\chi^2_{0.025}}$: about **−12**% to **+16**% for 100 runs and ±4–5% for 1000 (Example 20-11.6).
- **Yield claims.** If $n$ runs all pass, the failure rate is below $p$ with 95% confidence only if $(1 - p)^n \le 0.05$, about $n \ge 3/p$ (the "rule of three"). Showing a failure rate below 0.27% (3σ) needs about 1109 failure-free runs; 6σ-class claims need statistical extrapolation, not brute force.

![Upper and lower 95 percent confidence limits on the ratio of true to estimated sigma against the number of Monte Carlo runs from 10 to 10,000 on a log axis: the band narrows from about 0.69 to 1.83 at 10 runs, to 0.878 to 1.162 at 100 runs and 0.958 to 1.046 at 1000 runs](../../../assets/figures/20-11/ci.svg)

*Figure 4. How much a Monte Carlo of n runs tells you about σ: the band narrows only as $1/\sqrt n$.*

### 3.8 Trimming and calibration

When matching cannot reach a specification at acceptable area and power, designs measure and correct the error: **trimming** at production test (fuses, one-time-programmable memory or laser-trimmed resistors that adjust a bandgap's output or an amplifier's offset at one temperature) and **calibration** in the field (foreground at power-up or background while operating, as in the converters of 20-06 to 20-09). Trimming at one temperature removes the error at that temperature; the residual drift over temperature remains and is often the true accuracy limit (20-03).

## 4. Worked examples

### Example 20-11.1 · Sizing for matching (tier A)

**Setup.** A process has $A_{VT}$ = 3.5 mV·µm. Find σ(ΔV_TH) for a pair of 10 µm × 1 µm devices, the 3σ offset, and the area that brings σ(ΔV_TH) to 0.5 mV.

**Solution.**

- σ(ΔV_TH) = 3.5 mV·µm/√(10 µm²) = **1.11** mV; 3σ = **3.32** mV.
- For 0.5 mV: $WL = (3.5/0.5)^2$ = **49** µm², **4.9** times the area for **2.2** times less mismatch.

**Units check.** mV·µm divided by µm gives mV.

**Sanity check.** $(1.11/0.5)^2 = 4.9$: the area ratio is the square of the mismatch ratio.

### Example 20-11.2 · Mirror or pair: which $g_m/I_D$? (tier B)

**Setup.** With $A_{VT}$ = 3.5 mV·µm, $A_\beta$ = 1%·µm and 10 µm × 1 µm devices, find a mirror's current mismatch and a pair's offset at $g_m/I_D$ = 5, 10 and 20 V⁻¹.

**Solution.** σ(ΔV_TH) = **1.107** mV and σ(Δβ/β) = **0.316**%.

| $g_m/I_D$ (V⁻¹) | Mirror σ(ΔI/I) | Pair σ(V_os) |
|---|---|---|
| 5 | **0.64**% | **1.27** mV |
| 10 | **1.15**% | **1.15** mV |
| 20 | **2.24**% | **1.12** mV |

**Units check.** $(g_m/I_D)\,\sigma(\Delta V_{TH})$ is V⁻¹ × V, dimensionless; σ(Δβ/β)/(g_m/I_D) is a voltage.

**Sanity check.** The mirror gets **3.5** times worse from 5 to 20 V⁻¹, while the pair improves slightly and saturates at σ(ΔV_TH): mirrors want large overdrive, pairs want weak inversion.

### Example 20-11.3 · The price of accuracy (tier B)

**Setup.** A comparator's input pair must reach σ(V_os) = 1 mV and then 0.25 mV, with $A_{VT}$ = 3.5 mV·µm and a gate capacitance of 10 fF/µm². Find the gate area and capacitance in each case, and the power ratio for the same speed.

**Solution.**

- 1 mV: $WL = 3.5^2$ = **12.25** µm², $C$ = **122.5** fF per device.
- 0.25 mV: $WL$ = **196** µm², $C$ = **1960** fF.
- At the same bandwidth and swing, power scales with capacitance: **16** times more for four times the accuracy.

**Units check.** fF/µm² × µm² = fF.

**Sanity check.** Two more bits of mismatch-limited accuracy cost 16× in power: this is the trade that drives trimming, calibration and offset cancellation (chopping, auto-zeroing) in precision analog.

### Example 20-11.4 · Gradients and placement (tier B)

**Setup.** A threshold gradient of 0.01 mV/µm runs along a row of unit cells on a 10 µm pitch. Find the systematic offset for AB placement (two cells, centers 10 µm apart), ABBA and ABBABAAB. Then add a quadratic term of 10⁻⁴ mV/µm².

**Solution.**

- Linear only: AB **0.1** mV; ABBA **0**; ABBABAAB **0**.
- With the quadratic term: ABBA leaves $2g_2p^2 = 2 \times 10^{-4} \times 100$ = **0.02** mV; ABBABAAB **0**.

**Units check.** mV/µm × µm and mV/µm² × µm² both give mV.

**Sanity check.** The systematic offset of the side-by-side pair is about a tenth of the random σ of Example 20-11.1 here, but it does not shrink with area while the random part does: large precision devices are where common centroid pays off.

### Example 20-11.5 · From σ to yield (tier B)

**Setup.** A comparator's offset has the σ = 1.107 mV of Example 20-11.1 and must stay within ±3 mV. What fraction of parts fail? What σ would make the limit a 4.5σ one?

**Solution.**

- 3 mV is **2.71**σ: failures $2[1 - \Phi(2.71)]$ = **0.67**%, a yield of **99.33**%.
- For 4.5σ, σ ≤ 3/4.5 = **0.667** mV, which by Example 20-11.1 needs $(3.5/0.667)^2$ = **27.6** µm² of gate area per device.

**Units check.** mV/mV is a count of standard deviations.

**Sanity check.** Going from 2.71σ to 4.5σ cuts the failure rate by nearly three orders of magnitude (from 0.67% to **6.8** parts per million) for **2.8** times the area: the Gaussian tail falls very fast.

### Example 20-11.6 · How many Monte Carlo runs? (tier B)

**Setup.** (a) A Monte Carlo of 100 runs gives σ(V_os) = 1.1 mV. What is the 95% confidence interval? With 1000 runs? (b) How many failure-free runs show a failure rate below 0.27% with 95% confidence?

**Solution.**

- (a) 100 runs: σ between **0.878** and **1.162** times the estimate (**0.97** to **1.28** mV). 1000 runs: **0.958** to **1.046** times.
- (b) $(1 - 0.0027)^n \le 0.05$: $n \ge$ **1109** (the rule of three gives 3/0.0027 ≈ **1111**).

**Units check.** Ratios and counts.

**Sanity check.** A "100-run Monte Carlo shows no failures" demonstrates only a failure rate below about 3%, not a 3σ design.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 20-11.1a | σ(ΔV_TH), 10 × 1 µm | 1.11 | mV |
| Ex 20-11.1b | 3σ offset | 3.32 | mV |
| Ex 20-11.1c | area for 0.5 mV | 49 | µm² |
| Ex 20-11.2a | mirror, gm/ID 5 | 0.64 | % |
| Ex 20-11.2b | mirror, gm/ID 10 | 1.15 | % |
| Ex 20-11.2c | mirror, gm/ID 20 | 2.24 | % |
| Ex 20-11.2d | pair, gm/ID 5 | 1.27 | mV |
| Ex 20-11.2e | pair, gm/ID 10 | 1.15 | mV |
| Ex 20-11.2f | pair, gm/ID 20 | 1.12 | mV |
| Ex 20-11.3a | area for 1 mV | 12.25 | µm² |
| Ex 20-11.3b | capacitance for 1 mV | 122.5 | fF |
| Ex 20-11.3c | area for 0.25 mV | 196 | µm² |
| Ex 20-11.3d | capacitance for 0.25 mV | 1960 | fF |
| Ex 20-11.3e | power ratio | 16 | — |
| Ex 20-11.4a | AB offset, linear | 0.1 | mV |
| Ex 20-11.4b | ABBA offset, linear | 0 | mV |
| Ex 20-11.4c | ABBABAAB offset, linear | 0 | mV |
| Ex 20-11.4d | ABBA offset with quadratic | 0.02 | mV |
| Ex 20-11.4e | ABBABAAB offset with quadratic | 0 | mV |
| Ex 20-11.5a | failure fraction | 0.67 | % |
| Ex 20-11.5b | yield | 99.33 | % |
| Ex 20-11.5c | σ for 4.5σ | 0.667 | mV |
| Ex 20-11.5d | area for 4.5σ | 27.6 | µm² |
| Ex 20-11.6a | CI low, 100 runs | 0.878 | — |
| Ex 20-11.6b | CI high, 100 runs | 1.162 | — |
| Ex 20-11.6c | CI low, 1000 runs | 0.958 | — |
| Ex 20-11.6d | CI high, 1000 runs | 1.046 | — |
| Ex 20-11.6e | failure-free runs | 1109 | — |
| Ex 20-11.1d | area ratio | 4.9 | — |
| Ex 20-11.1e | mismatch ratio | 2.2 | — |
| Ex 20-11.2g | σ(ΔV_TH) | 1.107 | mV |
| Ex 20-11.2h | σ(Δβ/β) | 0.316 | % |
| Ex 20-11.2i | mirror ratio, 20 vs 5 | 3.5 | — |
| Ex 20-11.5e | limit in σ | 2.71 | — |
| Ex 20-11.5f | failure rate at 4.5σ | 6.8 | ppm |
| Ex 20-11.5g | area ratio for 4.5σ | 2.8 | — |
| Ex 20-11.6f | σ low, 100 runs | 0.97 | mV |
| Ex 20-11.6g | σ high, 100 runs | 1.28 | mV |
| Ex 20-11.6h | rule-of-three runs | 1111 | — |
| Txt 20-11.a | CI low, 100 runs | −12 | % |
| Txt 20-11.b | CI high, 100 runs | +16 | % |
| Txt 20-11.c | 65 nm pair, 1 × 0.06 µm | 14.3 | mV |
| Txt 20-11.d | 1989 pair, 20 × 20 µm | 1.5 | mV |
| Txt 20-11.e | 4σ two-sided tail | 63 | ppm |
| Txt 20-11.f | 5σ two-sided tail | 0.57 | ppm |
| Txt 20-11.g | 6σ two-sided tail | 0.0020 | ppm |
| Txt 20-11.h | REF35 box over temperature | 0.174 | % |
| Txt 20-11.i | box over room-temperature spec | 3.5 | — |
| Txt 20-11.j | 100-sample σ error over 10% | 15.9 | % |

## 5. Simulate it

The lab ([labs/20-11-lab](../labs/20-11-lab/README.md)) implements the mismatch formulas, placement residuals and run-count statistics in `matching.py` and confirms a mirror's threshold sensitivity in ngspice.

**Predict, then run.**

1. Predict the slope of σ(ΔV_TH) against $1/\sqrt{WL}$, then simulate pairs built from independent unit cells and fit it (Part 1).
2. Predict the current mismatch of three square-law mirrors with a 1 mV threshold step at $g_m/I_D$ = 20, 6.32 and 3.16 V⁻¹, then run `ngspice -b mirror.cir` (Part 2).
3. Predict which of AB, AABB, ABAB, ABBA and ABBABAAB cancel linear and quadratic gradients, then compute their residuals (Part 3).
4. Predict the fraction of offsets outside ±3 mV for σ = 1.107 mV, then draw a million (Part 4).
5. Predict how widely a 100-run estimate of σ scatters and how many failure-free runs a 4.5σ claim needs, then simulate and tabulate (Part 5).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Device area | Random mismatch (σ² ∝ 1/area) | Capacitance, so speed or power; die area | Analog designer |
| $g_m/I_D$ of mirrors (low) and pairs (high) | Mirror matching; pair offset | Headroom (mirrors); area and speed (pairs) | Analog designer |
| Common-centroid and interdigitated placement | Gradient cancellation | Routing complexity, parasitic asymmetry | Layout designer |
| Dummy devices and keep-out from well edges | Layout-dependent effects | Area | Layout designer |
| Guard rings | Latch-up immunity, substrate isolation | Area, routing | Layout designer and ESD/latch-up owner |
| Monte Carlo run count | Confidence in σ and yield | Simulation time | Verification lead |
| Trimming and calibration | Accuracy beyond matching | Test time, fuses or memory, calibration logic | Product and test engineering |

## 7. Numbers to know

| Quantity | Typical value | Note |
|---|---|---|
| $A_{VT}$ rule of thumb | ≈ 1 mV·µm per nm of gate oxide | Pelgrom; Boser's course notes [4], [9] **[Established]** |
| $A_{VT}$ by process | 2.5 µm: 30 (n) / 35 (p); 180 nm: ≈ 5; 65 nm: 3.5; 28 nm bulk HKMG: 2.4; 20 nm: 1.9; 28/14 nm FD-SOI: ≈ 1.3–1.4; 14 nm SOI FinFET: 1.4 (n) / 0.7 (p) mV·µm | [1], [4], [6], with 180 nm from Boser's notes [9] [R-353], [R-354]; definitions vary by $\sqrt2$ [5] **[Industry estimate]** |
| $A_{VT}$ at 7 nm, 5 nm, GAA (as of Nov 2026) | no public measured value found | foundry data are in confidential design kits |
| Gain factor $A_\beta$ | 1–2 %·µm | [4] |
| Other components | bipolar $V_{BE}$ ≈ 0.3 mV·µm; resistors 0.5–5 %·µm; capacitors ≈ 0.3%/√(C in fF) | Pelgrom's summary [4] |
| A small 65 nm pair (1 µm × 0.06 µm) | σ(ΔV_TH) ≈ **14.3** mV | from $A_{VT}$ = 3.5 mV·µm; our arithmetic |
| Pelgrom's 1989 pair (20 µm × 20 µm) | σ(ΔV_TH) ≈ **1.5** mV | from $A_{VT}$ = 30 mV·µm; our arithmetic |
| Well-proximity shift | up to 100 mV within about 1 µm of the well edge (0.18 µm, 2003); 33% for 40 nm I/O devices against 1.87% at 16 nm FinFET | [7] [R-355] |
| Layout-dependent bias shift | 20–30% (well proximity, STI stress) | Drennan et al. [7] |
| Supply and temperature corners | $V_{DD}$ ±10%; commercial 0 to 70 °C; industrial −40 to 85 °C; AEC-Q100 grades 3/2/1/0: −40 °C to 85/105/125/150 °C | [9], [11] [R-356] **[Established]** |
| Two-sided Gaussian tails | 3σ: 2700 ppm; 4σ: **63** ppm; 4.5σ: 6.8 ppm; 5σ: **0.57** ppm; 6σ: **0.0020** ppm | exact |
| Monte Carlo precision on σ (95%) | 100 runs: −12% to +16%; 1000 runs: ±4–5% | §3.7 |
| Analog area per node (as of 2019) | 0.8–0.9× per node, against 0.5× for logic and SRAM | Loke et al. [12] **[Industry estimate]** |
| Wire capacitance | ≈ 0.2 fF/µm, about a tenth of gate capacitance per µm of width | course teaching value [9] |

## 8. Common mistakes

- **Doubling area to halve mismatch.** Mismatch scales as $1/\sqrt{\text{area}}$: halving it takes four times the area.
- **Running current mirrors in weak inversion.** High $g_m/I_D$ multiplies threshold mismatch into current mismatch.
- **Trusting common centroid against everything.** It cancels gradients, not layout-dependent effects; those need dummies and identical surroundings.
- **Treating corners as worst case for every specification.** Different specifications peak at different corners; simulate them all, plus Monte Carlo for mismatch.
- **Claiming a yield from a short Monte Carlo.** A hundred clean runs prove only a failure rate below about 3%.
- **Trimming at room temperature and quoting the result over temperature.** The drift remains.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Matching kept improving, unevenly [Established].** Random threshold variation follows oxide thickness: Kuhn et al. report that it stalled at 65 nm, the last silicon-oxynitride generation, and that high-k metal gates "restored Tox scaling" at 45 nm [5]; thin-body devices (FD-SOI and FinFETs), with little or no channel doping to fluctuate, match best. Published values run from 2.4 mV·µm for 28 nm bulk to about 1.3 mV·µm for FD-SOI and 0.7–1.4 mV·µm for a 14 nm SOI FinFET; Intel's 14 nm single-fin devices show σ(V_TH) of 19 mV (n) and 24 mV (p), "normally distributed out to +/-5σ" [6].
- **Analog area does not follow [Industry estimate].** A 2019 CICC tutorial by Loke et al. puts analog and mixed-signal area scaling at 0.8–0.9× per node against 0.5× for logic and SRAM, and warns that "parasitics and LDEs only get worse" [12]. Matching sets a minimum area for a given accuracy, whatever the lithography (20-12).
- **Layout-dependent effects are modeled, not avoided [Established].** Well proximity, diffusion length and isolation stress shift devices by amounts that depend on their neighborhood; at 16 nm FinFET a well-edge shift measured 1.87%, against 33% for 40 nm I/O devices [7]. Design kits include these effects, so post-layout extraction and simulation are mandatory sign-off steps.
- **Corners are giving way to statistics [Established].** Dongaonkar, Mudanai and Giles describe corner-based validation as having "fundamental limitations in predicting the circuit performance variation" [10]; foundry kits ship statistical global and mismatch models alongside the corners [10]. FinFET logic adds temperature-effect inversion, where delay falls with rising temperature, so the slow corner can be cold [10].

### Why it matters commercially

Matching and PVT robustness decide yield, test cost and qualification, and the learner's coverage areas meet them everywhere. **Automotive** parts must meet AEC-Q100 grades up to −40 to 150 °C and are tested at room and hot temperature per grade [11]: an automotive analog block carries a wider PVT space and a stricter yield target. **Wearables and IoT** depend on trimmed references and sensors, such as a digital temperature sensor guaranteed to ±0.1 °C over −20 to 50 °C [13]. In **AI datacenter** chips, random threshold variation sets SRAM's minimum supply voltage, and larger cells buy lower minimum voltages [5]: matching is a digital power problem too. For **M&A**, analog IP is tied to its process: porting it means re-layout, new statistical models and re-characterization, and a team's silicon-versus-Monte-Carlo correlation data is a good indicator of its maturity.

### Questions for engineering leaders

1. **"How does the measured offset or mismatch spread across lots compare with your Monte Carlo prediction?"** Strong: plots of silicon against simulation over several lots, with the ratio explained. Evasive: simulation only, or one lot.
2. **"How many Monte Carlo runs support the yield number, and how did you reach tails beyond 3σ?"** Strong: the run count, the confidence interval, and an importance-sampling or extrapolation method for high-sigma tails. Evasive: "we ran Monte Carlo and saw no failures."
3. **"Which parameters are trimmed, at what temperature, and what is left over temperature, after solder reflow and after aging?"** Strong: guaranteed limits over the full range plus typical drift terms stated separately. Evasive: the room-temperature trimmed value.
4. **"How much did post-layout simulation move your key specifications, and what layout-dependent effects are in sign-off?"** Strong: numbers before and after extraction, with WPE and stress modeled. Evasive: "the layout was done carefully."
5. **"How portable is this analog block to another foundry or node?"** Strong: an honest estimate of re-layout and re-characterization effort. Evasive: "it is just a shrink."

### Marketing vs Reality

- **"±0.05% reference."** TI's REF35 guarantees ±0.05% at 25 °C. Its 12 ppm/°C box-method temperature coefficient over −40 to 105 °C allows another **0.174**%, about **3.5** times the room-temperature figure (our arithmetic), and its long-term stability (40 ppm) and thermal hysteresis (70 ppm) are typical values only: the data sheet says long-term stability "is not ensured by design" [13].
- **"±0.1 °C sensor."** The TMP117's ±0.1 °C applies from −20 to 50 °C, measured with eight-sample averaging; over −55 to 150 °C it is ±0.3 °C [13]. A research sensor's "3σ inaccuracy of ±0.1 °C" is a statistical spread, not a guaranteed maximum [13].
- **"Verified at all corners."** Corners model global variation only, not mismatch, and one foundry's kit says its corners are "primarily for predicting static logic delay" [10]. Ask for Monte Carlo with mismatch and for the corners each specification is worst at.
- **"The Monte Carlo shows no failures."** Pelgrom noted that estimating σ from 100 samples is off by more than 10% about one time in six [1] (our χ² check: **15.9**%). Showing a 3σ failure rate needs about 1109 clean runs (Example 20-11.6).
- **"Our process has $A_{VT}$ = X."** Values differ by $\sqrt2$ depending on whether the author quotes the pair or the single device, and FinFET values depend on area normalization [5]; Drennan and McAndrew showed that mismatch does not follow the simple area law for wide-short and narrow-long devices [8]. Compare like with like.
- **"Common centroid takes care of it."** Topography effects reaching beyond 30 µm "are not reduced by common-centroid layout techniques" [8], and well-proximity shifts must be equalized by identical surroundings [7].
- **"Mismatch costs a hundred times kT" [Contested].** Kinget's 1996 abstract says "two orders", Pelgrom's 2013 slides "70x" and Kinget's 2005 abstract "several orders of magnitude" [3], [4]: the factor depends on how accuracy is defined (1σ or 3σ) and on the circuit. The direction is not contested: matching, not thermal noise, usually sets the power of uncalibrated precision circuits.

## 10. Concept check

**Q1.** Why does mismatch scale as $1/\sqrt{WL}$?

<details><summary>Answer</summary>

A device's parameter is the average of many independent local contributions; the number of contributions is proportional to area, and the standard deviation of an average of $n$ independent terms falls as $1/\sqrt n$.

</details>

**Q2.** Why should a current mirror run at low $g_m/I_D$ but a differential pair at high $g_m/I_D$?

<details><summary>Answer</summary>

A threshold error turns into a current error multiplied by $g_m/I_D$, so a mirror's current matching improves at low $g_m/I_D$ (large overdrive). A pair's offset is the threshold error plus the gain-factor error divided by $g_m/I_D$, so high $g_m/I_D$ minimizes the second term.

</details>

**Q3.** What does common-centroid layout cancel, and what does it not?

<details><summary>Answer</summary>

It cancels gradients up to the order its pattern matches (ABBA: linear; ABBABAAB: linear and quadratic). It does not cancel random mismatch (only area does) or layout-dependent effects such as well proximity and isolation stress, which need dummies and identical surroundings.

</details>

**Q4.** Why does better matching cost power, not just area?

<details><summary>Answer</summary>

Larger devices have more capacitance, and driving more capacitance at the same speed and swing takes proportionally more power: speed × accuracy² / power is fixed by the technology's matching constant.

</details>

**Q5.** What is latch-up, and how do guard rings help?

<details><summary>Answer</summary>

The parasitic PNP and NPN bipolar transistors in CMOS form a thyristor between the supplies; injected current can turn it on and short the supply. Guard rings collect injected carriers and lower the parasitic resistances that would bias the bipolars on.

</details>

**Q6.** A 200-run Monte Carlo shows no failures. What failure rate does that demonstrate at 95% confidence?

<details><summary>Answer</summary>

About 3/200 = 1.5%: the rule of three. Demonstrating rare failures needs far more runs or statistical extrapolation.

</details>

Problems: [20-11 problem set](../problems/20-11-problems.md) · Worked solutions: [20-11 solutions](../solutions/20-11-solutions.md)

## 11. Key terms

[Mismatch](../../../reference/glossary.md#mismatch) · [Pelgrom's law](../../../reference/glossary.md#pelgroms-law) · [Common-centroid layout](../../../reference/glossary.md#common-centroid-layout) · [Interdigitation](../../../reference/glossary.md#interdigitation) · [Dummy device](../../../reference/glossary.md#dummy-device) · [Well-proximity effect](../../../reference/glossary.md#well-proximity-effect) · [Guard ring](../../../reference/glossary.md#guard-ring) · [Latch-up](../../../reference/glossary.md#latch-up) · [PVT corner](../../../reference/glossary.md#pvt-corner) · [Monte Carlo simulation](../../../reference/glossary.md#monte-carlo-simulation) · [Trimming](../../../reference/glossary.md#trimming)

## 12. Connections

- **Previous:** [20-10](20-10-plls-and-jitter.md) (charge-pump mismatch makes reference spurs).
- **Builds on:** [20-01](20-01-analog-design-fundamentals-gm-id.md) ($g_m/I_D$), [03-04](../../03-probability-statistics-and-random-variables/chapters/03-04-joint-distributions-and-clt.md) and [03-05](../../03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md) (statistics), [19-11](../../19-digital-vlsi-design/chapters/19-11-place-route-signoff.md) (layout and extraction).
- **Next:** [20-12](20-12-why-analog-does-not-scale.md) asks why matching, headroom and noise keep analog from scaling like digital.
- **Used earlier:** the offsets and linearity limits of 20-05 (comparators), 20-06 and 20-07 (converter DNL and INL) and 20-09 (DAC yield) all rest on this chapter's laws.

## 13. Further study

- A. Hastings, *The Art of Analog Layout*, 2nd ed., Prentice Hall, 2005: the standard text on matching layout, guard rings and latch-up.
- M. J. M. Pelgrom, A. C. J. Duinmaijer and A. P. G. Welbers, "Matching properties of MOS transistors," *IEEE J. Solid-State Circuits*, 1989: the original area law.
- P. R. Kinget, "Device mismatch and tradeoffs in the design of analog circuits," *IEEE J. Solid-State Circuits*, 2005: the speed–accuracy–power limit.

## 14. Sources

1. M. J. M. Pelgrom, A. C. J. Duinmaijer and A. P. G. Welbers, "Matching properties of MOS transistors," *IEEE J. Solid-State Circuits*, vol. 24, no. 5, pp. 1433–1439, Oct. 1989, DOI 10.1109/JSSC.1989.572629 [R-353].
2. Lakshmikumar, Hadaway and Copeland, "Characterisation and modeling of mismatch in MOS transistors for precision analog design," *IEEE J. Solid-State Circuits*, vol. 21, no. 6, pp. 1057–1066, Dec. 1986, DOI 10.1109/JSSC.1986.1052648 [R-353].
3. P. R. Kinget, "Device mismatch and tradeoffs in the design of analog circuits," *IEEE J. Solid-State Circuits*, vol. 40, no. 6, pp. 1212–1224, June 2005, DOI 10.1109/JSSC.2005.848021; P. Kinget and M. Steyaert, CICC 1996, pp. 333–336, DOI 10.1109/CICC.1996.510569; P. Kinget and M. Steyaert, "Implications of transistor mismatch on analog circuit design and system performance," in *Analog VLSI Integration of Massive Parallel Signal Processing Systems*, Springer, 1997, DOI 10.1007/978-1-4757-2580-3_2 [R-353].
4. M. J. M. Pelgrom, H. P. Tuinhout and M. Vertregt, "Transistor matching in analog CMOS applications," *IEDM 1998*, pp. 915–918, DOI 10.1109/IEDM.1998.746503; M. Pelgrom, "Mismatch in deep-submicron and the consequences for analog designs," TWEPP-13 slides, CERN Indico, Sep. 2013 [R-353], [R-354].
5. Kuhn et al., "Process technology variation," *IEEE Trans. Electron Devices*, vol. 58, no. 8, pp. 2197–2208, Aug. 2011, DOI 10.1109/TED.2011.2121913 [R-354].
6. L. Rahhal, "Analysis and modeling of mismatch phenomena for advanced MOSFETs," PhD thesis, Univ. Grenoble Alpes, 2014 (HAL tel-01305050); Paul et al., IEDM 2013, DOI 10.1109/IEDM.2013.6724625; Giles et al., VLSI Technology Symposium 2015, pp. T150–T151, DOI 10.1109/VLSIT.2015.7223657 [R-354].
7. Hook et al., "Lateral ion implant straggle and mask proximity effect," *IEEE Trans. Electron Devices*, vol. 50, no. 9, pp. 1946–1951, Sep. 2003, DOI 10.1109/TED.2003.815371; Drennan, Kniffin and Locascio, "Implications of proximity effects for analog design," CICC 2006, pp. 169–176, DOI 10.1109/CICC.2006.320869; Grochowska and Pleskacz, DDECS 2024, pp. 37–40, DOI 10.1109/DDECS60919.2024.10508916 [R-355].
8. Gregor, "On the relationship between topography and transistor matching in an analog CMOS technology," *IEEE Trans. Electron Devices*, vol. 39, no. 2, pp. 275–282, 1992, DOI 10.1109/16.121683; Drennan and McAndrew, "Understanding MOSFET mismatch for analog design," *IEEE J. Solid-State Circuits*, vol. 38, no. 3, pp. 450–456, Mar. 2003, DOI 10.1109/JSSC.2002.808305 [R-355].
9. D. Harris, Harvey Mudd College E158 lecture slides (nonideal transistors, circuit pitfalls, interconnect), 2004; B. Boser, UC Berkeley EE240B lecture "Matching," 2016 [R-354], [R-356].
10. GlobalFoundries GF180MCU open PDK documentation, §2.4 and §9 (corner and statistical models), 2022; Dongaonkar, Mudanai and Giles, "From process corners to statistical circuit design methodology: opportunities and challenges," *IEEE Trans. Electron Devices*, vol. 66, no. 1, pp. 19–27, Jan. 2019, DOI 10.1109/TED.2018.2860929; temperature-effect inversion: ICCAD 2015, DOI 10.1109/ICCAD.2015.7372611 [R-356].
11. Renesas, "Temperature ranges" support page; Texas Instruments, qualification summary FAQ (AEC-Q100 grades), both read Nov. 2026 [R-356].
12. Loke et al., "Nanoscale CMOS implications on analog/mixed-signal design," CICC 2019 tutorial, DOI 10.1109/CICC.2019.8780267 [R-354].
13. Texas Instruments, REF35 data sheet SNAS809C (rev. Sep. 2024) and TMP117 data sheet SNOSD82D (rev. Sep. 2022); M. A. P. Pertijs, K. A. A. Makinwa and J. H. Huijsing, "A CMOS smart temperature sensor with a 3σ inaccuracy of ±0.1 °C from −55 °C to 125 °C," *IEEE J. Solid-State Circuits*, vol. 40, no. 12, pp. 2805–2815, Dec. 2005, DOI 10.1109/JSSC.2005.858476 [R-356].
