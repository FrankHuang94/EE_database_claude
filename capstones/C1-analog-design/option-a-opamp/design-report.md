# C1 Option A · Reference Design Report: a Two-Stage CMOS Op-Amp

This is the reference solution to [Capstone C1, option A](../README.md). It shows the level of reasoning, calculation and verification the rubric expects. Work the capstone yourself first: the point is the method, not these particular widths. Every hand-calculated number below is recomputed by [verify_c1a.py](verify_c1a.py). Every simulated number comes from the netlists in [corners/](corners/) and [tt_extra.cir](tt_extra.cir), which CI re-runs, and is tabulated in [results.md](results.md).

**Prerequisites used:** [12-01](../../../courses/12-electronics-2/chapters/12-01-differential-pairs.md) (differential pairs), [12-03](../../../courses/12-electronics-2/chapters/12-03-frequency-response-miller-poles-zeros.md) (frequency response), [20-02](../../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md) (two-stage design and compensation) and [20-11](../../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-11-layout-matching-pvt.md) (PVT).

---

## 1. Specification

The brief's specification, restated with the conditions under which each item is checked:

| Parameter | Requirement | Checked at |
|---|---|---|
| Open-loop DC gain $A_0$ | ≥ 65 dB | all corners |
| Unity-gain frequency $f_u$ | ≥ 25 MHz | all corners |
| Phase margin, unity-gain follower | ≥ 60° | all corners |
| Slew rate, both edges | ≥ 20 V/µs | all corners |
| Output range (closed-loop gain within 1% of −1) | at least 0.25 V to $V_{DD}$ − 0.25 V | all corners |
| Tail-source saturation margin at $V_{CM}$ = 0.9 V | ≥ 50 mV | all corners |
| Supply power, including the bias branch | ≤ 500 µW | all corners |
| Input-referred noise at 1 MHz | ≤ 15 nV/√Hz | TT, 27 °C, 1.8 V |
| CMRR and PSRR+ at DC | ≥ 60 dB each | TT, 27 °C, 1.8 V |

Conditions: the C1 process ([models/c1_process.lib](../models/c1_process.lib)); $V_{DD}$ = 1.8 V ± 10%; −40 °C to 125 °C; process corners SS, TT, FF, SF and FS; load 2 pF; input common mode 0.9 V; a 20 µA reference current supplied from off the block.

## 2. Architecture

**Choice: a two-stage Miller-compensated amplifier with an NMOS input pair.** Figure 1 shows it. The first stage (M1–M5) gives gain and the differential-to-single-ended conversion. The second stage (M6, M7) gives more gain and the output swing. The Miller capacitor $C_c$, with its nulling resistor $R_z$, makes the first stage's output node the dominant pole ([20-02 §3.2](../../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md)).

```text
            VDD ─────┬──────────┬───────────────┬──────────
                     │          │               │
                M3 ─┤├┐    ┌┤├─ M4         M6 ─┤├┐ (PMOS)
                (diode) x ─┴──┘              │      │
                     │          ├── n1 ──────┘      ├── out ──┬── CL = 2 pF
                     │          │   │               │         │
                     │          │   └─ Rz ── Cc ────┤        GND
          inn ──┤├ M1          M2 ┤├── inp          │
                     └────┬─────┘                    │
                        tail                         │
                     M5 ┤├──── ibias ────────── M7 ┤├
     Iref (20 µA) ──► M8 (diode) ───┘                │
                     │                               │
            VSS ─────┴───────────────────────────────┴──────────
```

*Figure 1. The reference op-amp. M8 mirrors the 20 µA reference into the tail source M5 (40 µA) and the output sink M7 (160 µA). The node $x$ is the mirror's diode side; $n_1$ is the first stage's output.*

**Why not a folded cascode?** A single-stage folded cascode would meet the gain only with cascodes. Each cascode costs about $2V_{ov}$ of headroom at a 1.62 V supply, which squeezes the swing, and the specification asks for a wide output range into a 2 pF load. The two-stage design buys swing and gain cheaply. Its cost is the compensation capacitor, which limits the slew rate and must be designed carefully (§4.4).

**Why an NMOS input pair?** A common mode of 0.9 V is half the nominal supply. NMOS inputs give more transconductance for a given width and overdrive in this process ($KP_n/KP_p$ = **3.86**), and §5 shows the common-mode range comfortably contains 0.9 V. A PMOS pair would have suited a common mode near ground.

**Bias.** An ideal 20 µA reference flows into the diode M8. This treats bias generation as outside the block. In a real chip a beta-multiplier or bandgap-derived reference would supply it, and its own process and temperature variation would add to the corners here.

## 3. Strategy for corners

The corners move three things: $KP$ (±15% for process, and $(T/T_{nom})^{-1.5}$ for temperature), the threshold (±50 mV for process, and about −1 mV/K with temperature in these models), and the supply. With a fixed bias current, every transconductance scales as $\sqrt{KP}$. The worst case for speed is SS at 125 °C, where

$$
\frac{KP}{KP_{TT,27}} = 0.85 \times \left(\frac{398.15}{300.15}\right)^{-1.5} = 0.556, \qquad \frac{g_m}{g_{m,TT,27}} = \sqrt{0.556} = 0.746.
$$

So the design targets about 42 MHz at TT to leave $42.4 \times 0.746 = 31.7$ MHz at SS-hot, with margin over the 25 MHz requirement for the effects the hand analysis leaves out. Slew rate depends only on currents and $C_c$, so it barely moves with corners. Phase margin improves at slow corners and degrades at fast ones, because $g_{m1}$ and $g_{m6}$ move together but the crossover moves with $g_{m1}$ alone.

## 4. Hand sizing

Process values used ([models/c1_process.lib](../models/c1_process.lib)): $KP_n$ = 270 µA/V², $KP_p$ = 70 µA/V², $\lvert V_{TH0}\rvert$ = 0.45 V, $\lambda_n$ = 0.10 V⁻¹, $\lambda_p$ = 0.12 V⁻¹, $\gamma_n$ = 0.40 V^½, $2\phi_F$ = 0.80 V, $t_{ox}$ = 4.1 nm, so $C_{ox} = \varepsilon_{ox}/t_{ox}$ = **8.42** fF/µm², and gate overlap 0.3 fF/µm. All devices use $L$ = 0.5 µm, the length for which the deck's $\lambda$ is characterized. Square-law relations ([10-02](../../../courses/10-electronics-1/chapters/10-02-mosfet-dc-operation-and-biasing.md)): $I_D = \tfrac12 KP(W/L)V_{ov}^2$ and $g_m = 2I_D/V_{ov}$.

### 4.1 Compensation capacitor

A common starting rule is $C_c \ge 0.22C_L$ for 60° when the right-half-plane zero is pushed far away. This design takes $C_c$ = 1.5 pF (0.75 $C_L$). The larger value keeps the second pole well above the crossover even at fast corners. It costs slew rate (fixed by $I_5/C_c$) and first-stage current for a given $f_u$.

### 4.2 Input pair

The unity-gain frequency is $\omega_u \approx g_{m1}/C_c$. Choose $g_{m1}$ = **400** µS, giving $g_{m1}/(2\pi C_c)$ = **42.4** MHz. An overdrive of $V_{ov1}$ = 0.1 V keeps the pair's $V_{GS}$ low for common-mode range and gives $I_{D1} = g_{m1}V_{ov1}/2$ = **20** µA, so the tail current is $I_5$ = **40** µA. Then:

- slew rate $I_5/C_c$ = **26.7** V/µs, above 20 at every corner because it depends on no device parameter;
- $(W/L)_1 = 2I_{D1}/(KP_nV_{ov1}^2)$ = **14.8**, so $W_1$ = **7.41** µm, drawn 7.4 µm.

### 4.3 Second stage

For a second pole at least 2.2 times the crossover ($p_2 \approx g_{m6}/C_L$ when $C_c \gg C_1$), $g_{m6} \ge 2.2(C_L/C_c)g_{m1}$ = **1173** µS. Choose $g_{m6}$ = 1.6 mS for margin. With $V_{ov6}$ = 0.2 V, $I_6 = g_{m6}V_{ov6}/2$ = **160** µA, and $(W/L)_6 = 2I_6/(KP_pV_{ov6}^2)$ = **114.3**, so $W_6$ = **57.1** µm, drawn 57 µm.

### 4.4 Mirror, sources and the nulling resistor

- **Mirror M3, M4.** To make the systematic offset zero, the mirror's $V_{SG}$ must equal the one M6 needs, so M3 runs at M6's current density: $(W/L)_3 = (W/L)_6 \times I_{D1}/I_6$ = **14.29**, $W_3$ = **7.14** µm, drawn 7.1 µm.
- **Current sources.** At $V_{ov}$ = 0.15 V, $(W/L)_5 = 2I_5/(KP_nV_{ov5}^2)$ = **13.17**, so $W_5$ = **6.58** µm (drawn 6.6). M8 carries 20 µA at the same density, $W_8$ = **3.29** µm (drawn 3.3). M7 carries 160 µA, $W_7$ = **26.3** µm (drawn 26.4, so that $W_7/W_5$ = 4 exactly).
- **Nulling resistor.** Without it, the feedforward path through $C_c$ makes a right-half-plane zero at $g_{m6}/(2\pi C_c)$ = **169.8** MHz, only four times the crossover. That would cost several degrees of phase. $R_z = 1/g_{m6}$ = **625** Ω moves the zero to infinity ([20-02 §3.4](../../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md)). A larger $R_z$ could cancel $p_2$, but $g_{m6}$ moves with corners while a resistor does not, so the exact cancellation would not survive PVT.

## 5. Predicted performance

**Gain.** $A_1 = g_{m1}/[(\lambda_n + \lambda_p)I_{D1}]$ = **90.9** and $A_2 = g_{m6}/[(\lambda_n + \lambda_p)I_6]$ = **45.5**, so $A_0$ = **4132**, or **72.3** dB.

**Second pole and phase margin.** The first stage's output node carries $C_1 \approx C_{gs6} + C_{gd2,ov} + C_{gd4,ov}$, with $C_{gs6} = \tfrac23W_6LC_{ox} + W_6C_{ov}$ = **177** fF, so $C_1$ = **181** fF. The output node carries $C_2 \approx C_L + C_{gd6,ov} + C_{gd7,ov}$ = **2.025** pF. Junction capacitances are left out of both. Then

$$
p_2 = \frac{g_{m6}C_c}{C_1C_2 + C_c(C_1 + C_2)} \;\Rightarrow\; \frac{p_2}{2\pi} = \textbf{103.9}\ \text{MHz},
$$

**2.45** times $\omega_u$. The first-order estimate of phase margin is $90° - \arctan(\omega_u/p_2)$ = **67.8**°. A two-pole model refines it: the crossover is where $(f_{GBW}/f)/\sqrt{1 + (f/f_{p2})^2} = 1$, which gives $f_u$ = **39.7** MHz and PM = **69.1**°. The second pole pulls the crossover below $g_{m1}/(2\pi C_c)$.

**Common-mode range.** At the low end the tail source sits at the edge of saturation: $V_{CM,min} = V_{GS1} + V_{ov5}$. The pair's threshold rises with its source voltage, $\Delta V_{TH} = \gamma(\sqrt{2\phi_F + V_{SB}} - \sqrt{2\phi_F})$, which is **32.1** mV at $V_{SB}$ = 0.15 V. So $V_{CM,min}$ = **0.732** V. At the high end M1 leaves saturation when its gate exceeds $V_{DD} - V_{SG3} + V_{TH1}$, giving $V_{CM,max}$ = **1.79** V. At $V_{CM}$ = 0.9 V, iterating the body effect puts the tail node at **0.290** V, a margin of **140** mV over $V_{ov5}$.

**Output range.** The square-law edges are $V_{ov7}$ = 0.15 V and $V_{DD} - V_{ov6}$ = 1.60 V.

**Noise.** The thermal noise of the pair and the mirror, referred to the input, is $\bar v_n^2 = \frac{16kT}{3g_{m1}}(1 + g_{m3}/g_{m1})$ ([20-02 §3.9](../../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md)), with $g_{m3} = 2I_{D1}/V_{ov3}$ = 200 µS. That gives **9.10** nV/√Hz.

**Power.** $(20 + 40 + 160)$ µA × 1.8 V = **396** µW.

**At SS, 125 °C.** $KP$ falls to **0.556** of its TT value, $g_m$ to **0.746**, so $g_{m1}/(2\pi C_c)$ falls to **31.7** MHz.

## 6. Simulation at the typical corner

Nominal corner TT, 27 °C, 1.8 V, from [corners/tt-n.cir](corners/tt-n.cir) and [tt_extra.cir](tt_extra.cir):

| Quantity | Hand | Simulated | Why they differ |
|---|---|---|---|
| $A_0$ | 72.3 dB | **74.6** dB | Level-1 output conductance is $\lambda I_D/(1 + \lambda V_{DS})$, not $\lambda I_D$, so $r_o$ is larger than the hand formula assumes. |
| $f_u$ | 39.7 MHz (two-pole) | **39.3** MHz | Junction capacitances on $n_1$ lower $p_2$ slightly. |
| Phase margin | 69.1° (two-pole) | **68.2**° | The same, plus the pole that $R_z$ and $C_1$ form. |
| Slew rate | 26.7 V/µs | **25.6** / **24.0** V/µs (rise/fall) | The tail current is a little below 40 µA, because M5's $V_{DS}$ is lower than M8's, and the output node's own capacitance takes part of the current. |
| Output range | 0.15–1.60 V | **0.0914**–**1.649** V | A 1% gain-error criterion tolerates the first part of triode operation. |
| Tail margin at 0.9 V | 140 mV | **149** mV | |
| Noise at 1 MHz | 9.10 nV/√Hz | **8.98** nV/√Hz | |
| Power | 396 µW | **402** µW | Mirror ratios include $1 + \lambda V_{DS}$ terms. |
| CMRR, PSRR+ | — | **83.0** dB, **79.7** dB | Matched devices only. Mismatch, which level-1 does not model, would set CMRR in silicon. |

The hand design predicted the speed, slew, noise, power and bias quantities within about 10%; the gain differs by 2.3 dB because of the $\lambda$ model, and the two-pole model brought the crossover and margin within about 1%. That is the purpose of hand analysis: the simulator confirms the design and catches what the model leaves out, but it does not choose the widths.

## 7. PVT corners

The full table is in [results.md](results.md). Worst cases against the specification:

| Specification | Worst corner | Worst value | Requirement | Margin |
|---|---|---|---|---|
| $A_0$ | SS-H | **69.1** dB | ≥ 65 dB | 4.1 dB |
| $f_u$ | SS-H | **28.7** MHz | ≥ 25 MHz | 15% |
| Phase margin | FS-N | **64.4**° | ≥ 60° | 4.4° |
| Slew rate | SS-C (falling) | **23.3** V/µs | ≥ 20 V/µs | 3.3 V/µs |
| Power | FF-C | **443** µW | ≤ 500 µW | 11% |
| Tail margin | SS-C | **79.6** mV | ≥ 50 mV | 30 mV |
| Output high | SS-H | **1.405** V | ≥ 1.37 V | 35 mV |
| Output low | SS-H | **0.143** V | ≤ 0.25 V | 107 mV |

All requirements are met at all eleven corners. Three observations a reviewer should make:

1. **The worst corners differ by specification.** Speed and gain are worst at SS-hot, phase margin at FS, power at FF-cold-high and tail margin at SS-cold. Checking only "worst case" (SS-hot) would have missed the last three.
2. **FS sets the phase margin.** At FS, fast NMOS raise $g_{m1}$ and the crossover, while slow PMOS lower $g_{m6}$ and $p_2$. The margin falls to 64.4°, the tightest phase margin in the table. This is the mixed corner a design review should ask for.
3. **The hand prediction for SS-hot was optimistic.** It gave 31.7 MHz for $g_{m1}/(2\pi C_c)$. The simulation shows 28.7 MHz, about 9% lower: the two-pole crossover reduction plus the higher threshold eating into overdrive. The 42 MHz target at TT left enough room; a design aimed at exactly 25 MHz over 0.746 would have failed.

## 8. Tradeoffs and alternatives

| Knob | Improves | Costs |
|---|---|---|
| Larger $C_c$ | Phase margin, robustness to load | Slew rate; first-stage current for the same $f_u$ |
| Larger $g_{m6}$ ($I_6$) | Second pole, phase margin, output slew | Power (M6–M7 take 73% of the supply current) |
| Lower $V_{ov1}$ | $g_{m1}$ per µA, noise, common-mode range | Width (input capacitance); weak inversion eventually limits it |
| Longer $L$ | Gain ($\lambda$ falls) | Area, capacitance, speed; this deck characterizes only 0.5 µm |
| $R_z$ cancelling $p_2$ | Phase margin at TT | Robustness: the cancellation fails across corners and loads |

**What this design does not address**, and what a production design must: random mismatch (offset and CMRR), flicker noise, the bias generator's own PVT variation, layout parasitics, and an output stage for resistive loads. The [20-11](../../../courses/20-analog-and-mixed-signal-ic-design/chapters/20-11-layout-matching-pvt.md) chapter covers the first three.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| C1A.cox | gate-oxide capacitance per area | 8.42 | fF/µm² |
| C1A.kpss | KP at SS, 125 °C, relative to TT, 27 °C | 0.556 | — |
| C1A.gmss | g_m at SS, 125 °C, relative to TT, 27 °C | 0.746 | — |
| C1A.gbwss | g_m1/(2πC_c) at SS, 125 °C | 31.7 | MHz |
| C1A.gbwss0 | the same at TT, 27 °C | 42.4 | MHz |
| C1A.gm1 | input-pair transconductance | 400 | µS |
| C1A.gbw | g_m1/(2πC_c) | 42.4 | MHz |
| C1A.id1 | input-device current | 20 | µA |
| C1A.i5 | tail current | 40 | µA |
| C1A.sr | slew rate | 26.7 | V/µs |
| C1A.wl1 | (W/L)_1 | 14.8 | — |
| C1A.w1 | W_1 | 7.41 | µm |
| C1A.gm6min | minimum g_m6 | 1173 | µS |
| C1A.i6 | second-stage current | 160 | µA |
| C1A.wl6 | (W/L)_6 | 114.3 | — |
| C1A.w6 | W_6 | 57.1 | µm |
| C1A.wl3 | (W/L)_3 | 14.29 | — |
| C1A.w3 | W_3 | 7.14 | µm |
| C1A.wl5 | (W/L)_5 | 13.17 | — |
| C1A.w5 | W_5 | 6.58 | µm |
| C1A.w8 | W_8 | 3.29 | µm |
| C1A.w7 | W_7 | 26.3 | µm |
| C1A.zrhp | right-half-plane zero without R_z | 169.8 | MHz |
| C1A.rz | nulling resistor | 625 | Ω |
| C1A.a1 | first-stage gain | 90.9 | — |
| C1A.a2 | second-stage gain | 45.5 | — |
| C1A.a0 | DC gain | 4132 | — |
| C1A.a0db | DC gain | 72.3 | dB |
| C1A.cgs6 | C_gs of M6 | 177 | fF |
| C1A.c1 | first-stage output capacitance | 181 | fF |
| C1A.c2 | output-node capacitance | 2.025 | pF |
| C1A.p2 | second pole | 103.9 | MHz |
| C1A.p2r | p_2 over ω_u | 2.45 | — |
| C1A.pm1 | phase margin, first-order estimate | 67.8 | ° |
| C1A.fu2 | crossover, two-pole model | 39.7 | MHz |
| C1A.pm2 | phase margin, two-pole model | 69.1 | ° |
| C1A.dvt | body-effect threshold rise at V_SB = 0.15 V | 32.1 | mV |
| C1A.vcmmin | lowest input common mode | 0.732 | V |
| C1A.vcmmax | highest input common mode | 1.79 | V |
| C1A.vtail | tail node at V_CM = 0.9 V | 0.290 | V |
| C1A.tailmar | tail margin at V_CM = 0.9 V | 140 | mV |
| C1A.outhi | output high, square law | 1.60 | V |
| C1A.outlo | output low, square law | 0.15 | V |
| C1A.vn | input-referred noise | 9.10 | nV/√Hz |
| C1A.pwr | supply power | 396 | µW |
| C1A.share6 | share of the supply current in M6–M7 | 73 | % |
| S.tt.a0 | simulated A0, TT-N | 74.6 | dB |
| S.tt.ugf | simulated UGF, TT-N | 39.3 | MHz |
| S.tt.pm | simulated phase margin, TT-N | 68.2 | ° |
| S.tt.srr | simulated slew rate, rising, TT-N | 25.6 | V/µs |
| S.tt.srf | simulated slew rate, falling, TT-N | 24.0 | V/µs |
| S.tt.outlo | simulated output low, TT-N | 0.0914 | V |
| S.tt.outhi | simulated output high, TT-N | 1.649 | V |
| S.tt.m5mar | simulated tail margin, TT-N | 149 | mV |
| S.tt.vn | simulated noise, TT-N | 8.98 | nV/√Hz |
| S.tt.pwr | simulated power, TT-N | 402 | µW |
| S.tt.cmrr | simulated CMRR, TT-N | 83.0 | dB |
| S.tt.psrr | simulated PSRR+, TT-N | 79.7 | dB |
| S.min.a0 | worst A0 | 69.1 | dB |
| S.min.ugf | worst UGF | 28.7 | MHz |
| S.min.pm | worst phase margin | 64.4 | ° |
| S.min.sr | worst slew rate | 23.3 | V/µs |
| S.max.pwr | worst power | 443 | µW |
| S.min.m5mar | worst tail margin | 79.6 | mV |
| S.min.outhi | worst output high | 1.405 | V |
| S.max.outlo | worst output low | 0.143 | V |
| S.req.outhi | required output high at SS-H (V_DD − 0.25 V) | 1.37 | V |
| S.mar.a0 | worst-case gain margin over 65 dB | 4.1 | dB |
| S.mar.ugf | worst-case UGF margin over 25 MHz | 15 | % |
| S.mar.pm | worst-case phase margin over 60° | 4.4 | ° |
| S.mar.sr | worst-case slew margin over 20 V/µs | 3.3 | V/µs |
| S.mar.pwr | worst-case power margin under 500 µW | 11 | % |
| S.mar.m5 | worst-case tail margin over 50 mV | 30 | mV |
| S.mar.outhi | worst-case output-high margin | 35 | mV |
| S.mar.outlo | worst-case output-low margin | 107 | mV |
| S.gain.diff | simulated minus hand DC gain at TT-N | 2.3 | dB |
| S.err.ssh | SS-H UGF below the hand estimate | 9 | % |
| C1A.kpratio | KP_n/KP_p | 3.86 | — |
