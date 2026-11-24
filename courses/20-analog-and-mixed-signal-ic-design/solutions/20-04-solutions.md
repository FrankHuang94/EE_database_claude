# Solutions 20-04 · Low-Dropout Regulators

Problems: [20-04 problem set](../problems/20-04-problems.md) · Chapter: [20-04](../chapters/20-04-ldo-regulators.md). Every number below is recomputed by [verify_20_04.py](../verify/verify_20_04.py).

---

## Solutions

### Solution 20-04.1

(a) $\eta = V_{out}I_L/[V_{in}(I_L + I_Q)]$ with $I_L + I_Q$ = 50.03 mA. The pass device dissipates $(V_{in} - V_{out})I_L$.

- From 1.2 V: input power 1.2 × 50.03 mA = 60.04 mW, so η = 50/60.04 = **83.3**%; the pass device dissipates 0.2 V × 50 mA = **10.0** mW.
- From 3.3 V: input power **165.1** mW, so η = **30.3**%; the pass device dissipates 2.3 V × 50 mA = **115** mW.

(b) The buck converter draws 50 mW/0.9 = **55.6** mW from 3.3 V, about a third of the LDO's 165.1 mW.

**Check.** The LDO's efficiency is essentially $V_{out}/V_{in}$ (83.3% against 83.3%; 30.3% against 30.3%); the 30 µA of quiescent current costs only 0.06% here. An LDO is the right choice when the input is close to the output; from a much higher rail it wastes most of the power as heat.

### Solution 20-04.2

(a) The source follows the gate, so the gate must be at $V_{out} + V_{GS}$ = 1.2 + 0.75 = **1.95** V. The driver needs 0.15 V above that: $V_{in,min}$ = **2.10** V. Best-case efficiency there is 1.2/2.1 = **57.1**%.

(b) The PMOS needs only $V_{out} + V_{DO}$ = 1.35 V, where the bound is **88.9**%.

(c) An NMOS follower has a low open-loop output impedance (about $1/g_m$), which helps load transients and stability, and its gate is not referenced to $V_{in}$, which gives good supply rejection. Both are worth having when a higher auxiliary supply or a charge pump can provide the gate drive, which is common for on-chip regulators fed from a higher rail.

### Solution 20-04.3

With $V_{SG}$ = 1.3 V and $V_{SD}$ = 0.10 V, solving the long-channel triode equation for 100 mA gives $W_{long}$ = **2.470** mm. The field is 0.10 V/0.15 µm = 0.667 V/µm, so the velocity-saturation factor is 1 + 0.667/6.0 = **1.111**, and $W$ = **2.745** mm.

That is **1.462** times the design's 1.877 mm. The gate capacitance is $\tfrac23(2.745\text{ mm})(0.15\text{ µm})(8.6\text{ fF/µm}^2)$ = **2.361** pF.

The gate pole falls from 197 MHz to $g_{mb}/(2\pi C_g)$ = 2 mS/(2π × 2.361 pF) = **134.8** MHz.

**Check.** Lower dropout costs twice over: both the lower gate drive (1.3 V instead of 1.35 V) and the smaller $V_{SD}$ reduce the current per micrometer of width. The velocity-saturation penalty shrinks slightly because the field is lower.

### Solution 20-04.4

Solving $I_D(V_{SG})$ = 10 mA in saturation gives $V_{SG}$ = **0.602** V and $g_m/I_D$ = **9.84** S/A, so $g_{mp}$ = **98.4** mS. Then:

- $r_{ds}$ = 1.2 V/10 mA = **120** Ω and $R_L$ = 120 Ω, so $R_{out}$ = 120 ∥ 120 ∥ 1.2 MΩ = **60.0** Ω;
- $L_0$ = 100 × 0.5 × 98.4 mS × 60.0 Ω = **295** (**49.4** dB);
- the closed-loop output impedance is $R_{out}/(1 + L_0)$ = **0.203** Ω;
- the line regulation is $g_{ds}R_{out}/(1 + L_0)$ = (1/120) × 60.0/296 = **1.69** mV/V.

**Check.** Every quantity lies between the 100 µA and 100 mA values of Example 20-04.3: $L_0$ between 844 and 94.1, the output impedance between 7.07 Ω and 63.1 mΩ, the line regulation between 0.589 and 5.26 mV/V.

### Solution 20-04.5

(a) $\Delta V_{SG}$ = 0.675 V (Example 20-04.3), so $A_{EA} = \Delta V_{SG}/(\beta \cdot 5\text{ mV})$ = 0.675/(0.5 × 0.005) = **270** (**48.6** dB), and $g_{ma}$ = 270/100 kΩ = **2.70** mS.

(b) With the full loop gain:

| | Crossover | Phase margin |
|---|---|---|
| 100 µA | **60.7** kHz | **89.7**° |
| 100 mA | **5.59** MHz | **63.5**° |

The crossover is proportional to $A_{EA}$ (§3.4), so it rises by about 2.7 at both loads: from 22.5 to 60.7 kHz at light load. At full load the simple estimate would be 2.7 × 2.39 = 6.5 MHz, but the crossover now sits close to the error amplifier's 7.96 MHz pole. That pole both lowers it, to 5.59 MHz, and costs phase, so the margin drops from 77.5° to 63.5°. Regulation was bought with stability margin, exactly the trade-off of §6.

### Solution 20-04.6

Solving for the $C_L$ at which the full-load phase margin is 60° gives $C_L$ = **0.406** µF, with the crossover at **5.17** MHz.

The estimate $A_{EA}\beta g_{mp}/(2\pi C_L)$ = 100 × 0.5 × 0.3136/(2π × 0.406 µF) = **6.15** MHz is too high, because near $p_a$ the error amplifier's gain has started to fall. At 5.17 MHz, $|1 + jf/f_a| = \sqrt{1 + (5.17/7.96)^2}$ = 1.19, and 6.15/1.19 = 5.17 MHz.

**Check.** A data sheet would specify something like "1 µF minimum" to leave room for capacitor tolerance and the DC-bias derating of ceramic capacitors, which can lose half their capacitance at rated voltage.

### Solution 20-04.7

(a) The ESR zero is $1/(2\pi R_{ESR}C_L)$ = 1/(2π × 0.5 Ω × 1 µF) = **318** kHz. The crossover moves to **54.9** MHz with a phase margin of **82.4**°.

Above the zero, $Z_{out}$ stops falling and flattens at $R_{out} \parallel R_{ESR}$ = 6.00 Ω ∥ 0.5 Ω = 0.462 Ω. The loop gain then flattens at $A_{EA}\beta g_{mp}(R_{out} \parallel R_{ESR})$ = 100 × 0.5 × 0.3136 × 0.462 = **7.24**, and stays there until the error amplifier's pole rolls it off. It crosses unity near 7.24 × 7.96 MHz ≈ 58 MHz, lowered by the gate pole to 54.9 MHz: the loop has become an error-amplifier-dominant loop with a crossover above 50 MHz.

(b) With a 30 MHz parasitic pole:

| ESR | Crossover | Phase margin |
|---|---|---|
| 5 mΩ | **2.39** MHz | **73.0**° |
| 0.5 Ω | **35.6** MHz | **42.0**° |

With low ESR the extra pole is far above the crossover and costs only 4.5°. With high ESR the crossover moves to where every parasitic pole matters, and the margin collapses. This is the upper edge of the ESR window (15-12): too much ESR pushes the crossover up into the unmodeled poles. In this output-pole-dominant design, low ESR is harmless.

### Solution 20-04.8

From §3.5 at 2 MHz and 100 mA:

| | PSRR at 2 MHz | Output ripple (20 mV input) |
|---|---|---|
| $k$ = 1 | **46.6** dB | **93.1** µV |
| $k$ = 0 | **33.1** dB | **444** µV |

At 2 MHz the full-load loop still has gain (crossover 2.39 MHz), so the rejection is close to its DC value. The ground-referenced gate costs a factor of 4.8 in ripple.

### Solution 20-04.9

(a) Contributions at the output:

- reference ±0.5% of 1.2 V: **6.0** mV;
- divider ratio ±0.2%: $V_{out} = V_{REF}/\beta$, so a 0.2% ratio error moves the output by 0.2%: **2.4** mV;
- offset: ±2 mV/β = **4.0** mV;
- load regulation: 13.41 mV.

The worst case is the sum, **25.8** mV, or **2.15**% of 1.2 V.

(b) The three random terms in root-sum-square give $\sqrt{6.0^2 + 2.4^2 + 4.0^2}$ = **7.6** mV; adding the 13.41 mV systematic term gives **21.0** mV.

**Check.** Load regulation is the largest single term here, so a 40 dB error amplifier is not enough for a 1% regulator. That is one reason processor LDOs use high-gain or digitally assisted loops, and why some designs sense the output at the load (remote sense) to remove the drop in the wiring as well.

### Solution 20-04.10

(a) At 100 mA the crossover is 2.394 MHz, so $\Delta I/(\omega_cC_L)$ = 0.01/(2π × 2.394 MHz × 1 µF) = **0.665** mV, plus an ESR step of 0.01 × 5 mΩ = **0.050** mV. The final deviation is $\Delta I$ times the closed-loop output impedance, 0.01 × 63.1 mΩ = **0.631** mV.

(b) The linear step response of $Z_{out}/(1 + L)$ peaks at **0.631** mV, only **0.01**% above its final value. It reaches 90% of the final value in **98** ns; a single-pole loop would take $2.3/\omega_c$ = **153** ns, and the ESR step supplies the first **8**% at once.

There is essentially no overshoot because the full-load phase margin is 77.5°: the closed loop behaves almost like a single pole at $\omega_c$. As §3.6 noted, $\Delta I/(\omega_cC_L)$ is then just the small-signal load-regulation error, so the "dip" and the final value agree.

### Solution 20-04.11

(a) At 1 mA the pass device's $g_{mp}$ = **21.2** mS. The second pole is 21.2 mS/(2π × 200 pF) = **16.9** MHz. With a dominant pole far below, the phase margin is $90° - \arctan(f_u/f_{p2})$; 60° requires $f_u = f_{p2}\tan 30°$ = **9.76** MHz.

(b) $t_{resp} = C_o\Delta V/\Delta I$ = 200 pF × 60 mV/20 mA = **0.6** ns, equivalent to $1/(2\pi t_{resp})$ = **265** MHz of bandwidth.

(c) The light-load stability limit (under 10 MHz) and the transient requirement (hundreds of megahertz) are more than an order of magnitude apart, so a single error-amplifier loop cannot meet both. Designers add a fast local loop around the pass device (a flipped-voltage-follower or a capacitively coupled transient-enhancement path), raise the minimum load, bias the error amplifier adaptively with the load current, or accept more on-chip capacitance.

### Solution 20-04.12

(a) One unit current for one clock period changes the output by $I_u/(f_{clk}C_o)$ = 0.5 mA/(100 MHz × 100 nF) = **0.050** mV: a limit cycle of order 50 µV.

(b) 100 mA/0.5 mA = **200** switches (plus margin for process and supply corners).

(c) The array adds 0.5 mA per 10 ns, which is 50 mA/µs, so a 10 mA step takes **0.2** µs to follow. Meanwhile the shortfall falls linearly from 10 mA to zero, so the charge lost is ½ × 10 mA × 0.2 µs = 1 nC, and the dip is about 1 nC/100 nF = **10** mV.

**Check.** Ripple and speed pull in opposite directions: larger unit switches or a faster clock speed up the response but raise the ripple and the clock power. Hence coarse–fine arrays and event-driven controllers.

### Solution 20-04.13

(a) Input power:

| | Asleep | Active | Average (1% active) |
|---|---|---|---|
| LDO: $1.8(I_L + 1\text{ µA})$ | **10.8** µW | **5.40** mW | **64.7** µW |
| Buck: $0.9I_L/\eta$ | **7.5** µW | **3.18** mW | **39.2** µW |

The averages are 0.99 × asleep + 0.01 × active.

(b) The LDO's average power is **1.65** times the buck's. Its efficiency is 2.7 mW/5.40 mW = **50.0**% active and 4.5 µW/10.8 µW = **41.7**% asleep.

**Check.** Even at 1% duty the active term dominates both averages, so the LDO's 50% active efficiency is what hurts. Wearable power trees therefore use a buck for the large domains and LDOs where noise or area matters more, or where the input is already close to the output.

### Solution 20-04.14

(a) $p_a$ = 1/(2π × 100 kΩ × 2 pF) = **796** kHz.

| | Crossover | Phase margin |
|---|---|---|
| 100 µA | **22.5** kHz | **88.5**° |
| 100 mA | **1.30** MHz | **34.6**° |

(b) PSRR at 100 mA, $k$ = 1:

| | 100 kHz | 1 MHz |
|---|---|---|
| $C_a$ = 2 pF | **45.5** dB | **37.9** dB |
| Original ($C_a$ = 0.2 pF) | **45.6** dB | **45.9** dB |

(c) At light load the crossover (22.5 kHz) is still far below the new $p_a$, so almost nothing changes. At full load the crossover would be 2.39 MHz, above the new 796 kHz pole. The pole now cuts the crossover to 1.30 MHz and takes most of the margin: the loop has two significant poles below crossover.

PSRR suffers because, from §3.5, the rejection degrades from $p_a$ up to the crossover. With $p_a$ at 796 kHz, the 1 MHz ripple sits in exactly that window and loses 8 dB. Saving error-amplifier current costs both stability and mid-frequency rejection.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 20-04.1a | efficiency from 1.2 V | 83.3 | % |
| 20-04.1b | pass-device dissipation from 1.2 V | 10.0 | mW |
| 20-04.1c | input power from 3.3 V | 165.1 | mW |
| 20-04.1d | efficiency from 3.3 V | 30.3 | % |
| 20-04.1e | pass-device dissipation from 3.3 V | 115 | mW |
| 20-04.1f | buck input power | 55.6 | mW |
| 20-04.1g | input power from 1.2 V | 60.04 | mW |
| 20-04.2a | NMOS gate voltage | 1.95 | V |
| 20-04.2b | minimum input, NMOS | 2.10 | V |
| 20-04.2c | efficiency bound, NMOS | 57.1 | % |
| 20-04.2d | efficiency bound, PMOS | 88.9 | % |
| 20-04.3a | long-channel width | 2.470 | mm |
| 20-04.3b | velocity-saturation factor | 1.111 | — |
| 20-04.3c | width | 2.745 | mm |
| 20-04.3d | ratio to the design's width | 1.462 | — |
| 20-04.3e | gate capacitance | 2.361 | pF |
| 20-04.3f | gate pole | 134.8 | MHz |
| 20-04.3g | lateral field | 0.667 | V/µm |
| 20-04.4a | V_SG at 10 mA | 0.602 | V |
| 20-04.4b | g_m/I_D at 10 mA | 9.84 | S/A |
| 20-04.4c | g_mp at 10 mA | 98.4 | mS |
| 20-04.4d | r_ds at 10 mA | 120 | Ω |
| 20-04.4e | R_out at 10 mA | 60.0 | Ω |
| 20-04.4f | L_0 at 10 mA | 295 | — |
| 20-04.4g | L_0 at 10 mA in dB | 49.4 | dB |
| 20-04.4h | output impedance at 10 mA | 0.203 | Ω |
| 20-04.4i | line regulation at 10 mA | 1.69 | mV/V |
| 20-04.5a | required A_EA | 270 | — |
| 20-04.5b | required A_EA in dB | 48.6 | dB |
| 20-04.5c | required g_ma | 2.70 | mS |
| 20-04.5d | crossover at 100 uA | 60.7 | kHz |
| 20-04.5e | PM at 100 uA | 89.7 | ° |
| 20-04.5f | crossover at 100 mA | 5.59 | MHz |
| 20-04.5g | PM at 100 mA | 63.5 | ° |
| 20-04.6a | minimum C_L | 0.406 | µF |
| 20-04.6b | crossover at minimum C_L | 5.17 | MHz |
| 20-04.6c | estimated crossover | 6.15 | MHz |
| 20-04.6d | error-amplifier factor at 5.17 MHz | 1.19 | — |
| 20-04.7a | ESR zero | 318 | kHz |
| 20-04.7b | crossover, 0.5 ohm ESR | 54.9 | MHz |
| 20-04.7c | PM, 0.5 ohm ESR | 82.4 | ° |
| 20-04.7d | flat loop gain above the ESR zero | 7.24 | — |
| 20-04.7e | crossover, 5 mohm, 30 MHz pole | 2.39 | MHz |
| 20-04.7f | PM, 5 mohm, 30 MHz pole | 73.0 | ° |
| 20-04.7g | crossover, 0.5 ohm, 30 MHz pole | 35.6 | MHz |
| 20-04.7h | PM, 0.5 ohm, 30 MHz pole | 42.0 | ° |
| 20-04.7i | PM cost of the 30 MHz pole at 5 mohm | 4.5 | ° |
| 20-04.8a | PSRR k = 1 at 2 MHz | 46.6 | dB |
| 20-04.8b | output ripple k = 1 | 93.1 | µV |
| 20-04.8c | PSRR k = 0 at 2 MHz | 33.1 | dB |
| 20-04.8d | output ripple k = 0 | 444 | µV |
| 20-04.8e | ripple ratio k = 0 to k = 1 | 4.8 | — |
| 20-04.9a | reference contribution | 6.0 | mV |
| 20-04.9b | divider contribution | 2.4 | mV |
| 20-04.9c | offset contribution | 4.0 | mV |
| 20-04.9d | worst-case total | 25.8 | mV |
| 20-04.9e | worst-case total | 2.15 | % |
| 20-04.9f | RSS of the random terms | 7.6 | mV |
| 20-04.9g | RSS plus load regulation | 21.0 | mV |
| 20-04.10a | dip estimate | 0.665 | mV |
| 20-04.10b | ESR step | 0.050 | mV |
| 20-04.10c | final deviation | 0.631 | mV |
| 20-04.10d | linear peak | 0.631 | mV |
| 20-04.10e | overshoot | 0.01 | % |
| 20-04.10f | 90% time | 98 | ns |
| 20-04.10g | single-pole 90% time | 153 | ns |
| 20-04.10h | ESR step as fraction of final | 8 | % |
| 20-04.11a | g_mp at 1 mA | 21.2 | mS |
| 20-04.11b | second pole | 16.9 | MHz |
| 20-04.11c | largest unity-gain frequency | 9.76 | MHz |
| 20-04.11d | required response time | 0.6 | ns |
| 20-04.11e | equivalent bandwidth | 265 | MHz |
| 20-04.12a | limit-cycle ripple | 0.050 | mV |
| 20-04.12b | number of switches | 200 | — |
| 20-04.12c | time to follow the step | 0.2 | µs |
| 20-04.12d | dip | 10 | mV |
| 20-04.13a | LDO asleep | 10.8 | µW |
| 20-04.13b | LDO active | 5.40 | mW |
| 20-04.13c | LDO average | 64.7 | µW |
| 20-04.13d | buck asleep | 7.5 | µW |
| 20-04.13e | buck active | 3.18 | mW |
| 20-04.13f | buck average | 39.2 | µW |
| 20-04.13g | ratio LDO/buck | 1.65 | — |
| 20-04.13h | LDO efficiency active | 50.0 | % |
| 20-04.13i | LDO efficiency asleep | 41.7 | % |
| 20-04.14a | p_a/2 pi | 796 | kHz |
| 20-04.14b | crossover at 100 uA | 22.5 | kHz |
| 20-04.14c | PM at 100 uA | 88.5 | ° |
| 20-04.14d | crossover at 100 mA | 1.30 | MHz |
| 20-04.14e | PM at 100 mA | 34.6 | ° |
| 20-04.14f | PSRR at 100 kHz, slow EA | 45.5 | dB |
| 20-04.14g | PSRR at 1 MHz, slow EA | 37.9 | dB |
| 20-04.14h | PSRR at 100 kHz, original | 45.6 | dB |
| 20-04.14i | PSRR at 1 MHz, original | 45.9 | dB |
| 20-04.14j | PSRR loss at 1 MHz | 8 | dB |
