# Course 10 · Final Exam Solutions (Electronics I)

Exam: [README.md](README.md). Every number below is recomputed by [verify_10_exam.py](../verify/verify_10_exam.py) by an independent route.

**Grading.** Each [B] question is 8 points; give full credit to correct method with arithmetic slips of under 1%, half credit for a correct setup with a wrong region or model. Question 13 is graded on the derivation steps; Question 14 against its rubric.

---

## 1 · Diode models

(a) $(3 - 0.7)/1\text{ kΩ}$ = **2.3** mA.
(b) $V_T/I_D$ = 25.852 mV/2.3 mA = **11.24** Ω.

## 2 · A power supply

(a) $12\sqrt2$ = **16.97** V; minus two drops, $V_p$ = **15.57** V.
(b) Full-wave ripple at 120 Hz: $V_r = V_p/(2fRC)$ = 15.57/(2 × 60 × 500 × 10⁻³) = **0.2595** V.
(c) $V_p - V_r/2$ = **15.44** V, and $15.44/500$ = **30.88** mA.

## 3 · A Zener regulator

(a) At the lowest input (8 V) and full load, the resistor must pass 21 mA: $R = (8 - 5.1)/21\text{ mA}$ = **138.1** Ω.
(b) At 10 V and no load, all the current goes into the Zener: $(10 - 5.1)/138.1$ = **35.48** mA, dissipating $5.1 \times 35.48$ mA = **0.181** W.

## 4 · MOSFET bias

(a) $V_G = V_{GS} + I_DR_S$ with $I_D = V_{ov}^2$ mA/V² gives $2V_{ov}^2 + V_{ov} - 2.5 = 0$: $V_{ov}$ = **0.8956** V, $V_{GS}$ = **1.396** V, $I_D$ = **0.8022** mA.
(b) $V_D = 9 - 3 \times 0.8022$ = **6.593** V, $V_S$ = **1.604** V, $V_{DS}$ = **4.989** V > $V_{ov}$: saturation.
(c) $V_{ov}$ solves $2V_{ov}^2 + V_{ov} - 2.45 = 0$: $I_D$ = **0.7827** mA, **−2.43**%.

## 5 · BJT bias

(a) $V_{Th} = 10 \times 10/43$ = **2.326** V and $R_{Th}$ = 33 ∥ 10 = **7.674** kΩ.
(b) $I_E = (2.326 - 0.7)/(1 + 7.674/121)\text{ kΩ}$ = **1.529** mA; $I_C = \alpha I_E$ = **1.516** mA.
(c) $V_C = 10 - 3.3 \times 1.516$ = **4.997** V, $V_E$ = **1.529** V, $V_{CE}$ = **3.469** V: active.

## 6 · Small-signal parameters

(a) $g_m$ = 1.516 mA/25.852 mV = **58.64** mS; $r_\pi$ = **2.046** kΩ; $r_o$ = 80/1.516 mA = **52.77** kΩ; $g_mr_o$ = **3095**.
(b) $g_m = \sqrt{2 \times 2 \times 0.8022}$ mS = **1.791** mS; $r_o = 1/(0.05 \times 0.8022\text{ mA})$ = **24.93** kΩ; $g_mr_o$ = **44.66**.
(c) BJT **38.68** V⁻¹ against MOSFET **2.233** V⁻¹ ($2/V_{ov}$). The BJT's current responds to $V_T$, a small fixed voltage; this MOSFET's to its 0.9 V overdrive.

## 7 · Loading and cascades

(a) $\frac{20}{25} \times (-40) \times \frac{1}{1 + 4}$ = **−6.4**, or **16.12** dB.
(b) $\frac{20}{25} \times (-40) \times \frac{200}{204} \times 0.98 \times \frac{1000}{1050}$ = **−29.28**, or **29.33** dB: the follower recovers 13 dB.

## 8 · MOS amplifiers

(a) $-g_m(R_D \parallel r_o \parallel R_L) = -1.791 \times (3 \parallel 24.93 \parallel 10)$ = **−3.784**.
(b) $-g_m(R_D \parallel R_L)/(1 + g_mR_S) = -1.791 \times 2.308/4.583$ = **−0.902**.
(c) $1/(g_m + g_{mb}) = 1/(1.2 \times 1.791\text{ mS})$ = **465.2** Ω; the gain cannot exceed $1/(1 + \chi)$ = **0.8333**.

## 9 · BJT amplifiers

(a) $R_{in} = R_{Th} \parallel r_\pi$ = 7.674 ∥ 2.046 = **1.616** kΩ; input factor $1.616/2.616$ = **0.6177**; gain from the base $-g_m(3.3 \parallel 10 \parallel 52.77)$ = **−139.0**; overall **−85.84**.
(b) $r_e = \alpha/g_m$ = **16.91** Ω; $R_{in,base} = 121 \times (16.91 + 100)$ = **14.15** kΩ; $R_{in}$ = 7.674 ∥ 14.15 = **4.975** kΩ; gain from the base $-\alpha(3.3 \parallel 10)/(r_e + 100)$ = **−21.05**; overall $\frac{4.975}{5.975} \times (-21.05)$ = **−17.5**.

## 10 · Current mirrors

(a) Basic: $r_o$ = **50** kΩ. Cascode: $2r_o + g_mr_o^2$ = **2.6** MΩ.
(b) $V_{ov}$ = **0.2** V; $V_{TN} + 2V_{ov}$ = **0.85** V; $2V_{ov}$ = **0.4** V.
(c) $\sigma(\Delta V_{TH}) = 3.5/\sqrt{20}$ = 0.783 mV and $\sigma(\Delta I/I) = (2/0.2) \times 0.783$ mV = **0.783**%. For σ = 0.2% the threshold spread must be $\sigma(\Delta V_{TH}) = 0.002 \times 0.2/2$ = 0.2 mV, so $WL = (3.5/0.2)^2$ = **306** µm².

## 11 · Real op-amps

(a) $A_0$ = 10⁵: $10^5/(1 + 10^5/20)$ = **19.996**, an error of **0.0200**%.
(b) GBW/20 = **250** kHz; $\text{SR}/(2\pi V_p) = 2 \times 10^6/(2\pi \times 3)$ = **106.1** kHz.
(c) $0.5\text{ mV} \times 20$ = **10** mV.

## 12 · Applications

(a) $\Delta V_H = V_{DD}R_1/R_2$: $R_1 = 0.05 \times 100\text{ kΩ}/3.3$ = **1.515** kΩ; $V_{TH+} = 1.65(1 + R_1/R_2)$ = **1.675** V and $V_{TH-}$ = **1.625** V.
(b) $f_0 = \sqrt{\text{GBW}/(2\pi R_FC_{in})}$ = **1.262** MHz and $Q = \sqrt{2\pi\,\text{GBW}\,R_FC_{in}}$ = **15.85**. Solving $Q(C_F) = 1/\sqrt2$ from $R_F(C_{in} + C_F)s^2 + (1 + \omega_tR_FC_F)s + \omega_t = 0$: $C_F$ = **0.891** pF; then $f_0$ = **1.209** MHz, which is also the −3 dB bandwidth (Butterworth).

## 13 · Derivations

(a) $g_m = \partial i_C/\partial v_{BE} = I_C/V_T$. $r_\pi = (\partial i_B/\partial v_{BE})^{-1} = (g_m/\beta)^{-1} = \beta/g_m$. With $i_E = i_C(\beta + 1)/\beta$, $r_e = (\partial i_E/\partial v_{BE})^{-1} = \beta/[(\beta + 1)g_m] = \alpha/g_m$, so $r_\pi/r_e = \beta + 1$.
(b) At the source node: $g_m(v_g - v_s) - g_{mb}v_s - v_s/r_o = v_s/R_S$, so $v_s/v_g = g_m/(g_m + g_{mb} + 1/r_o + 1/R_S)$. Every term in the denominator is non-negative, so the gain is at most $g_m/(g_m + g_{mb}) = 1/(1 + \chi)$, reached only as $r_o$ and $R_S$ go to infinity.
(c) In the T model the emitter current is $i_e = v_b/(r_e + R_E)$ and the collector current $\alpha i_e$ flows through $R_C$: $A_v = -\alpha R_C/(r_e + R_E)$. For $R_E \gg r_e$ this is $-\alpha R_C/R_E$: $r_e$ (which carries the dependence on bias current, $r_e \approx V_T/I_E$) drops out, and β enters only through α, which changes by under 1% when β goes from 100 to 300.

## 14 · Diligence (12 points)

(a) $5\ \mu\text{W}/1.2\text{ V}$ = **4.17** µA in total; split between two input transistors, **2.08** µA each, whose largest transconductance (weak inversion) is $I/(nV_T)$ = **62.0** µS. Nothing is left for bias, references, the second stage or an ADC.

(b) Rubric: 2 points each for up to four of the following (or equivalent, well-argued points):

- **"Single stage, gain 1000."** One stage's gain is bounded by its intrinsic gain $g_mr_o$, tens at short channel lengths (10-04, 10-06); 1000 needs a cascode (headroom on 1.2 V is scarce, 10-08) or several stages. Ask for the topology and the intrinsic gain at the chosen length.
- **"120 dB CMRR."** At DC and in the lab? CMRR falls with frequency and with electrode-impedance mismatch (10-10 Problem 10); on a body, 50/60 Hz interference and its harmonics matter. Ask for CMRR at 50/60 Hz with a stated electrode-impedance imbalance.
- **"1 µV offset."** Achievable only with chopping or autozeroing (10-09), which brings switching artifacts and current noise; at 2 µA per device, matching alone gives millivolts unless the devices are huge (10-08). Ask for the offset distribution and the chopping architecture.
- **"5 µW."** The whole budget is 4.17 µA; ask what is included (reference, bias, ADC, digital) and at what noise. Input-referred noise at this current is a key ECG specification (12-10).
- **"1.2 V supply."** Headroom for cascodes and swing (10-06 §3.2, 10-08) is tight; ask for the output swing and the input common-mode range, especially with electrode DC offsets of hundreds of millivolts.

(c) 2 points for any two of: a chopper-stabilized instrumentation amplifier input; AC coupling or DC-offset servo for electrode offsets; a right-leg (common-mode) drive; a two-stage or folded-cascode architecture with gain split across stages; weak-inversion input devices for $g_m/I_D$; on-chip filtering before the ADC.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X10.1a | diode current | 2.3 | mA |
| X10.1b | small-signal resistance | 11.24 | Ω |
| X10.2a | transformer peak | 16.97 | V |
| X10.2b | peak output | 15.57 | V |
| X10.2c | ripple | 0.2595 | V |
| X10.2d | average output | 15.44 | V |
| X10.2e | load current | 30.88 | mA |
| X10.3a | series resistor | 138.1 | Ω |
| X10.3b | largest Zener current | 35.48 | mA |
| X10.3c | largest dissipation | 0.181 | W |
| X10.4a | V_ov | 0.8956 | V |
| X10.4b | V_GS | 1.396 | V |
| X10.4c | I_D | 0.8022 | mA |
| X10.4d | V_D | 6.593 | V |
| X10.4e | V_S | 1.604 | V |
| X10.4f | V_DS | 4.989 | V |
| X10.4g | I_D with V_TN + 50 mV | 0.7827 | mA |
| X10.4h | change | -2.43 | % |
| X10.5a | V_Th | 2.326 | V |
| X10.5b | R_Th | 7.674 | kΩ |
| X10.5c | I_E | 1.529 | mA |
| X10.5d | I_C | 1.516 | mA |
| X10.5e | V_C | 4.997 | V |
| X10.5f | V_E | 1.529 | V |
| X10.5g | V_CE | 3.469 | V |
| X10.6a | BJT g_m | 58.64 | mS |
| X10.6b | r_pi | 2.046 | kΩ |
| X10.6c | BJT r_o | 52.77 | kΩ |
| X10.6d | BJT intrinsic gain | 3095 | — |
| X10.6e | MOSFET g_m | 1.791 | mS |
| X10.6f | MOSFET r_o | 24.93 | kΩ |
| X10.6g | MOSFET intrinsic gain | 44.66 | — |
| X10.6h | BJT g_m/I | 38.68 | 1/V |
| X10.6i | MOSFET g_m/I | 2.233 | 1/V |
| X10.7a | gain without follower | -6.4 | — |
| X10.7b | gain without follower | 16.12 | dB |
| X10.7c | gain with follower | -29.28 | — |
| X10.7d | gain with follower | 29.33 | dB |
| X10.8a | CS gain, bypassed, with r_o | -3.784 | — |
| X10.8b | CS gain, degenerated | -0.902 | — |
| X10.8c | follower output resistance | 465.2 | Ω |
| X10.8d | follower gain limit | 0.8333 | — |
| X10.9a | R_in | 1.616 | kΩ |
| X10.9b | input factor | 0.6177 | — |
| X10.9c | gain from the base | -139.0 | — |
| X10.9d | overall gain | -85.84 | — |
| X10.9e | r_e | 16.91 | Ω |
| X10.9f | R_in at the base | 14.15 | kΩ |
| X10.9g | R_in of the stage | 4.975 | kΩ |
| X10.9h | gain from the base, degenerated | -21.05 | — |
| X10.9i | overall gain, degenerated | -17.5 | — |
| X10.10a | basic mirror R_out | 50 | kΩ |
| X10.10b | cascode R_out | 2.6 | MΩ |
| X10.10c | basic compliance | 0.2 | V |
| X10.10d | cascode compliance | 0.85 | V |
| X10.10e | low-voltage cascode compliance | 0.4 | V |
| X10.10f | σ(ΔI/I) | 0.783 | % |
| X10.10g | area for 0.2% | 306 | µm² |
| X10.11a | DC gain | 19.996 | — |
| X10.11b | gain error | 0.0200 | % |
| X10.11c | bandwidth | 250 | kHz |
| X10.11d | full-power bandwidth | 106.1 | kHz |
| X10.11e | offset at the output | 10 | mV |
| X10.12a | R_1 | 1.515 | kΩ |
| X10.12b | upper threshold | 1.675 | V |
| X10.12c | lower threshold | 1.625 | V |
| X10.12d | TIA f_0 without C_F | 1.262 | MHz |
| X10.12e | TIA Q without C_F | 15.85 | — |
| X10.12f | C_F | 0.891 | pF |
| X10.12g | bandwidth with C_F | 1.209 | MHz |
| X10.14a | total current | 4.17 | µA |
| X10.14b | per input transistor | 2.08 | µA |
| X10.14c | largest g_m per transistor | 62.0 | µS |
